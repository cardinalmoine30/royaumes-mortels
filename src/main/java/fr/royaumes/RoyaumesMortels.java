package fr.royaumes;

import com.mojang.logging.LogUtils;
import net.neoforged.bus.api.IEventBus;
import net.neoforged.bus.api.SubscribeEvent;
import net.neoforged.fml.ModContainer;
import net.neoforged.fml.common.Mod;
import net.neoforged.fml.event.lifecycle.FMLCommonSetupEvent;
import net.neoforged.neoforge.common.NeoForge;
import net.neoforged.neoforge.event.server.ServerStartedEvent;
import org.slf4j.Logger;

/** Point d'entrée du mod Royaumes Mortels (Warhammer Age of Sigmar). */
@Mod(RoyaumesMortels.MODID)
public class RoyaumesMortels {
    public static final String MODID = "royaumes";
    public static final Logger LOGGER = LogUtils.getLogger();

    public RoyaumesMortels(IEventBus modBus, ModContainer container) {
        modBus.addListener(this::commonSetup);
        ModEntites.enregistrer(modBus);
        ModObjets.enregistrer(modBus);
        modBus.addListener(fr.royaumes.reseau.Reseau::enregistrer);
        NeoForge.EVENT_BUS.addListener(fr.royaumes.reseau.Reseau::tickServeur);
        NeoForge.EVENT_BUS.addListener(fr.royaumes.camp.EvenementsCamp::tickEntite);
        NeoForge.EVENT_BUS.addListener(fr.royaumes.camp.EvenementsCamp::mort);
        NeoForge.EVENT_BUS.addListener(fr.royaumes.camp.EvenementsCamp::degats);
        NeoForge.EVENT_BUS.addListener(fr.royaumes.rpg.Voies::degats);
        NeoForge.EVENT_BUS.addListener(fr.royaumes.arsenal.PouvoirsOutils::casser);
        NeoForge.EVENT_BUS.register(this);
    }

    private void commonSetup(FMLCommonSetupEvent event) {
        LOGGER.info("[Royaumes Mortels] Initialisation du mod");
    }

    @SubscribeEvent
    public void onServerStarted(ServerStartedEvent event) {
        // Repère lu par le serveur de test sur GitHub Actions.
        LOGGER.info("ROYAUMES_OK serveur demarre avec le mod Royaumes Mortels");
    }
}
