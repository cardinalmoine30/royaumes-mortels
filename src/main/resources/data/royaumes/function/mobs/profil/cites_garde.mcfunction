tag @s add rm_c
tag @s remove rm_spawn
team join rm_ordre @s
data modify entity @s CustomName set value {"text": "Soldat de la Garde Franche", "color": "aqua"}
data modify entity @s IsBaby set value 0b
attribute @s minecraft:max_health base set 26
attribute @s minecraft:attack_damage base set 5
data modify entity @s Health set value 26.0f
loot replace entity @s armor.chest loot royaumes:equip/cites_garde/armor_chest
loot replace entity @s armor.head loot royaumes:equip/cites_garde/armor_head
loot replace entity @s weapon.mainhand loot royaumes:equip/cites_garde/weapon_mainhand
effect give @s minecraft:fire_resistance infinite 0 true
data modify entity @s DeathLootTable set value "royaumes:mobs/cites_garde"
