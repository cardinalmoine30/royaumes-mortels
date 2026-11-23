# -*- coding: utf-8 -*-
"""Humanoïdes détaillés : armure en plaques superposées, gantelets, bottes, genouillères, ceinture et boucle,
épaulières à plusieurs étages, casques propres à chaque faction, visages (yeux, nez, bouche), barbes,
capes à ourlet, armes détaillées, boucliers à bordure, ornements de faction (crânes, pustules, chaînes,
malepierre, runes, cristaux, mousse…)."""
from modele2 import Modele, mul, mix

# ------------------------------------------------------------------ gabarits
#            jambe (w,h,d)  torse (w,h,d)  bras (w,h,d)  tête
CORPS = {
    "massif": ((5, 13, 6), (14, 12, 8), (5, 11, 6), 8),
    "normal": ((4, 12, 4), (8, 12, 4), (4, 12, 4), 8),
    "fin": ((3, 14, 3), (8, 12, 4), (3, 13, 3), 7),
    "petit": ((3, 7, 3), (8, 8, 5), (3, 9, 3), 7),
    "nain": ((4, 6, 5), (12, 10, 7), (4, 9, 5), 8),
    "squelette": ((2, 12, 2), (8, 12, 3), (2, 12, 2), 8),
    "spectre": (None, (8, 12, 5), (3, 12, 3), 8),
    "geant": ((6, 12, 6), (16, 14, 10), (6, 14, 6), 8),
}

# ------------------------------------------------------------------ style des factions
STYLE = {
    "stormcast": dict(armure="or", casque="sc", orn=("laurier",)),
    "cites": dict(casque="morion", orn=("plumet", "echarpe")),
    "khaine": dict(casque="khaine", orn=("bijoux",)),
    "fyreslayers": dict(casque="fyre", orn=("runes", "bijoux")),
    "idoneth": dict(casque="idoneth", orn=("nageoires",)),
    "kharadron": dict(casque="khar", orn=("tuyaux",)),
    "lumineth": dict(casque="lum", orn=("cristaux",)),
    "seraphon": dict(peau="ecaille", orn=("bijoux", "plumes")),
    "sylvaneth": dict(peau="bois", armure="bois", orn=("mousse",)),
    "esclaves": dict(casque="chaos", orn=("pointes",)),
    "tzeentch": dict(casque="chaos", orn=("plumes",)),
    "khorne": dict(casque="khorne", orn=("cranes", "pointes")),
    "slaanesh": dict(casque="slaanesh", orn=("bijoux",)),
    "nurgle": dict(casque="nurgle", orn=("pustules", "rouille")),
    "skaven": dict(peau="fourrure", casque="skaven", orn=("malepierre", "haillons")),
    "hashut": dict(casque="hashut", orn=("pointes", "runes")),
    "fec": dict(orn=("haillons", "os")),
    "nighthaunt": dict(tissu="ether", peau="ether", orn=("chaines",)),
    "ossiarch": dict(armure="os", peau="os", casque="ossi", orn=("os",)),
    "soulblight": dict(casque="sb", orn=("col",)),
    "gitz": dict(orn=("champignons", "lune")),
    "ogors": dict(orn=("plaque_ventre",)),
    "orruks": dict(casque="orruk", orn=("rayures", "rivets")),
    "behemat": dict(orn=("corde",)),
}


def materiaux(P, st, s):
    peau_t = st.get("peau", "peau")
    if s.get("face") == "crane" or s.get("corps") == "squelette":
        peau_t = "os"
    pal = {
        "armure": (P["armure"], st.get("armure", "metal")),
        "armure2": (P["armure2"], "or" if P["armure2"][0] > 150 and P["armure2"][1] > 120 and P["armure2"][2] < 120 else "metal"),
        "tissu": (P["tissu"], st.get("tissu", "tissu")),
        "peau": (P["peau"], peau_t),
        "ventre": (P.get("ventre", mul(P["peau"], 1.2)), peau_t if peau_t != "ecaille" else "peau"),
        "cuir": (P.get("cuir", (92, 62, 40)), "cuir"),
        "metal": (P["metal"], "metal"),
        "lame": (P.get("lame", (205, 210, 220)), "metal"),
        "manche": (P.get("manche", (78, 52, 34)), "bois"),
        "lueur": (P["lueur"], "lueur"),
        "corne": (P.get("corne", (222, 208, 172)), "corne"),
        "poils": (P.get("poils", (96, 72, 50)), "fourrure"),
        "sombre": ((16, 16, 20), "sombre"),
        "bouclier": (P.get("bouclier", P["armure"]), "metal"),
        "membrane": (P.get("membrane", mul(P["peau"], 0.8)), "membrane"),
        "plume": (P.get("plume", (236, 236, 242)), "plume"),
        "chaine": ((96, 96, 104), "chaine"),
        "or": ((214, 172, 64), "or"),
        "os": ((226, 216, 190), "os"),
        "dent": ((236, 230, 206), "os"),
        "bois": (P.get("bois", (104, 76, 48)), "bois"),
        "pierre": ((128, 124, 116), "pierre"),
        "mousse": ((82, 128, 52), "fourrure"),
        "malepierre": ((90, 255, 70), "lueur"),
        "blanc": ((240, 236, 228), "peau"),
    }
    m = {k: {"c": c, "type": t} for k, (c, t) in pal.items()}
    if peau_t == "ecaille":
        m["peau"]["c2"] = P.get("ventre", mul(P["peau"], 1.3))
    return m


# ------------------------------------------------------------------ dessins (coordonnées en texels)
def f_bande(c, ou="bas", ep=1):
    def f(d, x, y, w, h, px):
        for k in range(ep):
            yy = y + (h - 1 - k if ou == "bas" else k)
            d.line((x, yy, x + w - 1, yy), fill=c)
    return f


def f_cadre(c):
    return lambda d, x, y, w, h, px: d.rectangle((x, y, x + w - 1, y + h - 1), outline=c)


def f_comete(c, fond=None):
    def f(d, x, y, w, h, px):
        if fond:
            d.rectangle((x + 1, y + 1, x + w - 2, y + h - 2), fill=fond)
        cx, cy = x + w // 2, y + h // 3
        d.ellipse((cx - 2, cy - 2, cx + 1, cy + 1), fill=c)
        d.line((cx - 1, cy + 1, x + 1, y + h - 2), fill=c, width=1)
        d.line((cx, cy + 1, x + w - 2, y + h - 2), fill=c, width=1)
    return f


