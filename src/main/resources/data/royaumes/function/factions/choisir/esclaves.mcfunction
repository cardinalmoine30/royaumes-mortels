scoreboard players set @s rm_faction 10
team join rm_chaos @s
function royaumes:factions/dons/esclaves
loot give @s loot royaumes:kits/esclaves
dialog clear @s
title @s title {"text": "Légions des Ténèbres", "color": "dark_gray", "bold": true}
title @s subtitle {"text": "Grande Alliance : Chaos", "color": "dark_red"}
playsound minecraft:ui.toast.challenge_complete master @s ~ ~ ~ 1 1
tellraw @s [{"text": "» ", "color": "gold"}, {"text": "Guerriers du Chaos Absolu, cuirassés de fer noir, qui cherchent la faveur des Dieux Sombres.", "color": "gray", "italic": true}]
tellraw @s [{"text": "» Dons : ", "color": "green"}, {"text": "Taille +10 %, +2 cœurs, +2 armure, +1 dégât", "color": "green"}]
tellraw @s [{"text": "» Faiblesses : ", "color": "red"}, {"text": "Chance -1 (marqués par le Chaos)", "color": "red"}]
tellraw @s [{"text": "» Utilise ta ", "color": "gold"}, {"text": "Pierre de Royaume", "color": "light_purple"}, {"text": " (clic droit) pour rejoindre les Royaumes Mortels.", "color": "gold"}]
tellraw @a [{"text": "⚔ ", "color": "gold"}, {"selector": "@s"}, {"text": " a rejoint : ", "color": "gray"}, {"text": "Légions des Ténèbres", "color": "dark_gray"}]
