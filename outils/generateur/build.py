# -*- coding: utf-8 -*-
"""Génère le datapack « Royaumes Mortels » pour Minecraft Java 26.3."""
import json, os, shutil, copy
from data_factions import FACTIONS, ALLIANCES, NS
from data_monde import P as PROFILS, BIOMES, SPAWN_MONSTRES, STRUCTURES
from structures import BUILDERS, START_Y
from chateaux import GRANDS
from decors import DECOS, OCEAN_DECOS, G as DECO_G
from structures3 import BUILDERS3, START3, NOUVELLES_STRUCTURES
BUILDERS.update(GRANDS)
BUILDERS.update(BUILDERS3)
START_Y.update(START3)
STRUCTURES.extend(NOUVELLES_STRUCTURES)
import data_v4
import data_v5
from structures4 import BUILDERS4, START4
BUILDERS.update(BUILDERS4)
START_Y.update(START4)
EN_ROYAUME = 'unless dimension minecraft:overworld unless dimension minecraft:the_nether unless dimension minecraft:the_end'
DIMS_ROYAUMES = [f'{NS}:royaumes_mortels'] + [f'{NS}:{d}' for d in data_v4.DIMENSIONS]

OUT = "/home/claude/aos/out/RoyaumesMortels"
VANILLA = "/tmp/mc-data/data/minecraft"
DIM = f"{NS}:royaumes_mortels"
ALL_ATTRS = sorted({a for f in FACTIONS for a, _, _ in f["attributs"]})


