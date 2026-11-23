scoreboard players set @s rm_faction 17
team join rm_mort @s
function royaumes:factions/dons/nighthaunt
loot give @s loot royaumes:kits/nighthaunt
dialog clear @s
title @s title {"text": "Nighthaunt", "color": "dark_aqua", "bold": true}
title @s subtitle {"text": "Grande Alliance : Mort", "color": "dark_purple"}
playsound minecraft:ui.toast.challenge_complete master @s ~ ~ ~ 1 1
tellraw @s [{"text": "» ", "color": "gold"}, {"text": "Spectres condamnés par Nagash, hurlant à travers les Royaumes.", "color": "gray", "italic": true}]
tellraw @s [{"text": "» Dons : ", "color": "green"}, {"text": "Gravité réduite, chute sûre +10, vitesse +5 %", "color": "green"}]
tellraw @s [{"text": "» Faiblesses : ", "color": "red"}, {"text": "-2 cœurs", "color": "red"}]
tellraw @s [{"text": "» Utilise ta ", "color": "gold"}, {"text": "Pierre de Royaume", "color": "light_purple"}, {"text": " (clic droit) pour rejoindre les Royaumes Mortels.", "color": "gold"}]
tellraw @a [{"text": "⚔ ", "color": "gold"}, {"selector": "@s"}, {"text": " a rejoint : ", "color": "gray"}, {"text": "Nighthaunt", "color": "dark_aqua"}]
