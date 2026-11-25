package fr.royaumes.client;

import com.geckolib.renderer.GeoEntityRenderer;
import com.geckolib.renderer.layer.GeoRenderLayer;
import com.geckolib.renderer.layer.builtin.AutoGlowingGeoLayer;
import fr.royaumes.ModEntites;
import fr.royaumes.RoyaumesMortels;
import fr.royaumes.entite.Combattant;
import fr.royaumes.entite.Monture;
import net.minecraft.client.renderer.entity.EntityRendererProvider;
import net.minecraft.client.renderer.entity.state.LivingEntityRenderState;
import net.minecraft.world.entity.EntityType;
import net.neoforged.api.distmarker.Dist;
import net.neoforged.bus.api.SubscribeEvent;
import net.neoforged.fml.common.EventBusSubscriber;
import net.neoforged.neoforge.client.event.EntityRenderersEvent;

/** Partie client : rendus GeckoLib de toutes les créatures du mod (yeux, runes et malepierre lumineux). */
@EventBusSubscriber(modid = RoyaumesMortels.MODID, value = Dist.CLIENT)
public final class RoyaumesClient {
    private RoyaumesClient() {}

    @SubscribeEvent
    static void ecrans(net.neoforged.neoforge.client.event.RegisterMenuScreensEvent event) {
        event.register(fr.royaumes.camp.Stockage.TYPE.get(), EcranStockage::new);
    }

    @SubscribeEvent
    static void rendus(EntityRenderersEvent.RegisterRenderers event) {
        ModEntites.ENTITES.values().forEach(type -> event.registerEntityRenderer(type.get(), ctx -> rendu(ctx, type.get())));
        ModEntites.MONTURES.values().forEach(type -> event.registerEntityRenderer(type.get(), ctx -> renduMonture(ctx, type.get())));
    }

    @SuppressWarnings({"unchecked", "rawtypes"})
    private static GeoEntityRenderer<Monture, LivingEntityRenderState> renduMonture(EntityRendererProvider.Context ctx, EntityType<Monture> type) {
        GeoEntityRenderer<Monture, LivingEntityRenderState> r = new GeoEntityRenderer<>(ctx, type);
        r.withRenderLayer((GeoRenderLayer) new AutoGlowingGeoLayer(r));
        return r;
    }

    /** Rendu GeckoLib + couche lumineuse (texture *_glowmask.png). */
    @SuppressWarnings({"unchecked", "rawtypes"})
    private static GeoEntityRenderer<Combattant, LivingEntityRenderState> rendu(EntityRendererProvider.Context ctx, EntityType<Combattant> type) {
        GeoEntityRenderer<Combattant, LivingEntityRenderState> r = new GeoEntityRenderer<>(ctx, type);
        r.withRenderLayer((GeoRenderLayer) new AutoGlowingGeoLayer(r));
        return r;
    }
}
