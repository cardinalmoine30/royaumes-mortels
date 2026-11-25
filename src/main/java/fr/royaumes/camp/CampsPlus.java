package fr.royaumes.camp;

import fr.royaumes.ContenuGenere;
import fr.royaumes.ModObjets;
import fr.royaumes.entite.Combattant;
import fr.royaumes.magie.Saga;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Random;
import java.util.UUID;
import net.minecraft.ChatFormatting;
import net.minecraft.core.BlockPos;
import net.minecraft.core.particles.ParticleTypes;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.network.chat.Component;
import net.minecraft.server.MinecraftServer;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.sounds.SoundSource;
import net.minecraft.world.entity.LivingEntity;
import net.minecraft.world.entity.player.Inventory;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.Items;
import net.minecraft.world.scores.Objective;
import net.minecraft.world.scores.PlayerScoreEntry;
import net.minecraft.world.scores.ScoreHolder;
import net.minecraft.world.scores.Scoreboard;

/**
 * Suite du camp de guerre : bâtiments (construction, production), alliés invités (neutres pour les troupes),
 * exploration (découverte des camps d'autres joueurs) et raids contre ces camps.
 * Marques : rm_hote_<invité> sur le chef, rm_invite_<chef> sur l'invité, rm_vu_<chef> sur qui a découvert un camp,
 * rm_cible_<chef> pendant un raid contre un joueur.
 */
public final class CampsPlus {
    /** Invité -> chef du camp qu'il consulte. */
    static final Map<UUID, UUID> VISITE = new HashMap<>();
    public static final int DUREE_EXPLORATION = 180;
    public static final int DUREE_RAID_JOUEUR = 240;
    private static final double[] BONUS_TOUR = {0, 0.15, 0.35, 0.6};
    private static final Random R = new Random();

    private CampsPlus() {}

    private static int get(Scoreboard sb, ScoreHolder h, String n) {
        return Camps.get(sb, h, n);
    }

    private static void set(Scoreboard sb, ScoreHolder h, String n, int v) {
        Camps.set(sb, h, n, v);
    }

    static String alliance(Scoreboard sb, ScoreHolder h) {
        int f = get(sb, h, "rm_faction");
        return f > 0 && f < ContenuGenere.ALLIANCES.length ? ContenuGenere.ALLIANCES[f] : "ordre";
    }

    // ------------------------------------------------------------------ bâtiments

    static void ameliorerBatiment(ServerPlayer p, int b) {
        Scoreboard sb = Camps.sb(p);
        if (b < 0 || b >= Batiments.IDS.length) {
            return;
        }
        BlockPos camp = Camps.pos(sb, p);
        if (get(sb, p, "rm_camp_dim") != Camps.indexDim(p.level()) || !p.blockPosition().closerThan(camp, 24)) {
            Camps.msg(p, "Reviens à ton camp pour bâtir.", ChatFormatting.RED);
            return;
        }
        int n = get(sb, p, "rm_b_" + Batiments.IDS[b]);
        if (n >= 3) {
            return;
        }
        if (get(sb, p, "rm_camp_niv") < Batiments.CAMP_REQUIS[n + 1]) {
            Camps.msg(p, "Il faut un camp de niveau " + Batiments.CAMP_REQUIS[n + 1] + ".", ChatFormatting.RED);
            return;
        }
        int c = Batiments.COUT[n + 1];
        if (get(sb, p, "rm_butin") < c) {
            Camps.msg(p, "Pas assez de butin (" + c + " requis).", ChatFormatting.RED);
            return;
        }
        set(sb, p, "rm_butin", get(sb, p, "rm_butin") - c);
        set(sb, p, "rm_b_" + Batiments.IDS[b], n + 1);
        ServerLevel l = (ServerLevel) p.level();
        Batiments.construire(l, camp, b, n + 1, alliance(sb, p));
        BlockPos centre = Batiments.centre(camp, b);
        l.sendParticles(ParticleTypes.CLOUD, centre.getX() + 0.5, centre.getY() + 3, centre.getZ() + 0.5, 80, 3, 2, 3, 0.05);
        l.playSound(null, centre, SoundEvents.ANVIL_USE, SoundSource.BLOCKS, 1.0F, 0.8F);
        Camps.msg(p, Batiments.NOMS[b] + " niveau " + (n + 1) + " : " + Batiments.effet(b, n + 1), ChatFormatting.GOLD);
        Saga.accorder(p, "batiment");
    }

