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
            if (c.profil().boss()) {
                // âmes de seigneur (paliers Mythique et Divin) : 2 à 3, +1 par héros supplémentaire au combat
                var heros = fr.royaumes.entite.Seigneurs.heros(c);
                if (relique != null) {
                    tirerRelique(c, relique.get(), heros, event.getSource().getEntity());
                }
                int ames = 2 + c.getRandom().nextInt(2) + Math.max(0, heros.size() - 1);
                c.level().addFreshEntity(new net.minecraft.world.entity.item.ItemEntity(c.level(), c.getX(), c.getY() + 1.5, c.getZ(),
                        new net.minecraft.world.item.ItemStack(fr.royaumes.arsenal.Arsenal.AME.get(), ames)));
                net.minecraft.server.level.ServerPlayer tueur = EvenementsCamp.heros(event.getSource().getEntity());
                if (tueur != null && !heros.contains(tueur)) {
                    fr.royaumes.rpg.Quetes.seigneur(tueur);
                }
                heros.forEach(fr.royaumes.rpg.Quetes::seigneur);
                // gloire de la victoire (le datapack ne la donnait qu'aux anciens boss de son équipe rm_boss)
                for (var h : heros) {
                    fr.royaumes.bloc.BlocPortail.executer(h, "scoreboard players set #gain rm_tmp 400");
                    fr.royaumes.bloc.BlocPortail.executer(h, "function royaumes:rpg/ajouter");
                }
                fr.royaumes.entite.Seigneurs.fin(c);
            } else {
                // le héros, ou une unité alliée (invocation de capacité, relique, sort, troupe du camp) qui travaille pour lui
                net.minecraft.server.level.ServerPlayer tueur = heros(event.getSource().getEntity());
                if (tueur != null) {
                    String equipe = c.profil().equipe();
                    fr.royaumes.rpg.Quetes.tuer(tueur, equipe.startsWith("rm_") ? equipe.substring(3) : equipe);
                }
            }
        }
    }

    /** Héros à qui revient une victime : le joueur lui-même ou le chef d'une unité alliée (tags rm_allie_ / rm_chef_). */
    static net.minecraft.server.level.ServerPlayer heros(net.minecraft.world.entity.Entity e) {
        if (e instanceof net.minecraft.server.level.ServerPlayer p) {
            return p;
        }
        if (e == null || e.level().getServer() == null) {
            return null;
        }
        for (String t : e.entityTags()) {
            String id = t.startsWith("rm_allie_") ? t.substring(9) : t.startsWith("rm_chef_") ? t.substring(8) : null;
            if (id != null) {
                try {
                    return e.level().getServer().getPlayerList().getPlayer(java.util.UUID.fromString(id));
                } catch (IllegalArgumentException ignore) {
                    return null;
                }
            }
        }
        return null;
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

    /**
     * La relique d'un seigneur est rare : 10 %, +5 % par héros en plus au combat, et +8 % par victoire sans relique (pitié,
     * comptée par héros dans rm_pitie et remise à zéro quand une relique tombe). Seul : en moyenne une relique toutes les ~4 victoires, au pire 12.
     */
    static void tirerRelique(Combattant c, net.minecraft.world.item.Item relique, java.util.List<net.minecraft.server.level.ServerPlayer> heros,
                             net.minecraft.world.entity.Entity tueur) {
        java.util.List<net.minecraft.server.level.ServerPlayer> l = new java.util.ArrayList<>(heros);
        if (tueur instanceof net.minecraft.server.level.ServerPlayer sp && !l.contains(sp)) {
            l.add(sp);
        }
        int pitie = 0;
        for (var h : l) {
            pitie = Math.max(pitie, fr.royaumes.rpg.Quetes.get(h, "rm_pitie"));
        }
        double chance = 0.10 + 0.05 * Math.max(0, l.size() - 1) + 0.08 * pitie;
        if (c.getRandom().nextDouble() < chance) {
            c.level().addFreshEntity(new net.minecraft.world.entity.item.ItemEntity(c.level(), c.getX(), c.getY() + 1, c.getZ(),
                    new net.minecraft.world.item.ItemStack(relique)));
            for (var h : l) {
                fr.royaumes.rpg.Quetes.set(h, "rm_pitie", 0);
            }
            String nom = new net.minecraft.world.item.ItemStack(relique).getHoverName().getString().replace("\"", "'");
            if (!l.isEmpty()) {
                fr.royaumes.bloc.BlocPortail.executer(l.get(0), "tellraw @a [{\"text\":\"✦ Relique ! \",\"color\":\"light_purple\",\"bold\":true},"
                        + "{\"text\":\"" + nom + "\",\"color\":\"gold\"},{\"text\":\" est tombée de la dépouille du seigneur.\",\"color\":\"gray\"}]");
                fr.royaumes.bloc.BlocPortail.executer(l.get(0), "playsound minecraft:ui.toast.challenge_complete master @a ~ ~ ~ 1 0.7");
            }
        } else {
            for (var h : l) {
                fr.royaumes.rpg.Quetes.set(h, "rm_pitie", fr.royaumes.rpg.Quetes.get(h, "rm_pitie") + 1);
                h.sendSystemMessage(net.minecraft.network.chat.Component.literal("La relique du seigneur ne s'est pas révélée cette fois ("
                        + Math.min(100, (int) Math.round(100 * (chance + 0.08))) + " % la prochaine fois).")
                        .withStyle(net.minecraft.ChatFormatting.DARK_PURPLE));
            }
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
