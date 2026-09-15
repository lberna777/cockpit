# Procedura Operativa — Network Intrusion Detection (S10)

> Sequenza fissa di azioni/comandi da eseguire per qualunque pcap ti capiti all'esame.
> Non contiene teoria — solo l'algoritmo operativo. Per la struttura del report vedi
> `template_report_NIDS.md`; per un esempio completo, `modello_network_intrusion_detection.md`.

> ⚠️ **Regola d'oro: non saltare al sospetto.** Anche se trovi l'anomalia entro i primi
> minuti (es. un protocollo con volume assurdo in Protocol Hierarchy), **completa comunque
> gli step 2-3 su tutti gli altri gruppi di traffico** prima di scrivere la regola Suricata —
> non solo su quello sospetto. La consegna chiede sempre di descrivere anche il traffico
> lecito, e la lista degli host "buoni" (necessaria per molte regole, es. `$GOOD_NET`) va
> **verificata isolando le conversazioni di ciascun protocollo legittimo**, non assunta per
> simmetria con quello che hai già trovato sull'attaccante. Saltare questo passo funziona
> "per caso" quando i conti tornano lo stesso, ma è il tipo di scorciatoia che a esame,
> sotto pressione, porta a un elenco sbagliato o incompleto.

## 1. Apertura e vista d'insieme

