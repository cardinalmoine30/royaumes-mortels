# -*- coding: utf-8 -*-
import sys, os
from rendu import lire_nbt, rendre_blocs
B = "out/RoyaumesMortels/data/royaumes/structure/"
NOMS = {
 "forteresse_stormcast": "Forteresse Stormcast (pic d'Azyr)", "temple_seraphon": "Temple-cité Seraphon",
 "camp_orruk": "Forteresse de ferraille Ironjawz", "antre_gitz": "Forteresse de la Mauvaise Lune (Gitz)",
 "bosquet_sylvaneth": "Bosquet Sylvaneth et arbres de Wyldwood", "magmahold": "Magmahold en ruine (volcans d'Aqshy)",
 "port_kharadron": "Port d'Aether Kharadron (tyrolienne)", "sanctuaire_lumineth": "Sanctuaire Lumineth sur île flottante",
 "temple_khaine": "Temple de Khaine", "ruines_idoneth": "Temple antique Idoneth (vue sans l'eau)",
 "ziggurat_hashut": "Ziggurat infernale de Hashut", "repaire_skavenblight": "Repaire de Skavenblight",
 "ossuaire_ossiarch": "Ossuaire des Âmes Ossiarch", "jardin_rotigus": "Jardin putride de Rotigus",
 "repaire_skaven": "Clocher Hurlant Skaven", "cimetiere_nighthaunt": "Cimetière Nighthaunt", "cite_sigmar": "Cité libre de Sigmar",
 "chateau_soulblight": "Château Soulblight", "citadelle_chaos": "Citadelle du Chaos", "necropole_nagash": "Nécropole de Nagash",
 "trone_archaon": "Trône d'Archaon", "arene_gordrakk": "Arène de Gordrakk", "autel_skarbrand": "Autel de Skarbrand",
 "portail": "Portail de Royaume (anneau)", "fort_kruleboyz": "Fort des Kruleboyz", "campement_ogor": "Campement Ogor",
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
