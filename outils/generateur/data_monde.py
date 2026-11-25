# -*- coding: utf-8 -*-
"""Biomes des Royaumes Mortels, profils de mobs et structures."""
from data_factions import C

# --------------------------------------------------------------------------- PROFILS DE MOBS
# equip : slot -> spec d'objet (même format que les kits) ; attrs : valeurs de base
def eq(item, **kw):
    d = {"id": item, "lore": [], "ench": {}}
    d.update(kw)
    return d

P = {}
def profil(pid, nom, c, alliance, base, equip=None, attrs=None, effets=(), bebe=False):
    P[pid] = dict(id=pid, nom=nom, c=c, alliance=alliance, base=base, equip=equip or {},
                  attrs=attrs or {}, effets=list(effets), bebe=bebe)

T_SC = ("gold", "sentry")
def armure_fer(trim, casque=True, mat="iron"):
    d = {"armor.chest": eq(f"minecraft:{mat}_chestplate", trim=trim),
         "armor.legs": eq(f"minecraft:{mat}_leggings", trim=trim),
         "armor.feet": eq(f"minecraft:{mat}_boots", trim=trim)}
    if casque:
        d["armor.head"] = eq(f"minecraft:{mat}_helmet", trim=trim, unbreakable=True)
    return d

def cuir(couleur, trim=None, casque=True, complet=False):
    d = {"armor.chest": eq("minecraft:leather_chestplate", dye=couleur, trim=trim)}
    if casque:
        d["armor.head"] = eq("minecraft:leather_helmet", dye=couleur, unbreakable=True)
    if complet:
        d["armor.legs"] = eq("minecraft:leather_leggings", dye=couleur)
        d["armor.feet"] = eq("minecraft:leather_boots", dye=couleur)
    return d

def avec(d, **slots):
    d = dict(d)
    for k, v in slots.items():
        d[k.replace("_", ".", 1)] = v
    return d

# ---- Ordre
profil("sc_liberator", "Libérateur Foudroyés", "gold", "ordre", "zombie",
       avec(armure_fer(T_SC), weapon_mainhand=eq("minecraft:iron_axe"), weapon_offhand=eq("minecraft:shield")),
       {"max_health": 40, "attack_damage": 6, "scale": 1.15})
profil("sc_judicator", "Justicier Foudroyés", "gold", "ordre", "skeleton",
       avec(armure_fer(T_SC), weapon_mainhand=eq("minecraft:bow", ench={"minecraft:power": 1})),
       {"max_health": 30, "scale": 1.15})
profil("sc_lord", "Seigneur-Céleste", "gold", "ordre", "zombie",
       avec(armure_fer(("lapis", "sentry"), mat="netherite"),
            weapon_mainhand=eq("minecraft:mace", ench={"royaumes:foudre_de_sigmar": 1})),
       {"max_health": 80, "attack_damage": 10, "scale": 1.25, "knockback_resistance": 0.6})
profil("cites_garde", "Soldat de la Garde Franche", "aqua", "ordre", "zombie",
       avec(cuir(C["azur"], ("gold", "coast"), casque=False), armor_head=eq("minecraft:iron_helmet", unbreakable=True),
            weapon_mainhand=eq("minecraft:iron_sword")),
       {"max_health": 26, "attack_damage": 5})
profil("cites_arbaletrier", "Tireur de la Garde Franche", "aqua", "ordre", "skeleton",
       avec(cuir(C["azur"], casque=False), armor_head=eq("minecraft:chainmail_helmet", unbreakable=True),
            weapon_mainhand=eq("minecraft:bow")), {"max_health": 22})
profil("fyreslayer", "Berserker de Braise", "gold", "ordre", "zombie",
       {"armor.head": eq("minecraft:golden_helmet", trim=("redstone", "ward"), unbreakable=True),
        "weapon.mainhand": eq("minecraft:golden_axe", ench={"minecraft:fire_aspect": 1})},
       {"max_health": 30, "attack_damage": 6, "scale": 0.85})
profil("kharadron", "Aéronaute Nuées", "gold", "ordre", "skeleton",
       {"armor.head": eq("minecraft:iron_helmet", trim=("copper", "wayfinder"), unbreakable=True),
        "armor.chest": eq("minecraft:iron_chestplate", trim=("copper", "wayfinder")),
        "weapon.mainhand": eq("minecraft:bow")},
       {"max_health": 26, "scale": 0.85})
