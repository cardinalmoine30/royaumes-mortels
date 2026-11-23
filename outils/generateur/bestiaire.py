# -*- coding: utf-8 -*-
"""Bestiaire : rendu de face (textures Minecraft) de chaque mob de faction tel qu'il apparaît en jeu."""
import os, sys
from PIL import Image, ImageDraw, ImageFont
import data_v4  # noqa
import extension
from data_monde import P as PROFILS
from data_factions import ALLIANCES

T = "/tmp/mc-assets/assets/minecraft/textures"
POL = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
POL2 = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
TRIM = {"gold": (232, 192, 64), "lapis": (42, 80, 192), "redstone": (176, 32, 32), "copper": (192, 106, 58),
        "quartz": (238, 234, 224), "netherite": (70, 60, 60), "amethyst": (154, 90, 208), "emerald": (32, 176, 80),
        "diamond": (90, 224, 224), "iron": (208, 208, 208), "resin": (224, 122, 32)}


def tex(p):
    return Image.open(f"{T}/{p}").convert("RGBA")


def crop(im, box):
    return im.crop(box)


def teinte(im, c):
    r, g, b, a = im.split()
    l = Image.merge("RGB", (r, g, b)).convert("L")
    return Image.merge("RGBA", (l.point(lambda v: v * c[0] // 255), l.point(lambda v: v * c[1] // 255),
                                l.point(lambda v: v * c[2] // 255), a))


# Gabarits UV (face avant) : tête, corps, bras droit/gauche, jambe droite/gauche  (x0,y0,x1,y1)
ZOMBIE = dict(tete=(8, 8, 16, 16), chapeau=(40, 8, 48, 16), corps=(20, 20, 28, 32), bd=(44, 20, 48, 32), bg=(36, 52, 40, 64),
              jd=(4, 20, 8, 32), jg=(20, 52, 24, 64), larg_bras=4)
SQUEL = dict(tete=(8, 8, 16, 16), chapeau=(40, 8, 48, 16), corps=(20, 20, 28, 32), bd=(42, 18, 44, 30), bg=(42, 18, 44, 30),
             jd=(2, 18, 4, 30), jg=(2, 18, 4, 30), larg_bras=2)
PIGLIN = dict(tete=(8, 8, 18, 16), corps=(20, 20, 28, 32), bd=(44, 20, 48, 32), bg=(36, 52, 40, 64),
              jd=(4, 20, 8, 32), jg=(20, 52, 24, 64), larg_bras=4)
ARM = dict(tete=(8, 8, 16, 16), corps=(20, 20, 28, 32), bras=(44, 20, 48, 32), jambe=(4, 20, 8, 32))
PEAUX = {"zombie": ("entity/zombie/zombie.png", ZOMBIE), "husk": ("entity/zombie/husk.png", ZOMBIE),
         "drowned": ("entity/zombie/drowned.png", ZOMBIE), "skeleton": ("entity/skeleton/skeleton.png", SQUEL),
         "wither_skeleton": ("entity/skeleton/wither_skeleton.png", SQUEL),
         "piglin_brute": ("entity/piglin/piglin_brute.png", PIGLIN)}


def figure(p):
    """Image 2D de face (pixels Minecraft) du mob équipé."""
    base = p["base"]
    if base not in PEAUX:
        return special(base)
    chemin, uv = PEAUX[base]
    peau = tex(chemin)
    W, H = 16 + 4, 32 + 2
    im = Image.new("RGBA", (W * 1, H), (0, 0, 0, 0))
    lb = uv["larg_bras"]
    tw = uv["tete"][2] - uv["tete"][0]
    ox = 2
    # corps
    def coller(box, x, y, flip=False):
        c = crop(peau, box)
        if flip:
            c = c.transpose(Image.FLIP_LEFT_RIGHT)
        im.alpha_composite(c, (x, y))
    cx = ox + 4                   # début du torse
    coller(uv["corps"], cx, 9)
    coller(uv["bd"], cx - lb, 9)
    coller(uv["bg"], cx + 8, 9, flip=True)
    coller(uv["jd"], cx + (4 - (uv["jd"][2] - uv["jd"][0])), 21)
    coller(uv["jg"], cx + 4, 21, flip=True)
    coller(uv["tete"], cx + (8 - tw) // 2, 1)
    if "chapeau" in uv:
        coller(uv["chapeau"], cx, 1)
    if base == "drowned":
        out = tex("entity/zombie/drowned_outer_layer.png")
        im.alpha_composite(crop(out, ZOMBIE["corps"]), (cx, 9))
    if "invisibility" in [e for e, _ in p.get("effets", [])]:
        a = im.split()[3].point(lambda v: v // 5)
        im.putalpha(a)
    # armure
    eqp = p.get("equip", {})
    for slot, spec in eqp.items():
        if not slot.startswith("armor."):
            continue
        mat = spec["id"].split(":")[1].rsplit("_", 1)[0]
        mat = {"golden": "gold"}.get(mat, mat)
        couche = "humanoid_leggings" if slot == "armor.legs" else "humanoid"
        try:
            t = tex(f"entity/equipment/{couche}/{mat}.png")
        except FileNotFoundError:
            continue
        if mat == "leather" and spec.get("dye") is not None:
            d = spec["dye"]
            t = teinte(t, ((d >> 16) & 255, (d >> 8) & 255, d & 255))
        if spec.get("trim"):
            m, pat = spec["trim"]
            try:
                tr = tex(f"trims/entity/{couche}/{pat}.png")
                tr = teinte(tr, TRIM.get(m, (200, 200, 200)))
                t.alpha_composite(tr)
            except FileNotFoundError:
                pass
        if slot == "armor.head":
            im.alpha_composite(crop(t, ARM["tete"]), (cx, 1))
        elif slot == "armor.chest":
            im.alpha_composite(crop(t, ARM["corps"]), (cx, 9))
            im.alpha_composite(crop(t, ARM["bras"]), (cx - 4, 9))
            im.alpha_composite(crop(t, ARM["bras"]).transpose(Image.FLIP_LEFT_RIGHT), (cx + 8, 9))
        elif slot == "armor.legs":
            im.alpha_composite(crop(t, (20, 20, 28, 27)), (cx, 20))
            im.alpha_composite(crop(t, ARM["jambe"]), (cx, 21))
            im.alpha_composite(crop(t, ARM["jambe"]).transpose(Image.FLIP_LEFT_RIGHT), (cx + 4, 21))
        elif slot == "armor.feet":
            b = crop(t, (4, 26, 8, 32))
            im.alpha_composite(b, (cx, 27)); im.alpha_composite(b.transpose(Image.FLIP_LEFT_RIGHT), (cx + 4, 27))
    return im


def special(base):
    if base == "spider":
        s = tex("entity/spider/spider.png")
        im = Image.new("RGBA", (28, 14))
        im.alpha_composite(crop(s, (40, 12, 48, 20)), (10, 3))
        d = ImageDraw.Draw(im)
        for i in range(4):
            d.line((9, 6 + i * 2, 1, 2 + i * 3), fill=(40, 30, 30, 255))
            d.line((18, 6 + i * 2, 26, 2 + i * 3), fill=(40, 30, 30, 255))
        return im
    if base == "ravager":
        r = tex("entity/illager/ravager.png")
        return crop(r, (16, 16, 32, 36))
    if base == "iron_golem":
        g = tex("entity/iron_golem/iron_golem.png") if os.path.exists(f"{T}/entity/iron_golem/iron_golem.png") else None
        return crop(g, (8, 8, 16, 18)) if g else Image.new("RGBA", (8, 10), (200, 200, 200, 255))
    return Image.new("RGBA", (8, 16), (150, 150, 150, 255))


def item_icone(spec):
    mid = spec.get("item_model") or spec["id"]
    n = mid.split(":")[1]
    for p in (f"{T}/item/{n}.png", f"{T}/block/{n}.png", f"{T}/block/{n}_top.png"):
        if os.path.exists(p):
            return Image.open(p).convert("RGBA").crop((0, 0, 16, 16))
    return None


def carte(pid, p, ech=10):
    fig = figure(p)
    sc = p["attrs"].get("scale", 1.0)
    if p.get("bebe"):
        sc *= 0.6
    k = max(4, int(ech * min(sc, 2.2)))
    fig = fig.resize((fig.width * k, fig.height * k), Image.NEAREST)
    Wc, Hc = 300, 460
    c = Image.new("RGBA", (Wc, Hc), (30, 32, 40, 255))
    d = ImageDraw.Draw(c)
    al = ALLIANCES.get(p["alliance"], {})
    col = {"gold": (230, 190, 70), "dark_red": (190, 50, 50), "dark_purple": (160, 90, 200), "dark_green": (80, 170, 80)}.get(
        al.get("couleur"), (220, 220, 220))
    if p.get("team") == "rm_boss":
        col = (230, 70, 70)
    d.rectangle((0, 0, Wc - 1, Hc - 1), outline=col, width=3)
    zone_h = 330
    if fig.height > zone_h - 20:
        r = (zone_h - 20) / fig.height
        fig = fig.resize((max(1, int(fig.width * r)), zone_h - 20), Image.NEAREST)
    x0 = (Wc - fig.width) // 2
    y0 = 10 + (zone_h - 20 - fig.height)
    c.alpha_composite(fig, (x0, y0))
    # armes
    main = p.get("equip", {}).get("weapon.mainhand")
    if main:
        ic = item_icone(main)
        if ic:
            ic = ic.resize((64, 64), Image.NEAREST)
            c.alpha_composite(ic, (max(0, x0 - 50), y0 + fig.height // 3))
    off = p.get("equip", {}).get("weapon.offhand")
    if off:
        ic = item_icone(off)
        if ic:
            ic = ic.resize((56, 56), Image.NEAREST)
            c.alpha_composite(ic, (min(Wc - 58, x0 + fig.width - 6), y0 + fig.height // 3))
    f1 = ImageFont.truetype(POL, 17); f2 = ImageFont.truetype(POL2, 13)
    nom = p["nom"] or pid
    d.text((12, zone_h + 6), nom, fill=col, font=f1)
    a = p["attrs"]
    lignes = [f"Base : {p['base']}   Taille ×{a.get('scale', 1.0)}",
              f"PV {a.get('max_health', '—')}   Dégâts {a.get('attack_damage', '—')}   Armure {a.get('armor', 0)}",
              "Ressource : " + extension.RES.get(extension.RES_PROFIL.get(pid, ""), ("—",))[0]]
    if p.get("team") == "rm_boss":
        lignes[2] = "BOSS : 3 capacités + rage"
    for i, l in enumerate(lignes):
        d.text((12, zone_h + 34 + i * 20), l, fill=(210, 210, 210), font=f2)
    return c


def planche(pids, titre, sortie, cols=5):
    cartes = [carte(pid, PROFILS[pid]) for pid in pids]
    rows = (len(cartes) + cols - 1) // cols
    sh = Image.new("RGBA", (cols * 310 + 10, rows * 470 + 70), (18, 20, 26, 255))
    ImageDraw.Draw(sh).text((16, 16), titre, fill=(240, 220, 150), font=ImageFont.truetype(POL, 30))
    for i, cimg in enumerate(cartes):
        sh.alpha_composite(cimg, (10 + (i % cols) * 310, 66 + (i // cols) * 470))
    sh.convert("RGB").save(sortie, optimize=True)
    print(sortie, sh.size)


if __name__ == "__main__":
    extension.preparer()
    par = {"ordre": [], "chaos": [], "mort": [], "destruction": []}
    boss = []
    for pid, p in PROFILS.items():
        if pid in ("habitant", "garde_cite"):
            continue
        if p.get("team") == "rm_boss":
            boss.append(pid)
        else:
            par[p["alliance"]].append(pid)
    os.makedirs("out/bestiaire", exist_ok=True)
    noms = {"ordre": "Ordre", "chaos": "Chaos", "mort": "Mort", "destruction": "Destruction"}
    for a, l in par.items():
        planche(l, f"Bestiaire des Royaumes Mortels — Grande Alliance : {noms[a]}", f"out/bestiaire/bestiaire_{a}.png")
    planche(boss, "Bestiaire — Boss légendaires", "out/bestiaire/bestiaire_boss.png", cols=4)
