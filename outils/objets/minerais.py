# -*- coding: utf-8 -*-
"""Répartition des minerais vanilla selon les Royaumes (à lancer après la génération du datapack).
Chaque Royaume a sa richesse et ses manques ; son minerai propre (éclats de Vent, malepierre) est ajouté par
objets.py (biome modifiers). Le monde de base garde la génération vanilla + un peu de pierre des Royaumes."""
import glob
import json
import os

ICI = os.path.dirname(os.path.abspath(__file__))
BIOMES = os.path.join(ICI, "..", "..", "src", "main", "resources", "data", "royaumes", "worldgen", "biome")
# préfixe de biome : (minerais retirés, minerais ajoutés)
REGLES = {
    "azyr_": (["ore_coal_upper", "ore_coal_lower", "ore_redstone", "ore_redstone_lower", "ore_copper"], ["ore_lapis", "ore_diamond_medium"]),
    "aqshy_": (["ore_lapis", "ore_lapis_buried", "ore_emerald", "ore_copper", "ore_diamond_buried"], ["ore_gold_extra", "ore_redstone"]),
    "ghur_": (["ore_diamond_large", "ore_diamond_buried", "ore_lapis_buried", "ore_emerald", "ore_gold_lower"], ["ore_copper_large", "ore_iron_upper"]),
    "ghyran_": (["ore_redstone", "ore_redstone_lower", "ore_diamond_large", "ore_gold_lower"], ["ore_emerald", "ore_copper_large"]),
    "hysh_": (["ore_coal_upper", "ore_coal_lower", "ore_redstone_lower", "ore_copper"], ["ore_emerald", "ore_diamond_large"]),
    "ulgu_": (["ore_gold", "ore_gold_lower", "ore_emerald", "ore_copper"], ["ore_lapis_buried", "ore_redstone_lower"]),
    "shyish_": (["ore_copper", "ore_emerald", "ore_lapis_buried", "ore_iron_upper"], ["ore_gold_lower", "ore_diamond_buried"]),
    "chamon_": (["ore_lapis", "ore_lapis_buried", "ore_emerald", "ore_coal_upper"], ["ore_gold_extra", "ore_copper_large", "ore_iron_upper"]),
    "chaos_": (["ore_lapis", "ore_lapis_buried", "ore_emerald", "ore_diamond_large"], ["ore_redstone"]),
    "terres_rongees": (["ore_lapis", "ore_emerald", "ore_diamond_large", "ore_gold_lower"], ["ore_coal_lower"]),
}


# ordre canonique (celui de la génération vanilla) : tous les biomes d'une dimension doivent lister leurs
# minerais dans le même ordre, sinon le jeu détecte un « feature order cycle » et ne génère plus rien.
CANON = ["ore_dirt", "ore_gravel", "ore_granite_upper", "ore_granite_lower", "ore_diorite_upper", "ore_diorite_lower",
         "ore_andesite_upper", "ore_andesite_lower", "ore_tuff", "ore_coal_upper", "ore_coal_lower", "ore_iron_upper",
         "ore_iron_middle", "ore_iron_small", "ore_gold", "ore_gold_lower", "ore_redstone", "ore_redstone_lower", "ore_diamond",
         "ore_diamond_medium", "ore_diamond_large", "ore_diamond_buried", "ore_lapis", "ore_lapis_buried", "ore_copper",
         "ore_copper_large", "underwater_magma", "ore_gold_extra", "disk_sand", "disk_clay", "disk_gravel", "ore_emerald"]


def rang(x):
    n = x.split(":")[1]
    return (0, CANON.index(n)) if x.startswith("minecraft:") and n in CANON else (1, 0)


def main():
    n = 0
    for f in sorted(glob.glob(os.path.join(BIOMES, "*.json"))):
        nom = os.path.basename(f)[:-5]
        regle = next((r for p, r in REGLES.items() if nom.startswith(p)), None)
        if not regle:
            continue
        j = json.load(open(f, encoding="utf-8"))
        etape = j["features"][6]
        retires = {"minecraft:" + x for x in regle[0]}
        etape[:] = [x for x in etape if x not in retires]
        for x in regle[1]:
            if "minecraft:" + x not in etape:
                etape.append("minecraft:" + x)
        etape.sort(key=rang)  # tri stable : les features du mod gardent leur ordre, après les minerais vanilla
        json.dump(j, open(f, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
        n += 1
    print(n, "biomes rééquilibrés")


if __name__ == "__main__":
    main()
