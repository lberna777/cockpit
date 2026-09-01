# Lezione — Modulo S15: GPG, proprietà e gestione delle chiavi

**Corso**: Lab Sicurezza Informatica T
**Materiale**: `Proprietà_e_gestione_delle_chiavi_15_maggio.pdf` (teoria, Prandini — "Chiavi crittografiche"), `LAB_gpg_13_maggio.pdf` (lab, Melis/Prandini), più due artefatti di lab: `Chiave_pubblica_Marco_Prandini.pdf` (in realtà un blocco `PGP PUBLIC KEY BLOCK`, chiave Ed25519 di Prandini) e `File_firmato.pdf` (in realtà un file `setup_ipt.sh` firmato con quella chiave).
**Prerequisiti**: **S14 (Crittografia — simmetrica/asimmetrica, hash, firma digitale, cifrari ibridi)**. Questa lezione *presuppone* S14 e non ne ripete i fondamenti: qui si dà per acquisito cosa sono una chiave pubblica/privata, cos'è un hash, e che *firma digitale = hash del documento cifrato con la chiave privata*. Se il verso firma/cifratura non è ancora solido, rileggere S14 §14 prima.

---

## Obiettivo

S14 ha spiegato *cos'è* una chiave e *come funziona* la matematica (RSA, DH, hash, firma). Questo modulo affronta il problema pratico che S14 lasciava aperto: **una chiave è un oggetto che nasce, va custodito, va distribuito e prima o poi muore — e ognuna di queste fasi ha i suoi attacchi**. È il "ciclo di vita delle chiavi".

Al termine Lorenzo deve saper rispondere da esame teorico a: perché generare una chiave asimmetrica è diverso dal generarne una simmetrica; cosa distingue un TRNG da un PRNG; perché una chiave di firma **non va salvata in backup** mentre una chiave di decifrazione **sì**; perché il problema delle chiavi pubbliche non è la riservatezza ma l'**autenticità**; la differenza tra **web of trust** e **PKI infrastrutturale**; e — parte pratica del lab — cosa fanno esattamente i comandi `gpg` per generare, importare/esportare, cifrare, firmare e verificare, e con *quale chiave* ognuno lavora.

> ⚠️ Questo modulo non aveva mai avuto lezione né appunti: si parte da zero. È l'ultimo tassello del blocco crittografico (S12→S13→S14→S15). L'esame teorico (40%, vero/falso e scelta multipla con penalità) chiede sia la teoria della gestione chiavi sia i **comandi/flag gpg** visti in laboratorio.

---

## 1. Il ciclo di vita delle chiavi — la mappa del modulo

Una chiave crittografica non è un dato statico: attraversa tre fasi, e la sicurezza complessiva è quella della fase più debole. Le tre fasi (che scandiscono anche questa lezione) sono:

1. **Generazione** — con la sua qualità fondamentale, la **robustezza** (§2).
2. **Memorizzazione** — dove custodirla, con requisiti contrastanti a seconda che sia una chiave di cifratura o di firma (§3).
3. **Distribuzione** — come farla arrivare a chi deve usarla, senza che un attaccante la sostituisca (§5).

A queste si aggancia il problema trasversale della **gestione** (quante chiavi, quali standard, §4) e la domanda che tiene insieme tutto: *come faccio a fidarmi che una chiave pubblica appartenga davvero a chi dice di appartenere?* → **certificazione** (§6).

**Visione**: S14 assumeva la chiave come un dato già presente e fidato. Nel mondo reale quell'assunzione è il punto più fragile. La crittografia "pura" quasi non si rompe più (S14: brute force e fattorizzazione sono infattibili con parametri adeguati); ciò che si rompe è la **gestione** — chiavi deboli perché generate male, rubate perché custodite male, o sostituite perché distribuite male.

---

## 2. Generazione delle chiavi

### 2.1 Simmetriche vs asimmetriche — due generazioni diverse

Il modo di generare una chiave dipende dal tipo:

- **Chiavi simmetriche** (e in generale nonce, vettori di inizializzazione, padding): **basta un buon generatore di numeri casuali**. Una chiave AES-256 è semplicemente 256 bit casuali — non deve avere nessuna struttura particolare, deve solo essere imprevedibile.
- **Chiavi asimmetriche**: servono **numeri primi** (S14: RSA parte da due primi `p` e `q`). Il procedimento è: si parte da numeri random, e si applica un **test di primalità** per verificare che siano primi. Generare una chiave RSA è quindi più costoso — non basta il caso, serve caso *filtrato* attraverso la primalità.

**Meccanismo**: in entrambi i casi il cuore è un generatore di numeri casuali; la differenza è che per l'asimmetrico quel numero casuale è solo il punto di partenza di una ricerca (il primo candidato-primo). **Visione**: è per questo che `gpg --gen-key` "ci mette un po'" e talvolta chiede di muovere il mouse o digitare — sta raccogliendo entropia per generare i primi.

### 2.2 Che cos'è la casualità — randomness vs unpredictability

La casualità è la materia prima di ogni chiave, e non è un concetto unico ma due proprietà distinte:

- **Randomness (casualità statistica)** — due sotto-requisiti:
  - **Uniform distribution**: la frequenza di 0 e 1 dev'essere approssimativamente uguale.
  - **Independence**: nessuna sottosequenza deve poter essere dedotta dalle altre.
- **Unpredictability (imprevedibilità)**: anche conoscendo i valori generati *finora*, non si deve poter prevedere il prossimo.

Una sequenza può essere statisticamente "casuale" (supera i test di distribuzione) ma **prevedibile** — ed è proprio la trappola dei generatori algoritmici. La distinzione tra i due tipi di generatore ruota attorno a questo:

- **TRUE random (TRNG)**: perfetta indipendenza → garantisce l'imprevedibilità. Ma è **difficile e inefficiente** da ottenere.
- **PSEUDO random (PRNG)**: è algoritmico → bisogna fare attenzione extra per rendere gli elementi difficili da prevedere conoscendo i precedenti.

### 2.3 TRNG — generatori veri, dalla fisica

