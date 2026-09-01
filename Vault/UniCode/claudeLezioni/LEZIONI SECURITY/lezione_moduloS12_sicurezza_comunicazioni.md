# Lezione — Modulo S12: Sicurezza delle comunicazioni

**Corso**: Lab Sicurezza Informatica T
**Fonte primaria**: `SLIDE TEORIA/SICINF/Sicurezza_delle_comunicazioni_23_aprile.pdf` (Marco Prandini, "Chapter 7", 62 slide)
**Tipo**: modulo teorico (nessun LAB dedicato). Rilevante per il **quiz teorico** (40% del voto): è un catalogo di attacchi al traffico di rete, terreno fertile per domande vero/falso e a scelta multipla.

---

## Dove si colloca questo modulo, e il suo threat model

Questo modulo risponde a una sola domanda, declinata in molti modi: **cosa può fare un avversario che ha accesso, anche solo parziale, al percorso che i tuoi dati attraversano in rete?**

La comunicazione tra due applicazioni non è un filo diretto: è una catena di segmenti fisici (LAN Ethernet, Wi-Fi, link tra router) attraversati da un pacchetto che cambia "vestito" a ogni salto. Ogni segmento, ogni apparato intermedio (switch, router, resolver DNS) è un punto in cui qualcuno può **ascoltare** (attacco passivo) o **intervenire** (attacco attivo). Il modulo cataloga sistematicamente questi punti, layer per layer.

**Il threat model del modulo, in una frase**: l'attaccante mira alle proprietà della comunicazione — **riservatezza** (sniffing, recupero chiavi), **integrità e autenticità** (spoofing, hijacking), **disponibilità** (DoS/DDoS) — sfruttando il fatto che i protocolli fondamentali di Internet (ARP, IP, BGP, DNS, TCP) sono nati **senza autenticazione né cifratura**. Il difensore, in questo modulo, è quasi sempre in posizione di svantaggio strutturale: le contromisure vere (canali sicuri) sono un *aggiunta* posticcia a protocolli progettati fidandosi di tutti.

**Confine con S13 — importante per non fare confusione all'esame.** L'outline del PDF stesso divide il territorio in due: gli **attacchi** (questo modulo, S12) e le **contromisure: canali sicuri** (data-link → VLAN/802.1X, network → IPSec, transport → TLS). Nel PDF la sezione contromisure è *in grigio*, cioè annunciata ma non svolta: le slide reali si fermano al DNS pharming. Quelle contromisure sono il contenuto di **S13 (Protezione delle comunicazioni + OpenSSL/TLS)**. Quindi:

- Sniffing, MAC/ARP/IP/BGP/DNS spoofing e hijacking, DoS → **stanno QUI, in S12** (lato attaccante).
- VLAN, 802.1X, IPsec, TLS, VPN come *meccanismi di protezione* → **sono S13** (lato difensore).

Il PDF di S12 nomina comunque, sulle slide "The Internet model", *quali* famiglie di tecnologie di sicurezza risolvono il problema a ciascun layer: le uso come "puntatori in avanti" verso S13/S14, senza svilupparle qui (non lo fa nemmeno la slide). Dove il PDF dice "vedi più avanti", il "più avanti" è S13.

---

## Parte 1 — Richiami di reti (senza questi, gli attacchi non si capiscono)

Metà del PDF è ripasso di reti. Non è riempitivo: **ogni attacco della seconda metà sfrutta esattamente un meccanismo di questa prima metà**. Li tratto quindi come "premesse dell'attacco", segnalando fin da subito la vulnerabilità che ciascuno nasconde.

### 1.1 Internet come "rete di reti"

Internet è una grande *rete di reti*. Il mattone elementare è la **network IP**: un'"isola" che contiene gli **host** (i nodi terminali) e che è connessa alle altre isole da apparati-ponte, i **router** (o **gateway**), calcolatori specializzati.

- **Meccanismo**: le isole sono isolate per default; per farle parlare servono (a) collegamenti fisici tra isole, spesso con tecnologia diversa da quella interna all'isola; (b) apparati che sappiano usare quei collegamenti; (c) un modo per scegliere il collegamento giusto verso la destinazione.
- **Visione (sicurezza)**: il fatto che il traffico attraversi apparati e link *di terzi* è la radice del problema. Non controlli il percorso, quindi devi assumere che sia ostile.

### 1.2 Indirizzo globale vs locale, rete logica vs rete fisica

Due distinzioni che Prandini tiene separate con cura:

- **Indirizzo globale**: valido su tutta la rete, deve essere **univoco** (nessuna replica → nessuna ambiguità), assegnato con una procedura di gestione globale. È l'**indirizzo IP** pubblico.
- **Indirizzo locale**: valido solo in una sottoporzione (dentro un terminale, o in un dominio di rete specifico), **può non essere globalmente univoco**, assegnabile con procedura puramente locale. Esempio: l'**indirizzo MAC** (locale al segmento fisico), o gli IP privati.

Parallelamente:

- **Rete logica**: la network IP (o *subnet*) a cui un host appartiene *logicamente*.
- **Rete fisica**: la rete (tipicamente una **LAN**) a cui un host è *effettivamente* connesso.

L'architettura a strati **nasconde gli indirizzi fisici** e lascia che le applicazioni lavorino solo con indirizzi IP. Questa astrazione è comoda ma, come vedremo, è anche ciò che permette a un attaccante di manipolare la corrispondenza IP↔MAC senza che l'applicazione se ne accorga.

### 1.3 Le tecnologie e la rete wireless

