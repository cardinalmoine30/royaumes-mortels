# Royaumes Mortels — initialisation
scoreboard objectives add rm_faction dummy
scoreboard objectives add rm_choix trigger
scoreboard objectives add rm_codex trigger
scoreboard objectives add rm_menu dummy
scoreboard objectives add rm_cd dummy
scoreboard objectives add rm_biome dummy
scoreboard objectives add rm_bnow dummy
scoreboard objectives add rm_tmp dummy
scoreboard objectives add rm_const dummy
scoreboard objectives add rm_pierre minecraft.used:minecraft.carrot_on_a_stick
scoreboard objectives add rm_quitte minecraft.custom:minecraft.leave_game
scoreboard players set #24000 rm_const 24000
scoreboard players set #5 rm_const 5
team add rm_ordre {"text": "Ordre", "color": "gold"}
team modify rm_ordre color gold
team modify rm_ordre prefix {"text": "[Ordre] ", "color": "gold"}
team modify rm_ordre friendlyFire false
team modify rm_ordre seeFriendlyInvisibles true
team add rm_chaos {"text": "Chaos", "color": "dark_red"}
team modify rm_chaos color dark_red
team modify rm_chaos prefix {"text": "[Chaos] ", "color": "dark_red"}
team modify rm_chaos friendlyFire false
team modify rm_chaos seeFriendlyInvisibles true
team add rm_mort {"text": "Mort", "color": "dark_purple"}
team modify rm_mort color dark_purple
team modify rm_mort prefix {"text": "[Mort] ", "color": "dark_purple"}
team modify rm_mort friendlyFire false
team modify rm_mort seeFriendlyInvisibles true
team add rm_destruction {"text": "Destruction", "color": "dark_green"}
team modify rm_destruction color dark_green
team modify rm_destruction prefix {"text": "[Destruction] ", "color": "dark_green"}
team modify rm_destruction friendlyFire false
team modify rm_destruction seeFriendlyInvisibles true
schedule function royaumes:boucle_seconde 20t replace
tellraw @a [{"text": "[Royaumes Mortels] ", "color": "gold"}, {"text": "Datapack chargé. Pour Sigmar !", "color": "yellow"}]
function royaumes:rpg/load
