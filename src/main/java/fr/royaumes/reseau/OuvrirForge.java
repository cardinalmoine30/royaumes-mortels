package fr.royaumes.reseau;

import fr.royaumes.RoyaumesMortels;
import net.minecraft.network.RegistryFriendlyByteBuf;
import net.minecraft.network.codec.StreamCodec;
import net.minecraft.network.protocol.common.custom.CustomPacketPayload;
import net.minecraft.resources.Identifier;

/** Serveur -> client : ouvrir l'écran de la Forge de guerre. */
public record OuvrirForge(int version) implements CustomPacketPayload {
    public static final CustomPacketPayload.Type<OuvrirForge> TYPE =
            new CustomPacketPayload.Type<>(Identifier.fromNamespaceAndPath(RoyaumesMortels.MODID, "ouvrir_forge"));
    public static final StreamCodec<RegistryFriendlyByteBuf, OuvrirForge> CODEC =
            CustomPacketPayload.codec((c, b) -> b.writeVarInt(c.version()), b -> new OuvrirForge(b.readVarInt()));

    @Override
    public CustomPacketPayload.Type<OuvrirForge> type() {
        return TYPE;
    }
}