def f_etoile(c):
    def f(d, x, y, w, h, px):
        cx, cy = x + w // 2, y + h // 2
        r = max(2, min(w, h) // 2 - 1)
        for dx, dy in ((0, -1), (0, 1), (-1, 0), (1, 0), (-0.7, -0.7), (0.7, 0.7), (-0.7, 0.7), (0.7, -0.7)):
            d.line((cx, cy, cx + dx * r, cy + dy * r), fill=c)
            d.point((cx + dx * r, cy + dy * r), fill=c)
    return f


def f_crane(c, yeux=(20, 20, 24)):
    def f(d, x, y, w, h, px):
        cx, cy = x + w // 2, y + h // 2
        r = max(2, min(w, h) // 3)
        d.ellipse((cx - r, cy - r, cx + r - 1, cy + r - 1), fill=c)
        d.rectangle((cx - r // 2, cy + r - 1, cx + r // 2 - 1, cy + r), fill=c)
        d.point((cx - r // 2, cy - 1), fill=yeux)
        d.point((cx + r // 2 - 1, cy - 1), fill=yeux)
    return f


def f_croc(c):
    def f(d, x, y, w, h, px):
        d.polygon([(x + 1, y + 1), (x + w - 2, y + 1), (x + w // 2, y + h - 2)], fill=c)
    return f


def f_eclair(c):
    def f(d, x, y, w, h, px):
        pts = [(x + w * 0.6, y + 1), (x + w * 0.25, y + h * 0.55), (x + w * 0.6, y + h * 0.5), (x + w * 0.35, y + h - 2)]
        d.line(pts, fill=c, width=max(1, w // 6))
    return f


def f_yeux(c, fond=None, hauteur=0.42, ecart=0.22, taille=1):
    def f(d, x, y, w, h, px):
        yy = y + int(h * hauteur)
        for sx in (-1, 1):
            xx = x + w // 2 + sx * int(w * ecart) - (1 if sx < 0 else 0)
            if fond:
                d.rectangle((xx - taille, yy - taille, xx + taille, yy + taille - 1), fill=fond)
            d.rectangle((xx - taille + 1, yy - taille + 1, xx + taille - 1, yy + taille - 1), fill=c)
    return f


def f_visage(peau, yeux=(30, 30, 40), bouche=None, sourcils=None):
    def f(d, x, y, w, h, px):
        yy = y + int(h * 0.42)
        for sx in (-1, 1):
            xx = x + w // 2 + sx * int(w * 0.22) - (1 if sx < 0 else 0)
            d.rectangle((xx - 1, yy, xx + 1, yy + 1), fill=(240, 240, 236))
            d.point((xx if sx < 0 else xx, yy + 1), fill=yeux)
            d.point((xx, yy), fill=yeux)
            d.line((xx - 1, yy - 2, xx + 1, yy - 2), fill=sourcils or mul(peau, 0.45))
        d.line((x + w // 2 - 2, y + int(h * 0.78), x + w // 2 + 1, y + int(h * 0.78)), fill=bouche or mul(peau, 0.5))
        d.point((x + w // 2 - 1, y + int(h * 0.62)), fill=mul(peau, 0.75))
    return f


def f_dents(c=(236, 232, 210)):
    def f(d, x, y, w, h, px):
        for i in range(1, w - 1, 2):
            d.line((x + i, y, x + i, y + max(1, h // 2)), fill=c)
    return f


def f_fente_t(c=(14, 14, 18), lueur=None):
    def f(d, x, y, w, h, px):
        yy = y + int(h * 0.4)
        d.rectangle((x + 2, yy, x + w - 3, yy + 1), fill=c)
        d.rectangle((x + w // 2 - 1, yy, x + w // 2, y + int(h * 0.85)), fill=c)
        if lueur:
            d.point((x + w // 2 - 3, yy), fill=lueur)
            d.point((x + w // 2 + 2, yy), fill=lueur)
    return f


def f_runes(c):
    def f(d, x, y, w, h, px):
        for k in range(2, w - 2, 4):
            d.line((x + k, y + 2, x + k, y + 5), fill=c)
            d.point((x + k + 1, y + 3), fill=c)
    return f


def f_rayures(c1, c2):
    def f(d, x, y, w, h, px):
        for i in range(w):
            for j in range(h):
                if ((i + j) // 2) % 2 == 0 and (i < 3 or j < 3):
                    px[x + i, y + j] = c2 + (255,) if ((i + j) // 2) % 4 == 0 else c1 + (255,)
    return f


def f_anneau(c):
    def f(d, x, y, w, h, px):
        for i in range(w):
            for j in range(h):
                px[x + i, y + j] = (0, 0, 0, 0)
        cx, cy = x + (w - 1) / 2, y + (h - 1) / 2
        r = min(w, h) / 2 - 3
        for i in range(w):
            for j in range(h):
                dd = ((x + i - cx) ** 2 + (y + j - cy) ** 2) ** 0.5
                if r - 1.2 <= dd <= r + 0.6:
                    px[x + i, y + j] = c + (255,)
        import math
        for k in range(10):
            an = k * math.pi / 5 + 0.3
            for t in range(3):
                xx, yy = int(cx + math.cos(an) * (r + 1 + t)), int(cy + math.sin(an) * (r + 1 + t))
                if x <= xx < x + w and y <= yy < y + h and an % (2 * math.pi) < 3.3:
                    px[xx, yy] = c + (255,)
    return f


def combine(*fs):
    fs = [f for f in fs if f]

    def f(*a):
        for g in fs:
            g(*a)
    return f


# ------------------------------------------------------------------ construction
def humanoide(nom, s, fac):
    st = STYLE.get(fac, {})
    P = s["pal"]
    mats = materiaux(P, st, s)
    m = Modele(nom)
    corps = s["corps"]
    jambe, torse, bras, hs = CORPS[corps]
    arm = bool(s.get("armure"))
    ex = set(s.get("extras", ())) | set(st.get("orn", ()))
    A2 = P["armure2"]
    LU = P["lueur"]
    lh = jambe[1] if jambe else 10
    tw, th, td = torse
    aw, ah, ad = bras
    yt = lh + th
    hx = -hs / 2
    mt = "armure" if arm else "tissu"        # matière du torse
    mb = "armure" if arm else "peau"         # matière des bras

    m.bone("root", None, (0, 0, 0))
    m.bone("body", "root", (0, lh, 0))
    m.bone("head", "body", (0, yt, 0))
    m.bone("right_arm", "body", (-tw / 2 - aw / 2, yt - 1, 0))
    m.bone("left_arm", "body", (tw / 2 + aw / 2, yt - 1, 0))
    m.bone("weapon", "right_arm", (-tw / 2 - aw / 2, yt - ah, 0))
    m.bone("offhand", "left_arm", (tw / 2 + aw / 2, yt - ah, 0))

    # ---------------- jambes
    if jambe:
        jw, jh, jd = jambe
        for os_, x in (("right_leg", -jw), ("left_leg", 0)):
            m.bone(os_, "root", (x + jw / 2, lh, 0))
            m.cube(os_, (x, 0, -jd / 2), (jw, jh, jd), "armure" if arm else ("peau" if corps in ("squelette",) or fac in ("sylvaneth", "seraphon", "skaven", "fec", "ogors", "behemat", "gitz") else "tissu"))
            hb = max(2, jh * 0.35)
            m.cube(os_, (x - 0.5, 0, -jd / 2 - 0.5), (jw + 1, hb, jd + 1), "armure2" if arm else "cuir",
                   north=f_bande(mul(A2, 0.7) if arm else (60, 40, 28), "haut"))
            if arm:
                m.cube(os_, (x + 0.5, jh * 0.42, -jd / 2 - 1), (jw - 1, max(1.5, jh * 0.16), 1), "armure2")   # genouillère
                m.cube(os_, (x + 0.5, hb, -jd / 2 - 0.5), (jw - 1, jh * 0.3, 0.5), "armure")                   # grève
            m.cube(os_, (x - 0.5, 0, -jd / 2 - 1.5), (jw + 1, 1, 1.5), "armure2" if arm else "cuir")             # pointe du pied
    elif s.get("serpent"):
        m.bone("tail", "root", (0, lh, 0))
        segs = [(-4.5, 4, -3.5, 9, 7, 7), (-3.5, 1.5, 2.5, 7, 5.5, 8), (-2.5, 0, 9.5, 5, 4, 7), (-1.5, 0, 15.5, 3, 3, 6), (-0.75, 0, 20.5, 1.5, 2, 4)]
        for x, y, z, w, h, d in segs:
            m.cube("tail", (x, y, z), (w, h, d), "peau", up=f_bande(mul(A2, 0.9), "haut"))
            m.cube("tail", (x + 0.5, y - 0.5, z + 0.5), (w - 1, 0.5, d - 1), "ventre")
    else:     # spectre : robe en lambeaux flottante
        m.cube("body", (-5, 4, -3.5), (10, 6, 7), "tissu")
        m.cube("body", (-4, 1, -3), (8, 3, 6), "tissu")
        m.cube("body", (-3, -1, -2), (6, 2, 4), "tissu")
        if "chaines" in ex:
            m.cube("body", (-4.5, 3, -3.8), (0.5, 6, 0.5), "chaine")
            m.cube("body", (3.5, 2, -3.8), (0.5, 7, 0.5), "chaine")

    # ---------------- bassin, ceinture, jupe d'armes
    m.cube("body", (-tw / 2 - 0.5, lh, -td / 2 - 0.5), (tw + 1, 2, td + 1), "cuir",
           north=lambda d, x, y, w, h, px: d.rectangle((x + w // 2 - 2, y, x + w // 2 + 1, y + h - 1), fill=mul(mats["or"]["c"], 1.05)))
    m.cube("body", (-1.5, lh - 0.5, -td / 2 - 1), (3, 2.5, 0.5), "or")                                       # boucle
    if arm:
        for x in (-tw / 2, tw / 4 - 1):
            m.cube("body", (x + 0.5, lh - 4, -td / 2 - 0.5), (tw / 4 + 1.5, 4, 0.5), "armure", north=f_bande(A2, "bas"))
        for sx in (-1, 1):
            m.cube("body", (sx * (tw / 2) - (0.5 if sx > 0 else 0), lh - 3.5, -td / 2 + 1), (0.5, 3.5, td - 2), "armure")
    if "tabard" in ex or (not arm and corps in ("normal", "fin", "massif") and fac not in ("sylvaneth", "nighthaunt")):
        m.cube("body", (-tw / 4, max(1, lh - 8), -td / 2 - 1), (tw / 2, 9, 0.5), "tissu", north=f_bande(A2, "bas", 2))
        m.cube("body", (-tw / 4, max(1, lh - 7), td / 2 + 0.5), (tw / 2, 8, 0.5), "tissu", south=f_bande(A2, "bas", 2))

    # ---------------- torse
    em = {"comete": f_comete(LU if s.get("embleme_lueur") else mul(A2, 1.15)),
          "etoile": f_etoile(LU if s.get("embleme_lueur") else A2),
          "crane": f_crane(LU if s.get("embleme_lueur") else (226, 216, 190)),
          "croc": f_croc(LU if s.get("embleme_lueur") else A2)}.get(s.get("embleme"), None)
    corps_mat = "peau" if not arm and fac in ("sylvaneth", "seraphon", "skaven", "fec", "ogors", "behemat", "gitz", "orruks", "khorne", "slaanesh", "nurgle", "tzeentch") and not s.get("face") == "capuche" else mt
    if corps == "spectre":
        corps_mat = "tissu"
    m.cube("body", (-tw / 2, lh + 1.5, -td / 2), (tw, th - 1.5, td), corps_mat,
           north=None if arm else (lambda d, x, y, w, h, px: (d.line((x + w // 2, y + 3, x + w // 2, y + h - 4), fill=mul(P["peau"], 0.78)),
                                                              d.line((x + 3, y + h // 3, x + w - 4, y + h // 3), fill=mul(P["peau"], 0.82)))) if corps_mat == "peau" else None)
    if arm:
        # plastron, plaques abdominales, dossière, gorgerin
        m.cube("body", (-tw / 2 + 1, lh + th * 0.45, -td / 2 - 0.5), (tw - 2, th * 0.55 - 0.5, 0.5), "armure",
               north=combine(f_cadre(mul(A2, 0.95)), em))
        for k in range(2):
            m.cube("body", (-tw / 2 + 1.5, lh + 2 + k * 2.2, -td / 2 - 0.5), (tw - 3, 1.8, 0.5), "armure2" if k == 0 else "armure")
        m.cube("body", (-tw / 2 + 1, lh + 3, td / 2), (tw - 2, th - 4, 0.5), "armure", south=f_cadre(A2))
        m.cube("body", (-tw / 2 + 1.5, yt - 1, -td / 2 + 0.5), (tw - 3, 2, td - 1), "armure2")
    else:
        if em:
            m.cube("body", (-1.5, yt - 6, -td / 2 - 0.5), (3, 3, 0.5), "or", north=em)                       # médaillon / amulette
        if corps_mat == "peau" and fac not in ("sylvaneth", "nighthaunt"):
            # harnais de cuir en diagonale
            m.cube("body", (-0.5, lh + 2, -td / 2 - 0.5), (1, th * 0.95, 0.5), "cuir", rot=(0, 0, 32), pivot=(0, lh + th / 2, -td / 2))
            m.cube("body", (-0.5, lh + 2, td / 2), (1, th * 0.95, 0.5), "cuir", rot=(0, 0, -32), pivot=(0, lh + th / 2, td / 2))
    if "ventre" in ex:
        m.cube("body", (-tw / 2 + 1.5, lh + 0.5, -td / 2 - 3), (tw - 3, th - 5, 3), "ventre",
               north=lambda d, x, y, w, h, px: (d.ellipse((x + w // 2 - 1, y + h // 2, x + w // 2, y + h // 2 + 1), fill=mul(P["peau"], 0.5)),
                                                d.arc((x + 2, y + 2, x + w - 3, y + h - 3), 20, 160, fill=mul(P["peau"], 0.75))))
        if "plaque_ventre" in ex:
            m.cube("body", (-3.5, lh + 3, -td / 2 - 3.5), (7, 6, 0.5), "metal",
                   north=combine(f_cadre(mul(P["metal"], 0.7)), f_dents((240, 236, 220))))
    if "pustules" in ex:
        for (x, y, z) in ((-tw / 2 + 1, lh + 6, -td / 2 - 1), (tw / 2 - 3, lh + 3, -td / 2 - 1), (tw / 2 - 2, lh + 8, td / 2 - 1), (-2, lh + 9, td / 2)):
            m.cube("body", (x, y, z), (1.5, 1.5, 1.5), "lueur")
    if "cranes" in ex:
        for x in (-tw / 2 + 0.5, tw / 2 - 3):
            m.cube("body", (x, lh - 2.5, -td / 2 - 1.5), (2.5, 2.5, 2), "os", north=f_crane((226, 216, 190)))
    if "malepierre" in ex:
        m.cube("body", (tw / 2 - 2.5, lh - 2, -td / 2 - 1.5), (1.5, 2.5, 1.5), "malepierre", rot=(0, 0, 15), pivot=(tw / 2 - 2, lh, -td / 2))
    if "champignons" in ex:
        m.cube("body", (tw / 2 - 2, lh, -td / 2 - 1.5), (2, 1, 2), "lueur")
        m.cube("body", (tw / 2 - 1.5, lh - 1, -td / 2 - 1), (1, 1, 1), "blanc")
    if "mousse" in ex:
        m.cube("body", (-tw / 2 - 0.5, yt - 2.5, -td / 2 - 0.5), (tw / 2, 2, td + 1), "mousse")
        m.cube("body", (-1, lh + th / 2 - 1, -td / 2 - 0.6), (2, 2, 0.5), "lueur")
    if "cristaux" in ex:
        m.cube("body", (-0.75, yt - 3.5, -td / 2 - 1), (1.5, 2.5, 1), "lueur", rot=(0, 45, 0), pivot=(0, yt - 2, -td / 2 - 0.5))
    if "sac" in ex:      # moteur d'endrin des Kharadron
        m.cube("body", (-tw / 2 + 1.5, lh + 2, td / 2), (tw - 3, th - 3, 4), "metal", south=f_cadre(mul(P["metal"], 0.7)))
        m.cube("body", (-2, lh + th - 2, td / 2 + 1), (4, 4, 2.5), "lueur")
        for x in (-tw / 2 + 1, tw / 2 - 2):
            m.cube("body", (x, lh + 4, td / 2 + 4), (1, 7, 1), "or")
    if "queue" in ex:
        m.bone("tail", "body", (0, lh + 1, td / 2))
        for k, (w, h, d) in enumerate(((2.5, 2.5, 5), (2, 2, 5), (1.5, 1.5, 5), (1, 1, 4))):
            m.cube("tail", (-w / 2, lh - 0.5 - k * 0.8, td / 2 + k * 4.5), (w, h, d), "peau")
    if "cape" in ex:
        m.bone("cape", "body", (0, yt - 1, td / 2))
        tat = fac in ("nighthaunt", "soulblight", "fec", "skaven")
        m.cube("cape", (-tw / 2 + 1, yt - 5, td / 2 + 0.5), (tw - 2, 5, 0.5), "tissu", south=f_bande(A2, "haut"))
        m.cube("cape", (-tw / 2 + 0.5, max(1.5, lh - 7), td / 2 + 1), (tw - 1, yt - 5 - max(1.5, lh - 7), 0.5), "tissu",
               south=None if tat else f_bande(A2, "bas", 2), north=f_bande(mul(P["tissu"], 0.6), "bas", 2))
        if "col" in ex:
            m.cube("cape", (-tw / 2, yt - 1, td / 2), (tw, 6, 0.5), "tissu", rot=(-15, 0, 0), pivot=(0, yt, td / 2))
    if "ailes" in ex:
        plume = fac in ("stormcast", "lumineth", "khaine", "cites", "tzeentch")
        osw = fac in ("ossiarch",)
        for nomb, sx in (("wing_l", 1), ("wing_r", -1)):
            m.bone(nomb, "body", (sx * 2, yt - 2, td / 2 + 1))
            base_x = 0 if sx > 0 else -13
            if plume:
                for k, (L, y0) in enumerate(((13, yt - 4), (11, yt - 8), (8, yt - 12))):
                    m.cube(nomb, (sx * 2 + (0 if sx > 0 else -L), y0, td / 2 + 1 + k * 0.5), (L, 4, 0.5), "plume",
                           rot=(0, sx * -18, sx * 22), pivot=(sx * 2, yt - 2, td / 2 + 1))
                m.cube(nomb, (sx * 2 + (0 if sx > 0 else -13), yt - 1.5, td / 2 + 0.5), (13, 1.5, 1), "armure2",
                       rot=(0, sx * -18, sx * 22), pivot=(sx * 2, yt - 2, td / 2 + 1))
            else:
                mat = "os" if osw else "corne"
                m.cube(nomb, (sx * 2 + base_x * (sx < 0) * 0 + (0 if sx > 0 else -14), yt - 1, td / 2 + 1), (14, 1.5, 1.5), mat,
                       rot=(0, sx * -15, sx * 28), pivot=(sx * 2, yt - 2, td / 2 + 1))
                m.cube(nomb, (sx * 2 + (0 if sx > 0 else -13), yt - 12, td / 2 + 1.5), (13, 11, 0.5), "membrane" if not osw else "os",
                       rot=(0, sx * -15, sx * 28), pivot=(sx * 2, yt - 2, td / 2 + 1))

    # ---------------- épaulières
    if s.get("epaulieres"):
        pw, ph, pd = s["epaulieres"]
        for os_, sx in (("right_arm", -1), ("left_arm", 1)):
            x = sx * (tw / 2) - (pw - 1 if sx < 0 else -1 + 0)
            x = -tw / 2 - pw + 1 if sx < 0 else tw / 2 - 1
            y = yt - ph + 3
            m.cube(os_, (x, y + ph * 0.45, -pd / 2), (pw, ph * 0.55, pd), "armure", up=f_cadre(A2), toutes=f_bande(A2, "bas"))
            m.cube(os_, (x + (0.5 if sx < 0 else 0.5) - (0.5 if sx < 0 else 0), y, -pd / 2 + 0.5), (pw - 0.5, ph * 0.5, pd - 1), "armure",
                   toutes=f_bande(A2, "bas"))
            m.cube(os_, (x, y + ph * 0.45 - 0.5, -pd / 2 - 0.5), (pw, 0.5, pd + 1), "armure2")
            if "pointes" in ex or fac in ("orruks",):
                for k in range(2 if pw < 8 else 3):
                    zz = -pd / 2 + 1.5 + k * (pd - 3) / max(1, (2 if pw < 8 else 3) - 1)
                    m.cube(os_, (x + pw / 2 - 0.5, y + ph, zz - 0.5), (1, 3, 1), "corne" if fac != "orruks" else "metal",
                           rot=(0, 0, sx * 20), pivot=(x + pw / 2, y + ph, zz))
            if "cranes" in ex:
                m.cube(os_, (x + pw / 2 - 1.25, y + ph * 0.2, -pd / 2 - 1.5), (2.5, 2.5, 1.5), "os", north=f_crane((226, 216, 190)))
            if "os" in ex and arm:
                m.cube(os_, (x + pw / 2 - 0.5, y + ph, -1), (1, 3.5, 1), "os", rot=(0, 0, sx * 25), pivot=(x + pw / 2, y + ph, 0))
            if "rayures" in ex:
                m.cube(os_, (x, y + ph * 0.45, -pd / 2 - 0.5), (pw, ph * 0.55, 0.5), "armure2",
                       north=f_rayures((20, 20, 20), A2))
            if "laurier" in ex:
                m.cube(os_, (x + 0.5, y + ph - 0.5, -pd / 2 + 1), (pw - 1, 0.5, pd - 2), "lueur" if False else "armure2",
                       up=f_comete(mul(A2, 1.2)))
    # ---------------- bras
    for os_, x, sx in (("right_arm", -tw / 2 - aw, -1), ("left_arm", tw / 2, 1)):
        m.cube(os_, (x, yt - ah + 2, -ad / 2), (aw, ah - 2, ad), mb)
        m.cube(os_, (x + 0.25, yt - ah, -ad / 2 + 0.25), (aw - 0.5, 2, ad - 0.5), "peau" if not arm and fac not in ("kharadron",) else "armure2")  # main
        hg = ah * 0.42
        m.cube(os_, (x - 0.5, yt - ah + 1.5, -ad / 2 - 0.5), (aw + 1, hg, ad + 1), "armure2" if arm else "cuir",
               north=f_bande(mul(A2, 0.75) if arm else (60, 40, 28), "haut"))
        if arm:
            m.cube(os_, (x + aw / 2 - 1 + (0 if sx < 0 else 0), yt - ah * 0.45, ad / 2 - 0.5), (2, 1.5, 1), "armure2")  # coude
        if "griffes" in ex:
            for k in range(3):
                m.cube(os_, (x + 0.5 + k * (aw - 1) / 2.5, yt - ah - 2.5, -ad / 2 - 0.5), (0.5, 3, 0.5), "corne",
                       rot=(-25, 0, 0), pivot=(x + aw / 2, yt - ah, -ad / 2))

    # ---------------- tête
    face = s.get("face", "visage")
    casque = st.get("casque") if face == "heaume" else None
    tm = "armure" if face == "heaume" else ("tissu" if face == "capuche" else "peau")
    fn_face = {
        "visage": f_visage(P["peau"]),
        "bete": combine(f_yeux(LU, (12, 12, 14), 0.38, 0.25)),
        "crane": combine(f_yeux(LU, (12, 12, 14), 0.4, 0.22), f_dents((236, 232, 210)) if False else None),
        "capuche": lambda d, x, y, w, h, px: (d.rectangle((x + 2, y + 3, x + w - 3, y + h - 1), fill=(10, 10, 14)),
                                              f_yeux(LU, None, 0.5, 0.2)(d, x, y, w, h, px)),
        "heaume": f_fente_t((14, 14, 18), None),
    }[face]
    m.cube("head", (hx, yt, hx), (hs, hs, hs), tm, north=fn_face)
    if face == "crane":
        m.cube("head", (hx + 1, yt - 1.5, hx - 0.5), (hs - 2, 2, hs - 2), "os", north=f_dents((40, 36, 30)))    # mâchoire
        m.cube("head", (hx - 0.5, yt + 2.5, hx + 1), (0.5, 1.5, 2), "os")
        m.cube("head", (-hx, yt + 2.5, hx + 1), (0.5, 1.5, 2), "os")
    if face == "visage":
        m.cube("head", (-0.75, yt + hs * 0.35, hx - 0.75), (1.5, 1.5, 0.75), "peau")                          # nez
        if fac not in ("ossiarch",) and "barbe" not in ex:
            m.cube("head", (hx - 0.25, yt + hs - 2, hx + 1), (hs + 0.5, 2.5, hs - 0.5), "poils")                # cheveux
            m.cube("head", (hx - 0.25, yt + 2, -hx - 1.5), (hs + 0.5, hs - 2, 1.75), "poils")
        if corps == "fin":      # oreilles pointues des aelfes
            m.cube("head", (hx - 1.5, yt + hs * 0.45, -0.5), (1.5, 1, 1), "peau", rot=(0, 0, -25), pivot=(hx, yt + hs * 0.5, 0))
            m.cube("head", (-hx, yt + hs * 0.45, -0.5), (1.5, 1, 1), "peau", rot=(0, 0, 25), pivot=(-hx, yt + hs * 0.5, 0))
    if face == "capuche":
        m.cube("head", (hx - 0.5, yt - 0.5, hx - 0.5), (hs + 1, hs + 1, 1), "tissu",
               north=lambda d, x, y, w, h, px: d.rectangle((x + 3, y + 3, x + w - 4, y + h - 1), fill=(0, 0, 0, 0)))
        m.cube("head", (-1, yt + hs, -hx - 2.5), (2, 2, 3), "tissu")                                         # pointe de capuche
        m.cube("head", (hx - 1, yt - 2, hx), (hs + 2, 2.5, hs + 1), "tissu")                                 # pèlerine
    if face == "bete":
        if fac in ("skaven",) or "museau" in ex:
            long_ = 4 if fac == "skaven" else 3.5
            m.cube("head", (-2, yt + 0.5, hx - long_), (4, 3, long_), "peau", north=f_dents())
            m.cube("head", (-1, yt + 1.5, hx - long_ - 1.5), (2, 1.5, 1.5), "peau" if fac != "skaven" else "sombre")
            if fac == "skaven":
                for sx in (-1, 1):
                    m.cube("head", (sx * 2.5 - 1, yt + hs - 1, -1), (2, 2.5, 0.5), "peau", rot=(0, 0, sx * 15), pivot=(sx * 2.5, yt + hs, -1))
        elif fac in ("orruks",) or "machoire" in ex:
            m.cube("head", (hx - 0.5, yt - 1.5, hx - 1.5), (hs + 1, 3, hs - 1), "peau", north=f_dents())
            for sx in (-1, 1):
                m.cube("head", (sx * (hs / 2 - 1.5) - 0.5, yt + 1, hx - 2), (1, 2, 1), "dent")                # défenses
                m.cube("head", (sx * hs / 2 - (2 if sx < 0 else 0), yt + hs * 0.55, -0.5), (2, 1, 1), "peau",
                       rot=(0, 0, sx * 30), pivot=(sx * hs / 2, yt + hs * 0.6, 0))                              # oreilles
        else:
            m.cube("head", (-hs / 2 + 1, yt, hx - 2.5), (hs - 2, hs / 2, 2.5), "peau", north=f_dents())
    if "barbe" in ex:
        m.cube("head", (hx + 0.5, yt - 4, hx - 1), (hs - 1, 5, 2), "poils")
        m.cube("head", (-1.5, yt - 6.5, hx - 0.8), (3, 3, 1.5), "poils")
        if fac in ("fyreslayers", "kharadron"):
            m.cube("head", (-0.5, yt - 7, hx - 0.9), (1, 1, 1), "or")
    if "crete" in ex:
        m.cube("head", (-1, yt + hs, hx + 0.5), (2, 3.5, hs - 1), "poils")
        m.cube("head", (-0.75, yt + hs + 3, hx + 1.5), (1.5, 1.5, hs - 3), "poils")
    # casques de faction
    if casque == "sc":
        m.cube("head", (-0.75, yt + hs, hx + 0.5), (1.5, 1.5, hs - 1), "armure2")
        for sx in (-1, 1):
            m.cube("head", (sx * hs / 2 - (0.5 if sx < 0 else 0), yt + 1, hx + 1), (0.5, hs - 2, hs - 2), "armure", toutes=f_bande(A2, "bas"))
    elif casque == "chaos":
        m.cube("head", (hx - 0.5, yt + hs - 1.5, hx - 0.5), (hs + 1, 1.5, hs + 1), "armure2")
    elif casque == "khorne":
        m.cube("head", (-1.5, yt + hs * 0.4, hx - 1), (3, 3, 1), "os", north=f_crane((226, 216, 190)))
    elif casque == "khar":
        m.cube("head", (hx - 0.5, yt - 0.5, hx - 0.5), (hs + 1, hs + 1, 1), "armure",
               north=lambda d, x, y, w, h, px: (d.ellipse((x + 3, y + 3, x + w - 4, y + h - 5), fill=mul(LU, 0.6)),
                                                d.ellipse((x + 4, y + 4, x + w - 6, y + h - 7), fill=LU)))
        for sx in (-1, 1):
            m.cube("head", (sx * (hs / 2 + 0.5) - 0.5, yt + 1, -1), (1, 1, hs / 2 + 2), "or")                      # tuyaux
    elif casque == "lum":
        m.cube("head", (-0.75, yt + hs, hx), (1.5, 6, 2.5), "armure2", rot=(-12, 0, 0), pivot=(0, yt + hs, hx))
        for sx in (-1, 1):
            m.cube("head", (sx * hs / 2 - (2.5 if sx < 0 else 0), yt + hs - 2, 0), (2.5, 4, 0.5), "armure2",
                   rot=(0, 0, sx * 25), pivot=(sx * hs / 2, yt + hs - 2, 0))
    elif casque == "morion":
        m.cube("head", (hx - 1.5, yt + hs - 1.5, hx - 1.5), (hs + 3, 0.5, hs + 3), "metal")
        m.cube("head", (-0.5, yt + hs, hx + 1), (1, 1.5, hs - 2), "metal")
    elif casque == "orruk":
        m.cube("head", (hx - 0.5, yt + hs - 3, hx - 0.5), (hs + 1, 3, hs + 1), "armure", north=f_rayures((20, 20, 20), A2))
    elif casque == "nurgle":
        m.cube("head", (-0.75, yt + hs * 0.5, hx - 3), (1.5, 1.5, 3.5), "corne", rot=(-30, 0, 0), pivot=(0, yt + hs * 0.5, hx))
    elif casque == "ossi":
        for sx in (-1, 1):
            m.cube("head", (sx * hs / 2 - (1 if sx < 0 else 0), yt + hs - 1, -1), (1, 4, 1), "os", rot=(0, 0, sx * 20), pivot=(sx * hs / 2, yt + hs, 0))
    elif casque == "sb":
        m.cube("head", (hx - 0.5, yt + hs - 1, hx - 0.5), (hs + 1, 1, hs + 1), "armure2")
        m.cube("head", (-0.5, yt + hs, hx), (1, 3, 1), "armure2")
    elif casque == "hashut":
        m.cube("head", (hx + 0.5, yt + hs, hx + 0.5), (hs - 1, 4, hs - 1), "armure", toutes=f_runes(LU))
    elif casque == "idoneth":
        m.cube("head", (-0.5, yt + hs, hx), (1, 2.5, hs + 2), "armure2", rot=(10, 0, 0), pivot=(0, yt + hs, 0))
    elif casque == "slaanesh":
        m.cube("head", (-1, yt + hs, hx + 1), (2, 4, 2), "poils")
    elif casque == "skaven":
        pass
    # cornes, couronne, halo, haut heaume
    if "cornes" in ex or "grandes_cornes" in ex:
        g = "grandes_cornes" in ex
        # cornes en escalier : vers l'extérieur puis vers le haut, puis pointe recourbée
        segs = ([(0, 0, 2.5, 2.5), (2, 1.5, 2.2, 3), (3.4, 4, 1.8, 3.5), (3.6, 7.2, 1.3, 2.5), (3.0, 9.4, 1, 1.8)] if g
                else [(0, 0, 1.8, 2), (1.3, 1.4, 1.5, 2.2), (1.8, 3.4, 1.1, 1.8)])
        for sx in (-1, 1):
            for dx, dy, w, h in segs:
                x = sx * (hs / 2 + dx) - (w if sx < 0 else 0)
                m.cube("head", (x, yt + hs - 3 + dy, -w / 2), (w, h, w), "corne")
    if "couronne" in ex:
        m.cube("head", (hx - 0.25, yt + hs - 0.5, hx - 0.25), (hs + 0.5, 1, hs + 0.5), "or")
        for k in range(4):
            xx = hx + 0.25 + k * (hs - 1.5) / 3
            m.cube("head", (xx, yt + hs + 0.5, hx - 0.25), (1, 2 + (k % 2), 0.5), "or")
    if "haut_heaume" in ex:
        m.cube("head", (-1, yt + hs, hx), (2, 4.5, 3), "armure2", rot=(-10, 0, 0), pivot=(0, yt + hs, hx))
    if "plumet" in ex:
        m.cube("head", (-1, yt + hs + 1, -1), (2, 4, 2), "tissu", rot=(-20, 0, 0), pivot=(0, yt + hs, 0))
    if "halo" in ex:
        m.cube("head", (-7, yt - 2, -hx + 1.5), (14, 14, 0), "or", north=f_anneau(mul(A2, 1.0) if False else (232, 196, 90)),
               south=f_anneau((232, 196, 90)))
    if "branches" in ex:
        for sx, h in ((-1, 7), (1, 8)):
            m.cube("head", (sx * hs / 2 - 1, yt + hs - 1, -1), (2, h, 2), "bois", rot=(0, 0, sx * 18), pivot=(sx * hs / 2, yt + hs, 0))
            m.cube("head", (sx * hs / 2 + sx * 2.5 - 0.75, yt + hs + h * 0.55, -0.75), (1.5, 4, 1.5), "bois", rot=(0, 0, sx * 50),
                   pivot=(sx * hs / 2 + sx * 2.5, yt + hs + h * 0.55, 0))
        m.cube("head", (-0.75, yt + hs, 0.5), (1.5, 5, 1.5), "bois")
        m.cube("head", (-1, yt + hs * 0.55, hx - 0.6), (2, 1, 0.5), "lueur")
    if "chapeau" in ex:     # capuche pointue des Gitz, avec la lune
        m.cube("head", (hx - 1, yt + hs - 3, hx - 1), (hs + 2, 3.5, hs + 2), "tissu",
               north=lambda d, x, y, w, h, px: d.ellipse((x + w // 2 - 2, y + 1, x + w // 2 + 1, y + 4), fill=(232, 224, 130)))
        m.cube("head", (-2.5, yt + hs, -2), (5, 4, 5), "tissu", rot=(-12, 0, 0), pivot=(0, yt + hs, 0))
        m.cube("head", (-1.5, yt + hs + 3.5, 0), (3, 3, 3), "tissu", rot=(-28, 0, 0), pivot=(0, yt + hs + 3, 0))
        m.cube("head", (-0.5, yt + hs + 6, 2), (1, 2.5, 1), "tissu", rot=(-45, 0, 0), pivot=(0, yt + hs + 6, 2))
    if "nageoires" in ex and face != "heaume":
        for sx in (-1, 1):
            m.cube("head", (sx * hs / 2 - (0.5 if sx < 0 else 0), yt + 2, -1), (0.5, 3, 3), "membrane")

    # ---------------- armes
    hxw = -tw / 2 - aw / 2
    yh = yt - ah
    zf = -ad / 2 - 1.5
    a = s.get("arme")
    W = "weapon"
    if a == "marteau":
        m.cube(W, (hxw - 0.75, yh - 9, zf - 0.75), (1.5, 18, 1.5), "manche",
               toutes=lambda d, x, y, w, h, px: [d.line((x, y + k, x + w - 1, y + k + 1), fill=(150, 40, 40)) for k in range(6, h - 6, 3)])
        m.cube(W, (hxw - 1, yh - 10.5, zf - 1), (2, 1.5, 2), "metal")
        m.cube(W, (hxw - 3.5, yh + 7, zf - 2.5), (7, 4.5, 4.5), "metal", toutes=f_cadre(mul(P["metal"], 0.7)))
        for sx in (-1, 1):
            m.cube(W, (hxw + (3.5 if sx > 0 else -4), yh + 6.5, zf - 3), (0.5, 5.5, 5.5), "armure2",
                   east=f_eclair(LU), west=f_eclair(LU))
        m.cube(W, (hxw - 0.75, yh + 11.5, zf - 0.75), (1.5, 2, 1.5), "armure2")
    elif a in ("hache", "double_hache"):
        m.cube(W, (hxw - 0.75, yh - 8, zf - 0.75), (1.5, 18 if a == "hache" else 20, 1.5), "manche")
        cotes = (-1,) if a == "hache" else (-1, 1)
        for sx in cotes:
            bx = hxw + (0.75 if sx > 0 else -0.75)
            for k, (w, h, dy) in enumerate(((2, 7, 0), (2, 5.5, 0.75), (1.5, 3.5, 1.75))):
                x = bx + (sum(v[0] for v in ((2, 7, 0), (2, 5.5, 0.75), (1.5, 3.5, 1.75))[:k])) * sx
                m.cube(W, (x if sx > 0 else x - w, yh + 3.5 + dy, zf - 0.25), (w, h, 0.5), "lame" if k == 2 else "metal",
                       north=f_bande((240, 244, 250), "bas") if k == 2 else None)
        m.cube(W, (hxw - 1, yh + 10, zf - 1), (2, 1.5, 2), "armure2")
    elif a == "epee":
        m.cube(W, (hxw - 0.5, yh - 2.5, zf - 0.5), (1, 3.5, 1), "cuir")
        m.cube(W, (hxw - 0.75, yh - 3.5, zf - 0.75), (1.5, 1, 1.5), "armure2")
        m.cube(W, (hxw - 3, yh + 1, zf - 1), (6, 1, 2), "armure2")
        m.cube(W, (hxw - 1, yh + 2, zf - 0.25), (2, 14, 0.5), "lame",
               north=lambda d, x, y, w, h, px: d.line((x + w // 2, y, x + w // 2, y + h - 3), fill=(150, 156, 168)))
        m.cube(W, (hxw - 0.5, yh + 16, zf - 0.25), (1, 2, 0.5), "lame")
    elif a == "lance":
        m.cube(W, (hxw - 0.5, yh - 12, zf - 0.5), (1, 29, 1), "manche")
        m.cube(W, (hxw - 1.25, yh + 16, zf - 0.25), (2.5, 4, 0.5), "lame", north=f_bande((150, 156, 168), "bas"))
        m.cube(W, (hxw - 0.75, yh + 20, zf - 0.25), (1.5, 2, 0.5), "lame")
        m.cube(W, (hxw - 1.5, yh + 15.5, zf - 0.5), (3, 0.5, 1), "armure2")
        m.cube(W, (hxw + 0.5, yh + 11, zf), (0.5, 4, 3), "tissu", east=f_bande(A2, "bas"), west=f_bande(A2, "bas"))
    elif a == "faux":
        m.cube(W, (hxw - 0.75, yh - 10, zf - 0.75), (1.5, 26, 1.5), "manche")
        for k, (x, y, w) in enumerate(((0, 0, 4), (4, -0.8, 3.5), (7.5, -2, 3), (10.5, -3.8, 2))):
            m.cube(W, (hxw - x - w, yh + 14 + y, zf - 0.25), (w, 2.5 - k * 0.4, 0.5), "lame", north=f_bande((240, 244, 250), "bas"))
        m.cube(W, (hxw - 1, yh + 15.5, zf - 1), (2, 1.5, 2), "armure2")
    elif a == "couperet":
        m.cube(W, (hxw - 0.75, yh - 2.5, zf - 0.75), (1.5, 4, 1.5), "cuir")
        m.cube(W, (hxw - 0.5, yh + 1.5, zf - 4), (1, 11, 6.5), "metal",
               east=combine(f_cadre(mul(P["metal"], 0.65)), f_rayures((20, 20, 20), A2) if fac == "orruks" else None),
               west=f_cadre(mul(P["metal"], 0.65)))
        m.cube(W, (hxw - 0.25, yh + 1.5, zf - 4.5), (0.5, 11, 0.5), "lame")
    elif a == "baton":
        m.cube(W, (hxw - 0.75, yh - 12, zf - 0.75), (1.5, 26, 1.5), "manche")
        m.cube(W, (hxw - 1.5, yh + 13.5, zf - 1.5), (3, 3, 3), "lueur")
        for sx, sz in ((-1, -1), (1, -1), (-1, 1), (1, 1)):
            m.cube(W, (hxw + sx * 1.75 - 0.25, yh + 12.5, zf + sz * 1.75 - 0.25), (0.5, 5, 0.5), "or")
        m.cube(W, (hxw - 2, yh + 12, zf - 2), (4, 0.75, 4), "or")
        if fac in ("soulblight",):
            m.cube(W, (hxw - 1.5, yh + 17, zf - 1.5), (3, 3, 3), "os", north=f_crane((226, 216, 190), LU))
    elif a == "fusil":
        m.cube(W, (hxw - 1, yh - 3, zf + 1), (2, 3, 4), "bois")
        m.cube(W, (hxw - 1, yh - 1.5, zf - 12), (2, 2, 14), "metal", up=f_bande(mul(P["metal"], 0.6), "haut"))
        m.cube(W, (hxw - 1.25, yh - 1.75, zf - 13), (2.5, 2.5, 1.5), "armure2")
        m.cube(W, (hxw - 0.75, yh + 0.5, zf - 5), (1.5, 1.5, 3), "lueur" if fac in ("skaven", "kharadron", "stormcast", "idoneth") else "metal")
    elif a == "dague":
        m.cube(W, (hxw - 0.5, yh - 1.5, zf - 0.5), (1, 2.5, 1), "cuir")
        m.cube(W, (hxw - 1.5, yh + 0.5, zf - 0.75), (3, 0.75, 1.5), "armure2")
        m.cube(W, (hxw - 0.75, yh + 1.25, zf - 0.25), (1.5, 7, 0.5), "lame")
    elif a == "massue":
        m.cube(W, (hxw - 1, yh - 5, zf - 1), (2, 12, 2), "manche" if fac not in ("behemat",) else "bois")
        m.cube(W, (hxw - 3, yh + 6, zf - 3), (6, 7, 6), "pierre" if fac in ("seraphon",) else ("bois" if fac in ("behemat", "gitz", "orruks", "ogors") else "metal"))
        for (x, y, z) in ((-3.5, 9, -1), (2.5, 8, -1), (-1, 12.5, -1), (-1, 9, -3.5)):
            m.cube(W, (hxw + x, yh + y, zf + z), (1, 1, 1), "metal" if fac in ("behemat", "gitz", "orruks", "ogors") else "or")

    # ---------------- main gauche
    oxw = tw / 2 + aw
    off = s.get("main_gauche")
    if off == "bouclier":
        emb_b = f_eclair((226, 230, 236)) if fac == "stormcast" else (em or f_cadre(A2))
        m.cube("offhand", (oxw, yh - 4, -7), (1.5, 15, 14), "bouclier", west=combine(emb_b))
        m.cube("offhand", (oxw + 1.5, yh - 4.5, -7.5), (0.5, 16, 0.75), "armure2")
        m.cube("offhand", (oxw + 1.5, yh - 4.5, 6.75), (0.5, 16, 0.75), "armure2")
        m.cube("offhand", (oxw + 1.5, yh + 10.75, -7), (0.5, 0.75, 14), "armure2")
        m.cube("offhand", (oxw + 1.5, yh - 4.5, -7), (0.5, 0.75, 14), "armure2")
        m.cube("offhand", (oxw + 1.5, yh + 2.25, -1.25), (1, 2.5, 2.5), "armure2")
    elif off == "rondache":
        m.cube("offhand", (oxw, yh - 1, -4), (1.5, 8, 8), "bouclier", west=f_cadre(A2))
        m.cube("offhand", (oxw, yh + 0.5, -5), (1.5, 5, 10), "bouclier")
        m.cube("offhand", (oxw + 1.5, yh + 2, -1), (1, 2, 2), "armure2")
    elif off == "dague":
        m.cube("offhand", (oxw - aw / 2 - 0.5, yh - 1.5, zf - 0.5), (1, 2.5, 1), "cuir")
        m.cube("offhand", (oxw - aw / 2 - 0.75, yh + 1, zf - 0.25), (1.5, 7, 0.5), "lame")
    elif off == "hache":
        m.cube("offhand", (oxw - aw / 2 - 0.75, yh - 8, zf - 0.75), (1.5, 18, 1.5), "manche")
        m.cube("offhand", (oxw - aw / 2 + 0.75, yh + 3.5, zf - 0.25), (4, 6, 0.5), "metal", north=f_bande((240, 244, 250), "bas"))
    elif off == "griffe":
        for k in range(3):
            m.cube("offhand", (oxw - aw + 0.3 + k * (aw - 1) / 2.5, yh - 3, -ad / 2 - 1), (0.6, 3.5, 0.6), "corne",
                   rot=(-20, 0, 0), pivot=(oxw - aw / 2, yh, -ad / 2))
    return m, mats
