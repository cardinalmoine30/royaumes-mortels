# -*- coding: utf-8 -*-
"""Échantillons de biomes : terrain synthétique + végétation + décors du datapack, rendus avec les vraies textures."""
import math, random, sys
import rendu
from rendu import rendre_blocs
import data_v4  # noqa  (ajoute les nouveaux biomes et décors)
from data_monde import BIOMES
import decors
from data_v4 import FLOTTANTS

N = 72
EAU = 7


def hexa(c):
    c = c.lstrip("#")
    return tuple(int(c[i:i + 2], 16) for i in (0, 2, 4))


def bruit(seed):
    rng = random.Random(seed)
    ph = [(rng.uniform(0, 6.3), rng.uniform(0.05, 0.16), rng.uniform(0.05, 0.16)) for _ in range(5)]
    def f(x, z):
        return sum(math.sin(x * a + p) * math.cos(z * b - p * 0.7) for p, a, b in ph) / 2.5
    return f


def arbre(B, x, y, z, genre, rng):
    def s(dx, dy, dz, b):
        B[(x + dx, y + dy, z + dz)] = b
    def boule(cy, r, feuille):
        for dx in range(-r, r + 1):
            for dz in range(-r, r + 1):
                for dy in range(-r + 1, r):
                    if dx * dx + dz * dz + dy * dy * 1.6 <= r * r + 0.5 and rng.random() < 0.92:
                        k = (x + dx, y + cy + dy, z + dz)
                        if k not in B:
                            B[k] = feuille
    if genre in ("oak", "birch"):
        h = rng.randint(4, 6)
        for i in range(h):
            s(0, i, 0, f"minecraft:{genre}_log")
        boule(h, 3, f"minecraft:{genre}_leaves[persistent=true]")
    elif genre == "dark_oak":
        h = rng.randint(6, 8)
        for i in range(h):
            for dx in (0, 1):
                for dz in (0, 1):
                    s(dx, i, dz, "minecraft:dark_oak_log")
        boule(h, 4, "minecraft:dark_oak_leaves[persistent=true]")
    elif genre == "jungle":
        h = rng.randint(9, 13)
        for i in range(h):
            s(0, i, 0, "minecraft:jungle_log")
            if i > 3 and rng.random() < 0.4:
                s(1, i, 0, "minecraft:vine[west=true]")
        boule(h, 4, "minecraft:jungle_leaves[persistent=true]")
    elif genre == "acacia":
        h = rng.randint(4, 6)
        for i in range(h):
            s(i // 3, i, 0, "minecraft:acacia_log")
        for dx in range(-2, 4):
            for dz in range(-2, 3):
                if abs(dz) + abs(dx - 1) < 5:
                    B[(x + dx, y + h, z + dz)] = "minecraft:acacia_leaves[persistent=true]"
    elif genre == "cherry":
        h = rng.randint(5, 7)
        for i in range(h):
            s(0, i, 0, "minecraft:cherry_log")
        boule(h, 4, "minecraft:cherry_leaves[persistent=true]")
    elif genre == "pale":
        h = rng.randint(6, 8)
        for i in range(h):
            for dx in (0, 1):
                for dz in (0, 1):
                    s(dx, i, dz, "minecraft:pale_oak_log")
        boule(h, 4, "minecraft:pale_oak_leaves[persistent=true]")
        for k in range(4):
            s(rng.randint(-3, 3), h - 3, rng.randint(-3, 3), "minecraft:pale_hanging_moss")
    elif genre == "mangrove":
        h = rng.randint(6, 8)
        for (dx, dz) in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            s(dx, 0, dz, "minecraft:mangrove_roots"); s(dx, 1, dz, "minecraft:mangrove_roots")
        for i in range(2, h):
            s(0, i, 0, "minecraft:mangrove_log")
        boule(h, 3, "minecraft:mangrove_leaves[persistent=true]")
    elif genre == "mort":
        h = rng.randint(4, 7)
        for i in range(h):
            s(0, i, 0, "minecraft:dark_oak_log")
        for k in range(3):
            s(k - 1, h - 1 + k % 2, 1 - k, "minecraft:dark_oak_wood")
    elif genre == "cactus":
        for i in range(rng.randint(2, 4)):
            s(0, i, 0, "minecraft:cactus")


VEG = {  # base vanilla -> (arbres, densité arbres, sols décoratifs)
    "meadow": (["oak", "birch"], 0.004, ["minecraft:short_grass", "minecraft:cornflower", "minecraft:dandelion", "minecraft:allium"]),
    "cherry_grove": (["cherry"], 0.012, ["minecraft:short_grass", "minecraft:pink_petals[flower_amount=4]"]),
    "flower_forest": (["oak", "birch"], 0.02, ["minecraft:poppy", "minecraft:allium", "minecraft:azure_bluet", "minecraft:oxeye_daisy",
                                              "minecraft:cornflower", "minecraft:lily_of_the_valley", "minecraft:short_grass"]),
    "dark_forest": (["dark_oak", "dark_oak", "oak"], 0.03, ["minecraft:short_grass", "minecraft:fern", "minecraft:red_mushroom"]),
    "jungle": (["jungle", "jungle", "oak"], 0.035, ["minecraft:fern", "minecraft:short_grass", "minecraft:melon"]),
    "savanna": (["acacia"], 0.006, ["minecraft:short_grass", "minecraft:short_grass", "minecraft:tall_grass[half=lower]"]),
    "mangrove_swamp": (["mangrove"], 0.02, ["minecraft:short_grass", "minecraft:lily_pad"]),
    "swamp": (["oak", "mort"], 0.01, ["minecraft:short_grass", "minecraft:blue_orchid", "minecraft:brown_mushroom"]),
    "pale_garden": (["pale"], 0.02, ["minecraft:pale_moss_carpet", "minecraft:short_grass"]),
    "badlands": (["mort"], 0.002, ["minecraft:dead_bush"]),
    "desert": (["cactus"], 0.006, ["minecraft:dead_bush"]),
    "deep_ocean": ([], 0, ["minecraft:seagrass", "minecraft:kelp_plant"]),
}


def surface(b, n, rng):
    sdef = b.get("surface")
    if not sdef:
        return "minecraft:grass_block", "minecraft:dirt"
    top = sdef["top"][0][0]
    for blk, r in sdef["top"][1:]:
        if r[0] <= n <= r[1]:
            top = blk
    return top, sdef["under"]


def poser_template(B, st, cx, cz, h, G=decors.G, dy=0):
    sx, sy, sz = st.size
    for (x, y, z), (etat, _) in st.blocks.items():
        if etat == "minecraft:air":
            continue
        B[(cx - sx // 2 + x, h + (y - G) + dy, cz - sz // 2 + z)] = etat


def echantillon(b, seed=1):
    rng = random.Random(seed)
    f = bruit(seed)
    g = bruit(seed + 7)
    B = {}
    special = b.get("special")
    amp = {"pics": 22, "ocean": 3}.get(special, 6)
    if b["id"] in ("aqshy_volcans", "chaos_desolation"):
        amp = 9
    base_h = {"pics": 12, "ocean": 1}.get(special, 9)
    H = {}
    if special == "flottant":
        for (ix, iz, r, hy) in ((22, 26, 16, 26), (52, 46, 11, 34), (50, 14, 7, 20)):
            for x in range(ix - r - 2, ix + r + 3):
                for z in range(iz - r - 2, iz + r + 3):
                    d = math.hypot(x - ix, z - iz) + f(x, z) * 2
                    if d <= r and 0 <= x < N and 0 <= z < N:
                        prof = int((1 - d / r) ** 0.7 * 14) + 1
                        for y in range(hy - prof, hy):
                            B[(x, y, z)] = rng.choice(["minecraft:stone", "minecraft:calcite", "minecraft:dirt"])
                        top, _ = surface(b, g(x, z), rng)
                        B[(x, hy, z)] = top
                        H[(x, z)] = hy
    else:
        for x in range(N):
            for z in range(N):
                h = int(base_h + amp * (f(x, z) + 1) / 2 + (amp * 0.6 * max(0, f(x * 0.5, z * 0.5)) if special == "pics" else 0))
                top, under = surface(b, g(x, z), rng)
                if special == "pics" and h > base_h + amp * 0.7:
                    top = rng.choice(["minecraft:snow_block", "minecraft:stone", "minecraft:calcite"])
                for y in range(0, h - 3):
                    B[(x, y, z)] = "minecraft:stone"
                for y in range(max(0, h - 3), h):
                    B[(x, y, z)] = under
                if h <= EAU and top == "minecraft:grass_block":
                    top = "minecraft:dirt" if special != "ocean" else "minecraft:gravel"
                B[(x, h, z)] = top
                H[(x, z)] = h
                for y in range(h + 1, EAU + 1):
                    B[(x, y, z)] = "minecraft:water"
    # Végétation
    arbres, dens, sol = VEG.get(b["base"], (["oak"], 0.01, ["minecraft:short_grass"]))
    if b["id"] == "ghyran_wyldwood":
        arbres, dens = ["dark_oak", "oak"], 0.02
    if b["id"] in ("aqshy_cendres", "aqshy_volcans", "chaos_desolation"):
        arbres, dens, sol = ["mort"], 0.002, ["minecraft:fire"] if b["id"] != "chaos_desolation" else ["minecraft:crimson_roots"]
    occupe = set()
    for (x, z), h in H.items():
        top = B[(x, h, z)]
        if h < EAU and special != "flottant":
            if special == "ocean" and rng.random() < 0.08:
                B[(x, h + 1, z)] = rng.choice(sol)
            continue
        if top in ("minecraft:grass_block", "minecraft:podzol", "minecraft:moss_block", "minecraft:sand", "minecraft:mud",
                   "minecraft:coarse_dirt", "minecraft:soul_soil", "minecraft:basalt", "minecraft:netherrack", "minecraft:crimson_nylium"):
            if arbres and rng.random() < dens and 4 < x < N - 5 and 4 < z < N - 5:
                arbre(B, x, h + 1, z, rng.choice(arbres), rng)
                occupe.add((x, z))
            elif rng.random() < 0.18:
                vg = rng.choice(sol)
                if vg == "minecraft:lily_pad":
                    continue
                if (x, h + 1, z) not in B:
                    B[(x, h + 1, z)] = vg
    # Décors du datapack propres au biome
    for did, (fn_, bl, chance) in list(decors.DECOS.items()) + list(FLOTTANTS.items()):
        if b["id"] not in bl:
            continue
        st = fn_()
        nb = 2 if chance <= 6 else 1
        for _ in range(nb):
            for essai in range(30):
                x, z = rng.randint(10, N - 11), rng.randint(10, N - 11)
                if (x, z) in H and H[(x, z)] >= EAU - (3 if did in decors.OCEAN_DECOS else 0):
                    break
            h = H.get((x, z), 10)
            poser_template(B, st, x, z, h, dy=(18 if did in FLOTTANTS else 0))
    return B


def rendre_biome(b, s=5):
    rendu.TINT_FEUILLE = hexa(b["feuilles"])
    rendu.TINT_HERBE = hexa(b["herbe"])
    rendu.TINT_EAU = hexa(b["eau"])
    rendu.faces.cache_clear(); rendu._cache.clear()
    B = echantillon(b, seed=hash(b["id"]) % 1000)
    xs = [k[0] for k in B]; ys = [k[1] for k in B]; zs = [k[2] for k in B]
    mn = (min(xs), min(ys), min(zs))
    B2 = {(x - mn[0], y - mn[1], z - mn[2]): v for (x, y, z), v in B.items()}
    taille = (max(xs) - mn[0] + 1, max(ys) - mn[1] + 1, max(zs) - mn[2] + 1)
    fond = tuple(int(v * 0.35) for v in hexa(b["ciel"])) + (255,)
    return rendre_blocs(B2, taille, s, fond=fond, titre=f"{b['nom']} — {b['sous']}")


if __name__ == "__main__":
    ids = sys.argv[1:]
    for b in BIOMES:
        if ids and b["id"] not in ids:
            continue
        im = rendre_biome(b)
        im.convert("RGB").save(f"out/apercus/biome_{b['id']}.png")
        print(b["id"], im.size)
