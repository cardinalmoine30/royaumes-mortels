title @a[distance=..40] actionbar [{"text": "Nagash : ", "color": "dark_purple"}, {"text": "Invocation des Morts", "color": "white", "bold": true}]
summon minecraft:skeleton ~2 ~ ~2 {Tags:["rm_spawn","rm_p_deathrattle"]}
summon minecraft:skeleton ~-2 ~ ~-2 {Tags:["rm_spawn","rm_p_deathrattle"]}
summon minecraft:zombie ~2 ~ ~-2 {Tags:["rm_spawn","rm_p_chainrasp"]}
particle minecraft:soul ~ ~1 ~ 3 1 3 0.05 120
playsound minecraft:entity.evoker.prepare_summon hostile @a[distance=..40] ~ ~ ~ 2 0.6
