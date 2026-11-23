package fr.royaumes.reseau;

/** Dernière fiche reçue par le client (aucune classe cliente ici : chargeable des deux côtés). */
public final class DonneesHeros {
    private DonneesHeros() {}

    public static volatile FicheHeros actuelle = null;
}
