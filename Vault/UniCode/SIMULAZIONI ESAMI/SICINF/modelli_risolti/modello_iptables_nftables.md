# Modello Risolto — Iptables/NFTables

> Fonte: `SIMULAZIONI ESAMI/SICINF/IptablesNFTables.html` (Virtuale) — **7 esercizi d'esame reali**
> (11 giugno 2021 → 12 gennaio 2026), in ordine cronologico in questo file.
>
> **Nota tecnica sull'estrazione (rilevante per come sono stati trovati questi materiali)**: in
> questo HTML le soluzioni ufficiali del docente non sono testo visibile scorrendo la pagina — sono
> allegate come **data URI in base64** dietro ogni link "SOLUZIONE" (`href="data:text/plain;
> base64,..."` o simili). Vanno decodificate esplicitamente per essere lette. Con questo metodo,
> **tutti e 7 gli esercizi del pool hanno soluzione ufficiale del docente recuperabile** — nessuna
> elaborazione è stata necessaria per completare questo file.
>
> **AGGIORNAMENTO 15/07/2026**: quando il caso del 13 settembre 2023 fu catalogato per la prima
> volta (09/07/2026), la soluzione ufficiale non venne trovata con una lettura superficiale
> dell'HTML e fu quindi elaborata (segnalato esplicitamente all'epoca, correttamente, come
> elaborazione e non trascrizione). Riesaminando l'HTML con decodifica sistematica dei link
> `SOLUZIONE`, la soluzione ufficiale **esiste ed è stata trovata** — è trascritta più sotto nel
> caso 2, con l'elaborazione precedente mantenuta accanto per confronto (resta un ragionamento
> valido, ma il testo da studiare è quello ufficiale).

---

## Come leggere questo file

Per ciascuno dei 7 casi: consegna trascritta fedelmente dall'HTML, topologia (dal disegno originale
se presente nell'HTML, altrimenti dedotta dagli indirizzi usati nella soluzione ufficiale — sempre
segnalato quale dei due casi si applica), ragionamento INPUT/OUTPUT/FORWARD per ogni host coinvolto,
la soluzione ufficiale per intero, e una sezione "Perché funziona" a due livelli (meccanismo +
visione). Gotcha e refusi nel testo del docente sono segnalati onestamente, mai silenziati né
corretti senza nota — quando lo faccio, la correzione proposta è chiaramente etichettata come mia,
non come parte del materiale ufficiale.

---

## Caso 1 — 11 giugno 2021 (iptables, host singolo)

### Consegna originale

> L'esercitazione di iptables consiste nel creare una serie di regole per un singolo host che
> potrebbe avere più interfacce e funzionare come router.
>
> Scrivete nel file di testo i comandi che si devono impartire per ottenere i risultati richiesti.
> Si consiglia di leggere prima tutta la lista per determinare correttamente i requisiti.
>
> Le regole saranno testate per verificarne la correttezza.
>
> **Le regole devono essere applicate nell'ordine in cui vengono proposte.**
>
> Si inizi garantendo che le catene siano tutte vuote, e si proceda per:
> 1. Consentire qualsiasi traffico sull'interfaccia di loopback
> 2. Consentire il traffico delle connessioni HTTP entranti
> 3. Consentire connessioni SSH uscenti verso la rete host-only `192.168.56.0/24`
> 4. Bloccare l'inoltro del traffico proveniente dalla rete host-only verso altre destinazioni
> 5. Consentire la risoluzione dei nomi DNS
> 6. Infine bloccare tutto il traffico non elencato nei punti 2, 3, 5

Nessun disegno di rete allegato in questo HTML: è deliberatamente un esercizio a **host singolo**
("potrebbe avere più interfacce e funzionare come router" — tipico contesto da VM VirtualBox con
un'interfaccia NAT/verso Internet e una host-only verso `192.168.56.0/24`, lo stesso contesto
esplicito anche nel caso 3 di questo file).

### Come ragionare

Un solo host da configurare, ma **due ruoli distinti nello stesso host**: traffico che lo riguarda
in prima persona (INPUT/OUTPUT) e traffico che eventualmente attraversa (FORWARD), perché il testo
dice esplicitamente che potrebbe fare da router.

- **Punto 2 (HTTP entrante)**: l'host è **server** → INPUT `--dport 80` (richiesta) + OUTPUT
  `--sport 80` con `ESTABLISHED` (risposta).
