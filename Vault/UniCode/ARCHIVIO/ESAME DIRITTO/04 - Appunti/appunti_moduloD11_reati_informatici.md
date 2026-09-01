# Appunti — Modulo D11: I Reati Informatici
**Corso**: Diritto dell'Informatica T
**PDF**: `11_DirInfo_2026_ReatiInformatici_DEF.pdf`
**Normative**: Legge 23 dicembre 1993 n. 547; Convenzione di Budapest 23/11/2001; Legge 18 marzo 2008 n. 48; Codice penale (artt. 392, 615-ter, 615-quater, 615-quinquies, 616, 617-quater, 617-quinquies, 617-sexies, 621, 635-bis, 635-ter, 635-quater, 635-quinquies, 640-ter)

---

## Obiettivo

Muoversi giuridicamente all'interno delle differenze tra le varie condotte informatiche illecite: identificare il reato corretto, distinguere le figure affini, e conoscere i criteri di aggravamento delle pene.

---

## Quadro Normativo

> ⚠️ Questa sezione non era presente negli appunti grezzi.

Il diritto penale italiano disciplina i reati informatici attraverso due interventi legislativi principali:

- **Legge 23 dicembre 1993, n. 547** — Prima legge italiana sulla criminalità informatica: introduce nel codice penale i reati informatici modificando e integrando le norme esistenti. [fonte: PDF]
- **Convenzione di Budapest del 23 novembre 2001** — Primo trattato internazionale sulla cybercriminalità, promosso dal Consiglio d'Europa. [fonte: PDF]
- **Legge 18 marzo 2008, n. 48** — Ratifica la Convenzione di Budapest e adegua l'ordinamento interno, modificando alcuni articoli del codice penale. [fonte: PDF]

---

## §1 — Elementi Generali

**Reato** = illecito penale, sanzionato con pene **pecuniarie** (multa) e/o **detentive** (reclusione). [fonte: PDF]

I **reati informatici** possono essere commessi:
- **mediante** tecnologie informatiche
- **a danno di** tecnologie informatiche

Distinzione fondamentale: [fonte: PDF]

| Tipo | Definizione | Esempio |
|------|-------------|---------|
| **Eventualmente informatici** | L'elemento informatico è una modalità accidentale — il reato esiste anche senza | Truffa online: è truffa anche commessa di persona |
| **Necessariamente informatici** | La presenza dell'elemento informatico è **necessaria** perché sussista il reato | Accesso abusivo (art. 615-ter): senza sistema informatico non esiste |

> ⚠️ Art. 392 c.p. (violenza sulle cose) — collocazione: questo articolo appartiene alla prima categoria ("eventualmente informatico") perché il reato esiste anche su cose fisiche; la legge lo estende ai programmi informatici. Tutti gli altri articoli del modulo sono "necessariamente informatici". Va qui, come punto di partenza, non in coda.

---

## §2 — Accesso Abusivo a un Sistema Informatico (!) — Art. 615-ter c.p.

**Definizione**: chiunque **abusivamente si introduce** in un **sistema informatico o telematico** **protetto da misure di sicurezza**, ovvero **vi si mantiene contro la volontà espressa o tacita** di chi ha diritto di escluderlo. È punito con la reclusione fino a 3 anni. [fonte: PDF]

Il reato è di **mera condotta** e si **perfeziona** con la **violazione del domicilio informatico**. Non è necessario che l'intrusione sia effettuata allo scopo di ledere la riservatezza degli utenti. [fonte: PDF — Cass. 6/2/2006]

L'**abusività** va intesa in **senso oggettivo** — conta **come** si è entrati, non **perché**: a nulla rilevano le finalità dell'autore e l'uso successivo dei dati, che, se illeciti, possono integrare un diverso titolo di reato. [fonte: PDF — Cass. 25/06/2009]

### Il caso dell'utente autorizzato

