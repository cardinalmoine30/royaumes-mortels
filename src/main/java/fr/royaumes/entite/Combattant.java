package fr.royaumes.entite;

import com.geckolib.animatable.GeoEntity;
import com.geckolib.animatable.instance.AnimatableInstanceCache;
import com.geckolib.animatable.manager.AnimatableManager;
import com.geckolib.animation.AnimationController;
import com.geckolib.animation.object.PlayState;
import com.geckolib.constant.DefaultAnimations;
import com.geckolib.util.GeckoLibUtil;
import fr.royaumes.Capacite;
import fr.royaumes.ModEntites;
import fr.royaumes.Profil;
import fr.royaumes.Special;
import java.util.EnumSet;
import net.minecraft.core.particles.ParticleOptions;
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
import net.minecraft.world.entity.ai.goal.Goal;
import net.minecraft.world.entity.ai.goal.LookAtPlayerGoal;
import net.minecraft.world.entity.ai.goal.MeleeAttackGoal;
import net.minecraft.world.entity.ai.goal.RandomLookAroundGoal;
import net.minecraft.world.entity.ai.goal.WaterAvoidingRandomStrollGoal;
import net.minecraft.world.entity.ai.goal.target.HurtByTargetGoal;
import net.minecraft.world.entity.ai.goal.target.NearestAttackableTargetGoal;
import net.minecraft.world.entity.monster.Enemy;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.level.Level;
import net.minecraft.world.level.levelgen.Heightmap;
import net.minecraft.world.phys.Vec3;
import net.minecraft.world.scores.PlayerTeam;
import net.minecraft.world.scores.Scoreboard;

/**
 * Mob de faction ou boss des Royaumes Mortels. Son profil (stats, alliance, mode de combat,
 * capacités) vient de ProfilsGeneres, choisi d'après l'identifiant de son type.
 * Les mobs de Grandes Alliances différentes se battent entre eux.
 */
public class Combattant extends PathfinderMob implements GeoEntity {
    private final AnimatableInstanceCache cache = GeckoLibUtil.createInstanceCache(this);
    private Profil profil;
    private int rechargeAttaque = 0;
    private int rechargeSpecial = 60;
    private int rechargeOnde = 100;
    private int charge = 0;
    private Vec3 patrouille = null;

    public Combattant(EntityType<? extends Combattant> type, Level level) {
        super(type, level);
        Profil p = profil();
        this.xpReward = p.boss() ? 500 : Math.max(5, (int) (p.pv() / 4));
        if (p.volant()) {
            this.setNoGravity(true);
        }
    }

    /** Profil résolu d'après le type (utilisable dès le constructeur parent). */
    public Profil profil() {
        if (profil == null) {
            profil = ModEntites.PROFILS.get(BuiltInRegistries.ENTITY_TYPE.getKey(this.getType()).getPath());
        }
        return profil;
    }

    public static AttributeSupplier.Builder creerAttributs(Profil p) {
        return Mob.createMobAttributes()
                .add(Attributes.MAX_HEALTH, p.pv())
                .add(Attributes.ATTACK_DAMAGE, p.degats())
                .add(Attributes.ARMOR, p.armure())
                .add(Attributes.MOVEMENT_SPEED, p.vitesse())
                .add(Attributes.FOLLOW_RANGE, p.boss() ? 48.0 : 32.0)
                .add(Attributes.KNOCKBACK_RESISTANCE, p.boss() ? 1.0 : Math.min(0.9, p.echelle() * 0.35))
                .add(Attributes.SCALE, p.echelle());
    }

    @Override
    protected void registerGoals() {
        Profil p = profil();
        if (!p.volant()) {
            this.goalSelector.addGoal(0, new FloatGoal(this));
            if (p.distance()) {
                this.goalSelector.addGoal(2, new GardeDistance());
            } else {
                this.goalSelector.addGoal(2, new MeleeAttackGoal(this, 1.15, true));
            }
            this.goalSelector.addGoal(5, new WaterAvoidingRandomStrollGoal(this, 0.8));
        }
        this.goalSelector.addGoal(6, new LookAtPlayerGoal(this, Player.class, 8.0F));
        this.goalSelector.addGoal(7, new RandomLookAroundGoal(this));
        this.targetSelector.addGoal(1, new HurtByTargetGoal(this));
        this.targetSelector.addGoal(2, new NearestAttackableTargetGoal<>(this, Player.class, 10, !p.volant(), false,
                (cible, niveau) -> joueurEnnemi(cible)));
        this.targetSelector.addGoal(3, new NearestAttackableTargetGoal<>(this, Mob.class, 10, !p.volant(), false,
                (cible, niveau) -> mobEnnemi(cible)));
    }

