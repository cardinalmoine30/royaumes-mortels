package fr.royaumes.client;

import fr.royaumes.ContenuGenere;
import fr.royaumes.FactionsGenerees;
import fr.royaumes.magie.Magie;
import fr.royaumes.objet.BatonVent;
import fr.royaumes.reseau.DonneesHeros;
import fr.royaumes.reseau.FicheHeros;
import net.minecraft.client.DeltaTracker;
import net.minecraft.client.Minecraft;
import net.minecraft.client.gui.GuiGraphicsExtractor;
import net.minecraft.client.player.LocalPlayer;
import net.minecraft.client.renderer.RenderPipelines;
import net.minecraft.resources.Identifier;
import net.minecraft.world.item.ItemStack;
import net.neoforged.neoforge.client.gui.GuiLayer;

/**
 * HUD des Royaumes : (1) jauge d'énergie arcanique en bas à gauche, (2) blason, faction, niveau et Royaume
 * en haut à gauche, (4) sort prêt et son coût au-dessus de la barre d'objets quand on tient un bâton.
 */
public class HudRoyaumes implements GuiLayer {
    static final Identifier HUD = EcranSerment.aos("hud");

    @Override
    public void render(GuiGraphicsExtractor g, DeltaTracker temps) {
        Minecraft mc = Minecraft.getInstance();
        LocalPlayer joueur = mc.player;
        FicheHeros f = DonneesHeros.actuelle;
        if (joueur == null || f == null || joueur.isSpectator()) {
            return;
        }
        int w = g.guiWidth();
        int h = g.guiHeight();
        int lieu = Magie.ventDuLieu(joueur.level());
        // (2) blason et faction
        if (f.faction() > 0 && f.faction() < FactionsGenerees.NOMS.length) {
            EcranSerment.cadre(g, 4, 4, 26, 26, 0xC80C1428);
            int u = ((f.faction() - 1) % 8) * 32;
            int v = ((f.faction() - 1) / 8) * 32;
            g.blit(RenderPipelines.GUI_TEXTURED, EcranSerment.EMBLEMES, 6, 6, u, v, 22, 22, 32, 32, 256, 128);
            g.text(mc.font, FactionsGenerees.NOMS[f.faction()], 34, 7, EcranSerment.OR_CLAIR, true);
            String ligne = "Niveau " + f.niveau() + (lieu >= 0 ? " · Royaume " + de(ContenuGenere.NOMS_VENTS[lieu]) : "");
            g.text(mc.font, ligne, 34, 18, 0xFFF0E6D2, true);
        }
        // (1) jauge arcanique
        int vent = ventAffiche(joueur, f);
        int gx = 6;
        int gy = h - 22;
        g.blit(RenderPipelines.GUI_TEXTURED, HUD, gx, gy - 2, vent * 16, 32, 16, 16, 256, 64);
        g.blit(RenderPipelines.GUI_TEXTURED, HUD, gx + 18, gy + 2, 0, 0, 104, 12, 256, 64);
        int max = Math.max(1, f.energieMax());
        int plein = Math.max(0, Math.min(100, 100 * f.energie() / max));
        if (plein > 0) {
            g.blit(RenderPipelines.GUI_TEXTURED, HUD, gx + 20, gy + 4, 0, 16, plein, 8, 256, 64);
        }
        g.text(mc.font, f.energie() + " / " + f.energieMax(), gx + 20, gy - 8, 0xFFC8BEFF, true);
        // (4) sort prêt
        ItemStack tenu = joueur.getMainHandItem();
        if (tenu.getItem() instanceof BatonVent baton) {
            int b = baton.vent();
            int rang = joueur.isShiftKeyDown() ? 1 : 0;
            int cout = ContenuGenere.SORTS_COUTS[b][rang];
            if (lieu == b) {
                cout = (cout + 1) / 2;
            }
            String texte = ContenuGenere.SORTS_NOMS[b][rang] + " — " + cout + " énergie";
            int couleur = f.energie() >= cout ? 0xFF000000 | ContenuGenere.COULEURS_VENTS[b] : 0xFFC85A50;
            g.centeredText(mc.font, texte, w / 2, h - 68, couleur);
        }
    }

    private static int ventAffiche(LocalPlayer joueur, FicheHeros f) {
        if (joueur.getMainHandItem().getItem() instanceof BatonVent b) {
            return b.vent();
        }
        if (f.faction() > 0 && f.faction() < ContenuGenere.VENT_FACTION.length) {
            return ContenuGenere.VENT_FACTION[f.faction()];
        }
        return 0;
    }

    static String de(String nom) {
        return ("AEIOUHaeiouh".indexOf(nom.charAt(0)) >= 0 ? "d'" : "de ") + nom;
    }
}