Ogni network IP può essere realizzata con una tecnologia specifica: **Wi-Fi** (wireless in area locale), **ADSL/xDSL** (media distanza via cavo, infrastruttura di un fornitore pubblico), **Ethernet** (breve distanza via cavo, privata, in area locale), **GPRS/EDGE/LTE** (radio a media distanza, infrastruttura pubblica).

Architettura Wi-Fi (802.11): un **Basic Service Set (BSS)** è l'insieme delle stazioni gestite da un **Access Point (AP)** / *base station*; l'AP fa da ponte verso la rete cablata attraverso il **Distribution System**; i client sono le **Wireless Station**.

- **Visione (sicurezza)**: il wireless trasmette *in broadcast nell'etere*. Chiunque nel raggio riceve i frame senza dover toccare un cavo. Per questo il wireless *dovrebbe* essere sempre cifrato — ed è il motivo per cui gli attacchi di "wireless key recovery" (§2.5) sono così centrali.

### 1.4 Switch, hub e il "learning bridge"

Un **bridge** è un ponte tra due LAN; un bridge tra più di due LAN (stessa tecnologia) è un **hub**. Uno **switch** Ethernet fa una cosa simile all'hub ma meglio: opera **commutazione a livello 2 basata sull'indirizzo MAC**, trasferendo trame da più porte di ingresso a più porte di uscita *contemporaneamente*.

Differenza cruciale (ricorre spesso nei quiz):

| | **Hub** | **Switch** |
|---|---|---|
| Comportamento | bus collassato = **mezzo condiviso**, trasmissione **broadcast** delle trame | sistema di commutazione = ri-trasmissione **selettiva** delle trame |
| Capacità aggregata | = capacità della singola porta | **superiore** a quella della singola porta |
| Esempio Fast Ethernet | 100 Mbit/s totali | 200 Mbit/s (due flussi paralleli) |

Come fa lo switch a essere selettivo? Costruisce una **tabella di inoltro** (implementata in **CAM**, *Content Addressable Memory*) che associa ogni MAC alla porta su cui quel MAC è raggiungibile. La riempie *imparando* (**learning bridge / learning switch**): quando vede una trama in ingresso da una porta, registra "il MAC sorgente sta su questa porta". Se a una porta è connesso un altro switch, da quella porta si raggiungono *molti* MAC.

- **Visione (sicurezza)**: lo switch offre una protezione *contro lo sniffing*, ma **limitata**. Idealmente manda ogni trama solo sulla porta del destinatario (gli altri non la vedono). Ma la CAM è finita, e il comportamento di *fallback* quando un MAC non è in tabella è **inondare in broadcast**. Questa è la crepa che il **MAC flooding** (§2.4) spalanca.

### 1.5 Interconnettere le LAN: switch vs router

- **LAN interconnesse via switch**: **unico dominio di broadcast**, funzionalmente equivalente a un'unica LAN (es. tutte in `192.168.8.0/22`).
- **LAN interconnesse via router**: **domini di broadcast separati** — permette di separare le LAN per **efficienza** e **sicurezza** (es. `192.168.8.0/24`, `.9.0/24`, `.10.0/23` distinte). Costo: **mobilità limitata** degli host da una LAN all'altra.

- **Visione (sicurezza)**: il router come *confine di broadcast* è già una prima linea di segmentazione. Molti attacchi di livello 2 (ARP poisoning, MAC flooding, MAC/IP spoofing) sono **confinati alla LAN**: non attraversano il router. La segmentazione via router quindi *contiene* il raggio d'azione dell'attaccante di livello 2 — è la stessa logica delle VLAN che vedrai come contromisura in S13.

### 1.6 Doppio indirizzamento nella LAN e ARP

Dentro una LAN/subnet ogni dispositivo ha **due** identità:

1. un **MAC address** — l'inoltro *fisico* del traffico avviene tra schede di rete;
2. un **indirizzo IP** — le applicazioni si conoscono come endpoint IP.

Serve tradurre l'uno nell'altro: lo fa **ARP — Address Resolution Protocol (RFC 826)**. Meccanismo:

- **ARP request** = **broadcast**: "*Who has 192.168.1.76? Tell 192.168.1.34 (at 54:8d:...)*" — la domanda arriva a *tutti* gli host del segmento.
- **ARP reply** = **unicast**: solo il possessore di quell'IP risponde "*192.168.1.76 is at 8d:ab:e4:0d:d8:5d*".
- **Caching opportunistico**: chiunque *vede passare* l'associazione IP↔MAC la mette in cache ("nice, I have learned that 192.168.1.34 is at 54:8d:... — let's cache this"), anche senza averla chiesta.

- **Visione (sicurezza)**: qui c'è il difetto di progetto più sfruttato del modulo. **ARP non ha autenticazione**: nessuno verifica che chi risponde sia davvero il proprietario dell'IP. Peggio, il caching opportunistico accetta anche reply *non richieste* (**gratuitous ARP**). Questa è l'esatta leva dell'**ARP poisoning** (§3.2.2).

### 1.7 Instradamento: consegna diretta vs indiretta

Quando un host ha un pacchetto da spedire, la **domanda cruciale** è: *"la destinazione è sulla mia network, o devo usare un ponte (router)?"* La **risposta**: ogni nodo ha una base dati di destinazioni; legge l'IP di destinazione, consulta la base dati, decide.

