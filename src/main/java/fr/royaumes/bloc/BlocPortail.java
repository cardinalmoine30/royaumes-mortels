package fr.royaumes.bloc;

import net.minecraft.ChatFormatting;
import net.minecraft.core.BlockPos;
import net.minecraft.core.particles.ParticleTypes;
import net.minecraft.network.chat.Component;
import net.minecraft.server.MinecraftServer;
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

/** Portail des Royaumes : ouvre le menu de voyage du datapack (choix du Royaume de destination). */
public class BlocPortail extends Block {
    public BlocPortail(Properties proprietes) {
        super(proprietes);
    }

    @Override
    protected InteractionResult useWithoutItem(BlockState etat, Level niveau, BlockPos pos, Player joueur, BlockHitResult impact) {
        if (niveau instanceof ServerLevel serveur && joueur instanceof ServerPlayer sp) {
            serveur.sendParticles(ParticleTypes.REVERSE_PORTAL, pos.getX() + 0.5, pos.getY() + 1.0, pos.getZ() + 0.5, 60, 0.5, 0.8, 0.5, 0.1);
            serveur.playSound(null, pos, SoundEvents.ENDERMAN_TELEPORT, SoundSource.BLOCKS, 0.6F, 0.7F);
            sp.sendOverlayMessage(Component.translatable("royaumes.portail.info").withStyle(ChatFormatting.LIGHT_PURPLE));
            // même menu que les failles du datapack, sans la poussée vers la faille la plus proche
            executer(sp, "scoreboard players enable @s rm_voyage");
            executer(sp, "scoreboard players set @s rm_voyage 0");
            executer(sp, "dialog show @s royaumes:voyage");
        }
        return InteractionResult.SUCCESS;
    }

    /** Exécute une fonction du datapack « en tant que » joueur, avec les droits du serveur. */
    public static void executer(ServerPlayer sp, String commande) {
        MinecraftServer serveur = sp.level().getServer();
        if (serveur == null) {
            return;
        }
        serveur.getCommands().performPrefixedCommand(serveur.createCommandSourceStack()
                .withEntity(sp).withPosition(sp.position()).withSuppressedOutput(), commande);
    }
}
