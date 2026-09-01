****

**Obbiettivo:** Sapere la gerarchia delle firme elettroniche, il loro **valore probatorio**, come si **certificano** e quali **regole** ci sono **sulla validità** e **su come si trasmette** un **documento informatico**

**COS'E' UN DOCUMENTO?**

l'ordinamento giuridico italiano non prevede una vera generale definizione di "documento". ma il **codice giuridico** ne **definisce e regola** solo **alcuni tipi specifici**:

- Scritture private 
- Atti pubblici 
- Riproduzioni meccaniche (fotocopie di atti, contratti, etc)

	Per aiutarti a distinguere meglio, puoi chiederti:
	
	- È stato redatto da un pubblico ufficiale? (Atto Pubblico)
	- È stato firmato dalle parti interessate? (Scrittura Privata)
	- Ha valore di prova legale in quanto documento ufficiale? (Atto Pubblico)
	- Ha valore di prova legale solo se firmato dalle parti interessate? (Scrittura Privata)

**DEMATERIALIZZAZIONE DEL DOCUMENTO - documento informatico**

**Documento tradizionale**: contenitore e contenuto sono inscindibili (carta/inchiostro). La firma è apposta sul supporto fisico.

**Documento informatico**: i bit possono essere **trasferiti, riprodotti e memorizzati** su infiniti supporti diversi. Qualsiasi strumento informatico impiegato in luogo della sottoscrizione dovrà essere apposto ai **dati** da sottoscrivere e non al supporto. [fonte: PDF slide 11]

se si utilizza un **strumento informatico per firmare un documento**, la firma digitale o l'autenticazione **deve essere applicata direttamente ai dati del documento**, e **non al supporto fisico su cui il documento è memorizzato**. Ad esempio, se si firma un documento con una firma digitale, la firma deve essere applicata ai bit del documento stesso, e non al file o al disco rigido su cui il documento è memorizzato.

**Definizioni** [fonte: PDF slide 16]:

- **Documento informatico**: il documento elettronico che contiene la rappresentazione informatica di atti, fatti o dati giuridicamente rilevanti.
- **Documento elettronico**: qualsiasi contenuto conservato in forma elettronica, in particolare testo o registrazione sonora, visiva o audiovisiva.

Quindi tutti i documenti informatici sono documenti elettronici, ma non sempre viceversa

**MECCANISMO TECNICO DELLA FIRMA DIGITALE**

La firma digitale si basa su una tecnica di **crittocrafia asimmetrica** o **a doppia chiave (pubblica/privata)**

le due chiavi funzionano solo congiuntamente:

- Il **mittente firma** il documento informatico con la **propria chiave privata** (nota solo a lui).
- Il **destinatario verifica** il documento con la **chiave pubblica del mittente**.

Il meccanismo è applicato non all'intero documento ma a una sua "**impronta digitale**" (stringa di dati che ne sintetizza in modo univoco il contenuto). 

L'impronta è generata mediante algoritmi, le c.d. "**funzioni di hash**" → garantiscono che sia pressoché impossibile ottenere la stessa impronta partendo da due file di dati diversi. 
Se il documento è modificato anche di un solo bit, l'algoritmo produrrà due impronte diverse e il destinatario potrà accorgersene. [fonte: PDF slide 14]

**VALIDITA' ED EFFICACIA PROBATORIA DEL DOCUMENTO INFORMATICO**

Il documento informatico soddisfa il requisito della **forma scritta** e ha l'efficacia di **scrittura privata** (art. 2702 c.c.) quando: [fonte: PDF slide 17]

- vi è apposta una **firma digitale**, altro tipo di **firma elettronica qualificata** o una **firma elettronica avanzata**; oppure
- è formato, previa **identificazione informatica** del suo **autore**, attraverso un processo che garantisca la **sicurezza, integrità** e **immodificabilità** del documento e, in maniera manifesta e inequivoca, la sua **riconducibilità all'autore**

Se non son soddisfatte queste condizioni, il loro **valore probatorio** e la soddisfazione del requisito di **forma scritta** sono **liberamente valutabili** in giudizio

