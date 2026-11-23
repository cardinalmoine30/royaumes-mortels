# -*- coding: utf-8 -*-
"""Outils communs pour générer des modèles GeckoLib (format Bedrock .geo.json) :
placement des UV, peinture procédurale de la texture, animations, aperçu en image."""
import json, math, os, random
from PIL import Image, ImageDraw, ImageFont, ImageChops

RACINE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SENS = 1
ASSETS = os.path.join(RACINE, "src/main/resources/assets/royaumes")


class Cube:
    def __init__(self, os_, taille, style, os_bone, details=None):
        self.o = os_            # origine (coin min) en pixels
        self.t = taille         # (largeur x, hauteur y, profondeur z), entiers
        self.style = style      # nom de palette
        self.bone = os_bone
        self.details = details or {}   # face -> fonction de dessin
        self.uv = None


class Modele:
    def __init__(self, nom, tex=128):
        self.nom = nom
        self.tex = tex
        self.bones = []         # (nom, parent, pivot)
        self.cubes = []

    def bone(self, nom, parent, pivot):
        self.bones.append((nom, parent, pivot))

    def cube(self, bone, origine, taille, style, **details):
        c = Cube(origine, taille, style, bone, details)
        self.cubes.append(c)
        return c

    # --- UV « box » empaquetés en étagères ---
    def placer_uv(self):
        x = y = haut = 0
        for c in sorted(self.cubes, key=lambda c: -(c.t[1] + c.t[2])):
            w, h, d = c.t
            lw, lh = 2 * (w + d), h + d
            if x + lw > self.tex:
                x, y, haut = 0, y + haut, 0
            c.uv = (x, y)
            x += lw
            haut = max(haut, lh)
        if y + haut > self.tex:
            raise ValueError(f"texture trop petite ({y + haut} > {self.tex})")

    @staticmethod
    def faces_uv(c):
        u, v = c.uv
        w, h, d = c.t
        return {"up": (u + d, v, w, d), "down": (u + d + w, v, w, d), "east": (u, v + d, d, h),
                "north": (u + d, v + d, w, h), "west": (u + d + w, v + d, d, h), "south": (u + 2 * d + w, v + d, w, h)}

    # --- texture ---
    def peindre(self, palettes, graine=7):
        rnd = random.Random(graine)
        im = Image.new("RGBA", (self.tex, self.tex), (0, 0, 0, 0))
        px = im.load()
        for c in self.cubes:
            pal = palettes[c.style]
            for f, (x0, y0, w, h) in self.faces_uv(c).items():
                base = pal.get(f, pal["base"])
                for i in range(w):
                    for j in range(h):
                        col = list(base)
                        bord = i == 0 or j == 0 or i == w - 1 or j == h - 1
                        if bord and pal.get("bord"):
                            col = list(pal["bord"])
                        if f == "up":
                            col = [min(255, k + 22) for k in col]
                        elif f == "down":
                            col = [max(0, k - 30) for k in col]
                        elif f in ("east", "west"):
                            col = [max(0, k - 14) for k in col]
                        n = rnd.randint(-pal.get("bruit", 6), pal.get("bruit", 6))
                        px[x0 + i, y0 + j] = tuple(max(0, min(255, k + n)) for k in col) + (255,)
                fn = c.details.get(f) or c.details.get("toutes")
                if fn:
                    fn(ImageDraw.Draw(im), x0, y0, w, h, px)
        return im

    # --- export ---
    def geo(self):
        bones = []
        for nom, parent, pivot in self.bones:
            b = {"name": nom, "pivot": list(pivot)}
            if parent:
                b["parent"] = parent
            cs = [{"origin": list(c.o), "size": list(c.t), "uv": list(c.uv)} for c in self.cubes if c.bone == nom]
            if cs:
                b["cubes"] = cs
            bones.append(b)
        return {"format_version": "1.12.0", "minecraft:geometry": [{
            "description": {"identifier": f"geometry.{self.nom}", "texture_width": self.tex, "texture_height": self.tex,
                            "visible_bounds_width": 4, "visible_bounds_height": 4, "visible_bounds_offset": [0, 1.5, 0]},
            "bones": bones}]}

    def exporter(self, palettes, animations):
        self.placer_uv()
        tex = self.peindre(palettes)
        chemins = {
            "geo": f"{ASSETS}/geckolib/models/entity/{self.nom}.geo.json",
            "anim": f"{ASSETS}/geckolib/animations/entity/{self.nom}.animation.json",
            "tex": f"{ASSETS}/textures/entity/{self.nom}.png",
        }
        for p in chemins.values():
            os.makedirs(os.path.dirname(p), exist_ok=True)
        json.dump(self.geo(), open(chemins["geo"], "w"), indent=1)
        json.dump({"format_version": "1.8.0", "animations": animations}, open(chemins["anim"], "w"), indent=1)
        tex.save(chemins["tex"])
        return tex

    # --- aperçu (projection orthographique 3/4, sans rotation des os) ---
    def apercu(self, tex, sortie, titre, ech=9, lacet=35, tangage=18):
        a, b = math.radians(lacet), math.radians(tangage)

        def proj(p):
            x, y, z = p
            xr = x * math.cos(a) + z * math.sin(a)
            zr = -x * math.sin(a) + z * math.cos(a)
            yr = y * math.cos(b) - zr * math.sin(b)
            prof = zr * math.cos(b) + y * math.sin(b)
            return xr, -yr, prof

        faces = []
        for c in self.cubes:
            (x0, y0, z0), (w, h, d) = c.o, c.t
            x1, y1, z1 = x0 + w, y0 + h, z0 + d
            fuv = self.faces_uv(c)
            # coins : haut-gauche, haut-droite, bas-gauche (dans l'orientation de la texture)
            geo = {"north": ((x1, y1, z0), (x0, y1, z0), (x1, y0, z0)),
                   "south": ((x0, y1, z1), (x1, y1, z1), (x0, y0, z1)),
                   "east": ((x0, y1, z1), (x0, y1, z0), (x0, y0, z1)),
                   "west": ((x1, y1, z0), (x1, y1, z1), (x1, y0, z0)),
                   "up": ((x1, y1, z1), (x0, y1, z1), (x1, y1, z0)),
                   "down": ((x1, y0, z0), (x0, y0, z0), (x1, y0, z1))}
            for f, (p0, p1, p2) in geo.items():
                q0, q1, q2 = proj(p0), proj(p1), proj(p2)
                # normale visible ? (produit vectoriel 2D)
                cr = (q1[0] - q0[0]) * (q2[1] - q0[1]) - (q1[1] - q0[1]) * (q2[0] - q0[0])
                if cr <= 0:
                    continue
                q3 = (q1[0] + q2[0] - q0[0], q1[1] + q2[1] - q0[1])
                cc = proj((x0 + w / 2, y0 + h / 2, z0 + d / 2))
                faces.append((cc[2], q0, q1, q2, q3, fuv[f]))
        faces.sort(key=lambda f: SENS * f[0])
        xs = [q[0] for f in faces for q in f[1:5]]
        ys = [q[1] for f in faces for q in f[1:5]]
        mx, my = min(xs), min(ys)
        W, H = int((max(xs) - mx) * ech) + 40, int((max(ys) - my) * ech) + 40
        img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        for _, q0, q1, q2, q3, (u, v, w, h) in faces:
            P = [((q[0] - mx) * ech + 20, (q[1] - my) * ech + 20) for q in (q0, q1, q2, q3)]
            src = tex.crop((u, v, u + w, v + h)).resize((w * 8, h * 8), Image.NEAREST)
            sw, sh = src.size
            # affine : écran -> source
            ax, ay = P[1][0] - P[0][0], P[1][1] - P[0][1]
            bx, by = P[2][0] - P[0][0], P[2][1] - P[0][1]
            det = ax * by - ay * bx
            if abs(det) < 1e-6:
                continue
            ia, ib, ic, id_ = by / det, -bx / det, -ay / det, ax / det
            coeffs = (ia * sw, ib * sw, -(ia * P[0][0] + ib * P[0][1]) * sw,
                      ic * sh, id_ * sh, -(ic * P[0][0] + id_ * P[0][1]) * sh)
            couche = src.transform((W, H), Image.AFFINE, coeffs, Image.NEAREST)
            masque = Image.new("L", (W, H), 0)
            ImageDraw.Draw(masque).polygon([P[0], P[1], P[3], P[2]], fill=255)
            img.paste(couche, (0, 0), ImageChops.multiply(masque, couche.split()[3]))
        fond = Image.new("RGBA", (W + 360, max(H, 300) + 70), (28, 30, 38, 255))
        fond.alpha_composite(img, (10, 60))
        t2 = tex.resize((320, 320), Image.NEAREST)
        fond.alpha_composite(Image.new("RGBA", (320, 320), (60, 60, 70, 255)), (W + 25, 60))
        fond.alpha_composite(t2, (W + 25, 60))
        d = ImageDraw.Draw(fond)
        f = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf", 26)
        d.text((16, 16), titre, fill=(240, 220, 150), font=f)
        d.text((W + 25, 386), "texture 128×128", fill=(180, 180, 180),
               font=ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 14))
        fond.convert("RGB").save(sortie)


