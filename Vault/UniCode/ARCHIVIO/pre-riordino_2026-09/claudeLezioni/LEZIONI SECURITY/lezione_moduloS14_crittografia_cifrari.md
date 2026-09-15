# Lezione — Modulo S14: Crittografia — Fondamenti, Cifrari Moderni e Rainbow Tables
**Corso**: Lab Sicurezza Informatica T
**Materiale**: `Introduzione_alla_crittografia_8_maggio.pdf`, `Cifrari_moderni_8-13_maggio.pdf`, `approfondimento_Rainbow_Tables.pdf` (tutti Prandini, `SLIDE TEORIA/SICINF/`)
**Prerequisiti**: S2 (Autenticazione — hash `password||salt`, `/etc/shadow`, proprietà one-way dell'hash vista con S-KEY, challenge-response asimmetrico)

---

## Obiettivo
Al termine di questa lezione Lorenzo deve saper distinguere con precisione da esame teorico: crittografia da steganografia; cifrari da codici; algoritmi pubblici da segreti; **cifrari simmetrici da asimmetrici**; **hash da cifratura** (la confusione più pericolosa del modulo); e le **tre tecniche d'attacco alle password — dictionary attack, brute force, rainbow table** — che sono il cuore concettuale a rischio di confusione. Deve inoltre saper enunciare cosa fanno DES, AES, RSA, MD5/SHA, cosa significa "sicurezza computazionale vs assoluta", e come una rainbow table cracca un hash nel dettaglio del meccanismo.

> ⚠️ Questo modulo non ha mai avuto una lezione o appunti prima d'ora: è teoria pura (nessun lab su VM associato lato S14; la parte pratica di crittografia vive in S13 TLS/OpenSSL e S15 gpg). L'esame teorico (40%) copre tutto questo, e la crittografia è la materia che più si presta a domande vero/falso secche del tipo "l'algoritmo X è simmetrico/asimmetrico".

---

## 1. A cosa serve la crittografia — il quadro delle proprietà

La sicurezza delle informazioni ha tre sfaccettature (le stesse viste in tutto il corso): **Confidentiality** (riservatezza), **Integrity** (integrità, con la sua sotto-proprietà **Authenticity**/paternità) e **Availability** (disponibilità). La crittografia è "un'elaborazione matematica e algoritmica della codifica delle informazioni" che interviene sulle prime due, in due modi radicalmente diversi:

- **Riservatezza → si PREVIENE la violazione.** Una rilevazione a posteriori sarebbe inutile: se un intruso (*eavesdropper*) ha già letto il messaggio, dirti dopo che l'ha letto non serve a niente. Quindi si altera il codice per renderlo incomprensibile a chi non ha diritto di leggerlo. **Meccanismo**: cifratura. **Visione**: la riservatezza è l'unica proprietà che *deve* essere protetta prima del fatto, perché il danno è irreversibile nell'istante stesso della lettura.

- **Integrità e autenticità → si RILEVA la violazione.** Qui invece prevenire è impossibile: non puoi impedire fisicamente a un intruso (*impostor*) di modificare o falsificare un messaggio sul canale. Quello che puoi fare è aggiungere al messaggio elementi che permettano al destinatario di *accorgersi* che è stato alterato. **Meccanismo**: hash, MAC, firme digitali. **Visione**: la sicurezza dell'integrità non è un muro, è un sigillo che si rompe in modo visibile.

Tieni fisso questo dualismo prevenire/rilevare: è la chiave di lettura di tutto il resto (la cifratura previene, l'hash rileva).

---

## 2. Crittografia, steganografia, codici — cosa NON è crittografia

La crittografia non è l'unica tecnica per proteggere un'informazione, e in una domanda a scelta multipla è facile confondere i vicini di casa.

- **Steganografia**: "l'arte e la scienza del comunicare senza che altri se ne accorgano". Non nasconde il *contenuto* del messaggio, nasconde l'*esistenza* del messaggio. Esempi storici: la tavoletta cerata di Demarato, lo schiavo "rapato" di Istieo (messaggio tatuato sul cuoio capelluto, coperto dai capelli ricresciuti), gli inchiostri invisibili. Tecnica moderna: modifica dei **bit meno significativi** di dati multimediali (LSB steganography — cambi l'ultimo bit di ogni pixel e l'occhio non se ne accorge, ma ci infili un messaggio). **Differenza chiave da esame**: la crittografia rende il messaggio illeggibile ma *visibile*; la steganografia lo rende invisibile ma, se scoperto, leggibile.

- **Codici** (≠ cifrari): sostituzione di **stringhe**, tipicamente parole intere ("l'aquila è atterrata" = "l'operazione è iniziata"). Sono limitati dal **dizionario**: capacità espressive ridotte (puoi dire solo ciò che è nel codebook) e complessità di rappresentazione. I cifrari, al contrario, lavorano su simboli elementari (lettere, bit) e possono cifrare *qualsiasi* messaggio.

**Tassonomia gerarchica** (da tenere a mente perché l'esame chiede spesso "X è un cifrario o un codice? classico o moderno?"):

```
Crittografia
 └─ Cifrari (vs Codici)
     └─ Moderni (vs Classici)
         └─ Algoritmi pubblici (vs Algoritmi segreti)
             ├─ A doppia chiave (asimmetrici)
             └─ A singola chiave (simmetrici)
```

---

## 3. Il cifrario per la riservatezza — notazione base

Due operazioni, sempre queste:
- **Cifratura** `E`: converte il testo in chiaro `m` (message/plaintext) in testo cifrato `c` (ciphertext). Si scrive `c = E(m)`.
- **Decifrazione** `D`: converte il testo cifrato in testo in chiaro. Si scrive `m = D(c)`.

Lo schema `A → E → [c=E(m)] → D → B` è il modello di riferimento di tutto il modulo. `A` è il mittente, `B` il destinatario, e sul canale in mezzo viaggia solo `c`.

---

## 4. I principi di Kerckhoffs — perché il segreto è la chiave, non l'algoritmo

Un **algoritmo segreto** sembra un'idea vincente: se l'attaccante non sa nemmeno *come* cifri, come fa a decifrare? Beneficio apparente: la difficoltà di studiare come invertire una cifratura sconosciuta. Ma i **problemi** sono strutturali e fatali:
- **mancanza di revisione della qualità** (nessuno può dirti se il tuo algoritmo è robusto se non lo mostri a nessuno — e la storia è piena di algoritmi segreti crollati appena rivelati);
- **difficoltà di diffusione** delle procedure;
- **difficoltà di sostituzione** delle procedure (se l'algoritmo viene scoperto, devi cambiarlo dappertutto, ed è enormemente più difficile che cambiare una chiave).

Nel 1883 **Kerckhoffs** formalizza i principi che reggono ancora oggi. I due che devi sapere:
1. Il sistema deve essere **materialmente, se non matematicamente, indecifrabile**. Questa è la distinzione tra **sicurezza computazionale** (in teoria craccabile, ma richiederebbe più tempo/risorse di quante ne esistano nell'universo pratico) e **sicurezza assoluta** (matematicamente impossibile da craccare, indipendentemente dalle risorse).
2. Il sistema **non deve richiedere segretezza** e deve poter cadere in mano al nemico senza inconvenienti. Ecco lo slogan del modulo: **~~segreto = algoritmo~~ → segreto = chiave!** L'algoritmo si assume pubblico e noto a tutti (incluso l'attaccante); l'unica cosa segreta è la chiave.

**Visione**: cifrare significa "ricordare un segreto semplice (la chiave) per poter scambiare molti segreti arbitrari (i messaggi)". La chiave è piccola, sostituibile, comunicabile a voce; l'algoritmo è grande, pubblico, studiato da tutti proprio perché resti robusto.

---

## 5. La crittoanalisi — cosa può fare l'attaccante

La **crittoanalisi** è la disciplina di chi attacca. A seconda del materiale a disposizione, il crittanalista ha diverse "opportunità di attacco". Questi sono i **modelli di attacco** che l'esame può chiederti di riconoscere:

| Attacco | Cosa ha a disposizione l'attaccante |
|---|---|
| **Forza bruta** | Prova a indovinare la chiave `D` (o il suo segreto), decifra, e se il risultato non ha senso ripete. Nessuna informazione esterna, solo tentativi. |
| **Solo testo cifrato** (ciphertext-only) | Ha molto materiale cifrato: fa analisi statistiche e ne deduce quale `p` corrisponde probabilmente a un dato `c`. |
| **Testo in chiaro noto** (known-plaintext) | Ha coppie (testo in chiaro, testo cifrato) e cerca di dedurre `D` analizzandole. |
| **Testo scelto** (chosen-plaintext) | Può *scegliere* lui il testo da cifrare (o da far decifrare) per ottimizzare la deduzione della chiave. |
| **Rubber hose** | Minaccia, ricatta o tortura qualcuno finché non cede la chiave. (Il promemoria che nessuna matematica protegge da una chiave sotto costrizione.) |

**La domanda-chiave** (compare spesso all'esame): *di fronte a un testo cifrato con algoritmo noto, cosa può SEMPRE fare un crittanalista?* Due cose, sempre disponibili:
1. **Analizzare le proprietà statistiche** del testo. Da qui la definizione di **robustezza** = capacità dell'algoritmo di **occultare le proprietà del testo in chiaro**.
2. **Cercare la chiave tra tutte quelle possibili** (forza bruta). Da qui le due sicurezze:
   - **sicurezza assoluta** = rendere *totalmente indistinguibile la chiave giusta* dalle altre (nessuna analisi la fa emergere);
   - **sicurezza computazionale** = rendere *troppo oneroso il processo di ricerca* della chiave (in teoria la trovi, in pratica no).

---

## 6. I "mattoni" della robustezza: confusione e diffusione

Ogni cifrario robusto si costruisce con due proprietà elementari, ripetute e combinate:

- **Confusione**: misura il grado in cui la **struttura della chiave** viene resa irriconoscibile nel testo cifrato. Idealmente, modificare *un solo elemento della chiave* dovrebbe riflettersi sul **50% del testo cifrato**; e l'analisi del cifrato non deve dare indicazioni utili sul valore della chiave. **La sostituzione è il modo più semplice di introdurre confusione.**

- **Diffusione**: misura il grado in cui le **proprietà statistiche del testo in chiaro** vengono sparse sul testo cifrato. Idealmente, modificare *un solo elemento del testo in chiaro* dovrebbe alterare il **50% del testo cifrato**; e l'analisi del cifrato non deve dare indicazioni utili sul testo in chiaro. **La trasposizione è il modo più semplice di introdurre diffusione.**

Memorizza l'accoppiamento: **confusione ↔ sostituzione ↔ nasconde la chiave**; **diffusione ↔ trasposizione ↔ nasconde il testo**. È esattamente il tipo di associazione che un quiz a scelta multipla mescola apposta.

---

## 7. Cifrari classici — e perché cadono tutti

### 7.1 Sostituzione monoalfabetica
Ogni lettera è sostituita sempre con la stessa lettera cifrata (una tabella fissa `A→Q, B→W, ...`). Esempi storici: cifrario di Cesare, Agony Columns del Times, parole crociate della Settimana Enigmistica. Lo spazio delle chiavi è enorme: `26! ≈ 4·10²⁶ ≈ 2⁸⁸` permutazioni.

> Attenzione al trabocchetto: **uno spazio delle chiavi enorme NON garantisce robustezza.** 2⁸⁸ chiavi sono troppe per la forza bruta, eppure la monoalfabetica cade banalmente.

**Attacco alla sostituzione** (ciphertext-only, statistico): nel linguaggio naturale le frequenze delle lettere sono molto sbilanciate (in inglese `e` ~12,7%, poi `t, a, o, i, n...`). Poiché la sostituzione è fissa, la lettera cifrata più frequente corrisponde quasi certamente alla `e`, e così via: si ricostruisce la tabella senza provare nessuna chiave. La monoalfabetica ha confusione ma **zero diffusione** — le frequenze del chiaro passano intatte nel cifrato.
> Nota "mondo binario": se la "lettera" è un lungo blocco di bit, le frequenze diventano basse e uniformi (come dopo compressione) → l'attacco statistico perde efficacia. È l'idea che porterà ai cifrari a blocchi (§8).

### 7.2 Trasposizione
Non cambia le lettere, ne cambia l'**ordine**. La **scitala degli Spartani** (bastone di un dato diametro attorno a cui si avvolge una striscia) è l'esempio storico. Algoritmicamente: scrivi il testo in una tabella per colonne e lo leggi per righe. La chiave è la **dimensione della tabella** + l'**ordine di lettura delle righe**. **Attacco**: statistiche di **digrammi** (`TH`, `IN`, `ER`...) e **trigrammi** (`THE`, `ING`...) permettono di dedurre la dimensione della tabella. Ha diffusione ma zero confusione (le lettere sono le stesse, solo spostate).

### 7.3 Sostituzione polialfabetica
L'idea di Leon Battista Alberti (1466) e la forma semplificata **Bellaso/Vigenère** (1553, usata per 4 secoli, fino alla macchina **Enigma** della WWII): si usa una **chiave che scorre** e cambia la sostituzione a ogni carattere. Esempio: `A=0, B=1, ... Z=25`, si somma modulo 26 la chiave (ripetuta ciclicamente) al testo. Effetto: le frequenze di un carattere in chiaro vengono **sparse** su più caratteri cifrati (introduce diffusione oltre alla confusione) → l'analisi delle frequenze semplice non basta più.

Ma è **attaccabile grazie al ripetersi periodico** delle sostituzioni. Due strumenti crittanalitici:
- **Test di Kasiski**: la chiave si ripete, quindi frammenti uguali del chiaro (poligrammi) distanti un multiplo della lunghezza della chiave producono lo *stesso* cifrato. Cerchi sequenze identiche nel cifrato, annoti le distanze, le fattorizzi: la **lunghezza della chiave = MCD** delle distanze con fattore comune. Trovata la lunghezza `L`, spezzi il cifrato in `L` sotto-testi ognuno cifrato con una monoalfabetica → attacco per frequenze su ciascuno.
- **Indice di coincidenza (IC)**: la probabilità che due lettere prese a caso nel testo siano uguali. Serve a misurare le variazioni di frequenza. Alta variazione (IC alto, ~0,066 per l'italiano/inglese) = poca "spargimento" = sostituzione semplice/lingua riconoscibile; distribuzione perfettamente casuale = IC minimo (~0,038). Confrontando l'IC del cifrato con questi riferimenti si stima la lunghezza della chiave.

### 7.4 One-time pad (OTP) — l'unico con sicurezza assoluta
Vernam/Mauborgne (1917): polialfabetica con una chiave che sia **(1) scelta perfettamente a caso, (2) lunga quanto il messaggio, (3) mai riutilizzata**. Rispettate queste tre condizioni, ottieni **sicurezza perfetta** (assoluta, non computazionale).

**Perché è perfetto — il meccanismo**: dato il cifrato `WPE`, *tutte* le chiavi possibili sono equiprobabili, e ognuna porta a un testo in chiaro diverso e sensato (`WPE` potrebbe venire da `SUL`, `TRA`, `FRA`, `RIO`...). L'attaccante non ha modo di distinguere quale sia il messaggio vero: ogni ipotesi valida della lingua è ugualmente plausibile → la chiave giusta è **indistinguibile**. **Visione**: OTP realizza alla lettera la definizione di sicurezza assoluta del §5 (chiave giusta indistinguibile dalle altre). **Il difetto pratico** ("Ma che fatica!"): una chiave lunga quanto il messaggio, casuale e usa-e-getta, è ingestibile — se puoi scambiare in sicurezza una chiave così lunga, tanto valeva scambiare il messaggio. Da qui la necessità dei cifrari moderni, che rinunciano alla sicurezza *assoluta* per quella *computazionale*, in cambio di chiavi corte e riutilizzabili.

---

## 8. Dai classici ai moderni — cifrari a blocchi

I cifrari moderni partono da due osservazioni sui classici:
- **Sull'input**: conviene ridurre a priori la riconoscibilità statistica dei simboli. Come? Aumentando il numero di simboli (frequenza media = 1/N più bassa e uniforme) — facile se prendo come "lettera" un **blocco di bit** (8, 16, 32, 64...) invece di un carattere; e rendendoli equiprobabili (compressione).
- **Sull'algoritmo**: ogni operazione di sostituzione e trasposizione aumenta confusione e diffusione. Quindi: **le combino tante volte.**

### 8.1 Cifrari composti e round
Un **round** applica una sostituzione (**S-box**: una tabella che rimappa i bit — confusione) seguita da una trasposizione (**P-box**: una permutazione che sparge i bit — diffusione). **Tanti round incrementano l'effetto**: dopo abbastanza round, un singolo bit del chiaro o della chiave ha influenzato metà del cifrato. Questo è il principio "a mattoni" del §6 portato su scala industriale.

### 8.2 Cifrari di Feistel e DES
La parte difficile è implementare `E` e `D` "modularmente" per poter lavorare liberamente sul numero di round. La **struttura di Feistel** risolve questo: divide il blocco in due metà e le processa in modo che **la decifrazione riusi lo stesso schema della cifratura al contrario** (con le sottochiavi in ordine inverso) — non serve invertire la funzione interna `F`, che può quindi essere arbitrariamente complessa.

**DES** (Data Encryption Standard): standard storico, National Bureau of Standards USA + IBM, pubblicato nel **1977**. Struttura di Feistel a **16 round**, **blocchi di 64 bit, chiave di 56 bit**.
> Il numero da ricordare per l'esame: DES = **56 bit di chiave** — oggi troppo pochi, forzabile a forza bruta, per questo è stato soppiantato.

### 8.3 AES
**AES** (Advanced Encryption Standard), standard attuale, **FIPS 197**, algoritmo **Rijndael**. Punti che l'esame chiede in forma vero/falso:
- **NON usa la struttura di Feistel**, ma l'**aritmetica dei campi finiti** (campi di Galois);
- **blocchi di 128 bit**;
- chiavi di lunghezza a scelta: **128, 192 o 256 bit**.

DES e AES sono entrambi **cifrari simmetrici (a singola chiave)**: la stessa chiave cifra e decifra.

---

## 9. Modi di operazione — come si cifrano messaggi più lunghi di un blocco

Un cifrario a blocchi cifra un blocco alla volta. Ma "cifrare blocco per blocco in modo indipendente è male":
- stesso plaintext → stesso ciphertext (analisi facilitata: si vedono i pattern, l'esempio classico è l'immagine cifrata in ECB in cui si intravede ancora la figura);
- modifica a un blocco → gli altri blocchi restano inalterati (integrità non protetta).

Questo modo ingenuo si chiama **ECB (Electronic Codebook)** ed è da evitare. Le soluzioni **concatenano** i blocchi in modo che ognuno dipenda dal precedente:
- **CBC (Cipher Block Chaining)**: ogni blocco in chiaro viene messo in XOR con il **blocco cifrato precedente** prima della cifratura; il primo usa un **IV (Initialization Vector)**. Stesso plaintext → ciphertext diverso.
- **CFB (Cipher Feedback)** e **OFB (Output Feedback)**: varianti con feedback del blocco cifrato/dell'output.
- **CTR (Counter)**: realizza l'equivalente a blocchi di un **cifrario a flusso** — cifra un contatore che avanza (nonce + counter) e mette in XOR il risultato col plaintext. I blocchi sono indipendenti tra loro ma ognuno usa un input diverso, quindi niente pattern.

**Visione**: il modo di operazione è ciò che trasforma un cifrario a blocchi "puro" in qualcosa di sicuro nella pratica. La domanda tipica: *"ECB è sicuro?"* → No, rivela i pattern.

---

## 10. Cifrari a flusso

Un **cifrario a flusso** è concettualmente un One-Time Pad con alfabeto binario (solo 0 e 1) → l'analisi statistica delle frequenze diventa inapplicabile. Il problema dell'OTP era la chiave lunga e casuale: qui si risolve generando un **flusso di chiave** (keystream) con un **generatore pseudocasuale** (PRNG) il cui **seme è la chiave condivisa**. Il plaintext viene messo in **XOR** col keystream byte per byte.

**Differenza rispetto all'OTP vero**: il keystream è *pseudo*-casuale (deterministico dato il seme), non veramente casuale → si scende dalla sicurezza assoluta a quella computazionale. Ma in cambio mittente e destinatario devono condividere solo la chiave-seme corta, non l'intero pad. È ancora un cifrario **simmetrico**.

---

## 11. Funzioni hash — il grande spartiacque: NON è cifratura

Questo è il concetto che Lorenzo deve inchiodare, perché è la confusione più comune del modulo. Gli stessi principi dei cifrari a blocchi possono essere usati **senza chiave** per ottenere "impronte digitali" (**fingerprint**) compatte di documenti di dimensione arbitraria.

Proprietà di una funzione hash:
- produce un output di **dimensione fissa** (es. 256 bit) qualunque sia la dimensione dell'input → **NON è biunivoca** (infiniti input, output finiti);
- è **pubblica e senza chiave** (chiunque può calcolarla, non c'è nulla di segreto);
- è **irreversibile per costruzione**.

**Differenza fondamentale hash vs cifratura** (tienila sempre in mente):

| | Cifratura | Hash |
|---|---|---|
| Chiave | Sì (simmetrica o asimmetrica) | **No** |
| Reversibile | **Sì** — `D(E(m)) = m`, si torna al messaggio | **No** — non esiste `D`, non si torna indietro |
| Dimensione output | ~quella dell'input | **Fissa**, indipendente dall'input |
| Scopo | Riservatezza (nascondere il contenuto) | Integrità/autenticità (rilevare modifiche) |

> Se una domanda dice "l'hash SHA-256 cifra il documento" → **Falso**. L'hash non cifra: non c'è chiave e non è invertibile. Cifrare e fare l'hash sono operazioni con scopi opposti (nascondere-e-recuperare vs impronta-irreversibile).

Una funzione hash si dice **crittografica (robusta)** se soddisfa due proprietà:
1. **Unidirezionalità (one-way)**: dato un fingerprint, non si può trovare un documento che lo produca. (È la stessa proprietà "hash facile in un senso, impossibile all'indietro" già vista in **S2 con S-KEY**, dove il ratchet di hash andava solo in avanti.)
2. **Assenza di collisioni (collision-free)**: non si può trovare una *coppia* di documenti diversi con lo stesso fingerprint.

### 11.1 Utilità e limite: il problema dell'uomo nel mezzo
L'hash usato come **checksum** protegge bene contro **alterazioni accidentali**: Alice manda `data + H(data)`, Bob ricalcola l'hash e confronta. Ma contro un attaccante **attivo** (Man-in-the-Middle) non basta: Darth intercetta, modifica `data → data'`, ricalcola `H(data')` e inoltra entrambi. Bob verifica e trova tutto coerente. **L'hash da solo dà integrità contro il rumore, non contro un avversario**, perché manca un "elemento univoco dell'autore" (autenticazione). Serve o un canale sicuro per l'hash, o legare l'hash all'identità di chi lo produce → è quello che risolveranno le **firme digitali** (§14).

### 11.2 Attacchi alla proprietà one-way
- **Ricerca di difetti nell'algoritmo**: improbabile per un hash ben progettato.
- **Forza bruta**: generare documenti a caso finché uno ha la fingerprint cercata. Tempo **esponenziale con la lunghezza dell'impronta** (per `m` bit, ~2^m tentativi).

Famiglie di hash più diffuse (da riconoscere): **MD5** (128 bit), MD6 (fino a 512), **RIPEMD** (128/160/320), **SHA** (160/224/256/384/512) / **SHA-3** (lunghezza arbitraria).

### 11.3 Attacchi alla proprietà collision-free — il birthday attack
- **Difetti nell'algoritmo**: **trovati!** Collisioni pratiche per **SHA-1 (2005)** e **MD5 (2008)** → questi due sono considerati rotti per l'uso crittografico.
- **Birthday attack (paradosso del compleanno)**: trovare *una qualsiasi* coppia con lo stesso hash è molto più facile che trovare la preimmagine di un hash *fissato*. Analogia: in un gruppo servono ~253 persone per avere >50% di probabilità che qualcuno compia gli anni in *una data specifica*, ma bastano **~23 persone** perché *due qualsiasi* di loro condividano un compleanno, perché conta il numero di *coppie* (`M·(M-1)/2`), che cresce col quadrato. **Conseguenza cruciale**: per un hash di `m` bit, lo spazio è `2^m`, ma per trovare una collisione bastano **~2^(m/2)** tentativi, non `2^m`.
> Numero da ricordare: **collisione ≈ 2^(m/2), preimmagine ≈ 2^m.** È il motivo per cui un hash a 128 bit dà solo ~64 bit di resistenza alle collisioni.

### 11.4 Length extension attack
Noto `H(m₁)` e la lunghezza di `m₁`, ma **senza conoscere `m₁`**, un attaccante che sceglie `m₂` riesce a calcolare `H(m₁ || m₂)`. **Vulnerabili**: MD5, SHA-1, RIPEMD-160, SHA-256, SHA-512. **Resistenti**: SHA-3 e le varianti troncate di SHA-2.

---

## 12. Problemi difficili e trapdoor — la base della crittografia asimmetrica

Per arrivare agli algoritmi a doppia chiave serve un ingrediente matematico: le **funzioni pseudo-unidirezionali** (trapdoor). Sono operazioni **facili in un verso e computazionalmente infattibili nell'altro — a meno di conoscere un segreto** (la "trapdoor", la botola). Due sorgenti di difficoltà usate in pratica:
- **fattorizzazione di grandi numeri** (facile moltiplicare due primi, difficilissimo risalire ai fattori dal prodotto);
- **operazioni in aritmetica modulare**: si prende come risultato il **resto della divisione per un modulo fisso**.

**Intuizione visiva** (dalle slide): la funzione `y = x¹³` sui reali è "regolare", monotona → se non conosci l'inversa la approssimi per bisezione. Ma `y = x¹³ mod 77` sul campo di Galois `Z₇₇` diventa **estremamente irregolare**: la riduzione modulare "frantuma" l'ordine → non c'è modo di fare una ricerca efficiente dell'inversa. Questo salto dalla regolarità (invertibile) all'irregolarità (non invertibile senza segreto) è il cuore della crittografia a chiave pubblica.

---

## 13. RSA — il cifrario asimmetrico per eccellenza

**RSA** (1977) usa esattamente la difficoltà della fattorizzazione + aritmetica modulare.

**Generazione delle chiavi**:
1. si scelgono due numeri primi `p` e `q`;
2. il modulo è `n = p·q`;
3. si sceglie a caso un numero `d` e si calcola `e` tale che `e·d mod (p-1)(q-1) = 1`. *Questo calcolo è facile solo conoscendo `p` e `q` — che poi vengono dimenticati.*

Risultato: **chiave pubblica `(e, n)`**, **chiave privata `(d, n)`**.
- **Cifratura**: `c = mᵉ mod n`
- **Decifrazione**: `m = cᵈ mod n`

**Il meccanismo dell'asimmetria**: chiunque conosca la chiave pubblica `(e, n)` può cifrare, ma per decifrare serve `d`, e ricavare `d` da `(e, n)` richiederebbe di fattorizzare `n` per ritrovare `p` e `q` — computazionalmente infattibile per `n` grande. La chiave pubblica e quella privata sono **matematicamente legate ma non l'una derivabile dall'altra**.

**Robustezza**:
- Non ci sono modi efficienti noti di invertire l'esponenziale modulare (complessità assimilabile alla forza bruta).
- Ci sono algoritmi "quasi efficienti" per fattorizzare il modulo (**General Number Field Sieve**, sub-esponenziale) → **contromisura: moduli grandi, oltre 2048 bit**.
- **Trappole (rischi pratici)**: non è *dimostrato* che non esistano algoritmi classici efficienti (nessuno li ha trovati); il **quantum computing** (§16); e implementazioni troppo ingenue (se si sceglie `e` piccolo con pochi "1" — es. 3, 17, 65537 — e `mᵉ` non "trabocca" da `n`, la cifratura è attaccabile).

RSA è un **cifrario asimmetrico (a doppia chiave)**. Visto da dentro è "un cifrario a blocchi, di sostituzione, con dimensioni enormi": niente forza bruta, niente analisi statistica dell'alfabeto (`c = mᵉ mod n` visualizzato è una nuvola di punti senza struttura).

---

## 14. Le tre applicazioni della crittografia asimmetrica

La stessa coppia di chiavi serve a scopi diversi a seconda di *quale* chiave si usa per *quale* operazione. Questo è il punto più elegante e più chiesto all'esame.

### 14.1 Riservatezza
`A` cifra con la **chiave pubblica di B** (`PUB_B`); solo `B`, con la **sua privata** (`PRIV_B`), può decifrare. **Vantaggio enorme**: la chiave pubblica **può essere distribuita** liberamente, chiunque la usa per cifrare, ma **solo il possessore della privata decifra** → risolve il problema della distribuzione delle chiavi che affligge la crittografia simmetrica (dove la stessa chiave segreta deve raggiungere entrambi).

### 14.2 Integrità e autenticità — la firma digitale
Si **inverte l'uso delle chiavi**. `A` calcola l'**hash del documento** e lo **cifra con la propria chiave privata** (`PRIV_A`): questa è la **firma**. `B` decifra la firma con la **chiave pubblica di A** (`PUB_A`), ricalcola l'hash del documento ricevuto, e confronta:
- se coincidono → il documento è **inalterato** (integrità);
- e poiché solo `A` possiede `PRIV_A`, la firma poteva produrla solo `A` → **autenticità** (a patto di potersi fidare che `PUB_A` sia davvero di `A` — problema che la PKI/i certificati risolvono, terreno di S13).

> Questa è la soluzione al problema dell'uomo nel mezzo del §11.1: l'hash da solo non bastava perché mancava l'elemento univoco dell'autore; cifrare l'hash con la privata *è* quell'elemento univoco. **Firma digitale = hash + cifratura asimmetrica con la chiave privata.**

### 14.3 Pregi, difetti e cifrari ibridi
- **Grandi vantaggi**: distribuzione delle chiavi; utilità per *tutte* le proprietà di sicurezza (riservatezza, integrità, autenticità).
- **Punti deboli**: **prestazioni** (5–10 volte più lenta di AES); alcuni attacchi specifici (known-plaintext).
- **Soluzione — cifrari ibridi**: si combinano i due mondi. Si cifra il **messaggio** con un cifrario **simmetrico** veloce (AES) usando una chiave di sessione `K` casuale; si cifra la sola **chiave `K`** con la crittografia **asimmetrica** (`PUB_B`). Così si ha la velocità del simmetrico e la comodità di distribuzione dell'asimmetrico. Bonus: per più destinatari basta un solo messaggio cifrato + una copia di `K` cifrata con la chiave pubblica di ognuno. **È esattamente il modello di TLS (S13) e di gpg (S15).**

---

## 15. Rainbow tables — attaccare gli hash con la precomputazione

Ora il pezzo dedicato dell'approfondimento, e il cuore del threat model del modulo. Attaccare la proprietà one-way per forza bruta (§11.2) significa ricalcolare hash finché non si trova quello giusto: costoso *al momento dell'attacco*. L'idea della **precomputazione** è spostare il costo *prima*.

### 15.1 Precomputare gli hash — lo space-time tradeoff
Principio: **risparmio tempo nel cracking (precalcolando gli hash), pago il costo di memorizzarli**. Il modo "ingenuo e brutto":
```
cat wordlist.txt | (while read WORD; do echo $WORD | md5sum | cut -c 1-32; done) > precomputed.txt
```
Si prende una wordlist, si calcola l'hash di ogni parola, si salva la tabella `(hash → parola)`. Poi, per craccare un hash, basta cercarlo nel file — nessun calcolo al momento dell'attacco. **Problemi**: lento da generare (usa la CPU una volta per tutte) e **file enorme** — MD5 produce fingerprint di 32 caratteri, quindi la dimensione finale è `32 × (n° di parole)` byte. Per coprire tutte le password fino a 8 caratteri il file diventa ingestibile.

### 15.2 Rainbow tables — precomputazione compressa
Le **rainbow tables** sono più sofisticate: **richiedono molto meno spazio** a parità di copertura. Usano due funzioni:
- una **funzione hash** `H` (quella che si vuole attaccare, es. MD5);
- una **funzione di riduzione** `R`: un algoritmo generico che mappa dallo spazio dei valori-hash allo spazio delle preimmagini (prende un hash e lo trasforma in una password). **Attenzione**: `R` **non inverte** l'hash — non restituisce la password originale (impossibile!) — produce semplicemente una password *nuova, diversa*, giusto per continuare la catena.

**Generazione (le "catene")**: si parte da un plaintext e si applica in catena, alternandoli, `H` e più funzioni di riduzione `R₁, R₂, R₃...` (ogni `Rᵢ` è un "colore" diverso del rainbow — da qui il nome):
```
aaaaa --H--> hash1 --R1--> brsoh --H--> hash2 --R2--> ormsp --H--> ... --R4--> sldep
```
Si generano **tantissime catene** lunghe, ma **si salvano solo il plaintext iniziale e quello finale** di ogni catena (`aaaaa | sldep`). Qui sta la compressione: una catena di migliaia di passi occupa in tabella solo due valori (TOP e BOTTOM).

**Lookup (craccare un hash `h`)**: dato l'hash da craccare, si applica **iterativamente la catena di funzioni partendo dall'ultima riduzione**, generando plaintext candidati, e si controlla se qualcuno coincide con un **BOTTOM** (plaintext finale) salvato in tabella.
- se nessun candidato coincide con un finale noto → si allunga il tentativo (si prova un pezzo più lungo di catena);
- quando un candidato **coincide col fondo di una catena salvata**, si prende il **plaintext in cima** (TOP) di quella catena e si **riapplica tutta la catena da capo** fino a incontrare l'hash `h` cercato → il plaintext *immediatamente prima* di `h` nella catena è la password.

**Visione**: la rainbow table baratta spazio con tempo in modo intelligente. La precomputazione ingenua salva *tutti* gli hash (velocissima ma gigantesca); la rainbow salva solo gli estremi delle catene e ricalcola il pezzo di catena necessario al momento del lookup (un po' più lenta del lookup diretto, ma incomparabilmente più piccola). Non è una tabella `hash → password`, è una tabella di *catene compresse* che vanno ripercorse.

### 15.3 In pratica e considerazioni
Tool: **`rainbowcrack`**.
```
sudo rtgen md5 loweralpha 1 7 0 1000 100000 0     # genera le catene (algoritmo, charset, lunghezze, parametri)
sudo rtsort /usr/share/rainbowcrack                # ordina la tabella
rcrack /usr/share/rainbowcrack -h <hash>           # cracca un hash dato
```
**Considerazioni**:
- attacchi "vecchio stile", popolari negli anni 2000, soprattutto per craccare password **Windows**;
- **solo certi algoritmi** sono supportati (MD5, SHA1, NTLM...);
- **possono fallire**: la tabella deve essere sufficientemente grande (più catene, catene più lunghe) per coprire lo spazio;
- la generazione richiede tempo, ma le tabelle **si condividono/vendono** comodamente (esistono tabelle NTLM/MD5/SHA1 da centinaia di GB in commercio).

---

## 16. Threat model del modulo — attaccante vs difensore

Questa è la sezione da studiare a memoria: il quiz teorico ama le domande "quale contromisura protegge da quale attacco".

### 16.1 Le TRE tecniche d'attacco alle password — disambiguazione precisa
Sono simili (tutte cercano una password che produca un dato hash) ma **profondamente diverse** su *dove* e *quando* spendono il lavoro. È la confusione più a rischio del modulo, quindi tabella netta:

| | **Dictionary attack** | **Brute force** | **Rainbow table** |
|---|---|---|---|
| **Spazio esplorato** | Una **lista di candidati probabili** (wordlist: parole comuni, password trapelate, varianti) | **Tutte** le combinazioni possibili del charset, esaustivamente | Uno spazio precompilato in **catene** (di solito un charset+lunghezza definiti) |
| **Quando si calcolano gli hash** | **Al momento dell'attacco**, uno per candidato | **Al momento dell'attacco**, uno per combinazione | **Prima** (precomputazione offline, una volta per tutte) |
| **Costo dominante** | CPU al momento dell'attacco, ma su pochi candidati "furbi" | CPU al momento dell'attacco, enorme (cresce esponenzialmente con lunghezza/charset) | **Spazio** su disco (tempo di attacco ridotto a lookup + ricostruzione catena) |
| **Punto di forza** | Velocissimo se la password è "umana"/comune | Trova *qualsiasi* password, prima o poi | Riusa lo stesso sforzo per craccare molti hash diversi |
| **Punto di debolezza** | Fallisce su password veramente casuali (non in lista) | Impraticabile per password lunghe ad alta entropia | Occupa molto spazio; **annullata dal salt**; solo alcuni algoritmi |

In una frase: **brute force** prova tutto e non precalcola nulla; **dictionary** prova solo i candidati probabili e non precalcola nulla; **rainbow table** precalcola (in forma compressa) e al momento dell'attacco fa solo lookup. Dictionary e brute force spostano il costo *al momento dell'attacco*; la rainbow lo sposta *prima*, pagandolo in spazio.

### 16.2 Le contromisure del difensore
- **Salt** (visto in **S2**): una variazione casuale concatenata alla password *prima* dell'hash (`hash(password || salt)`). **Rende inutili le rainbow tables e le precomputazioni**: la tabella dovrebbe essere ricalcolata per *ogni possibile salt*, cosa che distrugge il vantaggio della precomputazione. Rende anche unici gli hash di due utenti con la stessa password. **Ma attenzione** (già chiarito in S2): il salt **non protegge contro dictionary/brute force offline** su un hash rubato — l'attaccante conosce il salt (è nello `/etc/shadow`) e lo include nei suoi calcoli; semplicemente non può più *precalcolare*.
- **Password ad alta entropia** (S2): l'unica difesa contro dictionary e brute force offline. Una password veramente casuale e lunga esce dalla wordlist (batte il dictionary) e rende il brute force computazionalmente infattibile.
- **Scelta di algoritmi/parametri robusti**: usare hash non rotti (evitare MD5/SHA-1 per firme, §11.3); usare cifrari con chiavi adeguate (AES-256 non DES-56); moduli RSA ≥ 2048 bit (§13); modi di operazione sicuri (CBC/CTR, non ECB, §9); per lo storage di password, funzioni deliberatamente *lente* (non è nelle slide di S14, ma è il corollario pratico del "rendere oneroso l'attacco").
- **Pepper** (S2): segreto extra tenuto in un HSM, fuori dal database — anche rubando lo `/etc/shadow` l'attaccante non ha il pepper.

---

## 17. Un flash su Quantum Computing

Domanda tipica: *"il quantum computing rompe tutta la crittografia?"* → **No, in modo selettivo:**
- **Crittografia simmetrica e hash: nessun vero problema.** L'**algoritmo di Grover** dà una complessità ≈ `sqrt(dimensione dello spazio di ricerca)`, cioè dimezza i bit di sicurezza effettivi. Si **compensa raddoppiando** la lunghezza di chiavi e fingerprint (AES-256 resta sicuro, si usa hash più lungo).
- **Crittografia asimmetrica (RSA e affini basati su fattorizzazione/logaritmi discreti): spacciata.** L'**algoritmo di Shor** fattorizza in **tempo polinomiale** → RSA crolla. Servono ancora molti più qubit/gate di quanti oggi realizzabili (rischio sul lungo periodo), ma quando accadrà il crollo sarà **istantaneo**.
- **Post-quantum cryptography**: algoritmi resistenti al quantum già così avanzati da essere **in fase di standardizzazione**.

**Il punto da ricordare**: simmetrico/hash = raddoppia le chiavi e sei a posto; asimmetrico classico = a rischio esistenziale.

---

## 18. Domande di autoverifica — stile quiz teorico (40%)

> Rispondi *prima* di leggere le soluzioni negli appunti. Stile dell'esame reale: vero/falso e scelta multipla, penalità sulle sbagliate — quindi se non sei sicuro, ragiona sul meccanismo, non tirare a indovinare.

**Vero o Falso:**
1. La steganografia rende il messaggio illeggibile ma visibile sul canale.
2. Secondo i principi di Kerckhoffs, la sicurezza di un cifrario deve risiedere nella segretezza dell'algoritmo.
3. Un hash crittografico è una forma di cifratura reversibile senza chiave.
4. AES utilizza la struttura di Feistel.
5. DES usa una chiave di 56 bit.
6. Il salt impedisce gli attacchi con rainbow table.
7. Il salt protegge efficacemente contro un brute force offline su un hash rubato.
8. Per un hash di `m` bit, trovare una collisione richiede in media `2^m` tentativi.
9. Nel modo ECB, due blocchi di plaintext identici producono blocchi di ciphertext identici.
10. La funzione di riduzione di una rainbow table inverte l'hash restituendo la password originale.
11. RSA è un cifrario simmetrico.
12. L'algoritmo di Shor mette a rischio la crittografia simmetrica come AES.
13. Una firma digitale si ottiene cifrando l'hash del documento con la chiave privata del mittente.
14. L'One-Time Pad offre sicurezza computazionale, non assoluta.
15. Una funzione hash è biunivoca.

**Scelta multipla:**

16. Quale coppia associa correttamente proprietà e primitiva?
    a) confusione ↔ trasposizione; diffusione ↔ sostituzione
    b) confusione ↔ sostituzione; diffusione ↔ trasposizione
    c) confusione ↔ hash; diffusione ↔ salt
    d) confusione ↔ chiave pubblica; diffusione ↔ chiave privata

17. Un attaccante **precalcola offline** una struttura compatta di catene di hash e al momento dell'attacco fa solo lookup + ricostruzione. Di quale tecnica si tratta?
    a) brute force  b) dictionary attack  c) rainbow table  d) known-plaintext

