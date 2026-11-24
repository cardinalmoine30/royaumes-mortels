package fr.royaumes.rpg;

import fr.royaumes.ArsenalGenere;
import fr.royaumes.ContenuGenere;
import fr.royaumes.bloc.BlocPortail;
import fr.royaumes.magie.Magie;
import java.util.Random;
import net.minecraft.ChatFormatting;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.network.chat.Component;
import net.minecraft.resources.Identifier;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.world.entity.EquipmentSlot;
import net.minecraft.world.entity.item.ItemEntity;
import net.minecraft.world.entity.player.Inventory;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.scores.Objective;
import net.minecraft.world.scores.ReadOnlyScoreInfo;
import net.minecraft.world.scores.Scoreboard;
import net.minecraft.world.scores.criteria.ObjectiveCriteria;

/**
 * La Saga du Héros : une chaîne de quêtes qui sert de fil rouge et de tutoriel, du serment jusqu'à l'arme d'ascension,
 * puis des Contrats de chasse renouvelables. L'état vit dans le tableau des scores (rm_quete, rm_quete_n, rm_contrat…),
 * comme le reste du mod, pour rester lisible par le datapack.
 */
public final class Quetes {
    private Quetes() {}

    /** Une étape : type de condition, argument, objectif chiffré, gloire et objets offerts. */
    public record Etape(String titre, String texte, String type, String arg, int but, int gloire, String objets, String astuce) {}

