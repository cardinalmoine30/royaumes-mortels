# -*- coding: utf-8 -*-
"""Visuels du camp de guerre : scène reconstituée (vrais modèles) et maquette de l'écran du camp."""
import os
import random
import sys

from PIL import Image, ImageDraw, ImageFilter

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from scenes import Scene, TEX, LUM, coins, terrain, hud, legende, W, H  # noqa: E402
import maquettes as M  # noqa: E402

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "apercus", "jeu")
B = lambda n: os.path.join(TEX, "block", n + ".png")  # noqa: E731


def boite(s, o, t, chemin, emis=False):
    T = s.tex(chemin)
    for f in ("up", "north", "south", "east", "west"):
        c = coins(o, t, f)
        s.quads.append((c[0], c[1], c[2], T, (0, 0, T.shape[1], T.shape[0]), LUM[f], emis))


def etendard(s, x, y, z):
    boite(s, (x + 0.25, y, z + 0.25), (0.5, 0.12, 0.5), B("etendard_de_camp_hampe"))
    boite(s, (x + 0.44, y, z + 0.44), (0.12, 2.6, 0.12), B("etendard_de_camp_hampe"))
    boite(s, (x - 0.2, y + 2.45, z + 0.46), (1.4, 0.08, 0.08), B("etendard_de_camp_hampe"))
    boite(s, (x - 0.1, y + 0.9, z + 0.49), (1.2, 1.55, 0.02), B("etendard_de_camp"))


def tente(s, x, z, toile):
    for i in range(3):
        boite(s, (x - 1.5 + i * 0.5, i * 0.6, z), (3 - i, 0.6, 3), toile)


def scene():
    s = Scene((80, 130, 215), (210, 225, 245), (210, 225, 245), 46)
    herbe = terrain("herbe_azyr", (100, 150, 80), 0.12, 21)
    r = random.Random(4)
    for x in range(-16, 17):
        for z in range(-3, 40):
            s.bloc(x, -1, z, B("marbre_celeste") if abs(x) < 3 and z < 14 else herbe, faces=("up",))
    toile = terrain("toile", (60, 90, 170), 0.06, 22)
    toile_or = terrain("toile_or", (200, 160, 60), 0.06, 23)
    tente(s, -6, 12, toile)
    tente(s, 6, 13, toile_or)
    tente(s, -7, 20, toile_or)
    for x in range(-3, 4):
        s.bloc(x, 0, 24, B("marbre_celeste_grave"))
    for x in (-10, 10):
        for z in range(6, 26, 2):
            s.bloc(x, 0, z, B("bois_de_vie"))
    etendard(s, 0, 0, 9)
    s.modele("liberator", -2.2, 0, 8, lacet=200)
    s.modele("liberator", 2.4, 0, 8.4, lacet=160)
    s.modele("judicator", -3.5, 0, 14, lacet=30)
    s.modele("judicator", 3.8, 0, 15, lacet=-30)
    s.modele("vindictor", 0.5, 0, 17, lacet=0)
    s.joueur("stormcast", 0.8, 0, 4, lacet=180)
    img = s.rendre((1.5, 3.4, -2.8), (0, 1.6, 12))
    hud(img, 1, "Foudroyés Éternels", 12, "d'Célestis", "Frappe de foudre · prête (R)", 140, 160, 0)
    legende(img, "Scène reconstituée · Camp de guerre Foudroyés")
    return img


