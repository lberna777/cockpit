# Lezione — Modulo D12: L'Intelligenza Artificiale e l'AI Act
**Corso**: Diritto dell'Informatica T
**Materiale**: `12_DirInfo_2026_AI_Act_DEF.pdf` (prof. Claudia Cevenini, a.a. 2025/2026)
**Normativa di riferimento**: Regolamento (UE) 2024/1689 del 13 giugno 2024 (AI Act)

> ⚠️ **Attenzione — pattern ricorrente**: in questo modulo le distinzioni da NON fondere sono: fornitore vs deployer; pratiche vietate vs alto rischio vs rischio limitato; GPAI vs sistema di IA. Tenerle separate è il criterio che la professoressa usa per valutare la comprensione del modulo.

---

## Obiettivo

Saper spiegare la logica dell'AI Act, classificare un sistema di IA nel livello di rischio corretto, identificare gli obblighi applicabili a fornitore e deployer, e descrivere le principali novità del Digital Omnibus 2026.

---

## Quadro Normativo

**Regolamento (UE) 2024/1689 del 13 giugno 2024** — il primo quadro giuridico sull'IA a livello mondiale. [fonte: PDF]

Tre caratteristiche fondanti: [fonte: PDF]
- Primo quadro giuridico sull'IA a livello mondiale
- Intende promuovere un'IA affidabile in Europa
- Stabilisce norme **basate sul rischio** per gli sviluppatori e gli operatori di IA

### Tappe di applicazione [fonte: PDF]

La legge è entrata **in vigore il 1° agosto 2024** e sarà **pienamente applicabile il 2 agosto 2026**, con le seguenti eccezioni:

| Data | Cosa diventa applicabile |
|------|--------------------------|
| **2 febbraio 2025** | Divieti (pratiche vietate, art. 5) + obblighi di alfabetizzazione |
| **2 agosto 2025** | Norme di governance + obblighi per modelli GPAI |
| **2 agosto 2026** | Piena applicazione (tutto il resto) |
| **2 dicembre 2027** | Sistemi ad alto rischio standalone (Allegato III) — prorogato dal Digital Omnibus |
| **2 agosto 2028** | Sistemi ad alto rischio embedded in prodotti (Allegato I) — prorogato dal Digital Omnibus |

---

## §1 — Perché una Legge sull'IA?

La ratio della legge è **garantire che gli europei possano fidarsi dell'IA**. [fonte: PDF]

La maggior parte dei sistemi di IA non pone rischi e può essere di grande utilità. Alcuni sistemi presentano rischi che devono essere affrontati per prevenire ed evitare risultati indesiderati. Ad esempio, è importante comprendere i motivi che hanno condotto un sistema di IA a prendere una decisione o fare una previsione — qualcuno potrebbe essere stato indebitamente svantaggiato nell'accesso all'università o in un'assunzione, una valutazione o una diagnosi medica potrebbe essere errata. [fonte: PDF]

### Oggetto della legge [fonte: PDF]

Migliorare il funzionamento del mercato interno e **promuovere la diffusione di un'intelligenza artificiale (IA) antropocentrica e affidabile**, garantendo nel contempo un **livello elevato di protezione della salute, della sicurezza e dei diritti fondamentali** sanciti dalla Carta dei diritti fondamentali dell'Unione europea, compresi la democrazia, lo Stato di diritto e la protezione dell'ambiente, contro gli effetti nocivi dei sistemi di IA nell'Unione, e **promuovendo l'innovazione**. [fonte: PDF]

La legge sull'IA stabilisce: [fonte: PDF]
- a) **regole armonizzate** per l'immissione sul mercato, la messa in servizio e l'uso dei sistemi di IA nell'Unione
- b) **divieti** di talune pratiche di IA
- c) **requisiti specifici** per i sistemi di IA ad alto rischio e **obblighi** per gli operatori di tali sistemi
- d) **regole di trasparenza armonizzate** per determinati sistemi di IA
- e) **regole armonizzate per l'immissione sul mercato** di modelli di IA per finalità generali
- f) regole in materia di **monitoraggio** del mercato, **vigilanza** del mercato, governance ed esecuzione
- g) **misure a sostegno dell'innovazione**, con particolare attenzione alle PMI, comprese le start-up

