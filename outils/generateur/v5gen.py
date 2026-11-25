# -*- coding: utf-8 -*-
"""v5 : le joueur CHOISIT le Royaume où il va (Pierre de Royaume et portails ouvrent une carte des Royaumes)."""
import json, os
import build as B
import data_v4
from build import NS, OUT, fn, txt, jtxt

DESC = {
    "royaumes_mortels": "Célestis : pics foudroyés des forteresses Foudroyés et Célestheim, la cité de Aurion.",
    "ghyran": "Sylvéa : jungles des Astrosauriens, bois Sylvains, marais convoités par Morbus.",
    "aqshy": "Pyréa : volcans des Tueurs-de-Braise, cendres de Sangrath et ziggurats de Ashkar.",
    "shyish": "Nécréa : terres de Necrath, nécropoles Sanguinaire et déserts d'os Faucheurs d'Os.",
    "ghur": "Féralia : savanes des mégafaunes, Orcs, Ogres et Géants.",
    "chamon": "Ferrumia : collines de métal et ports volants Nuées.",
    "ulgu": "Umbria : brumes des Filles de Morvaine, mer des Abyssal, marais Gobelins.",
    "hysh": "Lumina : îles célestes et sanctuaires de Lumière.",
    "huit_points": "Les Huit-Voies : désolation du Chaos et Terres Rongées des Hommes-Rats.",
}


def royaumes():
    l = [("royaumes_mortels", "Célestis, Royaume des Cieux", "aqua")]
    l += [(d, v["nom"], v["c"]) for d, v in data_v4.DIMENSIONS.items()]
    return l


def generer():
    R = royaumes()
    actions = []
    for i, (did, nom, c) in enumerate(R, start=1):
        actions.append({"label": {"text": nom.split(",")[0], "color": c, "bold": True}, "tooltip": {"text": DESC[did]},
                        "width": 150, "action": {"type": "run_command", "command": f"trigger rm_voyage set {i}"}})
    actions.append({"label": {"text": "Monde-Pont (retour)", "color": "white"}, "tooltip": {"text": "Revenir dans le monde départ."},
                    "width": 150, "action": {"type": "run_command", "command": "trigger rm_voyage set 99"}})
    B.w(f"data/{NS}/dialog/voyage.json", {
        "type": "minecraft:multi_action",
        "title": {"text": "✦ Carte des Royaumes Mortels ✦", "color": "light_purple", "bold": True},
        "body": [{"type": "minecraft:plain_message", "width": 300, "contents": [
            {"text": "Où veux-tu aller ?\n", "color": "yellow"},
            {"text": "Survole un Royaume pour voir ce qu'on y trouve.", "color": "gray"}]}],
        "can_close_with_escape": True, "columns": 2, "actions": actions})

    ouvrir = ["scoreboard players enable @s rm_voyage", "scoreboard players set @s rm_voyage 0", f"dialog show @s {NS}:voyage"]
    item = f"minecraft:carrot_on_a_stick[minecraft:custom_data~{{royaumes:\"pierre\"}}]"
    fn("pierre/utiliser", [
        "scoreboard players set @s rm_pierre 0",
        f"execute unless items entity @s weapon.* {item} run return 0",
        f"execute if score @s rm_cd matches 1.. run return run title @s actionbar {jtxt(txt('La Pierre de Royaume se recharge…', 'gray'))}",
        "scoreboard players set @s rm_cd 3",
        "particle minecraft:reverse_portal ~ ~1 ~ 0.4 1 0.4 0.05 80",
        "playsound minecraft:block.respawn_anchor.set_spawn player @a ~ ~ ~ 1 0.8"] + ouvrir)
    fn("faille/voyager", [
        f"function {NS}:faille/repousser",
        "execute if score @s rm_cd matches 1.. run return 0",
        "scoreboard players set @s rm_cd 4",
        "particle minecraft:reverse_portal ~ ~1 ~ 0.5 1 0.5 0.2 120",
        "playsound minecraft:block.portal.trigger player @s ~ ~ ~ 0.4 1.3"] + ouvrir)
    fn("pierre/portail", ["scoreboard players set @s rm_cd 4"] + ouvrir)
    L = ["# Voyage vers le Royaume choisi dans la carte (trigger rm_voyage)",
         "particle minecraft:reverse_portal ~ ~1 ~ 0.5 1 0.5 0.2 120",
         "playsound minecraft:block.portal.travel player @s ~ ~ ~ 0.4 1.3"]
    for i, (did, nom, c) in enumerate(R, start=1):
        L.append(f'execute if score @s rm_voyage matches {i} run function {NS}:faille/vers {{dim:"{NS}:{did}",nom:"{nom}",c:"{c}"}}')
    L.append(f"execute if score @s rm_voyage matches 99 run function {NS}:pierre/vers_monde")
    L.append("scoreboard players set @s rm_voyage 0")
    fn("voyage/aller", L)
    # sous-titre du voyage : plus "terre inconnue", puisque c'est un choix
    p = f"{OUT}/data/{NS}/function/faille/vers.mcfunction"
    t = open(p, encoding="utf-8").read().replace("Le portail vous a mené en terre inconnue…", "Le voyage à travers les Royaumes est accompli.")
    open(p, "w", encoding="utf-8").write(t)
    base = f"{OUT}/data/{NS}/function"
    for f, lignes in (("tick", [f"execute as @a[scores={{rm_voyage=1..}}] at @s run function {NS}:voyage/aller"]),
                      ("rpg/load", ["scoreboard objectives add rm_voyage trigger"])):
        q = f"{base}/{f}.mcfunction"
        open(q, "a", encoding="utf-8").write("\n".join(lignes) + "\n")
