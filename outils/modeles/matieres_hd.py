# -*- coding: utf-8 -*-
"""Peinture HD des matières (4 texels par pixel de modèle), utilisée par modele2.Modele.peindre.

Chaque face est peinte directement à la haute résolution, avec la vraie matière du cube (pas devinée) :
- métal : biseau (arête claire en haut à gauche, sombre en bas à droite), métal brossé, bande de reflet,
  rivets aux coins des grandes plaques, rayures et éclats d'usure sur les bords ;
- or : comme le métal, plus des gravures en volutes sur les grandes plaques et des ombres chaudes ;
- tissu : trame, plis verticaux, ourlet cousu ; cuir : grain, taches, coutures, bord roulé ;
- peau : marbrures douces, creux ombrés ; écailles : rangées d'écailles qui se chevauchent, ventre clair ;
- os : pores, fêlures, bords jaunis ; bois : veines, nœuds, cernes sur les sections ;
- fourrure : mèches et pointes ; pierre : grain, fissures ; chaîne : mailles ; plumes : rachis et barbes ;
- membrane : nervures ; éther : volutes et bas effiloché ; lueur : cœur blanc ; corne : anneaux et stries.
Les dessins des faces (emblèmes, yeux, runes…) sont tracés en basse résolution puis agrandis en Scale2x
(diagonales lissées) et légèrement embossés."""
import math

import numpy as np
from scipy import ndimage

LUM = {"up": 1.14, "down": 0.62, "north": 1.0, "south": 0.84, "east": 0.9, "west": 0.9}


def _bruit(rng, h, w, s=0.0, axe=None):
    """Bruit blanc lissé, normalisé analytiquement (une petite face ne doit pas faire exploser l'écart-type)."""
    n = rng.normal(0, 1, (h, w))
    if s:
        if axe is None:
            n = ndimage.gaussian_filter(n, s, mode="wrap") * (2 * math.sqrt(math.pi) * s)
        else:
            n = ndimage.gaussian_filter1d(n, s, axis=axe, mode="wrap") * math.sqrt(2 * math.sqrt(math.pi) * s)
    return np.clip(n, -3, 3)


def _marche(rng, k, h, w, n, longueur, facteur, diag=True):
    """Fêlures / rayures : marches aléatoires fines."""
    for _ in range(n):
        x, y = rng.integers(0, w), rng.integers(0, h)
        dx = rng.choice((-1, 1))
        for _ in range(longueur):
            if 0 <= x < w and 0 <= y < h:
                k[y, x] *= facteur
            y += 1
            x += dx if (diag and rng.random() < 0.6) else int(rng.integers(-1, 2))


