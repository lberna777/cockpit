---
description: "Genera la guida-lab operativa per un modulo dalle fonti del corso (passo 3 del flusso). Uso: /lab <CODICE> <ID>"
argument-hint: "<CODICE> <ID modulo> — es. LAS 3D, FI2 02x, FI2 LAB02"
---

Il parametro passato è: "$ARGUMENTS"

---

**0. Risolvi corso e modulo**

`$ARGUMENTS` va letto come **due token**: `<CODICE> <ID modulo>`.

- Primo token → codice corso, validato contro `piano/codici.txt`.
- Secondo token → identificativo del modulo.
- Se manca un token o il codice non è valido: mostra i codici da `codici.txt` e fermati.
- Se il corso non prevede né laboratorio né esercizi svolti (lo dice `corsi/<COD>/percorso.md`
  o `piano/piano_laurea.md`): comunicalo e fermati — per quel corso esiste solo `/lezione`.

---

**1. Carica il contesto necessario**

In parallelo:
- `corsi/<COD>/percorso.md` — nome completo, materiale richiesto, esercizio attivo
- `corsi/<COD>/fonti.md` — gerarchia delle fonti e cosa manca
- `profilo/errori.md` — pattern ricorrenti rilevanti per questo modulo
Lo stato dell'esame attivo è già nel briefing: non rileggerlo.

Se il modulo non esiste nel percorso, comunicalo e fermati.

---

**2. Identifica e verifica le fonti**

Da `percorso.md` recupera i nomi esatti dei materiali del modulo — sia la parte teorica sia la
parte di laboratorio o eserciziario — e verificali in `corsi/<COD>/materiali/`.

Se uno o più mancano: **fermati**, elenca i titoli esatti da procurare e chiedi a Lorenzo. Non
generare contenuto senza aver letto le fonti.

---

**3. Leggi le fonti**

Leggi integralmente i materiali del modulo.

> **REGOLA CRITICA**: il contenuto della guida-lab deve venire SOLO dalle fonti lette in questo
> passo. I "concetti chiave" in `percorso.md` sono un indice per trovare le fonti, non una
> fonte da cui generare contenuto. Non inventare esercizi, comandi, output o passaggi che non
> siano nel materiale.

---

**4. Genera la guida-lab**

Path: `corsi/<COD>/lezioni/guida_lab_<ID>_<nome_breve>.md`

**Scelta del template** — dal tipo di verifica in `fonti.md`, non dal nome del corso:

| Tipo di verifica | Template |
|---|---|
| pratico-lab su macchina (es. `LAS`) | laboratorio su macchina |
| esercizi di calcolo o dimostrazione (es. `CA`, `ELT`, `MATAP`) | esercizi formali |
| codice che compila e passa i test, con startkit (es. `FI2`) | progetto a oggetti con startkit e test |

Per il terzo template, prima di scrivere:
- Da `percorso.md`, sezione *Mappa teoria → pratica*, ricava i **prerequisiti di teoria** della
  voce. Se uno è ancora ⬜, non fermarti ma dichiaralo in testa alla guida, con il modulo mancante.
- Leggi **per intero** le slide o il testo della voce e **lo startkit, test compresi**: i test
  sono il contratto. Scompatta gli zip nella scratchpad, non in `materiali/`.
- La **soluzione** del docente si legge solo per controllare che i suggerimenti portino a una
  strada che funziona. **Non se ne riporta codice nella guida, mai**, né a parole un algoritmo
  che Lorenzo dovrebbe trovare da sé.

---

### Template — laboratorio su macchina

