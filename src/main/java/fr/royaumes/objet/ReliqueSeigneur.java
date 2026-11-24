package fr.royaumes.objet;

import fr.royaumes.magie.Reliques;
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

/** Relique unique d'un seigneur : arme ou sceptre avec un ou deux pouvoirs (clic droit / accroupi). */
public class ReliqueSeigneur extends Item {
    private final String seigneur;
    private final String[] pouvoirs;

    public ReliqueSeigneur(Item.Properties p, String seigneur, String... pouvoirs) {
        super(p);
        this.seigneur = seigneur;
        this.pouvoirs = pouvoirs;
    }

    @Override
    public InteractionResult use(Level niveau, Player joueur, InteractionHand main) {
        ItemStack pile = joueur.getItemInHand(main);
        if (joueur.getCooldowns().isOnCooldown(pile)) {
            return InteractionResult.FAIL;
        }
        if (niveau instanceof ServerLevel sl && joueur instanceof ServerPlayer sp) {
            int recharge = Reliques.utiliser(sp, sl, seigneur, joueur.isShiftKeyDown());
            if (recharge > 0) {
                joueur.getCooldowns().addCooldown(pile, recharge);
            }
        }
        return InteractionResult.SUCCESS;
    }

    @Override
    public boolean isFoil(ItemStack pile) {
        return true;
    }

    @Override
    public void appendHoverText(ItemStack pile, Item.TooltipContext contexte, TooltipDisplay affichage,
                                Consumer<Component> ajout, TooltipFlag options) {
        ajout.accept(Component.literal("Relique unique d'un seigneur des Royaumes · très rare").withStyle(ChatFormatting.DARK_PURPLE, ChatFormatting.ITALIC));
        String passif = switch (seigneur) {
            case "archaon" -> "Tueuse de Rois : dégâts x1,75 contre les seigneurs";
            case "gordrakk" -> "Chaque coup projette la cible";
            case "skarbrand" -> "Chaque coup enflamme ; Force I sous 50 % de vie";
            case "thanquol" -> "Le malefeu flétrit et frappe 50 % plus fort";
            default -> "";
        };
        if (!passif.isEmpty()) {
            ajout.accept(Component.literal(passif).withStyle(ChatFormatting.LIGHT_PURPLE));
        }
        for (int i = 0; i < pouvoirs.length; i++) {
            ajout.accept(Component.literal((i == 0 ? "Clic droit : " : "Accroupi + clic droit : ") + pouvoirs[i]).withStyle(ChatFormatting.GOLD));
        }
    }
}
