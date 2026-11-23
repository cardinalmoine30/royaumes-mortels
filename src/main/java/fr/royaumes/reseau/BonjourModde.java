package fr.royaumes.reseau;

import fr.royaumes.RoyaumesMortels;
import net.minecraft.network.RegistryFriendlyByteBuf;
import net.minecraft.network.codec.StreamCodec;
import net.minecraft.network.protocol.common.custom.CustomPacketPayload;
import net.minecraft.resources.Identifier;

/** Client -> serveur, à la connexion : « j'ai le mod » (le serveur remplace alors le dialogue d'accueil par l'écran de serment). */
public record BonjourModde(int version) implements CustomPacketPayload {
    public static final CustomPacketPayload.Type<BonjourModde> TYPE =
            new CustomPacketPayload.Type<>(Identifier.fromNamespaceAndPath(RoyaumesMortels.MODID, "bonjour"));
    public static final StreamCodec<RegistryFriendlyByteBuf, BonjourModde> CODEC =
            CustomPacketPayload.codec((c, b) -> b.writeVarInt(c.version()), b -> new BonjourModde(b.readVarInt()));

    @Override
    public CustomPacketPayload.Type<BonjourModde> type() {
        return TYPE;
    }
}
