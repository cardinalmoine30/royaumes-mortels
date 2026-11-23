package fr.royaumes;

import fr.royaumes.entite.Liberator;
import net.minecraft.core.registries.Registries;
import net.minecraft.resources.ResourceKey;
import net.minecraft.world.entity.EntityType;
import net.minecraft.world.entity.MobCategory;
import net.neoforged.bus.api.IEventBus;
import net.neoforged.neoforge.event.entity.EntityAttributeCreationEvent;
import net.neoforged.neoforge.registries.DeferredHolder;
import net.neoforged.neoforge.registries.DeferredRegister;

/** Créatures du mod. */
public final class ModEntites {
    public static final DeferredRegister<EntityType<?>> TYPES =
            DeferredRegister.create(Registries.ENTITY_TYPE, RoyaumesMortels.MODID);

    public static final DeferredHolder<EntityType<?>, EntityType<Liberator>> LIBERATOR = TYPES.register("liberator",
            id -> EntityType.Builder.of(Liberator::new, MobCategory.MONSTER)
                    .sized(0.8F, 2.4F)
                    .eyeHeight(2.1F)
                    .clientTrackingRange(10)
                    .build(ResourceKey.create(Registries.ENTITY_TYPE, id)));

    private ModEntites() {}

    public static void enregistrer(IEventBus modBus) {
        TYPES.register(modBus);
        modBus.addListener(ModEntites::attributs);
    }

    private static void attributs(EntityAttributeCreationEvent event) {
        event.put(LIBERATOR.get(), Liberator.creerAttributs().build());
    }
}
