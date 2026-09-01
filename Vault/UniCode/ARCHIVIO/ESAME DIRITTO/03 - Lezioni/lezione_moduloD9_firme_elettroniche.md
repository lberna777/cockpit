# Lezione — Modulo D9: Firme Elettroniche e Documenti Informatici
**Corso**: Diritto dell'Informatica T
**Materiale**: `09_DirInfo_2026_FirmeElettr_DEF.pdf` (67 slide)
**Normative di riferimento**: Codice civile (artt. 2699-2719), Legge Bassanini (L. 15 marzo 1997, n. 59), CAD (D.Lgs. 7 marzo 2005, n. 82), Regolamento eIDAS (Reg. CE 910/2014), Regole tecniche (D.P.C.M. 22/02/2013), Linee Guida AGID

---

## Obiettivo

Saper spiegare la gerarchia delle firme elettroniche (semplice, avanzata, qualificata, digitale), il loro valore probatorio, il meccanismo di certificazione, e le regole sulla validità e trasmissione del documento informatico, nelle definizioni usate dalla professoressa.

---

## §1 — Quadro Normativo

Il modulo è attraversato da più fonti normative che si sovrappongono per livello e funzione. [fonte: PDF slide 2]

**Codice civile**: disciplina i tipi di documento con rilevanza probatoria (scrittura privata, riproduzioni meccaniche, atto pubblico). Non fornisce una definizione generale di "documento".

**Legge Bassanini (L. 15 marzo 1997, n. 59, art. 15 c. 2)**: prima norma che riconosce la validità e rilevanza giuridica "a tutti gli effetti di legge" degli atti, dati e documenti formati con strumenti informatici o telematici, dei contratti stipulati nelle medesime forme, e della loro archiviazione e trasmissione. Lo stesso principio vale per PA e privati. [fonte: PDF slide 3]

**CAD — Codice dell'Amministrazione Digitale (D.Lgs. 7 marzo 2005, n. 82)**: disciplina l'impiego delle nuove tecnologie nella pubblica amministrazione. Le regole relative a documenti informatici, firme elettroniche, pagamenti informatici, libri e scritture si applicano **anche ai privati**. [fonte: PDF slide 4]

**Regole tecniche (D.P.C.M. 22 febbraio 2013)**: "Regole tecniche in materia di generazione, apposizione e verifica delle firme elettroniche avanzate, qualificate e digitali". [fonte: PDF slide 5]

**Regolamento eIDAS (Reg. CE 910/2014)**: disciplina il riconoscimento dei mezzi di identificazione elettronica tra Stati membri e stabilisce le norme relative ai servizi fiduciari. Istituisce un quadro giuridico per firme elettroniche, sigilli elettronici, validazioni temporali elettroniche, documenti elettronici, servizi di recapito certificato e certificati di autenticazione di siti web. [fonte: PDF slide 6]

**Linee Guida AGID**: sulla formazione, gestione e conservazione dei documenti informatici.

---

## §2 — Il Concetto di Documento

L'ordinamento giuridico italiano non prevede una definizione di "documento" in generale. Il codice civile definisce e regola alcuni tipi specifici: [fonte: PDF slide 7]

- **Scritture private** (artt. 2702-2708)
- **Riproduzioni meccaniche** (art. 2712, richiamato come 2719 nelle slide)
- **Atti pubblici** (artt. 2699-2701)

### Scrittura privata (art. 2702 c.c.)
"La scrittura privata fa piena prova, fino a querela di falso, della **provenienza** delle dichiarazioni da chi l'ha **sottoscritta**, **se colui contro il quale** la scrittura è **prodotta** ne **riconosce** la sottoscrizione, ovvero se questa è **legalmente** considerata come **riconosciuta**." [fonte: PDF slide 8]

Per essere valida la firma: **non deve essere disconosciuta** durante una causa, **oppure** deve essere **autenticata**. Se si vuole contestare la provenienza occorre impugnare il documento con la querela di falso.

### Riproduzioni meccaniche (art. 2712 c.c.)
"Le riproduzioni fotografiche, informatiche o cinematografiche, le registrazioni fonografiche e, in genere, ogni altra rappresentazione meccanica di fatti e di cose formano **piena prova** dei fatti e delle cose rappresentate, **se colui contro il quale sono prodotte non ne disconosce la conformità** ai fatti o alle cose medesime." [fonte: PDF slide 9]

Il riferimento a "ogni altra rappresentazione meccanica" permette di applicare questa norma a qualsiasi tecnica di rappresentazione dei fatti.

### Atto pubblico (art. 2699 c.c.)
"L'**atto pubblico** è il documento redatto, con le richieste formalità, da un **notaio** o da altro **pubblico ufficiale autorizzato** ad attribuirgli **pubblica fede** nel luogo dove l'atto è formato." [fonte: PDF slide 10]

