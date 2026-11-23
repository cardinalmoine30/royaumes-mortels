# -*- coding: utf-8 -*-
"""Textures de l'inventaire « table de taverne » (pixel art, 1 texel = 1 pixel d'interface).
Sortie : assets/royaumes/textures/gui/taverne/{table,inventaire,carnet,onglets,decor}.png"""
import math
import os
import random
from PIL import Image, ImageDraw

ICI = os.path.dirname(os.path.abspath(__file__))
SORTIE = os.path.join(ICI, "..", "..", "src", "main", "resources", "assets", "royaumes", "textures", "gui", "taverne")
rng = random.Random(7)


def cl(v):
    return max(0, min(255, int(v)))


def teinte(c, k, n=0):
    return tuple(cl(v * k + n) for v in c[:3]) + ((c[3],) if len(c) > 3 else (255,))


# ------------------------------------------------------------------ table de chêne (raccordable)
def table():
    W = 256
    im = Image.new("RGBA", (W, W))
    px = im.load()
    base = (98, 64, 38)
    for planche in range(4):
        y0 = planche * 64
        ph = rng.random() * 6.28
        teinte_p = 0.92 + rng.random() * 0.16
        for y in range(64):
            for x in range(W):
                # veinage périodique en x (raccord parfait)
                v = math.sin(2 * math.pi * (x / W) * 3 + ph + math.sin(2 * math.pi * x / W * 2 + y * 0.21) * 1.4 + y * 0.35)
                k = teinte_p * (1 + 0.09 * v) * (0.97 + 0.06 * math.sin(2 * math.pi * x / W * 17 + y))
                if v > 0.93:
                    k *= 0.8
                n = rng.randint(-5, 5)
                c = teinte(base, k, n)
                if y < 2 or y > 61:                      # joints entre planches
                    c = (38, 24, 14, 255) if (y in (0, 63)) else teinte(base, 0.62)
                px[x, y0 + y] = c
        # nœuds
        for _ in range(2):
            cx, cy = rng.randint(10, W - 10), y0 + rng.randint(14, 50)
            for dy in range(-5, 6):
                for dx in range(-8, 9):
                    d = (dx / 8) ** 2 + (dy / 5) ** 2
                    if d < 1:
                        r = math.sqrt(d)
                        k = 0.55 + 0.4 * r + 0.08 * math.sin(r * 14)
                        px[(cx + dx) % W, cy + dy] = teinte(base, k)
        # clous
        for xc in range(18, W, 64):
            xx = (xc + planche * 23) % W
            for yy in (y0 + 6, y0 + 57):
                px[xx, yy] = (50, 46, 44, 255)
                px[xx + 1, yy] = (88, 84, 80, 255)
    # taches de chopes et rayures (fondues dans le bois)
    ov = Image.new("RGBA", (W, W), (0, 0, 0, 0))
    d = ImageDraw.Draw(ov)
    for _ in range(4):
        cx, cy, r = rng.randint(30, 220), rng.randint(30, 220), rng.randint(9, 14)
        d.ellipse((cx - r, cy - r, cx + r, cy + r), outline=(40, 24, 12, 90))
        d.ellipse((cx - r + 1, cy - r + 1, cx + r - 1, cy + r - 1), outline=(50, 30, 16, 50))
    for _ in range(10):
        x, y = rng.randint(10, 240), rng.randint(10, 240)
        L, a = rng.randint(6, 18), rng.random() * math.pi
        d.line((x, y, x + L * math.cos(a), y + L * math.sin(a)), fill=(150, 112, 76, 80))
    im.alpha_composite(ov)
    return im


# ------------------------------------------------------------------ panneau d'inventaire (176 x 166)
def parchemin(px, x0, y0, w, h, base=(226, 204, 156), bord=6):
    for y in range(h):
        for x in range(w):
            e = min(x, y, w - 1 - x, h - 1 - y)
            k = 1.0 - (0.22 * (1 - e / bord) if e < bord else 0)
            k *= 0.97 + 0.04 * math.sin(x * 0.31 + y * 0.17) * math.sin(y * 0.11)
            px[x0 + x, y0 + y] = teinte(base, k, rng.randint(-4, 4))


def case(d, x, y, w=18, h=18):
    d.rectangle((x, y, x + w - 1, y + h - 1), fill=(92, 66, 44))
    d.line((x, y, x + w - 2, y), fill=(56, 38, 24))
    d.line((x, y, x, y + h - 2), fill=(56, 38, 24))
    d.line((x + 1, y + h - 1, x + w - 1, y + h - 1), fill=(246, 230, 192))
    d.line((x + w - 1, y + 1, x + w - 1, y + h - 1), fill=(246, 230, 192))
    d.rectangle((x + 1, y + 1, x + w - 2, y + h - 2), fill=(104, 76, 50))


