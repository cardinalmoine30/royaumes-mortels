$scoreboard players operation #n rm_tmp = @s $(obj)
$scoreboard players set @s $(obj) 0
$scoreboard players set #v rm_tmp $(val)
scoreboard players operation #n rm_tmp *= #v rm_tmp
scoreboard players operation #gain rm_tmp = #n rm_tmp
function royaumes:rpg/ajouter