### La legge sull'IA NON si applica: [fonte: PDF]

- ai sistemi immessi sul mercato, messi in servizio o utilizzati esclusivamente per **scopi militari, di difesa o di sicurezza nazionale**
- ai sistemi di IA o modelli di IA specificamente sviluppati e messi in servizio al solo scopo di **ricerca e sviluppo scientifici**
- alle **persone fisiche** che utilizzano sistemi di IA nel corso di un'attività non professionale **puramente personale**

---

## §2 — Definizioni Chiave

### Sistema di IA [fonte: PDF]
Un **sistema automatizzato** progettato per funzionare con **livelli di autonomia variabili** e che può presentare **adattabilità dopo la diffusione** e che, per obiettivi espliciti o impliciti, **deduce dall'input che riceve come generare output** quali previsioni, contenuti, raccomandazioni o decisioni che possono influenzare ambienti fisici o virtuali.

> Tre tratti costitutivi: (1) automatizzato; (2) autonomia variabile + adattabilità post-diffusione; (3) deduce output da input. Un sistema che si limita a eseguire regole fisse scritte da un programmatore non è un sistema di IA ai sensi della legge.

### Rischio [fonte: PDF]
La **combinazione della probabilità del verificarsi di un danno** e la **gravità del danno stesso**.

### Fornitore [fonte: PDF]
Una persona fisica o giuridica, un'autorità pubblica, un'agenzia o un altro organismo che **sviluppa** un sistema di IA o un modello di IA per finalità generali **o** che **fa sviluppare** un sistema di IA e **immette tale sistema o modello sul mercato** o **mette in servizio il sistema di IA con il proprio nome o marchio**, a titolo oneroso o gratuito.

> Il fornitore è chi mette il proprio nome/marchio sul sistema — che lo abbia sviluppato direttamente o commissionato.

### Deployer [fonte: PDF]
Una persona fisica o giuridica, un'autorità pubblica, un'agenzia o un altro organismo che **utilizza un sistema di IA sotto la propria autorità**, tranne nel caso in cui il sistema di IA sia utilizzato nel corso di un'attività personale non professionale.

> ⚠️ **Distinzione da non fondere**: il fornitore **sviluppa e immette sul mercato**; il deployer **usa**. Stessa azienda può essere entrambe le cose in contesti diversi. Obblighi distinti per ciascuno.

### Incidente grave [fonte: PDF]
Un incidente o malfunzionamento di un sistema di IA che, direttamente o indirettamente, causa una delle conseguenze seguenti:
- a) il **decesso** di una persona o **gravi danni alla salute** di una persona
- b) una **perturbazione grave e irreversibile** della gestione o del funzionamento delle **infrastrutture critiche**
- c) la **violazione degli obblighi** a norma del diritto dell'Unione intesi a proteggere i **diritti fondamentali**
- d) **gravi danni alle cose o all'ambiente**

---

## §3 — Alfabetizzazione in Materia di IA

I **fornitori** e i **deployer** dei sistemi di IA adottano **misure** per garantire nella misura del possibile un **livello sufficiente di alfabetizzazione** in materia di IA del loro **personale** nonché di **qualsiasi altra persona** che si occupa del funzionamento e dell'utilizzo dei sistemi di IA per loro conto, prendendo in considerazione le loro conoscenze tecniche, la loro esperienza, istruzione e formazione, nonché il contesto in cui i sistemi di IA devono essere utilizzati, e tenendo conto delle persone o dei gruppi di persone su cui i sistemi di IA devono essere utilizzati. [fonte: PDF]

> Applicabile dal **2 febbraio 2025**. È un obbligo che grava sia su chi sviluppa sia su chi usa — non solo sui tecnici, ma su tutto il personale che interagisce con l'IA.

---

## §4 — Approccio Basato sul Rischio: i 4 Livelli

La legge sull'IA stabilisce **4 livelli di rischio** per i sistemi di IA. [fonte: PDF]

```
        ▲  RISCHIO INACCETTABILE — pratiche vietate
       ███
      █████  ALTO RISCHIO — obblighi rigorosi
     ███████
    █████████  RISCHIO LIMITATO — obblighi di trasparenza
   ███████████
  █████████████  RISCHIO MINIMO O NULLO — nessuna norma specifica
```