    private String equipeDe(LivingEntity e) {
        return e.getTeam() instanceof PlayerTeam t ? t.getName() : "";
    }

    /** L'Ordre ne s'en prend qu'aux joueurs des autres alliances ; les autres attaquent tout joueur hors de leur alliance. */
    private boolean joueurEnnemi(LivingEntity cible) {
        String e = equipeDe(cible);
        if ("rm_ordre".equals(profil().equipe())) {
            return e.startsWith("rm_") && !e.equals(profil().equipe());
        }
        return !e.equals(profil().equipe());
    }

    private boolean mobEnnemi(LivingEntity cible) {
        if (cible instanceof Combattant c) {
            return !c.profil().equipe().equals(profil().equipe());
        }
        String e = equipeDe(cible);
        if (e.startsWith("rm_")) {
            return !e.equals(profil().equipe());
        }
        return "rm_ordre".equals(profil().equipe()) && cible instanceof Enemy;
    }

    private boolean ennemi(LivingEntity e) {
        return e != this && e.isAlive() && (e instanceof Player ? joueurEnnemi(e) : mobEnnemi(e));
    }

    // ------------------------------------------------------------------ boucle principale

    @Override
    public void tick() {
        super.tick();
        if (!(this.level() instanceof ServerLevel niveau)) {
            return;
        }
        Profil p = profil();
        if (this.getTeam() == null && this.tickCount % 20 == 1) {
            Scoreboard sb = niveau.getScoreboard();
            PlayerTeam equipe = sb.getPlayerTeam(p.equipe());
            if (equipe == null) {
                equipe = sb.addPlayerTeam(p.equipe());
            }
            sb.addPlayerToTeam(this.getScoreboardName(), equipe);
        }
        if (rechargeAttaque > 0) rechargeAttaque--;
        if (rechargeSpecial > 0) rechargeSpecial--;
        if (rechargeOnde > 0) rechargeOnde--;
        LivingEntity cible = this.getTarget();
        if (cible != null && !cible.isAlive()) {
            cible = null;
        }
        if (p.volant()) {
            voler(niveau, cible);
            this.fallDistance = 0;
        }
        if (cible != null && p.distance() && rechargeAttaque == 0) {
            double d = this.distanceTo(cible);
            if (d < 24 && this.getSensing().hasLineOfSight(cible)) {
                tirer(niveau, cible);
                rechargeAttaque = p.magique() ? 50 : 40;
            }
        }
        if (p.boss() || p.special() == Special.ONDE) {
            if (rechargeOnde == 0 && cible != null && this.distanceTo(cible) < 4 + p.echelle() * 1.5) {
                frappeDeZone(niveau);
                rechargeOnde = p.boss() ? 140 : 200;
            }
        }
        special(niveau, p, cible);
    }

    // ------------------------------------------------------------------ vol

    private void voler(ServerLevel niveau, LivingEntity cible) {
        Profil p = profil();
        Vec3 but;
        if (cible != null) {
            double h = p.distance() ? 7.0 : cible.getBbHeight() * 0.5;
            but = cible.position().add(0, h, 0);
            if (!p.distance() && rechargeAttaque == 0 && this.distanceToSqr(cible) < Math.pow(this.getBbWidth() + cible.getBbWidth() + 1.5, 2)) {
                this.triggerAnim("Coups", "attaque");
                this.doHurtTarget(niveau, cible);
                rechargeAttaque = 20;
            }
        } else {
            if (patrouille == null || this.position().distanceToSqr(patrouille) < 4 || this.tickCount % 200 == 0) {
                double x = this.getX() + (this.getRandom().nextDouble() - 0.5) * 32;
                double z = this.getZ() + (this.getRandom().nextDouble() - 0.5) * 32;
                int sol = niveau.getHeight(Heightmap.Types.MOTION_BLOCKING, (int) x, (int) z);
                patrouille = new Vec3(x, sol + 6 + this.getRandom().nextInt(8), z);
            }
            but = patrouille;
        }
        Vec3 dir = but.subtract(this.position());
        double d = dir.length();
        double v = Math.max(0.15, p.vitesse() * 1.3);
        Vec3 mv = d > 0.6 ? dir.scale(v / d) : Vec3.ZERO;
        this.setDeltaMovement(this.getDeltaMovement().scale(0.75).add(mv.scale(0.25)));
        if (d > 0.6) {
            float lacet = (float) (Math.atan2(dir.z, dir.x) * 180.0 / Math.PI) - 90.0F;
            this.setYRot(lacet);
            this.yBodyRot = lacet;
            this.yHeadRot = lacet;
        }
    }

