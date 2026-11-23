package fr.royaumes.magie;

import fr.royaumes.entite.Combattant;
import java.util.ArrayList;
import java.util.Iterator;
import java.util.List;
import java.util.UUID;
import net.minecraft.core.particles.ParticleOptions;
import net.minecraft.core.particles.ParticleTypes;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.sounds.SoundEvent;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.sounds.SoundSource;
import net.minecraft.tags.EntityTypeTags;
import net.minecraft.world.effect.MobEffectInstance;
import net.minecraft.world.effect.MobEffects;
import net.minecraft.world.entity.Entity;
import net.minecraft.world.entity.EntitySpawnReason;
import net.minecraft.world.entity.EntityType;
import net.minecraft.world.entity.LightningBolt;
import net.minecraft.world.entity.LivingEntity;
import net.minecraft.world.entity.Mob;
import net.minecraft.world.entity.animal.wolf.Wolf;
import net.minecraft.world.entity.monster.Enemy;
import net.minecraft.world.entity.projectile.ProjectileUtil;
import net.minecraft.world.entity.projectile.hurtingprojectile.SmallFireball;
import net.minecraft.world.level.ClipContext;
import net.minecraft.world.phys.EntityHitResult;
import net.minecraft.world.phys.HitResult;
import net.minecraft.world.phys.Vec3;

/** Les seize sorts des huit Vents de magie. */
public final class Sorts {
    private record Invoque(ServerLevel niveau, UUID id, long fin) {}

    private static final List<Invoque> INVOQUES = new ArrayList<>();

    private Sorts() {}

    public static boolean lancer(ServerPlayer p, ServerLevel n, int vent, int rang) {
        return switch (vent * 2 + rang) {
            case 0 -> eclair(p, n);
            case 1 -> comete(p, n);
            case 2 -> trait(p, n);
            case 3 -> cendres(p, n);
            case 4 -> fureur(p, n);
            case 5 -> meute(p, n);
            case 6 -> seve(p, n);
            case 7 -> ronces(p, n);
            case 8 -> rayon(p, n);
            case 9 -> eclat(p, n);
            case 10 -> pas(p, n);
            case 11 -> voile(p, n);
            case 12 -> main(p, n);
            case 13 -> moisson(p, n);
            case 14 -> peau(p, n);
            case 15 -> plomb(p, n);
            default -> false;
        };
    }

    // ------------------------------------------------------------------ outils

    /** Un ennemi : monstre, guerrier d'une autre alliance, ou créature qui vise le lanceur. */
    static boolean ennemi(ServerPlayer p, LivingEntity e) {
        if (e == p || !e.isAlive()) {
            return false;
        }
        if (p.getTeam() != null && p.getTeam() == e.getTeam()) {
            return false;
        }
        return e instanceof Enemy || e instanceof Combattant || (e instanceof Mob m && m.getTarget() == p);
    }

    private static List<LivingEntity> ennemis(ServerPlayer p, ServerLevel n, Vec3 centre, double r) {
        return n.getEntitiesOfClass(LivingEntity.class, p.getBoundingBox().move(centre.subtract(p.position())).inflate(r),
                e -> ennemi(p, e) && e.position().distanceTo(centre) <= r + 1);
    }

    private static HitResult vise(ServerPlayer p, double portee) {
        return ProjectileUtil.getHitResultOnViewVector(p, e -> e instanceof LivingEntity l && l.isAlive() && e != p && !e.isSpectator(), portee);
    }

    private static LivingEntity cible(ServerPlayer p, double portee) {
        return vise(p, portee) instanceof EntityHitResult h && h.getEntity() instanceof LivingEntity l ? l : null;
    }

    private static void blesser(ServerPlayer p, ServerLevel n, LivingEntity e, float degats) {
        e.hurtServer(n, n.damageSources().indirectMagic(p, p), degats);
    }