- **Direct delivery** (consegna diretta): IP sorgente e IP destinatario sono **sulla stessa rete fisica**; l'host spedisce il datagramma **direttamente** al destinatario. In trama: `L2 address = HOST3`, `IP address = HOST3` — **entrambi puntano al destinatario finale**.
- **Indirect delivery** (consegna indiretta): sorgente e destinatario **non** sono sulla stessa rete fisica; l'host manda il datagramma a un **router intermedio**. In trama: `L2 address = ROUTER1`, `IP address = HOST4` — **l'indirizzo L2 punta al prossimo salto, l'IP punta ancora al destinatario finale**.

Questa asimmetria è il concetto-chiave del routing e va capito bene:

> **Il MAC di destinazione cambia a ogni hop; l'IP di destinazione resta quello finale per tutto il viaggio.** Il **routing** è la scelta del percorso; ogni singolo salto si chiama **hop**. Da mittente a destinatario c'è **sempre esattamente una consegna diretta** (l'ultimo tratto, dall'ultimo router all'host finale — o l'unico tratto se sono già vicini) e **zero o più consegne indirette**.

- **Visione (sicurezza)**: il fatto che il MAC di destinazione sia "solo il prossimo ponte" è ciò che rende efficace l'ARP poisoning: se avveleno la cache facendoti credere che il MAC del gateway sia il mio, tu mi consegni *fisicamente* tutti i pacchetti diretti fuori dalla LAN, pur avendo scritto nell'IP la destinazione giusta. Tu pensi di parlare col router; parli con me.

### 1.8 Il modello Internet a strati e "dove agisce la sicurezza"

Il PDF chiude i richiami con quattro versioni della stessa figura (client → switch → router → router → server), evidenziando di volta in volta *quale problema* ogni layer risolve e *quali tecnologie di sicurezza* gli competono. Questa è la **mappa che collega S12 a S13/S14** — vale la pena memorizzarla come tabella:

| Layer | Problema che risolve | Tecnologie di sicurezza (→ dove le studi) |
|---|---|---|
| **Data link** (Ethernet/PPP) | *local connectivity* (connettività locale) | IEEE **802.1X**, **WPA2**, **Layer-2 VPN** → S13 |
| **Rete** (IP) | *global connectivity* (connettività globale) | **IPsec**, **Layer-3 VPN**, autenticazione router → S13 |
| **Trasporto** (TCP) | *end-to-end reliable data transfer* | **SSL/TLS** → S13 |
| **Applicazione** (HTTP…) | *transparent data exchange between applications* | autenticazione, crittografia, VPN applicative, soluzioni specifiche → S13/S14/S15 |

- **Visione**: ogni riga è "un attacco di S12 ↔ la sua difesa di S13". Sniffing/MAC-flooding/ARP-poisoning (link) ↔ 802.1X/WPA2/VLAN. IP/BGP hijacking (rete) ↔ IPsec/autenticazione router. TCP hijacking + DNS spoofing (trasporto/applicazione) ↔ TLS. **Se in un quiz ti chiedono "a quale layer opera IPsec?" la risposta è: rete/IP.**

---

## Parte 2 — Attacchi passivi

**Definizione (dal PDF)**: gli attacchi passivi **non modificano i dati in transito**. Sono utili all'aggressore e comunque dannosi per la vittima:

- la **scansione** è uno dei primi passi della ricognizione;
- lo **sniffing** può compromettere la **riservatezza** dei dati;
- il **recupero di una chiave** consente di **impersonare** la vittima.

Usati *contro se stessi*, questi stessi strumenti fanno parte di un **vulnerability assessment (VA)**.

- **Distinzione da tenere ferma**: "passivo" = non altera i dati, mira alla **riservatezza** e alla **ricognizione**. "Attivo" (Parte 3) = altera/inietta/interrompe, mira a **integrità, autenticità, disponibilità**. È la prima grande dicotomia del modulo, e una tipica domanda V/F ("lo sniffing è un attacco attivo" → **Falso**).

### 2.1 Scanning (→ è esattamente il LAB di S1)

Due granularità:

- **Scansione di una rete**: quali **indirizzi sono raggiungibili** (host vivi). Esempio dal PDF: `nmap -sP 137.204.57.200-205` → *"6 IP addresses (2 hosts up) scanned"*.
- **Scansione di un host**: quali **porte TCP/UDP sono aperte**; consente di **dedurre le versioni** del sistema operativo e dei servizi in esecuzione (*fingerprinting*). Esempio: `nmap -A 137.204.57.104` → elenca `21/tcp ftp vsftpd 3.0.2`, `22/tcp ssh OpenSSH 6.6.1p1`, `80/tcp http Apache 2.4.7`, con hostkey SSH, header del server, e persino l'OS (`Unix, Linux`).

**Loudness (rumorosità)**: a scopo VA la scansione può essere *aggressiva* (rumorosa); ma gli strumenti implementano **molti modelli di scansione silenziosa** per eludere il rilevamento.

- **Threat model — attaccante**: la scansione è la **fase di ricognizione** che precede tutto. Sapere versione esatta di FTP/SSH/Apache significa poter cercare l'exploit pubblico corrispondente (il ponte verso S3/S4).
- **Threat model — difensore**: un IDS/NIDS (S10) rileva le scansioni rumorose; un firewall (S5) fa apparire le porte come `filtered` anziché `open`/`closed`, negando informazione all'attaccante.

### 2.2 Sniffing (→ è lo strumento di S10)

Lo **sniffing richiede l'accesso fisico ai dati in transito**. Due modi per ottenerlo:

1. **essere già sulla rete locale**;
2. arrivarci **a seguito di un attacco di dirottamento** (ecco perché sniffing passivo e hijacking attivo spesso si combinano).

