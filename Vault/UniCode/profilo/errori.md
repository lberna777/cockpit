# Errori ricorrenti

> Strato **permanente**, append-oriented. Aggiornato da `/appunti`, `/ripassa`, `/simula`
> nella stessa esecuzione in cui l'errore emerge.
>
> La sezione **trasversale** è quella che conta: sono modi di ragionare, non errori di
> materia, e si ripresenteranno identici su corsi che Lorenzo non ha ancora aperto.
> Il briefing d'avvio carica questa sezione per prima.

## Trasversale — vale su ogni corso

### 1. Semplificare distinzioni che vanno tenute separate
Tendenza accertata a collassare due concetti vicini in uno. Emerso ripetutamente in
Diritto, ma è un pattern cognitivo, non una lacuna giuridica.

**Dove si ripresenterà**: stabilità asintotica vs. semplice (`CA`); banda vs. banda
passante (`TLC`); processo vs. thread, concorrenza vs. parallelismo (`SO`); tensione di
soglia vs. tensione di saturazione (`ELN`); latenza vs. RTT (`RETI`).

**Contromisura**: davanti a due termini vicini, chiedersi *cosa distingue esattamente il
primo dal secondo, e quale caso limite li separa*. Se non emerge un caso limite, la
distinzione non è stata capita.

**Occorrenze registrate**
- [2026-09-15] `FI2` 01: collaudo e progetto fusi. Sul caso del bus 33, che il docente usa proprio
  per separarli, ha risposto che «un collaudo più estremo» avrebbe trovato l'errore; l'errore era
  nel modello del dominio, e i test scritti su quel modello passano tutti. Evidenza:
  `corsi/FI2/grezzi/grezzi_FI2_01.md`, autoverifica 3.
- [2026-09-15] `FI2`: commit e push fusi in un gesto solo. Lanciata a mano solo la prima metà del
  comando proposto (`git commit … && git push`), ha dichiarato «commit fatto, ora procediamo»
  considerando il lavoro al sicuro; su GitHub non c'era ancora nulla, e il push è partito solo più
  tardi su sua richiesta esplicita. È la stessa distinzione SVN/Git della sl. 7 del modulo 01: in
  Git il commit è locale, il push è il secondo passo. Evidenza: trascrizione del 2026-09-15
  («commit fatto, ora procediamo» → «ottimo, pusha tutto su github»);
  `corsi/FI2/appunti/appunti_01_linguaggi_infrastrutture.md` §2.
- [2026-09-16] `FI2` 01, verifica a voce: black-box / white-box distinti per *cosa controlla* il
  test («guardare come lavora invece del risultato») anziché per *da dove nasce il caso* (specifica
  vs codice); un collaudo povero, con un solo caso fortunato, scambiato per un limite del black-box.
  Nella stessa verifica l'error JUnit collocato «nella struttura» invece che nell'esecuzione.
  Recuperato con guida (caso white-box `(4, 4)` sul confine del `>`). Evidenza: `stato/giornata.md`
  del 2026-09-16 → `log/giornate.md`.
- [2026-09-16] FI2 02, verifica a voce: tre coppie vicine fuse. `char` e byte: U+1F608 = «4 char
  credo» (sono 2 `char`, coppia surrogata; 4 sono i byte in UTF-8). Eseguibile ed eseguibile dal
  SO: l'EXE di `cc` detto «vero e proprio eseguibile», come se il `.class` lo fosse meno, e legato a
  «un ambiente identico» invece che allo specifico sistema operativo. Verso della conversione:
  `float → double` e `double → float` scambiati (d.4). Evidenza: trascrizione del 2026-09-16
  pomeriggio («4 char credo»; «un vero e proprio eseguibile .exe, che fa affiamento sul trovare un
  ambiente identico»); `stato/giornata.md`, verifica 02 d.3–d.5.
- [2026-10-01] FI2 LAB04b: `length` (fine fisica) e dimensione logica (primo `null`) fuse: il
  ciclo `i < fs.length-1` scritto «per non andare nei valori nulli», e l'ultimo elemento logico
  cercato in `fs[fs.length]` / `fs[fs.length-1]`. Dettaglio nella sezione FI2. Evidenza:
  trascrizione del 2026-10-01, 17:18; `stato/giornata.md` 17:17.
- [2026-10-02] FI2 LAB04c: capacità fisica e contenuto logico ancora non separati nel costruttore
  `(int)`. Lo pensa come «vuota con una dimensione fisica data come campo» da «riempire con `put`»,
  e tiene il numero in un campo `physicalSize` invece di leggere la capacità da `innerContainer.length`;
  il «logicamente vuota» (`size = 0`) non c'è. Recuperato col modello a scaffale. Da notare in
  positivo: davanti a `Frazione.size` da solo ha detto «ho length ma non credo vada bene», cioè la
  distinzione fisica/logica sul conteggio oggi l'ha vista da sé. Evidenza: trascrizione del
  2026-10-02 («riempirla con put? o cosa?», «sono veramente confuso»); `stato/giornata.md` 12:40.
- [2026-10-02] `FI2` LAB04c: stessa fusione fisico/logico in tre punti dopo il costruttore. `size()` scritto
  contando i `null` dall'inizio invece di leggere il campo `size` («il for mi sembra giusto»); poi
  «il vettore è già sistemato in modo che dimensione fisica e virtuale siano uguali», vero solo col
  costruttore `(Frazione[])`; infine `toString` con l'ultimo elemento scritto fuori dal ciclo
  (`innerContainer[size-1]`), che rompe con `size` 0. Evidenza: trascrizione del 2026-10-02 pomeriggio;
  `stato/giornata.md` 15:40, 17:37.
- [2026-10-05] FI2 LAB05: stato dell'oggetto e dati della singola chiamata fusi. Davanti a
  `emettiTicket(inizio, fine)` non sapeva come dare l'orario al `Ticket` «da una classe che non
  riceve l'orario di inizio e fine sosta» (il `Parcometro` ha la `Tariffa` per tutta la vita, gli
  orari arrivano come parametri del metodo). Recuperato con la spiegazione di Claude. Evidenza:
  trascrizione del 2026-10-05 («come inizializzo un ticked da una classe che non riceve l'orario
  di inizio e fine sosta?», «non so che valori di inizio e fine sosta dargli»).
- [2026-10-05] FI2 LAB05 p2: giorno di partenza e giorno che avanza fusi in `calcolaCostoSuPiuGiorni`. La
  tariffa dei giorni interi letta da `da.getDayOfWeek()` (sempre il venerdì: ven→gio dà 99,75 invece di
  243,75); poi `giorno` inizializzato a `da` con il `plusDays(1)` rimasto nella condizione del `while`
  (mercoledì saltato, 207,75); poi, dopo il cambio, la tariffa del ramo «stesso giorno» presa da `giorno`
  (che ormai è il giorno dopo), mar 7:30→15:00 dà 9,75 invece di 3,25. Evidenza: trascrizione del
  2026-10-05 (risposte di Claude dopo «fatto tutto controlla» e «fatto, controlla»: «`da` non cambia mai», «hai tenuto il `plusDays(1)` di
  prima», «la riga dello stesso giorno ha usato `giorno`»); `confronto_LAB05.md` «Cosa porto via (parte 2)» 3.

