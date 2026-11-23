# -*- coding: utf-8 -*-
"""v4 : Portails de Royaume façon Nether (aléatoires), tyrolienne Kharadron, foudre et ambiances,
Sigmarite (minerai céleste, raffinage, textures) et pack de ressources."""
import json, os, math
from PIL import Image, ImageDraw
import build as B
from build import w, fn, jtxt, txt, NS, DIM, OUT
import extension as X
import data_v4
from data_monde import BIOMES

EN = B.EN_ROYAUME
RP = "/home/claude/aos/out/RoyaumesMortels_Textures"


# =========================================================================== PRÉPARATION (avant génération)
def preparer():
    X.RES["sigmarite_brute"] = ("Sigmarite Brute", "aqua", "minecraft:raw_iron",
                                "Minerai céleste d'Azyr, encore chargé de foudre.")
    cmd = {"sigmarite": "sigmarite", "sigmarite_brute": "sigmarite_brute"}
    ancien = X.res_spec

    def res_spec(rid, n=1):
        d = ancien(rid, n)
        if rid in cmd:
            d["cmd"] = cmd[rid]
        return d
    X.res_spec = res_spec
    for _, _, _, outs in X.RECETTES:
        for o in outs:
            rm = (o.get("custom_data") or {}).get("rm")
            if rm in cmd:
                o["cmd"] = cmd[rm]
    X.RECETTES.insert(0, ("raffinage", "Raffinage de Sigmarite", [("res:sigmarite_brute", 3), ("minecraft:gold_ingot", 1)],
                          [res_spec("sigmarite", 2)]))
    B.EXTRA_FEATURES["minerai_celeste"] = ({"type": "minecraft:ore", "discard_chance_on_air_exposure": 0.0, "size": 7, "targets": [
        {"state": "minecraft:lapis_ore", "target": {"predicate_type": "minecraft:tag_match", "tag": "minecraft:stone_ore_replaceables"}},
        {"state": "minecraft:deepslate_lapis_ore", "target": {"predicate_type": "minecraft:tag_match", "tag": "minecraft:deepslate_ore_replaceables"}}]},
        12, 40, 220)
    for b in BIOMES:
        if b["id"] == "azyr_cimes":
            b.setdefault("extra", []).append("minerai_celeste")