```
# Guida Lab — <COD> <ID>: <Nome Completo>
**Corso**: <nome esteso da piano/codici.txt>
**Materiale**: <titoli delle fonti usate>
**Ambiente**: <VM o toolchain, con il comando esatto per avviarla — da corsi/<COD>/percorso.md>
**Prerequisiti**: <moduli precedenti rilevanti>

---

## Setup

> ⚠️ **Snapshot prima di ogni esercizio distruttivo o di compromissione**, dove l'ambiente lo
> prevede.

Passi da eseguire prima di iniziare:
1. ...

---

## Threat model *(solo per i corsi dove la sicurezza è il tema)*

- **Prospettiva attaccante**: cosa si cerca, perché la tecnica funziona
- **Prospettiva difensore**: come si rileva, come si mitiga

---

## Esercizi

> Lorenzo digita tutti i comandi. La guida li fornisce, non li esegue.

Per ogni esercizio della fonte, struttura fissa:

### Esercizio N — <Titolo dalla fonte>

**Obiettivo**: cosa deve funzionare al termine di questo esercizio.

**Concetto minimo**: cos'è e perché esiste — solo la teoria necessaria per capire cosa stai
facendo.
*(Se Lorenzo ha errori ricorrenti su questo concetto: ⚠️ con il pattern da profilo/errori.md)*

**Comandi**:
```bash
# comando esatto da digitare
```

**Anatomia del comando**: per ogni comando — *cosa stai scrivendo* (cosa fa), *perché lo stai
scrivendo* (a cosa serve qui: quale informazione cerchi o quale pezzo dell'esercizio risolve,
nella catena «che informazione ho → cosa cerco → quale comando la trova»), *con che parametri*
(la funzione di ogni flag o opzione usata) e *come potresti scriverlo* (varianti equivalenti o
adattamenti a un caso simile). Serve a saperlo riscrivere a memoria all'esame, non a copiarlo.
Spiega solo comandi presenti nelle fonti, ma spiega i parametri in modo accurato e completo.

**Output atteso**:
```
# output tipico da confrontare
```

**Cosa verificare**: come sai che ha funzionato.

---

[Progressione: facile → difficile, nell'ordine della fonte]

## Deliverable da catturare

*(Solo se l'ambiente viene ripristinato a fine sessione — snapshot, revert, container
effimero.)* Elenco preciso dei file e degli screenshot da salvare **sull'host durante**
l'esercizio, non a fine lavoro: quando l'ambiente torna pulito, quel che non è uscito è perso.

## Connessioni

- Con il modulo precedente: [connessione SPECIFICA — cita modulo e concetto preciso]
- Con i corsi in catena da `piano/piano_laurea.md`: [essere precisi]
```

---

### Template — esercizi formali (calcolo, dimostrazioni)

```
# Guida Esercizi — <COD> <ID>: <Nome Completo>
**Corso**: <nome esteso>
**Materiale**: <titoli delle fonti usate>
**Prerequisiti**: <moduli e corsi in catena>

---

## Esercizi

> Lorenzo svolge i passaggi. La guida li imposta, non li risolve al posto suo.

### Esercizio N — <Titolo dalla fonte>

**Obiettivo**: quale classe di problemi allena.

**Concetto minimo**: la proprietà o il teorema che rende lecito il procedimento.
*(⚠️ errori ricorrenti da profilo/errori.md dove rilevanti.)*

**Impostazione**: i dati, cosa si cerca, quale strada si sceglie e **perché quella** —
nella catena «che dati ho → cosa cerco → quale strumento li collega».

**Passaggi**:
```
# lo svolgimento, un passaggio per riga
```

**Anatomia del passaggio**: per ogni passaggio non banale — *cosa stai facendo*, *perché lì*,
*quale ipotesi stai usando* e *cosa cambierebbe se l'ipotesi cadesse*. Serve a saper
ricostruire il procedimento all'esame, non a ricopiarlo.

**Risultato atteso**: il valore o la forma finale, con le unità.

**Come verificarlo**: il controllo indipendente — ordine di grandezza, caso limite,
sostituzione all'indietro.

---

[Progressione: dall'esercizio più semplice al più complesso, nell'ordine della fonte]

## Errori che questo esercizio intercetta
I punti dove il procedimento si rompe di solito, e il segnale che rivela lo sbaglio.
```

---

### Template — progetto a oggetti con startkit e test

> **`[2026-09-30, su richiesta di Lorenzo]` Scheda + chat, non guida.** Per `FI2` il lavoro si fa
> sui test dello startkit, **accompagnati in chat**: Claude legge i file di Lorenzo e lancia i test
> dal disco, dà suggerimenti a gradini (① concetto e pagina di slide → ② pseudocodice → ③ frammento
> del costrutto, mai il metodo richiesto) e, quando compare un costrutto nuovo, 5–10 righe su quello
> solo. Il file prodotto da `/lab` è una **scheda di una pagina (≤ 40 righe)** da tenere accanto
> a Eclipse, non una guida: la guida da 900 righe della 02x è il caso da non ripetere.
> I moduli di teoria che la voce richiede **non si aprono con `/lezione`**: entrano qui, quando
> servono, e si chiudono con la voce.
>
> Una voce pratica si chiude quando i suoi test passano, **anche se svolta con guida**
> (`CLAUDE.md` §7.2, decisione di Lorenzo del 2026-09-30): la guida si annota come «guidato» in
> `stato/corrente.md`. La scheda imposta il lavoro e si ferma prima dell'implementazione.
>
> **Due modalità, dalla colonna *Tipo* della mappa in `percorso.md`:**
> - **guidata** — esercitazioni `x`/`z`, `LAB` guidati, esercizi `ES-`: scheda completa;
> - **compito** — `LAB` in forma di compito (es. `LAB12`, `LAB13`) e prove d'esame: solo *Setup*
>   e *Condizioni della prova*; in chat nessun aiuto durante, confronto con la soluzione dopo.

