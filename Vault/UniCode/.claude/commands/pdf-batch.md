---
description: "Converte in PDF tutti gli appunti e le lezioni markdown che non hanno ancora un PDF corrispondente. Poi git add + commit + push."
---

**1. Trova file senza PDF**

Scansiona queste due coppie di cartelle ricorsivamente. Per ogni `.md` sorgente, verifica se esiste il corrispondente `.pdf` nella cartella destinazione con la stessa struttura.

| Sorgente | Destinazione |
|---|---|
| `claudeAppunti/` | `claudeAppunti_PDF/` |
| `claudeLezioni/` | `claudeLezioni_PDF/` |

Esempio:
- `claudeAppunti/APPUNTI DIRITTO/appunti_moduloD8_privacy_gdpr.md` → `claudeAppunti_PDF/APPUNTI DIRITTO/appunti_moduloD8_privacy_gdpr.pdf`
- `claudeLezioni/LEZIONI SECURITY/lezione_moduloS1_enumerazione.md` → `claudeLezioni_PDF/LEZIONI SECURITY/lezione_moduloS1_enumerazione.pdf`

Lista tutti i file mancanti.

---

**2. Converti**

Per ogni file mancante, esegui:
```bash
pandoc '<path_md>' -o '<path_pdf>' --pdf-engine=xelatex -V geometry:margin=2.5cm -V fontsize=11pt -V lang=it
```

Se pandoc fallisce su un file, segnalalo ma continua con gli altri.

---

**3. Git push**

```bash
cd /home/lorenzo/UniCode
git add claudeAppunti_PDF/ claudeLezioni_PDF/
git commit -m "pdf: batch convert $(date +%Y-%m-%d)"
git push
```

---

**4. Report**

Mostra:
- File convertiti (con path)
- File falliti (con errore)
- File già aggiornati (nessuna azione)
