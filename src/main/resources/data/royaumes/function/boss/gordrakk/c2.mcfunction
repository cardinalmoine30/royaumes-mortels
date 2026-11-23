title @a[distance=..40] actionbar [{"text": "Gordrakk : ", "color": "gold"}, {"text": "Coup de Poing de Gork", "color": "white", "bold": true}]
effect give @a[distance=..7,gamemode=!spectator,gamemode=!creative] minecraft:levitation 1 6
execute as @a[distance=..7,gamemode=!spectator,gamemode=!creative] run damage @s 8 minecraft:mob_attack
particle minecraft:explosion ~ ~ ~ 3 0.2 3 0 12
playsound minecraft:entity.generic.explode hostile @a[distance=..40] ~ ~ ~ 2 0.7
