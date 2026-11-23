scoreboard players set @s rm_faction 22
team join rm_destruction @s
function royaumes:factions/dons/kruleboyz
loot give @s loot royaumes:kits/kruleboyz
dialog clear @s
title @s title {"text": "Kruleboyz", "color": "dark_green", "bold": true}
title @s subtitle {"text": "Grande Alliance : Destruction", "color": "dark_green"}
playsound minecraft:ui.toast.challenge_complete master @s ~ ~ ~ 1 1
tellraw @s [{"text": "» ", "color": "gold"}, {"text": "Orruks des marais, rusés et cruels, adeptes des lames empoisonnées et des pièges.", "color": "gray", "italic": true}]
tellraw @s [{"text": "» Dons : ", "color": "green"}, {"text": "+1 cœur, déplacement accroupi +30 %", "color": "green"}]
tellraw @s [{"text": "» Faiblesses : ", "color": "red"}, {"text": "Aucun", "color": "red"}]
tellraw @s [{"text": "» Utilise ta ", "color": "gold"}, {"text": "Pierre de Royaume", "color": "light_purple"}, {"text": " (clic droit) pour rejoindre les Royaumes Mortels.", "color": "gold"}]
tellraw @a [{"text": "⚔ ", "color": "gold"}, {"selector": "@s"}, {"text": " a rejoint : ", "color": "gray"}, {"text": "Kruleboyz", "color": "dark_green"}]
