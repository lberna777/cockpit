---
description: "Genera la guida-lab operativa per un modulo dalle fonti del corso (passo 3 del flusso). Uso: /lab <CODICE> <ID>"
argument-hint: "<CODICE> <ID modulo> — es. LAS 3D, FI2 2A"
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

### Template — esercizi formali (calcolo, dimostrazioni, progetto)

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

Se un punto non è soddisfatto, correggi prima di procedere. Poi invoca
`lorenzo-skills:unicode-output-gate`.

---

**6. Collega la nota al grafo**

Invoca `lorenzo-skills:unicode-link-note` per il blocco AUTO-LINKS della guida-lab.

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
