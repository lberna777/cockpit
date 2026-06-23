#!/usr/bin/env bash
# memory_inject.sh — artefatto compatto iniettato in contesto dal SessionStart hook.
# Stampa su stdout: l'indice del vault (troncato) + gli ultimi N recap.
# NON inietta il grafo intero (sarebbe pesantissimo in token).
set -euo pipefail

VAULT="$HOME/cockpit/Vault"
INDEX="$VAULT/index.md"
RECAP_DIR="$VAULT/recap"
N_RECAPS=3
INDEX_MAX_LINES=200

# Genera i recap mancanti degli ultimi 7 giorni prima di iniettare
python3 "$HOME/cockpit/scripts/recap_generator.py" --backfill 7 >/dev/null 2>&1 || true

echo "=== MEMORIA PERSISTENTE (cockpit) ==="
echo "Vault: $VAULT — ricerca con 'rg' nel vault. Note curate in claude/."
echo ""

if [[ -f "$INDEX" ]]; then
  echo "--- Vault index (troncato a ${INDEX_MAX_LINES} righe) ---"
  head -n "$INDEX_MAX_LINES" "$INDEX"
  total=$(wc -l < "$INDEX")
  if (( total > INDEX_MAX_LINES )); then
    echo "... (index.md ha $total righe; apri $INDEX per il resto)"
  fi
else
  echo "(index.md assente — esegui scripts/build_index.py)"
fi

echo ""
echo "--- Ultimi $N_RECAPS recap ---"
if [[ -d "$RECAP_DIR" ]]; then
  mapfile -t recaps < <(find "$RECAP_DIR" -maxdepth 1 -name '20*.md' | sort -r | head -n "$N_RECAPS")
  if (( ${#recaps[@]} == 0 )); then
    echo "(nessun recap ancora)"
  else
    for r in "${recaps[@]}"; do
      echo ""
      echo "### $(basename "$r" .md)"
      cat "$r"
    done
  fi
else
  echo "(cartella recap/ assente)"
fi
echo ""
echo "=== fine memoria ==="
