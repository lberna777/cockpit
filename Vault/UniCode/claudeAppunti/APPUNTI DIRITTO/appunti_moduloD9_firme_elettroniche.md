# Appunti — Modulo D9: Firme Elettroniche e Documenti Informatici
**Corso**: Diritto dell'Informatica T
**PDF**: `09_DirInfo_2026_FirmeElettr_DEF.pdf` (67 slide)
**Normative**: c.c. artt. 2699-2712, L. 59/1997, CAD (D.Lgs. 82/2005), Reg. eIDAS (910/2014), Regole tecniche (D.P.C.M. 22/02/2013), Linee Guida AGID

---

## Obiettivo

Sapere la gerarchia delle firme elettroniche, il loro **valore probatorio**, come si **certificano** e quali **regole** ci sono **sulla validità** e **su come si trasmette** un **documento informatico**.

---

## §1 — Quadro Normativo

> ⚠️ Questa sezione non era presente negli appunti grezzi.

Il modulo è attraversato da più fonti normative che si sovrappongono per livello e funzione.

**Codice civile**: disciplina i tipi di documento con rilevanza probatoria (scrittura privata, riproduzioni meccaniche, atto pubblico). Non fornisce una definizione generale di "documento".

**Legge Bassanini (L. 15 marzo 1997, n. 59, art. 15 c. 2)**: prima norma che riconosce la validità e rilevanza giuridica "a tutti gli effetti di legge" degli atti, dati e documenti formati con strumenti informatici o telematici, dei contratti stipulati nelle medesime forme, e della loro archiviazione e trasmissione.

**CAD — Codice dell'Amministrazione Digitale (D.Lgs. 7 marzo 2005, n. 82)**: disciplina l'impiego delle nuove tecnologie nella pubblica amministrazione. Le regole relative a documenti informatici, firme elettroniche, pagamenti informatici, libri e scritture si applicano **anche ai privati**.

**Regole tecniche (D.P.C.M. 22 febbraio 2013)**: "Regole tecniche in materia di generazione, apposizione e verifica delle firme elettroniche avanzate, qualificate e digitali".

**Regolamento eIDAS (Reg. CE 910/2014)**: disciplina il riconoscimento dei mezzi di identificazione elettronica tra Stati membri e stabilisce le norme relative ai servizi fiduciari. Istituisce un quadro giuridico per firme elettroniche, sigilli elettronici, validazioni temporali elettroniche, documenti elettronici, servizi di recapito certificato e certificati di autenticazione di siti web.

**Linee Guida AGID**: sulla formazione, gestione e conservazione dei documenti informatici.

---

## §2 — Il Concetto di Documento

L'ordinamento giuridico italiano non prevede una vera e generale definizione di "documento". Il **codice civile** ne **definisce e regola** solo **alcuni tipi specifici**:

- **Scritture private** (artt. 2702-2708)
- **Riproduzioni meccaniche** (art. 2712)
- **Atti pubblici** (artt. 2699-2701)

Per distinguerli, puoi chiederti:
- È stato redatto da un pubblico ufficiale? → **Atto Pubblico**
- È stato firmato dalle parti interessate? → **Scrittura Privata**
- Ha valore di prova legale in quanto documento ufficiale? → **Atto Pubblico**
- Ha valore di prova legale solo se firmato dalle parti? → **Scrittura Privata**

### Scrittura privata (art. 2702 c.c.)
Fa piena prova, fino a querela di falso, della **provenienza** delle dichiarazioni da chi l'ha **sottoscritta**, se colui contro il quale la scrittura è prodotta ne **riconosce** la sottoscrizione, ovvero se questa è **legalmente** considerata come **riconosciuta**. Per essere valida la firma: **non deve essere disconosciuta** durante una causa, oppure deve essere **autenticata**.

### Riproduzioni meccaniche (art. 2712 c.c.)
Le riproduzioni fotografiche, informatiche o cinematografiche formano **piena prova** dei fatti e delle cose rappresentate, se colui contro il quale sono prodotte **non ne disconosce la conformità**.

### Atto pubblico (art. 2699 c.c.)
Il documento redatto, con le richieste formalità, da un **notaio** o da altro **pubblico ufficiale autorizzato** ad attribuirgli **pubblica fede** nel luogo dove l'atto è formato. Può essere contestato solo con querela di falso.

