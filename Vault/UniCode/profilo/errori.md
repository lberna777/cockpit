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

---

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
