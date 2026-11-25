scoreboard players set @s rm_faction 7
team join rm_ordre @s
function royaumes:factions/dons/lumineth
loot give @s loot royaumes:kits/lumineth
dialog clear @s
title @s title {"text": "Seigneurs de Lumière", "color": "white", "bold": true}
title @s subtitle {"text": "Grande Alliance : Ordre", "color": "gold"}
playsound minecraft:ui.toast.challenge_complete master @s ~ ~ ~ 1 1
tellraw @s [{"text": "» ", "color": "gold"}, {"text": "Elfes de la lumière, maîtres des arts élémentaires et de la perfection.", "color": "gray", "italic": true}]
tellraw @s [{"text": "» Dons : ", "color": "green"}, {"text": "Vision nocturne, vitesse +5 %, +1 chance, portée +1", "color": "green"}]
tellraw @s [{"text": "» Faiblesses : ", "color": "red"}, {"text": "Aucun", "color": "red"}]
tellraw @s [{"text": "» Utilise ta ", "color": "gold"}, {"text": "Pierre de Royaume", "color": "light_purple"}, {"text": " (clic droit) pour rejoindre les Royaumes Mortels.", "color": "gold"}]
tellraw @a [{"text": "⚔ ", "color": "gold"}, {"selector": "@s"}, {"text": " a rejoint : ", "color": "gray"}, {"text": "Seigneurs de Lumière", "color": "white"}]
