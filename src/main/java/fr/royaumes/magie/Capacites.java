package fr.royaumes.magie;

import fr.royaumes.ContenuGenere;
import fr.royaumes.ModEntites;
import fr.royaumes.reseau.Reseau;
import java.util.HashMap;
import java.util.Map;
import java.util.UUID;
import net.minecraft.ChatFormatting;
import net.minecraft.core.Holder;
import net.minecraft.core.particles.ParticleOptions;
import net.minecraft.core.particles.ParticleTypes;
import net.minecraft.core.particles.SimpleParticleType;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.network.chat.Component;
import net.minecraft.resources.Identifier;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.world.effect.MobEffect;
import net.minecraft.world.effect.MobEffectInstance;
import net.minecraft.world.entity.Entity;
import net.minecraft.world.entity.EntitySpawnReason;
import net.minecraft.world.entity.LivingEntity;
import net.minecraft.world.entity.projectile.arrow.Arrow;
import net.minecraft.world.entity.projectile.hurtingprojectile.SmallFireball;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.Items;
import net.minecraft.world.level.ClipContext;
import net.minecraft.world.phys.HitResult;
import net.minecraft.world.phys.Vec3;

/**
 * Capacités de faction (touche R) : une par faction, décrite dans ContenuGenere (outils/objets/capacites.py)
 * et construite sur une poignée d'archétypes. Gratuites, mais avec un long temps de recharge.
 */
public final class Capacites {
    private static final Map<UUID, Long> PRETE_A = new HashMap<>();

    private Capacites() {}

    /** Secondes restantes avant que la capacité soit prête (0 = prête). */
    public static int reste(ServerPlayer p) {
        long t = PRETE_A.getOrDefault(p.getUUID(), 0L) - p.level().getGameTime();
        return t <= 0 ? 0 : (int) ((t + 19) / 20);
    }

    public static void utiliser(ServerPlayer p, int faction) {
        if (faction < 1 || faction >= ContenuGenere.CAP_NOMS.length) {
            p.sendOverlayMessage(Component.translatable("royaumes.capacite.sans", Component.keybind("key.royaumes.serment")).withStyle(ChatFormatting.GRAY));
            return;
        }
        int r = reste(p);
        if (r > 0 && !p.isCreative()) {
            p.sendOverlayMessage(Component.translatable("royaumes.capacite.attente", ContenuGenere.CAP_NOMS[faction], r).withStyle(ChatFormatting.GRAY));
            return;
        }
        ServerLevel n = p.level();
        if (!lancer(p, n, faction)) {
            return;
        }
        appliquer(p, p, ContenuGenere.CAP_EFFETS_SOI[faction]);
        PRETE_A.put(p.getUUID(), n.getGameTime() + (long) (ContenuGenere.CAP_RECHARGES[faction] * 20L * fr.royaumes.rpg.Voies.recharge(p)));
        p.sendOverlayMessage(Component.literal("✦ " + ContenuGenere.CAP_NOMS[faction] + " ✦").withStyle(ChatFormatting.GOLD, ChatFormatting.BOLD));
        Reseau.envoyerFiche(p);
        Saga.accorder(p, "capacite");
    }

    // ------------------------------------------------------------------ outils

    private static ParticleOptions particule(int f) {
        var t = BuiltInRegistries.PARTICLE_TYPE.getValue(Identifier.withDefaultNamespace(ContenuGenere.CAP_PARTICULES[f]));
        return t instanceof SimpleParticleType s ? s : ParticleTypes.END_ROD;
    }

    /** "effet:amplificateur:durée,…" -> effets appliqués à la cible. */
    private static void appliquer(ServerPlayer source, LivingEntity cible, String effets) {
        if (effets.isEmpty()) {
            return;
        }
        for (String e : effets.split(",")) {
            String[] x = e.split(":");
            MobEffect effet = BuiltInRegistries.MOB_EFFECT.getValue(Identifier.withDefaultNamespace(x[0]));
            if (effet == null) {
                continue;
            }
            Holder<MobEffect> h = BuiltInRegistries.MOB_EFFECT.wrapAsHolder(effet);
            cible.addEffect(new MobEffectInstance(h, Integer.parseInt(x[2]), Integer.parseInt(x[1])), source);
        }
    }

