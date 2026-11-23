clear @s minecraft:carrot_on_a_stick[minecraft:custom_data~{royaumes:"sceau_gordrakk"}] 1
summon royaumes:gordrakk ^ ^1 ^7 {Tags:["rm_boss","rm_boss_gordrakk"],PersistenceRequired:1b}
bossbar add royaumes:gordrakk {"text": "Gordrakk, le Poing de Gork", "color": "gold"}
bossbar set royaumes:gordrakk max 800
bossbar set royaumes:gordrakk color yellow
bossbar set royaumes:gordrakk visible true
particle minecraft:explosion_emitter ^ ^1 ^7 0 0 0 0 1
playsound minecraft:entity.lightning_bolt.thunder hostile @a[distance=..60] ~ ~ ~ 2 0.6
return 1
