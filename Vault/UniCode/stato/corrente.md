# Stato Corrente — Studio Attivo

**Esame attivo**: `FI2` — Fondamenti di Informatica T-2 (12 CFU) | **Aggiornato**: 2026-10-05

> Un solo esame in fase attiva (`piano/piano_laurea.md`, regola 4). Gli altri tre di S1 —
> `CALC`, `MATAP`, `ELT` — hanno cartella, fonti e percorso pronti, e restano in attesa.
> Lo stato di `LAS` è archiviato in `corsi/LAS/stato.md`.

## Perché FI2

Testa di catena doppia: regge `IDS` in S2 e `WEB` in S3. Vale 12 CFU sui 30 della sessione, e
la sua verifica è pratica — codice che compila e passa i test — quindi è quella che richiede
più tempo di esecuzione e meno di lettura. È l'esame che non può slittare.

## Stato dei moduli

- 57 moduli di teoria, 13 esercitazioni di laboratorio, 11 esercizi autonomi.
- ✅ **01** «Dai linguaggi alle infrastrutture software» — chiuso il 2026-09-16 (criterio *teoria*,
  verifica a voce a libro chiuso: d.2 parziale, d.3 buona, d.4 buona, black-box/white-box parziale
  recuperata con guida; `mvn package` saltata). Primo ripasso dovuto il 2026-09-19.
- ✅ **02** «Linguaggio e piattaforma» e **02x** «Esercitazione: tipi base» — chiusi il 2026-09-26
  **per decisione di Lorenzo**, dopo aver svolto la 02x: la verifica a voce finale è stata saltata
  («stiamo ripassando troppo»). Inventario per il ripasso pre-esame, i tre punti deboli del 16/09:
  `float f = 3.54` contro `double x = 3.54F` (verso e Design Intent); a `java` si passa il nome della
  classe; U+1F608 = 2 `char`, 4 byte UTF-8. Dalla 02x è nato il **prontuario d'esame**
  `corsi/FI2/appunti/prontuario_FI2.md`, da aggiornare a ogni fine sessione pratica (`/chiudi` 8a).
  `/appunti FI2 02` non si fa (sospeso il 2026-10-05).
- ✅ **LAB02** «Frazione — prima parte» — chiuso il 2026-09-30 con i test verdi, **svolto con
  guida** (suggerimenti a gradini in chat): da rifare a freddo nella preparazione all'esame. Codice
  e confronto con il docente in `corsi/FI2/esame_FI2/svolti/LAB02_Frazione/`. Inciampi: caso 0 non
  coperto nel costruttore (`0/0` a test verdi), `mcm` con sottrazione invece di divisione.
- ✅ **LAB03** «Frazione — seconda parte» — chiuso il 2026-09-30 con i test verdi, **svolto con
  guida** (correzioni di `sumWithMcm`, `sub`, `getDouble` date in chat): da rifare a freddo. Codice e
  confronto in `corsi/FI2/esame_FI2/svolti/LAB03_Frazione/`. Inciampi: `den/mcm` invece di
  `mcm/den` (verso, pattern 5), `sub` come `f − this`, divisione intera in `getDouble`; test verdi
  per caso su `sub` e `compareTo` (pattern 2). Eclipse: `UnsupportedClassVersionError` 69/65 →
  compliance 21 nelle preferenze del workspace.
- ✅ **LAB04a** «Frazioni base — FrazLib» — chiuso il 2026-10-01 con i test verdi, **svolto con
  guida** (iniziato nel cloud, finito in locale): da rifare a freddo. Codice e confronto in
  `corsi/FI2/esame_FI2/svolti/LAB04a_FrazioniBase/`: logica identica al docente. `sum` scritta da
  solo; `mul` copiata da `sum` e corretta dopo due domande (neutro `1`, `.mul`). Lorenzo dichiara
  chiara la distinzione `static` / d'istanza (criterio «usa `this`?»), dopo la confusione delle
  15:23, e gestiti da solo gli array; verifica a voce saltata.
- ✅ **LAB04b** «Frazione double face» — chiuso il 2026-10-01 con i test verdi, **svolto con
  guida**: da rifare a freddo. Codice e confronto in `corsi/FI2/esame_FI2/svolti/LAB04b_FrazioniDoubleFace/`.
  `size` scritta da solo; `convertToString` e i cicli dei metodi statici dopo tre giri sulla
  condizione (`length-1` → `length` → `length && != null`, data dalla sl. 28): **fine fisica e
  fine logica confuse**; giudizio di Lorenzo: «chiaro ma non chiarissimo», fatica sul ragionamento con gli array e sulla forma «giusta». `0/6` risolto chiamando `sumWithMcm`. Il suo `sum(Frazione[])` regge le
  celle `null`, quello del docente no (verificato).
