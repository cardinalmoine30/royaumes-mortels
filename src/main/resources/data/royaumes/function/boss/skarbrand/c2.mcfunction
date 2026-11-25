title @a[distance=..40] actionbar [{"text": "Brakhar : ", "color": "red"}, {"text": "Brasier de Sangrath", "color": "white", "bold": true}]
execute as @a[distance=..12,gamemode=!spectator,gamemode=!creative] run damage @s 7 minecraft:in_fire
particle minecraft:flame ~ ~1 ~ 6 1 6 0.05 300
playsound minecraft:item.firecharge.use hostile @a[distance=..40] ~ ~ ~ 2 0.6
