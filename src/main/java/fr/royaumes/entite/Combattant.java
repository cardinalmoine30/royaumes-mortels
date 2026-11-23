package fr.royaumes.entite;

import com.geckolib.animatable.GeoEntity;
import com.geckolib.animatable.instance.AnimatableInstanceCache;
import com.geckolib.animatable.manager.AnimatableManager;
import com.geckolib.constant.DefaultAnimations;
import com.geckolib.util.GeckoLibUtil;
import fr.royaumes.Capacite;
import fr.royaumes.ModEntites;
import fr.royaumes.Profil;
import net.minecraft.core.particles.ParticleTypes;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.resources.Identifier;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.world.effect.MobEffectInstance;
import net.minecraft.world.effect.MobEffects;
import net.minecraft.world.entity.Entity;
import net.minecraft.world.entity.EntitySpawnReason;
import net.minecraft.world.entity.EntityType;
import net.minecraft.world.entity.LightningBolt;
import net.minecraft.world.entity.LivingEntity;
import net.minecraft.world.entity.Mob;
import net.minecraft.world.entity.PathfinderMob;
import net.minecraft.world.entity.ai.attributes.AttributeSupplier;
import net.minecraft.world.entity.ai.attributes.Attributes;
import net.minecraft.world.entity.ai.goal.FloatGoal;
import net.minecraft.world.entity.ai.goal.LookAtPlayerGoal;
import net.minecraft.world.entity.ai.goal.MeleeAttackGoal;
import net.minecraft.world.entity.ai.goal.RandomLookAroundGoal;
import net.minecraft.world.entity.ai.goal.WaterAvoidingRandomStrollGoal;
import net.minecraft.world.entity.ai.goal.target.HurtByTargetGoal;
import net.minecraft.world.entity.ai.goal.target.NearestAttackableTargetGoal;
import net.minecraft.world.entity.monster.Enemy;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.level.Level;
import net.minecraft.world.scores.PlayerTeam;
import net.minecraft.world.scores.Scoreboard;

/**
 * Mob de faction ou boss des Royaumes Mortels. Son profil (stats, alliance, capacité)
 * vient de ProfilsGeneres, choisi d'après l'identifiant de son type.
 * Les mobs de Grandes Alliances différentes se battent entre eux.
 */
public class Combattant extends PathfinderMob implements GeoEntity {
    private final AnimatableInstanceCache cache = GeckoLibUtil.createInstanceCache(this);
    private final Profil profil;
    private int recharge = 0;

    public Combattant(EntityType<? extends Combattant> type, Level level) {
        super(type, level);
        this.profil = ModEntites.PROFILS.get(BuiltInRegistries.ENTITY_TYPE.getKey(type).getPath());
        this.xpReward = profil.boss() ? 500 : Math.max(5, (int) (profil.pv() / 4));
    }

    public Profil profil() {
        return profil;
    }

    public static AttributeSupplier.Builder creerAttributs(Profil p) {
        return Mob.createMobAttributes()
                .add(Attributes.MAX_HEALTH, p.pv())
                .add(Attributes.ATTACK_DAMAGE, p.degats())
                .add(Attributes.ARMOR, p.armure())
                .add(Attributes.MOVEMENT_SPEED, p.vitesse())
                .add(Attributes.FOLLOW_RANGE, p.boss() ? 48.0 : 32.0)
                .add(Attributes.KNOCKBACK_RESISTANCE, p.boss() ? 1.0 : Math.min(0.8, p.echelle() * 0.35))
                .add(Attributes.SCALE, p.echelle());
    }

    @Override
    protected void registerGoals() {
        this.goalSelector.addGoal(0, new FloatGoal(this));
        this.goalSelector.addGoal(2, new MeleeAttackGoal(this, 1.15, true));
        this.goalSelector.addGoal(5, new WaterAvoidingRandomStrollGoal(this, 0.8));
        this.goalSelector.addGoal(6, new LookAtPlayerGoal(this, Player.class, 8.0F));
        this.goalSelector.addGoal(7, new RandomLookAroundGoal(this));
        this.targetSelector.addGoal(1, new HurtByTargetGoal(this));
        this.targetSelector.addGoal(2, new NearestAttackableTargetGoal<>(this, Player.class, 10, true, false,
                (cible, niveau) -> joueurEnnemi(cible)));
        this.targetSelector.addGoal(3, new NearestAttackableTargetGoal<>(this, Mob.class, 10, true, false,
                (cible, niveau) -> mobEnnemi(cible)));
    }

    private String equipeDe(LivingEntity e) {
        return e.getTeam() instanceof PlayerTeam t ? t.getName() : "";
    }

