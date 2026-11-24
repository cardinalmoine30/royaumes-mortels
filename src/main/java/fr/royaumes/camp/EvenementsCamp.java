package fr.royaumes.camp;

import fr.royaumes.entite.Combattant;
import net.neoforged.neoforge.event.entity.living.LivingDeathEvent;
import net.neoforged.neoforge.event.tick.EntityTickEvent;

/** Branche le comportement des unités de camp sur les événements du jeu. */
public final class EvenementsCamp {
    private EvenementsCamp() {}

    public static void tickEntite(EntityTickEvent.Post event) {
        if (event.getEntity() instanceof Combattant c && !c.level().isClientSide() && c.tickCount % 20 == 7
                && c.entityTags().contains(Camps.UNITE)) {
            Camps.tickUnite(c);
        }
    }

    public static void mort(LivingDeathEvent event) {
        if (event.getEntity() instanceof Combattant c && !c.level().isClientSide()) {
            if (c.entityTags().contains(Camps.UNITE)) {
                Camps.mortUnite(c);
            }
            // un seigneur vaincu lâche sa relique unique
            String id = net.minecraft.core.registries.BuiltInRegistries.ENTITY_TYPE.getKey(c.getType()).getPath();
            var relique = fr.royaumes.ModObjets.RELIQUES.get(id);
            if (relique != null && c.profil().boss()) {
                c.level().addFreshEntity(new net.minecraft.world.entity.item.ItemEntity(c.level(), c.getX(), c.getY() + 1, c.getZ(),
                        new net.minecraft.world.item.ItemStack(relique.get())));
            }
        }
    }

    /** Équilibrage : les guerriers de faction (hors troupes de camp et seigneurs) frappent les héros 25 % moins fort. */
    public static void degats(net.neoforged.neoforge.event.entity.living.LivingIncomingDamageEvent event) {
        if (event.getEntity() instanceof net.minecraft.world.entity.player.Player
                && event.getSource().getEntity() instanceof Combattant c && !c.profil().boss() && !c.entityTags().contains(Camps.UNITE)) {
            event.setAmount(event.getAmount() * 0.75F);
        }
    }
}
