package fr.royaumes.entite;

import com.geckolib.animatable.GeoEntity;
import com.geckolib.animatable.instance.AnimatableInstanceCache;
import com.geckolib.animatable.manager.AnimatableManager;
import com.geckolib.constant.DefaultAnimations;
import com.geckolib.util.GeckoLibUtil;
import fr.royaumes.ModEntites;
import fr.royaumes.ProfilMonture;
import net.minecraft.core.particles.ParticleTypes;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.world.InteractionHand;
import net.minecraft.world.InteractionResult;
import net.minecraft.world.damagesource.DamageSource;
import net.minecraft.world.entity.EntityType;
import net.minecraft.world.entity.LivingEntity;
import net.minecraft.world.entity.Mob;
import net.minecraft.world.entity.PathfinderMob;
import net.minecraft.world.entity.PlayerRideableJumping;
import net.minecraft.world.entity.ai.attributes.AttributeSupplier;
import net.minecraft.world.entity.ai.attributes.Attributes;
import net.minecraft.world.entity.ai.goal.FloatGoal;
import net.minecraft.world.entity.ai.goal.LookAtPlayerGoal;
import net.minecraft.world.entity.ai.goal.RandomLookAroundGoal;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.level.Level;
import net.minecraft.world.phys.Vec3;

/**
 * Monture de faction d'un joueur : pilotable, saute (barre de saut comme un cheval), vole pour certaines
 * (le regard du cavalier règle l'altitude), bondit pour les squigs, ignore les chutes.
 */
public class Monture extends PathfinderMob implements GeoEntity, PlayerRideableJumping {
    private final AnimatableInstanceCache cache = GeckoLibUtil.createInstanceCache(this);
    private ProfilMonture profil;
    private float sautEnAttente = 0;

    public Monture(EntityType<? extends Monture> type, Level level) {
        super(type, level);
        this.setPersistenceRequired();
    }

    public ProfilMonture profil() {
        if (profil == null) {
            profil = ModEntites.PROFILS_MONTURES.get(BuiltInRegistries.ENTITY_TYPE.getKey(this.getType()).getPath());
        }
        return profil;
    }

    public static AttributeSupplier.Builder creerAttributs(ProfilMonture p) {
        return Mob.createMobAttributes()
                .add(Attributes.MAX_HEALTH, p.pv())
                .add(Attributes.MOVEMENT_SPEED, p.vitesse())
                .add(Attributes.ARMOR, 4.0)
                .add(Attributes.STEP_HEIGHT, 1.1)
                .add(Attributes.SAFE_FALL_DISTANCE, 64.0)
                .add(Attributes.JUMP_STRENGTH, p.saut() ? 0.9 : 0.75)
                .add(Attributes.FOLLOW_RANGE, 16.0);
    }

    @Override
    protected void registerGoals() {
        this.goalSelector.addGoal(0, new FloatGoal(this));
        this.goalSelector.addGoal(6, new LookAtPlayerGoal(this, Player.class, 8.0F));
        this.goalSelector.addGoal(7, new RandomLookAroundGoal(this));
    }

    // ------------------------------------------------------------------ monter en selle
    @Override
    protected InteractionResult mobInteract(Player joueur, InteractionHand main) {
        if (this.isVehicle() || joueur.isSecondaryUseActive()) {
            return super.mobInteract(joueur, main);
        }
        if (this.level() instanceof ServerLevel) {
            joueur.startRiding(this);
        }
        return InteractionResult.SUCCESS;
    }

    @Override
    public LivingEntity getControllingPassenger() {
        if (this.getFirstPassenger() instanceof Player joueur) {
            return joueur;
        }
        return super.getControllingPassenger();
    }

    // ------------------------------------------------------------------ pilotage
    @Override
    protected void tickRidden(Player joueur, Vec3 entree) {
        super.tickRidden(joueur, entree);
        this.setRot(joueur.getYRot(), joueur.getXRot() * 0.5F);
        this.yRotO = this.getYRot();
        this.yBodyRot = this.getYRot();
        this.yHeadRot = this.getYRot();
        ProfilMonture p = profil();
        Vec3 dm = this.getDeltaMovement();
        if (p.vol()) {
            this.setNoGravity(true);
            double vy = dm.y * 0.6;
            if (joueur.zza > 0) {
                vy = -Math.sin(Math.toRadians(joueur.getXRot())) * p.vitesse() * 1.8;
            }
            if (this.sautEnAttente > 0) {
                vy = 0.5 + 0.3 * this.sautEnAttente;
                this.sautEnAttente = 0;
            }
            this.setDeltaMovement(dm.x, vy, dm.z);
        } else if (this.onGround()) {
            if (this.sautEnAttente > 0) {
                double force = this.getAttributeValue(Attributes.JUMP_STRENGTH) * this.sautEnAttente;
                this.setDeltaMovement(dm.x, force, dm.z);
                this.sautEnAttente = 0;
            } else if (p.saut() && (joueur.zza != 0 || joueur.xxa != 0)) {
                this.setDeltaMovement(dm.x, 0.42, dm.z);   // les squigs avancent par bonds
            }
        }
    }

    @Override
    protected Vec3 getRiddenInput(Player joueur, Vec3 entree) {
        float lateral = joueur.xxa * 0.5F;
        float avant = joueur.zza;
        if (avant <= 0) {
            avant *= 0.25F;
        }
        return new Vec3(lateral, 0, avant);
    }

    @Override
    protected float getRiddenSpeed(Player joueur) {
        float v = (float) this.getAttributeValue(Attributes.MOVEMENT_SPEED);
        return profil().vol() && !this.onGround() ? v * 1.5F : v;
    }

    @Override
    protected float getFlyingSpeed() {
        if (this.getControllingPassenger() != null) {
            return this.getSpeed() * (profil().vol() ? 0.15F : 0.1F);
        }
        return super.getFlyingSpeed();
    }

    @Override
    public void tick() {
        super.tick();
        ProfilMonture p = profil();
        if (p.vol() && !this.isVehicle() && this.isNoGravity()) {
            this.setNoGravity(false);
        }
        if (p.vol() && this.isVehicle() && !this.onGround() && this.level() instanceof ServerLevel niveau && this.tickCount % 4 == 0) {
            niveau.sendParticles(p.feu() ? ParticleTypes.FLAME : ParticleTypes.CLOUD,
                    this.getX(), this.getY() + 0.2, this.getZ(), 1, 0.3, 0.1, 0.3, 0.01);
        }
    }

    @Override
    public boolean causeFallDamage(double distance, float multiplicateur, DamageSource source) {
        return false;   // les montures amortissent toutes les chutes, cavalier compris
    }

    @Override
    public boolean removeWhenFarAway(double distance) {
        return false;
    }

    // ------------------------------------------------------------------ saut (barre de saut du cavalier)
    @Override
    public void onPlayerJump(int puissance) {
        this.sautEnAttente = puissance >= 90 ? 1.0F : 0.4F + 0.6F * puissance / 90.0F;
    }

    @Override
    public boolean canJump() {
        return true;
    }

    @Override
    public void handleStartJump(int puissance) {
    }

    @Override
    public void handleStopJump() {
    }

    // ------------------------------------------------------------------ animations GeckoLib
    @Override
    public void registerControllers(AnimatableManager.ControllerRegistrar controllers) {
        controllers.add(DefaultAnimations.genericWalkIdleController());
        controllers.add(DefaultAnimations.genericDeathController());
    }

    @Override
    public AnimatableInstanceCache getAnimatableInstanceCache() {
        return this.cache;
    }
}
