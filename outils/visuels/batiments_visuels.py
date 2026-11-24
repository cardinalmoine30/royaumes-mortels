# -*- coding: utf-8 -*-
"""Planches des bâtiments du camp (rendu des vrais plans ; blocs vanilla en couleurs approchées)."""
import os
import sys
from PIL import Image, ImageDraw, ImageFont

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "objets"))
import scenes  # noqa: E402
from scenes import Scene, TEX, terrain  # noqa: E402
from batiments import plan, BATIMENTS, STYLES  # noqa: E402

COUL = {"anvil": (60, 60, 64), "barrel": (120, 86, 50), "blast_furnace": (90, 90, 96), "blue_terracotta": (74, 60, 120), "bone_block": (226, 220, 196),
        "bookshelf": (120, 80, 50), "brown_wool": (114, 72, 40), "campfire": (230, 120, 40), "carrots": (240, 130, 30), "chest": (160, 110, 40),
        "coarse_dirt": (110, 80, 56), "cobblestone": (120, 120, 120), "composter": (110, 80, 40), "crafting_table": (140, 100, 60),
        "crimson_planks": (110, 48, 70), "dark_oak_planks": (66, 44, 22), "deepslate_tiles": (54, 54, 58), "enchanting_table": (60, 20, 40),
        "farmland": (90, 60, 40), "fletching_table": (180, 160, 110), "furnace": (110, 110, 110), "glass_pane": (190, 220, 230),
        "gray_wool": (70, 74, 78), "grindstone": (140, 140, 140), "hay_block": (200, 170, 40), "lantern": (255, 200, 90),
        "lava_cauldron": (240, 110, 20), "magma_block": (190, 80, 20), "polished_blackstone": (50, 44, 54),
        "polished_blackstone_bricks": (44, 38, 46), "polished_deepslate": (70, 70, 74), "red_nether_bricks": (90, 14, 16),
        "red_wool": (160, 40, 36), "scaffolding": (200, 170, 100), "skeleton_skull": (210, 210, 200), "smithing_table": (60, 50, 60),
        "smoker": (100, 90, 80), "soul_lantern": (90, 220, 230), "spruce_log": (70, 50, 30), "spruce_planks": (114, 84, 50),
        "target": (230, 200, 190), "water_cauldron": (60, 90, 200), "wheat": (200, 190, 80), "white_wool": (234, 236, 236)}
EMIS = {"lantern", "soul_lantern", "magma_block", "lava_cauldron", "campfire"}


def tex(bid):
    ns, n = bid.split(":")
    if ns == "royaumes":
        return os.path.join(TEX, "block", n + ".png"), n in ("pierre_de_lumiere", "cristal_de_hysh", "pierre_du_chaos", "dalle_des_ames")
    return terrain("v_" + n, COUL.get(n, (150, 150, 150)), 0.1, hash(n) % 100), n in EMIS


def rendu(b, ciel=((90, 120, 170), (190, 205, 225)), taille=(640, 520)):
    scenes.W, scenes.H = taille
    s = Scene(ciel[0], ciel[1], ciel[1], 80)
    herbe = terrain("herbe_planche", (100, 140, 80), 0.1, 31)
    for x in range(-6, 7):
        for z in range(-6, 7):
            if (x, -1, z) not in b:
                s.bloc(x, -1, z, herbe, faces=("up",))
    for (x, y, z), bid in b.items():
        chemin, e = tex(bid)
        s.bloc(x, y, z, chemin, emissif=e)
    hmax = max(k[1] for k in b)
    img = s.rendre((9 + hmax * 0.4, 7 + hmax * 0.55, -13 - hmax * 0.6), (0, hmax * 0.4, 0), fov=50)
    scenes.W, scenes.H = 1280, 720
    return img


def planche(titre, cases, sortie, col):
    w, h = 640, 520
    lignes = (len(cases) + col - 1) // col
    im = Image.new("RGB", (col * w, lignes * (h + 40) + 70), (14, 26, 51))
    d = ImageDraw.Draw(im)
    f = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf", 34)
    f2 = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 22)
    d.text((col * w // 2, 16), titre, font=f, fill=(242, 210, 122), anchor="mt")
    for i, (nom, b) in enumerate(cases):
        x, y = (i % col) * w, 70 + (i // col) * (h + 40)
        im.paste(rendu(b).convert("RGB"), (x, y + 36))
        d.text((x + w // 2, y + 6), nom, font=f2, fill=(230, 211, 168), anchor="mt")
    im.save(sortie)
    print(sortie)


if __name__ == "__main__":
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "apercus", "camp")
    os.makedirs(out, exist_ok=True)
    noms = {"ordre": "Ordre", "chaos": "Chaos", "mort": "Mort", "destruction": "Destruction"}
    planche("La forge selon les quatre Grandes Alliances (niveau 3)", [(noms[s], plan("forge", 3, s)) for s in STYLES],
            os.path.join(out, "forge_4_styles.png"), 2)
    planche("Forge de l'Ordre : niveaux 1, 2 et 3", [("Niveau %d" % n, plan("forge", n, "ordre")) for n in (1, 2, 3)],
            os.path.join(out, "forge_3_niveaux.png"), 3)
    for st in STYLES:
        planche("Camp " + noms[st] + " : les cinq bâtiments (niveau 3)",
                [(b.capitalize(), plan(b, 3, st)) for b in BATIMENTS] + [("Tour niveau 1", plan("tour", 1, st))],
                os.path.join(out, "batiments_" + st + ".png"), 3)
