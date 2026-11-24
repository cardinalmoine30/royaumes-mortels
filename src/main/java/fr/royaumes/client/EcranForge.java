package fr.royaumes.client;

import fr.royaumes.ArsenalGenere;
import fr.royaumes.FactionsGenerees;
import fr.royaumes.reseau.DonneesHeros;
import fr.royaumes.reseau.FicheHeros;
import net.minecraft.client.Minecraft;
import net.minecraft.client.gui.GuiGraphicsExtractor;
import net.minecraft.client.gui.screens.Screen;
import net.minecraft.client.renderer.RenderPipelines;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.network.chat.Component;
import net.minecraft.resources.Identifier;
import net.minecraft.world.entity.player.Inventory;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.ItemStack;

/** Forge de guerre : seules les 6 pièces de l'arsenal de TA faction, avec leurs matériaux (éclats de Royaumes étrangers). */
public class EcranForge extends Screen {
    private static final int PW = 460;
    private static final int PH = 262;
    private static final String[] ONGLETS = {"Soldat", "Élite", "Légende", "Mythique", "Divin", "Armes"};
    private static final int ARMES = ArsenalGenere.PALIERS.length * 9;
    private static final int[] COULEURS_PALIERS = {0xFFC8CAD2, 0xFF96D7E6, 0xFFF5CD50, 0xFF5AE6FF, 0xFFFFF5DC, 0xFFFFAA00};
    private static int onglet = 0;
    private int px;
    private int py;
    private final java.util.List<EcranCamp.BoutonAoS> boutons = new java.util.ArrayList<>();

    /** Lignes de la Forge affichées dans l'onglet. */
    static int[] lignes(int o) {
        return o < 5 ? new int[] {o * 9, o * 9 + 1, o * 9 + 2, o * 9 + 3, o * 9 + 4, o * 9 + 5, o * 9 + 6, o * 9 + 7, o * 9 + 8}
                : new int[] {ARMES, ARMES + 1, ARMES + 2};
    }

    public EcranForge() {
        super(Component.literal("Forge de guerre"));
    }

    static int faction() {
        FicheHeros f = DonneesHeros.actuelle;
        return f == null ? 0 : f.faction();
    }

    @Override
    protected void init() {
        px = (this.width - PW) / 2;
        py = (this.height - PH) / 2;
        int fa = faction();
        if (fa <= 0 || fa >= ArsenalGenere.IDS.length) {
            return;
        }
        for (int o = 0; o < ONGLETS.length; o++) {
            final int oo = o;
            int w = 70;
            int x = px + 10 + o * 74;
            boutons.add(addRenderableWidget(new EcranCamp.BoutonAoS(-1, x, py + 16, w, 18, () -> Component.literal(ONGLETS[oo]),
                    () -> onglet = oo, () -> true, () -> onglet == oo, () -> true)));
        }
        for (int o = 0; o < ONGLETS.length; o++) {
            int[] l = lignes(o);
            for (int k = 0; k < l.length; k++) {
                final int ligne = l[k];
                boutons.add(addRenderableWidget(new EcranCamp.BoutonAoS(o, px + PW - 68, py + 42 + k * 22, 60, 18,
                        () -> Component.literal(ligne < 9 || ligne == ARMES ? "Forger" : "Améliorer"),
                        () -> EcranCamp.envoyer(20, ligne, ""), () -> possible(ligne), () -> false, () -> true)));
            }
        }
    }

    @Override
    public void extractRenderState(GuiGraphicsExtractor g, int sx, int sy, float partiel) {
        for (EcranCamp.BoutonAoS b : boutons) {
            b.visible = b.onglet < 0 || b.onglet == onglet;
        }
        super.extractRenderState(g, sx, sy, partiel);
    }

    static Item item(String id) {
        return BuiltInRegistries.ITEM.getValue(Identifier.parse(id));
    }

    static int compte(Item it) {
        var p = Minecraft.getInstance().player;
        if (p == null) {
            return 0;
        }
        Inventory inv = p.getInventory();
        int n = 0;
        for (int i = 0; i < inv.getContainerSize(); i++) {
            if (inv.getItem(i).is(it)) {
                n += inv.getItem(i).getCount();
            }
        }
        return n;
    }

    static int niveau() {
        FicheHeros f = DonneesHeros.actuelle;
        return f == null ? 1 : f.niveau();
    }

    static int requis(int k) {
        return k < ArsenalGenere.NIVEAUX.length ? ArsenalGenere.NIVEAUX[k] : 1;
    }

    static boolean possible(int k) {
        var p = Minecraft.getInstance().player;
        if (p != null && p.isCreative()) {
            return true;
        }
        if (niveau() < requis(k)) {
            return false;
        }
        for (String x : ArsenalGenere.RECETTES[faction()][k].split(",")) {
            String[] a = x.split("\\*");
            if (compte(item(a[0])) < Integer.parseInt(a[1])) {
                return false;
            }
        }
        return true;
    }

