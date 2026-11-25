tag @s add rm_c
tag @s remove rm_spawn
team join rm_ordre @s
data modify entity @s CustomName set value {"text": "Justicier Foudroyés", "color": "gold"}
attribute @s minecraft:max_health base set 30
attribute @s minecraft:scale base set 1.15
data modify entity @s Health set value 30.0f
loot replace entity @s armor.chest loot royaumes:equip/sc_judicator/armor_chest
loot replace entity @s armor.legs loot royaumes:equip/sc_judicator/armor_legs
loot replace entity @s armor.feet loot royaumes:equip/sc_judicator/armor_feet
loot replace entity @s armor.head loot royaumes:equip/sc_judicator/armor_head
loot replace entity @s weapon.mainhand loot royaumes:equip/sc_judicator/weapon_mainhand
effect give @s minecraft:fire_resistance infinite 0 true
data modify entity @s DeathLootTable set value "royaumes:mobs/sc_judicator"
