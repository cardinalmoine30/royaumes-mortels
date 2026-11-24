package fr.royaumes.arsenal;

import fr.royaumes.ArsenalGenere;
import fr.royaumes.FactionsGenerees;
import fr.royaumes.ModObjets;
import fr.royaumes.RoyaumesMortels;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import net.minecraft.ChatFormatting;
import net.minecraft.core.Holder;
import net.minecraft.core.particles.ParticleTypes;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.network.chat.Component;
import net.minecraft.resources.Identifier;
import net.minecraft.resources.ResourceKey;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.sounds.SoundSource;
import net.minecraft.tags.ItemTags;
import net.minecraft.world.effect.MobEffect;
import net.minecraft.world.effect.MobEffectInstance;
import net.minecraft.world.entity.EquipmentSlot;
import net.minecraft.world.entity.player.Inventory;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.Rarity;
import net.minecraft.world.item.ToolMaterial;
import net.minecraft.world.item.equipment.ArmorMaterial;
import net.minecraft.world.item.equipment.ArmorType;
import net.minecraft.world.item.equipment.EquipmentAssets;
import net.neoforged.neoforge.registries.DeferredItem;

/**
 * Arsenal des 25 factions (ArsenalGenere, outils/objets/arsenal.py) : arme de champion (netherite, très puissante),
 * arme de lignée (diamant, atout spécial à chaque coup), armure en 4 pièces (bonus de panoplie complète).
 * Ces objets ne se fabriquent qu'à la Forge de guerre, et seulement par les héros de leur faction.
 */
public final class Arsenal {
    /** Tous les objets de l'arsenal (pour le menu créatif). */
    public static final List<DeferredItem<Item>> TOUS = new ArrayList<>();
    /** Outils d'alliance : objet -> {alliance 0-3, outil 0-4, palier 0-2}. */
    static final Map<Item, int[]> INFOS_OUTILS = new HashMap<>();
    private static final List<Object[]> OUTILS_A_INDEXER = new ArrayList<>();

    private Arsenal() {}

    private static final int[][] DEFENSE = {{2, 5, 6, 2}, {3, 6, 8, 3}, {3, 6, 8, 3}};

    private static ArmorMaterial materiau(String faction, int palier) {
        int[] d = DEFENSE[palier];
        return new ArmorMaterial(new int[] {15, 33, 37}[palier], Map.of(ArmorType.BOOTS, d[0], ArmorType.LEGGINGS, d[1], ArmorType.CHESTPLATE, d[2],
                ArmorType.HELMET, d[3], ArmorType.BODY, d[2] + 3), new int[] {9, 10, 15}[palier],
                palier == 0 ? SoundEvents.ARMOR_EQUIP_IRON : palier == 1 ? SoundEvents.ARMOR_EQUIP_DIAMOND : SoundEvents.ARMOR_EQUIP_NETHERITE,
                new float[] {0.0F, 2.0F, 3.0F}[palier], new float[] {0.0F, 0.0F, 0.1F}[palier],
                palier == 0 ? ItemTags.REPAIRS_IRON_ARMOR : palier == 1 ? ItemTags.REPAIRS_DIAMOND_ARMOR : ItemTags.REPAIRS_NETHERITE_ARMOR,
                ResourceKey.create(EquipmentAssets.ROOT_ID, Identifier.fromNamespaceAndPath(RoyaumesMortels.MODID,
                        faction + "_" + ArsenalGenere.PALIERS[palier])));
    }

    private static int typeArme(String t) {
        for (int i = 0; i < ArsenalGenere.TYPES_ARMES.length; i++) {
            if (t.startsWith(ArsenalGenere.TYPES_ARMES[i] + ":")) {
                return i;
            }
        }
        return 0;
    }

    private static final ToolMaterial[] MATERIAUX = {ToolMaterial.IRON, ToolMaterial.DIAMOND, ToolMaterial.NETHERITE};

