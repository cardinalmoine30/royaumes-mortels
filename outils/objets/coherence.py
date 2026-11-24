# -*- coding: utf-8 -*-
"""Passe de cohérence sur le datapack (à relancer après toute reconstruction du datapack ; idempotente).

1. Une seule économie de matériaux : les anciennes « écailles » du datapack (Braise d'Aqshy, Cristal de Hysh, Malepierre…)
   deviennent les vrais objets du mod (éclats des Vents, malepierre, pierre des Royaumes brute) partout : butin des mobs,
   coffres, kits, recettes de la Forge des Royaumes, textes des menus.
2. Une seule forge pour les armes et armures : la Forge des Royaumes (table de forgeron) ne fabrique plus que consommables,
   talismans, lingots et sceaux. Armes et armures se forgent à la Forge de guerre. Ses recettes de faction restantes
   (arc de Hysh, fusil à aether, festin ogor…) sont réservées à leur faction.
3. Kits de serment et coffres : les anciennes pièces d'armure de faction sont remplacées par l'armure Soldat de l'arsenal.
Lancer : python3 outils/objets/coherence.py"""
import glob
import json
import os
import re

ICI = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(ICI, "..", "..", "src", "main", "resources", "data", "royaumes")

ECAILLES = {  # rm de l'ancienne écaille -> (objet du mod, ancien nom, nouveau nom)
    "malepierre": ("royaumes:malepierre", "Malepierre", "Malepierre"),
    "braise": ("royaumes:eclat_aqshy", "Braise d'Aqshy", "Éclat d'Aqshy"),
    "cristal": ("royaumes:eclat_hysh", "Cristal de Hysh", "Éclat d'Hysh"),
    "ombre": ("royaumes:eclat_ulgu", "Pierre-Ombre", "Éclat d'Ulgu"),
    "ambre": ("royaumes:eclat_ghur", "Ambre de Ghur", "Éclat de Ghur"),
    "graine": ("royaumes:eclat_ghyran", "Graine de Vie", "Éclat de Ghyran"),
    "ame": ("royaumes:eclat_shyish", "Fragment d'Âme", "Éclat de Shyish"),
    "ur_or": ("royaumes:eclat_chamon", "Ur-Or", "Éclat de Chamon"),
    "aether_or": ("royaumes:eclat_chamon", "Aether-Or", "Éclat de Chamon"),
    "sigmarite_brute": ("royaumes:eclat_azyr", "Sigmarite Brute", "Éclat d'Azyr"),
    "eclat": ("royaumes:pierre_royaumes_brute", "Éclat de Royaume", "Pierre des Royaumes brute"),
}
RETIREES = {  # recettes d'armes/armures de l'ancienne forge -> nom dans le menu
    "panoplie_sigmarite": "Panoplie de Sigmarite (Ordre)", "panoplie_fleau": "Armure du Fléau Noir (Chaos)",
    "panoplie_nadirite": "Armure de Nadirite (Mort)", "panoplie_ferraille": "Armure de Ferraille Ironjawz (Destruction)",
    "marteau_sigmar": "Marteau de Sigmar", "lame_demoniaque": "Lame Démoniaque", "faux_ame": "Faux des Âmes",
    "choppa_gork": "Choppa de Gork", "lame_malepierre": "Lame de Malepierre", "hache_ur_or": "Hache d'Ur-Or",
}
# recettes de faction restantes : (numéros rm_faction min, max, nom affiché)
RESERVEES = {"arc_hysh": (7, 7, "Lumineth"), "fusil_aether": (4, 4, "Kharadron"), "festin_ogor": (24, 24, "Ogors"),
             "talisman_grimnir": (3, 3, "Fyreslayers"), "elixir_malepierre": (15, 15, "Skaven"), "oeil_chaos": (10, 16, "Chaos"),
             "rune_sigmar": (1, 9, "Ordre")}