L'atto pubblico dà certezza ufficiale su tutto ciò che si è svolto davanti al pubblico ufficiale. Può essere contestato solo con querela di falso. Esempi: atto di compravendita immobiliare, atto di costituzione di società di capitali, stipula contratto di mutuo.

---

## §3 — Dematerializzazione e Documento Informatico

**Documento tradizionale**: contenitore e contenuto sono inscindibili (carta/inchiostro). La firma è apposta sul supporto fisico.

**Documento informatico**: i bit possono essere trasferiti, riprodotti e memorizzati su infiniti supporti diversi. Qualsiasi strumento informatico impiegato in luogo della sottoscrizione dovrà essere apposto ai **dati** da sottoscrivere e non al supporto. [fonte: PDF slide 11]

Un documento formato e memorizzato mediante computer dovrebbe essere: inalterabile, conservabile, accessibile a distanza di tempo, imputabile a un soggetto determinato, riconosciuto giuridicamente. [fonte: PDF slide 12]

**Definizioni** [fonte: PDF slide 16]:

- **Documento informatico**: il documento elettronico che contiene la rappresentazione informatica di atti, fatti o dati giuridicamente rilevanti.
- **Documento elettronico**: qualsiasi contenuto conservato in forma elettronica, in particolare testo o registrazione sonora, visiva o audiovisiva.

A un **documento elettronico non** sono **negati** gli **effetti giuridici** e l'**ammissibilità come prova** in procedimenti giudiziali per il **solo motivo** della sua **forma elettronica**.

---

## §4 — Meccanismo Tecnico della Firma Digitale

La firma digitale (FD) è il risultato di una procedura informatica e si basa sulla tecnica di **crittografia asimmetrica** o **a doppia chiave (pubblica/privata)**. [fonte: PDF slide 13]

Sono impiegate **due chiavi diverse** (una privata e una pubblica), in grado di funzionare solo congiuntamente:
- Il **mittente firma** il documento informatico con la **propria chiave privata** (nota solo a lui).
- Il **destinatario verifica** il documento con la **chiave pubblica del mittente**.

Grazie a questo sistema, il destinatario è in grado di verificare sia la **paternità** del documento sia il **fatto** che non sia stato **modificato**.

Il meccanismo è applicato non all'intero documento ma a una sua "**impronta digitale**" (stringa di dati che ne sintetizza in modo univoco il contenuto). L'impronta è generata mediante algoritmi, le c.d. "**funzioni di hash**" → garantiscono che sia pressoché impossibile ottenere la stessa impronta partendo da due file di dati diversi. Se il documento è modificato anche di un solo bit, l'algoritmo produrrà due impronte diverse e il destinatario potrà accorgersene. [fonte: PDF slide 14]

### La certificazione
La firma digitale di per sé non è in grado di garantire la reale identità del firmatario: questi potrebbe firmare a nome di un terzo o con un nome inventato. È previsto l'intervento di "terze parti fidate", i c.d. **certificatori**, che: [fonte: PDF slide 15]
- verificano l'**identità** di un soggetto,
- la associano a una **chiave pubblica** di cifratura,
- **attestano** tali informazioni mediante l'emissione di un **certificato**,
- **pubblicano** tempestivamente **revoca** e **sospensione** del certificato in apposite **liste**.

---

## §5 — Validità ed Efficacia Probatoria del Documento Informatico

### Quando il documento informatico vale come scrittura privata

Il documento informatico soddisfa il requisito della **forma scritta** e ha l'efficacia di **scrittura privata** (art. 2702 c.c.) quando: [fonte: PDF slide 17]

- vi è apposta una **firma digitale**, altro tipo di **firma elettronica qualificata** o una **firma elettronica avanzata**; oppure
- è formato, previa **identificazione informatica** del suo **autore**, attraverso un processo che garantisca la **sicurezza, integrità** e **immodificabilità** del documento e, in maniera manifesta e inequivoca, la sua **riconducibilità all'autore**.

### Negli altri casi
In **tutti gli altri casi**, l'idoneità del documento informatico a soddisfare il requisito della **forma scritta** e il suo **valore probatorio** sono **liberamente valutabili in giudizio, in relazione alle caratteristiche di sicurezza, integrità** e **immodificabilità**. [fonte: PDF slide 18]

La **data** e l'**ora** di formazione del documento informatico sono **opponibili ai terzi** se apposte in conformità alle **Linee guida**.

### IMPORTANTE — Macroistuzioni e codici eseguibili

Il documento informatico sottoscritto con firma elettronica qualificata o digitale **NON** soddisfa il requisito di **immodificabilità** del documento se contiene **macroistuzioni, codici eseguibili** o altri elementi tali da attivare funzionalità che possano **modificare** gli atti, i fatti o i dati nello stesso rappresentati. (art. 4, c. 3 reg. tecn.) [fonte: PDF slide 19]

