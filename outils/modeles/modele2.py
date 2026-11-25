# -*- coding: utf-8 -*-
"""Moteur de modèles GeckoLib v2 :
- UV par face en double densité (2 texels par pixel de modèle) → détails fins ;
- matières peintes procéduralement (métal, or, tissu, cuir, peau, écailles, os, bois, fourrure, pierre, éther, corne…)
  avec ombrage (lumière venant du haut), arêtes, rivets, plis, grain ;
- rotation de cubes (cornes, ailes, lames inclinées) ;
- texture « _glowmask » pour les parties lumineuses (yeux, runes, malepierre) ;
- aperçu 3/4 par rastérisation avec tampon de profondeur."""
import json, math, os, random, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont

RACINE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(RACINE, "outils"))
ASSETS = os.path.join(RACINE, "src/main/resources/assets/royaumes")
D = 2   # texels par unité de modèle

DIMS = {"north": (0, 1), "south": (0, 1), "east": (2, 1), "west": (2, 1), "up": (0, 2), "down": (0, 2)}


def clamp(v):
    return max(0, min(255, int(v)))


def mul(c, k):
    return tuple(clamp(v * k) for v in c[:3])


def mix(a, b, t):
    return tuple(clamp(a[i] * (1 - t) + b[i] * t) for i in range(3))


class Cube:
    def __init__(self, bone, o, t, mat, rot=None, pivot=None, faces=None):
        self.bone, self.o, self.t, self.mat = bone, tuple(o), tuple(t), mat
        self.rot, self.pivot = rot, pivot
        self.faces = faces or {}
        self.uv = {}

    def taille_face(self, f):
        a, b = DIMS[f]
        return self.t[a], self.t[b]


