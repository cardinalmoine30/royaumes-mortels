package fr.royaumes.bloc;

import fr.royaumes.magie.Magie;
import java.util.HashMap;
import java.util.Map;
import java.util.UUID;
import net.minecraft.ChatFormatting;
import net.minecraft.core.BlockPos;
import net.minecraft.core.particles.ParticleTypes;
import net.minecraft.network.chat.Component;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.sounds.SoundSource;
import net.minecraft.world.InteractionResult;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.level.Level;
import net.minecraft.world.level.block.Block;
import net.minecraft.world.level.block.state.BlockState;
import net.minecraft.world.phys.BlockHitResult;

/** Autel arcanique : recharge entièrement l'énergie arcanique (une fois par minute et par joueur). */
public class BlocAutel extends Block {
    private static final Map<UUID, Long> DERNIER = new HashMap<>();

    public BlocAutel(Properties proprietes) {
        super(proprietes);
    }

    @Override
    protected InteractionResult useWithoutItem(BlockState etat, Level niveau, BlockPos pos, Player joueur, BlockHitResult impact) {
        if (niveau instanceof ServerLevel serveur && joueur instanceof ServerPlayer sp) {
            long maintenant = serveur.getGameTime();
            long reste = DERNIER.getOrDefault(sp.getUUID(), -10000L) + 1200 - maintenant;
            if (reste > 0) {
                sp.sendOverlayMessage(Component.translatable("royaumes.autel.attente", reste / 20 + 1).withStyle(ChatFormatting.GRAY));
                return InteractionResult.CONSUME;
            }
            DERNIER.put(sp.getUUID(), maintenant);
            Magie.ajouter(sp, Magie.maximum(sp));
            serveur.sendParticles(ParticleTypes.ENCHANT, pos.getX() + 0.5, pos.getY() + 1.5, pos.getZ() + 0.5, 80, 0.6, 0.8, 0.6, 1.0);
            serveur.sendParticles(ParticleTypes.END_ROD, sp.getX(), sp.getY() + 1, sp.getZ(), 20, 0.3, 0.6, 0.3, 0.05);
            serveur.playSound(null, pos, SoundEvents.BEACON_ACTIVATE, SoundSource.BLOCKS, 1.0F, 1.3F);
            sp.sendOverlayMessage(Component.translatable("royaumes.autel.info").withStyle(ChatFormatting.LIGHT_PURPLE));
        }
        return InteractionResult.SUCCESS;
    }
}
