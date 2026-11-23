execute if score @s rm_cd matches 1.. run return run function royaumes:faille/repousser
scoreboard players set @s rm_cd 4
particle minecraft:reverse_portal ~ ~1 ~ 0.5 1 0.5 0.2 120
playsound minecraft:block.portal.travel player @s ~ ~ ~ 0.4 1.3
execute unless dimension minecraft:overworld unless dimension minecraft:the_nether unless dimension minecraft:the_end run return run function royaumes:pierre/vers_monde
function royaumes:faille/aleatoire
