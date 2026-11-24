package fr.royaumes.magie;

import fr.royaumes.bloc.BlocPortail;
import java.util.HashSet;
import java.util.Set;
import net.minecraft.server.level.ServerPlayer;

/** Progrès « Saga des Royaumes » accordés par le mod (critères impossibles côté datapack). */
public final class Saga {
    private static final Set<String> DEJA = new HashSet<>();

    private Saga() {}

    public static void accorder(ServerPlayer p, String progres) {
        if (DEJA.add(p.getUUID() + progres)) {
            BlocPortail.executer(p, "advancement grant @s only royaumes:saga/" + progres);
        }
    }
}
