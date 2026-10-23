# Stato Corrente — Studio Attivo

**Esami attivi**: `FI2` e `CALC` | **Aggiornato**: 2026-10-23

- `CALC` — Calcolatori Elettronici T (6 CFU) · aperto il 2026-10-06 · **iscritto all'appello del 22 dicembre 2026, ore 9:00** (Lorenzo, 20/10) · checkpoint ~10 nov · `02p` ✅ chiusa il 9/10 · 🔶 `02`: lezione finita il 22/10; lab sulla prova 2023-12-21 (memorie) **svolto guidato il 23/10**, confronto con la soluzione senza errori di sostanza, sicurezza 3/5: il 02 si chiude a freddo su un'altra prova. ⚠️ Calendario indietro: 03–05 ancora da aprire.
  Sezione in fondo.
- `FI2` — Fondamenti di Informatica T-2 (12 CFU) · **iscritto all'appello del 13 gennaio 2027, ore 9:00** (Lorenzo, 20/10) · checkpoint ~2 dic · ✅ `LAB06` MasterMind **chiuso il 22/10** (34/34 verdi, **guidato**: da rifare a freddo); `calcolaRisposta` pensata da Lorenzo, bug dei minimi trovato da lui con stampe vs tabella. Codice e confronto (12 punti) in `esame_FI2/svolti/LAB06_MasterMind/`. Prossima voce: `LAB07` MyCalendar (`/lab FI2 LAB07`).

> Più esami attivi in parallelo dal 2026-10-06 (`piano/piano_laurea.md`, regola 4).
> `MATAP` ed `ELT` restano in attesa; lo stato di `LAS` è in `corsi/LAS/stato.md`.

## ═══ FI2 ═══

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
- ✅ **LAB05** «TicketSosta» — chiuso il 2026-10-05 con i test verdi di entrambe le parti (`TicketTest`, `ParcometroTest`, `TicketEvolutoTest`, `ParcometroEvolutoTest`), **svolto con guida**: da rifare a freddo. Codice e confronto (punti 1–16) in `corsi/FI2/esame_FI2/svolti/LAB05_TicketSosta/`. Parte 1: `calcolaCosto` in 4 passi suo; inciampi sull'ordine dei parametri, sul confronto del minimo (a test verdi). Parte 2: `TicketEvoluto`, ciclo sui giorni, tariffa per giorno, franchigia, `toString` suoi dopo correzioni; il **blocco del minimo** nel ramo «stesso giorno» l'ha scritto Claude. Inciampi: immutabilità di `plusDays`, tariffa dal giorno sbagliato, `tariffa.toString()` su array, quick fix di Eclipse che ha cambiato `Ticket` della parte 1. Debolezze note, non nei test: minimo solo sul ramo «stesso giorno» (il docente lo applica all'intera sosta), franchigia a cavallo di mezzanotte (comune al docente). Moduli `10`, `11`, `S02` entrati in voce 🔶. Verifica a voce saltata.
- ✅ **LAB06** «MasterMind» — chiuso il 2026-10-22 con 34/34 test verdi (`Combinazione`, `Risposta`, `Gioco`, `MasterMind`), **svolto con guida**: da rifare a freddo. Codice e confronto (12 punti) in `corsi/FI2/esame_FI2/svolti/LAB06_MasterMind/`. Prima voce fatta con la **procedura d'esame** (prontuario §2), costruita il 21/10. Suoi: `setPiolo`, `equals` (con `null` dopo il caso proprio), `Risposta` intera, `registraMossa` (stato salvato dopo correzione), l'algoritmo di `calcolaRisposta` (calcolato a mano sulle sl. 31 e 33, poi tradotto) e il bug dei minimi trovato con le stampe. Inciampi: estremi (`dim − 1`, cella libera vs ultima piena, ciclo fino a `maxTentativi`, `nextInt(5)`), posizioni e colori fusi nel ciclo dei minimi, `situazione` e i formati (tab, spazi, `Gioco: `). Teoria entrata in voce: `09` (enum, `ordinal`, `values`), `12` (package per funzionalità), `StringJoiner`, `Random`, `protected` e classe anonima nei test.
  **Osservazione di Lorenzo (2026-10-05)**: assimilati classi, chiamate, tipi; fatica sui *processi logici dentro le funzioni* e sulle spiegazioni che «danno indicazioni in un posto che non conosce». Ha funzionato: tabella a mano su un caso dei test, `/flusso`, `println` per cercare i bug.
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

0. **Procedura d'esame**: costruita il 21/10 e scritta nel prontuario §2 (obiettivo del 5/10 ✅). Restano da allenare: test propri scelti da lui (passo 7) e debug con stampe (passo 8).
1. **Punto di ripresa**: `LAB07` «MyCalendar» (`/lab FI2 LAB07`): slide + recap + commento + startkit; teoria 10, 12, S02 (`LocalDateTime`, `Duration`, MVC). Con la procedura del prontuario §2, partendo dall'UML.
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

## ═══ CALC ═══

**Aperto il 2026-10-06** per un appello anticipato del 2 dicembre che non c'era. `[2026-10-20]` Lorenzo
è **iscritto all'appello del 22 dicembre 2026, ore 9:00**: è il primo appello di S1, non più anticipato. Edizione del materiale
2024/25; mappa e stato dei moduli in `corsi/CALC/percorso.md`.

**Prova d'esame**: un unico esercizio di progetto di un sistema DLX (memorie, porte in
*handshake*, reti logiche, *interrupt handler*), invariato dal 2015. Indice delle 62 prove
(46 con soluzione) in `corsi/CALC/prove/INDICE.md`.