### 2. Fermarsi al primo indizio
Considera risolto un esercizio al primo risultato plausibile, senza verificare che spieghi
**tutti** i dati del problema. Emerso su analisi di traffico in Sicurezza.

**Contromisura**: far quadrare i numeri prima di concludere. Un esercizio è chiuso quando
ogni dato dell'enunciato è stato usato o esplicitamente scartato con motivazione.

**Occorrenze registrate**
- [2026-09-16] FI2 02, verifica d.4: su `float f = 3.54;` / `double x = 3.54F;` ha applicato l'idea
  giusta (conta la perdita di informazione) senza verificarla sulle due righe, e ha concluso a verso
  invertito («la prima riga non prevede perdita di precisione del dato, mentre la seconda riga si»);
  il dato decisivo, il suffisso `F` presente in una riga sola, non è stato usato benché la domanda
  chiedesse esplicitamente il tipo del letterale. Evidenza: trascrizione del 2026-09-16 pomeriggio;
  `stato/giornata.md`, verifica 02 d.4.
- [2026-09-30] FI2 LAB02: costruttore di `Frazione` dato per finito sulla console vuota di
  `FrazioneTest` («fatto, console vuota, controlla tu»), ma `new Frazione(0, -5)` dava `0/0`. Il caso
  numeratore 0 lo aveva sollevato lui stesso pochi minuti prima («e le frazioni con 0 al
  numeratore?») e non l'ha provato sul proprio codice: test verde preso come prova di correttezza.
  Evidenza: `stato/giornata.md` 15:46; trascrizione del 2026-09-30.
- [2026-09-30] FI2 LAB02: `mcm` scritto `a*b - mcd(a,b)` e consegnato senza provarlo sull'esempio
  appena svolto in chat (4 e 6 → 12; la sua formula dà 22) né sulla coppia di verifica proposta (6 e
  9 → 18); `FrazioneTest` verde perché nessun test usa `mcm`. Nella spiegazione di Claude «togli la
  parte comune» era ambiguo, ma i numeri per accorgersene erano sotto mano. Evidenza:
  `stato/giornata.md` 15:59; `svolti/LAB02_Frazione/confronto_LAB02.md` §7.
- [2026-10-01] FI2 LAB04b: per due volte ha dichiarato risolto il test `0/6` senza lanciare
  `FrazioneTest`, ogni volta dopo aver modificato un metodo che il test non chiama: prima `.minTerm()`
  aggiunto alla `FrazLib` del 04a («risolto riducendo le somme a minimi termini»; `minTerm` lascia
  comunque `0/36`), poi `sumWithMcm` dentro `sum(Frazione[])` («sum usa sumconmcm quindi dovrebbe
  funzionare ora»), benché Claude avesse già detto che quel passaggio «non tocca il caso `0/6`».
  Evidenza: trascrizione del 2026-10-01, 16:45 e 17:31; `stato/giornata.md` 17:16.
- [2026-10-02] `FI2` LAB04c: `remove` consegnato come finito con `testRemove` verde, ma con tre scarti di
  uno (`index <= size`, ciclo `i < size`, azzerata `[size]` invece di `[size-1]`); il test passa perché
  oltre `size` c'è un `null` che si compensa. Il caso con array pieno non è stato provato da lui prima
  di consegnare. Evidenza: codice letto alle 16:50; `stato/giornata.md` 17:00.
- [2026-10-05] FI2 LAB05: in `calcolaCosto` il minimo confrontato con `minutiSosta` (durata totale)
  invece che con `minutiDaPagare` (dopo la franchigia): `H1f` 10:00→11:30 dà 0,25 € invece di 0,50 €.
  Dichiarato finito con test verdi («ma già tutti i test sono verdi nel mio eclipse»), mantenuto dopo
  due segnalazioni di Claude, corretto solo più tardi. Il caso da 90 minuti non è nello startkit e non
  l'ha provato a mano; la regola (slide 8, «sottrarre franchigia, poi minimo») era sotto mano.
  Evidenza: `svolti/LAB05_TicketSosta/confronto_LAB05.md` §1; trascrizione del 2026-10-05.
- [2026-10-05] FI2 LAB05 p2: franchigia nel caso a più giorni dichiarata risolta senza verifica. Claude aveva
  mostrato che il primo pezzo partiva ancora da `da.toLocalTime()` (franchigia assente, `ven→sab` 60,75 invece
  di 60,25); Lorenzo: «ma la franchigia dovrebbe starla contando», poi, dopo la spiegazione, «ok direi
  risolto» senza modificare né rilanciare il test; il file non era cambiato e il test restava rosso («Non è
  risolto», dopo la lettura del file). Il calcolo a mano 8,25 vs 7,75 era già in chat. Evidenza:
  trascrizione del 2026-10-05 («ok direi risolto», poi «ho sistemato i tre punti»).

### 3. Autenticazione vs. autorizzazione
Distinzione teoricamente posseduta che scivola in pratica.
**Contromisura**: per ogni meccanismo chiedersi — *stabilisce chi sei, o cosa puoi fare?*

### 4. Parafrasi al posto della formulazione esatta
Dove la fonte usa una formulazione precisa, riformularla la degrada.
**Contromisura**: `[fonte: <fonte>]` sulle affermazioni riprese alla lettera.

**Occorrenze registrate**
- [2026-09-16] FI2 02, verifica d.5: Unicode detto «codifica come scrivere tutti i caratteri» e UTF
  «codifica come interpretarli per il calcolatore», al posto di *Unicode numera i caratteri (code
  point)* / *UTF mappa i code point in sequenze di byte*; la distinzione c'è nella sostanza ma la
  parafrasi la sfuma. In d.4 il cast descritto come dichiarazione di volontà senza il termine del
  docente, **Design Intent**. Evidenza: trascrizione del 2026-09-16 pomeriggio; `stato/giornata.md`,
  verifica 02 d.4–d.5.
- [2026-09-21] `FI2` 01, ripasso: due formule del docente non recuperate benché la domanda le
  chiedesse. Sl. 73 «standardizzare il linguaggio non basta» / «comunità incomunicabili»: al loro
  posto l'argomento della portabilità dell'eseguibile. Sl. 94 (definizione di «eseguibile»):
  «non mi ricordo la frase». Sl. 81: sostanza corretta ma con «versatilità» e «ottica scalabilità»
  al posto di «(piccolo) prezzo per questo passo extra» / «i vantaggi sono molto superiori al costo»
  / «massimamente riusabile». Evidenza: `stato/giornata.md` del 2026-09-21, ripasso 01 d.2 e d.5.

### 5. Inversione del verso in una relazione asimmetrica
`[promosso a trasversale il 2026-09-21, seconda occorrenza]` Davanti a una coppia A/B in cui una
proprietà vale per uno solo dei due, Lorenzo coglie *che* la proprietà è in gioco ma ne assegna il
verso a caso — e poi costruisce il resto del ragionamento sul verso sbagliato, senza che nulla lo
contraddica. È diverso dal pattern 1: la distinzione **è** stata capita, è l'orientamento che salta.

