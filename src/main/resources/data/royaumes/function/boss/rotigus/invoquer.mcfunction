clear @s minecraft:carrot_on_a_stick[minecraft:custom_data~{royaumes:"sceau_rotigus"}] 1
summon royaumes:rotigus ^ ^1 ^7 {Tags:["rm_boss","rm_boss_rotigus"],PersistenceRequired:1b}
bossbar add royaumes:rotigus {"text": "Rotigus, le Pluvieux", "color": "dark_green"}
bossbar set royaumes:rotigus max 950
bossbar set royaumes:rotigus color green
bossbar set royaumes:rotigus visible true
particle minecraft:explosion_emitter ^ ^1 ^7 0 0 0 0 1
playsound minecraft:entity.lightning_bolt.thunder hostile @a[distance=..60] ~ ~ ~ 2 0.6
return 1
