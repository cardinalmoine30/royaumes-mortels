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

MOBS = [
    # id, nom, alliance, corps, spec, stats(pv, degats, armure, vitesse), echelle, capacite, biomes
    ("liberator", "Liberator Stormcast", "ordre", dict(corps="massif", pal=P_SC, armure=True, face="heaume", arme="marteau", main_gauche="bouclier",
        epaulieres=(7, 6, 10), embleme="comete", extras=("cape", "halo")), (40, 6, 8, .27), 1.0, "foudre", ["azyr_cimes", "hysh_plateaux"]),
    ("judicator", "Judicator Stormcast", "ordre", dict(corps="massif", pal=P_SC, armure=True, face="heaume", arme="lance", epaulieres=(7, 6, 10),
        embleme="comete", extras=("cape", "haut_heaume")), (32, 5, 6, .27), 1.0, "foudre", ["azyr_cimes"]),
    ("lord_celestant", "Lord-Celestant", "ordre", dict(corps="massif", pal=pal((230, 190, 70), (240, 240, 250), (30, 50, 130), OR, (150, 230, 255)), armure=True,
        face="heaume", arme="epee", main_gauche="bouclier", epaulieres=(8, 7, 11), embleme="comete", extras=("cape", "halo", "haut_heaume")), (80, 10, 10, .28), 1.15, "foudre", ["azyr_cimes"]),
    ("garde_franche", "Soldat de la Garde Franche", "ordre", dict(corps="normal", pal=pal((150, 150, 160), (200, 170, 60), (40, 70, 150), (215, 175, 140), (250, 220, 120)),
        armure=False, face="visage", arme="lance", main_gauche="rondache", embleme="comete", extras=("tabard",)), (26, 5, 4, .26), 1.0, "aucune", ["azyr_cimes", "ghyran_jade"]),
    ("fyreslayer", "Vulkite Berzerker", "ordre", dict(corps="nain", pal=pal((200, 120, 60), (230, 180, 60), (120, 50, 30), (215, 150, 110), (255, 120, 30), poils=(240, 110, 30)),
        face="visage", arme="hache", main_gauche="rondache", embleme="croc", extras=("barbe", "crete")), (30, 6, 3, .28), 1.0, "feu", ["aqshy_cendres", "aqshy_volcans"]),
    ("kharadron", "Arkanaut Kharadron", "ordre", dict(corps="nain", pal=pal((60, 110, 140), (200, 170, 70), (60, 60, 70), (60, 110, 140), (120, 230, 255), metal=(160, 140, 90)),
        armure=True, face="heaume", arme="fusil", embleme="point", extras=("sac", "barbe")), (26, 5, 6, .25), 1.0, "aucune", ["chamon_desert"]),
    ("soeur_khaine", "Sœur du Massacre", "ordre", dict(corps="fin", pal=pal((60, 20, 30), (200, 170, 90), (130, 20, 40), (225, 190, 170), (255, 40, 60), poils=(20, 20, 24)),
        face="visage", arme="dague", main_gauche="dague", embleme="croc", extras=("crete",)), (22, 5, 2, .31), 1.0, "saignee", ["ghur_terres"]),
    ("idoneth", "Namarti Thrall", "ordre", dict(corps="fin", pal=pal((40, 90, 110), (220, 210, 190), (30, 60, 90), (190, 210, 220), (120, 255, 230)),
        armure=True, face="bete", arme="epee", embleme="point", extras=("cape",)), (30, 6, 3, .28), 1.0, "aucune", ["ulgu_mer"]),
    ("lumineth", "Gardien du Temple Lumineth", "ordre", dict(corps="fin", pal=pal((235, 235, 240), (210, 180, 90), (230, 230, 240), (240, 220, 200), (255, 250, 200)),
        armure=True, face="heaume", arme="lance", embleme="comete", embleme_lueur=True, extras=("haut_heaume", "cape")), (28, 5, 5, .27), 1.0, "lumiere", ["hysh_plateaux", "hysh_iles"]),
    ("saurus", "Guerrier Saurus", "ordre", dict(corps="massif", pal=pal((40, 120, 140), (210, 170, 60), (40, 120, 140), (60, 150, 110), (255, 230, 90), corne=(240, 200, 80)),
        face="bete", arme="massue", main_gauche="rondache", embleme="point", extras=("queue", "museau")), (34, 6, 4, .26), 1.1, "aucune", ["ghur_jungle"]),
    ("skink", "Skink", "ordre", dict(corps="petit", pal=pal((60, 160, 200), (230, 190, 60), (60, 160, 200), (70, 170, 210), (255, 230, 90)),
        face="bete", arme="lance", embleme="point", extras=("queue", "museau")), (16, 3, 1, .31), 1.0, "poison", ["ghur_jungle"]),
    ("dryade", "Dryade Sylvaneth", "ordre", dict(corps="fin", pal=pal((110, 80, 50), (120, 160, 60), (90, 70, 45), (120, 90, 60), (150, 255, 90), corne=(90, 70, 45)),
        face="bete", embleme="point", embleme_lueur=True, extras=("branches", "griffes"), main_gauche="griffe"), (30, 5, 4, .27), 1.0, "aucune", ["ghyran_jade", "ghyran_wyldwood", "ghyran_marais"]),
    ("guerrier_chaos", "Guerrier du Chaos", "chaos", dict(corps="massif", pal=P_CHAOS, armure=True, face="heaume", arme="hache", main_gauche="bouclier",
        epaulieres=(7, 7, 10), embleme="etoile", extras=("cornes", "cape")), (40, 7, 8, .25), 1.0, "aucune", ["chaos_desolation"]),
    ("seigneur_chaos", "Seigneur du Chaos", "chaos", dict(corps="massif", pal=pal((40, 40, 46), (200, 160, 60), (120, 10, 10), (200, 170, 140), (255, 60, 30), metal=(60, 60, 66)),
        armure=True, face="heaume", arme="epee", main_gauche="bouclier", epaulieres=(8, 8, 11), embleme="etoile", embleme_lueur=True, extras=("grandes_cornes", "cape")), (90, 11, 10, .27), 1.2, "feu", ["chaos_desolation"]),
    ("bloodreaver", "Bloodreaver de Khorne", "chaos", dict(corps="normal", pal=P_KHORNE, face="visage", arme="hache", main_gauche="hache", embleme="croc",
        extras=("cornes",)), (26, 6, 3, .29), 1.0, "saignee", ["chaos_desolation", "aqshy_cendres"]),
    ("tzaangor", "Tzaangor", "chaos", dict(corps="normal", pal=pal((50, 90, 170), (220, 180, 60), (50, 120, 180), (90, 130, 200), (120, 230, 255), corne=(240, 220, 150)),
        face="bete", arme="lance", main_gauche="rondache", embleme="etoile", extras=("museau", "grandes_cornes")), (24, 5, 3, .28), 1.0, "feu_magique", ["chaos_desolation", "ulgu_brumes"]),
    ("demonette", "Démonette de Slaanesh", "chaos", dict(corps="fin", pal=pal((200, 150, 200), (220, 210, 230), (170, 90, 170), (220, 180, 220), (255, 120, 220), poils=(240, 230, 250)),
        face="visage", embleme="point", extras=("griffes", "cornes", "crete"), main_gauche="griffe"), (20, 5, 1, .33), 1.0, "aucune", ["chaos_desolation"]),
    ("pestigor", "Porte-Peste de Nurgle", "chaos", dict(corps="geant", pal=P_NURGLE, face="crane", arme="epee", embleme="crane", extras=("ventre", "cornes")),
        (40, 5, 4, .19), 0.85, "poison", ["ghyran_marais", "chaos_desolation"]),
    ("clanrat", "Guerrier des Clans Skaven", "chaos", dict(corps="petit", pal=P_SKAVEN, face="bete", arme="epee", main_gauche="rondache", embleme="point",
        embleme_lueur=True, extras=("museau", "queue")), (16, 4, 2, .31), 1.0, "poison", ["terres_rongees"]),
    ("jezzail", "Tireur de Jezzail Skaven", "chaos", dict(corps="petit", pal=P_SKAVEN, face="bete", arme="fusil", embleme="point", embleme_lueur=True,
        extras=("museau", "queue", "sac")), (18, 4, 2, .3), 1.0, "poison", ["terres_rongees"]),
    ("hashut", "Garde Infernale de Hashut", "chaos", dict(corps="nain", pal=pal((40, 40, 44), (190, 140, 60), (90, 30, 20), (90, 90, 96), (255, 110, 30), poils=(30, 30, 34)),
        armure=True, face="heaume", arme="hache", main_gauche="bouclier", embleme="etoile", embleme_lueur=True, extras=("barbe", "haut_heaume")), (32, 6, 6, .25), 1.0, "feu", ["aqshy_volcans", "chaos_desolation"]),
    ("chainrasp", "Chainrasp Nighthaunt", "mort", dict(corps="spectre", pal=pal((60, 140, 130), (140, 200, 190), (70, 150, 140), (110, 200, 190), (160, 255, 230)),
        face="capuche", arme="epee", embleme="crane", embleme_lueur=True), (20, 5, 0, .28), 1.0, "drain", ["shyish_terres", "ulgu_brumes"]),
    ("glaivewraith", "Glaivewraith Nighthaunt", "mort", dict(corps="spectre", pal=pal((50, 110, 120), (170, 220, 210), (40, 100, 110), (100, 190, 190), (160, 255, 230)),
        face="capuche", arme="faux", embleme="crane", embleme_lueur=True), (24, 6, 0, .28), 1.0, "drain", ["shyish_terres"]),
    ("deathrattle", "Squelette Deathrattle", "mort", dict(corps="squelette", pal=pal((210, 205, 185), (160, 120, 60), (80, 40, 40), (215, 210, 190), (90, 255, 200)),
        face="crane", arme="epee", main_gauche="rondache", embleme="crane"), (22, 5, 3, .26), 1.0, "aucune", ["shyish_terres", "chamon_desert"]),
    ("vampire", "Seigneur Vampire", "mort", dict(corps="normal", pal=pal((40, 40, 50), (180, 30, 40), (100, 10, 20), (230, 225, 230), (255, 40, 50)),
        armure=True, face="visage", arme="epee", embleme="crane", extras=("cape", "couronne")), (70, 9, 6, .3), 1.05, "drain", ["shyish_terres", "ulgu_brumes"]),
    ("mortek", "Garde Mortek Ossiarch", "mort", dict(corps="massif", pal=pal((225, 215, 190), (60, 50, 80), (60, 50, 80), (230, 220, 200), (120, 230, 255)),
        armure=True, face="crane", arme="lance", main_gauche="bouclier", epaulieres=(6, 5, 9), embleme="crane", embleme_lueur=True), (36, 6, 6, .25), 1.0, "drain", ["shyish_terres"]),
    ("goule", "Goule des Cryptes", "mort", dict(corps="fin", pal=pal((150, 150, 140), (120, 60, 50), (90, 70, 60), (170, 170, 160), (220, 60, 60)),
        face="bete", embleme="point", extras=("griffes",), main_gauche="griffe"), (22, 5, 1, .32), 1.0, "saignee", ["shyish_terres", "ulgu_marais_lune"]),
    ("brute", "Brute Ironjawz", "destruction", dict(corps="massif", pal=P_ORRUK, armure=True, face="bete", arme="couperet", embleme="croc",
        epaulieres=(7, 6, 9), extras=("machoire",)), (45, 8, 7, .25), 1.15, "waaagh", ["ghur_terres", "ghur_jungle"]),
    ("megaboss", "Mégaboss Ironjawz", "destruction", dict(corps="massif", pal=pal((80, 80, 86), (240, 200, 30), (120, 40, 30), (70, 120, 45), (255, 200, 40)),
        armure=True, face="bete", arme="couperet", main_gauche="hache", epaulieres=(9, 8, 11), embleme="croc", extras=("machoire", "cornes")), (100, 12, 10, .25), 1.35, "waaagh", ["ghur_terres"]),
    ("gutrippa", "Gutrippa Kruleboyz", "destruction", dict(corps="normal", pal=P_KB, face="bete", arme="epee", main_gauche="rondache", embleme="croc",
        extras=("machoire",)), (28, 5, 4, .27), 1.1, "poison", ["ulgu_marais_lune", "ghyran_marais"]),
    ("grot", "Grot de la Mauvaise Lune", "destruction", dict(corps="petit", pal=P_GITZ, face="bete", arme="lance", embleme="point", extras=("chapeau",)),
        (10, 3, 0, .3), 1.0, "aucune", ["ulgu_marais_lune", "ulgu_brumes"]),
    ("gutbuster", "Ogor Gutbuster", "destruction", dict(corps="geant", pal=pal((120, 100, 80), (200, 160, 60), (110, 60, 40), (205, 170, 140), (255, 200, 60)),
        face="visage", arme="massue", embleme="croc", extras=("ventre",)), (60, 9, 4, .21), 1.35, "waaagh", ["ghur_terres"]),
    ("gargant", "Gargant Mangeur d'Hommes", "destruction", dict(corps="geant", pal=pal((120, 90, 60), (160, 120, 70), (110, 80, 50), (200, 160, 130), (255, 200, 60)),
        face="visage", arme="massue", embleme="point", extras=("ventre", "barbe")), (160, 14, 4, .22), 2.6, "seisme", ["ghur_terres", "ghur_jungle"]),
]