Il livello di rischio determina il regime normativo applicabile. Non si tratta di un continuum: ciascun livello ha un insieme specifico di obblighi.

---

## §5 — Rischio Inaccettabile: Pratiche Vietate

Include i sistemi di IA considerati una **chiara minaccia alla sicurezza, ai mezzi di sussistenza e ai diritti delle persone**. Sono definite **8 pratiche vietate**. [fonte: PDF]

> Applicabili dal **2 febbraio 2025**.

### Pratica 1 — Tecniche subliminali o manipolative [fonte: PDF]
L'immissione sul mercato, la messa in servizio o l'uso di un sistema di IA che utilizza **tecniche subliminali che agiscono senza che una persona ne sia consapevole** o **tecniche volutamente manipolative o ingannevoli** aventi lo scopo o l'effetto di **distorcere materialmente il comportamento di una persona o di un gruppo** di persone, **pregiudicando** in modo considerevole la loro **capacità di prendere una decisione informata**, inducendole pertanto a prendere una decisione che non avrebbero altrimenti preso, in un modo che provochi o possa ragionevolmente provocare a tale persona, a un'altra persona o a un gruppo di persone un **danno significativo**.

### Pratica 2 — Sfruttamento delle vulnerabilità [fonte: PDF]
L'immissione sul mercato, la messa in servizio o l'uso di un sistema di IA che **sfrutta le vulnerabilità di una persona fisica** o di uno specifico gruppo di persone, dovute all'**età**, alla **disabilità** o a una **specifica situazione sociale o economica**, con l'obiettivo o l'effetto di **distorcere materialmente il comportamento** di tale persona in un modo che provochi o possa ragionevolmente provocare un **danno significativo**.

### Pratica 3 — Social scoring [fonte: PDF]
L'immissione sul mercato, la messa in servizio o l'uso di sistemi di IA per la **valutazione o la classificazione delle persone fisiche** o di gruppi per un determinato **periodo di tempo** sulla base del loro **comportamento sociale** o di **caratteristiche personali o della personalità** note, inferite o previste, in cui il **punteggio sociale** così ottenuto comporti:
- i) un **trattamento pregiudizievole o sfavorevole** in contesti sociali **non collegati ai contesti** in cui i dati sono stati originariamente generati o raccolti
- ii) un trattamento pregiudizievole o sfavorevole che sia **ingiustificato o sproporzionato** rispetto al comportamento sociale o alla sua gravità

### Pratica 4 — Previsione del rischio di reato [fonte: PDF]
L'uso di sistemi di IA per effettuare **valutazioni del rischio relative a persone fisiche** al fine di **valutare o prevedere il rischio** che una persona fisica commetta un **reato**, **unicamente sulla base della profilazione** di una persona fisica o della valutazione dei suoi **tratti e delle caratteristiche della personalità**; tale divieto **non si applica** ai sistemi di IA utilizzati a sostegno della valutazione umana del coinvolgimento di una persona in un'attività criminosa, che si basa già su fatti oggettivi e verificabili direttamente connessi a un'attività criminosa.

### Pratica 5 — Scraping di immagini facciali [fonte: PDF]
L'immissione sul mercato, la messa in servizio o l'uso di sistemi di IA che **creano o ampliano le banche dati di riconoscimento facciale** mediante **scraping non mirato** di **immagini facciali** da **internet** o da **filmati di telecamere a circuito chiuso**.

### Pratica 6 — Inferenza delle emozioni sul lavoro e a scuola [fonte: PDF]
L'immissione sul mercato, la messa in servizio o l'uso di sistemi di IA per **inferire le emozioni di una persona fisica** nell'ambito del **luogo di lavoro** e degli **istituti di istruzione**, tranne laddove l'uso del sistema di IA sia destinato a essere messo in funzione o immesso sul mercato per **motivi medici o di sicurezza**.

### Pratica 7 — Categorizzazione biometrica per inferire categorie protette [fonte: PDF]
L'immissione sul mercato, la messa in servizio o l'uso di sistemi di **categorizzazione biometrica** che classificano individualmente le persone fisiche sulla base dei loro **dati biometrici** per trarre **deduzioni o inferenze** in merito a **razza, opinioni politiche, appartenenza sindacale, convinzioni religiose o filosofiche, vita sessuale o orientamento sessuale**; tale divieto non riguarda l'etichettatura o il filtraggio di set di dati biometrici acquisiti legalmente nel settore delle attività di contrasto.

