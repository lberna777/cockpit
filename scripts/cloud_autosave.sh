#!/usr/bin/env bash
# Salvataggio automatico nel cloud: commit e push del Vault sul ramo di sessione E su master.
#
# Il container è effimero: ciò che non è su GitHub si perde quando viene riciclato, e non è
# garantito che SessionEnd arrivi (il container può essere chiuso per inattività). Per questo
# gira su Stop — dopo ogni risposta — oltre che su SessionEnd. Se non c'è nulla di nuovo non fa
# nulla.
#
# Su master, non solo sul ramo (2026-10-01, richiesta di Lorenzo): i file creati nel cloud devono
# essere sul laptop — e in Obsidian — con un `git pull`, non dopo una PR a fine sessione. Il push
# su master è solo fast-forward: se master è andato avanti (push dal laptop), prima si unisce
# origin/master nel ramo; in conflitto il merge si annulla e l'avviso compare all'utente.
# Nel locale non fa nulla: lì si committa come sempre, a mano o da /chiudi.
#
# Gira anche su PostToolUse (Bash/Write/Edit), commit e push completi: il controllo git del
# container gira su Stop in parallelo a questo script e rimanda indietro la risposta se trova
# modifiche non committate o commit non inviati. Salvare subito dopo ogni modifica lo evita.
# --solo-commit resta disponibile per fermarsi al commit locale.
#
# Merge a metà (2026-10-22): il 19, 20 e 21/10 sono finiti su master marcatori di conflitto. Il
# merge non era dell'autosave (il suo, in conflitto, si annulla): era un `git merge` o `git pull`
# andato in conflitto in sessione, o un autosave interrotto dal timeout dell'hook. Subito dopo,
# il PostToolUse faceva `git add -A` — che segna risolti i file in conflitto — e `git commit`
# chiudeva il merge con i marcatori dentro. Ora: un'esecuzione alla volta (flock); un merge
# lasciato a metà dall'autosave stesso si annulla; con file in conflitto non si salva niente e
# si avvisa; un commit con marcatori non parte (qui e nel pre-commit di .githooks/).

SOLO_COMMIT=""
[ "${1:-}" = "--solo-commit" ] && SOLO_COMMIT=1

set -uo pipefail
cat >/dev/null 2>&1 || true

[ "${CLAUDE_CODE_REMOTE:-}" = "true" ] || exit 0

COCKPIT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$COCKPIT" || exit 0
export TZ="${TZ:-Europe/Rome}"

RAMO="$(git rev-parse --abbrev-ref HEAD 2>/dev/null)"
case "$RAMO" in claude/*) ;; *) exit 0 ;; esac   # mai su master o su rami altrui

avvisa() {
  python3 -c 'import json,sys; print(json.dumps({"systemMessage": sys.argv[1]}))' "$1"
}

GITDIR="$(git rev-parse --absolute-git-dir)"
# Stop e PostToolUse possono partire insieme: uno alla volta. Chi non ottiene il turno esce,
# tanto chi lo ha salva anche le sue modifiche (o lo farà la prossima esecuzione).
exec 9>"$GITDIR/autosave.lock"
flock -w 40 9 || exit 0

# Merge di master lasciato a metà da un autosave interrotto: si annulla, è roba nostra.
SEGNO="$GITDIR/autosave-merge"
if [ -f "$SEGNO" ]; then
  [ -f "$GITDIR/MERGE_HEAD" ] && git merge --abort >/dev/null 2>&1
  rm -f "$SEGNO"
fi

# Un merge in corso con file in conflitto non è nostro: non si tocca e non si salva niente.
IN_CONFLITTO="$(git diff --name-only --diff-filter=U 2>/dev/null | paste -sd ' ' -)"
if [ -n "$IN_CONFLITTO" ]; then
  avvisa "Salvataggio cloud sospeso: merge in corso con file in conflitto ($IN_CONFLITTO). Risolvi i conflitti (o git merge --abort): finché restano, niente commit né push."
  exit 0
fi

# Righe aggiunte che iniziano con <<<<<<< o >>>>>>>, esclusa .obsidian/ (marcatori legittimi).
con_marcatori() {
  git diff --cached --name-only --diff-filter=AM -- Vault 2>/dev/null | while IFS= read -r f; do
    case "$f" in */.obsidian/*) continue ;; esac
    git diff --cached -U0 --no-color -- "$f" | grep -qE '^\+(<<<<<<<|>>>>>>>)( |$)' && printf '%s ' "$f"
  done
}

if [ -n "$(git status --porcelain -- Vault 2>/dev/null)" ]; then
  git add -A -- Vault >/dev/null 2>&1
  MARCATI="$(con_marcatori)"; MARCATI="${MARCATI% }"
  if [ -n "$MARCATI" ]; then
    # shellcheck disable=SC2086
    git reset -q -- $MARCATI >/dev/null 2>&1
    avvisa "Salvataggio cloud sospeso: marcatori di conflitto (<<<<<<< / >>>>>>>) in $MARCATI. Toglili: finché ci sono, niente commit né push."
    exit 0
  fi
  git commit -q -m "UniCode (cloud): salvataggio automatico $(date '+%Y-%m-%d %H:%M')" >/dev/null 2>&1 || true
fi
[ -n "$SOLO_COMMIT" ] && exit 0

# Push anche dei commit fatti a mano e non ancora inviati.
if [ -n "$(git log --oneline "origin/$RAMO..HEAD" 2>/dev/null || echo nuovo)" ]; then
  for attesa in 2 4 8; do
    timeout 30 git push -q -u origin "$RAMO" >/dev/null 2>&1 && break
    sleep "$attesa"
  done
fi

# --- allineamento di master --------------------------------------------------
timeout 15 git fetch -q origin master 2>/dev/null || { avvisa "Salvataggio cloud: fetch di master fallito, master non aggiornato."; exit 0; }
git merge-base --is-ancestor HEAD origin/master 2>/dev/null && exit 0   # master ha già tutto

if ! git merge-base --is-ancestor origin/master HEAD 2>/dev/null; then
  : >"$SEGNO"
  if git merge -q --no-edit origin/master >/dev/null 2>&1; then
    rm -f "$SEGNO"
    timeout 30 git push -q origin "$RAMO" >/dev/null 2>&1 || true
  else
    git merge --abort >/dev/null 2>&1 || true
    rm -f "$SEGNO"
    avvisa "Salvataggio cloud: master è andato avanti (laptop?) e va in conflitto con il ramo $RAMO. Il lavoro è salvo sul ramo; master NON è aggiornato finché il conflitto non si risolve."
    exit 0
  fi
fi

for attesa in 2 4 8; do
  timeout 30 git push -q origin HEAD:master >/dev/null 2>&1 && exit 0
  sleep "$attesa"
done
avvisa "Salvataggio cloud: push su master fallito; il lavoro è salvo sul ramo $RAMO."

exit 0
