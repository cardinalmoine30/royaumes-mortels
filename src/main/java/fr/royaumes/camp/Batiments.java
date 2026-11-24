package fr.royaumes.camp;

import com.google.gson.JsonArray;
import com.google.gson.JsonElement;
import com.google.gson.JsonObject;
import com.google.gson.JsonParser;
import fr.royaumes.ModObjets;
import fr.royaumes.RoyaumesMortels;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.nio.charset.StandardCharsets;
import java.util.ArrayList;
import java.util.List;
import java.util.Random;
import net.minecraft.core.BlockPos;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.resources.Identifier;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.world.Container;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.Items;
import net.minecraft.world.level.block.Block;
import net.minecraft.world.level.block.Blocks;
import net.minecraft.world.level.block.entity.BlockEntity;
import net.minecraft.world.level.block.state.BlockState;

/**
 * Bâtiments du camp : forge, ferme, sanctuaire, caserne, tour de guet ; 3 niveaux chacun. Les plans
 * (royaumes_camp/batiments.json, outils/objets/batiments.py) existent en 4 styles, un par Grande Alliance :
 * même fonction, architecture différente. Chaque bâtiment est construit pour de vrai autour de l'étendard,
 * porte tournée vers lui, et produit dans son coffre (forge, ferme, sanctuaire).
 */
public final class Batiments {
    public static final String[] IDS = {"forge", "ferme", "sanctuaire", "caserne", "tour"};
    public static final String[] NOMS = {"Forge", "Ferme", "Sanctuaire", "Caserne", "Tour de guet"};
    /** Emplacement autour de l'étendard et rotation (porte vers l'étendard). */
    private static final int[][] SLOTS = {{11, 0, 3}, {-11, 0, 1}, {0, 11, 0}, {0, -11, 2}, {10, 10, 0}};
    public static final int[] COUT = {0, 40, 120, 300};
    public static final int[] CAMP_REQUIS = {0, 1, 2, 4};
    public static final String[] STYLES = {"ordre", "chaos", "mort", "destruction"};
    private static JsonObject plans;
    private static final Random R = new Random();

    private Batiments() {}

    public static int index(String id) {
        for (int i = 0; i < IDS.length; i++) {
            if (IDS[i].equals(id)) {
                return i;
            }
        }
        return -1;
    }

    private static JsonObject plans() {
        if (plans == null) {
            try (InputStream in = Batiments.class.getResourceAsStream("/royaumes_camp/batiments.json")) {
                plans = in == null ? new JsonObject() : JsonParser.parseReader(new InputStreamReader(in, StandardCharsets.UTF_8)).getAsJsonObject();
            } catch (Exception e) {
                RoyaumesMortels.LOGGER.warn("[Royaumes Mortels] Plans des bâtiments illisibles : {}", e.toString());
                plans = new JsonObject();
            }
        }
        return plans;
    }

    static int style(String alliance) {
        for (int i = 0; i < STYLES.length; i++) {
            if (STYLES[i].equals(alliance)) {
                return i;
            }
        }
        return 0;
    }

    private static BlockPos tourner(int x, int y, int z, int k) {
        for (int i = 0; i < k; i++) {
            int t = x;
            x = -z;
            z = t;
        }
        return new BlockPos(x, y, z);
    }

    public static BlockPos centre(BlockPos etendard, int b) {
        return etendard.offset(SLOTS[b][0], 0, SLOTS[b][1]);
    }

    /** Pose le bâtiment b au niveau n, dans le style de l'alliance ; renvoie la position du coffre (ou null). */
    public static BlockPos construire(ServerLevel l, BlockPos etendard, int b, int n, String alliance) {
        JsonObject parBat = plans().getAsJsonObject(IDS[b]);
        if (parBat == null) {
            return null;
        }
        JsonArray niveaux = parBat.getAsJsonArray(STYLES[style(alliance)]);
        if (niveaux == null || n < 1 || n > niveaux.size()) {
            return null;
        }
        JsonObject plan = niveaux.get(n - 1).getAsJsonObject();
        List<BlockState> palette = new ArrayList<>();
        for (JsonElement e : plan.getAsJsonArray("p")) {
            Block bl = BuiltInRegistries.BLOCK.getValue(Identifier.parse(e.getAsString()));
            palette.add(bl == null ? Blocks.STONE.defaultBlockState() : bl.defaultBlockState());
        }
        BlockPos c = centre(etendard, b);
        int k = SLOTS[b][2];
        // déblaie l'emplacement, puis consolide le sol
        for (int x = -5; x <= 5; x++) {
            for (int z = -5; z <= 5; z++) {
                for (int y = 0; y <= 20; y++) {
                    BlockPos p = c.offset(x, y, z);
                    if (!l.getBlockState(p).isAir()) {
                        l.setBlock(p, Blocks.AIR.defaultBlockState(), 2);
                    }
                }
                for (int y = -1; y >= -4; y--) {
                    BlockPos p = c.offset(x, y, z);
                    if (l.getBlockState(p).isAir() || !l.getFluidState(p).isEmpty()) {
                        l.setBlock(p, Blocks.COBBLESTONE.defaultBlockState(), 2);
                    }
                }
            }
        }
        BlockPos coffre = null;
        for (JsonElement e : plan.getAsJsonArray("b")) {
            JsonArray a = e.getAsJsonArray();
            BlockPos p = c.offset(tourner(a.get(0).getAsInt(), a.get(1).getAsInt(), a.get(2).getAsInt(), k));
            BlockState s = palette.get(a.get(3).getAsInt());
            l.setBlock(p, s, 3);
            if (s.is(Blocks.CHEST)) {
                coffre = p;
            }
        }
        return coffre;
    }

