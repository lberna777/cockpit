# Lezione — Modulo S13: Offensive Net Security + Protezione delle Comunicazioni + OpenSSL/TLS

**Corso**: Lab Sicurezza Informatica T
**Fonti primarie**:
- `SLIDE TEORIA/SICINF/05_05__va_pt.pdf` (Prandini, "Offensive security I — Reconnaissance & Assessment", 53 slide)
- `SLIDE TEORIA/SICINF/Protezione_delle_comunicazioni_15-20_maggio.pdf` (Prandini, 78 slide)
- `SLIDE TEORIA/SICINF/Altri_esercizi_configurazione_servizi_con_TLS_20_maggio.pdf` (Melis/Prandini, 17 slide)
- `SLIDE LAB/SICINF/LAB_Offensive_network_security.pdf` (Prandini/Melis, sniffing/spoofing/DoS)
- `SLIDE LAB/SICINF/Comandi_offensive_net_sec.html` (comandi passo-passo del lab)
- `SLIDE LAB/SICINF/LAB_OpenSSL_20_maggio.pdf` (Melis/Prandini, 28 slide)

**Tipo**: modulo misto — teoria (offensive security + protezione delle comunicazioni) e tre laboratori (offensive net sec, OpenSSL, TLS). Rilevante sia per il **quiz teorico (40%)** — è pieno di distinzioni vero/falso e di nomi di attacchi — sia per la **prova pratica** (comandi `openssl`, `nmap`, `ettercap`, `hping3`, configurazione `nginx`).

---

## Dove si colloca questo modulo, e i suoi due threat model

Questo è un modulo "a due facce", ed è essenziale tenerle distinte per non confondersi all'esame.

1. **Faccia offensiva** — *Offensive net security*: ci si mette nei panni dell'attaccante per **verificare** l'esposizione di un sistema. È la parte iniziale della *kill chain* (reconnaissance ed enumeration) più il passaggio da *Vulnerability Assessment* a *Penetration Testing*. Threat model: l'attaccante parte da zero conoscenza e accumula informazioni finché non trova una via d'ingresso; il "difensore" qui è chi conduce il test in modo autorizzato (**mai** su risorse non proprie senza permesso) per scoprire i buchi prima dei veri avversari.

2. **Faccia difensiva** — *Protezione delle comunicazioni*: dato che i protocolli fondamentali di Internet (ARP, IP, TCP, DNS) sono nati **senza autenticazione né cifratura**, si costruiscono **canali sicuri** come strato aggiuntivo, layer per layer (data link → VLAN, network → IPSec, transport → TLS), più strumenti d'uso quotidiano (TOR, SSH). Threat model: l'attaccante è un *man-in-the-middle* che ascolta o altera il traffico; il difensore aggiunge riservatezza, integrità e autenticità dove il protocollo nudo non le offre.

**Confine con i moduli vicini — leggere prima di tutto il resto:**
- **S1 (Offensive Security & Enumerazione)**: ha già trattato in dettaglio Google dorking, OSINT, DNS/subdomain enumeration, `nmap`, evasione, vulnerability scanner. Qui li **richiamo** per completezza (il PDF `va_pt` li ripresenta) ma non li rispiego riga per riga: il valore aggiunto di S13 è la **distinzione VA→PT**, le **metodologie di PT** e l'**architettura di OpenVAS**.
- **S12 (Sicurezza delle comunicazioni)**: ha già trattato in teoria gli *attacchi* al traffico (sniffing, ARP/DNS spoofing, hijacking, DoS). Il **lab offensive net sec** di S13 è la loro **controparte pratica** (li eseguo con `ettercap`/`hping3`), e la parte "Protezione" di S13 è la **risposta difensiva** che S12 lasciava annunciata ma non svolta ("contromisure: canali sicuri", in grigio nelle slide di S12).
- **S14 (Crittografia)**: ha fornito i mattoni (simmetrico/asimmetrico, RSA, hash, firma digitale, PKI come concetto). Qui li **uso in pratica** con `openssl`, senza rispiegare *come* funziona RSA — solo *come si invoca*.

---

# PARTE 1 — OFFENSIVE NET SECURITY

## 1. Il ciclo di vita della vulnerabilità

Le vulnerabilità si annidano a ogni livello dello stack (applicazioni, sistema operativo, hardware, interfacce di I/O). Alcuni concetti di temporizzazione, importanti per il quiz:

- **Vulnerabilità zero-day**: una vulnerabilità **sconosciuta** a chi dovrebbe mitigarla.
- **Finestra di opportunità**: il tempo tra quando il primo exploit diventa attivo e quando il fornitore rilascia (e si applica) una patch. Dato citato: nel 2005 durava in media 54 giorni, nel 2014 quasi 12 mesi.
- **Attacco zero-day**: un attacco che avviene *dentro* la finestra di opportunità.
- **Meccanismo**: gli attacchi si **intensificano dopo** la pubblicazione della vulnerabilità, non prima — appena esce una CVE, tipicamente entro **15 minuti** iniziano scansioni massive di Internet. Contro-intuitivo ma cruciale: rendere pubblica una vulnerabilità aumenta gli attacchi nel breve, ma è l'unico modo per far partire le patch.
- **Visione**: esiste un intero ecosistema di *responsible disclosure* — database pubblici (**CVE** di MITRE, **NVD** del NIST, exploit-db, cvedetails) e programmi di **bug bounty** (Zerodium, Google Project Zero) che pagano chi trova bug. La stessa informazione serve al difensore per correggere e all'attaccante per colpire.

## 2. Offensive security: perché e con quali cautele

Porsi nel ruolo dell'attaccante serve a tre cose: **verificare** l'esistenza di vulnerabilità, **stimare** l'impatto reale di un attacco, **testare** l'efficacia delle contromisure. Il processo si modella con la **kill chain** (la catena di passi di un attacco; il primo anello è *Reconnaissance*, tattica `TA0043` di MITRE ATT&CK).

- **Regola deontologica assoluta**: MAI usare queste tecniche su risorse non proprie senza permesso. "Permesso" è un termine ampio — anche in buona fede si rischiano grattacapi legali, effetti imprevisti sul bersaglio e danni alle **reti attraversate** per raggiungerlo.
- **Compromesso di fondo**: velocità *o* precisione? Ricerca esaustiva delle vulnerabilità *o* verifica di quanto i sistemi di rilevazione (IDS/IPS) se ne accorgono? Non si può ottimizzare tutto insieme.

## 3. VA → PT — la distinzione che l'esame ama

Questa è la distinzione-chiave della Parte 1, candidata perfetta a una domanda vero/falso.

