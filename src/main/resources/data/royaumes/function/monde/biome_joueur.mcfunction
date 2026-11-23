scoreboard players set @s rm_bnow 0
execute if biome ~ ~ ~ royaumes:azyr_cimes run scoreboard players set @s rm_bnow 1
execute if biome ~ ~ ~ royaumes:hysh_plateaux run scoreboard players set @s rm_bnow 2
execute if biome ~ ~ ~ royaumes:ghyran_jade run scoreboard players set @s rm_bnow 3
execute if biome ~ ~ ~ royaumes:ghyran_marais run scoreboard players set @s rm_bnow 4
execute if biome ~ ~ ~ royaumes:ghur_terres run scoreboard players set @s rm_bnow 5
execute if biome ~ ~ ~ royaumes:ghur_jungle run scoreboard players set @s rm_bnow 6
execute if biome ~ ~ ~ royaumes:aqshy_cendres run scoreboard players set @s rm_bnow 7
execute if biome ~ ~ ~ royaumes:chamon_desert run scoreboard players set @s rm_bnow 8
execute if biome ~ ~ ~ royaumes:shyish_terres run scoreboard players set @s rm_bnow 9
execute if biome ~ ~ ~ royaumes:ulgu_brumes run scoreboard players set @s rm_bnow 10
execute if biome ~ ~ ~ royaumes:ulgu_mer run scoreboard players set @s rm_bnow 11
execute if biome ~ ~ ~ royaumes:chaos_desolation run scoreboard players set @s rm_bnow 12
execute if biome ~ ~ ~ royaumes:terres_rongees run scoreboard players set @s rm_bnow 13
execute if biome ~ ~ ~ royaumes:aqshy_volcans run scoreboard players set @s rm_bnow 14
execute if biome ~ ~ ~ royaumes:ghyran_wyldwood run scoreboard players set @s rm_bnow 15
execute if biome ~ ~ ~ royaumes:ulgu_marais_lune run scoreboard players set @s rm_bnow 16
execute if biome ~ ~ ~ royaumes:hysh_iles run scoreboard players set @s rm_bnow 17
execute if biome ~ ~ ~ royaumes:azyr_vallees run scoreboard players set @s rm_bnow 18
execute if biome ~ ~ ~ royaumes:ghur_savane run scoreboard players set @s rm_bnow 19
execute if biome ~ ~ ~ royaumes:chamon_collines run scoreboard players set @s rm_bnow 20
execute if biome ~ ~ ~ royaumes:shyish_sables run scoreboard players set @s rm_bnow 21
execute unless score @s rm_bnow = @s rm_biome run function royaumes:monde/biome_titre
