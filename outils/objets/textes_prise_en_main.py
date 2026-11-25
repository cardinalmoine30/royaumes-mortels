# -*- coding: utf-8 -*-
"""Textes de prise en main (0.23) : fiches de faction (équipement de départ réel) et Codex à jour.
Usage : python3 outils/objets/textes_prise_en_main.py (idempotent)."""
import glob, json, os, re

ICI = os.path.dirname(os.path.abspath(__file__))
D = os.path.join(ICI, "..", "..", "src/main/resources/data/royaumes")


def nom_arme(fid):
    d = json.load(open(os.path.join(D, "loot_table/kits", fid + ".json")))
    e = d["pools"][0]["entries"][0]
    for m in e.get("modifier", []):
        n = m.get("components", {}).get("minecraft:custom_name", {}).get("text")
        if n:
            return n
    return e["name"].split(":")[1].replace("_", " ")


def remplacer(x, f):
    if isinstance(x, dict):
        return {k: remplacer(v, f) for k, v in x.items()}
    if isinstance(x, list):
        return [remplacer(v, f) for v in x]
    return f(x) if isinstance(x, str) else x


def main():
    n = 0
    for p in sorted(glob.glob(os.path.join(D, "dialog/faction/*.json"))):
        fid = os.path.basename(p)[:-5]
        if not os.path.exists(os.path.join(D, "loot_table/kits", fid + ".json")):
            continue
        d = json.load(open(p))
        arme = nom_arme(fid)
        txt = f"{arme} (niveau fer), vivres et Pierre de Royaume. Armure : à forger (Forge de guerre)."
        corps = d["body"][0]["contents"]
        for i, c in enumerate(corps):
            if isinstance(c, dict) and c.get("text") == "Équipement : " and i + 1 < len(corps):
                corps[i + 1]["text"] = txt
                n += 1
        json.dump(d, open(p, "w"), ensure_ascii=False)
    p = os.path.join(D, "dialog/codex.json")
    d = json.load(open(p))

    def maj(t):
        t = t.replace("Commande : /trigger rm_rpg", "Dépense-les avec les boutons + du Carnet du Héros (inventaire, à gauche) ; "
                      "l'onglet Héros ouvre ta voie (Guerrier, Mage, Éclaireur)")
        t = t.replace("La Corne d'appel (clic droit) fait venir", "La Corne d'appel (offerte quand tu plantes ton camp ; clic droit) fait venir")
        return t
    d = remplacer(d, maj)
    json.dump(d, open(p, "w"), ensure_ascii=False)
    print("fiches de faction : %d mises à jour ; Codex à jour" % n)


if __name__ == "__main__":
    main()
