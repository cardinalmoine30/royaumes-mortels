package fr.royaumes.camp;

import fr.royaumes.ContenuGenere;
import fr.royaumes.FactionsGenerees;
import fr.royaumes.ModEntites;
import fr.royaumes.ModObjets;
import fr.royaumes.Profil;
import fr.royaumes.entite.Combattant;
import fr.royaumes.magie.Magie;
import fr.royaumes.magie.Saga;
import fr.royaumes.reseau.FicheCamp;
import java.util.ArrayList;
import java.util.Comparator;
import java.util.List;
import java.util.Random;
import java.util.UUID;
import net.minecraft.ChatFormatting;
import net.minecraft.core.BlockPos;
import net.minecraft.core.particles.ParticleTypes;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.core.registries.Registries;
import net.minecraft.network.chat.Component;
import net.minecraft.resources.Identifier;
import net.minecraft.resources.ResourceKey;
import net.minecraft.server.MinecraftServer;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.sounds.SoundSource;
import net.minecraft.world.entity.Entity;
import net.minecraft.world.entity.EntitySpawnReason;
import net.minecraft.world.entity.player.Inventory;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.level.Level;
import net.minecraft.world.phys.AABB;
import net.minecraft.world.scores.Objective;
import net.minecraft.world.scores.ReadOnlyScoreInfo;
import net.minecraft.world.scores.ScoreHolder;
import net.minecraft.world.scores.Scoreboard;
import net.minecraft.world.scores.criteria.ObjectiveCriteria;
import net.neoforged.neoforge.network.PacketDistributor;

/**
 * Camp de guerre (« Minecolonies » simplifié) : un étendard par héros, du butin, des unités de sa faction
 * qui gardent le camp ou suivent le héros, des raids qui rapportent du butin, et des bandes ennemies
 * qui attaquent le camp. Tout l'état est dans le scoreboard (rm_camp_*, rm_butin, rm_raid_*),
 * les unités sont des Combattant marqués rm_unite et rm_chef_<uuid>.
 */
public final class Camps {
    public static final String UNITE = "rm_unite";
    public static final String[] DIMS = {"minecraft:overworld", "minecraft:the_nether", "minecraft:the_end", "royaumes:royaumes_mortels",
            "royaumes:aqshy", "royaumes:ghur", "royaumes:ghyran", "royaumes:hysh", "royaumes:ulgu", "royaumes:shyish", "royaumes:chamon", "royaumes:huit_points"};
    /** Raids : nom, durée (s), difficulté, butin de base. */
    public static final String[] RAIDS = {"Pillage", "Assaut", "Croisade"};
    public static final int[] RAID_DUREE = {120, 300, 600};
    public static final int[] RAID_DIFF = {15, 40, 90};
    public static final int[] RAID_BUTIN = {25, 70, 160};
    public static final int[] COUT_NIVEAU = {0, 0, 60, 150, 300, 600};
    public static final int NIVEAU_MAX = 5;
    private static final int RAYON = 16;
    private static final Random R = new Random();

    private Camps() {}

    // ------------------------------------------------------------------ scoreboard

    static Objective obj(Scoreboard sb, String nom) {
        Objective o = sb.getObjective(nom);
        if (o == null) {
            o = sb.addObjective(nom, ObjectiveCriteria.DUMMY, Component.literal(nom), ObjectiveCriteria.RenderType.INTEGER, false, null);
        }
        return o;
    }

    static int get(Scoreboard sb, ScoreHolder h, String nom) {
        Objective o = sb.getObjective(nom);
        if (o == null) {
            return 0;
        }
        ReadOnlyScoreInfo i = sb.getPlayerScoreInfo(h, o);
        return i == null ? 0 : i.value();
    }

    static void set(Scoreboard sb, ScoreHolder h, String nom, int v) {
        sb.getOrCreatePlayerScore(h, obj(sb, nom)).set(v);
    }

    private static Scoreboard sb(ServerPlayer p) {
        return p.level().getServer().getScoreboard();
    }

    static int maintenant(MinecraftServer s) {
        return (int) (s.overworld().getGameTime() / 20);
    }

    public static int maxUnites(int niveau) {
        return 2 + 2 * niveau;
    }

    // ------------------------------------------------------------------ unités recrutables

    static int puissance(String id) {
        Profil p = ModEntites.PROFILS.get(id);
        return p == null ? 10 : (int) (p.pv() + p.degats() * 4 + p.armure() * 2);
    }