> **(Domanda: spiega con esempi — non capisco quando commette, non commette, integra)**
>
> La giurisprudenza è genuinamente oscillante. Il modo più chiaro per uscirne è capire la logica sottostante a tre sentenze apparentemente contraddittorie:
>
> **Cass. 8/7/2008 (rv. 241202)** — COMMETTE il reato: un dipendente accede al sistema aziendale con le sue credenziali legittime, ma scarica dati riservati per passarli a un concorrente. → L'accesso aveva titolo, ma il sistema viene usato per **finalità diverse da quelle consentite**. L'accesso stesso era "fuori dai limiti" → 615-ter.
>
> **Cass. 13/2/2009** — INTEGRA il reato: un poliziotto accede alla banca dati interforze (ci ha accesso per lavoro) con la password di servizio, ma scarica notizie riservate per venderle a un'agenzia investigativa. → Accesso autorizzato, ma raccoglie **dati protetti per finalità estranee alle ragioni di istituto** → 615-ter.
>
> **Cass. 8/10/2008** — NON COMMETTE il reato (ma ne commette altri): un addetto alla cancelleria della Corte di Cassazione, regolarmente autorizzato, consulta lo stato dei procedimenti per passare informazioni a detenuti. → L'accesso era perfettamente regolare, consultava dati a cui aveva legittimamente accesso. Il 615-ter non scatta. Ma i reati che derivano dall'uso illecito di quelle informazioni (es. favoreggiamento) scattano eccome.
>
> **Il criterio pratico**: chiedi "l'accesso era già di per sé abusivo (superavo misure di sicurezza, accedevo a sezioni vietate, raccoglievo dati protetti che non competono alla mia funzione)?" → Sì → 615-ter. "Oppure l'accesso era regolare e il problema è solo ciò che ho fatto dopo con le informazioni?" → No 615-ter, ma altri reati per le condotte successive.

### Duplicazione dei dati

> **(Domanda: come si comporta la duplicazione dei dati quando so che è legale backuppare dati privati per finalità lavorative necessarie?)**
>
> La risposta dipende da **chi ha fatto cosa e con quale titolo**:
>
> **Caso 1 — Backup legittimo**: sei autorizzato ad accedere ai dati, li copi per finalità lavorative documentabili (es. backup aziendale di routine) → nessun reato. Il titolo di accesso copre anche la copia.
>
> **Caso 2 — Duplicazione abusiva** (Cass. 8/7/2008, rv. 241203): accedi a un sistema (anche abusivamente) e **duplichi** i dati → la duplicazione stessa integra il 615-ter, assorbendo il reato di appropriazione indebita. Non è necessario "rubare" il file originale — bastava copiarlo.
>
> **Caso 3 — Accesso autorizzato, dati protetti**: hai titolo per accedere al sistema ma copi dati che appartengono a una sezione protetta che non ti compete, per finalità estranee all'istituzione → dipende dalla giurisprudenza (Cass. 13/2/2009 dice sì a 615-ter).
>
> **La chiave**: il problema non è "copiare in sé" — è "copiare cosa, con quale titolo, per quali finalità, superando quali misure di sicurezza".

### Aggravanti

**Prima serie** — reclusione da 1 a 5 anni: [fonte: PDF]
1. Commesso da **pubblico ufficiale** o **incaricato di un pubblico servizio** con abuso dei poteri o violazione dei doveri, da **investigatore privato** (anche abusivo), o con **abuso della qualità di operatore del sistema**;
2. Il colpevole usa **violenza sulle cose** o alle **persone**, ovvero è palesamente **armato**;
3. Dal fatto deriva la **distruzione** o il **danneggiamento** del sistema o l'**interruzione** totale o parziale del funzionamento, ovvero la distruzione o il danneggiamento dei dati.

**Seconda serie** — sistemi di interesse pubblico: reclusione da 1 a 5 anni (o da 3 a 8 anni) se i fatti riguardano sistemi di **interesse militare**, **ordine pubblico**, **sicurezza pubblica**, **sanità**, **protezione civile** o comunque di interesse pubblico. [fonte: PDF]

**Procedibilità**: il reato base è **punibile a querela**; negli altri casi si **procede d'ufficio**. [fonte: PDF]

---

## §3 — Detenzione, Diffusione e Installazione Abusiva di Mezzi di Accesso — Art. 615-quater c.p.

