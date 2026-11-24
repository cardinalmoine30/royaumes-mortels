# -*- coding: utf-8 -*-
"""Extension « vrai jeu » : ressources, Forge des Royaumes, consommables, talismans, RPG (Gloire & compétences),
boss de faction avec capacités et barres de vie."""
import json, os, copy
import build as B
from build import w, fn, entry, components, jtxt, txt, NS, DIM, OUT
from data_monde import P as PROFILS, BIOMES, eq
from data_factions import C

# =========================================================================== RESSOURCES
BASE_RES = "minecraft:armadillo_scute"
RES = {
    "eclat":      ("Éclat de Royaume", "light_purple", "minecraft:amethyst_shard", "Fragment cristallisé d'un Royaume Mortel."),
    "sigmarite":  ("Lingot de Sigmarite", "gold", "minecraft:gold_ingot", "Métal divin forgé dans le Sigmarabulum."),
    "malepierre": ("Malepierre", "green", "minecraft:emerald", "Chaos solidifié. Ne surtout pas lécher."),
    "ur_or":      ("Ur-Or", "gold", "minecraft:raw_gold", "Or runique chargé de la fureur de Grimnir."),
    "aether_or":  ("Aether-Or", "yellow", "minecraft:glowstone_dust", "Gaz d'or des cieux de Chamon, solidifié."),
    "ame":        ("Fragment d'Âme", "dark_aqua", "minecraft:echo_shard", "Un murmure de Shyish emprisonné."),
    "braise":     ("Braise d'Aqshy", "red", "minecraft:blaze_powder", "Elle ne s'éteint jamais."),
    "ambre":      ("Ambre de Ghur", "gold", "minecraft:resin_brick", "La rage d'une bête primordiale y dort."),
    "graine":     ("Graine de Vie", "green", "minecraft:torchflower_seeds", "Bénie par Alarielle, la Reine Éternelle."),
    "ombre":      ("Pierre-Ombre", "dark_gray", "minecraft:flint", "Un éclat des brumes d'Ulgu."),
    "cristal":    ("Cristal de Hysh", "white", "minecraft:prismarine_crystals", "De la lumière pure, cristallisée."),
    "chaos":      ("Éclat du Chaos", "dark_red", "minecraft:magma_cream", "Il murmure des promesses de gloire."),
    "ferraille":  ("Ferraille d'Orruk", "gray", "minecraft:iron_nugget", "Ça peut toujours servir pour cogner."),
}


def res_spec(rid, n=1):
    nom, c, model, lore = RES[rid]
    return {"id": BASE_RES, "nom": nom, "c": c, "lore": [lore, "Ressource des Royaumes"], "item_model": model,
            "custom_data": {"rm": rid}, "rarity": "rare", "n": n}


def res_nbt(rid):
    return '{Item:{id:"%s",components:{"minecraft:custom_data":{rm:"%s"}}}}' % (BASE_RES, rid)


# Ressource principale lâchée par chaque profil de mob
RES_PROFIL = {
    "sc_liberator": "sigmarite", "sc_judicator": "sigmarite", "sc_lord": "sigmarite", "cites_garde": "eclat",
    "cites_arbaletrier": "eclat", "fyreslayer": "ur_or", "kharadron": "aether_or", "khaine_aelf": "ombre",
    "idoneth": "ombre", "lumineth": "cristal", "lumineth_garde": "cristal", "saurus": "ambre", "skink": "ambre",
    "dryade": "graine", "chaos_guerrier": "chaos", "chaos_seigneur": "chaos", "bloodreaver": "braise",
    "tzaangor": "chaos", "demonette": "chaos", "pestigor": "graine", "clanrat": "malepierre", "jezzail": "malepierre",
    "hashut": "braise", "hashut_tireur": "braise", "chainrasp": "ame", "glaivewraith": "ame", "deathrattle": "ame",
    "mort_sylvanie": "ame", "vampire": "ame", "mortek": "ame", "goule": "ame", "brute": "ferraille",
    "megaboss": "ferraille", "gutrippa": "ferraille", "kb_archer": "ferraille", "grot": "ombre",
    "arachnarok": "ombre", "gutbuster": "ambre", "ogor_chasseur": "ambre", "gargant": "ambre",
}
ELITES = {"sc_lord", "chaos_seigneur", "vampire", "megaboss", "gargant", "arachnarok"}


# =========================================================================== OBJETS FORGÉS
def armure(prefix, mat, trim, noms, couleur, bonus, uid):
    """Panoplie complète ; bonus = liste (attribut, valeur, op) appliquée à chaque pièce."""
    pieces = [("helmet", "head", 3), ("chestplate", "chest", 8), ("leggings", "legs", 6), ("boots", "feet", 3)]
    out = []
    for (p, slot, arm), nom in zip(pieces, noms):
        attrs = [("armor", arm, "add_value", slot), ("armor_toughness", 3, "add_value", slot)]
        attrs += [(a, v, op, slot) for a, v, op in bonus]
        out.append({"id": f"minecraft:{mat}_{p}", "nom": nom, "c": couleur, "trim": trim, "lore": [prefix],
                    "attrs": attrs, "uid": f"{uid}_{p}", "rarity": "epic"})
    return out


def potion(nom, couleur, model, effets, lore, uid):
    return {"id": BASE_RES, "nom": nom, "c": couleur, "lore": [lore], "item_model": model, "uid": uid,
            "custom_data": {"rm": uid}, "max_stack": 16,
            "consumable": {"animation": "drink", "consume_seconds": 1.6, "sound": "minecraft:entity.generic.drink",
                           "has_consume_particles": False,
                           "on_consume_effects": [{"type": "minecraft:apply_effects", "effects": [
                               {"id": f"minecraft:{e}", "duration": d, "amplifier": a, "show_icon": True} for e, d, a in effets]}]}}


def talisman(nom, couleur, model, attrs, lore, uid):
    return {"id": BASE_RES, "nom": nom, "c": couleur, "lore": [lore, "Tenir en main secondaire."], "item_model": model,
            "uid": uid, "custom_data": {"rm": uid}, "max_stack": 1, "rarity": "epic", "glint": True,
            "attrs": [(a, v, op, "offhand") for a, v, op in attrs]}


def baton(rid, nom, couleur, model=None, lore=""):
    d = {"id": "minecraft:carrot_on_a_stick", "nom": nom, "c": couleur, "lore": [lore, "Clic droit pour l'utiliser."],
         "item_model": model or "minecraft:echo_shard", "glint": True, "unbreakable": True, "rarity": "epic",
         "custom_data": {"royaumes": rid}}
    return d


SCEAUX = {
    "nagash": baton("sceau_nagash", "Sceau de Nagash", "dark_purple", "minecraft:wither_skeleton_skull",
                    "Invoque le Grand Nécromancien. Que Sigmar vous garde."),
    "archaon": baton("sceau_archaon", "Sceau d'Archaon", "dark_red", "minecraft:ender_eye",
                     "Invoque l'Élu Éternel, Seigneur de la Fin des Temps."),
    "gordrakk": baton("sceau_gordrakk", "Totem de Gordrakk", "gold", "minecraft:goat_horn",
                      "Souffle dedans et le Poing de Gork arrive. WAAAGH !"),
    "skarbrand": baton("sceau_skarbrand", "Crâne de Skarbrand", "red", "minecraft:skeleton_skull",
                       "La rage de l'Exilé y bouillonne encore."),
    "thanquol": baton("sceau_thanquol", "Cloche de Thanquol", "green", "minecraft:bell",
                      "Son tintement attire le Grand Prophète et Boneripper."),
    "rotigus": baton("sceau_rotigus", "Calice de Rotigus", "dark_green", "minecraft:honey_bottle",
                     "Grand-Père Nurgle envoie son plus généreux enfant."),
}
PARCHEMIN = baton("parchemin", "Parchemin de Gloire", "yellow", "minecraft:paper", "+100 Gloire.")
PARCHEMIN["unbreakable"] = False

