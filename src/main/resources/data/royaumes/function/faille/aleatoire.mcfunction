execute store result score #d rm_tmp run random value 1..10
execute if score #d rm_tmp matches 1..4 run return run function royaumes:faille/vers {dim:"royaumes:royaumes_mortels",nom:"Les Royaumes Mortels",c:"gold"}
execute if score #d rm_tmp matches 5..5 run return run function royaumes:faille/vers {dim:"royaumes:aqshy",nom:"Aqshy, Royaume du Feu",c:"gold"}
execute if score #d rm_tmp matches 6..6 run return run function royaumes:faille/vers {dim:"royaumes:shyish",nom:"Shyish, Royaume de la Mort",c:"dark_purple"}
execute if score #d rm_tmp matches 7..7 run return run function royaumes:faille/vers {dim:"royaumes:ghur",nom:"Ghur, Royaume des Bêtes",c:"gold"}
execute if score #d rm_tmp matches 8..8 run return run function royaumes:faille/vers {dim:"royaumes:huit_points",nom:"Les Huit-Points du Chaos",c:"dark_red"}
execute if score #d rm_tmp matches 9..10 run return run function royaumes:faille/vers {dim:"royaumes:hysh",nom:"Hysh, Îles de Lumière",c:"white"}
