# Traite le choix de faction (trigger rm_choix)
execute if score @s rm_faction matches 1.. run return run scoreboard players set @s rm_choix 0
execute if score @s rm_choix matches 1 run function royaumes:factions/choisir/stormcast
execute if score @s rm_choix matches 2 run function royaumes:factions/choisir/cites
execute if score @s rm_choix matches 3 run function royaumes:factions/choisir/fyreslayers
execute if score @s rm_choix matches 4 run function royaumes:factions/choisir/kharadron
execute if score @s rm_choix matches 5 run function royaumes:factions/choisir/khaine
execute if score @s rm_choix matches 6 run function royaumes:factions/choisir/idoneth
execute if score @s rm_choix matches 7 run function royaumes:factions/choisir/lumineth
execute if score @s rm_choix matches 8 run function royaumes:factions/choisir/seraphon
execute if score @s rm_choix matches 9 run function royaumes:factions/choisir/sylvaneth
execute if score @s rm_choix matches 10 run function royaumes:factions/choisir/esclaves
execute if score @s rm_choix matches 11 run function royaumes:factions/choisir/khorne
execute if score @s rm_choix matches 12 run function royaumes:factions/choisir/tzeentch
execute if score @s rm_choix matches 13 run function royaumes:factions/choisir/slaanesh
execute if score @s rm_choix matches 14 run function royaumes:factions/choisir/nurgle
execute if score @s rm_choix matches 15 run function royaumes:factions/choisir/skaven
execute if score @s rm_choix matches 16 run function royaumes:factions/choisir/hashut
execute if score @s rm_choix matches 17 run function royaumes:factions/choisir/nighthaunt
execute if score @s rm_choix matches 18 run function royaumes:factions/choisir/soulblight
execute if score @s rm_choix matches 19 run function royaumes:factions/choisir/ossiarch
execute if score @s rm_choix matches 20 run function royaumes:factions/choisir/fec
execute if score @s rm_choix matches 21 run function royaumes:factions/choisir/ironjawz
execute if score @s rm_choix matches 22 run function royaumes:factions/choisir/kruleboyz
execute if score @s rm_choix matches 23 run function royaumes:factions/choisir/gitz
execute if score @s rm_choix matches 24 run function royaumes:factions/choisir/ogors
execute if score @s rm_choix matches 25 run function royaumes:factions/choisir/behemat
scoreboard players set @s rm_choix 0
scoreboard players enable @s rm_choix