---

## §3 — Dematerializzazione e Documento Informatico

**Documento tradizionale**: contenitore e contenuto sono inscindibili (carta/inchiostro). La firma è apposta sul supporto fisico.

**Documento informatico**: i bit possono essere **trasferiti, riprodotti e memorizzati** su infiniti supporti diversi. Qualsiasi strumento informatico impiegato in luogo della sottoscrizione dovrà essere apposto ai **dati** da sottoscrivere e **non al supporto**. Ad esempio, se si firma un documento con firma digitale, la firma deve essere applicata ai bit del documento stesso, non al file o al disco rigido su cui è memorizzato.

**Definizioni**:
- **Documento informatico**: il documento elettronico che contiene la rappresentazione informatica di atti, fatti o dati giuridicamente rilevanti.
- **Documento elettronico**: qualsiasi contenuto conservato in forma elettronica, in particolare testo o registrazione sonora, visiva o audiovisiva.

Quindi tutti i documenti informatici sono documenti elettronici, ma non sempre viceversa.

A un **documento elettronico non** sono **negati** gli **effetti giuridici** e l'**ammissibilità come prova** in procedimenti giudiziali per il **solo motivo** della sua **forma elettronica**.

---

## §4 — Meccanismo Tecnico della Firma Digitale

La firma digitale si basa su una tecnica di **crittografia asimmetrica** o **a doppia chiave (pubblica/privata)**. Sono impiegate due chiavi diverse, in grado di funzionare solo congiuntamente:

- Il **mittente firma** il documento informatico con la **propria chiave privata** (nota solo a lui).
- Il **destinatario verifica** il documento con la **chiave pubblica del mittente**.

Il meccanismo è applicato non all'intero documento ma a una sua "**impronta digitale**" (stringa di dati che ne sintetizza in modo univoco il contenuto). L'impronta è generata mediante algoritmi, le c.d. "**funzioni di hash**" → garantiscono che sia pressoché impossibile ottenere la stessa impronta partendo da due file di dati diversi. Se il documento è modificato anche di un solo bit, l'algoritmo produrrà due impronte diverse e il destinatario potrà accorgersene.

### La certificazione
La firma digitale di per sé non è in grado di garantire la reale identità del firmatario: questi potrebbe firmare a nome di un terzo o con un nome inventato. È previsto l'intervento di "terze parti fidate", i c.d. **certificatori**, che:
- verificano l'**identità** di un soggetto,
- la associano a una **chiave pubblica** di cifratura,
- **attestano** tali informazioni mediante l'emissione di un **certificato**,
- **pubblicano** tempestivamente **revoca** e **sospensione** del certificato in apposite **liste**.

---

## §5 — Validità ed Efficacia Probatoria del Documento Informatico

Il documento informatico soddisfa il requisito della **forma scritta** e ha l'efficacia di **scrittura privata** (art. 2702 c.c.) quando:

- vi è apposta una **firma digitale**, altro tipo di **firma elettronica qualificata** o una **firma elettronica avanzata**; oppure
- è formato, previa **identificazione informatica** del suo **autore**, attraverso un processo che garantisca la **sicurezza, integrità** e **immodificabilità** del documento e, in maniera manifesta e inequivoca, la sua **riconducibilità all'autore**.

In **tutti gli altri casi**, l'idoneità del documento informatico a soddisfare il requisito della **forma scritta** e il suo **valore probatorio** sono **liberamente valutabili in giudizio**, in relazione alle caratteristiche di sicurezza, integrità e immodificabilità.

La **data** e l'**ora** di formazione del documento informatico sono **opponibili ai terzi** se apposte in conformità alle **Linee guida**.

### IMPORTANTE — Macroistuzioni e codici eseguibili

Il documento informatico sottoscritto con firma elettronica qualificata o digitale **NON** soddisfa il requisito di **immodificabilità** del documento se contiene **macroistuzioni, codici eseguibili** o altri elementi tali da attivare funzionalità che possano **modificare** gli atti, i fatti o i dati nello stesso rappresentati. (art. 4, c. 3 reg. tecn.)

