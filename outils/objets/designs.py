# -*- coding: utf-8 -*-
"""Un dessin unique pour chaque objet nommé du datapack, et ménage des doublons.

1. Doublons retirés : œufs de zombie « Œuf : … » (le mod a ses vrais œufs), trophées de boss du datapack (le mod lâche déjà
   la relique unique de chaque seigneur), armes de départ dont le nom recopiait une arme de l'arsenal (renommées).
2. Chaque objet nommé (armes de départ, sceaux, élixirs, matériaux, Pierre de Royaume, Corne d'appel…) reçoit le composant
   minecraft:item_model "royaumes:dp/<nom>" et une icône dessinée pour lui : plus de « hache en fer nommée ».
À relancer après toute reconstruction du datapack (idempotent).  python3 outils/objets/designs.py"""
import glob
import json
import os
import random
import re
import sys
import unicodedata

ICI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ICI)
from objets import T, mix, mul, ecrire  # noqa: E402
import arsenal as A  # noqa: E402

RES = os.path.join(ICI, "..", "..", "src", "main", "resources")
DATA = os.path.join(RES, "data", "royaumes")
ASSETS = os.path.join(RES, "assets", "royaumes")

TROPHEES = {"Alakanash, Bâton de Nagash", "Couronne de Nagash", "Tueuse de Rois", "Smasha", "Kunnin'", "Massacre",
            "Bâton de Malefoudre", "Bâton de Pluie Pestilentielle", "Cloche de Pluie"}
RENOMMES = {"Hache Runique d'Ur-Or": "Hachette de Forge-Novice", "Couperet de Boucher": "Couteau de Boucher",
            "Lame Vampirique": "Dague du Sang Neuf", "Lame du Meurtre": "Dague de l'Initiée", "Gros Choppa": "Choppa Rouillé",
            "Arc de Lumière": "Arc de Novice Vanari"}
COULEURS_MC = {"black": (30, 30, 30), "dark_blue": (40, 40, 170), "dark_green": (40, 140, 40), "dark_aqua": (40, 150, 150),
               "dark_red": (170, 30, 30), "dark_purple": (150, 50, 170), "gold": (240, 170, 30), "gray": (170, 170, 170),
               "dark_gray": (85, 85, 85), "blue": (85, 85, 255), "green": (85, 230, 85), "aqua": (85, 230, 230), "red": (240, 85, 85),
               "light_purple": (240, 110, 240), "yellow": (250, 240, 90), "white": (235, 235, 235)}


def slug(nom):
    nom = nom.replace("œ", "oe").replace("Œ", "Oe").replace("æ", "ae")
    s = unicodedata.normalize("NFKD", nom).encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z0-9]+", "_", s).strip("_")


def lire(p):
    return json.load(open(p, encoding="utf-8"))


def mods(e):
    m = e.get("modifier", e.get("functions", []))
    return [m] if isinstance(m, dict) else list(m)


def composants(e):
    for m in mods(e):
        if m.get("type", m.get("function")) == "minecraft:set_components":
            return m.setdefault("components", {})
    return None


