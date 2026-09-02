---
description: "Chiude la sessione di studio: raccoglie il giudizio, aggiorna stato e log. Facoltativo — la traccia meccanica è già automatica."
---

> **Questo comando è facoltativo.** La traccia meccanica della sessione la scrivono già il
> SessionEnd hook e il consolidamento serale. `/chiudi` aggiunge **il giudizio**: cosa ha
> funzionato, cosa è rimasto aperto, da dove si riparte. Se la giornata è finita senza, non è
> andato perso niente.

Esegui i passi in ordine.

---

**1. Leggi lo stato** *(solo se non già letto in questa conversazione)*

- `stato/corrente.md` — esame attivo, stato dei moduli, punto di ripresa
- `stato/giornata.md` — le righe già scritte oggi in presa diretta: sono la base dei fatti, non
  ripartire dalla memoria della conversazione

---

**2. Raccogli il giudizio**

Chiedi a Lorenzo in **un'unica domanda compatta**, adattata al tipo di corso toccato:

*Corsi con laboratorio:*
- quali moduli o argomenti sono stati affrontati
- quali esercizi completati, quali interrotti, quali saltati
- domande rimaste aperte o blocchi non risolti
- problemi tecnici nuovi sull'ambiente

*Corsi con esercizi formali:*
- quali moduli affrontati e quali esercizi svolti fino in fondo
- dove il procedimento si è rotto, e se è stato capito perché
- quali passaggi restano meccanici e non compresi

*Corsi discorsivi:*
- quali moduli affrontati
- se le domande di autoverifica sono state completate
- concetti rimasti poco chiari

Se la sessione ha toccato più corsi, chiedi per ciascuno. **Attendi la risposta** prima di
procedere.

---

**3. Completa `stato/giornata.md`**

Aggiungi le righe di evento per ciò che è emerso dalla risposta e non era ancora annotato. Ogni
modulo portato a termine oggi deve avere il suo marcatore:

```
HH:MM · <COD> · <fatto in una riga>. CHIUSO <COD> <ID>
HH:MM · <COD> · <fatto in una riga>. RIPASSO <COD> <ID> ok|debole
```

Criterio per `CHIUSO`, rigoroso: per i corsi con laboratorio **solo se Lorenzo ha eseguito gli
esercizi in prima persona**; per i corsi formali solo se ha svolto gli esercizi fino al
risultato; per i corsi discorsivi solo se ha risposto all'autoverifica e scritto i grezzi. Un
modulo letto non è un modulo chiuso.

---

**4. Aggiorna `stato/tracker.md` — solo per i moduli chiusi**

Per ogni marcatore `CHIUSO` scritto al passo 3, aggiungi o sostituisci la riga nel tracker:

| Colonna | Valore |
|---|---|
| Codice | `<COD>` |
| Modulo | `<ID>` |
| Chiuso | data odierna |
| Ultimo ripasso | `—` |
| Gradino | `3` |
| Prossimo | data odierna + 3 giorni |

Per ogni marcatore `RIPASSO`, aggiorna **solo** la colonna *Ultimo ripasso* alla data odierna.
**Non toccare Gradino e Prossimo.**

> Perché la differenza. Alle 23 `scripts/giornata.py` rilegge i marcatori: per `CHIUSO`
> riscrive la riga per intero e ottiene lo stesso risultato, quindi anticiparla è innocuo. Per
> `RIPASSO` invece **avanza il gradino di uno a partire dal valore che trova**: se l'avessi già
> avanzato tu, avanzerebbe due volte e il ripasso si allontanerebbe in silenzio. Lasciando
> gradino e data al consolidamento, il conto resta esatto.

---

**5. Aggiorna `stato/corrente.md`**

- Stato dei moduli toccati, con lo stesso criterio rigoroso del passo 3
- **Punto di ripresa**: il punto esatto da cui ripartire, non una generica "continuare con X"
- Se l'esame attivo è cambiato, riscrivi l'intestazione: `corrente.md` descrive **solo l'esame
  attivo**

---

**6. Aggiungi la voce di sessione in `log/AAAA-MM.md`**

Nel file del mese corrente, in coda:

```
### Sessione — AAAA-MM-GG
**Focus**: <COD> — <moduli>
**Coperto**:
- ...
**Non coperto / da riprendere**:
- ...
**Da dove ripartire**:
→ ...
```

---

**7. Aggiorna glossario e troubleshooting** *(solo se serve)*

- Termini nuovi → il glossario del corso, in `corsi/<COD>/`
- Problemi tecnici risolti sull'ambiente → `troubleshooting_vm.md`, con sintomo, causa,
  soluzione

---

**8. Conferma finale**

Mostra a Lorenzo:
- Corso e moduli aggiornati, con i marcatori scritti
- Il punto esatto da cui ripartirà
- I moduli con ripasso scaduto da `stato/tracker.md`, se ce ne sono:
  `⚠️ Ripasso scaduto: [moduli]`
- Che gradini e scadenze dei ripassi si assestano al consolidamento delle 23
