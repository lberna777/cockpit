---
description: "Analisi gap: identifica moduli a rischio, ripasso scaduto, errori ricorrenti e produce un piano d'azione prioritizzato."
---

**Carica tutto il contesto di analisi — in parallelo:**
- `stato/corrente.md`
- `stato/tracker_ripasso.md`
- `stato/errori_frequenti.md`
- `ESAMI SCELTI.md`

---

**Analisi e output**

Produci esclusivamente questo report:

---

## Analisi Lacune — [DATA]

### 1. Copertura per esame

Per ogni esame, calcola:
```
[Materia] — Esame: [data] (tra X giorni)
Moduli completati: X/Y (Z%)
Moduli in corso (🔄): [lista con stato interno]
Moduli non iniziati (⬜): [lista]
Ore stimate rimanenti: [da ESAMI SCELTI.md]
Ore disponibili: [giorni rimasti × ore/giorno dalla fase corrente]
Bilancio: [surplus/deficit ore]
```

### 2. Moduli a rischio critico

Lista ordinata per urgenza — moduli dove:
- L'esame è vicino E il modulo è ⬜
- Il modulo è 🔄 da più di 7 giorni senza progresso
- Il bilancio ore è in deficit

Per ciascuno: **azione concreta** per sbloccarlo.

### 3. Ripasso scaduto

Da tracker_ripasso.md, lista tutti i moduli con ripasso scaduto:
```
| Modulo | Completato | Ultimo ripasso | Scaduto da |
```

Suggerimento: "Dedica 15-20 min a inizio giornata a `/ripassa [modulo più urgente]`"

### 4. Pattern di errore attivi

Da errori_frequenti.md, i pattern che appaiono in 2+ moduli:
```
| Pattern | Moduli coinvolti | Rischio esame |
```

### 5. Piano d'azione prioritizzato

Top 5 azioni in ordine di impatto, con tempo stimato:
1. [azione] — [tempo] — [perché è prioritaria]
2. ...
3. ...
4. ...
5. ...

---

Non aggiungere testo libero oltre a questi elementi.
