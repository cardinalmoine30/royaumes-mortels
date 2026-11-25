# -*- coding: utf-8 -*-
"""Skins 64x64 (modèle classique) des 25 factions jouables, d'après les schémas officiels de couleurs.
Sortie : assets/royaumes/textures/skin/<faction>.png + apercus/planche_skins.png (face et dos)."""
import os
import random
from PIL import Image, ImageDraw, ImageFont

ICI = os.path.dirname(os.path.abspath(__file__))
SORTIE = os.path.join(ICI, "..", "..", "src", "main", "resources", "assets", "royaumes", "textures", "skin")
BAS = os.path.join(ICI, "bas")  # skins 64×64 d'origine (le mod reçoit la version HD de outils/remaster.py)
PARTS = {"head": (0, 0, 8, 8, 8), "hat": (32, 0, 8, 8, 8),
         "body": (16, 16, 8, 12, 4), "jacket": (16, 32, 8, 12, 4),
         "rarm": (40, 16, 4, 12, 4), "rsleeve": (40, 32, 4, 12, 4),
         "larm": (32, 48, 4, 12, 4), "lsleeve": (48, 48, 4, 12, 4),
         "rleg": (0, 16, 4, 12, 4), "rpants": (0, 32, 4, 12, 4),
         "lleg": (16, 48, 4, 12, 4), "lpants": (0, 48, 4, 12, 4)}
COTES = ("right", "front", "left", "back")


def faces(part):
    u, v, w, h, d = PARTS[part]
    return {"top": (u + d, v, w, d), "bottom": (u + d + w, v, w, d), "right": (u, v + d, d, h),
            "front": (u + d, v + d, w, h), "left": (u + d + w, v + d, d, h), "back": (u + d + w + d, v + d, w, h)}


def cl(v):
    return max(0, min(255, int(v)))


def mul(c, k):
    return tuple(cl(x * k) for x in c[:3])


class Skin:
    def __init__(self, graine):
        self.im = Image.new("RGBA", (64, 64), (0, 0, 0, 0))
        self.p = self.im.load()
        self.r = random.Random(graine)

    # -- primitives
    def pt(self, part, face, x, y, c, a=255):
        fx, fy, fw, fh = faces(part)[face]
        if 0 <= x < fw and 0 <= y < fh:
            self.p[fx + x, fy + y] = tuple(c[:3]) + (a,)

    def rect(self, part, face, x, y, w, h, c, bruit=0):
        for j in range(h):
            for i in range(w):
                n = self.r.randint(-bruit, bruit) if bruit else 0
                self.pt(part, face, x + i, y + j, tuple(cl(v + n) for v in c))

    def remplir(self, part, c, bruit=5, faces_=None, ombre=True):
        for f, (fx, fy, fw, fh) in faces(part).items():
            if faces_ and f not in faces_:
                continue
            k = {"top": 1.1, "bottom": 0.7, "right": 0.9, "left": 0.9, "back": 0.85, "front": 1.0}[f] if ombre else 1
            for j in range(fh):
                for i in range(fw):
                    g = 1.04 - 0.08 * j / max(1, fh - 1) if f not in ("top", "bottom") else 1
                    n = self.r.randint(-bruit, bruit)
                    self.p[fx + i, fy + j] = tuple(cl(v * k * g + n) for v in c) + (255,)

    def bande(self, part, y0, y1, c, bruit=4, cotes=COTES):
        for f in cotes:
            fx, fy, fw, fh = faces(part)[f]
            k = 0.9 if f in ("right", "left") else (0.85 if f == "back" else 1)
            for j in range(y0, min(y1, fh)):
                for i in range(fw):
                    self.p[fx + i, fy + j] = tuple(cl(v * k + self.r.randint(-bruit, bruit)) for v in c) + (255,)

    def colonne(self, part, face, x, y0, y1, c):
        for y in range(y0, y1):
            self.pt(part, face, x, y, c)

    def cadre(self, part, face, c, haut=True, bas=True, cote=True):
        fx, fy, fw, fh = faces(part)[face]
        for i in range(fw):
            if haut:
                self.pt(part, face, i, 0, c)
            if bas:
                self.pt(part, face, i, fh - 1, c)
        if cote:
            for j in range(fh):
                self.pt(part, face, 0, j, c)
                self.pt(part, face, fw - 1, j, c)

    def vider(self, part):
        for f, (fx, fy, fw, fh) in faces(part).items():
            for j in range(fh):
                for i in range(fw):
                    self.p[fx + i, fy + j] = (0, 0, 0, 0)


# ------------------------------------------------------------------ pièces communes
def corps_armure(s, A, T, emb=None):
    s.remplir("body", A)
    for f in COTES:
        s.cadre("body", f, mul(A, 0.65), haut=False, cote=False)
    s.rect("body", "front", 0, 0, 8, 1, T)
    s.rect("body", "front", 1, 1, 6, 4, mul(A, 1.08), bruit=3)               # plastron bombé
    s.rect("body", "front", 2, 1, 4, 1, mul(A, 1.25))
    s.bande("body", 7, 8, T)                                                # ceinture
    s.rect("body", "front", 3, 7, 2, 1, mul(T, 1.2))
    for f in COTES:
        s.colonne("body", f, 0, 0, 12, mul(A, 0.7))
    if emb:
        emb(s)


