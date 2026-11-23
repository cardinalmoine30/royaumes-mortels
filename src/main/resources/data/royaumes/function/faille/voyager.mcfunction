function royaumes:faille/repousser
execute if score @s rm_cd matches 1.. run return 0
scoreboard players set @s rm_cd 4
particle minecraft:reverse_portal ~ ~1 ~ 0.5 1 0.5 0.2 120
playsound minecraft:block.portal.trigger player @s ~ ~ ~ 0.4 1.3
scoreboard players enable @s rm_voyage
scoreboard players set @s rm_voyage 0
dialog show @s royaumes:voyage
