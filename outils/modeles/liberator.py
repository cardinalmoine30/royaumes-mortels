# -*- coding: utf-8 -*-
"""Liberator Stormcast (Hammers of Sigmar) : modèle provisoire GeckoLib.
À remplacer par le modèle Blockbench de l'utilisateur quand il sera prêt
(mêmes noms d'os pour garder les animations)."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from modele import Modele, apercu_vues

OR = (212, 165, 44)
OR_C = (240, 204, 96)
OR_S = (150, 108, 24)
TURQ = (38, 150, 160)
BLEU = (32, 62, 150)
NOIR = (22, 22, 28)
CYAN = (110, 235, 255)


def bande(couleur, epais=1, ou="bas"):
    def f(d, x, y, w, h, px):
        for k in range(epais):
            yy = y + (h - 1 - k if ou == "bas" else k)
            d.line((x, yy, x + w - 1, yy), fill=couleur)
    return f


def combine(*fs):
    def f(*a):
        for g in fs:
            g(*a)
    return f


def comete(d, x, y, w, h, px):
    cx, cy = x + w // 2, y + h // 2
    d.rectangle((x, y, x + w - 1, y + h - 1), fill=TURQ)
    d.rectangle((cx - 1, cy - 1, cx, cy), fill=OR_C)        # tête de la comète
    d.line((cx - 1, cy + 1, x, y + h - 1), fill=OR)          # queues jumelles
    d.line((cx + 1, cy + 1, x + w - 1, y + h - 1), fill=OR)


def visiere(d, x, y, w, h, px):
    d.rectangle((x, y, x + w - 1, y + h - 1), fill=NOIR)
    d.point((x + 1, y), fill=CYAN)
    d.point((x + w - 2, y), fill=CYAN)


def casque_face(d, x, y, w, h, px):
    d.line((x + w // 2 - 1, y + 4, x + w // 2 - 1, y + h - 1), fill=OR_S)   # arête du nez
    d.line((x + w // 2, y + 4, x + w // 2, y + h - 1), fill=OR_S)
    d.line((x, y + h - 2, x + w - 1, y + h - 2), fill=TURQ)


def eclair(d, x, y, w, h, px):
    pts = [(x + w // 2, y), (x + 1, y + h // 2), (x + w - 2, y + h // 2), (x + w // 2 - 1, y + h - 1)]
    d.line(pts, fill=CYAN)


def cape(d, x, y, w, h, px):
    d.line((x, y + h - 1, x + w - 1, y + h - 1), fill=OR)
    d.line((x, y + h - 2, x + w - 1, y + h - 2), fill=OR_S)


def tabard(d, x, y, w, h, px):
    d.rectangle((x, y, x, y + h - 1), fill=OR)
    d.rectangle((x + w - 1, y, x + w - 1, y + h - 1), fill=OR)
    d.line((x + 2, y + 3, x + w - 3, y + 3), fill=BLEU)
    d.line((x + w // 2, y + 1, x + w // 2, y + 6), fill=BLEU)


PAL = {
    "or": {"base": OR, "bord": OR_S, "bruit": 7},
    "or_sombre": {"base": OR_S, "bord": (110, 80, 20)},
    "turq": {"base": TURQ, "bord": (24, 100, 110)},
    "cape": {"base": BLEU, "bord": (22, 42, 110), "bruit": 5},
    "creme": {"base": (226, 214, 182), "bord": (190, 175, 140), "bruit": 4},
    "cuir": {"base": (78, 50, 32), "bord": (50, 32, 20)},
    "noir": {"base": NOIR, "bord": NOIR, "bruit": 2},
    "acier": {"base": (70, 66, 72), "bord": (40, 38, 44)},
    "crete": {"base": (40, 70, 170), "bord": (26, 46, 120)},
}

m = Modele("liberator")
m.bone("root", None, (0, 0, 0))
m.bone("right_leg", "root", (-3, 13, 0))
m.bone("left_leg", "root", (3, 13, 0))
m.bone("body", "root", (0, 13, 0))
m.bone("cape", "body", (0, 27, 4))
m.bone("head", "body", (0, 28, 0))
m.bone("right_arm", "body", (-9, 26, 0))
m.bone("hammer", "right_arm", (-10, 12, -5))
m.bone("left_arm", "body", (9, 26, 0))
m.bone("shield", "left_arm", (12, 16, 0))

# jambes (grèves dorées, genouillère turquoise)
for os_, x in (("right_leg", -6), ("left_leg", 1)):
    m.cube(os_, (x, 0, -3), (5, 13, 6), "or", north=combine(bande(TURQ, 1, "haut"), bande(OR_S, 2, "bas")))
# corps
m.cube("body", (-6, 13, -4), (12, 3, 8), "cuir", north=lambda d, x, y, w, h, px: d.rectangle((x + w // 2 - 1, y, x + w // 2, y + h - 1), fill=OR_C))
m.cube("body", (-7, 16, -4), (14, 12, 8), "or", north=combine(bande(TURQ, 1, "bas"), bande(TURQ, 1, "haut")),
       south=bande(TURQ, 1, "bas"))
m.cube("body", (-3, 5, -5), (6, 10, 1), "creme", north=tabard)
m.cube("body", (-3, 19, -5), (6, 6, 1), "turq", north=comete)
m.cube("body", (-5, 27, -4), (10, 2, 8), "or_sombre")
m.cube("cape", (-6, 6, 4), (12, 21, 1), "cape", south=cape, north=cape)
# tête
m.cube("head", (-4, 28, -4), (8, 9, 8), "or", north=casque_face, east=bande(TURQ, 1), west=bande(TURQ, 1))
m.cube("head", (-3, 31, -5), (6, 2, 1), "noir", north=visiere)
m.cube("head", (-1, 37, -4), (2, 3, 9), "crete")
# bras droit + marteau
m.cube("right_arm", (-13, 24, -5), (7, 6, 10), "or", toutes=bande(TURQ, 1, "bas"))
m.cube("right_arm", (-12, 13, -3), (5, 11, 6), "or", north=bande(OR_S, 3, "bas"))
m.cube("hammer", (-11, 2, -6), (2, 17, 2), "cuir")
m.cube("hammer", (-13, 18, -8), (6, 5, 6), "acier", north=eclair, south=eclair, east=eclair, west=eclair,
       up=lambda d, x, y, w, h, px: d.rectangle((x + 1, y + 1, x + w - 2, y + h - 2), outline=OR))
# bras gauche + bouclier
m.cube("left_arm", (6, 24, -5), (7, 6, 10), "or", toutes=bande(TURQ, 1, "bas"))
m.cube("left_arm", (7, 13, -3), (5, 11, 6), "or", north=bande(OR_S, 3, "bas"))
m.cube("shield", (12, 8, -7), (2, 16, 14), "or", west=lambda d, x, y, w, h, px: d.rectangle((x + 1, y + 1, x + w - 2, y + h - 2), outline=TURQ))
m.cube("shield", (14, 13, -3), (1, 6, 6), "turq", west=comete)

# Animations (noms GeckoLib par défaut : misc.idle, move.walk, attack.swing, misc.die)
def kf(**pts):
    return {str(k).replace("_", "."): v for k, v in pts.items()}

ANIMS = {
    "misc.idle": {"loop": True, "animation_length": 3.0, "bones": {
        "body": {"position": {"0.0": [0, 0, 0], "1.5": [0, -0.3, 0], "3.0": [0, 0, 0]}},
        "head": {"rotation": {"0.0": [0, 0, 0], "1.5": [2, 0, 0], "3.0": [0, 0, 0]}},
        "cape": {"rotation": {"0.0": [4, 0, 0], "1.5": [8, 0, 0], "3.0": [4, 0, 0]}},
        "right_arm": {"rotation": {"0.0": [-6, 0, 0], "1.5": [-9, 0, 0], "3.0": [-6, 0, 0]}},
        "left_arm": {"rotation": {"0.0": [-12, 0, -4], "1.5": [-14, 0, -4], "3.0": [-12, 0, -4]}}}},
    "move.walk": {"loop": True, "animation_length": 1.0, "bones": {
        "right_leg": {"rotation": {"0.0": [28, 0, 0], "0.5": [-28, 0, 0], "1.0": [28, 0, 0]}},
        "left_leg": {"rotation": {"0.0": [-28, 0, 0], "0.5": [28, 0, 0], "1.0": [-28, 0, 0]}},
        "right_arm": {"rotation": {"0.0": [-20, 0, 0], "0.5": [10, 0, 0], "1.0": [-20, 0, 0]}},
        "left_arm": {"rotation": {"0.0": [-12, 0, -4], "0.5": [-20, 0, -4], "1.0": [-12, 0, -4]}},
        "cape": {"rotation": {"0.0": [18, 0, 0], "0.5": [24, 0, 0], "1.0": [18, 0, 0]}},
        "body": {"position": {"0.0": [0, 0, 0], "0.25": [0, 0.6, 0], "0.5": [0, 0, 0], "0.75": [0, 0.6, 0], "1.0": [0, 0, 0]}}}},
    "attack.swing": {"loop": False, "animation_length": 0.6, "bones": {
        "right_arm": {"rotation": {"0.0": [0, 0, 0], "0.2": [-165, 0, -10], "0.35": [-40, 0, 0], "0.6": [0, 0, 0]}},
        "body": {"rotation": {"0.0": [0, 0, 0], "0.2": [-6, 8, 0], "0.35": [10, -6, 0], "0.6": [0, 0, 0]}}}},
    "misc.die": {"loop": "hold_on_last_frame", "animation_length": 1.0, "bones": {
        "root": {"rotation": {"0.0": [0, 0, 0], "1.0": [-85, 0, 0]}},
        "hammer": {"rotation": {"0.0": [0, 0, 0], "0.6": [40, 0, 0]}}}},
}

if __name__ == "__main__":
    tex = m.exporter(PAL, ANIMS)
    sortie = sys.argv[1] if len(sys.argv) > 1 else "/tmp/apercu_liberator.png"
    apercu_vues(m, tex, sortie, "Liberator Stormcast — modèle provisoire")
    print("ok", sortie)
