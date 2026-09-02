---
description: "Sessione di ripasso adattivo su un modulo completato. Genera domande nuove, non quelle dell'autoverifica. Uso: /ripassa <CODICE> <ID>"
argument-hint: "<CODICE> <ID modulo> — es. FI2 3A, LAS 2B"
---

Il parametro passato è: "$ARGUMENTS"

---

**0. Risolvi corso e modulo**

Due token: `<CODICE> <ID modulo>`, il codice validato contro `piano/codici.txt`. Se manca un
token o il codice non è valido, mostra i codici dal file e fermati.

---

**1. Verifica che il modulo sia chiuso**

Cerca il modulo in `stato/tracker.md`. Se non c'è, controlla `corsi/<COD>/percorso.md`: se il
modulo non è mai stato chiuso, comunicalo e suggerisci `/lezione` o `/appunti` invece.

---

**2. Carica il contesto — in parallelo**

- **Appunti definitivi**: `corsi/<COD>/appunti/appunti_<ID>_*.md`
- **Lezione**: `corsi/<COD>/lezioni/lezione_<ID>_*.md` — per sapere quali erano le domande di
  autoverifica, così da **non ripeterle**
- **Errori ricorrenti**: `profilo/errori.md` — per domande mirate sui punti deboli
- **Tracker**: `stato/tracker.md` — da quanto tempo il modulo non viene ripassato e a che
  gradino sta

---

**3. Genera le domande**

**5 domande nuove**, diverse da quelle di autoverifica della lezione.

Criteri di composizione, tutti obbligatori:
- Almeno **1 domanda su un errore ricorrente** di Lorenzo (da `profilo/errori.md`), scegliendo
  di preferenza un pattern **trasversale**: quelli tornano su ogni corso.
- Almeno **1 domanda di collegamento fra moduli** — meglio se attraversa i corsi in catena di
  `piano/piano_laurea.md` (es. da `FI2` verso `IDS`, da `CALC` verso `SO`).
- Difficoltà crescente: **2 base, 2 intermedio, 1 avanzato**.
- Devono essere del tipo che il docente farebbe all'esame.

Adatta la forma al tipo di verifica del corso:
- **Corsi con laboratorio**: almeno 2 domande devono chiedere di scrivere un comando o
  prevederne l'output — "cosa succede se esegui…?", "scrivi il comando per…", "quale output ti
  aspetti da…?"
- **Corsi con esercizi formali**: almeno 2 domande devono richiedere un procedimento svolto o
  la verifica di un caso limite — "quale ipotesi ti serve per applicare X?", "cosa succede al
  risultato se…?"
- **Corsi discorsivi**: almeno 2 domande devono richiedere la citazione del riferimento esatto
  e una distinzione fra concetti vicini.

---

**4. Modalità interrogazione**

Presenta le domande **una alla volta**. Aspetta la risposta di Lorenzo prima di passare alla
successiva.

Per ogni risposta:
- **Corretta**: conferma brevemente e passa oltre.
- **Parziale**: segnala cosa manca, poi mostra la risposta completa con il riferimento alla
  sezione degli appunti.
- **Errata**: correggi con spiegazione distesa, citando la sezione di appunti o lezione
  pertinente.

---

**5. Valutazione finale**

```
## Risultato ripasso — <COD> <ID>

Corrette: X/5   Parziali: X/5   Errate: X/5

**Punti solidi**: [concetti dimostrati]
**Da rivedere**: [concetti deboli, con il riferimento alla sezione degli appunti]
```

L'esito complessivo è **`ok`** se le corrette sono almeno 3 e nessun concetto centrale è
risultato errato; **`debole`** altrimenti.

Se sono emerse debolezze non presenti in `profilo/errori.md`, aggiungile lì — promuovendole a
**trasversale** se sono modi di ragionare e non errori di materia.

---

**6. Registra l'evento**

Appendi a `stato/giornata.md`:

```
HH:MM · <COD> · ripasso <ID>: X/5 corrette. RIPASSO <COD> <ID> ok|debole
```

> **Il tracker non va toccato da questo comando.** `scripts/giornata.py` lo fa avanzare alle 23
> a partire da questo marcatore: `ok` sale di un gradino (3 → 7 → 14 → 30 → 90 giorni),
> `debole` scende di uno. Scrivere anche qui significherebbe avanzare due volte e allontanare
> il ripasso senza accorgersene.

Comunica a Lorenzo l'esito registrato e che la nuova scadenza comparirà nel tracker dopo il
consolidamento serale.