# =========================================================================== PORTAILS DE ROYAUME (façon Nether)
def gen_failles():
    am = "minecraft:amethyst_block"
    # Test d'un cadre 4×5 (intérieur 2×3) selon l'axe
    for ax in ("x", "z"):
        dx = (1, 0) if ax == "x" else (0, 1)   # direction de largeur
        L = []
        for i in range(2):
            ox, oz = dx[0] * i, dx[1] * i
            L.append(f"execute unless block ~{ox} ~-1 ~{oz} {am} run return 0")
            L.append(f"execute unless block ~{ox} ~3 ~{oz} {am} run return 0")
            for y in range(3):
                L.append(f"execute unless block ~{ox} ~{y} ~{oz} #minecraft:air run return 0")
        for y in range(3):
            L.append(f"execute unless block ~{-dx[0]} ~{y} ~{-dx[1]} {am} run return 0")
            L.append(f"execute unless block ~{2 * dx[0]} ~{y} ~{2 * dx[1]} {am} run return 0")
        L.append("return 1")
        fn(f"faille/test_{ax}", L)
        cx, cz = (1, 0.5) if ax == "x" else (0.5, 1)
        fn(f"faille/allumer_{ax}", [
            f"fill ~ ~ ~ ~{dx[0]} ~2 ~{dx[1]} minecraft:nether_portal[axis={ax}]",
            f'summon minecraft:marker ~{cx} ~1.5 ~{cz} {{Tags:["rm_faille","rm_axe_{ax}"]}}',
            f"particle minecraft:reverse_portal ~{cx} ~1.5 ~{cz} 0.5 1 0.5 0.2 200",
            "playsound minecraft:block.end_portal.spawn block @a[distance=..32] ~ ~ ~ 0.8 1.3",
            f"tellraw @a[distance=..16] {jtxt(txt('✦ Un Portail de Royaume s’ouvre… ', 'light_purple'), txt('Où mènera-t-il ?', 'gray', italic=True))}",
            "scoreboard players set #gain rm_tmp 20", f"execute as @p[distance=..8] run function {NS}:rpg/ajouter",
            "kill @s"])
    fn("faille/activer", [
        f"execute if function {NS}:faille/test_x run return run function {NS}:faille/allumer_x",
        f"execute positioned ~-1 ~ ~ if function {NS}:faille/test_x run return run function {NS}:faille/allumer_x",
        f"execute if function {NS}:faille/test_z run return run function {NS}:faille/allumer_z",
        f"execute positioned ~ ~ ~-1 if function {NS}:faille/test_z run return run function {NS}:faille/allumer_z",
        "return 0"])
    fn("faille/tick", [
        "execute unless block ~ ~ ~ minecraft:nether_portal run return run kill @s",
        f"execute if entity @s[tag=rm_axe_x] positioned ~-1 ~-1.5 ~-0.5 as @a[dx=1,dy=2,dz=0] at @s run function {NS}:faille/voyager",
        f"execute if entity @s[tag=rm_axe_z] positioned ~-0.5 ~-1.5 ~-1 as @a[dx=0,dy=2,dz=1] at @s run function {NS}:faille/voyager"])
    fn("faille/voyager", [
        f"execute if score @s rm_cd matches 1.. run return run function {NS}:faille/repousser",
        "scoreboard players set @s rm_cd 4",
        "particle minecraft:reverse_portal ~ ~1 ~ 0.5 1 0.5 0.2 120",
        "playsound minecraft:block.portal.travel player @s ~ ~ ~ 0.4 1.3",
        f"execute {EN} run return run function {NS}:pierre/vers_monde",
        f"function {NS}:faille/aleatoire"])
    fn("faille/repousser", [
        "execute at @e[type=minecraft:marker,tag=rm_faille,sort=nearest,limit=1] facing entity @s feet run tp @s ^ ^ ^2.5"])
    # Destinations aléatoires
    dests = [(f"{NS}:royaumes_mortels", "Les Royaumes Mortels", "gold", 4)]
    for did, dd in data_v4.DIMENSIONS.items():
        dests.append((f"{NS}:{did}", dd["nom"], dd["c"], 1 if did != "hysh" else 2))
    total = sum(p for *_, p in dests)
    L = [f"execute store result score #d rm_tmp run random value 1..{total}"]
    k = 1
    for dim, nom, c, p in dests:
        L.append(f'execute if score #d rm_tmp matches {k}..{k + p - 1} run return run function {NS}:faille/vers '
                 f'{{dim:"{dim}",nom:"{nom}",c:"{c}"}}')
        k += p
    fn("faille/aleatoire", L)
    fn("faille/vers", [
        "$execute in $(dim) run spreadplayers ~ ~ 0 64 false @s",
        "$execute at @s unless dimension $(dim) in $(dim) run spreadplayers ~ ~ 0 800 false @s",
        '$title @s title {"text":"$(nom)","color":"$(c)","bold":true}',
        "title @s subtitle " + jtxt(txt("Le portail vous a mené en terre inconnue…", "gray", italic=True)),
        "effect give @s minecraft:resistance 6 4 true", "effect give @s minecraft:slow_falling 6 0 true",
        f"$execute at @s if dimension $(dim) run function {NS}:faille/retour"])
    fn("faille/retour", [
        "execute align xyz run fill ~-1 ~-1 ~3 ~2 ~3 ~3 minecraft:amethyst_block",
        "execute align xyz run fill ~ ~ ~3 ~1 ~2 ~3 minecraft:air",
        "execute align xyz run fill ~-1 ~ ~1 ~2 ~2 ~2 minecraft:air",
        "execute align xyz run fill ~ ~ ~3 ~1 ~2 ~3 minecraft:nether_portal[axis=x]",
        'execute align xyz run summon minecraft:marker ~1 ~1.5 ~3.5 {Tags:["rm_faille","rm_axe_x"]}',
        "tellraw @s " + jtxt(txt("Un portail de retour s’est formé devant vous.", "light_purple"))])