**Contromisura**: quando la risposta ha un verso, non dichiararlo a memoria — derivarlo da un caso
concreto verificabile. *Chi contiene cosa? Chi ha più bit? Chi ha bisogno dell'altro per esistere?*
Un verso che non si appoggia a un caso è un lancio di moneta.

**Dove si ripresenterà**: ogni conversione fra tipi numerici (`FI2`, `CALC`); ampiezza di banda e
bit rate (`TLC`); guadagno e attenuazione in dB (`ELT`, `ELN`); incapsulamento fra livelli di stack
— chi imbusta chi (`RETI`); prerequisiti fra moduli e dipendenze fra classi (`IDS`).

**Occorrenze registrate**
- [2026-09-16] `FI2` 02 d.4: `float f = 3.54;` / `double x = 3.54F;` con la perdita di precisione
  attribuita alla riga sbagliata. Già registrato sotto il pattern 2.
- [2026-09-21] `FI2` 01, ripasso d.4: alla domanda «dentro il JAR e dentro l'EXE ci sono le
  librerie?» ha risposto «dentro il jar sì e nell'exe no». È l'opposto: l'EXE è autocontenuto per
  collegamento statico, il JAR non contiene l'infrastruttura e la collega dinamicamente a run-time
  (sl. 78, 82–83). Sulla base del verso invertito tutta d.4 è caduta, incluso il punto che il verso
  giusto rende ovvio: **un solo file basta *proprio perché* non è autocontenuto**. Evidenza:
  `stato/giornata.md` del 2026-09-21, ripasso 01 d.4.
- [2026-09-30] FI2 LAB03: due versi invertiti nello stesso codice. In `sumWithMcm` e `sub` il
  fattore di conversione scritto `den/mcm` invece di `mcm/den` (su `1/4 + 1/8`: `4/8` fra `int` fa 0,
  risultato `1/8`); in `sub` in più `n1` (da `f`) − `n2` (da `this`), cioè `f − this` invece di
  `this − f`, con nomi `n1`/`n2` che nascondono la provenienza. Nessuno dei due versi era derivato
  da un caso: il conto a mano su `1/4 + 1/8` li avrebbe mostrati entrambi. A `/chiudi` Lorenzo
  dichiara di non avere chiara la matematica dell'mcm, che è la base da cui il verso si deriva.
  Evidenza: codice letto alle 17:26 (`int n2 = ((this.den/mcm)*this.num);`, `new Frazione(n1-n2,
  mcm)`); `stato/giornata.md` 17:26 e 18:02; `svolti/LAB03_Frazione/confronto_LAB03.md` §2.

---
- [2026-10-02] `FI2` LAB04c: due versi invertiti in `put` e `get`. Fattore di crescita scritto come somma
  (`length + DEFAULT_GROWTH_FACTOR`, con capacità 3 dà 5) invece del prodotto; condizione di indice non
  valido con `&&` (`index < 0 && index >= size`, mai vera) invece di `||`. Entrambi derivabili da un caso
  a mano (capacità 3 → 6; indice 1 su `size` 1). Evidenza: codice letto alle 15:35 e 16:20;
  `stato/giornata.md` 15:40, 16:30.