    @Override
    public boolean isPauseScreen() {
        return false;
    }

    @Override
    public void extractBackground(GuiGraphicsExtractor g, int sx, int sy, float partiel) {
        g.fillGradient(0, 0, this.width, this.height, 0xE0281408, 0xF00A0604);
        EcranSerment.cadre(g, px, py, PW, PH, 0xEB1A0F0A);
        EcranSerment.coins(g, px, py, PW, PH);
        g.blit(RenderPipelines.GUI_TEXTURED, EcranSerment.ORNEMENTS, px + PW / 2 - 80, py - 12, 0, 24, 160, 24, 256, 64);
        g.centeredText(this.font, "FORGE DE GUERRE", px + PW / 2, py - 4, EcranSerment.OR_CLAIR);
        int fa = faction();
        if (fa <= 0 || fa >= ArsenalGenere.IDS.length) {
            g.textWithWordWrap(this.font, Component.literal("Les maîtres-forgerons ne travaillent que pour un héros lié à une faction. "
                    + "Prête serment (touche J), puis reviens : seul l'arsenal de TA faction te sera ouvert."), px + 20, py + 40, PW - 40, 0xFFE6D3A8);
            return;
        }
        g.text(this.font, "Arsenal : " + FactionsGenerees.NOMS[fa], px + 12, py + 4, 0xFF000000 | FactionsGenerees.COULEURS[fa], true);
        int[] l = lignes(onglet);
        int req = requis(l[0]);
        String rq = onglet == 5 ? "Lignée niv. " + requis(ARMES) + " · Champion niv. " + requis(ARMES + 1) + " · Ascension niv. " + requis(ARMES + 2)
                : "Niveau de héros requis : " + req;
        g.text(this.font, rq + "  (toi : " + niveau() + ")", px + PW - 12 - this.font.width(rq + "  (toi : " + niveau() + ")"), py + 4,
                niveau() >= req ? 0xFF9EE69A : 0xFFFF6B6B, true);
        for (int k = 0; k < l.length; k++) {
            int ligne = l[k];
            int y = py + 40 + k * 22;
            g.fill(px + 8, y, px + PW - 8, y + 21, ligne % 9 < 4 || ligne >= ARMES ? 0x55402810 : 0x40203848);
            g.item(new ItemStack(item("royaumes:" + ArsenalGenere.IDS[fa][ligne])), px + 12, y + 2);
            String nom = ArsenalGenere.NOMS[fa][ligne];
            while (this.font.width(nom) > 150 && nom.length() > 4) {
                nom = nom.substring(0, nom.length() - 2) + "…";
                nom = nom.replace("……", "…");
            }
            g.text(this.font, nom, px + 32, y + 6, onglet == 5 ? (ligne == ARMES ? 0xFFE6D3A8 : COULEURS_PALIERS[5]) : COULEURS_PALIERS[onglet], true);
            if (onglet == 5 && niveau() < requis(ligne)) {
                g.text(this.font, "niv. " + requis(ligne), px + PW - 104, y + 6, 0xFFFF6B6B, true);
            }
            int x = px + 186;
            for (String ing : ArsenalGenere.RECETTES[fa][ligne].split(",")) {
                String[] a = ing.split("\\*");
                Item it = item(a[0]);
                int n = Integer.parseInt(a[1]);
                g.item(new ItemStack(it), x, y + 2);
                g.text(this.font, "" + n, x + 11, y + 11, compte(it) >= n ? 0xFF9EE69A : 0xFFFF6B6B, true);
                x += 24;
            }
        }
        String aide = switch (onglet) {
            case 0 -> "Soldat : fer et pierre des Royaumes. La panoplie complète donne le premier effet de faction.";
            case 1 -> "Élite : la pièce Soldat refondue, des diamants et des éclats de deux Royaumes étrangers.";
            case 2 -> "Légende : au-dessus de la netherite. Pièce Élite, netherite, cristal arcanique, éclats.";
            case 3 -> "Mythique : il faut les âmes des seigneurs vaincus. Panoplie : +1 niveau et 4 cœurs.";
            case 4 -> "Divin : étoile du Nether et âmes de seigneurs. Panoplie : +2 niveaux, 8 cœurs, régénération.";
            default -> "Lignée : atout à chaque coup. Champion puis Ascension : forgés à partir de l'arme précédente.";
        };
        g.centeredText(this.font, aide, px + PW / 2, py + PH - 26, 0xFFE6D3A8);
        g.centeredText(this.font, "Les éclats viennent de Royaumes étrangers : il faudra voyager ou commercer.", px + PW / 2, py + PH - 13, 0xFF9AA0B8);
    }
}
