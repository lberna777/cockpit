# Appunti — Modulo S8: LAB — Individuare e filtrare attacchi
**Corso**: Lab Sicurezza Informatica T
**Lezione di riferimento**: `lezione_moduloS8_individuare_filtrare_attacchi.md`
**Stato**: modulo di riepilogo trasversale — non esistono appunti grezzi di Lorenzo. Questi appunti simulano il processo di lettura critica (domande plausibili + risposte inline), con particolare attenzione alla zona grigia SNAT/DNAT.

> ⚠️ Nota metodo: non essendoci grezzi, le domande qui sotto sono ricostruite anticipando i punti su cui Lorenzo tende a inciampare (distinzioni simili-ma-diverse, termini compressi, il *perché*). L'obiettivo dichiarato è **zero zone grigie** prima del quiz.

---

## La topologia — capire chi parla con chi

La rete è: **client (10.1.1.1) → r1 → r2 → {s1 (10.2.2.1), s2 (10.3.3.1)}**. r2 è il router centrale con tre interfacce (eth1 verso s1, eth2 verso r1, eth3 verso s2) e fa NAT.

> **Domanda**: perché è importante che "il routing è completo tra tutti gli host", visto che nell'esercizio di S5 non lo era?
> **Risposta**: perché sposta tutto il peso della sicurezza sul **packet filter**. Se la topologia già segmentasse la rete (come in S5), alcune comunicazioni sarebbero impossibili *fisicamente*, a prescindere dalle regole. Qui invece ogni macchina può raggiungere ogni altra a livello di instradamento: l'unico confine che impedisce, ad esempio, a un host qualsiasi di bussare alla porta SSH di s1 è la regola nftables. Questo è coerente con la lezione di S5 ("le regole non salvano una topologia che lascia altre strade aperte", e qui *tutte* le strade sono aperte di default): il default-drop del punto 7 non è un dettaglio, è l'intera difesa.

> **Domanda**: perché s1 ha un servizio sulla 8000 *e* uno sulla 5000, e s2 il contrario? Sembra ridondante.
> **Risposta**: è voluto, e serve solo alla parte di filtraggio (punto 4). Il servizio "principale" di s1 è il binario pwn sulla **8000**; quello di s2 è il web sulla **5000**. Ma il requisito 4 chiede che questi due servizi siano raggiungibili "solo l'uno dall'altro": quindi **s2 deve poter fare da client** verso s1:8000 (4/a) e **s1 deve poter fare da client** verso s2:5000 (4/b). Non è che s1 esponga un secondo servizio nuovo: è che s1, come *client*, parla con la 5000 di s2, e s2, come *client*, parla con la 8000 di s1. "Servizio secondario" nella tabella indirizzi significa "in questa comunicazione la macchina è dalla parte del client", non "ospita un secondo demone".

## Enumerazione — perché non fidarsi di "SERVICE"

> **Domanda**: cosa vuol dire che nmap dice "unrecognized despite returning data"? Se riceve dati, perché non riconosce il servizio?
> **Risposta**: `nmap -sV` confronta la risposta del servizio con un database di **firme note** (`nmap-service-probes`). "Unrecognized despite returning data" significa: il servizio *ha risposto* (quindi è vivo e ha un protocollo), ma quella risposta non combacia con nessuna firma in database, quindi nmap non sa incasellarla con un nome. Non è un fallimento: i dati grezzi ci sono e li puoi leggere tu. Su s2 la "risposta non riconosciuta" contiene un redirect HTTP 308 e l'header `Server: Werkzeug/2.2.2 Python/3.11.2` — leggendolo *tu*, capisci che è un web server Flask, anche se nmap non ha una firma esatta per quella versione. La lezione d'esame: **il campo SERVICE è un suggerimento, il fingerprint grezzo è la prova**.

