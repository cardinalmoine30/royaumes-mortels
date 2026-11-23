# -*- coding: utf-8 -*-
"""Maquettes fidèles des écrans du mod (mêmes cotes que le code Java) :
 - maquette_serment.png : écran de serment (choix de faction + aperçu du skin)
 - maquette_hud.png     : HUD en jeu (jauge arcanique, emblème, nom du Royaume)
Les cotes sont en « pixels d'interface » Minecraft ; l'image est rendue à l'échelle K."""
import os
import sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter

ICI = os.path.dirname(os.path.abspath(__file__))
RACINE = os.path.join(ICI, "..", "..")
TEX = os.path.join(RACINE, "src", "main", "resources", "assets", "royaumes", "textures")
sys.path.insert(0, os.path.join(ICI, ".."))
from donnees_factions import FACTIONS, ALLIANCES  # noqa: E402

K = 3
F = "/usr/share/fonts/truetype/dejavu/"
OR, OR_C, NUIT, PARCH, ENCRE = (212, 166, 58), (242, 210, 122), (14, 26, 51), (230, 211, 168), (74, 46, 20)
VERT, ROUGE = (126, 200, 110), (220, 96, 80)
EMB = Image.open(os.path.join(TEX, "gui", "aos", "emblemes.png")).convert("RGBA")
ORN = Image.open(os.path.join(TEX, "gui", "aos", "ornements.png")).convert("RGBA")
HUD = Image.open(os.path.join(TEX, "gui", "aos", "hud.png")).convert("RGBA")


def police(t, gras=False, serif=True):
    nom = ("DejaVuSerif-Bold.ttf" if gras else "DejaVuSerif.ttf") if serif else ("DejaVuSans-Bold.ttf" if gras else "DejaVuSans.ttf")
    return ImageFont.truetype(F + nom, t * K)


def coller(img, src, x, y, w=None, h=None):
    w, h = w or src.width, h or src.height
    img.alpha_composite(src.resize((int(round(w * K)), int(round(h * K))), Image.NEAREST), (int(round(x * K)), int(round(y * K))))


