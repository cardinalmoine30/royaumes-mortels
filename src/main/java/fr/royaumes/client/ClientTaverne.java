package fr.royaumes.client;

import fr.royaumes.RoyaumesMortels;
import net.minecraft.client.Minecraft;
import net.minecraft.client.gui.screens.inventory.InventoryScreen;
import net.neoforged.api.distmarker.Dist;
import net.neoforged.bus.api.SubscribeEvent;
import net.neoforged.fml.common.EventBusSubscriber;
import net.neoforged.neoforge.client.event.ScreenEvent;

/** Remplace l'inventaire de survie par l'inventaire « table de taverne ». */
@EventBusSubscriber(modid = RoyaumesMortels.MODID, value = Dist.CLIENT)
public final class ClientTaverne {
    private ClientTaverne() {}

    @SubscribeEvent
    static void ouverture(ScreenEvent.Opening event) {
        if (event.getNewScreen() instanceof InventoryScreen && !(event.getNewScreen() instanceof EcranTaverne)) {
            Minecraft mc = Minecraft.getInstance();
            if (mc.player != null) {
                event.setNewScreen(new EcranTaverne(mc.player));
            }
        }
    }
}
