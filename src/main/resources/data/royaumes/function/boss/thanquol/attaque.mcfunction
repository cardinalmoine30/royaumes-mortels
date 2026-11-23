scoreboard players set @s rm_bt 0
execute store result score #r rm_tmp run random value 1..3
execute if score #r rm_tmp matches 1 run function royaumes:boss/thanquol/c1
execute if score #r rm_tmp matches 2 run function royaumes:boss/thanquol/c2
execute if score #r rm_tmp matches 3 run function royaumes:boss/thanquol/c3
