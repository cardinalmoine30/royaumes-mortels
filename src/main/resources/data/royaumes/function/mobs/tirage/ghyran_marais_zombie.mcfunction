execute store result score #r rm_tmp run random value 1..3
execute if score #r rm_tmp matches 1 run return run function royaumes:mobs/profil/pestigor
execute if score #r rm_tmp matches 2 run return run function royaumes:mobs/profil/gutrippa
execute if score #r rm_tmp matches 3 run return run function royaumes:mobs/profil/gutrippa
