# -*- coding: utf-8 -*-
"""Onglet de progrès « Saga des Royaumes » : guide le joueur à travers le mod.
Les critères « impossible » sont accordés par le mod (serment, premier sort, première capacité)."""
import json
import os
import shutil

ICI = os.path.dirname(os.path.abspath(__file__))
DOSSIER = os.path.join(ICI, "..", "..", "src", "main", "resources", "data", "royaumes", "advancement", "saga")
VENTS = ["azyr", "aqshy", "ghur", "ghyran", "hysh", "ulgu", "shyish", "chamon"]
NOMS = {"azyr": "Azyr", "aqshy": "Aqshy", "ghur": "Ghur", "ghyran": "Ghyran", "hysh": "Hysh", "ulgu": "Ulgu", "shyish": "Shyish", "chamon": "Chamon"}
DIMS = {"azyr": "royaumes:royaumes_mortels", "aqshy": "royaumes:aqshy", "ghur": "royaumes:ghur", "ghyran": "royaumes:ghyran",
        "hysh": "royaumes:hysh", "ulgu": "royaumes:ulgu", "shyish": "royaumes:shyish", "chamon": "royaumes:chamon"}
DESC_ROYAUMES = {"azyr": "Gagner Azyr, le Royaume des Cieux.", "aqshy": "Fouler les cendres d'Aqshy, le Royaume du Feu.",
                 "ghur": "Survivre à Ghur, le Royaume des Bêtes.", "ghyran": "Entrer dans Ghyran, le Royaume de la Vie.",
                 "hysh": "Voir la lumière de Hysh, le Royaume de la Lumière.", "ulgu": "Se perdre dans les brumes d'Ulgu, le Royaume des Ombres.",
                 "shyish": "Descendre en Shyish, le Royaume de la Mort.", "chamon": "Contempler l'or vif de Chamon, le Royaume des Métaux."}
BOSS = [("nagash", "Le Grand Nécromancien", "Vaincre Nagash, Dieu suprême de la Mort."),
        ("archaon", "L'Élu Éternel", "Vaincre Archaon, l'Élu Éternel."),
        ("gordrakk", "Le Poing de Gork", "Vaincre Gordrakk, le Poing de Gork."),
        ("skarbrand", "L'Exilé", "Vaincre Skarbrand, le Démon Exilé."),
        ("thanquol", "Le Prophète Gris", "Vaincre le Prophète Gris Thanquol."),
        ("rotigus", "Le Père-Pluie", "Vaincre Rotigus, Grand Immonde de Nurgle.")]
P = {}


def av(nom, parent, icone, titre, desc, criteres, cadre="task", requis=None, xp=0, cache=False, fond=None):
    d = {"display": {"icon": {"id": icone}, "title": {"text": titre}, "description": {"text": desc}, "frame": cadre,
                     "show_toast": True, "announce_to_chat": cadre != "task", "hidden": cache}, "criteria": criteres}
    if fond:
        d["display"]["background"] = fond
    if parent:
        d["parent"] = "royaumes:saga/" + parent
    if requis:
        d["requirements"] = requis
    if xp:
        d["rewards"] = {"experience": xp}
    P[nom] = d


def objet(*ids):
    return {"trigger": "minecraft:inventory_changed", "conditions": {"items": [{"items": list(ids) if len(ids) > 1 else ids[0]}]}}


def impossible():
    return {"trigger": "minecraft:impossible"}


