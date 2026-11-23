# -*- coding: utf-8 -*-
"""Validation hors-jeu du datapack contre les données vanilla 26.3."""
import json, os, re, glob, sys
import nbtlib

OUT = "/home/claude/aos/out/RoyaumesMortels"
REG = "/tmp/mc-reg"
VAN = "/tmp/mc-data/data/minecraft"
NS = "royaumes"
err = []


def reg(name):
    return set(json.load(open(f"{REG}/{name}/data.min.json")))


ITEMS, BLOCKS, ENTS, EFFECTS = reg("item"), reg("block"), reg("entity_type"), reg("mob_effect")
ATTRS, COMPS, PARTS, SOUNDS = reg("attribute"), reg("data_component_type"), reg("particle_type"), reg("sound_event")
TRIM_M = {os.path.basename(p)[:-5] for p in glob.glob(f"{VAN}/trim_material/*.json")}
TRIM_P = {os.path.basename(p)[:-5] for p in glob.glob(f"{VAN}/trim_pattern/*.json")}
V_ENCH = {os.path.basename(p)[:-5] for p in glob.glob(f"{VAN}/enchantment/*.json")}
M_ENCH = {os.path.basename(p)[:-5] for p in glob.glob(f"{OUT}/data/{NS}/enchantment/*.json")}
V_PF = {os.path.relpath(p, f"{VAN}/worldgen/placed_feature")[:-5] for p in glob.glob(f"{VAN}/worldgen/placed_feature/**/*.json", recursive=True)}
M_PF = {os.path.basename(p)[:-5] for p in glob.glob(f"{OUT}/data/{NS}/worldgen/placed_feature/*.json")}
V_CARV = {os.path.basename(p)[:-5] for p in glob.glob(f"{VAN}/worldgen/carver/*.json")}
V_TAGS_ITEM = {os.path.relpath(p, f"{VAN}/tags/item")[:-5] for p in glob.glob(f"{VAN}/tags/item/**/*.json", recursive=True)}
V_TAGS_BLOCK = {os.path.relpath(p, f"{VAN}/tags/block")[:-5] for p in glob.glob(f"{VAN}/tags/block/**/*.json", recursive=True)}
V_BIOMES = {os.path.basename(p)[:-5] for p in glob.glob(f"{VAN}/worldgen/biome/*.json")}
M_BIOMES = {os.path.basename(p)[:-5] for p in glob.glob(f"{OUT}/data/{NS}/worldgen/biome/*.json")}
DIALOGS = {os.path.relpath(p, f"{OUT}/data/{NS}/dialog")[:-5] for p in glob.glob(f"{OUT}/data/{NS}/dialog/**/*.json", recursive=True)}
LOOTS = {os.path.relpath(p, f"{OUT}/data/{NS}/loot_table")[:-5] for p in glob.glob(f"{OUT}/data/{NS}/loot_table/**/*.json", recursive=True)}
FUNCS = {os.path.relpath(p, f"{OUT}/data/{NS}/function")[:-11] for p in glob.glob(f"{OUT}/data/{NS}/function/**/*.mcfunction", recursive=True)}
STRUCTS = {os.path.basename(p)[:-4] for p in glob.glob(f"{OUT}/data/{NS}/structure/*.nbt")}


def short(i):
    return i.split(":", 1)[1] if ":" in i else i


def check_item(i, where):
    if short(i) not in ITEMS:
        err.append(f"{where}: objet inconnu {i}")


def check_components(c, where):
    for k, v in c.items():
        if short(k) not in COMPS:
            err.append(f"{where}: composant inconnu {k}")
        if k == "minecraft:enchantments":
            for e in v:
                ns, n = e.split(":")
                if (ns == "minecraft" and n not in V_ENCH) or (ns == NS and n not in M_ENCH):
                    err.append(f"{where}: enchantement inconnu {e}")
        if k == "minecraft:trim":
            if short(v["material"]) not in TRIM_M or short(v["pattern"]) not in TRIM_P:
                err.append(f"{where}: garniture inconnue {v}")
        if k == "minecraft:item_model" and short(v) not in ITEMS:
            err.append(f"{where}: modèle inconnu {v}")