profil("khaine_aelf", "Sorcière de Morvaine", "red", "ordre", "zombie",
       avec(cuir(C["cramoisi"], ("iron", "vex")), weapon_mainhand=eq("minecraft:iron_sword")),
       {"max_health": 22, "attack_damage": 5, "movement_speed": 0.3})
profil("idoneth", "Serf des Abysses", "dark_aqua", "ordre", "drowned",
       avec(cuir(C["sarcelle"], ("diamond", "tide")), weapon_mainhand=eq("minecraft:trident")),
       {"max_health": 30, "attack_damage": 6})
profil("lumineth", "Archer Lumineux", "white", "ordre", "skeleton",
       avec(cuir(C["blanc"], ("quartz", "spire")), weapon_mainhand=eq("minecraft:bow")), {"max_health": 24})
profil("lumineth_garde", "Garde du Temple de Lumière", "white", "ordre", "zombie",
       avec(cuir(C["blanc"], ("quartz", "spire"), complet=True), weapon_mainhand=eq("minecraft:iron_sword")),
       {"max_health": 28, "attack_damage": 5})
profil("saurus", "Guerrier Écailleux", "green", "ordre", "zombie",
       avec(cuir(C["vert_sombre"], ("gold", "wild")), weapon_mainhand=eq("minecraft:stone_sword")),
       {"max_health": 34, "attack_damage": 6, "scale": 1.25, "armor": 4})
profil("skink", "Scinque", "green", "ordre", "skeleton",
       avec(cuir(C["jade"], ("gold", "wild")), weapon_mainhand=eq("minecraft:bow")),
       {"max_health": 16, "scale": 0.75, "movement_speed": 0.3})
profil("dryade", "Dryade Sylvains", "dark_green", "ordre", "zombie",
       avec(cuir(C["jade"], ("emerald", "flow"), complet=True), weapon_mainhand=eq("minecraft:wooden_sword")),
       {"max_health": 30, "attack_damage": 5}, effets=[("regeneration", 0)])
# ---- Chaos
profil("chaos_guerrier", "Guerrier du Chaos", "dark_gray", "chaos", "zombie",
       avec(armure_fer(("netherite", "eye")), weapon_mainhand=eq("minecraft:iron_sword"),
            weapon_offhand=eq("minecraft:shield")),
       {"max_health": 40, "attack_damage": 7, "scale": 1.1})
profil("chaos_seigneur", "Seigneur du Chaos", "dark_red", "chaos", "zombie",
       avec(armure_fer(("redstone", "rib"), mat="netherite"),
            weapon_mainhand=eq("minecraft:netherite_sword", ench={"minecraft:sharpness": 2})),
       {"max_health": 90, "attack_damage": 11, "scale": 1.3, "knockback_resistance": 0.6})
profil("bloodreaver", "Pillard de Sang de Sangrath", "dark_red", "chaos", "zombie",
       avec(cuir(C["cramoisi"], ("gold", "rib")), weapon_mainhand=eq("minecraft:iron_axe")),
       {"max_health": 26, "attack_damage": 6, "movement_speed": 0.28}, effets=[("strength", 0)])
profil("tzaangor", "Homme-Bec", "blue", "chaos", "skeleton",
       avec(cuir(C["bleu_tz"], ("amethyst", "eye")), weapon_mainhand=eq("minecraft:bow")), {"max_health": 24})
profil("demonette", "Démonette de Lyssara", "light_purple", "chaos", "zombie",
       avec(cuir(C["rose"], ("amethyst", "vex")), weapon_mainhand=eq("minecraft:iron_sword")),
       {"max_health": 20, "attack_damage": 5, "movement_speed": 0.33})
profil("pestigor", "Porte-Fléau de Morbus", "dark_green", "chaos", "zombie",
       avec(cuir(C["putride"], ("resin", "host"), complet=True),
            weapon_mainhand=eq("minecraft:iron_axe", ench={"royaumes:peste": 1})),
       {"max_health": 40, "attack_damage": 5, "movement_speed": 0.18}, effets=[("regeneration", 0)])
profil("clanrat", "Rat de Clan Hommes-Rats", "green", "chaos", "zombie",
       avec(cuir(C["brun"], ("emerald", "snout")),
            weapon_mainhand=eq("minecraft:stone_sword", ench={"royaumes:malepierre": 1})),
       {"max_health": 16, "attack_damage": 4, "scale": 0.75, "movement_speed": 0.3})
