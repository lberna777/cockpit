#!/usr/bin/env bash
# Allinea alle versioni su GitHub tutte le repo di lberna777 clonate su questa macchina.
# Uso: ~/cockpit/scripts/allinea_repo.sh [cartella di partenza, default ~]
#
# Sicuro: aggiorna solo con avanzamento semplice (fast-forward). Una repo con file modificati e non
# salvati, commit non inviati o rami divergenti NON viene toccata: compare nell'elenco finale
# con il motivo, e la si sistema a mano (o con Claude). Le repo cancellate su GitHub vengono
# solo segnalate.
set -uo pipefail

RADICE="${1:-$HOME}"
ok=(); fermi=()

while IFS= read -r gitdir; do
  repo="$(dirname "$gitdir")"
  url="$(git -C "$repo" remote get-url origin 2>/dev/null || true)"
  case "$url" in *lberna777/*) ;; *) continue ;; esac
  nome="${repo/#"$HOME"/\~}"

  if ! git -C "$repo" fetch -q origin 2>/dev/null; then
    fermi+=("$nome: non raggiungibile su GitHub (cancellata o senza accesso)"); continue
  fi
  if [ -n "$(git -C "$repo" status --porcelain --untracked-files=no)" ]; then
    fermi+=("$nome: modifiche non salvate in un commit"); continue
  fi
  # I file non tracciati non bloccano un avanzamento semplice: si segnalano soltanto.
  nuovi="$(git -C "$repo" status --porcelain | grep -c '^??' || true)"
  [ "$nuovi" -gt 0 ] && fermi+=("$nome: $nuovi file non tracciati (aggiornata lo stesso, decidi tu se tenerli)")
  ramo="$(git -C "$repo" symbolic-ref --short -q HEAD || true)"
  if [ -z "$ramo" ] || ! git -C "$repo" rev-parse -q --verify "origin/$ramo" >/dev/null; then
    fermi+=("$nome: ramo '${ramo:-nessuno}' senza corrispondente su GitHub"); continue
  fi
  if git -C "$repo" merge -q --ff-only "origin/$ramo" 2>/dev/null; then
    ok+=("$nome ($ramo)")
  else
    avanti="$(git -C "$repo" rev-list --count "origin/$ramo..HEAD")"
    if [ "$avanti" -gt 0 ]; then
      fermi+=("$nome: $avanti commit locali non inviati, rami divergenti")
    else
      fermi+=("$nome: aggiornamento bloccato da file locali che GitHub sovrascriverebbe")
    fi
  fi
done < <(find "$RADICE" -maxdepth 5 -name .git -type d \
           -not -path '*/node_modules/*' -not -path '*/.cache/*' 2>/dev/null | sort)

echo "Aggiornate (${#ok[@]}):"; printf '  ✓ %s\n' "${ok[@]}"
if [ ${#fermi[@]} -gt 0 ]; then
  echo "Da guardare (${#fermi[@]}):"; printf '  ! %s\n' "${fermi[@]}"
fi
