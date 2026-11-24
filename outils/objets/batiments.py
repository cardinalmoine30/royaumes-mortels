# -*- coding: utf-8 -*-
"""Bâtiments du camp de guerre : 5 bâtiments x 3 niveaux x 4 styles (Ordre, Chaos, Mort, Destruction).
Même fonction pour tous, mais une architecture propre à chaque Grande Alliance (matériaux ET forme du toit,
des murs et des ornements). Sortie : src/main/resources/royaumes_camp/batiments.json, lu par le mod qui pose
les blocs autour de l'étendard (porte tournée vers l'étendard). Repère : x/z centrés, y = 0 au niveau du sol,
porte côté -z."""
import json
import os

ICI = os.path.dirname(os.path.abspath(__file__))
SORTIE = os.path.join(ICI, "..", "..", "src", "main", "resources", "royaumes_camp", "batiments.json")

BATIMENTS = ["forge", "ferme", "sanctuaire", "caserne", "tour"]
STYLES = ["ordre", "chaos", "mort", "destruction"]
PAL = {
    "ordre": dict(sol="royaumes:marbre_celeste", mur="royaumes:marbre_celeste", pilier="royaumes:or_vif", toit="minecraft:blue_terracotta",
                  faite="royaumes:or_vif", deco="royaumes:marbre_celeste_grave", lum="minecraft:lantern", bois="minecraft:dark_oak_planks"),
    "chaos": dict(sol="minecraft:polished_blackstone", mur="minecraft:polished_blackstone_bricks", pilier="royaumes:obsidienne_corrompue",
                  toit="minecraft:red_nether_bricks", faite="royaumes:pierre_du_chaos", deco="royaumes:pierre_du_chaos", lum="minecraft:magma_block",
                  bois="minecraft:crimson_planks"),
    "mort": dict(sol="minecraft:deepslate_tiles", mur="royaumes:pierre_funeraire", pilier="minecraft:bone_block", toit="minecraft:polished_deepslate",
                 faite="royaumes:dalle_des_ames", deco="royaumes:dalle_des_ames", lum="minecraft:soul_lantern", bois="minecraft:dark_oak_planks"),
    "destruction": dict(sol="minecraft:coarse_dirt", mur="minecraft:cobblestone", pilier="minecraft:spruce_log", toit="minecraft:spruce_planks",
                        faite="minecraft:hay_block", deco="royaumes:os_de_monstre", lum="minecraft:lantern", bois="minecraft:spruce_planks"),
}


class Plan:
    def __init__(self, style):
        self.b = {}
        self.p = PAL[style]
        self.style = style

    def mettre(self, x, y, z, bloc):
        self.b[(x, y, z)] = self.p.get(bloc, bloc)

    def boite(self, x0, y0, z0, x1, y1, z1, bloc, creux=False):
        for x in range(x0, x1 + 1):
            for y in range(y0, y1 + 1):
                for z in range(z0, z1 + 1):
                    bord = x in (x0, x1) or z in (z0, z1)
                    if not creux or bord:
                        self.mettre(x, y, z, bloc)

    def vider(self, x0, y0, z0, x1, y1, z1):
        for k in [k for k in self.b if x0 <= k[0] <= x1 and y0 <= k[1] <= y1 and z0 <= k[2] <= z1]:
            del self.b[k]


def coque(P, r, h):
    """Sol, murs et piliers d'angle propres au style, porte au centre du côté -z."""
    s = P.style
    P.boite(-r, -1, -r, r, -1, r, "sol")
    if s == "destruction":  # palissade de rondins irrégulière
        for x in range(-r, r + 1):
            for z in range(-r, r + 1):
                if x in (-r, r) or z in (-r, r):
                    hh = h + ((x * 7 + z * 3) % 2)
                    for y in range(hh):
                        P.mettre(x, y, z, "pilier" if (x + z) % 2 == 0 else "mur")
    else:
        P.boite(-r, 0, -r, r, h - 1, r, "mur", creux=True)
        for (x, z) in ((-r, -r), (r, -r), (-r, r), (r, r)):
            for y in range(h + (1 if s in ("chaos", "mort") else 0)):
                P.mettre(x, y, z, "pilier")
    if s == "ordre":  # frise gravée et fenêtres
        for x in range(-r + 1, r):
            P.mettre(x, h - 1, -r, "deco")
            P.mettre(x, h - 1, r, "deco")
        for z in (-1, 1):
            if h > 3:
                P.mettre(-r, 2, z, "minecraft:glass_pane")
                P.mettre(r, 2, z, "minecraft:glass_pane")
    if s == "mort":  # contreforts d'os
        for x in (-r - 1, r + 1):
            for z in range(-r + 1, r, 2):
                P.mettre(x, 0, z, "pilier")
                P.mettre(x, 1, z, "pilier")
    P.vider(0, 0, -r, 0, 1, -r)  # porte
    if s == "destruction":
        P.mettre(-1, 2, -r - 1, "deco")  # défenses de bête sur la porte
        P.mettre(1, 2, -r - 1, "deco")
    P.mettre(-1, 2 if h > 2 else 1, -r - 1, "lum") if s != "destruction" else None