**APPROFONDIMENTO - MACROISTRUZIONI E ESEGUIBILI**

acroistruzioni e i codici eseguibili sono istruzioni o programmi che possono essere eseguiti all'interno di un documento informatico, come ad esempio:

- Macro in Word o Excel
- Script in PDF
- Codice JavaScript o VBScript in un documento Office

Questi elementi possono essere utilizzati per automatizzare compiti, eseguire calcoli o visualizzare dati, ma possono anche essere utilizzati per eseguire azioni maliziose, come ad esempio:

- Modificare il contenuto del documento
- Rubare informazioni sensibili
- Eseguire azioni dannose sul sistema

Per questo un documento che contiene **macroistruzioni o eseguibili** non soddisfa il requisito di **immodificabilità**

## §6 — Casistiche Giurisprudenziali: La E-mail

**Tribunale di Foggia, 27 novembre 2014**: la c**orrispondenza intercorsa via e-mail _può_ costituire prova scritta**, ex art. 2712 c.c., e quindi formare piena prova dei fatti o delle cose rappresentati, se colui contro il quale sono prodotte non ne disconosce la conformità. **Attenzione**: altri tribunali non hanno accettato le e-mail come prova. [fonte: PDF slide 20]

**Tribunale di Prato, 15/4/2011**: la **e-mail semplice (non PEC) è stata considerata inidonea a identificare univocamente il mittente e a provare la ricezione del messaggio.** Tuttavia, la e-mail è stata considerata documento informatico con firma elettronica, in quanto username e password sono dati utilizzati per l'identificazione informatica. [fonte: PDF slide 21]


**COPIE INFORMATICHE ED ANALOGICHE**

Documenti informatici contenente copia di atti pubblici, scritture private e documenti in genere, compresi **atti formati in origine su supporto analogico**, hanno **piena efficacia** se vi è applicata una **firma digitale o altra firma elettronica qualificata o avanzata**, sostituiscono in pieno **l'originale**

La **copia per immagine** (**scansione**) su supporto informatico di un documento analogico è prodotta mediante processi e strumenti che assicurano che il documento informatico abbia **contenuto e forma identici a quelli del documento analogico** da cui è tratto, previo raffronto dei documenti o attraverso **certificazione di processo**

Al contrario una **copia analogica di un documento informatico**, se **conforme alle regole tecniche** ha la stessa efficacia probatoria se la loro conformità non è **espressamente disconosciuta** (si può dubitare)

regole tecniche: supervisione di un **pubblico ufficiale** o apposizione di un **contrassegno** che rimanda al documento informatico

**CONSERVAZIONE E TRASMISSIONE DEI DOCUMENTI INFORMATICI**

I libri, i repertori e le scritture, ivi compresi quelli previsti dalla legge sull'ordinamento del notariato e degli archivi notarili, di cui sia **obbligatoria la tenuta** possono essere formati e conservati su **supporti informatici** in conformità al CAD e secondo le Linee Guida.

Gli obblighi di conservazione e di esibizione di documenti sono soddisfatti a tutti gli effetti di legge a mezzo di **documenti informatici**, se le procedure sono effettuate in modo tale da garantire la **conformità** ai documenti originali e sono conformi alle Linee guida.

I documenti informatici conservati per legge da pubbliche amministrazioni, gestori di servizi pubblici etc. etc.) non devono essere obbligatoriamente conservati anche dal cittadino e delle imprese, che possono in ogni momento richiedere accesso al documento ai medesimi soggetti

**TRASMISSIONE INFORMATICA**

I documenti trasmessi da chiunque ad una PA con qualsiasi **mezzo telematico o informatico, idoneo** ad accertarne la provenienza, soddisfano il requisito della **forma scritta** e la loro trasmissione **non deve essere seguita** da quella del **documento originale**.

**LA PEC - Posta Certificata**

L'invio telematico di comunicazioni che necessitano di una **ricevuta di invio** e **di consegna** avviene mediante **posta elettronica certificata** o altri metodi certificati con regole tecniche

