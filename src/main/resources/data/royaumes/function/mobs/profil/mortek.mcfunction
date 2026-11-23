tag @s add rm_c
tag @s remove rm_spawn
team join rm_mort @s
data modify entity @s CustomName set value {"text": "Garde Mortek Ossiarch", "color": "white"}
attribute @s minecraft:max_health base set 36
attribute @s minecraft:scale base set 1.15
attribute @s minecraft:armor base set 6
data modify entity @s Health set value 36.0f
loot replace entity @s armor.chest loot royaumes:equip/mortek/armor_chest
loot replace entity @s armor.legs loot royaumes:equip/mortek/armor_legs
loot replace entity @s armor.feet loot royaumes:equip/mortek/armor_feet
loot replace entity @s armor.head loot royaumes:equip/mortek/armor_head
loot replace entity @s weapon.mainhand loot royaumes:equip/mortek/weapon_mainhand
loot replace entity @s weapon.offhand loot royaumes:equip/mortek/weapon_offhand
effect give @s minecraft:fire_resistance infinite 0 true
data modify entity @s DeathLootTable set value "royaumes:mobs/mortek"
