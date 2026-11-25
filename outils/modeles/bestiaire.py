# -*- coding: utf-8 -*-
"""Bestiaire complet des Royaumes Mortels : unités et créatures de chaque faction.
Chaque entrée : apparence (gabarit + options), stats, capacité au contact, mode combat,
capacité spéciale, butin. Utilisé par factions.py pour tout générer."""
from factions import pal

# ------------------------------------------------------------------ factions : alliance, ressource, biomes
FAC = {
    "stormcast": ("ordre", "sigmarite", ["azyr_cimes", "azyr_vallees"]),
    "cites": ("ordre", "eclat", ["azyr_vallees", "ghyran_jade"]),
    "khaine": ("ordre", "ombre", ["ulgu_brumes"]),
    "fyreslayers": ("ordre", "ur_or", ["aqshy_volcans", "aqshy_cendres"]),
    "idoneth": ("ordre", "ombre", ["ulgu_mer", "ulgu_brumes"]),
    "kharadron": ("ordre", "aether_or", ["chamon_collines", "chamon_desert"]),
    "lumineth": ("ordre", "cristal", ["hysh_iles", "hysh_plateaux"]),
    "seraphon": ("ordre", "ambre", ["ghur_jungle"]),
    "sylvaneth": ("ordre", "graine", ["ghyran_wyldwood", "ghyran_jade"]),
    "esclaves": ("chaos", "chaos", ["chaos_desolation"]),
    "tzeentch": ("chaos", "chaos", ["chaos_desolation"]),
    "khorne": ("chaos", "braise", ["chaos_desolation", "aqshy_cendres"]),
    "slaanesh": ("chaos", "chaos", ["chaos_desolation", "ulgu_brumes"]),
    "nurgle": ("chaos", "graine", ["ghyran_marais", "chaos_desolation"]),
    "skaven": ("chaos", "malepierre", ["terres_rongees"]),
    "hashut": ("chaos", "braise", ["aqshy_cendres", "aqshy_volcans"]),
    "fec": ("mort", "ame", ["shyish_terres", "ulgu_marais_lune"]),
    "nighthaunt": ("mort", "ame", ["shyish_terres"]),
    "ossiarch": ("mort", "ame", ["shyish_sables"]),
    "soulblight": ("mort", "ame", ["shyish_terres"]),
    "gitz": ("destruction", "ombre", ["ulgu_marais_lune"]),
    "ogors": ("destruction", "ambre", ["ghur_savane", "ghur_terres"]),
    "orruks": ("destruction", "ferraille", ["ghur_terres"]),
    "behemat": ("destruction", "ambre", ["ghur_terres", "ghur_savane"]),
}

# ------------------------------------------------------------------ palettes
OR, BLEU = (204, 158, 52), (40, 66, 150)
P = {
    "sc": pal(OR, (60, 90, 170), BLEU, OR, (120, 220, 255), metal=(120, 130, 140), manche=(130, 40, 40), bouclier=BLEU, membrane=(230, 235, 245)),
    "cites": pal((152, 154, 162), (200, 190, 160), (184, 64, 40), (215, 175, 140), (250, 220, 120), bouclier=(168, 40, 32), plume=(184, 64, 40), embleme=(232, 214, 172)),
    "griffon": pal((150, 120, 80), (240, 240, 235), (120, 90, 60), (170, 130, 80), (250, 220, 120), corne=(230, 190, 80), membrane=(235, 230, 220)),
    "dragon": pal((180, 50, 40), (230, 180, 70), (150, 40, 30), (170, 45, 35), (255, 150, 40), corne=(230, 210, 170), membrane=(130, 30, 25)),
    "khaine": pal((176, 106, 56), (200, 150, 80), (100, 36, 70), (226, 206, 206), (120, 255, 220), poils=(222, 200, 226), membrane=(48, 112, 106), cuir=(60, 30, 40), serpent=(44, 104, 98)),
    "avatar": pal((70, 70, 76), (200, 160, 60), (60, 20, 20), (80, 80, 86), (255, 110, 30)),
    "fyre": pal((214, 160, 60), (230, 186, 64), (100, 40, 26), (222, 160, 120), (255, 150, 40), poils=(246, 110, 24), cuir=(120, 56, 30)),
    "magma": pal((60, 40, 36), (230, 180, 60), (90, 40, 20), (90, 50, 40), (255, 120, 30), corne=(240, 200, 90)),
    "idoneth": pal((40, 72, 82), (160, 186, 186), (50, 90, 150), (226, 230, 234), (120, 255, 230), membrane=(232, 112, 52), poils=(226, 226, 230)),
    "abyss": pal((40, 72, 82), (160, 186, 186), (50, 90, 150), (104, 84, 116), (120, 255, 230), membrane=(232, 112, 52), ventre=(170, 150, 176)),
    "khar": pal((186, 132, 74), (214, 186, 120), (88, 40, 72), (220, 170, 140), (150, 220, 255), metal=(150, 150, 156), bois=(88, 40, 72), poils=(140, 90, 60)),
    "navire": pal((186, 132, 74), (214, 186, 120), (190, 140, 80), (186, 132, 74), (150, 220, 255), metal=(170, 130, 80), bois=(88, 40, 72)),
    "lum": pal((238, 238, 242), (212, 180, 92), (172, 112, 170), (240, 220, 200), (255, 250, 200), plume=(196, 120, 186)),
    "alarith": pal((180, 180, 175), (210, 180, 90), (150, 150, 145), (170, 170, 165), (255, 250, 200), corne=(230, 230, 220)),
    "sera": pal((206, 160, 54), (226, 186, 70), (180, 40, 36), (62, 168, 200), (255, 220, 90), corne=(236, 220, 170), ventre=(176, 218, 224), crete=(44, 96, 160), oeil=(250, 200, 40)),
    "sylv": pal((112, 96, 64), (120, 170, 60), (90, 80, 50), (140, 130, 90), (150, 232, 240), corne=(96, 84, 56)),
    "chaos": pal((38, 38, 44), (182, 140, 72), (150, 30, 30), (200, 170, 140), (230, 60, 40), metal=(70, 70, 76), poils=(206, 190, 160), corne=(222, 206, 170)),
    "chaos_cheval": pal((30, 30, 34), (182, 140, 72), (150, 30, 30), (36, 34, 38), (230, 60, 40), corne=(222, 206, 170), poils=(20, 20, 22)),
    "demon": pal((110, 30, 60), (200, 170, 70), (80, 20, 40), (120, 40, 70), (255, 80, 200), membrane=(70, 20, 40)),
    "rejeton": pal((150, 80, 110), (90, 60, 90), (120, 70, 100), (160, 90, 120), (255, 200, 80), membrane=(120, 60, 90)),
    "tzeentch": pal((52, 172, 192), (192, 142, 82), (226, 220, 204), (176, 126, 86), (120, 230, 255), corne=(230, 214, 170), membrane=(60, 80, 170), plume=(54, 76, 168)),
    "rose": pal((230, 120, 180), (240, 200, 90), (220, 110, 170), (235, 130, 190), (120, 230, 255)),
    "khorne": pal((130, 32, 30), (172, 122, 62), (60, 20, 18), (172, 42, 32), (255, 80, 40), metal=(70, 60, 60), corne=(40, 32, 30), membrane=(110, 20, 15)),
    "laiton": pal((180, 130, 60), (150, 30, 26), (60, 20, 18), (190, 140, 60), (255, 80, 40), corne=(60, 50, 40)),
    "slaanesh": pal((200, 160, 82), (230, 210, 140), (112, 52, 112), (206, 200, 220), (255, 120, 220), poils=(214, 150, 206), corne=(78, 44, 100)),
    "nurgle": pal((96, 104, 64), (150, 110, 60), (68, 88, 58), (176, 188, 128), (190, 230, 60), metal=(120, 84, 50), corne=(46, 70, 70), oeil=(230, 200, 40), membrane=(206, 104, 146)),
    "skaven": pal((96, 90, 86), (176, 112, 68), (150, 40, 40), (136, 108, 92), (80, 255, 60), metal=(172, 112, 70), poils=(120, 96, 82), rose=(214, 140, 140)),
    "hashut": pal((40, 40, 44), (190, 140, 60), (90, 30, 20), (90, 90, 96), (255, 110, 30), poils=(30, 30, 34)),
    "fec": pal((150, 150, 140), (120, 60, 50), (90, 70, 60), (166, 186, 150), (220, 60, 60), membrane=(70, 44, 44), corne=(210, 200, 180), poils=(30, 30, 32)),
    "nh": pal((60, 140, 130), (150, 110, 70), (176, 220, 210), (190, 228, 218), (160, 255, 230), membrane=(70, 150, 140), metal=(110, 76, 52), capuche=(78, 54, 44)),
    "ossi": pal((218, 204, 168), (44, 54, 96), (44, 54, 96), (224, 212, 184), (130, 224, 172), membrane=(200, 190, 170), corne=(224, 212, 184), manche=(150, 40, 40), bouclier=(44, 54, 96)),
    "sb": pal((150, 28, 32), (196, 152, 60), (36, 64, 58), (226, 222, 226), (255, 40, 50), membrane=(90, 60, 50), poils=(170, 30, 30)),
    "sbz": pal((150, 140, 96), (120, 150, 120), (40, 44, 40), (210, 200, 176), (90, 255, 160), membrane=(90, 100, 80), corne=(220, 215, 190)),
    "gitz": pal((40, 40, 50), (220, 210, 120), (34, 34, 46), (120, 160, 70), (230, 220, 120)),
    "squig": pal((40, 40, 50), (220, 210, 120), (34, 34, 46), (206, 44, 40), (255, 230, 90), ventre=(236, 150, 160), rose=(236, 140, 160)),
    "troll": pal((90, 110, 100), (120, 100, 70), (80, 70, 60), (82, 128, 156), (255, 220, 90), ventre=(222, 216, 190)),
    "ogor": pal((150, 150, 156), (200, 160, 60), (70, 92, 132), (218, 150, 128), (255, 200, 60), corne=(230, 220, 200), poils=(90, 70, 50)),
    "givre": pal((200, 210, 225), (90, 120, 170), (150, 160, 180), (210, 220, 230), (160, 220, 255), corne=(240, 240, 240), poils=(220, 230, 240)),
    "orruk": pal((226, 184, 34), (62, 62, 68), (90, 60, 40), (96, 140, 56), (255, 200, 40), metal=(112, 112, 118)),
    "kb": pal((66, 62, 56), (150, 40, 30), (100, 70, 50), (132, 150, 72), (200, 255, 80), metal=(90, 96, 80), bouclier=(190, 40, 30)),
    "pierre": pal((130, 125, 115), (200, 170, 60), (110, 105, 95), (130, 125, 115), (120, 255, 120)),
    "gargant": pal((120, 90, 60), (160, 120, 70), (110, 80, 50), (222, 170, 146), (255, 200, 60), poils=(190, 100, 50)),
}