- [2026-10-08] CALC: 02p §4, causa del «uno solo acceso» attribuita al verso sbagliato: «lavorano
  opposti, quindi un chip acceso "spegne" GLI ALTRI». Ha colto che la proprietà è in gioco (un solo
  chip con l'uscita attiva), ma ha dato il comando ai chip invece che al decoder: è il decoder ad
  accendere un solo `CS`, e gli altri restano in Z perché il loro `CS` è spento, non perché un altro
  chip li spegne. Nella stessa risposta «opposti», vero solo con 2 chip, preso come regola (con 4 chip
  vale «al massimo un CS a 1»). Evidenza: trascrizione del 2026-10-08 («un chip acceso "spegne" GLI
  ALTRI» → «la causa è al contrario»); `corsi/CALC/grezzi/traccia_02p_2026-10-08.md`, Inciampi.

## Per corso

### `LAS` — Amministrazione di Sistemi (bash/Linux)
- Spazi obbligatori nelle condizioni: `[ ! -d "$x" ]`, non `[ !-d "$x" ]`.
- Loop incompleti: manca `done`.
- Shebang assente o incompleto.
- Confusione fra contare *righe* (`grep -c`) e contare *occorrenze* (`grep -o | wc -l`).
- **Contromisura**: testare con casi limite prima di fidarsi della logica.

### `FI2` — Fondamenti di Informatica T-2
- [2026-09-15] Compilazione ed esecuzione fuse: ha attribuito l'*error* di JUnit a un problema
  «sintattico» → causa: non separa le due fasi, e un errore di sintassi non arriva mai ai test
  (il codice non compila) → correzione: non compila = nessun test; compila e l'asserzione non
  torna = failure; compila ed esplode un'eccezione a run-time = error. Evidenza:
  `corsi/FI2/grezzi/grezzi_FI2_01.md`, autoverifica 2. **Candidato trasversale** (è il pattern 1
  applicato a due fasi): da promuovere se si ripresenta su un altro corso.
- [2026-09-15] Terminologia imprecisa sul collegamento: «scaricati» per le librerie caricate
  dinamicamente a run-time, «hardcodati» per il collegamento statico → correzione: usare *collegamento
  statico / dinamico*; «scaricare» è ciò che fa un build tool dalla rete. Evidenza: autoverifica 5.
- [2026-09-15] Risposta alla domanda posta solo a metà: all'autoverifica 1 ha descritto la
  *soluzione* (organizzazione industriale, progetto, tracciamento delle versioni) senza nominare la
  coppia **in-the-small / in-the-large**, che la domanda chiedeva esplicitamente → causa: risponde
  con ciò che ricorda del contenuto invece che con ciò che la domanda chiede, e salta il problema
  che genera la soluzione → correzione: rileggere la domanda punto per punto prima di consegnare, e
  su una domanda a due parti verificare di aver coperto entrambe. Evidenza:
  `corsi/FI2/grezzi/grezzi_FI2_01.md`, autoverifica 1 (esito «parziale»);
  `appunti_01_linguaggi_infrastrutture.md` §1. **Candidato trasversale**: da promuovere se si
  ripresenta su un altro corso.
- [2026-09-16] Ricorrenza, stesso corso: nella verifica a voce di 01 ha risposto a metà due volte —
  failure/error senza dire *dove cercare* l'errore, black-box/white-box senza dare un caso white-box.
  In entrambi i casi la seconda parte, richiesta, è arrivata corretta o quasi. Resta candidato
  (nessun altro corso ancora).
- [2026-09-16] Ricorrenza, stesso corso (terza sessione): nella verifica a voce di 02, con le parti
  numerate da Claude nella domanda, ha risposto a metà su quasi ogni domanda — d.1 solo parte 1 di 3;
  il «perché» della domanda di controllo non dato; d.2 una risposta sola per l'installazione di due
  comandi e «cosa produce» risposto con cosa *fa* `javac`; d.4 tipo del letterale non nominato,
  sintassi del cast assente; d.5 «4 char credo» senza perché. Le parti mancanti, richieste, sono
  arrivate corrette dopo la guida. Evidenza: trascrizione del 2026-09-16 pomeriggio («Però hai
  risposto solo alla prima delle tre parti»); `stato/giornata.md`, verifica 02 d.1–d.5. Resta
  candidato (nessun altro corso ancora).
- [2026-09-16] Ricorrenza di «compilazione ed esecuzione fuse», sul piano dell'installazione: alla
  verifica 02 d.2 «servono installati JDK e gli strumenti per sviluppatori di java» — JDK dato per
  entrambi i comandi, e JDK e strumenti di sviluppo detti come due cose (sono la stessa) → causa: non
  lega ogni strumento alla sua fase (`javac` è sviluppo → JDK; `java` esegue un `.class` già
  compilato → JRE) → correzione recuperata con guida («per javac serve JDK e per java serve JRE»),
  ma senza i perché. Già in verifica 01 d.4 aveva parlato di «strumenti da sviluppatore» senza
  nominare JDK/`javac`. Evidenza: trascrizione del 2026-09-16; `stato/giornata.md`, verifica 01 d.4
  e 02 d.2.
- [2026-09-16] A `java` passato un file invece di una classe: «il secondo riceve quale programma
  eseguire, in questo caso il file Esempio1 precedentemente compilato»; alla richiesta esplicita
  («cosa riceve il secondo») ha dichiarato di non saper rispondere → causa: non separa il nome del
  file (`Esempio1.class`, prodotto da `javac`) dal nome della classe che contiene il `main`
  (`Esempio1`, che si passa a `java`, senza estensione) → correzione: `java <NomeClasseColMain>
  args…`; la JVM cerca da sé il bytecode (prova: `Esempio1.kt` → `kotlin Esempio1Kt`). Recuperato
  sul controllo `java Esempio1.class alfa`. Evidenza: trascrizione del 2026-09-16 pomeriggio;
  `stato/giornata.md`, verifica 02 d.2.
- [2026-09-16] Servizio chiesto all'array: età media di più persone scritta `persone[].getMediaEta`
  → causa: dà l'operazione su più entità alla pari al contenitore, che non è un'entità a cui si
  possono aggiungere metodi («non possiamo aggiungere un metodo alla classe `[]`», LAB04) →
  correzione: operazione di un solo soggetto → metodo di quel soggetto (`persona.getNomeCompleto()`);
  operazione fra più soggetti alla pari → ente terzo, funzione statica di libreria
  (`PersonaLib.mediaEta(persone)`, come `FrazLib.sum`, `Math.sin`). Nella stessa risposta chiamate
  scritte senza parentesi. Evidenza: trascrizione del 2026-09-16 pomeriggio, controllo di d.1.
- [2026-09-16] Tipo del letterale non riconosciuto dalla sintassi: in d.4 verso della conversione
  invertito (`float f = 3.54` detto senza perdita, `double x = 3.54F` con perdita) → causa: non legge
  il suffisso — `3.54` senza suffisso è `double`, `3.54F` è `float` — e quindi non può stabilire il
  verso; Lorenzo stesso dichiara «mi è chiaro come funziona il meccanismo, ma non come riconoscere a
  livello di sintassi quando si perdono informazioni» → correzione: prima il tipo del letterale dal
  suffisso, poi il confronto con il tipo della variabile (più piccolo ← più grande = perdita, serve
  `(float)`, Design Intent). Da allenare su righe concrete in `02x`. Evidenza: trascrizione del
  2026-09-16 pomeriggio; `stato/giornata.md`, verifica 02 d.4 e controllo non svolto.
- [2026-09-21] Ripasso 01 d.2: due argomenti distinti del modulo fusi in uno. Alla domanda sul C++
  come controesempio (sl. 73, *standardizzazione dell'ecosistema*) ha risposto con l'argomento della
  *portabilità dell'eseguibile* (§6, collegamento statico/dinamico) → causa: risponde con ciò che
  ricorda del contenuto invece che con ciò che la domanda chiede — quarta ricorrenza dello stesso
  meccanismo, stesso corso → correzione data col caso limite che separa le due cause: due programmi
  C++ per lo stesso SO, con librerie dinamiche presenti su entrambe le macchine, sono portabili e
  restano incomunicabili se usano librerie di stringhe diverse.
- [2026-09-21] Ripasso 01 d.4: **JRE** non nominato («il Jqualcosa, non me lo ricordo bene»), pur
  avendo descritto correttamente la funzione dello strato locale che adatta il bytecode. Terza
  sessione in cui i nomi dell'infrastruttura non arrivano (cfr. verifica 01 d.4 e 02 d.2 del
  2026-09-16): il meccanismo c'è, l'etichetta no. Manca anche la formula «unico strato dipendente
  dalla piattaforma» (sl. 84). Nella stessa risposta, «compilandolo» per ciò che la JVM fa al
  bytecode, che è già compilato.
- [2026-09-25] Sesta ricorrenza della risposta a metà, stesso corso. Ripasso 01, domanda in due
  parti esplicite (a: nomi delle due relazioni UML; b: cosa cambia nel codice Java): data solo la a)
  — «generalizzazione la continua, implementazione di interfaccia la tratteggiata», corretta. Alla
  richiesta della b) è arrivata solo la metà sull'interfaccia («devo scrivere tutti i metodi da
  zero», corretta), non quella su `extends`/ereditarietà. Il pattern è ormai stabile su FI2: risponde
  alla prima parte e considera chiusa la domanda. Resta candidato trasversale (nessun altro corso
  ancora aperto per verificarlo). Evidenza: `stato/giornata.md` del 2026-09-25.
- **[2026-09-21] Superato — black-box / white-box.** Nel ripasso 01 d.3 il criterio è stato applicato
  correttamente: caso `eta = 18` su `return eta > 18;` classificato white-box **perché nato dalla
  lettura dell'operatore**, cioè per origine del caso e non per cosa il test controlla. Failure/error
  pure solido, con la motivazione giusta. Supera l'occorrenza del 2026-09-16 (trasversale n. 1).
- **[2026-09-21] Superato — commit e push.** Ripasso 01 d.1: distinzione tenuta separata e formulata
  correttamente senza guida. Supera l'occorrenza del 2026-09-15 (trasversale n. 1).
- [2026-09-30] Catena `if (i > 0) … else if (i < 0)` nel costruttore, senza ramo per `i == 0` →
  causa: i rami non coprono tutti i valori dell'input, e Java non lo segnala perché i **campi**
  hanno già il default `0` (una variabile locale non compilerebbe) → correzione: il costruttore
  deve lasciare l'oggetto valido per ogni input; ciò che è uguale in tutti i rami si assegna fuori
  dai rami (`this.den = Math.abs(den)`), nei rami solo ciò che cambia (forma del docente con
  `negativo ? … : …`). Evidenza: trascrizione del 2026-09-30, versione con `i > 0`;
  `confronto_LAB02.md` §1.
