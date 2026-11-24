package fr.royaumes.rpg;

import fr.royaumes.RoyaumesMortels;
import fr.royaumes.entite.Combattant;
import java.util.HashMap;
import java.util.Map;
import java.util.UUID;
import net.minecraft.ChatFormatting;
import net.minecraft.core.Holder;
import net.minecraft.core.particles.ParticleTypes;
import net.minecraft.network.chat.Component;
import net.minecraft.resources.Identifier;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.tags.DamageTypeTags;
import net.minecraft.world.effect.MobEffectInstance;
import net.minecraft.world.effect.MobEffects;
import net.minecraft.world.entity.LivingEntity;
import net.minecraft.world.entity.ai.attributes.Attribute;
import net.minecraft.world.entity.ai.attributes.AttributeInstance;
import net.minecraft.world.entity.ai.attributes.AttributeModifier;
import net.minecraft.world.entity.ai.attributes.Attributes;
import net.minecraft.world.item.Items;
import net.minecraft.world.phys.Vec3;
import net.neoforged.neoforge.event.entity.living.LivingIncomingDamageEvent;

/**
 * Voies du héros : Guerrier, Mage ou Éclaireur (dès le niveau 5), puis un talent à choisir parmi deux aux niveaux 10, 20,
 * 30 et 40. Tout est passif : attributs, effets et réactions aux coups. État : rm_voie (1-3) et rm_talents (un chiffre en
 * base 3 par palier : 0 rien, 1 premier talent, 2 second).
 */
public final class Voies {
    private Voies() {}

    public static final String[] NOMS = {"", "Guerrier", "Mage", "Éclaireur"};
    public static final String[] DESCRIPTIONS = {"",
        "Au cœur de la mêlée. +4 PV, +1 dégât au corps à corps. Ses talents : armure, rage, endurance, exécution.",
        "Maître des Vents de magie. +30 énergie, +1 énergie par seconde. Ses talents : réserve, sorts moins chers, archimagie.",
        "Rapide et insaisissable. +10 % de vitesse. Ses talents : arc, chute féline, coups dans le dos, esquive."};
    public static final int[] NIVEAUX = {10, 20, 30, 40};
    public static final int NIVEAU_VOIE = 5;
    /** [voie][palier][choix] = {nom, description}. */
    public static final String[][][][] TALENTS = {
        {},
        { // Guerrier
            {{"Peau de fer", "+2 points d'armure en permanence."}, {"Brute", "+1,5 dégât au corps à corps."}},
            {{"Second souffle", "Sous 30 % de vie : Régénération II pendant 5 s (toutes les 30 s)."}, {"Rage", "Sous 50 % de vie : Force I."}},
            {{"Inébranlable", "Résiste au recul (+30 %) et +2 de robustesse."}, {"Vampirisme", "Chaque coup au corps à corps rend 1 PV."}},
            {{"Champion des Dieux", "+6 PV supplémentaires."}, {"Exécuteur", "+50 % de dégâts contre une cible sous 30 % de vie."}},
        },
        { // Mage
            {{"Réserve", "+40 énergie arcanique maximum."}, {"Flux", "Régénération d'énergie +50 %."}},
            {{"Bouclier arcanique", "Quand tu es touché : Absorption II pendant 10 s (toutes les 45 s)."}, {"Concentration", "Sorts 20 % moins chers."}},
            {{"Maître du Vent", "Les sorts du Vent de ta faction coûtent moitié moins."}, {"Vents mêlés", "Capacité de faction rechargée 30 % plus vite."}},
            {{"Archimage", "+80 énergie maximum et régénération doublée."}, {"Clairvoyance", "Vision nocturne ; les ennemis proches sont révélés."}},
        },
        { // Éclaireur
            {{"Pied léger", "+15 % de vitesse supplémentaire."}, {"Archer", "+30 % de dégâts avec les projectiles."}},
            {{"Chute féline", "Aucun dégât de chute."}, {"Ombre", "Invisible tant que tu te tiens accroupi."}},
            {{"Coup bas", "+60 % de dégâts en frappant une cible de dos."}, {"Pillard", "Chance II en permanence (meilleur butin)."}},
            {{"Fantôme", "20 % de chances d'esquiver une attaque."}, {"Œil de faucon", "Ennemis révélés à 32 blocs ; projectiles +50 %."}},
        },
    };

