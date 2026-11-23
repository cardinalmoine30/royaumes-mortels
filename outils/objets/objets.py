# -*- coding: utf-8 -*-
"""Génère tout le contenu « Java » du mod Royaumes Mortels (refonte) :
 - textures 16x16 des objets, blocs et œufs (une couleur de faction par œuf),
 - modèles, définitions d'objets (assets/royaumes/items), états de blocs, butins, recettes, étiquettes,
 - traductions fr_fr / en_us (fusionnées avec l'existant),
 - fr/royaumes/ContenuGenere.java (listes lues par ModObjets, l'écran de serment et la magie),
 - royaumes_creatif/*.json : objets du datapack (armes, kits, forge…) rangés dans les onglets créatifs,
 - apercus/planche_objets.png : planche de contrôle de toutes les textures.
Lancer : python3 outils/objets/objets.py"""
import glob
import json
import math
import os
import random
import sys

from PIL import Image, ImageDraw, ImageFont

ICI = os.path.dirname(os.path.abspath(__file__))
RACINE = os.path.abspath(os.path.join(ICI, "..", ".."))
RES = os.path.join(RACINE, "src", "main", "resources")
ASSETS = os.path.join(RES, "assets", "royaumes")
DATA = os.path.join(RES, "data", "royaumes")
JAVA = os.path.join(RACINE, "src", "main", "java", "fr", "royaumes")
sys.path.insert(0, os.path.join(ICI, ".."))
from donnees_factions import FACTIONS  # noqa: E402

R = random.Random(26)

# ------------------------------------------------------------------------------------------ données
# vent : id, nom, couleur principale, couleur claire, catalyseur vanilla de l'éclat, dimension
VENTS = [
    ("azyr", "Azyr", (70, 140, 255), (200, 230, 255), "minecraft:lightning_rod", "royaumes:royaumes_mortels"),
    ("aqshy", "Aqshy", (240, 90, 20), (255, 210, 90), "minecraft:blaze_powder", "royaumes:aqshy"),
    ("ghur", "Ghur", (160, 100, 50), (230, 200, 150), "minecraft:bone", "royaumes:ghur"),
    ("ghyran", "Ghyran", (60, 190, 70), (190, 250, 160), "minecraft:moss_block", "royaumes:ghyran"),
    ("hysh", "Hysh", (240, 230, 160), (255, 255, 240), "minecraft:glowstone_dust", "royaumes:hysh"),
    ("ulgu", "Ulgu", (100, 90, 140), (190, 180, 220), "minecraft:ink_sac", "royaumes:ulgu"),
    ("shyish", "Shyish", (150, 90, 210), (220, 190, 250), "minecraft:soul_sand", "royaumes:shyish"),
    ("chamon", "Chamon", (220, 170, 40), (255, 235, 140), "minecraft:gold_ingot", "royaumes:chamon"),
]
# sort : (vent, rang, id, nom, coût, recharge en ticks, description)
SORTS = [
    ("azyr", 0, "eclair", "Éclair d'Azyr", 15, 20, "La foudre frappe la cible visée."),
    ("azyr", 1, "comete", "Comète de Sigmar", 60, 200, "Une comète s'abat et foudroie la zone."),
    ("aqshy", 0, "trait", "Trait de flamme", 12, 15, "Lance une salve de boules de feu."),
    ("aqshy", 1, "cendres", "Vague de cendres", 45, 160, "Un cône de feu embrase les ennemis devant toi."),
    ("ghur", 0, "fureur", "Fureur bestiale", 20, 40, "Force et vitesse pendant 15 secondes."),
    ("ghur", 1, "meute", "Meute de Ghur", 50, 400, "Trois loups de Ghur combattent à tes côtés une minute."),
    ("ghyran", 0, "seve", "Sève de vie", 20, 40, "Soigne 8 points de vie et régénère."),
    ("ghyran", 1, "ronces", "Ronces d'Alarielle", 50, 200, "Des ronces entravent et blessent les ennemis proches."),
    ("hysh", 0, "rayon", "Rayon de Hysh", 15, 20, "Un rayon de lumière transperce la cible."),
    ("hysh", 1, "eclat", "Éclat aveuglant", 40, 200, "Aveugle et révèle les ennemis ; brûle les morts-vivants."),
    ("ulgu", 0, "pas", "Pas d'ombre", 15, 30, "Téléporte jusqu'à 16 blocs dans la direction visée."),
    ("ulgu", 1, "voile", "Voile de ténèbres", 45, 300, "Invisibilité ; les ennemis proches sont plongés dans le noir."),
    ("shyish", 0, "main", "Main de poussière", 15, 25, "Flétrit et blesse la cible visée."),
    ("shyish", 1, "moisson", "Moisson des âmes", 55, 240, "Draine la vie des ennemis proches."),
    ("chamon", 0, "peau", "Peau de fer", 20, 60, "Résistance et absorption pendant 20 secondes."),
    ("chamon", 1, "plomb", "Malédiction de plomb", 40, 200, "Alourdit et affaiblit les ennemis proches."),
]
# bloc : id, nom fr, nom en, vent (ou "chaos"), outil, dureté, lumière, recette (base vanilla ou bloc), dessin
BLOCS = [
    ("marbre_celeste", "Marbre céleste", "Celestial Marble", "azyr", "pioche", 1.5, 0, "minecraft:calcite"),
    ("marbre_celeste_grave", "Marbre céleste gravé", "Engraved Celestial Marble", "azyr", "pioche", 1.5, 0, "marbre_celeste"),
    ("basalte_ardent", "Basalte ardent", "Burning Basalt", "aqshy", "pioche", 1.8, 7, "minecraft:basalt"),
    ("brique_de_braise", "Briques de braise", "Ember Bricks", "aqshy", "pioche", 2.0, 4, "basalte_ardent"),
    ("os_de_monstre", "Os de monstre", "Monster Bone", "ghur", "pioche", 2.0, 0, "minecraft:bone_block"),
    ("pierre_de_croc", "Pierre de croc", "Fang Stone", "ghur", "pioche", 2.0, 0, "os_de_monstre"),
    ("bois_de_vie", "Bois de vie", "Lifewood", "ghyran", "hache", 2.0, 0, "minecraft:oak_planks"),
    ("jade_vivant", "Jade vivant", "Living Jade", "ghyran", "pioche", 1.8, 3, "bois_de_vie"),
    ("pierre_de_lumiere", "Pierre de lumière", "Lightstone", "hysh", "pioche", 1.5, 15, "minecraft:quartz_block"),
    ("cristal_de_hysh", "Cristal de Hysh", "Hysh Crystal", "hysh", "pioche", 1.2, 12, "pierre_de_lumiere"),
    ("ardoise_d_ombre", "Ardoise d'ombre", "Shadow Slate", "ulgu", "pioche", 2.5, 0, "minecraft:cobbled_deepslate"),
    ("brume_figee", "Brume figée", "Frozen Mist", "ulgu", "pioche", 1.0, 2, "ardoise_d_ombre"),
    ("pierre_funeraire", "Pierre funéraire", "Gravestone", "shyish", "pioche", 2.0, 0, "minecraft:tuff"),
    ("dalle_des_ames", "Dalle des âmes", "Soulstone Tiles", "shyish", "pioche", 2.0, 5, "pierre_funeraire"),
    ("cuivre_alchimique", "Cuivre alchimique", "Alchemical Copper", "chamon", "pioche", 3.0, 0, "minecraft:copper_block"),
    ("or_vif", "Or vif", "Quickgold", "chamon", "pioche", 3.0, 2, "cuivre_alchimique"),
    ("obsidienne_corrompue", "Obsidienne corrompue", "Corrupted Obsidian", "chaos", "pioche", 20.0, 3, "minecraft:obsidian"),
    ("pierre_du_chaos", "Pierre du Chaos", "Chaos Stone", "chaos", "pioche", 3.0, 6, "obsidienne_corrompue"),
    ("minerai_pierre_royaumes", "Minerai de pierre des Royaumes", "Realmstone Ore", "", "pioche", 3.0, 4, None),
    ("minerai_pierre_royaumes_profond", "Minerai profond de pierre des Royaumes", "Deepslate Realmstone Ore", "", "pioche", 4.5, 4, None),
    ("bloc_pierre_royaumes", "Bloc de pierre des Royaumes", "Block of Realmstone", "", "pioche", 5.0, 9, None),
    ("autel_arcanique", "Autel arcanique", "Arcane Altar", "", "pioche", 3.5, 10, None),
    ("portail_des_royaumes", "Portail des Royaumes", "Realmgate", "", "pioche", 25.0, 11, None),
]
SPECIAUX = {"autel_arcanique": "AUTEL", "portail_des_royaumes": "PORTAIL"}
# objets simples : id, nom fr, nom en, onglet
OBJETS = [("baton_" + v[0], "Bâton " + ("d'" if v[1][0] in "AEIOUH" else "de ") + v[1], v[1] + " Staff", "magie") for v in VENTS]
OBJETS += [("eclat_" + v[0], "Éclat " + ("d'" if v[1][0] in "AEIOUH" else "de ") + v[1], v[1] + " Shard", "magie") for v in VENTS]
OBJETS += [("pierre_royaumes_brute", "Pierre des Royaumes brute", "Raw Realmstone", "magie"),
           ("cristal_arcanique", "Cristal arcanique", "Arcane Crystal", "magie"),
           ("grimoire_des_vents", "Grimoire des Vents", "Grimoire of the Winds", "magie"),
           ("marteau_tempete", "Marteau-tempête", "Stormhammer", "armes")]

