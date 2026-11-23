package fr.royaumes;

import fr.royaumes.entite.Combattant;
import fr.royaumes.entite.Monture;
import java.util.LinkedHashMap;
import java.util.Map;
import net.minecraft.core.registries.Registries;
import net.minecraft.resources.ResourceKey;
import net.minecraft.world.entity.EntityType;
import net.minecraft.world.entity.Mob;
import net.minecraft.world.entity.MobCategory;
import net.minecraft.world.entity.SpawnPlacementTypes;
import net.minecraft.world.level.levelgen.Heightmap;
import net.neoforged.bus.api.IEventBus;
import net.neoforged.neoforge.event.entity.EntityAttributeCreationEvent;
import net.neoforged.neoforge.event.entity.RegisterSpawnPlacementsEvent;
import net.neoforged.neoforge.registries.DeferredHolder;
import net.neoforged.neoforge.registries.DeferredRegister;

/** Enregistre un type de créature par profil de ProfilsGeneres. */
public final class ModEntites {
    public static final DeferredRegister<EntityType<?>> TYPES =
            DeferredRegister.create(Registries.ENTITY_TYPE, RoyaumesMortels.MODID);

    public static final Map<String, Profil> PROFILS = new LinkedHashMap<>();
    public static final Map<String, DeferredHolder<EntityType<?>, EntityType<Combattant>>> ENTITES = new LinkedHashMap<>();
    public static final Map<String, ProfilMonture> PROFILS_MONTURES = new LinkedHashMap<>();
    public static final Map<String, DeferredHolder<EntityType<?>, EntityType<Monture>>> MONTURES = new LinkedHashMap<>();

    static {
        for (Profil p : ProfilsGeneres.TOUS) {
            PROFILS.put(p.id(), p);
            ENTITES.put(p.id(), TYPES.register(p.id(), id -> EntityType.Builder
                    .of(Combattant::new, MobCategory.MONSTER)
                    .sized(p.largeur(), p.hauteur())
                    .clientTrackingRange(p.boss() ? 16 : 10)
                    .build(ResourceKey.create(Registries.ENTITY_TYPE, id))));
        }
        for (ProfilMonture p : MonturesGenerees.TOUTES) {
            PROFILS_MONTURES.put(p.id(), p);
            MONTURES.put(p.id(), TYPES.register(p.id(), id -> {
                EntityType.Builder<Monture> b = EntityType.Builder
                        .of(Monture::new, MobCategory.CREATURE)
                        .sized(p.largeur(), p.hauteur())
                        .passengerAttachments(p.selle())
                        .clientTrackingRange(10)
                        .noLootTable();
                if (p.feu()) {
                    b = b.fireImmune();
                }
                return b.build(ResourceKey.create(Registries.ENTITY_TYPE, id));
            }));
        }
    }

    private ModEntites() {}

    public static void enregistrer(IEventBus modBus) {
        TYPES.register(modBus);
        modBus.addListener(ModEntites::attributs);
        modBus.addListener(ModEntites::placements);
    }

    private static void attributs(EntityAttributeCreationEvent event) {
        ENTITES.forEach((id, type) -> event.put(type.get(), Combattant.creerAttributs(PROFILS.get(id)).build()));
        MONTURES.forEach((id, type) -> event.put(type.get(), Monture.creerAttributs(PROFILS_MONTURES.get(id)).build()));
    }

    private static void placements(RegisterSpawnPlacementsEvent event) {
        ENTITES.values().forEach(type -> event.register(type.get(), SpawnPlacementTypes.ON_GROUND,
                Heightmap.Types.MOTION_BLOCKING_NO_LEAVES, Mob::checkMobSpawnRules,
                RegisterSpawnPlacementsEvent.Operation.REPLACE));
    }
}
