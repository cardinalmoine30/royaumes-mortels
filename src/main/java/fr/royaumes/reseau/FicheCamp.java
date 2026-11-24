package fr.royaumes.reseau;

import fr.royaumes.RoyaumesMortels;
import java.util.ArrayList;
import java.util.List;
import net.minecraft.network.RegistryFriendlyByteBuf;
import net.minecraft.network.codec.StreamCodec;
import net.minecraft.network.protocol.common.custom.CustomPacketPayload;
import net.minecraft.resources.Identifier;

/** Serveur -> client : état du camp de guerre (ouvre l'écran du camp si ouvrir est vrai). */
public record FicheCamp(boolean ouvrir, boolean proprio, String chef, int faction, int niveau, int butin, int unites, int max, int ordre,
                        int raidType, int raidReste, int force, int coutNiveau, int debloquees, List<String> recrues, List<Integer> couts,
                        int[] batiments, int explReste, int explNb, List<String> proches, List<String> invites, List<String> cibles,
                        List<Integer> ciblesDef, String raidCible, int tour) implements CustomPacketPayload {
    public static final CustomPacketPayload.Type<FicheCamp> TYPE =
            new CustomPacketPayload.Type<>(Identifier.fromNamespaceAndPath(RoyaumesMortels.MODID, "camp"));
    public static final StreamCodec<RegistryFriendlyByteBuf, FicheCamp> CODEC = CustomPacketPayload.codec(FicheCamp::ecrire, FicheCamp::lire);

    private static void textes(RegistryFriendlyByteBuf b, List<String> l) {
        b.writeVarInt(l.size());
        l.forEach(b::writeUtf);
    }

    private static List<String> textes(RegistryFriendlyByteBuf b) {
        int n = Math.min(32, b.readVarInt());
        List<String> l = new ArrayList<>();
        for (int i = 0; i < n; i++) {
            l.add(b.readUtf(64));
        }
        return l;
    }

    private static void entiers(RegistryFriendlyByteBuf b, List<Integer> l) {
        b.writeVarInt(l.size());
        l.forEach(b::writeVarInt);
    }

    private static List<Integer> entiers(RegistryFriendlyByteBuf b) {
        int n = Math.min(32, b.readVarInt());
        List<Integer> l = new ArrayList<>();
        for (int i = 0; i < n; i++) {
            l.add(b.readVarInt());
        }
        return l;
    }

    private void ecrire(RegistryFriendlyByteBuf b) {
        b.writeBoolean(ouvrir);
        b.writeBoolean(proprio);
        b.writeUtf(chef);
        for (int v : new int[] {faction, niveau, butin, unites, max, ordre, raidType, raidReste + 1, force, coutNiveau, debloquees,
                explReste + 1, explNb, tour}) {
            b.writeVarInt(v);
        }
        textes(b, recrues);
        entiers(b, couts);
        b.writeVarInt(batiments.length);
        for (int v : batiments) {
            b.writeVarInt(v);
        }
        textes(b, proches);
        textes(b, invites);
        textes(b, cibles);
        entiers(b, ciblesDef);
        b.writeUtf(raidCible);
    }

    private static FicheCamp lire(RegistryFriendlyByteBuf b) {
        boolean o = b.readBoolean();
        boolean pr = b.readBoolean();
        String chef = b.readUtf(64);
        int[] v = new int[14];
        for (int i = 0; i < v.length; i++) {
            v[i] = b.readVarInt();
        }
        List<String> recrues = textes(b);
        List<Integer> couts = entiers(b);
        int[] bat = new int[Math.min(16, b.readVarInt())];
        for (int i = 0; i < bat.length; i++) {
            bat[i] = b.readVarInt();
        }
        List<String> proches = textes(b);
        List<String> invites = textes(b);
        List<String> cibles = textes(b);
        List<Integer> defs = entiers(b);
        String rc = b.readUtf(64);
        return new FicheCamp(o, pr, chef, v[0], v[1], v[2], v[3], v[4], v[5], v[6], v[7] - 1, v[8], v[9], v[10], recrues, couts, bat,
                v[11] - 1, v[12], proches, invites, cibles, defs, rc, v[13]);
    }

    @Override
    public CustomPacketPayload.Type<FicheCamp> type() {
        return TYPE;
    }
}