Un **True Random Number Generator** attinge a **sorgenti fisiche di entropia**:
- elementi *ad hoc*: rumore termico, processi dinamici caotici (l'esempio celebre è **LavaRand** di Cloudflare, una parete di lampade di lava filmate);
- eventi "imprevedibili" nel calcolatore: es. gli intervalli di arrivo degli **interrupt** dai dispositivi.

Poi c'è una fase di **elaborazione**: conversione **A/D** (analogico→digitale) e **condizionamento** (rimozione del bias, perché una sorgente fisica raramente produce 0 e 1 perfettamente bilanciati).

**Visione**: il TRNG è l'unico modo di produrre imprevedibilità *vera*, perché la sua sorgente è un fenomeno fisico non deterministico. Il prezzo è che è lento e ingombrante.

### 2.4 PRNG — generatori algoritmici, veloci ma deterministici

Un **Pseudo Random Number Generator** è un **algoritmo** → per definizione **deterministico**. Se supera i test statistici è accettabile come PRNG, *ma sempre con attenzione all'imprevedibilità*. Il punto cruciale è il **seme (seed)**:
- tipicamente l'input è un seme prodotto da un TRNG;
- **noto il seme → nota tutta la sequenza generata!** (questa è la vulnerabilità strutturale: un PRNG con seme prevedibile o trapelato produce chiavi prevedibili);
- se l'algoritmo è robusto, conoscere una sequenza di valori intermedi non deve permettere di risalire al seme né di prevedere i valori futuri.

**Meccanismo**: TRNG (lento, imprevedibile) genera un seme corto → PRNG (veloce, deterministico) lo espande in tutta la casualità di cui si ha bisogno. **Visione**: è lo stesso pattern del cifrario a flusso di S14 (seme corto → keystream lungo): si baratta l'imprevedibilità assoluta con l'efficienza, e la sicurezza si concentra tutta nel proteggere il seme.

### 2.5 Test di casualità — NIST SP 800-22

Come si stabilisce se un generatore è buono? Con una batteria di test statistici. Lo standard di riferimento è **NIST SP 800-22**, che comprende **15 test**. I tre citati:
- **Frequency test**: il più basilare, deve essere in ogni suite — verifica che il numero di 1 e 0 sia circa quello atteso da una sequenza davvero casuale.
- **Runs test**: conta i "run" (sequenze ininterrotte di bit identici) e verifica che la loro numerosità/lunghezza sia quella attesa.
- **Maurer's universal statistical test**: verifica se la sequenza può essere significativamente **compressa senza perdita** — una sequenza comprimibile contiene ridondanza, quindi **non è casuale** (una sequenza davvero random è incomprimibile).

### 2.6 Robustezza (1): resistenza alla forza bruta

Generare bene la chiave serve a poco se la chiave è corta. La **robustezza** contro l'attacco più banale — provare tutte le chiavi — dipende dalla **lunghezza in bit**. La tabella delle slide (tempo per testare l'intero spazio DES/AES con tecnologie recenti):

| Budget | 56 bit | 128 bit | 256 bit |
|---|---|---|---|
| 1 K€ (individuo) | 16 anni | 10²² anni | 10⁶¹ anni |
| 1 M€ (impresa) | 6 giorni | 10¹⁹ anni | 10⁵⁸ anni |
| 1 G€ (NSA) | 8 minuti | 10¹⁶ anni | 10⁵⁵ anni |

Da leggere così: **56 bit (DES) sono forzabili** — 8 minuti per un budget statale; **128 bit e oltre no**, con margini astronomici. Ecco perché S14 insisteva: DES-56 è morto, AES-128/256 è sicuro.

**Il limite invalicabile — la termodinamica**: anche se la legge di Moore proseguisse all'infinito, c'è un muro fisico. Il **limite di Landauer**: cambiare 1 bit costa almeno `k·T·ln(2)` (≈ 3×10⁻²³ J a 3°K). Facendo i conti: tutta l'energia emessa dal Sole in un anno (1.2×10³⁴ J) basterebbe per ~4×10⁵⁶ bit flip = contare fino a 2¹⁸⁸; l'energia di una supernova (2×10⁴⁴ J) per ~7×10⁶⁶ bit flip = contare fino a 2²²². **Visione**: una chiave da 256 bit non è "molto difficile" da forzare a forza bruta — è **fisicamente impossibile**, non basta l'energia dell'universo. La sicurezza computazionale (S14) qui prende un significato letterale.

> Attenzione al trabocchetto delle slide: occhio alle "ricerche con tempo di calcolo gratis" (botnet/virus che rubano CPU, "lotteria cinese" = tanti computer che tentano in parallelo) e alla **sfortuna** (la forza bruta *in media* è metà spazio, ma con fortuna la chiave giusta è il primo tentativo). Il muro termodinamico resta comunque invalicabile per 256 bit.

### 2.7 Robustezza (2): resistenza alla fattorizzazione (asimmetrico)

Per gli asimmetrici il discorso cambia: **il miglior attacco a RSA NON è la forza bruta ma la ricerca dei fattori del modulo** (S14: fattorizzare `n` per ritrovare `p` e `q` → ricavare la privata). Quindi la robustezza di RSA non si misura come per una chiave simmetrica.
- Le stime sono difficili (riferimento: keylength.com); indicativamente **3000 bit robusti fino al 2026**.
- Stato dell'arte: nel **2020 Boudot et al. hanno fattorizzato RSA-250 (829 bit)** usando ~2700 anni-core di calcolo.

**Visione da esame**: una chiave RSA di 829 bit è già stata rotta; per questo (S14) i moduli RSA devono essere **≥ 2048 bit**, e il lab (§8) impone `>= 2048`. Non confondere: **256 bit sono tantissimi per una chiave simmetrica AES, ma pochissimi per un modulo RSA** — perché l'attacco è diverso (brute force vs fattorizzazione).

---

## 3. Memorizzazione — dove e come custodire la chiave

Custodire una chiave privata pone requisiti **contrastanti**, e la lezione centrale del modulo è che **dipende da cosa serve la chiave**.

### 3.1 La chiave di decifrazione — backup obbligatorio

