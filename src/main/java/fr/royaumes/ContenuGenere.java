package fr.royaumes;

/** FICHIER GÉNÉRÉ par outils/objets/objets.py : ne pas modifier à la main. */
public final class ContenuGenere {
    private ContenuGenere() {}

    /** Les huit Vents de magie (index = icône du HUD). */
    public static final String[] VENTS = {"azyr", "aqshy", "ghur", "ghyran", "hysh", "ulgu", "shyish", "chamon"};
    public static final String[] NOMS_VENTS = {"Azyr", "Aqshy", "Ghur", "Ghyran", "Hysh", "Ulgu", "Shyish", "Chamon"};
    public static final int[] COULEURS_VENTS = {0x468CFF, 0xF05A14, 0xA06432, 0x3CBE46, 0xF0E6A0, 0x645A8C, 0x965AD2, 0xDCAA28};
    public static final String[] DIMENSIONS_VENTS = {"royaumes:royaumes_mortels", "royaumes:aqshy", "royaumes:ghur", "royaumes:ghyran", "royaumes:hysh", "royaumes:ulgu", "royaumes:shyish", "royaumes:chamon"};

    /** Sorts : [vent][rang] (0 = sort mineur, clic droit ; 1 = grand sort, accroupi + clic droit). */
    public static final String[][] SORTS_IDS = {
        {"eclair", "comete"},
        {"trait", "cendres"},
        {"fureur", "meute"},
        {"seve", "ronces"},
        {"rayon", "eclat"},
        {"pas", "voile"},
        {"main", "moisson"},
        {"peau", "plomb"},
    };
    public static final String[][] SORTS_NOMS = {
        {"Éclair d'Azyr", "Comète de Sigmar"},
        {"Trait de flamme", "Vague de cendres"},
        {"Fureur bestiale", "Meute de Ghur"},
        {"Sève de vie", "Ronces d'Alarielle"},
        {"Rayon de Hysh", "Éclat aveuglant"},
        {"Pas d'ombre", "Voile de ténèbres"},
        {"Main de poussière", "Moisson des âmes"},
        {"Peau de fer", "Malédiction de plomb"},
    };
    public static final String[][] SORTS_DESC = {
        {"La foudre frappe la cible visée.", "Une comète s'abat et foudroie la zone."},
        {"Lance une salve de boules de feu.", "Un cône de feu embrase les ennemis devant toi."},
        {"Force et vitesse pendant 15 secondes.", "Trois loups de Ghur combattent à tes côtés une minute."},
        {"Soigne 8 points de vie et régénère.", "Des ronces entravent et blessent les ennemis proches."},
        {"Un rayon de lumière transperce la cible.", "Aveugle et révèle les ennemis ; brûle les morts-vivants."},
        {"Téléporte jusqu'à 16 blocs dans la direction visée.", "Invisibilité ; les ennemis proches sont plongés dans le noir."},
        {"Flétrit et blesse la cible visée.", "Draine la vie des ennemis proches."},
        {"Résistance et absorption pendant 20 secondes.", "Alourdit et affaiblit les ennemis proches."},
    };
    public static final int[][] SORTS_COUTS = {
        {15, 60},
        {12, 45},
        {20, 50},
        {20, 50},
        {15, 40},
        {15, 45},
        {15, 55},
        {20, 40},
    };
    public static final int[][] SORTS_RECHARGES = {
        {20, 200},
        {15, 160},
        {40, 400},
        {40, 200},
        {20, 200},
        {30, 300},
        {25, 240},
        {60, 200},
    };

