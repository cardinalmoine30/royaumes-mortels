package fr.royaumes.client;

import fr.royaumes.ContenuGenere;
import fr.royaumes.FactionsGenerees;
import fr.royaumes.RoyaumesMortels;
import fr.royaumes.reseau.ChoixFaction;
import fr.royaumes.reseau.DonneesHeros;
import fr.royaumes.reseau.FicheHeros;
import java.util.ArrayList;
import java.util.List;
import net.minecraft.client.Minecraft;
import net.minecraft.client.gui.Font;
import net.minecraft.client.gui.GuiGraphicsExtractor;
import net.minecraft.client.gui.components.AbstractButton;
import net.minecraft.client.gui.narration.NarrationElementOutput;
import net.minecraft.client.gui.screens.Screen;
import net.minecraft.client.input.InputWithModifiers;
import net.minecraft.client.multiplayer.ClientPacketListener;
import net.minecraft.client.renderer.RenderPipelines;
import net.minecraft.network.chat.Component;
import net.minecraft.network.protocol.common.ServerboundCustomPayloadPacket;
import net.minecraft.resources.Identifier;

/**
 * Écran de serment d'allégeance (charte « or de Aurion sur bleu nuit ») :
 * à gauche les 25 blasons rangés par Grande Alliance, à droite le skin de la faction, son Royaume,
 * ses dons et son fardeau. « Prêter serment » envoie le choix au serveur (trigger rm_choix du datapack).
 * Mêmes cotes que la maquette outils/visuels/maquettes.py.
 */
public class EcranSerment extends Screen {
    static Identifier aos(String nom) {
        return Identifier.fromNamespaceAndPath(RoyaumesMortels.MODID, "textures/gui/aos/" + nom + ".png");
    }

    static final Identifier EMBLEMES = aos("emblemes");
    static final Identifier ORNEMENTS = aos("ornements");
    static final int OR = 0xFFD4A63A;
    static final int OR_CLAIR = 0xFFF2D27A;
    static final int OR_SOMBRE = 0xFF78601E;
    static final int PARCHEMIN = 0xFFE6D3A8;
    private static final int PW = 400;
    private static final int PH = 232;
    private static final String[] ALLIANCES = {"ordre", "chaos", "mort", "destruction"};
    private static final String[] NOMS_ALLIANCES = {"ORDRE", "CHAOS", "MORT", "DESTRUCTION"};
    private static final int[] COULEURS_ALLIANCES = {0xFFD4A63A, 0xFFC83C32, 0xFF9682C8, 0xFF78AA3C};

    private int px;
    private int py;
    private int choix = 0;
    private int survol = 0;
    private BoutonSerment bouton;
    private final List<BoutonBlason> blasons = new ArrayList<>();

    public EcranSerment() {
        super(Component.translatable("royaumes.serment.titre"));
    }

    static int factionActuelle() {
        FicheHeros f = DonneesHeros.actuelle;
        return f == null ? 0 : f.faction();
    }

    @Override
    protected void init() {
        px = (this.width - PW) / 2;
        py = Texte.haut(this.height, PH);
        blasons.clear();
        int y = py + 20;
        for (int a = 0; a < ALLIANCES.length; a++) {
            int j = 0;
            for (int num = 1; num < ContenuGenere.ALLIANCES.length; num++) {
                if (ALLIANCES[a].equals(ContenuGenere.ALLIANCES[num])) {
                    blasons.add(this.addRenderableWidget(new BoutonBlason(px + 11 + j * 21, y + 13, num)));
                    j++;
                }
            }
            y += 46;
        }
        if (choix == 0) {
            choix = factionActuelle();
        }
        int qx = px + 210;
        int qw = 180;
        int qh = PH - 28;
        bouton = this.addRenderableWidget(new BoutonSerment(qx + qw / 2 - 60, py + 18 + qh - 26));
    }

    @Override
    public boolean isPauseScreen() {
        return false;
    }

    // ------------------------------------------------------------------ rendu

