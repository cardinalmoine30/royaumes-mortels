# -*- coding: utf-8 -*-
"""Arsenal des 25 factions : pour chacune, une arme de champion (très puissante), une arme de lignée (moyenne, atout
spécial) et une armure en 4 pièces (bonus de panoplie). Tout se forge à la Forge de guerre, réservée à sa faction, avec
des éclats de deux Royaumes étrangers.
Produit : modèles 3D des armes (en main) + icônes plates (inventaire), textures d'armure portée tirées des skins,
traductions, recettes et fr/royaumes/ArsenalGenere.java.  Lancer : python3 outils/objets/arsenal.py"""
import json
import os
import random
import sys

from PIL import Image

ICI = os.path.dirname(os.path.abspath(__file__))
RACINE = os.path.abspath(os.path.join(ICI, "..", ".."))
ASSETS = os.path.join(RACINE, "src", "main", "resources", "assets", "royaumes")
JAVA = os.path.join(RACINE, "src", "main", "java", "fr", "royaumes")
sys.path.insert(0, ICI)
sys.path.insert(0, os.path.join(ICI, ".."))
sys.path.insert(0, os.path.join(ICI, "..", "gui"))
from objets import VENTS, vent_de_royaume, ecrire, T, mul, mix, jstr  # noqa: E402
from donnees_factions import FACTIONS  # noqa: E402
from aos import EMBLEMES  # noqa: E402

