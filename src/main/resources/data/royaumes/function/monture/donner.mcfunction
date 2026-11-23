give @s minecraft:carrot_on_a_stick[minecraft:custom_data={royaumes:"monture"},minecraft:item_model="minecraft:goat_horn",minecraft:unbreakable={},minecraft:rarity="rare",minecraft:custom_name={"text":"Corne d'appel","color":"gold","italic":false},minecraft:lore=[{"text":"Clic droit : appelle la monture de ta faction.","color":"gray","italic":true}]]
tag @s add rm_corne
tellraw @s [{"text": "✦ Tu reçois une ", "color": "gold"}, {"text": "Corne d'appel", "color": "yellow"}, {"text": " : clic droit pour appeler la monture de ta faction.", "color": "gold"}]
