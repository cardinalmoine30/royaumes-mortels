package fr.royaumes.magie;

import fr.royaumes.ModEntites;
import net.minecraft.ChatFormatting;
import net.minecraft.core.particles.ParticleTypes;
import net.minecraft.network.chat.Component;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.world.effect.MobEffectInstance;
import net.minecraft.world.effect.MobEffects;
import net.minecraft.world.entity.Entity;
import net.minecraft.world.entity.EntitySpawnReason;
import net.minecraft.world.entity.LivingEntity;
import net.minecraft.world.entity.projectile.hurtingprojectile.SmallFireball;
import net.minecraft.world.phys.Vec3;

/** Pouvoirs des reliques des six seigneurs (clic droit ; accroupi pour le second pouvoir quand il existe). */
public final class Reliques {
    private Reliques() {}

    /** Renvoie le temps de recharge en ticks, ou 0 si rien n'a été lancé. */
    public static int utiliser(ServerPlayer p, ServerLevel n, String seigneur, boolean accroupi) {
        Vec3 pos = p.position();
        switch (seigneur) {
            case "nagash" -> {
                if (accroupi) { // Main de Nagash : drain de vie
                    float soin = 0;
                    for (LivingEntity e : Sorts.ennemis(p, n, pos, 9)) {
                        Sorts.blesser(p, n, e, 9.0F);
                        e.addEffect(new MobEffectInstance(MobEffects.WITHER, 100, 1), p);
                        Sorts.trainee(n, ParticleTypes.SOUL, e.position().add(0, 1, 0), pos.add(0, 1, 0), 0.5);
                        soin += 3;
                    }
                    p.heal(Math.min(16, soin));
                    Sorts.cercle(n, ParticleTypes.SOUL_FIRE_FLAME, pos, 9, 60);
                    Sorts.son(n, p, SoundEvents.WITHER_SHOOT, 1.0F, 0.5F);
                    return 300;
                }
                var type = ModEntites.ENTITES.get("deathrattle");
                if (type == null) {
                    return 0;
                }
                for (int i = 0; i < 4; i++) { // Armée des Morts
                    Entity e = type.get().create(n, EntitySpawnReason.MOB_SUMMONED);
                    if (e == null) {
                        continue;
                    }
                    double a = i * Math.PI / 2;
                    e.setPos(pos.x + Math.cos(a) * 2.5, pos.y, pos.z + Math.sin(a) * 2.5);
                    if (p.getTeam() != null) {
                        n.getScoreboard().addPlayerToTeam(e.getScoreboardName(), n.getScoreboard().getPlayerTeam(p.getTeam().getName()));
                    }
                    e.addTag("rm_nom_" + p.getScoreboardName());
                    n.addFreshEntity(e);
                    n.sendParticles(ParticleTypes.SOUL, e.getX(), e.getY() + 1, e.getZ(), 30, 0.4, 0.8, 0.4, 0.05);
                    Sorts.INVOQUES.add(new Sorts.Invoque(n, e.getUUID(), n.getGameTime() + 1200));
                }
                Sorts.son(n, p, SoundEvents.EVOKER_PREPARE_SUMMON, 1.2F, 0.5F);
                return 600;
            }
            case "archaon" -> { // Œil de Sheerian
                for (LivingEntity e : Sorts.ennemis(p, n, pos, 9)) {
                    e.addEffect(new MobEffectInstance(MobEffects.BLINDNESS, 100, 0), p);
                    e.addEffect(new MobEffectInstance(MobEffects.WEAKNESS, 200, 2), p);
                    Sorts.blesser(p, n, e, 6.0F);
                }
                p.addEffect(new MobEffectInstance(MobEffects.STRENGTH, 300, 2));
                p.addEffect(new MobEffectInstance(MobEffects.RESISTANCE, 300, 1));
                n.sendParticles(ParticleTypes.SMOKE, pos.x, pos.y + 1, pos.z, 120, 4, 1, 4, 0.05);
                Sorts.son(n, p, SoundEvents.ENDER_DRAGON_GROWL, 0.8F, 1.3F);
                return 400;
            }
            case "gordrakk" -> { // Onde du Waaagh
                Sorts.cercle(n, ParticleTypes.EXPLOSION, pos, 4, 16);
                for (LivingEntity e : Sorts.ennemis(p, n, pos, 7)) {
                    Sorts.blesser(p, n, e, 14.0F);
                    Vec3 d = e.position().subtract(pos).normalize();
                    e.push(d.x * 1.6, 0.9, d.z * 1.6);
                }
                p.addEffect(new MobEffectInstance(MobEffects.SPEED, 200, 1));
                Sorts.son(n, p, SoundEvents.RAVAGER_ROAR, 1.2F, 0.8F);
                return 300;
            }
            case "skarbrand" -> { // Rugissement de rage : cône de feu
                Vec3 o = p.getEyePosition();
                Vec3 regard = p.getLookAngle().normalize();
                for (int k = 1; k <= 11; k++) {
                    Vec3 q = o.add(regard.scale(k));
                    n.sendParticles(ParticleTypes.FLAME, q.x, q.y - 0.3, q.z, 10 + k * 2, k * 0.18, 0.4, k * 0.18, 0.03);
                }
                for (LivingEntity e : Sorts.ennemis(p, n, pos, 11)) {
                    Vec3 vers = e.position().add(0, e.getBbHeight() / 2, 0).subtract(o);
                    if (vers.normalize().dot(regard) > 0.7) {
                        Sorts.blesser(p, n, e, 12.0F);
                        e.igniteForSeconds(8);
                    }
                }
                Sorts.son(n, p, SoundEvents.BLAZE_SHOOT, 1.2F, 0.5F);
                return 240;
            }
            case "thanquol" -> {
                if (accroupi) { // saut par la Warp
                    Sorts.lancer(p, n, 5, 0);
                    return 160;
                }
                Vec3 regard = p.getLookAngle();
                for (int i = -2; i <= 2; i++) { // malefeu
                    Vec3 d = regard.yRot((float) Math.toRadians(i * 7)).normalize();
                    SmallFireball b = new SmallFireball(n, p, d);
                    b.setPos(p.getX() + d.x, p.getEyeY() - 0.15, p.getZ() + d.z);
                    n.addFreshEntity(b);
                }
                n.sendParticles(ParticleTypes.HAPPY_VILLAGER, p.getX(), p.getEyeY(), p.getZ(), 30, 0.5, 0.4, 0.5, 0.1);
                Sorts.son(n, p, SoundEvents.BLAZE_SHOOT, 1.0F, 1.4F);
                return 100;
            }
            case "rotigus" -> { // Pluie de pestilence
                for (LivingEntity e : Sorts.ennemis(p, n, pos, 9)) {
                    e.addEffect(new MobEffectInstance(MobEffects.POISON, 200, 1), p);
                    e.addEffect(new MobEffectInstance(MobEffects.SLOWNESS, 200, 1), p);
                    Sorts.blesser(p, n, e, 4.0F);
                }
                p.addEffect(new MobEffectInstance(MobEffects.REGENERATION, 200, 1));
                n.sendParticles(ParticleTypes.FALLING_WATER, pos.x, pos.y + 6, pos.z, 300, 6, 0.5, 6, 0);
                n.sendParticles(ParticleTypes.ITEM_SLIME, pos.x, pos.y + 1, pos.z, 80, 5, 0.5, 5, 0);
                Sorts.son(n, p, SoundEvents.EVOKER_CAST_SPELL, 1.0F, 0.6F);
                return 300;
            }
            default -> {
                p.sendOverlayMessage(Component.literal("Cette relique sommeille.").withStyle(ChatFormatting.GRAY));
                return 0;
            }
        }
    }
}