COUL = {e[0]: (e[1], e[2]) for e in EMBLEMES}
# faction : (champion nom, type), (lignée nom, type), atout, (casque, torse, jambes, bottes), bonus de panoplie
ARSENAL = {
    "stormcast": (("Marteau de Sigmar", "marteau"), ("Lame runique d'Azyr", "epee"), "foudre", ("Heaume céleste", "Cuirasse de sigmarite", "Grèves de sigmarite", "Solerets d'Azyr"), "resistance:0,speed:0"),
    "cites": (("Épée de Freeguild", "epee"), ("Hallebarde de la cité", "lance"), "faiblesse", ("Morion de garde", "Cuirasse de la cité", "Cuissards de garde", "Bottes de marche"), "resistance:0,haste:0"),
    "fyreslayers": (("Hache runique d'ur-or", "hache"), ("Marteau de forge-rune", "marteau"), "feu", ("Casque à crête", "Plastron runique", "Jambières d'ur-or", "Bottes de magma"), "fire_resistance:0,strength:0"),
    "kharadron": (("Marteau à aether", "marteau"), ("Hachette d'aéronaute", "hache"), "recul", ("Masque à aether", "Combinaison d'aether-or", "Jambières d'arkanaute", "Bottes à endrins"), "slow_falling:0,resistance:0"),
    "khaine": (("Lame du Meurtrier", "epee"), ("Glaive sacrificiel", "lance"), "vol_de_vie", ("Bandeau de Khaine", "Harnais de sang", "Jupe de lames", "Sandales de sœur"), "speed:1,strength:0"),
    "idoneth": (("Lance de la marée", "lance"), ("Lame d'âme", "epee"), "lenteur", ("Heaume des profondeurs", "Écailles d'Idoneth", "Jambières de nacre", "Bottes des abysses"), "water_breathing:0,dolphins_grace:0"),
    "lumineth": (("Épée de soleil-métal", "epee"), ("Lance de Hysh", "lance"), "aveugle", ("Heaume de Hysh", "Cuirasse de lumière", "Grèves d'albâtre", "Bottes de Teclis"), "night_vision:0,speed:0"),
    "seraphon": (("Macuahuitl céleste", "epee"), ("Lance du Slann", "lance"), "lenteur", ("Masque de Saurus", "Plastron d'écailles", "Jambières de jade", "Pattes de Saurus"), "jump_boost:1,resistance:0"),
    "sylvaneth": (("Lame de bois-vif", "epee"), ("Bâton épineux", "baton"), "lenteur", ("Couronne d'écorce", "Écorce d'Alarielle", "Racines-jambières", "Racines-bottes"), "regeneration:0,speed:0"),
    "esclaves": (("Épée du Chaos", "epee"), ("Hache de guerre maudite", "hache"), "faiblesse", ("Heaume à cornes", "Armure du Chaos", "Jambières maudites", "Solerets noirs"), "strength:0,resistance:0"),
    "khorne": (("Hache de sang", "hache"), ("Épée de Khorne", "epee"), "feu", ("Heaume de crânes", "Cuirasse d'airain", "Jambières de sang", "Bottes de carnage"), "strength:1"),
    "tzeentch": (("Lame changeante", "epee"), ("Bâton de feu de Tzeentch", "baton"), "feu", ("Masque de Tzeentch", "Robe changeante", "Jambières bleues", "Bottes à plumes"), "speed:0,fire_resistance:0"),
    "slaanesh": (("Rapière exquise", "epee"), ("Fouet-lame", "lance"), "aveugle", ("Diadème d'extase", "Corset de Slaanesh", "Jambières de soie", "Bottes à talons"), "speed:1,haste:0"),
    "nurgle": (("Fléau pestilentiel", "marteau"), ("Hache rouillée", "hache"), "poison", ("Heaume putride", "Armure pestilente", "Jambières gonflées", "Bottes de fange"), "regeneration:0,resistance:0"),
    "skaven": (("Hallebarde de malepierre", "lance"), ("Lame rouillée", "epee"), "poison", ("Casque de clanrat", "Haillons de malepierre", "Jambières rapiécées", "Pattes de rat"), "speed:1,night_vision:0"),
    "hashut": (("Marteau de l'Ash", "marteau"), ("Hache de forge", "hache"), "feu", ("Haut casque d'Hashut", "Cuirasse de basalte", "Jambières de lave", "Bottes de cendre"), "fire_resistance:0,resistance:0"),
    "nighthaunt": (("Faux spectrale", "faux"), ("Lame tranchante", "epee"), "fletri", ("Capuche spectrale", "Linceul", "Haillons fantômes", "Chaînes d'ombre"), "invisibility:0,slow_falling:0"),
    "soulblight": (("Épée vampirique", "epee"), ("Lance du chevalier de sang", "lance"), "vol_de_vie", ("Heaume du comte", "Cuirasse sanglante", "Jambières de nuit", "Bottes de l'aristocrate"), "night_vision:0,strength:0"),
    "ossiarch": (("Glaive d'os", "faux"), ("Lance-os", "lance"), "fletri", ("Crâne-heaume", "Cage thoracique", "Fémurs-jambières", "Os-solerets"), "resistance:1"),
    "fec": (("Couperet du festin", "hache"), ("Massue d'os", "marteau"), "vol_de_vie", ("Couronne du roi-goule", "Haillons royaux", "Jambières de fange", "Pattes griffues"), "regeneration:0,speed:0"),
    "ironjawz": (("Grand Kikoup'", "hache"), ("Choppa", "hache"), "recul", ("Casque à mâchoire", "Plaques d'Ironjawz", "Jambières de fer", "Bottes de fer"), "resistance:0,strength:0"),
    "kruleboyz": (("Pique des marais", "lance"), ("Lame empoisonnée", "epee"), "poison", ("Casque de Kruleboy", "Armure de marais", "Jambières de vase", "Bottes de vase"), "speed:0,resistance:0"),
    "gitz": (("Lune-lance", "lance"), ("Bâton à champignons", "baton"), "aveugle", ("Capuche noire", "Robe de Gitz", "Jambières sombres", "Bottes de squig"), "jump_boost:1,night_vision:0"),
    "ogors": (("Couperet de boucher", "hache"), ("Massue d'ogre", "marteau"), "recul", ("Casque de boucher", "Plaque de bedaine", "Jambières d'ogre", "Bottes d'ogre"), "health_boost:1,strength:0"),
    "behemat": (("Arbre-gourdin", "marteau"), ("Massue de géant", "marteau"), "recul", ("Casque de géant", "Harnais de géant", "Braies de géant", "Sandales de géant"), "health_boost:2,resistance:0"),
}
ATOUTS = {"foudre": "Foudre : la cible est frappée par l'éclair", "feu": "Brasier : enflamme la cible", "poison": "Venin : empoisonne la cible",
          "fletri": "Flétrissure : flétrit la cible", "vol_de_vie": "Vol de vie : te soigne à chaque coup", "lenteur": "Entrave : ralentit fortement la cible",
          "recul": "Fracas : projette la cible au loin", "aveugle": "Éclat : aveugle la cible", "faiblesse": "Brise-garde : affaiblit la cible"}