# (id, nom affiché, ingrédients, sorties)
RECETTES = [
    ("sigmarite", "Lingot de Sigmarite", [("minecraft:gold_ingot", 3), ("minecraft:lapis_lazuli", 2), ("res:eclat", 1)],
     [res_spec("sigmarite", 2)]),
    ("pierre", "Pierre de Royaume", [("res:eclat", 4), ("minecraft:ender_pearl", 1)], [B.PIERRE]),
    ("parchemin", "Parchemin de Gloire", [("res:eclat", 3), ("minecraft:paper", 1)], [PARCHEMIN]),
    # --- Panoplies d'alliance
    ("panoplie_sigmarite", "Panoplie de Sigmarite (Ordre)", [("res:sigmarite", 16), ("minecraft:diamond", 2)],
     armure("Armure des Stormcast Eternals", "diamond", ("gold", "sentry"),
            ["Heaume de Sigmarite", "Cuirasse de Sigmarite", "Jambières de Sigmarite", "Solerets de Sigmarite"],
            "gold", [("max_health", 2, "add_value")], "sigmarite")),
    ("panoplie_fleau", "Armure du Fléau Noir (Chaos)", [("res:chaos", 16), ("minecraft:netherite_scrap", 2)],
     armure("Forgée dans les Huit-Points", "netherite", ("redstone", "eye"),
            ["Heaume de l'Élu", "Plastron du Fléau", "Cuissards du Fléau", "Bottes du Fléau"],
            "dark_red", [("attack_damage", 0.5, "add_value")], "fleau")),
    ("panoplie_nadirite", "Armure de Nadirite (Mort)", [("res:ame", 16), ("minecraft:diamond", 2)],
     armure("Os et âmes liés par Nagash", "diamond", ("amethyst", "rib"),
            ["Heaume de Nadirite", "Ossature de Nadirite", "Grèves de Nadirite", "Pieds de Nadirite"],
            "dark_purple", [("knockback_resistance", 0.1, "add_value"), ("max_health", 1, "add_value")], "nadirite")),
    ("panoplie_ferraille", "Armure de Ferraille Ironjawz (Destruction)", [("res:ferraille", 16), ("res:ambre", 4)],
     armure("Plus y a de fer, plus c'est solide", "netherite", ("copper", "wild"),
            ["Casque de Kasse-Tête", "Plastron de Ferraille", "Jambières Kabossées", "Bottes de Krusheur"],
            "gold", [("knockback_resistance", 0.15, "add_value"), ("movement_speed", -0.02, "add_multiplied_base")], "ferraille")),
    # --- Armes légendaires d'artisan
    ("marteau_sigmar", "Marteau de Sigmar", [("res:sigmarite", 8), ("res:cristal", 2), ("minecraft:iron_block", 1)],
     [{"id": "minecraft:mace", "nom": "Marteau-Tonnerre de Sigmar", "c": "gold", "atk": (11, -3.2), "rarity": "epic",
       "ench": {"royaumes:foudre_de_sigmar": 1}, "lore": ["Ghal Maraz lui-même en serait jaloux."]}]),
    ("lame_demoniaque", "Lame Démoniaque", [("res:chaos", 8), ("res:braise", 2), ("minecraft:iron_block", 1)],
     [{"id": "minecraft:netherite_sword", "nom": "Lame Démoniaque", "c": "dark_red", "atk": (10, -2.4), "rarity": "epic",
       "ench": {"royaumes:flammes_de_tzeentch": 1, "minecraft:sharpness": 2}, "lore": ["Un démon y est enchaîné."]}]),
    ("faux_ame", "Faux des Âmes", [("res:ame", 8), ("res:ombre", 2), ("minecraft:iron_block", 1)],
     [{"id": "minecraft:netherite_hoe", "nom": "Faux des Âmes", "c": "dark_aqua", "atk": (10, -2.8), "rarity": "epic",
       "ench": {"royaumes:vol_d_ame": 2}, "lore": ["Chaque coup nourrit son porteur."]}]),
    ("choppa_gork", "Choppa de Gork", [("res:ferraille", 10), ("res:ambre", 3), ("minecraft:iron_block", 1)],
     [{"id": "minecraft:netherite_axe", "nom": "Choppa de Gork", "c": "gold", "atk": (12, -3.2), "rarity": "epic",
       "ench": {"royaumes:waaagh": 1, "minecraft:sharpness": 2}, "lore": ["Gork aime cogner fort."]}]),
    ("lame_malepierre", "Lame de Malepierre", [("res:malepierre", 6), ("minecraft:iron_sword", 1)],
     [{"id": "minecraft:iron_sword", "nom": "Lame de Malepierre Raffinée", "c": "green", "atk": (8, -2.2), "rarity": "rare",
       "ench": {"royaumes:malepierre": 1, "minecraft:sharpness": 2}}]),
    ("arc_hysh", "Arc de Lumière de Hysh", [("res:cristal", 6), ("minecraft:bow", 1)],
     [{"id": "minecraft:bow", "nom": "Arc de Lumière de Hysh", "c": "white", "rarity": "epic",
       "ench": {"minecraft:power": 4, "minecraft:infinity": 1}}]),
    ("hache_ur_or", "Hache d'Ur-Or", [("res:ur_or", 8), ("minecraft:gold_block", 1)],
     [{"id": "minecraft:golden_axe", "nom": "Hache Runique de Grimnir", "c": "gold", "atk": (11, -3.0), "unbreakable": True,
       "rarity": "epic", "ench": {"minecraft:fire_aspect": 2}}]),
    ("fusil_aether", "Fusil à Aether", [("res:aether_or", 8), ("minecraft:crossbow", 1)],
     [{"id": "minecraft:crossbow", "nom": "Grand Fusil à Aether", "c": "yellow", "rarity": "epic",
       "ench": {"minecraft:quick_charge": 2, "minecraft:piercing": 3}}]),
    # --- Consommables
    ("elixir_ghyran", "Élixir de Ghyran ×2", [("res:graine", 2), ("minecraft:glass_bottle", 2)],
     [dict(potion("Élixir de Ghyran", "green", "minecraft:honey_bottle", [("regeneration", 300, 1), ("instant_health", 1, 0)],
                  "La vie jaillit en vous.", "elixir_ghyran"), n=2)]),
    ("elixir_malepierre", "Élixir de Malepierre", [("res:malepierre", 1), ("minecraft:glass_bottle", 1)],
     [potion("Élixir de Malepierre", "green", "minecraft:experience_bottle", [("strength", 600, 1), ("wither", 60, 0)],
             "Force démesurée… et quelques effets secondaires.", "elixir_malepierre")]),
    ("tonique_aqshy", "Tonique d'Aqshy", [("res:braise", 2), ("minecraft:glass_bottle", 1)],
     [potion("Tonique d'Aqshy", "red", "minecraft:dragon_breath", [("fire_resistance", 3600, 0), ("strength", 600, 0)],
             "Brûlant, mais revigorant.", "tonique_aqshy")]),
    ("brume_ulgu", "Brume d'Ulgu", [("res:ombre", 2), ("minecraft:glass_bottle", 1)],
     [potion("Brume d'Ulgu", "dark_gray", "minecraft:ominous_bottle", [("invisibility", 1200, 0), ("speed", 1200, 1)],
             "Disparaissez dans les ombres.", "brume_ulgu")]),
    ("lumiere_hysh", "Lumière de Hysh", [("res:cristal", 2), ("minecraft:glass_bottle", 1)],
     [potion("Lumière de Hysh", "white", "minecraft:experience_bottle", [("night_vision", 6000, 0), ("haste", 3600, 1)],
             "Voyez tout, creusez tout.", "lumiere_hysh")]),
    ("festin_ogor", "Festin d'Ogor ×2", [("res:ambre", 1), ("minecraft:cooked_beef", 4)],
     [{"id": BASE_RES, "nom": "Festin d'Ogor", "c": "gold", "item_model": "minecraft:cooked_beef", "n": 2,
       "custom_data": {"rm": "festin"}, "lore": ["De quoi nourrir un Gutbuster."],
       "food": {"nutrition": 14, "saturation": 16.0, "can_always_eat": True},
       "consumable": {"consume_seconds": 2.4, "on_consume_effects": [{"type": "minecraft:apply_effects", "effects": [
           {"id": "minecraft:absorption", "duration": 1200, "amplifier": 2, "show_icon": True}]}]}}]),
    # --- Talismans
    ("talisman_grimnir", "Talisman de Grimnir", [("res:ur_or", 6), ("minecraft:gold_ingot", 2)],
     [talisman("Talisman de Grimnir", "gold", "minecraft:raw_gold", [("attack_damage", 2, "add_value")],
               "+2 dégâts", "talisman_grimnir")]),
    ("amulette_ambre", "Amulette d'Ambre", [("res:ambre", 6), ("minecraft:gold_ingot", 2)],
     [talisman("Amulette d'Ambre de Ghur", "gold", "minecraft:resin_clump", [("max_health", 6, "add_value")],
               "+3 cœurs", "amulette_ambre")]),
    ("pendentif_ombre", "Pendentif d'Ombre", [("res:ombre", 6), ("minecraft:gold_ingot", 2)],
     [talisman("Pendentif d'Ombre d'Ulgu", "dark_gray", "minecraft:ender_eye",
               [("movement_speed", 0.12, "add_multiplied_base"), ("sneaking_speed", 0.3, "add_value")],
               "+12 % vitesse", "pendentif_ombre")]),
    ("coeur_hysh", "Cœur de Cristal de Hysh", [("res:cristal", 6), ("minecraft:gold_ingot", 2)],
     [talisman("Cœur de Cristal de Hysh", "white", "minecraft:heart_of_the_sea",
               [("luck", 3, "add_value"), ("block_break_speed", 0.3, "add_multiplied_base")],
               "+3 chance, +30 % minage", "coeur_hysh")]),
    ("rune_sigmar", "Comète de Sigmar", [("res:sigmarite", 6), ("res:cristal", 2)],
     [talisman("Comète de Sigmar", "aqua", "minecraft:nether_star",
               [("armor", 4, "add_value"), ("max_health", 4, "add_value")], "+4 armure, +2 cœurs", "rune_sigmar")]),
    ("oeil_chaos", "Œil des Dieux Sombres", [("res:chaos", 6), ("res:malepierre", 2)],
     [talisman("Œil des Dieux Sombres", "dark_red", "minecraft:ender_eye",
               [("attack_damage", 3, "add_value"), ("max_health", -4, "add_value")], "+3 dégâts, -2 cœurs", "oeil_chaos")]),
    # --- Sceaux d'invocation de boss
    ("sceau_nagash", "Sceau de Nagash (boss)", [("res:ame", 24), ("res:eclat", 4)], [SCEAUX["nagash"]]),
    ("sceau_archaon", "Sceau d'Archaon (boss)", [("res:chaos", 24), ("res:eclat", 4)], [SCEAUX["archaon"]]),
    ("sceau_gordrakk", "Totem de Gordrakk (boss)", [("res:ferraille", 24), ("res:ambre", 8)], [SCEAUX["gordrakk"]]),
    ("sceau_skarbrand", "Crâne de Skarbrand (boss)", [("res:braise", 24), ("res:chaos", 4)], [SCEAUX["skarbrand"]]),
    ("sceau_thanquol", "Cloche de Thanquol (boss)", [("res:malepierre", 24), ("res:eclat", 4)], [SCEAUX["thanquol"]]),
    ("sceau_rotigus", "Calice de Rotigus (boss)", [("res:graine", 16), ("res:chaos", 8)], [SCEAUX["rotigus"]]),
]

