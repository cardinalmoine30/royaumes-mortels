tag @s add rm_c
tag @s remove rm_spawn
team join rm_chaos @s
data modify entity @s CustomName set value {"text": "Porte-Peste de Nurgle", "color": "dark_green"}
data modify entity @s IsBaby set value 0b
attribute @s minecraft:max_health base set 40
attribute @s minecraft:attack_damage base set 5
attribute @s minecraft:movement_speed base set 0.18
data modify entity @s Health set value 40.0f
loot replace entity @s armor.chest loot royaumes:equip/pestigor/armor_chest
loot replace entity @s armor.head loot royaumes:equip/pestigor/armor_head
loot replace entity @s armor.legs loot royaumes:equip/pestigor/armor_legs
loot replace entity @s armor.feet loot royaumes:equip/pestigor/armor_feet
loot replace entity @s weapon.mainhand loot royaumes:equip/pestigor/weapon_mainhand
effect give @s minecraft:regeneration infinite 0 true
effect give @s minecraft:fire_resistance infinite 0 true
data modify entity @s DeathLootTable set value "royaumes:mobs/pestigor"
