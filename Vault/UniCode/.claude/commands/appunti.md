---
description: "Elabora gli appunti grezzi di un modulo in appunti definitivi e aggiorna lo stato. Uso: /appunti <CODICE> <ID>"
argument-hint: "<CODICE> <ID modulo> — es. FI2 3A, SO 2B"
---

Il parametro passato è: "$ARGUMENTS"

---

**0. Risolvi corso e modulo**

`$ARGUMENTS` va letto come **due token**: `<CODICE> <ID modulo>`.

- Primo token → codice corso, validato contro `piano/codici.txt`.
- Secondo token → identificativo del modulo.
- Se manca un token o il codice non è valido: mostra i codici da `codici.txt` e fermati.

---

**1. Individua il file grezzo**

Cerca `corsi/<COD>/grezzi/appunti_<ID>*.md`. Considera varianti di nome (maiuscole, underscore,
spazi). Se il file non esiste, comunicalo e fermati: senza appunti grezzi non c'è niente da
elaborare.

---

**2. Carica il contesto necessario — in parallelo**

- **File grezzo** (dal passo 1)
- **Lezione di riferimento**: `corsi/<COD>/lezioni/lezione_<ID>_*.md`
- **Guida-lab**, se esiste: `corsi/<COD>/lezioni/guida_lab_<ID>_*.md`
- **Percorso del corso**: `corsi/<COD>/percorso.md` — stato del modulo e prerequisiti
- **Errori ricorrenti**: `profilo/errori.md` — dove Lorenzo tende a sbagliare

---

**3. Analisi del file grezzo**

Identifica e annota (non scrivere ancora il file di output):

- **Domande aperte**: esplicite ("perché X?") o tra parentesi o quadre.
- **Lacune**: concetti presenti nella lezione ma assenti negli appunti grezzi. Ricorda:
  **l'assenza può essere intenzionale** — Lorenzo salta deliberatamente ciò che ha già
  consolidato. Non marcarla come lacuna finché non è verificata.
- **Errori di esecuzione**, per i corsi pratici: bug negli script o nei comandi (sintassi,
  logica invertita, keyword mancanti). Per i corsi formali: passaggi non giustificati, ipotesi
  usate senza verificarle, errori di segno o di unità. Confronta con i pattern in
  `profilo/errori.md` — se l'errore è già noto, **segnalalo esplicitamente come ricorrente**.
- **Imprecisioni di formulazione**, per i corsi discorsivi: definizioni parafrasate dove la
  fonte è precisa, riferimenti citati in modo errato, concetti confusi.
- **Punti di forza**: concetti che Lorenzo ha spiegato bene o intuizioni originali —
  segnalarli positivamente rafforza l'apprendimento.

---

**4. Crea il file di appunti definitivi**

Path: `corsi/<COD>/appunti/appunti_<ID>_<nome_breve>.md`

`<nome_breve>` deve corrispondere a quello usato nella lezione dello stesso modulo.

**Struttura, valida per ogni corso:**
- Segui l'ordine della lezione come ossatura.
- Per ogni domanda aperta: **rispondi inline come blocco citazione `>`**, immediatamente dopo
  il concetto a cui si riferisce — non raccolte in fondo.
- Per ogni sezione omessa dagli appunti grezzi che risulta davvero mancante: includila con
  `> ⚠️ Questa sezione non era presente negli appunti grezzi.`
- Per ogni punto di forza: `> ✅ Ottima osservazione: ...`

**Per i corsi pratici e formali** — aggiungi:
- Per ogni errore individuato: mostra la versione errata, l'analisi di *perché* è sbagliata, e
  la versione corretta. L'analisi conta più della correzione.
- Se l'errore corrisponde a un pattern noto:
  `> ⚠️ Errore ricorrente: stesso pattern di <modulo precedente>. Vedi profilo/errori.md`

**Per i corsi discorsivi** — aggiungi:
- Per ogni imprecisione: la formulazione di Lorenzo, la correzione, e il riferimento esatto
  alla fonte.
- In chiusura: "Domande di autoverifica — Risposte", se Lorenzo le ha incluse nel grezzo.

---

**5. Aggiorna `profilo/errori.md`**

Se sono emersi errori o imprecisioni:
- Pattern già presente → aggiungi il modulo alla riga esistente.
- Pattern nuovo, legato alla materia → nuova voce nella sezione del corso (creala se il corso
  non ne ha ancora una).
- **Se lo stesso modo di sbagliare compare in 3+ moduli, o si ripresenta su un corso diverso**
  → promuovilo alla sezione **Trasversale**, con la contromisura e la previsione di dove
  tornerà. È quella sezione che il briefing carica per prima.

---

**6. Registra l'evento e aggiorna lo stato**

Appendi a `stato/giornata.md` una riga per fatto. Se il modulo è stato completato, il marcatore
è obbligatorio:

```
HH:MM · <COD> · appunti <ID> elaborati: <n> domande risolte, <n> errori corretti. CHIUSO <COD> <ID>
```

Il marcatore `CHIUSO` va scritto **solo con evidenza pratica**: per i corsi con laboratorio,
solo se Lorenzo ha eseguito gli esercizi in prima persona; per i corsi discorsivi, solo se ha
risposto alle domande di autoverifica. Verificalo dagli appunti grezzi, non darlo per scontato.
Se l'evidenza manca, niente marcatore: scrivi la riga di evento e basta.

> È da questi marcatori che `scripts/giornata.py` fa avanzare `stato/tracker.md` alle 23.
> Il tracker **non va modificato a mano da questo comando**.

Se `<COD>` è il corso attivo, aggiorna `stato/corrente.md`: stato del modulo e punto di ripresa.

---

**7. Verifica qualità (checklist interna)**

- [ ] Ogni domanda dagli appunti grezzi ha una risposta inline
- [ ] Nessuna sezione della lezione è stata saltata senza nota
- [ ] Gli errori hanno l'analisi del perché, non solo la correzione
- [ ] `profilo/errori.md` aggiornato dove serviva, con promozione a trasversale se ricorre
- [ ] La riga di evento è in `stato/giornata.md`, e il marcatore `CHIUSO` c'è **solo** con
      evidenza pratica

Poi invoca `lorenzo-skills:unicode-output-gate` per la verifica finale.

---

**8. Collega la nota al grafo**

Invoca `lorenzo-skills:unicode-link-note` per il blocco AUTO-LINKS dei nuovi appunti.

---

**9. Comunica il risultato**

- Path del file creato
- Conteggio: domande risolte, errori corretti, sezioni integrate, punti di forza segnalati
- Se il modulo è stato chiuso o è rimasto aperto, con la motivazione
- Se sono emersi errori ricorrenti, menzionali
