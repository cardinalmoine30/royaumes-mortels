schedule function royaumes:boucle_seconde 20t replace
# Reconnexion : rouvrir le menu si aucune faction
execute as @a[scores={rm_quitte=1..}] run scoreboard players set @s rm_menu 0
scoreboard players set @a[scores={rm_quitte=1..}] rm_quitte 0
scoreboard players enable @a rm_codex
scoreboard players remove @a[scores={rm_menu=1..}] rm_menu 1
execute as @a unless score @s rm_faction matches 1.. unless score @s rm_menu matches 1.. run function royaumes:choix/ouvrir
scoreboard players remove @a[scores={rm_cd=1..}] rm_cd 1
# Dons toutes les 5 secondes
scoreboard players add #cycle rm_tmp 1
scoreboard players operation #c5 rm_tmp = #cycle rm_tmp
scoreboard players operation #c5 rm_tmp %= #5 rm_const
execute if score #c5 rm_tmp matches 0 run function royaumes:factions/boucle_dons
# Biomes et habitants des Royaumes
execute as @a at @s unless dimension minecraft:overworld unless dimension minecraft:the_nether unless dimension minecraft:the_end run function royaumes:monde/biome_joueur
execute as @a at @s if dimension minecraft:overworld run scoreboard players set @s rm_biome 0
execute as @a at @s if dimension minecraft:the_nether run scoreboard players set @s rm_biome 0
execute in royaumes:royaumes_mortels as @e[type=#royaumes:convertibles,tag=!rm_c,distance=0..] at @s run function royaumes:mobs/convertir
execute in royaumes:aqshy as @e[type=#royaumes:convertibles,tag=!rm_c,distance=0..] at @s run function royaumes:mobs/convertir
execute in royaumes:shyish as @e[type=#royaumes:convertibles,tag=!rm_c,distance=0..] at @s run function royaumes:mobs/convertir
execute in royaumes:ghur as @e[type=#royaumes:convertibles,tag=!rm_c,distance=0..] at @s run function royaumes:mobs/convertir
execute in royaumes:huit_points as @e[type=#royaumes:convertibles,tag=!rm_c,distance=0..] at @s run function royaumes:mobs/convertir
execute in royaumes:hysh as @e[type=#royaumes:convertibles,tag=!rm_c,distance=0..] at @s run function royaumes:mobs/convertir
execute as @e[tag=rm_spawn] at @s run function royaumes:mobs/marqueur
execute as @e[type=minecraft:marker,tag=rm_portail] at @s as @a[distance=..1.8] unless score @s rm_cd matches 1.. at @s run function royaumes:pierre/portail
function royaumes:rpg/boucle
function royaumes:boss/boucle
execute as @a at @s unless dimension minecraft:overworld unless dimension minecraft:the_nether unless dimension minecraft:the_end run function royaumes:rpg/decouvrir
function royaumes:ambiance/boucle