    public static int cout(String id) {
        return Math.max(10, puissance(id) / 3);
    }

    /** Unités de la faction, de la moins chère à la plus chère. */
    public static List<String> recrutables(int faction) {
        List<String> l = new ArrayList<>();
        if (faction > 0 && faction < ContenuGenere.UNITES_CAMP.length) {
            for (String id : ContenuGenere.UNITES_CAMP[faction]) {
                if (ModEntites.ENTITES.containsKey(id)) {
                    l.add(id);
                }
            }
        }
        l.sort(Comparator.comparingInt(Camps::cout));
        return l;
    }

    /** Nombre de types d'unités débloqués au niveau donné. */
    public static int debloquees(int niveau) {
        return Math.min(8, 1 + niveau);
    }

    // ------------------------------------------------------------------ lieu du camp

    static ServerLevel niveauCamp(MinecraftServer s, int dim) {
        if (dim < 0 || dim >= DIMS.length) {
            return null;
        }
        return s.getLevel(ResourceKey.create(Registries.DIMENSION, Identifier.parse(DIMS[dim])));
    }

    static int indexDim(Level l) {
        for (int i = 0; i < DIMS.length; i++) {
            if (Magie.estDans(l, DIMS[i])) {
                return i;
            }
        }
        return 0;
    }

    static BlockPos pos(Scoreboard sb, ScoreHolder h) {
        return new BlockPos(get(sb, h, "rm_camp_x"), get(sb, h, "rm_camp_y"), get(sb, h, "rm_camp_z"));
    }

    public static boolean aUnCamp(ServerPlayer p) {
        return get(sb(p), p, "rm_camp_niv") > 0;
    }

    static boolean estSonEtendard(ServerPlayer p, BlockPos pos) {
        Scoreboard sb = sb(p);
        return aUnCamp(p) && pos(sb, p).equals(pos) && get(sb, p, "rm_camp_dim") == indexDim(p.level());
    }

    // ------------------------------------------------------------------ actions

    public static void fonder(ServerPlayer p, BlockPos pos) {
        Scoreboard sb = sb(p);
        set(sb, p, "rm_camp_x", pos.getX());
        set(sb, p, "rm_camp_y", pos.getY());
        set(sb, p, "rm_camp_z", pos.getZ());
        set(sb, p, "rm_camp_dim", indexDim(p.level()));
        if (get(sb, p, "rm_camp_niv") < 1) {
            set(sb, p, "rm_camp_niv", 1);
        }
        if (get(sb, p, "rm_camp_att") == 0) {
            set(sb, p, "rm_camp_att", maintenant(p.level().getServer()) + 1200);
        }
        p.sendSystemMessage(Component.translatable("royaumes.camp.fonde").withStyle(ChatFormatting.GOLD));
        p.level().playSound(null, pos, SoundEvents.BEACON_ACTIVATE, SoundSource.PLAYERS, 1.0F, 1.0F);
        Saga.accorder(p, "camp");
    }

    public static void ouvrir(ServerPlayer p, BlockPos pos) {
        if (!estSonEtendard(p, pos)) {
            if (!aUnCamp(p)) {
                fonder(p, pos);
            } else {
                p.sendOverlayMessage(Component.translatable("royaumes.camp.pas_a_toi").withStyle(ChatFormatting.GRAY));
                return;
            }
        }
        envoyer(p, true);
    }

