tag @s add rm_c
tag @s remove rm_spawn
team join rm_chaos @s
data modify entity @s CustomName set value {"text": "Garde Infernale de Hashut", "color": "gold"}
data modify entity @s IsBaby set value 0b
attribute @s minecraft:max_health base set 32
attribute @s minecraft:attack_damage base set 6
attribute @s minecraft:scale base set 0.85
data modify entity @s Health set value 32.0f
loot replace entity @s armor.chest loot royaumes:equip/hashut/armor_chest
loot replace entity @s armor.legs loot royaumes:equip/hashut/armor_legs
loot replace entity @s armor.feet loot royaumes:equip/hashut/armor_feet
loot replace entity @s armor.head loot royaumes:equip/hashut/armor_head
loot replace entity @s weapon.mainhand loot royaumes:equip/hashut/weapon_mainhand
effect give @s minecraft:fire_resistance infinite 0 true
data modify entity @s DeathLootTable set value "royaumes:mobs/hashut"