    // ------------------------------------------------------------------ alliés

    static List<String> invites(ServerPlayer p) {
        List<String> l = new ArrayList<>();
        for (String t : p.entityTags()) {
            if (t.startsWith("rm_hote_")) {
                l.add(t.substring(8));
            }
        }
        l.sort(String::compareTo);
        return l;
    }

    static List<String> proches(ServerPlayer p) {
        List<String> l = new ArrayList<>();
        for (ServerPlayer o : p.level().getServer().getPlayerList().getPlayers()) {
            if (o != p && o.level() == p.level() && o.distanceTo(p) < 24 && !p.entityTags().contains("rm_hote_" + o.getScoreboardName())) {
                l.add(o.getScoreboardName());
            }
        }
        l.sort(String::compareTo);
        return l;
    }

    static void inviter(ServerPlayer p, String nom) {
        ServerPlayer o = p.level().getServer().getPlayerList().getPlayerByName(nom);
        if (o == null || o == p || o.distanceTo(p) > 24) {
            return;
        }
        p.addTag("rm_hote_" + o.getScoreboardName());
        o.addTag("rm_invite_" + p.getScoreboardName());
        Camps.msg(p, o.getScoreboardName() + " est désormais l'allié de ton camp : tes troupes ne l'attaqueront pas.", ChatFormatting.GREEN);
        Camps.msg(o, p.getScoreboardName() + " t'accueille dans son camp de guerre : ses troupes te sont neutres, tu peux ouvrir son étendard.", ChatFormatting.GREEN);
    }

    static void retirer(ServerPlayer p, String nom) {
        p.removeTag("rm_hote_" + nom);
        ServerPlayer o = p.level().getServer().getPlayerList().getPlayerByName(nom);
        if (o != null) {
            o.removeTag("rm_invite_" + p.getScoreboardName());
            Camps.msg(o, p.getScoreboardName() + " t'a retiré de son camp.", ChatFormatting.GRAY);
        }
        Camps.msg(p, nom + " n'est plus allié de ton camp.", ChatFormatting.GRAY);
    }

    private static String chefDe(Combattant c) {
        for (String t : c.entityTags()) {
            if (t.startsWith("rm_nom_")) {
                return t.substring(7);
            }
        }
        return null;
    }

    /** Vrai si l'unité a ne doit pas attaquer b (son chef, un allié invité, ou une unité d'un camp ami). */
    public static boolean allies(Combattant a, LivingEntity b) {
        String chef = chefDe(a);
        if (chef == null) {
            return false;
        }
        if (b instanceof Player j) {
            String n = j.getScoreboardName();
            return n.equals(chef) || j.entityTags().contains("rm_invite_" + chef) || j.entityTags().contains("rm_hote_" + chef);
        }
        if (b instanceof Combattant c) {
            String autre = chefDe(c);
            if (autre == null) {
                return false;
            }
            if (autre.equals(chef)) {
                return true;
            }
            MinecraftServer s = a.level().getServer();
            if (s == null) {
                return false;
            }
            ServerPlayer pa = s.getPlayerList().getPlayerByName(chef);
            ServerPlayer pb = s.getPlayerList().getPlayerByName(autre);
            return (pa != null && (pa.entityTags().contains("rm_hote_" + autre) || pa.entityTags().contains("rm_invite_" + autre)))
                    || (pb != null && (pb.entityTags().contains("rm_hote_" + chef) || pb.entityTags().contains("rm_invite_" + chef)));
        }
        return false;
    }

