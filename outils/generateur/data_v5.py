# -*- coding: utf-8 -*-
"""v5 : un monde par Royaume, biomes et structures fidèles au lore, plus de monstres vanilla.
La dimension principale royaumes:royaumes_mortels devient Azyr (Royaume des Cieux)."""
import copy
from data_monde import BIOMES, STRUCTURES, SPAWN_MONSTRES
import data_v4
import decors
from structures4 import DECOS4

_par_id = {b["id"]: b for b in BIOMES}


def cloner(src, **kw):
    b = copy.deepcopy(_par_id[src])
    b.update(kw)
    b.pop("special", None) if "special" not in kw else None
    BIOMES.append(b)
    _par_id[b["id"]] = b
    # mêmes décors que la source
    for table in (decors.DECOS, DECOS4):
        for did, (fn, bl, ch) in list(table.items()):
            if src in bl and b["id"] not in bl:
                bl.append(b["id"])
    return b


# --- Nouveaux biomes pour que chaque Royaume en ait au moins deux ---
cloner("ghyran_jade", id="azyr_vallees", nom="Vallées d'Azyrheim", sous="Royaume des Cieux — terres de Sigmar", c="aqua",
       base="meadow", ciel="#4a8aff", brume="#a8c8ff", herbe="#7ac0a0", feuilles="#6ab0c0", weird=(-1.0, 1.0),
       particules=[("minecraft:electric_spark", 0.002)])
cloner("ghur_terres", id="ghur_savane", nom="Plaines des Mégafaunes", sous="Royaume des Bêtes — terrains de chasse des Ogors",
       base="savanna_plateau", ciel="#e09048", herbe="#c0a038")
cloner("chamon_desert", id="chamon_collines", nom="Collines de Métal de Chamon", sous="Royaume du Métal — mines des Kharadron",
       base="badlands", ciel="#c8c8d8", brume="#a8a8b8", herbe="#a0a0a8", feuilles="#909098",
       surface={"top": [("minecraft:smooth_basalt", None), ("minecraft:raw_iron_block", (0.55, 0.6)), ("minecraft:tuff", (-0.3, 0.1))],
                "under": "minecraft:deepslate"})
cloner("chamon_desert", id="shyish_sables", nom="Sables d'Améthyste de Shyish", sous="Royaume de la Mort — déserts des Ossiarch",
       base="desert", ciel="#5a4a7a", brume="#3a2a5a", herbe="#7a6a8a", feuilles="#6a5a7a",
       particules=[("minecraft:soul", 0.002), ("minecraft:white_ash", 0.01)],
       surface={"top": [("minecraft:sand", None), ("minecraft:amethyst_block", (0.6, 0.65)), ("minecraft:bone_block", (-0.7, -0.65))],
                "under": "minecraft:sandstone"})
_par_id["hysh_plateaux"]["special"] = None

# Noms des biomes déplacés
_par_id["ghur_jungle"].update(nom="Jungles de Ghyran", sous="Royaume de la Vie — cités-temples des Seraphon")

# --- Un monde par Royaume ---
AZYR = ["azyr_cimes", "azyr_vallees"]       # dimension principale royaumes:royaumes_mortels
data_v4.DIMENSIONS.clear()
data_v4.DIMENSIONS.update({
    "ghyran": dict(nom="Ghyran, Royaume de la Vie", c="green",
                   biomes=["ghyran_jade", "ghyran_wyldwood", "ghyran_marais", "ghur_jungle"]),
    "aqshy": dict(nom="Aqshy, Royaume du Feu", c="gold", biomes=["aqshy_cendres", "aqshy_volcans"]),
    "shyish": dict(nom="Shyish, Royaume de la Mort", c="dark_purple", biomes=["shyish_terres", "shyish_sables"]),
    "ghur": dict(nom="Ghur, Royaume des Bêtes", c="gold", biomes=["ghur_terres", "ghur_savane"]),
    "chamon": dict(nom="Chamon, Royaume du Métal", c="gray", biomes=["chamon_desert", "chamon_collines"]),
    "ulgu": dict(nom="Ulgu, Royaume des Ombres", c="dark_gray", biomes=["ulgu_brumes", "ulgu_marais_lune", "ulgu_mer"]),
    "hysh": dict(nom="Hysh, Royaume de la Lumière", c="white", biomes=["hysh_iles", "hysh_plateaux"], flottant=True),
    "huit_points": dict(nom="Les Huit-Points du Chaos", c="dark_red", biomes=["chaos_desolation", "terres_rongees"]),
})

