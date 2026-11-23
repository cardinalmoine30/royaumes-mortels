tag @s add rm_c
tag @s remove rm_spawn
team join rm_destruction @s
data modify entity @s CustomName set value {"text": "Grot de la Mauvaise Lune", "color": "yellow"}
data modify entity @s IsBaby set value 1b
attribute @s minecraft:max_health base set 10
attribute @s minecraft:attack_damage base set 3
data modify entity @s Health set value 10.0f
loot replace entity @s armor.head loot royaumes:equip/grot/armor_head
loot replace entity @s weapon.mainhand loot royaumes:equip/grot/weapon_mainhand
effect give @s minecraft:fire_resistance infinite 0 true
data modify entity @s DeathLootTable set value "royaumes:mobs/grot"
