tag @s add rm_phase2
effect give @s minecraft:speed infinite 0 true
effect give @s minecraft:resistance infinite 0 true
title @a[distance=..48] title {"text": "Gordrakk", "color": "gold", "bold": true}
title @a[distance=..48] subtitle {"text": "entre dans une rage terrible !", "color": "red"}
playsound minecraft:entity.wither.spawn hostile @a[distance=..60] ~ ~ ~ 2 0.8
summon minecraft:zombie ~2 ~ ~2 {Tags:["rm_spawn","rm_p_brute"]}
summon minecraft:zombie ~-2 ~ ~-2 {Tags:["rm_spawn","rm_p_brute"]}
summon minecraft:zombie ~2 ~ ~-2 {Tags:["rm_spawn","rm_p_brute"]}