    /** Blocs : id, outil, dureté, lumière, type spécial. */
    public static final String[] BLOCS = {"marbre_celeste", "marbre_celeste_grave", "basalte_ardent", "brique_de_braise", "os_de_monstre", "pierre_de_croc", "bois_de_vie", "jade_vivant", "pierre_de_lumiere", "cristal_de_hysh", "ardoise_d_ombre", "brume_figee", "pierre_funeraire", "dalle_des_ames", "cuivre_alchimique", "or_vif", "obsidienne_corrompue", "pierre_du_chaos", "minerai_pierre_royaumes", "minerai_pierre_royaumes_profond", "bloc_pierre_royaumes", "autel_arcanique", "portail_des_royaumes", "etendard_de_camp", "autel_des_seigneurs", "minerai_azyrite", "minerai_braise", "minerai_croc", "minerai_jade", "minerai_lumineux", "minerai_ombre", "minerai_ames", "minerai_or_vif", "minerai_malepierre"};
    public static final float[] BLOCS_DURETE = {1.5f, 1.5f, 1.8f, 2.0f, 2.0f, 2.0f, 2.0f, 1.8f, 1.5f, 1.2f, 2.5f, 1.0f, 2.0f, 2.0f, 3.0f, 3.0f, 20.0f, 3.0f, 3.0f, 4.5f, 5.0f, 3.5f, 25.0f, 2.0f, 50.0f, 3.0f, 3.0f, 3.0f, 3.0f, 3.0f, 3.0f, 3.0f, 3.0f, 4.0f};
    public static final int[] BLOCS_LUMIERE = {0, 0, 7, 4, 0, 0, 0, 3, 15, 12, 0, 2, 0, 5, 0, 2, 3, 6, 4, 4, 9, 10, 11, 6, 7, 3, 5, 0, 2, 8, 0, 4, 2, 6};
    public static final boolean[] BLOCS_BOIS = {false, false, false, false, false, false, true, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, true, false, false, false, false, false, false, false, false, false, false};
    public static final String[] BLOCS_SPECIAL = {"", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "AUTEL", "PORTAIL", "CAMP", "SEIGNEURS", "", "", "", "", "", "", "", "", ""};