    static boolean ouvrirInvite(ServerPlayer p, BlockPos pos) {
        Scoreboard sb = Camps.sb(p);
        for (ServerPlayer chef : p.level().getServer().getPlayerList().getPlayers()) {
            if (chef != p && p.entityTags().contains("rm_invite_" + chef.getScoreboardName()) && Camps.aUnCamp(chef)
                    && Camps.pos(sb, chef).equals(pos) && get(sb, chef, "rm_camp_dim") == Camps.indexDim(p.level())) {
                VISITE.put(p.getUUID(), chef.getUUID());
                Camps.envoyer(p, chef, chef.getUUID(), chef.getScoreboardName(), false, true);
                return true;
            }
        }
        return false;
    }

    /** Un invité ne peut que déposer du butin dans le camp de son hôte. */
    static void actionInvite(ServerPlayer p, int action) {
        ServerPlayer chef = p.level().getServer().getPlayerList().getPlayer(VISITE.get(p.getUUID()));
        if (chef == null) {
            VISITE.remove(p.getUUID());
            return;
        }
        if (action == 3) {
            Inventory inv = p.getInventory();
            int total = 0;
            for (int i = 0; i < inv.getContainerSize(); i++) {
                ItemStack s = inv.getItem(i);
                int v = Stockage.valeur(s);
                if (v > 0 && !s.isEmpty()) {
                    total += v * s.getCount();
                    inv.setItem(i, ItemStack.EMPTY);
                }
            }
            if (total > 0) {
                Scoreboard sb = Camps.sb(p);
                set(sb, chef, "rm_butin", get(sb, chef, "rm_butin") + total);
                Camps.msg(p, "+" + total + " butin offert au camp de " + chef.getScoreboardName() + ".", ChatFormatting.GOLD);
                Camps.msg(chef, p.getScoreboardName() + " a offert " + total + " butin à ton camp.", ChatFormatting.GOLD);
            }
        }
        Camps.envoyer(p, chef, chef.getUUID(), chef.getScoreboardName(), false, false);
    }

    // ------------------------------------------------------------------ défense et exploration

    static int forceAuCamp(MinecraftServer s, Scoreboard sb, ScoreHolder chef, UUID id) {
        ServerLevel l = Camps.niveauCamp(s, get(sb, chef, "rm_camp_dim"));
        if (l == null || get(sb, chef, "rm_camp_niv") <= 0) {
            return 0;
        }
        BlockPos camp = Camps.pos(sb, chef);
        if (!l.isLoaded(camp)) {
            return get(sb, chef, "rm_camp_def");
        }
        String tag = "rm_chef_" + id;
        int f = 0;
        for (Combattant c : l.getEntitiesOfClass(Combattant.class, new net.minecraft.world.phys.AABB(camp).inflate(32),
                c -> c.isAlive() && c.entityTags().contains(tag))) {
            f += Camps.puissance(BuiltInRegistries.ENTITY_TYPE.getKey(c.getType()).getPath()) / 10;
        }
        return f;
    }

    /** Défense estimée d'un camp (troupes + tour de guet). */
    static int defense(Scoreboard sb, ScoreHolder h) {
        int base = Math.max(get(sb, h, "rm_camp_def"), get(sb, h, "rm_camp_nb") * 6) + 5 * get(sb, h, "rm_camp_niv");
        return (int) (base * (1 + BONUS_TOUR[Math.min(3, get(sb, h, "rm_b_tour"))]));
    }

    static void explorer(ServerPlayer p, int n) {
        Scoreboard sb = Camps.sb(p);
        if (get(sb, p, "rm_expl_fin") > 0) {
            return;
        }
        int[] t = Camps.partir(p, "rm_expl_u", Math.max(1, Math.min(5, n)));
        if (t[0] == 0) {
            Camps.msg(p, "Aucune troupe au camp pour partir en exploration.", ChatFormatting.RED);
            return;
        }
        set(sb, p, "rm_expl_fin", Camps.maintenant(p.level().getServer()) + DUREE_EXPLORATION);
        Camps.msg(p, "🧭 " + t[0] + " éclaireur(s) partent explorer les Royaumes. Retour dans " + DUREE_EXPLORATION / 60 + " min.", ChatFormatting.AQUA);
    }

