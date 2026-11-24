# -*- coding: utf-8 -*-
"""Test d'équilibrage : combien de coups un héros encaisse avant de mourir, selon son équipement, face aux guerriers des
Royaumes et aux seigneurs. Formules de Minecraft : armure/robustesse (plafond 80 %), Protection (EPF, plafond 20 -> 80 %),
Résistance (20 % par niveau), cœurs bonus. Usage : python3 simulation.py  -> tableau + equilibrage.png"""
import os
import re
import statistics

ICI = os.path.dirname(os.path.abspath(__file__))
JAVA = os.path.join(ICI, "..", "..", "src", "main", "java", "fr", "royaumes", "ProfilsGeneres.java")


def profils():
    s = open(JAVA, encoding="utf-8").read()
    r = re.findall(r'new Profil\("([a-z_]+)", "([a-z_]+)", ([0-9.]+)f, ([0-9.]+)f', s)
    return [(a, b, float(c), float(d)) for a, b, c, d in r]


def apres_armure(d, armure, robustesse):
    eff = min(20.0, max(armure / 5.0, armure - 4.0 * d / (robustesse + 8.0)))
    return d * (1 - eff / 25.0)


def coups(d, eq, contre_seigneur=False, regle=None):
    """Coups pour tuer le héros (frappes de d dégâts), équipement eq."""
    if contre_seigneur and regle and regle.get("adaptation"):
        d *= 1 + regle["adaptation"] * max(0, eq.get("arsenal", eq["palier"]) - 1)
    if not contre_seigneur and not (regle and regle.get("novices") and eq["palier"] >= 2):
        d *= 0.75  # guerriers : -25 % contre les héros (0.16 : seulement sous le niveau 20, donc avant Légende)
    x = apres_armure(d, eq["armure"], eq["robustesse"])
    x *= 1 - min(20, eq["epf"]) * 0.04
    x *= max(0.0, 1 - 0.2 * eq["resistance"])
    vie = 20 + eq["coeurs"] * 2
    return float("inf") if x <= 0 else vie / x


# équipement : armure, robustesse, Protection (EPF : 4 pièces Protection IV = 16), niveau de Résistance (0 = aucune), cœurs bonus
AVANT = {
    "Sans armure": dict(palier=0, armure=0, robustesse=0, epf=0, resistance=0, coeurs=0),
    "Fer (vanilla)": dict(palier=0, armure=15, robustesse=0, epf=0, resistance=0, coeurs=0),
    "Netherite Prot IV": dict(palier=2, arsenal=0, armure=20, robustesse=12, epf=16, resistance=0, coeurs=0),
    "Légende Prot IV (0.15)": dict(palier=2, armure=24, robustesse=16, epf=16, resistance=1, coeurs=0),
    "Mythique Prot IV (0.15)": dict(palier=3, armure=27, robustesse=20, epf=16, resistance=2, coeurs=4),
    "Divin Prot IV (0.15)": dict(palier=4, armure=30, robustesse=24, epf=16, resistance=3, coeurs=8),
}
APRES = {
    "Sans armure": AVANT["Sans armure"],
    "Fer (vanilla)": AVANT["Fer (vanilla)"],
    "Netherite Prot IV": AVANT["Netherite Prot IV"],
    "Légende Prot IV": dict(palier=2, armure=24, robustesse=16, epf=16, resistance=1, coeurs=0),
    "Mythique Prot IV": dict(palier=3, armure=24, robustesse=18, epf=16, resistance=1, coeurs=4),
    "Divin Prot IV": dict(palier=4, armure=25, robustesse=20, epf=16, resistance=1, coeurs=8),
}
REGLE_APRES = {"adaptation": 0.3, "novices": True}


def main():
    P = profils()
    mobs = [p for p in P if p[1] != "rm_boss" and p[2] < 400]
    dm = sorted(p[3] for p in mobs)
    med, p90 = statistics.median(dm), dm[int(len(dm) * 0.9)]
    boss = statistics.mean(p[3] for p in P if p[2] >= 400)
    cas = [("Guerrier moyen (%.0f)" % med, med, False), ("Élite (%.0f)" % p90, p90, False),
           ("Seigneur, coup (%.0f)" % boss, boss, True), ("Seigneur, onde (%.0f)" % (boss * 0.75), boss * 0.75, True)]
    lignes = []
    for titre, eqs, regle in (("AVANT (0.15)", AVANT, None), ("APRÈS (0.16)", APRES, REGLE_APRES)):
        print("\n" + titre)
        print("%-26s" % "" + "".join("%22s" % c[0] for c in cas))
        for nom, eq in eqs.items():
            vals = [coups(d, eq, s, regle) for _, d, s in cas]
            lignes.append((titre, nom, vals))
            print("%-26s" % nom + "".join("%22s" % ("immortel" if v > 999 else "%.0f" % v) for v in vals))
    return cas, lignes


def graphique(cas, lignes):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    noms = [n for t, n, v in lignes if t.startswith("APR")]
    avant = {n.replace(" (0.15)", ""): v for t, n, v in lignes if t.startswith("AVANT")}
    apres = {n: v for t, n, v in lignes if t.startswith("APR")}
    fig, axes = plt.subplots(1, 2, figsize=(13, 5.2), dpi=110)
    fig.patch.set_facecolor("#0e1a33")
    for ax, (k, titre) in zip(axes, ((0, cas[0][0]), (2, cas[2][0]))):
        x = range(len(noms))
        ax.bar([i - 0.2 for i in x], [avant[n][k] for n in noms], 0.4, label="0.15 (avant)", color="#c8553d")
        ax.bar([i + 0.2 for i in x], [apres[n][k] for n in noms], 0.4, label="0.16 (après)", color="#d4a63a")
        for i, n in enumerate(noms):
            ax.text(i - 0.2, avant[n][k] + 2, "%.0f" % avant[n][k], ha="center", color="#f0e6d2", fontsize=8)
            ax.text(i + 0.2, apres[n][k] + 2, "%.0f" % apres[n][k], ha="center", color="#f2d27a", fontsize=8)
        ax.set_xticks(list(x))
        ax.set_xticklabels([n.replace(" Prot IV", "\nProt IV") for n in noms], color="#f0e6d2", fontsize=8)
        ax.set_title("Coups encaissés avant de mourir : " + titre, color="#f2d27a", fontsize=11)
        ax.set_facecolor("#14233f")
        ax.tick_params(colors="#9aa0b8")
        for s_ in ax.spines.values():
            s_.set_color("#3a4a6a")
        ax.legend(facecolor="#14233f", labelcolor="#f0e6d2", edgecolor="#3a4a6a")
    fig.tight_layout()
    out = os.path.join(ICI, "equilibrage.png")
    fig.savefig(out, facecolor=fig.get_facecolor())
    print(out)


if __name__ == "__main__":
    graphique(*main())
