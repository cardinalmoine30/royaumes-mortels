package fr.royaumes.reseau;

import fr.royaumes.RoyaumesMortels;
import net.minecraft.network.RegistryFriendlyByteBuf;
import net.minecraft.network.codec.StreamCodec;
import net.minecraft.network.protocol.common.custom.CustomPacketPayload;
import net.minecraft.resources.Identifier;

/** Client -> serveur : le joueur prête serment à la faction n (1 à 25). */
public record ChoixFaction(int faction) implements CustomPacketPayload {
    public static final CustomPacketPayload.Type<ChoixFaction> TYPE =
            new CustomPacketPayload.Type<>(Identifier.fromNamespaceAndPath(RoyaumesMortels.MODID, "choix_faction"));
    public static final StreamCodec<RegistryFriendlyByteBuf, ChoixFaction> CODEC =
            CustomPacketPayload.codec((c, b) -> b.writeVarInt(c.faction()), b -> new ChoixFaction(b.readVarInt()));

    @Override
    public CustomPacketPayload.Type<ChoixFaction> type() {
        return TYPE;
    }
}
