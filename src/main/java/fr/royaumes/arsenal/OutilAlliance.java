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
        // épée Mythique et Divine : la frappe fend aussi les ennemis autour de la cible (40 % / 60 % des dégâts)
        if (palier >= 3) {
            float part = palier >= 4 ? 0.6F : 0.4F;
            float degats = (float) sp.getAttributeValue(net.minecraft.world.entity.ai.attributes.Attributes.ATTACK_DAMAGE) * part;
            String equipe = "rm_" + ArsenalGenere.ALLIANCES[alliance];
            for (LivingEntity e : n.getEntitiesOfClass(LivingEntity.class, cible.getBoundingBox().inflate(3.0),
                    e -> e != cible && e != sp && e.isAlive() && !(e instanceof net.minecraft.world.entity.player.Player)
                            && (e instanceof net.minecraft.world.entity.monster.Enemy || e instanceof fr.royaumes.entite.Combattant)
                            && !(e instanceof fr.royaumes.entite.Combattant cc && (cc.profil().equipe().equals(equipe)
                                    || cc.entityTags().contains(fr.royaumes.camp.Camps.UNITE))))) {
                e.hurtServer(n, n.damageSources().playerAttack(sp), degats);
            }
            n.sendParticles(ParticleTypes.SWEEP_ATTACK, cible.getX(), cible.getY() + 1, cible.getZ(), 3, 1.2, 0.2, 1.2, 0.0);
        }
        switch (ArsenalGenere.BUFFS_OUTILS[alliance][4]) {
            case "faiblesse" -> {
                cible.addEffect(new MobEffectInstance(MobEffects.WEAKNESS, 60, Math.min(3, palier)), attaquant);
                if (palier >= 2 && attaquant.getRandom().nextFloat() < 0.1F + 0.1F * palier) {
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
            if (i[1] == 2) {
                l.playSound(null, pos, SoundEvents.AXE_STRIP.value(), SoundSource.BLOCKS, 1.0F, 1.0F);
            } else if (i[1] == 1) {
                l.playSound(null, pos, SoundEvents.SHOVEL_FLATTEN.value(), SoundSource.BLOCKS, 1.0F, 1.0F);
            } else {
                l.playSound(null, pos, SoundEvents.HOE_TILL.value(), SoundSource.BLOCKS, 1.0F, 1.0F);
            }
            if (c.getPlayer() != null) {
                c.getItemInHand().hurtAndBreak(1, c.getPlayer(), c.getHand());
            }
            // houe Mythique (3×3) et Divine (5×5) : laboure toute la zone autour
            int r = i[1] == 3 ? (palier >= 4 ? 2 : palier == 3 ? 1 : 0) : 0;
            if (r > 0 && c.getPlayer() != null && !c.getPlayer().isShiftKeyDown()) {
                for (int dx = -r; dx <= r; dx++) {
                    for (int dz = -r; dz <= r; dz++) {
                        BlockPos q = pos.offset(dx, 0, dz);
                        BlockState sq = l.getBlockState(q);
                        if ((dx != 0 || dz != 0) && (sq.is(Blocks.GRASS_BLOCK) || sq.is(Blocks.DIRT) || sq.is(Blocks.DIRT_PATH))
                                && l.getBlockState(q.above()).isAir()) {
                            l.setBlock(q, Blocks.FARMLAND.defaultBlockState(), 11);
                        }
                    }
                }
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
        static final java.util.Map<String, String> NOMS_EFFETS = java.util.Map.ofEntries(java.util.Map.entry("haste", "Célérité"),
                java.util.Map.entry("speed", "Vitesse"), java.util.Map.entry("resistance", "Résistance"), java.util.Map.entry("regeneration", "Régénération"),
                java.util.Map.entry("fire_resistance", "Résistance au feu"), java.util.Map.entry("strength", "Force"), java.util.Map.entry("luck", "Chance"),
                java.util.Map.entry("night_vision", "Vision nocturne"), java.util.Map.entry("health_boost", "Vie bonus"),
                java.util.Map.entry("slow_falling", "Chute lente"), java.util.Map.entry("water_breathing", "Respiration"),
                java.util.Map.entry("dolphins_grace", "Grâce du dauphin"), java.util.Map.entry("jump_boost", "Saut"),
                java.util.Map.entry("invisibility", "Invisibilité"));

        public static String nomEffet(String e) {
            return NOMS_EFFETS.getOrDefault(e, e);
        }

        static final java.util.Map<String, String> EPEE = java.util.Map.of("faiblesse", "Affaiblit la cible (foudre en Légende)",
                "feu", "Enflamme la cible", "vol_de_vie", "Te soigne à chaque coup", "recul", "Projette la cible");

        public static void tooltip(int alliance, int outil, int palier, Consumer<Component> ajout) {
            ajout.accept(Component.literal(NOMS[alliance] + " · " + ArsenalGenere.NOMS_PALIERS[palier]).withStyle(ChatFormatting.GOLD));
            String b = ArsenalGenere.BUFFS_OUTILS[alliance][outil];
            int niv = b.equals("regeneration") || b.equals("resistance") ? 0 : Math.min(3, palier);
            String t = outil == 4 ? EPEE.getOrDefault(b, b) : TEXTES.getOrDefault(b, b) + (niv > 0 ? " (niveau " + (niv + 1) + ")" : "");
            ajout.accept(Component.literal(t).withStyle(ChatFormatting.GREEN));
            String pouvoir = switch (outil) {
                case 0, 1 -> PouvoirsOutils.ligne(palier) > 1 ? "Creuse " + PouvoirsOutils.ligne(palier) + " blocs en ligne (accroupi : un seul)" : "";
                case 2 -> PouvoirsOutils.arbre(palier) > 0 ? "Abat l'arbre entier, jusqu'à " + PouvoirsOutils.arbre(palier) + " bûches" : "";
                case 3 -> palier >= 3 ? "Laboure une zone " + (palier >= 4 ? "5×5" : "3×3") : "";
                default -> palier >= 3 ? "Fend les ennemis autour de la cible (" + (palier >= 4 ? 60 : 40) + " % des dégâts)" : "";
            };
            if (!pouvoir.isEmpty()) {
                ajout.accept(Component.literal("✦ " + pouvoir).withStyle(ChatFormatting.LIGHT_PURPLE));
            }
            ajout.accept(Component.literal("Réservé aux héros de l'alliance").withStyle(ChatFormatting.GRAY));
        }
    }
}
