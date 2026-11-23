tag @s add rm_c
tag @s remove rm_spawn
team join rm_chaos @s
data modify entity @s CustomName set value {"text": "Seigneur du Chaos", "color": "dark_red"}
data modify entity @s IsBaby set value 0b
attribute @s minecraft:max_health base set 90
attribute @s minecraft:attack_damage base set 11
attribute @s minecraft:scale base set 1.3
attribute @s minecraft:knockback_resistance base set 0.6
data modify entity @s Health set value 90.0f
loot replace entity @s armor.chest loot royaumes:equip/chaos_seigneur/armor_chest
loot replace entity @s armor.legs loot royaumes:equip/chaos_seigneur/armor_legs
loot replace entity @s armor.feet loot royaumes:equip/chaos_seigneur/armor_feet
loot replace entity @s armor.head loot royaumes:equip/chaos_seigneur/armor_head
loot replace entity @s weapon.mainhand loot royaumes:equip/chaos_seigneur/weapon_mainhand
effect give @s minecraft:fire_resistance infinite 0 true
data modify entity @s DeathLootTable set value "royaumes:mobs/chaos_seigneur"
