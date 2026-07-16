# Guida Esame — Iptables/NFTables

> File cockpit da aprire il giorno dell'esame appena riconosci un esercizio di questo tipo: una
> topologia di rete (uno o più host, spesso un Router) su cui scrivere regole di filtraggio — e
> talvolta NAT — che consentano **esclusivamente** il traffico descritto in consegna, scartando
> tutto il resto. Deliverable tipico: uno o più file di comandi (`iptables.txt`, `ipt-*.sh`,
> `*.nft`), **non** un report scritto con screenshot. Autosufficiente per la maggior parte dei casi
> insieme ai suoi rimandi. Per l'algoritmo esteso passo-passo e la cheatsheet sintassi completa,
> vedi `procedura_operativa_iptables.md`; per 7 casi reali già risolti (tutti con soluzione
> ufficiale del docente, incluse le imprecisioni onestamente segnalate), `modello_iptables_nftables.md`.
>
> **Principio guida**: se sei bloccato su *come* costruire una regola, la risposta è quasi sempre
> nella **Sezione 4** di questo file o nella cheatsheet di `procedura_operativa_iptables.md`. Se sei
> bloccato su *quale* traffico va aperto per ogni host, è nella **Sezione 2**. Se sei bloccato su
> *dove leggere* un singolo pezzo di una regola (protocollo, porta, nome interfaccia, indirizzo — e
> cosa invece è "metodo fisso" sempre uguale), la mappa delle tre fonti è in
> `procedura_operativa_iptables.md` §0.5 "Da dove viene ogni pezzo di una regola".

---

## 0. I gate che NON hai il permesso di saltare