def walk(o, cb, path=""):
    cb(o, path)
    if isinstance(o, dict):
        for k, v in o.items():
            walk(v, cb, path + "/" + k)
    elif isinstance(o, list):
        for i, v in enumerate(o):
            walk(v, cb, path + f"[{i}]")


# ---------------------------------------------------------------- JSON
for p in glob.glob(f"{OUT}/**/*.json", recursive=True) + [f"{OUT}/pack.mcmeta"]:
    rel = os.path.relpath(p, OUT)
    try:
        d = json.load(open(p, encoding="utf-8"))
    except Exception as e:
        err.append(f"{rel}: JSON invalide {e}"); continue

    def cb(o, path):
        if isinstance(o, dict):
            if o.get("type") == "minecraft:item" and "name" in o:
                check_item(o["name"], rel)
            if o.get("type") == "minecraft:set_components":
                check_components(o["components"], rel)
            if "state" in o and isinstance(o["state"], str) and short(o["state"].split("[")[0]) not in BLOCKS:
                err.append(f"{rel}: bloc inconnu {o['state']}")
            if "result_state" in o and short(o["result_state"]) not in BLOCKS:
                err.append(f"{rel}: bloc inconnu {o['result_state']}")
            if "block" in o and isinstance(o["block"], str) and short(o["block"]) not in BLOCKS:
                err.append(f"{rel}: bloc inconnu {o['block']}")
            if o.get("predicate_type") == "minecraft:tag_match" and short(o["tag"]) not in V_TAGS_BLOCK:
                err.append(f"{rel}: tag de bloc inconnu {o['tag']}")
            if "to_apply" in o and short(o["to_apply"]) not in EFFECTS:
                err.append(f"{rel}: effet inconnu {o['to_apply']}")
            if "sound" in o and isinstance(o["sound"], str) and short(o["sound"]) not in SOUNDS:
                err.append(f"{rel}: son inconnu {o['sound']}")
            if "particle" in o and isinstance(o["particle"], dict) and short(o["particle"]["type"]) not in PARTS:
                err.append(f"{rel}: particule inconnue {o['particle']}")
            if o.get("type") == "show_dialog":
                ns, n = o["dialog"].split(":")
                if n not in DIALOGS:
                    err.append(f"{rel}: dialogue inconnu {o['dialog']}")
            if o.get("type", "").startswith("minecraft:") and "count" in o and "weight" in o and "name" not in o:
                if short(o["type"]) not in ENTS:
                    err.append(f"{rel}: entité inconnue {o['type']}")
    walk(d, cb)
    if rel.endswith("recipe/pierre_de_royaume.json"):
        for v in d["key"].values():
            check_item(v, rel)
        check_item(d["result"]["id"], rel); check_components(d["result"]["components"], rel)
    if "/worldgen/biome/" in rel and "/tags/" not in rel:
        for step in d["features"]:
            for f in step:
                ns, n = f.split(":")
                if (ns == "minecraft" and n not in V_PF) or (ns == NS and n not in M_PF):
                    err.append(f"{rel}: feature inconnue {f}")
        for c in d["carvers"]:
            if short(c) not in V_CARV:
                err.append(f"{rel}: carver inconnu {c}")
        for cat, lst in d["attributes"]["minecraft:gameplay/natural_mob_spawns"]["argument"]["spawns_by_category"].items():
            for s in lst:
                if short(s["type"]) not in ENTS:
                    err.append(f"{rel}: entité inconnue {s['type']}")
    if "/tags/worldgen/biome/" in rel:
        for v in d["values"]:
            ns, n = v.split(":")
            if (ns == "minecraft" and n not in V_BIOMES) or (ns == NS and n not in M_BIOMES):
                err.append(f"{rel}: biome inconnu {v}")
    if "/tags/item/" in rel:
        for v in d["values"]:
            if v.startswith("#"):
                if short(v[1:]) not in V_TAGS_ITEM:
                    err.append(f"{rel}: tag inconnu {v}")
            else:
                check_item(v, rel)
    if "/tags/entity_type/" in rel:
        for v in d["values"]:
            if short(v) not in ENTS:
                err.append(f"{rel}: entité inconnue {v}")