Una chiave usata per **decifrare** ha due requisiti in tensione:
- **la perdita è devastante** → se la perdi, tutto ciò che era cifrato per te diventa illeggibile per sempre → serve un **backup**;
- **la segretezza è fondamentale** → non deve diffondersi → **non diffusione**.

Backup e non-diffusione tirano in direzioni opposte (ogni copia è un rischio in più, ma zero copie è un rischio di perdita). Gli **accorgimenti di memorizzazione** che bilanciano i due:
- **Cifratura con passphrase**: la chiave privata è salvata cifrata; per usarla serve la passphrase (è esattamente ciò che fa `gpg` quando chiede la passphrase, §8).
- **Hardware Security Module (HSM)**: un dispositivo dedicato che custodisce la chiave e la usa *senza mai esporla* — le operazioni crittografiche avvengono dentro l'HSM.
- **Key escrow**: la chiave (o una copia) è depositata presso una terza parte fidata, recuperabile in caso di necessità.
- **Secret sharing**: la chiave è spezzata in più parti distribuite a soggetti diversi, e ne serve un quorum per ricostruirla (nessun singolo detentore può usarla da solo).

### 3.2 La chiave di firma — NESSUN backup

Qui sta la distinzione più chiesta del modulo. Una chiave usata per **firmare** ha requisiti diversi:
- **se compromessa, si sostituisce**: nessuno ha bisogno di recuperarla in assenza del titolare → **nessun backup!** Se la perdi, semplicemente ne generi una nuova e comunichi che la vecchia non vale più (revoca). Il "valore" di una firma sta nel poterla produrre *d'ora in avanti*, non nel recuperare la chiave passata.
- **non deve essere usata contro la volontà del titolare** → protezione con **cifratura con passphrase** o **HSM**.

**Perché la differenza è profonda** (meccanismo): una chiave di *decifrazione* protegge dati che *esistono già* (il cifrato archiviato); perderla significa perdere l'accesso a quei dati → backup necessario. Una chiave di *firma* non custodisce nulla — serve solo a produrre firme future; perderla non distrugge le firme già emesse (quelle restano verificabili con la vecchia chiave pubblica), quindi basta rimpiazzarla → backup inutile e anzi dannoso (una copia in più della chiave di firma = una possibilità in più che qualcuno firmi a tuo nome).

> **Regola-esame da inchiodare**: chiave di **decifrazione** → **backup sì** (la perdita è irreversibile); chiave di **firma** → **backup no** (basta sostituirla). Sono simmetriche solo in apparenza; il *perché* le separa nettamente.

---

## 4. Gestione — il problema del numero e degli standard

Oltre a generarle e custodirle, le chiavi vanno *gestite* nel tempo. Parametri che complicano la gestione:

- **Numero delle chiavi in gioco** — la differenza è enorme tra i due modelli:
  - **sistemi asimmetrici**: **una chiave pubblica per ogni soggetto** → il numero cresce **linearmente** (N soggetti = N chiavi pubbliche).
  - **sistemi simmetrici**: **una chiave segreta per ogni coppia di soggetti** = **N(N-1)/2 chiavi** → cresce **quadraticamente**. Con 1000 utenti servono ~500.000 chiavi segrete condivise.

  **Visione**: questo è uno dei grandi vantaggi pratici dell'asimmetrico (già emerso in S14 come "risoluzione del problema della distribuzione"): non solo la chiave pubblica può viaggiare in chiaro, ma ne basta *una per persona* invece di una per ogni coppia. Il salto da O(N²) a O(N) è ciò che rende la crittografia a chiave pubblica scalabile a Internet.

- **Aderenza a standard e policy**: frequenza di sostituzione (rotazione periodica delle chiavi), compatibilità di formato tra sistemi diversi.
- **Standard di gestione**: **OASIS KMIP** (Key Management Interoperability Protocol) è lo standard che permette a prodotti diversi di gestire chiavi in modo interoperabile.

---

## 5. Distribuzione — far arrivare la chiave senza farla sostituire

### 5.1 Chiavi simmetriche — mai in chiaro

Una chiave simmetrica **non deve mai essere esposta in chiaro** (chi la vede, la usa). Modi per distribuirla:
- **scambio manuale** (di persona, canale fuori banda);
- **KDC (Key Distribution Center)**: ogni utente condivide *una* chiave con un centro fidato; per parlare con un altro utente, i due negoziano una chiave di sessione attraverso connessioni cifrate col KDC (è l'idea alla base di Kerberos);
- **scambio di Diffie-Hellman** (S14/S13): i due concordano una chiave condivisa su canale pubblico senza mai trasmetterla.

### 5.2 Chiavi asimmetriche — il vero problema è l'autenticità, non la riservatezza

Questo è il concetto-cardine della distribuzione, e ribalta l'intuizione. Una chiave pubblica **è pubblica**: un **attaccante passivo** (che si limita ad ascoltare) **non apprende nulla** vedendo una chiave pubblica o intercettando i parametri di un DH — non c'è riservatezza da proteggere. Il pericolo è l'**attaccante attivo**, che può **sostituire** i valori inviati da una parte all'altra con i propri. È il **Man-in-the-Middle** applicato alle chiavi pubbliche:

- **Attacco MITM su RSA**: l'attaccante ha una propria coppia (`PRIV_I`, `PUB_I`). Quando A e B cercano la chiave pubblica l'uno dell'altro, ricevono invece `PUB_I`. Conseguenze:
  - quando il mittente cifra un messaggio (credendo di usare la pubblica del destinatario, in realtà `PUB_I`), **l'attaccante può decifrarlo** con `PRIV_I`; poi lo ri-cifra con la vera pubblica del destinatario legittimo (magari alterato) per non insospettire nessuno;
  - l'attaccante può **firmare messaggi con `PRIV_I`**, e il destinatario, verificandoli con `PUB_I` (che crede del mittente legittimo), **si convince che siano autentici**.
- **Attacco MITM su Diffie-Hellman**: l'attaccante stabilisce **due chiavi separate**, una con A e una con B, e continua a fare da **"passacarte"** (decifra da un lato, ri-cifra dall'altro) senza che nessuno se ne accorga.

