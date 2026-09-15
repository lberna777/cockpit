# Piano di laurea — Ingegneria Informatica T

> Strato **permanente**. Cambia nell'ordine dei mesi, e ogni cambiamento è una decisione
> presa, non un aggiustamento. Si emenda, non si riscrive: quando una scelta viene superata,
> si marca `[superato AAAA-MM]` e si aggiunge quella nuova, con la ragione.
>
> Redatto il 2026-09-02. Sostituisce `ESAMI SCELTI.md`, che serviva una sola sessione.
> Emendato il 2026-09-14: ripartizione rivista per propedeuticità di `LAS`.

## Il conto

| Voce | CFU |
|---|---|
| Acquisiti | 81 |
| Dodici esami rimanenti | 96 |
| Prova finale | 3 |
| **Totale** | **180** |

Media di laurea alla data: **92,4 / 110**.

> I 3 CFU della prova finale sono dedotti per differenza (180 − 81 − 96). Verificare sul piano
> di studi ufficiale prima di farci affidamento per il calcolo di una scadenza.

## Orizzonte

Laurea nella **sessione estiva 2028**. Tre sessioni d'esame e un elaborato.

### Ripartizione vigente — decisa il 2026-09-14

| Fase | Finestra | CFU | Esami |
|---|---|---|---|
| **S1** | 19 dic 2026 – 14 feb 2027 | 30 | FI2, CALC, MATAP, **ELT** |
| **S2** | 5 giu – 10 set 2027 | 36 | SO, IDS, TLC, **RETI** |
| **S3** | gennaio–febbraio 2028 | 30 | CA, WEB, ELN, **LAS** |
| **Elaborato** | primavera 2028 | 3 | prova finale |
| **Laurea** | sessione estiva 2028 | — | — |

### Ripartizione precedente `[superato 2026-09]`

| Fase | Finestra | CFU | Esami |
|---|---|---|---|
| S1 | gennaio–febbraio 2027 | 30 | FI2, CALC, MATAP, LAS |
| S2 | giugno–luglio 2027 | 33 | SO, IDS, TLC, ELT |
| S3 | gennaio–febbraio 2028 | 33 | CA, RETI, WEB, ELN |

**Perché è cambiata.** La pagina ufficiale dell'insegnamento dichiara, fra le conoscenze
richieste in ingresso di `LAS`, che *Reti di calcolatori e Sistemi Operativi sono
indispensabili per poter fruire dei contenuti* del corso. Nella ripartizione precedente
`LAS` stava in S1, cioè **prima di entrambi i suoi prerequisiti** — `SO` in S2 e `RETI` in
S3. Non era un problema di carico: era una collocazione contro la propedeuticità dichiarata,
e coincide con la ragione per cui la preparazione di giugno 2026 si è arenata sulla parte
teorica, che è a libro chiuso e poggia su quei due corsi.

Tre spostamenti, ciascuno con la sua ragione:

- `LAS` **da S1 a S3**: arriva dopo `SO` e `RETI`, che sono ora entrambi in S2. Questa è la
  destinazione nominata che la regola 3 richiede, non un rinvio.
- `RETI` **da S3 a S2**: `RETI` non ha code che dipendono da lui, quindi anticiparlo è gratuito
  in termini di catene, ed è ciò che rende possibile la collocazione di `LAS`.
- `ELT` **da S2 a S1**: è testa di catena verso `ELN`, quindi anticiparlo non ipoteca niente
  ed è l'unico esame da 6 CFU che guadagna a stare prima. Prende il posto lasciato da `LAS`
  e tiene S1 a 30 CFU, cioè al carico già ritenuto sostenibile.

Fonte delle finestre di sessione e della propedeuticità, consultate il 2026-09-14:
`corsi.unibo.it/laurea/IngegneriaInformatica/calendario-didattico` e la scheda
dell'insegnamento 434713 su `unibo.it`.

I codici e i CFU per esame stanno in `piano/codici.txt`, che è la fonte unica: qui non si
duplicano, si raggruppano.

### Date degli appelli

> **Da compilare.** Il calcolo delle settimane rimanenti in `/piano`, `/stato` e `/lacune`, e
> con esso il checkpoint delle sei settimane, dipende da queste date. Finché la riga è vuota,
> quei comandi ragionano sulla finestra di sessione e non sul singolo appello, con un margine
> d'errore di settimane.
>
> `[2026-09-14]` Rilevato che in AlmaEsami le date sono visibili solo per gli appelli con
> prenotazione aperta: quelle di S1 compariranno avvicinandosi alla sessione. Regola empirica
> nota a Lorenzo, non verificata su fonte: due o tre appelli per insegnamento a sessione.
> Da riempire appena le prenotazioni si aprono, esame per esame.

| Esame | Primo appello utile | Secondo appello | Fonte |
|---|---|---|---|
| FI2 | — | — | — |
| CALC | — | — | — |
| MATAP | — | — | — |
| ELT | — | — | — |
| SO | — | — | — |
| IDS | — | — | — |
| TLC | — | — | — |
| RETI | — | — | — |
| CA | — | — | — |
| WEB | — | — | — |
| ELN | — | — | — |
| LAS | — | — | — |

**Appelli straordinari**: sulla pagina del calendario didattico non risultano menzionati. Non
si dà per esistente finché non è verificato in segreteria o sul regolamento del corso di
studi: è la destinazione su cui la regola 3 si appoggerebbe in caso di un secondo taglio.

## Catene di dipendenza

Un esame in testa a una catena non si sposta: ritardarlo ritarda tutto ciò che gli sta sotto,
anche a sessioni di distanza.