TOUS = []


def M(id, nom, fac, gabarit, spec, stats, ech=1.0, cap="aucune", mode="melee", special="aucun", sbire="", butin=(),
      biomes=None, poids=None, boss=False):
    pv = stats[0]
    TOUS.append(dict(id=id, nom=nom, fac=fac, gabarit=gabarit, spec=spec, stats=stats, ech=ech, cap=cap, mode=mode,
                     special=special, sbire=sbire, butin=list(butin), biomes=FAC[fac][2] if biomes is None else biomes,
                     poids=(0 if boss else (40 if pv < 40 else 15 if pv < 90 else 4 if pv < 250 else 1)) if poids is None else poids,
                     boss=boss))


def H(corps, p, **kw):
    d = dict(corps=corps, pal=P[p])
    d.update(kw)
    return d


def B(p, **kw):
    d = dict(pal=P[p])
    d.update(kw)
    return d


OS = [("minecraft:bone", 1, 3)]
CUIR = [("minecraft:leather", 1, 2)]
FER = [("minecraft:iron_nugget", 2, 6)]
OR_ = [("minecraft:gold_nugget", 2, 6)]
VIANDE = [("minecraft:beef", 1, 3)]
ECAILLE = [("minecraft:armadillo_scute", 0, 1)]

# ==================================================================== ORDRE
# --- Éternels de l'Orage (Célestis)
M("liberator", "Libérateur", "stormcast", "h", H("massif", "sc", armure=True, face="heaume", arme="marteau", main_gauche="bouclier", epaulieres=(7, 6, 10), embleme="comete", extras=("cape", "halo")), (40, 6, 8, .27), cap="foudre", butin=FER)
M("judicator", "Justicier", "stormcast", "h", H("massif", "sc", armure=True, face="heaume", arme="fusil", epaulieres=(7, 6, 10), embleme="comete", extras=("cape", "haut_heaume")), (32, 5, 6, .27), cap="foudre", mode="tir", butin=FER)
M("prosecutor", "Poursuivant", "stormcast", "h", H("massif", "sc", armure=True, face="heaume", arme="lance", epaulieres=(7, 6, 10), embleme="comete", extras=("ailes", "halo")), (34, 6, 6, .3), cap="foudre", mode="vol", butin=FER + [("minecraft:feather", 1, 3)])
M("vindictor", "Vengeur", "stormcast", "h", H("massif", "sc", armure=True, face="heaume", arme="lance", main_gauche="bouclier", epaulieres=(7, 6, 10), embleme="comete", extras=("cape", "haut_heaume")), (42, 6, 9, .26), cap="foudre", butin=FER)
M("lord_celestant", "Seigneur-Céleste", "stormcast", "h", H("massif", "sc", armure=True, face="heaume", arme="epee", main_gauche="bouclier", epaulieres=(8, 7, 11), embleme="comete", extras=("cape", "halo", "haut_heaume")), (90, 10, 10, .28), 1.15, cap="foudre", special="onde", butin=OR_)
M("stardrake", "Drake Stellaire", "stormcast", "bete", B("sc", corps=(16, 12, 30), jambe=(5, 12), tete=(9, 8, 10), cou=8, queue=16, ailes=24, cornes=True, crete_dos=True, tex=256), (320, 16, 14, .3), 1.6, cap="foudre", mode="vol", special="onde", butin=[("minecraft:diamond", 1, 3)] + ECAILLE)
M("dracoth", "Chevalier sur Draconide", "stormcast", "bete", B("sc", corps=(10, 8, 18), jambe=(4, 9), tete=(6, 6, 7), cou=4, queue=8, cornes=True, cavalier=True, arme_cavalier="marteau"), (90, 9, 10, .3), 1.1, cap="foudre", special="charge", butin=FER + ECAILLE)
M("gryph_charger", "Chevalier sur Griffon-Coursier", "stormcast", "bete", B("griffon", corps=(8, 8, 16), jambe=(3, 12), tete=(6, 6, 6), cou=5, queue=6, bec=True, criniere=True, cavalier=True, arme_cavalier="lance"), (70, 8, 8, .36), 1.1, cap="foudre", special="charge", butin=[("minecraft:feather", 2, 4)])
# --- Cités d'Aurion
M("heaumefer", "Heaumefer des Compagnies Franches", "cites", "h", H("normal", "cites", armure=True, face="heaume", arme="lance", main_gauche="bouclier", embleme="losange", extras=("tabard",)), (28, 5, 6, .26), butin=FER)
M("cavalier_franc", "Cavalier des Compagnies Franches", "cites", "bete", B("cites", corps=(8, 9, 16), jambe=(3, 12), tete=(4, 5, 8), cou=6, queue=5, sabots=True, caparacon=True, cavalier=True), (45, 7, 6, .36), special="charge", butin=CUIR + FER)
M("fusilier", "Fusilier des Compagnies Franches", "cites", "h", H("normal", "cites", face="visage", arme="fusil", embleme="losange", extras=("tabard",)), (22, 6, 3, .26), mode="tir", butin=[("minecraft:gunpowder", 1, 3)])
M("griffon", "Griffon", "cites", "bete", B("griffon", corps=(12, 10, 22), jambe=(4, 12), tete=(7, 7, 7), cou=6, queue=10, bec=True, ailes=18, criniere=True, griffes_pattes=True), (140, 12, 6, .3), 1.3, mode="vol", special="charge", butin=[("minecraft:feather", 3, 6)] + VIANDE)
M("demigryph", "Demi-Griffon", "cites", "bete", B("griffon", corps=(10, 9, 18), jambe=(4, 12), tete=(6, 6, 6), cou=5, queue=8, bec=True, criniere=True, cavalier=True), (80, 9, 6, .34), 1.1, special="charge", butin=[("minecraft:feather", 2, 4)])
M("dragon", "Dragon", "cites", "bete", B("dragon", corps=(18, 14, 34), jambe=(6, 13), tete=(10, 9, 12), cou=10, queue=20, ailes=28, cornes=True, crete_dos=True, ventre=True, tex=256), (400, 18, 12, .3), 1.8, cap="feu", mode="vol_mage", special="onde", butin=[("minecraft:diamond", 2, 4), ("minecraft:dragon_breath", 1, 2)], poids=1)
# --- Filles de Morvaine (Umbria)
M("furie", "Furie", "khaine", "h", H("fin", "khaine", face="bete", embleme="croc", extras=("ailes", "griffes", "cornes"), main_gauche="griffe"), (22, 5, 1, .34), cap="saignee", mode="vol")
M("khinerai", "Harpie Arrache-Cœur", "khaine", "h", H("fin", "khaine", face="visage", arme="lance", embleme="croc", extras=("ailes", "crete")), (26, 6, 2, .33), cap="saignee", mode="vol_tir")
M("melusai", "Sœur de Sang serpentine", "khaine", "h", H("spectre", "khaine", serpent=True, face="visage", arme="epee", embleme="croc", extras=("crete",)), (40, 7, 4, .28), cap="poison")
M("avatar_khaine", "Avatar de Morvaine", "khaine", "h", H("geant", "avatar", armure=True, face="heaume", arme="epee", embleme="croc", embleme_lueur=True, extras=("cornes",)), (300, 16, 14, .26), 2.2, cap="feu", special="onde", butin=[("minecraft:iron_ingot", 4, 10)], poids=1)
M("medusa", "Méduse Sanglante", "khaine", "h", H("spectre", "khaine", serpent=True, face="visage", arme="lance", embleme="croc", embleme_lueur=True, extras=("crete", "couronne")), (60, 6, 4, .26), cap="poison", mode="mage")
M("ombre_khaine", "Ombre de Morvaine", "khaine", "h", H("spectre", "khaine", serpent=True, face="capuche", arme="dague", main_gauche="dague", embleme="croc", embleme_lueur=True, extras=("ailes",)), (120, 11, 4, .32), 1.4, cap="saignee", mode="vol", poids=2)
# --- Pyrotueurs (Pyréa)
M("vulkite", "Berserker de Braise", "fyreslayers", "h", H("nain", "fyre", face="visage", arme="hache", main_gauche="hache", embleme="croc", extras=("barbe", "crete")), (30, 6, 3, .28), cap="feu", butin=OR_)
M("hearthguard", "Gardien du Foyer", "fyreslayers", "h", H("nain", "fyre", armure=True, face="heaume", arme="double_hache", embleme="croc", extras=("barbe", "crete")), (40, 8, 6, .26), cap="feu", butin=OR_)
M("auric_hearthguard", "Garde du Foyer d'Or", "fyreslayers", "h", H("nain", "fyre", armure=True, face="heaume", arme="baton", embleme="croc", embleme_lueur=True, extras=("barbe", "haut_heaume")), (34, 6, 6, .25), cap="feu", mode="mage", butin=OR_)
M("magmadroth", "Drake de Magma", "fyreslayers", "bete", B("magma", corps=(14, 12, 24), jambe=(5, 10), tete=(8, 7, 9), cou=5, queue=12, cornes=True, crete_dos=True, ventre=True, cavalier=True, arme_cavalier="hache"), (220, 14, 10, .26), 1.4, cap="feu", special="charge", butin=[("minecraft:magma_cream", 2, 5)] + OR_, poids=3)
M("elementaire_magma", "Élémentaire de Magma", "fyreslayers", "h", H("geant", "magma", face="bete", embleme="point", embleme_lueur=True, extras=("cornes",)), (160, 12, 6, .22), 1.6, cap="feu", special="onde", butin=[("minecraft:magma_block", 1, 4)], poids=3)
M("salamandre", "Salamandre", "fyreslayers", "bete", B("magma", corps=(6, 5, 12), jambe=(2, 5), tete=(5, 4, 6), cou=2, queue=8, crete_dos=True), (40, 5, 3, .3), cap="feu", mode="mage", butin=[("minecraft:blaze_powder", 1, 2)])
# --- Abyssaux Idoneths (Umbria : mer d'éther)
M("namarti_thrall", "Serf des Abysses", "idoneth", "h", H("fin", "idoneth", armure=True, face="visage", arme="epee", embleme="point", extras=("cape", "sans_yeux")), (30, 6, 3, .28), butin=[("minecraft:prismarine_shard", 1, 2)])
M("namarti_reaver", "Écumeur des Abysses", "idoneth", "h", H("fin", "idoneth", face="visage", arme="fusil", embleme="point", extras=("sans_yeux",)), (24, 5, 2, .3), mode="tir", butin=[("minecraft:prismarine_shard", 1, 2)])
M("ishlaen", "Garde des Marées", "idoneth", "poisson", B("abyss", corps=(10, 6, 6), cavalier=True, lanternes=True), (60, 8, 6, .3), mode="vol", special="charge", butin=[("minecraft:prismarine_crystals", 1, 3)])
M("leviadon", "Léviathan des Abysses", "idoneth", "poisson", B("abyss", corps=(22, 12, 9), carapace=True, cavalier=True, tex=256), (280, 14, 14, .22), 1.6, mode="vol", special="onde", butin=[("minecraft:turtle_scute", 2, 4), ("minecraft:nautilus_shell", 1, 2)], poids=2)
M("allopex", "Requin de guerre", "idoneth", "poisson", B("abyss", corps=(18, 7, 7), lanternes=True, cavalier=True), (110, 12, 6, .3), 1.2, cap="saignee", mode="vol", butin=[("minecraft:cod", 2, 4), ("minecraft:prismarine_shard", 1, 3)])
M("morrsarr", "Garde des Anguilles", "idoneth", "poisson", B("abyss", corps=(14, 5, 5), cavalier=True, lanternes=True), (70, 9, 6, .32), cap="foudre", mode="vol", special="charge", butin=[("minecraft:prismarine_crystals", 1, 3)])
# --- Magnats Kharadrons (Ferrumia)
M("arkanaute", "Aéronaute", "kharadron", "h", H("nain", "khar", armure=True, face="heaume", arme="fusil", embleme="point", extras=("sac", "barbe")), (26, 5, 6, .25), mode="tir", butin=OR_)
M("endrinrigger", "Gréeur d'Éther", "kharadron", "h", H("nain", "khar", armure=True, face="heaume", arme="marteau", embleme="point", extras=("sac", "barbe")), (32, 6, 6, .28), mode="vol", butin=OR_ + FER)
M("thunderer", "Tonnerreur des Nuées", "kharadron", "h", H("nain", "khar", armure=True, face="heaume", arme="fusil", embleme="point", embleme_lueur=True, extras=("barbe", "haut_heaume")), (30, 7, 7, .24), mode="tir", butin=[("minecraft:gunpowder", 1, 3)])
M("gunhauler", "Canonnière des Nuées", "kharadron", "navire", B("navire", coque=(18, 8, 6), ballon=(10, 6, 12), canons=1), (110, 10, 10, .3), 1.2, mode="vol_tir", butin=[("minecraft:gold_ingot", 1, 3)], poids=3)
M("fregate", "Frégate des Nuées", "kharadron", "navire", B("navire", coque=(26, 10, 7), ballon=(12, 8, 18), canons=2), (220, 12, 12, .26), 1.6, mode="vol_tir", sbire="arkanaute", special="invoque", butin=[("minecraft:gold_ingot", 2, 5)], poids=2)
M("ironclad", "Cuirassé des Nuées", "kharadron", "navire", B("navire", coque=(32, 12, 9), ballon=(14, 9, 22), canons=3, tex=256), (380, 16, 16, .22), 2.0, mode="vol_tir", sbire="thunderer", special="invoque", butin=[("minecraft:gold_block", 1, 2)], poids=1)
# --- Suzerains Lumineths (Lumina)
M("sentinelle_vanari", "Sentinelle de Lumière", "lumineth", "h", H("fin", "lum", armure=True, face="heaume", arme="lance", embleme="comete", embleme_lueur=True, extras=("haut_heaume",)), (24, 5, 3, .28), cap="lumiere", mode="tir", butin=[("minecraft:quartz", 1, 3)])
M("garde_vanari", "Gardien de Lumière", "lumineth", "h", H("fin", "lum", armure=True, face="heaume", arme="lance", embleme="comete", embleme_lueur=True, extras=("haut_heaume", "cape")), (30, 6, 6, .27), cap="lumiere", butin=[("minecraft:quartz", 1, 3)])
M("bladelord", "Maître-Lame", "lumineth", "h", H("fin", "lum", armure=True, face="heaume", arme="epee", embleme="comete", extras=("haut_heaume", "cape")), (36, 9, 5, .31), cap="lumiere", special="charge", butin=[("minecraft:quartz", 2, 4)])
M("alarith", "Esprit de la Montagne", "lumineth", "bete", B("alarith", corps=(14, 12, 20), jambe=(5, 13), tete=(8, 8, 8), cou=6, queue=4, cornes=True, sabots=True, tex=256), (260, 14, 16, .22), 1.6, cap="seisme", special="onde", butin=[("minecraft:calcite", 4, 8), ("minecraft:quartz_block", 1, 3)], poids=2)
M("hurakan", "Esprit du Vent", "lumineth", "h", H("spectre", "lum", face="capuche", arme="lance", embleme="comete", embleme_lueur=True, extras=("ailes",)), (110, 9, 4, .36), 1.3, cap="lumiere", mode="vol", butin=[("minecraft:breeze_rod", 1, 2)], poids=3)
M("scinari", "Illuminé", "lumineth", "h", H("fin", "lum", face="visage", arme="baton", embleme="comete", embleme_lueur=True, extras=("cape", "couronne")), (40, 7, 3, .27), cap="lumiere", mode="mage", butin=[("minecraft:glowstone_dust", 2, 4)])
# --- Séraphons (jungles de Sylvéa)
M("saurus", "Guerrier Écailleux", "seraphon", "h", H("massif", "sera", face="bete", arme="massue", main_gauche="rondache", embleme="point", extras=("queue", "museau")), (34, 6, 4, .26), 1.1, butin=ECAILLE)
M("skink", "Scinque", "seraphon", "h", H("petit", "sera", face="bete", arme="lance", embleme="point", extras=("queue", "museau")), (16, 3, 1, .31), cap="poison", mode="tir")
M("kroxigor", "Croc-Brute", "seraphon", "h", H("geant", "sera", face="bete", arme="massue", embleme="point", extras=("queue", "museau", "machoire")), (90, 12, 6, .24), 1.3, special="charge", butin=ECAILLE + VIANDE)
M("carnosaur", "Carnosaure", "seraphon", "bete", B("sera", corps=(14, 14, 22), jambe=(6, 16), tete=(10, 9, 12), cou=4, queue=18, crete_dos=True, ventre=True, cavalier=True, arme_cavalier="lance", tex=256), (300, 18, 10, .3), 1.6, cap="saignee", special="charge", butin=VIANDE + ECAILLE + [("minecraft:bone", 3, 6)], poids=2)
M("stegadon", "Stégodonte", "seraphon", "bete", B("sera", corps=(18, 12, 26), jambe=(6, 10), tete=(10, 8, 10), cou=3, queue=14, corne_nez=True, cornes=True, collerette=True, plaques=True, queue_massue=True, nacelle=True, tex=256), (320, 14, 16, .22), 1.6, special="charge", butin=ECAILLE + VIANDE, poids=2)
M("bastiladon", "Bastionodon", "seraphon", "bete", B("sera", corps=(16, 10, 22), jambe=(5, 7), tete=(8, 6, 8), cou=2, queue=10, carapace=True, queue_massue=True, autel=True), (300, 10, 20, .18), 1.4, cap="lumiere", mode="mage", butin=ECAILLE + [("minecraft:turtle_scute", 1, 3)], poids=2)
# --- Sylvaneths (Sylvéa)
M("dryade", "Dryade", "sylvaneth", "h", H("fin", "sylv", face="bete", embleme="point", embleme_lueur=True, extras=("branches", "griffes"), main_gauche="griffe"), (30, 5, 4, .27), special="regen", butin=[("minecraft:stick", 2, 4), ("minecraft:oak_sapling", 0, 1)])
M("revenant", "Revenant Sylvestre", "sylvaneth", "h", H("fin", "sylv", face="bete", arme="epee", embleme="point", embleme_lueur=True, extras=("branches", "cape")), (32, 7, 4, .3), special="regen", butin=[("minecraft:stick", 2, 4)])
M("kurnoth", "Chasseur Cornu", "sylvaneth", "h", H("massif", "sylv", face="bete", arme="lance", embleme="point", embleme_lueur=True, extras=("branches", "cornes")), (60, 8, 6, .26), 1.2, mode="tir", special="regen", butin=[("minecraft:oak_log", 1, 3)])
M("treelord", "Seigneur-Arbre", "sylvaneth", "h", H("geant", "sylv", face="bete", embleme="point", embleme_lueur=True, extras=("branches", "griffes"), main_gauche="griffe"), (220, 14, 10, .22), 2.0, special="regen", butin=[("minecraft:oak_log", 4, 8), ("minecraft:moss_block", 1, 3)], poids=3)
M("durthu", "Esprit du Chêne-Roi", "sylvaneth", "h", H("geant", "sylv", face="bete", arme="epee", embleme="point", embleme_lueur=True, extras=("branches", "cornes")), (360, 18, 12, .22), 2.3, special="onde", butin=[("minecraft:dark_oak_log", 6, 10)], poids=1)
M("treelord_ancien", "Ancien Seigneur-Arbre", "sylvaneth", "h", H("geant", "sylv", face="bete", arme="baton", embleme="point", embleme_lueur=True, extras=("branches", "couronne")), (260, 12, 10, .2), 2.1, cap="seisme", mode="mage", special="regen", butin=[("minecraft:oak_log", 4, 8)], poids=2)