    private static final Map<UUID, Long> RECHARGES = new HashMap<>();

    // ------------------------------------------------------------------ état

    public static int voie(ServerPlayer p) {
        int v = Quetes.get(p, "rm_voie");
        return v >= 1 && v <= 3 ? v : 0;
    }

    /** Choix au palier (0 rien, 1 ou 2). */
    public static int choix(int talents, int palier) {
        for (int i = 0; i < palier; i++) {
            talents /= 3;
        }
        return talents % 3;
    }

    static boolean a(ServerPlayer p, int voie, int palier, int c) {
        return voie(p) == voie && choix(Quetes.get(p, "rm_talents"), palier) == c;
    }

    // ------------------------------------------------------------------ actions (depuis l'écran, touche K)

    public static void action(ServerPlayer p, int action, int arg) {
        int niveau = Quetes.get(p, "rm_niveau");
        if (action == 30) {
            if (voie(p) != 0 || arg < 1 || arg > 3) {
                return;
            }
            if (niveau < NIVEAU_VOIE && !p.isCreative()) {
                p.sendSystemMessage(Component.literal("Il faut être de niveau " + NIVEAU_VOIE + " pour choisir ta voie.").withStyle(ChatFormatting.RED));
                return;
            }
            Quetes.set(p, "rm_voie", arg);
            Quetes.set(p, "rm_talents", 0);
            p.sendSystemMessage(Component.literal("✦ Tu suis désormais la voie du " + NOMS[arg] + ".").withStyle(ChatFormatting.GOLD));
            fr.royaumes.bloc.BlocPortail.executer(p, "playsound minecraft:ui.toast.challenge_complete master @s ~ ~ ~ 0.6 1.4");
        } else if (action == 31) {
            int palier = arg / 2;
            int c = arg % 2 + 1;
            int t = Quetes.get(p, "rm_talents");
            if (voie(p) == 0 || palier < 0 || palier >= NIVEAUX.length || choix(t, palier) != 0) {
                return;
            }
            if (niveau < NIVEAUX[palier] && !p.isCreative()) {
                p.sendSystemMessage(Component.literal("Ce talent s'apprend au niveau " + NIVEAUX[palier] + ".").withStyle(ChatFormatting.RED));
                return;
            }
            int puissance = 1;
            for (int i = 0; i < palier; i++) {
                puissance *= 3;
            }
            Quetes.set(p, "rm_talents", t + c * puissance);
            p.sendSystemMessage(Component.literal("✦ Talent appris : " + TALENTS[voie(p)][palier][c - 1][0]).withStyle(ChatFormatting.GOLD));
        } else if (action == 32) {
            if (voie(p) == 0) {
                return;
            }
            if (!p.isCreative()) {
                if (fr.royaumes.arsenal.Arsenal.compter(p.getInventory(), Items.DIAMOND) < 3) {
                    p.sendSystemMessage(Component.literal("Oublier ta voie coûte 3 diamants.").withStyle(ChatFormatting.RED));
                    return;
                }
                fr.royaumes.arsenal.Arsenal.retirer(p.getInventory(), Items.DIAMOND, 3);
            }
            Quetes.set(p, "rm_voie", 0);
            Quetes.set(p, "rm_talents", 0);
            passif(p);
            p.sendSystemMessage(Quetes.avecTouches("Tu as oublié ta voie : choisis-en une nouvelle (touche [voie]).").withStyle(ChatFormatting.YELLOW));
        }
        fr.royaumes.reseau.Reseau.envoyerFiche(p);
    }

    // ------------------------------------------------------------------ passifs (chaque seconde)