# =========================================================================== BOSS
BOSS = {
    "nagash": dict(nom="Nagash, Dieu de la Mort", c="dark_purple", barre="purple", base="wither_skeleton", hp=900,
                   attrs={"attack_damage": 18, "scale": 2.6, "armor": 14, "knockback_resistance": 1.0,
                          "movement_speed": 0.26, "follow_range": 48},
                   equip={"armor.head": eq("minecraft:golden_helmet", trim=("amethyst", "silence"), unbreakable=True),
                          "armor.chest": eq("minecraft:netherite_chestplate", trim=("amethyst", "silence")),
                          "armor.legs": eq("minecraft:netherite_leggings", trim=("amethyst", "silence")),
                          "weapon.mainhand": eq("minecraft:netherite_hoe", item_model="minecraft:blaze_rod"),
                          "weapon.offhand": eq("minecraft:netherite_sword")},
                   biome="shyish_terres", invoc=("skeleton", "deathrattle"), invoc2=("zombie", "chainrasp"),
                   annonce="« Tout ce qui vit m'appartient. »"),
    "archaon": dict(nom="Archaon, l'Élu Éternel", c="dark_red", barre="red", base="zombie", hp=1000,
                    attrs={"attack_damage": 20, "scale": 2.4, "armor": 18, "knockback_resistance": 1.0,
                           "movement_speed": 0.27, "follow_range": 48},
                    equip={"armor.head": eq("minecraft:netherite_helmet", trim=("redstone", "eye"), unbreakable=True),
                           "armor.chest": eq("minecraft:netherite_chestplate", trim=("gold", "eye")),
                           "armor.legs": eq("minecraft:netherite_leggings", trim=("redstone", "eye")),
                           "armor.feet": eq("minecraft:netherite_boots", trim=("redstone", "eye")),
                           "weapon.mainhand": eq("minecraft:netherite_sword", ench={"minecraft:sharpness": 5}),
                           "weapon.offhand": eq("minecraft:shield")},
                    biome="chaos_desolation", invoc=("zombie", "chaos_guerrier"), invoc2=("skeleton", "tzaangor"),
                    annonce="« Je suis la Fin des Temps. »"),
    "gordrakk": dict(nom="Gordrakk, le Poing de Gork", c="gold", barre="yellow", base="zombie", hp=800,
                     attrs={"attack_damage": 19, "scale": 2.6, "armor": 14, "knockback_resistance": 1.0,
                            "movement_speed": 0.27, "follow_range": 48},
                     equip={"armor.head": eq("minecraft:netherite_helmet", trim=("copper", "wild"), unbreakable=True),
                            "armor.chest": eq("minecraft:netherite_chestplate", trim=("copper", "wild")),
                            "armor.legs": eq("minecraft:iron_leggings", trim=("copper", "wild")),
                            "weapon.mainhand": eq("minecraft:netherite_axe"), "weapon.offhand": eq("minecraft:iron_axe")},
                     biome="ghur_terres", invoc=("zombie", "brute"), invoc2=("zombie", "brute"),
                     annonce="« WAAAAAGH ! »"),
    "skarbrand": dict(nom="Skarbrand, l'Exilé", c="red", barre="red", base="piglin_brute", hp=850,
                      attrs={"attack_damage": 22, "scale": 2.8, "armor": 10, "knockback_resistance": 1.0,
                             "movement_speed": 0.3, "follow_range": 48},
                      equip={"armor.chest": eq("minecraft:netherite_chestplate", trim=("gold", "rib")),
                             "weapon.mainhand": eq("minecraft:netherite_axe", ench={"minecraft:fire_aspect": 2}),
                             "weapon.offhand": eq("minecraft:netherite_axe")},
                      biome="aqshy_cendres", invoc=("zombie", "bloodreaver"), invoc2=("zombie", "bloodreaver"),
                      annonce="« DU SANG ! DU SANG POUR KHORNE ! »",
                      extra=['data modify entity @s IsImmuneToZombification set value 1b']),
    "thanquol": dict(nom="Thanquol & Boneripper", c="green", barre="green", base="ravager", hp=750,
                     attrs={"attack_damage": 16, "scale": 1.6, "armor": 12, "knockback_resistance": 1.0,
                            "movement_speed": 0.32, "follow_range": 48},
                     equip={}, biome="terres_rongees", invoc=("zombie", "clanrat"), invoc2=("skeleton", "jezzail"),
                     annonce="« Tuez-les ! Tuez-les tous, idiots-idiots ! »",
                     extra=['summon minecraft:zombie ~ ~2 ~ {Tags:["rm_spawn","rm_p_thanquol_cavalier","rm_monture"],PersistenceRequired:1b}',
                            'ride @e[tag=rm_monture,limit=1,sort=nearest] mount @s',
                            'tag @e[tag=rm_monture] remove rm_monture']),
    "rotigus": dict(nom="Rotigus, le Pluvieux", c="dark_green", barre="green", base="zombie", hp=950,
                    attrs={"attack_damage": 16, "scale": 3.2, "armor": 8, "knockback_resistance": 1.0,
                           "movement_speed": 0.2, "follow_range": 48},
                    equip={"armor.chest": eq("minecraft:leather_chestplate", dye=C["putride"], trim=("resin", "host")),
                           "armor.legs": eq("minecraft:leather_leggings", dye=C["putride"]),
                           "armor.head": eq("minecraft:leather_helmet", dye=C["putride"], unbreakable=True),
                           "weapon.mainhand": eq("minecraft:wooden_shovel", item_model="minecraft:stick")},
                    biome="ghyran_marais", invoc=("zombie", "pestigor"), invoc2=("zombie", "pestigor"),
                    annonce="« Mes enfants, recevez la bénédiction de Grand-Père ! »"),
}

