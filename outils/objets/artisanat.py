# -*- coding: utf-8 -*-
"""Hub d'artisanat (0.23) : toutes les recettes du mod, lues dans le datapack, pour l'écran client EcranArtisanat.

Sources :
- function/forge/r/*.mcfunction : rituels de la Table de forgeron (on lâche les ingrédients dessus) ;
  ingrédients et quantités, réservation d'alliance ou de faction, objet obtenu (loot_table/forge/*.json) ;
- recipe/*.json : recettes d'établi du mod (bâtons, blocs, étendard, forge de guerre, yeux de seigneur…).
Sorties : src/main/java/fr/royaumes/ArtisanatGenere.java et dialog/forge.json (liste texte réécrite, sans entrées vides).
Les objets du datapack (base vanilla + item_model) sont codés « id@modèle@Nom » pour que le client les dessine et les
reconnaisse dans l'inventaire. Usage : python3 outils/objets/artisanat.py"""
import glob, json, os, re

ICI = os.path.dirname(os.path.abspath(__file__))
R = os.path.join(ICI, "..", "..", "src", "main", "resources")
D = os.path.join(R, "data", "royaumes")
LANG = json.load(open(os.path.join(R, "assets", "royaumes", "lang", "fr_fr.json")))
FACTIONS = [f["nom"] for f in json.load(open(os.path.join(ICI, "..", "donnees_factions.json")))]
ALLIANCES = {(1, 9): "Ordre", (10, 16): "Chaos", (17, 20): "Mort", (21, 25): "Destruction"}
TAGS = {"#minecraft:banners": "minecraft:white_banner"}


def modeles_dp():
    """custom_data rm -> (id de base, item_model, nom) relevés dans toutes les tables de butin."""
    m = {}

    def parcourir(x):
        if isinstance(x, dict):
            if x.get("type") == "minecraft:item" and "name" in x:
                comp = {}
                mods = x.get("modifier", [])
                for f in mods if isinstance(mods, list) else []:
                    if isinstance(f, dict):
                        comp.update(f.get("components", {}))
                rm = comp.get("minecraft:custom_data", {}).get("rm")
                if rm and "minecraft:item_model" in comp and rm not in m:
                    m[rm] = (x["name"], comp["minecraft:item_model"], comp.get("minecraft:custom_name", {}).get("text", rm))
            for v in x.values():
                parcourir(v)
        elif isinstance(x, list):
            for v in x:
                parcourir(v)
    for p in glob.glob(os.path.join(D, "loot_table", "**", "*.json"), recursive=True):
        parcourir(json.load(open(p)))
    return m


def resultat_forge(nom):
    d = json.load(open(os.path.join(D, "loot_table", "forge", nom + ".json")))
    e = d["pools"][0]["entries"][0]
    n, comp = 1, {}
    for f in e.get("modifier", []):
        comp.update(f.get("components", {}))
        if f.get("type") == "minecraft:set_count":
            n = int(f["count"]) if isinstance(f["count"], (int, float)) else 1
    modele = comp.get("minecraft:item_model", "")
    nom_aff = comp.get("minecraft:custom_name", {}).get("text") or ""
    return e["name"], modele, nom_aff, n


CATEGORIES = [
    ("Matériaux", ("lingot_de_sigmarite", "cristal_arcanique", "pierre_royaumes_brute", "bloc_pierre_royaumes")),
    ("Voyage et gloire", ("pierre_de_royaume", "parchemin_de_gloire")),
    ("Armes", ("arc_", "fusil", "marteau_tempete")),
    ("Élixirs et vivres", ("elixir", "tonique", "brume_d_ulgu", "lumiere_de_hysh", "festin")),
    ("Talismans", ("amulette", "comete", "coeur_de", "pendentif", "talisman", "rune", "oeil_des_dieux")),
    ("Magie", ("baton_", "grimoire")),
    ("Camp, forge et autels", ("etendard", "forge_de_guerre", "autel", "portail")),
    ("Yeux de seigneur", ("oeil_",)),
    ("Sceaux de seigneur", ("sceau", "totem", "crane_de", "cloche", "calice")),
]


