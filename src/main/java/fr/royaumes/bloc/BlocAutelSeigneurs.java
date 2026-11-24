package fr.royaumes.bloc;

import net.minecraft.ChatFormatting;
import net.minecraft.core.BlockPos;
import net.minecraft.network.chat.Component;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.world.InteractionHand;
import net.minecraft.world.InteractionResult;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.Items;
import net.minecraft.world.level.Level;
import net.minecraft.world.level.block.Block;
import net.minecraft.world.level.block.state.BlockState;
import net.minecraft.world.phys.BlockHitResult;

/** Autel des Seigneurs, au cœur de chaque antre : on y éveille le sceau d'un seigneur pour l'invoquer. */
public class BlocAutelSeigneurs extends Block {
    static final String[] SEIGNEURS = {"nagash", "archaon", "gordrakk", "skarbrand", "thanquol", "rotigus"};

    public BlocAutelSeigneurs(Properties p) {
        super(p);
    }

    @Override
    protected InteractionResult useItemOn(ItemStack pile, BlockState etat, Level niveau, BlockPos pos, Player joueur, InteractionHand main,
                                          BlockHitResult impact) {
        if (!(joueur instanceof ServerPlayer sp)) {
            return InteractionResult.SUCCESS;
        }
        if (!pile.is(Items.CARROT_ON_A_STICK)) {
            sp.sendOverlayMessage(Component.literal("Autel des Seigneurs : pose ici le sceau d'un seigneur pour l'invoquer.").withStyle(ChatFormatting.GOLD));
            return InteractionResult.SUCCESS;
        }
        for (String s : SEIGNEURS) {
            BlocPortail.executer(sp, "execute if items entity @s weapon.mainhand minecraft:carrot_on_a_stick[minecraft:custom_data~{royaumes:\"sceau_"
                    + s + "\"}] positioned " + pos.getX() + " " + (pos.getY() + 1) + " " + pos.getZ() + " run function royaumes:boss/" + s + "/invoquer");
        }
        return InteractionResult.SUCCESS;
    }

    @Override
    protected InteractionResult useWithoutItem(BlockState etat, Level niveau, BlockPos pos, Player joueur, BlockHitResult impact) {
        if (joueur instanceof ServerPlayer sp) {
            sp.sendOverlayMessage(Component.literal("Autel des Seigneurs : pose ici le sceau d'un seigneur pour l'invoquer.").withStyle(ChatFormatting.GOLD));
        }
        return InteractionResult.SUCCESS;
    }
}
