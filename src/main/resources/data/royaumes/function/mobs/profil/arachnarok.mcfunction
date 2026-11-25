tag @s add rm_c
tag @s remove rm_spawn
team join rm_destruction @s
data modify entity @s CustomName set value {"text": "Araignée Araignée Titanesque", "color": "yellow"}
attribute @s minecraft:max_health base set 70
attribute @s minecraft:attack_damage base set 8
attribute @s minecraft:scale base set 2.2
data modify entity @s Health set value 70.0f
effect give @s minecraft:fire_resistance infinite 0 true
data modify entity @s DeathLootTable set value "royaumes:mobs/arachnarok"