BOSS = [
    ("nagash", "Nagash, Dieu de la Mort", "mort", dict(corps="squelette", pal=pal((40, 50, 60), (220, 190, 80), (30, 30, 40), (220, 215, 195), (90, 255, 220)),
        armure=True, face="crane", arme="baton", embleme="crane", embleme_lueur=True, extras=("ailes", "couronne", "cape")), (900, 16, 14, .26), 3.0, "drain", []),
    ("archaon", "Archaon l'Élu Éternel", "chaos", dict(corps="massif", pal=pal((30, 30, 36), (210, 170, 60), (110, 10, 10), (190, 160, 130), (255, 60, 30), metal=(50, 50, 56)),
        armure=True, face="heaume", arme="epee", main_gauche="bouclier", epaulieres=(9, 9, 12), embleme="etoile", embleme_lueur=True, extras=("grandes_cornes", "cape", "couronne")), (1000, 18, 16, .27), 1.9, "feu", []),
    ("gordrakk", "Gordrakk, le Poing de Gork", "destruction", dict(corps="massif", pal=pal((90, 90, 96), (240, 200, 30), (130, 30, 20), (70, 125, 45), (255, 210, 40)),
        armure=True, face="bete", arme="couperet", main_gauche="hache", epaulieres=(10, 9, 12), embleme="croc", extras=("machoire", "cornes", "cape")), (800, 17, 12, .28), 1.9, "waaagh", []),
    ("skarbrand", "Skarbrand l'Exilé", "chaos", dict(corps="geant", pal=pal((150, 30, 26), (60, 50, 40), (100, 20, 15), (170, 40, 30), (255, 90, 30), corne=(60, 50, 40)),
        face="bete", arme="double_hache", main_gauche="hache", embleme="croc", embleme_lueur=True, extras=("grandes_cornes", "ailes")), (850, 18, 8, .27), 2.2, "feu", []),
    ("thanquol", "Thanquol, Prophète Gris", "chaos", dict(corps="petit", pal=pal((90, 90, 96), (120, 110, 90), (110, 110, 116), (140, 140, 140), (80, 255, 60), poils=(150, 150, 150)),
        face="bete", arme="baton", embleme="point", embleme_lueur=True, extras=("museau", "queue", "grandes_cornes", "cape")), (750, 14, 8, .3), 2.4, "foudre_verte", []),
    ("rotigus", "Rotigus le Pluviomancien", "chaos", dict(corps="geant", pal=pal((100, 120, 60), (140, 110, 60), (80, 90, 50), (130, 150, 80), (190, 230, 60), corne=(170, 160, 110)),
        face="crane", arme="baton", embleme="crane", embleme_lueur=True, extras=("ventre", "grandes_cornes")), (950, 15, 10, .2), 2.2, "poison", []),
]

