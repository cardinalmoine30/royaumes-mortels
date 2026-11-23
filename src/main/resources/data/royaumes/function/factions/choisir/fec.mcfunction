scoreboard players set @s rm_faction 20
team join rm_mort @s
function royaumes:factions/dons/fec
loot give @s loot royaumes:kits/fec
dialog clear @s
title @s title {"text": "Cours Cannibales", "color": "dark_purple", "bold": true}
title @s subtitle {"text": "Grande Alliance : Mort", "color": "dark_purple"}
playsound minecraft:ui.toast.challenge_complete master @s ~ ~ ~ 1 1
tellraw @s [{"text": "» ", "color": "gold"}, {"text": "Goules folles qui se croient nobles chevaliers d'une cour glorieuse.", "color": "gray", "italic": true}]
tellraw @s [{"text": "» Dons : ", "color": "green"}, {"text": "Vitesse +10 %, saut +, +1 dégât", "color": "green"}]
tellraw @s [{"text": "» Faiblesses : ", "color": "red"}, {"text": "Leur « festin » est de la chair pourrie", "color": "red"}]
tellraw @s [{"text": "» Utilise ta ", "color": "gold"}, {"text": "Pierre de Royaume", "color": "light_purple"}, {"text": " (clic droit) pour rejoindre les Royaumes Mortels.", "color": "gold"}]
tellraw @a [{"text": "⚔ ", "color": "gold"}, {"selector": "@s"}, {"text": " a rejoint : ", "color": "gray"}, {"text": "Cours Cannibales", "color": "dark_purple"}]