Su reti locali:

- **wireless**: *tutto dovrebbe essere criptato, ma molti protocolli sono difettosi* (→ §2.5);
- **cablate**: la crittografia esiste — **802.1x** per l'autenticazione delle porte, **802.1AE** per la cifratura del traffico (MACsec) — *ma non la usa quasi nessuno*.

Il PDF mostra un esempio con **Wireshark** (una cattura `.pcap` con traffico Netflix/DNS/TCP dissezionato frame per frame): lo strumento con cui hai lavorato tutto il LAB NIDS in S10.

- **Threat model — attaccante**: cattura credenziali in chiaro, cookie di sessione, contenuti. Non lascia tracce (è passivo!) → difficile da rilevare.
- **Threat model — difensore**: cifrare il traffico rende lo sniffing inutile (leggi solo ciphertext). È il *perché esistono* TLS (S13), 802.1AE, le VPN.

### 2.3 Precisazione importante: scanning e sniffing non sono la stessa cosa

Coppia facile da confondere. **Scanning** = *sondare attivamente* mandando pacchetti e osservando le risposte (genera traffico, può essere rumoroso, è ricognizione). **Sniffing** = *ascoltare passivamente* il traffico che già passa (non genera nulla di suo, è pura intercettazione). Entrambi sono classificati "passivi" nel senso che **non modificano i dati della vittima**, ma il primo *emette* pacchetti-sonda, il secondo no.

### 2.4 MAC flooding (l'attacco che riabilita lo sniffing su switch)

Ricorda (§1.4): lo switch offre protezione *limitata* contro lo sniffing — idealmente il traffico va solo sulla porta del destinatario, **ma se lo switch non trova un MAC nella CAM manda i pacchetti in broadcast**.

Il **MAC flooding** sfrutta esattamente questo: l'attaccante **inonda lo switch di MAC sorgente falsi** (`flood of fake MACs`) finché la CAM (di dimensione finita, es. 6 righe nell'esempio) **si riempie**. A quel punto lo switch non ha più spazio per le associazioni legittime e, non trovandole, ripiega sul broadcast.

> **Il MAC flooding costringe lo switch a comportarsi come un hub.** Da quel momento l'attaccante vede *tutto* il traffico del segmento, e lo sniffing (§2.2) torna possibile anche su una rete commutata.

- **Threat model — attaccante**: trasforma una rete switch (che lo isolava) in un mezzo condiviso; obiettivo = sniffing di massa.
- **Threat model — difensore**: *port security* sugli switch gestiti (limitare il numero di MAC per porta), 802.1X.

### 2.5 Wireless key recovery (→ è la crittografia di S14 vista "da rotta")

Quattro generazioni di protezione Wi-Fi, ciascuna nata per riparare la precedente e ciascuna poi bucata. È la parte più densa di dettagli quiz-abili del modulo.

**WEP (Wired Equivalent Privacy)**
- chiave **simmetrica precondivisa**;
- **stream cipher RC4**, con una **falla di progettazione**: è possibile **recuperare la chiave** se si raccoglie sufficiente testo cifrato prodotto con la stessa chiave;
- la chiave è "randomizzata" tramite **XOR con un IV (Initialization Vector) piccolo, 24 bit**;
- generando abbastanza traffico, **l'IV si ripete** → e con la ripetizione dell'IV la protezione crolla.

**WPA (Wi-Fi Protected Access)**
- una **patch intermedia** durante il lancio di WPA2;
- sostituisce l'IV con **TKIP (128 bit)**;
- **modalità personale** con **chiave precondivisa** → *nessuna segretezza in avanti* (no forward secrecy): qualsiasi utente che conosce la chiave può decifrare **tutti** i pacchetti;
- **modalità aziendale** con **autenticazione utente su canale protetto**.

**WPA2**
- a lungo considerato **essenzialmente sicuro**;
- grave vulnerabilità nel **2017: KRACK** (Key Reinstallation Attacks) —
  - Android e Linux possono essere indotti a (re)installare una **chiave di crittografia completamente a zero**;
  - su altri dispositivi è comunque possibile decrittografare un gran numero di pacchetti;
  - i pacchetti possono contenere **credenziali utente con validità a livello aziendale**;
- **PSK corta** se si usa **WPS**.

**WPA3**
- vari miglioramenti a garanzia della **scelta di cifrari robusti**;
- sostituisce la PSK con **SAE (Simultaneous Authentication of Equals)**, che usa un handshake detto **Dragonfly**;
- vulnerabile ad **attacchi Dragonblood**:
  - **tipo 1**: sfrutta la **retrocompatibilità con WPA2** → attacco **MITM per forzare un downgrade**;
  - **tipo 2**: sfrutta un'**implementazione non corretta** di alcuni passaggi crittografici → consente **password partitioning**;
- i dispositivi sono **aggiornabili**.

- **Threat model — attaccante**: recuperata la chiave, entra nella "rete fidata" e da lì fa sniffing (§2.2) e attacchi attivi *dall'interno*. "Il recupero di una chiave consente di impersonare la vittima" (definizione di §2).
- **Threat model — difensore**: usare WPA3 aggiornato, PSK lunghe, disabilitare WPS, modalità *enterprise* con 802.1X.
- **Visione (ponte con S14)**: qui vedi la crittografia *da dove rompe* — IV troppo corto e riusato, stream cipher con chiave riusata, downgrade. In **S14 (Crittografia)** vedrai *perché* uno stream cipher che riusa il keystream è fatale e cosa rende robusto un cifrario; in **S15 (gpg/gestione chiavi)** vedrai la gestione delle chiavi che qui, se fatta male (PSK condivisa, no forward secrecy), è il punto debole.

