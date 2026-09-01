# Modello Risolto — Network Intrusion Detection

> Fonte: `SIMULAZIONI ESAMI/SICINF/Network_Intrusion_Detection.html` (Virtuale), esercizio dell'
> **11 gennaio 2024**. Consegna e testo di analisi sono quelli reali della soluzione ufficiale.
> Il formato dei file da consegnare è cambiato leggermente nelle sessioni più recenti (vedi nota in
> fondo), ma il procedimento di analisi è identico.

---

## Consegna originale

> Scaricate il tracciato di traffico `dump.pcap`. Analizzate il tracciato con Wireshark (suggerimento:
> fate uso dell'ordinamento per distinguere diversi tipi di attacco). Identificate **quattro tipi di
> interazione** verso il server `10.10.10.10`. Scrivete una regola per Suricata che permetta di
> registrare la FLAG nel file degli eventi.

**Consegna**: un file `attacks.txt` con la descrizione dei quattro tipi di interazione individuati (se
sono o no attacchi, di che tipo, che porte/indirizzi coinvolgono), e uno screenshot `suricata.png` che
mostri il comando con cui si estrae la FLAG dal file eventi di Suricata.

---

## Soluzione modello

### Metodo di analisi (Wireshark)

Il trucco è **ordinare per colonna**, non scorrere il pcap pacchetto per pacchetto:

1. **Ordinando per indirizzo sorgente**: si nota una grande quantità di pacchetti tutti provenienti
   da `10.10.10.10` diretti a **porte di destinazione variabili** → segnatura tipica di **port scan**
   (es. nmap).
2. **Ordinando per protocollo**: emergono una normale connessione **SSH** legittima da `10.10.10.10`,
   e una connessione **Telnet** (in chiaro) il cui payload applicativo contiene la flag.
3. **Ordinando per porta di destinazione**: si nota una grande quantità di pacchetti diretti alla
   porta **80**, provenienti da sorgenti **multiple e variabili** → segnatura tipica di **DDoS**
   (Distributed Denial of Service) verso il servizio web.

### `attacks.txt`

```
Analisi del tracciato dump.pcap (Wireshark), ordinato per sorgente / protocollo / porta destinazione:

1. PORT SCAN — grande quantità di pacchetti da 10.10.10.10 verso 10.10.10.10... 
   [nota: sorgente dello scan] con porte di destinazione variabili e crescenti,
   nessuna risposta applicativa: tipica scansione delle porte (es. nmap SYN scan).

2. CONNESSIONE SSH LEGITTIMA — sessione SSH regolare (porta 22) da 10.10.10.10,
   traffico cifrato, nessuna anomalia nel pattern: interazione legittima.

3. CONNESSIONE TELNET — protocollo Telnet (porta 23), traffico in chiaro,
   payload applicativo contenente la stringa FLAG: questo è il traffico
   da intercettare per estrarre la flag.

4. DDoS — grande volume di pacchetti diretti alla porta 80 del server,
   provenienti da un elevato numero di sorgenti diverse e variabili:
   pattern tipico di Distributed Denial of Service contro il servizio web.

REGOLA SURICATA (per intercettare/registrare la flag nel traffico Telnet):
alert tcp 10.10.0.0/16 any -> 10.10.10.10 23 (msg:"Flag"; content:"FLAG"; sid:30202030; rev:1;)
```

### Estrazione della flag da `eve.json` (equivalente a `suricata.png`)

Per vedere il contenuto applicativo (payload) nei log di Suricata va abilitata l'opzione
`payload-printable` nella sezione `eve-log` di `/etc/suricata/suricata.yaml`. Poi si esegue Suricata
in modalità offline sul pcap con la regola sopra, e si estrae la flag dal log eventi:

```
sudo suricata -r dump.pcap -c /etc/suricata/suricata.yaml -S exam.rules -l /tmp/out
cat /tmp/out/eve.json | jq -r 'select(.event_type=="alert") | .payload_printable' | grep FLAG
```

---

## Perché funziona (meccanismo, non solo comandi)

Suricata **non "capisce" da sola** cosa è un attacco: bisogna prima fare l'analisi umana con
Wireshark per capire *quale traffico* è anomalo (qui: il payload Telnet con la flag), e solo dopo si
scrive una regola che lo intercetti **specificamente** — matchando protocollo/porta (`tcp ... 23`) e
contenuto del payload (`content:"FLAG"`). La regola non "rileva un attacco" in astratto: rileva
esattamente il pattern di traffico che l'analisi manuale ha già identificato come rilevante. Questo è
il motivo per cui il primo passo (ordinamento in Wireshark per sorgente/protocollo/porta) è la parte
più importante dell'esercizio — la regola Suricata finale è quasi sempre corta e semplice una volta
capito cosa cercare.

> **Nota sul formato di consegna più recente** (dal 2025 in poi): gli esercizi più recenti chiedono
> `report.txt` (equivalente ad `attacks.txt`, più esteso: include anche il traffico *innocuo*
> individuato), i file `suricata.yaml` e `exam.rules` usati, e il file `eve.json` risultante con
> l'alert presente — invece del solo screenshot. Il contenuto richiesto è lo stesso (analisi +
> regola + prova che la regola funzioni), cambia solo la forma di consegna (file di configurazione
> reali invece di uno screenshot del comando).

