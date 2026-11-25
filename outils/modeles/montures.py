# -*- coding: utf-8 -*-
"""Montures des joueurs : une par faction jouable, inspirées des figurines officielles.
Génère les modèles GeckoLib (sans cavalier, avec selle), MonturesGenerees.java, les traductions
et la planche d'aperçu. La liste MONTURES sert aussi au générateur du datapack (cornes d'appel)."""
import json
import os
from bestiaire import P, FAC
from factions import pal

H = lambda p, **kw: dict(pal=dict(P[p], **kw.pop("teinte", {})), **kw)

# faction joueur -> (id, nom, gabarit, spec, vitesse, pv, vol, feu, saut, description)
MONTURES = [
    ("stormcast", "dracoth", "Draconid'Célestis", "dragon",
     H("sc", corps=(10, 8, 18), jambe=(4, 9), tete=(6, 6, 7), cou=4, queue=8, cornes=True, crete_dos=True,
       teinte=dict(peau=(88, 108, 150), ventre=(184, 194, 214), corne=(230, 230, 236))),
     0.30, 60, False, False, False, "Reptile céleste crachant la foudre, monture des Extremis."),
    ("cites", "destrier", "Destrier des Compagnies Franches", "cheval",
     H("cites", corps=(8, 9, 16), jambe=(3, 12), tete=(4, 5, 8), cou=6, queue=5, sabots=True, caparacon=True,
       teinte=dict(peau=(112, 76, 46), poils=(38, 26, 18))),
     0.34, 40, False, False, False, "Cheval de guerre bardé de rouge et de crème, fierté des Cavaliers."),
    ("fyreslayers", "magmadroth", "Drake de Magma", "dragon",
     H("magma", corps=(12, 10, 20), jambe=(4, 8), tete=(7, 6, 8), cou=4, queue=10, cornes=True, crete_dos=True, ventre=True,
       teinte=dict(ventre=(255, 120, 40))),
     0.27, 70, False, True, False, "Drake au sang de magma, insensible au feu et à la lave."),
    ("kharadron", "gunhauler", "Canonnière des Nuées", "navire",
     H("navire", coque=(16, 8, 6), ballon=(10, 6, 12), canons=1, ballon_y=22),
     0.30, 50, True, False, False, "Petit vaisseau d'aether : regarde vers le haut ou le bas pour monter ou descendre."),
    ("khaine", "coursier_ombre", "Coursier d'Ombre de Nid-de-Ronces", "cheval",
     H("khaine", corps=(8, 9, 16), jambe=(3, 12), tete=(4, 5, 8), cou=6, queue=5, sabots=True, caparacon=True, cornes=True,
       teinte=dict(peau=(40, 30, 40), poils=(222, 200, 226))),
     0.37, 40, False, False, False, "Destrier noir aux crins lilas, consacré au Dieu du Meurtre."),
    ("idoneth", "ishlaen", "Fangmora des Marées", "poisson",
     H("abyss", corps=(14, 6, 6), lanternes=True, teinte=dict(peau=(104, 84, 116), ventre=(170, 150, 176))),
     0.32, 45, True, False, False, "Poisson des abysses qui nage dans l'air comme dans l'eau."),
    ("lumineth", "destrier_aube", "Destrier de l'Aube", "cheval",
     H("lum", corps=(8, 9, 16), jambe=(3, 13), tete=(4, 5, 8), cou=7, queue=6, sabots=True, caparacon=True,
       teinte=dict(peau=(236, 236, 240), poils=(232, 214, 160))),
     0.38, 40, False, False, False, "Cheval blanc des Lumineux Dawnriders, rapide comme la lumière."),
    ("seraphon", "aggradon", "Raptor de guerre", "theropode",
     H("sera", corps=(9, 9, 14), jambe=(4, 11), tete=(7, 6, 8), cou=3, queue=12,
       teinte=dict(peau=(56, 140, 150), ventre=(190, 214, 200), crete=(200, 60, 40))),
     0.33, 55, False, False, False, "Prédateur bipède des Écailleux Knights, aussi têtu que vorace."),
    ("sylvaneth", "cerf_wyldwood", "Cerf de la Bois-Sauvage", "cheval",
     H("sylv", corps=(7, 8, 15), jambe=(3, 13), tete=(4, 5, 7), cou=7, queue=3, sabots=True, cornes=True),
     0.36, 40, False, False, False, "Esprit sylvestre à ramure, qui guérit en foulant la mousse."),
    ("esclaves", "destrier_chaos", "Destrier du Chaos", "cheval",
     H("chaos_cheval", corps=(9, 9, 17), jambe=(3, 12), tete=(4, 5, 8), cou=6, queue=5, sabots=True, caparacon=True, cornes=True),
     0.34, 50, False, False, False, "Cheval noir caparaçonné de mailles, aux cornes recourbées."),
    ("khorne", "juggernaut", "Juggernaut de Sangrath", "mastodonte",
     H("laiton", corps=(11, 10, 18), jambe=(5, 10), tete=(7, 7, 7), cou=2, queue=4, cornes=True, sabots=True),
     0.27, 80, False, True, False, "Démon d'airain et de chair, qui charge sans jamais s'arrêter."),
    ("tzeentch", "disque", "Disque de Vharys", "disque",
     H("tzeentch", rayon=8),
     0.34, 40, True, False, False, "Démon en forme de disque qui file dans les airs sur un feu magique."),
    ("slaanesh", "seeker", "Coursier de Lyssara", "cheval",
     H("slaanesh", corps=(6, 7, 14), jambe=(2, 13), tete=(4, 4, 6), cou=7, queue=6,
       teinte=dict(peau=(150, 110, 170), poils=(230, 200, 240))),
     0.42, 35, False, False, False, "La monture la plus rapide des Royaumes, à la langue démesurée."),
    ("nurgle", "pusgoyle", "Mouche Géante", "fauve",
     H("nurgle", corps=(10, 9, 14), jambe=(3, 8), tete=(6, 6, 6), cou=2, queue=6, ailes=14, dard=True,
       teinte=dict(peau=(130, 150, 80), membrane=(170, 190, 150))),
     0.26, 55, True, False, False, "Mouche-démon bourdonnante des Blightlords."),
    ("skaven", "gnaw_beast", "Gnaw-beast", "fauve",
     H("skaven", corps=(9, 9, 16), jambe=(3, 9), tete=(6, 6, 8), cou=2, queue=12, crete_dos=True,
       teinte=dict(peau=(150, 112, 96))),
     0.35, 45, False, False, False, "Rat monstrueux des Clawlords, à la queue rose sans fin."),
    ("hashut", "taurus", "Grand Taurus", "fauve",
     H("hashut", corps=(10, 10, 16), jambe=(4, 9), tete=(7, 6, 7), cou=2, queue=6, cornes=True, ailes=16,
       teinte=dict(peau=(60, 40, 34), corne=(200, 150, 70), membrane=(110, 50, 30))),
     0.30, 60, True, True, False, "Taureau ailé au sang de feu, monture des prêtres de Ashkar."),
    ("nighthaunt", "dreadblade", "Coursier Spectral", "cheval",
     H("nh", corps=(8, 9, 16), jambe=(3, 12), tete=(4, 5, 8), cou=6, queue=5, sabots=True),
     0.37, 40, False, False, False, "Cheval fantôme qui ignore les chutes."),
    ("soulblight", "cauchemar", "Cauchemar des Chevaliers de Sang", "cheval",
     H("sb", corps=(9, 9, 17), jambe=(3, 12), tete=(4, 5, 8), cou=6, queue=5, sabots=True, caparacon=True,
       teinte=dict(peau=(42, 32, 36), poils=(20, 16, 18))),
     0.36, 50, False, False, False, "Destrier mort-vivant bardé de cramoisi et de sarcelle."),
    ("ossiarch", "kavalos", "Destrier d'Os", "cheval",
     H("ossi", corps=(8, 9, 16), jambe=(3, 12), tete=(4, 5, 8), cou=6, queue=4, sabots=True, crete_dos=True),
     0.35, 50, False, False, False, "Monture d'os ciselé des Deathriders."),
    ("fec", "morbheg", "Chauve-Souris", "fauve",
     H("fec", corps=(9, 8, 16), jambe=(3, 11), tete=(6, 6, 6), cou=4, queue=6, ailes=12, criniere=True,
       teinte=dict(peau=(132, 84, 60), poils=(70, 44, 34), membrane=(48, 36, 36))),
     0.30, 50, True, False, False, "Bête ailée des chevaliers de la Cour Cannibale."),
    ("ironjawz", "gore_grunta", "Sanglier de Guerre", "fauve",
     H("orruk", corps=(9, 9, 15), jambe=(3, 8), tete=(6, 6, 7), cou=2, queue=4, defenses_haut=True, crete_dos=True,
       teinte=dict(peau=(110, 80, 58), poils=(50, 36, 28), corne=(40, 40, 44))),
     0.34, 55, False, False, False, "Sanglier de guerre cuirassé de jaune, aussi teigneux que son orruk."),
    ("kruleboyz", "gnashtoof", "Grand Gnashtoof", "fauve",
     H("kb", corps=(10, 9, 16), jambe=(3, 9), tete=(6, 6, 8), cou=3, queue=6, crete_dos=True,
       teinte=dict(peau=(122, 100, 116), poils=(70, 56, 60))),
     0.33, 55, False, False, False, "Fauve des marais à la peau violacée, monture des Killabosses."),
    ("gitz", "squig", "Croqueur Bondissant", "squig",
     H("squig", taille=11),
     0.33, 35, False, False, True, "Une gueule sur pattes qui avance par grands bonds imprévisibles."),
    ("ogors", "mournfang", "Croc-Funèbre", "fauve",
     H("ogor", corps=(11, 10, 17), jambe=(4, 9), tete=(7, 7, 7), cou=2, queue=4, defenses_haut=True, criniere=True,
       teinte=dict(peau=(110, 76, 52), poils=(80, 56, 40))),
     0.32, 70, False, False, False, "Grand fauve hirsute aux défenses de sanglier."),
    ("behemat", "mammouth", "Mammouth des Plaines", "mastodonte",
     H("givre", corps=(14, 12, 20), jambe=(5, 10), tete=(8, 8, 8), cou=2, queue=4, defenses=True, criniere=True,
       teinte=dict(peau=(120, 90, 64), poils=(96, 70, 48))),
     0.27, 90, False, False, False, "Colosse laineux assez fort pour porter un fils de Ymorath."),
]