18. Per la riservatezza con crittografia asimmetrica, `A` cifra un messaggio destinato a `B` usando:
    a) la chiave privata di A  b) la chiave pubblica di B  c) la chiave privata di B  d) la chiave pubblica di A

19. Quale hash ha collisioni pratiche dimostrate ed è quindi da evitare per le firme?
    a) SHA-3  b) SHA-256  c) MD5  d) le varianti troncate di SHA-2

20. In un cifrario ibrido (es. TLS), l'asimmetrico serve a:
    a) cifrare l'intero messaggio  b) cifrare la chiave di sessione simmetrica  c) calcolare l'hash  d) generare il salt

---

## 19. Connessioni con altri moduli

**Con S2 (Autenticazione)** — il legame più stretto:
- Lo `hash(password || salt)` in `/etc/shadow` è *questa* crittografia applicata: l'`$6$` è l'identificativo SHA-512, il **salt** è la contromisura del §16.2, la **fingerprint** è l'hash del §11.
- La **proprietà one-way** dell'hash che qui definiamo formalmente (§11) è quella che in S2 faceva funzionare **S-KEY** (il ratchet di hash che va solo avanti) e che rende irreversibile lo `/etc/shadow`.
- Il **challenge-response asimmetrico** di S2 (SSH con chiave pubblica: V cifra un nonce con `PUB_P`, solo `PRIV_P` lo decifra) è l'applicazione dell'asimmetrica del §14 alla dimostrazione d'identità.
- **Costruiamo sopra, non ripetiamo**: S2 diceva "il salt impedisce le rainbow tables" senza spiegare *cosa siano*; §15 spiega il meccanismo delle catene, e §16.1 chiude il cerchio disambiguando le tre tecniche d'attacco che S2 nominava di sfuggita (rainbow/brute force). Il concetto di **entropia** della password (S2) è la difesa contro dictionary/brute force qui formalizzati.

