package fr.royaumes.reseau;

import fr.royaumes.FactionsGenerees;
import net.minecraft.server.MinecraftServer;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.world.scores.Objective;
import net.minecraft.world.scores.ReadOnlyScoreInfo;
import net.minecraft.world.scores.ScoreHolder;
import net.minecraft.world.scores.Scoreboard;
import net.neoforged.neoforge.event.tick.ServerTickEvent;
import net.neoforged.neoforge.network.PacketDistributor;
import net.neoforged.neoforge.network.event.RegisterPayloadHandlersEvent;

/** Canal réseau du mod : la fiche du héros (niveau, gloire, compétences) lue dans le scoreboard du datapack. */
public final class Reseau {
    private static int compteur = 0;

    private Reseau() {}

    public static void enregistrer(RegisterPayloadHandlersEvent event) {
        event.registrar("1").optional()
                .playToClient(FicheHeros.TYPE, FicheHeros.CODEC, (fiche, contexte) -> DonneesHeros.actuelle = fiche);
    }

    public static void tickServeur(ServerTickEvent.Post event) {
        if (++compteur % 20 != 0) {
            return;
        }
        MinecraftServer serveur = event.getServer();
        Scoreboard sb = serveur.getScoreboard();
        for (ServerPlayer joueur : serveur.getPlayerList().getPlayers()) {
            int[] rangs = new int[FactionsGenerees.COMPETENCES.length];
            for (int i = 0; i < rangs.length; i++) {
                rangs[i] = score(sb, joueur, "rm_" + FactionsGenerees.COMPETENCES[i]);
            }
            FicheHeros fiche = new FicheHeros(score(sb, joueur, "rm_niveau"), score(sb, joueur, "rm_gloire"),
                    score(sb, joueur, "rm_besoin"), score(sb, joueur, "rm_pts"), score(sb, joueur, "rm_faction"), rangs);
            try {
                PacketDistributor.sendToPlayer(joueur, fiche);
            } catch (RuntimeException e) {
                // client sans le mod : on ignore
            }
        }
    }

    private static int score(Scoreboard sb, ScoreHolder joueur, String nom) {
        Objective o = sb.getObjective(nom);
        if (o == null) {
            return 0;
        }
        ReadOnlyScoreInfo info = sb.getPlayerScoreInfo(joueur, o);
        return info == null ? 0 : info.value();
    }
}
