execute unless block ~ ~ ~ minecraft:nether_portal run return run kill @s
execute if entity @s[tag=rm_axe_x] positioned ~-1 ~-1.5 ~-0.5 as @a[dx=1,dy=2,dz=0] at @s run function royaumes:faille/voyager
execute if entity @s[tag=rm_axe_z] positioned ~-0.5 ~-1.5 ~-1 as @a[dx=0,dy=2,dz=1] at @s run function royaumes:faille/voyager
