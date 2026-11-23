execute store result bossbar royaumes:thanquol value run data get entity @s Health
bossbar set royaumes:thanquol players @a[distance=..56]
execute unless entity @a[distance=..28,gamemode=!spectator,gamemode=!creative] run return 0
scoreboard players add @s rm_bt 1
execute store result score #hp rm_tmp run data get entity @s Health
execute if entity @s[tag=!rm_phase2] if score #hp rm_tmp matches ..375 run function royaumes:boss/thanquol/phase2
execute if entity @s[tag=rm_phase2] if score @s rm_bt matches 4.. run function royaumes:boss/thanquol/attaque
execute if score @s rm_bt matches 6.. run function royaumes:boss/thanquol/attaque