# Trophées légendaires
TROPHEES = {
    "nagash": [{"id": "minecraft:netherite_hoe", "nom": "Alakanash, Bâton de Nagash", "c": "dark_purple", "atk": (15, -2.6),
                "item_model": "minecraft:blaze_rod", "unbreakable": True, "rarity": "epic",
                "ench": {"royaumes:vol_d_ame": 2, "royaumes:malepierre": 1}, "lore": ["Le bâton du Grand Nécromancien."]},
               {"id": "minecraft:golden_helmet", "nom": "Couronne de Nagash", "c": "dark_purple", "unbreakable": True,
                "rarity": "epic", "trim": ("amethyst", "silence"), "uid": "couronne",
                "attrs": [("armor", 5, "add_value", "head"), ("max_health", 10, "add_value", "head"),
                          ("armor_toughness", 3, "add_value", "head")]}],
    "archaon": [{"id": "minecraft:netherite_sword", "nom": "Tueuse de Rois", "c": "dark_red", "atk": (17, -2.4),
                 "unbreakable": True, "rarity": "epic", "ench": {"minecraft:sharpness": 5, "royaumes:flammes_de_tzeentch": 1},
                 "lore": ["Un démon y est lié : U'zuhl le Dévoreur."]}],
    "gordrakk": [{"id": "minecraft:netherite_axe", "nom": "Smasha", "c": "gold", "atk": (18, -3.0), "unbreakable": True,
                  "rarity": "epic", "ench": {"royaumes:waaagh": 1, "minecraft:sharpness": 4}},
                 {"id": "minecraft:netherite_axe", "nom": "Kunnin'", "c": "gold", "atk": (14, -2.6), "unbreakable": True,
                  "rarity": "epic", "ench": {"royaumes:peste": 2, "minecraft:sharpness": 3}}],
    "skarbrand": [{"id": "minecraft:netherite_axe", "nom": "Massacre", "c": "red", "atk": (19, -3.0), "unbreakable": True,
                   "rarity": "epic", "ench": {"minecraft:fire_aspect": 3, "minecraft:sharpness": 4}}],
    "thanquol": [{"id": "minecraft:netherite_hoe", "nom": "Bâton de Malefoudre", "c": "green", "atk": (13, -2.4),
                  "item_model": "minecraft:blaze_rod", "unbreakable": True, "rarity": "epic",
                  "ench": {"royaumes:foudre_de_sigmar": 1, "royaumes:malepierre": 1}}],
    "rotigus": [{"id": "minecraft:netherite_shovel", "nom": "Bâton de Pluie Pestilentielle", "c": "dark_green",
                 "atk": (14, -2.8), "item_model": "minecraft:stick", "unbreakable": True, "rarity": "epic",
                 "ench": {"royaumes:peste": 2, "royaumes:vol_d_ame": 1}},
                {"id": BASE_RES, "nom": "Cloche de Pluie", "c": "dark_green", "item_model": "minecraft:bell",
                 "custom_data": {"rm": "cloche_pluie"}, "max_stack": 1, "rarity": "epic", "uid": "cloche_pluie",
                 "attrs": [("max_health", 8, "add_value", "offhand"), ("armor", 2, "add_value", "offhand")],
                 "lore": ["Talisman : +4 cœurs, +2 armure", "Tenir en main secondaire."]}],
}
RES_BOSS = {"nagash": "ame", "archaon": "chaos", "gordrakk": "ferraille", "skarbrand": "braise",
            "thanquol": "malepierre", "rotigus": "graine"}


def preparer():
    """Ajoute les profils de boss et les tables de butin aux profils existants (avant gen_mobs)."""
    for pid in RES_PROFIL:
        PROFILS[pid]["loot"] = f"{NS}:mobs/{pid}"
    for bid, b in BOSS.items():
        PROFILS[f"boss_{bid}"] = dict(
            id=f"boss_{bid}", nom=b["nom"], c=b["c"], alliance="chaos", base=b["base"], equip=b["equip"],
            attrs=dict(max_health=b["hp"], **b["attrs"]), effets=[], bebe=False, team="rm_boss",
            loot=f"{NS}:boss/{bid}",
            extra=[f"tag @s add rm_boss", f"tag @s add rm_boss_{bid}", "data modify entity @s PersistenceRequired set value 1b",
                   'data modify entity @s CustomNameVisible set value 1b',
                   f"tellraw @a[distance=..96] {jtxt(txt('☠ ', b['c']), txt(b['nom'], b['c'], bold=True), txt(' ' + b['annonce'], 'gray', italic=True))}",
                   "playsound minecraft:entity.wither.spawn hostile @a[distance=..96] ~ ~ ~ 2 0.6"] + b.get("extra", []))
    PROFILS["thanquol_cavalier"] = dict(
        id="thanquol_cavalier", nom="Grand Prophète Thanquol", c="green", alliance="chaos", base="zombie",
        equip={"armor.chest": eq("minecraft:leather_chestplate", dye=C["gris"], trim=("emerald", "snout")),
               "armor.head": eq("minecraft:leather_helmet", dye=C["gris"], unbreakable=True),
               "weapon.mainhand": eq("minecraft:blaze_rod")},
        attrs={"max_health": 120, "attack_damage": 8, "scale": 0.9}, effets=[], bebe=False, team="rm_boss",
        loot=f"{NS}:mobs/clanrat", extra=["data modify entity @s PersistenceRequired set value 1b"])


# =========================================================================== GÉNÉRATION
def gen_loot():
    def base_pools(base):
        p = f"{B.VANILLA}/loot_table/entities/{base}.json"
        if not os.path.exists(p):
            return []
        return json.load(open(p))["pools"]

    killed = {"type": "minecraft:killed_by_player"}

    def chance(c):
        return {"type": "minecraft:all_of", "terms": [killed, {"type": "minecraft:random_chance", "chance": c}]}

    for pid, rid in RES_PROFIL.items():
        p = PROFILS[pid]
        elite = pid in ELITES
        pools = base_pools(p["base"])
        pools.append({"rolls": 1, "condition": chance(0.6 if elite else 0.3), "entries": [entry(res_spec("eclat"), n=(1, 2))]})
        pools.append({"rolls": 1, "condition": chance(1.0 if elite else 0.45),
                      "entries": [entry(res_spec(rid), n=(2, 5) if elite else (1, 2))]})
        if elite:
            pools.append({"rolls": 1, "condition": chance(0.5), "entries": [entry({"id": "minecraft:diamond"}, n=(1, 3))]})
        w(f"data/{NS}/loot_table/mobs/{pid}.json", {"type": "minecraft:entity", "pools": pools})
    for bid in BOSS:
        pools = [{"rolls": 1, "entries": [entry(t)]} for t in TROPHEES[bid]]
        pools += [{"rolls": 1, "entries": [entry(res_spec(RES_BOSS[bid]), n=(12, 20))]},
                  {"rolls": 1, "entries": [entry(res_spec("eclat"), n=(6, 10))]},
                  {"rolls": 1, "entries": [entry({"id": "minecraft:diamond"}, n=(4, 8))]},
                  {"rolls": 1, "entries": [entry({"id": "minecraft:netherite_scrap"}, n=(1, 3))]},
                  {"rolls": 1, "entries": [entry({"id": "minecraft:experience_bottle"}, n=(16, 32))]},
                  {"rolls": 1, "entries": [entry(PARCHEMIN, n=3)]}]
        w(f"data/{NS}/loot_table/boss/{bid}.json", {"type": "minecraft:entity", "pools": pools})
    # Blocs des Royaumes qui donnent des ressources
    def loc(dim=None, biome=None):
        pr = {}
        if dim:
            pr["dimension"] = dim
        if biome:
            pr["biomes"] = f"{NS}:{biome}"
        return {"type": "minecraft:location_check", "predicate": pr}

    blocs = [
        ("verdant_froglight", "malepierre", (1, 3), 1.0, loc(dim=DIM)),
        ("raw_gold_block", "aether_or", (2, 4), 1.0, loc(biome="chamon_desert")),
        ("magma_block", "braise", (1, 1), 0.35, loc(biome="aqshy_cendres")),
        ("bone_block", "ame", (1, 1), 0.35, loc(biome="shyish_terres")),
        ("crying_obsidian", "chaos", (1, 2), 0.6, loc(dim=DIM)),
        ("calcite", "cristal", (1, 1), 0.12, loc(biome="hysh_plateaux")),
        ("flowering_azalea_leaves", "graine", (1, 1), 0.08, loc(biome="ghyran_jade")),
        ("gold_ore", "ur_or", (1, 1), 0.5, loc(dim=DIM)),
        ("deepslate_gold_ore", "ur_or", (1, 2), 0.5, loc(dim=DIM)),
        ("amethyst_cluster", "eclat", (1, 2), 0.5, loc(dim=DIM)),
    ]
    for bloc, rid, n, ch, cond in blocs:
        v = json.load(open(f"{B.VANILLA}/loot_table/blocks/{bloc}.json"))
        v.pop("random_sequence", None)
        terms = [cond, {"type": "minecraft:survives_explosion"}]
        if ch < 1:
            terms.append({"type": "minecraft:random_chance", "chance": ch})
        v["pools"].append({"rolls": 1, "condition": {"type": "minecraft:all_of", "terms": terms},
                           "entries": [entry(res_spec(rid), n=n)]})
        w(f"data/minecraft/loot_table/blocks/{bloc}.json", v)
    # Ressources dans les coffres des structures
    import glob
    for p in glob.glob(f"{OUT}/data/{NS}/loot_table/coffres/*.json"):
        d = json.load(open(p))
        d["pools"].append({"rolls": {"type": "minecraft:uniform", "min": 1, "max": 3},
                           "entries": [entry(res_spec(r), weight=(6 if r == "eclat" else 2), n=(1, 4)) for r in RES]})
        d["pools"].append({"rolls": 1, "entries": [entry(PARCHEMIN, weight=1), {"type": "minecraft:empty", "weight": 4}]})
        json.dump(d, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=2)