def ecran(fond):
    K = 3
    M.K = K
    img = Image.new("RGBA", (480 * K, 270 * K), (0, 0, 0, 0))
    M.img_courante[0] = img
    d = ImageDraw.Draw(img)
    PW, PH = 400, 240
    px, py = 40, 15
    M.cadre_or(d, px, py, PW, PH, fond=(12, 20, 40, 238))
    M.coins(img, px, py, PW, PH)
    M.coller(img, M.ORN.crop((0, 24, 160, 48)), px + PW // 2 - 80, py - 10)
    M.texte(d, px + PW // 2, py - 4, "CAMP DE GUERRE", 8, M.OR_C, gras=True, centre=True)
    x = px + 12
    M.texte(d, x, py + 20, "Niveau 3 / 5", 7, M.OR_C, gras=True)
    M.texte(d, x + 100, py + 20, "Butin : 214", 7, (242, 210, 122), serif=False)
    M.texte(d, x, py + 32, "Troupes : 5 / 8", 7, M.PARCH, serif=False)
    M.texte(d, x + 100, py + 32, "Force au camp : 41", 7, M.PARCH, serif=False)

    def bouton(bx, by, w, h, t, choisi=False, inactif=False):
        M.coller(img, M.ORN.crop((128 if choisi else 64, 0, 192 if choisi else 128, 20)), bx, by, w, h)
        M.texte(d, bx + w / 2, by + (h - 8) / 2, t, 6, (140, 140, 140) if inactif else M.OR_C, gras=True, centre=True, serif=False)
        if inactif:
            voile = Image.new("RGBA", img.size)
            ImageDraw.Draw(voile).rectangle(((bx + 2) * K, (by + 2) * K, (bx + w - 2) * K, (by + h - 2) * K), fill=(0, 0, 0, 110))
            img.alpha_composite(voile)
    M.texte(d, x, py + 54, "ORDRES", 7, M.OR, gras=True)
    d.line((x * K, (py + 63) * K, (x + 184) * K, (py + 63) * K), fill=M.OR, width=2)
    bouton(x, py + 66, 90, 18, "Garder le camp", choisi=True)
    bouton(x + 94, py + 66, 90, 18, "Me suivre")
    bouton(x, py + 90, 184, 18, "Déposer le butin")
    bouton(x, py + 112, 184, 18, "Améliorer le camp — 300 butin", inactif=True)
    M.texte(d, x, py + 136, "RAIDS", 7, M.OR, gras=True)
    d.line((x * K, (py + 145) * K, (x + 184) * K, (py + 145) * K), fill=M.OR, width=2)
    for k, (n, du, dif) in enumerate((("Pillage", 2, 15), ("Assaut", 5, 40), ("Croisade", 10, 90))):
        bouton(x, py + 154 + k * 22, 184, 18, "%s · %d min · réussite %d %%" % (n, du, 100 * 41 // (41 + dif)))
    qx = px + 206
    M.cadre_or(d, qx, py + 14, 184, PH - 22, fond=(24, 30, 52))
    M.texte(d, qx + 92, py + 20, "RECRUTEMENT", 7, M.OR_C, gras=True, centre=True)
    unites = [("Libérateur", 22), ("Justicier", 26), ("Vengeur", 30), ("Poursuivant", 34), ("Seigneur-Céleste", 70),
              ("Draconide", 95), ("Griffon-Coursier", 110), ("Drake Stellaire", 260)]
    for i, (n, c) in enumerate(unites):
        y = py + 36 + i * 24
        ouvert = i < 5
        d.rectangle(((qx + 6) * K, (y - 2) * K, (qx + 178) * K, (y + 20) * K), fill=(60, 52, 30, 255) if ouvert else (16, 20, 34, 255))
        M.texte(d, qx + 10, y + 1, n, 7, (240, 230, 210) if ouvert else (112, 112, 112), gras=True, serif=False)
        M.texte(d, qx + 10, y + 11, ("%d butin" % c) if ouvert else "Camp niveau %d" % [n for n in range(1, 6) if [0, 2, 3, 5, 6, 8][n] > i][0], 6, (242, 210, 122) if ouvert else (112, 112, 112), serif=False)
        bouton(qx + 124, y, 52, 18, "Recruter", inactif=not ouvert)
    img = img.resize((W, H), Image.LANCZOS)
    base = fond.filter(ImageFilter.GaussianBlur(6))
    base.alpha_composite(Image.new("RGBA", (W, H), (0, 0, 0, 100)))
    base.alpha_composite(img)
    return base


if __name__ == "__main__":
    sc = scene()
    sc.convert("RGB").save(os.path.join(OUT, "6_camp_de_guerre.png"))
    ecran(sc).convert("RGB").save(os.path.join(OUT, "7_ecran_camp.png"))
    print("ok")