# ---------------------------------------------------------------- Ordre des features (cycles)
import itertools
biomes = [json.load(open(p)) for p in glob.glob(f"{OUT}/data/{NS}/worldgen/biome/*.json")]
for step in range(11):
    edges = {}
    for b in biomes:
        lst = b["features"][step] if step < len(b["features"]) else []
        for a, c in zip(lst, lst[1:]):
            edges.setdefault(a, set()).add(c)
    # détection de cycle (DFS)
    state = {}
    def dfs(n, stack):
        state[n] = 1
        for m in edges.get(n, ()):
            if state.get(m) == 1:
                err.append(f"Cycle d'ordre des features à l'étape {step}: {m} <- {n}")
            elif not state.get(m):
                dfs(m, stack)
        state[n] = 2
    for n in list(edges):
        if not state.get(n):
            dfs(n, [])
# Une même feature ne doit pas apparaître à deux étapes différentes
seen = {}
for b in biomes:
    for st, lst in enumerate(b["features"]):
        for f in lst:
            if seen.setdefault(f, st) != st:
                err.append(f"Feature {f} à des étapes différentes")

# ---------------------------------------------------------------- Fonctions (analyse sur l'arbre des commandes)
CMD = json.load(open("/tmp/mc-sum/commands/data.json"))


def tokenize(line):
    toks, i, n = [], 0, len(line)
    while i < n:
        if line[i] == " ":
            i += 1; continue
        j, depth, q = i, 0, None
        while j < n:
            ch = line[j]
            if q:
                if ch == "\\":
                    j += 2; continue
                if ch == q:
                    q = None
            elif ch in "\"'":
                q = ch
            elif ch in "{[(":
                depth += 1
            elif ch in "}])":
                depth -= 1
            elif ch == " " and depth == 0:
                break
            j += 1
        toks.append(line[i:j]); i = j
    return toks


def node_at(path):
    n = CMD
    for p in path:
        n = n["children"][p]
    return n


GREEDY = {"minecraft:message", "brigadier:string"}


def parse(tokens, node, where):
    i = 0
    while i < len(tokens):
        if "redirect" in node and not node.get("children"):
            node = node_at(node["redirect"])
        ch = node.get("children", {})
        t = tokens[i]
        if t in ch and ch[t]["type"] == "literal":
            node = ch[t]; i += 1
            if t == "run" and not node.get("children") and "redirect" not in node:
                node = CMD
            continue
        args = [(k, v) for k, v in ch.items() if v["type"] == "argument"]
        if not args:
            if "redirect" in node:
                node = node_at(node["redirect"]); continue
            err.append(f"{where}: jeton inattendu « {t} » (attendu {list(ch)[:8]})"); return
        k, v = args[0]
        if t.startswith("@") and len(args) > 1:
            for kk, vv in args:
                if vv.get("parser") == "minecraft:entity" and (vv.get("children") or i == len(tokens) - 1):
                    k, v = kk, vv
                    break
        if t[:1] in "~^-0123456789" and len(args) > 1 and v.get("parser") == "minecraft:entity":
            for kk, vv in args:
                if vv.get("parser") in ("minecraft:vec3", "minecraft:block_pos"):
                    k, v = kk, vv
                    break
        parser = v.get("parser")
        if parser in ("minecraft:vec3", "minecraft:block_pos", "minecraft:vec2", "minecraft:column_pos", "minecraft:rotation"):
            dims = 2 if parser in ("minecraft:vec2", "minecraft:column_pos", "minecraft:rotation") else 3
            i += dims
        elif parser == "brigadier:string" and v.get("properties", {}).get("type") == "greedy":
            return
        elif parser == "minecraft:message":
            return
        elif parser == "minecraft:int_range" or parser == "minecraft:float_range":
            i += 1
        else:
            i += 1
        node = v
    if not node.get("executable") and not ("redirect" in node):
        err.append(f"{where}: commande incomplète")


