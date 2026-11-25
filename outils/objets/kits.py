# -*- coding: utf-8 -*-
"""Kits de départ (0.23) : au serment, le héros ne reçoit que
- son arme de faction, ramenée au plus au niveau d'une arme en fer (dégâts ≤ hache en fer, dégâts par seconde ≤ épée
  en fer), sans enchantement vanilla (l'enchantement de faction reste, au niveau 1) ;
- de la nourriture (12 pains, 6 steaks) ;
- la Pierre de Royaume (le cristal pour voyager vers les Royaumes Mortels).
Armure, bouclier et Corne d'appel se gagnent ensuite (forge, tutoriel). Usage : python3 outils/objets/kits.py"""
import glob, json, os

ICI = os.path.dirname(os.path.abspath(__file__))
KITS = os.path.join(ICI, "..", "..", "src/main/resources/data/royaumes/loot_table/kits")
EPEE_FER_DPS = 6 * 1.6      # 9,6
HACHE_FER = 9.0


def composants(e):
    c = {}
    for m in e.get("functions", e.get("modifier", [])):
        c.update(m.get("components", {}))
    return c


def borner(e):
    fs = e.get("functions", e.get("modifier", []))
    for m in fs:
        comp = m.get("components", {})
        ench = comp.get("minecraft:enchantments")
        if ench:
            garde = {k: 1 for k in ench if not k.startswith("minecraft:")}
            if garde:
                comp["minecraft:enchantments"] = garde
            else:
                del comp["minecraft:enchantments"]
        am = comp.get("minecraft:attribute_modifiers")
        if am is None and e["name"] == "minecraft:trident":
            am = comp["minecraft:attribute_modifiers"] = [
                {"type": "minecraft:attack_damage", "amount": 8.0, "id": "minecraft:base_attack_damage", "operation": "add_value", "slot": "mainhand"},
                {"type": "minecraft:attack_speed", "amount": -2.9, "id": "minecraft:base_attack_speed", "operation": "add_value", "slot": "mainhand"}]
        if am:
            vit = 4.0 + sum(a["amount"] for a in am if a["type"] == "minecraft:attack_speed")
            for a in am:
                if a["type"] == "minecraft:attack_damage":
                    plafond = min(HACHE_FER, EPEE_FER_DPS / max(0.5, vit)) - 1
                    a["amount"] = round(min(a["amount"], plafond), 1)
        lore = comp.get("minecraft:lore")
        if lore is not None:
            comp["minecraft:lore"] = [l for l in lore if "Arme de départ" not in json.dumps(l, ensure_ascii=False)] + [
                {"text": "Arme de départ (niveau fer).", "color": "dark_gray", "italic": True}]


def main():
    n = 0
    for p in sorted(glob.glob(os.path.join(KITS, "*.json"))):
        d = json.load(open(p))
        entrees = [e for pool in d["pools"] for e in pool["entries"]]
        arme, pierre = entrees[0], None
        for e in entrees:
            if composants(e).get("minecraft:custom_name", {}).get("text") == "Pierre de Royaume":
                pierre = e
        borner(arme)
        vivres = [{"type": "minecraft:item", "name": "minecraft:bread", "modifier": [{"type": "minecraft:set_count", "count": 12}]},
                  {"type": "minecraft:item", "name": "minecraft:cooked_beef", "modifier": [{"type": "minecraft:set_count", "count": 6}]}]
        d["pools"] = [{"rolls": 1, "entries": [e]} for e in [arme] + vivres + ([pierre] if pierre else [])]
        json.dump(d, open(p, "w"), ensure_ascii=False, indent=1)
        n += 1
    print("kits de départ : %d réécrits" % n)


if __name__ == "__main__":
    main()
