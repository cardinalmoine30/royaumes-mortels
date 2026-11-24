# -*- coding: utf-8 -*-
"""Équilibrage global, troisième partie : temps pour atteindre les niveaux qui ouvrent les paliers de la Forge.
Gloire nécessaire pour passer du niveau n à n+1 : 20 n + 40 (datapack). Sources estimées par heure de jeu active :
guerriers de faction (10 gloire, ~150/h), contrats (~1 rempli/10 min, 5×but + 3×niveau), minerais (~250/h),
quêtes de la Saga (gloire fixe), seigneurs (400 chacun)."""
from simulation import profils  # noqa: F401  (même dossier)
import re
import os

ICI = os.path.dirname(os.path.abspath(__file__))
Q = open(os.path.join(ICI, "..", "..", "src", "main", "java", "fr", "royaumes", "rpg", "Quetes.java"), encoding="utf-8").read()
SAGA = [(t, int(g)) for t, g in re.findall(r'new Etape\("([^"]+)", "[^"]*", "[^"]*", "[^"]*", \d+, (\d+),', Q)]


def cumul(n):
    return sum(20 * k + 40 for k in range(1, n))


def heures(niveau, quetes_faites):
    total = cumul(niveau) - sum(g for _, g in SAGA[:quetes_faites])
    par_heure = 150 * 10 + 6 * (5 * 20 + 3 * niveau) + 250
    return max(0, total) / par_heure


if __name__ == "__main__":
    print("Saga : %d quêtes, %d gloire au total" % (len(SAGA), sum(g for _, g in SAGA)))
    for nom, niv, q in (("Élite", 8, 9), ("Légende", 16, 16), ("Mythique", 25, 20), ("Divin", 35, 22), ("Niveau max", 61, 24)):
        print("%-11s niveau %2d : %6d gloire cumulée, ~%.1f h de jeu actif" % (nom, niv, cumul(niv), heures(niv, q)))
