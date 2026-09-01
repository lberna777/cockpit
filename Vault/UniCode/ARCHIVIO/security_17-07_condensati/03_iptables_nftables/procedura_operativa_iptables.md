# Procedura Operativa — Iptables/NFTables

> Algoritmo esteso passo-passo per qualunque esercizio di questa famiglia (regole di filtraggio, e
> talvolta NAT, per una topologia di rete multi-host). Non contiene teoria di base sul networking —
> solo l'algoritmo operativo e la sintassi comparata. Per il triage rapido e i rami per scenario
> vedi `guida_esame_iptables.md`; per 7 esempi completi già risolti (tutti con soluzione ufficiale
> del docente), `modello_iptables_nftables.md`.

> ⚠️ **Regola d'oro: il file di consegna richiesto (`iptables.txt`, `ipt.sh`, `*.nft`...) è quasi
> sempre l'unico deliverable — non ci sono screenshot o report da scrivere in questa tipologia,**
> a differenza di privesc/NIDS. Verifica comunque la consegna specifica: se dovesse chiedere
> qualcos'altro (è raro nel pool ma non impossibile), segnalalo, non inventare un formato.

---

## 0. Prima di scrivere qualunque regola

- [ ] **Leggi tutta la consegna prima di scrivere la prima riga.** Il pool premia esplicitamente
  questo comportamento: l'11 giugno 2021 lo dice testualmente ("si consiglia di leggere prima tutta
  la lista"), perché un punto successivo (l'ordine delle regole, o un'esclusione) cambia come vanno
  scritti i punti precedenti.
- [ ] **Identifica quanti file/host la consegna chiede davvero.** Non è sempre "un file per ogni
  host della topologia": alcuni esercizi chiedono solo il Router (8 feb 2024), altri Router+Server
  senza il Client (13 giu 2024), altri ancora ogni host coinvolto (13 set 2023, 12 gen 2026). Conta
  i nomi di file richiesti nel testo, non presumerli dal disegno.
- [ ] **Identifica la sintassi richiesta**: `iptables` (legacy) o `nftables`. Nel pool osservato,
  gli esercizi fino al 13 giugno 2024 sono in `iptables`; dal 10 luglio 2025 in poi sono tutti in
  `nftables` — ma non affidarti solo alla data, la consegna/l'estensione del file richiesto
  (`.sh`/`.txt` vs `.nft`) lo dice sempre esplicitamente.
- [ ] **Individua se serve NAT** (vedi §2) prima di iniziare a scrivere le regole di filtro — cambia
  la struttura del file (tabella/catena NAT separata) e a volte l'indirizzo da usare nei match del
  filtro (vedi §2, "matcha l'indirizzo dopo la traduzione").

---

## 0.5 Da dove viene ogni pezzo di una regola (le tre fonti)

Prima di scrivere qualunque riga, sappi che ogni regola si **assembla** pescando informazioni da
tre posti distinti, sempre gli stessi. Sapere *quale fonte* dà *quale pezzo* elimina il "dove lo
trovo?" da ogni esercizio: niente in una regola è "da indovinare".

| Pezzo della regola | Da dove si legge |
|---|---|
| protocollo (`-p tcp/udp`) | **consegna (testo)** — il servizio nominato o la porta ("porta TCP 443", "UDP 53") |
| numero di porta (`--dport`/`--sport`) | **consegna (testo)** — esplicito, o porta standard del servizio nominato (SSH 22, DNS 53, SMTP 25, IMAPS 993...) |
| chi parla con chi, concettualmente | **consegna (testo)** — "il client accede a...", "il server è raggiungibile da..." |
| nome esatto delle interfacce (`-i`/`-o`) | **disegno (topologia)** — mai inventato, **mai preso da un altro host** (vedi §1, i nomi `eth*` sono locali a ciascuna macchina) |
| quante interfacce ha l'host, quale rete/IP sta dietro ciascuna | **disegno (topologia)** |
| indirizzo/rete da matchare (`-s`/`-d`) | **disegno (topologia)** — gli IP e le subnet scritti accanto agli host |
| ogni interazione = **2 righe** (richiesta + risposta) | **metodo fisso** — sempre, mai da "cercare" |
| `--dport` sulla richiesta / `--sport` sulla risposta | **metodo fisso** — automatico dalla direzione, il numero di porta è lo stesso (cambia solo quale flag lo tiene) |
| `-m state --state ESTABLISHED` **solo** sulla risposta | **metodo fisso** — mai sulla richiesta |
| `-j ACCEPT` come target | **metodo fisso** — quasi sempre; la policy `DROP` di default fa il resto |