    // ------------------------------------------------------------------ attaques à distance

    private void tirer(ServerLevel niveau, LivingEntity cible) {
        Profil p = profil();
        this.triggerAnim("Coups", "attaque");
        Vec3 a = this.getEyePosition();
        Vec3 b = cible.getEyePosition();
        ParticleOptions trace = p.magique() ? particuleMagie() : ParticleTypes.CRIT;
        Vec3 pas = b.subtract(a);
        int n = (int) Math.max(4, pas.length() * 2);
        for (int i = 0; i <= n; i++) {
            Vec3 q = a.add(pas.scale(i / (double) n));
            niveau.sendParticles(trace, q.x, q.y, q.z, 1, 0.02, 0.02, 0.02, 0.0);
        }
        niveau.sendParticles(p.magique() ? trace : ParticleTypes.SMOKE, b.x, b.y, b.z, 6, 0.2, 0.2, 0.2, 0.02);
        cible.hurtServer(niveau, p.magique() ? this.damageSources().indirectMagic(this, this) : this.damageSources().mobAttack(this), p.degats());
        if (this.getRandom().nextFloat() < 0.35F) {
            appliquer(niveau, cible);
        }
    }

    private ParticleOptions particuleMagie() {
        return switch (profil().capacite()) {
            case FEU -> ParticleTypes.FLAME;
            case FEU_MAGIQUE -> ParticleTypes.SOUL_FIRE_FLAME;
            case FOUDRE, FOUDRE_VERTE -> ParticleTypes.ELECTRIC_SPARK;
            case POISON -> ParticleTypes.ITEM_SLIME;
            case DRAIN -> ParticleTypes.SOUL;
            case LUMIERE -> ParticleTypes.END_ROD;
            case SEISME -> ParticleTypes.SNOWFLAKE;
            default -> ParticleTypes.WITCH;
        };
    }

    // ------------------------------------------------------------------ capacités spéciales

    private void special(ServerLevel niveau, Profil p, LivingEntity cible) {
        switch (p.special()) {
            case REGEN -> {
                if (this.tickCount % 20 == 0 && this.getHealth() < this.getMaxHealth()) {
                    this.heal(Math.max(1.0F, p.pv() * 0.01F));
                }
            }
            case AURA_PESTE -> {
                if (this.tickCount % 40 == 0) {
                    niveau.sendParticles(ParticleTypes.ITEM_SLIME, this.getX(), this.getY() + 1, this.getZ(), 10, 2.5, 0.5, 2.5, 0.0);
                    for (LivingEntity e : niveau.getEntitiesOfClass(LivingEntity.class, this.getBoundingBox().inflate(5.0))) {
                        if (ennemi(e)) e.addEffect(new MobEffectInstance(MobEffects.POISON, 80, 0), this);
                    }
                }
            }
            case AURA_BUFF -> {
                if (this.tickCount % 60 == 0) {
                    for (Combattant c : niveau.getEntitiesOfClass(Combattant.class, this.getBoundingBox().inflate(10.0))) {
                        if (c.profil().equipe().equals(p.equipe())) {
                            c.addEffect(new MobEffectInstance(MobEffects.STRENGTH, 100, 0));
                            c.addEffect(new MobEffectInstance(MobEffects.RESISTANCE, 100, 0));
                        }
                    }
                    niveau.sendParticles(ParticleTypes.ENCHANT, this.getX(), this.getY() + 2, this.getZ(), 30, 3, 1, 3, 0.5);
                }
            }
            case CHARGE -> {
                if (charge > 0) {
                    charge--;
                    if (cible != null && this.distanceTo(cible) < this.getBbWidth() + 2.0F) {
                        cible.hurtServer(niveau, this.damageSources().mobAttack(this), p.degats() * 1.3F);
                        cible.push((cible.getX() - this.getX()) * 0.5, 0.5, (cible.getZ() - this.getZ()) * 0.5);
                        charge = 0;
                    }
                } else if (cible != null && rechargeSpecial == 0 && this.onGround()) {
                    double d = this.distanceTo(cible);
                    if (d > 5 && d < 16) {
                        Vec3 dir = cible.position().subtract(this.position()).normalize();
                        this.setDeltaMovement(dir.x * 1.4, 0.3, dir.z * 1.4);
                        niveau.sendParticles(ParticleTypes.CLOUD, this.getX(), this.getY(), this.getZ(), 12, 0.5, 0.1, 0.5, 0.05);
                        charge = 12;
                        rechargeSpecial = 100;
                    }
                }
            }
            case SAUT -> {
                this.fallDistance = 0;
                if (cible != null && rechargeSpecial == 0 && this.onGround() && this.distanceTo(cible) < 12) {
                    Vec3 dir = cible.position().subtract(this.position());
                    this.setDeltaMovement(dir.x * 0.12, 0.75, dir.z * 0.12);
                    rechargeSpecial = 40;
                }
            }
            case INVOQUE -> {
                if (cible != null && rechargeSpecial == 0 && !p.sbire().isEmpty()) {
                    invoquer(niveau, 2);
                    rechargeSpecial = 300;
                }
            }
            default -> {
            }
        }
        if (p.boss() && !p.sbire().isEmpty() && cible != null && this.tickCount % 400 == 0) {
            invoquer(niveau, 3);
        }
    }

