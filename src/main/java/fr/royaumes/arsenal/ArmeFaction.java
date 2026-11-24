package fr.royaumes.arsenal;

import fr.royaumes.ArsenalGenere;
import fr.royaumes.FactionsGenerees;
import java.util.function.Consumer;
import net.minecraft.ChatFormatting;
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

/** Arme de faction. Champion : très puissante, atout une fois sur quatre. Lignée : moyenne, atout à chaque coup. */
public class ArmeFaction extends Item {
    private final int faction;
    private final boolean champion;
    private final int rang;
    private final String type;

    /** rang : 0 lignée (atout à chaque coup), 1 champion (1 coup sur 4, plus fort), 2 ascension (1 coup sur 2, le plus fort). */
    public ArmeFaction(Item.Properties p, int faction, int rang, String type) {
        super(p);
        this.faction = faction;
        this.champion = rang > 0;
        this.rang = rang;
        this.type = type;
    }

    @Override
    public void hurtEnemy(ItemStack pile, LivingEntity cible, LivingEntity attaquant) {
        super.hurtEnemy(pile, cible, attaquant);
        if (!(attaquant.level() instanceof ServerLevel n) || (rang > 0 && attaquant.getRandom().nextFloat() > (rang == 2 ? 0.5F : 0.25F))) {
            return;
        }
        int fort = rang;
        switch (ArsenalGenere.ATOUTS[faction]) {
            case "foudre" -> {
                n.sendParticles(ParticleTypes.ELECTRIC_SPARK, cible.getX(), cible.getY() + 1, cible.getZ(), 30, 0.3, 0.8, 0.3, 0.3);
                cible.hurtServer(n, n.damageSources().lightningBolt(), 4.0F);
            }
            case "feu" -> cible.igniteForSeconds(4 + 2 * rang);
            case "poison" -> cible.addEffect(new MobEffectInstance(MobEffects.POISON, 80, 1 + fort), attaquant);
            case "fletri" -> cible.addEffect(new MobEffectInstance(MobEffects.WITHER, 80, fort), attaquant);
            case "vol_de_vie" -> {
                attaquant.heal(2.5F + 1.5F * rang);
                n.sendParticles(ParticleTypes.DAMAGE_INDICATOR, cible.getX(), cible.getY() + 1, cible.getZ(), 6, 0.3, 0.3, 0.3, 0.1);
            }
            case "lenteur" -> cible.addEffect(new MobEffectInstance(MobEffects.SLOWNESS, 60, 2 + fort), attaquant);
            case "recul" -> {
                Vec3 d = cible.position().subtract(attaquant.position()).normalize();
                cible.push(d.x * 1.4, 0.45, d.z * 1.4);
            }
            case "aveugle" -> cible.addEffect(new MobEffectInstance(MobEffects.BLINDNESS, 50, 0), attaquant);
            case "faiblesse" -> cible.addEffect(new MobEffectInstance(MobEffects.WEAKNESS, 80, 1 + fort), attaquant);
            default -> {
            }
        }
    }

    @Override
    public boolean isFoil(ItemStack pile) {
        return champion;
    }

    @Override
    public void appendHoverText(ItemStack pile, Item.TooltipContext contexte, TooltipDisplay affichage,
                                Consumer<Component> ajout, TooltipFlag options) {
        ajout.accept(Component.literal(new String[] {"Arme de lignée", "Arme de champion", "Arme d'ascension"}[rang] + " · " + FactionsGenerees.NOMS[faction])
                .withColor(FactionsGenerees.COULEURS[faction]));
        ajout.accept(Component.literal(ArsenalGenere.TEXTES_ATOUTS[faction] + new String[] {" (à chaque coup)", " (1 coup sur 4)", " (1 coup sur 2, renforcé)"}[rang]))
                .withStyle(ChatFormatting.GOLD));
    }
}