def panneau():
    im = Image.new("RGBA", (256, 256), (0, 0, 0, 0))
    px = im.load()
    W, H = 176, 166
    bois = (122, 82, 48)
    for y in range(H):
        for x in range(W):
            v = math.sin(x * 0.09 + math.sin(y * 0.3) * 1.2 + y * 0.05)
            px[x, y] = teinte(bois, 1 + 0.08 * v, rng.randint(-5, 5))
    d = ImageDraw.Draw(im)
    d.rectangle((0, 0, W - 1, H - 1), outline=(52, 32, 18))
    d.rectangle((1, 1, W - 2, H - 2), outline=(160, 116, 72))
    parchemin(px, 4, 4, W - 8, H - 8)
    d.rectangle((3, 3, W - 4, H - 4), outline=(70, 44, 24))
    # coins de fer rivetés
    for (cx, cy, sx, sy) in ((0, 0, 1, 1), (W - 1, 0, -1, 1), (0, H - 1, 1, -1), (W - 1, H - 1, -1, -1)):
        for i in range(9):
            for j in range(3):
                for (xx, yy) in ((cx + sx * i, cy + sy * j), (cx + sx * j, cy + sy * i)):
                    px[xx, yy] = (70, 70, 76, 255) if (i + j) % 5 else (110, 110, 118, 255)
        px[cx + sx * 1, cy + sy * 1] = (170, 170, 176, 255)
        px[cx + sx * 6, cy + sy * 1] = (150, 150, 156, 255)
        px[cx + sx * 1, cy + sy * 6] = (150, 150, 156, 255)
    # fenêtre du personnage : alcôve éclairée à la bougie
    d.rectangle((25, 7, 76, 79), fill=(46, 30, 20))
    for y in range(8, 79):
        t = (y - 8) / 71
        c = (cl(34 + 40 * (1 - t) * 0.6), cl(22 + 26 * (1 - t) * 0.6), cl(16 + 12 * (1 - t) * 0.6))
        d.line((26, y, 75, y), fill=c)
    d.rectangle((24, 6, 77, 80), outline=(68, 44, 24))
    d.line((25, 80, 77, 80), fill=(240, 222, 180))
    d.line((77, 7, 77, 80), fill=(240, 222, 180))
    # cases : armure, main secondaire, artisanat 2x2, résultat, sac, barre d'action
    for i in range(4):
        case(d, 7, 7 + 18 * i)
    case(d, 76, 61)
    for i in range(2):
        for j in range(2):
            case(d, 97 + 18 * j, 17 + 18 * i)
    d.rectangle((150, 24, 173, 47), outline=(176, 132, 52))
    d.rectangle((151, 25, 172, 46), outline=(214, 172, 74))
    case(d, 153, 27)
    for r in range(3):
        for c in range(9):
            case(d, 7 + 18 * c, 83 + 18 * r)
    for c in range(9):
        case(d, 7 + 18 * c, 141)
    # flèche d'artisanat
    fl = [(134, 34), (146, 34), (146, 30), (152, 36), (146, 42), (146, 38), (134, 38)]
    d.polygon(fl, fill=(110, 76, 44), outline=(62, 40, 22))
    # filet décoratif entre le sac et la barre d'action
    for x in range(8, 168):
        if x % 6 != 3:
            px[x, 138] = (150, 116, 76, 255)
    for x in (8, 87, 167):
        d.rectangle((x - 1, 137, x + 1, 139), fill=(176, 132, 52))
    return im


