tag @s add rm_c
tag @s remove rm_spawn
team join rm_chaos @s
data modify entity @s CustomName set value {"text": "Démonette de Lyssara", "color": "light_purple"}
data modify entity @s IsBaby set value 0b
attribute @s minecraft:max_health base set 20
attribute @s minecraft:attack_damage base set 5
attribute @s minecraft:movement_speed base set 0.33
data modify entity @s Health set value 20.0f
loot replace entity @s armor.chest loot royaumes:equip/demonette/armor_chest
loot replace entity @s armor.head loot royaumes:equip/demonette/armor_head
loot replace entity @s weapon.mainhand loot royaumes:equip/demonette/weapon_mainhand
effect give @s minecraft:fire_resistance infinite 0 true
data modify entity @s DeathLootTable set value "royaumes:mobs/demonette"