    @Override
    public void extractBackground(GuiGraphicsExtractor g, int sx, int sy, float partiel) {
        g.fillGradient(0, 0, this.width, this.height, 0xF0162648, 0xF8060A16);
        // éclairs d'Célestis discrets
        for (int k = 0; k < 2; k++) {
            int x0 = k == 0 ? px - 20 : px + PW + 20;
            g.fill(x0, 0, x0 + 1, 40, 0x662C5AA0);
            g.fill(x0 + 1, 40, x0 + 2, 70, 0x662C5AA0);
            g.fill(x0 - 1, 70, x0, 120, 0x662C5AA0);
        }
        cadre(g, px, py, PW, PH, 0xEB0C1428);
        coins(g, px, py, PW, PH);
        g.blit(RenderPipelines.GUI_TEXTURED, ORNEMENTS, px + PW / 2 - 80, py - 10, 0, 24, 160, 24, 256, 64);
        g.centeredText(this.font, Component.translatable("royaumes.serment.titre").getString().toUpperCase(), px + PW / 2, py - 2, OR_CLAIR);
        // colonne des alliances
        int y = py + 20;
        for (int a = 0; a < ALLIANCES.length; a++) {
            g.text(this.font, NOMS_ALLIANCES[a], px + 12, y, COULEURS_ALLIANCES[a], true);
            g.fill(px + 12, y + 10, px + 200, y + 11, COULEURS_ALLIANCES[a]);
            y += 46;
        }
        Texte.ligne(g, this.font, Component.translatable("royaumes.serment.aide").getString(), px + 12, py + PH - 22, 192, 0xFFA0AAC8, false);
        Texte.ligne(g, this.font, Component.translatable("royaumes.serment.touche", ClientRoyaumes.TOUCHE_SERMENT.getTranslatedKeyMessage()).getString(), px + 12, py + PH - 12, 192, 0xFFA0AAC8, false);
        // panneau de la faction
        int qx = px + 210;
        int qy = py + 18;
        int qw = 180;
        int qh = PH - 28;
        cadre(g, qx, qy, qw, qh, 0xFF181E34);
        int f = survol > 0 ? survol : (choix > 0 ? choix : 1);
        panneau(g, f, qx, qy, qw);
    }

    private void panneau(GuiGraphicsExtractor g, int f, int qx, int qy, int qw) {
        Font police = this.font;
        int a = indexAlliance(ContenuGenere.ALLIANCES[f]);
        Texte.centre(g, police, FactionsGenerees.NOMS[f], qx + qw / 2, qy + 6, qw - 10, OR_CLAIR);
        Texte.centre(g, police, nomAlliance(a) + " · " + ContenuGenere.ROYAUMES[f], qx + qw / 2, qy + 17, qw - 10, COULEURS_ALLIANCES[Math.max(0, a)]);
        // aperçu du skin
        g.fill(qx + 8, qy + 28, qx + 56, qy + 100, 0xFF0A1020);
        g.fill(qx + 8, qy + 28, qx + 56, qy + 29, OR_SOMBRE);
        g.fill(qx + 8, qy + 99, qx + 56, qy + 100, OR_SOMBRE);
        g.fill(qx + 8, qy + 28, qx + 9, qy + 100, OR_SOMBRE);
        g.fill(qx + 55, qy + 28, qx + 56, qy + 100, OR_SOMBRE);
        long t = System.currentTimeMillis() / 3000;
        poupee(g, FactionsGenerees.IDS[f], qx + 16, qy + 32, (t % 2) == 1);
        // blason + description
        g.blit(RenderPipelines.GUI_TEXTURED, EMBLEMES, qx + 62, qy + 28, ((f - 1) % 8) * 32, ((f - 1) / 8) * 32, 24, 24, 32, 32, 256, 128);
        int vent = ContenuGenere.VENT_FACTION[f];
        Texte.ligne(g, police, "Vent : " + ContenuGenere.NOMS_VENTS[vent], qx + 90, qy + 36, qw - 96, 0xFF000000 | ContenuGenere.COULEURS_VENTS[vent], true);
        Texte.ligne(g, police, "[R] " + ContenuGenere.CAP_NOMS[f], qx + 62, qy + 56, qw - 68, 0xFFF2D27A, true);
        Texte.bloc(g, police, ContenuGenere.CAP_DESC[f], qx + 62, qy + 66, qw - 68, 34, 0xFFBFB2E6, false);
        // dons et fardeau : jusqu'au bouton du serment
        int bas = qy + (PH - 28) - 28;
        int y = qy + 104;
        g.text(police, Component.translatable("royaumes.serment.dons"), qx + 8, y, 0xFF7EC86E, true);
        y += 10;
        int place = (bas - y - 10) / 2;
        y += Texte.bloc(g, police, ContenuGenere.DONS[f], qx + 8, y, qw - 16, place, 0xFFC8E6BE, false) + 2;
        g.text(police, Component.translatable("royaumes.serment.fardeau"), qx + 8, y, 0xFFDC6050, true);
        y += 10;
        Texte.bloc(g, police, ContenuGenere.FARDEAUX[f], qx + 8, y, qw - 16, Math.max(9, bas - y), 0xFFF0BEB4, false);
    }

