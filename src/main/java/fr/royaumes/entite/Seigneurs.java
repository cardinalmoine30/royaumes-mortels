package fr.royaumes.entite;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.Iterator;
import java.util.List;
import java.util.Map;
import java.util.UUID;
import net.minecraft.core.particles.ParticleTypes;
import net.minecraft.network.chat.Component;
import net.minecraft.server.MinecraftServer;
import net.minecraft.server.level.ServerBossEvent;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.world.BossEvent;
import net.minecraft.world.effect.MobEffectInstance;
import net.minecraft.world.effect.MobEffects;
import net.minecraft.world.phys.Vec3;

/**
 * Combats de seigneurs. Invoqués à l'autel, le datapack gère déjà leur barre et leur rage (phase 2) ; le mod ajoute la
 * phase finale (désespoir sous 25 % de vie : renforts, écran assombri et frappes annoncées au sol, un cercle de flammes
 * puis l'impact, il faut bouger). Un seigneur apparu autrement (œuf, commande) reçoit ici sa barre et ses trois phases.
 */
public final class Seigneurs {
    private static final Map<UUID, ServerBossEvent> BARRES = new HashMap<>();
    private static final Map<UUID, Integer> PHASES = new HashMap<>();
    private static final Map<UUID, List<double[]>> FRAPPES = new HashMap<>();
    private static final Map<UUID, Combattant> ACTIFS = new HashMap<>();

    private Seigneurs() {}

    static void commande(Combattant c, String cmd) {
        MinecraftServer s = c.level().getServer();
        if (s != null) {
            s.getCommands().performPrefixedCommand(s.createCommandSourceStack().withEntity(c).withPosition(c.position())
                    .withSuppressedOutput(), cmd);
        }
    }

    public static int phase(Combattant c) {
        return PHASES.getOrDefault(c.getUUID(), 1);
    }

    public static void tick(Combattant c, ServerLevel n) {
        UUID id = c.getUUID();
        ACTIFS.put(id, c);
        float vie = c.getHealth() / Math.max(1.0F, c.getMaxHealth());
        boolean datapack = c.entityTags().contains("rm_boss");
        if (datapack) {
            if (phase(c) < 3 && vie <= 0.25F) {
                PHASES.put(id, 3);
                annonce(c, "déchaîne sa puissance ! Esquive les cercles !", "red", "minecraft:entity.ender_dragon.growl");
                c.invoquerRenforts(n, 4);
            }
            frappes(c, n, proches(c, n));
            return;
        }
        ServerBossEvent barre = BARRES.computeIfAbsent(id, k -> new ServerBossEvent(c.getDisplayName(),
                BossEvent.BossBarColor.PURPLE, BossEvent.BossBarOverlay.NOTCHED_10));
        barre.setProgress(Math.max(0.0F, Math.min(1.0F, vie)));
        if (c.tickCount % 10 == 0) {
            for (ServerPlayer p : n.players()) {
                boolean proche = p.distanceToSqr(c) < 48 * 48 && !p.isSpectator();
                if (proche && !barre.getPlayers().contains(p)) {
                    barre.addPlayer(p);
                } else if (!proche && barre.getPlayers().contains(p)) {
                    barre.removePlayer(p);
                }
            }
        }
        int phase = phase(c);
        if (phase == 1 && vie <= 0.6F) {
            PHASES.put(id, 2);
            barre.setColor(BossEvent.BossBarColor.YELLOW);
            c.addEffect(new MobEffectInstance(MobEffects.SPEED, 20 * 3600, 0, false, false));
            c.addEffect(new MobEffectInstance(MobEffects.STRENGTH, 20 * 3600, 0, false, false));
            n.sendParticles(ParticleTypes.ANGRY_VILLAGER, c.getX(), c.getY() + c.getBbHeight(), c.getZ(), 20, 0.8, 0.6, 0.8, 0.1);
            annonce(c, "entre en fureur !", "yellow", "minecraft:entity.ravager.roar");
            c.invoquerRenforts(n, 3);
        } else if (phase == 2 && vie <= 0.25F) {
            PHASES.put(id, 3);
            barre.setColor(BossEvent.BossBarColor.RED);
            barre.setDarkenScreen(true);
            c.addEffect(new MobEffectInstance(MobEffects.RESISTANCE, 20 * 3600, 0, false, false));
            annonce(c, "déchaîne sa puissance ! Esquive les cercles !", "red", "minecraft:entity.ender_dragon.growl");
            c.invoquerRenforts(n, 4);
        }
        frappes(c, n, new ArrayList<>(barre.getPlayers()));
    }