def gen_forge():
    lines_essai = []
    for rid, nom, ings, outs in RECETTES:
        L = []
        nbts = []
        for ing, n in ings:
            nbt = res_nbt(ing[4:]) if ing.startswith("res:") else '{Item:{id:"%s"}}' % ing
            sel = f"@e[type=minecraft:item,distance=..1.5,nbt={nbt},limit=1]"
            nbts.append((sel, n))
            L.append(f"execute unless entity {sel} run return 0")
            L.append(f"execute store result score #c rm_tmp run data get entity {sel} Item.count")
            L.append(f"execute if score #c rm_tmp matches ..{n - 1} run return 0")
        for sel, n in nbts:
            L.append(f"execute as {sel} run function {NS}:forge/retirer {{n:{n}}}")
        L += [f"loot spawn ~ ~0.6 ~ loot {NS}:forge/{rid}",
              "particle minecraft:lava ~ ~0.8 ~ 0.3 0.3 0.3 0 12",
              "particle minecraft:enchant ~ ~1 ~ 0.4 0.6 0.4 0.5 40",
              "playsound minecraft:block.anvil.use block @a[distance=..16] ~ ~ ~ 1 0.9",
              "playsound minecraft:block.smithing_table.use block @a[distance=..16] ~ ~ ~ 1 1",
              f"tellraw @a[distance=..8] {jtxt(txt('⚒ Forgé : ', 'gold'), txt(nom, 'yellow'))}",
              "scoreboard players set #gain rm_tmp 5",
              f"execute as @p[distance=..8] run function {NS}:rpg/ajouter",
              "return 1"]
        fn(f"forge/r/{rid}", L)
        w(f"data/{NS}/loot_table/forge/{rid}.json", {"pools": [{"rolls": 1, "entries": [entry(o)]} for o in outs]})
        lines_essai.append(f"execute if function {NS}:forge/r/{rid} run return 1")
    fn("forge/essayer", lines_essai + ["return 0"])
    fn("forge/retirer", ["$scoreboard players set #r rm_tmp $(n)",
                         "execute store result score #c rm_tmp run data get entity @s Item.count",
                         "scoreboard players operation #c rm_tmp -= #r rm_tmp",
                         "execute store result entity @s Item.count int 1 run scoreboard players get #c rm_tmp",
                         "execute if score #c rm_tmp matches ..0 run kill @s"])
    fn("forge/boucle", [f"schedule function {NS}:forge/boucle 10t replace",
                        "execute as @e[type=minecraft:item] at @s if block ~ ~-0.3 ~ minecraft:smithing_table "
                        f"run function {NS}:forge/essayer"])
    # Livre de recettes (dialogue)
    contenus = [{"text": "Posez une Table de forgeron, puis lâchez-y (touche Q) les ingrédients. "
                         "Ils fusionnent automatiquement.\n\n", "color": "gray"}]
    for rid, nom, ings, outs in RECETTES:
        parts = []
        for ing, n in ings:
            nm = RES[ing[4:]][0] if ing.startswith("res:") else ing.split(":")[1].replace("_", " ")
            parts.append(f"{n} {nm}")
        contenus.append({"text": "• " + nom, "color": "gold"})
        contenus.append({"text": " : " + ", ".join(parts) + "\n", "color": "white"})
    w(f"data/{NS}/dialog/forge.json", {
        "type": "minecraft:notice", "title": {"text": "⚒ Forge des Royaumes", "color": "gold", "bold": True},
        "external_title": {"text": "Forge des Royaumes", "color": "gold"},
        "body": [{"type": "minecraft:plain_message", "width": 400, "contents": contenus}],
        "action": {"label": {"text": "Fermer"}, "width": 100}})
    res_txt = [{"text": "Où trouver les ressources :\n\n", "color": "gray"}]
    sources = {
        "eclat": "tous les guerriers de faction, améthyste des Royaumes",
        "sigmarite": "Stormcast (Azyr) ; ou Forge : or + lapis + éclat", "malepierre": "Skaven ; blocs de malepierre verts",
        "ur_or": "Fyreslayers ; minerai d'or des Royaumes", "aether_or": "Kharadron ; or brut de Chamon",
        "ame": "morts-vivants de Shyish ; blocs d'os de Shyish", "braise": "Khorne et Hashut ; magma d'Aqshy",
        "ambre": "Seraphon, Ogors, Gargants", "graine": "Sylvaneth, Nurgle ; azalées de Ghyran",
        "ombre": "Filles de Khaine, Idoneth, Gitz", "cristal": "Lumineth ; calcite de Hysh",
        "chaos": "Guerriers du Chaos ; obsidienne pleureuse", "ferraille": "Ironjawz et Kruleboyz"}
    for r, (nom, c, _, _) in RES.items():
        res_txt += [{"text": "• " + nom, "color": c}, {"text": " — " + sources.get(r, "minerai de lapis des Cimes d'Azyr") + "\n", "color": "white"}]
    w(f"data/{NS}/dialog/ressources.json", {
        "type": "minecraft:notice", "title": {"text": "Ressources des Royaumes", "color": "light_purple", "bold": True},
        "external_title": {"text": "Ressources des Royaumes", "color": "light_purple"},
        "body": [{"type": "minecraft:plain_message", "width": 400, "contents": res_txt}],
        "action": {"label": {"text": "Fermer"}, "width": 100}})


# =========================================================================== RPG
SKILLS = [  # (id, nom, couleur, description, [(attribut, valeur par rang, opération)])
    ("vigueur", "Vigueur", "red", "+1 cœur par rang", [("max_health", 2, "add_value")]),
    ("force", "Force", "dark_red", "+0,6 dégât par rang", [("attack_damage", 0.6, "add_value")]),
    ("agilite", "Agilité", "aqua", "+2,5 % vitesse, +3 % vitesse d'attaque",
     [("movement_speed", 0.025, "add_multiplied_base"), ("attack_speed", 0.03, "add_multiplied_base")]),
    ("mineur", "Mineur", "gray", "+15 % vitesse de minage par rang",
     [("block_break_speed", 0.15, "add_multiplied_base"), ("submerged_mining_speed", 0.1, "add_value")]),
    ("endurance", "Endurance", "dark_green", "+1 armure, +0,5 robustesse, +3 % anti-recul",
     [("armor", 1, "add_value"), ("armor_toughness", 0.5, "add_value"), ("knockback_resistance", 0.03, "add_value")]),
    ("fortune", "Fortune", "gold", "+0,5 chance (meilleur butin)", [("luck", 0.5, "add_value")]),
]
RANG_MAX = 10
NIVEAU_MAX = 61

MINERAIS = [("coal_ore", 2), ("deepslate_coal_ore", 2), ("copper_ore", 2), ("deepslate_copper_ore", 2),
            ("iron_ore", 3), ("deepslate_iron_ore", 3), ("gold_ore", 5), ("deepslate_gold_ore", 5),
            ("redstone_ore", 3), ("deepslate_redstone_ore", 3), ("lapis_ore", 4), ("deepslate_lapis_ore", 4),
            ("diamond_ore", 15), ("deepslate_diamond_ore", 15), ("emerald_ore", 15), ("deepslate_emerald_ore", 15),
            ("nether_gold_ore", 3), ("nether_quartz_ore", 2), ("ancient_debris", 30),
            ("verdant_froglight", 6), ("raw_gold_block", 6), ("crying_obsidian", 5), ("amethyst_cluster", 3)]
KILLS = [("rm_k_mob", "minecraft.custom:minecraft.mob_kills", 2), ("rm_k_or", "teamkill.gold", 8),
         ("rm_k_cr", "teamkill.dark_red", 8), ("rm_k_dp", "teamkill.dark_purple", 8),
         ("rm_k_dg", "teamkill.dark_green", 8), ("rm_k_boss", "teamkill.red", 500)]