**Calendario (8 settimane)** `[superato 2026-10-20: l'appello è il 22/12, il checkpoint passa a ~10 nov; calendario da rifare con /pianifica]`:
- sett. 1–3 (6–26 ott): `02`, `03`, `04`, `05`; `00` solo se la prova lo richiede;
- sett. 4 (27 ott – 2 nov): `07`, `08`, `01`;
- **checkpoint ~3 nov**: prova `2024-01-19` a freddo, cronometrata. Sotto la sufficienza si
  rinuncia al 2 dicembre (`piano/piano_laurea.md`, regola 1);
- sett. 5–8: ciclo sulle prove, dalle più recenti all'indietro; riserva `2025-01-29`, `2025-02-12`.

**Stato dei moduli**:
- 🔶 **02** «Mapping e decodifica» — lezione creata il 2026-10-06 nel template *progetto su prova*
  (`corsi/CALC/lezioni/lezione_02_mapping_decodifica.md`), estratto dalla prova `2025-01-08`;
  passo 1 della procedura nel prontuario `corsi/CALC/appunti/prontuario_CALC.md`.
  **20/10 — punti 1–2 della prova `2025-01-08` fatti, CS a metà.** Ricavata da Lorenzo, con
  guida, la mappa completa: 1600 = 1024+512+64; EPROM `00000000h–3FFFFFFFh`,
  `40000000h–5FFFFFFFh`, `60000000h–63FFFFFFh`; RAM `80000000h–FFFFFFFFh` con il metodo
  dall'alto (FFFFFFFFh − taglia + 1) trovato da lui. Inciampi: la M persa due volte (512 MB →
  esponente 9·3 = 27; 64 MB → 2^6), 2 GB letti come 2000 MB, cifre perse (7 invece di 8),
  `1` + 30 zeri letto «2», prestito/riporto hex dimenticati (rifatti in colonna), «ultimo
  indirizzo» non capito finché non è arrivato l'esempio dei posti al cinema (fine = inizio +
  taglia − 1). Sua osservazione giusta: k·2^n = k in binario + n zeri (il 3·2^29 = `60000000h`).
  Chip-select: non capiti con la tabella ridotta alle prime cifre hex; rispiegata la firma
  per esteso a 32 bit sull'EPROM da 1 GB, **non ancora letta da Lorenzo** (pausa). Il testo
  della 21/12/2023 (1032 MB) resta intatto per il lab a freddo. Prodotto: cheatsheet §1a.
  **20/10, pomeriggio — CS fatti, Decisione 2 a metà.** Firme a 32 bit (512 MB, 64 MB, RAM) e
  tutti i CS ricavati da lui, coincidenti con la soluzione; idea sua: prima tutte le firme, poi
  tutti i CS. Porta nel buco capita solo con la sua regola («indirizzo tondo nel buco, confronto
  la firma con le altre») dopo tre spiegazioni fallite. Zone dei CS e repliche (64 MB: 4 copie)
  trovate da lui; mutua esclusione verificata. Decisione 2: «4 banchi da taglia/4» capito con
  l'esempio a 8 byte, `CS_..._i = CS blocco · BEi` fatto; banco/riga (BA1–0 / BA2) e piedini RAM
  `A[28..0] ← BA[30..2]` fatti, poi **piedini non capiti** sul 64 MB, stanco. Decisione 3 non
  letta (sostanza già fatta: semplificata e repliche). Prodotto l'artefatto
  «Prova DLX 8 gennaio 2025» (https://claude.ai/artifact/5iHgc8vnP9dtjop3fQ8j3w, sorgente
  `corsi/CALC/appunti/prova_2025-01-08_svolta.html`): i 10 passi collegati alla soluzione intera.
  **22/10 — lezione finita.** Piedini e bus dati non passavano a parole né con lo schema a
  blocchi («persissimo», «voglio vedere i singoli piedini e fili»); capiti con la vista «filo per
  filo» dell'artefatto: EPROM 64 MB `A[23..0] ← BA[25..2]` letto dal disegno, 512 MB
  `A[26..0] ← BA[28..2]` da solo con i tre passi (esponente, piedini, fili); «ogni byte avanti
  cambio banco» detto da lui. Decisione 3 nella sostanza già fatta; `RESET_P` = comando → `·MEMWR`
  (dispensa p. 47). L'artefatto ora ha anche: dati/incognite, foglio «su carta» in 4 riquadri
  (anche nel prontuario §0b), mappa della memoria cliccabile, vista filo per filo con indirizzo di
  prova. **Giudizio di Lorenzo**: sicurezza **1/5** a fare da solo la tabella della risposta; la
  fatica è sapere «dove mi sto muovendo, cosa cerco, cosa so» e capire fisicamente cosa controlla.
  **23/10 — lab sulla prova `2023-12-21` (memorie), guidato.** Per decisione di Lorenzo con
  l'artefatto dell'8/01 aperto: non chiude il 02 (§7.2). Fatti da lui: 1032 = 2^30 + 2^23, mappa
  completa (EPROM `00000000h–3FFFFFFFh`, `40000000h–407FFFFFh`, buco `40800000h–7FFFFFFFh`, RAM
  `80000000h–FFFFFFFFh`), firme, porte messe da lui a `50000000h`/`60000000h`, tutti i CS
  semplificati (porte comprese), banchi, piedini. Aiuti: +1 esadecimale col riporto; **valore dei
  bit di firma** (sapeva fin dove arriva la firma, non leggerne i valori: sbloccato con la
  conversione cifra per cifra sotto BA31..BA20 e l'esempio passo per passo sull'1 GB);
  semplificazione con le porte (CS dell'8 MB a `/BA31·BA30` sopra tutto il buco; capito con «il CS
  vede solo i suoi fili → repliche», poi «prima scelgo le porte, poi confronto i bit»); CS per
  banco (`·BEi` capito con la cassettiera e LB/LW); piedini (regola «da BA2, ultimo = piedini + 1»).
  Confronto con la soluzione: tutto coincide; CS 8 MB con un bit in più (`/BA28`) per la sua scelta
  delle porte, giusto; mancava RD/WR (EPROM MEMRD, RAM MEMRD+MEMWR). La soluzione mette le due porte
  su **un unico** `CS_INPUT` (mutua esclusione via `ACTIVE_0`): moduli 04–05. **Giudizio di
  Lorenzo**: sicurezza **3/5** sulla tabella (era 1/5), scelta degli spazi 5/5; piedini fatti
  nell'esercizio ma «non mi è chiaro cosa siano nel pratico e come funzionino»: da rifare.
