# -*- coding: utf-8 -*-
"""Petites constructions posées comme décorations de biome (feature « template »).
Chaque gabarit est centré ; G = niveau du sol dans le gabarit (les couches dessous servent de fondations)."""
import math
from nbtgen import Struct
from details import statue_guerrier, lustre

G = 3
L = "royaumes:coffres/"


def S(w, h, seed):
    return Struct(w, h, w, seed)


def socle(s, x0, z0, x1, z1, bloc):
    s.fill(x0, 0, z0, x1, G, z1, bloc)


def ruine(s, p):
    """Effondre aléatoirement une partie des blocs hauts (aspect ruiné)."""
    for (x, y, z), (st, nbt) in list(s.blocks.items()):
        if y > G + 1 and nbt is None and s.rng.random() < p * (y - G) / s.size[1] * 2:
            del s.blocks[(x, y, z)]


# ------------------------------------------------------------------- AZYR / HYSH
def statue_stormcast():
    s = S(7, 16, 101); c = 3
    socle(s, 1, 1, 5, 5, "minecraft:quartz_bricks")
    s.fill(1, G + 1, 1, 5, G + 1, 5, "minecraft:smooth_quartz")
    s.fill(0, G, 0, 6, G, 6, "minecraft:quartz_bricks")
    statue_guerrier(s, c, G + 2, c, "minecraft:gold_block", "minecraft:lapis_block", "minecraft:lightning_rod", "minecraft:quartz_bricks")
    for (x, z) in ((0, 0), (6, 0), (0, 6), (6, 6)):
        s.set(x, G + 1, z, "minecraft:diorite_wall"); s.set(x, G + 2, z, "minecraft:lantern")
    return s


def autel_celeste():
    s = S(9, 10, 102); c = 4
    socle(s, 0, 0, 8, 8, "minecraft:stone_bricks")
    s.disk(c, c, 4, G, ["minecraft:smooth_quartz", "minecraft:calcite"])
    s.disk(c, c, 2, G + 1, "minecraft:lapis_block")
    s.set(c, G + 2, c, "minecraft:gold_block"); s.set(c, G + 3, c, "minecraft:lightning_rod")
    for a in range(0, 360, 45):
        x = c + round(4 * math.cos(math.radians(a))); z = c + round(4 * math.sin(math.radians(a)))
        s.fill(x, G + 1, z, x, G + 3, z, "minecraft:quartz_pillar")
        s.set(x, G + 4, z, "minecraft:sea_lantern")
    s.chest(c + 1, G + 2, c, L + "forteresse_stormcast", "west")
    return s


def tour_guet_quartz():
    s = S(9, 20, 103); c = 4
    socle(s, 1, 1, 7, 7, "minecraft:stone_bricks")
    s.cylinder(c, c, 3, G, G + 13, ["minecraft:quartz_bricks", "minecraft:smooth_quartz", "minecraft:calcite"])
    s.clear(c, G + 1, c + 3, c, G + 2, c + 3)
    for y in range(G + 1, G + 13):
        s.set(c - 2, y, c, "minecraft:ladder[facing=east]")
    s.disk(c, c, 4, G + 13, "minecraft:smooth_quartz_slab")
    s.disk(c, c, 2, G + 13, "minecraft:smooth_quartz")
    s.set(c - 2, G + 13, c, "minecraft:ladder[facing=east]")
    for a in range(0, 360, 45):
        s.set(c + round(4 * math.cos(math.radians(a))), G + 14, c + round(4 * math.sin(math.radians(a))), "minecraft:diorite_wall")
    s.set(c, G + 14, c, "minecraft:blue_banner[rotation=0]")
    ruine(s, 0.25)
    return s


def cristal_hysh():
    s = S(9, 18, 104); c = 4
    socle(s, 2, 2, 6, 6, "minecraft:calcite")
    for (dx, dz, h) in ((0, 0, 12), (1, 0, 8), (-1, 1, 7), (0, -1, 9), (1, 1, 5), (-1, -1, 6)):
        for y in range(G + 1, G + h):
            s.set(c + dx, y, c + dz, "minecraft:white_stained_glass" if y % 3 else "minecraft:quartz_block")
        s.set(c + dx, G + h, c + dz, "minecraft:end_rod")
    s.disk(c, c, 3, G, ["minecraft:calcite", "minecraft:smooth_quartz"])
    s.set(c + 2, G + 1, c + 2, "minecraft:amethyst_cluster")
    s.set(c - 2, G + 1, c - 2, "minecraft:amethyst_cluster")
    return s


