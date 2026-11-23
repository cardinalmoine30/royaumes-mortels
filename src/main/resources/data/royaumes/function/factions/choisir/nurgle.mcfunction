scoreboard players set @s rm_faction 14
team join rm_chaos @s
function royaumes:factions/dons/nurgle
loot give @s loot royaumes:kits/nurgle
dialog clear @s
title @s title {"text": "Maggotkin de Nurgle", "color": "dark_green", "bold": true}
title @s subtitle {"text": "Grande Alliance : Chaos", "color": "dark_red"}
playsound minecraft:ui.toast.challenge_complete master @s ~ ~ ~ 1 1
tellraw @s [{"text": "» ", "color": "gold"}, {"text": "Enfants du Grand-Père Nurgle, porteurs de pestes joyeuses et d'une endurance infinie.", "color": "gray", "italic": true}]
tellraw @s [{"text": "» Dons : ", "color": "green"}, {"text": "+4 cœurs, régénération, +1 armure", "color": "green"}]
tellraw @s [{"text": "» Faiblesses : ", "color": "red"}, {"text": "Vitesse -10 %", "color": "red"}]
tellraw @s [{"text": "» Utilise ta ", "color": "gold"}, {"text": "Pierre de Royaume", "color": "light_purple"}, {"text": " (clic droit) pour rejoindre les Royaumes Mortels.", "color": "gold"}]
tellraw @a [{"text": "⚔ ", "color": "gold"}, {"selector": "@s"}, {"text": " a rejoint : ", "color": "gray"}, {"text": "Maggotkin de Nurgle", "color": "dark_green"}]