    /** Écran de serment : données des 25 factions (index = numéro rm_faction, 0 = aucune). */
    public static final String[] ALLIANCES = {"", "ordre", "ordre", "ordre", "ordre", "ordre", "ordre", "ordre", "ordre", "ordre", "chaos", "chaos", "chaos", "chaos", "chaos", "chaos", "chaos", "mort", "mort", "mort", "mort", "destruction", "destruction", "destruction", "destruction", "destruction"};
    public static final String[] ROYAUMES = {"", "Azyr", "Ghyran", "Aqshy", "Chamon", "Ulgu", "Ulgu (océans)", "Hysh", "Ghur (jungles)", "Ghyran", "Les Huit-Points", "Aqshy", "Hysh / Huit-Points", "Les Huit-Points", "Ghyran (marais)", "Les Terres Rongées", "Aqshy", "Shyish", "Shyish", "Shyish", "Shyish / Ulgu", "Ghur", "Ghyran (marais)", "Ulgu", "Ghur", "Ghur"};
    public static final String[] DESCRIPTIONS = {"", "Héros mortels forgés à nouveau par Sigmar et lancés au combat par la foudre.", "Humains, aelfs et duardins des grandes cités libres, comme Hammerhal ou Excelsis.", "Duardins berserkers qui puisent leur rage dans l'ur-or incrusté dans leur chair.", "Duardins du ciel, marchands et pilotes de navires volants propulsés à l'aether-or.", "Aelfs fanatiques vouées au dieu du meurtre, guidées par Morathi-Khaine.", "Aelfs sans âme des profondeurs, qui chassent les âmes des vivants lors de leurs raids.", "Aelfs de la lumière, maîtres des arts élémentaires et de la perfection.", "Hommes-lézards célestes guidés par les Slann, forces de l'ordre cosmique.", "Esprits-arbres enfants d'Alarielle, la Reine Éternelle.", "Guerriers du Chaos Absolu, cuirassés de fer noir, qui cherchent la faveur des Dieux Sombres.", "« Du sang pour le Dieu du Sang ! » Berserkers dévoués au carnage.", "Sorciers et tzaangors du Grand Manipulateur, maître du changement.", "Adorateurs du Prince des Plaisirs, en quête d'excès et de perfection.", "Enfants du Grand-Père Nurgle, porteurs de pestes joyeuses et d'une endurance infinie.", "Hommes-rats du Grand Rat Cornu, maîtres de la malepierre et des tunnels.", "Duardins du Chaos, serviteurs du Père des Ténèbres, maîtres des forges infernales.", "Spectres condamnés par Nagash, hurlant à travers les Royaumes.", "Vampires de la lignée de Soulblight et leurs armées de morts relevés.", "Légions d'os façonnées par Nagash, la plus disciplinée des armées.", "Goules folles qui se croient nobles chevaliers d'une cour glorieuse.", "Les plus grands et les plus brutaux des orruks, couverts de ferraille. WAAAGH !", "Orruks des marais, rusés et cruels, adeptes des lames empoisonnées et des pièges.", "Grots fous de la Mauvaise Lune, chevaucheurs d'araignées et cultivateurs de champignons.", "Ogors gloutons et géants, pour qui tout ce qui bouge est un repas.", "Gargants colossaux, enfants du dieu-titan Behemat. Ils écrasent tout sur leur passage."};
    public static final String[] DONS = {"", "Taille +15 %, +3 cœurs, +2 armure", "Héros du village (rabais marchands), +1 chance, +1 cœur", "Résistance au feu, +1 dégât", "Dégâts de chute -50 %, chute sûre +6 blocs", "Vitesse +10 %, vitesse d'attaque +15 %", "Respiration aquatique, nage +60 %, minage sous l'eau", "Vision nocturne, vitesse +5 %, +1 chance, portée +1", "Taille +20 %, +2 cœurs, +4 armure, nage +30 %", "Régénération permanente, +2 cœurs", "Taille +10 %, +2 cœurs, +2 armure, +1 dégât", "Force I, vitesse d'attaque +10 %", "Célérité, +2 chance", "Vitesse +15 %, vitesse d'attaque +20 %", "+4 cœurs, régénération, +1 armure", "Vitesse +15 %, vision nocturne", "Résistance au feu, +4 armure", "Gravité réduite, chute sûre +10, vitesse +5 %", "+2 cœurs, +1 dégât, vision nocturne", "+6 armure, recul -40 %, +1 cœur", "Vitesse +10 %, saut +, +1 dégât", "Taille +15 %, +2 cœurs, +2 dégâts, recul -30 %", "+1 cœur, déplacement accroupi +30 %", "Vitesse +10 %, vision nocturne, saut amélioré", "Taille +40 %, +5 cœurs, +2 dégâts", "Taille ×2, +10 cœurs, +4 dégâts, grande portée, enjambe les blocs"};
    public static final String[] FARDEAUX = {"", "Vitesse -5 %", "Aucun don surnaturel", "Taille -15 %", "Taille -15 %", "-1 cœur", "Lent hors de l'eau (aucun bonus terrestre)", "Aucun", "Vitesse -5 %", "Brûle 2× plus longtemps, vitesse -5 %", "Chance -1 (marqués par le Chaos)", "-2 armure (Khorne méprise la prudence)", "-1 cœur", "-2 cœurs", "Vitesse -10 %", "Taille -20 %, -2 cœurs", "Taille -15 %, vitesse -5 %", "-2 cœurs", "Faiblesse en plein soleil", "Vitesse -10 %", "Leur « festin » est de la chair pourrie", "Vitesse -5 %", "Aucun", "Taille -30 %, -3 cœurs", "Faim permanente, vitesse -10 %", "Faim II permanente, ne passe pas les portes"};
    public static final int[] VENT_FACTION = {0, 0, 3, 1, 7, 5, 5, 4, 2, 3, 5, 1, 4, 5, 3, 6, 1, 6, 6, 6, 6, 2, 3, 5, 2, 2};
    public static final String[] DIMENSION_FACTION = {"", "royaumes:royaumes_mortels", "royaumes:ghyran", "royaumes:aqshy", "royaumes:chamon", "royaumes:ulgu", "royaumes:ulgu", "royaumes:hysh", "royaumes:ghur", "royaumes:ghyran", "royaumes:huit_points", "royaumes:aqshy", "royaumes:hysh", "royaumes:huit_points", "royaumes:ghyran", "royaumes:ulgu", "royaumes:aqshy", "royaumes:shyish", "royaumes:shyish", "royaumes:shyish", "royaumes:shyish", "royaumes:ghur", "royaumes:ghyran", "royaumes:ulgu", "royaumes:ghur", "royaumes:ghur"};

