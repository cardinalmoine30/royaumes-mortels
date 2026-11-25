# -*- coding: utf-8 -*-
"""Remaster HD des textures du mod : chaque texture est redessinée à 2× sa résolution avec un vrai modelé.

Pour chaque face (d'un cube de mob, d'une partie de skin ou d'une icône entière) :
- les zones de même matière sont détectées (couleurs proches et contiguës) ;
- chaque zone reçoit un biseau (arête claire en haut à gauche, ombre en bas à droite), un modelé convexe
  (plus clair en haut), et un rendu de matière deviné par sa couleur : métal et or (reflet spéculaire,
  métal brossé, rayures), tissu (trame), cuir, peau (grain doux), os et pierre (pores), sombre (presque mat),
  lumineux (laissé intact pour rester émissif) ;
- la face entière reçoit l'éclairage de son orientation (dessus clair, dessous sombre, côtés en dégradé)
  et une occlusion ambiante dans les creux ;
- les petits détails (yeux, runes, emblèmes de 1 à 4 pixels) sont gardés nets.

Les modèles GeckoLib, le modèle du joueur et les icônes normalisent leurs UV : une texture 2× plus grande
s'affiche à la même place, simplement plus fine. Le script est idempotent (une texture déjà en HD est ignorée).
Usage : python3 outils/remaster.py [mobs|skins|objets|tout]"""
import colorsys
import glob
import json
import os
import sys

import numpy as np
from PIL import Image
from scipy import ndimage

ICI = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(ICI, "..", "src", "main", "resources", "assets", "royaumes")
S = 2
RNG = np.random.default_rng(1234)


# ------------------------------------------------------------------ zones de matière
def zones(lo, x, y, w, h, seuil=34):
    """Étiquettes des zones de couleur proche, contiguës, dans la face (x, y, w, h) ; -1 = transparent."""
    sub = lo[y:y + h, x:x + w].astype(int)
    lab = -np.ones((h, w), int)
    parent = list(range(w * h))

    def trouver(a):
        while parent[a] != a:
            parent[a] = parent[parent[a]]
            a = parent[a]
        return a

    opaque = sub[:, :, 3] > 0
    for j in range(h):
        for i in range(w):
            if not opaque[j, i]:
                continue
            c = sub[j, i, :3]
            for dj, di in ((0, -1), (-1, 0)):
                jj, ii = j + dj, i + di
                if jj >= 0 and ii >= 0 and opaque[jj, ii] and np.abs(sub[jj, ii, :3] - c).sum() < seuil:
                    a, b = trouver(j * w + i), trouver(jj * w + ii)
                    if a != b:
                        parent[a] = b
    for j in range(h):
        for i in range(w):
            if opaque[j, i]:
                lab[j, i] = trouver(j * w + i)
    return lab


def matiere(rgb):
    r, g, b = [v / 255.0 for v in rgb]
    hh, s, v = colorsys.rgb_to_hsv(r, g, b)
    deg = hh * 360
    if v > 0.86 and s > 0.45:
        return "lumineux"
    if v < 0.2:
        return "sombre"
    if 32 <= deg <= 58 and s > 0.38 and v > 0.5:
        return "or"
    if s < 0.22 and v > 0.38:
        return "os" if (deg < 60 and s > 0.08 and v > 0.7) else "metal"
    if 8 <= deg <= 40 and 0.18 < s < 0.62 and v > 0.42:
        return "peau"
    if 15 <= deg <= 40 and s >= 0.35 and v <= 0.5:
        return "cuir"
    return "tissu"


#            arête claire, arête sombre, modelé (bombé), bruit fin, bruit large, reflet, stries
REGLAGES = {"metal": (0.18, 0.32, 0.26, 3.0, 2.0, 0.32, 0.04), "or": (0.20, 0.32, 0.26, 2.5, 2.0, 0.36, 0.03),
            "os": (0.10, 0.24, 0.22, 6.0, 4.0, 0.05, 0.0), "peau": (0.06, 0.18, 0.22, 1.5, 3.0, 0.03, 0.0),
            "cuir": (0.08, 0.26, 0.20, 5.0, 5.0, 0.06, 0.0), "tissu": (0.06, 0.22, 0.20, 2.5, 7.0, 0.0, 0.0),
            "sombre": (0.10, 0.10, 0.08, 2.0, 2.0, 0.06, 0.0), "lumineux": (0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0)}