EQUIPES = {"ordre": "rm_ordre", "chaos": "rm_chaos", "mort": "rm_mort", "destruction": "rm_destruction"}


def hauteur_modele(m):
    return max(c.o[1] + c.t[1] for c in m.cubes) / 16.0


def largeur_modele(m):
    xs = [c.o[0] for c in m.cubes if c.bone in ("body", "root")] + [c.o[0] + c.t[0] for c in m.cubes if c.bone in ("body", "root")]
    return (max(xs) - min(xs)) / 16.0


def java(entrees):
    l = []
    for mid, nom, al, spec, (pv, deg, arm, vit), ech, cap, biomes, boss, h, w in entrees:
        l.append(f'        new Profil("{mid}", "{EQUIPES[al]}", {pv}f, {deg}f, {arm}f, {vit}f, {ech}f, {w:.2f}f, {h:.2f}f, Capacite.{cap.upper()}, {str(boss).lower()})')
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


def main():
    entrees = []
    planche = []
    os.makedirs(f"{ICI}/apercus", exist_ok=True)
    for groupe, boss in ((MOBS, False), (BOSS, True)):
        for mid, nom, al, spec, stats, ech, cap, biomes in groupe:
            m, palettes = construire(mid, spec)
            tex = m.exporter(palettes, animations(m))
            h, w = hauteur_modele(m), max(0.5, min(largeur_modele(m), 1.4))
            entrees.append((mid, nom, al, spec, stats, ech, cap, biomes, boss, round(h * 0.95, 2), round(w * 0.8, 2)))
            sortie = f"{ICI}/apercus/{mid}.png"
            apercu_vues(m, tex, sortie, nom)
            planche.append((nom, al, sortie, boss))
    # Java
    open(f"{RACINE}/src/main/java/fr/royaumes/ProfilsGeneres.java", "w").write(java(entrees))
    # traductions
    for lang in ("fr_fr", "en_us"):
        p = f"{ASSETS}/lang/{lang}.json"
        d = json.load(open(p)) if os.path.exists(p) else {}
        for e in entrees:
            d[f"entity.royaumes.{e[0]}"] = e[1]
        json.dump(d, open(p, "w"), ensure_ascii=False, indent=1)
    # apparitions dans les biomes
    dossier = f"{RACINE}/src/main/resources/data/royaumes/worldgen/biome"
    for f in os.listdir(dossier):
        b = f[:-5]
        p = f"{dossier}/{f}"
        d = json.load(open(p))
        cat = d["attributes"]["minecraft:gameplay/natural_mob_spawns"]["argument"]["spawns_by_category"].setdefault("monster", [])
        cat[:] = [x for x in cat if not x["type"].startswith("royaumes:")]
        for e in entrees:
            if b in e[7]:
                cat.append({"type": f"royaumes:{e[0]}", "count": {"type": "minecraft:uniform", "min_inclusive": 1, "max_inclusive": 3 if e[4][0] < 60 else 1},
                            "weight": 40 if e[4][0] < 60 else 8})
        json.dump(d, open(p, "w"), indent=1)
    # fonction de test : tous les mobs en cercle autour du joueur
    lignes = ["# Fait apparaître tous les mobs du mod autour de toi (sans IA, pour les regarder)", "tellraw @s {\"text\":\"Bestiaire du mod : tous les mobs autour de toi\",\"color\":\"gold\"}"]
    import math
    n = len(entrees)
    for i, e in enumerate(entrees):
        a = 2 * math.pi * i / n
        r = 14
        lignes.append(f"summon royaumes:{e[0]} ~{r * math.cos(a):.1f} ~ ~{r * math.sin(a):.1f} {{NoAI:1b,PersistenceRequired:1b,CustomNameVisible:1b}}")
    p = f"{RACINE}/src/main/resources/data/royaumes/function/debug/mobs.mcfunction"
    os.makedirs(os.path.dirname(p), exist_ok=True)
    open(p, "w").write("\n".join(lignes) + "\n")
    open(f"{RACINE}/src/main/resources/data/royaumes/function/debug/nettoyer.mcfunction", "w").write(
        "kill @e[type=#royaumes:mobs_du_mod]\nkill @e[type=minecraft:text_display,tag=rm_debug]\n")
    tag = f"{RACINE}/src/main/resources/data/royaumes/tags/entity_type/mobs_du_mod.json"
    os.makedirs(os.path.dirname(tag), exist_ok=True)
    json.dump({"values": [f"royaumes:{e[0]}" for e in entrees]}, open(tag, "w"), indent=1)
    # planches d'aperçu
    faire_planches(planche)
    print(len(entrees), "mobs générés")


