---
description: "Converte in PDF le lezioni e gli appunti markdown che non hanno ancora un PDF. Poi git add + commit + push."
argument-hint: "<CODICE> opzionale — vuoto = tutti i corsi aperti"
---

Il parametro passato è: "$ARGUMENTS"

Se è un codice valido in `piano/codici.txt`, lavora solo su quel corso. Se è vuoto, su tutti i
corsi che hanno una cartella in `corsi/`.

---

**1. Trova i file senza PDF**

Per ogni corso, i PDF stanno in una cartella separata dai sorgenti, che rispecchia la struttura:

| Sorgente | Destinazione |
|---|---|
| `corsi/<COD>/lezioni/` | `corsi/<COD>/pdf/lezioni/` |
| `corsi/<COD>/appunti/` | `corsi/<COD>/pdf/appunti/` |

Esempio: `corsi/FI2/lezioni/lezione_3A_ricorsione.md` →
`corsi/FI2/pdf/lezioni/lezione_3A_ricorsione.pdf`

Un file va convertito se il PDF manca **oppure** se il `.md` è più recente del `.pdf`. Elenca
i file da convertire prima di iniziare.

---

**2. Converti**

Crea le cartelle di destinazione se non esistono, poi per ogni file:

```bash
sed -e 's/\xEF\xB8\x8F//g' -e 's/✅/✔/g' -e 's/🔶/(in corso)/g' \
    -e 's/⬜/☐/g' -e 's/⭐/★/g' '<path_md>' \
  | awk '/^ *```/{f=!f} f{gsub(/⚠/,"(!)")} {print}' \
  | pandoc -f markdown -o '<path_pdf>' --pdf-engine=xelatex \
  --resource-path="$(dirname '<path_md>')" \
  -V geometry:margin=2.5cm -V fontsize=11pt -V lang=it \
  -V mainfont="DejaVu Sans" -V monofont="DejaVu Sans Mono"
```

`--resource-path` serve perché il sorgente arriva da stdin: senza, pandoc non trova le immagini
`img/…` degli appunti. `✅`, `🔶`, `⬜` e `⭐` non esistono in DejaVu Sans e vengono sostituiti
(`⬜` → `☐`, `⭐` → `★`). L'`awk` sostituisce `⚠` con `(!)` **solo dentro i blocchi di codice**:
lì pandoc rende i commenti in DejaVu Sans Mono Oblique, che non ha il glifo (verificato il
2026-10-08 sul prontuario FI2); fuori dal codice `⚠` resta.

Il font di default (Latin Modern) non ha `⚠` e le lezioni perderebbero in silenzio gli avvisi
sugli errori ricorrenti: DejaVu Sans li ha. Il `sed` toglie il selettore di variante U+FE0F
che segue gli emoji, assente in ogni font. Controllo: la conversione non deve stampare
`Missing character`.

Se xelatex fallisce per sequenze di escape nel sorgente (tipicamente `\x` dentro blocchi di
codice), fai il pre-processing su una copia temporanea invece di modificare il sorgente.

Se un file fallisce comunque, **segnalalo e continua con gli altri**: un errore non deve
fermare il batch.

---

**3. Commit e push**

```bash
git add 'corsi/*/pdf/'
git commit -m "pdf: batch convert $(date +%Y-%m-%d)"
git push
```

---

**4. Report**

- File convertiti, con il path
- File falliti, con l'errore
- File già aggiornati, nessuna azione

---

**5. Registra l'evento**

Appendi a `stato/giornata.md`:

```
HH:MM · — · pdf batch: <n> convertiti, <n> falliti.
```