Esempi di elementi che invalidano l'immodificabilità:
- Macro in Word o Excel
- Script in PDF
- Codice JavaScript o VBScript in un documento Office

---

## §6 — Casistiche Giurisprudenziali: La E-mail

**Tribunale di Foggia, 27 novembre 2014**: la corrispondenza intercorsa via e-mail *può* costituire prova scritta, ex art. 2712 c.c., e quindi formare piena prova dei fatti o delle cose rappresentati, **se colui contro il quale sono prodotte non ne disconosce la conformità**. Attenzione: altri tribunali non hanno accettato le e-mail come prova.

**Tribunale di Prato, 15/4/2011**: la e-mail semplice (non PEC) è stata considerata inidonea a identificare univocamente il mittente e a provare la ricezione del messaggio. Tuttavia, la e-mail è stata considerata documento informatico con firma elettronica, in quanto username e password sono dati utilizzati per l'identificazione informatica.

---

## §7 — Copie Informatiche e Analogiche

### Copie informatiche di documenti analogici
I documenti informatici contenenti copia di atti pubblici, scritture private e documenti in genere, compresi gli atti formati **in origine su supporto analogico**, hanno **piena efficacia** (ai sensi artt. 2714 e 2715 c.c.) se vi è apposta una **firma digitale o altra firma elettronica qualificata o avanzata**. La loro esibizione e produzione **sostituisce** quella dell'originale.

La **copia per immagine** (scansione) su supporto informatico di un documento analogico è prodotta mediante processi e strumenti che assicurano che il documento informatico abbia **contenuto e forma identici a quelli del documento analogico** da cui è tratto, previo raffronto dei documenti o attraverso **certificazione di processo**.

Le copie per immagine hanno la stessa efficacia probatoria degli originali:
- se la loro conformità è attestata da un **notaio o altro pubblico ufficiale** a ciò autorizzato; oppure
- se la loro conformità **non è espressamente disconosciuta**.

> **Imprecisione corretta**: negli appunti grezzi compariva la nota "si può dubitare" accanto alla condizione del "non disconoscimento". Quella nota non è tecnicamente errata come intuizione, ma la legge non prevede un regime di dubbio aggiuntivo: se la conformità non viene espressamente disconosciuta, la copia ha piena efficacia probatoria, punto. La possibilità di contestare esiste come in ogni caso processuale, ma non è una caratteristica specifica di questa norma.

### Copie analogiche di documenti informatici
Le copie analogiche di documenti informatici hanno la stessa efficacia probatoria dell'originale se:
- la conformità è attestata da un **pubblico ufficiale** autorizzato; oppure
- le copie conformi alle regole tecniche non vengono **espressamente disconosciute**.

Sulle copie analogiche può essere apposto a stampa un **contrassegno**, col quale è possibile accedere al documento informatico o verificare la corrispondenza della copia. Il contrassegno **sostituisce** a tutti gli effetti la **sottoscrizione autografa** del pubblico ufficiale.

### Duplicati informatici
I **duplicati informatici** (copie informatiche di documenti informatici) hanno lo **stesso valore giuridico** del documento originale, ad ogni effetto di legge, se prodotti in **conformità** alle **Linee Guida**.

---

## §8 — Conservazione e Trasmissione dei Documenti Informatici

I libri, repertori e scritture di cui sia **obbligatoria la tenuta** possono essere formati e conservati su **supporti informatici** in conformità al CAD e secondo le Linee Guida.

Gli obblighi di conservazione e di esibizione di documenti sono soddisfatti a tutti gli effetti di legge a mezzo di **documenti informatici**, se le procedure sono effettuate in modo tale da garantire la **conformità** ai documenti originali e sono conformi alle Linee guida.

I documenti informatici conservati per legge da pubbliche amministrazioni, gestori di servizi pubblici, ecc. **non devono essere obbligatoriamente conservati anche dal cittadino e dalle imprese**, che possono in ogni momento richiedere accesso al documento agli stessi soggetti.

### Trasmissione informatica
Il documento informatico inviato telematicamente si intende:
- **spedito dal mittente** se inviato al proprio gestore;
- **consegnato al destinatario** se reso disponibile all'indirizzo elettronico da questi dichiarato.