- **Vulnerability Assessment (VA)**: trova **solo vulnerabilità note** e **non procede oltre**. Non sfrutta i buchi, quindi non vede la "vista interna" che si aprirebbe superandone uno; non considera la specificità del sistema (produce anche **falsi positivi**, es. un servizio che dichiara una versione vulnerabile ma è stato patchato). È automatizzabile.
- **Penetration Testing (PT)**: un **tester umano** avanza fin dove può, **sfruttando** le vulnerabilità con veri *exploit*. Più realistico, report più dettagliato, ma **RISCHIOSO** (può danneggiare il bersaglio).
- In una frase: *il VA fotografa i buchi noti; il PT li attraversa per vedere dove portano.*

**Punti di partenza del PT:**
- **Regole d'ingaggio**: mappatura, prioritizzazione, tracciamento dei confini del target.
- **Postura e visibilità** (assi "conoscenza dell'attaccante sul target" × "conoscenza del target sull'attacco"): dal **Blind/Double Blind** (l'attaccante sa poco, il target non sa di essere testato — sembra realistico ma fa perdere tempo al tester esperto) al **Grey Box / Double Grey Box / Tandem / Reversal** (gradi crescenti di conoscenza condivisa). Nota di Prandini: gli attacchi "ciechi" sembrano realistici ma spesso è meglio spendere il tempo del tester sui dettagli davvero nascosti.
- **Protezione del bersaglio**: dove possibile si testa una **replica**, ma alcuni sistemi sono troppo complessi o troppo critici per rischiare che un dettaglio perso nella copia alteri il test.

**Metodologie di PT** (seguirne una rende il test coerente, ripetibile, misurabile — senza pregiudizi o aneddoti). Da conoscere per nome:
- **OSSTMM** — Open Source Security Testing Methodology Manual (generale, aperta).
- **OWASP** — specifico per applicazioni **web**.
- **PCI DSS** — settore finanziario; la sezione **11.3** riguarda il pentesting.
- **NIST 800-115** — standard ufficiale del governo USA.
- **ISSAF** — completo ma non più sviluppato attivamente.

## 4. Reconnaissance ed Enumeration (richiamo, dettaglio in S1)

> Questa sezione ricalca il PDF `va_pt`, che coincide in gran parte con S1. La riassumo per completezza del quiz; per gli esempi di comando approfonditi vedi la lezione S1.

- **Reconnaissance** = raccolta di informazioni utili + estensione del perimetro + preparazione degli strumenti. **Enumeration** = delimitazione del perimetro + verifica puntuale delle risorse.
- **OSINT** (Open Source INTelligence): uso di **qualsiasi fonte pubblica** per profilare un obiettivo (geolocation, domini DNS, range IP, autonomous system, certificati X.509, porte, fingerprinting, username). Legale "sostanzialmente sì", con aree grigie. Strumento-indice: `osintframework.com`.
- **Google Dork**: operatori di ricerca per affinare i risultati. I principali: `site:` (URL indicizzati di un dominio), `filetype:` (estensione), `intitle:`/`inurl:`/`intext:` (parole nel titolo/URL/testo), `cache:` (versione in cache), `allintext:`/`allinurl:`, `link:`, `*` (wildcard). Esempi d'attacco: `allintext:password filetype:log after:2020`, `site:ulisse.unibo.it intitle:index.of id_rsa -id_rsa.pub` (chiavi SSH indicizzate). **Contromisura**: `robots.txt` (`User-agent: *` / `Disallow: /`) — tutto ciò che Google trova è perché è stato indicizzato.
- **DNS enumeration**: i record DNS svelano IP registrati, server applicativi, sottoreti non raggiungibili, alias verso risorse in cloud o domini fidati (foresta Active Directory). Strumenti: lookup di base (`host`, `dig`, `nslookup`; es. `nslookup -type=any google.com`), e con guessing/bruteforce (`dnsenum`, `dnsmap`, `dnsrecon -d DOMAIN`, `fierce`). Aggravanti: *domain transfer* abilitato (plateale), record rimossi ma rimasti in cache (sottile).
- **Subdomain enumeration**: amplia enormemente la superficie d'attacco (sottodomini dimenticati, non aggiornati). **Passiva** (query a dataset noti: SecurityTrails, Shodan, Censys, VirusTotal; wrapper come **amass** di OWASP, subfinder, assetfinder) vs **attiva** (bruteforce DNS, permutation, VHOST probing). **CT abuse**: poiché ogni certificato TLS emesso finisce nei log pubblici di **Certificate Transparency** (RFC 6962), interrogandoli (es. `https://crt.sh/?q=%25.dell.com`) si enumerano i sottodomini che hanno un certificato. Precisazione: un **FQDN** (`miopc.ulisse.com`) è un sottodominio; `internal.accounts.ulisse.com` come *URL* è invece un'applicazione web su una porta di un host, non necessariamente un sottodominio DNS distinto.
- **Enumerazione host/servizi**: individuare i **live host** (ping — ma bloccabile da FW o ignorabile dagli host; `masscan` per scansioni massive; `arping`/sniffing passivo su rete locale) e poi le **porte aperte** (le due fasi possono collassare se si sospetta che gli host ignorino i ping → si sondano direttamente le porte). Tool principe: **nmap** (scansione di range di IP e porte, fingerprinting di OS e versioni). `unicornscan` è un'alternativa con fingerprinting più affidabile, più veloce, e — importante per l'evasione — **non usa lo stack TCP/IP dell'host di origine**, evitando il *reverse fingerprinting*.
- **Evasione**: reconnaissance in modalità anonima (TOR, account usa-e-getta, VM sostituite periodicamente); enumerazione *stealth* (temporizzazione configurabile, randomizzazione di indirizzi/porte, stack proprio) e adattativa rispetto a FW/IDS/IPS.
- **Postura interna vs esterna**: la recon esterna è più fedele all'attaccante reale ma potrebbe non trovare la via d'ingresso; auto-attaccarsi *dall'interno* scavalca NIDS e FW ed è il miglior test per gli **HIDS**.
- **Vulnerability scanner completi**: **Nessus** (commerciale, Tenable) e il suo equivalente open-source **OpenVAS** (nato nel 2005 come fork quando Nessus passò a licenza proprietaria, oggi **Greenbone Community Edition**). Il valore fondamentale è il **feed** di *Network Vulnerability Tests* (descrizione + piattaforme colpite + processo di verifica, aggiornato ogni giorno), collegato alla documentazione (CVE).

## 5. Il lab offensive: sniffing, spoofing e DoS in pratica

Questo è il laboratorio con `docker-compose`: tre container sulla stessa rete *self-named bridge* — **A (Alice, 10.9.0.5)**, **B (Bob, 10.9.0.6)** e **M (MITM, 10.9.0.105)**. Wireshark si lancia **sulla VM host**, non nei container, in ascolto sull'interfaccia `br-<esadecimale>`. Ci si connette a un container con `sudo docker exec -it NOME /bin/bash`. Sull'attaccante va abilitato l'ip forwarding (`echo 1 >/proc/sys/net/ipv4/ip_forward`), altrimenti il MITM interrompe il traffico invece di inoltrarlo.

### 5.1 ARP poisoning (MITM)

L'**ARP spoofing/poisoning** è la tecnica principe per un MITM in una switched LAN. Si osservano le tabelle ARP con `arp -n`, si può cancellare una entry con `arp -d HOST`.

```bash
ettercap -T -M arp /// ///                 # poisoning di TUTTI gli host (di fatto un DoS)
ettercap -T -M arp /10.9.0.6// /10.9.0.5//  # poisoning MIRATO: solo Alice e Bob
```

- **Meccanismo**: `ettercap` inonda gli host di risposte ARP fasulle che associano il MAC dell'attaccante agli IP delle vittime; da quel momento Alice e Bob mandano i pacchetti destinati l'uno all'altro a M, che li inoltra (avendo ip_forward attivo) restando in mezzo. La versione `/// ///` avvelena tutti → tutto il traffico converge su M: utile solo in laboratorio, di fatto un DoS.
- **Visione**: si verifica l'attacco guardando le tabelle ARP alterate sulle vittime e i pacchetti "che non dovrebbero" arrivare a M in Wireshark. Per simulare connessioni si usano `nc -vnlp 8080` (Bob in ascolto) + `nc 10.9.0.6 8080` (Alice), oppure `iperf -u -s`/`iperf -u -c` per UDP.

### 5.2 DHCP spoofing

```bash
# Bob: si toglie l'IP per forzare una nuova richiesta
ip addr del 10.9.0.6/24 dev eth0
# MITM: inonda la rete di offerte DHCP con gateway/DNS a piacere
ettercap -T -M dhcp:10.9.0.20-60/255.255.255.0/8.8.8.8
# Bob: chiede una configurazione
dhclient eth0
```

- **Meccanismo**: "battere" il DHCP legittimo significa **rispondere più in fretta** con un'offerta che impone all'attaccante come gateway (o un DNS malevolo). Inondando di *request* si può anche saturare il server DHCP legittimo (DoS). La sintassi `dhcp:range/netmask/DNS` dice a ettercap quali IP offrire, con quale maschera e quale DNS annunciare.
- **Visione**: dopo l'attacco la configurazione di rete di Bob non è più l'originale; per ripristinarla il modo più semplice è fermare `docker-compose` (Ctrl-C) e rilanciarlo.

### 5.3 DoS — SYN flood

```bash
# baseline: banda disponibile senza attacco
iperf -s              # Bob (server)
iperf -c 10.9.0.6     # Alice (client)
# attacco dal MITM
hping3 -c 10000 -d 120 -S -w 64 -p 21 --flood --rand-source 10.9.0.6
```

- **Meccanismo dei flag** (`hping3`): `-c 10000` numero di pacchetti; `-d 120` dimensione di ciascuno; `-S` invia solo pacchetti **SYN**; `-w 64` TCP window size; `-p 21` porta di destinazione; `--flood` invia il più veloce possibile **senza guardare le risposte**; `--rand-source` usa IP sorgente casuali (una "connessione" per ogni IP, e nasconde l'origine). Il SYN flood apre una valanga di mezze connessioni TCP che saturano la vittima.
- **Visione**: si rimisura la banda con `iperf` sotto attacco e si osserva il degrado. `hping3` supporta anche LAND e SMURF attack.

---

# PARTE 2 — PROTEZIONE DELLE COMUNICAZIONI (canali sicuri)

L'idea unificante: per ogni layer esiste una tecnologia che aggiunge sicurezza dove il protocollo nudo non ne ha. **Data link → VLAN**; **network → IPSec**; **transport → TLS**; e come strumenti d'uso comune **TOR** e **SSH**. Più il caso applicativo di **HTTPS** con i suoi attacchi e contromisure.

## 6. SSL/TLS — architettura

SSL è stato progettato come uno **strato di protocolli indipendente**, collocato **logicamente tra il livello di trasporto e le applicazioni**. Vantaggio: non richiede di modificare i protocolli di rete; l'implementazione è una **libreria** (SSLeay, poi OpenSSL) e per rendere un'applicazione capace di SSL basta inserire le chiamate a quelle funzioni.

**Sessione vs connessione** (distinzione da tenere ferma):
- Due entità che colloquiano in SSL devono avere aperto una **sessione**.
- Una singola sessione può includere **molte connessioni** sicure contemporanee, e due entità possono avere più sessioni attive insieme. La sessione porta i parametri crittografici negoziati; le connessioni li riutilizzano.

**Due sotto-protocolli:**
- **Handshake Protocol** — la parte più complessa. Consente a server e client di **autenticarsi reciprocamente** (challenge-response su crittografia asimmetrica e **certificati X.509** — nel web è comune che *solo il server* provi la propria identità), **negozia** algoritmi e chiavi per cifratura e integrità, **prima** che qualsiasi dato sia trasmesso. Progettato per limitare il carico: usa un **caching delle sessioni** (numero di sessione) così che, se la comunicazione si interrompe, i parametri si recuperano senza rinegoziarli.
- **Record Protocol** (SSLRP) — impacchetta i dati in **record** e si occupa di cifratura/decifrazione dei record conformemente a quanto negoziato.

**SSL → TLS** (distinzione classica da quiz): **TLS è l'evoluzione di SSL**, con lo **stesso formato di record**; definito in **RFC 5246 (v1.2)** e **8446 (v1.3)**. Simile a SSLv3 ma diverso in: numero di versione, codice di autenticazione del messaggio, funzione pseudocasuale, codici di avviso, suite di cifratura, tipi di certificato client, `certificate_verify`/messaggio *finished*, calcoli crittografici, padding. In pratica oggi "SSL" e "TLS" si usano come sinonimi, ma **SSL è la vecchia famiglia (insicura), TLS la nuova**.

**Confronto SSL/TLS vs IPSec** (per il quiz):
- SSL/TLS: **specifico di un dominio applicativo**, semplice e realmente standard.
- IPSec: **generale e trasparente alle applicazioni**, implementato nello stack TCP/IP del SO, con varianti che ne rendono difficile l'interoperabilità.
- Soluzioni **ibride**: varianti di SSL per trasportare pacchetti IP (analogo al tunnel mode di IPSec) ma in **user space**, indipendenti dal SO — es. **OpenVPN**.

## 7. HTTPS — attacchi al caso applicativo e contromisure

HTTPS = HTTP over SSL/TLS. Blocca gli attacchi al traffico, ma esistono modi per aggirarlo. Il browser verifica la prova del server (il certificato) tramite il proprio **certificate store** e le **Trusted CA**.

- **Occultamento della barra degli indirizzi**: nascondere/falsificare la URL mostrata (vecchio: JS/ActiveX; nuovo: auto-hiding della barra nei browser mobili → *inception bar*).
- **Attacchi omografici (IDN)**: gli **International Domain Names** ammettono alfabeti non latini, ma il DNS supporta solo il latino base → conversione in **punycode** (`點看 → xn--c1yn36f`). Problema: esistono caratteri **omografi** (es. una "а" cirillica identica alla "a" latina): `pаypal.com → xn--pypal-4ve.com`. Nulla impedisce di registrare quel dominio e ottenerne un **certificato X.509 legittimo** (HTTPS funziona regolarmente!). Contromisura lato browser: **mostrare il punycode** invece del font internazionale ingannevole.
- **Iniezione di CA nel certificate store / fake certificate**: il modo più semplice di impersonare un sito è **falsificare il certificato**; raro ma gravissimo se si compromette una **CA**. Contromisure:
  - **HPKP** (HTTP Public Key Pinning, RFC 7469): limita quali chiavi (root/intermediate/end-entity) sono associabili a un dominio, dichiarato nell'header `Public-Key-Pins`. **Deprecato** da Google Chrome.
  - **Certificate Transparency (CT, RFC 6962)**: framework aperto che rende **impossibile (o molto difficile)** a una CA emettere un certificato senza che sia **visibile** al proprietario del dominio; sistema pubblico di auditing/monitoraggio (è lo stesso meccanismo che l'attaccante *abusa* per la subdomain enumeration — la stessa trasparenza serve difesa e offesa).
- **Stripping**: pagine HTTP che poi inviano dati sensibili via HTTPS possono essere **modificate da un MITM** (che declassa la connessione a HTTP in chiaro). Mitigazione: **HSTS** (HTTP Strict Transport Security, RFC 6797) — una policy nell'header di risposta che forza il browser a usare **solo HTTPS**; ma è **inefficace sulla prima richiesta** (il browser non ha ancora visto la policy). Attacco analogo senza equivalente di HSTS: **STARTTLS command injection** (connessioni che partono in chiaro e chiedono l'upgrade; il MITM interferisce o accoda comandi in ordine errato).

## 8. Vulnerabilità di SSL/TLS — il catalogo da quiz

Distinguere **due livelli**: vulnerabilità **di protocollo** (difetti di progettazione) e **di implementazione** (bug nel codice, es. OpenSSL).

**A livello di protocollo:**
- **Crittografia debole**: cifrari con problemi noti (**RC4** — "non abilitatelo!"), IV prevedibili.
- **BEAST** (2011, CVE-2011-3389): "Browser Exploit Against SSL/TLS"; sfrutta il **CBC con IV concatenati**; un MITM recupera header HTTP in chiaro con un *blockwise chosen-boundary attack* + codice JavaScript.
- **Padding Oracle Attacks**: causati dalla sequenza **MAC-then-encrypt**. Famiglia: **Lucky Thirteen** (2013, CVE-2013-0169; side-channel di **timing** sul controllo del MAC durante il padding CBC malformato; basso impatto, mitigato da scelte crittografiche più accorte) e **POODLE** (2014, CVE-2014-3566; un MITM forza il **downgrade** verso **SSLv3**, che usa cifrari deboli — RC4 e CBC vulnerabile a padding oracle; impatto: decifrazione del traffico; **unica mitigazione: disabilitare SSLv3**).
- **Compressione**: **CRIME, TIME, BREACH**.
- **DROWN** (2016, CVE-2016-0800): "Decrypting RSA with Obsolete and Weakened eNcryption"; sfrutta il supporto residuo a **SSLv2** (indebolito dalle restrizioni USA all'export di crittografia → probe che limitano lo spazio di ricerca delle chiavi a **40 bit**). Se un server con una certa chiave privata supporta SSLv2, **tutti** i server che usano quella chiave sono vulnerabili. Impatto: controllo completo, impersonamento del server.

**A livello di implementazione:**
- **Heartbleed** (2014, CVE-2014-0160): implementazione errata della **heartbeat extension** (RFC 6520) in **OpenSSL**. Il heartbeat è uno scambio per tenere viva la connessione: il client manda una stringa **dichiarandone la lunghezza**, il server la restituisce. **Bug**: il server usa la lunghezza *dichiarata* per leggere la propria memoria **senza controllare** che corrisponda alla stringa realmente ricevuta → restituisce anche pezzi di memoria adiacente. Impatto: **leak di materiale sensibile, incluse le chiavi private**. È un difetto di *codice*, non di *protocollo* — da qui l'importanza di aggiornare le librerie.

## 9. IPSec — protezione a livello di rete

**IPSec non è un protocollo singolo**: è un insieme di algoritmi + un framework per negoziarli + specifiche per la gestione delle chiavi. Vantaggi: **trasparente alle applicazioni** e applicabile anche al traffico infrastrutturale (es. messaggi di routing tra router). Standard: RFC 4301 (architettura), 4302 (AH), 4303 (ESP), 7296 (IKEv2).

**Servizi**: controllo dell'accesso, integrità senza connessione, autenticazione dell'origine, rilevazione dei **replay**, riservatezza (con cifrari come 3DES, IDEA, CAST, Blowfish; autenticazione con HMAC-MD5/SHA-1; gestione chiavi manuale o automatica via ISAKMP/Oakley).

**Terminologia:**
- **SA (Security Association)**: relazione **unidirezionale** mittente→destinatario, identificata da **SPI (Security Parameter Index) + IP destinazione + identificatore del protocollo di sicurezza**. Due modalità: **Transport** e **Tunnel**.
- **Due protocolli di sicurezza:**
  - **AH (Authentication Header)**: garantisce **autenticazione e integrità** del pacchetto IP e protegge dai replay. Gli **indirizzi vengono autenticati** → le alterazioni del **NAT** sono percepite come violazioni dell'integrità (AH e NAT sono incompatibili!).
  - **ESP (Encapsulating Security Payload)**: offre essenzialmente **riservatezza** (cifratura); opzionalmente anche aut/int, ma in grado minore di AH (ESP non autentica l'header IP esterno).

**Transport vs Tunnel mode** (tabella riassuntiva — molto probabile a quiz):

| | Transport Mode | Tunnel Mode |
|---|---|---|
| **AH** | autentica il payload IP + alcuni campi dell'header | autentica l'intero pacchetto IP **interno** + alcuni campi dell'esterno |
| **ESP** | cifra il **contenuto** del pacchetto | cifra l'**intero pacchetto IP interno** |
| **ESP+auth** | cifra il contenuto, autentica il payload ma **non l'header IP** | cifra e autentica l'intero pacchetto IP interno |

Idea: **Transport mode** protegge il payload lasciando visibile l'header originale (host-to-host); **Tunnel mode** incapsula l'intero pacchetto dentro un nuovo pacchetto (gateway-to-gateway, nasconde la topologia interna).

## 10. VPN e OpenVPN

**VPN** = metodi di trasporto del traffico che sono *virtualmente privati*: **privati** perché garantiscono sicurezza, **virtualmente** perché il traffico passa su reti insicure. Scenari: host-host, host-net, net-net.

**OpenVPN** riproduce in **software user space** i concetti di transport e tunnel mode di IPSec, senza dipendere dal SO. Serve solo un piccolo componente kernel: la creazione di **interfacce di rete virtuali**:
- **tun** (layer 3, punto-punto): i pacchetti inviati a questa interfaccia non vanno a una scheda fisica ma **al processo OpenVPN**, che li incapsula in TLS e li spedisce come payload UDP all'omologo remoto (che decifra, verifica, decapsula ed emette sull'interfaccia). Usata per il **tunnel mode** — connette due reti remote; gli IP delle interfacce tun sono un puro artificio punto-punto, trasparenti alle applicazioni.
- **tap** (layer 2): usata per il **transport mode** associato al **bridging** — fa apparire una macchina remota come **fisicamente parte** della LAN remota (tap0 fa da "cavo", niente IP separato, inoltro layer 2 in un bridge `br0 = tap0 + eth1`).
- L'uso o meno di queste interfacce è deciso da normali entry nella **routing table**.

## 11. Data link security — VLAN

Gli switch gestiscono **Virtual LAN**: segregano il traffico tra subnet diverse anche se condividono l'infrastruttura fisica. Senza VLAN servirebbe un segmento fisico e una porta del router per ogni subnet; con VLAN le subnet possono essere sparse su più segmenti, con anche una sola porta del router e collocazione configurabile dei membri.

- **Classificazione**: **statica/port-based** (l'appartenenza dipende dalla **porta** dello switch; spostare un host = riconfigurare la porta) vs **dinamica** (dipende da **MAC/IP** dell'host, indipendente dalla porta).
- **Tagging 802.1q**: i frame vengono marcati con un tag di VLAN. Le **porte** funzionano in:
  - **access mode**: appartengono a **una sola** VLAN, tagging non necessario (uso tipico: host semplici).
  - **trunk mode**: appartengono a **più** VLAN, tagging **necessario** per distinguerle; possono gestire una **VLAN nativa** per i pacchetti *untagged* + pacchetti tagged delle altre (uso tipico: connessione a router o tra switch).
- **VLAN hopping** (la separazione logica non è robusta come quella fisica):
  - **Switched spoofing**: l'attaccante finge di essere uno switch (via **DTP**) e fa configurare la propria porta come **trunk**, ricevendo tutte le VLAN.
  - **Double tagging**: l'attaccante, sulla VLAN **nativa** del trunk, invia un pacchetto con **due tag annidati** (V2 dentro V1); il primo switch rimuove V1 e inoltra sul trunk, il secondo interpreta V2 e consegna alla vittima. Funziona **solo in andata** (non c'è modo di farsi rispondere).

## 12. Strumenti d'uso comune — SOCKS5, TOR, SSH

### 12.1 SOCKS5 (RFC 1928)

Un **circuit-level gateway**: un proxy che **spezza la connessione a livello di sessione** diventando lui stesso endpoint del traffico (non un intermediario trasparente come un router). Usi: decidere quali connessioni sono ammesse da una rete protetta verso l'esterno; intermediario generico (senza predefinire i protocolli applicativi). Svantaggio: richiede la modifica dello stack del client o la configurazione consapevole delle applicazioni ("socksified client").

### 12.2 TOR (The Onion Router)

Progetto open source (avviato dalla EFF) per connessioni cifrate in cui il legame tra chi fa richieste e il contenuto è **profondamente oscurato**. Un *local proxy* espone un'interfaccia **SOCKS5** ai client locali per farli accedere a TOR.

- **Meccanismo**: il setup del percorso restituisce al client un set di **chiavi AES** condivise con ognuno dei relay attraversati; il messaggio è cifrato **"a cipolla"** (a strati); **ogni relay conosce solo i suoi due vicini** di percorso.
- **Debolezze**: entry ed exit node nello stesso **AS** → correlazione; l'**exit node vede il traffico in chiaro** (ma non l'IP sorgente — attenzione a dati identificativi nel payload!); *bad apple* (un'app insicura che fa IP leak traccia anche quelle sicure dello stesso utente); usare TOR aumenta il sospetto. Contromisure: percorso random per ogni connessione, cifratura applicativa (HTTPS sull'ultimo hop), **bridges** (entry node non elencati nella directory, per non mostrare all'ISP che si usa TOR o aggirarne il blocco).

### 12.3 SSH — amministrazione remota

Nasce per rimpiazzare **TELNET** (nessuna confidenzialità, nessuna autenticazione dell'host, autenticazione utente passiva). Il collegamento tra `ssh` (client) e `sshd` (server) segue: negoziazione dei cifrari → **autenticazione dell'host remoto** (via chiave pubblica) → canale cifrato → negoziazione dei metodi di autenticazione utente → **autenticazione dell'utente**.

- **Host authentication**: serve a non cadere nella trappola di un MITM che catturerebbe la password dell'amministratore. Non c'è un sistema centralizzato (solo supporto non ufficiale a X.509): alla **prima connessione** l'admin verifica *out-of-band* la chiave pubblica dell'host; questa viene salvata in `~/.ssh/known_hosts` per le connessioni successive (autenticazione attiva).
- **User authentication**: **passiva** (username+password, trasmessi però su canale già cifrato) o **attiva** (challenge-response a chiave pubblica: l'utente genera una coppia di chiavi e installa la pubblica sul server). L'identità con cui ci si logga è selezionabile: `ssh remoteserver` usa lo stesso username locale; `ssh root@remoteserver` si presenta come root.
- **Generazione chiavi**:
  ```bash
  ssh-keygen -t rsa -b 2048        # → chiave privata ~/.ssh/id_rsa, pubblica id_rsa.pub
  ssh-copy-id [-i file] user@remote  # installa la pubblica sul remoto
  # oppure manualmente:
  scp .ssh/id_rsa.pub user@remote:
  cat id_rsa.pub >> .ssh/authorized_keys   # sul remoto
  ```
  Il ruolo autenticante della password è sostituito dalla **presenza della chiave privata** sul client → grande cura nei **permessi** di `.ssh` (spesso il passwordless login non funziona perché i permessi sono troppo larghi e `sshd` "non si fida"). La chiave privata può essere protetta con una passphrase (perde il passwordless, ma è più sicuro).
- **Esecuzione remota**: `ssh utente@host` dà un terminale interattivo; aggiungendo un comando (`ssh root@server "grep pattern"`) quel comando viene eseguito sul remoto e i suoi STDIN/STDOUT/STDERR passano cifrati attraverso il canale.

### 12.4 SSH tunnelling — le quattro forme (probabile a quiz)

| Flag | Nome/idea | Effetto |
|---|---|---|
| `-L [bind:]port:host:hostport` | *local forward* ("poor man's VPN") | una porta **locale** viene inoltrata a `host:hostport` visto **dal lato remoto** — rende raggiungibili servizi al di là del gateway. Es: `ssh -L 110:10.0.0.2:110 200.1.1.1` |
| `-R port:host:hostport` | *remote forward* | una porta sul **server remoto** viene inoltrata a `host:hostport` visto **dal lato locale** — "buca il firewall": espone verso l'esterno un servizio interno non altrimenti raggiungibile. Es: `ssh -R 110:10.0.0.2:110 200.1.1.1` |
| `-D [bind:]port` | *dynamic* — attiva un **proxy SOCKS** | ssh agisce da server SOCKS4/5; il lato remoto decide dove connettersi in base al protocollo — simil-TOR (senza il triplo salto) o simil-VPN per porte arbitrarie. Es: `ssh -D 10.0.0.2:8888 200.1.1.1` |
| `-J jumphost` | *jump* | si connette alla destinazione **passando prima** per uno o più jumphost (separati da virgole) — come `-L` ma specifico per SSH e multi-salto. Es: `ssh -J u1@1.1.1.1,u2@2.2.2.2 u3@3.3.3.3` |

Distinzione chiave: **`-L`** apre una porta *locale* (io raggiungo qualcosa oltre il gateway); **`-R`** apre una porta *remota* (io espongo qualcosa di mio verso l'esterno); **`-D`** è un proxy dinamico; **`-J`** è solo un modo comodo di concatenare salti SSH.

---

# PARTE 3 — OPENSSL IN PRATICA

**OpenSSL** è una libreria C che implementa le principali operazioni crittografiche (simmetrica, chiave pubblica, firma, hash) e il protocollo SSL/TLS. Da riga di comando è una "cassetta degli attrezzi". Orientamento:

```bash
openssl version        # es. "OpenSSL 3.0.8 7 Feb 2023"
openssl help           # Standard / Message Digest / Cipher commands
```

Comandi principali: `ca` (creare una CA), `dgst` (digest hash), `enc` (cifra simmetrica), `genrsa` (coppia RSA), `pkeyutl`/`rsautl` (asimmetrico), `rand`, `rsa` (manipolare chiavi RSA), `verify` (verificare certificati/catene), `x509` (manipolare certificati X.509).

## 13. Codifica vs cifratura simmetrica

```bash
openssl enc -base64 -in file_base64.txt     # NON è cifratura!
```
- **Meccanismo/visione**: `base64` è solo una **codifica** (reversibile da chiunque, senza chiave). Manca proprio la chiave: non nasconde nulla. È la trappola concettuale della slide ("Cosa manca per poterla considerare una cifratura?" → una **chiave segreta**).

Cifratura vera con AES:
```bash
openssl enc -aes-256-cbc -md sha512 -pbkdf2 -iter 100000 -salt -in file_testo.txt -out cifrato.bin
openssl enc -aes-256-cbc -md sha512 -pbkdf2 -iter 100000 -salt -d -in cifrato.bin   # -d = decifra
```
- **Significato dei flag**: `-aes-256-cbc` algoritmo AES a 256 bit in modalità CBC (molto sicuro); `-md sha512` funzione hash usata nella derivazione della chiave dalla password; `-pbkdf2` usa la **Password-Based Key Derivation Function 2** per derivare la chiave dalla password; `-iter 100000` numero di iterazioni della derivazione (**più alto → più lento il brute-force** del file); `-salt` aggiunge sale casuale (impedisce rainbow tables); `-d` decifra; `-pass pass:"..."` per passare la password inline (**sconsigliato** — resta nella history). L'elenco dei cifrari disponibili: `openssl enc -ciphers`.

## 14. Chiave pubblica (RSA)

```bash
openssl genrsa -out chiave.pem 2048        # coppia RSA; MINIMO 2048 bit per dirsi sicura
openssl rsa -in chiave.pem -text -noout    # dettagli; -noout = NON stampare la chiave in base64
```
- **Punto sottile fondamentale**: il file `chiave.pem` generato contiene **SIA la chiave privata SIA la pubblica** (la pubblica è derivabile dalla privata). Delimitatori: `-----BEGIN RSA PRIVATE KEY-----` … `-----END RSA PRIVATE KEY-----`.

Proteggere la chiave privata e estrarre la pubblica:
```bash
openssl rsa -in chiave.pem -aes-256-cbc -out enc_chiave.pem   # cifra il FILE della chiave privata con AES (passphrase)
openssl rsa -in chiave.pem -pubout -out pub_chiave.pem        # ESTRAE la sola chiave pubblica
```
- La chiave pubblica ha delimitatori diversi: `-----BEGIN PUBLIC KEY-----` … `-----END PUBLIC KEY-----`.

Cifratura/decifratura asimmetrica e firma:
```bash
openssl rsautl -encrypt -in testo.txt -inkey chiave.pem -out cifrato_rsa.bin
openssl rsautl -encrypt -in testo.txt -inkey pub_chiave.pem -pubin -out cifrato_rsa.bin  # -pubin: la chiave in input È già pubblica
openssl rsautl -decrypt -in cifrato_rsa.bin -inkey chiave.pem -out nuova.txt             # per decifrare serve la privata

openssl dgst -md5 -out digestfile testo.txt          # 1) calcola il digest (hash) del file
openssl rsautl -sign  -in digestfile -out digest_firmato -inkey chiave.pem   # 2) firma il digest con la privata
openssl rsautl -verify -in digest_firmato -out digest_verifica -inkey chiave.pem  # 3) verifica con la coppia
diff digestfile digest_verifica                      # se identici → firma valida (nessun output)
```
- **Perché firmare il digest e non il file**: non è efficiente firmare direttamente un file grande con un algoritmo a chiave pubblica → si firma il suo **hash** (la slide avverte: questo schema è in realtà meno sicuro della firma diretta con RSA, ma è il modello didattico).

## 15. PKI e certificati X.509

**Perché serve una PKI**: la crittografia a chiave pubblica risolve la distribuzione delle chiavi, ma resta il **problema del MITM** — se un avversario (Marco) mi convince che *la sua* chiave pubblica è quella di Bob, cifro per lui pensando di parlare con Bob. Serve un meccanismo per **legare in modo affidabile una chiave pubblica a un'identità**. Due approcci (distinzione da quiz):
- **PGP → Web of Trust**: ognuno costruisce la propria rete di fiducia condividendo chiavi affidabili (decentralizzato).
- **PKI → Root CA trust**: soluzione **centralizzata** — un'entità fidata (CA) certifica che una chiave pubblica appartiene davvero a una persona identificata, emettendo un **certificato** firmato.

**Cosa contiene un certificato**: informazioni identificative, la **chiave pubblica** del soggetto, data di creazione, data di **revoca** (validità tipica 1-3 anni), e la **firma digitale** della CA su tutto quanto sopra. Chi riceve il certificato controlla la firma della CA e la data di revoca.

**Creare una CA locale e firmare un certificato** (il cuore del lab — file di configurazione in `/etc/ssl/openssl.cnf`, sezioni `[ca]`, policy, req):

```bash
# 1) La CA: coppia di chiavi + certificato auto-firmato (self-signed) valido 10 anni
openssl genrsa -out rootCA.key 2048
openssl req -x509 -new -key rootCA.key -days 3650 -out rootCA.pem
#   -x509: produce un certificato (non una CSR); rootCA.pem contiene SOLO la pubblica + identità + firma,
#          NON la chiave privata (che resta in rootCA.key)

# (opzionale) esportare il cert della CA in formato DER per caricarlo nel browser
openssl x509 -in rootCA.pem -outform DER -out cacert.der

# 2) Il client: coppia di chiavi + richiesta di certificato (CSR)
openssl genrsa -out client1.key 2048
openssl req -new -key client1.key -out client1.csr
#   -new senza -x509 → una CSR (Certificate Signing Request): contiene la chiave PUBBLICA da firmare
#   per il Web PKI aggiungere:  -addext "subjectAltName = DNS:www.sitename.domain"

# 3) La CA firma la CSR → certificato del client
openssl x509 -req -days 365 \
  -CA rootCA.pem -CAkey rootCA.key \
  -CAcreateserial -CAserial serial \
  -copy_extensions copy \
  -in client1.csr -out client1.pem

# 4) Visualizzare e verificare
openssl x509 -in client1.pem -text -noout
openssl verify -verbose -CAfile rootCA.pem client1.pem
```
- **Significato dei flag di firma**: `-req` dice a `x509` che l'input è una CSR; `-CA`/`-CAkey` sono cert e chiave della CA firmante; `-CAcreateserial`/`-CAserial serial` gestiscono il **numero di serie** univoco del certificato (un file che tiene il contatore); `-copy_extensions copy` copia le estensioni (es. il SAN) dalla CSR al certificato; `-days` la validità. `verify -CAfile` controlla che il certificato del client sia firmato da una CA di cui ci fidiamo.

**Le tre entità da non confondere** (Lorenzo, attenzione): la **chiave** (`.key`, coppia priv+pub, segreta); la **CSR** (`.csr`, richiesta = chiave pubblica + identità, ancora *non* firmata); il **certificato** (`.pem`/`.crt`, = chiave pubblica + identità + **firma della CA**, pubblicabile). Il certificato **non** contiene mai la chiave privata.

---

# PARTE 4 — TLS IN PRATICA (configurazione servizi)

Obiettivo: usare la catena di certificati per creare un **tunnel TLS** su servizi reali (web server nginx, broker MQTT) e testare la vulnerabilità **Heartbleed**.

## 16. HTTPS con nginx e certificato self-signed

```bash
# certificato self-signed in un solo comando
sudo openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
  -keyout /etc/ssl/private/nginx-selfsigned.key \
  -out /etc/ssl/certs/nginx-selfsigned.crt
```
- **Flag**: `-x509` produce direttamente un certificato (auto-firmato); `-nodes` = "**no DES**" → **non** cifra la chiave privata con passphrase (comodo per far ripartire il server senza digitarla, meno sicuro); `-newkey rsa:2048` genera al volo una nuova coppia RSA a 2048 bit; `-keyout`/`-out` i due file prodotti. Durante l'input, il campo **Common Name (CN)** deve essere il **FQDN del sito** (es. `seclab.it`): è il sito per cui il certificato vale.
- **Self-signed vs CA-signed**: qui la CA è il sito stesso → il browser avvisa che non si fida (va "accettato il rischio"). Con una CA importata nel browser l'avviso sparisce.

```bash
# gruppo Diffie-Hellman per la Perfect Forward Secrecy (PFS)
sudo openssl dhparam -out /etc/nginx/dhparam.pem 512
```
- **Meccanismo**: il gruppo DH serve a negoziare chiavi effimere → **Perfect Forward Secrecy** (se in futuro si compromette la chiave del server, le sessioni passate restano protette). Il **minimo raccomandato è 2048** (qui 512 solo per non aspettare; "la security è scomoda").

Configurazione nginx (snippet): `ssl_certificate`/`ssl_certificate_key` (cert e chiave), poi `ssl-params.conf` con `ssl_protocols TLSv1.2;` (impone la versione), `ssl_prefer_server_ciphers on;`, `ssl_dhparam`, una `ssl_ciphers` selezionata (ECDHE/DHE-RSA-AES256-GCM…), `ssl_session_*` (cache/timeout), e header di sicurezza (`X-Frame-Options DENY`, `X-Content-Type-Options nosniff`, `X-XSS-Protection`). Il virtual host mette `listen 443 ssl;` e include gli snippet; un secondo `server` su `listen 80` fa `return 302 https://...` (redirect da HTTP a HTTPS). Si abilita con un symlink `sites-available → sites-enabled`, si verifica con `sudo nginx -t` (il warning `ssl_stapling ignored` è **normale** con un self-signed) e si riavvia con `systemctl restart nginx`. Per risolvere il nome si aggiunge `127.0.0.1 seclab.it` a `/etc/hosts`.

Test:
```bash
wget --no-check-certificate seclab.it     # --no-check-certificate: accetta il self-signed
```
- Nota: `http://seclab.it` risponde **302** (redirect), `https://seclab.it` risponde **200**.

## 17. TLS su MQTT (cenno)

**MQTT** (Message Queuing Telemetry Transport) è un protocollo publish/subscribe con un **broker** centrale (qui `mosquitto`) che accoda i messaggi per i subscriber. In chiaro:
```bash
mosquitto_sub -h localhost -t sensor/#              # subscriber
mosquitto_pub -t sensor/dht11/temperature -m 25     # publisher
```
Su Wireshark si vede il messaggio in chiaro. Abilitare TLS (compito per casa) significa applicare **lo stesso schema PKI**: creare CA + coppia+CSR del broker + firma, mettere i file in `<mosquitto>/certs/`, e nel `mosquitto.conf` impostare `port 8883`, `cafile`/`certfile`/`keyfile` e `tls_version`. Concetto-chiave: **TLS è solo un layer che cifra il traffico del tunnel**, quindi si applica a qualunque protocollo, non solo HTTP.

## 18. Heartbleed — dal riconoscimento all'exploit

```bash
nmap -p 443 --script ssl-heartbleed 192.168.56.XXX
```
- **Meccanismo**: lo script NSE `ssl-heartbleed` di `nmap` sonda la porta 443 e riporta `State: VULNERABLE` se il server usa una versione OpenSSL affetta (1.0.1 – 1.0.1f, 1.0.2-beta). Ricollega la teoria (§8) alla pratica: la heartbeat extension mal implementata legge memoria oltre la stringa ricevuta.
- **Exploit**: non esiste un exploit generico unico — deve adattarsi a SO e applicazione perché lavora leggendo *memoria*. Nel lab si usa un PoC (`git clone https://github.com/sensepost/heartbleed-poc.git`) che, dopo alcune iterazioni, legge dagli `access.log` di nginx richieste POST precedenti con **username e password in chiaro**. Insegnamento: un bug di *implementazione* di una libreria vanifica un protocollo teoricamente sicuro.

---

## Connessioni con altri moduli

- **Con S1 (Offensive Security & Enumerazione)**: la Parte 1 (recon, OSINT, dorking, DNS/subdomain enum, `nmap`, evasione, OpenVAS) è la stessa fase di *reconnaissance* di S1. Il di più di S13 è la coppia **VA/PT**, le **metodologie** (OSSTMM/OWASP/PCI-DSS/NIST/ISSAF) e le **posture** (blind/grey box). Non ripetere i dettagli dei comandi `nmap`: sono in S1.
- **Con S12 (Sicurezza delle comunicazioni)**: S12 ha catalogato in **teoria** gli attacchi (sniffing, ARP/DNS spoofing, hijacking, DoS); il **lab offensive** di S13 (§5) li **esegue** con `ettercap`/`hping3`, e la **Parte 2** di S13 fornisce le **contromisure** (canali sicuri) che S12 lasciava "in grigio". Sono le due metà complementari: attacco (S12) ↔ difesa (S13).
- **Con S14 (Crittografia)**: S14 spiega *come* funzionano RSA, hash, firma, PKI; la **Parte 3** di S13 li **invoca** con `openssl` (genrsa, dgst, rsautl, x509). Il "problema del MITM" che motiva la PKI (§15) è esattamente la firma digitale di S14 applicata all'associazione chiave↔identità.
- **Con S15 (comunicazioni sicure, se distinto)**: TLS/IPSec/VPN come *realizzazioni concrete* delle proprietà di sicurezza (riservatezza/integrità/autenticità) discusse nei moduli crittografici — TLS usa asimmetrico per l'handshake e simmetrico per il record, esempio da manuale di **cifrario ibrido**.

---

## Domande di autoverifica — stile quiz teorico (40%)

Rispondere **prima** di guardare le soluzioni (in fondo agli appunti). Attenzione: nel quiz reale le risposte sbagliate hanno **penalità**, quindi meglio astenersi se davvero incerti.

1. **V/F** — Un Vulnerability Assessment sfrutta le vulnerabilità trovate per accedere a viste più interne del sistema.
2. **V/F** — In TLS, una singola connessione può contenere più sessioni.
3. **V/F** — TLS e SSL condividono lo stesso formato di record; TLS è definito in RFC 5246 e 8446.
4. **Scelta multipla** — L'unica mitigazione efficace contro POODLE è: (a) abilitare RC4; (b) **disabilitare SSLv3**; (c) usare CBC con IV concatenati; (d) attivare la compressione.
5. **V/F** — Heartbleed è una vulnerabilità di *protocollo* di TLS.
6. **V/F** — HSTS protegge anche la primissima richiesta HTTP di un browser verso un sito mai visitato.
7. **Scelta multipla** — In IPSec, quale protocollo offre *riservatezza* (cifratura) come servizio principale? (a) AH; (b) **ESP**; (c) SPI; (d) ISAKMP.
8. **V/F** — AH è pienamente compatibile con il NAT, perché non autentica gli indirizzi IP.
9. **Scelta multipla** — In una porta di switch in *access mode*: (a) serve il tagging 802.1q; (b) **appartiene a una sola VLAN e il tagging non serve**; (c) trasporta più VLAN; (d) è l'uso tipico verso i router.
10. **V/F** — `openssl enc -base64` fornisce riservatezza perché trasforma il testo in una stringa illeggibile.
11. **V/F** — Il file prodotto da `openssl genrsa -out chiave.pem 2048` contiene sia la chiave privata sia la pubblica.
12. **V/F** — Il certificato `rootCA.pem` prodotto con `openssl req -x509` contiene anche la chiave privata della CA.
13. **Scelta multipla** — Il flag `-nodes` in `openssl req -x509 -nodes ...` significa: (a) nessun output; (b) **non cifrare la chiave privata con una passphrase**; (c) usa più nodi; (d) disabilita DES nel certificato.
14. **V/F** — Con `ssh -L 8080:interno:80 gateway`, la porta 8080 viene aperta sul *server remoto*.
15. **Scelta multipla** — Il *double tagging* nel VLAN hopping: (a) funziona in entrambe le direzioni; (b) **funziona solo in andata**; (c) richiede DTP sulla vittima; (d) non usa i tag 802.1q.
16. **V/F** — In TOR l'exit node vede il traffico applicativo in chiaro se non c'è cifratura end-to-end.
17. **V/F** — PGP usa una Root CA centralizzata, mentre la PKI usa un Web of Trust.
18. **Scelta multipla** — Cosa distingue tunnel mode da transport mode in IPSec? (a) nulla; (b) **il tunnel incapsula l'intero pacchetto IP originale in uno nuovo**; (c) il transport cifra sempre l'header esterno; (d) il tunnel è solo per host-to-host.
