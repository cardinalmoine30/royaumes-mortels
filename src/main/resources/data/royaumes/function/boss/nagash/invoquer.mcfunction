clear @s minecraft:carrot_on_a_stick[minecraft:custom_data~{royaumes:"sceau_nagash"}] 1
summon royaumes:nagash ^ ^1 ^7 {Tags:["rm_boss","rm_boss_nagash"],PersistenceRequired:1b}
bossbar add royaumes:nagash {"text": "Necrath, Dieu de la Mort", "color": "dark_purple"}
bossbar set royaumes:nagash max 900
bossbar set royaumes:nagash color purple
bossbar set royaumes:nagash visible true
particle minecraft:explosion_emitter ^ ^1 ^7 0 0 0 0 1
playsound minecraft:entity.lightning_bolt.thunder hostile @a[distance=..60] ~ ~ ~ 2 0.6
return 1
