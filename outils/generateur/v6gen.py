# -*- coding: utf-8 -*-
"""v6 : montures de faction (Corne d'appel), onglet « Blocs » de l'inventaire de taverne, Codex enrichi."""
import json
import os
import sys
import build as B
from build import NS, OUT, fn, txt, jtxt, w
from data_factions import FACTIONS

LISTE = "/home/claude/royaumes-mortels/outils/modeles/liste_montures.json"

CORNE = {"id": "minecraft:carrot_on_a_stick", "nom": "Corne d'appel", "c": "gold",
         "lore": ["Clic droit : appelle la monture de ta faction", "et te met en selle. Sneak + clic droit sur",
                  "la monture : la laisser. Saut : barre de saut,", "monture volante : regarde où tu veux aller."],
         "item_model": "minecraft:goat_horn", "unbreakable": True, "rarity": "rare",
         "custom_data": {"royaumes": "monture"}}
PRED = 'minecraft:carrot_on_a_stick[minecraft:custom_data~{royaumes:"monture"}]'
GIVE = ('minecraft:carrot_on_a_stick[minecraft:custom_data={royaumes:"monture"},minecraft:item_model="minecraft:goat_horn",'
        'minecraft:unbreakable={},minecraft:rarity="rare",'
        'minecraft:custom_name={"text":"Corne d\'appel","color":"gold","italic":false},'
        'minecraft:lore=[{"text":"Clic droit : appelle la monture de ta faction.","color":"gray","italic":true}]]')


def ajouter(f, lignes, debut=False):
    p = f"{OUT}/data/{NS}/function/{f}.mcfunction"
    t = open(p, encoding="utf-8").read() if os.path.exists(p) else ""
    t = ("\n".join(lignes) + "\n" + t) if debut else (t.rstrip("\n") + "\n" + "\n".join(lignes) + "\n")
    open(p, "w", encoding="utf-8").write(t)