    private static void son(ServerLevel n, Entity e, SoundEvent s, float volume, float hauteur) {
        n.playSound(null, e.getX(), e.getY(), e.getZ(), s, SoundSource.PLAYERS, volume, hauteur);
    }

    private static void trainee(ServerLevel n, ParticleOptions part, Vec3 a, Vec3 b, double pas) {
        Vec3 d = b.subtract(a);
        int k = (int) Math.max(1, d.length() / pas);
        for (int i = 0; i <= k; i++) {
            Vec3 q = a.add(d.scale(i / (double) k));
            n.sendParticles(part, q.x, q.y, q.z, 1, 0.02, 0.02, 0.02, 0.0);
        }
    }

    private static void cercle(ServerLevel n, ParticleOptions part, Vec3 c, double r, int points) {
        for (int i = 0; i < points; i++) {
            double a = 2 * Math.PI * i / points;
            n.sendParticles(part, c.x + Math.cos(a) * r, c.y + 0.2, c.z + Math.sin(a) * r, 1, 0.05, 0.05, 0.05, 0.0);
        }
    }

    private static void foudreVisuelle(ServerLevel n, Vec3 pos) {
        Entity e = EntityType.LIGHTNING_BOLT.create(n, EntitySpawnReason.TRIGGERED);
        if (e instanceof LightningBolt foudre) {
            foudre.setPos(pos.x, pos.y, pos.z);
            foudre.setVisualOnly(true);
            n.addFreshEntity(foudre);
        }
    }

    /** Retire les loups de Ghur arrivés au terme de leur minute. */
    public static void tick(long temps) {
        Iterator<Invoque> it = INVOQUES.iterator();
        while (it.hasNext()) {
            Invoque i = it.next();
            if (temps >= i.fin()) {
                Entity e = i.niveau().getEntity(i.id());
                if (e != null) {
                    i.niveau().sendParticles(ParticleTypes.POOF, e.getX(), e.getY() + 0.5, e.getZ(), 10, 0.3, 0.3, 0.3, 0.02);
                    e.discard();
                }
                it.remove();
            }
        }
    }

    // ------------------------------------------------------------------ Azyr

    private static boolean eclair(ServerPlayer p, ServerLevel n) {
        Vec3 pos = vise(p, 32).getLocation();
        foudreVisuelle(n, pos);
        for (LivingEntity e : ennemis(p, n, pos, 1.8)) {
            blesser(p, n, e, 9.0F);
            e.igniteForSeconds(2);
        }
        n.sendParticles(ParticleTypes.ELECTRIC_SPARK, pos.x, pos.y + 0.5, pos.z, 30, 0.6, 0.8, 0.6, 0.2);
        return true;
    }

    private static boolean comete(ServerPlayer p, ServerLevel n) {
        Vec3 pos = vise(p, 40).getLocation();
        for (int i = 0; i < 5; i++) {
            double a = i * 2 * Math.PI / 5;
            foudreVisuelle(n, pos.add(Math.cos(a) * 3, 0, Math.sin(a) * 3));
        }
        foudreVisuelle(n, pos);
        trainee(n, ParticleTypes.END_ROD, pos.add(-6, 18, -6), pos, 0.4);
        n.sendParticles(ParticleTypes.EXPLOSION_EMITTER, pos.x, pos.y + 0.5, pos.z, 1, 0, 0, 0, 0);
        n.sendParticles(ParticleTypes.ELECTRIC_SPARK, pos.x, pos.y + 1, pos.z, 120, 3, 1, 3, 0.4);
        cercle(n, ParticleTypes.END_ROD, pos, 5, 40);
        for (LivingEntity e : ennemis(p, n, pos, 5)) {
            blesser(p, n, e, 16.0F);
            Vec3 d = e.position().subtract(pos).normalize().scale(1.2);
            e.push(d.x, 0.6, d.z);
        }
        son(n, p, SoundEvents.LIGHTNING_BOLT_THUNDER, 1.5F, 0.8F);
        return true;
    }

