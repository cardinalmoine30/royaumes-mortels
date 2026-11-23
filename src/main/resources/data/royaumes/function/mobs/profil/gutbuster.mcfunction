tag @s add rm_c
tag @s remove rm_spawn
team join rm_destruction @s
data modify entity @s CustomName set value {"text": "Ogor Gutbuster", "color": "gold"}
data modify entity @s IsBaby set value 0b
attribute @s minecraft:max_health base set 60
attribute @s minecraft:attack_damage base set 9
attribute @s minecraft:scale base set 1.6
attribute @s minecraft:movement_speed base set 0.2
data modify entity @s Health set value 60.0f
loot replace entity @s armor.chest loot royaumes:equip/gutbuster/armor_chest
loot replace entity @s weapon.mainhand loot royaumes:equip/gutbuster/weapon_mainhand
effect give @s minecraft:fire_resistance infinite 0 true
data modify entity @s DeathLootTable set value "royaumes:mobs/gutbuster"