# ==================================================================== CHAOS
# --- Légions des Ténèbres
M("guerrier_chaos", "Guerrier du Chaos", "esclaves", "h", H("massif", "chaos", armure=True, face="heaume", arme="hache", main_gauche="bouclier", epaulieres=(7, 7, 10), embleme="etoile", extras=("cornes", "cape")), (40, 7, 8, .25), butin=FER)
M("chevalier_chaos", "Chevalier du Chaos", "esclaves", "bete", B("chaos_cheval", corps=(8, 9, 17), jambe=(3, 12), tete=(4, 5, 8), cou=6, queue=5, sabots=True, caparacon=True, cornes=True, cavalier=True), (70, 9, 10, .34), special="charge", butin=FER + CUIR)
M("chosen", "Élu du Chaos", "esclaves", "h", H("massif", "chaos", armure=True, face="heaume", arme="double_hache", epaulieres=(8, 8, 11), embleme="etoile", embleme_lueur=True, extras=("grandes_cornes", "cape")), (60, 10, 10, .26), 1.1, cap="feu", butin=FER + [("minecraft:gold_ingot", 0, 1)])
M("warshrine", "Autel de Guerre du Chaos", "esclaves", "char", B("chaos", caisse=(12, 10, 6), toit=True, autel=True), (180, 10, 12, .2), 1.4, special="aura_buff", butin=[("minecraft:gold_ingot", 1, 3)], poids=2)
M("prince_demon", "Prince Démon", "esclaves", "h", H("massif", "demon", armure=True, face="bete", arme="epee", epaulieres=(8, 8, 11), embleme="etoile", embleme_lueur=True, extras=("grandes_cornes", "ailes")), (260, 16, 10, .3), 1.8, cap="feu", mode="vol", special="onde", butin=[("minecraft:diamond", 1, 2)], poids=1)
M("rejeton_chaos", "Rejeton du Chaos", "esclaves", "blob", B("rejeton", taille=12, tentacules=True, cornes=True), (70, 9, 2, .27), 1.2, special="regen", butin=[("minecraft:rotten_flesh", 2, 5)])
# --- Disciples de Vharys
M("tzaangor", "Homme-Bec", "tzeentch", "h", H("normal", "tzeentch", face="bete", arme="lance", main_gauche="rondache", embleme="etoile", extras=("bec", "grandes_cornes")), (24, 5, 3, .28), cap="feu_magique", butin=[("minecraft:feather", 1, 2)])
M("acolyte", "Acolyte du Changement", "tzeentch", "h", H("normal", "tzeentch", face="capuche", arme="baton", embleme="etoile", embleme_lueur=True, extras=("cape",)), (20, 5, 1, .27), cap="feu_magique", mode="mage", butin=[("minecraft:lapis_lazuli", 1, 3)])
M("horreur_rose", "Horreur Chatoyante", "tzeentch", "h", H("normal", "rose", face="bete", embleme="point", embleme_lueur=True, extras=("griffes", "machoire"), main_gauche="griffe"), (26, 5, 2, .27), cap="feu_magique", mode="mage", butin=[("minecraft:pink_dye", 1, 2)])
M("seigneur_changement", "Grand Démon du Changement", "tzeentch", "h", H("geant", "tzeentch", face="bete", arme="baton", embleme="etoile", embleme_lueur=True, extras=("bec", "ailes", "grandes_cornes")), (320, 14, 10, .3), 2.0, cap="feu_magique", mode="vol_mage", special="onde", butin=[("minecraft:diamond", 1, 2), ("minecraft:feather", 4, 8)], poids=1)
M("char_flammes", "Char Flamboyant de Vharys", "tzeentch", "char", B("tzeentch", caisse=(8, 8, 3), disque=True), (110, 9, 6, .3), 1.2, cap="feu_magique", mode="vol_mage", butin=[("minecraft:blaze_powder", 2, 4)], poids=3)
M("mutalith", "Bête du Vortex", "tzeentch", "blob", B("tzeentch", taille=16, tentacules=True, cornes=True, cavalier=True, tex=256), (240, 12, 8, .2), 1.6, cap="feu_magique", mode="mage", special="regen", butin=[("minecraft:ender_pearl", 1, 3)], poids=2)
# --- Lames de Sangrath
M("bloodletter", "Saigneur Démoniaque", "khorne", "h", H("normal", "khorne", face="bete", arme="epee", embleme="croc", embleme_lueur=True, extras=("cornes", "machoire")), (28, 7, 2, .3), cap="saignee", butin=[("minecraft:redstone", 1, 3)])
M("blood_warrior", "Guerrier de Sang", "khorne", "h", H("massif", "khorne", armure=True, face="heaume", arme="hache", main_gauche="hache", epaulieres=(7, 6, 9), embleme="croc", extras=("cornes",)), (40, 8, 8, .27), cap="saignee", butin=FER)
M("bloodreaver", "Pillard de Sang", "khorne", "h", H("normal", "khorne", face="visage", arme="hache", main_gauche="hache", embleme="croc", extras=("cornes",)), (26, 6, 3, .29), cap="saignee", butin=FER)
M("skullreaper", "Faucheur de Crânes", "khorne", "h", H("massif", "khorne", armure=True, face="bete", arme="double_hache", epaulieres=(8, 7, 10), embleme="croc", embleme_lueur=True, extras=("grandes_cornes", "machoire")), (60, 10, 8, .28), 1.1, cap="saignee", butin=[("minecraft:redstone", 2, 4), ("minecraft:skeleton_skull", 0, 1)])
M("bloodthirster", "Grand Démon du Sang", "khorne", "h", H("geant", "khorne", face="bete", arme="double_hache", main_gauche="hache", embleme="croc", embleme_lueur=True, extras=("grandes_cornes", "ailes", "machoire")), (380, 18, 12, .3), 2.1, cap="feu", mode="vol", special="onde", butin=[("minecraft:netherite_scrap", 1, 2)], poids=1)
M("chien_khorne", "Chien de Sangrath", "khorne", "bete", B("khorne", corps=(6, 7, 14), jambe=(2, 8), tete=(5, 5, 6), cou=3, queue=6, cornes=True, crete_dos=True), (34, 7, 6, .38), cap="saignee", special="charge", butin=CUIR + [("minecraft:redstone", 1, 2)])
M("juggernaut", "Juggernaut de Sangrath", "khorne", "bete", B("laiton", corps=(12, 11, 20), jambe=(5, 11), tete=(7, 7, 7), cou=2, queue=4, cornes=True, sabots=True, cavalier=True, arme_cavalier="hache"), (160, 13, 16, .3), 1.3, special="charge", butin=[("minecraft:copper_ingot", 2, 6)], poids=3)
# --- Hédonites de Lyssara
M("demonette", "Démonette", "slaanesh", "h", H("fin", "slaanesh", face="visage", embleme="point", extras=("pinces", "cornes", "crete")), (20, 5, 1, .33), cap="saignee", butin=[("minecraft:pink_petals", 1, 3)])
M("seeker", "Coursier de Lyssara", "slaanesh", "bete", B("slaanesh", corps=(6, 7, 14), jambe=(2, 12), tete=(4, 4, 6), cou=7, queue=6, cavalier=True, arme_cavalier="epee"), (40, 6, 2, .42), cap="saignee", special="charge", butin=CUIR)
M("painbringer", "Myrmidon de la Douleur", "slaanesh", "h", H("fin", "slaanesh", armure=True, face="heaume", arme="epee", main_gauche="rondache", embleme="point", extras=("crete",)), (32, 7, 6, .3), cap="saignee", butin=FER)
M("gardien_secrets", "Grand Démon des Plaisirs", "slaanesh", "h", H("geant", "slaanesh", face="bete", arme="epee", embleme="point", embleme_lueur=True, extras=("grandes_cornes", "griffes"), main_gauche="griffe"), (340, 16, 8, .32), 2.0, cap="saignee", special="onde", butin=[("minecraft:amethyst_shard", 4, 8), ("minecraft:diamond", 0, 2)], poids=1)
M("syllesske", "Les Jumeaux de la Concorde", "slaanesh", "h", H("spectre", "slaanesh", serpent=True, face="visage", arme="hache", main_gauche="dague", embleme="point", embleme_lueur=True, extras=("couronne", "crete")), (220, 13, 8, .3), 1.6, cap="saignee", mode="mage", butin=[("minecraft:amethyst_shard", 3, 6)], poids=1)
M("demon_slaanesh", "Démon de Lyssara", "slaanesh", "bete", B("slaanesh", corps=(8, 7, 12), jambe=(2, 8), tete=(5, 5, 5), cou=3, queue=10, dard=True, griffes_pattes=True), (60, 8, 4, .34), cap="poison", butin=[("minecraft:spider_eye", 1, 2)])
# --- Engeance de Morbus
M("plaguebearer", "Porte-Fléau", "nurgle", "h", H("normal", "nurgle", face="bete", arme="epee", embleme="crane", extras=("corne_unique", "cyclope", "ventre_ouvert")), (30, 5, 3, .22), cap="poison", special="aura_peste", butin=[("minecraft:slime_ball", 1, 2)])
M("blightking", "Roi Putride", "nurgle", "h", H("geant", "nurgle", armure=True, face="heaume", arme="hache", main_gauche="bouclier", embleme="crane", extras=("ventre", "cornes")), (70, 10, 8, .22), 1.1, cap="poison", butin=FER + [("minecraft:slime_ball", 1, 2)])
M("pusgoyle", "Seigneur des Mouches", "nurgle", "bete", B("nurgle", corps=(10, 9, 14), jambe=(3, 8), tete=(6, 6, 6), cou=2, queue=6, ailes=14, dard=True, cavalier=True, arme_cavalier="lance"), (90, 10, 8, .28), 1.2, cap="poison", mode="vol", butin=[("minecraft:slime_ball", 2, 4)])
M("grand_immonde", "Grand Démon de la Peste", "nurgle", "h", H("geant", "nurgle", face="crane", arme="baton", embleme="crane", embleme_lueur=True, extras=("ventre", "grandes_cornes")), (420, 15, 10, .18), 2.4, cap="poison", special="aura_peste", butin=[("minecraft:slime_block", 2, 4)], poids=1)
M("bete_nurgle", "Bête de Morbus", "nurgle", "blob", B("nurgle", taille=12, tentacules=True, pustules=True), (80, 6, 3, .2), 1.2, cap="poison", special="aura_peste", butin=[("minecraft:slime_ball", 2, 5)])
# --- Hommes-Rats (Terres Rongées)
M("clanrat", "Rat de Clan", "skaven", "h", H("petit", "skaven", face="bete", arme="epee", main_gauche="rondache", embleme="point", embleme_lueur=True, extras=("museau", "queue")), (16, 4, 2, .31), butin=FER)
M("stormvermin", "Rat de Choc", "skaven", "h", H("normal", "skaven", armure=True, face="bete", arme="lance", embleme="point", embleme_lueur=True, extras=("museau", "queue")), (28, 6, 6, .29), butin=FER)
M("jezzail", "Tireur de Long-Fusil", "skaven", "h", H("petit", "skaven", face="bete", arme="fusil", embleme="point", embleme_lueur=True, extras=("museau", "queue", "sac")), (18, 7, 2, .28), cap="poison", mode="tir", butin=[("minecraft:gunpowder", 1, 2)])
M("abomination", "Abomination des Fosses", "skaven", "blob", B("skaven", taille=18, rats=True, tentacules=True, tex=256), (300, 14, 6, .22), 1.8, special="regen", butin=[("minecraft:rotten_flesh", 4, 8)], poids=1)
M("rat_ogre", "Rat-Ogre", "skaven", "h", H("geant", "skaven", face="bete", embleme="point", embleme_lueur=True, extras=("museau", "queue", "griffes"), main_gauche="griffe"), (90, 12, 5, .28), 1.2, special="charge", butin=CUIR + [("minecraft:bone", 1, 3)])
M("doomwheel", "Roue Infernale", "skaven", "char", B("skaven", roue_geante=True), (150, 12, 10, .32), 1.2, cap="foudre_verte", mode="tir", special="charge", butin=[("minecraft:copper_ingot", 2, 4)], poids=3)
# --- Ashkar (Nain du Chaos)
M("hashut", "Garde Infernale de Ashkar", "hashut", "h", H("nain", "hashut", armure=True, face="heaume", arme="hache", main_gauche="bouclier", embleme="etoile", embleme_lueur=True, extras=("barbe", "haut_heaume")), (32, 6, 6, .25), cap="feu", butin=FER)