La trasmissione del documento informatico per via telematica mediante **PEC** equivale, salvo che la legge disponga diversamente, alla **notificazione a mezzo posta**. **Data e ora** di trasmissione e ricezione mediante PEC sono **opponibili ai terzi** se conformi alla normativa vigente, incluse le regole tecniche.

## §9 — Le Firme Elettroniche: Tipologie
****
**Firma elettronica (semplice)**
"Dati in forma **elettronica**, **acclusi** oppure **connessi** tramite associazione logica ad **altri dati elettronici** e utilizzati dal firmatario per **firmare**."

**Firma elettronica avanzata** (come la firma digitale)
Una firma elettronica che: a) è **connessa unicamente** al **firmatario**; b) è **idonea a identificare** il **firmatario**; c) è creata mediante dati per la creazione di una firma elettronica che il firmatario può, con un elevato livello di sicurezza, **utilizzare sotto il proprio esclusivo controllo**; d) è **collegata ai dati sottoscritti** in modo da **consentire l'identificazione** di ogni **successiva modifica** di tali dati. [fonte: PDF slide 31]

**Firma elettronica qualificata**
una firma elettronica avanzata che soddisfa requisiti più stringenti di sicurezza e autenticità, e deve essere utilizzata per firmare documenti elettronici che richiedono un livello di sicurezza e autenticità più alto.

**Firma digitale**
Un particolare **tipo** di **firma qualificata** basata su un sistema di **chiavi crittografiche**, una **pubblica** e una **privata**, correlate tra loro, che consente al titolare tramite la chiave privata e a un soggetto terzo tramite la chiave pubblica, rispettivamente, di rendere manifesta e di verificare la **provenienza** e l'**integrità** di un documento informatico o di un insieme di documenti informatici.

(inserisci lo schema)

**Effetti giuridici delle firme elettroniche**
A una **firma elettronica non possono** essere **negati** gli **effetti giuridici** e l'**ammissibilità come prova** in procedimenti giudiziali per il **solo motivo** della sua **forma elettronica** o perché non soddisfa i requisiti per firme elettroniche **qualificate**

**FIRMA DIGITALE - dettaglio**

Deve riferirsi in modo univoco **a un solo soggetto** e al **documento o insieme di documenti** su cui è apposta o associata. Integra e sostituisce sigilli, punzoni, timbri analogici. 

Per generare la FD deve essere impiegato un **certificato qualificato non scaduto, non revocato o sospeso** al momento della firma. Dal certificato qualificato devono risultare la validità, gli estremi identificativi del titolare e del certificatore ed **eventuali limiti d'uso**.

L'apposizione di una **firma digitale** o di un altro tipo di **firma elettronica qualificata** basata su un certificato elettronico **revocato, scaduto** o **sospeso** equivale a **mancata sottoscrizione**, salvo che lo stato di sospensione sia stato annullato.

**Firme digitali straniere**
Le regole sulla firma digitale si applicano anche se la firma elettronica è basata su un certificato qualificato rilasciato da un certificatore stabilito in uno Stato non facente parte dell'Unione europea, quando ricorre una delle seguenti condizioni:

1. il certificatore possiede i requisiti previsti dal regolamento eIDAS ed è qualificato in uno Stato membro; 
2. il certificato qualificato è garantito da un certificatore stabilito nella Unione europea, in possesso dei requisiti di cui al medesimo regolamento; 
3. il certificato qualificato, o il certificatore, è riconosciuto in forza di un **accordo bilaterale o multilaterale** tra l'Unione europea e Paesi terzi o organizzazioni internazionali.

(questi successivi tipi di firma, integrali nella tabella delle firme antecedente)

12 - **IL CERTIFICATO QUALIFICATO**

Il certificato di firma elettronica è un attestato elettronico che collega i dati di convalida di una firma elettronica a una persona fisica. e ne conferma almeno il nome o pseudonimo

Esisteil **certificato qualificato**, rilasciato da un **prestatore di servizi fiduciari qualificato**

I certificati qualificati di firma elettronica contengono: [fonte: PDF slide 43-44]