I documenti trasmessi da chiunque ad una PA con qualsiasi **mezzo telematico o informatico, idoneo** ad accertarne la provenienza, soddisfano il requisito della **forma scritta** e la loro trasmissione **non deve essere seguita** da quella del **documento originale**.

### La PEC — Posta Elettronica Certificata
L'invio telematico di comunicazioni che necessitano di una **ricevuta di invio** e **di consegna** avviene mediante **posta elettronica certificata** (DPR 68/2005).

La trasmissione del documento informatico per via telematica mediante **PEC** equivale, salvo che la legge disponga diversamente, alla **notificazione a mezzo posta**. **Data e ora** di trasmissione e ricezione mediante PEC sono **opponibili ai terzi** se conformi alla normativa vigente, incluse le regole tecniche.

---

## §9 — Le Firme Elettroniche: Tipologie

### Firma elettronica (semplice)
"Dati in forma **elettronica**, **acclusi** oppure **connessi** tramite associazione logica ad **altri dati elettronici** e utilizzati dal firmatario per **firmare**." (eIDAS)

### Firma elettronica avanzata
Una firma elettronica che:
a) è **connessa unicamente** al **firmatario**;
b) è **idonea a identificare** il **firmatario**;
c) è creata mediante dati che il firmatario può, con un elevato livello di sicurezza, **utilizzare sotto il proprio esclusivo controllo**;
d) è **collegata ai dati sottoscritti** in modo da **consentire l'identificazione** di ogni **successiva modifica** di tali dati.

### Firma elettronica qualificata

> **Imprecisione corretta**: negli appunti grezzi la firma qualificata veniva definita genericamente come "una firma elettronica avanzata che soddisfa requisiti più stringenti di sicurezza e autenticità". Questa definizione è incompleta. La definizione normativa corretta (eIDAS) specifica i **due elementi costitutivi precisi**:

La firma elettronica qualificata è una **firma elettronica avanzata** che è:
- **creata** da un **dispositivo per la creazione di una firma elettronica qualificata**, e
- **basata** su un **certificato qualificato** per firme elettroniche.

Il "dispositivo qualificato" e il "certificato qualificato" sono requisiti specifici e non generici "requisiti più stringenti": senza entrambi, la firma non è qualificata.

### Firma digitale
Un particolare **tipo** di **firma qualificata** basata su un sistema di **chiavi crittografiche**, una **pubblica** e una **privata**, correlate tra loro, che consente al titolare tramite la chiave privata e a un soggetto terzo tramite la chiave pubblica, rispettivamente, di rendere manifesta e di verificare la **provenienza** e l'**integrità** di un documento informatico o di un insieme di documenti informatici. (CAD, art. 1)

### Schema riassuntivo

> **Domanda aperta risolta**: "(inserisci lo schema)" — schema delle tipologie di firme elettroniche:

| Tipo | Definizione sintetica | Valore giuridico |
|------|----------------------|-----------------|
| Firma elettronica (semplice) | Qualsiasi dato elettronico usato per firmare | Non negati effetti giuridici né ammissibilità come prova |
| Firma elettronica avanzata | Connessa univocamente al firmatario, sotto suo esclusivo controllo, identifica ogni modifica | Scrittura privata (art. 2702 c.c.) |
| Firma elettronica qualificata | Avanzata + **dispositivo qualificato** + **certificato qualificato** | Equivalente a firma autografa |
| Firma digitale | Tipo specifico di qualificata italiana, basata su chiavi crittografiche (CAD, art. 1) | Equivalente a firma autografa |
| Firma automatica | Qualificata/digitale eseguita previa autorizzazione, senza presidio continuo del firmatario | Come la tipologia su cui si basa |
| Firma remota | Qualificata/digitale generata su HSM, garantisce controllo esclusivo delle chiavi | Come la tipologia su cui si basa |
| Firma autenticata | Qualsiasi firma elettronica (anche avanzata) autenticata da notaio o pubblico ufficiale | Equivalente a firma autografa con certezza legale rafforzata |

