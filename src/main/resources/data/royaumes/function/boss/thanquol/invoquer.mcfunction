clear @s minecraft:carrot_on_a_stick[minecraft:custom_data~{royaumes:"sceau_thanquol"}] 1
summon royaumes:thanquol ^ ^1 ^7 {Tags:["rm_boss","rm_boss_thanquol"],PersistenceRequired:1b}
bossbar add royaumes:thanquol {"text": "Thanquol & Boneripper", "color": "green"}
bossbar set royaumes:thanquol max 750
bossbar set royaumes:thanquol color green
bossbar set royaumes:thanquol visible true
particle minecraft:explosion_emitter ^ ^1 ^7 0 0 0 0 1
playsound minecraft:entity.lightning_bolt.thunder hostile @a[distance=..60] ~ ~ ~ 2 0.6
return 1
