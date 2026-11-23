execute store result score #r rm_tmp run random value 1..4
execute if score #r rm_tmp matches 1 run return run function royaumes:mobs/profil/deathrattle
execute if score #r rm_tmp matches 2 run return run function royaumes:mobs/profil/deathrattle
execute if score #r rm_tmp matches 3 run return run function royaumes:mobs/profil/mortek
execute if score #r rm_tmp matches 4 run return run function royaumes:mobs/profil/glaivewraith