def distances(masque_bord):
    """Distance (en pixels HD) au bord le plus proche dans chaque direction : haut, gauche, bas, droite."""
    H, W = masque_bord.shape
    haut = np.zeros((H, W))
    bas = np.zeros((H, W))
    gauche = np.zeros((H, W))
    droite = np.zeros((H, W))
    for j in range(H):
        haut[j] = np.where(masque_bord[j], 0, (haut[j - 1] + 1) if j else 0)
    for j in range(H - 1, -1, -1):
        bas[j] = np.where(masque_bord[j], 0, (bas[j + 1] + 1) if j < H - 1 else 0)
    for i in range(W):
        gauche[:, i] = np.where(masque_bord[:, i], 0, (gauche[:, i - 1] + 1) if i else 0)
    for i in range(W - 1, -1, -1):
        droite[:, i] = np.where(masque_bord[:, i], 0, (droite[:, i + 1] + 1) if i < W - 1 else 0)
    return haut, gauche, bas, droite


def bruit_doux(h, w, echelle=3.0):
    n = RNG.normal(0, 1, (h, w))
    n = ndimage.gaussian_filter(n, echelle, mode="wrap")
    return n / (n.std() + 1e-6)


BRUITS = {}


def preparer_bruits(Hh, Wh):
    """Bruits tirés une fois pour toute l'image (un bruit lissé sur une toute petite face s'emballerait)."""
    BRUITS["fin"] = bruit_doux(Hh, Wh, 0.8)
    BRUITS["large"] = bruit_doux(Hh, Wh, 3.5)
    st = ndimage.gaussian_filter1d(RNG.normal(0, 1, (Hh, Wh)), 6, axis=1, mode="wrap")
    BRUITS["stries"] = st / (st.std() + 1e-6)


def epx(lab, col, silhouette=False):
    """Scale2x (EPX) : les diagonales et les coins s'arrondissent au lieu de rester en escalier.
    L'égalité est jugée sur les zones de matière (couleurs proches), pas sur la couleur exacte, pour rester
    efficace sur les textures bruitées. Renvoie les étiquettes et les couleurs en 2×."""
    h, w = lab.shape
    L = np.pad(lab, 1, mode="edge")
    Cp = np.pad(col, ((1, 1), (1, 1), (0, 0)), mode="edge")
    A, B, C, D = L[:-2, 1:-1], L[1:-1, 2:], L[1:-1, :-2], L[2:, 1:-1]          # haut, droite, gauche, bas
    cA, cB, cC, cD = Cp[:-2, 1:-1], Cp[1:-1, 2:], Cp[1:-1, :-2], Cp[2:, 1:-1]
    labH = np.repeat(np.repeat(lab, 2, 0), 2, 1)
    colH = np.repeat(np.repeat(col, 2, 0), 2, 1).astype(float)
    regles = (((0, 0), (C == A) & (C != D) & (A != B), A, cA), ((0, 1), (A == B) & (A != C) & (B != D), B, cB),
              ((1, 0), (D == C) & (D != B) & (C != A), C, cC), ((1, 1), (B == D) & (B != A) & (D != C), D, cD))
    for (dj, di), m, nl, nc in regles:
        m = m & (((lab >= 0) | (nl >= 0)) if silhouette else ((lab >= 0) & (nl >= 0)))
        vue = labH[dj::2, di::2]
        vue[m] = nl[m]
        vc = colH[dj::2, di::2]
        vc[m] = nc[m]
    return labH, colH


