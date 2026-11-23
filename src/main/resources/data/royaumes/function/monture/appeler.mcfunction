# Corne d'appel : rappelle (ou fait naître) la monture de la faction du joueur, puis le met en selle
execute unless score @s rm_faction matches 1.. run return run title @s actionbar {"text": "Choisis d'abord une faction : ta monture en dépend.", "color": "red"}
execute if score @s rm_cdm matches 1.. run return run title @s actionbar {"text": "La corne résonne encore…", "color": "gray"}
scoreboard players set @s rm_cdm 4
execute unless score @s rm_id matches 1.. run function royaumes:monture/numero
scoreboard players operation #id rm_tmp = @s rm_id
playsound minecraft:item.goat_horn.sound.0 player @a ~ ~ ~ 1.2 0.9
execute as @e[type=#royaumes:montures,distance=..256] if score @s rm_id = #id rm_tmp run tag @s add rm_trouvee
execute if entity @e[type=#royaumes:montures,tag=rm_trouvee,distance=..256] run return run function royaumes:monture/rappeler
execute if score @s rm_faction matches 1 run summon royaumes:monture_dracoth ~ ~ ~ {Tags:["rm_nouvelle"],PersistenceRequired:1b}
execute if score @s rm_faction matches 2 run summon royaumes:monture_destrier ~ ~ ~ {Tags:["rm_nouvelle"],PersistenceRequired:1b}
execute if score @s rm_faction matches 3 run summon royaumes:monture_magmadroth ~ ~ ~ {Tags:["rm_nouvelle"],PersistenceRequired:1b}
execute if score @s rm_faction matches 4 run summon royaumes:monture_gunhauler ~ ~ ~ {Tags:["rm_nouvelle"],PersistenceRequired:1b}
execute if score @s rm_faction matches 5 run summon royaumes:monture_coursier_ombre ~ ~ ~ {Tags:["rm_nouvelle"],PersistenceRequired:1b}
execute if score @s rm_faction matches 6 run summon royaumes:monture_ishlaen ~ ~ ~ {Tags:["rm_nouvelle"],PersistenceRequired:1b}
execute if score @s rm_faction matches 7 run summon royaumes:monture_destrier_aube ~ ~ ~ {Tags:["rm_nouvelle"],PersistenceRequired:1b}
execute if score @s rm_faction matches 8 run summon royaumes:monture_aggradon ~ ~ ~ {Tags:["rm_nouvelle"],PersistenceRequired:1b}
execute if score @s rm_faction matches 9 run summon royaumes:monture_cerf_wyldwood ~ ~ ~ {Tags:["rm_nouvelle"],PersistenceRequired:1b}
execute if score @s rm_faction matches 10 run summon royaumes:monture_destrier_chaos ~ ~ ~ {Tags:["rm_nouvelle"],PersistenceRequired:1b}
execute if score @s rm_faction matches 11 run summon royaumes:monture_juggernaut ~ ~ ~ {Tags:["rm_nouvelle"],PersistenceRequired:1b}
execute if score @s rm_faction matches 12 run summon royaumes:monture_disque ~ ~ ~ {Tags:["rm_nouvelle"],PersistenceRequired:1b}
execute if score @s rm_faction matches 13 run summon royaumes:monture_seeker ~ ~ ~ {Tags:["rm_nouvelle"],PersistenceRequired:1b}
execute if score @s rm_faction matches 14 run summon royaumes:monture_pusgoyle ~ ~ ~ {Tags:["rm_nouvelle"],PersistenceRequired:1b}
execute if score @s rm_faction matches 15 run summon royaumes:monture_gnaw_beast ~ ~ ~ {Tags:["rm_nouvelle"],PersistenceRequired:1b}
execute if score @s rm_faction matches 16 run summon royaumes:monture_taurus ~ ~ ~ {Tags:["rm_nouvelle"],PersistenceRequired:1b}
execute if score @s rm_faction matches 17 run summon royaumes:monture_dreadblade ~ ~ ~ {Tags:["rm_nouvelle"],PersistenceRequired:1b}
execute if score @s rm_faction matches 18 run summon royaumes:monture_cauchemar ~ ~ ~ {Tags:["rm_nouvelle"],PersistenceRequired:1b}
execute if score @s rm_faction matches 19 run summon royaumes:monture_kavalos ~ ~ ~ {Tags:["rm_nouvelle"],PersistenceRequired:1b}
execute if score @s rm_faction matches 20 run summon royaumes:monture_morbheg ~ ~ ~ {Tags:["rm_nouvelle"],PersistenceRequired:1b}
execute if score @s rm_faction matches 21 run summon royaumes:monture_gore_grunta ~ ~ ~ {Tags:["rm_nouvelle"],PersistenceRequired:1b}
execute if score @s rm_faction matches 22 run summon royaumes:monture_gnashtoof ~ ~ ~ {Tags:["rm_nouvelle"],PersistenceRequired:1b}
execute if score @s rm_faction matches 23 run summon royaumes:monture_squig ~ ~ ~ {Tags:["rm_nouvelle"],PersistenceRequired:1b}
execute if score @s rm_faction matches 24 run summon royaumes:monture_mournfang ~ ~ ~ {Tags:["rm_nouvelle"],PersistenceRequired:1b}
execute if score @s rm_faction matches 25 run summon royaumes:monture_mammouth ~ ~ ~ {Tags:["rm_nouvelle"],PersistenceRequired:1b}
scoreboard players operation @e[type=#royaumes:montures,tag=rm_nouvelle,distance=..4] rm_id = #id rm_tmp
ride @s mount @e[type=#royaumes:montures,tag=rm_nouvelle,limit=1,sort=nearest]
tag @e[type=#royaumes:montures,tag=rm_nouvelle] remove rm_nouvelle
particle minecraft:cloud ~ ~0.5 ~ 0.8 0.3 0.8 0.02 30
title @s actionbar {"text": "Ta monture répond à l'appel !", "color": "gold"}