    /** L'Ordre ne s'en prend qu'aux joueurs des autres alliances ; les autres attaquent tout joueur hors de leur alliance. */
    private boolean joueurEnnemi(LivingEntity cible) {
        String e = equipeDe(cible);
        if ("rm_ordre".equals(profil.equipe())) {
            return e.startsWith("rm_") && !e.equals(profil.equipe());
        }
        return !e.equals(profil.equipe());
    }

    private boolean mobEnnemi(LivingEntity cible) {
        if (cible instanceof Combattant c) {
            return !c.profil.equipe().equals(profil.equipe());
        }
        String e = equipeDe(cible);
        if (e.startsWith("rm_")) {
            return !e.equals(profil.equipe());
        }
        return "rm_ordre".equals(profil.equipe()) && cible instanceof Enemy;
    }

    @Override
    public void tick() {
        super.tick();
        if (this.level() instanceof ServerLevel niveau) {
            if (this.getTeam() == null && this.tickCount % 20 == 1) {
                Scoreboard sb = niveau.getScoreboard();
                PlayerTeam equipe = sb.getPlayerTeam(profil.equipe());
                if (equipe == null) {
                    equipe = sb.addPlayerTeam(profil.equipe());
                }
                sb.addPlayerToTeam(this.getScoreboardName(), equipe);
            }
            if (recharge > 0) {
                recharge--;
            }
            if (profil.boss() && recharge == 0 && this.getTarget() != null && this.distanceTo(this.getTarget()) < 6.0F) {
                frappeDeZone(niveau);
                recharge = 140;
            }
        }
    }

    /** Boss : onde de choc autour de lui. */
    private void frappeDeZone(ServerLevel niveau) {
        niveau.sendParticles(ParticleTypes.EXPLOSION, this.getX(), this.getY() + 0.5, this.getZ(), 8, 2.5, 0.3, 2.5, 0.0);
        for (LivingEntity e : niveau.getEntitiesOfClass(LivingEntity.class, this.getBoundingBox().inflate(5.0))) {
            if (e != this && (e instanceof Player ? joueurEnnemi(e) : mobEnnemi(e))) {
                e.hurtServer(niveau, this.damageSources().mobAttack(this), profil.degats() * 0.75F);
                e.push((e.getX() - this.getX()) * 0.4, 0.6, (e.getZ() - this.getZ()) * 0.4);
                appliquer(niveau, e);
            }
        }
    }

    @Override
    public boolean doHurtTarget(ServerLevel niveau, Entity cible) {
        boolean touche = super.doHurtTarget(niveau, cible);
        if (touche && cible instanceof LivingEntity vivant && this.getRandom().nextFloat() < 0.25F) {
            appliquer(niveau, vivant);
        }
        return touche;
    }

    private void appliquer(ServerLevel niveau, LivingEntity cible) {
        switch (profil.capacite()) {
            case FOUDRE, FOUDRE_VERTE -> {
                Entity e = BuiltInRegistries.ENTITY_TYPE.getValue(Identifier.withDefaultNamespace("lightning_bolt"))
                        .create(niveau, EntitySpawnReason.TRIGGERED);
                if (e instanceof LightningBolt foudre) {
                    foudre.setPos(cible.getX(), cible.getY(), cible.getZ());
                    foudre.setVisualOnly(true);
                    niveau.addFreshEntity(foudre);
                }
                cible.hurtServer(niveau, this.damageSources().magic(), 4.0F);
            }
            case FEU, FEU_MAGIQUE -> cible.igniteForSeconds(4.0F);
            case POISON -> cible.addEffect(new MobEffectInstance(MobEffects.POISON, 100, 0), this);
            case DRAIN -> {
                cible.addEffect(new MobEffectInstance(MobEffects.WITHER, 60, 0), this);
                this.heal(profil.degats() * 0.5F);
            }
            case SAIGNEE -> cible.hurtServer(niveau, this.damageSources().magic(), 3.0F);
            case LUMIERE -> cible.addEffect(new MobEffectInstance(MobEffects.BLINDNESS, 60, 0), this);
            case WAAAGH -> this.addEffect(new MobEffectInstance(MobEffects.STRENGTH, 100, 0));
            case SEISME -> cible.addEffect(new MobEffectInstance(MobEffects.SLOWNESS, 80, 2), this);
            default -> {
            }
        }
    }

    @Override
    public boolean removeWhenFarAway(double distance) {
        return !profil.boss() && super.removeWhenFarAway(distance);
    }

    // --- GeckoLib ---

    @Override
    public void registerControllers(AnimatableManager.ControllerRegistrar controllers) {
        controllers.add(DefaultAnimations.genericWalkIdleController());
        controllers.add(DefaultAnimations.genericAttackAnimation(DefaultAnimations.ATTACK_SWING));
        controllers.add(DefaultAnimations.genericDeathController());
    }

    @Override
    public AnimatableInstanceCache getAnimatableInstanceCache() {
        return this.cache;
    }
}
