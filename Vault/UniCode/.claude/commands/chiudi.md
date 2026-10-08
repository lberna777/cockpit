---
description: "Chiude la sessione di studio: raccoglie il giudizio, aggiorna stato e log, fissa nella Plancia lo studio di domani."
---

> **Questo comando è facoltativo.** La traccia meccanica della sessione la scrivono già il
> SessionEnd hook e il consolidamento serale. `/chiudi` aggiunge **il giudizio**: cosa ha
> funzionato, cosa è rimasto aperto, da dove si riparte — e fissa nella Plancia lo studio di
> domani (passo 9). Se la giornata è finita senza, non è andato perso niente: il briefing del
> giorno dopo segnala che la giornata non è pianificata e la si fissa all'avvio.

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
- Se gli esami attivi sono cambiati, riscrivi l'intestazione: `corrente.md` descrive **solo gli
  esami attivi**, con una riga di sintesi ciascuno in testa

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

**7. Revisione degli errori — agente dedicato**

Si esegue **per ogni corso toccato oggi** (i codici presenti in `stato/giornata.md`). Serve ad
accrescere `profilo/errori.md` con gli errori che Lorenzo commette davvero sulle materie nuove:
il quality gate conosce solo quelle vecchie, e i pattern di un corso nascono dall'esecuzione, non
dalle previsioni.

**7a. Raccogli il materiale da passare all'agente** — non leggerlo tu:
- i file del corso creati o modificati oggi:
  `find corsi/<COD> -type f -newermt "$(date +%F)" -not -path '*/materiali/*' -not -path '*/prove/*'`
- le trascrizioni delle sessioni di oggi — Claude Code risolve il symlink `~/UniCode`, quindi
  stanno sotto il percorso reale:
  `find ~/.claude/projects/-home-lorenzo-cockpit-Vault-UniCode -maxdepth 1 -name '*.jsonl' -newermt "$(date +%F)"`;
- la risposta di Lorenzo al passo 2 e le righe di `stato/giornata.md` del corso.

**7b. Lancia un subagent** (`general-purpose`) con questo mandato, completato dei percorsi:

> Sei il revisore degli errori di studio di Lorenzo per il corso `<COD>` (<nome esteso>).
> Leggi per intero `~/UniCode/profilo/errori.md`, poi i file e la trascrizione indicati.
> Nella trascrizione concentrati sui messaggi di Lorenzo: codice che ha scritto, risposte
> alle autoverifiche, comandi eseguiti, domande, e i punti in cui Claude lo ha corretto.
>
> Cerca **solo errori commessi da Lorenzo, con un'evidenza**. Le avvertenze ⚠️ scritte nelle
> lezioni sono previsioni, non errori: non contano. Un errore di Claude non conta.
>
> Per ciascun errore trovato:
> - se è un'istanza di un pattern **trasversale** già presente, aggiungi sotto quel pattern una
>   riga `- [AAAA-MM-GG] <COD>: <cosa è successo>. Evidenza: <file o citazione breve>`;
> - se è un pattern **del corso**, aggiungilo nella sezione `### <COD> — <nome esteso>` sotto
>   «Per corso», creandola prima di «Archivio — corsi chiusi» se non esiste, nel formato
>   `- [AAAA-MM-GG] <errore> → <causa> → <correzione>. Evidenza: <…>`;
> - se lo stesso errore di corso compare già su **un altro corso**, non duplicarlo: segnalalo
>   come candidato trasversale nel report, senza promuoverlo.
>
> Regole di strato: `profilo/errori.md` si **accresce, non si riscrive**. Non cancellare né
> riformulare righe esistenti; una riga superata si marca `[superato AAAA-MM]`. Non toccare
> nessun altro file. Se non trovi errori con evidenza, non scrivere nulla.
>
> Restituisci un report breve: errori aggiunti (con sezione), ricorrenze di pattern esistenti,
> candidati trasversali, e ciò che hai scartato per mancanza di evidenza.

