package fr.royaumes.objet;

import fr.royaumes.ContenuGenere;
import fr.royaumes.magie.Magie;
import java.util.function.Consumer;
import net.minecraft.ChatFormatting;
import net.minecraft.network.chat.Component;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.world.InteractionHand;
import net.minecraft.world.InteractionResult;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.TooltipFlag;
import net.minecraft.world.item.component.TooltipDisplay;
import net.minecraft.world.level.Level;

/** Bâton d'un des huit Vents : clic droit = sort mineur, accroupi + clic droit = grand sort. */
public class BatonVent extends Item {
    private final int vent;

    public BatonVent(Item.Properties proprietes, int vent) {
        super(proprietes);
        this.vent = vent;
    }

    public int vent() {
        return vent;
    }

    @Override
    public InteractionResult use(Level niveau, Player joueur, InteractionHand main) {
        ItemStack pile = joueur.getItemInHand(main);
        if (joueur.getCooldowns().isOnCooldown(pile)) {
            return InteractionResult.FAIL;
        }
        if (niveau instanceof ServerLevel serveur && joueur instanceof ServerPlayer sp) {
            int rang = joueur.isShiftKeyDown() ? 1 : 0;
            if (Magie.lancer(sp, serveur, vent, rang)) {
                joueur.getCooldowns().addCooldown(pile, ContenuGenere.SORTS_RECHARGES[vent][rang]);
                joueur.swing(main, true);
            }
        }
        return InteractionResult.SUCCESS;
    }

    @Override
    public void appendHoverText(ItemStack pile, Item.TooltipContext contexte, TooltipDisplay affichage,
                                Consumer<Component> ajout, TooltipFlag options) {
        int c = ContenuGenere.COULEURS_VENTS[vent];
        for (int rang = 0; rang < 2; rang++) {
            ajout.accept(Component.translatable(rang == 0 ? "royaumes.sort.mineur" : "royaumes.sort.majeur",
                    Component.translatable("royaumes.sort." + ContenuGenere.SORTS_IDS[vent][rang]),
                    ContenuGenere.SORTS_COUTS[vent][rang]).withColor(c));
            ajout.accept(Component.literal("  " + ContenuGenere.SORTS_DESC[vent][rang]).withStyle(ChatFormatting.GRAY));
        }
        ajout.accept(Component.translatable("royaumes.sort.royaume", ContenuGenere.NOMS_VENTS[vent]).withStyle(ChatFormatting.DARK_PURPLE));
    }
}
