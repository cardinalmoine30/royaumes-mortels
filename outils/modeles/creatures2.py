# -*- coding: utf-8 -*-
"""Créatures détaillées (moteur v2) : bêtes et montures, dragons, navires Nuées, squigs et rejetons,
poissons de l'Ethersea, chars et roues. Mêmes clés de spécification que la v1."""
from modele2 import Modele, mul
from humanoide import materiaux, STYLE, f_bande, f_cadre, f_yeux, f_dents, f_eclair, f_etoile, f_crane, f_rayures, combine, f_comete

# matière de la peau des créatures
PEAU = {
    "ecaille": {"stardrake", "dracoth", "dragon", "magmadroth", "salamandre", "carnosaur", "stegadon", "bastiladon",
                "dragon_zombie", "ishlaen", "allopex", "morrsarr", "leviadon", "demon_slaanesh", "pusgoyle"},
    "plume": {"griffon", "gryph_charger", "demigryph"},
    "fourrure": {"sabre_givre", "thundertusk", "varghulf", "bete_zombie", "chien_khorne", "abomination"},
    "os": {"kavalos", "gothizzar"},
    "pierre": {"alarith", "stonehorn"},
    "ether": {"dreadblade", "carrosse_noir"},
    "metal": {"juggernaut"},
}


def mats_creature(nom, s, fac):
    st = dict(STYLE.get(fac, {}))
    for t, ids in PEAU.items():
        if nom in ids:
            st["peau"] = t
    mats = materiaux(s["pal"], st, dict(s, corps="bete", face="bete"))
    mats["corps"] = mats["peau"]
    mats["armure2b"] = mats["armure2"]
    return mats


def epines(m, bone, x, y, z0, z1, h=2.5, mat="corne", pas=3.0):
    z = z0
    k = 0
    while z < z1:
        hh = h * (1 - abs((z - z0) / max(1, z1 - z0) - 0.4))
        m.cube(bone, (x - 0.5, y, z), (1, max(0.8, hh), 1.2), mat)
        z += pas
        k += 1


def mini_cavalier(m, P, mats, fac, y0, z0, arme="lance", t=1.0):
    """Cavalier détaillé : casque, plastron, cape, bras armé."""
    A2 = P["armure2"]
    LU = P["lueur"]
    m.bone("rider", "body", (0, y0, z0))
    m.bone("rider_arm", "rider", (-4 * t, y0 + 9 * t, z0))
    m.cube("rider", (-3 * t, y0, z0 - 2 * t), (6 * t, 8 * t, 4 * t), "armure", north=combine(f_cadre(A2), f_comete(A2)))
    m.cube("rider", (-3.5 * t, y0 - 0.5, z0 - 2.5 * t), (7 * t, 1.5, 5 * t), "cuir")
    m.cube("rider", (-2 * t, y0 + 8 * t, z0 - 2 * t), (4 * t, 4 * t, 4 * t), "armure", north=f_yeux(LU, (14, 14, 18), 0.45, 0.22))
    m.cube("rider", (-0.5, y0 + 12 * t, z0 - 2 * t), (1, 1.5 * t, 4 * t), "armure2")
    m.cube("rider", (-4.5 * t, y0 + 6 * t, z0 - 2.5 * t), (2.5 * t, 2 * t, 5 * t), "armure2")
    m.cube("rider", (2 * t, y0 + 6 * t, z0 - 2.5 * t), (2.5 * t, 2 * t, 5 * t), "armure2")
    for sx in (-1, 1):
        m.cube("rider", (sx * 3.5 * t - (1 * t if sx < 0 else 0) - (1 if sx < 0 else 0) * 0, y0 - 3 * t, z0 - 1.5 * t), (2 * t, 4 * t, 3 * t), "armure")
    m.cube("rider", (2.5 * t, y0 + 2 * t, z0 - 1 * t), (2 * t, 5 * t, 2 * t), "armure")
    m.cube("rider", (-2.5 * t, y0 - 2, z0 + 2 * t), (5 * t, 9 * t, 0.5), "tissu", south=f_bande(A2, "bas"))
    m.cube("rider_arm", (-5 * t, y0 + 3 * t, z0 - 1 * t), (2 * t, 6 * t, 2 * t), "armure")
    if arme == "lance":
        m.cube("rider_arm", (-4.5 * t, y0 + 3.5 * t, z0 - 20 * t), (1, 1, 22 * t), "manche")
        m.cube("rider_arm", (-5 * t, y0 + 3 * t, z0 - 24 * t), (2, 2, 4), "lame")
        m.cube("rider_arm", (-4.25 * t, y0 + 4.5 * t, z0 - 18 * t), (0.5, 3, 4), "tissu", east=f_bande(A2, "bas"), west=f_bande(A2, "bas"))
    elif arme == "fusil":
        m.cube("rider_arm", (-5 * t, y0 + 3 * t, z0 - 12 * t), (2, 2, 12 * t), "metal")
    else:
        m.cube("rider_arm", (-4.5 * t, y0 + 2 * t, z0 - 2 * t), (1, 12 * t, 2), "lame" if arme == "epee" else "manche")
        if arme in ("hache", "marteau"):
            m.cube("rider_arm", (-6 * t, y0 + 11 * t, z0 - 3 * t), (3.5, 3, 4), "metal", toutes=f_cadre(mul(P["metal"], 0.7)))