FACTIONS = ["", "stormcast", "cites", "fyreslayers", "kharadron", "khaine", "idoneth", "lumineth", "seraphon", "sylvaneth", "esclaves",
            "khorne", "tzeentch", "slaanesh", "nurgle", "skaven", "hashut", "nighthaunt", "soulblight", "ossiarch", "fec", "ironjawz",
            "kruleboyz", "gitz", "ogors", "behemat"]
PIECES = {"helmet": "casque", "chestplate": "torse", "leggings": "jambes", "boots": "bottes"}


def lire(p):
    return json.load(open(p, encoding="utf-8"))


def ecrire(p, o):
    with open(p, "w", encoding="utf-8") as f:
        json.dump(o, f, ensure_ascii=False, indent=2)
        f.write("\n")


def remplacer_textes(s):
    for _, (_, ancien, nouveau) in ECAILLES.items():
        if ancien != nouveau:
            s = s.replace(ancien, nouveau)
    return s


def mods(e):
    m = e.get("modifier", e.get("functions", []))
    return [m] if isinstance(m, dict) else list(m)


def composants(e):
    c = {}
    for m in mods(e):
        if m.get("type", m.get("function")) == "minecraft:set_components":
            c.update(m.get("components", {}))
    return c


def nettoyer(e, nouveau):
    """Remplace l'objet d'une entrée de butin et retire ses composants d'écaille (nom, description, données)."""
    e["name"] = nouveau
    garde = [m for m in mods(e) if m.get("type", m.get("function")) not in ("minecraft:set_components", "minecraft:set_name", "minecraft:set_lore")]
    cle = "modifier" if "modifier" in e else "functions"
    e.pop("modifier", None)
    e.pop("functions", None)
    if garde:
        e[cle] = garde


def armures_des_kits():
    """Nom des anciennes pièces d'armure de faction -> objet Soldat de l'arsenal."""
    table = {}
    for fid in FACTIONS[1:]:
        p = os.path.join(DATA, "loot_table", "kits", fid + ".json")
        if not os.path.exists(p):
            continue
        for pool in lire(p)["pools"]:
            for e in pool["entries"]:
                nom = e.get("name", "")
                piece = next((PIECES[k] for k in PIECES if nom.endswith("_" + k)), None)
                n = composants(e).get("minecraft:custom_name", {})
                if piece and isinstance(n, dict) and n.get("text"):
                    table[n["text"]] = "royaumes:%s_%s_soldat" % (fid, piece)
    return table


def butin(armures):
    n_ecailles = n_armures = 0
    for p in glob.glob(os.path.join(DATA, "loot_table", "**", "*.json"), recursive=True):
        j = lire(p)
        change = False

        def visiter(o):
            nonlocal change, n_ecailles, n_armures
            if isinstance(o, dict):
                if o.get("type") == "minecraft:item" and isinstance(o.get("name"), str):
                    c = composants(o)
                    rm = (c.get("minecraft:custom_data") or {}).get("rm") if isinstance(c.get("minecraft:custom_data"), dict) else None
                    nom = (c.get("minecraft:custom_name") or {}).get("text") if isinstance(c.get("minecraft:custom_name"), dict) else None
                    if o["name"] == "minecraft:armadillo_scute" and rm in ECAILLES:
                        nettoyer(o, ECAILLES[rm][0])
                        change, n_ecailles = True, n_ecailles + 1
                    elif nom in armures and any(o["name"].endswith("_" + k) for k in PIECES):
                        nettoyer(o, armures[nom])
                        change, n_armures = True, n_armures + 1
                for v in o.values():
                    visiter(v)
            elif isinstance(o, list):
                for v in o:
                    visiter(v)
        visiter(j)
        if change:
            ecrire(p, j)
    return n_ecailles, n_armures


def fonctions():
    motif = re.compile(r'id:"minecraft:armadillo_scute",components:\{"minecraft:custom_data":\{rm:"([a-z_]+)"\}\}')
    n = 0
    for p in glob.glob(os.path.join(DATA, "function", "**", "*.mcfunction"), recursive=True):
        s = open(p, encoding="utf-8").read()
        t = motif.sub(lambda m: 'id:"%s"' % ECAILLES[m.group(1)][0] if m.group(1) in ECAILLES else m.group(0), s)
        t = remplacer_textes(t)
        if t != s:
            open(p, "w", encoding="utf-8").write(t)
            n += 1
    return n