```
wireshark <file>.pcap
```
- Ordina per colonna **Source** (click sull'intestazione) → conta quanti IP/subnet distinti compaiono.
- **Statistics → Protocol Hierarchy** → espandi tutti i nodi (tasto destro → Expand All, o `+` da tastiera) → annota ogni protocollo applicativo presente e la sua percentuale/conteggio pacchetti.
- Fai la somma: se i protocolli applicativi etichettati (SMTP, HTTP, DNS, ecc.) non coprono il totale di TCP/UDP, quella differenza è la prima pista da seguire.

### Se ARP è anomalo: opcode + relazione MAC↔IP

ARP non ha "stream" da seguire e non copre porte, quindi va trattato a parte rispetto al
resto della procedura. Due errori da evitare: fermarsi al primo pattern trovato senza
controllare che copra tutto il traffico ARP osservato, e non separare request da reply
(sono due minacce diverse, non varianti dello stesso fenomeno).

1. **Fai quadrare i numeri prima di tutto.** Se il tuo filtro isola N pacchetti ma il
   Protocol Hierarchy ne segnalava M > N per ARP, la differenza M-N è traffico ARP che
   non hai ancora spiegato — vai a guardarlo, non fermarti alla prima pista che "funziona".
2. **Dividi sempre in due indagini separate per opcode:**
   - `arp.opcode==1` (**request**, "chi ha X?") → rischio: enumerazione/scan. Raggruppa
     per Sender IP e conta i target distinti (vedi scorciatoia tshark sopra): un numero
     vicino alla dimensione della subnet = scansione a tappeto.
   - `arp.opcode==2` (**reply**, "X è mio") → rischio: spoofing/poisoning, perché è
     un'*affermazione* che gli altri host credono vera e usano per instradare traffico
     (a differenza della request, che è solo una domanda).
3. **Per le reply, cerca la relazione 1 MAC → molti IP:**
```
tshark -r <file> -Y "arp.opcode==2" -T fields -e arp.src.hw_mac -e arp.src.proto_ipv4 | sort | uniq -c | sort -rn
```
   Un host legittimo ha un MAC che dichiara **un solo** IP (il proprio). Un MAC che
   dichiara **più IP diversi** sta mentendo su più identità — è la firma dello spoofing
   (a meno che non sia un router/NAT, da escludere dal contesto).
4. Uno stesso IP sorgente può comparire in entrambe le fasi (prima scan, poi spoofing
   mirato solo sui target che lo scan ha confermato vivi) — non sono alternative, controllale
   entrambe anche se la prima che trovi "spiega già tutto".

## 2. Isolare i gruppi di conversazioni

```
Statistics → Conversations → tab TCP (o UDP)
"Limit to display filter" attivo se hai già un filtro (es. tcp && !smtp && !http)
```
- Cerca pattern **ripetuti** (stesse due IP, stessa porta destinazione, porta sorgente sempre diversa) → sono lo stesso tipo di flusso ripetuto N volte.
- Nota quali coppie IP/porta compaiono, quanti pacchetti/byte per ciascuna.

### Scorciatoia: isolare/contare un campo preciso quando Conversations non basta (es. ARP)

Conversations copre bene TCP/UDP, ma per protocolli senza porte (ARP, ICMP) o quando serve
un **conteggio** (es. "quanti IP distinti interroga questa sorgente?") il percorso è: costruisci
il filtro dalla GUI, poi lo riusi in `tshark` — non serve ricordare a memoria i nomi dei campi.

1. Clicca un pacchetto del gruppo sospetto, espandi il protocollo nel pannello dettagli (in basso).
2. Sul campo che ti interessa (es. "Sender IP address"): **tasto destro → Apply as Filter → Selected**
   → Wireshark scrive da solo il filtro (es. `arp.src.proto_ipv4 == 172.21.1.129`) e lo applica,
   così vedi subito se il risultato è quello giusto.
3. Per il nome tecnico di un altro campo da estrarre (es. "Target IP address"): **click singolo**
   sul campo → il nome (es. `arp.dst.proto_ipv4`) appare in basso a sinistra nella barra di stato.
4. Riusa lo stesso filtro/campo in tshark:
```
tshark -r <file> -Y "<filtro dal passo 2>" -T fields -e <campo dal passo 3> | sort -u | wc -l
```
`sort -u` = valori unici, `wc -l` = quanti sono — se il numero si avvicina alla dimensione della
subnet (es. ~254 per un /24) è una scansione a tappeto, non traffico normale.

## 3. Ispezionare il contenuto

Su una riga di ciascun gruppo trovato: tasto destro (o pulsante "Follow Stream...") → **Follow → TCP/UDP Stream**.

Per ogni stream, rispondi a queste 4 domande (in quest'ordine):
1. La richiesta è sintatticamente valida per il protocollo?
2. Path/parametri/contenuto sono nella norma o contengono qualcosa di anomalo (stringhe di riempimento, comandi, caratteri di escape, pattern non testuali)?
3. La risposta è quella attesa (status code, contenuto) o rivela qualcosa (errore, dato sensibile)?
4. Confrontalo con un gruppo che sospetti legittimo dello stesso protocollo — la differenza salta all'occhio?

## 4. Verificare la frequenza (se il contenuto da solo non basta)

```
Wireshark → View → Time Display Format → Seconds Since Previously Displayed Packet
```
- Guarda la colonna Time sui pacchetti dello stesso gruppo: millisecondi tra un pacchetto e l'altro = automatismo/flood; secondi o più = comportamento umano o probe periodico legittimo.
- Confronta sempre il gruppo sospetto con un gruppo legittimo dello stesso protocollo — è la differenza relativa che conta, non il valore assoluto isolato.

## 5. Non dimenticare ICMP

```
Filtro Wireshark: icmp
```
Controlla sempre, anche se raramente contiene l'attacco — la consegna chiede tutti i tipi di traffico, non solo quello sospetto.

### Se vedi tanti TCP SYN con risposta RST: port scan

Firma diversa da tutte le altre di questa procedura (niente contenuto anomalo nel payload — la
connessione TCP non arriva mai a completarsi). Pattern: una sorgente manda **SYN** verso una singola
vittima su **molte porte diverse**, la stragrande maggioranza delle risposte è **TCP RST** (porta
chiusa, rifiuto immediato) tranne un numero ristretto di porte che si comportano diversamente (SYN-ACK
= porta aperta) — è il fingerprint di un TCP SYN scan (es. `nmap -sS`). In Wireshark: `tcp.flags.syn==1 && tcp.flags.ack==0`
per isolare i SYN in uscita, poi confronta col volume di `tcp.flags.reset==1` in risposta dalla
stessa vittima. Spesso convive con uno scan ARP (fase di scoperta host, vedi sopra) fatto dalla
stessa sorgente subito prima — stesso principio "non fermarti alla prima pista": se trovi uno scan
ARP, controlla se la stessa sorgente fa *anche* uno scan di porte sugli host che ha scoperto vivi.

## 6. Scrivere ed eseguire la regola Suricata

Sintassi:
```
alert <proto> <src_net/host> <src_port> -> <dst_net/host> <dst_port> (msg:"..."; content:"<stringa trovata>"; <buffer_keyword se serve, es. http_uri>; sid:<numero univoco >=1000000>; rev:1;)
```
- Usa le **reti** (`/24`) se la consegna lo richiede esplicitamente, non i singoli IP osservati.
- `content` = la stringa/pattern trovato al passo 3. Se serve restringere a un campo specifico (URI, header, ecc.), aggiungi il buffer keyword giusto **subito dopo** il content che modifica.

### Se l'attacco è sotto il livello IP (es. ARP spoofing): non puoi rilevarlo direttamente

Suricata analizza solo dagli header IP in su — non ha un modo pulito per condizionare un
alert sul contenuto di un pacchetto ARP o su un MAC address (protocollo `ip`/`tcp`/`udp`/...
richiede un header IP che ARP non ha). In questi casi non provare a inseguire l'attacco:
approssimalo con un elenco di indirizzi noti-buoni/noti-cattivi, verificato con gli step 1-3.

1. In `suricata.yaml`, sezione `vars: → address-groups:` (accanto a `HOME_NET`), definisci le
   tue variabili:
```yaml
    GOOD_NET: "[ip1,ip2,...]"   # host legittimi verificati (step 1-3)
    BAD_NET: "ip_attaccante"    # identificato con l'analisi (es. relazione MAC↔IP per ARP)
```
2. Due regole standard:
```
alert ip $GOOD_NET any <> $GOOD_NET any (msg:"Traffico lecito"; sid:1000001; rev:1;)
alert ip $BAD_NET any <> any any (msg:"TRAFFICO SOSPETTO"; sid:1000002; rev:1;)
```
   - Regola 1: scatta solo se **sia** sorgente **sia** destinazione sono in `GOOD_NET` — log di
     baseline, non rileva nulla di per sé.
   - Regola 2: scatta se **un lato qualunque** (grazie a `<>`) è `BAD_NET`, indipendentemente
     dall'altro (`any any`) — approssima "traffico IP reale coinvolge l'attaccante", non
     l'attacco in sé (può includere falsi positivi: traffico innocuo dello stesso host).
3. Esegui Suricata con `-c <tua-copia-di-suricata.yaml>` (non quella di default) perché le
   variabili custom devono essere lette dal file che le contiene.
4. Nel report, dichiara esplicitamente il limite: "Suricata non può rilevare l'attacco a
   questo livello, la regola approssima flaggando il traffico IP dell'host malevolo".

Esecuzione:
```
mkdir -p <dir_output>
suricata -r <file>.pcap -S exam.rules -l <dir_output>
```
- Aggiungi `-c <tua-copia-di-suricata.yaml>` se hai definito variabili custom (es. `$GOOD_NET`/`$BAD_NET` sopra) — senza, Suricata usa il config di default dove quelle variabili non esistono e la regola non parsa.
- Nessun errore di parsing all'avvio → regola sintatticamente valida.

## 7. Verificare che la regola funzioni

Nel JSON il campo non si chiama `sid` (quello è solo il nome usato nella sintassi della
regola) ma **`signature_id`**, annidato dentro l'oggetto `"alert":{...}` — `grep -c "<sid>"`
da solo non lo trova mai, sembra sempre 0 alert anche quando la regola funziona.
```
grep -c '"signature_id":<sid>' <dir_output>/eve.json      # conta gli alert
grep '"signature_id":<sid>' <dir_output>/eve.json | head -1   # un esempio completo
```
Se il conteggio è **davvero** 0 (verificato prima con `grep -c '"event_type":"alert"' <dir_output>/eve.json`
che il file contenga alert *di qualunque regola* — se anche quello è 0 il problema è nella
regola, non nel grep): ricontrolla rete/porta/direzione invertite, buffer keyword mancante,
o che il content sia scritto esattamente come appare nel payload.

## 8. Scrivere report.txt

Segui `template_report_NIDS.md`. Non lasciare terminale grezzo incollato: solo comando + risultato rilevante, riscritti puliti.

## 9. Confezionare la consegna

```
cp /etc/suricata/suricata.yaml .
cp <dir_output>/eve.json .
ls -la
```
Verifica che ci siano: `report.txt`, `exam.rules`, `suricata.yaml`, `eve.json`.