---

## Secondo caso: ARP spoofing — attacco sotto il livello IP (12 gennaio 2026)

> Fonte: `Network_Intrusion_Detection.html`, esercizio `trace-2026-01-12.pcapng` (prova d'esame
> passata più recente al 09/07/2026). Soluzione ufficiale del prof recuperata dall'allegato
> "Soluzione" nascosto nella stessa pagina HTML (tarball `ids_20260112`, non solo testo/screenshot).
> Caso interessante perché **diverso in natura** dal primo modello sopra: lì l'attacco viveva nel
> payload applicativo (Telnet in chiaro); qui l'attacco vive **sotto** IP, a livello ARP — Suricata
> non può vederlo affatto, e la regola finale è un'approssimazione dichiarata, non un rilevamento.

### Perché ARP va trattato diversamente da TCP/UDP

ARP non ha porte né "stream" da seguire (niente Follow Stream). Le uniche due leve sono:
- **opcode**: `1`=request ("chi ha X?", rischio enumerazione/scan), `2`=reply ("X è mio", rischio
  spoofing — è un'affermazione, non una domanda, ed è quella che gli altri host credono vera).
- **relazione MAC↔IP**: un host reale dichiara un solo IP nelle sue reply. Un MAC che ne dichiara
  più di uno sta mentendo su più identità (a meno che non sia un router/NAT).

In questo pcap conviveva**no due fasi distinte dello stesso attaccante** (`172.21.1.129`, MAC
`08:00:27:3b:72:ff`), facilmente confuse se ci si ferma alla prima pista trovata:
1. **Fase 1 — ricognizione**: 1302 richieste ARP (`opcode==1`), una per ciascuno dei 255 IP
   possibili della subnet `/24` — scan a tappeto per scoprire chi è vivo.
2. **Fase 2 — poisoning mirato**: 510 reply ARP non richieste (`opcode==2`, gratuite — nessuna
   request corrispondente), inviate in **unicast** a ciascuno dei 5 host realmente vivi (scoperti
   in fase 1), dichiarando falsamente che i loro IP sono al MAC dell'attaccante.

Il modo per non fermarsi alla fase 1 (facile da trovare, ma non è il cuore dell'esercizio secondo
la soluzione del prof): **far quadrare i numeri**. Protocol Hierarchy segnalava 1966 pacchetti ARP
totali; isolando la fase 1 (`arp.src.proto_ipv4==<attaccante>`) se ne spiegano solo 1302 — il
residuo di 664 va sempre investigato invertendo il filtro (`arp and not (...)`), mai ignorato.

Comando chiave per isolare la fase 2 (raggruppa le reply per MAC sorgente e IP dichiarato):
```
tshark -r <file> -Y "arp.opcode==2" -T fields -e arp.src.hw_mac -e arp.src.proto_ipv4 \
  | sort | uniq -c | sort -rn
```
Un MAC che compare con **più IP diversi** nell'output è la firma dello spoofing.

### La regola Suricata — un'approssimazione dichiarata, non un rilevamento

Suricata analizza solo dagli header IP in su: non esiste sintassi per condizionare un alert sul
contenuto di un pacchetto ARP o su un MAC address. La soluzione ufficiale non prova a inseguire
l'attacco — lo approssima con un elenco di indirizzi noti-buoni/noti-cattivi, verificato con
Conversations sui protocolli legittimi (step 2-3 della procedura), **non** dedotto per simmetria
dall'analisi ARP (scorciatoia comoda ma da evitare — vedi `procedura_operativa_NIDS.md`, regola
d'oro in cima al file):

```yaml
# suricata.yaml, vars -> address-groups
GOOD_NET: "[172.21.1.1,172.21.1.65,172.21.1.140,172.21.1.153,172.21.1.172]"
BAD_NET: "[172.21.1.129]"
```
```
# exam.rules
alert ip $GOOD_NET any <> $GOOD_NET any (msg:"Traffico lecito"; sid:1000001; rev:1;)
alert ip $BAD_NET any <> any any (msg:"TRAFFICO SOSPETTO"; sid:1000002; rev:1;)
```
Risultato verificato: 112 alert sid 1000001 (traffico lecito tra i 5 host), **2** alert sid
1000002 — entrambi su DHCP legittimo tra l'attaccante e il server (non sul poisoning, che resta
invisibile a Suricata). Dimostra bene il limite da scrivere nel report: la regola 2 rileva "è
coinvolto l'IP sospetto", non "sta succedendo qualcosa di malevolo".

