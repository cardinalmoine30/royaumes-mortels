scoreboard players set @s rm_faction 19
team join rm_mort @s
function royaumes:factions/dons/ossiarch
loot give @s loot royaumes:kits/ossiarch
dialog clear @s
title @s title {"text": "Faucheurs d'Os", "color": "white", "bold": true}
title @s subtitle {"text": "Grande Alliance : Mort", "color": "dark_purple"}
playsound minecraft:ui.toast.challenge_complete master @s ~ ~ ~ 1 1
tellraw @s [{"text": "» ", "color": "gold"}, {"text": "Légions d'os façonnées par Necrath, la plus disciplinée des armées.", "color": "gray", "italic": true}]
tellraw @s [{"text": "» Dons : ", "color": "green"}, {"text": "+6 armure, recul -40 %, +1 cœur", "color": "green"}]
tellraw @s [{"text": "» Faiblesses : ", "color": "red"}, {"text": "Vitesse -10 %", "color": "red"}]
tellraw @s [{"text": "» Utilise ta ", "color": "gold"}, {"text": "Pierre de Royaume", "color": "light_purple"}, {"text": " (clic droit) pour rejoindre les Royaumes Mortels.", "color": "gold"}]
tellraw @a [{"text": "⚔ ", "color": "gold"}, {"selector": "@s"}, {"text": " a rejoint : ", "color": "gray"}, {"text": "Faucheurs d'Os", "color": "white"}]