Chiunque, al **fine** di procurare a sé o ad altri un **profitto** o di arrecare ad altri un **danno**, abusivamente si procura, detiene, produce, riproduce, diffonde, importa, comunica, consegna, mette in altro modo a disposizione di altri o installa **apparati, strumenti, parti di apparati o di strumenti, codici, parole chiave o altri mezzi idonei all'accesso ad un sistema informatico o telematico** protetto da misure di sicurezza, **oppure comunque fornisce indicazioni o istruzioni idonee al predetto scopo**, è punito con la reclusione sino a due anni e con la multa sino a euro 5.164. [fonte: PDF]

È la norma sui "grimaldelli digitali" — punisce chi possiede o distribuisce strumenti finalizzati a **entrare** abusivamente in un sistema. Non punisce l'entrata in sé (quello è il 615-ter), ma la preparazione o la diffusione degli strumenti per farlo.

**Aggravanti**: reclusione da 1 a 3 anni se commesso in danno di sistemi dello **Stato** o **ente pubblico**, da **pubblico ufficiale** con abuso dei poteri, o da **investigatore privato**. [fonte: PDF]

**Caso pratico** (Cass. 17/12/2004): integra questo reato procurarsi abusivamente il numero seriale di un cellulare altrui per clonarlo — la clonazione realizza un'illecita connessione alla rete di telefonia mobile, che è un sistema telematico protetto. [fonte: PDF]

---

## §4 — Apparecchiature, Dispositivi o Programmi Diretti al Danneggiamento — Art. 615-quinquies c.p.

Chiunque, allo scopo di:
- **danneggiare illecitamente un sistema** informatico o telematico, le informazioni, i dati o i programmi in esso contenuti o ad esso pertinenti, ovvero di
- **favorire l'interruzione, totale o parziale**, o l'**alterazione** del suo funzionamento,

si procura, detiene, produce, riproduce, importa, diffonde, comunica, consegna o mette a disposizione in qualunque modo **apparecchiature, dispositivi, o programmi informatici**, è punito con la reclusione fino a due anni e con la multa sino a euro 10.329. [fonte: PDF]

Questa è la norma su malware, ransomware, strumenti DDoS: punisce chi possiede o distribuisce strumenti **progettati per fare danno**, non per entrare. La differenza con il 615-quater è nello **scopo dello strumento**.

> **(Richiesta: inserisci la tabella tra quater e quinquies)**

| Articolo | Strumento punito | Scopo dello strumento | Analogia |
|----------|-----------------|----------------------|----------|
| **615-quater** | Codici, password, apparati idonei all'**accesso** | Entrare in un sistema protetto | Grimaldello |
| **615-quinquies** | Dispositivi, programmi diretti al **danneggiamento o interruzione** | Fare danno al sistema o ai suoi dati | Malware/bomba |

---

## §5 — Corrispondenza Informatica — Art. 616 c.p.

Per "**corrispondenza**" si intende quella epistolare, telegrafica, telefonica, **informatica** o **telematica**, ovvero effettuata con **ogni altra forma di comunicazione a distanza**. [fonte: PDF]

Condotte punite:
- **prende cognizione** del contenuto di una corrispondenza chiusa, a lui non diretta;
- **sottrae** o **distrae** al fine di prenderne cognizione;
- la **distrugge** o **sopprime**;
- senza giusta causa **rivela** il contenuto — se ne deriva **nocumento**: reclusione fino a 3 anni.

> ⚠️ **Imprecisione corretta**: negli appunti grezzi il termine usato era "danno". Il termine giuridico preciso è **nocumento** — è la parola del PDF. Nocumento e danno non sono sinonimi: nocumento indica un pregiudizio giuridicamente rilevante, non qualsiasi tipo di disagio. Conta il termine esatto, non la parafrasi.

Il reato è **punibile a querela**: l'autorità giudiziaria non può procedere se la persona offesa non presenta querela. [fonte: PDF]

**Caso pratico** (Cass. 11/12/2007): non integra il reato il superiore gerarchico che prenda cognizione della posta elettronica contenuta nel computer del dipendente assente dal lavoro, dopo aver utilizzato la password comunicatagli in conformità al protocollo aziendale. [fonte: PDF]

---

## §6 — Intercettazione di Comunicazioni Informatiche — Art. 617-quater c.p.

> ⚠️ **Titolo corretto**: il reato si chiama "Intercettazione, impedimento o interruzione illecita di comunicazioni informatiche o telematiche" — non "Rivelazione di Intercettazioni". La rivelazione è solo una delle condotte punite dallo stesso articolo.