def categorie(cle):
    base = cle.split("/")[-1].split(":")[-1]
    for cat, mots in CATEGORIES:
        if any(base.startswith(mt) or ("_" + mt) in base for mt in mots):
            return cat
    return "Blocs des Royaumes"


def forge(dp):
    out = []
    for p in sorted(glob.glob(os.path.join(D, "function", "forge", "r", "*.mcfunction"))):
        t = open(p).read()
        ings, cur = [], None
        for l in t.split("\n"):
            m = re.match(r'execute unless entity @e\[type=minecraft:item,distance=\.\.1\.5,nbt=\{Item:\{id:"([^"]+)"(?:,components:\{"minecraft:custom_data":\{rm:"(\w+)"\}\})?\}\}', l)
            if m:
                cur = (m.group(1), m.group(2))
            m = re.match(r"execute if score #c rm_tmp matches \.\.(\d+) run return 0", l)
            if m and cur:
                ings.append((cur, int(m.group(1)) + 1))
                cur = None
        res = re.search(r"faction=(\d+)\.\.(\d+)\}", t) or re.search(r"rm_faction=(\d+)\}", t)
        reserve = ""
        m = re.search(r"scores=\{rm_faction=(\d+)\.\.(\d+)\}", t)
        if m:
            reserve = ALLIANCES.get((int(m.group(1)), int(m.group(2))), "")
        m = re.search(r"scores=\{rm_faction=(\d+)\}\}", t)
        if m:
            reserve = FACTIONS[int(m.group(1)) - 1]
        nom = os.path.basename(p)[:-11]
        rid, modele, nom_aff, n = resultat_forge(nom)
        m = re.search(r'"⚒ Forgé : "[^]]*?\{"text": "([^"]+)"', t)
        if m:
            nom_aff = m.group(1)
        nom_aff = nom_aff.replace("Cœur de Éclat d'Hysh", "Cœur de Hysh")
        if nom == "raffinage":
            nom_aff = "Lingot de Sigmarite (raffinage d'éclats d'Azyr)"
        ing_codes = []
        for (iid, rm), q in ings:
            if rm and rm in dp:
                base, mod, nm = dp[rm]
                ing_codes.append((f"{base}@{mod}@{nm}", q))
            else:
                ing_codes.append((iid, q))
        out.append(dict(nom=nom_aff, station="forgeron", res=rid + (f"@{modele}@{nom_aff}" if modele else ""), n=n,
                        ings=ing_codes, reserve=reserve, cat=categorie(modele or rid), cle=nom))
    return out


def etabli():
    out = []
    for p in sorted(glob.glob(os.path.join(D, "recipe", "*.json"))):
        d = json.load(open(p))
        cpt = {}
        if d["type"] == "minecraft:crafting_shaped":
            for ligne in d["pattern"]:
                for ch in ligne:
                    if ch != " ":
                        k = d["key"][ch]
                        k = k if isinstance(k, str) else k[0] if isinstance(k, list) else k.get("item", "?")
                        cpt[k] = cpt.get(k, 0) + 1
        else:
            for k in d["ingredients"]:
                k = k if isinstance(k, str) else k[0] if isinstance(k, list) else k.get("item", "?")
                cpt[k] = cpt.get(k, 0) + 1
        rid = d["result"]["id"]
        comp = d["result"].get("components", {})
        nom = (comp.get("minecraft:custom_name", {}).get("text") or LANG.get("item.royaumes." + rid.split(":")[1])
               or LANG.get("block.royaumes." + rid.split(":")[1]) or rid)
        if comp.get("minecraft:item_model"):
            rid = f"{rid}@{comp['minecraft:item_model']}@{nom}"
        ings = [(TAGS.get(k, k), q) for k, q in cpt.items()]
        cle = os.path.basename(p)[:-5]
        out.append(dict(nom=nom, station="etabli", res=rid, n=d["result"].get("count", 1), ings=ings, reserve="", cat=categorie(cle), cle=cle))
    return out


