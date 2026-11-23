tag @s add rm_c
tag @s remove rm_spawn
team join rm_mort @s
data modify entity @s CustomName set value {"text": "Glaivewraith Nighthaunt", "color": "dark_aqua"}
attribute @s minecraft:max_health base set 24
attribute @s minecraft:attack_damage base set 6
data modify entity @s Health set value 24.0f
loot replace entity @s armor.head loot royaumes:equip/glaivewraith/armor_head
loot replace entity @s armor.chest loot royaumes:equip/glaivewraith/armor_chest
loot replace entity @s weapon.mainhand loot royaumes:equip/glaivewraith/weapon_mainhand
effect give @s minecraft:invisibility infinite 0 true
effect give @s minecraft:fire_resistance infinite 0 true
data modify entity @s DeathLootTable set value "royaumes:mobs/glaivewraith"
