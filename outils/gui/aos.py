# -*- coding: utf-8 -*-
"""Charte « or de Sigmar sur bleu nuit » : emblèmes des 25 factions, ornements de cadre, jauge arcanique,
icônes des 8 Vents. Sortie : assets/royaumes/textures/gui/aos/*.png"""
import math
import os
from PIL import Image, ImageDraw

ICI = os.path.dirname(os.path.abspath(__file__))
SORTIE = os.path.join(ICI, "..", "..", "src", "main", "resources", "assets", "royaumes", "textures", "gui", "aos")
OR, OR_C, OR_S = (212, 166, 58), (242, 210, 122), (140, 104, 34)
NUIT, AZYR = (14, 26, 51), (44, 90, 160)

# faction -> (couleur du blason, couleur du symbole, symbole)
EMBLEMES = [
    ("stormcast", (40, 74, 150), OR, "comete"), ("cites", (168, 40, 32), (232, 214, 172), "losange"),
    ("fyreslayers", (200, 90, 30), OR_C, "rune"), ("kharadron", (88, 40, 72), (214, 186, 120), "engrenage"),
    ("khaine", (100, 30, 50), (226, 206, 206), "dague"), ("idoneth", (40, 72, 82), (232, 112, 52), "vague"),
    ("lumineth", (238, 238, 242), OR, "soleil"), ("seraphon", (30, 110, 140), OR_C, "etoile"),
    ("sylvaneth", (70, 100, 40), (150, 232, 240), "feuille"), ("esclaves", (30, 30, 36), OR, "chaos"),
    ("khorne", (130, 32, 30), (172, 122, 62), "khorne"), ("tzeentch", (40, 110, 170), (120, 230, 255), "oeil"),
    ("slaanesh", (112, 52, 112), (214, 150, 206), "slaanesh"), ("nurgle", (68, 88, 58), (190, 230, 60), "nurgle"),
    ("skaven", (120, 30, 30), (80, 255, 60), "rat"), ("hashut", (40, 40, 44), (255, 140, 40), "taureau"),
    ("nighthaunt", (40, 80, 80), (190, 228, 218), "capuche"), ("soulblight", (110, 20, 26), OR, "couronne"),
    ("ossiarch", (44, 54, 96), (218, 204, 168), "crane"), ("fec", (90, 60, 50), (166, 186, 150), "couronne_sang"),
    ("ironjawz", (226, 184, 34), (40, 40, 44), "poing"), ("kruleboyz", (60, 70, 40), (190, 40, 30), "oeil_rouge"),
    ("gitz", (30, 30, 40), (230, 210, 60), "lune"), ("ogors", (160, 40, 40), (230, 220, 200), "gueule"),
    ("behemat", (110, 120, 70), (222, 170, 146), "pied"),
]
VENTS = [("azyr", (90, 160, 255)), ("aqshy", (255, 110, 30)), ("ghur", (170, 110, 60)), ("ghyran", (90, 220, 90)),
         ("hysh", (255, 250, 200)), ("ulgu", (110, 100, 150)), ("shyish", (170, 110, 220)), ("chamon", (230, 190, 60))]