def face_hd(lo, out, x, y, w, h, orientation=None):
    """Repeint la face (x, y, w, h) de la texture basse résolution lo dans out (HD, flottants)."""
    lab = zones(lo, x, y, w, h)
    if (lab >= 0).sum() == 0:
        return
    labH, colH = epx(lab, lo[y:y + h, x:x + w])
    H, W = labH.shape
    sub = out[y * S:(y + h) * S, x * S:(x + w) * S]
    sub[:, :, :3] = colH[:, :, :3]
    bord = np.zeros((H, W), bool)
    bord[0, :] = bord[-1, :] = bord[:, 0] = bord[:, -1] = True
    diff_v = labH[1:, :] != labH[:-1, :]
    diff_h = labH[:, 1:] != labH[:, :-1]
    bord[1:, :] |= diff_v
    bord[:-1, :] |= diff_v
    bord[:, 1:] |= diff_h
    bord[:, :-1] |= diff_h
    dh, dg, db, dd = distances(bord)
    dist = ndimage.distance_transform_edt(~bord) + 0.5     # distance euclidienne au bord de zone
    zone = (slice(y * S, y * S + H), slice(x * S, x * S + W))
    fin, large, stries = BRUITS["fin"][zone], BRUITS["large"][zone], BRUITS["stries"][zone]
    ids, tailles = np.unique(lab[lab >= 0], return_counts=True)
    for z, taille in zip(ids, tailles):
        m = labH == z
        taille = m.sum() / (S * S)
        moyenne = lo[y:y + h, x:x + w][lab == z][:, :3].mean(axis=0)
        mat = matiere(moyenne)
        clair, sombre_, bombe, bf, bl, reflet, st = REGLAGES[mat]
        if mat == "lumineux":
            continue
        if taille <= 3:  # yeux, runes, rivets : nets, juste éclairés
            k = 1.04 + 0.04 * (dh <= S)
        else:
            rayon = max(2.0, min(7.0, np.sqrt(taille) * S / 2.2))
            r = np.clip(dist / rayon, 0, 1)
            t = dh / np.maximum(dh + db, 1)
            k = (1 - bombe / 2) + bombe * np.sqrt(r)                 # bombé : bords sombres, cœur plein
            k = k + 0.10 * (0.5 - t)                                  # lumière venant du haut
            k = k + clair * np.exp(-np.minimum(dh, dg) / 1.2)          # arête éclairée (haut, gauche)
            k = k - sombre_ * np.exp(-np.minimum(db, dd) / 1.4)        # arête dans l'ombre (bas, droite)
            if reflet:
                k = k + reflet * np.exp(-((t - 0.25) ** 2) / 0.012) * np.sqrt(r)
            k = k * (1 + 0.01 * bf * fin + 0.01 * bl * large)
            if st:  # métal brossé ; atténué sur les teintes très claires (peaux pâles, os, tissus blancs)
                k = k * (1 + st * stries * np.clip((215 - moyenne.mean()) / 60, 0.15, 1))
        for c in range(3):
            canal = sub[:, :, c]
            canal[m] = (canal * k)[m]
        if taille > 3:
            # éclaircissement des arêtes, comme sur une figurine peinte : un filet fin et clair sur les arêtes
            # hautes et gauches, teinté de la couleur de la zone (le noir s'éclaire en gris acier, le rouge en rose)
            filet = {"metal": 0.42, "or": 0.40, "sombre": 0.30, "os": 0.22, "cuir": 0.22}.get(mat, 0.16)
            arete = (np.minimum(dh, dg) == 0) & (np.minimum(db, dd) > 0)
            cible = 0.45 * moyenne + 0.55 * np.array([255.0, 250.0, 235.0])
            for c in range(3):
                canal = sub[:, :, c]
                canal[m & arete] = (canal + (cible[c] - canal) * filet)[m & arete]
        if taille >= 12:
            ys, xs = np.nonzero(lab == z)
            bx0, bx1, by0, by1 = xs.min() * S, (xs.max() + 1) * S, ys.min() * S, (ys.max() + 1) * S
            if mat in ("metal", "or") and bx1 - bx0 >= 8 and by1 - by0 >= 8:
                # rivets aux coins de la plaque : point clair, ombre portée en bas à droite
                for rx, ry in ((bx0 + 2, by0 + 2), (bx1 - 3, by0 + 2), (bx0 + 2, by1 - 3), (bx1 - 3, by1 - 3)):
                    if m[ry, rx]:
                        sub[ry, rx, :3] = np.minimum(255, sub[ry, rx, :3] * 1.45 + 20)
                        if ry + 1 < H and rx + 1 < W and m[ry + 1, rx + 1]:
                            sub[ry + 1, rx + 1, :3] *= 0.7
            elif mat == "cuir" and bx1 - bx0 >= 8 and by1 - by0 >= 8:
                jj, ii = np.mgrid[0:H, 0:W]
                couture = m & (np.abs(dist - 2.5) < 0.5) & ((ii + jj) % 3 == 0)
                sub[couture, :3] = np.minimum(255, sub[couture, :3] * 1.3 + 8)
            elif mat == "tissu" and moyenne.mean() < 185:  # trame (pas sur les teintes pâles : os, ivoire)
                jj, ii = np.mgrid[0:H, 0:W]
                trame = np.where((ii + jj) % 2 == 0, 1.022, 0.978)
                for c in range(3):
                    canal = sub[:, :, c]
                    canal[m] = (canal * trame)[m]
        if mat == "peau":  # la peau rougit légèrement dans les creux
            sub[:, :, 0][m] = np.minimum(255, sub[:, :, 0] * (1 + 0.05 * (1 - np.clip(dist / 4, 0, 1))))[m]
        if mat == "or":  # l'or garde sa chaleur dans les ombres
            sub[:, :, 2][m] = (sub[:, :, 2] * 0.94)[m]
    if orientation:
        L = {"up": 1.08, "top": 1.08, "down": 0.80, "bottom": 0.80}.get(orientation)
        if L is None:
            yy = np.linspace(0, 1, H)[:, None]
            sub[:, :, :3] *= (1.06 - 0.14 * yy)[:, :, None]
        else:
            sub[:, :, :3] *= L
    np.clip(sub, 0, 255, out=sub)


