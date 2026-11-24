package fr.royaumes.bloc;

import fr.royaumes.camp.Camps;
import net.minecraft.core.BlockPos;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.world.InteractionResult;
import net.minecraft.world.entity.LivingEntity;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.level.BlockGetter;
import net.minecraft.world.level.Level;
import net.minecraft.world.level.block.Block;
import net.minecraft.world.level.block.state.BlockState;
import net.minecraft.world.phys.BlockHitResult;
import net.minecraft.world.phys.shapes.CollisionContext;
import net.minecraft.world.phys.shapes.VoxelShape;

/** Étendard de camp : le poser fonde (ou déplace) le camp de guerre du joueur ; clic droit = écran du camp. */
public class BlocEtendard extends Block {
    private static final VoxelShape FORME = Block.box(4, 0, 4, 12, 16, 12);

    public BlocEtendard(Properties proprietes) {
        super(proprietes);
    }

    @Override
    protected VoxelShape getShape(BlockState etat, BlockGetter monde, BlockPos pos, CollisionContext contexte) {
        return FORME;
    }

    @Override
    public void setPlacedBy(Level niveau, BlockPos pos, BlockState etat, LivingEntity poseur, ItemStack pile) {
        super.setPlacedBy(niveau, pos, etat, poseur, pile);
        if (!niveau.isClientSide() && poseur instanceof ServerPlayer sp) {
            Camps.fonder(sp, pos);
        }
    }

    @Override
    protected InteractionResult useWithoutItem(BlockState etat, Level niveau, BlockPos pos, Player joueur, BlockHitResult impact) {
        if (joueur instanceof ServerPlayer sp) {
            Camps.ouvrir(sp, pos);
        }
        return InteractionResult.SUCCESS;
    }
}
