#!/usr/bin/env bash
# Consolidamento serale del laptop, con git intorno. Lo lancia unicode-giornata.service alle 23.
#
# Perché esiste (2026-10-20): il timer chiamava solo giornata.py e lasciava il consolidamento
# non inviato; il cloud, il giorno dopo, consolidava la stessa giornata e al `git pull` del
# laptop i due lati divergevano su log/giornate.md, stato/giornata.md, log/giornate_dettaglio/.
#
#   1. pull (merge se i rami sono divisi; in conflitto annulla): se il cloud ha già consolidato, giornata.py lo vede e non duplica;
#      se il pull non riesce (modifiche locali in conflitto, rete), NON consolida: lo farà il
#      recupero alla prossima sessione, che giornata.py gestisce senza perdite;
#   2. giornata.py;
#   3. commit dei soli file del consolidamento e push su master.
set -u
UNICODE="$(cd "$(dirname "$0")/.." && pwd)"
REPO="$(git -C "$UNICODE" rev-parse --show-toplevel)"
cd "$REPO" || exit 1
REL="${UNICODE#"$REPO"/}"

# Traccia di fine sessione rimasta non committata (2026-10-22): bloccava il pull («Le tue modifiche
# locali… sarebbero sovrascritte»). Se log/AAAA-MM.md o stato/giornata.md sono modificati, si
# committano prima del pull; durante un merge o con marcatori di conflitto no.
salva_traccia() {
  local f traccia=()
  for f in "$REL/log/$(date +%Y-%m).md" "$REL/stato/giornata.md"; do
    [ -n "$(git status --porcelain -- "$f")" ] && traccia+=("$f")
  done
  [ ${#traccia[@]} -eq 0 ] && return 0
  [ -f "$(git rev-parse --absolute-git-dir)/MERGE_HEAD" ] && return 0
  grep -qE '^(<<<<<<<|>>>>>>>)( |$)' "${traccia[@]}" && {
    echo "$1: marcatori di conflitto in ${traccia[*]}, traccia non committata" >&2; return 0; }
  git add -- "${traccia[@]}" && \
    git commit --quiet -m "UniCode (laptop): traccia di sessione $(date '+%F %H:%M')" -- "${traccia[@]}"
}
salva_traccia giornata_laptop

if ! git pull --no-rebase --no-edit --quiet origin master; then
  git merge --abort 2>/dev/null
  echo "giornata_laptop: pull non riuscito, consolidamento rimandato alla prossima sessione" >&2
  exit 0
fi

UNICODE_ROOT="$UNICODE" python3 "$UNICODE/scripts/giornata.py" "$@"

git add -- "$REL/stato" "$REL/log"
if ! git diff --cached --quiet; then
  git commit --quiet -m "UniCode (laptop): consolidamento serale $(date +%F)"
  git push --quiet origin HEAD:master \
    || echo "giornata_laptop: push non riuscito, il commit resta locale" >&2
fi