    public static final Etape[] SAGA = {
        new Etape("Le Serment", "Prête serment à une faction (touche [serment]).", "score", "rm_faction", 1, 40, "",
                "25 factions en 4 Grandes Alliances. Tu reçois ton armure Soldat, une arme de départ et une Pierre de Royaume."),
        new Etape("Soldat de ta faction", "Équipe les 4 pièces de ton armure Soldat.", "panoplie", "0", 1, 60, "",
                "Panoplie complète d'une même faction = effets permanents, plus forts à chaque palier."),
        new Etape("Au-delà du voile", "Rejoins un des Royaumes Mortels.", "royaume", "", 1, 120, "minecraft:bread*8",
                "Clic droit avec la Pierre de Royaume reçue au serment. Plus tard : le Portail des Royaumes."),
        new Etape("Premier sang", "Abats des guerriers d'une autre Grande Alliance.", "tuer", "", 10, 120, "royaumes:pierre_royaumes_brute*4",
                "Dans les Royaumes, les créatures deviennent des guerriers de faction. Ceux de ton alliance ne t'attaquent pas."),
        new Etape("Le camp de guerre", "Plante l'Étendard de camp dans le monde de base.", "score", "rm_camp_niv", 1, 100, "",
                "Étendard : lingot d'or, bannière et pierre des Royaumes brute, en colonne. Pose-le puis clic droit dessus."),
        new Etape("Bâtisseur", "Construis un bâtiment de camp.", "batiment", "", 1, 100, "minecraft:iron_ingot*6",
                "Clic droit sur l'Étendard, onglet Bâtiments. Le Sanctuaire produit les éclats de ton Vent (pour la magie)."),
        new Etape("Premières armes", "Bâtis une Forge de guerre et forge une pièce Soldat.", "evt", "forge:0", 1, 120, "",
                "Forge de guerre : 3 lingots d'or, une enclume, 2 obsidiennes, pierre des Royaumes. Elle n'ouvre que TON arsenal."),
        new Etape("Le Vent en toi", "Lance un sort avec un bâton de ton Vent.", "evt", "saga:sort", 1, 100, "royaumes:cristal_arcanique*1",
                "Bâton : 2 lingots d'or, 2 bâtons et un éclat du Vent. Clic droit : sort ; accroupi + clic droit : grand sort."),
        new Etape("Pouvoir de faction", "Utilise ta capacité de faction (touche [capacite]).", "evt", "saga:capacite", 1, 100, "",
                "Chaque faction a la sienne, gratuite mais longue à recharger. Le HUD indique quand elle est prête."),
        new Etape("Héros reconnu", "Atteins le niveau 8.", "score", "rm_niveau", 8, 0, "minecraft:diamond*2,royaumes:cristal_arcanique*1",
                "La gloire vient des combats, des quêtes, des contrats et des découvertes. Chaque niveau donne un point de compétence."),
        new Etape("La Voie du héros", "Choisis ta voie : Guerrier, Mage ou Éclaireur.", "score", "rm_voie", 1, 120, "",
                "Touche [voie]. Un talent parmi deux aux niveaux 10, 20, 30 et 40."),
        new Etape("Matière étrangère", "Obtiens l'éclat d'un Vent qui n'est pas le tien.", "etranger", "", 1, 150, "",
                "Minerais et créatures des autres Royaumes, contrats de chasse, raids, ou échange avec un ami d'une autre faction."),
        new Etape("Élite", "Forge une pièce Élite (niveau 8).", "palier", "1", 1, 250, "minecraft:diamond*2",
                "Améliorer consomme la pièce du palier précédent : forge-la d'abord, puis monte-la."),
        new Etape("Raid victorieux", "Lance un raid depuis ton camp et reviens vainqueur.", "evt", "saga:raid", 1, 250, "",
                "Recrute des troupes (onglet Camp), puis onglet Raids. Plus le raid est long, plus le butin est gros."),
        new Etape("Fléau de l'ennemi", "Abats des guerriers ennemis.", "tuer", "", 40, 300, "minecraft:diamond*3", ""),
        new Etape("Champion", "Atteins le niveau 16.", "score", "rm_niveau", 16, 0, "minecraft:netherite_ingot*1", ""),
        new Etape("Légende", "Forge une pièce Légende (niveau 16).", "palier", "2", 1, 500, "minecraft:netherite_ingot*1",
                "Les seigneurs se mesurent en Légende : en dessous, même à plusieurs, le combat est perdu d'avance."),
        new Etape("Sur la piste d'un seigneur", "Fabrique un Œil de seigneur.", "objet", "royaumes:oeil_", 1, 300, "",
                "Œil de l'Ender, 2 éclats du Royaume du seigneur et pierre des Royaumes. Lance-le pour voir la direction de l'antre."),
        new Etape("Tueur de légendes", "Invoque un seigneur à son autel et vaincs-le.", "boss", "", 1, 500, "",
                "Forge son sceau (table de forgeron, voir le Codex) et utilise-le sur l'Autel des Seigneurs. Sous 25 % de vie : esquive les cercles !"),
        new Etape("Pourfendeur de seigneurs", "Vaincs encore des seigneurs.", "boss", "", 3, 700, "",
                "Chaque seigneur lâche des âmes. Sa relique est rare (10 % au premier combat), mais chaque échec rapproche de la suivante."),
        new Etape("Mythique", "Forge une pièce Mythique (niveau 25).", "palier", "3", 1, 800, "", "Il faut des âmes de seigneur."),
        new Etape("Héros mythique", "Atteins le niveau 35.", "score", "rm_niveau", 35, 0, "minecraft:nether_star*1", ""),
        new Etape("Divin", "Forge une pièce Divine (niveau 35).", "palier", "4", 1, 1200, "", "Étoile du Nether et âmes de seigneur."),
        new Etape("Ascension", "Éveille ton arme de champion à la Forge de guerre.", "objet", "_ascension", 1, 1500, "",
                "Lignée, puis champion, puis ascension : onglet Armes de la Forge de guerre."),
    };
    static final String[] NOMS_ALLIANCES = {"l'Ordre", "le Chaos", "la Mort", "la Destruction"};
    static final String[] ALLIANCES = {"ordre", "chaos", "mort", "destruction"};
    private static final Random R = new Random();

    // ------------------------------------------------------------------ scores

    static Objective obj(Scoreboard sb, String nom) {
        Objective o = sb.getObjective(nom);
        if (o == null) {
            o = sb.addObjective(nom, ObjectiveCriteria.DUMMY, Component.literal(nom), ObjectiveCriteria.RenderType.INTEGER, false, null);
        }
        return o;
    }

    public static int get(ServerPlayer p, String nom) {
        Scoreboard sb = p.level().getServer().getScoreboard();
        Objective o = sb.getObjective(nom);
        if (o == null) {
            return 0;
        }
        ReadOnlyScoreInfo i = sb.getPlayerScoreInfo(p, o);
        return i == null ? 0 : i.value();
    }

