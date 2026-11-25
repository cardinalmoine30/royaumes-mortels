package fr.royaumes.client;

import fr.royaumes.ArsenalGenere;
import fr.royaumes.ArtisanatGenere;
import fr.royaumes.FactionsGenerees;
import java.util.ArrayList;
import java.util.LinkedHashSet;
import java.util.List;
import net.minecraft.client.Minecraft;
import net.minecraft.client.gui.GuiGraphicsExtractor;
import net.minecraft.client.gui.screens.Screen;
import net.minecraft.client.renderer.RenderPipelines;
import net.minecraft.core.component.DataComponents;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.network.chat.Component;
import net.minecraft.resources.Identifier;
import net.minecraft.world.entity.player.Inventory;
import net.minecraft.world.item.ItemStack;

/**
 * Hub d'artisanat (onglet Forge de l'inventaire) : toutes les recettes du mod en images.
 * Trois postes (Table de forgeron, Établi, Forge de guerre), des catégories, et pour chaque recette l'objet obtenu,
 * ses ingrédients avec ce que tu as déjà (vert) ou ce qu'il te manque (rouge). Survoler une recette l'explique en bas.
 */
public class EcranArtisanat extends Screen {
    private static final int PW = 440;
    private static final int PH = 240;
    private static final int CW = 150;
    private static final int CH = 34;
    private static final int PAR_PAGE = 10;
    private static final String[] POSTES = {"forgeron", "etabli", "arsenal"};
    private static final String[] NOMS_POSTES = {"Table de forgeron", "Établi", "Forge de guerre"};
    private static final String[] PALIERS = {"Soldat", "Élite", "Légende", "Mythique", "Divin"};
    private static final int[] COULEURS_PALIERS = {0xFFC8CAD2, 0xFF96D7E6, 0xFFF5CD50, 0xFF5AE6FF, 0xFFFFF5DC};
    private static int poste = 0;
    private static String categorie = "";
    private static int page = 0;
    private int px;
    private int py;
    private int survol = -1;
    private final List<EcranCamp.BoutonAoS> boutons = new ArrayList<>();

    public EcranArtisanat() {
        super(Component.literal("Hub d'artisanat"));
    }

    // ------------------------------------------------------------------ données
    static ItemStack pile(String code) {
        String[] a = code.split("@");
        var it = BuiltInRegistries.ITEM.getValue(Identifier.parse(a[0]));
        ItemStack s = new ItemStack(it);
        if (a.length > 1) {
            s.set(DataComponents.ITEM_MODEL, Identifier.parse(a[1]));
        }
        return s;
    }

    static String nom(String code) {
        String[] a = code.split("@");
        return a.length > 2 ? a[2] : pile(code).getHoverName().getString();
    }

    /** Combien le joueur en porte (objets du datapack reconnus à leur modèle). */
    private static final java.util.Map<String, Integer> CACHE = new java.util.HashMap<>();
    private static long cacheTick = -1;

    /** Compte mis en cache pour l'image en cours (le hub interroge plusieurs fois les mêmes ingrédients). */
    static int compte(String code) {
        var mc = Minecraft.getInstance();
        long t = mc.level == null ? 0 : mc.level.getGameTime();
        if (t != cacheTick) {
            CACHE.clear();
            cacheTick = t;
        }
        return CACHE.computeIfAbsent(code, EcranArtisanat::compter);
    }

    private static int compter(String code) {
        var p = Minecraft.getInstance().player;
        if (p == null) {
            return 0;
        }
        String[] a = code.split("@");
        var it = BuiltInRegistries.ITEM.getValue(Identifier.parse(a[0]));
        Inventory inv = p.getInventory();
        int n = 0;
        for (int i = 0; i < inv.getContainerSize(); i++) {
            ItemStack s = inv.getItem(i);
            if (!s.is(it)) {
                continue;
            }
            if (a.length > 1) {
                Identifier m = s.get(DataComponents.ITEM_MODEL);
                if (m == null || !m.toString().equals(a[1])) {
                    continue;
                }
            }
            n += s.getCount();
        }
        return n;
    }

