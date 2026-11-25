tag @s add rm_c
tag @s remove rm_spawn
team join rm_destruction @s
data modify entity @s CustomName set value {"text": "Tireur Cruelgars", "color": "dark_green"}
attribute @s minecraft:max_health base set 24
attribute @s minecraft:scale base set 1.1
data modify entity @s Health set value 24.0f
loot replace entity @s armor.chest loot royaumes:equip/kb_archer/armor_chest
loot replace entity @s armor.head loot royaumes:equip/kb_archer/armor_head
loot replace entity @s weapon.mainhand loot royaumes:equip/kb_archer/weapon_mainhand
effect give @s minecraft:fire_resistance infinite 0 true
data modify entity @s DeathLootTable set value "royaumes:mobs/kb_archer"