    public static void set(ServerPlayer p, String nom, int v) {
        Scoreboard sb = p.level().getServer().getScoreboard();
        sb.getOrCreatePlayerScore(p, obj(sb, nom)).set(v);
    }

    static int allianceJoueur(ServerPlayer p) {
        int f = get(p, "rm_faction");
        if (f <= 0 || f >= ContenuGenere.ALLIANCES.length) {
            return -1;
        }
        for (int i = 0; i < ALLIANCES.length; i++) {
            if (ALLIANCES[i].equals(ContenuGenere.ALLIANCES[f])) {
                return i;
            }
        }
        return -1;
    }

    /** Étape en cours (0-based), ou SAGA.length si la saga est achevée. */
    public static int etape(ServerPlayer p) {
        return Math.max(0, get(p, "rm_quete") - 1);
    }

    // ------------------------------------------------------------------ conditions

    static boolean possede(ServerPlayer p, java.util.function.Predicate<String> test) {
        Inventory inv = p.getInventory();
        for (int i = 0; i < inv.getContainerSize(); i++) {
            ItemStack s = inv.getItem(i);
            if (!s.isEmpty() && test.test(BuiltInRegistries.ITEM.getKey(s.getItem()).toString())) {
                return true;
            }
        }
        for (EquipmentSlot e : new EquipmentSlot[] {EquipmentSlot.HEAD, EquipmentSlot.CHEST, EquipmentSlot.LEGS, EquipmentSlot.FEET}) {
            ItemStack s = p.getItemBySlot(e);
            if (!s.isEmpty() && test.test(BuiltInRegistries.ITEM.getKey(s.getItem()).toString())) {
                return true;
            }
        }
        return false;
    }

    /** Un objet de l'arsenal de palier >= t (pièce ou outil). */
    static boolean palierAtteint(ServerPlayer p, int t) {
        return possede(p, id -> {
            if (!id.startsWith("royaumes:")) {
                return false;
            }
            for (int k = t; k < ArsenalGenere.PALIERS.length; k++) {
                if (id.endsWith("_" + ArsenalGenere.PALIERS[k])) {
                    return true;
                }
            }
            return false;
        });
    }

    static boolean panoplie(ServerPlayer p, int t) {
        int faction = -1;
        for (EquipmentSlot e : new EquipmentSlot[] {EquipmentSlot.HEAD, EquipmentSlot.CHEST, EquipmentSlot.LEGS, EquipmentSlot.FEET}) {
            if (!(p.getItemBySlot(e).getItem() instanceof fr.royaumes.arsenal.ArmureFaction a) || a.palier() < t
                    || (faction >= 0 && a.faction() != faction)) {
                return false;
            }
            faction = a.faction();
        }
        return faction == get(p, "rm_faction");
    }

    /** Progrès actuel de l'étape (pour les conditions d'état ; les compteurs vivent dans rm_quete_n). */
    static int progres(ServerPlayer p, Etape e) {
        return switch (e.type()) {
            case "score" -> Math.min(e.but(), get(p, e.arg()));
            case "batiment" -> {
                int n = 0;
                for (String b : fr.royaumes.camp.Batiments.IDS) {
                    n = Math.max(n, get(p, "rm_b_" + b));
                }
                yield Math.min(1, n);
            }
            case "palier" -> palierAtteint(p, Integer.parseInt(e.arg())) ? 1 : 0;
            case "panoplie" -> panoplie(p, Integer.parseInt(e.arg())) ? 1 : 0;
            case "royaume" -> Magie.ventDuLieu(p.level()) >= 0 ? 1 : 0;
            case "etranger" -> {
                int f = get(p, "rm_faction");
                int vent = f > 0 && f < ContenuGenere.VENT_FACTION.length ? ContenuGenere.VENT_FACTION[f] : -1;
                String mien = vent >= 0 ? "royaumes:eclat_" + ContenuGenere.VENTS[vent] : "";
                yield possede(p, id -> id.startsWith("royaumes:eclat_") && !id.equals(mien)) ? 1 : 0;
            }
            case "objet" -> possede(p, id -> e.arg().startsWith("royaumes:") ? id.startsWith(e.arg()) : id.endsWith(e.arg())) ? 1 : 0;
            default -> Math.min(e.but(), get(p, "rm_quete_n"));
        };
    }

    // ------------------------------------------------------------------ boucle (chaque seconde)