    private static void finirExploration(ServerPlayer p) {
        Scoreboard sb = Camps.sb(p);
        int[] r = Camps.revenir(p, "rm_expl_u", 0.1);
        set(sb, p, "rm_expl_fin", 0);
        int n = Math.max(1, r[0]);
        Camps.donner(p, new ItemStack(ModObjets.PIERRE_BRUTE.get(), n + R.nextInt(n + 1)));
        if (R.nextDouble() < 0.4) {
            Camps.donner(p, new ItemStack(R.nextBoolean() ? Items.EMERALD : Items.DIAMOND, 1 + R.nextInt(2)));
        }
        double chance = Math.min(0.9, 0.25 + 0.1 * n + 0.15 * get(sb, p, "rm_b_tour"));
        List<String> trouves = new ArrayList<>();
        Objective o = sb.getObjective("rm_camp_niv");
        if (o != null) {
            for (PlayerScoreEntry e : sb.listPlayerScores(o)) {
                String nom = e.owner();
                if (e.value() > 0 && !nom.equals(p.getScoreboardName()) && !nom.startsWith("#") && !estAllie(p, nom)
                        && !p.entityTags().contains("rm_vu_" + nom) && R.nextDouble() < chance) {
                    p.addTag("rm_vu_" + nom);
                    trouves.add(nom);
                }
            }
        }
        String rapport = "🧭 Retour d'exploration : " + r[1] + "/" + r[0] + " éclaireurs rentrent.";
        Camps.msg(p, rapport + (trouves.isEmpty() ? " Aucun camp ennemi repéré." : " Camps repérés : " + String.join(", ", trouves) + " !"),
                trouves.isEmpty() ? ChatFormatting.AQUA : ChatFormatting.GOLD);
        if (!trouves.isEmpty()) {
            Saga.accorder(p, "exploration");
        }
    }

    private static boolean estAllie(ServerPlayer p, String nom) {
        return p.entityTags().contains("rm_hote_" + nom) || p.entityTags().contains("rm_invite_" + nom);
    }

    static List<String> cibles(ServerPlayer p) {
        Scoreboard sb = Camps.sb(p);
        List<String> l = new ArrayList<>();
        for (String t : p.entityTags()) {
            if (t.startsWith("rm_vu_")) {
                String nom = t.substring(6);
                if (!estAllie(p, nom) && get(sb, ScoreHolder.forNameOnly(nom), "rm_camp_niv") > 0) {
                    l.add(nom);
                }
            }
        }
        l.sort(String::compareTo);
        return l.size() > 5 ? l.subList(0, 5) : l;
    }

    static String cibleEnCours(ServerPlayer p) {
        for (String t : p.entityTags()) {
            if (t.startsWith("rm_cible_")) {
                return t.substring(9);
            }
        }
        return "";
    }

    // ------------------------------------------------------------------ raids contre les joueurs

    static void raidJoueur(ServerPlayer p, String nom) {
        Scoreboard sb = Camps.sb(p);
        if (get(sb, p, "rm_raid_fin") > 0 || !cibles(p).contains(nom)) {
            return;
        }
        int[] t = Camps.partir(p, "rm_raid_u", 99);
        if (t[0] == 0) {
            Camps.msg(p, "Aucune troupe au camp pour ce raid.", ChatFormatting.RED);
            return;
        }
        set(sb, p, "rm_raid_type", 3);
        set(sb, p, "rm_raid_force", t[1]);
        set(sb, p, "rm_raid_fin", Camps.maintenant(p.level().getServer()) + DUREE_RAID_JOUEUR);
        p.addTag("rm_cible_" + nom);
        Camps.msg(p, "⚔ " + t[0] + " guerriers marchent sur le camp de " + nom + " (force " + t[1] + " contre ~"
                + defense(sb, ScoreHolder.forNameOnly(nom)) + "). Retour dans " + DUREE_RAID_JOUEUR / 60 + " min.", ChatFormatting.GOLD);
        ServerPlayer cible = p.level().getServer().getPlayerList().getPlayerByName(nom);
        if (cible != null) {
            Camps.msg(cible, "⚠ Tes éclaireurs signalent une armée en marche vers ton camp…", ChatFormatting.DARK_RED);
        }
    }

