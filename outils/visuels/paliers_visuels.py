# -*- coding: utf-8 -*-
"""Planche : les trois paliers d'armure (Soldat, Élite, Légende) portés, et les outils d'alliance."""
import os
import sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont

ICI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ICI)
sys.path.insert(0, os.path.join(ICI, "..", "objets"))
import scenes as S  # noqa: E402
from scenes import Scene, TEX  # noqa: E402
from arsenal import ARSENAL, TIERS, OUTILS, ALLIANCES, NOMS_ALLIANCES  # noqa: E402

A = os.path.join(ICI, "..", "..", "src", "main", "resources", "assets", "royaumes")
F = "/usr/share/fonts/truetype/dejavu/"
EQ = os.path.join(A, "textures", "entity", "equipment")


def skin_arme(fid, tid):
    """Skin de base recouvert par l'armure du palier (couche du haut et jambières)."""
    sk = Image.open(os.path.join(TEX, "skin", fid + ".png")).convert("RGBA")
    l1 = Image.open(os.path.join(EQ, "humanoid", fid + "_" + tid + ".png")).convert("RGBA")
    l2 = Image.open(os.path.join(EQ, "humanoid_leggings", fid + "_" + tid + ".png")).convert("RGBA")
    out = sk.copy()
    for lay in (l2, l1):
        h = Image.new("RGBA", (64, 64), (0, 0, 0, 0))
        h.paste(lay, (0, 0))
        out.alpha_composite(h)
        # bras et jambe gauches (format 64x64) : copie du côté droit
        out.alpha_composite(h.crop((40, 16, 56, 32)), (32, 48))
        out.alpha_composite(h.crop((0, 16, 16, 32)), (16, 48))
    return np.array(out)


def main():
    fids = ["stormcast", "khorne", "nighthaunt", "ironjawz"]
    W = 1600
    im = Image.new("RGB", (W, 80 + 300 * len(fids) + 330), (14, 26, 51))
    d = ImageDraw.Draw(im)
    f1 = ImageFont.truetype(F + "DejaVuSerif-Bold.ttf", 34)
    f2 = ImageFont.truetype(F + "DejaVuSans-Bold.ttf", 20)
    f3 = ImageFont.truetype(F + "DejaVuSans.ttf", 16)
    d.text((W // 2, 16), "Forge de guerre : Soldat → Élite → Légende", font=f1, fill=(242, 210, 122), anchor="mt")
    for k, fid in enumerate(fids):
        y = 70 + k * 300
        S.W, S.H = 900, 250
        s = Scene((24, 36, 66), (40, 56, 96), (40, 56, 96), 60)
        for t, (tid, _) in enumerate(TIERS):
            chemin = os.path.join(TEX, "skin", "_%s_%s.png" % (fid, tid))
            s.cache[os.path.join(TEX, "skin", chemin.split("/")[-1])] = skin_arme(fid, tid)
            s.joueur("_%s_%s" % (fid, tid), 2.6 - t * 2.6, 0, 0, lacet=-15)
        img = s.rendre((0, 1.2, -9.5), (0, 1.0, 0), fov=42)
        im.paste(img.convert("RGB"), (20, y))
        for t, (_, tnom) in enumerate(TIERS):
            d.text((20 + 150 + t * 322, y + 252), tnom, font=f2, fill=[(190, 192, 200), (120, 215, 230), (245, 205, 80)][t], anchor="mt")
        ch, li, atout, pieces, bonus = ARSENAL[fid]
        d.text((940, y + 10), fid.capitalize(), font=f2, fill=(242, 210, 122))
        d.text((940, y + 42), ", ".join(pieces), font=ImageFont.truetype(F + "DejaVuSans.ttf", 14), fill=(230, 225, 210))
        d.text((940, y + 66), "Soldat : fer + 1 éclat étranger ; 1er effet de panoplie", font=f3, fill=(190, 192, 200))
        d.text((940, y + 88), "Élite : pièce Soldat + diamants + éclats ; panoplie complète", font=f3, fill=(120, 215, 230))
        d.text((940, y + 110), "Légende : pièce Élite + netherite + éclats ; effets +1 niveau", font=f3, fill=(245, 205, 80))
        x = 940
        for t, (tid, _) in enumerate(TIERS):
            for piece in ("casque", "torse", "jambes", "bottes"):
                ic = Image.open(os.path.join(TEX, "item", "%s_%s_%s.png" % (fid, piece, tid))).convert("RGBA").resize((40, 40), Image.NEAREST)
                d.rectangle((x - 2, y + 146, x + 42, y + 190), fill=(139, 139, 139), outline=(55, 55, 55), width=2)
                im.paste(ic, (x, y + 148), ic)
                x += 48
            x += 12
    y = 80 + 300 * len(fids)
    d.text((W // 2, y), "Outils d'alliance (communs à toutes les factions de l'alliance)", font=f2, fill=(242, 210, 122), anchor="mt")
    for a, al in enumerate(ALLIANCES):
        yy = y + 40 + a * 70
        d.text((30, yy + 18), "Alliance " + NOMS_ALLIANCES[al], font=f3, fill=(230, 225, 210))
        x = 300
        for t, (tid, tnom) in enumerate(TIERS):
            for o in OUTILS:
                ic = Image.open(os.path.join(TEX, "item", "%s_%s_%s.png" % (al, o, tid))).convert("RGBA").resize((48, 48), Image.NEAREST)
                d.rectangle((x - 2, yy, x + 50, yy + 52), fill=(139, 139, 139), outline=(55, 55, 55), width=2)
                im.paste(ic, (x, yy + 2), ic)
                x += 56
            x += 40
    S.W, S.H = 1280, 720
    out = os.path.join(ICI, "apercus", "arsenal", "paliers.png")
    im.save(out)
    print(out)


if __name__ == "__main__":
    main()