# ==================================================================== MORT
# --- Cours des Mangechairs
M("goule", "Goule des Cryptes", "fec", "h", H("fin", "fec", face="bete", embleme="point", extras=("griffes",), main_gauche="griffe"), (22, 5, 1, .32), cap="saignee", butin=OS)
M("horreur_crypte", "Horreur des Cryptes", "fec", "h", H("geant", "fec", face="bete", embleme="point", extras=("griffes", "machoire"), main_gauche="griffe"), (60, 9, 3, .28), cap="saignee", special="regen", butin=OS + [("minecraft:rotten_flesh", 1, 3)])
M("morbheg", "Chevalier Chauve-Souris", "fec", "bete", B("fec", corps=(9, 8, 16), jambe=(3, 11), tete=(6, 6, 6), cou=4, queue=6, ailes=10, cavalier=True, arme_cavalier="lance"), (70, 9, 5, .33), cap="saignee", special="charge", butin=OS + CUIR)
M("terrorgheist", "Spectre-Terreur", "fec", "bete", B("fec", corps=(14, 11, 22), jambe=(4, 12), tete=(9, 8, 9), cou=6, queue=8, ailes=24, tex=256), (260, 14, 8, .3), 1.6, cap="drain", mode="vol_mage", special="onde", butin=OS + [("minecraft:phantom_membrane", 2, 4)], biomes=["shyish_terres"], poids=1)
M("dragon_zombie", "Dragon Zombie", "soulblight", "bete", B("sbz", corps=(16, 12, 30), jambe=(5, 12), tete=(10, 8, 11), cou=9, queue=16, ailes=26, cornes=True, crete_dos=True, cavalier=True, arme_cavalier="epee", tex=256), (340, 16, 10, .28), 1.8, cap="poison", mode="vol_mage", special="onde", butin=OS + [("minecraft:phantom_membrane", 2, 4)], poids=1)
M("varghulf", "Vampire-Bête", "fec", "bete", B("fec", corps=(10, 10, 14), jambe=(4, 10), tete=(7, 7, 7), cou=2, queue=0, ailes=12, griffes_pattes=True, criniere=True), (140, 13, 6, .34), 1.3, cap="saignee", special="charge", butin=OS + CUIR, poids=3)
# --- Hantise Nocturne
M("chainrasp", "Spectre Enchaîné", "nighthaunt", "h", H("spectre", "nh", face="capuche", arme="epee", embleme="crane", embleme_lueur=True), (20, 5, 0, .28), cap="drain", butin=[("minecraft:iron_chain", 0, 1)])
M("grimghast", "Faucheur Spectral", "nighthaunt", "h", H("spectre", "nh", face="capuche", arme="faux", embleme="crane", embleme_lueur=True, extras=("cape",)), (24, 7, 0, .3), cap="drain", butin=[("minecraft:phantom_membrane", 0, 1)])
M("hote_spirite", "Hôte Spirite", "nighthaunt", "h", H("spectre", "nh", face="capuche", embleme="crane", embleme_lueur=True, extras=("griffes",), main_gauche="griffe"), (40, 5, 0, .26), 1.2, cap="drain", mode="vol", butin=[("minecraft:soul_sand", 1, 2)])
M("carrosse_noir", "Carrosse Noir", "nighthaunt", "char", B("nh", caisse=(14, 10, 6), toit=True, betes=True), (200, 12, 8, .32), 1.4, cap="drain", special="charge", butin=[("minecraft:soul_lantern", 1, 2)], poids=2)
M("dreadblade", "Cavalier Spectral", "nighthaunt", "bete", B("nh", corps=(8, 9, 16), jambe=(3, 12), tete=(4, 5, 8), cou=6, queue=5, sabots=True, cavalier=True, arme_cavalier="epee"), (60, 9, 4, .38), cap="drain", special="charge", butin=[("minecraft:soul_sand", 1, 2)])
M("mourngul", "Dévoreur Lugubre", "nighthaunt", "h", H("geant", "nh", face="bete", embleme="crane", embleme_lueur=True, extras=("griffes", "machoire"), main_gauche="griffe"), (220, 13, 6, .3), 1.6, cap="drain", special="regen", butin=[("minecraft:soul_soil", 2, 4), ("minecraft:echo_shard", 0, 1)], poids=2)
# --- Faucheurs d'Os (déserts d'os de Nécréa)
M("mortek", "Gard'Os", "ossiarch", "h", H("massif", "ossi", armure=True, face="crane", arme="lance", main_gauche="bouclier", epaulieres=(6, 5, 9), embleme="crane", embleme_lueur=True), (36, 6, 6, .25), cap="drain", butin=OS + [("minecraft:bone_meal", 1, 3)])
M("kavalos", "Cavalier d'Os", "ossiarch", "bete", B("ossi", corps=(8, 9, 16), jambe=(3, 12), tete=(4, 5, 8), cou=6, queue=4, sabots=True, crete_dos=True, cavalier=True), (60, 9, 8, .36), cap="drain", special="charge", butin=OS + [("minecraft:bone_block", 0, 1)])
M("immortis", "Garde Immortelle", "ossiarch", "h", H("geant", "ossi", armure=True, face="crane", arme="lance", main_gauche="bouclier", embleme="crane", embleme_lueur=True), (90, 11, 12, .24), 1.2, cap="drain", butin=OS + [("minecraft:bone_block", 1, 2)])
M("gothizzar", "Moissonneur d'Os", "ossiarch", "bete", B("ossi", corps=(16, 12, 20), jambe=(5, 12), tete=(8, 7, 8), cou=4, queue=8, cornes=True, crete_dos=True, nacelle=True, tex=256), (300, 14, 14, .2), 1.6, cap="drain", special="invoque", sbire="mortek", butin=[("minecraft:bone_block", 3, 6)], poids=1)
M("morghast_archai", "Archange d'Os", "ossiarch", "h", H("massif", "ossi", armure=True, face="crane", arme="epee", main_gauche="bouclier", epaulieres=(7, 6, 10), embleme="crane", embleme_lueur=True, extras=("ailes", "cornes")), (120, 12, 12, .3), 1.4, cap="drain", mode="vol", butin=OS + [("minecraft:bone_block", 1, 2)], poids=3)
M("morghast_harbinger", "Héraut d'Os", "ossiarch", "h", H("massif", "ossi", armure=True, face="crane", arme="faux", epaulieres=(7, 6, 10), embleme="crane", embleme_lueur=True, extras=("ailes", "cornes")), (110, 14, 10, .31), 1.4, cap="drain", mode="vol", butin=OS + [("minecraft:bone_block", 1, 2)], poids=3)
# --- Sanguinaire Gravelords
M("deathrattle", "Squelette Cliquetant", "soulblight", "h", H("squelette", "sbz", face="crane", arme="epee", main_gauche="rondache", embleme="crane"), (22, 5, 3, .26), butin=OS)
M("grave_guard", "Garde des Tombes", "soulblight", "h", H("squelette", "sbz", armure=True, face="crane", arme="epee", main_gauche="bouclier", embleme="crane", embleme_lueur=True, extras=("cape",)), (30, 7, 6, .26), cap="drain", butin=OS + FER)
M("blood_knight", "Chevalier de Sang", "soulblight", "bete", B("sb", corps=(8, 9, 17), jambe=(3, 12), tete=(4, 5, 8), cou=6, queue=5, sabots=True, caparacon=True, cavalier=True), (80, 11, 10, .35), cap="drain", special="charge", butin=FER + [("minecraft:redstone", 1, 3)])
M("vargheist", "Vampire Ailé", "soulblight", "h", H("fin", "sb", face="bete", embleme="point", extras=("ailes", "griffes", "machoire"), main_gauche="griffe"), (50, 9, 3, .33), cap="drain", mode="vol", butin=OS + CUIR)
M("bete_zombie", "Bête Zombie", "soulblight", "bete", B("sbz", corps=(7, 7, 14), jambe=(3, 9), tete=(5, 5, 7), cou=3, queue=5, criniere=True), (34, 7, 2, .33), cap="poison", butin=OS + [("minecraft:rotten_flesh", 1, 3)])
M("vampire", "Seigneur Vampire", "soulblight", "h", H("normal", "sb", armure=True, face="visage", arme="epee", embleme="crane", extras=("cape", "couronne")), (70, 9, 6, .3), 1.05, cap="drain", sbire="deathrattle", special="invoque", butin=[("minecraft:gold_ingot", 1, 2), ("minecraft:redstone", 2, 4)], poids=4)

