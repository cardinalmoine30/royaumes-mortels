scoreboard players set @s rm_faction 9
team join rm_ordre @s
function royaumes:factions/dons/sylvaneth
loot give @s loot royaumes:kits/sylvaneth
dialog clear @s
title @s title {"text": "Sylvaneth", "color": "dark_green", "bold": true}
title @s subtitle {"text": "Grande Alliance : Ordre", "color": "gold"}
playsound minecraft:ui.toast.challenge_complete master @s ~ ~ ~ 1 1
tellraw @s [{"text": "» ", "color": "gold"}, {"text": "Esprits-arbres enfants d'Alarielle, la Reine Éternelle.", "color": "gray", "italic": true}]
tellraw @s [{"text": "» Dons : ", "color": "green"}, {"text": "Régénération permanente, +2 cœurs", "color": "green"}]
tellraw @s [{"text": "» Faiblesses : ", "color": "red"}, {"text": "Brûle 2× plus longtemps, vitesse -5 %", "color": "red"}]
tellraw @s [{"text": "» Utilise ta ", "color": "gold"}, {"text": "Pierre de Royaume", "color": "light_purple"}, {"text": " (clic droit) pour rejoindre les Royaumes Mortels.", "color": "gold"}]
tellraw @a [{"text": "⚔ ", "color": "gold"}, {"selector": "@s"}, {"text": " a rejoint : ", "color": "gray"}, {"text": "Sylvaneth", "color": "dark_green"}]
