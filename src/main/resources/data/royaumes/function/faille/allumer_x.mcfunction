fill ~ ~ ~ ~1 ~2 ~0 minecraft:nether_portal[axis=x]
summon minecraft:marker ~1 ~1.5 ~0.5 {Tags:["rm_faille","rm_axe_x"]}
particle minecraft:reverse_portal ~1 ~1.5 ~0.5 0.5 1 0.5 0.2 200
playsound minecraft:block.end_portal.spawn block @a[distance=..32] ~ ~ ~ 0.8 1.3
tellraw @a[distance=..16] [{"text": "✦ Un Portail de Royaume s’ouvre… ", "color": "light_purple"}, {"text": "Où mènera-t-il ?", "color": "gray", "italic": true}]
scoreboard players set #gain rm_tmp 20
execute as @p[distance=..8] run function royaumes:rpg/ajouter
kill @s
