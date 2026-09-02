#!/usr/bin/env bash
# SessionStart hook — inietta stato/briefing.md nel contesto della sessione.
#
# Registrato in .claude/settings.json su SessionStart (matcher: startup|resume|clear).
# Riceve JSON su stdin; non lo usa, ma lo consuma per non lasciare la pipe aperta.
#
# Il briefing viene rigenerato qui prima dell'iniezione: se il cron serale non è
# girato (macchina spenta, sospensione), la sessione parte comunque da dati freschi.

set -uo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT="$(python3 "$HERE/paths.py" 2>/dev/null || echo "${UNICODE_ROOT:-$HOME/UniCode}")"
BRIEFING="$ROOT/stato/briefing.md"

cat >/dev/null 2>&1 || true   # consuma stdin

# Rigenerazione best-effort: un fallimento qui non deve impedire l'avvio.
if [ -f "$ROOT/scripts/briefing.py" ]; then
  UNICODE_ROOT="$ROOT" python3 "$ROOT/scripts/briefing.py" >/dev/null 2>&1 || true
fi

if [ ! -f "$BRIEFING" ]; then
  exit 0   # nessun briefing: la sessione parte senza contesto iniettato
fi

UNICODE_BRIEFING_FILE="$BRIEFING" python3 <<'PY'
import json, os, sys

path = os.environ["UNICODE_BRIEFING_FILE"]
try:
    with open(path, encoding="utf-8") as fh:
        content = fh.read()
except OSError:
    sys.exit(0)

# Tetto di sicurezza: il briefing non deve mai diventare un costo imprevisto.
LIMIT = 12000
if len(content) > LIMIT:
    content = content[:LIMIT].rstrip() + "\n\n_(briefing troncato al limite di sicurezza)_"

print(json.dumps({
    "hookSpecificOutput": {
        "hookEventName": "SessionStart",
        "additionalContext": content,
    }
}))
PY