> **Domanda aperta risolta**: "(questi successivi tipi di firma, integrali nella tabella delle firme antecedente)" — integrati sopra. Firma automatica, remota e autenticata sono **modalità operative** di firma qualificata/digitale, non tipi autonomi nella gerarchia eIDAS. Sono incluse nella tabella come riga separata per chiarezza.

### Effetti giuridici delle firme elettroniche
A una **firma elettronica non possono** essere **negati** gli **effetti giuridici** e l'**ammissibilità come prova** in procedimenti giudiziali per il **solo motivo** della sua **forma elettronica** o perché non soddisfa i requisiti per firme elettroniche **qualificate**.

Una **firma elettronica qualificata** ha effetti giuridici equivalenti a quelli di una **firma autografa**.

Una firma elettronica qualificata basata su un certificato qualificato rilasciato in uno Stato membro è riconosciuta quale firma elettronica qualificata in tutti gli altri Stati membri.

---

## §10 — Firma Digitale: Dettaglio

La FD deve riferirsi in modo univoco **a un solo soggetto** e al **documento** (o insieme di documenti) cui è apposta o associata. Integra e sostituisce sigilli, punzoni, timbri, contrassegni e marchi di qualsiasi genere.

Per generare la FD deve essere impiegato un **certificato qualificato non scaduto, non revocato o sospeso** al momento della firma. Dal certificato qualificato devono risultare la validità, gli estremi identificativi del titolare e del certificatore ed **eventuali limiti d'uso**.

### Conseguenze del certificato invalido
L'apposizione di una **firma digitale** o di un altro tipo di **firma elettronica qualificata** basata su un certificato elettronico **revocato, scaduto** o **sospeso** equivale a **mancata sottoscrizione**, salvo che lo stato di sospensione sia stato annullato.

La **revoca o la sospensione**, comunque motivate, hanno **effetto dal momento della pubblicazione**, salvo che il revocante non dimostri che essa era già a conoscenza di tutte le parti interessate.

### Applicazione transfrontaliera (firme digitali straniere)
Le regole sulla firma digitale si applicano anche se la firma elettronica è basata su un certificato qualificato rilasciato da un certificatore **non UE**, quando ricorre una delle seguenti condizioni:
1. il certificatore possiede i requisiti eIDAS ed è qualificato in uno Stato membro;
2. il certificato qualificato è garantito da un certificatore stabilito nell'UE con requisiti eIDAS;
3. il certificato qualificato o il certificatore è riconosciuto in forza di un **accordo bilaterale o multilaterale** tra UE e Paesi terzi.

### IMPORTANTE — Valore delle firme qualificate e digitali nel tempo
Le firme elettroniche qualificate e digitali, anche se è scaduto, revocato o sospeso il relativo certificato qualificato, sono **valide** se alle stesse è associabile un **riferimento temporale opponibile ai terzi** che colloca la generazione di dette firme in un **momento precedente** alla scadenza, revoca o sospensione del certificato. (regole tecniche, art. 62)

---

## §11 — Firma Automatica, Remota e Autenticata

> ⚠️ Questa sezione non era presente negli appunti grezzi.

**Firma automatica**: particolare procedura informatica di firma elettronica qualificata o di firma digitale eseguita previa autorizzazione del sottoscrittore che mantiene il controllo esclusivo delle proprie chiavi di firma, **in assenza di presidio puntuale e continuo** da parte di questo. Esempio: firma in batch di documenti multipli (es. fatturazione automatizzata).

**Firma remota**: particolare procedura di firma elettronica qualificata o di firma digitale, generata su **HSM** (Hardware Security Module — insieme di hardware e software che realizza dispositivi sicuri per la generazione delle firme), che consente di garantire il controllo esclusivo delle chiavi private da parte dei titolari. Il firmatario accede alle proprie chiavi da remoto tramite il dispositivo HSM custodito dal prestatore.

### Firma autenticata
La firma elettronica o la firma elettronica avanzata può essere **autenticata** da: notaio o altro pubblico ufficiale autorizzato.

**Autenticazione** (cosa fa il pubblico ufficiale):
- accertamento dell'**identità** personale del firmatario;
- attestazione che la **firma** è stata apposta **in sua presenza**;
- accertamento della **validità** dell'eventuale **certificato elettronico**;
- accertamento che il documento sottoscritto **non è contrario all'ordinamento giuridico**.

