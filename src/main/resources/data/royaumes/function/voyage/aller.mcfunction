# Voyage vers le Royaume choisi dans la carte (trigger rm_voyage)
particle minecraft:reverse_portal ~ ~1 ~ 0.5 1 0.5 0.2 120
playsound minecraft:block.portal.travel player @s ~ ~ ~ 0.4 1.3
execute if score @s rm_voyage matches 1 run function royaumes:faille/vers {dim:"royaumes:royaumes_mortels",nom:"Azyr, Royaume des Cieux",c:"aqua"}
execute if score @s rm_voyage matches 2 run function royaumes:faille/vers {dim:"royaumes:ghyran",nom:"Ghyran, Royaume de la Vie",c:"green"}
execute if score @s rm_voyage matches 3 run function royaumes:faille/vers {dim:"royaumes:aqshy",nom:"Aqshy, Royaume du Feu",c:"gold"}
execute if score @s rm_voyage matches 4 run function royaumes:faille/vers {dim:"royaumes:shyish",nom:"Shyish, Royaume de la Mort",c:"dark_purple"}
execute if score @s rm_voyage matches 5 run function royaumes:faille/vers {dim:"royaumes:ghur",nom:"Ghur, Royaume des Bêtes",c:"gold"}
execute if score @s rm_voyage matches 6 run function royaumes:faille/vers {dim:"royaumes:chamon",nom:"Chamon, Royaume du Métal",c:"gray"}
execute if score @s rm_voyage matches 7 run function royaumes:faille/vers {dim:"royaumes:ulgu",nom:"Ulgu, Royaume des Ombres",c:"dark_gray"}
execute if score @s rm_voyage matches 8 run function royaumes:faille/vers {dim:"royaumes:hysh",nom:"Hysh, Royaume de la Lumière",c:"white"}
execute if score @s rm_voyage matches 9 run function royaumes:faille/vers {dim:"royaumes:huit_points",nom:"Les Huit-Points du Chaos",c:"dark_red"}
execute if score @s rm_voyage matches 99 run function royaumes:pierre/vers_monde
scoreboard players set @s rm_voyage 0