> **Domanda**: la nota dice "prima scansioni leggere, poi approfondire" ma nell'esempio usa subito `-sV -p-`. Qual è la regola giusta?
> **Risposta**: la regola giusta è quella della nota (leggera prima, `-sV` mirato dopo). Nell'esercizio il docente usa direttamente `-sV -p-` solo per **sintetizzare** e mostrare il risultato in un colpo, ma avverte esplicitamente che nella pratica conviene il contrario, perché `-sV -p-` (version detection su tutte le 65535 porte) è **lento**. Sequenza consigliata: prima `nmap` veloce ad ampio spettro per trovare le porte aperte, poi `-sV` solo su quelle. All'esame, se ti chiedono la buona pratica, è "prima ampio e leggero, poi profondo e mirato".

## Buffer overflow — il pezzo di S4

> **Domanda**: perché "resta appeso in attesa di input" è la prova che l'overflow ha funzionato? Non dovrebbe crashare?
> **Risposta**: dipende da *dove* salta l'esecuzione. Quando il return address sullo stack viene sovrascritto con un valore a caso (offset sbagliato), il programma di solito **crasha** (segfault: salta su un indirizzo non valido). Quando invece l'offset è quello giusto e sovrascrivi il return address con l'indirizzo *voluto* (`0x565561ad`, che è codice valido che legge da stdin), l'esecuzione **salta lì con successo** e quel codice si mette **in attesa di input** — non crasha, non ritorna, resta appeso. Quindi "si appende invece di crashare o terminare" è esattamente il segnale che hai centrato l'offset (16 byte) e il salto è avvenuto. È lo stesso comportamento osservato in S4 con `secret_function_remote`.

> **Domanda**: cos'è la "bisezione dell'offset"? Perché si chiama così?
> **Risposta**: qui in realtà lo script prova le lunghezze **una per una** (`for i in {1..50}`), quindi è una ricerca lineare crescente più che una bisezione vera. Il termine "bisezione" (ereditato da S4) indica il *principio*: cerchi la lunghezza-soglia a cui il comportamento del programma cambia. Puoi trovarla dimezzando l'intervallo (bisezione classica: provo 25, se già va male so che è <25, provo 12, ecc.) oppure incrementando finché non scatta (come fa `client.sh`). L'idea condivisa è: **non serve conoscere in anticipo la dimensione del buffer, la si scopre osservando a quale lunghezza il comportamento cambia**. Qui cambia a 16.

> **Domanda**: cosa fa esattamente `( perl -e '...' ; cat ) | nc 10.2.2.1 8000`? Perché il `cat`?
> **Risposta**: è un pattern in due tempi dentro un'unica pipe verso `nc`:
> 1. `perl -e 'print "A"x16,"\xad\x61\x55\x56","\n"'` genera e "spara" il payload (16 byte di riempimento + return address) che dirotta l'esecuzione: dopo questo, sul server c'è una shell in attesa di comandi.
> 2. `cat` (senza argomenti) legge da **stdin** e lo ributta su stdout: serve a **tenere il canale aperto** e a inoltrare a `nc` ciò che tu digiti sulla tastiera. Senza `cat`, dopo il payload la pipe si chiuderebbe subito e non potresti interagire con la shell ottenuta.
> Le parentesi `( ... )` creano una subshell il cui output complessivo (payload + poi tutto quello che digiti) viene mandato a `nc`, cioè al servizio remoto. Risultato: shell root su s1, interattiva.

## Command injection — il pezzo di S3

> **Domanda**: il filtro blocca `;`, `e`, `|`. La `e` è la lettera "e"? E se `/etc/passwd` contiene delle "e", come fa `cat /etc/passwd` a funzionare?
> **Risposta — chiarito**: no, non è un terzo carattere filtrato. Nel testo sorgente la frase era "filtra solo i caratteri `;` e `|`" — la "e" è la **congiunzione italiana** tra i due caratteri elencati (`;` **e** `|`), non un carattere bloccato a sua volta. Il filtro blocca **due** caratteri, non tre. Il punto concettuale resta comunque quello che conta all'esame: la blacklist blocca i **separatori di comando "ovvi"** — il `;` (concatena comandi) e la pipe `|`. Il meccanismo di bypass non dipende dai singoli caratteri della blacklist, ma dal fatto che **esistono altri modi di eseguire comandi che non usano quei separatori**: la command substitution `$(...)` e il concatenamento `&`/`&&`. Nota che i payload esfiltrano `/etc/passwd` e `flag.txt` via URL-encoding (`%2F` per `/`, `%20` per lo spazio, `%26` per `&`): il filtro agisce sul valore del parametro `filepath`, e i costrutti scelti (`$(cat ...)`, `...&cat...`) passano perché non contengono un separatore vietato. In sede d'esame concentrati su: **blacklist parziale sui separatori → bypass con `$(...)`/`&` → il vero fix è la whitelist**.