    static void modificateur(ServerPlayer p, Holder<Attribute> attr, String nom, double valeur) {
        AttributeInstance i = p.getAttribute(attr);
        if (i == null) {
            return;
        }
        Identifier id = Identifier.fromNamespaceAndPath(RoyaumesMortels.MODID, "voie_" + nom);
        if (valeur == 0) {
            i.removeModifier(id);
        } else {
            i.addOrUpdateTransientModifier(new AttributeModifier(id, valeur, AttributeModifier.Operation.ADD_VALUE));
        }
    }

    static void effet(ServerPlayer p, Holder<net.minecraft.world.effect.MobEffect> e, int duree, int niveau) {
        p.addEffect(new MobEffectInstance(e, duree, niveau, true, false, true));
    }

    public static void passif(ServerPlayer p) {
        int v = voie(p);
        double pv = 0;
        double degats = 0;
        double armure = 0;
        double robustesse = 0;
        double recul = 0;
        double vitesse = 0;
        if (v == 1) {
            pv = 4 + (a(p, 1, 3, 1) ? 6 : 0);
            degats = 1 + (a(p, 1, 0, 2) ? 1.5 : 0);
            armure = a(p, 1, 0, 1) ? 2 : 0;
            if (a(p, 1, 2, 1)) {
                recul = 0.3;
                robustesse = 2;
            }
        } else if (v == 3) {
            vitesse = 0.01 + (a(p, 3, 0, 1) ? 0.015 : 0);
        }
        modificateur(p, Attributes.MAX_HEALTH, "pv", pv);
        modificateur(p, Attributes.ATTACK_DAMAGE, "degats", degats);
        modificateur(p, Attributes.ARMOR, "armure", armure);
        modificateur(p, Attributes.ARMOR_TOUGHNESS, "robustesse", robustesse);
        modificateur(p, Attributes.KNOCKBACK_RESISTANCE, "recul", recul);
        modificateur(p, Attributes.MOVEMENT_SPEED, "vitesse", vitesse);
        if (v == 0) {
            return;
        }
        float vie = p.getHealth() / Math.max(1.0F, p.getMaxHealth());
        long t = p.level().getGameTime();
        if (a(p, 1, 1, 1) && vie < 0.3F && t >= RECHARGES.getOrDefault(p.getUUID(), 0L)) {
            effet(p, MobEffects.REGENERATION, 100, 1);
            RECHARGES.put(p.getUUID(), t + 600);
            p.sendOverlayMessage(Component.literal("Second souffle !").withStyle(ChatFormatting.GREEN));
        }
        if (a(p, 1, 1, 2) && vie < 0.5F) {
            effet(p, MobEffects.STRENGTH, 40, 0);
        }
        if (a(p, 2, 3, 2)) {
            effet(p, MobEffects.NIGHT_VISION, 300, 0);
            reveler(p, 16);
        }
        if (a(p, 3, 1, 2) && p.isShiftKeyDown()) {
            effet(p, MobEffects.INVISIBILITY, 30, 0);
        }
        if (a(p, 3, 2, 2)) {
            effet(p, MobEffects.LUCK, 60, 1);
        }
        if (a(p, 3, 3, 2)) {
            reveler(p, 32);
        }
    }

    static void reveler(ServerPlayer p, double rayon) {
        int alliance = Quetes.allianceJoueur(p);
        String equipe = alliance >= 0 ? "rm_" + Quetes.ALLIANCES[alliance] : "";
        for (Combattant c : p.level().getEntitiesOfClass(Combattant.class, p.getBoundingBox().inflate(rayon),
                c -> !c.profil().equipe().equals(equipe) && !c.entityTags().contains(fr.royaumes.camp.Camps.UNITE))) {
            c.addEffect(new MobEffectInstance(MobEffects.GLOWING, 30, 0, true, false));
        }
    }

    // ------------------------------------------------------------------ magie

    public static int bonusEnergie(ServerPlayer p) {
        if (voie(p) != 2) {
            return 0;
        }
        return 30 + (a(p, 2, 0, 1) ? 40 : 0) + (a(p, 2, 3, 1) ? 80 : 0);
    }

