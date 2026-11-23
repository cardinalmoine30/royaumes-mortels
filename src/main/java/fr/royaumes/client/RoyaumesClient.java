package fr.royaumes.client;

import com.geckolib.renderer.GeoEntityRenderer;
import fr.royaumes.ModEntites;
import fr.royaumes.RoyaumesMortels;
import fr.royaumes.entite.Liberator;
import net.minecraft.client.renderer.entity.state.LivingEntityRenderState;
import net.neoforged.api.distmarker.Dist;
import net.neoforged.bus.api.SubscribeEvent;
import net.neoforged.fml.common.EventBusSubscriber;
import net.neoforged.neoforge.client.event.EntityRenderersEvent;

/** Partie client : rendus des créatures (GeckoLib). */
@EventBusSubscriber(modid = RoyaumesMortels.MODID, value = Dist.CLIENT)
public final class RoyaumesClient {
    private RoyaumesClient() {}

    @SubscribeEvent
    static void rendus(EntityRenderersEvent.RegisterRenderers event) {
        event.registerEntityRenderer(ModEntites.LIBERATOR.get(),
                ctx -> new GeoEntityRenderer<Liberator, LivingEntityRenderState>(ctx, ModEntites.LIBERATOR.get()));
    }
}