- **Punto 3 (SSH uscente verso l'host-only)**: l'host è **client** → OUTPUT `--dport 22` (richiesta)
  + INPUT `--sport 22` con `ESTABLISHED` (risposta), ristretto a quella rete specifica.
- **Punto 4 (bloccare il forwarding dalla rete host-only verso altre destinazioni)**: qui l'host
  **attraversa** traffico che non lo riguarda (non è né sorgente né destinazione finale) → `FORWARD`.
- **Punto 5 (risoluzione DNS)**: è l'host stesso a dover risolvere nomi → OUTPUT `--dport 53`
  (richiesta) + INPUT `--sport 53` con `ESTABLISHED` (risposta).
- **Punto 6 (blocca tutto il resto)**: nota bene, dice **"non elencato nei punti 2, 3, 5"** — il
  punto 4 (FORWARD) non è tra quelli richiamati. È l'indizio testuale che la policy di default per
  `FORWARD` non deve essere `DROP` (vedi "Perché funziona").

### `iptables.txt` — soluzione ufficiale

```
# Utilizzo l'opzione -A in tutte le regole per fare in modo che vengano inserite una in seguito all'altra in ordine

# 1) Consentire qualsiasi traffico sull'interfaccia di loopback

iptables -A INPUT -i lo -j ACCEPT
iptables -A OUTPUT -o lo -j ACCEPT


# 2) Consentire il traffico delle connessioni HTTP entranti

iptables -A INPUT -p tcp --dport 80 -j ACCEPT
iptables -A OUTPUT -p tcp --sport 80 -m state --state ESTABLISHED -j ACCEPT


# 3) Consentire connessioni SSH uscenti verso la rete host-only 192.168.56.0/24

iptables -A OUTPUT -p tcp -d 192.168.56.0/24 --dport 22 -j ACCEPT
iptables -A INPUT -p tcp -s 192.168.56.0/24 --sport 22 -m state --state ESTABLISHED -j ACCEPT

# 4) Bloccare l'inoltro del traffico proveniente dalla rete host-only verso altre destinazioni

iptables -A FORWARD -s 192.168.56.0/24 ! -d 192.168.56.0/24 -j DROP

# 5) Consentire la risoluzione dei nomi DNS

iptables -A OUTPUT -p udp --dport 53 -j ACCEPT
iptables -A INPUT -p udp --sport 53 -m state --state ESTABLISHED -j ACCEPT


# 6) Infine bloccare tutto il traffico non elencato nei punti 2, 3, 5

iptables -P INPUT DROP
iptables -P OUTPUT DROP
iptables -P FORWARD ACCEPT

# notare che l'esclusione della regola 4 deve far dedurre  che per il forwarding
# deve valere un principio di default accept, altrimenti non avrebbe senso la regola
# che applica a un caso specifico l'azione DROP
```

### Perché funziona

**`-A` ovunque, non `-I`, e il perché è nella consegna stessa.** La traccia dice esplicitamente "le
regole devono essere applicate nell'ordine in cui vengono proposte" — `-A` (append) accoda ogni
regola in fondo alla catena, preservando l'ordine di scrittura; `-I` (insert, senza numero) la mette
sempre in **testa**, quindi una sequenza di `-I` produce l'ordine **invertito** rispetto a quello di
scrittura. Qui l'ordine non è un dettaglio stilistico: è testato. Tienilo a mente per il triage di
ogni esercizio di questa famiglia — se la consegna richiama esplicitamente l'ordine, usa `-A`; se
non lo richiama (vedi caso 3 più sotto) e le regole non si sovrappongono nel traffico che
intercettano, `-I` è innocuo.

**Il punto più sottile dell'esercizio è dedurre la default policy di `FORWARD` dal testo, non da
una regola esplicita.** Il punto 6 dice di bloccare tutto ciò "non elencato nei punti 2, 3, 5":
il punto 4 (il DROP sul forwarding host-only) resta fuori da questo elenco. Se la policy di
`FORWARD` fosse già `DROP` di default, la regola del punto 4 sarebbe **ridondante** (un DROP
esplicito su un sottoinsieme di traffico che sarebbe comunque scartato dalla policy) — non avrebbe
senso scriverla. L'unica lettura coerente è che `FORWARD` resti `ACCEPT` di default, e la regola
del punto 4 sia l'**unica** eccezione esplicita a quella libertà: tutto il resto del forwarding
(traffico che non ha sorgente nella rete host-only) passa, mentre specificamente il traffico
originato dalla rete host-only e diretto altrove viene bloccato. Il commento ufficiale nel file lo
conferma testualmente.

**`! -d 192.168.56.0/24`** nella regola 4 è la negazione di match: "sorgente nella rete host-only
**e** destinazione **non** nella stessa rete" — se il `!` mancasse, la regola bloccherebbe anche il
traffico host-only↔host-only (violando implicitamente lo scopo dell'esercizio, che è isolare la
rete host-only dal resto, non da sé stessa).

**Sintassi**: `iptables` legacy. Nessun NAT. **Gotcha**: nessun refuso rilevato in questa soluzione
— è però l'unico caso del pool con `FORWARD` default `ACCEPT` invece di `DROP`: non applicare
meccanicamente "default-drop ovunque" senza aver riletto la consegna punto per punto.

---

## Caso 2 — 13 settembre 2023 (iptables, 3 host)

### Consegna originale

> Facendo riferimento allo schema di rete sopra riportato, si definiscano regole di filtraggio che
> consentano il traffico come sotto specificato; **qualsiasi altro pacchetto deve essere
> scartato**.
> **NOTA**: le regole devono essere installate su **ogni** host coinvolto nel flusso di traffico
> specificato.
> 1. i Client sulla rete privata `192.168.0.0/24` devono poter interrogare DNS e servizi di
>    sincronizzazione NTP in Internet (porte UDP 53 e **1233**)
> 2. il servizio SMTP (porta 25 tcp) del Server collocato sulla rete privata `172.16.0.0/20` deve
>    essere raggiungibile da qualsiasi host di Internet
> 3. il servizio LDAP (porta 389 tcp) del Router deve essere raggiungibile dal Server
>
> **MODALITÀ DI CONSEGNA**: 1 file `iptables.txt` con tre sezioni chiaramente contrassegnate, una
> per ogni host su cui è richiesto installare le regole, coi comandi (sintatticamente corretti)
> che le realizzano.

Topologia (dal disegno originale):
```
Client (eth1) ---- Rete 192.168.0.0/24 ---- eth1(.254) [R] eth2(172.16.15.254) ---- Rete 172.16.0.0/20 ---- Server (eth1, 172.16.0.1)
                                                    eth3 (130.136.5.15)
                                                      |
                                                  Internet
```

### Come ragionare sulla topologia

- **Client**: genera traffico (DNS/NTP) verso Internet → **OUTPUT** (richiesta) + **INPUT**
  (risposta). Non fa forwarding.
- **Router**: il traffico Client↔Internet e Internet↔Server lo **attraversa** → **FORWARD**. Il
  traffico Server→Router:389 **termina sul Router stesso** (è lui il server LDAP) → **INPUT**
  (richiesta) + **OUTPUT** (risposta).
- **Server**: riceve SMTP da Internet → **INPUT**+**OUTPUT** locale. Interroga LDAP sul Router →
  **OUTPUT**+**INPUT** locale (è lui il client in questa interazione).

Poi, per ogni regola: default-drop su tutte e tre le catene, loopback sempre permesso, e per ogni
interazione bidirezionale due righe (richiesta con `--dport`, risposta con `--sport` +
`ESTABLISHED`).

### `iptables.txt` — soluzione ufficiale (ritrovata il 15/07/2026)

```
################ CLIENT ################

iptables -F INPUT
iptables -F OUTPUT
iptables -F FORWARD

iptables -I INPUT -i lo -j ACCEPT
iptables -I OUTPUT -o lo -j ACCEPT

# 1) i Client sulla rete privata 192.168.0.0/24
# devono poter interrogare DNS e servizi di sincronizzazione NTP
# in Internet (porte UDP 53 e 123)

iptables -A INPUT -p udp -i eth1 --sport 53 -m state --state ESTABLISHED -j ACCEPT
iptables -A OUTPUT -p udp -o eth1 --dport 53 -j ACCEPT
iptables -A INPUT -p udp -i eth1 --sport 123 -m state --state ESTABLISHED -j ACCEPT
iptables -A OUTPUT -p udp -o eth1 --dport 123 -j ACCEPT
#
# nulla da configurare per i punti (2) e (3)
#

iptables -P INPUT DROP
iptables -P OUTPUT DROP
iptables -P FORWARD DROP

################ SERVER ################

iptables -F INPUT
iptables -F OUTPUT
iptables -F FORWARD

iptables -I INPUT -i lo -j ACCEPT
iptables -I OUTPUT -o lo -j ACCEPT

# nulla da configurare per il punto (1)
#
# 2) il servizio SMTP (porta 25 tcp) del Server collocato sulla rete privata 172.16.0.0/20
# deve essere raggiungibile da qualsiasi host di Internet
#
# per semplicità accettiamo tutte le sorgenti ma a rigore andrebbero escluse le reti private
#
iptables -A INPUT -p tcp -i eth1 -d 172.16.0.1 --dport 25 -j ACCEPT
iptables -A OUTPUT -p tcp -o eth1 -s 172.16.0.1 --sport 25 -m state --state ESTABLISHED -j ACCEPT

#
# 3) il servizio LDAP (porta 389 tcp) del Router deve essere raggiungibile dal Server
#
iptables -A OUTPUT -p tcp -o eth1 -s 172.16.0.1 -d 172.16.15.254 --dport 389 -j ACCEPT
iptables -A INPUT -p tcp -i eth1 -s 172.16.15.254 -d 172.16.0.1 --sport 389 -m state --state ESTABLISHED -j ACCEPT

iptables -P INPUT DROP
iptables -P OUTPUT DROP
iptables -P FORWARD DROP

################ ROUTER ################

iptables -t nat -F
iptables -F INPUT
iptables -F OUTPUT
iptables -F FORWARD

iptables -I INPUT -i lo -j ACCEPT
iptables -I OUTPUT -o lo -j ACCEPT

# 1) i Client sulla rete privata 192.168.0.0/24
# devono poter interrogare DNS e servizi di sincronizzazione NTP
# in Internet (porte UDP 53 e 123)

iptables -A FORWARD -p udp -i eth1 -o eth3 -s 192.168.0.0/16 --dport 53 -j ACCEPT
iptables -A FORWARD -p udp -i eth3 -o eth1 -d 192.168.0.0/16 --sport 53 -m state --state ESTABLISHED -j ACCEPT
iptables -A FORWARD -p udp -i eth1 -o eth3 -s 192.168.0.0/16 --dport 123 -j ACCEPT
iptables -A FORWARD -p udp -i eth3 -o eth1 -d 192.168.0.0/16 --sport 123 -m state --state ESTABLISHED -j ACCEPT
iptables -t nat -A POSTROUTING -p tcp -i eth1 -s 192.168.0.0/24 -o eth3 -j SNAT --to-source 130.136.5.15

# 2) il servizio SMTP (porta 25 tcp) del Server collocato sulla rete privata 172.16.0.0/20
# deve essere raggiungibile da qualsiasi host di Internet
#
iptables -t nat -A PREROUTING -i eth3 -o eth1 -s 130.136.5.15 -p tcp --dport 25 -j SNAT --to-destination 172.16.0.1
iptables -A FORWARD -p tcp -i eth3 -o eth2 -d 172.16.0.1 --dport 25 -j ACCEPT
iptables -A FORWARD -p tcp -i eth2 -o eth3 -s 172.16.0.1 --sport 25 -m state --state ESTABLISHED -j ACCEPT

#
# 3) il servizio LDAP (porta 389 tcp) del Router deve essere raggiungibile dal Server
#
iptables -A INPUT -p tcp -i eth2 -s 172.16.0.1 -d 172.16.15.254 --dport 389 -j ACCEPT
iptables -A OUTPUT -p tcp -o eth2 -s 172.16.15.254 -d 172.16.0.1 --sport 389 -m state --state ESTABLISHED -j ACCEPT

iptables -P INPUT DROP
iptables -P OUTPUT DROP
iptables -P FORWARD DROP
```

### Perché funziona

Le policy di default `DROP` su tutte e tre le catene realizzano subito il requisito "qualsiasi
altro pacchetto deve essere scartato" — non serve una regola finale di DROP esplicita: si scrivono
solo le regole di ciò che deve passare. Ogni interazione "vera" (non locale all'host) è bidirezionale:
chi apre la connessione lo fa in uscita verso una porta di **destinazione** nota; chi risponde lo fa
in ingresso su quella porta e risponde con sorgente uguale a quella porta — da cui la coppia
`--dport` (richiesta) / `--sport` + `ESTABLISHED` (risposta), sempre più restrittiva di "apri anche
la porta sorgente in permanenza".

Sul Router, la parte concettualmente delicata è distinguere `FORWARD` (Client↔Internet,
Internet↔Server: il router non è né sorgente né destinazione finale) da `INPUT`/`OUTPUT` (LDAP:
il router **è** il server, quindi per lui è locale come su un host qualunque) — lo stesso errore
concettuale da evitare ovunque in questo pool è mettere in `FORWARD` un servizio che gira sull'host
stesso: non funzionerebbe mai, quel traffico non transita mai per quella catena.

### Differenze rispetto all'elaborazione precedente (09/07/2026)

Quando questo caso fu catalogato la prima volta senza la soluzione ufficiale, il ragionamento
prodotto era strutturalmente corretto (stessa distinzione INPUT/OUTPUT/FORWARD, stesso schema
richiesta/risposta) ma differiva in due dettagli minori: filtrava sull'intera subnet
`172.16.0.0/20` per SMTP/LDAP invece che sull'host specifico `172.16.0.1` (più permissivo, non
sbagliato se il Server è l'unico host di quel ruolo in quella rete), e non replicava i due errori
di sintassi della soluzione ufficiale descritti sotto (semplicemente perché non li aveva "copiati").
Se stai ripassando da zero questo caso, usa il testo ufficiale sopra come riferimento, non
l'elaborazione — ma il ragionamento del "Perché funziona" resta valido in entrambe le versioni.

### ⚠️ Gotcha 1 — refuso nella consegna: la porta NTP

La consegna scrive "porte UDP 53 e **1233**", ma la soluzione ufficiale usa correttamente
`--dport 123` (la porta NTP standard, RFC 5905) sia sul Client sia sul Router — **il docente stesso
ignora il proprio testo e usa la porta corretta**. `1233` è quasi certamente un refuso di
battitura (le cifre 2/3 vicine, o un errore di trascrizione del compito). **Lezione operativa**: se
un esercizio nomina un servizio noto (DNS, NTP, SSH, SMTP, LDAP, POP, IMAPS...) con una porta che
non corrisponde a quella standard, sospetta un refuso — e se hai la soluzione ufficiale a
disposizione per verificare, fidati di quella, non del numero scritto nel testo della consegna.

### ⚠️ Gotcha 2 — SNAT/DNAT invertiti sulla riga SMTP del Router

```
iptables -t nat -A PREROUTING -i eth3 -o eth1 -s 130.136.5.15 -p tcp --dport 25 -j SNAT --to-destination 172.16.0.1
```
Due problemi verificabili secondo la sintassi standard di `iptables`, non solo uno stile diverso dal
mio:
1. **`-j SNAT --to-destination`** non è una combinazione valida — `--to-destination` è un'opzione
   del target `DNAT` (cambia la destinazione), non di `SNAT` (che accetta solo `--to-source`).
   Caricata così, la regola verrebbe rifiutata da `iptables` al momento dell'inserimento
   ("unrecognized option"). L'intento è chiaro dal contesto (tradurre la destinazione del traffico
   SMTP in arrivo dall'IP pubblico del router verso il server interno): quello che serve è
   `-j DNAT --to-destination 172.16.0.1`.
2. **`-o eth1` in catena `PREROUTING`**: nel punto in cui agisce `PREROUTING` (prima della
   decisione di instradamento) l'interfaccia di uscita non è ancora nota — `iptables` non accetta
   `-o` in `PREROUTING`/`INPUT` (né `-i` in `OUTPUT`/`POSTROUTING`), qualunque sia la tabella.

Presa alla lettera, questa riga non si installerebbe. È probabile che sia un refuso da
copia-incolla della riga SNAT del Client subito sopra (stesso schema `-i .. -o .. -s .. -j SNAT
--to-...`), adattata nell'indirizzo ma non nel target né nell'interfaccia. Versione corretta per
intento:
```
iptables -t nat -A PREROUTING -i eth3 -s 130.136.5.15 -p tcp --dport 25 -j DNAT --to-destination 172.16.0.1
```
(quest'ultima è una mia correzione di intento, non fa parte del testo ufficiale del docente.)

### ⚠️ Gotcha 3 — protocollo sbagliato **e** `-i` non ammesso, sulla riga SNAT del Client

```
iptables -t nat -A POSTROUTING -p tcp -i eth1 -s 192.168.0.0/24 -o eth3 -j SNAT --to-source 130.136.5.15
```
Questa riga vuole mascherare l'uscita DNS/NTP dei client verso Internet, e ha **due** difetti (non
uno solo):
1. **Protocollo sbagliato (`-p tcp`)**: DNS e NTP sono **UDP** (le due coppie FORWARD subito sopra
   sono infatti correttamente `-p udp`), mentre qui il match è `-p tcp`, quindi non intercetta i
   pacchetti UDP a cui è destinata. Probabile copia-incolla da un contesto TCP (SMTP) non adattato al
   protocollo. Per intento andrebbe `-p udp`, o nessun vincolo di protocollo.
2. **`-i eth1` non è ammesso in `POSTROUTING`**: è la stessa regola d'oro del kit (§6 di
   `procedura_operativa_iptables.md` — «`iptables` non accetta `-i` in `OUTPUT`/`POSTROUTING`»)
   violata sul lato speculare rispetto al Gotcha 2 (che segnalava `-o eth1` in `PREROUTING`). Al
   momento in cui agisce `POSTROUTING` l'interfaccia di **entrata** non è più un'informazione
   disponibile → `iptables` rifiuterebbe la regola al caricamento. Il match sull'interfaccia di
   uscita (`-o eth3`) è invece corretto e sufficiente a delimitare l'uscita verso Internet; la
   sorgente è già ristretta da `-s 192.168.0.0/24`. Versione corretta per intento (mia correzione,
   non del docente):
```
iptables -t nat -A POSTROUTING -p udp -s 192.168.0.0/24 -o eth3 -j SNAT --to-source 130.136.5.15
```
Presa alla lettera, quindi, come la riga SMTP del Gotcha 2, anche questa riga non si installerebbe:
entrambe hanno l'interfaccia messa in una catena che non la ammette.

**Sintassi**: `iptables` legacy.

---

## Caso 3 — 8 febbraio 2024 (iptables, 1 file per il Router)

### Consegna originale

> Fate riferimento all'**esercizio su Intrusion Detection** [collegamento a
> `Network_Intrusion_Detection.html`, stessa data], dopo aver individuato l'attacco (eventualmente
> guardando le soluzioni), gli altri tipi di traffico presenti nel tracciato sono da considerare
> legittimi.
> Consegnate un file **`ipt.sh`** coi comandi che permettano di configurare il packet filter del
> **router** per consentire unicamente tali interazioni.