def remaster_image(img, faces):
    """faces : liste de (x, y, w, h, orientation) en coordonnées basse résolution."""
    lo = np.array(img.convert("RGBA"))
    out = np.repeat(np.repeat(lo, S, 0), S, 1).astype(float)
    preparer_bruits(out.shape[0], out.shape[1])
    vus = set()
    for x, y, w, h, o in faces:
        if (x, y, w, h) in vus:  # deux faces sur les mêmes pixels : un seul passage
            continue
        vus.add((x, y, w, h))
        if w <= 0 or h <= 0:
            continue
        x, y = max(0, x), max(0, y)
        w, h = min(w, lo.shape[1] - x), min(h, lo.shape[0] - y)
        face_hd(lo, out, int(x), int(y), int(w), int(h), o)
    out[:, :, 3] = np.repeat(np.repeat(lo[:, :, 3], S, 0), S, 1)
    return Image.fromarray(np.clip(out, 0, 255).astype(np.uint8))


def sauver(img, chemin):
    """PNG indexé (palette de 256 couleurs) quand la perte est invisible : 4 à 5 fois plus léger."""
    img = img.convert("RGBA")
    a = np.array(img).astype(int)
    q = img.quantize(256, method=Image.Quantize.FASTOCTREE, dither=Image.Dither.NONE)
    b = np.array(q.convert("RGBA")).astype(int)
    ecart = np.abs(a - b)[:, :, :3].max(axis=2)[a[:, :, 3] > 0]
    if ecart.size and np.percentile(ecart, 99.8) <= 18 and (b[:, :, 3] == a[:, :, 3]).all():
        q.save(chemin, optimize=True)
    else:
        img.save(chemin, optimize=True)


# ------------------------------------------------------------------ mobs (GeckoLib)
def faces_geo(geo):
    tex_w = geo["minecraft:geometry"][0]["description"]["texture_width"]
    fs = []
    for b in geo["minecraft:geometry"][0]["bones"]:
        for c in b.get("cubes", []):
            uv = c.get("uv")
            if isinstance(uv, dict):
                for f, d in uv.items():
                    (u, v), (uw, uh) = d["uv"], d["uv_size"]
                    u0, u1 = sorted((u, u + uw))
                    v0, v1 = sorted((v, v + uh))
                    fs.append((int(u0), int(v0), int(round(u1 - u0)), int(round(v1 - v0)), f))
            elif isinstance(uv, list):
                w, h, d = [int(round(t)) for t in c["size"]]
                u, v = uv
                for f, r in {"up": (u + d, v, w, d), "down": (u + d + w, v, w, d), "east": (u, v + d, d, h),
                             "north": (u + d, v + d, w, h), "west": (u + d + w, v + d, d, h),
                             "south": (u + 2 * d + w, v + d, w, h)}.items():
                    fs.append(r + (f,))
    return tex_w, fs


