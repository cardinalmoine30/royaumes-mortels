execute unless entity @p[distance=..8,scores={rm_faction=24..24}] run return 0
execute unless entity @e[type=minecraft:item,distance=..1.5,nbt={Item:{id:"royaumes:eclat_ghur"}},limit=1] run return 0
execute store result score #c rm_tmp run data get entity @e[type=minecraft:item,distance=..1.5,nbt={Item:{id:"royaumes:eclat_ghur"}},limit=1] Item.count
execute if score #c rm_tmp matches ..0 run return 0
execute unless entity @e[type=minecraft:item,distance=..1.5,nbt={Item:{id:"minecraft:cooked_beef"}},limit=1] run return 0
execute store result score #c rm_tmp run data get entity @e[type=minecraft:item,distance=..1.5,nbt={Item:{id:"minecraft:cooked_beef"}},limit=1] Item.count
execute if score #c rm_tmp matches ..3 run return 0
execute as @e[type=minecraft:item,distance=..1.5,nbt={Item:{id:"royaumes:eclat_ghur"}},limit=1] run function royaumes:forge/retirer {n:1}
execute as @e[type=minecraft:item,distance=..1.5,nbt={Item:{id:"minecraft:cooked_beef"}},limit=1] run function royaumes:forge/retirer {n:4}
loot spawn ~ ~0.6 ~ loot royaumes:forge/festin_ogor
particle minecraft:lava ~ ~0.8 ~ 0.3 0.3 0.3 0 12
particle minecraft:enchant ~ ~1 ~ 0.4 0.6 0.4 0.5 40
playsound minecraft:block.anvil.use block @a[distance=..16] ~ ~ ~ 1 0.9
playsound minecraft:block.smithing_table.use block @a[distance=..16] ~ ~ ~ 1 1
tellraw @a[distance=..8] [{"text": "⚒ Forgé : ", "color": "gold"}, {"text": "Festin d'Ogre ×2", "color": "yellow"}]
scoreboard players set #gain rm_tmp 5
execute as @p[distance=..8] run function royaumes:rpg/ajouter
return 1
