execute align xyz run fill ~-1 ~-1 ~3 ~2 ~3 ~3 minecraft:amethyst_block
execute align xyz run fill ~ ~ ~3 ~1 ~2 ~3 minecraft:air
execute align xyz run fill ~-1 ~ ~1 ~2 ~2 ~2 minecraft:air
execute align xyz run fill ~ ~ ~3 ~1 ~2 ~3 minecraft:nether_portal[axis=x]
execute align xyz run summon minecraft:marker ~1 ~1.5 ~3.5 {Tags:["rm_faille","rm_axe_x"]}
tellraw @s {"text": "Un portail de retour s’est formé devant vous.", "color": "light_purple"}