    /** Skin plat (face ou dos), comme sur la planche des skins. */
    private static void poupee(GuiGraphicsExtractor g, String faction, int x, int y, boolean dos) {
        Identifier skin = Identifier.fromNamespaceAndPath(RoyaumesMortels.MODID, "textures/skin/" + faction + ".png");
        int[][] face = {{8, 8, 8, 8, 4, 0}, {20, 20, 8, 12, 4, 8}, {44, 20, 4, 12, 0, 8}, {36, 52, 4, 12, 12, 8},
                {4, 20, 4, 12, 4, 20}, {20, 52, 4, 12, 8, 20}, {40, 8, 8, 8, 4, 0},
                {20, 36, 8, 12, 4, 8}, {44, 36, 4, 12, 0, 8}, {52, 52, 4, 12, 12, 8}, {4, 36, 4, 12, 4, 20}, {4, 52, 4, 12, 8, 20}};
        int[][] arriere = {{24, 8, 8, 8, 4, 0}, {32, 20, 8, 12, 4, 8}, {52, 20, 4, 12, 12, 8}, {44, 52, 4, 12, 0, 8},
                {12, 20, 4, 12, 8, 20}, {28, 52, 4, 12, 4, 20}, {56, 8, 8, 8, 4, 0},
                {32, 36, 8, 12, 4, 8}, {52, 36, 4, 12, 12, 8}, {60, 52, 4, 12, 0, 8}, {12, 36, 4, 12, 8, 20}, {12, 52, 4, 12, 4, 20}};
        g.pose().pushMatrix();
        g.pose().translate(x, y);
        g.pose().scale(2.0F, 2.0F);
        for (int[] p : dos ? arriere : face) {
            g.blit(RenderPipelines.GUI_TEXTURED, skin, p[4], p[5], p[0], p[1], p[2], p[3], 64, 64);
        }
        g.pose().popMatrix();
    }

    static void cadre(GuiGraphicsExtractor g, int x, int y, int w, int h, int fond) {
        g.fill(x, y, x + w, y + h, fond);
        g.fill(x, y, x + w, y + 1, OR);
        g.fill(x, y + h - 1, x + w, y + h, OR);
        g.fill(x, y, x + 1, y + h, OR);
        g.fill(x + w - 1, y, x + w, y + h, OR);
        g.fill(x + 2, y + 2, x + w - 2, y + 3, OR_SOMBRE);
        g.fill(x + 2, y + h - 3, x + w - 2, y + h - 2, OR_SOMBRE);
        g.fill(x + 2, y + 2, x + 3, y + h - 2, OR_SOMBRE);
        g.fill(x + w - 3, y + 2, x + w - 2, y + h - 2, OR_SOMBRE);
    }

    static void coins(GuiGraphicsExtractor g, int x, int y, int w, int h) {
        int[][] pos = {{x - 4, y - 4}, {x + w - 12, y - 4}, {x - 4, y + h - 12}, {x + w - 12, y + h - 12}};
        for (int k = 0; k < 4; k++) {
            g.blit(RenderPipelines.GUI_TEXTURED, ORNEMENTS, pos[k][0], pos[k][1], k * 16, 0, 16, 16, 256, 64);
        }
    }