def symbole(d, sym, c, cx, cy, r):
    if sym == "comete":
        d.polygon([(cx, cy - r), (cx + 3, cy - 3), (cx + r, cy), (cx + 3, cy + 3), (cx, cy + r), (cx - 3, cy + 3), (cx - r, cy), (cx - 3, cy - 3)], fill=c)
        d.line((cx + 3, cy + 3, cx + r + 2, cy + r + 2), fill=c, width=2)
    elif sym == "losange":
        d.polygon([(cx, cy - r), (cx + r - 2, cy), (cx, cy + r), (cx - r + 2, cy)], fill=c)
        d.rectangle((cx - 1, cy - 2, cx + 1, cy + 2), fill=(60, 20, 16))
    elif sym == "rune":
        d.line((cx - 4, cy - r, cx - 4, cy + r), fill=c, width=3)
        d.line((cx - 4, cy - 2, cx + 5, cy - r), fill=c, width=3)
        d.line((cx - 4, cy + 2, cx + 5, cy + r), fill=c, width=3)
    elif sym == "engrenage":
        for k in range(8):
            a = k * math.pi / 4
            d.rectangle((cx + math.cos(a) * r - 2, cy + math.sin(a) * r - 2, cx + math.cos(a) * r + 2, cy + math.sin(a) * r + 2), fill=c)
        d.ellipse((cx - r + 2, cy - r + 2, cx + r - 2, cy + r - 2), fill=c)
        d.ellipse((cx - 3, cy - 3, cx + 3, cy + 3), fill=(150, 220, 255))
    elif sym == "dague":
        d.polygon([(cx, cy - r), (cx + 3, cy + 3), (cx - 3, cy + 3)], fill=c)
        d.rectangle((cx - 6, cy + 3, cx + 6, cy + 5), fill=c)
        d.rectangle((cx - 1, cy + 5, cx + 1, cy + r), fill=c)
    elif sym == "vague":
        for k in range(3):
            d.arc((cx - r + k * 4 - 4, cy - 6 + k * 3, cx + k * 4, cy + 4 + k * 3), 180, 360, fill=c, width=2)
    elif sym == "soleil":
        for k in range(12):
            a = k * math.pi / 6
            d.line((cx, cy, cx + math.cos(a) * r, cy + math.sin(a) * r), fill=c, width=2)
        d.ellipse((cx - 5, cy - 5, cx + 5, cy + 5), fill=c)
    elif sym == "etoile":
        pts = []
        for k in range(10):
            a = -math.pi / 2 + k * math.pi / 5
            rr = r if k % 2 == 0 else r * 0.45
            pts.append((cx + math.cos(a) * rr, cy + math.sin(a) * rr))
        d.polygon(pts, fill=c)
    elif sym == "feuille":
        d.ellipse((cx - 5, cy - r, cx + 5, cy + r - 2), fill=c)
        d.line((cx, cy - r + 2, cx, cy + r), fill=(40, 70, 30), width=1)
    elif sym == "chaos":
        for k in range(8):
            a = k * math.pi / 4
            d.line((cx, cy, cx + math.cos(a) * r, cy + math.sin(a) * r), fill=c, width=2)
            d.polygon([(cx + math.cos(a) * (r + 1), cy + math.sin(a) * (r + 1)), (cx + math.cos(a + 0.35) * (r - 4), cy + math.sin(a + 0.35) * (r - 4)),
                       (cx + math.cos(a - 0.35) * (r - 4), cy + math.sin(a - 0.35) * (r - 4))], fill=c)
        d.ellipse((cx - 3, cy - 3, cx + 3, cy + 3), fill=c)
    elif sym == "khorne":
        d.rectangle((cx - r + 2, cy - r + 2, cx + r - 2, cy - r + 5), fill=c)
        d.line((cx - 5, cy - r + 5, cx + 4, cy + 2), fill=c, width=3)
        d.line((cx + 5, cy - r + 5, cx - 4, cy + 2), fill=c, width=3)
        d.rectangle((cx - r + 2, cy + r - 5, cx + r - 2, cy + r - 2), fill=c)
        d.line((cx, cy + 2, cx, cy + r - 5), fill=c, width=3)
    elif sym == "oeil":
        d.ellipse((cx - r, cy - 6, cx + r, cy + 6), fill=c)
        d.ellipse((cx - 4, cy - 4, cx + 4, cy + 4), fill=(20, 40, 90))
        d.ellipse((cx - 1, cy - 1, cx + 1, cy + 1), fill=(255, 255, 255))
    elif sym == "slaanesh":
        d.ellipse((cx - 6, cy - r + 2, cx + 6, cy + 2), outline=c, width=3)
        d.line((cx, cy + 2, cx, cy + r), fill=c, width=3)
        d.line((cx - 5, cy + r - 4, cx + 5, cy + r - 4), fill=c, width=2)
    elif sym == "nurgle":
        for (dx, dy) in ((-5, -3), (5, -3), (0, 5)):
            d.ellipse((cx + dx - 5, cy + dy - 5, cx + dx + 5, cy + dy + 5), outline=c, width=2)
    elif sym == "rat":
        d.polygon([(cx, cy - r), (cx + r, cy + r - 2), (cx - r, cy + r - 2)], outline=c, width=2)
        d.line((cx - 6, cy + 2, cx + 6, cy + 2), fill=c, width=2)
        d.line((cx, cy - 4, cx, cy + 8), fill=c, width=2)
    elif sym == "taureau":
        d.rectangle((cx - 6, cy - 4, cx + 6, cy + r - 2), fill=c)
        d.arc((cx - r, cy - r, cx - 2, cy + 2), 180, 300, fill=c, width=3)
        d.arc((cx + 2, cy - r, cx + r, cy + 2), 240, 360, fill=c, width=3)
        d.rectangle((cx - 3, cy + 4, cx + 3, cy + 7), fill=(40, 40, 44))
    elif sym == "capuche":
        d.polygon([(cx, cy - r), (cx + r - 2, cy + r), (cx - r + 2, cy + r)], fill=c)
        d.ellipse((cx - 5, cy - 3, cx + 5, cy + 7), fill=(20, 40, 40))
        d.rectangle((cx - 3, cy + 1, cx - 2, cy + 2), fill=(160, 255, 230))
        d.rectangle((cx + 2, cy + 1, cx + 3, cy + 2), fill=(160, 255, 230))
    elif sym in ("couronne", "couronne_sang"):
        d.polygon([(cx - r, cy + 6), (cx - r, cy - 6), (cx - 5, cy), (cx, cy - r), (cx + 5, cy), (cx + r, cy - 6), (cx + r, cy + 6)], fill=c)
        if sym == "couronne_sang":
            d.rectangle((cx - 1, cy + 6, cx + 1, cy + r), fill=(170, 20, 20))
    elif sym == "crane":
        d.ellipse((cx - r + 2, cy - r, cx + r - 2, cy + 4), fill=c)
        d.rectangle((cx - 5, cy + 2, cx + 5, cy + r - 2), fill=c)
        d.rectangle((cx - 6, cy - 4, cx - 2, cy), fill=(30, 40, 60))
        d.rectangle((cx + 2, cy - 4, cx + 6, cy), fill=(30, 40, 60))
    elif sym == "poing":
        d.rectangle((cx - 8, cy - 6, cx + 8, cy + 8), fill=c)
        for k in range(4):
            d.line((cx - 8 + k * 4, cy - 6, cx - 8 + k * 4, cy), fill=(226, 184, 34))
        d.rectangle((cx - 10, cy - 2, cx - 7, cy + 6), fill=c)
    elif sym == "oeil_rouge":
        d.ellipse((cx - r, cy - 7, cx + r, cy + 7), fill=c)
        d.rectangle((cx - 1, cy - 6, cx + 1, cy + 6), fill=(20, 20, 20))
    elif sym == "lune":
        d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=c)
        d.ellipse((cx - 5, cy - 6, cx - 1, cy - 2), fill=(30, 30, 40))
        d.ellipse((cx + 2, cy - 6, cx + 6, cy - 2), fill=(30, 30, 40))
        d.arc((cx - 7, cy - 2, cx + 7, cy + 8), 20, 160, fill=(30, 30, 40), width=2)
    elif sym == "gueule":
        d.ellipse((cx - r, cy - r + 2, cx + r, cy + r - 2), fill=c)
        d.rectangle((cx - 8, cy - 1, cx + 8, cy + 3), fill=(90, 20, 20))
        for k in range(4):
            d.polygon([(cx - 8 + k * 4, cy - 1), (cx - 6 + k * 4, cy + 2), (cx - 4 + k * 4, cy - 1)], fill=(240, 230, 210))
    elif sym == "pied":
        d.ellipse((cx - 6, cy - 4, cx + 6, cy + r), fill=c)
        for k in range(4):
            d.ellipse((cx - 8 + k * 4, cy - r, cx - 5 + k * 4, cy - r + 4), fill=c)