```
# Scheda — <COD> <ID>: <Nome Completo>
**Materiale**: <slide/testo, startkit — nomi esatti> · **Modalità**: guidata | compito
**Teoria che entra qui**: <moduli dalla mappa, con la pagina di slide da tenere aperta>

## Setup
- importa lo startkit, **rinomina il progetto** (all'esame è richiesto), package da rispettare;
- configurazione di esecuzione se la fonte la richiede; le X rosse iniziali e perché.

## Ordine di lavoro
| # | Classe | Cosa rappresenta (1 riga) | Test che la coprono | Costrutto nuovo → slide |
|---|---|---|---|---|

## Casi limite da pensare
- Solo come **domande**, dalla fonte e dai test. (⚠️ la classe è finita quando passano tutti i
  test, non il primo — `profilo/errori.md` pattern 2.)

## Test rosso?
Non compila (firma/nome/package) · failure (logica: guarda il caso del test) · error
(eccezione durante l'esecuzione: guarda lo stack trace) → prontuario §1, oppure scrivilo in chat.

## Dopo i test verdi
- copia il progetto in `corsi/FI2/esame_FI2/svolti/<ID>_<Nome>/`;
- apri la soluzione del docente e confronta: rappresentazione interna, casi limite, metodi privati;
- Claude scrive `svolti/<ID>_<Nome>/confronto_<ID>.md`: per ogni differenza fra il codice di Lorenzo
  e la soluzione del docente, i due frammenti, *migliore* (motivato, onesto) e *da seguire* (sempre
  il docente); in fondo *Cosa porto via*. Modello: `svolti/LAB02_Frazione/confronto_LAB02.md`
  `[2026-09-30, su richiesta di Lorenzo]`;
- `/chiudi` aggiorna il prontuario con ciò che hai incontrato.

## Condizioni della prova *(solo modalità compito)*
Tempo massimo e punteggio per parte, dalla fonte; cronometro; al termine, test passati per parte.
```

---

## Famiglia d'esame

*(Solo se il modulo è marcato ⭐ nel percorso — altrimenti ometti la sezione.)*

```
Tipologia: <nome della tipologia d'esame>
Prova passata correlata: `corsi/<COD>/prove/<file>` — eseguila al termine del lab.
```

---

**5. Verifica qualità (checklist interna)**

- [ ] Ancorata alle fonti reali: nessun contenuto inventato, `[fonte: ...]` dove serve
- [ ] Setup esplicito: ambiente corretto, snapshot dove previsto
- [ ] Ogni passo: comando o passaggio esatto + risultato atteso + come verificarlo
- [ ] Ogni comando o passaggio ha l'**anatomia**: cosa fa, perché lì, funzione dei parametri o
      delle ipotesi, varianti (saperlo riscrivere, non copiare)
- [ ] Threat model a due prospettive, dove il corso lo richiede
- [ ] Progressione facile → difficile, nell'ordine della fonte
- [ ] Deliverable dichiarati, se l'ambiente viene ripristinato
- [ ] Errori frequenti di Lorenzo integrati come ⚠️ dove rilevanti
- [ ] Se ⭐: tipologia d'esame e rimando alla prova passata
- [ ] **Lorenzo digita i comandi: la guida non li esegue al suo posto**
- [ ] *Progetto con startkit*: nessun corpo di metodo né algoritmo della soluzione nella guida;
      frammenti solo entro i gradini ammessi e solo da slide, con `[fonte: ...]`
- [ ] *Progetto con startkit*: firme e nomi di package coincidono con quelli dei test dello
      startkit (verificati leggendo i test, non dedotti)
- [ ] *Progetto con startkit, modalità compito*: niente analisi, contratti né suggerimenti

Se un punto non è soddisfatto, correggi prima di procedere. Poi invoca
`lorenzo-skills:unicode-output-gate`.

---

**6. Collega la nota al grafo**

Invoca `lorenzo-skills:unicode-link-note`: la nota riceve in testa il frontmatter
`tags: [<COD>, guida-lab]`, e se è la prima nota del corso si aggiunge il suo gruppo colore in Obsidian.

---

**7. Registra l'evento**

Appendi a `stato/giornata.md`:

```
HH:MM · <COD> · guida-lab <ID> generata.
```

Se `<COD>` è il corso attivo, porta il modulo a "in corso" in `stato/corrente.md`.

---

**8. Comunica il risultato**

- Path del file creato
- Indica di aprire l'ambiente e seguire gli esercizi nell'ordine della guida
- Ricorda i deliverable da catturare durante il lavoro, se ce ne sono
- Se sono stati integrati avvertimenti da `profilo/errori.md`, menzionalo brevemente
