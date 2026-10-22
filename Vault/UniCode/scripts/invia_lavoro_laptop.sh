#!/usr/bin/env bash
# Invio automatico del codice di Lorenzo dal laptop. Lo lancia unicode-invia.timer ogni 5 minuti.
#
# Perché esiste (2026-10-20, richiesta di Lorenzo): i LAB di FI2 si svolgono dentro la repo
# (esame_FI2/da_importare/…) e Claude, nel cloud, li legge solo da GitHub. Lorenzo non vuole
# ricordarsi di fare commit: ci pensa questo script.
#
# Tocca solo corsi/*/esame_*/ (il codice svolto) e, prima del pull, la traccia di fine sessione
# (salva_traccia); il resto di stato/ e log/ resta al consolidamento serale (giornata_laptop.sh). Se il pull non riesce (conflitto, rete, un file
# modificato in locale che il pull dovrebbe aggiornare), non invia niente e lo scrive nel journal.
set -u
UNICODE="$(cd "$(dirname "$0")/.." && pwd)"
REPO="$(git -C "$UNICODE" rev-parse --show-toplevel)"
cd "$REPO" || exit 1
REL="${UNICODE#"$REPO"/}"

shopt -s nullglob
CARTELLE=("$REL"/corsi/*/esame_*)
[ ${#CARTELLE[@]} -eq 0 ] && exit 0

# niente da inviare: esce senza toccare la rete
[ -z "$(git status --porcelain -- "${CARTELLE[@]}")" ] && exit 0

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
salva_traccia invia_lavoro

# merge, non solo fast-forward: se il laptop ha un commit locale non inviato i rami si dividono,
# e con --ff-only lo script si fermava. In conflitto: annulla ed esce.
if ! git pull --no-rebase --no-edit --quiet origin master; then
  git merge --abort 2>/dev/null
  echo "invia_lavoro: pull non riuscito (conflitto o rete), niente inviato" >&2
  exit 0
fi
git add -A -- "${CARTELLE[@]}"
git diff --cached --quiet && exit 0
git commit --quiet -m "UniCode (laptop): lavoro in corso $(date '+%F %H:%M')"
git push --quiet origin HEAD:master || echo "invia_lavoro: push non riuscito, il commit resta locale" >&2
