package fr.royaumes.objet;

import fr.royaumes.ContenuGenere;
import fr.royaumes.magie.Magie;
import java.util.function.Consumer;
import net.minecraft.ChatFormatting;
import net.minecraft.network.chat.Component;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.world.InteractionHand;
import net.minecraft.world.InteractionResult;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.TooltipFlag;
import net.minecraft.world.item.component.TooltipDisplay;
import net.minecraft.world.level.Level;

/** Grimoire des Vents : affiche les seize sorts, leur coût et l'énergie du héros. */
public class GrimoireVents extends Item {
    public GrimoireVents(Item.Properties proprietes) {
        super(proprietes);
    }

    @Override
    public InteractionResult use(Level niveau, Player joueur, InteractionHand main) {
        if (joueur instanceof ServerPlayer sp) {
            sp.sendSystemMessage(Component.literal("✦ Grimoire des Vents ✦").withStyle(ChatFormatting.GOLD, ChatFormatting.BOLD));
            sp.sendSystemMessage(Component.translatable("royaumes.energie").append(" : " + Magie.energie(sp) + " / " + Magie.maximum(sp))
                    .withStyle(ChatFormatting.LIGHT_PURPLE));
            for (int v = 0; v < ContenuGenere.VENTS.length; v++) {
                Component ligne = Component.literal(ContenuGenere.NOMS_VENTS[v] + " — ").withColor(ContenuGenere.COULEURS_VENTS[v])
                        .append(Component.literal(ContenuGenere.SORTS_NOMS[v][0] + " (" + ContenuGenere.SORTS_COUTS[v][0] + "), "
                                + ContenuGenere.SORTS_NOMS[v][1] + " (" + ContenuGenere.SORTS_COUTS[v][1] + ")").withStyle(ChatFormatting.GRAY));
                sp.sendSystemMessage(ligne);
            }
            sp.sendSystemMessage(Component.literal("Sorts à moitié prix dans le Royaume de leur Vent.").withStyle(ChatFormatting.DARK_AQUA));
        }
        return InteractionResult.SUCCESS;
    }

    @Override
    public void appendHoverText(ItemStack pile, Item.TooltipContext contexte, TooltipDisplay affichage,
                                Consumer<Component> ajout, TooltipFlag options) {
        ajout.accept(Component.translatable("royaumes.grimoire.info").withStyle(ChatFormatting.GRAY));
    }
}
