# Guida Esame — Network Intrusion Detection (S10)

> File cockpit da aprire il giorno dell'esame appena riconosci un esercizio di questo tipo.
> Autosufficiente per la maggior parte dei casi — quando serve un esempio completo già risolto,
> rimanda a `modello_network_intrusion_detection.md`. Per l'algoritmo esteso passo-passo vedi
> `procedura_operativa_NIDS.md`; per la struttura del report `template_report_NIDS.md`.
>
> **Principio guida**: se sei bloccato su come costruire un comando, la risposta è quasi sempre
> nella **Sezione 4** — non indovinare la sintassi, cercala lì.

---

## 0. I due gate che NON hai il permesso di saltare

Nei due esercizi risolti finora, l'errore più costoso non è mai stato un comando sbagliato — è
stato **saltare un passo** pensando di aver già capito abbastanza. Prima di leggere il resto:

- ⚠️ **Gate A**: hai guardato Protocol Hierarchy **per intero** (tutti i protocolli, non solo
  quello che salta all'occhio)? Se no, torna alla Sezione 2, step 1.
- ⚠️ **Gate B**: prima di scrivere la regola Suricata, hai isolato/verificato **ogni** gruppo di
  traffico legittimo mostrato da Protocol Hierarchy — non solo quello sospetto? Se no, torna alla
  Sezione 2, step 2-3. **Questo è saltato in entrambi gli esercizi fatti finora** — non fidarti
  dell'istinto che dice "ho già capito tutto", verificalo.

---

## 1. Triage — capire in 1 minuto che tipo di esercizio hai davanti

Non tutti gli esercizi NIDS chiedono la stessa cosa. Guarda il testo della consegna e Protocol
Hierarchy, poi usa questa tabella (costruita sui 6+ casi reali già visti nel pool d'esame):

| Segnale (testo del compito o Protocol Hierarchy) | Natura probabile | Vai a |
|---|---|---|
| Il testo dice "identificare protocollo/IP/porte", **non** "trovare l'attacco" | Task di identificazione, non detection | § 3.4 — salta quasi tutto il resto |
| Il testo chiede di classificare/elencare **più tipi di interazione** verso un host (non "trova l'attacco" singolo) | Classificazione multi-tipo | § 3.7 |
| Il testo menziona esplicitamente una **FLAG** da recuperare + hint su `payload-printable` | Flag-extraction | § 3.5 |
| ARP molto sopra il rumore di fondo atteso (>10-15% del totale) | Scan e/o spoofing L2 | § 3.1 |
| Molti TCP SYN verso una vittima, risposte quasi tutte RST tranne poche porte | Port scan | § 3.2 |
| Un protocollo applicativo con richieste ripetute a distanza di **millisecondi**, payload con pattern di riempimento (fisso o crescente) + marcatore | Buffer-overflow probe | § 3.3 |
| Nessuno dei precedenti salta all'occhio | Segui il percorso standard dall'inizio | § 2 |

Il triage non è definitivo — può convivere più di un pattern nello stesso pcap (es. ARP scan +
port scan nello stesso attacco, caso reale del 10/09/2025). Non fermarti al primo che riconosci.

---

## 2. Percorso standard (checklist)

Versione condensata di `procedura_operativa_NIDS.md` — apri quel file se serve il dettaglio di un
singolo step.

- [ ] **1. Apertura**: `wireshark <file>` → ordina per Source → **Statistics → Protocol Hierarchy**,
  espandi tutto, annota ogni protocollo e percentuale. *(Gate A qui.)*
- [ ] **2. Isola le conversazioni**: `Statistics → Conversations` per ogni protocollo applicativo
  visto in Protocol Hierarchy — **anche quelli che sembrano ovviamente innocui**. Se ti perdi tra
  le schede (Ethernet/IPv4/TCP/UDP non hanno gli stessi nomi della gerarchia), vai a **§ 2.1**.
- [ ] **3. Ispeziona il contenuto**: Follow Stream su un campione di ciascun gruppo — sintassi
  valida? contenuto anomalo? risposta attesa? confronto con un gruppo che sospetti legittimo. Se
  Follow Stream non basta (es. capire se è passato davvero un dato o solo controllo), vedi § 4.7.
- [x] **4. Verifica la frequenza** se il contenuto da solo non basta (`View → Time Display Format
  → Seconds Since Previously Displayed Packet`).
- [ ] **5. ICMP e DNS**: controllali sempre, anche se raramente contengono l'attacco — criteri
  concreti per giudicarli (non solo l'istinto) in **§ 3.8**.
- [ ] *(Gate B qui — prima di procedere.)*
- [ ] **6. Scrivi ed esegui la regola Suricata** (§ 4.3 per la sintassi — ricorda: `alert` **logga
  soltanto, non blocca nulla**, specialmente girando offline su un pcap con `-r`).
- [ ] **7. Verifica che generi alert** (§ 4.6 — occhio a `signature_id` vs `sid`).
- [ ] **8. Scrivi `report.txt`** seguendo `template_report_NIDS.md`.
- [ ] **9. Confeziona la consegna**: `report.txt`, `exam.rules`, `suricata.yaml`, `eve.json`.

### 2.1 Da Protocol Hierarchy a Conversations — la mappa che manca

Le due finestre organizzano l'informazione in due modi diversi, ed è facilissimo perdersi
passando dall'una all'altra (è successo entrambe le volte finora):

- **Protocol Hierarchy** guarda **in verticale**, lungo lo stack: Ethernet → IP → TCP/UDP →
  protocollo applicativo (SMTP, HTTP, DNS...). Ti dice *cosa c'è* e quanto.
- **Conversations** guarda **in orizzontale**, per livello di indirizzamento: chi ha parlato con
  chi, a quel livello. Non ha una scheda "SMTP" o "HTTP" — quei nomi non sono un livello di
  indirizzamento, viaggiano *dentro* TCP, distinti solo dalla **porta**.

**La mappatura**: un protocollo applicativo visto in Protocol Hierarchy (es. "SMTP: 157
pacchetti") si trova nella scheda **TCP** o **UDP** di Conversations, individuato dalla colonna
**Port A / Port B** col numero di porta noto (25=SMTP, 80=HTTP, 53=DNS, 23=Telnet, 22=SSH...). Non
cercare il nome del protocollo lì dentro, cerca la porta.

**Le schede, dalla più grezza alla più fine, e a cosa serve ciascuna**:
- **Ethernet** — coppie di **MAC**. A differenza degli IP, i MAC vengono **riscritti a ogni salto
  di router** (un router ha un MAC *diverso per ciascuna interfaccia/subnet*, non uno solo per
  tutto il dispositivo). Utile per confermare la **topologia**: se vedi *N* righe con *2N* MAC
  tutti diversi (nessuno ripetuto), hai *N* host ciascuno sulla propria subnet, ognuno che parla
  con l'interfaccia del router a lui dedicata. Utile anche per attacchi di livello 2 (§ 3.1). Non
  è dove si nasconde un attacco applicativo.
- **IPv4/IPv6** — coppie di soli **indirizzi IP**, senza porta. A differenza dei MAC, gli IP **non
  vengono riscritti dal router** — restano quelli reali end-to-end, indipendentemente da quanti
  salti attraversano. Aggregazione più larga della scheda TCP/UDP: se due host parlano sia su
  porta 25 che su porta 80, è **una riga sola** qui, ma **due righe separate** in TCP. Utile per
  una vista macro (quante coppie di host distinte, quanto traffico totale) e per isolare l'ICMP
  (vedi sotto).
- **TCP / UDP** — coppie **IP:porta**, la granularità fine, dove trovi effettivamente SMTP/HTTP/
  DNS/etc. distinti per porta.

**ICMP non ha una scheda propria — non è un bug**: non avendo porte, non ha il concetto di
"conversazione" nello stesso senso di TCP/UDP. Il suo traffico finisce dentro la scheda **IPv4**,
mescolato a qualsiasi altro traffico IP tra la stessa coppia di host. Per isolarlo: scrivi `icmp`
nella barra filtri principale di Wireshark, poi in Conversations spunta **"Limit to display
filter"** — la scheda IPv4 mostrerà solo le coppie con traffico ICMP tra loro.

**Controllo di coerenza utile ad ogni passaggio**: la somma dei pacchetti per riga in una scheda
deve tornare col totale di quel livello in Protocol Hierarchy (es. le righe TCP sommate = il
totale TCP della gerarchia). Se non torna, c'è un filtro attivo che non ricordavi o un gruppo che
ti sei perso.

---

## 3. Rami speciali

### 3.1 ARP (scan e/o spoofing)

Non ha stream da seguire, non ha porte. Due mosse obbligatorie:
1. **Dividi per opcode**: `arp.opcode==1` (request, "chi ha X?" → rischio scan/enumerazione) vs
   `arp.opcode==2` (reply, "X è mio" → rischio spoofing, è un'affermazione creduta vera).
2. **Fai quadrare i numeri**: se isoli N pacchetti ma Protocol Hierarchy ne segnalava M>N per ARP,
   la differenza va investigata (`arp and not (<tuo filtro>)`), non ignorata — request e reply
   spesso convivono nello stesso pcap come **fasi diverse dello stesso attacco** (scan per scoprire
   chi è vivo, poi spoofing mirato solo su quelli confermati).

Per le reply, cerca la relazione **1 MAC → molti IP** (un host reale dichiara solo il proprio):
```
tshark -r <file> -Y "arp.opcode==2" -T fields -e arp.src.hw_mac -e arp.src.proto_ipv4 | sort | uniq -c | sort -rn
```
Esempio completo: `modello_network_intrusion_detection.md`, secondo caso (12/01/2026).

### 3.2 Port scan

Firma: una sorgente manda **SYN** a una vittima su molte porte diverse, la maggioranza delle
risposte è **RST** (chiuse) tranne un numero ristretto (aperte, si comportano diverso). Isola con:
```
tcp.flags.syn==1 && tcp.flags.ack==0
```
poi confronta il volume di `tcp.flags.reset==1` in risposta dalla stessa vittima. Spesso preceduto
da uno scan ARP della stessa sorgente (§ 3.1) — controlla sempre se convivono.
Esempio completo: `modello_network_intrusion_detection.md`, quarto caso (10/09/2025).

### 3.3 Buffer-overflow probe (contenuto)

Payload con stringa di riempimento (`AAAA...`) seguita da un marcatore fisso (`BBBB`, `ABCD`...),
a distanza di millisecondi tra i tentativi — stessa tecnica di ricerca dell'offset vista in S4.
**Due varianti osservate**: marcatore su un'unica stringa lunga fissa (caso 1, HTTP), oppure
padding che **cresce di 1 byte per tentativo** su più pacchetti consecutivi — in quel caso il
segnale è nella sequenza, non in un singolo pacchetto isolato (caso 3, SMTP). La regola matcha
quasi sempre solo sul marcatore finale (invariante), non serve intercettare ogni lunghezza.
Esempi completi: `modello_network_intrusion_detection.md`, primo e terzo caso.

### 3.4 Identificazione di protocollo (non detection)

Compito diverso: non "trova l'attacco", ma "identifica protocollo + IP + porte" di un traffico
dato. **Statistics → Protocol Hierarchy da solo di norma basta** — non serve Follow Stream esteso
né analisi di frequenza né necessariamente una regola di rilevamento (a volte sì, se richiesta:
verifica la consegna). Esempio completo: `modello_network_intrusion_detection.md`, quinto caso
(TELNET, 10/02/2023) — introduce anche `flowbits` (§ 4.3).

### 3.5 Flag-extraction

Il testo chiede esplicitamente di recuperare una FLAG dal payload. Serve abilitare
`payload-printable` nella sezione `eve-log` di `suricata.yaml` (di default disattivato), scrivere
una regola che matchi il pattern noto, poi estrarre da `eve.json`:
```
jq -r 'select(.event_type=="alert") | .payload_printable' <dir_output>/eve.json | grep -i flag
```
**Se `jq` non è installato** (capitato su questa VM): prova `sudo apt install -y jq` se hai rete,
altrimenti fallback senza installare nulla (Python è già presente):
```
python3 -c "
import json
with open('<dir_output>/eve.json') as f:
    for line in f:
        e = json.loads(line)
        if e.get('event_type') == 'alert':
            print(e.get('payload_printable'))
"
```
Se la flag è frammentata su più pacchetti, va ricostruita manualmente dai frammenti estratti.
Verificato hands-on con successo il 10/07/2026 (esercizio dell'11/01/2024, flag Telnet
`FLAG{this_port_is_dangerous}` estratta al primo tentativo). Riferimenti: quinto caso in
`modello_network_intrusion_detection.md`, compito MQTT in `esercizi/SICINF/COMPITI_security.md`.

### 3.6 Attacco sotto il livello IP — Suricata non lo vede

Se l'attacco vive sotto IP (es. ARP), Suricata non ha sintassi per condizionare un alert su un
pacchetto ARP o un MAC address (i protocolli `ip`/`tcp`/`udp`/... richiedono un header IP che ARP
non ha). Non inseguirlo: approssima con un elenco di indirizzi noti-buoni/noti-cattivi — dettaglio
completo in § 4.3/4.4. Dichiara sempre questo limite esplicitamente nel report.

### 3.7 Classificazione multi-tipo (elenco di interazioni, non un solo attacco)

Alcuni esercizi non chiedono "trova l'attacco" ma "identifica N tipi di interazione verso l'host
X, per ciascuno di' se è un attacco e di che tipo" — **tutti** i gruppi vanno classificati, non
solo quello più sospetto (a differenza del percorso standard, dove di solito UN pattern è "quello
vero" e il resto è rumore di fondo liquidabile in due righe).

Metodo, per ciascun gruppo emerso da Conversations (§2 step 2):
1. Follow Stream su un campione → verdetto dal contenuto letterale, non dal volume o dall'istinto.
2. **Scrivi subito un verdetto di una riga** (benigno/malevolo, che tipo, porte/IP coinvolti) prima
   di passare al gruppo successivo — giudicarli tutti insieme alla fine mischia le impressioni.
3. Due gruppi con stessa porta/protocollo ma IP sorgente diversi non sono automaticamente "lo
   stesso tipo di interazione": Follow Stream su **entrambi** e confronta il contenuto — potrebbero
   essere, es., un login legittimo e un payload con marcatore, distinti.
4. Un gruppo che "a prima vista non sembra malevolo" (poche connessioni, a distanza di secondi,
   nessun payload sospetto) può comunque essere l'attacco se il pattern emerge solo aggregando —
   non fermarti all'impressione del singolo stream preso isolatamente. Conta quante sorgenti
   **diverse** colpiscono la **stessa porta di destinazione** sull'host:
   ```
   tshark -r <file> -Y "tcp.dstport==<porta>" -T fields -e ip.src | sort -u | wc -l
   ```
   Un numero alto di sorgenti distinte verso un solo servizio è la firma di un pattern volumetrico
   anche se ogni singolo stream, preso da solo, sembra un dialogo 1:1 normale — è proprio questo
   che lo rende difficile da vedere se lo guardi stream per stream invece che in aggregato.
5. Solo **dopo** aver classificato tutti i gruppi, controlla quale (se richiesto dalla consegna)
   necessita davvero una regola Suricata — di solito è solo quello nominato esplicitamente da
   "intercettare/registrare" (es. il gruppo con la flag), non uno per ciascuno dei tipi trovati.

**Nota su Protocol Hierarchy e pacchetti "TCP" senza protocollo applicativo**: se la somma dei
protocolli applicativi (Telnet, SSH, HTTP...) non copre il totale TCP/UDP (procedura, step 1), il
residuo non è un errore di conteggio — sono pacchetti che Wireshark non è riuscito a dissezionare
come un protocollo applicativo specifico, tipicamente perché non contengono uno scambio
applicativo completo (SYN/RST di uno scan, pacchetti di un flood senza payload, connessioni mai
stabilite). È spesso proprio lì che si nasconde lo scan/flood, non rumore da ignorare.

### 3.8 Valutare ICMP e DNS — i gruppi "ovviamente innocui" (ma vanno verificati lo stesso)

Sono i due gruppi più facili da liquidare come "sicuramente traffico normale" senza guardarli —
esattamente il tipo di scorciatoia che Gate B vieta. Criteri concreti per giudicarli, non l'istinto:

**ICMP** — qui il criterio non è il contenuto, è **l'accoppiamento richiesta/risposta**:
- Normale: ogni **Echo Request** (tipo 8) ha una **Echo Reply** (tipo 0) corrispondente dalla
  stessa coppia di host, poco dopo — un dialogo 1:1 completo, anche se ravvicinato nel tempo (un
  semplice `ping`, o un controllo di raggiungibilità automatico, sono normalissimi).
- Sospetto: tante Echo Request **senza** le rispettive reply (il bersaglio non risponde quasi
  mai), o un volume sproporzionato rispetto al resto del traffico — quello si avvicina a un
  flood/DoS.

**DNS** — qui il criterio è la **leggibilità dei nomi interrogati**:
- Normale: nomi di dominio brevi, leggibili, "umani" (es. `mail.esempio.com`); tipo di query per
  lo più `A`/`AAAA` (a volte `MX`, `PTR` per risoluzione inversa); la risposta contiene un IP
  plausibile.
- Sospetto (segno tipico di **DNS tunneling/exfiltration**, dati nascosti dentro le query invece
  di usarle solo per risolvere un nome): sottodomini **lunghi e "casuali"** che non si leggono
  come parole (es. `bxnlcibwyxnzd3jk.attacker.xyz` invece di `www.attacker.xyz` — dati codificati
  base32/64 travestiti da nome); query di tipo **TXT** frequenti (i record TXT portano più dati
  arbitrari, strumento preferito per l'abuso); stesso dominio base con un sottodominio **diverso
  ogni volta** (i dati da esfiltrare spezzati in tanti pezzi, una query ciascuno).

Nota pratica: query **PTR** (risoluzione inversa, da IP a nome) ripetute verso lo stesso host sono
spesso legate a un **altro** gruppo di traffico che hai già trovato altrove (es. un server che fa
un controllo anti-spam sul client a ogni nuova connessione) — non trattarle come un fenomeno a
parte se il pattern si spiega già con qualcos'altro nel pcap. Esempio completo:
`modello_network_intrusion_detection.md`, terzo caso (10/07/2025).

---

## 4. Riferimento comandi — come si costruiscono, non solo cosa copiare

### 4.1 Costruire un filtro Wireshark senza sapere il nome del campo

Non serve ricordare i nomi a memoria — Wireshark te li dà lui:
1. Clicca il pacchetto, espandi il protocollo nel pannello dettagli (in basso).
2. Sul campo che ti interessa: **tasto destro → Apply as Filter → Selected** → Wireshark scrive
   lui il filtro nella barra in alto e lo applica (vedi subito se il risultato è giusto).
3. Per il nome tecnico di un campo da estrarre via `tshark`: **click singolo** sul campo → il nome
   appare in basso a sinistra nella barra di stato.

### 4.2 `tshark`, pezzo per pezzo

Le **righe** (una per pacchetto) le decide sempre `-r`+`-Y` — questo non cambia mai:
- **`-r <file>`**: apri il file, come `File → Open` nella GUI.
- **`-Y "<filtro>"`**: la stessa identica barra dei filtri della GUI (§ 4.1) — tra virgolette.
- **`-T fields`**: cambia il *modello* di output — invece del riassunto fisso per pacchetto (No,
  Time, Source, Destination, Protocol, Info), scegli tu quali campi vedere.
- **`-e <campo>`**: dentro `-T fields`, ogni `-e` è una colonna. Ripetibile.

Pattern riusabili:
```
tshark -r <f> -Y "<filtro>" -T fields -e <campo> | sort -u | wc -l          # conta valori unici
tshark -r <f> -Y "<filtro>" -T fields -e <c1> -e <c2> | sort | uniq -c | sort -rn   # raggruppa e conta
```
Perché serve `-T fields` prima di `sort -u`/`uniq -c`: senza, ogni riga porta anche timestamp/numero
pacchetto (sempre diversi), quindi `sort -u` non elimina mai nulla — con `-T fields -e` la riga
contiene *solo* il valore su cui vuoi deduplicare/raggruppare.

### 4.3 Anatomia di una regola Suricata

```
alert ip $GOOD_NET any <> $GOOD_NET any (msg:"..."; content:"..."; sid:1000001; rev:1;)
  │    │  │         │   │  │         │   │
  │    │  │         │   │  │         │   └─ opzioni (metadati/match aggiuntivi)
  │    │  │         │   │  │         └───── destinazione: porta ("any" se non rilevante)
  │    │  │         │   │  └─────────────── destinazione: IP/rete/variabile
  │    │  │         │   └────────────────── direzione: "->" mono-direzionale, "<>" bidirezionale
  │    │  │         └────────────────────── sorgente: porta
  │    │  └──────────────────────────────── sorgente: IP/rete/variabile
  │    └─────────────────────────────────── protocollo — vedi elenco sotto
  └──────────────────────────────────────── azione: "alert" logga in eve.json, non blocca nulla
```

**Protocolli validi nell'header**: `ip` (tutto ciò che ha un header IP), `tcp`, `udp`, `icmp`,
`http`, `dns`, `smtp`, `tls`, `ssh`, `ftp`, e altri protocolli applicativi se il parser è abilitato.
**`arp` NON è tra questi** — vedi § 3.6/4.4 per come gestire attacchi ARP.

**Keyword incontrate finora, cosa fanno**:
| Keyword | Significato |
|---|---|
| `content:"<stringa>"` | Match su una stringa/pattern nel payload |
| `http_uri` | Restringe il `content` precedente all'URI HTTP (buffer keyword, subito dopo il content che modifica) |
| `flow:from_client` | Matcha solo pacchetti nella direzione client→server della connessione |
| `flowbits:set,<nome>` | Imposta un flag con nome sulla connessione, leggibile da altre regole con `flowbits:isset,<nome>` — per condizioni stateful su più pacchetti/regole |
| `threshold: type threshold, track by_src, count N, seconds T` | Scatena l'alert solo se una sorgente supera N match in T secondi — utile per volumi/scan invece di un content specifico |
| `sid:<numero>` | ID univoco della regola (usa numeri ≥1000000 per le tue) |
| `rev:1` | Numero di revisione, incrementa se modifichi la stessa regola |

### 4.4 Attacco sotto IP: pattern `$GOOD_NET`/`$BAD_NET`

In `suricata.yaml`, sezione `vars: → address-groups:` (accanto a `HOME_NET`):
```yaml
    GOOD_NET: "[ip1,ip2,...]"   # host legittimi, verificati con § 2 step 2-3 — non assunti per simmetria
    BAD_NET: "ip_attaccante"
```
Due regole standard:
```
alert ip $GOOD_NET any <> $GOOD_NET any (msg:"Traffico lecito"; sid:1000001; rev:1;)
alert ip $BAD_NET any <> any any (msg:"TRAFFICO SOSPETTO"; sid:1000002; rev:1;)
```
La prima scatta solo se **entrambi** i lati sono in `GOOD_NET` (log di baseline). La seconda scatta
se **un lato qualunque** è `BAD_NET` (approssima "l'attaccante è coinvolto", non l'attacco in sé —
può includere falsi positivi su traffico innocuo dello stesso host, dichiaralo nel report).

### 4.5 `suricata.yaml` — checklist per aggiungere una variabile custom

Errore fatto in questa sessione, checklist per non ripeterlo:
- [ ] **Nessun `#` davanti** alla riga — a differenza delle alternative `#HOME_NET: ...` già nel
  file (quelle sono varianti disattivate tra cui scegliere), le tue variabili sono le uniche
  definizioni che hai: se restano commentate, per Suricata non esistono.
- [ ] **Virgolette aperte E chiuse**: `"[ip1,ip2]"` — controlla che non manchi la chiusura.
- [ ] **Nessun `;`** — YAML non lo usa.
- [ ] **Indentazione a spazi**, stessa profondità delle righe vicine (`HOME_NET` sopra) — non tab.
- [ ] Lancia poi Suricata con **`-c <tuo-yaml>`**, non quello di default: `suricata -r <file> -S exam.rules -c suricata.yaml -l <dir_output>`.

### 4.6 `eve.json` — i due grep che servono

```
grep -c '"event_type":"alert"' <dir>/eve.json         # 1. c'è ALMENO un alert di qualunque regola?
grep -c '"signature_id":<N>' <dir>/eve.json            # 2. quanti della regola N specifica?
```
⚠️ **Mai `grep -c '"sid":<N>'`** — nel JSON il campo si chiama `signature_id`, annidato dentro
`"alert":{...}`; `sid` è solo il nome usato nella sintassi della *regola*, non nel log. Se il
comando 2 dà 0 ma il comando 1 dà >0, il problema è il nome del campo nel grep, non la regola.

### 4.7 Confermare un'ipotesi con i flag TCP grezzi (non fidarti del colore in Wireshark)

Il colore delle righe in Wireshark è solo un aiuto visivo (regole di colorazione secondarie) — il
dato affidabile per capire cosa fa davvero una connessione è il campo **Flags** del pacchetto TCP,
non il colore né i numeri seq/ack da soli (seq/ack relativi possono essere identici sia per
un'accettazione che per un rifiuto — quello che li distingue è il flag, non il numero).

**Decodifica flag** (si sommano i bit): `SYN=0x02`, `ACK=0x10`, `PSH=0x08`, `FIN=0x01`, `RST=0x04`.
Combinazioni comuni: `0x02`=SYN, `0x12`=SYN+ACK, `0x10`=ACK puro (nessun dato), `0x18`=PSH+ACK
(**pacchetto con dati applicativi reali**), `0x11`=FIN+ACK (chiusura pulita), `0x14`=RST+ACK
(chiusura brusca/rifiuto).

**Comando per vedere la sequenza esatta di una connessione, pacchetto per pacchetto**:
```
tshark -r <file> -Y "ip.addr==<hostA> && ip.addr==<hostB> && tcp.port==<porta>" -T fields -e frame.number -e ip.src -e tcp.flags -e tcp.len
```
`tcp.len` è la lunghezza del payload TCP (byte di dati applicativi, escluso l'header) — se per
ogni riga è `0`, quella connessione ha scambiato solo controllo (handshake/teardown), zero dati
veri, **anche se ha completato un handshake regolare**. Se anche un solo pacchetto ha `tcp.len` >
0, lì dentro c'è payload — vai a leggerlo con Follow Stream.

Questo distingue in modo affidabile, ad esempio, un **probe di scan** (connette, verifica, si
disconnette con RST, zero payload) da un **uso legittimo dello stesso servizio** sulla stessa
porta (handshake completo, PSH+ACK con dati reali, chiusura pulita con FIN+ACK) — due connessioni
sulla stessa porta, stessa coppia di host anche, possono essere cose completamente diverse: **non
dare per scontato** che "porta X aperta" significhi automaticamente "è tutto scan", né estendere
per analogia la conclusione di una connessione simile senza verificarla.

### 4.8 Prima di eseguire un file scritto a mano

```
cat -A <file>
```
Controlla che ogni riga finisca esattamente dove dovrebbe (`$` di `cat -A` = fine riga, niente
dopo). In questa sessione sono spariti caratteri digitando comandi lunghi (`any`→`an`, spazi
mancanti) — sintomo di lag della VM, non errore di sintassi: se un parsing fallisce in modo
strano, **prima di rileggere la sintassi da capo, verifica che il file contenga davvero quello che
pensi di aver scritto.**

---

## 5. Riferimenti

- `procedura_operativa_NIDS.md` — algoritmo esteso, passo per passo
- `template_report_NIDS.md` — struttura di `report.txt`
- `modello_network_intrusion_detection.md` — 5 casi reali completi:
  1. Port scan / DDoS / SSH legittimo / flag Telnet (11/01/2024) — anche il caso originale con `dump.pcap`
  2. ARP spoofing in due fasi, `$GOOD_NET`/`$BAD_NET` (12/01/2026)
  3. Buffer-overflow SMTP a padding incrementale (10/07/2025)
  4. ARP scan + TCP port scan combinati (10/09/2025)
  5. Identificazione protocollo TELNET + `flowbits` (10/02/2023)
