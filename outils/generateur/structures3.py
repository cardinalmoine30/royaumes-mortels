# -*- coding: utf-8 -*-
"""Version 3 des structures : ambiance dark fantasy héroïque marquée, portails de royaume et repaires de boss."""
import math
from nbtgen import Struct
from details import (rempart, meurtrieres, tour, fenetre_arc, lustre, table, tapis, banniere_murale, cheminee,
                     bibliotheque, statue_guerrier, comete, etoile8, crane_geant)

F = 4
L = "royaumes:coffres/"


def base(sx, sy, sz, sol, fond, seed, haut=8):
    s = Struct(sx, sy, sz, seed)
    s.foundation(0, 0, sx - 1, sz - 1, F - 1, F, fond)
    s.fill(0, F, 0, sx - 1, F, sz - 1, sol)
    s.clear(0, F + 1, 0, sx - 1, F + haut, sz - 1)
    return s


def cercle(cx, cz, r, pas=10):
    for a in range(0, 360, pas):
        yield cx + round(r * math.cos(math.radians(a))), cz + round(r * math.sin(math.radians(a)))


# =================================================================== DESTRUCTION
def camp_orruk():
    """Forteresse de ferraille Mâchefers avec idole de Brog, fosse de forge et trône du Grand Chef."""
    W = 45
    s = base(W, 30, W, ["minecraft:coarse_dirt", "minecraft:packed_mud", "minecraft:dirt_path", "minecraft:gravel"],
             "minecraft:dirt", 41)
    c = W // 2
    ferraille = ["minecraft:iron_block", "minecraft:waxed_exposed_cut_copper", "minecraft:waxed_weathered_copper",
                 "minecraft:spruce_planks", "minecraft:iron_block", "minecraft:waxed_oxidized_cut_copper", "minecraft:stripped_spruce_log"]
    # Palissade ferraille dentelée
    for (x, z) in [(x, z) for x in range(1, W - 1) for z in (1, W - 2)] + [(x, z) for z in range(1, W - 1) for x in (1, W - 2)]:
        h = 6 + (x * 7 + z * 3) % 3
        s.fill(x, F + 1, z, x, F + h, z, ferraille)
        if (x + z) % 3 == 0:
            s.set(x, F + h + 1, z, "minecraft:pointed_dripstone[vertical_direction=up]")
        if (x + z) % 11 == 0:
            s.set(x, F + h + 1, z, "minecraft:skeleton_skull")
    s.clear(c - 2, F + 1, W - 2, c + 2, F + 7, W - 2)
    # Porte : mâchoire de Brog (dents d'os)
    s.fill(c - 4, F + 8, W - 2, c + 4, F + 10, W - 2, "minecraft:iron_block")
    for x in range(c - 3, c + 4, 2):
        s.set(x, F + 7, W - 2, "minecraft:bone_block[axis=y]"); s.set(x, F + 6, W - 2, "minecraft:pointed_dripstone[vertical_direction=down]")
    s.set(c - 2, F + 11, W - 2, "minecraft:redstone_lamp[lit=true]"); s.set(c + 2, F + 11, W - 2, "minecraft:redstone_lamp[lit=true]")
    # Tours de guet en échafaudage
    for (x, z) in ((4, 4), (W - 5, 4), (4, W - 5), (W - 5, W - 5)):
        for (dx, dz) in ((-1, -1), (1, -1), (-1, 1), (1, 1)):
            s.fill(x + dx, F + 1, z + dz, x + dx, F + 12, z + dz, "minecraft:spruce_log")
        s.fill(x - 2, F + 12, z - 2, x + 2, F + 12, z + 2, "minecraft:spruce_planks")
        s.walls(x - 2, F + 13, z - 2, x + 2, F + 13, z + 2, "minecraft:iron_bars")
        s.fill(x - 2, F + 16, z - 2, x + 2, F + 16, z + 2, "minecraft:waxed_exposed_cut_copper")
        for (dx, dz) in ((-2, -2), (2, -2), (-2, 2), (2, 2)):
            s.fill(x + dx, F + 13, z + dz, x + dx, F + 15, z + dz, "minecraft:spruce_fence")
        for y in range(F + 1, F + 12):
            s.set(x, y, z + 1, "minecraft:ladder[facing=north]")
        s.set(x, F + 17, z, "minecraft:yellow_banner[rotation=0]")
    # Idole géante de Brog (tête verte aux défenses d'os)
    ix, iz = c, 9
    s.fill(ix - 4, F + 1, iz - 2, ix + 4, F + 3, iz + 2, ["minecraft:cobblestone", "minecraft:mossy_cobblestone"])
    s.fill(ix - 3, F + 4, iz - 2, ix + 3, F + 11, iz + 2, ["minecraft:green_terracotta", "minecraft:green_concrete", "minecraft:moss_block"])
    s.fill(ix - 4, F + 9, iz - 2, ix + 4, F + 10, iz + 2, "minecraft:green_terracotta")  # arcades sourcilières
    s.set(ix - 2, F + 8, iz + 2, "minecraft:redstone_block"); s.set(ix + 2, F + 8, iz + 2, "minecraft:redstone_block")
    s.fill(ix - 2, F + 5, iz + 2, ix + 2, F + 5, iz + 2, "minecraft:black_concrete")  # gueule
    for x in (ix - 2, ix, ix + 2):
        s.set(x, F + 5, iz + 2, "minecraft:bone_block[axis=y]")
    for x in (ix - 3, ix + 3):
        s.fill(x, F + 4, iz + 3, x, F + 7, iz + 3, "minecraft:bone_block[axis=y]")  # défenses
    s.fill(ix - 4, F + 12, iz - 2, ix + 4, F + 12, iz + 2, "minecraft:iron_block")  # casque de ferraille
    s.fill(ix - 1, F + 13, iz, ix + 1, F + 15, iz, "minecraft:pointed_dripstone[vertical_direction=up]")
    s.set(ix - 5, F + 1, iz + 3, "minecraft:campfire"); s.set(ix + 5, F + 1, iz + 3, "minecraft:campfire")
    # Trône du Grand Chef
    s.fill(c - 2, F + 1, c - 3, c + 2, F + 1, c - 1, "minecraft:iron_block")
    s.fill(c - 1, F + 2, c - 3, c + 1, F + 5, c - 3, "minecraft:iron_block")
    s.set(c, F + 2, c - 2, "minecraft:spruce_stairs[facing=south]")
    s.set(c - 2, F + 6, c - 3, "minecraft:skeleton_skull"); s.set(c + 2, F + 6, c - 3, "minecraft:skeleton_skull")
    s.chest(c + 3, F + 1, c - 3, L + "camp_orruk", "south")
    # Fosse de forge
    s.disk(c - 11, c + 6, 3, F, "minecraft:magma_block")
    s.disk(c - 11, c + 6, 1, F, "minecraft:lava")
    s.set(c - 8, F + 1, c + 6, "minecraft:anvil"); s.set(c - 11, F + 1, c + 9, "minecraft:blast_furnace[facing=north]")
    s.barrel(c - 13, F + 1, c + 9, L + "camp_orruk")
    # Huttes de ferraille au toit de cuivre
    for (x, z) in ((6, 16), (6, 27), (W - 13, 16), (W - 13, 27)):
        s.hollow(x, F, z, x + 7, F + 5, z + 6, ferraille, floor="minecraft:coarse_dirt")
        s.fill(x - 1, F + 6, z - 1, x + 8, F + 6, z + 7, "minecraft:waxed_weathered_cut_copper")
        s.fill(x, F + 7, z, x + 7, F + 7, z + 6, "minecraft:waxed_oxidized_cut_copper")
        s.clear(x + 3, F + 1, z + 6, x + 4, F + 3, z + 6)
        s.set(x + 1, F + 1, z + 1, "minecraft:red_bed[facing=north,part=head]"); s.set(x + 1, F + 1, z + 2, "minecraft:red_bed[facing=north,part=foot]")
        s.barrel(x + 6, F + 1, z + 1, L + "camp_orruk")
        s.set(x + 4, F + 4, z + 3, "minecraft:lantern[hanging=true]")
    # Enclos du Broyeur-Gueule (os géants)
    s.walls(c + 3, F + 1, c + 4, c + 13, F + 2, c + 14, "minecraft:spruce_fence")
    for z in range(c + 6, c + 13, 2):
        s.fill(c + 8, F + 1, z, c + 8, F + 3, z, "minecraft:bone_block[axis=y]")
    s.set(c + 8, F + 1, c + 9, "minecraft:hay_block")
    # Bannières Mâchefers (jaune / rouge)
    for x in range(4, W - 4, 6):
        s.banner_pole(x, F + 1, c, 4, "yellow" if x % 12 else "red", "minecraft:iron_bars")
    s.mob(c, F + 2, c - 1, "zombie", "megaboss")
    s.mob(c - 3, F + 1, c + 3, "zombie", "brute", 4)
    s.mob(c + 6, F + 1, c - 6, "zombie", "brute", 2)
    s.mob(4, F + 13, 4, "skeleton", "ogor_chasseur", 1)
    return s