- ✅ **02p** «Fondamenta per il mapping» — chiusa il 2026-10-09. — lezione creata l'8/10 su richiesta di Lorenzo, perché
  la 02 dava per scontati quadro fisico, notazione e binario/esadecimale
  (`corsi/CALC/lezioni/lezione_02p_fondamenta.md`). Studiate le sezioni 1–5 con domande in chat:
  bus e chi li pilota, chip e piedini, decoder di I livello (sbloccato con l'analogia del
  condominio dopo che schema e widget non avevano funzionato), 3-state, conversioni. Inciampi:
  unità K/M nelle potenze di due (32 KB → «5», 64 MB → «7»), lettura del binario (`1100` = 8),
  causa invertita sul 3-state. Prodotti: prontuario §0, `appunti/cheatsheet_conversioni_CALC.md`,
  traccia per gli appunti in `grezzi/traccia_02p_2026-10-08.md`. Della 02 letta solo la
  Decisione 1.
  **9/10, mattina — §6 a metà.** Ricavati da Lorenzo, con guida, tutti gli intervalli
  dell'esercizio 10 (RAM_1 `0000h–1FFFh`, RAM_2 `2000h–27FFh`, RAM_3 `2800h–2FFFh`, EPROM
  `C000h–FFFFh`); i segnali CS non ancora affrontati. Emerse lacune di aritmetica hex: somme e
  prestito a 16, cifre A–F nelle colonne (12 scritto «12» invece di C), 2^n = 1 seguito da n zeri
  (scritto rovesciato), di nuovo la K persa (16K → «2^4»). Sua domanda giusta: perché 8K+2K+2K e
  non 8K+4K — il testo non impone taglie, la lezione è stata corretta. Prodotti: cheatsheet §10e–g,
  prontuario §0 inciampi del 9/10.
  **9/10, pomeriggio — chiusa.** Segnali CS dell'esercizio 10 ricavati da Lorenzo: firma = bit
  uguali agli estremi (lo schema `A15..A0` capito solo dopo averlo ricostruito da `1FFFh`), pausa
  su `A11*` risolta da lui, «un CS ha senso solo per confronto con gli altri chip» detto da lui
  (`CS_EPROM = A15`); dimenticato `A15*` in `CS_RAM_1` (separa dalla EPROM). Spiegate le repliche
  della decodifica semplificata. «Prova tu» 6/6 da solo, K tenuta. Saltate per scelta la variante
  8K + 4K e la §7. **Giudizio di Lorenzo**: sicuro su conversioni, firma e CS; fatica a
  **«muoversi nella memoria»** (dove finisce un blocco, ragionare per intervalli).