- ✅ **LAB04c** «ADT FractionCollection» — chiuso il 2026-10-02 con i test verdi (eseguiti con `javac`/`java -ea`), **svolto con guida**: da rifare a freddo. Codice e confronto in `corsi/FI2/esame_FI2/svolti/LAB04c_FractionCollection/`. Scritti da solo campi, costanti, tre costruttori, `sum`/`mul` (con la scelta `IllegalArgumentException` se le `size` differiscono); corretti dopo controllo `size()` (non ricalcolarlo dai `null`), `get` (`||`), `put` (assegnare il nuovo array, `*` e non `+`, inserimento fattorizzato, caso capacità 0 risolto da lui), `remove` (tre scarti di uno), `toString` (mai usato `StringBuilder`; ultimo elemento fuori dal ciclo → eccezione sulla vuota). Fisico/logico: riconosciuto da solo all'inizio, ricaduto in `size()` e `toString`. Verifica a voce saltata. Resta nel codice svolto il formato `[ 1/3 ]` con spazi (docente: `[1/3]`), vedi il confronto.
- 🔶 **LAB05** «TicketSosta» — **parte 1 chiusa nei test il 2026-10-05, resta 🔶 per decisione di Lorenzo finché non è fatta la parte 2** (`TicketEvoluto`, `ParcometroEvoluto`, 60 min [sl. 26]). **Svolta con guida**: da rifare a freddo. Codice e confronto in `corsi/FI2/esame_FI2/svolti/LAB05_TicketSosta/`. Scritti da lui: struttura di `calcolaCosto` in 4 passi, `toStringDuration`, `getCostoAsString`, `emettiTicket`, `toString` di `Parcometro`; `toString` di `Ticket` ripreso dalla slide 11. Inciampi: ordine dei parametri del costruttore, confronto del minimo sulla durata totale invece che dopo la franchigia (corretto dopo tre segnalazioni; i test dati non lo vedono), cosa va nel costruttore e cosa nei parametri. Rimandati: mezzanotte, nomi dei getter, `toString` di `Ticket`. Moduli `10`, `11`, `S02` entrati in voce 🔶. Verifica a voce saltata.
  **Osservazione di Lorenzo (2026-10-05)**: assimilati classi, chiamate, tipi; fatica sui *processi logici dentro le funzioni* (la regola del docente) e sulle spiegazioni che «danno indicazioni in un posto che non conosce». Rimedio da provare: prima del codice, tracciare la regola **a mano su un caso dei test** (come i numeri del `/flusso`), poi tradurre.
- 🔶 **07** «Array» e **08** «Package e namespace»: entrati in LAB04a (array di oggetti, *for
  each*, `length`; package e `import`); si completano con LAB04b/c ed `ES-MATRICI`.
- 🔶 **04b** «Classi e oggetti» e **06** «Stringhe»: entrati in LAB02 per costruttori, `this(...)`,
  `toString`/`@Override`; si completano con i LAB che li riusano.
- Tutti gli altri: non aperti.
- Materiale completo in `corsi/FI2/materiali/`; mappa in `corsi/FI2/percorso.md`.
- Edizione del materiale: 2023/24, quella d'iscrizione.

## Prossimo passo esatto

**`[2026-09-30]` Metodo cambiato**: si lavora sui LAB con i test, accompagnati in chat; la teoria
entra solo quando la voce la richiede, e i moduli di teoria non si aprono più con `/lezione`
(`CLAUDE.md` §2 e §8, `/lab` template FI2). Prontuario riorganizzato per parte del compito; kit
d'esame in `corsi/FI2/esame_FI2/`.