def apercu_vues(m, tex, sortie, titre, ech=8):
    """Vues orthographiques exactes : face, profil droit, dos (+ texture)."""
    xs = [c.o[0] for c in m.cubes] + [c.o[0] + c.t[0] for c in m.cubes]
    ys = [c.o[1] for c in m.cubes] + [c.o[1] + c.t[1] for c in m.cubes]
    zs = [c.o[2] for c in m.cubes] + [c.o[2] + c.t[2] for c in m.cubes]
    X0, X1, Y1, Z0, Z1 = min(xs), max(xs), max(ys), min(zs), max(zs)

    def vue(face, cle, pos, larg):
        im = Image.new("RGBA", (int(larg * ech), int(Y1 * ech) + 2), (0, 0, 0, 0))
        for c in sorted(m.cubes, key=cle):
            u, v, w, h = Modele.faces_uv(c)[face]
            if w == 0 or h == 0:
                continue
            src = tex.crop((u, v, u + w, v + h))
            x, larg_f = pos(c)
            if face in ("south", "west"):
                pass
            src = src.resize((int(larg_f * ech), int(c.t[1] * ech)), Image.NEAREST)
            y = int((Y1 - c.o[1] - c.t[1]) * ech)
            im.alpha_composite(src, (int(x * ech), y))
        return im

    face = vue("north", lambda c: -c.o[2], lambda c: (c.o[0] - X0, c.t[0]), X1 - X0)
    dos = vue("south", lambda c: c.o[2] + c.t[2], lambda c: (X1 - c.o[0] - c.t[0], c.t[0]), X1 - X0)
    profil = vue("east", lambda c: -c.o[0], lambda c: (c.o[2] - Z0, c.t[2]), Z1 - Z0)
    vues = [("Face", face), ("Profil", profil), ("Dos", dos)]
    W = sum(v.width for _, v in vues) + 60 * len(vues) + 300
    H = max(v.height for _, v in vues) + 110
    fond = Image.new("RGBA", (W, max(H, 420)), (28, 30, 38, 255))
    d = ImageDraw.Draw(fond)
    fb = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf", 26)
    fs = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 15)
    d.text((20, 16), titre, fill=(240, 220, 150), font=fb)
    x = 30
    for nom, v in vues:
        fond.alpha_composite(v, (x, 70))
        d.text((x, 70 + v.height + 8), nom, fill=(200, 200, 200), font=fs)
        x += v.width + 60
    fond.alpha_composite(Image.new("RGBA", (256, 256), (60, 60, 70, 255)), (x, 70))
    fond.alpha_composite(tex.resize((256, 256), Image.NEAREST), (x, 70))
    d.text((x, 70 + 264), f"texture {m.tex}×{m.tex}", fill=(200, 200, 200), font=fs)
    fond.convert("RGB").save(sortie)