    private static final java.util.Map<String, List<String>> CATEGORIES = new java.util.HashMap<>();

    static List<String> categories(String p) {
        return CATEGORIES.computeIfAbsent(p, EcranArtisanat::lister);
    }

    private static List<String> lister(String p) {
        LinkedHashSet<String> c = new LinkedHashSet<>();
        for (int i = 0; i < ArtisanatGenere.NOMS.length; i++) {
            if (ArtisanatGenere.POSTES[i].equals(p)) {
                c.add(ArtisanatGenere.CATEGORIES[i]);
            }
        }
        return new ArrayList<>(c);
    }

    static List<Integer> recettes() {
        List<Integer> l = new ArrayList<>();
        for (int i = 0; i < ArtisanatGenere.NOMS.length; i++) {
            if (ArtisanatGenere.POSTES[i].equals(POSTES[poste]) && (categorie.isEmpty() || ArtisanatGenere.CATEGORIES[i].equals(categorie))) {
                l.add(i);
            }
        }
        return l;
    }

    static boolean faisable(int r) {
        for (int k = 0; k < ArtisanatGenere.INGREDIENTS[r].length; k++) {
            if (compte(ArtisanatGenere.INGREDIENTS[r][k]) < ArtisanatGenere.NOMBRES[r][k]) {
                return false;
            }
        }
        return true;
    }

    // ------------------------------------------------------------------ boutons
    @Override
    protected void init() {
        px = (this.width - PW) / 2;
        py = Texte.haut(this.height, PH);
        for (int i = 0; i < POSTES.length; i++) {
            final int ii = i;
            boutons.add(addRenderableWidget(new EcranCamp.BoutonAoS(-1, px + 8, py + 24 + i * 20, 112, 17, () -> Component.literal(NOMS_POSTES[ii]),
                    () -> {
                        poste = ii;
                        categorie = "";
                        page = 0;
                    }, () -> true, () -> poste == ii, () -> true)));
        }
        for (int c = 0; c < 10; c++) {
            final int cc = c;
            boutons.add(addRenderableWidget(new EcranCamp.BoutonAoS(-1, px + 14, py + 92 + c * 14, 104, 12,
                    () -> Component.literal(cc == 0 ? "Tout" : categorieNo(cc - 1)),
                    () -> {
                        categorie = cc == 0 ? "" : categorieNo(cc - 1);
                        page = 0;
                    }, () -> true, () -> cc == 0 ? categorie.isEmpty() : categorie.equals(categorieNo(cc - 1)),
                    () -> poste < 2 && (cc == 0 || cc - 1 < categories(POSTES[poste]).size()))));
        }
        boutons.add(addRenderableWidget(new EcranCamp.BoutonAoS(-1, px + 130, py + PH - 46, 40, 14, () -> Component.literal("◀"),
                () -> page = Math.max(0, page - 1), () -> page > 0, () -> false, () -> poste < 2)));
        boutons.add(addRenderableWidget(new EcranCamp.BoutonAoS(-1, px + PW - 50, py + PH - 46, 40, 14, () -> Component.literal("▶"),
                () -> page++, () -> (page + 1) * PAR_PAGE < recettes().size(), () -> false, () -> poste < 2)));
    }

    private static String categorieNo(int k) {
        List<String> c = categories(POSTES[poste]);
        return k < c.size() ? c.get(k) : "";
    }

    @Override
    public void extractRenderState(GuiGraphicsExtractor g, int sx, int sy, float partiel) {
        boutons.forEach(b -> b.visible = b.visibleSi.getAsBoolean());
        super.extractRenderState(g, sx, sy, partiel);
    }

    @Override
    public boolean isPauseScreen() {
        return false;
    }