**La conclusione da memorizzare** (compare spesso all'esame): *per i sistemi asimmetrici il problema non è la **riservatezza** dei dati pubblici, ma la loro **autenticità*** — cioè avere la certezza che la chiave pubblica ricevuta appartenga davvero al soggetto giusto e non a un impostore che si è messo in mezzo.

**Visione**: la crittografia asimmetrica risolve il problema di *scambiare* segreti tra sconosciuti, ma ne apre un altro: *come faccio a sapere che questa chiave pubblica è tua e non di chi sta fingendo di essere te?* Tutto il §6 è la risposta a questa domanda.

---

## 6. Certificazione delle chiavi pubbliche — di chi mi fido?

Serve un modo per **associare con certezza una chiave pubblica al suo legittimo titolare** (l'unico possessore della corrispondente chiave privata). Ci sono due modelli, ed è la distinzione teorica più importante del modulo insieme a firma-vs-cifratura.

### 6.1 Web of trust — fiducia distribuita

Nel **modello web of trust** (rete di fiducia, il modello nativo di PGP/GPG):
- l'autenticità di una chiave pubblica è **testimoniata da altri utenti** (che la firmano);
- l'utente che riceve una chiave da uno sconosciuto può decidere di **accettarla come autentica se è firmata da qualcuno di cui si fida**;
- **Vantaggio**: **nessuna entità "super partes"** di cui doversi fidare per forza — la fiducia nasce dal basso, dalle relazioni tra utenti;
- **Svantaggio**: **pessima scalabilità** — funziona in comunità in cui le persone si conoscono e firmano le reciproche chiavi (i "key signing party"), non su scala Internet dove miliardi di sconosciuti dovrebbero fidarsi a vicenda.

Questo modello è concretamente ciò che fa il comando `gpg --sign-key` (§8.9): firmare la chiave pubblica di qualcuno significa *testimoniare* che quella chiave è davvero sua.

### 6.2 Modello infrastrutturale — PKI e certificati

Nel **modello infrastrutturale**:
- esiste una **terza parte fidata** (Certification Authority, CA) che documenta l'associazione chiave↔titolare;
- questa associazione, attestata dalla CA, prende la forma di un **certificato di chiave pubblica**, standardizzato come **ITU-T X.509v3**.

Un **certificato** è, in sostanza, la chiave pubblica del titolare + i suoi dati identificativi, il tutto **firmato dalla CA** (S14: firma = hash + cifratura con la privata *della CA*). L'insieme di CA, certificati, procedure e ruoli è la **Public Key Infrastructure (PKI)**.

**Verifica di un certificato** (l'iter che risponde alla domanda "di chi mi fido?"):
1. Ricevo un messaggio firmato → mi procuro il **certificato del mittente**;
2. con la chiave (pubblica) del certificato **verifico la firma** del messaggio → se ok, messaggio integro e autentico;
3. **ma il certificato stesso è integro e autentico?** → è **firmato dalla CA**;
4. mi procuro il **certificato della CA**, con la sua chiave verifico la firma del certificato del mittente → se ok, il certificato è integro e autentico.

Ma allora *quando finisce questo iter*? Il certificato della CA è firmato da un'altra CA, e così via: si forma una **certificate chain** (catena di certificati). La catena termina in una **root CA**, che **firma il proprio certificato** (certificato *self-signed*): la fiducia nella root CA non deriva da nessun altro, è **preinstallata** e assunta come radice (i browser e i sistemi operativi arrivano con un elenco di root CA fidate).

> **Web of trust vs PKI — la disambiguazione da esame** (facile invertirle):
> - **Web of trust**: fiducia **orizzontale/distribuita**, gli utenti si firmano le chiavi a vicenda, **nessuna autorità centrale**. Pro: niente ente super partes. Contro: non scala.
> - **PKI infrastrutturale**: fiducia **verticale/gerarchica**, una **CA** (terza parte fidata) firma i certificati, catena che risale a una **root CA** self-signed. Pro: scala (è il modello di TLS/HTTPS, S13). Contro: devi fidarti per forza delle root CA.

---

## 7. Uno sguardo al futuro — Quantum Key Distribution (BB84)

Le slide chiudono la parte teorica con una prospettiva futura sulla **distribuzione delle chiavi** sfruttando la fisica quantistica. (Attenzione a non confondere: S14 parlava di quantum computing come *minaccia* — Shor rompe RSA; qui il quantum è invece uno *strumento difensivo* per distribuire chiavi in modo intrinsecamente sicuro.)

### 7.1 Qubit e misura — l'ingrediente fisico

Un **qubit** è un sistema quantistico a due stati (es. la polarizzazione di un fotone). Può trovarsi in una **sovrapposizione** `|v⟩ = a|0⟩ + b|1⟩` (con `|a|² + |b|² = 1`). I fatti che servono a BB84:
- **misurare un qubit ha senso solo rispetto a una base** (quella del dispositivo di misura);
- **l'atto di misura cambia lo stato** del qubit: misurando `|v⟩` ottieni `|0⟩` con probabilità `|a|²` (e lo stato *diventa* `|0⟩`) oppure `|1⟩` con probabilità `|b|²`;
- se misuri nella base "giusta" (quella in cui il fotone è stato preparato) ottieni un risultato **deterministico**; se misuri nella base "sbagliata", il risultato è **casuale (50-50)** e — cruciale — **hai alterato irreversibilmente il fotone**;
- **un qubit non può essere clonato** (no-cloning) → non puoi fare tante misure su copie.

### 7.2 Il protocollo BB84 (Bennett & Brassard, 1984)

Obiettivo: stabilire una **chiave segreta condivisa** tra Alice e Bob (una sequenza casuale di 0 e 1). Scenario: un **canale quantistico** (per i fotoni) + un **canale classico** (pubblico, per confrontarsi). L'origliatrice è Eve.

1. Alice sceglie a caso una stringa di bit **e** una base per ciascuno (base standard `S={↑,→}` o base di Hadamard `H={↗,↖}`), codifica ogni bit nella sua base e invia i fotoni a Bob.
2. Bob, per ogni fotone, **sceglie a caso una base** con cui misurarlo. Ha il 50% di probabilità di indovinare la stessa base di Alice (→ bit corretto), 50% di sbagliarla (→ bit casuale).
3. Sul **canale classico** Alice e Bob si rivelano *quali basi* hanno usato (non i bit): **tengono solo i bit in cui le basi coincidono**, scartano gli altri. Quei bit formano la chiave.

### 7.3 Perché è sicuro — Eve si tradisce

Se Eve intercetta un fotone deve misurarlo, ma **non conosce la base di Alice** → indovina la base col 50%. Quando sbaglia base **altera la polarizzazione** del fotone, e quel disturbo si propaga a Bob. Risultato: la manomissione di Eve introduce **errori** nei bit di Alice e Bob (circa il 25% di probabilità che Bob misuri un bit diverso da quello inviato, per i bit toccati da Eve). Confrontando pubblicamente un campione di `n` bit, Alice e Bob hanno una probabilità `1/2²ⁿ` che l'intercettazione di Eve passi inosservata → **con abbastanza bit, l'origliamento è rilevabile con certezza pratica**.

**Visione**: BB84 non nasconde la chiave con la difficoltà computazionale (come RSA/DH), ma con una **legge fisica** — misurare disturba, quindi ogni intercettazione lascia tracce. Non garantisce il *successo* (l'attacco può far fallire lo scambio), ma garantisce che una chiave scambiata con successo è *segreta*.

---

## 8. LAB — GPG in pratica

Questa è la parte operativa: **GnuPG (gpg)** è l'implementazione con cui si toccano con mano tutti i concetti visti (generazione, custodia con passphrase, distribuzione via keyserver, cifratura ibrida, firma, web of trust). Per ogni comando: cosa fa (meccanismo) e a cosa serve nel flusso (visione).

### 8.1 GPG vs PGP — cosa sono

- **PGP** (Pretty Good Privacy): nato negli anni '90, oggi proprietà di **Symantec**. Soluzione **proprietaria**, storicamente lo standard *de facto* per la crittografia dei file.
- **GPG** (GnuPG, GNU Privacy Guard): implementazione **open source** dello standard **OpenPGP**, definita da **RFC 4880**. Alternativa libera a PGP; **può aprire/decifrare file cifrati da PGP** (interoperabile).

**Da esame**: PGP proprietario (Symantec) vs GPG open source (GnuPG), ma **funzionalmente equivalenti**, entrambi conformi a OpenPGP.

### 8.2 Generare una chiave — `gpg --gen-key`

```bash
gpg --gen-key
```

Il comando è interattivo e chiede:
- **identità** (nome + email — sarà lo *user ID* associato alla chiave);
- **grandezza della chiave**: **>= 2048 bit** (§2.7: sotto i 2048 il modulo RSA è troppo debole);
- **data di scadenza** (importante!) — una chiave con scadenza si "auto-revoca" nel tempo, limitando i danni se un giorno venisse compromessa senza che tu te ne accorga;
- **passphrase** — cifra la chiave privata a riposo (§3.1: "cifratura con passphrase").

**Meccanismo**: gpg genera la coppia (per un asimmetrico servono primi + test di primalità, §2.1 — da cui la raccolta di entropia). Il risultato è una coppia chiave pubblica/privata legata al tuo user ID. **Visione**: questo unico comando compie in un colpo generazione (§2) e memorizzazione protetta (§3, via passphrase).

> Nota sui default moderni: le slide del lab mostrano un esempio a **RSA-2048**, ma le versioni recenti di gpg tendono a generare per default chiavi a **curva ellittica Ed25519** — infatti la chiave reale di Prandini fornita come artefatto di lab (`Chiave_pubblica_Marco_Prandini.pdf`) è proprio una **Ed25519** (algoritmo di firma EdDSA). Concettualmente non cambia nulla: è sempre una coppia pubblica/privata asimmetrica; cambia solo il problema matematico difficile sottostante (curve ellittiche invece di fattorizzazione).

### 8.3 Dove vivono le chiavi — la cartella `~/.gnupg/`

```bash
cd ~
cd .gnupg/
ls -l
```

Contenuto:
- **`pubring.kbx`** → il **portachiavi pubblico** (keyring): tutte le chiavi pubbliche che conosci (la tua + quelle importate).
- **`private-keys.d/`** → directory con le **chiavi private**, ogni file con estensione **`.key`** (cifrate con la passphrase).
- **`gpg.conf`** → file di configurazione (default, preferenze).

**Visione**: questa è la memorizzazione (§3) resa concreta. Le pubbliche stanno insieme in un keyring condivisibile; le private stanno separate, una per file, cifrate. Rubare `pubring.kbx` non serve a nulla (sono dati pubblici); rubare `private-keys.d/` senza la passphrase nemmeno (sono cifrate).

### 8.4 Importare una chiave — `gpg --import`

```bash
gpg --import                          # poi incolli il blocco della chiave pubblica da terminale
gpg --import vostrachiavepubblica.pub  # oppure importi direttamente il file
```

All'import viene stampato il **Key-ID** della chiave. Per visualizzare:

```bash
gpg --list-keys Key-ID    # una chiave specifica
gpg --list-keys           # senza Key-ID: tutte le chiavi importate
```

**Visione**: importare la chiave pubblica di qualcuno significa aggiungerla al tuo `pubring.kbx` per poterla usare (cifrare per lui, o verificarne le firme). È il primo passo per verificare il file firmato di Prandini (§8.10).

### 8.5 Esportare la chiave **pubblica** — `gpg --export`

```bash
gpg --output public.pgp --armor --export identita@email
```

Anatomia:
- `--output public.pgp` → scrive su file invece che a schermo;
- `--armor` → **ASCII armor**: codifica la chiave in testo base64 (il blocco `-----BEGIN PGP PUBLIC KEY BLOCK-----`) invece che in binario, così è incollabile in una mail o su un sito. È esattamente il formato dell'artefatto `Chiave_pubblica_Marco_Prandini.pdf`;
- `--export identita@email` → esporta la pubblica di quello user ID.

**Visione**: la chiave pubblica **va distribuita** (§5.2: distribuirla è l'obiettivo, il pericolo è solo che qualcuno la sostituisca). Esportarla e pubblicarla è normale e desiderabile.

### 8.6 Esportare la chiave **privata** — `--export-secret-key` (da NON fare)

```bash
gpg --output private.pgp --armor --export-secret-key vostraidentita@email
```

**Ma è fortemente sconsigliato**: non ci sono situazioni in cui sia strettamente necessario e **non deve MAI essere distribuita**. L'unica eccezione legittima è un **backup** della chiave privata, per cui esiste l'opzione dedicata:

```bash
gpg --output backupkeys.pgp --armor --export-secret-keys \
    --export-options export-backup vostraidentita@email
```

**Visione — il legame con la teoria**: qui si vede in pratica la tensione del §3.1 (backup vs non-diffusione). La chiave privata si esporta *solo* per backup, mai per condividerla. E ricorda il §3.2: se è una chiave *di sola firma*, nemmeno il backup serve (basta rigenerarla).

> **Il verso, tradotto nei comandi** (contro la confusione tipica): la **pubblica** si esporta *per distribuirla a tutti* (`--export`); la **privata** *non esce mai*, se non per un backup personale (`--export-secret-key(s)`). Chi cifra per te usa la tua **pubblica**; solo tu decifri con la tua **privata**. Chi verifica le tue firme usa la tua **pubblica**; solo tu firmi con la tua **privata**.

### 8.7 Pubblicare e recuperare chiavi — i keyserver

I **keyserver** sono server dove pubblicare le proprie chiavi pubbliche e recuperare quelle altrui. Prima serve il **Key-ID** in formato lungo:

```bash
gpg --keyid-format LONG --list-keys a.melis@unibo.it
# pub   rsa2048/9D6A4A7849845D01 2018-04-01 [SC] [expires: 2023-03-31]
#       AD54A494EF4F97AF54E9FDC59D6A4A7849845D01
# uid   [ unknown] Andrea Melis <a.melis@unibo.it>
```

Poi:

```bash
# pubblicare la propria chiave sul keyserver
gpg --keyserver pgp.mit.edu --send-keys 9D6A4A7849845D01

# recuperare la chiave pubblica di un target (dato il suo Key-ID, ottenuto es. dalla sua mail)
gpg --keyserver pgp.mit.edu --recv-keys 49845D01
```

Keyserver disponibili: **pgp.mit.edu**, **keys.openpgp.org**, e alternativi **hkp://keyserver.ubuntu.com**, **hkp://keys.gnupg.net**.

**Visione**: il keyserver è l'infrastruttura di **distribuzione** (§5) delle chiavi pubbliche su scala Internet. Ma attenzione: un keyserver **non certifica** l'autenticità — chiunque può caricare una chiave con qualunque nome/email. È di nuovo il problema del §5.2/§6: il keyserver risolve *far arrivare* la chiave, non *fidarsi* che sia autentica (per quello servono web of trust o PKI).

### 8.8 Cifrare, cifrare+firmare, decifrare

**Cifrare** un file con la chiave pubblica di un destinatario:

```bash
gpg --encrypt --armor -r identita@mail file_da_crittare
```
- `-r` (recipient) → destinatario; **con più `-r` si cifra per più destinatari** (ognuno potrà decifrare con la propria privata — è il cifrario ibrido di S14 §14.3: il file è cifrato una volta con una chiave di sessione simmetrica, e quella chiave è cifrata separatamente con la pubblica di ciascun destinatario);
- `--armor` → output in testo ASCII.

**Cifrare *e* firmare** — basta aggiungere `--sign`:

```bash
gpg --encrypt --armor --sign -r identita@mail file_da_crittare
```
Così il file è insieme **riservato** (cifrato per il destinatario) **e autenticato** (firmato con la *tua* privata → il destinatario, decifrando, verifica anche che venga da te e sia integro).

**Decifrare** con la propria chiave privata:

```bash
gpg --decrypt file_da_crittare
```

**Il verso, ancora una volta** (meccanismo): cifrare usa la **pubblica del destinatario** (`-r destinatario`); decifrare usa la **tua privata** (implicita: gpg cerca nella tua keyring la privata giusta e chiede la passphrase). Firmare usa la **tua privata**; verificare userà la **pubblica del firmatario**.

### 8.9 Firmare una chiave — `gpg --sign-key` (il web of trust in pratica)

```bash
gpg --sign-key identita@mail
```

Firma la **chiave pubblica di qualcun altro**: con questo atto **testimoni** (col peso della tua chiave) che quella chiave pubblica appartiene davvero a quella persona. È il **web of trust** del §6.1 reso operativo: la tua firma sulla chiave di X aiuta un terzo, che si fida di te, a fidarsi anche di X.

**Attenzione a non confondere `--sign` con `--sign-key`**: `--sign` (§8.8) firma **un file/messaggio** (autenticità del contenuto); `--sign-key` firma **una chiave** (certificazione dell'identità del titolare). Scopi diversi.

### 8.10 Esercizio concreto — verificare il file firmato di Prandini

I due artefatti del lab compongono un esercizio reale di verifica:
1. **Importi** la chiave pubblica di Prandini: `gpg --import Chiave_pubblica_Marco_Prandini.pdf` (è un `PGP PUBLIC KEY BLOCK`, user ID `Marco Prandini (SIC2026) <marco.prandini@unibo.it>`, Ed25519).
2. **Verifichi** il file firmato: `File_firmato.pdf` è in realtà `setup_ipt.sh` firmato (firma *one-pass*, compressa) con quella chiave.
   ```bash
   gpg --decrypt File_firmato.pdf     # estrae il file e riporta l'esito della firma
   # oppure, se fosse una firma staccata, gpg --verify
   ```
   gpg ricalcola l'hash del contenuto, verifica la firma con la pubblica di Prandini appena importata, e stampa **"Good signature from Marco Prandini..."** se tutto torna.

**Visione**: questo è l'intero modulo in tre righe — distribuzione della pubblica (§5), verifica di autenticità/integrità (S14 §14.2: si verifica con la **pubblica** del firmatario), e la fiducia che quella pubblica sia davvero di Prandini (§6, che nel mondo reale confermeresti confrontando il *fingerprint* per un canale fidato).

---

## 9. Threat model del modulo

### 9.1 Firma vs cifratura — cosa garantisce ciascuna

| | **Firma digitale** | **Cifratura** |
|---|---|---|
| Proprietà garantita | **Integrità + Autenticità** (il documento non è alterato ed è del firmatario dichiarato) | **Confidenzialità** (solo il destinatario legge) |
| Chi la produce, con quale chiave | Il **mittente**, con la **propria chiave PRIVATA** | Il **mittente**, con la chiave **PUBBLICA del destinatario** |
| Chi la "annulla"/verifica, con quale chiave | Chiunque, con la **chiave PUBBLICA del mittente** | Il **destinatario**, con la **propria chiave PRIVATA** |
| Cosa NON garantisce | Non nasconde il contenuto (il documento resta leggibile) | Non prova chi l'ha mandato né che sia integro |

Le due sono **ortogonali** e spesso combinate (`--encrypt --sign`): si ottiene un messaggio che è insieme riservato *e* autenticato.

### 9.2 Il verso corretto — la trappola numero uno

Da fissare in modo indelebile (è l'errore che l'esame cerca di indurre invertendo i termini):

> - **FIRMA**: si firma con la **propria chiave PRIVATA**, si verifica con la **chiave PUBBLICA altrui**.
> - **CIFRATURA**: si cifra con la **chiave PUBBLICA del destinatario**, si decifra con la **propria chiave PRIVATA**.

Regola mnemonica: **la chiave privata fa sempre l'operazione che "solo tu puoi fare"** (firmare a tuo nome, decifrare ciò che è destinato a te); **la chiave pubblica fa sempre l'operazione che "chiunque può fare"** (verificare la tua firma, cifrare qualcosa per te). Se in una domanda leggi "firma con la chiave pubblica" o "decifra con la chiave pubblica" → **è falso**.

### 9.3 Se una chiave privata è compromessa

Dipende — di nuovo — da *quale* chiave (§3):
- **Chiave privata di firma compromessa**: l'attaccante può firmare a tuo nome (impersonarti) *finché la revoca non si propaga*. Rimedio: **revocare** la chiave e **sostituirla** (nessun backup da recuperare, §3.2). Le firme legittime già emesse *prima* della compromissione restano problematiche solo se non c'è marca temporale che le collochi prima dell'evento.
- **Chiave privata di decifrazione compromessa**: **tutto ciò che è mai stato cifrato per te diventa leggibile dall'attaccante** (danno retroattivo su tutto il cifrato archiviato che riesce a intercettare/recuperare). Rimedio: sostituire la chiave per il futuro, ma il passato è irrimediabilmente esposto. Questo è il motivo per cui la protezione a riposo (passphrase/HSM) è così critica per le chiavi di decifrazione.

### 9.4 Attaccante sulla distribuzione (MITM) e difese

Il §5.2 mostrava l'attacco attivo che **sostituisce le chiavi pubbliche**. Le difese sono i modelli di certificazione del §6:
- **web of trust**: la firma di terzi fidati sulla chiave (verificabile con `--sign-key`) rende una chiave sostituita non fidata (l'impostore non ha le firme giuste);
- **PKI/certificati X.509**: la firma della CA lega chiave e identità; una chiave sostituita non ha un certificato valido firmato dalla CA.

In entrambi i casi, la difesa pratica dell'utente è **verificare il fingerprint** della chiave su un canale indipendente prima di fidarsene.

---

## 10. Domande di autoverifica — stile quiz teorico (40%)

> Rispondi *prima* di leggere le soluzioni negli appunti. Stile dell'esame: vero/falso e scelta multipla con **penalità sulle sbagliate** — se non sei sicuro, ragiona sul meccanismo.

**Vero o Falso:**
1. Per generare una chiave simmetrica robusta è sufficiente un buon generatore di numeri casuali.
2. Un PRNG, noto il seme, produce una sequenza prevedibile.
3. Un TRNG è più veloce ed efficiente di un PRNG.
4. Una chiave di firma, se compromessa, va recuperata da un backup.
5. Una chiave di decifrazione richiede un backup perché la sua perdita è irreversibile.
6. In un sistema simmetrico con N soggetti servono N chiavi segrete.
7. Il problema principale nella distribuzione delle chiavi pubbliche è la loro riservatezza.
8. Un attaccante passivo che intercetta una chiave pubblica ne compromette la sicurezza.
9. Nel modello web of trust esiste un'autorità centrale (CA) che certifica le chiavi.
10. Una root CA possiede un certificato firmato da se stessa (self-signed).
11. Si firma un documento con la propria chiave pubblica.
12. Si cifra un messaggio per Bob usando la chiave pubblica di Bob.
13. Una chiave RSA di 256 bit è robusta come una chiave simmetrica AES di 256 bit.
14. Il comando `gpg --export-secret-key` va usato normalmente per condividere la propria chiave con altri.
15. In BB84, se Eve misura un fotone nella base sbagliata ne altera lo stato e può essere rilevata.
16. Il flag `--armor` di gpg produce output binario compatto.
17. Una firma digitale garantisce la confidenzialità del documento.
18. DES, con i suoi 56 bit di chiave, è oggi forzabile a forza bruta.

**Scelta multipla:**

19. Quale opzione elenca correttamente le tre fasi del ciclo di vita di una chiave?
    a) cifratura, firma, verifica
    b) generazione, memorizzazione, distribuzione
    c) confusione, diffusione, permutazione
    d) import, export, revoke

20. In un sistema simmetrico con N soggetti, il numero di chiavi segrete necessarie è:
    a) N   b) N-1   c) N(N-1)/2   d) 2ᴺ

