tag @s add rm_c
tag @s remove rm_spawn
team join rm_destruction @s
data modify entity @s CustomName set value {"text": "Mégaboss Ironjawz", "color": "gold"}
data modify entity @s IsBaby set value 0b
attribute @s minecraft:max_health base set 100
attribute @s minecraft:attack_damage base set 12
attribute @s minecraft:scale base set 1.45
attribute @s minecraft:knockback_resistance base set 0.8
data modify entity @s Health set value 100.0f
loot replace entity @s armor.chest loot royaumes:equip/megaboss/armor_chest
loot replace entity @s armor.legs loot royaumes:equip/megaboss/armor_legs
loot replace entity @s armor.feet loot royaumes:equip/megaboss/armor_feet
loot replace entity @s armor.head loot royaumes:equip/megaboss/armor_head
loot replace entity @s weapon.mainhand loot royaumes:equip/megaboss/weapon_mainhand
effect give @s minecraft:fire_resistance infinite 0 true
data modify entity @s DeathLootTable set value "royaumes:mobs/megaboss"
