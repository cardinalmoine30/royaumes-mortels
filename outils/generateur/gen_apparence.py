# -*- coding: utf-8 -*-
"""Textures d'armure de faction (apparence de la classe choisie) : equipment assets 26.3."""
import json, os, sys
from PIL import Image
import data_v5

MOD = sys.argv[1]
A = f"{MOD}/src/main/resources/assets/royaumes"
V = "/tmp/mc-assets/assets/minecraft/textures/entity/equipment"


def teinter(src, base, det, acc, couche):
    im = src.copy()
    px = im.load()
    for x in range(im.width):
        for y in range(im.height):
            r, g, b, a = px[x, y]
            if a == 0:
                continue
            l = (0.3 * r + 0.59 * g + 0.11 * b) / 255.0
            c = base
            # zones de détail : bordures sombres -> couleur secondaire
            if l < 0.42:
                c = det
            k = 0.55 + 0.75 * l
            px[x, y] = tuple(max(0, min(255, int(v * k))) for v in c) + (a,)
    if couche == "humanoid":
        # emblème sur le plastron (face avant du torse : x 20..27, y 20..31)
        for (dx, dy) in ((3, 2), (4, 2), (3, 3), (4, 3), (2, 4), (5, 4), (3, 5), (4, 5)):
            px[20 + dx, 20 + dy] = acc + (255,)
        # visière lumineuse du heaume (face avant de la tête : x 8..15, y 8..15)
        for x in range(9, 15):
            if px[x, 12][3]:
                px[x, 12] = (20, 20, 26, 255)
        for x in (10, 13):
            if px[x, 12][3]:
                px[x, 12] = acc + (255,)
        # crête/cimier sur le dessus du heaume (x 8..15, y 0..7)
        for y in range(0, 8):
            if px[11, y][3]:
                px[11, y] = det + (255,)
                px[12, y] = det + (255,)
    return im


for fac, (base, det, acc) in data_v5.APPARENCE.items():
    for couche, src in (("humanoid", "iron"), ("humanoid_leggings", "iron")):
        im = teinter(Image.open(f"{V}/{couche}/{src}.png").convert("RGBA"), base, det, acc, couche)
        p = f"{A}/textures/entity/equipment/{couche}/{fac}.png"
        os.makedirs(os.path.dirname(p), exist_ok=True)
        im.save(p)
    p = f"{A}/equipment/{fac}.json"
    os.makedirs(os.path.dirname(p), exist_ok=True)
    json.dump({"layers": {"humanoid": [{"texture": f"royaumes:{fac}"}],
                          "humanoid_leggings": [{"texture": f"royaumes:{fac}"}]}}, open(p, "w"), indent=1)
print(len(data_v5.APPARENCE), "apparences de faction")
