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
    private final String type;

    public ArmeFaction(Item.Properties p, int faction, boolean champion, String type) {
        super(p);
        this.faction = faction;
        this.champion = champion;
        this.type = type;
    }

    @Override
    public void hurtEnemy(ItemStack pile, LivingEntity cible, LivingEntity attaquant) {
        super.hurtEnemy(pile, cible, attaquant);
        if (!(attaquant.level() instanceof ServerLevel n) || (champion && attaquant.getRandom().nextFloat() > 0.25F)) {
            return;
        }
        int fort = champion ? 1 : 0;
        switch (ArsenalGenere.ATOUTS[faction]) {
            case "foudre" -> {
                n.sendParticles(ParticleTypes.ELECTRIC_SPARK, cible.getX(), cible.getY() + 1, cible.getZ(), 30, 0.3, 0.8, 0.3, 0.3);
                cible.hurtServer(n, n.damageSources().lightningBolt(), 4.0F);
            }
            case "feu" -> cible.igniteForSeconds(champion ? 6 : 4);
            case "poison" -> cible.addEffect(new MobEffectInstance(MobEffects.POISON, 80, 1 + fort), attaquant);
            case "fletri" -> cible.addEffect(new MobEffectInstance(MobEffects.WITHER, 80, fort), attaquant);
            case "vol_de_vie" -> {
                attaquant.heal(champion ? 4.0F : 2.5F);
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
        ajout.accept(Component.literal((champion ? "Arme de champion" : "Arme de lignée") + " · " + FactionsGenerees.NOMS[faction])
                .withColor(FactionsGenerees.COULEURS[faction]));
        ajout.accept(Component.literal(ArsenalGenere.TEXTES_ATOUTS[faction] + (champion ? " (1 coup sur 4)" : " (à chaque coup)"))
                .withStyle(ChatFormatting.GOLD));
    }
}