### Gotcha incontrati (validi per qualunque esercizio Suricata)

- **`grep -c "<sid>"` su `eve.json` dà sempre 0** anche se la regola funziona: nel JSON il campo
  si chiama `signature_id`, annidato dentro `"alert":{...}` — `sid` è solo il nome nella sintassi
  della regola. Usa `grep -c '"signature_id":<numero>'`. Se il dubbio persiste, verifica prima
  che ci siano alert *di qualunque tipo* con `grep -c '"event_type":"alert"' eve.json`.
- Variabili custom (`$GOOD_NET`, `$BAD_NET`) vanno definite in `suricata.yaml` **senza** `#`
  davanti (a differenza delle alternative `#HOME_NET: ...` già presenti nel file, che sono
  varianti disattivate tra cui scegliere) — e lanciare Suricata con `-c <tuo-yaml>`, non quello
  di default, altrimenti le variabili non esistono e la regola non parsa.

---

## Terzo caso: buffer-overflow probe via SMTP, padding incrementale (10 luglio 2025)

> Fonte: stesso HTML, `trace-2025-07-10.pcapng`. Soluzione ufficiale recuperata da un allegato
> collegato **senza** la dicitura "Soluzione" visibile (link diretto dopo il testo dell'esercizio,
> `report.txt`+`suricata.yaml`+`exam.rules`+`eve.json` in uno zip) — tienilo a mente: la ricerca
> del link va fatta per **ogni** pcap del pool, non solo dove compare la parola "Soluzione".

**Traffico legittimo**: ARP request/reply tra 6 host su 3 subnet diverse, ICMP ping tra due host,
HTTP GET legittimo, DNS. Punto di metodo dal report ufficiale: *"il fatto che alcuni di questi
scambi siano più consistenti di altri non è motivo sufficiente per classificarli come tentativi di
DoS, in quanto si tratta sempre di dialoghi completi 1:1"* — cioè volume alto da solo non basta,
serve anche guardare se è un dialogo normale (richiesta→risposta, sorgente unica) o un pattern
degenere (tante sorgenti verso una vittima, o richieste mai risposte).