# =========================================================================== TYROLIENNE KHARADRON
def gen_tyrolienne():
    fn("tyrolienne/depart", ["tag @s add rm_tyro", "scoreboard players set @s rm_tyt 0",
                             "playsound minecraft:block.chain.place player @s ~ ~ ~ 1 0.6",
                             "title @s actionbar " + jtxt(txt("Tyrolienne d'aether ! Accrochez-vous…", "yellow"))])
    fn("tyrolienne/glisser", [
        "scoreboard players add @s rm_tyt 1",
        f"execute if score @s rm_tyt matches 240.. run return run function {NS}:tyrolienne/fin",
        f"execute if entity @e[type=minecraft:marker,tag=rm_tyro_fin,distance=..1.6] run return run function {NS}:tyrolienne/fin",
        f"execute unless entity @e[type=minecraft:marker,tag=rm_tyro_fin,distance=..160] run return run function {NS}:tyrolienne/fin",
        "execute facing entity @e[type=minecraft:marker,tag=rm_tyro_fin,sort=nearest,limit=1] feet run tp @s ^ ^ ^0.6",
        "particle minecraft:electric_spark ~ ~2.2 ~ 0.1 0.1 0.1 0 2"])
    fn("tyrolienne/fin", ["tag @s remove rm_tyro", "effect give @s minecraft:slow_falling 3 0 true",
                          "playsound minecraft:block.chain.break player @s ~ ~ ~ 1 0.8"])


# =========================================================================== FOUDRE ET AMBIANCES
AMB = {
    "rm_amb_ames": ["particle minecraft:soul ~ ~1 ~ 5 2 5 0.02 14", "particle minecraft:sculk_soul ~ ~2 ~ 3 3 3 0.02 6"],
    "rm_amb_peste": ["particle minecraft:item_slime ~ ~ ~ 4 1 4 0 18", "particle minecraft:mycelium ~ ~1 ~ 8 2 8 0 50",
                     "particle minecraft:white_ash ~ ~2 ~ 6 2 6 0 30"],
    "rm_amb_lueur": ["particle minecraft:glow ~ ~2 ~ 0.4 3 0.4 0 10",
                     "particle minecraft:dust{color:[0.3,1.0,0.3],scale:2.0} ~ ~3 ~ 0.6 3 0.6 0 18"],
    "rm_amb_braise": ["particle minecraft:lava ~ ~ ~ 5 2 5 0 6", "particle minecraft:large_smoke ~ ~4 ~ 4 2 4 0.02 10"],
    "rm_amb_aether": ["particle minecraft:wax_on ~ ~ ~ 5 3 5 0 12", "particle minecraft:end_rod ~ ~ ~ 4 3 4 0.01 4"],
    "rm_amb_lumiere": ["particle minecraft:end_rod ~ ~ ~ 6 6 6 0.01 20"],
    "rm_amb_sang": ["particle minecraft:dust{color:[0.6,0.0,0.0],scale:1.6} ~ ~1 ~ 2 1 2 0 25",
                    "particle minecraft:falling_lava ~ ~4 ~ 2 1 2 0 4"],
    "rm_amb_celeste": ["particle minecraft:electric_spark ~ ~ ~ 3 3 0.3 0.3 40", "particle minecraft:end_rod ~ ~ ~ 2 2 0.2 0.02 10",
                       "particle minecraft:glow ~ ~ ~ 1 1 0.2 0 8"],
    "rm_amb_vie": ["particle minecraft:spore_blossom_air ~ ~ ~ 10 6 10 0 30", "particle minecraft:happy_villager ~ ~ ~ 4 3 4 0 6"],
    "rm_amb_malepierre": ["particle minecraft:dust{color:[0.4,1.0,0.2],scale:1.4} ~ ~1 ~ 6 3 6 0 30"],
}