# stats : (dégâts en plus, vitesse) selon le type, champion (netherite) / lignée (diamant)
STATS = {"epee": ((6.0, -2.4), (3.5, -2.4)), "hache": ((8.0, -3.0), (5.0, -3.0)), "marteau": ((9.0, -3.2), (5.5, -3.1)),
         "lance": ((6.5, -2.6), (4.0, -2.5)), "faux": ((7.5, -2.8), (4.5, -2.7)), "baton": ((5.0, -2.2), (3.0, -2.0))}
PIECES = ["casque", "torse", "jambes", "bottes"]


def etrangers(f):
    """Deux Royaumes étrangers dont la faction doit importer les éclats."""
    h = vent_de_royaume(f["royaume"])
    a, b = (h + 3) % 8, (h + 5) % 8
    return VENTS[a][0], VENTS[b][0]


def recettes(f):
    a, b = etrangers(f)
    ea, eb = "royaumes:eclat_" + a, "royaumes:eclat_" + b
    return [
        [("minecraft:netherite_ingot", 1), (ea, 4), (eb, 2), ("royaumes:pierre_royaumes_brute", 4)],
        [("minecraft:diamond", 2), (ea, 2), ("minecraft:iron_ingot", 4)],
        [("minecraft:iron_ingot", 5), (eb, 2), ("royaumes:pierre_royaumes_brute", 2)],
        [("minecraft:diamond", 2), ("minecraft:iron_ingot", 6), (ea, 3), (eb, 2)],
        [("minecraft:diamond", 1), ("minecraft:iron_ingot", 5), (ea, 2), (eb, 2)],
        [("minecraft:iron_ingot", 4), (eb, 2), ("royaumes:pierre_royaumes_brute", 2)],
    ]


