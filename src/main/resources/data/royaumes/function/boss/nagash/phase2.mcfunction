tag @s add rm_phase2
effect give @s minecraft:speed infinite 0 true
effect give @s minecraft:resistance infinite 0 true
title @a[distance=..48] title {"text": "Nagash", "color": "dark_purple", "bold": true}
title @a[distance=..48] subtitle {"text": "entre dans une rage terrible !", "color": "red"}
playsound minecraft:entity.wither.spawn hostile @a[distance=..60] ~ ~ ~ 2 0.8
summon royaumes:deathrattle ~2 ~ ~2
summon royaumes:deathrattle ~-2 ~ ~-2
summon royaumes:chainrasp ~2 ~ ~-2
