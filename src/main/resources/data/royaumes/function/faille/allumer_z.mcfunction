fill ~ ~ ~ ~0 ~2 ~1 minecraft:nether_portal[axis=z]
summon minecraft:marker ~0.5 ~1.5 ~1 {Tags:["rm_faille","rm_axe_z"]}
particle minecraft:reverse_portal ~0.5 ~1.5 ~1 0.5 1 0.5 0.2 200
playsound minecraft:block.end_portal.spawn block @a[distance=..32] ~ ~ ~ 0.8 1.3
tellraw @a[distance=..16] [{"text": "✦ Un Portail de Royaume s’ouvre… ", "color": "light_purple"}, {"text": "Où mènera-t-il ?", "color": "gray", "italic": true}]
scoreboard players set #gain rm_tmp 20
execute as @p[distance=..8] run function royaumes:rpg/ajouter
kill @s
