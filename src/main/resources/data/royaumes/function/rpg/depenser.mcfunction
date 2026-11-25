scoreboard players set #muet rm_tmp 0
execute if score @s rm_comp matches 11..16 run scoreboard players set #muet rm_tmp 1
execute if score @s rm_comp matches 11..16 run scoreboard players remove @s rm_comp 10
execute if score @s rm_comp matches 6 run function royaumes:rpg/monter/fortune
execute if score @s rm_comp matches 5 run function royaumes:rpg/monter/endurance
execute if score @s rm_comp matches 4 run function royaumes:rpg/monter/mineur
execute if score @s rm_comp matches 3 run function royaumes:rpg/monter/agilite
execute if score @s rm_comp matches 2 run function royaumes:rpg/monter/force
execute if score @s rm_comp matches 1 run function royaumes:rpg/monter/vigueur
scoreboard players set @s rm_comp 0
scoreboard players enable @s rm_comp
execute if score #muet rm_tmp matches 0 run function royaumes:rpg/fiche