21. Per verificare la firma su un messaggio ricevuto da Alice si usa:
    a) la chiave privata di Alice   b) la chiave pubblica di Alice   c) la propria chiave privata   d) la propria chiave pubblica

22. Quale comando gpg cifra un file per il destinatario `bob@x.it` in formato testo?
    a) `gpg --sign -r bob@x.it file`
    b) `gpg --decrypt bob@x.it file`
    c) `gpg --encrypt --armor -r bob@x.it file`
    d) `gpg --export bob@x.it file`

23. Il modello di certificazione delle chiavi pubbliche **privo di un'autorità centrale**, basato sulle firme reciproche degli utenti, è:
    a) PKI X.509   b) KDC   c) web of trust   d) key escrow

24. Rispetto a GPG, PGP è:
    a) uno standard open source definito da RFC 4880
    b) una soluzione proprietaria (Symantec)
    c) un algoritmo di hash
    d) un keyserver

25. La distinzione corretta tra `gpg --sign` e `gpg --sign-key` è:
    a) sono sinonimi
    b) `--sign` firma un file/messaggio, `--sign-key` firma (certifica) la chiave pubblica di qualcuno
    c) `--sign` firma una chiave, `--sign-key` cifra un file
    d) `--sign` è per RSA, `--sign-key` per Ed25519

