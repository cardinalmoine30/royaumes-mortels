package fr.royaumes.client;

import fr.royaumes.FactionsGenerees;
import fr.royaumes.RoyaumesMortels;
import fr.royaumes.reseau.DonneesHeros;
import java.lang.reflect.Field;
import java.util.Map;
import java.util.UUID;
import java.util.function.Supplier;
import net.minecraft.client.Minecraft;
import net.minecraft.client.multiplayer.ClientPacketListener;
import net.minecraft.client.multiplayer.PlayerInfo;
import net.minecraft.core.ClientAsset;
import net.minecraft.resources.Identifier;
import net.minecraft.world.entity.player.PlayerModelType;
import net.minecraft.world.entity.player.PlayerSkin;

/**
 * Skin de faction : quand un joueur a prêté serment, son apparence devient celle de sa faction
 * (textures/skin/<faction>.png), pour lui comme pour les autres joueurs qui ont le mod.
 * On remplace le fournisseur de skin de son PlayerInfo ; cape et élytres d'origine sont conservées.
 */
public final class SkinsFactions {
    private static Field champ;
    private static boolean indisponible = false;

    private SkinsFactions() {}

    /** Fournisseur de skin de faction, qui garde le fournisseur d'origine. */
    record SkinFaction(Supplier<PlayerSkin> origine, int faction) implements Supplier<PlayerSkin> {
        @Override
        public PlayerSkin get() {
            PlayerSkin o = origine.get();
            Identifier id = Identifier.fromNamespaceAndPath(RoyaumesMortels.MODID, "skin/" + FactionsGenerees.IDS[faction]);
            return new PlayerSkin(new ClientAsset.ResourceTexture(id), o.cape(), o.elytra(), PlayerModelType.WIDE, o.secure());
        }
    }

    @SuppressWarnings("unchecked")
    public static void appliquer(Minecraft mc) {
        ClientPacketListener connexion = mc.getConnection();
        if (connexion == null || indisponible) {
            return;
        }
        try {
            if (champ == null) {
                champ = PlayerInfo.class.getDeclaredField("skinLookup");
                champ.setAccessible(true);
            }
            for (Map.Entry<UUID, Integer> e : DonneesHeros.FACTIONS.entrySet()) {
                int f = e.getValue();
                PlayerInfo info = connexion.getPlayerInfo(e.getKey());
                if (info == null) {
                    continue;
                }
                Supplier<PlayerSkin> actuel = (Supplier<PlayerSkin>) champ.get(info);
                Supplier<PlayerSkin> origine = actuel instanceof SkinFaction sf ? sf.origine() : actuel;
                if (f <= 0 || f >= FactionsGenerees.IDS.length) {
                    if (actuel instanceof SkinFaction) {
                        champ.set(info, origine);
                    }
                    continue;
                }
                if (actuel instanceof SkinFaction sf && sf.faction() == f) {
                    continue;
                }
                champ.set(info, new SkinFaction(origine, f));
            }
        } catch (ReflectiveOperationException | RuntimeException ex) {
            indisponible = true;
            RoyaumesMortels.LOGGER.warn("[Royaumes Mortels] Skins de faction indisponibles : {}", ex.toString());
        }
    }
}
