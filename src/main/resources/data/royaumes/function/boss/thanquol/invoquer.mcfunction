clear @s minecraft:carrot_on_a_stick[minecraft:custom_data~{royaumes:"sceau_thanquol"}] 1
summon minecraft:ravager ^ ^1 ^7 {Tags:["rm_spawn","rm_p_boss_thanquol"],PersistenceRequired:1b}
particle minecraft:explosion_emitter ^ ^1 ^7 0 0 0 0 1
playsound minecraft:entity.lightning_bolt.thunder hostile @a[distance=..60] ~ ~ ~ 2 0.6
return 1