    /** Appelé pendant l'initialisation statique de ModObjets. */
    public static void enregistrer() {
        // outils d'alliance, communs à toutes les factions d'une alliance
        for (int a = 0; a < ArsenalGenere.ALLIANCES.length; a++) {
            for (int t = 0; t < 3; t++) {
                for (int o = 0; o < ArsenalGenere.OUTILS.length; o++) {
                    final int al = a;
                    final int pal = t;
                    final ToolMaterial m = MATERIAUX[t];
                    String outil = ArsenalGenere.OUTILS[o];
                    String id = ArsenalGenere.ALLIANCES[a] + "_" + outil + "_" + ArsenalGenere.PALIERS[t];
                    float bonus = t == 2 ? 1.0F : 0.0F;
                    DeferredItem<Item> it = switch (outil) {
                        case "pioche" -> ModObjets.OBJETS.registerItem(id, p -> new OutilAlliance(p, al, pal, false), p -> p.pickaxe(m, 1.0F + bonus, -2.8F));
                        case "pelle" -> ModObjets.OBJETS.registerItem(id, p -> new OutilAlliance(p, al, pal, false), p -> p.shovel(m, 1.5F + bonus, -3.0F));
                        case "hache" -> ModObjets.OBJETS.registerItem(id, p -> new OutilAlliance(p, al, pal, false), p -> p.axe(m, 5.0F + bonus, -3.0F));
                        case "houe" -> ModObjets.OBJETS.registerItem(id, p -> new OutilAlliance(p, al, pal, false), p -> p.hoe(m, -2.0F, -1.0F + pal));
                        default -> ModObjets.OBJETS.registerItem(id, p -> new OutilAlliance(p, al, pal, true), p -> p.sword(m, 3.0F + bonus, -2.4F));
                    };
                    TOUS.add(it);
                    OUTILS_A_INDEXER.add(new Object[] {it, new int[] {a, o, t}});
                }
            }
        }
        for (int f = 1; f < ArsenalGenere.IDS.length; f++) {
            final int faction = f;
            String fid = FactionsGenerees.IDS[f];
            ArmorType[] types = {ArmorType.HELMET, ArmorType.CHESTPLATE, ArmorType.LEGGINGS, ArmorType.BOOTS};
            for (int t = 0; t < 3; t++) {
                final int pal = t;
                ArmorMaterial mat = materiau(fid, t);
                for (int k = 0; k < 4; k++) {
                    final ArmorType at = types[k];
                    TOUS.add(ModObjets.OBJETS.registerItem(ArsenalGenere.IDS[f][t * 9 + k], p -> new ArmureFaction(p, faction, pal),
                            p -> p.humanoidArmor(mat, at).rarity(pal == 2 ? Rarity.EPIC : pal == 1 ? Rarity.RARE : Rarity.UNCOMMON)));
                }
            }
            for (int k = 27; k < 29; k++) {
                final boolean champion = k == 28;
                String type = ArsenalGenere.TYPES[f][k];
                float[] st = ArsenalGenere.STATS[typeArme(type)][champion ? 0 : 1];
                TOUS.add(ModObjets.OBJETS.registerItem(ArsenalGenere.IDS[f][k], p -> new ArmeFaction(p, faction, champion, type.split(":")[0]),
                        p -> p.sword(champion ? ToolMaterial.NETHERITE : ToolMaterial.DIAMOND, st[0], st[1])
                                .rarity(champion ? Rarity.EPIC : Rarity.RARE)));
            }
        }
    }

    @SuppressWarnings("unchecked")
    static int[] infosOutil(Item item) {
        if (INFOS_OUTILS.isEmpty() && !OUTILS_A_INDEXER.isEmpty()) {
            for (Object[] o : OUTILS_A_INDEXER) {
                INFOS_OUTILS.put(((DeferredItem<Item>) o[0]).get(), (int[]) o[1]);
            }
        }
        return INFOS_OUTILS.get(item);
    }

    static int alliance(int faction) {
        if (faction <= 0 || faction >= fr.royaumes.ContenuGenere.ALLIANCES.length) {
            return -1;
        }
        String a = fr.royaumes.ContenuGenere.ALLIANCES[faction];
        for (int i = 0; i < ArsenalGenere.ALLIANCES.length; i++) {
            if (ArsenalGenere.ALLIANCES[i].equals(a)) {
                return i;
            }
        }
        return -1;
    }

    static void effet(ServerPlayer p, String nom, int niveau) {
        MobEffect effet = BuiltInRegistries.MOB_EFFECT.getValue(Identifier.withDefaultNamespace(nom));
        if (effet != null) {
            p.addEffect(new MobEffectInstance(BuiltInRegistries.MOB_EFFECT.wrapAsHolder(effet), nom.equals("night_vision") ? 300 : 60,
                    Math.max(0, niveau), true, false, true));
        }
    }

    // ------------------------------------------------------------------ bonus de panoplie