    /** Capacités de faction (touche R), index = numéro de faction. */
    public static final String[] CAP_NOMS = {"", "Frappe de foudre", "Salve de mousquets", "Rune de fureur", "Saut d'aethergold", "Danse de mort", "Marée spectrale", "Lumière de Teclis", "Comète céleste", "Bois enchevêtré", "Œil des Dieux", "Soif de sang", "Feu changeant", "Extase", "Miasme", "Fuite par la Warp", "Souffle de l'Ash", "Voile spectral", "Soif du vampire", "Mur d'os", "Festin", "Waaagh !", "Venin des marais", "Mauvaise Lune", "Charge de bedaine", "Piétinement"};
    public static final String[] CAP_DESC = {"", "Tu frappes comme la foudre : téléporté sur la cible, tu foudroies tout autour.", "Une salve de neuf traits part droit devant.", "Les runes d'ur-or s'embrasent : force, célérité, peau ignifuge.", "Tes endrins te propulsent dans les airs, puis tu planes.", "Tu tournoies, lames au clair, et blesses tout ce qui t'entoure.", "Une marée d'âmes noie tes ennemis dans l'obscurité.", "Un éclat de lumière pure brûle et aveugle les ennemis proches.", "Une comète tombe là où tu regardes.", "La forêt te soigne, toi et tes alliés, et entrave tes ennemis.", "Les Puissances te regardent : force et résistance.", "Le Dieu du Sang exige des crânes : tu frappes plus fort et plus vite.", "Cinq boules de feu changeant jaillissent de tes mains.", "Tes ennemis chancellent, ivres de sensations ; toi, tu danses.", "Un nuage de peste empoisonne et affame les ennemis proches.", "Tu traverses la Warp vingt blocs plus loin, invisible un instant.", "Un cône de feu et de cendres jaillit devant toi.", "Tu deviens spectre : invisible, rapide et insaisissable.", "Tu draines la vie de tes ennemis pour la faire tienne.", "Ton armure d'os se referme : résistance et absorption.", "Le banquet des Goules te rassasie et referme tes plaies.", "Deux brutes orruks répondent à ton cri de guerre.", "Une nappe de venin empoisonne et ralentit tes ennemis.", "Sous la Mauvaise Lune, deux squigs bondissent à tes côtés.", "Tu charges droit devant et renverses tout sur ton passage.", "Tu frappes le sol : les ennemis proches sont blessés et projetés."};
    public static final String[] CAP_TYPES = {"", "ECLAIR", "SALVE_FLECHES", "AURA", "ENVOL", "FRAPPE_SOI", "MALEDICTION", "FRAPPE_SOI", "COMETE", "SOIN", "AURA", "AURA", "SALVE_FEU", "MALEDICTION", "MALEDICTION", "TELEPORT", "CONE", "AURA", "DRAIN", "AURA", "SOIN", "INVOCATION", "MALEDICTION", "INVOCATION", "CHARGE", "FRAPPE_SOI"};
    public static final String[] CAP_EFFETS_SOI = {"", "resistance:1:100", "", "strength:1:400,haste:1:400,fire_resistance:0:400", "slow_falling:0:300", "speed:2:200,strength:0:200", "water_breathing:0:600", "", "", "regeneration:1:120", "strength:1:400,resistance:0:400", "strength:2:300,speed:0:300", "", "speed:1:200", "", "invisibility:0:100,speed:1:100", "fire_resistance:0:200", "invisibility:0:300,speed:1:300,resistance:1:300", "", "resistance:2:200,absorption:2:400", "saturation:0:20,regeneration:0:200", "strength:0:300", "", "", "resistance:0:60", ""};
    public static final String[] CAP_EFFETS_ENNEMIS = {"", "", "", "", "", "", "slowness:2:120,blindness:0:80", "glowing:0:200,blindness:0:60", "", "slowness:3:100", "", "", "", "nausea:0:160,weakness:1:160", "poison:1:160,hunger:1:200", "", "", "", "", "", "", "", "poison:1:140,slowness:1:140", "", "", "slowness:1:60"};
    public static final String[] CAP_PARTICULES = {"", "electric_spark", "crit", "flame", "cloud", "sweep_attack", "bubble_pop", "end_rod", "end_rod", "happy_villager", "smoke", "crimson_spore", "witch", "heart", "sneeze", "portal", "flame", "soul", "damage_indicator", "white_ash", "heart", "angry_villager", "item_slime", "squid_ink", "cloud", "explosion"};
    public static final String[] CAP_INVOCATIONS = {"", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "brute", "", "squig_hopper", "", ""};
    public static final float[] CAP_DEGATS = {0F, 10.0F, 7.0F, 0.0F, 0.0F, 8.0F, 4.0F, 8.0F, 14.0F, 10.0F, 0.0F, 0.0F, 0.0F, 3.0F, 2.0F, 0.0F, 8.0F, 0.0F, 5.0F, 0.0F, 12.0F, 0.0F, 3.0F, 0.0F, 9.0F, 10.0F};
    public static final float[] CAP_RAYONS = {0F, 3.5F, 0.0F, 0.0F, 0.0F, 4.0F, 8.0F, 7.0F, 5.0F, 6.0F, 0.0F, 0.0F, 0.0F, 8.0F, 7.0F, 20.0F, 9.0F, 0.0F, 6.0F, 0.0F, 0.0F, 0.0F, 7.0F, 0.0F, 3.0F, 6.0F};
    public static final int[] CAP_RECHARGES = {0, 45, 25, 60, 40, 30, 45, 45, 60, 50, 60, 60, 30, 45, 45, 30, 35, 50, 45, 60, 50, 90, 40, 90, 30, 40};

