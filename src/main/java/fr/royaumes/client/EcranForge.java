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
    private static final int PW = 420;
    private static final int PH = 262;
    private static final String[] ONGLETS = {"Soldat", "Élite", "Légende", "Armes de faction"};
    private static int onglet = 0;
    private int px;
    private int py;
    private final java.util.List<EcranCamp.BoutonAoS> boutons = new java.util.ArrayList<>();

    /** Lignes de la Forge affichées dans l'onglet. */
    static int[] lignes(int o) {
        return o < 3 ? new int[] {o * 9, o * 9 + 1, o * 9 + 2, o * 9 + 3, o * 9 + 4, o * 9 + 5, o * 9 + 6, o * 9 + 7, o * 9 + 8} : new int[] {27, 28};
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
            int w = o == 3 ? 120 : 80;
            int x = px + 10 + o * 86;
            boutons.add(addRenderableWidget(new EcranCamp.BoutonAoS(-1, x, py + 16, w, 18, () -> Component.literal(ONGLETS[oo]),
                    () -> onglet = oo, () -> true, () -> onglet == oo, () -> true)));
        }
        for (int o = 0; o < ONGLETS.length; o++) {
            int[] l = lignes(o);
            for (int k = 0; k < l.length; k++) {
                final int ligne = l[k];
                boutons.add(addRenderableWidget(new EcranCamp.BoutonAoS(o, px + PW - 70, py + 42 + k * 22, 60, 18,
                        () -> Component.literal(ligne < 9 || ligne == 27 ? "Forger" : "Améliorer"),
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

    static boolean possible(int k) {
        var p = Minecraft.getInstance().player;
        if (p != null && p.isCreative()) {
            return true;
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
        for (int k = 0; k < l.length; k++) {
            int ligne = l[k];
            int y = py + 40 + k * 22;
            g.fill(px + 8, y, px + PW - 8, y + 21, ligne % 9 < 4 || ligne >= 27 ? 0x55402810 : 0x40203848);
            g.item(new ItemStack(item("royaumes:" + ArsenalGenere.IDS[fa][ligne])), px + 12, y + 2);
            g.text(this.font, ArsenalGenere.NOMS[fa][ligne], px + 32, y + 6, ligne == 28 || ligne >= 18 && ligne < 27 ? 0xFFFFAA00 : 0xFFE6D3A8, true);
            int x = px + 200;
            for (String ing : ArsenalGenere.RECETTES[fa][ligne].split(",")) {
                String[] a = ing.split("\\*");
                Item it = item(a[0]);
                int n = Integer.parseInt(a[1]);
                g.item(new ItemStack(it), x, y + 2);
                g.text(this.font, "" + n, x + 11, y + 11, compte(it) >= n ? 0xFF9EE69A : 0xFFFF6B6B, true);
                x += 26;
            }
        }
        String aide = onglet == 0 ? "Palier 1 : fer et pierre des Royaumes. Élite et Légende : éclats de Royaumes étrangers."
                : onglet == 3 ? "Lignée : atout à chaque coup. Champion : forgé à partir de l'arme de lignée."
                : "Chaque amélioration exige la pièce du palier précédent (elle est refondue).";
        g.centeredText(this.font, aide, px + PW / 2, py + PH - 26, 0xFFE6D3A8);
        g.centeredText(this.font, "Les éclats viennent de Royaumes étrangers : il faudra voyager ou commercer.", px + PW / 2, py + PH - 13, 0xFF9AA0B8);
    }
}