### Pratica 8 — Identificazione biometrica remota "in tempo reale" in spazi pubblici [fonte: PDF]
L'uso di sistemi di **identificazione biometrica remota "in tempo reale" in spazi accessibili al pubblico** a fini di **attività di contrasto**, a meno che — e nella misura in cui — tale uso sia strettamente necessario per uno degli obiettivi seguenti:
- i) la **ricerca mirata di specifiche vittime** di sottrazione, tratta di esseri umani o sfruttamento sessuale, nonché la **ricerca di persone scomparse**
- ii) la **prevenzione di una minaccia specifica, sostanziale e imminente per la vita o l'incolumità fisica** delle persone o di un **attacco terroristico**
- iii) la **localizzazione o l'identificazione di una persona sospettata** di aver commesso un reato grave (pena massima di almeno quattro anni), ai fini di indagine penale

---

## §6 — Sistemi di IA ad Alto Rischio

I casi d'uso dell'IA che possono comportare **gravi rischi per la salute, la sicurezza o i diritti fondamentali** sono classificati come ad alto rischio. [fonte: PDF]

### Categorie (esempi dal PDF) [fonte: PDF]

| Area | Esempi |
|------|--------|
| **Infrastrutture critiche** | Componenti di sicurezza nei trasporti — un guasto potrebbe mettere a rischio vita e salute |
| **Istruzione** | Sistemi che determinano l'accesso all'istruzione e il corso della vita professionale (punteggio esami) |
| **Componenti di sicurezza** | IA applicata alla chirurgia assistita da robot |
| **Occupazione** | Software di selezione CV per le assunzioni |
| **Servizi essenziali** | Credit scoring che nega l'accesso a un prestito |
| **Biometria** | Identificazione biometrica remota, riconoscimento emozioni, categorizzazione biometrica (es. identificare retroattivamente un taccheggiatore) |
| **Attività di contrasto** | Casi d'uso che possono interferire con i diritti fondamentali (es. valutazione affidabilità prove) |
| **Migrazione e frontiere** | Esame automatizzato delle domande di visto |
| **Giustizia** | Soluzioni di IA per preparare sentenze dei tribunali |

### Obblighi per i sistemi ad alto rischio [fonte: PDF]

I sistemi di IA ad alto rischio sono soggetti a **obblighi rigorosi** prima di poter essere immessi sul mercato:
- adeguati **sistemi di valutazione e mitigazione dei rischi**
- **alta qualità** delle **serie di dati** che alimentano il sistema per ridurre al minimo i rischi di **risultati discriminatori**
- **registrazione dell'attività** per garantire la **tracciabilità dei risultati**
- **documentazione dettagliata** che fornisca tutte le informazioni necessarie sul sistema e sul suo scopo affinché le **autorità ne valutino la conformità**
- **informazioni chiare e adeguate** per l'operatore
- adeguate **misure di sorveglianza umana**
- **elevato livello di robustezza, cibersicurezza e accuratezza**

---

## §7 — Rischio Limitato: Obblighi di Trasparenza

La legge sull'IA introduce **obblighi di divulgazione specifici** per garantire che gli esseri umani siano **informati** quando necessario per preservare la fiducia. [fonte: PDF]

- Quando si utilizzano sistemi di IA come i **chatbot**, gli esseri umani dovrebbero essere **consapevoli** del fatto che stanno **interagendo con una macchina** in modo che possano prendere una decisione informata.
- I fornitori di IA generativa devono garantire che i **contenuti generati dall'IA siano identificabili**.
- Alcuni **contenuti generati dall'IA** dovrebbero essere **etichettati in modo chiaro e visibile**: deep fake e testi pubblicati allo scopo di informare il pubblico su questioni di interesse pubblico.

---

## §8 — Rischio Minimo o Nullo

La legge sull'IA **non introduce norme** per l'IA ritenuta a rischio minimo o nullo. La **stragrande maggioranza** dei sistemi di IA attualmente utilizzati nell'UE rientra in questa categoria. [fonte: PDF]

> Esempi: videogiochi abilitati all'intelligenza artificiale o filtri antispam.

---