---

## §6 — Casistiche Giurisprudenziali: La E-mail

**Tribunale di Foggia, 27 novembre 2014**: la corrispondenza intercorsa via e-mail *può* costituire prova scritta, ex art. 2712 c.c., e quindi formare piena prova dei fatti o delle cose rappresentati, se colui contro il quale sono prodotte non ne disconosce la conformità. **Attenzione**: altri tribunali non hanno accettato le e-mail come prova. [fonte: PDF slide 20]

**Tribunale di Prato, 15/4/2011**: la e-mail semplice (non PEC) è stata considerata inidonea a identificare univocamente il mittente e a provare la ricezione del messaggio. Tuttavia, la e-mail è stata considerata documento informatico con firma elettronica, in quanto username e password sono dati utilizzati per l'identificazione informatica. [fonte: PDF slide 21]

---

## §7 — Copie Informatiche e Analogiche

### Copie informatiche di documenti analogici
Il **documento analogico** è la rappresentazione non informatica di atti, fatti o dati giuridicamente rilevanti (es. documenti cartacei). [fonte: PDF slide 22]

I documenti informatici contenenti copia di atti pubblici, scritture private e documenti in genere, compresi gli atti formati **in origine su supporto analogico**, spediti o rilasciati da depositari pubblici autorizzati e pubblici ufficiali, hanno **piena efficacia** (ai sensi artt. 2714 e 2715 c.c.) se vi è apposta una **firma digitale o altra firma elettronica qualificata o avanzata**. La loro esibizione e produzione **sostituisce** quella dell'originale. [fonte: PDF slide 22]

La **copia per immagine** su supporto informatico di un documento analogico è prodotta mediante processi e strumenti che assicurano che il documento informatico abbia **contenuto e forma identici a quelli del documento analogico** da cui è tratto, previo raffronto dei documenti o attraverso **certificazione di processo**. [fonte: PDF slide 23]

Le copie per immagine hanno la **stessa efficacia probatoria** degli originali: [fonte: PDF slide 24]
- se la loro conformità è attestata da un **notaio o altro pubblico ufficiale** a ciò autorizzato, secondo le Linee Guida; oppure
- nel rispetto delle Linee Guida, se la loro conformità **non è espressamente disconosciuta**.

Le copie formate nei modi indicati **sostituiscono** a ogni effetto di legge gli originali formati in origine su supporto analogico e sono idonee ad **assolvere gli obblighi di conservazione** previsti dalla legge.

### Copie analogiche di documenti informatici
Le copie analogiche di documenti informatici (anche sottoscritti con firma avanzata, qualificata o digitale) hanno la stessa efficacia probatoria dell'originale da cui sono tratte se la loro conformità in tutte le sue componenti è attestata da un **pubblico ufficiale** a ciò autorizzato. [fonte: PDF slide 25]

Le copie e gli estratti su supporto analogico, conformi alle regole tecniche, hanno la stessa efficacia probatoria se la loro conformità **non è espressamente disconosciuta**.

Sulle copie analogiche può essere apposto a stampa un **contrassegno**, col quale è possibile accedere al documento informatico o verificare la corrispondenza della copia. Il contrassegno **sostituisce** a tutti gli effetti di legge la **sottoscrizione autografa** del pubblico ufficiale.

### Copie informatiche di documenti informatici
I **duplicati informatici** hanno lo **stesso valore giuridico**, ad ogni effetto di legge, del documento informatico da cui sono tratti, se prodotti in **conformità** alle **Linee Guida**. [fonte: PDF slide 26]

Le copie e gli estratti informatici hanno la stessa efficacia probatoria dell'originale se la loro conformità in tutte le sue componenti è attestata da un pubblico ufficiale o se la conformità **non è espressamente disconosciuta**.

---

## §8 — Conservazione e Trasmissione dei Documenti Informatici

### Libri e scritture
I libri, i repertori e le scritture, ivi compresi quelli previsti dalla legge sull'ordinamento del notariato e degli archivi notarili, di cui sia **obbligatoria la tenuta** possono essere formati e conservati su **supporti informatici** in conformità al CAD e secondo le Linee Guida. [fonte: PDF slide 27]

### Conservazione ed esibizione
Gli obblighi di conservazione e di esibizione di documenti sono soddisfatti a tutti gli effetti di legge a mezzo di **documenti informatici**, se le procedure sono effettuate in modo tale da garantire la **conformità** ai documenti originali e sono conformi alle Linee guida. [fonte: PDF slide 28]

Se il documento informatico è **conservato per legge** da uno dei soggetti di cui all'art. 2, c. 2 (es. pubbliche amministrazioni, gestori di servizi pubblici), **cessa l'obbligo di conservazione** a carico dei **cittadini** e delle **imprese**, che possono in ogni momento richiedere accesso al documento stesso ai medesimi soggetti.

