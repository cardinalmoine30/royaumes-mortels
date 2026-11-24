schedule function royaumes:forge/boucle 10t replace
execute as @e[type=minecraft:item] at @s if block ~ ~-0.3 ~ minecraft:smithing_table run function royaumes:forge/essayer
execute as @e[type=minecraft:item,nbt={Item:{id:"royaumes:pierre_royaumes_brute"}}] at @s if block ~ ~-0.3 ~ minecraft:amethyst_block align xyz run function royaumes:faille/activer