    static List<ServerPlayer> proches(Combattant c, ServerLevel n) {
        List<ServerPlayer> l = new ArrayList<>();
        for (ServerPlayer p : n.players()) {
            if (p.distanceToSqr(c) < 48 * 48 && !p.isSpectator()) {
                l.add(p);
            }
        }
        return l;
    }

    /** Phase finale : frappes annoncées sous chaque héros proche, toutes les 4 secondes. */
    static void frappes(Combattant c, ServerLevel n, List<ServerPlayer> heros) {
        UUID id = c.getUUID();
        if (phase(c) >= 3 && c.tickCount % 80 == 0) {
            List<double[]> l = FRAPPES.computeIfAbsent(id, k -> new ArrayList<>());
            for (ServerPlayer p : heros) {
                l.add(new double[] {p.getX(), p.getY(), p.getZ(), c.tickCount + 30});
            }
        }
        List<double[]> l = FRAPPES.get(id);
        if (l != null) {
            Iterator<double[]> it = l.iterator();
            while (it.hasNext()) {
                double[] f = it.next();
                if (c.tickCount >= f[3]) {
                    n.sendParticles(ParticleTypes.EXPLOSION, f[0], f[1] + 0.5, f[2], 3, 0.6, 0.3, 0.6, 0.0);
                    n.sendParticles(ParticleTypes.SOUL_FIRE_FLAME, f[0], f[1] + 0.2, f[2], 40, 1.2, 0.2, 1.2, 0.05);
                    for (ServerPlayer p : n.players()) {
                        if (p.distanceToSqr(f[0], f[1], f[2]) < 2.6 * 2.6) {
                            p.hurtServer(n, n.damageSources().mobAttack(c), 10.0F);
                            Vec3 d = p.position().subtract(f[0], f[1], f[2]).normalize();
                            p.push(d.x * 0.8, 0.5, d.z * 0.8);
                        }
                    }
                    it.remove();
                } else if (c.tickCount % 4 == 0) {
                    for (int a = 0; a < 16; a++) {
                        double t = a * Math.PI / 8;
                        n.sendParticles(ParticleTypes.FLAME, f[0] + Math.cos(t) * 2.4, f[1] + 0.1, f[2] + Math.sin(t) * 2.4, 1, 0, 0, 0, 0);
                    }
                }
            }
        }
    }

    static void annonce(Combattant c, String texte, String couleur, String son) {
        String nom = c.getDisplayName().getString().replace("\"", "'");
        commande(c, "title @a[distance=..48] subtitle {\"text\":\"" + texte + "\",\"color\":\"" + couleur + "\"}");
        commande(c, "title @a[distance=..48] title {\"text\":\"" + nom + "\",\"color\":\"" + couleur + "\",\"bold\":true}");
        commande(c, "playsound " + son + " hostile @a[distance=..48] ~ ~ ~ 2 0.8");
    }

    /** Héros présents au combat (pour créditer la victoire à tous). */
    public static List<ServerPlayer> heros(Combattant c) {
        ServerBossEvent b = BARRES.get(c.getUUID());
        if (b != null) {
            return new ArrayList<>(b.getPlayers());
        }
        return c.level() instanceof ServerLevel n ? proches(c, n) : List.of();
    }

    public static void fin(Combattant c) {
        UUID id = c.getUUID();
        ServerBossEvent b = BARRES.remove(id);
        if (b != null) {
            b.removeAllPlayers();
        }
        PHASES.remove(id);
        FRAPPES.remove(id);
        ACTIFS.remove(id);
    }

    /** Chaque seconde : retire les barres des seigneurs disparus (déchargés, renvoyés). */
    public static void nettoyer() {
        Iterator<Map.Entry<UUID, Combattant>> it = ACTIFS.entrySet().iterator();
        while (it.hasNext()) {
            Map.Entry<UUID, Combattant> e = it.next();
            if (e.getValue().isRemoved() || !e.getValue().isAlive()) {
                ServerBossEvent b = BARRES.remove(e.getKey());
                if (b != null) {
                    b.removeAllPlayers();
                }
                PHASES.remove(e.getKey());
                FRAPPES.remove(e.getKey());
                it.remove();
            }
        }
    }
}