### Trasmissione informatica
Il documento informatico inviato telematicamente si intende: [fonte: PDF slide 29]
- **spedito dal mittente** se inviato al proprio gestore;
- **consegnato al destinatario** se reso disponibile all'indirizzo elettronico da questi dichiarato, nella casella di posta elettronica del destinatario messa a disposizione dal gestore.

I documenti trasmessi da chiunque ad una PA con qualsiasi **mezzo telematico o informatico, idoneo** ad accertarne la provenienza, soddisfano il requisito della **forma scritta** e la loro trasmissione **non deve essere seguita** da quella del **documento originale**.

### Trasmissione mediante PEC
L'invio telematico di comunicazioni che necessitano di una **ricevuta di invio** e **di consegna** avviene mediante **posta elettronica certificata** (DPR 11 febbraio 2005, n. 68) o con altre soluzioni tecnologiche individuate con le regole tecniche. [fonte: PDF slide 30]

La trasmissione del documento informatico per via telematica mediante **PEC** equivale, salvo che la legge disponga diversamente, alla **notificazione a mezzo posta**. **Data e ora** di trasmissione e ricezione mediante PEC sono **opponibili ai terzi** se conformi alla normativa vigente, incluse le regole tecniche.

---

## §9 — Le Firme Elettroniche: Tipologie

### Firma elettronica (semplice)
"Dati in forma **elettronica**, **acclusi** oppure **connessi** tramite associazione logica ad **altri dati elettronici** e utilizzati dal firmatario per **firmare**." [fonte: PDF slide 31]

### Firma elettronica avanzata
Una firma elettronica che:
a) è **connessa unicamente** al **firmatario**;
b) è **idonea a identificare** il **firmatario**;
c) è creata mediante dati per la creazione di una firma elettronica che il firmatario può, con un elevato livello di sicurezza, **utilizzare sotto il proprio esclusivo controllo**;
d) è **collegata ai dati sottoscritti** in modo da **consentire l'identificazione** di ogni **successiva modifica** di tali dati. [fonte: PDF slide 31]

### Firma elettronica qualificata
Una **firma elettronica avanzata** che è: [fonte: PDF slide 32]
- **creata** da un **dispositivo per la creazione di una firma elettronica qualificata** e
- **basata** su un **certificato qualificato** per firme elettroniche.

### Firma digitale
Un particolare **tipo** di **firma qualificata** basata su un sistema di **chiavi crittografiche**, una **pubblica** e una **privata**, correlate tra loro, che consente al titolare tramite la chiave privata e a un soggetto terzo tramite la chiave pubblica, rispettivamente, di rendere manifesta e di verificare la **provenienza** e l'**integrità** di un documento informatico o di un insieme di documenti informatici. (CAD, art. 1) [fonte: PDF slide 34]

### Schema riassuntivo delle tipologie

| Tipo | Definizione sintetica | Valore giuridico |
|------|----------------------|-----------------|
| Firma elettronica (semplice) | Qualsiasi dato elettronico usato per firmare | Non negati effetti giuridici né ammissibilità come prova |
| Firma elettronica avanzata | Connessa univocamente al firmatario, sotto suo esclusivo controllo | Scrittura privata (art. 2702 c.c.) |
| Firma elettronica qualificata | Avanzata + dispositivo qualificato + certificato qualificato | Equivalente a firma autografa |
| Firma digitale | Tipo specifico di qualificata italiana, basata su chiavi crittografiche (CAD, art. 1) | Equivalente a firma autografa |

### Effetti giuridici delle firme elettroniche
A una **firma elettronica non possono** essere **negati** gli **effetti giuridici** e l'**ammissibilità come prova** in procedimenti giudiziali per il **solo motivo** della sua **forma elettronica** o perché non soddisfa i requisiti per firme elettroniche **qualificate**. [fonte: PDF slide 33]

Una **firma elettronica qualificata** ha effetti giuridici equivalenti a quelli di una **firma autografa**.

**Attenzione**: una firma elettronica qualificata basata su un certificato qualificato rilasciato in uno Stato membro è riconosciuta quale firma elettronica qualificata in tutti gli altri Stati membri. [fonte: PDF slide 33]

---

## §10 — Firma Digitale: Dettaglio

### Caratteristiche essenziali
La FD deve riferirsi in modo univoco a **un solo soggetto** e al **documento** (o insieme di documenti) cui è apposta o associata. Integra e sostituisce sigilli, punzoni, timbri, contrassegni e marchi di qualsiasi genere a ogni fine previsto dalla normativa vigente. [fonte: PDF slide 35]

Per generare la FD deve essere impiegato un **certificato qualificato non scaduto, non revocato o sospeso** al momento della firma. Dal certificato qualificato devono risultare la validità, gli estremi identificativi del titolare e del certificatore ed **eventuali limiti d'uso**.

