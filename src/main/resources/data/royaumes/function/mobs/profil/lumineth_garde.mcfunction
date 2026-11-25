tag @s add rm_c
tag @s remove rm_spawn
team join rm_ordre @s
data modify entity @s CustomName set value {"text": "Garde du Temple de Lumière", "color": "white"}
data modify entity @s IsBaby set value 0b
attribute @s minecraft:max_health base set 28
attribute @s minecraft:attack_damage base set 5
data modify entity @s Health set value 28.0f
loot replace entity @s armor.chest loot royaumes:equip/lumineth_garde/armor_chest
loot replace entity @s armor.head loot royaumes:equip/lumineth_garde/armor_head
loot replace entity @s armor.legs loot royaumes:equip/lumineth_garde/armor_legs
loot replace entity @s armor.feet loot royaumes:equip/lumineth_garde/armor_feet
loot replace entity @s weapon.mainhand loot royaumes:equip/lumineth_garde/weapon_mainhand
effect give @s minecraft:fire_resistance infinite 0 true
data modify entity @s DeathLootTable set value "royaumes:mobs/lumineth_garde"