    public static void action(ServerPlayer p, int action, int arg) {
        Scoreboard sb = sb(p);
        if (!aUnCamp(p)) {
            return;
        }
        BlockPos camp = pos(sb, p);
        boolean pres = get(sb, p, "rm_camp_dim") == indexDim(p.level()) && p.blockPosition().closerThan(camp, 12);
        int faction = get(sb, p, "rm_faction");
        int niveau = get(sb, p, "rm_camp_niv");
        switch (action) {
            case 1 -> { // recruter
                List<String> l = recrutables(faction);
                if (!pres || arg < 0 || arg >= Math.min(l.size(), debloquees(niveau))) {
                    return;
                }
                if (get(sb, p, "rm_camp_nb") >= maxUnites(niveau)) {
                    msg(p, "Ton camp est plein : améliore-le pour accueillir plus de troupes.", ChatFormatting.RED);
                    break;
                }
                int c = cout(l.get(arg));
                if (get(sb, p, "rm_butin") < c) {
                    msg(p, "Pas assez de butin (" + c + " requis).", ChatFormatting.RED);
                    break;
                }
                if (invoquer(p, p.level(), camp, l.get(arg), 1) > 0) {
                    set(sb, p, "rm_butin", get(sb, p, "rm_butin") - c);
                    set(sb, p, "rm_camp_nb", get(sb, p, "rm_camp_nb") + 1);
                }
            }
            case 2 -> { // améliorer
                if (niveau >= NIVEAU_MAX) {
                    return;
                }
                int c = COUT_NIVEAU[niveau + 1];
                if (get(sb, p, "rm_butin") < c) {
                    msg(p, "Pas assez de butin (" + c + " requis).", ChatFormatting.RED);
                    break;
                }
                set(sb, p, "rm_butin", get(sb, p, "rm_butin") - c);
                set(sb, p, "rm_camp_niv", niveau + 1);
                ((ServerLevel) p.level()).sendParticles(ParticleTypes.TOTEM_OF_UNDYING, camp.getX() + 0.5, camp.getY() + 1.5, camp.getZ() + 0.5, 60, 0.6, 1, 0.6, 0.3);
                msg(p, "Le camp passe au niveau " + (niveau + 1) + " : " + maxUnites(niveau + 1) + " troupes, nouvelles unités.", ChatFormatting.GOLD);
            }
            case 3 -> deposer(p);
            case 4 -> set(sb, p, "rm_camp_ordre", arg == 1 ? 1 : 0);
            case 5 -> lancerRaid(p, arg);
            default -> {
            }
        }
        envoyer(p, false);
    }

    private static void msg(ServerPlayer p, String s, ChatFormatting c) {
        p.sendSystemMessage(Component.literal(s).withStyle(c));
    }

    /** Valeur en butin des objets qu'on peut déposer au camp. */
    static int valeur(ItemStack s) {
        Identifier id = BuiltInRegistries.ITEM.getKey(s.getItem());
        String n = id.toString();
        return switch (n) {
            case "minecraft:iron_ingot", "minecraft:copper_ingot" -> 1;
            case "minecraft:gold_ingot" -> 4;
            case "minecraft:emerald" -> 6;
            case "minecraft:diamond" -> 12;
            case "minecraft:netherite_ingot" -> 40;
            case "minecraft:gold_block" -> 36;
            case "minecraft:iron_block" -> 9;
            case "minecraft:emerald_block" -> 54;
            case "royaumes:pierre_royaumes_brute" -> 5;
            case "royaumes:cristal_arcanique" -> 8;
            default -> n.startsWith("royaumes:eclat_") ? 6 : 0;
        };
    }

    private static void deposer(ServerPlayer p) {
        Inventory inv = p.getInventory();
        int total = 0;
        for (int i = 0; i < inv.getContainerSize(); i++) {
            ItemStack s = inv.getItem(i);
            int v = valeur(s);
            if (v > 0 && !s.isEmpty()) {
                total += v * s.getCount();
                inv.setItem(i, ItemStack.EMPTY);
            }
        }
        if (total > 0) {
            Scoreboard sb = sb(p);
            set(sb, p, "rm_butin", get(sb, p, "rm_butin") + total);
            p.level().playSound(null, p.blockPosition(), SoundEvents.ANVIL_LAND, SoundSource.PLAYERS, 0.5F, 1.6F);
            msg(p, "+" + total + " butin déposé au camp.", ChatFormatting.GOLD);
        } else {
            msg(p, "Rien à déposer : lingots, gemmes, pierre des Royaumes, cristaux, éclats.", ChatFormatting.GRAY);
        }
    }

    /** Fait apparaître n unités alliées autour du camp ; renvoie le nombre apparu. */
    static int invoquer(ServerPlayer chef, Level l, BlockPos camp, String id, int n) {
        var type = ModEntites.ENTITES.get(id);
        if (type == null || !(l instanceof ServerLevel sl)) {
            return 0;
        }
        int ok = 0;
        for (int i = 0; i < n; i++) {
            Entity e = type.get().create(sl, EntitySpawnReason.MOB_SUMMONED);
            if (!(e instanceof Combattant c)) {
                continue;
            }
            double a = R.nextDouble() * Math.PI * 2;
            c.setPos(camp.getX() + 0.5 + Math.cos(a) * 3, camp.getY(), camp.getZ() + 0.5 + Math.sin(a) * 3);
            c.setPersistenceRequired();
            c.addTag(UNITE);
            c.addTag("rm_chef_" + chef.getUUID());
            c.addTag("rm_nom_" + chef.getScoreboardName());
            sl.addFreshEntity(c);
            sl.sendParticles(ParticleTypes.CLOUD, c.getX(), c.getY() + 1, c.getZ(), 15, 0.4, 0.6, 0.4, 0.02);
            ok++;
        }
        sl.playSound(null, camp, SoundEvents.EVOKER_PREPARE_SUMMON, SoundSource.PLAYERS, 0.6F, 1.2F);
        return ok;
    }

