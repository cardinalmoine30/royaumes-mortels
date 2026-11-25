tag @s add rm_c
tag @s remove rm_spawn
team join rm_mort @s
data modify entity @s CustomName set value {"text": "Squelette Cliquetant", "color": "dark_purple"}
attribute @s minecraft:max_health base set 22
data modify entity @s Health set value 22.0f
loot replace entity @s armor.head loot royaumes:equip/deathrattle/armor_head
loot replace entity @s weapon.mainhand loot royaumes:equip/deathrattle/weapon_mainhand
loot replace entity @s weapon.offhand loot royaumes:equip/deathrattle/weapon_offhand
effect give @s minecraft:fire_resistance infinite 0 true
data modify entity @s DeathLootTable set value "royaumes:mobs/deathrattle"
