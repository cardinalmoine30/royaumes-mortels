execute unless score @s rm_pts matches 1.. run return run tellraw @s {"text": "Aucun point de compétence disponible.", "color": "red"}
execute if score @s rm_force matches 10.. run return run tellraw @s {"text": "Force est déjà au maximum.", "color": "red"}
scoreboard players add @s rm_force 1
scoreboard players remove @s rm_pts 1
function royaumes:rpg/appliquer/force
playsound minecraft:block.enchantment_table.use player @s ~ ~ ~ 1 1.2
tellraw @s [{"text": "✦ Force → rang ", "color": "dark_red"}, {"score": {"name": "@s", "objective": "rm_force"}, "color": "dark_red"}]