profil("jezzail", "Tireur de Long-Fusil Hommes-Rats", "green", "chaos", "skeleton",
       avec(cuir(C["brun"], ("emerald", "snout")), weapon_mainhand=eq("minecraft:bow", ench={"minecraft:power": 2})),
       {"max_health": 18, "scale": 0.8})
profil("hashut", "Garde Infernale de Ashkar", "gold", "chaos", "zombie",
       avec(armure_fer(("netherite", "shaper")), weapon_mainhand=eq("minecraft:iron_axe", ench={"minecraft:fire_aspect": 1})),
       {"max_health": 32, "attack_damage": 6, "scale": 0.85})
profil("hashut_tireur", "Arquebusier de Ashkar", "gold", "chaos", "skeleton",
       avec(armure_fer(("netherite", "shaper")), weapon_mainhand=eq("minecraft:bow", ench={"minecraft:flame": 1})),
       {"max_health": 26, "scale": 0.85})
# ---- Mort
profil("chainrasp", "Spectre Enchaîné Hantise Nocturne", "dark_aqua", "mort", "zombie",
       {"armor.head": eq("minecraft:chainmail_helmet", unbreakable=True), "armor.chest": eq("minecraft:chainmail_chestplate"),
        "weapon.mainhand": eq("minecraft:iron_hoe")},
       {"max_health": 20, "attack_damage": 5}, effets=[("invisibility", 0)])
profil("glaivewraith", "Spectre à Glaive Hantise Nocturne", "dark_aqua", "mort", "skeleton",
       {"armor.head": eq("minecraft:chainmail_helmet", unbreakable=True), "armor.chest": eq("minecraft:chainmail_chestplate"),
        "weapon.mainhand": eq("minecraft:iron_hoe", ench={"royaumes:vol_d_ame": 1})},
       {"max_health": 24, "attack_damage": 6}, effets=[("invisibility", 0)])
profil("deathrattle", "Squelette Cliquetant", "dark_purple", "mort", "skeleton",
       {"armor.head": eq("minecraft:chainmail_helmet", unbreakable=True), "weapon.mainhand": eq("minecraft:iron_sword"),
        "weapon.offhand": eq("minecraft:shield")}, {"max_health": 22})
profil("mort_sylvanie", "Mort de Sanguinie", "dark_purple", "mort", "zombie", {}, {"max_health": 24})
profil("vampire", "Seigneur Vampire", "dark_red", "mort", "zombie",
       avec(cuir(C["noir"], ("redstone", "silence"), casque=False, complet=True),
            armor_chest=eq("minecraft:netherite_chestplate", trim=("redstone", "silence")),
            weapon_mainhand=eq("minecraft:iron_sword", ench={"royaumes:vol_d_ame": 2})),
       {"max_health": 70, "attack_damage": 9, "movement_speed": 0.3})
profil("mortek", "Gard'Os Faucheurs d'Os", "white", "mort", "skeleton",
       avec(armure_fer(("quartz", "rib")), weapon_mainhand=eq("minecraft:iron_sword"), weapon_offhand=eq("minecraft:shield")),
       {"max_health": 36, "scale": 1.15, "armor": 6})
profil("goule", "Goule des Cryptes", "dark_purple", "mort", "zombie",
       {"armor.chest": eq("minecraft:leather_chestplate", dye=C["violet"], trim=("gold", "host"))},
       {"max_health": 22, "attack_damage": 5, "movement_speed": 0.32})
# ---- Destruction
profil("brute", "Brute Mâchefers", "gold", "destruction", "zombie",
       avec(armure_fer(("copper", "wild")), weapon_mainhand=eq("minecraft:iron_axe")),
       {"max_health": 45, "attack_damage": 8, "scale": 1.25})
profil("megaboss", "Grand Chef Mâchefers", "gold", "destruction", "zombie",
       avec(armure_fer(("copper", "wild"), mat="netherite"),
            weapon_mainhand=eq("minecraft:iron_axe", ench={"minecraft:sharpness": 3, "royaumes:waaagh": 1})),
       {"max_health": 100, "attack_damage": 12, "scale": 1.45, "knockback_resistance": 0.8})