# --- Structures fidèles au lore ---
LORE = {
    "forteresse_stormcast": ["azyr_cimes"],                 # uniquement au sommet des montagnes d'Azyr
    "cite_sigmar": ["azyr_vallees"],
    "temple_seraphon": ["ghur_jungle"],
    "bosquet_sylvaneth": ["ghyran_wyldwood", "ghyran_jade"],
    "fort_kruleboyz": ["ghyran_marais"],
    "jardin_rotigus": ["ghyran_marais"],                    # Nurgle convoite Ghyran
    "magmahold": ["aqshy_volcans"],
    "autel_skarbrand": ["aqshy_cendres"],
    "ziggurat_hashut": ["aqshy_cendres", "aqshy_volcans"],
    "chateau_soulblight": ["shyish_terres"],
    "cimetiere_nighthaunt": ["shyish_terres"],
    "necropole_nagash": ["shyish_terres"],
    "ossuaire_ossiarch": ["shyish_sables"],
    "camp_orruk": ["ghur_terres"],
    "arene_gordrakk": ["ghur_terres"],
    "campement_ogor": ["ghur_savane"],
    "port_kharadron": ["chamon_collines", "chamon_desert"],
    "temple_khaine": ["ulgu_brumes"],
    "ruines_idoneth": ["ulgu_mer"],
    "antre_gitz": ["ulgu_marais_lune"],
    "sanctuaire_lumineth": ["hysh_iles", "hysh_plateaux"],
    "citadelle_chaos": ["chaos_desolation"],
    "trone_archaon": ["chaos_desolation"],
    "repaire_skaven": ["terres_rongees"],
    "repaire_skavenblight": ["terres_rongees"],
    "tour_thanquol": ["terres_rongees"],
}
for st in STRUCTURES:
    if st["id"] in LORE:
        st["biomes"] = list(LORE[st["id"]])
    if st["id"] == "portail":
        st["biomes"] = sorted({b["id"] for b in BIOMES if b["id"] != "ulgu_mer"})

# --- Plus aucun monstre vanilla dans les Royaumes (les mobs du mod les remplacent) ---
for b in BIOMES:
    SPAWN_MONSTRES[b["id"]] = []
    b["mobs"] = {}

# --- Îles de Hysh : moins nombreuses mais bien plus grandes ---
HYSH_XZ_SCALE = 0.1          # vanilla 0.25 → îles ~2,5× plus larges, ~6× moins nombreuses
if "ilot_flottant" in data_v4.FLOTTANTS:
    fn, bl, ch = data_v4.FLOTTANTS["ilot_flottant"]
    data_v4.FLOTTANTS["ilot_flottant"] = (fn, bl, max(ch * 3, 24) if isinstance(ch, int) else ch)

# --- Apparence de faction : armure complète aux couleurs de la classe choisie ---
from data_factions import FACTIONS
APPARENCE = {  # faction -> (armure, détails, accent)
    "stormcast": ((204, 158, 52), (40, 66, 150), (120, 220, 255)), "cites": ((150, 150, 160), (40, 70, 150), (230, 190, 70)),
    "fyreslayers": ((200, 120, 60), (230, 180, 60), (255, 120, 30)), "kharadron": ((60, 110, 140), (200, 170, 70), (120, 230, 255)),
    "khaine": ((60, 20, 30), (200, 170, 90), (255, 40, 60)), "idoneth": ((40, 90, 110), (220, 210, 190), (120, 255, 230)),
    "lumineth": ((235, 235, 240), (210, 180, 90), (255, 250, 200)), "seraphon": ((40, 120, 140), (210, 170, 60), (255, 230, 90)),
    "sylvaneth": ((110, 80, 50), (120, 160, 60), (150, 255, 90)), "esclaves": ((60, 60, 66), (170, 140, 60), (230, 60, 40)),
    "khorne": ((150, 30, 26), (190, 160, 70), (255, 80, 40)), "tzeentch": ((50, 90, 170), (220, 180, 60), (120, 230, 255)),
    "slaanesh": ((170, 110, 180), (220, 210, 230), (255, 120, 220)), "nurgle": ((110, 120, 60), (150, 120, 60), (190, 230, 60)),
    "skaven": ((80, 66, 50), (120, 110, 90), (80, 255, 60)), "hashut": ((40, 40, 44), (190, 140, 60), (255, 110, 30)),
    "nighthaunt": ((60, 140, 130), (140, 200, 190), (160, 255, 230)), "soulblight": ((40, 40, 50), (180, 30, 40), (255, 40, 50)),
    "ossiarch": ((225, 215, 190), (60, 50, 80), (120, 230, 255)), "fec": ((150, 150, 140), (120, 60, 50), (220, 60, 60)),
    "ironjawz": ((90, 90, 96), (230, 200, 40), (255, 200, 40)), "kruleboyz": ((60, 70, 50), (150, 120, 70), (200, 255, 80)),
    "gitz": ((40, 40, 50), (220, 210, 120), (230, 220, 120)), "ogors": ((120, 100, 80), (200, 160, 60), (255, 200, 60)),
    "behemat": ((120, 90, 60), (160, 120, 70), (255, 200, 60)),
}
NOMS_PIECES = {"helmet": "Heaume", "chestplate": "Cuirasse", "leggings": "Jambières", "boots": "Bottes"}
for f in FACTIONS:
    garde = [o for o in f["kit"] if not any(o["id"].endswith(p) for p in NOMS_PIECES)]
    anciennes = {o["id"].rsplit("_", 1)[1]: o for o in f["kit"] if any(o["id"].endswith(p) for p in NOMS_PIECES)}
    for piece, nom in NOMS_PIECES.items():
        a = anciennes.get(piece, {})
        mat = a["id"].split(":")[1].rsplit("_", 1)[0] if a else "chainmail"
        if mat in ("leather", "turtle"):
            mat = "chainmail"
        garde.append({"id": f"minecraft:{mat}_{piece}", "nom": a.get("nom", f"{nom} — {f['nom']}"), "c": f["couleur"],
                      "lore": a.get("lore", []) + ["Apparence de faction"], "ench": a.get("ench", {}), "apparence": f["id"]})
    f["kit"] = garde