**Attacco — variante nuova rispetto al primo caso (S10, sessione 47)**: buffer-overflow probe via
**SMTP** (non HTTP), nel campo `DATA` del payload — ma qui il padding **cresce di 1 byte alla
volta** ad ogni tentativo (non un'unica stringa lunga fissa come `AAAA...BBBB`), seguito sempre da
un marcatore fisso a 4 byte (`ABCD`). È lo stesso obiettivo del primo caso (trovare l'offset esatto
del return address via trial-and-error) ma con una **strategia di ricerca diversa**: incrementale
invece che a payload singolo — riconoscerlo richiede guardare la **sequenza** di più pacchetti
consecutivi (lunghezza del padding che cresce ad ogni richiesta), non un singolo pacchetto isolato.

```
alert tcp 192.168.101.129 any -> 192.168.103.172 25 (msg:"ALERT ATTACCO DI BOF VIA SMTP"; content:"ABCD"; sid:100001;)
```
Nota: regola volutamente semplice — matcha solo sul marcatore fisso `ABCD` in porta 25/tcp, non
serve intercettare ogni singola lunghezza di padding, il marcatore finale è invariante e basta.

---

## Quarto caso: ARP scan + TCP port scan combinati (10 settembre 2025)

> Fonte: stesso HTML, `dump_20250910.pcapng`. ⚠️ **Attenzione**: l'esercizio gemello
> `dump_20251030.pcapng` (30 ottobre 2025) ha testo e allegato-soluzione **identici byte per byte**
> a questo — anche il testo dell'esercizio del 30/10 contiene per errore il nome del file del
> 10/09 nel comando `gunzip`. Sembra un refuso di chi ha preparato la pagina (pagina duplicata e
> non aggiornata), non due esercizi realmente distinti — se ti capita `dump_20251030.pcapng`
> all'esame, trattalo come questo stesso caso.

**Traffico legittimo**: DNS tra 3 host e i rispettivi router, ARP (alcune richieste legittime
mescolate a quelle dello scan), ICMP, HTTP, SMTP — stesso schema "rumore di fondo multiplo" degli
altri casi.

**Attacco — combinazione di DUE tecniche mai viste insieme finora**:
1. **IP scan via ARP** (stessa firma della fase 1 del nostro caso di oggi, 12/01/2026): il router
   riceve richieste ARP per tutti gli IP delle subnet coinvolte — ricognizione degli host vivi.
2. **Port scan TCP**: la sorgente `10.33.33.174` manda **SYN** verso gli host "vivi" trovati al
   punto 1, su tutte le porte comuni. Il segnale è nella **risposta**: quasi sempre **TCP RST**
   (porta chiusa, connessione rifiutata immediatamente) tranne che su `80` e `443` (porte
   effettivamente aperte, lì la connessione si comporta diversamente) — è il fingerprint classico
   di un TCP SYN scan (es. `nmap -sS`): tante connessioni tentate, quasi tutte respinte a vuoto,
   un numero ristretto che "risponde per bene".

```
alert tcp 10.33.33.174 any -> $HOME_NET any (msg:"Scanning detected"; sid:10000001; rev:1;)
```
Nota metodologica dal report ufficiale: *"in assenza di criteri più specifici, si può scrivere una
regola per allertare di qualsiasi pacchetto provenga dall'host attaccante"* — stesso principio di
approssimazione già visto con `$BAD_NET` nel secondo caso (quando il pattern esatto è complesso da
esprimere in una singola regola di contenuto, la scorciatoia accettabile è "flagga la sorgente
nota", non provare a descrivere ogni singola porta/pacchetto dello scan).

---

## Quinto caso: identificazione di protocollo (non ricerca di un attacco) — 10 febbraio 2023

> Fonte: stesso HTML, `esame_10_febbraio_2023.pcapng`. **Tipo di compito diverso dagli altri 4**:
> qui non si cerca "l'attacco", si identifica un protocollo/servizio a partire dal traffico.

**Consegna**: il pcap mostra diversi tentativi di autenticazione su un protocollo non dichiarato.
Identificare: protocollo, i 2 IP coinvolti, la/le porte. Hint ufficiale: *"avete un tool valido per
recuperare queste informazioni"* — cioè **Statistics → Protocol Hierarchy** (lo stesso primo passo
della procedura standard, qui è sufficiente da solo per rispondere, senza bisogno di Follow Stream
o analisi di frequenza).

**Risposta**: protocollo **TELNET** (testo in chiaro, per questo "tentativi di autenticazione" si
vedono direttamente nel payload), IP `192.168.56.1` ↔ `192.168.56.8`, porta **23**.

**Regola con feature mai vista prima — `flowbits`:**
```
alert tcp 192.168.56.1 41852 -> 192.168.56.8 23 (msg:"Flag detected"; flow:from_client; flowbits:set,logged_in; content:"sec:sec"; sid:100005; rev:1;)
```
- `flow:from_client` — matcha solo pacchetti nella direzione client→server della connessione (a
  differenza delle regole viste finora, che non specificavano una direzione all'interno del flow).
- `flowbits:set,logged_in` — **imposta un flag con nome** (`logged_in`) associato a quella
  connessione, leggibile/testabile da **altre regole successive** (`flowbits:isset,logged_in`) —
  serve a incatenare condizioni stateful su più pacchetti/regole della stessa sessione (es. "alert
  solo se PRIMA è avvenuto il login" — qui la regola *marca* il momento del login, non lo usa
  ancora, ma è il building block per farlo).
- `content:"sec:sec"` — il pattern di login catturato in chiaro nel payload Telnet.
- Con `payload-printable` abilitato in `suricata.yaml`, `eve.json` contiene il payload leggibile
  dei pacchetti — da lì si ricostruisce la flag frammentata (stessa tecnica del compito MQTT visto
  in `COMPITI_security.md`, mai ancora eseguita hands-on).
