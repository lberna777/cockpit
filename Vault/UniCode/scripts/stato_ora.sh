#!/usr/bin/env bash
# Consolidamento su richiesta, a giornata ancora aperta.
#
# Perché esiste (2026-09-21, su richiesta di Lorenzo). `giornata.py` avanza il tracker alle
# 23:00 leggendo i marcatori CHIUSO / RIPASSO da stato/giornata.md. Chiedere «com'è lo stato
# di FI2?» a metà giornata mostrava quindi un tracker vecchio: il ripasso era fatto, la
# scadenza no. Questo script fa avanzare il tracker subito, senza toccare il timer serale.
#
# Cosa fa `giornata.py --force`, e perché da solo non basta:
#   - applica i marcatori al tracker, rigenera il briefing, archivia il buffer in
#     log/giornate_dettaglio/ (in APPEND: niente va perso) e lo azzera. Fin qui è ciò che
#     serve, ed è già idempotente — log/giornate.md non duplica il giorno, e i marcatori
#     consumati escono dal buffer, quindi il consolidamento delle 23 non li riapplica.
#   - MA riapre il buffer intestato a DOMANI, perché assume di essere il consolidamento
#     serale. A giornata aperta è sbagliato: i fatti del pomeriggio finirebbero sotto la
#     data di domani, e il timer delle 23 troverebbe un buffer futuro da consolidare.
# Questo script ripristina l'intestazione a oggi. È l'unica differenza.
#
# Uso:  bash scripts/stato_ora.sh
# Il timer systemd (unicode-giornata.timer, 23:00) resta invariato e gira comunque.

set -euo pipefail

ROOT="${UNICODE_ROOT:-$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)}"
export UNICODE_ROOT="$ROOT"

BUFFER="$ROOT/stato/giornata.md"
OGGI="$(date +%F)"
ORA="$(date +%-H)"

python3 "$ROOT/scripts/giornata.py" --force

# Dopo le 22 il consolidamento serale è legittimo: il buffer deve restare intestato a
# domani, e non lo tocchiamo. Prima, la giornata è ancora in corso.
if [ "$ORA" -lt 22 ] && [ -f "$BUFFER" ]; then
  if head -1 "$BUFFER" | grep -q '^# Giornata ' && ! head -1 "$BUFFER" | grep -q "$OGGI"; then
    sed -i "1s/^# Giornata .*/# Giornata $OGGI/" "$BUFFER"
    echo "buffer riaperto su $OGGI (la giornata è ancora in corso)" >&2
  fi
fi
