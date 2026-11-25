clear @s minecraft:carrot_on_a_stick[minecraft:custom_data~{royaumes:"sceau_skarbrand"}] 1
summon royaumes:skarbrand ^ ^1 ^7 {Tags:["rm_boss","rm_boss_skarbrand"],PersistenceRequired:1b}
bossbar add royaumes:skarbrand {"text": "Brakhar, l'Exilé", "color": "red"}
bossbar set royaumes:skarbrand max 850
bossbar set royaumes:skarbrand color red
bossbar set royaumes:skarbrand visible true
particle minecraft:explosion_emitter ^ ^1 ^7 0 0 0 0 1
playsound minecraft:entity.lightning_bolt.thunder hostile @a[distance=..60] ~ ~ ~ 2 0.6
return 1
