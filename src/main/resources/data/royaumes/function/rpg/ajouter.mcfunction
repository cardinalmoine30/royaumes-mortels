execute if score @s rm_niveau matches 61.. run return 0
scoreboard players operation @s rm_gloire += #gain rm_tmp
function royaumes:rpg/verifier
title @s actionbar [{"text": "+", "color": "gold"}, {"score": {"name": "#gain", "objective": "rm_tmp"}, "color": "gold"}, {"text": " Gloire   ", "color": "gold"}, {"text": "Niv. ", "color": "gray"}, {"score": {"name": "@s", "objective": "rm_niveau"}, "color": "yellow"}, {"text": "  (", "color": "gray"}, {"score": {"name": "@s", "objective": "rm_gloire"}, "color": "gray"}, {"text": "/", "color": "gray"}, {"score": {"name": "@s", "objective": "rm_besoin"}, "color": "gray"}, {"text": ")", "color": "gray"}]
