package fr.royaumes.objet;

import fr.royaumes.RoyaumesMortels;
import java.util.function.Consumer;
import net.minecraft.ChatFormatting;
import net.minecraft.core.BlockPos;
import net.minecraft.core.particles.ParticleTypes;
import net.minecraft.core.registries.Registries;
import net.minecraft.network.chat.Component;
import net.minecraft.resources.Identifier;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.sounds.SoundSource;
import net.minecraft.tags.TagKey;
import net.minecraft.world.InteractionHand;
import net.minecraft.world.InteractionResult;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.TooltipFlag;
import net.minecraft.world.item.component.TooltipDisplay;
import net.minecraft.world.level.Level;
import net.minecraft.world.level.levelgen.structure.Structure;
import net.minecraft.world.phys.Vec3;

/** Œil d'un seigneur : comme l'œil de l'Ender, il montre la direction de l'antre (et de son Autel des Seigneurs). */
public class OeilSeigneur extends Item {
    private final String seigneur;
    private final String nom;
    private final String royaume;

    public OeilSeigneur(Item.Properties p, String seigneur, String nom, String royaume) {
        super(p);
        this.seigneur = seigneur;
        this.nom = nom;
        this.royaume = royaume;
    }

    @Override
    public InteractionResult use(Level niveau, Player joueur, InteractionHand main) {
        ItemStack pile = joueur.getItemInHand(main);
        if (!(niveau instanceof ServerLevel sl) || !(joueur instanceof ServerPlayer sp) || joueur.getCooldowns().isOnCooldown(pile)) {
            return InteractionResult.SUCCESS;
        }
        joueur.getCooldowns().addCooldown(pile, 60);
        TagKey<Structure> antre = TagKey.create(Registries.STRUCTURE, Identifier.fromNamespaceAndPath(RoyaumesMortels.MODID, "antre_" + seigneur));
        BlockPos cible = sl.findNearestMapStructure(antre, sp.blockPosition(), 100, false);
        if (cible == null) {
            sp.sendSystemMessage(Component.literal("L'œil reste aveugle : l'antre de " + nom + " ne se trouve pas dans ce monde. Cherche-le en "
                    + royaume + ".").withStyle(ChatFormatting.GRAY));
            sl.playSound(null, sp.blockPosition(), SoundEvents.ENDER_EYE_DEATH, SoundSource.PLAYERS, 1.0F, 0.6F);
            return InteractionResult.SUCCESS;
        }
        Vec3 o = sp.getEyePosition();
        Vec3 d = new Vec3(cible.getX() + 0.5 - o.x, 0, cible.getZ() + 0.5 - o.z);
        double distance = d.length();
        d = d.normalize();
        for (int i = 1; i <= 24; i++) {
            Vec3 q = o.add(d.scale(i * 0.6)).add(0, Math.sin(i * 0.4) * 0.3 + i * 0.05, 0);
            sl.sendParticles(ParticleTypes.PORTAL, q.x, q.y, q.z, 4, 0.05, 0.05, 0.05, 0.0);
            sl.sendParticles(ParticleTypes.END_ROD, q.x, q.y, q.z, 1, 0, 0, 0, 0);
        }
        sl.playSound(null, sp.blockPosition(), SoundEvents.ENDER_EYE_LAUNCH, SoundSource.PLAYERS, 1.0F, 0.7F);
        String[] dirs = {"au sud", "au sud-ouest", "à l'ouest", "au nord-ouest", "au nord", "au nord-est", "à l'est", "au sud-est"};
        double angle = Math.toDegrees(Math.atan2(-d.x, d.z));
        String dir = dirs[(int) Math.floorMod(Math.round(angle / 45.0), 8)];
        sp.sendSystemMessage(Component.literal("L'œil s'élance " + dir + " : l'antre de " + nom + " est à " + (int) distance + " blocs.")
                .withStyle(ChatFormatting.LIGHT_PURPLE));
        return InteractionResult.SUCCESS;
    }

    @Override
    public void appendHoverText(ItemStack pile, Item.TooltipContext contexte, TooltipDisplay affichage,
                                Consumer<Component> ajout, TooltipFlag options) {
        ajout.accept(Component.literal("Clic droit : montre la direction de l'antre de " + nom).withStyle(ChatFormatting.LIGHT_PURPLE));
        ajout.accept(Component.literal("Antre en " + royaume + " ; utilise le sceau sur son Autel des Seigneurs.").withStyle(ChatFormatting.GRAY));
    }
}