**Il punto pratico**: protocollo/porta/chi-con-chi li **detta la consegna**; interfacce/reti/indirizzi
li **detta il disegno**; la struttura (2 righe, dport-richiesta/sport-risposta, ESTABLISHED sulla
risposta, ACCEPT) è **sempre identica** e non dipende dall'esercizio. Se ti manca un pezzo mentre
scrivi una riga, sai esattamente in quale delle tre fonti cercarlo — non è mai "creatività".

---

## 1. Leggere la topologia e classificare ogni flusso per ogni host

Per **ogni host** della topologia e **ogni interazione di rete** richiesta dalla consegna, chiediti:
questo host è **sorgente/destinazione finale** del traffico, o lo **attraversa** soltanto?

| L'host è... | Catena | Esempio dal pool |
|---|---|---|
| endpoint che risponde a una richiesta (server di un servizio) | INPUT (richiesta) + OUTPUT (risposta) | Server SMTP riceve da Internet (13 set 2023) |
| endpoint che inizia una richiesta (client di un servizio) | OUTPUT (richiesta) + INPUT (risposta) | Client interroga DNS (tutti i casi) |
| né sorgente né destinazione, il traffico passa da lui | FORWARD (in entrambe le direzioni) | Router tra Client e Internet |
| un solo collegamento fisico verso "tutto il resto" (single-homed dietro un router) | INPUT/OUTPUT, MAI FORWARD, distinzione per indirizzo non per interfaccia | Bastion (10 lug 2025), webserver verso Internet (30 ott 2025) |

**L'errore concettuale più comune del pool**: mettere in `FORWARD` un servizio che gira sull'host
stesso (o viceversa). Non funziona mai, perché quel traffico non passa mai per la catena sbagliata —
verifica sempre "chi risponde effettivamente a questa richiesta?" prima di scegliere la catena.

**Caso speciale — host con un solo link verso l'esterno (Bastion, webserver dietro un router)**:
se un host ha una singola interfaccia che porta sia il traffico locale al proprio segmento sia
quello che continua oltre (verso/da Internet attraverso il router), non puoi distinguere le due
direzioni con `-i`/`-o` — usa un match sull'indirizzo: in nftables, un insieme con negazione
(`ip saddr != {rete1, rete2}` = "non nelle mie reti private note" = "da fuori"); non c'è un
equivalente altrettanto compatto in iptables legacy, andrebbe simulato con più regole `-s`/`! -s`.

---

## 2. Quando serve NAT, e come deciderlo dalla consegna

**Segnali testuali che implicano NAT** (in ordine di forza del segnale):
1. La parola **"indiretto"/"indirettamente"** riferita a un servizio raggiungibile dall'esterno →
   il server ha IP privato, serve **DNAT** per pubblicarlo dietro l'IP pubblico del router (12 gen
   2026, 10 lug 2025, 30 ott 2025 sono tutti così).
2. Un host con **IP privato** deve raggiungere una rete che **non ha instradamento di ritorno**
   verso quella privata (anche senza la parola "indiretto" esplicita) → serve **SNAT/MASQUERADE**
   sul router che fa da confine, altrimenti le risposte non saprebbero tornare (13 giu 2024, punti
   1 e 3: nessuna delle due consegne dice "indiretto", ma la topologia — client su rete privata che
   deve raggiungere un segmento "pubblico" diverso, o Internet — lo richiede comunque).