def bras_armure(s, A, T, main, epaul=None):
    for b in ("rarm", "larm"):
        s.remplir(b, A)
        s.bande(b, 5, 6, T)
        s.bande(b, 10, 12, main)
        s.bande(b, 9, 10, mul(A, 0.75))
    if epaul:
        for b in ("rsleeve", "lsleeve"):
            s.remplir(b, epaul, faces_=("top", "right", "front", "left", "back"))
            for f in COTES:
                fx, fy, fw, fh = faces(b)[f]
                for j in range(4, fh):
                    for i in range(fw):
                        s.p[fx + i, fy + j] = (0, 0, 0, 0)
                s.rect(b, f, 0, 3, 4, 1, mul(epaul, 0.65))
            s.bande(b, 0, 1, mul(epaul, 1.2))


def jambes_armure(s, A, T, bottes):
    for b in ("rleg", "lleg"):
        s.remplir(b, A)
        s.bande(b, 4, 5, mul(A, 0.7))
        s.bande(b, 5, 6, T)
        s.bande(b, 9, 12, bottes)
        s.bande(b, 9, 10, mul(bottes, 1.15))


def tabard(s, c, bord, emb=None, dos=True):
    s.rect("jacket", "front", 2, 6, 4, 6, c, bruit=3)
    for j in range(6, 12):
        s.pt("jacket", "front", 2, j, bord)
        s.pt("jacket", "front", 5, j, bord)
    for b, cote in (("rpants", "front"), ("lpants", "front")):
        pass
    for b in ("rpants", "lpants"):
        fx, fy, fw, fh = faces(b)["front"]
        for j in range(0, 6):
            for i in range(fw):
                x = i if b == "lpants" else i
                if (b == "rpants" and i >= 2) or (b == "lpants" and i <= 1):
                    s.pt(b, "front", i, j, mul(c, 0.96 - 0.03 * j))
        for i in range(fw):
            if (b == "rpants" and i >= 2) or (b == "lpants" and i <= 1):
                s.pt(b, "front", i, 6, bord)
    if dos:
        s.rect("jacket", "back", 1, 2, 6, 10, mul(c, 0.85), bruit=3)
        for b in ("rpants", "lpants"):
            s.rect(b, "back", 0, 0, 4, 7, mul(c, 0.8), bruit=3)
            s.rect(b, "back", 0, 7, 4, 1, bord)
    if emb:
        emb(s)


def cape(s, c, bord):
    s.rect("jacket", "back", 0, 0, 8, 12, c, bruit=4)
    s.rect("jacket", "back", 0, 11, 8, 1, bord)
    s.rect("jacket", "top", 0, 3, 8, 1, c)
    for b in ("rpants", "lpants"):
        s.rect(b, "back", 0, 0, 4, 5, mul(c, 0.92), bruit=4)
        s.rect(b, "back", 0, 5, 4, 1, bord)


def peau_tete(s, P, yeux=(60, 40, 30), bouche=None, nez=True):
    s.remplir("head", P, bruit=3)
    s.rect("head", "front", 2, 4, 1, 1, (255, 255, 255))
    s.rect("head", "front", 5, 4, 1, 1, (255, 255, 255))
    s.rect("head", "front", 1, 4, 1, 1, yeux)
    s.rect("head", "front", 6, 4, 1, 1, yeux)
    s.rect("head", "front", 1, 3, 2, 1, mul(P, 0.75))
    s.rect("head", "front", 5, 3, 2, 1, mul(P, 0.75))
    if nez:
        s.rect("head", "front", 3, 5, 2, 1, mul(P, 0.85))
    s.rect("head", "front", 3, 6, 2, 1, bouche or mul(P, 0.6))


def cheveux(s, c, long=False, crete=False):
    s.rect("head", "top", 0, 0, 8, 8, c, bruit=6)
    s.rect("head", "front", 0, 0, 8, 2, c, bruit=6)
    for f in ("right", "left", "back"):
        s.rect("head", f, 0, 0, 8, 8 if (long or f == "back") else 4, c, bruit=6)
    if long:
        s.rect("hat", "back", 0, 0, 8, 8, mul(c, 1.05), bruit=8)
        s.rect("jacket", "back", 1, 0, 6, 5, c, bruit=8)
    if crete:
        s.rect("hat", "top", 3, 0, 2, 8, crete, bruit=8)
        s.rect("hat", "front", 3, 0, 2, 2, crete)
        s.rect("hat", "back", 3, 0, 2, 4, crete)


def barbe(s, c, longue=True):
    s.rect("head", "front", 0, 5, 8, 3, c, bruit=6)
    s.rect("head", "front", 3, 6, 2, 1, mul(c, 0.6))
    for f in ("right", "left"):
        s.rect("head", f, 0, 5, 8, 3, c, bruit=6) if f == "left" else s.rect("head", f, 0, 5, 8, 3, c, bruit=6)
    if longue:
        s.rect("jacket", "front", 1, 0, 6, 5, c, bruit=8)
        s.rect("jacket", "front", 2, 5, 4, 2, mul(c, 0.9), bruit=8)
        s.rect("hat", "front", 0, 5, 8, 3, c, bruit=8)


def comete(s, part, face, x, y, c):
    for (dx, dy) in ((1, 0), (0, 1), (1, 1), (2, 1), (1, 2), (2, 2), (3, 3)):
        s.pt(part, face, x + dx, y + dy, c)