    /** Unités du joueur chargées autour d'un point. */
    static List<Combattant> unites(ServerLevel l, ServerPlayer chef, BlockPos centre, double rayon) {
        String tag = "rm_chef_" + chef.getUUID();
        return l.getEntitiesOfClass(Combattant.class, new AABB(centre).inflate(rayon), c -> c.isAlive() && c.getTags().contains(tag));
    }

    // ------------------------------------------------------------------ raids

    private static void lancerRaid(ServerPlayer p, int type) {
        Scoreboard sb = sb(p);
        if (type < 0 || type >= RAIDS.length || get(sb, p, "rm_raid_fin") > 0) {
            return;
        }
        BlockPos camp = pos(sb, p);
        ServerLevel l = niveauCamp(p.level().getServer(), get(sb, p, "rm_camp_dim"));
        if (l == null) {
            return;
        }
        List<Combattant> troupe = unites(l, p, camp, 32);
        if (troupe.isEmpty()) {
            msg(p, "Aucune troupe au camp : recrute des unités, ou ramène-les près de l'étendard.", ChatFormatting.RED);
            return;
        }
        List<String> types = recrutables(get(sb, p, "rm_faction"));
        int force = 0;
        int[] compte = new int[8];
        for (Combattant c : troupe) {
            String id = BuiltInRegistries.ENTITY_TYPE.getKey(c.getType()).getPath();
            int k = types.indexOf(id);
            if (k >= 0 && k < 8) {
                compte[k]++;
            }
            force += puissance(id) / 10;
            l.sendParticles(ParticleTypes.CAMPFIRE_COSY_SMOKE, c.getX(), c.getY() + 1, c.getZ(), 4, 0.3, 0.5, 0.3, 0.02);
            c.discard();
        }
        for (int k = 0; k < 8; k++) {
            set(sb, p, "rm_raid_u" + k, compte[k]);
        }
        set(sb, p, "rm_raid_type", type);
        set(sb, p, "rm_raid_force", force);
        set(sb, p, "rm_raid_fin", maintenant(p.level().getServer()) + RAID_DUREE[type]);
        set(sb, p, "rm_camp_nb", Math.max(0, get(sb, p, "rm_camp_nb") - troupe.size()));
        l.playSound(null, camp, SoundEvents.EVOKER_PREPARE_SUMMON, SoundSource.PLAYERS, 1.2F, 1.0F);
        msg(p, "⚔ " + troupe.size() + " guerriers partent en " + RAIDS[type].toLowerCase() + " (force " + force
                + " contre " + RAID_DIFF[type] + "). Retour dans " + RAID_DUREE[type] / 60 + " min.", ChatFormatting.GOLD);
    }