### Conseguenze del certificato invalido
L'apposizione di una **firma digitale** o di un altro tipo di **firma elettronica qualificata** basata su un certificato elettronico **revocato, scaduto** o **sospeso** equivale a **mancata sottoscrizione**, salvo che lo stato di sospensione sia stato annullato. [fonte: PDF slide 36]

La **revoca o la sospensione**, comunque motivate, hanno **effetto dal momento della pubblicazione**, salvo che il revocante, o chi richiede la sospensione, non dimostri che essa era già a conoscenza di tutte le parti interessate.

### Applicazione transfrontaliera
Le regole sulla firma digitale si applicano anche se la firma elettronica è basata su un certificato qualificato rilasciato da un certificatore stabilito in uno Stato non facente parte dell'Unione europea, quando ricorre una delle seguenti condizioni: [fonte: PDF slide 37]
a) il certificatore possiede i requisiti previsti dal regolamento eIDAS ed è qualificato in uno Stato membro;
b) il certificato qualificato è garantito da un certificatore stabilito nella Unione europea, in possesso dei requisiti di cui al medesimo regolamento;
c) il certificato qualificato, o il certificatore, è riconosciuto in forza di un **accordo bilaterale o multilaterale** tra l'Unione europea e Paesi terzi o organizzazioni internazionali.

### IMPORTANTE — Valore delle firme qualificate e digitali nel tempo
Le firme elettroniche qualificate e digitali, anche se è scaduto, revocato o sospeso il relativo certificato qualificato del sottoscrittore, sono **valide** se alle stesse è associabile un **riferimento temporale opponibile ai terzi** che colloca la generazione di dette firme in un **momento precedente** alla scadenza, revoca o sospensione, scadenza o revoca del suddetto certificato. (regole tecniche, art. 62) [fonte: PDF slide 38]

---

## §11 — Firma Automatica, Remota e Autenticata

**Firma automatica**: particolare procedura informatica di firma elettronica qualificata o di firma digitale eseguita previa autorizzazione del sottoscrittore che mantiene il controllo esclusivo delle proprie chiavi di firma, in assenza di presidio puntuale e continuo da parte di questo. [fonte: PDF slide 39]

**Firma remota**: particolare procedura di firma elettronica qualificata o di firma digitale, generata su HSM(*), che consente di garantire il controllo esclusivo delle chiavi private da parte dei titolari delle stesse.
(*) HSM: insieme di hardware e software che realizza dispositivi sicuri per la generazione delle firme in grado di gestire in modo sicuro una o più coppie di chiavi crittografiche.

### Firma autenticata
La firma elettronica o la firma elettronica avanzata può essere **autenticata** da: notaio o altro pubblico ufficiale autorizzato. Può essere acquisita digitalmente la sottoscrizione autografa o qualsiasi firma elettronica avanzata. [fonte: PDF slide 40]

**Autenticazione** (= cosa fa il pubblico ufficiale): [fonte: PDF slide 41]
- accertamento dell'**identità** personale del firmatario;
- attestazione che la **firma** è stata apposta **in sua presenza**;
- accertamento della **validità** dell'eventuale **certificato elettronico**;
- accertamento che il documento sottoscritto **non è contrario all'ordinamento giuridico**.

---

## §12 — Il Certificato Qualificato

### Definizioni
**Certificato di firma elettronica**: un attestato elettronico che collega i dati di convalida di una firma elettronica a una persona fisica e conferma almeno il nome o lo pseudonimo di tale persona. [fonte: PDF slide 42]

**Certificato qualificato di firma elettronica**: un certificato di firma elettronica che è rilasciato da un **prestatore di servizi fiduciari qualificato** ed è conforme ai requisiti di cui all'**allegato I** del Regolamento eIDAS. [fonte: PDF slide 42]

### Contenuto del certificato qualificato
I certificati qualificati di firma elettronica contengono: [fonte: PDF slide 43-44]
- indicazione che il certificato è qualificato;
- informazioni sul prestatore di servizi fiduciari qualificato;
- il **nome del firmatario**, o uno pseudonimo;
- i dati di convalida della firma elettronica;
- **inizio e fine del periodo di validità** del certificato;
- codice di identità del certificato unico per il prestatore;
- firma elettronica avanzata o sigillo elettronico avanzato del prestatore;
- il luogo in cui il certificato è disponibile gratuitamente;
- l'ubicazione dei servizi per informarsi sulla validità del certificato qualificato;
- eventuale indicazione se i dati per la creazione della firma sono ubicati in un dispositivo qualificato.

### Periodo di validità
Il **certificatore** determina il **periodo di validità dei certificati qualificati** anche in funzione della robustezza crittografica delle chiavi. L'**AGID** determina il **periodo massimo** di **validità** del **certificato qualificato** in funzione degli algoritmi e delle caratteristiche delle chiavi. (Regole tecniche, art. 19) [fonte: PDF slide 45]

