scoreboard players set @s rm_faction 6
team join rm_ordre @s
function royaumes:factions/dons/idoneth
loot give @s loot royaumes:kits/idoneth
dialog clear @s
title @s title {"text": "Idoneth Deepkin", "color": "dark_aqua", "bold": true}
title @s subtitle {"text": "Grande Alliance : Ordre", "color": "gold"}
playsound minecraft:ui.toast.challenge_complete master @s ~ ~ ~ 1 1
tellraw @s [{"text": "» ", "color": "gold"}, {"text": "Aelfs sans âme des profondeurs, qui chassent les âmes des vivants lors de leurs raids.", "color": "gray", "italic": true}]
tellraw @s [{"text": "» Dons : ", "color": "green"}, {"text": "Respiration aquatique, nage +60 %, minage sous l'eau", "color": "green"}]
tellraw @s [{"text": "» Faiblesses : ", "color": "red"}, {"text": "Lent hors de l'eau (aucun bonus terrestre)", "color": "red"}]
tellraw @s [{"text": "» Utilise ta ", "color": "gold"}, {"text": "Pierre de Royaume", "color": "light_purple"}, {"text": " (clic droit) pour rejoindre les Royaumes Mortels.", "color": "gold"}]
tellraw @a [{"text": "⚔ ", "color": "gold"}, {"selector": "@s"}, {"text": " a rejoint : ", "color": "gray"}, {"text": "Idoneth Deepkin", "color": "dark_aqua"}]
