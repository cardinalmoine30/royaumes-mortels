package fr.royaumes.client;

import fr.royaumes.reseau.ActionCamp;
import fr.royaumes.reseau.DonneesHeros;
import fr.royaumes.reseau.FicheCamp;
import java.util.ArrayList;
import java.util.List;
import java.util.function.BooleanSupplier;
import java.util.function.Supplier;
import net.minecraft.client.Minecraft;
import net.minecraft.client.gui.GuiGraphicsExtractor;
import net.minecraft.client.gui.components.AbstractButton;
import net.minecraft.client.gui.narration.NarrationElementOutput;
import net.minecraft.client.gui.screens.Screen;
import net.minecraft.client.input.InputWithModifiers;
import net.minecraft.client.multiplayer.ClientPacketListener;
import net.minecraft.client.renderer.RenderPipelines;
import net.minecraft.network.chat.Component;
import net.minecraft.network.protocol.common.ServerboundCustomPayloadPacket;

/** Écran du camp de guerre, en onglets : Camp, Bâtiments, Exploration, Raids, Alliés. */
public class EcranCamp extends Screen {
    private static final int PW = 400;
    private static final int PH = 250;
    private static final String[] ONGLETS = {"Camp", "Bâtiments", "Exploration", "Raids", "Alliés"};
    private static final String[] RAIDS = {"Pillage", "Assaut", "Croisade", "Raid joueur"};
    private static final int[] DUREE = {2, 5, 10};
    private static final int[] DIFF = {15, 40, 90};
    private static final int[] DEBLOQUEES = {0, 2, 3, 5, 6, 8};
    private static final String[] BATS = {"Forge", "Ferme", "Sanctuaire", "Caserne", "Tour de guet"};
    private static final int[] COUT_BAT = {0, 40, 120, 300};
    private static final int[] CAMP_REQUIS = {0, 1, 2, 4};
    private static int onglet = 0;
    private int px;
    private int py;
    private final List<BoutonAoS> boutons = new ArrayList<>();

    public EcranCamp() {
        super(Component.literal("Camp de guerre"));
    }

    static FicheCamp f() {
        return DonneesHeros.camp;
    }

    static boolean proprio() {
        return f() != null && f().proprio();
    }

    static int niveauRequis(int i) {
        for (int n = 1; n < DEBLOQUEES.length; n++) {
            if (DEBLOQUEES[n] > i) {
                return n;
            }
        }
        return 5;
    }

    static void envoyer(int action, int arg, String texte) {
        ClientPacketListener c = Minecraft.getInstance().getConnection();
        if (c != null) {
            try {
                c.send(new ServerboundCustomPayloadPacket(new ActionCamp(action, arg, texte)));
            } catch (RuntimeException e) {
                // serveur sans le mod
            }
        }
    }

    static String effet(int b, int n) {
        if (n <= 0) {
            return "Pas encore construit";
        }
        return switch (b) {
            case 0 -> n == 1 ? "2 fer, 2 charbon / min" : n == 2 ? "3 fer, 3 charbon, 1 or / min" : "5 fer, 4 charbon, 2 or, pierre / min";
            case 1 -> n == 1 ? "2 pains, 2 blé / min" : n == 2 ? "3 pains, 2 bœufs, 2 carottes / min" : "4 pains, 3 bœufs, carottes dorées";
            case 2 -> n == 1 ? "1 éclat de Vent / 3 min" : n == 2 ? "1 éclat / min, 1 cristal / 3 min" : "1 éclat et 1 cristal / min";
            case 3 -> "+" + (2 * n) + " places, recrutement -" + (10 * n) + " %";
            case 4 -> "Défense +" + new int[] {0, 15, 35, 60}[n] + " %, exploration +" + (15 * n) + " %";
            default -> "";
        };
    }

    private void bouton(int ong, int x, int y, int w, Supplier<String> t, Runnable a, BooleanSupplier actif, BooleanSupplier choisi,
                        BooleanSupplier visible) {
        BoutonAoS b = new BoutonAoS(ong, x, y, w, 18, () -> Component.literal(t.get()), a, actif, choisi, visible);
        boutons.add(b);
        addRenderableWidget(b);
    }

    private static boolean libre() {
        return f() != null && f().raidReste() < 0;
    }

