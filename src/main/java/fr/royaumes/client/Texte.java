package fr.royaumes.client;

import java.util.ArrayList;
import java.util.List;
import net.minecraft.client.gui.Font;
import net.minecraft.client.gui.GuiGraphicsExtractor;

/**
 * Texte qui tient toujours dans sa place : une ligne trop longue est rétrécie (jusqu'à 70 %) puis coupée par « … » ;
 * un paragraphe est replié sur la largeur donnée et rétréci si ses lignes dépassent la hauteur disponible.
 */
public final class Texte {
    private Texte() {}

    static final float MIN = 0.7F;

    static String couper(Font f, String s, int max) {
        if (f.width(s) <= max) {
            return s;
        }
        while (s.length() > 1 && f.width(s + "…") > max) {
            s = s.substring(0, s.length() - 1);
        }
        return s.stripTrailing() + "…";
    }

    /** Une ligne à gauche, dans maxW pixels. */
    public static void ligne(GuiGraphicsExtractor g, Font f, String s, int x, int y, int maxW, int couleur, boolean ombre) {
        int w = f.width(s);
        if (w <= maxW) {
            g.text(f, s, x, y, couleur, ombre);
            return;
        }
        float k = Math.max(MIN, (float) maxW / w);
        String t = couper(f, s, (int) (maxW / k));
        g.pose().pushMatrix();
        g.pose().translate(x, y + (1 - k) * 4);
        g.pose().scale(k, k);
        g.text(f, t, 0, 0, couleur, ombre);
        g.pose().popMatrix();
    }

    /** Une ligne centrée sur cx, dans maxW pixels. */
    public static void centre(GuiGraphicsExtractor g, Font f, String s, int cx, int y, int maxW, int couleur) {
        int w = f.width(s);
        if (w <= maxW) {
            g.text(f, s, cx - w / 2, y, couleur, true);
            return;
        }
        float k = Math.max(MIN, (float) maxW / w);
        String t = couper(f, s, (int) (maxW / k));
        float largeur = f.width(t) * k;
        g.pose().pushMatrix();
        g.pose().translate(cx - largeur / 2, y + (1 - k) * 4);
        g.pose().scale(k, k);
        g.text(f, t, 0, 0, couleur, true);
        g.pose().popMatrix();
    }

    static List<String> replier(Font f, String s, int w) {
        List<String> l = new ArrayList<>();
        StringBuilder cur = new StringBuilder();
        for (String mot : s.split(" ")) {
            String essai = cur.length() == 0 ? mot : cur + " " + mot;
            if (f.width(essai) > w && cur.length() > 0) {
                l.add(cur.toString());
                cur = new StringBuilder(mot);
            } else {
                cur = new StringBuilder(essai);
            }
        }
        if (cur.length() > 0) {
            l.add(cur.toString());
        }
        return l;
    }

    /** Paragraphe dans un cadre w × maxH ; renvoie la hauteur réellement utilisée. */
    public static int bloc(GuiGraphicsExtractor g, Font f, String s, int x, int y, int w, int maxH, int couleur, boolean ombre) {
        float k = 1.0F;
        List<String> l = replier(f, s, w);
        while (l.size() * 9 * k > maxH && k > MIN) {
            k = Math.max(MIN, k - 0.1F);
            l = replier(f, s, (int) (w / k));
        }
        int max = Math.max(1, (int) (maxH / (9 * k)));
        if (l.size() > max) {
            List<String> c = new ArrayList<>(l.subList(0, max));
            c.set(max - 1, couper(f, c.get(max - 1) + " " + l.get(max), (int) (w / k)));
            l = c;
        }
        g.pose().pushMatrix();
        g.pose().translate(x, y);
        g.pose().scale(k, k);
        for (int i = 0; i < l.size(); i++) {
            g.text(f, l.get(i), 0, i * 9, couleur, ombre);
        }
        g.pose().popMatrix();
        return (int) Math.ceil(l.size() * 9 * k);
    }

    /** Haut du cadre : centré, mais jamais sous le bord de l'écran (l'ornement du titre dépasse de 12 px). */
    public static int haut(int hauteurEcran, int ph) {
        return Math.max(13, (hauteurEcran - ph) / 2 + 4);
    }
}
