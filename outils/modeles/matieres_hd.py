# -*- coding: utf-8 -*-
"""Peinture HD des matières (4 texels par pixel de modèle), utilisée par modele2.Modele.peindre.

Chaque face est peinte directement à la haute résolution, avec la vraie matière du cube (pas devinée) :
- métal : biseau (arête claire en haut à gauche, sombre en bas à droite), métal brossé, bande reflet,
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


def _hash(n, graine):
    v = np.sin(n * 12.9898 + graine * 78.233) * 43758.5453
    return v - np.floor(v)


def _voronoi(I, J, pas, graine):
    """Distances au germe le plus proche et au suivant, identifiant de cellule, écart vertical au germe."""
    rang_h = pas * 0.86
    gy0 = np.floor(J / rang_h).astype(int)
    d1 = np.full(I.shape, 1e9)
    d2 = np.full(I.shape, 1e9)
    ident = np.zeros(I.shape)
    dy = np.zeros(I.shape)
    for oy in (-1, 0, 1):
        gy = gy0 + oy
        decal = (gy % 2) * 0.5
        gx0 = np.floor(I / pas - decal).astype(int)
        for ox in (-1, 0, 1):
            gx = gx0 + ox
            n = gx * 157 + gy * 1013
            cx = (gx + 0.5 + decal) * pas + (_hash(n, graine) - 0.5) * pas * 0.7
            cy = (gy + 0.5) * rang_h + (_hash(n, graine + 1.3) - 0.5) * rang_h * 0.7
            d = np.hypot(I - cx, (J - cy) * 1.15)
            plus_pres = d < d1
            d2 = np.where(plus_pres, d1, np.minimum(d2, d))
            ident = np.where(plus_pres, n, ident)
            dy = np.where(plus_pres, J - cy, dy)
            d1 = np.where(plus_pres, d, d1)
    return d1, d2, ident, dy


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
            k *= 1 + 0.18 * np.exp(-((J / h - 0.22) ** 2) / 0.004)               # bande reflet
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
        # écailles en galets irréguliers (cellules de Voronoï sur une grille décalée) : chaque écaille est bombée,
        # éclairée en haut, cernée d'un sillon fin ; le ventre porte de larges plaques transversales
        d1, d2, ident, dy = _voronoi(I, J, 5.5, seed)
        bombe = np.clip((d2 - d1) / 2.8, 0, 1)
        var = _hash(ident, seed + 3.7) - 0.5
        k *= (0.74 + 0.34 * np.sqrt(bombe)) * (1 + 0.12 * var) * (1 + 0.12 * np.clip(-dy / 2.5, -1, 1)) * (1 + 0.02 * fin)
        k = np.where(d2 - d1 < 0.8, k * 0.8, k)                                    # sillon entre les écailles
        if c2 is not None:
            ventre = np.ones((h, w), bool) if face == "down" else ((J > h * 0.62) if cote else np.zeros((h, w), bool))
            if ventre.any():
                col[ventre] = np.array(c2[:3], float)
                bande = (J % 5)
                kv = LUM[face] * (1 + 0.025 * fin) * np.where(bande == 4, 0.74, np.where(bande == 0, 1.08, 1.0))
                kv *= 0.92 + 0.08 * np.clip(np.minimum(I, w - 1 - I) / 3, 0, 1)
                k = np.where(ventre, kv, k)
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


# ------------------------------------------------------------------ visages et yeux peints en HD
def _ellipse(I, J, cx, cy, rx, ry):
    return ((I - cx) / max(rx, 0.5)) ** 2 + ((J - cy) / max(ry, 0.5)) ** 2


def _trait(reg, masque, pts, couleur, epais=1, k=None):
    """Trait (polyligne) dessiné pixel par pixel ; k : facteur au lieu d'une couleur."""
    H, W = reg.shape[:2]
    for (x0, y0), (x1, y1) in zip(pts[:-1], pts[1:]):
        n = int(max(abs(x1 - x0), abs(y1 - y0)) * 2) + 1
        for t in np.linspace(0, 1, n):
            for e in range(epais):
                xi, yi = int(round(x0 + (x1 - x0) * t)), int(round(y0 + (y1 - y0) * t)) + e
                if 0 <= xi < W and 0 <= yi < H:
                    if k is not None:
                        reg[yi, xi, :3] = np.clip(reg[yi, xi, :3] * k, 0, 255)
                    else:
                        reg[yi, xi, :3] = couleur
                    masque[yi, xi] = True