3. La consegna dice esplicitamente che **le reti private non sono instradate automaticamente**
   nemmeno tra loro (12 gen 2026) → praticamente ogni comunicazione che attraversa il confine
   pubblico/privato richiede NAT in una direzione o nell'altra.

**Quando NON serve NAT**: se l'host di destinazione ha già un indirizzo instradabile pubblicamente
(anche se la consegna lo chiama semplicemente "il server", senza dire "IP pubblico" esplicitamente
— guarda il disegno: se l'indirizzo è del tipo di quelli su Internet/rete dichiarata pubblica, il
FORWARD puro basta, 13 set 2023 punto 2 e 13 giu 2024 punto 2 sono così).

**Discriminante decisivo per il segnale 2 — c'è o no una rotta di ritorno?** Il segnale 2 non è
"sono reti diverse?" ma "**il segmento di destinazione sa come rispedire indietro verso la
sorgente?**". Una rete privata che raggiunge un altro segmento richiede SNAT **solo se quel segmento
non ha rotta di ritorno** verso di lei. Confronta due casi reali del pool, che sembrano simili ma
si decidono in modo opposto:
- **13 giu 2024**: i client privati (`172.20.0.0/20`) raggiungono un server sulla rete "pubblica"
  `1.1.1.0/28`; quel segmento **non ha rotta** verso la rete privata dei client → **serve SNAT**
  (senza, le risposte del server non saprebbero tornare a un IP privato che lì non esiste).
- **10 lug 2025**: Bastion e Server stanno su **due reti private diverse**, eppure **niente SNAT** —
  perché la consegna dice esplicitamente che **il Router è il default gateway di entrambe**: chi
  riceve un pacchetto da una rete "sconosciuta" lo rispedisce al proprio default gateway, che sa
  dove trovarla. La rotta di ritorno esiste, quindi mascherare sarebbe superfluo.

Regola operativa: privato→pubblico/Internet quasi sempre SNAT; privato→privato **dipende** dal fatto
che esista un gateway comune / routing dichiarato che chiuda il giro di ritorno. Leggi la consegna
per capire se quella rotta c'è.

**Regola pratica per non sbagliare la direzione**:
- **DNAT** cambia la **destinazione** — vive in **PREROUTING** (iptables) o in una catena con hook
  `prerouting`/priority `dstnat` (nftables), perché deve agire *prima* che il kernel decida come
  instradare il pacchetto.
- **SNAT/MASQUERADE** cambia la **sorgente** — vive in **POSTROUTING** (iptables) o hook
  `postrouting`/priority `srcnat` (nftables), perché agisce *dopo* che tutto il resto è deciso,
  appena prima che il pacchetto lasci il sistema.
- Occhio all'opzione: `SNAT` accetta solo `--to-source`; `DNAT` accetta solo `--to-destination`.
  Scambiarle (visto realmente nel pool, 13 set 2023) fa fallire il caricamento della regola.

**Conseguenza sul filtro, da non dimenticare mai**: se una catena NAT traduce un indirizzo *prima*
di `FORWARD`/`filter`, le regole di filtro successive devono guardare l'indirizzo **dopo** la
traduzione, non quello originale — es. dopo un DNAT che pubblica un server privato dietro un IP
pubblico, la regola `FORWARD` guarda l'IP **privato reale** del server (perché il DNAT prerouting
è già avvenuto), non l'IP pubblico con cui l'ha contattato Internet. Questo vale anche per l'host
finale (server/webserver): il suo filtro locale vede il pacchetto già tradotto, quindi filtra
sull'indirizzo post-NAT che gli arriva davvero (visto in 3 casi del pool: 12 gen 2026, 13 giu 2024,
30 ott 2025).

**Generalizzazione (vale per SNAT come per DNAT)** — l'host "dall'altra parte" del NAT filtra
**sull'indirizzo come gli arriva davvero**, cioè quello già tradotto:
- dietro un **DNAT**: il server pubblicato vede la propria **destinazione tradotta** (il suo IP
  privato reale) ma la **sorgente originale** del richiedente esterno — il DNAT tocca solo la
  destinazione. (es. 12 gen 2026: `server.nft` accetta `ip saddr != <rete_locale>`, non un IP
  pubblico specifico).
