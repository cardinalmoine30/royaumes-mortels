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
    private final int palier;

    public ArmureFaction(Item.Properties p, int faction, int palier) {
        super(p);
        this.faction = faction;
        this.palier = palier;
    }

    static String romain(int n) {
        return new String[] {"", "I", "II", "III", "IV", "V"}[Math.max(0, Math.min(5, n))];
    }

    public int palier() {
        return palier;
    }

    public int faction() {
        return faction;
    }

    @Override
    public void appendHoverText(ItemStack pile, Item.TooltipContext contexte, TooltipDisplay affichage,
                                Consumer<Component> ajout, TooltipFlag options) {
        ajout.accept(Component.literal(FactionsGenerees.NOMS[faction]).withColor(FactionsGenerees.COULEURS[faction]));
        ajout.accept(Component.literal("Palier " + ArsenalGenere.NOMS_PALIERS[palier]).withStyle(ChatFormatting.GOLD));
        StringBuilder b = new StringBuilder();
        for (var e : Arsenal.effetsPanoplie(faction, palier).entrySet()) {
            b.append(b.length() > 0 ? ", " : "").append(OutilAlliance.Infos.nomEffet(e.getKey())).append(" ").append(romain(e.getValue() + 1));
        }
        ajout.accept(Component.literal("Panoplie complète : " + b).withStyle(ChatFormatting.GREEN));
    }
}
