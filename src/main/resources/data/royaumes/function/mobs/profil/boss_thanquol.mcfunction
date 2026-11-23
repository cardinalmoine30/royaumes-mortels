tag @s add rm_c
tag @s remove rm_spawn
team join rm_boss @s
data modify entity @s CustomName set value {"text": "Thanquol & Boneripper", "color": "green"}
attribute @s minecraft:max_health base set 750
attribute @s minecraft:attack_damage base set 16
attribute @s minecraft:scale base set 1.6
attribute @s minecraft:armor base set 12
attribute @s minecraft:knockback_resistance base set 1.0
attribute @s minecraft:movement_speed base set 0.32
attribute @s minecraft:follow_range base set 48
data modify entity @s Health set value 750.0f
effect give @s minecraft:fire_resistance infinite 0 true
data modify entity @s DeathLootTable set value "royaumes:boss/thanquol"
tag @s add rm_boss
tag @s add rm_boss_thanquol
data modify entity @s PersistenceRequired set value 1b
data modify entity @s CustomNameVisible set value 1b
tellraw @a[distance=..96] [{"text": "☠ ", "color": "green"}, {"text": "Thanquol & Boneripper", "color": "green", "bold": true}, {"text": " « Tuez-les ! Tuez-les tous, idiots-idiots ! »", "color": "gray", "italic": true}]
playsound minecraft:entity.wither.spawn hostile @a[distance=..96] ~ ~ ~ 2 0.6
summon minecraft:zombie ~ ~2 ~ {Tags:["rm_spawn","rm_p_thanquol_cavalier","rm_monture"],PersistenceRequired:1b}
ride @e[tag=rm_monture,limit=1,sort=nearest] mount @s
tag @e[tag=rm_monture] remove rm_monture