**Con S13 (Protezione delle comunicazioni, OpenSSL/TLS)**: i **cifrari ibridi** del §14.3 sono il modello di TLS — handshake asimmetrico per concordare la chiave di sessione, poi AES simmetrico per i dati. I **certificati/PKI** risolvono il "se posso fidarmi che `PUB_A` sia davvero di A" lasciato aperto dalla firma digitale (§14.2). I modi di operazione (§9) e AES (§8.3) sono le cipher suite che TLS negozia.

**Con S15 (LAB gpg + gestione chiavi)**: gpg è l'applicazione operativa di *tutto* questo modulo — genera coppie RSA (§13), cifra con schema ibrido (§14.3), firma calcolando hash + cifratura con la privata (§14.2), gestisce la fiducia sulle chiavi pubbliche. Fare S14 prima di S15 è ciò che rende i comandi gpg comprensibili invece che magici.

---

## 20. Riepilogo

- **Crittografia**: previene la violazione della riservatezza (cifratura), rileva quella dell'integrità/autenticità (hash, firme). Non è steganografia (che nasconde l'esistenza) né codici (che sostituiscono parole).
- **Kerckhoffs**: il segreto è la **chiave**, non l'algoritmo. Sicurezza **assoluta** (chiave indistinguibile, solo l'OTP) vs **computazionale** (troppo onerosa da attaccare, tutto il resto).
- **Simmetrico** (una chiave: DES-56, AES-128/192/256, cifrari a flusso) vs **asimmetrico** (due chiavi: RSA, `c=mᵉ mod n`). Ibrido = simmetrico per i dati + asimmetrico per la chiave.
- **Hash ≠ cifratura**: senza chiave, irreversibile, output fisso. Robusto se one-way + collision-free. Collisione ≈ `2^(m/2)` (birthday), preimmagine ≈ `2^m`. MD5 e SHA-1 rotti.
- **Firma digitale** = hash del documento cifrato con la **chiave privata** → integrità + autenticità.
- **Tre attacchi alle password**: **brute force** (prova tutto, calcola al volo), **dictionary** (prova candidati probabili, calcola al volo), **rainbow table** (precalcola catene compresse offline, poi solo lookup). Difese: **salt** (uccide le rainbow/precomputazioni), **entropia** (contro dictionary/brute force), algoritmi/parametri robusti, pepper.
- **Quantum**: simmetrico/hash si salvano raddoppiando le chiavi (Grover); asimmetrico classico è spacciato (Shor) → post-quantum crypto in standardizzazione.

<!-- AUTO-LINKS:START -->
<!-- AUTO-LINKS:END -->