# ------------------------------------------------------------------ factions
def stormcast(s):
    G, B, BL, R = (212, 166, 58), (40, 74, 150), (230, 232, 240), (200, 30, 40)
    s.remplir("head", G)
    s.rect("head", "front", 1, 3, 6, 1, (24, 22, 26))                    # fente du masque
    s.rect("head", "front", 3, 3, 2, 4, (24, 22, 26))
    s.rect("head", "front", 2, 1, 4, 1, mul(G, 1.25))
    s.rect("head", "front", 3, 0, 2, 1, R)                                # gemme rouge
    s.rect("hat", "top", 3, 0, 2, 8, B, bruit=4)                          # crête bleue
    s.rect("hat", "front", 3, 0, 2, 1, B)
    s.rect("hat", "back", 3, 0, 2, 3, B)
    for f in ("right", "left"):
        s.rect("head", f, 2, 2, 4, 3, mul(G, 0.8))                        # ailes du heaume
        s.rect("head", f, 3, 3, 2, 1, mul(G, 1.2))
    corps_armure(s, G, BL, lambda s: comete(s, "body", "front", 2, 1, BL))
    bras_armure(s, G, BL, G, epaul=B)
    jambes_armure(s, G, BL, mul(G, 0.9))
    tabard(s, B, BL, emb=lambda s: s.rect("jacket", "front", 3, 8, 2, 2, G))
    cape(s, B, BL)


def cites(s):
    A, T, R, C, P = (152, 154, 162), (200, 190, 160), (184, 64, 40), (232, 214, 172), (215, 172, 136)
    peau_tete(s, P)
    barbe(s, (110, 70, 40), longue=False)
    s.rect("head", "top", 0, 0, 8, 8, A)                                   # morion
    s.rect("head", "front", 0, 0, 8, 2, A)
    for f in ("right", "left", "back"):
        s.rect("head", f, 0, 0, 8, 2, A)
    s.rect("hat", "front", 0, 2, 8, 1, mul(A, 1.1))
    s.rect("hat", "right", 0, 2, 8, 1, mul(A, 1.1))
    s.rect("hat", "left", 0, 2, 8, 1, mul(A, 1.1))
    s.rect("hat", "back", 0, 2, 8, 1, mul(A, 1.1))
    s.rect("hat", "top", 3, 0, 2, 8, mul(A, 1.2))
    s.remplir("body", R)
    s.rect("body", "front", 1, 0, 6, 6, A, bruit=4)                       # cuirasse
    s.rect("body", "front", 3, 2, 2, 2, C)
    s.bande("body", 7, 8, (80, 50, 30))
    for b in ("rarm", "larm"):
        s.remplir(b, R)
        s.bande(b, 0, 4, A)
        s.bande(b, 10, 12, (90, 60, 40))
    for b in ("rleg", "lleg"):
        s.remplir(b, (90, 70, 60))
        s.bande(b, 8, 12, (60, 40, 30))
    tabard(s, R, C, emb=lambda s: [s.pt("jacket", "front", x, y, C) for (x, y) in ((3, 7), (4, 7), (2, 8), (5, 8), (3, 9), (4, 9))])


def fyreslayers(s):
    P, O, Or, Cu = (222, 160, 120), (246, 110, 24), (230, 186, 64), (120, 56, 30)
    peau_tete(s, P)
    barbe(s, O)
    s.rect("head", "top", 0, 0, 8, 8, Or)                                 # heaume à drake
    s.rect("head", "front", 0, 0, 8, 2, Or)
    for f in ("right", "left", "back"):
        s.rect("head", f, 0, 0, 8, 2, Or)
    s.rect("hat", "top", 2, 0, 4, 8, O, bruit=10)                         # crête
    s.rect("hat", "front", 2, 0, 4, 2, O)
    s.rect("hat", "back", 2, 0, 4, 5, O, bruit=10)
    s.remplir("body", P)
    for (x, y) in ((2, 3), (5, 3), (3, 5), (4, 5), (2, 8), (5, 8)):     # runes d'ur-or
        s.pt("body", "front", x, y, Or)
    s.bande("body", 9, 12, Or)
    s.rect("body", "front", 3, 9, 2, 3, mul(Or, 1.2))
    for b in ("rarm", "larm"):
        s.remplir(b, P)
        s.bande(b, 3, 4, Or)
        s.bande(b, 9, 12, Or)
    for b in ("rleg", "lleg"):
        s.remplir(b, (70, 60, 110))
        s.bande(b, 9, 12, Cu)
    cape(s, (210, 120, 40), (150, 70, 20))                                # peau de salamandre


def kharadron(s):
    Cu, La, Pr, V = (186, 132, 74), (214, 186, 120), (88, 40, 72), (150, 220, 255)
    s.remplir("head", Cu)
    s.rect("head", "front", 1, 2, 6, 5, (60, 50, 50))                    # hublot
    s.rect("head", "front", 2, 3, 4, 3, V)
    s.rect("head", "front", 2, 3, 1, 1, (255, 255, 255))
    s.cadre("head", "front", La)
    for f in ("right", "left"):
        s.rect("head", f, 3, 3, 2, 2, La)
    s.rect("hat", "top", 2, 2, 4, 4, La)
    corps_armure(s, Cu, La, lambda s: s.rect("body", "front", 3, 2, 2, 2, V))
    s.rect("body", "back", 1, 1, 6, 8, (90, 90, 96))                     # réservoir d'aether
    s.rect("body", "back", 2, 2, 4, 2, V)
    bras_armure(s, Cu, La, (90, 90, 96), epaul=La)
    jambes_armure(s, Pr, La, Cu)