    // ------------------------------------------------------------------ Aqshy

    private static boolean trait(ServerPlayer p, ServerLevel n) {
        Vec3 regard = p.getLookAngle();
        for (int i = -1; i <= 1; i++) {
            Vec3 d = regard.yRot((float) Math.toRadians(i * 6)).normalize();
            SmallFireball boule = new SmallFireball(n, p, d);
            boule.setPos(p.getX() + d.x, p.getEyeY() - 0.15, p.getZ() + d.z);
            n.addFreshEntity(boule);
        }
        son(n, p, SoundEvents.BLAZE_SHOOT, 1.0F, 1.1F);
        return true;
    }

    private static boolean cendres(ServerPlayer p, ServerLevel n) {
        Vec3 o = p.getEyePosition();
        Vec3 regard = p.getLookAngle().normalize();
        for (int k = 1; k <= 8; k++) {
            Vec3 q = o.add(regard.scale(k));
            n.sendParticles(ParticleTypes.FLAME, q.x, q.y - 0.3, q.z, 6 + k * 2, k * 0.15, 0.3, k * 0.15, 0.02);
            n.sendParticles(ParticleTypes.LARGE_SMOKE, q.x, q.y, q.z, 2, k * 0.1, 0.2, k * 0.1, 0.01);
        }
        for (LivingEntity e : ennemis(p, n, p.position(), 9)) {
            Vec3 vers = e.position().add(0, e.getBbHeight() / 2, 0).subtract(o);
            if (vers.length() <= 9 && vers.normalize().dot(regard) > 0.8) {
                blesser(p, n, e, 7.0F);
                e.igniteForSeconds(5);
            }
        }
        son(n, p, SoundEvents.FIRECHARGE_USE, 1.2F, 0.7F);
        return true;
    }

    // ------------------------------------------------------------------ Ghur

    private static boolean fureur(ServerPlayer p, ServerLevel n) {
        p.addEffect(new MobEffectInstance(MobEffects.STRENGTH, 300, 1));
        p.addEffect(new MobEffectInstance(MobEffects.SPEED, 300, 1));
        n.sendParticles(ParticleTypes.ANGRY_VILLAGER, p.getX(), p.getY() + 1.5, p.getZ(), 8, 0.5, 0.4, 0.5, 0.0);
        n.sendParticles(ParticleTypes.CRIT, p.getX(), p.getY() + 1, p.getZ(), 30, 0.5, 0.7, 0.5, 0.3);
        son(n, p, SoundEvents.EVOKER_PREPARE_SUMMON, 1.0F, 0.6F);
        return true;
    }

    private static boolean meute(ServerPlayer p, ServerLevel n) {
        for (int i = 0; i < 3; i++) {
            Wolf loup = EntityType.WOLF.create(n, EntitySpawnReason.MOB_SUMMONED);
            if (loup == null) {
                continue;
            }
            double a = i * 2 * Math.PI / 3;
            loup.setPos(p.getX() + Math.cos(a) * 1.8, p.getY(), p.getZ() + Math.sin(a) * 1.8);
            loup.tame(p);
            loup.addEffect(new MobEffectInstance(MobEffects.STRENGTH, 1200, 1));
            loup.addEffect(new MobEffectInstance(MobEffects.RESISTANCE, 1200, 0));
            n.addFreshEntity(loup);
            n.sendParticles(ParticleTypes.POOF, loup.getX(), loup.getY() + 0.5, loup.getZ(), 12, 0.3, 0.3, 0.3, 0.02);
            INVOQUES.add(new Invoque(n, loup.getUUID(), n.getGameTime() + 1200));
        }
        son(n, p, SoundEvents.EVOKER_PREPARE_SUMMON, 1.0F, 1.2F);
        return true;
    }

    // ------------------------------------------------------------------ Ghyran

