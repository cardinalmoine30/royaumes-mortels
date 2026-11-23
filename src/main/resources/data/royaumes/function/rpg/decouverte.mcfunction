$scoreboard players set @s rm_bd$(i) 1
tellraw @s [{"text": "✧ Nouvelle région découverte ! ", "color": "aqua"}, {"text": "+30 Gloire", "color": "gold"}]
scoreboard players set #gain rm_tmp 30
function royaumes:rpg/ajouter