    public static void tick(ServerPlayer p) {
        int q = get(p, "rm_quete");
        if (q == 0) {
            set(p, "rm_quete", 1);
            set(p, "rm_quete_n", 0);
            annoncer(p, 0);
            return;
        }
        int i = q - 1;
        if (i < SAGA.length && progres(p, SAGA[i]) >= SAGA[i].but()) {
            accomplir(p, i);
        }
        if (q >= 5 && get(p, "rm_contrat") == 0 && get(p, "rm_faction") > 0) {
            nouveauContrat(p);
        }
    }

    static void accomplir(ServerPlayer p, int i) {
        Etape e = SAGA[i];
        set(p, "rm_quete", i + 2);
        set(p, "rm_quete_n", 0);
        BlocPortail.executer(p, "title @s subtitle {\"text\":\"" + e.titre().replace("\"", "'") + "\",\"color\":\"yellow\"}");
        BlocPortail.executer(p, "title @s title {\"text\":\"Quête accomplie\",\"color\":\"gold\",\"bold\":true}");
        BlocPortail.executer(p, "playsound minecraft:ui.toast.challenge_complete master @s ~ ~ ~ 0.8 1");
        recompenser(p, e.gloire(), e.objets());
        if (i + 1 < SAGA.length) {
            annoncer(p, i + 1);
        } else {
            p.sendSystemMessage(Component.literal("✦ La Saga du Héros est achevée : tu es l'Élu des Dieux. Les Contrats de chasse continuent.")
                    .withStyle(ChatFormatting.GOLD, ChatFormatting.BOLD));
        }
    }

    /** À la connexion : rappelle la quête en cours. */
    public static void rappel(ServerPlayer p) {
        int i = etape(p);
        if (get(p, "rm_quete") > 0 && i < SAGA.length) {
            annoncer(p, i);
        }
    }

    /** Texte de chat où [serment], [capacite], [voie] deviennent la touche configurée par le joueur. */
    public static net.minecraft.network.chat.MutableComponent avecTouches(String s) {
        net.minecraft.network.chat.MutableComponent c = Component.empty();
        java.util.regex.Matcher m = java.util.regex.Pattern.compile("\\[(serment|capacite|voie)\\]").matcher(s);
        int debut = 0;
        while (m.find()) {
            c.append(s.substring(debut, m.start()));
            c.append(Component.keybind("key.royaumes." + m.group(1)));
            debut = m.end();
        }
        return c.append(s.substring(debut));
    }

    static void annoncer(ServerPlayer p, int i) {
        Etape e = SAGA[i];
        p.sendSystemMessage(Component.literal("✦ Saga du Héros " + (i + 1) + "/" + SAGA.length + " : ").withStyle(ChatFormatting.GOLD)
                .append(Component.literal(e.titre()).withStyle(ChatFormatting.YELLOW))
                .append(avecTouches(" — " + e.texte() + (e.but() > 1 ? " (" + e.but() + ")" : "")).withStyle(ChatFormatting.GRAY)));
        if (!e.astuce().isEmpty()) {
            p.sendSystemMessage(avecTouches("  ➜ " + e.astuce()).withStyle(ChatFormatting.DARK_AQUA));
        }
    }

    static void recompenser(ServerPlayer p, int gloire, String objets) {
        if (gloire > 0) {
            BlocPortail.executer(p, "scoreboard players set #gain rm_tmp " + gloire);
            BlocPortail.executer(p, "function royaumes:rpg/ajouter");
        }
        StringBuilder txt = new StringBuilder(gloire > 0 ? "+" + gloire + " gloire" : "");
        if (!objets.isEmpty()) {
            for (String o : objets.split(",")) {
                String[] a = o.split("\\*");
                Item it = BuiltInRegistries.ITEM.getValue(Identifier.parse(a[0]));
                ItemStack s = new ItemStack(it, Integer.parseInt(a[1]));
                txt.append(txt.length() > 0 ? ", " : "").append(a[1]).append(" × ").append(s.getHoverName().getString());
                if (!p.getInventory().add(s)) {
                    p.level().addFreshEntity(new ItemEntity(p.level(), p.getX(), p.getY() + 0.5, p.getZ(), s));
                }
            }
        }
        if (txt.length() > 0) {
            p.sendSystemMessage(Component.literal("  Récompense : " + txt).withStyle(ChatFormatting.GREEN));
        }
    }

