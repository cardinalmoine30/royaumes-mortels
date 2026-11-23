scoreboard players set @s rm_faction 18
team join rm_mort @s
function royaumes:factions/dons/soulblight
loot give @s loot royaumes:kits/soulblight
dialog clear @s
title @s title {"text": "Seigneurs Sanguinaires", "color": "dark_red", "bold": true}
title @s subtitle {"text": "Grande Alliance : Mort", "color": "dark_purple"}
playsound minecraft:ui.toast.challenge_complete master @s ~ ~ ~ 1 1
tellraw @s [{"text": "» ", "color": "gold"}, {"text": "Vampires de la lignée de Soulblight et leurs armées de morts relevés.", "color": "gray", "italic": true}]
tellraw @s [{"text": "» Dons : ", "color": "green"}, {"text": "+2 cœurs, +1 dégât, vision nocturne", "color": "green"}]
tellraw @s [{"text": "» Faiblesses : ", "color": "red"}, {"text": "Faiblesse en plein soleil", "color": "red"}]
tellraw @s [{"text": "» Utilise ta ", "color": "gold"}, {"text": "Pierre de Royaume", "color": "light_purple"}, {"text": " (clic droit) pour rejoindre les Royaumes Mortels.", "color": "gold"}]
tellraw @a [{"text": "⚔ ", "color": "gold"}, {"selector": "@s"}, {"text": " a rejoint : ", "color": "gray"}, {"text": "Seigneurs Sanguinaires", "color": "dark_red"}]
