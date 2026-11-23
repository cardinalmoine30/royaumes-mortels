tag @s add rm_c
tag @s remove rm_spawn
team join rm_ordre @s
data modify entity @s CustomName set value {"text": "Dryade Sylvaneth", "color": "dark_green"}
data modify entity @s IsBaby set value 0b
attribute @s minecraft:max_health base set 30
attribute @s minecraft:attack_damage base set 5
data modify entity @s Health set value 30.0f
loot replace entity @s armor.chest loot royaumes:equip/dryade/armor_chest
loot replace entity @s armor.head loot royaumes:equip/dryade/armor_head
loot replace entity @s armor.legs loot royaumes:equip/dryade/armor_legs
loot replace entity @s armor.feet loot royaumes:equip/dryade/armor_feet
loot replace entity @s weapon.mainhand loot royaumes:equip/dryade/weapon_mainhand
effect give @s minecraft:regeneration infinite 0 true
effect give @s minecraft:fire_resistance infinite 0 true
data modify entity @s DeathLootTable set value "royaumes:mobs/dryade"
