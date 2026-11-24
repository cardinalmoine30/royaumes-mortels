package fr.royaumes.arsenal;

import fr.royaumes.ArsenalGenere;
import java.util.function.Consumer;
import net.minecraft.ChatFormatting;
import net.minecraft.core.BlockPos;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.resources.Identifier;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.sounds.SoundSource;
import net.minecraft.world.InteractionResult;
import net.minecraft.world.item.context.UseOnContext;
import net.minecraft.world.level.Level;
import net.minecraft.world.level.block.Block;
import net.minecraft.world.level.block.Blocks;
import net.minecraft.world.level.block.state.BlockState;
import net.minecraft.core.particles.ParticleTypes;
import net.minecraft.network.chat.Component;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.world.effect.MobEffectInstance;
import net.minecraft.world.effect.MobEffects;
import net.minecraft.world.entity.LivingEntity;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.TooltipFlag;
import net.minecraft.world.item.component.TooltipDisplay;
import net.minecraft.world.phys.Vec3;

/** Outil d'alliance : effet en main (Arsenal.bonusPanoplie), atout au coup pour l'épée. */
public class OutilAlliance extends Item {
    private final int alliance;
    private final int palier;
    private final boolean epee;

    public OutilAlliance(Item.Properties p, int alliance, int palier, boolean epee) {
        super(p);
        this.alliance = alliance;
        this.palier = palier;
        this.epee = epee;
    }

    @Override
    public void hurtEnemy(ItemStack pile, LivingEntity cible, LivingEntity attaquant) {
        super.hurtEnemy(pile, cible, attaquant);
        if (!epee || !(attaquant.level() instanceof ServerLevel n)
                || !(attaquant instanceof net.minecraft.server.level.ServerPlayer sp) || Arsenal.alliance(Arsenal.scoreFaction(sp)) != alliance) {
            return;
        }
        switch (ArsenalGenere.BUFFS_OUTILS[alliance][4]) {
            case "faiblesse" -> {
                cible.addEffect(new MobEffectInstance(MobEffects.WEAKNESS, 60, palier), attaquant);
                if (palier == 2 && attaquant.getRandom().nextFloat() < 0.2F) {
                    n.sendParticles(ParticleTypes.ELECTRIC_SPARK, cible.getX(), cible.getY() + 1, cible.getZ(), 30, 0.3, 0.8, 0.3, 0.3);
                    cible.hurtServer(n, n.damageSources().lightningBolt(), 4.0F);
                }
            }
            case "feu" -> cible.igniteForSeconds(2 + 2 * palier);
            case "vol_de_vie" -> attaquant.heal(1.0F + palier);
            case "recul" -> {
                Vec3 d = cible.position().subtract(attaquant.position()).normalize();
                cible.push(d.x * (0.6 + 0.4 * palier), 0.3, d.z * (0.6 + 0.4 * palier));
            }
            default -> {
            }
        }
    }

    /** Hache : écorce ; pelle : chemin ; houe : laboure (comme les outils vanilla). */
    @Override
    public InteractionResult useOn(UseOnContext c) {
        int[] i = Arsenal.infosOutil(this);
        if (i == null || i[1] < 1 || i[1] > 3) {
            return super.useOn(c);
        }
        Level l = c.getLevel();
        BlockPos pos = c.getClickedPos();
        BlockState st = l.getBlockState(pos);
        Identifier id = BuiltInRegistries.BLOCK.getKey(st.getBlock());
        BlockState neuf = null;
        if (i[1] == 2 && !id.getPath().startsWith("stripped_") && (id.getPath().endsWith("_log") || id.getPath().endsWith("_wood")
                || id.getPath().endsWith("_stem") || id.getPath().endsWith("_hyphae"))) {
            Block b = BuiltInRegistries.BLOCK.getValue(Identifier.fromNamespaceAndPath(id.getNamespace(), "stripped_" + id.getPath()));
            if (b != Blocks.AIR) {
                neuf = b.withPropertiesOf(st);
            }
        } else if (i[1] == 1 && st.is(Blocks.GRASS_BLOCK) && l.getBlockState(pos.above()).isAir()) {
            neuf = Blocks.DIRT_PATH.defaultBlockState();
        } else if (i[1] == 3 && (st.is(Blocks.GRASS_BLOCK) || st.is(Blocks.DIRT) || st.is(Blocks.DIRT_PATH))
                && l.getBlockState(pos.above()).isAir()) {
            neuf = Blocks.FARMLAND.defaultBlockState();
        }
        if (neuf == null) {
            return super.useOn(c);
        }
        if (!l.isClientSide()) {
            l.setBlock(pos, neuf, 11);
            l.playSound(null, pos, i[1] == 2 ? SoundEvents.AXE_STRIP : i[1] == 1 ? SoundEvents.SHOVEL_FLATTEN : SoundEvents.HOE_TILL,
                    SoundSource.BLOCKS, 1.0F, 1.0F);
            if (c.getPlayer() != null) {
                c.getItemInHand().hurtAndBreak(1, c.getPlayer(), c.getHand());
            }
        }
        return InteractionResult.SUCCESS;
    }

    @Override
    public void appendHoverText(ItemStack pile, Item.TooltipContext contexte, TooltipDisplay affichage,
                                Consumer<Component> ajout, TooltipFlag options) {
        int[] i = Arsenal.infosOutil(this);
        Infos.tooltip(alliance, i == null ? 0 : i[1], palier, ajout);
    }

    /** Texte commun aux outils d'alliance. */
    public static final class Infos {
        private Infos() {}

        static final String[] NOMS = {"Grande Alliance de l'Ordre", "Grande Alliance du Chaos", "Grande Alliance de la Mort", "Grande Alliance de la Destruction"};
        static final java.util.Map<String, String> TEXTES = java.util.Map.of("haste", "Célérité en main", "speed", "Vitesse en main",
                "resistance", "Résistance en main", "regeneration", "Régénération en main", "fire_resistance", "Résistance au feu en main",
                "strength", "Force en main", "luck", "Chance en main", "night_vision", "Vision nocturne en main", "health_boost", "Vie bonus en main");
        static final java.util.Map<String, String> EPEE = java.util.Map.of("faiblesse", "Affaiblit la cible (foudre en Légende)",
                "feu", "Enflamme la cible", "vol_de_vie", "Te soigne à chaque coup", "recul", "Projette la cible");

        public static void tooltip(int alliance, int outil, int palier, Consumer<Component> ajout) {
            ajout.accept(Component.literal(NOMS[alliance] + " · " + ArsenalGenere.NOMS_PALIERS[palier]).withStyle(ChatFormatting.GOLD));
            String b = ArsenalGenere.BUFFS_OUTILS[alliance][outil];
            String t = outil == 4 ? EPEE.getOrDefault(b, b) : TEXTES.getOrDefault(b, b) + (palier > 0 ? " (niveau " + (palier + 1) + ")" : "");
            ajout.accept(Component.literal(t).withStyle(ChatFormatting.GREEN));
            ajout.accept(Component.literal("Réservé aux héros de l'alliance").withStyle(ChatFormatting.GRAY));
        }
    }
}