    // ------------------------------------------------------------------ dessin
    @Override
    public void extractBackground(GuiGraphicsExtractor g, int sx, int sy, float partiel) {
        g.fillGradient(0, 0, this.width, this.height, 0xE0281408, 0xF00A0604);
        EcranSerment.cadre(g, px, py, PW, PH, 0xEB1A0F0A);
        EcranSerment.coins(g, px, py, PW, PH);
        g.blit(RenderPipelines.GUI_TEXTURED, EcranSerment.ORNEMENTS, px + PW / 2 - 80, py - 12, 0, 24, 160, 24, 256, 64);
        g.centeredText(this.font, "HUB D'ARTISANAT", px + PW / 2, py - 4, EcranSerment.OR_CLAIR);
        Texte.ligne(g, this.font, "Postes", px + 10, py + 12, 100, EcranSerment.OR, true);
        if (poste < 2) {
            Texte.ligne(g, this.font, "Catégories", px + 10, py + 82, 100, EcranSerment.OR, true);
        }
        g.fill(px + 124, py + 10, px + 125, py + PH - 10, 0x66D4A63A);
        if (poste == 2) {
            arsenal(g);
            return;
        }
        List<Integer> l = recettes();
        int pages = Math.max(1, (l.size() + PAR_PAGE - 1) / PAR_PAGE);
        page = Math.min(page, pages - 1);
        survol = -1;
        for (int k = 0; k < PAR_PAGE; k++) {
            int idx = page * PAR_PAGE + k;
            if (idx >= l.size()) {
                break;
            }
            int r = l.get(idx);
            int x = px + 130 + (k % 2) * (CW + 4);
            int y = py + 12 + (k / 2) * (CH + 2);
            boolean dessus = sx >= x && sx < x + CW && sy >= y && sy < y + CH;
            if (dessus) {
                survol = r;
            }
            boolean ok = faisable(r);
            g.fill(x, y, x + CW, y + CH, dessus ? 0x8A5A3A18 : 0x5A3A2410);
            g.fill(x, y, x + 2, y + CH, ok ? 0xFF5ADC6E : 0xFF8C6A3A);
            g.item(pile(ArtisanatGenere.RESULTATS[r]), x + 5, y + 3);
            if (ArtisanatGenere.QUANTITES[r] > 1) {
                g.text(this.font, "×" + ArtisanatGenere.QUANTITES[r], x + 6, y + 20, 0xFFF2D27A, true);
            }
            Texte.ligne(g, this.font, ArtisanatGenere.NOMS[r], x + 24, y + 3, CW - 28,
                    ArtisanatGenere.RESERVES[r].isEmpty() ? 0xFFF2E6C8 : 0xFFFFB46E, true);
            int ix = x + 24;
            for (int i = 0; i < ArtisanatGenere.INGREDIENTS[r].length && i < 5; i++) {
                String ing = ArtisanatGenere.INGREDIENTS[r][i];
                int n = ArtisanatGenere.NOMBRES[r][i];
                g.item(pile(ing), ix, y + 15);
                String t = "" + n;
                g.text(this.font, t, ix + 17 - this.font.width(t), y + 24, compte(ing) >= n ? 0xFF9EE69A : 0xFFFF6B6B, true);
                ix += 24;
            }
        }
        Texte.centre(g, this.font, "Page " + (page + 1) + " / " + pages + "  ·  " + l.size() + " recettes", px + 130 + (PW - 140) / 2,
                py + PH - 43, 200, 0xFFB4AA96);
        // explication en bas : la recette survolée, sinon le mod'emploi du poste
        String bas;
        if (survol >= 0) {
            StringBuilder b = new StringBuilder(ArtisanatGenere.NOMS[survol] + " : ");
            for (int i = 0; i < ArtisanatGenere.INGREDIENTS[survol].length; i++) {
                String ing = ArtisanatGenere.INGREDIENTS[survol][i];
                int a = compte(ing);
                int n = ArtisanatGenere.NOMBRES[survol][i];
                b.append(i > 0 ? ", " : "").append(n).append(" ").append(nom(ing)).append(a >= n ? "" : " (il en manque " + (n - a) + ")");
            }
            if (!ArtisanatGenere.RESERVES[survol].isEmpty()) {
                b.append(". Réservé : ").append(ArtisanatGenere.RESERVES[survol]);
            }
            bas = b.toString();
        } else if (poste == 0) {
            bas = "Table de forgeron : pose-la, puis lâche les ingrédients dessus (touche "
                    + Minecraft.getInstance().options.keyDrop.getTranslatedKeyMessage().getString() + ") ; ils fusionnent seuls. Barre verte : tu as tout.";
        } else {
            bas = "Établi : recettes 3 × 3 classiques, aussi dans le livre de recettes. Barre verte : tu as tout. Survole une recette pour le détail.";
        }
        Texte.bloc(g, this.font, bas, px + 130, py + PH - 28, PW - 140, 22, 0xFFE6D3A8, false);
    }

