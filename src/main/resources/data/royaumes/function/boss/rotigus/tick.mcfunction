execute store result bossbar royaumes:rotigus value run data get entity @s Health
bossbar set royaumes:rotigus players @a[distance=..56]
execute unless entity @a[distance=..28,gamemode=!spectator,gamemode=!creative] run return 0
scoreboard players add @s rm_bt 1
execute store result score #hp rm_tmp run data get entity @s Health
execute if entity @s[tag=!rm_phase2] if score #hp rm_tmp matches ..475 run function royaumes:boss/rotigus/phase2
execute if entity @s[tag=rm_phase2] if score @s rm_bt matches 4.. run function royaumes:boss/rotigus/attaque
execute if score @s rm_bt matches 6.. run function royaumes:boss/rotigus/attaque