    @Override
    protected void init() {
        px = (this.width - PW) / 2;
        py = (this.height - PH) / 2;
        boutons.clear();
        int x = px + 12;
        BooleanSupplier oui = () -> true;
        BooleanSupplier non = () -> false;
        BooleanSupplier chef = EcranCamp::proprio;
        for (int i = 0; i < ONGLETS.length; i++) {
            final int k = i;
            bouton(-1, px + 10 + i * 76, py + 10, 74, () -> ONGLETS[k], () -> onglet = k, oui, () -> onglet == k, () -> proprio() || k == 0);
        }
        // --- Camp
        bouton(0, x, py + 76, 90, () -> "Garder le camp", () -> envoyer(4, 0, ""), oui, () -> f() != null && f().ordre() == 0, chef);
        bouton(0, x + 94, py + 76, 90, () -> "Me suivre", () -> envoyer(4, 1, ""), oui, () -> f() != null && f().ordre() == 1, chef);
        bouton(0, x, py + 100, 184, () -> proprio() ? "Déposer le butin" : "Offrir du butin à ce camp", () -> envoyer(3, 0, ""), oui, non, oui);
        bouton(0, x, py + 122, 184, () -> f() == null || f().coutNiveau() == 0 ? "Camp au niveau maximum" : "Améliorer le camp — " + f().coutNiveau(),
                () -> envoyer(2, 0, ""), () -> f() != null && f().coutNiveau() > 0 && f().butin() >= f().coutNiveau(), non, chef);
        for (int i = 0; i < 8; i++) {
            final int k = i;
            bouton(0, px + 330, py + 48 + i * 24, 52, () -> "Recruter", () -> envoyer(1, k, ""),
                    () -> f() != null && k < f().debloquees() && k < f().couts().size() && f().butin() >= f().couts().get(k) && f().unites() < f().max(),
                    non, () -> proprio() && f().recrues().size() > k);
        }
        // --- Bâtiments
        for (int b = 0; b < BATS.length; b++) {
            final int k = b;
            bouton(1, px + 296, py + 38 + b * 40, 92, () -> {
                int n = f() == null ? 0 : f().batiments()[k];
                return n >= 3 ? "Niveau max" : (n == 0 ? "Bâtir — " : "Améliorer — ") + COUT_BAT[n + 1];
            }, () -> envoyer(6, k, ""), () -> {
                if (f() == null) {
                    return false;
                }
                int n = f().batiments()[k];
                return n < 3 && f().butin() >= COUT_BAT[n + 1] && f().niveau() >= CAMP_REQUIS[n + 1];
            }, non, chef);
        }
        // --- Exploration
        int[] eclaireurs = {1, 3, 5};
        for (int i = 0; i < 3; i++) {
            final int n = eclaireurs[i];
            bouton(2, x, py + 112 + i * 22, 184, () -> "Envoyer " + n + " éclaireur" + (n > 1 ? "s" : ""), () -> envoyer(9, n, ""),
                    () -> f() != null && f().explReste() < 0 && f().force() > 0, non, chef);
        }
        // --- Raids
        for (int k = 0; k < 3; k++) {
            final int t = k;
            bouton(3, x, py + 50 + k * 22, 184, () -> {
                int force = f() == null ? 0 : f().force();
                return RAIDS[t] + " · " + DUREE[t] + " min · " + (force <= 0 ? 0 : 100 * force / (force + DIFF[t])) + " %";
            }, () -> envoyer(5, t, ""), () -> libre() && f().force() > 0, non, chef);
        }
        for (int i = 0; i < 5; i++) {
            final int k = i;
            bouton(3, px + 330, py + 56 + i * 30, 56, () -> "Attaquer", () -> envoyer(10, 0, f().cibles().get(k)),
                    () -> libre() && f().force() > 0, non, () -> proprio() && f().cibles().size() > k);
        }
        // --- Alliés
        for (int i = 0; i < 5; i++) {
            final int k = i;
            bouton(4, x + 124, py + 52 + i * 24, 60, () -> "Retirer", () -> envoyer(8, 0, f().invites().get(k)), oui, non,
                    () -> proprio() && f().invites().size() > k);
            bouton(4, px + 322, py + 52 + i * 24, 66, () -> "Inviter", () -> envoyer(7, 0, f().proches().get(k)), oui, non,
                    () -> proprio() && f().proches().size() > k);
        }
    }

    @Override
    public boolean isPauseScreen() {
        return false;
    }

    @Override
    public void extractRenderState(GuiGraphicsExtractor g, int sx, int sy, float partiel) {
        if (!proprio()) {
            onglet = 0;
        }
        for (BoutonAoS b : boutons) {
            b.visible = (b.onglet < 0 || b.onglet == onglet) && b.visibleSi.getAsBoolean();
        }
        super.extractRenderState(g, sx, sy, partiel);
    }

    private void t(GuiGraphicsExtractor g, String s, int x, int y, int c) {
        g.text(this.font, s, x, y, c, true);
    }

    private void titre(GuiGraphicsExtractor g, String s, int x, int y, int w) {
        g.text(this.font, s, x, y, EcranSerment.OR, true);
        g.fill(x, y + 9, x + w, y + 10, EcranSerment.OR);
    }

