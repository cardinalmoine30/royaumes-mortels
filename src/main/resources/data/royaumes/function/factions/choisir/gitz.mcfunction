scoreboard players set @s rm_faction 23
team join rm_destruction @s
function royaumes:factions/dons/gitz
loot give @s loot royaumes:kits/gitz
dialog clear @s
title @s title {"text": "Gloomspite Gitz", "color": "yellow", "bold": true}
title @s subtitle {"text": "Grande Alliance : Destruction", "color": "dark_green"}
playsound minecraft:ui.toast.challenge_complete master @s ~ ~ ~ 1 1
tellraw @s [{"text": "» ", "color": "gold"}, {"text": "Grots fous de la Mauvaise Lune, chevaucheurs d'araignées et cultivateurs de champignons.", "color": "gray", "italic": true}]
tellraw @s [{"text": "» Dons : ", "color": "green"}, {"text": "Vitesse +10 %, vision nocturne, saut amélioré", "color": "green"}]
tellraw @s [{"text": "» Faiblesses : ", "color": "red"}, {"text": "Taille -30 %, -3 cœurs", "color": "red"}]
tellraw @s [{"text": "» Utilise ta ", "color": "gold"}, {"text": "Pierre de Royaume", "color": "light_purple"}, {"text": " (clic droit) pour rejoindre les Royaumes Mortels.", "color": "gold"}]
tellraw @a [{"text": "⚔ ", "color": "gold"}, {"selector": "@s"}, {"text": " a rejoint : ", "color": "gray"}, {"text": "Gloomspite Gitz", "color": "yellow"}]