- indicazione che il certificato è qualificato;
- informazioni sul prestatore di servizi fiduciari qualificato;
- il **nome del firmatario**, o uno pseudonimo;
- i dati di convalida della firma elettronica;
- **inizio e fine del periodo di validità** del certificato;
- codice di identità del certificato unico per il prestatore;
- firma elettronica avanzata o sigillo elettronico avanzato del prestatore;
- il luogo in cui il certificato è disponibile gratuitamente;
- l'ubicazione dei servizi per informarsi sulla validità del certificato qualificato;
- eventuale indicazione se i dati per la creazione della firma sono ubicati in un dispositivo qualificato.
- 
Il **certificatore** determina il **periodo di validità dei certificati qualificati** anche in funzione della robustezza crittografica delle chiavi. L'**AGID** determina il **periodo massimo** di **validità** del **certificato qualificato** in funzione degli algoritmi e delle caratteristiche delle chiavi

(spiega più semplicemente la revoca e sospensione del certificato qualificato)

certificati sospesi e revocati devono essere resi pubblici, quelli attivi possono esserlo su richiesta del titolare

**IL SIGILLO ELETTRONICO**

Il **sigillo elettronico** (per persone giuridiche, non per persone fisiche) è definito dal Regolamento eIDAS, art. 3. [fonte: PDF slide 49]

|Tipo|Definizione|
|---|---|
|**Sigillo elettronico**|Dati in forma elettronica, acclusi o connessi ad altri dati elettronici, per garantire l'origine e l'integrità di questi ultimi|
|**Sigillo elettronico avanzato**|Connesso al creatore, idoneo a identificarlo, sotto suo controllo, collegato ai dati in modo da identificare ogni modifica|
|**Sigillo elettronico qualificato**|Sigillo avanzato + dispositivo qualificato + certificato qualificato per sigilli|
## §14 — Validazione Temporale

**Validazione temporale elettronica**: dati in forma elettronica che collegano altri dati in forma elettronica a una particolare ora e data, così da provare che questi ultimi esistevano in quel momento. (eIDAS, art. 3) [fonte: PDF slide 51]

**Marca temporale**: il riferimento temporale che consente la validazione temporale e che dimostra l'esistenza di un'evidenza informatica in un tempo certo. (regole tecniche, art. 1)

**Riferimento temporale**: evidenza informatica, contenente la data e l'ora, che viene associata ad uno o più documenti informatici. (regole tecniche, art. 1)

I **riferimenti temporali** realizzati dai certificatori accreditati in conformità alle **regole tecniche** sono **opponibili ai terzi**. [fonte: PDF slide 52]

Costituiscono validazione temporale i riferimenti temporali ottenuti con l'utilizzo della **PEC**. (regole tecniche, art. 41)


**SERVIZI FIDUCIARI E I PRESTATORI**

Definizioni:

- Servizio Fiduciario: servizio elettronico per cui si paga, che crea verifica, convalida e conserva: firme, sigilli, validazioni temporali elettroniche, certifiati di autenticazione siti web. 
- Servizio Fiduciario qualificato: soddisfa i requisiti pertinenti stabiliti nel regolamento

### Accreditamento (per fare i prestatori/servizi fiduciari)

I soggetti che intendono prestare servizi fiduciari qualificati o svolgere l'attività di gestore di PEC, di gestore dell'identità digitale, di conservatore di documenti informatici, presentano all'**AgID** domanda di qualificazione o di accreditamento, allegando una relazione di valutazione della conformità rilasciata da un organismo accreditato. 

I prestatori di servizi fiduciari qualificati, i gestori di PEC, i gestori dell'identità digitale e i conservatori accreditati che cagionano **danno** ad altri nello svolgimento della loro attività, sono tenuti al **risarcimento**, **se non provano** di avere adottato tutte le **misure idonee a evitare il danno**.

### Obblighi del titolare del certificato (CAD, art. 32)

Il titolare del certificato di firma è tenuto a: [fonte: PDF slide 56]

