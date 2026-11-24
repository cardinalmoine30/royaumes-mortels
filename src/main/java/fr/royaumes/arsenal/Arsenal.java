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
    /** Première ligne des armes de faction dans la Forge (après les 5 paliers de 9 lignes). */
    public static final int LIGNE_ARMES = ArsenalGenere.PALIERS.length * 9;
    /** Tous les objets de l'arsenal (pour le menu créatif). */
    public static final List<DeferredItem<Item>> TOUS = new ArrayList<>();
    /** Outils d'alliance : objet -> {alliance 0-3, outil 0-4, palier 0-2}. */
    static final Map<Item, int[]> INFOS_OUTILS = new HashMap<>();
    private static final List<Object[]> OUTILS_A_INDEXER = new ArrayList<>();

    private Arsenal() {}

    /** Défense par palier (bottes, jambières, torse, casque) : fer 15, diamant 20, puis 24, 24, 25 (netherite : 20). Au-delà de
     *  Légende, la défense progresse peu : les paliers Mythique et Divin apportent surtout des pouvoirs (voir simulation d'équilibrage). */
    private static final int[][] DEFENSE = {{2, 5, 6, 2}, {3, 6, 8, 3}, {4, 7, 9, 4}, {4, 7, 9, 4}, {4, 8, 9, 4}};
    private static final int[] DURABILITE = {15, 33, 45, 55, 70};
    private static final int[] ENCHANT = {9, 10, 18, 20, 25};
    private static final float[] ROBUSTESSE = {0.0F, 2.0F, 4.0F, 4.5F, 5.0F};
    private static final float[] RECUL = {0.0F, 0.0F, 0.15F, 0.2F, 0.25F};
    private static final Rarity[] RARETE = {Rarity.UNCOMMON, Rarity.RARE, Rarity.EPIC, Rarity.EPIC, Rarity.EPIC};

    private static ArmorMaterial materiau(String faction, int palier) {
        int[] d = DEFENSE[palier];
        return new ArmorMaterial(DURABILITE[palier], Map.of(ArmorType.BOOTS, d[0], ArmorType.LEGGINGS, d[1], ArmorType.CHESTPLATE, d[2],
                ArmorType.HELMET, d[3], ArmorType.BODY, d[2] + 3), ENCHANT[palier],
                palier == 0 ? SoundEvents.ARMOR_EQUIP_IRON : palier == 1 ? SoundEvents.ARMOR_EQUIP_DIAMOND : SoundEvents.ARMOR_EQUIP_NETHERITE,
                ROBUSTESSE[palier], RECUL[palier],
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

    /** Métaux au-dessus de la netherite (2031 / 9 / +4) : Légende, Mythique, Divin. */
    static final ToolMaterial LEGENDE = metal(2800, 11.0F, 5.0F, 18);
    static final ToolMaterial MYTHIQUE = metal(3800, 14.0F, 6.0F, 20);
    static final ToolMaterial DIVIN = metal(5200, 18.0F, 7.0F, 25);
    private static final ToolMaterial[] MATERIAUX = {ToolMaterial.IRON, ToolMaterial.DIAMOND, LEGENDE, MYTHIQUE, DIVIN};

    private static ToolMaterial metal(int durabilite, float vitesse, float degats, int enchant) {
        return new ToolMaterial(net.minecraft.tags.BlockTags.INCORRECT_FOR_NETHERITE_TOOL, durabilite, vitesse, degats, enchant,
                ItemTags.NETHERITE_TOOL_MATERIALS);
    }

    /** Âme de seigneur : lâchée par les seigneurs vaincus (paliers Mythique, Divin et armes d'ascension). */
    public static DeferredItem<Item> AME;

    /** Appelé pendant l'initialisation statique de ModObjets. */
    public static void enregistrer() {
        AME = ModObjets.OBJETS.registerSimpleItem("ame_de_seigneur", p -> p.rarity(Rarity.EPIC));
        TOUS.add(AME);
        final int paliers = ArsenalGenere.PALIERS.length;
        // outils d'alliance, communs à toutes les factions d'une alliance
        for (int a = 0; a < ArsenalGenere.ALLIANCES.length; a++) {
            for (int t = 0; t < paliers; t++) {
                for (int o = 0; o < ArsenalGenere.OUTILS.length; o++) {
                    final int al = a;
                    final int pal = t;
                    final ToolMaterial m = MATERIAUX[t];
                    String outil = ArsenalGenere.OUTILS[o];
                    String id = ArsenalGenere.ALLIANCES[a] + "_" + outil + "_" + ArsenalGenere.PALIERS[t];
                    float bonus = 0.0F;
                    DeferredItem<Item> it = switch (outil) {
                        case "pioche" -> ModObjets.OBJETS.registerItem(id, p -> new OutilAlliance(p, al, pal, false),
                                p -> p.pickaxe(m, 1.0F + bonus, -2.8F).rarity(RARETE[pal]));
                        case "pelle" -> ModObjets.OBJETS.registerItem(id, p -> new OutilAlliance(p, al, pal, false),
                                p -> p.shovel(m, 1.5F + bonus, -3.0F).rarity(RARETE[pal]));
                        case "hache" -> ModObjets.OBJETS.registerItem(id, p -> new OutilAlliance(p, al, pal, false),
                                p -> p.axe(m, 5.0F + bonus, -3.0F).rarity(RARETE[pal]));
                        case "houe" -> ModObjets.OBJETS.registerItem(id, p -> new OutilAlliance(p, al, pal, false),
                                p -> p.hoe(m, -2.0F, Math.min(0.0F, -1.0F + pal)).rarity(RARETE[pal]));
                        default -> ModObjets.OBJETS.registerItem(id, p -> new OutilAlliance(p, al, pal, true),
                                p -> p.sword(m, 3.0F + bonus, -2.4F).rarity(RARETE[pal]));
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
            for (int t = 0; t < paliers; t++) {
                final int pal = t;
                ArmorMaterial mat = materiau(fid, t);
                for (int k = 0; k < 4; k++) {
                    final ArmorType at = types[k];
                    TOUS.add(ModObjets.OBJETS.registerItem(ArsenalGenere.IDS[f][t * 9 + k], p -> new ArmureFaction(p, faction, pal),
                            p -> p.humanoidArmor(mat, at).rarity(RARETE[pal])));
                }
            }
            // armes de faction : lignée (diamant), champion (netherite), ascension (métal divin)
            for (int r = 0; r < 3; r++) {
                final int rang = r;
                int k = LIGNE_ARMES + r;
                String type = ArsenalGenere.TYPES[f][k];
                float[] st = ArsenalGenere.STATS[typeArme(type)][r == 0 ? 1 : 0];
                ToolMaterial m = r == 0 ? ToolMaterial.DIAMOND : r == 1 ? ToolMaterial.NETHERITE : DIVIN;
                TOUS.add(ModObjets.OBJETS.registerItem(ArsenalGenere.IDS[f][k], p -> new ArmeFaction(p, faction, rang, type.split(":")[0]),
                        p -> p.sword(m, st[0], st[1]).rarity(rang == 0 ? Rarity.RARE : Rarity.EPIC)));
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
     * Élite = tous les effets, Légende = +1 niveau, Mythique = +4 cœurs, Divin = +8 cœurs (Résistance et Régénération plafonnées au
     * niveau I). Outil d'alliance en main (héros de l'alliance) : son effet, plus fort à chaque palier.
     */
    public static void bonusPanoplie(ServerPlayer p) {
        int fa = scoreFaction(p);
        int[] outil = infosOutil(p.getMainHandItem().getItem());
        if (outil != null && outil[0] == alliance(fa) && outil[1] < 4) {
            String e = ArsenalGenere.BUFFS_OUTILS[outil[0]][outil[1]];
            int niv = e.equals("regeneration") || e.equals("resistance") ? 0 : Math.min(3, outil[2]);
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
        for (Map.Entry<String, Integer> e : effetsPanoplie(faction, palier).entrySet()) {
            effet(p, e.getKey(), e.getValue());
        }
    }

    /** Effets de la panoplie complète d'une faction à un palier (effet -> amplificateur). */
    public static Map<String, Integer> effetsPanoplie(int faction, int palier) {
        Map<String, Integer> r = new java.util.LinkedHashMap<>();
        String[] bonus = ArsenalGenere.BONUS[faction].split(",");
        int plus = new int[] {0, 0, 1, 1, 1}[Math.min(4, palier)];
        for (int i = 0; i < (palier == 0 ? 1 : bonus.length); i++) {
            String[] x = bonus[i].split(":");
            // équilibrage 0.16 : jamais plus de Résistance I ni de Régénération I ; le reste plafonne au niveau II
            int cap = switch (x[0]) {
                case "resistance", "regeneration", "invisibility", "fire_resistance", "water_breathing", "night_vision" -> 0;
                case "health_boost" -> 2;
                default -> 1;
            };
            r.merge(x[0], Math.min(cap, Integer.parseInt(x[1]) + plus), Math::max);
        }
        if (palier >= 3) {
            r.merge("health_boost", palier == 3 ? 0 : 1, Math::max);
        }
        return r;
    }

    // ------------------------------------------------------------------ forge

    public static int compter(Inventory inv, Item item) {
        int n = 0;
        for (int i = 0; i < inv.getContainerSize(); i++) {
            ItemStack s = inv.getItem(i);
            if (s.is(item)) {
                n += s.getCount();
            }
        }
        return n;
    }

    public static void retirer(Inventory inv, Item item, int n) {
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
            p.sendSystemMessage(fr.royaumes.rpg.Quetes.avecTouches("La Forge de guerre ne répond qu'aux héros ayant prêté serment (touche [serment]).").withStyle(ChatFormatting.RED));
            return;
        }
        int requis = k < ArsenalGenere.NIVEAUX.length ? ArsenalGenere.NIVEAUX[k] : 1;
        var sb = p.level().getServer().getScoreboard();
        var on = sb.getObjective("rm_niveau");
        var ni = on == null ? null : sb.getPlayerScoreInfo(p, on);
        if ((ni == null ? 1 : ni.value()) < requis && !p.isCreative()) {
            p.sendSystemMessage(Component.literal("Les maîtres-forgerons refusent : il faut être héros de niveau " + requis + " pour porter cela.")
                    .withStyle(ChatFormatting.RED));
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
        p.sendSystemMessage(Component.literal("⚒ " + (k < 9 || k == LIGNE_ARMES ? "Forgé" : "Amélioré") + " : ").append(fait.getHoverName()).withStyle(ChatFormatting.GOLD));
        fr.royaumes.magie.Saga.accorder(p, "forge_guerre");
        fr.royaumes.rpg.Quetes.evenement(p, "forge:" + (k < LIGNE_ARMES ? String.valueOf(k / 9) : "arme" + (k - LIGNE_ARMES)));
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
