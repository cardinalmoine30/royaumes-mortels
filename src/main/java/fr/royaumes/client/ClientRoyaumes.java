package fr.royaumes.client;

import fr.royaumes.RoyaumesMortels;
import fr.royaumes.reseau.BonjourModde;
import fr.royaumes.reseau.DonneesHeros;
import fr.royaumes.reseau.FicheHeros;
import fr.royaumes.reseau.UtiliserCapacite;
import net.minecraft.client.KeyMapping;
import net.minecraft.client.Minecraft;
import net.minecraft.client.multiplayer.ClientPacketListener;
import net.minecraft.network.protocol.common.ServerboundCustomPayloadPacket;
import net.minecraft.resources.Identifier;
import net.neoforged.api.distmarker.Dist;
import net.neoforged.bus.api.SubscribeEvent;
import net.neoforged.fml.common.EventBusSubscriber;
import net.neoforged.neoforge.client.event.ClientPlayerNetworkEvent;
import net.neoforged.neoforge.client.event.ClientTickEvent;
import net.neoforged.neoforge.client.event.RegisterGuiLayersEvent;
import net.neoforged.neoforge.client.event.RegisterKeyMappingsEvent;

/** Client : touche J (écran de serment), HUD des Royaumes, poignée de main « j'ai le mod », skins de faction. */
@EventBusSubscriber(modid = RoyaumesMortels.MODID, value = Dist.CLIENT)
public final class ClientRoyaumes {
    static final KeyMapping.Category CATEGORIE = new KeyMapping.Category(Identifier.fromNamespaceAndPath(RoyaumesMortels.MODID, "royaumes"));
    static final KeyMapping TOUCHE_SERMENT = new KeyMapping("key.royaumes.serment", 74 /* J */, CATEGORIE);
    static final KeyMapping TOUCHE_CAPACITE = new KeyMapping("key.royaumes.capacite", 82 /* R */, CATEGORIE);
    static final KeyMapping TOUCHE_VOIE = new KeyMapping("key.royaumes.voie", 75 /* K */, CATEGORIE);
    private static int attente = 60;
    private static int compteur = 0;

    private ClientRoyaumes() {}

    @SubscribeEvent
    static void touches(RegisterKeyMappingsEvent event) {
        event.registerCategory(CATEGORIE);
        event.register(TOUCHE_SERMENT);
        event.register(TOUCHE_CAPACITE);
        event.register(TOUCHE_VOIE);
    }

    @SubscribeEvent
    static void couches(RegisterGuiLayersEvent event) {
        event.registerAboveAll(Identifier.fromNamespaceAndPath(RoyaumesMortels.MODID, "hud"), new HudRoyaumes());
    }

    @SubscribeEvent
    static void connexion(ClientPlayerNetworkEvent.LoggingIn event) {
        DonneesHeros.actuelle = null;
        DonneesHeros.FACTIONS.clear();
        attente = 60;
        ClientPacketListener c = Minecraft.getInstance().getConnection();
        if (c != null) {
            try {
                c.send(new ServerboundCustomPayloadPacket(new BonjourModde(1)));
            } catch (RuntimeException e) {
                // serveur sans le mod
            }
        }
    }

    /** Remplace [serment], [capacite], [voie] par la touche réellement configurée par le joueur. */
    public static String touches(String s) {
        return s.replace("[serment]", TOUCHE_SERMENT.getTranslatedKeyMessage().getString())
                .replace("[capacite]", TOUCHE_CAPACITE.getTranslatedKeyMessage().getString())
                .replace("[voie]", TOUCHE_VOIE.getTranslatedKeyMessage().getString());
    }

    static void ouvrir(Minecraft mc) {
        mc.gui.setScreen(new EcranSerment());
    }

    @SubscribeEvent
    static void tick(ClientTickEvent.Post event) {
        Minecraft mc = Minecraft.getInstance();
        if (mc.player == null) {
            return;
        }
        while (TOUCHE_SERMENT.consumeClick()) {
            if (mc.gui.screen() == null) {
                ouvrir(mc);
            }
        }
        while (TOUCHE_VOIE.consumeClick()) {
            if (mc.gui.screen() == null) {
                mc.gui.setScreen(new EcranVoies());
            }
        }
        while (TOUCHE_CAPACITE.consumeClick()) {
            ClientPacketListener c = mc.getConnection();
            if (c != null && mc.gui.screen() == null) {
                try {
                    c.send(new ServerboundCustomPayloadPacket(new UtiliserCapacite(1)));
                } catch (RuntimeException e) {
                    // serveur sans le mod
                }
            }
        }
        if (DonneesHeros.ouvrirForge) {
            DonneesHeros.ouvrirForge = false;
            mc.gui.setScreen(new EcranForge());
        }
        if (DonneesHeros.ouvrirCamp) {
            DonneesHeros.ouvrirCamp = false;
            mc.gui.setScreen(new EcranCamp());
        }
        // sans faction : l'écran de serment s'ouvre de lui-même (puis toutes les 2 minutes s'il est fermé)
        FicheHeros f = DonneesHeros.actuelle;
        if (f != null && f.faction() == 0 && mc.gui.screen() == null) {
            if (--attente <= 0) {
                ouvrir(mc);
                attente = 2400;
            }
        }
        if (++compteur % 10 == 0) {
            SkinsFactions.appliquer(mc);
        }
    }
}
