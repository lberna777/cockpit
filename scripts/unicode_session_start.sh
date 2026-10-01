#!/usr/bin/env bash
# SessionStart di cockpit per lo studio: porta qui gli automatismi di UniCode.
#
# Perché esiste (2026-10-01, decisione di Lorenzo): cockpit è la cartella sempre aggiornata e
# contiene UniCode, quindi le sessioni di studio possono partire anche da qui — in locale e,
# soprattutto, nel cloud, dove si clona il repo cockpit e ~/UniCode non esiste.
#
# Ordine, e per questo un solo script invece di due hook paralleli:
#   1. solo nel cloud: scripts/cloud_bootstrap.sh (symlink, lavoro cloud non unito, consolidamento
#      arretrato). Deve finire PRIMA del briefing, altrimenti il briefing legge un tracker vecchio.
#   2. sempre: lo stesso session_start.sh di UniCode (rigenera e inietta stato/briefing.md).
#      Il suo stdout è JSON: niente deve scrivere su stdout prima di lui.

set -uo pipefail

PAYLOAD="$(cat 2>/dev/null || true)"   # consuma stdin, lo ripassa allo script di UniCode

COCKPIT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
export TZ="${TZ:-Europe/Rome}"

if [ "${CLAUDE_CODE_REMOTE:-}" != "true" ]; then
  printf '%s' "$PAYLOAD" | bash "$COCKPIT/Vault/UniCode/scripts/session_start.sh"
  exit 0
fi

bash "$COCKPIT/scripts/cloud_bootstrap.sh" >/dev/null 2>&1 || true

# Nel cloud: in testa al briefing, gli avvisi del bootstrap e il promemoria sui limiti.
JSON="$(printf '%s' "$PAYLOAD" | bash "$COCKPIT/Vault/UniCode/scripts/session_start.sh")"
JSON="$JSON" AVVISI="$COCKPIT/Vault/UniCode/stato/cloud_avvisi.md" python3 <<'PY'
import json, os

try:
    ctx = json.loads(os.environ["JSON"])["hookSpecificOutput"]["additionalContext"]
except Exception:
    ctx = ""

try:
    with open(os.environ["AVVISI"], encoding="utf-8") as fh:
        avvisi = fh.read().strip()
except OSError:
    avvisi = ""

testa = (
    "## Sessione di studio nel cloud\n\n"
    "Radice di UniCode: `Vault/UniCode` (anche `~/UniCode`). Il lavoro sul Vault viene "
    "committato e inviato da solo dopo ogni risposta, sul ramo claude/* di questa sessione: "
    "arriva su master — e quindi sul laptop — solo dopo il merge della PR. Eclipse non c'è: "
    "i progetti si compilano qui con javac (JDK 21), Lorenzo li importa in locale.\n\n"
    "**A ogni `/chiudi` nel cloud** (autorizzazione di Lorenzo del 2026-10-01): dopo il commit, "
    "apri la PR dal ramo di sessione verso master e uniscila tu (squash). **Rischio di conflitto**: "
    "se il laptop ha consolidato la stessa giornata col timer serale senza inviarla, master e il "
    "ramo divergono su `log/giornate.md`, `stato/tracker.md` e `log/giornate_dettaglio/`. Prima del "
    "merge controlla che la PR sia mergeable; in conflitto su quei file tieni la versione del ramo "
    "cloud se il contenuto coincide, altrimenti fermati e chiedi a Lorenzo. Ricordaglielo anche "
    "a voce in chiusura.\n"
)
if avvisi:
    testa += "\n**Avvisi dall'avvio**:\n" + avvisi + "\n"

print(json.dumps({
    "hookSpecificOutput": {
        "hookEventName": "SessionStart",
        "additionalContext": testa + "\n" + ctx,
    }
}))
PY