def khaine(s):
    P, Hc, Br, Pr = (226, 206, 206), (222, 200, 226), (176, 106, 56), (100, 36, 70)
    peau_tete(s, P, yeux=(150, 20, 40), bouche=(150, 40, 60))
    cheveux(s, Hc, long=True)
    s.rect("head", "front", 0, 2, 8, 1, Br)                               # bandeau de bronze
    s.remplir("body", P)
    s.rect("body", "front", 1, 1, 6, 4, Br, bruit=3)
    s.bande("body", 7, 9, Pr)
    for b in ("rarm", "larm"):
        s.remplir(b, P)
        s.bande(b, 8, 12, Br)
    for b in ("rleg", "lleg"):
        s.remplir(b, P)
        s.bande(b, 0, 5, Pr)
        s.bande(b, 8, 12, (60, 30, 40))
    cape(s, Pr, Br)


def idoneth(s):
    P, A, Ag, Bl, O = (226, 230, 234), (40, 72, 82), (160, 186, 186), (50, 90, 150), (232, 112, 52)
    s.remplir("head", A)
    s.rect("head", "front", 1, 3, 6, 4, P)                                # visage blanc
    s.rect("head", "front", 2, 4, 1, 1, (40, 40, 60))
    s.rect("head", "front", 5, 4, 1, 1, (40, 40, 60))
    s.rect("hat", "top", 3, 0, 2, 8, O, bruit=8)                          # nageoire orange
    s.rect("hat", "back", 3, 0, 2, 5, O)
    for f in ("right", "left"):
        s.rect("hat", f, 2, 1, 5, 2, O)
    corps_armure(s, A, Ag, lambda s: s.rect("body", "front", 3, 2, 2, 3, Ag))
    bras_armure(s, A, Ag, P, epaul=Ag)
    jambes_armure(s, A, Ag, mul(A, 0.8))
    cape(s, Bl, O)


def lumineth(s):
    W, G, Ro, Vi, P = (238, 238, 242), (212, 180, 92), (196, 120, 186), (120, 70, 140), (240, 220, 200)
    s.remplir("head", W)
    s.rect("head", "front", 1, 3, 6, 4, P)
    s.rect("head", "front", 2, 4, 1, 1, (70, 110, 160))
    s.rect("head", "front", 5, 4, 1, 1, (70, 110, 160))
    s.rect("head", "front", 0, 2, 8, 1, G)
    s.rect("hat", "top", 3, 0, 2, 8, Ro, bruit=8)                          # plumet
    s.rect("hat", "front", 3, 0, 2, 1, G)
    s.rect("hat", "back", 2, 0, 4, 7, Ro, bruit=8)
    corps_armure(s, W, G, lambda s: s.rect("body", "front", 3, 2, 2, 2, G))
    bras_armure(s, W, G, W, epaul=G)
    jambes_armure(s, W, G, G)
    tabard(s, Vi, G)


def seraphon(s):
    T, V, C, G = (62, 168, 200), (176, 218, 224), (44, 96, 160), (206, 160, 54)
    s.remplir("head", T, bruit=8)
    s.rect("head", "front", 0, 5, 8, 3, V)                                # mâchoire claire
    s.rect("head", "front", 1, 6, 6, 1, (240, 240, 230))                  # dents
    s.rect("head", "front", 1, 3, 2, 1, (250, 200, 40))
    s.rect("head", "front", 5, 3, 2, 1, (250, 200, 40))
    s.pt("head", "front", 2, 3, (20, 20, 20))
    s.pt("head", "front", 5, 3, (20, 20, 20))
    s.rect("hat", "top", 3, 0, 2, 8, C)                                   # crête
    s.rect("hat", "back", 3, 0, 2, 6, C)
    s.rect("hat", "front", 3, 0, 2, 2, C)
    for b in ("body", "rarm", "larm", "rleg", "lleg"):
        s.remplir(b, T, bruit=8)
    s.rect("body", "front", 2, 2, 4, 8, V)
    s.rect("body", "front", 1, 0, 6, 2, G)                                # collier d'or
    for b in ("rarm", "larm"):
        s.bande(b, 8, 9, G)
    for b in ("rleg", "lleg"):
        s.bande(b, 0, 4, (180, 40, 36))
        s.bande(b, 11, 12, mul(T, 0.7))


def sylvaneth(s):
    E, Fe, Cy = (112, 96, 64), (120, 170, 60), (150, 232, 240)
    for b in ("head", "body", "rarm", "larm", "rleg", "lleg"):
        s.remplir(b, E, bruit=10)
        for f in COTES:
            for x in range(0, faces(b)[f][2], 3):
                s.colonne(b, f, x, 0, faces(b)[f][3], mul(E, 0.75))
    s.rect("head", "front", 1, 2, 6, 5, Cy)                               # visage-esprit
    s.rect("head", "front", 2, 3, 1, 2, (20, 60, 70))
    s.rect("head", "front", 5, 3, 1, 2, (20, 60, 70))
    s.rect("head", "front", 3, 6, 2, 1, (60, 130, 140))
    for (x, y) in ((0, 0), (1, 1), (6, 1), (7, 0), (2, 0), (5, 0)):       # ramure
        s.pt("hat", "front", x, y, mul(E, 0.8))
    s.rect("hat", "top", 0, 0, 8, 8, Fe, bruit=14)
    s.rect("jacket", "front", 2, 2, 4, 3, Fe, bruit=14)
    s.rect("rpants", "front", 0, 0, 4, 3, Fe, bruit=14)


