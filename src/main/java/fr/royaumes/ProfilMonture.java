package fr.royaumes;

/** Caractéristiques d'une monture de joueur (générées par outils/modeles/montures.py). */
public record ProfilMonture(String id, String faction, double vitesse, double pv, boolean vol, boolean feu, boolean saut,
                            float largeur, float hauteur, float selle) {
}
