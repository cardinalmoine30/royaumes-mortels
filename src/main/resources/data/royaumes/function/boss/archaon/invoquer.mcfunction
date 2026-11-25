clear @s minecraft:carrot_on_a_stick[minecraft:custom_data~{royaumes:"sceau_archaon"}] 1
summon royaumes:archaon ^ ^1 ^7 {Tags:["rm_boss","rm_boss_archaon"],PersistenceRequired:1b}
bossbar add royaumes:archaon {"text": "Varkhan, l'Élu Éternel", "color": "dark_red"}
bossbar set royaumes:archaon max 1000
bossbar set royaumes:archaon color red
bossbar set royaumes:archaon visible true
particle minecraft:explosion_emitter ^ ^1 ^7 0 0 0 0 1
playsound minecraft:entity.lightning_bolt.thunder hostile @a[distance=..60] ~ ~ ~ 2 0.6
return 1
