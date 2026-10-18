---
description: "Fissa insieme a Lorenzo le attività di studio del mese, della settimana o del giorno e le scrive con una data nella Plancia. Uso: /pianifica [mese] [settimana] [giorno|domani]"
argument-hint: "[mese] [settimana] [giorno|domani]"
---

> Regola di Lorenzo del 2026-10-08: **lo studio non resta mai senza data** e viene prima del
> lavoro e dello svago. Il mese si pianifica il giorno 1, la settimana il lunedì, il giorno dopo
> a `/chiudi`; se quel giorno non si apre una sessione, alla prima sessione successiva. Il
> briefing segnala in testa le pianificazioni dovute.

Ambiti da pianificare: `$ARGUMENTS`. Se vuoto, prendi quelli elencati in «Pianificazione dovuta»
nel briefing; se il briefing non ne elenca, chiedi a Lorenzo quale vuole fare. Si procede
**dall'ambito più largo al più stretto**: mese, poi settimana, poi giorno, perché ciascuno si
ricava dal precedente.

---

**1. Carica il contesto** *(il briefing è già in contesto: non rileggere ciò che contiene)*

- `piano/piano_laurea.md`: sessione in corso, appelli, checkpoint, regole del piano.
- `corsi/<COD>/percorso.md` di ogni esame attivo: moduli rimasti e punto di ripresa.
- La Plancia (URL nel `CLAUDE.md` di cockpit, protocollo e schema nel documento
  `meta/protocollo` del suo database): leggi con `ArtifactData` le
  collezioni `progetti` e `attivita`, per vedere cosa è già fissato e cosa è rimasto aperto.
  Le attività di studio aperte **senza data** vanno sistemate in questa esecuzione.

**2. Proponi, non imporre**

Per ogni ambito prepara una proposta e mostrala a Lorenzo **in un unico messaggio**:

- **Mese** — gli obiettivi d'esame del mese, per esame attivo: blocchi di programma da coprire
  (moduli o LAB per nome), checkpoint e prove a freddo che cadono nel mese, prenotazioni
  d'appello. Scadenza: il giorno in cui l'obiettivo deve essere raggiunto, al più tardi
  l'ultimo del mese.
- **Settimana** — 2-4 blocchi di programma per la settimana, ricavati dagli obiettivi del mese.
  Scadenza: il giorno previsto, al più tardi la domenica.
- **Giorno** (`giorno` = oggi, `domani` = domani) — 1-3 attività concrete e verificabili
  («`/lab FI2 LAB06` fino all'esercizio 3», non «studiare FI2»), ricavate dalla settimana e dal
  punto di ripresa. Scadenza: quel giorno.

Criteri, dalle regole del piano e dal profilo:
- disponibilità **molto variabile**: si pianifica programma coperto, mai ore; una giornata può
  avere una sola attività;
- il checkpoint o l'appello più vicino ha la precedenza (regole 1 e 4 di `piano_laurea.md`);
- i ripassi si fanno in blocco a ridosso dell'esame (regola 4b): non proporli giorno per giorno;
- un'attività che non ha ancora un giorno ragionevole prende comunque una data: l'ultimo giorno
  della settimana o del mese in cui va fatta.

**Giornata a ore** `[2026-10-19, richiesta di Lorenzo]` — quando l'ambito è `giorno` o `domani`,
oltre alle attività si divide il giorno in **blocchi orari** nella sezione *Giornata* della
Plancia (collezione `agenda`, schema e regole nel protocollo). Prima di proporre:
- leggi `agenda` di oggi e domani: i blocchi con `toccato: true` li ha spostati Lorenzo
  trascinandoli; digli cosa è cambiato e tienine conto;
- **chiedi a Lorenzo cosa ha intenzione di fare** quel giorno, in un solo messaggio di domande
  brevi: sveglia, impegni fissi e spostamenti, dove studia e fino a che ora, pasti, doccia e
  preparazione prima di uscire, svago, lavoro. Non chiedere ciò che ha già detto.
Poi proponi la giornata in una tabella `ora · cosa`, con lo studio nelle ore migliori e ogni
attività in scadenza quel giorno collocata in un blocco (o dichiarata senza orario).

**Attendi la risposta** e applica le correzioni di Lorenzo prima di scrivere. Se Lorenzo ha
chiesto di fare in autonomia, scrivi subito e mostragli il risultato.

**3. Scrivi nella Plancia** — un solo `batch` di `ArtifactData`

- attività nuove in `attivita`, id `studio-<COD>-<AAAA-MM-GG>-<slug>`, con
  `progetto` (id del corso: `fi2`, `calc`…), `scadenza`, `stato: "da fare"`, `priorita`,
  `note` (da dove viene: «obiettivo di ottobre», «settimana del 12/10»), `creata`, `aggiornata`
  e `piano`: `"mese"`, `"settimana"` o `"giorno"`;
- attività di studio già presenti e senza data: aggiornale con la data concordata
  (`if_version` della lettura al passo 1);
- se un corso non ha ancora un progetto in `progetti`, crealo (area `studio`, ordine 10-19).
- per `giorno`/`domani`: i blocchi in `agenda`, id `<AAAA-MM-GG>-<HHMM>`, con `attivita`
  quando il blocco serve un'attività, `piano_inizio`/`piano_fine` uguali a `inizio`/`fine` e
  `toccato: false`; nello stesso `batch` riallinea i blocchi `toccato` già letti.

**4. Registra la pianificazione** in `stato/pianificazione.md`, sostituendo solo le righe degli
ambiti fatti:

- `mese: AAAA-MM`, `settimana: <lunedì della settimana, AAAA-MM-GG>`,
  `giorno: <ultimo giorno pianificato, AAAA-MM-GG>`.

Poi una riga in `stato/giornata.md`: `HH:MM · PIANO · pianificati <ambiti>: <n> attività nella Plancia`
e una voce nel `diario` della Plancia (area `studio`).

**5. Conferma** — un elenco compatto per giorno di ciò che è stato fissato, e il link alla Plancia.