    @Override
    public void extractBackground(GuiGraphicsExtractor g, int sx, int sy, float partiel) {
        g.fillGradient(0, 0, this.width, this.height, 0xE0162648, 0xF0060A16);
        EcranSerment.cadre(g, px, py, PW, PH, 0xEB0C1428);
        EcranSerment.coins(g, px, py, PW, PH);
        g.blit(RenderPipelines.GUI_TEXTURED, EcranSerment.ORNEMENTS, px + PW / 2 - 80, py - 12, 0, 24, 160, 24, 256, 64);
        FicheCamp fc = f();
        g.centeredText(this.font, fc != null && !fc.proprio() ? "CAMP DE " + fc.chef().toUpperCase() : "CAMP DE GUERRE", px + PW / 2, py - 4,
                EcranSerment.OR_CLAIR);
        if (fc == null) {
            return;
        }
        int x = px + 12;
        int y = py + 34;
        int or = 0xFFF2D27A;
        int parch = 0xFFE6D3A8;
        int gris = 0xFF9AA0B8;
        switch (onglet) {
            case 0 -> {
                t(g, "Niveau " + fc.niveau() + " / 5", x, y, EcranSerment.OR_CLAIR);
                t(g, "Butin : " + fc.butin(), x + 100, y, or);
                t(g, "Troupes : " + fc.unites() + " / " + fc.max(), x, y + 12, parch);
                t(g, "Force au camp : " + fc.force(), x + 100, y + 12, parch);
                if (fc.proprio()) {
                    titre(g, "ORDRES", x, y + 30, 184);
                    int qx = px + 206;
                    EcranSerment.cadre(g, qx, py + 30, 184, PH - 38, 0xFF181E34);
                    g.centeredText(this.font, "RECRUTEMENT", qx + 92, py + 36, EcranSerment.OR_CLAIR);
                    for (int i = 0; i < Math.min(8, fc.recrues().size()); i++) {
                        int ry = py + 48 + i * 24;
                        boolean ouvert = i < fc.debloquees();
                        g.fill(qx + 6, ry - 2, qx + 178, ry + 20, ouvert ? 0x40D4A63A : 0x40000000);
                        g.text(this.font, Component.translatable("entity.royaumes." + fc.recrues().get(i)), qx + 10, ry + 1,
                                ouvert ? 0xFFF0E6D2 : 0xFF707070, true);
                        g.text(this.font, ouvert ? fc.couts().get(i) + " butin" : "Camp niveau " + niveauRequis(i), qx + 10, ry + 11,
                                ouvert ? or : 0xFF707070, false);
                    }
                } else {
                    g.textWithWordWrap(this.font, Component.literal("Tu es l'invité de ce camp : ses troupes te sont neutres. Tu peux y offrir du butin."),
                            x, y + 30, 184, parch, false);
                }
            }
            case 1 -> {
                for (int b = 0; b < BATS.length; b++) {
                    int ry = py + 36 + b * 40;
                    int n = fc.batiments()[b];
                    g.fill(px + 10, ry - 2, px + PW - 10, ry + 34, n > 0 ? 0x30D4A63A : 0x30000000);
                    t(g, BATS[b] + "  ·  niveau " + n + " / 3", px + 16, ry + 1, n > 0 ? EcranSerment.OR_CLAIR : parch);
                    t(g, effet(b, n), px + 16, ry + 12, n > 0 ? 0xFFC8E6BE : gris);
                    if (n < 3) {
                        t(g, "Suivant : " + effet(b, n + 1) + (fc.niveau() < CAMP_REQUIS[n + 1] ? " (camp niv. " + CAMP_REQUIS[n + 1] + ")" : ""),
                                px + 16, ry + 22, gris);
                    }
                }
            }
            case 2 -> {
                titre(g, "EXPLORATION", x, y, PW - 24);
                g.textWithWordWrap(this.font, Component.literal("Tes éclaireurs parcourent les Royaumes pendant 3 minutes. Ils rapportent "
                        + "des ressources et peuvent repérer les camps d'autres héros, que tu pourras ensuite attaquer depuis l'onglet Raids. "
                        + "Plus ils sont nombreux, et plus ta tour de guet est haute, plus ils trouvent."), x, y + 14, PW - 24, parch, false);
                t(g, "Force au camp : " + fc.force() + "   ·   Tour de guet : niveau " + fc.tour() + " (+" + 15 * fc.tour() + " %)", x, y + 64, or);
                if (fc.explReste() >= 0) {
                    t(g, fc.explNb() + " éclaireur(s) en route", x + 196, y + 82, 0xFF80D0FF);
                    t(g, "retour dans " + fc.explReste() / 60 + ":" + String.format("%02d", fc.explReste() % 60), x + 196, y + 94, 0xFF80D0FF);
                }
                t(g, "Camps ennemis repérés : " + fc.cibles().size(), x + 196, y + 110, parch);
            }
            case 3 -> {
                titre(g, "RAIDS DE CONQUÊTE", x, y, 184);
                titre(g, "CAMPS ENNEMIS REPÉRÉS", px + 206, y, 182);
                if (fc.raidReste() >= 0) {
                    String r = (fc.raidType() == 3 ? "Raid sur " + fc.raidCible() : RAIDS[Math.max(0, Math.min(2, fc.raidType()))])
                            + " — retour dans " + fc.raidReste() / 60 + ":" + String.format("%02d", fc.raidReste() % 60);
                    t(g, r, x, y + 86, 0xFFFFC060);
                }
                t(g, "Force au camp : " + fc.force(), x, y + 100, parch);
                if (fc.cibles().isEmpty()) {
                    g.textWithWordWrap(this.font, Component.literal("Aucun camp repéré : envoie des éclaireurs (onglet Exploration)."),
                            px + 210, y + 16, 176, gris, false);
                }
                for (int i = 0; i < Math.min(5, fc.cibles().size()); i++) {
                    int ry = py + 54 + i * 30;
                    int def = i < fc.ciblesDef().size() ? fc.ciblesDef().get(i) : 0;
                    int ch = fc.force() <= 0 ? 0 : 100 * fc.force() / (fc.force() + Math.max(1, def));
                    g.fill(px + 206, ry - 2, px + 390, ry + 24, 0x40962820);
                    t(g, fc.cibles().get(i), px + 210, ry + 1, 0xFFF0E6D2);
                    t(g, "défense ~" + def + " · " + ch + " %", px + 210, ry + 12, gris);
                }
            }
            case 4 -> {
                titre(g, "ALLIÉS DU CAMP", x, y, 184);
                titre(g, "HÉROS À PROXIMITÉ", px + 206, y, 182);
                if (fc.invites().isEmpty()) {
                    t(g, "Aucun allié.", x, y + 20, gris);
                }
                for (int i = 0; i < Math.min(5, fc.invites().size()); i++) {
                    t(g, fc.invites().get(i), x, py + 57 + i * 24, 0xFF9EE69A);
                }
                if (fc.proches().isEmpty()) {
                    t(g, "Personne à moins de 24 blocs.", px + 206, y + 20, gris);
                }
                for (int i = 0; i < Math.min(5, fc.proches().size()); i++) {
                    t(g, fc.proches().get(i), px + 206, py + 57 + i * 24, 0xFFF0E6D2);
                }
                g.textWithWordWrap(this.font, Component.literal("Un allié, de n'importe quelle faction, est épargné par tes troupes, "
                        + "peut ouvrir ton étendard et offrir du butin. Il ne peut pas être la cible de tes raids."), x, py + PH - 46, PW - 24, gris, false);
            }
            default -> {
            }
        }
    }