---

## Parte 3 — Attacchi attivi

**Definizione (dal PDF)**: gli attacchi attivi **minacciano l'integrità, l'autenticità o la disponibilità** di reti e sistemi. **Spoofing e hijacking** sono spesso un *passaggio preliminare* per un attacco più impattante, ad esempio: rubare una rete per originare spam e sparire; fingere un'identità di rete per rubare credenziali; **dirottare il traffico per fare sniffing**. Il **Denial of Service (DoS)** rende inaccessibile un servizio — a volte come passaggio intermedio, a volte come obiettivo principale.

- **Distinzione spoofing vs hijacking** (utile a tenere ordinati i termini): **spoofing** = *falsificare un'identità* (assumere un MAC/IP/nome altrui); **hijacking** = *dirottare/impossessarsi* di un flusso o di una rotta già esistente. Lo spoofing è spesso il *mezzo*, l'hijacking l'*effetto*.

Gli attacchi attivi si distribuiscono su tutti i layer. Li seguo dal basso verso l'alto.

### 3.1 Link layer

#### 3.1.1 MAC spoofing
- **assumere l'identità di un dispositivo a livello di indirizzo fisico** (mettersi il MAC di un altro);
- **molto efficace** per **bypassare le ACL** (liste di controllo accessi basate su MAC) e per **ottenere tutto il traffico destinato alla vittima**;
- **limitato alla LAN**;
- **tecnicamente facile da mitigare con 802.1x**, ma *organizzativamente complesso* → **raro che lo si faccia**.

#### 3.1.2 ARP poisoning (ARP cache poisoning)
Sfrutta il difetto di §1.6 (ARP non autenticato + caching opportunistico). Obiettivo: **convincere un host — specialmente il gateway — che l'IP di una vittima è associato al MAC dell'attaccante**.

- Meccanismo: l'attaccante invia **gratuitous ARP replies** non richieste — "*l'IP del gateway è al MAC dell'attaccante*". Gli host mettono in cache l'associazione avvelenata.
- Effetto: gli host usano la **cache "avvelenata"** e **mandano sul cavo all'attaccante i pacchetti destinati all'IP del gateway**. L'attaccante si è inserito **in mezzo** (man-in-the-middle) tra vittima e gateway.

- **Threat model — attaccante**: da qui parte lo sniffing di §2.2 e la manipolazione del traffico; è la via classica per un MITM in LAN.
- **Threat model — difensore**: *Dynamic ARP Inspection* sugli switch gestiti, tabelle ARP statiche per host critici, 802.1X, segmentazione (l'attacco è confinato alla LAN, §1.5).

#### 3.1.3 Coppia da non confondere: MAC flooding vs ARP poisoning
Entrambi sono di livello 2 ed entrambi *abilitano lo sniffing*, ma il meccanismo e la portata sono diversi:

| | **MAC flooding** | **ARP poisoning** |
|---|---|---|
| Bersaglio | la **CAM dello switch** | la **cache ARP degli host** (spesso il gateway) |
| Meccanismo | saturare la tabella con MAC falsi | inviare ARP reply false (gratuitous) |
| Effetto | switch → hub: vedo **tutto** il segmento (sniffing di massa, indiscriminato) | reindirizzo a me un **flusso specifico** (MITM mirato vittima↔gateway) |
| Selettività | indiscriminato | mirato |

### 3.2 Network layer

#### 3.2.1 IP spoofing
- **assumere l'indirizzo IP di una vittima**;
- **efficace per dirottare il traffico solo su LAN**. Perché solo su LAN? Perché **su Internet il routing invierà le risposte agli indirizzi mimati**: l'attaccante *manda* pacchetti con IP sorgente falso ma **non può ricevere** le risposte (tornano al vero proprietario dell'IP). Le risposte che arrivano a un IP-vittima non coinvolto sono il fenomeno del **backscatter**.

#### 3.2.2 IP hijacking (BGP hijacking)
- i **router si scambiano informazioni** su come raggiungere le destinazioni (routing inter-dominio);
- **BGP non è autenticato!** — chiunque annunci una rotta viene, in linea di principio, creduto;
- **estende la portata dello spoofing IP su scala globale**: non più confinato alla LAN, ma capace di dirottare interi blocchi di indirizzi in tutta Internet.

Entrambi (IP spoofing e IP hijacking) sono utili per **bypassare le ACL** e per **dirottare le connessioni dopo l'autenticazione** (il "vedere più avanti" del PDF → l'idea del session hijacking di §3.3).

#### 3.2.3 Coppia da non confondere: IP spoofing vs IP hijacking
| | **IP spoofing** | **IP hijacking (BGP)** |
|---|---|---|
| Cosa falsifico | l'**IP sorgente** dei miei pacchetti | le **rotte** annunciate tra router |
| Portata | **LAN** (su Internet le risposte non mi tornano → backscatter) | **globale** (dirotto blocchi di IP in tutta Internet) |
| Difetto sfruttato | nessuna verifica dell'IP sorgente | **BGP non autenticato** |