def blason(sym, fond, c, taille=32):
    im = Image.new("RGBA", (taille * 4, taille * 4), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    T = taille * 4
    pts = [(8, 8), (T - 8, 8), (T - 8, T * 0.55), (T / 2, T - 6), (8, T * 0.55)]
    d.polygon(pts, fill=OR_S)
    d.polygon([(14, 14), (T - 14, 14), (T - 14, T * 0.54), (T / 2, T - 16), (14, T * 0.54)], fill=OR)
    d.polygon([(22, 22), (T - 22, 22), (T - 22, T * 0.52), (T / 2, T - 28), (22, T * 0.52)], fill=fond)
    sm = Image.new("RGBA", (40, 40), (0, 0, 0, 0))
    symbole(ImageDraw.Draw(sm), sym, c, 20, 19, 13)
    sm = sm.resize((80, 80), Image.NEAREST)
    im.alpha_composite(sm, (T // 2 - 40, T // 2 - 46))
    return im.resize((taille, taille), Image.LANCZOS)


def emblemes():
    at = Image.new("RGBA", (256, 128), (0, 0, 0, 0))
    for i, (fid, fond, c, sym) in enumerate(EMBLEMES):
        at.alpha_composite(blason(sym, fond, c), ((i % 8) * 32, (i // 8) * 32))
    return at


def ornements():
    """256x64 : coins en comète (4 x 16x16), bouton (normal, survol, actif : 3 x 64x20), bandeau de titre."""
    im = Image.new("RGBA", (256, 64), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    for k in range(4):
        x0 = k * 16
        c = Image.new("RGBA", (16, 16), (0, 0, 0, 0))
        dc = ImageDraw.Draw(c)
        dc.line((0, 0, 15, 0), fill=OR)
        dc.line((0, 0, 0, 15), fill=OR)
        dc.line((2, 2, 11, 2), fill=OR_S)
        dc.line((2, 2, 2, 11), fill=OR_S)
        dc.polygon([(4, 1), (6, 4), (9, 4), (6, 6), (7, 9), (4, 7), (1, 9), (2, 6), (0, 4), (3, 4)], fill=OR_C)
        dc.point((4, 4), fill=(255, 255, 255))
        c = [c, c.transpose(Image.FLIP_LEFT_RIGHT), c.transpose(Image.FLIP_TOP_BOTTOM),
             c.transpose(Image.ROTATE_180)][k]
        im.alpha_composite(c, (x0, 0))
    for k, (fond, bord) in enumerate((((24, 40, 72), OR), ((40, 66, 110), OR_C), ((60, 44, 20), OR_C))):
        x0, y0 = 64 + k * 64, 0
        d.rectangle((x0, y0, x0 + 63, y0 + 19), fill=fond, outline=bord)
        d.rectangle((x0 + 1, y0 + 1, x0 + 62, y0 + 1), fill=tuple(min(255, v + 30) for v in fond))
        d.rectangle((x0 + 2, y0 + 2, x0 + 61, y0 + 17), outline=OR_S)
        for (px_, py_) in ((x0 + 3, y0 + 3), (x0 + 60, y0 + 3), (x0 + 3, y0 + 16), (x0 + 60, y0 + 16)):
            d.point((px_, py_), fill=OR_C)
    # bandeau de titre 160x24 en (0,24)
    d.rectangle((8, 26, 151, 45), fill=AZYR, outline=OR)
    d.polygon([(0, 30), (8, 26), (8, 45), (0, 41), (4, 36)], fill=OR_S)
    d.polygon([(159, 30), (151, 26), (151, 45), (159, 41), (155, 36)], fill=OR_S)
    d.line((10, 28, 149, 28), fill=(80, 130, 200))
    return im


def hud():
    """256x64 : cadre de jauge 104x12 (0,0), remplissage 100x8 (0,16), icône d'énergie 12x12 (112,0),
    icônes des 8 Vents 16x16 (0,32 ...)."""
    im = Image.new("RGBA", (256, 64), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rectangle((0, 0, 103, 11), fill=(10, 16, 34, 220), outline=OR)
    d.rectangle((1, 1, 102, 10), outline=OR_S)
    for x in (0, 103):
        d.point((x, 0), fill=OR_C)
        d.point((x, 11), fill=OR_C)
    for x in range(100):
        t = x / 99
        c = (int(123 + (69 - 123) * t), int(92 + (200 - 92) * t), 255)
        for y in range(8):
            k = 1.15 if y < 2 else (0.85 if y > 5 else 1.0)
            im.putpixel((x, 16 + y), tuple(min(255, int(v * k)) for v in c) + (255,))
    # icône : losange arcanique
    d.polygon([(118, 0), (123, 6), (118, 11), (113, 6)], fill=(123, 92, 255), outline=OR_C)
    d.point((117, 4), fill=(255, 255, 255))
    for i, (v, c) in enumerate(VENTS):
        x0, y0 = i * 16, 32
        d.ellipse((x0 + 1, y0 + 1, x0 + 14, y0 + 14), fill=(14, 26, 51), outline=OR)
        d.ellipse((x0 + 4, y0 + 4, x0 + 11, y0 + 11), fill=c)
        d.point((x0 + 6, y0 + 6), fill=(255, 255, 255))
    return im


if __name__ == "__main__":
    os.makedirs(SORTIE, exist_ok=True)
    emblemes().save(os.path.join(SORTIE, "emblemes.png"))
    ornements().save(os.path.join(SORTIE, "ornements.png"))
    hud().save(os.path.join(SORTIE, "hud.png"))
    big = emblemes().resize((1024, 512), Image.NEAREST)
    os.makedirs(os.path.join(ICI, "apercus"), exist_ok=True)
    big.save(os.path.join(ICI, "apercus", "emblemes_x4.png"))
    print("ok")
