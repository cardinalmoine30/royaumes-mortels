# -*- coding: utf-8 -*-
"""Annonce des biomes dans le tchat (et plus au milieu de l'écran) + relation du biome avec le joueur.

Chaque biome des Royaumes appartient à l'alliance qui y fait apparaître le plus de troupes (poids d'apparition des
mobs du bestiaire). En entrant dans un biome, le joueur reçoit une ligne dans le tchat :
  « ⛰ Forêts de Jade Sylvéa — Royaume de la Vie  ·  ⚑ Terre alliée » (ou « ⚔ Terre ennemie : Chaos »)
et le score rm_brel (1 alliée, 2 ennemie, 0 sans faction ou hors des Royaumes) alimente l'indicateur du HUD.
Usage : python3 outils/objets/biomes_tchat.py (relit les noms de biomes_titre.mcfunction, idempotent)."""
import collections, json, os, re, sys

ICI = os.path.dirname(os.path.abspath(__file__))
RACINE = os.path.join(ICI, "..", "..")
F = os.path.join(RACINE, "src/main/resources/data/royaumes/function/monde")
sys.path.insert(0, os.path.join(RACINE, "outils/modeles"))
from bestiaire import TOUS, FAC  # noqa: E402

NOMS_ALLIANCES = {"ordre": ("Ordre", "aqua"), "chaos": ("Chaos", "red"), "mort": ("Mort", "dark_purple"),
                  "destruction": ("Destruction", "green")}
ALLIANCE_NUM = {"ordre": (1, 9), "chaos": (10, 16), "mort": (17, 20), "destruction": (21, 25)}


def biomes_ids():
    ids = {}
    for l in open(os.path.join(F, "biome_joueur.mcfunction")):
        m = re.search(r"royaumes:(\w+) run scoreboard players set @s rm_bnow (\d+)", l)
        if m:
            ids[int(m.group(2))] = m.group(1)
    return ids


def noms():
    """Noms et sous-titres : depuis biomes_noms.json (créé au premier passage à partir des anciens titres)."""
    p = os.path.join(ICI, "biomes_noms.json")
    if os.path.exists(p):
        return {int(k): v for k, v in json.load(open(p)).items()}
    d = collections.defaultdict(dict)
    for l in open(os.path.join(F, "biome_titre.mcfunction")):
        m = re.search(r"rm_bnow matches (\d+) run title @s (title|subtitle) (\{.*\})$", l.strip())
        if m:
            d[int(m.group(1))][m.group(2)] = json.loads(m.group(3))
    json.dump(d, open(p, "w"), ensure_ascii=False, indent=1)
    return dict(d)


def maitres():
    poids = collections.defaultdict(collections.Counter)
    for e in TOUS:
        for b in e["biomes"]:
            poids[b][FAC[e["fac"]][0]] += e["poids"]
    return {b: c.most_common(1)[0][0] for b, c in poids.items()}


def main():
    ids, nm, mt = biomes_ids(), noms(), maitres()
    L = ["scoreboard players operation @s rm_biome = @s rm_bnow",
         "scoreboard players set @s rm_brel 0"]
    for n, b in sorted(ids.items()):
        al = mt.get(b)
        if not al:
            continue
        lo, hi = ALLIANCE_NUM[al]
        L.append(f"execute if score @s rm_bnow matches {n} if score @s rm_faction matches 1.. run scoreboard players set @s rm_brel 2")
        L.append(f"execute if score @s rm_bnow matches {n} if score @s rm_faction matches {lo}..{hi} run scoreboard players set @s rm_brel 1")
    for n, b in sorted(ids.items()):
        t = nm.get(n, {})
        titre = t.get("title", {"text": b, "color": "white"})
        sous = t.get("subtitle", {"text": ""})
        al = mt.get(b)
        nom_al, coul_al = NOMS_ALLIANCES.get(al, ("?", "gray"))
        base = [{"text": "⛰ ", "color": "gold"}, {"text": titre["text"], "color": titre.get("color", "white"), "bold": True}]
        if sous.get("text"):
            base.append({"text": " — " + sous["text"], "color": "gray", "italic": True})
        allie = base + [{"text": "   ⚑ Terre alliée", "color": "green", "bold": True},
                        {"text": f" (tenue par l'{nom_al})" if nom_al == "Ordre" else f" (tenue par la {nom_al})" if nom_al in ("Mort", "Destruction") else f" (tenue par le {nom_al})", "color": "dark_green"}]
        ennemi = base + [{"text": "   ⚔ Terre ennemie", "color": "red", "bold": True},
                         {"text": f" : {nom_al}", "color": coul_al}]
        neutre = base + [{"text": f"   Terre de l'alliance : {nom_al}", "color": coul_al}]
        for rel, msg in ((1, allie), (2, ennemi), (0, neutre)):
            L.append(f"execute if score @s rm_bnow matches {n} if score @s rm_brel matches {rel} run tellraw @s "
                     + json.dumps(msg, ensure_ascii=False))
    L.append("execute if score @s rm_brel matches 2 run playsound minecraft:block.note_block.bass player @s ~ ~ ~ 0.6 0.6")
    L.append("execute if score @s rm_brel matches 1 run playsound minecraft:block.note_block.bell player @s ~ ~ ~ 0.4 1.4")
    open(os.path.join(F, "biome_titre.mcfunction"), "w").write("\n".join(L) + "\n")
    # hors des Royaumes : plus d'indicateur
    p = os.path.join(RACINE, "src/main/resources/data/royaumes/function/boucle_seconde.mcfunction")
    s = open(p).read()
    for d in ("overworld", "the_nether"):
        old = f"execute as @a at @s if dimension minecraft:{d} run scoreboard players set @s rm_biome 0\n"
        new = old + f"execute as @a at @s if dimension minecraft:{d} run scoreboard players set @s rm_brel 0\n"
        if old in s and new not in s:
            s = s.replace(old, new)
    open(p, "w").write(s)
    p = os.path.join(RACINE, "src/main/resources/data/royaumes/function/load.mcfunction")
    s = open(p).read()
    if "rm_brel" not in s:
        s = s.replace("scoreboard objectives add rm_biome dummy\n", "scoreboard objectives add rm_biome dummy\nscoreboard objectives add rm_brel dummy\n")
    open(p, "w").write(s)
    print("biomes : %d annoncés dans le tchat" % len(ids))


if __name__ == "__main__":
    main()