#### 3.2.4 Il caso famoso: YouTube & Pakistan Telecom (2008)
Esempio reale di **BGP hijacking**, dalla presentazione Pilosov & Kapela a DEFCON16. YouTube annuncia i suoi prefissi (tra cui un `/22` = `208.65.152.0/22`). Il governo pakistano decide di **bloccare** YouTube; Pakistan Telecom annuncia internamente una rotta **più specifica** (`208.65.153.0/24`) verso `null0` (l'interfaccia che scarta) per farlo internamente. Per errore, questa rotta **fuoriesce** (redistribuita da statico → BGP → verso l'upstream PCCW) e si propaga a tutti: essendo *più specifica* del `/22` di YouTube, **la maggior parte di Internet inizia a mandare il traffico YouTube verso il Pakistan**, dove viene scartato. YouTube reagisce annunciando rotte ancora più specifiche (`/24` e due `/25`); PCCW stacca il peering di Pakistan Telecom dopo due ore; in 3-5 minuti la tabella BGP globale torna pulita.

- **Lezione**: mostra *concretamente* che (a) BGP crede a chi annuncia, (b) vince la **rotta più specifica** (prefisso più lungo), (c) un errore locale può diventare un blackout globale. È l'illustrazione del perché serve autenticazione del routing (S13).

### 3.3 Layer di trasporto e applicazione

Se il dirottamento IP serve a **impossessarsi di una connessione dopo un'autenticazione**, devono essere coinvolti i livelli superiori:

- **UDP** è **privo di connessione** → **molto facile** da dirottare (non c'è stato da indovinare);
- **TCP** invece **perderà la connessione se l'attaccante non usa i numeri di sequenza corretti** per la finestra scorrevole → più difficile;
- a livello **applicazione**, spesso i protocolli usano **identificatori di sessione** come i **cookie HTTP**.

In tutti i casi l'attaccante ha **due opzioni**:
1. **indovinare** (forza bruta — spesso molto difficile, es. i sequence number TCP);
2. **sfruttare lo sniffing** (facile *se è già sul percorso dei dati* — ecco di nuovo la sinergia passivo+attivo: prima si mette in mezzo con ARP poisoning, poi sniffa il sequence number / il cookie, poi dirotta).

- **Coppia da non confondere: UDP vs TCP hijacking** — UDP è facile *perché* stateless (niente da indovinare); TCP è difficile *perché* stateful (i sequence number della sliding window vanno azzeccati). Non è che TCP sia "più sicuro per progetto crittografico": è solo che il suo stato alza la barriera del brute force.

### 3.4 (D)DoS — Denial of Service

- **Qualsiasi attacco di dirottamento può causare un errore mirato**: a livello di trasporto, **inviare un SN (sequence number) errato o un reset (RST) esplicito interrompe una connessione TCP**.
- **DDoS (Distributed DoS)**: **molti host coordinano gli sforzi** per saturare la capacità di rete o le risorse di calcolo della vittima. Le **botnet** sono insiemi di **computer zombie** che lanciano DDoS quando istruiti da un **Command & Control (C&C)**. Esempi di botnet IoT: **Mirai, Bashlite**.
- **Un controllo degli accessi impreciso sull'infrastruttura può peggiorare le cose**: amplificando l'effetto, nascondendo l'origine — esempio: **attacchi di amplificazione DNS** (piccola query con IP sorgente spoofato → risposta grande verso la vittima).

- **Threat model — difensore**: rate limiting, anti-DDoS a monte, chiudere i resolver DNS aperti (contro l'amplificazione), controllo accessi preciso sull'infrastruttura.

### 3.5 Attacchi ai protocolli ausiliari: DNS

Il DNS è "ausiliario" ma onnipresente (traduce nomi in IP), e come ARP/IP/BGP è **non autenticato**. Il PDF ne cataloga quattro abusi, facili da confondere: teniamoli separati.

#### 3.5.1 DNS tunnelling (esfiltrazione)
- **Query e risposte DNS possono contenere dati**;
- utilizzabile per **esfiltrare dati** da un computer infettato, o per **mettere in contatto un bot con il C&C** (canale nascosto: il traffico DNS è quasi sempre lasciato uscire dai firewall).
- **Nota**: qui il DNS non è "attaccato" — è *abusato come canale*. È un uso *offensivo* del DNS, non una sua falsificazione.

#### 3.5.2 DNS hijacking
- un **server DNS malevolo** fornisce in risposta **l'IP dell'attaccante** quando la vittima chiede di risolvere un nome legittimo;
- il DNS si presta perché **non è autenticato**, è **distribuito**, ha **molti livelli di caching**;
- la **falsificazione arbitraria è difficile** (per via del caching e della distribuzione) **ma**: si può fare con un attacco *combinato* (→ pharming), oppure i **server legittimi possono essere attaccati e portati ad agire in modo malevolo**.

#### 3.5.3 DNS spoofing
- caso concreto: la vittima chiede `www.amazon.com?`; nella risposta *normale* riceve l'IP vero (`207.171.166.48` del web server Amazon);
- nella **risposta falsificata** un **rogue name server** restituisce l'indirizzo del **cracker** → il browser mostra una pagina Amazon *identica* servita dal **web server dell'attaccante**.
- L'utente non si accorge di nulla: URL corretto nella barra, pagina identica, IP sbagliato sotto.

#### 3.5.4 DNS spoofing (pharming) — l'attacco combinato
Risponde alla domanda "*ma non è difficile falsificare una risposta DNS?*" mostrando come aggirare la difficoltà **non falsificando il DNS in transito, ma riprogrammando chi fa le domande**:

1. l'utente **visita una pagina HTML** (consapevolmente o no);
2. la pagina **contiene uno script**;
3. lo script, **usando la password di default del router domestico**, **riprogramma il server DNS** configurato sul router;
4. **da quel momento ogni risoluzione di nomi sarà eseguita dal name server dell'attaccante**.

- **Perché "combinato"**: mette insieme web (pagina+script), debolezza di configurazione (password di default), e DNS. Non rompe la crittografia di nulla: sfrutta l'anello umano/gestionale più debole.
- **Threat model — attaccante**: *persistenza* — non deve più intercettare nulla in tempo reale, ha spostato la fiducia sul proprio name server.
- **Threat model — difensore**: cambiare le password di default (!), **DNSSEC** (autentica le risposte DNS), DoH/DoT (DNS cifrato), aggiornare i router.

#### 3.5.5 Le quattro varianti DNS a colpo d'occhio (coppia/quartetto da non confondere)
| Attacco | Cosa fa | Il DNS è… |
|---|---|---|
| **Tunnelling** | usa query/risposte come *canale nascosto* per esfiltrare/C&C | **abusato come veicolo** (non falsificato) |
| **Hijacking** | un DNS malevolo dà l'IP dell'attaccante per un nome legittimo | **sostituito/compromesso** (il server risolutore mente) |
| **Spoofing** | risposta falsificata → il nome giusto punta all'IP dell'attaccante | **falsificato nella risposta** |
| **Pharming** | riprogramma il resolver del router (via script + password default) → tutte le future risoluzioni passano dall'attaccante | **dirottato alla fonte, in modo persistente** |

---

## Parte 4 — Il threat model del modulo, in tabella

Vista d'insieme attaccante/difensore per layer (sintesi di tutto il modulo — utile come ripasso finale):

| Layer | Attacco passivo | Attacco attivo | Proprietà colpita | Difesa (→ S13/S14) |
|---|---|---|---|---|
| **Data link** | sniffing (dopo MAC flooding) | MAC spoofing, ARP poisoning | riservatezza, autenticità | 802.1X, 802.1AE/MACsec, VLAN, port security, DAI |
| **Rete (IP)** | — | IP spoofing, BGP hijacking | autenticità, integrità | IPsec, autenticazione del routing |
| **Trasporto** | — | TCP/UDP hijacking, RST injection, DoS | integrità, disponibilità | TLS, anti-DDoS |
| **Applicazione** | sniffing di credenziali/cookie | session hijacking (cookie), DNS spoofing/hijacking/pharming, DNS tunnelling, DNS amplification | riservatezza, autenticità, disponibilità | TLS/HTTPS, DNSSEC, auth applicativa, hardening config |
| **Wireless (trasversale)** | sniffing dell'etere, wireless key recovery (WEP/WPA/WPA2/WPA3) | (da chiave recuperata: tutto il resto) | riservatezza → poi tutto | WPA3 aggiornato, PSK lunga, no WPS, enterprise+802.1X |

**Filo conduttore**: quasi ogni attacco sfrutta l'**assenza di autenticazione** di un protocollo fondamentale (ARP, IP, BGP, DNS) o l'**assenza/debolezza di cifratura** (Wi-Fi difettoso, traffico in chiaro). Le contromisure di S13 *aggiungono* proprio queste due cose — autenticazione e cifratura — a un layer alla volta.

---

## Connessioni con altri moduli (specifiche)

- **← S1 (Enumerazione)**: la sezione *Scanning* di questo modulo **è** il LAB di S1 — gli stessi comandi `nmap -sP` (host discovery) e `nmap -A` (fingerprinting versioni/OS) che hai eseguito lì. S12 li ricolloca come "attacco passivo / prima fase della kill chain".
- **← S5 (Firewall/ACL)**: MAC spoofing e IP spoofing sono descritti come modi per **"bypassare le ACL"**. Quelle ACL sono le regole `iptables`/`nft` di S5 basate su indirizzo sorgente: lo spoofing dell'IP sorgente vanifica una regola `-s <ip>` che si fida dell'IP mittente. Il firewall che filtra `-i <interfaccia>` + coerenza subnet/interfaccia è la contromisura all'IP spoofing.
- **← S10 (NIDS/Suricata/Wireshark)**: lo **sniffing** qui descritto è l'atto che produce i `.pcap` che in S10 analizzi con Wireshark; il **port scan**, il **DDoS** e l'**ARP** che hai cercato nelle simulazioni NIDS sono esattamente gli attacchi di questo modulo *visti dal lato rilevamento*. S12 li spiega dal lato attaccante, S10 dal lato difensore/analista.
- **→ S13 (Protezione delle comunicazioni + OpenSSL/TLS)**: è il **seguito diretto**. La sezione "Contromisure: canali sicuri" annunciata (in grigio) nell'outline di S12 — VLAN al data-link, IPsec alla rete, TLS al trasporto — è il *corpo* di S13. Ogni attacco di S12 motiva una difesa di S13: DNS spoofing + TCP hijacking + sniffing → **TLS**; ARP poisoning/MAC flooding → **802.1X/VLAN**; BGP hijacking → **autenticazione del routing/IPsec**.
- **→ S14 (Crittografia)**: la sezione *Wireless key recovery* ti mostra la crittografia *da dove si rompe* (IV di 24 bit riusato in WEP, keystream RC4 riusato, downgrade WPA3). S14 spiega il *perché* teorico: cos'è uno stream cipher, perché riusare il keystream è fatale, cosa rende un cifrario robusto. Il "recupero della chiave" che qui *permette di impersonare la vittima* è il problema che S14/S15 affrontano alla radice.
- **→ S15 (gpg / gestione chiavi)**: la debolezza "chiave precondivisa → nessuna forward secrecy" (WPA personale) è un problema di **gestione delle chiavi** — il tema di S15.
- **↔ S2 (Autenticazione)**: il *session hijacking* via cookie HTTP dopo l'autenticazione, e la modalità WPA-enterprise con "autenticazione utente su canale protetto", sono l'anello con S2. Molti attacchi qui mirano precisamente a **scavalcare** un'autenticazione già avvenuta senza rifarla.

---

## Autoverifica — stile quiz teorico (40%)

> Formato dell'esame reale: **vero/falso** e **scelta multipla**, **penalità sulle risposte sbagliate** → se sei incerto e la penalità è significativa, valuta di non rispondere. Prova a rispondere *prima* di guardare la soluzione in fondo agli appunti. Le risposte commentate sono in `appunti_moduloS12_sicurezza_comunicazioni.md`.

**Vero o Falso**

1. Un attacco passivo, per definizione, non modifica i dati in transito.
2. Lo sniffing su una rete basata su switch è impossibile, perché lo switch invia ogni trama solo alla porta del destinatario.
3. Nella consegna indiretta, l'indirizzo IP di destinazione della trama è quello del router del prossimo hop.
4. ARP è un protocollo autenticato: solo il legittimo proprietario di un IP può rispondere a una ARP request.
5. L'IP spoofing è efficace per ricevere le risposte della vittima anche quando attaccante e vittima si trovano su reti diverse attraverso Internet.
6. In WEP, la ripetizione dell'IV (24 bit) contribuisce alla possibilità di recuperare la chiave.
7. BGP autentica gli annunci di rotta, per cui il caso YouTube/Pakistan Telecom fu possibile solo per un bug del software.
8. Il MAC flooding riempie la cache ARP degli host della vittima.
9. Il DNS tunnelling consiste nel falsificare la risposta di un name server per dirottare la vittima su un IP malevolo.
10. La modalità WPA "personale" con chiave precondivisa non fornisce forward secrecy.

**Scelta multipla**

11. Il MAC flooding ha successo perché lo switch, quando un MAC di destinazione non è presente in CAM:
    a) scarta la trama; b) la invia in broadcast su tutte le porte; c) genera una ARP request; d) la reindirizza al gateway.