profil("gutrippa", "Étripeur Cruelgars", "dark_green", "destruction", "zombie",
       avec(cuir(C["marais"], ("emerald", "wild")), weapon_mainhand=eq("minecraft:iron_sword", ench={"royaumes:peste": 1})),
       {"max_health": 28, "attack_damage": 5, "scale": 1.1})
profil("kb_archer", "Tireur Cruelgars", "dark_green", "destruction", "skeleton",
       avec(cuir(C["marais"], ("emerald", "wild")), weapon_mainhand=eq("minecraft:bow")), {"max_health": 24, "scale": 1.1})
profil("grot", "Gobelin de la Mauvaise Lune", "yellow", "destruction", "zombie",
       {"armor.head": eq("minecraft:leather_helmet", dye=C["noir"], unbreakable=True), "weapon.mainhand": eq("minecraft:stone_sword")},
       {"max_health": 10, "attack_damage": 3}, bebe=True)
profil("arachnarok", "Araignée Araignée Titanesque", "yellow", "destruction", "spider", {},
       {"max_health": 70, "attack_damage": 8, "scale": 2.2})
profil("gutbuster", "Ogre Panse-de-Fer", "gold", "destruction", "zombie",
       avec(cuir(C["brun"], ("iron", "host"), casque=False), weapon_mainhand=eq("minecraft:iron_axe")),
       {"max_health": 60, "attack_damage": 9, "scale": 1.6, "movement_speed": 0.2})
profil("ogor_chasseur", "Chasseur Ogre", "gold", "destruction", "skeleton",
       avec(cuir(C["brun"]), weapon_mainhand=eq("minecraft:bow", ench={"minecraft:punch": 1})),
       {"max_health": 40, "scale": 1.4})
profil("gargant", "Géant Mangeur d'Hommes", "dark_green", "destruction", "zombie",
       {"weapon.mainhand": eq("minecraft:wooden_axe", item_model="minecraft:oak_log")},
       {"max_health": 160, "attack_damage": 14, "scale": 3.5, "movement_speed": 0.2, "knockback_resistance": 1.0})
# ---- Spéciaux (structures)
profil("garde_cite", "Garde la Cité", "aqua", "ordre", "iron_golem", {}, {})
profil("habitant", None, "white", "ordre", "villager", {}, {})

