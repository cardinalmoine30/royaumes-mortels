scoreboard players set @s rm_faction 15
team join rm_chaos @s
function royaumes:factions/dons/skaven
loot give @s loot royaumes:kits/skaven
dialog clear @s
title @s title {"text": "Skaven", "color": "green", "bold": true}
title @s subtitle {"text": "Grande Alliance : Chaos", "color": "dark_red"}
playsound minecraft:ui.toast.challenge_complete master @s ~ ~ ~ 1 1
tellraw @s [{"text": "» ", "color": "gold"}, {"text": "Hommes-rats du Grand Rat Cornu, maîtres de la malepierre et des tunnels.", "color": "gray", "italic": true}]
tellraw @s [{"text": "» Dons : ", "color": "green"}, {"text": "Vitesse +15 %, vision nocturne", "color": "green"}]
tellraw @s [{"text": "» Faiblesses : ", "color": "red"}, {"text": "Taille -20 %, -2 cœurs", "color": "red"}]
tellraw @s [{"text": "» Utilise ta ", "color": "gold"}, {"text": "Pierre de Royaume", "color": "light_purple"}, {"text": " (clic droit) pour rejoindre les Royaumes Mortels.", "color": "gold"}]
tellraw @a [{"text": "⚔ ", "color": "gold"}, {"selector": "@s"}, {"text": " a rejoint : ", "color": "gray"}, {"text": "Skaven", "color": "green"}]