---

## §12 — Il Certificato Qualificato

**Certificato di firma elettronica**: attestato elettronico che collega i dati di convalida di una firma elettronica a una **persona fisica** e conferma almeno il nome o lo pseudonimo.

**Certificato qualificato di firma elettronica**: certificato di firma elettronica rilasciato da un **prestatore di servizi fiduciari qualificato** e conforme ai requisiti dell'allegato I del Regolamento eIDAS.

### Contenuto del certificato qualificato
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

Il **certificatore** determina il **periodo di validità dei certificati qualificati** anche in funzione della robustezza crittografica delle chiavi. L'**AGID** determina il **periodo massimo** in funzione degli algoritmi e delle caratteristiche delle chiavi.

### Revoca e sospensione del certificato qualificato

> **Domanda aperta risolta**: "(spiega più semplicemente la revoca e sospensione del certificato qualificato)"
>
> **Revoca** = cancellazione definitiva. **Sospensione** = blocco temporaneo, reversibile. Entrambe devono essere pubblicate immediatamente, perché la data di pubblicazione è l'**effetto** della revoca/sospensione: nessuno può opporsi a una revoca che non sia stata pubblicata.
>
> **Quando il certificatore è obbligato a revocare/sospendere:**
> 1. **Cessazione** dell'attività del certificatore (salvo trasferimento a un certificatore sostitutivo) → solo revoca
> 2. **Provvedimento dell'autorità** (es. autorità giudiziaria o AgID) → revoca o sospensione
> 3. **Richiesta del titolare** o del soggetto da cui derivano i poteri del titolare → revoca o sospensione
> 4. **Cause limitative della capacità** del titolare, o **abusi o falsificazioni** → revoca o sospensione
>
> **Regola di pubblicità**: i certificati sospesi e revocati **devono essere resi pubblici**; i certificati qualificati attivi **possono** essere resi accessibili al pubblico su **richiesta del titolare**. Chiunque ha diritto di sapere se a proprio nome sia stato rilasciato un certificato qualificato.
>
> **Effetto dalla pubblicazione**: la revoca/sospensione ha effetto dal momento della pubblicazione della lista, salvo che il revocante dimostri che la notizia era già nota a tutte le parti interessate. Questo significa che se la revoca non è ancora pubblicata, la firma resta valida per i terzi in buona fede.

---

## §13 — Il Sigillo Elettronico

Il **sigillo elettronico** è lo strumento equivalente alla firma elettronica ma per le **persone giuridiche** (non persone fisiche). Definito dal Regolamento eIDAS, art. 3.

| Tipo | Definizione |
|------|-------------|
| **Sigillo elettronico** | Dati in forma elettronica, acclusi o connessi ad altri dati elettronici, per garantire l'**origine** e l'**integrità** di questi ultimi |
| **Sigillo elettronico avanzato** | Connesso al creatore, idoneo a identificarlo, sotto suo controllo, collegato ai dati in modo da identificare ogni modifica |
| **Sigillo elettronico qualificato** | Sigillo avanzato + dispositivo qualificato + certificato qualificato per sigilli |

Un **sigillo elettronico qualificato** gode della **presunzione di integrità** dei **dati** e di **correttezza dell'origine** di quei dati a cui è associato. (eIDAS, art. 35)

---

## §14 — Validazione Temporale

**Validazione temporale elettronica**: dati in forma elettronica che collegano altri dati in forma elettronica a una particolare ora e data, così da **provare che questi ultimi esistevano in quel momento**. (eIDAS, art. 3)

**Marca temporale**: il riferimento temporale che consente la validazione temporale e che dimostra l'esistenza di un'evidenza informatica in un **tempo certo**. (regole tecniche, art. 1)

**Riferimento temporale**: evidenza informatica, contenente la data e l'ora, che viene associata ad uno o più documenti informatici. (regole tecniche, art. 1)

I **riferimenti temporali** realizzati dai certificatori accreditati in conformità alle **regole tecniche** sono **opponibili ai terzi**.

Costituiscono validazione temporale i riferimenti temporali ottenuti con l'utilizzo della **PEC**. (regole tecniche, art. 41)

