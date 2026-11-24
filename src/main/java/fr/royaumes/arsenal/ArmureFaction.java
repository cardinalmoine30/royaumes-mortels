package fr.royaumes.arsenal;

import fr.royaumes.ArsenalGenere;
import fr.royaumes.FactionsGenerees;
import java.util.function.Consumer;
import net.minecraft.ChatFormatting;
import net.minecraft.network.chat.Component;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.TooltipFlag;
import net.minecraft.world.item.component.TooltipDisplay;

/** Pièce d'armure de faction : la panoplie complète donne des effets permanents. */
public class ArmureFaction extends Item {
    private final int faction;

    public ArmureFaction(Item.Properties p, int faction) {
        super(p);
        this.faction = faction;
    }

    public int faction() {
        return faction;
    }

    @Override
    public void appendHoverText(ItemStack pile, Item.TooltipContext contexte, TooltipDisplay affichage,
                                Consumer<Component> ajout, TooltipFlag options) {
        ajout.accept(Component.literal(FactionsGenerees.NOMS[faction]).withColor(FactionsGenerees.COULEURS[faction]));
        ajout.accept(Component.literal("Panoplie complète : " + ArsenalGenere.BONUS[faction].replace(",", ", ")).withStyle(ChatFormatting.GREEN));
    }
}
