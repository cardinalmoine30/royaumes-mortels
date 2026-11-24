# -*- coding: utf-8 -*-
"""Maquettes 0.14 aux cotes du code Java :
 - maquette_forge.png : Forge de guerre, onglet Mythique (EcranForge : 460×262, 6 onglets, 9 lignes de 22 px)
 - maquette_saga.png  : HUD avec le suivi de la Saga du Héros et du contrat (HudRoyaumes), seigneur en phase finale."""
import os
import sys
import re

from PIL import Image, ImageDraw

ICI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ICI)
import maquettes as M  # noqa: E402
from maquettes import K, texte, cadre_or, coins, coller, OR, OR_C  # noqa: E402

JAVA = os.path.join(ICI, "..", "..", "src", "main", "java", "fr", "royaumes", "ArsenalGenere.java")
TEXI = os.path.join(M.TEX, "item")


def tableau(nom):
    s = open(JAVA, encoding="utf-8").read()
    bloc = s[s.index("String[][] %s = {" % nom):]
    bloc = bloc[:bloc.index("};")]
    return [re.findall(r'"([^"]*)"', l) for l in bloc.split("\n")[2:] if l.strip().startswith("{")]


def icone(idd):
    idd = idd.split(":")[-1]
    p = os.path.join(TEXI, idd + ".png")
    if os.path.exists(p):
        return Image.open(p).convert("RGBA")
    van = {"netherite_ingot": (70, 60, 64), "nether_star": (240, 240, 255), "diamond": (90, 230, 230), "iron_ingot": (220, 220, 220)}
    im = Image.new("RGBA", (16, 16))
    d = ImageDraw.Draw(im)
    d.rectangle((3, 5, 12, 11), fill=van.get(idd, (180, 180, 180)) + (255,), outline=(30, 30, 30, 255))
    return im


def forge(faction=1, onglet=3):
    W, H = 560, 350
    img = M.fond_nuit(W, H)
    M.img_courante[0] = img
    d = ImageDraw.Draw(img)
    PW, PH = 460, 286
    px, py = (W - PW) // 2, (H - PH) // 2 + 6
    d.rectangle((0, 0, W * K, H * K), fill=(40, 20, 8, 170))
    cadre_or(d, px, py, PW, PH, fond=(26, 15, 10, 235))
    coins(img, px, py, PW, PH)
    coller(img, M.ORN.crop((0, 24, 160, 48)), px + PW / 2 - 80, py - 12)
    texte(d, px + PW / 2, py - 4, "FORGE DE GUERRE", 8, OR_C, gras=True, centre=True, serif=False)
    ids, noms, recettes = tableau("IDS")[faction - 1], tableau("NOMS")[faction - 1], tableau("RECETTES")[faction - 1]
    texte(d, px + 12, py + 4, "Arsenal : Stormcast Eternals", 7, (255, 170, 0), serif=False)
    onglets = ["Soldat", "Élite", "Légende", "Mythique", "Divin", "Armes"]
    for o, t in enumerate(onglets):
        x = px + 10 + o * 74
        coller(img, M.ORN.crop((128 if o == onglet else 64, 0, 192 if o == onglet else 128, 20)), x, py + 16, 70, 18)
        texte(d, x + 35, py + 20, t, 7, OR_C if o == onglet else (200, 190, 160), centre=True, serif=False)
    coul = [(200, 202, 210), (150, 215, 230), (245, 205, 80), (90, 230, 255), (255, 245, 220)][onglet]
    for k in range(9):
        ligne = onglet * 9 + k
        y = py + 40 + k * 22
        d.rectangle(((px + 8) * K, y * K, (px + PW - 8) * K, (y + 21) * K), fill=(64, 40, 16, 85) if k < 4 else (32, 56, 72, 64))
        coller(img, icone(ids[ligne]), px + 12, y + 2, 16, 16)
        texte(d, px + 32, y + 6, noms[ligne][:26], 7, coul, serif=False)
        x = px + 186
        for i, ing in enumerate(recettes[ligne].split(",")):
            a, n = ing.split("*")
            coller(img, icone(a), x, y + 2, 16, 16)
            ok = not (a.endswith("nether_star") or (a.endswith("ame_de_seigneur") and int(n) > 1))
            texte(d, x + 11, y + 11, n, 6, (158, 230, 154) if ok else (255, 107, 107), gras=True, serif=False)
            x += 24
        actif = k % 3 != 1
        coller(img, M.ORN.crop((64, 0, 128, 20)), px + PW - 68, y + 2, 60, 18)
        texte(d, px + PW - 38, y + 6, "Améliorer", 6, OR_C if actif else (140, 140, 140), centre=True, serif=False)
    texte(d, px + PW / 2, py + PH - 28, "Mythique : il faut les âmes des seigneurs vaincus. Panoplie : +1 niveau et 4 cœurs.", 6,
          PARCH := (230, 211, 168), centre=True, serif=False)
    texte(d, px + PW / 2, py + PH - 14, "Niveau de héros requis : 25  (toi : 27)", 6, (158, 230, 154), centre=True, serif=False)
    return img


