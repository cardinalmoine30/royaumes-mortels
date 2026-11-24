package fr.royaumes.reseau;

import fr.royaumes.RoyaumesMortels;
import net.minecraft.network.RegistryFriendlyByteBuf;
import net.minecraft.network.codec.StreamCodec;
import net.minecraft.network.protocol.common.custom.CustomPacketPayload;
import net.minecraft.resources.Identifier;

/** Fiche du héros envoyée chaque seconde au client (inventaire de taverne, HUD, écran de serment). */
public record FicheHeros(int niveau, int gloire, int besoin, int points, int faction, int[] rangs, int energie, int energieMax, int capacite) implements CustomPacketPayload {
    public static final CustomPacketPayload.Type<FicheHeros> TYPE =
            new CustomPacketPayload.Type<>(Identifier.fromNamespaceAndPath(RoyaumesMortels.MODID, "fiche"));
    public static final StreamCodec<RegistryFriendlyByteBuf, FicheHeros> CODEC =
            CustomPacketPayload.codec(FicheHeros::ecrire, FicheHeros::lire);

    private void ecrire(RegistryFriendlyByteBuf b) {
        b.writeVarInt(niveau);
        b.writeVarInt(gloire);
        b.writeVarInt(besoin);
        b.writeVarInt(points);
        b.writeVarInt(faction);
        b.writeVarInt(rangs.length);
        for (int r : rangs) {
            b.writeVarInt(r);
        }
        b.writeVarInt(energie);
        b.writeVarInt(energieMax);
        b.writeVarInt(capacite);
    }

    private static FicheHeros lire(RegistryFriendlyByteBuf b) {
        int niveau = b.readVarInt();
        int gloire = b.readVarInt();
        int besoin = b.readVarInt();
        int points = b.readVarInt();
        int faction = b.readVarInt();
        int n = Math.min(32, b.readVarInt());
        int[] rangs = new int[n];
        for (int i = 0; i < n; i++) {
            rangs[i] = b.readVarInt();
        }
        int energie = b.readVarInt();
        int energieMax = b.readVarInt();
        int capacite = b.readVarInt();
        return new FicheHeros(niveau, gloire, besoin, points, faction, rangs, energie, energieMax, capacite);
    }

    @Override
    public CustomPacketPayload.Type<FicheHeros> type() {
        return TYPE;
    }
}
