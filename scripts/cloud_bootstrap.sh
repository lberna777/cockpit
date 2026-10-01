#!/usr/bin/env bash
# Preparazione del container cloud, prima del briefing. Nel locale non fa nulla.
#
# Il container clona cockpit da zero a ogni sessione: mancano i symlink del laptop, il timer
# serale (unicode-giornata.timer) e il lavoro delle sessioni cloud precedenti, che vive su rami
# claude/* finché non viene unito in master. Questo script ricostruisce ciò che si può:
#
#   1. ~/cockpit e ~/UniCode come symlink al clone, perché comandi e script li citano;
#   2. rami claude/* più recenti di HEAD e non ancora uniti → merge nel ramo di sessione, così
#      una sessione cloud riparte da dove si è fermata la precedente; in conflitto, merge
#      annullato e avviso nel briefing (stato/cloud_avvisi.md);
#   3. consolidamento arretrato di stato/giornata.md (giornata.py senza --force: chiude solo
#      giorni passati, mai quello in corso).
#
# Gli avvisi finiscono in Vault/UniCode/stato/cloud_avvisi.md, che briefing.py non conosce:
# li inietta memory_inject_cloud.sh. Il file è ignorato da git.

set -uo pipefail

[ "${CLAUDE_CODE_REMOTE:-}" = "true" ] || exit 0

COCKPIT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
UNICODE="$COCKPIT/Vault/UniCode"
AVVISI="$UNICODE/stato/cloud_avvisi.md"
export TZ="${TZ:-Europe/Rome}"

: >"$AVVISI"
avviso() { printf -- '- %s\n' "$1" >>"$AVVISI"; }

# --- 1. symlink --------------------------------------------------------------
[ -e "$HOME/cockpit" ] || ln -s "$COCKPIT" "$HOME/cockpit"
[ -e "$HOME/UniCode" ] || ln -s "$UNICODE" "$HOME/UniCode"

# --- 2. lavoro cloud non ancora in master -----------------------------------
cd "$COCKPIT" || exit 0
git config user.name >/dev/null 2>&1 || git config user.name "Claude"
git config user.email >/dev/null 2>&1 || git config user.email "noreply@anthropic.com"

if timeout 15 git fetch -q origin 2>/dev/null; then
  HEAD_TS="$(git log -1 --format=%ct HEAD)"
  ATTUALE="$(git rev-parse --abbrev-ref HEAD)"
  for ref in $(git for-each-ref --format='%(refname:short)' 'refs/remotes/origin/claude/'); do
    [ "$ref" = "origin/$ATTUALE" ] && continue
    git merge-base --is-ancestor "$ref" HEAD 2>/dev/null && continue
    # Solo rami più recenti di HEAD: uno più vecchio e mai unito è superato, non da riprendere.
    [ "$(git log -1 --format=%ct "$ref")" -gt "$HEAD_TS" ] || continue
    # Solo rami che toccano lo studio.
    git diff --quiet "$(git merge-base HEAD "$ref")" "$ref" -- Vault/UniCode 2>/dev/null && continue
    if git merge -q --no-edit "$ref" >/dev/null 2>&1; then
      avviso "Unito \`$ref\` (sessione cloud precedente non ancora in master)."
    else
      git merge --abort >/dev/null 2>&1 || true
      avviso "\`$ref\` ha lavoro di studio non in master e va in conflitto: unirlo a mano prima di proseguire."
    fi
  done
else
  avviso "git fetch fallito: non verificato se esiste lavoro cloud non unito."
fi

# --- 3. consolidamento arretrato --------------------------------------------
if [ -f "$UNICODE/scripts/giornata.py" ]; then
  OUT="$(UNICODE_ROOT="$UNICODE" python3 "$UNICODE/scripts/giornata.py" 2>&1 | tail -1)"
  case "$OUT" in
    giornata\ ????-??-??:*) avviso "Consolidamento arretrato eseguito: $OUT" ;;
  esac
fi

exit 0
