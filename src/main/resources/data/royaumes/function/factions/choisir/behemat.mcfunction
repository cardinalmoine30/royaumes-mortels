scoreboard players set @s rm_faction 25
team join rm_destruction @s
function royaumes:factions/dons/behemat
loot give @s loot royaumes:kits/behemat
dialog clear @s
title @s title {"text": "Fils d'Ymorath", "color": "dark_green", "bold": true}
title @s subtitle {"text": "Grande Alliance : Destruction", "color": "dark_green"}
playsound minecraft:ui.toast.challenge_complete master @s ~ ~ ~ 1 1
tellraw @s [{"text": "» ", "color": "gold"}, {"text": "Géants colossaux, enfants du dieu-titan Ymorath. Ils écrasent tout sur leur passage.", "color": "gray", "italic": true}]
tellraw @s [{"text": "» Dons : ", "color": "green"}, {"text": "Taille ×2, +10 cœurs, +4 dégâts, grande portée, enjambe les blocs", "color": "green"}]
tellraw @s [{"text": "» Faiblesses : ", "color": "red"}, {"text": "Faim II permanente, ne passe pas les portes", "color": "red"}]
tellraw @s [{"text": "» Utilise ta ", "color": "gold"}, {"text": "Pierre de Royaume", "color": "light_purple"}, {"text": " (clic droit) pour rejoindre les Royaumes Mortels.", "color": "gold"}]
tellraw @a [{"text": "⚔ ", "color": "gold"}, {"selector": "@s"}, {"text": " a rejoint : ", "color": "gray"}, {"text": "Fils d'Ymorath", "color": "dark_green"}]
