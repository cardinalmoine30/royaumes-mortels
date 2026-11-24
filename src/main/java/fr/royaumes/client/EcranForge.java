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
    private static final int PW = 380;
    private static final int PH = 236;
    private int px;
    private int py;

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
        for (int k = 0; k < 6; k++) {
            final int i = k;
            addRenderableWidget(new EcranCamp.BoutonAoS(-1, px + PW - 76, py + 40 + k * 31, 64, 18, () -> Component.literal("Forger"),
                    () -> EcranCamp.envoyer(20, i, ""), () -> possible(i), () -> false, () -> true));
        }
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
        g.text(this.font, "Arsenal : " + FactionsGenerees.NOMS[fa], px + 12, py + 20, 0xFF000000 | FactionsGenerees.COULEURS[fa], true);
        g.text(this.font, ArsenalGenere.TEXTES_ATOUTS[fa], px + 160, py + 20, 0xFFF2D27A, true);
        for (int k = 0; k < 6; k++) {
            int y = py + 36 + k * 31;
            g.fill(px + 8, y, px + PW - 8, y + 28, k < 2 ? 0x55402810 : 0x40202838);
            Item obj = item("royaumes:" + ArsenalGenere.IDS[fa][k]);
            g.item(new ItemStack(obj), px + 12, y + 6);
            String type = ArsenalGenere.TYPES[fa][k];
            String sous = type.endsWith(":c") ? "Champion · très puissante" : type.endsWith(":l") ? "Lignée · atout à chaque coup" : "Armure · " + type;
            g.text(this.font, ArsenalGenere.NOMS[fa][k], px + 32, y + 4, k == 0 ? 0xFFFFAA00 : 0xFFE6D3A8, true);
            g.text(this.font, sous, px + 32, y + 16, 0xFF9AA0B8, false);
            int x = px + 176;
            for (String ing : ArsenalGenere.RECETTES[fa][k].split(",")) {
                String[] a = ing.split("\\*");
                Item it = item(a[0]);
                int n = Integer.parseInt(a[1]);
                g.item(new ItemStack(it), x, y + 2);
                g.text(this.font, "" + n, x + 10, y + 16, compte(it) >= n ? 0xFF9EE69A : 0xFFFF6B6B, true);
                x += 26;
            }
        }
        g.centeredText(this.font, "Les éclats viennent de Royaumes étrangers : il faudra voyager ou commercer.", px + PW / 2, py + PH - 12, 0xFF9AA0B8);
    }
}
