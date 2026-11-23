# -*- coding: utf-8 -*-
"""Rendu isométrique texturé (textures Minecraft 26.3) des structures et échantillons de biomes."""
import json, os, math
from functools import lru_cache
from PIL import Image, ImageDraw, ImageEnhance
import nbtlib

A = "/tmp/mc-assets/assets/minecraft"
TINT_HERBE = (124, 189, 80)
TINT_FEUILLE = (90, 160, 60)
TINT_EAU = (63, 118, 228)
CROSS = {"cross", "tinted_cross", "flower_pot_cross", "crop", "stem_fruit", "cross_emissive"}
TRANSP = ("glass", "leaves", "pane", "bars", "water", "ice", "slime", "honey", "chain", "fence", "wall", "torch", "lantern",
          "rod", "carpet", "slab", "stairs", "ladder", "vine", "door", "trapdoor", "candle", "head", "skull", "bell", "web",
          "lichen", "roots", "moss_carpet", "pickle", "coral", "kelp", "seagrass", "campfire", "fire", "banner", "bed",
          "anvil", "cauldron", "lectern", "grindstone", "brewing", "dripstone", "cluster", "egg", "lily", "flower",
          "mushroom", "bush", "grass", "fern", "sapling", "tulip", "orchid", "allium", "valley", "daisy", "azalea",
          "hanging", "pot", "end_rod", "conduit", "beacon", "enchanting", "chest", "barrel", "litter", "scaffold", "grate")


def png(nom):
    if ":" in nom:
        nom = nom.split(":", 1)[1]
    p = f"{A}/textures/{nom}.png"
    if not os.path.exists(p):
        return None
    im = Image.open(p).convert("RGBA")
    if im.height > im.width:
        im = im.crop((0, 0, im.width, im.width))
    return im.resize((16, 16), Image.NEAREST) if im.width != 16 else im