def saga():
    W, H = 480, 270
    img = Image.new("RGBA", (W * K, H * K))
    d = ImageDraw.Draw(img)
    import random
    import math
    from PIL import ImageFilter
    for i in range(H * K):  # ciel d'Aqshy, sol de cendre
        t = i / (H * K)
        c = tuple(int(a + (b - a) * t) for a, b in zip((120, 40, 30), (230, 120, 60))) if t < 0.55 else (70, 50, 44)
        d.line((0, i, W * K, i), fill=c)
    R = random.Random(7)
    for _ in range(12):
        x, h = R.randint(0, W), R.randint(30, 90)
        d.polygon([((x - 40) * K, int(H * 0.55) * K), (x * K, (int(H * 0.55) - h) * K), ((x + 40) * K, int(H * 0.55) * K)], fill=(60, 30, 28))
    for _ in range(300):
        x, y = R.randint(0, W), R.randint(int(H * 0.56), H)
        d.rectangle((x * K, y * K, (x + 3) * K, (y + 2) * K), fill=(60 + R.randint(0, 30), 44 + R.randint(0, 20), 40))
    img = img.filter(ImageFilter.GaussianBlur(K * 1.2))
    M.img_courante[0] = img
    d = ImageDraw.Draw(img)
    # seigneur (silhouette) au fond
    d.ellipse(((W // 2 - 22) * K, 100 * K, (W // 2 + 22) * K, 150 * K), fill=(120, 20, 20))
    d.polygon([((W // 2 - 30) * K, 112 * K), ((W // 2 - 60) * K, 90 * K), ((W // 2 - 26) * K, 124 * K)], fill=(90, 14, 14))
    d.polygon([((W // 2 + 30) * K, 112 * K), ((W // 2 + 60) * K, 90 * K), ((W // 2 + 26) * K, 124 * K)], fill=(90, 14, 14))
    d.rectangle(((W // 2 - 14) * K, 148 * K, (W // 2 + 14) * K, 170 * K), fill=(100, 16, 16))
    cx = W // 2
    # barre d'objets, cœurs (dont 4 cœurs bonus Mythique), jauge arcanique
    d.rectangle(((cx - 91) * K, (H - 22) * K, (cx + 91) * K, H * K - 1), fill=(40, 40, 40, 200), outline=(20, 20, 20), width=K)
    for i in range(9):
        d.rectangle(((cx - 90 + i * 20) * K, (H - 21) * K, (cx - 72 + i * 20) * K, (H - 2) * K), outline=(130, 130, 130), width=K // 2 + 1)
    for i, idd in enumerate(["khorne_ascension", "chaos_pioche_mythique", "chaos_hache_mythique", "ame_de_seigneur", "baton_aqshy"]):
        coller(img, icone(idd), cx - 88 + i * 20, H - 19, 16, 16)
    d.rectangle(((cx - 92) * K, (H - 23) * K, (cx - 68) * K, (H - 1) * K), outline=(240, 240, 240), width=K)
    for i in range(10):
        d.ellipse(((cx - 91 + i * 8) * K, (H - 39) * K, (cx - 84 + i * 8) * K, (H - 32) * K), fill=(200, 30, 30))
    for i in range(4):
        d.ellipse(((cx - 91 + i * 8) * K, (H - 47) * K, (cx - 84 + i * 8) * K, (H - 40) * K), fill=(230, 60, 60))
    d.rectangle(((cx - 91) * K, (H - 29) * K, (cx + 91) * K, (H - 25) * K), fill=(20, 40, 10))
    d.rectangle(((cx - 91) * K, (H - 29) * K, (cx + 60) * K, (H - 25) * K), fill=(128, 255, 32))
    texte(d, cx, H - 36, "27", 7, (128, 255, 32), gras=True, centre=True, serif=False)
    gx, gy = 6, H - 22
    coller(img, M.HUD.crop((16, 32, 32, 48)), gx, gy - 2)
    coller(img, M.HUD.crop((0, 0, 104, 12)), gx + 18, gy + 2)
    coller(img, M.HUD.crop((0, 16, 64, 24)), gx + 20, gy + 4)
    texte(d, gx + 20, gy - 8, "96 / 150", 6, (200, 190, 255), serif=False)
    # emblème, faction, capacité (HudRoyaumes 2)
    d.rectangle((4 * K, 4 * K, 30 * K, 30 * K), fill=(12, 20, 40, 200), outline=OR, width=K)
    coller(img, M.embleme(10), 6, 6, 22, 22)
    texte(d, 34, 6, "Lames de Khorne", 7, OR_C, gras=True, serif=False)
    texte(d, 34, 17, "Niveau 27 · Royaume d'Aqshy", 6, (240, 230, 210), serif=False)
    texte(d, 34, 28, "Soif de sang · prête (R)", 6, OR_C, serif=False)
    # suivi de la Saga (HudRoyaumes 5)
    l1, l2, l3 = "✦ 17/23 · Tueur de légendes", "Invoque un seigneur à son autel et vaincs-le.", "⚔ Contrat : guerriers de l'Ordre  11/23"
    larg = 168
    d.rectangle((4 * K, 44 * K, (4 + larg) * K, (44 + 35) * K), fill=(12, 20, 40, 150))
    d.rectangle((4 * K, 44 * K, 5 * K, (44 + 35) * K), fill=OR)
    texte(d, 8, 47, l1, 6, OR_C, serif=False)
    texte(d, 8, 57, l2, 6, (207, 198, 180), serif=False)
    texte(d, 8, 68, l3, 6, (127, 214, 230), serif=False)
    # barre du seigneur (datapack) et annonce de la phase finale (mod)
    texte(d, cx, 4, "Skarbrand, l'Exilé", 7, (255, 255, 255), centre=True, serif=False)
    d.rectangle(((cx - 91) * K, 13 * K, (cx + 91) * K, 18 * K), fill=(60, 10, 10))
    d.rectangle(((cx - 91) * K, 13 * K, (cx - 91 + 40) * K, 18 * K), fill=(220, 30, 30))
    texte(d, cx, 50, "Skarbrand", 14, (230, 50, 40), gras=True, centre=True)
    texte(d, cx, 70, "déchaîne sa puissance ! Esquive les cercles !", 7, (255, 140, 110), centre=True, serif=False)
    for (ox, oy, r) in [(cx - 70, 196, 26), (cx + 80, 206, 22)]:
        for a in range(32):
            t = a * math.pi / 16
            x, y = ox + math.cos(t) * r, oy + math.sin(t) * r * 0.35
            d.ellipse(((x - 1.5) * K, (y - 1.5) * K, (x + 1.5) * K, (y + 1.5) * K), fill=(255, 140 + (a % 3) * 30, 40))
    texte(d, cx - 70, 208, "impact dans 1,5 s", 6, (255, 220, 160), centre=True, serif=False)
    d.line(((W // 2 - 4) * K, H // 2 * K, (W // 2 + 4) * K, H // 2 * K), fill=(255, 255, 255), width=K)
    d.line((W // 2 * K, (H // 2 - 4) * K, W // 2 * K, (H // 2 + 4) * K), fill=(255, 255, 255), width=K)
    return img


if __name__ == "__main__":
    out = os.path.join(ICI, "apercus", "jeu")
    os.makedirs(out, exist_ok=True)
    forge().convert("RGB").save(os.path.join(out, "maquette_forge.png"))
    saga().convert("RGB").save(os.path.join(out, "maquette_saga.png"))
    print("ok")
