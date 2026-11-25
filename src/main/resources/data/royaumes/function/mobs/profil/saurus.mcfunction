tag @s add rm_c
tag @s remove rm_spawn
team join rm_ordre @s
data modify entity @s CustomName set value {"text": "Guerrier Écailleux", "color": "green"}
data modify entity @s IsBaby set value 0b
attribute @s minecraft:max_health base set 34
attribute @s minecraft:attack_damage base set 6
attribute @s minecraft:scale base set 1.25
attribute @s minecraft:armor base set 4
data modify entity @s Health set value 34.0f
loot replace entity @s armor.chest loot royaumes:equip/saurus/armor_chest
loot replace entity @s armor.head loot royaumes:equip/saurus/armor_head
loot replace entity @s weapon.mainhand loot royaumes:equip/saurus/weapon_mainhand
effect give @s minecraft:fire_resistance infinite 0 true
data modify entity @s DeathLootTable set value "royaumes:mobs/saurus"
