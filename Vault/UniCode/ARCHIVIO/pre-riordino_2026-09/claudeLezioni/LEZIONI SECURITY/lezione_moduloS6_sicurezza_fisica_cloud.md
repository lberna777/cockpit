# Lezione — Modulo S6: Sicurezza fisica e collocazione delle risorse (on-premise / cloud)

**Corso**: Lab Sicurezza Informatica T
**Docente slide**: Marco Prandini
**PDF sorgente**: `SLIDE TEORIA/SICINF/Sicurezza_fisica_e_collocazione_in_cloud_10_aprile.pdf` (42 slide)
**Natura del modulo**: teorico. Non c'è un LAB dedicato: il contenuto è materia da quiz (40%), e diversi comandi citati (LILO/GRUB, `gpg --verify`, `apt-key`, `signed-by`, `repoquery`, `yum versionlock`) sono candidati tipici a domande vero/falso.

---

## 1. Il problema di fondo: dove stanno le risorse cambia il modello di sicurezza

Tutti i sistemi di controllo dell'accesso alle informazioni visti finora sono **mediati**: qualcuno, sopra il dato, decide chi può leggerlo o modificarlo. Questa mediazione ha due pilastri:

- il **sistema operativo** (es. i permessi sui file);
- la **gestione dei segreti** (es. le chiavi crittografiche).

Il punto centrale del modulo è che entrambi questi pilastri presuppongono un'assunzione implicita: che l'hardware sotto di essi funzioni correttamente e che il software che li implementa sia autentico e integro. La **collocazione fisica delle risorse** è precisamente ciò che determina quanto quell'assunzione sia difendibile. La domanda guida è: *come cambia la sicurezza a seconda di dove metto la macchina?*

Si contrappongono due scenari:

- **On premises** (la macchina è "in casa mia"): nessuna condivisione dell'infrastruttura; relativa semplicità nel tenere separati i segreti dai sistemi e dai dati (tipicamente password e chiavi si inseriscono manualmente); ma resta a carico mio garantire il **corretto funzionamento dell'hardware** e **l'esecuzione di sistemi operativi e software integri e autentici**.
- **In the cloud**: gestione hardware/software di altissimo livello delegata al fornitore, ma ambienti di memorizzazione ed elaborazione **condivisi** con altri clienti e **delocalizzazione** (non so fisicamente dove siano i miei dati).

Molti dei problemi che si presentano on premises sono *cambiati* nello scenario cloud, non spariti: alcuni diventano irrilevanti (non è più io a dover chiudere il rack), altri concettualmente simili riappaiono in forma nuova (l'accesso fisico dell'insider diventa il vicino di rack multi-tenant), e la logica delle contromisure si adatta.

> **Perché esiste questa distinzione**: perché un errore comune è concentrare tutte le difese su un solo fronte (di solito la rete) e dare per scontato il resto. Il modulo serve a mostrare che l'accesso fisico e la provenienza del software sono canali di attacco a sé, che scavalcano interamente le difese di rete.

**Connessione con S5 (Firewall)**: nel modulo S5 il firewall è la difesa di perimetro contro gli attacchi *via rete*. Qui il messaggio è complementare e sovversivo: *le corrispondenti contromisure di rete possono essere facilmente scavalcate da un attaccante con accesso fisico al sistema*. Un firewall perfettamente configurato non protegge da chi stacca il disco e se lo porta via. I due moduli descrivono due superfici d'attacco disgiunte: rete (S5) e presenza fisica (S6).

---

## 2. On premises — la messa in sicurezza fisica

Un server è, prima ancora che un nodo di rete, **un sistema di calcolo collocato in un ambiente e connesso a una varietà di dispositivi**. Normalmente le difese si concentrano sul fronte software (applicazioni, sistema operativo, attacchi via rete). Le minacce fisiche principali sono tre:

