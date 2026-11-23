# -*- coding: utf-8 -*-
"""Génère /function royaumes:debug/objets : des tonneaux avec TOUS les objets du jeu
(Pierre de Royaume, objets de forge, ressources, sceaux de boss, trophées, œufs des mobs du mod)."""
import json, os, sys
import build as B
import extension as X

MOD = sys.argv[1]
DATA = f"{MOD}/src/main/resources/data/royaumes"
X.preparer()


def table(nom, specs):
    pools = [{"rolls": 1, "entries": [B.entry(s, n=s.get("n", 1))]} for s in specs]
    p = f"{DATA}/loot_table/debug/{nom}.json"
    os.makedirs(os.path.dirname(p), exist_ok=True)
    json.dump({"pools": pools}, open(p, "w"), ensure_ascii=False, indent=1)
    return f"royaumes:debug/{nom}"


ressources = [X.res_spec(r, 16) for r in X.RES]
os.makedirs(f"{DATA}/loot_table/debug/res", exist_ok=True)
for r in X.RES:
    json.dump({"pools": [{"rolls": 1, "entries": [B.entry(X.res_spec(r, 1), n=1)]}]},
              open(f"{DATA}/loot_table/debug/res/{r}.json", "w"), ensure_ascii=False, indent=1)
for s in ressources:
    s["n"] = 16
import v6gen
divers = [B.PIERRE, X.PARCHEMIN, v6gen.CORNE] + list(X.SCEAUX.values())
trophees = [t for l in X.TROPHEES.values() for t in l]

# œufs d'apparition des mobs du mod
mobs = json.load(open(f"{DATA}/tags/entity_type/mobs_du_mod.json"))["values"]
lang = json.load(open(f"{MOD}/src/main/resources/assets/royaumes/lang/fr_fr.json"))
oeufs = []
os.makedirs(f"{DATA}/loot_table/debug", exist_ok=True)
for m in mobs:
    nom = lang.get(f"entity.royaumes.{m.split(':')[1]}", m)
    oeufs.append({"type": "minecraft:item", "name": "minecraft:zombie_spawn_egg", "modifier": [{"type": "minecraft:set_components", "components": {
        "minecraft:entity_data": {"id": m}, "minecraft:item_name": {"text": f"Œuf : {nom}", "color": "gold"}}}]})
for i in range(0, len(oeufs), 27):
    p = f"{DATA}/loot_table/debug/oeufs_{i // 27}.json"
    json.dump({"pools": [{"rolls": 1, "entries": [e]} for e in oeufs[i:i + 27]]}, open(p, "w"), ensure_ascii=False, indent=1)

forge = sorted(f[:-5] for f in os.listdir(f"{DATA}/loot_table/forge"))
tonneaux = [
    ("Divers et sceaux de boss", [table("divers", divers)]),
    ("Ressources", [table("ressources", ressources)]),
    ("Trophées de boss", [table("trophees", trophees)]),
    ("Forge (1)", [f"royaumes:forge/{f}" for f in forge[:27]]),
    ("Forge (2)", [f"royaumes:forge/{f}" for f in forge[27:]]),
] + [(f"Œufs des mobs ({i + 1})", [f"royaumes:debug/oeufs_{i}"]) for i in range((len(oeufs) + 26) // 27)]

L = ["# Pose des tonneaux remplis de tous les objets du jeu, devant toi (vers l'est)",
     'tellraw @s {"text":"Tous les objets du jeu sont dans les tonneaux à côté de toi.","color":"gold"}']
for i, (nom, tables) in enumerate(tonneaux):
    x = 2 + 2 * i
    L.append(f'setblock ~{x} ~ ~2 minecraft:barrel[facing=up]{{CustomName:"{nom}"}} replace')
    for t in tables:
        L.append(f"loot insert ~{x} ~ ~2 loot {t}")
    L.append(f'summon minecraft:text_display ~{x}.5 ~1.3 ~2.5 {{text:"{nom}",billboard:"center",Tags:["rm_debug"]}}')
open(f"{DATA}/function/debug/objets.mcfunction", "w").write("\n".join(L) + "\n")
print(len(tonneaux), "tonneaux,", len(oeufs), "œufs,", len(forge), "objets de forge,", len(ressources), "ressources")