- [2026-09-30] Stampa dentro `equals` (`System.out.print(… + " sono equivalenti")`) → causa: il
  metodo che *risponde* vero/falso usato anche per *comunicare*, per cui nel `Main` la frase
  compariva due volte → correzione: un predicato restituisce il `boolean` e basta; la stampa la fa
  il chiamante. Riconosciuto da Lorenzo sul suggerimento di Claude. Evidenza: trascrizione del
  2026-09-30, prima versione di `Frazione.java`.
- [2026-09-30] Proposto di far restituire 1 a `mcd` quando il numeratore è 0, dicendo che `0/5`
  ridotta «fa sempre 1» → causa: valore della frazione (0), denominatore normalizzato (1) e mcd
  (`mcd(0,5) = 5`) fusi in un solo «1»; e il crash si toglie falsando la funzione di libreria
  condivisa invece di proteggere la chiamata → correzione: caso speciale gestito nel chiamante
  (`minTerm`, prima di chiamare `mcd`); una funzione di libreria non si fa mentire per evitare
  un'eccezione. Evidenza: trascrizione del 2026-09-30 («fa sempre 1 no? quindi un controllo in mcd
  che dia 1 se num = 0?»).
- [2026-09-30] Ridondanze nel codice: `if (cond) return true; else return false;` al posto di
  `return cond;`; `this.den = Math.abs(den)` ripetuto in entrambi i rami; `Math.abs` sul
  denominatore in `minTerm`, già garantito positivo dal costruttore → causa: non si chiede, riga per
  riga, *«questo lo so già?»* (Lorenzo: «scrivo ancora come su C») → correzione: togliere ciò che è
  già noto, chiarezza prima della brevità. Da cercare nei prossimi confronti. Evidenza:
  `confronto_LAB02.md` §1, §3, §5; `stato/giornata.md` 16:09.
- [2026-09-30] `getDouble` scritto `double val = this.num / this.den;` → `0.0` per ogni frazione
  fra −1 e 1 → causa: crede che il tipo della variabile a sinistra decida la divisione; invece il
  tipo di `/` lo decidono gli operandi, e `int / int` tronca prima dell'assegnamento (stessa
  famiglia della riga del 2026-09-16 sul tipo del letterale: il tipo di un'espressione si legge
  dagli operandi, non dalla destinazione). La stessa troncatura silenziosa ha nascosto `den/mcm`
  in `sumWithMcm` → correzione: cast su un operando **prima** della divisione, `(double) num / den`.
  Correzione data in chat su richiesta. Evidenza: codice letto alle 17:47; output di `MainFrazione`
  «valore reale associato a : 3/12 è 0.0»; `confronto_LAB03.md` §5.
- [2026-09-30] mcm, seconda sessione su due nello stesso giorno: in LAB02 formula `a*b - mcd`, in
  LAB03 fattore di conversione `den/mcm` → causa dichiarata da Lorenzo a `/chiudi`: «non mi è stata
  troppo chiara la matematica alla base del mcm […] da essermela scordata» — l'aritmetica di base
  manca, e senza di lei né la formula né il verso si possono derivare → correzione: `mcm = a·b/mcd`
  perché il prodotto conta due volte i fattori comuni; il fattore per portare `n/den` al
  denominatore `mcm` è `mcm/den`, «quante volte `den` sta in `mcm`»; verificare sempre su 4 e 6
  (mcm 12, fattori 3 e 2). Da riprendere prima di rifare LAB02–03 a freddo. Evidenza:
  `stato/giornata.md` 15:59 e 18:02; trascrizione LAB03, risposta a `/chiudi`.
- [2026-09-30] Ricorrenza delle ridondanze, nel LAB successivo allo stesso richiamo: `div` rifà a
  mano il prodotto invece di riusare `mul`, e costruisce `f.reciprocal()` due volte; `compareTo`
  calcola `getDouble()` quattro volte e sottrae prima di confrontare. Criterio da aggiungere a
  «questo lo so già?»: *«un metodo della classe lo fa già?»*. Evidenza: `confronto_LAB03.md` §3–§4;
  `svolti/LAB03_Frazione/src/Frazione.java`.
- [2026-10-01] LAB04a: `FrazLib.mul` copiata da `sum` senza adattarla, con due righe sbagliate
  (accumulatore da `new Frazione(0)` e chiamata `.sum(f)`), e consegnata («ho scritto […] sia sum
  che mul, come procedo») senza lanciare `FrazLibTest` → causa: dopo il copia-incolla del metodo
  gemello non rilegge riga per riga per la nuova operazione; la domanda di Claude sul valore di
  partenza, posta esplicitamente «per `sum` […] e per `mul`», era stata saltata, e la risposta è
  arrivata solo per `sum` → correzione: dopo ogni copia chiedersi per ogni riga «ha senso per
  *questa* operazione?»; l'elemento neutro dipende dall'operazione (`0` per `+`, `1` per `×`).
  Corretta dopo due domande guida. Evidenza: `stato/giornata.md` 16:16; trascrizione del
  2026-10-01 14:16–14:20; `confronto_LAB04a.md` §1–2.
- [2026-10-01] LAB04a: credeva di dover dichiarare il tipo array da qualche parte («non ho
  introdotto il concetto di array di frazione da nessuna parte») → causa: non sa che per ogni
  classe il tipo `T[]` esiste già, e confonde il tipo con l'array concreto, che crea e passa il
  chiamante (qui il test) → correzione: `Frazione[]` esiste da sé; dentro `sum(Frazione[] fs)`
  servono solo `fs.length`, `fs[i]` e il *for each* (07 sl. 17–19). Evidenza: trascrizione del
  2026-10-01, 13:43.
- [2026-10-01] LAB04a (parte nel cloud): metodo d'istanza e `static` non distinti — non coglieva
  la differenza fra `f[1].sumArray(...)` e `FrazLib.sum(...)` né quali «due mondi» convivano in
  `Frazione` → causa: stessa famiglia della riga del 2026-09-16 su `persone[].getMediaEta`: non
  lega il metodo al soggetto su cui opera → correzione: criterio «il metodo usa `this`?» — sì →
  d'istanza, no → `static`. Lorenzo lo dichiara chiaro (13:43 e a `/chiudi`), ma le tre domande di
  verifica sono state saltate: **comprensione dichiarata, non verificata**; il banco di prova è
  LAB04b, dove i due mondi stanno nella stessa classe. Evidenza: `stato/giornata.md` 15:23 e 15:47.
