# Appunti — Modulo S6: Sicurezza fisica e collocazione delle risorse (on-premise / cloud)

**Corso**: Lab Sicurezza Informatica T
**Lezione di riferimento**: `lezione_moduloS6_sicurezza_fisica_cloud.md`
**PDF sorgente**: `SLIDE TEORIA/SICINF/Sicurezza_fisica_e_collocazione_in_cloud_10_aprile.pdf` (42 slide)
**Natura**: modulo teorico, nessun LAB. Materia da quiz (40%): vero/falso e scelta multipla con penalità sulle risposte sbagliate. Molte domande sono costruite sulle *distinzioni* fra termini simili — è lì che si cade.
**Stato**: lezione letta e verificata; appunti consolidati con processo critico (rilettura lezione+PDF paragrafo per paragrafo, domande generate e risolte). Nessun grezzo preesistente: modulo mai studiato prima.

---

## 1. On premises vs. in the cloud — perché la collocazione cambia il modello di sicurezza

Tutti i controlli d'accesso alle informazioni visti finora sono **mediati**: fra me e il dato c'è sempre un intermediario che decide chi legge/scrive. I due intermediari sono il **sistema operativo** (permessi sui file) e la **gestione dei segreti** (chiavi crittografiche). Entrambi presuppongono che l'hardware sottostante funzioni bene e che il software sia autentico e integro: la **collocazione fisica** decide quanto quell'assunzione regge.

> **Domanda**: cosa vuol dire esattamente che i controlli sono "mediati", e perché è il punto di partenza del modulo?
> **Risposta**: "mediato" significa che il permesso di accedere al dato non è una proprietà fisica del dato stesso, ma una decisione presa da un software *sopra* di esso (il kernel che controlla i permessi, il gestore delle chiavi che decide se decifrare). Questa mediazione funziona **solo finché quel software gira come previsto**. Se l'attaccante scavalca il software — per esempio avviando la macchina con un *proprio* sistema operativo, o staccando il disco e leggendolo altrove — la mediazione sparisce e con essa ogni controllo d'accesso. Il modulo parte da qui perché tutto il resto (boot sicuro, cifratura, sicurezza fisica) serve a difendere proprio l'assunzione implicita su cui la mediazione poggia.

**On premises** (macchina "in casa mia"): nessuna condivisione dell'infrastruttura; relativa semplicità nel tenere separati segreti, sistemi e dati (password e chiavi si inseriscono manualmente); ma resta a carico mio garantire il **corretto funzionamento dell'hardware** e **l'esecuzione di SO e software integri e autentici**.

**In the cloud**: gestione hardware/software di altissimo livello delegata al fornitore, ma **ambienti di memorizzazione ed elaborazione condivisi** con altri clienti e **delocalizzazione** (non so fisicamente dove sono i miei dati).