# ------------------------------------------------------------------ dessins
def categorie(nom, base):
    n = nom.lower()
    b = base.split(":")[-1]
    regles = [("arc", lambda: b == "bow" or n.startswith("arc ")), ("fusil", lambda: b == "crossbow" or "fusil" in n or "arquebuse" in n),
              ("bouclier", lambda: b == "shield" or "bouclier" in n or "pavois" in n), ("lance", lambda: b == "trident" or "lance" in n),
              ("marteau", lambda: b == "mace" or "marteau" in n or "tronc d" in n or "gourdin" in n), ("faux", lambda: "faux" in n),
              ("pioche", lambda: b.endswith("pickaxe") or n.startswith("pic ")), ("griffes", lambda: "griffe" in n),
              ("hache", lambda: b.endswith("_axe") or "hache" in n or "choppa" in n or "couperet" in n),
              ("baton", lambda: b == "blaze_rod" or n.startswith("bâton")),
              ("epee", lambda: b.endswith("_sword") or any(k in n for k in ("lame", "épée", "dague", "coupe", "couteau"))),
              ("bombe", lambda: b == "tnt" or "globe" in n), ("bol", lambda: b == "mushroom_stew" or "bouillon" in n),
              ("parchemin", lambda: "parchemin" in n), ("corne", lambda: "corne" in n), ("crane", lambda: "crâne" in n),
              ("cloche", lambda: "cloche" in n), ("calice", lambda: "calice" in n), ("totem", lambda: "totem" in n),
              ("sceau", lambda: "sceau" in n), ("coeur", lambda: "cœur" in n), ("oeil", lambda: "œil" in n),
              ("fiole", lambda: any(k in n for k in ("élixir", "tonique", "brume", "lumière"))),
              ("amulette", lambda: any(k in n for k in ("talisman", "amulette", "pendentif"))), ("viande", lambda: "festin" in n),
              ("comete", lambda: "comète" in n), ("lingot", lambda: "lingot" in n), ("ferraille", lambda: "ferraille" in n),
              ("eclat", lambda: "éclat" in n), ("gemme", lambda: True)]
    for c, f in regles:
        if f():
            return c
    return "gemme"


def disque(t, cx, cy, r, c1, c2=None):
    for y in range(16):
        for x in range(16):
            d = ((x - cx) ** 2 + (y - cy) ** 2) ** 0.5
            if d <= r:
                t.p(x, y, mix(c2, c1, d / max(r, 0.1)) if c2 else c1)


def rect(t, x0, y0, x1, y1, c):
    for y in range(y0, y1 + 1):
        for x in range(x0, x1 + 1):
            t.p(x, y, c)


METAUX_MOTS = [("os", (226, 220, 198)), ("malepierre", (120, 230, 80)), ("sang", (190, 40, 40)), ("fléau", (70, 62, 78)),
               ("noir", (70, 62, 78)), ("hysh", (250, 245, 210)), ("lumière", (250, 245, 210)), ("pestilent", (150, 165, 60)),
               ("empoison", (110, 185, 70)), ("extatique", (225, 150, 235)), ("rouill", (160, 100, 60)), ("ur-or", (245, 190, 70)),
               ("forge", (245, 190, 70)), ("akhelian", (120, 220, 230)), ("esprit", (170, 230, 220)), ("saurus", (110, 160, 210)),
               ("tonnerre", (180, 210, 255)), ("tronc d", (120, 84, 50)), ("goule", (150, 140, 120)), ("dryade", (120, 170, 80))]


def metal(nom):
    n = nom.lower()
    for k, c in METAUX_MOTS:
        if k in n:
            return c
    return (200, 205, 215)