- [2026-10-01] LAB04b: cicli su un array riempito a metà con `i < fs.length-1` «per non andare nei
  valori nulli» (salta l'ultima cella fisica e alla cella 4 va comunque in `NullPointerException`),
  poi `i < fs.length` senza controllo sul `null`; in `convertToString` l'ultimo elemento cercato in
  `fs[fs.length]` (sempre `ArrayIndexOutOfBoundsException`) e poi in `fs[fs.length-1]` (`null` o
  indice `-1`) → causa: fine fisica (`length`, celle allocate) e fine logica (primo `null`, celle
  usate) trattate come una sola, e `-1` usato come se escludesse le celle vuote → correzione: ogni
  ciclo su un array a metà controlla entrambe, in quest'ordine: `i < a.length && a[i] != null`
  (sl. 28); l'ultimo elemento logico non si conosce finché non si incontra il `null`, quindi il
  separatore va *prima* di ogni elemento tranne il primo (`i != 0`). Lorenzo a `/chiudi`: «i
  problemi li ho avuti coi ragionamenti logici per operare con gli array, i valori nulli, dove
  finisce». Condizione data da Claude (gradino ③). Evidenza: trascrizione del 2026-10-01, 17:18 e
  17:20 (tabelle di Claude con NPE/AIOOBE); `confronto_LAB04b.md` §2 e «Cosa porto via».
- [2026-10-01] LAB04b: le tre `sum` di `Frazione` (d'istanza; statica su un array; statica a
  coppie) non distinte nel ragionare su un test: per il caso `0/6` ha modificato due volte un
  metodo che il test non chiama (prima la `FrazLib` del 04a, poi `sum(Frazione[])`), mentre il test
  passa da `setA[k].sum(setB[k])`, cioè dalla `sum` d'istanza → causa: non risale dal test al
  metodo davvero chiamato, e l'overloading rende uguali i nomi → correzione: partire dalla riga del
  test e seguire la chiamata; distinguere le `sum` per firma (argomenti e tipo restituito). Stessa
  famiglia della riga del 2026-10-01 su istanza/`static`. Evidenza: trascrizione del 2026-10-01,
  16:45 e 17:31 («sum usa sumconmcm quindi dovrebbe funzionare ora»); `confronto_LAB04b.md` §5.
- [2026-10-01] Settima ricorrenza della risposta a metà, ora **nel codice**: davanti a una
  correzione in due parti ne applica una sola. Detto che la condizione deve contenere «entrambi i
  controlli» (fine fisica e `null`), ha corretto solo `length-1` → `length`; detto per
  `convertToString` «la stessa condizione di `sum`, e la virgola prima», ha corretto il corpo e
  lasciato il ciclo `i < fs.length-1`. Resta candidato trasversale (nessun altro corso ancora).
  Evidenza: trascrizione del 2026-10-01, 17:19–17:28; `stato/giornata.md` 17:21 e 17:28.
- [2026-10-01] Terza ricorrenza delle ridondanze: in `size` `int size = 0;` ripetuto
  dall'inizializzazione del `for`; nelle somme a coppie `size(fA)` calcolata due volte (ogni volta
  scorre l'array, il costo che la sl. 29 segnala); `return risultato;` sulla riga della `}` del
  ciclo. Coerente con quanto dichiarato a `/chiudi`: fatica a trovare la forma «giusta» oltre che
  funzionante. Evidenza: `svolti/LAB04b_FrazioniDoubleFace/src/frazione/Frazione.java` (`size`,
  `sum`/`mul` a coppie); trascrizione del 2026-10-01, 17:38 e 17:41.
- [2026-10-02] LAB04c: costruttori che non portano l'oggetto in stato valido. Il `(int)` memorizzava
  il parametro in un campo `physicalSize` senza creare l'array, `size` assente; il `()` vuoto,
  quindi `innerContainer` sarebbe rimasto `null` e ogni `put` in errore → causa: il costruttore è
  visto come il posto dove «salvare il parametro», non dove costruire la rappresentazione interna;
  parametro del costruttore e campo della classe fusi (`physicalSize` non è un campo, la capacità
  è `innerContainer.length`) → correzione: ogni costruttore lascia `innerContainer` su un array
  vero e `size` coerente; `(int)` crea `new Frazione[n]` e pone `size = 0`; `()` delega con
  `this(DEFAULT_PHYSICAL_SIZE)`. Stessa famiglia della riga del 2026-09-30 sul costruttore che
  non copre tutti i casi. Evidenza: trascrizione del 2026-10-02 («gli ho scritti, ma sono
  veramente confuso», lettura del codice da parte di Claude); `stato/giornata.md` 12:40.
- [2026-10-02] LAB04c `put`: il nuovo array creato nel ramo del raddoppio resta in una variabile locale,
  mai assegnato a `innerContainer` → causa: non distingue la variabile locale `fs` dal campo che deve
  cambiare (il costruttore faceva già `innerContainer = …`, qui lo ha dimenticato) → correzione: dopo la
  copia, `innerContainer = fs;`; senza, la frazione aggiunta si perde e `get` lancia. Inserimento duplicato nei
  due rami → si fattorizza dopo l'`if`. Evidenza: codice letto alle 16:20; `stato/giornata.md` 16:30.
- [2026-10-02] LAB04c `remove`: tre scarti di uno insieme (`<= size`, ciclo `i < size`, azzeramento di
  `[size]`) → causa: gli estremi non sono derivati da un esempio con 4 celle (`[A,B,C,D]`, `remove(1)`)
  → correzione: valido `0 ≤ index < size`; ciclo fino a `size - 1` (legge `[i+1]`); azzerare `[size - 1]`.
  Evidenza: codice letto alle 16:50; `stato/giornata.md` 17:00.
- [2026-10-02] LAB04c `toString`: prima volta con `StringBuilder`; l'idea del separatore (virgola prima, tranne il
  primo) l'aveva già in `convertToString` ma qui ha scritto il ciclo fino a `size - 1` con l'ultimo fuori,
  e ha aggiunto un prefisso «Container: » non richiesto → causa: forma del metodo ripresa dalla slide/stampa a
  video senza rileggere il formato della scheda (`[a, b, c]`) → correzione: tutto nel ciclo, `[`/`]`
  senza spazi. Evidenza: `stato/giornata.md` 17:37. Lorenzo ha anche chiesto di rinominare `size()` in
  `getSize()` per chiarezza: i test lo chiamano `size()`, il nome dei metodi lo fissa il diagramma.
- [2026-10-05] LAB05: `Ticket` scritto senza leggere i test come contratto: costruttore con parametri
  `(double costo, LocalTime fine, LocalTime inizio)` invece di `(inizio, fine, costo)` (non compila con
  `TicketTest` e `Parcometro`), e `getCostoAsString()` che restituiva `"Costo = " + costo` invece di
  `"3,50 €"` col formattatore valuta → causa: forma di firma e di output ricavata a memoria, non dal
  test che li fissa (stessa famiglia del `toString` del 2026-10-02) → correzione: prima di scrivere una
  firma o una stringa, leggere nel test ordine degli argomenti e valore atteso. Evidenza: tabella di
  Claude sul `Ticket.java` del 2026-10-05 (punti 1 e 3); `stato/giornata.md` 12:21.