## §9 — Modelli di IA per Uso Generale (GPAI)

I modelli GPAI (General Purpose AI) sono **modelli addestrati su grandi quantità di dati**, capaci di svolgere un'**ampia gamma di compiti**: es. ChatGPT (OpenAI), Gemini (Google), Claude (Anthropic), LLaMA (Meta). [fonte: PDF]

> ⚠️ **Distinzione da non fondere**: un **modello GPAI** è il modello di base (es. GPT-4); un **sistema di IA** è il sistema che lo incorpora e lo usa in un contesto specifico (es. un chatbot per il servizio clienti basato su GPT-4). Obblighi diversi per ciascuno.

### Obblighi per i fornitori GPAI (applicabili dal 2 agosto 2025) [fonte: PDF]
- Redigere e aggiornare la **documentazione tecnica** del modello
- Rispettare la normativa sul **diritto d'autore** nei dati di addestramento e pubblicare una **sintesi pubblica dei contenuti formativi**

### Modelli con rischio sistemico ("frontier models") [fonte: PDF]
Obblighi aggiuntivi: **sicurezza**, **valutazione avversariale**, **segnalazione incidenti all'AI Office**.

### Codice di buone pratiche GPAI (luglio 2025) [fonte: PDF]
Strumento **volontario** redatto da esperti indipendenti; l'**adesione costituisce presunzione di conformità**.

### Vigilanza sui GPAI [fonte: PDF]
La **Commissione europea**, tramite l'**AI Office**, ha **competenza esclusiva** sui fornitori GPAI; i poteri sanzionatori diventano pienamente operativi il **2 agosto 2026**.

---

## §10 — Sanzioni

| Fascia | Violazione | Importo |
|--------|-----------|---------|
| **Fascia 1** | Violazioni dei divieti (pratiche vietate, art. 5) | Fino a **35.000.000 €** o **7%** del fatturato mondiale annuo |
| **Fascia 2** | Altre violazioni (es. obblighi sistemi ad alto rischio) | Fino a **15.000.000 €** o **3%** del fatturato mondiale annuo |
| **Fascia 3** | Informazioni false o fuorvianti alle autorità | Fino a **7.500.000 €** o **1%** del fatturato mondiale annuo |

**PMI e start-up**: si applica il minore tra la soglia fissa e la percentuale sul fatturato (regime più favorevole). [fonte: PDF]

**Sanzioni non pecuniarie**: ritiro del sistema dal mercato, blocco immediato dell'utilizzo, cancellazione dai database. **Le sanzioni sono simili per struttura a quelle del GDPR** e si **cumulano** con esse. [fonte: PDF]

**Autorità di vigilanza**: ogni Stato membro doveva designare l'autorità nazionale competente entro il 2 agosto 2025; la Commissione europea supervisiona i fornitori di modelli GPAI tramite l'AI Office. [fonte: PDF]

---

## §11 — Digital Omnibus sull'IA (Aggiornamento 2026)

Il 19 novembre 2025 la Commissione ha proposto il "Digital Omnibus sull'IA", pacchetto di modifiche mirate all'AI Act. Il **7 maggio 2026** Parlamento e Consiglio UE hanno raggiunto un **accordo politico provvisorio**. [fonte: PDF]

### Principali modifiche [fonte: PDF]

| Cosa | Prima | Dopo |
|------|-------|------|
| Sistemi ad alto rischio standalone (Allegato III) | Scadenza 2 agosto 2026 | Scadenza **2 dicembre 2027** |
| Sistemi ad alto rischio embedded in prodotti (Allegato I) | Scadenza 2 agosto 2026 | Scadenza **2 agosto 2028** |
| Watermarking contenuti AI generativi | Scadenza 2 agosto 2026 | Prorogato al **2 dicembre 2026**; esenzioni estese a PMI e "piccole medie imprese" |
| Nuovo divieto (deepfake intimi, CSAM) | Non previsto | Sistemi IA per generazione di immagini sessuali non consensuali — vietati dal **2 dicembre 2026** |

### Cosa resta invariato [fonte: PDF]
I **divieti vigenti** (art. 5), gli **obblighi di alfabetizzazione IA** (art. 4) e gli **obblighi GPAI** restano invariati. L'accordo provvisorio deve ancora essere formalmente adottato.

