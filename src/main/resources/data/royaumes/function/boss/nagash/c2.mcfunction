title @a[distance=..40] actionbar [{"text": "Necrath : ", "color": "dark_purple"}, {"text": "Main de Necrath", "color": "white", "bold": true}]
effect give @a[distance=..12,gamemode=!spectator,gamemode=!creative] minecraft:wither 6 1
effect give @a[distance=..12,gamemode=!spectator,gamemode=!creative] minecraft:darkness 6 0
execute as @a[distance=..12,gamemode=!spectator,gamemode=!creative] run damage @s 6 minecraft:magic
effect give @s minecraft:instant_damage 1 1 true
particle minecraft:sculk_soul ~ ~2 ~ 6 2 6 0.05 200
playsound minecraft:entity.wither.shoot hostile @a[distance=..40] ~ ~ ~ 2 0.5