# --------------------------------------------------------------------------- BIOMES
# base : biome vanilla dont on reprend les décorations / créatures
# grille : (bande température 1-4, band'humidité 1-3)
BIOMES = [
    dict(id="azyr_cimes", nom="Cimes Célestes d'Célestis", sous="Royaume des Cieux", c="aqua", base="meadow",
         temp=0.3, pluie=0.6, precip=True, ciel="#4f8cff", brume="#b0d0ff", eau="#3f9ee4", eau_brume="#1a4a8a",
         herbe="#7fd08a", feuilles="#5fbf6a", particules=[("minecraft:end_rod", 0.0015)],
         surface=None, special="pics",
         mobs={"zombie": ["sc_liberator"], "skeleton": ["sc_judicator"]}),
    dict(id="hysh_plateaux", nom="Plateaux de Lumière de Lumina", sous="Royaume de la Lumière", c="white", base="cherry_grove",
         temp=0.5, pluie=0.5, precip=True, ciel="#fff3c0", brume="#fffbe6", eau="#9fe0ff", eau_brume="#4a90b0",
         herbe="#d4e89a", feuilles="#e8f0b0", particules=[("minecraft:end_rod", 0.002)],
         surface={"top": [("minecraft:grass_block", None), ("minecraft:calcite", (0.25, 0.6))], "under": "minecraft:dirt"},
         grille=(1, 2), mobs={"zombie": ["lumineth_garde"], "skeleton": ["lumineth", "lumineth", "tzaangor"]}),
    dict(id="ghyran_jade", nom="Forêts de Jade Sylvéa", sous="Royaume de la Vie", c="green", base="flower_forest",
         temp=0.7, pluie=0.9, precip=True, ciel="#8fd9a8", brume="#c0f0d0", eau="#3fbfa0", eau_brume="#1a6a50",
         herbe="#3fbf5f", feuilles="#2fa84f", particules=[("minecraft:spore_blossom_air", 0.004)],
         surface=None, grille=(2, 3),
         mobs={"zombie": ["dryade", "dryade", "cites_garde"], "skeleton": ["cites_arbaletrier"]}),
    dict(id="ghyran_marais", nom="Marais Putrides de Sylvéa", sous="Terres corrompues par Morbus", c="dark_green",
         base="mangrove_swamp", temp=0.85, pluie=0.9, precip=True, ciel="#9aab5a", brume="#7a8a3a", eau="#4a5a1a",
         eau_brume="#2a3a08", herbe="#6b7a2a", feuilles="#5a6a20", particules=[("minecraft:mycelium", 0.02)],
         surface={"top": [("minecraft:grass_block", None), ("minecraft:mud", (-0.2, 0.3))], "under": "minecraft:mud"},
         grille=(4, 3), mobs={"zombie": ["pestigor", "gutrippa", "gutrippa"], "skeleton": ["kb_archer"]}),
    dict(id="ghur_terres", nom="Terres Sauvages de Féralia", sous="Royaume des Bêtes", c="gold", base="savanna",
         temp=1.2, pluie=0.2, precip=False, ciel="#e8a858", brume="#f0c890", eau="#4fa0c0", eau_brume="#205060",
         herbe="#b8a040", feuilles="#a09030", particules=[],
         surface={"top": [("minecraft:grass_block", None), ("minecraft:coarse_dirt", (0.3, 0.7))], "under": "minecraft:dirt"},
         grille=[(2, 2), (3, 2)],
         mobs={"zombie": ["brute", "brute", "brute", "gutbuster", "gutbuster", "gargant"],
               "skeleton": ["ogor_chasseur"]}),
    dict(id="ghur_jungle", nom="Jungles Primordiales de Féralia", sous="Royaume des Bêtes", c="green", base="jungle",
         temp=0.95, pluie=0.9, precip=True, ciel="#7fe0a0", brume="#b0f0c0", eau="#3fa0a0", eau_brume="#105050",
         herbe="#30c040", feuilles="#20b030", particules=[],
         surface=None, grille=(3, 3), mobs={"zombie": ["saurus"], "skeleton": ["skink"]}),
    dict(id="aqshy_cendres", nom="Plaines de Cendres d'Pyréa", sous="Royaume du Feu", c="red", base="badlands",
         temp=2.0, pluie=0.0, precip=False, ciel="#ff6a3a", brume="#8a2a10", eau="#ff7a2a", eau_brume="#6a1a00",
         herbe="#7a5a30", feuilles="#6a4a20", particules=[("minecraft:white_ash", 0.04), ("minecraft:lava", 0.0008)],
         surface={"top": [("minecraft:basalt", None), ("minecraft:blackstone", (-0.3, 0.3)), ("minecraft:magma_block", (0.55, 0.62))],
                  "under": "minecraft:blackstone"},
         grille=(4, 1), extra=["magma_aqshy"],
         mobs={"zombie": ["fyreslayer", "bloodreaver", "hashut"], "skeleton": ["hashut_tireur"], "husk": ["hashut", "bloodreaver"]}),
    dict(id="chamon_desert", nom="Déserts d'Or de Ferrumia", sous="Royaume du Métal", c="yellow", base="desert",
         temp=2.0, pluie=0.0, precip=False, ciel="#ffd75a", brume="#f0d080", eau="#c0b040", eau_brume="#605010",
         herbe="#c0b040", feuilles="#b0a030", particules=[("minecraft:wax_on", 0.002)],
         surface={"top": [("minecraft:sand", None), ("minecraft:yellow_terracotta", (0.3, 0.5)), ("minecraft:raw_gold_block", (0.62, 0.64))],
                  "under": "minecraft:sandstone"},
         grille=(3, 1), extra=["or_chamon"],
         mobs={"zombie": ["hashut"], "skeleton": ["kharadron"], "husk": ["hashut"]}),
    dict(id="shyish_terres", nom="Terres Funèbres de Nécréa", sous="Royaume de la Mort", c="dark_purple", base="pale_garden",
         temp=0.4, pluie=0.4, precip=False, ciel="#5a5a6e", brume="#3a3a48", eau="#3a3a5a", eau_brume="#101020",
         herbe="#6a6a6a", feuilles="#5a5a5a", particules=[("minecraft:white_ash", 0.03), ("minecraft:soul", 0.0008)],
         surface={"top": [("minecraft:grass_block", None), ("minecraft:soul_soil", (0.2, 0.6)), ("minecraft:podzol", (-0.5, -0.2))],
                  "under": "minecraft:dirt"},
         grille=(1, 1), extra=["os_shyish"],
         mobs={"zombie": ["mort_sylvanie", "mort_sylvanie", "goule", "chainrasp"],
               "skeleton": ["deathrattle", "deathrattle", "mortek", "glaivewraith"]}),
    dict(id="ulgu_brumes", nom="Brumes d'Ombre d'Umbria", sous="Royaume des Ombres", c="dark_gray", base="dark_forest",
         temp=0.6, pluie=0.8, precip=True, ciel="#3a3a50", brume="#2a2a3a", eau="#2a3a5a", eau_brume="#0a1020",
         herbe="#3a5a3a", feuilles="#2a4a2a", particules=[("minecraft:ash", 0.02)], brouillard=0.25,
         surface=None, grille=(1, 3),
         mobs={"zombie": ["khaine_aelf", "khaine_aelf", "grot", "grot", "goule"], "spider": ["arachnarok", "_", "_", "_"]}),
    dict(id="ulgu_mer", nom="Mers d'Ombre d'Umbria", sous="Royaume des Ombres", c="dark_aqua", base="deep_ocean",
         temp=0.5, pluie=0.5, precip=True, ciel="#4a5a7a", brume="#3a4a6a", eau="#1a2a4a", eau_brume="#081428",
         herbe="#3a5a3a", feuilles="#2a4a2a", particules=[],
         surface={"top": [("minecraft:gravel", None), ("minecraft:sand", (0.0, 0.5))], "under": "minecraft:gravel"},
         special="ocean", mobs={"drowned": ["idoneth"]}),
    dict(id="chaos_desolation", nom="Désolation des Huit-Voies", sous="Le Royaume du Chaos", c="dark_red", base="badlands",
         temp=1.5, pluie=0.0, precip=False, ciel="#6a0a0a", brume="#4a0808", eau="#5a0a0a", eau_brume="#200000",
         herbe="#5a2a2a", feuilles="#4a1a1a", particules=[("minecraft:crimson_spore", 0.02)],
         surface={"top": [("minecraft:netherrack", None), ("minecraft:blackstone", (-0.25, 0.25)), ("minecraft:crimson_nylium", (0.5, 0.7))],
                  "under": "minecraft:blackstone"},
         grille=(2, 1), extra=["obsidienne_chaos"],
         mobs={"zombie": ["chaos_guerrier", "chaos_guerrier", "chaos_guerrier", "bloodreaver", "demonette", "demonette"],
               "skeleton": ["tzaangor"]}),
    dict(id="terres_rongees", nom="Terres Rongées de Fangepierre", sous="Domaine des Hommes-Rats", c="green", base="swamp",
         temp=0.8, pluie=0.7, precip=True, ciel="#6a7a3a", brume="#5a6a2a", eau="#4a6a1a", eau_brume="#1a2a00",
         herbe="#7a7a3a", feuilles="#6a6a2a", particules=[("minecraft:mycelium", 0.015)],
         surface={"top": [("minecraft:coarse_dirt", None), ("minecraft:gravel", (-0.3, 0.1)), ("minecraft:mud", (0.4, 0.8))],
                  "under": "minecraft:dirt"},
         grille=(4, 2), extra=["malepierre"],
         mobs={"zombie": ["clanrat"], "skeleton": ["jezzail"]}),
]