- ⚠️ **Gate A — hai letto TUTTA la consegna prima di scrivere la prima regola?** Il pool lo chiede
  esplicitamente in almeno un caso ("si consiglia di leggere prima tutta la lista per determinare
  correttamente i requisiti", 11 giu 2021) — un punto successivo può cambiare come va scritto un
  punto precedente (es. un'esclusione dall'elenco finale che rivela una policy diversa dalle altre).
- ⚠️ **Gate B — hai contato ESATTAMENTE quali file la consegna chiede?** Non presumere "un file per
  host della topologia": nel pool ci sono esercizi che chiedono solo il Router (8 feb 2024), altri
  Router+Server senza il Client (13 giu 2024), altri ancora ogni host coinvolto (13 set 2023, 12
  gen 2026). Cerca i nomi di file esatti nel testo (`iptables.txt`, `ipt-router.sh`, `bastion.nft`,
  ...) e produci solo quelli.
- ⚠️ **Gate C — hai deciso sintassi (iptables/nftables) e se serve NAT PRIMA di scrivere?** Cambiare
  idea a metà file costa tempo. Il triage per entrambe le decisioni è in Sezione 1 e Sezione 2.

---

## 1. Triage — che tipo di esercizio è

| Segnale nella consegna | Cosa implica |
|---|---|
| Estensione file richiesta `.txt`/`.sh`, sintassi vista negli esempi con `-A`/`-I`/`-j` | `iptables` legacy — sezione cheatsheet iptables in `procedura_operativa_iptables.md` §5 |
| Estensione file richiesta `.nft`, o la consegna nomina esplicitamente "nftables" | `nftables` — stessa sezione, colonna destra |
| Un solo host, "potrebbe avere più interfacce e funzionare da router" | Host singolo multi-ruolo: alcune regole sono INPUT/OUTPUT (locali), altre FORWARD (se davvero funge da router) — vedi caso 1 nel modello |
| Consegna rimanda a un **altro esercizio** (es. "fate riferimento all'esercizio su Intrusion Detection") per la topologia | La topologia non è nel testo iptables: va letta/dedotta dall'altro esercizio richiamato (stesso corso, altra tipologia). Non inventarla: cercala |
| Parola **"indiretto"/"indirettamente"** riferita a un servizio raggiungibile dall'esterno | Il target ha IP privato → serve **DNAT** per pubblicarlo dietro l'IP pubblico del router |
| Consegna dice che le reti private **non sono instradate automaticamente** (nemmeno tra loro) | Quasi ogni comunicazione che attraversa il confine pubblico/privato richiede NAT in una direzione |
| Un host ha IP privato e deve raggiungere una rete diversamente indirizzata, **anche senza la parola "indiretto"** | Il bisogno di NAT può essere implicito nella topologia (client privato che raggiunge un segmento "pubblico" diverso, o Internet) — leggi gli indirizzi, non solo le parole chiave |
| "le regole devono essere applicate nell'ordine in cui vengono proposte" | Usa `-A` (append), mai `-I` (insert, che inverte l'ordine) |
| Un host ha **una sola interfaccia fisica** verso "tutto il resto" (es. un Bastion, o un webserver dietro un router) | Non puoi distinguere "da Internet" da "dalla mia rete" con `-i`/`-o` — serve un match sull'indirizzo (in nftables: insieme con negazione `!= {reti note}`) |
| "qualsiasi altro pacchetto deve essere scartato" / "e null'altro oltre al traffico indispensabile" | Default-drop su tutte le catene, loopback sempre permesso, scrivi solo le regole di ciò che deve passare |

Il triage non decide da solo tutte le regole: la distinzione INPUT/OUTPUT/FORWARD per ogni host va
comunque fatta caso per caso leggendo la topologia (Sezione 2). Non presumere che un esercizio usi
lo stesso schema NAT/filtro di uno simile solo perché "sembra uguale" — il pool varia deliberatamente
quali host servono NAT e quali no.

---

## 2. Percorso standard (checklist)

Versione condensata di `procedura_operativa_iptables.md` — apri quel file per il dettaglio ed
esempi di codice.

- [ ] **0. Leggi tutta la consegna** (Gate A). Nota ogni parola chiave di Sezione 1.
- [ ] **1. Conta i file richiesti** (Gate B) e la sintassi (Gate C: iptables o nftables).
- [ ] **2. Per ogni host della topologia**, classifica ogni flusso richiesto: è locale
  (INPUT/OUTPUT, l'host è client o server di quella interazione) o attraversa soltanto (FORWARD)?
  Tabella di riferimento in `procedura_operativa_iptables.md` §1.
- [ ] **3. Decidi se e dove serve NAT** (`procedura_operativa_iptables.md` §2): DNAT in
  PREROUTING/hook `prerouting priority dstnat` per pubblicare un server privato; SNAT/MASQUERADE in
  POSTROUTING/hook `postrouting priority srcnat` per far uscire client privati. Ricorda: dopo un
  DNAT, il filtro `FORWARD` (e l'host finale) vanno scritti sull'indirizzo **tradotto**, non
  quello originale.
- [ ] **4. Scrivi lo scheletro fisso** per ogni host: flush/reset, loopback ACCEPT, poi le regole
  di servizio, poi le policy DROP finali (eccetto se il testo implica il contrario — vedi caso 1
  del modello). Schema esatto in `procedura_operativa_iptables.md` §3.
- [ ] **5. Per ogni servizio consentito, scrivi la coppia richiesta/risposta** su ogni host
  coinvolto (client: OUTPUT dport + INPUT established sport; server: INPUT dport + OUTPUT
  established sport) — occhio all'eccezione NTP (porta 123 simmetrica). Schema in
  `procedura_operativa_iptables.md` §4.
- [ ] **6. Rileggi ogni regola NAT**: target giusto (`SNAT`/`DNAT`) con l'opzione giusta
  (`--to-source`/`--to-destination`), interfaccia ammessa per quella catena, protocollo coerente
  col servizio che stai abilitando. Sono i quattro errori più frequenti nelle soluzioni reali del
  pool (§6 di `procedura_operativa_iptables.md`).
- [ ] **7. Verifica il conteggio finale**: hai scritto regole solo per ciò che deve passare?
  Nessuna regola per traffico esplicitamente escluso/identificato come attacco (visto in 8 feb
  2024: il traffico dell'attacco individuato in un altro esercizio non va aperto, semplicemente non
  scriverci nessuna regola)?

---

## 3. Rami per scenario

### 3.1 Host singolo (con o senza funzione di router)

- **Riconoscere**: la consegna descrive un solo host, eventualmente "con più interfacce",
  potenzialmente "funziona da router".
- **Come procedere**: stesso host può avere sia regole locali (INPUT/OUTPUT per servizi che
  eroga/consuma lui stesso) sia regole FORWARD (se davvero inoltra traffico tra reti). Non
  confonderle: chiediti separatamente, per ogni riga della consegna, se il servizio termina
  sull'host o lo attraversa.
- **Gotcha noto**: se la consegna richiama esplicitamente l'ordine delle regole, usa `-A`; se un
  punto della lista finale "blocca tutto il resto" non richiama una catena già trattata, è un
  indizio che quella catena ha una policy diversa (vedi caso 1 del modello, 11 giu 2021).

### 3.2 Filtro multi-host senza NAT

- **Riconoscere**: più host, indirizzi già tutti instradabili senza traduzione (nessuna parola
  "indiretto", nessun accenno a reti private non raggiungibili).
- **Come procedere**: per ogni host, classifica ogni flusso (Sezione 2, passo 3), scrivi lo
  scheletro fisso + le coppie richiesta/risposta. Nessuna tabella NAT necessaria in nessun file.
- **Esempio nel pool**: 8 febbraio 2024 (solo Router, tre reti interne, nessun Internet).

### 3.3 Filtro + NAT (pubblicazione indiretta o uscita mascherata)

- **Riconoscere**: parola "indiretto", o un host con IP privato che deve raggiungere/essere
  raggiunto da una rete diversamente indirizzata.
- **Come procedere**:
  1. Identifica **quale** host fa da confine (quasi sempre il Router) — è lì che vive la tabella
     NAT, mai sull'host finale (client/server non fanno mai NAT di se stessi in questo pool).
  2. DNAT per "pubblicare" un servizio con IP privato: prerouting, matcha l'IP pubblico esterno
     come destinazione, traduci verso l'IP privato reale.
  3. SNAT/MASQUERADE per far uscire un client/server privato verso una rete che non saprebbe
     rispedire una risposta a quell'indirizzo: postrouting, matcha la sorgente privata, traduci con
     l'IP del confine su quel segmento. **Ma prima verifica che la rotta di ritorno manchi davvero**:
     se il router è il *default gateway* di entrambe le reti private (o la consegna dichiara il
     routing), la risposta sa già tornare e il SNAT è superfluo — è la differenza tra 13 giu 2024
     (serve SNAT) e 10 lug 2025 (niente SNAT pur essendo privato→privato). Criterio completo in
     `procedura_operativa_iptables.md` §2, "Discriminante decisivo per il segnale 2".
  4. **Sul filtro** (FORWARD sul router, o INPUT/OUTPUT sull'host finale): usa l'indirizzo **dopo**
     la traduzione — il DNAT/SNAT in prerouting/postrouting accade prima che il filtro esamini il
     pacchetto.
  5. Sull'host finale (server pubblicato, o client mascherato), il filtro locale vede il pacchetto
     già tradotto: il server non vede mai l'IP pubblico con cui è stato contattato, solo la
     sorgente originale del richiedente (il DNAT cambia solo la destinazione); un host dietro un
     SNAT del router viene visto dagli altri come se fosse il router stesso.
- **Ti serve UNA sola riga SNAT, non due**: il verso di ritorno lo ritraduce automaticamente il
  conntrack (nessuna regola NAT per la risposta). Se hai bisogno di *vederlo* pacchetto per pacchetto
  per fidartene sotto stress, la traccia "senza SNAT vs con SNAT" hop per hop è in
  `procedura_operativa_iptables.md` §2, "Traccia pacchetto per pacchetto". Ricorda solo che la riga
  di *filtro* `ESTABLISHED` per la risposta va scritta comunque a mano — quella è filtro, non NAT.
- **Esempi nel pool**: 13 giugno 2024 (SNAT sia per raggiungere il server "pubblico" sia per uscire
  su Internet), 10 luglio 2025 e 30 ottobre 2025 (DNAT per pubblicare un servizio interno + SNAT
  per il traffico DNS in uscita), 12 gennaio 2026 (DNAT + SNAT combinati, reti private non
  instradate nemmeno tra loro).

### 3.4 Host "single-homed dietro un router" (Bastion, ALG, webserver con un solo link esterno)

- **Riconoscere**: un host che non è il router ma ha comunque **una sola interfaccia** verso tutto
  ciò che sta oltre il proprio segmento (Internet e/o altre reti raggiunte solo tramite il router).
- **Come procedere**: niente `-i`/`-o` per distinguere "da Internet" da "dal mio segmento" — usa un
  match sull'indirizzo. In nftables: insieme con negazione, `ip saddr != {rete_propria_1,
  rete_propria_2}` per dire "viene da fuori". Questo host **non ha bisogno di una catena FORWARD
  funzionante** (non inoltra nulla per definizione) — dichiarala comunque vuota con policy drop,
  per chiarezza esplicita (visto nella soluzione ufficiale del 10 luglio 2025, commento "bastion
  non è un router").
- **Attenzione al ruolo ALG**: se l'host fa da Application-Level Gateway, la connessione in
  ingresso (es. porta 8443) e quella in uscita verso il servizio reale (es. porta 443) sono **due
  connessioni indipendenti**, non un semplice inoltro — quindi sull'host ALG la prima è INPUT (lui
  è server) e la seconda è OUTPUT (lui è client), mai FORWARD.
- **Esempi nel pool**: 10 luglio 2025 (Bastion/ALG), 30 ottobre 2025 (webserver verso Internet sulla
  sua unica interfaccia esterna, ma con un secondo link dedicato — quindi non single-homed — verso
  il DB server).

---

## 4. Riferimento comandi — come si costruiscono, non solo cosa copiare

### 4.1 Lo scheletro fisso (default-drop + loopback)

Vedi `procedura_operativa_iptables.md` §3 per il codice completo in entrambe le sintassi. Il punto
concettuale: le policy di default realizzano da sole "qualsiasi altro pacchetto deve essere
scartato" — non serve mai una regola finale di DROP esplicita, si scrivono solo le regole di ciò
che deve passare.

### 4.2 La coppia richiesta/risposta

Vedi `procedura_operativa_iptables.md` §4. Il punto concettuale: `ESTABLISHED`/`ct state
established` (non un secondo match statico sulla porta sorgente) restringe l'accettazione alle sole
risposte di connessioni già avviate legittimamente da questo host — un match statico su `--sport`
senza stato accetterebbe qualunque pacchetto con quella porta sorgente, anche non richiesto.
Eccezione: NTP usa la porta 123 su entrambi i lati, quindi la stessa riga ha sia `--dport 123` sia
`--sport 123`. Stesso principio (porte fisse su entrambi i lati) per **DHCP**: server 67, client 68
→ richiesta `--sport 68 --dport 67`, risposta `--sport 67 --dport 68` (dettaglio in
`procedura_operativa_iptables.md` §4). **ICMP/ping** è un altro caso a parte — non ha porte e si
abbina per *tipo di messaggio* (echo-request/echo-reply), non per porta: vedi §4.6. Se un servizio
correlato (FTP attivo) o un errore ICMP legato a una connessione va lasciato passare, `ESTABLISHED`
da solo non basta — serve `ESTABLISHED,RELATED` (`procedura_operativa_iptables.md` §4, "Quando serve
`RELATED`").

### 4.3 Cheatsheet sintassi comparata iptables ↔ nftables

Tabella completa (tabelle/catene, hook/priority, match, NAT, verdetti) in
`procedura_operativa_iptables.md` §5 — apri quella sezione ogni volta che devi tradurre un comando
da una sintassi all'altra o non ricordi la keyword esatta.

### 4.4 NAT: costruire la regola giusta, non solo copiarla

```
# DNAT (iptables) — pubblica un servizio con IP privato dietro un IP pubblico
iptables -t nat -A PREROUTING -i <if_esterna> -d <ip_pubblico> -p tcp --dport <porta_pubblica> \
    -j DNAT --to-destination <ip_privato>:<porta_reale>

# SNAT (iptables) — maschera un host/rete privata in uscita
iptables -t nat -A POSTROUTING -s <rete_privata> -o <if_esterna> -j SNAT --to-source <ip_confine>
```
```
# nftables — DNAT
chain prerouting {
    type nat hook prerouting priority dstnat;
    iif <if_esterna> ip daddr <ip_pubblico> tcp dport <porta_pubblica> dnat to <ip_privato>:<porta_reale>
}

# nftables — SNAT
chain postrouting {
    type nat hook postrouting priority srcnat;
    oif <if_esterna> ip saddr <rete_privata> snat to <ip_confine>
}
```
**Perché l'hook/la catena sono vincolanti e non intercambiabili**: DNAT deve avvenire *prima* che
il kernel decida come instradare (altrimenti instrada verso l'indirizzo sbagliato, quello ancora
non tradotto) → `prerouting`. SNAT deve avvenire *dopo* che tutto il resto è deciso, appena prima
che il pacchetto lasci il sistema (altrimenti il resto del sistema — routing, filtro — ragionerebbe
su un indirizzo che non è quello reale del mittente) → `postrouting`.

**`SNAT` o `MASQUERADE`? Il criterio è l'IP di uscita**: se la topologia ti dà un **IP pubblico fisso**
accanto all'interfaccia esterna del router (il caso di tutti i 7 esercizi del pool), usa
`-j SNAT --to-source <ip>` / `snat to <ip>` — esplicito e più efficiente. Se l'IP esterno è
**dinamico o non fornito** (uplink DHCP/PPPoE), usa `-j MASQUERADE` / `masquerade`, che prende in
automatico l'IP corrente dell'interfaccia di uscita. Dettaglio in `procedura_operativa_iptables.md` §2.

**Verifica sempre, riga per riga, prima di consegnare**:
- Il target è quello giusto per la direzione che vuoi (`DNAT`↔destinazione, `SNAT`↔sorgente)? Non
  sono intercambiabili nemmeno nelle opzioni (`--to-destination` non esiste per `SNAT` e viceversa).
- L'interfaccia che hai messo (`-i`/`-o`, `iif`/`oif`) è ammessa in quella catena? `PREROUTING`/
  `INPUT` non ammettono `-o`; `OUTPUT`/`POSTROUTING` non ammettono `-i`.
- Il protocollo (`-p`/`tcp`/`udp`) nella riga NAT corrisponde davvero al servizio che stai
  traducendo? Un protocollo sbagliato non dà errore, semplicemente la regola non fa mai match sul
  traffico che dovrebbe abilitare — bug silenzioso, il più insidioso da individuare rileggendo.

### 4.5 Dopo il NAT, il filtro guarda l'indirizzo tradotto

Se una catena NAT agisce prima del filtro nel percorso del pacchetto (`prerouting` prima di
`forward`), le regole di filtro successive devono matchare l'indirizzo **come appare dopo** quella
traduzione:
```
# Esempio: DNAT pubblica 130.136.1.1:443 -> 192.168.1.7:443 in prerouting.
# La regola forward, scritta DOPO che prerouting ha già agito, guarda l'IP privato:
iif eth3 oif eth2 ip daddr 192.168.1.7 tcp dport 443 accept       # corretto
iif eth3 oif eth2 ip daddr 130.136.1.1 tcp dport 443 accept       # SBAGLIATO: non farà mai match
```
Lo stesso vale per il filtro dell'host finale pubblicato: vede la destinazione locale già tradotta
(il proprio IP privato reale), ma la sorgente rimane quella originale del richiedente esterno — il
DNAT cambia **solo** la destinazione, mai la sorgente.

### 4.6 ICMP/ping — nessuna porta, si abbina per tipo di messaggio

ICMP (`-p icmp` / `icmp`) **non ha porte**: niente `--dport`/`--sport`, perché la porta è un concetto
di TCP/UDP, non di ICMP. Al loro posto c'è il **tipo** di messaggio: la richiesta ping è
`echo-request` (tipo 8), la risposta è `echo-reply` (tipo 0). L'andata/ritorno si abbina quindi **per
tipo**, non per porta — ma per il resto è la solita coppia richiesta/risposta con `ESTABLISHED` sulla
risposta.

```
# iptables — lato client (chi lancia il ping)
iptables -A OUTPUT -p icmp --icmp-type echo-request -j ACCEPT
iptables -A INPUT  -p icmp --icmp-type echo-reply -m state --state ESTABLISHED -j ACCEPT
# lato host pingato: INPUT echo-request + OUTPUT echo-reply ESTABLISHED

# nftables (table ip)
oif <if> icmp type echo-request accept
iif <if> icmp type echo-reply ct state established accept
```

**Punto chiave — conntrack traccia ICMP come TCP**: per i tipi domanda/risposta (echo incluso) il
kernel registra l'`echo-request` e riconosce l'`echo-reply` corrispondente come **`ESTABLISHED`**.
Quindi lo schema "richiesta esplicita + risposta con `ct state established`" **vale identico anche per
ICMP** — la riga di ritorno la scrivi con `--icmp-type echo-reply` esplicito o con `ESTABLISHED`, sono
equivalenti. Non c'è sintassi nuova da inventare.

**Scenario "il client fa ping verso l'esterno"**: sul client le due righe qui sopra; sul router il
ping *attraversa* → `FORWARD` per `echo-request` (andata) + `echo-reply ESTABLISHED` (ritorno). Se il
client è privato e pinga Internet, serve anche il SNAT/MASQUERADE in POSTROUTING (conntrack maschera
anche ICMP). Esempio completo e nota su `inet`/IPv6 in `procedura_operativa_iptables.md` §4, "Caso
speciale ICMP".

---

## 5. Errori comuni — riferimento rapido

Elenco completo con spiegazione in `procedura_operativa_iptables.md` §6. I più frequenti nel pool
reale (con soluzione ufficiale del docente, non solo negli errori di uno studente):
- Confondere `FORWARD` con `INPUT`/`OUTPUT`.
- Scambiare `SNAT`/`DNAT` o le rispettive opzioni.
- Dimenticare `-j SNAT`/`-j DNAT` prima di `--to-source`/`--to-destination`.
- Usare `-i`/`-o` in catene che non li ammettono.
- Protocollo sbagliato su una riga NAT (bug silenzioso).
- Filtrare sull'indirizzo pre-NAT invece che post-NAT.
- `type filter`/`priority nat` invece di `type nat`/`priority dstnat`/`srcnat` in nftables.
- Usare `-I` quando l'ordine delle regole è esplicitamente richiesto.
- Assumere "un file per host" senza verificarlo nella consegna specifica.

---

## 6. Indice dei casi reali (collegamento a `modello_iptables_nftables.md`)

| Data | Scenario (§3) | Sintassi | NAT | Particolarità da ricordare |
|---|---|---|---|---|
| 11 giugno 2021 | 3.1 Host singolo | iptables | no | `FORWARD` default ACCEPT dedotto dal testo; `-A` obbligatorio per l'ordine |
| 13 settembre 2023 | 3.3 Filtro + NAT | iptables | sì | porta NTP: testo dice 1233, soluzione usa 123 (refuso nel testo); SNAT/DNAT invertiti nella soluzione ufficiale |
| 8 febbraio 2024 | 3.2 Filtro multi-host senza NAT | iptables | no | topologia dedotta da un esercizio NIDS collegato; NTP porta simmetrica 123/123 |
| 13 giugno 2024 | 3.3 Filtro + NAT | iptables | sì | SNAT senza `-j SNAT` nella soluzione ufficiale; solo 2 file richiesti (non il Client) |
| 10 luglio 2025 | 3.4 Single-homed (Bastion/ALG) | nftables | sì (solo DNAT) | primo esercizio nftables del pool; ALG = due connessioni indipendenti, non forwarding |
| 30 ottobre 2025 | 3.3 + 3.4 combinati | nftables | sì | `type filter`/`priority nat` invece di `type nat`/`dstnat`/`srcnat` nella tabella NAT ufficiale |
| 12 gennaio 2026 | 3.3 Filtro + NAT | nftables | sì | reti private non instradate nemmeno tra loro; refuso sospetto `:accept` in un file ufficiale |

Per il testo integrale di ogni consegna, la topologia, il ragionamento host-per-host e la soluzione
ufficiale completa, apri `modello_iptables_nftables.md` e cerca la data.
