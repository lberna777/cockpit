#!/usr/bin/env bash
# memory_inject.sh — memoria compatta iniettata in contesto dal SessionStart hook.
#
# Rifatto il 2026-10-22 («memoria automatica piccola», decisione di Lorenzo): prima iniettava
# 200 righe di index.md e tre recap con sintesi di Ollama, circa 28 KB a ogni avvio. Ora stampa
# dove cercare, le note curate di Vault/claude/ e gli ultimi recap, che sono di poche righe.
# Non genera più i recap all'avvio: li scrive e li committa il timer serale del laptop
# (Vault/UniCode/scripts/giornata_laptop.sh), così non restano file non tracciati.
set -euo pipefail

# Percorso ricavato dallo script, non da $HOME: nel cloud il clone non sta in ~/cockpit.
COCKPIT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
VAULT="$COCKPIT/Vault"
INDEX="$VAULT/index.md"
RECAP_DIR="$VAULT/recap"
N_RECAPS=3

echo "=== MEMORIA PERSISTENTE (cockpit) ==="
echo "Vault: $VAULT — si cerca con 'rg'. Impegni e diario di tutti gli ambiti: Plancia (ArtifactData)."
if [[ -f "$INDEX" ]]; then
  echo "Indice completo delle note: $INDEX ($(sed -n 's/.* \([0-9][0-9]*\) note\..*/\1/p' "$INDEX" | head -1) note, $(sed -n '1s/.*— //p' "$INDEX")): aprirlo solo se serve."
fi

echo ""
echo "--- Note curate per Claude (Vault/claude/) ---"
for f in "$VAULT"/claude/*.md; do
  [[ -f "$f" ]] || continue
  titolo="$(grep -m1 '^# ' "$f" | sed 's/^# //')"
  echo "- claude/$(basename "$f") — ${titolo:-senza titolo}"
done

echo ""
echo "--- Ultimi $N_RECAPS recap ---"
mapfile -t recaps < <(find "$RECAP_DIR" -maxdepth 1 -name '20*.md' 2>/dev/null | sort -r | head -n "$N_RECAPS")
if (( ${#recaps[@]} == 0 )); then
  echo "(nessun recap ancora)"
fi
for r in "${recaps[@]}"; do
  echo ""
  # i recap del vecchio formato (fino al 2026-10-21) hanno una sintesi di Ollama inaffidabile:
  # se ne mostrano solo i fatti
  sed -e '/^## SINTESI/,$d' -e 's/^# Recap /### /' "$r"
done
echo ""
echo "=== fine memoria ==="
