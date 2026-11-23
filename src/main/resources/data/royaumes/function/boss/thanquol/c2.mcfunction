title @a[distance=..40] actionbar [{"text": "Thanquol & Boneripper : ", "color": "green"}, {"text": "Nuage de Gaz Empoisonné", "color": "white", "bold": true}]
effect give @a[distance=..12,gamemode=!spectator,gamemode=!creative] minecraft:poison 8 1
effect give @a[distance=..12,gamemode=!spectator,gamemode=!creative] minecraft:nausea 8 0
particle minecraft:item_slime ~ ~1 ~ 5 1 5 0 200
playsound minecraft:entity.puffer_fish.blow_up hostile @a[distance=..40] ~ ~ ~ 2 0.5
