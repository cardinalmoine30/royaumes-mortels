# -*- coding: utf-8 -*-
"""Aides visuelles de jeu, générées depuis les vraies textures et données du mod :
 - guide_magie.png     : les huit Vents, leurs bâtons, leurs deux sorts et leur coût
 - onglets_creatifs.png : les cinq onglets du menu créatif et ce qu'ils contiennent"""
import json
import os
import sys

from PIL import Image, ImageDraw, ImageFont

ICI = os.path.dirname(os.path.abspath(__file__))
RACINE = os.path.join(ICI, "..", "..")
TEX = os.path.join(RACINE, "src", "main", "resources", "assets", "royaumes", "textures")
sys.path.insert(0, os.path.join(ICI, "..", "objets"))
from objets import VENTS, SORTS, BLOCS  # noqa: E402

F = "/usr/share/fonts/truetype/dejavu/"
OR, OR_C, NUIT, PARCH = (212, 166, 58), (242, 210, 122), (14, 26, 51), (230, 211, 168)


def police(t, gras=False, serif=True):
    return ImageFont.truetype(F + (("DejaVuSerif-Bold.ttf" if gras else "DejaVuSerif.ttf") if serif else ("DejaVuSans-Bold.ttf" if gras else "DejaVuSans.ttf")), t)


def icone(chemin, k):
    im = Image.open(chemin).convert("RGBA")
    return im.resize((im.width * k, im.height * k), Image.NEAREST)


def fond(W, H):
    im = Image.new("RGB", (W, H), NUIT)
    d = ImageDraw.Draw(im)
    for y in range(H):
        t = y / H
        d.line((0, y, W, y), fill=tuple(int(a + (b - a) * t) for a, b in zip((22, 38, 72), (8, 12, 26))))
    d.rectangle((8, 8, W - 9, H - 9), outline=OR, width=3)
    d.rectangle((16, 16, W - 17, H - 17), outline=(120, 92, 36), width=1)
    return im, d


