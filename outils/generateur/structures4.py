# -*- coding: utf-8 -*-
"""Version 4 : constructions inspirées des références Age of Sigmar fournies."""
import math
from nbtgen import Struct
from details import (rempart, meurtrieres, tour, fenetre_arc, lustre, table, tapis, banniere_murale, cheminee,
                     bibliotheque, statue_guerrier, comete, etoile8, crane_geant)
import chateaux
import structures3 as S3

F = 4
L = "royaumes:coffres/"


def base(sx, sy, sz, sol, fond, seed, haut=14):
    s = Struct(sx, sy, sz, seed)
    s.foundation(0, 0, sx - 1, sz - 1, F - 1, F, fond)
    s.fill(0, F, 0, sx - 1, F, sz - 1, sol)
    s.clear(0, F + 1, 0, sx - 1, F + haut, sz - 1)
    return s


def cercle(cx, cz, r, pas=10):
    vus = set()
    for a in range(0, 360, pas):
        p = (cx + round(r * math.cos(math.radians(a))), cz + round(r * math.sin(math.radians(a))))
        if p not in vus:
            vus.add(p)
            yield p


def marqueur(s, x, y, z, *tags):
    s.entities.append(((x + 0.5, y, z + 0.5), (x, y, z), {"id": "minecraft:marker", "Tags": list(tags)}))


def coller(dst, src, ox, oy, oz):
    for (x, y, z), v in src.blocks.items():
        dst.blocks[(x + ox, y + oy, z + oz)] = v
    for (px, py, pz), (bx, by, bz), nbt in src.entities:
        dst.entities.append(((px + ox, py + oy, pz + oz), (bx + ox, by + oy, bz + oz), nbt))


def sous_marin(s):
    """Remplace l'air par de l'eau et immerge les blocs compatibles."""
    import json
    blocs = json.load(open("/tmp/mc-sum/blocks/data.json"))
    for k, (st, nbt) in list(s.blocks.items()):
        bid = st.split("[")[0]
        short = bid.split(":")[1]
        if short == "air":
            s.blocks[k] = ("minecraft:water", None)
        elif short in blocs and "waterlogged" in blocs[short][0]:
            if "waterlogged=true" in st:
                continue
            if "[" in st:
                st = st[:-1] + ",waterlogged=true]" if "waterlogged" not in st else st.replace("waterlogged=false", "waterlogged=true")
            else:
                st = st + "[waterlogged=true]"
            s.blocks[k] = (st, nbt)


def statue_ailee(s, x, y, z, corps="minecraft:gold_block", aile="minecraft:white_wool", socle="minecraft:quartz_bricks"):
    """Stormcast ailé (Prosecutor) aux ailes déployées, sur un rocher."""
    statue_guerrier(s, x, y, z, corps, "minecraft:lapis_block", "minecraft:lightning_rod", socle)
    for side in (-1, 1):
        for k in range(1, 7):
            h = 6 + (k if k < 4 else 7 - k)
            for dy in range(0, 3 if k < 5 else 2):
                s.set(x + side * (2 + k), y + h - dy, z + 1, aile if dy else "minecraft:smooth_quartz")