# ------------------------------------------------------------------ carnet du héros (118 x 166)
def carnet():
    im = Image.new("RGBA", (256, 256), (0, 0, 0, 0))
    px = im.load()
    W, H = 118, 166
    parchemin(px, 0, 0, W, H, base=(234, 214, 168), bord=8)
    # bords déchirés
    for x in range(W):
        for y in range(rng.randint(0, 2)):
            px[x, y] = (0, 0, 0, 0)
            px[x, H - 1 - y] = (0, 0, 0, 0)
    for y in range(H):
        for x in range(rng.randint(0, 2)):
            px[x, y] = (0, 0, 0, 0)
            px[W - 1 - x, y] = (0, 0, 0, 0)
    d = ImageDraw.Draw(im)
    for y in range(30, H - 20, 11):                        # lignes d'écriture
        for x in range(8, W - 8):
            if x % 2 == 0:
                px[x, y] = teinte(px[x, y], 0.9)
    # signet rouge
    d.rectangle((W - 18, 0, W - 12, 26), fill=(150, 30, 30))
    d.polygon([(W - 18, 26), (W - 12, 26), (W - 15, 22)], fill=(0, 0, 0, 0))
    d.line((W - 17, 0, W - 17, 24), fill=(190, 60, 50))
    # sceau de cire
    cx, cy = W - 18, H - 16
    d.ellipse((cx - 9, cy - 9, cx + 9, cy + 9), fill=(150, 26, 30))
    d.ellipse((cx - 7, cy - 7, cx + 7, cy + 7), outline=(110, 16, 20))
    d.line((cx - 3, cy + 4, cx, cy - 4), fill=(200, 70, 60))
    d.line((cx, cy - 4, cx + 3, cy + 4), fill=(200, 70, 60))
    d.line((cx - 2, cy + 1, cx + 2, cy + 1), fill=(200, 70, 60))
    return im