    /** Forge de guerre : la progression de l'arsenal de la faction, palier par palier, en images. */
    private void arsenal(GuiGraphicsExtractor g) {
        int fa = EcranForge.faction();
        int x0 = px + 132;
        if (fa <= 0 || fa >= ArsenalGenere.IDS.length) {
            Texte.bloc(g, this.font, "Prête serment à une faction pour voir son arsenal : 5 paliers d'armure (Soldat, Élite, Légende, Mythique, Divin), "
                    + "des outils et l'arme de lignée.", x0, py + 20, PW - 142, 60, 0xFFE6D3A8, false);
            return;
        }
        Texte.ligne(g, this.font, "Arsenal : " + FactionsGenerees.NOMS[fa], x0, py + 12, PW - 142, 0xFF000000 | FactionsGenerees.COULEURS[fa], true);
        for (int t = 0; t < PALIERS.length; t++) {
            int ligne = t * 9 + 1;                       // le plastron de chaque palier
            if (ligne >= ArsenalGenere.IDS[fa].length) {
                break;
            }
            int y = py + 26 + t * 30;
            int req = EcranForge.requis(ligne);
            boolean ok = EcranForge.niveau() >= req;
            g.fill(x0, y, px + PW - 10, y + 27, 0x5A3A2410);
            g.fill(x0, y, x0 + 2, y + 27, COULEURS_PALIERS[t]);
            g.item(new ItemStack(EcranForge.item("royaumes:" + ArsenalGenere.IDS[fa][ligne])), x0 + 5, y + 5);
            Texte.ligne(g, this.font, PALIERS[t] + "  ·  niv. " + req, x0 + 24, y + 3, 110, ok ? COULEURS_PALIERS[t] : 0xFF8C8C8C, true);
            Texte.ligne(g, this.font, ArsenalGenere.NOMS[fa][ligne], x0 + 24, y + 15, 110, 0xFFB4AA96, false);
            int x = x0 + 140;
            for (String ing : ArsenalGenere.RECETTES[fa][ligne].split(",")) {
                String[] a = ing.split("\\*");
                var it = EcranForge.item(a[0]);
                int n = Integer.parseInt(a[1]);
                g.item(new ItemStack(it), x, y + 5);
                g.text(this.font, "" + n, x + 17 - this.font.width("" + n), y + 14, EcranForge.compte(it) >= n ? 0xFF9EE69A : 0xFFFF6B6B, true);
                x += 22;
                if (x > px + PW - 30) {
                    break;
                }
            }
        }
        Texte.bloc(g, this.font, "Chaque palier se forge à partir de la pièce du palier précédent, à la Forge de guerre (onglet Établi : "
                + "3 lingots d'or, une enclume, 2 obsidiennes, pierre des Royaumes). Clic droit dessus : armure, outils et armes de ta faction.",
                x0, py + PH - 40, PW - 142, 34, 0xFFE6D3A8, false);
    }
}
