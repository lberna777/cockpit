# Lezione — Modulo S8: LAB — Individuare e filtrare attacchi
**Corso**: Lab Sicurezza Informatica T
**Materiale**: "LAB — Individuare e filtrare attacchi [15 apr]" (trascrizione integrale in `security_teoria_notebooklm/S08_individuare_filtrare_attacchi/`)
**Prerequisiti**: S1 (Enumerazione — nmap e lettura dei fingerprint), S3 (Web security — command injection e bypass della sanitizzazione), S4 (Binary exploits — buffer overflow e bisezione dell'offset), S5 (Firewall/nftables — packet filtering, NAT, conntrack), S10 (NIDS — Wireshark e regole Suricata)
**Nota esame**: modulo di **riepilogo trasversale** — non introduce concetti nuovi, ma li applica tutti insieme sullo stesso scenario. Conta per il **quiz teorico (40%)**, con domande anche sulla sintassi vista in laboratorio (comandi nmap/nc, sintassi delle regole Suricata, chain/hook nftables per SNAT vs DNAT); c'è penalità per risposta sbagliata.

---

## Come leggere questa lezione

Questo laboratorio è deliberatamente diverso dagli altri: non insegna una tecnica nuova, ma mette in fila l'intera *kill chain* di un attacco e la sua contromisura difensiva su un'unica infrastruttura. Il percorso è lineare e va letto come un'unica storia: si **enumera** la rete (S1), si **sfrutta** un servizio binario con un buffer overflow (S4) e un servizio web con una command injection (S3), si **cattura e analizza** il traffico dei due attacchi riusciti (S10), si scrivono le **regole Suricata** che li riconoscono (S10) e infine si costruisce il **packet filter nftables** che, a valle, regola chi può parlare con chi, NAT compreso (S5). Per ogni tecnica trovi il *meccanismo* (come funziona a basso livello) e la *visione* (perché conta, cosa insegna, con quale altro modulo si collega). Il valore d'esame di questo modulo è proprio la **trasferibilità**: se sai rifare qui ciò che hai imparato altrove, i concetti sono assimilati e non mnemonici.

## La visione d'insieme / threat model

Lo scenario è una piccola rete instradata: un **client** (10.1.1.1) che raggiunge, attraverso due router in cascata **r1** e **r2**, due server — **s1** (10.2.2.1) e **s2** (10.3.3.1). A differenza dell'esercitazione netfilter di S5, qui il **routing è completo tra tutti gli host**: ogni macchina può in linea di principio raggiungere ogni altra, e questo rende il packet filter finale l'unico vero confine. s1 espone un **servizio binario vulnerabile** sulla porta 8000, s2 un **webserver vulnerabile a command injection** sulla porta 5000; entrambi espongono anche SSH (22) e un secondo servizio "incrociato" che conta solo nella parte di filtraggio. r2 è il router centrale e sarà anche il punto in cui vive il **NAT** (SNAT e DNAT).

Dal punto di vista dell'**attaccante**, il threat model è quello di chi parte dal client con accesso di rete e deve: (1) capire cosa c'è (enumerazione), (2) ottenere esecuzione di codice remoto sui server (pwn del binario, injection sul web), (3) muoversi in modo che il traffico prodotto sia il più possibile "normale" per non farsi notare. Dal punto di vista del **difensore**, il threat model è duplice e complementare: **rilevare** gli attacchi che passano (con un NIDS, Suricata, che ispeziona il payload e cerca firme concrete) e **prevenire/contenere** ciò che non deve nemmeno poter transitare (con un packet filter a default-drop, che decide *se* un pacchetto passa, indipendentemente dal suo contenuto). La lezione tiene sempre le due prospettive affiancate: ogni tecnica offensiva ha subito accanto la sua rilevazione o il suo filtro.

## 1. Enumerazione (richiama S1)

**Comando**: `nmap -sV -p- 10.2.2.1` (e analogo per 10.3.3.1). `-p-` scansiona tutte le 65535 porte, `-sV` tenta il *service/version detection* aprendo una connessione e leggendo il banner/la risposta.

**Meccanismo**: su s1, nmap trova la 22 (OpenSSH) e la **8000** che risponde con una riga vuota (`\r\n`) e resta "unrecognized" — comportamento tipico di un **binario in ascolto su socket**, non di un webserver. Su s2 trova la 22 e la **5000**, anch'essa "unrecognized" per nome, ma il *fingerprint grezzo* rivela redirect HTTP 308, header `Server: Werkzeug/2.2.2 Python/3.11.2` e pagine d'errore Flask: è chiaramente un **servizio web** (Flask/Werkzeug), anche se nmap non ne riconosce la firma esatta.

> **Visione (perché conta)**: la lezione del docente è metodologica e va ricordata per il quiz. Primo: conviene **prima una scansione leggera ad ampio spettro, poi approfondire** solo le porte attive (`-sV -p-` su tutte le porte è lento; in generale si fa il contrario per risparmiare tempo). Secondo, e più importante: **non fidarsi del campo "SERVICE"**. Quando nmap dice "unrecognized", i dettagli grezzi della risposta (banner, redirect, header) bastano comunque a classificare il servizio. Riconoscere "Werkzeug/Flask" da un fingerprint incompleto è esattamente la lettura critica del fingerprint di S1.

**Collegamento a S1**: stesso strumento, stessa logica ("porta aperta ≠ servizio identificato"). Le regole firewall che scriverai al punto 7 sono precisamente ciò che questa `nmap`, rifatta dopo, vedrebbe come `filtered` invece di `open`.

## 2. Accesso al servizio binario — buffer overflow (richiama S4)

**Strumento**: lo script `/client.sh`, il cui cuore è un ciclo che invia un numero crescente di `A` seguito da un indirizzo di ritorno fisso:

```bash
for i in {1..50} ; do
  perl -e 'print "A"x'$i',"\xad\x61\x55\x56","\n"' | nc "$1" 8000
done
```

**Meccanismo**: è **lo stesso schema di "secret_function_remote" di S4**. Si invia riempimento (`A`) di lunghezza crescente più un *return address* fisso (`\xad\x61\x55\x56`). Finché il riempimento è troppo corto, il return address non arriva a sovrascrivere il punto giusto sullo stack; quando la lunghezza è esatta, l'indirizzo di ritorno salvato viene sovrascritto con il valore voluto e l'esecuzione "salta" lì. Nel test, al contatore **16** il processo **resta appeso in attesa di input** invece di crashare: segnale che a quell'offset l'overflow ha funzionato (l'indirizzo target è codice che aspetta input da stdin). L'offset è quindi **16 byte**; il return address target è `0x565561ad`, scritto `\xad\x61\x55\x56` in **little-endian**.

Lo sfruttamento riproduce l'overflow a offset 16 e poi passa `cat` per digitare comandi sulla shell remota ottenuta:

```bash
( perl -e 'print "A"x16,"\xad\x61\x55\x56","\n"' ; cat ) | nc 10.2.2.1 8000
# id → uid=0(root) ... ; hostname → s1
```

**Risultato**: shell **root** su s1.

> **Visione (perché conta)**: la ricerca dell'offset è una **bisezione comportamentale** — non serve un debugger, basta osservare a quale lunghezza il comportamento del programma cambia (da crash/nulla a "appeso in attesa"). Il pattern `( exploit ; cat ) | nc` è idiomatico: la subshell prima "spara" il payload che dirotta l'esecuzione, poi `cat` tiene aperto lo stdin per interagire con la shell che ne risulta. È letteralmente il meccanismo di S4 riproposto su un servizio di rete.

**Collegamento a S4**: identico schema di bisezione dell'offset e di sfruttamento via `nc`; l'unica differenza è che il bersaglio è raggiunto attraverso la rete anziché in locale.

## 3. Accesso al servizio web — command injection (richiama S3)

**Strumento**: il browser testuale `lynx` (il tasto `=` mostra l'URL completa della pagina). Il webserver di s2 accetta un parametro **`filepath`** e internamente esegue in shell il comando `stat <filepath>`.

**La vulnerabilità**: l'applicazione **filtra solo i caratteri `;` e `|`** (due caratteri — nel testo sorgente comparivano come "`;` e `|`", dove "e" è la congiunzione italiana, non un terzo carattere filtrato) prima di passare il parametro alla shell. È una **blacklist incompleta**: blocca alcuni separatori "ovvi" (il `;` che concatena comandi, la pipe `|`) ma non tutti i modi che la shell offre per eseguire altro codice.

**Meccanismo del bypass**: si aggira il filtro con costrutti che *non contengono* nessuno dei caratteri vietati:
- **command substitution** `$(...)`: la shell esegue il comando interno e ne sostituisce l'output. Non usa `;` né `|`, quindi passa indenne.
- **concatenamento con `&` / `&&`** (in URL: `%26`): esegue un secondo comando in sequenza. Anche `&` non è nella blacklist.

Esempi (URL-encoded — `%20` = spazio, `%2F` = `/`, `%26` = `&`):

```bash
lynx 'http://10.3.3.1:5000/stat?filepath=$(cat%20%2Fetc%2Fpasswd)'          # esfiltra /etc/passwd
lynx 'http://10.3.3.1:5000/stat?filepath=%2Fetc%2Fpasswd%26cat%20%2Fetc%2Fpasswd'  # variante con &
lynx 'http://10.3.3.1:5000/stat?filepath=$(find%20/%20-name%20flag.txt)'    # trova → /tmp/flag.txt
lynx 'http://10.3.3.1:5000/stat?filepath=$(cat%20%2Ftmp%2Fflag.txt)'        # esfiltra la flag
```

La catena è: **enumera il parametro vulnerabile → verifica il filtro parziale → bypass con command substitution → localizza il target (`find`) → esfiltra (`cat`)**.

> **Visione (perché conta)**: è l'errore classico della **sanitizzazione a blacklist** ("vieto ciò che conosco") contro la **whitelist** ("permetto solo ciò che serve"). Un filtro parziale su un sottoinsieme di metacaratteri non copre mai l'intero linguaggio della shell: basta un costrutto non previsto (`$(...)`, `&`, backtick) per evadere. La difesa corretta non è "aggiungere `&` alla lista" ma non passare mai input non fidato a una shell (whitelist rigida, o API che non invocano una shell).

**Collegamento a S3**: stessa metodologia di command injection / bypass della sanitizzazione vista in Web security, applicata qui a un endpoint `stat`.

## 4. Analisi del traffico — criteri di triage in Wireshark (richiama S10)

Si cattura il traffico dei due attacchi riusciti con `tcpdump`, separando i due servizi:

```bash
tcpdump -i eth1 -w /host/pwn.pcap    # su r2, lato s1
tcpdump -i eth3 -w /host/web.pcap    # su r2, lato s2
```

Poi si aprono le catture in Wireshark. Il contenuto concettuale è il **criterio di selezione dei pacchetti "interessanti"**, formulato *per esclusione*:
- **connessioni complete** — si escludono i SYN flood (in cui non si vedrebbero gli ACK di risposta);
- **da/per gli stessi endpoint** — si esclude un'enumerazione di host o porte (che genererebbe traffico verso molti indirizzi/porte diversi);
- **non protocolli che ingannano la consegna** — si escludono DHCP o ARP poisoning (che manipolano la risoluzione degli indirizzi, non il contenuto applicativo).

> **Visione (perché conta)**: è un **triage per esclusione** che restringe migliaia di pacchetti a poche connessioni plausibili *prima* di leggerne il contenuto. Il principio è quello di S10: non tutto il traffico anomalo è un attacco, e non tutti gli attacchi sono rumorosi. Filtrando per *tipo di connessione*, *endpoint* e *protocollo* si isola rapidamente ciò che vale la pena ispezionare a fondo.

**Collegamento a S10**: identico criterio di triage del traffico già praticato con Wireshark nel modulo NIDS.

## 5. NIDS — regole Suricata (richiama S10)

> **Nota di sintassi da esame**: le regole si scrivono qui su più righe per leggibilità, ma **Suricata v7 le esige su un'unica riga**.

### Regola WEB — rilevare l'esfiltrazione di `flag.txt`

Invece di inseguire ogni possibile metacarattere, ci si concentra sul **tentativo concreto**: esfiltrare `flag.txt` tramite uno dei tre meccanismi di bypass noti (`$(`, backtick `` ` ``, `&`).

```
alert http any any -> $WEB_SERVERS 5000 (
    msg:"Tentativo di rubare la flag";
    flow:to_server,established;
    http.uri; http_decode_uri;
    content:"/stat"; content:"filepath=";
    pcre:"/\/stat\?filepath=.*[\$\`\&].*flag\.txt/i";
    classtype:web-application-attack; sid:9000002; rev:1;
)
```

**Meccanismo**: `flow:to_server,established` limita l'ispezione al traffico client→server di connessioni già stabilite; `http.uri` + `http_decode_uri` normalizzano l'URI (decodificano il percent-encoding, così `%26` torna `&` prima del match); i due `content` restringono all'endpoint giusto; il `pcre` è la firma vera: cerca `/stat?filepath=` seguito da almeno uno dei tre caratteri di bypass e poi da `flag.txt`. `$WEB_SERVERS` è una variabile da impostare in `/etc/suricata/suricata.yaml`. Sulla cattura: **2 alert**.

### Regola PWN — rilevare il buffer overflow

```
alert tcp any any -> 10.2.2.1 8000 (
    msg:"BOF verso 0x565561ad";
    flow:to_server,established;
    detection_filter:track by_src, count 10, seconds 60;
    content:"|ad 61 55 56|";
    classtype:attempted-admin; sid:9000001; rev:1;
)
```

**Meccanismo (punto d'esame)**: la firma **non è la sequenza di `A`**. Il riempimento è solo il metodo con cui l'attaccante cerca l'offset e potrebbe comparire per caso anche in traffico legittimo lungo. La firma affidabile è **l'indirizzo di ritorno target**, `0x565561ad`, cercato come sequenza di byte grezzi `|ad 61 55 56|` (notazione esadecimale di Suricata): è un valore specifico e concreto che non compare per caso. Il `detection_filter:track by_src, count 10, seconds 60` fa scattare l'alert **solo se la firma appare >10 volte in 60 s dallo stesso sorgente**, per ridurre i falsi positivi: un singolo pacchetto con quei byte può essere casuale, una raffica ripetuta è un indicatore forte. Sulla cattura: **3 alert**.

> **Visione (perché conta)**: una buona firma NIDS si aggancia a ciò che è **invariante e specifico** dell'attacco (l'indirizzo di ritorno, la catena esatta di esfiltrazione), non a ciò che è variabile e rumoroso (la lunghezza del padding). E `detection_filter` incarna il compromesso fondamentale del NIDS: sensibilità vs falsi positivi.

**Collegamento a S10**: firma su contenuto/pattern binario e uso di `detection_filter` per il tuning dei falsi positivi sono esattamente i costrutti Suricata di S10.

## 6. Packet filtering con NAT (richiama S5)

Ultimo passo: configurare i packet filter di **tutte** le macchine (`nftables`) per ottenere esattamente questo, con **default-drop** ovunque (INPUT/OUTPUT/FORWARD):

1. SSH del **client** raggiungibile **solo da r1**.
2. SSH di **s1** raggiungibile **solo dal client**, ma s1 deve vedere la connessione come proveniente da **r2** → **SNAT** su r2.
3. SSH di **s2** raggiungibile **solo dal client**, che lo raggiunge come se fosse esposto da **r2 sulla porta 222** → **DNAT** su r2.
4. I servizi non-SSH: **solo s2→s1:8000** (4/a) e **solo s1→s2:5000** (4/b).
5. **Tutto il resto è vietato**.

### Il pattern generale (da ricordare per qualunque variante)

- **Host non-router** (client, s1, s2): chain `INPUT`/`OUTPUT` con `policy drop`, eccezione per `lo`, poi **una coppia di regole per ogni comunicazione permessa** — una per l'**andata** (match sulla porta di destinazione, `dport`) e una per il **ritorno** (match sulla porta sorgente, `sport`, quasi sempre con `ct state established`).
- **Router** (r1, r2): stesso schema ma nella chain `FORWARD`, con `iif`/`oif` espliciti per instradare tra le interfacce giuste. r1 è un router *puro* (solo FORWARD, niente NAT); r2 è un router *con NAT*.
- **Il conntrack (`ct state established`) gestisce da solo il traffico di ritorno**, sia per le connessioni normali sia per quelle NAT-ate: non si scrive mai la regola "inversa" del NAT a mano.

### SNAT vs DNAT — la distinzione da non confondere

Questa è la **zona grigia esplicitamente segnalata** dal materiale, ed è il punto più facile da sbagliare al quiz. Entrambi i requisiti (2) e (3) collegano il client a un server passando per r1→r2, ma usano NAT opposti:

- **Requisito 2 → SNAT** (Source NAT): si maschera la **sorgente**. Il client raggiunge l'indirizzo *reale* di s1 (10.2.2.1), ma r2 riscrive l'IP sorgente in uscita così che **s1 creda di parlare con r2** invece che col client. La consegna lo dice con "mascherato **come se la connessione provenisse da** r2". Regola chiave, in **POSTROUTING** su r2 (l'ultimo hook prima dell'uscita):
  ```nft
  chain POSTROUTING { type nat hook postrouting priority srcnat; policy accept;
      oif eth1 ip saddr 10.1.1.1 ip daddr 10.2.2.1 snat to 10.2.2.254 }
  ```
- **Requisito 3 → DNAT** (Destination NAT): si maschera la **destinazione**. Il client si connette a un indirizzo/porta *finti* (10.9.9.2:222), e r2 riscrive destinazione+porta verso il server *reale* (10.3.3.1:22). La consegna lo dice con "che lo può raggiungere **come se fosse esposto da** r2 sulla porta 222". Regola chiave, in **PREROUTING** su r2 (il primo hook, prima della decisione di routing):
  ```nft
  chain PREROUTING { type nat hook prerouting priority dstnat; policy accept;
      iif eth2 ip saddr 10.1.1.1 ip daddr 10.9.9.2 tcp dport 222 dnat to 10.3.3.1:22 }
  ```

> **Il modo mnemonico per non confonderli**: **SNAT cambia chi sembra il mittente** (va in **POSTROUTING**, "dopo" — quando il pacchetto sta per uscire e non serve più decidere dove instradarlo); **DNAT cambia dove sembra andare** (va in **PREROUTING**, "prima" — deve agire *prima* della decisione di routing, perché è proprio la destinazione riscritta a determinare dove il pacchetto verrà instradato). "S come Source come POSTROUTING (uscita)", "D come Destination come PREROUTING (entrata)". La priority lo conferma anche nel nome: `dstnat` in prerouting, `srcnat` in postrouting.

### NAT si aggiunge, non sostituisce il filtro

Punto cruciale: anche con SNAT/DNAT attivi, le regole `filter`/`FORWARD` **restano necessarie**. Il NAT decide *quali indirizzi/porte* si vedono; il filtro decide *se* il pacchetto passa. Sono due decisioni ortogonali. Nel `r2.nft`, infatti, accanto alle regole `nat` ci sono comunque le coppie FORWARD per (2), (3), (4/a) e (4/b). E per il ritorno del NAT non serve nulla di esplicito: il **conntrack** ricorda l'associazione originale↔tradotto e "smaschera" automaticamente i pacchetti di risposta.

**Collegamento a S5**: SNAT vs DNAT, PREROUTING vs POSTROUTING, FORWARD vs INPUT/OUTPUT, conntrack per il traffico di ritorno — è esattamente il modello di netfilter/nftables di S5, qui calato su una topologia con NAT reale.

## Connessioni (riepilogo trasversale)

Questo modulo è un **banco di prova** che combina cinque moduli già trattati in profondità:
- **S1 (Enumerazione)**: `nmap -sV -p-` e lettura critica del fingerprint (riconoscere Flask/Werkzeug anche se "unrecognized").
- **S3 (Web security)**: command injection via `filepath`, bypass della blacklist con `$(...)`/`&`.
- **S4 (Binary exploits)**: buffer overflow, bisezione dell'offset (16 byte), return address in little-endian, sfruttamento `( payload ; cat ) | nc`.
- **S10 (NIDS)**: triage del traffico in Wireshark per esclusione; regole Suricata su firma binaria (`|ad 61 55 56|`) e su pattern URI, `detection_filter` per i falsi positivi.
- **S5 (Firewall)**: packet filter a default-drop, coppie andata/ritorno, SNAT/DNAT, hook, conntrack.

Non c'è nulla di nuovo: c'è la verifica di saper applicare tutto insieme.

## Domande di autoverifica (stile quiz teorico)

*Se non sei sicuro di una risposta, all'esame è meglio non rispondere — c'è penalità per errore.*

1. **Vero/Falso**: In una regola Suricata contro il buffer overflow, la firma più affidabile è la sequenza crescente di caratteri `A` inviata dall'exploit.
2. **Vero/Falso**: `nmap` ha classificato la porta 5000 di s2 come "unrecognized", quindi non è possibile determinare che tipo di servizio sia.
3. **Scelta multipla**: in quale chain/hook nftables va scritta la regola che fa apparire s2 (10.3.3.1:22) come se fosse esposto da r2 su 10.9.9.2:222? (a) PREROUTING, `type nat hook prerouting priority dstnat`, con `dnat to` — (b) POSTROUTING, `priority srcnat`, con `snat to` — (c) FORWARD, `type filter`, con `accept` — (d) INPUT, `priority dstnat`.
4. **Scelta multipla**: il requisito "SSH di s1 raggiungibile solo dal client, ma mascherato come se la connessione provenisse da r2" si realizza con: (a) DNAT in PREROUTING — (b) SNAT in POSTROUTING — (c) MASQUERADE in INPUT — (d) una semplice regola FORWARD senza NAT.
5. **Vero/Falso**: con SNAT/DNAT configurati su r2, occorre comunque scrivere le regole `filter`/FORWARD per il traffico interessato, perché il NAT non decide se un pacchetto passa.
6. **Vero/Falso**: per il traffico di ritorno di una connessione NAT-ata bisogna scrivere esplicitamente una regola "inversa" del NAT.
7. **Scelta multipla**: la command injection funziona perché il filtro applicativo (`;`, `e`, `|`) è aggirabile. Quale costrutto NON contiene alcun carattere filtrato e permette comunque di eseguire un secondo comando? (a) `; cmd` — (b) `| cmd` — (c) `$(cmd)` — (d) nessuno dei precedenti.
8. **Vero/Falso**: a offset 16 byte il processo binario resta appeso in attesa di input; ciò indica che il return address è stato sovrascritto e l'esecuzione è saltata all'indirizzo target (`0x565561ad`).
9. **Vero/Falso**: `\xad\x61\x55\x56` rappresenta l'indirizzo `0x565561ad` perché i byte sono in little-endian.
10. **Scelta multipla**: nel triage Wireshark, quale delle seguenti connessioni NON corrisponde ai criteri per il traffico d'attacco "interessante" cercato? (a) connessione TCP completa tra client e s2 — (b) un SYN flood senza ACK di risposta — (c) traffico da/verso gli stessi due endpoint — (d) nessuna, tutte sono interessanti.

### Risposte

1. **Falso** — la firma affidabile è l'indirizzo di ritorno target (`|ad 61 55 56|`), non i `A`, che sono solo il metodo di ricerca dell'offset e possono comparire per caso.
2. **Falso** — il fingerprint grezzo (redirect 308, header `Server: Werkzeug/... Python/...`, pagine Flask) identifica il servizio come web anche senza il nome esatto.
3. **(a)** — è un DNAT (destinazione riscritta), va in **PREROUTING** con `priority dstnat` e `dnat to 10.3.3.1:22`.
4. **(b)** — "provenisse da r2" = mascherare la sorgente = **SNAT in POSTROUTING** (`snat to 10.2.2.254`).
5. **Vero** — NAT e filter sono decisioni ortogonali: il NAT riscrive indirizzi/porte, il filter decide il passaggio; entrambi servono.
6. **Falso** — il conntrack gestisce automaticamente il "de-NAT" del traffico di ritorno; nessuna regola inversa esplicita.
7. **(c)** — `$(cmd)` è command substitution: non usa `;` né `|`, quindi passa il filtro (anche `&`/`%26` funzionerebbe).
8. **Vero** — l'esecuzione è saltata al target invece di crashare, e resta in attesa perché quell'indirizzo legge da stdin.
9. **Vero** — little-endian: i byte meno significativi per primi, `ad 61 55 56` → `0x565561ad`.
10. **(b)** — il SYN flood senza ACK è escluso dal criterio "connessioni complete"; le altre rientrano.

## Riepilogo

- **È un modulo di sintesi, non di novità**: enumerazione (S1) → pwn del binario (S4) → command injection sul web (S3) → analisi del traffico (S10) → firme Suricata (S10) → packet filtering con NAT (S5), tutto sullo stesso scenario.
- **Firme NIDS su ciò che è specifico**: l'indirizzo di ritorno `|ad 61 55 56|` (non i `A`) e la catena `filepath=...bypass...flag.txt`; `detection_filter` per abbattere i falsi positivi.
- **SNAT vs DNAT è la zona grigia da presidiare**: SNAT maschera la **sorgente** e vive in **POSTROUTING** (`srcnat`); DNAT maschera la **destinazione** e vive in **PREROUTING** (`dstnat`). Il NAT si **aggiunge** al filtro (non lo sostituisce) e il conntrack copre da solo il ritorno.

<!-- AUTO-LINKS:START -->
## 🔗 Collegati

- [[appunti_moduloS8_individuare_filtrare_attacchi]]

**Hub:** [[master_map_studio]] · [[concept_maps]] · [[metodo_studio_esami_pratici]]
<!-- AUTO-LINKS:END -->