FAC_COUL = {}
try:
    sys.path.insert(0, os.path.join(ICI, "..", "gui"))
    from aos import EMBLEMES
    FAC_COUL = {e[0]: (e[1], e[2]) for e in EMBLEMES}
except Exception:  # pragma: no cover
    pass
FAC_COUL.setdefault("orruks", ((60, 110, 40), (230, 190, 40)))


def vent_de_royaume(r):
    r = r.lower()
    for i, v in enumerate(VENTS):
        if r.startswith(v[0]) or r.startswith(v[1].lower()):
            return i
    if "huit" in r:
        return 5
    return 6  # Terres Rongées : Shyish (décrépitude)


def dimension_de_royaume(r):
    r = r.lower()
    if "huit" in r and not r.startswith("hysh"):
        return "royaumes:huit_points"
    if "rong" in r:
        return "royaumes:ulgu"
    return VENTS[vent_de_royaume(r)][5]


# ------------------------------------------------------------------------------------------ pinceaux
def cl(c):
    return tuple(max(0, min(255, int(v))) for v in c[:3])


def mul(c, k):
    return cl([v * k for v in c])


def mix(a, b, t):
    return cl([a[i] + (b[i] - a[i]) * t for i in range(3)])


class T:
    def __init__(s, fond=None):
        s.im = Image.new("RGBA", (16, 16), (0, 0, 0, 0) if fond is None else cl(fond) + (255,))
        s.px = s.im.load()

    def p(s, x, y, c, a=255):
        if 0 <= x < 16 and 0 <= y < 16:
            s.px[x, y] = cl(c) + (a,)

    def get(s, x, y):
        return s.px[x, y]

    def bruit(s, base, amp=0.12, graine=0):
        r = random.Random(graine)
        for y in range(16):
            for x in range(16):
                s.p(x, y, mul(base, 1 + (r.random() - 0.5) * 2 * amp))

    def contour(s, c=(20, 16, 24)):
        a = [[s.px[x, y][3] for x in range(16)] for y in range(16)]
        for y in range(16):
            for x in range(16):
                if a[y][x] == 0:
                    for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < 16 and 0 <= ny < 16 and a[ny][nx] > 0:
                            s.p(x, y, c)
                            break


def ligne(t, pts, c):
    for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
        n = max(abs(x1 - x0), abs(y1 - y0), 1)
        for i in range(n + 1):
            t.p(round(x0 + (x1 - x0) * i / n), round(y0 + (y1 - y0) * i / n), c)


# ------------------------------------------------------------------------------------------ textures d'objets
def manche(t, bois=(110, 70, 40)):
    for i in range(11):
        x, y = 1 + i, 14 - i
        t.p(x, y, mul(bois, 1.15))
        t.p(x + 1, y, mul(bois, 0.75))
    for i in (2, 6):
        t.p(1 + i, 14 - i, (212, 166, 58))
        t.p(2 + i, 14 - i, (150, 110, 30))


