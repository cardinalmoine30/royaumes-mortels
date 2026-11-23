tag @s add rm_c
tag @s remove rm_spawn
team join rm_mort @s
data modify entity @s CustomName set value {"text": "Goule des Cryptes", "color": "dark_purple"}
data modify entity @s IsBaby set value 0b
attribute @s minecraft:max_health base set 22
attribute @s minecraft:attack_damage base set 5
attribute @s minecraft:movement_speed base set 0.32
data modify entity @s Health set value 22.0f
loot replace entity @s armor.chest loot royaumes:equip/goule/armor_chest
effect give @s minecraft:fire_resistance infinite 0 true
data modify entity @s DeathLootTable set value "royaumes:mobs/goule"
