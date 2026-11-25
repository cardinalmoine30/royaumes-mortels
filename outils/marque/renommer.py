# -*- coding: utf-8 -*-
"""Noms propres originaux à la place des marques de Games Workshop, pour pouvoir publier le mod.

Remplace dans tous les textes affichés (traductions, datapack, Java, générateurs Python, README) les noms déposés
(factions, dieux, Royaumes, unités, seigneurs…) par ceux de noms.json. Les identifiants techniques en minuscules
(royaumes:skaven, textures, fonctions) ne changent pas : les mondes existants restent compatibles.
Usage : python3 outils/marque/renommer.py [--verifier] (idempotent)."""
import glob, json, os, re, sys

ICI = os.path.dirname(os.path.abspath(__file__))
RACINE = os.path.normpath(os.path.join(ICI, "..", ".."))
NOMS = json.load(open(os.path.join(ICI, "noms.json")))
# mots en minuscules dans les phrases (jamais après « : _ / " », pour épargner les identifiants)
MINUSCULES = {"malepierre": "fangepierre", "aelfes": "elfes", "aelfs": "elfes", "duardins": "nains", "duardin": "nain",
              "orruks": "orcs", "skavens": "hommes-rats", "gargants": "géants", "sigmarite": "célestacier"}
L = r"A-Za-zÀ-ÿ0-9"
MOTIF = re.compile(r"(?<![" + L + r"])(" + "|".join(re.escape(k) for k in sorted(NOMS, key=len, reverse=True)) + r")(?![" + L + r"])")
MOTIF_MIN = re.compile(r"(?<=[ '(«])(" + "|".join(MINUSCULES) + r")(?![" + L + r"_])")
FICHIERS = ["src/main/resources/assets/royaumes/lang/*.json", "src/main/resources/data/royaumes/**/*.json",
            "src/main/resources/data/royaumes/**/*.mcfunction", "src/main/java/**/*.java", "src/main/templates/**/*.toml",
            "outils/**/*.py", "outils/*.json", "outils/**/*.json", "README.md"]
EXCLUS = ("outils/marque/",)


CORRECTIONS = {"de de ": "de ", "de d'": "d'", "Démon de Lyssara (Démon)": "Démon de Lyssara", "des des ": "des ",
               "le Abyssal": "l'Abyssal", "les Abyssal ": "les Abyssaux ", "de Faucheurs d'Os": "des Faucheurs d'Os"}


def traiter(t):
    t = MOTIF.sub(lambda m: NOMS[m.group(1)], t)
    t = MOTIF_MIN.sub(lambda m: MINUSCULES[m.group(1)], t)
    for a, b in CORRECTIONS.items():
        t = t.replace(a, b)
    return t


def main():
    verifier = "--verifier" in sys.argv
    vus, changes, restes = set(), 0, {}
    for motif in FICHIERS:
        for p in glob.glob(os.path.join(RACINE, motif), recursive=True):
            rel = os.path.relpath(p, RACINE)
            if p in vus or rel.startswith(EXCLUS):
                continue
            vus.add(p)
            t = open(p, encoding="utf-8").read()
            if verifier:
                for m in MOTIF.findall(t):
                    restes[m] = restes.get(m, 0) + 1
                continue
            n = traiter(t)
            if n != t:
                open(p, "w", encoding="utf-8").write(n)
                changes += 1
    if verifier:
        print("noms déposés restants :", restes or "aucun")
    else:
        print("renommage : %d fichiers modifiés" % changes)


if __name__ == "__main__":
    main()
