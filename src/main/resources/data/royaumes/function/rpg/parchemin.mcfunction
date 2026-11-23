clear @s minecraft:carrot_on_a_stick[minecraft:custom_data~{royaumes:"parchemin"}] 1
scoreboard players set #gain rm_tmp 100
function royaumes:rpg/ajouter
playsound minecraft:item.book.page_turn player @s ~ ~ ~ 1 1
particle minecraft:enchant ~ ~1 ~ 0.5 1 0.5 1 60
return 1
