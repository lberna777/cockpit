---
description: "Crea la lezione strutturata per un modulo dai materiali del corso. Uso: /lezione <CODICE> <ID>  (es. /lezione FI2 3A)"
argument-hint: "<CODICE> <ID modulo> — es. FI2 3A, SO 2B, CA 4"
---

Il parametro passato è: "$ARGUMENTS"

---

**0. Risolvi corso e modulo**

`$ARGUMENTS` va letto come **due token**: `<CODICE> <ID modulo>`.

- Primo token → codice corso. Validalo contro `piano/codici.txt`, che è la fonte unica.
- Secondo token → identificativo del modulo dentro quel corso.
- Se manca un token, o il codice non è in `codici.txt`: mostra i codici validi presi dal file
  (non da una lista cablata qui) e fermati.

Da qui in avanti, nel testo: `<COD>` = codice corso, `<ID>` = identificativo modulo.
La radice del corso è `corsi/<COD>/`.

---

**1. Carica il contesto necessario**

Leggi questi file in parallelo:
- `corsi/<COD>/percorso.md` — nome completo del modulo, materiale richiesto, concetti chiave,
  esercizio attivo, connessioni. Se il corso non ha ancora un `percorso.md`, comunicalo e
  fermati: il corso non è aperto.
- `corsi/<COD>/fonti.md` — gerarchia delle fonti e, soprattutto, **cosa manca**.
- `profilo/errori.md` — pattern di errore ricorrenti rilevanti per questo modulo. La sezione
  **trasversale** vale su ogni corso, anche uno mai aperto prima.
Lo stato dell'esame attivo è già nel briefing: non rileggerlo.

Se il modulo non esiste nel percorso, comunicalo e fermati.

---

**2. Verifica i materiali**

Da `percorso.md` recupera i nomi esatti dei materiali assegnati al modulo e verificali in
`corsi/<COD>/materiali/`.

Usa **solo i materiali assegnati al modulo nel percorso** — non riclassificare di tua
iniziativa, non attingere ai materiali di altri moduli. Se uno o più mancano: **fermati**,
elenca i titoli esatti da procurare e chiedi a Lorenzo. Non creare contenuto senza la fonte.

> **Esami arretrati**: se `fonti.md` segnala che il materiale disponibile è di un'annata
> diversa da quella in cui il corso era in piano, dichiaralo in testa alla lezione e segnala
> ogni punto in cui il programma risulta cambiato.

---

**3. Leggi le fonti**

Leggi integralmente i materiali rilevanti. Per documenti molto lunghi (>50 pagine), leggi per
sezioni e individua le parti pertinenti al modulo.

> **REGOLA CRITICA**: il contenuto della lezione deve venire SOLO dalle fonti lette in questo
> passo. I "concetti chiave" in `percorso.md` sono un indice per sapere quali fonti cercare —
> NON sono una fonte da cui generare contenuto. Se non hai letto la fonte, non puoi creare la
> lezione. Contenuto generato senza leggere la fonte è superficiale e inaccettabile. Non
> inventare comandi, strumenti, formule o norme che non siano nel materiale.

---

**4. Scegli il registro in base al tipo di verifica**

Da `percorso.md` (o da `piano/piano_laurea.md`) ricava il tipo d'esame del corso e applica il
template corrispondente. I tre registri sono in `CLAUDE.md` §7.2.

**FORMATO per i corsi con laboratorio pratico** — vincolante, da feedback di Lorenzo:

La lezione è **prosa discorsiva ancorata ai comandi/file concreti**, NON un walkthrough.
- **Prosa scorrevole**, non tabelle o elenchi a raffica. Si legge la sera prima.
- **Organizzata attorno ai comandi/file concreti**, usati come ganci per spiegare la teoria.
- Per ciascuno, **due livelli**: *cosa c'è dietro in piccolo* (il meccanismo) + *la visione
  d'insieme in grande* (dove si inserisce, perché esiste, quale superficie apre).
- **NON è un walkthrough**: niente sequenza "passo 1 → passo 2 → output atteso", niente
  anatomia parametro-per-parametro. Quella è la **guida-lab** (`/lab`). La lezione spiega
  *perché*; la guida-lab dice *come, passo passo*.

> Confine col walkthrough: se stai scrivendo "esegui questo, poi quello, output X" → è materia
> di `/lab`, non della lezione.

**Per i corsi con esercizi formali** (calcolo, dimostrazioni, progetto): la prosa si ancora ai
**procedimenti** invece che ai comandi. Per ciascuno, gli stessi due livelli: il meccanismo che
lo fa funzionare, e il posto che occupa nella teoria. Gli esercizi svolti passo-passo sono
materia di `/lab`.

**Per i corsi discorsivi con un docente di riferimento** (giuridici, e ogni corso dove conta la
formulazione): la terminologia della fonte va **riprodotta, non parafrasata**. Nessuna
integrazione da fonti esterne. `[fonte: <fonte>]` su ogni affermazione ripresa alla lettera.

---

**5. Crea il file lezione**

Path: `corsi/<COD>/lezioni/lezione_<ID>_<nome_breve>.md`

`<nome_breve>` = identificatore conciso del contenuto (es. `ricorsione`, `systemd_servizi`).

---

### Template — corso con laboratorio pratico

