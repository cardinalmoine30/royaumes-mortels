tag @s add rm_c
tag @s remove rm_spawn
team join rm_boss @s
data modify entity @s CustomName set value {"text": "Rotigus, le Pluvieux", "color": "dark_green"}
data modify entity @s IsBaby set value 0b
attribute @s minecraft:max_health base set 950
attribute @s minecraft:attack_damage base set 16
attribute @s minecraft:scale base set 3.2
attribute @s minecraft:armor base set 8
attribute @s minecraft:knockback_resistance base set 1.0
attribute @s minecraft:movement_speed base set 0.2
attribute @s minecraft:follow_range base set 48
data modify entity @s Health set value 950.0f
loot replace entity @s armor.chest loot royaumes:equip/boss_rotigus/armor_chest
loot replace entity @s armor.legs loot royaumes:equip/boss_rotigus/armor_legs
loot replace entity @s armor.head loot royaumes:equip/boss_rotigus/armor_head
loot replace entity @s weapon.mainhand loot royaumes:equip/boss_rotigus/weapon_mainhand
effect give @s minecraft:fire_resistance infinite 0 true
data modify entity @s DeathLootTable set value "royaumes:boss/rotigus"
tag @s add rm_boss
tag @s add rm_boss_rotigus
data modify entity @s PersistenceRequired set value 1b
data modify entity @s CustomNameVisible set value 1b
tellraw @a[distance=..96] [{"text": "☠ ", "color": "dark_green"}, {"text": "Rotigus, le Pluvieux", "color": "dark_green", "bold": true}, {"text": " « Mes enfants, recevez la bénédiction de Grand-Père ! »", "color": "gray", "italic": true}]
playsound minecraft:entity.wither.spawn hostile @a[distance=..96] ~ ~ ~ 2 0.6