---

## 11. Connessioni con altri moduli

**Con S14 (Crittografia) — il legame diretto e portante**:
- S14 spiegava la *matematica* (RSA `c=mᵉ mod n`, hash, firma = hash cifrato con la privata, cifrari ibridi); S15 spiega il *ciclo di vita* di quelle chiavi e le rende operative con gpg. Fare S14 prima di S15 è ciò che rende i comandi gpg comprensibili invece che magici (lo diceva già la §19 di S14).
- La **firma digitale** di S14 §14.2 è ciò che `gpg --sign` / `--verify` eseguono; il **cifrario ibrido** di S14 §14.3 è *esattamente* ciò che fa `gpg --encrypt -r` (chiave di sessione simmetrica + chiave cifrata con la pubblica di ogni `-r`).
- **Non ripetiamo, costruiamo sopra**: S14 assumeva la chiave "già data e fidata"; S15 mostra che generarla (§2), custodirla (§3) e soprattutto *fidarsi* della pubblica altrui (§5-6) è il vero problema aperto. Il §9.2 (verso firma/cifratura) rafforza la tabella di S14 §14 perché è la confusione più a rischio.

**Con S13 (Protezione delle comunicazioni, TLS/OpenSSL) e la PKI**:
- I **certificati X.509** e la **catena fino alla root CA** (§6.2) sono la stessa PKI su cui poggia HTTPS/TLS. Il "di chi mi fido?" che qui risolviamo con web of trust *o* CA è ciò che in TLS è sempre risolto con le **CA** (il browser ha le root CA preinstallate).
- La **distribuzione con MITM sulle chiavi pubbliche** (§5.2) è la minaccia che i certificati TLS neutralizzano.