def embleme(i):
    return EMB.crop(((i % 8) * 32, (i // 8) * 32, (i % 8) * 32 + 32, (i // 8) * 32 + 32))


def cadre_or(d, x, y, w, h, fond=None, ep=1):
    if fond:
        d.rectangle((x * K, y * K, (x + w) * K - 1, (y + h) * K - 1), fill=fond)
    d.rectangle((x * K, y * K, (x + w) * K - 1, (y + h) * K - 1), outline=OR, width=ep * K)
    d.rectangle(((x + 2) * K, (y + 2) * K, (x + w - 2) * K - 1, (y + h - 2) * K - 1), outline=(120, 92, 36), width=max(1, K // 2))


def coins(img, x, y, w, h):
    for k, (cx, cy) in enumerate(((x - 4, y - 4), (x + w - 12, y - 4), (x - 4, y + h - 12), (x + w - 12, y + h - 12))):
        coller(img, ORN.crop((k * 16, 0, k * 16 + 16, 16)), cx, cy)


def texte(d, x, y, s, t=8, c=OR_C, gras=False, centre=False, serif=True, ombre=True):
    f = police(t, gras, serif)
    if centre:
        x = x - d.textlength(s, font=f) / K / 2
    if ombre:
        d.text((x * K + K, y * K + K), s, font=f, fill=(0, 0, 0))
    d.text((x * K, y * K), s, font=f, fill=c)


def paragraphe(d, x, y, s, larg, t=7, c=PARCH, inter=9):
    f = police(t, False, False)
    mots, ligne = s.split(), ""
    for m in mots:
        essai = (ligne + " " + m).strip()
        if d.textlength(essai, font=f) / K > larg and ligne:
            texte(d, x, y, ligne, t, c, serif=False)
            y += inter
            ligne = m
        else:
            ligne = essai
    if ligne:
        texte(d, x, y, ligne, t, c, serif=False)
        y += inter
    return y


def poupee(skin, x, y, e):
    """Skin plat vu de face (comme EcranSerment.dessinerPoupee)."""
    pieces = [((8, 8, 8, 8), (4, 0)), ((20, 20, 8, 12), (4, 8)), ((44, 20, 4, 12), (0, 8)), ((36, 52, 4, 12), (12, 8)),
              ((4, 20, 4, 12), (4, 20)), ((20, 52, 4, 12), (8, 20)), ((40, 8, 8, 8), (4, 0))]
    for (u, v, w, h), (dx, dy) in pieces:
        p = skin.crop((u, v, u + w, v + h))
        coller(img_courante[0], p, x + dx * e, y + dy * e, w * e, h * e)


img_courante = [None]


def fond_nuit(W, H):
    img = Image.new("RGBA", (W * K, H * K), NUIT + (255,))
    d = ImageDraw.Draw(img)
    for i in range(H * K):
        t = i / (H * K)
        c = tuple(int(a + (b - a) * t) for a, b in zip((22, 38, 72), (6, 10, 22)))
        d.line((0, i, W * K, i), fill=c)
    return img


# ----------------------------------------------------------------------------------- écran de serment
def serment(choix=0, survol=11):
    W, H = 480, 270
    img = fond_nuit(W, H)
    img_courante[0] = img
    d = ImageDraw.Draw(img)
    # éclairs d'Azyr discrets en fond
    for x0 in (60, 400):
        pts = [(x0, 0), (x0 + 8, 40), (x0 - 4, 70), (x0 + 10, 120)]
        d.line([(a * K, b * K) for a, b in pts], fill=(44, 90, 160), width=K)
    PW, PH = 400, 236
    px, py = (W - PW) // 2, (H - PH) // 2
    cadre_or(d, px, py, PW, PH, fond=(12, 20, 40, 235))
    coins(img, px, py, PW, PH)
    # bannière de titre
    coller(img, ORN.crop((0, 24, 160, 48)), px + PW // 2 - 80, py - 10)
    texte(d, px + PW // 2, py - 4, "SERMENT D'ALLÉGEANCE", 8, OR_C, gras=True, centre=True)
    # colonne des alliances
    y = py + 20
    for nom, couleur, ids in ALLIANCES:
        texte(d, px + 12, y, nom.upper(), 7, couleur, gras=True)
        d.line(((px + 12) * K, (y + 10) * K, (px + 200) * K, (y + 10) * K), fill=couleur, width=K // 2 + 1)
        for j, num in enumerate(ids):
            ex, ey = px + 12 + j * 21, y + 14
            if num == survol or num == choix:
                d.rectangle(((ex - 2) * K, (ey - 2) * K, (ex + 22) * K - 1, (ey + 22) * K - 1), fill=(60, 48, 20), outline=OR_C if num == survol else OR, width=K)
            coller(img, embleme(num - 1), ex, ey, 20, 20)
        y += 46
    texte(d, px + 12, py + PH - 22, "Survole un blason pour lire son serment.", 6, (160, 170, 200), serif=False)
    texte(d, px + 12, py + PH - 13, "Touche J : rouvrir cet écran.", 6, (160, 170, 200), serif=False)
    # panneau de la faction survolée
    f = FACTIONS[survol - 1]
    qx, qy, qw, qh = px + 210, py + 18, 180, PH - 28
    cadre_or(d, qx, qy, qw, qh, fond=(24, 30, 52))
    skin = Image.open(os.path.join(TEX, "skin", f["id"] + ".png")).convert("RGBA")
    al = [a for a in ALLIANCES if survol in a[2]][0]
    texte(d, qx + qw / 2, qy + 6, f["nom"], 8, OR_C, gras=True, centre=True)
    texte(d, qx + qw / 2, qy + 18, al[0] + " · " + f["royaume"], 6, al[1], centre=True, serif=False)
    d.rectangle(((qx + 8) * K, (qy + 28) * K, (qx + 60) * K, (qy + 116) * K), fill=(10, 16, 32), outline=(120, 92, 36), width=K // 2 + 1)
    poupee(skin, qx + 14, qy + 32, 2.5)
    coller(img, embleme(survol - 1), qx + 66, qy + 28, 24, 24)
    yy = paragraphe(d, qx + 66, qy + 56, f["desc"], 106, 6, PARCH, 8)
    yy = qy + 122
    texte(d, qx + 8, yy, "Dons", 7, VERT, gras=True)
    yy = paragraphe(d, qx + 8, yy + 10, f["bonus"], qw - 16, 6, (200, 230, 190), 8)
    texte(d, qx + 8, yy + 2, "Fardeau", 7, ROUGE, gras=True)
    yy = paragraphe(d, qx + 8, yy + 12, f["malus"], qw - 16, 6, (240, 190, 180), 8)
    # bouton
    bx, by = qx + qw // 2 - 60, qy + qh - 28
    coller(img, ORN.crop((128, 0, 192, 20)), bx, by, 120, 20)
    texte(d, bx + 60, by + 5, "Prêter serment", 8, OR_C, gras=True, centre=True)
    return img


# ----------------------------------------------------------------------------------- HUD en jeu
def hud(num=21, energie=72, maxi=135, vent=2):
    W, H = 480, 270
    img = Image.new("RGBA", (W * K, H * K))
    d = ImageDraw.Draw(img)
    # décor : ciel de Ghur et plaine
    for i in range(H * K):
        t = i / (H * K)
        c = tuple(int(a + (b - a) * t) for a, b in zip((206, 140, 90), (240, 200, 150))) if t < 0.55 else (92, 120, 52)
        d.line((0, i, W * K, i), fill=c)
    import random
    R = random.Random(4)
    for _ in range(14):
        x, h = R.randint(0, W), R.randint(30, 80)
        d.polygon([((x - 40) * K, int(H * 0.55) * K), (x * K, (int(H * 0.55) - h) * K), ((x + 40) * K, int(H * 0.55) * K)], fill=(120, 84, 60))
    for _ in range(300):
        x, y = R.randint(0, W), R.randint(int(H * 0.56), H)
        d.rectangle((x * K, y * K, (x + 3) * K, (y + 2) * K), fill=(80 + R.randint(0, 30), 108 + R.randint(0, 30), 44))
    img = img.filter(ImageFilter.GaussianBlur(K * 1.2))
    img_courante[0] = img
    d = ImageDraw.Draw(img)
    # réticule
    d.line(((W // 2 - 4) * K, H // 2 * K, (W // 2 + 4) * K, H // 2 * K), fill=(255, 255, 255), width=K)
    d.line((W // 2 * K, (H // 2 - 4) * K, W // 2 * K, (H // 2 + 4) * K), fill=(255, 255, 255), width=K)
    # barre d'objets vanilla (simplifiée)
    cx = W // 2
    d.rectangle(((cx - 91) * K, (H - 22) * K, (cx + 91) * K, H * K - 1), fill=(40, 40, 40, 200), outline=(20, 20, 20), width=K)
    for i in range(9):
        d.rectangle(((cx - 90 + i * 20) * K, (H - 21) * K, (cx - 72 + i * 20) * K, (H - 2) * K), outline=(130, 130, 130), width=K // 2 + 1)
    d.rectangle(((cx - 92) * K, (H - 23) * K, (cx - 68) * K, (H - 1) * K), outline=(240, 240, 240), width=K)
    for i in range(10):
        d.ellipse(((cx - 91 + i * 8) * K, (H - 39) * K, (cx - 84 + i * 8) * K, (H - 32) * K), fill=(200, 30, 30))
        d.ellipse(((cx + 84 - i * 8) * K, (H - 39) * K, (cx + 91 - i * 8) * K, (H - 32) * K), fill=(150, 100, 50))
    d.rectangle(((cx - 91) * K, (H - 29) * K, (cx + 91) * K, (H - 25) * K), fill=(20, 40, 10))
    d.rectangle(((cx - 91) * K, (H - 29) * K, (cx + 20) * K, (H - 25) * K), fill=(128, 255, 32))
    texte(d, cx, H - 36, "7", 7, (128, 255, 32), gras=True, centre=True, serif=False)
    # --- ajouts du mod ---
    # 1) jauge arcanique en bas à gauche (HudRoyaumes)
    gx, gy = 6, H - 22
    coller(img, HUD.crop((vent * 16, 32, vent * 16 + 16, 48)), gx, gy - 2)
    coller(img, HUD.crop((0, 0, 104, 12)), gx + 18, gy + 2)
    lf = int(100 * energie / maxi)
    coller(img, HUD.crop((0, 16, lf, 24)), gx + 20, gy + 4)
    texte(d, gx + 18, gy - 8, "Énergie arcanique  %d/%d" % (energie, maxi), 6, (200, 190, 255), serif=False)
    # 2) emblème + faction + niveau en haut à gauche
    d.rectangle((4 * K, 4 * K, 30 * K, 30 * K), fill=(12, 20, 40, 200), outline=OR, width=K)
    coller(img, embleme(num - 1), 6, 6, 22, 22)
    texte(d, 34, 6, FACTIONS[num - 1]["nom"], 7, OR_C, gras=True)
    texte(d, 34, 17, "Niveau 7 · Royaume de Ghur", 6, (240, 230, 210), serif=False)
    # 3) titre d'entrée dans un Royaume (titre vanilla stylé)
    texte(d, W // 2, 70, "ROYAUME DE GHUR", 16, (230, 170, 110), gras=True, centre=True)
    texte(d, W // 2, 92, "Le Royaume des Bêtes — Vent de Ghur : sorts à moitié prix", 7, (250, 240, 220), centre=True, serif=False)
    # 4) temps de recharge du sort en cours (barre d'action)
    texte(d, cx, H - 50, "Fureur bestiale — 20 énergie", 7, (255, 220, 160), centre=True, serif=False)
    # légendes
    lg = [("1", gx + 60, gy - 18), ("2", 90, 10), ("3", W // 2 + 120, 74), ("4", cx + 80, H - 52)]
    for n, x, y in lg:
        d.ellipse(((x - 5) * K, (y - 5) * K, (x + 5) * K, (y + 5) * K), fill=(150, 30, 30), outline=OR_C, width=K // 2 + 1)
        texte(d, x, y - 4, n, 6, (255, 255, 255), gras=True, centre=True, serif=False, ombre=False)
    return img


if __name__ == "__main__":
    out = os.path.join(ICI, "apercus")
    os.makedirs(out, exist_ok=True)
    serment(choix=0, survol=1).convert("RGB").save(os.path.join(out, "maquette_serment.png"))
    serment(choix=0, survol=21).convert("RGB").save(os.path.join(out, "maquette_serment_ironjawz.png"))
    hud().convert("RGB").save(os.path.join(out, "maquette_hud.png"))
    print("ok")