- [2026-10-05] LAB05: API di `java.time`/`java.text` non recuperate: `NumberFormat.getCurrencyInstance(
  Locale.ITALY)` («mi sono bloccato»), `toHours` proposto per la durata, poi «non riesco a ottenere una
  durata in minuti partendo da DA e A» benché `Duration.between` l'avesse già scritto in `Ticket`;
  `toMinutes` (totali) vs `toMinutesPart` (parte) da distinguere; formattatori di data e orario
  copiati dalla slide 11 («mentirei se dicessi di non copiare diretto dalle slide»). Lorenzo ne trae
  la regola giusta: sono frammenti da prontuario, da trovare e incollare. Evidenza: trascrizione del
  2026-10-05.
- [2026-10-05] LAB05, dichiarato da Lorenzo a `/chiudi`: «sto iniziando a fare confusione con i processi
  interni alle funzioni»; capisce come si costruisce una classe, come si chiama un metodo, i tipi, ma
  non l'algoritmo che il docente richiede, e quando Claude lo spiega «mi sembra che tu mi stia dando
  indicazioni in un posto che non conosco» → causa: manca un modello di ciò che il metodo deve fare
  *prima* di scrivere (nei passi di `calcolaCosto`: durata → franchigia → minimo → ore, con l'ordine
  che conta); stessa difficoltà dichiarata il 2026-10-01 («ragionamenti logici per operare con gli
  array») → correzione da provare: disegnare i passi su un esempio numerico prima del codice
  (`/flusso`, nato oggi). Evidenza: risposta a `/chiudi` del 2026-10-05; piano a parole di Lorenzo
  («misuro la durata, converto in ore […] poi la durata minima […] non ho capito cosa fa la franchigia»).
- [2026-10-05] LAB05 p2: `da.plusDays(1);` scritto senza assegnare il risultato → causa: crede che il metodo
  modifichi l'oggetto, ma `LocalDate`/`LocalDateTime` sono immutabili e `plusDays` restituisce un oggetto nuovo
  che qui viene buttato; `da` resta uguale e la condizione del `while` resta vera per sempre (il test
  ven→gio 1/4 non termina) → correzione: `giorno = giorno.plusDays(1);`, il risultato va sempre assegnato (ordine
  nel ciclo: usa il giorno, poi avanza). Stessa famiglia della riga del 2026-10-05 sulle API di `java.time`.
  Evidenza: codice letto da Claude dopo «fatto tutto controlla»; `confronto_LAB05.md` «Cosa porto via (parte 2)» 2.
- [2026-10-05] LAB05 p2: `toString` di `ParcometroEvoluto` con `tariffa.toString()` dentro il ciclo → causa: chiama il
  metodo sull'array intero invece che sull'elemento; un array non ha un `toString` utile e stampa tipo e
  indirizzo (`[Lticketsosta.Tariffa;@6d06d69c`, sette volte); nello stesso metodo il ciclo con `i < 7` scritto a
  mano invece di `i < tariffa.length`, rimasto anche dopo il suggerimento → correzione: `tariffa[i].toString()`,
  e il limite del ciclo è `length`. Stessa famiglia di `persone[].getMediaEta`
  (2026-09-16): confonde il contenitore con i suoi elementi. Evidenza: trascrizione del 2026-10-05 (output
  mostrato da Claude dopo «ho scritto il toString, controlla»; «hai ancora `i < 7`»).
- [2026-10-05] LAB05 p2: il «minimo» non più riconosciuto tre ore dopo averlo sbagliato nella parte 1 («ma che è
  sto minimo, restiamo sulla nostra strada») → causa: nessun modello della regola in testa; la sequenza durata →
  franchigia → minimo → ore era stata seguita in parte 1 col codice sotto mano, senza essere interiorizzata (e il
  minimo scritto sulla durata sbagliata, riga del 2026-10-05); il blocco del minimo nel ramo «stesso giorno»
  l'ha scritto Claude → correzione da provare: disegnare i passi con un caso numerico prima di scrivere (`/flusso`,
  prontuario §3.13). Ricorrenza della riga «processi interni alle funzioni» del 2026-10-05. Evidenza:
  trascrizione del 2026-10-05 (risposta a «Scrivilo tu, con il metodo del debug»; «ma che è sto minimo»).

### CALC — Calcolatori Elettronici T
- [2026-10-08] 02p §2: taglia convertita in bit senza l'unità. RAM da 32 KB → «5 piedini perché 32 =
  2^5»; 64 MB → «2^6 × 2^4 = 10», poi «2», poi «7» → causa: della taglia legge solo il numero e lascia
  cadere l'unità, e il valore di M non lo conosce (lo pensa 2^4); 512 KB → 19 e 2 GB → 31 corretti da
  solo dopo la prima correzione → correzione: spezzare sempre in numero × unità e sommare gli
  esponenti, con K, M, G = 2^10, 2^20, 2^30 (32 KB → 15, 64 MB → 26). Evidenza: trascrizione del
  2026-10-08 («direi 5 piedini perchè 32 = 2^5», «64 quindi 2^6, immagino per 2^4, quindi 10»,
  «volevo dire 7 piedini»); `stato/giornata.md` 11:16, 12:17.
- [2026-10-08] 02, Decisione 1: binario letto senza i pesi. `1100` letto come 8 («pensavo che 1100
  fosse 8») e proposto come partenza di un chip da 8 byte in uno spazio da 16 (vale 12, non è multiplo
  di 8, e 12 + 8 esce dallo spazio); alla prova di conversione di `1010`, `0100`, `1110`: «non so
  farlo» → causa: manca la lettura posizionale (pesi 8 4 2 1), base data per scontata dalla lezione 02
  → correzione: sommare i pesi dove c'è un 1; partenza allineata = ultimi K bit a zero. Evidenza:
  trascrizione del 2026-10-08 («no, partirà da 1100», «pensavo che 1100 fosse 8»); traccia 02p,
  Inciampi.
- [2026-10-08] 02, Decisione 1: allineamento ridotto alle prime due posizioni. Per un dispositivo da 2
  byte «parte da 2 o da 0», ricalcando i due soli valori (0 e 8) appena visti per il chip da 8 → causa:
  la regola «base multipla della taglia» non è stata generalizzata, è stato copiato il numero di
  partenze del caso precedente → correzione: valgono tutti i multipli della taglia (da 2 byte in 16:
  0, 2, 4 … 14, cioè 2^3 posizioni per i 3 bit di selezione). Evidenza: trascrizione del 2026-10-08
  («un dispositivo da 2 byte, ha 1 bit e parte da 2 o da 0»).
- [2026-10-08] 02p §3: conteggio delle celle da 1. Indirizzo `0 11` → «palazzina B 4 appartamento»
  (la palazzina è giusta; `11` = 3) → causa: conta le celle come posizioni ordinali (la quarta)
  invece che col valore del numero binario, che parte da 0 → correzione: la cella *è* il valore dei
  bit bassi, da 0 (`00` … `11` = celle 0 … 3); su `1 01` subito dopo ha risposto «appartamento numero
  1», corretto. Evidenza: trascrizione del 2026-10-08; traccia 02p, Inciampi («si conta da 0»).
