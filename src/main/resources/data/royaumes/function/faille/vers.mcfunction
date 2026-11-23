$execute in $(dim) run spreadplayers ~ ~ 0 64 false @s
$execute at @s unless dimension $(dim) in $(dim) run spreadplayers ~ ~ 0 800 false @s
$title @s title {"text":"$(nom)","color":"$(c)","bold":true}
title @s subtitle {"text": "Le portail vous a mené en terre inconnue…", "color": "gray", "italic": true}
effect give @s minecraft:resistance 6 4 true
effect give @s minecraft:slow_falling 6 0 true
$execute at @s if dimension $(dim) run function royaumes:faille/retour
