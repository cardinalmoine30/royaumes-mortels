$scoreboard players set #r rm_tmp $(n)
execute store result score #c rm_tmp run data get entity @s Item.count
scoreboard players operation #c rm_tmp -= #r rm_tmp
execute store result entity @s Item.count int 1 run scoreboard players get #c rm_tmp
execute if score #c rm_tmp matches ..0 run kill @s