    // ------------------------------------------------------------------ événements

    /** Événement ponctuel (saga:sort, saga:raid…) : avance une étape de type « evt » qui l'attend. */
    public static void evenement(ServerPlayer p, String cle) {
        int i = etape(p);
        if (i < SAGA.length && SAGA[i].type().equals("evt") && SAGA[i].arg().equals(cle)) {
            set(p, "rm_quete_n", get(p, "rm_quete_n") + 1);
        }
    }

    /** Un seigneur vaincu (crédité à tous les héros de son combat). */
    public static void seigneur(ServerPlayer p) {
        int i = etape(p);
        if (i < SAGA.length && SAGA[i].type().equals("boss")) {
            set(p, "rm_quete_n", get(p, "rm_quete_n") + 1);
        }
    }

    /** Un guerrier d'une autre alliance abattu. */
    public static void tuer(ServerPlayer p, String allianceVictime) {
        int mien = allianceJoueur(p);
        if (mien < 0 || ALLIANCES[mien].equals(allianceVictime)) {
            return;
        }
        int i = etape(p);
        if (i < SAGA.length && SAGA[i].type().equals("tuer")) {
            set(p, "rm_quete_n", get(p, "rm_quete_n") + 1);
        }
        int c = get(p, "rm_contrat");
        if (c > 0 && ALLIANCES[c - 1].equals(allianceVictime)) {
            int n = get(p, "rm_contrat_n") + 1;
            set(p, "rm_contrat_n", n);
            int but = get(p, "rm_contrat_but");
            if (n >= but) {
                int niveau = Math.max(1, get(p, "rm_niveau"));
                p.sendSystemMessage(Component.literal("⚔ Contrat rempli : " + but + " guerriers de " + NOMS_ALLIANCES[c - 1] + " abattus.")
                        .withStyle(ChatFormatting.GOLD));
                BlocPortail.executer(p, "playsound minecraft:entity.player.levelup master @s ~ ~ ~ 0.7 1.2");
                String eclat = "royaumes:eclat_" + ContenuGenere.VENTS[R.nextInt(ContenuGenere.VENTS.length)];
                recompenser(p, 5 * but + 3 * niveau, eclat + "*" + (1 + niveau / 15) + ",royaumes:pierre_royaumes_brute*2");
                set(p, "rm_contrat", 0);
            }
        }
    }

    static void nouveauContrat(ServerPlayer p) {
        int mien = allianceJoueur(p);
        int a;
        do {
            a = R.nextInt(ALLIANCES.length);
        } while (a == mien);
        int but = Math.min(30, 10 + Math.max(1, get(p, "rm_niveau")) / 2);
        set(p, "rm_contrat", a + 1);
        set(p, "rm_contrat_n", 0);
        set(p, "rm_contrat_but", but);
        p.sendSystemMessage(Component.literal("⚔ Nouveau contrat de chasse : abats " + but + " guerriers de " + NOMS_ALLIANCES[a] + ".")
                .withStyle(ChatFormatting.DARK_AQUA));
    }

    // ------------------------------------------------------------------ affichage (envoyé au client avec la fiche)

    /** {titre, texte} de l'étape en cours, et progrès/but ; contrat en texte. */
    public static String[] textes(ServerPlayer p) {
        int i = etape(p);
        String q = i < SAGA.length ? (i + 1) + "/" + SAGA.length + " · " + SAGA[i].titre() : "Saga achevée · Élu des Dieux";
        String d = i < SAGA.length ? SAGA[i].texte() : "";
        int c = get(p, "rm_contrat");
        String contrat = c > 0 ? "Contrat : guerriers de " + NOMS_ALLIANCES[c - 1] : "";
        return new String[] {q, d, contrat};
    }

    public static int[] nombres(ServerPlayer p) {
        int i = etape(p);
        int prog = i < SAGA.length ? progres(p, SAGA[i]) : 0;
        int but = i < SAGA.length ? SAGA[i].but() : 0;
        return new int[] {prog, but, get(p, "rm_contrat_n"), get(p, "rm_contrat_but"), Voies.voie(p), get(p, "rm_talents")};
    }
}