- [2026-10-09] Ricorrenza di «taglia convertita in bit senza l'unità» (2026-10-08), il giorno dopo: 02p
  §6, EPROM da 16K → «16 = 2^4», K di nuovo persa; corretto subito in 2^14 alla prima segnalazione
  («lo sottintendevo»). Terza taglia su quattro in due giorni in cui l'unità cade al primo colpo.
  Evidenza: trascrizione del 2026-10-09 («16 = 2^4»); `stato/giornata.md` 12:44.
- [2026-10-09] 02p §6: 2^14 scritto in binario con l'1 in fondo, «0000 0000 0000 001» → causa: non sa
  che base^n si scrive 1 seguito da n zeri, quindi non ha un modello di dove stia l'1 (subito dopo ha
  chiesto «perché 1 seguito da 14 zeri se era 2 alla qualcosa»); stessa famiglia della riga del
  2026-10-08 sul binario letto senza i pesi: manca la notazione posizionale → correzione: 2^n = 1 e n
  zeri, come 10^n in decimale; raggruppare a 4 **da destra** e completare a sinistra con zeri
  (`0100 0000 0000 0000` = `4000h`). Evidenza: trascrizione del 2026-10-09; `stato/giornata.md` 13:05.
- [2026-10-09] 02p §6: `10000h − 4000h` → «12000» → causa: non ha l'aritmetica in base 16 (dichiarato
  poco prima: «non so fare le somme in esadecimale»): il 16 − 4 = 12 della colonna è giusto, ma lo
  scrive come due cifre invece della cifra C, e l'1 che ha prestato non viene azzerato → correzione:
  in hex ogni colonna ha una sola cifra 0…F (12 = C); chi presta scende di 1; verifica inversa
  `C000h + 4000h = 10000h`. Evidenza: trascrizione del 2026-10-09 («quindi viene 12000»);
  `stato/giornata.md` 12:34, 13:12; `appunti/prontuario_CALC.md` §0.
- [2026-10-09] Ricorrenza di «binario letto senza i pesi» (2026-10-08) e della riga del mattino su 2^14,
  nel pomeriggio: 02p §6, `2000h` e `27FFh` scritti «00100000000000 e 0010100111111111», cioè `2000h`
  con 14 bit invece di 16 e il 7 reso `1001` (vale 9; 7 = `0111`). Le stringhe senza gruppi nascondono
  tutti e due gli errori, benché la consegna di Claude fosse «ogni cifra hex diventa 4 bit». Corretto
  scrivendo a gruppi di 4 con i pesi 8-4-2-1; dopo, `2800h`, `2FFFh`, `C000h`, `FFFFh` e `2400h`
  convertiti giusti da solo, sempre a gruppi. Evidenza: trascrizione del 2026-10-09 pomeriggio
  («00100000000000 e 0010100111111111»); `stato/giornata.md` 15:14.
- [2026-10-09] Ricorrenza di «taglia convertita in bit senza l'unità» (2026-10-08), in forma lieve: Prova
  tu 4, «512 = 2^19» — esponente giusto, l'unità caduta solo nella scrittura (512 da solo è 2^9). Nello
  stesso giro K tenuta e scritta su 2K («2 * 2^10 = 2^11») e 32 KB. Evidenza: trascrizione del
  2026-10-09 pomeriggio («quindi 32KB = 2^15 e 512 = 2^19»); `stato/giornata.md` 15:41.
- [2026-10-09] 02p Prova tu 4: regola dei piedini non recuperata («damn non mi ricordo come si faceva
  per i piedini»), venti minuti dopo aver contato gli 11 bit che cambiano in RAM_2; e già lì, davanti
  alla tabella dei fili, «quanti bit cambiano? torna con 2^11?» aveva avuto «non so rispondere» → causa:
  la regola del 2026-10-08 (§2) è rimasta una procedura a sé, non collegata ai bit di cella della
  finestra → correzione: piedini A = bit di cella = bit che cambiano fra primo e ultimo indirizzo =
  esponente della taglia, un solo numero visto da tre lati. Recuperato al primo richiamo. Evidenza:
  trascrizione del 2026-10-09 pomeriggio («fino ad A11 uguali ma non so rispondere alle altre due»,
  «damn non mi ricordo…»); `stato/giornata.md` 15:41.
- [2026-10-09] 02p Prova tu 3 e 5: dalla taglia non sa arrivare alla posizione nella memoria. Su 2K da
  `2800h`: «2K = 2^11, ma non so riconoscere a quali bit corrispondono in 2800h»; su 1 GB da `00000000h`:
  «so solo che 1GB = 2^30, come faccio a sapere dove finisce?» → causa: il blocco da 2^n non è visto
  come gli n bit più a destra (A0 … A(n−1)) che vanno da tutti 0 a tutti 1 sotto una firma fissa; in
  §6 la stessa lettura l'aveva fatta nel verso estremi → firma, e non la rovescia (taglia → estremi);
  giudizio di Lorenzo a `/chiudi`: fatica a «muoversi nella memoria» (dove finisce un blocco, ragionare
  per intervalli) → correzione: i bit bassi si contano da destra, da A0; ultimo indirizzo = primo con
  gli n bit bassi a 1 = primo + 2^n − 1 (1 GB da 0: 30 uni → `3FFFFFFFh`, verifica `40000000h − 1`);
  raggruppare a 4 da destra. Recuperato con guida. Evidenza: trascrizione del 2026-10-09 pomeriggio;
  `stato/giornata.md` 15:41, 15:52.

### Archivio — corsi chiusi
> Conservati perché i pattern sopravvivono al corso che li ha generati.

<details>
<summary>Diritto dell'Informatica — superato 16/06/2026</summary>

| Concetto | Errore | Correzione |
|---|---|---|
| Regolamenti UE | detti "non direttamente applicabili" | sono **direttamente applicabili** per definizione |
| Direttive UE | dette "ideali" | vincolanti quanto al risultato |
| Diritto d'autore | 70 anni = diritti morali | 70 anni = diritti **patrimoniali**; i morali sono imprescrittibili |
| Creative Commons | CC BY = pubblico dominio | CC BY ≠ pubblico dominio; **CC0** = rinuncia totale |
| Dati sensibili | capacità di identificare la persona | **natura dell'informazione** |
| Reati informatici | parafrasati anziché nominati | 615-ter = mera condotta, il danno non è richiesto |
| AI Act | lett. e) uguale a lett. a) | a) regole generali IA; e) regole specifiche modelli GPAI |

</details>

<details>
<summary>Laboratorio di Sicurezza Informatica — superato 17/07/2026</summary>

- `nmap`: porte con virgole `-p 22,80,3306`; `-sV` per version detection; `-p-` per porte
  non standard; `sudo` per ARP affidabile.
- `psql`: meta-comandi e SQL su righe separate; `\r` resetta il buffer.
- `scp` dal terminale locale, non da una sessione SSH attiva.
- Suricata: verificare sempre il traffico legittimo prima di scrivere regole; variabili
  custom senza `#` iniziale; nel JSON il campo è `signature_id`, non `sid`; `cat -A` per
  verificare i file scritti a mano.

</details>
