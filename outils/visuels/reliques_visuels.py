# -*- coding: utf-8 -*-
"""Planche des seigneurs (œil, relique, pouvoirs) et des minerais propres à chaque Royaume."""
import os
import sys
from PIL import Image, ImageDraw, ImageFont

ICI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(ICI, "..", "objets"))
from objets import SEIGNEURS, MINERAIS  # noqa: E402

TEX = os.path.join(ICI, "..", "..", "src", "main", "resources", "assets", "royaumes", "textures")
F = "/usr/share/fonts/truetype/dejavu/"
POUV = {"nagash": "Armée des Morts · Main de Nagash", "archaon": "Œil de Sheerian · épée légendaire",
        "gordrakk": "Onde du Waaagh ! · hache géante", "skarbrand": "Rugissement de rage · haches de feu",
        "thanquol": "Malefeu · Saut par la Warp", "rotigus": "Pluie de pestilence"}
ROY = {"minerai_azyrite": "Azyr", "minerai_braise": "Aqshy", "minerai_croc": "Ghur", "minerai_jade": "Ghyran", "minerai_lumineux": "Hysh",
       "minerai_ombre": "Ulgu", "minerai_ames": "Shyish", "minerai_or_vif": "Chamon", "minerai_malepierre": "Huit-Points"}


def img(p, k=6):
    i = Image.open(p).convert("RGBA")
    return i.resize((i.width * k, i.height * k), Image.NEAREST)


im = Image.new("RGB", (1500, 1180), (14, 26, 51))
d = ImageDraw.Draw(im)
t1, t2, t3 = ImageFont.truetype(F + "DejaVuSerif-Bold.ttf", 34), ImageFont.truetype(F + "DejaVuSans-Bold.ttf", 21), ImageFont.truetype(F + "DejaVuSans.ttf", 17)
d.text((750, 18), "Les six Seigneurs : œil, autel, relique", font=t1, fill=(242, 210, 122), anchor="mt")
d.text((750, 64), "Œil → direction de l'antre · Sceau sur l'Autel des Seigneurs → le seigneur s'éveille · Victoire → relique unique",
       font=t3, fill=(230, 211, 168), anchor="mt")
for i, (sid, nom, desc, roy, _, c1, _) in enumerate(SEIGNEURS):
    x, y = 30 + (i % 3) * 490, 110 + (i // 3) * 250
    d.rounded_rectangle((x, y, x + 470, y + 230), 12, fill=(20, 30, 56), outline=c1, width=3)
    e = img(os.path.join(TEX, "item", "oeil_" + sid + ".png"), 5)
    r = img(os.path.join(TEX, "item", "relique_" + sid + ".png"), 8)
    im.paste(e, (x + 20, y + 20), e)
    im.paste(r, (x + 20, y + 100), r)
    d.text((x + 170, y + 18), nom, font=t2 if len(nom) < 24 else ImageFont.truetype(F + "DejaVuSans-Bold.ttf", 16), fill=(242, 210, 122))
    d.text((x + 170, y + 50), "Antre : " + roy, font=t3 if len(roy) < 26 else ImageFont.truetype(F + "DejaVuSans.ttf", 14), fill=(200, 205, 225))
    words, ligne, yy = desc.split(), "", y + 80
    for w in words:
        if d.textlength(ligne + " " + w, font=t3) > 285:
            d.text((x + 170, yy), ligne.strip(), font=t3, fill=(190, 180, 230))
            ligne, yy = w, yy + 22
        else:
            ligne += " " + w
    d.text((x + 170, yy), ligne.strip(), font=t3, fill=(190, 180, 230))
    d.text((x + 170, y + 170), POUV[sid], font=t3, fill=(255, 200, 120))
y0 = 640
d.text((750, y0), "Minerais propres à chaque Royaume", font=t1, fill=(242, 210, 122), anchor="mt")
d.text((750, y0 + 46), "Absents du monde de base : il faut voyager pour obtenir les éclats de Vent et la malepierre.",
       font=t3, fill=(230, 211, 168), anchor="mt")
for i, (mid, val) in enumerate(MINERAIS.items()):
    x, y = 40 + (i % 5) * 290, y0 + 100 + (i // 5) * 210
    b = img(os.path.join(TEX, "block", mid + ".png"), 7)
    drop = val[0].split(":")[1]
    o = img(os.path.join(TEX, "item", drop + ".png"), 4)
    im.paste(b, (x, y), b)
    d.text((x + 120, y + 10), ROY[mid], font=t2, fill=(242, 210, 122))
    d.text((x + 120, y + 40), "→", font=t2, fill=(230, 211, 168))
    im.paste(o, (x + 150, y + 30), o)
    d.text((x, y + 120), drop.replace("_", " ").replace("eclat", "éclat"), font=t3, fill=(200, 205, 225))
out = os.path.join(ICI, "apercus", "seigneurs_et_minerais.png")
im.save(out)
print(out)
