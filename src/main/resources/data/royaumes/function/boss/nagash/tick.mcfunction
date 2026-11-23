execute store result bossbar royaumes:nagash value run data get entity @s Health
bossbar set royaumes:nagash players @a[distance=..56]
execute unless entity @a[distance=..28,gamemode=!spectator,gamemode=!creative] run return 0
scoreboard players add @s rm_bt 1
execute store result score #hp rm_tmp run data get entity @s Health
execute if entity @s[tag=!rm_phase2] if score #hp rm_tmp matches ..450 run function royaumes:boss/nagash/phase2
execute if entity @s[tag=rm_phase2] if score @s rm_bt matches 4.. run function royaumes:boss/nagash/attaque
execute if score @s rm_bt matches 6.. run function royaumes:boss/nagash/attaque