    private static void frapperZone(ServerPlayer p, ServerLevel n, int f, Vec3 centre, double rayon, boolean projeter) {
        for (LivingEntity e : Sorts.ennemis(p, n, centre, rayon)) {
            Sorts.blesser(p, n, e, ContenuGenere.CAP_DEGATS[f]);
            appliquer(p, e, ContenuGenere.CAP_EFFETS_ENNEMIS[f]);
            if (projeter) {
                Vec3 d = e.position().subtract(centre).normalize();
                e.push(d.x * 1.2, 0.7, d.z * 1.2);
            }
        }
    }

    // ------------------------------------------------------------------ archétypes

    private static boolean lancer(ServerPlayer p, ServerLevel n, int f) {
        ParticleOptions part = particule(f);
        float rayon = ContenuGenere.CAP_RAYONS[f];
        Vec3 pos = p.position();
        switch (ContenuGenere.CAP_TYPES[f]) {
            case "ECLAIR" -> {
                Vec3 cible = Sorts.vise(p, 30).getLocation();
                n.sendParticles(part, pos.x, pos.y + 1, pos.z, 30, 0.3, 0.8, 0.3, 0.2);
                p.teleportTo(cible.x, cible.y + 0.1, cible.z);
                p.resetFallDistance();
                Sorts.foudreVisuelle(n, cible);
                n.sendParticles(part, cible.x, cible.y + 1, cible.z, 60, 1.5, 1, 1.5, 0.3);
                frapperZone(p, n, f, cible, rayon, true);
                Sorts.son(n, p, SoundEvents.LIGHTNING_BOLT_THUNDER, 1.0F, 1.2F);
            }
            case "COMETE" -> {
                Vec3 cible = Sorts.vise(p, 40).getLocation();
                Sorts.trainee(n, part, cible.add(8, 20, 8), cible, 0.5);
                Sorts.foudreVisuelle(n, cible);
                n.sendParticles(ParticleTypes.EXPLOSION_EMITTER, cible.x, cible.y + 0.5, cible.z, 1, 0, 0, 0, 0);
                Sorts.cercle(n, part, cible, rayon, 40);
                frapperZone(p, n, f, cible, rayon, true);
                Sorts.son(n, p, SoundEvents.LIGHTNING_BOLT_THUNDER, 1.5F, 0.7F);
            }
            case "FRAPPE_SOI" -> {
                Sorts.cercle(n, part, pos, rayon, 48);
                Sorts.cercle(n, part, pos, rayon * 0.5, 24);
                frapperZone(p, n, f, pos, rayon, true);
                Sorts.son(n, p, SoundEvents.PLAYER_ATTACK_SWEEP, 1.2F, 0.7F);
            }
            case "MALEDICTION" -> {
                n.sendParticles(part, pos.x, pos.y + 1, pos.z, 120, rayon * 0.5, 1, rayon * 0.5, 0.05);
                frapperZone(p, n, f, pos, rayon, false);
                Sorts.son(n, p, SoundEvents.EVOKER_CAST_SPELL, 1.0F, 0.6F);
            }
            case "AURA" -> {
                n.sendParticles(part, pos.x, pos.y + 1, pos.z, 60, 0.6, 1, 0.6, 0.1);
                Sorts.son(n, p, SoundEvents.EVOKER_PREPARE_SUMMON, 1.0F, 0.9F);
            }
            case "SOIN" -> {
                p.heal(ContenuGenere.CAP_DEGATS[f]);
                if (rayon > 0) {
                    for (ServerPlayer allie : n.getEntitiesOfClass(ServerPlayer.class, p.getBoundingBox().inflate(rayon), a -> a != p)) {
                        allie.heal(ContenuGenere.CAP_DEGATS[f] / 2);
                        n.sendParticles(ParticleTypes.HEART, allie.getX(), allie.getY() + 2, allie.getZ(), 4, 0.3, 0.2, 0.3, 0);
                    }
                    for (LivingEntity e : Sorts.ennemis(p, n, pos, rayon)) {
                        appliquer(p, e, ContenuGenere.CAP_EFFETS_ENNEMIS[f]);
                    }
                    Sorts.cercle(n, part, pos, rayon, 48);
                }
                n.sendParticles(part, pos.x, pos.y + 1, pos.z, 40, 0.6, 0.8, 0.6, 0.05);
                Sorts.son(n, p, SoundEvents.AMETHYST_BLOCK_CHIME, 1.0F, 0.7F);
            }
            case "DRAIN" -> {
                float soin = 0;
                for (LivingEntity e : Sorts.ennemis(p, n, pos, rayon)) {
                    Sorts.blesser(p, n, e, ContenuGenere.CAP_DEGATS[f]);
                    Sorts.trainee(n, part, e.position().add(0, 1, 0), pos.add(0, 1, 0), 0.6);
                    soin += ContenuGenere.CAP_DEGATS[f] * 0.6F;
                }
                p.heal(Math.min(14F, soin));
                Sorts.son(n, p, SoundEvents.WITHER_SHOOT, 0.6F, 0.8F);
            }
            case "SALVE_FLECHES" -> {
                Vec3 regard = p.getLookAngle();
                for (int i = -4; i <= 4; i++) {
                    Vec3 d = regard.yRot((float) Math.toRadians(i * 4)).normalize();
                    Arrow fleche = new Arrow(n, p, new ItemStack(Items.ARROW), null);
                    fleche.setPos(p.getX(), p.getEyeY() - 0.1, p.getZ());
                    fleche.shoot(d.x, d.y, d.z, 3.0F, 1.0F);
                    fleche.setBaseDamage(ContenuGenere.CAP_DEGATS[f] / 3.0);
                    fleche.pickup = Arrow.Pickup.DISALLOWED;
                    n.addFreshEntity(fleche);
                }
                n.sendParticles(part, p.getX(), p.getEyeY(), p.getZ(), 20, 0.4, 0.2, 0.4, 0.1);
                Sorts.son(n, p, SoundEvents.CROSSBOW_SHOOT, 1.2F, 0.8F);
            }
            case "SALVE_FEU" -> {
                Vec3 regard = p.getLookAngle();
                for (int i = -2; i <= 2; i++) {
                    Vec3 d = regard.yRot((float) Math.toRadians(i * 9)).normalize();
                    SmallFireball boule = new SmallFireball(n, p, d);
                    boule.setPos(p.getX() + d.x, p.getEyeY() - 0.15, p.getZ() + d.z);
                    n.addFreshEntity(boule);
                }
                n.sendParticles(part, p.getX(), p.getEyeY(), p.getZ(), 30, 0.5, 0.4, 0.5, 0.1);
                Sorts.son(n, p, SoundEvents.BLAZE_SHOOT, 1.0F, 0.6F);
            }
            case "CONE" -> {
                Vec3 o = p.getEyePosition();
                Vec3 regard = p.getLookAngle().normalize();
                for (int k = 1; k <= (int) rayon; k++) {
                    Vec3 q = o.add(regard.scale(k));
                    n.sendParticles(part, q.x, q.y - 0.3, q.z, 6 + k * 2, k * 0.15, 0.3, k * 0.15, 0.02);
                    n.sendParticles(ParticleTypes.LARGE_SMOKE, q.x, q.y, q.z, 2, k * 0.1, 0.2, k * 0.1, 0.01);
                }
                for (LivingEntity e : Sorts.ennemis(p, n, pos, rayon)) {
                    Vec3 vers = e.position().add(0, e.getBbHeight() / 2, 0).subtract(o);
                    if (vers.length() <= rayon && vers.normalize().dot(regard) > 0.75) {
                        Sorts.blesser(p, n, e, ContenuGenere.CAP_DEGATS[f]);
                        e.igniteForSeconds(6);
                    }
                }
                Sorts.son(n, p, SoundEvents.FIRECHARGE_USE, 1.2F, 0.5F);
            }
            case "ENVOL" -> {
                p.push(0, 1.6, 0);
                p.needsSync = true;
                n.sendParticles(part, pos.x, pos.y, pos.z, 40, 0.6, 0.2, 0.6, 0.05);
                Sorts.son(n, p, SoundEvents.FIRECHARGE_USE, 0.8F, 1.5F);
            }
            case "CHARGE" -> {
                Vec3 d = p.getLookAngle().multiply(1, 0, 1).normalize();
                p.push(d.x * 2.4, 0.35, d.z * 2.4);
                p.needsSync = true;
                Vec3 devant = pos.add(d.scale(3));
                n.sendParticles(part, pos.x, pos.y + 0.5, pos.z, 40, 0.8, 0.3, 0.8, 0.05);
                frapperZone(p, n, f, devant, rayon, true);
                Sorts.son(n, p, SoundEvents.RAVAGER_ROAR, 0.8F, 1.2F);
            }
            case "TELEPORT" -> {
                Vec3 o = p.getEyePosition();
                HitResult h = n.clip(new ClipContext(o, o.add(p.getLookAngle().scale(rayon)), ClipContext.Block.COLLIDER, ClipContext.Fluid.NONE, p));
                Vec3 cible = h.getLocation().subtract(p.getLookAngle().scale(0.8)).subtract(0, p.getEyeHeight() * 0.5, 0);
                for (int essai = 0; essai < 6 && !n.noCollision(p, p.getBoundingBox().move(cible.subtract(p.position()))); essai++) {
                    cible = cible.add(0, 0.5, 0);
                }
                n.sendParticles(part, pos.x, pos.y + 1, pos.z, 50, 0.3, 0.7, 0.3, 0.4);
                p.teleportTo(cible.x, cible.y, cible.z);
                p.resetFallDistance();
                n.sendParticles(ParticleTypes.REVERSE_PORTAL, cible.x, cible.y + 1, cible.z, 50, 0.3, 0.7, 0.3, 0.1);
                Sorts.son(n, p, SoundEvents.ENDERMAN_TELEPORT, 1.0F, 0.8F);
            }
            case "INVOCATION" -> {
                var type = ModEntites.ENTITES.get(ContenuGenere.CAP_INVOCATIONS[f]);
                if (type == null) {
                    return false;
                }
                for (int i = 0; i < 2; i++) {
                    Entity e = type.get().create(n, EntitySpawnReason.MOB_SUMMONED);
                    if (e == null) {
                        continue;
                    }
                    double a = i * Math.PI + p.getYRot();
                    e.setPos(pos.x + Math.cos(a) * 2, pos.y, pos.z + Math.sin(a) * 2);
                    if (p.getTeam() != null) {
                        n.getScoreboard().addPlayerToTeam(e.getScoreboardName(), n.getScoreboard().getPlayerTeam(p.getTeam().getName()));
                    }
                    e.addTag("rm_allie_" + p.getUUID());     // ses victimes comptent pour les quêtes du héros
                    n.addFreshEntity(e);
                    n.sendParticles(part, e.getX(), e.getY() + 1, e.getZ(), 30, 0.4, 0.6, 0.4, 0.05);
                    Sorts.INVOQUES.add(new Sorts.Invoque(n, e.getUUID(), n.getGameTime() + 1800));
                }
                Sorts.son(n, p, SoundEvents.EVOKER_PREPARE_SUMMON, 1.2F, 0.6F);
            }
            default -> {
                return false;
            }
        }
        return true;
    }
}
