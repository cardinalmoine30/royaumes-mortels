function royaumes:rpg/besoin
execute if score @s rm_niveau matches 61.. run return 0
execute if score @s rm_gloire >= @s rm_besoin run function royaumes:rpg/niveau_sup
