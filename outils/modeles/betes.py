# -*- coding: utf-8 -*-
"""Bêtes v3 : silhouettes organiques par familles (chevaux, griffons, dragons, fauves, mastodontes,
carnosaure, squigs). Membres articulés en segments inclinés, cous et queues courbés, ailes levées
(plumes en éventail ou membrane tendue entre les doigts).

Conventions : avant du modèle = -z, haut = +y. Rotation de cube [rx, ry, rz] (ordre x puis y puis z) :
rx > 0 relève un segment orienté vers l'arrière, ry > 0 tourne +z vers +x, rz < 0 relève une aile côté +x."""
import math
from modele2 import Modele, mul
from creatures2 import mats_creature, mini_cavalier, PEAU
from humanoide import f_yeux, f_dents, f_cadre, f_bande, f_comete, combine, f_etoile, f_rayures

R = math.radians


# ------------------------------------------------------------------ outils géométriques
def av(m, b, p, a, L, w, h, mat, ext=0.0, x=None, **f):
    """Segment vers l'avant (-z), relevé de a° ; renvoie l'extrémité."""
    px, py, pz = p
    if x is not None:
        px = x
    m.cube(b, (px - w / 2, py - h / 2, pz - L), (w, h, L + ext), mat, rot=(-a, 0, 0) if a else None, pivot=(px, py, pz), **f)
    return (px, py + L * math.sin(R(a)), pz - L * math.cos(R(a)))


def ar(m, b, p, a, L, w, h, mat, ext=0.0, **f):
    """Segment vers l'arrière (+z), relevé de a°."""
    px, py, pz = p
    m.cube(b, (px - w / 2, py - h / 2, pz - ext), (w, h, L + ext), mat, rot=(a, 0, 0) if a else None, pivot=(px, py, pz), **f)
    return (px, py + L * math.sin(R(a)), pz + L * math.cos(R(a)))


def bas(m, b, p, a, L, w, h, mat, ext=0.0, **f):
    """Segment vers le bas ; a > 0 envoie l'extrémité vers l'arrière."""
    px, py, pz = p
    m.cube(b, (px - w / 2, py - L, pz - h / 2), (w, L + ext, h), mat, rot=(a, 0, 0) if a else None, pivot=(px, py, pz), **f)
    return (px, py - L * math.cos(R(a)), pz + L * math.sin(R(a)))


def dir_av(a):
    return (0, math.sin(R(a)), -math.cos(R(a)))


def nor_av(a):
    """Normale « dessus » d'un segment vers l'avant relevé de a°."""
    return (0, math.cos(R(a)), math.sin(R(a)))


def nor_ar(a):
    return (0, math.cos(R(a)), -math.sin(R(a)))


def add(p, *vs):
    x, y, z = p
    for k, v in vs:
        x, y, z = x + k * v[0], y + k * v[1], z + k * v[2]
    return (x, y, z)


def jambe(m, b, hanche, segs, sol):
    """Patte en segments (a, fraction, w, h, mat) dont les longueurs sont ajustées pour toucher y = sol."""
    tot = sum(f * math.cos(R(a)) for a, f, *_ in segs)
    k = (hanche[1] - sol) / tot
    p = hanche
    for a, f, w, h, mat in segs:
        p = bas(m, b, p, a, f * k, w, h, mat, ext=min(w, h) * 0.45)
    return p


def pied(m, b, p, w, l, h, mat, griffes=3, mat_g="corne", arriere=False):
    x, _, z = p
    m.cube(b, (x - w / 2, 0, z - l * 0.6), (w, h, l), mat)
    if griffes:
        for k in range(griffes):
            xx = x - w / 2 + (k + 0.5) * w / griffes
            m.cube(b, (xx - 0.35, 0, z - l * 0.6 - 1.0), (0.7, min(h, 0.9), 1.2), mat_g)
    if arriere:
        m.cube(b, (x - 0.35, 0, z + l * 0.4 - 0.2), (0.7, 0.8, 1.2), mat_g)


def oeil(m, b, p, cote, r, mat="sombre", reflet=True):
    """Œil saillant sur une face latérale (cote = demi-largeur de la tête)."""
    x, y, z = p
    for sx in (-1, 1):
        xx = sx * cote - (0.3 if sx > 0 else 0.6)
        m.cube(b, (xx, y - r / 2, z - r / 2), (0.9, r, r), mat)
        if reflet and r >= 1:
            m.cube(b, (xx + (0.65 if sx > 0 else -0.05), y + r / 2 - 0.45, z - r / 2 + 0.1), (0.3, 0.35, 0.35), "blanc")


def miroir(m, b, o, t, mat, rot, piv, sx, **f):
    if sx > 0:
        m.cube(b, o, t, mat, rot=rot, pivot=piv, **f)
    else:
        m.cube(b, (-(o[0] + t[0]), o[1], o[2]), t, mat, rot=(rot[0], -rot[1], -rot[2]) if rot else None,
               pivot=(-piv[0], piv[1], piv[2]), **f)


class Cadre:
    """Repère plat d'une aile (côté +x), relevé d'un angle th autour de z."""

    def __init__(self, o, th):
        self.o, self.th = o, th

    def monde(self, p):
        c, s = math.cos(R(self.th)), math.sin(R(self.th))
        return (self.o[0] + p[0] * c - p[1] * s, self.o[1] + p[0] * s + p[1] * c, self.o[2] + p[2])

    def barre(self, m, b, x0, x1, h, d, mat, sx, z=0.0, **f):
        rw = self.monde((x0, 0, z))
        miroir(m, b, (rw[0], rw[1] - h / 2, rw[2] - d / 2), (x1 - x0, h, d), mat, (0, 0, -self.th), rw, sx, **f)

    def piece(self, m, b, racine, lacet, w, h, L, mat, sx, **f):
        """Pièce orientée vers l'arrière (+z), tournée de « lacet »° vers l'extérieur."""
        rw = self.monde(racine)
        miroir(m, b, (rw[0] - w / 2, rw[1] - h / 2, rw[2]), (w, h, L), mat, (0, lacet, -self.th), rw, sx, **f)


def mat(mats, nom, c, t):
    mats[nom] = {"c": tuple(int(v) for v in c), "type": t}


# ------------------------------------------------------------------ ailes
def ailes_plumes(m, mats, S, e, th1=18, th2=32, couv="plume_b", rem="plume_b", bord="plume_c"):
    """Aile d'oiseau levée : bras, couvertures, rémiges secondaires puis primaires en éventail."""
    Li, Lo = e * 0.48, e * 0.42
    for nomb, sx in (("wing_l", 1), ("wing_r", -1)):
        m.bone(nomb, "body", (sx * S[0], S[1], S[2]))
        A = Cadre(S, th1)
        A.barre(m, nomb, -0.5, Li + 0.5, 1.8, 2.6, couv, sx)                               # bras
        A.barre(m, nomb, 0, Li, 0.9, 4.0, couv, sx, z=2.6)                                  # couvertures
        for k in range(5):                                                                  # rémiges secondaires
            xk = 0.4 + k * (Li - 0.6) / 5
            A.piece(m, nomb, (xk + Li / 10, -0.1 - 0.05 * k, 3.0), 3 + k * 2, Li / 5 + 1.2, 0.45, e * 0.32 + k * 0.5, rem, sx)
        E = A.monde((Li, 0, 0))
        B = Cadre(E, th2)
        B.barre(m, nomb, -0.5, Lo * 0.55, 1.5, 2.2, couv, sx)                              # main
        B.barre(m, nomb, 0, Lo * 0.5, 0.8, 3.0, couv, sx, z=2.2)
        for k in range(8):                                                                  # rémiges primaires
            t = k / 7
            B.piece(m, nomb, (Lo * 0.05 + t * Lo * 0.5, 0.06 * k, 1.8), 14 + t * 58, 2.6, 0.4, e * (0.34 + 0.26 * t),
                    rem if k < 6 else bord, sx)


def ailes_membrane(m, mats, S, e, th1=14, th2=26, os_="corne", memb="membrane", dechire=False):
    """Aile de chauve-souris / dragon : humérus, avant-bras, quatre doigts et membrane en lanières."""
    Li, Lo = e * 0.42, e * 0.18
    for nomb, sx in (("wing_l", 1), ("wing_r", -1)):
        m.bone(nomb, "body", (sx * S[0], S[1], S[2]))
        A = Cadre(S, th1)
        A.barre(m, nomb, -0.5, Li + 0.5, 1.8, 1.8, os_, sx)
        # membrane intérieure, du flanc au poignet
        n = 5
        for k in range(n):
            xk = k * Li / n
            A.piece(m, nomb, (xk + Li / (2 * n), 0, 0.6), 0, Li / n + 0.3, 0.25, e * 0.42 - k * 0.6, memb, sx)
        E = A.monde((Li, 0, 0))
        B = Cadre(E, th2)
        B.barre(m, nomb, -0.4, Lo + 0.4, 1.4, 1.4, os_, sx)
        doigts = [(18, e * 0.48), (38, e * 0.56), (62, e * 0.62), (84, e * 0.6)]
        for lac, ld in doigts:
            B.piece(m, nomb, (Lo, 0.15, 0), lac, 0.7, 0.6, ld, os_, sx)
        B.piece(m, nomb, (Lo + 0.3, 0.4, -0.6), 100, 0.8, 0.8, 2.2, "corne", sx)                     # griffe du pouce
        # membrane entre les doigts : lanières en éventail, festonnées entre deux doigts
        lac = 4
        while lac < 84:
            # longueur interpolée entre les doigts encadrants
            prev = (0, e * 0.46)
            nxt = doigts[0]
            for d_ in doigts:
                if d_[0] <= lac:
                    prev = d_
                else:
                    nxt = d_
                    break
            else:
                nxt = doigts[-1]
            t = 0 if nxt[0] == prev[0] else (lac - prev[0]) / (nxt[0] - prev[0])
            ln = prev[1] + (nxt[1] - prev[1]) * t
            ln *= 1 - 0.22 * math.sin(math.pi * t)
            if dechire and int(lac) % 3 == 0:
                ln *= 0.7
            B.piece(m, nomb, (Lo - 0.5, 0, 0), lac, max(2.2, ln * 0.14), 0.25, ln, memb, sx)
            lac += 6


