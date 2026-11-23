scoreboard players set @s rm_faction 24
team join rm_destruction @s
function royaumes:factions/dons/ogors
loot give @s loot royaumes:kits/ogors
dialog clear @s
title @s title {"text": "Ogor Mawtribes", "color": "gold", "bold": true}
title @s subtitle {"text": "Grande Alliance : Destruction", "color": "dark_green"}
playsound minecraft:ui.toast.challenge_complete master @s ~ ~ ~ 1 1
tellraw @s [{"text": "» ", "color": "gold"}, {"text": "Ogors gloutons et géants, pour qui tout ce qui bouge est un repas.", "color": "gray", "italic": true}]
tellraw @s [{"text": "» Dons : ", "color": "green"}, {"text": "Taille +40 %, +5 cœurs, +2 dégâts", "color": "green"}]
tellraw @s [{"text": "» Faiblesses : ", "color": "red"}, {"text": "Faim permanente, vitesse -10 %", "color": "red"}]
tellraw @s [{"text": "» Utilise ta ", "color": "gold"}, {"text": "Pierre de Royaume", "color": "light_purple"}, {"text": " (clic droit) pour rejoindre les Royaumes Mortels.", "color": "gold"}]
tellraw @a [{"text": "⚔ ", "color": "gold"}, {"selector": "@s"}, {"text": " a rejoint : ", "color": "gray"}, {"text": "Ogor Mawtribes", "color": "gold"}]
