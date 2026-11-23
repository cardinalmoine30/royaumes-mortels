# -*- coding: utf-8 -*-
"""Petit moteur pour générer des fichiers de structure .nbt (format 26.3, DataVersion 5023)."""
import json, math, random
import nbtlib
from nbtlib import Compound, List, Int, String, Double, Byte, Float

DATA_VERSION = 5023
BLOCKS = json.load(open("/tmp/mc-sum/blocks/data.json"))


def parse_state(s):
    """'minecraft:oak_stairs[facing=east,half=top]' -> (id, {props})"""
    if "[" in s:
        bid, props = s[:-1].split("[", 1)
        p = dict(kv.split("=") for kv in props.split(",") if kv)
    else:
        bid, p = s, {}
    if ":" not in bid:
        bid = "minecraft:" + bid
    short = bid.split(":", 1)[1]
    if short not in BLOCKS:
        raise ValueError(f"Bloc inconnu : {bid}")
    valid, defaults = BLOCKS[short]
    for k, v in p.items():
        if k not in valid or v not in valid[k]:
            raise ValueError(f"Propriété invalide {k}={v} pour {bid} (valide: {valid.get(k)})")
    full = dict(defaults)
    full.update(p)
    return bid, full


# Profils du datapack -> mobs du mod (v5 : plus de mobs vanilla dans les structures)
MOB_DU_MOD = {
    "sc_liberator": "liberator", "sc_judicator": "judicator", "sc_lord": "lord_celestant", "cites_garde": "heaumefer",
    "cites_arbaletrier": "fusilier", "fyreslayer": "vulkite", "kharadron": "arkanaute", "khaine_aelf": "melusai",
    "idoneth": "namarti_thrall", "lumineth": "sentinelle_vanari", "lumineth_garde": "garde_vanari", "saurus": "saurus",
    "skink": "skink", "dryade": "dryade", "chaos_guerrier": "guerrier_chaos", "chaos_seigneur": "chosen",
    "bloodreaver": "bloodreaver", "tzaangor": "tzaangor", "demonette": "demonette", "pestigor": "plaguebearer",
    "clanrat": "clanrat", "jezzail": "jezzail", "hashut": "hashut", "hashut_tireur": "hashut", "chainrasp": "chainrasp",
    "glaivewraith": "grimghast", "deathrattle": "deathrattle", "mort_sylvanie": "grave_guard", "vampire": "vampire",
    "mortek": "mortek", "goule": "goule", "brute": "brute", "megaboss": "megaboss", "gutrippa": "gutrippa",
    "kb_archer": "gutrippa", "grot": "stabba", "arachnarok": "squig_mangler", "gutbuster": "glutton",
    "ogor_chasseur": "leadbelcher", "gargant": "mancrusher",
    "boss_nagash": "nagash", "boss_archaon": "archaon", "boss_gordrakk": "gordrakk", "boss_skarbrand": "skarbrand",
    "boss_thanquol": "thanquol", "boss_rotigus": "rotigus",
}


