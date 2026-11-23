package fr.royaumes.reseau;

import fr.royaumes.RoyaumesMortels;
import java.util.ArrayList;
import java.util.List;
import java.util.UUID;
import net.minecraft.network.RegistryFriendlyByteBuf;
import net.minecraft.network.codec.StreamCodec;
import net.minecraft.network.protocol.common.custom.CustomPacketPayload;
import net.minecraft.resources.Identifier;

/** Serveur -> clients : faction de chaque joueur connecté (pour afficher son skin de faction). */
public record FactionsVisibles(List<UUID> joueurs, List<Integer> factions) implements CustomPacketPayload {
    public static final CustomPacketPayload.Type<FactionsVisibles> TYPE =
            new CustomPacketPayload.Type<>(Identifier.fromNamespaceAndPath(RoyaumesMortels.MODID, "factions"));
    public static final StreamCodec<RegistryFriendlyByteBuf, FactionsVisibles> CODEC =
            CustomPacketPayload.codec(FactionsVisibles::ecrire, FactionsVisibles::lire);

    private void ecrire(RegistryFriendlyByteBuf b) {
        b.writeVarInt(joueurs.size());
        for (int i = 0; i < joueurs.size(); i++) {
            b.writeLong(joueurs.get(i).getMostSignificantBits());
            b.writeLong(joueurs.get(i).getLeastSignificantBits());
            b.writeVarInt(factions.get(i));
        }
    }

    private static FactionsVisibles lire(RegistryFriendlyByteBuf b) {
        int n = Math.min(1000, b.readVarInt());
        List<UUID> j = new ArrayList<>(n);
        List<Integer> f = new ArrayList<>(n);
        for (int i = 0; i < n; i++) {
            j.add(new UUID(b.readLong(), b.readLong()));
            f.add(b.readVarInt());
        }
        return new FactionsVisibles(j, f);
    }

    @Override
    public CustomPacketPayload.Type<FactionsVisibles> type() {
        return TYPE;
    }
}
