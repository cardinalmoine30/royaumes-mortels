package fr.royaumes;

import com.google.gson.JsonArray;
import com.google.gson.JsonElement;
import com.google.gson.JsonParser;
import com.mojang.serialization.JsonOps;
import fr.royaumes.bloc.BlocAutel;
import fr.royaumes.bloc.BlocEtendard;
import fr.royaumes.bloc.BlocPortail;
import fr.royaumes.objet.BatonVent;
import fr.royaumes.objet.CristalArcanique;
import fr.royaumes.objet.GrimoireVents;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.nio.charset.StandardCharsets;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import net.minecraft.core.registries.Registries;
import net.minecraft.network.chat.Component;
import net.minecraft.resources.RegistryOps;
import net.minecraft.world.item.CreativeModeTab;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.Rarity;
import net.minecraft.world.item.SpawnEggItem;
import net.minecraft.world.item.ToolMaterial;
import net.minecraft.world.level.block.Block;
import net.minecraft.world.level.block.SoundType;
import net.minecraft.world.level.block.state.BlockBehaviour;
import net.neoforged.bus.api.IEventBus;
import net.neoforged.neoforge.registries.DeferredBlock;
import net.neoforged.neoforge.registries.DeferredItem;
import net.neoforged.neoforge.registries.DeferredRegister;

/**
 * Objets, blocs et onglets créatifs du mod.
 * Les listes viennent de ContenuGenere (outils/objets/objets.py) ; les armes et objets du datapack
 * sont lus dans royaumes_creatif/*.json et ajoutés tels quels aux onglets.
 */
public final class ModObjets {
    public static final DeferredRegister.Items OBJETS = DeferredRegister.createItems(RoyaumesMortels.MODID);
    public static final DeferredRegister.Blocks BLOCS = DeferredRegister.createBlocks(RoyaumesMortels.MODID);
    public static final DeferredRegister<CreativeModeTab> ONGLETS = DeferredRegister.create(Registries.CREATIVE_MODE_TAB, RoyaumesMortels.MODID);

    public static final List<DeferredItem<Item>> BATONS = new ArrayList<>();
    public static final List<DeferredItem<Item>> ECLATS = new ArrayList<>();
    public static final Map<String, DeferredBlock<Block>> BLOCS_PAR_ID = new LinkedHashMap<>();
    public static final List<DeferredItem<Item>> OEUFS_MOBS = new ArrayList<>();
    public static final List<DeferredItem<Item>> OEUFS_MONTURES = new ArrayList<>();

    public static final DeferredItem<Item> PIERRE_BRUTE = OBJETS.registerSimpleItem("pierre_royaumes_brute", p -> p.rarity(Rarity.UNCOMMON));
    public static final DeferredItem<Item> CRISTAL = OBJETS.registerItem("cristal_arcanique", CristalArcanique::new, p -> p.rarity(Rarity.RARE).stacksTo(16));
    public static final DeferredItem<Item> GRIMOIRE = OBJETS.registerItem("grimoire_des_vents", GrimoireVents::new, p -> p.rarity(Rarity.RARE).stacksTo(1));
    public static final DeferredItem<Item> MARTEAU = OBJETS.registerItem("marteau_tempete", Item::new,
            p -> p.sword(ToolMaterial.NETHERITE, 5.0F, -3.0F).rarity(Rarity.EPIC).fireResistant());

