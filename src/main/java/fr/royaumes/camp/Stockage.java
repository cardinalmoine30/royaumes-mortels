package fr.royaumes.camp;

import fr.royaumes.RoyaumesMortels;
import java.util.LinkedHashMap;
import java.util.Map;
import net.minecraft.ChatFormatting;
import net.minecraft.core.BlockPos;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.core.registries.Registries;
import net.minecraft.network.chat.Component;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.sounds.SoundSource;
import net.minecraft.world.CompoundContainer;
import net.minecraft.world.Container;
import net.minecraft.world.SimpleContainer;
import net.minecraft.world.SimpleMenuProvider;
import net.minecraft.world.entity.player.Inventory;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.flag.FeatureFlags;
import net.minecraft.world.inventory.ChestMenu;
import net.minecraft.world.inventory.MenuType;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.level.block.Blocks;
import net.neoforged.bus.api.IEventBus;
import net.neoforged.neoforge.registries.DeferredHolder;
import net.neoforged.neoforge.registries.DeferredRegister;

/**
 * Stockage du camp : 6 rangées. Les 5 premières gardent les affaires du héros ; la rangée du bas (dorée) est le
 * tribut : minerais, minerais bruts, lingots et gemmes vanilla (et ressources des Royaumes) déposés là deviennent du
 * butin quand on referme le stockage. Le butin sert à recruter, améliorer le camp et ses bâtiments.
 * Le contenu est rangé dans deux tonneaux enterrés sous l'Étendard (sauvegardés avec le monde).
 */
public final class Stockage {
    private Stockage() {}

    public static final DeferredRegister<MenuType<?>> MENUS = DeferredRegister.create(Registries.MENU, RoyaumesMortels.MODID);
    public static final DeferredHolder<MenuType<?>, MenuType<Menu>> TYPE = MENUS.register("stockage",
            () -> new MenuType<>((id, inv) -> new Menu(id, inv, new SimpleContainer(54)), FeatureFlags.DEFAULT_FLAGS));
    /** Première case de la rangée de tribut. */
    public static final int TRIBUT = 45;

    public static void enregistrer(IEventBus bus) {
        MENUS.register(bus);
    }

    /** Valeur en butin d'un objet déposé dans le tribut (0 = refusé, il reste dans sa case). */
    public static int valeur(ItemStack s) {
        if (s.isEmpty()) {
            return 0;
        }
        String n = BuiltInRegistries.ITEM.getKey(s.getItem()).toString();
        return switch (n) {
            case "minecraft:coal", "minecraft:raw_copper", "minecraft:copper_ingot", "minecraft:raw_iron", "minecraft:iron_ingot",
                 "minecraft:lapis_lazuli", "minecraft:redstone", "minecraft:quartz", "minecraft:amethyst_shard" -> 1;
            case "minecraft:coal_ore", "minecraft:deepslate_coal_ore", "minecraft:copper_ore", "minecraft:deepslate_copper_ore",
                 "minecraft:iron_ore", "minecraft:deepslate_iron_ore", "minecraft:nether_gold_ore", "minecraft:nether_quartz_ore" -> 2;
            case "minecraft:raw_gold" -> 3;
            case "minecraft:gold_ingot" -> 4;
            case "minecraft:gold_ore", "minecraft:deepslate_gold_ore", "minecraft:lapis_ore", "minecraft:deepslate_lapis_ore",
                 "minecraft:redstone_ore", "minecraft:deepslate_redstone_ore" -> 5;
            case "minecraft:emerald" -> 6;
            case "minecraft:emerald_ore", "minecraft:deepslate_emerald_ore", "minecraft:iron_block", "minecraft:raw_iron_block",
                 "minecraft:copper_block", "minecraft:raw_copper_block", "minecraft:coal_block", "minecraft:lapis_block",
                 "minecraft:redstone_block" -> 9;
            case "minecraft:diamond" -> 12;
            case "minecraft:diamond_ore", "minecraft:deepslate_diamond_ore" -> 15;
            case "minecraft:ancient_debris", "minecraft:netherite_scrap" -> 30;
            case "minecraft:raw_gold_block" -> 27;
            case "minecraft:gold_block" -> 36;
            case "minecraft:netherite_ingot" -> 40;
            case "minecraft:emerald_block" -> 54;
            case "minecraft:diamond_block" -> 108;
            case "royaumes:pierre_royaumes_brute" -> 5;
            case "royaumes:cristal_arcanique" -> 8;
            default -> n.startsWith("royaumes:eclat_") ? 6 : 0;
        };
    }

    /** Menu du stockage : coffre de 6 rangées dont la dernière convertit son contenu à la fermeture. */
    public static class Menu extends ChestMenu {
        public Menu(int id, Inventory inv, Container c) {
            super(TYPE.get(), id, inv, c, 6);
        }

        @Override
        public void removed(Player joueur) {
            if (joueur instanceof ServerPlayer sp) {
                convertir(sp, getContainer());
            }
            super.removed(joueur);
        }
    }

    private static Container tonneau(ServerLevel l, BlockPos pos) {
        if (!(l.getBlockEntity(pos) instanceof Container)) {
            l.setBlock(pos, Blocks.BARREL.defaultBlockState(), 3);
        }
        return l.getBlockEntity(pos) instanceof Container c ? c : new SimpleContainer(27);
    }

    public static void ouvrir(ServerPlayer p, BlockPos camp) {
        if (!(p.level() instanceof ServerLevel l)) {
            return;
        }
        Container c = new CompoundContainer(tonneau(l, camp.below(2)), tonneau(l, camp.below(3)));
        p.openMenu(new SimpleMenuProvider((id, inv, joueur) -> new Menu(id, inv, c),
                Component.literal("Stockage du camp")));
    }

    static void convertir(ServerPlayer p, Container c) {
        if (c.getContainerSize() < 54) {
            return;
        }
        int total = 0;
        boolean refuse = false;
        Map<String, Integer> detail = new LinkedHashMap<>();
        for (int i = TRIBUT; i < 54; i++) {
            ItemStack s = c.getItem(i);
            int v = valeur(s);
            if (v > 0) {
                total += v * s.getCount();
                detail.merge(s.getHoverName().getString(), s.getCount(), Integer::sum);
                c.setItem(i, ItemStack.EMPTY);
            } else if (!s.isEmpty()) {
                refuse = true;
            }
        }
        if (total > 0) {
            var sb = Camps.sb(p);
            Camps.set(sb, p, "rm_butin", Camps.get(sb, p, "rm_butin") + total);
            StringBuilder t = new StringBuilder();
            detail.forEach((k, n) -> t.append(t.length() > 0 ? ", " : "").append(n).append(" ").append(k));
            Camps.msg(p, "⚖ Tribut : " + t + " → +" + total + " butin (total " + Camps.get(sb, p, "rm_butin") + ").", ChatFormatting.GOLD);
            p.level().playSound(null, p.blockPosition(), SoundEvents.ANVIL_LAND, SoundSource.PLAYERS, 0.4F, 1.7F);
            fr.royaumes.rpg.Quetes.evenement(p, "stockage");
        }
        if (refuse) {
            Camps.msg(p, "La rangée dorée ne prend que les minerais, lingots, gemmes et ressources des Royaumes : le reste y attend.",
                    ChatFormatting.GRAY);
        }
    }
}
