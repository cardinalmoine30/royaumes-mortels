package fr.royaumes.client;

import com.geckolib.renderer.GeoEntityRenderer;
import fr.royaumes.ModEntites;
import fr.royaumes.RoyaumesMortels;
import fr.royaumes.entite.Combattant;
import net.minecraft.client.renderer.entity.state.LivingEntityRenderState;
import net.neoforged.api.distmarker.Dist;
import net.neoforged.bus.api.SubscribeEvent;
import net.neoforged.fml.common.EventBusSubscriber;
import net.neoforged.neoforge.client.event.EntityRenderersEvent;

/** Partie client : rendus GeckoLib de toutes les créatures du mod. */
@EventBusSubscriber(modid = RoyaumesMortels.MODID, value = Dist.CLIENT)
public final class RoyaumesClient {
    private RoyaumesClient() {}

    @SubscribeEvent
    static void rendus(EntityRenderersEvent.RegisterRenderers event) {
        ModEntites.ENTITES.values().forEach(type -> event.registerEntityRenderer(type.get(),
                ctx -> new GeoEntityRenderer<Combattant, LivingEntityRenderState>(ctx, type.get())));
    }
}