def arme(cat, nom, c1, c2, R):
    """Armes de départ : silhouette paramétrée par l'objet (longueur, largeur, garde, dents, courbure, tête)."""
    t = T()
    m = metal(nom)
    ms = mul(m, 0.7)
    manche, manche_s = (112, 78, 48), (70, 48, 30)
    n = nom.lower()
    if cat == "epee":
        court = any(k in n for k in ("dague", "couteau", "coupe-gorge"))
        L = 6 if court else R.randint(8, 10)
        large = 2 if any(k in n for k in ("épée", "fléau", "os", "hammerhal")) else 1
        dents = any(k in n for k in ("coupe", "malepierre", "goule"))
        courbe = "extatique" in n or "tronche" in n
        x0, y0 = 4, 11
        for i in range(L):
            dx = 1 if courbe and i > L // 2 else 0
            x, y = x0 + 1 + i, y0 - 1 - i - dx
            t.p(x, y, m)
            if large == 2:
                t.p(x + 1, y, ms)
            if dents and i % 2:
                t.p(x - 1, y - 1, ms)
        t.p(x0 + L + 1, y0 - L - 1, mix(m, (255, 255, 255), 0.5))
        g = R.randint(2, 3)
        for k in range(-g, g + 1):  # garde
            t.p(x0 + k, y0 + k, c2)
        t.p(x0 - 1, y0 + 1, manche)
        t.p(x0 - 2, y0 + 2, manche_s)
        t.p(x0 - 3, y0 + 3, c1)  # pommeau
        t.p(x0 - 4, y0 + 4, c1)
    elif cat == "hache":
        for i in range(11):
            t.p(2 + i, 14 - i, manche if i % 3 else manche_s)
        double = any(k in n for k in ("choppa", "sanglante", "pestilent"))
        haut = R.randint(5, 7)
        for y in range(1, 1 + haut):
            for x in range(9, 15):
                if (x - 10) ** 2 / 20 + (y - (1 + haut / 2)) ** 2 / (haut * haut / 4) <= 1:
                    t.p(x, y, m if x > 11 else ms)
        if double:
            for y in range(2, 6):
                for x in range(5, 9):
                    if (x - 8) ** 2 / 9 + (y - 3.5) ** 2 / 4 <= 1:
                        t.p(x, y, ms)
        t.p(10, 1 + haut // 2, c2)
        t.p(3, 13, c1)
    elif cat == "marteau":
        for i in range(10):
            t.p(2 + i, 14 - i, manche if i % 2 else manche_s)
        bois = "tronc d" in n
        rond = any(k in n for k in ("gourdin", "tronc d"))
        for y in range(0, 8):
            for x in range(8, 16):
                d = ((x - 11.5) ** 2 + (y - 3.5) ** 2) ** 0.5 if rond else max(abs(x - 11.5), abs(y - 3.5) * 1.3)
                if d <= 3.6:
                    t.p(x, y, (m if (x + y) % 3 else ms) if not bois else ((120, 84, 50) if (x * y) % 4 else (90, 130, 50)))
        t.p(11, 3, c2)
        t.p(3, 13, c1)
    elif cat == "lance":
        for i in range(12):
            t.p(1 + i, 14 - i, manche)
        for k in range(4):
            t.p(12 + k // 2, 3 - k, m)
            t.p(13 + k // 2, 3 - k, ms)
        if "akhelian" in n:  # trident
            t.p(11, 1, m)
            t.p(15, 5, m)
        t.p(10, 5, c2)
        t.p(9, 6, c1)
    elif cat == "faux":
        for i in range(12):
            t.p(2 + i, 14 - i, manche)
        for k in range(9):
            t.p(13 - k, 2 + int(0.12 * k * k), m)
            t.p(13 - k, 3 + int(0.12 * k * k), ms)
        t.p(12, 3, c2)
    else:  # bâton
        for i in range(11):
            t.p(2 + i, 14 - i, manche)
        disque(t, 12.5, 3.5, 2.4, c1, mix(c1, (255, 255, 255), 0.6))
        t.p(12, 3, c2)
    t.contour()
    return t.im


def dessin(cat, c1, c2, graine, nom=""):
    """Icône 16×16 : forme selon la catégorie, couleurs de l'objet, détails tirés de son nom (donc uniques)."""
    R = random.Random(graine)
    clair, sombre = mix(c1, (255, 255, 255), 0.45), mul(c1, 0.55)
    t = T()
    if cat in ("epee", "hache", "marteau", "lance", "faux", "baton"):
        return arme(cat, nom, c1, c2, R)
    if cat == "pioche":
        A.METAUX_ALLIANCE["_dp"] = [c1] * 5
        A.MANCHES_ALLIANCE["_dp"] = ((110, 76, 46), (70, 46, 28))
        A.ACCENTS_ALLIANCE["_dp"] = (c2, clair, c2)
        A.MOTIFS_ALLIANCE["_dp"] = A.MOTIFS_ALLIANCE["chaos" if R.random() < 0.5 else "destruction"]
        return A.icone_outil("pioche", "_dp", 1)
    if cat == "arc":
        for k in range(12):  # branche courbe
            x = 4 + int(3 * ((k - 6) / 6.0) ** 2 * 1.5)
            t.p(x, 2 + k, c1)
            t.p(x + 1, 2 + k, sombre)
        for y in range(2, 14):
            t.p(10, y, (230, 230, 220))
        t.p(5, 7, c2)
        t.p(5, 8, c2)
    elif cat == "fusil":
        rect(t, 2, 6, 13, 7, sombre)
        rect(t, 3, 5, 12, 5, c1)
        rect(t, 2, 8, 5, 12, (110, 76, 46))
        rect(t, 12, 4, 13, 8, c2)
        t.p(8, 8, (40, 40, 40))
        t.p(R.randint(6, 10), 5, clair)
    elif cat == "bouclier":
        if "os" in nom.lower().split() or "pavois" in nom.lower():
            c1, c2 = (220, 214, 190), (140, 130, 110)
        for y in range(2, 15):
            for x in range(3, 13):
                if y < 10 or abs(x - 7.5) < (15 - y) * 0.9:
                    t.p(x, y, c1)
        for y in range(3, 13):
            t.p(7, y, c2)
            t.p(8, y, c2)
        disque(t, 7.5, 7, 1.6, c2, clair)
    elif cat == "griffes":
        for k in range(3):
            for i in range(9):
                t.p(4 + k * 3 + i // 4, 3 + i, c1 if i < 7 else sombre)
        rect(t, 3, 12, 12, 13, c2)
    elif cat == "bombe":
        disque(t, 7.5, 9, 5.2, c1, clair)
        rect(t, 7, 2, 8, 4, (110, 76, 46))
        t.p(9, 1, (255, 200, 60))
        t.p(6, 7, c2)
    elif cat == "bol":
        for y in range(8, 14):
            for x in range(2, 14):
                if (x - 7.5) ** 2 / 36 + (y - 8) ** 2 / 30 <= 1:
                    t.p(x, y, (120, 84, 50))
        rect(t, 3, 7, 12, 8, c1)
        t.p(5, 7, c2)
        t.p(9, 7, clair)
    elif cat == "parchemin":
        rect(t, 3, 3, 12, 12, (232, 216, 170))
        rect(t, 2, 2, 13, 3, (190, 160, 110))
        rect(t, 2, 12, 13, 13, (190, 160, 110))
        for y in (5, 7, 9):
            rect(t, 4, y, 4 + R.randint(5, 7), y, mul(c1, 0.8))
        disque(t, 10, 10, 1.4, c2)
    elif cat == "corne":
        for k in range(11):
            x, y = 2 + k, 11 - int(4 * (k / 10.0) ** 1.6)
            for w in range(1 + k // 4):
                t.p(x, y - w, mix((230, 220, 190), c1, k / 10.0))
        rect(t, 12, 4, 13, 8, c2)
    elif cat in ("crane", "sceau", "totem", "cloche", "calice"):
        if cat == "crane":
            disque(t, 7.5, 6.5, 5, (225, 220, 200), (255, 255, 240))
            rect(t, 5, 10, 10, 13, (210, 205, 185))
            rect(t, 5, 6, 6, 7, (20, 20, 20))
            rect(t, 9, 6, 10, 7, (20, 20, 20))
            t.p(R.choice((4, 11)), 2, c1)
        elif cat == "sceau":
            disque(t, 7.5, 7.5, 6.2, sombre, c1)
            for k in range(R.randint(3, 6)):  # rune gravée, propre au seigneur
                t.p(R.randint(4, 11), R.randint(4, 11), clair)
            disque(t, 7.5, 7.5, 3.0, c2, clair)
        elif cat == "totem":
            rect(t, 6, 2, 9, 14, (120, 84, 50))
            rect(t, 4, 3, 11, 5, c1)
            rect(t, 6, 8, 9, 9, c2)
            t.p(7, 4, (255, 255, 255))
        elif cat == "cloche":
            for y in range(3, 12):
                for x in range(2, 14):
                    if abs(x - 7.5) < 2 + (y - 3) * 0.6:
                        t.p(x, y, c1 if y < 11 else sombre)
            disque(t, 7.5, 12.5, 1.2, c2)
            rect(t, 7, 1, 8, 2, sombre)
        else:
            for y in range(2, 8):
                for x in range(3, 13):
                    if abs(x - 7.5) < 5 - (y - 2) * 0.5:
                        t.p(x, y, c1)
            rect(t, 7, 8, 8, 11, sombre)
            rect(t, 5, 12, 10, 13, c1)
            rect(t, 4, 2, 11, 2, c2)
    elif cat == "fiole":
        disque(t, 7.5, 10, 4.5, c1, clair)
        rect(t, 6, 2, 9, 5, (200, 220, 230))
        rect(t, 6, 1, 9, 1, (120, 84, 50))
        t.p(6, 9, (255, 255, 255))
        t.p(R.randint(8, 10), 11, c2)
    elif cat == "amulette":
        for k in range(10):
            t.p(3 + k, 2 + abs(k - 5) // 2, (200, 170, 80))
        disque(t, 7.5, 10, 3.8, c1, clair)
        disque(t, 7.5, 10, 1.5, c2)
    elif cat == "coeur":
        for y in range(16):
            for x in range(16):
                u, v = (x - 7.5) / 6, (y - 7) / 6
                if (u * u + v * v - 0.6) ** 3 - u * u * v ** 3 * 1.2 <= 0:
                    t.p(x, y, mix(c1, clair, (x + y) / 30))
        t.p(5, 5, (255, 255, 255))
    elif cat == "oeil":
        for y in range(16):
            for x in range(16):
                if ((x - 7.5) / 6.5) ** 2 + ((y - 7.5) / 4) ** 2 <= 1:
                    t.p(x, y, (235, 225, 210))
        disque(t, 7.5, 7.5, 3.2, c1, clair)
        disque(t, 7.5, 7.5, 1.2, (10, 10, 10))
    elif cat == "viande":
        disque(t, 8, 7, 5, (170, 70, 50), (210, 110, 80))
        rect(t, 2, 11, 6, 12, (235, 230, 215))
        disque(t, 9, 6, 1.5, c2)
    elif cat == "comete":
        disque(t, 10, 5, 3.2, (255, 255, 255), c1)
        for k in range(8):
            t.p(9 - k, 6 + k, mix(c1, c2, k / 8.0))
            t.p(8 - k, 6 + k, mul(c1, 0.7))
    elif cat == "lingot":
        for y in range(5, 12):
            for x in range(2, 14):
                if x >= 2 + (11 - y) // 2 and x <= 13 - (11 - y) // 2:
                    t.p(x, y, c1 if y > 6 else clair)
        t.p(R.randint(5, 10), 9, c2)
    elif cat == "ferraille":
        for _ in range(9):
            x, y = R.randint(2, 11), R.randint(3, 11)
            rect(t, x, y, x + R.randint(1, 3), y + R.randint(0, 2), R.choice((c1, sombre, (150, 110, 80))))
    else:  # gemme / éclat / pierre
        pts = [(7, 1), (12, 5), (11, 12), (4, 13), (3, 6)]
        for y in range(16):
            for x in range(16):
                dedans = True
                for i in range(len(pts)):
                    (x1, y1), (x2, y2) = pts[i], pts[(i + 1) % len(pts)]
                    if (x2 - x1) * (y - y1) - (y2 - y1) * (x - x1) < 0:
                        dedans = False
                if dedans:
                    t.p(x, y, mix(clair, c1, (x + y) / 26))
        t.p(6, 4, (255, 255, 255))
        t.p(R.randint(6, 9), R.randint(8, 11), c2)
    t.contour()
    return t.im


# ------------------------------------------------------------------ passes sur le datapack
def couleurs_faction():
    return {fid: A.COUL[fid] for fid in A.COUL if not fid.startswith("_")}


def principal():
    coul_f = couleurs_faction()
    vus = {}
    retires = renommes = 0
    for p in glob.glob(os.path.join(DATA, "loot_table", "**", "*.json"), recursive=True):
        rel = os.path.relpath(p, os.path.join(DATA, "loot_table"))
        if re.match(r"debug[/\\]oeufs_\d+\.json", rel):
            os.remove(p)
            retires += 1
            continue
        j = lire(p)
        faction = os.path.basename(p)[:-5] if rel.startswith("kits") else None
        change = False
        for pool in j.get("pools", []):
            garde = []
            for e in pool.get("entries", []):
                c = composants(e) if e.get("type") == "minecraft:item" else None
                nom = c.get("minecraft:custom_name") if c else None
                texte = nom.get("text") if isinstance(nom, dict) else None
                if texte in TROPHEES:
                    change, retires = True, retires + 1
                    continue
                if texte in RENOMMES:
                    nom["text"] = RENOMMES[texte]
                    texte = RENOMMES[texte]
                    change, renommes = True, renommes + 1
                if texte and not e["name"].endswith("spawn_egg") and not e["name"].startswith("royaumes:"):
                    s = slug(texte)
                    cible = "royaumes:dp/" + s
                    if c.get("minecraft:item_model") != cible:
                        c["minecraft:item_model"] = cible
                        change = True
                    couleur = COULEURS_MC.get(nom.get("color", ""), (200, 200, 200))
                    v = vus.setdefault(s, {"nom": texte, "base": e["name"], "c1": couleur, "faction": faction})
                    if faction and not v["faction"]:
                        v["faction"] = faction
                garde.append(e)
            if len(garde) != len(pool.get("entries", [])):
                pool["entries"] = garde
        j["pools"] = [pl for pl in j.get("pools", []) if pl.get("entries")]
        if change:
            ecrire(p, j)
    # fonctions : lignes qui ouvraient les tables d'œufs supprimées, et objets donnés par « give »
    for p in glob.glob(os.path.join(DATA, "function", "**", "*.mcfunction"), recursive=True):
        s = open(p, encoding="utf-8").read()
        t = "\n".join(l for l in s.split("\n") if not re.search(r"loot royaumes:debug/oeufs_\d", l)
                      and not ("Œufs des mobs" in l and "text_display" in l))
        for m in re.finditer(r'item_model="([^"]+)"([^\n]*?)custom_name=\{"text":"([^"]+)"', t):
            s2 = slug(m.group(3))
            vus.setdefault(s2, {"nom": m.group(3), "base": "minecraft:carrot_on_a_stick", "c1": (240, 170, 30), "faction": None})
            t = t.replace('item_model="%s"%s' % (m.group(1), m.group(2)), 'item_model="royaumes:dp/%s"%s' % (s2, m.group(2)), 1)
        for a, b in RENOMMES.items():
            t = t.replace(a, b)
        if t != s:
            open(p, "w", encoding="utf-8").write(t)
    for p in glob.glob(os.path.join(DATA, "dialog", "**", "*.json"), recursive=True):
        s = open(p, encoding="utf-8").read()
        t = s
        for a, b in RENOMMES.items():
            t = t.replace(a, b)
        if t != s:
            open(p, "w", encoding="utf-8").write(t)
    # icônes
    d_tex = os.path.join(ASSETS, "textures", "item", "dp")
    os.makedirs(d_tex, exist_ok=True)
    for s, v in vus.items():
        cat = categorie(v["nom"], v["base"])
        fc = coul_f.get(v["faction"]) if v["faction"] else None
        c1 = fc[0] if fc and cat in ("epee", "hache", "marteau", "lance", "faux", "baton", "arc", "fusil", "bouclier", "griffes", "pioche") else v["c1"]
        c2 = fc[1] if fc else mix(v["c1"], (255, 230, 150), 0.5)
        im = dessin(cat, tuple(c1), tuple(c2), s, v["nom"])
        im.save(os.path.join(d_tex, s + ".png"))
        manie = cat in ("epee", "hache", "marteau", "lance", "faux", "baton", "pioche", "griffes")
        ecrire(os.path.join(ASSETS, "models", "item", "dp", s + ".json"),
               {"parent": "minecraft:item/handheld" if manie else "minecraft:item/generated", "textures": {"layer0": "royaumes:item/dp/" + s}})
        ecrire(os.path.join(ASSETS, "items", "dp", s + ".json"), {"model": {"type": "minecraft:model", "model": "royaumes:item/dp/" + s}})
    print("designs : %d objets dessinés, %d doublons retirés, %d renommés" % (len(vus), retires, renommes))
    return vus


if __name__ == "__main__":
    principal()