    private static int indexAlliance(String a) {
        for (int i = 0; i < ALLIANCES.length; i++) {
            if (ALLIANCES[i].equals(a)) {
                return i;
            }
        }
        return -1;
    }

    private static String nomAlliance(int a) {
        return a < 0 ? "" : NOMS_ALLIANCES[a].charAt(0) + NOMS_ALLIANCES[a].substring(1).toLowerCase();
    }

    @Override
    public void extractRenderState(GuiGraphicsExtractor g, int sx, int sy, float partiel) {
        survol = 0;
        for (BoutonBlason b : blasons) {
            if (b.isHovered()) {
                survol = b.faction;
            }
        }
        bouton.active = choix > 0 && factionActuelle() == 0;
        super.extractRenderState(g, sx, sy, partiel);
    }

    private void preterSerment() {
        if (choix <= 0 || factionActuelle() != 0) {
            return;
        }
        ClientPacketListener connexion = Minecraft.getInstance().getConnection();
        if (connexion != null) {
            try {
                connexion.send(new ServerboundCustomPayloadPacket(new ChoixFaction(choix)));
            } catch (RuntimeException e) {
                RoyaumesMortels.LOGGER.warn("[Royaumes Mortels] Serment non transmis : {}", e.toString());
            }
        }
        this.onClose();
    }

    // ------------------------------------------------------------------ boutons

    private class BoutonBlason extends AbstractButton {
        final int faction;

        BoutonBlason(int x, int y, int faction) {
            super(x, y, 22, 22, Component.literal(FactionsGenerees.NOMS[faction]));
            this.faction = faction;
        }

        @Override
        public void onPress(InputWithModifiers entree) {
            if (factionActuelle() == 0) {
                choix = faction;
            }
        }

        @Override
        protected void extractContents(GuiGraphicsExtractor g, int sx, int sy, float partiel) {
            boolean marque = faction == choix || this.isHovered();
            if (marque) {
                g.fill(getX(), getY(), getX() + 22, getY() + 22, 0xFF3C3014);
                int c = this.isHovered() ? OR_CLAIR : OR;
                g.fill(getX(), getY(), getX() + 22, getY() + 1, c);
                g.fill(getX(), getY() + 21, getX() + 22, getY() + 22, c);
                g.fill(getX(), getY(), getX() + 1, getY() + 22, c);
                g.fill(getX() + 21, getY(), getX() + 22, getY() + 22, c);
            }
            int u = ((faction - 1) % 8) * 32;
            int v = ((faction - 1) / 8) * 32;
            g.blit(RenderPipelines.GUI_TEXTURED, EMBLEMES, getX() + 1, getY() + 1, u, v, 20, 20, 32, 32, 256, 128);
        }

        @Override
        protected void updateWidgetNarration(NarrationElementOutput sortie) {
            this.defaultButtonNarrationText(sortie);
        }
    }

    private class BoutonSerment extends AbstractButton {
        BoutonSerment(int x, int y) {
            super(x, y, 120, 20, Component.translatable("royaumes.serment.bouton"));
        }

        @Override
        public void onPress(InputWithModifiers entree) {
            preterSerment();
        }

        @Override
        protected void extractContents(GuiGraphicsExtractor g, int sx, int sy, float partiel) {
            int u = this.active && this.isHovered() ? 128 : 64;
            g.blit(RenderPipelines.GUI_TEXTURED, ORNEMENTS, getX(), getY(), u, 0, 120, 20, 64, 20, 256, 64);
            Component texte = factionActuelle() > 0 ? Component.translatable("royaumes.serment.deja") : getMessage();
            Texte.centre(g, Minecraft.getInstance().font, texte.getString(), getX() + 60, getY() + 6, 112, this.active ? OR_CLAIR : 0xFF8C8C8C);
            if (!this.active) {
                g.fill(getX() + 2, getY() + 2, getX() + 118, getY() + 18, 0x66000000);
            }
        }

        @Override
        protected void updateWidgetNarration(NarrationElementOutput sortie) {
            this.defaultButtonNarrationText(sortie);
        }
    }
}
