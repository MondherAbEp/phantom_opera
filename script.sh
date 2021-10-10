#!/bin/sh

MAX=100

I=0
COUNT=0
TESTVAR=0

runLolemoFantom() {
  python3 server.py &
  sleep 0.2 && python3 random_inspector.py &
  sleep 0.2 && python3 lolemo_fantom.py
}

runLolemoInspector() {
  python3 server.py &
  sleep 0.2 && python3 lolemo_inspector.py &
  sleep 0.2 && python3 random_fantom.py
}

runLolemoInspectorAndFantom() {
  python3 server.py &
  sleep 0.2 && python3 lolemo_inspector.py &
  sleep 0.2 && python3 lolemo_fantom.py
}

rm logs/game.log 2>/dev/null

while [ $I -le $MAX ]; do
  runLolemoInspectorAndFantom
  I=$(($I + 1))
done

COUNT=$(grep -o -i "fantom wins" logs/game.log | wc -l)

echo $COUNT

echo "Victoire du fantome: ${COUNT}"

INSPECTOR_WINS=$(grep -o -i "inspector wins" logs/game.log | wc -l)

echo "Victoire de l'inspecteur:" $INSPECTOR_WINS
