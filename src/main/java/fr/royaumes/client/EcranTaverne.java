package fr.royaumes.client;

import fr.royaumes.FactionsGenerees;
import fr.royaumes.RoyaumesMortels;
import fr.royaumes.reseau.DonneesHeros;
import fr.royaumes.reseau.FicheHeros;
import java.util.ArrayList;
import java.util.List;
import net.minecraft.client.gui.GuiGraphicsExtractor;
import net.minecraft.client.gui.screens.inventory.InventoryScreen;
import net.minecraft.client.renderer.RenderPipelines;
import net.minecraft.network.chat.Component;
import net.minecraft.resources.Identifier;
import net.minecraft.world.entity.player.Player;

/**
 * Inventaire « table de taverne » : l'inventaire est un parchemin cloué sur une table de chêne,
 * entouré d'une chope, d'une bougie, de dés et du Carnet du Héros (niveau, gloire, compétences).
 * Des onglets ouvrent le Codex, la Forge, les Blocs et la Fiche du héros.
 */
public class EcranTaverne extends InventoryScreen {
    static Identifier tex(String nom) {
        return Identifier.fromNamespaceAndPath(RoyaumesMortels.MODID, "textures/gui/taverne/" + nom + ".png");
    }

    static final Identifier TABLE = tex("table");
    static final Identifier PANNEAU = tex("inventaire");
    static final Identifier CARNET = tex("carnet");
    static final Identifier DECOR = tex("decor");
    static final Identifier ONGLETS = tex("onglets");

    private static final String[][] DEFS = {
            {"Codex", "Codex des Royaumes Mortels : voyages, gloire, forge, boss, montures", "trigger rm_codex"},
            {"Forge", "Hub d'artisanat : toutes les recettes en images, ce que tu as et ce qu'il te manque", ""},
            {"Blocs", "Ressources et blocs des Royaumes", "trigger rm_blocs"},
            {"Héros", "Ta voie : Guerrier, Mage ou Éclaireur, et ses talents (les points de compétence se dépensent dans le Carnet, à gauche)", ""},
    };
    private static final int ENCRE = 0xFF4A2E14;
    private final List<Onglet> onglets = new ArrayList<>();
    private final List<BoutonPlus> plus = new ArrayList<>();

    public EcranTaverne(Player joueur) {
        super(joueur);
    }

    @Override
    protected void init() {
        super.init();
        onglets.clear();
        for (int i = 0; i < DEFS.length; i++) {
            final int ii = i;
            Runnable ouvrir = !DEFS[i][2].isEmpty() ? null
                    : () -> this.minecraft.gui.setScreen(ii == 1 ? new EcranArtisanat() : new EcranVoies());
            onglets.add(this.addRenderableWidget(new Onglet(0, 0, i, Component.literal(DEFS[i][0]),
                    Component.literal(DEFS[i][1]), DEFS[i][2], ouvrir)));
        }
        plus.clear();
        for (int i = 0; i < FactionsGenerees.NOMS_COMPETENCES.length; i++) {
            final int comp = i;
            plus.add(this.addRenderableWidget(new BoutonPlus(comp)));
        }
        placer();
    }

    private void placer() {
        int total = DEFS.length * Onglet.L + (DEFS.length - 1) * 2;
        int x0 = this.leftPos + (this.imageWidth - total) / 2;
        for (int i = 0; i < onglets.size(); i++) {
            onglets.get(i).setX(x0 + i * (Onglet.L + 2));
            onglets.get(i).setY(this.topPos - Onglet.H + 3);
        }
        FicheHeros f = DonneesHeros.actuelle;
        int x0 = this.leftPos - 122;
        boolean carnet = !livreDeRecettesOuvert() && x0 >= 2 && f != null;
        for (BoutonPlus b : plus) {
            b.setX(x0 + 103);
            b.setY(this.topPos + 92 + b.comp * 10);
            int rang = f != null && b.comp < f.rangs().length ? f.rangs()[b.comp] : 0;
            b.visible = carnet && f.points() > 0 && rang < FactionsGenerees.RANG_MAX;
        }
    }