def jstr(s):
    return '"' + s.replace("\\", "\\\\").replace('"', '\\"') + '"'


def java(rs):
    L = ["package fr.royaumes;", "", "/** FICHIER GÉNÉRÉ par outils/objets/artisanat.py : ne pas modifier à la main. */",
         "public final class ArtisanatGenere {", "    private ArtisanatGenere() {}", ""]
    L.append("    /** Nom affiché, poste (forgeron = Table de forgeron, etabli = établi), catégorie, réservation. */")
    L.append("    public static final String[] NOMS = {" + ", ".join(jstr(r["nom"]) for r in rs) + "};")
    L.append("    public static final String[] POSTES = {" + ", ".join(jstr(r["station"]) for r in rs) + "};")
    L.append("    public static final String[] CATEGORIES = {" + ", ".join(jstr(r["cat"]) for r in rs) + "};")
    L.append("    public static final String[] RESERVES = {" + ", ".join(jstr(r["reserve"]) for r in rs) + "};")
    L.append("    /** Objet obtenu : « id » ou « id@item_model@Nom » pour les objets du datapack. */")
    L.append("    public static final String[] RESULTATS = {" + ", ".join(jstr(r["res"]) for r in rs) + "};")
    L.append("    public static final int[] QUANTITES = {" + ", ".join(str(r["n"]) for r in rs) + "};")
    L.append("    public static final String[][] INGREDIENTS = {" + ", ".join("{" + ", ".join(jstr(i) for i, _ in r["ings"]) + "}" for r in rs) + "};")
    L.append("    public static final int[][] NOMBRES = {" + ", ".join("{" + ", ".join(str(q) for _, q in r["ings"]) + "}" for r in rs) + "};")
    L.append("}")
    return "\n".join(L) + "\n"


def dialogue(rs):
    """Liste texte de la Table de forgeron (commande /trigger rm_forge), réécrite sans entrées vides."""
    p = os.path.join(D, "dialog", "forge.json")
    d = json.load(open(p))
    corps = [{"text": "Le hub d'artisanat illustré : onglet Forge de l'inventaire (icônes, ce qu'il te manque).\n", "color": "yellow"},
             {"text": "Table de forgeron : pose-la, puis lâche dessus (touche ", "color": "gray",
              "extra": [{"keybind": "key.drop"}, {"text": ") les ingrédients ; ils fusionnent seuls.\n\n"}]}]
    for r in rs:
        if r["station"] != "forgeron":
            continue
        ing = ", ".join(f"{q} {i.split('@')[2] if '@' in i else (LANG.get('item.' + i.replace(':', '.')) or i.split(':')[1].replace('_', ' '))}" for i, q in r["ings"])
        corps.append({"text": "• " + r["nom"] + (f" [réservé : {r['reserve']}]" if r["reserve"] else ""), "color": "gold"})
        corps.append({"text": " : " + ing + "\n", "color": "white"})
    d["body"][0]["contents"] = corps
    json.dump(d, open(p, "w"), ensure_ascii=False)


def main():
    rs = forge(modeles_dp()) + etabli()
    ordre = [c for c, _ in CATEGORIES] + ["Blocs des Royaumes"]
    rs.sort(key=lambda r: (ordre.index(r["cat"]) if r["cat"] in ordre else 99, r["nom"]))
    vus, uniques = set(), []
    for r in rs:                                   # pas de doublon (même objet, même poste)
        k = (r["cle"], r["station"])
        if k not in vus:
            vus.add(k)
            uniques.append(r)
    open(os.path.join(R, "..", "java", "fr", "royaumes", "ArtisanatGenere.java"), "w").write(java(uniques))
    dialogue(uniques)
    print("artisanat : %d recettes (%d forgeron, %d établi)" % (len(uniques), sum(r["station"] == "forgeron" for r in uniques),
                                                              sum(r["station"] == "etabli" for r in uniques)))
    for r in uniques:
        print("  ", r["cat"], "|", r["nom"], "|", r["station"], "|", r["res"][:60], "|", r["ings"], r["reserve"])


if __name__ == "__main__":
    main()