# ==================================================================== DESTRUCTION
# --- Gobelins de la Lune Noire (Umbria)
M("shoota", "Archer de la Lune", "gitz", "h", H("petit", "gitz", face="bete", arme="fusil", embleme="point", extras=("chapeau",)), (12, 4, 0, .3), mode="tir", butin=[("minecraft:arrow", 1, 4)])
M("squig_hopper", "Croqueur Sauteur", "gitz", "blob", B("squig", taille=9, cavalier=True), (24, 6, 1, .34), special="saut", butin=[("minecraft:red_mushroom", 1, 2)])
M("stabba", "Piqueur de la Lune", "gitz", "h", H("petit", "gitz", face="bete", arme="lance", embleme="point", extras=("chapeau",)), (12, 4, 1, .3), butin=[("minecraft:brown_mushroom", 0, 2)])
M("squig_mangler", "Croqueurs Broyeurs", "gitz", "blob", B("squig", taille=16, cavalier=True), (140, 14, 2, .3), 1.4, special="saut", butin=[("minecraft:red_mushroom", 2, 4), ("minecraft:leather", 1, 3)], poids=3)
M("squig_colossal", "Croqueur Colossal", "gitz", "blob", B("squig", taille=22, tex=256), (300, 16, 4, .28), 2.0, special="onde", butin=[("minecraft:red_mushroom_block", 2, 5)], poids=1)
M("troggoth_dankhold", "Troll des Profondeurs", "gitz", "h", H("geant", "troll", face="bete", arme="massue", embleme="point", extras=("machoire",)), (200, 15, 8, .2), 1.8, special="regen", butin=[("minecraft:mossy_cobblestone", 2, 5)], poids=3)
# --- Tribus Ogresses (Féralia)
M("glutton", "Ogre Glouton", "ogors", "h", H("geant", "ogor", face="visage", arme="massue", embleme="croc", extras=("ventre",)), (60, 9, 4, .22), 1.3, cap="waaagh", butin=VIANDE)
M("irongut", "Ventre-de-Fer", "ogors", "h", H("geant", "ogor", armure=True, face="visage", arme="massue", embleme="croc", extras=("ventre", "barbe")), (80, 11, 8, .22), 1.35, cap="waaagh", butin=VIANDE + FER)
M("leadbelcher", "Crache-Plomb", "ogors", "h", H("geant", "ogor", face="visage", arme="fusil", embleme="croc", extras=("ventre",)), (60, 10, 4, .21), 1.3, mode="tir", butin=[("minecraft:gunpowder", 2, 4)])
M("stonehorn", "Corne-de-Pierre", "ogors", "bete", B("ogor", corps=(18, 14, 24), jambe=(6, 12), tete=(10, 9, 9), cou=2, queue=6, cornes=True, defenses=True, carapace=True, cavalier=True, arme_cavalier="lance", tex=256), (320, 16, 16, .24), 1.6, special="charge", butin=[("minecraft:stone", 6, 12), ("minecraft:leather", 2, 4)], poids=2)
M("thundertusk", "Défense-Tonnerre", "ogors", "bete", B("givre", corps=(18, 15, 24), jambe=(6, 12), tete=(10, 9, 9), cou=2, queue=4, defenses=True, criniere=True, nacelle=True, tex=256), (300, 14, 12, .22), 1.6, cap="seisme", mode="mage", butin=[("minecraft:packed_ice", 2, 5), ("minecraft:leather", 2, 4)], poids=2)
M("sabre_givre", "Sabre de Givre", "ogors", "bete", B("givre", corps=(6, 6, 13), jambe=(2, 8), tete=(5, 5, 6), cou=2, queue=8, defenses=True), (30, 7, 2, .38), cap="seisme", special="charge", butin=CUIR)
# --- Orc Warclans (Féralia / marais de Sylvéa pour les Cruelgars)
M("ardboy", "Dur-à-Cuire", "orruks", "h", H("massif", "orruk", armure=True, face="bete", arme="couperet", main_gauche="bouclier", embleme="croc", extras=("machoire",)), (36, 7, 6, .26), cap="waaagh", butin=[("minecraft:iron_nugget", 3, 7)])
M("brute", "Brute Mâchefers", "orruks", "h", H("massif", "orruk", armure=True, face="bete", arme="couperet", embleme="croc", epaulieres=(7, 6, 9), extras=("machoire",)), (45, 8, 7, .25), 1.15, cap="waaagh", butin=FER)
M("gutrippa", "Étripeur Cruelgars", "orruks", "h", H("normal", "kb", face="bete", arme="epee", main_gauche="rondache", embleme="croc", extras=("machoire",)), (28, 5, 4, .27), 1.1, cap="poison", butin=FER, biomes=["ghyran_marais", "ulgu_marais_lune"])
M("megaboss", "Grand Chef Mâchefers", "orruks", "h", H("massif", "orruk", armure=True, face="bete", arme="couperet", main_gauche="hache", epaulieres=(9, 8, 11), embleme="croc", extras=("machoire", "cornes")), (110, 13, 10, .25), 1.35, cap="waaagh", special="onde", sbire="ardboy", butin=FER + [("minecraft:iron_ingot", 2, 4)], poids=3)
M("maw_krusha", "Broyeur-Gueule", "orruks", "bete", B("orruk", corps=(16, 14, 22), jambe=(6, 12), tete=(10, 9, 10), cou=2, queue=6, ailes=10, cornes=True, crete_dos=True, cavalier=True, arme_cavalier="hache", tex=256), (320, 17, 12, .28), 1.7, cap="waaagh", special="charge", butin=[("minecraft:iron_block", 1, 2), ("minecraft:leather", 2, 4)], poids=1)
M("mirebrute", "Troll des Marais", "orruks", "h", H("geant", "troll", face="bete", arme="massue", embleme="point", extras=("machoire", "branches")), (200, 15, 8, .2), 1.8, special="regen", butin=[("minecraft:mud", 2, 5)], biomes=["ghyran_marais"], poids=3)
M("idole_rogue", "Idole Sauvage", "orruks", "h", H("geant", "pierre", face="bete", embleme="croc", embleme_lueur=True, extras=("cornes", "machoire")), (360, 18, 18, .18), 2.4, cap="seisme", special="onde", butin=[("minecraft:cobblestone", 8, 16), ("minecraft:emerald", 1, 3)], poids=1)
# --- Fils d'Ymorath
M("mancrusher", "Géant Broyeur", "behemat", "h", H("geant", "gargant", face="visage", arme="massue", embleme="point", extras=("ventre", "barbe")), (180, 14, 4, .22), 2.6, cap="seisme", special="onde", butin=VIANDE + [("minecraft:leather", 2, 4)], poids=3)
M("mega_gargant", "Méga-Géant", "behemat", "h", H("geant", "gargant", face="visage", arme="massue", embleme="point", extras=("ventre", "barbe")), (420, 20, 8, .22), 3.6, cap="seisme", special="onde", butin=[("minecraft:beef", 6, 12), ("minecraft:leather", 4, 8)], poids=1)
M("gatebreaker", "Brise-Porte Méga-Géant", "behemat", "h", H("geant", "gargant", armure=True, face="visage", arme="massue", embleme="point", extras=("ventre", "barbe", "cornes")), (480, 22, 12, .21), 3.8, cap="seisme", special="onde", butin=[("minecraft:iron_block", 1, 3)], poids=1)
M("kraken_eater", "Mange-Kraken Méga-Géant", "behemat", "h", H("geant", "gargant", face="visage", arme="faux", embleme="point", extras=("ventre", "barbe")), (460, 21, 10, .22), 3.7, cap="seisme", special="onde", butin=[("minecraft:nautilus_shell", 1, 3), ("minecraft:cod", 4, 8)], poids=1)
M("warstomper", "Piétine-Guerre Méga-Géant", "behemat", "h", H("geant", "gargant", face="visage", arme="massue", embleme="point", extras=("ventre",)), (450, 20, 10, .23), 3.7, cap="seisme", special="onde", butin=[("minecraft:beef", 6, 12)], poids=1)
M("beast_smasher", "Broie-Bêtes Méga-Géant", "behemat", "h", H("geant", "gargant", face="visage", arme="massue", embleme="point", extras=("ventre", "cornes")), (450, 21, 10, .22), 3.7, cap="seisme", special="onde", butin=[("minecraft:leather", 6, 10)], poids=1)