def fort_kruleboyz():
    """Fort sur pilotis des marais : murs de racines épineuses, chaudrons de venin, cages et totems."""
    W = 41
    s = Struct(W, 30, W, 42)
    c = W // 2
    # Pilotis
    for x in range(2, W - 2, 4):
        for z in range(2, W - 2, 4):
            s.fill(x, 0, z, x, 8, z, "minecraft:mangrove_log")
    s.fill(2, 9, 2, W - 3, 9, W - 3, ["minecraft:mangrove_planks", "minecraft:mud_bricks", "minecraft:mangrove_planks", "minecraft:packed_mud"])
    # Murs de racines dentelés
    for (x, z) in [(x, z) for x in range(2, W - 2) for z in (2, W - 3)] + [(x, z) for z in range(2, W - 2) for x in (2, W - 3)]:
        h = 4 + (x * 3 + z * 5) % 3
        s.fill(x, 10, z, x, 9 + h, z, ["minecraft:mangrove_roots", "minecraft:mud_bricks", "minecraft:mangrove_log"])
        if (x + z) % 2 == 0:
            s.set(x, 10 + h, z, "minecraft:pointed_dripstone[vertical_direction=up]")
    s.clear(c - 1, 10, W - 3, c + 1, 12, W - 3)
    # Passerelle d'entrée et échelle
    s.fill(c - 1, 9, W - 2, c + 1, 9, W - 1, "minecraft:mangrove_planks")
    s.fill(c, 0, W - 1, c, 8, W - 1, "minecraft:mangrove_log")
    for y in range(1, 9):
        s.set(c, y, W - 2, "minecraft:ladder[facing=north]")
    s.set(c, 9, W - 2, "minecraft:mangrove_trapdoor[facing=north,open=true]")
    # Grande hutte du Boss : dôme de boue et toit de paille
    s.cylinder(c, c - 4, 7, 10, 16, ["minecraft:mud_bricks", "minecraft:packed_mud", "minecraft:mangrove_roots"])
    s.disk(c, c - 4, 6, 9, "minecraft:mangrove_planks")
    y = 17
    for r in range(8, -1, -1):
        s.cylinder(c, c - 4, r, y, y, ["minecraft:hay_block", "minecraft:mangrove_roots", "minecraft:moss_block"], hollow=True, inside=None)
        y += 1
    s.fill(c, y, c - 4, c, y + 3, c - 4, "minecraft:mangrove_log"); s.set(c, y + 4, c - 4, "minecraft:skeleton_skull")
    s.clear(c - 1, 10, c + 3, c + 1, 12, c + 3)
    s.chest(c - 3, 10, c - 9, L + "fort_kruleboyz", "south"); s.chest(c + 3, 10, c - 9, L + "fort_kruleboyz", "south")
    s.set(c, 10, c - 9, "minecraft:mangrove_stairs[facing=south]")
    lustre(s, c, 16, c - 4, 2)
    # Chaudrons de venin
    for (x, z) in ((7, W - 9), (W - 8, W - 9), (7, 10)):
        s.set(x, 10, z, "minecraft:water_cauldron[level=3]")
        s.set(x, 9, z, "minecraft:magma_block")
        s.set(x + 1, 10, z, "minecraft:lime_candle[candles=3,lit=true]")
        s.set(x - 1, 10, z, "minecraft:brewing_stand")
    # Cages suspendues et totems
    for (x, z) in ((W - 9, 9), (10, c + 8)):
        s.walls(x - 1, 10, z - 1, x + 1, 12, z + 1, "minecraft:iron_bars")
        s.fill(x - 1, 13, z - 1, x + 1, 13, z + 1, "minecraft:mangrove_slab")
        s.set(x, 10, z, "minecraft:skeleton_skull")
    for (x, z) in ((5, 5), (W - 6, 5), (5, W - 6), (W - 6, W - 6), (c + 9, c + 4)):
        s.fill(x, 10, z, x, 16, z, "minecraft:mangrove_log")
        s.set(x - 1, 15, z, "minecraft:skeleton_skull"); s.set(x + 1, 15, z, "minecraft:skeleton_skull")
        s.set(x, 17, z, "minecraft:zombie_head")
        s.set(x, 14, z + 1, "minecraft:green_wall_banner[facing=south]")
    s.mob(c + 6, 10, c + 6, "zombie", "gutrippa", 5)
    s.mob(6, 10, W - 6, "skeleton", "kb_archer", 2)
    s.mob(c, 10, c - 6, "zombie", "gutrippa", 2)
    return s


def antre_gitz():
    """Repaire de la Mauvaise Lune : idole lunaire grimaçante, forêt de champignons géants, nid d'Araignée Titanesque."""
    W = 41
    s = base(W, 34, W, ["minecraft:mycelium", "minecraft:podzol", "minecraft:moss_block", "minecraft:coarse_dirt"],
             "minecraft:dirt", 43, haut=14)
    c = W // 2
    rng = s.rng
    for (x, z, h, cap) in ((6, 6, 11, "red"), (W - 7, 8, 15, "brown"), (8, W - 7, 9, "red"),
                           (W - 8, W - 9, 13, "red"), (c - 9, c + 2, 8, "brown"), (c + 11, c - 3, 10, "red")):
        s.fill(x, F + 1, z, x, F + h, z, "minecraft:mushroom_stem")
        r = 4 if h > 10 else 3
        s.cylinder(x, z, r, F + h + 1, F + h + 1, f"minecraft:{cap}_mushroom_block", hollow=False)
        s.cylinder(x, z, r - 1, F + h + 2, F + h + 2, f"minecraft:{cap}_mushroom_block", hollow=False)
        for (dx, dz) in ((r, 0), (-r, 0), (0, r), (0, -r)):
            s.set(x + dx, F + h, z + dz, f"minecraft:{cap}_mushroom_block")
        s.set(x, F + h, z, "minecraft:shroomlight")
    # La Mauvaise Lune : disque pâle à visage grimaçant
    mx, my, mz = c, F + 13, 3
    for x in range(mx - 6, mx + 7):
        for y in range(my - 6, my + 7):
            if (x - mx) ** 2 + (y - my) ** 2 <= 36:
                s.set(x, y, mz, rng.choice(["minecraft:end_stone", "minecraft:end_stone", "minecraft:yellow_terracotta"]))
    for (dx, dy) in ((-3, 2), (3, 2), (-2, 2), (2, 2)):
        s.set(mx + dx, my + dy, mz + 1, "minecraft:black_concrete")
    for dx in range(-4, 5):
        s.set(mx + dx, my - 2 - (1 if abs(dx) < 3 else 0), mz + 1, "minecraft:black_concrete")
    for dx in (-3, -1, 1, 3):
        s.set(mx + dx, my - 3, mz + 1, "minecraft:white_concrete")
    s.fill(mx, F + 1, mz, mx, my - 7, mz, "minecraft:mushroom_stem")
    # Grotte creusée dans une butte de mousse
    s.cylinder(c, c + 8, 6, F + 1, F + 6, ["minecraft:moss_block", "minecraft:mossy_cobblestone", "minecraft:dirt"], hollow=False)
    for y in range(F + 1, F + 6):
        s.cylinder(c, c + 8, 4, y, y, "minecraft:air", hollow=False)
    s.clear(c - 1, F + 1, c + 14, c + 1, F + 3, c + 14)
    s.set(c, F + 1, c + 8, "minecraft:campfire")
    s.chest(c - 3, F + 1, c + 8, L + "antre_gitz", "east"); s.barrel(c + 3, F + 1, c + 8, L + "antre_gitz")
    s.set(c, F + 5, c + 8, "minecraft:shroomlight")
    # Nid d'Araignée Titanesque : toiles et œufs
    for (x, z) in cercle(c + 10, c + 11, 4, 30):
        s.set(x, F + 1, z, "minecraft:cobweb"); s.set(x, F + 2, z, "minecraft:cobweb")
    s.set(c + 10, F + 1, c + 11, "minecraft:turtle_egg[eggs=4]")
    # Enclos à squigs
    s.walls(4, F + 1, c - 6, 12, F + 2, c + 2, "minecraft:spruce_fence")
    for x in range(5, 12, 2):
        s.set(x, F + 1, c - 2, rng.choice(["minecraft:red_mushroom", "minecraft:brown_mushroom"]))
    s.mob(c + 4, F + 1, c - 4, "zombie", "grot", 6)
    s.mob(c + 10, F + 1, c + 11, "spider", "arachnarok")
    s.mob(8, F + 1, c - 2, "zombie", "grot", 2)
    return s


def campement_ogor():
    """Campement des Tribus : la Grande Gueule (fosse dentée), marmite géante, séchoirs à viande, os de Corne-de-Pierre."""
    W = 41
    s = base(W, 22, W, ["minecraft:coarse_dirt", "minecraft:dirt", "minecraft:rooted_dirt", "minecraft:snow_block"],
             "minecraft:dirt", 44)
    c = W // 2
    # La Grande Gueule : fosse ronde aux dents d'os
    for y in range(F - 3, F + 1):
        s.cylinder(c, c, 5, y, y, "minecraft:air", hollow=False)
    s.cylinder(c, c, 6, F - 3, F, ["minecraft:packed_mud", "minecraft:mud_bricks"], hollow=True, inside=None)
    s.disk(c, c, 5, F - 4, "minecraft:red_terracotta")
    for (x, z) in cercle(c, c, 6, 24):
        s.fill(x, F + 1, z, x, F + 2, z, "minecraft:bone_block[axis=y]")
        s.set(x, F + 3, z, "minecraft:pointed_dripstone[vertical_direction=up]")
    # Marmite géante (Gutpot)
    gx, gz = c + 11, c - 9
    s.cylinder(gx, gz, 3, F + 1, F + 3, "minecraft:iron_block", hollow=True, inside="minecraft:water")
    s.disk(gx, gz, 2, F, "minecraft:magma_block")
    for (dx, dz) in ((-3, 0), (3, 0)):
        s.fill(gx + dx, F + 4, gz + dz, gx + dx, F + 6, gz + dz, "minecraft:spruce_fence")
    s.fill(gx - 3, F + 7, gz, gx + 3, F + 7, gz, "minecraft:spruce_fence")
    s.fill(gx, F + 5, gz, gx, F + 6, gz, "minecraft:iron_chain")
    s.set(gx, F + 4, gz, "minecraft:bone_block")
    # Séchoirs à viande
    for z in (6, 10):
        s.fill(5, F + 1, z, 5, F + 4, z, "minecraft:spruce_fence"); s.fill(13, F + 1, z, 13, F + 4, z, "minecraft:spruce_fence")
        s.fill(5, F + 5, z, 13, F + 5, z, "minecraft:spruce_fence")
        for x in range(6, 13, 2):
            s.set(x, F + 4, z, "minecraft:iron_chain"); s.set(x, F + 3, z, s.rng.choice(["minecraft:red_terracotta", "minecraft:brown_mushroom_block"]))
    # Tentes de peaux (dômes)
    for (x, z, col) in ((7, W - 9, "brown"), (W - 10, W - 9, "white"), (W - 9, c + 3, "brown"), (8, c + 4, "brown")):
        for y in range(5):
            s.cylinder(x, z, 4 - y, F + 1 + y, F + 1 + y, f"minecraft:{col}_wool", hollow=True, inside="minecraft:air")
        s.clear(x, F + 1, z + 4, x, F + 2, z + 4)
        s.set(x, F + 1, z, "minecraft:hay_block"); s.barrel(x + 2, F + 1, z, L + "campement_ogor")
        s.fill(x, F + 6, z, x, F + 8, z, "minecraft:spruce_fence"); s.set(x, F + 9, z, "minecraft:skeleton_skull")
    # Carcasse de Corne-de-Pierre
    for x in range(c - 8, c + 4):
        s.set(x, F + 5, 4, "minecraft:bone_block[axis=x]")
    for x in range(c - 7, c + 3, 2):
        for k in range(4):
            s.set(x, F + 4 - k, 3, "minecraft:bone_block[axis=y]"); s.set(x, F + 4 - k, 5, "minecraft:bone_block[axis=y]")
    s.fill(c + 4, F + 3, 3, c + 6, F + 6, 5, "minecraft:bone_block")
    s.fill(c + 7, F + 5, 2, c + 8, F + 7, 2, "minecraft:bone_block[axis=y]"); s.fill(c + 7, F + 5, 6, c + 8, F + 7, 6, "minecraft:bone_block[axis=y]")
    # Totem du Tyran
    s.fill(c - 12, F + 1, c - 12, c - 12, F + 10, c - 12, "minecraft:stripped_spruce_log")
    for y in (F + 6, F + 8, F + 10):
        s.set(c - 13, y, c - 12, "minecraft:skeleton_skull"); s.set(c - 11, y, c - 12, "minecraft:skeleton_skull")
    s.chest(c + 2, F + 1, c + 8, L + "campement_ogor", "north")
    s.mob(c + 4, F + 1, c - 4, "zombie", "gutbuster", 4)
    s.mob(c - 6, F + 1, c + 6, "skeleton", "ogor_chasseur", 2)
    return s