    /** Bouton « + » du Carnet : dépense un point de compétence (trigger silencieux, sans ouvrir la fiche dans le tchat). */
    private static final class BoutonPlus extends net.minecraft.client.gui.components.AbstractButton {
        final int comp;

        BoutonPlus(int comp) {
            super(0, 0, 9, 9, Component.literal("+"));
            this.comp = comp;
            this.setTooltip(net.minecraft.client.gui.components.Tooltip.create(Component.literal(
                    "Dépenser un point : " + FactionsGenerees.NOMS_COMPETENCES[comp] + " +1")));
        }

        @Override
        public void onPress(net.minecraft.client.input.InputWithModifiers entree) {
            var c = net.minecraft.client.Minecraft.getInstance().getConnection();
            if (c != null) {
                c.sendCommand("trigger rm_comp set " + (11 + comp));
            }
        }

        @Override
        protected void extractContents(GuiGraphicsExtractor g, int sx, int sy, float partiel) {
            boolean s = this.isHoveredOrFocused();
            g.fill(getX(), getY(), getX() + 9, getY() + 9, s ? 0xFF7A1E14 : 0xFF5A3A1A);
            g.fill(getX() + 1, getY() + 1, getX() + 8, getY() + 8, s ? 0xFFD6AA3C : 0xFFB48A3A);
            g.fill(getX() + 4, getY() + 2, getX() + 5, getY() + 7, 0xFF3A2414);
            g.fill(getX() + 2, getY() + 4, getX() + 7, getY() + 5, 0xFF3A2414);
        }

        @Override
        protected void updateWidgetNarration(net.minecraft.client.gui.narration.NarrationElementOutput sortie) {
            this.defaultButtonNarrationText(sortie);
        }
    }

    @Override
    public void containerTick() {
        super.containerTick();
        placer();
    }

    private boolean livreDeRecettesOuvert() {
        return this.leftPos != (this.width - this.imageWidth) / 2;
    }

    @Override
    public void extractBackground(GuiGraphicsExtractor g, int sourisX, int sourisY, float partiel) {
        // la table de chêne, puis l'ombre de la salle
        for (int x = 0; x < this.width; x += 256) {
            for (int y = 0; y < this.height; y += 256) {
                g.blit(RenderPipelines.GUI_TEXTURED, TABLE, x, y, 0, 0, 256, 256, 256, 256);
            }
        }
        g.fillGradient(0, 0, this.width, this.height / 4, 0x99000000, 0x00000000);
        g.fillGradient(0, this.height * 3 / 4, this.width, this.height, 0x00000000, 0xAA000000);
        for (int k = 0; k < 8; k++) {
            int a = (int) (110 * (1 - k / 8.0)) << 24;
            g.fill(k * 6, 0, k * 6 + 6, this.height, a);
            g.fill(this.width - k * 6 - 6, 0, this.width - k * 6, this.height, a);
        }
        decor(g);
        if (!livreDeRecettesOuvert()) {
            carnet(g);
        }
        g.blit(RenderPipelines.GUI_TEXTURED, PANNEAU, this.leftPos, this.topPos, 0, 0, this.imageWidth, this.imageHeight, 256, 256);
        InventoryScreen.extractEntityInInventoryFollowsMouse(g, this.leftPos + 26, this.topPos + 8, this.leftPos + 75,
                this.topPos + 78, 30, 0.0625F, sourisX, sourisY, this.minecraft.player);
    }

    private void sprite(GuiGraphicsExtractor g, int u, int v, int w, int h, int x, int y) {
        g.blit(RenderPipelines.GUI_TEXTURED, DECOR, x, y, u, v, w, h, 256, 256);
    }

    private void decor(GuiGraphicsExtractor g) {
        int l = this.leftPos;
        int t = this.topPos;
        int bx = Math.max(4, l - 190);
        sprite(g, 128, 0, 96, 96, bx - 30, t + 10);       // halo de la bougie
        sprite(g, 48, 0, 24, 64, bx + 6, t + 40);         // bougie
        sprite(g, 0, 104, 80, 18, l - 110, t + 176);      // dague
        sprite(g, 0, 64, 72, 34, l + 186, t - 34);        // carte roulée
        sprite(g, 80, 0, 36, 22, l + 186, t + 10);        // pièces
        sprite(g, 0, 0, 40, 48, l + 196, t + 112);        // chope
        sprite(g, 80, 24, 30, 16, l + 238, t + 146);      // dés
    }