def _oeil(reg, masque, plat, I, J, ex, ey, lw, lh, iris, sx, regard, peau, lueur=False):
    """Œil vivant : blanc rosé aux coins, iris à liseré sombre et dégradé, pupille, deux reflets, paupières."""
    oe = _ellipse(I, J, ex, ey, lw + 0.45, lh + 0.45) <= 1.0
    coin = np.clip(np.abs(I - ex) / (lw + 0.5), 0, 1)
    blanc = np.array([236, 230, 222.0])[None, None, :] * (1 - 0.1 * coin[..., None]) + np.array([12, -6, -6.0]) * coin[..., None]
    reg[oe, :3] = blanc[oe]
    ix = ex + regard
    ri = max(1.3, lw * 0.62)
    di = _ellipse(I, J, ix, ey, ri, lh + 0.7)
    ir = (di <= 1.0) & oe
    teinte = iris[None, None, :] * (1.25 - 0.55 * np.sqrt(np.clip(di, 0, 1)))[..., None]
    reg[ir, :3] = np.clip(teinte[ir], 0, 255)
    liseré = ir & (di > 0.62)
    reg[liseré, :3] = iris * 0.45
    pupille = ir & (_ellipse(I, J, ix, ey, ri * 0.42, lh * 0.55 + 0.3) <= 1.0)
    reg[pupille, :3] = iris * 0.12 if not lueur else iris * 0.35
    for (dx, dy, v) in ((-0.8, -0.8, 252), (0.9, 0.6, 205)):
        r = ir & (np.abs(I - (ix + dx * sx * 0 + dx)) < 0.5) & (np.abs(J - (ey + dy)) < 0.5)
        reg[r, :3] = v
    if lueur:
        plat[ir, :3] = iris
        plat[ir, 3] = 255
    haut = (_ellipse(I, J, ex, ey - 0.3, lw + 1.0, lh + 1.0) <= 1.0) & ~oe & (J <= ey)
    reg[haut, :3] = peau * 0.38
    bas = (_ellipse(I, J, ex, ey + 0.4, lw + 0.8, lh + 0.9) <= 1.0) & ~oe & (J > ey)
    reg[bas, :3] = np.clip(peau * 0.92 + 10, 0, 255)
    masque |= oe | haut | bas