Chiunque **fraudolentemente intercetta** comunicazioni relative ad un sistema informatico o telematico o intercorrenti tra più sistemi, ovvero le **impedisce** o le **interrompe**, è punito con la reclusione da un anno e sei mesi a cinque anni. [fonte: PDF]

La stessa pena si applica a chiunque **rivela** mediante qualsiasi mezzo di informazione al pubblico, in tutto o in parte, il contenuto delle comunicazioni intercettate. [fonte: PDF]

Punibile a **querela**; si **procede d'ufficio** con pena più grave (reclusione da 3 a 8 anni) se commesso in danno di sistemi dello Stato/ente pubblico, da pubblico ufficiale, o da investigatore privato. [fonte: PDF]

---

## §7 — Apparecchiature per Intercettare — Art. 617-quinquies c.p.

Chiunque, fuori dai casi consentiti dalla legge, al fine di intercettare, impedire o interrompere comunicazioni informatiche, si procura, detiene, produce, riproduce, diffonde, importa, comunica, consegna, mette in altro modo a disposizione di altri o installa **apparecchiature, programmi, codici, parole chiave o altri mezzi atti ad intercettare, impedire o interrompere comunicazioni** relative ad un sistema informatico o telematico, è punito con la reclusione da uno a quattro anni. [fonte: PDF]

**Caso pratico** (Cass. 9/11/2007): l'utilizzazione di apparecchiature capaci di copiare i codici di accesso degli utenti di un sistema informatico integra questo reato — la copiatura abusiva dei codici di accesso per la prima comunicazione con il sistema rientra nella nozione di "intercettare". [fonte: PDF]

---

## §8 — Falsificazione di Comunicazioni Informatiche — Art. 617-sexies c.p.

Chiunque, al **fine** di procurare a sé o ad altri un **vantaggio** o di arrecare ad altri un **danno**, **forma falsamente** ovvero **altera** o **sopprime**, in tutto o in parte, il **contenuto**, **anche occasionalmente intercettato**, di taluna delle **comunicazioni** relative ad un sistema informatico o telematico, è punito — qualora ne faccia uso o lasci che altri ne facciano uso — con la reclusione da uno a quattro anni. Punibile a querela. [fonte: PDF]

Pena aggravata (1-5 anni) nei casi di sistemi pubblici o commesso da pubblico ufficiale/investigatore privato. [fonte: PDF]

---

## §9 — Rivelazione del Contenuto di Documenti Segreti — Art. 621 c.p.

Chiunque, essendo venuto **abusivamente** a cognizione del contenuto, che debba rimanere segreto, di altrui atti o documenti, pubblici o privati, non costituenti corrispondenza, lo **rivela**, senza giusta causa, o **lo impiega a proprio o altrui profitto**, è **punito, se dal fatto deriva nocumento**, con la reclusione fino a tre anni o con la multa. [fonte: PDF]

Ai fini di questo articolo è considerato **documento anche qualunque supporto informatico contenente dati, informazioni o programmi**. [fonte: PDF]

Si è punibili solo se il **nocumento** è provato: è condizione oggettiva di punibilità. La rivelazione non è ciò che fa scattare la pena — è il danno giuridicamente rilevante che ne deriva. Se non produce nocumento al titolare del diritto alla segretezza, il reato non sussiste neanche in forma tentata. [fonte: PDF — Cass. 16/01/2009]

Punibile a querela. [fonte: PDF]

---

## §10 — Danneggiamento Informatico: la Famiglia di Reati

> **(Richiesta: inserisci la tabella)**

La famiglia è strutturata su **due assi**: cosa viene danneggiato × chi subisce il danno.

| Articolo | Oggetto del danno | Soggetto passivo | Pena base |
|----------|-------------------|------------------|-----------|
| **635-bis** | **Dati, programmi** informatici | Privato | 6 mesi – 3 anni |
| **635-ter** | **Dati, programmi** informatici | Stato / ente pubblico / pubblica utilità | 1 – 4 anni |
| **635-quater** | **Sistemi** informatici o telematici | Privato | 1 – 5 anni |
| **635-quinquies** | **Sistemi** informatici o telematici | Pubblica utilità | 1 – 4 anni (o 3–8 se inservibile) |