    static {
        for (int i = 0; i < ContenuGenere.VENTS.length; i++) {
            final int vent = i;
            String v = ContenuGenere.VENTS[i];
            BATONS.add(OBJETS.registerItem("baton_" + v, p -> new BatonVent(p, vent), p -> p.stacksTo(1).rarity(Rarity.RARE)));
            ECLATS.add(OBJETS.registerSimpleItem("eclat_" + v, p -> p.rarity(Rarity.UNCOMMON)));
        }
        for (int i = 0; i < ContenuGenere.BLOCS.length; i++) {
            final String id = ContenuGenere.BLOCS[i];
            final float durete = ContenuGenere.BLOCS_DURETE[i];
            final int lumiere = ContenuGenere.BLOCS_LUMIERE[i];
            final boolean bois = ContenuGenere.BLOCS_BOIS[i];
            final String special = ContenuGenere.BLOCS_SPECIAL[i];
            DeferredBlock<Block> bloc = BLOCS.registerBlock(id, props -> switch (special) {
                case "AUTEL" -> new BlocAutel(props);
                case "PORTAIL" -> new BlocPortail(props);
                case "CAMP" -> new BlocEtendard(props);
                default -> new Block(props);
            }, p -> proprietes(p, durete, lumiere, bois));
            BLOCS_PAR_ID.put(id, bloc);
            OBJETS.registerSimpleBlockItem(bloc);
        }
        for (String id : ContenuGenere.OEUFS_MOBS) {
            var type = ModEntites.ENTITES.get(id);
            if (type != null) {
                OEUFS_MOBS.add(OBJETS.registerItem("oeuf_" + id, SpawnEggItem::new, p -> p.spawnEgg(type.get())));
            }
        }
        for (String id : ContenuGenere.OEUFS_MONTURES) {
            var type = ModEntites.MONTURES.get(id);
            if (type != null) {
                OEUFS_MONTURES.add(OBJETS.registerItem("oeuf_" + id, SpawnEggItem::new, p -> p.spawnEgg(type.get())));
            }
        }

        ONGLETS.register("armes", () -> CreativeModeTab.builder()
                .title(Component.translatable("itemGroup.royaumes.armes"))
                .icon(() -> new ItemStack(MARTEAU.get()))
                .displayItems((params, sortie) -> {
                    sortie.accept(MARTEAU.get());
                    depuisDatapack(params, sortie, "armes");
                }).build());
        ONGLETS.register("magie", () -> CreativeModeTab.builder()
                .title(Component.translatable("itemGroup.royaumes.magie"))
                .icon(() -> new ItemStack(BATONS.get(0).get()))
                .displayItems((params, sortie) -> {
                    BATONS.forEach(b -> sortie.accept(b.get()));
                    ECLATS.forEach(e -> sortie.accept(e.get()));
                    sortie.accept(PIERRE_BRUTE.get());
                    sortie.accept(CRISTAL.get());
                    sortie.accept(GRIMOIRE.get());
                    sortie.accept(BLOCS_PAR_ID.get("autel_arcanique").get());
                    depuisDatapack(params, sortie, "magie");
                }).build());
        ONGLETS.register("blocs", () -> CreativeModeTab.builder()
                .title(Component.translatable("itemGroup.royaumes.blocs"))
                .icon(() -> new ItemStack(BLOCS_PAR_ID.get("marbre_celeste_grave").get()))
                .displayItems((params, sortie) -> BLOCS_PAR_ID.values().forEach(b -> sortie.accept(b.get())))
                .build());
        ONGLETS.register("creatures", () -> CreativeModeTab.builder()
                .title(Component.translatable("itemGroup.royaumes.creatures"))
                .icon(() -> OEUFS_MOBS.isEmpty() ? new ItemStack(PIERRE_BRUTE.get()) : new ItemStack(OEUFS_MOBS.get(0).get()))
                .displayItems((params, sortie) -> OEUFS_MOBS.forEach(o -> sortie.accept(o.get())))
                .build());
        ONGLETS.register("montures", () -> CreativeModeTab.builder()
                .title(Component.translatable("itemGroup.royaumes.montures"))
                .icon(() -> new ItemStack(BLOCS_PAR_ID.get("portail_des_royaumes").get()))
                .displayItems((params, sortie) -> {
                    sortie.accept(BLOCS_PAR_ID.get("portail_des_royaumes").get());
                    sortie.accept(BLOCS_PAR_ID.get("etendard_de_camp").get());
                    OEUFS_MONTURES.forEach(o -> sortie.accept(o.get()));
                    depuisDatapack(params, sortie, "montures");
                }).build());
    }

    private ModObjets() {}

    private static BlockBehaviour.Properties proprietes(BlockBehaviour.Properties p, float durete, int lumiere, boolean bois) {
        if (bois && lumiere > 0) {
            p = p.noOcclusion();
        }
        p = p.strength(durete, durete >= 20.0F ? 1200.0F : durete * 2.0F)
                .lightLevel(etat -> lumiere)
                .sound(bois ? SoundType.WOOD : SoundType.STONE);
        return bois ? p : p.requiresCorrectToolForDrops();
    }

    public static void enregistrer(IEventBus modBus) {
        BLOCS.register(modBus);
        OBJETS.register(modBus);
        ONGLETS.register(modBus);
    }

    // ------------------------------------------------------------------ objets du datapack (armes, kits, forge…)

    private static final Map<String, JsonArray> CACHE = new HashMap<>();

    private static JsonArray lire(String nom) {
        return CACHE.computeIfAbsent(nom, n -> {
            try (InputStream in = ModObjets.class.getResourceAsStream("/royaumes_creatif/" + n + ".json")) {
                if (in == null) {
                    return new JsonArray();
                }
                return JsonParser.parseReader(new InputStreamReader(in, StandardCharsets.UTF_8)).getAsJsonArray();
            } catch (Exception e) {
                RoyaumesMortels.LOGGER.warn("[Royaumes Mortels] Onglet créatif {} illisible : {}", n, e.toString());
                return new JsonArray();
            }
        });
    }

    private static void depuisDatapack(CreativeModeTab.ItemDisplayParameters params, CreativeModeTab.Output sortie, String nom) {
        RegistryOps<JsonElement> ops = RegistryOps.create(JsonOps.INSTANCE, params.holders());
        List<ItemStack> deja = new ArrayList<>();
        int rejets = 0;
        for (JsonElement e : lire(nom)) {
            var r = ItemStack.CODEC.parse(ops, e).result();
            if (r.isEmpty() || r.get().isEmpty()) {
                rejets++;
                continue;
            }
            ItemStack pile = r.get();
            if (deja.stream().noneMatch(d -> ItemStack.isSameItemSameComponents(d, pile))) {
                deja.add(pile);
                sortie.accept(pile);
            }
        }
        if (rejets > 0) {
            RoyaumesMortels.LOGGER.warn("[Royaumes Mortels] Onglet {} : {} objet(s) du datapack ignoré(s)", nom, rejets);
        }
    }
}