```
FI2  (S1) ──┬──→ IDS  (S2)
            └──→ WEB  (S3)
CALC (S1) ─────→ SO   (S2) ──┐
MATAP(S1) ─────→ CA   (S3)   ├─→ LAS (S3)   ← propedeuticità dichiarata dal docente
ELT  (S1) ─────→ ELN  (S3)   │
RETI (S2) ───────────────────┘
```

Verificato il 2026-09-14: ogni testa precede le sue code di almeno una sessione, e `LAS` è
preceduto da entrambi i suoi prerequisiti.

**Conseguenza sulla forma del piano.** Le teste di catena sono ora **tutte** in S1: FI2, CALC,
MATAP ed ELT. S2 ne contiene una sola in senso lato — `RETI`, che regge `LAS` — e S3 nessuna.
Il piano resta rigido in testa e flessibile in coda, ma la rigidità di S1 è aumentata: non
c'è più, in quella sessione, un esame che si possa togliere senza spostare qualcos'altro.

### Chi è tagliabile, per sessione

Vigente dal 2026-09-14:

| Sessione | Non tagliabili | Tagliabili |
|---|---|---|
| S1 | FI2, CALC, MATAP, ELT — tutte teste di catena | **nessuno** |
| S2 | SO, RETI (reggono `LAS`) | **TLC** — l'unico; IDS solo a costo di spostare la coda |
| S3 | — | CA, WEB, ELN, LAS |

`[superato 2026-09]` La valvola di sfogo era `LAS` in S1. Ora la valvola è `TLC` in S2: è
l'unico esame senza code e senza prerequisiti a valle, e va tolto per primo se una sessione
non regge.

## Regole di carico

**1. Checkpoint a meno sei settimane.** Sei settimane prima del primo appello della sessione si
decide se la sessione resta a quattro esami o scende a tre. È una decisione presa in una data
fissata, non quando la situazione diventa evidente: nel 2026 la decisione su LAS è arrivata a
metà sessione, dopo aver già speso il tempo di preparazione. Il costo del ritardo non è stato
l'esame perso, è stato il tempo speso su un esame poi abbandonato.

`/lacune` produce questa decisione quando il checkpoint è dovuto.

> `[2026-09-14]` La sessione invernale si apre il **19 dicembre 2026**, non a gennaio. Finché
> le date dei singoli appelli non sono note, il checkpoint si conta dall'apertura della
> finestra: sei settimane prima del 19 dicembre cade intorno al **7 novembre 2026**. Va
> ricalcolato sul primo appello reale appena la prenotazione si apre.

**2. Si taglia dal fondo, mai la testa di una catena.** L'esame che si toglie è l'ultimo in
ordine di priorità nella sessione, e non deve avere code che dipendono da lui. La tabella qui
sopra dice chi può essere tolto.

**3. Un esame tagliato ha già una destinazione.** Non si "rimanda": si sposta in una sessione
nominata, nello stesso momento in cui lo si toglie. Un esame senza destinazione è un esame
perso, e lo si scopre mesi dopo.

> **Punto aperto — parzialmente sciolto il 2026-09-14.** Per `LAS` la destinazione è nominata:
> S3, dopo `SO` e `RETI`. Resta il problema generale: le tre sessioni esauriscono i 96 CFU
> senza margine, quindi un *ulteriore* taglio non ha dove andare. Le destinazioni disponibili
> restano due, entrambe da verificare:
> - un **appello straordinario** fra le sessioni ordinarie, se il corso di studi ne prevede;
> - la **sessione estiva 2028**, in parallelo all'elaborato e prima della laurea, che però è
>   anche l'ultimo margine: usarlo significa restare senza rete.
>
> Da risolvere prima del primo checkpoint, cioè entro **novembre 2026**.

**4. Un solo esame per volta in fase attiva.** Gli altri restano in ripasso, non in parallelo
(`profilo/studente.md`). `stato/corrente.md` descrive solo l'esame attivo; gli altri corsi
vivono in `corsi/<COD>/percorso.md`.

**5. Il piano si verifica su blocchi settimanali di programma coperto.** Mai su ore giornaliere:
la disponibilità di Lorenzo è troppo variabile perché un monte ore significhi qualcosa. La
metrica è *moduli chiusi a settimana*, confrontata con quella necessaria per arrivare
all'appello. `/lacune` calcola entrambe — quella osservata dalle ultime quattro settimane di
`log/giornate.md`, non da una stima.

**6. Le fonti si procurano da Virtuale, corso per corso.** `[2026-09-14]` Nessuno dei dodici
esami ha materiale già in casa: quello presente in radice riguarda solo esami chiusi ed è
archiviato in `ARCHIVIO/pre-riordino_2026-09/`. Il primo lavoro su ogni corso è compilare
`corsi/<COD>/fonti.md` e scaricare il materiale, prima di qualsiasi contenuto didattico
(`CLAUDE.md` §7.1). Per gli arretrati il materiale su Virtuale può essere dell'annata corrente
e differire da quello dell'anno in cui il corso era in piano: `fonti.md` deve dirlo.

## Perché questo piano esiste in questa forma

Il sistema precedente pianificava una sessione alla volta, con le date d'esame scritte dentro i
comandi. Funzionava finché l'orizzonte era di settimane. Su diciotto mesi il problema non è
sapere cosa fare questa settimana: è accorgersi *in tempo* che una sessione non sta reggendo, e
avere già deciso cosa si taglia e dove va. Le regole di carico sono la parte importante di
questo file; la tabella delle sessioni è solo il punto di partenza da cui si misurano gli
scostamenti.