def visage_hd(arr, X, Y, W, H, peau, yeux=(30, 30, 40), bouche=None, sourcils=None, style=None):
    """Visage peint en HD, avec du caractère : regard (iris coloré, deux reflets, regard de côté), sourcils
    expressifs, bouche (ferme, sourire, rictus, cri, crocs), modelé (front, pommettes, ombre du nez, mâchoire,
    menton) et marques (cicatrice, peinture de guerre, runes, cernes, maquillage, barbe naissante, rides)."""
    st = dict(style or {})
    rng = np.random.default_rng(st.get("graine", 7))
    reg = arr[Y:Y + H, X:X + W]
    J, I = np.mgrid[0:H, 0:W].astype(float)
    peau = np.array(peau[:3], float)
    pale = peau.mean() > 200
    # ---- modelé
    k = np.ones((H, W))
    ey = H * 0.44
    k *= 1 + 0.05 * np.clip(1 - _ellipse(I, J, W / 2, H * 0.2, W * 0.4, H * 0.16), 0, 1)                  # front
    for sx in (-1, 1):
        ex = W / 2 + sx * W * 0.2 - 0.5
        k *= 1 - 0.17 * np.clip(1 - _ellipse(I, J, ex, ey + 0.6, W * 0.15, H * 0.11), 0, 1)               # orbite
        k *= 1 - 0.08 * np.clip(1 - _ellipse(I, J, ex, ey + H * 0.09, W * 0.11, H * 0.04), 0, 1)          # sous l'œil
        k *= 1 + 0.08 * np.clip(1 - _ellipse(I, J, W / 2 + sx * W * 0.27, H * 0.6, W * 0.11, H * 0.06), 0, 1)   # pommette
        k *= 1 - 0.1 * np.clip(1 - _ellipse(I, J, W / 2 + sx * W * 0.42, H * 0.72, W * 0.1, H * 0.2), 0, 1)     # mâchoire
    k *= 1 + 0.06 * np.clip(1 - _ellipse(I, J, W / 2 - 0.5, H * 0.52, W * 0.05, H * 0.1), 0, 1)        # arête du nez
    k *= 1 - 0.22 * np.clip(1 - _ellipse(I, J, W / 2 - 0.5, H * 0.67, W * 0.1, H * 0.035), 0, 1)       # ombre du nez
    k *= 1 - 0.07 * np.clip(1 - _ellipse(I, J, W / 2 - 0.5, H * 0.73, W * 0.03, H * 0.035), 0, 1)      # philtrum
    k *= 1 - 0.1 * np.clip(1 - _ellipse(I, J, W / 2 - 0.5, H * 0.9, W * 0.16, H * 0.05), 0, 1)        # creux du menton
    reg[..., :3] *= k[..., None]
    joues = np.clip(1 - np.minimum(_ellipse(I, J, W * 0.27, H * 0.63, W * 0.1, H * 0.06),
                                   _ellipse(I, J, W * 0.73 - 1, H * 0.63, W * 0.1, H * 0.06)), 0, 1)
    rougeur = 0.05 if pale else 0.1
    reg[..., 0] = np.minimum(255, reg[..., 0] * (1 + rougeur * joues))
    reg[..., 2] = reg[..., 2] * (1 - 0.04 * joues)
    masque = np.zeros((H, W), bool)
    plat = np.zeros((H, W, 4))
    det = set(st.get("details", ()))
    # ---- marques sous les yeux et le reste du visage (peintes avant les yeux)
    if "barbe_naissante" in det:
        zone = (J > H * 0.7) & (rng.random((H, W)) < 0.35) & (np.abs(I - W / 2 + 0.5) < W * 0.42)
        reg[zone, :3] *= 0.8
    if "cernes" in det:
        for sx in (-1, 1):
            c = np.clip(1 - _ellipse(I, J, W / 2 + sx * W * 0.2 - 0.5, ey + H * 0.08, W * 0.1, H * 0.035), 0, 1)
            reg[..., :3] *= (1 - 0.2 * c)[..., None]
            reg[..., 2] = np.minimum(255, reg[..., 2] * (1 + 0.1 * c))
    if "peinture_guerre" in det:
        coul = np.array(st.get("peinture", (150, 20, 20)), float)
        bande = (np.abs(J - (ey + 0.5)) < H * 0.07) & (np.abs(I - W / 2) < W * 0.44)
        reg[bande, :3] = reg[bande, :3] * 0.35 + coul * 0.65
        masque |= bande
    if "griffures" in det:
        for sx in (-1, 1):
            for t in range(3):
                x0 = W / 2 + sx * W * (0.16 + t * 0.06)
                _trait(reg, masque, [(x0, H * 0.55), (x0 - sx * 1, H * 0.66)], np.array(st.get("peinture", (150, 20, 20)), float))
    if "runes" in det:
        lr = np.array(st.get("runes_c", (255, 140, 40)), float)
        avant = masque.copy()
        for sx in (-1, 1):
            cx = W / 2 + sx * W * 0.3
            _trait(reg, masque, [(cx, H * 0.56), (cx + sx * 1.5, H * 0.62), (cx, H * 0.68)], lr)
        _trait(reg, masque, [(W / 2 - 2, H * 0.12), (W / 2 - 0.5, H * 0.2), (W / 2 + 1, H * 0.12)], lr)
        nouveaux = masque & ~avant
        plat[nouveaux, :3] = lr
        plat[nouveaux, 3] = 255
    if "rides" in det:
        for t in range(2):
            _trait(reg, masque, [(W * 0.3, H * (0.18 + t * 0.06)), (W * 0.7, H * (0.18 + t * 0.06))], None, k=0.86)
    if "pustules" in det:
        for _ in range(4):
            px_, py_ = rng.uniform(W * 0.15, W * 0.85), rng.uniform(H * 0.55, H * 0.9)
            b = _ellipse(I, J, px_, py_, 1.2, 1.0) <= 1
            reg[b, :3] = np.array([170, 175, 80.0]) * np.clip(1.15 - 0.3 * _ellipse(I, J, px_ - 0.4, py_ - 0.4, 1.2, 1.0)[b], 0.7, 1.2)[:, None]
            masque |= b
    # ---- yeux
    iris = np.array(st.get("iris", yeux)[:3], float)
    if iris.mean() < 50:
        iris = np.array([88, 62, 40], float)
    lueur = st.get("yeux_lueur", False)
    lw, lh = max(2, round(W * 0.09)), max(1, round(H * 0.05))
    regard = st.get("regard", float(rng.choice((-0.6, 0.0, 0.6))))
    if "maquillage" in det:
        fard = np.array(st.get("fard", (90, 30, 110)), float)
        for sx in (-1, 1):
            ex = W / 2 + sx * W * 0.2 - 0.5
            f = (_ellipse(I, J, ex + sx * 0.8, ey - lh - 1.0, lw + 2.0, lh + 1.2) <= 1.0)
            reg[f, :3] = reg[f, :3] * 0.4 + fard * 0.6
            masque |= f
    for sx in (-1, 1):
        ex = int(round(W / 2 + sx * W * 0.2 - 0.5))
        _oeil(reg, masque, plat, I, J, ex, int(round(ey)), lw, lh, iris, sx, regard, peau, lueur)
    # ---- sourcils
    sour = np.array((sourcils or tuple(peau * 0.42))[:3], float) if not st.get("sourcils_c") else np.array(st["sourcils_c"], float)
    forme = st.get("sourcils", "neutre")
    for sx in (-1, 1):
        ex = W / 2 + sx * W * 0.2 - 0.5
        yb = ey - lh - 2.4
        interieur = ex - sx * (lw + 1.0)
        exterieur = ex + sx * (lw + 1.6)
        dyi, dye, dym = {"neutre": (0.4, 0.4, -0.4), "colere": (1.8, -0.9, 0.3), "severe": (0.9, 0.6, 0.7),
                         "triste": (-1.0, 1.0, -0.2), "arque": (0.6, 0.8, -1.4)}.get(forme, (0.4, 0.4, -0.4))
        pts = [(interieur, yb + dyi), (ex, yb + dym), (exterieur, yb + dye)]
        _trait(reg, masque, pts, sour, epais=2 if forme in ("colere", "severe") else 1)
        _trait(reg, masque, [(interieur, yb + dyi - 1), (ex, yb + dym - 1)], sour * 1.15)
    # ---- bouche
    my = H * 0.79
    bw = W * 0.15
    levre = np.array((bouche or tuple(np.clip(peau * 0.55 + np.array([25, -5, -5]), 0, 255)))[:3], float)
    if st.get("levres"):
        levre = np.array(st["levres"], float)
    type_b = st.get("bouche", "neutre")
    g, d = W / 2 - bw, W / 2 + bw - 1
    if type_b in ("neutre", "ferme", "crocs"):
        coins = 0.0 if type_b == "neutre" else 0.9
        _trait(reg, masque, [(g, my + coins), (g + 2, my), (d - 2, my), (d, my + coins)], levre * 0.8)
        _trait(reg, masque, [(g + 1.5, my + 1), (d - 1.5, my + 1)], np.clip(levre * 1.15 + 15, 0, 255))
        _trait(reg, masque, [(g + 2, my + 2.2), (d - 2, my + 2.2)], None, k=0.85)
        if type_b == "crocs":
            for sx in (-1, 1):
                xx = W / 2 + sx * bw * 0.45
                _trait(reg, masque, [(xx, my + 0.6), (xx, my + 2.4)], np.array([240, 236, 222.0]))
    elif type_b in ("sourire", "rictus"):
        cg = -1.3
        cd = -1.3 if type_b == "sourire" else 0.4
        _trait(reg, masque, [(g, my + cg), (g + 2, my + 0.3), (d - 2, my + 0.3), (d, my + cd)], levre * 0.75)
        _trait(reg, masque, [(g + 2, my + 1.3), (d - 2, my + 1.3)], np.clip(levre * 1.1 + 15, 0, 255))
        _trait(reg, masque, [(g - 1, my + cg - 1.2), (g, my + cg)], None, k=0.86)                      # fossette
        if type_b == "sourire":
            _trait(reg, masque, [(d + 1, my + cd - 1.2), (d, my + cd)], None, k=0.86)
    elif type_b == "cri":
        o = _ellipse(I, J, W / 2 - 0.5, my + 0.6, bw + 0.4, 2.4) <= 1.0
        reg[o, :3] = np.array([60, 14, 14.0])
        dents = o & (J < my - 0.6)
        reg[dents, :3] = np.array([236, 228, 206.0])
        dents2 = o & (J > my + 2.0) & ((I.astype(int) % 2) == 0)
        reg[dents2, :3] = np.array([220, 210, 186.0])
        bord = (_ellipse(I, J, W / 2 - 0.5, my + 0.6, bw + 1.4, 3.3) <= 1.0) & ~o
        reg[bord, :3] = levre * 0.9
        masque |= o | bord
    if "cicatrice" in det:
        sx = 1 if rng.random() < 0.5 else -1
        ex = W / 2 + sx * W * 0.2
        pts = [(ex - sx * 1, ey - H * 0.2), (ex + sx * 0.5, ey), (ex + sx * 2, ey + H * 0.2)]
        _trait(reg, masque, pts, np.clip(peau * 1.12 + np.array([30, 0, 0]), 0, 255))
        _trait(reg, masque, [(x + 1, y) for x, y in pts], None, k=0.75)
    reste = masque & (plat[..., 3] == 0)
    plat[reste] = reg[reste]
    return masque, plat


