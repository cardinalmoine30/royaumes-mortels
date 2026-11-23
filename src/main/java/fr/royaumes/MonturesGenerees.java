package fr.royaumes;

import java.util.List;

/** Généré par outils/modeles/montures.py : une monture par faction jouable. */
public final class MonturesGenerees {
    private MonturesGenerees() {}

    public static final List<ProfilMonture> TOUTES = List.of(
        new ProfilMonture("monture_dracoth", "stormcast", 0.3, 60, false, false, false, 1.8F, 1.02F, 1.061F),
        new ProfilMonture("monture_destrier", "cites", 0.34, 40, false, false, false, 1.42F, 1.6F, 1.413F),
        new ProfilMonture("monture_magmadroth", "fyreslayers", 0.27, 70, false, true, false, 1.8F, 1.09F, 1.135F),
        new ProfilMonture("monture_gunhauler", "kharadron", 0.3, 50, true, false, false, 1.25F, 1.73F, 0.719F),
        new ProfilMonture("monture_coursier_ombre", "khaine", 0.37, 40, false, false, false, 1.42F, 1.63F, 1.413F),
        new ProfilMonture("monture_ishlaen", "idoneth", 0.32, 45, true, false, false, 1.49F, 0.8F, 0.8F),
        new ProfilMonture("monture_destrier_aube", "lumineth", 0.38, 40, false, false, false, 1.47F, 1.71F, 1.475F),
        new ProfilMonture("monture_aggradon", "seraphon", 0.33, 55, false, false, false, 1.8F, 1.23F, 1.291F),
        new ProfilMonture("monture_cerf_wyldwood", "sylvaneth", 0.36, 40, false, false, false, 1.38F, 1.69F, 1.413F),
        new ProfilMonture("monture_destrier_chaos", "esclaves", 0.34, 50, false, false, false, 1.47F, 1.63F, 1.413F),
        new ProfilMonture("monture_juggernaut", "khorne", 0.27, 80, false, true, false, 1.44F, 1.16F, 1.387F),
        new ProfilMonture("monture_disque", "tzeentch", 0.34, 40, true, false, false, 0.85F, 0.61F, 0.625F),
        new ProfilMonture("monture_seeker", "slaanesh", 0.42, 35, false, false, false, 1.29F, 1.59F, 1.35F),
        new ProfilMonture("monture_pusgoyle", "nurgle", 0.26, 55, true, false, false, 1.35F, 1.15F, 1.125F),
        new ProfilMonture("monture_gnaw_beast", "skaven", 0.35, 45, false, false, false, 1.68F, 1.2F, 1.188F),
        new ProfilMonture("monture_taurus", "hashut", 0.3, 60, true, true, false, 1.38F, 1.26F, 1.25F),
        new ProfilMonture("monture_dreadblade", "nighthaunt", 0.37, 40, false, false, false, 1.41F, 1.6F, 1.413F),
        new ProfilMonture("monture_cauchemar", "soulblight", 0.36, 50, false, false, false, 1.47F, 1.6F, 1.413F),
        new ProfilMonture("monture_kavalos", "ossiarch", 0.35, 50, false, false, false, 1.42F, 1.6F, 1.413F),
        new ProfilMonture("monture_morbheg", "fec", 0.3, 50, true, false, false, 1.42F, 1.29F, 1.25F),
        new ProfilMonture("monture_gore_grunta", "ironjawz", 0.34, 55, false, false, false, 1.32F, 1.15F, 1.125F),
        new ProfilMonture("monture_gnashtoof", "kruleboyz", 0.33, 55, false, false, false, 1.47F, 1.22F, 1.188F),
        new ProfilMonture("monture_squig", "gitz", 0.33, 35, false, false, true, 0.48F, 0.7F, 0.875F),
        new ProfilMonture("monture_mournfang", "ogors", 0.32, 70, false, false, false, 1.41F, 1.28F, 1.25F),
        new ProfilMonture("monture_mammouth", "behemat", 0.27, 90, false, false, false, 1.78F, 1.26F, 1.512F)
    );
}
