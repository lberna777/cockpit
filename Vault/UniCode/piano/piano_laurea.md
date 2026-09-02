# Piano di laurea — Ingegneria Informatica T

> Strato **permanente**. Cambia nell'ordine dei mesi, e ogni cambiamento è una decisione
> presa, non un aggiustamento. Si emenda, non si riscrive: quando una scelta viene superata,
> si marca `[superato AAAA-MM]` e si aggiunge quella nuova, con la ragione.
>
> Redatto il 2026-09-02. Sostituisce `ESAMI SCELTI.md`, che serviva una sola sessione.

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

Laurea nella **sessione estiva 2028**. Tre sessioni d'esame e un elaborato:

| Fase | Finestra | CFU | Esami |
|---|---|---|---|
| **S1** | gennaio–febbraio 2027 | 30 | FI2, CALC, MATAP, LAS |
| **S2** | giugno–luglio 2027 | 33 | SO, IDS, TLC, ELT |
| **S3** | gennaio–febbraio 2028 | 33 | CA, RETI, WEB, ELN |
| **Elaborato** | primavera 2028 | 3 | prova finale |
| **Laurea** | sessione estiva 2028 | — | — |

I codici e i CFU per esame stanno in `piano/codici.txt`, che è la fonte unica: qui non si
duplicano, si raggruppano.

### Date degli appelli

> **Da compilare.** Il calcolo delle settimane rimanenti in `/piano`, `/stato` e `/lacune`, e
> con esso il checkpoint delle sei settimane, dipende da queste date. Finché la riga è vuota,
> quei comandi ragionano sulla finestra di sessione e non sul singolo appello, con un margine
> d'errore di settimane.

| Esame | Primo appello utile | Secondo appello | Fonte |
|---|---|---|---|
| FI2 | — | — | — |
| CALC | — | — | — |
| MATAP | — | — | — |
| LAS | — | — | — |
| SO | — | — | — |
| IDS | — | — | — |
| TLC | — | — | — |
| ELT | — | — | — |
| CA | — | — | — |
| RETI | — | — | — |
| WEB | — | — | — |
| ELN | — | — | — |

## Catene di dipendenza

Un esame in testa a una catena non si sposta: ritardarlo ritarda tutto ciò che gli sta sotto,
anche a sessioni di distanza.

```
FI2  (S1) ──┬──→ IDS  (S2)
            └──→ WEB  (S3)
CALC (S1) ─────→ SO   (S2)
MATAP(S1) ─────→ CA   (S3)
ELT  (S2) ─────→ ELN  (S3)
```

Verificato: ogni testa precede le sue code di almeno una sessione. La ripartizione è
consistente con le catene.

**Conseguenza sulla forma del piano.** Le teste di catena sono concentrate all'inizio: S1 ne
contiene tre su quattro (FI2, CALC, MATAP), S2 una (ELT), S3 nessuna. Quindi il piano è
**rigido in testa e flessibile in coda**, ed è esattamente il contrario di come si è tentati di
gestirlo quando si è in ritardo. S1 è la sessione che non si può comprimere; S3 è quella dove
un taglio costa meno.

### Chi è tagliabile, per sessione

| Sessione | Non tagliabili (testa di catena) | Tagliabili |
|---|---|---|
| S1 | FI2, CALC, MATAP | **LAS** — l'unico |
| S2 | ELT | SO, IDS, TLC |
| S3 | — | CA, RETI, WEB, ELN |

In S1 il margine è di un solo esame, e quell'esame è `LAS`, che è **già stato rimandato una
volta** (abbandonato a metà sessione estiva 2026, non sostenuto all'appello di settembre 2026).
Tagliarlo di nuovo non è un aggiustamento neutro: significa che un esame da 6 CFU ha consumato
tre sessioni. Se a dicembre 2026 il checkpoint indica di scendere a tre esami, la domanda da
porsi non è *quale taglio* — è già deciso — ma *dove va LAS*, e la risposta va scritta prima di
tagliare.

## Regole di carico

**1. Checkpoint a meno sei settimane.** Sei settimane prima del primo appello della sessione si
decide se la sessione resta a quattro esami o scende a tre. È una decisione presa in una data
fissata, non quando la situazione diventa evidente: nel 2026 la decisione su LAS è arrivata a
metà sessione, dopo aver già speso il tempo di preparazione. Il costo del ritardo non è stato
l'esame perso, è stato il tempo speso su un esame poi abbandonato.

`/lacune` produce questa decisione quando il checkpoint è dovuto.

**2. Si taglia dal fondo, mai la testa di una catena.** L'esame che si toglie è l'ultimo in
ordine di priorità nella sessione, e non deve avere code che dipendono da lui. La tabella qui
sopra dice chi può essere tolto.

**3. Un esame tagliato ha già una destinazione.** Non si "rimanda": si sposta in una sessione
nominata, nello stesso momento in cui lo si toglie. Un esame senza destinazione è un esame
perso, e lo si scopre mesi dopo.

> **Punto aperto — richiede una decisione.** Le tre sessioni sono piene: 30 + 33 + 33 esaurisce
> i 96 CFU senza margine. Un esame tolto da S1 e spostato su S2 porterebbe S2 a cinque esami e
> 39 CFU, che è peggio del problema che il taglio voleva risolvere. Le destinazioni realmente
> disponibili sono due, e nessuna delle due è ancora verificata:
> - un **appello straordinario** fra le sessioni ordinarie, se il corso di studi ne prevede per
>   l'esame in questione;
> - la **sessione estiva 2028**, in parallelo all'elaborato e prima della laurea, che però è
>   anche l'ultimo margine disponibile: usarlo per un esame significa restare senza rete.
>
> Finché questo punto non è sciolto, la regola 3 non è applicabile e il checkpoint della regola
> 1 non ha una risposta da dare. Va risolto **prima** del primo checkpoint, cioè entro dicembre
> 2026.

**4. Un solo esame per volta in fase attiva.** Gli altri restano in ripasso, non in parallelo
(`profilo/studente.md`). `stato/corrente.md` descrive solo l'esame attivo; gli altri corsi
vivono in `corsi/<COD>/percorso.md`.

**5. Il piano si verifica su blocchi settimanali di programma coperto.** Mai su ore giornaliere:
la disponibilità di Lorenzo è troppo variabile perché un monte ore significhi qualcosa. La
metrica è *moduli chiusi a settimana*, confrontata con quella necessaria per arrivare
all'appello. `/lacune` calcola entrambe — quella osservata dalle ultime quattro settimane di
`log/giornate.md`, non da una stima.

## Perché questo piano esiste in questa forma

Il sistema precedente pianificava una sessione alla volta, con le date d'esame scritte dentro i
comandi. Funzionava finché l'orizzonte era di settimane. Su diciotto mesi il problema non è
sapere cosa fare questa settimana: è accorgersi *in tempo* che una sessione non sta reggendo, e
avere già deciso cosa si taglia e dove va. Le regole di carico sono la parte importante di
questo file; la tabella delle sessioni è solo il punto di partenza da cui si misurano gli
scostamenti.