### Revoca e sospensione del certificato qualificato
Il certificato qualificato deve essere a cura del certificatore: [fonte: PDF slide 46]
a) **revocato** in caso di **cessazione** dell'attività del certificatore, a meno che non abbia indicato un **certificatore sostitutivo**;
b) **revocato o sospeso** in esecuzione di un **provvedimento dell'autorità**;
c) **revocato o sospeso** a seguito di **richiesta del titolare** o del terzo dal quale derivano i poteri del titolare;
d) **revocato o sospeso** in presenza di **cause limitative della capacità** del titolare o di **abusi o falsificazioni**.

Il certificato qualificato può essere revocato o sospeso anche per **violazione delle regole tecniche** previste nelle Linee guida. [fonte: PDF slide 47]

La revoca o la sospensione, **qualunque** ne sia la causa, ha **effetto dal momento della pubblicazione della lista che lo contiene**. Il momento della pubblicazione deve essere attestato mediante adeguato **riferimento temporale**. (CAD, art. 36)

### Accesso ai certificati
Le **liste dei certificati revocati e sospesi devono essere rese pubbliche**. I **certificati qualificati possono** essere resi **accessibili al pubblico** su richiesta del titolare. [fonte: PDF slide 48]

Le liste possono essere utilizzate solo per le finalità di applicazione delle norme sulla verifica e validità delle firme elettroniche qualificate e digitali. **Chiunque** ha **diritto** di conoscere **se a proprio nome** sia stato rilasciato un **certificato qualificato**. (regole tecniche, art. 34)

---

## §13 — Il Sigillo Elettronico

Il **sigillo elettronico** (per persone giuridiche, non per persone fisiche) è definito dal Regolamento eIDAS, art. 3. [fonte: PDF slide 49]

| Tipo | Definizione |
|------|-------------|
| **Sigillo elettronico** | Dati in forma elettronica, acclusi o connessi ad altri dati elettronici, per garantire l'origine e l'integrità di questi ultimi |
| **Sigillo elettronico avanzato** | Connesso al creatore, idoneo a identificarlo, sotto suo controllo, collegato ai dati in modo da identificare ogni modifica |
| **Sigillo elettronico qualificato** | Sigillo avanzato + dispositivo qualificato + certificato qualificato per sigilli |

### Effetti giuridici dei sigilli elettronici
A un **sigillo elettronico non** possono essere **negati** gli **effetti giuridici** e l'**ammissibilità come prova** per il solo motivo della sua forma elettronica o perché non soddisfa i requisiti per i sigilli elettronici qualificati. [fonte: PDF slide 50]

Un **sigillo elettronico qualificato** gode della **presunzione di integrità** dei **dati** e di **correttezza dell'origine** di quei dati a cui il sigillo elettronico qualificato è associato. (eIDAS, art. 35)

---

## §14 — Validazione Temporale

**Validazione temporale elettronica**: dati in forma elettronica che collegano altri dati in forma elettronica a una particolare ora e data, così da provare che questi ultimi esistevano in quel momento. (eIDAS, art. 3) [fonte: PDF slide 51]

**Marca temporale**: il riferimento temporale che consente la validazione temporale e che dimostra l'esistenza di un'evidenza informatica in un tempo certo. (regole tecniche, art. 1)

**Riferimento temporale**: evidenza informatica, contenente la data e l'ora, che viene associata ad uno o più documenti informatici. (regole tecniche, art. 1)

I **riferimenti temporali** realizzati dai certificatori accreditati in conformità alle **regole tecniche** sono **opponibili ai terzi**. [fonte: PDF slide 52]

Costituiscono validazione temporale i riferimenti temporali ottenuti con l'utilizzo della **PEC**. (regole tecniche, art. 41)

---

## §15 — I Servizi Fiduciari e i Prestatori

### Definizioni
**Servizio fiduciario**: un servizio elettronico fornito normalmente dietro remunerazione, consistente in: creazione, verifica e convalida di firme/sigilli/validazioni temporali elettroniche; creazione, verifica e convalida di certificati di autenticazione di siti web; o conservazione di firme, sigilli o certificati elettronici. (eIDAS, art. 3) [fonte: PDF slide 53]

**Servizio fiduciario qualificato**: un servizio fiduciario che soddisfa i requisiti pertinenti stabiliti nel Regolamento.

### Accreditamento
I soggetti che intendono prestare servizi fiduciari qualificati o svolgere l'attività di gestore di PEC, di gestore dell'identità digitale, di conservatore di documenti informatici, presentano all'**AgID** domanda di qualificazione o di accreditamento, allegando una relazione di valutazione della conformità rilasciata da un organismo accreditato. (CAD, art. 29) [fonte: PDF slide 54]

