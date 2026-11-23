execute in minecraft:overworld run spreadplayers ~ ~ 0 48 false @s
execute at @s unless dimension minecraft:overworld unless dimension minecraft:the_nether unless dimension minecraft:the_end in minecraft:overworld run spreadplayers ~ ~ 0 600 false @s
title @s title {"text": "Le Monde-Pont", "color": "aqua", "bold": true}
effect give @s minecraft:resistance 5 4 true
effect give @s minecraft:slow_falling 5 0 true
execute at @s run playsound minecraft:block.portal.travel player @s ~ ~ ~ 0.4 1.5