def gen_rpg():
    L = ["scoreboard objectives add rm_gloire dummy", "scoreboard objectives add rm_besoin dummy",
         f"scoreboard objectives add rm_niveau dummy {jtxt(txt('Niv.', 'gold'))}",
         "scoreboard objectives add rm_pts dummy", "scoreboard objectives add rm_comp trigger",
         "scoreboard objectives add rm_rpg trigger", "scoreboard objectives add rm_forge trigger",
         "scoreboard objectives add rm_bt dummy",
         "scoreboard objectives setdisplay list rm_niveau", "scoreboard objectives setdisplay below_name rm_niveau",
         "scoreboard players set #20 rm_const 20", "scoreboard players set #40 rm_const 40",
         "team add rm_boss " + jtxt(txt("Boss", "red")), "team modify rm_boss color red",
         "team modify rm_boss friendlyFire false"]
    for sk, *_ in SKILLS:
        L.append(f"scoreboard objectives add rm_{sk} dummy")
    for i, (b, _) in enumerate(MINERAIS):
        L.append(f"scoreboard objectives add rm_m{i} minecraft.mined:minecraft.{b}")
    for o, crit, _ in KILLS:
        L.append(f"scoreboard objectives add {o} {crit}")
    for i in range(1, len(BIOMES) + 1):
        L.append(f"scoreboard objectives add rm_bd{i} dummy")
    for bid, b in BOSS.items():
        L += [f"bossbar add {NS}:{bid} {jtxt(txt(b['nom'], b['c'], bold=True))}",
              f"bossbar set {NS}:{bid} color {b['barre']}", f"bossbar set {NS}:{bid} style notched_10",
              f"bossbar set {NS}:{bid} max {b['hp']}"]
    L.append(f"schedule function {NS}:forge/boucle 10t replace")
    fn("rpg/load", L)

    fn("rpg/init", ["scoreboard players set @s rm_niveau 1", "scoreboard players set @s rm_gloire 0",
                    "scoreboard players set @s rm_pts 0"] + [f"scoreboard players set @s rm_{sk} 0" for sk, *_ in SKILLS]
       + ["function royaumes:rpg/besoin"])
    fn("rpg/besoin", ["scoreboard players operation @s rm_besoin = @s rm_niveau",
                      "scoreboard players operation @s rm_besoin *= #20 rm_const",
                      "scoreboard players operation @s rm_besoin += #40 rm_const"])
    fn("rpg/ajouter", [
        f"execute if score @s rm_niveau matches {NIVEAU_MAX}.. run return 0",
        "scoreboard players operation @s rm_gloire += #gain rm_tmp",
        f"function {NS}:rpg/verifier",
        "title @s actionbar " + jtxt(txt("+", "gold"), {"score": {"name": "#gain", "objective": "rm_tmp"}, "color": "gold"},
                                     txt(" Gloire   ", "gold"), txt("Niv. ", "gray"),
                                     {"score": {"name": "@s", "objective": "rm_niveau"}, "color": "yellow"},
                                     txt("  (", "gray"), {"score": {"name": "@s", "objective": "rm_gloire"}, "color": "gray"},
                                     txt("/", "gray"), {"score": {"name": "@s", "objective": "rm_besoin"}, "color": "gray"},
                                     txt(")", "gray"))])
    fn("rpg/verifier", [f"function {NS}:rpg/besoin",
                        f"execute if score @s rm_niveau matches {NIVEAU_MAX}.. run return 0",
                        f"execute if score @s rm_gloire >= @s rm_besoin run function {NS}:rpg/niveau_sup"])
    fn("rpg/niveau_sup", [
        "scoreboard players operation @s rm_gloire -= @s rm_besoin",
        "scoreboard players add @s rm_niveau 1", "scoreboard players add @s rm_pts 1",
        "title @s times 5 40 15",
        "title @s title " + jtxt(txt("NIVEAU ", "gold", bold=True), {"score": {"name": "@s", "objective": "rm_niveau"}, "color": "yellow", "bold": True}),
        "title @s subtitle " + jtxt(txt("+1 point de compétence", "green")),
        "playsound minecraft:entity.player.levelup player @s ~ ~ ~ 1 0.8",
        "playsound minecraft:ui.toast.challenge_complete player @s ~ ~ ~ 0.6 1.2",
        "execute at @s run particle minecraft:totem_of_undying ~ ~1 ~ 0.5 1 0.5 0.4 60",
        "tellraw @s " + jtxt(txt("★ Niveau ", "gold"), {"score": {"name": "@s", "objective": "rm_niveau"}, "color": "yellow"},
                             txt(" atteint ! ", "gold"), txt("[Dépenser mes points]", "green", underlined=True,
                                                             click_event={"action": "run_command", "command": "/trigger rm_rpg"})),
        f"function {NS}:rpg/verifier"])
    # Compétences
    for i, (sk, nom, c, desc, mods) in enumerate(SKILLS, start=1):
        for r in range(RANG_MAX + 1):
            lines = []
            for a, v, op in mods:
                lines.append(f"attribute @s minecraft:{a} modifier remove {NS}:rpg_{sk}")
                if r:
                    lines.append(f"attribute @s minecraft:{a} modifier add {NS}:rpg_{sk} {round(v * r, 4)} {op}")
            fn(f"rpg/rang/{sk}/{r}", lines)
        fn(f"rpg/monter/{sk}", [
            "execute unless score @s rm_pts matches 1.. run return run tellraw @s " + jtxt(txt("Aucun point de compétence disponible.", "red")),
            f"execute if score @s rm_{sk} matches {RANG_MAX}.. run return run tellraw @s " + jtxt(txt(nom + " est déjà au maximum.", "red")),
            f"scoreboard players add @s rm_{sk} 1", "scoreboard players remove @s rm_pts 1",
            f"function {NS}:rpg/appliquer/{sk}",
            "playsound minecraft:block.enchantment_table.use player @s ~ ~ ~ 1 1.2",
            "tellraw @s " + jtxt(txt("✦ " + nom + " → rang ", c), {"score": {"name": "@s", "objective": f"rm_{sk}"}, "color": c})])
        fn(f"rpg/appliquer/{sk}", [f"execute if score @s rm_{sk} matches {r} run function {NS}:rpg/rang/{sk}/{r}"
                                    for r in range(RANG_MAX + 1)])
    # Maintien après la mort (ajout seulement, jamais retrait)
    L = []
    for sk, nom, c, desc, mods in SKILLS:
        for r in range(1, RANG_MAX + 1):
            for a, v, op in mods:
                L.append(f"execute if score @s rm_{sk} matches {r} run attribute @s minecraft:{a} modifier add {NS}:rpg_{sk} {round(v * r, 4)} {op}")
    fn("rpg/maintenir", L)
    lines = ["scoreboard players set @s rm_comp 0", "scoreboard players enable @s rm_comp"]
    for i, (sk, *_ ) in enumerate(SKILLS, start=1):
        lines.insert(0, f"execute if score @s rm_comp matches {i} run function {NS}:rpg/monter/{sk}")
    lines.append(f"function {NS}:rpg/fiche")
    fn("rpg/depenser", lines)
    # Fiche du héros
    stats = [txt("\n══ Fiche du Héros ══\n", "gold", bold=True), txt("Niveau ", "gray"),
             {"score": {"name": "@s", "objective": "rm_niveau"}, "color": "yellow"}, txt("   Gloire ", "gray"),
             {"score": {"name": "@s", "objective": "rm_gloire"}, "color": "gold"}, txt("/", "gray"),
             {"score": {"name": "@s", "objective": "rm_besoin"}, "color": "gold"}, txt("   Points : ", "gray"),
             {"score": {"name": "@s", "objective": "rm_pts"}, "color": "green"}, txt("\n")]
    for sk, nom, c, desc, mods in SKILLS:
        stats += [txt(f"{nom} ", c), {"score": {"name": "@s", "objective": f"rm_{sk}"}, "color": "white"},
                  txt(f"/{RANG_MAX}  ", "gray")]
    fn("rpg/fiche", ["scoreboard players enable @s rm_comp", "tellraw @s " + jtxt(*stats), f"dialog show @s {NS}:fiche"])
    w(f"data/{NS}/dialog/fiche.json", {
        "type": "minecraft:multi_action",
        "title": {"text": "Fiche du Héros — Compétences", "color": "gold", "bold": True},
        "external_title": {"text": "Fiche du Héros", "color": "gold"},
        "body": [{"type": "minecraft:plain_message", "width": 320, "contents": [
            {"text": "Chaque niveau donne 1 point de compétence (max. 10 rangs par compétence).\n"
                     "Ta Gloire vient des combats, des boss, du minage, de la forge et de l'exploration.\n"
                     "Tes statistiques actuelles sont affichées dans le tchat.", "color": "gray"}]}],
        "can_close_with_escape": True, "pause": False, "columns": 2,
        "actions": [{"label": {"text": f"{nom}", "color": c, "bold": True}, "tooltip": {"text": desc}, "width": 150,
                     "action": {"type": "run_command", "command": f"trigger rm_comp set {i}"}}
                    for i, (sk, nom, c, desc, _) in enumerate(SKILLS, start=1)],
        "exit_action": {"label": {"text": "Fermer"}, "width": 100}})
    # Sources de Gloire (boucle chaque seconde)
    L = ["execute as @a unless score @s rm_niveau matches 1.. run function royaumes:rpg/init"]
    for i, (b, g) in enumerate(MINERAIS):
        L.append(f"execute as @a[scores={{rm_m{i}=1..}}] run function {NS}:rpg/source {{obj:\"rm_m{i}\",val:{g}}}")
    for o, crit, g in KILLS:
        L.append(f"execute as @a[scores={{{o}=1..}}] run function {NS}:rpg/source {{obj:\"{o}\",val:{g}}}")
    L += [f"execute as @a[scores={{rm_rpg=1..}}] run function {NS}:rpg/ouvrir",
          f"execute as @a[scores={{rm_comp=1..}}] run function {NS}:rpg/depenser",
          f"execute as @a[scores={{rm_forge=1..}}] run function {NS}:forge/ouvrir",
          "scoreboard players enable @a rm_rpg", "scoreboard players enable @a rm_forge"]
    fn("rpg/boucle", L)
    fn("rpg/source", ["$scoreboard players operation #n rm_tmp = @s $(obj)",
                      "$scoreboard players set @s $(obj) 0",
                      "$scoreboard players set #v rm_tmp $(val)",
                      "scoreboard players operation #n rm_tmp *= #v rm_tmp",
                      "scoreboard players operation #gain rm_tmp = #n rm_tmp",
                      f"function {NS}:rpg/ajouter"])
    fn("rpg/ouvrir", ["scoreboard players set @s rm_rpg 0", f"function {NS}:rpg/fiche"])
    fn("forge/ouvrir", ["scoreboard players set @s rm_forge 0", f"dialog show @s {NS}:forge"])
    # Découverte des biomes (+30 Gloire)
    L = []
    for i, b in enumerate(BIOMES, start=1):
        L.append(f"execute if score @s rm_bnow matches {i} unless score @s rm_bd{i} matches 1 run function {NS}:rpg/decouverte {{i:{i}}}")
    fn("rpg/decouvrir", L)
    fn("rpg/decouverte", ["$scoreboard players set @s rm_bd$(i) 1",
                          "tellraw @s " + jtxt(txt("✧ Nouvelle région découverte ! ", "aqua"), txt("+30 Gloire", "gold")),
                          "scoreboard players set #gain rm_tmp 30", f"function {NS}:rpg/ajouter"])
    w("data/minecraft/tags/dialog/quick_actions.json", {"replace": False, "values": [
        f"{NS}:codex", f"{NS}:fiche", f"{NS}:forge", f"{NS}:ressources"]})