> **Perché conta la validazione temporale**: in combinazione con il principio del §10 (valore delle firme nel tempo), la marca temporale è lo strumento concreto per dimostrare che una firma qualificata/digitale è stata apposta *prima* che il relativo certificato venisse revocato o scaduto. Senza un riferimento temporale opponibile ai terzi, una firma apposta su un certificato poi revocato equivale a mancata sottoscrizione — anche se al momento della firma il certificato era valido.

---

## §15 — I Servizi Fiduciari e i Prestatori

**Servizio fiduciario**: un servizio elettronico fornito normalmente dietro remunerazione, consistente in: creazione, verifica e convalida di firme/sigilli/validazioni temporali elettroniche; creazione, verifica e convalida di certificati di autenticazione di siti web; o conservazione di firme, sigilli o certificati elettronici. (eIDAS, art. 3)

**Servizio fiduciario qualificato**: un servizio fiduciario che soddisfa i requisiti pertinenti stabiliti nel Regolamento.

### Accreditamento
I soggetti che intendono prestare servizi fiduciari qualificati o svolgere l'attività di gestore di PEC, di gestore dell'identità digitale, di conservatore di documenti informatici, presentano all'**AgID** domanda di qualificazione o di accreditamento, allegando una relazione di valutazione della conformità rilasciata da un organismo accreditato. (CAD, art. 29)

Requisiti: natura giuridica di **società di capitali**, requisiti di onorabilità, tecnologici e organizzativi, garanzie assicurative.

