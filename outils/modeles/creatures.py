# -*- coding: utf-8 -*-
"""Gabarits non humanoïdes : bêtes (et montures avec cavalier), dragons/volants, navires Kharadron,
blobs (squigs, rejetons), poissons/tortues de l'Ethersea, chars et roues."""
from modele import Modele
from factions import sombre, bande, yeux, dents, eclair, combine, embleme


def _pal(P):
    pal = {"corps": P["peau"], "armure": P["armure"], "armure2b": P["armure2"], "tissu": P["tissu"], "peau": P["peau"],
           "metal": P["metal"], "lueur": P["lueur"], "corne": P.get("corne", (220, 205, 170)), "manche": P.get("manche", (70, 46, 30)),
           "lame": P.get("lame", (200, 205, 215)), "poils": P.get("poils", (90, 70, 50)), "bois": P.get("bois", (110, 80, 50)),
           "ventre": P.get("ventre", tuple(min(255, int(v * 1.25)) for v in P["peau"])), "membrane": P.get("membrane", sombre(P["peau"], 0.8)),
           "sombre": (24, 22, 26)}
    return {k: {"base": v, "bord": sombre(v), "bruit": 6} for k, v in pal.items()}


def cavalier(m, P, y0, z0, arme="lance", taille=1):
    """Petit cavalier humanoïde assis sur une monture (os rider_*)."""
    t = taille
    m.bone("rider", "body", (0, y0, z0))
    m.bone("rider_arm", "rider", (-4 * t, y0 + 9 * t, z0))
    m.cube("rider", (-3 * t, y0, z0 - 2 * t), (6 * t, 9 * t, 4 * t), "armure", north=bande(P["armure2"], "bas"))
    m.cube("rider", (-2 * t, y0 + 9 * t, z0 - 2 * t), (4 * t, 4 * t, 4 * t), "armure",
           north=yeux(P["lueur"], (20, 20, 26)))
    m.cube("rider", (-5 * t, y0 - 2 * t, z0 - 2 * t), (2 * t, 4 * t, 4 * t), "armure")        # jambes de part et d'autre
    m.cube("rider", (3 * t, y0 - 2 * t, z0 - 2 * t), (2 * t, 4 * t, 4 * t), "armure")
    m.cube("rider", (3 * t, y0 + 3 * t, z0 - 1 * t), (2 * t, 6 * t, 2 * t), "armure")
    m.cube("rider_arm", (-5 * t, y0 + 3 * t, z0 - 1 * t), (2 * t, 6 * t, 2 * t), "armure")
    if arme == "lance":
        m.cube("rider_arm", (-5 * t, y0 + 4 * t, z0 - 18 * t), (1, 1, 18 * t), "manche")
        m.cube("rider_arm", (-5 * t - 1, y0 + 3 * t, z0 - 21 * t), (3, 3, 3), "lame")
    elif arme in ("epee", "hache", "marteau"):
        m.cube("rider_arm", (-5 * t, y0 + 2 * t, z0 - 2 * t), (1, 12 * t, 2), "manche" if arme != "epee" else "lame")
        if arme != "epee":
            m.cube("rider_arm", (-6 * t, y0 + 11 * t, z0 - 3 * t), (3, 3, 4), "metal")
    elif arme == "fusil":
        m.cube("rider_arm", (-6 * t, y0 + 3 * t, z0 - 12 * t), (2, 2, 12 * t), "metal")


