title @a[distance=..40] actionbar [{"text": "Rotigus : ", "color": "dark_green"}, {"text": "Déluge de Nurgle", "color": "white", "bold": true}]
effect give @a[distance=..12,gamemode=!spectator,gamemode=!creative] minecraft:poison 10 1
effect give @a[distance=..12,gamemode=!spectator,gamemode=!creative] minecraft:slowness 6 1
effect give @a[distance=..12,gamemode=!spectator,gamemode=!creative] minecraft:hunger 10 2
particle minecraft:falling_water ~ ~4 ~ 6 1 6 0 400
playsound minecraft:weather.rain hostile @a[distance=..40] ~ ~ ~ 2 0.5
