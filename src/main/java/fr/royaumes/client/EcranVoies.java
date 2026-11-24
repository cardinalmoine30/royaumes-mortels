package fr.royaumes.client;

import fr.royaumes.reseau.DonneesHeros;
import fr.royaumes.reseau.FicheHeros;
import fr.royaumes.rpg.Voies;
import java.util.ArrayList;
import java.util.List;
import net.minecraft.client.gui.GuiGraphicsExtractor;
import net.minecraft.client.gui.screens.Screen;
import net.minecraft.client.renderer.RenderPipelines;
import net.minecraft.network.chat.Component;

/** Voie du héros (touche K) : choix de la voie au niveau 5, puis un talent parmi deux aux niveaux 10, 20, 30 et 40. */
public class EcranVoies extends Screen {
    private static final int PW = 440;
    private static final int PH = 268;
    private static final int[] COULEURS = {0xFFE6D3A8, 0xFFE05A46, 0xFF8C7CFF, 0xFF6EDC8C};
    private int px;
    private int py;
    private final List<EcranCamp.BoutonAoS> choixVoie = new ArrayList<>();
    private final List<EcranCamp.BoutonAoS> talents = new ArrayList<>();

    public EcranVoies() {
        super(Component.literal("Voie du héros"));
    }

    static int[] donnees() {
        FicheHeros f = DonneesHeros.actuelle;
        int[] r = {1, 0, 0};
        if (f != null) {
            r[0] = f.niveau();
            if (f.progres() != null && f.progres().length > 5) {
                r[1] = f.progres()[4];
                r[2] = f.progres()[5];
            }
        }
        return r;
    }

    @Override
    protected void init() {
        px = (this.width - PW) / 2;
        py = (this.height - PH) / 2;
        for (int v = 1; v <= 3; v++) {
            final int vv = v;
            choixVoie.add(addRenderableWidget(new EcranCamp.BoutonAoS(-1, px + 14 + (v - 1) * 140 + 25, py + PH - 40, 86, 18,
                    () -> Component.literal("Choisir"), () -> EcranCamp.envoyer(30, vv, ""),
                    () -> donnees()[0] >= Voies.NIVEAU_VOIE, () -> false, () -> true)));
        }
        for (int t = 0; t < 4; t++) {
            for (int c = 0; c < 2; c++) {
                final int palier = t;
                final int ch = c;
                talents.add(addRenderableWidget(new EcranCamp.BoutonAoS(-1, px + 64 + c * 186, py + 50 + t * 48, 180, 18,
                        () -> {
                            int v = donnees()[1];
                            return Component.literal(v > 0 ? Voies.TALENTS[v][palier][ch][0] : "");
                        },
                        () -> EcranCamp.envoyer(31, palier * 2 + ch, ""),
                        () -> donnees()[0] >= Voies.NIVEAUX[palier] && Voies.choix(donnees()[2], palier) == 0,
                        () -> Voies.choix(donnees()[2], palier) == ch + 1, () -> true)));
            }
        }
        talents.add(addRenderableWidget(new EcranCamp.BoutonAoS(-1, px + PW - 176, py + PH - 26, 164, 18,
                () -> Component.literal("Oublier ma voie (3 diamants)"), () -> EcranCamp.envoyer(32, 0, ""),
                () -> true, () -> false, () -> true)));
    }

    @Override
    public void extractRenderState(GuiGraphicsExtractor g, int sx, int sy, float partiel) {
        boolean sansVoie = donnees()[1] == 0;
        choixVoie.forEach(b -> b.visible = sansVoie);
        talents.forEach(b -> b.visible = !sansVoie);
        super.extractRenderState(g, sx, sy, partiel);
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
        g.blit(RenderPipelines.GUI_TEXTURED, EcranSerment.ORNEMENTS, px + PW / 2 - 80, py - 12, 0, 24, 160, 24, 256, 64);
        g.centeredText(this.font, "VOIE DU HÉROS", px + PW / 2, py - 4, EcranSerment.OR_CLAIR);
        int[] d = donnees();
        if (d[1] == 0) {
            g.centeredText(this.font, d[0] >= Voies.NIVEAU_VOIE ? "Choisis ta voie. Elle s'ajoute à ta faction et à tes compétences."
                    : "Ta voie s'ouvre au niveau " + Voies.NIVEAU_VOIE + " (tu es niveau " + d[0] + ").", px + PW / 2, py + 18,
                    d[0] >= Voies.NIVEAU_VOIE ? 0xFFE6D3A8 : 0xFFFF6B6B);
            for (int v = 1; v <= 3; v++) {
                int x = px + 14 + (v - 1) * 140;
                EcranSerment.cadre(g, x, py + 36, 132, PH - 84, 0xFF181E34);
                g.centeredText(this.font, Voies.NOMS[v].toUpperCase(), x + 66, py + 46, COULEURS[v]);
                g.fill(x + 16, py + 57, x + 116, py + 58, COULEURS[v]);
                g.textWithWordWrap(this.font, Component.literal(Voies.DESCRIPTIONS[v]), x + 8, py + 66, 116, 0xFFE6D3A8);
            }
            return;
        }
        g.centeredText(this.font, "Voie du " + Voies.NOMS[d[1]], px + PW / 2, py + 18, COULEURS[d[1]]);
        g.centeredText(this.font, "Un talent parmi deux à chaque palier. Niveau actuel : " + d[0], px + PW / 2, py + 32, 0xFF9AA0B8);
        for (int t = 0; t < 4; t++) {
            int y = py + 50 + t * 48;
            boolean ouvert = d[0] >= Voies.NIVEAUX[t];
            g.text(this.font, "Niv. " + Voies.NIVEAUX[t], px + 14, y + 5, ouvert ? EcranSerment.OR_CLAIR : 0xFF8C8C8C, true);
            for (int c = 0; c < 2; c++) {
                g.textWithWordWrap(this.font, Component.literal(Voies.TALENTS[d[1]][t][c][1]), px + 66 + c * 186, y + 21, 176,
                        Voies.choix(d[2], t) == c + 1 ? 0xFF9EE69A : 0xFFB4AA96);
            }
        }
    }
}