1. **Furto** dello storage o dell'intero calcolatore.
2. **Connessione di sistemi di raccolta dati** alle interfacce (dispositivi che si agganciano fisicamente per esfiltrare o iniettare).
3. **Avvio del sistema con un sistema operativo arbitrario** (boot da supporto esterno controllato dall'attaccante).

La gravità di queste minacce **dipende fortemente dallo specifico ambiente**: un server in un data center presidiato con badge e telecamere è esposto in modo diverso da una postazione in un ufficio open space.

### Threat model

- **Attaccante**: cerca di ottenere accesso fisico anche breve. Con esso può bypassare l'intero stack di controllo accessi software — non deve indovinare password di rete se può avviare la macchina con un proprio SO e leggere il disco direttamente.
- **Difensore**: deve trattare l'accesso fisico come un vettore di prima classe, non come un dettaglio logistico. Le contromisure sono in parte *non informatiche* (perimetro, sorveglianza) e in parte tecniche (cifratura del disco, protezione del boot).

---

## 3. Fattori non informatici: come si ottiene l'accesso

Poiché l'accesso al sistema abilita attacchi specifici, la prima domanda difensiva è: *come fa un attaccante a entrare fisicamente?* Le vie tipiche:

- **Insider**: chi ha già accesso legittimo e ne abusa. È la voce più difficile da contrastare perché non c'è un perimetro da forzare.
- **Tailgating**: seguire una persona autorizzata attraverso una porta controllata senza autenticarsi (il classico "mi tieni la porta?").
- **Errata identificazione di visitatori**: far passare per legittimo chi non lo è (finto tecnico, finto corriere).
- **Social engineering**: manipolare le persone perché concedano accesso o informazioni.
- **Effrazione**: forzatura fisica vera e propria.

Contro questi vettori serve la **sicurezza fisica "tradizionale"**, considerata *essenziale*:

- **Regolamenti chiari e condivisi** (tutti sanno chi può entrare e come);
- **Perimetro robusto**;
- **Sorveglianza e procedure**.

### La disponibilità è il terzo vertice della triade CIA

La sicurezza fisica non riguarda solo riservatezza e integrità: la **disponibilità** (Availability, il terzo vertice della triade CIA insieme a Confidentiality e Integrity) è spesso minacciata proprio da fattori fisici/ambientali:

- **Alimentazione** (mancanza di corrente);
- **Connettività** (il link cade);
- **Condizionamento** (surriscaldamento della sala);
- **Incidenti, disastri, attentati**.

> **Perché conta per l'esame**: una domanda tipica può chiedere di attribuire una minaccia al vertice giusto della triade. Il condizionamento che salta o l'alimentazione che manca sono minacce alla **disponibilità**, non alla riservatezza. Il furto del disco è minaccia alla **riservatezza** (e potenzialmente disponibilità). La manomissione del software al boot è minaccia all'**integrità**.

### Threat model

- **Attaccante**: predilige la via a minor resistenza. Se il tailgating funziona, non serve forzare nulla. L'insider è la posizione più potente.
- **Difensore**: nessuna singola misura basta; regolamenti + perimetro + sorveglianza vanno combinati, e la disponibilità va difesa con ridondanza di alimentazione, raffreddamento e connettività.

---

## 4. Vulnerabilità sfruttabili "in presenza"

Con accesso fisico, anche solo per pochi minuti, entra in gioco un arsenale specifico. Il PDF elenca (con riferimenti a casi reali) le seguenti classi:

- **BadUSB e simili**: un dispositivo USB il cui *firmware* è stato riprogrammato per fingersi qualcosa di diverso (es. una chiavetta che si presenta al sistema come tastiera e digita comandi). Il punto insidioso: la minaccia è nel firmware della periferica, non in un file scansionabile dall'antivirus.
- **Thunderspy**: attacchi che sfruttano l'accesso diretto alla memoria (DMA) offerto da porte ad alte prestazioni (Thunderbolt) per leggere/scrivere la RAM scavalcando il sistema operativo.
- **Keylogging e videoghosting**: dispositivi hardware interposti fisicamente (es. un *KeyGrabber* tra tastiera e PC, un *VideoGhost* sul cavo video) che registrano quanto digitato o visualizzato. Non lasciano traccia software.
- **Key injection**: iniezione di sequenze di tasti (keystroke injection) per far eseguire comandi come se li avesse battuti l'utente.
- **Disk un/plugging**: scollegare/ricollegare dischi, incluse tecniche per **bypassare i Self-Encrypting Drive (SED)**: se il disco si auto-cifra ma la chiave viene sbloccata all'avvio, staccarlo "a caldo" e ricollegarlo altrove può in certi scenari aggirare la protezione.
- **Power glitching**: disturbare deliberatamente l'alimentazione per provocare errori nel processore in momenti critici, così da far saltare controlli di sicurezza altrimenti solidi (attacco "hardware" al software sicuro).

> **Distinzione da tenere separata** (BadUSB vs keylogger hardware vs key injection): il **keylogger hardware** *registra passivamente* ciò che passa; la **key injection / BadUSB-tastiera** *inietta attivamente* input. Uno esfiltra, l'altro comanda. Sono minacce diverse anche se entrambe passano dalla porta USB.

### Threat model

- **Attaccante**: sfrutta il fatto che le periferiche fisiche e il firmware sono *fidati per default*. Il sistema si aspetta che una tastiera sia una tastiera.
- **Difensore**: disabilitare periferiche/porte non usate, cifrare, controllare l'integrità del firmware, e limitare l'accesso fisico non presidiato — perché tutti questi attacchi richiedono contatto fisico con la macchina.

---

## 5. Collocazione "in remoto": la macchina fuori dal controllo diretto

Quando il calcolatore è collocato dove non ho controllo fisico diretto (housing/colocation, o comunque un sito non presidiato da me), si adottano misure che rendano l'accesso fisico altrui meno utile:

- **Scegliere un case che possa essere chiuso e fissato al rack** (contro il furto e l'apertura).
- **Installare dispositivi di rilevazione delle intrusioni** (fisiche: sensori di apertura del case).
- **Adottare misure di protezione dei dati che rendano inutile il furto** — tipicamente la **cifratura**. Attenzione al rovescio della medaglia: se i dati sono cifrati, **l'accesso ai dati va abilitato manualmente** (bisogna fornire la chiave/passphrase all'avvio), il che complica il funzionamento non presidiato.
- **Disabilitare le periferiche non utilizzate** (riducendo la superficie degli attacchi "in presenza" del §4), salvo poi riabilitarle se sopraggiungono esigenze nuove.

> **Il compromesso ricorrente**: quasi ogni contromisura fisica robusta (password al boot, disco cifrato) **peggiora l'automazione**. Un sistema che riparte da solo dopo un blackout è comodo ma indifeso; un sistema che richiede una passphrase all'avvio è protetto ma non riparte da solo. Questa tensione tra sicurezza e disponibilità/automazione torna più volte nel modulo.

---

## 6. Attacchi fisici alle risorse logiche: il processo di boot

Il cuore tecnico del modulo. Per andare a regime un sistema attraversa un **processo di boot** in quattro fasi, e **ognuna può essere dirottata** da un attaccante con accesso fisico per far caricare software malevolo:

1. **BIOS** — individua i dispositivi da cui è possibile caricare il boot loader e l'ordine in cui esaminarli. Molti BIOS permettono di proteggere con **password** l'avvio o la modifica della configurazione.
2. **Boot Loader** — sceglie il sistema operativo e gli passa eventuali parametri. Gestisce la *maintenance mode*. Può essere protetto con password come il BIOS.
3. **Sistema operativo** — carica i **device driver** (da non sottovalutare come superficie d'attacco) e avvia il processo **init**.
4. **init** — gestisce i **runlevel** (o i **target**, nel mondo systemd) per coordinare l'inizializzazione del sistema, cioè avviare i servizi nell'ordine corretto.

**Connessione con S9 (Demoni di sistema + Autorizzazione)**: le fasi 3 e 4 (device driver, `init`, runlevel/target, avvio ordinato dei servizi) sono esattamente il territorio del modulo S9. Qui la stessa sequenza è guardata dall'ottica dell'attaccante: *ognuno di questi punti di aggancio è dirottabile*.

### 6.1 Password al boot: pro e contro

- Se serve una password per l'avvio, il **funzionamento non supervisionato** diventa problematico: dopo un banale calo di alimentazione la macchina può restare ferma per ore in attesa che qualcuno digiti la password.
- In sistemi con gravi esigenze di sicurezza la password di boot **non sarà comunque l'unica** da fornire, quindi tanto vale proteggere *tutti gli strati*.
- Almeno la **protezione contro i cambi di configurazione** è sempre consigliabile (anche quando non si mette la password all'avvio vero e proprio).

Il principio cardine: **MAI affidarsi a un unico strato di protezione**. Le password del BIOS in particolare:

- hanno **meccanismi semplici di reset** (spesso basta un jumper sulla scheda madre o togliere la batteria);
- possono essere **indovinate**.

> **Perché è una regola, non un consiglio**: la difesa in profondità nasce proprio dall'osservazione che ogni singolo strato ha un modo noto di essere aggirato. La password BIOS da sola è teatro di sicurezza; ha senso solo come uno strato tra tanti.

### 6.2 Configurazione del bootloader a runtime: LILO e GRUB

Due bootloader storici del mondo Linux:

- **LILO** (the Linux Loader): usato fin dagli albori di Linux.
- **GRUB** (the Grand Unified Bootloader): più potente e flessibile di LILO, dotato di una **shell** che permette di eseguire comandi per modificare al volo la procedura di avvio — naturalmente questa potenza abilita molti abusi.

Entrambi permettono di **passare parametri al kernel**. I due più critici per la sicurezza:

- **`single`**: avvia in modalità single-user/maintenance. Alcune distribuzioni hanno default rischiosi: se si innesca il *maintenance mode* si apre una **shell di root senza chiedere password**.
- **`init=…`**: sostituisce il comando lanciato dal kernel come primo processo (normalmente `/sbin/init`). La slide pone la domanda retorica che è il fulcro dell'attacco: **"E se fosse `/bin/bash`?"** — passando `init=/bin/bash` il kernel avvia una shell di root al posto di init, dando controllo totale senza autenticazione.

> **Distinzione `single` vs `init=/bin/bash`**: entrambi portano a una shell privilegiata all'avvio, ma per vie diverse. `single` sfrutta la *maintenance mode* prevista dal sistema (con default di sicurezza deboli); `init=/bin/bash` *scavalca del tutto init* dicendo al kernel di eseguire direttamente bash come processo 1. È il motivo per cui proteggere con password il **bootloader** (non solo il BIOS) è essenziale: senza quella protezione chiunque, al menu di GRUB, può aggiungere questi parametri.

**Connessione con S11 (Misconfiguration / Privilege Escalation)**: questo è un privilege escalation "da accesso fisico". La differenza rispetto al privesc di S11 è il vettore: là si sale a root sfruttando misconfigurazioni *da un accesso già ottenuto sul sistema*; qui si ottiene root direttamente al boot con accesso fisico. Concettualmente stessa posta in gioco (shell di root), vettore diverso.

### 6.3 Password del bootloader: sintassi (candidati a domande d'esame)

**LILO**:

- `password=YourPasswordHere` — imposta una password richiesta al boot, **a meno che** non sia specificato…
- `restricted` — con `restricted` la password è richiesta **solo per modificare i parametri** durante il boot, non per il semplice avvio.
- **Global vs. single-entry** (la distinzione più insidiosa):
  - `password` e `restricted` nella *global section*: chiede la password prima di consentire l'aggiunta di parametri — attenzione alle entry non sicure.
  - `password` e `restricted` in una *image section*: chiede la password prima di consentire l'aggiunta di parametri, **solo per l'immagine specificata**.
  - `password` nella *global section* e `restricted` in una *image section*: chiede la password prima di consentire l'aggiunta di parametri solo per quell'immagine, **mentre chiede sempre la password per avviare altre immagini**.

**GRUB**:

- `password [--md5] passwd [new-config-file]` — se nella *global section*, imposta una password richiesta per attivare l'**interactive operation** del bootloader (e opzionalmente può innescare il caricamento di un file di configurazione alternativo); se specificata per un item del menu, la password serve per avviare quell'item.
- `lock` — messo subito dopo `title`, contrassegna quell'item come **password-protected**. Funziona **solo se esiste una direttiva `password` nella global section** (senza di essa, `lock` non protegge nulla).
- `md5crypt` — comando usabile al grub prompt per **calcolare il password hash** da usare con `--md5` (così la password non sta in chiaro nel file di configurazione).

> **Distinzione `password` (global) vs `password` (per-item) vs `lock`**: `password` in global protegge l'accesso alla *modalità interattiva* del bootloader (la shell/l'editing dei parametri); `password` su un item protegge l'*avvio di quello specifico item*; `lock` marca un item come protetto ma *dipende* dalla password globale per funzionare. Confondere questi tre è esattamente il tipo di errore che una domanda a scelta multipla cerca di far cadere.

---

## 7. La sicurezza del processo di boot: la catena di fiducia

Posto che ogni fase è dirottabile, si arriva al problema di fondo: **come assicurarsi che ogni componente software eseguito da un computer sia autentico, integro e benevolo?** Il ragionamento procede a ritroso, e ogni risposta sposta la fiducia più in basso:

- Gli **anti-malware** verificano le applicazioni. Ma **chi verifica gli anti-malware?**
- Il **sistema operativo** li verifica (idealmente rendendo l'anti-malware perfino inutile). Ma **chi verifica il S.O.?**
- Il **boot loader** potrebbe. Ma **chi verifica il boot loader?**
- Il **BIOS** potrebbe, specialmente se **assistito da hardware speciale** che non possa essere modificato dal S.O. e quindi sia immune da infezioni.

Questo hardware speciale, incorruttibile e alla base di tutto, è la **hardware root of trust**: la radice fidata da cui parte una **catena di fiducia** (*chain of trust*). Ogni anello verifica il successivo prima di cedergli il controllo; la radice è fidata *per costruzione* perché non modificabile via software.

> **Perché serve una radice hardware**: qualsiasi verifica puramente software può, in linea di principio, essere compromessa dallo stesso attaccante che compromette ciò che dovrebbe verificare. Serve un punto d'ancoraggio che l'attaccante software non possa toccare — e questo può essere solo hardware.

### 7.1 Measured / Trusted / Secure Boot — tre termini da non confondere

Questi tre nomi sono la trappola concettuale principale del modulo. **Non sono sinonimi**:

- **Measured Boot**: processo *generale* che tipicamente usa un **TPM** come hardware root of trust. **Misura** (calcola e registra l'hash di) ogni componente caricato. **NON definisce come *prevenire* un avvio malevolo** — si limita a *registrare* cosa è stato caricato, lasciando ad altri la decisione.
- **Trusted Boot**: processo che *usa gli strumenti del Measured Boot* e in più **blocca il boot non appena individua un componente non fidato**. Cioè: measured boot + capacità di *fermarsi*.
- **Secure Boot**: è il **nome specifico dato all'implementazione di trusted boot basata su UEFI**. Implementazione software + chiavi nel firmware; richiede un BIOS standard per la fase di POST; può avvalersi del TPM per velocizzare e migliorare i controlli di integrità.

> **La distinzione chiave (misurare vs bloccare)**: Measured Boot *misura e basta* (registra hash, non impedisce nulla); Trusted Boot *misura e blocca*. Secure Boot è semplicemente il nome di Trusted Boot **quando è implementato su UEFI**. Una domanda tipica: "Il Measured Boot impedisce l'avvio di un bootloader manomesso? → **Falso**: lo misura soltanto, la decisione è demandata (eventualmente a una remote attestation)."

### 7.2 Measured Boot in dettaglio: TPM, CRTM, PCR

Il **TPM** (Trusted Platform Module) è un chip con funzionalità crittografiche, parte delle specifiche del **Trusted Computing Group**. Il measured boot vi si basa attraverso:

- **CRTM** (Core Root of Trust for Measurement): il primo pezzo di codice fidato, la radice da cui parte la misurazione.
- **PCR** (Platform Configuration Registers): registri che **una volta scritti sono fisicamente non modificabili** (si possono solo estendere, non riscrivere arbitrariamente).

Il funzionamento (rappresentato nella slide con lo schema CRTM → BIOS → Bootloader → OS, con frecce di *measuring*, *passing control* e *storing* verso i PCR): a ogni passaggio il componente corrente **misura** il successivo, **memorizza** l'hash nei PCR e poi gli **passa il controllo**. Si raccoglie così l'hash di ogni componente caricato.

Caratteristica importante: il measured boot **pospone i controlli** finché non dispone (a) delle chiavi crittografiche e (b) di abbastanza memoria per fare i calcoli necessari. E soprattutto: **si può decidere chi fa i controlli e quando** — per esempio *dall'esterno*, da un sistema fidato, per abilitare funzioni critiche. Questo è il meccanismo della **remote attestation**: un verificatore remoto interroga i PCR e decide se la macchina è in uno stato fidato prima di concederle, per esempio, l'accesso a una risorsa.

> **Perché "pospone i controlli" e perché conta**: proprio perché measured boot *registra* e non *blocca*, la valutazione può avvenire dopo (quando ci sono chiavi e memoria) e altrove (remote attestation). È l'esatto opposto del secure boot UEFI, che invece verifica e blocca *sul momento*, componente per componente.

### 7.3 UEFI e Secure Boot

- **EFI** (nato in Intel) nasce come interfaccia più flessibile del BIOS tra S.O. e firmware; l'**UEFI Forum** ne standardizza e aggiorna la specifica.
- **UEFI è un "mini OS"**: milioni di righe di codice, standard per molte piattaforme — e proprio per questo un **bersaglio ideale degli attaccanti** (una superficie enorme, sotto il sistema operativo).
- **UEFI verifica ogni componente software prima di passare il controllo** a Bootloader/Sistema Operativo: richiede la disponibilità di un **database di chiavi** e **blocca il boot appena rileva una difformità**.

#### Le chiavi di UEFI Secure Boot

UEFI Secure Boot definisce **due processi di sicurezza**: (1) la **verifica dell'immagine di boot** e (2) la **verifica degli aggiornamenti al database** di sicurezza delle immagini. Per farlo usa più database e set di chiavi (schema della slide 16), in una gerarchia dove le chiavi più in alto autorizzano quelle più in basso:

| Chiave | Verifica | Il suo aggiornamento è verificato da | Ruolo |
|---|---|---|---|
| **PK** | nuova PK, KEK, db/dbx/dbt/dbr, OsRecovery… | PK | **Platform Key** (la radice) |
| **KEK** | nuovi db/dbx/dbt/dbr, OsRecovery… | PK | **Key Exchange Key** |
| **db** | immagini UEFI | PK/KEK | **Authorized** Image Database (lista dei "consentiti") |
| **dbx** | immagini UEFI | PK/KEK | **Forbidden** Image Database (lista dei "vietati/revocati") |
| **dbt** | immagine UEFI + dbx | PK/KEK | Timestamp Database |
| **dbr** | OsRecovery | PK/KEK | Recovery Database |

> **Distinzione db vs dbx (la coppia più chiedibile)**: **db** è la lista *bianca* (immagini autorizzate); **dbx** è la lista *nera* (immagini proibite/revocate — es. un bootloader di cui è emersa una vulnerabilità). Sono complementari: un'immagine passa se è in `db` **e** non è in `dbx`. La **PK** è la radice che autorizza tutto il resto; la **KEK** sta in mezzo e autorizza gli aggiornamenti a db/dbx.

#### UEFI Secure Boot Image Verification (il modello Clark-Wilson)

La slide 17 descrive le entità coinvolte nella verifica delle immagini al boot con un vocabolario formale:

- **TP** = *Trusted Platform*: la procedura di verifica stessa.
- **CDI** = il **UEFI Secure Boot Image Security Database** (Constrained Data Item): il **database delle politiche di sicurezza** da applicare alle immagini da caricare. È **aggiornabile**.
- **UDI** = *Unconstrained Data Item*: qualsiasi firmware di terze parti, incluso **boot loader, PCI option ROM, o UEFI shell tool**.

Meccanismo: **al boot, TP verifica l'integrità di UDI utilizzando le policy CDI**; se il controllo va a buon fine, **UDI entra a far parte di CDI** e il firmware di terze parti viene eseguito. Poiché il CDI è aggiornabile, un fornitore che voglia far accettare il proprio componente deve **firmarlo con la propria chiave privata e rendere disponibile la chiave pubblica**; questa **chiave pubblica va iscritta (*enrolled*) nel firmware del sistema**. E qui la garanzia cruciale: **normalmente questo passaggio richiede un reboot in una modalità speciale e l'intervento sulla console**, bloccando quindi l'azione di utenti malevoli **ma senza accesso fisico** al sistema.

> **Perché il modello Clark-Wilson**: è un modello formale di integrità in cui procedure fidate (TP) trasformano dati non vincolati (UDI) in dati vincolati/fidati (CDI) solo dopo verifica. Non serve conoscerlo a fondo per l'esame, ma è utile capire il *movimento*: un componente esterno diventa fidato solo dopo che una procedura fidata lo ha validato con una policy, e l'iscrizione di nuove chiavi richiede presenza alla console.

#### UEFI Secure Boot in Linux: shim e MOK

Su Linux la catena (schema slide 18: PK → KEK db → **Shim** ↔ **MOK List** → GRUB2 → Kernel) funziona così:

1. La **Platform Key ufficiale verifica un piccolo pre-boot-loader, `shim`**. La chiave usata per firmare `shim` deve essere fornita dal costruttore hardware — **in pratica è una chiave Microsoft** (è Microsoft a firmare `shim` perché la sua PK è quella preinstallata su quasi tutto l'hardware consumer).
2. **`shim` può usare o trasferire le MOK** (*Machine Owner Keys*): per validare il bootloader e per validare **moduli custom del kernel**.
3. I **componenti aggiuntivi del kernel devono essere firmati** per poter essere caricati:
   - l'utente **genera le MOK**;
   - l'utente **deposita le MOK in shim**;
   - **al boot successivo, shim trova le chiavi nella fase di setup e chiede conferma per salvarle in firmware** → il **consenso esplicito e basato su password è sempre richiesto**.

> **Perché esiste `shim`**: risolve un problema pratico. L'hardware si fida solo di chiavi Microsoft (la PK preinstallata). Le distribuzioni Linux non possono far firmare ogni kernel da Microsoft, quindi Microsoft firma un piccolo componente stabile (`shim`), e `shim` a sua volta gestisce le MOK dell'utente. Il meccanismo MOK è ciò che permette al proprietario della macchina di far caricare moduli propri (es. un driver che compili tu) senza disabilitare Secure Boot — ma solo con **consenso alla console + password**, mai da remoto.
>
> **Nota pratica ricorrente**: chi ha Secure Boot attivo e installa VirtualBox su Linux incontra proprio questo — il modulo `vboxdrv` non si carica finché non lo si firma con una MOK e la si iscrive rispondendo al prompt di `shim` al reboot. È l'esempio concreto del meccanismo.

**Connessione con S14/S15 (Crittografia e gestione delle chiavi con gpg)**: l'intera catena di fiducia poggia su firma digitale e gestione delle chiavi — hash nei PCR, chiavi PK/KEK, firma di `shim` e dei moduli con MOK. È la stessa primitiva (firma asimmetrica, chiave privata firma / chiave pubblica verifica) che S15 esercita concretamente con `gpg`. Qui la si vede applicata alla catena di boot; là alla verifica di file e messaggi.

---

## 8. Integrità e autenticità del software applicativo

Il **secure boot garantisce l'integrità fino all'avvio del sistema operativo** — ma non oltre. I **pacchetti software applicativi** sono meno "potenti" (girano senza privilegi di boot) ma **non necessariamente meno pericolosi**. Da qui il problema di verificare la provenienza del software che installo *dopo* l'avvio.

### 8.1 Autenticazione del software scaricato

La **prima cautela** quando si scarica software dovrebbe essere **verificarne l'autenticità da una firma digitale**. Ma per verificare una firma serve una **chiave pubblica fidata** — il che sposta il problema (da dove viene la fiducia in quella chiave?). Procedura tipica con GPG:

1. `gpg --verify FILE.asc FILE.tar.gz` — mostra il *key id* con cui è stato firmato.
2. `gpg --keyserver pgpkeys.mit.edu --recv-key <KEY_ID>` — scarica quella chiave. Ma **l'autenticità della chiave, in questo caso, deriva solo dalla fonte… basta?** Va valutato caso per caso, seguendo indicazioni specifiche del progetto.
3. Si ripete il passo (1) ora che si ha la chiave.

Come minimo dovrebbe essere disponibile un **fingerprint**. Basta mettere il fingerprint (es. in formato `.sha256`) nella stessa directory del file e lanciare `sha256 -c FILE.sha256`.

> **Distinzione firma vs fingerprint/hash**: la **firma digitale** (`gpg --verify`) prova *autenticità + integrità* (chi l'ha prodotto e che non è stato alterato), ma richiede fiducia in una chiave pubblica. Il **fingerprint/hash** (`sha256`) prova solo *integrità* (il file non è cambiato rispetto a quello di cui il produttore ha pubblicato l'hash) — non dice nulla su chi l'ha prodotto se non ti fidi già del canale su cui hai preso l'hash. Sono controlli diversi con garanzie diverse.

### 8.2 Installazione da sorgenti: la trappola della fiducia

Installare da sorgenti *offre la possibilità teorica di verificare il codice*. Ma:

- **se non lo fai davvero, è un falso senso di sicurezza**;
- se ti limiti a fidarti della firma sull'archivio, **non è diverso dal verificare la firma su un binario** (non hai guadagnato nulla in sicurezza rispetto al binario firmato);
- è **più difficile da manutenere**;
- richiede **MOLTI componenti ausiliari** (header, librerie, processori di macro, compilatori, linker…) — e **ognuno di essi può avvantaggiare un attaccante**. Il riferimento classico è il **Ken Thompson Hack**: un compilatore compromesso può inserire backdoor nei binari che compila (e persino in una nuova versione di sé stesso), rendendo inutile ispezionare il *sorgente* perché il male sta nel *toolchain*.

Da qui l'ingresso di **distribuzioni e pacchetti** come soluzione pragmatica:

- **chiavi di verifica installate una volta per tutte** — comodo, ma diventa un **Single Point Of Failure** (SPOF): se quella chiave è compromessa, cade tutto;
- **gestione automatica delle dipendenze**;
- **garanzia di compatibilità binaria** tra tutti gli elementi del set.

> **Perché il Ken Thompson Hack è citato**: dimostra che "installo da sorgenti così controllo tutto" è un'illusione se non controlli anche il compilatore, il linker, le librerie — un regresso infinito di fiducia analogo a quello del boot (§7). La soluzione, come per il boot, è spostare la fiducia su un punto gestito centralmente (la distribuzione), accettandone i limiti (lo SPOF della chiave).

### 8.3 Installazione assistita e package manager

L'installazione è comunemente effettuata tramite **software ausiliari**: il **package manager** specifico della distribuzione (rpm/yum, dpkg/apt…) o un installer su Windows. Un tool di installazione:

- **può farsi carico delle verifiche relative alle dipendenze**;
- **non può configurare ogni dettaglio del sistema** in modo specifico;
- **può generare dinamicamente dati specifici**.

Le dipendenze formano un **grafo** (es. `glibc` serve a `gtk`, `firefox`, `zlib`…; `zlib` serve ad `apache`; `apache` serve a `php`). "A → B" significa "A serve per B", dove *servire* può essere logico (non ha senso un linguaggio di generazione pagine web senza un web server) o fisico (un binario linkato dinamicamente non gira senza le librerie di cui importa i simboli).

### 8.4 Debian e Red Hat: pacchetti e repository

Le due **distribuzioni capostipite** da cui derivano quasi tutte le varianti, con due sistemi di gestione dei pacchetti molto simili, articolati su tre livelli: tool **di basso livello** (singolo pacchetto), tool **intermedi** (gestione coordinata di pacchetti + dipendenze), tool per il **reperimento automatico dai repository**.

**Anatomia del nome del pacchetto** (candidato a domanda):

- Debian/derivate (.deb): `aptitude-0.2.15.9-2_i386.deb` → **nome** (`aptitude`) · **versione del software** (`0.2.15.9`) · **versione del pacchetto** (`2`) · **architettura** (`i386`).
- RedHat/derivate (.rpm): `httpd-2.4.6-45.el7.centos.x86_64.rpm` → nome · versione software · versione pacchetto · architettura.

> **Distinzione "versione del software" vs "versione del pacchetto"**: la prima è la versione del programma a monte (upstream); la seconda incrementa quando il *packaging* cambia (patch della distribuzione, correzioni allo script di installazione) a parità di software. Due errori diversi da non confondere.

**Repository**: raccolte indicizzate di pacchetti, online o su filesystem locale. I package manager leggono per ogni repo l'**indice e i metadati**, così conoscono le versioni disponibili e le dipendenze (e come risolverle). Collocazioni tipiche:

- APT: `/etc/apt/sources.list` e `/etc/apt/sources.list.d/*` — es. `deb http://archive.ubuntu.com/ubuntu bionic-updates universe`.
- YUM: `/etc/yum.conf` e `/etc/yum.repos.d/*.repo` — con direttive come `gpgcheck=1` e `gpgkey=file:///etc/pki/rpm-gpg/RPM-GPG-KEY-CentOS-7`.

### 8.5 Verifica dell'autenticità dei pacchetti

La **firma dei pacchetti è gestita centralmente**: i *mantainer* della distribuzione forniscono le chiavi di verifica nei media di installazione ufficiali o sui repository online. I set di chiavi si possono gestire in modo standard con **GnuPG** (es. i sistemi .deb mettono i keyring in `/etc/apt/trusted.gpg.d/`), ma è **più comune usare gli strumenti forniti dalla distribuzione**:

- .deb: `apt-key {add file | list | del keyid | adv --recv-key keyid | …}` — **deprecato da tempo ma ancora in uso**; metteva tutte le chiavi nello stesso file `/etc/apt/trusted.gpg`.
- .rpm: `rpm {--import | -e | -q[ai] | …}` — **rpm tratta le chiavi come se fossero pacchetti**, quindi si usano gli stessi comandi per interrogarle, eliminarle, ecc.

### 8.6 Lavorare coi repository esterni: il rischio dell'autenticazione disattivata

Esigenza comune: installare software ben supportato ma **non incluso nei canali ufficiali**. Si aggiunge semplicemente il repository all'elenco — ma **succede che non tutti supportino l'autenticazione**, e la si disattiva:

- APT: `deb [allow-insecure=yes] http://good.site/virtualbox/debian bookworm contrib`
- YUM: nel `.repo`, `gpgcheck=0`.

> **Threat model dell'`allow-insecure`/`gpgcheck=0`**: disattivare la verifica della firma significa installare pacchetti la cui autenticità non è provata. È comodo (funziona subito) ma apre alla sostituzione malevola dei pacchetti (man-in-the-middle sul mirror, mirror compromesso). È l'equivalente, per il software, di avviare un SO non firmato: si è rinunciato alla catena di fiducia.

### 8.7 Cross-signing threat (la minaccia sottile dei keyring condivisi)

Nelle distro .deb era diffuso l'uso di righe di configurazione **prive di specifica della chiave**: `deb http://download.virtualbox.org/virtualbox/debian xenial contrib`. In questo caso vengono usate **tutte le chiavi collocate in posti "fidati"** (`/etc/apt/trusted.gpg` e `/etc/apt/trusted.gpg.d/*`). Conseguenza: **una chiave importata per convalidare *una* fonte di pacchetti può essere usata per *tutti*** → **cross signing**. Se un repo viene violato e la sua chiave privata sottratta, quella chiave può **pubblicare aggiornamenti fraudolenti per qualsiasi pacchetto, anche degli altri**.

**Best practice correnti**: legare ogni fonte alla *sua* chiave.

- Opzione sulla singola riga: `deb [arch=amd64 signed-by=/usr/share/keyrings/oracle-virtualbox-2016.gpg] https://download.virtualbox.org/virtualbox/debian bookworm contrib`.
- File di configurazione in stile "rpm-like" (`.sources` con campo `Signed-By: /usr/share/keyrings/ubuntu-archive-keyring.gpg`).

> **Perché il cross-signing è pericoloso e la distinzione con `allow-insecure`**: sono due debolezze diverse. `allow-insecure`/`gpgcheck=0` = *nessuna* verifica. Cross-signing = c'è verifica, **ma con lo scope sbagliato**: la chiave giusta per un repo minore diventa valida per l'intero sistema. `signed-by` risolve il secondo problema restringendo *quale* chiave è accettata *per quale* fonte.

### 8.8 Gestire la provenienza dei pacchetti: software injection

Confusione possibile se un pacchetto con lo **stesso nome** esiste in **versioni diverse in repository differenti**. I package manager, di default, **scelgono sempre la versione più avanzata**. Scenario d'attacco: si è aggiunto un repo semisconosciuto per un'app innocua; se a quel repo viene aggiunto un pacchetto **"core"** dichiarato più recente della versione ufficiale → **software injection** (il sistema aggiorna un componente critico prelevandolo dal repo malevolo). In alcuni casi anche aggiornamenti nello stesso repo sono indesiderabili (situazioni legacy). La situazione va **controllata e gestita**:

- Provenienza di un pacchetto: YUM `repoquery -i [package name]`; APT `apt-cache showpkg [package name]`.
- Elenco pacchetti da un repo: YUM `yum list installed | grep [repo name]`; APT: vari comandi per estrarre info dalla cache.

### 8.9 Limitare le modifiche automatiche: version locking/pinning

Per evitare a priori problemi in sistemi con dipendenze complesse (mix di pacchetti installati a mano e via package manager) si usa il **version locking/pinning**:

- APT: editare `/etc/apt/preferences.d/*` (Apt Preferences/pinning).
- YUM: `yum install yum-plugin-versionlock`, poi `yum versionlock [package name]` (o editare `/etc/yum/pluginconf.d/versionlock.list`).

> **Perché il pinning è una contromisura di sicurezza e non solo di stabilità**: bloccare la versione di un pacchetto critico è anche una difesa contro la software injection (§8.8): impedisce che un repo dichiari una versione "più recente" e me la faccia installare al posto di quella fidata.

### 8.10 DevOps woes: dependency confusion

**DevOps** (development + operations) automatizza build e deployment, inclusa **l'inclusione automatica delle dipendenze**. Il problema: **raramente c'è una gestione corretta dei namespace** — es. `npm` per Node è praticamente *flat* (piatto, senza namespace robusti). Scenario (**dependency confusion**): un'azienda sviluppa internamente un pacchetto `myutils`; un attaccante registra un pacchetto `myutils` nel repo pubblico di default; al prossimo build, **quale prende il sistema di CI/CD?** Se prende quello pubblico (magari perché ha numero di versione più alto), esegue codice dell'attaccante nella pipeline.

> **Connessione con §8.8**: dependency confusion è software injection portata nel mondo dei package manager di linguaggio (npm, pip…). Stessa logica ("il sistema sceglie la versione/fonte sbagliata perché ha lo stesso nome"), contesto diverso (build automatizzati invece di aggiornamenti di sistema). La radice comune è la mancanza di un *namespace* che distingua "il mio pacchetto interno" da "un pacchetto pubblico omonimo".

---

## 9. Due parole su cloud security

Nel cloud, **a seconda del livello di servizio utilizzato, molti problemi "svaniscono"** (delegati al provider). I livelli, dal più basso al più alto (schema slide 32):

- **Hardware** (i server fisici) — sotto tutto.
- **IaaS** (Infrastructure as a Service): Computer, Network, Storage — es. EC2, S3, VPC.
- **PaaS** (Platform as a Service): Components, Services — es. runtime Java/Node/Ruby, Lambda, API Gateway.
- **SaaS** (Software as a Service): User Interface, Machine Interface — es. G Suite, applicazioni web pronte.

> **Perché "svaniscono" e la distinzione tra i livelli**: più si sale (IaaS → PaaS → SaaS), più responsabilità (e controllo) si cede al provider. In IaaS gestisco ancora il sistema operativo della VM (e me ne assumo la sicurezza); in SaaS uso solo l'applicazione e quasi tutta la sicurezza è del provider. È il modello della **responsabilità condivisa**: chi è responsabile di cosa dipende dal livello scelto. Una domanda tipica: "In SaaS il cliente è responsabile del patching del sistema operativo sottostante? → **Falso**: a quel livello lo gestisce il provider."

### 9.1 Sicurezza: cloud vs. on-premise

- I problemi di sicurezza del cloud riguardano **raramente** la sicurezza dell'host e della rete (di cui si occupa il provider).
- C'è un **impatto "emotivo" della distanza**: la **perdita di controllo**.
- **Osservazione razionale**: il più delle volte i fornitori cloud hanno **team di sicurezza di livello mondiale** che quasi nessuna azienda potrebbe permettersi per i propri data center.
- La **due diligence** suggerisce però di **verificare** questa affermazione quando si seleziona un fornitore: **certificazione ISO27001** (con il suo *ambito di applicazione*) e risultati di un **audit SAS70 di tipo II**.
- Paradossalmente, **alcune minacce reali riguardano la disponibilità**: **lock-in**, **dipendenza dalla rete**, **cessazione dell'attività** del fornitore.

> **Perché la certificazione va letta con l'"ambito di applicazione"**: una ISO27001 certifica che *un certo perimetro* è gestito secondo lo standard — ma se il servizio che uso è fuori da quel perimetro, la certificazione non mi copre. Errore da manuale: fidarsi del bollino senza guardare *cosa* certifica.

### 9.2 I benefici potenziali del cloud per la sicurezza

Le misure di sicurezza sono **più economiche su scala ampia**:

- **Collocazioni multiple** = ridondanza di istanze e dati = indipendenza dai guasti (anche dolosi) e opportunità di ripristino.
- **Tempestività migliorata** nella risposta agli incidenti.
- **Gestione delle minacce** con specialisti dedicati.
- La **sicurezza come elemento di differenziazione sul mercato**: il **CSC** (Cloud Service Customer, il cliente) sceglie in base alla reputazione di riservatezza/integrità/resilienza del **CSP** (Cloud Service Provider) — forte motore per i CSP a migliorare.
- **Aggiornamenti più tempestivi**: immagini di VM pre-rafforzate e aggiornate centralmente; IaaS che consente snapshot regolari e deploy rapido su piattaforme omogenee.
- **Concentrazione delle risorse e ridimensionamento rapido**: applicare controlli e policy in modo economico; il CSP può **scalare dinamicamente** i meccanismi difensivi (traffic shaping, filtraggio, crittografia) durante un attacco.
- **Sicurezza come servizio e raccolta di prove**: interfacce standardizzate di sicurezza gestita; IaaS che clona VM e offre storage per i log utile ad **analisi forensi offline** senza degradare le prestazioni.
- **Gli SLA impongono una migliore gestione del rischio**: per quantificare le sanzioni negli SLA, i CSP adottano audit interni e valutazioni del rischio più rigorosi.

> **Definizioni CSC e CSP (da tenere dritte)**: **CSC** = *Customer* (chi compra/usa il servizio cloud); **CSP** = *Provider* (chi lo eroga). Molte domande sui rischi organizzativi (§9.4) giocano proprio sul chi-fa-cosa tra questi due attori.

**Connessione con S10 (NIDS) e con l'analisi forense**: il cloud che offre "storage conveniente per i log" e "clonazione di VM per analisi forense offline" è la controparte infrastrutturale della rilevazione (S10): i dati che un NIDS produce e i log da correlare trovano nel cloud un luogo economico dove essere conservati e analizzati senza toccare i sistemi in produzione.

### 9.3 Attori e minacce nel cloud

Lo schema (slide 39) mostra che attorno alla "nuvola" gravitano molti attori, ciascuno una potenziale minaccia: Government, Identity provider, Attribute provider, Image/application publisher, Cloud provider, Transport agent, Hacker/cracker, Competitor, Cloud broker, Consumer. Il messaggio: la superficie di fiducia nel cloud è **molto più affollata** che on-premise — ci si fida (volenti o nolenti) di parecchi terzi.

### 9.4 I rischi specifici del cloud: tre categorie

Il cuore "da quiz" della parte cloud. **Tre categorie**:

**A) Rischi Organizzativi**
- **Perdita di controllo** — *forse il rischio considerato più grave*: il CSC cede il controllo al CSP su molti aspetti critici; se lo SLA lascia un *gap* rispetto alle necessità, non c'è modo di chiuderlo; outsourcing/subcontracting possono introdurre attori non fidati; il CSC non può verificare autonomamente la compliance del CSP.
- **Lock-in** — aspetti proprietari rendono difficile la migrazione (esiste anche on premise, ma lì almeno i dati restano in mano al CSC).
- **Supply Chain Failure** — l'outsourcing crea catene di fornitura *forti quanto l'anello più debole*.
- **Interferenze tra politiche di sicurezza CSC-CSP** — il CSC potrebbe volere controlli in conflitto con l'ambiente del CSP (non implementabili); le insicurezze di *un* CSC possono diventare vulnerabilità dell'intera piattaforma condivisa.

**B) Rischi Tecnici**
- **Economic Denial of Service (EDoS)** — con servizi *pay-per-use* che scalano automaticamente, un attacco di sovraccarico, **invece di degradare le prestazioni, aumenta i costi**. È il "DoS economico".
- **Vulnerabilità della piattaforma** — un attacco all'infrastruttura potrebbe dare accesso a *tutte* le VM (molto improbabile ma devastante); più plausibile la **compromissione dell'interfaccia di gestione**.
- **Cedimento dell'isolamento** — la **multi-tenancy** permette teoricamente di installare una VM malevola *accanto* a quella della vittima: possibili **attacchi cross-VM via side channel**, forzatura di migrazioni saturando l'host, **intercettazione dei dati in transito** (non tanto quelli dell'utente — che deve cautelarsi cifrando **end-to-end** — quanto le operazioni trasparenti del CSP: sincronizzazioni, migrazioni).

**C) Rischi Legali**
- **Protezione dei dati** — legislazioni differenti; potrebbe essere **illegale trasferire certi dati in certi paesi**; il CSP potrebbe spostare i dati tra i propri datacenter **senza dirlo al CSC**.
- **Giurisdizione** — il CSP potrebbe essere costretto ad azioni dagli organi giudiziari sulla base delle leggi del paese della sede legale o dei datacenter; il CSC potrebbe subire interruzioni o **sequestro di dati per motivi che non sussistono nel proprio paese**.

> **Distinzioni da non confondere nei rischi cloud** (fonte tipica di domande a scelta multipla):
> - **EDoS vs DoS classico**: il DoS classico *nega il servizio*; l'EDoS lo mantiene ma *fa esplodere il conto* sfruttando l'auto-scaling pay-per-use.
> - **Lock-in (organizzativo) vs cedimento dell'isolamento (tecnico)**: il primo è un problema di *dipendenza contrattuale/proprietaria* (difficile andarsene); il secondo è un problema *tecnico* di multi-tenancy (il vicino di rack ti attacca). Categorie diverse.
> - **Cedimento dell'isolamento vs vulnerabilità della piattaforma**: il primo è "il tenant accanto rompe l'isolamento tra VM"; il secondo è "l'infrastruttura stessa/l'interfaccia di gestione è bucata". Il secondo è più raro ma colpisce *tutti* i tenant.
> - **Rischi legali** = *dove* stanno i dati e *quali leggi* si applicano; sono l'altra faccia della **delocalizzazione** vista al §1.

**Connessione con S12/S13 (Sicurezza delle comunicazioni, TLS)**: la contromisura esplicita al cedimento dell'isolamento sul fronte dati in transito è la **cifratura end-to-end** — cioè esattamente la materia di S12/S13 (protezione delle comunicazioni, TLS). Il modulo S6 identifica la minaccia (intercettazione nel multi-tenant) e rimanda per la soluzione tecnica alla crittografia dei canali.

---

## 10. Sintesi dei fili conduttori

1. **La collocazione decide il modello di minaccia**: on-premise → accesso fisico; cloud → condivisione + delocalizzazione. Le contromisure si adattano, non spariscono.
2. **L'accesso fisico scavalca le difese di rete** (contrappunto diretto a S5).
3. **Regresso della fiducia**: chi verifica chi? Sia nel boot (anti-malware ← SO ← bootloader ← BIOS ← hardware root of trust) sia nel software da sorgenti (Ken Thompson Hack). La soluzione è sempre ancorare la fiducia a un punto gestito/incorruttibile e costruire una catena.
4. **Measured ≠ Trusted ≠ Secure Boot**: misurare / misurare+bloccare / implementazione UEFI di trusted boot.
5. **Provenienza del software**: firma vs hash, chiavi centralizzate (comode ma SPOF), scope delle chiavi (cross-signing → `signed-by`), scelta della versione/fonte (software injection, dependency confusion).
6. **Cloud**: responsabilità condivisa per livello (IaaS/PaaS/SaaS); benefici reali (scala, ridondanza, competenze) ma rischi propri (organizzativi/tecnici/legali), con la disponibilità e la delocalizzazione come temi ricorrenti.

---

## 11. Autoverifica — domande in stile quiz d'esame

> Formato reale: vero/falso e scelta multipla, penalità sulle risposte sbagliate. Rispondi *prima* di guardare le soluzioni negli appunti. Molte domande sono costruite sulle **distinzioni** segnalate nella lezione, perché è lì che si cade.

**Vero/Falso**

1. Un firewall correttamente configurato protegge il sistema anche da un attaccante con accesso fisico che avvia la macchina da un supporto esterno. *(V/F)*
2. Il Measured Boot, da solo, blocca l'avvio non appena rileva un componente non fidato. *(V/F)*
3. Secure Boot è semplicemente il nome dato all'implementazione di Trusted Boot basata su UEFI. *(V/F)*
4. Nel database UEFI Secure Boot, `db` è la lista delle immagini *proibite* e `dbx` quella delle immagini *autorizzate*. *(V/F)*
5. Passare `init=/bin/bash` come parametro al kernel dal bootloader può fornire una shell di root senza autenticazione. *(V/F)*
6. Le password del BIOS sono considerate una protezione sufficiente da sole, perché non hanno meccanismi di reset. *(V/F)*
7. In `shim`, l'iscrizione di una MOK avviene automaticamente da remoto senza intervento alla console. *(V/F)*
8. `gpg --verify` fornisce una garanzia di sola integrità, mentre un hash `sha256` fornisce anche autenticità. *(V/F)*
9. Impostare `gpgcheck=0` in un repo YUM disattiva la verifica della firma dei pacchetti provenienti da quel repo. *(V/F)*
10. Un attacco EDoS tipicamente riduce la disponibilità del servizio negandolo del tutto. *(V/F)*
11. La disponibilità (alimentazione, condizionamento, connettività) è il terzo vertice della triade CIA. *(V/F)*
12. In un modello SaaS, il cliente (CSC) è responsabile del patching del sistema operativo sottostante. *(V/F)*

**Scelta multipla**

13. In che situazione la direttiva GRUB `lock` protegge effettivamente un item del menu?
    a) sempre, in modo autonomo;
    b) solo se esiste una direttiva `password` nella *global section*;
    c) solo se il BIOS ha una password impostata;
    d) solo con Secure Boot attivo.

