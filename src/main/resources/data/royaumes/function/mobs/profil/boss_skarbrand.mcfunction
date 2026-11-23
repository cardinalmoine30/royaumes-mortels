tag @s add rm_c
tag @s remove rm_spawn
team join rm_boss @s
data modify entity @s CustomName set value {"text": "Skarbrand, l'Exilé", "color": "red"}
attribute @s minecraft:max_health base set 850
attribute @s minecraft:attack_damage base set 22
attribute @s minecraft:scale base set 2.8
attribute @s minecraft:armor base set 10
attribute @s minecraft:knockback_resistance base set 1.0
attribute @s minecraft:movement_speed base set 0.3
attribute @s minecraft:follow_range base set 48
data modify entity @s Health set value 850.0f
loot replace entity @s armor.chest loot royaumes:equip/boss_skarbrand/armor_chest
loot replace entity @s weapon.mainhand loot royaumes:equip/boss_skarbrand/weapon_mainhand
loot replace entity @s weapon.offhand loot royaumes:equip/boss_skarbrand/weapon_offhand
effect give @s minecraft:fire_resistance infinite 0 true
data modify entity @s DeathLootTable set value "royaumes:boss/skarbrand"
tag @s add rm_boss
tag @s add rm_boss_skarbrand
data modify entity @s PersistenceRequired set value 1b
data modify entity @s CustomNameVisible set value 1b
tellraw @a[distance=..96] [{"text": "☠ ", "color": "red"}, {"text": "Skarbrand, l'Exilé", "color": "red", "bold": true}, {"text": " « DU SANG ! DU SANG POUR KHORNE ! »", "color": "gray", "italic": true}]
playsound minecraft:entity.wither.spawn hostile @a[distance=..96] ~ ~ ~ 2 0.6
data modify entity @s IsImmuneToZombification set value 1b
