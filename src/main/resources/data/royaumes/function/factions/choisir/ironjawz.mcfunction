scoreboard players set @s rm_faction 21
team join rm_destruction @s
function royaumes:factions/dons/ironjawz
loot give @s loot royaumes:kits/ironjawz
dialog clear @s
title @s title {"text": "Ironjawz", "color": "gold", "bold": true}
title @s subtitle {"text": "Grande Alliance : Destruction", "color": "dark_green"}
playsound minecraft:ui.toast.challenge_complete master @s ~ ~ ~ 1 1
tellraw @s [{"text": "» ", "color": "gold"}, {"text": "Les plus grands et les plus brutaux des orruks, couverts de ferraille. WAAAGH !", "color": "gray", "italic": true}]
tellraw @s [{"text": "» Dons : ", "color": "green"}, {"text": "Taille +15 %, +2 cœurs, +2 dégâts, recul -30 %", "color": "green"}]
tellraw @s [{"text": "» Faiblesses : ", "color": "red"}, {"text": "Vitesse -5 %", "color": "red"}]
tellraw @s [{"text": "» Utilise ta ", "color": "gold"}, {"text": "Pierre de Royaume", "color": "light_purple"}, {"text": " (clic droit) pour rejoindre les Royaumes Mortels.", "color": "gold"}]
tellraw @a [{"text": "⚔ ", "color": "gold"}, {"selector": "@s"}, {"text": " a rejoint : ", "color": "gray"}, {"text": "Ironjawz", "color": "gold"}]