def gen_ambiances():
    L = []
    for tag, cmds in AMB.items():
        fn(f"ambiance/{tag[7:]}", cmds)
        L.append(f"execute as @e[type=minecraft:marker,tag={tag}] at @s if entity @a[distance=..48] run function {NS}:ambiance/{tag[7:]}")
    L.append(f"execute as @e[type=minecraft:marker,tag=rm_foudre] at @s if entity @a[distance=..96] run function {NS}:ambiance/foudre")
    fn("ambiance/boucle", L)
    fn("ambiance/foudre", ["execute store result score #f rm_tmp run random value 1..8",
                           "execute if score #f rm_tmp matches 1 run summon minecraft:lightning_bolt ~ ~ ~",
                           "execute if score #f rm_tmp matches 1 if entity @s[tag=rm_malefoudre] run particle "
                           "minecraft:dust{color:[0.4,1.0,0.2],scale:3.0} ~ ~-4 ~ 1 5 1 0 120",
                           "execute if score #f rm_tmp matches 2 run particle minecraft:electric_spark ~ ~ ~ 1 1 1 0.3 30"])


# =========================================================================== SIGMARITE : butin du minerai céleste
def gen_sigmarite_loot():
    for bloc in ("lapis_ore", "deepslate_lapis_ore"):
        v = json.load(open(f"{B.VANILLA}/loot_table/blocks/{bloc}.json"))
        v.pop("random_sequence", None)
        v["pools"].append({"rolls": 1, "condition": {"type": "minecraft:all_of", "terms": [
            {"type": "minecraft:location_check", "predicate": {"biomes": f"{NS}:azyr_cimes"}},
            {"type": "minecraft:survives_explosion"}, {"type": "minecraft:random_chance", "chance": 0.6}]},
            "entries": [B.entry(X.res_spec("sigmarite_brute"), n=(1, 2))]})
        w(f"data/minecraft/loot_table/blocks/{bloc}.json", v)


# =========================================================================== TEXTURES (pack de ressources)
PAL = {
    ".": (0, 0, 0, 0), "o": (46, 30, 10, 255), "d": (128, 92, 24, 255), "g": (212, 168, 52, 255), "l": (246, 214, 110, 255),
    "w": (255, 247, 214, 255), "b": (40, 96, 200, 255), "c": (120, 184, 255, 255), "n": (22, 46, 110, 255),
    "s": (88, 96, 120, 255), "t": (128, 138, 160, 255), "u": (168, 178, 196, 255), "k": (52, 56, 72, 255),
}


def dessiner(grille):
    img = Image.new("RGBA", (16, 16))
    for y, ligne in enumerate(grille):
        for x, ch in enumerate(ligne):
            img.putpixel((x, y), PAL[ch])
    return img


# Lingot de Sigmarite : or divin, liseré azur et comète à deux queues gravée
LINGOT = [
    "................",
    "................",
    "................",
    "......oooooooo..",
    ".....owwllllllo.",
    "....owlllllllcbo",
    "...owllllllllcbo",
    "..ooooooooooocbo",
    "..olggggggggdcbo",
    "..oggcggggcbdbno",
    "..oggbccgcbgdbno",
    "..oggggbbbggdno.",
    "..odddddddddno..",
    "..oooooooooooo..",
    "................",
    "................",
]
# Sigmarite brute : roche céleste gris-bleu veinée d'or et de cristaux azur
BRUTE = [
    "................",
    "................",
    "......kkkk......",
    "....kkuttskk....",
    "...ktuutlcsk....",
    "..ktutgltcbsk...",
    "..kttgltsbcsk...",
    ".kstltttscbtsk..",
    ".ksttsgltsttsk..",
    ".kssttglgtcbsk..",
    "..kssttgtcbcsk..",
    "..kksssttbbsk...",
    "...kksssssskk...",
    ".....kkkkkk.....",
    "................",
    "................",
]