def toit(P, r, h):
    s = P.style
    if s == "ordre":  # toit à deux pans, faîtage d'or
        for k in range(r + 1):
            P.boite(-r - 1 + k, h + k, -r - 1, r + 1 - k, h + k, r + 1, "toit")
        P.boite(0, h + r, -r - 1, 0, h + r, r + 1, "faite")
    elif s == "chaos":  # toit plat, pointes aux angles et brasier central
        P.boite(-r, h, -r, r, h, r, "toit")
        for (x, z) in ((-r, -r), (r, -r), (-r, r), (r, r)):
            for y in range(h, h + 3):
                P.mettre(x, y, z, "pilier")
            P.mettre(x, h + 3, z, "faite")
        P.mettre(0, h + 1, 0, "lum")
    elif s == "mort":  # toit en gradins de crypte
        for k in range(r + 1):
            P.boite(-r + k, h + k, -r + k, r - k, h + k, r - k, "toit")
        P.mettre(0, h + r + 1, 0, "faite")
        P.mettre(0, h + r + 2, 0, "lum")
    else:  # destruction : toit penché de planches et de paille
        for k in range(2 * r + 3):
            z = -r - 1 + k
            y = h + k // 3
            for x in range(-r - 1, r + 2):
                P.mettre(x, y, z, "toit" if (x + k) % 3 else "faite")
        P.mettre(r, h + 2, -r, "deco")


def interieur(P, bat, n, r, h):
    P.mettre(r - 1, 0, r - 1, "minecraft:chest")
    P.mettre(-r + 1, h - 1 if h > 2 else 1, 0, "lum") if P.style != "chaos" else P.mettre(0, -1, 0, "lum")
    if bat == "forge":
        P.mettre(-r + 1, 0, r - 1, "minecraft:blast_furnace")
        P.mettre(0, 0, r - 1, "minecraft:anvil")
        if n >= 2:
            P.mettre(-r + 1, 0, 1, "minecraft:lava_cauldron")
            P.mettre(-r + 1, 0, -1, "minecraft:furnace")
            for y in range(h, h + 5):  # cheminée
                P.mettre(-r + 1, y, r - 1, "mur")
            P.mettre(-r + 1, h + 5, r - 1, "minecraft:campfire")
        if n >= 3:
            P.mettre(r - 1, 0, 1, "minecraft:smithing_table")
            P.mettre(r - 1, 0, -1, "minecraft:grindstone")
            P.mettre(1, 0, r - 1, "minecraft:blast_furnace")
    elif bat == "ferme":
        P.mettre(-r + 1, 0, r - 1, "minecraft:hay_block")
        P.mettre(-r + 1, 1, r - 1, "minecraft:hay_block")
        P.mettre(0, 0, r - 1, "minecraft:smoker")
        P.mettre(r - 1, 0, -r + 1, "minecraft:composter")
        if n >= 2:
            for x in range(-r + 1, 0):
                P.mettre(x, -1, -1, "minecraft:farmland")
                P.mettre(x, 0, -1, "minecraft:wheat")
            P.mettre(1, 0, r - 1, "minecraft:barrel")
        if n >= 3:
            P.mettre(r - 1, 0, 1, "minecraft:water_cauldron")
            for x in range(-r + 1, 0):
                P.mettre(x, -1, 1, "minecraft:farmland")
                P.mettre(x, 0, 1, "minecraft:carrots")
    elif bat == "sanctuaire":
        P.mettre(0, 0, 1, "royaumes:autel_arcanique")
        if n >= 2:
            P.mettre(-r + 1, 0, r - 1, "minecraft:enchanting_table")
            P.mettre(-r + 1, 0, 1, "minecraft:bookshelf")
            P.mettre(r - 1, 0, 1, "minecraft:bookshelf")
        if n >= 3:
            for (x, z) in ((-1, -1), (1, -1)):
                P.mettre(x, 0, z, "royaumes:cristal_de_hysh")
                P.mettre(x, 1, z, "royaumes:cristal_de_hysh")
            P.mettre(0, h - 1, 1, "royaumes:pierre_de_lumiere")
    elif bat == "caserne":
        for z in range(-r + 2, r, 2):
            P.mettre(-r + 1, 0, z, "minecraft:white_wool" if P.style == "ordre" else "minecraft:red_wool" if P.style == "chaos" else "minecraft:gray_wool" if P.style == "mort" else "minecraft:brown_wool")
        P.mettre(0, 0, r - 1, "minecraft:crafting_table")
        P.mettre(1, 0, r - 1, "minecraft:barrel")
        if n >= 2:
            for z in range(-r + 2, r, 2):
                P.mettre(r - 1, 0, z, "minecraft:white_wool" if P.style == "ordre" else "minecraft:red_wool" if P.style == "chaos" else "minecraft:gray_wool" if P.style == "mort" else "minecraft:brown_wool")
        if n >= 3:
            P.mettre(0, 0, 1, "minecraft:target")
            P.mettre(-1, 0, r - 1, "minecraft:fletching_table")