    private static boolean seve(ServerPlayer p, ServerLevel n) {
        p.heal(8.0F);
        p.addEffect(new MobEffectInstance(MobEffects.REGENERATION, 100, 0));
        n.sendParticles(ParticleTypes.HEART, p.getX(), p.getY() + 1.8, p.getZ(), 6, 0.4, 0.3, 0.4, 0.0);
        n.sendParticles(ParticleTypes.HAPPY_VILLAGER, p.getX(), p.getY() + 1, p.getZ(), 30, 0.6, 0.8, 0.6, 0.0);
        son(n, p, SoundEvents.AMETHYST_BLOCK_CHIME, 1.0F, 0.8F);
        return true;
    }

    private static boolean ronces(ServerPlayer p, ServerLevel n) {
        cercle(n, ParticleTypes.COMPOSTER, p.position(), 6, 60);
        for (LivingEntity e : ennemis(p, n, p.position(), 6)) {
            blesser(p, n, e, 6.0F);
            e.addEffect(new MobEffectInstance(MobEffects.SLOWNESS, 100, 3), p);
            e.addEffect(new MobEffectInstance(MobEffects.POISON, 80, 0), p);
            n.sendParticles(ParticleTypes.HAPPY_VILLAGER, e.getX(), e.getY() + 0.3, e.getZ(), 15, 0.4, 0.2, 0.4, 0.0);
        }
        son(n, p, SoundEvents.EVOKER_CAST_SPELL, 1.0F, 0.8F);
        return true;
    }

    // ------------------------------------------------------------------ Hysh

    private static boolean rayon(ServerPlayer p, ServerLevel n) {
        HitResult h = vise(p, 24);
        trainee(n, ParticleTypes.END_ROD, p.getEyePosition().add(p.getLookAngle().scale(0.8)), h.getLocation(), 0.35);
        if (h instanceof EntityHitResult eh && eh.getEntity() instanceof LivingEntity l) {
            blesser(p, n, l, l.getType().is(EntityTypeTags.UNDEAD) ? 14.0F : 9.0F);
        }
        son(n, p, SoundEvents.BEACON_DEACTIVATE, 1.0F, 2.0F);
        return true;
    }

    private static boolean eclat(ServerPlayer p, ServerLevel n) {
        n.sendParticles(ParticleTypes.END_ROD, p.getX(), p.getY() + 1.2, p.getZ(), 150, 4, 2, 4, 0.15);
        for (LivingEntity e : ennemis(p, n, p.position(), 10)) {
            e.addEffect(new MobEffectInstance(MobEffects.BLINDNESS, 80, 0), p);
            e.addEffect(new MobEffectInstance(MobEffects.GLOWING, 200, 0), p);
            blesser(p, n, e, e.getType().is(EntityTypeTags.UNDEAD) ? 10.0F : 4.0F);
        }
        son(n, p, SoundEvents.BEACON_ACTIVATE, 1.2F, 1.8F);
        return true;
    }

    // ------------------------------------------------------------------ Ulgu

    private static boolean pas(ServerPlayer p, ServerLevel n) {
        Vec3 o = p.getEyePosition();
        Vec3 fin = o.add(p.getLookAngle().scale(16));
        HitResult h = n.clip(new ClipContext(o, fin, ClipContext.Block.COLLIDER, ClipContext.Fluid.NONE, p));
        Vec3 cible = h.getLocation().subtract(p.getLookAngle().scale(0.8)).subtract(0, p.getEyeHeight() * 0.5, 0);
        for (int essai = 0; essai < 6; essai++) {
            if (n.noCollision(p, p.getBoundingBox().move(cible.subtract(p.position())))) {
                break;
            }
            cible = cible.add(0, 0.5, 0);
        }
        n.sendParticles(ParticleTypes.SQUID_INK, p.getX(), p.getY() + 1, p.getZ(), 25, 0.3, 0.6, 0.3, 0.02);
        p.teleportTo(cible.x, cible.y, cible.z);
        p.resetFallDistance();
        n.sendParticles(ParticleTypes.PORTAL, cible.x, cible.y + 1, cible.z, 40, 0.3, 0.6, 0.3, 0.3);
        son(n, p, SoundEvents.ENDERMAN_TELEPORT, 0.8F, 0.6F);
        return true;
    }

