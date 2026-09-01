
**Obbiettivo:** spiegare finalità, destinatari e obblighi principali di **DSA, DMA e Data Act** - i regolamenti che affiancano senza sovrapporsi e si coordinano con il **GDPR**

I tre regolamenti rispondono a domande diverse:

**DSA - Cosa può stare online?**
**DMA - Come si compete nei mercati digitali?**
**Data Act - chi controlla i dati generati dai dispositivi?**

## PARTE I — Digital Services Act (DSA)

**Obbiettivi:**

- Garantire un ambiente online sicuro, prevedibile e affidabile
- Proteggere i diritti fondamentali degli utenti (libertà di espressione, privacy, non discriminazione)
- Contrastare la diffusione di contenuti illegali, fake news, informazioni manipolate
- Rafforzare la responsabilità e trasparenza dei servizi intermediari (elabora...)
- promuovere innovazione e crescita del mercato digitale UE

**Principio cardine**: «ciò che è illegale offline è illegale online»

**Vigilanza:**

- **DSC nazionale** (Coordinatore dei Servizi Digitali): vigila su tutti gli intermediari — in Italia: AGCOM
- **Commissione europea**: vigilanza esclusiva sulle VLOP e VLOSE
- **Comitato europeo per i servizi digitali**: coordinamento tra DSC

(spiegami le classificazioni che usi >VLOP VLOSE DSC AGCOM)

### Ambito di applicazione — i 6 livelli [fonte: PDF]

Si applica ai servizi che agiscono da **intermediari tra utenti e contenuti, beni, servizi** offerti a destinatari nell'UE

|Categoria|Esempi|Obblighi|
|---|---|---|
|Mere conduit|ISP, provider di accesso internet, registri di domini|Minimi|
|Caching|Proxy, CDN|Minimi|
|Hosting|Cloud, web hosting, server dedicati|Obblighi aggiuntivi|
|Piattaforme online|Marketplace, social network, app store (es. Amazon, Meta, Apple App Store)|Obblighi aggiuntivi|
|VLOP (≥ 45 mln utenti UE)|Facebook, YouTube, TikTok, Amazon Store|Obblighi massimi|
|VLOSE (≥ 45 mln utenti UE)|Google Search, Bing|Obblighi massimi|()
(di questi so solo cosa sono piattaforme online e VLOP VLOSE, le ultime due so solo gli esempi ma non le definizioni effettive)

### Esenzione di responsabilità (safe harbour) [fonte: PDF]

DSA mantiene il principio di esenzione dalla responsabilità per i contenuti degli utenti, già previsto dalla Direttiva e-commerce, a condizione che l'intermediario:

- **Mere conduit** (art. 4): non avvii, non selezioni il destinatario, non modifichi le informazioni trasmesse
- **Caching** (art. 5): agisca tempestivamente per rimuovere o disabilitare l'accesso ai contenuti illegali appena ne venga a conoscenza
- **Hosting** (art. 6): agisca prontamente dopo aver ricevuto una segnalazione e non abbia conoscenza effettiva dell'illecito

spiegami meglio il principio del buon sanmaritano, come funziona, in che modo si rischierebbe di perdere l'esenzione e perchè non succede

**Nessun obbligo generale di sorveglianza (art. 8)**: vietato imporre agli intermediari di monitorare in modo generalizzato i contenuti. [fonte: PDF]

### Obblighi comuni a tutti gli intermediari (artt. 11-15) [fonte: PDF]

- Identificazione di **un referente per le comunicazioni con le autorità e utenti**
- Avere un **rappresentate legale nell'UE** se il fornitore è fuori dall'UE
- **Relazione annuale sulla trasparenza** relativa all'attività di moderazione dei contenuti
- **Ordini delle autorità** sempre rispettati prontamente riguardo alla rimozione di contenuti illegali o all'accesso a informazioni 

**obblighi aggiuntivi per i servizi di hosting** (tipo azure, AWS etc?):

- **Meccanismo di segnalazione (notice & action)**: consentire a chiunque di segnalare contenuti illegali e agire prontamente
- **Notifica all'utente** della decisione di rimozione e possibilità di ricorso interno

### Obblighi per le piattaforme online (artt. 19-32) [fonte: PDF] (differenze tra intermediari di prima e piattaforme online?)

