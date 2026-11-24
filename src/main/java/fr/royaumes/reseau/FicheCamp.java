package fr.royaumes.reseau;

import fr.royaumes.RoyaumesMortels;
import java.util.ArrayList;
import java.util.List;
import net.minecraft.network.RegistryFriendlyByteBuf;
import net.minecraft.network.codec.StreamCodec;
import net.minecraft.network.protocol.common.custom.CustomPacketPayload;
import net.minecraft.resources.Identifier;

/** Serveur -> client : état du camp de guerre (ouvre l'écran du camp si ouvrir est vrai). */
public record FicheCamp(boolean ouvrir, int faction, int niveau, int butin, int unites, int max, int ordre, int raidType,
                        int raidReste, int force, int coutNiveau, int debloquees, List<String> recrues, List<Integer> couts)
        implements CustomPacketPayload {
    public static final CustomPacketPayload.Type<FicheCamp> TYPE =
            new CustomPacketPayload.Type<>(Identifier.fromNamespaceAndPath(RoyaumesMortels.MODID, "camp"));
    public static final StreamCodec<RegistryFriendlyByteBuf, FicheCamp> CODEC = CustomPacketPayload.codec(FicheCamp::ecrire, FicheCamp::lire);

    private void ecrire(RegistryFriendlyByteBuf b) {
        b.writeBoolean(ouvrir);
        for (int v : new int[] {faction, niveau, butin, unites, max, ordre, raidType, raidReste + 1, force, coutNiveau, debloquees}) {
            b.writeVarInt(v);
        }
        b.writeVarInt(recrues.size());
        for (int i = 0; i < recrues.size(); i++) {
            b.writeUtf(recrues.get(i));
            b.writeVarInt(couts.get(i));
        }
    }

    private static FicheCamp lire(RegistryFriendlyByteBuf b) {
        boolean o = b.readBoolean();
        int[] v = new int[11];
        for (int i = 0; i < v.length; i++) {
            v[i] = b.readVarInt();
        }
        int n = Math.min(16, b.readVarInt());
        List<String> r = new ArrayList<>();
        List<Integer> c = new ArrayList<>();
        for (int i = 0; i < n; i++) {
            r.add(b.readUtf());
            c.add(b.readVarInt());
        }
        return new FicheCamp(o, v[0], v[1], v[2], v[3], v[4], v[5], v[6], v[7] - 1, v[8], v[9], v[10], r, c);
    }

    @Override
    public CustomPacketPayload.Type<FicheCamp> type() {
        return TYPE;
    }
}
