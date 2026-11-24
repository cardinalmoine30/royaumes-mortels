package fr.royaumes.arsenal;

import fr.royaumes.ArsenalGenere;
import fr.royaumes.FactionsGenerees;
import fr.royaumes.ModObjets;
import fr.royaumes.RoyaumesMortels;
import fr.royaumes.camp.Camps;
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
    /** Objets par faction, dans l'ordre champion, lignée, casque, torse, jambes, bottes. */
    public static final List<List<DeferredItem<Item>>> PAR_FACTION = new ArrayList<>();
    static final Map<String, Integer> FACTION_ARMURE = new HashMap<>();

    private Arsenal() {}

    private static ArmorMaterial materiau(String faction) {
        return new ArmorMaterial(37, Map.of(ArmorType.BOOTS, 3, ArmorType.LEGGINGS, 6, ArmorType.CHESTPLATE, 8, ArmorType.HELMET, 3,
                ArmorType.BODY, 11), 15, SoundEvents.ARMOR_EQUIP_NETHERITE, 3.0F, 0.1F, ItemTags.REPAIRS_NETHERITE_ARMOR,
                ResourceKey.create(EquipmentAssets.ROOT_ID, Identifier.fromNamespaceAndPath(RoyaumesMortels.MODID, faction)));
    }

    private static int typeArme(String t) {
        for (int i = 0; i < ArsenalGenere.TYPES_ARMES.length; i++) {
            if (t.startsWith(ArsenalGenere.TYPES_ARMES[i] + ":")) {
                return i;
            }
        }
        return 0;
    }

    /** Appelé pendant l'initialisation statique de ModObjets. */
    public static void enregistrer() {
        PAR_FACTION.add(List.of());
        for (int f = 1; f < ArsenalGenere.IDS.length; f++) {
            final int faction = f;
            List<DeferredItem<Item>> l = new ArrayList<>();
            String fid = FactionsGenerees.IDS[f];
            ArmorMaterial mat = materiau(fid);
            ArmorType[] types = {ArmorType.HELMET, ArmorType.CHESTPLATE, ArmorType.LEGGINGS, ArmorType.BOOTS};
            for (int k = 0; k < 6; k++) {
                String id = ArsenalGenere.IDS[f][k];
                String type = ArsenalGenere.TYPES[f][k];
                if (k < 2) {
                    final boolean champion = k == 0;
                    float[] st = ArsenalGenere.STATS[typeArme(type)][champion ? 0 : 1];
                    l.add(ModObjets.OBJETS.registerItem(id, p -> new ArmeFaction(p, faction, champion, type.split(":")[0]),
                            p -> p.sword(champion ? ToolMaterial.NETHERITE : ToolMaterial.DIAMOND, st[0], st[1])
                                    .rarity(champion ? Rarity.EPIC : Rarity.RARE)));
                } else {
                    final ArmorType at = types[k - 2];
                    l.add(ModObjets.OBJETS.registerItem(id, p -> new ArmureFaction(p, faction), p -> p.humanoidArmor(mat, at).rarity(Rarity.RARE)));
                    FACTION_ARMURE.put(id, faction);
                }
            }
            PAR_FACTION.add(l);
        }
    }

    // ------------------------------------------------------------------ bonus de panoplie

    /** Chaque seconde : panoplie complète d'une faction = ses effets permanents. */
    public static void bonusPanoplie(ServerPlayer p) {
        int faction = -1;
        for (EquipmentSlot s : new EquipmentSlot[] {EquipmentSlot.HEAD, EquipmentSlot.CHEST, EquipmentSlot.LEGS, EquipmentSlot.FEET}) {
            if (!(p.getItemBySlot(s).getItem() instanceof ArmureFaction a)) {
                return;
            }
            if (faction >= 0 && a.faction() != faction) {
                return;
            }
            faction = a.faction();
        }
        for (String e : ArsenalGenere.BONUS[faction].split(",")) {
            String[] x = e.split(":");
            MobEffect effet = BuiltInRegistries.MOB_EFFECT.getValue(Identifier.withDefaultNamespace(x[0]));
            if (effet != null) {
                Holder<MobEffect> h = BuiltInRegistries.MOB_EFFECT.wrapAsHolder(effet);
                p.addEffect(new MobEffectInstance(h, x[0].equals("night_vision") ? 300 : 60, Integer.parseInt(x[1]), true, false, true));
            }
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
        int faction = Camps.niveauJoueur(p.level().getServer(), p) >= 0 ? scoreFaction(p) : 0;
        if (faction <= 0 || faction >= ArsenalGenere.IDS.length || k < 0 || k >= 6) {
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
        ItemStack fait = new ItemStack(PAR_FACTION.get(faction).get(k).get());
        if (!inv.add(fait)) {
            p.level().addFreshEntity(new net.minecraft.world.entity.item.ItemEntity(p.level(), p.getX(), p.getY() + 0.5, p.getZ(), fait));
        }
        ServerLevel l = (ServerLevel) p.level();
        l.sendParticles(ParticleTypes.LAVA, p.getX(), p.getY() + 1, p.getZ(), 12, 0.4, 0.4, 0.4, 0.1);
        l.playSound(null, p.blockPosition(), SoundEvents.ANVIL_USE, SoundSource.BLOCKS, 1.0F, 0.9F);
        p.sendSystemMessage(Component.literal("⚒ Forgé : " + ArsenalGenere.NOMS[faction][k]).withStyle(ChatFormatting.GOLD));
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
