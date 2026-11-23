tag @s add rm_c
tag @s remove rm_spawn
team join rm_mort @s
data modify entity @s CustomName set value {"text": "Seigneur Vampire", "color": "dark_red"}
data modify entity @s IsBaby set value 0b
attribute @s minecraft:max_health base set 70
attribute @s minecraft:attack_damage base set 9
attribute @s minecraft:movement_speed base set 0.3
data modify entity @s Health set value 70.0f
loot replace entity @s armor.chest loot royaumes:equip/vampire/armor_chest
loot replace entity @s armor.legs loot royaumes:equip/vampire/armor_legs
loot replace entity @s armor.feet loot royaumes:equip/vampire/armor_feet
loot replace entity @s weapon.mainhand loot royaumes:equip/vampire/weapon_mainhand
effect give @s minecraft:fire_resistance infinite 0 true
data modify entity @s DeathLootTable set value "royaumes:mobs/vampire"