def densite(geo):
    """Texels par pixel de modèle (2 pour les textures d'origine, 4 pour celles peintes directement en HD)."""
    for b in geo["minecraft:geometry"][0]["bones"]:
        for c in b.get("cubes", []):
            uv = c.get("uv")
            if isinstance(uv, dict):
                for f, ax in (("north", 0), ("east", 2), ("up", 0)):
                    if f in uv and c["size"][ax] >= 1:
                        return abs(uv[f]["uv_size"][0]) / c["size"][ax]
            elif isinstance(uv, list) and c["size"][0] >= 1:
                return 1.0
    return 1.0


def mobs():
    n = 0
    for g in sorted(glob.glob(os.path.join(ASSETS, "geckolib", "models", "entity", "*.geo.json"))):
        nom = os.path.basename(g)[:-9]
        p = os.path.join(ASSETS, "textures", "entity", nom + ".png")
        if not os.path.exists(p):
            continue
        geo = json.load(open(g))
        if densite(geo) >= 3.5:  # déjà peinte en HD par outils/modeles (matières réelles)
            continue
        tex_w, fs = faces_geo(geo)
        img = Image.open(p)
        if img.width != tex_w:  # déjà en HD
            continue
        hd = remaster_image(img, fs)
        pg = os.path.join(ASSETS, "textures", "entity", nom + "_glowmask.png")
        if os.path.exists(pg):
            glow = np.array(Image.open(pg).convert("RGBA"))
            gH = np.repeat(np.repeat(glow, S, 0), S, 1)
            h = np.array(hd)
            masque = gH[:, :, 3] > 0
            gH[masque, :3] = h[masque, :3]
            sauver(Image.fromarray(gH), pg)
        sauver(hd, p)
        n += 1
    print("mobs : %d textures en HD" % n)


# ------------------------------------------------------------------ skins et armures portées
PARTS = {"head": (0, 0, 8, 8, 8), "hat": (32, 0, 8, 8, 8), "body": (16, 16, 8, 12, 4), "jacket": (16, 32, 8, 12, 4),
         "rarm": (40, 16, 4, 12, 4), "rsleeve": (40, 32, 4, 12, 4), "larm": (32, 48, 4, 12, 4), "lsleeve": (48, 48, 4, 12, 4),
         "rleg": (0, 16, 4, 12, 4), "rpants": (0, 32, 4, 12, 4), "lleg": (16, 48, 4, 12, 4), "lpants": (0, 48, 4, 12, 4)}


def faces_parties(hauteur):
    fs = []
    for nom, (u, v, w, h, d) in PARTS.items():
        if v + d + h > hauteur:
            continue
        fs += [(u + d, v, w, d, "top"), (u + d + w, v, w, d, "bottom"), (u, v + d, d, h, "right"),
               (u + d, v + d, w, h, "front"), (u + d + w, v + d, d, h, "left"), (u + 2 * d + w, v + d, w, h, "back")]
    return fs


def skin_hd(img):
    """Skin 64×64 ou texture d'équipement 64×32 -> 128×128 ou 128×64."""
    return remaster_image(img, faces_parties(img.height))


def skins():
    n = 0
    for p in glob.glob(os.path.join(ASSETS, "textures", "skin", "*.png")):
        img = Image.open(p)
        if img.width == 64:
            sauver(skin_hd(img), p)
            n += 1
    for p in glob.glob(os.path.join(ASSETS, "textures", "entity", "equipment", "*", "*.png")):
        img = Image.open(p)
        if img.width == 64:
            sauver(skin_hd(img), p)
            n += 1
    print("skins et armures portées : %d textures en HD" % n)


