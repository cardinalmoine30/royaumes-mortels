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
                // gloire de la victoire (le datapack ne la donnait qu'aux anciens boss de son équipe rm_boss)
                for (var h : heros) {
                    fr.royaumes.bloc.BlocPortail.executer(h, "scoreboard players set #gain rm_tmp 400");
                    fr.royaumes.bloc.BlocPortail.executer(h, "function royaumes:rpg/ajouter");
                }
                fr.royaumes.entite.Seigneurs.fin(c);
            } else if (event.getSource().getEntity() instanceof net.minecraft.server.level.ServerPlayer tueur) {
                String equipe = c.profil().equipe();
                fr.royaumes.rpg.Quetes.tuer(tueur, equipe.startsWith("rm_") ? equipe.substring(3) : equipe);
            }
        }
    }

    /** Équilibrage : les guerriers de faction (hors troupes de camp et seigneurs) frappent les héros 25 % moins fort. */
    public static void degats(net.neoforged.neoforge.event.entity.living.LivingIncomingDamageEvent event) {
        if (!(event.getEntity() instanceof net.minecraft.server.level.ServerPlayer joueur)
                || !(event.getSource().getEntity() instanceof Combattant c) || c.entityTags().contains(Camps.UNITE)) {
            return;
        }
        if (c.profil().boss()) {
            // les seigneurs s'adaptent : +20 % de dégâts par palier d'armure au-dessus d'Élite (Divin : x1,6)
            int palier = palierArmure(joueur);
            if (palier >= 2) {
                event.setAmount(event.getAmount() * (1.0F + 0.2F * (palier - 1)));
            }
        } else if (fr.royaumes.rpg.Quetes.get(joueur, "rm_niveau") < 20) {
            // équilibrage des débuts : les guerriers frappent les héros novices 25 % moins fort
            event.setAmount(event.getAmount() * 0.75F);
        }
    }

    /** Plus bas palier des pièces d'arsenal portées (−1 sans armure complète d'arsenal). */
    static int palierArmure(net.minecraft.server.level.ServerPlayer p) {
        int min = 9;
        for (var s : new net.minecraft.world.entity.EquipmentSlot[] {net.minecraft.world.entity.EquipmentSlot.HEAD,
                net.minecraft.world.entity.EquipmentSlot.CHEST, net.minecraft.world.entity.EquipmentSlot.LEGS,
                net.minecraft.world.entity.EquipmentSlot.FEET}) {
            if (!(p.getItemBySlot(s).getItem() instanceof fr.royaumes.arsenal.ArmureFaction a)) {
                return -1;
            }
            min = Math.min(min, a.palier());
        }
        return min;
    }
}
