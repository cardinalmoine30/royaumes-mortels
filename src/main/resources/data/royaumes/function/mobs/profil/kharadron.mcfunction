tag @s add rm_c
tag @s remove rm_spawn
team join rm_ordre @s
data modify entity @s CustomName set value {"text": "Aéronaute Nuées", "color": "gold"}
attribute @s minecraft:max_health base set 26
attribute @s minecraft:scale base set 0.85
data modify entity @s Health set value 26.0f
loot replace entity @s armor.head loot royaumes:equip/kharadron/armor_head
loot replace entity @s armor.chest loot royaumes:equip/kharadron/armor_chest
loot replace entity @s weapon.mainhand loot royaumes:equip/kharadron/weapon_mainhand
effect give @s minecraft:fire_resistance infinite 0 true
data modify entity @s DeathLootTable set value "royaumes:mobs/kharadron"
