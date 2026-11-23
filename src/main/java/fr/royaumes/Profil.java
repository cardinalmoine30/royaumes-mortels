package fr.royaumes;

/** Caractéristiques d'un mob de faction ou d'un boss (voir ProfilsGeneres). */
public record Profil(String id, String equipe, float pv, float degats, float armure, float vitesse,
                     float echelle, float largeur, float hauteur, Capacite capacite, boolean boss) {}
