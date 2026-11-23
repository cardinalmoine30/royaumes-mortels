tag @s add rm_c
tag @s remove rm_spawn
team join rm_boss @s
data modify entity @s CustomName set value {"text": "Grand Prophète Thanquol", "color": "green"}
data modify entity @s IsBaby set value 0b
attribute @s minecraft:max_health base set 120
attribute @s minecraft:attack_damage base set 8
attribute @s minecraft:scale base set 0.9
data modify entity @s Health set value 120.0f
loot replace entity @s armor.chest loot royaumes:equip/thanquol_cavalier/armor_chest
loot replace entity @s armor.head loot royaumes:equip/thanquol_cavalier/armor_head
loot replace entity @s weapon.mainhand loot royaumes:equip/thanquol_cavalier/weapon_mainhand
effect give @s minecraft:fire_resistance infinite 0 true
data modify entity @s DeathLootTable set value "royaumes:mobs/clanrat"
data modify entity @s PersistenceRequired set value 1b
