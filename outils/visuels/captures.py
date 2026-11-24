# -*- coding: utf-8 -*-
"""Scènes de jeu reconstituées avec les vrais modèles et textures du mod (voir scenes.py)."""
import os
import random
import sys

from PIL import Image, ImageFilter

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from scenes import (Scene, TEX, W, H, terrain, lueur, eclair, hud, legende)  # noqa: E402

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "apercus", "jeu")
os.makedirs(OUT, exist_ok=True)
B = lambda n: os.path.join(TEX, "block", n + ".png")  # noqa: E731
I = lambda n: os.path.join(TEX, "item", n + ".png")  # noqa: E731


def sol(s, x0, x1, z0, z1, choix, y=-1, graine=1):
    r = random.Random(graine)
    for x in range(x0, x1):
        for z in range(z0, z1):
            s.bloc(x, y, z, r.choice(choix), faces=("up",))


def pilier(s, x, z, h, corps, tete):
    for y in range(h):
        s.bloc(x, y, z, tete if y == h - 1 else corps)


# ------------------------------------------------------------------ 1. Azyr : Éclair d'Azyr
def azyr():
    s = Scene((70, 120, 210), (205, 222, 245), (205, 222, 245), 46)
    sol(s, -16, 17, -3, 40, [B("marbre_celeste")] * 6 + [B("marbre_celeste_grave")])
    for z in (6, 14, 22, 30):
        pilier(s, 6, z, 5, B("marbre_celeste"), B("or_vif"))
        pilier(s, -6, z, 5, B("marbre_celeste"), B("or_vif"))
    for x in range(-4, 5):
        s.bloc(x, 0, 34, B("marbre_celeste_grave"))
        s.bloc(x, 1, 34, B("marbre_celeste_grave"))
    s.joueur("stormcast", 0.9, 0, 3, lacet=180, pose={"right_arm": (-75, 0, 0)})
    s.modele("liberator", 4, 0, 6.5, lacet=180)
    s.modele("bloodletter", -0.5, 0, 13, lacet=10)
    s.modele("blood_warrior", 2.5, 0, 15, lacet=-10)
    s.modele("bloodletter", -3.5, 0, 17, lacet=20)
    img = s.rendre((2.2, 3.3, -3.2), (0, 1.4, 12))
    a, _ = s._proj((-0.5, 14, 13))
    b, _ = s._proj((-0.5, 1.2, 13))
    eclair(img, tuple(a), tuple(b))
    eclair(img, tuple(a), tuple(b), graine=9)
    lueur(img, [tuple(b)], (160, 210, 255), 34)
    rr = random.Random(2)
    lueur(img, [(b[0] + rr.uniform(-60, 60), b[1] + rr.uniform(-60, 20)) for _ in range(14)], (220, 240, 255), 3)
    hud(img, 1, "Stormcast Eternals", 12, "d'Azyr", "Frappe de foudre · prête (R)", 103, 160, 0,
        objet=I("baton_azyr"), sort="Éclair d'Azyr — 8 énergie", couleur_sort=(120, 170, 255))
    legende(img, "Scène reconstituée · Royaume d'Azyr")
    return img


# ------------------------------------------------------------------ 2. Ghur : Waaagh !
def ghur():
    s = Scene((200, 120, 70), (245, 200, 140), (235, 190, 140), 44)
    herbe = terrain("herbe_ghur", (120, 110, 60), 0.15, 3, dessus=None)
    terre = terrain("terre_ghur", (130, 92, 60), 0.15, 4)
    sol(s, -18, 19, -3, 42, [herbe] * 5 + [terre], graine=3)
    r = random.Random(7)
    for _ in range(9):
        x, z = r.randint(-15, 15), r.randint(10, 38)
        if abs(x) < 4:
            continue
        for y in range(r.randint(1, 3)):
            s.bloc(x, y, z, B("pierre_de_croc"))
    for k in range(5):  # côtes d'un monstre géant
        x = -10 + k * 2
        for y in range(0, 4 + (2 - abs(k - 2))):
            s.bloc(x, y, 26, B("os_de_monstre"))
    s.joueur("ironjawz", 0, 0, 3, lacet=180, pose={"right_arm": (-150, 0, 20), "left_arm": (-150, 0, -20)})
    s.modele("brute", 2.8, 0, 5.2, lacet=190)
    s.modele("brute", -2.6, 0, 5.4, lacet=170)
    s.modele("saurus", 1, 0, 14, lacet=0)
    s.modele("saurus", -2, 0, 15, lacet=10)
    s.modele("carnosaur", 3, 0, 20, lacet=-15)
    img = s.rendre((1.2, 3.2, -3), (0, 1.6, 12))
    hud(img, 21, "Ironjawz", 9, "de Ghur", "Waaagh ! · 87 s", 71, 145, 2, objet=I("marteau_tempete"))
    from PIL import ImageDraw, ImageFont
    d = ImageDraw.Draw(img)
    f = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 24)
    msg = "✦ Waaagh ! ✦"
    d.text((W / 2 - d.textlength(msg, font=f) / 2 + 2, H - 202), msg, font=f, fill=(40, 30, 0))
    d.text((W / 2 - d.textlength(msg, font=f) / 2, H - 204), msg, font=f, fill=(255, 190, 40))
    for (x, z) in ((2.8, 5.2), (-2.6, 5.4)):
        p, _ = s._proj((x, 2.4, z))
        lueur(img, [(p[0] + random.uniform(-30, 30), p[1] + random.uniform(-20, 20)) for _ in range(6)], (110, 200, 70), 5)
    legende(img, "Scène reconstituée · Royaume de Ghur")
    return img