def montures():
    liste = json.load(open(LISTE, encoding="utf-8"))          # écrite par outils/modeles/montures.py
    par_fac = {m["faction"]: m["id"] for m in liste}
    ids = [f"{NS}:{m['id']}" for m in liste]
    w(f"data/{NS}/tags/entity_type/montures.json", {"values": ids})
    L = ["# Corne d'appel : rappelle (ou fait naître) la monture de la faction du joueur, puis le met en selle",
         "execute unless score @s rm_faction matches 1.. run return run title @s actionbar "
         + jtxt(txt("Choisis d'abord une faction : ta monture en dépend.", "red")),
         "execute if score @s rm_cdm matches 1.. run return run title @s actionbar "
         + jtxt(txt("La corne résonne encore…", "gray")),
         "scoreboard players set @s rm_cdm 4",
         "execute unless score @s rm_id matches 1.. run function royaumes:monture/numero",
         "scoreboard players operation #id rm_tmp = @s rm_id",
         "playsound minecraft:item.goat_horn.sound.0 player @a ~ ~ ~ 1.2 0.9",
         f"execute as @e[type=#{NS}:montures,distance=..256] if score @s rm_id = #id rm_tmp run tag @s add rm_trouvee",
         f"execute if entity @e[type=#{NS}:montures,tag=rm_trouvee,distance=..256] run return run function {NS}:monture/rappeler"]
    for f in FACTIONS:
        m = par_fac.get(f["id"])
        if m:
            L.append(f"execute if score @s rm_faction matches {f['num']} run summon {NS}:{m} ~ ~ ~ "
                     f"{{Tags:[\"rm_nouvelle\"],PersistenceRequired:1b}}")
    L += [f"scoreboard players operation @e[type=#{NS}:montures,tag=rm_nouvelle,distance=..4] rm_id = #id rm_tmp",
          f"ride @s mount @e[type=#{NS}:montures,tag=rm_nouvelle,limit=1,sort=nearest]",
          f"tag @e[type=#{NS}:montures,tag=rm_nouvelle] remove rm_nouvelle",
          "particle minecraft:cloud ~ ~0.5 ~ 0.8 0.3 0.8 0.02 30",
          "title @s actionbar " + jtxt(txt("Ta monture répond à l'appel !", "gold"))]
    fn("monture/appeler", L)
    fn("monture/rappeler", [
        f"tp @e[type=#{NS}:montures,tag=rm_trouvee,limit=1,sort=nearest] @s",
        f"ride @s mount @e[type=#{NS}:montures,tag=rm_trouvee,limit=1,sort=nearest]",
        f"tag @e[type=#{NS}:montures,tag=rm_trouvee] remove rm_trouvee",
        "particle minecraft:cloud ~ ~0.5 ~ 0.8 0.3 0.8 0.02 20",
        "title @s actionbar " + jtxt(txt("Ta monture accourt à ton appel.", "gold"))])
    fn("monture/numero", ["scoreboard players add #suivant rm_id 1", "scoreboard players operation @s rm_id = #suivant rm_id"])
    fn("monture/donner", [f"give @s {GIVE}", "tag @s add rm_corne",
                          "tellraw @s " + jtxt(txt("✦ Tu reçois une ", "gold"), txt("Corne d'appel", "yellow"),
                                               txt(" : clic droit pour appeler la monture de ta faction.", "gold"))])
    # branchement : clic droit, boucle, chargement
    p = f"{OUT}/data/{NS}/function/objets/utiliser.mcfunction"
    t = open(p, encoding="utf-8").read().rstrip("\n").split("\n")
    t.insert(len(t) - 1, f"execute if items entity @s weapon.mainhand {PRED} run return run function {NS}:monture/appeler")
    open(p, "w", encoding="utf-8").write("\n".join(t) + "\n")
    ajouter("rpg/load", ["scoreboard objectives add rm_id dummy", "scoreboard objectives add rm_cdm dummy"])
    ajouter("boucle_seconde", ["scoreboard players remove @a[scores={rm_cdm=1..}] rm_cdm 1",
                               f"execute as @a[tag=!rm_corne,scores={{rm_faction=1..}}] run function {NS}:monture/donner"])
    # la corne fait partie du paquetage de chaque faction
    for f in FACTIONS:
        p = f"{OUT}/data/{NS}/loot_table/kits/{f['id']}.json"
        if os.path.exists(p):
            d = json.load(open(p, encoding="utf-8"))
            d["pools"].append({"rolls": 1, "entries": [B.entry(CORNE)]})
            json.dump(d, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    return ids


def blocs():
    res = json.load(open(f"{OUT}/data/{NS}/dialog/ressources.json", encoding="utf-8"))
    corps = res["body"]
    w(f"data/{NS}/dialog/blocs.json", {
        "type": "minecraft:multi_action",
        "title": {"text": "Blocs et ressources des Royaumes", "color": "light_purple", "bold": True},
        "external_title": {"text": "Blocs des Royaumes", "color": "light_purple"},
        "body": corps,
        "can_close_with_escape": True, "pause": False, "columns": 2,
        "actions": [
            {"label": {"text": "Forge des Royaumes", "color": "gold"}, "width": 150,
             "tooltip": {"text": "Ce que l'on fabrique avec ces ressources"},
             "action": {"type": "run_command", "command": "trigger rm_forge"}},
            {"label": {"text": "Tout recevoir (créatif)", "color": "aqua"}, "width": 150,
             "tooltip": {"text": "Réservé aux opérateurs : tonneaux de tous les objets et blocs du mod"},
             "action": {"type": "run_command", "command": f"function {NS}:debug/objets"}}],
        "exit_action": {"label": {"text": "Fermer"}, "width": 100}})
    fn("blocs/ouvrir", ["scoreboard players set @s rm_blocs 0", "scoreboard players enable @s rm_blocs",
                        f"dialog show @s {NS}:blocs"])
    ajouter("rpg/load", ["scoreboard objectives add rm_blocs trigger"])
    ajouter("tick", [f"execute as @a[scores={{rm_blocs=1..}}] run function {NS}:blocs/ouvrir"])
    ajouter("boucle_seconde", ["scoreboard players enable @a rm_blocs", "scoreboard players enable @a rm_codex"])
    w("data/minecraft/tags/dialog/quick_actions.json", {"replace": False, "values": [
        f"{NS}:codex", f"{NS}:fiche", f"{NS}:forge", f"{NS}:blocs"]})


def codex():
    p = f"{OUT}/data/{NS}/dialog/codex.json"
    d = json.load(open(p, encoding="utf-8"))
    cont = d["body"][0]["contents"]
    cont += [
        {"text": "Montures de faction\n", "color": "aqua", "bold": True},
        {"text": "La Corne d'appel (clic droit) fait venir la monture de ta faction et te met en selle : Dracoth, "
                 "Destrier, Magmadroth, Gunhauler, Ishlaen, Aggradon, Juggernaut, Disque de Tzeentch, Squig, Mournfang… "
                 "Barre d'espace : sauter. Montures volantes : avance en regardant vers le haut ou le bas. "
                 "Sneak + clic droit sur la monture : la laisser. Elles amortissent toutes les chutes.\n\n", "color": "white"},
        {"text": "Inventaire de taverne\n", "color": "gold", "bold": True},
        {"text": "Ouvre ton inventaire (E) : les onglets Codex, Forge, Blocs et Héros mènent aux menus du jeu, "
                 "et le Carnet du Héros affiche ton niveau, ta gloire et tes compétences.\n\n", "color": "white"}]
    json.dump(d, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=2)


def generer():
    ids = montures()
    blocs()
    codex()
    print("v6 :", len(ids), "montures, onglet Blocs, Codex enrichi")