# ------------------------------------------------------------------ palette (texture 16x16 en cases de 4x4)
def palette(fid, champion):
    c1, c2 = COUL.get(fid, ((120, 120, 120), (220, 220, 220)))
    metal = (225, 228, 235) if champion else (190, 192, 200)
    cases = [metal, mul(metal, 0.7), c2, mul(c2, 0.7), (92, 62, 40), (60, 40, 26), c1, mul(c1, 0.7),
             mix(c2, (255, 255, 255), 0.5), (40, 36, 44), mix(c1, (255, 255, 255), 0.4), (255, 240, 200),
             mul(metal, 0.5), c2, c1, (20, 20, 24)]
    t = T()
    r = random.Random(sum(map(ord, fid)))
    for i, c in enumerate(cases):
        for y in range(4):
            for x in range(4):
                t.p((i % 4) * 4 + x, (i // 4) * 4 + y, mul(c, 0.94 + r.random() * 0.12))
    return t.im


UV = {"metal": 0, "metal_s": 1, "acc": 2, "acc_s": 3, "manche": 4, "manche_s": 5, "fac": 6, "fac_s": 7, "clair": 8, "sombre": 9,
      "fac_c": 10, "gemme": 11}


def el(a, b, mat):
    i = UV[mat]
    u, v = (i % 4) * 4, (i // 4) * 4
    faces = {f: {"uv": [u, v, u + 4, v + 4], "texture": "#p"} for f in ("north", "south", "east", "west", "up", "down")}
    return {"from": a, "to": b, "faces": faces, "rotation": {"angle": -45, "axis": "z", "origin": [8, 8, 8]}}


def geometrie(type_, champion):
    """Arme verticale (y), centrée en x=8, z=8, inclinée à 45° comme une arme en main."""
    E = []
    z0, z1 = 7.25, 8.75
    m = "metal" if champion else "metal_s"
    if type_ == "epee":
        E += [el([7.4, -3, 7.4], [8.6, 3, 8.6], "manche"), el([7.2, -4, 7.2], [8.8, -3, 8.8], "acc"),
              el([4.5, 3, 7], [11.5, 4.2, 9], "acc"), el([6.9, 4.2, 7.6], [9.1, 18.5, 8.4], m), el([7.4, 18.5, 7.7], [8.6, 20, 8.3], m),
              el([7.8, 4.2, 7.5], [8.2, 17, 8.5], "fac")]
        if champion:
            E += [el([7.5, 2.8, 6.8], [8.5, 4.4, 9.2], "gemme")]
    elif type_ == "hache":
        E += [el([7.4, -4, 7.4], [8.6, 16, 8.6], "manche"), el([8.6, 9, 7.6], [13.5, 16.5, 8.4], m),
              el([13.5, 8, 7.7], [14.5, 17.5, 8.3], "clair"), el([4.5, 11, 7.7], [7.4, 14.5, 8.3], m if champion else "manche_s"),
              el([7.2, 15.5, 7.2], [8.8, 17, 8.8], "acc")]
    elif type_ == "marteau":
        E += [el([7.4, -4, 7.4], [8.6, 13, 8.6], "manche"), el([4, 13, 5.5], [12, 18.5, 10.5], m),
              el([3.6, 13.8, 5.2], [4.2, 17.7, 10.8], "acc"), el([11.8, 13.8, 5.2], [12.4, 17.7, 10.8], "acc"),
              el([7, 14.5, 4.9], [9, 17, 11.1], "fac")]
        if champion:
            E += [el([7.6, 18.5, 7.6], [8.4, 20.5, 8.4], "gemme")]
    elif type_ == "lance":
        E += [el([7.5, -6, 7.5], [8.5, 15, 8.5], "manche"), el([7, 15, 7.6], [9, 20, 8.4], m), el([7.6, 20, 7.8], [8.4, 22, 8.2], m),
              el([6, 14.5, 7.2], [10, 15.5, 8.8], "acc"), el([7.3, 11, 7.3], [8.7, 13, 8.7], "fac")]
    elif type_ == "faux":
        E += [el([7.5, -5, 7.5], [8.5, 17, 8.5], "manche"), el([8.5, 15, 7.7], [16, 17, 8.3], m), el([14, 12, 7.7], [16, 15, 8.3], m),
              el([7.2, 16.5, 7.2], [8.8, 18, 8.8], "fac"), el([7.3, 3, 7.3], [8.7, 4.5, 8.7], "acc")]
    else:  # bâton
        E += [el([7.5, -5, 7.5], [8.5, 15, 8.5], "manche"), el([6.5, 15, 6.5], [9.5, 18, 9.5], "fac"),
              el([7.2, 18, 7.2], [8.8, 19.6, 8.8], "gemme"), el([6.2, 14, 6.2], [9.8, 15, 9.8], "acc")]
    return E


AFFICHAGE = {
    "thirdperson_righthand": {"rotation": [0, -90, 55], "translation": [0, 4, 0.5], "scale": [0.85, 0.85, 0.85]},
    "thirdperson_lefthand": {"rotation": [0, 90, -55], "translation": [0, 4, 0.5], "scale": [0.85, 0.85, 0.85]},
    "firstperson_righthand": {"rotation": [0, -90, 25], "translation": [1.13, 3.2, 1.13], "scale": [0.68, 0.68, 0.68]},
    "firstperson_lefthand": {"rotation": [0, 90, -25], "translation": [1.13, 3.2, 1.13], "scale": [0.68, 0.68, 0.68]},
}


# ------------------------------------------------------------------ icônes plates (inventaire)
def icone(type_, fid, champion):
    c1, c2 = COUL.get(fid, ((120, 120, 120), (220, 220, 220)))
    metal = (225, 228, 235) if champion else (180, 182, 190)
    t = T()
    for i in range(10 if type_ in ("lance", "faux", "baton") else 6):  # manche en diagonale
        t.p(1 + i, 14 - i, (110, 74, 46))
        t.p(2 + i, 14 - i, (70, 46, 28))
    if type_ == "epee":
        for i in range(10):
            t.p(5 + i, 10 - i, metal)
            t.p(6 + i, 10 - i, mul(metal, 0.7))
        for k in range(-2, 3):
            t.p(5 + k, 11 + k, c2)
        t.p(4, 11, c1)
    elif type_ in ("hache", "faux"):
        for y in range(1, 9):
            for x in range(8, 16):
                if (x - 11) ** 2 / 10 + (y - 4.5) ** 2 / 14 <= 1 and x >= 10:
                    t.p(x, y, metal if x > 12 else mul(metal, 0.75))
        t.p(14, 3, c2)
        for i in range(4):
            t.p(7 + i, 8 - i, c1)
    elif type_ == "marteau":
        for y in range(1, 8):
            for x in range(9, 16):
                if abs((x - 12) - (y - 4)) <= 3 and abs((x - 12) + (y - 4)) <= 4:
                    t.p(x, y, metal if (x + y) % 4 else mul(metal, 0.7))
        t.p(12, 4, c1)
        t.p(13, 3, c2)
    elif type_ == "lance":
        for (x, y) in [(12, 3), (13, 2), (14, 1), (13, 3), (12, 2), (14, 2), (13, 1)]:
            t.p(x, y, metal)
        t.p(11, 4, c2)
        t.p(10, 5, c1)
    else:
        for y in range(1, 6):
            for x in range(10, 15):
                if (x - 12) ** 2 + (y - 3) ** 2 <= 5:
                    t.p(x, y, c1 if (x + y) % 2 else c2)
        t.p(12, 3, (255, 245, 200))
    if champion:
        t.p(15, 0, (255, 240, 160))
        t.p(14, 0, (255, 220, 120))
    t.contour()
    return t.im


def icone_armure(piece, fid):
    c1, c2 = COUL.get(fid, ((120, 120, 120), (220, 220, 220)))
    t = T()
    if piece == "casque":
        for y in range(3, 12):
            for x in range(3, 13):
                if (x - 7.5) ** 2 / 25 + (y - 7) ** 2 / 20 <= 1 or y >= 7:
                    t.p(x, y, c1)
        for x in range(5, 11):
            t.p(x, 8, (20, 16, 24))
        for y in range(3, 12):
            t.p(7, y, c2)
            t.p(8, y, c2)
    elif piece == "torse":
        for y in range(2, 15):
            for x in range(2, 14):
                if (y < 6 or 4 <= x <= 11) and not (y < 4 and 6 <= x <= 9):
                    t.p(x, y, c1)
        for y in range(5, 14):
            t.p(7, y, c2)
            t.p(8, y, c2)
        for x in range(4, 12):
            t.p(x, 13, c2)
    elif piece == "jambes":
        for y in range(2, 15):
            for x in range(3, 13):
                if y < 6 or not (7 <= x <= 8):
                    t.p(x, y, c1)
        for x in range(3, 13):
            t.p(x, 3, c2)
    else:
        for y in range(8, 15):
            for x in range(2, 14):
                if not (7 <= x <= 8) and (y > 10 or x in (3, 4, 5, 10, 11, 12)):
                    t.p(x, y, c1)
        for x in (2, 3, 4, 5, 10, 11, 12, 13):
            t.p(x, 14, c2)
    t.contour()
    return t.im


# ------------------------------------------------------------------ armure portée : tirée du skin de la faction
def armure_portee(fid):
    skin = Image.open(os.path.join(ASSETS, "textures", "skin", fid + ".png")).convert("RGBA")
    c1, c2 = COUL.get(fid, ((120, 120, 120), (220, 220, 220)))
    l1 = Image.new("RGBA", (64, 32), (0, 0, 0, 0))
    l1.paste(skin.crop((0, 0, 32, 16)), (0, 0))      # casque (tête)
    l1.paste(skin.crop((16, 16, 56, 32)), (16, 16))  # torse et bras
    l1.paste(skin.crop((0, 16, 16, 32)), (0, 16))    # bottes (jambes)
    px = l1.load()
    # visière : la face avant du casque devient métal de faction avec une fente sombre
    for y in range(8, 16):
        for x in range(8, 16):
            px[x, y] = tuple(mul(c1, 0.9 if (x + y) % 3 else 0.8)) + (255,)
    for x in range(9, 15):
        px[x, 11] = (16, 14, 20, 255)
    for y in range(9, 16):
        px[11, y] = px[12, y] = tuple(c2) + (255,)
    for x in range(8, 16):  # couronne du casque
        px[x, 0] = px[x, 7] = tuple(c2) + (255,)
    l2 = Image.new("RGBA", (64, 32), (0, 0, 0, 0))
    l2.paste(skin.crop((0, 16, 16, 32)), (0, 16))    # jambières
    l2.paste(skin.crop((16, 24, 40, 32)), (16, 24))  # taille
    for d in ("humanoid", "humanoid_leggings"):
        os.makedirs(os.path.join(ASSETS, "textures", "entity", "equipment", d), exist_ok=True)
    l1.save(os.path.join(ASSETS, "textures", "entity", "equipment", "humanoid", fid + ".png"))
    l2.save(os.path.join(ASSETS, "textures", "entity", "equipment", "humanoid_leggings", fid + ".png"))
    ecrire(os.path.join(ASSETS, "equipment", fid + ".json"),
           {"layers": {"humanoid": [{"texture": "royaumes:" + fid}], "humanoid_leggings": [{"texture": "royaumes:" + fid}]}})


# ------------------------------------------------------------------ fichiers
def main():
    ti = os.path.join(ASSETS, "textures", "item")
    fr, en = {}, {}
    java = {"ids": [], "noms": [], "types": [], "ingr": [], "atout": [], "bonus": []}
    for f in FACTIONS:
        fid = f["id"]
        champ, lign, atout, pieces, bonus = ARSENAL[fid]
        ids, noms, types = [], [], []
        for k, ((nom, type_), champion) in enumerate(((champ, True), (lign, False))):
            oid = fid + ("_champion" if champion else "_lignee")
            palette(fid, champion).save(os.path.join(ti, oid + "_palette.png"))
            icone(type_, fid, champion).save(os.path.join(ti, oid + ".png"))
            ecrire(os.path.join(ASSETS, "models", "item", oid + "_3d.json"),
                   {"textures": {"p": "royaumes:item/" + oid + "_palette", "particle": "royaumes:item/" + oid + "_palette"},
                    "elements": geometrie(type_, champion), "display": AFFICHAGE, "gui_light": "front"})
            ecrire(os.path.join(ASSETS, "models", "item", oid + ".json"),
                   {"parent": "minecraft:item/handheld", "textures": {"layer0": "royaumes:item/" + oid}})
            ecrire(os.path.join(ASSETS, "items", oid + ".json"), {"model": {
                "type": "minecraft:select", "property": "minecraft:display_context",
                "cases": [{"when": ["gui", "ground", "fixed"], "model": {"type": "minecraft:model", "model": "royaumes:item/" + oid}}],
                "fallback": {"type": "minecraft:model", "model": "royaumes:item/" + oid + "_3d"}}})
            ids.append(oid)
            noms.append(nom)
            types.append(type_ + (":c" if champion else ":l"))
            fr["item.royaumes." + oid] = nom
            en["item.royaumes." + oid] = nom
        for piece, nom in zip(PIECES, pieces):
            oid = fid + "_" + piece
            icone_armure(piece, fid).save(os.path.join(ti, oid + ".png"))
            ecrire(os.path.join(ASSETS, "models", "item", oid + ".json"), {"parent": "minecraft:item/generated", "textures": {"layer0": "royaumes:item/" + oid}})
            ecrire(os.path.join(ASSETS, "items", oid + ".json"), {"model": {"type": "minecraft:model", "model": "royaumes:item/" + oid}})
            ids.append(oid)
            noms.append(nom)
            types.append(piece)
            fr["item.royaumes." + oid] = nom
            en["item.royaumes." + oid] = nom
        armure_portee(fid)
        java["ids"].append(ids)
        java["noms"].append(noms)
        java["types"].append(types)
        java["ingr"].append([",".join("%s*%d" % (i, n) for i, n in r) for r in recettes(f)])
        java["atout"].append(atout)
        java["bonus"].append(bonus)
    fr.update({"block.royaumes.forge_de_guerre": "Forge de guerre", "royaumes.forge.titre": "Forge de guerre"})
    en.update({"block.royaumes.forge_de_guerre": "War Forge", "royaumes.forge.titre": "War Forge"})
    for lang, d in (("fr_fr", fr), ("en_us", en)):
        p = os.path.join(ASSETS, "lang", lang + ".json")
        old = json.load(open(p, encoding="utf-8"))
        old.update(d)
        ecrire(p, old)
    L = ["package fr.royaumes;", "", "/** FICHIER GÉNÉRÉ par outils/objets/arsenal.py : ne pas modifier à la main. */",
         "public final class ArsenalGenere {", "    private ArsenalGenere() {}", ""]

    def tab2(nom, t):
        L.append("    public static final String[][] %s = {" % nom)
        L.append("        {},")
        for ligne in t:
            L.append("        {" + ", ".join(jstr(x) for x in ligne) + "},")
        L.append("    };")
    tab2("IDS", java["ids"])
    tab2("NOMS", java["noms"])
    tab2("TYPES", java["types"])
    tab2("RECETTES", java["ingr"])
    L.append("    public static final String[] ATOUTS = {\"\", " + ", ".join(jstr(x) for x in java["atout"]) + "};")
    L.append("    public static final String[] TEXTES_ATOUTS = {\"\", " + ", ".join(jstr(ATOUTS[x]) for x in java["atout"]) + "};")
    L.append("    public static final String[] BONUS = {\"\", " + ", ".join(jstr(x) for x in java["bonus"]) + "};")
    L.append("    /** Dégâts en plus et vitesse d'attaque : [type][0 champion, 1 lignée][0 dégâts, 1 vitesse]. */")
    L.append("    public static final String[] TYPES_ARMES = {" + ", ".join(jstr(t) for t in STATS) + "};")
    L.append("    public static final float[][][] STATS = {" + ", ".join(
        "{{%.1fF, %.1fF}, {%.1fF, %.1fF}}" % (c[0], c[1], l[0], l[1]) for c, l in STATS.values()) + "};")
    L.append("}")
    open(os.path.join(JAVA, "ArsenalGenere.java"), "w", encoding="utf-8").write("\n".join(L) + "\n")
    print("arsenal :", sum(len(x) for x in java["ids"]), "objets")


if __name__ == "__main__":
    main()
