# -*- coding: utf-8 -*-
"""Scènes « en jeu » reconstituées : un petit moteur de rendu 3D (perspective, z-buffer, brouillard) qui
affiche les VRAIS modèles GeckoLib et les VRAIES textures du mod (créatures, skins de faction, blocs)
dans un décor de blocs, avec le HUD du mod par-dessus. Ce ne sont pas des captures du jeu, mais tout ce
qui y figure vient des fichiers du mod."""
import json
import math
import os
import random

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

ICI = os.path.dirname(os.path.abspath(__file__))
RACINE = os.path.join(ICI, "..", "..")
A = os.path.join(RACINE, "src", "main", "resources", "assets", "royaumes")
TEX = os.path.join(A, "textures")
W, H = 1280, 720
GUI = 3  # échelle d'interface : 1 pixel d'interface = 3 pixels écran
F = "/usr/share/fonts/truetype/dejavu/"


# ------------------------------------------------------------------ géométrie
def rot(p, r, piv):
    if not r or not any(r):
        return p
    x, y, z = p[0] - piv[0], p[1] - piv[1], p[2] - piv[2]
    rx, ry, rz = math.radians(-r[0]), math.radians(r[1]), math.radians(-r[2])
    y, z = y * math.cos(rx) - z * math.sin(rx), y * math.sin(rx) + z * math.cos(rx)
    x, z = x * math.cos(ry) + z * math.sin(ry), -x * math.sin(ry) + z * math.cos(ry)
    x, y = x * math.cos(rz) - y * math.sin(rz), x * math.sin(rz) + y * math.cos(rz)
    return (x + piv[0], y + piv[1], z + piv[2])


def coins(o, t, f, gonfle=0.0):
    x0, y0, z0 = o[0] - gonfle, o[1] - gonfle, o[2] - gonfle
    x1, y1, z1 = o[0] + t[0] + gonfle, o[1] + t[1] + gonfle, o[2] + t[2] + gonfle
    return {"north": ((x0, y1, z0), (x1, y1, z0), (x0, y0, z0)),
            "south": ((x1, y1, z1), (x0, y1, z1), (x1, y0, z1)),
            "east": ((x0, y1, z1), (x0, y1, z0), (x0, y0, z1)),
            "west": ((x1, y1, z0), (x1, y1, z1), (x1, y0, z0)),
            "up": ((x0, y1, z1), (x1, y1, z1), (x0, y1, z0)),
            "down": ((x0, y0, z0), (x1, y0, z0), (x0, y0, z1))}[f]


LUM = {"up": 1.12, "north": 0.95, "south": 0.8, "east": 0.88, "west": 0.75, "down": 0.55}