    private static boolean voile(ServerPlayer p, ServerLevel n) {
        p.addEffect(new MobEffectInstance(MobEffects.INVISIBILITY, 400, 0));
        n.sendParticles(ParticleTypes.SQUID_INK, p.getX(), p.getY() + 1, p.getZ(), 80, 3, 1, 3, 0.02);
        for (LivingEntity e : ennemis(p, n, p.position(), 8)) {
            e.addEffect(new MobEffectInstance(MobEffects.DARKNESS, 120, 0), p);
            e.addEffect(new MobEffectInstance(MobEffects.SLOWNESS, 120, 0), p);
            if (e instanceof Mob m && m.getTarget() == p) {
                m.setTarget(null);
            }
        }
        son(n, p, SoundEvents.ILLUSIONER_MIRROR_MOVE, 1.0F, 0.7F);
        return true;
    }

    // ------------------------------------------------------------------ Shyish

    private static boolean main(ServerPlayer p, ServerLevel n) {
        LivingEntity c = cible(p, 20);
        if (c == null) {
            return false;
        }
        trainee(n, ParticleTypes.SOUL, p.getEyePosition(), c.position().add(0, c.getBbHeight() / 2, 0), 0.5);
        blesser(p, n, c, 6.0F);
        c.addEffect(new MobEffectInstance(MobEffects.WITHER, 120, 1), p);
        son(n, p, SoundEvents.WITHER_SHOOT, 0.6F, 1.4F);
        return true;
    }

    private static boolean moisson(ServerPlayer p, ServerLevel n) {
        float soin = 0;
        for (LivingEntity e : ennemis(p, n, p.position(), 6)) {
            blesser(p, n, e, 5.0F);
            trainee(n, ParticleTypes.SOUL_FIRE_FLAME, e.position().add(0, e.getBbHeight() / 2, 0), p.position().add(0, 1, 0), 0.6);
            soin += 2.0F;
        }
        p.heal(Math.min(10.0F, soin));
        cercle(n, ParticleTypes.SOUL, p.position(), 6, 50);
        son(n, p, SoundEvents.EVOKER_CAST_SPELL, 1.0F, 0.5F);
        return true;
    }

    // ------------------------------------------------------------------ Chamon

    private static boolean peau(ServerPlayer p, ServerLevel n) {
        p.addEffect(new MobEffectInstance(MobEffects.RESISTANCE, 400, 1));
        p.addEffect(new MobEffectInstance(MobEffects.ABSORPTION, 400, 1));
        n.sendParticles(ParticleTypes.WAX_ON, p.getX(), p.getY() + 1, p.getZ(), 40, 0.4, 0.8, 0.4, 0.5);
        son(n, p, SoundEvents.ANVIL_LAND, 0.5F, 1.6F);
        return true;
    }

    private static boolean plomb(ServerPlayer p, ServerLevel n) {
        cercle(n, ParticleTypes.WAX_OFF, p.position(), 8, 60);
        for (LivingEntity e : ennemis(p, n, p.position(), 8)) {
            e.addEffect(new MobEffectInstance(MobEffects.SLOWNESS, 160, 2), p);
            e.addEffect(new MobEffectInstance(MobEffects.WEAKNESS, 160, 1), p);
            e.addEffect(new MobEffectInstance(MobEffects.MINING_FATIGUE, 160, 1), p);
            n.sendParticles(ParticleTypes.WAX_OFF, e.getX(), e.getY() + 1, e.getZ(), 12, 0.3, 0.5, 0.3, 0.1);
        }
        son(n, p, SoundEvents.ANVIL_LAND, 0.7F, 0.5F);
        return true;
    }
}
