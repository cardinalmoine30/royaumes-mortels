package fr.royaumes.client;

import net.minecraft.client.gui.GuiGraphicsExtractor;
import net.minecraft.client.gui.screens.inventory.ContainerScreen;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.network.chat.Component;
import net.minecraft.resources.Identifier;
import net.minecraft.world.entity.player.Inventory;
import net.minecraft.world.inventory.ChestMenu;
import net.minecraft.world.item.ItemStack;

/** Stockage du camp : coffre de 6 rangées, la dernière (dorée) est le tribut qui change les minerais en butin. */
public class EcranStockage extends ContainerScreen {
    private static final String[][] BAREME = {
            {"minecraft:raw_iron", "1"}, {"minecraft:raw_copper", "1"}, {"minecraft:coal", "1"}, {"minecraft:redstone", "1"},
            {"minecraft:lapis_lazuli", "1"}, {"minecraft:raw_gold", "3"}, {"minecraft:gold_ingot", "4"}, {"minecraft:emerald", "6"},
            {"minecraft:diamond", "12"}, {"minecraft:ancient_debris", "30"}, {"minecraft:netherite_ingot", "40"}};

    public EcranStockage(ChestMenu menu, Inventory inv, Component titre) {
        super(menu, inv, titre);
    }

    @Override
    public void extractBackground(GuiGraphicsExtractor g, int sx, int sy, float partiel) {
        super.extractBackground(g, sx, sy, partiel);
        int l = getLeftPos();
        int t = getTopPos();
        // rangée du tribut : liseré et voile dorés
        int y = t + 17 + 5 * 18;
        g.fill(l + 7, y, l + 7 + 9 * 18, y + 18, 0x40D4A63A);
        g.fill(l + 6, y - 1, l + 8 + 9 * 18, y, 0xFFD4A63A);
        g.fill(l + 6, y + 18, l + 8 + 9 * 18, y + 19, 0xFFD4A63A);
        // panneau : à quoi sert la rangée dorée, et le barème
        int px = l + getImageWidth() + 4;
        int largeur = 118;
        if (px + largeur > this.width - 2) {
            px = Math.max(2, l - largeur - 4);
        }
        EcranSerment.cadre(g, px, t, largeur, 46 + BAREME.length * 12, 0xE80C1428);
        g.text(this.font, "Tribut (rangée dorée)", px + 6, t + 5, EcranSerment.OR_CLAIR, true);
        Texte.bloc(g, this.font, "Minerais, lingots, gemmes : changés en butin à la fermeture.", px + 6, t + 16, largeur - 12, 26,
                0xFFE6D3A8, false);
        for (int i = 0; i < BAREME.length; i++) {
            int yy = t + 44 + i * 12;
            var it = BuiltInRegistries.ITEM.getValue(Identifier.parse(BAREME[i][0]));
            g.pose().pushMatrix();
            g.pose().translate(px + 6, yy - 1);
            g.pose().scale(0.625F, 0.625F);
            g.item(new ItemStack(it), 0, 0);
            g.pose().popMatrix();
            Texte.ligne(g, this.font, new ItemStack(it).getHoverName().getString(), px + 18, yy, largeur - 46, 0xFFCFC6B4, false);
            String v = "+" + BAREME[i][1];
            g.text(this.font, v, px + largeur - 6 - this.font.width(v), yy, 0xFFF2D27A, false);
        }
    }
}
