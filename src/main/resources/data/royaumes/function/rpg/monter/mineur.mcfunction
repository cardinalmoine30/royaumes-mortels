execute unless score @s rm_pts matches 1.. run return run tellraw @s {"text": "Aucun point de compétence disponible.", "color": "red"}
execute if score @s rm_mineur matches 10.. run return run tellraw @s {"text": "Mineur est déjà au maximum.", "color": "red"}
scoreboard players add @s rm_mineur 1
scoreboard players remove @s rm_pts 1
function royaumes:rpg/appliquer/mineur
playsound minecraft:block.enchantment_table.use player @s ~ ~ ~ 1 1.2
tellraw @s [{"text": "✦ Mineur → rang ", "color": "gray"}, {"score": {"name": "@s", "objective": "rm_mineur"}, "color": "gray"}]