```
# Lezione — <COD> <ID>: <Nome Completo>
**Corso**: <nome esteso da piano/codici.txt>
**Materiale**: <titoli delle fonti usate>
**Prerequisiti**: <moduli precedenti rilevanti — verificarne lo stato nel percorso>

---

## Obiettivo
Una frase: cosa Lorenzo deve saper fare al termine.

## [Sezioni ancorate ai comandi/file chiave] — in prosa

Una sezione per ogni comando o file concreto centrale del modulo.
Per ciascuno, in prosa discorsiva:
- **cosa fa** (il gesto pratico)
- **cosa c'è dietro** (il meccanismo, in piccolo)
- **la visione** (dove si inserisce, perché esiste, quale superficie introduce)
*(Se Lorenzo ha errori ricorrenti su questo da profilo/errori.md: ⚠️ con il pattern specifico.)*

> NON mettere qui la sequenza di esecuzione passo-passo né l'anatomia parametro-per-parametro:
> quella è la guida-lab (`/lab`).

## Connessioni
- Con il modulo precedente: [connessione SPECIFICA, non generica]
- Con altri corsi in catena: [quale dipendenza da piano/piano_laurea.md — essere precisi]

## Riepilogo
3 concetti chiave in forma di domanda-risposta (non lista passiva)
```

---

### Template — corso con esercizi formali

```
# Lezione — <COD> <ID>: <Nome Completo>
**Corso**: <nome esteso>
**Materiale**: <titoli delle fonti usate>
**Prerequisiti**: <moduli e corsi in catena>

---

## Obiettivo
Una frase: quale classe di problemi Lorenzo deve saper risolvere al termine.

## [Sezioni ancorate ai procedimenti chiave] — in prosa

Una sezione per ogni procedimento centrale del modulo.
Per ciascuno, in prosa discorsiva:
- **cosa produce** (il risultato che dà)
- **cosa c'è dietro** (perché funziona: il teorema, l'invariante, la proprietà che lo regge)
- **la visione** (quando si applica e quando no, e quale ipotesi lo rompe)
*(⚠️ errori ricorrenti da profilo/errori.md dove rilevanti.)*

> Gli esercizi svolti passo-passo sono materia di `/lab`, non della lezione.

## Casi limite
I casi in cui il procedimento non si applica, e come li si riconosce.

## Connessioni
- Con il modulo precedente e con i corsi in catena: [specifiche]

## Riepilogo
3 concetti chiave in forma di domanda-risposta
```

---

### Template — corso discorsivo con docente di riferimento

> **Regola vincolante**: l'esame verte sugli argomenti e le spiegazioni della fonte del
> docente. Le definizioni devono rispecchiarne il linguaggio — non riformulare, non
> parafrasare, non integrare con fonti esterne. Segnalare con `[fonte: <fonte>]` ogni
> affermazione tratta dal materiale. Registro accademico. Usare paragrafi discorsivi dove la
> fonte lo fa.

```
# Lezione — <COD> <ID>: <Nome Completo>
**Corso**: <nome esteso>
**Materiale**: <titolo della fonte usata>
**Riferimenti**: <norme, teoremi o testi citati, con estremi completi>

---

## Obiettivo
Una frase: cosa Lorenzo deve saper esporre, nelle parole del docente.

## Quadro di riferimento
Le fonti normative o teoriche con estremi completi. Solo quelle presenti nel materiale.

## Concetti Chiave
Per ogni concetto:
- Definizione ripresa fedelmente dalla fonte [fonte: <fonte>]
- La ratio, se il docente la spiega
- Gli esempi usati nel materiale
- Se Lorenzo ha pattern di errore su questo tipo di concetto: "⚠️ Attenzione: in passato hai
  confuso X con Y"

## Tabella dei riferimenti
| Riferimento | Contenuto (come descritto nella fonte) | Rilevanza per il corso |
|---|---|---|

## Casi e Scenari
Situazioni concrete portate dal docente. Se non presenti nella fonte, omettere.

## Domande di Autoverifica
Cinque domande aperte del tipo che il docente potrebbe fare all'esame.
Almeno una deve testare le distinzioni che Lorenzo tende a fondere (da profilo/errori.md).

## Riepilogo
Tre concetti centrali, formulati come nella fonte.
```

---

**Se il corso ha un quiz a punteggio negativo**: aggiungi in testa la nota sul peso della prova
e chiudi le autoverifiche con l'avvertenza — *se non sei sicuro, all'esame non rispondere*.

---

**6. Verifica qualità (checklist interna)**

- [ ] Ogni concetto della fonte è stato coperto
- [ ] Corsi pratici: **prosa ancorata ai comandi/file**, ogni comando a due livelli (meccanismo
      + visione) — NON un walkthrough, niente sequenza passo-passo né anatomia parametri
- [ ] Corsi formali: ogni procedimento ha il perché funziona e i casi limite
- [ ] Corsi discorsivi: terminologia esatta della fonte, `[fonte: ...]` dove serve
- [ ] Le connessioni sono specifiche (citano moduli, corsi e concetti precisi)
- [ ] Pattern di errore di Lorenzo integrati come ⚠️
- [ ] Nessun comando, formula o norma inventata fuori dalle fonti

Se una voce non è soddisfatta, correggi prima di procedere. Poi invoca
`lorenzo-skills:unicode-output-gate` per la verifica finale.

---

**7. Collega la nota al grafo**

Invoca `lorenzo-skills:unicode-link-note` per scrivere il blocco AUTO-LINKS della nuova lezione.

---

**8. Registra l'evento**

Appendi a `stato/giornata.md`:

```
HH:MM · <COD> · lezione <ID> creata da <n> fonti.
```

Se `<COD>` è il corso attivo, aggiorna anche lo stato del modulo in `stato/corrente.md`
(da "non iniziato" a "in corso").

---

**9. Comunica il risultato**

- Path del file creato
- Per i corsi con laboratorio: ricorda che l'esecuzione è la guida-lab (`/lab <COD> <ID>`),
  passo separato del flusso
- Per i corsi discorsivi: ricorda di rispondere alle domande di autoverifica prima di scrivere
  gli appunti grezzi
- Se sono stati integrati avvertimenti da `profilo/errori.md`, menzionalo brevemente