    private void invoquer(ServerLevel niveau, int nombre) {
        EntityType<?> type = BuiltInRegistries.ENTITY_TYPE.getValue(Identifier.fromNamespaceAndPath("royaumes", profil().sbire()));
        long deja = niveau.getEntitiesOfClass(Combattant.class, this.getBoundingBox().inflate(16.0),
                c -> c.getType() == type).size();
        for (int i = 0; i < nombre && deja + i < 6; i++) {
            Entity e = type.create(niveau, EntitySpawnReason.MOB_SUMMONED);
            if (e != null) {
                e.setPos(this.getX() + this.getRandom().nextInt(7) - 3, this.getY(), this.getZ() + this.getRandom().nextInt(7) - 3);
                niveau.addFreshEntity(e);
                niveau.sendParticles(ParticleTypes.POOF, e.getX(), e.getY() + 1, e.getZ(), 12, 0.4, 0.6, 0.4, 0.02);
            }
        }
    }

    /** Onde de choc autour du mob (boss et grandes créatures). */
    private void frappeDeZone(ServerLevel niveau) {
        Profil p = profil();
        double r = 3.5 + p.echelle() * 1.5;
        niveau.sendParticles(ParticleTypes.EXPLOSION, this.getX(), this.getY() + 0.5, this.getZ(), 8, r / 2, 0.3, r / 2, 0.0);
        for (LivingEntity e : niveau.getEntitiesOfClass(LivingEntity.class, this.getBoundingBox().inflate(r))) {
            if (ennemi(e)) {
                e.hurtServer(niveau, this.damageSources().mobAttack(this), p.degats() * 0.75F);
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
        switch (profil().capacite()) {
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
                this.heal(profil().degats() * 0.5F);
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
        return !profil().boss() && super.removeWhenFarAway(distance);
    }

    /** Tireurs et mages : se placent à bonne distance de leur cible. */
    private class GardeDistance extends Goal {
        GardeDistance() {
            this.setFlags(EnumSet.of(Goal.Flag.MOVE, Goal.Flag.LOOK));
        }

        @Override
        public boolean canUse() {
            LivingEntity t = Combattant.this.getTarget();
            return t != null && t.isAlive();
        }

        @Override
        public boolean requiresUpdateEveryTick() {
            return true;
        }

        @Override
        public void tick() {
            LivingEntity t = Combattant.this.getTarget();
            if (t == null) return;
            Combattant.this.getLookControl().setLookAt(t, 30.0F, 30.0F);
            double d = Combattant.this.distanceTo(t);
            boolean voit = Combattant.this.getSensing().hasLineOfSight(t);
            if (d > 14 || !voit) {
                Combattant.this.getNavigation().moveTo(t, 1.0);
            } else if (d < 5) {
                Vec3 fuite = Combattant.this.position().add(Combattant.this.position().subtract(t.position()).normalize().scale(6));
                Combattant.this.getNavigation().moveTo(fuite.x, fuite.y, fuite.z, 1.1);
            } else {
                Combattant.this.getNavigation().stop();
            }
        }
    }

    // ------------------------------------------------------------------ GeckoLib

    @Override
    public void registerControllers(AnimatableManager.ControllerRegistrar controllers) {
        controllers.add(DefaultAnimations.genericWalkIdleController());
        controllers.add(DefaultAnimations.genericAttackAnimation(DefaultAnimations.ATTACK_SWING));
        controllers.add(DefaultAnimations.genericDeathController());
        controllers.add(new AnimationController<>("Coups", etat -> PlayState.STOP)
                .triggerableAnim("attaque", DefaultAnimations.ATTACK_SWING));
    }

    @Override
    public AnimatableInstanceCache getAnimatableInstanceCache() {
        return this.cache;
    }
}