def faire_planches(planche):
    COUL = {"ordre": (230, 190, 70), "chaos": (200, 60, 60), "mort": (170, 110, 220), "destruction": (100, 190, 90)}
    fb = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf", 30)
    fs = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 15)
    groupes = [("Ordre", [p for p in planche if p[1] == "ordre" and not p[3]]),
               ("Chaos", [p for p in planche if p[1] == "chaos" and not p[3]]),
               ("Mort & Destruction", [p for p in planche if p[1] in ("mort", "destruction") and not p[3]]),
               ("Boss", [p for p in planche if p[3]])]
    for titre, items in groupes:
        vignettes = []
        for nom, al, chemin, boss in items:
            im = Image.open(chemin)
            # garde seulement les 2 premières vues (face + profil)
            w = im.width - 300
            v = im.crop((0, 60, int(w * 0.62), im.height - 30))
            v.thumbnail((300, 300))
            vignettes.append((nom, al, v))
        cols = 4
        rows = (len(vignettes) + cols - 1) // cols
        W, H = cols * 320 + 20, rows * 350 + 80
        sh = Image.new("RGB", (W, H), (22, 24, 30))
        d = ImageDraw.Draw(sh)
        d.text((20, 20), f"Mobs du mod — {titre}", fill=(240, 220, 150), font=fb)
        for i, (nom, al, v) in enumerate(vignettes):
            x, y = 20 + (i % cols) * 320, 80 + (i // cols) * 350
            d.rectangle((x, y, x + 300, y + 335), outline=COUL[al], width=2)
            sh.paste(v, (x + (300 - v.width) // 2, y + 8 + (300 - v.height)))
            d.text((x + 8, y + 312), nom[:34], fill=COUL[al], font=fs)
        sh.save(f"{ICI}/apercus/planche_{titre.split()[0].lower()}.png")


if __name__ == "__main__":
    main()
