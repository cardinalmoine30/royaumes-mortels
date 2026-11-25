# -*- coding: utf-8 -*-
import sys, os
from rendu import lire_nbt, rendre_blocs
B = "out/RoyaumesMortels/data/royaumes/structure/"
NOMS = {
 "forteresse_stormcast": "Forteresse Foudroyés (pic d'Célestis)", "temple_seraphon": "Temple-cité Astrosauriens",
 "camp_orruk": "Forteresse de ferraille Mâchefers", "antre_gitz": "Forteresse de la Mauvaise Lune (Gobelins)",
 "bosquet_sylvaneth": "Bosquet Sylvains et arbres de Bois-Sauvage", "magmahold": "Magmahold en ruine (volcans d'Pyréa)",
 "port_kharadron": "Port d'Éther Nuées (tyrolienne)", "sanctuaire_lumineth": "Sanctuaire de Lumière sur île flottante",
 "temple_khaine": "Temple de Morvaine", "ruines_idoneth": "Temple antique Abyssal (vue sans l'eau)",
 "ziggurat_hashut": "Ziggurat infernale de Ashkar", "repaire_skavenblight": "Repaire de Skavenblight",
 "ossuaire_ossiarch": "Ossuaire des Âmes Faucheurs d'Os", "jardin_rotigus": "Jardin putride Putrefax",
 "repaire_skaven": "Clocher Hurlant Hommes-Rats", "cimetiere_nighthaunt": "Cimetière Hantise Nocturne", "cite_sigmar": "Cité libre de Aurion",
 "chateau_soulblight": "Château Sanguinaire", "citadelle_chaos": "Citadelle du Chaos", "necropole_nagash": "Nécropole de Necrath",
 "trone_archaon": "Trône d'Varkhan", "arene_gordrakk": "Arène de Krognak", "autel_skarbrand": "Autel de Brakhar",
 "portail": "Portail de Royaume (anneau)", "fort_kruleboyz": "Fort des Cruelgars", "campement_ogor": "Campement Ogre",
}
cibles = sys.argv[1:] or list(NOMS)
for n in cibles:
    blocs, t = lire_nbt(B + n + ".nbt")
    if n == "ruines_idoneth":
        blocs = {k: v for k, v in blocs.items() if not v.startswith("minecraft:water")}
    s = 6 if max(t) <= 45 else 5
    import rendu
    rendu.TINT_FEUILLE = (200, 100, 42) if n == "bosquet_sylvaneth" else (90, 160, 60)
    rendu.faces.cache_clear(); rendu._cache.clear()
    im = rendre_blocs(blocs, t, s, titre=NOMS[n])
    im.convert("RGB").save(f"out/apercus/{n}.png")
    print(n, im.size)