for p in glob.glob(f"{OUT}/data/{NS}/function/**/*.mcfunction", recursive=True):
    rel = os.path.relpath(p, OUT)
    for ln, line in enumerate(open(p, encoding="utf-8"), 1):
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("$"):
            line = re.sub(r"\$\(\w+\)", "1", line[1:])
        toks = tokenize(line)
        if toks[0] not in CMD["children"]:
            err.append(f"{rel}:{ln}: commande inconnue {toks[0]}"); continue
        parse(toks[1:], CMD["children"][toks[0]], f"{rel}:{ln}")
        # Références
        for m in re.finditer(r"function (royaumes:[\w/]+)", line):
            if short(m.group(1)) not in FUNCS:
                err.append(f"{rel}:{ln}: fonction inconnue {m.group(1)}")
        for m in re.finditer(r'DeathLootTable set value "(royaumes:[\w/]+)"', line):
            if short(m.group(1)) not in LOOTS:
                err.append(f"{rel}:{ln}: loot de mort inconnu {m.group(1)}")
        for m in re.finditer(r"loot (royaumes:[\w/]+)", line):
            if short(m.group(1)) not in LOOTS:
                err.append(f"{rel}:{ln}: loot inconnu {m.group(1)}")
        for m in re.finditer(r"dialog show \S+ (royaumes:[\w/]+)", line):
            if short(m.group(1)) not in DIALOGS:
                err.append(f"{rel}:{ln}: dialogue inconnu {m.group(1)}")
        for m in re.finditer(r"attribute @s minecraft:(\w+)", line):
            if m.group(1) not in ATTRS:
                err.append(f"{rel}:{ln}: attribut inconnu {m.group(1)}")
        for m in re.finditer(r"effect give \S+ minecraft:(\w+)", line):
            if m.group(1) not in EFFECTS:
                err.append(f"{rel}:{ln}: effet inconnu {m.group(1)}")
        for m in re.finditer(r"(?:particle|playsound) minecraft:([\w.]+)", line):
            if m.group(1) not in PARTS and m.group(1) not in SOUNDS:
                err.append(f"{rel}:{ln}: particule/son inconnu {m.group(1)}")
        for m in re.finditer(r"if biome ~ ~ ~ royaumes:(\w+)", line):
            if m.group(1) not in M_BIOMES:
                err.append(f"{rel}:{ln}: biome inconnu {m.group(1)}")
        for m in re.finditer(r"type=minecraft:(\w+)", line):
            if m.group(1) not in ENTS:
                err.append(f"{rel}:{ln}: entité inconnue {m.group(1)}")

# ---------------------------------------------------------------- Structures NBT
for p in glob.glob(f"{OUT}/data/{NS}/structure/*.nbt"):
    f = nbtlib.load(p)
    sx, sy, sz = [int(v) for v in f["size"]]
    for b in f["blocks"]:
        x, y, z = [int(v) for v in b["pos"]]
        if not (0 <= x < sx and 0 <= y < sy and 0 <= z < sz):
            err.append(f"{p}: bloc hors limites")
            break
        if "nbt" in b and "LootTable" in b["nbt"]:
            lt = str(b["nbt"]["LootTable"]).split(":")[1]
            if lt not in LOOTS:
                err.append(f"{p}: loot inconnu {lt}")
    for e in f["entities"]:
        if short(str(e["nbt"]["id"])) not in ENTS:
            err.append(f"{p}: entité inconnue {e['nbt']['id']}")

# Template pools -> structures
for p in glob.glob(f"{OUT}/data/{NS}/worldgen/template_pool/**/*.json", recursive=True):
    d = json.load(open(p))
    for el in d["elements"]:
        if short(el["element"]["location"]) not in STRUCTS:
            err.append(f"{p}: gabarit absent {el['element']['location']}")

print("\n".join(err) if err else "Aucune erreur détectée.")
print(f"{len(err)} erreur(s)")
