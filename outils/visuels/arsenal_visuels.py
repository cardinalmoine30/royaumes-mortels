# -*- coding: utf-8 -*-
"""Planche de l'arsenal : armes en 3D (vrais modèles à éléments) et armures portées, pour quelques factions."""
import json
import math
import os
import sys
from PIL import Image, ImageDraw, ImageFont

ICI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ICI)
sys.path.insert(0, os.path.join(ICI, "..", "objets"))
import scenes as S  # noqa: E402
from scenes import Scene, LUM, coins, TEX  # noqa: E402
from arsenal import ARSENAL  # noqa: E402

A = os.path.join(ICI, "..", "..", "src", "main", "resources", "assets", "royaumes")
F = "/usr/share/fonts/truetype/dejavu/"


def arme(s, oid, x0, z0, rot_y=25):
    m = json.load(open(os.path.join(A, "models", "item", oid + "_3d.json")))
    T = s.tex(os.path.join(TEX, "item", oid + "_palette.png"))
    for e in m["elements"]:
        for f, fd in e["faces"].items():
            pts = coins(e["from"], [e["to"][i] - e["from"][i] for i in range(3)], f)
            res = []
            for (x, y, z) in pts:
                x, y = x - 8, y - 8
                a = math.radians(-45)
                x, y = x * math.cos(a) - y * math.sin(a), x * math.sin(a) + y * math.cos(a)
                b = math.radians(rot_y)
                x, z = x * math.cos(b) - (z - 8) * math.sin(b), x * math.sin(b) + (z - 8) * math.cos(b)
                res.append((x0 + x / 16 * 2.2, 1.6 + y / 16 * 2.2, z0 + z / 16 * 2.2))
            u0, v0, u1, v1 = fd["uv"]
            s.quads.append((res[0], res[1], res[2], T, (u0, v0, u1 - u0, v1 - v0), LUM[f], False))


def rendu_factions(fids, sortie):
    S.W, S.H = 1600, 260 * len(fids) + 80
    im = Image.new("RGB", (S.W, S.H), (14, 26, 51))
    d = ImageDraw.Draw(im)
    d.text((800, 16), "Arsenal de faction : armes 3D en main et armure portée", font=ImageFont.truetype(F + "DejaVuSerif-Bold.ttf", 34),
           fill=(242, 210, 122), anchor="mt")
    f2, f3 = ImageFont.truetype(F + "DejaVuSans-Bold.ttf", 20), ImageFont.truetype(F + "DejaVuSans.ttf", 16)
    for k, fid in enumerate(fids):
        y = 70 + k * 260
        S.W, S.H = 760, 250
        s = Scene((24, 36, 66), (40, 56, 96), (40, 56, 96), 60)
        arme(s, fid + "_champion", -1.4, 0)
        arme(s, fid + "_lignee", 1.4, 0)
        s.joueur(fid, 4.2, 0.2, 0.5, lacet=20)
        img = s.rendre((1.2, 1.6, -11), (1.4, 1.5, 0), fov=45)
        # le joueur porte l'armure : on réutilise le skin (l'armure portée en est tirée)
        im.paste(img.convert("RGB"), (20, y))
        ch, li, atout, pieces, bonus = ARSENAL[fid]
        d.text((800, y + 10), fid.capitalize(), font=f2, fill=(242, 210, 122))
        d.text((800, y + 44), "Champion : " + ch[0], font=f3, fill=(240, 230, 210))
        d.text((800, y + 70), "Lignée : " + li[0] + "  (atout : " + atout.replace("_", " ") + ")", font=f3, fill=(240, 230, 210))
        d.text((800, y + 96), "Armure : " + ", ".join(pieces), font=f3, fill=(200, 205, 225))
        TR = {"resistance": "résistance", "speed": "vitesse", "haste": "célérité", "fire_resistance": "résistance au feu", "strength": "force",
              "slow_falling": "chute lente", "water_breathing": "respiration aquatique", "dolphins_grace": "grâce du dauphin",
              "night_vision": "vision nocturne", "jump_boost": "saut", "regeneration": "régénération", "invisibility": "invisibilité",
              "health_boost": "vie bonus"}
        txt = ", ".join(TR.get(b.split(":")[0], b) + ("" if b.endswith(":0") else " " + "I" * (int(b.split(":")[1]) + 1)) for b in bonus.split(","))
        d.text((800, y + 122), "Panoplie complète : " + txt,
               font=f3, fill=(158, 230, 154))
        x = 800
        for piece in ("casque", "torse", "jambes", "bottes", "champion", "lignee"):
            ic = Image.open(os.path.join(TEX, "item", fid + "_" + piece + ".png")).convert("RGBA").resize((64, 64), Image.NEAREST)
            d.rectangle((x - 2, y + 156, x + 66, y + 224), fill=(139, 139, 139), outline=(55, 55, 55), width=2)
            im.paste(ic, (x, y + 158), ic)
            x += 76
    S.W, S.H = 1280, 720
    im.save(sortie)
    print(sortie)


if __name__ == "__main__":
    out = os.path.join(ICI, "apercus", "arsenal")
    os.makedirs(out, exist_ok=True)
    rendu_factions(["stormcast", "nurgle", "skaven", "khorne"], os.path.join(out, "arsenal_1.png"))
    rendu_factions(["lumineth", "nighthaunt", "ironjawz", "seraphon"], os.path.join(out, "arsenal_2.png"))
