#!/usr/bin/env bash
# PDF «grafico» di un appunto markdown: pandoc → HTML con stile.css → Chromium → PDF.
# Per i file pensati da leggere stampati (prontuari, cheatsheet): disegni SVG, riquadri colorati,
# tabelle e codice leggibili. Il markdown resta l'unico sorgente; il PDF si rigenera.
#
# Uso: scripts/pdf_grafico.sh corsi/CALC/appunti/prontuario_CALC.md [altri .md ...]
# Uscita: corsi/<COD>/pdf/appunti/<nome>.pdf (stessa regola di /pdf-batch).
#
# Riquadri: nel markdown si scrivono come callout di Obsidian (> [!regola] Titolo), così si
# vedono anche in Obsidian. Tipi: regola, esempio, attenzione, perche, soluzioni.
# Il titolo del piè di pagina è il campo `title` del frontmatter.
# Serve: pandoc, node con playwright (nel cloud c'è); in mancanza, chromium --headless.
set -euo pipefail

QUI="$(cd "$(dirname "$0")" && pwd)"
ASSET="$QUI/pdf_grafico"
TMP="$(mktemp -d)"; trap 'rm -rf "$TMP"' EXIT

for md in "$@"; do
  md="$(realpath "$md")"
  dir="$(dirname "$md")"; nome="$(basename "$md" .md)"
  corso="$(dirname "$dir")"; sotto="$(basename "$dir")"
  out_dir="$corso/pdf/$sotto"; mkdir -p "$out_dir"
  pdf="$out_dir/$nome.pdf"
  html="$dir/.$nome.stampa.html"   # accanto al sorgente: così i percorsi img/… si risolvono

  titolo="$(awk '/^---$/{n++; next} n==1 && /^title:/{sub(/^title: *"?/,""); sub(/"$/,""); print; exit}' "$md")"
  [ -z "$titolo" ] && titolo="$nome"

  pandoc "$md" -f markdown+wikilinks_title_after_pipe+mark -t html5 -s \
    --lua-filter="$ASSET/obsidian.lua" --css="$ASSET/stile.css" --embed-resources \
    --resource-path="$dir" --toc --toc-depth=2 --number-sections \
    --highlight-style=pygments -M lang=it -o "$html"

  if node -e "require('playwright')" 2>/dev/null; then
    NODE_PATH="$(npm root -g 2>/dev/null || true)" node "$ASSET/stampa.js" "$html" "$pdf" "$titolo"
  else
    chrome="$(command -v chromium || command -v chromium-browser || command -v google-chrome || true)"
    [ -z "$chrome" ] && { echo "manca un Chromium per stampare $nome" >&2; rm -f "$html"; exit 1; }
    "$chrome" --headless --no-sandbox --no-pdf-header-footer --print-to-pdf="$pdf" "file://$html"
  fi
  rm -f "$html"
  echo "✔ $pdf"
done