def forge():
    r = os.path.join(DATA, "function", "forge")
    for nom in RETIREES:
        for chemin in (os.path.join(r, "r", nom + ".mcfunction"), os.path.join(DATA, "loot_table", "forge", nom + ".json")):
            if os.path.exists(chemin):
                os.remove(chemin)
    for p in glob.glob(os.path.join(DATA, "function", "**", "*.mcfunction"), recursive=True):
        s = open(p, encoding="utf-8").read()
        t = "\n".join(l for l in s.split("\n") if not any("royaumes:forge/%s" % n in l and "forge/r/" not in l for n in RETIREES))
        if t != s:
            open(p, "w", encoding="utf-8").write(t)
    ess = os.path.join(r, "essayer.mcfunction")
    lignes = [l for l in open(ess, encoding="utf-8").read().splitlines() if not any("forge/r/%s " % n in l for n in RETIREES)]
    open(ess, "w", encoding="utf-8").write("\n".join(lignes) + "\n")
    for nom, (a, b, qui) in RESERVEES.items():
        p = os.path.join(r, "r", nom + ".mcfunction")
        if not os.path.exists(p):
            continue
        s = open(p, encoding="utf-8").read()
        verrou = "execute unless entity @p[distance=..8,scores={rm_faction=%d..%d}] run return 0" % (a, b)
        if verrou not in s:
            open(p, "w", encoding="utf-8").write(verrou + "\n" + s)
    # menu de la forge
    d = os.path.join(DATA, "dialog", "forge.json")
    j = lire(d)
    for corps in j.get("body", []):
        c = corps.get("contents")
        if not isinstance(c, list):
            continue
        neuf, saute = [], False
        for el in c:
            t = el.get("text", "") if isinstance(el, dict) else ""
            if t.startswith("• "):
                nom = t[2:]
                saute = nom in RETIREES.values()
                if not saute:
                    for k, (a, b, qui) in RESERVEES.items():
                        base = {"arc_hysh": "Arc de Lumière de Hysh", "fusil_aether": "Fusil à Aether", "festin_ogor": "Festin",
                                "talisman_grimnir": "Talisman de Grimnir", "elixir_malepierre": "Élixir de Malepierre",
                                "oeil_chaos": "Œil du Chaos", "rune_sigmar": "Rune de Sigmar"}[k]
                        if nom.startswith(base) and "réservé" not in nom:
                            el = dict(el, text=t + " [réservé : " + qui + "]")
                neuf.append(el)
                continue
            if saute:
                saute = False
                continue
            neuf.append(el)
        if neuf and isinstance(neuf[0], dict) and "Forge de guerre" not in neuf[0].get("text", ""):
            neuf.insert(0, {"text": "Armes et armures : à la Forge de guerre (bloc à fabriquer), qui n'ouvre que l'arsenal de ta faction "
                                    "et de ton alliance.\n", "color": "yellow"})
        # la touche « jeter » réelle du joueur au lieu d'un Q écrit en dur (claviers AZERTY : c'est A)
        for i, el in enumerate(neuf):
            if isinstance(el, dict) and "(touche Q)" in el.get("text", ""):
                avant, apres = el["text"].split("(touche Q)", 1)
                neuf[i] = dict(el, text=avant + "(touche ", extra=[{"keybind": "key.drop"}, {"text": ")" + apres}])
        corps["contents"] = neuf
    ecrire(d, j)


