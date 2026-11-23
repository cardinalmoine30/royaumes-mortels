scoreboard players set @s rm_cd 10
particle minecraft:reverse_portal ~ ~1 ~ 0.6 1.2 0.6 0.1 150
playsound minecraft:block.portal.trigger player @a[distance=..16] ~ ~ ~ 0.6 1.4
execute unless dimension minecraft:overworld unless dimension minecraft:the_nether unless dimension minecraft:the_end run return run function royaumes:pierre/vers_monde
function royaumes:faille/aleatoire
