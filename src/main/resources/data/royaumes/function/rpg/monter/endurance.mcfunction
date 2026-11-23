execute unless score @s rm_pts matches 1.. run return run tellraw @s {"text": "Aucun point de compétence disponible.", "color": "red"}
execute if score @s rm_endurance matches 10.. run return run tellraw @s {"text": "Endurance est déjà au maximum.", "color": "red"}
scoreboard players add @s rm_endurance 1
scoreboard players remove @s rm_pts 1
function royaumes:rpg/appliquer/endurance
playsound minecraft:block.enchantment_table.use player @s ~ ~ ~ 1 1.2
tellraw @s [{"text": "✦ Endurance → rang ", "color": "dark_green"}, {"score": {"name": "@s", "objective": "rm_endurance"}, "color": "dark_green"}]
