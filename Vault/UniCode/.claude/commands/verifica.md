---
description: "Verifica qualità di una lezione o appunti generati. Confronta con il PDF sorgente e segnala gap. Uso: /verifica <ID>"
argument-hint: "ID modulo — SysAdmin: 0A-3F | Security: S1-S12 | Diritto: D1-D13"
---

Il modulo da verificare è: $ARGUMENTS

---

**1. Identifica i file da verificare**

Cerca:
- Lezione (glob ricorsivo — sottocartelle `LEZIONI <MATERIA>/`): `claudeLezioni/**/lezione_modulo$ARGUMENTS_*.md`
- Appunti definitivi (glob ricorsivo — sottocartelle `APPUNTI <MATERIA>/`): `claudeAppunti/**/appunti_modulo$ARGUMENTS_*.md`

Se nessuno dei due esiste, comunicalo e fermati.

---

**2. Identifica il PDF sorgente**

Da `stato/percorso.md`, recupera il materiale Virtuale del modulo $ARGUMENTS.
Cerca e leggi il PDF corrispondente.

Se il PDF non è disponibile, la verifica è limitata alla coerenza interna (salta il passo 3).

---

**3. Confronto con il PDF sorgente**

Per la lezione (se esiste):
- [ ] Ogni concetto chiave del PDF è presente nella lezione
- [ ] Nessun concetto è stato aggiunto che non sia nel PDF (per Diritto: critico)
- [ ] La terminologia corrisponde esattamente al PDF (per Diritto: verificare parola per parola)
- [ ] Gli esercizi coprono i concetti del lab PDF (per SysAdmin/Security)

Per gli appunti definitivi (se esistono):
- [ ] Ogni domanda degli appunti grezzi ha ricevuto risposta
- [ ] Le risposte inline sono accurate rispetto al PDF
- [ ] Le sezioni integrate sono complete

---

**4. Verifica coerenza interna**

- [ ] Lezione e appunti usano la stessa terminologia
- [ ] I concetti chiave nella lezione corrispondono a quelli in `stato/percorso.md`
- [ ] Le connessioni con altri moduli sono accurate (i moduli citati esistono e i concetti referenziati sono corretti)

---

**5. Report**

```
## Verifica — Modulo $ARGUMENTS

### Copertura PDF
Concetti nel PDF: X
Concetti nella lezione: Y
Copertura: Z%
Concetti mancanti: [lista, se presenti]

### Accuratezza (solo Diritto)
Terminologia fedele al PDF: [sì/no — dettagli se no]
Articoli/norme citati correttamente: [sì/no]

### Coerenza interna
Lezione ↔ Appunti: [coerente/discrepanze]
Connessioni: [accurate/da correggere]

### Azioni correttive
[Lista numerata di correzioni necessarie, se presenti]
```

Se ci sono correzioni necessarie, chiedere a Lorenzo se vuole che vengano applicate.