# ==================================================================== BOSS LÉGENDAIRES (sceaux)
M("nagash", "Necrath, Dieu de la Mort", "soulblight", "h", H("squelette", "sbz", armure=True, face="crane", arme="baton", embleme="crane", embleme_lueur=True, extras=("ailes", "couronne", "cape")), (900, 16, 14, .26), 3.0, cap="drain", mode="vol_mage", special="onde", sbire="grave_guard", boss=True)
M("archaon", "Varkhan le Fléau Éternel", "esclaves", "h", H("massif", "chaos", armure=True, face="heaume", arme="epee", main_gauche="bouclier", epaulieres=(9, 9, 12), embleme="etoile", embleme_lueur=True, extras=("grandes_cornes", "cape", "couronne")), (1000, 18, 16, .27), 1.9, cap="feu", special="onde", sbire="chosen", boss=True)
M("gordrakk", "Krognak, le Poing de Brog", "orruks", "h", H("massif", "orruk", armure=True, face="bete", arme="couperet", main_gauche="hache", epaulieres=(10, 9, 12), embleme="croc", extras=("machoire", "cornes", "cape")), (800, 17, 12, .28), 1.9, cap="waaagh", special="onde", sbire="brute", boss=True)
M("skarbrand", "Brakhar l'Exilé", "khorne", "h", H("geant", "khorne", face="bete", arme="double_hache", main_gauche="hache", embleme="croc", embleme_lueur=True, extras=("grandes_cornes", "ailes")), (850, 18, 8, .27), 2.2, cap="feu", special="onde", sbire="bloodletter", boss=True)
M("thanquol", "Skrivel, Prophète des Cendres", "skaven", "h", H("petit", "skaven", face="bete", arme="baton", embleme="point", embleme_lueur=True, extras=("museau", "queue", "grandes_cornes", "cape")), (750, 14, 8, .3), 2.4, cap="foudre_verte", mode="mage", special="onde", sbire="stormvermin", boss=True)
M("rotigus", "Putrefax le Pluviomancien", "nurgle", "h", H("geant", "nurgle", face="crane", arme="baton", embleme="crane", embleme_lueur=True, extras=("ventre", "grandes_cornes")), (950, 15, 10, .2), 2.2, cap="poison", special="aura_peste", sbire="plaguebearer", boss=True)

