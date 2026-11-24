execute unless entity @p[distance=..8,scores={rm_faction=7..7}] run return 0
execute unless entity @e[type=minecraft:item,distance=..1.5,nbt={Item:{id:"royaumes:eclat_hysh"}},limit=1] run return 0
execute store result score #c rm_tmp run data get entity @e[type=minecraft:item,distance=..1.5,nbt={Item:{id:"royaumes:eclat_hysh"}},limit=1] Item.count
execute if score #c rm_tmp matches ..5 run return 0
execute unless entity @e[type=minecraft:item,distance=..1.5,nbt={Item:{id:"minecraft:bow"}},limit=1] run return 0
execute store result score #c rm_tmp run data get entity @e[type=minecraft:item,distance=..1.5,nbt={Item:{id:"minecraft:bow"}},limit=1] Item.count
execute if score #c rm_tmp matches ..0 run return 0
execute as @e[type=minecraft:item,distance=..1.5,nbt={Item:{id:"royaumes:eclat_hysh"}},limit=1] run function royaumes:forge/retirer {n:6}
execute as @e[type=minecraft:item,distance=..1.5,nbt={Item:{id:"minecraft:bow"}},limit=1] run function royaumes:forge/retirer {n:1}
loot spawn ~ ~0.6 ~ loot royaumes:forge/arc_hysh
particle minecraft:lava ~ ~0.8 ~ 0.3 0.3 0.3 0 12
particle minecraft:enchant ~ ~1 ~ 0.4 0.6 0.4 0.5 40
playsound minecraft:block.anvil.use block @a[distance=..16] ~ ~ ~ 1 0.9
playsound minecraft:block.smithing_table.use block @a[distance=..16] ~ ~ ~ 1 1
tellraw @a[distance=..8] [{"text": "⚒ Forgé : ", "color": "gold"}, {"text": "Arc de Lumière de Hysh", "color": "yellow"}]
scoreboard players set #gain rm_tmp 5
execute as @p[distance=..8] run function royaumes:rpg/ajouter
return 1