### Responsabilità
I prestatori di servizi fiduciari qualificati che cagionano **danno** ad altri nello svolgimento della loro attività, sono tenuti al **risarcimento**, **se non provano** di avere adottato tutte le **misure idonee a evitare il danno**. (responsabilità per inversione dell'onere della prova)

Il certificato qualificato può contenere **limiti d'uso o di valore**: il **certificatore non è responsabile** dei danni derivanti dall'uso di un certificato qualificato che ecceda i limiti posti, purché i limiti siano chiaramente evidenziati nel certificato.

### Obblighi del titolare del certificato (CAD, art. 32)
Il titolare del certificato di firma è tenuto a:
- assicurare la **custodia** del dispositivo di firma;
- adottare **tutte le misure organizzative e tecniche idonee** ad evitare danno ad altri;
- **utilizzare personalmente** il dispositivo di firma.

### Conservazione delle chiavi
Le chiavi private possono essere conservate in un dispositivo di firma (es. smart card, chiavetta USB).

La **chiave privata** e il **dispositivo non possono essere duplicati**. Devono essere conservati **con diligenza**, garantendo integrità e riservatezza. Le **informazioni di abilitazione** alla chiave privata vanno conservate in **luogo diverso** dal **dispositivo**.

**Necessario richiedere immediatamente la revoca** se si è perso il possesso del dispositivo contenente la chiave privata o se si ha il dubbio che sia stato utilizzato da persone non autorizzate.

### Obblighi del prestatore di servizi di firma elettronica qualificata (CAD, art. 32)
- **Identificare con certezza** la persona che fa richiesta della certificazione.
- Rilasciare e **rendere pubblico il certificato elettronico** nei modi stabiliti dalle regole tecniche.
- **Pubblicare tempestivamente** la revoca e la sospensione del certificato.
- Assicurare la **precisa determinazione della data e dell'ora** di rilascio, di revoca e di sospensione dei certificati.
- Tenere **registrazione** di tutte le informazioni relative al certificato qualificato dal momento della sua emissione **almeno per 20 anni** (ai fini di prova in eventuali procedimenti giudiziari).
- **Non copiare, né conservare**, le **chiavi private di firma dei clienti**.
- Il prestatore è **responsabile** dell'**identificazione** del soggetto che richiede il certificato qualificato **anche se tale attività è delegata a terzi**.

---

## §16 — Tutela della Segretezza

Per gli atti, dati e documenti informatici inviati telematicamente è prevista una **tutela di segretezza** analoga a quella della corrispondenza cartacea.

Gli **addetti alla trasmissione non** hanno il diritto di prendere cognizione della corrispondenza telematica, **duplicare** o **cedere a terzi** informazioni anche in forma sintetica sull'esistenza o sul contenuto di corrispondenza telematica, salvo che si tratti di informazioni destinate ad essere rese pubbliche.

Gli atti, i dati e i documenti trasmessi per via **telematica** si considerano, **nei confronti del gestore** del sistema di trasporto, di **proprietà del mittente sino a che** non sia avvenuta la **consegna al destinatario**. (CAD, art. 49)

---

## §17 — SPID e Istanze alle PA

**SPID — Sistema Pubblico delle Identità Digitali**: istituito a cura dell'Agenzia per l'Italia digitale, è un insieme aperto di soggetti pubblici e privati che, previo accreditamento da parte dell'AgID, identificano gli utenti per consentire loro l'accesso ai servizi in rete. L'accesso può avvenire anche con la **carta di identità elettronica** e la **carta nazionale dei servizi**.

**Istanze e dichiarazioni alle PA** inviate per via telematica sono valide se:
- sottoscritte con **firma digitale o firma elettronica qualificata**, il cui certificato è rilasciato da un certificatore qualificato;
- l'autore è identificato con il sistema **SPID, la carta di identità elettronica** o la **carta nazionale dei servizi**;
- sottoscritte e presentate con un **documento di identità**;
- trasmesse dal proprio **domicilio digitale** purché le credenziali di accesso siano state rilasciate previa identificazione del titolare.

Le istanze così presentate sono **equivalenti** alle istanze sottoscritte con **firma autografa** apposta in presenza del dipendente addetto al procedimento. (CAD, art. 65)

---

## §18 — Riferimenti Normativi Riepilogo

> ⚠️ Questa sezione non era presente negli appunti grezzi.

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

## Domande di Autoverifica — Risposte

> ⚠️ Le risposte alle domande di autoverifica non erano presenti negli appunti grezzi. Le domande sono da rispondere in autonomia prima di portare il modulo a ✅.

**Domanda 1**: Qual è la differenza tra firma elettronica semplice, firma elettronica avanzata, firma elettronica qualificata e firma digitale? Definisci ciascuna nelle parole del PDF.

**Domanda 2**: Quando un documento informatico ha l'efficacia della scrittura privata ai sensi dell'art. 2702 c.c.? Cosa succede "in tutti gli altri casi"?

**Domanda 3**: Cosa sono la marca temporale e il riferimento temporale? Perché il valore delle firme qualificate e digitali "nel tempo" è rilevante?

**Domanda 4**: Quali sono gli obblighi principali del prestatore di servizi di firma elettronica qualificata nei confronti del titolare e dei terzi? Quale responsabilità ha se cagiona un danno?

**Domanda 5**: Cosa accade se un documento informatico sottoscritto con firma digitale contiene macroistuzioni o codici eseguibili? Cita la norma di riferimento.

---

## Attenzione Ripasso (dalla professoressa — slide 66-67)

Temi prioritari per l'esame segnalati esplicitamente:
- Scrittura privata, sottoscrizione autografa, atto pubblico, riproduzioni meccaniche
- Tecnologia e meccanismo di firma digitale
- Certificazione (cosa è e a cosa serve)
- **FIRMA ELETTRONICA SEMPLICE, AVANZATA, QUALIFICATA E DIGITALE**
- Certificato qualificato (i punti essenziali)
- **VALIDITA' DEL DOCUMENTO INFORMATICO**
- **MACROISTUZIONI nel documento informatico**
- Cosa succede se il certificato della firma è revocato o sospeso?
- Copie analogiche di documenti informatici e copie informatiche di originali cartacei
- **TRASMISSIONE del documento informatico**
- **La PEC**
- I prestatori di servizi fiduciari: cosa sono, compiti e responsabilità
- Obblighi del titolare e del prestatore
- **Valore delle firme qualificate e digitali nel TEMPO**

<!-- AUTO-LINKS:START -->
## 🔗 Collegati

- [[Appunti_moduloD9]]
- [[lezione_moduloD9_firme_elettroniche]]
- [[speedreview_D09_firme_elettroniche]]

**Hub:** [[master_map_studio]] · [[glossario_diritto]] · [[concept_maps]]
<!-- AUTO-LINKS:END -->
