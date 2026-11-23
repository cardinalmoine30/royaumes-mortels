tag @s add rm_c
tag @s remove rm_spawn
team join rm_chaos @s
data modify entity @s CustomName set value {"text": "Tireur de Jezzail Skaven", "color": "green"}
attribute @s minecraft:max_health base set 18
attribute @s minecraft:scale base set 0.8
data modify entity @s Health set value 18.0f
loot replace entity @s armor.chest loot royaumes:equip/jezzail/armor_chest
loot replace entity @s armor.head loot royaumes:equip/jezzail/armor_head
loot replace entity @s weapon.mainhand loot royaumes:equip/jezzail/weapon_mainhand
effect give @s minecraft:fire_resistance infinite 0 true
data modify entity @s DeathLootTable set value "royaumes:mobs/jezzail"
