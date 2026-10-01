#!/usr/bin/env bash
# SessionEnd di cockpit: traccia di studio di UniCode, poi salvataggio cloud.
#
# Da cockpit partono anche sessioni di codice. La traccia di UniCode (log/AAAA-MM.md e la riga
# «sessione aperta» in stato/giornata.md) si scrive solo se la sessione ha toccato lo studio:
# file modificati sotto Vault/UniCode, oppure eventi annotati oggi nel buffer della giornata.
# Altrimenti una sessione su agenticdash risulterebbe una giornata di studio.

set -uo pipefail

PAYLOAD="$(cat 2>/dev/null || true)"
COCKPIT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
UNICODE="$COCKPIT/Vault/UniCode"
export TZ="${TZ:-Europe/Rome}"

STUDIO=""
[ -n "$(git -C "$COCKPIT" status --porcelain -- Vault/UniCode 2>/dev/null)" ] && STUDIO=1
grep -q '^[0-9][0-9]:' "$UNICODE/stato/giornata.md" 2>/dev/null && STUDIO=1
# Nel cloud i cambiamenti sono già committati dall'autosave su Stop: conta il ramo di sessione.
if [ "${CLAUDE_CODE_REMOTE:-}" = "true" ] && \
   ! git -C "$COCKPIT" diff --quiet origin/master HEAD -- Vault/UniCode 2>/dev/null; then
  STUDIO=1
fi

if [ -n "$STUDIO" ]; then
  printf '%s' "$PAYLOAD" | bash "$UNICODE/scripts/session_end.sh"
fi

bash "$COCKPIT/scripts/cloud_autosave.sh" </dev/null
exit 0
