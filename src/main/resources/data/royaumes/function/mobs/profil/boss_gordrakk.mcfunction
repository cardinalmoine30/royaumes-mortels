tag @s add rm_c
tag @s remove rm_spawn
team join rm_boss @s
data modify entity @s CustomName set value {"text": "Krognak, le Poing de Brog", "color": "gold"}
data modify entity @s IsBaby set value 0b
attribute @s minecraft:max_health base set 800
attribute @s minecraft:attack_damage base set 19
attribute @s minecraft:scale base set 2.6
attribute @s minecraft:armor base set 14
attribute @s minecraft:knockback_resistance base set 1.0
attribute @s minecraft:movement_speed base set 0.27
attribute @s minecraft:follow_range base set 48
data modify entity @s Health set value 800.0f
loot replace entity @s armor.head loot royaumes:equip/boss_gordrakk/armor_head
loot replace entity @s armor.chest loot royaumes:equip/boss_gordrakk/armor_chest
loot replace entity @s armor.legs loot royaumes:equip/boss_gordrakk/armor_legs
loot replace entity @s weapon.mainhand loot royaumes:equip/boss_gordrakk/weapon_mainhand
loot replace entity @s weapon.offhand loot royaumes:equip/boss_gordrakk/weapon_offhand
effect give @s minecraft:fire_resistance infinite 0 true
data modify entity @s DeathLootTable set value "royaumes:boss/gordrakk"
tag @s add rm_boss
tag @s add rm_boss_gordrakk
data modify entity @s PersistenceRequired set value 1b
data modify entity @s CustomNameVisible set value 1b
tellraw @a[distance=..96] [{"text": "☠ ", "color": "gold"}, {"text": "Krognak, le Poing de Brog", "color": "gold", "bold": true}, {"text": " « GRAAAAAH ! »", "color": "gray", "italic": true}]
playsound minecraft:entity.wither.spawn hostile @a[distance=..96] ~ ~ ~ 2 0.6