class Struct:
    def __init__(self, sx, sy, sz, seed=0):
        self.size = (sx, sy, sz)
        self.blocks = {}      # (x,y,z) -> (state_str, nbt)
        self.entities = []
        self.rng = random.Random(seed)

    # ---------------------------------------------------------------- primitives
    def inb(self, x, y, z):
        return 0 <= x < self.size[0] and 0 <= y < self.size[1] and 0 <= z < self.size[2]

    def set(self, x, y, z, st, nbt=None):
        if self.inb(x, y, z):
            self.blocks[(x, y, z)] = (st, nbt)

    def get(self, x, y, z):
        b = self.blocks.get((x, y, z))
        return b[0] if b else None

    def fill(self, x0, y0, z0, x1, y1, z1, st, only_empty=False):
        for x in range(min(x0, x1), max(x0, x1) + 1):
            for y in range(min(y0, y1), max(y0, y1) + 1):
                for z in range(min(z0, z1), max(z0, z1) + 1):
                    if only_empty and (x, y, z) in self.blocks:
                        continue
                    self.set(x, y, z, self._pick(st))

    def _pick(self, st):
        if isinstance(st, (list, tuple)):
            return self.rng.choice(st)
        return st

    def hollow(self, x0, y0, z0, x1, y1, z1, wall, inside="minecraft:air", floor=None, roof=None):
        self.fill(x0, y0, z0, x1, y1, z1, wall)
        self.fill(x0 + 1, y0 + 1, z0 + 1, x1 - 1, y1 - 1, z1 - 1, inside)
        if floor:
            self.fill(x0, y0, z0, x1, y0, z1, floor)
        if roof:
            self.fill(x0, y1, z0, x1, y1, z1, roof)

    def walls(self, x0, y0, z0, x1, y1, z1, st):
        for y in range(y0, y1 + 1):
            for x in range(x0, x1 + 1):
                self.set(x, y, z0, self._pick(st)); self.set(x, y, z1, self._pick(st))
            for z in range(z0, z1 + 1):
                self.set(x0, y, z, self._pick(st)); self.set(x1, y, z, self._pick(st))

    def crenel(self, x0, y, z0, x1, z1, st):
        for x in range(x0, x1 + 1):
            if (x - x0) % 2 == 0:
                self.set(x, y, z0, st); self.set(x, y, z1, st)
        for z in range(z0, z1 + 1):
            if (z - z0) % 2 == 0:
                self.set(x0, y, z, st); self.set(x1, y, z, st)

    def cylinder(self, cx, cz, r, y0, y1, st, hollow=True, inside="minecraft:air"):
        for x in range(cx - r, cx + r + 1):
            for z in range(cz - r, cz + r + 1):
                d = math.hypot(x - cx, z - cz)
                if d <= r + 0.3:
                    for y in range(y0, y1 + 1):
                        if hollow and d < r - 0.7:
                            if inside:
                                self.set(x, y, z, inside)
                        else:
                            self.set(x, y, z, self._pick(st))

    def disk(self, cx, cz, r, y, st):
        for x in range(cx - r, cx + r + 1):
            for z in range(cz - r, cz + r + 1):
                if math.hypot(x - cx, z - cz) <= r + 0.3:
                    self.set(x, y, z, self._pick(st))

    def cone(self, cx, cz, r, y0, st):
        y = y0
        while r >= 0:
            self.cylinder(cx, cz, r, y, y, st, hollow=False)
            r -= 1; y += 1
        return y

    def pyramid(self, x0, z0, x1, z1, y0, st, step=1, hollow_inside=False):
        y = y0
        while x0 <= x1 and z0 <= z1:
            self.fill(x0, y, z0, x1, y, z1, st)
            x0 += step; z0 += step; x1 -= step; z1 -= step; y += 1
        return y

    def foundation(self, x0, z0, x1, z1, y_top, depth, st):
        """Remplit sous le sol pour combler les pentes."""
        self.fill(x0, max(0, y_top - depth), z0, x1, y_top, z1, st)

    def clear(self, x0, y0, z0, x1, y1, z1):
        self.fill(x0, y0, z0, x1, y1, z1, "minecraft:air")

    def roof_gable(self, x0, z0, x1, z1, y, mat_stairs, mat_full, axis="x"):
        """Toit à deux pans le long de l'axe donné."""
        if axis == "x":
            w = z1 - z0
            for i in range((w + 2) // 2):
                za, zb = z0 - 1 + i, z1 + 1 - i
                yy = y + i
                for x in range(x0 - 1, x1 + 2):
                    if za < zb:
                        self.set(x, yy, za, f"{mat_stairs}[facing=south]")
                        self.set(x, yy, zb, f"{mat_stairs}[facing=north]")
                    else:
                        self.set(x, yy, za, mat_full)
                # pignons
                for z in range(za + 1, zb):
                    self.set(x0, yy, z, mat_full); self.set(x1, yy, z, mat_full)
        else:
            w = x1 - x0
            for i in range((w + 2) // 2):
                xa, xb = x0 - 1 + i, x1 + 1 - i
                yy = y + i
                for z in range(z0 - 1, z1 + 2):
                    if xa < xb:
                        self.set(xa, yy, z, f"{mat_stairs}[facing=east]")
                        self.set(xb, yy, z, f"{mat_stairs}[facing=west]")
                    else:
                        self.set(xa, yy, z, mat_full)
                for x in range(xa + 1, xb):
                    self.set(x, yy, z0, mat_full); self.set(x, yy, z1, mat_full)

    def door(self, x, y, z, st="minecraft:oak_door", facing="south"):
        self.set(x, y, z, f"{st}[facing={facing},half=lower]")
        self.set(x, y + 1, z, f"{st}[facing={facing},half=upper]")

    def chest(self, x, y, z, loot, facing="north"):
        self.set(x, y, z, f"minecraft:chest[facing={facing}]",
                 {"id": "minecraft:chest", "LootTable": loot, "Items": []})

    def barrel(self, x, y, z, loot):
        self.set(x, y, z, "minecraft:barrel[facing=up]", {"id": "minecraft:barrel", "LootTable": loot, "Items": []})

    def mob(self, x, y, z, base, profil, n=1):
        for i in range(n):
            ox = x + 0.5 + (i % 3) * 0.3
            oz = z + 0.5 + (i // 3) * 0.3
            mod = MOB_DU_MOD.get(profil)
            if mod:
                nbt = {"id": f"royaumes:{mod}", "PersistenceRequired": True}
            else:
                nbt = {"id": f"minecraft:{base}", "Tags": ["rm_spawn", f"rm_p_{profil}"], "PersistenceRequired": True}
            self.entities.append(((ox, y, oz), (x, y, z), nbt))

    def banner_pole(self, x, y, z, h, banner_color, pole="minecraft:oak_fence"):
        for i in range(h):
            self.set(x, y + i, z, pole)
        self.set(x, y + h, z, f"minecraft:{banner_color}_banner[rotation=0]")

    # ---------------------------------------------------------------- export
    def connecter(self):
        """Calcule les connexions des barrières, vitres, barreaux et murets."""
        NON = ("air", "carpet", "torch", "lantern", "flower", "sapling", "banner", "candle", "mushroom", "tulip",
               "orchid", "allium", "valley", "fern", "rail", "skull", "head", "button", "pressure", "chain", "ladder",
               "campfire", "rod", "pickle", "cluster", "bell", "vine", "grass", "bush", "door", "bed", "wheat",
               "carrots", "potatoes", "water", "lava", "fire", "slab", "stairs", "end_rod", "potted")
        DIRS = {"north": (0, -1), "south": (0, 1), "west": (-1, 0), "east": (1, 0)}
        for (x, y, z), (st, nbt) in list(self.blocks.items()):
            bid = st.split("[")[0]
            short = bid.split(":")[-1]
            fam = None
            if short.endswith("_fence") or short.endswith("_pane") or short == "iron_bars" or short == "glass_pane":
                fam = "fence"
            elif short.endswith("_wall") and "banner" not in short and "sign" not in short and "torch" not in short \
                    and "head" not in short and "skull" not in short:
                fam = "wall"
            if not fam:
                continue
            props = {}
            if "[" in st:
                props = dict(kv.split("=") for kv in st[:-1].split("[", 1)[1].split(","))
            con = {}
            for d, (dx, dz) in DIRS.items():
                n_ = self.blocks.get((x + dx, y, z + dz))
                ok = False
                if n_:
                    ns = n_[0].split("[")[0].split(":")[-1]
                    ok = not any(k in ns for k in NON) or ns == short
                    if ns.endswith("_fence") or ns.endswith("_pane") or ns == "iron_bars" or ns.endswith("_wall"):
                        ok = True
                con[d] = ok
            if fam == "fence":
                for d, ok in con.items():
                    props[d] = "true" if ok else "false"
            else:
                for d, ok in con.items():
                    props[d] = "low" if ok else "none"
                droit = (con["north"] and con["south"] and not con["east"] and not con["west"]) or \
                        (con["east"] and con["west"] and not con["north"] and not con["south"])
                au_dessus = self.blocks.get((x, y + 1, z))
                props["up"] = "false" if droit and not au_dessus else "true"
            self.blocks[(x, y, z)] = (bid + "[" + ",".join(f"{k}={v}" for k, v in props.items()) + "]", nbt)

    def save(self, path):
        self.connecter()
        palette, idx = [], {}
        blocks = []
        for (x, y, z), (st, nbt) in sorted(self.blocks.items(), key=lambda kv: (kv[0][1], kv[0][2], kv[0][0])):
            bid, props = parse_state(st)
            key = (bid, tuple(sorted(props.items())))
            if key not in idx:
                idx[key] = len(palette)
                c = Compound({"id": String(bid)})
                if props:
                    c["properties"] = Compound({k: String(v) for k, v in props.items()})
                palette.append(c)
            b = Compound({"pos": List[Int]([Int(x), Int(y), Int(z)]), "state": Int(idx[key])})
            if nbt:
                b["nbt"] = to_nbt(nbt)
            blocks.append(b)
        ents = []
        for (px, py, pz), (bx, by, bz), nbt in self.entities:
            n = dict(nbt)
            n["Pos"] = [float(px), float(py), float(pz)]
            ents.append(Compound({
                "pos": List[Double]([Double(px), Double(py), Double(pz)]),
                "blockPos": List[Int]([Int(bx), Int(by), Int(bz)]),
                "nbt": to_nbt(n)}))
        root = Compound({
            "size": List[Int]([Int(s) for s in self.size]),
            "entities": List[Compound](ents),
            "blocks": List[Compound](blocks),
            "palette": List[Compound](palette),
            "DataVersion": Int(DATA_VERSION),
        })
        nbtlib.File(root).save(path, gzipped=True)
        return len(blocks), len(ents)


def to_nbt(v):
    if isinstance(v, bool):
        return Byte(1 if v else 0)
    if isinstance(v, int):
        return Int(v)
    if isinstance(v, float):
        return Double(v)
    if isinstance(v, str):
        return String(v)
    if isinstance(v, dict):
        return Compound({k: to_nbt(x) for k, x in v.items()})
    if isinstance(v, list):
        if not v:
            return List([])
        items = [to_nbt(x) for x in v]
        return List[type(items[0])](items)
    raise TypeError(v)
