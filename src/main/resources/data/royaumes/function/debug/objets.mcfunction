# Pose des tonneaux remplis de tous les objets du jeu, devant toi (vers l'est)
tellraw @s {"text":"Tous les objets du jeu sont dans les tonneaux à côté de toi.","color":"gold"}
setblock ~2 ~ ~2 minecraft:barrel[facing=up]{CustomName:"Divers et sceaux de boss"} replace
loot insert ~2 ~ ~2 loot royaumes:debug/divers
summon minecraft:text_display ~2.5 ~1.3 ~2.5 {text:"Divers et sceaux de boss",billboard:"center",Tags:["rm_debug"]}
setblock ~4 ~ ~2 minecraft:barrel[facing=up]{CustomName:"Ressources"} replace
loot insert ~4 ~ ~2 loot royaumes:debug/ressources
summon minecraft:text_display ~4.5 ~1.3 ~2.5 {text:"Ressources",billboard:"center",Tags:["rm_debug"]}
setblock ~6 ~ ~2 minecraft:barrel[facing=up]{CustomName:"Trophées de boss"} replace
loot insert ~6 ~ ~2 loot royaumes:debug/trophees
summon minecraft:text_display ~6.5 ~1.3 ~2.5 {text:"Trophées de boss",billboard:"center",Tags:["rm_debug"]}
setblock ~8 ~ ~2 minecraft:barrel[facing=up]{CustomName:"Forge (1)"} replace
loot insert ~8 ~ ~2 loot royaumes:forge/amulette_ambre
loot insert ~8 ~ ~2 loot royaumes:forge/arc_hysh
loot insert ~8 ~ ~2 loot royaumes:forge/brume_ulgu
loot insert ~8 ~ ~2 loot royaumes:forge/coeur_hysh
loot insert ~8 ~ ~2 loot royaumes:forge/elixir_ghyran
loot insert ~8 ~ ~2 loot royaumes:forge/elixir_malepierre
loot insert ~8 ~ ~2 loot royaumes:forge/festin_ogor
loot insert ~8 ~ ~2 loot royaumes:forge/fusil_aether
loot insert ~8 ~ ~2 loot royaumes:forge/lumiere_hysh
loot insert ~8 ~ ~2 loot royaumes:forge/oeil_chaos
loot insert ~8 ~ ~2 loot royaumes:forge/parchemin
loot insert ~8 ~ ~2 loot royaumes:forge/pendentif_ombre
loot insert ~8 ~ ~2 loot royaumes:forge/pierre
loot insert ~8 ~ ~2 loot royaumes:forge/raffinage
loot insert ~8 ~ ~2 loot royaumes:forge/rune_sigmar
loot insert ~8 ~ ~2 loot royaumes:forge/sceau_archaon
loot insert ~8 ~ ~2 loot royaumes:forge/sceau_gordrakk
summon minecraft:text_display ~8.5 ~1.3 ~2.5 {text:"Forge (1)",billboard:"center",Tags:["rm_debug"]}
setblock ~10 ~ ~2 minecraft:barrel[facing=up]{CustomName:"Forge (2)"} replace
loot insert ~10 ~ ~2 loot royaumes:forge/sceau_nagash
loot insert ~10 ~ ~2 loot royaumes:forge/sceau_rotigus
loot insert ~10 ~ ~2 loot royaumes:forge/sceau_skarbrand
loot insert ~10 ~ ~2 loot royaumes:forge/sceau_thanquol
loot insert ~10 ~ ~2 loot royaumes:forge/sigmarite
loot insert ~10 ~ ~2 loot royaumes:forge/talisman_grimnir
loot insert ~10 ~ ~2 loot royaumes:forge/tonique_aqshy
summon minecraft:text_display ~10.5 ~1.3 ~2.5 {text:"Forge (2)",billboard:"center",Tags:["rm_debug"]}
setblock ~12 ~ ~2 minecraft:barrel[facing=up]{CustomName:"Œufs des mobs (1)"} replace
setblock ~14 ~ ~2 minecraft:barrel[facing=up]{CustomName:"Œufs des mobs (2)"} replace
setblock ~16 ~ ~2 minecraft:barrel[facing=up]{CustomName:"Œufs des mobs (3)"} replace
setblock ~18 ~ ~2 minecraft:barrel[facing=up]{CustomName:"Œufs des mobs (4)"} replace
setblock ~20 ~ ~2 minecraft:barrel[facing=up]{CustomName:"Œufs des mobs (5)"} replace
setblock ~22 ~ ~2 minecraft:barrel[facing=up]{CustomName:"Œufs des mobs (6)"} replace
