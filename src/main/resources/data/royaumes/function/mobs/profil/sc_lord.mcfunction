tag @s add rm_c
tag @s remove rm_spawn
team join rm_ordre @s
data modify entity @s CustomName set value {"text": "Lord-Celestant", "color": "gold"}
data modify entity @s IsBaby set value 0b
attribute @s minecraft:max_health base set 80
attribute @s minecraft:attack_damage base set 10
attribute @s minecraft:scale base set 1.25
attribute @s minecraft:knockback_resistance base set 0.6
data modify entity @s Health set value 80.0f
loot replace entity @s armor.chest loot royaumes:equip/sc_lord/armor_chest
loot replace entity @s armor.legs loot royaumes:equip/sc_lord/armor_legs
loot replace entity @s armor.feet loot royaumes:equip/sc_lord/armor_feet
loot replace entity @s armor.head loot royaumes:equip/sc_lord/armor_head
loot replace entity @s weapon.mainhand loot royaumes:equip/sc_lord/weapon_mainhand
effect give @s minecraft:fire_resistance infinite 0 true
data modify entity @s DeathLootTable set value "royaumes:mobs/sc_lord"
