package fr.royaumes.bloc;

import fr.royaumes.reseau.OuvrirForge;
import net.minecraft.core.BlockPos;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.world.InteractionResult;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.level.Level;
import net.minecraft.world.level.block.Block;
import net.minecraft.world.level.block.state.BlockState;
import net.minecraft.world.phys.BlockHitResult;
import net.neoforged.neoforge.network.PacketDistributor;

/** Forge de guerre : ouvre l'écran des recettes de la faction du héros. */
public class BlocForge extends Block {
    public BlocForge(Properties p) {
        super(p);
    }

    @Override
    protected InteractionResult useWithoutItem(BlockState etat, Level niveau, BlockPos pos, Player joueur, BlockHitResult impact) {
        if (joueur instanceof ServerPlayer sp) {
            try {
                PacketDistributor.sendToPlayer(sp, new OuvrirForge(1));
            } catch (RuntimeException e) {
                // client sans le mod
            }
        }
        return InteractionResult.SUCCESS;
    }
}