- dietro un **SNAT**: il server contattato vede come **sorgente l'IP del router** su quel segmento,
  non l'IP reale del client — il SNAT tocca solo la sorgente. Quindi se la consegna limita l'accesso
  "dai client", sull'host finale filtri sull'IP **tradotto** del router, non su un range di client
  che non vedrai mai (es. 13 giu 2024: `ipt-server.sh` filtra `-s 1.1.1.1`, l'IP del router, per la
  porta 993).

⚠️ Questo riguarda **solo** i flussi che hanno effettivamente subito NAT. Gli altri flussi verso lo
stesso host **restano come sono**: se un flusso non passa per SNAT/DNAT e la consegna dice "da
qualsiasi host", non aggiungi nessun `-s`/`-d` per quel flusso (sempre 13 giu 2024: SMTP "da
qualsiasi host di Internet" **non** ha SNAT, quindi `ipt-server.sh` non mette alcun `-s` per la
porta 25). Non applicare la restrizione dell'IP tradotto a tappeto su tutte le righe dell'host:
riga per riga, chiediti "questo specifico flusso ha subito NAT?".

### Traccia pacchetto per pacchetto: perché UNA sola riga SNAT basta

Dubbio ricorrente: "ho scritto una riga SNAT per l'andata — e la risposta? non serve una seconda
regola NAT per ritradurre al ritorno?". **No**, e conviene vederlo letteralmente. Esempio 13 giu
2024: client `172.20.0.5` (rete privata) contatta il server `1.1.1.14:993`; il router fa
`-t nat -A POSTROUTING -s 172.20.0.0/20 -d 1.1.1.14 -j SNAT --to-source 1.1.1.1`.

**Senza SNAT — cosa si rompe:**
1. Client manda: `src=172.20.0.5  dst=1.1.1.14`. Il router lo inoltra invariato.
2. Il server riceve `src=172.20.0.5` e prova a rispondere verso `dst=172.20.0.5`. Ma
   `172.20.0.0/20` è una rete **privata non instradabile** dal segmento del server → la risposta non
   sa dove andare, muore lì. Connessione mai completata.

**Con SNAT — passo per passo dell'header:**
1. Client manda: `src=172.20.0.5  dst=1.1.1.14`.
2. Router, in `POSTROUTING` (appena prima di far uscire il pacchetto), **riscrive la sorgente**:
   `src=1.1.1.1  dst=1.1.1.14`. **E annota la traduzione in conntrack** (la tabella di stato del
   kernel): "la connessione 172.20.0.5 ↔ 1.1.1.14:993 sta uscendo mascherata come 1.1.1.1".
3. Il server riceve `src=1.1.1.1` — un indirizzo **del suo stesso segmento pubblico**, raggiungibile.
   Risponde: `src=1.1.1.14  dst=1.1.1.1`.
4. La risposta torna al router. Il router **non ha bisogno di una seconda regola NAT**: conntrack
   riconosce che questo pacchetto appartiene alla connessione annotata al passo 2 e **ritraduce
   automaticamente** la destinazione da `1.1.1.1` a `172.20.0.5`. Il pacchetto arriva al client come
   se nulla fosse successo.

**Da qui ci si fida della singola riga SNAT**: la traduzione di ritorno la fa il **conntrack**, non
una regola che scrivi tu. La tua unica riga SNAT descrive solo l'andata; il ritorno è gestito dallo
stato di connessione. ⚠️ Attenzione a non confondere due meccanismi diversi che convivono: sul
**filtro** (`FORWARD`/`INPUT`) la risposta va comunque abilitata **esplicitamente** con la riga
`-m state --state ESTABLISHED` — ma quello è *filtro*, non *NAT*. Il conntrack serve entrambi (traccia
la connessione), ma la riga ESTABLISHED la scrivi tu, la ritraduzione NAT no.

---

## 3. Pattern fisso: default-drop + loopback