# ------------------------------------------------------------------ cheval et montures équines
def cheval(nom, s, fac):
    P = s["pal"]
    mats = mats_creature(nom, s, fac)
    A2, LU = P["armure2"], P["lueur"]
    m = Modele(nom)
    W, H, L = s.get("corps", (8, 9, 16))
    lw, lh = s.get("jambe", (3, 12))
    tw, th, td = s.get("tete", (4, 5, 8))
    cou = s.get("cou", 6)
    fin = nom == "seeker"
    yb = lh
    m.bone("root", None, (0, 0, 0))
    m.bone("body", "root", (0, yb + H / 2, 0))
    # tronc : poitrail, ventre en tonneau, croupe arrondie
    m.cube("body", (-W / 2, yb + 0.6, -L / 2), (W, H - 0.2, L * 0.4), "corps")
    m.cube("body", (-W / 2 + 0.3, yb, -L / 2 + L * 0.32), (W - 0.6, H - 0.6, L * 0.4), "corps")
    m.cube("body", (-W / 2, yb + 0.8, L / 2 - L * 0.34), (W, H - 0.6, L * 0.34), "corps")
    m.cube("body", (-W / 2 + 0.9, yb + H - 0.2, L / 2 - L * 0.31), (W - 1.8, 0.8, L * 0.26), "corps")       # croupe
    m.cube("body", (-W / 2 + 1, yb + H + 0.2, -L / 2 + 0.8), (W - 2, 0.7, L * 0.22), "corps")              # garrot
    m.cube("body", (-W / 2 + 0.9, yb + 1.8, -L / 2 - 0.8), (W - 1.8, H - 3.2, 0.9), "corps")               # poitrail
    m.cube("body", (-W / 2 + 1.2, yb - 0.5, -L / 2 + L * 0.3), (W - 2.4, 0.6, L * 0.42), "ventre")
    # pattes : antérieures droites, postérieures en Z (grasset en avant, jarret en arrière)
    sab = 1.4
    fl = lw * (0.85 if fin else 1.0)
    for nomj, sx, av_ in (("leg_fl", -1, 1), ("leg_fr", 1, 1), ("leg_bl", -1, 0), ("leg_br", 1, 0)):
        x = sx * (W / 2 - fl / 2 - 0.2)
        z = -L / 2 + fl / 2 + 1 if av_ else L / 2 - fl / 2 - 1.4
        h0 = (x, yb + 2.2, z)
        m.bone(nomj, "root", h0)
        if av_:
            segs = [(-4, 0.5, fl + 0.9, fl + 1.1, "corps"), (3, 0.5, fl * 0.72, fl * 0.72, "corps")]
        else:
            segs = [(-14, 0.3, fl + 1.4, fl + 2.4, "corps"), (24, 0.36, fl * 0.95, fl * 1.1, "corps"),
                    (-4, 0.34, fl * 0.72, fl * 0.72, "corps")]
        p = jambe(m, nomj, h0, segs, sab)
        if not fin and fac not in ("ossiarch", "nighthaunt"):
            m.cube(nomj, (x - fl * 0.5, sab, p[2] - fl * 0.45), (fl, 1.4, fl * 0.95), "poils")          # fanons
        m.cube(nomj, (x - fl * 0.48, 0, p[2] - fl * 0.6), (fl * 0.96, sab, fl * 1.05), "sombre")        # sabot
        if s.get("caparacon"):
            m.cube(nomj, (x - fl * 0.5 - 0.1, lh * 0.55, h0[2] - fl * 0.6), (fl + 0.2, 1.2, fl * 1.2), "armure2")
    # encolure arquée et crinière
    m.bone("neck", "body", (0, yb + H - 1.6, -L / 2 + 1.6))
    p0 = (0, yb + H - 1.6, -L / 2 + 1.6)
    a1, a2 = (48, 64) if not fin else (58, 74)
    l1, l2 = cou * 0.75 + 1, cou * 0.6
    w1, w2 = W * (0.62 if not fin else 0.5), W * (0.48 if not fin else 0.4)
    p1 = av(m, "neck", p0, a1, l1, w1, H * 0.62, "corps", ext=1.5)
    p2 = av(m, "neck", p1, a2, l2, w2, H * 0.5, "corps", ext=1.0)
    crin = "poils"
    for (pa, a, ln, hh) in ((p0, a1, l1, H * 0.62), (p1, a2, l2 + 0.6, H * 0.5)):
        pm = add(pa, (hh / 2 + 0.3, nor_av(a)))
        av(m, "neck", pm, a, ln, 1.3, 1.6, crin, ext=0.4)
    if s.get("crete_dos"):
        for (pa, a, ln, hh) in ((p0, a1, l1, H * 0.62), (p1, a2, l2, H * 0.5)):
            for t in (0.25, 0.65):
                pc = add(pa, (ln * t, dir_av(a)), (hh / 2 + 1.2, nor_av(a)))
                m.cube("neck", (-0.5, pc[1] - 1, pc[2] - 0.5), (1, 2.4, 1), "corne", rot=(-25, 0, 0), pivot=pc)
    # tête longue, inclinée vers le bas
    m.bone("head", "neck", p2)
    ah = -42 if not fin else -30
    ph = add(p2, (1.0, nor_av(ah)), (-0.8, dir_av(ah)))
    pe = av(m, "head", ph, ah, td * 0.62, tw, th, "corps", ext=0.8)
    pm = av(m, "head", add(pe, (-0.5, dir_av(ah)), (-th * 0.1, nor_av(ah))), ah - 6, td * 0.48, tw * 0.82, th * 0.72, "corps", ext=0.4)
    m.cube("head", (-tw * 0.3, pm[1] - 0.6, pm[2] - 0.5), (tw * 0.6, 0.6, 0.6), "sombre", rot=(-(ah - 6), 0, 0), pivot=pm)  # naseaux
    m.bone("jaw", "head", add(pe, (-th * 0.42, nor_av(ah))))
    av(m, "jaw", add(pe, (-th * 0.4, nor_av(ah)), (-0.3, dir_av(ah))), ah - 10, td * 0.42, tw * 0.6, th * 0.28, "corps")
    yeux = "lueur" if fac in ("soulblight", "nighthaunt", "ossiarch", "esclaves", "slaanesh") else "sombre"
    oeil(m, "head", add(ph, (td * 0.2, dir_av(ah)), (th * 0.18, nor_av(ah))), tw / 2, 1.0, yeux, reflet=(yeux == "sombre"))
    for sx in (-1, 1):                                                                       # oreilles
        po = add(ph, (th / 2, nor_av(ah)), (0.4, dir_av(ah)))
        m.cube("head", (sx * tw * 0.3 - 0.5, po[1] - 0.3, po[2] - 0.4), (1, 2.4, 0.9), "corps", rot=(12, 0, sx * -10), pivot=po)
    av(m, "head", add(ph, (th / 2 + 0.2, nor_av(ah))), ah, td * 0.35, 1.4, 1.2, crin)          # toupet
    if s.get("caparacon") or fac in ("ossiarch",):                                          # chanfrein
        av(m, "head", add(ph, (th / 2 + 0.15, nor_av(ah)), (0.5, dir_av(ah))), ah - 3, td * 0.85, tw + 0.5, 0.6, "armure",
           up=f_bande(A2, "haut"))
    if s.get("cornes"):
        for sx in (-1, 1):
            pc = add(ph, (th / 2, nor_av(ah)), (td * 0.15, dir_av(ah)))
            pc = (sx * tw * 0.3, pc[1], pc[2])
            q = av(m, "head", pc, 40, 2.6, 1.3, 1.3, "corne")
            av(m, "head", q, 70, 1.8, 0.9, 0.9, "corne")
    if fin:                                                                                  # longue langue des Seekers
        av(m, "jaw", add(pm, (-0.6, nor_av(ah))), ah - 35, 4.5, 1.0, 0.4, "rose")
    # queue : tronçon puis crins tombants
    m.bone("tail", "body", (0, yb + H - 1.2, L / 2))
    q = ar(m, "tail", (0, yb + H - 1.2, L / 2 - 0.4), -30, 2.5, 1.8, 1.8, "corps")
    q = ar(m, "tail", q, -62, lh * 0.45, 2.6, 1.8, crin, ext=0.6)
    ar(m, "tail", q, -80, lh * 0.3, 2.1, 1.4, crin, ext=0.4)
    # caparaçon, selle, cavalier
    if s.get("caparacon"):
        for sx in (-1, 1):
            m.cube("body", (sx * (W / 2 + 0.2) - (0.5 if sx < 0 else 0), yb - 3.5, -L / 2 - 0.2), (0.5, H + 2.2, L * 0.92), "tissu",
                   east=combine(f_bande(A2, "bas", 2), f_comete(A2)), west=combine(f_bande(A2, "bas", 2), f_comete(A2)))
        m.cube("body", (-W / 2 - 0.2, yb + H + 0.6, -L / 2 + L * 0.15), (W + 0.4, 0.5, L * 0.8), "tissu")
        m.cube("body", (-W / 2 + 0.4, yb - 1.5, -L / 2 - 1.3), (W - 0.8, H - 0.5, 0.5), "armure",
               north=combine(f_cadre(A2), f_comete(A2)))                                      # bardes de poitrail
    zs = -L / 2 + L * 0.36
    if s.get("cavalier") or s.get("selle"):
        m.cube("body", (-W / 2 + 0.4, yb + H + 0.6, zs - 3), (W - 0.8, 1, 6), "cuir", toutes=f_bande(A2, "haut"))
        m.cube("body", (-W / 2 + 0.6, yb + H + 1.6, zs + 2), (W - 1.2, 1.4, 1), "cuir")
        for sx in (-1, 1):
            m.cube("body", (sx * W / 2 - (0.4 if sx < 0 else 0), yb + 1, zs), (0.4, H - 0.5, 0.8), "cuir")
            m.cube("body", (sx * W / 2 - (0.9 if sx < 0 else 0.1), yb + 0.2, zs - 0.6), (1, 1, 2), "metal")
        m.selle = (yb + H + 1.6, zs)
    if s.get("cavalier"):
        mini_cavalier(m, P, mats, fac, yb + H + 1.6, zs, s.get("arme_cavalier", "lance"), s.get("taille_cavalier", 1))
    return m, mats


