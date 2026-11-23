# -*- coding: utf-8 -*-
"""Données v4 : nouveaux biomes, dimensions de royaume, mise à jour des structures et décors."""
from data_monde import BIOMES, STRUCTURES, SPAWN_MONSTRES
import decors
from structures4 import DECOS4, DECOS_FLOTTANTS

# Partage de cases de la grille climatique par l'étrangeté (weirdness)
for b in BIOMES:
    if b["id"] in ("aqshy_cendres", "ghyran_jade", "ulgu_brumes"):
        b["weird"] = (-1.0, 0.0)

BIOMES.extend([
    dict(id="aqshy_volcans", nom="Volcans d'Aqshy", sous="Royaume du Feu — terres des Fyreslayers", c="gold", base="badlands",
         temp=2.0, pluie=0.0, precip=False, ciel="#ff4a1a", brume="#6a1a0a", eau="#ff6a1a", eau_brume="#5a1000",
         herbe="#6a4a2a", feuilles="#5a3a1a",
         particules=[("minecraft:white_ash", 0.06), ("minecraft:lava", 0.002), ("minecraft:campfire_cosy_smoke", 0.0008)],
         surface={"top": [("minecraft:basalt", None), ("minecraft:blackstone", (-0.4, 0.0)), ("minecraft:magma_block", (0.45, 0.55)),
                          ("minecraft:tuff", (0.2, 0.3))], "under": "minecraft:blackstone"},
         grille=(4, 1), weird=(0.0, 1.0), extra=["magma_aqshy"],
         mobs={"zombie": ["fyreslayer", "fyreslayer", "hashut", "bloodreaver"], "skeleton": ["hashut_tireur"], "husk": ["fyreslayer", "hashut"]}),
    dict(id="ghyran_wyldwood", nom="Wyldwood d'Automne", sous="Royaume de la Vie — bois des Sylvaneth", c="gold", base="dark_forest",
         temp=0.6, pluie=0.8, precip=True, ciel="#a8c8a0", brume="#e0c8a0", eau="#3f9f80", eau_brume="#1a5a40",
         herbe="#8a8a3a", feuilles="#c8642a", particules=[("minecraft:tinted_leaves", 0.01), ("minecraft:spore_blossom_air", 0.003)],
         surface={"top": [("minecraft:grass_block", None), ("minecraft:podzol", (0.3, 0.6)), ("minecraft:moss_block", (-0.6, -0.3))],
                  "under": "minecraft:dirt"},
         grille=(2, 3), weird=(0.0, 1.0),
         mobs={"zombie": ["dryade", "dryade", "dryade"], "skeleton": ["cites_arbaletrier"]}),
    dict(id="ulgu_marais_lune", nom="Marais de la Mauvaise Lune", sous="Royaume des Ombres — antres des Gitz", c="yellow", base="swamp",
         temp=0.7, pluie=0.9, precip=True, ciel="#1a2a1a", brume="#2a4a2a", eau="#2a6a2a", eau_brume="#0a2a0a",
         herbe="#3a5a2a", feuilles="#2a4a1a", particules=[("minecraft:mycelium", 0.03), ("minecraft:glow", 0.003)], brouillard=0.35,
         surface={"top": [("minecraft:grass_block", None), ("minecraft:mud", (-0.3, 0.3)), ("minecraft:mycelium", (0.5, 0.8))],
                  "under": "minecraft:mud"},
         grille=(1, 3), weird=(0.0, 1.0),
         mobs={"zombie": ["grot", "grot", "grot", "khaine_aelf"], "spider": ["arachnarok", "_", "_"]}),
    dict(id="hysh_iles", nom="Îles Célestes de Hysh", sous="Royaume de la Lumière — sanctuaires Lumineth", c="white", base="cherry_grove",
         temp=0.5, pluie=0.5, precip=False, ciel="#fff6d0", brume="#fffbe8", eau="#9fe0ff", eau_brume="#4a90b0",
         herbe="#d4e89a", feuilles="#e8f0b0", particules=[("minecraft:end_rod", 0.003)],
         surface={"top": [("minecraft:grass_block", None), ("minecraft:calcite", (0.3, 0.6))], "under": "minecraft:dirt"},
         special="flottant", mobs={"zombie": ["lumineth_garde"], "skeleton": ["lumineth"]}),
])
SPAWN_MONSTRES["aqshy_volcans"] = SPAWN_MONSTRES["aqshy_cendres"]
SPAWN_MONSTRES["ulgu_marais_lune"] = [("zombie", 100, 4), ("spider", 90, 4), ("slime", 20, 2), ("witch", 6, 1)]

