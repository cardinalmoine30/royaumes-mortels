execute as @a[scores={rm_faction=1}] run function royaumes:factions/dons/stormcast
execute as @a[scores={rm_faction=2}] run function royaumes:factions/dons/cites
execute as @a[scores={rm_faction=3}] run function royaumes:factions/dons/fyreslayers
execute as @a[scores={rm_faction=4}] run function royaumes:factions/dons/kharadron
execute as @a[scores={rm_faction=5}] run function royaumes:factions/dons/khaine
execute as @a[scores={rm_faction=6}] run function royaumes:factions/dons/idoneth
execute as @a[scores={rm_faction=7}] run function royaumes:factions/dons/lumineth
execute as @a[scores={rm_faction=8}] run function royaumes:factions/dons/seraphon
execute as @a[scores={rm_faction=9}] run function royaumes:factions/dons/sylvaneth
execute as @a[scores={rm_faction=10}] run function royaumes:factions/dons/esclaves
execute as @a[scores={rm_faction=11}] run function royaumes:factions/dons/khorne
execute as @a[scores={rm_faction=12}] run function royaumes:factions/dons/tzeentch
execute as @a[scores={rm_faction=13}] run function royaumes:factions/dons/slaanesh
execute as @a[scores={rm_faction=14}] run function royaumes:factions/dons/nurgle
execute as @a[scores={rm_faction=15}] run function royaumes:factions/dons/skaven
execute as @a[scores={rm_faction=16}] run function royaumes:factions/dons/hashut
execute as @a[scores={rm_faction=17}] run function royaumes:factions/dons/nighthaunt
execute as @a[scores={rm_faction=18}] run function royaumes:factions/dons/soulblight
execute as @a[scores={rm_faction=19}] run function royaumes:factions/dons/ossiarch
execute as @a[scores={rm_faction=20}] run function royaumes:factions/dons/fec
execute as @a[scores={rm_faction=21}] run function royaumes:factions/dons/ironjawz
execute as @a[scores={rm_faction=22}] run function royaumes:factions/dons/kruleboyz
execute as @a[scores={rm_faction=23}] run function royaumes:factions/dons/gitz
execute as @a[scores={rm_faction=24}] run function royaumes:factions/dons/ogors
execute as @a[scores={rm_faction=25}] run function royaumes:factions/dons/behemat
# Soulblight : faiblesse en plein soleil
execute store result score #jour rm_tmp run time query time
scoreboard players operation #jour rm_tmp %= #24000 rm_const
execute if score #jour rm_tmp matches 0..12000 as @a[scores={rm_faction=18}] at @s if predicate royaumes:sous_le_ciel run effect give @s minecraft:weakness 6 0 true
execute as @a run function royaumes:rpg/maintenir
