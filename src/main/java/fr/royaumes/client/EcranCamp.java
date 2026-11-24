package fr.royaumes.client;

import fr.royaumes.reseau.ActionCamp;
import fr.royaumes.reseau.DonneesHeros;
import fr.royaumes.reseau.FicheCamp;
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

/** Écran du camp de guerre : butin, troupes, ordres, amélioration, raids et recrutement. */
public class EcranCamp extends Screen {
    private static final int PW = 400;
    private static final int PH = 240;
    private static final String[] RAIDS = {"Pillage", "Assaut", "Croisade"};
    private static final int[] DUREE = {2, 5, 10};
    private static final int[] DIFF = {15, 40, 90};
    private static final int[] DEBLOQUEES = {0, 2, 3, 5, 6, 8};
    private int px;
    private int py;

    public EcranCamp() {
        super(Component.literal("Camp de guerre"));
    }

    static int niveauRequis(int i) {
        for (int n = 1; n < DEBLOQUEES.length; n++) {
            if (DEBLOQUEES[n] > i) {
                return n;
            }
        }
        return 5;
    }

    static FicheCamp f() {
        return DonneesHeros.camp;
    }

    static void envoyer(int action, int arg) {
        ClientPacketListener c = Minecraft.getInstance().getConnection();
        if (c != null) {
            try {
                c.send(new ServerboundCustomPayloadPacket(new ActionCamp(action, arg)));
            } catch (RuntimeException e) {
                // serveur sans le mod
            }
        }
    }

    private boolean enRaid() {
        return f() != null && f().raidReste() >= 0;
    }

    @Override
    protected void init() {
        px = (this.width - PW) / 2;
        py = (this.height - PH) / 2;
        int x = px + 12;
        addRenderableWidget(new BoutonAoS(x, py + 66, 90, 18, () -> Component.literal("Garder le camp"), () -> envoyer(4, 0),
                () -> true, () -> f() != null && f().ordre() == 0));
        addRenderableWidget(new BoutonAoS(x + 94, py + 66, 90, 18, () -> Component.literal("Me suivre"), () -> envoyer(4, 1),
                () -> true, () -> f() != null && f().ordre() == 1));
        addRenderableWidget(new BoutonAoS(x, py + 90, 184, 18, () -> Component.literal("Déposer le butin"), () -> envoyer(3, 0),
                () -> true, () -> false));
        addRenderableWidget(new BoutonAoS(x, py + 112, 184, 18,
                () -> Component.literal(f() == null || f().coutNiveau() == 0 ? "Niveau maximum" : "Améliorer le camp — " + f().coutNiveau() + " butin"),
                () -> envoyer(2, 0), () -> f() != null && f().coutNiveau() > 0 && f().butin() >= f().coutNiveau(), () -> false));
        for (int k = 0; k < 3; k++) {
            final int t = k;
            addRenderableWidget(new BoutonAoS(x, py + 154 + k * 22, 184, 18, () -> {
                int force = f() == null ? 0 : f().force();
                int chance = force <= 0 ? 0 : 100 * force / (force + DIFF[t]);
                return Component.literal(RAIDS[t] + " · " + DUREE[t] + " min · réussite " + chance + " %");
            }, () -> envoyer(5, t), () -> !enRaid() && f() != null && f().force() > 0, () -> false));
        }
        FicheCamp fc = f();
        int n = fc == null ? 0 : Math.min(8, fc.recrues().size());
        for (int i = 0; i < n; i++) {
            final int k = i;
            addRenderableWidget(new BoutonAoS(px + 330, py + 36 + i * 24, 52, 18, () -> Component.literal("Recruter"), () -> envoyer(1, k),
                    () -> f() != null && k < f().debloquees() && k < f().couts().size() && f().butin() >= f().couts().get(k) && f().unites() < f().max(),
                    () -> false));
        }
    }

    @Override
    public boolean isPauseScreen() {
        return false;
    }

    @Override
    public void extractBackground(GuiGraphicsExtractor g, int sx, int sy, float partiel) {
        g.fillGradient(0, 0, this.width, this.height, 0xE0162648, 0xF0060A16);
        EcranSerment.cadre(g, px, py, PW, PH, 0xEB0C1428);
        EcranSerment.coins(g, px, py, PW, PH);
        g.blit(RenderPipelines.GUI_TEXTURED, EcranSerment.ORNEMENTS, px + PW / 2 - 80, py - 10, 0, 24, 160, 24, 256, 64);
        g.centeredText(this.font, "CAMP DE GUERRE", px + PW / 2, py - 2, EcranSerment.OR_CLAIR);
        FicheCamp fc = f();
        if (fc == null) {
            return;
        }
        int x = px + 12;
        g.text(this.font, "Niveau " + fc.niveau() + " / 5", x, py + 20, EcranSerment.OR_CLAIR, true);
        g.text(this.font, "Butin : " + fc.butin(), x + 100, py + 20, 0xFFF2D27A, true);
        g.text(this.font, "Troupes : " + fc.unites() + " / " + fc.max(), x, py + 32, 0xFFE6D3A8, true);
        g.text(this.font, "Force au camp : " + fc.force(), x + 100, py + 32, 0xFFE6D3A8, true);
        g.text(this.font, "ORDRES", x, py + 54, EcranSerment.OR, true);
        g.fill(x, py + 63, x + 184, py + 64, EcranSerment.OR);
        g.text(this.font, "RAIDS", x, py + 136, EcranSerment.OR, true);
        g.fill(x, py + 145, x + 184, py + 146, EcranSerment.OR);
        if (fc.raidReste() >= 0) {
            String r = (fc.raidType() >= 0 && fc.raidType() < 3 ? RAIDS[fc.raidType()] : "Raid") + " en cours — retour dans "
                    + fc.raidReste() / 60 + ":" + String.format("%02d", fc.raidReste() % 60);
            g.text(this.font, r, x + 40, py + 136, 0xFFFFC060, true);
        }
        // recrutement
        int qx = px + 206;
        EcranSerment.cadre(g, qx, py + 14, 184, PH - 22, 0xFF181E34);
        g.centeredText(this.font, "RECRUTEMENT", qx + 92, py + 21, EcranSerment.OR_CLAIR);
        for (int i = 0; i < Math.min(8, fc.recrues().size()); i++) {
            int y = py + 36 + i * 24;
            boolean ouvert = i < fc.debloquees();
            g.fill(qx + 6, y - 2, qx + 178, y + 20, ouvert ? 0x40D4A63A : 0x40000000);
            Component nom = Component.translatable("entity.royaumes." + fc.recrues().get(i));
            g.text(this.font, nom, qx + 10, y + 1, ouvert ? 0xFFF0E6D2 : 0xFF707070, true);
            g.text(this.font, ouvert ? fc.couts().get(i) + " butin" : "Camp niveau " + niveauRequis(i), qx + 10, y + 11,
                    ouvert ? 0xFFF2D27A : 0xFF707070, false);
        }
    }

    /** Bouton aux ornements d'or, texte et état calculés à chaque image. */
    static class BoutonAoS extends AbstractButton {
        private final Supplier<Component> texte;
        private final Runnable action;
        private final BooleanSupplier actif;
        private final BooleanSupplier choisi;

        BoutonAoS(int x, int y, int w, int h, Supplier<Component> texte, Runnable action, BooleanSupplier actif, BooleanSupplier choisi) {
            super(x, y, w, h, texte.get());
            this.texte = texte;
            this.action = action;
            this.actif = actif;
            this.choisi = choisi;
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
