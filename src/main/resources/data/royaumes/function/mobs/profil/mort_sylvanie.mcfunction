tag @s add rm_c
tag @s remove rm_spawn
team join rm_mort @s
data modify entity @s CustomName set value {"text": "Mort de Sanguinie", "color": "dark_purple"}
data modify entity @s IsBaby set value 0b
attribute @s minecraft:max_health base set 24
data modify entity @s Health set value 24.0f
effect give @s minecraft:fire_resistance infinite 0 true
data modify entity @s DeathLootTable set value "royaumes:mobs/mort_sylvanie"