def tete_baton(t, v):
    nom, c, cc = v[0], v[2], v[3]
    cx, cy = 12, 4
    if nom == "azyr":  # comète à deux queues
        for (x, y) in [(12, 1), (11, 2), (12, 2), (13, 2), (10, 3), (11, 3), (12, 3), (13, 3), (14, 3), (11, 4), (12, 4), (13, 4), (12, 5)]:
            t.p(x, y, cc)
        t.p(12, 3, (255, 255, 255))
        for i in range(3):
            t.p(9 - i, 6 + i, c)
            t.p(10 - i, 7 + i, mul(c, 0.7))
    elif nom == "aqshy":  # flamme
        for (x, y) in [(12, 0), (11, 1), (12, 1), (13, 2), (11, 2), (12, 2), (10, 3), (11, 3), (12, 3), (13, 3), (10, 4), (11, 4), (12, 4), (13, 4), (14, 4), (11, 5), (12, 5), (13, 5)]:
            t.p(x, y, c)
        for (x, y) in [(12, 3), (11, 4), (12, 4), (12, 2)]:
            t.p(x, y, cc)
    elif nom == "ghur":  # croc recourbé
        for (x, y) in [(10, 1), (11, 1), (12, 1), (13, 2), (14, 3), (14, 4), (13, 5), (12, 4), (11, 3), (12, 3), (13, 3), (13, 4)]:
            t.p(x, y, cc)
        t.p(10, 1, mul(cc, 0.7))
        t.p(14, 4, (255, 255, 255))
    elif nom == "ghyran":  # feuille
        for (x, y) in [(13, 1), (14, 1), (12, 2), (13, 2), (14, 2), (11, 3), (12, 3), (13, 3), (14, 3), (11, 4), (12, 4), (13, 4), (11, 5), (12, 5)]:
            t.p(x, y, c)
        ligne(t, [(11, 5), (14, 1)], cc)
    elif nom == "hysh":  # soleil
        for y in range(2, 7):
            for x in range(10, 15):
                if (x - 12) ** 2 + (y - 4) ** 2 <= 4:
                    t.p(x, y, cc if (x - 12) ** 2 + (y - 4) ** 2 <= 1 else c)
        for (x, y) in [(12, 0), (12, 8), (8, 4), (15, 4), (9, 1), (15, 1), (9, 7)]:
            t.p(x, y, c)
    elif nom == "ulgu":  # croissant de lune
        for y in range(1, 8):
            for x in range(9, 16):
                d1 = (x - 12) ** 2 + (y - 4) ** 2
                d2 = (x - 13.5) ** 2 + (y - 3.2) ** 2
                if d1 <= 9 and d2 > 5:
                    t.p(x, y, cc if d1 <= 4 else c)
    elif nom == "shyish":  # sablier
        for (x, y) in [(10, 1), (11, 1), (12, 1), (13, 1), (14, 1), (11, 2), (12, 2), (13, 2), (12, 3), (12, 4), (11, 5), (12, 5), (13, 5), (10, 6), (11, 6), (12, 6), (13, 6), (14, 6)]:
            t.p(x, y, c)
        t.p(12, 2, cc)
        t.p(12, 5, cc)
        t.p(11, 6, cc)
        t.p(12, 6, cc)
    elif nom == "chamon":  # engrenage
        for y in range(1, 8):
            for x in range(9, 16):
                d = (x - 12) ** 2 + (y - 4) ** 2
                if 2 <= d <= 6:
                    t.p(x, y, c)
        for (x, y) in [(12, 0), (12, 8), (8, 4), (16, 4), (9, 1), (15, 1), (9, 7), (15, 7)]:
            t.p(x, y, mul(c, 0.8))
        t.p(12, 4, cc)


def tex_baton(v):
    t = T()
    manche(t)
    tete_baton(t, v)
    t.contour()
    return t.im


def tex_eclat(v):
    t = T()
    c, cc = v[2], v[3]
    pts = [(8, 2), (10, 5), (11, 9), (9, 13), (7, 13), (5, 9), (6, 5)]
    for y in range(16):
        for x in range(16):
            # point dans le polygone ?
            ins = False
            j = len(pts) - 1
            for i in range(len(pts)):
                xi, yi = pts[i]
                xj, yj = pts[j]
                if (yi > y) != (yj > y) and x < (xj - xi) * (y - yi) / (yj - yi + 1e-9) + xi:
                    ins = not ins
                j = i
            if ins:
                t.p(x, y, mix(cc, c, (x - 5) / 6))
    ligne(t, [(8, 3), (8, 12)], cc)
    t.p(7, 5, (255, 255, 255))
    t.p(7, 6, (255, 255, 255))
    t.contour(mul(c, 0.35))
    return t.im


def tex_pierre_brute():
    t = T()
    r = random.Random(5)
    for y in range(3, 14):
        for x in range(2, 14):
            if (x - 8) ** 2 / 36 + (y - 8.5) ** 2 / 30 <= 1:
                t.p(x, y, mul((110, 96, 120), 0.85 + r.random() * 0.3))
    for i, v in enumerate(VENTS):
        x, y = 4 + (i * 5) % 8, 5 + (i * 3) % 6
        t.p(x, y, v[2])
        t.p(x + 1, y, v[3])
    t.contour()
    return t.im


def tex_cristal():
    t = T()
    for (x0, h, c) in ((5, 9, (120, 90, 255)), (8, 12, (80, 200, 255)), (11, 7, (150, 110, 255))):
        for y in range(15 - h, 15):
            for x in range(x0 - 1, x0 + 2):
                k = 1.25 if x == x0 - 1 else (0.8 if x == x0 + 1 else 1)
                t.p(x, y, mul(c, k))
        t.p(x0, 14 - h, mul(c, 1.3))
    for x in range(3, 14):
        t.p(x, 15, (60, 50, 80))
    t.contour((30, 20, 60))
    return t.im


def tex_grimoire():
    t = T()
    for y in range(2, 15):
        for x in range(3, 13):
            t.p(x, y, (40, 60, 120))
    for y in range(2, 15):
        t.p(3, y, (150, 110, 30))
        t.p(12, y, (240, 230, 200))
    for x in range(4, 12):
        t.p(x, 2, (212, 166, 58))
        t.p(x, 14, (212, 166, 58))
    for (x, y) in [(8, 5), (7, 6), (8, 6), (9, 6), (6, 7), (7, 7), (8, 7), (9, 7), (10, 7), (7, 8), (8, 8), (9, 8), (8, 9)]:
        t.p(x, y, (242, 210, 122))
    for i in range(3):
        t.p(9 + i, 9 + i, (242, 210, 122))
    t.contour()
    return t.im


def tex_marteau():
    t = T()
    manche(t, (60, 70, 110))
    for y in range(1, 7):
        for x in range(9, 16):
            if abs((x - 12) - (y - 4)) <= 3 and abs((x - 12) + (y - 4)) <= 4:
                t.p(x, y, (212, 166, 58) if (x + y) % 5 else (242, 210, 122))
    t.p(12, 4, (70, 140, 255))
    t.p(13, 3, (200, 230, 255))
    t.contour()
    return t.im


