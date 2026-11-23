tag @s add rm_c
tag @s remove rm_spawn
team join rm_ordre @s
data modify entity @s CustomName set value {"text": "Tireur de la Garde Franche", "color": "aqua"}
attribute @s minecraft:max_health base set 22
data modify entity @s Health set value 22.0f
loot replace entity @s armor.chest loot royaumes:equip/cites_arbaletrier/armor_chest
loot replace entity @s armor.head loot royaumes:equip/cites_arbaletrier/armor_head
loot replace entity @s weapon.mainhand loot royaumes:equip/cites_arbaletrier/weapon_mainhand
effect give @s minecraft:fire_resistance infinite 0 true
data modify entity @s DeathLootTable set value "royaumes:mobs/cites_arbaletrier"
