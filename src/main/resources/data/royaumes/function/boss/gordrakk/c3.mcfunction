title @a[distance=..40] actionbar [{"text": "Gordrakk : ", "color": "gold"}, {"text": "Charge du Maw-Krusha", "color": "white", "bold": true}]
execute as @p[distance=..28,gamemode=!spectator,gamemode=!creative] at @s run tp @e[tag=rm_boss_gordrakk,limit=1,sort=nearest] ~ ~ ~
execute as @a[distance=..4] run damage @s 6 minecraft:mob_attack
particle minecraft:cloud ~ ~ ~ 2 0.5 2 0.1 60