In quasi tutti i casi del pool (unica eccezione nota: 11 giugno 2021, dove `FORWARD` resta
`ACCEPT` per un motivo dedotto dal testo — vedi `modello_iptables_nftables.md` caso 1), lo scheletro
è identico su ogni host:

**iptables:**
```
iptables -F INPUT
iptables -F OUTPUT
iptables -F FORWARD
iptables -t nat -F        # solo se l'host fa NAT

iptables -A INPUT -i lo -j ACCEPT
iptables -A OUTPUT -o lo -j ACCEPT

# ... qui le regole di servizio ...

iptables -P INPUT DROP
iptables -P OUTPUT DROP
iptables -P FORWARD DROP
```

**nftables** (schema minimo, una tabella `inet`/`ip` per famiglia):
```
flush ruleset      # oppure flush chain <tabella> <catena> per catena, se preferisci essere selettivo

table inet filter {
    chain input   { type filter hook input   priority filter; policy drop; iif "lo" accept  ...regole... }
    chain output  { type filter hook output  priority filter; policy drop; oif "lo" accept  ...regole... }
    chain forward { type filter hook forward priority filter; policy drop;                   ...regole... }
}
```

**Perché il default-drop semplifica tutto**: realizza da solo il requisito quasi universale
"qualsiasi altro pacchetto deve essere scartato" — non serve una regola finale di DROP esplicita.
Scrivi **solo** le regole di ciò che deve passare. Le regole di policy vanno **sempre per ultime**
nello script (in iptables la policy si applica comunque indipendentemente dall'ordine di scrittura,
ma per chiarezza e per coerenza con `nft`, mettile in fondo).

