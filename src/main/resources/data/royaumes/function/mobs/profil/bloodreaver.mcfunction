tag @s add rm_c
tag @s remove rm_spawn
team join rm_chaos @s
data modify entity @s CustomName set value {"text": "Pillard de Sang de Sangrath", "color": "dark_red"}
data modify entity @s IsBaby set value 0b
attribute @s minecraft:max_health base set 26
attribute @s minecraft:attack_damage base set 6
attribute @s minecraft:movement_speed base set 0.28
data modify entity @s Health set value 26.0f
loot replace entity @s armor.chest loot royaumes:equip/bloodreaver/armor_chest
loot replace entity @s armor.head loot royaumes:equip/bloodreaver/armor_head
loot replace entity @s weapon.mainhand loot royaumes:equip/bloodreaver/weapon_mainhand
effect give @s minecraft:strength infinite 0 true
effect give @s minecraft:fire_resistance infinite 0 true
data modify entity @s DeathLootTable set value "royaumes:mobs/bloodreaver"