def visage_simple_hd(arr, X, Y, W, H, peau, yeux=(30, 30, 40), bouche=None, sourcils=None):
    """Visage de la 0.21 (gardé pour la Destruction et la Mort) : visage humain peint en HD sur la peau déjà peinte : orbites, yeux (blanc, iris, pupille, reflet),
    paupières, sourcils, ombre du nez, pommettes, lèvres, menton."""
    reg = arr[Y:Y + H, X:X + W]
    J, I = np.mgrid[0:H, 0:W].astype(float)
    peau = np.array(peau[:3], float)
    k = np.ones((H, W))
    ey = H * 0.44
    for sx in (-1, 1):
        ex = W / 2 + sx * W * 0.2 - 0.5
        k *= 1 - 0.16 * np.clip(1 - _ellipse(I, J, ex, ey + 0.5, W * 0.15, H * 0.11), 0, 1)       # orbite
        k *= 1 + 0.07 * np.clip(1 - _ellipse(I, J, ex, H * 0.62, W * 0.13, H * 0.07), 0, 1)       # pommette
    k *= 1 - 0.2 * np.clip(1 - _ellipse(I, J, W / 2 - 0.5, H * 0.67, W * 0.1, H * 0.035), 0, 1)  # ombre du nez
    k *= 1 - 0.1 * np.clip(1 - _ellipse(I, J, W / 2 - 0.5, H * 0.9, W * 0.18, H * 0.05), 0, 1)   # creux du menton
    reg[..., :3] *= k[..., None]
    rouge = np.clip(1 - np.minimum(_ellipse(I, J, W * 0.27, H * 0.64, W * 0.1, H * 0.06),
                                   _ellipse(I, J, W * 0.73 - 1, H * 0.64, W * 0.1, H * 0.06)), 0, 1)
    reg[..., 0] = np.minimum(255, reg[..., 0] * (1 + 0.08 * rouge))
    masque = np.zeros((H, W), bool)
    plat = np.zeros((H, W, 4))
    iris = np.array(yeux[:3], float)
    if iris.mean() < 50:
        iris = np.array([88, 62, 40], float)          # iris brun plutôt qu'un trou noir
    cil = peau * 0.42
    sour = np.array((sourcils or tuple(peau * 0.45))[:3], float)
    lw, lh = max(2, round(W * 0.085)), max(1, round(H * 0.05))
    for sx in (-1, 1):
        ex = int(round(W / 2 + sx * W * 0.2 - 0.5))
        eyi = int(round(ey))
        oe = _ellipse(I, J, ex, eyi, lw + 0.4, lh + 0.4) <= 1.0
        reg[oe, :3] = np.array([232, 228, 220]) * 0.95
        ir = _ellipse(I, J, ex - sx * 0.3, eyi, max(1.1, lw * 0.55), lh + 0.6) <= 1.0
        ir &= oe
        reg[ir, :3] = iris
        reg[ir & (np.abs(I - (ex - sx * 0.3)) < 0.6) & (np.abs(J - eyi) < 0.6), :3] = iris * 0.25     # pupille
        reflet = (I == ex - sx) & (J == eyi - 1) & ir
        reg[reflet, :3] = 250
        paupiere = (_ellipse(I, J, ex, eyi - 0.4, lw + 0.9, lh + 0.9) <= 1.0) & ~oe & (J <= eyi)
        reg[paupiere, :3] = cil
        # sourcil épais, relevé vers l'extérieur
        for t in np.linspace(-1, 1, 2 * lw + 3):
            xx = ex + t * (lw + 1.2)
            yy = eyi - lh - 2.6 - 0.8 * (t * sx > 0) * abs(t)
            for e in (0, 1):
                xi, yi = int(round(xx)), int(round(yy + e))
                if 0 <= xi < W and 0 <= yi < H:
                    reg[yi, xi, :3] = sour * (1.0 if e == 0 else 0.85)
                    masque[yi, xi] = True
        masque |= oe | paupiere
    # bouche : lèvre supérieure sombre, lèvre inférieure plus claire, ombre dessous
    my = int(round(H * 0.79))
    bw = W * 0.14
    levre = np.array((bouche or tuple(peau * 0.5))[:3], float)
    for i in range(int(W / 2 - bw), int(W / 2 + bw)):
        reg[my, i, :3] = levre
        reg[my + 1, i, :3] = np.clip(peau * 0.85 + np.array([30, 0, 0]), 0, 255)
        if my + 2 < H:
            reg[my + 2, i, :3] *= 0.86
        masque[my:my + 2, i] = True
    plat[masque] = reg[masque]
    return masque, plat