# ------------------------------------------------------------------ onglets (52 x 24) et icônes 16 x 16
def onglets():
    im = Image.new("RGBA", (256, 64), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    for k, (fond, ombre) in enumerate((((204, 176, 126), (150, 118, 76)), ((236, 210, 154), (176, 142, 92)))):
        y0 = k * 24
        d.rounded_rectangle((0, y0, 51, y0 + 23), radius=4, fill=fond, outline=(78, 50, 28))
        d.rectangle((1, y0 + 19, 50, y0 + 23), fill=ombre)
        d.line((2, y0 + 1, 49, y0 + 1), fill=teinte(fond, 1.12)[:3])
        px = im.load()
        for y in range(y0 + 2, y0 + 19):
            for x in range(2, 50):
                if rng.random() < 0.08:
                    px[x, y] = teinte(px[x, y], 0.94)
    # icônes : codex, forge, blocs, héros
    x = 64
    # livre
    d.rectangle((x + 2, 2, x + 13, 14), fill=(120, 40, 30))
    d.rectangle((x + 4, 3, x + 13, 13), fill=(236, 226, 196))
    d.line((x + 4, 3, x + 4, 13), fill=(90, 28, 22))
    for yy in (5, 7, 9, 11):
        d.line((x + 6, yy, x + 11, yy), fill=(150, 130, 100))
    d.rectangle((x + 2, 2, x + 3, 14), fill=(90, 28, 22))
    # enclume
    x = 80
    d.rectangle((x + 2, 5, x + 13, 7), fill=(70, 72, 80))
    d.polygon([(x + 1, 5), (x + 3, 5), (x + 3, 7)], fill=(70, 72, 80))
    d.rectangle((x + 6, 8, x + 10, 10), fill=(56, 58, 64))
    d.rectangle((x + 4, 11, x + 12, 13), fill=(50, 52, 58))
    d.line((x + 3, 5, x + 13, 5), fill=(130, 132, 140))
    d.point((x + 12, 3), fill=(255, 180, 60))
    d.point((x + 11, 2), fill=(255, 220, 120))
    # bloc de cristal des Royaumes
    x = 96
    d.polygon([(x + 8, 2), (x + 14, 5), (x + 8, 8), (x + 2, 5)], fill=(190, 140, 230))
    d.polygon([(x + 2, 5), (x + 8, 8), (x + 8, 14), (x + 2, 11)], fill=(120, 70, 170))
    d.polygon([(x + 14, 5), (x + 8, 8), (x + 8, 14), (x + 14, 11)], fill=(150, 96, 200))
    d.point((x + 6, 4), fill=(255, 255, 255))
    # héros : heaume et étoile
    x = 112
    d.rectangle((x + 4, 3, x + 11, 12), fill=(204, 158, 52))
    d.rectangle((x + 5, 7, x + 10, 8), fill=(30, 24, 20))
    d.rectangle((x + 7, 8, x + 8, 11), fill=(30, 24, 20))
    d.line((x + 7, 1, x + 8, 1), fill=(40, 66, 150))
    d.rectangle((x + 7, 2, x + 8, 3), fill=(40, 66, 150))
    d.line((x + 4, 12, x + 11, 12), fill=(150, 110, 30))
    d.point((x + 13, 2), fill=(255, 240, 150))
    d.point((x + 2, 4), fill=(255, 240, 150))
    return im


# ------------------------------------------------------------------ décor posé sur la table
def decor():
    im = Image.new("RGBA", (256, 256), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    # chope d'étain mousseuse (0,0) 40x48
    d.rounded_rectangle((4, 10, 30, 46), radius=3, fill=(132, 134, 142), outline=(60, 62, 70))
    for x in range(6, 30, 2):
        d.line((x, 12, x, 44), fill=(146, 148, 156) if x % 4 else (116, 118, 126))
    d.rectangle((4, 18, 30, 20), fill=(90, 92, 100))
    d.rectangle((4, 36, 30, 38), fill=(90, 92, 100))
    d.arc((24, 18, 39, 38), -90, 90, fill=(70, 72, 80), width=3)
    d.ellipse((2, 4, 32, 16), fill=(240, 232, 210))
    for (x, y) in ((6, 6), (14, 3), (22, 5), (27, 8), (10, 9)):
        d.ellipse((x, y, x + 6, y + 5), fill=(250, 246, 232))
    d.line((28, 14, 30, 22), fill=(236, 220, 170))
    # bougie sur bougeoir (48,0) 24x64
    d.ellipse((48, 56, 71, 63), fill=(150, 110, 40), outline=(90, 64, 20))
    d.rectangle((57, 50, 62, 57), fill=(170, 126, 46))
    d.rectangle((54, 22, 65, 52), fill=(236, 226, 196))
    d.line((54, 22, 54, 52), fill=(206, 194, 160))
    d.rectangle((56, 23, 58, 30), fill=(246, 240, 220))
    d.polygon([(64, 24), (66, 24), (66, 33), (64, 30)], fill=(226, 214, 182))
    d.line((59, 18, 59, 22), fill=(40, 30, 20))
    d.polygon([(59, 4), (63, 12), (61, 18), (57, 18), (55, 12)], fill=(255, 160, 40))
    d.polygon([(59, 8), (61, 13), (60, 17), (58, 17), (57, 13)], fill=(255, 236, 140))
    # pièces (80,0) 36x22
    for (x, y) in ((82, 10), (92, 12), (100, 8), (88, 4), (96, 2), (106, 11)):
        d.ellipse((x, y, x + 9, y + 6), fill=(214, 170, 60), outline=(140, 100, 30))
        d.line((x + 2, y + 2, x + 6, y + 2), fill=(250, 220, 120))
    # dés (80,24) 30x16
    for (x, y, pts) in ((82, 26, ((3, 3), (7, 7), (11, 11))), (98, 28, ((3, 3), (11, 3), (7, 7), (3, 11), (11, 11)))):
        d.rounded_rectangle((x, y, x + 14, y + 14), radius=2, fill=(232, 224, 204), outline=(120, 110, 90))
        for (a, b) in pts:
            d.rectangle((x + a, y + b, x + a + 1, y + b + 1), fill=(150, 30, 30))
    # carte roulée (0,64) 72x34
    d.rectangle((6, 70, 66, 92), fill=(226, 204, 156), outline=(120, 90, 56))
    for (x, y, x2, y2) in ((12, 80, 30, 74), (30, 74, 44, 84), (44, 84, 58, 76)):
        d.line((x, y, x2, y2), fill=(150, 40, 30))
    d.ellipse((46, 72, 54, 80), outline=(60, 90, 140))
    d.line((20, 86, 26, 86), fill=(90, 70, 40))
    d.ellipse((0, 66, 10, 96), fill=(206, 182, 134), outline=(110, 80, 48))
    d.ellipse((62, 66, 72, 96), fill=(206, 182, 134), outline=(110, 80, 48))
    # dague (0,104) 80x18
    d.polygon([(4, 112), (50, 108), (56, 112), (50, 116)], fill=(196, 200, 210), outline=(100, 104, 114))
    d.line((8, 112, 50, 112), fill=(236, 240, 248))
    d.rectangle((54, 104, 58, 120), fill=(160, 120, 40))
    d.rectangle((58, 109, 74, 115), fill=(90, 50, 30))
    for x in range(60, 74, 3):
        d.line((x, 109, x, 115), fill=(60, 34, 20))
    d.ellipse((73, 108, 79, 116), fill=(180, 140, 50))
    # halo de bougie (128,0) 96x96, très doux
    px = im.load()
    for y in range(96):
        for x in range(96):
            r = math.hypot(x - 47.5, y - 47.5) / 48
            if r < 1:
                a = int(70 * (1 - r) ** 2)
                px[128 + x, y] = (255, 190, 90, a)
    return im


if __name__ == "__main__":
    os.makedirs(SORTIE, exist_ok=True)
    for nom, f in (("table", table), ("inventaire", panneau), ("carnet", carnet), ("onglets", onglets), ("decor", decor)):
        f().save(os.path.join(SORTIE, nom + ".png"))
        print("ok", nom)