- priorità di trattamento per segnalazioni da soggetti certificati
- **Misure anti-abuso** relative a difendere il sistema di segnalazione
- **Trasparenza della pubblicità online**, rendendola chiaramente segnalata
- **Divieto di indicizzare la pubblicità in base a categorie speciali di dati**
- **Divieto di pubblicità targettizzata rivolta ai minori**
- Sistemi di raccomandazione (ma tipo correlati di youtube o raccomandazioni di adv?)
- **Risoluzione extragiudiziale delle controversie** (art. 21): accesso a organismi certificati di risoluzione alternativa

### Divieto di dark pattern — art. 25 [fonte: PDF]

I fornitori di piattaforme online NON possono progettare, organizzare o gestire le proprie interfacce online in modo tale da:

- Ingannare o manipolare i destinatari del servizio
- Falsare o compromettere materialmente la capacità di prendere decisioni libere e informate

Ad esempio:
- Pulsanti di dissenso nascosti o difficili da raggiungere
- Richieste di conferma ripetute («confirm shaming»)
- Preimpostazione di opzioni a favore del fornitore
- Interfacce che inducono urgenza fittizia

**Connessione con D12 (AI Act)**: il divieto di dark pattern del DSA si sovrappone parzialmente al divieto di tecniche manipolative (pratica 1, rischio inaccettabile). La differenza: l'AI Act vieta le tecniche subliminali/manipolative realizzate tramite sistemi AI; il DSA vieta i dark pattern nell'interfaccia indipendentemente dall'uso dell'IA.

### Protezione dei minori — art. 28 [fonte: PDF]

Le piattaforme accessibili ai minori devono adottare misure adeguate per garantire un elevato livello di riservatezza, sicurezza e protezione.

**Divieti assoluti:**

- Divieto di presentare pubblicità basata su profilazione ai minori
- Divieto di interfacce progettate per sfruttare le debolezze dei minori (dark pattern aggressivi)

**Obblighi per le VLOP:**

- Valutazione specifica dei rischi per i minori nella valutazione annuale dei rischi sistemici
- Misure di attenuazione specifiche (parental control, impostazioni di default più sicure)

_non si richiede verifica dell'età obbligatoria, ma i fornitori che rivolgono servizi ai minori devono prendere misure adeguate._ (tipo?)

### Obblighi per VLOP e VLOSE (artt. 33-43) [fonte: PDF]

- Valutazione annuale dei rischi sistematici, **derivanti dal funzionamento e uso del servizio**
- misure i **attenuazione dei rischi** adattamento dei sistemi di raccomandazione, moderazione, strumenti per cooperare con le autorità,,,
- **audit indipentendi** (cosa sono?) su conformità
- obbligo di condividere i dati con i ricercatori accademici accreditati per analizzare i rischi sistemici
-  nomina di uno o più responsabili interni indipendenti con competenze specifiche **responsabile della conformità**
- Trasparenza degli algoritmi di raccomandazione, permette agli utenti di **scegliere un sistema di raccomandazione non basato sulla profilazione**
- **pubblicare e mantenere archivi** accessibili al pubblico di **tutti gli annunci mostrati**, per almeno un anno

