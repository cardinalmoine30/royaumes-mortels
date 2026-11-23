tag @s add rm_c
tag @s remove rm_spawn
team join rm_ordre @s
data modify entity @s CustomName set value {"text": "Archer Vanari", "color": "white"}
attribute @s minecraft:max_health base set 24
data modify entity @s Health set value 24.0f
loot replace entity @s armor.chest loot royaumes:equip/lumineth/armor_chest
loot replace entity @s armor.head loot royaumes:equip/lumineth/armor_head
loot replace entity @s weapon.mainhand loot royaumes:equip/lumineth/weapon_mainhand
effect give @s minecraft:fire_resistance infinite 0 true
data modify entity @s DeathLootTable set value "royaumes:mobs/lumineth"