# Monstres apparaissant par biome (créatures passives : reprises du biome de base)
SPAWN_MONSTRES = {
    "default": [("zombie", 95, 4), ("skeleton", 90, 4), ("spider", 60, 4), ("creeper", 60, 4), ("enderman", 10, 1)],
    "aqshy_cendres": [("zombie", 70, 4), ("husk", 60, 4), ("skeleton", 60, 4), ("magma_cube", 30, 2), ("creeper", 30, 2)],
    "chamon_desert": [("husk", 80, 4), ("zombie", 30, 4), ("skeleton", 80, 4), ("spider", 40, 4), ("creeper", 40, 2)],
    "ulgu_mer": [("drowned", 100, 4)],
    "ulgu_brumes": [("zombie", 95, 4), ("spider", 80, 4), ("skeleton", 40, 4), ("witch", 10, 1), ("enderman", 10, 1)],
    "shyish_terres": [("zombie", 90, 4), ("skeleton", 110, 4), ("wither_skeleton", 8, 1), ("spider", 30, 2)],
    "chaos_desolation": [("zombie", 110, 4), ("skeleton", 60, 4), ("blaze", 5, 1), ("enderman", 15, 1)],
}

# --------------------------------------------------------------------------- STRUCTURES
# biomes : biomes des Royaumes ; monde : biomes vanilla de l'Overworld
STRUCTURES = [
    dict(id="forteresse_stormcast", nom="Forteresse Foudroyés", biomes=["azyr_cimes", "hysh_plateaux"],
         monde=["meadow", "plains", "windswept_hills"], espacement=36, sep=14),
    dict(id="cite_sigmar", nom="Cité Libre de Aurion", biomes=["ghyran_jade", "ghur_terres", "chamon_desert"],
         monde=["plains", "sunflower_plains", "savanna", "meadow"], espacement=34, sep=14),
    dict(id="camp_orruk", nom="Camp Mâchefers", biomes=["ghur_terres"], monde=["savanna", "badlands", "windswept_savanna"],
         espacement=24, sep=8),
    dict(id="fort_kruleboyz", nom="Fort des Cruelgars", biomes=["ghyran_marais"], monde=["swamp", "mangrove_swamp"],
         espacement=24, sep=8),
    dict(id="temple_seraphon", nom="Temple-Cité Astrosauriens", biomes=["ghur_jungle"], monde=["jungle", "bamboo_jungle"],
         espacement=28, sep=10),
    dict(id="bosquet_sylvaneth", nom="Bosquet Sylvains", biomes=["ghyran_jade"], monde=["forest", "flower_forest", "birch_forest"],
         espacement=24, sep=8),
    dict(id="magmahold", nom="Magmahold Fyreslayer", biomes=["aqshy_cendres"], monde=["badlands", "eroded_badlands"],
         espacement=26, sep=9),
    dict(id="port_kharadron", nom="Port Céleste Nuées", biomes=["chamon_desert"], monde=["desert", "windswept_gravelly_hills"],
         espacement=26, sep=9),
    dict(id="ziggurat_hashut", nom="Ziggurat de Ashkar", biomes=["aqshy_cendres", "chaos_desolation"], monde=[],
         espacement=26, sep=9),
    dict(id="citadelle_chaos", nom="Citadelle du Chaos", biomes=["chaos_desolation"],
         monde=["stony_peaks", "windswept_gravelly_hills", "snowy_taiga"], espacement=30, sep=10),
    dict(id="repaire_skaven", nom="Repaire Hommes-Rats", biomes=["terres_rongees"], monde=["swamp", "taiga"], espacement=22, sep=8),
    dict(id="chateau_soulblight", nom="Château Sanguinaire", biomes=["shyish_terres"], monde=["dark_forest", "pale_garden"],
         espacement=30, sep=10),
    dict(id="ossuaire_ossiarch", nom="Ossuaire Faucheurs d'Os", biomes=["shyish_terres"], monde=["desert"], espacement=28, sep=10),
    dict(id="cimetiere_nighthaunt", nom="Cimetière Hanté", biomes=["shyish_terres", "ulgu_brumes"], monde=["dark_forest", "pale_garden", "swamp"],
         espacement=22, sep=8),
    dict(id="sanctuaire_lumineth", nom="Sanctuaire de Lumière", biomes=["hysh_plateaux"], monde=["cherry_grove", "meadow"],
         espacement=26, sep=9),
    dict(id="temple_khaine", nom="Temple de Morvaine", biomes=["ulgu_brumes"], monde=["dark_forest"], espacement=26, sep=9),
    dict(id="ruines_idoneth", nom="Ruines Abyssal", biomes=["ulgu_mer"], monde=["deep_ocean", "ocean", "deep_lukewarm_ocean", "deep_cold_ocean"],
         espacement=26, sep=9, ocean=True),
    dict(id="antre_gitz", nom="Antre des Gobelins", biomes=["ulgu_brumes"], monde=["old_growth_spruce_taiga", "dark_forest"],
         espacement=24, sep=8),
    dict(id="campement_ogor", nom="Campement Ogre", biomes=["ghur_terres"], monde=["savanna_plateau", "windswept_savanna"],
         espacement=26, sep=9),
]
