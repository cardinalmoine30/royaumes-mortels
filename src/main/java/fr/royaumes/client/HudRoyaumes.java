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
            Texte.ligne(g, mc.font, FactionsGenerees.NOMS[f.faction()], 34, 7, w / 2 - 40, EcranSerment.OR_CLAIR, true);
            int voie = f.progres() != null && f.progres().length > 4 ? f.progres()[4] : 0;
            String ligne = "Niveau " + f.niveau() + (voie > 0 && voie < fr.royaumes.rpg.Voies.NOMS.length ? " · " + fr.royaumes.rpg.Voies.NOMS[voie] : "")
                    + (lieu >= 0 ? " · Royaume " + de(ContenuGenere.NOMS_VENTS[lieu]) : "");
            Texte.ligne(g, mc.font, ligne, 34, 18, w / 2 - 40, 0xFFF0E6D2, true);
            String cap = ContenuGenere.CAP_NOMS[f.faction()] + (f.capacite() > 0 ? " · " + f.capacite() + " s" : " · prête (R)");
            g.text(mc.font, cap, 34, 29, f.capacite() > 0 ? 0xFF8C8CA0 : 0xFFF2D27A, true);
        }
        // (5) Saga du Héros : quête en cours et contrat de chasse
        if (f.quete() != null && f.quete().length >= 3) {
            int qy = f.faction() > 0 ? 44 : 6;
            int[] pr = f.progres();
            String l1 = "✦ " + f.quete()[0] + (pr.length > 1 && pr[1] > 1 ? "  " + pr[0] + "/" + pr[1] : "");
            int max = Math.min(230, w / 2 - 20);
            l1 = coupe(mc, l1, max);
            String l2 = coupe(mc, f.quete()[1], max);
            String l3 = f.quete()[2].isEmpty() ? "" : coupe(mc, "⚔ " + f.quete()[2] + (pr.length > 3 ? "  " + pr[2] + "/" + pr[3] : ""), max);
            int largeur = Math.max(mc.font.width(l1), Math.max(mc.font.width(l2), mc.font.width(l3))) + 8;
            int hauteur = l3.isEmpty() ? 24 : 35;
            g.fill(4, qy, 4 + largeur, qy + hauteur, 0x780C1428);
            g.fill(4, qy, 5, qy + hauteur, 0xFFD4A63A);
            g.text(mc.font, l1, 8, qy + 3, 0xFFF2D27A, true);
            g.text(mc.font, l2, 8, qy + 13, 0xFFCFC6B4, true);
            if (!l3.isEmpty()) {
                g.text(mc.font, l3, 8, qy + 24, 0xFF7FD6E6, true);
            }
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

    static String coupe(Minecraft mc, String s, int max) {
        if (mc.font.width(s) <= max) {
            return s;
        }
        while (s.length() > 3 && mc.font.width(s + "…") > max) {
            s = s.substring(0, s.length() - 1);
        }
        return s + "…";
    }

    static String de(String nom) {
        return ("AEIOUHaeiouh".indexOf(nom.charAt(0)) >= 0 ? "d'" : "de ") + nom;
    }
}
