# Appunti — Modulo S12: Sicurezza delle comunicazioni

**Corso**: Lab Sicurezza Informatica T
**Lezione di riferimento**: `lezione_moduloS12_sicurezza_comunicazioni.md`
**Fonte primaria**: `SLIDE TEORIA/SICINF/Sicurezza_delle_comunicazioni_23_aprile.pdf` (M. Prandini, 62 slide)
**Stato**: modulo **teorico** (nessun LAB su VM). Nessun appunto grezzo pre-esistente → questi appunti sono una **rilettura critica** della lezione e del PDF, con le domande che sorgono leggendo, risposte inline. Obiettivo: zero zone grigie in vista del **quiz teorico (40%, penalità sugli errori)**.

> ⚠️ **Sezione grezzi non presente**: Lorenzo non ha prodotto appunti grezzi per S12 (modulo mai svolto in aula/lab). Le domande qui sotto simulano la sua lettura critica, non sono trascritte da un file grezzo.

---

## 0. La domanda di fondo (perché esiste questo modulo)

Il modulo cataloga cosa può fare chi ha accesso — anche parziale — al **percorso** che i dati attraversano. Non è "come si buca un server" (quello è S3/S4/S7): è "come si abusa della **rete** tra due endpoint".

> **Domanda**: perché metà del PDF è "richiami di reti"? Sembra riempitivo.
> **Risposta**: non lo è. **Ogni attacco della seconda metà sfrutta un dettaglio preciso della prima metà.** ARP poisoning sfrutta il caching opportunistico di ARP (§1.6); MAC flooding sfrutta il fallback-in-broadcast dello switch (§1.4); IP spoofing sfrutta l'asimmetria della consegna diretta/indiretta (§1.7); BGP hijacking sfrutta il fatto che i router si fidano degli annunci di rotta. Se salti i richiami, gli attacchi diventano formule da memorizzare invece che conseguenze da capire. Regola mentale: per ogni meccanismo di rete, chiediti *"cosa succede se qualcuno mente su questo?"*.

> **Domanda**: qual è il "filo rosso" da tenere a mente per rispondere alle domande a colpo sicuro?
> **Risposta**: quasi ogni attacco sfrutta **una di due assenze**: (a) un protocollo fondamentale **non autenticato** (ARP, IP, BGP, DNS: nessuno verifica *chi* parla), oppure (b) traffico **non cifrato / cifrato male** (Wi-Fi difettoso, traffico in chiaro). Le contromisure "canali sicuri" (S13) non fanno altro che *aggiungere* autenticazione e cifratura, un layer alla volta. Se in un quiz non ricordi il dettaglio, ripiega su questo principio: spesso basta.

---

## 1. Richiami di reti — i termini che vanno definiti

### 1.1 Indirizzo globale vs locale, rete logica vs fisica