def trogne_hd(arr, X, Y, W, H, c, fond, hauteur, ecart, taille, style=None):
    """Face de bête humanoïde (orcs, démons, hommes-rats, sylvaneth…) : yeux de yeux_hd, plus une bouche
    expressive et des marques selon le style (défenses, crocs, gueule hurlante, bouche creuse, rides de bois)."""
    st = dict(style or {})
    masque, plat = yeux_hd(arr, X, Y, W, H, c, fond, hauteur, ecart, taille)
    reg = arr[Y:Y + H, X:X + W]
    J, I = np.mgrid[0:H, 0:W].astype(float)
    peau = reg[int(H * 0.6), 1, :3].copy()
    b = st.get("bouche")
    my = H * min(0.86, hauteur + 0.42)
    if b == "machoire":        # mâchoire inférieure avancée et crocs vers le haut (orcs, gitz, ogres)
        bw = W * 0.3
        _trait(reg, masque, [(W / 2 - bw, my - 1), (W / 2 - bw + 2, my + 0.6), (W / 2 + bw - 2, my + 0.6), (W / 2 + bw, my - 1)], peau * 0.3, epais=2)
        for sx in (-1, 1):
            xx = W / 2 + sx * bw * 0.6
            _trait(reg, masque, [(xx, my - 2.6), (xx, my)], np.array([236, 228, 200.0]), epais=1)
            _trait(reg, masque, [(xx + sx, my - 1.8), (xx + sx, my)], np.array([210, 200, 170.0]))
        for sx in (-1, 1):
            _trait(reg, masque, [(W / 2 + sx * 1.2 - 0.5, H * (hauteur + 0.22)), (W / 2 + sx * 1.2 - 0.5, H * (hauteur + 0.24))], peau * 0.35)
    elif b == "gueule":        # gueule hurlante pleine de crocs (démons, goules)
        o = _ellipse(I, J, W / 2 - 0.5, my - 0.5, W * 0.26, 2.8) <= 1.0
        reg[o, :3] = np.array([50, 10, 12.0])
        for i in range(int(W / 2 - W * 0.24), int(W / 2 + W * 0.24), 2):
            for (j0, j1) in ((my - 3.2, my - 1.4), (my + 1.8, my + 0.4)):
                _trait(reg, masque, [(i, j0), (i, j1)], np.array([236, 230, 210.0]))
        masque |= o
    elif b == "creuse":        # bouche creuse et nœuds du bois (sylvaneth)
        o = _ellipse(I, J, W / 2 - 0.5, my - 0.5, W * 0.12, 1.8) <= 1.0
        reg[o, :3] = np.array([24, 16, 10.0])
        reg[o & (J < my - 1), :3] = np.array([255, 210, 120.0]) * 0.5
        masque |= o
        for sx in (-1, 1):
            _trait(reg, masque, [(W / 2 + sx * W * 0.32, H * 0.15), (W / 2 + sx * W * 0.36, H * 0.32), (W / 2 + sx * W * 0.3, H * 0.5)], None, k=0.7)
    elif b == "sourire":
        bw = W * 0.24
        _trait(reg, masque, [(W / 2 - bw, my - 1.5), (W / 2 - bw + 2, my + 0.3), (W / 2 + bw - 2, my + 0.3), (W / 2 + bw, my - 1.5)], peau * 0.3)
        _trait(reg, masque, [(W / 2 - bw + 2, my - 0.7), (W / 2 + bw - 2, my - 0.7)], np.array([226, 220, 196.0]))
    if st.get("balafre"):
        pts = [(W * 0.3, H * 0.15), (W * 0.42, H * (hauteur + 0.05)), (W * 0.36, H * 0.75)]
        _trait(reg, masque, pts, np.clip(peau * 1.25 + 20, 0, 255))
        _trait(reg, masque, [(x + 1, y) for x, y in pts], None, k=0.7)
    reste = masque & (plat[..., 3] == 0)
    plat[reste] = reg[reste]
    return masque, plat