---

## §12 — Orientamenti Etici per un'IA Affidabile

**2018**: la Commissione Europea istituisce un "**Gruppo indipendente di esperti ad alto livello sull'Intelligenza Artificiale**". [fonte: PDF]

**2019**: il Gruppo pubblica gli "**Orientamenti etici per un'IA affidabile**". [fonte: PDF]

Un'IA affidabile deve essere: [fonte: PDF]
- a) **legale** (rispetto di tutte le leggi e i regolamenti applicabili)
- b) **etica** (adesione a principi e valori etici)
- c) **robusta** (dal punto di vista tecnico e sociale)

### Principi Etici [fonte: PDF]
1. Rispetto dell'**autonomia umana**
2. **Prevenzione dei danni**
3. **Equità**
4. **Esplicabilità**

### Requisiti di un'IA Affidabile [fonte: PDF]
1. **Intervento e sorveglianza umani** — inclusi i diritti fondamentali, l'intervento umano e la sorveglianza umana
2. **Robustezza tecnica e sicurezza** — inclusi la resilienza agli attacchi, il piano di emergenza, la precisione, l'affidabilità e la riproducibilità
3. **Riservatezza e governance dei dati** — inclusi il rispetto della riservatezza, la qualità e l'integrità dei dati e l'accesso ai dati
4. **Trasparenza** — incluse la tracciabilità, la spiegabilità e la comunicazione
5. **Diversità, non discriminazione ed equità** — incluse la prevenzione di distorsioni inique, l'accessibilità e la progettazione universale
6. **Benessere sociale e ambientale** — inclusi la sostenibilità, l'impatto sociale, la società e la democrazia
7. **Accountability** — inclusi la verificabilità, la riduzione al minimo degli effetti negativi e la loro segnalazione, i compromessi e i ricorsi

### ALTAI [fonte: PDF]
Nel luglio 2020 il Gruppo ha presentato la lista di controllo finale per un'IA affidabile: **ALTAI = Assessment List for Trustworthy AI**. Strumento pratico che traduce gli orientamenti etici in una lista di controllo accessibile e dinamica per autovalutazione. Utilizzabile da sviluppatori e operatori.

---

## Casi Pratici dal PDF

### Caso 1 — Clearview AI e il riconoscimento facciale [fonte: PDF]

Clearview AI (società statunitense) ha costruito un database con oltre 30 miliardi di immagini facciali scaricate da internet senza consenso, offrendolo a forze dell'ordine e altri soggetti per il riconoscimento di persone.

**Sanzioni europee (GDPR)**: Italia (Garante): 20 mln €; Francia (CNIL): 20 mln €; Paesi Bassi: 30,5 mln € (2024) — totale sanzioni EU circa 100 mln €.

**Rilevanza rispetto all'AI Act**:
- Pratica vietata n. 5 (art. 5): scraping non mirato di immagini facciali per ampliare banche dati biometriche — divieto in vigore dal 2 febbraio 2025
- L'uso di identificazione biometrica remota in tempo reale in spazi pubblici è vietato (pratica n. 8)
- Con l'AI Act le sanzioni potenziali sarebbero ancora più elevate (fino al 7% del fatturato globale)

### Caso 2 — Amazon: algoritmo di selezione del personale [fonte: PDF]

Dal 2014 al 2017 Amazon ha sviluppato un sistema di IA per valutare automaticamente i candidati (da 1 a 5 stelle). Il modello, addestrato su 10 anni di CV ricevuti (prevalentemente maschili nel settore tech), ha imparato a svantaggiare sistematicamente le candidate donne, penalizzando CV contenenti la parola "women's" o riferimenti a college femminili. Il sistema è stato abbandonato nel 2017.

**Rilevanza rispetto all'AI Act**:
- **Sistema ad alto rischio**: i software di selezione CV per assunzioni rientrano nell'Allegato III, punto 4 (strumenti IA per l'occupazione e gestione lavoratori)
- Con l'AI Act oggi obbligatorio: **governance dei dati di addestramento** per ridurre i bias, documentazione tecnica, sorveglianza umana, tracciabilità dei risultati
- **Principio chiave**: i sistemi IA ereditano i *bias* presenti nei dati di addestramento; **la tecnologia non è neutrale per definizione**