Particolarità di questo esercizio: **non ha un proprio testo di topologia** — rimanda esplicitamente
all'esercizio NIDS omonimo (stessa data, altro libro Virtuale) per il contesto, e chiede **un solo
file** (solo il Router, non "ogni host coinvolto" come nel caso 2).

### Contesto dall'esercizio NIDS collegato (necessario per capire la topologia)

Dal testo dell'esercizio NIDS "8 febbraio 2024": *"il tracciato è raccolto su di un router che ha
indirizzo con byte finale = 1 su tre subnet diverse"*, e la consegna chiede di scrivere due regole
Suricata per l'attacco individuato (non richieste qui, sono nell'altro libro). La soluzione
ufficiale di **quell'**esercizio identifica l'attacco: richieste HTTP GET ripetute da
`172.21.1.118` verso `172.22.2.159` su `/api/index.html`, sempre respinte con `401 Unauthorized` —
un tentativo di accesso non autorizzato via HTTP (porta 80). Questo è il traffico da **non**
considerare legittimo: non compare in nessuna regola della soluzione `ipt.sh` qui sotto, ed è
corretto che sia così.

### Topologia (dedotta dagli indirizzi nella soluzione ufficiale + dal testo NIDS collegato — nessun disegno esplicito in questo HTML)

```
rete1 172.21.1.0/24                    rete2 172.22.2.0/24                    rete3 172.23.3.0/24
Client 172.21.1.118 ------+                                          +------ Host3 172.23.3.187
                          |                                          |       (server NTP/SSH per rete2;
                          |     [ROUTER: eth?=172.21.1.1 /            |       client DNS verso router)
                          +---- 172.22.2.1 / 172.23.3.1] -------------+
                                       |
                          Host2 172.22.2.159
                          (server POP/IMAPS per rete1;
                           client NTP/SSH verso rete3)
```
Un solo router con tre interfacce (indirizzo `.1` su ciascuna subnet), niente NAT, niente Internet
in questo esercizio — è un router puramente interno a tre reti.

