execute as @a[scores={rm_choix=1..}] run function royaumes:choix/traiter
execute as @a[scores={rm_pierre=1..}] at @s run function royaumes:pierre/utiliser
execute as @a[scores={rm_codex=1..}] run function royaumes:codex
execute as @e[type=minecraft:marker,tag=rm_faille] at @s run function royaumes:faille/tick
execute as @e[type=minecraft:marker,tag=rm_tyro_debut] at @s as @a[distance=..1.5,tag=!rm_tyro] run function royaumes:tyrolienne/depart
execute as @a[tag=rm_tyro] at @s run function royaumes:tyrolienne/glisser