def tex_oeuf(c1, c2, graine):
    t = T()
    r = random.Random(graine)
    for y in range(1, 16):
        for x in range(3, 13):
            dy = (y - 9) / (7.0 if y >= 9 else 7.8)
            dx = (x - 7.5) / (5.0 - max(0, (9 - y)) * 0.18)
            if dx * dx + dy * dy <= 1:
                k = 1.18 if x < 7 and y < 9 else (0.82 if x > 9 or y > 12 else 1)
                t.p(x, y, mul(c1, k))
    for _ in range(9):
        x, y = r.randint(4, 11), r.randint(3, 13)
        if t.get(x, y)[3]:
            t.p(x, y, c2)
            if r.random() < 0.6 and t.get(x + 1, y)[3]:
                t.p(x + 1, y, mul(c2, 0.85))
    t.p(5, 4, mix(c1, (255, 255, 255), 0.6))
    t.contour((18, 14, 20))
    return t.im


# ------------------------------------------------------------------------------------------ textures de blocs
def briques(t, c, joint, h=4, w=8, graine=0):
    r = random.Random(graine)
    for y in range(16):
        for x in range(16):
            dec = (w // 2) if (y // h) % 2 else 0
            if y % h == 0 or (x + dec) % w == 0:
                t.p(x, y, joint)
            else:
                t.p(x, y, mul(c, 0.9 + r.random() * 0.2))


def veines(t, c, n, graine, longueur=10):
    r = random.Random(graine)
    for _ in range(n):
        x, y = r.randint(0, 15), r.randint(0, 15)
        for _ in range(longueur):
            t.p(x, y, c)
            x = (x + r.choice((-1, 0, 1, 1))) % 16
            y = (y + r.choice((0, 1, 1))) % 16


def tex_bloc(bid):
    t = T()
    g = sum(map(ord, bid))
    if bid == "marbre_celeste":
        t.bruit((232, 234, 240), 0.05, g)
        veines(t, (210, 175, 90), 3, g, 12)
        veines(t, (180, 190, 215), 2, g + 1, 8)
    elif bid == "marbre_celeste_grave":
        t.bruit((228, 230, 238), 0.04, g)
        for i in range(16):
            t.p(i, 0, (212, 166, 58))
            t.p(i, 15, (150, 110, 30))
            t.p(0, i, (212, 166, 58))
            t.p(15, i, (150, 110, 30))
        for (x, y) in [(8, 3), (7, 5), (8, 5), (9, 5), (5, 7), (6, 7), (7, 7), (8, 7), (9, 7), (10, 7), (11, 7), (7, 9), (8, 9), (9, 9), (8, 11), (8, 6), (8, 8), (8, 10), (8, 4)]:
            t.p(x, y, (212, 166, 58))
        t.p(8, 7, (70, 140, 255))
    elif bid == "basalte_ardent":
        t.bruit((52, 46, 48), 0.15, g)
        veines(t, (255, 120, 20), 4, g, 9)
        veines(t, (255, 210, 80), 2, g + 3, 4)
    elif bid == "brique_de_braise":
        briques(t, (110, 40, 26), (255, 140, 40), graine=g)
    elif bid == "os_de_monstre":
        t.bruit((222, 210, 180), 0.07, g)
        for y in range(16):
            for x in range(16):
                if (x - 8) ** 2 + (y - 8) ** 2 in range(26, 37):
                    t.p(x, y, (170, 150, 110))
        veines(t, (150, 130, 95), 2, g, 6)
    elif bid == "pierre_de_croc":
        t.bruit((120, 100, 80), 0.1, g)
        for cx in (3, 8, 13):
            for i in range(6):
                for dx in range(-(2 - i // 3), 3 - i // 3):
                    t.p(cx + dx, i, (232, 222, 196))
                    t.p(cx + dx + 2, 15 - i, (232, 222, 196))
    elif bid == "bois_de_vie":
        for y in range(16):
            for x in range(16):
                base = (150, 120, 60) if (y // 4) % 2 else (140, 112, 56)
                t.p(x, y, mul(base, 0.92 + 0.08 * math.sin(x * 1.3 + y)))
            if y % 4 == 0:
                for x in range(16):
                    t.p(x, y, (90, 70, 35))
        veines(t, (110, 210, 90), 3, g, 5)
    elif bid == "jade_vivant":
        t.bruit((60, 160, 110), 0.12, g)
        veines(t, (170, 250, 190), 3, g, 10)
        veines(t, (30, 100, 70), 3, g + 1, 8)
    elif bid == "pierre_de_lumiere":
        t.bruit((250, 246, 225), 0.04, g)
        for i in range(16):
            t.p(i, i, (255, 255, 255))
            t.p(15 - i, i, (255, 255, 255))
        for (x, y) in [(7, 7), (8, 7), (7, 8), (8, 8)]:
            t.p(x, y, (255, 220, 120))
    elif bid == "cristal_de_hysh":
        for y in range(16):
            for x in range(16):
                k = ((x * 3 + y * 5) % 16) / 16
                t.p(x, y, mix((210, 240, 255), (255, 250, 220), k))
        for i in range(0, 16, 4):
            ligne(t, [(i, 0), (15, 15 - i)], (255, 255, 255))
    elif bid == "ardoise_d_ombre":
        t.bruit((48, 46, 60), 0.12, g)
        for y in (5, 11):
            for x in range(16):
                t.p(x, y, (30, 28, 40))
    elif bid == "brume_figee":
        r = random.Random(g)
        for y in range(16):
            for x in range(16):
                v = 0.5 + 0.5 * math.sin(x * 0.7 + math.sin(y * 0.6) * 2)
                t.p(x, y, mix((70, 60, 100), (170, 160, 210), v * 0.7 + r.random() * 0.2))
    elif bid == "pierre_funeraire":
        t.bruit((96, 92, 104), 0.1, g)
        veines(t, (70, 66, 80), 4, g, 6)
    elif bid == "dalle_des_ames":
        briques(t, (80, 70, 100), (40, 34, 52), h=8, w=8, graine=g)
        for (x, y) in [(4, 4), (12, 12), (4, 12), (12, 4)]:
            t.p(x, y, (190, 140, 255))
    elif bid == "cuivre_alchimique":
        t.bruit((200, 110, 70), 0.08, g)
        for i in range(16):
            t.p(i, 0, (240, 160, 110))
            t.p(0, i, (240, 160, 110))
            t.p(i, 15, (120, 60, 40))
            t.p(15, i, (120, 60, 40))
        for y in range(4, 12):
            for x in range(4, 12):
                if (x - 7.5) ** 2 + (y - 7.5) ** 2 <= 10:
                    t.p(x, y, (80, 200, 170) if (x + y) % 3 else (60, 160, 140))
    elif bid == "or_vif":
        for y in range(16):
            for x in range(16):
                t.p(x, y, mix((255, 230, 110), (200, 140, 20), (x + y) / 30))
        veines(t, (255, 250, 210), 3, g, 7)
    elif bid == "obsidienne_corrompue":
        t.bruit((30, 16, 40), 0.2, g)
        veines(t, (150, 20, 30), 3, g, 8)
    elif bid == "pierre_du_chaos":
        t.bruit((40, 30, 34), 0.12, g)
        c = (230, 50, 40)
        for a in range(8):
            ang = a * math.pi / 4
            ligne(t, [(8, 8), (round(8 + 6 * math.cos(ang)), round(8 + 6 * math.sin(ang)))], c)
        t.p(8, 8, (255, 200, 120))
    elif bid in ("minerai_pierre_royaumes", "minerai_pierre_royaumes_profond"):
        base = (125, 125, 125) if bid == "minerai_pierre_royaumes" else (70, 70, 76)
        t.bruit(base, 0.1, g)
        r = random.Random(g)
        for i in range(7):
            x, y = r.randint(1, 13), r.randint(1, 13)
            c = VENTS[i % 8][2]
            for dx, dy in ((0, 0), (1, 0), (0, 1), (1, 1)):
                t.p(x + dx, y + dy, mul(c, 1.2 if dx == 0 and dy == 0 else 0.9))
    elif bid == "bloc_pierre_royaumes":
        for y in range(16):
            for x in range(16):
                i = ((x // 4) + (y // 4) * 2) % 8
                t.p(x, y, mul(VENTS[i][2], 0.8 + ((x + y) % 4) * 0.08))
        for i in range(16):
            for (x, y) in ((i, 0), (0, i), (i, 15), (15, i)):
                t.p(x, y, (212, 166, 58))
    elif bid == "autel_arcanique":
        t.bruit((60, 56, 80), 0.08, g)
        for i in range(16):
            for (x, y) in ((i, 0), (0, i), (i, 15), (15, i)):
                t.p(x, y, (212, 166, 58))
        for y in range(4, 12):
            for x in range(4, 12):
                d = abs(x - 7.5) + abs(y - 7.5)
                if d <= 4:
                    t.p(x, y, mix((120, 90, 255), (80, 220, 255), d / 4))
    elif bid == "portail_des_royaumes":
        for y in range(16):
            for x in range(16):
                d = math.hypot(x - 7.5, y - 7.5)
                a = math.atan2(y - 7.5, x - 7.5)
                v = 0.5 + 0.5 * math.sin(a * 3 + d * 1.2)
                t.p(x, y, mix((40, 20, 90), (120, 200, 255), v * max(0, 1 - d / 9)))
        for i in range(16):
            for (x, y) in ((i, 0), (0, i), (i, 15), (15, i), (i, 1), (1, i), (i, 14), (14, i)):
                t.p(x, y, (212, 166, 58) if (x + y) % 2 else (150, 110, 30))
    return t.im


# ------------------------------------------------------------------------------------------ fichiers
def ecrire(chemin, obj):
    os.makedirs(os.path.dirname(chemin), exist_ok=True)
    with open(chemin, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)


def modele_objet(oid, parent="minecraft:item/generated"):
    ecrire(os.path.join(ASSETS, "models", "item", oid + ".json"), {"parent": parent, "textures": {"layer0": "royaumes:item/" + oid}})
    ecrire(os.path.join(ASSETS, "items", oid + ".json"), {"model": {"type": "minecraft:model", "model": "royaumes:item/" + oid}})


def modele_bloc(bid):
    ecrire(os.path.join(ASSETS, "models", "block", bid + ".json"), {"parent": "minecraft:block/cube_all", "textures": {"all": "royaumes:block/" + bid}})
    ecrire(os.path.join(ASSETS, "blockstates", bid + ".json"), {"variants": {"": {"model": "royaumes:block/" + bid}}})
    ecrire(os.path.join(ASSETS, "items", bid + ".json"), {"model": {"type": "minecraft:model", "model": "royaumes:block/" + bid}})


def butin_bloc(bid):
    if bid.startswith("minerai_"):
        entree = {"type": "minecraft:alternatives", "children": [
            {"type": "minecraft:item", "name": "royaumes:" + bid,
             "conditions": [{"condition": "minecraft:match_tool", "predicate": {"predicates": {"minecraft:enchantments": [{"enchantments": "minecraft:silk_touch", "levels": {"min": 1}}]}}}]},
            {"type": "minecraft:item", "name": "royaumes:pierre_royaumes_brute",
             "functions": [{"function": "minecraft:set_count", "count": {"type": "minecraft:uniform", "min": 1, "max": 2}},
                           {"function": "minecraft:apply_bonus", "enchantment": "minecraft:fortune", "formula": "minecraft:ore_drops"},
                           {"function": "minecraft:explosion_decay"}]}]}
    else:
        entree = {"type": "minecraft:item", "name": "royaumes:" + bid}
    ecrire(os.path.join(DATA, "loot_table", "blocks", bid + ".json"),
           {"type": "minecraft:block", "pools": [{"rolls": 1, "entries": [entree], "conditions": [{"condition": "minecraft:survives_explosion"}]}],
            "random_sequence": "royaumes:blocks/" + bid})


def recette(nom, obj):
    ecrire(os.path.join(DATA, "recipe", nom + ".json"), obj)


def forme(motif, cles, resultat, n=1):
    return {"type": "minecraft:crafting_shaped", "category": "misc", "pattern": motif, "key": cles, "result": {"id": resultat, "count": n}}


def sans_forme(ingr, resultat, n=1):
    return {"type": "minecraft:crafting_shapeless", "category": "misc", "ingredients": ingr, "result": {"id": resultat, "count": n}}


def recettes():
    for v in VENTS:
        recette("eclat_" + v[0], sans_forme(["royaumes:pierre_royaumes_brute", v[4]], "royaumes:eclat_" + v[0], 2))
        recette("baton_" + v[0], forme([" GE", " SG", "S  "], {"E": "royaumes:eclat_" + v[0], "G": "minecraft:gold_ingot", "S": "minecraft:stick"}, "royaumes:baton_" + v[0]))
    recette("cristal_arcanique", sans_forme(["royaumes:pierre_royaumes_brute", "royaumes:pierre_royaumes_brute", "minecraft:amethyst_shard"], "royaumes:cristal_arcanique"))
    recette("grimoire_des_vents", sans_forme(["minecraft:book", "royaumes:pierre_royaumes_brute"], "royaumes:grimoire_des_vents"))
    recette("marteau_tempete", forme(["GEG", " S ", " S "], {"G": "minecraft:gold_block", "E": "royaumes:eclat_azyr", "S": "minecraft:stick"}, "royaumes:marteau_tempete"))
    recette("bloc_pierre_royaumes", forme(["PPP", "PPP", "PPP"], {"P": "royaumes:pierre_royaumes_brute"}, "royaumes:bloc_pierre_royaumes"))
    recette("pierre_royaumes_brute_depuis_bloc", sans_forme(["royaumes:bloc_pierre_royaumes"], "royaumes:pierre_royaumes_brute", 9))
    recette("autel_arcanique", forme(["CCC", "GBG", "OOO"], {"C": "royaumes:cristal_arcanique", "G": "minecraft:gold_ingot", "B": "royaumes:bloc_pierre_royaumes", "O": "minecraft:obsidian"}, "royaumes:autel_arcanique"))
    recette("portail_des_royaumes", forme(["OEO", "EBE", "OEO"], {"O": "minecraft:crying_obsidian", "E": "minecraft:ender_eye", "B": "royaumes:bloc_pierre_royaumes"}, "royaumes:portail_des_royaumes"))
    for b in BLOCS:
        bid, base = b[0], b[7]
        if base is None:
            continue
        if base.startswith("minecraft:"):
            cat = "royaumes:eclat_" + b[3] if b[3] != "chaos" else "royaumes:pierre_royaumes_brute"
            recette(bid, forme(["BBB", "BEB", "BBB"], {"B": base, "E": cat}, "royaumes:" + bid, 8))
        else:
            recette(bid, forme(["BB", "BB"], {"B": "royaumes:" + base}, "royaumes:" + bid, 4))


def etiquettes():
    pioche = [("royaumes:" + b[0]) for b in BLOCS if b[4] == "pioche"]
    hache = [("royaumes:" + b[0]) for b in BLOCS if b[4] == "hache"]
    ecrire(os.path.join(RES, "data", "minecraft", "tags", "block", "mineable", "pickaxe.json"), {"replace": False, "values": pioche})
    ecrire(os.path.join(RES, "data", "minecraft", "tags", "block", "mineable", "axe.json"), {"replace": False, "values": hache})
    ecrire(os.path.join(RES, "data", "minecraft", "tags", "block", "needs_iron_tool.json"), {"replace": False, "values": [
        "royaumes:minerai_pierre_royaumes", "royaumes:minerai_pierre_royaumes_profond", "royaumes:bloc_pierre_royaumes"]})
    ecrire(os.path.join(RES, "data", "minecraft", "tags", "block", "needs_diamond_tool.json"), {"replace": False, "values": [
        "royaumes:obsidienne_corrompue", "royaumes:portail_des_royaumes"]})


def generation_minerai():
    biomes = sorted(os.path.splitext(os.path.basename(p))[0] for p in glob.glob(os.path.join(DATA, "worldgen", "biome", "*.json")))
    cible = [{"predicate_type": "minecraft:tag_match", "tag": "minecraft:stone_ore_replaceables"},
             {"predicate_type": "minecraft:tag_match", "tag": "minecraft:deepslate_ore_replaceables"}]
    etats = [{"target": cible[0], "state": "royaumes:minerai_pierre_royaumes"},
             {"target": cible[1], "state": "royaumes:minerai_pierre_royaumes_profond"}]
    # format 26.x (comme le datapack) : dossier « feature », configuration à plat
    ecrire(os.path.join(DATA, "worldgen", "feature", "minerai_pierre_royaumes.json"),
           {"type": "minecraft:ore", "size": 6, "discard_chance_on_air_exposure": 0.0, "targets": etats})
    for nom, n, haut in (("minerai_pierre_royaumes", 10, 96), ("minerai_pierre_royaumes_rare", 3, 40)):
        ecrire(os.path.join(DATA, "worldgen", "placed_feature", nom + ".json"), {
            "feature": "royaumes:minerai_pierre_royaumes",
            "placement": [{"type": "minecraft:count", "count": n}, {"type": "minecraft:in_square"},
                          {"type": "minecraft:height_range", "height": {"type": "minecraft:uniform", "min_inclusive": {"absolute": -48}, "max_inclusive": {"absolute": haut}}},
                          {"type": "minecraft:biome"}]})
    ecrire(os.path.join(DATA, "neoforge", "biome_modifier", "minerai_royaumes.json"), {
        "type": "neoforge:add_features", "biomes": ["royaumes:" + b for b in biomes],
        "features": "royaumes:minerai_pierre_royaumes", "step": "underground_ores"})
    ecrire(os.path.join(DATA, "neoforge", "biome_modifier", "minerai_overworld.json"), {
        "type": "neoforge:add_features", "biomes": "#minecraft:is_overworld",
        "features": "royaumes:minerai_pierre_royaumes_rare", "step": "underground_ores"})


# ------------------------------------------------------------------------------------------ objets du datapack pour le créatif
def piles_datapack():
    """Lit les tables de butin « vitrine » du datapack et en tire des piles d'objets (id + composants)."""
    lt = os.path.join(DATA, "loot_table")

    def lire(motif):
        vus, sortie = set(), []
        for f in sorted(glob.glob(os.path.join(lt, motif), recursive=True)):
            j = json.load(open(f, encoding="utf-8"))
            for p in j.get("pools", []):
                for e in p.get("entries", []):
                    if e.get("type") != "minecraft:item":
                        continue
                    comp = {}
                    mods = e.get("modifier", e.get("functions", []))
                    if isinstance(mods, dict):
                        mods = [mods]
                    for m in mods:
                        if m.get("type", m.get("function")) == "minecraft:set_components":
                            comp.update(m["components"])
                    if not comp.get("minecraft:custom_name") and not comp.get("minecraft:item_name"):
                        continue
                    cle = json.dumps([e["name"], comp.get("minecraft:custom_name"), comp.get("minecraft:item_name")], sort_keys=True)
                    if cle in vus:
                        continue
                    vus.add(cle)
                    sortie.append({"id": e["name"], "count": 1, "components": comp})
        return sortie
    armes = lire("kits/*.json") + lire("forge/*.json") + lire("debug/trophees.json")
    magie = lire("debug/divers.json") + lire("debug/ressources.json")
    out = os.path.join(RES, "royaumes_creatif")
    ecrire(os.path.join(out, "armes.json"), armes)
    ecrire(os.path.join(out, "magie.json"), magie)
    voyage = [s for s in magie if s["components"].get("minecraft:custom_data", {}).get("royaumes") in ("monture", "pierre")]
    ecrire(os.path.join(out, "montures.json"), voyage)
    return len(armes), len(magie)


# ------------------------------------------------------------------------------------------ Java
def jstr(s):
    return '"' + s.replace("\\", "\\\\").replace('"', '\\"') + '"'


def java(mobs, montures):
    L = []
    a = L.append
    a("package fr.royaumes;\n")
    a("/** FICHIER GÉNÉRÉ par outils/objets/objets.py : ne pas modifier à la main. */")
    a("public final class ContenuGenere {")
    a("    private ContenuGenere() {}\n")
    a("    /** Les huit Vents de magie (index = icône du HUD). */")
    a("    public static final String[] VENTS = {" + ", ".join(jstr(v[0]) for v in VENTS) + "};")
    a("    public static final String[] NOMS_VENTS = {" + ", ".join(jstr(v[1]) for v in VENTS) + "};")
    a("    public static final int[] COULEURS_VENTS = {" + ", ".join("0x%02X%02X%02X" % v[2] for v in VENTS) + "};")
    a("    public static final String[] DIMENSIONS_VENTS = {" + ", ".join(jstr(v[5]) for v in VENTS) + "};\n")
    a("    /** Sorts : [vent][rang] (0 = sort mineur, clic droit ; 1 = grand sort, accroupi + clic droit). */")
    for champ, idx, fmt in (("SORTS_IDS", 2, jstr), ("SORTS_NOMS", 3, jstr), ("SORTS_DESC", 6, jstr)):
        a("    public static final String[][] %s = {" % champ)
        for v in VENTS:
            s = [x for x in SORTS if x[0] == v[0]]
            a("        {" + ", ".join(fmt(x[idx]) for x in sorted(s, key=lambda z: z[1])) + "},")
        a("    };")
    for champ, idx in (("SORTS_COUTS", 4), ("SORTS_RECHARGES", 5)):
        a("    public static final int[][] %s = {" % champ)
        for v in VENTS:
            s = sorted([x for x in SORTS if x[0] == v[0]], key=lambda z: z[1])
            a("        {" + ", ".join(str(x[idx]) for x in s) + "},")
        a("    };")
    a("")
    a("    /** Blocs : id, outil, dureté, lumière, type spécial. */")
    a("    public static final String[] BLOCS = {" + ", ".join(jstr(b[0]) for b in BLOCS) + "};")
    a("    public static final float[] BLOCS_DURETE = {" + ", ".join("%.1ff" % b[5] for b in BLOCS) + "};")
    a("    public static final int[] BLOCS_LUMIERE = {" + ", ".join(str(b[6]) for b in BLOCS) + "};")
    a("    public static final boolean[] BLOCS_BOIS = {" + ", ".join("true" if b[4] == "hache" else "false" for b in BLOCS) + "};")
    a("    public static final String[] BLOCS_SPECIAL = {" + ", ".join(jstr(SPECIAUX.get(b[0], "")) for b in BLOCS) + "};\n")
    a("    /** Écran de serment : données des 25 factions (index = numéro rm_faction, 0 = aucune). */")
    fs = [None] + FACTIONS
    for champ, cle in (("ALLIANCES", "alliance"), ("ROYAUMES", "royaume"), ("DESCRIPTIONS", "desc"), ("DONS", "bonus"), ("FARDEAUX", "malus")):
        a("    public static final String[] %s = {" % champ + ", ".join(jstr(f[cle]) if f else '""' for f in fs) + "};")
    a("    public static final int[] VENT_FACTION = {0, " + ", ".join(str(vent_de_royaume(f["royaume"])) for f in FACTIONS) + "};")
    a("    public static final String[] DIMENSION_FACTION = {\"\", " + ", ".join(jstr(dimension_de_royaume(f["royaume"])) for f in FACTIONS) + "};\n")
    a("    /** Œufs : créature -> couleurs (fond, taches) pour l'aperçu. */")
    a("    public static final String[] OEUFS_MOBS = {" + ", ".join(jstr(m["id"]) for m in mobs) + "};")
    a("    public static final String[] OEUFS_MONTURES = {" + ", ".join(jstr(m["id"]) for m in montures) + "};")
    a("}")
    with open(os.path.join(JAVA, "ContenuGenere.java"), "w", encoding="utf-8") as f:
        f.write("\n".join(L) + "\n")


# ------------------------------------------------------------------------------------------ traductions
def traductions(mobs, montures):
    fr, en = {}, {}
    for oid, nf, ne, _ in OBJETS:
        fr["item.royaumes." + oid] = nf
        en["item.royaumes." + oid] = ne
    for b in BLOCS:
        fr["block.royaumes." + b[0]] = b[1]
        en["block.royaumes." + b[0]] = b[2]
    for m in mobs:
        fr["item.royaumes.oeuf_" + m["id"]] = "Œuf d'apparition : " + m["nom"]
        en["item.royaumes.oeuf_" + m["id"]] = m["nom"] + " Spawn Egg"
    for m in montures:
        fr["item.royaumes.oeuf_" + m["id"]] = "Œuf de monture : " + m["nom"]
        en["item.royaumes.oeuf_" + m["id"]] = m["nom"] + " Mount Egg"
    onglets = {"armes": ("Royaumes — Armes et armures", "Realms — Weapons & Armour"),
               "magie": ("Royaumes — Magie", "Realms — Magic"),
               "blocs": ("Royaumes — Blocs des Royaumes", "Realms — Realm Blocks"),
               "creatures": ("Royaumes — Créatures", "Realms — Creatures"),
               "montures": ("Royaumes — Montures et voyage", "Realms — Mounts & Travel")}
    for k, (a, b) in onglets.items():
        fr["itemGroup.royaumes." + k] = a
        en["itemGroup.royaumes." + k] = b
    textes = {
        "royaumes.sort.mineur": ("Clic droit : %s (%s énergie)", "Right-click: %s (%s energy)"),
        "royaumes.sort.majeur": ("Accroupi + clic droit : %s (%s énergie)", "Sneak + right-click: %s (%s energy)"),
        "royaumes.sort.royaume": ("Moitié prix dans le Royaume de %s", "Half cost in the Realm of %s"),
        "royaumes.sort.manque": ("Énergie arcanique insuffisante (%s/%s)", "Not enough arcane energy (%s/%s)"),
        "royaumes.sort.lance": ("%s — %s énergie", "%s — %s energy"),
        "royaumes.cristal.info": ("Clic droit : rend 40 points d'énergie arcanique", "Right-click: restores 40 arcane energy"),
        "royaumes.grimoire.info": ("Clic droit : liste des sorts et de ton énergie", "Right-click: lists spells and your energy"),
        "royaumes.autel.info": ("L'autel recharge ton énergie arcanique.", "The altar refills your arcane energy."),
        "royaumes.autel.attente": ("L'autel se recharge encore (%s s).", "The altar is still recharging (%s s)."),
        "royaumes.portail.info": ("Le Portail des Royaumes s'ouvre…", "The Realmgate opens…"),
        "royaumes.energie": ("Énergie arcanique", "Arcane energy"),
        "royaumes.niveau": ("Niveau %s", "Level %s"),
        "royaumes.royaume": ("Royaume de %s", "Realm of %s"),
        "royaumes.serment.titre": ("Serment d'allégeance", "Oath of Allegiance"),
        "royaumes.serment.bouton": ("Prêter serment", "Swear the oath"),
        "royaumes.serment.deja": ("Serment prêté", "Oath sworn"),
        "royaumes.serment.aide": ("Survole un blason pour lire son serment.", "Hover a crest to read its oath."),
        "royaumes.serment.touche": ("Touche J : rouvrir cet écran.", "J key: reopen this screen."),
        "royaumes.serment.dons": ("Dons", "Gifts"),
        "royaumes.serment.fardeau": ("Fardeau", "Burden"),
        "royaumes.serment.choisi": ("Tu as prêté serment : %s", "You have sworn your oath: %s"),
        "key.royaumes.serment": ("Écran de serment", "Oath screen"),
        "key.categories.royaumes": ("Royaumes Mortels", "Mortal Realms"),
        "key.category.royaumes.royaumes": ("Royaumes Mortels", "Mortal Realms"),
    }
    for k, (a, b) in textes.items():
        fr[k] = a
        en[k] = b
    for v in VENTS:
        s = sorted([x for x in SORTS if x[0] == v[0]], key=lambda z: z[1])
        for x in s:
            fr["royaumes.sort." + x[2]] = x[3]
            en["royaumes.sort." + x[2]] = x[3]
    for lang, d in (("fr_fr", fr), ("en_us", en)):
        p = os.path.join(ASSETS, "lang", lang + ".json")
        old = json.load(open(p, encoding="utf-8")) if os.path.exists(p) else {}
        old.update(d)
        ecrire(p, old)


# ------------------------------------------------------------------------------------------ planche
def planche(objs, blocs, oeufs):
    k = 4
    col = 16
    toutes = [("Objets", objs), ("Blocs", blocs), ("Œufs (extrait)", oeufs[:48])]
    h = 40 + sum(30 + ((len(l) + col - 1) // col) * (16 * k + 8) for _, l in toutes)
    W = 40 + col * (16 * k + 8)
    im = Image.new("RGB", (W, h), (14, 26, 51))
    d = ImageDraw.Draw(im)
    f = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf", 20)
    y = 16
    for titre, liste in toutes:
        d.text((20, y), titre, font=f, fill=(242, 210, 122))
        y += 30
        for i, img in enumerate(liste):
            x = 20 + (i % col) * (16 * k + 8)
            yy = y + (i // col) * (16 * k + 8)
            d.rectangle((x - 2, yy - 2, x + 16 * k + 1, yy + 16 * k + 1), fill=(24, 34, 62))
            im.paste(img.resize((16 * k, 16 * k), Image.NEAREST), (x, yy), img.resize((16 * k, 16 * k), Image.NEAREST))
        y += ((len(liste) + col - 1) // col) * (16 * k + 8)
    os.makedirs(os.path.join(ICI, "apercus"), exist_ok=True)
    im.save(os.path.join(ICI, "apercus", "planche_objets.png"))


def main():
    mobs = json.load(open(os.path.join(RACINE, "outils", "modeles", "liste_mobs.json"), encoding="utf-8"))
    montures = json.load(open(os.path.join(RACINE, "outils", "modeles", "liste_montures.json"), encoding="utf-8"))
    ti = os.path.join(ASSETS, "textures", "item")
    tb = os.path.join(ASSETS, "textures", "block")
    os.makedirs(ti, exist_ok=True)
    os.makedirs(tb, exist_ok=True)
    apercu_o, apercu_b, apercu_e = [], [], []
    for oid, _, _, _ in OBJETS:
        if oid.startswith("baton_"):
            im = tex_baton([v for v in VENTS if v[0] == oid[6:]][0])
        elif oid.startswith("eclat_"):
            im = tex_eclat([v for v in VENTS if v[0] == oid[6:]][0])
        else:
            im = {"pierre_royaumes_brute": tex_pierre_brute, "cristal_arcanique": tex_cristal,
                  "grimoire_des_vents": tex_grimoire, "marteau_tempete": tex_marteau}[oid]()
        im.save(os.path.join(ti, oid + ".png"))
        modele_objet(oid, "minecraft:item/handheld" if oid.startswith("baton_") or oid == "marteau_tempete" else "minecraft:item/generated")
        apercu_o.append(im)
    for b in BLOCS:
        im = tex_bloc(b[0])
        im.save(os.path.join(tb, b[0] + ".png"))
        modele_bloc(b[0])
        butin_bloc(b[0])
        apercu_b.append(im)
    for i, m in enumerate(mobs + montures):
        fac = m.get("fac") or m.get("faction")
        c1, c2 = FAC_COUL.get(fac, ((120, 120, 120), (230, 230, 230)))
        if i >= len(mobs):
            c1, c2 = c2, c1  # montures : couleurs inversées pour les distinguer
        im = tex_oeuf(c1, c2, i)
        im.save(os.path.join(ti, "oeuf_" + m["id"] + ".png"))
        modele_objet("oeuf_" + m["id"])
        apercu_e.append(im)
    recettes()
    etiquettes()
    generation_minerai()
    na, nm = piles_datapack()
    java(mobs, montures)
    traductions(mobs, montures)
    planche(apercu_o, apercu_b, apercu_e)
    print("objets", len(OBJETS), "blocs", len(BLOCS), "oeufs", len(mobs) + len(montures), "créatif armes", na, "magie", nm)


if __name__ == "__main__":
    main()