- assicurare la **custodia** del dispositivo di firma;
- adottare **tutte le misure organizzative e tecniche idonee** ad evitare danno ad altri;
- **utilizzare personalmente** il dispositivo di firma.

### Conservazione delle chiavi

Le chiavi private possono essere conservate in un dispositivo di firma (es. smart card, chiavetta USB). [fonte: PDF slide 57]

La **chiave privata** e il **dispositivo non possono essere duplicati**. Devono essere conservati **con diligenza**, garantendo integrità e riservatezza. Le **informazioni di abilitazione** alla chiave privata vanno conservate in **luogo diverso** dal **dispositivo**.

**Necessario richiedere immediatamente la revoca** se si è perso il possesso del dispositivo contenente la chiave privata o se si ha il dubbio che sia stato utilizzato da persone non autorizzate.

### Obblighi del prestatore di servizi di firma elettronica qualificata (CAD, art. 32)

Principali: [fonte: PDF slide 58-60]

- **Identificare con certezza** la persona che fa richiesta della certificazione.
- Rilasciare e **rendere pubblico il certificato elettronico** nei modi stabiliti dalle regole tecniche.
- **Pubblicare tempestivamente** la revoca e la sospensione del certificato.
- Assicurare la **precisa determinazione della data e dell'ora** di rilascio, di revoca e di sospensione dei certificati.
- Tenere **registrazione** di tutte le informazioni relative al certificato qualificato dal momento della sua emissione **almeno per 20 anni** (ai fini di prova in eventuali procedimenti giudiziari).
- **Non copiare, né conservare**, le **chiavi private di firma dei clienti**.
- Il prestatore è **responsabile** dell'**identificazione** del soggetto che richiede il certificato qualificato **anche se tale attività è delegata a terzi**. [fonte: PDF slide 61]


## §16 — Tutela della Segretezza

Per gli atti, dati e documenti informatici inviati telematicamente è prevista una **tutela di segretezza** analoga a quella della corrispondenza cartacea. [fonte: PDF slide 62]

Gli **addetti alla trasmissione non** hanno il diritto di prendere cognizione della corrispondenza telematica, **duplicare** con qualsiasi mezzo o **cedere a terzi** informazioni anche in forma sintetica o per estratto sull'esistenza o sul contenuto di corrispondenza, comunicazioni o messaggi trasmessi per via telematica, salvo che si tratti di informazioni destinate ad essere rese pubbliche.

Gli atti, i dati e i documenti trasmessi per via **telematica** si considerano, **nei confronti del gestore** del sistema di trasporto delle informazioni, di **proprietà del mittente sino a che** non sia avvenuta la **consegna al destinatario**. (CAD, art. 49) [fonte: PDF slide 63]

## §17 — SPID e Istanze alle PA

**SPID — Sistema Pubblico delle Identità Digitali**: istituito a cura dell'Agenzia per l'Italia digitale, è un insieme aperto di soggetti pubblici e privati che, previo accreditamento da parte dell'AgID, identificano gli utenti per consentire loro l'accesso ai servizi in rete. Le pubbliche amministrazioni consentono mediante SPID l'accesso ai servizi in rete che richiedono identificazione informatica. L'accesso può avvenire anche con la carta di identità elettronica e la carta nazionale dei servizi. [fonte: PDF slide 64]

**Istanze e dichiarazioni alle PA (pubblica amministrazione)** inviate per via telematica sono valide se: [fonte: PDF slide 65]

- sottoscritte con **firma digitale o firma elettronica qualificata**, il cui certificato è rilasciato da un certificatore qualificato;
- l'autore è identificato con il sistema **SPID, la carta di identità elettronica** o la **carta nazionale dei servizi**;
- sottoscritte e presentate con un **documento di identità**;
- trasmesse dal proprio **domicilio digitale** purché le credenziali di accesso siano state rilasciate previa identificazione del titolare.

Le istanze e le dichiarazioni così presentate sono **equivalenti** alle istanze e dichiarazioni sottoscritte con **firma autografa** apposta in presenza del dipendente addetto al procedimento. (CAD, art. 65)