---
description: "Elabora gli appunti grezzi di un modulo in appunti definitivi e aggiorna lo stato. Uso: /appunti <ID>  (es. /appunti 3A, /appunti D1, /appunti S4)"
argument-hint: "ID modulo — SysAdmin: 0A-4C | Security: S1-S15 | Diritto: D1-D13"
---

Il modulo da elaborare è: $ARGUMENTS

**Rileva il tipo di modulo dal prefisso dell'ID:**
- ID inizia con `D` → modulo **Diritto** — cartella grezzi: `APPUNTI GREZZI/Diritto/`
- ID inizia con `S` → modulo **Security** — cartella grezzi: `APPUNTI GREZZI/Lab - Security/`
- ID inizia con cifra → modulo **SysAdmin** — cartella grezzi: `APPUNTI GREZZI/Lab - sysAdm/`
- ID vuoto o non riconosciuto → mostra i formati validi e fermati

---

**1. Individua il file grezzo**

Cerca il file in base al tipo:
- SysAdmin: `/home/lorenzo/UniCode/APPUNTI GREZZI/Lab - sysAdm/Appunti_modulo$ARGUMENTS.md`
- Security: `/home/lorenzo/UniCode/APPUNTI GREZZI/Lab - Security/Appunti_modulo$ARGUMENTS.md`
- Diritto: `/home/lorenzo/UniCode/APPUNTI GREZZI/Diritto/Appunti_modulo$ARGUMENTS.md`

Considera varianti di nome (minuscole, underscore, spazi). Se il file non esiste, comunicalo e fermati.

---

**2. Carica il contesto necessario — in parallelo**

Leggi tutti questi file contemporaneamente:
- **File grezzo** (dal passo 1)
- **Lezione di riferimento** (glob ricorsivo — sottocartelle `LEZIONI <MATERIA>/`): `claudeLezioni/**/lezione_modulo$ARGUMENTS_*.md`
- **Stato corrente**: `stato/corrente.md` — per lo stato del modulo e i prerequisiti
- **Errori frequenti**: `stato/errori_frequenti.md` — per sapere dove Lorenzo tende a sbagliare

---

**3. Analisi del file grezzo**

Identifica e annota (non scrivere ancora il file output):

- **Domande aperte**: esplicite ("perché X?") o tra parentesi/quadre
- **Lacune**: concetti presenti nella lezione ma assenti negli appunti grezzi. Ricorda: l'assenza può essere intenzionale (sezione consolidata), non marcarla come lacuna
- **Per SysAdmin/Security**: bug negli script (sintassi, logica invertita, keyword mancanti). Confronta con i pattern in errori_frequenti.md — se l'errore è già noto, segnalalo esplicitamente
- **Per Diritto**: imprecisioni nelle definizioni giuridiche, articoli citati in modo errato, concetti confusi. Confronta con i pattern in errori_frequenti.md
- **Punti di forza**: concetti che Lorenzo ha spiegato bene o insight originali — segnalarli positivamente rafforza l'apprendimento

---

**4. Crea il file di appunti definitivi**

Path: `/home/lorenzo/UniCode/claudeAppunti/<SOTTOCARTELLA>/appunti_modulo$ARGUMENTS_<nome_breve>.md`

Sottocartelle:
- SysAdmin → `APPUNTI SYSADM/`
- Diritto → `APPUNTI DIRITTO/`
- Security → `APPUNTI SECURITY/` (creare se non esiste)

`<nome_breve>` deve corrispondere a quello usato nella lezione corrispondente.

**Struttura comune a tutti i tipi:**
- Segui l'ordine della lezione come ossatura
- Per ogni domanda aperta: rispondi inline come blocco citazione `>` immediatamente dopo il concetto a cui si riferisce
- Per ogni sezione omessa dagli appunti grezzi: includila con nota `> ⚠️ Questa sezione non era presente negli appunti grezzi.`
- Per ogni punto di forza di Lorenzo: `> ✅ Ottima osservazione...`

**Solo per SysAdmin e Security — aggiungi:**
- Per ogni bug identificato: mostra il codice errato, l'analisi dell'errore e la versione corretta
- Se il bug corrisponde a un pattern noto da errori_frequenti.md: `> ⚠️ Errore ricorrente: questo è lo stesso pattern di [modulo precedente]. Vedi errori_frequenti.md`

**Solo per Diritto — aggiungi:**
- Per ogni imprecisione giuridica: mostra la formulazione di Lorenzo, la correzione e il riferimento normativo esatto
- Alla fine: sezione "Domande di autoverifica — Risposte" con le risposte alle domande della lezione, se Lorenzo le ha incluse negli appunti grezzi

---

**5. Aggiorna errori_frequenti.md**

Se sono stati trovati bug o imprecisioni, aggiorna `stato/errori_frequenti.md`:
- Se il pattern esiste già: aggiungi il nuovo modulo alla riga esistente
- Se è un pattern nuovo: aggiungi una nuova riga nella sezione appropriata
- Se lo stesso tipo di errore appare in 3+ moduli: aggiungerlo come "Pattern Ricorrente"

---

**6. Aggiorna lo stato**

Aggiorna `stato/corrente.md`:
- Stato del modulo:
  - → ✅ solo se Lorenzo ha eseguito gli esercizi sulla VM (SysAdmin/Security) o ha risposto alle domande di autoverifica (Diritto) — verificarlo dagli appunti grezzi
  - → 🔄 altrimenti, con nota sullo stato interno
- Aggiorna la sezione "Prossimi Passi" se necessario

Aggiorna `stato/log_sessioni.md`:
- Nell'ultima voce del log aggiungi: "Appunti modulo `$ARGUMENTS` elaborati → `appunti_modulo$ARGUMENTS_<nome_breve>.md`"

---

**7. Verifica qualità (checklist interna)**

Prima di comunicare il risultato:
- [ ] Ogni domanda dagli appunti grezzi ha una risposta inline
- [ ] Nessuna sezione della lezione è stata saltata senza nota
- [ ] Bug/imprecisioni hanno analisi dettagliata (non solo la correzione)
- [ ] errori_frequenti.md è stato aggiornato se necessario
- [ ] Lo stato in corrente.md riflette la realtà (✅ solo con evidenza pratica)

Poi invoca la skill `lorenzo-skills:unicode-output-gate` per la verifica finale.

---

**8. Collega la nota al grafo**

Invoca la skill `lorenzo-skills:unicode-link-note` per scrivere il blocco AUTO-LINKS (fratelli + hub) dei nuovi appunti.

---

**9. Comunica il risultato**

Indica:
- Path del file creato
- Conteggio: domande risolte, bug/imprecisioni corrette, sezioni integrate, punti di forza segnalati
- Se il modulo è stato portato a ✅ o è rimasto 🔄 (con motivazione)
- Se sono stati trovati errori ricorrenti, menzionarli