12. Quale coppia descrive correttamente gli indirizzi della trama in una *consegna diretta*?
    a) L2 = destinatario finale, IP = destinatario finale; b) L2 = router, IP = destinatario finale; c) L2 = router, IP = router; d) L2 = destinatario finale, IP = router.

13. Il pharming (DNS spoofing) illustrato nel modulo ottiene la falsificazione:
    a) rompendo la firma DNSSEC della risposta; b) saturando la CAM dello switch; c) riprogrammando, via script e password di default, il server DNS del router domestico; d) indovinando i sequence number TCP.

14. Perché dirottare una connessione **TCP** è più difficile che dirottare **UDP**?
    a) TCP è cifrato per default; b) UDP non attraversa i router; c) TCP richiede di indovinare i sequence number corretti della finestra scorrevole; d) UDP usa sempre i cookie HTTP.

15. Quale tecnologia, citata nel modello Internet del PDF, protegge la connettività **end-to-end reliable** a livello di trasporto?
    a) 802.1X; b) IPsec; c) SSL/TLS; d) WPA2.

16. WPA3 è vulnerabile a Dragonblood di "tipo 1" perché:
    a) usa RC4; b) sfrutta la retrocompatibilità con WPA2 per forzare un downgrade via MITM; c) espone la CAM dello switch; d) non usa alcun handshake.

17. L'ARP poisoning permette a un attaccante di fare MITM perché:
    a) modifica la tabella di routing BGP; b) convince gli host (spesso il gateway) che l'IP della vittima è al MAC dell'attaccante, tramite gratuitous ARP reply; c) satura la banda con pacchetti zombie; d) cifra il traffico della vittima.

18. Un attacco di **amplificazione DNS** serve tipicamente a:
    a) esfiltrare dati via query DNS; b) autenticare gli annunci BGP; c) potenziare e mascherare l'origine di un DDoS; d) recuperare la chiave WEP.

---

## Riepilogo (la mappa mentale del modulo)

- **Due grandi famiglie**: **passivi** (non toccano i dati → riservatezza/ricognizione: scanning, sniffing, MAC flooding, wireless key recovery) e **attivi** (toccano/iniettano/interrompono → integrità/autenticità/disponibilità: MAC/IP spoofing, ARP/BGP/DNS hijacking, DoS/DDoS).
- **Il filo rosso**: i protocolli fondanti di Internet (ARP, IP, BGP, DNS) sono **non autenticati**, e molta comunicazione viaggia **in chiaro** → l'attaccante sfrutta l'una o l'altra assenza.
- **La sinergia ricorrente**: prima ci si *mette in mezzo* con un attacco attivo (ARP poisoning), poi si *ascolta* con uno passivo (sniffing); prima si *recupera una chiave* (passivo), poi si *impersona* (attivo).
- **La mappa a strati** collega ogni attacco alla sua difesa: data-link → 802.1X/VLAN; rete → IPsec; trasporto → TLS. Le difese sono **S13**; la crittografia sotto WEP/WPA/TLS è **S14**; la gestione chiavi è **S15**.
- **Confine**: questo modulo si ferma agli attacchi (fino al DNS pharming). Le contromisure "canali sicuri" sono annunciate ma non svolte qui — sono il modulo successivo.
