execute as @a unless score @s rm_niveau matches 1.. run function royaumes:rpg/init
execute as @a[scores={rm_m0=1..}] run function royaumes:rpg/source {obj:"rm_m0",val:2}
execute as @a[scores={rm_m1=1..}] run function royaumes:rpg/source {obj:"rm_m1",val:2}
execute as @a[scores={rm_m2=1..}] run function royaumes:rpg/source {obj:"rm_m2",val:2}
execute as @a[scores={rm_m3=1..}] run function royaumes:rpg/source {obj:"rm_m3",val:2}
execute as @a[scores={rm_m4=1..}] run function royaumes:rpg/source {obj:"rm_m4",val:3}
execute as @a[scores={rm_m5=1..}] run function royaumes:rpg/source {obj:"rm_m5",val:3}
execute as @a[scores={rm_m6=1..}] run function royaumes:rpg/source {obj:"rm_m6",val:5}
execute as @a[scores={rm_m7=1..}] run function royaumes:rpg/source {obj:"rm_m7",val:5}
execute as @a[scores={rm_m8=1..}] run function royaumes:rpg/source {obj:"rm_m8",val:3}
execute as @a[scores={rm_m9=1..}] run function royaumes:rpg/source {obj:"rm_m9",val:3}
execute as @a[scores={rm_m10=1..}] run function royaumes:rpg/source {obj:"rm_m10",val:4}
execute as @a[scores={rm_m11=1..}] run function royaumes:rpg/source {obj:"rm_m11",val:4}
execute as @a[scores={rm_m12=1..}] run function royaumes:rpg/source {obj:"rm_m12",val:15}
execute as @a[scores={rm_m13=1..}] run function royaumes:rpg/source {obj:"rm_m13",val:15}
execute as @a[scores={rm_m14=1..}] run function royaumes:rpg/source {obj:"rm_m14",val:15}
execute as @a[scores={rm_m15=1..}] run function royaumes:rpg/source {obj:"rm_m15",val:15}
execute as @a[scores={rm_m16=1..}] run function royaumes:rpg/source {obj:"rm_m16",val:3}
execute as @a[scores={rm_m17=1..}] run function royaumes:rpg/source {obj:"rm_m17",val:2}
execute as @a[scores={rm_m18=1..}] run function royaumes:rpg/source {obj:"rm_m18",val:30}
execute as @a[scores={rm_m19=1..}] run function royaumes:rpg/source {obj:"rm_m19",val:6}
execute as @a[scores={rm_m20=1..}] run function royaumes:rpg/source {obj:"rm_m20",val:6}
execute as @a[scores={rm_m21=1..}] run function royaumes:rpg/source {obj:"rm_m21",val:5}
execute as @a[scores={rm_m22=1..}] run function royaumes:rpg/source {obj:"rm_m22",val:3}
execute as @a[scores={rm_k_mob=1..}] run function royaumes:rpg/source {obj:"rm_k_mob",val:2}
execute as @a[scores={rm_k_or=1..}] run function royaumes:rpg/source {obj:"rm_k_or",val:8}
execute as @a[scores={rm_k_cr=1..}] run function royaumes:rpg/source {obj:"rm_k_cr",val:8}
execute as @a[scores={rm_k_dp=1..}] run function royaumes:rpg/source {obj:"rm_k_dp",val:8}
execute as @a[scores={rm_k_dg=1..}] run function royaumes:rpg/source {obj:"rm_k_dg",val:8}
execute as @a[scores={rm_k_boss=1..}] run function royaumes:rpg/source {obj:"rm_k_boss",val:500}
execute as @a[scores={rm_rpg=1..}] run function royaumes:rpg/ouvrir
execute as @a[scores={rm_comp=1..}] run function royaumes:rpg/depenser
execute as @a[scores={rm_forge=1..}] run function royaumes:forge/ouvrir
scoreboard players enable @a rm_rpg
scoreboard players enable @a rm_forge
