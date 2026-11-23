title @a[distance=..40] actionbar [{"text": "Archaon : ", "color": "dark_red"}, {"text": "Foudre des Huit-Points", "color": "white", "bold": true}]
execute at @a[distance=..20,gamemode=!spectator,gamemode=!creative,limit=3,sort=random] run summon minecraft:lightning_bolt ~ ~ ~
playsound minecraft:entity.lightning_bolt.thunder hostile @a[distance=..60] ~ ~ ~ 2 0.7
