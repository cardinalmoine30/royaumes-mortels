package fr.royaumes.objet;

import fr.royaumes.magie.Magie;
import java.util.function.Consumer;
import net.minecraft.ChatFormatting;
import net.minecraft.core.particles.ParticleTypes;
import net.minecraft.network.chat.Component;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.sounds.SoundSource;
import net.minecraft.world.InteractionHand;
import net.minecraft.world.InteractionResult;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.TooltipFlag;
import net.minecraft.world.item.component.TooltipDisplay;
import net.minecraft.world.level.Level;

/** Cristal arcanique : rend 40 points d'énergie arcanique. */
public class CristalArcanique extends Item {
    public CristalArcanique(Item.Properties proprietes) {
        super(proprietes);
    }

    @Override
    public InteractionResult use(Level niveau, Player joueur, InteractionHand main) {
        ItemStack pile = joueur.getItemInHand(main);
        if (niveau instanceof ServerLevel serveur && joueur instanceof ServerPlayer sp) {
            if (Magie.energie(sp) >= Magie.maximum(sp)) {
                return InteractionResult.FAIL;
            }
            Magie.ajouter(sp, 40);
            serveur.sendParticles(ParticleTypes.ENCHANT, sp.getX(), sp.getY() + 1.2, sp.getZ(), 40, 0.4, 0.6, 0.4, 0.8);
            serveur.playSound(null, sp.getX(), sp.getY(), sp.getZ(), SoundEvents.AMETHYST_BLOCK_CHIME, SoundSource.PLAYERS, 1.0F, 1.4F);
            if (!sp.isCreative()) {
                pile.shrink(1);
            }
            sp.getCooldowns().addCooldown(pile, 20);
        }
        return InteractionResult.SUCCESS;
    }

    @Override
    public void appendHoverText(ItemStack pile, Item.TooltipContext contexte, TooltipDisplay affichage,
                                Consumer<Component> ajout, TooltipFlag options) {
        ajout.accept(Component.translatable("royaumes.cristal.info").withStyle(ChatFormatting.AQUA));
    }
}