def esclaves(s):
    N, Bz, R, F, Co = (38, 38, 44), (182, 140, 72), (150, 30, 30), (206, 190, 160), (222, 206, 170)
    s.remplir("head", N)
    s.rect("head", "front", 3, 2, 2, 5, (10, 10, 10))                     # fente en T
    s.rect("head", "front", 1, 3, 6, 1, (10, 10, 10))
    s.rect("head", "front", 0, 0, 8, 1, Bz)
    for f in ("right", "left"):
        s.rect("hat", f, 1, 0, 2, 3, Co)                                  # cornes
    s.rect("hat", "top", 0, 1, 1, 2, Co)
    s.rect("hat", "top", 7, 1, 1, 2, Co)
    corps_armure(s, N, Bz, lambda s: [s.pt("body", "front", x, y, Bz) for (x, y) in ((3, 2), (4, 2), (2, 3), (5, 3), (3, 4), (4, 4))])
    bras_armure(s, N, Bz, N, epaul=F)
    jambes_armure(s, N, Bz, mul(N, 1.2))
    cape(s, R, Bz)


def khorne(s):
    R, L, N = (130, 32, 30), (172, 122, 62), (40, 32, 30)
    s.remplir("head", R)
    s.rect("head", "front", 1, 3, 6, 3, (30, 10, 10))                     # grille
    for x in (2, 4, 6):
        s.colonne("head", "front", x, 3, 6, L)
    s.rect("head", "front", 0, 1, 8, 1, L)
    for f in ("right", "left"):
        s.rect("hat", f, 0, 0, 3, 3, N)                                   # cornes noires
    s.rect("hat", "top", 0, 0, 2, 2, N)
    s.rect("hat", "top", 6, 0, 2, 2, N)
    corps_armure(s, R, L, lambda s: [s.pt("body", "front", x, y, L) for (x, y) in ((2, 2), (3, 2), (4, 2), (5, 2), (4, 3), (3, 4), (2, 5), (3, 5), (4, 5), (5, 5))])
    bras_armure(s, R, L, mul(R, 0.8), epaul=L)
    jambes_armure(s, R, L, N)


def tzeentch(s):
    F, T, Cu, C = (176, 126, 86), (52, 172, 192), (192, 142, 82), (226, 220, 204)
    s.remplir("head", F)
    s.rect("head", "front", 2, 4, 4, 4, (230, 214, 170))                  # bec
    s.rect("head", "front", 3, 7, 2, 1, mul((230, 214, 170), 0.7))
    s.rect("head", "front", 1, 3, 1, 1, (90, 220, 255))
    s.rect("head", "front", 6, 3, 1, 1, (90, 220, 255))
    for f in ("right", "left"):
        s.rect("hat", f, 0, 0, 3, 2, (230, 214, 170))                     # cornes
    s.remplir("body", F)
    s.rect("body", "front", 0, 0, 8, 3, T)
    s.bande("body", 8, 9, Cu)
    for b in ("rarm", "larm"):
        s.remplir(b, F)
        s.bande(b, 0, 3, T)
        s.bande(b, 8, 10, Cu)
    for b in ("rleg", "lleg"):
        s.remplir(b, F)
        s.bande(b, 10, 12, (90, 60, 40))
    tabard(s, C, T)


def slaanesh(s):
    P, G, Ro, Vi = (206, 200, 220), (200, 160, 82), (214, 150, 206), (112, 52, 112)
    peau_tete(s, P, yeux=(130, 60, 180), bouche=(160, 60, 120))
    cheveux(s, Ro, long=True)
    s.rect("head", "front", 0, 2, 8, 1, G)
    corps_armure(s, G, Vi, lambda s: s.rect("body", "front", 3, 2, 2, 2, Ro))
    for b in ("rarm", "larm"):
        s.remplir(b, P)
        s.bande(b, 8, 12, (78, 44, 100))
    for b in ("rleg", "lleg"):
        s.remplir(b, Vi)
        s.bande(b, 9, 12, G)
    cape(s, Vi, G)


def nurgle(s):
    V, P, Ro = (68, 88, 58), (176, 188, 128), (120, 84, 50)
    s.remplir("head", V)
    s.rect("head", "front", 1, 2, 6, 6, P)
    s.rect("head", "front", 3, 3, 2, 1, (230, 200, 40))                   # œil unique
    s.rect("head", "front", 2, 6, 4, 1, (90, 60, 40))
    s.rect("hat", "front", 3, 0, 2, 2, (46, 70, 70))                       # corne unique
    for b in ("body", "rarm", "larm", "rleg", "lleg"):
        s.remplir(b, V, bruit=8)
    s.rect("body", "front", 2, 4, 4, 5, P)
    s.rect("body", "front", 3, 6, 2, 2, (150, 60, 60))                     # plaie
    for b in ("rarm", "larm"):
        s.bande(b, 9, 12, P)
        s.bande(b, 4, 5, Ro)
    s.bande("body", 9, 10, Ro)