    /**
     * Chaque seconde. Panoplie complète d'une faction portée par un héros de cette faction : Soldat = premier effet,
     * Élite = tous les effets, Légende = tous les effets un niveau au-dessus. Outil d'alliance en main (héros de l'alliance) :
     * son effet, plus fort à chaque palier.
     */
    public static void bonusPanoplie(ServerPlayer p) {
        int fa = scoreFaction(p);
        int[] outil = infosOutil(p.getMainHandItem().getItem());
        if (outil != null && outil[0] == alliance(fa) && outil[1] < 4) {
            String e = ArsenalGenere.BUFFS_OUTILS[outil[0]][outil[1]];
            int niv = e.equals("regeneration") || e.equals("resistance") ? outil[2] / 2 : outil[2];
            effet(p, e, niv);
        }
        int faction = -1;
        int palier = 9;
        for (EquipmentSlot s : new EquipmentSlot[] {EquipmentSlot.HEAD, EquipmentSlot.CHEST, EquipmentSlot.LEGS, EquipmentSlot.FEET}) {
            if (!(p.getItemBySlot(s).getItem() instanceof ArmureFaction a)) {
                return;
            }
            if (faction >= 0 && a.faction() != faction) {
                return;
            }
            faction = a.faction();
            palier = Math.min(palier, a.palier());
        }
        if (faction != fa) {
            return;
        }
        String[] bonus = ArsenalGenere.BONUS[faction].split(",");
        for (int i = 0; i < (palier == 0 ? 1 : bonus.length); i++) {
            String[] x = bonus[i].split(":");
            effet(p, x[0], Integer.parseInt(x[1]) + (palier == 2 ? 1 : 0));
        }
    }

    // ------------------------------------------------------------------ forge

    static int compter(Inventory inv, Item item) {
        int n = 0;
        for (int i = 0; i < inv.getContainerSize(); i++) {
            ItemStack s = inv.getItem(i);
            if (s.is(item)) {
                n += s.getCount();
            }
        }
        return n;
    }

    static void retirer(Inventory inv, Item item, int n) {
        for (int i = 0; i < inv.getContainerSize() && n > 0; i++) {
            ItemStack s = inv.getItem(i);
            if (s.is(item)) {
                int k = Math.min(n, s.getCount());
                s.shrink(k);
                n -= k;
            }
        }
    }

    /** Forge l'objet k de la faction du joueur, si elle est la sienne et s'il a les matériaux. */
    public static void forger(ServerPlayer p, int k) {
        int faction = scoreFaction(p);
        if (faction <= 0 || faction >= ArsenalGenere.IDS.length || k < 0 || k >= ArsenalGenere.IDS[faction].length) {
            p.sendSystemMessage(Component.literal("La Forge de guerre ne répond qu'aux héros ayant prêté serment (touche J).").withStyle(ChatFormatting.RED));
            return;
        }
        Inventory inv = p.getInventory();
        String[] ingr = ArsenalGenere.RECETTES[faction][k].split(",");
        for (String x : ingr) {
            String[] a = x.split("\\*");
            Item item = BuiltInRegistries.ITEM.getValue(Identifier.parse(a[0]));
            if (compter(inv, item) < Integer.parseInt(a[1]) && !p.isCreative()) {
                p.sendSystemMessage(Component.literal("Il te manque des matériaux : " + Integer.parseInt(a[1]) + " × ")
                        .append(item.getName(new ItemStack(item))).withStyle(ChatFormatting.RED));
                return;
            }
        }
        if (!p.isCreative()) {
            for (String x : ingr) {
                String[] a = x.split("\\*");
                retirer(inv, BuiltInRegistries.ITEM.getValue(Identifier.parse(a[0])), Integer.parseInt(a[1]));
            }
        }
        ItemStack fait = new ItemStack(BuiltInRegistries.ITEM.getValue(Identifier.fromNamespaceAndPath(RoyaumesMortels.MODID, ArsenalGenere.IDS[faction][k])));
        if (!inv.add(fait)) {
            p.level().addFreshEntity(new net.minecraft.world.entity.item.ItemEntity(p.level(), p.getX(), p.getY() + 0.5, p.getZ(), fait));
        }
        ServerLevel l = (ServerLevel) p.level();
        l.sendParticles(ParticleTypes.LAVA, p.getX(), p.getY() + 1, p.getZ(), 12, 0.4, 0.4, 0.4, 0.1);
        l.playSound(null, p.blockPosition(), SoundEvents.ANVIL_USE, SoundSource.BLOCKS, 1.0F, 0.9F);
        p.sendSystemMessage(Component.literal("⚒ " + (k < 9 ? "Forgé" : "Amélioré") + " : ").append(fait.getHoverName()).withStyle(ChatFormatting.GOLD));
        fr.royaumes.magie.Saga.accorder(p, "forge_guerre");
    }

    static int scoreFaction(ServerPlayer p) {
        var sb = p.level().getServer().getScoreboard();
        var o = sb.getObjective("rm_faction");
        if (o == null) {
            return 0;
        }
        var i = sb.getPlayerScoreInfo(p, o);
        return i == null ? 0 : i.value();
    }
}
