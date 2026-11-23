execute unless score @s rm_pts matches 1.. run return run tellraw @s {"text": "Aucun point de compétence disponible.", "color": "red"}
execute if score @s rm_agilite matches 10.. run return run tellraw @s {"text": "Agilité est déjà au maximum.", "color": "red"}
scoreboard players add @s rm_agilite 1
scoreboard players remove @s rm_pts 1
function royaumes:rpg/appliquer/agilite
playsound minecraft:block.enchantment_table.use player @s ~ ~ ~ 1 1.2
tellraw @s [{"text": "✦ Agilité → rang ", "color": "aqua"}, {"score": {"name": "@s", "objective": "rm_agilite"}, "color": "aqua"}]
