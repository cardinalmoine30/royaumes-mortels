scoreboard players set @s rm_faction 1
team join rm_ordre @s
function royaumes:factions/dons/stormcast
loot give @s loot royaumes:kits/stormcast
dialog clear @s
title @s title {"text": "Foudroyés Éternels", "color": "gold", "bold": true}
title @s subtitle {"text": "Grande Alliance : Ordre", "color": "gold"}
playsound minecraft:ui.toast.challenge_complete master @s ~ ~ ~ 1 1
tellraw @s [{"text": "» ", "color": "gold"}, {"text": "Héros mortels forgés à nouveau par Aurion et lancés au combat par la foudre.", "color": "gray", "italic": true}]
tellraw @s [{"text": "» Dons : ", "color": "green"}, {"text": "Taille +15 %, +3 cœurs, +2 armure", "color": "green"}]
tellraw @s [{"text": "» Faiblesses : ", "color": "red"}, {"text": "Vitesse -5 %", "color": "red"}]
tellraw @s [{"text": "» Utilise ta ", "color": "gold"}, {"text": "Pierre de Royaume", "color": "light_purple"}, {"text": " (clic droit) pour rejoindre les Royaumes Mortels.", "color": "gold"}]
tellraw @a [{"text": "⚔ ", "color": "gold"}, {"selector": "@s"}, {"text": " a rejoint : ", "color": "gray"}, {"text": "Foudroyés Éternels", "color": "gold"}]