def guide_magie():
    W, H = 1500, 1010
    im, d = fond(W, H)
    d.text((W // 2, 40), "Les huit Vents de magie", font=police(42, True), fill=OR_C, anchor="mt")
    d.text((W // 2, 96), "Clic droit : sort mineur  ·  Accroupi + clic droit : grand sort  ·  Coût en énergie (moitié prix dans le Royaume du Vent)",
           font=police(20, False, False), fill=PARCH, anchor="mt")
    d.text((W // 2, 126), "Énergie arcanique : 100 + 5 par niveau, +2/s (+4/s dans le Royaume de ta faction) · Cristal arcanique : +40 · Autel arcanique : plein",
           font=police(17, False, False), fill=(190, 180, 240), anchor="mt")
    y0 = 170
    for i, v in enumerate(VENTS):
        col, lig = i % 2, i // 2
        x, y = 40 + col * 720, y0 + lig * 205
        c = v[2]
        d.rounded_rectangle((x, y, x + 700, y + 190), 10, fill=(18, 26, 48), outline=c, width=3)
        im.paste(icone(os.path.join(TEX, "item", "baton_" + v[0] + ".png"), 7), (x + 14, y + 40), icone(os.path.join(TEX, "item", "baton_" + v[0] + ".png"), 7))
        im.paste(icone(os.path.join(TEX, "item", "eclat_" + v[0] + ".png"), 3), (x + 14, y + 10), icone(os.path.join(TEX, "item", "eclat_" + v[0] + ".png"), 3))
        d.text((x + 140, y + 14), v[1], font=police(30, True), fill=c)
        dim = {"royaumes_mortels": "Célestis"}.get(v[5].split(":")[1], v[5].split(":")[1].capitalize())
        d.text((x + 140, y + 52), "Bâton " + ("d'" if v[1][0] in "AEIOUH" else "de ") + v[1] + " · Royaume : " + dim, font=police(16, False, False), fill=(200, 205, 225))
        s = sorted([z for z in SORTS if z[0] == v[0]], key=lambda z: z[1])
        for k, z in enumerate(s):
            yy = y + 84 + k * 50
            etiquette = "Clic droit" if k == 0 else "Accroupi"
            d.rounded_rectangle((x + 140, yy, x + 236, yy + 22), 6, fill=c if k else (40, 50, 80))
            d.text((x + 188, yy + 11), etiquette, font=police(13, True, False), fill=(10, 10, 20) if k else (230, 230, 240), anchor="mm")
            d.text((x + 246, yy - 1), "%s — %d (%d en %s)" % (z[3], z[4], (z[4] + 1) // 2, v[1]), font=police(17, True, False), fill=OR_C)
            d.text((x + 246, yy + 22), z[6], font=police(15, False, False), fill=PARCH)
    out = os.path.join(ICI, "apercus", "guide_magie.png")
    im.save(out)
    return out


def onglets():
    W, H = 1500, 900
    im, d = fond(W, H)
    d.text((W // 2, 40), "Menu créatif : les cinq onglets des Royaumes", font=police(40, True), fill=OR_C, anchor="mt")
    mobs = json.load(open(os.path.join(RACINE, "outils", "modeles", "liste_mobs.json"), encoding="utf-8"))
    montures = json.load(open(os.path.join(RACINE, "outils", "modeles", "liste_montures.json"), encoding="utf-8"))
    armes = json.load(open(os.path.join(RACINE, "src", "main", "resources", "royaumes_creatif", "armes.json"), encoding="utf-8"))
    magie = json.load(open(os.path.join(RACINE, "src", "main", "resources", "royaumes_creatif", "magie.json"), encoding="utf-8"))
    ti = os.path.join(TEX, "item")
    tb = os.path.join(TEX, "block")
    lignes = [
        ("Armes et armures", "Marteau-tempête + %d armes, armures et reliques des 25 factions (kits, forge, trophées)" % len(armes),
         [os.path.join(ti, "marteau_tempete.png")]),
        ("Magie", "8 bâtons, 8 éclats, pierre des Royaumes, cristal, grimoire, autel + %d objets du Codex" % len(magie),
         [os.path.join(ti, "baton_" + v[0] + ".png") for v in VENTS] + [os.path.join(ti, "eclat_" + v[0] + ".png") for v in VENTS[:4]]
         + [os.path.join(ti, n + ".png") for n in ("pierre_royaumes_brute", "cristal_arcanique", "grimoire_des_vents")]),
        ("Blocs des Royaumes", "%d blocs : deux par Royaume, Chaos, minerais, autel et Portail des Royaumes" % len(BLOCS),
         [os.path.join(tb, "marbre_celeste_grave.png")] + [os.path.join(tb, b[0] + ".png") for b in BLOCS if b[0] != "marbre_celeste_grave"][:14]),
        ("Créatures", "%d œufs d'apparition : toutes les unités et tous les boss des factions" % len(mobs),
         [os.path.join(ti, "oeuf_" + m["id"] + ".png") for m in mobs[::10][:15]]),
        ("Montures et voyage", "Portail des Royaumes, %d œufs de monture, Corne d'appel et Pierre de Royaume" % len(montures),
         [os.path.join(tb, "portail_des_royaumes.png")] + [os.path.join(ti, "oeuf_" + m["id"] + ".png") for m in montures[:14]]),
    ]
    y = 110
    for nom, desc, icones in lignes:
        d.rounded_rectangle((40, y, W - 40, y + 145), 10, fill=(18, 26, 48), outline=OR, width=2)
        d.rounded_rectangle((56, y + 14, 120, y + 78), 8, fill=(40, 50, 84), outline=OR_C, width=2)
        ic = icone(icones[0], 3)
        im.paste(ic, (64, y + 22), ic)
        d.text((140, y + 16), "Royaumes — " + nom, font=police(26, True), fill=OR_C)
        d.text((140, y + 52), desc, font=police(17, False, False), fill=PARCH)
        for k, ch in enumerate(icones[:15]):
            x = 140 + k * 58
            d.rectangle((x, y + 84, x + 52, y + 136), fill=(139, 139, 139), outline=(55, 55, 55), width=2)
            ic = icone(ch, 3)
            im.paste(ic, (x + 2, y + 86), ic)
        if nom.startswith("Armes"):
            d.text((210, y + 100), "… suivis des armes et armures de chaque faction, avec leurs propres modèles (marteaux, lames, arcs, armures teintes).",
                   font=police(16, False, False), fill=(170, 180, 205))
        y += 158
    out = os.path.join(ICI, "apercus", "onglets_creatifs.png")
    im.save(out)
    return out


if __name__ == "__main__":
    print(guide_magie())
    print(onglets())
