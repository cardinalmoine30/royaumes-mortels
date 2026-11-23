title @a[distance=..40] actionbar [{"text": "Thanquol & Boneripper : ", "color": "green"}, {"text": "Esclaves-Rats !", "color": "white", "bold": true}]
summon minecraft:zombie ~2 ~ ~2 {Tags:["rm_spawn","rm_p_clanrat"]}
summon minecraft:zombie ~-2 ~ ~-2 {Tags:["rm_spawn","rm_p_clanrat"]}
summon minecraft:skeleton ~2 ~ ~-2 {Tags:["rm_spawn","rm_p_jezzail"]}
playsound minecraft:block.bell.use hostile @a[distance=..60] ~ ~ ~ 2 0.5
