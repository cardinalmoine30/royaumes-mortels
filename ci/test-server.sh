#!/usr/bin/env bash
# Lance un vrai serveur NeoForge 26.3 avec le mod, exécute les commandes de ci/commandes.txt,
# puis s'arrête. Les journaux vont dans ci-out/.
set -uo pipefail

RACINE="$(pwd)"
SORTIE="$RACINE/ci-out"
mkdir -p "$SORTIE"
VER=$(grep '^neo_version=' gradle.properties | cut -d= -f2)

mkdir -p srv && cd srv
curl -fsSL -o installer.jar "https://maven.neoforged.net/releases/net/neoforged/neoforge/$VER/neoforge-$VER-installer.jar"
java -jar installer.jar --install-server . > "$SORTIE/installation.log" 2>&1 || { echo "Echec installation NeoForge"; exit 1; }

echo "eula=true" > eula.txt
cat > server.properties <<EOF
online-mode=false
level-seed=sigmar
spawn-protection=0
view-distance=6
simulation-distance=6
pause-when-empty-seconds=-1
EOF
echo "-Xmx4G" > user_jvm_args.txt

mkdir -p mods
find "$RACINE/build/libs" -name 'royaumes-*.jar' ! -name '*-sources.jar' -exec cp {} mods/ \;
ls mods

mkfifo entree
exec 3<>entree
./run.sh nogui < entree > "$SORTIE/console.log" 2>&1 &
PID=$!

PRET=0
for i in $(seq 1 900); do
  if grep -q 'Done (' "$SORTIE/console.log" 2>/dev/null; then PRET=1; break; fi
  if ! kill -0 $PID 2>/dev/null; then break; fi
  sleep 1
done

if [ "$PRET" = "1" ]; then
  echo "Serveur prêt, exécution des commandes de test"
  while IFS= read -r cmd || [ -n "$cmd" ]; do
    case "$cmd" in ''|\#*) continue;; esac
    case "$cmd" in
      attendre*) sleep "${cmd#attendre }";;
      *) echo "$cmd" >&3; sleep 2;;
    esac
  done < "$RACINE/ci/commandes.txt"
  echo "stop" >&3
fi

for i in $(seq 1 180); do kill -0 $PID 2>/dev/null || break; sleep 1; done
kill -9 $PID 2>/dev/null || true

cp logs/latest.log "$SORTIE/latest.log" 2>/dev/null || true
cp -r crash-reports "$SORTIE/" 2>/dev/null || true

# Résumé : erreurs et avertissements importants
grep -nE 'ERROR|Exception|Caused by|Failed to|Unknown function|Couldn.t (load|parse)|Error loading|ROYAUMES_OK' "$SORTIE/console.log" > "$SORTIE/resume_erreurs.txt" || true

if [ "$PRET" != "1" ]; then echo "Le serveur n'a pas démarré"; exit 1; fi
grep -q ROYAUMES_OK "$SORTIE/console.log" || { echo "Le mod ne s'est pas chargé"; exit 1; }
echo "Serveur de test OK"
# Plantages de génération du monde ou du serveur pendant les tests
if grep -qE 'Feature order cycle|Exception generating new chunk|Considering it to be crashed' "$SORTIE/console.log" logs/latest.log 2>/dev/null; then
  echo "Le serveur a planté pendant les tests (génération du monde ?)"; exit 1
fi
grep -q 'Autel seigneurs OK' "$SORTIE/console.log" || { echo "Les commandes de test ne sont pas allées au bout"; exit 1; }
grep -q 'Forge de guerre OK' "$SORTIE/console.log" || { echo "La Forge de guerre n'est pas posée"; exit 1; }
if grep -qE 'Failed to load function|Couldn.t (load|parse)|Failed to parse|Unknown function|Error loading' "$SORTIE/console.log"; then echo "Erreur de chargement du datapack"; exit 1; fi