def tour(P, n):
    hauteur = {1: 6, 2: 10, 3: 14}[n]
    P.boite(-2, -1, -2, 2, -1, 2, "sol")
    P.boite(-1, 0, -1, 1, hauteur - 1, 1, "mur", creux=True)
    for (x, z) in ((-1, -1), (1, -1), (-1, 1), (1, 1)):
        for y in range(hauteur):
            P.mettre(x, y, z, "pilier")
    for y in range(hauteur):
        P.mettre(0, y, 0, "minecraft:scaffolding")
    P.vider(0, 0, -1, 0, 1, -1)
    P.boite(-2, hauteur, -2, 2, hauteur, 2, "bois")
    P.vider(0, hauteur, 0, 0, hauteur, 0)
    for x in range(-2, 3):
        for z in range(-2, 3):
            if x in (-2, 2) or z in (-2, 2):
                P.mettre(x, hauteur + 1, z, "mur" if (x + z) % 2 == 0 else "pilier")
    P.mettre(0, hauteur + 2, 2, "royaumes:pierre_de_lumiere" if n >= 2 else "lum")
    P.mettre(1, 0, 2, "minecraft:chest")  # coffre au pied, adossé
    s = P.style
    if s == "ordre":
        P.mettre(0, hauteur + 3, 2, "faite")
    elif s == "chaos":
        for (x, z) in ((-2, -2), (2, -2), (-2, 2), (2, 2)):
            P.mettre(x, hauteur + 2, z, "pilier")
            P.mettre(x, hauteur + 3, z, "faite")
    elif s == "mort":
        P.mettre(0, hauteur + 2, -2, "minecraft:skeleton_skull")
        P.mettre(0, hauteur + 1, 0, "lum")
    else:
        P.mettre(-2, hauteur + 2, -2, "deco")
        P.mettre(2, hauteur + 2, -2, "deco")
    if n >= 3:  # bannière de signal
        P.mettre(0, hauteur + 1, -2, "faite")


def plan(bat, n, style):
    P = Plan(style)
    if bat == "tour":
        tour(P, n)
    else:
        r = {1: 2, 2: 3, 3: 3}[n]
        h = {1: 3, 2: 4, 3: 5}[n]
        coque(P, r, h)
        toit(P, r, h)
        interieur(P, bat, n, r, h)
        if n >= 3:  # annexe/ornement de niveau 3
            P.mettre(-r - 1, 0, -r - 1, "pilier")
            P.mettre(r + 1, 0, -r - 1, "pilier")
            P.mettre(-r - 1, 1, -r - 1, "lum")
            P.mettre(r + 1, 1, -r - 1, "lum")
    return P.b


def compacter(b):
    pal = sorted(set(b.values()))
    idx = {v: i for i, v in enumerate(pal)}
    return {"p": pal, "b": [[x, y, z, idx[v]] for (x, y, z), v in sorted(b.items(), key=lambda kv: (kv[0][1], kv[0][0], kv[0][2]))]}


def tous():
    return {bat: {st: [plan(bat, n, st) for n in (1, 2, 3)] for st in STYLES} for bat in BATIMENTS}


def main():
    t = tous()
    sortie = {bat: {st: [compacter(b) for b in niv] for st, niv in d.items()} for bat, d in t.items()}
    os.makedirs(os.path.dirname(SORTIE), exist_ok=True)
    with open(SORTIE, "w", encoding="utf-8") as f:
        json.dump(sortie, f, separators=(",", ":"))
    n = sum(len(b) for d in t.values() for niv in d.values() for b in niv)
    print("bâtiments :", len(BATIMENTS), "x 3 niveaux x", len(STYLES), "styles,", n, "blocs,", os.path.getsize(SORTIE) // 1024, "Ko")


if __name__ == "__main__":
    main()
