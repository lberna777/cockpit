#!/usr/bin/env bash
# Memoria notturna nel cloud: consolidamento, recap e indice anche a laptop spento.
#
# Lo lancia l'attività programmata «Memoria notturna» (23:50, sessione cloud nuova), dalla
# radice di un clone di cockpit con permesso di push. Richiesta di Lorenzo del 2026-10-22: il
# timer delle 23 del laptop (giornata_laptop.sh) non gira se il portatile è spento.
#
#   1. pull di master;
#   2. giornata.py: chiude la giornata di oggi se il laptop non l'ha già fatto (dalle 22:00);
#   3. clone senza file (--filter=blob:none) delle repo non archiviate di lberna777, così il recap
#      vede i loro commit: quelle che non si riescono a leggere si saltano e si elencano;
#   4. recap di oggi e dei 7 giorni prima, indice del Vault;
#   5. commit e push su master; con marcatori di conflitto o push rifiutato si ferma.
#
# Due scrittori, il laptop alle 23 e questo alle 23:50: entrambi fanno pull prima, e un recap già
# presente non si riscrive. Uscita: righe «ok · …» o «saltata · …» da riportare nella risposta.
set -uo pipefail
export TZ=Europe/Rome
COCKPIT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$COCKPIT" || exit 1
UNICODE="$COCKPIT/Vault/UniCode"
# Repo non archiviate con commit da riportare (mappa del CLAUDE.md di cockpit).
REPO=(Developing plugin-creator carguy bibiciclo barca-halloween lberna777.github.io lberna777 claudereset
      Boot_Debian diritto-quiz-app StereoCompressor NEMO-StereoCompressor FreakFM acidmoog-synth)
CLONI="$(mktemp -d)"
trap 'rm -rf "$CLONI"' EXIT

git config user.name >/dev/null 2>&1 || git config user.name "Claude"
git config user.email >/dev/null 2>&1 || git config user.email "noreply@anthropic.com"
git config core.hooksPath .githooks

git checkout -q master 2>/dev/null
if ! git pull -q --no-rebase --no-edit origin master; then
  git merge --abort 2>/dev/null
  echo "errore · pull di master non riuscito: niente fatto"; exit 1
fi

UNICODE_ROOT="$UNICODE" python3 "$UNICODE/scripts/giornata.py" 2>&1 | tail -1 | sed 's/^/ok · /'

PERCORSI=""
for r in "${REPO[@]}"; do
  if timeout 60 git clone -q --bare --filter=blob:none "https://github.com/lberna777/$r" "$CLONI/$r" 2>/dev/null; then
    PERCORSI="$PERCORSI:$CLONI/$r"
  else
    echo "saltata · $r (non leggibile da questa sessione)"
  fi
done
RECAP_REPOS="${PERCORSI#:}" python3 scripts/recap_generator.py | sed 's/^/ok · /'
RECAP_REPOS="${PERCORSI#:}" python3 scripts/recap_generator.py --backfill 7 | head -1 | sed 's/^/ok · /'
python3 scripts/build_index.py 2>&1 | tail -1 | sed 's/^/ok · /'

git add -- Vault/recap Vault/index.md Vault/UniCode/stato Vault/UniCode/log
if git diff --cached --quiet; then
  echo "ok · niente da committare"; exit 0
fi
if ! git commit -q -m "Memoria notturna $(date +%F): consolidamento, recap e indice"; then
  echo "errore · commit rifiutato (marcatori di conflitto?): niente inviato"; exit 1
fi
for attesa in 2 4 8; do
  timeout 30 git push -q origin HEAD:master && { echo "ok · inviato su master"; exit 0; }
  sleep "$attesa"
done
echo "errore · push su master non riuscito"; exit 1