**Loopback**: sempre permesso, sempre per primo per convenzione (anche se l'ordine relativo non
conta quando policy e match sono disgiunti — vedi §4 sull'ordine).

---

## 4. Pattern fisso: richiesta/risposta simmetrica

Ogni interazione di rete "vera" (non locale all'host) coinvolge due parti: chi **inizia** la
connessione (client, verso una porta di **destinazione** nota) e chi **risponde** (server, da quella
stessa porta come **sorgente**). Per questo motivo, ogni servizio genera **due righe per ogni host
coinvolto**, mai una sola:

**iptables:**
```
# lato client (chi inizia)
iptables -A OUTPUT -p <proto> --dport <porta> -j ACCEPT
iptables -A INPUT  -p <proto> --sport <porta> -m state --state ESTABLISHED -j ACCEPT

# lato server (chi risponde)
iptables -A INPUT  -p <proto> --dport <porta> -j ACCEPT
iptables -A OUTPUT -p <proto> --sport <porta> -m state --state ESTABLISHED -j ACCEPT
```

**nftables** (equivalente):
```
# lato client
oif <if> <proto> dport <porta> accept
iif <if> <proto> sport <porta> ct state established accept

# lato server
iif <if> <proto> dport <porta> accept
oif <if> <proto> sport <porta> ct state established accept
```

**Perché `ESTABLISHED`/`ct state established` e non aprire anche la porta sorgente in permanenza**:
una regola che matcha solo `--sport <porta>` senza `ESTABLISHED` accetterebbe **qualunque**
pacchetto con quella porta sorgente, anche non in risposta a nulla — un uso improprio che un
attaccante potrebbe sfruttare (spoofing della porta sorgente). Il match sullo stato di connessione
restringe l'accettazione alle sole risposte di connessioni **già avviate legittimamente** da questo
host, tracciate da `conntrack`.

**Eccezione da conoscere: NTP**. A differenza della maggioranza dei servizi (porta client effimera,
porta server nota), NTP usa la porta **123 su entrambi i lati** — quindi la regola FORWARD/router
per NTP ha **sia** `--dport 123` **sia** `--sport 123` nella stessa riga (visto nel caso 8 feb 2024
del modello). Non generalizzare lo schema dport-richiesta/sport-risposta a occhi chiusi: verifica
sempre se il servizio in questione è simmetrico.

**Altri servizi a porte fisse (stesso principio dell'NTP): DHCP**. Anche DHCP non usa porte effimere
lato client — **server sulla 67, client sulla 68**, entrambe fisse (non identiche come NTP, ma
entrambe note). La richiesta ha quindi `--sport 68 --dport 67` e la risposta `--sport 67 --dport 68`,
con **entrambe** le porte esplicite su ogni riga (visto nel caso 8 feb 2024, dove il router è server
DHCP per le tre reti). **Regola pratica**: per DNS/HTTP/HTTPS/SSH/SMTP/IMAPS/... la porta client è
effimera → ometti `--sport` sulla richiesta; per NTP (123/123) e DHCP (67/68) **entrambe** le porte
sono note e vanno scritte su ogni riga.

---

## 5. Cheatsheet sintassi comparata — iptables legacy ↔ nftables

### Struttura del comando

| Concetto | iptables | nftables |
|---|---|---|
| Tabelle/catene predefinite | Sì (`filter`/`nat`/`mangle`/`raw`, `INPUT`/`OUTPUT`/`FORWARD`/...) | **No** — tabella e catena vanno dichiarate esplicitamente |
| Creare una tabella | (implicita) | `table <famiglia> <nome> { ... }` — famiglia tipica: `ip` (solo IPv4), `inet` (IPv4+IPv6) |
| Creare una catena builtin | (implicita) | `chain <nome> { type <tipo> hook <hook> priority <valore>; policy <accept\|drop>; }` |
| Aggiungere una regola | `iptables -A <catena> <match> -j <target>` | scrivi direttamente `<match> <verdetto>` dentro il blocco `chain { }` |
| Svuotare | `iptables -F [<catena>]` | `flush ruleset` (tutto) oppure `flush chain <tabella> <catena>` |
| Policy di default | `iptables -P <catena> <ACCEPT\|DROP>` | `policy accept;`/`policy drop;` dentro la dichiarazione della catena |

### Hook/tipo di catena (dove si aggancia nel percorso del pacchetto)

| Hook (nftables) | Catena equivalente (iptables) | Quando scatta |
|---|---|---|
| `prerouting` | `PREROUTING` | Appena il pacchetto entra, **prima** della decisione di instradamento |
| `input` | `INPUT` | Pacchetto destinato al sistema locale |
| `forward` | `FORWARD` | Pacchetto da inoltrare altrove (non locale) |
| `output` | `OUTPUT` | Pacchetto generato localmente |
| `postrouting` | `POSTROUTING` | Appena prima che il pacchetto lasci il sistema |

Priorità standard per gli hook NAT (nftables): **`dstnat`** per `prerouting` (valore -100),
**`srcnat`** per `postrouting` (valore 100). Per `filter`/`forward`/`input`/`output` la priorità
tipica è `filter` (valore 0). ⚠️ Un errore reale visto nel pool (30 ottobre 2025): scrivere
`type filter hook prerouting priority nat;` invece di `type nat hook prerouting priority dstnat;`
— `dnat to`/`snat to` sono statement validi **solo** dentro catene `type nat`, e `nat` non è un
nome di priorità riconosciuto.

### Match

| Concetto | iptables | nftables |
|---|---|---|
| Interfaccia entrata/uscita | `-i <if>` / `-o <if>` | `iif <if>` / `oif <if>` (anche `iifname`/`oifname` per nome, utile con wildcard) |
| IP sorgente/destinazione | `-s <addr>` / `-d <addr>` | `ip saddr <addr>` / `ip daddr <addr>` |
| Protocollo | `-p tcp\|udp\|icmp` | `tcp`/`udp`/`icmp` in testa al match (es. `tcp dport 80`) |
| Porta sorgente/destinazione | `--sport <p>` / `--dport <p>` | `<proto> sport <p>` / `<proto> dport <p>` |
| Negazione | `! -s <addr>` | `ip saddr != <addr>` |
| Insieme di valori (set) | serve `-m multiport --dports p1,p2` o più regole | `{ v1, v2, ... }` inline, es. `tcp dport { 80, 443 }` |
| Stato connessione | `-m state --state NEW,ESTABLISHED,RELATED` | `ct state new,established,related` |

### NAT

| Concetto | iptables | nftables |
|---|---|---|
| Cambiare destinazione | `-j DNAT --to-destination <ip>[:<porta>]` (in `PREROUTING`/`OUTPUT`) | `dnat to <ip>[:<porta>]` (in catena `type nat hook prerouting`) |
| Cambiare sorgente (fissa) | `-j SNAT --to-source <ip>` (in `POSTROUTING`) | `snat to <ip>` (in catena `type nat hook postrouting`) |
| Mascherare con IP dinamico dell'interfaccia | `-j MASQUERADE` (solo `POSTROUTING`) | `masquerade` |
| Dirottare alla macchina locale | `-j REDIRECT` | `redirect to :<porta>` |

### Verdetti/target

| Concetto | iptables | nftables |
|---|---|---|
| Accetta | `-j ACCEPT` | `accept` |
| Scarta | `-j DROP` | `drop` |
| Salta a catena custom (torna dopo) | `-j <CATENA>` | `jump <catena>` |
| Salta a catena custom (non torna) | — (non esiste equivalente diretto) | `goto <catena>` |
| Termina lo scorrimento della catena custom / applica la default policy se in una builtin | `-j RETURN` | `return` |

---

## 6. Errori comuni da evitare (dedotti dai gotcha reali del pool)

- **Confondere `FORWARD` con `INPUT`/`OUTPUT`** per un servizio che gira sull'host stesso (o
  viceversa, per traffico che lo attraversa soltanto): la regola non farà mai match. Prima di
  scrivere, rispondi "chi risponde davvero a questa richiesta?" per ogni host.
- **Scambiare `SNAT`/`DNAT`** o le rispettive opzioni (`--to-source` vs `--to-destination`): visto
  realmente in una soluzione ufficiale del pool (13 set 2023) — `-j SNAT --to-destination` non è
  una combinazione valida, `iptables` rifiuta la regola al caricamento.
- **Dimenticare `-j SNAT`/`-j DNAT`** prima di `--to-source`/`--to-destination`: senza il target
  esplicito, l'opzione non è riconosciuta (visto in 13 giu 2024).
- **Usare `-i`/`-o` in catene dove non sono ammessi**: `iptables` non accetta `-o` in
  `PREROUTING`/`INPUT`, né `-i` in `OUTPUT`/`POSTROUTING` — l'interfaccia di uscita non è ancora
  nota così presto nel percorso del pacchetto (o, simmetricamente, quella di entrata non ha più
  senso così tardi).
- **Sbagliare protocollo su una regola NAT** (es. `-p tcp` su una SNAT pensata per traffico UDP):
  la regola non fa mai match sul traffico che dovrebbe tradurre, ma non dà errore — è un bug
  silenzioso, verifica sempre che il `-p`/protocollo nella riga NAT corrisponda a quello del
  servizio che stai abilitando.
- **Dimenticare che dopo un DNAT il filtro va scritto sull'indirizzo tradotto**, non su quello
  originale — la regola `FORWARD`/`forward` (e il filtro dell'host finale) vedono il pacchetto
  **dopo** `prerouting`, che accade prima.
- **`type filter` invece di `type nat`, o `priority nat` invece di `dstnat`/`srcnat`** in nftables:
  gli statement `dnat to`/`snat to` richiedono una catena dichiarata `type nat`.
- **Usare `-I` quando l'ordine delle regole è esplicitamente richiesto dalla consegna** (11 giu
  2021): `-I` inserisce in testa, quindi una sequenza di `-I` produce l'ordine **inverso** di
  scrittura — usa `-A` quando l'ordine conta.
- **Assumere che "un file per host" sia sempre richiesto**: verifica quanti/quali file la consegna
  nomina esplicitamente — non tutti gli esercizi del pool chiedono le regole per ogni host della
  topologia.
- **Non rileggere la consegna per dedurre eccezioni implicite** alla policy di default (es. 11 giu
  2021: il fatto che un punto della consegna non sia richiamato nell'elenco finale "blocca tutto il
  resto" è un indizio che quella catena ha una policy diversa dalle altre).
