tag @s add rm_c
tag @s remove rm_spawn
team join rm_chaos @s
data modify entity @s CustomName set value {"text": "Guerrier du Chaos", "color": "dark_gray"}
data modify entity @s IsBaby set value 0b
attribute @s minecraft:max_health base set 40
attribute @s minecraft:attack_damage base set 7
attribute @s minecraft:scale base set 1.1
data modify entity @s Health set value 40.0f
loot replace entity @s armor.chest loot royaumes:equip/chaos_guerrier/armor_chest
loot replace entity @s armor.legs loot royaumes:equip/chaos_guerrier/armor_legs
loot replace entity @s armor.feet loot royaumes:equip/chaos_guerrier/armor_feet
loot replace entity @s armor.head loot royaumes:equip/chaos_guerrier/armor_head
loot replace entity @s weapon.mainhand loot royaumes:equip/chaos_guerrier/weapon_mainhand
loot replace entity @s weapon.offhand loot royaumes:equip/chaos_guerrier/weapon_offhand
effect give @s minecraft:fire_resistance infinite 0 true
data modify entity @s DeathLootTable set value "royaumes:mobs/chaos_guerrier"