    static void finirRaidJoueur(ServerPlayer p) {
        Scoreboard sb = Camps.sb(p);
        String nom = cibleEnCours(p);
        p.removeTag("rm_cible_" + nom);
        set(sb, p, "rm_raid_fin", 0);
        set(sb, p, "rm_raid_type", 0);
        ScoreHolder h = ScoreHolder.forNameOnly(nom);
        int force = get(sb, p, "rm_raid_force");
        int def = Math.max(1, defense(sb, h));
        boolean victoire = !nom.isEmpty() && R.nextDouble() < force / (double) (force + def);
        int[] r = Camps.revenir(p, "rm_raid_u", victoire ? 0.35 * def / (force + def) : 0.6);
        int vol = 0;
        if (victoire) {
            vol = Math.min(300, get(sb, h, "rm_butin") / 4);
            set(sb, h, "rm_butin", get(sb, h, "rm_butin") - vol);
            set(sb, p, "rm_butin", get(sb, p, "rm_butin") + vol);
            set(sb, h, "rm_camp_def", get(sb, h, "rm_camp_def") * 7 / 10);
            set(sb, h, "rm_pille", get(sb, h, "rm_pille") + vol);
            set(sb, p, "rm_gloire", get(sb, p, "rm_gloire") + def / 2);
            Camps.donner(p, new ItemStack(ModObjets.PIERRE_BRUTE.get(), 2 + R.nextInt(4)));
            Saga.accorder(p, "raid_joueur");
            p.removeTag("rm_vu_" + nom);
        }
        Camps.msg(p, (victoire ? "✦ Le camp de " + nom + " est pillé ! " : "✖ L'assaut sur le camp de " + nom + " a échoué. ")
                + r[1] + "/" + r[0] + " guerriers rentrent" + (victoire ? ", +" + vol + " butin." : "."), victoire ? ChatFormatting.GOLD : ChatFormatting.RED);
        ServerPlayer cible = p.level().getServer().getPlayerList().getPlayerByName(nom);
        if (cible != null) {
            Camps.msg(cible, victoire ? "⚠ " + p.getScoreboardName() + " a pillé ton camp : -" + vol + " butin !"
                    : "✦ Ton camp a repoussé l'assaut de " + p.getScoreboardName() + " !", victoire ? ChatFormatting.DARK_RED : ChatFormatting.GOLD);
            set(sb, h, "rm_pille", 0);
        }
    }

    // ------------------------------------------------------------------ chaque seconde

    static void tick(ServerPlayer p, int t) {
        Scoreboard sb = Camps.sb(p);
        int efin = get(sb, p, "rm_expl_fin");
        if (efin > 0 && t >= efin) {
            finirExploration(p);
        }
        int pille = get(sb, p, "rm_pille");
        if (pille > 0) {
            Camps.msg(p, "⚠ Pendant ton absence, ton camp a été pillé : -" + pille + " butin. Renforce ta tour de guet et tes troupes !", ChatFormatting.DARK_RED);
            set(sb, p, "rm_pille", 0);
        }
        if (t % 60 != 0) {
            return;
        }
        MinecraftServer s = p.level().getServer();
        ServerLevel l = Camps.niveauCamp(s, get(sb, p, "rm_camp_dim"));
        if (l == null) {
            return;
        }
        BlockPos camp = Camps.pos(sb, p);
        if (l.isLoaded(camp)) {
            set(sb, p, "rm_camp_def", forceAuCamp(s, sb, p, p.getUUID()));
        }
        String al = alliance(sb, p);
        int minute = t / 60;
        for (int b = 0; b < 3; b++) {
            int n = get(sb, p, "rm_b_" + Batiments.IDS[b]);
            if (n > 0) {
                Batiments.livrer(l, Batiments.coffre(camp, b, n, al), Batiments.production(b, n, minute, get(sb, p, "rm_faction")));
            }
        }
    }
}
