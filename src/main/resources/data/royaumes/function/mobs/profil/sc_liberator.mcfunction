tag @s add rm_c
tag @s remove rm_spawn
team join rm_ordre @s
data modify entity @s CustomName set value {"text": "Libérateur Foudroyés", "color": "gold"}
data modify entity @s IsBaby set value 0b
attribute @s minecraft:max_health base set 40
attribute @s minecraft:attack_damage base set 6
attribute @s minecraft:scale base set 1.15
data modify entity @s Health set value 40.0f
loot replace entity @s armor.chest loot royaumes:equip/sc_liberator/armor_chest
loot replace entity @s armor.legs loot royaumes:equip/sc_liberator/armor_legs
loot replace entity @s armor.feet loot royaumes:equip/sc_liberator/armor_feet
loot replace entity @s armor.head loot royaumes:equip/sc_liberator/armor_head
loot replace entity @s weapon.mainhand loot royaumes:equip/sc_liberator/weapon_mainhand
loot replace entity @s weapon.offhand loot royaumes:equip/sc_liberator/weapon_offhand
effect give @s minecraft:fire_resistance infinite 0 true
data modify entity @s DeathLootTable set value "royaumes:mobs/sc_liberator"
