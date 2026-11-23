# -*- coding: utf-8 -*-
"""Plans procéduraux des structures des Royaumes Mortels."""
from nbtgen import Struct

F = 4  # niveau du sol dans le gabarit (les 4 couches dessous sont des fondations)
L = "royaumes:coffres/"


def base(sx, sy, sz, sol, fond="minecraft:cobblestone", seed=1, marge=0):
    s = Struct(sx, sy, sz, seed)
    s.foundation(marge, marge, sx - 1 - marge, sz - 1 - marge, F - 1, F, fond)
    s.fill(marge, F, marge, sx - 1 - marge, F, sz - 1 - marge, sol)
    s.clear(marge, F + 1, marge, sx - 1 - marge, min(sy - 1, F + 6), sz - 1 - marge)
    return s


# ======================================================================= ORDRE
def forteresse_stormcast():
    W = 41
    s = base(W, 34, W, ["minecraft:smooth_quartz", "minecraft:quartz_bricks"], "minecraft:stone_bricks", seed=11)
    murs = ["minecraft:quartz_bricks"] * 4 + ["minecraft:smooth_quartz"]
    # Remparts
    s.walls(2, F + 1, 2, W - 3, F + 9, W - 3, murs)
    s.fill(3, F + 9, 3, W - 4, F + 9, 4, "minecraft:smooth_quartz_slab")  # chemin de ronde partiel
    s.crenel(2, F + 10, 2, W - 3, W - 3, "minecraft:quartz_block")
    for y in (F + 4, F + 7):
        for i in range(6, W - 6, 4):
            s.set(i, y, 2, "minecraft:blue_stained_glass"); s.set(i, y, W - 3, "minecraft:blue_stained_glass")
            s.set(2, y, i, "minecraft:blue_stained_glass"); s.set(W - 3, y, i, "minecraft:blue_stained_glass")
    # Liseré d'or
    for x in range(2, W - 2):
        for z in (2, W - 3):
            s.set(x, F + 8, z, "minecraft:gold_block")
    for z in range(2, W - 2):
        for x in (2, W - 3):
            s.set(x, F + 8, z, "minecraft:gold_block")
    # Porte monumentale (sud)
    s.clear(W // 2 - 2, F + 1, W - 3, W // 2 + 2, F + 6, W - 3)
    s.fill(W // 2 - 3, F + 7, W - 3, W // 2 + 3, F + 7, W - 3, "minecraft:gold_block")
    # Tours d'angle
    for cx, cz in ((3, 3), (W - 4, 3), (3, W - 4), (W - 4, W - 4)):
        s.cylinder(cx, cz, 3, F + 1, F + 15, murs)
        s.disk(cx, cz, 3, F + 15, "minecraft:smooth_quartz")
        s.cone(cx, cz, 3, F + 16, "minecraft:lapis_block")
        s.set(cx, F + 20, cz, "minecraft:lightning_rod")
        s.set(cx, F + 14, cz, "minecraft:sea_lantern")
    # Donjon central (Temple de Sigmar)
    c = W // 2
    s.hollow(c - 7, F, c - 7, c + 7, F + 14, c + 7, murs, floor="minecraft:polished_diorite")
    s.walls(c - 7, F + 13, c - 7, c + 7, F + 13, c + 7, "minecraft:gold_block")
    s.pyramid(c - 7, c - 7, c + 7, c + 7, F + 14, "minecraft:lapis_block")
    s.set(c, F + 22, c, "minecraft:lightning_rod")
    s.clear(c - 1, F + 1, c + 7, c + 1, F + 4, c + 7)
    for y in (F + 4, F + 9):
        for i in (c - 4, c, c + 4):
            s.set(i, y, c - 7, "minecraft:light_blue_stained_glass"); s.set(c - 7, y, i, "minecraft:light_blue_stained_glass")
            s.set(c + 7, y, i, "minecraft:light_blue_stained_glass")
    # Autel et statue de Sigmar (colonne d'or + éclair)
    s.fill(c - 1, F + 1, c - 5, c + 1, F + 1, c - 4, "minecraft:gold_block")
    s.fill(c, F + 2, c - 5, c, F + 6, c - 5, "minecraft:gold_block")
    s.set(c - 1, F + 5, c - 5, "minecraft:gold_block"); s.set(c + 1, F + 5, c - 5, "minecraft:gold_block")
    s.set(c, F + 7, c - 5, "minecraft:sea_lantern")
    for dx, dz in ((-5, -5), (5, -5), (-5, 5), (5, 5)):
        s.fill(c + dx, F + 1, c + dz, c + dx, F + 12, c + dz, "minecraft:quartz_pillar")
        s.set(c + dx, F + 12, c + dz, "minecraft:sea_lantern")
    s.chest(c - 3, F + 1, c - 5, L + "forteresse_stormcast", "south")
    s.chest(c + 3, F + 1, c - 5, L + "forteresse_stormcast", "south")
    s.fill(c - 6, F + 1, c + 2, c - 6, F + 3, c + 5, "minecraft:bookshelf")
    # Cour : forges et râteliers
    s.set(8, F + 1, 8, "minecraft:anvil"); s.set(9, F + 1, 8, "minecraft:smithing_table")
    s.set(10, F + 1, 8, "minecraft:blast_furnace"); s.barrel(11, F + 1, 8, L + "forteresse_stormcast")
    s.set(W - 9, F + 1, 8, "minecraft:enchanting_table")
    for x, z in ((8, W - 9), (W - 9, W - 9)):
        s.set(x, F + 1, z, "minecraft:lantern")
    for i in range(6, W - 6, 6):
        s.set(i, F + 1, W // 2 + 9, "minecraft:sea_lantern")
    # Garnison
    s.mob(c, F + 1, c, "zombie", "sc_lord")
    s.mob(c - 3, F + 1, c + 3, "zombie", "sc_liberator", 2)
    s.mob(10, F + 1, 12, "zombie", "sc_liberator", 2)
    s.mob(W - 11, F + 1, 12, "skeleton", "sc_judicator", 2)
    s.mob(12, F + 1, W - 10, "skeleton", "sc_judicator", 1)
    return s


def cite_sigmar():
    W = 47
    s = base(W, 26, W, ["minecraft:stone_bricks", "minecraft:cobblestone", "minecraft:andesite"], "minecraft:stone", seed=12)
    s.walls(1, F + 1, 1, W - 2, F + 6, W - 2, ["minecraft:stone_bricks", "minecraft:stone_bricks", "minecraft:mossy_stone_bricks"])
    s.crenel(1, F + 7, 1, W - 2, W - 2, "minecraft:stone_bricks")
    c = W // 2
    # Portes
    s.clear(c - 1, F + 1, W - 2, c + 1, F + 4, W - 2); s.clear(c - 1, F + 1, 1, c + 1, F + 4, 1)
    for cx, cz in ((1, 1), (W - 2, 1), (1, W - 2), (W - 2, W - 2)):
        s.cylinder(cx, cz, 2, F + 1, F + 10, "minecraft:stone_bricks")
        s.cone(cx, cz, 2, F + 11, "minecraft:dark_oak_planks")
    # Rues pavées
    s.fill(c - 1, F, 2, c + 1, F, W - 3, "minecraft:polished_andesite")
    s.fill(2, F, c - 1, W - 3, F, c + 1, "minecraft:polished_andesite")
    # Maisons à colombages
    maisons = [(4, 4), (13, 4), (29, 4), (37, 4), (4, 30), (13, 33), (30, 30), (37, 34), (4, 15), (37, 15)]
    for i, (x, z) in enumerate(maisons):
        w, d, h = 6, 6, 4
        s.hollow(x, F, z, x + w, F + h, z + d, "minecraft:white_terracotta", floor="minecraft:spruce_planks")
        for (xx, zz) in ((x, z), (x + w, z), (x, z + d), (x + w, z + d)):
            s.fill(xx, F + 1, zz, xx, F + h, zz, "minecraft:spruce_log")
        s.fill(x, F + h, z, x + w, F + h, z + d, "minecraft:spruce_planks")
        s.fill(x + 1, F + h, z + 1, x + w - 1, F + h, z + d - 1, "minecraft:air")
        s.roof_gable(x, z, x + w, z + d, F + h + 1, "minecraft:dark_oak_stairs", "minecraft:dark_oak_planks", axis="x")
        dz = z + d if z < c else z
        s.door(x + 3, F + 1, dz, facing="south" if z < c else "north")
        s.set(x + 1, F + 2, z + 3, "minecraft:glass_pane"); s.set(x + w - 1, F + 1, z + 1, "minecraft:lantern")
        s.set(x + 1, F + 1, z + 1, "minecraft:red_bed[facing=north,part=head]")
        s.set(x + 1, F + 1, z + 2, "minecraft:red_bed[facing=north,part=foot]")
        if i % 3 == 0:
            s.chest(x + w - 1, F + 1, z + d - 1, L + "cite_sigmar")
        s.mob(x + 3, F + 1, z + 3, "villager", "habitant")
    # Temple de Sigmar (au nord de la place)
    s.hollow(c - 5, F, 12, c + 5, F + 9, 19, "minecraft:polished_diorite", floor="minecraft:polished_andesite")
    s.pyramid(c - 5, 12, c + 5, 19, F + 9, "minecraft:blue_terracotta")
    s.clear(c - 1, F + 1, 19, c + 1, F + 4, 19)
    s.fill(c, F + 1, 13, c, F + 5, 13, "minecraft:gold_block"); s.set(c, F + 6, 13, "minecraft:sea_lantern")
    s.set(c - 4, F + 4, 15, "minecraft:yellow_stained_glass"); s.set(c + 4, F + 4, 15, "minecraft:yellow_stained_glass")
    s.chest(c - 3, F + 1, 13, L + "cite_sigmar", "south")
    # Place du marché
    s.fill(c - 1, F, c - 1, c + 1, F, c + 1, "minecraft:chiseled_stone_bricks")
    s.set(c, F + 1, c, "minecraft:water_cauldron[level=3]")
    for dx, col in ((-6, "red"), (6, "blue"), (0, "yellow")):
        x = c + dx; z = c + 7 if dx == 0 else c + 4
        s.fill(x - 1, F + 1, z, x + 1, F + 1, z, "minecraft:barrel[facing=up]")
        for xx in (x - 1, x + 1):
            s.fill(xx, F + 2, z, xx, F + 3, z, "minecraft:oak_fence")
        s.fill(x - 1, F + 4, z - 1, x + 1, F + 4, z + 1, f"minecraft:{col}_wool")
    s.set(c + 6, F + 1, c - 6, "minecraft:smithing_table"); s.set(c - 6, F + 1, c - 6, "minecraft:lectern")
    # Population
    s.mob(c, F + 1, c + 3, "iron_golem", "garde_cite")
    s.mob(c - 3, F + 1, W - 5, "zombie", "cites_garde", 2)
    s.mob(c + 3, F + 1, 5, "skeleton", "cites_arbaletrier", 2)
    s.mob(c - 8, F + 1, c, "villager", "habitant", 2)
    return s


def bosquet_sylvaneth():
    W = 29
    s = base(W, 32, W, ["minecraft:moss_block", "minecraft:grass_block"], "minecraft:dirt", seed=13)
    c = W // 2
    # Arbre-mère : tronc creux en spirale
    s.cylinder(c, c, 3, F + 1, F + 16, ["minecraft:oak_wood", "minecraft:oak_wood", "minecraft:moss_block"])
    s.clear(c - 1, F + 1, c + 3, c + 1, F + 3, c + 3)
    s.set(c, F + 1, c, "minecraft:shroomlight"); s.chest(c, F + 1, c - 1, L + "bosquet_sylvaneth", "south")
    for y in range(F + 16, F + 24):
        r = 8 - abs(y - (F + 20))
        s.cylinder(c, c, max(r, 3), y, y, ["minecraft:azalea_leaves[persistent=true]",
                                          "minecraft:flowering_azalea_leaves[persistent=true]"], hollow=False)
    for (dx, dz) in ((-5, 0), (5, 0), (0, -5), (0, 5)):
        s.fill(c + dx, F + 12, c + dz, c + dx, F + 16, c + dz, "minecraft:oak_wood")
        s.set(c + dx, F + 11, c + dz, "minecraft:shroomlight")
    # Cercle de pierres moussues et fleurs
    for i in range(0, 360, 30):
        import math
        x = c + round(11 * math.cos(math.radians(i))); z = c + round(11 * math.sin(math.radians(i)))
        s.fill(x, F + 1, z, x, F + 2, z, "minecraft:mossy_cobblestone")
        s.set(x, F + 3, z, "minecraft:glow_lichen[up=false,down=true]")
    for x in range(2, W - 2, 3):
        for z in range(2, W - 2, 4):
            if abs(x - c) > 4 or abs(z - c) > 4:
                s.set(x, F + 1, z, s.rng.choice(["minecraft:allium", "minecraft:blue_orchid", "minecraft:lily_of_the_valley",
                                                  "minecraft:fern", "minecraft:azalea"]))
    s.mob(c + 5, F + 1, c + 5, "zombie", "dryade", 3)
    return s


def magmahold():
    W = 35
    s = base(W, 24, W, ["minecraft:polished_blackstone_bricks", "minecraft:blackstone"], "minecraft:blackstone", seed=14)
    c = W // 2
    s.walls(2, F + 1, 2, W - 3, F + 6, W - 3, ["minecraft:polished_blackstone_bricks", "minecraft:gilded_blackstone"])
    s.crenel(2, F + 7, 2, W - 3, W - 3, "minecraft:gold_block")
    s.clear(c - 1, F + 1, W - 3, c + 1, F + 4, W - 3)
    # Fosse de lave centrale avec runes d'or
    s.cylinder(c, c, 5, F, F, "minecraft:gold_block", hollow=False)
    s.cylinder(c, c, 3, F, F, "minecraft:lava", hollow=False)
    s.cylinder(c, c, 4, F + 1, F + 1, "minecraft:polished_blackstone_brick_wall", hollow=True, inside=None)
    # Effigie de Grimnir
    s.fill(c, F + 1, 6, c, F + 9, 6, "minecraft:gold_block")
    s.fill(c - 2, F + 7, 6, c + 2, F + 7, 6, "minecraft:gold_block")
    s.set(c, F + 10, 6, "minecraft:magma_block"); s.set(c - 2, F + 8, 6, "minecraft:fire")
    # Halls de forge
    for x0 in (4, W - 12):
        s.hollow(x0, F, 9, x0 + 7, F + 6, 16, "minecraft:polished_blackstone_bricks", floor="minecraft:blackstone")
        s.fill(x0, F + 6, 9, x0 + 7, F + 6, 16, "minecraft:polished_blackstone")
        s.clear(x0 + 3, F + 1, 16, x0 + 4, F + 3, 16)
        s.set(x0 + 1, F + 1, 10, "minecraft:blast_furnace"); s.set(x0 + 2, F + 1, 10, "minecraft:anvil")
        s.set(x0 + 6, F + 1, 10, "minecraft:lava_cauldron")
        s.chest(x0 + 6, F + 1, 15, L + "magmahold", "west")
        s.set(x0 + 3, F + 5, 12, "minecraft:shroomlight")
    s.mob(c + 4, F + 1, c + 7, "zombie", "fyreslayer", 4)
    return s


def port_kharadron():
    W = 33
    s = Struct(W, 36, W, 15)
    # Piliers et quai sur pilotis
    for x, z in ((4, 4), (W - 5, 4), (4, W - 5), (W - 5, W - 5), (W // 2, 4), (W // 2, W - 5)):
        s.fill(x, 0, z, x, 14, z, "minecraft:cut_copper")
    s.fill(2, 15, 2, W - 3, 15, W - 3, ["minecraft:waxed_cut_copper", "minecraft:waxed_exposed_cut_copper", "minecraft:spruce_planks"])
    s.walls(2, 16, 2, W - 3, 16, W - 3, "minecraft:iron_bars")
    s.fill(W // 2 - 1, 0, W - 3, W // 2 + 1, 15, W - 3, "minecraft:air")
    for y in range(0, 16):  # échelle
        s.set(W // 2, y, W - 4, "minecraft:ladder[facing=north]")
    s.fill(W // 2, 0, W - 5, W // 2, 15, W - 5, "minecraft:cut_copper")
    # Navire volant (frégate) amarré
    cx = W // 2
    for z in range(6, W - 8):
        half = 4 if 9 < z < W - 11 else 3 if 7 < z < W - 9 else 2
        s.fill(cx - half, 19, z, cx + half, 19, z, "minecraft:waxed_copper_block")
        s.set(cx - half, 20, z, "minecraft:waxed_cut_copper"); s.set(cx + half, 20, z, "minecraft:waxed_cut_copper")
        s.fill(cx - half + 1, 18, z, cx + half - 1, 18, z, "minecraft:spruce_planks")
    s.fill(cx - 2, 20, 10, cx + 2, 23, 14, "minecraft:spruce_planks")
    s.fill(cx - 1, 21, 10, cx + 1, 22, 14, "minecraft:air")
    s.chest(cx, 21, 11, L + "port_kharadron", "south")
    # Ballon d'endrinrigging
    for z in range(8, W - 10):
        for dx in range(-3, 4):
            for dy in range(0, 5):
                if dx * dx + (dy - 2) ** 2 <= 10:
                    s.set(cx + dx, 26 + dy, z, "minecraft:yellow_wool" if (z % 4) else "minecraft:orange_wool")
    for z in (10, W - 12):
        s.fill(cx, 21, z, cx, 25, z, "minecraft:iron_chain")
    s.set(cx, 19, 6, "minecraft:lightning_rod[facing=south]")
    s.fill(cx - 5, 15, 13, cx - 5, 18, 13, "minecraft:iron_chain")
    # Entrepôt
    s.fill(4, 16, 18, 9, 20, 26, "minecraft:waxed_cut_copper"); s.fill(5, 16, 19, 8, 19, 25, "minecraft:air")
    s.clear(9, 16, 21, 9, 17, 22)
    for z in range(19, 25, 2):
        s.barrel(5, 16, z, L + "port_kharadron")
    s.set(7, 19, 22, "minecraft:lantern")
    s.mob(cx, 20, 16, "skeleton", "kharadron", 3)
    s.mob(12, 16, 20, "skeleton", "kharadron", 2)
    return s


def sanctuaire_lumineth():
    W = 25
    s = base(W, 40, W, ["minecraft:calcite", "minecraft:smooth_quartz"], "minecraft:calcite", seed=16)
    c = W // 2
    s.disk(c, c, 10, F, ["minecraft:calcite", "minecraft:polished_diorite", "minecraft:smooth_quartz"])
    s.cylinder(c, c, 4, F + 1, F + 24, ["minecraft:smooth_quartz", "minecraft:quartz_bricks", "minecraft:calcite"])
    for y in range(F + 3, F + 24, 4):
        s.set(c + 4, y, c, "minecraft:white_stained_glass"); s.set(c - 4, y, c, "minecraft:white_stained_glass")
        s.set(c, y, c + 4, "minecraft:white_stained_glass"); s.set(c, y, c - 4, "minecraft:white_stained_glass")
    y = s.cone(c, c, 4, F + 25, "minecraft:quartz_block")
    s.fill(c, y, c, c, y + 3, c, "minecraft:end_rod")
    s.clear(c, F + 1, c + 4, c, F + 2, c + 4)
    s.set(c, F + 1, c, "minecraft:beacon"); s.fill(c - 1, F, c - 1, c + 1, F, c + 1, "minecraft:gold_block")
    s.chest(c + 2, F + 1, c, L + "sanctuaire_lumineth", "west")
    for i, (dx, dz) in enumerate(((-8, -8), (8, -8), (-8, 8), (8, 8))):
        s.fill(c + dx, F + 1, c + dz, c + dx, F + 6, c + dz, "minecraft:quartz_pillar")
        s.set(c + dx, F + 7, c + dz, "minecraft:sea_lantern")
    s.mob(c + 6, F + 1, c, "zombie", "lumineth_garde", 2)
    s.mob(c - 6, F + 1, c, "skeleton", "lumineth", 2)
    return s


def temple_seraphon():
    W = 37
    s = base(W, 30, W, ["minecraft:mossy_stone_bricks", "minecraft:stone_bricks", "minecraft:mossy_cobblestone"],
             "minecraft:mossy_cobblestone", seed=17)
    c = W // 2
    pierre = ["minecraft:mossy_stone_bricks", "minecraft:stone_bricks", "minecraft:cracked_stone_bricks", "minecraft:mossy_stone_bricks"]
    top = s.pyramid(6, 6, W - 7, W - 7, F + 1, pierre, step=1)
    # Escalier frontal
    for i in range(0, top - F - 1):
        s.fill(c - 1, F + 1 + i, W - 7 - i, c + 1, F + 1 + i, W - 7 - i, "minecraft:stone_brick_stairs[facing=north]")
    # Sanctuaire au sommet
    s.hollow(c - 3, top, c - 3, c + 3, top + 5, c + 3, "minecraft:chiseled_stone_bricks", floor="minecraft:gold_block")
    s.clear(c - 1, top + 1, c + 3, c + 1, top + 3, c + 3)
    s.fill(c - 3, top + 5, c - 3, c + 3, top + 5, c + 3, "minecraft:gold_block")
    s.set(c, top + 1, c - 1, "minecraft:chest[facing=south]", {"id": "minecraft:chest", "LootTable": L + "temple_seraphon", "Items": []})
    s.set(c, top + 3, c, "minecraft:sea_lantern")
    # Bassin sacré
    s.fill(3, F, c - 2, 3, F, c + 2, "minecraft:water")
    s.chest(c, F + 1, 2, L + "temple_seraphon", "south")
    s.mob(c, top + 1, c + 1, "zombie", "saurus", 2)
    s.mob(c + 6, F + 1, W - 3, "zombie", "saurus", 2)
    s.mob(c - 6, F + 1, W - 3, "skeleton", "skink", 3)
    return s


def ruines_idoneth():
    W = 27
    s = Struct(W, 20, W, 18)
    s.fill(0, 0, 0, W - 1, 1, W - 1, ["minecraft:prismarine", "minecraft:sand", "minecraft:gravel"])
    c = W // 2
    s.disk(c, c, 11, 2, ["minecraft:prismarine_bricks", "minecraft:dark_prismarine", "minecraft:prismarine"])
    for i, (dx, dz) in enumerate(((-9, 0), (9, 0), (0, -9), (0, 9), (-6, -6), (6, 6), (-6, 6), (6, -6))):
        h = 4 + (i * 3) % 7
        s.fill(c + dx, 3, c + dz, c + dx, 3 + h, c + dz, ["minecraft:prismarine_bricks", "minecraft:dark_prismarine"])
        s.set(c + dx, 4 + h, c + dz, "minecraft:sea_lantern")
    s.hollow(c - 3, 2, c - 3, c + 3, 8, c + 3, "minecraft:dark_prismarine", inside="minecraft:water")
    s.clear(c, 3, c + 3, c, 4, c + 3); s.set(c, 3, c + 3, "minecraft:water"); s.set(c, 4, c + 3, "minecraft:water")
    s.set(c, 3, c, "minecraft:conduit[waterlogged=true]")
    s.set(c - 2, 3, c - 2, "minecraft:chest[facing=south,waterlogged=true]",
          {"id": "minecraft:chest", "LootTable": L + "ruines_idoneth", "Items": []})
    s.set(c + 2, 3, c - 2, "minecraft:chest[facing=south,waterlogged=true]",
          {"id": "minecraft:chest", "LootTable": L + "ruines_idoneth", "Items": []})
    for x in range(3, W - 3, 3):
        s.set(x, 3, 2, "minecraft:sea_pickle[pickles=3,waterlogged=true]")
    s.mob(c + 5, 3, c + 5, "drowned", "idoneth", 3)
    return s


def temple_khaine():
    W = 31
    s = base(W, 22, W, ["minecraft:red_nether_bricks", "minecraft:nether_bricks"], "minecraft:nether_bricks", seed=19)
    c = W // 2
    s.walls(3, F + 1, 3, W - 4, F + 8, W - 4, ["minecraft:red_nether_bricks", "minecraft:red_nether_bricks", "minecraft:nether_bricks"])
    s.fill(3, F + 9, 3, W - 4, F + 9, W - 4, "minecraft:red_nether_brick_slab")
    s.fill(4, F + 9, 4, W - 5, F + 9, W - 5, "minecraft:air")
    s.clear(c - 1, F + 1, W - 4, c + 1, F + 5, W - 4)
    # Chaudron de sang central
    s.disk(c, c, 4, F, "minecraft:polished_blackstone")
    s.disk(c, c, 2, F, "minecraft:red_concrete")
    s.fill(c - 1, F + 1, c - 1, c + 1, F + 1, c + 1, "minecraft:iron_block")
    s.set(c, F + 2, c, "minecraft:lava_cauldron"); s.set(c - 1, F + 2, c, "minecraft:iron_bars"); s.set(c + 1, F + 2, c, "minecraft:iron_bars")
    # Statue de Khaine (lames)
    s.fill(c, F + 1, 6, c, F + 10, 6, "minecraft:polished_blackstone")
    s.fill(c - 3, F + 8, 6, c + 3, F + 8, 6, "minecraft:iron_block")
    s.set(c - 3, F + 9, 6, "minecraft:iron_bars"); s.set(c + 3, F + 9, 6, "minecraft:iron_bars")
    s.set(c, F + 11, 6, "minecraft:redstone_lamp[lit=true]")
    for x in (6, W - 7):
        for z in range(7, W - 6, 4):
            s.fill(x, F + 1, z, x, F + 7, z, "minecraft:red_nether_brick_wall")
            s.set(x, F + 8, z, "minecraft:shroomlight")
    s.chest(c - 2, F + 1, 7, L + "temple_khaine", "south"); s.chest(c + 2, F + 1, 7, L + "temple_khaine", "south")
    s.mob(c, F + 1, c + 6, "zombie", "khaine_aelf", 4)
    return s


# ======================================================================= CHAOS
def citadelle_chaos():
    W = 39
    s = base(W, 40, W, ["minecraft:polished_blackstone_bricks", "minecraft:cracked_polished_blackstone_bricks"], "minecraft:blackstone", seed=20)
    c = W // 2
    noir = ["minecraft:polished_blackstone_bricks", "minecraft:cracked_polished_blackstone_bricks", "minecraft:blackstone"]
    s.walls(2, F + 1, 2, W - 3, F + 10, W - 3, noir)
    for x in range(2, W - 2, 3):
        s.set(x, F + 11, 2, "minecraft:blackstone_wall"); s.set(x, F + 11, W - 3, "minecraft:blackstone_wall")
        s.set(2, F + 11, x, "minecraft:blackstone_wall"); s.set(W - 3, F + 11, x, "minecraft:blackstone_wall")
    s.clear(c - 2, F + 1, W - 3, c + 2, F + 7, W - 3)
    s.fill(c - 3, F + 8, W - 3, c + 3, F + 8, W - 3, "minecraft:crying_obsidian")
    # Pointes et tours
    for cx, cz in ((3, 3), (W - 4, 3), (3, W - 4), (W - 4, W - 4)):
        s.cylinder(cx, cz, 2, F + 1, F + 16, noir)
        for i in range(6):
            s.set(cx, F + 17 + i, cz, "minecraft:obsidian" if i < 4 else "minecraft:crying_obsidian")
        s.set(cx, F + 15, cz, "minecraft:soul_lantern")
    # Donjon : la Tour des Huit
    s.hollow(c - 6, F, c - 6, c + 6, F + 20, c + 6, noir, floor="minecraft:polished_blackstone")
    s.clear(c - 1, F + 1, c + 6, c + 1, F + 4, c + 6)
    for y in (F + 7, F + 14):
        s.fill(c - 5, y, c - 5, c + 5, y, c + 5, "minecraft:polished_blackstone_slab[type=top]")
        s.fill(c - 2, y, c - 2, c + 2, y, c + 2, "minecraft:air")
    s.cone(c, c, 6, F + 21, ["minecraft:obsidian", "minecraft:blackstone"])
    # Étoile du Chaos (8 branches) au sol
    for dx, dz in ((1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, -1), (1, -1), (-1, 1)):
        for k in range(1, 5):
            s.set(c + dx * k, F, c + dz * k, "minecraft:red_concrete")
    s.set(c, F, c, "minecraft:crying_obsidian"); s.set(c, F + 1, c, "minecraft:soul_campfire")
    s.chest(c - 4, F + 1, c - 4, L + "citadelle_chaos", "south"); s.chest(c + 4, F + 15, c + 4, L + "citadelle_chaos", "north")
    s.chest(c - 4, F + 8, c + 4, L + "citadelle_chaos", "north")
    s.set(c + 3, F + 1, c - 4, "minecraft:soul_lantern")
    s.mob(c, F + 15, c, "zombie", "chaos_seigneur")
    s.mob(c + 3, F + 1, c + 3, "zombie", "chaos_guerrier", 3)
    s.mob(8, F + 1, W - 8, "zombie", "chaos_guerrier", 2)
    s.mob(W - 9, F + 1, 9, "skeleton", "tzaangor", 2)
    return s


def ziggurat_hashut():
    W = 33
    s = base(W, 28, W, ["minecraft:polished_blackstone", "minecraft:blackstone"], "minecraft:blackstone", seed=21)
    c = W // 2
    top = s.pyramid(4, 4, W - 5, W - 5, F + 1, ["minecraft:polished_blackstone_bricks", "minecraft:obsidian", "minecraft:polished_blackstone_bricks"], step=1)
    for y in range(F + 1, top):
        i = y - F - 1
        s.set(4 + i, y, c, "minecraft:magma_block"); s.set(W - 5 - i, y, c, "minecraft:magma_block")
    for i in range(0, top - F - 1):
        s.fill(c - 1, F + 1 + i, W - 5 - i, c + 1, F + 1 + i, W - 5 - i, "minecraft:polished_blackstone_stairs[facing=north]")
    # Taureau de Hashut stylisé au sommet
    s.fill(c - 2, top, c - 1, c + 2, top + 2, c + 1, "minecraft:gilded_blackstone")
    s.set(c - 3, top + 3, c, "minecraft:gold_block"); s.set(c + 3, top + 3, c, "minecraft:gold_block")
    s.set(c - 2, top + 3, c, "minecraft:gold_block"); s.set(c + 2, top + 3, c, "minecraft:gold_block")
    s.set(c, top + 3, c, "minecraft:magma_block"); s.set(c, top + 4, c, "minecraft:fire")
    # Forge intérieure
    s.clear(c - 3, F + 1, c - 3, c + 3, F + 4, c + 3)
    s.clear(c, F + 1, c + 4, c, F + 2, W - 3)
    s.fill(c - 3, F, c - 3, c + 3, F, c + 3, "minecraft:magma_block")
    s.set(c, F, c, "minecraft:lava"); s.set(c, F + 3, c, "minecraft:shroomlight")
    s.chest(c - 2, F + 1, c - 2, L + "ziggurat_hashut", "south"); s.set(c + 2, F + 1, c - 2, "minecraft:blast_furnace")
    s.mob(c, F + 1, W - 4, "zombie", "hashut", 3)
    s.mob(c, top, c + 3, "skeleton", "hashut_tireur", 2)
    return s


def repaire_skaven():
    W = 27
    s = base(W, 30, W, ["minecraft:coarse_dirt", "minecraft:gravel", "minecraft:mud"], "minecraft:dirt", seed=22)
    c = W // 2
    pourri = ["minecraft:cobblestone", "minecraft:mossy_cobblestone", "minecraft:cracked_stone_bricks", "minecraft:stone_bricks", "minecraft:air"]
    # Tour penchée et ruinée
    for y in range(F + 1, F + 22):
        off = (y - F) // 6
        s.cylinder(c + off, c, 4, y, y, pourri if y > F + 14 else pourri[:-1])
    s.clear(c, F + 1, c + 4, c + 1, F + 3, c + 4)
    # Cloche hurlante
    s.fill(c + 3, F + 22, c, c + 3, F + 24, c, "minecraft:spruce_fence"); s.set(c + 3, F + 21, c, "minecraft:bell[attachment=ceiling]")
    # Malepierre (froglight verte) en tas
    for (dx, dz) in ((-1, -1), (1, -2), (0, 1), (-2, 0)):
        s.set(c + dx, F + 1, c + dz, "minecraft:verdant_froglight")
    s.set(c, F + 2, c - 1, "minecraft:verdant_froglight")
    # Tunnels d'entrée
    for (x, z) in ((4, 4), (W - 5, 6), (5, W - 5)):
        s.fill(x - 1, F - 3, z - 1, x + 1, F, z + 1, "minecraft:air")
        s.set(x, F - 3, z, "minecraft:verdant_froglight")
        s.set(x - 1, F - 3, z, "minecraft:chest[facing=east]", {"id": "minecraft:chest", "LootTable": L + "repaire_skaven", "Items": []})
    s.chest(c - 2, F + 1, c + 1, L + "repaire_skaven", "east")
    for x in range(2, W - 2, 4):
        s.set(x, F + 1, W - 3, "minecraft:cobweb")
    s.mob(c - 1, F + 1, c, "zombie", "clanrat", 5)
    s.mob(c + 1, F + 8, c, "skeleton", "jezzail", 2)
    return s


# ======================================================================= MORT
def chateau_soulblight():
    W = 39
    s = base(W, 38, W, ["minecraft:deepslate_tiles", "minecraft:cracked_deepslate_tiles"], "minecraft:cobbled_deepslate", seed=23)
    c = W // 2
    pierre = ["minecraft:deepslate_bricks", "minecraft:cracked_deepslate_bricks", "minecraft:polished_deepslate"]
    s.walls(3, F + 1, 3, W - 4, F + 8, W - 4, pierre)
    s.crenel(3, F + 9, 3, W - 4, W - 4, "minecraft:deepslate_brick_wall")
    s.clear(c - 1, F + 1, W - 4, c + 1, F + 5, W - 4)
    s.fill(c - 1, F + 1, W - 4, c + 1, F + 1, W - 4, "minecraft:iron_bars")
    for cx, cz in ((3, 3), (W - 4, 3), (3, W - 4), (W - 4, W - 4)):
        s.cylinder(cx, cz, 3, F + 1, F + 18, pierre)
        y = s.cone(cx, cz, 4, F + 19, "minecraft:dark_oak_planks")
        s.set(cx, F + 17, cz, "minecraft:soul_lantern")
    # Donjon gothique
    s.hollow(c - 7, F, c - 9, c + 7, F + 16, c + 3, pierre, floor="minecraft:polished_deepslate")
    s.roof_gable(c - 7, c - 9, c + 7, c + 3, F + 17, "minecraft:deepslate_tile_stairs", "minecraft:deepslate_tiles", axis="z")
    s.clear(c - 1, F + 1, c + 3, c + 1, F + 5, c + 3)
    for z in range(c - 7, c + 2, 3):
        s.fill(c - 7, F + 4, z, c - 7, F + 8, z, "minecraft:red_stained_glass")
        s.fill(c + 7, F + 4, z, c + 7, F + 8, z, "minecraft:red_stained_glass")
    # Salle du trône : tapis rouge, trône, cercueils
    s.fill(c, F, c - 7, c, F, c + 2, "minecraft:red_concrete")
    s.fill(c - 1, F + 1, c - 8, c + 1, F + 1, c - 8, "minecraft:polished_blackstone")
    s.set(c, F + 2, c - 8, "minecraft:polished_blackstone_stairs[facing=south]")
    s.fill(c - 1, F + 2, c - 8, c - 1, F + 4, c - 8, "minecraft:gold_block"); s.fill(c + 1, F + 2, c - 8, c + 1, F + 4, c - 8, "minecraft:gold_block")
    for dx in (-5, 5):
        s.fill(c + dx, F + 1, c - 6, c + dx, F + 1, c - 4, "minecraft:dark_oak_planks")
    s.chest(c - 4, F + 1, c - 8, L + "chateau_soulblight", "south"); s.chest(c + 4, F + 1, c - 8, L + "chateau_soulblight", "south")
    s.set(c, F + 10, c - 3, "minecraft:iron_chain"); s.set(c, F + 9, c - 3, "minecraft:soul_lantern[hanging=true]")
    # Cimetière de la cour
    for x in range(6, W - 6, 4):
        for z in (W - 9, W - 7):
            s.set(x, F + 1, z, "minecraft:cobblestone_wall"); s.set(x, F, z + 1, "minecraft:coarse_dirt")
    s.mob(c, F + 1, c - 6, "zombie", "vampire")
    s.mob(c - 3, F + 1, c, "skeleton", "deathrattle", 3)
    s.mob(8, F + 1, W - 9, "zombie", "mort_sylvanie", 3)
    return s


def ossuaire_ossiarch():
    W = 31
    s = base(W, 26, W, ["minecraft:bone_block[axis=y]", "minecraft:smooth_sandstone"], "minecraft:sandstone", seed=24)
    c = W // 2
    os = ["minecraft:bone_block[axis=y]", "minecraft:bone_block[axis=y]", "minecraft:calcite"]
    s.walls(2, F + 1, 2, W - 3, F + 7, W - 3, os)
    for x in range(2, W - 2, 2):
        s.set(x, F + 8, 2, "minecraft:skeleton_skull"); s.set(x, F + 8, W - 3, "minecraft:skeleton_skull")
    s.clear(c - 1, F + 1, W - 3, c + 1, F + 4, W - 3)
    # Ziggurat d'ossements
    top = s.pyramid(c - 7, c - 7, c + 7, c + 7, F + 1, os, step=1)
    s.clear(c - 3, F + 1, c - 3, c + 3, F + 3, c + 3); s.clear(c, F + 1, c + 4, c, F + 2, c + 7)
    s.chest(c, F + 1, c - 2, L + "ossuaire_ossiarch", "south")
    s.set(c, F + 3, c, "minecraft:soul_lantern")
    for (dx, dz) in ((-11, -11), (11, -11), (-11, 11), (11, 11)):
        s.fill(c + dx, F + 1, c + dz, c + dx, F + 9, c + dz, "minecraft:bone_block[axis=y]")
        s.set(c + dx, F + 10, c + dz, "minecraft:wither_skeleton_skull")
    s.mob(c + 5, F + 1, c + 9, "skeleton", "mortek", 4)
    return s


def cimetiere_nighthaunt():
    W = 25
    s = base(W, 16, W, ["minecraft:podzol", "minecraft:coarse_dirt", "minecraft:soul_soil"], "minecraft:dirt", seed=25)
    c = W // 2
    s.walls(1, F + 1, 1, W - 2, F + 2, W - 2, ["minecraft:cobblestone_wall", "minecraft:mossy_cobblestone_wall"])
    s.clear(c, F + 1, W - 2, c, F + 2, W - 2)
    for x in range(4, W - 4, 3):
        for z in range(4, W - 5, 4):
            s.set(x, F + 1, z, s.rng.choice(["minecraft:cobblestone_wall", "minecraft:mossy_cobblestone_wall", "minecraft:stone_brick_wall"]))
            s.set(x, F, z + 1, "minecraft:soul_soil")
    # Mausolée
    s.hollow(c - 3, F, 2, c + 3, F + 6, 7, ["minecraft:stone_bricks", "minecraft:mossy_stone_bricks"], floor="minecraft:polished_andesite")
    s.roof_gable(c - 3, 2, c + 3, 7, F + 7, "minecraft:stone_brick_stairs", "minecraft:stone_bricks", axis="z")
    s.clear(c, F + 1, 7, c, F + 2, 7)
    s.chest(c, F + 1, 3, L + "cimetiere_nighthaunt", "south")
    s.set(c - 2, F + 1, 3, "minecraft:soul_campfire"); s.set(c + 2, F + 1, 3, "minecraft:soul_campfire")
    s.mob(c, F + 1, c + 3, "zombie", "chainrasp", 3)
    s.mob(c - 4, F + 1, c, "skeleton", "glaivewraith", 2)
    return s


# ======================================================================= DESTRUCTION
def camp_orruk():
    W = 29
    s = base(W, 16, W, ["minecraft:coarse_dirt", "minecraft:dirt_path", "minecraft:packed_mud"], "minecraft:dirt", seed=26)
    c = W // 2
    s.walls(1, F + 1, 1, W - 2, F + 4, W - 2, ["minecraft:stripped_spruce_log", "minecraft:spruce_log", "minecraft:spruce_fence"])
    for x in range(1, W - 1, 2):
        s.set(x, F + 5, 1, "minecraft:pointed_dripstone[vertical_direction=up]")
        s.set(x, F + 5, W - 2, "minecraft:pointed_dripstone[vertical_direction=up]")
    s.clear(c - 1, F + 1, W - 2, c + 1, F + 4, W - 2)
    # Huttes de ferraille
    for (x, z) in ((4, 4), (19, 4), (4, 18), (19, 18)):
        s.hollow(x, F, z, x + 5, F + 4, z + 5, ["minecraft:iron_block", "minecraft:spruce_planks", "minecraft:exposed_cut_copper"], floor="minecraft:coarse_dirt")
        s.clear(x + 2, F + 1, z + 5 if z < c else z, x + 3, F + 2, z + 5 if z < c else z)
        s.set(x + 1, F + 1, z + 1, "minecraft:red_bed[facing=north,part=head]")
        s.set(x + 1, F + 1, z + 2, "minecraft:red_bed[facing=north,part=foot]")
        s.barrel(x + 4, F + 1, z + 1, L + "camp_orruk")
    # Feu de camp, trophées, totem
    s.set(c, F + 1, c, "minecraft:campfire"); s.fill(c - 1, F, c - 1, c + 1, F, c + 1, "minecraft:cobblestone")
    s.fill(c, F + 1, c - 5, c, F + 7, c - 5, "minecraft:stripped_spruce_log")
    s.set(c, F + 8, c - 5, "minecraft:skeleton_skull"); s.set(c - 1, F + 6, c - 5, "minecraft:skeleton_skull")
    s.set(c + 1, F + 6, c - 5, "minecraft:zombie_head")
    s.chest(c + 2, F + 1, c - 5, L + "camp_orruk", "west")
    s.banner_pole(3, F + 5, c, 4, "red"); s.banner_pole(W - 4, F + 5, c, 4, "yellow")
    s.mob(c + 2, F + 1, c + 2, "zombie", "megaboss")
    s.mob(c - 3, F + 1, c + 3, "zombie", "brute", 4)
    return s


def fort_kruleboyz():
    W = 29
    s = Struct(W, 22, W, 27)
    c = W // 2
    # Pilotis dans le marais
    for x in range(3, W - 3, 5):
        for z in range(3, W - 3, 5):
            s.fill(x, 0, z, x, 7, z, "minecraft:mangrove_log")
    s.fill(2, 8, 2, W - 3, 8, W - 3, ["minecraft:mangrove_planks", "minecraft:mud_bricks", "minecraft:mangrove_planks"])
    s.walls(2, 9, 2, W - 3, 11, W - 3, ["minecraft:mangrove_roots", "minecraft:mud_bricks", "minecraft:mangrove_log"])
    for x in range(2, W - 2, 2):
        s.set(x, 12, 2, "minecraft:mangrove_fence"); s.set(x, 12, W - 3, "minecraft:mangrove_fence")
    s.clear(c - 1, 9, W - 3, c + 1, 11, W - 3)
    for i in range(0, 9):  # rampe
        s.fill(c - 1, 8 - i, W - 2 + i, c + 1, 8 - i, W - 2 + i, "minecraft:mangrove_planks") if W - 2 + i < W else None
    for y in range(0, 9):
        s.set(c, y, W - 2, "minecraft:ladder[facing=north]") if y < 8 else None
    s.fill(c, 0, W - 1, c, 8, W - 1, "minecraft:mangrove_log")
    # Hutte du chef
    s.hollow(c - 4, 8, c - 4, c + 4, 14, c + 4, ["minecraft:mud_bricks", "minecraft:packed_mud"], floor="minecraft:mangrove_planks")
    s.cone(c, c, 6, 15, ["minecraft:hay_block", "minecraft:mangrove_roots"])
    s.clear(c, 9, c + 4, c, 10, c + 4)
    s.chest(c - 2, 9, c - 3, L + "fort_kruleboyz", "south"); s.set(c + 2, 9, c - 3, "minecraft:brewing_stand")
    s.set(c, 12, c, "minecraft:lantern[hanging=true]")
    s.set(5, 9, 5, "minecraft:cauldron"); s.barrel(6, 9, 5, L + "fort_kruleboyz")
    s.mob(c + 6, 9, c + 6, "zombie", "gutrippa", 4)
    s.mob(5, 9, W - 6, "skeleton", "kb_archer", 2)
    return s


def antre_gitz():
    W = 27
    s = base(W, 24, W, ["minecraft:mycelium", "minecraft:podzol", "minecraft:moss_block"], "minecraft:dirt", seed=28)
    c = W // 2
    # Champignons géants
    for (x, z, h, cap) in ((6, 6, 9, "red"), (W - 7, 8, 12, "brown"), (8, W - 7, 7, "red"), (c, c, 14, "red")):
        s.fill(x, F + 1, z, x, F + h, z, "minecraft:mushroom_stem")
        s.cylinder(x, z, 4 if h > 10 else 3, F + h + 1, F + h + 1, f"minecraft:{cap}_mushroom_block", hollow=False)
        s.cylinder(x, z, 3 if h > 10 else 2, F + h + 2, F + h + 2, f"minecraft:{cap}_mushroom_block", hollow=False)
        s.set(x, F + h, z, "minecraft:shroomlight")
    # Gîte creusé sous le grand champignon
    s.cylinder(c, c, 4, F + 1, F + 4, ["minecraft:mushroom_stem", "minecraft:brown_mushroom_block"])
    s.clear(c, F + 1, c + 4, c, F + 2, c + 4)
    s.set(c, F + 1, c, "minecraft:mushroom_stem")
    s.chest(c - 2, F + 1, c, L + "antre_gitz", "east")
    for x in range(3, W - 3, 3):
        s.set(x, F + 1, W - 4, s.rng.choice(["minecraft:red_mushroom", "minecraft:brown_mushroom", "minecraft:cobweb"]))
    # Lune de pierre (la Mauvaise Lune)
    s.mob(c + 4, F + 1, c + 5, "zombie", "grot", 5)
    s.mob(c - 5, F + 1, c - 5, "spider", "arachnarok")
    return s


def campement_ogor():
    W = 27
    s = base(W, 16, W, ["minecraft:coarse_dirt", "minecraft:dirt", "minecraft:rooted_dirt"], "minecraft:dirt", seed=29)
    c = W // 2
    # Grand foyer avec broche
    s.fill(c - 2, F, c - 2, c + 2, F, c + 2, "minecraft:cobblestone")
    s.set(c, F + 1, c, "minecraft:campfire")
    s.fill(c - 2, F + 1, c, c - 2, F + 3, c, "minecraft:oak_fence"); s.fill(c + 2, F + 1, c, c + 2, F + 3, c, "minecraft:oak_fence")
    s.fill(c - 2, F + 4, c, c + 2, F + 4, c, "minecraft:oak_fence")
    s.set(c, F + 3, c, "minecraft:hay_block")
    # Tentes en peaux
    for (x, z, col) in ((3, 3, "brown"), (W - 9, 3, "brown"), (3, W - 9, "white"), (W - 9, W - 9, "brown")):
        for i in range(4):
            s.fill(x + i, F + 1 + i, z, x + 6 - i, F + 1 + i, z + 5, f"minecraft:{col}_wool")
            s.fill(x + i + 1, F + 1 + i, z, x + 5 - i, F + 1 + i, z + 5, "minecraft:air") if i < 3 else None
        s.barrel(x + 3, F + 1, z + 2, L + "campement_ogor")
    # Os et trophées
    for (x, z) in ((c - 6, c + 6), (c + 6, c - 6), (c + 7, c + 5)):
        s.fill(x, F + 1, z, x, F + 2, z, "minecraft:bone_block[axis=y]")
    s.chest(c + 3, F + 1, c + 3, L + "campement_ogor", "north")
    s.mob(c + 4, F + 1, c - 3, "zombie", "gutbuster", 3)
    s.mob(c - 4, F + 1, c + 4, "skeleton", "ogor_chasseur", 1)
    return s


BUILDERS = {
    "forteresse_stormcast": forteresse_stormcast, "cite_sigmar": cite_sigmar, "camp_orruk": camp_orruk,
    "fort_kruleboyz": fort_kruleboyz, "temple_seraphon": temple_seraphon, "bosquet_sylvaneth": bosquet_sylvaneth,
    "magmahold": magmahold, "port_kharadron": port_kharadron, "ziggurat_hashut": ziggurat_hashut,
    "citadelle_chaos": citadelle_chaos, "repaire_skaven": repaire_skaven, "chateau_soulblight": chateau_soulblight,
    "ossuaire_ossiarch": ossuaire_ossiarch, "cimetiere_nighthaunt": cimetiere_nighthaunt,
    "sanctuaire_lumineth": sanctuaire_lumineth, "temple_khaine": temple_khaine, "ruines_idoneth": ruines_idoneth,
    "antre_gitz": antre_gitz, "campement_ogor": campement_ogor,
}

# Hauteur de départ (le sol du gabarit doit tomber au niveau du terrain)
START_Y = {k: -F for k in BUILDERS}
START_Y.update({"port_kharadron": -1, "fort_kruleboyz": -2, "ruines_idoneth": -1})