> **Domanda**: condivisione e delocalizzazione sono la stessa cosa? Tendo a confonderle.
> **Risposta**: no, sono due proprietà distinte del cloud, entrambe assenti on-premise. **Condivisione** (multi-tenancy) = le *stesse* risorse fisiche (CPU, RAM, storage) ospitano più clienti contemporaneamente → problema di *isolamento* fra vicini (§9.4, cedimento dell'isolamento). **Delocalizzazione** = non so *dove geograficamente* stanno i miei dati, e possono spostarsi → problema *legale/giurisdizionale* (§9.4, rischi legali) e di *perdita di controllo*. Una domanda d'esame può attribuire una minaccia all'una o all'altra: "attacco cross-VM del vicino di rack" → condivisione; "sequestro dei dati per una legge estera" → delocalizzazione.

Nota chiave: passando al cloud molti problemi **non spariscono, cambiano forma**. L'accesso fisico dell'insider diventa il vicino di rack multi-tenant; la logica delle contromisure si adatta. Contrappunto diretto a S5 (firewall): **le contromisure di rete possono essere facilmente scavalcate da chi ha accesso fisico**. Rete (S5) e presenza fisica (S6) sono due superfici d'attacco disgiunte.

---

## 2. On premises — la messa in sicurezza fisica

Un server è, prima ancora di un nodo di rete, **un sistema di calcolo collocato in un ambiente e connesso a molti dispositivi**. Di solito le difese si concentrano sul software (applicazioni, SO, attacchi via rete), ma quelle difese si scavalcano con accesso fisico. Le **tre minacce fisiche principali**:

1. **Furto** dello storage o dell'intero calcolatore.
2. **Connessione di sistemi di raccolta dati** alle interfacce (dispositivi agganciati fisicamente per esfiltrare/iniettare).
3. **Avvio del sistema con un SO arbitrario** (boot da supporto esterno controllato dall'attaccante).

La gravità **dipende fortemente dallo specifico ambiente**: un data center presidiato con badge e telecamere è esposto in modo diverso da un open space.

> **Domanda**: perché "avviare la macchina con un altro SO" è così grave? In fondo i miei file sono protetti dai permessi.
> **Risposta**: perché i permessi del file system (proprietario, `rwx`, ecc.) li fa rispettare **il *mio* sistema operativo mentre gira**. Se l'attaccante avvia un SO *suo* dal suo supporto (chiavetta, CD, disco esterno), quel SO monta il mio disco come semplice volume di dati e **ignora completamente i miei permessi**: li legge come metadati, non come regole da applicare a sé stesso, perché root sul *suo* sistema può leggere tutto. È esattamente lo scavalcamento della "mediazione" del §1. L'unica difesa reale a quel punto non è più il permesso, ma la **cifratura del disco** (i dati restano illeggibili senza la chiave, indipendentemente da chi li monta).

---

## 3. Fattori non informatici: come si ottiene l'accesso fisico

Poiché l'accesso abilita gli attacchi specifici, la prima domanda difensiva è *come entra fisicamente un attaccante*. Le vie tipiche:

- **Insider**: chi ha già accesso legittimo e ne abusa. La più difficile da contrastare (nessun perimetro da forzare) e la posizione più potente.
- **Tailgating**: seguire una persona autorizzata attraverso una porta controllata senza autenticarsi (il classico "mi tieni la porta?").
- **Errata identificazione di visitatori**: far passare per legittimo chi non lo è (finto tecnico, finto corriere).
- **Social engineering**: manipolare le persone perché concedano accesso o informazioni.
- **Effrazione**: forzatura fisica vera e propria.

Contro questi vettori serve la **sicurezza fisica "tradizionale"**, definita *essenziale*: **regolamenti chiari e condivisi**, **perimetro robusto**, **sorveglianza e procedure**.

> **Domanda**: tailgating, social engineering ed errata identificazione dei visitatori mi sembrano quasi la stessa cosa. Come li tengo separati per un vero/falso?
> **Risposta**: si distinguono per *cosa* sfrutta l'attaccante. **Tailgating** = sfrutta la *fisica della porta*: entra materialmente dietro qualcuno, senza necessariamente parlargli o ingannarlo (basta che la porta resti aperta un attimo). **Social engineering** = sfrutta la *psicologia*: convince attivamente una persona a concedergli qualcosa (accesso, password, un badge). **Errata identificazione dei visitatori** = è il *fallimento del controllo di identità*: il sistema/procedura scambia un estraneo per legittimo (finto tecnico con pettorina). Spesso si combinano (il social engineering *causa* l'errata identificazione), ma la domanda d'esame vuole l'etichetta precisa del meccanismo primario.

### La disponibilità è il terzo vertice della triade CIA

La sicurezza fisica non tocca solo riservatezza e integrità: la **disponibilità** (Availability, terzo vertice della triade **CIA** con Confidentiality e Integrity) è minacciata proprio da fattori fisici/ambientali: **alimentazione** (manca la corrente), **connettività** (cade il link), **condizionamento** (surriscaldamento della sala), **incidenti, disastri, attentati**.

> **Domanda**: come attribuisco al vertice giusto della triade una minaccia fisica? È una domanda tipica.
> **Risposta**: chiediti *quale proprietà del dato viene violata*.
> - **Confidentiality (riservatezza)**: qualcuno legge ciò che non dovrebbe → **furto del disco**, keylogger, videoghosting, intercettazione.
> - **Integrity (integrità)**: qualcuno altera ciò che non dovrebbe → **manomissione del software al boot**, key injection, BadUSB che digita comandi.
> - **Availability (disponibilità)**: il legittimo proprietario *non riesce ad accedere* → **blackout, condizionamento saltato, link giù, disastro**, EDoS nel cloud.
> Attenzione: il furto del disco è primariamente riservatezza ma tocca *anche* la disponibilità (se non ho backup, quel dato l'ho perso). Nei quiz però la risposta attesa è di norma il vertice *principale*.

---

## 4. Vulnerabilità sfruttabili "in presenza"

Con accesso fisico anche breve entra in gioco un arsenale specifico. Il PDF (con riferimenti a casi reali) elenca:

- **BadUSB e simili**: dispositivo USB il cui *firmware* è stato riprogrammato per fingersi altro (es. una chiavetta che si presenta come **tastiera** e digita comandi). Insidioso perché la minaccia è nel *firmware della periferica*, non in un file scansionabile dall'antivirus.
- **Thunderspy**: attacchi che sfruttano l'accesso diretto alla memoria (**DMA**) offerto da porte ad alte prestazioni (**Thunderbolt**) per leggere/scrivere la RAM scavalcando il SO.
- **Keylogging e videoghosting**: dispositivi hardware interposti fisicamente (un *KeyGrabber* fra tastiera e PC; un *VideoGhost* sul cavo video) che registrano quanto digitato o visualizzato. Non lasciano traccia software.
- **Key injection** (keystroke injection): iniezione di sequenze di tasti per far eseguire comandi come se li avesse battuti l'utente.
- **Disk un/plugging**: scollegare/ricollegare dischi, incluse tecniche per **bypassare i Self-Encrypting Drive (SED)**.
- **Power glitching**: disturbare deliberatamente l'alimentazione per provocare errori nel processore in istanti critici, così da far saltare controlli di sicurezza altrimenti solidi (attacco *hardware* al software sicuro).

> **Domanda**: cos'è il DMA e perché Thunderbolt lo rende pericoloso?
> **Risposta**: **DMA** (*Direct Memory Access*) è un meccanismo per cui una periferica può leggere/scrivere direttamente nella RAM **senza passare dalla CPU** (nato per efficienza: una scheda di rete o un disco copiano dati in memoria senza tenere occupato il processore). Thunderbolt è una porta ad altissime prestazioni che, per essere veloce, concede alle periferiche collegate proprio l'accesso DMA. Il problema di sicurezza: un dispositivo malevolo collegato alla porta Thunderbolt può **leggere l'intera RAM** (chiavi di cifratura, password in chiaro, dati sbloccati) o **scriverla** per manomettere processi, il tutto **scavalcando il sistema operativo**, che non media più quell'accesso. È di nuovo lo scavalcamento della mediazione, stavolta a livello di memoria fisica.

> **Domanda**: cos'è un SED e come si fa a "bypassarlo" staccando il disco? Se si auto-cifra, non dovrebbe essere sicuro?
> **Risposta**: un **SED** (*Self-Encrypting Drive*) è un disco che cifra/decifra i dati *in hardware*, con una chiave che sta nel disco stesso; all'avvio la chiave viene "sbloccata" (tipicamente con una password/autenticazione) e da quel momento il disco serve dati in chiaro finché resta alimentato. Il bypass sfrutta proprio questo: una volta che il disco è stato **sbloccato all'avvio**, se lo si stacca "a caldo" (senza togliere l'alimentazione, con opportuni accorgimenti) e lo si ricollega a un'altra macchina, in certi scenari il disco **resta nello stato sbloccato** e serve i dati in chiaro anche al nuovo host. La lezione da trarre: l'auto-cifratura protegge il disco *spento e non sbloccato*, non necessariamente il disco *già sbloccato e in funzione* — motivo per cui la protezione va accompagnata da controllo dell'accesso fisico.

> **Distinzione centrale (esfiltra vs comanda)**: il **keylogger hardware** *registra passivamente* ciò che passa (esfiltra); la **key injection / BadUSB-tastiera** *inietta attivamente* input (comanda). Entrambi passano dalla porta USB ma fanno cose opposte: uno **ruba** ciò che digiti (minaccia alla riservatezza), l'altro **digita al posto tuo** (minaccia all'integrità). Non confonderli in un vero/falso.

> **Domanda**: il power glitching mi sembra fantascienza. Cosa fa concretamente e perché "batte" un software sicuro?
> **Risposta**: consiste nel disturbare deliberatamente e con precisione l'alimentazione (o il clock) del chip — un micro-calo di tensione (*glitch*) nell'istante giusto. In quell'istante il processore può *sbagliare un'istruzione*: per esempio un controllo `if (password_corretta)` può essere fatto saltare, o un contatore di tentativi non incrementato. È un attacco **hardware al software**: non trova un bug nel codice, ma corrompe *fisicamente l'esecuzione* del codice corretto. Per questo "scavalca" difese logiche solide — non le aggira, le fa proprio fallire a livello elettrico. Richiede accesso fisico e strumentazione, ma è reale nei contesti ad alta sicurezza (smart card, secure element).

Il filo comune di tutti questi attacchi: **le periferiche fisiche e il firmware sono fidati per default**. Il sistema si aspetta che una tastiera sia una tastiera. Difese: disabilitare porte/periferiche non usate, cifrare, controllare l'integrità del firmware, limitare l'accesso fisico non presidiato.

---

## 5. Collocazione "in remoto": la macchina fuori dal controllo diretto

Quando il calcolatore sta dove non ho controllo fisico diretto (housing/colocation, o comunque un sito non presidiato da me), si adottano misure che rendano *inutile* l'accesso fisico altrui:

- **Case chiudibile e fissabile al rack** (contro furto e apertura).
- **Dispositivi di rilevazione delle intrusioni** fisiche (sensori di apertura del case).
- **Protezione dei dati che renda inutile il furto** → tipicamente **cifratura**. Rovescio della medaglia: se i dati sono cifrati, **l'accesso va abilitato manualmente** (bisogna fornire la chiave/passphrase all'avvio), il che complica il funzionamento non presidiato.
- **Disabilitare le periferiche non utilizzate** (riduce la superficie degli attacchi "in presenza" del §4), salvo riabilitarle per esigenze nuove.

> **Il compromesso ricorrente del modulo (memorizzalo, torna più volte)**: quasi ogni contromisura fisica robusta **peggiora l'automazione**. Un sistema che riparte da solo dopo un blackout è comodo ma indifeso; un sistema che chiede una passphrase all'avvio è protetto ma non riparte da solo. È la tensione **sicurezza ↔ disponibilità/automazione**: una domanda d'esame può presentarla come trade-off da riconoscere.

---

## 6. Attacchi fisici alle risorse logiche: il processo di boot

Cuore tecnico del modulo. Il sistema, per andare a regime, attraversa un **processo di boot in quattro fasi**, e **ognuna è dirottabile** da chi ha accesso fisico, per far caricare software malevolo:

1. **BIOS** — individua i dispositivi da cui caricare il boot loader e l'ordine di esame. Molti BIOS permettono di proteggere con **password** l'avvio o la modifica della configurazione.
2. **Boot Loader** — sceglie il SO e gli passa eventuali parametri; gestisce la *maintenance mode*. Protezione con password come per il BIOS.
3. **Sistema operativo** — carica i **device driver** (da non sottovalutare come superficie d'attacco) e avvia il processo **init**.
4. **init** — gestisce **runlevel** (o **target**, nel mondo systemd) per coordinare l'inizializzazione, cioè avviare i servizi nell'ordine corretto.

> **Domanda**: cosa sono di preciso "runlevel" e "target", e perché il PDF li mette insieme con "o"?
> **Risposta**: sono due modi — uno storico, uno moderno — di dire *in quale configurazione operativa* deve trovarsi il sistema una volta avviato. Un **runlevel** (sistemi SysV init classici) è un numero (0–6) che identifica uno stato: es. 0 = spento, 1 = single-user/maintenance, 3 = multi-utente testuale con rete, 5 = con interfaccia grafica, 6 = reboot. A ogni runlevel corrisponde un insieme di servizi da avviare/fermare. Nel mondo **systemd** (moderno, oggi standard) lo stesso concetto si chiama **target** (es. `multi-user.target`, `graphical.target`): stessa idea, meccanismo più flessibile. Il PDF scrive "runlevel *o* target" perché sono la stessa funzione (`init` decide *cosa* avviare e in *quale ordine*) espressa in due tecnologie diverse. È materia di dettaglio del modulo S9; qui basta sapere che è la fase 4, ed è dirottabile.

> **Domanda**: perché i device driver sono citati come "da non sottovalutare"?
> **Risposta**: perché un driver gira **in kernel space**, con i massimi privilegi. Un driver malevolo o manomesso, caricato in fase 3, ha controllo totale sulla macchina prima ancora che parta qualsiasi servizio o difesa applicativa. È un punto d'aggancio potente per un attaccante che sia riuscito a inserirvi codice: non deve scalare privilegi, li ha già per costruzione.

Nota: le fasi 3–4 (driver, `init`, runlevel/target) sono esattamente il territorio del modulo S9, qui guardato dall'ottica dell'attaccante.

### 6.1 Password al boot: pro e contro

- Se serve una password per l'avvio, il **funzionamento non supervisionato** diventa problematico: dopo un banale calo di alimentazione la macchina può restare ferma per ore in attesa che qualcuno digiti la password.
- In sistemi con gravi esigenze di sicurezza la password di boot **non sarà l'unica** da fornire, quindi tanto vale proteggere *tutti gli strati*.
- Almeno la **protezione contro i cambi di configurazione** è sempre consigliabile.

Principio cardine: **MAI affidarsi a un unico strato di protezione** (difesa in profondità). Le password del BIOS in particolare hanno **meccanismi semplici di reset** (spesso un jumper sulla scheda madre o togliere la batteria) e possono essere **indovinate**.

> **Domanda**: perché "MAI un unico strato" è dato come regola assoluta e non come semplice consiglio?
> **Risposta**: perché l'osservazione empirica è che **ogni singolo strato ha un modo noto di essere aggirato**. La password BIOS si resetta con un jumper; la password del bootloader si aggira con altri mezzi; e così via. Nessuno strato è invalicabile da solo. La difesa in profondità non nasce dall'idea che "più è meglio" in astratto, ma dal fatto concreto che l'attaccante che buca uno strato si trova comunque davanti al successivo: la password BIOS *da sola* è "teatro di sicurezza", ha senso **solo** come uno strato fra tanti.

### 6.2 Configurazione del bootloader a runtime: LILO e GRUB

Due bootloader storici Linux:

- **LILO** (the Linux Loader): usato fin dagli albori di Linux.
- **GRUB** (the Grand Unified Bootloader): più potente e flessibile, dotato di una **shell** per eseguire comandi e modificare al volo la procedura di avvio — potenza che abilita molti abusi.

Entrambi permettono di **passare parametri al kernel**. I due più critici per la sicurezza:

- **`single`**: avvia in modalità single-user/maintenance. Alcune distribuzioni hanno default rischiosi: se si innesca il *maintenance mode* si apre una **shell di root senza chiedere password**.
- **`init=…`**: sostituisce il comando lanciato dal kernel come primo processo (normalmente `/sbin/init`). La domanda retorica del PDF è il fulcro dell'attacco: **"E se fosse `/bin/bash`?"** — con `init=/bin/bash` il kernel avvia direttamente una shell di root al posto di init, dando controllo totale senza autenticazione.

> **Distinzione `single` vs `init=/bin/bash` (entrambe → shell di root, ma per vie diverse)**:
> - `single` sfrutta la **maintenance mode prevista dal sistema**: è una modalità legittima di manutenzione che *dovrebbe* chiedere la password di root, ma su alcune distro il default è debole e apre la shell senza chiederla.
> - `init=/bin/bash` **scavalca del tutto init**: dice al kernel di eseguire bash *come processo 1*, quindi non passa per nessuna procedura di login/manutenzione — non c'è proprio un punto dove venga chiesta una password.
> È il motivo per cui va protetto con password il **bootloader** (non solo il BIOS): senza quella protezione, chiunque al menu di GRUB può *aggiungere questi parametri a mano* e ottenere root. Concettualmente è un **privilege escalation da accesso fisico** — stessa posta in gioco del privesc di S11 (shell di root), vettore diverso (là da un accesso già ottenuto sul sistema; qui direttamente al boot).

### 6.3 Password del bootloader — sintassi (candidati diretti a domande d'esame)

**LILO**:

- `password=YourPasswordHere` — imposta una password richiesta al boot, **a meno che** non sia specificato…
- `restricted` — con `restricted` la password è richiesta **solo per modificare i parametri** durante il boot, non per il semplice avvio.
- **Global vs. single-entry** (la distinzione più insidiosa):
  - `password` e `restricted` nella *global section*: chiede la password prima di consentire l'aggiunta di parametri — attenzione alle entry non sicure.
  - `password` e `restricted` in una *image section*: come sopra ma **solo per l'immagine specificata**.
  - `password` nella *global section* e `restricted` in una *image section*: chiede la password per aggiungere parametri solo a quell'immagine, **ma chiede sempre la password per avviare le altre immagini**.

**GRUB**:

- `password [--md5] passwd [new-config-file]` — nella *global section* imposta la password per attivare l'**interactive operation** del bootloader (opzionalmente può innescare il caricamento di un file di configurazione alternativo); su un item del menu, la password serve per avviare *quell'item*.
- `lock` — messo subito dopo `title`, contrassegna quell'item come **password-protected**. Funziona **solo se esiste una direttiva `password` nella global section** (senza, `lock` non protegge nulla).
- `md5crypt` — comando al grub prompt per **calcolare l'hash della password** da usare con `--md5` (così la password non è in chiaro nel file di configurazione).

> **Domanda**: cos'è l'"interactive operation" del bootloader che `password` (global) protegge?
> **Risposta**: è la modalità in cui l'utente, davanti al menu di GRUB, può **intervenire manualmente** sull'avvio: editare la riga di comando di una voce, aggiungere parametri al kernel (es. proprio `single` o `init=/bin/bash`), o aprire la shell di GRUB per eseguire comandi. È precisamente la funzionalità *pericolosa* del §6.2. Proteggerla con `password` in global significa: "puoi vedere il menu e avviare le voci previste, ma non puoi metterti a *modificarle* senza la password". È lo strato che chiude il buco dell'`init=/bin/bash` inserito a mano.

> **Domanda**: perché `md5crypt` e `--md5`? Che c'entra MD5 qui?
> **Risposta**: serve a non scrivere la password **in chiaro** nel file di configurazione del bootloader (che è un file leggibile). Invece di `password segreta123`, si memorizza `password --md5 <hash>`, dove `<hash>` è il digest MD5 (calcolato con `md5crypt` al prompt) della password. Al boot, GRUB applica MD5 a ciò che l'utente digita e confronta con l'hash salvato: se coincidono, accesso concesso. Così chi legge il file di configurazione vede solo l'hash, non la password. (MD5 è oggi crittograficamente debole, ma il concetto — *hash invece di password in chiaro* — è quello che conta per l'esame.)

> **Distinzione GRUB `password` (global) vs `password` (per-item) vs `lock`** — la terna più chiedibile:
> - `password` in **global** → protegge l'accesso alla **modalità interattiva** (editing/shell del bootloader).
> - `password` su un **item** → protegge l'**avvio di quello specifico item**.
> - `lock` su un item → **marca l'item come protetto**, ma **dipende dalla password globale** per funzionare (da solo è inerte).
> Confondere questi tre è esattamente ciò che una scelta multipla vuole far sbagliare.

---

## 7. La sicurezza del processo di boot: la catena di fiducia

Posto che ogni fase è dirottabile, il problema di fondo: **come assicurarsi che ogni componente software eseguito sia autentico, integro e benevolo?** Il ragionamento va a ritroso, e ogni risposta sposta la fiducia più in basso:

- Gli **anti-malware** verificano le applicazioni. Ma **chi verifica gli anti-malware?**
- Il **sistema operativo** (idealmente rendendo l'anti-malware perfino inutile). Ma **chi verifica il SO?**
- Il **boot loader** potrebbe. Ma **chi verifica il boot loader?**
- Il **BIOS** potrebbe, specialmente se **assistito da hardware speciale** non modificabile dal SO, quindi immune da infezioni.

Questo hardware speciale, incorruttibile e alla base di tutto, è la **hardware root of trust**: la radice fidata da cui parte una **catena di fiducia** (*chain of trust*). Ogni anello verifica il successivo prima di cedergli il controllo; la radice è fidata *per costruzione* perché non modificabile via software.

> **Domanda**: perché la radice deve essere *hardware*? Non basterebbe un software particolarmente ben protetto?
> **Risposta**: no, ed è il punto teorico chiave. Qualsiasi verifica *puramente software* può, in linea di principio, essere **compromessa dallo stesso attaccante che compromette ciò che dovrebbe verificare**: se il malware ha modificato il SO, può aver modificato anche il software che avrebbe dovuto controllare il SO (è un regresso infinito, "chi verifica il verificatore?"). Serve un punto d'ancoraggio che l'attaccante software **non possa toccare** — e qualcosa di immodificabile via software può essere **solo hardware**. È lo stesso schema del §8 (Ken Thompson Hack): la fiducia va ancorata a qualcosa fuori dalla portata dell'attaccante.

### 7.1 Measured / Trusted / Secure Boot — tre termini da non confondere (trappola principale del modulo)

- **Measured Boot**: processo *generale* che tipicamente usa un **TPM** come hardware root of trust. **Misura** (calcola e registra l'hash di) ogni componente caricato. **NON definisce come *prevenire* un avvio malevolo**: si limita a *registrare* cosa è stato caricato, la decisione è demandata ad altri.
- **Trusted Boot**: usa gli strumenti del Measured Boot e in più **blocca il boot appena individua un componente non fidato**. Cioè: measured boot + capacità di *fermarsi*.
- **Secure Boot**: è il **nome specifico dell'implementazione di trusted boot basata su UEFI**. Implementazione software + chiavi nel firmware; richiede un BIOS standard per la fase di **POST**; può avvalersi del TPM per velocizzare e migliorare i controlli di integrità.

> **La distinzione chiave (misurare vs bloccare)**: Measured Boot *misura e basta* (registra hash, non impedisce nulla); Trusted Boot *misura e blocca*; Secure Boot è il nome di Trusted Boot **quando implementato su UEFI**. Domanda tipica: "Il Measured Boot impedisce l'avvio di un bootloader manomesso? → **Falso**: lo misura soltanto, la decisione è demandata (eventualmente a una remote attestation)."

> **Domanda**: cos'è la fase di POST che il Secure Boot "richiede a un BIOS standard"?
> **Risposta**: **POST** = *Power-On Self-Test*, la sequenza di autodiagnostica che il firmware esegue all'accensione *prima* di qualunque boot: verifica che CPU, RAM, dispositivi di base ci siano e funzionino. Il PDF nota che Secure Boot, pur essendo una funzione UEFI, ha comunque bisogno che questa fase di inizializzazione hardware di basso livello (storicamente il "BIOS") avvenga: prima si accende e si testa l'hardware (POST), poi UEFI/Secure Boot entra in gioco per verificare le firme dei componenti software da caricare.

### 7.2 Measured Boot in dettaglio: TPM, CRTM, PCR

Il **TPM** (*Trusted Platform Module*) è un chip con funzionalità crittografiche, parte delle specifiche del **Trusted Computing Group**. Il measured boot vi si basa tramite:

- **CRTM** (*Core Root of Trust for Measurement*): il primo pezzo di codice fidato, la radice da cui parte la misurazione.
- **PCR** (*Platform Configuration Registers*): registri che, **una volta scritti, sono fisicamente non modificabili** — si possono solo **estendere**, non riscrivere arbitrariamente.

Funzionamento (schema slide 14, CRTM → BIOS → Bootloader → OS, con frecce di *measuring*, *passing control* e *storing* verso i PCR): a ogni passaggio il componente corrente **misura** il successivo, **memorizza** l'hash nei PCR e poi gli **passa il controllo**. Si raccoglie così l'hash di ogni componente caricato.

Caratteristica importante: il measured boot **pospone i controlli** finché non dispone (a) delle chiavi crittografiche e (b) di abbastanza memoria per i calcoli. E soprattutto **si può decidere chi fa i controlli e quando** — anche *dall'esterno*, da un sistema fidato, per abilitare funzioni critiche: è il meccanismo della **remote attestation** (un verificatore remoto interroga i PCR e decide se la macchina è in uno stato fidato prima di concederle, per esempio, l'accesso a una risorsa).

> **Domanda**: cosa vuol dire che i PCR si possono "solo estendere, non riscrivere"? E perché è una proprietà di sicurezza?
> **Risposta**: "estendere" un PCR significa che il nuovo valore non *sostituisce* il vecchio, ma è calcolato come `nuovo = hash(vecchio || misura_del_componente)` — cioè ogni misura viene "concatenata e ri-hashata" sopra lo stato precedente. Conseguenza: il valore finale del PCR dipende da **tutta la sequenza** di componenti caricati *e dal loro ordine*. Perché è sicurezza: un attaccante che carica un componente malevolo **non può riportare il PCR a un valore "pulito"** — non c'è un'operazione di scrittura arbitraria, solo l'estensione, che è a senso unico. Quindi qualunque manomissione lascia una traccia indelebile nel valore del PCR, che la remote attestation poi rileva.

> **Domanda**: cosa significa concretamente "remote attestation"?
> **Risposta**: è la procedura con cui una macchina **prova a un terzo remoto di essere in uno stato integro**. In pratica: un verificatore esterno (es. il server che custodisce una risorsa critica) chiede alla macchina i valori dei suoi PCR, firmati dal TPM; li confronta con i valori "attesi" di una configurazione fidata nota; se coincidono, conclude che quella macchina ha avviato *esattamente* i componenti giusti (nessun bootloader/kernel manomesso) e le concede l'accesso. È l'"altra metà" del measured boot: il measured boot *registra* lo stato, la remote attestation lo *valuta da fuori*. È il motivo per cui measured boot può permettersi di non bloccare nulla localmente: la decisione la prende qualcun altro, dopo.

> **Perché "pospone i controlli" e perché conta**: proprio perché measured boot *registra* e non *blocca*, la valutazione può avvenire dopo (quando ci sono chiavi e memoria) e altrove (remote attestation). È l'opposto del secure boot UEFI, che verifica e blocca *sul momento*, componente per componente.

### 7.3 UEFI e Secure Boot

- **EFI** (nato in Intel) nasce come interfaccia più flessibile del BIOS fra SO e firmware; l'**UEFI Forum** ne standardizza e aggiorna la specifica.
- **UEFI è un "mini OS"**: milioni di righe di codice, standard per molte piattaforme — e proprio per questo un **bersaglio ideale degli attaccanti** (superficie enorme, *sotto* il sistema operativo).
- **UEFI verifica ogni componente software prima di passargli il controllo** (Bootloader/SO): richiede un **database di chiavi** e **blocca il boot appena rileva una difformità**.

> **Domanda**: perché essere un "mini OS di milioni di righe" rende UEFI un bersaglio ideale?
> **Risposta**: per due ragioni che si sommano. (1) **Dimensione = superficie d'attacco**: milioni di righe significano molte più possibilità di bug sfruttabili rispetto a un firmware minimale. (2) **Posizione = privilegio**: UEFI gira *prima e sotto* il sistema operativo, quindi un attaccante che lo compromette sta *sotto* ogni difesa dell'OS (antivirus, permessi, ecc.) e sopravvive persino a una reinstallazione del sistema (è nel firmware, non sul disco). Grande superficie + massimo privilegio + persistenza = bersaglio perfetto. Il PDF cita casi reali (TrickBot con capacità UEFI, minacce documentate da Kaspersky).

#### Le chiavi di UEFI Secure Boot

UEFI Secure Boot definisce **due processi di sicurezza**: (1) la **verifica dell'immagine di boot** e (2) la **verifica degli aggiornamenti al database** di sicurezza delle immagini. Usa più database e set di chiavi in una **gerarchia** dove le chiavi più in alto autorizzano quelle più in basso:

| Chiave | Verifica | Il suo aggiornamento è verificato da | Ruolo |
|---|---|---|---|
| **PK** | nuova PK, KEK, db/dbx/dbt/dbr, OsRecovery… | PK | **Platform Key** (la radice) |
| **KEK** | nuovi db/dbx/dbt/dbr, OsRecovery… | PK | **Key Exchange Key** |
| **db** | immagini UEFI | PK/KEK | **Authorized** Image Database (i "consentiti") |
| **dbx** | immagini UEFI | PK/KEK | **Forbidden** Image Database (i "vietati/revocati") |
| **dbt** | immagine UEFI + dbx | PK/KEK | Timestamp Database |
| **dbr** | OsRecovery | PK/KEK | Recovery Database |

> **Distinzione db vs dbx (coppia molto chiedibile)**: **db** è la lista *bianca* (immagini autorizzate); **dbx** è la lista *nera* (immagini proibite/revocate — es. un bootloader di cui è emersa una vulnerabilità). Sono complementari: un'immagine passa se è in **db** *e* **non** è in **dbx**. La **PK** è la radice che autorizza tutto il resto; la **KEK** sta in mezzo e autorizza gli aggiornamenti a db/dbx.

> **Domanda**: qual è la logica della gerarchia PK → KEK → db/dbx? Perché tre livelli e non uno?
> **Risposta**: è una separazione di ruoli per limitare i danni e distribuire il controllo. La **PK** (Platform Key) è la radice unica: chi la possiede controlla la piattaforma (tipicamente il produttore hardware/proprietario), e serve solo per autorizzare le KEK e la propria sostituzione — la si usa raramente. Le **KEK** (Key Exchange Keys) sono il livello intermedio "operativo": autorizzano gli aggiornamenti alle liste db/dbx (tipicamente ne esiste una di Microsoft e/o del proprietario). **db/dbx** sono le liste effettive contro cui si verificano le immagini al boot. Il vantaggio: aggiornare la lista dei bootloader consentiti/revocati (operazione frequente) richiede una KEK, non la preziosissima PK; e revocare una KEK compromessa non obbliga a rifare tutto dalla radice. È lo stesso principio della PKI: poche chiavi radice preziose, molte chiavi operative sotto.

#### UEFI Secure Boot Image Verification (il modello Clark-Wilson)

La slide 17 descrive le entità della verifica delle immagini al boot con vocabolario formale:

- **TP** = *Trusted Platform*: la procedura di verifica stessa.
- **CDI** = *Constrained Data Item*, cioè il **UEFI Secure Boot Image Security Database**: il **database delle politiche di sicurezza** da applicare alle immagini da caricare. È **aggiornabile**.
- **UDI** = *Unconstrained Data Item*: qualsiasi firmware di terze parti, incluso **boot loader, PCI option ROM, o UEFI shell tool**.

Meccanismo: **al boot, TP verifica l'integrità di UDI usando le policy CDI**; se il controllo passa, **UDI entra a far parte di CDI** e il firmware di terze parti viene eseguito. Poiché il CDI è aggiornabile, un fornitore che voglia far accettare il proprio componente deve **firmarlo con la propria chiave privata e rendere disponibile la chiave pubblica**; questa **chiave pubblica va iscritta (*enrolled*) nel firmware**. Garanzia cruciale: **normalmente questo passaggio richiede un reboot in una modalità speciale e l'intervento sulla console**, bloccando l'azione di utenti malevoli **privi di accesso fisico**.

> **Domanda**: cos'è una "PCI option ROM" citata come esempio di UDI?
> **Risposta**: è il firmware che sta a bordo di una **scheda di espansione PCI/PCIe** (schede video, controller di rete/RAID, ecc.) e che viene eseguito all'avvio per inizializzare quella scheda prima che parta il SO. È rilevante per la sicurezza perché è **codice di terze parti che gira in fase di boot con alti privilegi**: se non fosse verificato, una scheda con option ROM malevola potrebbe iniettare codice nella catena di avvio. Ecco perché rientra fra gli **UDI** (firmware non fidato *finché non verificato*) che Secure Boot deve validare prima di eseguire.

> **Domanda**: il modello Clark-Wilson va saputo a fondo?
> **Risposta**: no — la lezione stessa lo dice. È un **modello formale di integrità** in cui procedure fidate (**TP**) trasformano dati non vincolati/non fidati (**UDI**) in dati vincolati/fidati (**CDI**) *solo dopo verifica*. Per l'esame basta capire il **movimento**: un componente esterno (UDI) diventa fidato (entra nel CDI) **solo dopo** che una procedura fidata (TP) lo ha validato con una policy; e l'iscrizione di nuove chiavi richiede **presenza fisica alla console**, non è automatizzabile da remoto. Il nome "Clark-Wilson" serve a inquadrarlo, non a essere ripetuto nel dettaglio.

#### UEFI Secure Boot in Linux: shim e MOK

Sulla catena Linux (schema slide 18: PK → KEK/db → **Shim** ↔ **MOK List** → GRUB2 → Kernel):

1. La **Platform Key ufficiale verifica un piccolo pre-boot-loader, `shim`**. La chiave che firma `shim` deve essere fornita dal costruttore hardware — **in pratica è una chiave Microsoft** (è Microsoft a firmare `shim`, perché la sua chiave è quella preinstallata su quasi tutto l'hardware consumer).
2. **`shim` può usare o trasferire le MOK** (*Machine Owner Keys*): per validare il bootloader e per validare **moduli custom del kernel**.
3. I **componenti aggiuntivi del kernel devono essere firmati** per essere caricati:
   - l'utente **genera le MOK**;
   - l'utente **deposita le MOK in shim**;
   - **al boot successivo, shim trova le chiavi in fase di setup e chiede conferma per salvarle in firmware** → il **consenso esplicito e basato su password è sempre richiesto**.

> **Domanda**: perché esiste `shim`? Non basterebbe che Microsoft firmasse direttamente il bootloader/kernel Linux?
> **Risposta**: `shim` risolve un problema pratico di scala. L'hardware si fida per default solo di chiavi **Microsoft** (la PK preinstallata). Ma le distribuzioni Linux sono tantissime e aggiornano kernel e bootloader di continuo: sarebbe impraticabile far firmare da Microsoft *ogni* kernel di *ogni* distro a *ogni* aggiornamento. La soluzione: Microsoft firma **una sola volta** un piccolo componente stabile e raramente modificato, `shim`; `shim` è fidato dall'hardware, e a sua volta gestisce le **MOK** (Machine Owner Keys) del proprietario della macchina. Così la fiducia si "trasferisce" un gradino più in basso in modo gestibile: la distro (o l'utente) firma i propri kernel/moduli con le proprie MOK, e `shim` li accetta — **senza dover disabilitare Secure Boot**.

> **Domanda**: cos'è concretamente una MOK e chi la controlla?
> **Risposta**: una **MOK** (*Machine Owner Key*) è una chiave che appartiene al **proprietario della macchina** (non a Microsoft, non alla distro): serve a far accettare da `shim` componenti firmati da lui. Il punto di forza di sicurezza è *come* la si iscrive: l'utente la genera e la deposita, ma al reboot successivo `shim` entra in una schermata di setup e **chiede conferma esplicita alla console, con password**, prima di salvarla in firmware. Questo garantisce che **solo chi ha accesso fisico alla console** possa aggiungere chiavi fidate — **mai da remoto, mai in automatico**. È la stessa garanzia del modello Clark-Wilson (§7.3): l'iscrizione di fiducia richiede presenza fisica.

> **Nota pratica ricorrente (esempio concreto del meccanismo)**: chi ha Secure Boot attivo e installa VirtualBox su Linux incontra proprio questo — il modulo `vboxdrv` non si carica finché non lo si firma con una MOK e la si iscrive rispondendo al prompt di `shim` al reboot.

Connessione con S14/S15 (crittografia e gestione chiavi con `gpg`): l'intera catena poggia su **firma digitale** (chiave privata firma / chiave pubblica verifica) — la stessa primitiva che S15 esercita con `gpg`, qui applicata al boot.

---

## 8. Integrità e autenticità del software applicativo

Il **secure boot garantisce l'integrità fino all'avvio del SO** — ma non oltre. I **pacchetti software applicativi** sono meno "potenti" (girano senza privilegi di boot) ma **non necessariamente meno pericolosi**. Da qui il problema di verificare la provenienza del software installato *dopo* l'avvio.

### 8.1 Autenticazione del software scaricato

**Prima cautela** quando si scarica software: **verificarne l'autenticità da una firma digitale**. Ma per verificare una firma serve una **chiave pubblica fidata** — il che sposta il problema (da dove viene la fiducia in quella chiave?). Procedura tipica con GPG:

1. `gpg --verify FILE.asc FILE.tar.gz` — mostra il *key id* con cui è stato firmato.
2. `gpg --keyserver pgpkeys.mit.edu --recv-key <KEY_ID>` — scarica quella chiave. Ma **l'autenticità della chiave, così, deriva solo dalla fonte… basta?** Va valutato caso per caso, seguendo indicazioni specifiche del progetto.
3. Si ripete il passo (1) ora che si ha la chiave.

Come minimo dovrebbe essere disponibile un **fingerprint** (es. in formato `.sha256`): si mette nella stessa directory del file e si lancia `sha256 -c FILE.sha256`.

> **Distinzione firma vs fingerprint/hash (garanzie diverse!)**:
> - La **firma digitale** (`gpg --verify`) prova **autenticità + integrità**: *chi* l'ha prodotto **e** che non è stato alterato. Ma richiede fiducia in una chiave pubblica.
> - Il **fingerprint/hash** (`sha256`) prova **solo integrità**: che il file non è cambiato rispetto a quello di cui il produttore ha pubblicato l'hash. **Non dice nulla su chi l'ha prodotto**, a meno che tu non ti fidi già del canale da cui hai preso l'hash.
> Attenzione al tranello del vero/falso (è la domanda 8 dell'autoverifica, e la formulazione è *invertita* apposta): "`gpg --verify` dà solo integrità, l'hash dà anche autenticità" → **Falso**, è esattamente il contrario.

### 8.2 Installazione da sorgenti: la trappola della fiducia

Installare da sorgenti *offre la possibilità teorica di verificare il codice*. Ma:

- **se non lo fai davvero, è un falso senso di sicurezza**;
- se ti limiti a fidarti della firma sull'archivio, **non è diverso dal verificare la firma su un binario** (nessun guadagno di sicurezza);
- è **più difficile da manutenere**;
- richiede **MOLTI componenti ausiliari** (header, librerie, processori di macro, compilatori, linker…) e **ognuno può avvantaggiare un attaccante**. Riferimento classico: il **Ken Thompson Hack** — un compilatore compromesso può inserire backdoor nei binari che compila (e persino in una nuova versione di sé stesso), rendendo inutile ispezionare il *sorgente* perché il male sta nel *toolchain*.

Da qui l'ingresso di **distribuzioni e pacchetti** come soluzione pragmatica:

- **chiavi di verifica installate una volta per tutte** — comodo, ma diventa un **Single Point Of Failure (SPOF)**: se quella chiave è compromessa, cade tutto;
- **gestione automatica delle dipendenze**;
- **garanzia di compatibilità binaria** fra tutti gli elementi del set.

> **Domanda**: cos'è il "Ken Thompson Hack" e perché è citato proprio qui?
> **Risposta**: è un celebre argomento di Ken Thompson (Reflections on Trusting Trust). Idea: immagina un **compilatore compromesso** che, quando compila il programma di `login`, ci inserisce di nascosto una backdoor; e che, quando compila *sé stesso* (un nuovo compilatore), reinserisce di nascosto entrambi i comportamenti malevoli. Risultato: la backdoor **non compare in nessun sorgente** — né in quello di `login`, né in quello del compilatore — eppure è presente in ogni binario. Ispezionare il codice sorgente non serve a niente, perché il male vive nel **toolchain** (compilatore, linker, librerie), non nel testo che leggi. È citato qui per demolire l'illusione "installo da sorgenti così controllo tutto": non è vero, a meno che tu non controlli *anche* ogni strumento che li trasforma in eseguibile — un regresso di fiducia analogo a quello del boot (§7). La soluzione, come per il boot, è **spostare la fiducia su un punto gestito centralmente** (la distribuzione), accettandone il limite (lo **SPOF** della chiave).

> **Domanda**: cos'è uno SPOF, in una parola?
> **Risposta**: **Single Point Of Failure** = un unico elemento il cui cedimento fa cadere *tutto il sistema*. Qui la chiave di verifica della distribuzione è comodissima (la installi una volta e verifica tutti i pacchetti), ma proprio perché è *una sola* e *vale per tutto*, se viene compromessa l'intero meccanismo di fiducia crolla. Comodità e SPOF sono due facce della stessa scelta di centralizzazione.

### 8.3 Installazione assistita e package manager

L'installazione è di norma effettuata tramite **software ausiliari**: il **package manager** della distribuzione (rpm/yum, dpkg/apt…) o un installer su Windows. Un tool di installazione: **può farsi carico delle verifiche sulle dipendenze**; **non può configurare ogni dettaglio del sistema** in modo specifico; **può generare dinamicamente dati specifici**.

Le dipendenze formano un **grafo** (es. `glibc` serve a `gtk`, `firefox`, `zlib`…; `zlib` serve ad `apache`; `apache` serve a `php`). "A → B" = "A serve per B", dove *servire* può essere **logico** (non ha senso un linguaggio di generazione pagine web senza un web server) o **fisico** (un binario linkato dinamicamente non gira senza le librerie di cui importa i simboli).

> **Domanda**: che differenza c'è fra dipendenza "logica" e "fisica" nel grafo?
> **Risposta**: **fisica** = tecnicamente il programma *non parte* senza l'altro componente: un eseguibile linkato dinamicamente cerca a runtime le librerie condivise (`.so`) di cui usa i simboli, e se mancano non gira affatto. È una necessità di esecuzione, verificabile meccanicamente (ldd, i simboli importati). **Logica** = non è che il programma non si avvii, ma *non avrebbe senso funzionale* senza l'altro: installare PHP (linguaggio per generare pagine web) senza un web server è tecnicamente possibile ma inutile allo scopo. Il package manager modella entrambe nel grafo per installare automaticamente ciò che serve.

### 8.4 Debian e Red Hat: pacchetti e repository

Le due **distribuzioni capostipite** da cui derivano quasi tutte le varianti, con sistemi di gestione pacchetti molto simili, su tre livelli: tool **di basso livello** (singolo pacchetto), tool **intermedi** (pacchetti + dipendenze), tool per il **reperimento automatico dai repository**.

**Anatomia del nome del pacchetto** (candidato a domanda):

- Debian/derivate (.deb): `aptitude-0.2.15.9-2_i386.deb` → **nome** (`aptitude`) · **versione del software** (`0.2.15.9`) · **versione del pacchetto** (`2`) · **architettura** (`i386`).
- RedHat/derivate (.rpm): `httpd-2.4.6-45.el7.centos.x86_64.rpm` → nome · versione software · versione pacchetto · architettura.

> **Distinzione "versione del software" vs "versione del pacchetto"**: la **versione del software** è quella del programma *a monte* (upstream), decisa dagli sviluppatori originali (es. Apache 2.4.6). La **versione del pacchetto** incrementa quando cambia il *packaging* — patch della distribuzione, correzioni allo script di installazione, ricompilazione — **a parità di software** (es. lo stesso 2.4.6 impacchettato meglio: `-45`). Due numeri diversi che rispondono a "quale programma" e "quale confezione di quel programma".

**Repository**: raccolte indicizzate di pacchetti, online o su filesystem locale. I package manager leggono per ogni repo **indice e metadati**, così conoscono versioni disponibili e dipendenze (e come risolverle). Collocazioni tipiche:

- APT: `/etc/apt/sources.list` e `/etc/apt/sources.list.d/*` — es. `deb http://archive.ubuntu.com/ubuntu bionic-updates universe`.
- YUM: `/etc/yum.conf` e `/etc/yum.repos.d/*.repo` — con direttive come `gpgcheck=1` e `gpgkey=file:///etc/pki/rpm-gpg/RPM-GPG-KEY-CentOS-7`.

### 8.5 Verifica dell'autenticità dei pacchetti

La **firma dei pacchetti è gestita centralmente**: i *maintainer* della distribuzione forniscono le chiavi di verifica nei media di installazione ufficiali o sui repository online. I set di chiavi si possono gestire in modo standard con **GnuPG** (es. i sistemi .deb mettono i keyring in `/etc/apt/trusted.gpg.d/`), ma è **più comune usare gli strumenti della distribuzione**:

- .deb: `apt-key {add file | list | del keyid | adv --recv-key keyid | …}` — **deprecato da tempo ma ancora in uso**; metteva tutte le chiavi nello stesso file `/etc/apt/trusted.gpg`.
- .rpm: `rpm {--import | -e | -q[ai] | …}` — **rpm tratta le chiavi come se fossero pacchetti**, quindi si usano gli stessi comandi per interrogarle, eliminarle, ecc.

> **Domanda**: perché `apt-key` è deprecato? Cosa c'era di sbagliato nel mettere tutte le chiavi in `/etc/apt/trusted.gpg`?
> **Risposta**: è deprecato proprio perché **metteva tutte le chiavi in un unico contenitore "fidato per tutto"**, che è la radice del problema di *cross-signing* del §8.7: una chiave importata per un singolo repo minore finiva per essere valida per convalidare *qualunque* pacchetto del sistema. La sostituzione moderna (`signed-by`, file `.sources`) lega ogni chiave al *suo* repo. Quindi `apt-key` non è deprecato per un difetto tecnico banale, ma per un **difetto di modello di sicurezza** (scope delle chiavi troppo ampio).

### 8.6 Repository esterni: il rischio dell'autenticazione disattivata

Esigenza comune: installare software ben supportato ma **non incluso nei canali ufficiali**. Si aggiunge il repo all'elenco — ma **non tutti supportano l'autenticazione**, e la si disattiva:

- APT: `deb [allow-insecure=yes] http://good.site/virtualbox/debian bookworm contrib`
- YUM: nel `.repo`, `gpgcheck=0`.

> **Threat model dell'`allow-insecure`/`gpgcheck=0`**: disattivare la verifica della firma = installare pacchetti la cui autenticità **non è provata**. È comodo (funziona subito) ma apre alla sostituzione malevola dei pacchetti (mirror compromesso, man-in-the-middle sul mirror). È l'equivalente, per il software, di avviare un SO non firmato: si è rinunciato alla catena di fiducia.

### 8.7 Cross-signing threat: la minaccia sottile dei keyring condivisi

Nelle distro .deb era diffuso l'uso di righe di configurazione **prive di specifica della chiave**: `deb http://download.virtualbox.org/virtualbox/debian xenial contrib`. In questo caso vengono usate **tutte le chiavi in posti "fidati"** (`/etc/apt/trusted.gpg` e `/etc/apt/trusted.gpg.d/*`). Conseguenza: **una chiave importata per convalidare *una* fonte può convalidarle *tutte*** → **cross signing**. Se un repo viene violato e la sua chiave privata sottratta, quella chiave può **pubblicare aggiornamenti fraudolenti per qualsiasi pacchetto, anche degli altri**.

**Best practice**: legare ogni fonte alla *sua* chiave.

- Sulla singola riga: `deb [arch=amd64 signed-by=/usr/share/keyrings/oracle-virtualbox-2016.gpg] https://download.virtualbox.org/virtualbox/debian bookworm contrib`.
- File `.sources` in stile "rpm-like" con campo `Signed-By: /usr/share/keyrings/ubuntu-archive-keyring.gpg`.

> **Distinzione cross-signing vs `allow-insecure`/`gpgcheck=0` (due debolezze diverse!)**:
> - `allow-insecure`/`gpgcheck=0` = **nessuna verifica** (si è spenta la firma del tutto).
> - Cross-signing = **c'è verifica, ma con lo scope sbagliato**: la chiave giusta per un repo minore diventa valida per *l'intero sistema*.
> `signed-by`/`Signed-By:` risolve il *secondo* problema restringendo *quale* chiave è accettata *per quale* fonte. Non confondere "verifica assente" con "verifica dallo scope troppo largo": è una coppia di vero/falso classica.

### 8.8 Provenienza dei pacchetti: software injection

Confusione possibile se un pacchetto con lo **stesso nome** esiste in **versioni diverse in repository differenti**. I package manager, di default, **scelgono sempre la versione più avanzata**. Scenario d'attacco: hai aggiunto un repo semisconosciuto per un'app innocua; se a quel repo viene aggiunto un pacchetto **"core"** dichiarato più recente della versione ufficiale → **software injection** (il sistema aggiorna un componente critico prelevandolo dal repo malevolo). A volte anche aggiornamenti nello stesso repo sono indesiderati (situazioni legacy). Va **controllata e gestita**:

- Provenienza di un pacchetto: YUM `repoquery -i [package name]`; APT `apt-cache showpkg [package name]`.
- Elenco pacchetti da un repo: YUM `yum list installed | grep [repo name]`; APT: vari comandi sulla cache.

### 8.9 Limitare le modifiche automatiche: version locking/pinning

Per prevenire problemi in sistemi con dipendenze complesse (mix di pacchetti installati a mano e via package manager) si usa il **version locking/pinning**:

- APT: editare `/etc/apt/preferences.d/*` (Apt Preferences/pinning).
- YUM: `yum install yum-plugin-versionlock`, poi `yum versionlock [package name]` (o editare `/etc/yum/pluginconf.d/versionlock.list`).

> **Perché il pinning è anche sicurezza, non solo stabilità**: bloccare la versione di un pacchetto critico impedisce che un repo dichiari una versione "più recente" e me la faccia installare al posto di quella fidata — cioè è una **difesa diretta contro la software injection (§8.8)**, oltre che una tutela contro aggiornamenti che romperebbero le dipendenze.

### 8.10 DevOps woes: dependency confusion

**DevOps** (development + operations) automatizza build e deployment, inclusa **l'inclusione automatica delle dipendenze**. Problema: **raramente c'è una gestione corretta dei namespace** — es. `npm` (Node) è praticamente *flat* (piatto, senza namespace robusti). Scenario (**dependency confusion**): un'azienda sviluppa internamente un pacchetto `myutils`; un attaccante registra un pacchetto `myutils` nel repo pubblico di default; al prossimo build, **quale prende il sistema di CI/CD?** Se prende quello pubblico (magari con numero di versione più alto), esegue codice dell'attaccante nella pipeline.

> **Domanda**: cos'è un "namespace" e perché "npm è flat" abilita l'attacco?
> **Risposta**: un **namespace** è uno spazio di nomi che *qualifica* un identificatore per evitare collisioni — come un cognome che distingue due persone con lo stesso nome, o un dominio (`azienda.myutils` ≠ `pubblico.myutils`). Se il repo di pacchetti fosse *namespaced*, il pacchetto interno `azienda/myutils` e quello pubblico `myutils` sarebbero **nomi diversi** e non potrebbero confondersi. Ma se il repo è **flat** (piatto), esiste un solo spazio globale di nomi: `myutils` è `myutils` e basta, chiunque l'abbia pubblicato. L'attaccante sfrutta proprio questo registrando pubblicamente lo *stesso nome* del pacchetto interno: il tool di build, dovendo scegliere fra due `myutils` omonimi, può prendere quello sbagliato (spesso quello con versione più alta, sul repo pubblico). La radice del problema è la **mancanza di un namespace** che separi "mio interno" da "pubblico omonimo".

> **Connessione con §8.8**: dependency confusion **è** software injection portata nei package manager di *linguaggio* (npm, pip…). Stessa logica ("il sistema sceglie versione/fonte sbagliata per omonimia"), contesto diverso (build automatizzati vs aggiornamenti di sistema). Radice comune: **assenza di namespace**. Nell'autoverifica (domanda 19) la risposta è proprio "software injection da repository".

---

## 9. Cloud security

Nel cloud, **a seconda del livello di servizio, molti problemi "svaniscono"** (delegati al provider). I livelli, dal più basso al più alto (schema slide 33):

- **Hardware** (server fisici) — sotto tutto.
- **IaaS** (Infrastructure as a Service): Computer, Network, Storage — es. EC2, S3, VPC.
- **PaaS** (Platform as a Service): Components, Services — es. runtime Java/Node/Ruby, Lambda, API Gateway.
- **SaaS** (Software as a Service): User Interface, Machine Interface — es. G Suite, applicazioni web pronte.

> **Distinzione IaaS / PaaS / SaaS e responsabilità condivisa (domanda tipica)**: più si sale (IaaS → PaaS → SaaS), più responsabilità *e controllo* si cedono al provider. In **IaaS** gestisco ancora il **sistema operativo** della VM (e la sua sicurezza: patching, hardening); in **PaaS** uso una piattaforma/runtime pronto e mi occupo solo del mio codice/configurazione; in **SaaS** uso solo l'applicazione e **quasi tutta la sicurezza è del provider**. È il modello della **responsabilità condivisa**: chi è responsabile di cosa dipende dal livello. Vero/falso classico (domanda 12): "In SaaS il cliente (CSC) è responsabile del patching del SO sottostante?" → **Falso**, a quel livello lo gestisce il provider. (Occhio: in *IaaS* invece sarebbe **Vero**.)

### 9.1 Sicurezza: cloud vs. on-premise

- I problemi di sicurezza del cloud riguardano **raramente** host e rete (se ne occupa il provider).
- C'è un **impatto "emotivo" della distanza**: la **perdita di controllo**.
- **Osservazione razionale**: i fornitori cloud hanno spesso **team di sicurezza di livello mondiale** che quasi nessuna azienda potrebbe permettersi per i propri data center.
- La **due diligence** suggerisce di **verificarlo** quando si sceglie un fornitore: **certificazione ISO27001** (con il suo *ambito di applicazione*) e risultati di un **audit SAS70 di tipo II**.
- Paradossalmente, **alcune minacce reali riguardano la disponibilità**: **lock-in**, **dipendenza dalla rete**, **cessazione dell'attività** del fornitore.

> **Domanda**: cosa sono ISO27001 e SAS70 di tipo II, e perché sono citate?
> **Risposta**: sono due strumenti per *verificare oggettivamente* le affermazioni di sicurezza di un fornitore (la "due diligence" che non ci si può fidare sulla parola). **ISO27001** è uno standard internazionale che certifica che un'organizzazione gestisce la sicurezza delle informazioni secondo un sistema di gestione formale (ISMS); il PDF insiste sull'**ambito di applicazione** (vedi sotto). **SAS70 di tipo II** è un vecchio standard di *audit* (oggi sostituito da SSAE/ISAE, ma citato dal PDF) in cui un revisore indipendente valuta i controlli di un fornitore di servizi: il "tipo II" significa che il revisore non guarda solo se i controlli *esistono sulla carta* (tipo I), ma che ne verifica l'**efficacia operativa su un periodo di tempo**. Insieme dicono: non fidarti del marketing, chiedi certificazioni e audit indipendenti.

> **Perché la certificazione va letta con l'"ambito di applicazione"**: una ISO27001 certifica che *un certo perimetro* è gestito secondo lo standard — ma se il servizio che uso è *fuori* da quel perimetro, la certificazione **non mi copre**. Errore da manuale: fidarsi del "bollino" senza guardare *cosa esattamente* certifica.

### 9.2 Benefici potenziali del cloud per la sicurezza

Le misure di sicurezza sono **più economiche su scala ampia**:

- **Collocazioni multiple** = ridondanza di istanze e dati = indipendenza dai guasti (anche dolosi) e possibilità di ripristino.
- **Tempestività migliorata** nella risposta agli incidenti.
- **Gestione delle minacce** con specialisti dedicati.
- **Sicurezza come differenziatore di mercato**: il **CSC** (cliente) sceglie in base alla reputazione di riservatezza/integrità/resilienza del **CSP** (provider) → forte motore per i CSP a migliorare.
- **Aggiornamenti più tempestivi**: immagini di VM pre-rafforzate e aggiornate centralmente; IaaS che consente snapshot regolari e deploy rapido su piattaforme omogenee.
- **Concentrazione delle risorse e ridimensionamento rapido**: applicare controlli e policy in modo economico; il CSP può **scalare dinamicamente** i meccanismi difensivi (traffic shaping, filtraggio, crittografia) durante un attacco.
- **Sicurezza come servizio e raccolta di prove**: interfacce standardizzate di sicurezza gestita; IaaS che clona VM e offre storage per i log utile ad **analisi forensi offline** senza degradare le prestazioni.
- **SLA che impongono migliore gestione del rischio**: per quantificare le sanzioni negli SLA, i CSP adottano audit interni e valutazioni del rischio più rigorosi.

> **Definizioni CSC e CSP (da tenere dritte, molte domande ci giocano)**: **CSC** = *Cloud Service Customer*, il **cliente** che compra/usa il servizio. **CSP** = *Cloud Service Provider*, il **fornitore** che lo eroga. Trucco mnemonico: **C**ustomer = **C**ompra; **P**rovider = **P**roduce/fornisce.

> **Domanda**: cos'è uno SLA e perché "impone una migliore gestione del rischio"?
> **Risposta**: uno **SLA** (*Service Level Agreement*) è il contratto che fissa i **livelli di servizio garantiti** (es. uptime del 99,9%, tempi di risposta) e le **penali** se non vengono rispettati. L'effetto virtuoso: per non pagare le sanzioni, il CSP è **costretto a misurare e gestire seriamente il proprio rischio** (audit interni, valutazioni rigorose, azioni correttive). In pratica il vincolo contrattuale *scarica a monte* disciplina sulla sicurezza: la penale monetaria è l'incentivo che rende la buona gestione del rischio conveniente per il fornitore.

### 9.3 Attori e minacce nel cloud

Attorno alla "nuvola" gravitano molti attori, ciascuno una potenziale minaccia: Government, Identity provider, Attribute provider, Image/application publisher, Cloud provider, Transport agent, Hacker/cracker, Competitor, Cloud broker, Consumer. Messaggio: la **superficie di fiducia nel cloud è molto più affollata** che on-premise — ci si fida (volenti o nolenti) di parecchi terzi.

### 9.4 I rischi specifici del cloud: tre categorie (cuore "da quiz")

**A) Rischi Organizzativi**
- **Perdita di controllo** — *forse il rischio considerato più grave*: il CSC cede il controllo al CSP su molti aspetti critici; se lo SLA lascia un *gap* rispetto alle necessità, non c'è modo di chiuderlo; outsourcing/subcontracting possono introdurre attori non fidati; il CSC non può verificare autonomamente la compliance del CSP.
- **Lock-in** — aspetti proprietari rendono difficile la migrazione (esiste anche on-premise, ma lì almeno i dati restano in mano al CSC).
- **Supply Chain Failure** — l'outsourcing crea catene di fornitura *forti quanto l'anello più debole*.
- **Interferenze tra politiche di sicurezza CSC-CSP** — il CSC potrebbe volere controlli in conflitto con l'ambiente del CSP (non implementabili); le insicurezze di *un* CSC possono diventare vulnerabilità dell'intera piattaforma condivisa.

**B) Rischi Tecnici**
- **Economic Denial of Service (EDoS)** — con servizi *pay-per-use* che scalano automaticamente, un attacco di sovraccarico, **invece di degradare le prestazioni, aumenta i costi**. È il "DoS economico".
- **Vulnerabilità della piattaforma** — un attacco all'infrastruttura potrebbe dare accesso a *tutte* le VM (molto improbabile ma devastante); più plausibile la **compromissione dell'interfaccia di gestione**.
- **Cedimento dell'isolamento** — la **multi-tenancy** permette teoricamente di installare una VM malevola *accanto* a quella della vittima: possibili **attacchi cross-VM via side channel**, forzatura di migrazioni saturando l'host, **intercettazione dei dati in transito** (non tanto quelli dell'utente — che deve cautelarsi cifrando **end-to-end** — quanto le operazioni trasparenti del CSP: sincronizzazioni, migrazioni; raramente il CSP dà garanzie su questi aspetti).

**C) Rischi Legali**
- **Protezione dei dati** — legislazioni differenti; potrebbe essere **illegale trasferire certi dati in certi paesi**; il CSP potrebbe spostare i dati tra i propri datacenter **senza dirlo al CSC**.
- **Giurisdizione** — il CSP potrebbe essere costretto ad azioni dagli organi giudiziari in base alle leggi del paese della sede legale o dei datacenter; il CSC potrebbe subire interruzioni o **sequestro di dati per motivi che non sussistono nel proprio paese**.

> **Domanda**: cos'è di preciso un "pay-per-use che scala automaticamente" e perché rende possibile l'EDoS?
> **Risposta**: è il modello economico tipico del cloud: **paghi in proporzione a quanto consumi** (ore-CPU, GB trasferiti, richieste servite) e l'infrastruttura **aggiunge risorse in automatico** (auto-scaling) quando il carico cresce, per non degradare il servizio. On-premise, un attacco di sovraccarico satura le tue risorse *fisse* e il servizio rallenta/cade (DoS classico). Nel cloud auto-scaling accade l'opposto: il sistema **regge il carico aggiungendo risorse** — ma quelle risorse **le paghi tu**. Quindi l'attaccante non ti nega il servizio, ti **gonfia la bolletta** fino a costringerti a spegnere per motivi economici. Da qui il nome **EDoS** (Economic Denial of Service).

> **Domanda**: cos'è un "side channel" e come permette un attacco cross-VM?
> **Risposta**: un **side channel** (canale laterale) è una via di fuga di informazione **non prevista dal progetto**, che non passa dai dati "ufficiali" ma da *effetti collaterali fisici/misurabili* dell'elaborazione: tempi di esecuzione, consumo della cache della CPU, consumo energetico, ecc. In multi-tenancy, la VM dell'attaccante e quella della vittima **condividono lo stesso hardware fisico** (stessa CPU, stessa cache). L'attaccante, misurando con precisione *come le proprie operazioni vengono rallentate o accelerate* dall'attività della vittima sulla cache condivisa, può **dedurre informazioni segrete** (in casi noti, persino chiavi crittografiche) **senza mai accedere direttamente** alla memoria della vittima. È il "cedimento dell'isolamento": l'hypervisor isola *la memoria*, ma non riesce a isolare perfettamente gli *effetti fisici condivisi* dell'hardware.

> **Distinzioni da non confondere nei rischi cloud (fonte tipica di scelta multipla)**:
> - **EDoS vs DoS classico**: il DoS classico *nega il servizio* (lo fa cadere); l'EDoS *mantiene il servizio* ma **fa esplodere il conto** sfruttando l'auto-scaling pay-per-use. Vero/falso 10: "EDoS riduce la disponibilità negandola del tutto" → **Falso**.
> - **Lock-in (organizzativo) vs cedimento dell'isolamento (tecnico)**: il primo è *dipendenza contrattuale/proprietaria* (difficile andarsene); il secondo è *tecnico* di multi-tenancy (il vicino di rack ti attacca). **Categorie diverse** (attenzione all'accoppiamento sbagliato "lock-in → tecnico", che è la risposta-trappola della domanda 18).
> - **Cedimento dell'isolamento vs vulnerabilità della piattaforma**: il primo è "il tenant accanto rompe l'isolamento fra VM"; il secondo è "l'infrastruttura stessa / l'interfaccia di gestione è bucata". Il secondo è più raro ma colpisce *tutti* i tenant.
> - **Rischi legali** = *dove* stanno i dati e *quali leggi* si applicano; sono l'altra faccia della **delocalizzazione** del §1.

> **Domanda**: la classificazione dei tre rischi lasciati con "….." nella slide 40 va completata a memoria?
> **Risposta**: no, il PDF li lascia aperti apposta (gli elenchi non sono esaustivi). Ciò che serve sapere con certezza per un quiz è: (1) le **tre categorie** — Organizzativi, Tecnici, Legali; (2) il **rischio-simbolo di ciascuna** — Perdita di controllo (organizzativo), EDoS e Cedimento dell'isolamento (tecnici), Protezione dati e Giurisdizione (legali); (3) saper **attribuire correttamente** un rischio alla sua categoria (è lì che cascano le domande, vedi le distinzioni sopra). Il resto (Lock-in, Supply Chain Failure, Vulnerabilità della piattaforma…) è utile ma la posta vera è l'attribuzione categoria↔rischio.

Contromisura esplicita al cedimento dell'isolamento sul fronte dati in transito: **cifratura end-to-end** — materia di S12/S13 (protezione delle comunicazioni, TLS). S6 identifica la minaccia (intercettazione nel multi-tenant), rimanda a S12/S13 per la soluzione tecnica.

---

## 10. I fili conduttori (sintesi da rivedere prima del quiz)

1. **La collocazione decide il modello di minaccia**: on-premise → accesso fisico; cloud → condivisione + delocalizzazione. Le contromisure si *adattano*, non spariscono.
2. **L'accesso fisico scavalca le difese di rete** (contrappunto diretto a S5): un firewall perfetto non ferma chi avvia la macchina da un supporto esterno o stacca il disco.
3. **Regresso della fiducia — "chi verifica chi?"**: nel boot (anti-malware ← SO ← bootloader ← BIOS ← **hardware root of trust**) e nel software da sorgenti (**Ken Thompson Hack**). Soluzione sempre uguale: ancorare la fiducia a un punto **gestito/incorruttibile** e costruire una **catena**.
4. **Measured ≠ Trusted ≠ Secure Boot**: misurare / misurare+bloccare / implementazione **UEFI** di trusted boot. (Measured = registra e demanda; remote attestation valuta da fuori.)
5. **Provenienza del software**: firma (autenticità+integrità) vs hash (solo integrità); chiavi centralizzate (comode ma **SPOF**); scope delle chiavi (**cross-signing** → `signed-by`); scelta di versione/fonte (**software injection**, **dependency confusion** = stessa logica, contesti diversi, radice = mancanza di namespace).
6. **Cloud**: responsabilità condivisa per livello (IaaS/PaaS/SaaS); benefici reali (scala, ridondanza, competenze) ma rischi propri (**organizzativi / tecnici / legali**), con disponibilità e delocalizzazione come temi ricorrenti. Sapere **attribuire ogni rischio alla categoria giusta**.

---

## 11. Griglia rapida delle distinzioni ad alto rischio di trabocchetto

| Coppia/terna | In una riga |
|---|---|
| Condivisione vs delocalizzazione | stesso hardware con altri (→isolamento) vs non so *dove* stanno i dati (→legge) |
| Keylogger hw vs key injection/BadUSB | registra passivo (esfiltra) vs digita attivo (comanda) |
| `single` vs `init=/bin/bash` | maintenance mode con default deboli vs scavalca del tutto init (bash come PID 1) |
| GRUB `password` global vs per-item vs `lock` | modalità interattiva vs avvio di *quell'*item vs marca item (serve password globale) |
| Measured vs Trusted vs Secure Boot | misura vs misura+blocca vs trusted boot su UEFI |
| db vs dbx | lista bianca (autorizzate) vs lista nera (proibite/revocate) |
| PK vs KEK | radice che autorizza tutto vs livello intermedio che autorizza gli update a db/dbx |
| Firma (`gpg --verify`) vs hash (`sha256`) | autenticità+integrità (serve chiave fidata) vs solo integrità |
| `gpgcheck=0`/`allow-insecure` vs cross-signing | verifica assente vs verifica con scope troppo largo (→`signed-by`) |
| Versione del software vs del pacchetto | versione upstream del programma vs versione del packaging |
| Software injection vs dependency confusion | omonimia fra repo di sistema vs fra repo di linguaggio (npm/pip); radice = no namespace |
| EDoS vs DoS classico | gonfia il costo (auto-scaling) vs nega il servizio |
| Lock-in vs cedimento dell'isolamento | rischio organizzativo (dipendenza) vs rischio tecnico (multi-tenancy) |
| Cedimento isolamento vs vulnerabilità piattaforma | vicino di rack rompe l'isolamento vs infrastruttura/interfaccia di gestione bucata |
| CSC vs CSP | Customer (compra) vs Provider (fornisce) |
| IaaS vs PaaS vs SaaS | gestisci il SO vs gestisci il codice vs usi solo l'app (responsabilità sale al provider) |

---

<!-- Fine appunti S6. Copertura ancorata alle 42 slide del PDF e alla lezione; ogni termine tecnico del PDF (DMA, SED, POST, CRTM/PCR, remote attestation, Clark-Wilson/TP/CDI/UDI, shim/MOK, SPOF, namespace, side channel, EDoS, SLA, ISO27001/SAS70, CSC/CSP) risolto senza zone grigie. -->