class Modele:
    def __init__(self, nom):
        self.nom = nom
        self.bones = []
        self.cubes = []
        self.tex = 256

    def bone(self, nom, parent, pivot):
        if any(b[0] == nom for b in self.bones):
            return
        self.bones.append((nom, parent, tuple(pivot)))

    def cube(self, bone, o, t, mat, rot=None, pivot=None, **faces):
        if "toutes" in faces:
            f = faces.pop("toutes")
            for k in ("north", "south", "east", "west"):
                faces.setdefault(k, f)
        c = Cube(bone, o, t, mat, rot, pivot, faces)
        self.cubes.append(c)
        return c

    # ---------------------------------------------------------------- UV
    def placer_uv(self):
        faces = []
        for c in self.cubes:
            for f in DIMS:
                fw, fh = c.taille_face(f)
                tw, th = int(round(fw * D)), int(round(fh * D))
                if tw > 0 and th > 0:
                    faces.append((th, tw, c, f))
        faces.sort(key=lambda x: (-x[0], -x[1]))
        for W in (128, 256, 512, 1024):
            x = y = haut = 0
            ok = True
            pos = []
            for th, tw, c, f in faces:
                if x + tw > W:
                    x, y, haut = 0, y + haut, 0
                if y + th > W or tw > W:
                    ok = False
                    break
                pos.append((c, f, x, y, tw, th))
                x += tw
                haut = max(haut, th)
            if ok:
                self.tex = W
                for c, f, x, y, tw, th in pos:
                    c.uv[f] = (x, y, tw, th)
                return
        raise ValueError("modèle trop grand")

    # ---------------------------------------------------------------- peinture
    def peindre(self, mats, graine=11):
        """Texture en haute définition (2 × D texels par pixel de modèle) et son masque lumineux.
        La peinture basse résolution (matières + dessins) sert de calque des dessins ; les matières sont
        repeintes en HD par matieres_hd, les dessins agrandis en Scale2x. Les UV sont ensuite doublées."""
        import matieres_hd as MH
        rng = random.Random(graine)
        im = Image.new("RGBA", (self.tex, self.tex), (0, 0, 0, 0))
        px = im.load()
        d = ImageDraw.Draw(im)
        lueurs = set()
        for c in self.cubes:
            m = mats[c.mat]
            for f, (x0, y0, w, h) in c.uv.items():
                peindre_matiere(px, x0, y0, w, h, f, m, rng)
                if m["type"] == "lueur":
                    lueurs.add((x0, y0, w, h))
        base = np.array(im)
        def parties(fn):
            return getattr(fn, "parties", [fn])

        for c in self.cubes:
            for f, (x0, y0, w, h) in c.uv.items():
                fn = c.faces.get(f)
                if fn:
                    for p in parties(fn):
                        if not hasattr(p, "hd"):   # les dessins qui ont leur version HD ne passent pas par l'agrandissement
                            p(d, x0, y0, w, h, px)
        lo = np.array(im)
        # ---- haute définition
        T = 2 * self.tex
        hd = np.zeros((T, T, 4), float)
        dessins = np.zeros((T, T, 4), float)
        masque_dessins = np.zeros((T, T), bool)
        nrng = np.random.default_rng(graine * 7919 + len(self.cubes))
        for c in self.cubes:
            m = mats[c.mat]
            for f, (x0, y0, w, h) in c.uv.items():
                MH.peindre_face(hd, 2 * x0, 2 * y0, 2 * w, 2 * h, f, m, nrng)
        for c in self.cubes:
            for f, (x0, y0, w, h) in c.uv.items():
                fn = c.faces.get(f)
                if not fn:
                    continue
                zone = (slice(2 * y0, 2 * (y0 + h)), slice(2 * x0, 2 * (x0 + w)))
                resultats = [MH.decors_hd(hd, lo, base, x0, y0, w, h, f, mats[c.mat]["c"])]
                resultats += [p.hd(hd, 2 * x0, 2 * y0, 2 * w, 2 * h) for p in parties(fn) if hasattr(p, "hd")]
                for r in resultats:
                    if r:
                        mk, couleur = r
                        masque_dessins[zone] |= mk
                        dessins[zone][mk] = couleur[mk]
        arr = np.clip(hd, 0, 255).astype(np.uint8)
        # masque lumineux : faces « lueur » + pixels (dessins compris) de la couleur d'une lueur
        g = np.zeros_like(arr)
        for (x0, y0, w, h) in lueurs:
            g[2 * y0:2 * (y0 + h), 2 * x0:2 * (x0 + w)] = arr[2 * y0:2 * (y0 + h), 2 * x0:2 * (x0 + w)]
        cl = [m["c"] for m in mats.values() if m["type"] == "lueur"]
        plat = np.where(masque_dessins[..., None], dessins, arr.astype(float))
        for col in cl:
            dist = np.abs(plat[:, :, :3] - np.array(col)).sum(axis=2)
            masque = (dist < 40) & (arr[:, :, 3] > 0)
            g[masque] = arr[masque]
        # les UV passent à la haute définition
        self.tex = T
        for c in self.cubes:
            c.uv = {f: (2 * x0, 2 * y0, 2 * w, 2 * h) for f, (x0, y0, w, h) in c.uv.items()}
        return Image.fromarray(arr), Image.fromarray(g)

    # ---------------------------------------------------------------- export
    def geo(self):
        bones = []
        for nom, parent, pivot in self.bones:
            b = {"name": nom, "pivot": list(pivot)}
            if parent:
                b["parent"] = parent
            cs = []
            for c in self.cubes:
                if c.bone != nom:
                    continue
                cd = {"origin": [round(v, 3) for v in c.o], "size": [round(v, 3) for v in c.t],
                      "uv": {f: {"uv": [u, v], "uv_size": [w, h]} for f, (u, v, w, h) in c.uv.items()}}
                if c.rot:
                    cd["rotation"] = list(c.rot)
                    cd["pivot"] = list(c.pivot or c.o)
                cs.append(cd)
            if cs:
                b["cubes"] = cs
            bones.append(b)
        return {"format_version": "1.12.0", "minecraft:geometry": [{
            "description": {"identifier": f"geometry.{self.nom}", "texture_width": self.tex, "texture_height": self.tex,
                            "visible_bounds_width": 6, "visible_bounds_height": 6, "visible_bounds_offset": [0, 2, 0]},
            "bones": bones}]}

    def exporter(self, mats, animations):
        self.placer_uv()
        tex, glow = self.peindre(mats)
        p = {"geo": f"{ASSETS}/geckolib/models/entity/{self.nom}.geo.json",
             "anim": f"{ASSETS}/geckolib/animations/entity/{self.nom}.animation.json",
             "tex": f"{ASSETS}/textures/entity/{self.nom}.png",
             "glow": f"{ASSETS}/textures/entity/{self.nom}_glowmask.png"}
        for v in p.values():
            os.makedirs(os.path.dirname(v), exist_ok=True)
        json.dump(self.geo(), open(p["geo"], "w"), separators=(",", ":"))
        json.dump({"format_version": "1.8.0", "animations": animations}, open(p["anim"], "w"), indent=1)
        import remaster  # PNG indexé quand la perte est invisible
        remaster.sauver(tex, p["tex"])
        remaster.sauver(glow, p["glow"])
        return tex


