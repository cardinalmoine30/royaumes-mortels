execute store result score #f rm_tmp run random value 1..8
execute if score #f rm_tmp matches 1 run summon minecraft:lightning_bolt ~ ~ ~
execute if score #f rm_tmp matches 1 if entity @s[tag=rm_malefoudre] run particle minecraft:dust{color:[0.4,1.0,0.2],scale:3.0} ~ ~-4 ~ 1 5 1 0 120
execute if score #f rm_tmp matches 2 run particle minecraft:electric_spark ~ ~ ~ 1 1 1 0.3 30
