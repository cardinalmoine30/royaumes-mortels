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
            if (c.profil().boss()) {
                // âmes de seigneur (paliers Mythique et Divin) : 2 à 3, +1 par héros supplémentaire au combat
                var heros = fr.royaumes.entite.Seigneurs.heros(c);
                int ames = 2 + c.getRandom().nextInt(2) + Math.max(0, heros.size() - 1);
                c.level().addFreshEntity(new net.minecraft.world.entity.item.ItemEntity(c.level(), c.getX(), c.getY() + 1.5, c.getZ(),
                        new net.minecraft.world.item.ItemStack(fr.royaumes.arsenal.Arsenal.AME.get(), ames)));
                if (event.getSource().getEntity() instanceof net.minecraft.server.level.ServerPlayer tueur && !heros.contains(tueur)) {
                    fr.royaumes.rpg.Quetes.seigneur(tueur);
                }
                heros.forEach(fr.royaumes.rpg.Quetes::seigneur);
                fr.royaumes.entite.Seigneurs.fin(c);
            } else if (event.getSource().getEntity() instanceof net.minecraft.server.level.ServerPlayer tueur) {
                String equipe = c.profil().equipe();
                fr.royaumes.rpg.Quetes.tuer(tueur, equipe.startsWith("rm_") ? equipe.substring(3) : equipe);
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