def lingot():
    """Lingot trapézoïdal d'or divin, extrémités émaillées d'azur et comète à deux queues de Sigmar."""
    g = [["." for _ in range(16)] for _ in range(16)]
    for r in range(3, 7):                       # face supérieure (trapèze)
        a, b = 5 - (r - 3), 10 + (r - 3)
        for x in range(a, b + 1):
            g[r][x] = "l"
        g[r][a] = "w"; g[r][b] = "g"
    for x in range(5, 9):
        g[3][x] = "w"
    g[4][5] = g[4][6] = "w"
    for x in range(2, 14):                      # arête
        g[7][x] = "g"
    for r in range(8, 12):                      # face avant
        for x in range(2, 14):
            g[r][x] = "g"
    for r in range(7, 12):                      # extrémités émaillées
        g[r][2] = "c"; g[r][3] = "b"; g[r][13] = "n"; g[r][12] = "b"
    for x in range(2, 14):
        g[12][x] = "d"
    # comète : tête à droite, une queue vers le haut-gauche, une vers le bas-gauche
    for (x, y, ch) in ((10, 9, "w"), (11, 9, "c"), (10, 10, "c"), (11, 10, "c"),
                       (9, 9, "c"), (8, 9, "b"), (7, 8, "b"), (6, 8, "b"), (5, 8, "b"),
                       (9, 10, "c"), (8, 10, "b"), (7, 11, "b"), (6, 11, "b"), (5, 11, "b")):
        g[y][x] = ch
    forme = {(x, y) for y in range(16) for x in range(16) if g[y][x] != "."}
    for (x, y) in list(forme):
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nx, ny = x + dx, y + dy
            if 0 <= nx < 16 and 0 <= ny < 16 and (nx, ny) not in forme:
                g[ny][nx] = "o"
    return ["".join(r) for r in g]