    /** Camp de guerre : unités recrutables par faction (de la plus modeste à la plus puissante). */
    public static final String[][] UNITES_CAMP = {
        {},
        {"liberator", "judicator", "prosecutor", "vindictor", "lord_celestant", "stardrake", "dracoth", "gryph_charger"},
        {"heaumefer", "cavalier_franc", "fusilier", "griffon", "demigryph", "dragon"},
        {"vulkite", "hearthguard", "auric_hearthguard", "magmadroth", "elementaire_magma", "salamandre"},
        {"arkanaute", "endrinrigger", "thunderer", "gunhauler", "fregate", "ironclad"},
        {"furie", "khinerai", "melusai", "avatar_khaine", "medusa", "ombre_khaine"},
        {"namarti_thrall", "namarti_reaver", "ishlaen", "leviadon", "allopex", "morrsarr"},
        {"sentinelle_vanari", "garde_vanari", "bladelord", "alarith", "hurakan", "scinari"},
        {"saurus", "skink", "kroxigor", "carnosaur", "stegadon", "bastiladon"},
        {"dryade", "revenant", "kurnoth", "treelord", "durthu", "treelord_ancien"},
        {"guerrier_chaos", "chevalier_chaos", "chosen", "warshrine", "prince_demon", "rejeton_chaos"},
        {"bloodletter", "blood_warrior", "bloodreaver", "skullreaper", "bloodthirster", "chien_khorne", "juggernaut"},
        {"tzaangor", "acolyte", "horreur_rose", "seigneur_changement", "char_flammes", "mutalith"},
        {"demonette", "seeker", "painbringer", "gardien_secrets", "syllesske", "demon_slaanesh"},
        {"plaguebearer", "blightking", "pusgoyle", "grand_immonde", "bete_nurgle"},
        {"clanrat", "stormvermin", "jezzail", "abomination", "rat_ogre", "doomwheel"},
        {"hashut", "bloodletter", "blood_warrior", "bloodreaver"},
        {"chainrasp", "grimghast", "hote_spirite", "carrosse_noir", "dreadblade", "mourngul"},
        {"dragon_zombie", "deathrattle", "grave_guard", "blood_knight", "vargheist", "bete_zombie", "vampire"},
        {"mortek", "kavalos", "immortis", "gothizzar", "morghast_archai", "morghast_harbinger"},
        {"goule", "horreur_crypte", "morbheg", "terrorgheist", "varghulf"},
        {"ardboy", "brute", "megaboss", "maw_krusha"},
        {"gutrippa", "mirebrute", "idole_rogue"},
        {"shoota", "squig_hopper", "stabba", "squig_mangler", "squig_colossal", "troggoth_dankhold"},
        {"glutton", "irongut", "leadbelcher", "stonehorn", "thundertusk", "sabre_givre"},
        {"mancrusher", "mega_gargant", "gatebreaker", "kraken_eater", "warstomper", "beast_smasher"},
    };

