---
description: "Riepilogo rapido: stato dei moduli del corso attivo, avanzamento e prossimo passo."
---

Leggi `stato/corrente.md`, `stato/tracker.md` e `piano/piano_laurea.md`. Per i corsi non
attivi che hanno un `corsi/<COD>/percorso.md`, leggi quello.

Produci esclusivamente:

---

**1. Corso attivo**

```
### <COD> — <nome esteso da piano/codici.txt>
| Modulo | Nome | Stato |
|--------|------|-------|
```

Per i moduli in corso, indica lo stato interno fra parentesi.

---

**2. Avanzamento**

Una riga per ogni corso aperto, nell'ordine della sessione d'esame in
`piano/piano_laurea.md`:

```
<COD>  ████████░░ 77%  (10/13 moduli chiusi)
```

Calcola le percentuali dai file. Non inventarle.

---

**3. Prossimo passo per corso aperto**

```
<COD>  → [ID] — [azione concreta]
```

---

**4. Sessione d'esame**

Una riga: sessione corrente, esami che vi appartengono, settimane al primo appello, e se il
**checkpoint delle sei settimane** è passato o è imminente.

---

**5. Alert ripasso** *(solo se presenti)*

Dal tracker, i moduli con la data "Prossimo" già passata:

```
⚠️ Ripasso scaduto: [modulo — scaduto da N giorni]
```

---

Non aggiungere spiegazioni, commenti o testo libero oltre a questi elementi.