    private void carnet(GuiGraphicsExtractor g) {
        int x0 = this.leftPos - 122;
        int y0 = this.topPos;
        if (x0 < 2) {
            return;
        }
        g.blit(RenderPipelines.GUI_TEXTURED, CARNET, x0, y0, 0, 0, 118, 166, 256, 256);
        g.text(this.font, "Carnet du Héros", x0 + 18, y0 + 7, ENCRE, false);
        FicheHeros f = DonneesHeros.actuelle;
        if (f == null) {
            g.text(this.font, "La plume attend…", x0 + 10, y0 + 36, 0xFF7A5A3A, false);
            return;
        }
        if (f.faction() > 0 && f.faction() < FactionsGenerees.NOMS.length) {
            Texte.ligne(g, this.font, FactionsGenerees.NOMS[f.faction()], x0 + 10, y0 + 21, 98,
                    sombre(FactionsGenerees.COULEURS[f.faction()]), false);
        } else {
            g.text(this.font, "Sans allégeance", x0 + 10, y0 + 21, 0xFF7A5A3A, false);
        }
        g.text(this.font, "Niveau " + f.niveau(), x0 + 10, y0 + 36, ENCRE, false);
        int besoin = Math.max(1, f.besoin());
        int plein = Math.min(95, 95 * Math.max(0, f.gloire()) / besoin);
        g.fill(x0 + 10, y0 + 49, x0 + 107, y0 + 56, 0xFF50382A);
        g.fill(x0 + 11, y0 + 50, x0 + 11 + plein, y0 + 55, 0xFFD6AA3C);
        g.fill(x0 + 11, y0 + 50, x0 + 11 + plein, y0 + 51, 0xFFF4D27A);
        Texte.ligne(g, this.font, "Gloire " + f.gloire() + " / " + f.besoin(), x0 + 10, y0 + 59, 98, 0xFF6E5028, false);
        Texte.ligne(g, this.font, f.points() > 0 ? "Points : " + f.points() + "  (boutons +)" : "Points : 0", x0 + 10, y0 + 70, 98,
                f.points() > 0 ? 0xFF286E28 : 0xFF6E5028, false);
        int voie = f.progres() != null && f.progres().length > 4 ? f.progres()[4] : 0;
        Texte.ligne(g, this.font, voie > 0 && voie < fr.royaumes.rpg.Voies.NOMS.length ? "Voie : " + fr.royaumes.rpg.Voies.NOMS[voie]
                : (f.niveau() >= fr.royaumes.rpg.Voies.NIVEAU_VOIE ? "Voie à choisir : onglet Héros" : "Voie : au niveau " + fr.royaumes.rpg.Voies.NIVEAU_VOIE),
                x0 + 10, y0 + 80, 98, voie > 0 ? 0xFF6E3A8C : 0xFF8C5A28, false);
        int n = Math.min(f.rangs().length, FactionsGenerees.NOMS_COMPETENCES.length);
        for (int i = 0; i < n; i++) {
            int y = y0 + 92 + i * 10;
            Texte.ligne(g, this.font, FactionsGenerees.NOMS_COMPETENCES[i], x0 + 8, y, 52, sombre(FactionsGenerees.COULEURS_COMPETENCES[i]), false);
            for (int r = 0; r < FactionsGenerees.RANG_MAX; r++) {
                int px = x0 + 61 + r * 4;
                g.fill(px, y + 2, px + 3, y + 6, r < f.rangs()[i] ? 0xFF962820 : 0xFFC4B088);
            }
        }
    }

    /** Couleur de faction assombrie pour rester lisible sur le parchemin. */
    private static int sombre(int rgb) {
        int r = (int) (((rgb >> 16) & 0xFF) * 0.55);
        int v = (int) (((rgb >> 8) & 0xFF) * 0.55);
        int b = (int) ((rgb & 0xFF) * 0.55);
        return 0xFF000000 | (r << 16) | (v << 8) | b;
    }
}