def teinter(im, c):
    r, g, b, a = im.split()
    gris = Image.merge("RGB", (r, g, b)).convert("L")
    out = Image.merge("RGBA", (gris.point(lambda v: v * c[0] // 255), gris.point(lambda v: v * c[1] // 255),
                               gris.point(lambda v: v * c[2] // 255), a))
    return out


@lru_cache(None)
def modele(mid):
    if ":" in mid:
        mid = mid.split(":", 1)[1]
    p = f"{A}/models/{mid}.json"
    if not os.path.exists(p):
        return {}, []
    d = json.load(open(p))
    tex, parents = {}, [mid]
    if "parent" in d:
        t2, p2 = modele(d["parent"])
        tex.update(t2); parents += p2
    tex.update(d.get("textures", {}))
    return tex, parents


def resoudre(ref, tex, prof=0):
    while prof < 10:
        if isinstance(ref, dict):
            ref = ref.get("sprite")
        if ref and isinstance(ref, str) and ref.startswith("#"):
            ref = tex.get(ref[1:]); prof += 1
            continue
        break
    return ref if isinstance(ref, str) else None


@lru_cache(None)
def faces(etat):
    """Retourne (texture_dessus, texture_côté, genre)."""
    bid = etat.split("[")[0].split(":")[1]
    props = {}
    if "[" in etat:
        props = dict(kv.split("=") for kv in etat[:-1].split("[", 1)[1].split(","))
    if bid in ("water",):
        t = teinter(png("block/water_still"), TINT_EAU)
        return t, t, "eau"
    if bid == "lava":
        t = png("block/lava_still")
        return t, t, "cube"
    if bid in ("air", "cave_air", "void_air", "structure_void", "light", "barrier"):
        return None, None, "vide"
    bsp = f"{A}/blockstates/{bid}.json"
    mid = None
    if os.path.exists(bsp):
        bs = json.load(open(bsp))
        if "variants" in bs:
            choix = None
            for k, v in bs["variants"].items():
                conds = dict(c.split("=") for c in k.split(",") if "=" in c)
                if all(props.get(a) == b for a, b in conds.items()):
                    choix = v; break
            if choix is None:
                choix = next(iter(bs["variants"].values()))
            if isinstance(choix, list):
                choix = choix[0]
            mid = choix["model"]
        elif "multipart" in bs:
            for part in bs["multipart"]:
                ap = part["apply"]
                ap = ap[0] if isinstance(ap, list) else ap
                mid = ap["model"]
                if "when" not in part:
                    break
    if bid.endswith("mushroom_block") or bid == "mushroom_stem":
        t = png(f"block/{bid}")
        return t, t, "cube"
    tex, parents = modele(mid) if mid else ({}, [])
    genre = "cube"
    if any(p.split("/")[-1] in CROSS for p in parents):
        genre = "croix"
    def premier(*cles):
        for k in cles:
            r = resoudre(tex.get(k), tex)
            if r:
                return r
        return None
    dessus = premier("up", "top", "end", "all", "texture", "cross", "plant", "pattern", "particle", "side")
    cote = premier("north", "side", "all", "texture", "cross", "plant", "front", "particle", "top")
    if props.get("axis") in ("x", "z") and genre == "cube":
        dessus = cote
    td, tc = (png(dessus) if dessus else None), (png(cote) if cote else None)
    if td is None and tc is None:
        tc = td = png(f"block/{bid}")
    td = td or tc; tc = tc or td
    if td is None:
        c = Image.new("RGBA", (16, 16), (150, 150, 150, 255))
        td = tc = c
    teinte = None
    if "leaves" in bid and not any(k in bid for k in ("cherry", "azalea", "pale")):
        teinte = TINT_FEUILLE
    elif bid in ("vine", "short_grass", "tall_grass", "fern", "large_fern", "lily_pad", "sugar_cane"):
        teinte = TINT_HERBE
    if teinte:
        td, tc = teinter(td, teinte), teinter(tc, teinte)
    if bid == "grass_block":
        td = teinter(png("block/grass_block_top"), TINT_HERBE)
        tc = png("block/grass_block_side")
    if any(k in bid for k in ("pane", "bars", "chain", "fence", "_wall", "rod", "torch", "lantern", "ladder", "candle", "pickle",
                              "dripstone", "cluster", "web", "bell", "skull", "head", "campfire", "fire", "banner", "lichen",
                              "hanging", "carpet")) and genre == "cube":
        genre = "fin"
    return td, tc, genre


def sprite_cube(td, tc, s, mask, alpha=255):
    W = 4 * s
    img = Image.new("RGBA", (W, W), (0, 0, 0, 0))
    if mask & 1:
        top = td.transform((W, W), Image.AFFINE, (4 / s, 8 / s, -8, -4 / s, 8 / s, 8), resample=Image.NEAREST)
        img.alpha_composite(top)
    if mask & 2:
        g = tc.transform((W, W), Image.AFFINE, (8 / s, 0, 0, -4 / s, 8 / s, -8), resample=Image.NEAREST)
        g = ImageEnhance.Brightness(g).enhance(0.82)
        img.alpha_composite(g)
    if mask & 4:
        d = tc.transform((W, W), Image.AFFINE, (8 / s, 0, -16, 4 / s, 8 / s, -24), resample=Image.NEAREST)
        d = ImageEnhance.Brightness(d).enhance(0.64)
        img.alpha_composite(d)
    if alpha < 255:
        a = img.split()[3].point(lambda v: v * alpha // 255)
        img.putalpha(a)
    return img


_cache = {}


def sprite(etat, s, mask):
    k = (etat, s, mask)
    if k in _cache:
        return _cache[k]
    td, tc, genre = faces(etat)
    if genre == "vide":
        sp = None
    elif genre == "croix":
        t = tc.resize((2 * s, 2 * s), Image.NEAREST)
        sp = Image.new("RGBA", (4 * s, 4 * s)); sp.alpha_composite(t, (s, s + s // 2))
    elif genre == "fin":
        sp = sprite_cube(td, tc, s, mask)
        sp = sp.resize((2 * s, 2 * s), Image.NEAREST)
        c = Image.new("RGBA", (4 * s, 4 * s)); c.alpha_composite(sp, (s, 2 * s)); sp = c
    elif genre == "eau":
        sp = sprite_cube(td, tc, s, mask & 1 or 1, alpha=190)
    else:
        sp = sprite_cube(td, tc, s, mask)
    _cache[k] = sp
    return sp


def opaque(etat):
    if etat is None:
        return False
    bid = etat.split("[")[0].split(":")[1]
    return not any(k in bid for k in TRANSP) and bid not in ("air", "lava")


def rendre_blocs(blocs, taille, s=6, fond=(24, 26, 32, 255), titre=None):
    sx, sy, sz = taille
    Wd = (sx + sz) * 2 * s + 8 * s
    Ht = (sx + sz) * s + sy * 2 * s + 8 * s
    img = Image.new("RGBA", (Wd, Ht), fond)
    ox, oy = sz * 2 * s + 4 * s, sy * 2 * s + 2 * s
    ordre = sorted(blocs.items(), key=lambda kv: (kv[0][0] + kv[0][2], kv[0][1]))
    for (x, y, z), etat in ordre:
        if etat.endswith(":air") or ":air[" in etat:
            continue
        mask = 0
        if not opaque(blocs.get((x, y + 1, z))):
            mask |= 1
        if not opaque(blocs.get((x, y, z + 1))):
            mask |= 2
        if not opaque(blocs.get((x + 1, y, z))):
            mask |= 4
        if mask == 0:
            continue
        sp = sprite(etat, s, mask)
        if sp is None:
            continue
        px = ox + (x - z) * 2 * s - 2 * s
        py = oy + (x + z) * s - y * 2 * s
        img.alpha_composite(sp, (int(px), int(py)))
    bb = img.getbbox()
    fond_img = Image.new("RGBA", img.size, fond)
    diff = Image.new("RGBA", img.size)
    # recadrage sur le contenu
    from PIL import ImageChops
    bbox = ImageChops.difference(img.convert('RGB'), fond_img.convert('RGB')).getbbox()
    if bbox:
        m = 3 * s
        img = img.crop((max(0, bbox[0] - m), max(0, bbox[1] - m), min(img.width, bbox[2] + m), min(img.height, bbox[3] + m)))
    if titre:
        from PIL import ImageFont
        police = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf", 22)
        tw = int(ImageDraw.Draw(img).textlength(titre, font=police)) + 30
        largeur = max(img.width, tw)
        out = Image.new("RGBA", (largeur, img.height + 40), fond)
        ImageDraw.Draw(out).text((14, 8), titre, fill=(240, 220, 150, 255), font=police)
        out.alpha_composite(img, ((largeur - img.width) // 2, 40))
        img = out
    return img


def lire_nbt(path):
    f = nbtlib.load(path)
    pal = []
    for p in f["palette"]:
        props = p.get("properties")
        st = str(p["id"])
        if props:
            st += "[" + ",".join(f"{k}={v}" for k, v in props.items()) + "]"
        pal.append(st)
    blocs = {}
    for b in f["blocks"]:
        x, y, z = (int(v) for v in b["pos"])
        blocs[(x, y, z)] = pal[int(b["state"])]
    return blocs, tuple(int(v) for v in f["size"])


def rendre_structure(path, s=6, titre=None):
    blocs, taille = lire_nbt(path)
    return rendre_blocs(blocs, taille, s, titre=titre)
