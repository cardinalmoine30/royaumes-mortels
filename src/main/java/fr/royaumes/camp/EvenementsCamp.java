package fr.royaumes.camp;

import fr.royaumes.entite.Combattant;
import net.neoforged.neoforge.event.entity.living.LivingDeathEvent;
import net.neoforged.neoforge.event.tick.EntityTickEvent;

/** Branche le comportement des unités de camp sur les événements du jeu. */
public final class EvenementsCamp {
    private EvenementsCamp() {}

    public static void tickEntite(EntityTickEvent.Post event) {
        if (event.getEntity() instanceof Combattant c && !c.level().isClientSide() && c.tickCount % 20 == 7
                && c.getTags().contains(Camps.UNITE)) {
            Camps.tickUnite(c);
        }
    }

    public static void mort(LivingDeathEvent event) {
        if (event.getEntity() instanceof Combattant c && !c.level().isClientSide() && c.getTags().contains(Camps.UNITE)) {
            Camps.mortUnite(c);
        }
    }
}