def arche_lumineth():
    s = S(11, 15, 105); c = 5
    for x in (1, 9):
        socle(s, x, c - 1, x, c + 1, "minecraft:calcite")
        s.fill(x, G + 1, c, x, G + 7, c, "minecraft:quartz_pillar")
    for x in range(1, 10):
        y = G + 8 + (1 if 3 <= x <= 7 else 0)
        s.set(x, y, c, "minecraft:smooth_quartz")
    s.set(2, G + 7, c, "minecraft:quartz_stairs[facing=west,half=top]")
    s.set(8, G + 7, c, "minecraft:quartz_stairs[facing=east,half=top]")
    s.set(c, G + 10, c, "minecraft:end_rod")
    s.set(c, G + 8, c, "minecraft:sea_lantern")
    return s


# ------------------------------------------------------------------- GHYRAN
def arbre_esprit():
    s = S(21, 34, 106); c = 10
    socle(s, c - 3, c - 3, c + 3, c + 3, "minecraft:dirt")
    # racines rampantes
    for a in range(0, 360, 60):
        for r in range(2, 8):
            x = c + round(r * math.cos(math.radians(a))); z = c + round(r * math.sin(math.radians(a)))
            s.set(x, G - (1 if r > 5 else 0), z, "minecraft:oak_wood")
            if r < 4:
                s.set(x, G + 1, z, "minecraft:oak_wood")
    # tronc
    for y in range(G, G + 18):
        r = 3 if y < G + 6 else 2
        s.cylinder(c, c, r, y, y, ["minecraft:oak_wood", "minecraft:oak_wood", "minecraft:moss_block"], hollow=False)
    # branches
    for a in range(0, 360, 72):
        for r in range(2, 7):
            x = c + round(r * math.cos(math.radians(a))); z = c + round(r * math.sin(math.radians(a)))
            s.set(x, G + 14 + r // 2, z, "minecraft:oak_wood")
    # canopée
    for y in range(G + 16, G + 27):
        r = 9 - abs(y - (G + 20))
        s.cylinder(c, c, max(r, 3), y, y, ["minecraft:azalea_leaves[persistent=true]", "minecraft:flowering_azalea_leaves[persistent=true]",
                                          "minecraft:oak_leaves[persistent=true]"], hollow=False)
    for (dx, dz) in ((-4, 0), (4, 0), (0, -4), (0, 4), (3, 3), (-3, -3)):
        s.set(c + dx, G + 15, c + dz, "minecraft:shroomlight")
    # lianes lumineuses
    for (dx, dz) in ((-6, 2), (5, -5), (2, 7), (-5, -5)):
        for y in range(G + 12, G + 16):
            s.set(c + dx, y, c + dz, "minecraft:cave_vines_plant[berries=true]")
        s.set(c + dx, G + 11, c + dz, "minecraft:cave_vines[berries=true]")
    return s


def cercle_pierres():
    s = S(15, 8, 107); c = 7
    for a in range(0, 360, 36):
        x = c + round(6 * math.cos(math.radians(a))); z = c + round(6 * math.sin(math.radians(a)))
        h = 2 + (a // 36) % 3
        s.fill(x, 0, z, x, G + h, z, ["minecraft:mossy_cobblestone", "minecraft:mossy_stone_bricks", "minecraft:stone"])
        s.set(x, G + h + 1, z, "minecraft:moss_carpet")
    s.fill(c - 1, 0, c - 1, c + 1, G, c + 1, "minecraft:mossy_stone_bricks")
    s.set(c, G + 1, c, "minecraft:flowering_azalea")
    return s


def sanctuaire_alarielle():
    s = S(9, 10, 108); c = 4
    socle(s, 0, 0, 8, 8, "minecraft:mossy_stone_bricks")
    s.fill(0, G, 0, 8, G, 8, ["minecraft:moss_block", "minecraft:mossy_stone_bricks"])
    for (x, z) in ((1, 1), (7, 1), (1, 7), (7, 7)):
        s.fill(x, G + 1, z, x, G + 5, z, "minecraft:stripped_birch_log")
        s.set(x, G + 6, z, "minecraft:flowering_azalea_leaves[persistent=true]")
    s.fill(1, G + 6, 1, 7, G + 6, 7, "minecraft:flowering_azalea_leaves[persistent=true]")
    s.fill(2, G + 6, 2, 6, G + 6, 6, "minecraft:air")
    s.set(c, G + 1, c, "minecraft:mossy_stone_bricks"); s.set(c, G + 2, c, "minecraft:potted_flowering_azalea_bush")
    for (x, z) in ((2, c), (6, c), (c, 2), (c, 6)):
        s.set(x, G + 1, z, s.rng.choice(["minecraft:lily_of_the_valley", "minecraft:allium", "minecraft:blue_orchid"]))
    s.chest(c, G + 1, c + 1, L + "bosquet_sylvaneth", "south")
    return s


def totem_kruleboyz():
    s = S(7, 12, 109); c = 3
    socle(s, 2, 2, 4, 4, "minecraft:mud")
    s.fill(c, G + 1, c, c, G + 8, c, "minecraft:mangrove_log")
    s.fill(c - 2, G + 6, c, c + 2, G + 6, c, "minecraft:mangrove_log[axis=x]")
    for (x, y) in ((c - 2, G + 7), (c + 2, G + 7), (c, G + 9)):
        s.set(x, y, c, "minecraft:skeleton_skull")
    s.set(c - 2, G + 5, c, "minecraft:iron_chain"); s.set(c - 2, G + 4, c, "minecraft:zombie_head")
    s.set(c + 2, G + 5, c, "minecraft:iron_chain"); s.set(c + 2, G + 4, c, "minecraft:lantern[hanging=true]")
    s.set(c, G + 1, c + 1, "minecraft:green_banner[rotation=8]")
    return s


def hutte_pilotis():
    s = S(11, 14, 110); c = 5
    for (x, z) in ((2, 2), (8, 2), (2, 8), (8, 8)):
        s.fill(x, 0, z, x, G + 3, z, "minecraft:mangrove_log")
    s.fill(1, G + 3, 1, 9, G + 3, 9, "minecraft:mangrove_planks")
    s.hollow(2, G + 3, 2, 8, G + 7, 8, ["minecraft:mud_bricks", "minecraft:mangrove_roots", "minecraft:packed_mud"])
    s.cone(c, c, 5, G + 8, ["minecraft:hay_block", "minecraft:mangrove_roots"])
    s.clear(c, G + 4, 8, c, G + 5, 8)
    for y in range(G - 1, G + 3):
        s.set(c, y, 9, "minecraft:ladder[facing=south]")
    s.set(c, G + 4, 9, "minecraft:air")
    s.set(3, G + 4, 3, "minecraft:cauldron"); s.barrel(7, G + 4, 3, L + "fort_kruleboyz")
    s.set(c, G + 6, c, "minecraft:lantern[hanging=true]")
    s.mob(c, G + 4, c, "zombie", "gutrippa")
    return s


def chaudron_nurgle():
    s = S(9, 8, 111); c = 4
    socle(s, 1, 1, 7, 7, "minecraft:mud")
    s.disk(c, c, 4, G, ["minecraft:moss_block", "minecraft:mud", "minecraft:slime_block"])
    s.cylinder(c, c, 2, G + 1, G + 1, "minecraft:mossy_cobblestone", hollow=True, inside="minecraft:water")
    s.set(c, G + 1, c, "minecraft:water")
    s.set(c, G, c, "minecraft:magma_block")
    for (x, z) in ((0, c), (8, c), (c, 0), (c, 8)):
        s.set(x, G + 1, z, "minecraft:mossy_cobblestone_wall"); s.set(x, G + 2, z, "minecraft:skeleton_skull")
    s.set(c + 3, G + 1, c + 3, "minecraft:brown_mushroom"); s.set(c - 3, G + 1, c + 2, "minecraft:red_mushroom")
    return s


# ------------------------------------------------------------------- GHUR
def squelette_bete():
    s = S(23, 14, 112); c = 11
    # colonne vertébrale
    for x in range(2, 21):
        y = G + 6 + round(1.5 * math.sin((x - 2) / 18 * math.pi))
        s.set(x, y, c, "minecraft:bone_block[axis=x]")
    # côtes
    for x in range(6, 17, 2):
        top = G + 6 + round(1.5 * math.sin((x - 2) / 18 * math.pi))
        for side in (-1, 1):
            for k in range(1, 8):
                z = c + side * round(5 * math.sin(k / 7 * math.pi / 1.4))
                yy = top - k + 1
                if yy >= G - 1:
                    s.set(x, yy, z, "minecraft:bone_block[axis=y]")
    # crâne
    s.fill(18, G + 5, c - 2, 21, G + 8, c + 2, "minecraft:bone_block")
    s.fill(19, G + 6, c - 1, 21, G + 7, c + 1, "minecraft:air")
    s.set(21, G + 7, c - 2, "minecraft:air"); s.set(21, G + 7, c + 2, "minecraft:air")
    for z in (c - 2, c + 2):
        s.fill(22, G + 4, z, 22, G + 6, z, "minecraft:bone_block[axis=y]")
    # défenses
    s.fill(20, G + 2, c - 3, 20, G + 5, c - 3, "minecraft:bone_block[axis=y]")
    s.fill(20, G + 2, c + 3, 20, G + 5, c + 3, "minecraft:bone_block[axis=y]")
    return s


def menhir_orruk():
    s = S(7, 14, 113); c = 3
    socle(s, 1, 1, 5, 5, "minecraft:stone")
    s.fill(2, G + 1, 2, 4, G + 7, 4, ["minecraft:stone", "minecraft:andesite", "minecraft:cobblestone"])
    s.fill(c, G + 8, c, c, G + 10, c, "minecraft:stone")
    for y in (G + 3, G + 6):
        s.set(c, y, 1, "minecraft:red_terracotta")
        s.set(c - 1, y + 1, 1, "minecraft:red_terracotta"); s.set(c + 1, y + 1, 1, "minecraft:red_terracotta")
    s.set(c, G + 11, c, "minecraft:skeleton_skull")
    s.set(c + 2, G + 1, c, "minecraft:campfire")
    return s


def campement_ruine():
    s = S(13, 8, 114); c = 6
    socle(s, 2, 2, 10, 10, "minecraft:coarse_dirt")
    s.fill(0, G, 0, 12, G, 12, ["minecraft:coarse_dirt", "minecraft:dirt_path", "minecraft:grass_block"])
    s.set(c, G + 1, c, "minecraft:campfire[lit=false]")
    for i in range(3):
        s.fill(2 + i, G + 1 + i, 2, 6 - i, G + 1 + i, 5, "minecraft:brown_wool")
    s.clear(3, G + 1, 2, 5, G + 2, 5)
    s.fill(3, G + 1, 3, 5, G + 1, 4, "minecraft:air")
    s.set(9, G + 1, 9, "minecraft:bone_block"); s.set(9, G + 2, 9, "minecraft:skeleton_skull")
    s.barrel(8, G + 1, 3, L + "camp_orruk")
    s.set(10, G + 1, 7, "minecraft:spruce_log[axis=x]"); s.set(9, G + 1, 7, "minecraft:spruce_log[axis=x]")
    return s


def stele_seraphon():
    s = S(9, 12, 115); c = 4
    socle(s, 1, 1, 7, 7, "minecraft:mossy_stone_bricks")
    s.pyramid(1, 1, 7, 7, G, ["minecraft:mossy_stone_bricks", "minecraft:mossy_cobblestone"])
    s.fill(c, G + 3, c, c, G + 7, c, "minecraft:chiseled_stone_bricks")
    s.set(c, G + 8, c, "minecraft:gold_block")
    s.set(c, G + 5, c - 1, "minecraft:gold_block"); s.set(c, G + 5, c + 1, "minecraft:gold_block")
    s.set(c - 1, G + 3, c, "minecraft:lantern"); s.set(c + 1, G + 3, c, "minecraft:lantern")
    return s


def statue_slann():
    s = S(11, 12, 116); c = 5
    socle(s, 1, 1, 9, 9, "minecraft:mossy_stone_bricks")
    s.fill(1, G, 1, 9, G + 1, 9, ["minecraft:mossy_stone_bricks", "minecraft:cracked_stone_bricks"])
    s.disk(c, c, 3, G + 2, "minecraft:gold_block")  # palanquin
    s.fill(c - 2, G + 3, c - 2, c + 2, G + 5, c + 2, "minecraft:prismarine")  # corps du Sage-Crapaud
    s.fill(c - 1, G + 6, c - 1, c + 1, G + 7, c + 1, "minecraft:prismarine")
    s.set(c, G + 7, c + 2, "minecraft:prismarine_stairs[facing=north]")
    s.set(c - 1, G + 7, c + 1, "minecraft:gold_block"); s.set(c + 1, G + 7, c + 1, "minecraft:gold_block")
    s.set(c, G + 8, c, "minecraft:gold_block")
    ruine(s, 0.1)
    return s


# ------------------------------------------------------------------- AQSHY / CHAMON
def pilier_flamme():
    s = S(7, 16, 117); c = 3
    socle(s, 1, 1, 5, 5, "minecraft:basalt")
    for y in range(G, G + 11):
        r = 2 if y < G + 4 else 1
        s.cylinder(c, c, r, y, y, ["minecraft:basalt", "minecraft:polished_basalt", "minecraft:blackstone"], hollow=False)
    s.set(c, G + 11, c, "minecraft:netherrack"); s.set(c, G + 12, c, "minecraft:fire")
    s.set(c + 1, G + 7, c, "minecraft:magma_block"); s.set(c - 1, G + 4, c + 1, "minecraft:magma_block")
    return s


def forge_abandonnee():
    s = S(11, 10, 118); c = 5
    socle(s, 0, 0, 10, 10, "minecraft:blackstone")
    s.fill(0, G, 0, 10, G, 10, ["minecraft:polished_blackstone_bricks", "minecraft:cracked_polished_blackstone_bricks"])
    for (x, z) in ((1, 1), (9, 1), (1, 9), (9, 9)):
        s.fill(x, G + 1, z, x, G + 5, z, "minecraft:polished_blackstone_brick_wall")
    s.fill(1, G + 6, 1, 9, G + 6, 9, "minecraft:polished_blackstone_slab")
    s.fill(c - 1, G + 1, 2, c + 1, G + 3, 3, "minecraft:polished_blackstone_bricks")
    s.set(c, G + 1, 3, "minecraft:lava_cauldron"); s.set(c, G + 1, 4, "minecraft:anvil")
    s.set(c + 2, G + 1, 4, "minecraft:blast_furnace[facing=south]")
    s.chest(c - 2, G + 1, 4, L + "magmahold", "south")
    ruine(s, 0.4)
    return s


def mare_lave():
    s = S(11, 6, 119); c = 5
    socle(s, 0, 0, 10, 10, "minecraft:blackstone")
    s.disk(c, c, 5, G, ["minecraft:magma_block", "minecraft:basalt"])
    s.disk(c, c, 3, G, "minecraft:lava")
    s.disk(c, c, 3, G - 1, "minecraft:magma_block")
    s.set(c + 4, G + 1, c, "minecraft:polished_basalt"); s.set(c + 4, G + 2, c, "minecraft:polished_basalt")
    return s


def epave_kharadron():
    s = S(23, 14, 120); c = 11
    # coque échouée et inclinée
    for x in range(2, 21):
        half = 3 if 6 < x < 16 else 2 if 3 < x < 19 else 1
        tilt = (x - 2) // 7
        s.fill(x, G - 1 + tilt, c - half, x, G - 1 + tilt, c + half, ["minecraft:waxed_copper_block", "minecraft:waxed_exposed_copper", "minecraft:waxed_weathered_copper"])
        s.set(x, G + tilt, c - half, "minecraft:waxed_cut_copper"); s.set(x, G + tilt, c + half, "minecraft:waxed_cut_copper")
        s.fill(x, G + tilt, c - half + 1, x, G + tilt, c + half - 1, "minecraft:spruce_planks")
    # mât brisé et ballon effondré
    s.fill(11, G + 2, c, 11, G + 8, c, "minecraft:spruce_log")
    for x in range(12, 19):
        for z in range(c - 3, c + 4):
            if s.rng.random() < 0.7:
                s.set(x, G + 2 + (x - 12) // 3, z, s.rng.choice(["minecraft:yellow_wool", "minecraft:orange_wool"]))
    s.barrel(6, G + 1, c, L + "port_kharadron"); s.barrel(7, G + 1, c + 1, L + "port_kharadron")
    s.set(4, G + 1, c, "minecraft:lightning_rod[facing=west]")
    return s


def obelisque_or():
    s = S(7, 18, 121); c = 3
    socle(s, 1, 1, 5, 5, "minecraft:smooth_sandstone")
    s.fill(1, G, 1, 5, G + 1, 5, "minecraft:cut_sandstone")
    for y in range(G + 2, G + 13):
        s.fill(2, y, 2, 4, y, 4, "minecraft:gold_block" if y > G + 10 else "minecraft:smooth_sandstone")
    s.fill(c, G + 13, c, c, G + 14, c, "minecraft:gold_block")
    for y in range(G + 4, G + 10, 2):
        s.set(c, y, 1, "minecraft:chiseled_sandstone")
    return s


# ------------------------------------------------------------------- SHYISH
def pierres_tombales():
    s = S(11, 6, 122); c = 5
    socle(s, 0, 0, 10, 10, "minecraft:dirt")
    s.fill(0, G, 0, 10, G, 10, ["minecraft:podzol", "minecraft:coarse_dirt", "minecraft:soul_soil"])
    for x in range(1, 10, 3):
        for z in range(1, 10, 3):
            if s.rng.random() < 0.8:
                s.set(x, G + 1, z, s.rng.choice(["minecraft:cobblestone_wall", "minecraft:mossy_cobblestone_wall", "minecraft:stone_brick_wall", "minecraft:deepslate_brick_wall"]))
                if s.rng.random() < 0.4:
                    s.set(x, G + 2, z, "minecraft:skeleton_skull")
                s.set(x, G, z + 1, "minecraft:rooted_dirt")
    s.set(c, G + 1, c, "minecraft:soul_lantern")
    return s


def mausolee_ruine():
    s = S(11, 12, 123); c = 5
    socle(s, 0, 0, 10, 10, "minecraft:cobbled_deepslate")
    s.hollow(1, G, 1, 9, G + 6, 9, ["minecraft:deepslate_bricks", "minecraft:cracked_deepslate_bricks", "minecraft:mossy_stone_bricks"],
             floor="minecraft:polished_deepslate")
    s.roof_gable(1, 1, 9, 9, G + 7, "minecraft:deepslate_tile_stairs", "minecraft:deepslate_tiles", axis="z")
    s.clear(c, G + 1, 9, c, G + 3, 9)
    s.fill(3, G + 1, 3, 7, G + 1, 4, "minecraft:polished_deepslate")  # sarcophage
    s.set(c, G + 2, 3, "minecraft:skeleton_skull")
    s.set(2, G + 1, 7, "minecraft:soul_campfire"); s.set(8, G + 1, 7, "minecraft:soul_campfire")
    s.chest(8, G + 1, 2, L + "cimetiere_nighthaunt", "west")
    ruine(s, 0.3)
    s.mob(c, G + 1, 6, "skeleton", "glaivewraith")
    return s


def gibet():
    s = S(7, 10, 124); c = 3
    socle(s, 2, 2, 4, 4, "minecraft:dirt")
    s.fill(1, G + 1, c, 1, G + 6, c, "minecraft:dark_oak_log")
    s.fill(1, G + 6, c, 5, G + 6, c, "minecraft:dark_oak_fence")
    s.fill(5, G + 5, c, 5, G + 4, c, "minecraft:iron_chain")
    s.walls(4, G + 1, c - 1, 6, G + 3, c + 1, "minecraft:iron_bars")
    s.set(5, G + 1, c, "minecraft:skeleton_skull")
    return s


def arbre_mort():
    s = S(11, 16, 125); c = 5
    socle(s, c - 1, c - 1, c + 1, c + 1, "minecraft:dirt")
    s.fill(c, G + 1, c, c, G + 9, c, "minecraft:dark_oak_log")
    for (dx, dz, y, L_) in ((1, 0, G + 6, 4), (-1, 0, G + 8, 3), (0, 1, G + 5, 3), (0, -1, G + 9, 4)):
        for k in range(1, L_ + 1):
            s.set(c + dx * k, y + k // 2, c + dz * k, "minecraft:dark_oak_wood")
    s.set(c + 3, G + 6, c, "minecraft:iron_chain"); s.set(c + 3, G + 5, c, "minecraft:soul_lantern[hanging=true]")
    return s


def ossuaire_tas():
    s = S(9, 8, 126); c = 4
    socle(s, 1, 1, 7, 7, "minecraft:dirt")
    s.disk(c, c, 3, G, "minecraft:soul_soil")
    for y in range(G + 1, G + 4):
        s.disk(c, c, 3 - (y - G - 1), y, ["minecraft:bone_block", "minecraft:bone_block", "minecraft:skeleton_skull"])
    return s


# ------------------------------------------------------------------- ULGU
def autel_khaine():
    s = S(9, 9, 127); c = 4
    socle(s, 0, 0, 8, 8, "minecraft:nether_bricks")
    s.disk(c, c, 4, G, ["minecraft:red_nether_bricks", "minecraft:polished_blackstone"])
    s.disk(c, c, 2, G, "minecraft:red_concrete")
    s.fill(c - 1, G + 1, c - 1, c + 1, G + 1, c + 1, "minecraft:iron_block")
    s.set(c, G + 2, c, "minecraft:lava_cauldron")
    for (x, z) in ((0, 0), (8, 0), (0, 8), (8, 8)):
        s.fill(x, G + 1, z, x, G + 3, z, "minecraft:red_nether_brick_wall")
        s.set(x, G + 4, z, "minecraft:redstone_lamp[lit=true]")
    return s


def champignon_geant():
    s = S(11, 16, 128); c = 5
    socle(s, c - 1, c - 1, c + 1, c + 1, "minecraft:mycelium")
    s.fill(c, G + 1, c, c, G + 10, c, "minecraft:mushroom_stem")
    cap = s.rng.choice(["red", "brown"])
    s.cylinder(c, c, 5, G + 11, G + 11, f"minecraft:{cap}_mushroom_block", hollow=False)
    s.cylinder(c, c, 4, G + 12, G + 12, f"minecraft:{cap}_mushroom_block", hollow=False)
    s.cylinder(c, c, 2, G + 13, G + 13, f"minecraft:{cap}_mushroom_block", hollow=False)
    s.set(c, G + 10, c, "minecraft:shroomlight")
    s.set(c + 1, G + 1, c, "minecraft:red_mushroom"); s.set(c - 1, G + 1, c + 1, "minecraft:brown_mushroom")
    return s


def ruines_brumes():
    s = S(13, 12, 129); c = 6
    socle(s, 0, 0, 12, 12, "minecraft:cobbled_deepslate")
    s.walls(1, G, 1, 11, G + 7, 11, ["minecraft:deepslate_bricks", "minecraft:tuff_bricks", "minecraft:cracked_deepslate_bricks"])
    s.clear(c - 1, G + 1, 11, c + 1, G + 4, 11)
    s.fill(2, G, 2, 10, G, 10, ["minecraft:tuff", "minecraft:polished_tuff", "minecraft:moss_block"])
    s.set(c, G + 1, c, "minecraft:lodestone")
    ruine(s, 0.6)
    return s


def arche_prismarine():
    s = S(11, 12, 130); c = 5
    for x in (1, 9):
        s.fill(x, 0, c, x, G + 6, c, ["minecraft:prismarine_bricks", "minecraft:dark_prismarine"])
    for x in range(1, 10):
        s.set(x, G + 7, c, "minecraft:prismarine_bricks")
    s.set(c, G + 8, c, "minecraft:sea_lantern")
    s.fill(0, 0, 0, 10, G - 1, 10, ["minecraft:sand", "minecraft:gravel", "minecraft:prismarine"])
    s.set(c, G, c + 2, "minecraft:sea_pickle[pickles=4,waterlogged=true]")
    return s


# ------------------------------------------------------------------- CHAOS / SKAVEN
def pointe_chaos():
    s = S(9, 22, 131); c = 4
    socle(s, 2, 2, 6, 6, "minecraft:blackstone")
    h = 18
    for y in range(G, G + h):
        r = max(0, 3 - (y - G) * 3 // h)
        s.cylinder(c, c, r, y, y, ["minecraft:obsidian", "minecraft:obsidian", "minecraft:crying_obsidian", "minecraft:blackstone"], hollow=False)
    s.set(c, G + h, c, "minecraft:crying_obsidian")
    for (dx, dz) in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        s.set(c + dx * 3, G + 5, c + dz * 3, "minecraft:iron_chain")
        s.set(c + dx * 3, G + 4, c + dz * 3, "minecraft:skeleton_skull")
    return s


def autel_chaos():
    s = S(15, 10, 132); c = 7
    socle(s, 0, 0, 14, 14, "minecraft:blackstone")
    s.disk(c, c, 7, G, ["minecraft:polished_blackstone", "minecraft:blackstone"])
    for (dx, dz) in ((1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, -1), (1, -1), (-1, 1)):
        for k in range(1, 7):
            s.set(c + dx * k, G, c + dz * k, "minecraft:red_concrete")
        s.fill(c + dx * 6, G + 1, c + dz * 6, c + dx * 6, G + 3, c + dz * 6, "minecraft:obsidian")
        s.set(c + dx * 6, G + 4, c + dz * 6, "minecraft:soul_campfire")
    s.set(c, G + 1, c, "minecraft:crying_obsidian"); s.set(c, G + 2, c, "minecraft:enchanting_table")
    s.chest(c + 1, G + 1, c, L + "citadelle_chaos", "west")
    return s


def cage_prisonniers():
    s = S(9, 8, 133); c = 4
    socle(s, 1, 1, 7, 7, "minecraft:blackstone")
    s.fill(1, G, 1, 7, G, 7, "minecraft:polished_blackstone")
    s.walls(1, G + 1, 1, 7, G + 3, 7, "minecraft:iron_bars")
    s.fill(1, G + 4, 1, 7, G + 4, 7, "minecraft:polished_blackstone_slab")
    s.set(c, G + 1, c, "minecraft:bone_block"); s.set(c, G + 2, c, "minecraft:skeleton_skull")
    s.mob(c + 1, G + 1, c + 1, "villager", "habitant")
    return s


def cristaux_malepierre():
    s = S(9, 12, 134); c = 4
    socle(s, 1, 1, 7, 7, "minecraft:coarse_dirt")
    s.disk(c, c, 3, G, ["minecraft:gravel", "minecraft:coarse_dirt", "minecraft:mud"])
    for (dx, dz, h) in ((0, 0, 7), (1, 1, 4), (-1, 0, 5), (0, -2, 3), (2, -1, 3)):
        for y in range(G + 1, G + h + 1):
            s.set(c + dx, y, c + dz, "minecraft:verdant_froglight" if y < G + h else "minecraft:lime_stained_glass")
    s.set(c - 2, G + 1, c + 2, "minecraft:lime_stained_glass")
    return s


def cloche_hurlante():
    s = S(9, 16, 135); c = 4
    socle(s, 1, 1, 7, 7, "minecraft:cobblestone")
    for (x, z) in ((1, 1), (7, 1), (1, 7), (7, 7)):
        s.fill(x, G + 1, z, x, G + 9, z, ["minecraft:spruce_log", "minecraft:spruce_log", "minecraft:spruce_fence"])
    s.fill(1, G + 10, 1, 7, G + 10, 7, "minecraft:spruce_planks")
    s.fill(2, G + 10, 2, 6, G + 10, 6, "minecraft:air")
    s.set(c, G + 10, c, "minecraft:spruce_planks")
    s.set(c, G + 9, c, "minecraft:bell[attachment=ceiling]")
    s.set(c, G + 11, c, "minecraft:verdant_froglight")
    ruine(s, 0.25)
    return s


def tunnel_skaven():
    s = S(7, 8, 136); c = 3
    socle(s, 0, 0, 6, 6, "minecraft:cobblestone")
    s.fill(1, 0, 1, 5, G, 5, ["minecraft:cobblestone", "minecraft:mossy_cobblestone", "minecraft:gravel"])
    s.fill(2, 0, 2, 4, G, 4, "minecraft:air")
    for y in range(0, G + 1):
        s.set(c, y, 2, "minecraft:ladder[facing=south]")
    s.set(c, 0, c, "minecraft:verdant_froglight")
    s.fill(1, G + 1, 1, 5, G + 1, 1, "minecraft:spruce_fence")
    return s


# ------------------------------------------------------------------- Catalogue
# id: (constructeur, biomes, 1 chance sur N par chunk, carte de hauteur)
DECOS = {
    "statue_stormcast": (statue_stormcast, ["azyr_cimes", "hysh_plateaux"], 14),
    "autel_celeste": (autel_celeste, ["azyr_cimes"], 12),
    "tour_guet_quartz": (tour_guet_quartz, ["azyr_cimes", "hysh_plateaux"], 18),
    "cristal_hysh": (cristal_hysh, ["hysh_plateaux"], 5),
    "arche_lumineth": (arche_lumineth, ["hysh_plateaux"], 14),
    "arbre_esprit": (arbre_esprit, ["ghyran_jade"], 7),
    "cercle_pierres": (cercle_pierres, ["ghyran_jade", "ghur_terres"], 20),
    "sanctuaire_alarielle": (sanctuaire_alarielle, ["ghyran_jade"], 16),
    "totem_kruleboyz": (totem_kruleboyz, ["ghyran_marais"], 6),
    "hutte_pilotis": (hutte_pilotis, ["ghyran_marais"], 12),
    "chaudron_nurgle": (chaudron_nurgle, ["ghyran_marais"], 10),
    "squelette_bete": (squelette_bete, ["ghur_terres", "aqshy_cendres", "chamon_desert"], 14),
    "menhir_orruk": (menhir_orruk, ["ghur_terres"], 8),
    "campement_ruine": (campement_ruine, ["ghur_terres"], 14),
    "stele_seraphon": (stele_seraphon, ["ghur_jungle"], 7),
    "statue_slann": (statue_slann, ["ghur_jungle"], 18),
    "pilier_flamme": (pilier_flamme, ["aqshy_cendres"], 4),
    "forge_abandonnee": (forge_abandonnee, ["aqshy_cendres"], 16),
    "mare_lave": (mare_lave, ["aqshy_cendres"], 8),
    "epave_kharadron": (epave_kharadron, ["chamon_desert"], 16),
    "obelisque_or": (obelisque_or, ["chamon_desert"], 9),
    "pierres_tombales": (pierres_tombales, ["shyish_terres"], 5),
    "mausolee_ruine": (mausolee_ruine, ["shyish_terres"], 14),
    "gibet": (gibet, ["shyish_terres", "ulgu_brumes"], 10),
    "arbre_mort": (arbre_mort, ["shyish_terres", "chaos_desolation"], 4),
    "ossuaire_tas": (ossuaire_tas, ["shyish_terres"], 10),
    "autel_khaine": (autel_khaine, ["ulgu_brumes"], 14),
    "champignon_geant": (champignon_geant, ["ulgu_brumes"], 4),
    "ruines_brumes": (ruines_brumes, ["ulgu_brumes"], 12),
    "arche_prismarine": (arche_prismarine, ["ulgu_mer"], 8),
    "pointe_chaos": (pointe_chaos, ["chaos_desolation"], 4),
    "autel_chaos": (autel_chaos, ["chaos_desolation"], 14),
    "cage_prisonniers": (cage_prisonniers, ["chaos_desolation"], 12),
    "cristaux_malepierre": (cristaux_malepierre, ["terres_rongees"], 4),
    "cloche_hurlante": (cloche_hurlante, ["terres_rongees"], 14),
    "tunnel_skaven": (tunnel_skaven, ["terres_rongees"], 8),
}
OCEAN_DECOS = {"arche_prismarine"}