1. **LAB05 parte 2**: `ticketsostaevoluto` (`TicketEvoluto`, `ParcometroEvoluto`) con i test già nel progetto `da_importare/LAB05_TicketSosta-051026/tests/ticketsostaevoluto/`; prima di scrivere codice, `/flusso` sul `calcolaCostoSuPiuGiorni` (slide 21–23: franchigia solo sul primo giorno, tariffa per giorno dell'array `0=lunedì`). Pendenze minori della parte 1: rinominare i getter in `getInizioSosta`/`getFineSosta`, `toString` di `Ticket` come il docente, mezzanotte (`00:00`) con la soluzione del docente.
   Pulizia ancora da fare: nel workspace Eclipse restano `Lab04c-…-Soluzione.zip_expanded` e `…-Startkit.zip_expanded` (la prima contiene la soluzione del docente).
2. Dopo ogni LAB verde: `confronto_<ID>.md` in `svolti/` e prontuario da `/chiudi` 8a.

Chiuso (§4b della guida, verificato di nuovo il 2026-09-26 e scritto nel prontuario): la slide 34 annota `FE FF` come marcatore *little endian*, ma
`"A".getBytes("UTF-16")` dà `[-2, -1, 0, 65]`, cioè il BOM **big endian**, coerente con la slide 35
(«Everything in Java is stored in big-endian order»). Verificato il 2026-09-21: la slide 34 è
imprecisa. Da sapere prima dell'orale.

## Ripassi — decisione di metodo del 2026-09-25

I ripassi **non si fanno più a intervalli durante il percorso**: si accumulano e si fanno **in
blocco a ridosso dell'esame**. Deciso da Lorenzo il 2026-09-25, dopo aver interrotto il secondo
ripasso di 01 alla seconda domanda: la priorità è avanzare sui moduli, non consolidare quelli
chiusi. Conseguenze operative:

- il tracker continua a registrare scadenze, ma **non vanno proposte** all'inizio della sessione;
- `SCADUTO` nel briefing va letto come inventario di ciò che andrà ripassato prima della prova,
  non come lavoro dovuto oggi;
- il rischio accettato è esplicito: `FI2` è la testa di catena di `IDS` e `WEB`, e un modulo chiuso
  a settembre 2026 dovrà reggere fino a febbraio 2027 senza passaggi intermedi. Il recupero si
  concentra tutto nelle settimane che precedono l'esame e va previsto nel piano.

Il secondo ripasso di 01 (2026-09-25) è stato interrotto dopo due domande e **non conta**: nessun
marcatore scritto, il modulo resta a gradino 3. Il primo, del 2026-09-21, era stato `debole` (1/5). Era previsto di verificare **per primi** i due punti rimasti deboli, che hanno
la stessa radice — *da dove nasce* la cosa:
- **error** JUnit: eccezione imprevista **durante l'esecuzione**, l'asserzione non viene raggiunta
  (non «la struttura», che è a posto perché il codice ha compilato);
- **black-box / white-box**: il caso si ricava dalla **specifica** o dal **codice**; entrambi
  controllano il risultato.

## Punti aperti su questo corso

1. Numeri 18 e 19 assenti dalla numerazione delle slide: da chiarire.
1b. La «struttura formale» di Java (da cosa è composto il linguaggio) resta poco chiara a Lorenzo,
    che la giudica poco rilevante per l'esame: non è prioritaria, ma i moduli 02, 04b e 12 la
    costruiscono in modo operativo, quindi va ripresa lì e non in astratto.
1c. Il versioning è il punto in cui l'esperienza pregressa (GitHub) ha agganciato la teoria:
    Lorenzo vuole approfondirlo. Il corso non ci torna sopra (solo 01 sl. 5–12).
1d. Maven (`mvn package`, perché può non produrre il JAR): rimandato da Lorenzo il 2026-09-16 al
    momento in cui servirà. Il corso gli dedica una sola slide (01 sl. 17) e all'esame si consegna
    un progetto Eclipse: non è una lacuna d'esame.
1e. **Da riprendere (2026-09-16, verifica 02 d.4)**: Lorenzo dice che il meccanismo della perdita
    di informazione è chiaro, ma non sa **riconoscerla a occhio dalla sintassi**: leggere il tipo
    del letterale dal suffisso (`3.54` → `double`, `3.54F` → `float`; interi `L` → `long`) e il verso
    dell'assegnamento. Nella verifica aveva invertito `float f = 3.54` e `double x = 3.54F`. Da
    allenare su righe concrete prima di chiudere 02 — `02x` è il posto naturale.
2. Libro di testo dichiarato in scheda ma non reperito.

## Archivio delle prove — acquisito

**30 sessioni complete** con testo, start kit e soluzione ufficiale (2020-01 → 2025-02), in
`prove/`. Il curricolo si costruisce sulle tipologie ricorrenti che emergono da questi testi
(`CLAUDE.md` §7.3). `15/01/2025` e `12/02/2025` restano di riserva per la verifica finale.