IDS = [m["id"] for m in TOUS]
assert len(IDS) == len(set(IDS)), "identifiants en double"

# Couleurs propres à certaines montures et créatures (remplacent la palette de faction)
TEINTES = {
    "stormvermin": dict(armure=(150, 40, 38), armure2=(70, 64, 60)),
    "carnosaur": dict(peau=(206, 204, 188), ventre=(228, 224, 210), crete=(120, 80, 150), corne=(240, 236, 222), armure=(200, 150, 70)),
    "bastiladon": dict(peau=(70, 130, 96), armure=(64, 112, 56), ventre=(170, 200, 150)),
    "seigneur_changement": dict(peau=(58, 80, 172), plume=(56, 78, 170), ventre=(226, 226, 236), corne=(150, 90, 160), membrane=(56, 78, 170)),
    "horreur_rose": dict(peau=(232, 128, 186)),
    "ishlaen": dict(peau=(104, 84, 116), ventre=(170, 150, 176)),
    "allopex": dict(peau=(196, 150, 66), ventre=(226, 200, 140)),
    "morbheg": dict(peau=(132, 84, 60), poils=(70, 44, 34), membrane=(48, 36, 36)),
    "vargheist": dict(peau=(226, 222, 222), membrane=(92, 62, 52)),
    "bete_nurgle": dict(peau=(120, 160, 80), membrane=(206, 104, 146), ventre=(190, 200, 140)),
    "troggoth_dankhold": dict(peau=(82, 128, 156), ventre=(222, 216, 190)),
    "mournfang": dict(peau=(110, 76, 52), poils=(80, 56, 40)),
    "stardrake": dict(peau=(52, 84, 168), ventre=(160, 190, 230), corne=(236, 236, 242), membrane=(64, 104, 196)),
    "dracoth": dict(peau=(88, 108, 150), ventre=(184, 194, 214), corne=(230, 230, 236)),
    "gryph_charger": dict(peau=(128, 138, 160), corne=(222, 184, 80), poils=(92, 98, 120)),
    "cavalier_franc": dict(peau=(112, 76, 46), poils=(38, 26, 18)),
    "blood_knight": dict(peau=(42, 32, 36), poils=(20, 16, 18), ventre=(60, 48, 52)),
    "chevalier_chaos": dict(poils=(20, 18, 20)),
    "stonehorn": dict(peau=(122, 120, 114), corne=(204, 198, 186), ventre=(150, 146, 138)),
    "demigryph": dict(peau=(150, 120, 80)),
    "seeker": dict(peau=(210, 170, 210), poils=(240, 230, 250)),
    "sabre_givre": dict(peau=(210, 220, 232), poils=(240, 244, 250)),
    "magmadroth": dict(ventre=(255, 120, 40)),
    "dragon": dict(ventre=(230, 170, 90)),
    "varghulf": dict(peau=(90, 70, 70), poils=(60, 50, 50)),
    "terrorgheist": dict(peau=(150, 140, 130), membrane=(110, 90, 90)),
}
for _e in TOUS:
    if _e["id"] in TEINTES:
        _e["spec"] = dict(_e["spec"], pal=dict(_e["spec"]["pal"], **TEINTES[_e["id"]]))