# ------------------------------------------------------------------ griffons (aigle devant, lion derrière)
def griffon(nom, s, fac):
    P = s["pal"]
    mats = mats_creature(nom, s, fac)
    A2 = P["armure2"]
    m = Modele(nom)
    W, H, L = s.get("corps", (12, 10, 22))
    lw, lh = s.get("jambe", (4, 12))
    tw, th, td = s.get("tete", (7, 7, 7))
    cou = s.get("cou", 6)
    fauve = P["peau"]
    mat(mats, "plume_c", P.get("plume", (238, 232, 216)), "plume")
    mat(mats, "plume_b", P.get("plume2", mul(fauve, 0.78)), "plume")
    mat(mats, "fauve", fauve, "fourrure")
    mat(mats, "fauve_v", mul(fauve, 1.15), "fourrure")
    yb = lh
    m.bone("root", None, (0, 0, 0))
    m.bone("body", "root", (0, yb + H / 2, 0))
    # poitrail d'aigle (plus haut) et arrière-train de lion
    m.cube("body", (-W / 2, yb + 0.4, -L / 2), (W, H + 0.8, L * 0.44), "plume_b")
    m.cube("body", (-W / 2 + 1, yb + 1.2, -L / 2 - 1), (W - 2, H - 1.6, 1.2), "plume_c")
    m.cube("body", (-W / 2 + 0.6, yb + 0.4, -L / 2 + L * 0.38), (W - 1.2, H - 1.4, L * 0.62), "fauve")
    m.cube("body", (-W / 2 + 1.4, yb + H - 1.2, L / 2 - L * 0.36), (W - 2.8, 0.9, L * 0.3), "fauve")
    m.cube("body", (-W / 2 + 1.6, yb - 0.3, -L / 2 + L * 0.42), (W - 3.2, 0.8, L * 0.45), "fauve_v")
    m.cube("body", (-W / 2 - 0.2, yb + H * 0.35, -L / 2 + L * 0.36), (W + 0.4, H * 0.75, 2.2), "plume_b")   # pèlerine de plumes
    # pattes avant d'aigle : culotte de plumes, tarse écailleux, serres
    for nomj, sx in (("leg_fl", -1), ("leg_fr", 1)):
        x = sx * (W / 2 - lw / 2 - 0.3)
        h0 = (x, yb + 2.5, -L / 2 + lw / 2 + 1.2)
        m.bone(nomj, "root", h0)
        p = jambe(m, nomj, h0, [(-12, 0.5, lw + 1.4, lw + 1.8, "plume_b"), (10, 0.5, lw * 0.55, lw * 0.6, "corne")], 0.9)
        x, _, z = p
        for dx in (-1.1, 0, 1.1):
            m.cube(nomj, (x + dx - 0.45, 0, z - 2.6), (0.9, 0.9, 2.6), "corne")
            m.cube(nomj, (x + dx - 0.3, 0, z - 3.3), (0.6, 0.7, 0.9), "sombre")
        m.cube(nomj, (x - 0.45, 0, z), (0.9, 0.9, 1.8), "corne")
        m.cube(nomj, (x - lw * 0.35, 0, z - 0.8), (lw * 0.7, 1.1, 1.8), "corne")
    # pattes arrière de lion
    for nomj, sx in (("leg_bl", -1), ("leg_br", 1)):
        x = sx * (W / 2 - lw / 2 - 0.4)
        h0 = (x, yb + 3, L / 2 - lw / 2 - 2)
        m.bone(nomj, "root", h0)
        p = jambe(m, nomj, h0, [(-14, 0.38, lw + 1.8, lw + 2.8, "fauve"), (30, 0.36, lw * 0.85, lw, "fauve"),
                                (-6, 0.26, lw * 0.75, lw * 0.75, "fauve")], 1.2)
        x, _, z = p
        m.cube(nomj, (x - lw * 0.5, 0, z - lw * 0.75), (lw, 1.3, lw * 1.35), "fauve")
        for k in range(3):
            m.cube(nomj, (x - lw * 0.42 + k * lw * 0.33, 0, z - lw * 0.75 - 0.5), (0.6, 0.6, 0.6), "sombre")
    # cou à collerette et tête d'aigle
    p0 = (0, yb + H - 0.5, -L / 2 + 1.5)
    m.bone("neck", "body", p0)
    m.cube("neck", (-W * 0.42, yb + H * 0.45, -L / 2 - 1.6), (W * 0.84, H * 0.75, 3), "plume_c")               # collerette
    p1 = av(m, "neck", p0, 42, cou + 1, tw + 0.8, th + 0.4, "plume_c", ext=1.5)
    m.bone("head", "neck", p1)
    pe = av(m, "head", add(p1, (-0.6, dir_av(8))), 8, td, tw, th, "plume_c", ext=0.6)
    oeil(m, "head", add(p1, (td * 0.55, dir_av(8)), (th * 0.12, nor_av(8))), tw / 2, 1.2, "or", reflet=False)
    for sx in (-1, 1):
        pb = add(p1, (td * 0.4, dir_av(8)), (th * 0.38, nor_av(8)))
        m.cube("head", (sx * tw * 0.28 - 1.1, pb[1] - 0.4, pb[2] - 1.8), (2.2, 0.9, 3.2), "plume_c")           # arcades
    pb = add(pe, (th * 0.12, nor_av(8)))
    q = av(m, "head", pb, -8, 3.2, tw * 0.55, th * 0.48, "corne", ext=0.8)                                    # bec
    av(m, "head", add(q, (-0.3, nor_av(-8))), -62, 2.6, tw * 0.34, 1.5, "corne", ext=0.5)                      # crochet
    m.bone("jaw", "head", add(pe, (-th * 0.32, nor_av(8))))
    av(m, "jaw", add(pe, (-th * 0.3, nor_av(8)), (0.4, dir_av(8))), -14, 2.8, tw * 0.44, 1.0, "corne")
    for k, a in enumerate((26, 14)):                                                                          # aigrette
        pc = add(p1, (th / 2 - 0.4 - k * 1.2, nor_av(8)), (0.6, dir_av(8)))
        ar(m, "head", pc, a, 3.4 - k * 0.6, tw * 0.6 - k, 1.1, "plume_c", ext=0.5)
    # queue de lion à houppe
    m.bone("tail", "body", (0, yb + H - 2, L / 2))
    q = ar(m, "tail", (0, yb + H - 2, L / 2 - 0.5), -34, s.get("queue", 10) * 0.55, 1.4, 1.4, "fauve")
    q = ar(m, "tail", q, 6, s.get("queue", 10) * 0.45, 1.2, 1.2, "fauve")
    ar(m, "tail", add(q, (0.6, (0, -1, 0))), 24, 3.2, 2.4, 2.2, "poils", ext=0.8)
    # ailes levées
    if s.get("ailes"):
        ailes_plumes(m, mats, (W / 2 - 1.2, yb + H, -L / 2 + L * 0.28), s["ailes"] * 1.15)
    if s.get("cavalier") or s.get("selle"):
        zs = -L / 2 + L * 0.45
        m.cube("body", (-W / 2 + 0.6, yb + H, zs - 3), (W - 1.2, 1, 6), "cuir", toutes=f_bande(A2, "haut"))
        m.selle = (yb + H + 1, zs)
    if s.get("cavalier"):
        mini_cavalier(m, P, mats, fac, yb + H + 1, zs, s.get("arme_cavalier", "lance"), s.get("taille_cavalier", 1))
    return m, mats


