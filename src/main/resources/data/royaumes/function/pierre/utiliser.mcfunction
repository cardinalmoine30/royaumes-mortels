scoreboard players set @s rm_pierre 0
execute unless items entity @s weapon.* minecraft:carrot_on_a_stick[minecraft:custom_data~{royaumes:"pierre"}] run return 0
execute if score @s rm_cd matches 1.. run return run title @s actionbar {"text": "La Pierre de Royaume se recharge…", "color": "gray"}
scoreboard players set @s rm_cd 3
particle minecraft:reverse_portal ~ ~1 ~ 0.4 1 0.4 0.05 80
playsound minecraft:block.respawn_anchor.set_spawn player @a ~ ~ ~ 1 0.8
scoreboard players enable @s rm_voyage
scoreboard players set @s rm_voyage 0
dialog show @s royaumes:voyage
