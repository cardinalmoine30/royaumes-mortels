scoreboard objectives add rm_gloire dummy
scoreboard objectives add rm_besoin dummy
scoreboard objectives add rm_niveau dummy {"text": "Niv.", "color": "gold"}
scoreboard objectives add rm_pts dummy
scoreboard objectives add rm_comp trigger
scoreboard objectives add rm_rpg trigger
scoreboard objectives add rm_forge trigger
scoreboard objectives add rm_bt dummy
scoreboard objectives setdisplay list rm_niveau
scoreboard objectives setdisplay below_name rm_niveau
scoreboard players set #20 rm_const 20
scoreboard players set #40 rm_const 40
team add rm_boss {"text": "Boss", "color": "red"}
team modify rm_boss color red
team modify rm_boss friendlyFire false
scoreboard objectives add rm_vigueur dummy
scoreboard objectives add rm_force dummy
scoreboard objectives add rm_agilite dummy
scoreboard objectives add rm_mineur dummy
scoreboard objectives add rm_endurance dummy
scoreboard objectives add rm_fortune dummy
scoreboard objectives add rm_m0 minecraft.mined:minecraft.coal_ore
scoreboard objectives add rm_m1 minecraft.mined:minecraft.deepslate_coal_ore
scoreboard objectives add rm_m2 minecraft.mined:minecraft.copper_ore
scoreboard objectives add rm_m3 minecraft.mined:minecraft.deepslate_copper_ore
scoreboard objectives add rm_m4 minecraft.mined:minecraft.iron_ore
scoreboard objectives add rm_m5 minecraft.mined:minecraft.deepslate_iron_ore
scoreboard objectives add rm_m6 minecraft.mined:minecraft.gold_ore
scoreboard objectives add rm_m7 minecraft.mined:minecraft.deepslate_gold_ore
scoreboard objectives add rm_m8 minecraft.mined:minecraft.redstone_ore
scoreboard objectives add rm_m9 minecraft.mined:minecraft.deepslate_redstone_ore
scoreboard objectives add rm_m10 minecraft.mined:minecraft.lapis_ore
scoreboard objectives add rm_m11 minecraft.mined:minecraft.deepslate_lapis_ore
scoreboard objectives add rm_m12 minecraft.mined:minecraft.diamond_ore
scoreboard objectives add rm_m13 minecraft.mined:minecraft.deepslate_diamond_ore
scoreboard objectives add rm_m14 minecraft.mined:minecraft.emerald_ore
scoreboard objectives add rm_m15 minecraft.mined:minecraft.deepslate_emerald_ore
scoreboard objectives add rm_m16 minecraft.mined:minecraft.nether_gold_ore
scoreboard objectives add rm_m17 minecraft.mined:minecraft.nether_quartz_ore
scoreboard objectives add rm_m18 minecraft.mined:minecraft.ancient_debris
scoreboard objectives add rm_m19 minecraft.mined:minecraft.verdant_froglight
scoreboard objectives add rm_m20 minecraft.mined:minecraft.raw_gold_block
scoreboard objectives add rm_m21 minecraft.mined:minecraft.crying_obsidian
scoreboard objectives add rm_m22 minecraft.mined:minecraft.amethyst_cluster
scoreboard objectives add rm_k_mob minecraft.custom:minecraft.mob_kills
scoreboard objectives add rm_k_or teamkill.gold
scoreboard objectives add rm_k_cr teamkill.dark_red
scoreboard objectives add rm_k_dp teamkill.dark_purple
scoreboard objectives add rm_k_dg teamkill.dark_green
scoreboard objectives add rm_k_boss teamkill.red
scoreboard objectives add rm_bd1 dummy
scoreboard objectives add rm_bd2 dummy
scoreboard objectives add rm_bd3 dummy
scoreboard objectives add rm_bd4 dummy
scoreboard objectives add rm_bd5 dummy
scoreboard objectives add rm_bd6 dummy
scoreboard objectives add rm_bd7 dummy
scoreboard objectives add rm_bd8 dummy
scoreboard objectives add rm_bd9 dummy
scoreboard objectives add rm_bd10 dummy
scoreboard objectives add rm_bd11 dummy
scoreboard objectives add rm_bd12 dummy
scoreboard objectives add rm_bd13 dummy
scoreboard objectives add rm_bd14 dummy
scoreboard objectives add rm_bd15 dummy
scoreboard objectives add rm_bd16 dummy
scoreboard objectives add rm_bd17 dummy
bossbar add royaumes:nagash {"text": "Nagash, Dieu de la Mort", "color": "dark_purple", "bold": true}
bossbar set royaumes:nagash color purple
bossbar set royaumes:nagash style notched_10
bossbar set royaumes:nagash max 900
bossbar add royaumes:archaon {"text": "Archaon, l'Élu Éternel", "color": "dark_red", "bold": true}
bossbar set royaumes:archaon color red
bossbar set royaumes:archaon style notched_10
bossbar set royaumes:archaon max 1000
bossbar add royaumes:gordrakk {"text": "Gordrakk, le Poing de Gork", "color": "gold", "bold": true}
bossbar set royaumes:gordrakk color yellow
bossbar set royaumes:gordrakk style notched_10
bossbar set royaumes:gordrakk max 800
bossbar add royaumes:skarbrand {"text": "Skarbrand, l'Exilé", "color": "red", "bold": true}
bossbar set royaumes:skarbrand color red
bossbar set royaumes:skarbrand style notched_10
bossbar set royaumes:skarbrand max 850
bossbar add royaumes:thanquol {"text": "Thanquol & Boneripper", "color": "green", "bold": true}
bossbar set royaumes:thanquol color green
bossbar set royaumes:thanquol style notched_10
bossbar set royaumes:thanquol max 750
bossbar add royaumes:rotigus {"text": "Rotigus, le Pluvieux", "color": "dark_green", "bold": true}
bossbar set royaumes:rotigus color green
bossbar set royaumes:rotigus style notched_10
bossbar set royaumes:rotigus max 950
schedule function royaumes:forge/boucle 10t replace
scoreboard objectives add rm_tyt dummy