# =========================================================================== BOSS : capacités
def gen_boss():
    for bid, b in BOSS.items():
        half = b["hp"] // 2
        sel_j = "@a[distance=..12,gamemode=!spectator,gamemode=!creative]"
        sel_p = "@a[distance=..28,gamemode=!spectator,gamemode=!creative]"
        fn(f"boss/{bid}/tick", [
            f"execute store result bossbar {NS}:{bid} value run data get entity @s Health",
            f"bossbar set {NS}:{bid} players @a[distance=..56]",
            f"execute unless entity {sel_p} run return 0",
            "scoreboard players add @s rm_bt 1",
            "execute store result score #hp rm_tmp run data get entity @s Health",
            f"execute if entity @s[tag=!rm_phase2] if score #hp rm_tmp matches ..{half} run function {NS}:boss/{bid}/phase2",
            f"execute if entity @s[tag=rm_phase2] if score @s rm_bt matches 4.. run function {NS}:boss/{bid}/attaque",
            f"execute if score @s rm_bt matches 6.. run function {NS}:boss/{bid}/attaque"])
        inv1, inv2 = b["invoc"], b["invoc2"]
        sbire = {"deathrattle": "deathrattle", "chainrasp": "chainrasp", "chaos_guerrier": "guerrier_chaos",
                 "brute": "brute", "bloodreaver": "bloodreaver", "clanrat": "clanrat", "pestigor": "plaguebearer",
                 "chaos_seigneur": "chosen", "gutrippa": "gutrippa", "jezzail": "jezzail", "tzaangor": "tzaangor"}
        m1, m2 = sbire.get(inv1[1], "guerrier_chaos"), sbire.get(inv2[1], "guerrier_chaos")
        invoc = [f'summon {NS}:{m1} ~2 ~ ~2', f'summon {NS}:{m1} ~-2 ~ ~-2', f'summon {NS}:{m2} ~2 ~ ~-2']
        cap = {  # 3 capacités par boss
            "nagash": [
                ("Invocation des Morts", invoc + ["particle minecraft:soul ~ ~1 ~ 3 1 3 0.05 120",
                                                   "playsound minecraft:entity.evoker.prepare_summon hostile @a[distance=..40] ~ ~ ~ 2 0.6"]),
                ("Main de Nagash", [f"effect give {sel_j} minecraft:wither 6 1", f"effect give {sel_j} minecraft:darkness 6 0",
                                     f"execute as {sel_j} run damage @s 6 minecraft:magic",
                                     "effect give @s minecraft:instant_damage 1 1 true",
                                     "particle minecraft:sculk_soul ~ ~2 ~ 6 2 6 0.05 200",
                                     "playsound minecraft:entity.wither.shoot hostile @a[distance=..40] ~ ~ ~ 2 0.5"]),
                ("Pas de l'Ombre", [f"execute as @p[distance=..28,gamemode=!spectator,gamemode=!creative] at @s run tp @e[tag=rm_boss_nagash,limit=1,sort=nearest] ^ ^ ^-3",
                                    "particle minecraft:reverse_portal ~ ~2 ~ 1 2 1 0.2 150",
                                    "playsound minecraft:entity.enderman.teleport hostile @a[distance=..40] ~ ~ ~ 2 0.5"])],
            "archaon": [
                ("Les Huit Malédictions", [f"effect give {sel_j} minecraft:weakness 8 1", f"effect give {sel_j} minecraft:slowness 4 1",
                                           f"effect give {sel_j} minecraft:glowing 10 0",
                                           "particle minecraft:crimson_spore ~ ~2 ~ 6 2 6 0 300"]),
                ("Foudre des Huit-Points", [f"execute at @a[distance=..20,gamemode=!spectator,gamemode=!creative,limit=3,sort=random] run summon minecraft:lightning_bolt ~ ~ ~",
                                            "playsound minecraft:entity.lightning_bolt.thunder hostile @a[distance=..60] ~ ~ ~ 2 0.7"]),
                ("Élus d'Archaon", invoc + ["particle minecraft:flame ~ ~1 ~ 2 1 2 0.05 80"])],
            "gordrakk": [
                ("WAAAGH !", invoc + ["effect give @e[team=rm_destruction,distance=..20] minecraft:strength 15 1",
                                      "effect give @s minecraft:speed 8 1",
                                      "playsound minecraft:entity.ravager.roar hostile @a[distance=..60] ~ ~ ~ 2 0.6"]),
                ("Coup de Poing de Gork", [f"effect give @a[distance=..7,gamemode=!spectator,gamemode=!creative] minecraft:levitation 1 6",
                                           f"execute as @a[distance=..7,gamemode=!spectator,gamemode=!creative] run damage @s 8 minecraft:mob_attack",
                                           "particle minecraft:explosion ~ ~ ~ 3 0.2 3 0 12",
                                           "playsound minecraft:entity.generic.explode hostile @a[distance=..40] ~ ~ ~ 2 0.7"]),
                ("Charge du Maw-Krusha", [f"execute as @p[distance=..28,gamemode=!spectator,gamemode=!creative] at @s run tp @e[tag=rm_boss_gordrakk,limit=1,sort=nearest] ~ ~ ~",
                                          f"execute as @a[distance=..4] run damage @s 6 minecraft:mob_attack",
                                          "particle minecraft:cloud ~ ~ ~ 2 0.5 2 0.1 60"])],
            "skarbrand": [
                ("Rage Totale", ["effect give @s minecraft:strength 10 2", "effect give @s minecraft:speed 10 1",
                                 "particle minecraft:angry_villager ~ ~3 ~ 1 1 1 0 20",
                                 "playsound minecraft:entity.ravager.roar hostile @a[distance=..60] ~ ~ ~ 2 0.4"]),
                ("Brasier de Khorne", [f"execute as {sel_j} run damage @s 7 minecraft:in_fire",
                                       "particle minecraft:flame ~ ~1 ~ 6 1 6 0.05 300",
                                       "playsound minecraft:item.firecharge.use hostile @a[distance=..40] ~ ~ ~ 2 0.6"]),
                ("Appel du Sang", invoc)],
            "thanquol": [
                ("Malefoudre", [f"execute at @a[distance=..20,gamemode=!spectator,gamemode=!creative,limit=2,sort=random] run summon minecraft:lightning_bolt ~ ~ ~",
                                f"effect give {sel_j} minecraft:wither 5 1",
                                "particle minecraft:happy_villager ~ ~2 ~ 5 2 5 0 200"]),
                ("Nuage de Gaz Empoisonné", [f"effect give {sel_j} minecraft:poison 8 1", f"effect give {sel_j} minecraft:nausea 8 0",
                                             "particle minecraft:item_slime ~ ~1 ~ 5 1 5 0 200",
                                             "playsound minecraft:entity.puffer_fish.blow_up hostile @a[distance=..40] ~ ~ ~ 2 0.5"]),
                ("Esclaves-Rats !", invoc + ["playsound minecraft:block.bell.use hostile @a[distance=..60] ~ ~ ~ 2 0.5"])],
            "rotigus": [
                ("Déluge de Nurgle", [f"effect give {sel_j} minecraft:poison 10 1", f"effect give {sel_j} minecraft:slowness 6 1",
                                      f"effect give {sel_j} minecraft:hunger 10 2",
                                      "particle minecraft:falling_water ~ ~4 ~ 6 1 6 0 400",
                                      "playsound minecraft:weather.rain hostile @a[distance=..40] ~ ~ ~ 2 0.5"]),
                ("Bénédiction de Grand-Père", ["effect give @s minecraft:instant_damage 1 1 true",
                                               "effect give @e[team=rm_chaos,distance=..20] minecraft:resistance 10 1",
                                               "particle minecraft:item_slime ~ ~2 ~ 2 2 2 0 80"]),
                ("Enfants de la Peste", invoc)],
        }[bid]
        lines = ["scoreboard players set @s rm_bt 0", f"execute store result score #r rm_tmp run random value 1..{len(cap)}"]
        for i, (nom, cmds) in enumerate(cap, start=1):
            fn(f"boss/{bid}/c{i}", [f"title @a[distance=..40] actionbar {jtxt(txt(b['nom'].split(',')[0] + ' : ', b['c']), txt(nom, 'white', bold=True))}"] + cmds)
            lines.append(f"execute if score #r rm_tmp matches {i} run function {NS}:boss/{bid}/c{i}")
        fn(f"boss/{bid}/attaque", lines)
        fn(f"boss/{bid}/phase2", [
            "tag @s add rm_phase2", "effect give @s minecraft:speed infinite 0 true",
            "effect give @s minecraft:resistance infinite 0 true",
            f"title @a[distance=..48] title {jtxt(txt(b['nom'].split(',')[0], b['c'], bold=True))}",
            f"title @a[distance=..48] subtitle {jtxt(txt('entre dans une rage terrible !', 'red'))}",
            "playsound minecraft:entity.wither.spawn hostile @a[distance=..60] ~ ~ ~ 2 0.8"] + invoc)
    L = [f"bossbar set {NS}:{bid} players" for bid in BOSS]
    for bid in BOSS:
        L.append(f"execute as @e[tag=rm_boss_{bid}] at @s run function {NS}:boss/{bid}/tick")
    fn("boss/boucle", L)
    # Utilisation des sceaux et parchemins (appelé depuis pierre/utiliser)
    L = []
    base_s = {"nagash": "wither_skeleton", "archaon": "zombie", "gordrakk": "zombie", "skarbrand": "piglin_brute",
              "thanquol": "ravager", "rotigus": "zombie"}
    for bid in BOSS:
        pred = f'minecraft:carrot_on_a_stick[minecraft:custom_data~{{royaumes:"sceau_{bid}"}}]'
        fn(f"boss/{bid}/invoquer", [
            f"clear @s {pred} 1",
            f'summon {NS}:{bid} ^ ^1 ^7 {{Tags:["rm_boss","rm_boss_{bid}"],PersistenceRequired:1b}}',
            f'bossbar add {NS}:{bid} {jtxt(txt(BOSS[bid]["nom"], BOSS[bid]["c"]))}',
            f'bossbar set {NS}:{bid} max {BOSS[bid]["hp"]}', f'bossbar set {NS}:{bid} color {BOSS[bid]["barre"]}',
            f'bossbar set {NS}:{bid} visible true',
            "particle minecraft:explosion_emitter ^ ^1 ^7 0 0 0 0 1",
            "playsound minecraft:entity.lightning_bolt.thunder hostile @a[distance=..60] ~ ~ ~ 2 0.6", "return 1"])
        # les seigneurs ne s'invoquent plus n'importe où : il faut utiliser le sceau sur l'Autel des Seigneurs de leur antre
        L.append(f'execute if items entity @s weapon.mainhand {pred} run return run tellraw @s {{"text": "Ce sceau ne s\'éveille que sur l\'Autel des Seigneurs, au cœur de l\'antre du seigneur. Suis son Œil pour le trouver.", "color": "gold"}}')
    ppred = 'minecraft:carrot_on_a_stick[minecraft:custom_data~{royaumes:"parchemin"}]'
    L.append(f"execute if items entity @s weapon.mainhand {ppred} run return run function {NS}:rpg/parchemin")
    fn("objets/utiliser", L + ["return 0"])
    fn("rpg/parchemin", [f"clear @s {ppred} 1", "scoreboard players set #gain rm_tmp 100",
                         f"function {NS}:rpg/ajouter", "playsound minecraft:item.book.page_turn player @s ~ ~ ~ 1 1",
                         "particle minecraft:enchant ~ ~1 ~ 0.5 1 0.5 1 60", "return 1"])


