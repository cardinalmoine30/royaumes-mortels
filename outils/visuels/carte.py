# -*- coding: utf-8 -*-
"""Carte des Royaumes Mortels (aide visuelle) : Célestis au-dessus, sept Royaumes en anneau, les Huit-Voies au centre."""
import math, os, random
from PIL import Image, ImageDraw, ImageFilter, ImageFont

ICI = os.path.dirname(os.path.abspath(__file__))
W, H = 1600, 1240
F = "/usr/share/fonts/truetype/dejavu/"
fb = lambda n: ImageFont.truetype(F + "DejaVuSerif-Bold.ttf", n)
fr = lambda n: ImageFont.truetype(F + "DejaVuSans.ttf", n)
OR, OR_C, OR_S = (212, 166, 58), (242, 210, 122), (140, 104, 34)
R = random.Random(3)
ROY = [  # nom, vent, couleur, dimension, lignes — dans le sens horaire après Célestis
    ("Lumina", "Royaume de la Lumière", (250, 238, 180), "royaumes:hysh", ["Îles flottantes, plateaux", "de Lumière, Astrosauriens"]),
    ("Umbria", "Royaume de l'Ombre", (120, 110, 160), "royaumes:ulgu", ["Brumes, mer d'ombre", "Morvaine, Abyssal"]),
    ("Nécréa", "Royaume de la Mort", (156, 96, 206), "royaumes:shyish", ["Sables d'os, terres mortes", "Vampires, Hantise Nocturne, Faucheurs d'Os"]),
    ("Ferrumia", "Royaume du Métal", (224, 184, 56), "royaumes:chamon", ["Collines de métal, désert doré", "Nuées, Vharys"]),
    ("Pyréa", "Royaume du Feu", (232, 86, 32), "royaumes:aqshy", ["Plaines de cendres, volcans", "Tueurs-de-Braise, Sangrath"]),
    ("Féralia", "Royaume des Bêtes", (176, 116, 62), "royaumes:ghur", ["Jungle, savane, terres sauvages", "Orcs, Ogres, Géants"]),
    ("Sylvéa", "Royaume de la Vie", (86, 196, 86), "royaumes:ghyran", ["Forêts de jade, marais", "Sylvains, Morbus"]),
]
AZYR = ("Célestis", "Royaume des Cieux", (96, 160, 255), "royaumes:royaumes_mortels", ["Cimes et vallées d'Célestis", "Foudroyés, Cités d'Aurion"])

im = Image.new("RGB", (W, H), (10, 18, 38))
px = im.load()
for y in range(H):
    for x in range(0, W):
        dx, dy = (x - W / 2) / W, (y - H / 2) / H
        k = 1 - 0.55 * (dx * dx + dy * dy) * 2.2
        px[x, y] = (int(14 * k), int(24 * k), int(50 * k))
neb = Image.new("RGBA", (W, H), (0, 0, 0, 0))
dn = ImageDraw.Draw(neb)
for _ in range(16):
    x, y, r = R.randint(0, W), R.randint(0, H), R.randint(120, 300)
    c = R.choice([(60, 40, 110), (30, 70, 130), (90, 30, 60)])
    dn.ellipse((x - r, y - r, x + r, y + r), fill=c + (38,))
neb = neb.filter(ImageFilter.GaussianBlur(70))
im = Image.alpha_composite(im.convert("RGBA"), neb)
d = ImageDraw.Draw(im)
for _ in range(900):
    x, y = R.randint(0, W - 1), R.randint(0, H - 1)
    b = R.randint(90, 255)
    d.point((x, y), fill=(b, b, min(255, b + 20)))
CX, CY, RX, RY = W // 2, 620, 520, 400
pos = []
for i in range(1, 8):
    a = math.radians(270 + 45 * i)
    pos.append((CX + math.cos(a) * RX, CY + math.sin(a) * RY))
