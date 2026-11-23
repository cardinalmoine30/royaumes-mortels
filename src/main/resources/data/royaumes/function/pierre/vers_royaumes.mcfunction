execute in royaumes:royaumes_mortels run spreadplayers ~ ~ 0 48 false @s
# Si tout est océan autour, on élargit la recherche
execute at @s unless dimension royaumes:royaumes_mortels in royaumes:royaumes_mortels run spreadplayers ~ ~ 0 600 false @s
title @s title {"text": "Les Royaumes Mortels", "color": "gold", "bold": true}
effect give @s minecraft:resistance 5 4 true
effect give @s minecraft:slow_falling 5 0 true
execute at @s run playsound minecraft:block.portal.travel player @s ~ ~ ~ 0.4 1.5