def bete(nom, s, fac):
    import betes
    f = betes.forme(nom)
    if f:
        return f(nom, s, fac)
    P = s["pal"]
    mats = mats_creature(nom, s, fac)
    LU, A2 = P["lueur"], P["armure2"]
    m = Modele(nom)
    W, H, L = s.get("corps", (8, 8, 10))     # largeur, hauteur, longueur
    lw, lh = s.get("jambe", (3, 8))
    ys = lh
    m.bone("root", None, (0, 0, 0))
    m.bone("body", "root", (0, lh + H / 2, 0))
    # corps : torse avant plus large, arrière-train, ventre
    m.cube("body", (-W / 2, ys, -L / 2), (W, H, L * 0.55), "corps")
    m.cube("body", (-W / 2 + 0.5, ys + 0.5, -L / 2 + L * 0.5), (W - 1, H - 1, L * 0.5), "corps")
    m.cube("body", (-W / 2 + 1, ys - 0.5, -L / 2 + 1.5), (W - 2, 0.5, L - 3), "ventre")
    if s.get("crete_dos"):
        epines(m, "body", 0, ys + H, -L / 2 + 1, L / 2 - 1, h=2.5 if L > 14 else 1.5)
    if s.get("carapace"):
        m.cube("body", (-W / 2 - 1, ys + H - 2.5, -L / 2 + 0.5), (W + 2, 4.5, L - 1), "armure",
               up=combine(f_cadre(A2), f_rayures(mul(P["armure"], 0.6), A2) if fac == "seraphon" else None), toutes=f_bande(A2, "bas", 2))
        for k in range(3):
            m.cube("body", (-W / 2 - 1.5, ys + H - 3, -L / 2 + 2 + k * (L - 4) / 3), (0.5, 3, (L - 4) / 3 - 0.5), "armure2")
            m.cube("body", (W / 2 + 1, ys + H - 3, -L / 2 + 2 + k * (L - 4) / 3), (0.5, 3, (L - 4) / 3 - 0.5), "armure2")
    if s.get("plaques"):
        for i in range(int((L - 4) // 3)):
            hh = 3 + (i % 2) * 2
            m.cube("body", (-1, ys + H, -L / 2 + 2 + i * 3), (2, hh, 2.5), "armure2", north=f_bande(LU, "haut"))
    if s.get("caparacon"):
        m.cube("body", (-W / 2 - 0.5, ys - 2.5, -L / 2 + 1), (W + 1, H - 1, L * 0.6), "tissu",
               east=combine(f_bande(A2, "bas", 2), f_comete(A2)), west=combine(f_bande(A2, "bas", 2), f_comete(A2)))
        m.cube("body", (-W / 2 - 0.5, ys + H - 1, -L / 2), (W + 1, 1, 3), "armure")
    # selle
    if s.get("cavalier"):
        m.cube("body", (-W / 2 + 0.5, ys + H, -2.5), (W - 1, 1, 6), "cuir", toutes=f_bande(A2, "haut"))
        m.cube("body", (-W / 2 + 0.5, ys + H + 1, 2.5), (W - 1, 1.5, 1), "cuir")
        for sx in (-1, 1):
            m.cube("body", (sx * W / 2 - (0.5 if sx < 0 else 0), ys + 1, -1), (0.5, H - 1, 1), "cuir")
            m.cube("body", (sx * W / 2 - (1 if sx < 0 else 0), ys, -1.5), (1, 1, 2), "metal")
    # pattes : cuisse, jambe, pied griffu
    for nomj, sx, sz in (("leg_fl", -1, -1), ("leg_fr", 1, -1), ("leg_bl", -1, 1), ("leg_br", 1, 1)):
        x = -W / 2 if sx < 0 else W / 2 - lw
        z = -L / 2 + 1 if sz < 0 else L / 2 - lw - 1
        m.bone(nomj, "root", (x + lw / 2, lh, z + lw / 2))
        m.cube(nomj, (x - 0.5, lh * 0.5, z - 0.5), (lw + 1, lh * 0.55, lw + 1), "corps")
        m.cube(nomj, (x, 1, z), (lw, lh * 0.55, lw), "corps")
        if s.get("sabots"):
            m.cube(nomj, (x - 0.25, 0, z - 0.25), (lw + 0.5, 1.5, lw + 0.5), "sombre")
        else:
            m.cube(nomj, (x - 0.5, 0, z - 1), (lw + 1, 1.2, lw + 1), "corps")
            for k in range(3 if lw >= 3 else 2):
                m.cube(nomj, (x + k * (lw - 0.5) / 2, 0, z - 2), (0.6, 0.8, 1.2), "corne")
        if s.get("carapace") or s.get("caparacon"):
            m.cube(nomj, (x - 0.5, lh * 0.6, z - 0.75), (lw + 1, 1.5, 0.5), "armure2")
    # cou + tête
    tw, th, td = s.get("tete", (6, 6, 7))
    cou = s.get("cou", 4)
    yt = ys + H - 2 + cou / 2
    m.bone("neck", "body", (0, ys + H - 3, -L / 2))
    if cou:
        n = 2 if cou > 4 else 1
        for k in range(n):
            ww = max(3.5, tw - 2 - k)
            m.cube("neck", (-ww / 2, ys + H - 4 + k * cou / (2 * n), -L / 2 - cou * (k + 1) / n - 0.5), (ww, max(4, th - 1 - k), cou / n + 1), "corps")
            if s.get("criniere"):
                m.cube("neck", (-1, ys + H - 0.5 + k * cou / (2 * n), -L / 2 - cou * (k + 1) / n), (2, 2.5, cou / n + 1), "poils")
            elif s.get("crete_dos"):
                m.cube("neck", (-0.5, ys + H - 0.5 + k * cou / (2 * n) + max(4, th - 1 - k) - 2, -L / 2 - cou * (k + 1) / n + 0.5), (1, 1.5, 1.2), "corne")
    zt = -L / 2 - cou - td + 1
    m.bone("head", "neck", (0, yt, zt + td))
    m.cube("head", (-tw / 2, yt, zt), (tw, th, td), "corps",
           east=f_yeux(LU, (14, 14, 16), 0.32, 0.25), west=f_yeux(LU, (14, 14, 16), 0.32, 0.25),
           north=f_yeux(LU, (14, 14, 16), 0.3, 0.3))
    m.cube("head", (-tw / 2 - 0.25, yt + th - 1.5, zt - 0.25), (tw + 0.5, 1.5, td * 0.6), "corps")              # arcade
    m.bone("jaw", "head", (0, yt, zt + td))
    if s.get("bec"):
        m.cube("head", (-2, yt + 1, zt - 3), (4, 3, 3.5), "corne")
        m.cube("head", (-1.5, yt + 0.5, zt - 4.5), (3, 2, 2), "corne")
        m.cube("head", (-1, yt - 0.5, zt - 5.5), (2, 1.5, 1.5), "corne")
        m.cube("jaw", (-1.5, yt - 1, zt - 2.5), (3, 1.5, 3), "corne")
    else:
        m.cube("head", (-tw / 2 + 0.5, yt + 0.5, zt - td * 0.45), (tw - 1, th * 0.5, td * 0.5), "corps",
               north=lambda d, x, y, w, h, px: (d.point((x + 2, y + 1), fill=(10, 10, 10)), d.point((x + w - 3, y + 1), fill=(10, 10, 10))))
        m.cube("jaw", (-tw / 2 + 1, yt - 1.5, zt - td * 0.4), (tw - 2, 1.5, td * 0.85), "corps", north=f_dents(), up=f_dents())
        for sx in (-1, 1):
            m.cube("head", (sx * (tw / 2 - 1.5) - 0.5, yt - 0.5, zt - td * 0.4 + 0.5), (1, 1.5, 1), "dent")
    if s.get("cornes"):
        segs = [(0, 0, 2, 2), (1.5, 1.2, 1.7, 2.5), (2.4, 3.2, 1.3, 2.5), (2.6, 5.4, 1, 1.8)]
        for sx in (-1, 1):
            for dx, dy, w, h in segs:
                x = sx * (tw / 2 + dx) - (w if sx < 0 else 0)
                m.cube("head", (x, yt + th - 2 + dy, zt + td - 3), (w, h, w), "corne")
    if s.get("corne_nez"):
        m.cube("head", (-1, yt + th - 1, zt - 2), (2, 2.5, 2), "corne")
        m.cube("head", (-0.75, yt + th + 1.5, zt - 2.5), (1.5, 2.5, 1.5), "corne")
        m.cube("head", (-0.5, yt + th + 4, zt - 3), (1, 1.5, 1), "corne")
    if s.get("defenses"):
        for sx in (-1, 1):
            m.cube("head", (sx * (tw / 2 - 1) - 1, yt - 2, zt - 1), (2, 2, 3), "dent")
            m.cube("head", (sx * (tw / 2 - 1) - 0.75, yt - 3.5, zt - 3.5), (1.5, 1.5, 3), "dent")
            m.cube("head", (sx * (tw / 2 - 1) - 0.5, yt - 3, zt - 5.5), (1, 1.5, 2), "dent")
    if s.get("collerette"):
        m.cube("head", (-tw / 2 - 3, yt - 1, zt + td - 1), (tw + 6, th + 4, 1), "armure2", south=f_cadre(LU), north=f_bande(LU, "haut"))
    if s.get("criniere"):
        m.cube("head", (-1.5, yt + th, zt + 1), (3, 2.5, td - 1), "poils")
    # queue segmentée
    q = s.get("queue", 6)
    if q:
        m.bone("tail", "body", (0, ys + H - 2, L / 2))
        segs = 3 if q > 6 else 2
        z = L / 2
        for k in range(segs):
            w = max(1, 3.5 - k * 1.0)
            ln = q / segs + 0.5
            m.cube("tail", (-w / 2, ys + H - 3.5 - k * 0.8, z), (w, w, ln), "corps", up=None)
            if s.get("crete_dos") and w > 1.5:
                m.cube("tail", (-0.5, ys + H - 3.5 - k * 0.8 + w, z + 0.5), (1, 1, 1), "corne")
            z += ln - 0.5
        if s.get("queue_massue"):
            m.cube("tail", (-2.5, ys + H - 6, z), (5, 5, 4), "armure2", toutes=f_cadre(mul(A2, 0.7)))
            for (dx, dy) in ((-3, 1.5), (2.5, 1.5), (-0.5, 4.5)):
                m.cube("tail", (dx, ys + H - 6 + dy, z + 1), (1, 1, 1.5), "corne")
        elif s.get("dard"):
            m.cube("tail", (-1, ys + H - 4, z), (2, 5, 2), "corne")
            m.cube("tail", (-0.5, ys + H + 1, z - 1), (1, 2, 1.5), "lueur")
    # ailes : bras osseux, doigts, membrane (ou plumes)
    e = s.get("ailes", 0)
    if e:
        plume = nom in PEAU["plume"]
        for nomb, sx in (("wing_l", 1), ("wing_r", -1)):
            m.bone(nomb, "body", (sx * W / 2, ys + H, -L / 4))
            x0 = W / 2 if sx > 0 else -W / 2 - e
            m.cube(nomb, (x0, ys + H - 0.5, -L / 4 - 1.5), (e, 1.5, 1.5), "corne" if not plume else "corps")
            if plume:
                for k in range(3):
                    m.cube(nomb, (x0 + (e * k / 6 if sx > 0 else 0), ys + H - 0.25, -L / 4 + k * 3), (e * (1 - k / 6), 0.5, 3.5), "plume")
            else:
                ld = max(6, L / 2 + 2)
                for k in range(3):
                    xx = x0 + (e * (k + 1) / 4 if sx > 0 else e * (3 - k) / 4)
                    m.cube(nomb, (xx - 0.5, ys + H - 0.25, -L / 4), (1, 1, ld - k * 1.5), "corne")
                m.cube(nomb, (x0, ys + H - 0.25, -L / 4), (e, 0.5, ld), "membrane")
    # cavalier / nacelle / autel
    if s.get("cavalier"):
        mini_cavalier(m, P, mats, fac, ys + H + 1, -1, s.get("arme_cavalier", "lance"), s.get("taille_cavalier", 1))
    if s.get("nacelle"):
        m.cube("body", (-W / 2 + 0.5, ys + H, -3), (W - 1, 5, 9), "bois", toutes=f_bande(A2, "haut", 2))
        for (x, z) in ((-W / 2 + 0.5, -3), (W / 2 - 1.5, -3), (-W / 2 + 0.5, 5), (W / 2 - 1.5, 5)):
            m.cube("body", (x, ys + H + 5, z), (1, 4, 1), "or")
        m.cube("body", (-W / 2 + 0.5, ys + H + 9, -3), (W - 1, 0.5, 9), "tissu", up=f_bande(A2, "bas"))
        if fac == "seraphon":
            m.cube("body", (-1.5, ys + H + 5, 0), (3, 3, 3), "lueur")
    if s.get("autel"):
        m.cube("body", (-3, ys + H, -2), (6, 8, 6), "or", north=f_etoile(LU) if fac != "seraphon" else f_comete(LU))
        m.cube("body", (-2, ys + H + 8, -1), (4, 4, 4), "lueur")
    return m, mats


def navire(nom, s, fac):
    P = s["pal"]
    mats = mats_creature(nom, s, fac)
    LU, A2 = P["lueur"], P["armure2"]
    m = Modele(nom)
    L, W, H = s.get("coque", (24, 10, 7))
    m.bone("root", None, (0, 0, 0))
    m.bone("body", "root", (0, 6, 0))
    planches = lambda d, x, y, w, h, px: [d.line((x, y + k, x + w - 1, y + k), fill=(60, 42, 28)) for k in range(2, h, 3)]
    m.cube("body", (-W / 2, 4, -L / 2), (W, H, L), "bois", east=combine(planches, f_bande(A2, "haut", 2)), west=combine(planches, f_bande(A2, "haut", 2)))
    m.cube("body", (-W / 2 + 1.5, 2.5, -L / 2 + 1), (W - 3, 1.5, L - 2), "bois")                                # quille
    m.cube("body", (-W / 2 + 2, 4, -L / 2 - 4), (W - 4, H - 1, 4), "bois", east=planches, west=planches)         # proue
    m.cube("body", (-W / 2 + 3.5, 4.5, -L / 2 - 7), (W - 7, H - 2.5, 3), "armure2")
    m.cube("body", (-1, 3.5, -L / 2 - 10), (2, 2.5, 4), "armure2")                                                # éperon
    for z in range(int(-L / 2 + 3), int(L / 2 - 2), 5):                                                           # hublots
        for sx in (-1, 1):
            m.cube("body", (sx * W / 2 - (0.5 if sx < 0 else 0), 4 + H * 0.45, z), (0.5, 1.5, 1.5), "lueur")
    m.cube("body", (-W / 2, 4 + H, -L / 2), (W, 0.5, L), "armure", up=f_cadre(A2))                                 # pont
    for sx in (-1, 1):                                                                                             # bastingage
        m.cube("body", (sx * W / 2 - (0.5 if sx < 0 else 0), 4.5 + H, -L / 2), (0.5, 1.5, L), "or")
    m.cube("body", (-W / 2 + 1, 4.5 + H, L / 2 - 6), (W - 2, 4, 5), "armure", north=f_cadre(A2))                 # timonerie
    m.cube("body", (-1, 4 + H, -2), (2, 10, 2), "metal")
    yb_ = s.get("ballon_y", 14)
    m.bone("ballon", "body", (0, yb_ + H, 0))
    bw, bh, bl = s.get("ballon", (W + 2, 8, L - 4))
    m.cube("ballon", (-bw / 2, yb_ + H, -bl / 2), (bw, bh, bl), "tissu", east=f_bande(A2, "haut"), west=f_bande(A2, "haut"))
    for k in range(3):
        m.cube("ballon", (-bw / 2 - 0.5, yb_ + H - 0.5, -bl / 2 + 1 + k * (bl - 2) / 2.2), (bw + 1, bh + 1, 1), "or")
    m.cube("ballon", (-1.5, yb_ + H + bh * 0.3, -bl / 2 - 1), (3, 3, 1), "lueur")
    for sx in (-1, 1):                                                                     # haubans
        m.cube("ballon", (sx * (bw / 2 - 1) - 0.25, 4.5 + H, -bl / 4), (0.5, yb_ - 4.5, 0.5), "metal")
        m.cube("ballon", (sx * (bw / 2 - 1) - 0.25, 4.5 + H, bl / 4), (0.5, yb_ - 4.5, 0.5), "metal")
    m.bone("rotor", "body", (0, 4 + H / 2, L / 2 + 2))
    m.cube("rotor", (-5, 4 + H / 2 - 0.75, L / 2 + 1.5), (10, 1.5, 0.5), "metal")
    m.cube("rotor", (-0.75, 4 + H / 2 - 5, L / 2 + 1.5), (1.5, 10, 0.5), "metal")
    m.cube("rotor", (-1, 4 + H / 2 - 1, L / 2 + 1), (2, 2, 1.5), "or")
    for i in range(s.get("canons", 1)):
        x = -W / 2 + 2 + i * 3.5
        m.cube("body", (x, 5 + H, -L / 2 - 2), (2, 2, 7), "metal", north=f_cadre(LU))
        m.cube("body", (x - 0.25, 4.75 + H, -L / 2 - 2.5), (2.5, 2.5, 1), "or")
    if s.get("selle"):
        m.cube("body", (-2, 4.5 + H, 2), (4, 1, 4), "cuir")
        m.selle = (5.5 + H, 3.5)
    for x in ((-W / 4, W / 4) if not s.get("selle") else ()):
        m.cube("body", (x - 1.5, 4.5 + H, 1), (3, 4, 3), "armure", north=f_yeux(LU, (14, 14, 18), 0.4, 0.2))
        m.cube("body", (x - 1, 8.5 + H, 1.5), (2, 2.5, 2), "armure", north=lambda d, x, y, w, h, px: d.ellipse((x + 1, y + 1, x + w - 2, y + h - 2), fill=LU))
    return m, mats


def blob(nom, s, fac):
    if nom.startswith("squig"):
        import betes
        return betes.squig(nom, s, fac)
    P = s["pal"]
    mats = mats_creature(nom, s, fac)
    LU = P["lueur"]
    m = Modele(nom)
    r = s.get("taille", 10)
    m.bone("root", None, (0, 0, 0))
    m.bone("body", "root", (0, r / 2 + 2, 0))
    m.cube("body", (-r / 2, 4, -r / 2), (r, r - 2, r), "corps")
    m.cube("body", (-r / 2 + 1, r + 2, -r / 2 + 1), (r - 2, 1.5, r - 2), "corps")
    m.cube("body", (-r / 2 - 0.5, 5, -r / 2 + 1), (r + 1, r - 5, r - 2), "corps")
    for sx in (-1, 1):                                                                                  # yeux sur le dessus
        m.cube("body", (sx * r / 4 - 1, r + 1.5, -r / 2 + 1), (2, 2, 2), "blanc",
               north=lambda d, x, y, w, h, px: d.rectangle((x + 1, y + 1, x + 2, y + 2), fill=(12, 12, 12)))
    m.bone("jaw", "body", (0, 4, -r / 2))
    m.cube("jaw", (-r / 2 + 0.5, 2, -r / 2 - 0.5), (r - 1, 2.5, r - 1), "ventre", north=f_dents(), up=f_dents())
    m.cube("body", (-r / 2 + 0.5, 4, -r / 2 - 0.5), (r - 1, 1, 0.5), "dent", north=f_dents((250, 248, 236)))
    m.cube("body", (-r / 2 + 1, 4.5, -r / 2 + 0.5), (r - 2, r * 0.3, 0.5), "sombre")                    # gueule ouverte
    for nomj, x in (("leg_l", -r / 2 + 1), ("leg_r", r / 2 - 3)):
        m.bone(nomj, "root", (x + 1, 3, 0))
        m.cube(nomj, (x, 0.5, -1), (2, 3, 3), "corps")
        m.cube(nomj, (x - 0.25, 0, -2), (2.5, 1, 3.5), "corps")
        for k in range(2):
            m.cube(nomj, (x + k * 1.2, 0, -2.75), (0.6, 0.6, 1), "corne")
    if s.get("tentacules"):
        for i, (x, z, ln) in enumerate(((-r / 2 - 2, 0, 6), (r / 2, -2, 7), (-2, r / 2, 6), (r / 2, r / 4, 5))):
            for k in range(3):
                w = 2 - k * 0.5
                m.cube("body", (x + k * 0.5, 4 + i + k * 2, z), (w, 2.5, w), "membrane")
            m.cube("body", (x + 1, 4 + i + 6, z), (1, 1, 1), "lueur")
    if s.get("cornes"):
        for sx in (-1, 1):
            for k, (dx, dy, w, h) in enumerate(((0, 0, 2, 2.5), (0.8, 2.3, 1.5, 2.5), (1.3, 4.6, 1, 2))):
                m.cube("body", (sx * (r / 2 - 1 + dx) - (w if sx < 0 else 0), r + 1 + dy, -1), (w, h, w), "corne")
    if s.get("pustules"):
        for x, y, z in ((-r / 2 - 1, 6, -2), (r / 2, 8, 1), (-2, r + 3, 0), (1, 6, r / 2), (r / 2, 5, -3)):
            m.cube("body", (x, y, z), (1.5, 1.5, 1.5), "lueur")
    if s.get("rats"):
        for x, y, z in ((-r / 2 - 2, 5, -2), (r / 2, 6, 1), (-1, 5, r / 2), (r / 3, r, -1)):
            m.cube("body", (x, y, z), (3, 2.5, 4), "poils", north=f_yeux((255, 60, 60), None, 0.4, 0.2))
    if s.get("cavalier"):
        mini_cavalier(m, P, mats, fac, r + 3, 0, s.get("arme_cavalier", "lance"))
    return m, mats


def poisson(nom, s, fac):
    P = s["pal"]
    mats = mats_creature(nom, s, fac)
    LU, A2 = P["lueur"], P["armure2"]
    m = Modele(nom)
    L, W, H = s.get("corps", (16, 6, 6))
    m.bone("root", None, (0, 0, 0))
    m.bone("body", "root", (0, 6 + H / 2, 0))
    m.cube("body", (-W / 2, 6, -L / 2), (W, H, L * 0.6), "corps")
    m.cube("body", (-W / 2 + 0.5, 6.5, -L / 2 + L * 0.55), (W - 1, H - 1, L * 0.45), "corps")
    m.cube("body", (-W / 2 + 1, 5.5, -L / 2 + 1), (W - 2, 0.5, L - 2), "ventre")
    m.bone("head", "body", (0, 6 + H / 2, -L / 2))
    m.cube("head", (-W / 2 + 0.5, 6.5, -L / 2 - 5), (W - 1, H - 1.5, 5), "corps", east=f_yeux(LU, None, 0.3, 0.2), west=f_yeux(LU, None, 0.3, 0.2))
    m.cube("head", (-W / 2 + 1.5, 7, -L / 2 - 7), (W - 3, H - 3, 2), "corps")
    m.bone("jaw", "head", (0, 6.5, -L / 2))
    m.cube("jaw", (-W / 2 + 1, 5, -L / 2 - 6), (W - 2, 1.5, 6), "ventre", north=f_dents(), up=f_dents())
    for k in range(3):
        m.cube("body", (-0.5, 6 + H, -2 + k * 1.5), (1, 4 - k, 1.5), "membrane")                     # aileron dorsal
    for nomb, sx in (("wing_l", 1), ("wing_r", -1)):
        m.bone(nomb, "body", (sx * W / 2, 7, -2))
        m.cube(nomb, (W / 2 if sx > 0 else -W / 2 - 6, 7, -3.5), (6, 0.5, 5), "membrane")
    m.bone("tail", "body", (0, 6 + H / 2, L / 2))
    m.cube("tail", (-W / 2 + 1.5, 7, L / 2), (W - 3, H - 2.5, 4), "corps")
    m.cube("tail", (-W / 2 + 2.5, 7.5, L / 2 + 4), (W - 5, H - 3.5, 3), "corps")
    m.cube("tail", (-0.25, 4, L / 2 + 6), (0.5, H + 5, 4), "membrane")
    if s.get("carapace"):
        m.cube("body", (-W / 2 - 2, 6 + H - 1, -L / 2 + 1), (W + 4, 4, L - 2), "armure",
               up=combine(f_cadre(A2), f_rayures(mul(P["armure"], 0.6), A2)), toutes=f_bande(A2, "bas", 2))
        for sx in (-1, 1):
            m.cube("body", (sx * (W / 2 + 1) - 1.5, 3, -L / 4), (3, 4, 3), "corps")
            m.cube("body", (sx * (W / 2 + 1) - 1.5, 3, L / 4), (3, 4, 3), "corps")
    if s.get("lanternes"):
        m.cube("head", (-0.25, 6 + H - 1, -L / 2 - 8), (0.5, 0.5, 4), "corne", rot=(20, 0, 0), pivot=(0, 6 + H - 1, -L / 2 - 4))
        m.cube("head", (-1, 6 + H, -L / 2 - 10), (2, 2, 2), "lueur")
    if s.get("selle"):
        m.cube("body", (-W / 2 + 0.5, 6 + H - 0.2, -2.5), (W - 1, 1, 5), "cuir", toutes=f_bande(A2, "haut"))
        m.selle = (6 + H + 0.8, 0)
    if s.get("cavalier"):
        mini_cavalier(m, P, mats, fac, 6 + H + 0.5, 0, s.get("arme_cavalier", "lance"))
    return m, mats


def roue(m, bone, cx, cy, cz, R, e, n=10, jante="bois", bandage="metal", rayon="bois", moyeu="metal", lame=None, sx=1):
    """Vraie roue en volume dans le plan YZ (elle tourne autour de X) : jante en segments, bandage de fer cloué,
    rayons, moyeu et chapeau ; lame de faux optionnelle sur le moyeu (côté sx)."""
    import math
    t = max(0.8, R * 0.16)
    seg = 2 * R * math.sin(math.pi / n) + 0.35
    piv = (cx, cy, cz)
    for k in range(n):
        a = k * 360.0 / n
        m.cube(bone, (cx - e / 2, cy + R - t, cz - seg / 2), (e, t, seg), jante, rot=(a, 0, 0), pivot=piv)
        m.cube(bone, (cx - e / 2 - 0.15, cy + R - 0.05, cz - seg / 2 + 0.1), (e + 0.3, 0.45, seg - 0.2), bandage, rot=(a, 0, 0), pivot=piv)
        if k % 2 == 0:
            m.cube(bone, (cx - e / 2 - 0.3, cy + R - 0.35, cz - 0.3), (e + 0.6, 0.6, 0.6), "or", rot=(a, 0, 0), pivot=piv)   # clou
    nr = max(3, n // 2)
    for k in range(nr):
        a = k * 180.0 / nr
        m.cube(bone, (cx - e * 0.3, cy - (R - t), cz - 0.4), (e * 0.6, 2 * (R - t), 0.8), rayon, rot=(a, 0, 0), pivot=piv)
    hm = max(1.6, R * 0.32)
    m.cube(bone, (cx - e / 2 - 0.6, cy - hm / 2, cz - hm / 2), (e + 1.2, hm, hm), moyeu)
    m.cube(bone, (cx - e / 2 - 1.2, cy - hm / 4, cz - hm / 4), (e + 2.4, hm / 2, hm / 2), "or")
    if lame:
        x = cx + sx * (e / 2 + 1.2) - (0 if sx > 0 else 4)
        m.cube(bone, (x, cy - 0.3, cz - 0.6), (4, 0.6, 1.2), lame)
        m.cube(bone, (x + (3 if sx > 0 else 0), cy - 0.3, cz - 2.2), (1, 0.6, 2.2), lame)


def rat_coureur(m, bone, x, y, z):
    """Petit rat qui court dans la grande roue."""
    m.cube(bone, (x - 1.2, y + 1.2, z - 2), (2.4, 2.2, 4), "poils")
    m.cube(bone, (x - 1, y + 1.8, z - 3.6), (2, 1.8, 1.8), "poils", north=f_yeux((255, 60, 60), None, 0.35, 0.22))
    m.cube(bone, (x - 0.4, y + 1.9, z - 4.4), (0.8, 0.8, 0.9), "rose")
    for sx in (-1, 1):
        m.cube(bone, (x + sx * 0.7 - 0.3, y + 3.5, z - 3.2), (0.6, 0.8, 0.4), "rose")
    for (dx, dz) in ((-0.9, -1.5), (0.4, -1.5), (-0.9, 1.0), (0.4, 1.0)):
        m.cube(bone, (x + dx, y, z + dz), (0.5, 1.3, 0.6), "poils")
    m.cube(bone, (x - 0.25, y + 1.6, z + 2), (0.5, 0.5, 3.5), "rose", rot=(-20, 0, 0), pivot=(x, y + 1.8, z + 2))


def char(nom, s, fac):
    P = s["pal"]
    mats = mats_creature(nom, s, fac)
    LU, A2 = P["lueur"], P["armure2"]
    m = Modele(nom)
    L, W, H = s.get("caisse", (12, 10, 6))
    m.bone("root", None, (0, 0, 0))
    m.bone("body", "root", (0, 8, 0))
    rayons = lambda d, x, y, w, h, px: (d.ellipse((x, y, x + w - 1, y + h - 1), outline=mul(P["metal"], 1.0)),
                                        d.line((x + w // 2, y, x + w // 2, y + h - 1), fill=P["metal"]),
                                        d.line((x, y + h // 2, x + w - 1, y + h // 2), fill=P["metal"]),
                                        d.ellipse((x + w // 2 - 2, y + h // 2 - 2, x + w // 2 + 1, y + h // 2 + 1), fill=A2))
    if s.get("roue_geante"):
        R = 11
        m.bone("wheel_l", "body", (0, R, 0))
        for x in (-4.5, 4.5):
            roue(m, "wheel_l", x, R, 0, R, 1.2, n=14)
        import math
        for k in range(8):                                                        # barreaux de la cage (marches des rats)
            an = k * math.pi / 4
            m.cube("wheel_l", (-4.5, R + math.sin(an) * (R - 1.2) - 0.4, math.cos(an) * (R - 1.2) - 0.4), (9, 0.8, 0.8), "metal")
        m.cube("wheel_l", (-5.5, R - 0.8, -0.8), (11, 1.6, 1.6), "metal")              # essieu
        # générateur de malefoudre au centre, avec ses bobines et ses plaques rivetées
        m.cube("body", (-3, R - 3, -3), (6, 6, 6), "metal", north=f_eclair(LU), south=f_eclair(LU))
        for sx in (-1, 1):
            m.cube("body", (sx * 3.2 - (0.6 if sx < 0 else 0), R - 2.5, -2.5), (0.6, 5, 5), "armure2")
        for k in range(3):
            m.cube("body", (-3.4, R - 2.2 + k * 1.8, -3.4), (6.8, 0.6, 6.8), "or")      # bobines de cuivre
        m.cube("body", (-1, R + 3, -1), (2, 4, 2), "lueur")                             # fangepierre
        m.cube("body", (-1.6, R + 7, -1.6), (3.2, 0.8, 3.2), "metal")
        for sx in (-1, 1):                                                              # paratonnerres
            m.cube("body", (sx * 1.6 - 0.25, R + 7.5, -0.25), (0.5, 4, 0.5), "metal", rot=(0, 0, sx * 18), pivot=(sx * 1.6, R + 7.5, 0))
            m.cube("body", (sx * 2.6 - 0.5, R + 11, -0.5), (1, 1, 1), "lueur")
        # canon à malefoudre à l'avant et pilote
        m.cube("body", (-0.8, R - 1, -10), (1.6, 1.6, 7), "metal")
        m.cube("body", (-1.2, R - 1.4, -11), (2.4, 2.4, 1.2), "lueur")
        m.cube("body", (-1.5, R + 3.5, 2.5), (3, 3, 3), "poils", north=f_yeux((255, 60, 60), None, 0.35, 0.2))
        for x in (-2.2, 2.2):                                                           # rats qui courent au fond
            rat_coureur(m, "body", x, 1.4, 0)
        return m, mats
    planches = lambda d, x, y, w, h, px: [d.line((x, y + k, x + w - 1, y + k), fill=mul(mats["bois"]["c"], 0.6)) for k in range(2, h, 3)]
    m.cube("body", (-W / 2, 6, -L / 2), (W, H, L), "bois", north=combine(planches, f_bande(A2, "haut", 2)),
           east=combine(planches, f_bande(A2, "haut", 2)), west=combine(planches, f_bande(A2, "haut", 2)))
    m.cube("body", (-W / 2 - 0.5, 6 + H - 1, -L / 2 - 0.5), (W + 1, 1, L + 1), "or")
    m.cube("body", (-1, 4, -L / 2 - 8), (2, 2, 9), "bois")                                                     # timon
    for nomb, x, sx in (("wheel_l", -W / 2 - 1, -1), ("wheel_r", W / 2 + 1, 1)):
        m.bone(nomb, "body", (x, 5, 0))
        roue(m, nomb, x, 5, 0, 5, 1.4, n=10,
             lame="lame" if fac in ("esclaves", "khorne", "tzeentch", "nurgle", "slaanesh", "skaven") else None, sx=sx)
    # caisse : coins ferrés, plaque avant rivetée, essieu
    m.cube("body", (-W / 2 - 1, 4.3, -0.7), (W + 2, 1.4, 1.4), "metal")
    for (x, z) in ((-W / 2 - 0.4, -L / 2 - 0.4), (W / 2 - 0.6, -L / 2 - 0.4), (-W / 2 - 0.4, L / 2 - 0.6), (W / 2 - 0.6, L / 2 - 0.6)):
        m.cube("body", (x, 6, z), (1, H, 1), "metal")
    m.cube("body", (-W / 2 + 1, 6.5, -L / 2 - 0.6), (W - 2, H - 2, 0.6), "armure2", north=f_cadre(mul(A2, 0.7)))
    if s.get("toit"):
        m.cube("body", (-W / 2 + 1, 6 + H, -2), (W - 2, 9, L / 2 + 2), "tissu",
               north=combine(f_yeux(LU, (10, 10, 14), 0.4, 0.25), f_cadre(A2)))
        m.cube("body", (-W / 2, 15 + H, -3), (W, 1.5, L / 2 + 4), "armure2")
        for (x, z) in ((-W / 2, -3), (W / 2 - 1, -3), (-W / 2, L / 2 - 0.5), (W / 2 - 1, L / 2 - 0.5)):
            m.cube("body", (x, 6 + H, z), (1, 9, 1), "or")
        if fac == "nighthaunt":
            m.cube("body", (-1, 16.5 + H, -1), (2, 3, 2), "lueur")
            m.cube("body", (-W / 2 - 1, 8, -L / 2 - 1), (0.5, 7, 0.5), "chaine")
        if s.get("autel"):
            m.cube("body", (-2, 16.5 + H, -1), (4, 6, 4), "lueur", north=f_etoile(A2))
            m.cube("body", (-3, 22.5 + H, -2), (6, 1, 6), "armure2")
    if s.get("disque"):
        m.cube("body", (-W / 2 - 3, 4, -L / 2 - 3), (W + 6, 2, L + 6), "lueur", up=f_etoile(A2))
        m.cube("body", (-W / 2 - 2, 3, -L / 2 - 2), (W + 4, 1, L + 4), "armure2")
    mini_cavalier(m, P, mats, fac, 6 + H, -L / 4, s.get("arme_cavalier", "epee"))
    if s.get("betes"):
        m.bone("beast", "body", (0, 6, -L / 2 - 8))
        bz = -L / 2 - 16
        m.cube("beast", (-3, 4, bz), (6, 6, 11), "corps" if fac != "nighthaunt" else "tissu")
        m.cube("beast", (-2, 7, bz - 4), (4, 4, 5), "corps", north=f_yeux(LU, None, 0.35, 0.25))
        m.cube("beast", (-0.5, 10, bz - 2), (1, 2.5, 5), "poils")
        for (x, z) in ((-3, bz + 1), (1.5, bz + 1), (-3, bz + 8), (1.5, bz + 8)):
            m.cube("beast", (x, 0, z), (1.5, 4.5, 1.5), "corps")
            m.cube("beast", (x - 0.25, 0, z - 0.25), (2, 1, 2), "sombre")
    return m, mats