def skaven(s):
    F, Ro, R, Cu = (136, 108, 92), (214, 140, 140), (150, 40, 40), (172, 112, 70)
    s.remplir("head", F, bruit=8)
    s.rect("head", "front", 2, 5, 4, 3, mul(F, 1.15))                     # museau
    s.rect("head", "front", 3, 5, 2, 1, Ro)
    s.rect("head", "front", 3, 7, 2, 1, (240, 230, 200))                  # incisives
    s.rect("head", "front", 1, 3, 1, 1, (200, 30, 30))
    s.rect("head", "front", 6, 3, 1, 1, (200, 30, 30))
    for f in ("right", "left"):
        s.rect("hat", f, 1, 0, 3, 3, Ro)                                  # oreilles
    for b in ("body", "rarm", "larm", "rleg", "lleg"):
        s.remplir(b, F, bruit=8)
    s.rect("body", "front", 1, 0, 6, 9, R, bruit=6)                        # haillons rouges
    s.rect("body", "front", 2, 9, 2, 1, R)
    s.bande("body", 6, 7, Cu)
    for b in ("rarm", "larm"):
        s.bande(b, 10, 12, Ro)
    for b in ("rleg", "lleg"):
        s.bande(b, 11, 12, Ro)
    s.rect("rpants", "back", 1, 0, 2, 12, Ro)                              # queue


def hashut(s):
    N, Bz, Br = (40, 40, 44), (176, 120, 60), (255, 120, 30)
    s.remplir("head", Bz)
    s.rect("head", "front", 1, 3, 2, 1, Br)
    s.rect("head", "front", 5, 3, 2, 1, Br)
    s.rect("head", "front", 2, 5, 4, 3, mul(Bz, 0.8))                     # mufle de taureau
    s.rect("head", "front", 3, 6, 2, 1, (20, 20, 20))
    for f in ("right", "left"):
        s.rect("hat", f, 0, 1, 4, 2, (230, 220, 190))
    corps_armure(s, N, Bz, lambda s: s.rect("body", "front", 3, 3, 2, 2, Br))
    bras_armure(s, N, Bz, N, epaul=Bz)
    jambes_armure(s, N, Bz, Bz)


def nighthaunt(s):
    G, Ca, Ch = (190, 228, 218), (78, 54, 44), (110, 76, 52)
    s.remplir("head", Ca)
    s.rect("head", "front", 1, 2, 6, 6, (30, 50, 50))
    s.rect("head", "front", 2, 3, 4, 4, G)                                # crâne spectral
    s.rect("head", "front", 2, 4, 1, 1, (10, 40, 40))
    s.rect("head", "front", 5, 4, 1, 1, (10, 40, 40))
    s.rect("head", "front", 3, 6, 2, 1, (60, 100, 100))
    s.rect("hat", "top", 0, 0, 8, 8, Ca)
    for b in ("body", "rarm", "larm"):
        s.remplir(b, G, bruit=10)
    s.rect("body", "front", 0, 0, 8, 3, Ca)
    for b in ("rleg", "lleg"):
        s.remplir(b, mul(G, 0.9), bruit=10)
        for f in COTES:
            fx, fy, fw, fh = faces(b)[f]
            for j in range(8, fh):
                for i in range(fw):
                    a = int(255 * (1 - (j - 7) / 6))
                    c = s.p[fx + i, fy + j]
                    s.p[fx + i, fy + j] = c[:3] + (max(80, a),)
    for b in ("rarm", "larm"):
        s.bande(b, 3, 4, Ch)
        s.bande(b, 7, 8, Ch)
    s.bande("body", 5, 6, Ch)


def soulblight(s):
    R, G, T, P = (150, 28, 32), (196, 152, 60), (36, 64, 58), (226, 222, 226)
    peau_tete(s, P, yeux=(220, 20, 30), bouche=(140, 20, 30))
    s.rect("head", "top", 0, 0, 8, 8, R)
    s.rect("head", "front", 0, 0, 8, 2, R)
    for f in ("right", "left", "back"):
        s.rect("head", f, 0, 0, 8, 3, R)
    s.rect("hat", "top", 3, 0, 2, 8, G)
    s.rect("hat", "front", 2, 0, 4, 1, G)
    corps_armure(s, R, G, lambda s: s.rect("body", "front", 3, 2, 2, 3, G))
    bras_armure(s, R, G, mul(R, 0.7), epaul=R)
    jambes_armure(s, R, G, (40, 30, 30))
    cape(s, T, G)


def ossiarch(s):
    O, Bn, Vg, Rg = (218, 204, 168), (44, 54, 96), (130, 224, 172), (150, 40, 40)
    s.remplir("head", O)
    s.rect("head", "front", 1, 3, 2, 2, (30, 40, 40))
    s.rect("head", "front", 5, 3, 2, 2, (30, 40, 40))
    s.pt("head", "front", 2, 4, Vg)
    s.pt("head", "front", 5, 4, Vg)
    s.rect("head", "front", 2, 6, 4, 1, (60, 60, 50))
    for x in (2, 4):
        s.pt("head", "front", x, 6, O)
    s.rect("hat", "top", 3, 0, 2, 8, O)                                   # cimier d'os
    s.rect("hat", "front", 3, 0, 2, 2, O)
    s.rect("hat", "back", 3, 0, 2, 4, O)
    s.remplir("body", O)
    for y in (2, 4, 6):
        s.rect("body", "front", 2, y, 4, 1, mul(O, 0.7))                  # côtes
    s.rect("body", "front", 0, 0, 8, 2, Bn)
    s.bande("body", 8, 9, Bn)
    for b in ("rarm", "larm", "rleg", "lleg"):
        s.remplir(b, O)
        s.bande(b, 2, 5, Bn)
        s.bande(b, 5, 6, mul(O, 0.7))
    tabard(s, Bn, O, emb=lambda s: s.rect("jacket", "front", 3, 8, 2, 2, Vg))