# ==================================================================== matières
def peindre_matiere(px, x0, y0, w, h, face, m, rng):
    typ, c = m["type"], m["c"]
    c2 = m.get("c2")
    lum = {"up": 1.14, "down": 0.62, "north": 1.0, "south": 0.84, "east": 0.9, "west": 0.9}[face]
    cote = face not in ("up", "down")
    seed = rng.random() * 100
    for j in range(h):
        g = 1.0 + (0.13 * (0.5 - j / max(1, h - 1)) if cote else 0)
        for i in range(w):
            k = lum * g
            col = c
            a = 255
            n = rng.randint(-1, 1)
            bord = i == 0 or j == 0 or i == w - 1 or j == h - 1
            if typ in ("metal", "or"):
                n = rng.randint(-4, 4)
                if bord:
                    k *= 0.72
                elif j == 1 and h >= 5:
                    k *= 1.22 if typ == "or" else 1.18
                elif i == w // 3 and h >= 6:
                    k *= 1.1
                if w >= 7 and h >= 7 and (i, j) in ((2, 2), (w - 3, 2), (2, h - 3), (w - 3, h - 3)):
                    k *= 1.35
            elif typ == "tissu":
                n = rng.randint(-4, 4)
                if i % 4 == 0:
                    k *= 0.9
                if cote and j == h - 1:
                    k *= 0.75
            elif typ == "cuir":
                n = rng.randint(-6, 6)
                if not bord and (i == 1 or j == 1 or i == w - 2 or j == h - 2) and (i + j) % 2 == 0 and w > 4 and h > 4:
                    k *= 1.25
                if bord:
                    k *= 0.8
            elif typ == "peau":
                n = rng.randint(-5, 5)
            elif typ == "ecaille":
                n = rng.randint(-3, 3)
                if (j % 2 == 1) and ((i + (j // 2) * 2) % 4 == 0):
                    k *= 0.72
                elif j % 2 == 0 and (i + (j // 2) * 2) % 4 == 2:
                    k *= 1.1
                if c2 and (face == "down" or (cote and j > h * 0.62)):
                    col = c2
            elif typ == "os":
                n = rng.randint(-6, 6)
                if bord:
                    k *= 0.82
                if rng.random() < 0.025:
                    k *= 0.6
            elif typ == "bois":
                n = rng.randint(-8, 8)
                vein = math.sin((i + seed) * 1.7 + math.sin(j * 0.6 + seed) * 1.5)
                if vein > 0.75:
                    k *= 0.72
                elif vein < -0.85:
                    k *= 1.12
            elif typ == "fourrure":
                n = rng.randint(-5, 5)
                mech = (i + (j // 3) * 2 + int(seed)) % 4
                k *= (1.06, 1.0, 0.94, 0.86)[mech]
                if cote and j % 3 == 2 and mech == 3:
                    k *= 0.9
            elif typ == "pierre":
                n = rng.randint(-10, 10)
                if rng.random() < 0.04:
                    k *= 0.65
                if bord:
                    k *= 0.85
            elif typ == "ether":
                n = rng.randint(-6, 6)
                k *= 1.0 + 0.2 * math.sin(i * 0.9 + j * 0.4 + seed)
                if cote and j >= h - 2 and rng.random() < 0.45:
                    a = 0
            elif typ == "lueur":
                n = rng.randint(-3, 3)
                cx, cy = (w - 1) / 2, (h - 1) / 2
                dd = math.hypot((i - cx) / max(1, w / 2), (j - cy) / max(1, h / 2))
                k = 1.15 - 0.3 * dd
            elif typ == "corne":
                n = rng.randint(-4, 4)
                k = lum * (0.8 + 0.4 * (1 - j / max(1, h - 1))) if cote else lum
                if j % 3 == 0:
                    k *= 0.9
            elif typ == "sombre":
                n = rng.randint(-3, 3)
            elif typ == "chaine":
                n = rng.randint(-3, 3)
                if (i + j) % 2 == 0:
                    k *= 0.55
            elif typ == "plume":
                n = rng.randint(-3, 3)
                rang = j // 3
                u, v = (i + (rang % 2) * 2) % 4, j % 3
                k *= (1.08, 1.0, 0.84)[v]
                if u == 3:
                    k *= 0.92
                elif u == 0 and v == 0:
                    k *= 1.05
            elif typ == "membrane":
                n = rng.randint(-4, 4)
                if i % 6 == 0:
                    k *= 0.7
            px[x0 + i, y0 + j] = tuple(clamp(v * k + n) for v in col[:3]) + (a,)


# ==================================================================== aperçu (rastérisation)
def _rot(p, rot, piv):
    if not rot:
        return p
    x, y, z = p[0] - piv[0], p[1] - piv[1], p[2] - piv[2]
    rx, ry, rz = math.radians(-rot[0]), math.radians(rot[1]), math.radians(-rot[2])
    y, z = y * math.cos(rx) - z * math.sin(rx), y * math.sin(rx) + z * math.cos(rx)
    x, z = x * math.cos(ry) + z * math.sin(ry), -x * math.sin(ry) + z * math.cos(ry)
    x, y = x * math.cos(rz) - y * math.sin(rz), x * math.sin(rz) + y * math.cos(rz)
    return (x + piv[0], y + piv[1], z + piv[2])


def _coins(c, f):
    (x0, y0, z0), (w, h, d) = c.o, c.t
    x1, y1, z1 = x0 + w, y0 + h, z0 + d
    # haut-gauche, haut-droite, bas-gauche de la texture (vue de face : le côté droit du modèle, -x, à gauche)
    q = {"north": ((x0, y1, z0), (x1, y1, z0), (x0, y0, z0)),
         "south": ((x1, y1, z1), (x0, y1, z1), (x1, y0, z1)),
         "east": ((x0, y1, z1), (x0, y1, z0), (x0, y0, z1)),
         "west": ((x1, y1, z0), (x1, y1, z1), (x1, y0, z0)),
         "up": ((x0, y1, z1), (x1, y1, z1), (x0, y1, z0)),
         "down": ((x0, y0, z0), (x1, y0, z0), (x0, y0, z1))}[f]
    return [_rot(p, c.rot, c.pivot or c.o) for p in q]


def rendre(m, tex, lacet=-35, tangage=20, taille=520):
    a, b = math.radians(lacet), math.radians(tangage)

    def proj(p):
        # vue depuis l'avant (-z), le côté droit du modèle (-x) apparaît à gauche
        x, y, z = p
        xr = x * math.cos(a) - z * math.sin(a)
        zr = x * math.sin(a) + z * math.cos(a)
        yr = y * math.cos(b) + zr * math.sin(b)
        dr = -zr * math.cos(b) + y * math.sin(b)
        return xr, -yr, dr

    T = np.array(tex)
    faces = []
    for c in m.cubes:
        for f, (u, v, w, h) in c.uv.items():
            p0, p1, p2 = [proj(p) for p in _coins(c, f)]
            faces.append((p0, p1, p2, (u, v, w, h), f))
    xs = [p[i][0] for p in faces for i in range(3)] + [p[1][0] + p[2][0] - p[0][0] for p in faces]
    ys = [p[i][1] for p in faces for i in range(3)] + [p[1][1] + p[2][1] - p[0][1] for p in faces]
    mx, Mx, my, My = min(xs), max(xs), min(ys), max(ys)
    ech = (taille - 20) / max(Mx - mx, My - my, 1)
    W = int((Mx - mx) * ech) + 20
    H = int((My - my) * ech) + 20
    img = np.zeros((H, W, 4), np.uint8)
    zb = np.full((H, W), -1e9)
    LUM = {"up": 1.15, "north": 1.0, "west": 0.85, "east": 0.85, "south": 0.75, "down": 0.6}
    for p0, p1, p2, (u, v, w, h), f in faces:
        P0 = np.array([(p0[0] - mx) * ech + 10, (p0[1] - my) * ech + 10])
        A = np.array([(p1[0] - p0[0]) * ech, (p1[1] - p0[1]) * ech])
        B = np.array([(p2[0] - p0[0]) * ech, (p2[1] - p0[1]) * ech])
        det = A[0] * B[1] - A[1] * B[0]
        if abs(det) < 1e-6:
            continue
        coins = [P0, P0 + A, P0 + B, P0 + A + B]
        x0, x1 = int(max(0, min(q[0] for q in coins))), int(min(W - 1, max(q[0] for q in coins)) + 1)
        y0, y1 = int(max(0, min(q[1] for q in coins))), int(min(H - 1, max(q[1] for q in coins)) + 1)
        if x1 <= x0 or y1 <= y0:
            continue
        gx, gy = np.meshgrid(np.arange(x0, x1) + 0.5, np.arange(y0, y1) + 0.5)
        dx, dy = gx - P0[0], gy - P0[1]
        s = (dx * B[1] - dy * B[0]) / det
        t = (A[0] * dy - A[1] * dx) / det
        ok = (s >= 0) & (s < 1) & (t >= 0) & (t < 1)
        if not ok.any():
            continue
        prof = p0[2] + s * (p1[2] - p0[2]) + t * (p2[2] - p0[2])
        tu = np.clip((u + s * w).astype(int), 0, T.shape[1] - 1)
        tv = np.clip((v + t * h).astype(int), 0, T.shape[0] - 1)
        col = T[tv, tu]
        ok &= col[:, :, 3] > 0
        sub = zb[y0:y1, x0:x1]
        ok &= prof > sub
        sub[ok] = prof[ok]
        k = LUM[f]
        rgb = np.clip(col[:, :, :3].astype(float) * k, 0, 255).astype(np.uint8)
        dst = img[y0:y1, x0:x1]
        dst[ok, :3] = rgb[ok]
        dst[ok, 3] = 255
    return Image.fromarray(img)


def apercu(m, tex, sortie, titre):
    v1 = rendre(m, tex, -35, 18)
    v2 = rendre(m, tex, 145, 18)
    v1.thumbnail((520, 520))
    v2.thumbnail((360, 360))
    W = v1.width + v2.width + 70
    H = max(v1.height, v2.height) + 90
    fond = Image.new("RGBA", (W, H), (30, 32, 40, 255))
    fond.alpha_composite(v1, (20, 70))
    fond.alpha_composite(v2, (v1.width + 50, 70 + (v1.height - v2.height)))
    d = ImageDraw.Draw(fond)
    d.text((20, 18), titre, fill=(240, 220, 150), font=ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf", 26))
    fond.convert("RGB").save(sortie)
    return v1