def yeux_hd(arr, X, Y, W, H, c, fond=None, hauteur=0.42, ecart=0.22, taille=1):
    """Yeux de bête ou de monstre : orbite creusée, arcade sombre, iris lumineux dégradé, pupille fendue, reflet."""
    reg = arr[Y:Y + H, X:X + W]
    J, I = np.mgrid[0:H, 0:W].astype(float)
    c = np.array(c[:3], float)
    masque = np.zeros((H, W), bool)
    plat = np.zeros((H, W, 4))
    r = 1.6 * taille + 0.6
    ey = H * hauteur
    for sx in (-1, 1):
        ex = W / 2 + sx * W * ecart - 0.5
        orb = np.clip(1 - _ellipse(I, J, ex, ey + 0.3, r * 2.0, r * 1.5), 0, 1)
        reg[..., :3] *= (1 - 0.28 * orb)[..., None]
        arcade = (np.abs(J - (ey - r - 0.8)) < 0.9) & (np.abs(I - ex) < r * 1.7)
        reg[arcade, :3] *= 0.7
        bord = _ellipse(I, J, ex, ey, r + 0.8, r * 0.8 + 0.6) <= 1.0
        if fond is not None:
            reg[bord, :3] = np.array(fond[:3], float)
            masque |= bord
        oeil = _ellipse(I, J, ex, ey, r, r * 0.8) <= 1.0
        dg = np.sqrt(np.clip(_ellipse(I, J, ex, ey, r, r * 0.8), 0, 1))
        teinte = c[None, None, :] * (1.15 - 0.35 * dg[..., None])
        teinte = teinte + (255 - teinte) * np.clip(0.35 - dg, 0, None)[..., None]
        reg[oeil, :3] = np.clip(teinte[oeil], 0, 255)
        plat[oeil, :3] = c
        plat[oeil, 3] = 255
        fente = oeil & (np.abs(I - ex) < 0.5) & (np.abs(J - ey) < r * 0.6)
        reg[fente, :3] = c * 0.15
        reflet = oeil & (np.abs(I - (ex - r * 0.45)) < 0.5) & (np.abs(J - (ey - r * 0.35)) < 0.5)
        reg[reflet, :3] = 255
        masque |= oeil
    reste = masque & (plat[..., 3] == 0)
    plat[reste] = reg[reste]
    return masque, plat
