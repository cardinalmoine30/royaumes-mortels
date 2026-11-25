# -*- coding: utf-8 -*-
"""Grandes constructions détaillées : forteresse Foudroyés, cité de Aurion, château Sanguinaire, citadelle du Chaos."""
from nbtgen import Struct
from details import (rempart, meurtrieres, tour, tour_carree, fenetre_arc, lustre, table, tapis,
                     banniere_murale, cheminee, bibliotheque, jardiniere, statue_guerrier)

F = 4
L = "royaumes:coffres/"


def base(sx, sy, sz, sol, fond, seed):
    s = Struct(sx, sy, sz, seed)
    s.foundation(0, 0, sx - 1, sz - 1, F - 1, F, fond)
    s.fill(0, F, 0, sx - 1, F, sz - 1, sol)
    s.clear(0, F + 1, 0, sx - 1, F + 8, sz - 1)
    return s


# =================================================================== FORTERESSE STORMCAST (55×55)
def forteresse_stormcast():
    W = 55
    s = base(W, 52, W, ["minecraft:smooth_quartz", "minecraft:quartz_bricks", "minecraft:polished_diorite"],
             "minecraft:stone_bricks", 31)
    murs = ["minecraft:quartz_bricks", "minecraft:quartz_bricks", "minecraft:smooth_quartz", "minecraft:calcite"]
    c = W // 2
    # ---- Remparts extérieurs
    rempart(s, 3, 3, W - 4, W - 4, F + 1, 11, murs, "minecraft:quartz_pillar", "minecraft:quartz_stairs",
            "minecraft:diorite_wall", "minecraft:smooth_quartz_slab[type=top]")
    meurtrieres(s, 3, 3, W - 4, W - 4, F + 5, pas=6, bloc="minecraft:blue_stained_glass_pane")
    # liseré d'or
    for x in range(3, W - 3):
        s.set(x, F + 9, 3, "minecraft:gold_block"); s.set(x, F + 9, W - 4, "minecraft:gold_block")
        s.set(3, F + 9, x, "minecraft:gold_block"); s.set(W - 4, F + 9, x, "minecraft:gold_block")
    # ---- Barbacane / grande porte au sud
    s.fill(c - 5, F + 1, W - 6, c + 5, F + 14, W - 2, murs)
    s.fill(c - 4, F + 14, W - 5, c + 4, F + 14, W - 3, "minecraft:smooth_quartz")
    s.crenel(c - 5, F + 15, W - 6, c + 5, W - 2, "minecraft:diorite_wall")
    s.clear(c - 2, F + 1, W - 7, c + 2, F + 7, W - 1)
    for x in range(c - 2, c + 3):
        s.set(x, F + 8, W - 2, "minecraft:quartz_stairs[facing=north,half=top]")
    s.fill(c - 2, F + 6, W - 4, c + 2, F + 7, W - 4, "minecraft:iron_bars")  # herse levée
    s.fill(c - 1, F + 9, W - 2, c + 1, F + 11, W - 2, "minecraft:gold_block")
    s.set(c, F + 10, W - 2, "minecraft:lapis_block")
    for dx in (-4, 4):
        banniere_murale(s, c + dx, F + 10, W - 1, "blue", "south")
        s.set(c + dx, F + 6, W - 1, "minecraft:lantern")
    # ---- Tours d'angle et tours intermédiaires
    for cx, cz in ((4, 4), (W - 5, 4), (4, W - 5), (W - 5, W - 5)):
        tour(s, cx, cz, 4, F, 20, murs, "minecraft:lapis_block", pointe="minecraft:lightning_rod",
             fenetre="minecraft:blue_stained_glass_pane", plancher="minecraft:birch_planks")
        s.set(cx, F + 19, cz, "minecraft:sea_lantern")
    for cx, cz in ((c, 4), (4, c), (W - 5, c)):
        tour(s, cx, cz, 3, F, 15, murs, "minecraft:lapis_block", pointe="minecraft:lightning_rod",
             fenetre="minecraft:blue_stained_glass_pane", plancher="minecraft:birch_planks")
    # ---- Cour : allée, jardins, fontaine, statues
    s.fill(c - 2, F, c + 8, c + 2, F, W - 7, "minecraft:polished_diorite")
    for z in range(c + 9, W - 7, 3):
        s.set(c - 3, F + 1, z, "minecraft:diorite_wall"); s.set(c - 3, F + 2, z, "minecraft:lantern")
        s.set(c + 3, F + 1, z, "minecraft:diorite_wall"); s.set(c + 3, F + 2, z, "minecraft:lantern")
    # fontaine
    s.cylinder(c - 13, c + 13, 3, F + 1, F + 1, "minecraft:quartz_bricks", hollow=True, inside="minecraft:water")
    s.fill(c - 13, F + 1, c + 13, c - 13, F + 3, c + 13, "minecraft:quartz_pillar")
    s.set(c - 13, F + 4, c + 13, "minecraft:gold_block"); s.set(c - 13, F + 5, c + 13, "minecraft:sea_lantern")
    # statues de Foudroyés
    for (x, z) in ((c + 12, c + 12), (c + 12, c + 18)):
        statue_guerrier(s, x, F + 1, z, "minecraft:gold_block", "minecraft:lapis_block", "minecraft:lightning_rod",
                        "minecraft:quartz_bricks")
    # jardins
    for x in range(8, 18, 2):
        for z in (c + 20, c + 21):
            s.set(x, F, z, "minecraft:grass_block")
            s.set(x, F + 1, z, s.rng.choice(["minecraft:white_tulip", "minecraft:cornflower", "minecraft:lily_of_the_valley"]))
    # ---- Casernes (ouest) : dortoir à 2 niveaux
    s.hollow(7, F, 8, 18, F + 10, 22, murs, floor="minecraft:birch_planks")
    s.fill(8, F + 5, 9, 17, F + 5, 21, "minecraft:birch_planks")
    s.roof_gable(7, 8, 18, 22, F + 11, "minecraft:quartz_stairs", "minecraft:lapis_block", axis="z")
    s.clear(18, F + 1, 14, 18, F + 3, 15)
    for z in range(10, 21, 3):
        s.set(8, F + 1, z, "minecraft:blue_bed[facing=east,part=foot]"); s.set(9, F + 1, z, "minecraft:blue_bed[facing=east,part=head]")
        s.set(8, F + 6, z, "minecraft:blue_bed[facing=east,part=foot]"); s.set(9, F + 6, z, "minecraft:blue_bed[facing=east,part=head]")
        fenetre_arc(s, 7, F + 2, z, "z", 2, "minecraft:blue_stained_glass_pane", "minecraft:quartz_stairs")
    s.set(17, F + 1, 9, "minecraft:ladder[facing=west]")
    for y in range(F + 1, F + 6):
        s.set(17, y, 21, "minecraft:ladder[facing=west]")
    s.set(17, F + 5, 21, "minecraft:ladder[facing=west]")
    s.chest(16, F + 6, 9, L + "forteresse_stormcast", "south")
    lustre(s, 13, F + 5, 15, 1); lustre(s, 13, F + 10, 15, 1)
    # ---- Forge et armurerie (est)
    s.hollow(W - 19, F, 8, W - 8, F + 8, 20, murs, floor="minecraft:polished_andesite")
    s.roof_gable(W - 19, 8, W - 8, 20, F + 9, "minecraft:quartz_stairs", "minecraft:lapis_block", axis="z")
    s.clear(W - 19, F + 1, 13, W - 19, F + 3, 14)
    cheminee(s, W - 9, F + 1, 14, "west", "minecraft:polished_blackstone_bricks", 8)
    s.set(W - 11, F + 1, 10, "minecraft:anvil"); s.set(W - 12, F + 1, 10, "minecraft:smithing_table")
    s.set(W - 13, F + 1, 10, "minecraft:blast_furnace"); s.set(W - 14, F + 1, 10, "minecraft:grindstone[face=floor]")
    s.set(W - 15, F + 1, 10, "minecraft:water_cauldron[level=3]")
    for z in (17, 18, 19):
        s.barrel(W - 10, F + 1, z, L + "forteresse_stormcast")
    lustre(s, W - 14, F + 8, 14, 2)
    # ---- Temple-donjon de Aurion (centre nord)
    k0, k1, kz0, kz1 = c - 10, c + 10, 9, c + 7
    s.hollow(k0, F, kz0, k1, F + 20, kz1, murs, floor="minecraft:polished_diorite")
    for x in range(k0, k1 + 1, 4):
        s.fill(x, F, kz1, x, F + 20, kz1, "minecraft:quartz_pillar")
        s.fill(x, F, kz0, x, F + 20, kz0, "minecraft:quartz_pillar")
    for z in range(kz0, kz1 + 1, 4):
        s.fill(k0, F, z, k0, F + 20, z, "minecraft:quartz_pillar")
        s.fill(k1, F, z, k1, F + 20, z, "minecraft:quartz_pillar")
    for x in range(k0 + 2, k1 - 1, 4):
        fenetre_arc(s, x, F + 6, kz0, "x", 5, "minecraft:light_blue_stained_glass_pane", "minecraft:quartz_stairs")
    for z in range(kz0 + 2, kz1 - 1, 4):
        fenetre_arc(s, k0, F + 6, z, "z", 5, "minecraft:light_blue_stained_glass_pane", "minecraft:quartz_stairs")
        fenetre_arc(s, k1, F + 6, z, "z", 5, "minecraft:light_blue_stained_glass_pane", "minecraft:quartz_stairs")
    s.walls(k0, F + 20, kz0, k1, F + 20, kz1, "minecraft:gold_block")
    s.roof_gable(k0, kz0, k1, kz1, F + 21, "minecraft:quartz_stairs", "minecraft:lapis_block", axis="x")
    # porche
    s.clear(c - 2, F + 1, kz1, c + 2, F + 8, kz1)
    for x in range(c - 2, c + 3):
        s.set(x, F + 9, kz1, "minecraft:quartz_stairs[facing=north,half=top]")
    s.fill(c - 3, F + 10, kz1, c + 3, F + 10, kz1, "minecraft:gold_block")
    # nef : colonnade, tapis, bancs
    tapis(s, c - 1, kz0 + 6, c + 1, kz1 - 1, F + 1, "blue")
    for z in range(kz0 + 7, kz1 - 2, 2):
        for x in (c - 6, c - 5, c - 4, c + 4, c + 5, c + 6):
            s.set(x, F + 1, z, "minecraft:birch_stairs[facing=north]")
    for z in range(kz0 + 3, kz1, 5):
        for x in (c - 8, c + 8):
            s.fill(x, F + 1, z, x, F + 19, z, "minecraft:quartz_pillar")
            s.set(x, F + 12, z, "minecraft:sea_lantern")
    for z in range(kz0 + 6, kz1 - 1, 6):
        lustre(s, c, F + 20, z, 4, "minecraft:sea_lantern")
    # choeur : autel, statue de Aurion, comète à deux queues
    s.fill(c - 4, F + 1, kz0 + 1, c + 4, F + 1, kz0 + 4, "minecraft:smooth_quartz")
    s.fill(c - 1, F + 2, kz0 + 3, c + 1, F + 2, kz0 + 3, "minecraft:gold_block")
    statue_guerrier(s, c, F + 2, kz0 + 2, "minecraft:gold_block", "minecraft:gold_block", "minecraft:lightning_rod",
                    "minecraft:lapis_block")
    for y, dx in ((F + 14, 0), (F + 15, -1), (F + 15, 1), (F + 16, -2), (F + 16, 2)):
        s.set(c + dx, y, kz0 + 1, "minecraft:gold_block")
    s.set(c, F + 13, kz0 + 1, "minecraft:sea_lantern")
    for dx in (-3, 3):
        s.set(c + dx, F + 2, kz0 + 4, "minecraft:white_candle[candles=4,lit=true]")
    s.chest(c - 3, F + 2, kz0 + 1, L + "forteresse_stormcast", "south")
    s.chest(c + 3, F + 2, kz0 + 1, L + "forteresse_stormcast", "south")
    bibliotheque(s, k0 + 1, F + 1, kz1 - 5, k0 + 1, F + 4, kz1 - 1)
    s.set(k0 + 2, F + 1, kz1 - 3, "minecraft:lectern[facing=east]")
    s.set(k1 - 2, F + 1, kz1 - 3, "minecraft:enchanting_table")
    for dz in (-2, 2):
        banniere_murale(s, k0 + 1, F + 9, c + dz - 6, "blue", "east")
        banniere_murale(s, k1 - 1, F + 9, c + dz - 6, "blue", "west")
    # ---- Garnison
    s.mob(c, F + 2, kz0 + 6, "zombie", "sc_lord")
    s.mob(c - 5, F + 1, c + 2, "zombie", "sc_liberator", 3)
    s.mob(c + 2, F + 1, W - 10, "zombie", "sc_liberator", 2)
    s.mob(12, F + 1, 15, "zombie", "sc_liberator", 2)
    s.mob(W - 13, F + 1, 15, "skeleton", "sc_judicator", 2)
    s.mob(4, F + 13, 4, "skeleton", "sc_judicator", 1)
    s.mob(W - 5, F + 13, W - 5, "skeleton", "sc_judicator", 1)
    return s