def w(path, data):
    full = os.path.join(OUT, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    if isinstance(data, (dict, list)):
        with open(full, "w", encoding="utf-8") as fh:
            json.dump(data, fh, ensure_ascii=False, indent=2)
    else:
        with open(full, "w", encoding="utf-8") as fh:
            fh.write(data.strip() + "\n")


def fn(name, lines):
    w(f"data/{NS}/function/{name}.mcfunction", "\n".join(lines) if isinstance(lines, list) else lines)


def snbt_str(s):
    return '"' + s.replace("\\", "\\\\").replace('"', '\\"') + '"'


def txt(text, color="white", **kw):
    d = {"text": text, "color": color}
    d.update(kw)
    return d


def jtxt(*parts):
    """Composant texte en JSON compact (accepté comme SNBT par les commandes)."""
    return json.dumps(list(parts) if len(parts) > 1 else parts[0], ensure_ascii=False)


# =========================================================================== OBJETS
def components(spec):
    c = {}
    if spec.get("nom"):
        c["minecraft:custom_name"] = {"text": spec["nom"], "color": spec.get("c", "white"), "italic": False}
    lore = [{"text": l, "color": "gray", "italic": True} for l in spec.get("lore", [])]
    if lore:
        c["minecraft:lore"] = lore
    if "atk" in spec:
        atk, vit = spec["atk"]
        c["minecraft:attribute_modifiers"] = [
            {"type": "minecraft:attack_damage", "amount": float(atk - 1), "id": "minecraft:base_attack_damage",
             "operation": "add_value", "slot": "mainhand"},
            {"type": "minecraft:attack_speed", "amount": float(vit), "id": "minecraft:base_attack_speed",
             "operation": "add_value", "slot": "mainhand"}]
    if spec.get("attrs"):
        mods = c.setdefault("minecraft:attribute_modifiers", [])
        for i, (a, v, op, slot) in enumerate(spec["attrs"]):
            mods.append({"type": f"minecraft:{a}", "amount": float(v), "id": f"royaumes:{spec.get('uid', 'objet')}_{i}",
                         "operation": op, "slot": slot})
    if spec.get("consumable"):
        c["minecraft:consumable"] = spec["consumable"]
    if spec.get("food"):
        c["minecraft:food"] = spec["food"]
    if spec.get("max_stack"):
        c["minecraft:max_stack_size"] = spec["max_stack"]
    if spec.get("ench"):
        c["minecraft:enchantments"] = dict(spec["ench"])
    if spec.get("dye") is not None:
        c["minecraft:dyed_color"] = spec["dye"]
    if spec.get("trim"):
        m, p = spec["trim"]
        c["minecraft:trim"] = {"material": f"minecraft:{m}", "pattern": f"minecraft:{p}"}
    if spec.get("unbreakable"):
        c["minecraft:unbreakable"] = {}
    if spec.get("item_model"):
        c["minecraft:item_model"] = spec["item_model"]
    if spec.get("glint"):
        c["minecraft:enchantment_glint_override"] = True
    if spec.get("rarity"):
        c["minecraft:rarity"] = spec["rarity"]
    if spec.get("custom_data"):
        c["minecraft:custom_data"] = spec["custom_data"]
    if spec.get("cmd"):
        c["minecraft:custom_model_data"] = {"strings": [spec["cmd"]]}
    if spec.get("apparence"):
        slot = {"helmet": "head", "chestplate": "chest", "leggings": "legs", "boots": "feet"}[spec["id"].rsplit("_", 1)[1]]
        c["minecraft:equippable"] = {"slot": slot, "asset_id": f"royaumes:{spec['apparence']}",
                                     "equip_sound": "minecraft:item.armor.equip_iron"}
        c.pop("minecraft:trim", None)
    return c


def entry(spec, weight=None, n=None):
    mods = []
    comp = components(spec)
    if comp:
        mods.append({"type": "minecraft:set_components", "components": comp})
    count = n if n is not None else spec.get("n", 1)
    if isinstance(count, tuple):
        mods.append({"type": "minecraft:set_count", "count": {"type": "minecraft:uniform", "min": count[0], "max": count[1]}})
    elif count != 1:
        mods.append({"type": "minecraft:set_count", "count": count})
    e = {"type": "minecraft:item", "name": spec["id"]}
    if mods:
        e["modifier"] = mods
    if weight:
        e["weight"] = weight
    return e


PIERRE = {"id": "minecraft:carrot_on_a_stick", "nom": "Pierre de Royaume", "c": "light_purple",
          "lore": ["Clic droit : voyager entre ce monde", "et les Royaumes Mortels."],
          "item_model": "minecraft:echo_shard", "glint": True, "unbreakable": True, "rarity": "epic",
          "custom_data": {"royaumes": "pierre"}}


def gen_objets():
    # Kits de faction
    for f in FACTIONS:
        pools = [{"rolls": 1, "entries": [entry(it)]} for it in f["kit"]]
        pools.append({"rolls": 1, "entries": [entry(PIERRE)]})
        pools.append({"rolls": 1, "entries": [entry({"id": "minecraft:bread"}, n=8)]})
        w(f"data/{NS}/loot_table/kits/{f['id']}.json", {"pools": pools})
    w(f"data/{NS}/loot_table/pierre.json", {"pools": [{"rolls": 1, "entries": [entry(PIERRE)]}]})
    # Recette de la Pierre de Royaume
    w(f"data/{NS}/recipe/pierre_de_royaume.json", {
        "type": "minecraft:crafting_shaped", "category": "misc",
        "key": {"A": "minecraft:amethyst_shard", "E": "minecraft:ender_pearl", "O": "minecraft:gold_ingot"},
        "pattern": ["OAO", "AEA", "OAO"],
        "result": {"id": PIERRE["id"], "count": 1, "components": components(PIERRE)}})
    # Équipements des mobs
    for pid, p in PROFILS.items():
        for slot, spec in p["equip"].items():
            w(f"data/{NS}/loot_table/equip/{pid}/{slot.replace('.', '_')}.json",
              {"pools": [{"rolls": 1, "entries": [entry(spec)]}]})


def gen_coffres():
    generiques = [
        ({"id": "minecraft:gold_ingot"}, 12, (1, 5)), ({"id": "minecraft:iron_ingot"}, 14, (2, 6)),
        ({"id": "minecraft:diamond"}, 3, (1, 2)), ({"id": "minecraft:emerald"}, 8, (1, 4)),
        ({"id": "minecraft:experience_bottle"}, 6, (2, 6)), ({"id": "minecraft:bread"}, 12, (2, 5)),
        ({"id": "minecraft:golden_apple"}, 2, 1), ({"id": "minecraft:arrow"}, 8, (4, 12)),
        ({"id": "minecraft:amethyst_shard"}, 6, (1, 4)), ({"id": "minecraft:ender_pearl"}, 4, 1),
    ]
    themes = {
        "forteresse_stormcast": ["stormcast", "cites"], "cite_sigmar": ["cites"], "camp_orruk": ["ironjawz"],
        "fort_kruleboyz": ["kruleboyz"], "temple_seraphon": ["seraphon"], "bosquet_sylvaneth": ["sylvaneth"],
        "magmahold": ["fyreslayers"], "port_kharadron": ["kharadron"], "ziggurat_hashut": ["hashut"],
        "citadelle_chaos": ["esclaves", "khorne", "tzeentch", "slaanesh"], "repaire_skaven": ["skaven"],
        "chateau_soulblight": ["soulblight"], "ossuaire_ossiarch": ["ossiarch"], "cimetiere_nighthaunt": ["nighthaunt", "fec"],
        "sanctuaire_lumineth": ["lumineth"], "temple_khaine": ["khaine"], "ruines_idoneth": ["idoneth"],
        "antre_gitz": ["gitz"], "campement_ogor": ["ogors", "behemat"],
    }
    from data_factions import FACTION_BY_ID
    for sid, facs in themes.items():
        rares = []
        for fid in facs:
            for it in FACTION_BY_ID[fid]["kit"]:
                if it.get("nom"):
                    rares.append(entry(it, weight=3))
        pools = [
            {"rolls": {"type": "minecraft:uniform", "min": 3, "max": 7},
             "entries": [entry(sp, weight=wt, n=n) for sp, wt, n in generiques]},
            {"rolls": 1, "entries": rares + [{"type": "minecraft:empty", "weight": max(2, len(rares) // 2)}]},
            {"rolls": 1, "entries": [entry(PIERRE, weight=1), {"type": "minecraft:empty", "weight": 6}]},
        ]
        w(f"data/{NS}/loot_table/coffres/{sid}.json", {"type": "minecraft:chest", "pools": pools})


# =========================================================================== ENCHANTEMENTS
def gen_enchantements():
    w(f"data/{NS}/tags/item/armes_des_royaumes.json", {"values": [
        "#minecraft:swords", "#minecraft:axes", "#minecraft:hoes", "minecraft:mace", "minecraft:trident", "minecraft:blaze_rod"]})
    direct = {"type": "minecraft:damage_source_properties", "predicate": {"is_direct": True}}

    def ench(eid, nom, effets, max_level=1, chance=None):
        req = direct if chance is None else {"type": "minecraft:all_of", "terms": [
            direct, {"type": "minecraft:random_chance", "chance": chance}]}
        for e in effets:
            e.setdefault("requirements", req)
        w(f"data/{NS}/enchantment/{eid}.json", {
            "anvil_cost": 4, "description": {"text": nom, "color": "gold"},
            "effects": {"minecraft:post_attack": effets},
            "max_cost": {"base": 50, "per_level_above_first": 10}, "max_level": max_level,
            "min_cost": {"base": 20, "per_level_above_first": 10},
            "slots": ["mainhand"], "supported_items": f"#{NS}:armes_des_royaumes", "weight": 1})

    ench("foudre_de_sigmar", "Foudre de Sigmar", [{
        "affected": "victim", "enchanted": "attacker",
        "effect": {"type": "minecraft:all_of", "effects": [
            {"type": "minecraft:damage_entity", "damage_type": "minecraft:lightning_bolt", "min_damage": 3.0, "max_damage": 6.0},
            {"type": "minecraft:ignite", "duration": 2.0},
            {"type": "minecraft:play_sound", "sound": "minecraft:item.trident.thunder", "volume": 1.0, "pitch": 1.4}]}}],
        chance=0.25)
    ench("peste", "Peste de Nurgle", [{
        "affected": "victim", "enchanted": "attacker",
        "effect": {"type": "minecraft:apply_mob_effect", "to_apply": "minecraft:poison",
                   "min_duration": 3.0, "max_duration": {"type": "minecraft:linear", "base": 4.0, "per_level_above_first": 2.0},
                   "min_amplifier": 0.0, "max_amplifier": {"type": "minecraft:linear", "base": 0.0, "per_level_above_first": 1.0}}}],
        max_level=2)
    ench("malepierre", "Malepierre", [{
        "affected": "victim", "enchanted": "attacker",
        "effect": {"type": "minecraft:apply_mob_effect", "to_apply": "minecraft:wither",
                   "min_duration": 2.0, "max_duration": 4.0, "min_amplifier": 0.0, "max_amplifier": 0.0}}])
    ench("vol_d_ame", "Vol d'Âme", [{
        "affected": "attacker", "enchanted": "attacker",
        "effect": {"type": "minecraft:apply_mob_effect", "to_apply": "minecraft:regeneration",
                   "min_duration": 2.0, "max_duration": 3.0, "min_amplifier": 0.0,
                   "max_amplifier": {"type": "minecraft:linear", "base": 0.0, "per_level_above_first": 1.0}}}],
        max_level=2, chance=0.4)
    ench("flammes_de_tzeentch", "Flammes de Tzeentch", [{
        "affected": "victim", "enchanted": "attacker",
        "effect": {"type": "minecraft:all_of", "effects": [
            {"type": "minecraft:ignite", "duration": 4.0},
            {"type": "minecraft:apply_mob_effect", "to_apply": "minecraft:levitation",
             "min_duration": 1.0, "max_duration": 1.5, "min_amplifier": 0.0, "max_amplifier": 0.0}]}}])
    ench("waaagh", "WAAAGH !", [{
        "affected": "attacker", "enchanted": "attacker",
        "effect": {"type": "minecraft:apply_mob_effect", "to_apply": "minecraft:speed",
                   "min_duration": 3.0, "max_duration": 4.0, "min_amplifier": 0.0, "max_amplifier": 0.0}}], chance=0.5)


# =========================================================================== FACTIONS & DIALOGUES
def faction_label(f):
    return {"text": f["nom"], "color": f["couleur"]}


def gen_dialogues():
    # Accueil
    w(f"data/{NS}/dialog/accueil.json", {
        "type": "minecraft:multi_action",
        "title": {"text": "⚔ Les Royaumes Mortels ⚔", "color": "gold", "bold": True},
        "body": [{"type": "minecraft:plain_message", "width": 300, "contents": [
            {"text": "L'Âge de Sigmar a commencé.\n\n", "color": "yellow"},
            {"text": "Les huit Royaumes Mortels sont déchirés par la guerre entre les quatre Grandes Alliances. "
                     "Choisis ta Grande Alliance, puis ta faction : elle te donnera des dons, des faiblesses, "
                     "un équipement de départ et des alliés.\n\n", "color": "white"},
            {"text": "Attention : ce choix est définitif.", "color": "red"}]}],
        "can_close_with_escape": False,
        "columns": 2,
        "actions": [{"label": {"text": a["nom"], "color": a["couleur"], "bold": True},
                     "tooltip": {"text": a["desc"]}, "width": 140,
                     "action": {"type": "show_dialog", "dialog": f"{NS}:alliance_{aid}"}}
                    for aid, a in ALLIANCES.items()]})
    for aid, a in ALLIANCES.items():
        facs = [f for f in FACTIONS if f["alliance"] == aid]
        w(f"data/{NS}/dialog/alliance_{aid}.json", {
            "type": "minecraft:multi_action",
            "title": {"text": f"Grande Alliance : {a['nom']}", "color": a["couleur"], "bold": True},
            "body": [{"type": "minecraft:plain_message", "width": 300, "contents": {"text": a["desc"]}}],
            "can_close_with_escape": False, "columns": 2,
            "actions": [{"label": faction_label(f),
                         "tooltip": [{"text": f"Royaume : {f['royaume']}\n", "color": "gray"},
                                     {"text": f"+ {f['bonus']}\n", "color": "green"},
                                     {"text": f"- {f['malus']}", "color": "red"}],
                         "width": 150,
                         "action": {"type": "show_dialog", "dialog": f"{NS}:faction/{f['id']}"}} for f in facs],
            "exit_action": {"label": {"text": "← Retour"}, "width": 120,
                            "action": {"type": "show_dialog", "dialog": f"{NS}:accueil"}}})
    for f in FACTIONS:
        kit = ", ".join(it.get("nom") or it["id"].split(":")[1].replace("_", " ") for it in f["kit"])
        w(f"data/{NS}/dialog/faction/{f['id']}.json", {
            "type": "minecraft:confirmation",
            "title": {"text": f["nom"], "color": f["couleur"], "bold": True},
            "body": [{"type": "minecraft:plain_message", "width": 300, "contents": [
                {"text": f["desc"] + "\n\n", "color": "white", "italic": True},
                {"text": "Grande Alliance : ", "color": "gray"},
                {"text": ALLIANCES[f["alliance"]]["nom"] + "\n", "color": ALLIANCES[f["alliance"]]["couleur"]},
                {"text": "Royaume d'origine : ", "color": "gray"}, {"text": f["royaume"] + "\n\n", "color": "white"},
                {"text": "Dons : ", "color": "green", "bold": True}, {"text": f["bonus"] + "\n", "color": "green"},
                {"text": "Faiblesses : ", "color": "red", "bold": True}, {"text": f["malus"] + "\n\n", "color": "red"},
                {"text": "Équipement : ", "color": "gold"}, {"text": kit + ", Pierre de Royaume", "color": "yellow"}]}],
            "can_close_with_escape": False,
            "yes": {"label": {"text": "Rejoindre", "color": "green", "bold": True}, "width": 120,
                    "action": {"type": "run_command", "command": f"trigger rm_choix set {f['num']}"}},
            "no": {"label": {"text": "← Retour"}, "width": 120,
                   "action": {"type": "show_dialog", "dialog": f"{NS}:alliance_{f['alliance']}"}}})
    # Codex (accessible via le menu « Actions rapides »)
    w(f"data/{NS}/dialog/codex.json", {
        "type": "minecraft:notice",
        "title": {"text": "Codex des Royaumes Mortels", "color": "gold", "bold": True},
        "external_title": {"text": "Codex des Royaumes", "color": "gold"},
        "body": [{"type": "minecraft:plain_message", "width": 320, "contents": [
            {"text": "Pierre de Royaume\n", "color": "light_purple", "bold": True},
            {"text": "Clic droit pour passer de ce monde aux Royaumes Mortels et inversement (10 s de recharge). "
                     "Recette : or aux coins, améthyste sur les côtés, perle de l'Ender au centre.\n\n"},
            {"text": "Les Royaumes\n", "color": "gold", "bold": True},
            {"text": "Azyr (montagnes), Hysh, Ghyran (forêts et marais), Ghur (savanes et jungles), Aqshy (cendres), "
                     "Chamon (déserts d'or), Shyish (terres funèbres), Ulgu (brumes et mers), les Huit-Points du Chaos "
                     "et les Terres Rongées des Skaven.\n\n"},
            {"text": "Alliances\n", "color": "gold", "bold": True},
            {"text": "Les guerriers de ta Grande Alliance ne t'attaquent pas. Les autres, si.\n\n"},
            {"text": "Commande utile : ", "color": "gray"}, {"text": "/trigger rm_codex", "color": "yellow"}]}],
        "action": {"label": {"text": "Fermer"}, "width": 100}})
    w("data/minecraft/tags/dialog/quick_actions.json", {"replace": False, "values": [f"{NS}:codex"]})


def gen_fonctions_factions():
    # Application des dons
    for f in FACTIONS:
        lines = [f"# Dons de la faction {f['nom']}"]
        for a, v, op in f["attributs"]:
            lines.append(f"attribute @s minecraft:{a} modifier add {NS}:faction {v} {op}")
        for e, amp in f["effets"]:
            lines.append(f"effect give @s minecraft:{e} infinite {amp} true")
        fn(f"factions/dons/{f['id']}", lines)
    fn("factions/retirer_dons", [f"attribute @s minecraft:{a} modifier remove {NS}:faction" for a in ALL_ATTRS]
       + ["effect clear @s"])
    # Choix
    for f in FACTIONS:
        a = ALLIANCES[f["alliance"]]
        fn(f"factions/choisir/{f['id']}", [
            f"scoreboard players set @s rm_faction {f['num']}",
            f"team join {a['team']} @s",
            f"function {NS}:factions/dons/{f['id']}",
            f"loot give @s loot {NS}:kits/{f['id']}",
            "dialog clear @s",
            f"title @s title {jtxt(txt(f['nom'], f['couleur'], bold=True))}",
            f"title @s subtitle {jtxt(txt('Grande Alliance : ' + a['nom'], a['couleur']))}",
            "playsound minecraft:ui.toast.challenge_complete master @s ~ ~ ~ 1 1",
            f"tellraw @s {jtxt(txt('» ', 'gold'), txt(f['desc'], 'gray', italic=True))}",
            f"tellraw @s {jtxt(txt('» Dons : ', 'green'), txt(f['bonus'], 'green'))}",
            f"tellraw @s {jtxt(txt('» Faiblesses : ', 'red'), txt(f['malus'], 'red'))}",
            f"tellraw @s {jtxt(txt('» Utilise ta ', 'gold'), txt('Pierre de Royaume', 'light_purple'), txt(' (clic droit) pour rejoindre les Royaumes Mortels.', 'gold'))}",
            f"tellraw @a {jtxt(txt('⚔ ', 'gold'), {'selector': '@s'}, txt(' a rejoint : ', 'gray'), txt(f['nom'], f['couleur']))}",
        ])
    lines = ["# Traite le choix de faction (trigger rm_choix)",
             "execute if score @s rm_faction matches 1.. run return run scoreboard players set @s rm_choix 0"]
    for f in FACTIONS:
        lines.append(f"execute if score @s rm_choix matches {f['num']} run function {NS}:factions/choisir/{f['id']}")
    lines += ["scoreboard players set @s rm_choix 0", "scoreboard players enable @s rm_choix"]
    fn("choix/traiter", lines)
    fn("choix/ouvrir", ["scoreboard players set @s rm_menu 120", "scoreboard players enable @s rm_choix",
                        f"dialog show @s {NS}:accueil"])
    # Boucle des dons (toutes les 5 s)
    lines = []
    for f in FACTIONS:
        lines.append(f"execute as @a[scores={{rm_faction={f['num']}}}] run function {NS}:factions/dons/{f['id']}")
    sb = FACTIONS[[x["id"] for x in FACTIONS].index("soulblight")]["num"]
    lines += ["# Soulblight : faiblesse en plein soleil",
              "execute store result score #jour rm_tmp run time query time",
              "scoreboard players operation #jour rm_tmp %= #24000 rm_const",
              f"execute if score #jour rm_tmp matches 0..12000 as @a[scores={{rm_faction={sb}}}] at @s "
              f"if predicate {NS}:sous_le_ciel run effect give @s minecraft:weakness 6 0 true"]
    fn("factions/boucle_dons", lines)
    w(f"data/{NS}/predicate/sous_le_ciel.json", {"type": "minecraft:location_check", "predicate": {"can_see_sky": True}})
    # Administration
    fn("admin/reinitialiser", [
        "# Réinitialise la faction du joueur (à lancer : /execute as <joueur> run function royaumes:admin/reinitialiser)",
        f"function {NS}:factions/retirer_dons",
        "scoreboard players reset @s rm_faction", "team leave @s", "scoreboard players set @s rm_menu 0",
        f"tellraw @s {jtxt(txt('Ta faction a été réinitialisée.', 'yellow'))}"])


# =========================================================================== CŒUR (load / tick)
def gen_coeur():
    lines = [
        "# Royaumes Mortels — initialisation",
        "scoreboard objectives add rm_faction dummy",
        "scoreboard objectives add rm_choix trigger",
        "scoreboard objectives add rm_codex trigger",
        "scoreboard objectives add rm_menu dummy",
        "scoreboard objectives add rm_cd dummy",
        "scoreboard objectives add rm_biome dummy",
        "scoreboard objectives add rm_bnow dummy",
        "scoreboard objectives add rm_tmp dummy",
        "scoreboard objectives add rm_const dummy",
        "scoreboard objectives add rm_pierre minecraft.used:minecraft.carrot_on_a_stick",
        "scoreboard objectives add rm_quitte minecraft.custom:minecraft.leave_game",
        "scoreboard players set #24000 rm_const 24000",
        "scoreboard players set #5 rm_const 5",
    ]
    for aid, a in ALLIANCES.items():
        lines += [f"team add {a['team']} {jtxt(txt(a['nom'], a['couleur']))}",
                  f"team modify {a['team']} color {a['couleur']}",
                  f"team modify {a['team']} prefix {jtxt(txt('[' + a['nom'] + '] ', a['couleur']))}",
                  f"team modify {a['team']} friendlyFire false",
                  f"team modify {a['team']} seeFriendlyInvisibles true"]
    lines += [f"schedule function {NS}:boucle_seconde 20t replace",
              f"tellraw @a {jtxt(txt('[Royaumes Mortels] ', 'gold'), txt('Datapack chargé. Pour Sigmar !', 'yellow'))}"]
    fn("load", lines)
    w("data/minecraft/tags/function/load.json", {"values": [f"{NS}:load"]})
    w("data/minecraft/tags/function/tick.json", {"values": [f"{NS}:tick"]})
    fn("tick", [
        f"execute as @a[scores={{rm_choix=1..}}] run function {NS}:choix/traiter",
        f"execute as @a[scores={{rm_pierre=1..}}] at @s run function {NS}:pierre/utiliser",
        f"execute as @a[scores={{rm_codex=1..}}] run function {NS}:codex",
    ])
    fn("codex", ["scoreboard players set @s rm_codex 0", "scoreboard players enable @s rm_codex",
                 f"dialog show @s {NS}:codex"])
    fn("boucle_seconde", [
        f"schedule function {NS}:boucle_seconde 20t replace",
        "# Reconnexion : rouvrir le menu si aucune faction",
        "execute as @a[scores={rm_quitte=1..}] run scoreboard players set @s rm_menu 0",
        "scoreboard players set @a[scores={rm_quitte=1..}] rm_quitte 0",
        "scoreboard players enable @a rm_codex",
        "scoreboard players remove @a[scores={rm_menu=1..}] rm_menu 1",
        f"execute as @a[tag=!rm_modde] unless score @s rm_faction matches 1.. unless score @s rm_menu matches 1.. run function {NS}:choix/ouvrir",
        "scoreboard players remove @a[scores={rm_cd=1..}] rm_cd 1",
        "# Dons toutes les 5 secondes",
        "scoreboard players add #cycle rm_tmp 1",
        "scoreboard players operation #c5 rm_tmp = #cycle rm_tmp",
        "scoreboard players operation #c5 rm_tmp %= #5 rm_const",
        f"execute if score #c5 rm_tmp matches 0 run function {NS}:factions/boucle_dons",
        "# Biomes et habitants des Royaumes",
        f"execute as @a at @s {EN_ROYAUME} run function {NS}:monde/biome_joueur",
        "execute as @a at @s if dimension minecraft:overworld run scoreboard players set @s rm_biome 0",
        "execute as @a at @s if dimension minecraft:the_nether run scoreboard players set @s rm_biome 0",
    ] + [f"execute in {d} as @e[type=#{NS}:convertibles,tag=!rm_c,distance=0..] at @s run function {NS}:mobs/convertir"
         for d in DIMS_ROYAUMES] + [
        f"execute as @e[tag=rm_spawn] at @s run function {NS}:mobs/marqueur",
        f"execute as @e[type=minecraft:marker,tag=rm_portail] at @s as @a[distance=..1.8] unless score @s rm_cd matches 1.. at @s run function {NS}:pierre/portail",
    ])


# =========================================================================== PIERRE DE ROYAUME
def gen_pierre():
    item = f"minecraft:carrot_on_a_stick[minecraft:custom_data~{{royaumes:\"pierre\"}}]"
    fn("pierre/utiliser", [
        "scoreboard players set @s rm_pierre 0",
        f"execute unless items entity @s weapon.* {item} run return 0",
        f"execute if score @s rm_cd matches 1.. run return run title @s actionbar {jtxt(txt('La Pierre de Royaume se recharge…', 'gray'))}",
        "scoreboard players set @s rm_cd 10",
        "particle minecraft:reverse_portal ~ ~1 ~ 0.4 1 0.4 0.05 80",
        "playsound minecraft:block.respawn_anchor.set_spawn player @a ~ ~ ~ 1 0.8",
        f"execute {EN_ROYAUME} run return run function {NS}:pierre/vers_monde",
        f"function {NS}:pierre/vers_royaumes",
    ])
    fn("pierre/portail", [
        "scoreboard players set @s rm_cd 10",
        "particle minecraft:reverse_portal ~ ~1 ~ 0.6 1.2 0.6 0.1 150",
        "playsound minecraft:block.portal.trigger player @a[distance=..16] ~ ~ ~ 0.6 1.4",
        f"execute {EN_ROYAUME} run return run function {NS}:pierre/vers_monde",
        f"function {NS}:faille/aleatoire"])
    fn("pierre/vers_royaumes", [
        f"execute in {DIM} run spreadplayers ~ ~ 0 48 false @s",
        "# Si tout est océan autour, on élargit la recherche",
        f"execute at @s unless dimension {DIM} in {DIM} run spreadplayers ~ ~ 0 600 false @s",
        f"title @s title {jtxt(txt('Les Royaumes Mortels', 'gold', bold=True))}",
        "effect give @s minecraft:resistance 5 4 true",
        "effect give @s minecraft:slow_falling 5 0 true",
        "execute at @s run playsound minecraft:block.portal.travel player @s ~ ~ ~ 0.4 1.5",
    ])
    fn("pierre/vers_monde", [
        "execute in minecraft:overworld run spreadplayers ~ ~ 0 48 false @s",
        f"execute at @s {EN_ROYAUME} in minecraft:overworld run spreadplayers ~ ~ 0 600 false @s",
        f"title @s title {jtxt(txt('Le Monde-Pont', 'aqua', bold=True))}",
        "effect give @s minecraft:resistance 5 4 true",
        "effect give @s minecraft:slow_falling 5 0 true",
        "execute at @s run playsound minecraft:block.portal.travel player @s ~ ~ ~ 0.4 1.5",
    ])


# =========================================================================== MONDE (dimension, biomes)
def charger(path):
    with open(os.path.join(VANILLA, path)) as fh:
        return json.load(fh)


EXTRA_FEATURES = {
    "magma_aqshy": ({"type": "minecraft:ore", "discard_chance_on_air_exposure": 0.0, "size": 24, "targets": [
        {"state": "minecraft:magma_block", "target": {"predicate_type": "minecraft:tag_match", "tag": "minecraft:base_stone_overworld"}},
        {"state": "minecraft:magma_block", "target": {"predicate_type": "minecraft:block_match", "block": "minecraft:blackstone"}}]},
        8, 40, 140),
    "or_chamon": ({"type": "minecraft:ore", "discard_chance_on_air_exposure": 0.0, "size": 5, "targets": [
        {"state": "minecraft:raw_gold_block", "target": {"predicate_type": "minecraft:block_match", "block": "minecraft:sandstone"}},
        {"state": "minecraft:gold_ore", "target": {"predicate_type": "minecraft:tag_match", "tag": "minecraft:stone_ore_replaceables"}}]},
        14, 30, 140),
    "os_shyish": ({"type": "minecraft:ore", "discard_chance_on_air_exposure": 0.0, "size": 10, "targets": [
        {"state": "minecraft:bone_block", "target": {"predicate_type": "minecraft:tag_match", "tag": "minecraft:stone_ore_replaceables"}}]},
        6, 20, 110),
    "obsidienne_chaos": ({"type": "minecraft:ore", "discard_chance_on_air_exposure": 0.0, "size": 6, "targets": [
        {"state": "minecraft:crying_obsidian", "target": {"predicate_type": "minecraft:tag_match", "tag": "minecraft:base_stone_overworld"}},
        {"state": "minecraft:obsidian", "target": {"predicate_type": "minecraft:block_match", "block": "minecraft:blackstone"}}]},
        6, 30, 140),
    "malepierre": ({"type": "minecraft:ore", "discard_chance_on_air_exposure": 0.0, "size": 6, "targets": [
        {"state": "minecraft:verdant_froglight", "target": {"predicate_type": "minecraft:tag_match", "tag": "minecraft:stone_ore_replaceables"}}]},
        10, 0, 120),
}


def gen_features():
    for fid, (conf, count, ymin, ymax) in EXTRA_FEATURES.items():
        w(f"data/{NS}/worldgen/feature/{fid}.json", conf)
        w(f"data/{NS}/worldgen/placed_feature/{fid}.json", {"feature": f"{NS}:{fid}", "placement": [
            {"type": "minecraft:count", "count": count}, {"type": "minecraft:in_square"},
            {"type": "minecraft:height_range", "height": {"type": "minecraft:uniform",
                                                          "min_inclusive": {"absolute": ymin}, "max_inclusive": {"absolute": ymax}}},
            {"type": "minecraft:biome"}]})


CREATURES = {
    "azyr_cimes": [("goat", 10, 3), ("sheep", 8, 4), ("horse", 3, 3)],
    "hysh_plateaux": [("rabbit", 8, 3), ("sheep", 8, 4), ("fox", 4, 2), ("horse", 3, 3)],
    "ghyran_jade": [("fox", 6, 3), ("rabbit", 8, 3), ("wolf", 4, 4), ("pig", 6, 4), ("cow", 6, 4)],
    "ghyran_marais": [("frog", 10, 5), ("slime", 2, 2)],
    "ghur_terres": [("horse", 8, 6), ("cow", 10, 4), ("goat", 6, 3), ("wolf", 6, 6), ("camel", 3, 2),
                    ("armadillo", 6, 3), ("llama", 5, 4), ("sheep", 6, 4)],
    "ghur_jungle": [("parrot", 30, 3), ("ocelot", 4, 2), ("panda", 3, 2), ("chicken", 8, 4)],
    "aqshy_cendres": [("armadillo", 6, 2)],
    "chamon_desert": [("camel", 6, 2), ("armadillo", 8, 3), ("rabbit", 6, 3)],
    "ulgu_brumes": [("wolf", 6, 4), ("fox", 6, 2), ("rabbit", 4, 2)],
    "terres_rongees": [("chicken", 6, 3), ("frog", 6, 3)],
}
CREATURES.update(data_v4.CREATURES_V4)


def gen_decors():
    for did, (fn_, bl, chance) in DECOS.items():
        st = fn_()
        path = os.path.join(OUT, f"data/{NS}/structure/decor/{did}.nbt")
        os.makedirs(os.path.dirname(path), exist_ok=True)
        st.save(path)
        w(f"data/{NS}/worldgen/feature/decor_{did}.json", {
            "type": "minecraft:template", "templates": [{"data": {"id": f"{NS}:decor/{did}"}, "weight": 1}]})
        ocean = did in OCEAN_DECOS
        w(f"data/{NS}/worldgen/placed_feature/decor_{did}.json", {"feature": f"{NS}:decor_{did}", "placement": [
            {"type": "minecraft:rarity_filter", "chance": chance},
            {"type": "minecraft:in_square"},
            {"type": "minecraft:heightmap", "heightmap": "OCEAN_FLOOR" if ocean else "MOTION_BLOCKING_NO_LEAVES"},
            {"type": "minecraft:offset", "x": 0, "y": -1, "z": 0},
            {"type": "minecraft:block_predicate_filter", "predicate": {"type": "minecraft:solid"}},
            {"type": "minecraft:offset", "x": 0, "y": -DECO_G, "z": 0},
            {"type": "minecraft:biome"}]})
    for did, (fn_, bl, chance) in data_v4.FLOTTANTS.items():
        st = fn_()
        path = os.path.join(OUT, f"data/{NS}/structure/decor/{did}.nbt")
        st.save(path)
        w(f"data/{NS}/worldgen/feature/decor_{did}.json", {
            "type": "minecraft:template", "templates": [{"data": {"id": f"{NS}:decor/{did}"}, "weight": 1}]})
        w(f"data/{NS}/worldgen/placed_feature/decor_{did}.json", {"feature": f"{NS}:decor_{did}", "placement": [
            {"type": "minecraft:rarity_filter", "chance": chance}, {"type": "minecraft:in_square"},
            {"type": "minecraft:heightmap", "heightmap": "MOTION_BLOCKING_NO_LEAVES"},
            {"type": "minecraft:offset", "x": 0, "y": 14, "z": 0},
            {"type": "minecraft:offset", "x": 0, "y": {"type": "minecraft:uniform", "min_inclusive": 0, "max_inclusive": 16}, "z": 0},
            {"type": "minecraft:biome"}]})
    # Rochers thématiques
    for bid, bloc, n in (("aqshy_cendres", "minecraft:blackstone", 3), ("chamon_desert", "minecraft:raw_gold_block", 1),
                         ("shyish_terres", "minecraft:bone_block", 2), ("chaos_desolation", "minecraft:obsidian", 2),
                         ("ghur_terres", "minecraft:mossy_cobblestone", 2), ("terres_rongees", "minecraft:verdant_froglight", 1)):
        w(f"data/{NS}/worldgen/feature/rocher_{bid}.json", {"type": "minecraft:block_blob",
            "can_place_on": {"type": "minecraft:solid"}, "state": bloc})
        w(f"data/{NS}/worldgen/placed_feature/rocher_{bid}.json", {"feature": f"{NS}:rocher_{bid}", "placement": [
            {"type": "minecraft:count", "count": n}, {"type": "minecraft:in_square"},
            {"type": "minecraft:heightmap", "heightmap": "MOTION_BLOCKING"}, {"type": "minecraft:biome"}]})


def particule(p):
    """Options obligatoires de certaines particules (26.3)."""
    if p == "minecraft:tinted_leaves":
        return {"type": p, "color": -3644374}  # 0xFFC8642A, feuillage roux du wyldwood
    if p == "minecraft:entity_effect":
        return {"type": p, "color": -10092442}
    return {"type": p}


def gen_biomes():
    for b in BIOMES:
        v = charger(f"worldgen/biome/{b['base']}.json")
        d = copy.deepcopy(v)
        d["temperature"] = b["temp"]
        d["downfall"] = b["pluie"]
        d["has_precipitation"] = b["precip"]
        d.pop("temperature_modifier", None)
        attrs = d.setdefault("attributes", {})
        attrs["minecraft:visual/sky_color"] = b["ciel"]
        attrs["minecraft:visual/fog_color"] = b["brume"]
        attrs["minecraft:visual/water_fog_color"] = b["eau_brume"]
        attrs["minecraft:gameplay/monsters_burn"] = False
        if b.get("particules"):
            attrs["minecraft:visual/ambient_particles"] = {
                "argument": [{"particle": particule(p), "probability": pr} for p, pr in b["particules"]],
                "modifier": "append"}
        if b.get("brouillard"):
            attrs["minecraft:visual/fog_end_distance"] = {"argument": b["brouillard"], "modifier": "multiply"}
        # Monstres
        spawns = attrs["minecraft:gameplay/natural_mob_spawns"]["argument"]["spawns_by_category"]
        mons = SPAWN_MONSTRES.get(b["id"], SPAWN_MONSTRES["default"])
        spawns["monster"] = [{"type": f"minecraft:{t}", "count": {"type": "minecraft:uniform", "min_inclusive": 1, "max_inclusive": c}
                              if c > 1 else 1, "weight": wt} for t, wt, c in mons]
        eff = d.setdefault("effects", {})
        eff["water_color"] = b["eau"]
        eff["grass_color"] = b["herbe"]
        eff["foliage_color"] = b["feuilles"]
        eff["dry_foliage_color"] = b["feuilles"]
        for ex in b.get("extra", []):
            d["features"][6].append(f"{NS}:{ex}")
        for did, (_, bl, _) in list(DECOS.items()) + list(data_v4.FLOTTANTS.items()):
            if b["id"] in bl:
                d["features"][4].append(f"{NS}:decor_{did}")
        cr = spawns.setdefault("creature", [])
        for t, wt, cmax in CREATURES.get(b["id"], []):
            cr.append({"type": f"minecraft:{t}", "count": {"type": "minecraft:uniform", "min_inclusive": 1, "max_inclusive": cmax}
                       if cmax > 1 else 1, "weight": wt})
        if os.path.exists(os.path.join(OUT, f"data/{NS}/worldgen/feature/rocher_{b['id']}.json")):
            d["features"][4].append(f"{NS}:rocher_{b['id']}")
        w(f"data/{NS}/worldgen/biome/{b['id']}.json", d)


def gen_dimension():
    # Paramètres multi-bruit
    T = [(-1.0, -0.45), (-0.45, 0.0), (0.0, 0.45), (0.45, 1.0)]
    H = [(-1.0, -0.35), (-0.35, 0.3), (0.3, 1.0)]
    pts = []

    def pt(bid, temp, hum, cont, ero, weird=(-1.0, 1.0), offset=0.0):
        pts.append({"biome": f"{NS}:{bid}", "parameters": {
            "temperature": list(temp), "humidity": list(hum), "continentalness": list(cont),
            "erosion": list(ero), "weirdness": list(weird), "depth": 0.0, "offset": offset}})

    for b in BIOMES:
        if b.get("special") == "ocean":
            pt(b["id"], (-1, 1), (-1, 1), (-1.2, -0.19), (-1, 1))
        elif b.get("special") == "pics":
            pt(b["id"], (-1, 1), (-1, 1), (0.3, 1.0), (-1.0, -0.6))
        elif b.get("special") == "flottant":
            continue
        else:
            cells = b["grille"] if isinstance(b["grille"], list) else [b["grille"]]
            for (t, h) in cells:
                pt(b["id"], T[t - 1], H[h - 1], (-0.19, 1.0), (-0.6, 1.0), weird=b.get("weird", (-1.0, 1.0)))
    def points_royaume(ids, flottant=False):
        """Points multi-bruit d'un Royaume : océans, pics, puis grille climatique partagée."""
        res = []
        terres = [i for i in ids if _BIOME[i].get("special") not in ("ocean", "pics")]
        for i in ids:
            sp = _BIOME[i].get("special")
            if sp == "ocean" and not flottant:
                res.append((i, (-1, 1), (-1, 1), (-1.2, -0.19), (-1, 1), (-1, 1)))
            elif sp == "pics":
                res.append((i, (-1, 1), (-1, 1), (0.05, 1.0), (-1.0, -0.15), (-1, 1)))
        n = len(terres)
        for k, i in enumerate(terres):
            # bandes de température x humidité en damier pour bien mélanger
            for j in range(2):
                t0 = -1.0 + 2.0 * k / n
                t1 = -1.0 + 2.0 * (k + 1) / n
                h = (-1.0, 0.0) if j == 0 else (0.0, 1.0)
                tt = (t0, t1) if j == 0 else (-1.0 + 2.0 * ((k + 1) % n) / n, -1.0 + 2.0 * ((k + 1) % n + 1) / n)
                res.append((i, tt, h, (-0.19 if not flottant else -1.2, 1.0), (-1.0, 1.0), (-1, 1)))
        # avec des pics, les autres biomes reçoivent un léger décalage pour leur laisser les sommets
        decal = 0.12 if any(_BIOME[i].get("special") == "pics" for i in ids) else 0.0
        return [{"biome": f"{NS}:{i}", "parameters": {"temperature": list(t), "humidity": list(hh), "continentalness": list(c),
                 "erosion": list(e), "weirdness": list(wd), "depth": 0.0,
                 "offset": 0.0 if _BIOME[i].get("special") in ("pics", "ocean") else decal}} for i, t, hh, c, e, wd in res]

    _BIOME = {b["id"]: b for b in BIOMES}
    w(f"data/{NS}/dimension/royaumes_mortels.json", {
        "type": "minecraft:overworld",
        "generator": {"type": "minecraft:noise", "settings": DIM,
                      "biome_source": {"type": "minecraft:multi_noise", "biomes": points_royaume(data_v5.AZYR)}}})
    # Un monde par Royaume
    for did, dd in data_v4.DIMENSIONS.items():
        fl = bool(dd.get("flottant"))
        src = {"type": "minecraft:multi_noise", "biomes": points_royaume(dd["biomes"], fl)}
        reglages = f"{NS}:iles_flottantes" if fl else DIM
        w(f"data/{NS}/dimension/{did}.json", {"type": "minecraft:overworld",
                                              "generator": {"type": "minecraft:noise", "settings": reglages, "biome_source": src}})
    base = charger("worldgen/density_function/end/base_3d_noise.json")
    base["xz_scale"] = data_v5.HYSH_XZ_SCALE
    w(f"data/{NS}/worldgen/density_function/hysh_iles.json", base)
    nf = charger("worldgen/noise_settings/floating_islands.json")
    nf["material_rule"] = DIM
    nf = json.loads(json.dumps(nf).replace('"minecraft:end/base_3d_noise"', f'"{NS}:hysh_iles"'))
    for clim in ("temperature", "vegetation"):
        nf["noise_router"][clim] = f"{NS}:{clim}"
    w(f"data/{NS}/worldgen/noise_settings/iles_flottantes.json", nf)
    ns = charger("worldgen/noise_settings/overworld.json")
    ns["material_rule"] = DIM
    # Biomes ~3× plus grands : bruit climatique étiré
    for clim in ("temperature", "vegetation"):
        dfn = charger(f"worldgen/density_function/overworld/{clim}.json")
        dfn["xz_scale"] = 0.08
        w(f"data/{NS}/worldgen/density_function/{clim}.json", dfn)
        ns["noise_router"][clim] = f"{NS}:{clim}"
    w(f"data/{NS}/worldgen/noise_settings/royaumes_mortels.json", ns)
    # Règles de surface
    regles = []
    for b in BIOMES:
        s = b.get("surface")
        if not s:
            continue
        top_seq = []
        for blk, rng in s["top"][1:]:
            top_seq.append({"type": "minecraft:condition",
                            "if_true": {"type": "minecraft:noise_threshold", "noise": "minecraft:surface",
                                        "min_threshold": rng[0], "max_threshold": rng[1]},
                            "then_run": {"type": "minecraft:block", "result_state": blk}})
        top_seq.append({"type": "minecraft:block", "result_state": s["top"][0][0]})
        regles.append({"type": "minecraft:condition",
                       "if_true": {"type": "minecraft:biome", "biome_is": f"{NS}:{b['id']}"},
                       "then_run": {"type": "minecraft:sequence", "sequence": [
                           {"type": "minecraft:condition", "if_true": "minecraft:on_floor",
                            "then_run": {"type": "minecraft:sequence", "sequence": top_seq}},
                           {"type": "minecraft:condition", "if_true": "minecraft:under_floor",
                            "then_run": {"type": "minecraft:block", "result_state": s["under"]}}]}})
    w(f"data/{NS}/worldgen/material_rule/royaumes_mortels.json", {
        "type": "minecraft:sequence", "sequence": [
            "minecraft:bedrock_floor", "minecraft:overworld/copper_ore_vein", "minecraft:overworld/iron_ore_vein",
            {"type": "minecraft:condition", "if_true": {"type": "minecraft:above_preliminary_surface"},
             "then_run": {"type": "minecraft:sequence", "sequence": regles + ["minecraft:overworld/surface"]}},
            "minecraft:overworld/underground"]})
    # Titres de biomes
    lines = ["scoreboard players set @s rm_bnow 0"]
    for i, b in enumerate(BIOMES, start=1):
        lines.append(f"execute if biome ~ ~ ~ {NS}:{b['id']} run scoreboard players set @s rm_bnow {i}")
    lines.append(f"execute unless score @s rm_bnow = @s rm_biome run function {NS}:monde/biome_titre")
    fn("monde/biome_joueur", lines)
    lines = ["scoreboard players operation @s rm_biome = @s rm_bnow", "title @s times 10 50 20"]
    for i, b in enumerate(BIOMES, start=1):
        lines.append(f"execute if score @s rm_bnow matches {i} run title @s subtitle {jtxt(txt(b['sous'], 'gray', italic=True))}")
        lines.append(f"execute if score @s rm_bnow matches {i} run title @s title {jtxt(txt(b['nom'], b['c'], bold=True))}")
    fn("monde/biome_titre", lines)


# =========================================================================== MOBS
def gen_mobs():
    types = sorted({t for b in BIOMES for t in b["mobs"]})
    w(f"data/{NS}/tags/entity_type/convertibles.json", {"values": [f"minecraft:{t}" for t in types]})
    for pid, p in PROFILS.items():
        a = ALLIANCES[p["alliance"]]
        L = ["tag @s add rm_c", "tag @s remove rm_spawn", f"team join {p.get('team') or a['team']} @s"]
        if p["nom"]:
            L.append(f"data modify entity @s CustomName set value {jtxt(txt(p['nom'], p['c']))}")
        if p["base"] == "zombie":
            L.append(f"data modify entity @s IsBaby set value {'1b' if p['bebe'] else '0b'}")
        for attr, val in p["attrs"].items():
            L.append(f"attribute @s minecraft:{attr} base set {val}")
        if "max_health" in p["attrs"]:
            L.append(f"data modify entity @s Health set value {float(p['attrs']['max_health'])}f")
        for slot in p["equip"]:
            L.append(f"loot replace entity @s {slot} loot {NS}:equip/{pid}/{slot.replace('.', '_')}")
        for e, amp in p["effets"]:
            L.append(f"effect give @s minecraft:{e} infinite {amp} true")
        if p["base"] not in ("villager", "iron_golem"):
            L.append("effect give @s minecraft:fire_resistance infinite 0 true")
        if p.get("loot"):
            L.append(f'data modify entity @s DeathLootTable set value "{p["loot"]}"')
        L.extend(p.get("extra", []))
        fn(f"mobs/profil/{pid}", L)
    # Marqueurs posés dans les structures
    L = []
    for pid in PROFILS:
        L.append(f"execute if entity @s[tag=rm_p_{pid}] run return run function {NS}:mobs/profil/{pid}")
    L.append("tag @s remove rm_spawn")
    fn("mobs/marqueur", L)
    # Conversion des monstres selon le biome
    L = ["tag @s add rm_c"]
    for b in BIOMES:
        L.append(f"execute if biome ~ ~ ~ {NS}:{b['id']} run return run function {NS}:mobs/biome/{b['id']}")
    fn("mobs/convertir", L)
    for b in BIOMES:
        BL = []
        for t, opts in b["mobs"].items():
            BL.append(f"execute if entity @s[type=minecraft:{t}] run return run function {NS}:mobs/tirage/{b['id']}_{t}")
            TL = [f"execute store result score #r rm_tmp run random value 1..{len(opts)}"]
            for i, o in enumerate(opts, start=1):
                if o != "_":
                    TL.append(f"execute if score #r rm_tmp matches {i} run return run function {NS}:mobs/profil/{o}")
            fn(f"mobs/tirage/{b['id']}_{t}", TL)
        fn(f"mobs/biome/{b['id']}", BL or ["return 0"])


# =========================================================================== STRUCTURES
def gen_structures():
    from nbtgen import Struct  # noqa
    stats = {}
    for i, st in enumerate(STRUCTURES):
        sid = st["id"]
        s = BUILDERS[sid]()
        path = os.path.join(OUT, f"data/{NS}/structure/{sid}.nbt")
        os.makedirs(os.path.dirname(path), exist_ok=True)
        stats[sid] = (s.size, *s.save(path))
        w(f"data/{NS}/worldgen/template_pool/{sid}/debut.json", {
            "elements": [{"weight": 1, "element": {"element_type": "minecraft:single_pool_element",
                                                   "location": f"{NS}:{sid}", "processors": "minecraft:empty",
                                                   "projection": "rigid"}}],
            "fallback": "minecraft:empty"})
        w(f"data/{NS}/tags/worldgen/biome/has_structure/{sid}.json",
          {"values": [f"{NS}:{b}" for b in st["biomes"]] + [f"minecraft:{b}" for b in st["monde"]]})
        w(f"data/{NS}/worldgen/structure/{sid}.json", {
            "type": "minecraft:jigsaw", "biomes": f"#{NS}:has_structure/{sid}",
            "max_distance_from_center": 80,
            "project_start_to_heightmap": "OCEAN_FLOOR_WG" if st.get("ocean") else "WORLD_SURFACE_WG",
            "size": 1, "spawn_overrides": {},
            "start_height": {"absolute": START_Y[sid]},
            "start_pool": f"{NS}:{sid}/debut",
            "step": "surface_structures",
            "terrain_adaptation": "none" if (st.get("ocean") or st.get("flottant")) else "beard_box",
            "use_expansion_hack": False})
        w(f"data/{NS}/worldgen/structure_set/{sid}.json", {
            "placement": {"type": "minecraft:random_spread", "spacing": st["espacement"], "separation": st["sep"],
                          "salt": 735021 + i * 7919},
            "structures": [{"structure": f"{NS}:{sid}", "weight": 1}]})
    return stats


def gen_pack():
    w("pack.mcmeta", {"pack": {
        "description": [{"text": "Royaumes Mortels", "color": "gold", "bold": True},
                        {"text": "\nAge of Sigmar — projet fan non officiel", "color": "gray"}],
        "min_format": 121, "max_format": 121}})


if __name__ == "__main__":
    if os.path.exists(OUT):
        shutil.rmtree(OUT)
    import extension
    extension.preparer()
    import v4
    v4.preparer()
    EXTRA_FEATURES.update(v4.B.EXTRA_FEATURES)
    gen_pack(); gen_objets(); gen_coffres(); gen_enchantements(); gen_dialogues(); gen_fonctions_factions()
    gen_coeur(); gen_pierre(); gen_features(); gen_decors(); gen_biomes(); gen_dimension(); gen_mobs()
    stats = gen_structures()
    extension.generer()
    v4.generer()
    import v5gen
    v5gen.generer()
    import v6gen
    v6gen.generer()
    for k, v in stats.items():
        print(f"{k:24s} taille={v[0]} blocs={v[1]} mobs={v[2]}")
    n = sum(len(f) for _, _, f in os.walk(OUT))
    print("fichiers:", n)
