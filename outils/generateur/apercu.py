# -*- coding: utf-8 -*-
"""Rendu isométrique rapide des structures pour vérification visuelle."""
import glob, os, nbtlib
from PIL import Image, ImageDraw, ImageFont

COUL = [
    ("gold", (230, 190, 40)), ("gilded", (150, 110, 40)), ("lapis", (40, 70, 170)), ("quartz", (235, 230, 222)),
    ("calcite", (225, 225, 220)), ("diorite", (200, 200, 200)), ("blue_stained", (70, 110, 220)), ("light_blue", (120, 170, 240)),
    ("sea_lantern", (200, 235, 235)), ("blackstone", (45, 40, 48)), ("deepslate", (70, 70, 75)), ("obsidian", (30, 20, 45)),
    ("crying", (90, 30, 160)), ("magma", (190, 80, 20)), ("lava", (240, 110, 20)), ("red_nether", (110, 20, 20)),
    ("nether_brick", (60, 30, 35)), ("red_concrete", (150, 30, 30)), ("red_", (170, 40, 40)), ("bone", (220, 215, 190)),
    ("prismarine", (90, 160, 150)), ("dark_prismarine", (50, 100, 90)), ("copper", (190, 110, 70)), ("iron_block", (215, 215, 215)),
    ("iron_bars", (160, 160, 160)), ("chain", (90, 90, 90)), ("mossy", (100, 120, 90)), ("moss", (90, 130, 50)),
    ("stone_brick", (125, 125, 125)), ("cobble", (115, 115, 115)), ("andesite", (135, 135, 135)), ("stone", (128, 128, 128)),
    ("mangrove", (115, 55, 50)), ("mud", (90, 75, 65)), ("spruce", (110, 80, 50)), ("dark_oak", (65, 45, 25)),
    ("oak", (160, 130, 80)), ("terracotta", (210, 180, 160)), ("white_terracotta", (215, 185, 170)), ("blue_terracotta", (75, 60, 95)),
    ("wool", (200, 200, 200)), ("yellow", (230, 200, 60)), ("orange", (230, 130, 40)), ("brown", (110, 75, 45)),
    ("grass", (100, 160, 70)), ("podzol", (95, 65, 35)), ("dirt", (120, 85, 60)), ("soul", (85, 65, 50)), ("gravel", (130, 125, 120)),
    ("mycelium", (120, 100, 120)), ("mushroom_stem", (210, 205, 195)), ("red_mushroom_block", (190, 40, 40)),
    ("brown_mushroom_block", (150, 110, 80)), ("leaves", (60, 140, 60)), ("froglight", (120, 220, 120)), ("shroomlight", (240, 160, 80)),
    ("glass", (180, 210, 230)), ("sand", (220, 205, 150)), ("hay", (200, 170, 40)), ("water", (50, 90, 200)), ("bookshelf", (140, 100, 60)),
]
SKIP = ("air", "structure_void")


def couleur(bid):
    n = bid.split(":")[1]
    for k, c in COUL:
        if k in n:
            return c
    return (150, 150, 150)


def rendre(path, s=4):
    f = nbtlib.load(path)
    pal = [str(p["id"]) for p in f["palette"]]
    sx, sy, sz = [int(v) for v in f["size"]]
    vox = []
    for b in f["blocks"]:
        bid = pal[int(b["state"])]
        if bid.split(":")[1] in SKIP:
            continue
        x, y, z = [int(v) for v in b["pos"]]
        vox.append((x, y, z, couleur(bid)))
    W = (sx + sz) * s * 2 + 20
    H = (sx + sz) * s + sy * s * 2 + 20
    img = Image.new("RGB", (W, H), (28, 30, 36))
    d = ImageDraw.Draw(img)
    ox, oy = sz * s * 2 + 10, sy * s * 2 + 10
    vox.sort(key=lambda v: (v[0] + v[2], v[1]))
    for x, y, z, c in vox:
        px = ox + (x - z) * s * 2
        py = oy + (x + z) * s - y * s * 2
        top = [(px, py), (px + 2 * s, py + s), (px, py + 2 * s), (px - 2 * s, py + s)]
        left = [(px - 2 * s, py + s), (px, py + 2 * s), (px, py + 4 * s), (px - 2 * s, py + 3 * s)]
        right = [(px + 2 * s, py + s), (px, py + 2 * s), (px, py + 4 * s), (px + 2 * s, py + 3 * s)]
        d.polygon(top, fill=c)
        d.polygon(left, fill=tuple(int(v * 0.75) for v in c))
        d.polygon(right, fill=tuple(int(v * 0.55) for v in c))
    return img


if __name__ == "__main__":
    paths = sorted(glob.glob("/home/claude/aos/out/RoyaumesMortels/data/royaumes/structure/*.nbt"))
    imgs = []
    for p in paths:
        im = rendre(p, 3)
        im.thumbnail((420, 420))
        canvas = Image.new("RGB", (420, 450), (28, 30, 36))
        canvas.paste(im, ((420 - im.width) // 2, 30 + (420 - im.height) // 2))
        ImageDraw.Draw(canvas).text((10, 8), os.path.basename(p)[:-4], fill=(240, 220, 150))
        imgs.append(canvas)
    cols = 5
    rows = (len(imgs) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * 420, rows * 450), (28, 30, 36))
    for i, im in enumerate(imgs):
        sheet.paste(im, ((i % cols) * 420, (i // cols) * 450))
    sheet.save("/home/claude/aos/out/apercu_structures.png")
    print(sheet.size)
