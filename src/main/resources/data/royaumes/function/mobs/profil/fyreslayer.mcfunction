tag @s add rm_c
tag @s remove rm_spawn
team join rm_ordre @s
data modify entity @s CustomName set value {"text": "Vulkite Berzerker", "color": "gold"}
data modify entity @s IsBaby set value 0b
attribute @s minecraft:max_health base set 30
attribute @s minecraft:attack_damage base set 6
attribute @s minecraft:scale base set 0.85
data modify entity @s Health set value 30.0f
loot replace entity @s armor.head loot royaumes:equip/fyreslayer/armor_head
loot replace entity @s weapon.mainhand loot royaumes:equip/fyreslayer/weapon_mainhand
effect give @s minecraft:fire_resistance infinite 0 true
data modify entity @s DeathLootTable set value "royaumes:mobs/fyreslayer"