AZ = (CX, CY - RY)
lignes = Image.new("RGBA", (W, H), (0, 0, 0, 0))
dl = ImageDraw.Draw(lignes)
def pointille(a, b, c, w=2, pas=14):
    L = math.dist(a, b); n = int(L // pas)
    for k in range(n):
        if k % 2 == 0:
            t0, t1 = k / n, min(1, (k + 1) / n)
            dl.line((a[0] + (b[0] - a[0]) * t0, a[1] + (b[1] - a[1]) * t0, a[0] + (b[0] - a[0]) * t1, a[1] + (b[1] - a[1]) * t1), fill=c, width=w)
anneau = [AZ] + pos
for i, p in enumerate(anneau):
    pointille(p, (CX, CY), (212, 166, 58, 150))
    pointille(p, anneau[(i + 1) % 8], (180, 190, 220, 90), 1, 10)
im = Image.alpha_composite(im, lignes)
d = ImageDraw.Draw(im)

def disque(cx, cy, r, c, halo=True):
    g = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    dg = ImageDraw.Draw(g)
    if halo:
        dg.ellipse((cx - r * 1.7, cy - r * 1.7, cx + r * 1.7, cy + r * 1.7), fill=c + (70,))
    g = g.filter(ImageFilter.GaussianBlur(r * 0.45))
    base = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    db = ImageDraw.Draw(base)
    for k in range(int(r), 0, -1):
        t = k / r
        col = tuple(int(v * (0.55 + 0.45 * (1 - t)) + 30 * (1 - t)) for v in c)
        db.ellipse((cx - k - (1 - t) * r * 0.12, cy - k - (1 - t) * r * 0.12, cx + k - (1 - t) * r * 0.12, cy + k - (1 - t) * r * 0.12), fill=col + (255,))
    db.ellipse((cx - r, cy - r, cx + r, cy + r), outline=OR, width=4)
    db.ellipse((cx - r - 7, cy - r - 7, cx + r + 7, cy + r + 7), outline=OR_S, width=2)
    return Image.alpha_composite(g, base)

def etiquette(cx, y, nom, vent, lignes_, c):
    for (t, f, col, dy) in ((nom, fb(30), OR_C, 0), (vent, fr(17), (230, 230, 240), 38)):
        w = d.textlength(t, font=f)
        d.text((cx - w / 2 + 2, y + dy + 2), t, font=f, fill=(0, 0, 0))
        d.text((cx - w / 2, y + dy), t, font=f, fill=col)
    for k, t in enumerate(lignes_):
        w = d.textlength(t, font=fr(15))
        d.text((cx - w / 2, y + 62 + k * 20), t, font=fr(15), fill=(190, 196, 215))

# Huit-Voies
im = Image.alpha_composite(im, disque(CX, CY, 92, (150, 30, 30)))
d = ImageDraw.Draw(im)
for k in range(8):
    a = k * math.pi / 4
    x2, y2 = CX + math.cos(a) * 70, CY + math.sin(a) * 70
    d.line((CX, CY, x2, y2), fill=(255, 200, 120), width=5)
    d.polygon([(CX + math.cos(a) * 82, CY + math.sin(a) * 82), (CX + math.cos(a + 0.25) * 62, CY + math.sin(a + 0.25) * 62),
               (CX + math.cos(a - 0.25) * 62, CY + math.sin(a - 0.25) * 62)], fill=(255, 200, 120))
d.ellipse((CX - 14, CY - 14, CX + 14, CY + 14), fill=(255, 210, 140))
etiquette(CX, CY + 112, "Les Huit-Voies", "Terre du Chaos, carrefour des Royaumes", ["Forteresses du Chaos, Hommes-Rats, boss", "royaumes:huit_points"], None)
# Célestis
im = Image.alpha_composite(im, disque(AZ[0], AZ[1], 78, AZYR[2]))
d = ImageDraw.Draw(im)
d.polygon([(AZ[0], AZ[1] - 50), (AZ[0] + 12, AZ[1] - 12), (AZ[0] + 50, AZ[1]), (AZ[0] + 12, AZ[1] + 12), (AZ[0], AZ[1] + 50),
           (AZ[0] - 12, AZ[1] + 12), (AZ[0] - 50, AZ[1]), (AZ[0] - 12, AZ[1] - 12)], fill=(240, 248, 255))
etiquette(AZ[0], AZ[1] + 92, AZYR[0], AZYR[1] + ", le Royaume de Aurion", AZYR[4] + [AZYR[3]], None)
# sept Royaumes
SYM = {"Pyréa": "flamme", "Féralia": "croc", "Sylvéa": "feuille", "Lumina": "soleil", "Umbria": "lune", "Nécréa": "sablier", "Ferrumia": "engrenage"}
for (nom, vent, c, dim, lig), (x, y) in zip(ROY, pos):
    im = Image.alpha_composite(im, disque(x, y, 62, c))
    d = ImageDraw.Draw(im)
    s = SYM[nom]
    w = (255, 255, 255)
    if s == "flamme":
        d.polygon([(x, y - 34), (x + 18, y + 6), (x + 8, y + 26), (x - 8, y + 26), (x - 18, y + 6)], fill=(255, 220, 120))
        d.polygon([(x, y - 10), (x + 8, y + 10), (x, y + 22), (x - 8, y + 10)], fill=(255, 250, 220))
    elif s == "croc":
        d.polygon([(x - 26, y - 20), (x + 26, y - 20), (x, y + 32)], fill=(245, 235, 210))
    elif s == "feuille":
        d.ellipse((x - 16, y - 32, x + 16, y + 30), fill=(200, 255, 190))
        d.line((x, y - 28, x, y + 30), fill=(60, 120, 50), width=3)
    elif s == "soleil":
        for k in range(12):
            a = k * math.pi / 6
            d.line((x, y, x + math.cos(a) * 36, y + math.sin(a) * 36), fill=(255, 255, 255), width=4)
        d.ellipse((x - 16, y - 16, x + 16, y + 16), fill=(255, 250, 220))
    elif s == "lune":
        d.ellipse((x - 28, y - 28, x + 28, y + 28), fill=(230, 230, 250))
        d.ellipse((x - 14, y - 34, x + 38, y + 18), fill=c)
    elif s == "sablier":
        d.polygon([(x - 22, y - 30), (x + 22, y - 30), (x, y), (x + 22, y + 30), (x - 22, y + 30), (x, y)], fill=(240, 230, 255))
    elif s == "engrenage":
        for k in range(8):
            a = k * math.pi / 4
            d.rectangle((x + math.cos(a) * 28 - 6, y + math.sin(a) * 28 - 6, x + math.cos(a) * 28 + 6, y + math.sin(a) * 28 + 6), fill=(255, 245, 200))
        d.ellipse((x - 26, y - 26, x + 26, y + 26), fill=(255, 245, 200))
        d.ellipse((x - 9, y - 9, x + 9, y + 9), fill=c)
    ty = y + 78 if y > CY - 40 else y - 178
    etiquette(x, ty, nom, vent, lig + [dim], c)
# cadre doré et titre
d.rectangle((8, 8, W - 9, H - 9), outline=OR, width=5)
d.rectangle((20, 20, W - 21, H - 21), outline=OR_S, width=2)
t = "Les Royaumes Mortels"
d.text((48, 36), t, font=fb(44), fill=OR_C)
d.text((50, 92), "Neuf mondes à explorer dans le mod", font=fr(20), fill=(210, 215, 230))
leg = ["— — —  Portail des Royaumes : chaque Royaume relie les Huit-Voies",
       "Voyager : Pierre de Royaume, Failles, bloc Portail des Royaumes (carte de voyage)",
       "Dans le Royaume de son Vent, un sort coûte deux fois moins d'énergie"]
for k, l in enumerate(leg):
    w = d.textlength(l, font=fr(16))
    d.text((W - 48 - w, 40 + k * 24), l, font=fr(16), fill=(220, 210, 170))
os.makedirs(os.path.join(ICI, "apercus"), exist_ok=True)
im.convert("RGB").save(os.path.join(ICI, "apercus", "carte_royaumes.png"))
print("ok")
