scoreboard players set @s rm_faction 4
team join rm_ordre @s
function royaumes:factions/dons/kharadron
loot give @s loot royaumes:kits/kharadron
dialog clear @s
title @s title {"text": "Seigneurs des Nuées", "color": "gold", "bold": true}
title @s subtitle {"text": "Grande Alliance : Ordre", "color": "gold"}
playsound minecraft:ui.toast.challenge_complete master @s ~ ~ ~ 1 1
tellraw @s [{"text": "» ", "color": "gold"}, {"text": "Nains du ciel, marchands et pilotes de navires volants propulsés à l'aether-or.", "color": "gray", "italic": true}]
tellraw @s [{"text": "» Dons : ", "color": "green"}, {"text": "Dégâts de chute -50 %, chute sûre +6 blocs", "color": "green"}]
tellraw @s [{"text": "» Faiblesses : ", "color": "red"}, {"text": "Taille -15 %", "color": "red"}]
tellraw @s [{"text": "» Utilise ta ", "color": "gold"}, {"text": "Pierre de Royaume", "color": "light_purple"}, {"text": " (clic droit) pour rejoindre les Royaumes Mortels.", "color": "gold"}]
tellraw @a [{"text": "⚔ ", "color": "gold"}, {"selector": "@s"}, {"text": " a rejoint : ", "color": "gray"}, {"text": "Seigneurs des Nuées", "color": "gold"}]
