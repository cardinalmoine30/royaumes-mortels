tag @s add rm_c
tag @s remove rm_spawn
team join rm_destruction @s
data modify entity @s CustomName set value {"text": "Géant Mangeur d'Hommes", "color": "dark_green"}
data modify entity @s IsBaby set value 0b
attribute @s minecraft:max_health base set 160
attribute @s minecraft:attack_damage base set 14
attribute @s minecraft:scale base set 3.5
attribute @s minecraft:movement_speed base set 0.2
attribute @s minecraft:knockback_resistance base set 1.0
data modify entity @s Health set value 160.0f
loot replace entity @s weapon.mainhand loot royaumes:equip/gargant/weapon_mainhand
effect give @s minecraft:fire_resistance infinite 0 true
data modify entity @s DeathLootTable set value "royaumes:mobs/gargant"
