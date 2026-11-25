# -*- coding: utf-8 -*-
"""Icônes d'armure dessinées directement en 32 × 32 (0.24) : silhouette nette, contour sombre, plaques bombées
éclairées en haut à gauche, liserés de la couleur de faction, rivets, visière propre à chaque alliance
(fente en T de l'Ordre, cornes du Chaos, orbites de la Mort, défenses de la Destruction), gemme des paliers
Mythique et Divin. Utilisé par arsenal.py à la place des icônes 16 px agrandies."""
import numpy as np
from PIL import Image, ImageDraw
from scipy import ndimage

N = 32
LUM = np.array([-0.55, -0.62, 0.56])
LUM = LUM / np.linalg.norm(LUM)


def _masque(dessin):
    im = Image.new("L", (N, N), 0)
    dessin(ImageDraw.Draw(im))
    return np.array(im) > 0


def _silhouette(piece):
    if piece == "casque":
        return _masque(lambda d: (d.ellipse((6, 4, 25, 23), fill=1), d.rectangle((6, 13, 25, 27), fill=1)))
    if piece == "torse":
        return _masque(lambda d: (d.polygon([(4, 6), (11, 3), (20, 3), (27, 6), (28, 14), (23, 15), (23, 29), (8, 29), (8, 15), (3, 14)], fill=1),
                                  d.polygon([(12, 3), (19, 3), (16, 8)], fill=0)))
    if piece == "jambes":
        return _masque(lambda d: (d.rectangle((7, 4, 24, 11), fill=1), d.polygon([(7, 11), (15, 11), (14, 29), (8, 29)], fill=1),
                                  d.polygon([(16, 11), (24, 11), (23, 29), (17, 29)], fill=1)))
    return _masque(lambda d: (d.polygon([(4, 15), (11, 15), (11, 23), (14, 24), (14, 28), (3, 28)], fill=1),
                              d.polygon([(20, 15), (27, 15), (28, 28), (17, 28), (17, 24), (20, 23)], fill=1)))


def armure(piece, c1, c2, tier, alliance, graine=0):
    rng = np.random.default_rng(graine)
    m = _silhouette(piece)
    c1 = np.array(c1, float)
    c2 = np.array(c2, float)
    out = np.zeros((N, N, 4))
    out[m, :3] = c1
    deco = np.zeros((N, N), bool)          # pixels de liseré (couleur c2)
    sombre = np.zeros((N, N), bool)        # fentes et creux
    J, I = np.mgrid[0:N, 0:N]
    if piece == "casque":
        deco |= m & (np.abs(I - 15.5) < 1.2) & (J < 16)                        # crête
        deco |= m & (J >= 25)                                                  # bord inférieur
        if alliance == "ordre":
            sombre |= m & (((J >= 15) & (J <= 16) & (np.abs(I - 15.5) < 7)) | ((np.abs(I - 15.5) < 1.2) & (J >= 15) & (J <= 22)))
        elif alliance == "chaos":
            sombre |= m & (J >= 15) & (J <= 16) & (np.abs(I - 15.5) < 7) & ((I + J) % 3 != 0)
            corne = _masque(lambda d: (d.polygon([(6, 12), (1, 4), (2, 1), (8, 9)], fill=1), d.polygon([(25, 12), (30, 4), (29, 1), (23, 9)], fill=1)))
            out[corne & ~m, :3] = np.array([226, 214, 180.0])
            m = m | corne
        elif alliance == "mort":
            for cx in (11.5, 19.5):
                sombre |= m & ((I - cx) ** 2 / 6 + (J - 16) ** 2 / 5 <= 1)
            sombre |= m & (np.abs(I - 15.5) < 1) & (J >= 19) & (J <= 21)
        else:
            sombre |= m & (J >= 15) & (J <= 17) & (np.abs(I - 15.5) < 8)
            for cx in (9, 22):
                dent = (np.abs(I - cx) < 1.1) & (J >= 22) & (J <= 26)
                out[dent, :3] = np.array([236, 228, 200.0])
                m = m | dent
    elif piece == "torse":
        deco |= m & (np.abs(I - 15.5) < 1.2) & (J > 8)                          # arête du plastron
        deco |= m & (J >= 27)
        deco |= m & (J <= 7) & ((I <= 8) | (I >= 23))                          # bords des épaulières
        sombre |= m & (J == 15) & (I > 8) & (I < 23)                           # ceinture des plaques
        sombre |= m & (J == 21) & (I > 8) & (I < 23)
    elif piece == "jambes":
        deco |= m & (J <= 6)
        deco |= m & (J >= 18) & (J <= 19)                                      # genouillères
        sombre |= m & (J == 12)
    else:
        deco |= m & (J >= 27)
        deco |= m & (J <= 16)
        sombre |= m & (J == 22) & ((I < 11) | (I > 20))
    out[deco & m, :3] = c2
    out[sombre & m, :3] = np.array([24, 20, 28.0])
    # relief : bombé de la silhouette, éclairé en haut à gauche
    h = ndimage.gaussian_filter(np.minimum(ndimage.distance_transform_edt(m), 4.0) + 0.6 * (~sombre), 1.0)
    gy, gx = np.gradient(h)
    nrm = np.dstack([-gx, -gy, np.full_like(gx, 0.9)])
    nrm /= np.linalg.norm(nrm, axis=2, keepdims=True)
    e = nrm @ LUM - LUM[2]
    metal = 0.95 if alliance != "mort" else 0.75
    k = 1 + metal * np.clip(e, None, 0) * 1.2
    clair = np.clip(e, 0, None) * metal
    for c in range(3):
        v = out[:, :, c]
        out[:, :, c] = np.where(m & ~sombre, (v + (255 - v) * clair * 0.8) * k * (1 + 0.03 * rng.normal(0, 1, (N, N))), v)
    # rivets
    for (x, y) in {"casque": [(9, 20), (22, 20)], "torse": [(10, 10), (21, 10), (10, 25), (21, 25)],
                   "jambes": [(9, 8), (22, 8)], "bottes": [(6, 18), (25, 18)]}.get(piece, []):
        if m[y, x]:
            out[y, x, :3] = np.minimum(255, c2 * 1.3 + 30)
            if y + 1 < N and x + 1 < N and m[y + 1, x + 1]:
                out[y + 1, x + 1, :3] *= 0.6
    # contour sombre teinté
    bord = m & ~ndimage.binary_erosion(m)
    out[bord, :3] = np.clip(c1 * 0.28, 0, 255)
    out[m, 3] = 255
    # gemme (Mythique, Divin) et éclat des paliers supérieurs
    if tier >= 3:
        gem = np.array([60, 215, 240.0]) if tier == 3 else np.array([255, 176, 48.0])
        gx_, gy_ = {"casque": (15, 9), "torse": (15, 11), "jambes": (15, 8), "bottes": (7, 20)}.get(piece, (15, 12))
        for dy in range(2):
            for dx in range(2):
                out[gy_ + dy, gx_ + dx, :3] = gem * (1.2 if (dx, dy) == (0, 0) else 0.75 if (dx, dy) == (1, 1) else 1.0)
    if tier >= 2:
        etoile = np.array([255, 245, 180.0]) if tier < 4 else np.array([255, 255, 255.0])
        for (x, y) in ((1, 1), (2, 1), (1, 2), (0, 1), (1, 0)):
            out[y, x, :3] = etoile
            out[y, x, 3] = 255 if (x, y) == (1, 1) else 170
    return Image.fromarray(np.clip(out, 0, 255).astype(np.uint8))
