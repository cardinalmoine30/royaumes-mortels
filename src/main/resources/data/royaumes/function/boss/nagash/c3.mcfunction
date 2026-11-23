title @a[distance=..40] actionbar [{"text": "Nagash : ", "color": "dark_purple"}, {"text": "Pas de l'Ombre", "color": "white", "bold": true}]
execute as @p[distance=..28,gamemode=!spectator,gamemode=!creative] at @s run tp @e[tag=rm_boss_nagash,limit=1,sort=nearest] ^ ^ ^-3
particle minecraft:reverse_portal ~ ~2 ~ 1 2 1 0.2 150
playsound minecraft:entity.enderman.teleport hostile @a[distance=..40] ~ ~ ~ 2 0.5