def gen_pack_ressources():
    os.makedirs(RP, exist_ok=True)

    def wr(p, d):
        full = os.path.join(RP, p)
        os.makedirs(os.path.dirname(full), exist_ok=True)
        json.dump(d, open(full, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    wr("pack.mcmeta", {"pack": {"description": [{"text": "Royaumes Mortels — Textures", "color": "gold"},
                                                {"text": "\nSigmarite et objets des Royaumes", "color": "gray"}],
                                "min_format": 97, "max_format": 99}})
    textures = {"sigmarite": dessiner(lingot()), "sigmarite_brute": dessiner(BRUTE)}
    for nom, img in textures.items():
        p = os.path.join(RP, f"assets/royaumes/textures/item/{nom}.png")
        os.makedirs(os.path.dirname(p), exist_ok=True)
        img.save(p)
        wr(f"assets/royaumes/models/item/{nom}.json", {"parent": "minecraft:item/generated",
                                                       "textures": {"layer0": f"royaumes:item/{nom}"}})
    # Sélection par custom_model_data sur les modèles vanilla (repli vanilla si le pack est absent)
    for vanilla, nom in (("gold_ingot", "sigmarite"), ("raw_iron", "sigmarite_brute")):
        wr(f"assets/minecraft/items/{vanilla}.json", {"model": {
            "type": "minecraft:select", "property": "minecraft:custom_model_data", "index": 0,
            "cases": [{"when": nom, "model": {"type": "minecraft:model", "model": f"royaumes:item/{nom}"}}],
            "fallback": {"type": "minecraft:model", "model": f"minecraft:item/{vanilla}"}}})
    # Icône du pack (comète de Sigmar)
    ic = Image.new("RGBA", (64, 64), (20, 30, 60, 255))
    d = ImageDraw.Draw(ic)
    d.ellipse((34, 6, 52, 24), fill=(246, 214, 110, 255))
    d.line((38, 22, 8, 56), fill=(212, 168, 52, 255), width=5)
    d.line((48, 24, 30, 60), fill=(120, 184, 255, 255), width=5)
    ic.save(os.path.join(RP, "pack.png"))
    # Aperçu agrandi pour l'utilisateur
    prev = Image.new("RGBA", (760, 400), (24, 26, 32, 255))
    d = ImageDraw.Draw(prev)
    for i, (nom, img) in enumerate(textures.items()):
        big = img.resize((320, 320), Image.NEAREST)
        x0 = 40 + i * 360
        prev.alpha_composite(big, (x0, 40))
        d.text((x0, 368), {"sigmarite": "Lingot de Sigmarite", "sigmarite_brute": "Sigmarite Brute"}[nom], fill=(240, 220, 150, 255))
    prev.save("/home/claude/aos/out/apercu_sigmarite.png")


# =========================================================================== CODEX
def maj_codex():
    p = f"{OUT}/data/{NS}/dialog/codex.json"
    d = json.load(open(p, encoding="utf-8"))
    cont = d["body"][0]["contents"]
    ajout = [{"text": "Portails de Royaume (comme le Nether)\n", "color": "light_purple", "bold": True},
             {"text": "Construisez un cadre de Blocs d'améthyste de 4×5 (intérieur 2×3), puis lâchez un Éclat de Royaume "
                      "au fond du cadre. Le portail s'ouvre et mène vers un Royaume au hasard : les Royaumes Mortels, Aqshy, "
                      "Shyish, Ghur, les Huit-Points ou les îles célestes de Hysh. Un portail de retour se forme à l'arrivée.\n\n",
              "color": "white"},
             {"text": "Sigmarite\n", "color": "aqua", "bold": True},
             {"text": "Le minerai de lapis des Cimes d'Azyr donne de la Sigmarite Brute. 3 Sigmarite Brute + 1 lingot d'or "
                      "à la Forge = 2 Lingots de Sigmarite.\n\n", "color": "white"}]
    d["body"][0]["contents"] = cont[:2] + ajout + cont[2:]
    json.dump(d, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=2)


def brancher():
    base = f"{OUT}/data/{NS}/function"

    def ajouter(f, lignes):
        p = f"{base}/{f}.mcfunction"
        t = open(p, encoding="utf-8").read()
        open(p, "w", encoding="utf-8").write(t + "\n".join(lignes) + "\n")
    ajouter("tick", [
        f"execute as @e[type=minecraft:marker,tag=rm_faille] at @s run function {NS}:faille/tick",
        f"execute as @e[type=minecraft:marker,tag=rm_tyro_debut] at @s as @a[distance=..1.5,tag=!rm_tyro] run function {NS}:tyrolienne/depart",
        f"execute as @a[tag=rm_tyro] at @s run function {NS}:tyrolienne/glisser"])
    ajouter("boucle_seconde", [f"function {NS}:ambiance/boucle"])
    ajouter("forge/boucle", [
        'execute as @e[type=minecraft:item,nbt={Item:{id:"minecraft:armadillo_scute",components:{"minecraft:custom_data":{rm:"eclat"}}}}] '
        f"at @s if block ~ ~-0.3 ~ minecraft:amethyst_block align xyz run function {NS}:faille/activer"])
    ajouter("rpg/load", ["scoreboard objectives add rm_tyt dummy"])


def generer():
    gen_failles(); gen_tyrolienne(); gen_ambiances(); gen_sigmarite_loot(); gen_pack_ressources(); maj_codex(); brancher()
