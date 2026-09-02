---
description: "Genera il piano di studio per oggi basandosi su briefing, tracker e sessione d'esame in corso."
---

Il briefing è già in contesto: **non rileggere i file di stato che contiene**. Leggi in più solo:
- `piano/piano_laurea.md` — sessione corrente, esami che vi appartengono, catene di dipendenza
- `corsi/<COD>/percorso.md` del corso attivo, se serve il dettaglio del modulo

Calcola i giorni mancanti al primo appello della sessione in corso da `piano/piano_laurea.md`.
Non usare date cablate.

Identifica la **prossima singola cosa da fare**, in questa priorità:
1. **Ripasso scaduto** (dal tracker nel briefing) — se c'è, va per primo, 15-20 minuti
2. Il corso più a rischio rispetto all'appello: moduli rimasti diviso settimane rimaste
3. Il modulo aperto nel corso attivo

Produci esclusivamente:

---

**Prossima cosa da fare — [DATA]**

**[Corso] · [blocco di programma]**
[ID modulo] — [azione concreta: cosa fare, quale esercizio, quale file]

*(Solo se presente: un segnale di rischio in una riga — es. "SO: 5 moduli rimasti, 4 settimane")*

---

Regole:
- **Una sola azione, non un elenco di blocchi.**
- Se c'è un ripasso scaduto, quello è la prossima cosa: indicalo esplicitamente prima
  dell'azione principale.
- Dimensiona in **blocchi di programma**, non in ore: la disponibilità giornaliera di Lorenzo è
  troppo variabile perché una stima oraria significhi qualcosa.
- Se manca la fonte per il modulo: azione = "Procurare [titolo esatto] per [modulo]", e dillo
  come prima cosa.
- Un solo esame per volta in fase attiva: non proporre un modulo di un corso diverso da quello
  attivo, salvo che sia un ripasso scaduto.
- **Non aggiungere testo libero.**
