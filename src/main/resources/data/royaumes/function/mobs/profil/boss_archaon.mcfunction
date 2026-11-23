tag @s add rm_c
tag @s remove rm_spawn
team join rm_boss @s
data modify entity @s CustomName set value {"text": "Archaon, l'Élu Éternel", "color": "dark_red"}
data modify entity @s IsBaby set value 0b
attribute @s minecraft:max_health base set 1000
attribute @s minecraft:attack_damage base set 20
attribute @s minecraft:scale base set 2.4
attribute @s minecraft:armor base set 18
attribute @s minecraft:knockback_resistance base set 1.0
attribute @s minecraft:movement_speed base set 0.27
attribute @s minecraft:follow_range base set 48
data modify entity @s Health set value 1000.0f
loot replace entity @s armor.head loot royaumes:equip/boss_archaon/armor_head
loot replace entity @s armor.chest loot royaumes:equip/boss_archaon/armor_chest
loot replace entity @s armor.legs loot royaumes:equip/boss_archaon/armor_legs
loot replace entity @s armor.feet loot royaumes:equip/boss_archaon/armor_feet
loot replace entity @s weapon.mainhand loot royaumes:equip/boss_archaon/weapon_mainhand
loot replace entity @s weapon.offhand loot royaumes:equip/boss_archaon/weapon_offhand
effect give @s minecraft:fire_resistance infinite 0 true
data modify entity @s DeathLootTable set value "royaumes:boss/archaon"
tag @s add rm_boss
tag @s add rm_boss_archaon
data modify entity @s PersistenceRequired set value 1b
data modify entity @s CustomNameVisible set value 1b
tellraw @a[distance=..96] [{"text": "☠ ", "color": "dark_red"}, {"text": "Archaon, l'Élu Éternel", "color": "dark_red", "bold": true}, {"text": " « Je suis la Fin des Temps. »", "color": "gray", "italic": true}]
playsound minecraft:entity.wither.spawn hostile @a[distance=..96] ~ ~ ~ 2 0.6
