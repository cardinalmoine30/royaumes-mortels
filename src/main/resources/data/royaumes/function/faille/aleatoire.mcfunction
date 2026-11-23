execute store result score #d rm_tmp run random value 1..11
execute if score #d rm_tmp matches 1..2 run return run function royaumes:faille/vers {dim:"royaumes:royaumes_mortels",nom:"Azyr, Royaume des Cieux",c:"aqua"}
execute if score #d rm_tmp matches 3..3 run return run function royaumes:faille/vers {dim:"royaumes:ghyran",nom:"Ghyran, Royaume de la Vie",c:"green"}
execute if score #d rm_tmp matches 4..4 run return run function royaumes:faille/vers {dim:"royaumes:aqshy",nom:"Aqshy, Royaume du Feu",c:"gold"}
execute if score #d rm_tmp matches 5..5 run return run function royaumes:faille/vers {dim:"royaumes:shyish",nom:"Shyish, Royaume de la Mort",c:"dark_purple"}
execute if score #d rm_tmp matches 6..6 run return run function royaumes:faille/vers {dim:"royaumes:ghur",nom:"Ghur, Royaume des Bêtes",c:"gold"}
execute if score #d rm_tmp matches 7..7 run return run function royaumes:faille/vers {dim:"royaumes:chamon",nom:"Chamon, Royaume du Métal",c:"gray"}
execute if score #d rm_tmp matches 8..8 run return run function royaumes:faille/vers {dim:"royaumes:ulgu",nom:"Ulgu, Royaume des Ombres",c:"dark_gray"}
execute if score #d rm_tmp matches 9..10 run return run function royaumes:faille/vers {dim:"royaumes:hysh",nom:"Hysh, Royaume de la Lumière",c:"white"}
execute if score #d rm_tmp matches 11..11 run return run function royaumes:faille/vers {dim:"royaumes:huit_points",nom:"Les Huit-Points du Chaos",c:"dark_red"}