def main():
    av("racine", None, "royaumes:marbre_celeste_grave", "Saga des Royaumes", "Les Royaumes Mortels t'attendent, héros.",
       {"arrivee": {"trigger": "minecraft:tick"}}, fond="royaumes:block/marbre_celeste")
    av("serment", "racine", "minecraft:white_banner", "Serment d'allégeance", "Prêter serment à une faction (touche J).", {"serment": impossible()}, "goal", xp=50)
    av("capacite", "serment", "minecraft:blaze_powder", "Don de la faction", "Utiliser la capacité de ta faction (touche R).", {"capacite": impossible()})
    av("pierre", "racine", "royaumes:pierre_royaumes_brute", "Pierre des Royaumes", "Extraire de la pierre des Royaumes brute.", {"pierre": objet("royaumes:pierre_royaumes_brute")})
    av("baton", "pierre", "royaumes:baton_azyr", "Porteur de Vent", "Forger un bâton de magie.", {"baton": objet(*["royaumes:baton_" + v for v in VENTS])})
    av("sort", "baton", "royaumes:eclat_hysh", "Premier sortilège", "Lancer un sort avec un bâton.", {"sort": impossible()})
    av("huit_vents", "sort", "royaumes:grimoire_des_vents", "Maître des huit Vents", "Posséder les huit bâtons de magie.",
       {v: objet("royaumes:baton_" + v) for v in VENTS}, "challenge", xp=500)
    av("autel", "baton", "royaumes:autel_arcanique", "Source arcanique", "Fabriquer un autel arcanique.", {"autel": objet("royaumes:autel_arcanique")})
    av("portail", "pierre", "royaumes:portail_des_royaumes", "Porte des Royaumes", "Fabriquer un Portail des Royaumes.",
       {"portail": objet("royaumes:portail_des_royaumes")}, "goal")
    parent = "portail"
    for v in VENTS:
        av("royaume_" + v, "portail", "royaumes:eclat_" + v, "Royaume " + ("d'" if NOMS[v][0] in "AEIOUH" else "de ") + NOMS[v], DESC_ROYAUMES[v],
           {"entrer": {"trigger": "minecraft:changed_dimension", "conditions": {"to": DIMS[v]}}})
    av("huit_points", "portail", "royaumes:pierre_du_chaos", "Aux portes des Huit-Points", "Oser entrer dans les Huit-Points, domaine du Chaos.",
       {"entrer": {"trigger": "minecraft:changed_dimension", "conditions": {"to": "royaumes:huit_points"}}}, "goal")
    av("voyageur", "royaume_chamon", "minecraft:recovery_compass", "Voyageur des Royaumes", "Visiter les huit Royaumes Mortels.",
       {v: {"trigger": "minecraft:changed_dimension", "conditions": {"to": DIMS[v]}} for v in VENTS}, "challenge", xp=500)
    av("premier_boss", "serment", "minecraft:iron_sword", "Tueur de légendes", "Vaincre un des seigneurs des Royaumes.",
       {b[0]: {"trigger": "minecraft:player_killed_entity", "conditions": {"entity": {"type": "minecraft:entity_properties", "entity": "this", "predicate": {"type": "royaumes:" + b[0]}}}} for b in BOSS},
       "goal", requis=[[b[0] for b in BOSS]], xp=100)
    for b in BOSS:
        av("boss_" + b[0], "premier_boss", "minecraft:wither_skeleton_skull", b[1], b[2],
           {"tuer": {"trigger": "minecraft:player_killed_entity", "conditions": {"entity": {"type": "minecraft:entity_properties", "entity": "this", "predicate": {"type": "royaumes:" + b[0]}}}}}, "goal", xp=150)
    av("fleau", "premier_boss", "minecraft:nether_star", "Fléau des Dieux", "Vaincre les six seigneurs des Royaumes.",
       {b[0]: {"trigger": "minecraft:player_killed_entity", "conditions": {"entity": {"type": "minecraft:entity_properties", "entity": "this", "predicate": {"type": "royaumes:" + b[0]}}}} for b in BOSS},
       "challenge", xp=1000)
    shutil.rmtree(DOSSIER, ignore_errors=True)
    os.makedirs(DOSSIER)
    for n, d in P.items():
        with open(os.path.join(DOSSIER, n + ".json"), "w", encoding="utf-8") as f:
            json.dump(d, f, ensure_ascii=False, indent=2)
    print(len(P), "progrès")


if __name__ == "__main__":
    main()
