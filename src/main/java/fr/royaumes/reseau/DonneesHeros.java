package fr.royaumes.reseau;

import java.util.Map;
import java.util.UUID;
import java.util.concurrent.ConcurrentHashMap;

/** Dernières données reçues par le client (aucune classe cliente ici : chargeable des deux côtés). */
public final class DonneesHeros {
    private DonneesHeros() {}

    public static volatile FicheHeros actuelle = null;
    /** Faction de chaque joueur connu (uuid -> numéro rm_faction). */
    public static final Map<UUID, Integer> FACTIONS = new ConcurrentHashMap<>();
}