class Scene:
    def __init__(self, ciel_haut, ciel_bas, brouillard, portee=48):
        self.quads = []  # (p0, p1, p2, texture np, (u, v, w, h), lum, emissif)
        self.ciel = (ciel_haut, ciel_bas)
        self.brouillard = np.array(brouillard, float)
        self.portee = portee
        self.cache = {}

    def tex(self, chemin):
        if chemin not in self.cache:
            self.cache[chemin] = np.array(Image.open(chemin).convert("RGBA"))
        return self.cache[chemin]

    # --- blocs
    def bloc(self, x, y, z, chemin, faces=("up", "north", "south", "east", "west"), emissif=False, haut=None):
        T = self.tex(chemin)
        Th = self.tex(haut) if haut else T
        for f in faces:
            c = coins((x, y, z), (1, 1, 1), f)
            tt = Th if f == "up" else T
            self.quads.append((c[0], c[1], c[2], tt, (0, 0, tt.shape[1], tt.shape[0]), LUM[f], emissif))

    # --- modèle GeckoLib
    def modele(self, nom, x, y, z, lacet=0, echelle=1.0, pose=None, texture=None):
        g = json.load(open(os.path.join(A, "geckolib", "models", "entity", nom + ".geo.json")))["minecraft:geometry"][0]
        T = self.tex(texture or os.path.join(TEX, "entity", nom + ".png"))
        emis_p = os.path.join(TEX, "entity", nom + "_glowmask.png")
        os_ = {b["name"]: b for b in g["bones"]}
        pose = pose or {}
        for b in g["bones"]:
            chaine = []
            n = b
            while n is not None:
                chaine.append(n)
                n = os_.get(n.get("parent"))
            for c in b.get("cubes", []):
                for f, uvd in c.get("uv", {}).items():
                    u, v = uvd["uv"]
                    w, h = uvd["uv_size"]
                    pts = coins(c["origin"], c["size"], f, c.get("inflate", 0))
                    pts = [rot(p, c.get("rotation"), c.get("pivot", c["origin"])) for p in pts]
                    for bn in chaine:
                        r = pose.get(bn["name"]) or bn.get("rotation")
                        pts = [rot(p, r, bn.get("pivot", (0, 0, 0))) for p in pts]
                    pts = [self._monde(p, x, y, z, lacet, echelle) for p in pts]
                    if w < 0:
                        u, w = u + w, -w
                    if h < 0:
                        v, h = v + h, -h
                    self.quads.append((pts[0], pts[1], pts[2], T, (u, v, w, h), LUM[f], False))
        return self

    @staticmethod
    def _monde(p, x, y, z, lacet, e):
        px, py, pz = p[0] / 16 * e, p[1] / 16 * e, p[2] / 16 * e
        a = math.radians(lacet)
        return (x + px * math.cos(a) - pz * math.sin(a), y + py, z + px * math.sin(a) + pz * math.cos(a))

    # --- joueur avec un skin de faction (UV « boîte » des skins 64x64)
    def joueur(self, faction, x, y, z, lacet=0, pose=None):
        T = self.tex(os.path.join(TEX, "skin", faction + ".png"))
        pose = pose or {}
        parts = [("head", (-4, 24, -4), (8, 8, 8), (0, 0), (32, 0), 0.5, (0, 24, 0)),
                 ("body", (-4, 12, -2), (8, 12, 4), (16, 16), (16, 32), 0.25, (0, 24, 0)),
                 ("right_arm", (-8, 12, -2), (4, 12, 4), (40, 16), (40, 32), 0.25, (-5, 22, 0)),
                 ("left_arm", (4, 12, -2), (4, 12, 4), (32, 48), (48, 48), 0.25, (5, 22, 0)),
                 ("right_leg", (-4, 0, -2), (4, 12, 4), (0, 16), (0, 32), 0.25, (-2, 12, 0)),
                 ("left_leg", (0, 0, -2), (4, 12, 4), (16, 48), (0, 48), 0.25, (2, 12, 0))]
        for nom, o, t, uv, uv2, gon, piv in parts:
            for (bu, bv), g in ((uv, 0.0), (uv2, gon)):
                w, h, d = t
                faces = {"up": (bu + d, bv, w, d), "down": (bu + d + w, bv, w, d), "north": (bu + d, bv + d, w, h),
                         "south": (bu + 2 * d + w, bv + d, w, h), "east": (bu, bv + d, d, h), "west": (bu + d + w, bv + d, d, h)}
                for f, (u, v, ww, hh) in faces.items():
                    pts = [rot(p, pose.get(nom), piv) for p in coins(o, t, f, g)]
                    pts = [self._monde(p, x, y, z, lacet, 0.94) for p in pts]
                    self.quads.append((pts[0], pts[1], pts[2], T, (u, v, ww, hh), LUM[f], False))
        return self

    # --- rendu
    def rendre(self, cam, cible, fov=70):
        cam, cible = np.array(cam, float), np.array(cible, float)
        avant = cible - cam
        avant /= np.linalg.norm(avant)
        droite = np.cross(avant, [0, 1, 0])
        droite /= np.linalg.norm(droite)
        haut = np.cross(droite, avant)
        fpx = (W / 2) / math.tan(math.radians(fov) / 2)

        def proj(p):
            d = np.array(p) - cam
            zc = d @ avant
            return np.array([W / 2 + (d @ droite) * fpx / max(zc, 0.05), H / 2 - (d @ haut) * fpx / max(zc, 0.05)]), zc

        img = np.zeros((H, W, 3), float)
        hy = np.linspace(0, 1, H)[:, None]
        img[:] = (np.array(self.ciel[0]) * (1 - hy) + np.array(self.ciel[1]) * hy)[:, None, :][:, 0, :][:, None, :]
        zb = np.full((H, W), 1e9)
        for p0, p1, p2, T, (u, v, w, h), lum, emis in self.quads:
            (P0, z0), (P1, z1), (P2, z2) = proj(p0), proj(p1), proj(p2)
            if min(z0, z1, z2) < 0.1:
                continue
            Av, Bv = P1 - P0, P2 - P0
            det = Av[0] * Bv[1] - Av[1] * Bv[0]
            if abs(det) < 1e-4:
                continue
            P3 = P0 + Av + Bv
            xs = [P0[0], P1[0], P2[0], P3[0]]
            ys = [P0[1], P1[1], P2[1], P3[1]]
            x0, x1 = int(max(0, min(xs))), int(min(W, max(xs) + 1))
            y0, y1 = int(max(0, min(ys))), int(min(H, max(ys) + 1))
            if x1 <= x0 or y1 <= y0 or (x1 - x0) * (y1 - y0) > W * H:
                continue
            gx, gy = np.meshgrid(np.arange(x0, x1) + 0.5, np.arange(y0, y1) + 0.5)
            dx, dy = gx - P0[0], gy - P0[1]
            s = (dx * Bv[1] - dy * Bv[0]) / det
            t = (Av[0] * dy - Av[1] * dx) / det
            ok = (s >= 0) & (s < 1) & (t >= 0) & (t < 1)
            if not ok.any():
                continue
            prof = z0 + s * (z1 - z0) + t * (z2 - z0)
            tu = np.clip((u + s * w).astype(int), 0, T.shape[1] - 1)
            tv = np.clip((v + t * h).astype(int), 0, T.shape[0] - 1)
            col = T[tv, tu]
            ok &= col[:, :, 3] > 8
            sub = zb[y0:y1, x0:x1]
            ok &= prof < sub
            sub[ok] = prof[ok]
            rgb = col[:, :, :3].astype(float) * (1.0 if emis else lum)
            k = np.clip((prof - self.portee * 0.35) / (self.portee * 0.65), 0, 0.85)[:, :, None]
            rgb = rgb * (1 - k) + self.brouillard * k
            dst = img[y0:y1, x0:x1]
            dst[ok] = rgb[ok]
        self._proj = proj
        return Image.fromarray(np.clip(img, 0, 255).astype(np.uint8)).convert("RGBA")