# ------------------------------------------------------------------ dragons, drakes et grands reptiles
def dragon(nom, s, fac):
    P = s["pal"]
    mats = mats_creature(nom, s, fac)
    A2, LU = P["armure2"], P["lueur"]
    m = Modele(nom)
    W, H, L = s.get("corps", (18, 14, 34))
    lw, lh = s.get("jambe", (6, 13))
    tw, th, td = s.get("tete", (10, 9, 12))
    cou, qn = s.get("cou", 8), s.get("queue", 14)
    rampant = nom == "salamandre"
    chauve = nom in ("terrorgheist",)
    yb = lh * (0.82 if not rampant else 0.6)
    m.bone("root", None, (0, 0, 0))
    m.bone("body", "root", (0, yb + H / 2, 0))
    # tronc : poitrail massif, taille, hanches
    m.cube("body", (-W / 2, yb + 0.5, -L / 2), (W, H, L * 0.42), "corps")
    m.cube("body", (-W / 2 + 0.6, yb + 0.2, -L / 2 + L * 0.36), (W - 1.2, H - 1, L * 0.34), "corps")
    m.cube("body", (-W / 2 + 1.4, yb + 0.8, L / 2 - L * 0.32), (W - 2.8, H - 2.2, L * 0.32), "corps")
    m.cube("body", (-W / 2 + 1.5, yb + H, -L / 2 + 1.5), (W - 3, 0.9, L * 0.55), "corps")
    m.cube("body", (-W / 2 + 2, yb - 0.4, -L / 2 + 1), (W - 4, 0.8, L * 0.85), "ventre",
           down=lambda d, x, y, w, h, px: [d.line((x, y + k, x + w - 1, y + k), fill=mul(mats["ventre"]["c"], 0.72)) for k in range(1, h, 3)])
    if s.get("crete_dos"):
        for k in range(int(L // 3)):
            z = -L / 2 + 1.5 + k * 3
            hh = (2.6 * (1 - abs(k / max(1, L // 3) - 0.35)) + 0.6) * min(1.0, L / 26)
            m.cube("body", (-0.5, yb + H + 0.4, z), (1, hh, 1.6), "corne", rot=(18, 0, 0), pivot=(0, yb + H + 0.4, z + 0.8))
    if fac == "stormcast":                                                                     # bardes de sigmarite
        m.cube("body", (-W / 2 - 0.3, yb + H * 0.45, -L / 2 - 0.4), (W + 0.6, H * 0.6, L * 0.3), "armure",
               north=combine(f_cadre(A2), f_comete(A2)), toutes=f_bande(A2, "bas", 2))
    # pattes
    sol = 1.2
    for nomj, sx, av_ in (("leg_fl", -1, 1), ("leg_fr", 1, 1), ("leg_bl", -1, 0), ("leg_br", 1, 0)):
        x = sx * (W / 2 - lw * 0.35 + (lw * 0.4 if rampant else 0))
        z = -L / 2 + L * 0.18 if av_ else L / 2 - L * 0.2
        h0 = (x, yb + H * 0.35, z)
        m.bone(nomj, "root", h0)
        if av_:
            segs = [(24, 0.5, lw + 0.6, lw + 0.8, "corps"), (-20, 0.5, lw * 0.75, lw * 0.8, "corps")]
        else:
            segs = [(-28, 0.42, lw + 2, lw + 2.6, "corps"), (34, 0.36, lw * 0.85, lw * 0.95, "corps"),
                    (-10, 0.22, lw * 0.7, lw * 0.7, "corps")]
        p = jambe(m, nomj, h0, segs, sol)
        pied(m, nomj, p, lw * 1.05, lw * 1.5, sol + 0.2, "corps", griffes=3, arriere=not av_)
        if fac == "stormcast" and av_:
            m.cube(nomj, (x - lw * 0.5 - 0.1, h0[1] - lh * 0.4, z - lw * 0.55), (lw + 0.2, 1.5, lw * 1.1), "armure2")
    # cou sinueux
    p0 = (0, yb + H - 2, -L / 2 + 2)
    m.bone("neck", "body", p0)
    angs = [34, 48, 30, 8] if cou >= 6 else [28, 12]
    p = p0
    n = len(angs)
    for k, a in enumerate(angs):
        w_ = W * 0.55 - k * (W * 0.55 - tw * 0.78) / max(1, n - 1)
        h_ = H * 0.6 - k * (H * 0.6 - th * 0.72) / max(1, n - 1)
        ln = cou * 1.25 / n + 1.2
        q = av(m, "neck", p, a, ln, w_, h_, "corps", ext=1.4)
        if s.get("crete_dos"):
            pc = add(p, (ln * 0.5, dir_av(a)), (h_ / 2, nor_av(a)))
            m.cube("neck", (-0.5, pc[1] - 0.3, pc[2] - 0.6), (1, 2.0, 1.2), "corne", rot=(25 - a, 0, 0), pivot=pc)
        p = q
    # tête : crâne, museau, arcades, cornes, mâchoire
    m.bone("head", "neck", p)
    ah = -10 if not chauve else -4
    ps = add(p, (-1, dir_av(ah)))
    pe = av(m, "head", ps, ah, td * 0.5, tw, th, "corps", ext=1)
    pm = av(m, "head", add(pe, (0.3, nor_av(ah))), ah - 4, td * (0.55 if not chauve else 0.3), tw * 0.68, th * 0.55, "corps", ext=1.2)
    for sx in (-1, 1):                                                                         # naseaux
        m.cube("head", (sx * tw * 0.2 - 0.4, pm[1] + 0.2, pm[2] - 0.2), (0.8, 0.8, 0.6), "lueur" if fac in ("cites", "fyreslayers", "esclaves", "orruks") else "sombre")
    oeil(m, "head", add(ps, (td * 0.32, dir_av(ah)), (th * 0.18, nor_av(ah))), tw / 2, 1.2, "lueur", reflet=False)
    for sx in (-1, 1):                                                                         # arcades
        pa = add(ps, (td * 0.3, dir_av(ah)), (th * 0.42, nor_av(ah)))
        m.cube("head", (sx * tw * 0.33 - 1.2, pa[1] - 0.4, pa[2] - 1.6), (2.4, 1.1, 3.4), "corps", rot=(-ah, 0, 0), pivot=pa)
    m.bone("jaw", "head", add(ps, (-th * 0.42, nor_av(ah))))
    pj = add(ps, (-th * 0.38, nor_av(ah)), (0.5, dir_av(ah)))
    av(m, "jaw", pj, ah - 10, td * (1.0 if not chauve else 0.75), tw * 0.62, th * 0.3, "corps", up=f_dents((236, 230, 206)))
    pd_ = add(pe, (-th * 0.18, nor_av(ah)))
    m.cube("head", (-tw * 0.3, pd_[1] - th * 0.36, pd_[2] - td * 0.5), (tw * 0.6, 0.9, td * 0.5), "dent",
           north=f_dents((250, 248, 236), ), east=f_dents((250, 248, 236)), west=f_dents((250, 248, 236)))       # crocs
    if chauve:
        for sx in (-1, 1):                                                                     # grandes oreilles
            po = add(ps, (th / 2, nor_av(ah)), (td * 0.15, dir_av(ah)))
            m.cube("head", (sx * tw * 0.35 - 1.5, po[1] - 0.5, po[2] - 0.3), (3, 5, 0.6), "membrane", rot=(15, 0, sx * -20), pivot=po)
    elif s.get("cornes") or s.get("grandes_cornes"):
        for sx in (-1, 1):
            pc = add(ps, (th * 0.35, nor_av(ah)), (td * 0.05, dir_av(ah)))
            pc = (sx * tw * 0.3, pc[1], pc[2])
            q = ar(m, "head", pc, 24, td * 0.45, 2.0, 2.0, "corne", ext=0.5)
            q = ar(m, "head", q, 8, td * 0.35, 1.4, 1.4, "corne", ext=0.4)
            ar(m, "head", q, -12, td * 0.2, 0.9, 0.9, "corne")
            pk = add(ps, (-th * 0.1, nor_av(ah)), (td * 0.2, dir_av(ah)))                      # piquants des joues
            m.cube("head", (sx * (tw / 2 + 0.3) - 0.5, pk[1] - 0.5, pk[2]), (1, 1, 2.4), "corne", rot=(0, sx * 30, 0), pivot=(sx * tw / 2, pk[1], pk[2]))
    if fac == "stormcast":
        av(m, "head", add(ps, (th / 2 + 0.2, nor_av(ah))), ah, td * 0.9, tw * 0.7, 0.7, "armure", up=f_bande(A2, "haut"))
    # queue effilée
    m.bone("tail", "body", (0, yb + H - 3, L / 2))
    q = (0, yb + H - 3, L / 2 - 1)
    angs = [-12, -6, 0, 4, 2, -2]
    for k, a in enumerate(angs):
        w_ = max(1.0, W * 0.42 * (1 - k / len(angs)))
        q2 = ar(m, "tail", q, a, qn * 1.25 / len(angs) + 0.8, w_, w_ * 0.9, "corps", ext=1)
        if s.get("crete_dos") and w_ > 1.6:
            m.cube("tail", (-0.5, q[1] + w_ * 0.45, q[2] + 0.5), (1, 1.4, 1.2), "corne", rot=(20, 0, 0), pivot=(0, q[1] + w_ * 0.45, q[2] + 1))
        q = q2
    if not rampant:
        m.cube("tail", (-2, q[1] - 0.4, q[2] - 0.5), (4, 0.8, 3.5), "corne" if not chauve else "membrane")      # pointe en fer de lance
    # ailes
    if s.get("ailes"):
        ailes_membrane(m, mats, (W / 2 - 1.5, yb + H, -L / 2 + L * 0.3), s["ailes"] * 1.25,
                       dechire=nom in ("dragon_zombie", "terrorgheist"))
    if s.get("cavalier") or s.get("selle"):
        zs = -L / 2 + L * 0.38
        m.cube("body", (-W / 2 + 1.5, yb + H + 0.6, zs - 3), (W - 3, 1, 6.5), "cuir", toutes=f_bande(A2, "haut"))
        m.selle = (yb + H + 1.6, zs)
    if s.get("cavalier"):
        mini_cavalier(m, P, mats, fac, yb + H + 1.6, zs, s.get("arme_cavalier", "lance"), s.get("taille_cavalier", 1))
    return m, mats


# ------------------------------------------------------------------ carnosaure (bipède)
def theropode(nom, s, fac):
    P = s["pal"]
    mats = mats_creature(nom, s, fac)
    A2 = P["armure2"]
    m = Modele(nom)
    W, H, L = s.get("corps", (14, 14, 22))
    lw, lh = s.get("jambe", (6, 16))
    tw, th, td = s.get("tete", (10, 9, 12))
    yb = lh * 0.95
    m.bone("root", None, (0, 0, 0))
    m.bone("body", "root", (0, yb + H / 2, 0))
    m.cube("body", (-W / 2, yb, -L / 2), (W, H, L * 0.5), "corps", rot=(-8, 0, 0), pivot=(0, yb + H / 2, -L / 2 + L * 0.5))
    m.cube("body", (-W / 2 + 0.8, yb + 0.6, -L / 2 + L * 0.45), (W - 1.6, H - 1.6, L * 0.55), "corps")
    for k in range(int(L // 2.6)):                                                            # crête dorsale
        z = -L / 2 + 1 + k * 2.6
        m.cube("body", (-0.4, yb + H - 0.2 + (0.8 if z < 0 else 0), z), (0.8, 1.6, 1.4), "crete")
    for nomj, sx in (("right_leg", -1), ("left_leg", 1)):
        x = sx * (W / 2 - lw * 0.3)
        h0 = (x, yb + H * 0.4, L * 0.1)
        m.bone(nomj, "root", h0)
        p = jambe(m, nomj, h0, [(-30, 0.42, lw + 2.6, lw + 4, "corps"), (38, 0.36, lw * 0.85, lw, "corps"),
                                (-12, 0.22, lw * 0.6, lw * 0.6, "corps")], 1.2)
        pied(m, nomj, p, lw * 1.1, lw * 1.8, 1.4, "corps", griffes=3, arriere=True)
    for sx in (-1, 1):                                                                         # petits bras griffus
        pa = (sx * (W / 2 - 0.5), yb + H * 0.35, -L / 2 + 2.5)
        q = bas(m, "body", pa, -30, 3.5, 1.6, 1.6, "corps")
        q = bas(m, "body", q, -70, 2.8, 1.2, 1.2, "corps")
        m.cube("body", (q[0] - 0.6, q[1] - 1.4, q[2] - 0.6), (1.2, 1.6, 0.6), "corne")
    # cou court et énorme tête
    p0 = (0, yb + H * 0.8, -L / 2 + 1)
    m.bone("neck", "body", p0)
    p1 = av(m, "neck", p0, 30, s.get("cou", 4) + 2, W * 0.62, H * 0.6, "corps", ext=1.5)
    m.bone("head", "neck", p1)
    ps = add(p1, (-1, dir_av(-6)))
    pe = av(m, "head", ps, -6, td * 0.55, tw, th, "corps", ext=1)
    pm = av(m, "head", add(pe, (0.4, nor_av(-6))), -9, td * 0.55, tw * 0.75, th * 0.6, "corps", ext=1)
    oeil(m, "head", add(ps, (td * 0.3, dir_av(-6)), (th * 0.22, nor_av(-6))), tw / 2, 1.2, "oeil", reflet=False)
    for sx in (-1, 1):
        pa = add(ps, (td * 0.28, dir_av(-6)), (th * 0.45, nor_av(-6)))
        m.cube("head", (sx * tw * 0.3 - 1.2, pa[1] - 0.4, pa[2] - 1.6), (2.4, 1.4, 3.6), "crete")         # cornes d'arcade rouges
    for k in range(4):
        pc = add(ps, (th / 2, nor_av(-6)), (k * td * 0.22, dir_av(-6)))
        m.cube("head", (-0.4, pc[1] - 0.4, pc[2] - 0.7), (0.8, 1.8 - k * 0.2, 1.4), "crete")
    m.cube("head", (-tw * 0.32, pe[1] - th * 0.5, pe[2] - td * 0.5), (tw * 0.64, 1.0, td * 0.55), "dent",
           north=f_dents((250, 248, 236)), east=f_dents((250, 248, 236)), west=f_dents((250, 248, 236)))
    m.bone("jaw", "head", add(ps, (-th * 0.45, nor_av(-6))))
    av(m, "jaw", add(ps, (-th * 0.42, nor_av(-6)), (0.5, dir_av(-6))), -18, td * 1.0, tw * 0.7, th * 0.32, "corps", up=f_dents((236, 230, 206)))
    # queue de balancier
    m.bone("tail", "body", (0, yb + H - 2, L / 2))
    q = (0, yb + H - 2.5, L / 2 - 1)
    qn = s.get("queue", 18)
    for k, a in enumerate((-8, -4, 2, 6, 4)):
        w_ = max(1.0, W * 0.5 * (1 - k / 5))
        q = ar(m, "tail", q, a, qn * 1.3 / 5 + 0.8, w_, w_ * 0.9, "corps", ext=1)
    if s.get("cavalier") or s.get("selle"):
        zs = -L / 2 + L * 0.42
        m.cube("body", (-W / 2 + 1, yb + H, zs - 3.5), (W - 2, 1.2, 7), "or", toutes=f_bande(A2, "haut"))
        m.selle = (yb + H + 1.2, zs)
    if s.get("cavalier"):
        mini_cavalier(m, P, mats, fac, yb + H + 1.2, zs, s.get("arme_cavalier", "lance"), s.get("taille_cavalier", 1))
    return m, mats


# ------------------------------------------------------------------ fauves, molosses et bêtes de meute
def fauve(nom, s, fac):
    P = s["pal"]
    mats = mats_creature(nom, s, fac)
    A2, LU = P["armure2"], P["lueur"]
    m = Modele(nom)
    W, H, L = s.get("corps", (7, 7, 14))
    lw, lh = s.get("jambe", (2, 8))
    tw, th, td = s.get("tete", (5, 5, 6))
    chat = nom in ("sabre_givre",)
    voute = nom in ("varghulf", "morbheg")
    yb = lh
    m.bone("root", None, (0, 0, 0))
    m.bone("body", "root", (0, yb + H / 2, 0))
    # poitrail profond, taille fine, hanches
    m.cube("body", (-W / 2, yb - 0.5, -L / 2), (W, H + (1.5 if voute else 0.5), L * 0.45), "corps")
    m.cube("body", (-W / 2 + 0.7, yb + 1.2, -L / 2 + L * 0.4), (W - 1.4, H - 1.8, L * 0.32), "corps")
    m.cube("body", (-W / 2 + 0.4, yb + 0.6, L / 2 - L * 0.3), (W - 0.8, H - 0.9, L * 0.3), "corps")
    m.cube("body", (-W / 2 + 1, yb - 0.8, -L / 2 + 0.8), (W - 2, 0.5, L * 0.38), "ventre")
    if s.get("criniere") or voute:
        m.cube("body", (-W / 2 - 0.3, yb + H * 0.35, -L / 2 - 0.3), (W + 0.6, H * 0.7 + (1.2 if voute else 0), L * 0.3), "corps")
        for k in range(4):
            z = -L / 2 + k * L * 0.1
            m.cube("body", (-W / 2 + 0.5, yb + H + (1.2 if voute else 0.4), z), (W - 1, 1.2, 1.6), "corps", rot=(25, 0, 0),
                   pivot=(0, yb + H + 0.6, z + 0.8))
    if s.get("crete_dos"):
        for k in range(int(L // 2.4)):
            z = -L / 2 + 1 + k * 2.4
            m.cube("body", (-0.5, yb + H - 0.3, z), (1, 2.0, 1), "corne", rot=(25, 0, 0), pivot=(0, yb + H - 0.3, z + 0.5))
    for nomj, sx, av_ in (("leg_fl", -1, 1), ("leg_fr", 1, 1), ("leg_bl", -1, 0), ("leg_br", 1, 0)):
        x = sx * (W / 2 - lw / 2 - 0.2)
        z = -L / 2 + lw / 2 + 1.2 if av_ else L / 2 - lw / 2 - 1.2
        h0 = (x, yb + 1.8, z)
        m.bone(nomj, "root", h0)
        if av_:
            segs = [(-6, 0.52, lw + 1.0 + (1 if voute else 0), lw + 1.4, "corps"), (4, 0.36, lw * 0.8, lw * 0.85, "corps"),
                    (-25, 0.12, lw * 0.8, lw * 0.85, "corps")]
        else:
            segs = [(-18, 0.36, lw + 1.6, lw + 2.4, "corps"), (34, 0.38, lw * 0.85, lw, "corps"), (-14, 0.26, lw * 0.7, lw * 0.7, "corps")]
        p = jambe(m, nomj, h0, segs, 0.9)
        pied(m, nomj, p, lw * 1.15, lw * 1.5, 1.0, "corps", griffes=3 if not chat else 3, mat_g="corne")
    # cou et tête (museau long de molosse ou court de félin)
    p0 = (0, yb + H - 1.2, -L / 2 + 1)
    m.bone("neck", "body", p0)
    p1 = av(m, "neck", p0, 22 if not voute else -5, s.get("cou", 2) + 2.5, W * 0.6, H * 0.6, "corps", ext=1.2)
    m.bone("head", "neck", p1)
    ah = -6
    ps = add(p1, (-0.8, dir_av(ah)))
    pe = av(m, "head", ps, ah, td * 0.55, tw, th, "corps", ext=0.6)
    lm = td * (0.32 if chat else 0.55)
    pm = av(m, "head", add(pe, (-th * 0.1, nor_av(ah))), ah - 6, lm, tw * 0.62, th * 0.5, "corps", ext=0.5)
    m.cube("head", (-tw * 0.16, pm[1] + th * 0.08, pm[2] - 0.35), (tw * 0.32, 0.8, 0.6), "sombre")                # truffe
    yeux = "lueur" if fac in ("khorne", "slaanesh", "soulblight", "fec", "nurgle") else "sombre"
    oeil(m, "head", add(ps, (td * 0.35, dir_av(ah)), (th * 0.2, nor_av(ah))), tw / 2, 0.9, yeux, reflet=(yeux == "sombre"))
    m.bone("jaw", "head", add(ps, (-th * 0.4, nor_av(ah))))
    av(m, "jaw", add(ps, (-th * 0.38, nor_av(ah)), (0.4, dir_av(ah))), ah - 14, td * 0.55 + lm * 0.8, tw * 0.55, th * 0.25, "corps",
       up=f_dents((236, 230, 206)))
    for sx in (-1, 1):                                                                        # oreilles
        po = add(ps, (th / 2, nor_av(ah)), (0.6, dir_av(ah)))
        if nom in ("varghulf", "morbheg"):
            m.cube("head", (sx * tw * 0.32 - 1, po[1] - 0.5, po[2] - 0.3), (2, 3.6, 0.6), "membrane", rot=(15, 0, sx * -18), pivot=po)
        else:
            m.cube("head", (sx * tw * 0.3 - 0.75, po[1] - 0.4, po[2] - 0.5), (1.5, 2.2 if chat else 2.6, 1), "corps", rot=(18, 0, sx * -8), pivot=po)
    if s.get("defenses"):                                                                    # canines en sabre
        for sx in (-1, 1):
            pd_ = add(pe, (-th * 0.3, nor_av(ah)))
            m.cube("head", (sx * tw * 0.2 - 0.45, pd_[1] - 3.6, pd_[2] - 0.8), (0.9, 4, 1), "dent", rot=(-12, 0, 0), pivot=pd_)
    if s.get("cornes"):
        for sx in (-1, 1):
            pc = add(ps, (th / 2, nor_av(ah)), (td * 0.25, dir_av(ah)))
            pc = (sx * tw * 0.25, pc[1], pc[2])
            q = ar(m, "head", pc, 35, 2.4, 1.2, 1.2, "corne")
            ar(m, "head", q, 12, 1.8, 0.8, 0.8, "corne")
    if s.get("defenses_haut"):                                                                # défenses de sanglier
        for sx in (-1, 1):
            pd_ = add(pm, (-th * 0.15, nor_av(ah)), (-0.6, dir_av(ah)))
            pd_ = (sx * (tw * 0.31 + 0.3), pd_[1], pd_[2])
            q = av(m, "head", pd_, 20, 1.8, 1.1, 1.1, "dent")
            av(m, "head", q, 75, 2.2, 0.8, 0.8, "dent")
    if fac == "khorne":                                                                       # collier de laiton
        m.cube("neck", (-W * 0.34, p0[1] - H * 0.35, p0[2] - 2.6), (W * 0.68, 1.4, 2.4), "or", rot=(-22, 0, 0), pivot=p0)
    # queue
    qn = s.get("queue", 6)
    if qn:
        m.bone("tail", "body", (0, yb + H - 1.5, L / 2))
        q = ar(m, "tail", (0, yb + H - 1.5, L / 2 - 0.5), 22 if not chat else -20, qn * 0.5, 1.4, 1.4, "corps", ext=0.5)
        q = ar(m, "tail", q, -6 if not chat else 10, qn * 0.5, 1.2, 1.2, "rose" if fac == "skaven" else ("poils" if chat or fac == "ogors" else "corps"), ext=0.4)
        if s.get("dard"):
            q = ar(m, "tail", q, 55, qn * 0.5, 1.1, 1.1, "corps")
            q = ar(m, "tail", q, 110, 2.4, 1.4, 1.4, "corne")
            m.cube("tail", (-0.5, q[1] - 0.5, q[2] - 0.5), (1, 1, 1), "lueur")
    if s.get("ailes"):
        if nom == "pusgoyle":
            for nomb, sx in (("wing_l", 1), ("wing_r", -1)):
                m.bone(nomb, "body", (sx * W / 2, yb + H, -1))
                C = Cadre((W / 2 - 0.5, yb + H, -1), 18)
                C.piece(m, nomb, (s["ailes"] * 0.45, 0, -1), 22, s["ailes"] * 0.5, 0.25, s["ailes"] * 0.9, "membrane", sx)
                C.piece(m, nomb, (s["ailes"] * 0.32, -0.2, 2), 48, s["ailes"] * 0.35, 0.25, s["ailes"] * 0.6, "membrane", sx)
        else:
            ailes_membrane(m, mats, (W / 2 - 1, yb + H, -L / 2 + L * 0.3), s["ailes"] * 1.2)
    if s.get("cavalier") or s.get("selle"):
        zs = -L / 2 + L * 0.42
        m.cube("body", (-W / 2 + 0.5, yb + H + (1.2 if voute else 0), zs - 2.5), (W - 1, 1, 5), "cuir", toutes=f_bande(A2, "haut"))
        m.selle = (yb + H + 1 + (1.2 if voute else 0), zs)
    if s.get("cavalier"):
        mini_cavalier(m, P, mats, fac, yb + H + 1, zs, s.get("arme_cavalier", "lance"), s.get("taille_cavalier", 1))
    return m, mats


# ------------------------------------------------------------------ mastodontes (Stonehorn, Thundertusk, Juggernaut, Stegadon...)
def mastodonte(nom, s, fac):
    P = s["pal"]
    mats = mats_creature(nom, s, fac)
    A2, LU = P["armure2"], P["lueur"]
    m = Modele(nom)
    W, H, L = s.get("corps", (16, 12, 22))
    lw, lh = s.get("jambe", (5, 10))
    tw, th, td = s.get("tete", (9, 8, 9))
    yb = lh
    m.bone("root", None, (0, 0, 0))
    m.bone("body", "root", (0, yb + H / 2, 0))
    # tronc en barrique avec bosse au garrot
    m.cube("body", (-W / 2, yb, -L / 2), (W, H + 1, L * 0.5), "corps")
    m.cube("body", (-W / 2 + 0.6, yb + 0.3, -L / 2 + L * 0.45), (W - 1.2, H - 0.6, L * 0.55), "corps")
    m.cube("body", (-W / 2 + 1.5, yb + H + 1, -L / 2 + 1.5), (W - 3, 2.2, L * 0.38), "corps")                   # bosse
    m.cube("body", (-W / 2 + 1.2, yb - 0.6, -L / 2 + 2), (W - 2.4, 0.7, L - 4), "ventre")
    if s.get("criniere"):                                                                     # toison
        m.cube("body", (-W / 2 - 0.5, yb + H * 0.25, -L / 2 - 0.5), (W + 1, H * 0.95, L * 0.55), "poils")
        m.cube("body", (-W / 2 - 0.3, yb - 2, -L / 2 + 1), (W + 0.6, 2.5, L * 0.45), "poils")
    if s.get("carapace"):
        m.cube("body", (-W / 2 - 1, yb + H - 2.5, -L / 2 + 0.5), (W + 2, 4.5, L - 1), "armure",
               up=combine(f_cadre(A2), f_rayures(mul(P["armure"], 0.6), A2) if fac == "seraphon" else None), toutes=f_bande(A2, "bas", 2))
    if s.get("plaques"):
        for i in range(int((L - 4) // 3)):
            hh = 3 + (i % 2) * 2
            m.cube("body", (-1, yb + H + 1.5, -L / 2 + 2 + i * 3), (2, hh, 2.5), "armure2", north=f_bande(LU, "haut"),
                   rot=(15, 0, 0), pivot=(0, yb + H + 1.5, -L / 2 + 3 + i * 3))
    if s.get("crete_dos"):
        for k in range(int(L // 3)):
            z = -L / 2 + 1.5 + k * 3
            m.cube("body", (-0.5, yb + H + 1, z), (1, 2.6, 1.4), "corne", rot=(20, 0, 0), pivot=(0, yb + H + 1, z + 0.7))
    if fac == "khorne":                                                                       # bardes de laiton du Juggernaut
        for sx in (-1, 1):
            m.cube("body", (sx * (W / 2 + 0.2) - (0.6 if sx < 0 else 0), yb + 1, -L / 2 + 1), (0.6, H - 1, L * 0.5), "armure2",
                   east=f_cadre(mul(P["armure"], 0.7)), west=f_cadre(mul(P["armure"], 0.7)))
    # pattes-colonnes légèrement fléchies
    for nomj, sx, av_ in (("leg_fl", -1, 1), ("leg_fr", 1, 1), ("leg_bl", -1, 0), ("leg_br", 1, 0)):
        x = sx * (W / 2 - lw / 2 - 0.3)
        z = -L / 2 + lw / 2 + 1.5 if av_ else L / 2 - lw / 2 - 1.5
        h0 = (x, yb + 2.5, z)
        m.bone(nomj, "root", h0)
        segs = [(-6 if av_ else -12, 0.5, lw + 1.6, lw + 2, "corps"), (5 if av_ else 12, 0.5, lw + 0.4, lw + 0.6, "corps")]
        p = jambe(m, nomj, h0, segs, 1.5)
        mp = "sombre" if s.get("sabots") else "corps"
        m.cube(nomj, (x - lw * 0.62, 0, p[2] - lw * 0.68), (lw * 1.24, 1.6, lw * 1.36), mp)
        if not s.get("sabots"):
            for k in range(3):
                m.cube(nomj, (x - lw * 0.5 + k * lw * 0.38, 0, p[2] - lw * 0.68 - 0.6), (0.9, 1.0, 0.8), "corne")
        if s.get("carapace") or fac == "khorne":
            m.cube(nomj, (x - lw * 0.55, lh * 0.55, h0[2] - lw * 0.65), (lw * 1.1, 1.8, lw * 1.3), "armure2")
    # tête basse et massive
    p0 = (0, yb + H * 0.55, -L / 2 + 1)
    m.bone("neck", "body", p0)
    p1 = av(m, "neck", p0, -8, s.get("cou", 2) + 2, W * 0.6, H * 0.7, "corps", ext=1.5)
    m.bone("head", "neck", p1)
    ah = -14
    ps = add(p1, (-1, dir_av(ah)))
    pe = av(m, "head", ps, ah, td * 0.65, tw, th, "corps", ext=1)
    pm = av(m, "head", add(pe, (-th * 0.12, nor_av(ah))), ah - 8, td * 0.4, tw * 0.75, th * 0.6, "corps", ext=0.6)
    yeux = "lueur" if fac in ("khorne", "ossiarch", "lumineth", "seraphon") else "sombre"
    oeil(m, "head", add(ps, (td * 0.3, dir_av(ah)), (th * 0.15, nor_av(ah))), tw / 2, 1.0, yeux, reflet=(yeux == "sombre"))
    m.bone("jaw", "head", add(ps, (-th * 0.45, nor_av(ah))))
    av(m, "jaw", add(ps, (-th * 0.42, nor_av(ah)), (0.5, dir_av(ah))), ah - 10, td * 0.85, tw * 0.6, th * 0.26, "corps", up=f_dents((236, 230, 206)))
    if s.get("cornes"):
        for sx in (-1, 1):
            pc = add(ps, (th * 0.4, nor_av(ah)), (td * 0.2, dir_av(ah)))
            pc = (sx * (tw / 2 - 0.5), pc[1], pc[2])
            m.cube("head", (sx * (tw / 2 + 1.8) - 1.4, pc[1] - 1, pc[2] - 1), (2.8, 2, 2), "corne")
            q = (sx * (tw / 2 + 2.6), pc[1], pc[2])
            q = av(m, "head", q, 30, 3.2, 1.6, 1.6, "corne")
            av(m, "head", q, 60, 2.4, 1.1, 1.1, "corne")
    if s.get("corne_nez"):
        pn = add(pm, (th * 0.25, nor_av(ah)), (0.5, dir_av(ah)))
        q = av(m, "head", pn, 55, 3.4, 2.2, 2.2, "corne")
        av(m, "head", q, 78, 2.8, 1.4, 1.4, "corne")
    if s.get("defenses"):
        for sx in (-1, 1):
            pd_ = add(pm, (-th * 0.2, nor_av(ah)), (-1, dir_av(ah)))
            pd_ = (sx * tw * 0.32, pd_[1], pd_[2])
            q = av(m, "head", pd_, -55, 3.2, 1.5, 1.5, "dent")
            q = av(m, "head", q, -10, 3.2, 1.3, 1.3, "dent")
            av(m, "head", q, 40, 2.6, 1.0, 1.0, "dent")
    if s.get("collerette"):
        pc = add(ps, (th * 0.2, nor_av(ah)), (td * 0.05, dir_av(ah)))
        m.cube("head", (-tw / 2 - 1.5, pc[1] - th * 0.2, pc[2] + 0.5), (tw + 3, th + 1.5, 0.8), "armure2", south=f_cadre(LU), north=f_bande(LU, "haut"),
               rot=(-35, 0, 0), pivot=(0, pc[1] - th * 0.2, pc[2] + 0.5))
        for sx in (-1, 0, 1):
            m.cube("head", (sx * (tw / 2) - 0.5, pc[1] + th * 1.1, pc[2] + 0.2 + th * 0.6), (1, 1.6, 1), "corne")
    if fac == "khorne":
        av(m, "head", add(ps, (th / 2 + 0.2, nor_av(ah))), ah, td * 0.8, tw * 0.8, 0.7, "armure2")
    # queue
    qn = s.get("queue", 4)
    if qn:
        m.bone("tail", "body", (0, yb + H - 2, L / 2))
        q = ar(m, "tail", (0, yb + H - 2, L / 2 - 0.5), -28, qn * 0.6 + 1, 2.4, 2.4, "corps", ext=0.6)
        q = ar(m, "tail", q, -42, qn * 0.5 + 0.5, 1.8, 1.8, "corps")
        if s.get("queue_massue"):
            m.cube("tail", (-2.5, q[1] - 2.5, q[2] - 1), (5, 5, 4), "armure2", toutes=f_cadre(mul(A2, 0.7)))
            for (dx, dy) in ((-3, 1.5), (2.5, 1.5), (-0.5, 4.5)):
                m.cube("tail", (dx, q[1] - 2.5 + dy, q[2]), (1, 1, 1.5), "corne")
        elif qn <= 6 and not s.get("criniere"):
            m.cube("tail", (-1.2, q[1] - 2, q[2] - 0.6), (2.4, 2.4, 1.6), "poils")
    # cavalier, nacelle, autel
    if s.get("cavalier") or s.get("selle"):
        zs = -L / 2 + L * 0.4
        m.cube("body", (-W / 2 + 1, yb + H + 1, zs - 3), (W - 2, 1.2, 6.5), "cuir", toutes=f_bande(A2, "haut"))
        m.selle = (yb + H + 2.2, zs)
    if s.get("cavalier"):
        mini_cavalier(m, P, mats, fac, yb + H + 2.2, zs, s.get("arme_cavalier", "lance"), s.get("taille_cavalier", 1))
    if s.get("nacelle"):
        y0 = yb + H + (3 if s.get("criniere") else 1)
        m.cube("body", (-W / 2 + 0.5, y0, -3), (W - 1, 5, 10), "bois", toutes=f_bande(A2, "haut", 2))
        for (x, z) in ((-W / 2 + 0.5, -3), (W / 2 - 1.5, -3), (-W / 2 + 0.5, 6), (W / 2 - 1.5, 6)):
            m.cube("body", (x, y0 + 5, z), (1, 4, 1), "or")
        m.cube("body", (-W / 2 + 0.5, y0 + 9, -3), (W - 1, 0.5, 10), "tissu", up=f_bande(A2, "bas"))
        if fac == "seraphon":
            m.cube("body", (-1.5, y0 + 5, 0.5), (3, 3, 3), "lueur")
        if nom == "thundertusk":
            m.cube("body", (-2, y0 + 5, 1), (4, 4, 4), "lueur")
    if s.get("autel"):
        m.cube("body", (-3, yb + H + 2, -2), (6, 8, 6), "or", north=f_etoile(LU) if fac != "seraphon" else f_comete(LU))
        m.cube("body", (-2, yb + H + 10, -1), (4, 4, 4), "lueur")
    return m, mats


# ------------------------------------------------------------------ squigs : une gueule sur pattes
def squig(nom, s, fac):
    P = s["pal"]
    mats = mats_creature(nom, s, fac)
    A2 = P["armure2"]
    m = Modele(nom)
    r = s.get("taille", 10)
    Rr = r / 2
    cy = Rr + 2.2
    m.bone("root", None, (0, 0, 0))
    m.bone("body", "root", (0, cy, 0))
    ym0, ym1 = cy - 0.55 * Rr, cy + 0.12 * Rr          # bas et haut de la gueule
    zf = -0.25 * Rr                                    # fond de la gueule

    def boule(b, x0, x1, y0, y1, z0, z1, matr, n=7):
        """Sphère en tranches horizontales (croix + carré par tranche), tronquée au pavé demandé."""
        for k in range(n):
            ya, yb_ = -1 + 2 * k / n, -1 + 2 * (k + 1) / n
            yc = 0 if ya * yb_ <= 0 else min(abs(ya), abs(yb_))
            rr = math.sqrt(max(0.0, 1 - yc * yc))
            for (ax, az) in ((rr, rr * 0.6), (rr * 0.6, rr), (rr * 0.86, rr * 0.86)):
                bx0, bx1 = max(x0, -Rr * ax), min(x1, Rr * ax)
                by0, by1 = max(y0, cy + Rr * ya), min(y1, cy + Rr * yb_)
                bz0, bz1 = max(z0, -Rr * az), min(z1, Rr * az)
                if bx1 - bx0 > 0.2 and by1 - by0 > 0.2 and bz1 - bz0 > 0.2:
                    m.cube(b, (bx0, by0, bz0), (bx1 - bx0, by1 - by0, bz1 - bz0), matr)

    boule("body", -Rr, Rr, cy - Rr, cy + Rr, zf, Rr, "corps")                    # arrière
    boule("body", -Rr, Rr, ym1, cy + Rr, -Rr, zf + 0.5, "corps")                 # crâne au-dessus de la gueule
    for sx in (-1, 1):                                                           # joues
        m.cube("body", (sx * Rr * 0.86 - (0.8 if sx > 0 else 0), ym0, -Rr * 0.6), (0.8, ym1 - ym0, Rr * 0.6 + zf + 0.5), "corps")
    m.cube("body", (-Rr * 0.86, ym0, zf - 0.1), (Rr * 1.72, ym1 - ym0, 0.4), "sombre")                         # gosier
    m.cube("body", (-Rr * 0.7, ym1 - 0.6, -Rr * 0.85), (Rr * 1.4, 0.6, Rr * 0.85 + zf), "rose")                 # palais
    m.bone("jaw", "body", (0, ym0, zf))
    boule("jaw", -Rr * 0.95, Rr * 0.95, cy - Rr, ym0, -Rr * 0.95, zf + 0.5, "corps")
    m.cube("jaw", (-Rr * 0.62, ym0 - 0.2, -Rr * 0.7), (Rr * 1.24, 0.6, Rr * 0.7 + zf), "rose")                  # langue
    m.cube("body", (-Rr * 0.8, cy - Rr + 0.2, -Rr * 0.4), (Rr * 1.6, 0.5, Rr * 1.2), "ventre")
    # crocs en dents de scie : rangée du haut (vers le bas) et du bas (vers le haut)
    n = max(5, int(Rr * 1.4))
    for k in range(n):
        x = -Rr * 0.78 + k * (Rr * 1.56) / (n - 1)
        bord = abs(x) / Rr
        zz = -Rr * 0.86 + bord * bord * Rr * 0.4
        g = 1.0 + (0.6 if k % 3 == 1 else 0) + Rr * 0.04
        m.cube("body", (x - 0.45, ym1 - g - 0.3, zz), (0.9, g + 0.3, 0.9), "dent")
        if k % 2 == 0:
            m.cube("jaw", (x - 0.4, ym0 - 0.2, zz + 0.2), (0.8, g * 0.8 + 0.2, 0.8), "dent")
    # petits yeux méchants sur le dessus, arcades froncées
    for sx in (-1, 1):
        ex = sx * Rr * 0.38
        m.cube("body", (ex - 0.9, cy + Rr * 0.58, -Rr * 0.72), (1.8, 1.6, 1.4), "blanc")
        m.cube("body", (ex - 0.4 + sx * 0.2, cy + Rr * 0.58 + 0.3, -Rr * 0.72 - 0.15), (0.8, 0.9, 0.3), "sombre")
        m.cube("body", (ex - 1.3, cy + Rr * 0.58 + 1.4, -Rr * 0.78), (2.6, 0.7, 1.6), "corps", rot=(0, 0, sx * 18),
               pivot=(ex, cy + Rr * 0.58 + 1.6, -Rr * 0.7))
    # verrues et taches claires
    for (x, y, z) in ((-Rr * 0.7, cy + Rr * 0.5, Rr * 0.2), (Rr * 0.6, cy + Rr * 0.65, Rr * 0.4), (-Rr * 0.2, cy + Rr * 0.9, Rr * 0.3),
                      (Rr * 0.88, cy, Rr * 0.3), (-Rr * 0.92, cy + Rr * 0.1, -Rr * 0.1)):
        m.cube("body", (x - 0.5, y - 0.5, z - 0.5), (1.1, 1.1, 1.1), "ventre")
    if Rr >= 7:
        for sx in (-1, 1):                                                       # cornes des gros squigs
            pc = (sx * Rr * 0.55, cy + Rr * 0.75, -Rr * 0.1)
            q = av(m, "body", pc, 50, Rr * 0.35, 1.8, 1.8, "corne")
            av(m, "body", q, 85, Rr * 0.25, 1.2, 1.2, "corne")
    # pattes courtes et griffues à l'arrière
    for nomj, sx in (("leg_l", -1), ("leg_r", 1)):
        x = sx * Rr * 0.5
        m.bone(nomj, "root", (x, 3, Rr * 0.3))
        m.cube(nomj, (x - 1.3, 0.8, Rr * 0.3 - 1.3), (2.6, 3, 2.6), "corps")
        m.cube(nomj, (x - 1.6, 0, Rr * 0.3 - 2.8), (3.2, 1.1, 4), "corps")
        for k in range(3):
            m.cube(nomj, (x - 1.4 + k * 1.1, 0, Rr * 0.3 - 3.5), (0.6, 0.7, 0.9), "corne")
    if s.get("cavalier") or s.get("selle"):
        m.cube("body", (-Rr * 0.5, cy + Rr - 0.2, -1.5), (Rr, 1, 4), "cuir", toutes=f_bande(A2, "haut"))
        m.selle = (cy + Rr + 0.8, 0.5)
    if s.get("cavalier"):
        mini_cavalier(m, P, mats, fac, cy + Rr + 0.8, 0.5, s.get("arme_cavalier", "lance"), 0.8 if Rr < 6 else 1.0)
    return m, mats


# ------------------------------------------------------------------ disque de Tzeentch
def disque(nom, s, fac):
    P = s["pal"]
    mats = mats_creature(nom, s, fac)
    A2, LU = P["armure2"], P["lueur"]
    mat(mats, "flamme", (120, 200, 255), "lueur")
    mat(mats, "flamme_rose", (240, 120, 200), "lueur")
    m = Modele(nom)
    R_ = s.get("rayon", 8)
    y0 = 7
    m.bone("root", None, (0, 0, 0))
    m.bone("body", "root", (0, y0, 0))
    # plateau en anneaux : cuivre dessous, turquoise dessus
    for (r, h, y, matr) in ((R_, 1.2, y0, "armure2"), (R_ * 0.86, 1.0, y0 + 1.2, "armure"), (R_ * 0.55, 0.8, y0 + 2.2, "armure2"),
                            (R_ * 0.75, 1.0, y0 - 1.0, "armure2"), (R_ * 0.4, 1.2, y0 - 2.2, "armure")):
        for (ax, az) in ((1.0, 0.62), (0.62, 1.0), (0.87, 0.87)):
            m.cube("body", (-r * ax, y, -r * az), (2 * r * ax, h, 2 * r * az), matr)
    # couronne de lames
    for k in range(12):
        an = k * math.pi / 6
        x, z = math.sin(an) * (R_ + 0.4), math.cos(an) * (R_ + 0.4)
        m.cube("body", (x - 0.5, y0 + 0.2, z - 0.5), (1, 0.8, 1), "lame")
        m.cube("body", (x * 1.12 - 0.35, y0 + 0.35, z * 1.12 - 0.35), (0.7, 0.5, 0.7), "lame")
    # œil changeant au centre, tourné vers l'avant
    m.cube("body", (-1.6, y0 + 3.0, -R_ * 0.55 - 0.2), (3.2, 2.2, 1.2), "blanc")
    m.cube("body", (-0.7, y0 + 3.4, -R_ * 0.55 - 0.4), (1.4, 1.4, 0.4), "lueur")
    # traînée de feu magique sous le disque
    for k, (r, matr) in enumerate(((R_ * 0.35, "flamme"), (R_ * 0.25, "flamme_rose"), (R_ * 0.15, "flamme"))):
        m.cube("body", (-r, y0 - 3.4 - k * 1.4, -r + k * 0.6), (2 * r, 1.4, 2 * r), matr)
    m.selle = (y0 + 3.0, 0.5)
    return m, mats


# ------------------------------------------------------------------ aiguillage
FORMES = {
    "cheval": {"cavalier_franc", "chevalier_chaos", "blood_knight", "dreadblade", "kavalos", "seeker"},
    "griffon": {"griffon", "demigryph", "gryph_charger"},
    "dragon": {"dragon", "stardrake", "dragon_zombie", "dracoth", "magmadroth", "maw_krusha", "salamandre", "terrorgheist"},
    "theropode": {"carnosaur"},
    "fauve": {"chien_khorne", "sabre_givre", "bete_zombie", "varghulf", "demon_slaanesh", "morbheg", "pusgoyle"},
    "mastodonte": {"stonehorn", "thundertusk", "juggernaut", "stegadon", "bastiladon", "gothizzar", "alarith"},
}
FN = {"cheval": cheval, "griffon": griffon, "dragon": dragon, "theropode": theropode, "fauve": fauve, "mastodonte": mastodonte}


def forme(nom):
    for f, ids in FORMES.items():
        if nom in ids:
            return FN[f]
    return None
