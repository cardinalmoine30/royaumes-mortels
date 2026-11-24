package fr.royaumes.reseau;

import fr.royaumes.ContenuGenere;
import fr.royaumes.FactionsGenerees;
import fr.royaumes.camp.Camps;
import fr.royaumes.magie.Capacites;
import fr.royaumes.magie.Magie;
import fr.royaumes.magie.Saga;
import fr.royaumes.magie.Sorts;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.UUID;
import net.minecraft.ChatFormatting;
import net.minecraft.network.chat.Component;
import net.minecraft.server.MinecraftServer;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.world.scores.Objective;
import net.minecraft.world.scores.ReadOnlyScoreInfo;
import net.minecraft.world.scores.ScoreHolder;
import net.minecraft.world.scores.Scoreboard;
import net.neoforged.neoforge.event.tick.ServerTickEvent;
import net.neoforged.neoforge.network.PacketDistributor;
import net.neoforged.neoforge.network.event.RegisterPayloadHandlersEvent;

/**
 * Canal réseau du mod : fiche du héros (niveau, gloire, compétences, énergie arcanique), factions des joueurs
 * (skins), choix de faction depuis l'écran de serment. Les données viennent du scoreboard du datapack.
 */
public final class Reseau {
    public static final String TAG_MODDE = "rm_modde";
    private static int compteur = 0;
    private static final Map<UUID, Object> DERNIERE_DIMENSION = new HashMap<>();

    private Reseau() {}

    public static void enregistrer(RegisterPayloadHandlersEvent event) {
        var r = event.registrar("2").optional();
        r.playToClient(FicheHeros.TYPE, FicheHeros.CODEC, (fiche, contexte) -> DonneesHeros.actuelle = fiche);
        r.playToClient(FactionsVisibles.TYPE, FactionsVisibles.CODEC, (f, contexte) -> {
            for (int i = 0; i < f.joueurs().size(); i++) {
                DonneesHeros.FACTIONS.put(f.joueurs().get(i), f.factions().get(i));
            }
        });
        r.playToServer(ChoixFaction.TYPE, ChoixFaction.CODEC, (c, contexte) -> {
            if (contexte.player() instanceof ServerPlayer sp) {
                choisir(sp, c.faction());
            }
        });
        r.playToServer(UtiliserCapacite.TYPE, UtiliserCapacite.CODEC, (c, contexte) -> {
            if (contexte.player() instanceof ServerPlayer sp) {
                Capacites.utiliser(sp, score(sp.level().getServer().getScoreboard(), sp, "rm_faction"));
            }
        });
        r.playToClient(FicheCamp.TYPE, FicheCamp.CODEC, (f, contexte) -> {
            DonneesHeros.camp = f;
            if (f.ouvrir()) {
                DonneesHeros.ouvrirCamp = true;
            }
        });
        r.playToServer(ActionCamp.TYPE, ActionCamp.CODEC, (a, contexte) -> {
            if (contexte.player() instanceof ServerPlayer sp) {
                Camps.action(sp, a.action(), a.arg(), a.texte());
            }
        });
        r.playToClient(OuvrirForge.TYPE, OuvrirForge.CODEC, (o, contexte) -> DonneesHeros.ouvrirForge = true);
        r.playToServer(BonjourModde.TYPE, BonjourModde.CODEC, (c, contexte) -> {
            if (contexte.player() instanceof ServerPlayer sp) {
                sp.addTag(TAG_MODDE);
                envoyerFiche(sp);
            }
        });
    }

    /** Serment : on passe par le trigger rm_choix du datapack, qui applique la faction (une seule fois). */
    private static void choisir(ServerPlayer sp, int faction) {
        if (faction < 1 || faction >= FactionsGenerees.IDS.length) {
            return;
        }
        Scoreboard sb = sp.level().getServer().getScoreboard();
        if (score(sb, sp, "rm_faction") > 0) {
            return;
        }
        Objective choix = sb.getObjective("rm_choix");
        if (choix != null) {
            sb.getOrCreatePlayerScore(sp, choix).set(faction);
            sp.sendSystemMessage(Component.translatable("royaumes.serment.choisi", FactionsGenerees.NOMS[faction])
                    .withColor(FactionsGenerees.COULEURS[faction]));
        }
    }

    public static void envoyerFiche(ServerPlayer joueur) {
        Scoreboard sb = joueur.level().getServer().getScoreboard();
        int[] rangs = new int[FactionsGenerees.COMPETENCES.length];
        for (int i = 0; i < rangs.length; i++) {
            rangs[i] = score(sb, joueur, "rm_" + FactionsGenerees.COMPETENCES[i]);
        }
        FicheHeros fiche = new FicheHeros(score(sb, joueur, "rm_niveau"), score(sb, joueur, "rm_gloire"),
                score(sb, joueur, "rm_besoin"), score(sb, joueur, "rm_pts"), score(sb, joueur, "rm_faction"), rangs,
                Magie.energie(joueur), Magie.maximum(joueur), Capacites.reste(joueur));
        try {
            PacketDistributor.sendToPlayer(joueur, fiche);
        } catch (RuntimeException e) {
            // client sans le mod : on ignore
        }
    }

    public static void tickServeur(ServerTickEvent.Post event) {
        MinecraftServer serveur = event.getServer();
        Sorts.tick(serveur.overworld().getGameTime());
        if (++compteur % 20 != 0) {
            return;
        }
        Scoreboard sb = serveur.getScoreboard();
        List<UUID> ids = new ArrayList<>();
        List<Integer> factions = new ArrayList<>();
        for (ServerPlayer joueur : serveur.getPlayerList().getPlayers()) {
            int faction = score(sb, joueur, "rm_faction");
            Magie.regenerer(joueur, faction);
            if (faction > 0) {
                Saga.accorder(joueur, "serment");
            }
            envoyerFiche(joueur);
            ids.add(joueur.getUUID());
            factions.add(faction);
            annoncerRoyaume(joueur);
            Camps.tickJoueur(joueur);
            fr.royaumes.arsenal.Arsenal.bonusPanoplie(joueur);
        }
        FactionsVisibles visibles = new FactionsVisibles(ids, factions);
        for (ServerPlayer joueur : serveur.getPlayerList().getPlayers()) {
            try {
                PacketDistributor.sendToPlayer(joueur, visibles);
            } catch (RuntimeException e) {
                // client sans le mod
            }
        }
    }

    /** En entrant dans un Royaume : rappel du Vent qui y souffle (sorts à moitié prix). */
    private static void annoncerRoyaume(ServerPlayer joueur) {
        Object dim = joueur.level().dimension();
        Object avant = DERNIERE_DIMENSION.put(joueur.getUUID(), dim);
        if (avant == null || avant.equals(dim)) {
            return;
        }
        int vent = Magie.ventDuLieu(joueur.level());
        if (vent >= 0) {
            joueur.sendOverlayMessage(Component.literal("Royaume de " + ContenuGenere.NOMS_VENTS[vent] + " — le Vent de "
                    + ContenuGenere.NOMS_VENTS[vent] + " souffle ici : ses sorts coûtent moitié moins.")
                    .withColor(ContenuGenere.COULEURS_VENTS[vent]));
        } else if (Magie.estDans(joueur.level(), "royaumes:huit_points")) {
            joueur.sendOverlayMessage(Component.literal("Les Huit-Points — le Chaos règne ici.").withStyle(ChatFormatting.DARK_RED));
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