def bete(nom, s):
    """Quadrupède : monture, dragon, bête de guerre."""
    P = s["pal"]
    m = Modele(nom, s.get("tex", 128))
    L, W, H = s.get("corps", (10, 8, 8))
    lw, lh = s.get("jambe", (3, 8))
    m.bone("root", None, (0, 0, 0))
    m.bone("body", "root", (0, lh + H // 2, 0))
    ys = lh
    m.cube("body", (-W // 2, ys, -L // 2), (W, H, L), "corps", up=bande(P["armure2"], "haut") if s.get("crete_dos") else None,
           down=None)
    if s.get("ventre"):
        m.cube("body", (-W // 2 + 1, ys - 1, -L // 2 + 2), (W - 2, 1, L - 4), "ventre")
    if s.get("carapace"):
        m.cube("body", (-W // 2 - 1, ys + H - 2, -L // 2 + 1), (W + 2, 4, L - 2), "armure",
               up=combine(bande(P["armure2"], "haut"), bande(P["armure2"], "bas")))
    if s.get("plaques"):     # Stegadon
        for i in range(0, L - 4, 4):
            m.cube("body", (-1, ys + H, -L // 2 + 2 + i), (2, 3 + (i // 4) % 2 * 2, 3), "armure2b")
    if s.get("caparacon"):
        m.cube("body", (-W // 2 - 1, ys - 2, -L // 4), (W + 2, H - 2, L // 2), "tissu", east=bande(P["armure2"]), west=bande(P["armure2"]))
    # pattes
    for nomj, sx, sz in (("leg_fl", -1, -1), ("leg_fr", 1, -1), ("leg_bl", -1, 1), ("leg_br", 1, 1)):
        x = -W // 2 if sx < 0 else W // 2 - lw
        z = -L // 2 + 1 if sz < 0 else L // 2 - lw - 1
        m.bone(nomj, "root", (x + lw // 2, lh, z + lw // 2))
        m.cube(nomj, (x, 0, z), (lw, lh, lw), "corps", north=bande(P["armure2"], "bas", 2) if s.get("sabots") else None)
        if s.get("griffes_pattes"):
            m.cube(nomj, (x, 0, z - 1), (lw, 1, 1), "corne")
    # cou + tête
    tw, th, td = s.get("tete", (6, 6, 7))
    cou = s.get("cou", 4)
    yt = ys + H - 2 + cou // 2
    m.bone("neck", "body", (0, ys + H - 3, -L // 2))
    if cou:
        m.cube("neck", (-max(2, tw // 2 - 1), ys + H - 4, -L // 2 - cou), (max(4, tw - 2), max(4, th - 1), cou + 1), "corps")
    zt = -L // 2 - cou - td + 1
    m.bone("head", "neck", (0, yt, zt + td))
    m.cube("head", (-tw // 2, yt, zt), (tw, th, td), "corps", north=yeux(P["lueur"], None, 0.35),
           east=yeux(P["lueur"], None, 0.3), west=yeux(P["lueur"], None, 0.3))
    m.bone("jaw", "head", (0, yt, zt + td))
    if s.get("bec"):
        m.cube("head", (-2, yt + 1, zt - 4), (4, 3, 4), "corne")
        m.cube("jaw", (-1, yt - 1, zt - 2), (2, 2, 3), "corne")
    else:
        m.cube("jaw", (-tw // 2 + 1, yt - 2, zt - 1), (tw - 2, 2, td), "corps", north=dents)
    if s.get("cornes"):
        m.cube("head", (-tw // 2 - 2, yt + th - 2, zt + 1), (2, 2, 2), "corne")
        m.cube("head", (-tw // 2 - 3, yt + th, zt), (2, 4, 2), "corne")
        m.cube("head", (tw // 2, yt + th - 2, zt + 1), (2, 2, 2), "corne")
        m.cube("head", (tw // 2 + 1, yt + th, zt), (2, 4, 2), "corne")
    if s.get("corne_nez"):
        m.cube("head", (-1, yt + th - 1, zt - 2), (2, 5, 2), "corne")
    if s.get("defenses"):
        m.cube("head", (-tw // 2 - 1, yt - 4, zt - 3), (2, 2, 6), "corne")
        m.cube("head", (tw // 2 - 1, yt - 4, zt - 3), (2, 2, 6), "corne")
    if s.get("criniere"):
        m.cube("neck", (-1, ys + H, -L // 2 - cou + 1), (2, 3, cou + 3), "poils")
    if s.get("collerette"):
        m.cube("head", (-tw // 2 - 3, yt - 1, zt + td - 1), (tw + 6, th + 4, 1), "armure2b")
    # queue
    q = s.get("queue", 6)
    if q:
        m.bone("tail", "body", (0, ys + H - 2, L // 2))
        m.cube("tail", (-1, ys + H - 4, L // 2), (3, 3, q), "corps")
        if s.get("queue_massue"):
            m.cube("tail", (-2, ys + H - 5, L // 2 + q), (5, 5, 4), "armure2b")
        elif s.get("dard"):
            m.cube("tail", (-1, ys + H - 3, L // 2 + q), (2, 6, 2), "corne")
    # ailes
    e = s.get("ailes", 0)
    if e:
        for nomb, sx in (("wing_l", -1), ("wing_r", 1)):
            x0 = -W // 2 - e if sx < 0 else W // 2
            m.bone(nomb, "body", (-W // 2 if sx < 0 else W // 2, ys + H, -L // 4))
            m.cube(nomb, (x0, ys + H - 1, -L // 4 - 2), (e, 2, 2), "corne")
            m.cube(nomb, (x0, ys + H - 1, -L // 4), (e, 1, max(6, L // 2 + 2)), "membrane",
                   up=bande(P["armure2"], "bas"))
    # cavalier / nacelle
    if s.get("cavalier"):
        cavalier(m, P, ys + H, -1, s.get("arme_cavalier", "lance"), s.get("taille_cavalier", 1))
    if s.get("nacelle"):
        m.cube("body", (-W // 2 + 1, ys + H, -2), (W - 2, 6, 8), "bois", north=bande(P["armure2"], "haut"))
        m.cube("body", (-W // 2 + 1, ys + H + 6, -2), (W - 2, 1, 8), "armure2b")
    if s.get("autel"):
        m.cube("body", (-3, ys + H, -2), (6, 10, 6), "armure", north=embleme("etoile", P["lueur"]))
    return m, _pal(P)


def navire(nom, s):
    """Navire volant Kharadron : coque, ballon d'aether-endrin, hélice, canons."""
    P = s["pal"]
    m = Modele(nom, s.get("tex", 128))
    L, W, H = s.get("coque", (24, 10, 7))
    m.bone("root", None, (0, 0, 0))
    m.bone("body", "root", (0, 6, 0))
    m.cube("body", (-W // 2, 4, -L // 2), (W, H, L), "bois", east=bande(P["armure2"], "haut"), west=bande(P["armure2"], "haut"))
    m.cube("body", (-W // 2 + 2, 4, -L // 2 - 5), (W - 4, H - 1, 5), "bois")          # proue
    m.cube("body", (-1, 3, -L // 2 - 8), (2, 3, 4), "armure2b")                     # éperon
    m.cube("body", (-W // 2, 4 + H, -L // 2), (W, 1, L), "armure", up=bande(P["armure2"]))  # pont
    m.cube("body", (-1, 4 + H, -2), (2, 10, 2), "metal")                            # mât
    m.bone("ballon", "body", (0, 14 + H, 0))
    bw, bh, bl = s.get("ballon", (W + 2, 8, L - 4))
    m.cube("ballon", (-bw // 2, 14 + H, -bl // 2), (bw, bh, bl), "tissu",
           east=bande(P["armure2"]), west=bande(P["armure2"]), north=embleme("point", P["lueur"]))
    m.bone("rotor", "body", (0, 4 + H // 2, L // 2 + 2))
    m.cube("rotor", (-4, 4 + H // 2 - 1, L // 2 + 1), (8, 2, 1), "metal")
    m.cube("rotor", (-1, 4 + H // 2 - 4, L // 2 + 1), (2, 8, 1), "metal")
    for i in range(s.get("canons", 1)):
        x = -W // 2 + 2 + i * 4
        m.cube("body", (x, 4 + H + 1, -L // 2 - 2), (2, 2, 6), "metal", north=bande(P["lueur"]))
    if s.get("equipage", True):
        for x in (-W // 4, W // 4):
            m.cube("body", (x - 1, 5 + H, 2), (3, 5, 3), "armure", north=yeux(P["lueur"], (20, 20, 26)))
    return m, _pal(P)


def blob(nom, s):
    """Squigs, rejetons du Chaos, Bêtes de Nurgle, Abomination…"""
    P = s["pal"]
    m = Modele(nom, s.get("tex", 128))
    r = s.get("taille", 10)
    m.bone("root", None, (0, 0, 0))
    m.bone("body", "root", (0, r // 2 + 2, 0))
    m.cube("body", (-r // 2, 3, -r // 2), (r, r - 2, r), "corps", north=yeux(P["lueur"], None, 0.25))
    m.cube("body", (-r // 2 + 1, r + 1, -r // 2 + 1), (r - 2, 2, r - 2), "corps")
    m.bone("jaw", "body", (0, 4, -r // 2))
    m.cube("jaw", (-r // 2 + 1, 2, -r // 2 - 1), (r - 2, 3, r - 2), "ventre", north=dents)
    for nomj, x in (("leg_l", -r // 2 + 1), ("leg_r", r // 2 - 3)):
        m.bone(nomj, "root", (x + 1, 3, 0))
        m.cube(nomj, (x, 0, -1), (2, 3, 3), "corps")
    if s.get("tentacules"):
        for i, (x, z) in enumerate(((-r // 2 - 2, 0), (r // 2, -2), (-2, r // 2), (r // 2, r // 4))):
            m.cube("body", (x, 3 + i, z), (2, 2, 6 if i % 2 else 2), "membrane")
            m.cube("body", (x, 5 + i, z), (2, 6, 2), "membrane")
    if s.get("cornes"):
        m.cube("body", (-r // 2 - 1, r - 2, -1), (2, 5, 2), "corne")
        m.cube("body", (r // 2 - 1, r - 2, -1), (2, 5, 2), "corne")
    if s.get("pustules"):
        for x, y, z in ((-r // 2 - 1, 5, -2), (r // 2, 7, 1), (-2, r, 0), (1, 6, r // 2)):
            m.cube("body", (x, y, z), (2, 2, 2), "lueur")
    if s.get("rats"):
        for x, z in ((-r // 2 - 2, -2), (r // 2, 1), (-1, r // 2)):
            m.cube("body", (x, 4, z), (3, 3, 4), "poils")
    if s.get("cavalier"):
        cavalier(m, P, r + 1, 0, s.get("arme_cavalier", "lance"))
    return m, _pal(P)


def poisson(nom, s):
    """Allopex, Ishlaen, Morrsarr, Leviadon (tortue)."""
    P = s["pal"]
    m = Modele(nom, s.get("tex", 128))
    L, W, H = s.get("corps", (16, 6, 6))
    m.bone("root", None, (0, 0, 0))
    m.bone("body", "root", (0, 6 + H // 2, 0))
    m.cube("body", (-W // 2, 6, -L // 2), (W, H, L), "corps", down=None)
    m.cube("body", (-W // 2 + 1, 5, -L // 2 + 1), (W - 2, 1, L - 2), "ventre")
    m.bone("head", "body", (0, 6 + H // 2, -L // 2))
    m.cube("head", (-W // 2 + 1, 6, -L // 2 - 5), (W - 2, H - 1, 5), "corps", north=yeux(P["lueur"], None, 0.3))
    m.bone("jaw", "head", (0, 6, -L // 2))
    m.cube("jaw", (-W // 2 + 1, 4, -L // 2 - 5), (W - 2, 2, 5), "ventre", north=dents)
    m.cube("body", (-1, 6 + H, -2), (2, 5, 4), "membrane")                       # aileron
    for nomb, sx in (("wing_l", -1), ("wing_r", 1)):
        x0 = -W // 2 - 5 if sx < 0 else W // 2
        m.bone(nomb, "body", (-W // 2 if sx < 0 else W // 2, 7, -2))
        m.cube(nomb, (x0, 7, -3), (5, 1, 4), "membrane")
    m.bone("tail", "body", (0, 6 + H // 2, L // 2))
    m.cube("tail", (-W // 2 + 1, 7, L // 2), (W - 2, H - 2, 5), "corps")
    m.cube("tail", (-1, 5, L // 2 + 5), (2, H + 2, 3), "membrane")
    if s.get("carapace"):
        m.cube("body", (-W // 2 - 2, 6 + H - 1, -L // 2 + 1), (W + 4, 4, L - 2), "armure",
               up=combine(bande(P["armure2"], "haut"), bande(P["armure2"], "bas")))
    if s.get("cavalier"):
        cavalier(m, P, 6 + H, 0, s.get("arme_cavalier", "lance"))
    if s.get("lanternes"):
        m.cube("head", (-1, 6 + H, -L // 2 - 7), (1, 1, 4), "corne")
        m.cube("head", (-2, 6 + H - 1, -L // 2 - 9), (3, 3, 3), "lueur")
    return m, _pal(P)


def char(nom, s):
    """Chars, Carrosse noir, Autel de guerre du Chaos, Roue de malheur skaven."""
    P = s["pal"]
    m = Modele(nom, s.get("tex", 128))
    L, W, H = s.get("caisse", (12, 10, 6))
    m.bone("root", None, (0, 0, 0))
    m.bone("body", "root", (0, 8, 0))
    if s.get("roue_geante"):     # Doomwheel : une grande roue avec des rats dedans
        R = 22
        m.bone("wheel_l", "body", (0, R // 2, 0))
        m.cube("wheel_l", (-5, 0, -R // 2), (1, R, R), "bois", west=lambda d, x, y, w, h, px: d.ellipse((x, y, x + w - 1, y + h - 1), outline=P["metal"]))
        m.cube("wheel_l", (4, 0, -R // 2), (1, R, R), "bois", east=lambda d, x, y, w, h, px: d.ellipse((x, y, x + w - 1, y + h - 1), outline=P["metal"]))
        m.cube("body", (-4, R // 2 - 3, -3), (8, 6, 6), "metal", north=eclair(P["lueur"]))
        m.cube("body", (-3, R // 2 + 3, -2), (6, 6, 5), "poils", north=yeux(P["lueur"]))
        m.cube("body", (-1, R - 2, -1), (2, 6, 2), "lueur")
        return m, _pal(P)
    m.cube("body", (-W // 2, 6, -L // 2), (W, H, L), "bois", north=bande(P["armure2"], "haut"),
           east=bande(P["armure2"], "haut"), west=bande(P["armure2"], "haut"))
    for nomb, x in (("wheel_l", -W // 2 - 2), ("wheel_r", W // 2)):
        m.bone(nomb, "body", (x + 1, 5, 0))
        m.cube(nomb, (x, 0, -5), (2, 10, 10), "bois",
               east=lambda d, x0, y0, w, h, px: (d.ellipse((x0, y0, x0 + w - 1, y0 + h - 1), outline=P["metal"]), d.line((x0 + w // 2, y0, x0 + w // 2, y0 + h - 1), fill=P["metal"])),
               west=lambda d, x0, y0, w, h, px: (d.ellipse((x0, y0, x0 + w - 1, y0 + h - 1), outline=P["metal"]), d.line((x0, y0 + h // 2, x0 + w - 1, y0 + h // 2), fill=P["metal"])))
    if s.get("toit"):          # Carrosse noir / autel
        m.cube("body", (-W // 2 + 1, 6 + H, -2), (W - 2, 9, L // 2 + 2), "tissu", north=yeux(P["lueur"]))
        m.cube("body", (-W // 2, 15 + H, -3), (W, 2, L // 2 + 4), "armure2b")
        if s.get("autel"):
            m.cube("body", (-2, 17 + H, 0), (4, 6, 4), "lueur", north=embleme("etoile", P["armure2"]))
    if s.get("disque"):        # Char flamboyant de Tzeentch : disque flottant
        m.cube("body", (-W // 2 - 2, 4, -L // 2 - 2), (W + 4, 2, L + 4), "lueur")
    cavalier(m, P, 6 + H, -L // 4, s.get("arme_cavalier", "epee"))
    if s.get("betes"):
        m.bone("beast", "body", (0, 6, -L // 2 - 8))
        m.cube("beast", (-3, 4, -L // 2 - 14), (6, 6, 10), "peau", north=yeux(P["lueur"], None, 0.3))
        m.cube("beast", (-2, 6, -L // 2 - 18), (4, 4, 4), "peau", north=dents)
        m.cube("beast", (-3, 0, -L // 2 - 13), (2, 4, 2), "peau")
        m.cube("beast", (1, 0, -L // 2 - 13), (2, 4, 2), "peau")
        m.cube("beast", (-3, 0, -L // 2 - 7), (2, 4, 2), "peau")
        m.cube("beast", (1, 0, -L // 2 - 7), (2, 4, 2), "peau")
    return m, _pal(P)


def animations_gen(m, volant=False):
    os_ = {b[0] for b in m.bones}
    flap = {"wing_l": {"rotation": {"0.0": [0, 0, -25], "0.4": [0, 0, 25], "0.8": [0, 0, -25]}},
            "wing_r": {"rotation": {"0.0": [0, 0, 25], "0.4": [0, 0, -25], "0.8": [0, 0, 25]}}}
    idle = {
        "body": {"position": {"0.0": [0, 0, 0], "1.5": [0, -0.4, 0], "3.0": [0, 0, 0]}},
        "head": {"rotation": {"0.0": [0, 0, 0], "1.5": [4, 3, 0], "3.0": [0, 0, 0]}},
        "tail": {"rotation": {"0.0": [-5, -10, 0], "1.5": [-5, 10, 0], "3.0": [-5, -10, 0]}},
        "right_arm": {"rotation": {"0.0": [-6, 0, 0], "1.5": [-9, 0, 0], "3.0": [-6, 0, 0]}},
        "left_arm": {"rotation": {"0.0": [-6, 0, 0], "1.5": [-3, 0, 0], "3.0": [-6, 0, 0]}},
        "cape": {"rotation": {"0.0": [4, 0, 0], "1.5": [8, 0, 0], "3.0": [4, 0, 0]}},
        "ballon": {"position": {"0.0": [0, 0, 0], "1.5": [0, 0.5, 0], "3.0": [0, 0, 0]}},
        "rotor": {"rotation": {"0.0": [0, 0, 0], "1.0": [0, 0, 360]}},
        "jaw": {"rotation": {"0.0": [0, 0, 0], "1.5": [6, 0, 0], "3.0": [0, 0, 0]}},
        "wing_l": {"rotation": {"0.0": [0, 0, -8], "1.5": [0, 0, -14], "3.0": [0, 0, -8]}},
        "wing_r": {"rotation": {"0.0": [0, 0, 8], "1.5": [0, 0, 14], "3.0": [0, 0, 8]}},
    }
    marche = {
        "right_leg": {"rotation": {"0.0": [28, 0, 0], "0.5": [-28, 0, 0], "1.0": [28, 0, 0]}},
        "left_leg": {"rotation": {"0.0": [-28, 0, 0], "0.5": [28, 0, 0], "1.0": [-28, 0, 0]}},
        "leg_fl": {"rotation": {"0.0": [25, 0, 0], "0.5": [-25, 0, 0], "1.0": [25, 0, 0]}},
        "leg_br": {"rotation": {"0.0": [25, 0, 0], "0.5": [-25, 0, 0], "1.0": [25, 0, 0]}},
        "leg_fr": {"rotation": {"0.0": [-25, 0, 0], "0.5": [25, 0, 0], "1.0": [-25, 0, 0]}},
        "leg_bl": {"rotation": {"0.0": [-25, 0, 0], "0.5": [25, 0, 0], "1.0": [-25, 0, 0]}},
        "leg_l": {"position": {"0.0": [0, 0, 0], "0.25": [0, 1, 0], "0.5": [0, 0, 0]}},
        "leg_r": {"position": {"0.0": [0, 0, 0], "0.75": [0, 1, 0], "1.0": [0, 0, 0]}},
        "right_arm": {"rotation": {"0.0": [-20, 0, 0], "0.5": [12, 0, 0], "1.0": [-20, 0, 0]}},
        "left_arm": {"rotation": {"0.0": [12, 0, 0], "0.5": [-20, 0, 0], "1.0": [12, 0, 0]}},
        "tail": {"rotation": {"0.0": [0, -15, 0], "0.5": [0, 15, 0], "1.0": [0, -15, 0]}},
        "wheel_l": {"rotation": {"0.0": [0, 0, 0], "1.0": [-360, 0, 0]}},
        "wheel_r": {"rotation": {"0.0": [0, 0, 0], "1.0": [-360, 0, 0]}},
        "rotor": {"rotation": {"0.0": [0, 0, 0], "0.5": [0, 0, 360]}},
        "cape": {"rotation": {"0.0": [18, 0, 0], "0.5": [24, 0, 0], "1.0": [18, 0, 0]}},
        "body": {"position": {"0.0": [0, 0, 0], "0.25": [0, 0.6, 0], "0.5": [0, 0, 0], "0.75": [0, 0.6, 0], "1.0": [0, 0, 0]}},
    }
    if volant or ("wing_l" in os_ and "leg_fl" in os_):
        marche.update(flap)
        if volant:
            idle.update(flap)
    attaque = {
        "right_arm": {"rotation": {"0.0": [0, 0, 0], "0.2": [-160, 0, -10], "0.35": [-40, 0, 0], "0.6": [0, 0, 0]}},
        "rider_arm": {"rotation": {"0.0": [0, 0, 0], "0.2": [-120, 0, 0], "0.35": [-20, 0, 0], "0.6": [0, 0, 0]}},
        "neck": {"rotation": {"0.0": [0, 0, 0], "0.2": [-15, 0, 0], "0.35": [20, 0, 0], "0.6": [0, 0, 0]}},
        "jaw": {"rotation": {"0.0": [0, 0, 0], "0.2": [35, 0, 0], "0.35": [0, 0, 0]}},
        "body": {"rotation": {"0.0": [0, 0, 0], "0.2": [-5, 6, 0], "0.35": [8, -4, 0], "0.6": [0, 0, 0]}},
    }
    if "right_arm" not in os_ and "neck" not in os_ and "jaw" in os_:
        attaque["body"] = {"position": {"0.0": [0, 0, 0], "0.2": [0, 3, -2], "0.4": [0, 0, 0]}}
    A = {
        "misc.idle": {"loop": True, "animation_length": 3.0, "bones": idle},
        "move.walk": {"loop": True, "animation_length": 1.0, "bones": marche},
        "attack.swing": {"loop": False, "animation_length": 0.6, "bones": attaque},
        "misc.die": {"loop": "hold_on_last_frame", "animation_length": 1.0, "bones": {
            "root": {"rotation": {"0.0": [0, 0, 0], "1.0": [0, 0, 85]}}}},
    }
    for a in A.values():
        a["bones"] = {k: v for k, v in a["bones"].items() if k in os_}
    return A
