#!/usr/bin/env bash
# SessionEnd hook — registra la traccia meccanica della sessione e rigenera il briefing.
#
# Registrato in .claude/settings.json su SessionEnd.
# Non produce interpretazione: quella resta a /chiudi. Qui si registra ciò che è
# deducibile senza giudizio, perché avvenga sempre — anche quando /chiudi non viene eseguito.

set -uo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT="$(python3 "$HERE/paths.py" 2>/dev/null || echo "${UNICODE_ROOT:-$HOME/UniCode}")"
LOGDIR="$ROOT/log"
GIORNATA="$ROOT/stato/giornata.md"
STAMP="$(date +%Y-%m-%d)"
LOGFILE="$LOGDIR/$(date +%Y-%m).md"

mkdir -p "$LOGDIR" "$ROOT/stato"

PAYLOAD="$(cat 2>/dev/null || true)"

# --- estrazione dei campi dal JSON dell'hook -------------------------------
SESSION_ID="$(printf '%s' "$PAYLOAD" | python3 -c '
import json,sys
try: print(json.load(sys.stdin).get("session_id","")[:8])
except Exception: print("")
' 2>/dev/null)"

REASON="$(printf '%s' "$PAYLOAD" | python3 -c '
import json,sys
try:
    d=json.load(sys.stdin)
    print(d.get("reason") or d.get("matcher") or "other")
except Exception: print("other")
' 2>/dev/null)"

# --- file toccati nell'albero UniCode --------------------------------------
join_lines() { paste -sd ',' - | sed 's/,/, /g'; }

TOCCATI=""
if command -v git >/dev/null 2>&1 && git -C "$ROOT" rev-parse --git-dir >/dev/null 2>&1; then
  TOCCATI="$(git -C "$ROOT" status --porcelain 2>/dev/null | awk '{print $NF}' | head -12 | join_lines)"
fi
if [ -z "$TOCCATI" ]; then
  # Fallback senza git: solo il materiale di studio, non lo scaffolding.
  TOCCATI="$(find "$ROOT/corsi" "$ROOT/profilo" "$ROOT/plans" -type f -newermt '6 hours ago' \
      -not -path '*/.git/*' 2>/dev/null | sed "s|^$ROOT/||" | head -12 | join_lines)"
fi
[ -z "$TOCCATI" ] && TOCCATI="nessuna modifica su file"

# --- codici corso citati nel buffer di giornata ----------------------------
# I codici vengono da piano/codici.txt tramite paths.py: rinominare o aggiungere un corso
# non deve richiedere di toccare questo script.
CODICI_RE="$(python3 "$HERE/paths.py" codici 2>/dev/null)"
[ -z "$CODICI_RE" ] && CODICI_RE='FI2|CALC|MATAP|LAS|SO|IDS|TLC|ELT|CA|RETI|WEB|ELN'

CODICI=""
if [ -f "$GIORNATA" ]; then
  CODICI="$(grep -oE "\\b($CODICI_RE)\\b" "$GIORNATA" 2>/dev/null | sort -u | join_lines)"
fi
[ -z "$CODICI" ] && CODICI="—"

# grep -c stampa 0 ed esce 1 quando non trova nulla: senza `head -1` il fallback
# accodava una seconda riga e il confronto numerico più sotto falliva.
RIGHE_OGGI=0
if [ -f "$GIORNATA" ]; then
  RIGHE_OGGI="$(grep -c '^[0-9][0-9]:' "$GIORNATA" 2>/dev/null | head -1)"
  RIGHE_OGGI="${RIGHE_OGGI:-0}"
fi

# --- scrittura append-only --------------------------------------------------
if [ ! -f "$LOGFILE" ]; then
  printf '# Log sessioni — %s\n\n' "$(date +%Y-%m)" >"$LOGFILE"
fi

{
  printf -- '- **%s %s** · sessione `%s` (%s)\n' "$STAMP" "$(date +%H:%M)" "${SESSION_ID:-????}" "$REASON"
  printf -- '  - corsi toccati: %s · eventi registrati oggi: %s\n' "$CODICI" "$RIGHE_OGGI"
  printf -- '  - file: %s\n' "$TOCCATI"
} >>"$LOGFILE"

# Marcatore per il consolidamento serale: la giornata ha visto attività reale.
if [ -f "$GIORNATA" ] && [ "$RIGHE_OGGI" -eq 0 ]; then
  printf '%s · sessione aperta, nessun evento di merito registrato\n' "$(date +%H:%M)" >>"$GIORNATA"
fi

# --- commit della traccia, solo sul laptop -----------------------------------
# Perché (2026-10-22): la traccia restava modificata in locale e il `git pull` dei timer
# (invia_lavoro_laptop.sh, giornata_laptop.sh) si rifiutava di aggiornare log/AAAA-MM.md: dal
# 21 al 22/10 il codice del LAB06 non è arrivato su GitHub. Si committano solo i due file scritti
# qui, senza push (lo fanno i timer). Nel cloud ci pensa cloud_autosave.sh. Durante un merge
# o con marcatori di conflitto non si committa niente.
if [ "${CLAUDE_CODE_REMOTE:-}" != "true" ] && git -C "$ROOT" rev-parse --git-dir >/dev/null 2>&1; then
  GITDIR="$(git -C "$ROOT" rev-parse --absolute-git-dir)"
  TRACCIA=("$LOGFILE")
  [ -f "$GIORNATA" ] && TRACCIA+=("$GIORNATA")
  if [ ! -f "$GITDIR/MERGE_HEAD" ] && \
     ! grep -qE '^(<<<<<<<|>>>>>>>)( |$)' "${TRACCIA[@]}" 2>/dev/null; then
    git -C "$ROOT" add -- "${TRACCIA[@]}" >/dev/null 2>&1 && \
    git -C "$ROOT" commit -q -m "UniCode (laptop): traccia di sessione $STAMP $(date +%H:%M)" \
      -- "${TRACCIA[@]}" >/dev/null 2>&1 || true
  fi
fi

# --- briefing aggiornato per la prossima sessione ---------------------------
[ -f "$ROOT/scripts/briefing.py" ] && \
  UNICODE_ROOT="$ROOT" python3 "$ROOT/scripts/briefing.py" >/dev/null 2>&1 || true

exit 0