    /** Bouton aux ornements d'or, texte et état calculés à chaque image ; rangé dans un onglet (-1 = toujours). */
    static class BoutonAoS extends AbstractButton {
        final int onglet;
        final BooleanSupplier visibleSi;
        private final Supplier<Component> texte;
        private final Runnable action;
        private final BooleanSupplier actif;
        private final BooleanSupplier choisi;

        BoutonAoS(int onglet, int x, int y, int w, int h, Supplier<Component> texte, Runnable action, BooleanSupplier actif,
                  BooleanSupplier choisi, BooleanSupplier visibleSi) {
            super(x, y, w, h, Component.empty());
            this.onglet = onglet;
            this.texte = texte;
            this.action = action;
            this.actif = actif;
            this.choisi = choisi;
            this.visibleSi = visibleSi;
        }

        @Override
        public void onPress(InputWithModifiers entree) {
            if (actif.getAsBoolean()) {
                action.run();
            }
        }

        @Override
        protected void extractContents(GuiGraphicsExtractor g, int sx, int sy, float partiel) {
            this.active = actif.getAsBoolean();
            boolean c = choisi.getAsBoolean();
            int u = c || (this.active && this.isHovered()) ? 128 : 64;
            g.blit(RenderPipelines.GUI_TEXTURED, EcranSerment.ORNEMENTS, getX(), getY(), u, 0, getWidth(), getHeight(), 64, 20, 256, 64);
            g.centeredText(Minecraft.getInstance().font, texte.get(), getX() + getWidth() / 2, getY() + (getHeight() - 8) / 2,
                    this.active || c ? EcranSerment.OR_CLAIR : 0xFF8C8C8C);
            if (!this.active && !c) {
                g.fill(getX() + 2, getY() + 2, getX() + getWidth() - 2, getY() + getHeight() - 2, 0x55000000);
            }
        }

        @Override
        protected void updateWidgetNarration(NarrationElementOutput sortie) {
            this.defaultButtonNarrationText(sortie);
        }
    }
}