def rotonde(s, cx, y, cz, r=5, h=7, col="minecraft:quartz_pillar", toit="minecraft:smooth_quartz", dome="minecraft:lapis_block"):
    """Temple circulaire à colonnes (tholos) avec coupole."""
    s.disk(cx, cz, r + 1, y, "minecraft:quartz_bricks")
    for (x, z) in cercle(cx, cz, r, 30):
        s.fill(x, y + 1, z, x, y + h, z, col)
    s.cylinder(cx, cz, r + 1, y + h + 1, y + h + 1, toit, hollow=False)
    for i in range(r):
        s.cylinder(cx, cz, r - i, y + h + 2 + i // 2, y + h + 2 + i // 2, dome, hollow=True, inside=None)
    s.set(cx, y + h + 2 + r // 2, cz, "minecraft:gold_block")
    s.set(cx, y + h + 3 + r // 2, cz, "minecraft:lightning_rod")


# =================================================================== STORMCAST : forteresse sur pic rocheux
def forteresse_stormcast():
    core = chateaux.forteresse_stormcast()          # 55 × 52 × 55
    H, M = 16, 8                                     # hauteur du pic, marge autour
    W = 55 + 2 * M
    s = Struct(W, 52 + H, W, 71)
    roc = ["minecraft:stone", "minecraft:andesite", "minecraft:diorite", "minecraft:calcite", "minecraft:stone", "minecraft:tuff"]
    c = W // 2
    rng = s.rng
    # Pic rocheux évasé, aux falaises irrégulières
    for y in range(0, H + 1):
        demi = (W // 2) - int((M - 1) * (y / H)) - 0
        for x in range(W):
            for z in range(W):
                dx, dz = abs(x - c), abs(z - c)
                bruit = (math.sin(x * 0.7 + y) + math.cos(z * 0.6 - y * 0.5)) * 1.6
                if max(dx, dz) <= demi + bruit - 1:
                    s.set(x, y, z, rng.choice(roc))
    # rampe en lacet sur la face sud
    for i in range(H + 1):
        x0 = W - 4 - i
        z = W - 3
        for dz in range(0, 3):
            s.set(x0, i, z - dz, "minecraft:stone_brick_stairs[facing=west]")
            s.set(x0 + 1, i, z - dz, "minecraft:stone_bricks")
            for yy in range(i + 1, i + 4):
                s.set(x0, yy, z - dz, "minecraft:air"); s.set(x0 + 1, yy, z - dz, "minecraft:air")
        if i % 4 == 0:
            s.set(x0, i + 1, z + 0 if z + 0 < W else z, "minecraft:lantern")
    s.fill(c, H, W - 4, W - 4 - H, H, W - 2, "minecraft:stone_bricks")
    s.fill(c - 2, H, M + 52, c + 2, H, W - 2, "minecraft:polished_diorite")
    # Fortresse posée sur le pic
    coller(s, core, M, H - 3, M)
    # Statue ailée sur un éperon (nord-ouest) et rotonde (nord-est)
    s.fill(1, H - 2, 1, 7, H, 7, roc)
    statue_ailee(s, 4, H + 1, 4)
    s.fill(W - 9, H - 2, 1, W - 2, H, 9, roc)
    rotonde(s, W - 6, H, 5, r=3, h=6)
    # Éclairs : marqueurs sur les paratonnerres principaux
    temple_top = H - 3 + 4 + 21 + 8
    marqueur(s, c, temple_top + 2, M + 15, "rm_foudre")
    for (x, z) in ((M + 4, M + 4), (W - M - 5, W - M - 5)):
        marqueur(s, x, H - 3 + 4 + 28, z, "rm_foudre")
    return s


# =================================================================== SERAPHON : temple à glyphes et portail céleste
def glyphe(s, x, y, z, plan, motif, bloc="minecraft:gold_block", fond="minecraft:chiseled_stone_bricks"):
    """Panneau 3×3 de glyphes sur une face (plan 'x' = face nord/sud)."""
    for dy in range(3):
        for d in range(3):
            b = bloc if motif[dy][d] == "#" else fond
            if plan == "x":
                s.set(x + d, y + 2 - dy, z, b)
            else:
                s.set(x, y + 2 - dy, z + d, b)


MOTIFS = [["#.#", ".#.", "#.#"], ["###", "#.#", "###"], [".#.", "###", ".#."], ["#..", "##.", "###"], ["##.", "#.#", ".##"]]


def temple_seraphon():
    W = 53
    s = base(W, 52, W, ["minecraft:mossy_stone_bricks", "minecraft:grass_block", "minecraft:moss_block", "minecraft:stone_bricks"],
             "minecraft:mossy_cobblestone", 72, haut=10)
    c = W // 2
    pierre = ["minecraft:stone_bricks", "minecraft:mossy_stone_bricks", "minecraft:cracked_stone_bricks", "minecraft:chiseled_stone_bricks",
              "minecraft:stone_bricks"]
    rng = s.rng
    # Pyramide à 5 gradins de 4 blocs, faces couvertes de panneaux de glyphes
    x0, x1, y = 7, W - 8, F + 1
    gradins = []
    while x1 - x0 >= 12:
        s.fill(x0, y, x0, x1, y + 3, x1, pierre)
        s.fill(x0, y + 3, x0, x1, y + 3, x1, "minecraft:polished_andesite")
        for k in range(x0 + 1, x1 - 2, 4):
            m = MOTIFS[(k + y) % len(MOTIFS)]
            glyphe(s, k, y, x1, "x", m, "minecraft:gold_block" if (k // 4) % 2 else "minecraft:prismarine_bricks")
            glyphe(s, k, y, x0, "x", m, "minecraft:prismarine_bricks")
            glyphe(s, x0, y, k, "z", m); glyphe(s, x1, y, k, "z", m)
        gradins.append((x0, x1, y))
        x0 += 4; x1 -= 4; y += 4
    top = y
    # Grand escalier central bordé de rampes à glyphes
    for i in range(top - F - 1):
        zz = W - 8 - i
        s.fill(c - 3, F + 1 + i, zz, c + 3, F + 1 + i, zz, "minecraft:stone_brick_stairs[facing=north]")
        s.fill(c - 3, F + 1, zz, c + 3, F + i, zz, "minecraft:stone_bricks")
        for dx in (-4, 4):
            s.fill(c + dx, F + 1, zz, c + dx, F + 2 + i, zz, pierre)
    tapis_vegetal = ["minecraft:vine[north=true]", "minecraft:vine[south=true]", "minecraft:vine[east=true]", "minecraft:vine[west=true]"]
    # Lianes qui grimpent sur les faces
    for (x0_, x1_, y0) in gradins:
        for k in range(x0_, x1_ + 1, 2):
            if rng.random() < 0.45:
                for dy in range(rng.randint(1, 4)):
                    s.set(k, y0 + 3 - dy, x1_ + 1, "minecraft:vine[north=true]")
            if rng.random() < 0.45:
                for dy in range(rng.randint(1, 4)):
                    s.set(x1_ + 1, y0 + 3 - dy, k, "minecraft:vine[west=true]")
                for dy in range(rng.randint(1, 3)):
                    s.set(x0_ - 1, y0 + 3 - dy, k, "minecraft:vine[east=true]")
        for (xx, zz) in ((x0_, x0_), (x1_, x0_), (x0_, x1_), (x1_, x1_)):
            s.set(xx, y0 + 4, zz, "minecraft:azalea_leaves[persistent=true]")
    # Sommet : plateforme et portail céleste (anneau de glyphes, éclairs bleus, orbe noir)
    s.fill(c - 6, top, c - 6, c + 6, top, c + 6, "minecraft:chiseled_stone_bricks")
    R = 7
    for a in range(0, 360, 5):
        for rr in (R, R + 1):
            x = c + round(rr * math.cos(math.radians(a)))
            yy = top + 1 + R + round(rr * math.sin(math.radians(a)))
            if yy > top:
                s.set(x, yy, c, "minecraft:gold_block" if (a % 45 == 0 and rr == R + 1) else
                      "minecraft:chiseled_stone_bricks" if a % 15 == 0 else "minecraft:stone_bricks")
    oy = top + 1 + R
    for dx in range(-2, 3):
        for dy in range(-2, 3):
            if dx * dx + dy * dy <= 5:
                s.set(c + dx, oy + dy, c, "minecraft:black_concrete")
    s.set(c, oy, c, "minecraft:crying_obsidian")
    for k, a in enumerate(range(0, 360, 30)):  # arcs d'énergie céleste
        for r in range(3, R):
            x = c + round(r * math.cos(math.radians(a + r * 9)))
            yy = oy + round(r * math.sin(math.radians(a + r * 9)))
            if yy > top and s.get(x, yy, c) in (None, "minecraft:air"):
                s.set(x, yy, c, "minecraft:light_blue_stained_glass_pane" if (r + k) % 2 else "minecraft:cyan_stained_glass_pane")
    for dx in (-R - 3, R + 3):  # totems à visages
        s.fill(c + dx, top + 1, c, c + dx, top + 9, c, "minecraft:chiseled_stone_bricks")
        for yy in (top + 3, top + 6, top + 9):
            s.set(c + dx, yy, c + 1, "minecraft:gold_block")
        s.set(c + dx, top + 10, c, "minecraft:sea_lantern")
    marqueur(s, c, oy, c, "rm_amb_celeste")
    s.chest(c - 5, top + 1, c - 4, L + "temple_seraphon", "south"); s.chest(c + 5, top + 1, c - 4, L + "temple_seraphon", "south")
    # Totems de glyphes au pied de l'escalier (comme sur la maquette)
    for dx in (-8, 8):
        tx, tz = c + dx, W - 5
        s.fill(tx - 1, F + 1, tz - 1, tx + 1, F + 8, tz + 1, ["minecraft:chiseled_stone_bricks", "minecraft:mossy_stone_bricks"])
        for yy in (F + 2, F + 5):
            glyphe(s, tx - 1, yy, tz + 2, "x", MOTIFS[(yy + dx) % 5], "minecraft:gold_block", "minecraft:stone_bricks")
        s.set(tx, F + 9, tz, "minecraft:gold_block"); s.set(tx, F + 10, tz, "minecraft:end_rod")
    # Palanquin flottant du Slann (à droite) et Saurus
    px, pz = W - 6, W - 10
    s.disk(px, pz, 3, F + 3, "minecraft:gold_block")
    s.disk(px, pz, 2, F + 4, "minecraft:prismarine_bricks")
    s.fill(px - 1, F + 5, pz - 1, px + 1, F + 6, pz + 1, "minecraft:prismarine")
    s.set(px, F + 7, pz, "minecraft:prismarine"); s.set(px, F + 8, pz, "minecraft:gold_block")
    s.set(px - 1, F + 7, pz + 1, "minecraft:gold_block"); s.set(px + 1, F + 7, pz + 1, "minecraft:gold_block")
    # Arbres de jungle tordus autour
    for (tx, tz) in ((4, 5), (W - 5, 5), (3, W - 7), (W - 4, 18), (5, 22)):
        h = rng.randint(9, 13)
        s.fill(tx, F + 1, tz, tx, F + h, tz, "minecraft:jungle_log")
        for (dx, dz) in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            s.set(tx + dx, F + h - 3, tz + dz, "minecraft:jungle_log[axis=%s]" % ("x" if dx else "z"))
        for yy in range(F + h - 2, F + h + 2):
            r = 3 if yy < F + h + 1 else 2
            s.cylinder(tx, tz, r, yy, yy, ["minecraft:jungle_leaves[persistent=true]", "minecraft:azalea_leaves[persistent=true]"], hollow=False)
        for k in range(3):
            s.set(tx + 2, F + h - 3 - k, tz, "minecraft:vine[west=true]")
    # Bassins sacrés
    for (x, z) in ((3, c), (W - 4, c - 6)):
        s.fill(x - 1, F, z - 3, x + 1, F, z + 3, "minecraft:water")
        s.set(x, F - 1, z, "minecraft:sea_lantern")
        s.set(x, F + 1, z - 1, "minecraft:lily_pad")
    s.mob(c, top + 1, c - 3, "zombie", "saurus", 2)
    s.mob(c + 4, F + 1, W - 3, "zombie", "saurus", 3)
    s.mob(c - 6, F + 1, W - 3, "skeleton", "skink", 4)
    return s


# =================================================================== ORRUKS : huttes à pointes
def hutte_orruk(s, cx, cz, y, r=4):
    """Hutte ronde : soubassement de pierre et bois, toit en plaques de métal à étages, cornes, hublots, porte cerclée."""
    s.cylinder(cx, cz, r, y, y + 3, ["minecraft:cobblestone", "minecraft:spruce_planks", "minecraft:stripped_spruce_log", "minecraft:mossy_cobblestone"],
               hollow=True, inside="minecraft:air")
    s.disk(cx, cz, r - 1, y, "minecraft:spruce_planks")
    s.cylinder(cx, cz, r, y + 3, y + 3, "minecraft:spruce_log", hollow=True, inside=None)
    # Toit à 3 étages de plaques (fer / cuivre) avec débord
    plaques = ["minecraft:iron_block", "minecraft:waxed_weathered_cut_copper", "minecraft:waxed_exposed_cut_copper", "minecraft:iron_block"]
    for i, rr in enumerate((r + 1, r, r - 1)):
        yy = y + 4 + i
        s.cylinder(cx, cz, rr, yy, yy, plaques, hollow=True, inside=None)
        s.disk(cx, cz, rr - 1, yy, "minecraft:spruce_planks" if i < 2 else plaques[0])
    s.disk(cx, cz, max(1, r - 3), y + 7, "minecraft:iron_block")
    s.set(cx, y + 8, cz, "minecraft:iron_block"); s.set(cx, y + 9, cz, "minecraft:pointed_dripstone[vertical_direction=up]")
    # Cornes / pointes en os au bord du toit
    for (x, z) in cercle(cx, cz, r + 1, 60):
        s.set(x, y + 5, z, "minecraft:bone_block")
        s.set(x, y + 6, z, "minecraft:pointed_dripstone[vertical_direction=up]")
    # Hublots hexagonaux et porte
    for (dx, dz) in ((r, 0), (-r, 0), (0, -r)):
        s.set(cx + dx, y + 2, cz + dz, "minecraft:iron_bars")
    s.clear(cx - 1, y + 1, cz + r, cx + 1, y + 2, cz + r)
    s.set(cx, y + 3, cz + r, "minecraft:iron_block")
    s.set(cx - 1, y + 3, cz + r, "minecraft:spruce_stairs[facing=east,half=top]")
    s.set(cx + 1, y + 3, cz + r, "minecraft:spruce_stairs[facing=west,half=top]")
    s.set(cx, y + 3, cz, "minecraft:lantern[hanging=true]")
    s.set(cx - 2, y + 1, cz - 1, "minecraft:red_bed[facing=north,part=head]"); s.set(cx - 2, y + 1, cz, "minecraft:red_bed[facing=north,part=foot]")
    s.barrel(cx + 2, y + 1, cz - 1, L + "camp_orruk")


def camp_orruk():
    s = S3.camp_orruk()
    W = s.size[0]
    # On remplace les anciennes huttes carrées par des huttes à pointes
    for (x, z) in ((6, 16), (6, 27), (W - 13, 16), (W - 13, 27)):
        s.clear(x - 1, S3.F, z - 1, x + 8, S3.F + 8, z + 7)
        s.fill(x - 1, S3.F, z - 1, x + 8, S3.F, z + 7, "minecraft:coarse_dirt")
        hutte_orruk(s, x + 4, z + 3, S3.F, 4)
    return s


# =================================================================== GITZ : forteresse de la Mauvaise Lune dans les marais
def croissant(s, cx, cy, z, r=6, bloc="minecraft:yellow_terracotta", plan="x"):
    for x in range(-r, r + 1):
        for y in range(-r, r + 1):
            d1 = x * x + y * y
            d2 = (x - 3) ** 2 + (y + 1) ** 2
            if d1 <= r * r and d2 > (r - 1) ** 2:
                if plan == "x":
                    s.set(cx + x, cy + y, z, bloc if (x + y) % 5 else "minecraft:end_stone")
                else:
                    s.set(z, cy + y, cx + x, bloc if (x + y) % 5 else "minecraft:end_stone")


def antre_gitz():
    W = 51
    s = Struct(W, 64, W, 73)
    c = W // 2
    rng = s.rng
    sombre = ["minecraft:deepslate", "minecraft:cobbled_deepslate", "minecraft:tuff", "minecraft:blackstone", "minecraft:deepslate_bricks"]
    # Marais : sol boueux et mares vertes
    s.fill(0, 0, 0, W - 1, 3, W - 1, ["minecraft:mud", "minecraft:mud", "minecraft:dirt", "minecraft:moss_block"])
    for (x, z, r) in ((8, 9, 5), (W - 9, 12, 4), (10, W - 9, 6), (W - 10, W - 8, 4)):
        s.disk(x, z, r, 3, "minecraft:water"); s.disk(x, z, r, 2, "minecraft:lime_stained_glass")
        s.set(x, 4, z, "minecraft:lily_pad")
    # Rocher-forteresse aux tours déchiquetées
    for y in range(4, 20):
        r = int(15 - (y - 4) * 0.55)
        s.cylinder(c, c, r, y, y, sombre, hollow=False)
    for (dx, dz, h) in ((-6, -4, 30), (5, -5, 26), (0, 4, 34), (-4, 6, 22), (7, 3, 24)):
        x, z = c + dx, c + dz
        for y in range(19, 19 + h):
            r = 3 if y < 19 + h - 6 else 2 if y < 19 + h - 2 else 1
            s.cylinder(x, z, r, y, y, sombre, hollow=False)
            if y % 5 == 0:
                s.set(x + r, y, z, "minecraft:shroomlight")  # fenêtres orangées
        s.set(x, 19 + h, z, "minecraft:pointed_dripstone[vertical_direction=up]")
    # La Mauvaise Lune (croissant) au sommet de la plus haute tour
    croissant(s, c, 19 + 34 + 7, c + 4, r=7)
    s.set(c - 2, 19 + 34 + 6, c + 5, "minecraft:black_concrete"); s.set(c - 1, 19 + 34 + 8, c + 5, "minecraft:red_concrete")
    # Entrée de grotte et salle intérieure
    for y in range(4, 10):
        s.cylinder(c, c, 6, y, y, "minecraft:air", hollow=False)
    s.clear(c - 2, 4, c + 6, c + 2, 7, c + 16)
    s.set(c, 4, c, "minecraft:campfire")
    s.chest(c - 4, 4, c, L + "antre_gitz", "east"); s.chest(c + 4, 4, c, L + "antre_gitz", "west")
    s.set(c, 9, c, "minecraft:shroomlight")
    for (x, z) in cercle(c, c, 5, 45):
        s.set(x, 8, z, "minecraft:cobweb")
    # Colonnes de lueur verte (brume de la Mauvaise Lune)
    for (x, z) in ((5, c), (W - 6, c - 4), (c - 12, W - 5), (c + 14, 6), (c - 3, 4)):
        for y in range(4, 4 + rng.randint(5, 9)):
            s.set(x, y, z, rng.choice(["minecraft:lime_stained_glass", "minecraft:green_stained_glass", "minecraft:verdant_froglight"]))
        marqueur(s, x, 6, z, "rm_amb_lueur")
    # Champignons géants autour
    for (x, z, h, cap) in ((4, W - 4, 9, "red"), (W - 5, W - 4, 11, "brown"), (W - 5, 4, 8, "red")):
        s.fill(x, 4, z, x, 4 + h, z, "minecraft:mushroom_stem")
        s.cylinder(x, z, 3, 5 + h, 5 + h, f"minecraft:{cap}_mushroom_block", hollow=False)
        s.cylinder(x, z, 2, 6 + h, 6 + h, f"minecraft:{cap}_mushroom_block", hollow=False)
        s.set(x, 4 + h, z, "minecraft:shroomlight")
    s.mob(c + 2, 4, c + 10, "zombie", "grot", 6)
    s.mob(c - 3, 4, c - 2, "zombie", "grot", 3)
    s.mob(10, 4, W - 15, "spider", "arachnarok")
    return s


# =================================================================== SYLVANETH : arbres de Wyldwood
def arbre_wyldwood(s, x, y, z, h=12, seed=0, feuilles=("minecraft:acacia_leaves[persistent=true]", "minecraft:dark_oak_leaves[persistent=true]")):
    """Arbre tordu aux plateaux de feuilles plates (style Wyldwood Citadel)."""
    import random
    rng = random.Random(seed)
    tronc = ["minecraft:dark_oak_log", "minecraft:dark_oak_wood", "minecraft:mangrove_log"]
    # racines
    for (dx, dz) in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        s.set(x + dx, y, z + dz, "minecraft:dark_oak_wood"); s.set(x + 2 * dx, y - 1, z + 2 * dz, "minecraft:dark_oak_wood")
    cx, cz = x, z
    for yy in range(y, y + h):
        if yy - y in (h // 3, 2 * h // 3):
            cx += rng.choice((-1, 0, 1)); cz += rng.choice((-1, 0, 1))
        s.set(cx, yy, cz, rng.choice(tronc))
        if yy - y < 3:
            s.set(cx + 1, yy, cz, rng.choice(tronc))
    # visage d'esprit dans le tronc
    s.set(x, y + 2, z + 1, "minecraft:shroomlight")
    # branches et plateaux de feuilles
    for k in range(5):
        a = rng.uniform(0, 2 * math.pi)
        l = rng.randint(3, 6)
        by = y + h - 6 + rng.randint(0, 6)
        bx, bz = cx, cz
        for i in range(1, l + 1):
            bx = cx + round(i * math.cos(a)); bz = cz + round(i * math.sin(a))
            s.set(bx, by + i // 2, bz, "minecraft:dark_oak_wood")
        py = by + l // 2 + 1
        r = rng.randint(2, 3)
        for dx in range(-r, r + 1):
            for dz in range(-r, r + 1):
                if abs(dx) + abs(dz) <= r + 1 and rng.random() < 0.9:
                    s.set(bx + dx, py, bz + dz, rng.choice(feuilles))
        s.set(bx, py + 1, bz, rng.choice(feuilles))
    s.disk(cx, cz, 2, y + h, rng.choice(feuilles))
    s.set(cx, y + h + 1, cz, feuilles[0])


def bosquet_sylvaneth():
    s = S3.bosquet_sylvaneth()
    W = s.size[0]
    for i, (x, z) in enumerate(((6, 6), (W - 7, 6), (6, W - 7), (W - 7, W - 7), (4, W // 2), (W - 5, W // 2 + 3))):
        arbre_wyldwood(s, x, S3.F + 1, z, h=11 + i % 3, seed=100 + i)
    marqueur(s, W // 2, S3.F + 4, W // 2, "rm_amb_vie")
    return s


# =================================================================== MAGMAHOLD EN RUINE (volcans d'Aqshy)
def magmahold():
    W = 55
    s = Struct(W, 56, W, 74)
    c = W // 2
    rng = s.rng
    roc = ["minecraft:basalt", "minecraft:blackstone", "minecraft:polished_basalt", "minecraft:blackstone", "minecraft:smooth_basalt"]
    runes = ["minecraft:gold_block", "minecraft:orange_glazed_terracotta", "minecraft:gilded_blackstone"]
    # Deux falaises séparées par un gouffre de lave (axe nord-sud)
    for x in range(W):
        for z in range(W):
            d = abs(x - c) - 7                                   # distance au gouffre
            bord = min(z, W - 1 - z)                             # distance aux extrémités du canyon
            h = 34 - max(0, d) * 1.1 + 3 * math.sin(x * 0.4 + z * 0.25)
            h = min(h, 8 + bord * 2.2)
            for y in range(0, max(4, int(h))):
                gouffre = abs(x - c) < 7 + (y // 6) + int(2 * math.sin(z * 0.3))
                if not gouffre:
                    s.set(x, y, z, rng.choice(roc))
    s.fill(c - 14, 0, 0, c + 14, 2, W - 1, "minecraft:magma_block")
    for x in range(W):
        for z in range(W):
            if (x, 3, z) not in s.blocks:
                s.set(x, 3, z, "minecraft:lava")
    # Halls creusés dans les falaises : arches à bandeaux runiques
    for side in (-1, 1):
        fx = c + side * 10
        for zc in (12, 27, 42):
            for yy in range(20, 30):
                for dz in range(-3, 4):
                    if (dz * dz) / 9 + ((yy - 20) / 9) ** 2 <= 1:
                        for d in range(0, 6):
                            s.set(fx + side * d, yy, zc + dz, "minecraft:air")
            for dz in range(-4, 5):
                s.set(fx, 30, zc + dz, rng.choice(runes))
                s.set(fx, 19, zc + dz, "minecraft:polished_blackstone_bricks")
            s.fill(fx, 20, zc - 4, fx, 29, zc - 4, "minecraft:polished_blackstone_bricks")
            s.fill(fx, 20, zc + 4, fx, 29, zc + 4, "minecraft:polished_blackstone_bricks")
            s.set(fx + side * 4, 20, zc, "minecraft:lava_cauldron")
            if zc == 27:
                s.chest(fx + side * 3, 20, zc + 1, L + "magmahold", "north" if side > 0 else "south")
        # Grande tête de Fyreslayer sculptée dans la falaise
        hx = c + side * 9
        s.fill(hx, 28, c - 2, hx + side * 2, 36, c + 2, "minecraft:polished_blackstone_bricks")
        s.set(hx, 34, c - 1, "minecraft:magma_block"); s.set(hx, 34, c + 1, "minecraft:magma_block")
        s.fill(hx, 37, c - 2, hx + side * 2, 39, c + 2, "minecraft:orange_terracotta")  # crête
        s.fill(hx, 29, c - 1, hx, 31, c + 1, "minecraft:gold_block")                    # barbe d'or
    # Ponts runiques arqués
    for zb in (18, 34):
        for x in range(c - 12, c + 13):
            arc = int(4 * (1 - ((x - c) / 12.0) ** 2))
            for dz in range(-2, 3):
                s.set(x, 20 + arc, zb + dz, "minecraft:polished_blackstone_bricks")
                s.set(x, 19 + arc, zb + dz, rng.choice(runes) if dz in (-2, 2) else "minecraft:polished_blackstone_bricks")
                for yy in range(21 + arc, 25 + arc):
                    s.set(x, yy, zb + dz, "minecraft:air")
            s.set(x, 21 + arc, zb - 2, "minecraft:polished_blackstone_brick_wall")
            s.set(x, 21 + arc, zb + 2, "minecraft:polished_blackstone_brick_wall")
            if x % 4 == 0:
                s.set(x, 22 + arc, zb - 2, "minecraft:campfire"); s.set(x, 22 + arc, zb + 2, "minecraft:campfire")
        s.fill(c - 1, 15, zb - 1, c + 1, 18, zb + 1, "minecraft:polished_blackstone_bricks")  # pile centrale brisée
    # Chutes de lave
    for (x, z) in ((c - 8, 8), (c + 8, 24), (c - 8, 46)):
        for y in range(4, 34):
            s.set(x, y, z, "minecraft:lava")
    marqueur(s, c, 10, c, "rm_amb_braise")
    s.mob(c - 13, 20, 27, "zombie", "fyreslayer", 3)
    s.mob(c + 13, 20, 12, "zombie", "fyreslayer", 3)
    s.mob(c, 25, 18, "zombie", "hashut", 2)
    return s


# =================================================================== KHARADRON : port d'aether avec tyrolienne
def fregate(s, cx, y, z0, z1, ballon=True):
    cuivre = ["minecraft:waxed_cut_copper", "minecraft:waxed_exposed_cut_copper", "minecraft:waxed_copper_block"]
    for z in range(z0, z1 + 1):
        t = (z - z0) / max(1, (z1 - z0))
        half = 2 if t < 0.12 else 4 if t < 0.25 or t > 0.9 else 5
        s.fill(cx - half, y, z, cx + half, y, z, "minecraft:spruce_planks")
        s.fill(cx - half + 1, y - 1, z, cx + half - 1, y - 1, z, cuivre)
        s.fill(cx - half + 2, y - 2, z, cx + half - 2, y - 2, z, "minecraft:waxed_copper_block")
        s.set(cx - half, y + 1, z, "minecraft:waxed_cut_copper"); s.set(cx + half, y + 1, z, "minecraft:waxed_cut_copper")
        if z % 3 == 0:
            s.set(cx - half, y, z, "minecraft:glowstone"); s.set(cx + half, y, z, "minecraft:glowstone")
    s.fill(cx - 1, y, z0 - 2, cx + 1, y, z0 - 1, "minecraft:waxed_copper_block")
    s.set(cx, y, z0 - 3, "minecraft:lightning_rod[facing=north]")
    for z in range(z0 + 4, z1 - 3, 5):
        s.set(cx - 5, y + 1, z, "minecraft:dispenser[facing=west]"); s.set(cx + 5, y + 1, z, "minecraft:dispenser[facing=east]")
    if ballon:
        ez = (z0 + z1) // 2
        for x in range(cx - 5, cx + 6):
            for yy in range(y + 4, y + 15):
                for z in range(ez - 6, ez + 7):
                    d = ((x - cx) / 5) ** 2 + ((yy - y - 9) / 5) ** 2 + ((z - ez) / 6) ** 2
                    if 0.75 < d <= 1.0:
                        s.set(x, yy, z, "minecraft:waxed_copper_block" if (yy + z) % 4 else "minecraft:waxed_copper_bulb[lit=true]")
        for (dx, dz) in ((-4, -4), (4, -4), (-4, 4), (4, 4)):
            s.fill(cx + dx, y + 1, ez + dz, cx + dx, y + 4, ez + dz, "minecraft:iron_chain")
    for dx in (-6, 6):
        s.fill(cx + dx, y - 2, z1 - 2, cx + dx, y + 2, z1 - 2, "minecraft:waxed_copper_grate")
        s.fill(cx + dx, y, z1 - 4, cx + dx, y, z1, "minecraft:waxed_copper_grate")


def port_kharadron():
    W = 61
    s = Struct(W, 60, W, 75)
    c = W // 2
    cuivre = ["minecraft:waxed_cut_copper", "minecraft:waxed_exposed_cut_copper", "minecraft:waxed_copper_block", "minecraft:waxed_weathered_cut_copper"]
    # Quais de pierre, bassin d'amarrage et pontons
    s.fill(0, 0, 0, W - 1, 0, W - 1, ["minecraft:stone_bricks", "minecraft:polished_andesite", "minecraft:stone_bricks",
                                       "minecraft:cracked_stone_bricks"])
    s.fill(17, 0, 20, 50, 0, 46, "minecraft:water")
    s.walls(16, 0, 19, 51, 1, 47, "minecraft:polished_andesite")
    s.walls(16, 1, 19, 51, 1, 47, "minecraft:stone_brick_wall")
    for z in range(24, 46, 7):
        s.fill(17, 1, z, 30, 1, z + 1, "minecraft:spruce_planks")
        s.set(30, 2, z, "minecraft:spruce_fence"); s.set(30, 3, z, "minecraft:lantern")
    for (x, z) in ((16, 19), (51, 19), (16, 47), (51, 47), (34, 19), (34, 47)):
        s.fill(x, 2, z, x, 5, z, "minecraft:waxed_copper_block"); s.set(x, 6, z, "minecraft:waxed_copper_bulb[lit=true]")
    # Tour d'amarrage principale (A)
    ax, az = 8, 8
    s.cylinder(ax, az, 5, 1, 40, cuivre)
    s.cylinder(ax, az, 5, 1, 12, ["minecraft:polished_andesite", "minecraft:stone_bricks", "minecraft:chiseled_stone_bricks"])
    for y in range(14, 40, 5):
        for (dx, dz) in ((5, 0), (-5, 0), (0, 5), (0, -5)):
            if (dx, dz) != (-5, 0):
                s.set(ax + dx, y, az + dz, "minecraft:yellow_stained_glass")
    for y in range(6, 40, 6):
        s.cylinder(ax, az, 6, y, y, "minecraft:waxed_copper_grate", hollow=True, inside=None)
        s.disk(ax, az, 4, y, "minecraft:spruce_planks"); s.set(ax, y, az, "minecraft:air")
        s.set(ax + 5, y - 2, az, "minecraft:waxed_copper_bulb[lit=true]")
    for y in range(1, 41):
        s.set(ax + 4, y, az, "minecraft:ladder[facing=west]")
    s.clear(ax, 1, az + 5, ax, 2, az + 5)
    s.disk(ax, az, 7, 40, ["minecraft:waxed_cut_copper", "minecraft:spruce_planks"])
    s.cylinder(ax, az, 7, 41, 41, "minecraft:iron_bars", hollow=True, inside=None)
    s.cylinder(ax, az, 3, 41, 45, cuivre, hollow=True, inside="minecraft:air")
    s.cone(ax, az, 3, 46, "minecraft:waxed_copper_block")
    s.set(ax, 50, az, "minecraft:lightning_rod")
    # Tour B (arrivée de la tyrolienne)
    bx, bz = W - 9, W - 9
    s.cylinder(bx, bz, 4, 1, 22, cuivre)
    s.cylinder(bx, bz, 4, 1, 8, ["minecraft:polished_andesite", "minecraft:stone_bricks"])
    s.disk(bx, bz, 6, 22, ["minecraft:waxed_cut_copper", "minecraft:spruce_planks"])
    s.cylinder(bx, bz, 6, 23, 23, "minecraft:iron_bars", hollow=True, inside=None)
    for y in range(1, 23):
        s.set(bx - 3, y, bz, "minecraft:ladder[facing=east]")
    s.clear(bx, 1, bz - 4, bx, 2, bz - 4)
    # Câble de la tyrolienne (A → B)
    pa = (ax + 6, 45, az + 6)
    pb = (bx - 3, 26, bz - 3)
    n = 90
    for i in range(n + 1):
        t = i / n
        x = round(pa[0] + (pb[0] - pa[0]) * t); y = round(pa[1] + (pb[1] - pa[1]) * t)
        z = round(pa[2] + (pb[2] - pa[2]) * t)
        s.set(x, y, z, "minecraft:waxed_copper_chain[axis=x]")
    s.fill(ax + 5, 41, az + 5, ax + 7, 41, az + 7, "minecraft:waxed_cut_copper")
    s.set(ax + 6, 42, az + 7, "minecraft:waxed_copper_bulb[lit=true]")
    marqueur(s, ax + 6, 42, az + 6, "rm_tyro_debut")
    marqueur(s, bx - 3, 23, bz - 3, "rm_tyro_fin")
    s.set(ax + 6, 42, az + 6, "minecraft:yellow_carpet")
    # Frégate amarrée et canonnière
    fregate(s, 14, 24, 24, 50)
    fregate(s, 46, 14, 8, 22, ballon=False)
    s.fill(13, 24, az + 5, 15, 24, 23, "minecraft:waxed_cut_copper")  # passerelle tour → frégate
    s.chest(14, 25, 46, L + "port_kharadron", "north"); s.chest(12, 25, 46, L + "port_kharadron", "north")
    # Conduites d'aether-or et grue
    for x in range(20, W - 22, 2):
        s.set(x, 2, 4, "minecraft:waxed_copper_grate"); s.set(x, 3, 4, "minecraft:glowstone") if x % 4 == 0 else None
    s.fill(W - 20, 1, 6, W - 20, 16, 6, "minecraft:spruce_log")
    s.fill(W - 20, 16, 6, W - 10, 16, 6, "minecraft:spruce_log[axis=x]")
    s.fill(W - 11, 12, 6, W - 11, 15, 6, "minecraft:iron_chain")
    s.barrel(W - 11, 11, 6, L + "port_kharadron")
    # Entrepôts
    for (x0, z0) in ((20, 50), (36, 50)):
        s.hollow(x0, 0, z0, x0 + 10, 7, z0 + 8, cuivre, floor="minecraft:spruce_planks")
        s.roof_gable(x0, z0, x0 + 10, z0 + 8, 8, "minecraft:waxed_cut_copper_stairs", "minecraft:waxed_copper_block", axis="x")
        s.clear(x0 + 4, 1, z0, x0 + 6, 3, z0)
        for xx in range(x0 + 1, x0 + 10, 2):
            s.barrel(xx, 1, z0 + 7, L + "port_kharadron"); s.set(xx, 2, z0 + 7, "minecraft:glowstone")
    marqueur(s, 14, 30, 37, "rm_amb_aether")
    s.mob(14, 25, 36, "skeleton", "kharadron", 4)
    s.mob(ax, 41, az - 3, "skeleton", "kharadron", 2)
    s.mob(25, 1, 45, "skeleton", "kharadron", 2)
    return s


# =================================================================== LUMINETH : sanctuaire sur île flottante
def sanctuaire_lumineth():
    core = S3.sanctuaire_lumineth()                  # 41 × 56 × 41
    W = 55
    D = 26                                           # profondeur de l'île
    s = Struct(W, 56 + D, W, 76)
    c = W // 2
    rng = s.rng
    roche = ["minecraft:stone", "minecraft:calcite", "minecraft:andesite", "minecraft:diorite", "minecraft:dirt"]
    for y in range(0, D + 1):
        r = int(4 + (y / D) ** 0.6 * 19)
        for x in range(c - r - 2, c + r + 3):
            for z in range(c - r - 2, c + r + 3):
                d = math.hypot(x - c, z - c) + 1.5 * math.sin(x * 0.5) * math.cos(z * 0.5)
                if d <= r:
                    s.set(x, y, z, "minecraft:grass_block" if y == D else rng.choice(roche))
    # racines pendantes et lichen
    for (x, z) in cercle(c, c, 10, 15):
        for k in range(rng.randint(2, 6)):
            yy = int(D * ((math.hypot(x - c, z - c) - 4) / 20) ** (1 / 0.7)) - 1 - k
            if yy > 0:
                s.set(x, yy, z, "minecraft:hanging_roots")
    off = (W - 41) // 2
    coller(s, core, off, D - 3, off)
    # on arrondit le socle carré du sanctuaire pour qu'il épouse l'île
    for (x, y, z) in list(s.blocks):
        if D - 3 <= y <= D + 1 and math.hypot(x - c, z - c) > 21.5:
            del s.blocks[(x, y, z)]
        elif y == D + 1 and math.hypot(x - c, z - c) > 19.5 and s.blocks[(x, y, z)][0] != "minecraft:air":
            s.blocks[(x, y, z)] = ("minecraft:grass_block", None)
    # Îlots satellites avec cristaux
    for (x, z) in ((4, 4), (W - 5, 6), (5, W - 6)):
        for y in range(D + 4, D + 9):
            s.cylinder(x, z, max(0, 3 - (D + 8 - y) // 2) if y < D + 8 else 3, y, y, roche, hollow=False)
        s.fill(x, D + 9, z, x, D + 13, z, "minecraft:white_stained_glass")
        s.set(x, D + 14, z, "minecraft:end_rod")
    marqueur(s, c, D + 20, c, "rm_amb_lumiere")
    return s


# =================================================================== KHAINE : temple-estrade
def chaudron_sang(s, cx, y, cz):
    """Chaudron de Sang : vasque de cuivre pleine de sang sur un char à roues, flanqué de lames."""
    s.fill(cx - 2, y, cz - 2, cx + 2, y, cz + 2, "minecraft:dark_oak_planks")
    for (dx, dz) in ((-3, -2), (-3, 2), (3, -2), (3, 2)):
        s.set(cx + dx, y, cz + dz, "minecraft:polished_blackstone")   # roues
    s.fill(cx - 1, y + 1, cz - 1, cx + 1, y + 2, cz + 1, "minecraft:dark_oak_log")
    s.cylinder(cx, cz, 3, y + 3, y + 4, ["minecraft:waxed_copper_block", "minecraft:waxed_exposed_copper"], hollow=True, inside="minecraft:red_concrete")
    s.disk(cx, cz, 2, y + 4, "minecraft:red_stained_glass")
    for (dx, dz) in ((3, 0), (-3, 0), (0, 3), (0, -3)):
        s.fill(cx + dx, y + 5, cz + dz, cx + dx, y + 6, cz + dz, "minecraft:iron_bars")
    s.set(cx, y + 3, cz, "minecraft:magma_block")


def temple_khaine():
    W = 55
    s = base(W, 44, W, ["minecraft:smooth_stone", "minecraft:polished_deepslate", "minecraft:calcite", "minecraft:polished_deepslate"],
             "minecraft:stone_bricks", 77, haut=16)
    c = W // 2
    # Dallage en damier avec panneaux runiques
    for x in range(W):
        for z in range(W):
            s.set(x, F, z, "minecraft:calcite" if (x // 3 + z // 3) % 2 else "minecraft:polished_deepslate")
    for (px, pz) in ((c - 10, c + 10), (c + 10, c + 10)):
        s.fill(px - 3, F, pz - 3, px + 3, F, pz + 3, "minecraft:smooth_quartz")
        etoile8(s, px, F, pz, 2, "minecraft:red_concrete", "minecraft:gold_block")
    # Estrade à degrés au fond, tapis rouges sur les marches
    for i in range(5):
        s.fill(6 + i, F + 1 + i, 4, W - 7 - i, F + 1 + i, 16 - i, ["minecraft:stone_bricks", "minecraft:cracked_stone_bricks", "minecraft:chiseled_stone_bricks"])
    top = F + 5
    for side in (c - 9, c + 9):
        for i in range(5):
            for dx in range(-2, 3):
                s.set(side + dx, F + 1 + i, 17 - i, "minecraft:stone_brick_stairs[facing=south]")
        tapis(s, side - 1, 4, side + 1, 11, top + 1, "red")
    s.fill(c - 1, F + 1, 12, c + 1, F + 4, 16, "minecraft:air")   # passage central vers la crypte
    s.fill(c - 1, F, 12, c + 1, F, 16, "minecraft:black_concrete")
    # Chaudrons de Sang sur l'estrade
    chaudron_sang(s, c - 9, top + 1, 8)
    chaudron_sang(s, c + 9, top + 1, 8)
    # Morathi-Khaine : serpent ailé enroulé autour d'une colonne
    s.fill(c - 1, top + 1, 6, c + 1, top + 2, 8, "minecraft:chiseled_stone_bricks")
    s.fill(c, top + 3, 7, c, top + 15, 7, "minecraft:polished_blackstone")
    for k in range(48):
        a = k * 0.45
        x = c + round(1.6 * math.cos(a)); z = 7 + round(1.6 * math.sin(a))
        yy = top + 3 + k // 4
        s.set(x, yy, z, "minecraft:gold_block" if k % 7 == 0 else "minecraft:red_terracotta")
    s.fill(c - 1, top + 15, 6, c + 1, top + 18, 8, "minecraft:red_terracotta")          # buste
    s.fill(c - 1, top + 19, 7, c + 1, top + 20, 7, "minecraft:red_terracotta")          # tête
    s.set(c, top + 21, 7, "minecraft:gold_block"); s.set(c, top + 20, 8, "minecraft:black_concrete")
    for side in (-1, 1):
        s.set(c + side * 2, top + 17, 7, "minecraft:red_terracotta")
        s.set(c + side * 3, top + 18, 7, "minecraft:iron_bars")                         # lames
        for k in range(1, 10):
            h = top + 14 + (k if k < 6 else 11 - k)
            for dy in range(0, 5 if k < 7 else 3):
                s.set(c + side * (1 + k), h - dy, 6, "minecraft:nether_wart_block" if dy else "minecraft:red_terracotta")
    # Mur de fond à arcades, piliers d'angle et braseros
    for x in range(6, W - 6):
        for y in range(top, top + 11):
            s.set(x, y, 2, "minecraft:stone_bricks" if (x + y) % 5 else "minecraft:chiseled_stone_bricks")
            s.set(x, y, 3, "minecraft:stone_bricks")
    for x in range(9, W - 8, 6):
        for y in range(top + 2, top + 8):
            s.set(x, y, 3, "minecraft:air"); s.set(x + 1, y, 3, "minecraft:air")
        banniere_murale(s, x, top + 6, 4, "red", "south"); banniere_murale(s, x + 1, top + 6, 4, "black", "south")
    for x in range(6, W - 6, 2):
        s.set(x, top + 11, 2, "minecraft:stone_brick_wall")
    for (x, z) in ((7, 5), (W - 8, 5), (7, 15), (W - 8, 15)):
        s.fill(x, top + 1, z, x, top + 8, z, "minecraft:chiseled_stone_bricks")
        s.set(x, top + 9, z, "minecraft:polished_blackstone"); s.set(x, top + 10, z, "minecraft:campfire")
    # Statue de Khaine (croix de lames) en haut à droite
    kx = W - 9
    s.fill(kx, top + 1, 6, kx, top + 12, 6, "minecraft:iron_block")
    s.fill(kx - 3, top + 9, 6, kx + 3, top + 9, 6, "minecraft:iron_block")
    for (dx, dy) in ((-4, 9), (4, 9), (0, 13)):
        s.set(kx + dx, top + dy, 6, "minecraft:iron_bars")
    s.set(kx, top + 10, 6, "minecraft:redstone_block")
    # Sphinx/griffons gardiens flanquant l'estrade
    for gx in (6, W - 7):
        s.fill(gx - 1, F + 1, 18, gx + 1, F + 2, 21, "minecraft:polished_diorite")
        s.fill(gx - 1, F + 3, 18, gx + 1, F + 4, 19, "minecraft:polished_diorite")
        s.set(gx, F + 5, 18, "minecraft:diorite"); s.set(gx, F + 4, 17, "minecraft:diorite_stairs[facing=south]")
        s.fill(gx - 1, F + 5, 19, gx + 1, F + 5, 20, "minecraft:light_blue_terracotta")  # ailes repliées
    # Piliers runiques à torches rouges
    for (x, z) in ((c - 14, 24), (c + 14, 24), (c - 14, 38), (c + 14, 38), (c - 6, 30), (c + 6, 30), (c - 6, 46), (c + 6, 46)):
        s.fill(x, F + 1, z, x, F + 6, z, ["minecraft:chiseled_stone_bricks", "minecraft:stone_bricks", "minecraft:chiseled_tuff_bricks"])
        s.set(x, F + 7, z, "minecraft:stone_brick_slab")
        s.set(x + 1, F + 5, z, "minecraft:redstone_wall_torch[facing=east]")
    # Autel central du sang et murs bas en ruine
    s.disk(c, 34, 3, F, "minecraft:red_concrete")
    s.set(c, F + 1, 34, "minecraft:lava_cauldron"); s.set(c, F + 2, 34, "minecraft:iron_bars")
    for x in range(1, W - 1):
        for z in (1, W - 2):
            if s.rng.random() < 0.7:
                s.fill(x, F + 1, z, x, F + s.rng.randint(1, 3), z, ["minecraft:stone_bricks", "minecraft:cracked_stone_bricks"])
    s.chest(c - 4, top + 1, 5, L + "temple_khaine", "south"); s.chest(c + 4, top + 1, 5, L + "temple_khaine", "south")
    marqueur(s, c, F + 2, 34, "rm_amb_sang")
    s.mob(c, F + 1, 30, "zombie", "khaine_aelf", 6)
    s.mob(c - 9, top + 1, 12, "zombie", "khaine_aelf", 2)
    s.mob(c + 9, top + 1, 12, "zombie", "khaine_aelf", 2)
    return s


# =================================================================== IDONETH : temple antique sous-marin
def colonne(s, x, y, z, h, brisee=False):
    s.set(x, y, z, "minecraft:chiseled_quartz_block")
    top = y + h if not brisee else y + max(2, h // 2)
    s.fill(x, y + 1, z, x, top - 1, z, "minecraft:quartz_pillar")
    if not brisee:
        s.set(x, top, z, "minecraft:chiseled_quartz_block")


def ruines_idoneth():
    W = 55
    s = Struct(W, 36, W, 78)
    c = W // 2
    rng = s.rng
    # Fond marin et colline
    s.fill(0, 0, 0, W - 1, 1, W - 1, ["minecraft:sand", "minecraft:gravel", "minecraft:sand", "minecraft:prismarine"])
    for y in range(2, 8):
        r = 24 - (y - 2) * 3
        s.cylinder(c, c, r, y, y, ["minecraft:stone", "minecraft:prismarine", "minecraft:sand", "minecraft:mossy_cobblestone"], hollow=False)
    # Stylobate à degrés
    for i in range(3):
        s.fill(c - 12 + i, 8 + i, c - 8 + i, c + 12 - i, 8 + i, c + 8 - i, "minecraft:prismarine_bricks" if i < 2 else "minecraft:smooth_quartz")
    y0 = 11
    # Péristyle : colonnes sur tout le pourtour
    for x in range(c - 9, c + 10, 3):
        for z in (c - 5, c + 5):
            colonne(s, x, y0, z, 10, brisee=(rng.random() < 0.2))
    for z in range(c - 2, c + 3, 3):
        for x in (c - 9, c + 9):
            colonne(s, x, y0, z, 10)
    # Architrave, frise et fronton triangulaire
    s.fill(c - 10, y0 + 10, c - 6, c + 10, y0 + 10, c + 6, "minecraft:smooth_quartz")
    for x in range(c - 10, c + 11):
        s.set(x, y0 + 11, c - 6, "minecraft:prismarine_bricks" if x % 2 else "minecraft:dark_prismarine")
        s.set(x, y0 + 11, c + 6, "minecraft:prismarine_bricks" if x % 2 else "minecraft:dark_prismarine")
    s.roof_gable(c - 10, c - 6, c + 10, c + 6, y0 + 12, "minecraft:quartz_stairs", "minecraft:smooth_quartz", axis="x")
    for x in range(c - 3, c + 4):  # tympan orné
        s.set(x, y0 + 13, c + 7, "minecraft:dark_prismarine")
    s.set(c, y0 + 14, c + 7, "minecraft:sea_lantern")
    # Cella et statue de l'Eidolon (vague)
    s.walls(c - 6, y0, c - 3, c + 6, y0 + 9, c + 3, ["minecraft:prismarine_bricks", "minecraft:smooth_quartz"])
    s.clear(c - 1, y0, c + 3, c + 1, y0 + 4, c + 3)
    s.fill(c - 1, y0, c - 2, c + 1, y0 + 1, c - 1, "minecraft:dark_prismarine")
    for k in range(9):
        x = c + round(1.5 * math.sin(k * 0.7)); z = c - 1 + round(0.8 * math.cos(k * 0.7))
        s.set(x, y0 + 2 + k, z, "minecraft:light_blue_stained_glass" if k % 2 else "minecraft:cyan_stained_glass")
    s.set(c, y0 + 8, c - 1, "minecraft:sea_lantern")
    s.chest(c - 4, y0, c - 2, L + "ruines_idoneth", "south"); s.chest(c + 4, y0, c - 2, L + "ruines_idoneth", "south")
    # Colonnes brisées, stèles et rochers alentour
    for (x, z) in ((5, 6), (9, W - 8), (W - 7, 9), (W - 10, W - 6), (c, 4), (4, c + 4), (W - 5, c - 3)):
        colonne(s, x, 2, z, rng.randint(4, 9), brisee=rng.random() < 0.6)
        s.set(x + 1, 2, z, "minecraft:chiseled_quartz_block")
    for (x, z) in ((12, 12), (W - 13, W - 14), (14, W - 10)):
        s.fill(x, 2, z, x, 5, z + 1, "minecraft:smooth_quartz"); s.set(x, 6, z, "minecraft:quartz_slab")
    # Anguille géante (Allopex) qui s'enroule autour d'une colonne
    for k in range(40):
        a = k * 0.35
        x = 8 + round(4 * math.cos(a)); z = c + 14 + round(4 * math.sin(a))
        if 0 <= z < W:
            s.set(x, 3 + k // 3, z, "minecraft:dark_prismarine" if k % 4 else "minecraft:light_blue_stained_glass")
    # Coraux, herbiers et lumières
    for x in range(1, W - 1, 2):
        for z in range(1, W - 1, 2):
            if (x, 2, z) not in s.blocks and rng.random() < 0.25:
                s.set(x, 2, z, rng.choice(["minecraft:seagrass", "minecraft:tall_seagrass[half=lower]", "minecraft:tube_coral",
                                           "minecraft:brain_coral", "minecraft:sea_pickle[pickles=3]", "minecraft:kelp_plant"]))
    sous_marin(s)
    s.mob(c, y0, c + 9, "drowned", "idoneth", 4)
    s.mob(c - 8, 2, c - 12, "drowned", "idoneth", 3)
    return s


# =================================================================== HASHUT : ziggurat-cathédrale infernale
def ziggurat_hashut():
    W = 51
    s = base(W, 72, W, ["minecraft:polished_blackstone", "minecraft:blackstone", "minecraft:basalt"], "minecraft:blackstone", 79, haut=14)
    c = W // 2
    noir = ["minecraft:polished_blackstone_bricks", "minecraft:deepslate_bricks", "minecraft:polished_blackstone_bricks",
            "minecraft:cracked_polished_blackstone_bricks", "minecraft:deepslate_tiles"]
    y = F + 1
    demi = 20
    etage = 0
    while demi >= 6:
        h = 8
        s.fill(c - demi, y, c - demi, c + demi, y + h - 1, c + demi, noir)
        s.clear(c - demi + 2, y, c - demi + 2, c + demi - 2, y + h - 2, c + demi - 2)
        # fenêtres gothiques lumineuses (vert malsain et orangé)
        for k in range(-demi + 3, demi - 2, 4):
            for (xx, zz, ax) in ((c + k, c + demi, "x"), (c + k, c - demi, "x"), (c + demi, c + k, "z"), (c - demi, c + k, "z")):
                fenetre_arc(s, xx, y + 2, zz, ax, 3, "minecraft:lime_stained_glass_pane" if (k + etage) % 3 else "minecraft:orange_stained_glass_pane",
                            "minecraft:polished_blackstone_brick_stairs")
        # contreforts et têtes de taureau dorées aux angles
        for (sx, sz) in ((-1, -1), (1, -1), (-1, 1), (1, 1)):
            x, z = c + sx * demi, c + sz * demi
            s.fill(x, y, z, x, y + h + 1, z, "minecraft:polished_basalt")
            s.set(x, y + h + 2, z, "minecraft:campfire")
            s.set(x, y + h - 2, z + sz, "minecraft:gold_block")
            s.set(x + sx, y + h - 1, z + sz, "minecraft:gold_block")
        s.fill(c - demi, y + h, c - demi, c + demi, y + h, c + demi, "minecraft:polished_blackstone")
        y += h
        demi -= 4
        etage += 1
    top = y
    # Couronne de flammes au sommet
    s.fill(c - 3, top, c - 3, c + 3, top + 3, c + 3, "minecraft:gilded_blackstone")
    for (x, z) in cercle(c, c, 4, 30):
        s.fill(x, top, z, x, top + 4, z, "minecraft:polished_basalt")
        s.set(x, top + 5, z, "minecraft:netherrack"); s.set(x, top + 6, z, "minecraft:fire")
    s.fill(c - 1, top + 4, c - 1, c + 1, top + 4, c + 1, "minecraft:netherrack")
    s.fill(c - 1, top + 5, c - 1, c + 1, top + 5, c + 1, "minecraft:fire")
    # Taureau de Hashut sur la façade sud
    fz = c + 20
    s.fill(c - 3, F + 9, fz + 1, c + 3, F + 13, fz + 2, "minecraft:gold_block")
    s.set(c - 1, F + 12, fz + 3, "minecraft:magma_block"); s.set(c + 1, F + 12, fz + 3, "minecraft:magma_block")
    for side in (-1, 1):
        for k in range(4):
            s.set(c + side * (4 + k), F + 13 + k // 2, fz + 1, "minecraft:gold_block")
    # Grande porte
    s.clear(c - 2, F + 1, fz - 1, c + 2, F + 6, fz)
    for x in range(c - 2, c + 3):
        s.set(x, F + 7, fz, "minecraft:polished_blackstone_brick_stairs[facing=north,half=top]")
    # Douves de lave et tours de flammes
    for x in range(W):
        for z in range(W):
            d = max(abs(x - c), abs(z - c))
            if d in (22, 23) and not (abs(x - c) <= 2 and z > c):
                s.set(x, F, z, "minecraft:lava")
    for (x, z) in ((3, 3), (W - 4, 3), (3, W - 4), (W - 4, W - 4)):
        s.cylinder(x, z, 2, F + 1, F + 22, noir)
        s.set(x, F + 23, z, "minecraft:netherrack"); s.set(x, F + 24, z, "minecraft:fire")
    # Forge intérieure, cages
    s.disk(c, c, 3, F, "minecraft:magma_block"); s.set(c, F, c, "minecraft:lava")
    s.set(c - 4, F + 1, c - 4, "minecraft:blast_furnace[facing=south]"); s.set(c + 4, F + 1, c - 4, "minecraft:anvil")
    s.chest(c - 3, F + 1, c - 5, L + "ziggurat_hashut", "south"); s.chest(c + 3, F + 1, c - 5, L + "ziggurat_hashut", "south")
    s.walls(c + 10, F + 1, c - 4, c + 14, F + 3, c + 4, "minecraft:iron_bars")
    s.mob(c + 12, F + 1, c, "villager", "habitant")
    marqueur(s, c, top + 3, c, "rm_amb_braise")
    s.mob(c, F + 1, c + 8, "zombie", "hashut", 4)
    s.mob(c, F + 9, c, "skeleton", "hashut_tireur", 2)
    s.mob(c, top, c + 4, "skeleton", "hashut_tireur", 2)
    return s


# =================================================================== SKAVEN : repaire de Skavenblight
def repaire_skavenblight():
    W = 57
    s = Struct(W, 64, W, 80)
    c = W // 2
    rng = s.rng
    pourri = ["minecraft:cobblestone", "minecraft:mossy_cobblestone", "minecraft:cracked_stone_bricks", "minecraft:stone_bricks",
              "minecraft:tuff_bricks", "minecraft:cobbled_deepslate"]
    s.fill(0, 0, 0, W - 1, 3, W - 1, ["minecraft:mud", "minecraft:coarse_dirt", "minecraft:gravel", "minecraft:cobblestone"])
    # Canal toxique (vert) traversant le repaire
    for x in range(W):
        z0 = c + int(5 * math.sin(x * 0.18))
        for dz in range(-3, 4):
            s.set(x, 3, z0 + dz, "minecraft:water"); s.set(x, 2, z0 + dz, "minecraft:lime_stained_glass")
            if rng.random() < 0.08:
                s.set(x, 3, z0 + dz, "minecraft:slime_block")
    # Tours en ruine reliées par des ponts branlants
    tours = [(9, 10, 30), (W - 11, 9, 24), (10, W - 11, 22), (W - 10, W - 10, 34)]
    for (x, z, h) in tours:
        for y in range(4, 4 + h):
            off = (y - 4) // 9
            r = 4 if y < 4 + h - 8 else 3
            s.cylinder(x + off, z, r, y, y, pourri + ["minecraft:air"] if y > 4 + h - 6 else pourri, hollow=True, inside="minecraft:air")
            if y % 7 == 0:
                s.disk(x + off, z, r - 1, y, "minecraft:spruce_planks")
            if y % 6 == 3:
                s.set(x + off + r, y, z, "minecraft:verdant_froglight")
        off = h // 9
        s.fill(x + off - 3, 4 + h, z - 3, x + off + 3, 4 + h, z + 3, "minecraft:spruce_planks")
        for (dx, dz) in ((-3, -3), (3, -3), (-3, 3), (3, 3)):
            s.fill(x + off + dx, 5 + h, z + dz, x + off + dx, 7 + h, z + dz, "minecraft:spruce_fence")
        s.cone(x + off, z, 3, 8 + h, ["minecraft:spruce_planks", "minecraft:dark_oak_planks", "minecraft:air"])
        for y in range(4, 4 + h):
            s.set(x + (y - 4) // 9 - 2, y, z, "minecraft:ladder[facing=east]")
    for i in range(len(tours)):
        (x1, z1, h1), (x2, z2, h2) = tours[i], tours[(i + 1) % len(tours)]
        y = 4 + min(h1, h2) - 4
        n = int(math.hypot(x2 - x1, z2 - z1))
        for k in range(n + 1):
            t = k / n
            x = round(x1 + (x2 - x1) * t); z = round(z1 + (z2 - z1) * t)
            yy = y - round(3 * math.sin(math.pi * t))
            if rng.random() < 0.88:
                s.set(x, yy, z, "minecraft:spruce_slab")
            if k % 3 == 0:
                s.set(x, yy + 1, z, "minecraft:spruce_fence")
    # Générateur de malefoudre : flèche centrale à bobines de cuivre
    s.cylinder(c, c, 3, 4, 12, ["minecraft:waxed_weathered_copper", "minecraft:waxed_oxidized_copper", "minecraft:cobblestone"])
    for y in range(12, 44):
        r = 2 if y < 30 else 1
        s.cylinder(c, c, r, y, y, ["minecraft:cobblestone", "minecraft:stone_bricks", "minecraft:waxed_copper_grate"], hollow=False)
        if y % 4 == 0:
            s.cylinder(c, c, r + 1, y, y, "minecraft:waxed_weathered_cut_copper", hollow=True, inside=None)
        if y % 6 == 0:
            s.set(c + r, y, c, "minecraft:verdant_froglight"); s.set(c - r, y, c, "minecraft:verdant_froglight")
    s.fill(c, 44, c, c, 47, c, "minecraft:lightning_rod")
    marqueur(s, c, 48, c, "rm_foudre", "rm_malefoudre")
    # Sphère de cuivre (globe) et tuyaux
    gx, gz = W - 15, c + 12
    for x in range(gx - 4, gx + 5):
        for y in range(4, 13):
            for z in range(gz - 4, gz + 5):
                d = (x - gx) ** 2 + (y - 8) ** 2 + (z - gz) ** 2
                if 12 <= d <= 18:
                    s.set(x, y, z, "minecraft:waxed_exposed_copper" if (x + y) % 3 else "minecraft:waxed_copper_bulb[lit=true]")
    for x in range(c + 3, gx - 3):
        s.set(x, 9, gz - 2, "minecraft:waxed_copper_grate")
    # Cloche hurlante et tas de malepierre
    s.fill(c - 14, 4, c + 14, c - 14, 14, c + 14, "minecraft:spruce_log")
    s.fill(c - 14, 15, c + 14, c - 10, 15, c + 14, "minecraft:spruce_log[axis=x]")
    s.set(c - 10, 14, c + 14, "minecraft:bell[attachment=ceiling]")
    for (x, z) in ((c + 6, c - 8), (c - 7, c - 9), (c + 10, c + 3)):
        for y in range(4, 4 + rng.randint(2, 5)):
            s.set(x, y, z, "minecraft:verdant_froglight")
        s.set(x + 1, 4, z, "minecraft:lime_stained_glass")
    s.chest(c - 3, 4, c - 4, L + "repaire_skaven", "south"); s.chest(c + 3, 4, c + 4, L + "repaire_skaven", "north")
    marqueur(s, c, 6, c + 8, "rm_amb_malepierre")
    s.mob(c - 4, 4, c - 6, "zombie", "clanrat", 6)
    s.mob(c + 6, 4, c - 10, "zombie", "clanrat", 4)
    s.mob(9, 20, 10, "skeleton", "jezzail", 2)
    return s


# =================================================================== OSSIARCH : ossuaire des âmes
def ossuaire_ossiarch():
    s = S3.ossuaire_ossiarch()
    W = s.size[0]
    c = W // 2
    # Douves de feu d'âmes
    for x in range(1, W - 1):
        for z in (1, W - 2):
            s.set(x, S3.F, z, "minecraft:soul_soil"); s.set(x, S3.F + 1, z, "minecraft:soul_fire")
    for z in range(1, W - 1):
        for x in (1, W - 2):
            s.set(x, S3.F, z, "minecraft:soul_soil"); s.set(x, S3.F + 1, z, "minecraft:soul_fire")
    s.clear(c - 2, S3.F + 1, W - 2, c + 2, S3.F + 1, W - 2)
    s.fill(c - 2, S3.F, W - 2, c + 2, S3.F, W - 2, "minecraft:bone_block")
    # Obélisque des âmes : os, verre bleu et feu d'âme
    ox, oz = c, c + 12
    s.fill(ox - 1, S3.F + 1, oz - 1, ox + 1, S3.F + 2, oz + 1, "minecraft:bone_block")
    for y in range(S3.F + 3, S3.F + 16):
        s.set(ox, y, oz, "minecraft:light_blue_stained_glass" if y % 3 else "minecraft:bone_block[axis=y]")
        if y % 4 == 0:
            for (dx, dz) in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                s.set(ox + dx, y, oz + dz, "minecraft:soul_lantern")
    s.set(ox, S3.F + 16, oz, "minecraft:soul_campfire[signal_fire=true]")
    # Braseros d'âmes, vitraux bleus, sculk
    for (x, z) in cercle(c, c + 12, 6, 45):
        s.fill(x, S3.F + 1, z, x, S3.F + 2, z, "minecraft:bone_block[axis=y]")
        s.set(x, S3.F + 3, z, "minecraft:soul_campfire")
    for x in range(6, W - 6, 4):
        s.set(x, S3.F + 4, 3, "minecraft:light_blue_stained_glass_pane"); s.set(x, S3.F + 4, W - 4, "minecraft:light_blue_stained_glass_pane")
    for x in range(5, W - 5):
        for z in range(5, W - 5):
            if s.get(x, S3.F, z) and s.rng.random() < 0.06 and abs(x - c) > 10:
                s.set(x, S3.F, z, "minecraft:sculk")
    marqueur(s, ox, S3.F + 8, oz, "rm_amb_ames")
    marqueur(s, c, S3.F + 3, c, "rm_amb_ames")
    return s


# =================================================================== ROTIGUS : jardin putride
def jardin_rotigus():
    W = 51
    s = Struct(W, 40, W, 81)
    c = W // 2
    rng = s.rng
    sol = ["minecraft:mud", "minecraft:mycelium", "minecraft:moss_block", "minecraft:mud", "minecraft:lime_concrete_powder",
           "minecraft:podzol", "minecraft:slime_block", "minecraft:muddy_mangrove_roots"]
    s.fill(0, 0, 0, W - 1, 3, W - 1, sol)
    for (x, z, r) in ((8, 10, 5), (W - 10, 8, 4), (c - 14, W - 10, 6), (W - 9, W - 12, 5), (c + 3, c - 16, 3)):
        s.disk(x, z, r, 3, "minecraft:water"); s.disk(x, z, r, 2, "minecraft:lime_stained_glass")
        for k in range(r):
            s.set(x + rng.randint(-r + 1, r - 1), 4, z + rng.randint(-r + 1, r - 1), "minecraft:lily_pad")
    # Chaudron de Grand-Père : immense, bouillonnant, verdâtre
    s.cylinder(c, c, 8, 4, 10, ["minecraft:waxed_oxidized_copper", "minecraft:waxed_weathered_copper", "minecraft:mossy_cobblestone",
                                 "minecraft:waxed_oxidized_cut_copper"], hollow=True, inside="minecraft:water")
    s.disk(c, c, 7, 3, "minecraft:lime_stained_glass")
    s.disk(c, c, 7, 2, "minecraft:magma_block")
    for (x, z) in cercle(c, c, 9, 30):
        s.set(x, 4, z, "minecraft:campfire")
    for (x, z) in cercle(c, c, 8, 45):
        s.fill(x, 11, z, x, 12, z, "minecraft:slime_block")
    # Pustules géantes
    for (x, z, r) in ((12, c, 3), (W - 12, c + 4, 4), (c - 6, 8, 3), (c + 10, W - 7, 3)):
        for y in range(4, 4 + r + 1):
            rr = int(math.sqrt(max(0, r * r - (y - 4) ** 2)))
            s.cylinder(x, z, rr, y, y, ["minecraft:lime_terracotta", "minecraft:green_terracotta", "minecraft:slime_block", "minecraft:moss_block"],
                       hollow=False)
        s.set(x, 4 + r + 1, z, "minecraft:slime_block")
    # Arbres pourrissants aux cosses suintantes
    for (x, z) in ((5, 5), (W - 6, 5), (5, W - 6), (W - 6, W - 6), (c, W - 4)):
        h = rng.randint(8, 12)
        for y in range(4, 4 + h):
            s.set(x, y, z, rng.choice(["minecraft:mangrove_log", "minecraft:muddy_mangrove_roots", "minecraft:mangrove_wood"]))
        for (dx, dz) in ((2, 0), (-2, 0), (0, 2), (0, -2)):
            s.set(x + dx // 2, 4 + h - 2, z + dz // 2, "minecraft:mangrove_wood")
            s.set(x + dx, 4 + h - 2, z + dz, "minecraft:mangrove_roots")
            for k in range(rng.randint(1, 3)):
                s.set(x + dx, 4 + h - 3 - k, z + dz, "minecraft:pale_hanging_moss")
            s.set(x + dx, 4 + h - 4, z + dz, "minecraft:slime_block") if rng.random() < 0.5 else None
        s.cylinder(x, z, 2, 4 + h, 4 + h, ["minecraft:moss_block", "minecraft:mangrove_roots", "minecraft:brown_mushroom_block"], hollow=False)
    # Arbre abattu couvert de champignons
    for x in range(c - 18, c - 8):
        s.set(x, 4, c + 12, "minecraft:mangrove_log[axis=x]")
        if x % 2 == 0:
            s.set(x, 5, c + 12, rng.choice(["minecraft:brown_mushroom", "minecraft:red_mushroom"]))
    # Charognes et cloches de peste
    for (x, z) in ((c + 14, c - 8), (c - 15, c - 5), (c + 6, c + 15)):
        s.fill(x - 1, 4, z - 1, x + 1, 4, z + 1, ["minecraft:bone_block", "minecraft:nether_wart_block", "minecraft:red_mushroom_block"])
        s.set(x, 5, z, "minecraft:nether_wart_block"); s.set(x, 6, z, "minecraft:skeleton_skull")
    for (x, z) in ((c - 10, c + 2), (c + 12, c + 10), (c - 2, c - 12)):
        s.fill(x, 4, z, x, 9, z, "minecraft:dark_oak_fence")
        s.set(x + 1, 9, z, "minecraft:dark_oak_fence"); s.set(x + 1, 8, z, "minecraft:bell[attachment=ceiling]")
    # Tapis de moisissure
    for x in range(W):
        for z in range(W):
            if (x, 4, z) not in s.blocks and rng.random() < 0.18:
                s.set(x, 4, z, rng.choice(["minecraft:moss_carpet", "minecraft:brown_mushroom", "minecraft:red_mushroom", "minecraft:short_grass",
                                           "minecraft:leaf_litter[segment_amount=3]"]))
    s.chest(c - 9, 4, c - 10, L + "fort_kruleboyz", "south"); s.chest(c + 9, 4, c + 10, L + "fort_kruleboyz", "north")
    marqueur(s, c, 11, c, "rm_amb_peste")
    marqueur(s, 12, 6, c, "rm_amb_peste")
    s.mob(c, 4, c + 13, "zombie", "boss_rotigus")
    s.mob(c - 6, 4, c + 14, "zombie", "pestigor", 4)
    return s


BUILDERS4 = {
    "forteresse_stormcast": forteresse_stormcast, "temple_seraphon": temple_seraphon, "camp_orruk": camp_orruk,
    "antre_gitz": antre_gitz, "bosquet_sylvaneth": bosquet_sylvaneth, "magmahold": magmahold, "port_kharadron": port_kharadron,
    "sanctuaire_lumineth": sanctuaire_lumineth, "temple_khaine": temple_khaine, "ruines_idoneth": ruines_idoneth,
    "ziggurat_hashut": ziggurat_hashut, "repaire_skavenblight": repaire_skavenblight, "ossuaire_ossiarch": ossuaire_ossiarch,
    "jardin_rotigus": jardin_rotigus,
}
START4 = {"forteresse_stormcast": -1, "temple_seraphon": -F, "camp_orruk": -F, "antre_gitz": -3, "bosquet_sylvaneth": -F,
          "magmahold": -12, "port_kharadron": -1, "sanctuaire_lumineth": 22, "temple_khaine": -F, "ruines_idoneth": -2,
          "ziggurat_hashut": -F, "repaire_skavenblight": -3, "ossuaire_ossiarch": -F, "jardin_rotigus": -3}


# =================================================================== DÉCORS v4
G = 3


def S_(w, h, seed):
    return Struct(w, h, w, seed)


def volcan():
    s = S_(33, 30, 201); c = 16
    rng = s.rng
    for y in range(0, 26):
        r = int(16 - y * 0.55)
        for x in range(c - r, c + r + 1):
            for z in range(c - r, c + r + 1):
                d = math.hypot(x - c, z - c)
                if d <= r - 0.3 + math.sin(x + z) * 0.6:
                    s.set(x, y, z, rng.choice(["minecraft:basalt", "minecraft:blackstone", "minecraft:smooth_basalt", "minecraft:tuff",
                                               "minecraft:magma_block"]) if d > r - 2 else "minecraft:blackstone")
    for y in range(18, 26):
        rr = 2 + (y - 18) // 2
        s.cylinder(c, c, rr, y, y, "minecraft:air", hollow=False)
    s.disk(c, c, 3, 18, "minecraft:lava")
    for k in range(4):  # coulées de lave
        a = k * math.pi / 2 + 0.4
        for i in range(4, 15):
            x = c + round(i * math.cos(a)); z = c + round(i * math.sin(a))
            y = max(G, 24 - int(i * 1.4))
            if s.get(x, y, z):
                s.set(x, y + 1, z, "minecraft:lava") if i in (4, 9) else s.set(x, y, z, "minecraft:magma_block")
    return s


def chute_lave():
    s = S_(11, 20, 202); c = 5
    for y in range(0, 17):
        r = 4 if y < 10 else 3
        s.cylinder(c, c, r, y, y, ["minecraft:basalt", "minecraft:blackstone", "minecraft:tuff"], hollow=False)
    s.set(c, 17, c, "minecraft:lava")
    for y in range(G + 1, 17):
        s.set(c + 4, y, c, "minecraft:lava") if y == 16 else None
    s.set(c + 3, 16, c, "minecraft:lava")
    s.disk(c, c, 5, G, ["minecraft:magma_block", "minecraft:basalt"])
    return s


def arbre_wyldwood_a():
    s = S_(17, 22, 203)
    s.fill(7, 0, 7, 9, G, 9, "minecraft:dirt")
    arbre_wyldwood(s, 8, G + 1, 8, h=11, seed=7)
    return s


def arbre_wyldwood_b():
    s = S_(19, 24, 204)
    s.fill(8, 0, 8, 10, G, 10, "minecraft:dirt")
    arbre_wyldwood(s, 9, G + 1, 9, h=14, seed=19)
    return s


def pilier_lueur():
    s = S_(5, 14, 205); c = 2
    s.fill(1, 0, 1, 3, G, 3, "minecraft:mud")
    for y in range(G + 1, G + 9):
        s.set(c, y, c, s.rng.choice(["minecraft:lime_stained_glass", "minecraft:green_stained_glass", "minecraft:verdant_froglight"]))
    s.set(c + 1, G + 1, c, "minecraft:verdant_froglight"); s.set(c - 1, G + 1, c + 1, "minecraft:lime_stained_glass")
    marqueur(s, c, G + 3, c, "rm_amb_lueur")
    return s


def idole_lune():
    s = S_(15, 22, 206); c = 7
    s.fill(c - 1, 0, c - 1, c + 1, G, c + 1, "minecraft:cobbled_deepslate")
    s.fill(c, G + 1, c, c, G + 8, c, "minecraft:mushroom_stem")
    croissant(s, c, G + 14, c, r=6)
    s.set(c - 2, G + 13, c + 1, "minecraft:black_concrete"); s.set(c - 1, G + 15, c + 1, "minecraft:red_concrete")
    return s


def ilot_flottant():
    s = S_(15, 22, 207); c = 7
    rng = s.rng
    for y in range(0, 9):
        r = int(1 + (y / 8) * 6)
        s.cylinder(c, c, r, y, y, ["minecraft:stone", "minecraft:calcite", "minecraft:diorite", "minecraft:dirt"], hollow=False)
    s.disk(c, c, 7, 8, "minecraft:grass_block")
    s.fill(c, 9, c, c, 13, c, "minecraft:white_stained_glass"); s.set(c, 14, c, "minecraft:end_rod")
    s.set(c + 3, 9, c, "minecraft:lily_of_the_valley"); s.set(c - 2, 9, c + 2, "minecraft:white_tulip")
    for (x, z) in cercle(c, c, 4, 60):
        s.set(x, 0 + rng.randint(1, 3), z, "minecraft:hanging_roots")
    return s


DECOS4 = {
    "volcan": (volcan, ["aqshy_volcans"], 7),
    "chute_lave": (chute_lave, ["aqshy_volcans", "aqshy_cendres"], 10),
    "arbre_wyldwood_a": (arbre_wyldwood_a, ["ghyran_wyldwood", "ghyran_jade"], 2),
    "arbre_wyldwood_b": (arbre_wyldwood_b, ["ghyran_wyldwood"], 3),
    "pilier_lueur": (pilier_lueur, ["ulgu_marais_lune"], 3),
    "idole_lune": (idole_lune, ["ulgu_marais_lune", "ulgu_brumes"], 12),
}
DECOS_FLOTTANTS = {"ilot_flottant": (ilot_flottant, ["hysh_plateaux", "hysh_iles", "azyr_cimes"], 6)}
