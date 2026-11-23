scoreboard players set @s rm_faction 2
team join rm_ordre @s
function royaumes:factions/dons/cites
loot give @s loot royaumes:kits/cites
dialog clear @s
title @s title {"text": "Cités de Sigmar", "color": "aqua", "bold": true}
title @s subtitle {"text": "Grande Alliance : Ordre", "color": "gold"}
playsound minecraft:ui.toast.challenge_complete master @s ~ ~ ~ 1 1
tellraw @s [{"text": "» ", "color": "gold"}, {"text": "Humains, aelfs et duardins des grandes cités libres, comme Hammerhal ou Excelsis.", "color": "gray", "italic": true}]
tellraw @s [{"text": "» Dons : ", "color": "green"}, {"text": "Héros du village (rabais marchands), +1 chance, +1 cœur", "color": "green"}]
tellraw @s [{"text": "» Faiblesses : ", "color": "red"}, {"text": "Aucun don surnaturel", "color": "red"}]
tellraw @s [{"text": "» Utilise ta ", "color": "gold"}, {"text": "Pierre de Royaume", "color": "light_purple"}, {"text": " (clic droit) pour rejoindre les Royaumes Mortels.", "color": "gold"}]
tellraw @a [{"text": "⚔ ", "color": "gold"}, {"selector": "@s"}, {"text": " a rejoint : ", "color": "gray"}, {"text": "Cités de Sigmar", "color": "aqua"}]
