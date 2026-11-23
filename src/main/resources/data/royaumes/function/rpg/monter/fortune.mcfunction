execute unless score @s rm_pts matches 1.. run return run tellraw @s {"text": "Aucun point de compétence disponible.", "color": "red"}
execute if score @s rm_fortune matches 10.. run return run tellraw @s {"text": "Fortune est déjà au maximum.", "color": "red"}
scoreboard players add @s rm_fortune 1
scoreboard players remove @s rm_pts 1
function royaumes:rpg/appliquer/fortune
playsound minecraft:block.enchantment_table.use player @s ~ ~ ~ 1 1.2
tellraw @s [{"text": "✦ Fortune → rang ", "color": "gold"}, {"score": {"name": "@s", "objective": "rm_fortune"}, "color": "gold"}]
