tag @s add rm_c
tag @s remove rm_spawn
team join rm_destruction @s
data modify entity @s CustomName set value {"text": "Chasseur Ogre", "color": "gold"}
attribute @s minecraft:max_health base set 40
attribute @s minecraft:scale base set 1.4
data modify entity @s Health set value 40.0f
loot replace entity @s armor.chest loot royaumes:equip/ogor_chasseur/armor_chest
loot replace entity @s armor.head loot royaumes:equip/ogor_chasseur/armor_head
loot replace entity @s weapon.mainhand loot royaumes:equip/ogor_chasseur/weapon_mainhand
effect give @s minecraft:fire_resistance infinite 0 true
data modify entity @s DeathLootTable set value "royaumes:mobs/ogor_chasseur"