- Tutti gli altri: non aperti.

**Giudizio di Lorenzo (20/10)**: chiari scomposizione, banchi, mappa, firme, CS, mutua
esclusione; porte «più o meno» (cosa fanno: moduli 04–05); repliche faticose → formula nel passo 5
dell'artefatto; legame banchi–CS–BE a metà, `CS_INPUT` e `RESET_P` non chiari (box aggiunti nei
passi 7 e 9); **piedini, bus dati e interfacciamento per nulla**. Mancano, rispetto alla soluzione:
passi 8 (piedini, bus dati, schemi pp. 9–12), 9 (porte, pulsante, reti) e 10 (handler).

**Prossimo passo esatto** `[2026-10-23]`: `/lezione CALC 03` «Linguaggio macchina» (24/10),
aprendo con 10 minuti sui piedini in senso fisico (cosa sono, cosa succede filo per filo quando il
DLX legge un indirizzo: vista «filo per filo» dell'artefatto dell'8/01). La chiusura a freddo del
02 va sulla prova `2024-01-19` (memorie), oppure si fonde nel checkpoint del ~10 nov, che usa la
stessa prova: decidere con `/pianifica settimana` lunedì 26/10.

**Prossimo passo** `[superato 2026-10-23: lab fatto, guidato]` `[2026-10-22, per il 23/10]`: `/lab CALC 02` sulla prova
`2023-12-21` (1032 MB di EPROM in basso, 2 GB di RAM in alto), solo consegne a) e b) per le
memorie, **a freddo** e con il foglio in 4 riquadri (prontuario §0b): ① dati, ② linea degli
indirizzi a mano, ③ tabella della risposta colonna per colonna, ④ controlli. Lorenzo si aspetta
di aver bisogno di un po' d'aiuto: per §7.2 il lab chiude il 02 solo se svolto a freddo; se serve
aiuto, dargli solo la **domanda del riquadro** («cosa sai? cosa cerchi in questa colonna?»),
mai il valore, e annotare dove. Poi confronto con la soluzione ufficiale. Il 1032 MB non è mai
stato guidato. Dopo: `/lezione CALC 03` (24/10). A fine 02p: `/appunti CALC 02p` dalla traccia.

**Punti aperti**: modulo `06` assente dalle dispense; le «domande di carattere generale» della
scheda non compaiono nei testi pubblicati; libro di testo non reperito.