# =================================================================== CITÉ DE SIGMAR (63×63)
def _maison(s, x, z, w, d, etages, porte_sud, style):
    murs, poutre, toit_e, toit_p, sol = style
    h = 4 * etages
    s.hollow(x, F, z, x + w, F + h, z + d, murs, floor=sol)
    for (xx, zz) in ((x, z), (x + w, z), (x, z + d), (x + w, z + d)):
        s.fill(xx, F + 1, zz, xx, F + h, zz, poutre)
    for e in range(1, etages):
        y = F + 4 * e
        s.fill(x, y, z, x + w, y, z + d, poutre)
        s.fill(x + 1, y, z + 1, x + w - 1, y, z + d - 1, sol)
        s.set(x + w - 1, y, z + 1, "minecraft:air")
        for yy in range(y - 3, y + 1):
            s.set(x + w - 1, yy, z + 1, "minecraft:ladder[facing=west]")
    s.fill(x, F + h, z, x + w, F + h, z + d, poutre)
    s.fill(x + 1, F + h, z + 1, x + w - 1, F + h, z + d - 1, sol)
    s.roof_gable(x, z, x + w, z + d, F + h + 1, toit_e, toit_p, axis="x")
    # fenêtres et volets
    for e in range(etages):
        y = F + 2 + 4 * e
        for xx in range(x + 2, x + w - 1, 3):
            for zz, f in ((z, "north"), (z + d, "south")):
                s.set(xx, y, zz, "minecraft:glass_pane")
        s.set(x, y, z + d // 2, "minecraft:glass_pane"); s.set(x + w, y, z + d // 2, "minecraft:glass_pane")
    # porte + perron
    pz = z + d if porte_sud else z
    face = "south" if porte_sud else "north"
    s.door(x + w // 2, F + 1, pz, "minecraft:spruce_door", face)
    # intérieur
    s.set(x + 1, F + 1, z + 1, "minecraft:crafting_table")
    s.set(x + 2, F + 1, z + 1, "minecraft:furnace[facing=south]")
    s.set(x + 1, F + 1, z + d - 1, "minecraft:barrel[facing=up]")
    lustre(s, x + w // 2, F + 4, z + d // 2, 1)
    if etages > 1:
        s.set(x + 2, F + 5, z + d - 2, "minecraft:red_bed[facing=north,part=head]")
        s.set(x + 2, F + 5, z + d - 1, "minecraft:red_bed[facing=north,part=foot]")
        jardiniere(s, x + 2, F + 5, z + 1, "poppy")
    return h


def cite_sigmar():
    W = 63
    s = base(W, 34, W, ["minecraft:cobblestone", "minecraft:andesite", "minecraft:stone"], "minecraft:stone", 32)
    c = W // 2
    mur = ["minecraft:stone_bricks", "minecraft:stone_bricks", "minecraft:mossy_stone_bricks", "minecraft:cracked_stone_bricks"]
    rempart(s, 2, 2, W - 3, W - 3, F + 1, 9, mur, "minecraft:chiseled_stone_bricks", "minecraft:stone_brick_stairs",
            "minecraft:stone_brick_wall", "minecraft:stone_brick_slab[type=top]")
    meurtrieres(s, 2, 2, W - 3, W - 3, F + 4, pas=7)
    for cx, cz in ((3, 3), (W - 4, 3), (3, W - 4), (W - 4, W - 4)):
        tour(s, cx, cz, 3, F, 15, mur, "minecraft:dark_oak_planks", pointe="minecraft:oak_fence",
             fenetre="minecraft:glass_pane")
    # portes nord et sud avec tours de garde
    for zg, face in ((2, "north"), (W - 3, "south")):
        s.clear(c - 2, F + 1, zg - 1, c + 2, F + 5, zg + 1)
        for dx in (-4, 4):
            tour(s, c + dx, zg, 2, F, 13, mur, "minecraft:dark_oak_planks", pointe="minecraft:oak_fence")
        for x in range(c - 2, c + 3):
            s.set(x, F + 6, zg, "minecraft:stone_brick_stairs[facing=%s,half=top]" % ("south" if face == "north" else "north"))
    # rues
    pave = ["minecraft:polished_andesite", "minecraft:stone_bricks", "minecraft:andesite"]
    s.fill(c - 2, F, 3, c + 2, F, W - 4, pave)
    s.fill(3, F, c - 2, W - 4, F, c + 2, pave)
    for k in (14, W - 15):
        s.fill(k - 1, F, 3, k + 1, F, W - 4, pave); s.fill(3, F, k - 1, W - 4, F, k + 1, pave)
    # lampadaires
    for i in range(6, W - 6, 6):
        for (x, z) in ((c + 3, i), (c - 3, i), (i, c + 3), (i, c - 3)):
            if abs(x - c) <= 3 and abs(z - c) <= 3:
                continue
            s.fill(x, F + 1, z, x, F + 3, z, "minecraft:spruce_fence")
            s.set(x, F + 4, z, "minecraft:lantern")
    # quartiers de maisons
    styles = [
        (["minecraft:white_terracotta", "minecraft:white_terracotta", "minecraft:mushroom_stem"], "minecraft:spruce_log",
         "minecraft:dark_oak_stairs", "minecraft:dark_oak_planks", "minecraft:spruce_planks"),
        (["minecraft:stone_bricks", "minecraft:cobblestone"], "minecraft:dark_oak_log",
         "minecraft:spruce_stairs", "minecraft:spruce_planks", "minecraft:oak_planks"),
        (["minecraft:bricks", "minecraft:bricks", "minecraft:white_terracotta"], "minecraft:oak_log",
         "minecraft:deepslate_tile_stairs", "minecraft:deepslate_tiles", "minecraft:birch_planks"),
    ]
    lots = [(4, 5), (17, 5), (35, 5), (49, 5), (4, 17), (49, 17), (4, 35), (49, 35),
            (4, 49), (17, 49), (35, 49), (49, 49), (17, 35), (35, 35)]
    for i, (x, z) in enumerate(lots):
        w, d = (8, 7) if i % 2 == 0 else (9, 6)
        if x + w > W - 4:
            x = W - 4 - w
        if z + d > W - 4:
            z = W - 4 - d
        _maison(s, x, z, w, d, 2 if i % 3 != 2 else 1, z < c, styles[i % 3])
        if i % 2 == 0:
            s.chest(x + w - 1, F + 1, z + d - 1, L + "cite_sigmar", "west")
        s.mob(x + 3, F + 1, z + 3, "villager", "habitant")
    # Taverne de la Comète (lot nord-ouest intérieur)
    tx, tz = 17, 17
    s.hollow(tx, F, tz, tx + 11, F + 9, tz + 9, styles[1][0], floor="minecraft:spruce_planks")
    s.fill(tx + 1, F + 5, tz + 1, tx + 10, F + 5, tz + 8, "minecraft:spruce_planks")
    s.roof_gable(tx, tz, tx + 11, tz + 9, F + 10, "minecraft:spruce_stairs", "minecraft:spruce_planks", axis="x")
    s.door(tx + 5, F + 1, tz + 9, "minecraft:spruce_door", "south")
    s.fill(tx + 1, F + 1, tz + 1, tx + 6, F + 1, tz + 1, "minecraft:barrel[facing=up]")
    s.fill(tx + 1, F + 2, tz + 1, tx + 6, F + 2, tz + 1, "minecraft:barrel[facing=up]")
    s.fill(tx + 1, F + 1, tz + 3, tx + 6, F + 1, tz + 3, "minecraft:spruce_slab[type=top]")  # comptoir
    table(s, tx + 3, tz + 6, tx + 7, tz + 6, F + 1, "minecraft:spruce_slab[type=top]", "minecraft:spruce_stairs")
    cheminee(s, tx + 10, F + 1, tz + 5, "west", "minecraft:bricks", 9)
    lustre(s, tx + 5, F + 5, tz + 5, 1)
    for y in range(F + 1, F + 6):
        s.set(tx + 1, y, tz + 8, "minecraft:ladder[facing=east]")
    s.chest(tx + 9, F + 1, tz + 1, L + "cite_sigmar", "south")
    s.mob(tx + 4, F + 1, tz + 4, "villager", "habitant", 2)
    # Grand temple de Aurion (côté est intérieur)
    gx, gz = 35, 17
    s.hollow(gx, F, gz, gx + 11, F + 14, gz + 11, ["minecraft:polished_diorite", "minecraft:calcite"], floor="minecraft:polished_andesite")
    for (xx, zz) in ((gx, gz), (gx + 11, gz), (gx, gz + 11), (gx + 11, gz + 11)):
        s.fill(xx, F, zz, xx, F + 16, zz, "minecraft:quartz_pillar")
    s.pyramid(gx, gz, gx + 11, gz + 11, F + 15, "minecraft:blue_terracotta")
    s.clear(gx + 5, F + 1, gz + 11, gx + 6, F + 4, gz + 11)
    for xx in (gx + 2, gx + 8):
        fenetre_arc(s, xx, F + 5, gz, "x", 5, "minecraft:yellow_stained_glass_pane", "minecraft:diorite_stairs")
    for zz in (gz + 2, gz + 8):
        fenetre_arc(s, gx, F + 5, zz, "z", 5, "minecraft:yellow_stained_glass_pane", "minecraft:diorite_stairs")
        fenetre_arc(s, gx + 11, F + 5, zz, "z", 5, "minecraft:yellow_stained_glass_pane", "minecraft:diorite_stairs")
    statue_guerrier(s, gx + 5, F + 1, gz + 2, "minecraft:gold_block", "minecraft:gold_block", "minecraft:lightning_rod",
                    "minecraft:polished_diorite")
    tapis(s, gx + 5, gz + 4, gx + 6, gz + 10, F + 1, "blue")
    for zz in range(gz + 5, gz + 10, 2):
        s.set(gx + 2, F + 1, zz, "minecraft:oak_stairs[facing=north]"); s.set(gx + 3, F + 1, zz, "minecraft:oak_stairs[facing=north]")
        s.set(gx + 8, F + 1, zz, "minecraft:oak_stairs[facing=north]"); s.set(gx + 9, F + 1, zz, "minecraft:oak_stairs[facing=north]")
    lustre(s, gx + 5, F + 14, gz + 6, 4, "minecraft:sea_lantern")
    s.chest(gx + 1, F + 1, gz + 1, L + "cite_sigmar", "south")
    # Place du marché centrale : fontaine monumentale et étals
    s.fill(c - 6, F, c - 6, c + 6, F, c + 6, ["minecraft:chiseled_stone_bricks", "minecraft:polished_andesite"])
    s.cylinder(c, c, 3, F + 1, F + 1, "minecraft:stone_bricks", hollow=True, inside="minecraft:water")
    s.fill(c, F + 1, c, c, F + 4, c, "minecraft:chiseled_stone_bricks")
    s.set(c, F + 5, c, "minecraft:gold_block"); s.set(c, F + 6, c, "minecraft:lightning_rod")
    for (x, z, col) in ((c - 5, c - 5, "red"), (c + 5, c - 5, "blue"), (c - 5, c + 5, "yellow"), (c + 5, c + 5, "green")):
        for xx in (x - 1, x + 1):
            for zz in (z - 1, z + 1):
                s.fill(xx, F + 1, zz, xx, F + 2, zz, "minecraft:oak_fence")
        s.fill(x - 1, F + 3, z - 1, x + 1, F + 3, z + 1, f"minecraft:{col}_wool")
        s.set(x, F + 1, z, "minecraft:barrel[facing=up]")
    s.set(c - 5, F + 1, c, "minecraft:composter"); s.set(c + 5, F + 1, c, "minecraft:smithing_table")
    s.set(c, F + 1, c - 5, "minecraft:lectern[facing=south]"); s.set(c, F + 1, c + 5, "minecraft:cartography_table")
    # jardins / potagers
    for x in range(17, 29):
        for z in (37, 38, 39, 41, 42, 43):
            s.set(x, F, z, "minecraft:farmland[moisture=7]")
            s.set(x, F + 1, z, s.rng.choice(["minecraft:wheat[age=7]", "minecraft:carrots[age=7]", "minecraft:potatoes[age=7]"]))
        s.set(x, F, 40, "minecraft:water")
    # population
    s.mob(c + 2, F + 1, c + 8, "iron_golem", "garde_cite")
    s.mob(c - 8, F + 1, c - 2, "iron_golem", "garde_cite")
    s.mob(c - 3, F + 1, W - 6, "zombie", "cites_garde", 2)
    s.mob(c + 3, F + 1, 6, "zombie", "cites_garde", 2)
    s.mob(3, F + 11, c, "skeleton", "cites_arbaletrier", 1)
    s.mob(W - 4, F + 11, c, "skeleton", "cites_arbaletrier", 1)
    s.mob(c - 8, F + 1, c + 8, "villager", "habitant", 3)
    return s


# =================================================================== CHÂTEAU SOULBLIGHT (51×51)
def chateau_soulblight():
    W = 51
    s = base(W, 56, W, ["minecraft:deepslate_tiles", "minecraft:cracked_deepslate_tiles", "minecraft:polished_deepslate"],
             "minecraft:cobbled_deepslate", 33)
    c = W // 2
    pierre = ["minecraft:deepslate_bricks", "minecraft:deepslate_bricks", "minecraft:cracked_deepslate_bricks", "minecraft:polished_deepslate"]
    rempart(s, 3, 3, W - 4, W - 4, F + 1, 12, pierre, "minecraft:polished_deepslate", "minecraft:deepslate_brick_stairs",
            "minecraft:deepslate_brick_wall", "minecraft:deepslate_tile_slab[type=top]")
    meurtrieres(s, 3, 3, W - 4, W - 4, F + 6, pas=5)
    for cx, cz in ((4, 4), (W - 5, 4), (4, W - 5), (W - 5, W - 5)):
        tour(s, cx, cz, 4, F, 24, pierre, "minecraft:dark_prismarine", pointe="minecraft:iron_chain",
             fenetre="minecraft:red_stained_glass_pane", plancher="minecraft:dark_oak_planks",
             lanterne="minecraft:soul_lantern[hanging=true]")
    # Pont-levis et douves (mur sud)
    s.clear(c - 2, F + 1, W - 6, c + 2, F + 7, W - 1)
    s.fill(c - 2, F, W - 3, c + 2, F, W - 1, "minecraft:dark_oak_planks")
    for x in range(c - 6, c + 7):
        if abs(x - c) > 2:
            s.fill(x, F - 2, W - 2, x, F, W - 1, "minecraft:water")
    for dx in (-3, 3):
        s.fill(c + dx, F + 1, W - 1, c + dx, F + 9, W - 1, "minecraft:polished_deepslate")
        s.fill(c + dx, F + 6, W - 2, c + dx, F + 8, W - 2, "minecraft:iron_chain")
        s.set(c + dx, F + 10, W - 1, "minecraft:soul_lantern")
    s.fill(c - 2, F + 6, W - 4, c + 2, F + 7, W - 4, "minecraft:iron_bars")
    # Cour : cimetière, gibets, arbres morts
    for x in range(8, 20, 3):
        for z in range(c + 6, W - 8, 3):
            s.set(x, F + 1, z, s.rng.choice(["minecraft:cobblestone_wall", "minecraft:mossy_cobblestone_wall", "minecraft:deepslate_brick_wall"]))
            s.set(x, F, z + 1, "minecraft:podzol")
    for (x, z) in ((W - 12, c + 10), (W - 16, c + 16)):
        s.fill(x, F + 1, z, x, F + 6, z, "minecraft:dark_oak_log")
        s.fill(x + 1, F + 6, z, x + 2, F + 6, z, "minecraft:dark_oak_log")
        s.fill(x + 2, F + 5, z, x + 2, F + 4, z, "minecraft:iron_chain")
        s.set(x + 2, F + 3, z, "minecraft:skeleton_skull")
    # ---- Donjon gothique
    k0, k1, kz0, kz1 = c - 11, c + 11, 8, c + 4
    s.hollow(k0, F, kz0, k1, F + 24, kz1, pierre, floor="minecraft:polished_deepslate")
    for x in range(k0, k1 + 1, 4):  # contreforts
        s.fill(x, F, kz1 + 1, x, F + 14, kz1 + 1, "minecraft:polished_deepslate")
        s.set(x, F + 15, kz1 + 1, "minecraft:deepslate_brick_stairs[facing=north]")
    for x in range(k0 + 2, k1 - 1, 4):
        fenetre_arc(s, x, F + 4, kz1, "x", 6, "minecraft:red_stained_glass_pane", "minecraft:deepslate_brick_stairs")
        fenetre_arc(s, x, F + 16, kz1, "x", 4, "minecraft:red_stained_glass_pane", "minecraft:deepslate_brick_stairs")
    s.fill(k0 + 1, F + 13, kz0 + 1, k1 - 1, F + 13, kz1 - 1, "minecraft:dark_oak_planks")
    s.roof_gable(k0, kz0, k1, kz1, F + 25, "minecraft:deepslate_tile_stairs", "minecraft:deepslate_tiles", axis="x")
    for x in (k0, k1):  # flèches
        s.fill(x, F + 25, kz0, x, F + 34, kz0, "minecraft:polished_deepslate")
        s.fill(x, F + 25, kz1, x, F + 34, kz1, "minecraft:polished_deepslate")
        s.set(x, F + 35, kz0, "minecraft:iron_chain"); s.set(x, F + 35, kz1, "minecraft:iron_chain")
    # Grand portail
    s.clear(c - 2, F + 1, kz1, c + 2, F + 7, kz1 + 1)
    for x in range(c - 2, c + 3):
        s.set(x, F + 8, kz1, "minecraft:deepslate_brick_stairs[facing=north,half=top]")
    # Salle de banquet sanglante (rez-de-chaussée)
    tapis(s, c - 1, kz0 + 2, c + 1, kz1 - 1, F + 1, "red")
    table(s, c - 7, kz0 + 9, c + 7, kz0 + 10, F + 1, "minecraft:dark_oak_slab[type=top]", "minecraft:dark_oak_stairs")
    for x in range(c - 6, c + 7, 3):
        s.set(x, F + 2, kz0 + 9, "minecraft:red_candle[candles=3,lit=true]")
    for x in (c - 5, c, c + 5):
        lustre(s, x, F + 12, kz0 + 9, 3, "minecraft:soul_lantern[hanging=true]")
    cheminee(s, k0 + 1, F + 1, kz0 + 9, "east", "minecraft:polished_blackstone_bricks", 10)
    bibliotheque(s, k1 - 1, F + 1, kz0 + 3, k1 - 1, F + 5, kz0 + 7)
    for z in (kz0 + 3, kz0 + 15):
        banniere_murale(s, k0 + 1, F + 7, z, "red", "east"); banniere_murale(s, k1 - 1, F + 7, z, "black", "west")
    # Trône du Seigneur Vampire
    s.fill(c - 2, F + 1, kz0 + 1, c + 2, F + 1, kz0 + 3, "minecraft:polished_blackstone")
    s.set(c, F + 2, kz0 + 2, "minecraft:polished_blackstone_stairs[facing=south]")
    s.fill(c, F + 3, kz0 + 1, c, F + 6, kz0 + 1, "minecraft:gold_block")
    s.set(c - 1, F + 3, kz0 + 2, "minecraft:gold_block"); s.set(c + 1, F + 3, kz0 + 2, "minecraft:gold_block")
    s.set(c, F + 7, kz0 + 1, "minecraft:wither_skeleton_skull")
    s.chest(c - 4, F + 2, kz0 + 1, L + "chateau_soulblight", "south"); s.chest(c + 4, F + 2, kz0 + 1, L + "chateau_soulblight", "south")
    # Escalier vers l'étage + crypte des cercueils
    for i in range(12):
        s.set(k1 - 3, F + 1 + i, kz1 - 2 - i if kz1 - 2 - i > kz0 else kz0 + 1, "minecraft:deepslate_brick_stairs[facing=north]")
    s.clear(k1 - 3, F + 13, kz1 - 13, k1 - 3, F + 13, kz1 - 3)
    for x in range(k0 + 3, k1 - 4, 3):
        s.fill(x, F + 14, kz0 + 3, x, F + 14, kz0 + 5, "minecraft:dark_oak_planks")
        s.set(x, F + 15, kz0 + 4, "minecraft:red_carpet")
    s.chest(k0 + 2, F + 14, kz1 - 2, L + "chateau_soulblight", "east")
    lustre(s, c, F + 24, c - 4, 6, "minecraft:soul_lantern[hanging=true]")
    # ---- Garnison
    s.mob(c, F + 2, kz0 + 5, "zombie", "vampire")
    s.mob(c - 5, F + 1, kz1 - 3, "skeleton", "deathrattle", 3)
    s.mob(c + 5, F + 14, kz0 + 8, "zombie", "vampire")
    s.mob(12, F + 1, c + 12, "zombie", "mort_sylvanie", 3)
    s.mob(W - 12, F + 1, c + 12, "skeleton", "deathrattle", 2)
    s.mob(4, F + 13, 4, "skeleton", "deathrattle", 1)
    return s


# =================================================================== CITADELLE DU CHAOS (51×51)
def citadelle_chaos():
    W = 51
    s = base(W, 60, W, ["minecraft:polished_blackstone_bricks", "minecraft:cracked_polished_blackstone_bricks", "minecraft:blackstone"],
             "minecraft:blackstone", 34)
    c = W // 2
    noir = ["minecraft:polished_blackstone_bricks", "minecraft:polished_blackstone_bricks",
            "minecraft:cracked_polished_blackstone_bricks", "minecraft:blackstone"] * 4 + ["minecraft:gilded_blackstone"]
    rempart(s, 3, 3, W - 4, W - 4, F + 1, 13, noir, "minecraft:chiseled_polished_blackstone", "minecraft:polished_blackstone_brick_stairs",
            "minecraft:blackstone_wall", "minecraft:polished_blackstone_slab[type=top]")
    meurtrieres(s, 3, 3, W - 4, W - 4, F + 7, pas=5, bloc="minecraft:iron_bars")
    # pointes sur les remparts
    for x in range(4, W - 4, 4):
        for z in (2, W - 3):
            s.fill(x, F + 15, z, x, F + 17, z, "minecraft:polished_basalt")
            s.set(x, F + 18, z, "minecraft:pointed_dripstone[vertical_direction=up]")
    # Porte de l'Œil
    s.clear(c - 2, F + 1, W - 5, c + 2, F + 8, W - 2)
    s.fill(c - 4, F + 9, W - 3, c + 4, F + 13, W - 3, "minecraft:obsidian")
    s.fill(c - 1, F + 10, W - 2, c + 1, F + 12, W - 2, "minecraft:magma_block")
    s.set(c, F + 11, W - 2, "minecraft:crying_obsidian")
    s.fill(c - 2, F + 7, W - 4, c + 2, F + 8, W - 4, "minecraft:iron_bars")
    for cx, cz in ((4, 4), (W - 5, 4), (4, W - 5), (W - 5, W - 5)):
        tour(s, cx, cz, 4, F, 22, noir, "minecraft:obsidian", pointe="minecraft:crying_obsidian",
             fenetre="minecraft:red_stained_glass_pane", plancher="minecraft:crimson_planks",
             lanterne="minecraft:soul_lantern[hanging=true]")
        for (dx, dz) in ((-3, -3), (3, -3), (-3, 3), (3, 3)):
            s.fill(cx + dx, F + 23, cz + dz, cx + dx, F + 27, cz + dz, "minecraft:polished_basalt")
    # Cour : étoile à huit branches, arène, cages
    for (dx, dz) in ((1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, -1), (1, -1), (-1, 1)):
        for k in range(3, 9):
            s.set(c + dx * k, F, c + 10 + dz * k, "minecraft:red_concrete" if k < 8 else "minecraft:crying_obsidian")
            if k == 8:
                s.fill(c + dx * k, F + 1, c + 10 + dz * k, c + dx * k, F + 4, c + 10 + dz * k, "minecraft:obsidian")
                s.set(c + dx * k, F + 5, c + 10 + dz * k, "minecraft:soul_campfire")
    s.cylinder(c, c + 10, 2, F, F, "minecraft:lava", hollow=False)
    s.cylinder(c, c + 10, 2, F + 1, F + 1, "minecraft:blackstone_wall", hollow=True, inside=None)
    for (x, z) in ((9, c + 14), (13, c + 14), (W - 10, c + 14)):
        s.walls(x - 1, F + 1, z - 1, x + 1, F + 3, z + 1, "minecraft:iron_bars")
        s.set(x - 1, F + 4, z - 1, "minecraft:polished_blackstone"); s.fill(x - 1, F + 4, z - 1, x + 1, F + 4, z + 1, "minecraft:polished_blackstone_slab")
        s.set(x, F + 1, z, "minecraft:bone_block")
    # ---- Tour des Huit (donjon)
    k0, k1, kz0, kz1 = c - 8, c + 8, 7, 23
    s.hollow(k0, F, kz0, k1, F + 32, kz1, noir, floor="minecraft:polished_blackstone")
    for (x, z) in ((k0, kz0), (k1, kz0), (k0, kz1), (k1, kz1)):
        s.fill(x, F, z, x, F + 40, z, "minecraft:polished_basalt")
        s.set(x, F + 41, z, "minecraft:crying_obsidian")
    for y in (F + 8, F + 16, F + 24):
        s.fill(k0 + 1, y, kz0 + 1, k1 - 1, y, kz1 - 1, "minecraft:crimson_planks")
        s.clear(k0 + 1, y, kz0 + 1, k0 + 3, y, kz0 + 3)
    for y in range(F + 1, F + 32):
        s.set(k0 + 1, y, kz0 + 1, "minecraft:ladder[facing=south]")
    for x in range(k0 + 3, k1 - 2, 4):
        for y in (F + 3, F + 11, F + 19, F + 27):
            fenetre_arc(s, x, y, kz1, "x", 3, "minecraft:red_stained_glass_pane", "minecraft:polished_blackstone_brick_stairs")
            fenetre_arc(s, x, y, kz0, "x", 3, "minecraft:red_stained_glass_pane", "minecraft:polished_blackstone_brick_stairs")
    s.cone(c, (kz0 + kz1) // 2, 9, F + 33, ["minecraft:obsidian", "minecraft:blackstone", "minecraft:crying_obsidian"])
    s.clear(c - 2, F + 1, kz1, c + 2, F + 6, kz1)
    for x in range(c - 2, c + 3):
        s.set(x, F + 7, kz1, "minecraft:polished_blackstone_brick_stairs[facing=north,half=top]")
    # RDC : salle des guerriers
    table(s, c - 5, kz0 + 7, c + 5, kz0 + 8, F + 1, "minecraft:crimson_slab[type=top]", "minecraft:crimson_stairs")
    cheminee(s, k1 - 1, F + 1, kz0 + 8, "west", "minecraft:nether_bricks", 7)
    tapis(s, c - 1, kz0 + 10, c + 1, kz1 - 1, F + 1, "red")
    lustre(s, c, F + 8, kz0 + 8, 2, "minecraft:soul_lantern[hanging=true]")
    for z in (kz0 + 3, kz1 - 3):
        banniere_murale(s, k0 + 1, F + 4, z, "black", "east"); banniere_murale(s, k1 - 1, F + 4, z, "red", "west")
    # 1er : armurerie
    for x in range(k0 + 2, k1 - 1, 2):
        s.set(x, F + 9, kz1 - 1, "minecraft:grindstone[face=floor]" if x % 4 == 0 else "minecraft:anvil")
    s.chest(c, F + 9, kz0 + 2, L + "citadelle_chaos", "south")
    # 2e : sanctum des sorciers de Vharys
    bibliotheque(s, k0 + 1, F + 17, kz0 + 4, k0 + 1, F + 20, kz1 - 2)
    s.set(c, F + 17, c - 10, "minecraft:enchanting_table")
    s.set(c + 2, F + 17, c - 10, "minecraft:brewing_stand")
    s.chest(k1 - 2, F + 17, kz1 - 2, L + "citadelle_chaos", "west")
    # 3e : salle du trône du Seigneur
    s.fill(c - 2, F + 25, kz0 + 2, c + 2, F + 25, kz0 + 4, "minecraft:gilded_blackstone")
    s.set(c, F + 26, kz0 + 3, "minecraft:polished_blackstone_stairs[facing=south]")
    s.fill(c, F + 27, kz0 + 2, c, F + 30, kz0 + 2, "minecraft:obsidian")
    s.set(c - 1, F + 29, kz0 + 2, "minecraft:obsidian"); s.set(c + 1, F + 29, kz0 + 2, "minecraft:obsidian")
    s.chest(c + 3, F + 25, kz0 + 2, L + "citadelle_chaos", "south")
    lustre(s, c, F + 32, c - 10, 3, "minecraft:soul_lantern[hanging=true]")
    # ---- Garnison
    s.mob(c, F + 25, kz0 + 6, "zombie", "chaos_seigneur")
    s.mob(c + 3, F + 1, kz0 + 12, "zombie", "chaos_guerrier", 3)
    s.mob(c - 6, F + 1, c + 10, "zombie", "chaos_guerrier", 3)
    s.mob(c + 6, F + 1, c + 16, "zombie", "bloodreaver", 2)
    s.mob(c, F + 17, kz0 + 6, "skeleton", "tzaangor", 2)
    s.mob(4, F + 14, 4, "skeleton", "tzaangor", 1)
    s.mob(W - 5, F + 14, W - 5, "skeleton", "tzaangor", 1)
    return s


GRANDS = {"forteresse_stormcast": forteresse_stormcast, "cite_sigmar": cite_sigmar,
          "chateau_soulblight": chateau_soulblight, "citadelle_chaos": citadelle_chaos}
