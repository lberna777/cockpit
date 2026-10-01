#!/usr/bin/env bash
# Salvataggio automatico nel cloud: commit e push del Vault sul ramo di sessione.
#
# Il container è effimero: ciò che non è su GitHub si perde quando viene riciclato, e non è
# garantito che SessionEnd arrivi (il container può essere chiuso per inattività). Per questo
# gira su Stop — dopo ogni risposta — oltre che su SessionEnd. Se non c'è nulla di nuovo non fa
# nulla; i commit intermedi spariscono con lo squash della PR verso master.
# Nel locale non fa nulla: lì si committa come sempre, a mano o da /chiudi.

set -uo pipefail
cat >/dev/null 2>&1 || true

[ "${CLAUDE_CODE_REMOTE:-}" = "true" ] || exit 0

COCKPIT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$COCKPIT" || exit 0
export TZ="${TZ:-Europe/Rome}"

RAMO="$(git rev-parse --abbrev-ref HEAD 2>/dev/null)"
case "$RAMO" in claude/*) ;; *) exit 0 ;; esac   # mai su master o su rami altrui

if [ -n "$(git status --porcelain -- Vault 2>/dev/null)" ]; then
  git add -A -- Vault >/dev/null 2>&1
  git commit -q -m "UniCode (cloud): salvataggio automatico $(date '+%Y-%m-%d %H:%M')" >/dev/null 2>&1 || true
fi

# Push anche dei commit fatti a mano e non ancora inviati.
if [ -n "$(git log --oneline "origin/$RAMO..HEAD" 2>/dev/null || echo nuovo)" ]; then
  for attesa in 2 4 8; do
    timeout 30 git push -q -u origin "$RAMO" >/dev/null 2>&1 && break
    sleep "$attesa"
  done
fi

exit 0
