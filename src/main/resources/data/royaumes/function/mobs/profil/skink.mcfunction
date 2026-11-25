tag @s add rm_c
tag @s remove rm_spawn
team join rm_ordre @s
data modify entity @s CustomName set value {"text": "Scinque", "color": "green"}
attribute @s minecraft:max_health base set 16
attribute @s minecraft:scale base set 0.75
attribute @s minecraft:movement_speed base set 0.3
data modify entity @s Health set value 16.0f
loot replace entity @s armor.chest loot royaumes:equip/skink/armor_chest
loot replace entity @s armor.head loot royaumes:equip/skink/armor_head
loot replace entity @s weapon.mainhand loot royaumes:equip/skink/weapon_mainhand
effect give @s minecraft:fire_resistance infinite 0 true
data modify entity @s DeathLootTable set value "royaumes:mobs/skink"
