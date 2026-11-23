title @a[distance=..40] actionbar [{"text": "Gordrakk : ", "color": "gold"}, {"text": "WAAAGH !", "color": "white", "bold": true}]
summon minecraft:zombie ~2 ~ ~2 {Tags:["rm_spawn","rm_p_brute"]}
summon minecraft:zombie ~-2 ~ ~-2 {Tags:["rm_spawn","rm_p_brute"]}
summon minecraft:zombie ~2 ~ ~-2 {Tags:["rm_spawn","rm_p_brute"]}
effect give @e[team=rm_destruction,distance=..20] minecraft:strength 15 1
effect give @s minecraft:speed 8 1
playsound minecraft:entity.ravager.roar hostile @a[distance=..60] ~ ~ ~ 2 0.6
