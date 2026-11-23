package fr.royaumes.client;

import net.minecraft.client.Minecraft;
import net.minecraft.client.gui.GuiGraphicsExtractor;
import net.minecraft.client.gui.components.AbstractButton;
import net.minecraft.client.gui.components.Tooltip;
import net.minecraft.client.gui.narration.NarrationElementOutput;
import net.minecraft.client.input.InputWithModifiers;
import net.minecraft.client.multiplayer.ClientPacketListener;
import net.minecraft.client.renderer.RenderPipelines;
import net.minecraft.network.chat.Component;

/** Onglet de parchemin au-dessus de l'inventaire : ouvre le Codex, la Forge, les Blocs ou la Fiche du héros. */
public class Onglet extends AbstractButton {
    public static final int L = 52;
    public static final int H = 22;
    private final int indice;
    private final String commande;

    public Onglet(int x, int y, int indice, Component nom, Component aide, String commande) {
        super(x, y, L, H, nom);
        this.indice = indice;
        this.commande = commande;
        this.setTooltip(Tooltip.create(aide));
    }

    @Override
    public void onPress(InputWithModifiers entree) {
        ClientPacketListener connexion = Minecraft.getInstance().getConnection();
        if (connexion != null) {
            connexion.sendCommand(commande);
        }
    }

    @Override
    protected void extractContents(GuiGraphicsExtractor g, int sourisX, int sourisY, float partiel) {
        boolean survol = this.isHoveredOrFocused();
        int dy = survol ? -2 : 0;
        g.blit(RenderPipelines.GUI_TEXTURED, EcranTaverne.ONGLETS, getX(), getY() + dy, 0, survol ? 24 : 0, L, 24, 256, 64);
        g.blit(RenderPipelines.GUI_TEXTURED, EcranTaverne.ONGLETS, getX() + 4, getY() + 3 + dy, 64 + indice * 16, 0, 16, 16, 256, 64);
        g.text(Minecraft.getInstance().font, getMessage(), getX() + 21, getY() + 7 + dy, 0xFF3A2414, false);
    }

    @Override
    protected void updateWidgetNarration(NarrationElementOutput sortie) {
        this.defaultButtonNarrationText(sortie);
    }
}