# =================================================================== ORDRE
def temple_seraphon():
    """Temple-cité Astrosauriens : pyramide à degrés, serpents de Sotek, observatoire céleste du Sage-Crapaud."""
    W = 47
    s = base(W, 40, W, ["minecraft:mossy_stone_bricks", "minecraft:stone_bricks", "minecraft:mossy_cobblestone"],
             "minecraft:mossy_cobblestone", 45)
    c = W // 2
    pierre = ["minecraft:mossy_stone_bricks", "minecraft:stone_bricks", "minecraft:cracked_stone_bricks",
              "minecraft:mossy_stone_bricks", "minecraft:chiseled_stone_bricks"]
    x0, x1 = 6, W - 7
    y = F + 1
    niveau = 0
    while x1 - x0 >= 6:
        s.fill(x0, y, x0, x1, y + 2, x1, pierre)
        # frise d'or et de prismarine (glyphes célestes)
        for k in range(x0, x1 + 1, 3):
            for (xx, zz) in ((k, x0), (k, x1), (x0, k), (x1, k)):
                s.set(xx, y + 1, zz, "minecraft:gold_block" if (k // 3) % 2 else "minecraft:prismarine_bricks")
        x0 += 2; x1 -= 2; y += 3; niveau += 1
    top = y
    # Escalier monumental flanqué de serpents de Sotek
    for i in range(top - F - 1):
        s.fill(c - 2, F + 1 + i, W - 7 - i * 2 // 3, c + 2, F + 1 + i, W - 7 - i * 2 // 3, "minecraft:stone_brick_stairs[facing=north]")
    for dx in (-3, 3):
        for i in range(0, top - F - 1, 1):
            zz = W - 7 - i * 2 // 3
            s.set(c + dx, F + 1 + i, zz, "minecraft:prismarine_bricks" if i % 2 else "minecraft:dark_prismarine")
        s.fill(c + dx, F + 1, W - 6, c + dx, F + 3, W - 5, "minecraft:dark_prismarine")  # têtes de serpent
        s.set(c + dx, F + 3, W - 4, "minecraft:gold_block"); s.set(c + dx, F + 2, W - 4, "minecraft:redstone_block")
    # Sanctuaire sommital et observatoire céleste
    s.hollow(c - 4, top, c - 4, c + 4, top + 6, c + 4, "minecraft:chiseled_stone_bricks", floor="minecraft:gold_block")
    for (dx, dz) in ((-4, -4), (4, -4), (-4, 4), (4, 4)):
        s.fill(c + dx, top, c + dz, c + dx, top + 8, c + dz, "minecraft:prismarine_bricks")
        s.set(c + dx, top + 9, c + dz, "minecraft:sea_lantern")
    s.fill(c - 4, top + 6, c - 4, c + 4, top + 6, c + 4, "minecraft:gold_block")
    s.clear(c - 1, top + 1, c + 4, c + 1, top + 4, c + 4)
    s.disk(c, c, 2, top + 1, "minecraft:gold_block")  # palanquin du Sage-Crapaud
    s.set(c, top + 2, c, "minecraft:enchanting_table")
    s.set(c, top + 7, c, "minecraft:beacon")
    for k in range(3):
        s.set(c, top + 8 + k, c, "minecraft:end_rod")
    s.chest(c - 2, top + 1, c - 3, L + "temple_seraphon", "south"); s.chest(c + 2, top + 1, c - 3, L + "temple_seraphon", "south")
    # Pierres-étoiles (obélisques) et bassins
    for (x, z) in ((3, 3), (W - 4, 3), (3, W - 4), (W - 4, W - 4)):
        s.fill(x, F + 1, z, x, F + 9, z, ["minecraft:prismarine_bricks", "minecraft:dark_prismarine"])
        s.set(x, F + 10, z, "minecraft:gold_block"); s.set(x, F + 11, z, "minecraft:end_rod")
    for (x, z) in ((3, c), (W - 4, c)):
        s.fill(x - 1, F, z - 3, x + 1, F, z + 3, "minecraft:water")
        s.set(x, F, z, "minecraft:sea_lantern")
    s.mob(c, top + 1, c + 2, "zombie", "saurus", 2)
    s.mob(c + 8, F + 1, W - 3, "zombie", "saurus", 3)
    s.mob(c - 8, F + 1, W - 3, "skeleton", "skink", 4)
    return s


def bosquet_sylvaneth():
    """Bosquet de Bois-Sauvage : Arbre-Mère au cœur lumineux, racines de royaume luminescentes, cercle de pierres."""
    W = 41
    s = base(W, 44, W, ["minecraft:moss_block", "minecraft:grass_block", "minecraft:rooted_dirt"], "minecraft:dirt", 46, haut=14)
    c = W // 2
    # Arbre-Mère
    for y in range(F, F + 24):
        r = 5 if y < F + 4 else 4 if y < F + 12 else 3
        s.cylinder(c, c, r, y, y, ["minecraft:oak_wood", "minecraft:oak_wood", "minecraft:moss_block", "minecraft:stripped_oak_wood"],
                   hollow=True, inside="minecraft:air")
    s.clear(c - 1, F + 1, c + 4, c + 1, F + 4, c + 5)
    s.fill(c, F + 1, c, c, F + 2, c, "minecraft:mossy_stone_bricks")
    s.set(c, F + 3, c, "minecraft:shroomlight")  # cœur de l'Arbre-Mère
    for y in range(F + 4, F + 22, 3):
        s.set(c, y, c, "minecraft:shroomlight")
    s.chest(c - 2, F + 1, c, L + "bosquet_sylvaneth", "east"); s.chest(c + 2, F + 1, c, L + "bosquet_sylvaneth", "west")
    # Branches et canopée
    for a in range(0, 360, 45):
        for r in range(3, 11):
            x = c + round(r * math.cos(math.radians(a))); z = c + round(r * math.sin(math.radians(a)))
            s.set(x, F + 18 + r // 3, z, "minecraft:oak_wood")
    for y in range(F + 21, F + 33):
        r = 13 - abs(y - (F + 26)) * 2 // 2
        s.cylinder(c, c, max(r, 4), y, y, ["minecraft:azalea_leaves[persistent=true]", "minecraft:flowering_azalea_leaves[persistent=true]",
                                          "minecraft:oak_leaves[persistent=true]", "minecraft:flowering_azalea_leaves[persistent=true]"], hollow=False)
    for (x, z) in cercle(c, c, 9, 40):
        for y in range(F + 14, F + 20):
            s.set(x, y, z, "minecraft:cave_vines_plant[berries=true]")
        s.set(x, F + 13, z, "minecraft:cave_vines[berries=true]")
    # Racines de royaume luminescentes rayonnantes
    for a in range(0, 360, 30):
        for r in range(6, 19):
            x = c + round(r * math.cos(math.radians(a + r * 2))); z = c + round(r * math.sin(math.radians(a + r * 2)))
            s.set(x, F, z, "minecraft:oak_wood")
            if r % 4 == 0:
                s.set(x, F + 1, z, "minecraft:glow_lichen[down=true]")
    # Cercle de menhirs moussus
    for i, (x, z) in enumerate(cercle(c, c, 17, 30)):
        h = 3 + i % 3
        s.fill(x, F + 1, z, x, F + h, z, ["minecraft:mossy_cobblestone", "minecraft:mossy_stone_bricks"])
        s.set(x, F + h + 1, z, "minecraft:moss_carpet")
    # Ronces et fleurs
    for x in range(2, W - 2, 2):
        for z in range(2, W - 2, 3):
            if 8 < math.hypot(x - c, z - c) < 15 and s.rng.random() < 0.5:
                s.set(x, F + 1, z, s.rng.choice(["minecraft:sweet_berry_bush[age=3]", "minecraft:allium", "minecraft:blue_orchid",
                                                 "minecraft:lily_of_the_valley", "minecraft:fern", "minecraft:azalea"]))
    s.mob(c + 7, F + 1, c + 7, "zombie", "dryade", 3)
    s.mob(c - 7, F + 1, c - 7, "zombie", "dryade", 2)
    return s


def magmahold():
    """Magmahold Fyreslayer : butte de basalte, porte runique d'or, rivière de lave, statue de Brasdur."""
    W = 47
    s = base(W, 34, W, ["minecraft:polished_blackstone_bricks", "minecraft:blackstone", "minecraft:basalt"], "minecraft:blackstone", 47, haut=14)
    c = W // 2
    noir = ["minecraft:blackstone", "minecraft:basalt", "minecraft:polished_blackstone_bricks", "minecraft:blackstone",
            "minecraft:polished_basalt", "minecraft:blackstone", "minecraft:basalt", "minecraft:polished_blackstone_bricks",
            "minecraft:gilded_blackstone", "minecraft:magma_block"]
    # Dôme-montagne creux
    for y in range(F + 1, F + 18):
        r = int(math.sqrt(max(0, 20 ** 2 - ((y - F) * 1.15) ** 2)))
        if r < 2:
            break
        s.cylinder(c, c, r, y, y, noir, hollow=True, inside="minecraft:air")
    s.disk(c, c, 3, F + 18, "minecraft:magma_block")
    s.set(c, F + 19, c, "minecraft:campfire")
    # Grande porte runique (sud)
    s.clear(c - 3, F + 1, W - 8, c + 3, F + 8, c + 18)
    for y in range(F + 1, F + 11):
        s.set(c - 4, y, W - 6, "minecraft:gold_block"); s.set(c + 4, y, W - 6, "minecraft:gold_block")
    s.fill(c - 4, F + 9, W - 6, c + 4, F + 11, W - 6, "minecraft:gold_block")
    for x in range(c - 3, c + 4, 2):
        s.set(x, F + 10, W - 5, "minecraft:magma_block")
    s.fill(c - 1, F + 12, W - 6, c + 1, F + 14, W - 6, "minecraft:polished_blackstone_bricks")
    s.set(c, F + 13, W - 5, "minecraft:gold_block")  # rune de Brasdur
    for dx in (-6, 6):
        s.fill(c + dx, F + 1, W - 5, c + dx, F + 6, W - 5, "minecraft:polished_blackstone_brick_wall")
        s.set(c + dx, F + 7, W - 5, "minecraft:campfire")
    # Rivière de lave intérieure avec pont
    s.fill(4, F, c - 1, W - 5, F, c + 1, "minecraft:lava")
    s.fill(c - 2, F, c - 1, c + 2, F, c + 1, "minecraft:gilded_blackstone")
    for x in range(4, W - 4, 3):
        s.set(x, F - 1, c, "minecraft:magma_block")
    # Statue colossale de Brasdur
    statue_guerrier(s, c, F + 1, 8, "minecraft:gold_block", "minecraft:magma_block", "minecraft:gold_block", "minecraft:polished_blackstone_bricks")
    s.fill(c - 1, F + 8, 7, c + 1, F + 8, 7, "minecraft:orange_terracotta")  # crête orange
    s.set(c, F + 9, 8, "minecraft:orange_terracotta"); s.set(c, F + 10, 8, "minecraft:orange_terracotta")
    # Forges runiques
    for x in (c - 12, c + 8):
        s.fill(x, F + 1, 10, x + 4, F + 1, 11, "minecraft:polished_blackstone_bricks")
        s.set(x, F + 2, 10, "minecraft:blast_furnace[facing=south]"); s.set(x + 1, F + 2, 10, "minecraft:anvil")
        s.set(x + 2, F + 2, 10, "minecraft:lava_cauldron"); s.set(x + 3, F + 2, 10, "minecraft:smithing_table")
        s.chest(x + 4, F + 2, 10, L + "magmahold", "south")
    # Braseros d'ur-or
    for (x, z) in cercle(c, c, 13, 45):
        s.fill(x, F + 1, z, x, F + 2, z, "minecraft:polished_blackstone_brick_wall")
        s.set(x, F + 4, z, "minecraft:campfire")
    s.mob(c + 4, F + 1, c + 6, "zombie", "fyreslayer", 4)
    s.mob(c - 4, F + 1, c - 6, "zombie", "fyreslayer", 3)
    return s


def port_kharadron():
    """Port d'Éther : tour d'amarrage en cuivre, frégate Aéronaute avec endrin, hélices, canons et conduites d'aether."""
    W = 45
    s = Struct(W, 50, W, 48)
    c = W // 2
    cuivre = ["minecraft:waxed_cut_copper", "minecraft:waxed_exposed_cut_copper", "minecraft:waxed_copper_block"]
    # Tour d'amarrage
    s.cylinder(c, 6, 4, 0, 30, cuivre)
    for y in range(4, 30, 5):
        s.cylinder(c, 6, 5, y, y, "minecraft:waxed_copper_grate", hollow=True, inside=None)
        s.disk(c, 6, 3, y, "minecraft:spruce_planks")
        s.set(c, y, 6, "minecraft:air")
    for y in range(1, 30):
        s.set(c + 3, y, 6, "minecraft:ladder[facing=west]")
    s.clear(c, 1, 10, c, 2, 10)
    s.disk(c, 6, 6, 30, ["minecraft:waxed_cut_copper", "minecraft:spruce_planks"])
    s.walls(c - 6, 31, 0, c + 6, 31, 12, "minecraft:iron_bars")
    s.fill(c, 31, 6, c, 35, 6, "minecraft:waxed_copper_block")
    s.set(c, 36, 6, "minecraft:lightning_rod")
    # Bras d'amarrage
    s.fill(c - 1, 28, 11, c + 1, 28, 18, "minecraft:waxed_cut_copper")
    for z in range(12, 19, 2):
        s.fill(c - 1, 29, z, c - 1, 29, z, "minecraft:iron_bars"); s.fill(c + 1, 29, z, c + 1, 29, z, "minecraft:iron_bars")
    # Frégate (coque)
    z0, z1 = 18, W - 3
    for z in range(z0, z1 + 1):
        t = (z - z0) / (z1 - z0)
        half = 2 if t < 0.12 else 4 if t < 0.25 or t > 0.9 else 5
        s.fill(c - half, 22, z, c + half, 22, z, "minecraft:spruce_planks")
        s.fill(c - half + 1, 21, z, c + half - 1, 21, z, cuivre)
        s.fill(c - half + 2, 20, z, c + half - 2, 20, z, "minecraft:waxed_copper_block")
        s.set(c - half, 23, z, "minecraft:waxed_cut_copper"); s.set(c + half, 23, z, "minecraft:waxed_cut_copper")
        if z % 3 == 0:
            s.set(c - half, 22, z, "minecraft:glowstone"); s.set(c + half, 22, z, "minecraft:glowstone")  # conduites d'aether
    s.fill(c - 1, 22, z0 - 2, c + 1, 22, z0 - 1, "minecraft:waxed_copper_block")  # éperon
    s.set(c, 22, z0 - 3, "minecraft:lightning_rod[facing=north]")
    # Endrin (sphère de cuivre) au-dessus du navire
    ez = (z0 + z1) // 2
    for x in range(c - 5, c + 6):
        for y in range(26, 37):
            for z in range(ez - 6, ez + 7):
                d = ((x - c) / 5) ** 2 + ((y - 31) / 5) ** 2 + ((z - ez) / 6) ** 2
                if 0.75 < d <= 1.0:
                    s.set(x, y, z, "minecraft:waxed_copper_block" if (y + z) % 4 else "minecraft:waxed_exposed_copper")
    for (dx, dz) in ((-4, -4), (4, -4), (-4, 4), (4, 4)):
        s.fill(c + dx, 23, ez + dz, c + dx, 26, ez + dz, "minecraft:iron_chain")
    # Hélices et canons
    for dx in (-6, 6):
        s.fill(c + dx, 22, z1 - 2, c + dx, 22, z1 - 2, "minecraft:waxed_copper_block")
        s.fill(c + dx, 20, z1 - 2, c + dx, 24, z1 - 2, "minecraft:waxed_copper_grate")
        s.fill(c + dx, 22, z1 - 4, c + dx, 22, z1, "minecraft:waxed_copper_grate")
    for z in range(z0 + 4, z1 - 3, 5):
        s.set(c - 5, 23, z, "minecraft:dispenser[facing=west]"); s.set(c + 5, 23, z, "minecraft:dispenser[facing=east]")
    # Cabine de pilotage
    s.hollow(c - 3, 22, z1 - 7, c + 3, 26, z1 - 2, cuivre, floor="minecraft:spruce_planks")
    s.fill(c - 2, 24, z1 - 7, c + 2, 25, z1 - 7, "minecraft:yellow_stained_glass")
    s.clear(c - 3, 23, z1 - 4, c - 3, 24, z1 - 4)
    s.set(c, 23, z1 - 3, "minecraft:lectern[facing=north]")
    s.chest(c + 2, 23, z1 - 3, L + "port_kharadron", "west"); s.chest(c - 2, 23, z1 - 3, L + "port_kharadron", "east")
    s.set(c, 25, z1 - 5, "minecraft:lantern[hanging=true]")
    # Quai au sol et entrepôt d'aether-or
    s.fill(0, 0, 0, W - 1, 0, 15, ["minecraft:waxed_cut_copper", "minecraft:spruce_planks", "minecraft:stone_bricks"])
    s.hollow(2, 0, 2, 11, 6, 12, cuivre, floor="minecraft:spruce_planks")
    s.clear(11, 1, 6, 11, 3, 7)
    for z in range(3, 12, 2):
        s.barrel(3, 1, z, L + "port_kharadron"); s.set(4, 1, z, "minecraft:glowstone")
    s.mob(c, 23, ez, "skeleton", "kharadron", 4)
    s.mob(8, 1, 8, "skeleton", "kharadron", 2)
    return s


def sanctuaire_lumineth():
    """Sanctuaire de Lumière : terrasses de calcite, spire à cristal flottant, arches aelfiques, jardins blancs."""
    W = 41
    s = base(W, 56, W, ["minecraft:calcite", "minecraft:smooth_quartz", "minecraft:polished_diorite"], "minecraft:calcite", 49, haut=14)
    c = W // 2
    blanc = ["minecraft:smooth_quartz", "minecraft:quartz_bricks", "minecraft:calcite"]
    # Terrasses circulaires
    for i, r in enumerate((17, 13, 9)):
        y = F + i * 3
        s.cylinder(c, c, r, F, y + 2, blanc, hollow=False)
        s.cylinder(c, c, r, y + 3, y + 3, "minecraft:quartz_slab", hollow=True, inside=None)
        for (x, z) in cercle(c, c, r, 30):
            s.set(x, y + 3, z, "minecraft:diorite_wall"); s.set(x, y + 4, z, "minecraft:end_rod")
    # Escaliers d'accès
    for i in range(9):
        s.fill(c - 1, F + 1 + i, W - 4 - i * 1, c + 1, F + 1 + i, W - 4 - i * 1, "minecraft:quartz_stairs[facing=north]")
    # Spire
    s.cylinder(c, c, 4, F + 9, F + 34, blanc)
    for y in range(F + 11, F + 34, 5):
        for (dx, dz) in ((4, 0), (-4, 0), (0, 4), (0, -4)):
            s.set(c + dx, y, c + dz, "minecraft:white_stained_glass"); s.set(c + dx, y + 1, c + dz, "minecraft:white_stained_glass")
    for y in range(F + 9, F + 34, 6):
        s.cylinder(c, c, 5, y, y, "minecraft:gold_block", hollow=True, inside=None)
    s.cone(c, c, 4, F + 35, "minecraft:quartz_block")
    s.clear(c, F + 10, c + 4, c, F + 12, c + 4)
    s.set(c, F + 10, c, "minecraft:beacon"); s.fill(c - 1, F + 9, c - 1, c + 1, F + 9, c + 1, "minecraft:gold_block")
    s.chest(c + 2, F + 10, c, L + "sanctuaire_lumineth", "west"); s.chest(c - 2, F + 10, c, L + "sanctuaire_lumineth", "east")
    # Cristal flottant au sommet
    for y in range(F + 44, F + 51):
        r = 2 - abs(y - (F + 47)) // 2
        s.cylinder(c, c, max(r, 0), y, y, ["minecraft:white_stained_glass", "minecraft:light_blue_stained_glass"], hollow=False)
    s.set(c, F + 47, c, "minecraft:sea_lantern")
    for k in range(F + 40, F + 44):
        s.set(c, k, c, "minecraft:end_rod")
    # Arches aelfiques
    for (x, z) in ((c, 1), (1, c), (W - 2, c)):
        if x == c:
            for dx in (-3, 3):
                s.fill(x + dx, F + 1, z, x + dx, F + 7, z, "minecraft:quartz_pillar")
            for dx in range(-3, 4):
                s.set(x + dx, F + 8 + (1 if abs(dx) < 2 else 0), z, "minecraft:smooth_quartz")
            s.set(x, F + 10, z, "minecraft:end_rod")
        else:
            for dz in (-3, 3):
                s.fill(x, F + 1, z + dz, x, F + 7, z + dz, "minecraft:quartz_pillar")
            for dz in range(-3, 4):
                s.set(x, F + 8 + (1 if abs(dz) < 2 else 0), z + dz, "minecraft:smooth_quartz")
    # Jardins de fleurs blanches et bassins
    for x in range(1, W - 1, 2):
        for z in range(1, W - 1, 2):
            d = math.hypot(x - c, z - c)
            if 18 < d < 20 and s.rng.random() < 0.7:
                s.set(x, F + 1, z, s.rng.choice(["minecraft:lily_of_the_valley", "minecraft:white_tulip", "minecraft:oxeye_daisy"]))
    s.mob(c + 6, F + 7, c, "zombie", "lumineth_garde", 2)
    s.mob(c - 6, F + 7, c, "skeleton", "lumineth", 3)
    return s


def temple_khaine():
    """Temple de Morvaine : chaudron de sang géant, Cœur de fer de Morvaine, arches de lames, trône de Morvaine."""
    W = 41
    s = base(W, 34, W, ["minecraft:red_nether_bricks", "minecraft:nether_bricks", "minecraft:polished_blackstone"],
             "minecraft:nether_bricks", 50, haut=14)
    c = W // 2
    rouge = ["minecraft:red_nether_bricks", "minecraft:red_nether_bricks", "minecraft:nether_bricks", "minecraft:polished_blackstone_bricks"]
    rempart(s, 3, 3, W - 4, W - 4, F + 1, 9, rouge, "minecraft:polished_blackstone", "minecraft:red_nether_brick_stairs",
            "minecraft:red_nether_brick_wall", "minecraft:red_nether_brick_slab[type=top]")
    s.clear(c - 2, F + 1, W - 5, c + 2, F + 6, W - 3)
    # Arches de lames le long de l'allée
    for z in range(c + 4, W - 5, 4):
        for dx in (-3, 3):
            s.fill(c + dx, F + 1, z, c + dx, F + 6, z, "minecraft:polished_blackstone")
        for dx in range(-3, 4):
            s.set(c + dx, F + 7, z, "minecraft:iron_bars")
        s.set(c - 2, F + 8, z, "minecraft:iron_bars"); s.set(c + 2, F + 8, z, "minecraft:iron_bars")
        s.set(c, F + 8, z, "minecraft:redstone_lamp[lit=true]")
    tapis(s, c - 1, c + 3, c + 1, W - 5, F + 1, "red")
    # Chaudron de sang géant
    s.cylinder(c, c, 5, F + 1, F + 4, "minecraft:iron_block", hollow=True, inside="minecraft:air")
    s.disk(c, c, 4, F + 3, "minecraft:red_concrete")
    s.disk(c, c, 3, F + 4, "minecraft:red_stained_glass")
    for (dx, dz) in ((5, 0), (-5, 0), (0, 5), (0, -5)):
        s.set(c + dx, F + 5, c + dz, "minecraft:iron_bars")
    s.disk(c, c, 3, F, "minecraft:magma_block")
    # Le Cœur de fer de Morvaine (sur l'autel nord)
    hx, hz = c, 8
    s.fill(hx - 3, F + 1, hz - 2, hx + 3, F + 2, hz + 2, "minecraft:polished_blackstone_bricks")
    for (dx, dy) in ((-2, 0), (-1, 0), (1, 0), (2, 0), (-2, 1), (-1, 1), (0, 1), (1, 1), (2, 1), (-1, 2), (0, 2), (1, 2), (0, 3),
                     (-2, -1), (-1, -1), (0, -1), (1, -1), (2, -1)):
        s.set(hx + dx, F + 7 - dy, hz, "minecraft:iron_block")
    s.set(hx, F + 7, hz, "minecraft:redstone_block")
    for y in range(F + 3, F + 4):
        s.set(hx, y, hz, "minecraft:iron_block")
    for dx in (-3, 3):
        s.fill(hx + dx, F + 3, hz, hx + dx, F + 9, hz, "minecraft:iron_bars")
        s.set(hx + dx, F + 10, hz, "minecraft:soul_campfire")
    # Trône de Morvaine
    s.set(c - 8, F + 1, 8, "minecraft:polished_blackstone_stairs[facing=south]")
    s.fill(c - 8, F + 2, 7, c - 8, F + 5, 7, "minecraft:obsidian")
    s.set(c - 9, F + 4, 7, "minecraft:obsidian"); s.set(c - 7, F + 4, 7, "minecraft:obsidian")
    s.chest(c + 6, F + 1, 7, L + "temple_khaine", "south"); s.chest(c + 8, F + 1, 7, L + "temple_khaine", "south")
    for z in range(8, W - 6, 5):
        banniere_murale(s, 5, F + 5, z, "red", "east"); banniere_murale(s, W - 6, F + 5, z, "black", "west")
    s.mob(c, F + 1, c + 8, "zombie", "khaine_aelf", 5)
    s.mob(c - 6, F + 1, 10, "zombie", "khaine_aelf", 2)
    return s


def ruines_idoneth():
    """Enclave Abyssal : dômes de nacre, spires de prismarine, squelette de Léviadon, jardins de corail."""
    W = 41
    s = Struct(W, 26, W, 51)
    c = W // 2
    s.fill(0, 0, 0, W - 1, 1, W - 1, ["minecraft:sand", "minecraft:gravel", "minecraft:prismarine"])
    s.disk(c, c, 16, 2, ["minecraft:prismarine_bricks", "minecraft:dark_prismarine", "minecraft:prismarine"])
    # Dôme principal en nacre
    for y in range(2, 13):
        r = int(math.sqrt(max(0, 10 ** 2 - (y - 2) ** 2)))
        s.cylinder(c, c, r, y, y, ["minecraft:prismarine_bricks", "minecraft:dark_prismarine", "minecraft:light_blue_stained_glass"],
                   hollow=True, inside="minecraft:water")
    s.clear(c - 1, 3, c + 9, c + 1, 5, c + 10)
    s.fill(c - 1, 3, c + 9, c + 1, 5, c + 10, "minecraft:water")
    s.set(c, 3, c, "minecraft:conduit[waterlogged=true]")
    s.set(c, 2, c, "minecraft:sea_lantern")
    for (dx, dz) in ((-4, -4), (4, -4)):
        s.set(c + dx, 3, c + dz, "minecraft:chest[facing=south,waterlogged=true]",
              {"id": "minecraft:chest", "LootTable": L + "ruines_idoneth", "Items": []})
    # Spires
    for (x, z) in cercle(c, c, 15, 45):
        s.fill(x, 3, z, x, 12, z, ["minecraft:prismarine_bricks", "minecraft:dark_prismarine"])
        s.set(x, 14, z, "minecraft:sea_pickle[pickles=4,waterlogged=true]")
    # Squelette de Léviadon (tortue géante)
    lz = 4
    for x in range(c - 8, c + 9):
        s.set(x, 7, lz, "minecraft:bone_block[axis=x]")
    for x in range(c - 6, c + 7, 2):
        for k in range(1, 5):
            s.set(x, 7 - k, lz - (k + 1) // 2, "minecraft:bone_block[axis=y]"); s.set(x, 7 - k, lz + (k + 1) // 2, "minecraft:bone_block[axis=y]")
    s.fill(c + 9, 5, lz - 1, c + 11, 7, lz + 1, "minecraft:bone_block")
    # Jardins de corail
    for x in range(2, W - 2, 2):
        for z in range(2, W - 2, 2):
            d = math.hypot(x - c, z - c)
            if 11 < d < 15 and s.rng.random() < 0.5:
                s.set(x, 3, z, s.rng.choice(["minecraft:tube_coral_block", "minecraft:brain_coral_block", "minecraft:fire_coral_block"]))
                s.set(x, 4, z, s.rng.choice(["minecraft:tube_coral[waterlogged=true]", "minecraft:brain_coral[waterlogged=true]",
                                             "minecraft:sea_pickle[pickles=2,waterlogged=true]"]))
    s.mob(c + 6, 3, c + 6, "drowned", "idoneth", 4)
    s.mob(c - 6, 3, c - 6, "drowned", "idoneth", 2)
    return s


# =================================================================== CHAOS
def ziggurat_hashut():
    """Ziggurat de Ashkar : gradins d'obsidienne, cornes de taureau, cheminées infernales, enclos d'esclaves."""
    W = 45
    s = base(W, 42, W, ["minecraft:polished_blackstone", "minecraft:blackstone", "minecraft:basalt"], "minecraft:blackstone", 52)
    c = W // 2
    x0, x1, y = 5, W - 6, F + 1
    while x1 - x0 >= 8:
        s.fill(x0, y, x0, x1, y + 2, x1, ["minecraft:polished_blackstone_bricks", "minecraft:obsidian", "minecraft:polished_blackstone_bricks"])
        for k in range(x0, x1 + 1, 4):
            for (xx, zz) in ((k, x0), (k, x1), (x0, k), (x1, k)):
                s.set(xx, y + 1, zz, "minecraft:magma_block")
        x0 += 3; x1 -= 3; y += 3
    top = y
    for i in range(top - F - 1):
        zz = W - 6 - (i * 3) // 3
        s.fill(c - 2, F + 1 + i, zz, c + 2, F + 1 + i, zz, "minecraft:polished_blackstone_stairs[facing=north]")
    # Taureau de Ashkar
    s.fill(c - 3, top, c - 2, c + 3, top + 3, c + 2, "minecraft:gilded_blackstone")
    s.fill(c - 2, top + 4, c - 1, c + 2, top + 5, c + 1, "minecraft:gilded_blackstone")
    for side in (-1, 1):
        for k in range(4):
            s.set(c + side * (3 + k), top + 5 + k // 2, c, "minecraft:gold_block")
    s.set(c - 1, top + 4, c + 2, "minecraft:magma_block"); s.set(c + 1, top + 4, c + 2, "minecraft:magma_block")
    s.set(c, top + 6, c, "minecraft:campfire")
    # Cheminées infernales
    for (x, z) in ((8, 8), (W - 9, 8), (8, W - 9), (W - 9, W - 9)):
        s.cylinder(x, z, 2, F + 1, F + 18, ["minecraft:polished_blackstone_bricks", "minecraft:cracked_polished_blackstone_bricks"])
        s.set(x, F + 19, z, "minecraft:campfire[signal_fire=true]")
        s.set(x, F + 18, z, "minecraft:magma_block")
    # Forge intérieure
    s.clear(c - 4, F + 1, c - 4, c + 4, F + 5, c + 4)
    s.clear(c - 1, F + 1, c + 4, c + 1, F + 3, W - 6)
    s.fill(c - 4, F, c - 4, c + 4, F, c + 4, "minecraft:magma_block")
    s.disk(c, c, 1, F, "minecraft:lava")
    s.set(c - 3, F + 1, c - 3, "minecraft:blast_furnace[facing=south]"); s.set(c + 3, F + 1, c - 3, "minecraft:anvil")
    s.chest(c - 2, F + 1, c - 4, L + "ziggurat_hashut", "south"); s.chest(c + 2, F + 1, c - 4, L + "ziggurat_hashut", "south")
    s.set(c, F + 4, c, "minecraft:shroomlight")
    # Enclos d'esclaves
    s.walls(1, F + 1, c - 4, 4, F + 3, c + 4, "minecraft:iron_bars")
    s.mob(2, F + 1, c, "villager", "habitant")
    s.mob(c, F + 1, W - 4, "zombie", "hashut", 4)
    s.mob(c, top, c + 3, "skeleton", "hashut_tireur", 2)
    return s


def repaire_skaven():
    """Clocher Hurlant : spire penchée de bois et pierre, cloche géante, canon à malefoudre, puits de fangepierre."""
    W = 37
    s = base(W, 52, W, ["minecraft:coarse_dirt", "minecraft:gravel", "minecraft:mud", "minecraft:cobblestone"], "minecraft:dirt", 53)
    c = W // 2
    pourri = ["minecraft:cobblestone", "minecraft:mossy_cobblestone", "minecraft:cracked_stone_bricks", "minecraft:spruce_planks",
              "minecraft:stripped_spruce_log", "minecraft:stone_bricks"]
    # Spire penchée
    for y in range(F + 1, F + 38):
        off = (y - F) // 7
        r = 5 if y < F + 10 else 4 if y < F + 24 else 3
        s.cylinder(c + off, c, r, y, y, pourri, hollow=True, inside="minecraft:air")
        if y % 6 == 0:
            s.disk(c + off, c, r - 1, y, "minecraft:spruce_planks")
            s.set(c + off, y, c, "minecraft:air")
    for y in range(F + 1, F + 37):
        off = (y - F) // 7
        s.set(c + off + 1, y, c, "minecraft:ladder[facing=west]")
    # Échafaudages extérieurs
    for y in range(F + 4, F + 30, 4):
        off = (y - F) // 7
        s.fill(c + off - 7, y, c - 1, c + off - 5, y, c + 1, "minecraft:spruce_slab")
        s.set(c + off - 7, y - 1, c, "minecraft:spruce_fence")
    # Cloche géante
    top = F + 38
    off = 38 // 7
    s.fill(c + off - 3, top, c - 3, c + off + 3, top, c + 3, "minecraft:spruce_planks")
    for (dx, dz) in ((-3, -3), (3, -3), (-3, 3), (3, 3)):
        s.fill(c + off + dx, top + 1, c + dz, c + off + dx, top + 6, c + dz, "minecraft:spruce_log")
    s.fill(c + off - 3, top + 7, c - 3, c + off + 3, top + 7, c + 3, "minecraft:spruce_planks")
    for y in range(top + 2, top + 6):
        r = 1 + (y - top - 2) // 2
        s.cylinder(c + off, c, r, y, y, "minecraft:gold_block", hollow=True, inside="minecraft:air")
    s.set(c + off, top + 6, c, "minecraft:iron_chain")
    s.set(c + off, top + 8, c, "minecraft:verdant_froglight")
    s.fill(c + off, top + 9, c, c + off, top + 11, c, "minecraft:lightning_rod")
    # Canon à malefoudre
    s.fill(4, F + 1, 4, 6, F + 2, 6, "minecraft:waxed_weathered_copper")
    s.fill(5, F + 3, 5, 5, F + 3, 10, "minecraft:waxed_copper_grate")
    s.set(5, F + 3, 11, "minecraft:lime_stained_glass"); s.set(5, F + 4, 5, "minecraft:verdant_froglight")
    s.fill(5, F + 4, 6, 5, F + 4, 9, "minecraft:lightning_rod[facing=south]")
    # Puits de fangepierre et tunnels
    for (x, z) in ((W - 6, 6), (6, W - 6), (W - 7, W - 7)):
        s.fill(x - 1, F - 3, z - 1, x + 1, F, z + 1, "minecraft:air")
        s.walls(x - 2, F + 1, z - 2, x + 2, F + 1, z + 2, "minecraft:spruce_fence")
        s.set(x, F - 3, z, "minecraft:verdant_froglight")
        s.set(x - 1, F - 3, z, "minecraft:chest[facing=east]", {"id": "minecraft:chest", "LootTable": L + "repaire_skaven", "Items": []})
    for (x, z, h) in ((c - 9, c + 8, 4), (c + 10, c - 9, 3), (c - 10, c - 8, 5)):
        for y in range(F + 1, F + h + 1):
            s.set(x, y, z, "minecraft:verdant_froglight" if y < F + h else "minecraft:lime_stained_glass")
    s.chest(c - 2, F + 1, c + 1, L + "repaire_skaven", "east")
    s.mob(c - 1, F + 1, c, "zombie", "clanrat", 5)
    s.mob(c + 2, F + 13, c, "skeleton", "jezzail", 2)
    s.mob(8, F + 1, c + 8, "zombie", "clanrat", 3)
    return s


# =================================================================== MORT
def ossuaire_ossiarch():
    """Ossuaire Mortisan : remparts d'os sertis de crânes, tours-cages thoraciques, trône d'os de Katakros."""
    W = 45
    s = base(W, 34, W, ["minecraft:bone_block[axis=y]", "minecraft:smooth_sandstone", "minecraft:calcite"], "minecraft:sandstone", 54)
    c = W // 2
    os = ["minecraft:bone_block[axis=y]", "minecraft:bone_block[axis=y]", "minecraft:calcite", "minecraft:smooth_quartz"]
    rempart(s, 3, 3, W - 4, W - 4, F + 1, 10, os, "minecraft:purpur_pillar", "minecraft:quartz_stairs",
            "minecraft:diorite_wall", "minecraft:smooth_quartz_slab[type=top]")
    for x in range(5, W - 5, 3):
        s.set(x, F + 6, 3, "minecraft:skeleton_skull"); s.set(x, F + 6, W - 4, "minecraft:skeleton_skull")
    s.clear(c - 2, F + 1, W - 6, c + 2, F + 6, W - 3)
    # Tours-cages thoraciques
    for (cx, cz) in ((4, 4), (W - 5, 4), (4, W - 5), (W - 5, W - 5)):
        for y in range(F + 1, F + 18):
            for (x, z) in cercle(cx, cz, 3, 45):
                if y % 2 == 0 or (x - cx) * (z - cz) == 0:
                    s.set(x, y, z, "minecraft:bone_block[axis=y]")
        s.disk(cx, cz, 3, F + 18, "minecraft:purpur_block")
        s.set(cx, F + 19, cz, "minecraft:wither_skeleton_skull")
        s.set(cx, F + 10, cz, "minecraft:soul_lantern")
    # Ziggurat central à violet de Necrath
    top = s.pyramid(c - 9, c - 9, c + 9, c + 9, F + 1, os, step=1)
    for y in range(F + 1, top, 2):
        k = y - F - 1
        s.set(c - 9 + k, y, c, "minecraft:purpur_block"); s.set(c + 9 - k, y, c, "minecraft:purpur_block")
    s.clear(c - 4, F + 1, c - 4, c + 4, F + 4, c + 4); s.clear(c - 1, F + 1, c + 5, c + 1, F + 3, c + 9)
    # Trône d'os
    s.fill(c - 1, F + 1, c - 3, c + 1, F + 1, c - 2, "minecraft:bone_block")
    s.set(c, F + 2, c - 2, "minecraft:quartz_stairs[facing=south]")
    s.fill(c, F + 2, c - 3, c, F + 4, c - 3, "minecraft:bone_block[axis=y]")
    s.set(c, F + 5, c - 3, "minecraft:wither_skeleton_skull")
    s.chest(c - 3, F + 1, c - 3, L + "ossuaire_ossiarch", "south"); s.chest(c + 3, F + 1, c - 3, L + "ossuaire_ossiarch", "south")
    s.set(c, F + 4, c, "minecraft:soul_lantern[hanging=true]")
    crane_geant(s, c, top, c, "minecraft:bone_block", "minecraft:soul_lantern")
    s.mob(c + 5, F + 1, c + 12, "skeleton", "mortek", 5)
    s.mob(c - 8, F + 1, c + 12, "skeleton", "mortek", 3)
    return s


def cimetiere_nighthaunt():
    """Cimetière hanté : chapelle en ruine à vitraux, crypte, arbres morts aux lanternes d'âmes, gibets."""
    W = 37
    s = base(W, 26, W, ["minecraft:podzol", "minecraft:coarse_dirt", "minecraft:soul_soil", "minecraft:rooted_dirt"], "minecraft:dirt", 55, haut=16)
    c = W // 2
    s.walls(1, F + 1, 1, W - 2, F + 2, W - 2, ["minecraft:cobblestone_wall", "minecraft:mossy_cobblestone_wall"])
    for x in range(1, W - 1, 4):
        s.fill(x, F + 1, 1, x, F + 3, 1, "minecraft:mossy_stone_bricks"); s.set(x, F + 4, 1, "minecraft:soul_lantern")
    s.clear(c - 1, F + 1, W - 2, c + 1, F + 3, W - 2)
    s.fill(c - 1, F + 3, W - 2, c + 1, F + 3, W - 2, "minecraft:iron_bars")
    # Tombes
    for x in range(4, W - 4, 3):
        for z in range(18, W - 4, 4):
            if s.rng.random() < 0.8:
                s.set(x, F + 1, z, s.rng.choice(["minecraft:cobblestone_wall", "minecraft:mossy_cobblestone_wall", "minecraft:stone_brick_wall",
                                                 "minecraft:deepslate_brick_wall"]))
                s.set(x, F, z + 1, "minecraft:soul_soil")
                if s.rng.random() < 0.3:
                    s.set(x, F + 2, z, "minecraft:skeleton_skull")
    # Chapelle gothique en ruine
    s.hollow(c - 6, F, 3, c + 6, F + 12, 15, ["minecraft:deepslate_bricks", "minecraft:cracked_deepslate_bricks", "minecraft:mossy_stone_bricks"],
             floor="minecraft:polished_deepslate")
    s.roof_gable(c - 6, 3, c + 6, 15, F + 13, "minecraft:deepslate_tile_stairs", "minecraft:deepslate_tiles", axis="z")
    for z in (6, 10):
        fenetre_arc(s, c - 6, F + 4, z, "z", 5, "minecraft:purple_stained_glass_pane", "minecraft:deepslate_brick_stairs")
        fenetre_arc(s, c + 6, F + 4, z, "z", 5, "minecraft:purple_stained_glass_pane", "minecraft:deepslate_brick_stairs")
    s.clear(c - 1, F + 1, 15, c + 1, F + 5, 15)
    s.fill(c - 1, F + 1, 4, c + 1, F + 1, 5, "minecraft:polished_deepslate")
    s.set(c, F + 2, 4, "minecraft:skeleton_skull")
    for dx in (-2, 2):
        s.set(c + dx, F + 2, 4, "minecraft:white_candle[candles=4,lit=true]")
    lustre(s, c, F + 12, 9, 4, "minecraft:soul_lantern[hanging=true]")
    # ruine : trous dans la toiture
    for (x, y, z) in list(s.blocks):
        if y > F + 9 and 3 <= z <= 15 and abs(x - c) <= 7 and s.rng.random() < 0.25:
            del s.blocks[(x, y, z)]
    # Crypte
    s.fill(c - 3, F - 3, 6, c + 3, F - 1, 12, "minecraft:air")
    s.walls(c - 4, F - 4, 5, c + 4, F, 13, "minecraft:deepslate_bricks")
    s.fill(c - 4, F - 4, 5, c + 4, F - 4, 13, "minecraft:polished_deepslate")
    for i in range(3):
        s.set(c + 3, F - i, 13 - i, "minecraft:deepslate_brick_stairs[facing=north]")
    s.chest(c, F - 3, 6, L + "cimetiere_nighthaunt", "south")
    s.set(c - 2, F - 3, 9, "minecraft:soul_campfire"); s.set(c + 2, F - 3, 9, "minecraft:soul_campfire")
    # Arbres morts aux lanternes
    for (x, z) in ((5, c), (W - 6, c + 3), (6, W - 6)):
        s.fill(x, F + 1, z, x, F + 8, z, "minecraft:dark_oak_log")
        for (dx, dz, yy) in ((1, 0, F + 6), (-1, 0, F + 7), (0, 1, F + 5)):
            for k in range(1, 4):
                s.set(x + dx * k, yy + k // 2, z + dz * k, "minecraft:dark_oak_wood")
        s.set(x + 3, F + 6, z, "minecraft:iron_chain"); s.set(x + 3, F + 5, z, "minecraft:soul_lantern[hanging=true]")
    s.mob(c, F + 1, c + 4, "zombie", "chainrasp", 4)
    s.mob(c - 5, F + 1, 22, "skeleton", "glaivewraith", 2)
    s.mob(c, F - 3, 9, "skeleton", "glaivewraith", 1)
    return s


# =================================================================== PORTAIL DE ROYAUME
def portail():
    """Portail de Royaume (Realmgate) : anneau runique monumental, dalle étoilée, piliers et éclats. Entrer = voyager."""
    W = 23
    s = base(W, 28, W, ["minecraft:chiseled_stone_bricks", "minecraft:stone_bricks", "minecraft:polished_andesite"],
             "minecraft:stone_bricks", 56, haut=18)
    c = W // 2
    s.disk(c, c, 10, F, ["minecraft:stone_bricks", "minecraft:polished_andesite", "minecraft:cracked_stone_bricks"])
    s.disk(c, c, 6, F, "minecraft:polished_deepslate")
    etoile8(s, c, F, c, 6, "minecraft:gold_block", "minecraft:lodestone")
    # Marches circulaires
    s.cylinder(c, c, 10, F + 1, F + 1, "minecraft:stone_brick_slab", hollow=True, inside=None)
    # Anneau vertical épais (2 couches) orné de runes d'or
    R = 8
    for a in range(0, 360, 4):
        for rr in (R, R + 1):
            x = c + round(rr * math.cos(math.radians(a)))
            y = F + 1 + R + round(rr * math.sin(math.radians(a)))
            if y >= F + 1:
                bloc = "minecraft:gold_block" if (a % 40 == 0 and rr == R) else "minecraft:chiseled_stone_bricks" if a % 20 == 0 else "minecraft:stone_bricks"
                s.set(x, y, c, bloc)
    # Voile de royaume
    for x in range(c - R, c + R + 1):
        for y in range(F + 1, F + 2 * R + 2):
            if (x - c) ** 2 + (y - F - 1 - R) ** 2 < (R - 0.5) ** 2 and s.get(x, y, c) in (None, "minecraft:air"):
                s.set(x, y, c, "minecraft:purple_stained_glass_pane" if (x * 3 + y) % 4 else "minecraft:magenta_stained_glass_pane")
    s.clear(c - 1, F + 1, c, c + 1, F + 3, c)
    s.set(c, F + 1 + 2 * R + 2, c, "minecraft:amethyst_cluster")
    # Piliers gardiens et braseros
    for dx in (-10, 10):
        s.fill(c + dx, F + 1, c, c + dx, F + 7, c, "minecraft:chiseled_stone_bricks")
        s.set(c + dx, F + 8, c, "minecraft:soul_campfire")
    for (x, z) in ((c - 7, c - 7), (c + 7, c - 7), (c - 7, c + 7), (c + 7, c + 7)):
        s.fill(x, F + 1, z, x, F + 2, z, "minecraft:amethyst_block")
        s.set(x, F + 3, z, "minecraft:amethyst_cluster")
    s.entities.append(((c + 0.5, F + 1, c + 0.5), (c, F + 1, c), {"id": "minecraft:marker", "Tags": ["rm_portail"]}))
    return s


# =================================================================== REPAIRES DE BOSS
def necropole_nagash():
    W = 51
    s = base(W, 46, W, ["minecraft:polished_deepslate", "minecraft:deepslate_tiles", "minecraft:bone_block[axis=y]"],
             "minecraft:cobbled_deepslate", 61, haut=14)
    c = W // 2
    noir = ["minecraft:deepslate_bricks", "minecraft:polished_deepslate", "minecraft:deepslate_tiles"]
    # Grand escalier de pyramide noire
    N = 10
    for k in range(N):
        y = F + 1 + k
        s.fill(3 + k, y, 3 + k, W - 4 - k, y, W - 4 - k, noir)
        for (xx, zz) in ((3 + k, c), (W - 4 - k, c), (c, 3 + k)):
            s.set(xx, y, zz, "minecraft:purpur_block")
        for (xx, zz) in ((3 + k, 3 + k), (W - 4 - k, 3 + k), (3 + k, W - 4 - k), (W - 4 - k, W - 4 - k)):
            s.set(xx, y + 1, zz, "minecraft:soul_lantern") if k % 3 == 0 else None
    top = F + 1 + N
    s.fill(3 + N, top - 1, 3 + N, W - 4 - N, top - 1, W - 4 - N, ["minecraft:polished_deepslate", "minecraft:bone_block[axis=y]"])
    etoile8(s, c, top - 1, c, 9, "minecraft:purpur_block", "minecraft:crying_obsidian")
    for i in range(N):
        s.fill(c - 2, F + 1 + i, W - 4 - i, c + 2, F + 1 + i, W - 4 - i, "minecraft:deepslate_brick_stairs[facing=north]")
    # Huit obélisques funéraires
    for (x, z) in cercle(c, c, 9, 45):
        s.fill(x, top, z, x, top + 10, z, ["minecraft:polished_deepslate", "minecraft:bone_block[axis=y]"])
        s.set(x, top + 11, z, "minecraft:soul_campfire")
    # Trône de Necrath
    s.fill(c - 3, top, c - 8, c + 3, top + 1, c - 6, "minecraft:polished_deepslate")
    s.fill(c - 1, top + 2, c - 8, c + 1, top + 9, c - 8, "minecraft:bone_block[axis=y]")
    s.fill(c - 3, top + 7, c - 8, c + 3, top + 7, c - 8, "minecraft:bone_block[axis=x]")
    crane_geant(s, c, top + 10, c - 8, "minecraft:bone_block", "minecraft:soul_lantern")
    s.chest(c - 4, top, c - 7, L + "chateau_soulblight", "south"); s.chest(c + 4, top, c - 7, L + "ossuaire_ossiarch", "south")
    s.mob(c, top, c, "wither_skeleton", "boss_nagash")
    s.mob(c - 5, top, c + 5, "skeleton", "mortek", 3)
    return s


def trone_archaon():
    W = 49
    s = base(W, 44, W, ["minecraft:polished_blackstone", "minecraft:blackstone", "minecraft:crimson_nylium"], "minecraft:blackstone", 62, haut=14)
    c = W // 2
    noir = ["minecraft:polished_blackstone_bricks", "minecraft:obsidian", "minecraft:blackstone"]
    # Arène circulaire bordée de pointes
    s.cylinder(c, c, 22, F + 1, F + 4, noir, hollow=True, inside="minecraft:air")
    for (x, z) in cercle(c, c, 22, 12):
        h = 8 + (x + z) % 6
        s.fill(x, F + 5, z, x, F + h, z, ["minecraft:obsidian", "minecraft:crying_obsidian"])
        s.set(x, F + h + 1, z, "minecraft:pointed_dripstone[vertical_direction=up]")
    s.clear(c - 2, F + 1, W - 3, c + 2, F + 4, W - 2)
    etoile8(s, c, F, c, 18, "minecraft:red_concrete", "minecraft:crying_obsidian", pointe="minecraft:soul_campfire")
    s.cylinder(c, c, 6, F, F, "minecraft:lava", hollow=True, inside=None)
    # Trône de l'Élu au nord
    s.fill(c - 4, F + 1, 3, c + 4, F + 3, 7, noir)
    s.set(c, F + 4, 5, "minecraft:polished_blackstone_stairs[facing=south]")
    s.fill(c, F + 5, 3, c, F + 12, 3, "minecraft:obsidian")
    for k in range(4):
        s.set(c - 1 - k, F + 9 + k, 3, "minecraft:obsidian"); s.set(c + 1 + k, F + 9 + k, 3, "minecraft:obsidian")
    s.set(c, F + 13, 3, "minecraft:crying_obsidian")
    s.chest(c - 3, F + 4, 5, L + "citadelle_chaos", "south"); s.chest(c + 3, F + 4, 5, L + "citadelle_chaos", "south")
    s.mob(c, F + 1, c, "zombie", "boss_archaon")
    s.mob(c - 6, F + 1, c + 8, "zombie", "chaos_guerrier", 4)
    return s


def arene_gordrakk():
    W = 47
    s = base(W, 30, W, ["minecraft:coarse_dirt", "minecraft:packed_mud", "minecraft:gravel"], "minecraft:dirt", 63, haut=14)
    c = W // 2
    ferraille = ["minecraft:iron_block", "minecraft:waxed_exposed_cut_copper", "minecraft:spruce_planks", "minecraft:waxed_weathered_copper"]
    # Gradins de ferraille
    for i in range(4):
        s.cylinder(c, c, 21 - i, F + 1 + i, F + 1 + i, ferraille, hollow=True, inside=None)
    for (x, z) in cercle(c, c, 22, 15):
        s.fill(x, F + 1, z, x, F + 9, z, "minecraft:stripped_spruce_log")
        s.set(x, F + 10, z, "minecraft:skeleton_skull")
    s.clear(c - 2, F + 1, W - 3, c + 2, F + 5, W - 1)
    # Idole de Brog & Mog (deux têtes)
    for (hx, col) in ((c - 6, "minecraft:green_terracotta"), (c + 6, "minecraft:lime_terracotta")):
        s.fill(hx - 3, F + 1, 3, hx + 3, F + 9, 6, col)
        s.set(hx - 1, F + 7, 7, "minecraft:redstone_block"); s.set(hx + 1, F + 7, 7, "minecraft:redstone_block")
        s.fill(hx - 2, F + 3, 7, hx + 2, F + 3, 7, "minecraft:black_concrete")
        for dx in (-2, 0, 2):
            s.set(hx + dx, F + 3, 7, "minecraft:bone_block[axis=y]")
        s.fill(hx - 3, F + 10, 3, hx + 3, F + 10, 6, "minecraft:iron_block")
    s.chest(c, F + 1, 5, L + "camp_orruk", "south")
    s.mob(c, F + 1, c, "zombie", "boss_gordrakk")
    s.mob(c + 6, F + 1, c + 8, "zombie", "brute", 4)
    return s


def autel_skarbrand():
    W = 45
    s = base(W, 36, W, ["minecraft:basalt", "minecraft:blackstone", "minecraft:magma_block"], "minecraft:blackstone", 64, haut=14)
    c = W // 2
    # Fosse de sang et pyramide crânes de Sangrath
    s.cylinder(c, c, 15, F, F, "minecraft:red_concrete", hollow=False)
    s.cylinder(c, c, 16, F + 1, F + 2, ["minecraft:polished_blackstone_bricks", "minecraft:gilded_blackstone"], hollow=True, inside=None)
    for (x, z) in cercle(c, c, 16, 24):
        s.fill(x, F + 3, z, x, F + 7, z, "minecraft:polished_blackstone_brick_wall")
        s.set(x, F + 8, z, "minecraft:campfire")
    s.clear(c - 2, F + 1, W - 7, c + 2, F + 3, W - 3)
    # Trône de crânes (rune de Sangrath en or)
    top = s.pyramid(c - 6, 3, c + 6, 15, F + 1, ["minecraft:bone_block", "minecraft:skeleton_skull", "minecraft:bone_block"], step=1)
    s.fill(c - 2, top, 7, c + 2, top + 4, 7, "minecraft:gold_block")
    s.fill(c - 1, top + 1, 7, c + 1, top + 1, 7, "minecraft:red_concrete")
    s.set(c, top + 3, 7, "minecraft:red_concrete")
    s.set(c - 2, top + 4, 7, "minecraft:air"); s.set(c + 2, top + 4, 7, "minecraft:air")
    s.chest(c - 8, F + 1, 9, L + "magmahold", "east"); s.chest(c + 8, F + 1, 9, L + "citadelle_chaos", "west")
    for (x, z) in ((6, 6), (W - 7, 6), (6, W - 7), (W - 7, W - 7)):
        for y in range(F + 1, F + 12):
            s.set(x, y, z, "minecraft:basalt")
        s.set(x, F + 12, z, "minecraft:netherrack"); s.set(x, F + 13, z, "minecraft:fire")
    s.mob(c, F + 1, c + 4, "piglin_brute", "boss_skarbrand")
    s.mob(c + 6, F + 1, c + 10, "zombie", "bloodreaver", 4)
    return s


def tour_thanquol():
    s = repaire_skaven()
    W = s.size[0]
    c = W // 2
    for (x, z) in cercle(c, c, 15, 20):
        s.fill(x, F + 1, z, x, F + 3, z, "minecraft:verdant_froglight" if (x + z) % 4 == 0 else "minecraft:spruce_fence")
    s.entities = [e for e in s.entities if "rm_p_jezzail" not in e[2].get("Tags", []) and e[2]["id"] != "royaumes:jezzail"]
    s.mob(c - 8, F + 1, c - 8, "ravager", "boss_thanquol")
    return s


def jardin_rotigus():
    W = 45
    s = base(W, 30, W, ["minecraft:mud", "minecraft:moss_block", "minecraft:mycelium", "minecraft:slime_block"], "minecraft:mud", 65, haut=14)
    c = W // 2
    # Chaudron géant de Grand-Père
    s.cylinder(c, c, 7, F + 1, F + 5, ["minecraft:waxed_oxidized_copper", "minecraft:waxed_weathered_copper", "minecraft:mossy_cobblestone"],
               hollow=True, inside="minecraft:water")
    s.disk(c, c, 6, F, "minecraft:magma_block")
    for (x, z) in cercle(c, c, 8, 45):
        s.fill(x, F + 1, z, x, F + 2, z, "minecraft:mossy_cobblestone_wall")
    # Arbres pourris et champignons
    for (x, z) in ((7, 7), (W - 8, 8), (8, W - 8), (W - 9, W - 9)):
        s.fill(x, F + 1, z, x, F + 9, z, "minecraft:mangrove_log")
        s.cylinder(x, z, 3, F + 10, F + 11, ["minecraft:moss_block", "minecraft:mangrove_leaves[persistent=true]", "minecraft:slime_block"], hollow=False)
        s.set(x + 1, F + 1, z, "minecraft:brown_mushroom"); s.set(x - 1, F + 1, z + 1, "minecraft:red_mushroom")
    # Mares putrides
    for (x, z) in ((c - 13, c + 6), (c + 12, c - 7)):
        s.disk(x, z, 3, F, "minecraft:water"); s.disk(x, z, 3, F - 1, "minecraft:mud")
        s.set(x, F + 1, z, "minecraft:lily_pad")
    s.chest(c - 9, F + 1, c - 9, L + "fort_kruleboyz", "south"); s.chest(c + 9, F + 1, c + 9, L + "fort_kruleboyz", "north")
    s.mob(c, F + 1, c + 11, "zombie", "boss_rotigus")
    s.mob(c - 6, F + 1, c + 12, "zombie", "pestigor", 4)
    return s


BUILDERS3 = {
    "camp_orruk": camp_orruk, "fort_kruleboyz": fort_kruleboyz, "antre_gitz": antre_gitz, "campement_ogor": campement_ogor,
    "temple_seraphon": temple_seraphon, "bosquet_sylvaneth": bosquet_sylvaneth, "magmahold": magmahold,
    "port_kharadron": port_kharadron, "sanctuaire_lumineth": sanctuaire_lumineth, "temple_khaine": temple_khaine,
    "ruines_idoneth": ruines_idoneth, "ziggurat_hashut": ziggurat_hashut, "repaire_skaven": repaire_skaven,
    "ossuaire_ossiarch": ossuaire_ossiarch, "cimetiere_nighthaunt": cimetiere_nighthaunt, "portail": portail,
    "necropole_nagash": necropole_nagash, "trone_archaon": trone_archaon, "arene_gordrakk": arene_gordrakk,
    "autel_skarbrand": autel_skarbrand, "tour_thanquol": tour_thanquol, "jardin_rotigus": jardin_rotigus,
}
START3 = {k: -F for k in BUILDERS3}
START3.update({"port_kharadron": -1, "fort_kruleboyz": -2, "ruines_idoneth": -1})

NOUVELLES_STRUCTURES = [
    dict(id="portail", nom="Portail de Royaume", biomes=["azyr_cimes", "hysh_plateaux", "ghyran_jade", "ghur_terres", "ghur_jungle",
                                                          "aqshy_cendres", "chamon_desert", "shyish_terres", "ulgu_brumes",
                                                          "chaos_desolation", "terres_rongees", "ghyran_marais"],
         monde=["plains", "meadow", "savanna", "forest", "desert", "taiga", "sunflower_plains", "cherry_grove", "snowy_plains"],
         espacement=30, sep=12),
    dict(id="necropole_nagash", nom="Nécropole de Necrath", biomes=["shyish_terres"], monde=[], espacement=56, sep=24),
    dict(id="trone_archaon", nom="Trône d'Varkhan", biomes=["chaos_desolation"], monde=[], espacement=56, sep=24),
    dict(id="arene_gordrakk", nom="Arène de Krognak", biomes=["ghur_terres"], monde=[], espacement=56, sep=24),
    dict(id="autel_skarbrand", nom="Autel de Brakhar", biomes=["aqshy_cendres"], monde=[], espacement=56, sep=24),
    dict(id="tour_thanquol", nom="Tour de Skrivel", biomes=["terres_rongees"], monde=[], espacement=56, sep=24),
    dict(id="jardin_rotigus", nom="Jardin de Putrefax", biomes=["ghyran_marais"], monde=[], espacement=56, sep=24),
]