    /** Œufs : créature -> couleurs (fond, taches) pour l'aperçu. */
    public static final String[] OEUFS_MOBS = {"liberator", "judicator", "prosecutor", "vindictor", "lord_celestant", "stardrake", "dracoth", "gryph_charger", "heaumefer", "cavalier_franc", "fusilier", "griffon", "demigryph", "dragon", "furie", "khinerai", "melusai", "avatar_khaine", "medusa", "ombre_khaine", "vulkite", "hearthguard", "auric_hearthguard", "magmadroth", "elementaire_magma", "salamandre", "namarti_thrall", "namarti_reaver", "ishlaen", "leviadon", "allopex", "morrsarr", "arkanaute", "endrinrigger", "thunderer", "gunhauler", "fregate", "ironclad", "sentinelle_vanari", "garde_vanari", "bladelord", "alarith", "hurakan", "scinari", "saurus", "skink", "kroxigor", "carnosaur", "stegadon", "bastiladon", "dryade", "revenant", "kurnoth", "treelord", "durthu", "treelord_ancien", "guerrier_chaos", "chevalier_chaos", "chosen", "warshrine", "prince_demon", "rejeton_chaos", "tzaangor", "acolyte", "horreur_rose", "seigneur_changement", "char_flammes", "mutalith", "bloodletter", "blood_warrior", "bloodreaver", "skullreaper", "bloodthirster", "chien_khorne", "juggernaut", "demonette", "seeker", "painbringer", "gardien_secrets", "syllesske", "demon_slaanesh", "plaguebearer", "blightking", "pusgoyle", "grand_immonde", "bete_nurgle", "clanrat", "stormvermin", "jezzail", "abomination", "rat_ogre", "doomwheel", "hashut", "goule", "horreur_crypte", "morbheg", "terrorgheist", "dragon_zombie", "varghulf", "chainrasp", "grimghast", "hote_spirite", "carrosse_noir", "dreadblade", "mourngul", "mortek", "kavalos", "immortis", "gothizzar", "morghast_archai", "morghast_harbinger", "deathrattle", "grave_guard", "blood_knight", "vargheist", "bete_zombie", "vampire", "shoota", "squig_hopper", "stabba", "squig_mangler", "squig_colossal", "troggoth_dankhold", "glutton", "irongut", "leadbelcher", "stonehorn", "thundertusk", "sabre_givre", "ardboy", "brute", "gutrippa", "megaboss", "maw_krusha", "mirebrute", "idole_rogue", "mancrusher", "mega_gargant", "gatebreaker", "kraken_eater", "warstomper", "beast_smasher", "nagash", "archaon", "gordrakk", "skarbrand", "thanquol", "rotigus"};
    public static final String[] OEUFS_MONTURES = {"monture_dracoth", "monture_destrier", "monture_magmadroth", "monture_gunhauler", "monture_coursier_ombre", "monture_ishlaen", "monture_destrier_aube", "monture_aggradon", "monture_cerf_wyldwood", "monture_destrier_chaos", "monture_juggernaut", "monture_disque", "monture_seeker", "monture_pusgoyle", "monture_gnaw_beast", "monture_taurus", "monture_dreadblade", "monture_cauchemar", "monture_kavalos", "monture_morbheg", "monture_gore_grunta", "monture_gnashtoof", "monture_squig", "monture_mournfang", "monture_mammouth"};
}
