# -*- coding: utf-8 -*-
"""Outils de construction détaillée : remparts, tours, fenêtres, mobilier."""
import math

OPP = {"north": "south", "south": "north", "east": "west", "west": "east"}


def perimetre(x0, z0, x1, z1):
    """Cases du périmètre avec la direction extérieure."""
    for x in range(x0, x1 + 1):
        yield x, z0, "north"
        yield x, z1, "south"
    for z in range(z0 + 1, z1):
        yield x0, z, "west"
        yield x1, z, "east"


DV = {"north": (0, -1), "south": (0, 1), "west": (-1, 0), "east": (1, 0)}


def rempart(s, x0, z0, x1, z1, y0, h, mat, pilier, escalier, mur_bloc, sol_chemin, pas=5):
    """Rempart épais de 2 avec pilastres, corbeaux, merlons et chemin de ronde."""
    for (x, z, d) in perimetre(x0, z0, x1, z1):
        dx, dz = DV[d]
        on_corner = (x in (x0, x1)) and (z in (z0, z1))
        k = (x - x0) if d in ("north", "south") else (z - z0)
        for y in range(y0, y0 + h):
            # parement extérieur : pilastre tous les `pas` blocs, socle en pilier
            b = pilier if (k % pas == 0 or y == y0 or on_corner) else s._pick(mat)
            s.set(x, y, z, b)
            ix, iz = x - dx, z - dz
            if not on_corner:
                s.set(ix, y, iz, s._pick(mat))
        # bandeau décoratif
        s.set(x, y0 + h - 3, z, pilier)
        # corbeaux (mâchicoulis) sous le parapet
        ox, oz = x + dx, z + dz
        if not on_corner:
            s.set(ox, y0 + h - 1, oz, f"{escalier}[facing={OPP[d]},half=top]")
            s.set(ox, y0 + h, oz, s._pick(mat))
            # merlons
            s.set(ox, y0 + h + 1, oz, mur_bloc if (k % 2 == 0) else "minecraft:air")
        s.set(x, y0 + h, z, sol_chemin)
        s.set(x - dx, y0 + h, z - dz, sol_chemin)


def meurtrieres(s, x0, z0, x1, z1, y, pas=6, bloc="minecraft:iron_bars"):
    for (x, z, d) in perimetre(x0, z0, x1, z1):
        k = (x - x0) if d in ("north", "south") else (z - z0)
        if k % pas == pas // 2 and not ((x in (x0, x1)) and (z in (z0, z1))):
            s.set(x, y, z, bloc); s.set(x, y + 1, z, bloc)
            dx, dz = DV[d]
            s.set(x - dx, y, z - dz, "minecraft:air"); s.set(x - dx, y + 1, z - dz, "minecraft:air")


def tour(s, cx, cz, r, y0, h, mat, toit, toit_esc=None, pointe=None, fenetre="minecraft:glass_pane",
         etage=6, plancher="minecraft:spruce_planks", lanterne="minecraft:lantern[hanging=true]"):
    """Tour ronde avec base talutée, étages, fenêtres, couronne de corbeaux et toit conique."""
    # talus
    s.cylinder(cx, cz, r + 1, y0, y0 + 1, mat, hollow=False)
    s.cylinder(cx, cz, r, y0, y0 + h, mat, hollow=True, inside="minecraft:air")
    s.disk(cx, cz, r - 1, y0, plancher)
    for y in range(y0 + etage, y0 + h, etage):
        s.disk(cx, cz, r - 1, y, plancher)
        s.set(cx, y, cz, "minecraft:air")
        if lanterne:
            s.set(cx, y - 1, cz, lanterne)
    # échelle centrale
    for y in range(y0 + 1, y0 + h):
        if s.get(cx + r - 1, y, cz) in (None, "minecraft:air", plancher):
            s.set(cx + r - 1, y, cz, "minecraft:ladder[facing=west]")
        if (y - y0) % etage == 0:
            s.set(cx + r - 1, y, cz, "minecraft:ladder[facing=west]")
    # fenêtres
    for y in range(y0 + 3, y0 + h - 1, etage):
        for (dx, dz) in ((r, 0), (-r, 0), (0, r), (0, -r)):
            if (dx, dz) != (r, 0):
                s.set(cx + dx, y, cz + dz, fenetre); s.set(cx + dx, y + 1, cz + dz, fenetre)
    # couronne
    top = y0 + h
    s.cylinder(cx, cz, r + 1, top, top, mat, hollow=True, inside=None)
    s.disk(cx, cz, r, top, plancher)
    for i in range(0, 360, 30):
        a = math.radians(i)
        s.set(cx + round((r + 1) * math.cos(a)), top + 1, cz + round((r + 1) * math.sin(a)), s._pick(mat))
    # toit conique
    rr, y = r + 1, top + 2
    while rr >= 0:
        s.cylinder(cx, cz, rr, y, y, toit, hollow=True, inside=None)
        rr -= 1; y += 1
    s.set(cx, y, cz, toit)
    if pointe:
        s.fill(cx, y + 1, cz, cx, y + 2, cz, pointe)
    return top