In base all'oggetto del danno distinguo tra **dati/programmi** (635-bis/ter) e **sistemi** (635-quater/quinquies); in base al soggetto passivo distinguo tra **privato** (635-bis/quater) e **Stato/ente pubblico/pubblica utilità** (635-ter/quinquies).

### Art. 635-bis — Danneggiamento di informazioni, dati e programmi informatici (privato)

Chiunque **distrugge**, **deteriora**, **cancella**, **altera** o **sopprime** **informazioni, dati o programmi informatici altrui** è punito, a querela, con la reclusione da sei mesi a tre anni. [fonte: PDF]

Aggravante (1-4 anni): fatto commesso con **violenza** alla persona, **minaccia**, o **abuso della qualità di operatore del sistema**. [fonte: PDF]

### Art. 635-ter — Dati/programmi di Stato o pubblica utilità

Stessa condotta del 635-bis ma rivolta a **dati e programmi utilizzati dallo Stato**, da altro **ente pubblico** o di **pubblica utilità**. Pena base 1-4 anni; se si produce effettiva distruzione/alterazione: 3-8 anni. [fonte: PDF]

### Art. 635-quater — Danneggiamento di sistemi informatici o telematici (privato)

Chiunque, mediante le condotte di cui all'articolo 635-bis ovvero attraverso **l'introduzione o la trasmissione di dati**, informazioni o programmi, **distrugge**, **danneggia**, **rende, in tutto o in parte, inservibili sistemi informatici o telematici** altrui o **ne ostacola gravemente il funzionamento**, è punito con la reclusione da uno a cinque anni. [fonte: PDF]

Aggravante: abuso della qualità di operatore del sistema. [fonte: PDF]

### Art. 635-quinquies — Sistemi di pubblica utilità

Come il 635-quater, ma il fatto è **diretto a** sistemi informatici o telematici di **pubblica utilità**. Pena aggravata: 3-8 anni se il sistema risulta distrutto, danneggiato o inservibile. [fonte: PDF]

> ✅ Ottima osservazione autonoma: il 635-bis colpisce i **contenuti** (dati, programmi); il 635-quater e quinquies colpiscono i **contenitori** (i sistemi che diventano inservibili o gravemente ostacolati). Un ransomware che cripta i file attacca i dati (635-bis); un attacco DDoS che rende irraggiungibile un server attacca il sistema (635-quater). La distinzione contenitori/contenuti è esatta e spiega perché le fattispecie sono separate.

---

## §11 — Frode Informatica (!) — Art. 640-ter c.p.

Chiunque,
- **alterando** in qualsiasi modo il funzionamento di un sistema informatico o telematico, o
- **intervenendo** senza diritto con qualsiasi modalità su dati, informazioni o programmi contenuti in un sistema informatico o telematico o ad esso pertinenti,

**procura** a sé o ad altri un **ingiusto profitto** con **altrui danno**, è punito con la reclusione da sei mesi a tre anni e con la multa da euro 51 a euro 1.032. [fonte: PDF]

Il reato di frode informatica ha la medesima struttura e quindi i medesimi elementi costitutivi della truffa dalla quale si differenzia solamente perché l'attività fraudolenta dell'agente investe non la **persona**, di cui difetta l'induzione in errore, bensì il **sistema informatico** di pertinenza della medesima, attraverso la manipolazione di detto sistema. [fonte: PDF — Trib. La Spezia 2004]

| Elemento | Truffa (art. 640) | Frode informatica (art. 640-ter) |
|----------|-------------------|----------------------------------|
| **Vittima dell'azione** | La **persona** — indotta in errore | Il **sistema informatico** — manipolato |
| **Meccanismo** | Artifizi o raggiri → induzione in errore | Alterazione del sistema o intervento sui dati |
| **Consenso** | Vittima dà consenso viziato | Non è necessario il consenso di nessuno |

### Aggravanti

**Aggravante 1** — reclusione da 1 a 5 anni: commesso a **danno dello Stato o ente pubblico**; produce un **trasferimento di denaro, di valore monetario o di valuta virtuale**; commesso con **abuso della qualità di operatore del sistema**. [fonte: PDF]

