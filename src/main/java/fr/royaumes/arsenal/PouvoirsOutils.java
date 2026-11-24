package fr.royaumes.arsenal;

import java.util.ArrayDeque;
import java.util.HashSet;
import java.util.Set;
import net.minecraft.core.BlockPos;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.tags.BlockTags;
import net.minecraft.world.InteractionHand;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.level.block.state.BlockState;
import net.minecraft.world.phys.Vec3;

/**
 * Pouvoirs des outils d'alliance aux hauts paliers (pour les héros de l'alliance, désactivés en restant accroupi) :
 * pioche et pelle creusent une ligne dans la direction du regard (Légende 2, Mythique 3, Divin 5 blocs) ;
 * la hache abat l'arbre entier (Mythique 24 bûches, Divin 96). Chaque bloc en plus use l'outil d'un point.
 */
public final class PouvoirsOutils {
    private static boolean enCours = false;

    private PouvoirsOutils() {}

    public static int ligne(int palier) {
        return palier >= 4 ? 5 : palier == 3 ? 3 : palier == 2 ? 2 : 1;
    }

    public static int arbre(int palier) {
        return palier >= 4 ? 96 : palier == 3 ? 24 : 0;
    }

    /** Appelé par OutilAlliance.mineBlock, après qu'un bloc a été miné avec l'outil. */
    public static void casser(ServerPlayer p, ItemStack outil, BlockPos pos, BlockState etat) {
        if (enCours || p.isShiftKeyDown() || !(p.level() instanceof ServerLevel n)) {
            return;
        }
        int[] i = Arsenal.infosOutil(outil.getItem());
        if (i == null || i[0] != Arsenal.alliance(Arsenal.scoreFaction(p))) {
            return;
        }
        enCours = true;
        try {
            if ((i[1] == 0 || i[1] == 1) && ligne(i[2]) > 1) {
                creuser(n, p, outil, pos, ligne(i[2]));
            } else if (i[1] == 2 && arbre(i[2]) > 0 && etat.is(BlockTags.LOGS)) {
                abattre(n, p, outil, pos, arbre(i[2]));
            }
        } finally {
            enCours = false;
        }
    }

    static boolean casserUn(ServerLevel n, ServerPlayer p, ItemStack outil, BlockPos q) {
        if (outil.isEmpty()) {
            return false;
        }
        BlockState s = n.getBlockState(q);
        if (s.isAir() || s.getDestroySpeed(n, q) < 0 || !outil.isCorrectToolForDrops(s) || outil.getDestroySpeed(s) <= 1.0F) {
            return false;
        }
        n.destroyBlock(q, true, p);
        outil.hurtAndBreak(1, p, InteractionHand.MAIN_HAND);
        return true;
    }

    static void creuser(ServerLevel n, ServerPlayer p, ItemStack outil, BlockPos depart, int longueur) {
        Vec3 v = p.getLookAngle();
        int dx = 0;
        int dy = 0;
        int dz = 0;
        if (Math.abs(v.y) > Math.abs(v.x) && Math.abs(v.y) > Math.abs(v.z)) {
            dy = v.y > 0 ? 1 : -1;
        } else if (Math.abs(v.x) > Math.abs(v.z)) {
            dx = v.x > 0 ? 1 : -1;
        } else {
            dz = v.z > 0 ? 1 : -1;
        }
        for (int k = 1; k < longueur; k++) {
            if (!casserUn(n, p, outil, depart.offset(dx * k, dy * k, dz * k))) {
                return;
            }
        }
    }

    static void abattre(ServerLevel n, ServerPlayer p, ItemStack outil, BlockPos depart, int max) {
        Set<BlockPos> vus = new HashSet<>();
        ArrayDeque<BlockPos> file = new ArrayDeque<>();
        file.add(depart);
        vus.add(depart);
        int faits = 0;
        while (!file.isEmpty() && faits < max) {
            BlockPos c = file.poll();
            for (int x = -1; x <= 1; x++) {
                for (int y = 0; y <= 1; y++) {
                    for (int z = -1; z <= 1; z++) {
                        BlockPos q = c.offset(x, y, z);
                        if (vus.add(q) && n.getBlockState(q).is(BlockTags.LOGS)) {
                            if (!casserUn(n, p, outil, q)) {
                                return;
                            }
                            faits++;
                            file.add(q);
                        }
                    }
                }
            }
        }
    }
}