    // ------------------------------------------------------------------ production (par minute)

    /** Production d'une minute du bâtiment b au niveau n (forge, ferme, sanctuaire). Le sanctuaire capte le Vent de la faction. */
    public static List<ItemStack> production(int b, int n, int minute, int faction) {
        List<ItemStack> l = new ArrayList<>();
        switch (b) {
            case 0 -> { // forge
                l.add(new ItemStack(Items.IRON_INGOT, n == 1 ? 2 : n == 2 ? 3 : 5));
                l.add(new ItemStack(Items.COAL, n == 1 ? 2 : n == 2 ? 3 : 4));
                if (n >= 2) {
                    l.add(new ItemStack(Items.GOLD_INGOT, n == 2 ? 1 : 2));
                }
                if (n >= 3) {
                    l.add(new ItemStack(ModObjets.PIERRE_BRUTE.get(), 1));
                }
            }
            case 1 -> { // ferme
                l.add(new ItemStack(Items.BREAD, n + 1));
                if (n == 1) {
                    l.add(new ItemStack(Items.WHEAT, 2));
                }
                if (n >= 2) {
                    l.add(new ItemStack(Items.COOKED_BEEF, n));
                    l.add(new ItemStack(Items.CARROT, 2));
                }
                if (n >= 3) {
                    l.add(new ItemStack(Items.GOLDEN_CARROT, 2));
                }
            }
            case 2 -> { // sanctuaire
                int vent = faction > 0 && faction < fr.royaumes.ContenuGenere.VENT_FACTION.length ? fr.royaumes.ContenuGenere.VENT_FACTION[faction] : 0;
                Item eclat = ModObjets.ECLATS.get(vent).get();
                if (n >= 2 || minute % 3 == 0) {
                    l.add(new ItemStack(eclat, 1));
                }
                if ((n == 2 && minute % 3 == 0) || n >= 3) {
                    l.add(new ItemStack(ModObjets.CRISTAL.get(), 1));
                }
                if (n >= 3 && minute % 5 == 0) {
                    l.add(new ItemStack(ModObjets.PIERRE_BRUTE.get(), 2));
                }
            }
            default -> {
            }
        }
        return l;
    }

    /** Texte court de ce que produit / apporte le bâtiment à un niveau. */
    public static String effet(int b, int n) {
        if (n <= 0) {
            return "Pas encore construit";
        }
        return switch (b) {
            case 0 -> n == 1 ? "2 fer et 2 charbon / min" : n == 2 ? "3 fer, 3 charbon, 1 or / min" : "5 fer, 4 charbon, 2 or, 1 pierre des Royaumes / min";
            case 1 -> n == 1 ? "2 pains et 2 blé / min" : n == 2 ? "3 pains, 2 bœufs cuits, 2 carottes / min" : "4 pains, 3 bœufs cuits, 2 carottes dorées / min";
            case 2 -> n == 1 ? "1 éclat de Vent / 3 min" : n == 2 ? "1 éclat / min, 1 cristal / 3 min" : "1 éclat et 1 cristal / min, pierre des Royaumes";
            case 3 -> "+" + (2 * n) + " places de troupes, recrutement -" + (10 * n) + " %";
            case 4 -> "Défense +" + new int[] {0, 15, 35, 60}[n] + " %, exploration +" + (15 * n) + " %";
            default -> "";
        };
    }

    /** Range la production dans le coffre (si la zone est chargée) ; le surplus est perdu. */
    public static void livrer(ServerLevel l, BlockPos coffre, List<ItemStack> piles) {
        if (coffre == null || !l.isLoaded(coffre)) {
            return;
        }
        BlockEntity be = l.getBlockEntity(coffre);
        if (!(be instanceof Container c)) {
            return;
        }
        for (ItemStack s : piles) {
            for (int i = 0; i < c.getContainerSize() && !s.isEmpty(); i++) {
                ItemStack d = c.getItem(i);
                if (d.isEmpty()) {
                    c.setItem(i, s.copy());
                    s.setCount(0);
                } else if (ItemStack.isSameItemSameComponents(d, s) && d.getCount() < d.getMaxStackSize()) {
                    int n = Math.min(s.getCount(), d.getMaxStackSize() - d.getCount());
                    d.grow(n);
                    s.shrink(n);
                }
            }
        }
        c.setChanged();
    }

    /** Coffre du bâtiment : cherché dans le plan posé (position mémorisée par le scoreboard). */
    public static BlockPos coffre(BlockPos etendard, int b, int n, String alliance) {
        JsonObject parBat = plans().getAsJsonObject(IDS[b]);
        if (parBat == null || n < 1) {
            return null;
        }
        JsonObject plan = parBat.getAsJsonArray(STYLES[style(alliance)]).get(n - 1).getAsJsonObject();
        JsonArray pal = plan.getAsJsonArray("p");
        int ic = -1;
        for (int i = 0; i < pal.size(); i++) {
            if ("minecraft:chest".equals(pal.get(i).getAsString())) {
                ic = i;
            }
        }
        for (JsonElement e : plan.getAsJsonArray("b")) {
            JsonArray a = e.getAsJsonArray();
            if (a.get(3).getAsInt() == ic) {
                return centre(etendard, b).offset(tourner(a.get(0).getAsInt(), a.get(1).getAsInt(), a.get(2).getAsInt(), SLOTS[b][2]));
            }
        }
        return null;
    }
}
