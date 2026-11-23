package fr.royaumes.entite;

import com.geckolib.animatable.GeoEntity;
import com.geckolib.animatable.instance.AnimatableInstanceCache;
import com.geckolib.animatable.manager.AnimatableManager;
import com.geckolib.constant.DefaultAnimations;
import com.geckolib.util.GeckoLibUtil;
import net.minecraft.server.level.ServerLevel;
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
 * Liberator des Stormcast Eternals (Ordre).
 * Combat au marteau ; un coup sur cinq appelle la foudre de Sigmar.
 * Rejoint l'équipe « rm_ordre » du datapack : allié des joueurs de l'Ordre, ennemi des autres alliances.
 */
public class Liberator extends PathfinderMob implements GeoEntity {
    public static final String EQUIPE = "rm_ordre";
    private final AnimatableInstanceCache cache = GeckoLibUtil.createInstanceCache(this);

    public Liberator(EntityType<? extends Liberator> type, Level level) {
        super(type, level);
        this.xpReward = 12;
    }

    public static AttributeSupplier.Builder creerAttributs() {
        return Mob.createMobAttributes()
                .add(Attributes.MAX_HEALTH, 40.0)
                .add(Attributes.ATTACK_DAMAGE, 6.0)
                .add(Attributes.ARMOR, 8.0)
                .add(Attributes.MOVEMENT_SPEED, 0.27)
                .add(Attributes.FOLLOW_RANGE, 32.0)
                .add(Attributes.KNOCKBACK_RESISTANCE, 0.5);
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
                (cible, niveau) -> estEnnemi(cible)));
        this.targetSelector.addGoal(3, new NearestAttackableTargetGoal<>(this, Mob.class, 10, true, false,
                (cible, niveau) -> cible instanceof Enemy && estEnnemi(cible)));
    }

    /** Ennemi = membre d'une autre Grande Alliance (les joueurs sans faction sont laissés tranquilles). */
    private boolean estEnnemi(LivingEntity cible) {
        PlayerTeam equipe = cible.getTeam() instanceof PlayerTeam t ? t : null;
        if (cible instanceof Player) {
            return equipe != null && equipe.getName().startsWith("rm_") && !EQUIPE.equals(equipe.getName());
        }
        return equipe == null || !EQUIPE.equals(equipe.getName());
    }

    @Override
    public void tick() {
        super.tick();
        if (!this.level().isClientSide() && this.getTeam() == null && this.tickCount % 20 == 1) {
            Scoreboard sb = this.level().getScoreboard();
            PlayerTeam equipe = sb.getPlayerTeam(EQUIPE);
            if (equipe != null) {
                sb.addPlayerToTeam(this.getScoreboardName(), equipe);
            }
        }
    }

    @Override
    public boolean doHurtTarget(ServerLevel niveau, Entity cible) {
        boolean touche = super.doHurtTarget(niveau, cible);
        if (touche && this.getRandom().nextFloat() < 0.2F) {
            LightningBolt foudre = EntityType.LIGHTNING_BOLT.create(niveau, EntitySpawnReason.TRIGGERED);
            if (foudre != null) {
                foudre.setPos(cible.getX(), cible.getY(), cible.getZ());
                foudre.setVisualOnly(true);
                niveau.addFreshEntity(foudre);
                cible.hurtServer(niveau, this.damageSources().lightningBolt(), 4.0F);
            }
        }
        return touche;
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
