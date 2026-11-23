scoreboard players set @s rm_faction 11
team join rm_chaos @s
function royaumes:factions/dons/khorne
loot give @s loot royaumes:kits/khorne
dialog clear @s
title @s title {"text": "Lames de Khorne", "color": "dark_red", "bold": true}
title @s subtitle {"text": "Grande Alliance : Chaos", "color": "dark_red"}
playsound minecraft:ui.toast.challenge_complete master @s ~ ~ ~ 1 1
tellraw @s [{"text": "» ", "color": "gold"}, {"text": "« Du sang pour le Dieu du Sang ! » Berserkers dévoués au carnage.", "color": "gray", "italic": true}]
tellraw @s [{"text": "» Dons : ", "color": "green"}, {"text": "Force I, vitesse d'attaque +10 %", "color": "green"}]
tellraw @s [{"text": "» Faiblesses : ", "color": "red"}, {"text": "-2 armure (Khorne méprise la prudence)", "color": "red"}]
tellraw @s [{"text": "» Utilise ta ", "color": "gold"}, {"text": "Pierre de Royaume", "color": "light_purple"}, {"text": " (clic droit) pour rejoindre les Royaumes Mortels.", "color": "gold"}]
tellraw @a [{"text": "⚔ ", "color": "gold"}, {"selector": "@s"}, {"text": " a rejoint : ", "color": "gray"}, {"text": "Lames de Khorne", "color": "dark_red"}]