VANILLA_FR = {"arrow": "flèches", "bone block": "bloc d'os", "bone meal": "poudre d'os", "brown mushroom": "champignon brun",
              "cake": "gâteau", "coal": "charbon", "cooked cod": "morue cuite", "cooked mutton": "mouton cuit",
              "cooked porkchop": "côtelette cuite", "cookie": "cookie", "copper ingot": "lingot de cuivre", "emerald": "émeraudes",
              "ender pearl": "perle de l'Ender", "firework rocket": "fusée", "flint and steel": "briquet", "gold nugget": "pépites d'or",
              "honey bottle": "fiole de miel", "lapis lazuli": "lapis-lazuli", "oak sapling": "pousse de chêne",
              "red mushroom": "champignon rouge", "rotten flesh": "chair putréfiée", "soul lantern": "lanterne des âmes",
              "sweet berries": "baies sucrées", "bow": "arc", "crossbow": "arbalète", "glass bottle": "fioles", "gold ingot": "lingots d'or",
              "paper": "papier", "cooked beef": "bœuf cuit", "bread": "pain", "iron block": "bloc de fer", "gold block": "bloc d'or",
              "iron sword": "épée en fer", "netherite scrap": "débris de netherite", "diamond": "diamants"}


def vanilla_fr(s):
    """Les menus affichaient les identifiants anglais des objets vanilla (« 2 gold ingot ») : on les traduit."""
    for en in sorted(VANILLA_FR, key=len, reverse=True):
        s = re.sub(r"(?<=[ ,:0-9])" + re.escape(en) + r"(?=[,\\\n\"])", VANILLA_FR[en], s)
    return s


def textes():
    n = 0
    for p in glob.glob(os.path.join(DATA, "dialog", "**", "*.json"), recursive=True):
        s = open(p, encoding="utf-8").read()
        t = vanilla_fr(remplacer_textes(s))
        if t != s:
            open(p, "w", encoding="utf-8").write(t)
            n += 1
    return n


def textes_kits(armures):
    """Les menus de faction listaient les anciennes pièces : ils annoncent l'armure Soldat."""
    for p in glob.glob(os.path.join(DATA, "dialog", "faction", "*.json")):
        s = open(p, encoding="utf-8").read()
        t = s
        for ancien in armures:
            t = t.replace(ancien + ",", "").replace(", " + ancien, "").replace(ancien, "")
        if t != s:
            t = t.replace("Pierre de Royaume", "armure Soldat de faction, Pierre de Royaume", 1) if "armure Soldat" not in t else t
            t = re.sub(r",\s+armure Soldat", ", armure Soldat", t)
            open(p, "w", encoding="utf-8").write(t)


MINERAIS_GLOIRE = [("minerai_pierre_royaumes", 3), ("minerai_pierre_royaumes_profond", 3), ("minerai_azyrite", 6), ("minerai_braise", 6),
                   ("minerai_croc", 6), ("minerai_jade", 6), ("minerai_lumineux", 6), ("minerai_ombre", 6), ("minerai_ames", 6),
                   ("minerai_or_vif", 6), ("minerai_malepierre", 8)]


def gloire_minerais():
    """Les minerais du mod rapportent de la gloire comme les minerais vanilla (le datapack ne connaissait que ces derniers)."""
    load = os.path.join(DATA, "function", "rpg", "load.mcfunction")
    boucle = os.path.join(DATA, "function", "rpg", "boucle.mcfunction")
    l, b = open(load, encoding="utf-8").read(), open(boucle, encoding="utf-8").read()
    for i, (bloc, v) in enumerate(MINERAIS_GLOIRE):
        obj = "rm_mr%d" % i
        if obj + " " not in l:
            l = l.rstrip("\n") + "\nscoreboard objectives add %s minecraft.mined:royaumes.%s\n" % (obj, bloc)
        if '"%s"' % obj not in b:
            b = b.rstrip("\n") + '\nexecute as @a[scores={%s=1..}] run function royaumes:rpg/source {obj:"%s",val:%d}\n' % (obj, obj, v)
    open(load, "w", encoding="utf-8").write(l)
    open(boucle, "w", encoding="utf-8").write(b)


def main():
    gloire_minerais()
    armures = armures_des_kits()
    e, a = butin(armures)
    f = fonctions()
    forge()
    t = textes()
    textes_kits(armures)
    print("cohérence : %d écailles -> objets du mod, %d armures -> Soldat, %d fonctions, %d menus" % (e, a, f, t))


if __name__ == "__main__":
    main()