    private static void finirRaid(ServerPlayer p) {
        Scoreboard sb = sb(p);
        int type = Math.max(0, Math.min(2, get(sb, p, "rm_raid_type")));
        int force = get(sb, p, "rm_raid_force");
        int diff = RAID_DIFF[type];
        double chance = force / (double) (force + diff);
        boolean victoire = R.nextDouble() < chance;
        double risque = victoire ? 0.3 * diff / (force + diff) : 0.5;
        List<String> types = recrutables(get(sb, p, "rm_faction"));
        BlockPos camp = pos(sb, p);
        ServerLevel l = niveauCamp(p.level().getServer(), get(sb, p, "rm_camp_dim"));
        int partis = 0;
        int revenus = 0;
        for (int k = 0; k < 8; k++) {
            int n = get(sb, p, "rm_raid_u" + k);
            partis += n;
            int vivants = 0;
            for (int i = 0; i < n; i++) {
                if (R.nextDouble() >= risque) {
                    vivants++;
                }
            }
            if (vivants > 0 && k < types.size() && l != null) {
                revenus += invoquer(p, l, camp, types.get(k), vivants);
            }
            set(sb, p, "rm_raid_u" + k, 0);
        }
        set(sb, p, "rm_camp_nb", get(sb, p, "rm_camp_nb") + revenus);
        int butin = (int) (RAID_BUTIN[type] * (victoire ? 0.8 + R.nextDouble() * 0.6 : 0.2));
        set(sb, p, "rm_butin", get(sb, p, "rm_butin") + butin);
        set(sb, p, "rm_raid_fin", 0);
        if (victoire) {
            donner(p, new ItemStack(ModObjets.PIERRE_BRUTE.get(), 1 + type * 2 + R.nextInt(3)));
            if (type >= 1) {
                donner(p, new ItemStack(ModObjets.CRISTAL.get(), type));
            }
            if (type == 2) {
                donner(p, new ItemStack(ModObjets.ECLATS.get(R.nextInt(ModObjets.ECLATS.size())).get(), 2));
            }
            set(sb, p, "rm_gloire", get(sb, p, "rm_gloire") + diff);
            Saga.accorder(p, "raid");
        }
        p.sendSystemMessage(Component.literal((victoire ? "✦ Victoire ! " : "✖ Défaite… ") + RAIDS[type] + " terminé : "
                + revenus + "/" + partis + " guerriers rentrent, +" + butin + " butin" + (victoire ? ", +" + diff + " gloire." : "."))
                .withStyle(victoire ? ChatFormatting.GOLD : ChatFormatting.RED));
        p.level().playSound(null, p.blockPosition(), victoire ? SoundEvents.PLAYER_LEVELUP : SoundEvents.WITHER_SHOOT, SoundSource.PLAYERS, 0.8F, 1.0F);
    }

    private static void donner(ServerPlayer p, ItemStack s) {
        if (!p.getInventory().add(s)) {
            p.drop(s, false);
        }
    }

    // ------------------------------------------------------------------ attaques ennemies

    private static void attaque(ServerPlayer p) {
        Scoreboard sb = sb(p);
        int niveau = get(sb, p, "rm_camp_niv");
        BlockPos camp = pos(sb, p);
        if (niveau < 2 || get(sb, p, "rm_camp_dim") != indexDim(p.level()) || !p.blockPosition().closerThan(camp, 80)) {
            return;
        }
        String mien = ContenuGenere.ALLIANCES[Math.max(0, get(sb, p, "rm_faction"))];
        List<Integer> ennemies = new ArrayList<>();
        for (int f = 1; f < ContenuGenere.ALLIANCES.length; f++) {
            if (!ContenuGenere.ALLIANCES[f].equals(mien) && recrutables(f).size() >= 2) {
                ennemies.add(f);
            }
        }
        if (ennemies.isEmpty()) {
            return;
        }
        int f = ennemies.get(R.nextInt(ennemies.size()));
        List<String> types = recrutables(f);
        ServerLevel l = (ServerLevel) p.level();
        double a = R.nextDouble() * Math.PI * 2;
        int n = 1 + niveau;
        for (int i = 0; i < n; i++) {
            var t = ModEntites.ENTITES.get(types.get(Math.min(types.size() - 1, R.nextInt(Math.min(types.size(), 1 + niveau / 2)))));
            Entity e = t.get().create(l, EntitySpawnReason.EVENT);
            if (e == null) {
                continue;
            }
            int x = camp.getX() + (int) (Math.cos(a) * 22) + R.nextInt(5) - 2;
            int z = camp.getZ() + (int) (Math.sin(a) * 22) + R.nextInt(5) - 2;
            int y = l.getHeight(net.minecraft.world.level.levelgen.Heightmap.Types.MOTION_BLOCKING_NO_LEAVES, x, z);
            e.setPos(x + 0.5, y, z + 0.5);
            e.addTag("rm_assaillant");
            l.addFreshEntity(e);
        }
        l.playSound(null, camp, SoundEvents.ENDER_DRAGON_GROWL, SoundSource.HOSTILE, 1.0F, 1.4F);
        msg(p, "⚠ Une bande de " + FactionsGenerees.NOMS[f] + " attaque ton camp ! (" + n + " guerriers)", ChatFormatting.DARK_RED);
    }

    // ------------------------------------------------------------------ tic serveur et comportement des unités