def fec(s):
    P, N, Br = (166, 186, 150), (30, 30, 32), (110, 80, 60)
    peau_tete(s, P, yeux=(200, 40, 40), bouche=(80, 30, 30))
    cheveux(s, N)
    s.rect("head", "front", 2, 6, 4, 1, (230, 230, 210))
    for b in ("body", "rarm", "larm", "rleg", "lleg"):
        s.remplir(b, P, bruit=8)
    for y in (3, 5):
        s.rect("body", "front", 2, y, 4, 1, mul(P, 0.75))
    for b in ("rleg", "lleg"):
        s.bande(b, 0, 4, Br)
    s.rect("rpants", "front", 0, 0, 4, 5, mul(Br, 0.9))


def ironjawz(s):
    J, Fe, V = (226, 184, 34), (62, 62, 68), (96, 140, 56)
    s.remplir("head", J)
    s.rect("head", "front", 1, 3, 6, 5, V)
    s.rect("head", "front", 2, 4, 1, 1, (200, 30, 30))
    s.rect("head", "front", 5, 4, 1, 1, (200, 30, 30))
    s.rect("head", "front", 1, 6, 1, 2, (240, 230, 200))                  # défenses
    s.rect("head", "front", 6, 6, 1, 2, (240, 230, 200))
    for x in range(0, 8, 2):
        s.pt("head", "front", x, 0, Fe)
        s.pt("head", "front", x + 1, 1, Fe)
    corps_armure(s, J, Fe, lambda s: [s.pt("body", "front", x, y, Fe) for x in range(0, 8) for y in (5, 6) if (x + y) % 2 == 0])
    bras_armure(s, J, Fe, V, epaul=Fe)
    jambes_armure(s, J, Fe, Fe)


def kruleboyz(s):
    V, Cu, Fe, R = (132, 150, 72), (100, 70, 50), (66, 62, 56), (190, 40, 30)
    peau_tete(s, V, yeux=(220, 200, 40), bouche=(60, 40, 30))
    s.rect("head", "front", 3, 4, 2, 3, mul(V, 0.85))                     # long nez
    s.rect("head", "top", 0, 0, 8, 8, Fe)
    s.rect("head", "front", 0, 0, 8, 2, Fe)
    for f in ("right", "left", "back"):
        s.rect("head", f, 0, 0, 8, 2, Fe)
    s.rect("hat", "top", 3, 0, 2, 6, R)
    for b in ("body", "rarm", "larm", "rleg", "lleg"):
        s.remplir(b, Cu, bruit=8)
    s.rect("body", "front", 2, 1, 4, 4, R)
    s.rect("body", "front", 3, 2, 2, 1, (240, 230, 200))
    for b in ("rarm", "larm"):
        s.bande(b, 9, 12, V)
    s.bande("body", 7, 8, Fe)


def gitz(s):
    N, V, J = (34, 34, 46), (150, 190, 100), (230, 210, 60)
    s.remplir("head", N)
    s.rect("head", "front", 1, 3, 6, 5, V)
    s.rect("head", "front", 2, 4, 1, 1, (220, 30, 30))
    s.rect("head", "front", 5, 4, 1, 1, (220, 30, 30))
    s.rect("head", "front", 3, 5, 2, 2, mul(V, 0.8))                      # grand nez
    s.rect("head", "front", 2, 7, 4, 1, (240, 230, 200))
    s.rect("hat", "top", 2, 2, 4, 4, N)                                   # capuche pointue
    s.rect("hat", "front", 2, 0, 4, 2, N)
    s.rect("hat", "back", 2, 0, 4, 6, N)
    for b in ("body", "rarm", "larm", "rleg", "lleg"):
        s.remplir(b, N, bruit=5)
    s.rect("body", "front", 2, 3, 4, 4, J)                                # lune jaune
    s.rect("body", "front", 3, 4, 1, 1, N)
    s.rect("body", "front", 4, 5, 1, 1, N)
    for b in ("rarm", "larm"):
        s.bande(b, 10, 12, V)


def ogors(s):
    P, A, Bl, R = (218, 150, 128), (150, 150, 156), (70, 92, 132), (160, 40, 40)
    peau_tete(s, P, yeux=(60, 40, 30), bouche=(120, 40, 40))
    s.rect("head", "front", 1, 6, 6, 2, (140, 50, 40))                    # grande bouche
    s.rect("head", "front", 2, 6, 1, 1, (240, 230, 200))
    s.rect("head", "front", 5, 6, 1, 1, (240, 230, 200))
    s.rect("head", "front", 0, 2, 8, 1, mul(P, 0.85))
    for b in ("body", "rarm", "larm"):
        s.remplir(b, P, bruit=4)
    s.rect("body", "front", 1, 5, 6, 5, A)                                # gutplate
    s.cadre("body", "front", mul(A, 0.6), haut=False, cote=False)
    s.rect("body", "front", 3, 6, 2, 2, R)
    for b in ("rleg", "lleg"):
        s.remplir(b, Bl)
        s.bande(b, 10, 12, (60, 40, 30))
    for b in ("rarm", "larm"):
        s.bande(b, 9, 10, (90, 60, 40))