**7c. Registra l'esito**, dopo il ritorno dell'agente:
- una riga in `stato/giornata.md`: `HH:MM · <COD> · revisione errori: <n> nuovi, <m> ricorrenze`;
- il report va mostrato a Lorenzo nella conferma finale (passo 9). I candidati trasversali
  li decide lui: non si promuovono in automatico.

---

**8. Aggiorna prontuario, glossario e troubleshooting**

**8a. Prontuario d'esame** — per ogni corso con prontuario (`corsi/<COD>/appunti/prontuario_<COD>.md`)
toccato oggi da una sessione **pratica** (lab, esercizi, prova). Il prontuario è materiale da
consultare in sede d'esame: si aggiorna con ciò che la sessione ha fatto **incontrare davvero**,
non con ciò che il materiale contiene.

- **Cosa entra**: codice nuovo imparato; ingegni e scorciatoie emersi eseguendo; frammenti da
  copiare e incollare così come sono; errori di compilazione o eccezioni incontrati, con il
  **testo esatto** del messaggio (Eclipse e `javac`), causa e rimedio; righe ⚠️ dove Lorenzo ha
  sbagliato. Schemi delle prove d'esame solo **dopo** aver fatto quella prova.
- **Dove**: nella sezione della **parte del compito** (§1 errori, §2 Eclipse, §3 model,
  §4 persistence, §5 controller/UI), non del modulo; aggiungere le voci nuove all'*Indice per
  bisogno* in cima, con la colonna *Fatto in* che punta al file svolto da Lorenzo. Se un LAB o una
  prova è stato completato, copiarne il progetto in `corsi/FI2/esame_FI2/svolti/`.
- **Forma**: tabelle e codice, non prosa. **Ogni frammento di codice è commentato riga per
  riga** — cosa fa e perché lì — perché si usi e si interpreti senza rileggere la teoria. Valori
  e messaggi verificati eseguendoli (jshell/terminale), non scritti a memoria.
- Se la sessione non ha prodotto niente di consultabile, non si scrive nulla.

Una riga in `stato/giornata.md`: `HH:MM · <COD> · prontuario: <cosa aggiunto>`.

**8b. Glossario e troubleshooting** *(solo se serve)*

- Termini nuovi → il glossario del corso, in `corsi/<COD>/`
- Problemi tecnici risolti sull'ambiente → `troubleshooting_vm.md`, con sintomo, causa,
  soluzione

---

**9. Pianifica domani** — *non facoltativo dentro `/chiudi`*

Regola di Lorenzo del 2026-10-08: lo studio non resta mai senza data. Esegui
`.claude/commands/pianifica.md` con ambito `domani`: proponi 1-3 attività di studio concrete per
domani partendo dal **punto di ripresa** scritto al passo 5, attendi la conferma di Lorenzo,
scrivile nella Plancia con scadenza domani e aggiorna `giorno:` in `stato/pianificazione.md`.

Se domani è lunedì o il primo del mese, chiedi a Lorenzo se vuole fissare già ora anche la
settimana o il mese (`/pianifica settimana domani`); altrimenti ci penserà il briefing all'avvio.
Se Lorenzo dice che domani non studia, scrivi comunque `giorno:` con la data di domani e una
riga in `stato/giornata.md` (`HH:MM · PIANO · domani niente studio, deciso da Lorenzo`): una
giornata vuota decisa è un dato, non una dimenticanza.

---

**10. Conferma finale**

Mostra a Lorenzo:
- Le attività di studio fissate per domani nella Plancia
- Corso e moduli aggiornati, con i marcatori scritti
- Il punto esatto da cui ripartirà
- Il report della revisione errori (passo 7), con gli eventuali candidati trasversali da decidere- I moduli con ripasso scaduto da `stato/tracker.md`, se ce ne sono:
  `⚠️ Ripasso scaduto: [moduli]`
- Che gradini e scadenze dei ripassi si assestano al consolidamento delle 23
