scoreboard players set @s rm_faction 8
team join rm_ordre @s
function royaumes:factions/dons/seraphon
loot give @s loot royaumes:kits/seraphon
dialog clear @s
title @s title {"text": "Astrosauriens", "color": "green", "bold": true}
title @s subtitle {"text": "Grande Alliance : Ordre", "color": "gold"}
playsound minecraft:ui.toast.challenge_complete master @s ~ ~ ~ 1 1
tellraw @s [{"text": "» ", "color": "gold"}, {"text": "Hommes-lézards célestes guidés par les Sage-Crapaud, forces de l'ordre cosmique.", "color": "gray", "italic": true}]
tellraw @s [{"text": "» Dons : ", "color": "green"}, {"text": "Taille +20 %, +2 cœurs, +4 armure, nage +30 %", "color": "green"}]
tellraw @s [{"text": "» Faiblesses : ", "color": "red"}, {"text": "Vitesse -5 %", "color": "red"}]
tellraw @s [{"text": "» Utilise ta ", "color": "gold"}, {"text": "Pierre de Royaume", "color": "light_purple"}, {"text": " (clic droit) pour rejoindre les Royaumes Mortels.", "color": "gold"}]
tellraw @a [{"text": "⚔ ", "color": "gold"}, {"selector": "@s"}, {"text": " a rejoint : ", "color": "gray"}, {"text": "Astrosauriens", "color": "green"}]
