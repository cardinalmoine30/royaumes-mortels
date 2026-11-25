tag @s add rm_c
tag @s remove rm_spawn
team join rm_mort @s
data modify entity @s CustomName set value {"text": "Spectre Enchaîné Hantise Nocturne", "color": "dark_aqua"}
data modify entity @s IsBaby set value 0b
attribute @s minecraft:max_health base set 20
attribute @s minecraft:attack_damage base set 5
data modify entity @s Health set value 20.0f
loot replace entity @s armor.head loot royaumes:equip/chainrasp/armor_head
loot replace entity @s armor.chest loot royaumes:equip/chainrasp/armor_chest
loot replace entity @s weapon.mainhand loot royaumes:equip/chainrasp/weapon_mainhand
effect give @s minecraft:invisibility infinite 0 true
effect give @s minecraft:fire_resistance infinite 0 true
data modify entity @s DeathLootTable set value "royaumes:mobs/chainrasp"