# ------------------------------------------------------------------ 3. Shyish : face à Nagash
def shyish():
    s = Scene((30, 20, 50), (110, 80, 140), (90, 70, 120), 40)
    sable = terrain("sable_shyish", (150, 140, 160), 0.1, 5)
    sol(s, -16, 17, -3, 40, [B("pierre_funeraire")] * 3 + [sable] * 2 + [B("dalle_des_ames")], graine=5)
    r = random.Random(11)
    for _ in range(12):
        x, z = r.randint(-14, 14), r.randint(6, 36)
        if abs(x) < 5:
            continue
        s.bloc(x, 0, z, B("pierre_funeraire"))
        if r.random() < 0.5:
            s.bloc(x, 1, z, B("pierre_funeraire"))
    for x in (-7, 7):
        for y in range(6):
            s.bloc(x, y, 24, B("dalle_des_ames"), emissif=(y == 5))
    s.joueur("lumineth", -0.6, 0, 3.2, lacet=180, pose={"right_arm": (-85, 0, 0)})
    s.modele("nagash", 0, 0, 17, lacet=0, echelle=2.11)
    s.modele("deathrattle", -3.5, 0, 11, lacet=15)
    s.modele("deathrattle", 3.5, 0, 12, lacet=-15)
    s.modele("grave_guard", 5, 0, 15, lacet=-20)
    img = s.rendre((1.4, 3.0, -2.6), (0, 2.8, 14))
    a, _ = s._proj((-0.9, 1.9, 4.0))
    b, _ = s._proj((0, 4.5, 16.5))
    from PIL import ImageDraw
    calque = Image.new("RGBA", img.size)
    ImageDraw.Draw(calque).line([tuple(a), tuple(b)], fill=(255, 250, 200, 255), width=16)
    img.alpha_composite(calque.filter(ImageFilter.GaussianBlur(9)))
    ImageDraw.Draw(img).line([tuple(a), tuple(b)], fill=(255, 255, 240), width=4)
    lueur(img, [tuple(b)], (255, 240, 180), 18)
    hud(img, 7, "Lumineth Realm-lords", 18, "de Shyish", "Lumière de Teclis · prête (R)", 58, 190, 4,
        objet=I("baton_hysh"), sort="Rayon de Hysh — 15 énergie", couleur_sort=(255, 245, 190))
    legende(img, "Scène reconstituée · Royaume de Shyish, boss Nagash")
    return img


# ------------------------------------------------------------------ 4. Aqshy : Portail des Royaumes et monture
def aqshy():
    s = Scene((90, 30, 20), (230, 120, 60), (180, 90, 60), 40)
    cendre = terrain("cendre", (80, 70, 70), 0.15, 8)
    sol(s, -16, 17, -3, 40, [cendre] * 3 + [B("basalte_ardent")], graine=8)
    for (x, z, h) in ((-9, 18, 4), (10, 22, 6), (-12, 30, 7), (6, 32, 5)):
        for y in range(h):
            s.bloc(x, y, z, B("basalte_ardent"), emissif=(y == h - 1))
    # Portail des Royaumes : cadre d'or vif, cœur de portail
    for x in range(-3, 4):
        for y in range(0, 6):
            bord = x in (-3, 3) or y in (0, 5)
            s.bloc(x, y, 12, B("or_vif") if bord else B("portail_des_royaumes"), emissif=not bord)
    s.bloc(0, 6, 12, B("brique_de_braise"))
    s.modele("monture_magmadroth", -4, 0, 7, lacet=-35, echelle=1.135)
    s.modele("monture_dracoth", 4.5, 0, 7.5, lacet=30, echelle=1.06)
    s.joueur("fyreslayers", -1.2, 0, 3.5, lacet=180)
    img = s.rendre((0.5, 3.0, -2.5), (0, 2.4, 12))
    p, _ = s._proj((0, 2.8, 12))
    lueur(img, [(p[0] + random.uniform(-80, 80), p[1] + random.uniform(-90, 90)) for _ in range(20)], (160, 120, 255), 4)
    hud(img, 3, "Fyreslayers", 15, "d'Aqshy", "Rune de fureur · prête (R)", 140, 175, 1)
    legende(img, "Scène reconstituée · Royaume d'Aqshy, Portail des Royaumes et montures")
    return img


# ------------------------------------------------------------------ 5. Écran de serment par-dessus le jeu
def serment(fond):
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    import maquettes
    maquettes.K = 3
    ecran = maquettes.serment(choix=0, survol=21)  # 480x270 interface -> 1440x810
    ecran = ecran.resize((W, H), Image.LANCZOS)
    base = fond.filter(ImageFilter.GaussianBlur(6))
    voile = Image.new("RGBA", (W, H), (0, 0, 0, 90))
    base.alpha_composite(voile)
    ecran.putalpha(235)
    base.alpha_composite(ecran)
    return base


if __name__ == "__main__":
    imgs = {"1_azyr_eclair": azyr(), "2_ghur_waaagh": ghur(), "3_shyish_nagash": shyish(), "4_aqshy_portail": aqshy()}
    imgs["5_ecran_serment"] = serment(imgs["1_azyr_eclair"])
    for n, im in imgs.items():
        im.convert("RGB").save(os.path.join(OUT, n + ".png"))
        print(n)
