scoreboard players set @s rm_faction 13
team join rm_chaos @s
function royaumes:factions/dons/slaanesh
loot give @s loot royaumes:kits/slaanesh
dialog clear @s
title @s title {"text": "Hédonites de Lyssara", "color": "light_purple", "bold": true}
title @s subtitle {"text": "Grande Alliance : Chaos", "color": "dark_red"}
playsound minecraft:ui.toast.challenge_complete master @s ~ ~ ~ 1 1
tellraw @s [{"text": "» ", "color": "gold"}, {"text": "Adorateurs du Prince des Plaisirs, en quête d'excès et de perfection.", "color": "gray", "italic": true}]
tellraw @s [{"text": "» Dons : ", "color": "green"}, {"text": "Vitesse +15 %, vitesse d'attaque +20 %", "color": "green"}]
tellraw @s [{"text": "» Faiblesses : ", "color": "red"}, {"text": "-2 cœurs", "color": "red"}]
tellraw @s [{"text": "» Utilise ta ", "color": "gold"}, {"text": "Pierre de Royaume", "color": "light_purple"}, {"text": " (clic droit) pour rejoindre les Royaumes Mortels.", "color": "gold"}]
tellraw @a [{"text": "⚔ ", "color": "gold"}, {"selector": "@s"}, {"text": " a rejoint : ", "color": "gray"}, {"text": "Hédonites de Lyssara", "color": "light_purple"}]