> **Domanda**: "globale vs locale" e "logica vs fisica" sembrano la stessa coppia detta in due modi. È così?
> **Risposta**: **No, sono due assi diversi** — è la classica coppia che confonderesti.
> - **globale/locale** riguarda l'**indirizzo**: globale = univoco su tutta Internet, assegnato da una procedura centrale (l'IP pubblico); locale = valido solo in un pezzo di rete, *può* essere non univoco, assegnato localmente (il MAC, gli IP privati).
> - **logica/fisica** riguarda la **rete di appartenenza**: rete logica = la network IP/subnet a cui appartieni *concettualmente*; rete fisica = la LAN a cui sei *materialmente attaccato col cavo/radio*.
> Il legame tra i due assi: l'IP (indirizzo globale) individua la rete **logica**; il MAC (indirizzo locale) vive sulla rete **fisica**. L'architettura a strati nasconde il MAC e lascia lavorare le applicazioni solo con l'IP — ed è proprio questa astrazione che l'attaccante manipola (cambia la corrispondenza IP↔MAC senza che l'app se ne accorga).

### 1.2 Hub vs switch, e cos'è la CAM

> **Domanda**: differenza pratica hub/switch in una frase, senza le solite parole?
> **Risposta**: l'**hub** urla tutto a tutti (mezzo condiviso, broadcast: la banda totale è quella di *una* porta, perché una trasmissione occupa il mezzo per tutti). Lo **switch** parla in privato porta-a-porta (commutazione selettiva: più coppie di porte comunicano in parallelo, banda aggregata > singola porta — es. Fast Ethernet: hub 100 Mbit/s totali, switch 200). Ai fini sicurezza conta questo: sull'hub **chiunque sniffa tutto** senza sforzo; sullo switch **no**, e questo *costringe* l'attaccante a un passo attivo (MAC flooding o ARP poisoning) per tornare a sniffare.

> **Domanda**: cos'è esattamente la CAM? Il nome "Content Addressable Memory" non mi dice nulla.
> **Risposta**: è la memoria fisica in cui lo switch tiene la **tabella di inoltro** (MAC → porta). "Content addressable" = *indirizzabile per contenuto*: invece di chiedere "cosa c'è alla riga 5?" chiedi "in quale riga sta il MAC `5b:06:...`?" e la memoria risponde in un colpo solo (hardware, velocissimo). Serve così perché a ogni trama lo switch deve cercare **il MAC di destinazione** nella tabella in tempo reale. Due proprietà da ricordare per gli attacchi: (1) la CAM è **finita** (numero di righe limitato); (2) quando lo switch *impara* (learning bridge), registra "il MAC **sorgente** che ho appena visto sta su **questa** porta". Il MAC flooding abusa di entrambe (§2.4).

> **Domanda**: "learning bridge" e "learning switch" sono due cose diverse?
> **Risposta**: no, è lo stesso comportamento. **Bridge** è il termine storico (ponte tra due LAN); lo **switch** è un bridge multiporta più performante. "Learning" = lo switch **non nasce con la tabella già piena**: la costruisce osservando il traffico. Prima trama da un MAC sconosciuto → "aha, quel MAC sorgente è raggiungibile da questa porta, lo annoto". Se il MAC di *destinazione* non lo conosce ancora → ripiega sul broadcast (ed è la crepa dello sniffing su switch).

### 1.3 Switch vs router per interconnettere LAN

> **Domanda**: se sia lo switch sia il router "collegano LAN", qual è la differenza che conta?
> **Risposta**: il **dominio di broadcast**. Più LAN collegate da **switch** = **un unico** dominio di broadcast (funzionalmente *una* LAN sola; un broadcast raggiunge tutti). Più LAN collegate da **router** = domini di broadcast **separati** (il router *non* propaga il broadcast oltre sé). Conseguenza di sicurezza fondamentale: la maggior parte degli attacchi di livello 2 (ARP poisoning, MAC flooding, MAC/IP spoofing) è **confinata alla LAN** e **non attraversa il router**. Quindi segmentare con router (o VLAN) *contiene* il raggio d'azione dell'attaccante di L2. Costo del router: mobilità degli host più rigida (cambiare LAN = cambiare subnet IP).

### 1.4 ARP e il "gratuitous ARP"

> **Domanda**: a cosa serve ARP, in una riga?
> **Risposta**: dentro una LAN ogni dispositivo ha **due** identità — l'IP (con cui le applicazioni si conoscono) e il MAC (con cui le schede di rete si consegnano fisicamente le trame). ARP **traduce IP → MAC**: "conosco l'IP `.76`, ma su che scheda glielo consegno?".

> **Domanda**: il meccanismo request/reply e questo "caching opportunistico"?
> **Risposta**:
> - **ARP request** = **broadcast**: "*Who has 192.168.1.76? Tell 192.168.1.34*" → la domanda arriva a **tutti** gli host del segmento.
> - **ARP reply** = **unicast**: solo il possessore di `.76` risponde "*.76 is at 8d:ab:...*".
> - **Caching opportunistico**: **chiunque vede passare** un'associazione IP↔MAC (anche una request non sua!) la **mette in cache** ("l'ho imparata, la salvo"), per non doverla richiedere dopo.

> **Domanda**: cos'è un "gratuitous ARP reply"? Nel PDF compare di colpo nell'ARP poisoning.
> **Risposta**: è una **ARP reply spedita senza che nessuno l'abbia richiesta** ("gratuita" = non sollecitata). Nasce per usi legittimi (annunciare "ho cambiato scheda, il mio IP ora è a questo nuovo MAC"). Ma siccome **ARP non autentica nulla** e il caching è opportunistico, un host che riceve una gratuitous reply **la crede e aggiorna la cache**. È esattamente la leva dell'ARP poisoning: l'attaccante spara gratuitous reply "*l'IP del gateway è al MIO MAC*" e gli altri le bevono.

### 1.5 Consegna diretta vs indiretta — LA coppia da non sbagliare al quiz

> **Domanda**: qual è la differenza tra direct e indirect delivery, e soprattutto **quale indirizzo cambia**? Qui mi confondo di sicuro.
> **Risposta**: dipende se sorgente e destinazione sono **sulla stessa rete fisica** o no.
> - **Consegna diretta**: stessa rete fisica → mando la trama **direttamente** al destinatario finale. In trama: **L2 (MAC) = destinatario finale**, **IP = destinatario finale** → *entrambi* puntano al destinatario.
> - **Consegna indiretta**: reti fisiche diverse → mando la trama a un **router intermedio** che poi la inoltrerà. In trama: **L2 (MAC) = ROUTER (prossimo hop)**, **IP = destinatario finale** → i due divergono.
>
> **La regola che azzera la confusione**: **il MAC di destinazione cambia a ogni hop** (è sempre "il prossimo ponte"), **l'IP di destinazione resta quello finale per tutto il viaggio**. Se al quiz leggi "nella consegna indiretta l'IP di destinazione è quello del router" → **FALSO**: è il *MAC* a puntare al router, l'IP punta ancora al destinatario finale.

> **Domanda**: "da mittente a destinatario c'è sempre una consegna diretta" — perché *sempre*?
> **Risposta**: perché **l'ultimo tratto** — quello che consegna il pacchetto all'host finale — è per forza tra due macchine sulla stessa rete fisica (l'host e l'ultimo router, o direttamente i due host se erano già vicini). Quindi: **esattamente una** consegna diretta (l'ultima o l'unica) + **zero o più** consegne indirette (i salti tra router nel mezzo).

> **Domanda**: perché questa asimmetria è "il cuore" dell'ARP poisoning?
> **Risposta**: perché siccome il MAC di destinazione è "solo il prossimo ponte", se avveleno la tua cache facendoti credere che **il MAC del gateway sia il mio**, tu — pur scrivendo nell'IP la destinazione giusta — consegni **fisicamente a me** ogni pacchetto diretto fuori dalla LAN. Tu credi di parlare col router; parli con me. È MITM.

---

## 2. Attacchi passivi

> **Domanda**: "passivo" vuol dire "innocuo"?
> **Risposta**: No. **Passivo = non modifica i dati in transito** (non li altera, non li inietta). Ma è eccome dannoso: lo sniffing viola la **riservatezza**, la scansione apre la strada a tutto il resto, il recupero di una chiave permette di **impersonare** la vittima. "Passivo" descrive il *modo* (non tocco i bit), non l'impatto. E c'è un bonus per l'attaccante: essendo passivo, **è difficilissimo da rilevare** (non lascia tracce sulla rete).

### 2.1 Scanning vs Sniffing — coppia passiva facile da confondere

> **Domanda**: scanning e sniffing sono entrambi "passivi": non sono la stessa cosa?
> **Risposta**: **No, e la differenza è netta**:
> - **Scanning** = **sondare attivamente**. Mando pacchetti-sonda e guardo le risposte per scoprire host vivi e porte aperte. **Genera traffico** (può essere rumoroso → "loudness"). È ricognizione.
> - **Sniffing** = **ascoltare passivamente** il traffico che *già* passa. **Non genera nulla di suo**, è pura intercettazione.
>
> Sono classificati entrambi "passivi" perché **nessuno dei due modifica i dati della vittima**. Ma lo scanning *emette* sonde (paradossalmente è il più "rumoroso" dei due), lo sniffing no. Non confondere "passivo" (= non altero i dati) con "silenzioso" (= non emetto traffico): lo scanning è passivo ma non silenzioso.

> **Domanda**: cosa vuol dire "loudness / la scansione può essere aggressiva"?
> **Risposta**: "loudness" = **quanto rumore fai** mentre scansioni. Una scansione aggressiva (es. `nmap -A`, tante sonde in fretta) è facile da vedere per un IDS; per questo gli strumenti offrono **modalità di scansione silenziosa** (più lente, frammentate, distribuite nel tempo) per **eludere il rilevamento**. Compromesso classico: velocità/completezza ↔ furtività.

> **Domanda**: cosa fanno di preciso i due comandi nmap dell'esempio?
> **Risposta**:
> - `nmap -sP 137.204.57.200-205` → **scansione di rete** (host discovery): *"quali indirizzi sono vivi?"*. Output: "6 IP scanned, 2 hosts up".
> - `nmap -A 137.204.57.104` → **scansione di host** aggressiva: porte aperte + **versioni** di OS e servizi (fingerprinting). Scopre `ftp vsftpd 3.0.2`, `ssh OpenSSH 6.6.1p1`, `http Apache 2.4.7`. **È letteralmente il LAB di S1.** Perché conta: conoscere la versione esatta = poter cercare l'exploit pubblico corrispondente (ponte verso S3/S4).

### 2.2 Sniffing su reti cablate: 802.1x vs 802.1AE

> **Domanda**: 802.1x e 802.1AE si assomigliano troppo. Cosa fanno rispettivamente?
> **Risposta**: due standard **diversi**, spesso citati insieme perché entrambi difendono la LAN cablata:
> - **802.1x** = **autenticazione delle porte**: prima di lasciarti mettere traffico sulla porta dello switch, ti chiede *chi sei*. Controlla l'**accesso** (identità), **non cifra**.
> - **802.1AE (MACsec)** = **cifratura del traffico** a livello 2. Rende inutile lo sniffing (leggi solo ciphertext).
>
> Frase-chiave del PDF: la crittografia cablata **esiste** (802.1x + 802.1AE) **ma non la usa quasi nessuno** → in pratica lo sniffing su cavo resta possibile. Trucco mnemonico: **x = "chi sei" (autentico)**, **AE = "Authenticated Encryption" (cifro)**.

> **Domanda**: perché lo sniffing "richiede l'accesso fisico ai dati in transito"?
> **Risposta**: per ascoltare devi **stare sul percorso** dei bit. Due modi: (1) **essere già sulla rete locale** (stessa LAN/etere), (2) **arrivarci con un dirottamento** (ARP poisoning, MAC flooding). Ecco perché passivo e attivo si combinano: prima un attacco attivo *ti mette in mezzo*, poi sniffi passivamente. Sul Wi-Fi l'"accesso fisico" è gratis: sei nel raggio radio, ricevi i frame senza toccare nulla → per questo il wireless *dovrebbe* essere sempre cifrato.

### 2.3 MAC flooding — perché "riabilita" lo sniffing su switch

> **Domanda**: come fa il MAC flooding a far sniffare su uno switch, che invece dovrebbe isolare?
> **Risposta**: lo switch isola **finché la CAM contiene** l'associazione MAC→porta giusta. Ma la CAM è **finita** e il fallback quando un MAC di destinazione **non c'è** è **broadcast su tutte le porte** (§1.2). Il MAC flooding **inonda lo switch di MAC sorgente falsi** finché la CAM **si riempie**: a quel punto non c'è più spazio per le associazioni legittime, lo switch non le trova e **ripiega sistematicamente sul broadcast**.
> **Risultato in una riga: il MAC flooding costringe lo switch a comportarsi come un hub** → l'attaccante torna a vedere *tutto* il segmento.

> **Domanda (la coppia critica)**: MAC flooding e ARP poisoning fanno entrambi sniffare in LAN. Come li distinguo?
> **Risposta**: **bersaglio ed effetto diversi**:
> | | **MAC flooding** | **ARP poisoning** |
> |---|---|---|
> | Cosa attacco | la **CAM dello switch** | la **cache ARP degli host** (spesso il gateway) |
> | Come | saturo la tabella con MAC falsi | invio ARP reply false (gratuitous) |
> | Effetto | switch → hub, vedo **tutto** il segmento | reindirizzo a me **un flusso specifico** |
> | Stile | **indiscriminato**, di massa | **mirato** (MITM vittima↔gateway) |
> Mnemonica: **flooding = riempio una memoria (CAM) → rumore per tutti**; **poisoning = avveleno un'informazione (cache ARP) → inganno mirato**.

### 2.4 Wireless key recovery — WEP / WPA / WPA2 / WPA3 senza confonderle

Quattro generazioni, ognuna nata per riparare la precedente e poi bucata. È la parte **più densa di dettagli quiz-abili** — la tabella fissa "quale falla appartiene a quale generazione":

| Gen. | Cifratura / meccanismo | Falla caratteristica (da ricordare) |
|---|---|---|
| **WEP** | chiave simmetrica precondivisa, **stream cipher RC4**, **IV 24 bit** | **IV troppo corto → si ripete** con abbastanza traffico → si **recupera la chiave** |
| **WPA** | patch intermedia; **TKIP (128 bit)** al posto dell'IV; PSK (personale) o auth utente (aziendale) | modalità personale = **no forward secrecy** (chi sa la PSK decifra *tutto*) |
| **WPA2** | a lungo "essenzialmente sicuro" | **KRACK (2017)**: reinstallazione chiave; PSK corta se **WPS** |
| **WPA3** | cifrari robusti; **SAE** (handshake **Dragonfly**) al posto della PSK | **Dragonblood**: tipo 1 = downgrade a WPA2 via MITM; tipo 2 = password partitioning |

> **Domanda**: cos'è uno "stream cipher" e cos'è l'"IV"? E perché un IV di 24 bit che "si ripete" fa recuperare la chiave?
> **Risposta**: uno **stream cipher** (RC4 qui) genera da una chiave un lungo flusso pseudocasuale (il **keystream**) e cifra facendo **XOR** del testo col keystream. **Regola d'oro violata: non riusare mai lo stesso keystream.** Se due messaggi sono cifrati con lo stesso keystream, `C1 XOR C2 = P1 XOR P2` → la chiave si "cancella" e resta una relazione tra i testi in chiaro, sfruttabile. L'**IV (Initialization Vector)** serve proprio a **variare** il keystream a ogni pacchetto (chiave effettiva = chiave base combinata con l'IV), così non lo riusi mai. Ma in WEP l'IV è **solo 24 bit**: i valori possibili si esauriscono in fretta e, con abbastanza traffico, **l'IV si ripete** → keystream riusato → attacco → recupero della chiave. Morale: **IV troppo corto = riuso inevitabile = protezione che crolla**. (Il *perché crittografico* profondo è S14.)

> **Domanda**: cos'è la "forward secrecy" / "segretezza in avanti", e perché WPA personale non ce l'ha?
> **Risposta**: **forward secrecy** = proprietà per cui **compromettere la chiave di lungo termine non permette di decifrare il traffico passato** (ogni sessione usa chiavi effimere, buttate dopo). In **WPA personale** tutti condividono **una** PSK e da quella si derivano le chiavi: **chi conosce la PSK può decifrare *tutti* i pacchetti** (anche registrati prima) → **nessuna forward secrecy**. È il motivo per cui una rete "con password condivisa" non protegge gli utenti *tra loro*.

> **Domanda**: cos'è KRACK e come si "reinstalla una chiave a zero"?
> **Risposta**: **KRACK = Key Reinstallation Attack** (WPA2, 2017). Sfrutta un difetto nell'**handshake**: l'attaccante forza il client a **rieseguire un passaggio** e quindi a **reinstallare una chiave già usata**, resettando i contatori (nonce). Su Android/Linux il bug era così grave che si poteva far installare una **chiave tutta a zero** (nota → tutto decifrabile). Su altri dispositivi: si decifra comunque una gran mole di pacchetti, che possono contenere **credenziali aziendali**. Punto: non si "indovina" la chiave, si **inganna il protocollo** perché ne riusi una prevedibile.

> **Domanda**: cos'è WPS e perché è un problema per WPA2?
> **Risposta**: **WPS (Wi-Fi Protected Setup)** è il meccanismo "premi il pulsante / PIN a 8 cifre" per connettersi senza digitare la password lunga. Il problema: introduce una **PSK/PIN corta**, brute-forzabile → vanifica una PSK WPA2 anche robusta. Difesa: **disabilitare WPS**.

> **Domanda**: SAE, Dragonfly, Dragonblood — troppi nomi. Chi è chi?
> **Risposta**:
> - **SAE (Simultaneous Authentication of Equals)** = il **nuovo metodo di autenticazione** di WPA3, che **sostituisce la PSK** con uno scambio più robusto (resistente al brute force offline).
> - **Dragonfly** = il **nome dell'handshake** usato da SAE.
> - **Dragonblood** = il **nome degli attacchi** contro quell'handshake. Due tipi: **tipo 1** sfrutta la **retrocompatibilità con WPA2** → MITM che forza un **downgrade** a WPA2 (più debole); **tipo 2** sfrutta **implementazioni scorrette** di alcuni passaggi crittografici → **password partitioning** (restringere progressivamente lo spazio della password). Nota positiva: i dispositivi WPA3 sono **aggiornabili** (le patch chiudono Dragonblood).
> Mnemonica: **SAE** è il metodo, **Dragonfly** è come lo fa, **Dragonblood** è come lo rompi.

> **Domanda**: "modalità personale vs aziendale" ritorna in WPA/WPA2. Cosa cambia?
> **Risposta**: **personale** = **una chiave precondivisa (PSK)** uguale per tutti (casa) → semplice ma no forward secrecy. **Aziendale (enterprise)** = **autenticazione utente su canale protetto** (ognuno ha le proprie credenziali, tipicamente via 802.1x/RADIUS) → più sicura e revocabile per singolo utente. È la stessa dicotomia "segreto condiviso" vs "identità individuale" che ritrovi ovunque in sicurezza.

---

## 3. Attacchi attivi

> **Domanda**: definizione secca "attivo" e la differenza da "passivo"?
> **Risposta**: **attivo = minaccia integrità, autenticità o disponibilità** — *tocca* i dati (li altera, inietta, interrompe) o le rotte/identità. Contro il **passivo** (che mira alla riservatezza senza toccare nulla). Prima grande dicotomia del modulo, gettonatissima al quiz.

> **Domanda (coppia di termini)**: "spoofing" e "hijacking" li uso come sinonimi. Sbaglio?
> **Risposta**: Sì, sono diversi:
> - **Spoofing** = **falsificare un'identità** (mi metto il MAC/IP/nome di un altro).
> - **Hijacking** = **dirottare/impossessarsi** di un flusso o di una rotta **già esistente**.
> Relazione: lo **spoofing è spesso il mezzo**, l'**hijacking l'effetto**. Es. faccio IP spoofing (mezzo) per fare session hijacking dopo l'autenticazione (effetto). Nota che il PDF stesso li accosta ("spoofing e hijacking sono spesso un passaggio preliminare per un attacco più impattante").

### 3.1 Link layer

> **Domanda**: MAC spoofing — a cosa serve concretamente e perché "limitato alla LAN"?
> **Risposta**: mi assegno il **MAC** di un altro dispositivo. Serve a **bypassare ACL basate su MAC** e a **intercettare il traffico** destinato alla vittima. È **limitato alla LAN** perché il MAC ha significato solo sul segmento fisico (indirizzo *locale*, §1.1): oltre il primo router non viaggia. Mitigazione **tecnicamente facile: 802.1x** — ma **organizzativamente complesso**, quindi *raro* che venga fatto (frase tipica da V/F: "il MAC spoofing è difficile da mitigare" → **Falso**, è facile *tecnicamente*, scomodo *organizzativamente*).

> **Domanda**: MAC spoofing vs IP spoofing — entrambi "spoofing", cosa cambia?
> **Risposta**: cambiano **il layer e la portata**. MAC spoofing falsifica l'indirizzo **fisico (L2)** → confinato alla LAN, per bypassare ACL MAC / rubare traffico locale. IP spoofing falsifica l'indirizzo **di rete (L3)** → discorso backscatter (§3.2). Entrambi "assumono un'identità altrui", ma su strati diversi.

### 3.2 Network layer

> **Domanda**: perché l'IP spoofing "funziona solo su LAN"? Sembra controintuitivo che tu possa fingere un IP ma non ricevere le risposte.
> **Risposta**: perché **spedire** con un IP sorgente falso è banale (nessuno verifica il mittente), ma **le risposte tornano all'IP scritto come sorgente** — cioè al **vero proprietario** di quell'IP, non a te. Su una **LAN** puoi comunque intercettare fisicamente quelle risposte (sei sullo stesso segmento). Su **Internet**, il routing le consegna altrove e **tu non le vedi**. Il fenomeno delle risposte che piovono su una vittima che non ha mai chiesto nulla si chiama **backscatter**. Quindi: IP spoofing utile per *dirottare traffico* solo in LAN; su Internet resta utile per *mandare* pacchetti falsi (es. DDoS con sorgente mascherata), non per *ricevere*.

> **Domanda**: cos'è BGP e perché il suo "non essere autenticato" è così grave?
> **Risposta**: **BGP (Border Gateway Protocol)** è il protocollo con cui i **router di reti diverse (Autonomous System) si scambiano gli annunci di rotta**: "per raggiungere il blocco di IP X, passate da me". Il problema: **BGP non è autenticato** → chiunque annunci una rotta viene, in linea di principio, **creduto**. Così l'**IP hijacking (BGP hijacking)** estende lo spoofing IP **su scala globale**: non più confinato alla LAN, ma capace di **dirottare interi blocchi di indirizzi** in tutta Internet.

> **Domanda**: IP spoofing vs IP hijacking — dove sta il confine?
> **Risposta**:
> | | **IP spoofing** | **IP hijacking (BGP)** |
> |---|---|---|
> | Cosa falsifico | l'**IP sorgente** dei miei pacchetti | le **rotte** annunciate tra router |
> | Portata | **LAN** (su Internet → backscatter) | **globale** |
> | Falla sfruttata | nessuna verifica dell'IP sorgente | **BGP non autenticato** |
> In una riga: **spoofing = mento sul mio indirizzo; hijacking (BGP) = mento su dove si trova un'intera rete.**

> **Domanda**: il caso YouTube/Pakistan — cosa devo davvero portarmi a casa (oltre all'aneddoto)?
> **Risposta**: nel 2008 il Pakistan, per **bloccare** YouTube internamente, annuncia una rotta `208.65.153.0/**24**` (verso `null0`, l'interfaccia che scarta). Per errore la rotta **esce** e si propaga via BGP a mezza Internet. Essendo **più specifica** del `/22` legittimo di YouTube, **la vince**, e il traffico YouTube di mezzo mondo finisce in Pakistan (dove viene buttato). I **tre principi** da ricordare: **(1)** BGP **crede a chi annuncia** (non autenticato); **(2)** vince la **rotta più specifica** (prefisso più lungo — un `/24` batte un `/22`); **(3)** un **errore locale** può diventare un **blackout globale**. È l'illustrazione del *perché serve autenticazione del routing* (S13).

> **Domanda**: cos'è "null0" e perché un `/24` "batte" un `/22`?
> **Risposta**: **null0** è l'interfaccia "cestino" di un router: instradare verso null0 = **scartare** i pacchetti (è così che il Pakistan voleva bloccare YouTube al proprio interno). Il "più specifico vince" è il **longest prefix match**: quando due rotte coprono lo stesso IP, il router sceglie quella col **prefisso più lungo** (più bit fissi = descrizione più precisa). `/24` fissa 24 bit, `/22` ne fissa 22 → il `/24` è più specifico e prevale. È una regola *di progetto* del routing (di solito utile: preferisci la rotta più precisa) che qui si ritorce contro, perché unita all'assenza di autenticazione lascia dirottare traffico con un annuncio più specifico.

### 3.3 Trasporto e applicazione — TCP vs UDP hijacking

> **Domanda**: perché dirottare **UDP** è "facile" e **TCP** "difficile"? Non è che TCP sia cifrato...
> **Risposta**: **niente a che vedere con la cifratura** (nessuno dei due è cifrato). La differenza è lo **stato**:
> - **UDP è senza connessione (stateless)**: non c'è nessuno stato da azzeccare → mi inserisco con un pacchetto e basta → **molto facile**.
> - **TCP è con connessione (stateful)**: usa i **sequence number** della **finestra scorrevole** (sliding window). Se l'attaccante non usa i **sequence number corretti**, TCP **scarta i pacchetti** e la connessione si perde → devo **azzeccare i SN** → **difficile**.
> Frase-trappola: "TCP è più difficile da dirottare perché è cifrato" → **Falso**. È più difficile perché è **stateful** (i SN alzano la barriera del brute force).

> **Domanda**: e i "cookie HTTP" cosa c'entrano col dirottamento?
> **Risposta**: a livello **applicazione** la sessione autenticata è spesso identificata da un **session id**, tipicamente un **cookie HTTP**. Rubare quel cookie = **impersonare la sessione già autenticata** (session hijacking) senza rifare login. Per ottenere il SN TCP o il cookie l'attaccante ha **due strade**: **(1) indovinare** (brute force — spesso durissimo per i SN); **(2) sniffare** (facile *se è già sul percorso* → di nuovo la sinergia: ARP poisoning per mettersi in mezzo, poi sniff del cookie, poi hijack).

### 3.4 (D)DoS

> **Domanda**: DoS e DDoS — la differenza è solo "una D in più"?
> **Risposta**: la seconda D = **Distributed**. **DoS** = rendere inaccessibile un servizio (anche con un singolo attacco mirato: es. un **RST** o un **SN errato** su una connessione TCP la interrompe). **DDoS** = **molti host coordinati** saturano banda o risorse di calcolo della vittima. Gli host sono **zombie** (macchine compromesse) organizzati in una **botnet**, comandati da un **C&C (Command & Control)**. Botnet IoT citate: **Mirai, Bashlite**.

> **Domanda**: cos'è l'"amplificazione DNS" e perché "amplifica"?
> **Risposta**: l'attaccante manda al resolver DNS una **piccola query** ma con **IP sorgente spoofato = quello della vittima**; il resolver risponde con un pacchetto **molto più grande** che finisce **sulla vittima**. "Amplifica" perché **poco traffico in ingresso → molto traffico verso la vittima** (fattore di amplificazione), e in più **maschera l'origine** (la vittima vede arrivare traffico dai resolver, non dall'attaccante). Ecco perché il PDF dice che *"un controllo accessi impreciso sull'infrastruttura peggiora le cose"*: resolver DNS aperti = amplificatori a disposizione. Difesa: chiudere i resolver aperti, filtrare l'IP sorgente spoofato a monte.

### 3.5 Attacchi al DNS — le quattro varianti da NON confondere

Il DNS traduce nomi in IP, è **onnipresente** e — come ARP/IP/BGP — **non autenticato**. Il PDF ne mostra quattro abusi diversi; è **la coppia/quartetto più insidioso del modulo**. Tabella fissa:

| Attacco | Cosa fa | Il DNS è… |
|---|---|---|
| **Tunnelling** | usa query/risposte come **canale nascosto** per esfiltrare dati o parlare col C&C | **abusato come veicolo** (non falsificato) |
| **Hijacking** | un DNS **malevolo/compromesso** dà l'IP dell'attaccante per un nome legittimo | **il risolutore mente** |
| **Spoofing** | **risposta falsificata**: il nome giusto punta all'IP dell'attaccante | **falsificato nella singola risposta** |
| **Pharming** | riprogramma il **resolver del router** (script + password default) → tutte le future risoluzioni passano dall'attaccante | **dirottato alla fonte, in modo persistente** |

> **Domanda**: tunnelling e spoofing mi sembrano la stessa cosa. Non lo sono?
> **Risposta**: **opposti**, quasi. Nel **tunnelling** il DNS **non è falsificato**: è **usato come tubo** per far uscire dati (le query/risposte *contengono* dati) da una macchina infetta, sfruttando il fatto che i firewall lasciano quasi sempre passare il DNS. È **esfiltrazione / canale col C&C**. Nello **spoofing** il DNS *è* falsificato: la **risposta** dice l'IP sbagliato per dirottare la vittima. Regola: **tunnelling = veicolo per portare fuori dati; spoofing = risposta bugiarda per mandarti sul sito sbagliato.**

> **Domanda**: hijacking e spoofing del DNS, allora, che differenza hanno?
> **Risposta**: **dove sta la bugia**. **DNS hijacking** = il **server risolutore stesso è malevolo o compromesso** e risponde male *strutturalmente* (la macchina che risolve è "dalla parte" dell'attaccante). **DNS spoofing** = si falsifica la **singola risposta** (magari in transito o via race), anche se il server legittimo sarebbe onesto. Il PDF nota che la falsificazione *arbitraria* di una risposta è **difficile** (caching + distribuzione del DNS) → per aggirare la difficoltà si passa al **pharming**.

> **Domanda**: cos'ha di speciale il pharming, e perché il PDF lo chiama attacco "combinato"?
> **Risposta**: risponde alla domanda "*ma non è difficile falsificare una risposta DNS?*" **cambiando bersaglio**: invece di falsificare il DNS *in transito*, **riprogramma chi fa le domande**. Sequenza: **(1)** la vittima visita una pagina HTML (anche a sua insaputa); **(2)** la pagina contiene uno **script**; **(3)** lo script, usando la **password di default del router domestico**, **riprogramma il server DNS** configurato nel router; **(4)** da lì in poi **ogni** risoluzione passa dal name server dell'attaccante. È **"combinato"** perché mette insieme **web** (pagina+script) + **debolezza di configurazione** (password di default del router) + **DNS**. Non rompe crittografia: sfrutta l'**anello gestionale più debole**. Vantaggio per l'attaccante: **persistenza** — non deve più intercettare nulla in tempo reale, ha spostato *stabilmente* la fiducia sul proprio DNS. Difesa n.1, banale ma decisiva: **cambiare la password di default del router** (poi DNSSEC, DoH/DoT, aggiornare i router).

---

## 4. Il confine con S13 (e perché il PDF "si ferma")

> **Domanda**: l'outline del PDF promette "Contromisure: canali sicuri — VLAN, IPSec, TLS", ma poi le slide finiscono al DNS pharming. Sono io che ho un PDF incompleto o mancano davvero?
> **Risposta**: **le slide reali si fermano al DNS pharming**: la sezione "Contromisure: canali sicuri" è **annunciata nell'outline ma non svolta** in questo file (nell'indice compare, di fatto, "in grigio"). **Non è un errore tuo** e non va inventata. Quelle contromisure — **VLAN/802.1X** (data-link), **IPSec** (rete), **TLS** (trasporto) — sono il **corpo di S13 (Protezione delle comunicazioni + OpenSSL/TLS)**. Quindi la ripartizione da tenere ferma all'esame:
> - **Attacchi** al traffico (sniffing, MAC/ARP/IP/BGP/DNS spoofing e hijacking, DoS) → **S12** (questo modulo).
> - **Difese** "canali sicuri" (VLAN, IPSec, TLS, VPN) come *meccanismi* → **S13**.
> Dove il PDF dice "vedi più avanti", il "più avanti" è **S13**.

> **Domanda**: allora la tabella "layer → tecnologia di sicurezza" della lezione (802.1X/WPA2 al data-link, IPsec alla rete, TLS al trasporto) da dove viene, se le slide contromisure mancano?
> **Risposta**: viene dalle quattro slide **"The Internet model"** dei richiami (immagini, poco testo estraibile): mostrano, layer per layer, *quale famiglia di tecnologie* risolve il problema di sicurezza di quel layer, **senza svilupparle**. Servono come **puntatori in avanti** verso S13/S14, ed è ragionevole memorizzarle come mappa "attacco ↔ difesa". Ma il **contenuto vero** delle difese resta S13: qui basta saper **associare il layer alla tecnologia** (tipica MC: *"a quale layer opera IPsec?"* → **rete/IP**; *"cosa protegge il trasporto end-to-end?"* → **SSL/TLS**).

---

## 5. Errori/trappole ricorrenti (il "non farti fregare" prima del quiz)

- **"Passivo" ≠ "silenzioso"**: lo *scanning* è passivo (non altera i dati) ma **rumoroso** (emette sonde). Lo *sniffing* è passivo **e** silenzioso.
- **Consegna indiretta**: cambia il **MAC** di destinazione (→ router), **non** l'**IP** (resta il destinatario finale). Non invertirli.
- **MAC flooding** riempie la **CAM dello switch**, **non** la cache ARP. L'**ARP poisoning** avvelena la **cache ARP degli host**. Bersagli diversi.
- **IP spoofing** dirotta traffico **solo in LAN** (su Internet → **backscatter**). Non "ricevo le risposte da qualsiasi rete".
- **TCP più difficile di UDP** perché **stateful** (sequence number), **non** perché "cifrato".
- **BGP non è autenticato** → il caso Pakistan **non** fu un bug del software, ma la conseguenza *by design* (annuncio più specifico creduto).
- **DNS tunnelling** = esfiltrazione/canale, **non** falsificazione. **Spoofing/hijacking/pharming** = falsificazione (a livelli diversi: risposta / server / resolver del router).
- **802.1x** = autentica (chi sei); **802.1AE (MACsec)** = cifra. Non sono sinonimi.
- **WEP → IV 24 bit**; **WPA → TKIP**; **WPA2 → KRACK/WPS**; **WPA3 → SAE/Dragonfly, rotto da Dragonblood**. Non mescolare le falle tra generazioni.
- **Forward secrecy assente** = tratto della **PSK condivisa** (WEP/WPA personale/WPA2 PSK), non un attacco.
- **Contromisure (VLAN/IPSec/TLS)**: annunciate ma **non svolte** in S12 → sono **S13**. Non attribuire a S12 contenuti di difesa.

---

## 6. Soluzioni commentate dell'autoverifica (lezione §"Autoverifica")

**Vero/Falso**

1. **VERO** — è la definizione stessa di attacco passivo (non modifica i dati in transito).
2. **FALSO** — lo switch isola *solo finché* la CAM contiene il MAC; con il **MAC flooding** (CAM piena → broadcast) lo sniffing torna possibile. Lo switch offre protezione *limitata*, non assoluta.
3. **FALSO** — nella consegna indiretta è il **MAC** di destinazione a puntare al router del prossimo hop; l'**IP** di destinazione resta quello del **destinatario finale**.
4. **FALSO** — **ARP non è autenticato**: chiunque può rispondere (anche con gratuitous reply non richieste). È il difetto alla base dell'ARP poisoning.
5. **FALSO** — l'IP spoofing dirotta il traffico **solo su LAN**; su Internet le risposte tornano al vero proprietario dell'IP (fenomeno del **backscatter**), l'attaccante non le riceve.
6. **VERO** — l'IV di 24 bit **si ripete** con abbastanza traffico → keystream RC4 riusato → recupero della chiave WEP.
7. **FALSO** — **BGP non è autenticato**; il caso YouTube/Pakistan fu possibile *per progetto* (annuncio più specifico creduto), non per un bug del software.
8. **FALSO** — il MAC flooding riempie la **CAM dello switch**, non la cache ARP degli host (quello è l'ARP poisoning).
9. **FALSO** — il DNS **tunnelling** usa le query/risposte come **canale per esfiltrare dati** (o C&C); la falsificazione di una risposta per dirottare la vittima è il DNS **spoofing**.
10. **VERO** — la PSK condivisa di WPA personale non fornisce **forward secrecy** (chi conosce la chiave decifra tutti i pacchetti).

**Scelta multipla**

11. **b)** la invia in **broadcast** su tutte le porte (fallback dello switch quando il MAC di destinazione non è in CAM).
12. **a)** consegna diretta → **L2 = destinatario finale, IP = destinatario finale** (entrambi puntano al destinatario).
13. **c)** pharming → **riprogramma, via script e password di default, il server DNS del router** domestico.
14. **c)** TCP richiede di **indovinare i sequence number** corretti della finestra scorrevole (è stateful). *Non* perché "cifrato".
15. **c)** **SSL/TLS** protegge il trasporto end-to-end (802.1X è data-link, IPsec è rete, WPA2 è wireless/data-link).
16. **b)** Dragonblood **tipo 1** sfrutta la **retrocompatibilità con WPA2** per forzare un **downgrade via MITM**.
17. **b)** ARP poisoning: convince gli host (spesso il gateway) che l'**IP della vittima è al MAC dell'attaccante**, tramite **gratuitous ARP reply**.
18. **c)** l'amplificazione DNS serve a **potenziare e mascherare l'origine di un DDoS** (piccola query spoofata → risposta grande verso la vittima).

---

## 7. Mappa mentale finale (30 secondi di ripasso)

- **Passivi** (non toccano i dati → riservatezza/ricognizione): scanning, sniffing, MAC flooding, wireless key recovery.
- **Attivi** (toccano/iniettano/interrompono → integrità/autenticità/disponibilità): MAC/IP spoofing, ARP/BGP/DNS hijacking, DoS/DDoS.
- **Filo rosso**: protocolli fondanti **non autenticati** (ARP, IP, BGP, DNS) + traffico **in chiaro** → l'attaccante sfrutta l'una o l'altra assenza.
- **Sinergia ricorrente**: prima *mi metto in mezzo* (attivo: ARP poisoning) poi *ascolto* (passivo: sniffing); prima *recupero una chiave* (passivo) poi *impersono* (attivo).
- **Mappa a strati**: data-link → 802.1X/802.1AE/VLAN; rete → IPsec; trasporto → TLS. **Le difese sono S13**, la crittografia sotto WEP/WPA/TLS è **S14**, la gestione chiavi è **S15**.
- **Confine**: S12 si ferma agli **attacchi** (fino al DNS pharming); le contromisure "canali sicuri" sono S13.