def construire(gab, mid, spec, fac):
    import betes
    import creatures2 as C
    spec = dict(spec, selle=True)
    fonctions = {"cheval": betes.cheval, "griffon": betes.griffon, "dragon": betes.dragon, "theropode": betes.theropode,
                 "fauve": betes.fauve, "mastodonte": betes.mastodonte, "squig": betes.squig, "disque": betes.disque,
                 "poisson": C.poisson, "navire": C.navire}
    return fonctions[gab](mid, spec, fac)


def generer(ICI, ASSETS, RACINE, boite, animations_gen, apercu):
    profils, planche = [], []
    for fac, ident, nom, gab, spec, vit, pv, vol, feu, saut, desc in MONTURES:
        mid = f"monture_{ident}"
        fac_modele = {"ironjawz": "orruks", "kruleboyz": "orruks"}.get(fac, fac)
        m, mats = construire(gab, mid, spec, fac_modele)
        tex = m.exporter(mats, animations_gen(m, vol))
        h, w = boite(m)
        selle_y, _ = getattr(m, "selle", (h * 16, 0))
        profils.append((mid, nom, fac, vit, pv, vol, feu, saut, round(min(w * 0.7, 1.8), 2), round(min(h * 0.8, 2.2), 2),
                        round(selle_y / 16.0, 3)))
        sortie = f"{ICI}/apercus/{mid}.png"
        apercu(m, tex, sortie, nom)
        planche.append((nom, sortie))
    # Java
    L = ["package fr.royaumes;", "", "import java.util.List;", "",
         "/** Généré par outils/modeles/montures.py : une monture par faction jouable. */",
         "public final class MonturesGenerees {", "    private MonturesGenerees() {}", "",
         "    public static final List<ProfilMonture> TOUTES = List.of("]
    lignes = []
    for (mid, nom, fac, vit, pv, vol, feu, saut, lw, lh, sy) in profils:
        lignes.append(f'        new ProfilMonture("{mid}", "{fac}", {vit}, {pv}, {str(vol).lower()}, {str(feu).lower()}, '
                      f'{str(saut).lower()}, {lw}F, {lh}F, {sy}F)')
    L.append(",\n".join(lignes))
    L += ["    );", "}", ""]
    open(f"{RACINE}/src/main/java/fr/royaumes/MonturesGenerees.java", "w").write("\n".join(L))
    for lang in ("fr_fr", "en_us"):
        p = f"{ASSETS}/lang/{lang}.json"
        d = json.load(open(p)) if os.path.exists(p) else {}
        for (mid, nom, *_r) in profils:
            d[f"entity.royaumes.{mid}"] = nom
        json.dump(d, open(p, "w"), ensure_ascii=False, indent=1)
    json.dump([{"id": p[0], "nom": p[1], "faction": p[2]} for p in profils],
              open(f"{ICI}/liste_montures.json", "w"), ensure_ascii=False, indent=1)
    return planche