# ------------------------------------------------------------------ textures de terrain procédurales
def terrain(nom, base, var=0.12, graine=1, dessus=None):
    chemin = os.path.join("/tmp", "rm_" + nom + ".png")
    r = random.Random(graine)
    im = Image.new("RGBA", (16, 16))
    for y in range(16):
        for x in range(16):
            c = dessus if (dessus and y < 3 + (x * 7 % 3)) else base
            k = 1 + (r.random() - 0.5) * 2 * var
            im.putpixel((x, y), tuple(max(0, min(255, int(v * k))) for v in c) + (255,))
    im.save(chemin)
    return chemin


# ------------------------------------------------------------------ effets et HUD
def lueur(img, pts, couleur, rayon=6, n=1):
    calque = Image.new("RGBA", img.size)
    d = ImageDraw.Draw(calque)
    for (x, y) in pts:
        d.ellipse((x - rayon, y - rayon, x + rayon, y + rayon), fill=couleur + (200,))
    flou = calque.filter(ImageFilter.GaussianBlur(rayon * 1.5))
    img.alpha_composite(flou)
    img.alpha_composite(calque)


def eclair(img, a, b, couleur=(200, 230, 255), graine=3):
    r = random.Random(graine)
    pts = [a]
    for i in range(1, 12):
        t = i / 12
        pts.append((a[0] + (b[0] - a[0]) * t + r.uniform(-18, 18), a[1] + (b[1] - a[1]) * t + r.uniform(-10, 10)))
    pts.append(b)
    calque = Image.new("RGBA", img.size)
    d = ImageDraw.Draw(calque)
    d.line(pts, fill=couleur + (255,), width=18)
    img.alpha_composite(calque.filter(ImageFilter.GaussianBlur(10)))
    d2 = ImageDraw.Draw(img)
    d2.line(pts, fill=(255, 255, 255), width=5)


def gui_img(nom):
    return Image.open(os.path.join(TEX, "gui", "aos", nom + ".png")).convert("RGBA")


def coller(img, src, x, y, w=None, h=None):
    w, h = w or src.width, h or src.height
    img.alpha_composite(src.resize((w * GUI, h * GUI), Image.NEAREST), (x * GUI, y * GUI))