Requisiti: natura giuridica di società di capitali, requisiti di onorabilità, tecnologici e organizzativi, garanzie assicurative.

### Responsabilità
I prestatori di servizi fiduciari qualificati, i gestori di PEC, i gestori dell'identità digitale e i conservatori accreditati che cagionano **danno** ad altri nello svolgimento della loro attività, sono tenuti al **risarcimento**, **se non provano** di avere adottato tutte le **misure idonee a evitare il danno**. [fonte: PDF slide 55]

Il certificato qualificato può contenere **limiti d'uso o di valore**, purché i limiti siano riconoscibili da parte dei terzi e chiaramente evidenziati nel certificato: il **certificatore non è responsabile** dei danni derivanti dall'uso di un certificato qualificato che ecceda i limiti posti. (CAD, art. 30)

### Obblighi del titolare del certificato (CAD, art. 32)
Il titolare del certificato di firma è tenuto a: [fonte: PDF slide 56]
- assicurare la **custodia** del dispositivo di firma;
- adottare **tutte le misure organizzative e tecniche idonee** ad evitare danno ad altri;
- **utilizzare personalmente** il dispositivo di firma.

### Conservazione delle chiavi
Le chiavi private possono essere conservate in un dispositivo di firma (es. smart card, chiavetta USB). [fonte: PDF slide 57]

La **chiave privata** e il **dispositivo non possono essere duplicati**. Devono essere conservati **con diligenza**, garantendo integrità e riservatezza. Le **informazioni di abilitazione** alla chiave privata vanno conservate in **luogo diverso** dal **dispositivo**.

**Necessario richiedere immediatamente la revoca** se si è perso il possesso del dispositivo contenente la chiave privata o se si ha il dubbio che sia stato utilizzato da persone non autorizzate.

### Obblighi del prestatore di servizi di firma elettronica qualificata (CAD, art. 32)
Principali: [fonte: PDF slide 58-60]
- **Identificare con certezza** la persona che fa richiesta della certificazione.
- Rilasciare e **rendere pubblico il certificato elettronico** nei modi stabiliti dalle regole tecniche.
- **Pubblicare tempestivamente** la revoca e la sospensione del certificato.
- Assicurare la **precisa determinazione della data e dell'ora** di rilascio, di revoca e di sospensione dei certificati.
- Tenere **registrazione** di tutte le informazioni relative al certificato qualificato dal momento della sua emissione **almeno per 20 anni** (ai fini di prova in eventuali procedimenti giudiziari).
- **Non copiare, né conservare**, le **chiavi private di firma dei clienti**.
- Il prestatore è **responsabile** dell'**identificazione** del soggetto che richiede il certificato qualificato **anche se tale attività è delegata a terzi**. [fonte: PDF slide 61]

---

## §16 — Tutela della Segretezza

Per gli atti, dati e documenti informatici inviati telematicamente è prevista una **tutela di segretezza** analoga a quella della corrispondenza cartacea. [fonte: PDF slide 62]

Gli **addetti alla trasmissione non** hanno il diritto di prendere cognizione della corrispondenza telematica, **duplicare** con qualsiasi mezzo o **cedere a terzi** informazioni anche in forma sintetica o per estratto sull'esistenza o sul contenuto di corrispondenza, comunicazioni o messaggi trasmessi per via telematica, salvo che si tratti di informazioni destinate ad essere rese pubbliche.

Gli atti, i dati e i documenti trasmessi per via **telematica** si considerano, **nei confronti del gestore** del sistema di trasporto delle informazioni, di **proprietà del mittente sino a che** non sia avvenuta la **consegna al destinatario**. (CAD, art. 49) [fonte: PDF slide 63]

---

## §17 — SPID e Istanze alle PA

**SPID — Sistema Pubblico delle Identità Digitali**: istituito a cura dell'Agenzia per l'Italia digitale, è un insieme aperto di soggetti pubblici e privati che, previo accreditamento da parte dell'AgID, identificano gli utenti per consentire loro l'accesso ai servizi in rete. Le pubbliche amministrazioni consentono mediante SPID l'accesso ai servizi in rete che richiedono identificazione informatica. L'accesso può avvenire anche con la carta di identità elettronica e la carta nazionale dei servizi. [fonte: PDF slide 64]

**Istanze e dichiarazioni alle PA** inviate per via telematica sono valide se: [fonte: PDF slide 65]
- sottoscritte con **firma digitale o firma elettronica qualificata**, il cui certificato è rilasciato da un certificatore qualificato;
- l'autore è identificato con il sistema **SPID, la carta di identità elettronica** o la **carta nazionale dei servizi**;
- sottoscritte e presentate con un **documento di identità**;
- trasmesse dal proprio **domicilio digitale** purché le credenziali di accesso siano state rilasciate previa identificazione del titolare.