def tour_carree(s, x0, z0, w, y0, h, mat, pilier, toit_esc, toit_plein, fenetre="minecraft:glass_pane",
                plancher="minecraft:spruce_planks", etage=6):
    x1, z1 = x0 + w - 1, z0 + w - 1
    s.hollow(x0, y0, z0, x1, y0 + h, z1, mat, floor=plancher)
    for (x, z) in ((x0, z0), (x1, z0), (x0, z1), (x1, z1)):
        s.fill(x, y0, z, x, y0 + h, z, pilier)
    for y in range(y0 + etage, y0 + h, etage):
        s.fill(x0 + 1, y, z0 + 1, x1 - 1, y, z1 - 1, plancher)
        s.set(x0 + 1, y, z0 + 1, "minecraft:air")
    for y in range(y0 + 1, y0 + h):
        s.set(x0 + 1, y, z0 + 1, "minecraft:ladder[facing=south]")
    c = w // 2
    for y in range(y0 + 3, y0 + h - 1, etage):
        for (x, z) in ((x0 + c, z0), (x0 + c, z1), (x0, z0 + c), (x1, z0 + c)):
            s.set(x, y, z, fenetre); s.set(x, y + 1, z, fenetre)
    s.roof_gable(x0, z0, x1, z1, y0 + h + 1, toit_esc, toit_plein, axis="x")
    return y0 + h


def fenetre_arc(s, x, y, z, axe, haut=3, verre="minecraft:glass_pane", esc="minecraft:stone_brick_stairs"):
    """Fenêtre de 2 de large avec arc en escaliers renversés. axe='x' : mur orienté nord/sud."""
    if axe == "x":
        for dx in (0, 1):
            for dy in range(haut):
                s.set(x + dx, y + dy, z, verre)
        s.set(x, y + haut, z, f"{esc}[facing=east,half=top]")
        s.set(x + 1, y + haut, z, f"{esc}[facing=west,half=top]")
    else:
        for dz in (0, 1):
            for dy in range(haut):
                s.set(x, y + dy, z + dz, verre)
        s.set(x, y + haut, z, f"{esc}[facing=south,half=top]")
        s.set(x, y + haut, z + 1, f"{esc}[facing=north,half=top]")


def lustre(s, x, y_plafond, z, long=2, lumiere="minecraft:lantern[hanging=true]"):
    for i in range(1, long + 1):
        s.set(x, y_plafond - i, z, "minecraft:iron_chain")
    s.set(x, y_plafond - long - 1, z, lumiere)