### Come ragionare (solo sul Router, unico host richiesto)

- **DHCP** (router serve le tre reti): locale al router → INPUT/OUTPUT sulle porte 67/68, senza
  restrizione di interfaccia (il router lo eroga uniformemente).
- **DNS** (router è server DNS per Host3 su rete3): locale al router → INPUT/OUTPUT, ristretto a
  `172.23.3.187 ↔ 172.23.3.1`.
- **NTP** (Host3 è server NTP per Host2): il router non è né sorgente né destinazione → **FORWARD**.
- **SSH** (stessa coppia Host3→Host2): **FORWARD**.
- **POP/IMAPS** (Host2 è server per Client su rete1): **FORWARD**.
- **HTTP (porta 80, l'attacco)**: nessuna regola — resta bloccato dalla policy di default.

### `ipt.sh` — soluzione ufficiale

```
# flush per partire puliti
iptables -F INPUT
iptables -F OUTPUT
iptables -F FORWARD

# router = server dhcp per le tre reti
iptables -I INPUT -p udp --sport 68 --dport 67 -j ACCEPT
iptables -I OUTPUT -p udp --dport 68 --sport 67 -m state --state ESTABLISHED -j ACCEPT


# router = server dns per rete .3
iptables -I INPUT -p udp -s 172.23.3.187 -d 172.23.3.1 --dport 53 -j ACCEPT
iptables -I OUTPUT -p udp -d 172.23.3.187 -s 172.23.3.1 --sport 53 -m state --state ESTABLISHED -j ACCEPT

# host su rete 3 = server NTP per client su rete 2
iptables -I FORWARD -p udp -s 172.22.2.159 -d 172.23.3.187 --dport 123 --sport 123 -j ACCEPT
iptables -I FORWARD -p udp -d 172.22.2.159 -s 172.23.3.187 --dport 123 --sport 123 -m state --state ESTABLISHED -j ACCEPT

# host su rete 3 = server ssh per client su rete 2
iptables -I FORWARD -p tcp -s 172.22.2.159 -d 172.23.3.187 --dport 22 -j ACCEPT
iptables -I FORWARD -p tcp -d 172.22.2.159 -s 172.23.3.187 --sport 22 -m state --state ESTABLISHED -j ACCEPT

# host su rete 2 = server POP per client su rete 1
iptables -I FORWARD -p tcp -s 172.21.1.118 -d 172.22.2.159 --dport 110 -j ACCEPT
iptables -I FORWARD -p tcp -d 172.21.1.118 -s 172.22.2.159 --sport 110 -m state --state ESTABLISHED -j ACCEPT

# host su rete 2 = server IMAPS per client su rete 1
iptables -I FORWARD -p tcp -s 172.21.1.118 -d 172.22.2.159 --dport 993 -j ACCEPT
iptables -I FORWARD -p tcp -d 172.21.1.118 -s 172.22.2.159 --sport 993 -m state --state ESTABLISHED -j ACCEPT

# detfault deny tranne loopback (e per il contesto virtualbox, eth0)
iptables -I INPUT -i lo -j ACCEPT
iptables -I OUTPUT -o lo -j ACCEPT
iptables -I INPUT -i eth0 -j ACCEPT
iptables -I OUTPUT -o eth0 -j ACCEPT

iptables -P INPUT DROP
iptables -P OUTPUT DROP
iptables -P FORWARD DROP
```
(`detfault` è un refuso di battitura nel commento originale del docente — "default" — segnalato
solo per completezza di trascrizione, ininfluente sul funzionamento.)

### Perché funziona

**NTP con `--dport 123 --sport 123` nella stessa regola** (non la coppia asimmetrica dport/sport
vista altrove): non è un errore, è una caratteristica reale del protocollo NTP, che a differenza
della maggior parte dei servizi non usa porte effimere lato client — client e server comunicano
entrambi sulla porta 123. Da qui la necessità di specificare **entrambi** i match nella stessa
regola invece della coppia dport-richiesta/sport-risposta.

**Qui `-I` non crea il problema visto nel caso 1**, anche se lo stile è identico (tutte le regole
con `-I`, quindi ogni nuova entra in testa e l'ordine finale nella catena è **inverso** rispetto
all'ordine di scrittura: `eth0`/`lo` finiscono per essere valutati per primi, DHCP per ultimo). La
differenza è che qui **nessuna consegna richiede un ordine specifico**, e le regole non si
sovrappongono nel traffico che intercettano (porte e coppie IP diverse, match disgiunti) — quindi
l'ordine relativo tra regole ACCEPT è irrilevante: conta solo che la policy DROP finale sia
impostata per ultima. Contrasta questo con il caso 1, dove l'ordine era invece parte esplicita del
test.

**Nessuna regola per la porta 80 (l'attacco)**: non serve un DROP esplicito, la policy di default
lo scarta già — coerente col principio "scrivi solo ciò che deve passare" di tutto questo pool.

**Un solo file (`ipt.sh`, solo Router)**: a differenza del caso 2, qui il servizio "vero" (POP,
IMAPS, NTP, SSH) gira su host che **non sono richiesti in consegna** (`ipt-server`,
`ipt-client`...) — la valutazione si concentra solo sul router che fa da packet filter centrale.
Non presumere che ogni esercizio richieda sempre "un file per host": leggi la consegna.

**Sintassi**: `iptables` legacy. Nessun NAT. **Gotcha**: nessuno di sostanza oltre al refuso di
battitura nel commento; nota comunque che le regole FORWARD non usano `-i`/`-o` (a differenza del
caso 2) — funziona perché gli indirizzi coinvolti sono host singoli e non sottoreti, ma è una
semplificazione: se in un esercizio simile gli indirizzi fossero intere subnet, l'assenza di
`-i`/`-o` diventerebbe rischiosa (regole più permissive di quanto intendi).

---

## Caso 4 — 13 giugno 2024 (iptables, Router+Server)

### Consegna originale

> Si consideri la rete illustrata: *(immagine, vedi sotto)*
> su cui devono essere consentiti unicamente i seguenti tipi di traffico:
> 1. accesso da parte dei client alla porta TCP 993 del server
> 2. accesso da parte di qualsiasi host su internet alla porta TCP 25 del server
> 3. navigazione sicura dei client sul web (internet, porta TCP 443)
> 4. accesso da parte dei client alla porta UDP 53 del router
>
> Si realizzino due script per la configurazione con iptables dei filtri necessari, rispettivamente
> **`ipt-router.sh`** per le regole da installare sul router e **`ipt-server.sh`** per le regole da
> installare sul server.

Topologia (dal disegno originale):
```
Client_n (eth1) ---- Rete privata 172.20.0.0/20 ---- eth1(172.20.15.254) [ROUTER: eth1,eth2] eth2(1.1.1.1) ---- Rete pubblica 1.1.1.0/28 ---- eth1(1.1.1.14) [SERVER]
                                                              eth3 (137.204.1.15)
                                                                |
                                                            Internet
```
(più client sulla stessa rete privata, rappresentati come pila di rettangoli tratteggiati nel
disegno originale — stesso stile grafico del "Client" del caso 2.)

**Particolarità**: si chiedono solo **due** script (Router, Server) — nessuno script Client
richiesto, a differenza del caso 2 dove ogni host coinvolto doveva avere le sue regole. Non
generalizzare "un file per host" da un esercizio all'altro: dipende dalla consegna specifica.

### Come ragionare

- **Punto 1** (client → server:993, IMAPS): il Server è endpoint → INPUT/OUTPUT locale sul Server;
  il Router fa FORWARD. Punto sottile: la rete "pubblica" `1.1.1.0/28` del server **non ha
  instradamento di ritorno** verso la rete privata dei client (`172.20.0.0/20` non è raggiungibile
  da quel segmento) — quindi il Router deve **SNAT-are** il traffico client in uscita verso il
  server con un proprio indirizzo su quella rete pubblica (`1.1.1.1`), altrimenti le risposte del
  server non saprebbero come tornare a un IP privato non instradabile lì.
- **Punto 2** (internet → server:25, SMTP): il Server ha già un indirizzo instradabile
  pubblicamente (`1.1.1.14`, sulla rete dichiarata "pubblica") → raggiungibile direttamente via
  FORWARD, **nessun NAT necessario** — diverso dal caso del 12 gennaio 2026 (più avanti in questo
  file), dove il server aveva IP privato e serviva DNAT: qui il segnale "serve NAT" non è la parola
  "indiretto" nel testo, ma la topologia stessa (l'indirizzo del server è già pubblico).
- **Punto 3** (client → internet:443): masquerade/SNAT classico in uscita — il client privato deve
  uscire con l'indirizzo pubblico del router sull'interfaccia Internet (`137.204.1.15`).
- **Punto 4** (client → router:53, DNS): il Router stesso è server DNS → INPUT/OUTPUT locale sul
  Router, nessun forwarding.

### `ipt-router.sh` — soluzione ufficiale

```
1. accesso da parte dei client alla porta TCP 993 del server

iptables -t nat -A POSTROUTING -s 172.20.0.0/20 -d 1.1.1.14 -j SNAT --to-source 1.1.1.1
iptables -A FORWARD -p tcp -s 172.20.0.0/20 -d 1.1.1.14 -i eth1 -o eth2 --dport 993 -j ACCEPT
iptables -A FORWARD -p tcp -s 1.1.1.14 -d 1.1.1.1 -i eth2 -o eth1 --sport 993 -m state --state ESTABLISHED -j ACCEPT

2. accesso da parte di qualsiasi host su internet alla porta TCP 25 del server

iptables -A FORWARD -p tcp -i eth3 -o eth2 -d 1.1.1.14 --dport 25 -j ACCEPT
iptables -A FORWARD -p tcp -i eth2 -o eth3 -s 1.1.1.14 --sport 25 -m state --state ESTABLISHED -j ACCEPT

3. navigazione sicura dei client sul web (internet, porta TCP 443)

iptables -t nat -A POSTROUTING -s 172.20.0.0/20 -i eth1 -o eth3 --to-source 137.204.1.15
iptables -A FORWARD -p tcp -s 172.20.0.0/20 -i eth1 -o eth3 --dport 443 -j ACCEPT
iptables -A FORWARD -p tcp -d 137.204.1.15 -i eth3 -o eth1 --sport 443 -m state --state ESTABLISHED -j ACCEPT

4. accesso da parte dei client alla porta UDP 53 del router

iptables -A INPUT -p udp -s 172.20.0.0/20 -i eth1 --dport 53 -j ACCEPT
iptables -A OUTPUT -p udp -d 172.20.0.0/20 -o eth1 --sport 53 -m state --state ESTABLISHED -j ACCEPT
```

### `ipt-server.sh` — soluzione ufficiale

```
1. accesso da parte dei client alla porta TCP 993 del server

iptables -A INPUT -p tcp -s 1.1.1.1 -i eth1 --dport 993 -j ACCEPT
iptables -A OUTPUT -p tcp -d 1.1.1.1 -o eth1 --sport 993 -m state --state ESTABLISHED -j ACCEPT

2. accesso da parte di qualsiasi host su internet alla porta TCP 25 del server

iptables -A INPUT -p tcp -i eth1 --dport 25 -j ACCEPT
iptables -A OUTPUT -p tcp -o eth1 --sport 25 -m state --state ESTABLISHED -j ACCEPT
```

### Perché funziona

**Il Server vede come sorgente `1.1.1.1` (il Router), non l'IP reale del client, per il punto 1.**
È l'effetto diretto del SNAT sul Router: dopo la traduzione, il pacchetto che arriva al Server ha
sorgente `1.1.1.1`. Per questo `ipt-server.sh` filtra `-s 1.1.1.1` e non un range di client — il
Server, dietro un NAT, **non vede mai gli indirizzi originali**: i suoi filtri vanno scritti pensando
a come appare il pacchetto *dopo* la traduzione, esattamente come nel caso del 12 gennaio 2026 (più
avanti) con il DNAT del server pubblicato indirettamente. È lo stesso principio applicato al lato
opposto della connessione (qui è la sorgente ad essere tradotta, lì la destinazione).

**Il punto 2 (SMTP) non ha SNAT/DNAT sul Router**: l'IP del server è già instradabile pubblicamente,
quindi non serve alcuna traduzione — il Router fa da semplice inoltro (FORWARD). Il Server vede
davvero l'IP del mittente originale (nessuna restrizione `-s` in `ipt-server.sh` per questo punto,
coerente con "qualsiasi host di Internet").

### ⚠️ Gotcha 1 — SNAT senza `-j SNAT` nel punto 3

```
iptables -t nat -A POSTROUTING -s 172.20.0.0/20 -i eth1 -o eth3 --to-source 137.204.1.15
```
Confrontala con la riga SNAT corretta del punto 1 (`... -j SNAT --to-source 1.1.1.1`): qui manca
**`-j SNAT`** prima di `--to-source`. Senza il target esplicito, `--to-source` è un'opzione del
modulo `SNAT` che non viene caricato — `iptables` la rifiuterebbe come opzione non riconosciuta al
momento del caricamento della regola. Versione corretta per intento (mia correzione, non del
docente):
```
iptables -t nat -A POSTROUTING -s 172.20.0.0/20 -i eth1 -o eth3 -j SNAT --to-source 137.204.1.15
```

### ⚠️ Gotcha 2 — nessuna policy/flush esplicita in questa soluzione

A differenza di tutti gli altri casi di questo file, né `ipt-router.sh` né `ipt-server.sh` mostrano
`iptables -F` o `iptables -P ... DROP` — solo le regole ACCEPT/SNAT/FORWARD dei quattro punti. Non
è detto sia un errore (l'esercizio potrebbe assumere chain già vuote/default-drop da un setup
comune del laboratorio), ma **non affidarti a questa omissione il giorno dell'esame**: se la
consegna non dice esplicitamente che le policy di default sono già impostate, aggiungi comunque tu
il flush iniziale e le policy DROP finali, come fanno tutte le altre soluzioni ufficiali di questo
pool.

**Sintassi**: `iptables` legacy — ultimo esercizio del pool prima del passaggio a `nftables` (il
caso successivo, 10 luglio 2025, è il primo etichettato esplicitamente "(NFTables)").

---

## Caso 5 — 10 luglio 2025, NFTables (Bastion/ALG, Router)

### Consegna originale

> In figura è rappresentata un'architettura firewall in cui il Server viene reso accessibile
> **indirettamente**, attraverso un application level gateway (ALG) installato sul **Bastion**.
> L'unico traffico consentito è quello delle connessioni da Internet verso il Server, che quindi
> prevedono una connessione da Internet alla porta **8443** del Bastion, a cui segue (se l'ALG lo
> consente) una connessione dal Bastion alla porta **443** del Server.
> Le reti lato Bastion (`172.18.0.0/29`) e lato Server (`172.16.1.0/28`) sono **private**, ma
> comunque il **Router è il default gateway** per le macchine di entrambe le reti.
>
> Consegnate: un file **`bastion.nft`** con la configurazione nftables del packet filter del
> Bastion; un file **`router.nft`** con la configurazione nftables del packet filter del router.

Topologia (dal disegno originale):
```
Bastion (eth1: 172.18.0.2) ---- Rete 172.18.0.0/29 ---- eth1(172.18.0.1) [R: eth1,eth2] eth2(172.16.1.1) ---- Rete 172.16.1.0/28 ---- eth1(172.16.1.2) [Server]
                                                              eth3 (130.136.77.88)
                                                                |
                                                            Internet
```

### Come ragionare

- **Il Bastion non è un router**: ha **una sola interfaccia** (`eth1`) verso tutto il resto (sia
  Internet sia Server, entrambi raggiunti attraverso il Router, che è il suo default gateway). Non
  può quindi distinguere "traffico da Internet" da "traffico dal Server" con `-i`/`-o` (ne ha una
  sola) — deve farlo per **indirizzo**: qualunque cosa non provenga dalle due reti private note è
  "da fuori".
- **L'ALG termina davvero la connessione, non la inoltra passivamente**: sulla 8443 il Bastion è
  **server** (INPUT, riceve connessioni nuove); verso il Server sulla 443 il Bastion è **client**
  (OUTPUT, apre lui una connessione nuova se l'ALG decide di proseguire). Per questo il Bastion non
  ha bisogno di una catena `FORWARD` funzionante — è dichiarata ma vuota, con un commento esplicito
  ("bastion non è un router") proprio per rendere visibile che non inoltra nulla.
- **Il Router fa DNAT** (Internet → `130.136.77.88:8443` diventa `172.18.0.2:8443`) e **FORWARD**
  per entrambi i segmenti che attraversa (Internet↔Bastion, Bastion↔Server). **Nessun SNAT**: la
  consegna dice esplicitamente che il Router è il gateway di default di entrambe le reti private —
  chi riceve un pacchetto da un indirizzo "sconosciuto" lo rispedirà comunque al proprio gateway di
  default, che sa esattamente dove trovare quella rete. Mascherare la sorgente sarebbe qui
  superfluo (lo dice anche un commento nella soluzione ufficiale).

### `router.nft` — soluzione ufficiale

```
flush chain filter INPUT
flush chain filter OUTPUT
flush chain filter FORWARD
flush chain nat PREROUTING
flush chain nat POSTROUTING

# nota: poichè è detto esplicitamente che router è il default gateway delle due reti private, e i pacchetti sono smistati solo dal router in figura, non è necessario mascherare gli indirizzi sorgente (chi riceve i pacchetti li manderà al default gateway in quanto provenienti da una rete "sconosciuta", ma il default gateway sa precisamente dove trovarla)

table ip nat {

	# fa eccezione ovviamente Internet, che non ha instradamento verso la rete privata del bastion host
	# quindi sarà il router a ricevere i pacchetti e dovrà modificarne la destinazione

	chain PREROUTING {
		type nat hook prerouting priority dstnat;
		iif eth3 ip daddr 130.136.77.88 tcp dport 8443 dnat to 172.18.0.2
	}
}

table ip filter {

	chain INPUT {
		# default comuni: tutto drop tranne loopback
		type filter hook input priority filter; policy drop;
		iif lo accept
	}

	chain OUTPUT {
		# default comuni: tutto drop tranne loopback
		type filter hook output priority filter; policy drop;
		oif lo accept
	}

	chain FORWARD {
		# default comuni: tutto drop
		type filter hook forward priority filter; policy drop;

		# movimento bidirezionale di pacchetti internet <--> bastion
		# nuovi da internet verso il bastion (già con ip giusto, prerouting è prima di forward)

		iif eth3 oif eth1 ip daddr 172.18.0.2 tcp dport 8443 accept
		iif eth1 oif eth3 ip saddr 172.18.0.2 tcp sport 8443 ct state established accept

		# movimento bidirezionale di pacchetti bastion <--> server
		# nuovi da bastion verso server

		iif eth1 oif eth2 ip saddr 172.18.0.2 ip daddr 172.16.1.2 tcp dport 443 accept
		iif eth2 oif eth1 ip daddr 172.18.0.2 ip saddr 172.16.1.2 tcp sport 443 ct state established accept

	}

}
```

### `bastion.nft` — soluzione ufficiale

```
flush chain filter INPUT
flush chain filter OUTPUT
flush chain filter FORWARD


table ip filter {

	chain INPUT {
		# default comuni: tutto drop tranne loopback
		type filter hook input priority filter; policy drop;
		iif lo accept

		# bastion riceve pacchetti nuovi da internet  sulla porta 8443
		iif eth1 ip saddr != {172.18.0.0/29, 172.16.1.0/28} ip daddr 172.18.0.2 tcp dport 8443 accept

		# bastion riceve pacchetti DI RISPOSTA dal server dalla porta 443
		iif eth1 ip saddr 172.16.1.2 ip daddr 172.18.0.2 tcp sport 443 ct state established accept
	}

	chain OUTPUT {
		# default comuni: tutto drop tranne loopback
		type filter hook output priority filter; policy drop;
		oif lo accept

		# bastion emette pacchetti DI RISPOSTA verso internet dalla porta 8443
		oif eth1 ip daddr != {172.18.0.0/29, 172.16.1.0/28} ip saddr 172.18.0.2 tcp sport 8443 ct state established accept

		# bastion emette pacchetti nuovi verso il server alla porta 443
		oif eth1 ip daddr 172.16.1.2 ip saddr 172.18.0.2 tcp dport 443 accept
	}

	chain FORWARD {
		# bastion non è un router
		type filter hook forward priority filter; policy drop;
	}

}

# nota: poichè è detto esplicitamente che router è il default gateway delle due reti private, e i pacchetti sono smistati solo dal router in figura, non è necessario mascherare gli indirizzi sorgente (chi riceve i pacchetti li manderà al default gateway in quanto provenienti da una rete "sconosciuta", ma il default gateway sa precisamente dove trovarla)
```

### Perché funziona

**`ip saddr != {172.18.0.0/29, 172.16.1.0/28}`** è l'idioma chiave di questo esercizio: un
**insieme anonimo** (`{...}`) con **negazione** (`!=`). Si legge "l'indirizzo sorgente non è in
nessuna di queste due reti private" = "viene da fuori, cioè da Internet". È la soluzione
nftables al problema del Bastion single-homed: dove un router vero userebbe interfacce diverse per
distinguere i segmenti, un host con un solo collegamento fisico deve farlo leggendo l'indirizzo.
Ritroverai lo stesso idioma nel caso successivo (30 ottobre 2025).

**`table ip nat` con catena `PREROUTING`, `type nat hook prerouting priority dstnat`**: a
differenza di `iptables` (dove `nat`/`PREROUTING` esistono già), in `nftables` dichiari tu tabella,
tipo, hook e priorità. `prerouting` agisce **prima** della decisione di instradamento — necessario
per il DNAT, che deve cambiare la destinazione **prima** che il kernel decida dove instradare il
pacchetto.

**Le regole `FORWARD` sul Router guardano `172.18.0.2` (l'IP del Bastion), non `130.136.77.88`
(l'IP pubblico)**: perché `prerouting` (hook `dstnat`) accade **prima** di `forward` nel percorso
del pacchetto — quando il filtro in `FORWARD` esamina il pacchetto, il DNAT lo ha già tradotto.
Stesso principio già visto nel caso del 12 gennaio 2026: scrivi il filtro pensando a come appare il
pacchetto **dopo** che `prerouting` lo ha già modificato.

**Nessun `policy accept;`/`policy drop;` esplicito sulla catena NAT `PREROUTING`**: in nftables, se
ometti la policy di una catena base, il default è `accept` — qui non è un errore (le catene NAT
traducono soltanto, non giudicano il destino finale del pacchetto: quello lo decide `FORWARD`), ma
è comunque buona pratica scriverla esplicitamente per chiarezza. Tienilo a mente come confronto: nel
caso successivo (30 ottobre 2025) trovi un errore reale nella tabella NAT, non solo un'omissione di
stile — la differenza tra i due sarà più chiara mettendoli a confronto.

**Sintassi**: `nftables` — primo esercizio del pool esplicitamente in questa sintassi (l'etichetta
"(NFTables)" nel titolo lo conferma). **Gotcha**: nessun refuso di sostanza rilevato in questo caso.

---

## Caso 6 — 30 ottobre 2025 (NFTables, Router + Webserver + DB)

### Consegna originale

> Si consideri la rete in figura.
> Il webserver, collocato su rete privata, deve:
> - essere raggiungibile attraverso il Router R da Internet sulla porta **TCP/443**
> - poter interrogare i DNS pubblici su Internet
> - potersi connettere al DB server, sul quale Postgres è in ascolto sulla porta **TCP/5432**
>
> Si consegnino un file **`router.nft`** con la configurazione nftables del Router R e un file
> **`webserver.nft`** con la configurazione nftables del webserver, che consentano le interazioni
> sopra descritte, e null'altro oltre al traffico indispensabile al funzionamento degli host.

Topologia (dal disegno originale):
```
Internet ---- eth2(130.136.129.54) [R] eth1(172.28.1.1) ---- Rete 172.28.1.0/24 ---- eth1(172.28.1.9) [webserver] eth2(10.0.115.9) ---- Rete 10.0.115.0/24 ---- eth1(10.0.115.6) [DB server]
```
**Nessun `dbserver.nft` richiesto** — come nel caso 5, la consegna limita esplicitamente il numero
di host da configurare.

### Come ragionare

Il webserver ha **due interfacce fisiche** (a differenza del Bastion del caso 5, che ne aveva una
sola): `eth1` verso il Router (e, attraverso di lui, verso Internet) ed `eth2` — un collegamento
**dedicato** — verso il DB server. Questo cambia il ragionamento su `eth2` (dove basta un match
diretto sull'unico peer noto, `10.0.115.6`, senza bisogno di set/negazione) ma non su `eth1`, dove
il webserver è comunque "single-homed verso l'esterno": la stessa interfaccia porta sia il traffico
locale al Router sia quello che il Router continua a inoltrare verso/da Internet, quindi serve di
nuovo l'idioma `ip saddr/daddr != {reti private}` per distinguere "da Internet" da "dalla propria
rete".

- **HTTPS da Internet**: DNAT sul Router (l'IP pubblico `130.136.129.54:443` diventa
  `172.28.1.9:443`); FORWARD sul Router; INPUT/OUTPUT locale sul webserver.
- **DNS del webserver verso Internet**: il webserver ha IP privato, non instradabile su Internet →
  serve SNAT sul Router in uscita (`snat to 130.136.129.54`); FORWARD sul Router; OUTPUT/INPUT
  locale sul webserver.
- **Postgres verso il DB server**: nessun NAT (collegamento dedicato, privato, solo tra webserver e
  DB) — il webserver è **client** (OUTPUT `dport 5432` + INPUT established), il Router non è
  coinvolto (traffico che non lo attraversa nemmeno, è sul link diretto webserver↔DB... nella
  topologia reale il Router non ha interfaccia su quella rete, quindi non compare in `router.nft`
  per questo punto).

### `webserver.nft` — soluzione ufficiale

```
flush ruleset

table filter{
	chain forward{
		type filter hook forward priority filter; policy drop;
	}

	chain input{
		type filter hook input priority filter; policy drop;
		iif lo accept;

		iif eth2 ip saddr 10.0.115.6 tcp sport 5432 ct state established accept

		iif eth1 ip saddr !{172.28.1.0/24, 10.0.115.0/24} tcp dport 443 accept
		iif eth1 ip saddr !{172.28.1.0/24, 10.0.115.0/24} udp sport 53 ct state established accept
	}

	chain output{
		type filter hook output priority filter; policy drop;
		oif lo accept;

		oif eth2 ip daddr 10.0.115.6 tcp dport 5432 accept

		oif eth1 ip daddr !{172.28.1.0/24, 10.0.115.0/24} tcp sport 443 ct state established accept
		oif eth1 ip daddr !{172.28.1.0/24, 10.0.115.0/24} udp dport 53 accept
	}
}
```

### `router.nft` — soluzione ufficiale

```
flush ruleset

table filter{
	chain forward{
		type filter hook forward priority filter; policy drop;

		iif eth2 oif eth1 ip saddr !{172.28.1.0/24, 10.0.115.0/24} ip daddr 172.28.1.9 tcp dport 443 accept
		iif eth1 oif eth2 ip daddr !{172.28.1.0/24, 10.0.115.0/24} ip saddr 172.28.1.9 tcp sport 443 ct state established accept

		iif eth1 oif eth2 ip daddr !{172.28.1.0/24, 10.0.115.0/24} ip saddr 172.28.1.9 udp dport 53 accept
		iif eth2 oif eth1 ip saddr !{172.28.1.0/24, 10.0.115.0/24} ip daddr 172.28.1.9 udp sport 53 ct state established accept
	}

	chain input{
		type filter hook input priority filter; policy drop;
		iif lo accept;
	}

	chain output{
		type filter hook output priority filter; policy drop;
		oif lo accept;
	}
}

table nat{
	chain prerouting{
		type filter hook prerouting priority nat; policy drop;
		iif eth2 oif eth1 ip daddr 130.136.129.54 tcp dport 443 dnat to 172.28.1.9
	}

	chain postrouting{
		type filter hook postrouting priority nat; policy drop;
		iif eth1 oif eth2 ip saddr 172.28.1.9 ip daddr !{172.28.1.0/24, 10.0.115.0/24} udp dport 53 snat to 130.136.129.54
	}
}
```

### Perché funziona

Stesso principio del caso 5 per `ip saddr/daddr != {...}` (distinguere "da/verso Internet" quando
un host è single-homed verso l'esterno), e stesso principio del 12 gennaio 2026 per il fatto che le
regole `forward` sul Router guardano l'indirizzo **dopo** il DNAT (`172.28.1.9`, non
`130.136.129.54`) perché `prerouting` precede `forward` nel percorso del pacchetto.

Da notare un dettaglio interessante nella direzione delle regole `forward` per il DNS: la richiesta
del webserver esce con `iif eth1 oif eth2` (entra dal lato webserver, esce verso Internet) e la
risposta rientra con `iif eth2 oif eth1` — le interfacce del Router in questo esercizio sono:
`eth1` verso il webserver (rete `172.28.1.0/24`), `eth2` verso Internet. Verificalo sempre contro il
disegno prima di scrivere `-i`/`-o` o `iif`/`oif`: invertirle è l'errore più facile da fare e più
difficile da notare rileggendo, perché la regola resta sintatticamente valida — semplicemente non
farà mai match.

### ⚠️ Gotcha — sintassi NAT probabilmente errata nella tabella `nat`

```
table nat{
	chain prerouting{
		type filter hook prerouting priority nat; policy drop;
		...
		dnat to 172.28.1.9
	}
	chain postrouting{
		type filter hook postrouting priority nat; policy drop;
		...
		snat to 130.136.129.54
	}
}
```
Confrontata con l'altro esercizio di questo pool in nftables (10 luglio 2025, caso 5), che scrive
correttamente `type nat hook prerouting priority dstnat;`, questa tabella ha **due problemi
cumulativi** secondo la sintassi standard di nftables:
1. **`type filter` invece di `type nat`**: gli statement `dnat to`/`snat to` sono validi solo dentro
   catene dichiarate di tipo `nat` — dentro una catena `type filter`, `nft -c -f` dovrebbe rifiutarli
   con un errore ("you must specify a table of type nat" o simile).
2. **`priority nat`**: non è un nome di priorità valido per gli hook `prerouting`/`postrouting` —
   quelli standard sono **`dstnat`** (prerouting, valore -100) e **`srcnat`** (postrouting, valore
   100). `nat` come identificatore letterale di priorità non è tra quelli riconosciuti.

`policy drop;` su una catena NAT è inoltre concettualmente insolito (le catene NAT traducono, non
giudicano il destino finale del pacchetto — quello lo fa `filter`/`forward`) — non è di per sé un
errore quanto i primi due punti, ma rinforza l'impressione che questa tabella sia stata scritta
riadattando in fretta un template pensato per `type filter`, senza cambiare `type`/`priority`.

⚠️ Non è stato possibile verificare con `nft -c -f` (binario non disponibile in questo ambiente) —
ma la sintassi contraddice sia la documentazione nftables sia l'altro esercizio in nftables di
questo stesso pool. Trattala con sospetto: se ti ricapita questo pattern, riscrivi con
```
chain prerouting { type nat hook prerouting priority dstnat; ... }
chain postrouting { type nat hook postrouting priority srcnat; ... }
```
e verifica con `nft -c -f nomefile.nft` prima di fidartene alla lettera (questa riscrittura è una
mia correzione di intento, non fa parte del testo ufficiale).

**Sintassi**: `nftables`.

---

## Caso 7 — 12 gennaio 2026 (NFTables, NAT + pubblicazione indiretta)

> Stessa giornata d'esame di `trace-2026-01-12.pcapng` in NIDS e dell'esercizio AIDE in
> Integrity/privesc. Soluzione ufficiale recuperata dall'allegato "Soluzione" nascosto nella pagina
> (tarball `nft_20260112`: `client.nft`, `router.nft`, `server.nft`, nessun report scritto
> richiesto per questo esercizio).

### Consegna originale

Topologia:
```
CLIENT (rete privata 10.20.0.0/22) ---- eth1 [ROUTER] eth2 ---- SERVER (192.168.1.7, rete privata)
                                          eth3 (130.136.1.1, pubblico)
                                            |
                                        Internet
```
Le reti private **non sono instradate automaticamente** nemmeno tra loro; le reti pubbliche
(Internet inclusa) sono raggiungibili dalle altre. Uniche interazioni consentite:
1. accesso **(necessariamente indiretto)** da Internet al server in **HTTPS (TCP/443)**
2. accesso di tutti i client a Internet per **query DNS (UDP/53)**

Consegna: `client.nft`, `router.nft`, `server.nft` (un file per host).

### Perché qui serve anche il NAT, non solo il filtro

Differenza chiave rispetto ai casi puramente di filtro: la parola "**indiretto**" nella consegna è
la chiave — il server ha un IP **privato** (`192.168.1.7`), quindi Internet non può indirizzarlo
direttamente: serve **pubblicare** il servizio dietro l'IP pubblico del router (`130.136.1.1`) e
lasciare che sia il router a tradurre. Stesso discorso all'inverso per i client: escono con un IP
privato non instradabile su Internet, quindi il router deve **mascherarli** dietro il proprio IP
pubblico.

### `router.nft` — NAT + filtro insieme

```nft
table ip nat {
    chain prerouting {
        type nat hook prerouting priority dstnat; policy accept;
        # Pubblicazione indiretta del server HTTPS:
        # Internet -> 130.136.1.1:443 viene tradotto verso 192.168.1.7:443.
        iif eth3 ip daddr 130.136.1.1 tcp dport 443 dnat to 192.168.1.7:443
    }
    chain postrouting {
        type nat hook postrouting priority srcnat; policy accept;
        # I client privati possono uscire su Internet solo per DNS UDP.
        oif eth3 ip saddr 10.20.0.0/22 udp dport 53 snat to 130.136.1.1
    }
}

table inet filter {
    chain forward {
        type filter hook forward priority filter; policy drop;
        iif eth1 oif eth3 ip saddr 10.20.0.0/22 udp dport 53 accept
        oif eth1 iif eth3 ip daddr 10.20.0.0/22 udp sport 53 ct state established accept
        iif eth3 oif eth2 ip daddr 192.168.1.7 tcp dport 443 accept
        oif eth3 iif eth2 ip saddr 192.168.1.7 tcp sport 443 ct state established accept
    }
    chain input { type filter hook input priority filter; policy drop; iif "lo" accept }
    chain output { type filter hook output priority filter; policy drop; oif "lo" accept }
}
```

**Cosa fa ciascun pezzo, meccanismo + visione:**
- **`table ip nat` con due catene, `prerouting` e `postrouting`**: in nftables (a differenza di
  iptables, dove le catene NAT built-in esistono già) devi dichiarare tu la catena, il suo `hook`
  (a quale punto del percorso del pacchetto si aggancia) e la sua `priority`. `prerouting` agisce
  **prima** che il kernel decida come instradare il pacchetto (giusto per il DNAT: bisogna cambiare
  la destinazione *prima* di instradare) — `postrouting` agisce **dopo**, quando il pacchetto sta
  per uscire (giusto per il SNAT: si riscrive la sorgente solo all'ultimo, dopo che tutto il resto
  del filtraggio/instradamento è già stato deciso). Nota qui il contrasto coi due gotcha già visti:
  questa catena scrive correttamente `type nat hook ... priority dstnat/srcnat`, esattamente lo
  schema che manca nel caso 6.
- **`dnat to 192.168.1.7:443`**: chiunque su Internet contatti `130.136.1.1:443`, il router riscrive
  la destinazione nel pacchetto con l'IP privato reale del server — è la "pubblicazione indiretta"
  richiesta dal testo: dall'esterno si vede solo l'IP pubblico del router, mai quello del server.
- **`snat to 130.136.1.1`**: i pacchetti DNS in uscita dai client (IP sorgente `10.20.0.0/22`, non
  instradabile su Internet) vengono riscritti con l'IP pubblico del router come sorgente — è
  l'equivalente concettuale del `MASQUERADE` di iptables, ma con IP fisso invece che "usa
  l'IP dell'interfaccia in quel momento".
- **`table inet filter`, chain `forward`**: qui il filtro vero e proprio, stessa logica sempre
  ribadita in questo file (chi attraversa il router va in `forward`, non `input`/`output`) — nota
  che le regole guardano `ip daddr 192.168.1.7` (l'IP **dopo** il DNAT, non l'IP pubblico): il
  filtro va scritto pensando a come appare il pacchetto **dopo** che `prerouting` lo ha già tradotto,
  perché `prerouting` (hook `dstnat`) accade prima di `forward` nel percorso del pacchetto — lo
  stesso principio ritrovato nei casi 5 e 6.
- **`define NET_CLIENTS`/`SERVER_IP`/`PUBLIC_IP`** in cima al file originale: variabili nominate
  (analogo del `$GOOD_NET` visto in Suricata) — non usate nelle righe finali di questa trascrizione
  ma dichiarate per readability, sostituiscile ai valori letterali se vuoi un file più leggibile.

### `client.nft` e `server.nft` — solo filtro, nessun NAT

I due host finali non fanno traduzione (non sono il router), solo `input`/`output` locali:
```nft
# client.nft (estratto)
chain output {
    type filter hook output priority filter; policy drop;
    oif "lo" accept
    oif eth1 ip daddr != 10.20.0.0/22 udp dport 53 accept   # query DNS verso l'esterno
}
```
```nft
# server.nft (estratto)
chain input {
    type filter hook input priority filter; policy drop;
    iifname "lo" accept
    # Dopo il DNAT del router la destinazione locale e' 192.168.1.7,
    # ma la sorgente rimane l'host pubblico esterno originale.
    iif eth1 ip saddr != 192.168.1.0/28 tcp dport 443 accept
}
```
Punto sottile su `server.nft`: il server non sa (né deve sapere) dell'IP pubblico del router — vede
arrivare il traffico già tradotto dal DNAT, con sorgente ancora l'IP pubblico originale del client
Internet (il **DNAT cambia solo la destinazione**, mai la sorgente) — per questo la regola filtra
`ip saddr != 192.168.1.0/28` (accetta tutto ciò che non viene dalla propria rete locale), non un
IP specifico: dal punto di vista del server, "chiunque da fuori la mia rete" è la definizione
corretta di "traffico da Internet", il router si è già occupato di instradarlo correttamente.

> ⚠️ Riga sospetta nel file originale del prof, trascritta fedelmente: `client.nft` ha
> `... ct state established :accept` (con `:` prima di `accept`) — sintassi che non risulta valida
> in nftables standard. Probabile refuso nel file consegnato dal prof stesso; se lo riusi come
> riferimento, verifica con `nft -c -f client.nft` (check di sintassi senza applicare) prima di
> fidartene alla lettera.

**Sintassi**: `nftables`.

---

## Indice riassuntivo

| Data | Host richiesti | Sintassi | NAT? | Soluzione | Gotcha principali |
|---|---|---|---|---|---|
| 11 giu 2021 | 1 (host singolo/router) | iptables | no | ufficiale | `FORWARD` default ACCEPT dedotto dal testo |
| 13 set 2023 | 3 (Client/Router/Server) | iptables | sì | ufficiale (ritrovata 15/07/2026) | porta NTP 1233→123 nel testo; SNAT/DNAT invertiti; protocollo sbagliato su una SNAT |
| 8 feb 2024 | 1 (solo Router) | iptables | no | ufficiale | dipende da esercizio NIDS collegato per la topologia; NTP dport=sport=123 |
| 13 giu 2024 | 2 (Router, Server) | iptables | sì | ufficiale | SNAT senza `-j SNAT`; nessuna policy/flush esplicita |
| 10 lug 2025 | 2 (Bastion, Router) | nftables | sì (solo DNAT) | ufficiale | nessuno di sostanza — primo caso nftables del pool |
| 30 ott 2025 | 2 (Router, Webserver) | nftables | sì | ufficiale | `type filter`/`priority nat` invece di `type nat`/`dstnat`/`srcnat` |
| 12 gen 2026 | 3 (Client/Router/Server) | nftables | sì | ufficiale | `ct state established :accept` (refuso `:` sospetto) |

Per l'algoritmo generale da applicare a qualunque variante il giorno dell'esame, vedi
`procedura_operativa_iptables.md`; per il documento di riferimento rapido da aprire per primo,
`guida_esame_iptables.md`.