**Aggravante 2** — reclusione da 2 a 6 anni: commesso con **furto o indebito utilizzo dell'identità digitale** in danno di uno o più soggetti. [fonte: PDF]

Punibile a **querela**, salvo aggravanti. [fonte: PDF]

### Concorso con accesso abusivo

> ⚠️ Questa sezione non era presente negli appunti grezzi.

Il delitto di accesso abusivo ad un sistema informatico può **concorrere** con quello di frode informatica, diversi essendo i beni giuridici tutelati e le condotte sanzionate: il primo tutela il **domicilio informatico** sotto il profilo dello "ius excludendi alios"; il secondo contempla l'**alterazione dei dati immagazzinati nel sistema** al fine della percezione di ingiusto profitto. [fonte: PDF — Cass. 30/09/2008]

> Esempio pratico: hacker entra abusivamente in un sistema bancario (615-ter) e poi manipola i dati per trasferirsi fondi (640-ter) → entrambi i reati si applicano in concorso.

---

## §12 — Violenza sulle Cose — Art. 392 c.p.

> **(Domanda: questo capitolo non ha senso di stare per ultimo, da solo, non lo collego a nulla)**
>
> Hai ragione sulla collocazione — nel PDF era alla slide 4, subito prima del 615-ter. Il senso è: l'art. 392 è l'unico reato "eventualmente informatico" del modulo (esiste anche senza informatica). Il legislatore lo cita come ponte tra la concezione classica di violenza sulle cose e quella informatica. Negli appunti va messo in §1 come esempio del primo tipo, non in coda.
>
> Il collegamento concreto: se qualcuno cancella il tuo software per farti un torto (esercitando un preteso diritto), è art. 392. Se invece lo cancella per danneggiare il sistema in sé, è art. 635-bis. La differenza è nell'**intenzione dell'agente** e nel contesto.

Si ha violenza sulle cose, agli effetti della legge penale, allorché un **programma informatico** viene **alterato**, **modificato** o **cancellato** in tutto o in parte ovvero viene **impedito o turbato il funzionamento** di un sistema informatico o telematico. [fonte: PDF]

---

## Schema Riepilogativo — Tutti gli Articoli

> **(Richiesta: schema grande di tutti gli articoli affrontati, classificati e spiegati brevemente)**

### Reati contro la riservatezza e il domicilio informatico

| Articolo | Nome | Condotta | Keyword |
|----------|------|----------|---------|
| **392 c.p.** | Violenza sulle cose | Altera/cancella programma o turba funzionamento | Eventualmente informatico |
| **615-ter c.p.** | Accesso abusivo | Si introduce o si mantiene abusivamente in sistema protetto | Domicilio informatico, mera condotta |
| **615-quater c.p.** | Detenzione mezzi di accesso | Detiene/diffonde strumenti per accedere (grimaldelli) | Profitto o danno, codici/password |
| **615-quinquies c.p.** | Detenzione strumenti di danneggiamento | Detiene/diffonde apparecchi/programmi per danneggiare | Malware, DDoS, scopo danno |

### Reati contro la corrispondenza e le comunicazioni

| Articolo | Nome | Condotta | Keyword |
|----------|------|----------|---------|
| **616 c.p.** | Corrispondenza | Prende cognizione, sottrae, distrugge o rivela corrispondenza informatica | Querela, nocumento |
| **617-quater c.p.** | Intercettazione | Intercetta, impedisce o interrompe comunicazioni — o le rivela al pubblico | Fraudolentemente |
| **617-quinquies c.p.** | Apparecchi per intercettare | Detiene/diffonde strumenti per intercettare comunicazioni | Fine di intercettare |
| **617-sexies c.p.** | Falsificazione comunicazioni | Forma falsamente, altera o sopprime contenuto di comunicazioni | Vantaggio o danno |

### Reati contro l'integrità di dati e sistemi

| Articolo | Nome | Oggetto | Soggetto passivo |
|----------|------|---------|-----------------|
| **621 c.p.** | Documenti segreti | Rivela/impiega contenuto segreto di atti/documenti | Qualunque titolare (nocumento richiesto) |
| **635-bis c.p.** | Danni dati/programmi | Dati, programmi altrui | Privato |
| **635-ter c.p.** | Danni dati/programmi pubblici | Dati, programmi Stato/ente pubblico | Stato/pubblica utilità |
| **635-quater c.p.** | Danni sistemi | Sistemi informatici/telematici | Privato |
| **635-quinquies c.p.** | Danni sistemi pubblici | Sistemi di pubblica utilità | Pubblica utilità |

