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

> **Perché è diverso dagli altri due.** Qui il «passaggio esatto» è il codice, e il codice è la
> soluzione. Un modulo si chiude solo su un esercizio risolto **a freddo** (`CLAUDE.md` §7.2):
> una guida che detta le classi lo rende impossibile. La guida quindi imposta il lavoro con il
> metodo dei LAB del docente — dominio → modello → classi nell'ordine delle dipendenze → test —
> e si ferma prima dell'implementazione.
>
> **Due modalità, dalla colonna *Tipo* della mappa in `percorso.md`:**
> - **guidata** — esercitazioni `x`/`z`, `LAB` guidati, esercizi `ES-`: template completo;
> - **compito** — `LAB` in forma di compito (es. `LAB12`, `LAB13`) e prove d'esame: solo
>   *Setup*, *Condizioni della prova* e *Dopo la prova*. Niente analisi, contratti né
>   suggerimenti: è una simulazione, e la guida non deve servire da aiuto durante.

```
# Guida Lab — <COD> <ID>: <Nome Completo>
**Corso**: <nome esteso>
**Materiale**: <slide/testo, startkit, soluzione — nomi esatti da percorso.md>
**Modalità**: guidata | compito
**Prerequisiti di teoria**: <dalla mappa, con stato; ⚠️ quelli ancora ⬜>

---

## Setup

Dalle slide del laboratorio e da `LAB02` (procedura d'esame):
- importazione dello startkit in Eclipse e **rinomina del progetto** — all'esame è richiesta;
- cartelle sorgenti (`src`, `test`) e package attesi: **i nomi vanno rispettati**, o i test non
  compilano;
- configurazione di esecuzione quando la fonte la richiede (`-ea`, VM JavaFX);
- «le X rosse sono normali»: quali classi mancano all'inizio e perché il progetto non compila.

## Il dominio

In prosa, dalla fonte: di cosa parla il problema, i termini del dominio e il loro significato
preciso, le ipotesi semplificative dichiarate. Dove la fonte pone domande di analisi («cos'è
esattamente un appuntamento?»), riportarle **senza risposta**: sono la prima cosa da fare.
*(⚠️ distinzioni fra termini vicini del dominio, da `profilo/errori.md` pattern 1.)*

## Il modello

- Le classi e le loro relazioni come le dà la fonte (UML o testo): cosa è **fornito** nello
  startkit e cosa è **da fare**.
- **Ordine di lavoro**: dalla classe con meno dipendenze a quella con più — dalla fonte se lo
  indica, altrimenti ricavato dal modello, dicendo da cosa.

## Classi da realizzare — una sezione per classe, nell'ordine sopra

### <NomeClasse>

**Responsabilità**: cosa rappresenta e cosa fa, in una o due frasi, dalla fonte.

**Contratto**: costruttori e metodi richiesti **con firma esatta** (dalla specifica, dall'UML
o dai test), e per ciascuno cosa deve garantire: valori restituiti, stato, eccezioni attese.
Nessun corpo di metodo.

**Test che la coprono**: la classe di test e i metodi di test dello startkit, e cosa verifica
ciascuno, in una riga. Suggerire l'ordine in cui togliere i commenti ai test, metodo per metodo.

**Casi limite da pensare prima di scrivere**: quelli che la fonte segnala («cosa succede intorno a
mezzanotte?») e quelli che i test esercitano. Formulati come **domande**, non come risposte.
*(⚠️ pattern 2 di `profilo/errori.md`: la classe è finita quando passano tutti i test, non il
primo.)*

**Frammenti di codice** — *solo nei LAB fino a `LAB04` compreso e nelle esercitazioni `x`
collegate a moduli fino a `07`, e solo per costrutti che Lorenzo usa per la prima volta*:
un frammento breve del **costrutto**, preso dalle slide di teoria o del laboratorio e citato con
`[fonte: <file>, sl. N]`, mai dalla soluzione e mai il metodo richiesto. Esempio lecito: la
forma del costruttore ausiliario con `this(n, 1)` (LAB02 sl. 6), dove il laboratorio stesso la
mostra. Oltre questi gradini, la sezione si omette.

<details><summary>Se sei bloccato — 1: una domanda</summary>

Una domanda che sposta l'attenzione sul punto giusto, senza nominare la soluzione.
</details>

<details><summary>Se sei bloccato — 2: l'idea</summary>

L'idea o la struttura dati da usare, a parole, **presa dai suggerimenti della fonte** quando ci
sono (es. le due strategie per contare i piolini bianchi in LAB06). Mai codice.
</details>

---

## Leggere un test rosso

Da riprendere a ogni esecuzione dei test:
- **non compila** → nessun test gira: firma, nome o package diversi da quelli attesi;
- **failure** → il codice gira ma l'asserzione non torna: l'errore è nella logica, cercare il caso
  del test;
- **error** → un'eccezione imprevista **durante l'esecuzione**, l'asserzione non è raggiunta:
  cercare lo stack trace.
*(⚠️ `profilo/errori.md`, `FI2`: compilazione ed esecuzione fuse, error collocato «nella
struttura».)*

## Dopo i test verdi — confronto con la soluzione

Solo ora si apre la soluzione del docente. La guida elenca **cosa guardare**, non cosa c'è:
scelte di rappresentazione interna, gestione dei casi limite, divisione in metodi privati.
Ciò che manca nel proprio codice va in `stato/giornata.md` e, se ricorre, in `profilo/errori.md`.

## Condizioni della prova *(solo modalità compito)*

Tempo massimo e punteggio per parte, dalla fonte. Regola: nessuna guida, nessuna soluzione,
nessun aiuto durante; cronometro. Al termine: quanti test passano, per parte.

## Dopo la prova *(solo modalità compito)*

Confronto con la soluzione del docente come sopra, più: quali parti hanno richiesto più tempo
e perché. Una prova sotto i 2/3 dei test è un dato, non un fallimento: va registrata.

## Connessioni

- Con la teoria: quali concetti dei moduli prerequisito compaiono e **dove** (classe, metodo).
- Con i LAB precedenti: cosa si riusa (es. `MyMath` da LAB01 in LAB02).
- Con le prove: la tipologia d'esame e la prova passata correlata, se la mappa la indica.
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