Le istanze e le dichiarazioni così presentate sono **equivalenti** alle istanze e dichiarazioni sottoscritte con **firma autografa** apposta in presenza del dipendente addetto al procedimento. (CAD, art. 65)

---

## §18 — Riferimenti Normativi Riepilogo

| Articolo / Norma | Contenuto | Rilevanza |
|------------------|-----------|-----------|
| Art. 2699 c.c. | Atto pubblico | Documento con pubblica fede, contestabile solo con querela di falso |
| Art. 2702 c.c. | Scrittura privata | Piena prova provenienza se non disconosciuta o autenticata |
| Art. 2712 c.c. | Riproduzioni meccaniche | Piena prova se conformità non disconosciuta; include doc. informatici |
| L. 59/1997, art. 15 c. 2 | Legge Bassanini | Prima norma che riconosce validità giuridica dei documenti informatici |
| CAD, art. 1 | Firma digitale | Definizione normativa italiana |
| CAD, art. 20 | Validità doc. informatico | Forma scritta + scrittura privata con firma qualificata/avanzata |
| CAD, art. 29 | Accreditamento | Requisiti per prestatori fiduciari qualificati |
| CAD, art. 30 | Responsabilità prestatori | Risarcimento; limiti d'uso nel certificato |
| CAD, art. 32 | Obblighi titolare e prestatore | Custodia, identificazione, non duplicare chiavi |
| CAD, art. 36 | Revoca/sospensione | Effetto dalla pubblicazione della lista |
| CAD, art. 49 | Tutela segretezza | Proprietà del mittente fino alla consegna |
| CAD, art. 65 | Istanze alla PA | Condizioni di validità delle comunicazioni telematiche |
| Reg. eIDAS, art. 3 | Definizioni | Servizi fiduciari, validazione temporale, sigillo |
| Reg. eIDAS, art. 35 | Sigillo qualificato | Presunzione di integrità e correttezza origine |
| Art. 4 c. 3 reg. tecn. | Macroistuzioni | Firma qualificata/digitale non garantisce immodificabilità con macro |
| Art. 62 reg. tecn. | Valore firme nel tempo | Firma valida se riferimento temporale opponibile ai terzi |

---

## Domande di Autoverifica

1. Qual è la differenza tra firma elettronica semplice, firma elettronica avanzata, firma elettronica qualificata e firma digitale? Definisci ciascuna nelle parole del PDF.

2. Quando un documento informatico ha l'efficacia della **scrittura privata** ai sensi dell'art. 2702 c.c.? Cosa succede "in tutti gli altri casi"?

3. Cosa sono la **marca temporale** e il **riferimento temporale**? Perché il valore delle firme qualificate e digitali "nel tempo" è rilevante?

4. Quali sono gli obblighi principali del **prestatore di servizi di firma elettronica qualificata** nei confronti del titolare e dei terzi? Quale responsabilità ha se cagiona un danno?

5. Cosa accade se un documento informatico sottoscritto con firma digitale contiene **macroistuzioni o codici eseguibili**? Cita la norma di riferimento.

---

## Attenzione Ripasso (dalla professoressa — slide 66-67)

Le slide indicano esplicitamente come temi prioritari per l'esame:
- Scrittura privata, sottoscrizione autografa, atto pubblico, riproduzioni meccaniche
- Tecnologia e meccanismo di firma digitale
- Certificazione (cosa è e a cosa serve)
- **FIRMA ELETTRONICA SEMPLICE, AVANZATA, QUALIFICATA E DIGITALE!!**
- Certificato qualificato (i punti essenziali)
- **VALIDITA' DEL DOCUMENTO INFORMATICO!!**
- **MACROISTUZIONI nel documento informatico**
- Cosa succede se il certificato della firma è revocato o sospeso?
- Copie analogiche di documenti informatici e copie informatiche di originali cartacei
- **TRASMISSIONE del documento informatico**
- **La PEC**
- I prestatori di servizi fiduciari: cosa sono, compiti e responsabilità
- Obblighi del titolare e del prestatore
- **Valore** delle firme qualificate e digitali **nel TEMPO**

---

## Riepilogo

- La **dematerializzazione** separa contenuto e supporto: la firma elettronica si appone ai dati, non al mezzo fisico. Il documento informatico deve essere inalterabile, conservabile, accessibile, imputabile e riconosciuto giuridicamente.
- Le firme elettroniche formano una gerarchia crescente (semplice → avanzata → qualificata → digitale): solo le ultime due equivalgono alla firma autografa, e solo se il certificato qualificato è valido al momento della firma.
- Il **valore nel tempo** dipende dal **riferimento temporale opponibile ai terzi**: una firma qualificata/digitale rimane valida anche dopo la scadenza/revoca del certificato, purché sia dimostrabile che è stata apposta prima dell'evento.