### Caso 3 — Manipolazione (pratica vietata n. 1) [fonte: PDF]

Un'app di e-commerce utilizza un modello IA per rilevare momenti di vulnerabilità emotiva dell'utente (es. orario notturno, comportamento ansioso di navigazione) e attivare messaggi di scarcità fittizia ("solo 1 rimasto!") per indurre acquisti compulsivi senza che l'utente ne sia consapevole. → Violazione dell'art. 5, par. 1, lett. a) — vietato dal 2 febbraio 2025.

### Caso 4 — Social scoring (pratica vietata n. 3) [fonte: PDF]

Un e-commerce assegna un punteggio ai clienti basato su comportamento sociale (recensioni negative lasciate, frequenza di resi, interazioni online) e usa tale punteggio per discriminarli nell'accesso a offerte, prezzi o spedizioni prioritarie. → Violazione dell'art. 5, par. 1, lett. c) — vietato dal 2 febbraio 2025. Analogo al sistema di credito sociale cinese, esplicitamente vietato nell'UE in qualsiasi forma.

### Caso 5 — Riconoscimento emozioni in ambito lavorativo (pratica vietata n. 6) [fonte: PDF]

Un datore di lavoro installa telecamere IA per analizzare le espressioni facciali dei dipendenti durante le riunioni, inferire il loro stato emotivo e valutare produttività o coinvolgimento. → Violazione dell'art. 5, par. 1, lett. f) — vietato dal 2 febbraio 2025.

---

## Schema Riepilogativo — I 4 Livelli e i loro Regimi

| Livello | Esempi | Regime |
|---------|--------|--------|
| **Inaccettabile** | Social scoring, manipolazione, identificazione biometrica real-time in spazi pubblici, scraping facciale | **Divieto assoluto** (art. 5) — sanzione fino al 7% fatturato |
| **Alto rischio** | CV screening, credit scoring, chirurgia robotica, sentenze IA, esame domande visto | **Obblighi rigorosi** prima dell'immissione sul mercato — sanzione fino al 3% |
| **Limitato** | Chatbot, IA generativa, deepfake | **Obblighi di trasparenza** — dichiarare che è IA |
| **Minimo/nullo** | Videogiochi, filtri antispam | **Nessuna norma specifica** |

---

## Domande di Autoverifica

1. Cos'è l'AI Act e qual è il suo oggetto? In quali casi non si applica?

2. Illustra i 4 livelli di rischio dell'approccio basato sul rischio. Fai un esempio concreto per ciascun livello e indica il regime normativo applicabile.

3. Elenca almeno 4 delle 8 pratiche vietate (rischio inaccettabile) e spiega il criterio comune che le accomuna. Sai distinguerle dai sistemi ad alto rischio?

4. Cosa si intende per modello GPAI? Quali obblighi gravano sui fornitori GPAI e come si differenziano da quelli dei fornitori di sistemi ad alto rischio?

5. Come funziona il sistema sanzionatorio dell'AI Act? Distingui le 3 fasce e spiega il rapporto con le sanzioni del GDPR. Cosa ha cambiato il Digital Omnibus del 2026 e cosa è rimasto invariato?

---

## Riepilogo

**Il Regolamento (UE) 2024/1689** è il primo quadro giuridico mondiale sull'IA: promuove un'IA antropocentrica e affidabile basando gli obblighi sul livello di rischio del sistema. [fonte: PDF]

**I 4 livelli**: rischio inaccettabile (8 pratiche vietate, divieto assoluto), alto rischio (obblighi rigorosi pre-mercato), rischio limitato (obblighi di trasparenza), rischio minimo/nullo (nessuna norma). [fonte: PDF]

**Il Digital Omnibus (accordo 7 maggio 2026)** ha prorogato le scadenze per i sistemi ad alto rischio ma ha lasciato invariati i divieti (art. 5), gli obblighi di alfabetizzazione e gli obblighi GPAI. [fonte: PDF]

<!-- AUTO-LINKS:START -->
## 🔗 Collegati

- [[Appunti_ModuloD12]]
- [[appunti_moduloD12_ai_act]]
- [[speedreview_D12_ai_act]]

**Hub:** [[master_map_studio]] · [[glossario_diritto]] · [[concept_maps]]
<!-- AUTO-LINKS:END -->
