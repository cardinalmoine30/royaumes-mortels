tp @e[type=#royaumes:montures,tag=rm_trouvee,limit=1,sort=nearest] @s
ride @s mount @e[type=#royaumes:montures,tag=rm_trouvee,limit=1,sort=nearest]
tag @e[type=#royaumes:montures,tag=rm_trouvee] remove rm_trouvee
particle minecraft:cloud ~ ~0.5 ~ 0.8 0.3 0.8 0.02 20
title @s actionbar {"text": "Ta monture accourt à ton appel.", "color": "gold"}