    public static int regeneration(ServerPlayer p, int gain) {
        if (voie(p) != 2) {
            return gain;
        }
        double g = gain + 1;
        if (a(p, 2, 0, 2)) {
            g *= 1.5;
        }
        if (a(p, 2, 3, 1)) {
            g *= 2;
        }
        return (int) Math.round(g);
    }

    public static int cout(ServerPlayer p, int vent, int c) {
        if (voie(p) != 2) {
            return c;
        }
        double r = c;
        if (a(p, 2, 1, 2)) {
            r *= 0.8;
        }
        int f = Quetes.get(p, "rm_faction");
        if (a(p, 2, 2, 1) && f > 0 && f < fr.royaumes.ContenuGenere.VENT_FACTION.length && fr.royaumes.ContenuGenere.VENT_FACTION[f] == vent) {
            r *= 0.5;
        }
        return Math.max(1, (int) Math.round(r));
    }

    public static double recharge(ServerPlayer p) {
        return a(p, 2, 2, 2) ? 0.7 : 1.0;
    }

    // ------------------------------------------------------------------ combat

    public static void degats(LivingIncomingDamageEvent event) {
        LivingEntity cible = event.getEntity();
        if (cible instanceof ServerPlayer p && voie(p) != 0) {
            if (a(p, 3, 1, 1) && event.getSource().is(DamageTypeTags.IS_FALL)) {
                event.setCanceled(true);
                return;
            }
            if (a(p, 3, 3, 1) && event.getSource().getEntity() != null && p.getRandom().nextFloat() < 0.2F) {
                event.setCanceled(true);
                if (p.level() instanceof ServerLevel n) {
                    n.sendParticles(ParticleTypes.CLOUD, p.getX(), p.getY() + 1, p.getZ(), 8, 0.3, 0.5, 0.3, 0.02);
                }
                p.sendOverlayMessage(Component.literal("Esquive !").withStyle(ChatFormatting.AQUA));
                return;
            }
            long t = p.level().getGameTime();
            if (a(p, 2, 1, 1) && event.getSource().getEntity() != null && t >= RECHARGES.getOrDefault(p.getUUID(), 0L)) {
                effet(p, MobEffects.ABSORPTION, 200, 1);
                RECHARGES.put(p.getUUID(), t + 900);
                p.sendOverlayMessage(Component.literal("Bouclier arcanique !").withStyle(ChatFormatting.LIGHT_PURPLE));
            }
        }
        if (event.getSource().getEntity() instanceof ServerPlayer p && voie(p) != 0 && cible != p) {
            boolean projectile = event.getSource().is(DamageTypeTags.IS_PROJECTILE);
            boolean melee = event.getSource().getDirectEntity() == p;
            float m = 1.0F;
            if (projectile && a(p, 3, 0, 2)) {
                m *= 1.3F;
            }
            if (projectile && a(p, 3, 3, 2)) {
                m *= 1.5F;
            }
            if (melee && a(p, 1, 3, 2) && cible.getHealth() < cible.getMaxHealth() * 0.3F) {
                m *= 1.5F;
            }
            if (melee && a(p, 3, 2, 1)) {
                Vec3 regard = cible.getLookAngle();
                Vec3 versAttaquant = p.position().subtract(cible.position()).normalize();
                if (regard.x * versAttaquant.x + regard.z * versAttaquant.z < -0.3) {
                    m *= 1.6F;
                    if (p.level() instanceof ServerLevel n) {
                        n.sendParticles(ParticleTypes.CRIT, cible.getX(), cible.getY() + 1, cible.getZ(), 10, 0.3, 0.4, 0.3, 0.2);
                    }
                }
            }
            if (melee && a(p, 1, 2, 2)) {
                p.heal(1.0F);
            }
            if (m != 1.0F) {
                event.setAmount(event.getAmount() * m);
            }
        }
    }
}
