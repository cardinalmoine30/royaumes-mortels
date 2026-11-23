# Réinitialise la faction du joueur (à lancer : /execute as <joueur> run function royaumes:admin/reinitialiser)
function royaumes:factions/retirer_dons
scoreboard players reset @s rm_faction
team leave @s
scoreboard players set @s rm_menu 0
tellraw @s {"text": "Ta faction a été réinitialisée.", "color": "yellow"}
function royaumes:rpg/rang/vigueur/0
function royaumes:rpg/rang/force/0
function royaumes:rpg/rang/agilite/0
function royaumes:rpg/rang/mineur/0
function royaumes:rpg/rang/endurance/0
function royaumes:rpg/rang/fortune/0
function royaumes:rpg/init
