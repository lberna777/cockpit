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
pandoc '<path_md>' -o '<path_pdf>' --pdf-engine=xelatex \
  -V geometry:margin=2.5cm -V fontsize=11pt -V lang=it
```

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