**Con S2 (Autenticazione)**:
- La **cifratura della chiave privata con passphrase** (§3.1, e la passphrase di `gpg --gen-key`) è lo stesso principio del proteggere un segreto derivandolo da una password.
- Il **challenge-response asimmetrico** di SSH (S2) usa la stessa coppia pubblica/privata: si autentica dimostrando il possesso della privata — stesso verso del §9.2.

**Con S5 (Firewall)** — curiosità dal lab: l'artefatto `File_firmato.pdf` è in realtà `setup_ipt.sh` firmato, cioè uno script di configurazione **iptables** (il tema di S5) distribuito con firma per garantirne l'integrità/autenticità prima di eseguirlo. È l'uso reale di gpg: firmare uno script perché chi lo scarica sia certo che non sia stato manomesso.

---

## 12. Riepilogo

- **Ciclo di vita** delle chiavi: **generazione → memorizzazione → distribuzione**, più gestione e certificazione. La crittografia pura non si rompe; si rompe la gestione.
- **Generazione**: simmetriche = buon RNG; asimmetriche = numeri primi (random + test di primalità). **TRNG** (fisico, imprevedibile, lento) genera il seme; **PRNG** (algoritmico, deterministico, veloce, noto-il-seme-nota-la-sequenza) lo espande. Test di casualità: **NIST SP 800-22, 15 test**. Robustezza: contro forza bruta serve lunghezza (**56 bit forzabili, 128+ no**, muro termodinamico di Landauer); contro fattorizzazione (RSA) servono **moduli grandi ≥ 2048 bit**.
- **Memorizzazione**: chiave di **decifrazione → backup SÌ** (perdita irreversibile) + non-diffusione; chiave di **firma → backup NO** (basta sostituirla). Accorgimenti: passphrase, HSM, key escrow, secret sharing.
- **Gestione/numero chiavi**: asimmetrico **O(N)** (una pubblica per soggetto) vs simmetrico **O(N²) = N(N-1)/2**.
- **Distribuzione**: simmetriche mai in chiaro (scambio manuale, KDC, DH). Asimmetriche: passivo non fa danni, **attivo (MITM) sostituisce le chiavi** → il problema non è riservatezza ma **autenticità**.
- **Certificazione**: **web of trust** (firme reciproche tra utenti, no autorità, non scala) vs **PKI infrastrutturale** (CA + certificati **X.509v3** + catena fino alla **root CA** self-signed, scala).
- **BB84 (QKD)**: distribuisce una chiave sfruttando che misurare un qubit nella base sbagliata lo altera → l'origliatrice Eve è **rilevabile**. (Il quantum qui difende; in S14 con Shor attaccava.)
- **GPG**: OpenPGP/RFC 4880 open source (vs PGP proprietario). `--gen-key` (size ≥2048, scadenza, passphrase); chiavi in `~/.gnupg/` (`pubring.kbx`, `private-keys.d/*.key`); `--import`/`--export` (pubblica sì, privata mai se non backup); keyserver `--send-keys`/`--recv-keys`; `--encrypt --armor -r` (cifra con la **pubblica del destinatario**); `--sign`/`--decrypt`; `--sign-key` (web of trust).
- **Verso da inchiodare**: **firma** = privata propria (produci) / pubblica altrui (verifichi); **cifratura** = pubblica del destinatario (cifri) / privata propria (decifri). La **privata** fa ciò che solo tu puoi fare; la **pubblica** ciò che chiunque può fare.

<!-- AUTO-LINKS:START -->
<!-- AUTO-LINKS:END -->
