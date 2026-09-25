# Stato Corrente — Studio Attivo

**Esame attivo**: `FI2` — Fondamenti di Informatica T-2 (12 CFU) | **Aggiornato**: 2026-09-25

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
- 🔶 **02** «Linguaggio e piattaforma» — in corso dal 2026-09-16. Lezione
  (`corsi/FI2/lezioni/lezione_02_linguaggi_piattaforme.md`, PDF in `pdf/lezioni/`) studiata e
  verificata a voce a libro chiuso: d.1 (`comp.operation`, chi fa cosa) buona dopo guida; d.2
  (`javac`/`java`) buona dopo guida; d.3 (EXE contro `.class`, EXE .NET) buona dopo guida; d.4
  (conversioni fra reali) **da riprendere** — verso invertito; d.5 (Unicode/UTF) parziale — `char`
  e byte fusi. Pratica `02x` non svolta: non è chiudibile finché non lo è.
- 🔶 **02x** «Esercitazione: tipi base» — aperto il 2026-09-21. Guida-lab generata in modalità
  guidata da `02x` (42 sl.) + `02z` (7 sl.): `corsi/FI2/lezioni/guida_lab_02x_tipi_base.md`.
  Nessuno startkit — il contratto è la lista di collaudo del docente (sl. 48, otto casi). Sei
  paragrafi: `main`/argomenti, assegnamenti fra numerici, overflow e IEEE-754, caratteri e UTF,
  primitivi contro classi-libreria, equazioni di 2° grado. Da svolgere; chiude 02 se l'esercizio
  finale regge a freddo.
- Tutti gli altri: non aperti.
- Materiale completo in `corsi/FI2/materiali/`; mappa in `corsi/FI2/percorso.md`.
- Edizione del materiale: 2023/24, quella d'iscrizione.

## Prossimo passo esatto

**Svolgere `corsi/FI2/lezioni/guida_lab_02x_tipi_base.md`**, nell'ordine che la guida indica:
comincia dal **§2** (assegnamenti fra tipi numerici) e non dal §1, perché è il punto che ha fatto
cadere la verifica del 16/09 e il ripasso del 21/09. Il drill del §2 sono 14 righe: per ciascuna,
**A o R e la ragione scritta**, nella forma «il letterale è X, la variabile è Y, X→Y ⇒ …»; poi
verifica in jshell. La regola: prima il **tipo del letterale dal suffisso**, poi il verso.

Poi §3 (overflow: `short d = c+1;` rifiutato contro `b++` accettato), §4 (`char` contro byte
sull'emoji: 2 `char`, 4 byte UTF-8), §5 (a chi si chiede il servizio), e infine **§6, le equazioni
di 2° grado**: scritto a freddo, con gli otto casi di collaudo previsti in tabella *prima* di
eseguirli, e le slide 49–51 (soluzione) chiuse fino al §7.

Quando i drill sono fatti, ridomandare a voce, a libro chiuso, i tre punti deboli di 02:
- `float f = 3.54;` contro `double x = 3.54F;` — quale compila e perché, cast e Design Intent;
- a `java` si passa **il nome della classe** col `main`, non il file `.class`;
- U+1F608 occupa **2 `char`** (coppia surrogata), cioè 4 byte.
Se tornano e `02x` è svolta: CHIUSO FI2 02 e CHIUSO FI2 02x. A seguire `03` (Deployment), poi `03x`
e `LAB01`.

Da segnalare nella guida (§4b): la slide 34 annota `FE FF` come marcatore *little endian*, ma
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