    /** Chaque seconde, pour chaque joueur connecté. */
    public static void tickJoueur(ServerPlayer p) {
        Scoreboard sb = sb(p);
        if (!aUnCamp(p)) {
            return;
        }
        int t = maintenant(p.level().getServer());
        int fin = get(sb, p, "rm_raid_fin");
        if (fin > 0 && t >= fin) {
            finirRaid(p);
        }
        int att = get(sb, p, "rm_camp_att");
        if (att > 0 && t >= att) {
            set(sb, p, "rm_camp_att", t + 1200 + R.nextInt(600));
            attaque(p);
        }
    }

    /** Chaque seconde, pour chaque unité chargée : garder le camp ou suivre le chef. */
    public static void tickUnite(Combattant c) {
        MinecraftServer s = c.level().getServer();
        if (s == null) {
            return;
        }
        UUID chef = null;
        String nom = null;
        for (String tag : c.getTags()) {
            if (tag.startsWith("rm_chef_")) {
                try {
                    chef = UUID.fromString(tag.substring(8));
                } catch (IllegalArgumentException e) {
                    return;
                }
            } else if (tag.startsWith("rm_nom_")) {
                nom = tag.substring(7);
            }
        }
        if (chef == null || nom == null || c.getTarget() != null) {
            return;
        }
        Scoreboard sb = s.getScoreboard();
        ScoreHolder h = ScoreHolder.forNameOnly(nom);
        ServerPlayer p = s.getPlayerList().getPlayer(chef);
        if (p != null && get(sb, h, "rm_camp_ordre") == 1 && p.level() == c.level()) {
            double d = c.distanceTo(p);
            if (d > 40) {
                c.teleportTo(p.getX() + R.nextInt(3) - 1, p.getY(), p.getZ() + R.nextInt(3) - 1);
            } else if (d > 6) {
                c.getNavigation().moveTo(p, 1.25);
            }
            return;
        }
        if (get(sb, h, "rm_camp_niv") > 0 && indexDim(c.level()) == get(sb, h, "rm_camp_dim")) {
            BlockPos camp = pos(sb, h);
            if (!c.blockPosition().closerThan(camp, RAYON)) {
                c.getNavigation().moveTo(camp.getX() + 0.5, camp.getY(), camp.getZ() + 0.5, 1.0);
            }
        }
    }

    /** Une unité est morte : une place se libère au camp. */
    public static void mortUnite(Combattant c) {
        MinecraftServer s = c.level().getServer();
        if (s == null) {
            return;
        }
        for (String tag : c.getTags()) {
            if (tag.startsWith("rm_nom_")) {
                ScoreHolder h = ScoreHolder.forNameOnly(tag.substring(7));
                set(s.getScoreboard(), h, "rm_camp_nb", Math.max(0, get(s.getScoreboard(), h, "rm_camp_nb") - 1));
            }
        }
    }

    // ------------------------------------------------------------------ fiche envoyée au client

    public static void envoyer(ServerPlayer p, boolean ouvrir) {
        Scoreboard sb = sb(p);
        int faction = get(sb, p, "rm_faction");
        int niveau = get(sb, p, "rm_camp_niv");
        List<String> l = recrutables(faction);
        List<Integer> couts = new ArrayList<>();
        for (String id : l) {
            couts.add(cout(id));
        }
        int fin = get(sb, p, "rm_raid_fin");
        int reste = fin > 0 ? Math.max(0, fin - maintenant(p.level().getServer())) : -1;
        int force = 0;
        ServerLevel lc = niveauCamp(p.level().getServer(), get(sb, p, "rm_camp_dim"));
        if (lc != null) {
            for (Combattant c : unites(lc, p, pos(sb, p), 32)) {
                force += puissance(BuiltInRegistries.ENTITY_TYPE.getKey(c.getType()).getPath()) / 10;
            }
        }
        FicheCamp fiche = new FicheCamp(ouvrir, faction, niveau, get(sb, p, "rm_butin"), get(sb, p, "rm_camp_nb"), maxUnites(niveau),
                get(sb, p, "rm_camp_ordre"), get(sb, p, "rm_raid_type"), reste, force,
                niveau < NIVEAU_MAX ? COUT_NIVEAU[niveau + 1] : 0, debloquees(niveau), l, couts);
        try {
            PacketDistributor.sendToPlayer(p, fiche);
        } catch (RuntimeException e) {
            // client sans le mod
        }
    }
}
