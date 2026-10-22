#!/usr/bin/env bash
# Invio automatico del codice di Lorenzo dal laptop. Lo lancia unicode-invia.timer ogni 5 minuti.
#
# Perché esiste (2026-10-20, richiesta di Lorenzo): i LAB di FI2 si svolgono dentro la repo
# (esame_FI2/da_importare/…) e Claude, nel cloud, li legge solo da GitHub. Lorenzo non vuole
# ricordarsi di fare commit: ci pensa questo script.
#
# Tocca solo corsi/*/esame_*/ (il codice svolto): niente stato/, log/ né altro, che restano al
# consolidamento serale (giornata_laptop.sh). Se il pull non è un fast-forward, non fa nulla.
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

# merge, non solo fast-forward: un commit locale non inviato (es. il recap del laptop) divide i
# rami, e con --ff-only lo script si fermava in silenzio (22/10). In conflitto: annulla ed esce.
if ! git pull --no-rebase --no-edit --quiet origin master; then
  git merge --abort 2>/dev/null
  echo "invia_lavoro: pull non riuscito (conflitto o rete), niente inviato" >&2
  exit 0
fi
git add -A -- "${CARTELLE[@]}"
git diff --cached --quiet && exit 0
git commit --quiet -m "UniCode (laptop): lavoro in corso $(date '+%F %H:%M')"
git push --quiet origin HEAD:master || echo "invia_lavoro: push non riuscito, il commit resta locale" >&2
