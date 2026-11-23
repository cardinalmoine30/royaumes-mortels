scoreboard players set @s rm_faction 16
team join rm_chaos @s
function royaumes:factions/dons/hashut
loot give @s loot royaumes:kits/hashut
dialog clear @s
title @s title {"text": "Forgerons de Hashut", "color": "gold", "bold": true}
title @s subtitle {"text": "Grande Alliance : Chaos", "color": "dark_red"}
playsound minecraft:ui.toast.challenge_complete master @s ~ ~ ~ 1 1
tellraw @s [{"text": "» ", "color": "gold"}, {"text": "Duardins du Chaos, serviteurs du Père des Ténèbres, maîtres des forges infernales.", "color": "gray", "italic": true}]
tellraw @s [{"text": "» Dons : ", "color": "green"}, {"text": "Résistance au feu, +4 armure", "color": "green"}]
tellraw @s [{"text": "» Faiblesses : ", "color": "red"}, {"text": "Taille -15 %, vitesse -5 %", "color": "red"}]
tellraw @s [{"text": "» Utilise ta ", "color": "gold"}, {"text": "Pierre de Royaume", "color": "light_purple"}, {"text": " (clic droit) pour rejoindre les Royaumes Mortels.", "color": "gold"}]
tellraw @a [{"text": "⚔ ", "color": "gold"}, {"selector": "@s"}, {"text": " a rejoint : ", "color": "gray"}, {"text": "Forgerons de Hashut", "color": "gold"}]
