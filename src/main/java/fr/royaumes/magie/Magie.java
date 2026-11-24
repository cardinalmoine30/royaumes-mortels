package fr.royaumes.magie;

import fr.royaumes.ContenuGenere;
import fr.royaumes.reseau.Reseau;
import net.minecraft.ChatFormatting;
import net.minecraft.core.registries.Registries;
import net.minecraft.network.chat.Component;
import net.minecraft.resources.Identifier;
import net.minecraft.resources.ResourceKey;
import net.minecraft.server.MinecraftServer;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.sounds.SoundSource;
import net.minecraft.world.level.Level;
import net.minecraft.world.scores.Objective;
import net.minecraft.world.scores.ReadOnlyScoreInfo;
import net.minecraft.world.scores.Scoreboard;
import net.minecraft.world.scores.criteria.ObjectiveCriteria;

/**
 * Énergie arcanique des héros (objectif rm_arcane, lisible par le datapack) :
 * maximum 100 + 5 par niveau, +2 par seconde (+4 dans le Royaume d'origine de sa faction),
 * sorts à moitié prix dans le Royaume de leur Vent.
 */
public final class Magie {
    public static final String OBJECTIF = "rm_arcane";
    private static final ResourceKey<Level>[] DIMENSIONS = dimensions();

    private Magie() {}

    @SuppressWarnings("unchecked")
    private static ResourceKey<Level>[] dimensions() {
        ResourceKey<Level>[] d = new ResourceKey[ContenuGenere.DIMENSIONS_VENTS.length];
        for (int i = 0; i < d.length; i++) {
            d[i] = ResourceKey.create(Registries.DIMENSION, Identifier.parse(ContenuGenere.DIMENSIONS_VENTS[i]));
        }
        return d;
    }

    /** Index du Vent dont le joueur se trouve dans le Royaume, ou -1. */
    public static int ventDuLieu(Level niveau) {
        for (int i = 0; i < DIMENSIONS.length; i++) {
            if (niveau.dimension().equals(DIMENSIONS[i])) {
                return i;
            }
        }
        return -1;
    }

    public static boolean estDans(Level niveau, String dimension) {
        return niveau.dimension().equals(ResourceKey.create(Registries.DIMENSION, Identifier.parse(dimension)));
    }

    private static Objective objectif(MinecraftServer serveur) {
        Scoreboard sb = serveur.getScoreboard();
        Objective o = sb.getObjective(OBJECTIF);
        if (o == null) {
            o = sb.addObjective(OBJECTIF, ObjectiveCriteria.DUMMY, Component.literal("Énergie arcanique"),
                    ObjectiveCriteria.RenderType.INTEGER, false, null);
        }
        return o;
    }

    private static int score(Scoreboard sb, ServerPlayer p, String nom) {
        Objective o = sb.getObjective(nom);
        if (o == null) {
            return 0;
        }
        ReadOnlyScoreInfo info = sb.getPlayerScoreInfo(p, o);
        return info == null ? 0 : info.value();
    }

    public static int maximum(ServerPlayer p) {
        return 100 + 5 * Math.max(0, score(p.level().getServer().getScoreboard(), p, "rm_niveau"));
    }

    public static int energie(ServerPlayer p) {
        Scoreboard sb = p.level().getServer().getScoreboard();
        Objective o = objectif(p.level().getServer());
        ReadOnlyScoreInfo info = sb.getPlayerScoreInfo(p, o);
        if (info == null) {
            sb.getOrCreatePlayerScore(p, o).set(maximum(p));
            return maximum(p);
        }
        return info.value();
    }

    public static void definir(ServerPlayer p, int valeur) {
        MinecraftServer s = p.level().getServer();
        s.getScoreboard().getOrCreatePlayerScore(p, objectif(s)).set(Math.max(0, Math.min(maximum(p), valeur)));
    }

    public static void ajouter(ServerPlayer p, int n) {
        definir(p, energie(p) + n);
        Reseau.envoyerFiche(p);
    }

    /** Appelé chaque seconde : régénération. */
    public static void regenerer(ServerPlayer p, int faction) {
        int e = energie(p);
        int max = maximum(p);
        if (e < max) {
            int gain = 2;
            if (faction > 0 && faction < ContenuGenere.DIMENSION_FACTION.length
                    && estDans(p.level(), ContenuGenere.DIMENSION_FACTION[faction])) {
                gain = 4;
            }
            definir(p, e + gain);
        } else if (e > max) {
            definir(p, max);
        }
    }

    public static int cout(ServerPlayer p, int vent, int rang) {
        int c = ContenuGenere.SORTS_COUTS[vent][rang];
        return ventDuLieu(p.level()) == vent ? (c + 1) / 2 : c;
    }

    /** Tente de lancer un sort ; renvoie vrai s'il a été lancé (énergie dépensée). */
    public static boolean lancer(ServerPlayer p, ServerLevel niveau, int vent, int rang) {
        int c = cout(p, vent, rang);
        int e = energie(p);
        boolean libre = p.isCreative();
        if (e < c && !libre) {
            p.sendOverlayMessage(Component.translatable("royaumes.sort.manque", e, c).withStyle(ChatFormatting.RED));
            niveau.playSound(null, p.getX(), p.getY(), p.getZ(), SoundEvents.ILLUSIONER_MIRROR_MOVE, SoundSource.PLAYERS, 0.6F, 0.6F);
            return false;
        }
        if (!Sorts.lancer(p, niveau, vent, rang)) {
            return false;
        }
        if (!libre) {
            definir(p, e - c);
        }
        p.sendOverlayMessage(Component.translatable("royaumes.sort.lance",
                Component.translatable("royaumes.sort." + ContenuGenere.SORTS_IDS[vent][rang]), c).withColor(ContenuGenere.COULEURS_VENTS[vent]));
        Reseau.envoyerFiche(p);
        Saga.accorder(p, "sort");
        return true;
    }
}
