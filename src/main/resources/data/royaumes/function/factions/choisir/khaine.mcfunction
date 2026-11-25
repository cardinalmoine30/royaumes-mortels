scoreboard players set @s rm_faction 5
team join rm_ordre @s
function royaumes:factions/dons/khaine
loot give @s loot royaumes:kits/khaine
dialog clear @s
title @s title {"text": "Filles de Morvaine", "color": "red", "bold": true}
title @s subtitle {"text": "Grande Alliance : Ordre", "color": "gold"}
playsound minecraft:ui.toast.challenge_complete master @s ~ ~ ~ 1 1
tellraw @s [{"text": "» ", "color": "gold"}, {"text": "Elfes fanatiques vouées au dieu du meurtre, guidées par Morvaine.", "color": "gray", "italic": true}]
tellraw @s [{"text": "» Dons : ", "color": "green"}, {"text": "Vitesse +10 %, vitesse d'attaque +15 %", "color": "green"}]
tellraw @s [{"text": "» Faiblesses : ", "color": "red"}, {"text": "-1 cœur", "color": "red"}]
tellraw @s [{"text": "» Utilise ta ", "color": "gold"}, {"text": "Pierre de Royaume", "color": "light_purple"}, {"text": " (clic droit) pour rejoindre les Royaumes Mortels.", "color": "gold"}]
tellraw @a [{"text": "⚔ ", "color": "gold"}, {"selector": "@s"}, {"text": " a rejoint : ", "color": "gray"}, {"text": "Filles de Morvaine", "color": "red"}]
