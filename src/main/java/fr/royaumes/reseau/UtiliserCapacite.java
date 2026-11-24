package fr.royaumes.reseau;

import fr.royaumes.RoyaumesMortels;
import net.minecraft.network.RegistryFriendlyByteBuf;
import net.minecraft.network.codec.StreamCodec;
import net.minecraft.network.protocol.common.custom.CustomPacketPayload;
import net.minecraft.resources.Identifier;

/** Client -> serveur : touche R, utiliser la capacité de sa faction. */
public record UtiliserCapacite(int version) implements CustomPacketPayload {
    public static final CustomPacketPayload.Type<UtiliserCapacite> TYPE =
            new CustomPacketPayload.Type<>(Identifier.fromNamespaceAndPath(RoyaumesMortels.MODID, "capacite"));
    public static final StreamCodec<RegistryFriendlyByteBuf, UtiliserCapacite> CODEC =
            CustomPacketPayload.codec((c, b) -> b.writeVarInt(c.version()), b -> new UtiliserCapacite(b.readVarInt()));

    @Override
    public CustomPacketPayload.Type<UtiliserCapacite> type() {
        return TYPE;
    }
}