def table(s, x0, z0, x1, z1, y, plateau="minecraft:dark_oak_slab[type=top]", chaise="minecraft:dark_oak_stairs",
          nappe=None):
    """Longue table (le long de x) avec chaises de chaque côté."""
    for x in range(x0, x1 + 1):
        for z in range(z0, z1 + 1):
            s.set(x, y, z, plateau)
        if (x - x0) % 2 == 0:
            s.set(x, y, z0 - 1, f"{chaise}[facing=south]")
            s.set(x, y, z1 + 1, f"{chaise}[facing=north]")
    s.set(x0 - 1, y, (z0 + z1) // 2, f"{chaise}[facing=east]")


def tapis(s, x0, z0, x1, z1, y, couleur):
    s.fill(x0, y, z0, x1, y, z1, f"minecraft:{couleur}_carpet")


def banniere_murale(s, x, y, z, couleur, facing):
    s.set(x, y, z, f"minecraft:{couleur}_wall_banner[facing={facing}]")


def cheminee(s, x, y, z, facing, brique="minecraft:bricks", haut=6):
    """Âtre de 3 de large adossé au mur ; facing = direction vers la pièce."""
    dx, dz = DV[facing]
    px, pz = (1, 0) if facing in ("north", "south") else (0, 1)
    for i in (-1, 0, 1):
        for yy in range(y, y + haut):
            s.set(x + px * i, yy, z + pz * i, brique)
    s.set(x, y, z, "minecraft:campfire[lit=true]")
    s.set(x, y + 1, z, "minecraft:air")
    s.set(x + px, y, z + pz, brique); s.set(x - px, y, z - pz, brique)


def bibliotheque(s, x0, y0, z0, x1, y1, z1):
    s.fill(x0, y0, z0, x1, y1, z1, ["minecraft:bookshelf", "minecraft:bookshelf", "minecraft:chiseled_bookshelf"])


def jardiniere(s, x, y, z, fleur):
    s.set(x, y, z, "minecraft:potted_" + fleur)


def statue_guerrier(s, x, y, z, corps, tete, arme, socle):
    """Statue de 7 de haut : socle, jambes, torse, bras, tête, arme levée."""
    s.fill(x - 1, y, z - 1, x + 1, y + 1, z + 1, socle)
    s.set(x - 1, y + 2, z, corps); s.set(x + 1, y + 2, z, corps)
    s.set(x - 1, y + 3, z, corps); s.set(x + 1, y + 3, z, corps)
    s.fill(x - 1, y + 4, z, x + 1, y + 6, z, corps)
    s.set(x - 2, y + 5, z, corps); s.set(x + 2, y + 5, z, corps)
    s.set(x - 2, y + 6, z, corps); s.set(x + 2, y + 6, z, corps)
    s.set(x, y + 7, z, tete)
    s.fill(x + 2, y + 7, z, x + 2, y + 10, z, arme)


def comete(s, x, y, z, plan="x", tete="minecraft:gold_block", queue="minecraft:gold_block"):
    """Comète à deux queues de Aurion, dessinée sur un mur vertical (plan x : mur nord/sud ; plan z : mur est/ouest)."""
    pts_tete = [(0, 0), (1, 0), (0, 1), (1, 1)]
    q1 = [(-1, -1), (-2, -2), (-3, -3), (-4, -4), (-5, -5)]
    q2 = [(1, -2), (1, -3), (0, -4), (0, -5), (-1, -6)]
    for (a, b), bl in [(p, tete) for p in pts_tete] + [(p, queue) for p in q1 + q2]:
        if plan == "x":
            s.set(x + a, y + b, z, bl)
        else:
            s.set(x, y + b, z + a, bl)


def etoile8(s, cx, y, cz, r, bloc, centre=None, pointe=None):
    for (dx, dz) in ((1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, -1), (1, -1), (-1, 1)):
        for k in range(1, r + 1):
            s.set(cx + dx * k, y, cz + dz * k, bloc)
        if pointe:
            s.set(cx + dx * r, y + 1, cz + dz * r, pointe)
    if centre:
        s.set(cx, y, cz, centre)


def crane_geant(s, cx, y, cz, bloc="minecraft:bone_block", oeil="minecraft:soul_lantern", face="south"):
    """Crâne de 5×5×5 tourné vers `face`."""
    s.fill(cx - 2, y, cz - 2, cx + 2, y + 4, cz + 2, bloc)
    s.fill(cx - 2, y, cz - 2, cx + 2, y, cz + 2, "minecraft:air")
    dz = 2 if face == "south" else -2
    s.set(cx - 1, y + 3, cz + dz, oeil); s.set(cx + 1, y + 3, cz + dz, oeil)
    s.set(cx, y + 2, cz + dz, "minecraft:air")
    for x in (cx - 2, cx - 1, cx, cx + 1, cx + 2):
        s.set(x, y, cz + dz, bloc if (x - cx) % 2 == 0 else "minecraft:air")