14. Il cross-signing threat nei sistemi APT consiste in:
    a) l'assenza totale di verifica delle firme;
    b) una chiave importata per una fonte che diventa valida per *tutte* le fonti fidate;
    c) la scelta automatica della versione più recente di un pacchetto;
    d) la cifratura end-to-end dei pacchetti.

15. La contromisura best-practice al cross-signing è:
    a) `allow-insecure=yes`;
    b) `gpgcheck=0`;
    c) legare la fonte alla sua chiave con `signed-by=`/`Signed-By:`;
    d) usare sempre `apt-key add`.

16. La *remote attestation* è resa possibile principalmente da:
    a) Secure Boot UEFI che blocca il boot;
    b) Measured Boot che registra gli hash nei PCR, verificabili da un sistema esterno;
    c) le password del bootloader;
    d) la cifratura del disco.

17. Il "Ken Thompson Hack" illustra che:
    a) installare da sorgenti garantisce sempre la sicurezza;
    b) un toolchain compromesso (es. il compilatore) può inserire backdoor invisibili nel sorgente;
    c) i pacchetti .deb sono più sicuri dei .rpm;
    d) i fingerprint sha256 sono inutili.

18. Quale coppia associa correttamente rischio cloud → categoria?
    a) Lock-in → tecnico;
    b) Cedimento dell'isolamento → organizzativo;
    c) EDoS → tecnico; giurisdizione → legale;
    d) Supply chain failure → legale.

19. La "dependency confusion" (DevOps) è concettualmente più vicina a:
    a) il power glitching;
    b) la software injection da repository (scelta della fonte/versione sbagliata per omonimia);
    c) il tailgating;
    d) la remote attestation.

20. Nella catena di fiducia del boot, la *hardware root of trust* è necessaria perché:
    a) è più veloce del software;
    b) qualsiasi verifica puramente software può essere compromessa dallo stesso attaccante che compromette il componente verificato;
    c) il BIOS non esiste più con UEFI;
    d) i PCR sono modificabili a piacere.

*(Soluzioni ragionate nel file di appunti corrispondente.)*

---

<!-- Fine lezione S6. Contenuto ancorato integralmente alle 42 slide del PDF; nessun concetto aggiunto oltre a ciò che il PDF tratta. -->