def peindre_face(arr, x0, y0, w, h, face, m, rng):
    """Peint la face HD (x0, y0, w, h) de arr (tableau flottant H×W×4) avec la matière m."""
    typ, c = m["type"], np.array(m["c"][:3], float)
    c2 = m.get("c2")
    I, J = np.meshgrid(np.arange(w), np.arange(h))
    cote = face not in ("up", "down")
    k = np.full((h, w), LUM[face], float)
    if cote:
        k *= 1.0 + 0.13 * (0.5 - J / max(1, h - 1))
    de = np.minimum(np.minimum(I, w - 1 - I), np.minimum(J, h - 1 - J))   # distance au bord de la face
    haut_g = (I == 0) | (J == 0)
    bas_d = (I == w - 1) | (J == h - 1)
    col = np.broadcast_to(c, (h, w, 3)).copy()
    alpha = np.full((h, w), 255.0)
    fin = _bruit(rng, h, w)
    doux = _bruit(rng, h, w, 2.5)
    seed = rng.random() * 100
    grand = w >= 10 and h >= 10

    if typ in ("metal", "or"):
        brosse = _bruit(rng, h, w, 4, axe=1)
        k *= 1 + 0.035 * brosse + 0.02 * fin
        k *= 0.88 + 0.12 * np.clip(de / 4, 0, 1)                                  # plaque bombée
        hg = (np.minimum(I, J) <= np.minimum(w - 1 - I, h - 1 - J))
        k = np.where(de == 0, k * 0.74, k)                                         # ligne entre les plaques
        k = np.where((de == 1) & hg, k * 1.38, k)                                  # arête éclaircie
        k = np.where((de == 1) & ~hg, k * 0.72, k)                                 # arête dans l'ombre
        k = np.where((de == 2) & hg, k * 1.1, k)
        if cote and h >= 8:
            k *= 1 + 0.18 * np.exp(-((J / h - 0.22) ** 2) / 0.004)               # bande de reflet
        if grand:
            for (rx, ry) in ((3, 3), (w - 5, 3), (3, h - 5), (w - 5, h - 5)):  # rivets
                k[ry, rx] *= 1.5
                k[ry, rx + 1] *= 1.2
                k[ry + 1, rx] *= 1.2
                k[ry + 1, rx + 1] *= 0.95
                if ry + 2 < h and rx + 2 < w:
                    k[ry + 2, rx + 1:rx + 3] *= 0.72
        _marche(rng, k, h, w, (w * h) // (420 if typ == "metal" else 700), int(rng.integers(3, 8)), 1.16)
        usure = (de <= 1) & (rng.random((h, w)) < 0.14)
        k = np.where(usure, k * 1.18, k)
        if typ == "or" and w >= 14 and h >= 14 and face != "down":
            volute = np.sin(I * 0.85 + 2.2 * np.sin(J * 0.42 + seed)) > 0.955
            volute &= de >= 3
            k = np.where(volute, k * 0.74, k)
            k = np.where(np.roll(volute, -1, axis=0) & ~volute, k * 1.12, k)
    elif typ == "tissu":
        k *= 1 + 0.035 * (((I + J) % 2) * 2 - 1) + 0.03 * fin
        if cote:
            periode = max(6.0, w / 3.0)
            k *= 1 + 0.12 * np.sin(2 * math.pi * I / periode + seed)               # plis
            k = np.where(J >= h - 2, k * 0.72, k)                                   # ourlet
            k = np.where((J == h - 3) & (I % 3 != 0), k * 1.1, k)
        k = np.where(de == 0, k * 0.86, k)
    elif typ == "cuir":
        k *= 1 + 0.06 * fin + 0.08 * doux
        k = np.where(de == 0, k * 0.74, k)
        k = np.where((de == 1) & ((I == 1) | (J == 1)), k * 1.1, k)
        if w >= 8 and h >= 8:
            couture = (de == 2) & ((I + J) % 3 == 0)
            k = np.where(couture, k * 1.32, k)
        k = np.where(rng.random((h, w)) < 0.02, k * 1.2, k)
    elif typ == "peau":
        k *= 1 + 0.07 * doux + 0.03 * fin
        k = np.where(de == 0, k * 0.86, np.where(de == 1, k * 0.95, k))
        col[..., 0] = np.minimum(255, col[..., 0] * (1 + 0.04 * (de <= 1)))
    elif typ == "ecaille":
        # écailles arrondies en quinconce (6 × 4 texels) : reflet en haut, liseré sombre en arc en bas
        rang = J // 4
        dec = (rang % 2) * 3
        u, v = (I + dec) % 6, J % 4
        ident = ((I + dec) // 6) * 131 + rang * 977
        var = np.sin(ident * 12.9898 + seed) * 43758.5453
        var = (var - np.floor(var)) - 0.5
        dist = ((u - 2.5) / 3.0) ** 2 + ((v - 0.6) / 3.2) ** 2
        k *= 1.1 - 0.42 * np.clip(dist, 0, 1) + 0.12 * var + 0.025 * fin
        k = np.where((v == 0) & (np.abs(u - 2.5) < 1.6), k * 1.12, k)
        ventre = np.ones((h, w), bool) if face == "down" else (J > h * 0.62)
        if c2 is not None and cote or (c2 is not None and face == "down"):
            col[ventre] = np.array(c2[:3], float)
            k = np.where(ventre, LUM[face] * (1 + 0.03 * fin) * np.where(J % 3 == 2, 0.88, 1.0), k)
    elif typ == "os":
        k *= 1 + 0.05 * fin + 0.05 * doux
        k = np.where(rng.random((h, w)) < 0.03, k * 0.74, k)
        _marche(rng, k, h, w, 1 + (w * h) // 500, max(3, (w + h) // 4), 0.62, diag=False)
        jauni = de <= 1
        col[jauni] = col[jauni] * 0.7 + np.array([190, 160, 110]) * 0.3
        k = np.where(de == 0, k * 0.82, k)
    elif typ == "bois":
        k *= 1 + 0.05 * fin
        if cote:
            long = h >= w
            a, b = (I, J) if long else (J, I)
            veine = np.sin(a * 1.3 + 2.2 * np.sin(b * 0.15 + seed))
            k = np.where(veine > 0.72, k * 0.74, np.where(veine < -0.85, k * 1.1, k))
            if w * h > 150:
                nx, ny = rng.integers(2, max(3, w - 2)), rng.integers(2, max(3, h - 2))
                dn = np.hypot((I - nx) / 1.6, (J - ny) / 2.6)
                k = np.where((dn > 0.8) & (dn < 1.6), k * 0.7, np.where(dn <= 0.8, k * 0.85, k))
        else:
            dc = np.hypot(I - (w - 1) / 2, J - (h - 1) / 2)
            k *= 1 + 0.1 * np.sin(dc * 1.4 + seed)                                   # cernes
        k = np.where(de == 0, k * 0.82, k)
    elif typ == "fourrure":
        # mèches courtes (bruit étiré verticalement), touffes, pointes sombres irrégulières
        meche = ndimage.gaussian_filter(rng.normal(0, 1, (h, w)), (1.8, 0.55), mode="wrap") * (2 * math.sqrt(math.pi) * math.sqrt(1.8 * 0.55))
        k *= 1 + 0.08 * np.clip(meche, -3, 3) + 0.12 * doux
        decal = rng.integers(0, 6, w)[None, :]
        k = np.where(((J + decal) % 6 == 5) & (meche > -0.2), k * 0.84, k)
        k = np.where(((J + decal) % 6 == 0) & (meche > 0.3), k * 1.08, k)
    elif typ == "pierre":
        k *= 1 + 0.08 * fin + 0.1 * doux
        _marche(rng, k, h, w, 1 + (w * h) // 400, max(3, (w + h) // 3), 0.62, diag=False)
        k = np.where((de == 0) & (rng.random((h, w)) < 0.5), k * 0.78, np.where(de == 0, k * 0.88, k))
    elif typ == "ether":
        k *= 1.0 + 0.2 * np.sin(I * 0.45 + J * 0.2 + seed) + 0.05 * doux
        if cote:
            p = np.clip((J - (h - 5)) / 4.0, 0, 1) * 0.6
            alpha = np.where(rng.random((h, w)) < p, 0, alpha)
    elif typ == "lueur":
        cx, cy = (w - 1) / 2, (h - 1) / 2
        dd = np.hypot((I - cx) / max(1, w / 2), (J - cy) / max(1, h / 2))
        k = 1.15 - 0.3 * dd + 0.02 * fin
        coeur = np.clip(0.35 - dd, 0, None)[..., None]
        col = col + (255 - col) * coeur * 0.7
    elif typ == "corne":
        if cote:
            k = LUM[face] * (0.8 + 0.4 * (1 - J / max(1, h - 1)))
        k = np.where(J % 5 == 0, k * 0.88, k)
        k *= 1 + 0.04 * _bruit(rng, h, w, 3, axe=0)
    elif typ == "sombre":
        k *= 1 + 0.03 * fin
        k = np.where(haut_g & ~bas_d, k * 1.6, k)
    elif typ == "chaine":
        u, v = I % 4, (J + (I // 4) % 2 * 2) % 4
        anneau = (u == 0) | (u == 3) | (v == 0) | (v == 3)
        k = np.where(anneau, k, k * 0.45)
        k = np.where(anneau & (u == 0) & (v <= 1), k * 1.3, k)
        k *= 1 + 0.03 * fin
    elif typ == "plume":
        v = J % 6
        u = (I + ((J // 6) % 2) * 3) % 6
        k *= 1.08 - 0.05 * v
        k = np.where(u == 3, k * 1.12, k)
        k = np.where(v == 5, k * 0.78, np.where(u == 0, k * 0.9, k))
        k *= 1 + 0.03 * fin
    elif typ == "membrane":
        nervure = (I % 10 == 0) | (np.abs((I % 10) - (J * 0.4) % 10) < 0.6)
        k = np.where(nervure, k * 0.72, k)
        k *= 1 + 0.08 * doux
    else:
        k *= 1 + 0.03 * fin

    rgb = col * k[..., None]
    if typ == "or":  # ombres chaudes
        rgb[..., 2] *= np.clip(0.88 + 0.12 * k, 0.8, 1.05)
    region = arr[y0:y0 + h, x0:x0 + w]
    region[..., :3] = np.clip(rgb, 0, 255)
    region[..., 3] = alpha


def epx_face(lo):
    """Scale2x sur une face basse résolution (couleurs exactes, alpha compris)."""
    h, w = lo.shape[:2]
    ident = (lo[..., 0].astype(np.int64) << 24) | (lo[..., 1].astype(np.int64) << 16) | (lo[..., 2].astype(np.int64) << 8) | lo[..., 3]
    L = np.pad(ident, 1, mode="edge")
    P = np.pad(lo, ((1, 1), (1, 1), (0, 0)), mode="edge")
    A, B, C, D = L[:-2, 1:-1], L[1:-1, 2:], L[1:-1, :-2], L[2:, 1:-1]
    cA, cB, cC, cD = P[:-2, 1:-1], P[1:-1, 2:], P[1:-1, :-2], P[2:, 1:-1]
    out = np.repeat(np.repeat(lo, 2, 0), 2, 1)
    for (dj, di), m, nc in (((0, 0), (C == A) & (C != D) & (A != B), cA), ((0, 1), (A == B) & (A != C) & (B != D), cB),
                            ((1, 0), (D == C) & (D != B) & (C != A), cC), ((1, 1), (B == D) & (B != A) & (D != C), cD)):
        vue = out[dj::2, di::2]
        vue[m] = nc[m]
    return out


def decors_hd(arr, lo, base, x0, y0, w, h, face, couleur_matiere=None):
    """Reporte en HD les dessins de la face (pixels où lo diffère de la peinture de base), lissés et embossés."""
    f_lo = lo[y0:y0 + h, x0:x0 + w]
    f_base = base[y0:y0 + h, x0:x0 + w]
    masque = (f_lo != f_base).any(axis=2)
    if not masque.any():
        return None
    # le masque suit les mêmes choix Scale2x que les couleurs : on l'encode dans un canal de plus
    marque = np.dstack([f_lo, masque.astype(np.uint8)])
    hd = epx_face(marque)
    m = hd[..., 4] > 0
    couleur = hd[..., :4].astype(float)
    region = arr[2 * y0:2 * (y0 + h), 2 * x0:2 * (x0 + w)]
    if couleur_matiere is not None:
        # le dessin reprend le modelé et le grain de la matière peinte dessous (brossé, trame, biseau…)
        ref = max(1.0, float(np.mean(couleur_matiere[:3])))
        k = np.clip(region[..., :3].mean(axis=2) / ref, 0.45, 1.6)
    else:
        k = np.full(m.shape, LUM[face])
        if face not in ("up", "down"):
            J = np.arange(m.shape[0])[:, None]
            k = k * (1.0 + 0.13 * (0.5 - J / max(1, m.shape[0] - 1)))
    dessus = m & ~np.roll(m, 1, axis=0)
    dessous = m & ~np.roll(m, -1, axis=0)
    k = np.where(dessus, k * 1.22, np.where(dessous, k * 0.76, k))
    region[m, :3] = np.clip(couleur[m, :3] * k[m, None], 0, 255)
    region[m, 3] = couleur[m, 3]
    return m, couleur