def texte(d, x, y, s, c=(255, 255, 255), t=9, centre=False):
    f = ImageFont.truetype(F + "DejaVuSans-Bold.ttf", t * 2)
    if centre:
        x -= d.textlength(s, font=f) / GUI / 2
    d.text((x * GUI + 3, y * GUI + 3), s, font=f, fill=(30, 30, 30))
    d.text((x * GUI, y * GUI), s, font=f, fill=c)


def hud(img, faction_num, faction_nom, niveau, royaume, capacite, energie, maxi, vent, objet=None, sort=None, couleur_sort=(255, 220, 160)):
    gw, gh = W // GUI, H // GUI
    d = ImageDraw.Draw(img)
    emb = gui_img("emblemes")
    i = faction_num - 1
    d.rectangle((4 * GUI, 4 * GUI, 30 * GUI, 30 * GUI), fill=(12, 20, 40, 200), outline=(212, 166, 58), width=GUI)
    coller(img, emb.crop(((i % 8) * 32, (i // 8) * 32, (i % 8) * 32 + 32, (i // 8) * 32 + 32)), 6, 6, 22, 22)
    texte(d, 34, 6, faction_nom, (242, 210, 122))
    texte(d, 34, 16, "Niveau %d · Royaume %s" % (niveau, royaume), (240, 230, 210), 8)
    texte(d, 34, 26, capacite, (242, 210, 122), 8)
    h = gui_img("hud")
    gx, gy = 6, gh - 22
    coller(img, h.crop((vent * 16, 32, vent * 16 + 16, 48)), gx, gy - 2)
    coller(img, h.crop((0, 0, 104, 12)), gx + 18, gy + 2)
    coller(img, h.crop((0, 16, max(1, int(100 * energie / maxi)), 24)), gx + 20, gy + 4)
    texte(d, gx + 20, gy - 9, "%d / %d" % (energie, maxi), (200, 190, 255), 8)
    cx = gw // 2
    d.rectangle(((cx - 91) * GUI, (gh - 22) * GUI, (cx + 91) * GUI, gh * GUI - 1), fill=(30, 30, 30, 190), outline=(10, 10, 10), width=GUI)
    for k in range(9):
        d.rectangle(((cx - 90 + k * 20) * GUI, (gh - 21) * GUI, (cx - 72 + k * 20) * GUI, (gh - 2) * GUI), outline=(110, 110, 110), width=2)
    d.rectangle(((cx - 92) * GUI, (gh - 23) * GUI, (cx - 68) * GUI, (gh - 1) * GUI), outline=(240, 240, 240), width=GUI)
    if objet:
        coller(img, Image.open(objet).convert("RGBA"), cx - 89, gh - 19, 16, 16)
    for k in range(10):
        d.ellipse(((cx - 91 + k * 8) * GUI, (gh - 39) * GUI, (cx - 84 + k * 8) * GUI, (gh - 32) * GUI), fill=(210, 30, 30), outline=(60, 0, 0))
        d.ellipse(((cx + 84 - k * 8) * GUI, (gh - 39) * GUI, (cx + 91 - k * 8) * GUI, (gh - 32) * GUI), fill=(170, 110, 50), outline=(60, 30, 0))
    d.rectangle(((cx - 91) * GUI, (gh - 29) * GUI, (cx + 91) * GUI, (gh - 26) * GUI), fill=(20, 40, 10))
    d.rectangle(((cx - 91) * GUI, (gh - 29) * GUI, (cx + 30) * GUI, (gh - 26) * GUI), fill=(128, 255, 32))
    if sort:
        texte(d, cx, gh - 68, sort, couleur_sort, 9, centre=True)
    d.line(((W // 2 - 10), H // 2, (W // 2 + 10), H // 2), fill=(255, 255, 255), width=2)
    d.line((W // 2, H // 2 - 10, W // 2, H // 2 + 10), fill=(255, 255, 255), width=2)


def legende(img, s):
    d = ImageDraw.Draw(img)
    f = ImageFont.truetype(F + "DejaVuSans.ttf", 15)
    tw = d.textlength(s, font=f)
    d.rectangle((W - tw - 24, 8, W - 8, 34), fill=(0, 0, 0, 150))
    d.text((W - tw - 16, 13), s, font=f, fill=(230, 230, 230))
