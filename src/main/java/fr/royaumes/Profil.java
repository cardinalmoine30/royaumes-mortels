package fr.royaumes;

/** Caractéristiques d'un mob de faction ou d'un boss (voir ProfilsGeneres). */
public record Profil(String id, String equipe, float pv, float degats, float armure, float vitesse,
                     float echelle, float largeur, float hauteur, Capacite capacite, Mode mode,
                     Special special, String sbire, boolean boss) {

    public boolean volant() {
        return mode == Mode.VOL || mode == Mode.VOL_TIR || mode == Mode.VOL_MAGE;
    }

    public boolean distance() {
        return mode == Mode.TIR || mode == Mode.MAGE || mode == Mode.VOL_TIR || mode == Mode.VOL_MAGE;
    }

    public boolean magique() {
        return mode == Mode.MAGE || mode == Mode.VOL_MAGE;
    }
}