> **Domanda**: qual è la differenza tra `$(...)`, `&` e `&&`? Sono intercambiabili qui?
> **Risposta**: fanno cose leggermente diverse ma nel contesto dell'injection ottengono lo scopo:
> - `$(comando)` — **command substitution**: la shell esegue `comando`, ne cattura l'output e lo *sostituisce* al posto di `$(...)`. Qui `stat $(cat /etc/passwd)` esegue prima `cat /etc/passwd` e ne inietta l'output; l'output del contenuto finisce nel messaggio d'errore di `stat` (che non trova un file con quel nome) e così viene esfiltrato.
> - `&` — esegue il comando **in background** e passa al successivo; usato come `A & B` avvia A e poi esegue B.
> - `&&` — esegue B **solo se A ha successo** (AND logico).
> Nel bypass sono equivalenti nell'obiettivo (eseguire un secondo comando accanto a `stat`), la differenza è il meccanismo. La trascrizione mostra sia `$(cat /etc/passwd)` sia la variante `stat /etc/passwd & cat /etc/passwd` (con `&` = `%26`).

## Analisi del traffico — i tre criteri di triage

> **Domanda**: i tre criteri di Wireshark (connessioni complete / stessi endpoint / no protocolli ingannevoli) sembrano scollegati. C'è una logica unica dietro?
> **Risposta**: sì, la logica è **escludere ciò che NON è l'attacco che cerchi**, per pattern grossolani, prima di leggere i payload. Ogni criterio esclude una classe di traffico:
> - **connessioni complete** → escludi i SYN flood / port scan a metà (che non completano l'handshake, non hanno ACK di risposta). L'attacco che cerchi (pwn, injection) è fatto di connessioni *complete e funzionanti*.
> - **stessi endpoint** → escludi le enumerazioni (che toccano molti IP/porte diversi). Il tuo attacco riuscito è una conversazione mirata *tra due host precisi*.
> - **niente DHCP/ARP** → escludi gli attacchi che manipolano la *consegna* (chi-è-chi in rete) invece del *contenuto*. Qui l'attacco è nel payload applicativo, non nella risoluzione degli indirizzi.
> È lo stesso triage per esclusione di S10: da migliaia di pacchetti a poche connessioni plausibili, senza aver ancora aperto un singolo payload.

## Suricata — le due regole

> **Domanda**: perché la firma del BOF è l'indirizzo `|ad 61 55 56|` e non la sequenza di `A`? Le `A` non sono più caratteristiche dell'attacco?
> **Risposta**: è il contrario. Le `A` sono solo **riempimento generico** scelto dall'attaccante — potrebbe usare qualunque byte, e sequenze lunghe di uno stesso carattere possono comparire per caso in traffico legittimo (upload, dati binari): firmerebbero un sacco di **falsi positivi**. L'indirizzo di ritorno `0x565561ad` invece è **specifico di quell'exploit**: è l'indirizzo concreto della funzione a cui l'attaccante vuole saltare, un valore che non ricorre per caso nel traffico normale. Per questo la regola cerca i byte grezzi `|ad 61 55 56|` (la notazione Suricata `|...|` = sequenza esadecimale). Principio generale NIDS: **firma su ciò che è invariante e specifico dell'attacco, non su ciò che è variabile e rumoroso**.

> **Domanda**: cosa fa `detection_filter:track by_src, count 10, seconds 60`? È obbligatorio?
> **Risposta**: non è obbligatorio, è un **tuning anti-falsi-positivi**. Dice a Suricata: "fai scattare l'alert solo se questa firma compare **più di 10 volte in 60 secondi**, contando **per indirizzo sorgente** (`track by_src`)". La ragione: un singolo pacchetto con quei byte potrebbe essere casuale; una *raffica* ripetuta in poco tempo dallo stesso mittente è un segnale molto più forte di un vero tentativo di exploit (che, ricorda, prova tanti offset in fila → tanti pacchetti). Incarna il compromesso centrale del NIDS: alzare la soglia riduce i falsi positivi ma rischia di perdere attacchi "lenti"; abbassarla è più sensibile ma più rumoroso.

> **Domanda**: nella regola web, a cosa servono `http.uri` e `http_decode_uri`? Non basta cercare la stringa?
> **Risposta**: no, e il motivo è l'**URL-encoding**. L'attacco arriva codificato (`%26` per `&`, `%2F` per `/`, ecc.). `http.uri` dice a Suricata di guardare specificamente il campo URI della richiesta HTTP (non tutto il pacchetto); `http_decode_uri` **normalizza** l'URI decodificando il percent-encoding, così che `%26` ridiventi `&` *prima* del match. Senza la normalizzazione, l'attaccante evaderebbe la firma semplicemente codificando i caratteri chiave. È lo stesso principio della normalizzazione vista in S10/S3: **normalizza prima di confrontare**, altrimenti la firma si aggira con banali ri-codifiche.

## SNAT vs DNAT — la zona grigia, sciolta del tutto

> **Domanda**: i requisiti 2 e 3 mi sembrano identici — in entrambi il client raggiunge un server via r1→r2. Perché uno è SNAT e l'altro DNAT? Come li distinguo senza sbagliare al quiz?
> **Risposta**: sono davvero simili nel percorso, e questa è *la* trappola del modulo. La chiave è chiedersi **cosa viene mascherato: il mittente o il destinatario?**
>
> | | Requisito 2 (SNAT) | Requisito 3 (DNAT) |
> |---|---|---|
> | Testo consegna | "mascherato **come se provenisse da** r2" | "come se fosse **esposto da** r2 sulla porta 222" |
> | Cosa si maschera | la **sorgente** (chi bussa) | la **destinazione** (a chi si bussa) |
> | Chi viene "ingannato" | **s1** (crede di parlare con r2, non col client) | il **client** (crede di parlare con r2:222, non con s2:22) |
> | Indirizzo che il client digita | l'IP **reale** di s1 (10.2.2.1:22) | un IP **finto**, 10.9.9.2:222 |
> | Chain / hook | **POSTROUTING** (`priority srcnat`) | **PREROUTING** (`priority dstnat`) |
> | Statement | `snat to 10.2.2.254` | `dnat to 10.3.3.1:22` |
>
> **Come ricordarlo senza tabella**:
> - **S**NAT = **S**ource, cambia il **mittente** → agisce quando il pacchetto sta per **uscire**, cioè **POSTROUTING** (l'ultimo hook). Il server non deve sapere chi è il vero client → gli fai vedere r2 come sorgente.
> - **D**NAT = **D**estination, cambia il **destinatario** → deve agire **prima** della decisione di routing (è la destinazione riscritta a decidere *dove* instradare!), cioè **PREROUTING** (il primo hook). Il client si connette a un indirizzo/porta che non esistono davvero (10.9.9.2:222) e r2 li riscrive verso s2 reale (10.3.3.1:22).
>
> Frase-chiave da fissare: **"Source ⇒ Post (uscita), Destination ⇒ Pre (entrata)"**. E il nome della priority te lo conferma: `srcnat` sta in postrouting, `dstnat` in prerouting.

> **Domanda**: perché DNAT *deve* stare in PREROUTING e non potrebbe stare dopo? È una regola arbitraria?
> **Risposta**: non è arbitraria, è **causale**. La decisione di routing ("dove mando questo pacchetto?") si basa sull'**indirizzo di destinazione**. Se vuoi cambiare la destinazione (DNAT), devi farlo *prima* che il kernel decida dove instradare, altrimenti il pacchetto verrebbe instradato verso l'indirizzo finto (10.9.9.2) e non arriverebbe mai a s2. Perciò DNAT vive in PREROUTING (prima del routing). Specularmente, SNAT cambia solo la sorgente, che non influenza il routing: puoi farlo all'ultimo momento, in POSTROUTING, appena prima che il pacchetto esca. È lo stesso ragionamento sugli hook di netfilter visto in S5 ("la catena decide *quando* nel ciclo di vita del pacchetto la regola scatta").

> **Domanda**: perché per il traffico di ritorno del NAT non serve una regola? Se ho tradotto l'indirizzo all'andata, al ritorno non devo "ritradurlo"?
> **Risposta**: sì, va ritradotto, ma lo fa **da solo il conntrack**, non tu. Quando la regola NAT traduce il *primo* pacchetto di una connessione, netfilter registra l'associazione (indirizzo originale ↔ tradotto) nella tabella conntrack. Da quel momento **tutti i pacchetti successivi della stessa connessione, in entrambe le direzioni, vengono tradotti automaticamente** secondo quell'associazione — comprese le risposte, che vengono ri-tradotte all'indirizzo originale prima ancora che tu le riveda. Ecco perché nel `r2.nft` c'è **una sola** regola SNAT e **una sola** DNAT, senza la loro "inversa": scriverla sarebbe ridondante e sbagliato. È esattamente il conntrack di S5.

## NAT vs filter — non confonderli

> **Domanda**: se ho messo SNAT/DNAT su r2, perché nel file r2.nft ci sono ancora le regole FORWARD? Il NAT non basta a far passare il traffico?
> **Risposta**: no, e questa è una seconda zona grigia. **NAT e filter rispondono a due domande diverse e indipendenti**:
> - la tabella **nat** (PREROUTING/POSTROUTING) risponde a *"quali indirizzi/porte deve mostrare questo pacchetto?"* — riscrive, ma **non decide se passa**. Anzi, la sua policy è `accept` proprio perché non è lì che si filtra.
> - la tabella **filter** (INPUT/OUTPUT/**FORWARD**) risponde a *"questo pacchetto ha il permesso di passare?"* — con `policy drop` di default.
> Con default-drop su FORWARD, se non scrivi la coppia di regole FORWARD per una connessione, quel traffico viene **scartato**, NAT o non NAT. Il NAT ti cambia gli indirizzi ma non ti apre il varco. Slogan da ricordare: **"il NAT dice *come* si vede il pacchetto, il filter dice *se* passa"**. Servono entrambi.

## Il pattern nftables generale (da riscrivere a memoria)

> **Domanda**: c'è uno schema fisso per costruire questi file .nft senza doverli imparare a memoria caso per caso?
> **Risposta**: sì, ed è il vero "trucco" d'esame. Tre regole:
> 1. **Host non-router** (client, s1, s2): chain INPUT e OUTPUT con `policy drop`; prima riga sempre `iif lo accept` / `oif lo accept` (il loopback non va mai bloccato); poi, per **ogni comunicazione permessa**, una **coppia** di regole:
>    - andata: match sulla **porta di destinazione** (`tcp dport N accept`);
>    - ritorno: match sulla **porta sorgente** + `ct state established accept`.
>    Chi *inizia* la connessione ha `dport` nell'OUTPUT e la risposta con `sport ... established` nell'INPUT; chi la *riceve* ha il contrario.
> 2. **Router** (r1, r2): stesso schema di coppie andata/ritorno, ma nella chain **FORWARD**, e con `iif`/`oif` espliciti (da quale interfaccia entra, verso quale esce) per instradare correttamente.
> 3. **NAT solo dove serve** (qui solo r2): si **aggiunge** alle regole filter, non le sostituisce; conntrack copre il ritorno.
> Se interiorizzi "coppia dport-andata / sport+established-ritorno" e "non-router→INPUT/OUTPUT, router→FORWARD", puoi ricostruire qualunque file di questo esercizio ragionando, senza memorizzarli.

> **Domanda**: perché nel ritorno c'è quasi sempre `ct state established` ma nell'andata no?
> **Risposta**: perché l'andata è il pacchetto che **inizia** la connessione (`NEW`): non c'è ancora nessuno stato "established" da matchare, la fai passare in base a porta/indirizzo. Il ritorno invece appartiene a una connessione **già aperta** dall'andata: `ct state established` dice "accetta questo pacchetto solo se fa parte di una connessione che *io* ho già visto iniziare e autorizzato". È più sicuro che aprire genericamente la porta sorgente: eviti che qualcuno sfrutti quella regola di ritorno per iniziare una connessione non autorizzata "al contrario". È lo stateful filtering di S5.

---

## Connessioni (riepilogo trasversale)

> Questo modulo **è** una sezione connessioni fatta esercizio. Ogni pezzo richiama un modulo:
> - **S1** — `nmap -sV -p-`, lettura del fingerprint grezzo (Werkzeug/Flask "unrecognized").
> - **S3** — command injection via `filepath`, bypass blacklist con `$(...)`/`&`.
> - **S4** — buffer overflow, offset 16, return address little-endian `\xad\x61\x55\x56` = `0x565561ad`, `( payload ; cat ) | nc`.
> - **S10** — triage Wireshark per esclusione; firme Suricata (`|ad 61 55 56|`, pcre su URI), `detection_filter`, `http_decode_uri`.
> - **S5** — packet filter default-drop, coppie andata/ritorno, SNAT/DNAT, hook PRE/POSTROUTING, conntrack.

## Domande di autoverifica — Risposte

*(dalla lezione; c'è penalità per errore all'esame reale)*

1. **Falso** — la firma affidabile del BOF è l'indirizzo di ritorno (`|ad 61 55 56|`), non i `A` di riempimento.
2. **Falso** — il fingerprint grezzo (header Werkzeug/Python, redirect 308) identifica comunque il servizio come web.
3. **(a)** — DNAT in **PREROUTING**, `priority dstnat`, `dnat to 10.3.3.1:22`.
4. **(b)** — SNAT in **POSTROUTING** (mascherare la sorgente = "provenisse da r2").
5. **Vero** — filter e nat sono ortogonali; le regole FORWARD servono comunque.
6. **Falso** — il conntrack gestisce il de-NAT del ritorno; nessuna regola inversa.
7. **(c)** — `$(cmd)` non contiene separatori filtrati.
8. **Vero** — "appeso in attesa di input" = salto riuscito all'indirizzo target.
9. **Vero** — little-endian: `ad 61 55 56` → `0x565561ad`.
10. **(b)** — il SYN flood senza ACK viola il criterio "connessioni complete".

## Riepilogo

> ⚠️ Sezione non presente in appunti grezzi (non esistono grezzi per questo modulo).

- **Modulo di sintesi**: enumerazione (S1) → pwn (S4) → command injection (S3) → analisi traffico (S10) → Suricata (S10) → packet filtering/NAT (S5), stesso scenario.
- **Firme su ciò che è specifico**: indirizzo di ritorno, catena `filepath=...bypass...flag.txt`; `detection_filter` e `http_decode_uri` per robustezza.
- **SNAT vs DNAT** (la trappola): SNAT = Source = **POSTROUTING** (`srcnat`), maschera il mittente, inganna il server; DNAT = Destination = **PREROUTING** (`dstnat`), maschera il destinatario, inganna il client. DNAT deve stare in PREROUTING perché la destinazione decide il routing. Il NAT **si aggiunge** al filter; conntrack copre il ritorno.

<!-- AUTO-LINKS:START -->
## 🔗 Collegati

- [[lezione_moduloS8_individuare_filtrare_attacchi]]

**Hub:** [[master_map_studio]] · [[concept_maps]] · [[metodo_studio_esami_pratici]]
<!-- AUTO-LINKS:END -->
