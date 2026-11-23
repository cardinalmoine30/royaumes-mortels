scoreboard players add @s rm_tyt 1
execute if score @s rm_tyt matches 240.. run return run function royaumes:tyrolienne/fin
execute if entity @e[type=minecraft:marker,tag=rm_tyro_fin,distance=..1.6] run return run function royaumes:tyrolienne/fin
execute unless entity @e[type=minecraft:marker,tag=rm_tyro_fin,distance=..160] run return run function royaumes:tyrolienne/fin
execute facing entity @e[type=minecraft:marker,tag=rm_tyro_fin,sort=nearest,limit=1] feet run tp @s ^ ^ ^0.6
particle minecraft:electric_spark ~ ~2.2 ~ 0.1 0.1 0.1 0 2
