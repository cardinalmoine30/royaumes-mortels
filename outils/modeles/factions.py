# -*- coding: utf-8 -*-
"""Génère TOUS les mobs de faction et les boss du mod :
- modèles GeckoLib (.geo.json), animations et textures (version rapide, provisoire) ;
- src/main/java/fr/royaumes/ProfilsGeneres.java (stats, alliance, capacité, taille) ;
- traductions, apparitions dans les biomes, fonction de test royaumes:debug/mobs ;
- planches d'aperçu dans outils/modeles/apercus/.
Usage : python3 factions.py
"""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from modele import Modele, apercu_vues, ASSETS, RACINE
from PIL import Image, ImageDraw, ImageFont

ICI = os.path.dirname(os.path.abspath(__file__))


def sombre(c, k=0.68):
    return tuple(int(v * k) for v in c)


# ---------------------------------------------------------------- dessins de détails
def yeux(couleur, fond=None, y_rel=0.45):
    def f(d, x, y, w, h, px):
        if fond:
            d.rectangle((x + 1, y + int(h * y_rel) - 1, x + w - 2, y + int(h * y_rel) + 1), fill=fond)
        yy = y + int(h * y_rel)
        d.point((x + w // 2 - 2, yy), fill=couleur)
        d.point((x + w // 2 + 1, yy), fill=couleur)
    return f


def crane(d, x, y, w, h, px):
    d.rectangle((x + 1, y + 3, x + 2, y + 4), fill=(20, 20, 20))
    d.rectangle((x + w - 3, y + 3, x + w - 2, y + 4), fill=(20, 20, 20))
    d.point((x + w // 2, y + 5), fill=(30, 30, 30))
    for i in range(1, w - 1, 2):
        d.point((x + i, y + h - 2), fill=(40, 40, 40))


def dents(d, x, y, w, h, px):
    for i in range(1, w - 1, 2):
        d.point((x + i, y), fill=(235, 230, 200))
    d.point((x + 1, y + 1), fill=(235, 230, 200))
    d.point((x + w - 2, y + 1), fill=(235, 230, 200))


def embleme(forme, c):
    def f(d, x, y, w, h, px):
        cx, cy = x + w // 2, y + h // 2
        if forme == "comete":
            d.rectangle((cx - 1, cy - 2, cx, cy - 1), fill=c)
            d.line((cx - 1, cy, cx - 3, cy + 3), fill=c)
            d.line((cx, cy, cx + 2, cy + 3), fill=c)
        elif forme == "etoile":   # étoile du Chaos
            for dx, dy in ((0, -3), (0, 3), (-3, 0), (3, 0), (-2, -2), (2, 2), (-2, 2), (2, -2)):
                d.line((cx, cy, cx + dx, cy + dy), fill=c)
        elif forme == "crane":
            d.rectangle((cx - 2, cy - 2, cx + 1, cy + 1), fill=c)
            d.point((cx - 1, cy - 1), fill=(20, 20, 20))
            d.point((cx, cy - 1), fill=(20, 20, 20))
            d.line((cx - 1, cy + 2, cx, cy + 2), fill=c)
        elif forme == "croc":
            d.polygon([(cx - 3, cy - 2), (cx + 2, cy - 2), (cx - 1, cy + 3)], fill=c)
        else:
            d.rectangle((cx - 1, cy - 1, cx, cy), fill=c)
    return f


def bande(c, ou="bas", ep=1):
    def f(d, x, y, w, h, px):
        for k in range(ep):
            yy = y + (h - 1 - k if ou == "bas" else k)
            d.line((x, yy, x + w - 1, yy), fill=c)
    return f


def eclair(c):
    def f(d, x, y, w, h, px):
        d.line([(x + w // 2, y + 1), (x + 1, y + h // 2), (x + w - 2, y + h // 2), (x + w // 2 - 1, y + h - 2)], fill=c)
    return f


def anneau(c):
    """Halo : anneau doré à rayons, centre transparent."""
    def f(d, x, y, w, h, px):
        for i in range(w):
            for j in range(h):
                px[x + i, y + j] = (0, 0, 0, 0)
        cx, cy = x + (w - 1) / 2, y + (h - 1) / 2
        r = min(w, h) / 2 - 1.5
        for i in range(w):
            for j in range(h):
                dist = ((x + i - cx) ** 2 + (y + j - cy) ** 2) ** 0.5
                if r - 1 <= dist <= r + 0.4:
                    px[x + i, y + j] = c + (255,)
        for dx, dy in ((0, -1), (1, -1), (-1, -1), (1, 0), (-1, 0)):
            px[int(cx + dx * (r + 1.2)), int(cy + dy * (r + 1.2))] = c + (255,)
    return f


def combine(*fs):
    def f(*a):
        for g in fs:
            if g:
                g(*a)
    return f


# ---------------------------------------------------------------- gabarits de corps
CORPS = {
    #           jambe (w,h,d)  torse (w,h,d)  bras (w,h,d)  tête
    "massif":   ((5, 13, 6), (14, 12, 8), (5, 11, 6), 8),
    "normal":   ((4, 12, 4), (8, 12, 4), (4, 12, 4), 8),
    "fin":      ((3, 14, 3), (8, 12, 4), (3, 13, 3), 7),
    "petit":    ((3, 7, 3), (8, 8, 5), (3, 9, 3), 7),
    "nain":     ((4, 6, 5), (12, 10, 7), (4, 9, 5), 8),
    "squelette": ((2, 12, 2), (8, 12, 3), (2, 12, 2), 8),
    "spectre":  (None, (8, 12, 5), (3, 12, 3), 8),
    "geant":    ((6, 12, 6), (16, 14, 10), (6, 14, 6), 8),
}


def construire(nom, s):
    """s : dict de spécification (corps, palette, tete, arme, extras...)."""
    jambe, torse, bras, hs = CORPS[s["corps"]]
    P = s["pal"]
    m = Modele(nom)
    lh = jambe[1] if jambe else 10
    tw, th, td = torse
    aw, ah, ad = bras
    yt = lh + th            # haut du torse
    m.bone("root", None, (0, 0, 0))
    m.bone("body", "root", (0, lh, 0))
    m.bone("head", "body", (0, yt, 0))
    m.bone("right_arm", "body", (-tw // 2 - aw // 2, yt - 1, 0))
    m.bone("left_arm", "body", (tw // 2 + aw // 2, yt - 1, 0))
    m.bone("weapon", "right_arm", (-tw // 2 - aw // 2, yt - ah, 0))
    m.bone("offhand", "left_arm", (tw // 2 + aw // 2, yt - ah, 0))
    if jambe:
        jw, jh, jd = jambe
        m.bone("right_leg", "root", (-jw // 2 - 1, lh, 0))
        m.bone("left_leg", "root", (jw // 2 + 1, lh, 0))
        ecart = 0 if s["corps"] in ("normal", "squelette", "fin", "petit") else 0
        m.cube("right_leg", (-jw - ecart, 0, -jd // 2), (jw, jh, jd), "jambes", north=bande(P["armure2"], "haut") if s.get("armure") else None)
        m.cube("left_leg", (ecart, 0, -jd // 2), (jw, jh, jd), "jambes", north=bande(P["armure2"], "haut") if s.get("armure") else None)
    elif s.get("serpent"):   # Melusai, Medusa, Syll'Esske : queue de serpent
        m.bone("tail", "root", (0, lh, 0))
        m.cube("tail", (-4, 4, -3), (8, 7, 6), "peau", north=bande(P["armure2"], "haut"))
        m.cube("tail", (-3, 1, 2), (6, 5, 8), "peau")
        m.cube("tail", (-2, 0, 9), (4, 3, 8), "peau")
        m.cube("tail", (-1, 0, 16), (2, 2, 6), "peau")
    else:   # robe spectrale flottante
        m.cube("body", (-5, 2, -3), (10, 8, 6), "tissu", north=bande(sombre(P["tissu"]), "bas", 2))
    # torse
    em = embleme(s.get("embleme", "point"), P["lueur"] if s.get("embleme_lueur") else P["armure2"])
    m.cube("body", (-tw // 2, lh, -td // 2), (tw, th, td), "torse",
           north=combine(bande(P["armure2"], "bas"), em), south=bande(P["armure2"], "bas"))
    if "ventre" in s.get("extras", ()):
        m.cube("body", (-tw // 2 + 2, lh + 1, -td // 2 - 3), (tw - 4, th - 5, 3), "peau",
               north=lambda d, x, y, w, h, px: d.ellipse((x + 2, y + 2, x + w - 3, y + h - 3), outline=sombre(P["peau"], 0.5)))
    if "tabard" in s.get("extras", ()):
        m.cube("body", (-tw // 4, max(1, lh - 8), -td // 2 - 1), (max(2, tw // 2), 10, 1), "tissu",
               north=bande(P["armure2"], "bas"))
    if "sac" in s.get("extras", ()):
        m.cube("body", (-tw // 2 + 1, lh + 3, td // 2), (tw - 2, th - 4, 4), "metal",
               south=combine(bande(P["lueur"], "haut"), em))
    if "queue" in s.get("extras", ()):
        m.bone("tail", "body", (0, lh + 1, td // 2))
        m.cube("tail", (-1, lh - 1, td // 2), (2, 2, 9), "peau")
        m.cube("tail", (-1, lh - 3, td // 2 + 8), (2, 2, 5), "peau")
    if "cape" in s.get("extras", ()):
        m.bone("cape", "body", (0, yt - 1, td // 2))
        m.cube("cape", (-tw // 2 + 1, max(2, lh - 6), td // 2), (tw - 2, th + 6 - 1, 1), "tissu",
               north=bande(P["armure2"], "bas"), south=bande(P["armure2"], "bas"))
    if "ailes" in s.get("extras", ()):
        m.bone("wings", "body", (0, yt - 3, td // 2))
        m.cube("wings", (-tw // 2 - 12, yt - 14, td // 2 + 1), (12, 16, 1), "tissu", north=bande(P["lueur"], "haut"))
        m.cube("wings", (tw // 2, yt - 14, td // 2 + 1), (12, 16, 1), "tissu", north=bande(P["lueur"], "haut"))
    # épaulières
    if s.get("epaulieres"):
        pw, ph, pd = s["epaulieres"]
        m.cube("right_arm", (-tw // 2 - pw + 1, yt - ph + 3, -pd // 2), (pw, ph, pd), "armure2b", toutes=bande(P["armure2"], "bas"))
        m.cube("left_arm", (tw // 2 - 1, yt - ph + 3, -pd // 2), (pw, ph, pd), "armure2b", toutes=bande(P["armure2"], "bas"))
    # bras
    m.cube("right_arm", (-tw // 2 - aw, yt - ah, -ad // 2), (aw, ah, ad), "bras")
    m.cube("left_arm", (tw // 2, yt - ah, -ad // 2), (aw, ah, ad), "bras")
    # tête
    t = s.get("tete", "visage")
    hx, hz = -hs // 2, -hs // 2
    visage = {
        "heaume": combine(yeux(P["lueur"], (20, 20, 26)), lambda d, x, y, w, h, px: d.line((x + w // 2, y + h // 2 + 1, x + w // 2, y + h - 1), fill=sombre(P["armure"]))),
        "visage": combine(yeux((20, 20, 20)), lambda d, x, y, w, h, px: d.line((x + 2, y + h - 3, x + w - 3, y + h - 3), fill=sombre(P["peau"], 0.5))),
        "crane": crane,
        "capuche": lambda d, x, y, w, h, px: (d.rectangle((x + 1, y + 2, x + w - 2, y + h - 1), fill=(14, 14, 18)), yeux(P["lueur"])(d, x, y, w, h, px)),
        "bete": yeux(P["lueur"]),
    }[s.get("face", "visage")]
    m.cube("head", (hx, yt, hz), (hs, hs, hs), "tete", north=visage, east=bande(P["armure2"]) if s.get("face") == "heaume" else None,
           west=bande(P["armure2"]) if s.get("face") == "heaume" else None)
    ex = s.get("extras", ())
    if "museau" in ex:
        m.cube("head", (-2, yt + 1, hz - 4), (4, 3, 4), "tete", north=dents)
    if "machoire" in ex:
        m.cube("head", (hx - 1, yt - 1, hz - 2), (hs + 2, 3, 4), "peau", north=dents)
    if "barbe" in ex:
        m.cube("head", (hx + 1, yt - 4, hz - 1), (hs - 2, 5, 2), "poils")
    if "crete" in ex:
        m.cube("head", (-1, yt + hs, hz + 1), (2, 3, hs - 1), "poils")
    if "cornes" in ex:
        m.cube("head", (hx - 2, yt + hs - 3, -1), (2, 2, 2), "corne")
        m.cube("head", (hx - 3, yt + hs - 1, -1), (2, 4, 2), "corne")
        m.cube("head", (-hx, yt + hs - 3, -1), (2, 2, 2), "corne")
        m.cube("head", (-hx + 1, yt + hs - 1, -1), (2, 4, 2), "corne")
    if "grandes_cornes" in ex:
        m.cube("head", (hx - 4, yt + hs - 2, -1), (4, 2, 2), "corne")
        m.cube("head", (hx - 5, yt + hs, -1), (2, 6, 2), "corne")
        m.cube("head", (-hx, yt + hs - 2, -1), (4, 2, 2), "corne")
        m.cube("head", (-hx + 3, yt + hs, -1), (2, 6, 2), "corne")
    if "chapeau" in ex:   # capuche pointue des Gitz
        m.cube("head", (hx - 1, yt + hs - 2, hz - 1), (hs + 2, 3, hs + 2), "tissu")
        m.cube("head", (-2, yt + hs + 1, -2), (4, 4, 4), "tissu")
        m.cube("head", (-1, yt + hs + 5, -1), (2, 3, 2), "tissu")
    if "haut_heaume" in ex:
        m.cube("head", (-1, yt + hs, hz), (2, 5, 3), "armure2b")
    if "couronne" in ex:
        for i, xx in enumerate((hx, -1, -hx - 2)):
            m.cube("head", (xx, yt + hs, hz + 2), (2, 3 + (i == 1) * 2, 2), "armure2b")
    if "branches" in ex:
        m.cube("head", (hx - 2, yt + hs - 1, -1), (2, 6, 2), "corne")
        m.cube("head", (-hx, yt + hs - 1, -1), (2, 7, 2), "corne")
        m.cube("head", (-1, yt + hs, 1), (2, 5, 2), "corne")
        m.cube("left_arm", (tw // 2 + aw, yt - 3, -1), (3, 2, 2), "corne")
    if "halo" in ex:
        m.cube("head", (-6, yt + 1, hz + hs + 1), (12, 12, 1), "halo", north=anneau(P["armure2"]), south=anneau(P["armure2"]))
    if "griffes" in ex:
        m.cube("right_arm", (-tw // 2 - aw, yt - ah - 2, -ad // 2 - 1), (aw, 2, 2), "corne")
        m.cube("left_arm", (tw // 2, yt - ah - 2, -ad // 2 - 1), (aw, 2, 2), "corne")
    # arme (verticale dans la main droite)
    hxw = -tw // 2 - aw // 2 - 1
    yh = yt - ah
    zf = -ad // 2 - 2
    arme = s.get("arme")
    if arme == "marteau":
        m.cube("weapon", (hxw, yh - 10, zf), (2, 17, 2), "manche")
        m.cube("weapon", (hxw - 2, yh + 6, zf - 2), (6, 5, 6), "metal", toutes=eclair(P["lueur"]))
    elif arme == "hache":
        m.cube("weapon", (hxw, yh - 8, zf), (2, 16, 2), "manche")
        m.cube("weapon", (hxw - 5, yh + 3, zf), (5, 6, 2), "metal")
    elif arme == "double_hache":
        m.cube("weapon", (hxw, yh - 8, zf), (2, 18, 2), "manche")
        m.cube("weapon", (hxw - 5, yh + 4, zf), (12, 6, 2), "metal")
    elif arme == "epee":
        m.cube("weapon", (hxw, yh - 2, zf), (2, 3, 2), "manche")
        m.cube("weapon", (hxw - 2, yh + 1, zf), (6, 1, 2), "metal")
        m.cube("weapon", (hxw, yh + 2, zf), (2, 15, 1), "lame")
    elif arme == "lance":
        m.cube("weapon", (hxw, yh - 12, zf), (1, 28, 1), "manche")
        m.cube("weapon", (hxw - 1, yh + 16, zf - 1), (3, 5, 3), "lame")
    elif arme == "faux":
        m.cube("weapon", (hxw, yh - 10, zf), (2, 26, 2), "manche")
        m.cube("weapon", (hxw - 10, yh + 13, zf), (10, 3, 1), "lame")
    elif arme == "couperet":
        m.cube("weapon", (hxw, yh - 2, zf), (2, 4, 2), "manche")
        m.cube("weapon", (hxw - 1, yh + 2, zf - 3), (3, 11, 6), "metal")
    elif arme == "baton":
        m.cube("weapon", (hxw, yh - 12, zf), (2, 26, 2), "manche")
        m.cube("weapon", (hxw - 1, yh + 14, zf - 1), (4, 4, 4), "lueur")
    elif arme == "fusil":
        m.cube("weapon", (hxw - 1, yh - 2, zf - 12), (3, 3, 16), "metal", north=bande(P["lueur"]))
    elif arme == "dague":
        m.cube("weapon", (hxw, yh - 1, zf), (2, 2, 2), "manche")
        m.cube("weapon", (hxw, yh + 1, zf), (1, 8, 2), "lame")
    elif arme == "massue":
        m.cube("weapon", (hxw, yh - 6, zf), (3, 12, 3), "manche")
        m.cube("weapon", (hxw - 2, yh + 5, zf - 2), (7, 8, 7), "corne")
    # main gauche
    oxw = tw // 2 + aw
    off = s.get("main_gauche")
    if off == "bouclier":
        m.cube("offhand", (oxw, yh - 4, -7), (2, 15, 14), "bouclier",
               west=combine(lambda d, x, y, w, h, px: d.rectangle((x, y, x + w - 1, y + h - 1), outline=P["armure2"]), eclair(P["lueur"]) if s.get("embleme") == "comete" else em))
    elif off == "rondache":
        m.cube("offhand", (oxw, yh - 2, -5), (2, 10, 10), "bouclier", west=em)
    elif off == "dague":
        m.cube("offhand", (oxw - aw // 2 - 1, yh - 1, zf), (1, 8, 2), "lame")
    elif off == "hache":
        m.cube("offhand", (oxw - aw // 2 - 1, yh - 8, zf), (2, 16, 2), "manche")
        m.cube("offhand", (oxw - aw // 2 + 1, yh + 3, zf), (5, 6, 2), "metal")
    elif off == "griffe":
        m.cube("offhand", (oxw - aw, yh - 3, -ad // 2 - 2), (aw, 3, 3), "corne")

    pal = {
        "jambes": P["armure"] if s.get("armure") else P["peau_bas"] if "peau_bas" in P else P["tissu"],
        "torse": P["armure"] if s.get("armure") else P["tissu"],
        "bras": P["armure"] if s.get("armure") else P["peau"],
        "tete": P["armure"] if s.get("face") == "heaume" else P["peau"] if s.get("face") in ("visage", "bete", "crane") else P["tissu"],
        "armure2b": P["armure2"], "tissu": P["tissu"], "peau": P["peau"], "metal": P["metal"],
        "manche": P.get("manche", (70, 46, 30)), "lame": P.get("lame", (200, 205, 215)), "lueur": P["lueur"],
        "poils": P.get("poils", (200, 90, 30)), "corne": P.get("corne", (220, 205, 170)),
        "bouclier": P.get("bouclier", P["armure"]), "halo": P["armure2"],
    }
    palettes = {k: {"base": v, "bord": sombre(v), "bruit": 6} for k, v in pal.items()}
    return m, palettes


def animations(m):
    os_ = {b[0] for b in m.bones}
    A = {
        "misc.idle": {"loop": True, "animation_length": 3.0, "bones": {
            "body": {"position": {"0.0": [0, 0, 0], "1.5": [0, -0.3, 0], "3.0": [0, 0, 0]}},
            "right_arm": {"rotation": {"0.0": [-6, 0, 0], "1.5": [-9, 0, 0], "3.0": [-6, 0, 0]}},
            "left_arm": {"rotation": {"0.0": [-6, 0, 0], "1.5": [-3, 0, 0], "3.0": [-6, 0, 0]}},
            "cape": {"rotation": {"0.0": [4, 0, 0], "1.5": [8, 0, 0], "3.0": [4, 0, 0]}},
            "tail": {"rotation": {"0.0": [-10, -8, 0], "1.5": [-10, 8, 0], "3.0": [-10, -8, 0]}},
            "wings": {"rotation": {"0.0": [0, 0, 0], "1.5": [6, 0, 0], "3.0": [0, 0, 0]}}}},
        "move.walk": {"loop": True, "animation_length": 1.0, "bones": {
            "right_leg": {"rotation": {"0.0": [28, 0, 0], "0.5": [-28, 0, 0], "1.0": [28, 0, 0]}},
            "left_leg": {"rotation": {"0.0": [-28, 0, 0], "0.5": [28, 0, 0], "1.0": [-28, 0, 0]}},
            "right_arm": {"rotation": {"0.0": [-20, 0, 0], "0.5": [12, 0, 0], "1.0": [-20, 0, 0]}},
            "left_arm": {"rotation": {"0.0": [12, 0, 0], "0.5": [-20, 0, 0], "1.0": [12, 0, 0]}},
            "cape": {"rotation": {"0.0": [18, 0, 0], "0.5": [24, 0, 0], "1.0": [18, 0, 0]}},
            "tail": {"rotation": {"0.0": [-5, -15, 0], "0.5": [-5, 15, 0], "1.0": [-5, -15, 0]}},
            "body": {"position": {"0.0": [0, 0, 0], "0.25": [0, 0.6, 0], "0.5": [0, 0, 0], "0.75": [0, 0.6, 0], "1.0": [0, 0, 0]}}}},
        "attack.swing": {"loop": False, "animation_length": 0.6, "bones": {
            "right_arm": {"rotation": {"0.0": [0, 0, 0], "0.2": [-160, 0, -10], "0.35": [-40, 0, 0], "0.6": [0, 0, 0]}},
            "body": {"rotation": {"0.0": [0, 0, 0], "0.2": [-6, 8, 0], "0.35": [10, -6, 0], "0.6": [0, 0, 0]}}}},
        "misc.die": {"loop": "hold_on_last_frame", "animation_length": 1.0, "bones": {
            "root": {"rotation": {"0.0": [0, 0, 0], "1.0": [-85, 0, 0]}}}},
    }
    for a in A.values():
        a["bones"] = {k: v for k, v in a["bones"].items() if k in os_}
    return A


# ---------------------------------------------------------------- palettes
def pal(armure, armure2, tissu, peau, lueur, metal=(150, 150, 160), **kw):
    d = dict(armure=armure, armure2=armure2, tissu=tissu, peau=peau, lueur=lueur, metal=metal)
    d.update(kw)
    return d


OR, BLEU, TURQ = (204, 158, 52), (40, 66, 150), (40, 150, 160)
P_SC = pal(OR, (60, 90, 170), BLEU, OR, (120, 220, 255), metal=(120, 130, 140), manche=(130, 40, 40), bouclier=BLEU)
P_CHAOS = pal((60, 60, 66), (170, 140, 60), (110, 20, 20), (200, 170, 140), (230, 60, 40), metal=(90, 90, 96))
P_KHORNE = pal((150, 30, 26), (190, 160, 70), (60, 20, 18), (190, 150, 120), (255, 80, 40), metal=(70, 60, 60))
P_NURGLE = pal((110, 120, 60), (150, 120, 60), (90, 80, 50), (150, 160, 100), (190, 230, 60), metal=(100, 90, 60))
P_SKAVEN = pal((80, 66, 50), (120, 110, 90), (70, 50, 40), (110, 90, 70), (80, 255, 60), metal=(90, 86, 80), poils=(90, 70, 55))
P_MORT = pal((120, 120, 110), (170, 150, 90), (40, 70, 70), (225, 220, 200), (90, 255, 220), metal=(110, 120, 120))
P_ORRUK = pal((90, 90, 96), (230, 200, 40), (90, 60, 40), (80, 130, 50), (255, 200, 40), metal=(110, 110, 116))
P_KB = pal((60, 70, 50), (150, 120, 70), (70, 80, 40), (90, 120, 60), (200, 255, 80), metal=(90, 96, 80))
P_GITZ = pal((40, 40, 50), (220, 210, 120), (34, 34, 46), (120, 160, 70), (230, 220, 120), metal=(100, 100, 110))

EQUIPES = {"ordre": "rm_ordre", "chaos": "rm_chaos", "mort": "rm_mort", "destruction": "rm_destruction"}


def hauteur_modele(m):
    return max(c.o[1] + c.t[1] for c in m.cubes) / 16.0


def largeur_modele(m):
    xs = [c.o[0] for c in m.cubes if c.bone in ("body", "root")] + [c.o[0] + c.t[0] for c in m.cubes if c.bone in ("body", "root")]
    return (max(xs) - min(xs)) / 16.0


def java(entrees):
    l = []
    for e in entrees:
        pv, deg, arm, vit = e["stats"]
        l.append(f'        new Profil("{e["id"]}", "{EQUIPES[e["alliance"]]}", {pv}f, {deg}f, {arm}f, {vit}f, {e["ech"]}f, '
                 f'{e["w"]:.2f}f, {e["h"]:.2f}f, Capacite.{e["cap"].upper()}, Mode.{e["mode"].upper()}, '
                 f'Special.{e["special"].upper()}, "{e["sbire"]}", {str(e["boss"]).lower()})')
    return """package fr.royaumes;

import java.util.List;

/** FICHIER GÉNÉRÉ par outils/modeles/factions.py : ne pas modifier à la main. */
public final class ProfilsGeneres {
    private ProfilsGeneres() {}

    public static final List<Profil> TOUS = List.of(
""" + ",\n".join(l) + """
    );
}
"""


def boite(m):
    xs = [c.o[0] for c in m.cubes] + [c.o[0] + c.t[0] for c in m.cubes]
    zs = [c.o[2] for c in m.cubes] + [c.o[2] + c.t[2] for c in m.cubes]
    h = max(c.o[1] + c.t[1] for c in m.cubes) / 16.0
    return h, max(max(xs) - min(xs), max(zs) - min(zs)) / 16.0


def main():
    import math
    from bestiaire import TOUS, FAC
    import creatures as C
    GAB = {"bete": C.bete, "navire": C.navire, "blob": C.blob, "poisson": C.poisson, "char": C.char}
    entrees, planche = [], []
    os.makedirs(f"{ICI}/apercus", exist_ok=True)
    for e in TOUS:
        if e["gabarit"] == "h":
            m, palettes = construire(e["id"], e["spec"])
            anims = C.animations_gen(m, e["mode"].startswith("vol") and "wings" in {b[0] for b in m.bones})
        else:
            m, palettes = GAB[e["gabarit"]](e["id"], e["spec"])
            anims = C.animations_gen(m, e["mode"].startswith("vol"))
        tex = m.exporter(palettes, anims)
        h, w = boite(m)
        if e["gabarit"] == "h":
            w = max(0.5, min(w * 0.6, 1.4))
        else:
            w = max(0.6, min(w * 0.75, 3.0 / e["ech"]))
        e["h"], e["w"] = round(h * 0.95, 2), round(w, 2)
        e["alliance"] = FAC[e["fac"]][0]
        entrees.append(e)
        sortie = f"{ICI}/apercus/{e['id']}.png"
        apercu_vues(m, tex, sortie, e["nom"])
        planche.append((e["nom"], e["alliance"], sortie, e["boss"], e["fac"]))
    open(f"{RACINE}/src/main/java/fr/royaumes/ProfilsGeneres.java", "w").write(java(entrees))
    # traductions
    for lang in ("fr_fr", "en_us"):
        p = f"{ASSETS}/lang/{lang}.json"
        d = {k: v for k, v in (json.load(open(p)) if os.path.exists(p) else {}).items() if not k.startswith("entity.royaumes.")}
        for e in entrees:
            d[f"entity.royaumes.{e['id']}"] = e["nom"]
        json.dump(d, open(p, "w"), ensure_ascii=False, indent=1)
    # apparitions : seulement les mobs du mod dans les Royaumes
    dossier = f"{RACINE}/src/main/resources/data/royaumes/worldgen/biome"
    for f in os.listdir(dossier):
        b = f[:-5]
        p = f"{dossier}/{f}"
        d = json.load(open(p))
        cat = d["attributes"]["minecraft:gameplay/natural_mob_spawns"]["argument"]["spawns_by_category"].setdefault("monster", [])
        cat[:] = [x for x in cat if not x["type"].startswith("minecraft:")]
        cat[:] = []
        for e in entrees:
            if b in e["biomes"] and e["poids"] > 0:
                n = 3 if e["stats"][0] < 40 else 1
                cat.append({"type": f"royaumes:{e['id']}", "count": {"type": "minecraft:uniform", "min_inclusive": 1, "max_inclusive": n} if n > 1 else 1,
                            "weight": e["poids"]})
        json.dump(d, open(p, "w"), indent=1)
    # butin
    for e in entrees:
        pools = []
        for item, a, bmax in e["butin"]:
            ent = {"type": "minecraft:item", "name": item, "modifier": [
                {"type": "minecraft:set_count", "count": {"type": "minecraft:uniform", "min": a, "max": bmax}},
                {"type": "minecraft:enchanted_count_increase", "enchantment": "minecraft:looting", "count": {"type": "minecraft:uniform", "min": 0.0, "max": 1.0}}]}
            pools.append({"rolls": 1, "entries": [ent]})
        res = FAC[e["fac"]][1]
        chance = 1.0 if e["boss"] or e["stats"][0] >= 150 else 0.35
        pools.append({"rolls": 1, "condition": {"type": "minecraft:all_of", "terms": [{"type": "minecraft:killed_by_player"},
                                                  {"type": "minecraft:random_chance_with_enchanted_bonus", "enchantment": "minecraft:looting",
                                                   "unenchanted_chance": chance, "enchanted_chance": {"type": "minecraft:linear", "base": min(1.0, chance + 0.1), "per_level_above_first": 0.1}}]},
                      "entries": [{"type": "minecraft:loot_table", "value": f"royaumes:debug/res/{res}"}]})
        if e["boss"]:
            pools.append({"rolls": 1, "entries": [{"type": "minecraft:loot_table", "value": f"royaumes:boss/{e['id']}"}]})
        p = f"{RACINE}/src/main/resources/data/royaumes/loot_table/entities/{e['id']}.json"
        os.makedirs(os.path.dirname(p), exist_ok=True)
        json.dump({"type": "minecraft:entity", "pools": pools}, open(p, "w"), indent=1)
    # fonctions de test
    lignes = ["# Fait apparaître tous les mobs du mod autour de toi (immobiles, pour les regarder)",
              "tellraw @s {\"text\":\"Bestiaire du mod : tous les mobs autour de toi\",\"color\":\"gold\"}"]
    n = len(entrees)
    for i, e in enumerate(entrees):
        a = 2 * math.pi * i / n
        r = 28 + 6 * (i % 3)
        lignes.append(f"summon royaumes:{e['id']} ~{r * math.cos(a):.1f} ~ ~{r * math.sin(a):.1f} {{NoAI:1b,PersistenceRequired:1b,CustomNameVisible:1b}}")
    base = f"{RACINE}/src/main/resources/data/royaumes"
    os.makedirs(f"{base}/function/debug", exist_ok=True)
    open(f"{base}/function/debug/mobs.mcfunction", "w").write("\n".join(lignes) + "\n")
    open(f"{base}/function/debug/nettoyer.mcfunction", "w").write(
        "kill @e[type=#royaumes:mobs_du_mod]\nkill @e[type=minecraft:text_display,tag=rm_debug]\n")
    for fac in FAC:
        L = [f"summon royaumes:{e['id']} ~{3 + 4 * k} ~ ~3 {{NoAI:1b,PersistenceRequired:1b,CustomNameVisible:1b}}"
             for k, e in enumerate([x for x in entrees if x["fac"] == fac])]
        os.makedirs(f"{base}/function/debug/faction", exist_ok=True)
        open(f"{base}/function/debug/faction/{fac}.mcfunction", "w").write("\n".join(L) + "\n")
    tag = f"{base}/tags/entity_type/mobs_du_mod.json"
    os.makedirs(os.path.dirname(tag), exist_ok=True)
    json.dump({"values": [f"royaumes:{e['id']}" for e in entrees]}, open(tag, "w"), indent=1)
    json.dump([{k: e[k] for k in ("id", "nom", "fac")} for e in entrees], open(f"{ICI}/liste_mobs.json", "w"), ensure_ascii=False, indent=1)
    faire_planches(planche)
    print(len(entrees), "mobs générés")


def faire_planches(planche):
    COUL = {"ordre": (230, 190, 70), "chaos": (200, 60, 60), "mort": (170, 110, 220), "destruction": (100, 190, 90)}
    fb = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf", 30)
    fs = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 14)
    for f in os.listdir(f"{ICI}/apercus"):
        if f.startswith("planche_"):
            os.remove(f"{ICI}/apercus/{f}")
    for al, titre in (("ordre", "Ordre"), ("chaos", "Chaos"), ("mort", "Mort"), ("destruction", "Destruction")):
        items = [p for p in planche if p[1] == al]
        for page in range(0, len(items), 24):
            lot = items[page:page + 24]
            cols = 6
            rows = (len(lot) + cols - 1) // cols
            W, H = cols * 260 + 20, rows * 290 + 80
            sh = Image.new("RGB", (W, H), (22, 24, 30))
            d = ImageDraw.Draw(sh)
            d.text((20, 20), f"Bestiaire — {titre} ({page // 24 + 1})", fill=(240, 220, 150), font=fb)
            for i, (nom, a, chemin, boss, fac) in enumerate(lot):
                im = Image.open(chemin)
                v = im.crop((0, 60, int((im.width - 300) * 0.62), im.height - 30))
                v.thumbnail((240, 240))
                x, y = 20 + (i % cols) * 260, 80 + (i // cols) * 290
                d.rectangle((x, y, x + 245, y + 278), outline=(255, 80, 80) if boss else COUL[a], width=2)
                sh.paste(v, (x + (245 - v.width) // 2, y + 6 + (240 - v.height)))
                d.text((x + 6, y + 256), nom[:30], fill=COUL[a], font=fs)
            sh.save(f"{ICI}/apercus/planche_{al}_{page // 24 + 1}.png")


if __name__ == "__main__":
    main()
