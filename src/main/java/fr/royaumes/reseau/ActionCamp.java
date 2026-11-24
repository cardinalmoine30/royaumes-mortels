package fr.royaumes.reseau;

import fr.royaumes.RoyaumesMortels;
import net.minecraft.network.RegistryFriendlyByteBuf;
import net.minecraft.network.codec.StreamCodec;
import net.minecraft.network.protocol.common.custom.CustomPacketPayload;
import net.minecraft.resources.Identifier;

/** Client -> serveur : action sur le camp (1 recruter, 2 améliorer, 3 déposer, 4 ordre, 5 raid, 6 bâtiment,
 * 7 inviter, 8 retirer un allié, 9 explorer, 10 raid contre un joueur). */
public record ActionCamp(int action, int arg, String texte) implements CustomPacketPayload {
    public static final CustomPacketPayload.Type<ActionCamp> TYPE =
            new CustomPacketPayload.Type<>(Identifier.fromNamespaceAndPath(RoyaumesMortels.MODID, "action_camp"));
    public static final StreamCodec<RegistryFriendlyByteBuf, ActionCamp> CODEC = CustomPacketPayload.codec(
            (c, b) -> { b.writeVarInt(c.action()); b.writeVarInt(c.arg()); b.writeUtf(c.texte()); },
            b -> new ActionCamp(b.readVarInt(), b.readVarInt(), b.readUtf(64)));

    @Override
    public CustomPacketPayload.Type<ActionCamp> type() {
        return TYPE;
    }
}