### Reati patrimoniali

| Articolo | Nome | Meccanismo | Differenza chiave |
|----------|------|------------|-------------------|
| **640-ter c.p.** | Frode informatica | Altera il sistema o interviene sui dati per ingiusto profitto | Vittima è il sistema, non la persona |

---

## Scenari di Qualificazione

**Scenario A**: Un hacker entra in un server universitario con credenziali trovate online. Non fa nulla, esplora solo i file.
→ **Art. 615-ter** — reato di mera condotta: si perfeziona con l'accesso, non è necessario un danno.

**Scenario B**: Un amministratore di sistema accede ai file personali di un dipendente per curiosità, usando i suoi privilegi di root.
→ **Art. 615-ter** — avendo titolo per accedere al sistema, lo utilizza per finalità diverse da quelle consentite [Cass. 8/7/2008]. Possibile concorso con **art. 616** se si tratta di corrispondenza.

**Scenario C**: Qualcuno vende su un forum una lista di password rubate per accedere a conti bancari online.
→ **Art. 615-quater** — codici/parole chiave idonei all'accesso a sistemi protetti, distribuiti a scopo di profitto.

**Scenario D**: Qualcuno distribuisce un ransomware che cripta tutti i file delle vittime e rende i PC inutilizzabili.
→ **Art. 615-quinquies** (distribuzione di programma diretto al danneggiamento). Quando eseguito: **art. 635-bis** (dati criptati) + **art. 635-quater** (sistema inutilizzabile) in concorso.

**Scenario E**: Un hacker manipola il database di una banca per trasferire fondi sul proprio conto, dopo essersi introdotto abusivamente.
→ **Art. 615-ter** (accesso abusivo) + **Art. 640-ter** (frode informatica) in concorso — aggravante per trasferimento di denaro. [Cass. 30/09/2008]

---

## Domande di Autoverifica — Risposte

> ⚠️ Le domande di autoverifica non erano incluse negli appunti grezzi. Da rispondere in autonomia prima di portare il modulo a ✅.

**D1.** Un penetration tester si introduce senza autorizzazione in un sistema aziendale per identificarne le vulnerabilità, non causa alcun danno e poi invia un report all'azienda. Ha commesso il reato di accesso abusivo? La risposta cambia se l'azienda aveva commissionato il test?

**D2.** Qual è la differenza tra art. 615-quater e art. 615-quinquies? Fai un esempio concreto per ciascuno.

**D3.** Un dipendente accede al sistema della propria azienda con le sue credenziali legittime, ma scarica dati riservati dei clienti per passarli a un concorrente. Commette il reato di accesso abusivo (art. 615-ter)? La risposta della Cassazione è univoca?

**D4.** Un attacco informatico rende completamente inutilizzabili i sistemi di un ospedale pubblico per tre giorni. Quali articoli del codice penale si applicano? Distingui tra fattispecie applicabili al danno ai dati e al danno ai sistemi.

**D5.** In cosa si differenzia la frode informatica (art. 640-ter) dalla truffa (art. 640)? I due reati possono concorrere con l'accesso abusivo (art. 615-ter)?

---

## Attenzione Esame — Temi Prioritari (dalla professoressa)

- **Accesso abusivo (art. 615-ter)** — reato di mera condotta, domicilio informatico, abusività oggettiva (!)
- Detenzione mezzi di accesso vs detenzione strumenti di danneggiamento (615-quater vs 615-quinquies)
- Corrispondenza informatica — definizione estesa di "corrispondenza"
- Intercettazione di comunicazioni informatiche
- Apparecchiature per intercettare
- Falsificazione di comunicazioni informatiche
- Rivelazione di documenti segreti — nocumento come condizione di punibilità
- Danneggiamento: famiglia 635-bis/ter/quater/quinquies — distinzione dati vs sistemi, privato vs Stato
- **Frode informatica (art. 640-ter)** — differenza dalla truffa, concorso con accesso abusivo (!)
