# -*- coding: utf-8 -*-
"""Capacités de faction (touche R) : une par faction, construite sur quelques archétypes codés en Java
(fr/royaumes/magie/Capacites.java). Effets : "effet:amplificateur:durée_en_ticks", séparés par des virgules."""

# faction : (nom, description, archétype, dégâts, rayon, recharge s, effets sur soi, effets sur ennemis, particule, invocation)
CAPACITES = {
    "stormcast": ("Frappe de foudre", "Tu frappes comme la foudre : téléporté sur la cible, tu foudroies tout autour.", "ECLAIR", 10, 3.5, 45, "resistance:1:100", "", "electric_spark", ""),
    "cites": ("Salve de mousquets", "Une salve de neuf traits part droit devant.", "SALVE_FLECHES", 7, 0, 25, "", "", "crit", ""),
    "fyreslayers": ("Rune de fureur", "Les runes d'ur-or s'embrasent : force, célérité, peau ignifuge.", "AURA", 0, 0, 60, "strength:1:400,haste:1:400,fire_resistance:0:400", "", "flame", ""),
    "kharadron": ("Saut d'aethergold", "Tes endrins te propulsent dans les airs, puis tu planes.", "ENVOL", 0, 0, 40, "slow_falling:0:300", "", "cloud", ""),
    "khaine": ("Danse de mort", "Tu tournoies, lames au clair, et blesses tout ce qui t'entoure.", "FRAPPE_SOI", 8, 4, 30, "speed:2:200,strength:0:200", "", "sweep_attack", ""),
    "idoneth": ("Marée spectrale", "Une marée d'âmes noie tes ennemis dans l'obscurité.", "MALEDICTION", 4, 8, 45, "water_breathing:0:600", "slowness:2:120,blindness:0:80", "bubble_pop", ""),
    "lumineth": ("Lumière de Lumarion", "Un éclat de lumière pure brûle et aveugle les ennemis proches.", "FRAPPE_SOI", 8, 7, 45, "", "glowing:0:200,blindness:0:60", "end_rod", ""),
    "seraphon": ("Comète céleste", "Une comète tombe là où tu regardes.", "COMETE", 14, 5, 60, "", "", "end_rod", ""),
    "sylvaneth": ("Bois enchevêtré", "La forêt te soigne, toi et tes alliés, et entrave tes ennemis.", "SOIN", 10, 6, 50, "regeneration:1:120", "slowness:3:100", "happy_villager", ""),
    "esclaves": ("Œil des Dieux", "Les Puissances te regardent : force et résistance.", "AURA", 0, 0, 60, "strength:1:400,resistance:0:400", "", "smoke", ""),
    "khorne": ("Soif de sang", "Le Dieu du Sang exige des crânes : tu frappes plus fort et plus vite.", "AURA", 0, 0, 60, "strength:2:300,speed:0:300", "", "crimson_spore", ""),
    "tzeentch": ("Feu changeant", "Cinq boules de feu changeant jaillissent de tes mains.", "SALVE_FEU", 0, 0, 30, "", "", "witch", ""),
    "slaanesh": ("Extase", "Tes ennemis chancellent, ivres de sensations ; toi, tu danses.", "MALEDICTION", 3, 8, 45, "speed:1:200", "nausea:0:160,weakness:1:160", "heart", ""),
    "nurgle": ("Miasme", "Un nuage de peste empoisonne et affame les ennemis proches.", "MALEDICTION", 2, 7, 45, "", "poison:1:160,hunger:1:200", "sneeze", ""),
    "skaven": ("Fuite par la Warp", "Tu traverses la Warp vingt blocs plus loin, invisible un instant.", "TELEPORT", 0, 20, 30, "invisibility:0:100,speed:1:100", "", "portal", ""),
    "hashut": ("Souffle de l'Ash", "Un cône de feu et de cendres jaillit devant toi.", "CONE", 8, 9, 35, "fire_resistance:0:200", "", "flame", ""),
    "nighthaunt": ("Voile spectral", "Tu deviens spectre : invisible, rapide et insaisissable.", "AURA", 0, 0, 50, "invisibility:0:300,speed:1:300,resistance:1:300", "", "soul", ""),
    "soulblight": ("Soif du vampire", "Tu draines la vie de tes ennemis pour la faire tienne.", "DRAIN", 5, 6, 45, "", "", "damage_indicator", ""),
    "ossiarch": ("Mur d'os", "Ton armure d'os se referme : résistance et absorption.", "AURA", 0, 0, 60, "resistance:2:200,absorption:2:400", "", "white_ash", ""),
    "fec": ("Festin", "Le banquet des Goules te rassasie et referme tes plaies.", "SOIN", 12, 0, 50, "saturation:0:20,regeneration:0:200", "", "heart", ""),
    "ironjawz": ("Graaah !", "Deux brutes orcs répondent à ton cri de guerre.", "INVOCATION", 0, 0, 90, "strength:0:300", "", "angry_villager", "brute"),
    "kruleboyz": ("Venin des marais", "Une nappe de venin empoisonne et ralentit tes ennemis.", "MALEDICTION", 3, 7, 40, "", "poison:1:140,slowness:1:140", "item_slime", ""),
    "gitz": ("Mauvaise Lune", "Sous la Mauvaise Lune, deux squigs bondissent à tes côtés.", "INVOCATION", 0, 0, 90, "", "", "squid_ink", "squig_hopper"),
    "ogors": ("Charge de bedaine", "Tu charges droit devant et renverses tout sur ton passage.", "CHARGE", 9, 3, 30, "resistance:0:60", "", "cloud", ""),
    "behemat": ("Piétinement", "Tu frappes le sol : les ennemis proches sont blessés et projetés.", "FRAPPE_SOI", 10, 6, 40, "", "slowness:1:60", "explosion", ""),
}


def java(ids, jstr):
    """Lignes Java pour ContenuGenere (index = numéro de faction, 0 vide)."""
    lignes = []
    champs = [("CAP_NOMS", 0, jstr), ("CAP_DESC", 1, jstr), ("CAP_TYPES", 2, jstr), ("CAP_EFFETS_SOI", 6, jstr),
              ("CAP_EFFETS_ENNEMIS", 7, jstr), ("CAP_PARTICULES", 8, jstr), ("CAP_INVOCATIONS", 9, jstr)]
    for nom, i, f in champs:
        lignes.append("    public static final String[] %s = {\"\", %s};" % (nom, ", ".join(f(CAPACITES[x][i]) for x in ids)))
    lignes.append("    public static final float[] CAP_DEGATS = {0F, %s};" % ", ".join("%.1fF" % CAPACITES[x][3] for x in ids))
    lignes.append("    public static final float[] CAP_RAYONS = {0F, %s};" % ", ".join("%.1fF" % CAPACITES[x][4] for x in ids))
    lignes.append("    public static final int[] CAP_RECHARGES = {0, %s};" % ", ".join(str(CAPACITES[x][5]) for x in ids))
    return lignes
