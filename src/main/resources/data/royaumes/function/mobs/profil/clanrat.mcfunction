tag @s add rm_c
tag @s remove rm_spawn
team join rm_chaos @s
data modify entity @s CustomName set value {"text": "Rat de Clan Hommes-Rats", "color": "green"}
data modify entity @s IsBaby set value 0b
attribute @s minecraft:max_health base set 16
attribute @s minecraft:attack_damage base set 4
attribute @s minecraft:scale base set 0.75
attribute @s minecraft:movement_speed base set 0.3
data modify entity @s Health set value 16.0f
loot replace entity @s armor.chest loot royaumes:equip/clanrat/armor_chest
loot replace entity @s armor.head loot royaumes:equip/clanrat/armor_head
loot replace entity @s weapon.mainhand loot royaumes:equip/clanrat/weapon_mainhand
effect give @s minecraft:fire_resistance infinite 0 true
data modify entity @s DeathLootTable set value "royaumes:mobs/clanrat"
