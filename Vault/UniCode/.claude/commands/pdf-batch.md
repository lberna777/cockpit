---
description: "Converte in PDF tutti gli appunti markdown che non hanno ancora un PDF corrispondente. Poi git add + commit + push."
---

**1. Trova appunti senza PDF**

Scansiona `claudeAppunti/` ricorsivamente. Per ogni file `.md`, verifica se esiste il corrispondente `.pdf` in `claudeAppunti_PDF/` con la stessa struttura di cartelle.

Esempio:
- `claudeAppunti/APPUNTI DIRITTO/appunti_moduloD8_privacy_gdpr.md`
- → deve esistere `claudeAppunti_PDF/APPUNTI DIRITTO/appunti_moduloD8_privacy_gdpr.pdf`

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
git add claudeAppunti_PDF/
git commit -m "pdf: batch convert $(date +%Y-%m-%d)"
git push
```

---

**4. Report**

Mostra:
- File convertiti (con path)
- File falliti (con errore)
- File già aggiornati (nessuna azione)
