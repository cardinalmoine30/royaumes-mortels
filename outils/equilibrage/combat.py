# -*- coding: utf-8 -*-
"""Équilibrage global, deuxième partie : duels complets (le héros frappe aussi) à chaque étape de la progression, contre un
guerrier moyen, une élite et un seigneur (seul ou à plusieurs). Hypothèses : le héros frappe 1,6 fois/s (épée) et touche 85 %
du temps ; un seigneur le touche 0,4 fois/s (il esquive, recule) et un guerrier 0,6 fois/s ; une pomme d'or toutes les 20 s
en combat de seigneur. Un combat est « jouable » si le héros tient au moins aussi longtemps qu'il met à gagner.
Usage : python3 combat.py [--avant]"""
import statistics
import sys
from simulation import profils, apres_armure, coups

ARMURE_PROFILS = 6.0  # armure médiane des guerriers
ETAPES = [  # nom, équipement (cf. simulation), dégâts de l'arme, palier d'arsenal
    ("Début : Soldat + arme de départ", dict(palier=0, arsenal=0, armure=15, robustesse=0, epf=0, resistance=1, coeurs=0), 6.0),
    ("Élite + arme de lignée (niv. 8-16)", dict(palier=1, armure=20, robustesse=8, epf=8, resistance=1, coeurs=0), 7.5),
    ("Légende + champion (niv. 16-25)", dict(palier=2, armure=24, robustesse=16, epf=16, resistance=1, coeurs=0), 9.5),
    ("Mythique + champion (niv. 25-35)", dict(palier=3, armure=24, robustesse=18, epf=16, resistance=1, coeurs=2), 10.5),
    ("Divin + ascension (niv. 35+)", dict(palier=4, armure=25, robustesse=20, epf=16, resistance=1, coeurs=4), 12.5),
]


def frappe(d, armure):
    return apres_armure(d, armure, 0.0)


def duel(eq, arme, pv, armure, d, seigneur, joueurs=1, mult_pv=1.0, regle=None):
    dps = 1.6 * 0.85 * frappe(arme, armure) * joueurs
    gagner = pv * mult_pv / dps
    touches = 0.4 if seigneur else 0.6
    tenir = coups(d, eq, seigneur, regle) / touches
    if seigneur:
        tenir *= 1.5  # pommes d'or, recul, régénération naturelle
    return gagner, tenir


def main(avant=False):
    P = profils()
    mobs = [p for p in P if p[2] < 400]
    pv_m, d_m = statistics.median(p[2] for p in mobs), statistics.median(p[3] for p in mobs)
    el = sorted(mobs, key=lambda p: p[2])[int(len(mobs) * 0.9)]
    lords = [p for p in P if p[2] >= 700]
    pv_b, d_b = statistics.mean(p[2] for p in lords), statistics.mean(p[3] for p in lords)
    regle = None if avant else {"adaptation": 0.2, "novices": True}
    mult = (lambda n: 1.0) if avant else (lambda n: min(1.6, 0.55 + 0.3 * (n - 1)))
    print("Guerrier moyen %.0f PV / %.0f dégâts ; élite %s %.0f PV ; seigneur moyen %.0f PV / %.0f dégâts"
          % (pv_m, d_m, el[0], el[2], pv_b, d_b))
    print("%-36s %16s %16s %20s %20s" % ("", "guerrier", "élite", "seigneur seul", "seigneur à 3"))
    res = []
    for nom, eq, arme in ETAPES:
        cas = [duel(eq, arme, pv_m, ARMURE_PROFILS, d_m, False, regle=regle),
               duel(eq, arme, el[2], ARMURE_PROFILS + 4, el[3], False, regle=regle),
               duel(eq, arme, pv_b, 14, d_b, True, 1, mult(1), regle),
               duel(eq, arme, pv_b, 14, d_b, True, 3, mult(3), regle)]
        res.append((nom, cas))
        print("%-36s" % nom + "".join("%20s" % ("%3.0fs / tient %s" % (g, "∞" if t > 999 else "%.0fs" % t)) for g, t in cas))
    return res


if __name__ == "__main__":
    main("--avant" in sys.argv)


def graphique(res):
    import os
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    noms = [n.split(" (")[0].replace(" + ", "\n+ ") for n, _ in res]
    fig, axes = plt.subplots(1, 2, figsize=(13, 5.2), dpi=110)
    fig.patch.set_facecolor("#0e1a33")
    for ax, (k, titre) in zip(axes, ((2, "Seigneur, seul"), (3, "Seigneur, à trois héros"))):
        g = [c[k][0] for _, c in res]
        t = [min(c[k][1], 200) for _, c in res]
        x = range(len(res))
        ax.bar([i - 0.2 for i in x], g, 0.4, label="temps pour le vaincre", color="#c8553d")
        ax.bar([i + 0.2 for i in x], t, 0.4, label="temps que le héros tient", color="#7ec86e")
        for i in x:
            ax.text(i - 0.2, g[i] + 2, "%.0f s" % g[i], ha="center", color="#f0e6d2", fontsize=8)
            ax.text(i + 0.2, t[i] + 2, "%.0f s" % t[i], ha="center", color="#c8e6be", fontsize=8)
        ax.set_xticks(list(x))
        ax.set_xticklabels(noms, color="#f0e6d2", fontsize=7)
        ax.set_ylim(0, max(max(g), max(t)) * 1.35)
        ax.set_title(titre + " : jouable quand le vert dépasse le rouge", color="#f2d27a", fontsize=11)
        ax.set_facecolor("#14233f")
        ax.tick_params(colors="#9aa0b8")
        for s_ in ax.spines.values():
            s_.set_color("#3a4a6a")
        ax.legend(facecolor="#14233f", labelcolor="#f0e6d2", edgecolor="#3a4a6a", fontsize=8)
    fig.tight_layout()
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "combats.png")
    fig.savefig(out, facecolor=fig.get_facecolor())
    print(out)


if __name__ == "__main__" and "--graphique" in sys.argv:
    graphique(main())