# ------------------------------------------------------------------ icônes
LUMIERE = np.array([-0.55, -0.62, 0.56])
LUMIERE = LUMIERE / np.linalg.norm(LUMIERE)


def objet_hd(img):
    """Icône 16×16 -> 32×32 : silhouette lissée (EPX), relief éclairé en haut à gauche, matières."""
    lo = np.array(img.convert("RGBA"))
    lab = zones(lo, 0, 0, lo.shape[1], lo.shape[0])
    labH, colH = epx(lab, lo, silhouette=True)
    opaque = colH[:, :, 3] > 0
    # relief : bombé de la silhouette + léger bombé de chaque zone de matière
    hauteur = np.minimum(ndimage.distance_transform_edt(opaque), 3.5)
    bord_zone = np.zeros_like(opaque)
    bord_zone[1:, :] |= labH[1:, :] != labH[:-1, :]
    bord_zone[:-1, :] |= labH[1:, :] != labH[:-1, :]
    bord_zone[:, 1:] |= labH[:, 1:] != labH[:, :-1]
    bord_zone[:, :-1] |= labH[:, 1:] != labH[:, :-1]
    hauteur = hauteur + 0.7 * np.minimum(ndimage.distance_transform_edt(~bord_zone), 2.0)
    hauteur = ndimage.gaussian_filter(hauteur, 0.9)
    gy, gx = np.gradient(hauteur)
    n = np.dstack([-gx, -gy, np.full_like(gx, 0.9)])
    n /= np.linalg.norm(n, axis=2, keepdims=True)
    eclat = n @ LUMIERE - LUMIERE[2] / np.linalg.norm([0, 0, 1])
    fin = ndimage.gaussian_filter(RNG.normal(0, 1, opaque.shape), 0.7)
    fin /= fin.std() + 1e-6
    out = colH.copy()
    for z in np.unique(labH[labH >= 0]):
        m = (labH == z) & opaque
        if not m.any():
            continue
        moyenne = colH[m][:, :3].mean(axis=0)
        mat = matiere(moyenne)
        lum = moyenne.mean()
        if mat == "lumineux" or lum < 42:  # contours et parties qui brillent : intacts
            continue
        force = {"metal": 0.85, "or": 0.8, "os": 0.6, "peau": 0.5, "cuir": 0.55, "tissu": 0.5, "sombre": 0.45}[mat]
        grain = 1 + 0.015 * fin * (2 if mat in ("cuir", "os", "tissu") else 1)
        clair = np.clip(eclat, 0, None) * force * 0.9      # les pentes éclairées montent vers le blanc sans le brûler
        sombre = np.clip(eclat, None, 0) * force * 1.1
        for c in range(3):
            canal = out[:, :, c]
            v = (canal + (255 - canal) * clair * (0.55 if lum > 170 else 1.0)) * (1 + sombre) * grain
            canal[m] = v[m]
        if mat in ("metal", "or") and lum < 200:  # reflet spéculaire sur les pentes les plus éclairées
            spec = np.clip(eclat - 0.2, 0, None) * (140 if mat == "metal" else 110) * (1 - lum / 255)
            for c, t in enumerate((1.0, 0.97, 0.86 if mat == "or" else 0.96)):
                canal = out[:, :, c]
                canal[m] = (canal + spec * t)[m]
    out[:, :, 3] = np.where(opaque, 255, 0)
    return Image.fromarray(np.clip(out, 0, 255).astype(np.uint8))


def objets():
    n = 0
    for p in glob.glob(os.path.join(ASSETS, "textures", "item", "**", "*.png"), recursive=True):
        if p.endswith("_palette.png"):
            continue
        img = Image.open(p)
        if img.size != (16, 16):
            continue
        sauver(objet_hd(img), p)
        n += 1
    print("objets : %d icônes en HD" % n)


if __name__ == "__main__":
    quoi = sys.argv[1] if len(sys.argv) > 1 else "tout"
    if quoi in ("mobs", "tout"):
        mobs()
    if quoi in ("skins", "tout"):
        skins()
    if quoi in ("objets", "tout"):
        objets()