# Dimensions de royaume (en plus de royaumes:royaumes_mortels)
DIMENSIONS = {
    "aqshy": dict(nom="Aqshy, Royaume du Feu", c="gold", biomes=["aqshy_cendres", "aqshy_volcans"]),
    "shyish": dict(nom="Shyish, Royaume de la Mort", c="dark_purple", biomes=["shyish_terres", "ulgu_brumes"]),
    "ghur": dict(nom="Ghur, Royaume des Bêtes", c="gold", biomes=["ghur_terres", "ghur_jungle"]),
    "huit_points": dict(nom="Les Huit-Points du Chaos", c="dark_red", biomes=["chaos_desolation", "terres_rongees"]),
    "hysh": dict(nom="Hysh, Îles de Lumière", c="white", biomes=["hysh_iles"], flottant=True),
}

# Structures : nouveaux emplacements
MAJ = {
    "forteresse_stormcast": dict(biomes=["azyr_cimes", "hysh_plateaux"],
                                 monde=["jagged_peaks", "stony_peaks", "frozen_peaks", "meadow", "windswept_hills"]),
    "magmahold": dict(biomes=["aqshy_volcans"], monde=[], espacement=30, sep=10),
    "antre_gitz": dict(biomes=["ulgu_marais_lune"], monde=["swamp", "mangrove_swamp"]),
    "bosquet_sylvaneth": dict(biomes=["ghyran_wyldwood", "ghyran_jade"], monde=["forest", "flower_forest", "dark_forest"]),
    "sanctuaire_lumineth": dict(biomes=["hysh_plateaux", "hysh_iles"], monde=["cherry_grove", "meadow"], flottant=True),
    "ziggurat_hashut": dict(biomes=["aqshy_cendres", "aqshy_volcans", "chaos_desolation"]),
    "autel_skarbrand": dict(biomes=["aqshy_cendres", "aqshy_volcans"]),
    "temple_khaine": dict(biomes=["ulgu_brumes"], monde=["dark_forest", "badlands"]),
}
for st in STRUCTURES:
    if st["id"] in MAJ:
        st.update(MAJ[st["id"]])
    if st["id"] == "portail":
        st["biomes"] += ["aqshy_volcans", "ghyran_wyldwood", "ulgu_marais_lune", "hysh_iles"]
STRUCTURES.append(dict(id="repaire_skavenblight", nom="Repaire de Skavenblight", biomes=["terres_rongees"],
                       monde=["swamp"], espacement=34, sep=12))

# Décors : nouveaux biomes ajoutés aux décors existants
AJOUTS = {"pilier_flamme": ["aqshy_volcans"], "mare_lave": ["aqshy_volcans"], "forge_abandonnee": ["aqshy_volcans"],
          "champignon_geant": ["ulgu_marais_lune"], "arbre_esprit": ["ghyran_wyldwood"], "cercle_pierres": ["ghyran_wyldwood"],
          "sanctuaire_alarielle": ["ghyran_wyldwood"], "cristal_hysh": ["hysh_iles"], "arche_lumineth": ["hysh_iles"],
          "statue_stormcast": ["hysh_iles"], "squelette_bete": ["aqshy_volcans"]}
for did, bl in AJOUTS.items():
    fn_, b0, ch = decors.DECOS[did]
    decors.DECOS[did] = (fn_, b0 + bl, ch)
decors.DECOS.update(DECOS4)
FLOTTANTS = DECOS_FLOTTANTS

CREATURES_V4 = {
    "ghyran_wyldwood": [("fox", 8, 3), ("rabbit", 6, 3), ("wolf", 4, 4), ("bee", 2, 3)],
    "ulgu_marais_lune": [("frog", 10, 5)],
    "aqshy_volcans": [("strider", 4, 2)],
    "hysh_iles": [("sheep", 8, 4), ("rabbit", 6, 3), ("allay", 1, 1)],
}