**VLOP designate (dall'elenco dal 2023):** Facebook, Instagram, TikTok, Twitter/X, LinkedIn, YouTube, Snapchat, Pinterest, Amazon Store, Booking.com, Apple App Store, Google Play, Zalando, Wikipedia, AliExpress. VLOSE: Bing, Google Search. [fonte: PDF]

### Sistema sanzionatorio DSA [fonte: PDF]

| Violazione | Sanzione |
|-----------|----------|
| Violazione degli obblighi del Regolamento | Fino al **6%** del fatturato mondiale annuo |
| Informazioni inesatte, incomplete o fuorvianti | Fino all'**1%** del fatturato mondiale annuo |
| Penalità di mora | Fino al **5%** del fatturato medio giornaliero mondiale per ogni giorno di inadempienza |

In caso di inadempienza sistematica: misure comportamentali o strutturali; per violazioni gravi e reiterate che minaccino la vita o la sicurezza: accesso temporaneo alla piattaforma limitato per specifici destinatari. [fonte: PDF]

## PARTE II — Digital Markets Act (DMA)

**Obiettivo**: garantire mercati digitali equi e contendibili, impedendo che pochi operatori controllino gli accessi essenziali a danno di concorrenti e consumatori.

A differenza del diritto antitrust tradizionale, il DMA non aspetta che si verifichi un danno concorrenziale: impone obblighi e divieti precauzionali a chi controlla snodi essenziali del mercato digitale. [fonte: PDF]

> il diritto antitrust tradizionale interviene ex post (dopo aver accertato l'abuso); il DMA interviene ex ante (prima che il danno avvenga), imponendo obblighi precauzionali strutturali.

Il DMA si applica alle piattaforme che forniscono i seguenti CPS:

- Servizi di intermediazione online (marketplace): es. Amazon Marketplace, Google Shopping
- Motori di ricerca online: es. Google Search, Bing
- Sistemi operativi: es. Android, iOS, Windows
- Browser web: es. Chrome, Safari
- Servizi di cloud computing: es. AWS, Azure, Google Cloud
- Servizi di comunicazione interpersonale numero-indipendenti: es. WhatsApp, Messenger, iMessage
- Piattaforme di condivisione video: es. YouTube, TikTok
- Social network: es. Facebook, Instagram, LinkedIn
- Servizi pubblicitari: es. Google Ads, Meta Ads (se legati a un CPS gatekeeper)
- Assistenti virtuali: es. Siri, Alexa, Google Assistant
### Sistema sanzionatorio DMA [fonte: PDF]

| Violazione                       | Sanzione                                                           |
| -------------------------------- | ------------------------------------------------------------------ |
| Violazione di obblighi o divieti | Fino al **10%** del fatturato totale mondiale dell'anno precedente |
| Violazione ripetuta (recidiva)   | Fino al **20%** del fatturato totale mondiale                      |
| Penalità di mora                 | Fino al **5%** del fatturato medio giornaliero mondiale            |
**Misure strutturali in caso di inosservanza sistematica (art. 18)**: se il gatekeeper viola gli obblighi per ≥ 3 volte in 8 anni, la Commissione può imporre rimedi comportamentali e strutturali — come ultima risorsa: obbligo di vendere una (parte della) propria attività o divieto di acquisire nuovi servizi. [fonte: PDF]

**Confronto DMA vs antitrust tradizionale**: il DMA prevede sanzioni più rapide e prescinde dalla prova di un abuso di posizione dominante caso per caso. [fonte: PDF]

**Caso pratico — Apple e il mercato delle app:** Il 4 marzo 2024 la Commissione ha aperto indagini formali contro Apple per sospette violazioni del DMA, tra cui: anti-steering nell'App Store; browser choice screen non conforme al DMA; accesso insufficiente alle funzioni NFC da parte di app di terzi per i pagamenti digitali. Primo caso DMA contro un gatekeeper; dimostra la portata dell'approccio ex ante rispetto al diritto antitrust. [fonte: PDF]

**Caso pratico — Google Shopping e self-preferencing:** Nel 2017 (pre-DMA), la Commissione multò Google di 2,42 mld € per aver favorito Google Shopping nei risultati di ricerca. Con il DMA, il self-preferencing è ora vietato ex ante per tutti i gatekeeper: non è più necessario dimostrare la posizione dominante e l'abuso caso per caso. Questo caso ha ispirato l'art. 6 §5 del DMA. [fonte: PDF]

### Il concetto di gatekeeper [fonte: PDF]

**Gatekeeper**: un'impresa che gestisce uno o più «servizi di piattaforma di base» (CPS) e soddisfa i seguenti **criteri cumulativi**

1. Impatto **significativo nel mercato interno**, stabilito in base al fatturato, all'espansione, e alla capitalizzazione
2. ruolo di **gateway**: un certo numero di utenti e utenti commerciali attivi
3. **posizione consolidata e duratura**

**Gatekeeper designati (2023-2024)**: Alphabet, Amazon, Apple, Booking, ByteDance, Meta, Microsoft → 23 CPS complessivamente designati. [fonte: PDF]

⚠️ **Distinzione critica — VLOP vs gatekeeper**: il criterio di designazione è diverso. VLOP (DSA): ≥ 45 mln di utenti attivi mensili nell'UE, indipendentemente dal fatturato. Gatekeeper (DMA): deve soddisfare tre criteri cumulativi, tra cui fatturato ≥ 7,5 mld € O capitalizzazione ≥ 75 mld €. Una piattaforma con 50 mln di utenti UE ma piccolo fatturato è VLOP, non gatekeeper.

### Obblighi dei gatekeeper — «do's» (art. 6) [fonte: PDF]

**Interoperabilità**: garantire che le funzioni base dei servizi di messaggistica (es. WhatsApp) siano interoperabili con servizi di terzi che ne facciano richiesta (ma in cosa è interoperabile whatsapp?...)

**Portabilità dei dati**: consentire agli utenti finali e commerciali di portare i propri dati a servizi concorrenti (in tempo reale e gratuitamente) (tipo passaggio apple android dei dati)

**Accesso ai dati di performance**: fornire agli inserzionisti e agli editori l'accesso ai dati sulle loro campagne pubblicitarie e sulle performance sulla piattaforma

**Notifica acquisizioni**: informare la Commissione di tutte le acquisizioni e fusioni realizzate (ma che commissione?)

**Trasparenza degli algoritmi di ranking**: fornire informazioni chiare sui criteri di posizionamento per gli utenti commerciali

**Accesso alle app store**: consentire agli sviluppatori di accedere alle stesse API e funzionalità disponibili al gatekeeper (in parole povere?)

### Divieti per i gatekeeper — «don'ts» (artt. 5-7) [fonte: PDF]

- **Self-preferencing**: vietato classificare i propri prodotti/servizi in modo più favorevole rispetto a quelli di terzi (es. Google Shopping nei risultati di Google Search)
- **Anti-steering**: vietato impedire agli utenti commerciali di informare i propri clienti di offerte più convenienti fuori dalla piattaforma (es. app store di Apple/Google) (cosa implica nel pratico?)
- **Bundling forzato**: vietato obbligare gli utenti a installare o usare servizi del gatekeeper come condizione per accedere ad altri (es. preinstallazione obbligatoria non rimovibile)
- **Tracciamento senza consenso**: vietato combinare dati personali provenienti da diversi CPS o da siti terzi ai fini di pubblicità mirata, salvo consenso effettivo dell'utente (in parole povere?)
- **Piattaforme di pagamento**: vietato impedire agli sviluppatori di usare piattaforme di pagamento di terzi per la vendita di app (tipo?)
- **Lock-in**: vietato ostacolare la disinstallazione di software/app preinstallate (esempio?)

### Designazione e procedura [fonte: PDF]

- Il fornitore che raggiunge le soglie quantitative deve **notificare alla Commissione entro 2 mesi**
- La Commissione emette la decisione di designazione entro **45 giorni lavorativi** dalla notifica completa
- Dopo la designazione, il gatekeeper ha **6 mesi** per conformarsi agli obblighi del DMA
- **Riesame periodico**: almeno ogni 3 anni dello status di gatekeeper
- **Vigilanza**: la Commissione europea ha competenza esclusiva sull'applicazione del DMA (art. 38); ampi poteri investigativi: ispezioni, richiesta di informazioni, audit tecnici, indagini di mercato
(quindi queste sono le condizioni per essere designati gatekeeper?)


## PARTE III — Data Act

**Obiettivo**: rendere i dati generati da prodotti connessi (IoT) e servizi correlati più accessibili e circolanti, per creare un vero mercato unico europeo dei dati equo e interoperabile. (definizione strana, in che senso mercato dei dati, in che senso prodotti connessi, a chi si rivolge?)

Il Data Act si inserisce nella **strategia europea dei dati**, accanto a: [fonte: PDF]

- GDPR (2016/679): protezione dei dati personali
- Data Governance Act (2022/868): condivisione volontaria dei dati
- DMA (2022/1925): portabilità dei dati sulle piattaforme gatekeeper

### Ambito di applicazione [fonte: PDF]

Si applica a (art. 1):

- **Produttori di prodotti connessi** immessi sul mercato dell'UE e i loro fornitori di servizi correlati
- **Titolari dei dati che mettono a disposizione dati** (in che senso dati che mettono a disposizione dati ai destinatari) ai destinatari nell'UE
- **Destinatari dei dati** nell'UE
- **Fornitori di servizi di trattamento dei dati** (cloud, edge) ai clienti nell'UE
- **Enti pubblici degli Stati membri e istituzioni UE** che **richiedono dati ai titolari in situazioni eccezionali** (tipo?)

**Definizioni chiave:** [fonte: PDF]

- **Prodotto connesso**: oggetto che raccoglie e trasmette dati (es. auto connessa, smartwatch, macchinario industriale, contatore smart, elettrodomestico connesso)
- **Utente**: chi possiede/noleggia/usa il prodotto connesso (consumatore o impresa)
- **Titolare dei dati**: chi ha il diritto/obbligo di utilizzare e mettere a disposizione i dati (es. il produttore) (non mi è chiaro, avrei detto che l'utente è titolare dei suoi dati)

### Diritto di accesso ai dati da prodotti connessi (cap. II) [fonte: PDF]

**Diritto di accesso dell'utente (artt. 4-6):**

L'utente di un prodotto connesso ha il diritto di accedere, in modo **gratuito**, sicuro e — ove tecnicamente possibile — in **tempo reale**, ai dati generati dall'uso del prodotto connesso e dai servizi correlati. I dati devono essere messi a disposizione in un formato **strutturato, di uso comune e leggibile da dispositivo automatico** (machine-readable). (ad esempio la memoria di un llm sempre leggibile e modificabile?)

**Obblighi del produttore:** [fonte: PDF]

- Informare precontrattualmente l'utente: tipo, formato, volume dei dati generati; se e come sono accessibili al produttore
- **Progettazione by default** (art. 4 §1): i prodotti devono essere progettati per permettere l'accesso predefinito dell'utente ai propri dati — obbligo dal 12 settembre 2026
- I dati non possono essere usati dal produttore per trarre conclusioni sulla posizione economica, sullo stato di salute, sulle preferenze dell'utente **senza consenso** (art. 4 §13)

### Condivisione dati con terzi (cap. II-III)

**Diritto dell'utente di condividere dati con terzi**
Su richiesta dell'utente, il titolare dei dati deve condividere i dati con **terzi designati dall'utente** (imprese o persone fisiche), a condizioni **FRAND** (eque, ragionevoli e non discriminatorie). I terzi che ricevono i dati possono usarli solo per le **finalità concordate con l'utente**

(voglio un esempio pratico di questa situazione)

**Condivisione dati B2B obbligatoria (cap. III, artt. 8-12):** [fonte: PDF]

- Obbligo di condivisione tra imprese a condizioni FRAND, qualora previsto da atti legislativi UE o nazionali
- **Compensazione equa**: il titolare dei dati può richiedere una compensazione per la messa a disposizione (valutata come costo marginale)
- **Tutela segreti commerciali**: il titolare dei dati può rifiutare la condivisione se dimostra che comporterebbe la divulgazione di segreti commerciali non adeguatamente tutelabili

(non riesco a immaginarmi un commercio di dati b2b)

### Clausole contrattuali abusive e protezione delle PMI

Una clausola contrattuale tra imprese è **abusiva** se:

- Esclude o limita in modo eccessivo **la responsabilità** dalla parte che impone la clausola per danni causati dall'inadempimento del contratto (non ho capito verso chi)
- Esclude i mezzi di ricorso dalla parte che riceve i dati se non vengono rispettati i requisiti relativi alla qualità dei dati
- Concede alla parte che impone la clausola il diritto di modificare **unilateralmente** le condizioni del contratto

### Accesso dei soggetti pubblici ai dati privati (cap. V) [fonte: PDF]

### Accesso dei soggetti pubblici ai dati privati (cap. V) [fonte: PDF]

Gli enti pubblici (e la Commissione (chi?)) possono richiedere ai titolari privati dati necessari per:

- Risposta a **emergenze pubbliche** (calamità naturali, pandemie, grandi incidenti)
- Prevenzione o ripristino in caso di **crisi eccezionale** (es. black-out, interruzione di infrastrutture critiche)
- Svolgimento di un **compito di interesse pubblico** esplicitamente previsto dalla legge


### CLOUD ----------------------------------------------------------

### Portabilità e switching tra servizi cloud (cap. VI) [fonte: PDF]

**Obblighi dei fornitori di cloud:** [fonte: PDF]

- Eliminare barriere tecniche, contrattuali e commerciali che rendono difficile il passaggio a un concorrente (switching)
- Garantire **equivalenza funzionale** durante la migrazione dei dati e delle risorse digitali
- Consentire la **disaggregazione dei servizi** (ove tecnicamente fattibile)
- **Abolizione graduale delle switching fees**: da settembre 2025 riduzione; dal 12 settembre 2027 gratuite

(fornisci esempi tangibili per questi obblighi)

**Interoperabilità**: i fornitori di servizi di trattamento dati devono adottare standard tecnici e specifiche per garantire l'interoperabilità. La Commissione può specificare standard armonizzati obbligatori tramite atti di esecuzione.

### Trasferimento internazionale di dati non personali (cap. VII) [fonte: PDF]

I fornitori di servizi cloud che trattano dati non personali nell'UE devono adottare misure tecniche e organizzative per impedire l'accesso non autorizzato da parte di autorità di paesi terzi. (come mai non personali? e per i dati personali? e poi lo proteggono dalle autorità? non sono i "buoni"?)

Se un'autorità di un paese terzo ordina il trasferimento di dati non personali, il fornitore deve:

- Informare il cliente prima di trasferire i dati (salvo divieto legale)
- Contestare l'ordine se viola il diritto UE o di uno Stato membro
- Non trasferire i dati se l'ordine è manifestamente contrario all'ordine pubblico dell'UE

per i dati personali rimangono pienamente vigenti le norme del GDPR; il Data Act copre solo i dati non personali o aggiunge norme ai dati misti. [fonte: PDF]

### Governance e sanzioni Data Act [fonte: PDF]

- Ogni Stato membro deve designare un'autorità competente (può coincidere con il Garante privacy o altra autorità sectoriale)
- Coordinamento tramite **Comitato europeo per i dati (EDIB)**
- Il Regolamento **non fissa un massimale comune**: richiede sanzioni «efficaci, proporzionate e dissuasive» — ogni Stato membro definisce le proprie
- **Rapporto con GDPR**: in caso di conflitto tra Data Act e GDPR, **prevalgono le norme GDPR** (art. 1 §5)

**Caso pratico — auto connessa:** Un automobilista acquista un veicolo connesso. Il produttore raccoglie continuamente dati (velocità, consumo, posizione, stile di guida, dati diagnostici). L'officina indipendente non riesce ad accedere ai dati tecnici del veicolo, disponibili solo tramite strumenti certificati dal produttore a costi elevati. Con il Data Act: l'automobilista ha il diritto di richiedere al produttore i propri dati di utilizzo in formato machine-readable; può condividerli con l'officina di fiducia; il produttore non può usare i dati di utilizzo per svantaggiare l'utente o per finalità non concordate. Lo stesso principio si applica a: macchinari industriali, elettrodomestici smart, dispositivi medici connessi, contatori smart, droni, edifici intelligenti. [fonte: PDF]

## Quadro d'insieme e coordinamento con GDPR

|                           | DSA                                      | DMA                                | Data Act                                |
| ------------------------- | ---------------------------------------- | ---------------------------------- | --------------------------------------- |
| **Chi regola**            | Intermediari online                      | Gatekeeper (grandi piattaforme)    | Produttori di prodotti connessi + cloud |
| **Cosa regola**           | Contenuti, responsabilità, moderazione   | Struttura dei mercati digitali     | Accesso e circolazione dei dati IoT     |
| **Autorità di vigilanza** | Commissione (VLOP/VLOSE) + DSC nazionale | Commissione (competenza esclusiva) | Autorità nazionale designata + EDIB     |
| **Sanzione massima**      | 6% fatturato mondiale                    | 10% / 20% in caso di recidiva      | Sanzioni nazionali «efficaci»           |
**In comune per tutti e tre:** [fonte: PDF]
- Applicazione extraterritoriale (valida per chi opera nell'UE, indipendentemente dalla sede)
- Coordinamento con il GDPR
- Commissione europea con ampi poteri di vigilanza

**Obiettivo finale**: creare uno spazio digitale europeo sicuro, equo, aperto e centrato sull'utente. [fonte: PDF]

## Riepilogo

**DSA**: il principio cardine è «ciò che è illegale offline è illegale online». Il DSA regola gli intermediari con obblighi proporzionati alla loro dimensione (dalla meno obbligata mere conduit alla più obbligata VLOP/VLOSE), mantiene il safe harbour, vieta i dark pattern e la pubblicità profilata ai minori, impone trasparenza sugli algoritmi di raccomandazione.

**DMA**: la logica è ex ante e preventiva. Il gatekeeper è designato dalla Commissione quando soddisfa tre criteri cumulativi (impatto significativo, ruolo di gateway, posizione consolidata). Ha obblighi strutturali (portabilità, interoperabilità) e divieti assoluti (self-preferencing, anti-steering, bundling forzato, tracciamento senza consenso). Sanzioni: fino al 10% del fatturato mondiale, 20% in caso di recidiva.

**Data Act**: il principio fondante è che i dati generati dall'uso di un prodotto connesso appartengono — in termini di accesso — all'utente, non al produttore. Il produttore deve consentire l'accesso gratuito e in tempo reale, in formato machine-readable; il passaggio tra fornitori cloud non deve comportare vendor lock-in; le switching fees saranno gratuite dal 12 settembre 2027.
