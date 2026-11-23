# -*- coding: utf-8 -*-
"""Données de faction partagées par les générateurs (exportées depuis le générateur de datapack)."""
import json
import os

FACTIONS = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "donnees_factions.json"), encoding="utf-8"))
COULEUR_ALLIANCE = {"ordre": (212, 166, 58), "chaos": (200, 60, 50), "mort": (150, 130, 200), "destruction": (120, 170, 60)}
NOM_ALLIANCE = {"ordre": "Ordre", "chaos": "Chaos", "mort": "Mort", "destruction": "Destruction"}
ALLIANCES = [(NOM_ALLIANCE[a], COULEUR_ALLIANCE[a], [f["num"] for f in FACTIONS if f["alliance"] == a])
             for a in ("ordre", "chaos", "mort", "destruction")]
