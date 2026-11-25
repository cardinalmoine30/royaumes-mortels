tag @s add rm_c
tag @s remove rm_spawn
team join rm_destruction @s
data modify entity @s CustomName set value {"text": "Étripeur Cruelgars", "color": "dark_green"}
data modify entity @s IsBaby set value 0b
attribute @s minecraft:max_health base set 28
attribute @s minecraft:attack_damage base set 5
attribute @s minecraft:scale base set 1.1
data modify entity @s Health set value 28.0f
loot replace entity @s armor.chest loot royaumes:equip/gutrippa/armor_chest
loot replace entity @s armor.head loot royaumes:equip/gutrippa/armor_head
loot replace entity @s weapon.mainhand loot royaumes:equip/gutrippa/weapon_mainhand
effect give @s minecraft:fire_resistance infinite 0 true
data modify entity @s DeathLootTable set value "royaumes:mobs/gutrippa"
