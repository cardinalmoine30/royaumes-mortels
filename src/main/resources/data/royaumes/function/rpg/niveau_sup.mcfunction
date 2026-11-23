scoreboard players operation @s rm_gloire -= @s rm_besoin
scoreboard players add @s rm_niveau 1
scoreboard players add @s rm_pts 1
title @s times 5 40 15
title @s title [{"text": "NIVEAU ", "color": "gold", "bold": true}, {"score": {"name": "@s", "objective": "rm_niveau"}, "color": "yellow", "bold": true}]
title @s subtitle {"text": "+1 point de compétence", "color": "green"}
playsound minecraft:entity.player.levelup player @s ~ ~ ~ 1 0.8
playsound minecraft:ui.toast.challenge_complete player @s ~ ~ ~ 0.6 1.2
execute at @s run particle minecraft:totem_of_undying ~ ~1 ~ 0.5 1 0.5 0.4 60
tellraw @s [{"text": "★ Niveau ", "color": "gold"}, {"score": {"name": "@s", "objective": "rm_niveau"}, "color": "yellow"}, {"text": " atteint ! ", "color": "gold"}, {"text": "[Dépenser mes points]", "color": "green", "underlined": true, "click_event": {"action": "run_command", "command": "/trigger rm_rpg"}}]
function royaumes:rpg/verifier
