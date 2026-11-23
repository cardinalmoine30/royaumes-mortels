#!/bin/bash
# Exporte les signatures des classes listées dans ci/api.txt (aide au développement hors ligne).
CP=$(./gradlew -q imprimerClasspath 2>/dev/null | grep '^CLASSPATH=' | cut -d= -f2-)
OUT=ci-out/api.txt
: > "$OUT"
while read -r cls; do
  [ -z "$cls" ] && continue
  echo "=================== $cls" >> "$OUT"
  javap -protected -cp "$CP" "$cls" >> "$OUT" 2>&1 || echo "(introuvable)" >> "$OUT"
done < ci/api.txt
# Recherche de classes par nom (paquets déplacés dans 26.x)
for f in $(echo "$CP" | tr ':' '\n' | grep -E 'neoforge|minecraft' ); do
  unzip -l "$f" 2>/dev/null | grep -oE '[a-z/]+/(GuiGraphics[A-Za-z]*|AbstractHorse|InventoryScreen|RenderPipelines|PlayerRideableJumping)\.class' ;
done | sort -u > ci-out/classes_trouvees.txt
ls -la "$OUT"