def behemat(s):
    P, Br, Ve = (222, 170, 146), (120, 90, 60), (110, 120, 70)
    peau_tete(s, P, yeux=(60, 40, 30))
    barbe(s, (190, 100, 50), longue=False)
    for b in ("body", "rarm", "larm"):
        s.remplir(b, P, bruit=4)
    s.rect("body", "front", 2, 3, 1, 1, mul(P, 0.85))
    s.bande("body", 8, 12, Br)
    for b in ("rleg", "lleg"):
        s.remplir(b, Br, bruit=8)
        s.bande(b, 3, 6, Ve)
        s.bande(b, 10, 12, P)
    s.rect("body", "back", 1, 1, 3, 3, Ve)                                 # rapiéçage


FACTIONS = [("stormcast", stormcast), ("cites", cites), ("fyreslayers", fyreslayers), ("kharadron", kharadron),
            ("khaine", khaine), ("idoneth", idoneth), ("lumineth", lumineth), ("seraphon", seraphon),
            ("sylvaneth", sylvaneth), ("esclaves", esclaves), ("khorne", khorne), ("tzeentch", tzeentch),
            ("slaanesh", slaanesh), ("nurgle", nurgle), ("skaven", skaven), ("hashut", hashut),
            ("nighthaunt", nighthaunt), ("soulblight", soulblight), ("ossiarch", ossiarch), ("fec", fec),
            ("ironjawz", ironjawz), ("kruleboyz", kruleboyz), ("gitz", gitz), ("ogors", ogors), ("behemat", behemat)]


# ------------------------------------------------------------------ aperçu face / dos
def poupee(im, dos=False, k=6):
    """Assemble la face (ou le dos) du personnage à partir du skin, calque supérieur compris."""
    out = Image.new("RGBA", (16 * k, 32 * k), (0, 0, 0, 0))
    def coller(part, x, y, inverse=False):
        f = faces(part)["back" if dos else "front"]
        r = im.crop((f[0], f[1], f[0] + f[2], f[1] + f[3]))
        if inverse:
            r = r.transpose(Image.FLIP_LEFT_RIGHT)
        r = r.resize((f[2] * k, f[3] * k), Image.NEAREST)
        out.alpha_composite(r, (x * k, y * k))
    plan = [("head", 4, 0), ("body", 4, 8), ("rarm", 0, 8), ("larm", 12, 8), ("rleg", 4, 20), ("lleg", 8, 20)]
    if dos:
        plan = [("head", 4, 0), ("body", 4, 8), ("rarm", 12, 8), ("larm", 0, 8), ("rleg", 8, 20), ("lleg", 4, 20)]
    sur = {"head": "hat", "body": "jacket", "rarm": "rsleeve", "larm": "lsleeve", "rleg": "rpants", "lleg": "lpants"}
    for p, x, y in plan:
        coller(p, x, y)
    for p, x, y in plan:
        coller(sur[p], x, y)
    return out


def planche(skins, noms, chemin):
    k = 5
    cw, ch = 16 * k * 2 + 30, 32 * k + 40
    cols = 5
    rows = (len(skins) + cols - 1) // cols
    W, H = cols * cw + 40, rows * ch + 90
    fond = Image.new("RGBA", (W, H), (14, 26, 51, 255))
    d = ImageDraw.Draw(fond)
    try:
        fb = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 26)
        fn = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 15)
    except OSError:
        fb = fn = ImageFont.load_default()
    d.rectangle((6, 6, W - 7, H - 7), outline=(212, 166, 58), width=3)
    d.rectangle((12, 12, W - 13, H - 13), outline=(140, 108, 40), width=1)
    d.text((30, 26), "Skins des 25 factions — face et dos", fill=(242, 210, 122), font=fb)
    for i, (sk, nom) in enumerate(zip(skins, noms)):
        x, y = 20 + (i % cols) * cw, 72 + (i // cols) * ch
        fond.alpha_composite(poupee(sk, False, k), (x + 8, y))
        fond.alpha_composite(poupee(sk, True, k), (x + 16 * k + 18, y))
        d.text((x + 10, y + 32 * k + 8), nom, fill=(230, 214, 172), font=fn)
    fond.convert("RGB").save(chemin)


if __name__ == "__main__":
    import json
    os.makedirs(SORTIE, exist_ok=True)
    noms = {}
    try:
        sys_path = "/home/claude/aos"
        import sys
        sys.path.insert(0, sys_path)
        from data_factions import FACTIONS as FD
        noms = {f["id"]: f["nom"] for f in FD}
    except Exception:
        pass
    skins = []
    for i, (fid, fn_) in enumerate(FACTIONS):
        s = Skin(i * 31 + 7)
        fn_(s)
        s.im.save(os.path.join(SORTIE, fid + ".png"))
        os.makedirs(BAS, exist_ok=True)
        s.im.save(os.path.join(BAS, fid + ".png"))
        skins.append(s.im)
    os.makedirs(os.path.join(ICI, "apercus"), exist_ok=True)
    planche(skins, [noms.get(f, f) for f, _ in FACTIONS], os.path.join(ICI, "apercus", "planche_skins.png"))
    print(len(skins), "skins")