def patcher_coeur():
    """Branche les nouveaux systèmes dans load, boucle_seconde, pierre/utiliser et le biome."""
    base = f"{OUT}/data/{NS}/function"
    def ajouter(f, lignes, debut=False):
        p = f"{base}/{f}.mcfunction"
        t = open(p, encoding="utf-8").read()
        t = ("\n".join(lignes) + "\n" + t) if debut else (t + "\n".join(lignes) + "\n")
        open(p, "w", encoding="utf-8").write(t)
    ajouter("load", [f"function {NS}:rpg/load"])
    ajouter("boucle_seconde", [f"function {NS}:rpg/boucle", f"function {NS}:boss/boucle",
                               f"execute as @a at @s {B.EN_ROYAUME} run function {NS}:rpg/decouvrir"])
    # boucle de 5 s : maintien des compétences
    ajouter("factions/boucle_dons", [f"execute as @a run function {NS}:rpg/maintenir"])
    # pierre/utiliser : tester d'abord sceaux et parchemins
    p = f"{base}/pierre/utiliser.mcfunction"
    t = open(p, encoding="utf-8").read().split("\n")
    t.insert(1, f"execute if function {NS}:objets/utiliser run return 1")
    open(p, "w", encoding="utf-8").write("\n".join(t))
    ajouter("admin/reinitialiser", [f"function {NS}:rpg/rang/{sk}/0" for sk, *_ in SKILLS] + [f"function {NS}:rpg/init"])


def gen_codex():
    B_ = lambda t, c="gold": {"text": t + "\n", "color": c, "bold": True}
    T_ = lambda t: {"text": t + "\n\n", "color": "white"}
    w(f"data/{NS}/dialog/codex.json", {
        "type": "minecraft:notice",
        "title": {"text": "Codex des Royaumes Mortels", "color": "gold", "bold": True},
        "external_title": {"text": "Codex des Royaumes", "color": "gold"},
        "body": [{"type": "minecraft:plain_message", "width": 380, "contents": [
            B_("Voyager", "light_purple"),
            T_("Pierre de Royaume (clic droit) ou Portails de Royaume (anneaux runiques violets) : passage entre ce monde "
               "et les Royaumes Mortels. 10 s de recharge."),
            B_("Gloire et niveaux", "yellow"),
            T_("Combattre, miner, forger et explorer rapporte de la Gloire. Chaque niveau donne un point de compétence : "
               "Vigueur, Force, Agilité, Mineur, Endurance, Fortune. Commande : /trigger rm_rpg"),
            B_("Forge des Royaumes", "gold"),
            T_("Lâchez les ingrédients sur une Table de forgeron : armures d'alliance, armes légendaires, élixirs, "
               "talismans, sceaux de boss. Recettes : /trigger rm_forge"),
            B_("Ressources", "aqua"),
            T_("Sigmarite, Malepierre, Ur-Or, Aether-Or, Âmes, Braises, Ambre, Graines de Vie, Pierre-Ombre, Cristal de Hysh, "
               "Éclats du Chaos, Ferraille : sur les guerriers de faction, dans les coffres et dans certains blocs des Royaumes."),
            B_("Boss légendaires", "red"),
            T_("Nagash (Shyish), Archaon (Désolation du Chaos), Gordrakk (Ghur), Skarbrand (Aqshy), Thanquol (Terres Rongées), "
               "Rotigus (Marais de Ghyran). Ils gardent leur repaire, ou s'invoquent avec un sceau forgé."),
            B_("Alliances", "green"),
            T_("Les guerriers de ta Grande Alliance ne t'attaquent pas. Les boss attaquent tout le monde.")]}],
        "action": {"label": {"text": "Fermer"}, "width": 100}})


def generer():
    gen_loot(); gen_forge(); gen_rpg(); gen_boss(); gen_codex(); patcher_coeur()
