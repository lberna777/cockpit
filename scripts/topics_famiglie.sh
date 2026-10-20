#!/usr/bin/env bash
# Mette i topic GitHub che raggruppano le repo per famiglia (mappa in CLAUDE.md di cockpit).
# Da lanciare sul laptop, con GitHub CLI autenticata (`gh auth login`). Rilanciabile: i topic
# già presenti restano. Se la mappa cambia, aggiornare anche questo elenco.
set -euo pipefail

topic() { # repo, poi i topic da aggiungere
  local repo=$1; shift
  for t in "$@"; do args+=(--add-topic "$t"); done
  gh repo edit "lberna777/$repo" "${args[@]}" && echo "ok  $repo: $*"
  args=()
}
args=()

# Padri
topic cockpit           padre famiglia-cockpit
topic Developing        padre famiglia-developing
topic plugin-creator    padre famiglia-plugin

# Autonome
topic carguy            autonoma
topic bibiciclo         autonoma

# Figlie attive
topic lberna777.github.io famiglia-developing
topic lberna777           famiglia-developing
topic diritto-quiz-app    famiglia-cockpit
topic claudereset         famiglia-cockpit
topic Boot_Debian         famiglia-cockpit
topic StereoCompressor      famiglia-plugin
topic NEMO-StereoCompressor famiglia-plugin
topic FreakFM               famiglia-plugin
topic acidmoog-synth        famiglia-plugin

# Le figlie archiviate sono in sola lettura: GitHub non accetta modifiche ai topic
# finché non si disarchiviano, quindi restano senza.
