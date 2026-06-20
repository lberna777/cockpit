---
description: "Sessione di ripasso adattivo su un modulo completato. Genera domande nuove (non le stesse dell'autoverifica). Uso: /ripassa <ID>"
argument-hint: "ID modulo — SysAdmin: 0A-3F | Security: S1-S12 | Diritto: D1-D13"
---

Il modulo da ripassare è: $ARGUMENTS

---

**1. Verifica che il modulo sia completato**

Leggi `stato/corrente.md`. Il modulo deve essere ✅. Se è ⬜ o 🔄, comunicalo e suggerisci `/lezione` o `/appunti` invece.

---

**2. Carica il contesto — in parallelo**

- **Appunti definitivi** del modulo (glob ricorsivo — stanno nelle sottocartelle per-materia `APPUNTI <MATERIA>/`): `claudeAppunti/**/appunti_modulo$ARGUMENTS_*.md`
- **Errori frequenti**: `stato/errori_frequenti.md` — per generare domande mirate sui punti deboli
- **Tracker ripasso**: `stato/tracker_ripasso.md` — per sapere quanto tempo è passato dall'ultimo ripasso

---

**3. Genera domande di ripasso**

Genera **5 domande nuove** — diverse dalle domande di autoverifica della lezione originale.

Criteri di generazione:
- Almeno 1 domanda deve testare un **errore ricorrente** di Lorenzo (da errori_frequenti.md)
- Almeno 1 domanda deve richiedere un **collegamento tra moduli** (es. "Come si collega X di questo modulo con Y del modulo Z?")
- Le domande devono essere del tipo che il professore farebbe all'esame
- Livello di difficoltà crescente: 2 base, 2 intermedio, 1 avanzato

**Per SysAdmin/Security:**
- Almeno 2 domande devono richiedere di scrivere/prevedere l'output di un comando
- "Cosa succede se esegui...?", "Scrivi il comando per...", "Quale output ti aspetti da...?"

**Per Diritto:**
- Almeno 2 domande devono richiedere la citazione dell'articolo/norma specifica
- "Qual è la base giuridica per...?", "Come distingui X da Y?", "Quale norma disciplina...?"

---

**4. Modalità interrogazione**

Presenta le domande **una alla volta**. Aspetta la risposta di Lorenzo prima di passare alla successiva.

Per ogni risposta:
- Se corretta: conferma brevemente e passa alla successiva
- Se parziale: segnala cosa manca, mostra la risposta completa con riferimento agli appunti
- Se errata: correggi con spiegazione dettagliata, cita la sezione degli appunti/lezione pertinente

---

**5. Valutazione finale**

Dopo le 5 domande, mostra:

```
## Risultato ripasso — Modulo $ARGUMENTS

Corrette: X/5
Parziali: X/5
Errate: X/5

**Punti solidi**: [concetti dimostrati]
**Da rivedere**: [concetti deboli — con riferimento alla sezione degli appunti]
```

Se sono emerse nuove debolezze non presenti in errori_frequenti.md, aggiornarlo.

---

**6. Aggiorna tracker_ripasso.md**

- "Ultimo ripasso" = data odierna
- Calcola "Prossimo ripasso" con intervallo crescente:
  - Prima volta: +3 giorni
  - Seconda volta: +7 giorni
  - Terza volta: +14 giorni
  - Quarta volta+: +30 giorni
- Aggiorna "Priorità" in base alla nuova data
