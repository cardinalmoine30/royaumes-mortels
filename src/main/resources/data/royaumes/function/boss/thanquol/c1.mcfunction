title @a[distance=..40] actionbar [{"text": "Skrivel & Broie-Os : ", "color": "green"}, {"text": "Fangefoudre", "color": "white", "bold": true}]
execute at @a[distance=..20,gamemode=!spectator,gamemode=!creative,limit=2,sort=random] run summon minecraft:lightning_bolt ~ ~ ~
effect give @a[distance=..12,gamemode=!spectator,gamemode=!creative] minecraft:wither 5 1
particle minecraft:happy_villager ~ ~2 ~ 5 2 5 0 200
