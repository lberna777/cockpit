# Appunti — Modulo D6: Contratto di Sviluppo Software — Analisi di Possibili Clausole
**Corso**: Diritto dell'Informatica T  
**Fonte**: `06_DirInfo_2026_SchemaContratt_DEF.pdf` (prof.ssa Cevenini)  
**Lezione di riferimento**: `claudeLezioni/LEZIONI DIRITTO/lezione_moduloD6_contratto_sviluppo_software.md`

---

## 1. Che tipo di contratto stiamo esaminando?

Il contratto esaminato è un **contratto d'opera intellettuale** per la consulenza avente ad oggetto lo sviluppo di un sistema software.

**Art. 2222 c.c. — Contratto d'opera**: «Quando una persona si obbliga a compiere verso un corrispettivo un'opera o un servizio, con lavoro prevalentemente proprio e senza vincolo di subordinazione nei confronti del committente».

**Art. 2230 c.c. — Contratto d'opera intellettuale**: «Il contratto che ha per oggetto una prestazione d'opera intellettuale».

> **Q: Non trovo la differenza di copertura che differenzia un'opera da un'opera intellettuale.**
>
> La distinzione è nella natura della prestazione:
> - Il **contratto d'opera** (art. 2222) riguarda qualsiasi opera o servizio eseguito con lavoro prevalentemente manuale o comunque personale — es. un artigiano che costruisce un mobile, un idraulico.
> - Il **contratto d'opera intellettuale** (art. 2230) riguarda prestazioni che implicano l'applicazione di conoscenze intellettuali specializzate — es. un avvocato, un architetto, un ingegnere informatico. La caratteristica decisiva è che il professionista applica competenze intellettuali che non sono replicabili meccanicamente.
>
> In termini di regime: il contratto d'opera intellettuale è regolato prima di tutto dagli artt. 2229–2238 c.c. (professioni intellettuali), poi — in quanto compatibili — dalle norme del contratto d'opera (artt. 2222–2228).
>
> **Distinzione pratica per il corso**: se lo sviluppo software è compiuto da un professionista-persona fisica → contratto d'opera intellettuale. Se è compiuto da un'**impresa** → contratto d'appalto di servizi (disciplina diversa, più vicina al diritto commerciale). La prof lo segnala esplicitamente come punto d'esame.

---

## 2. Parte Generale del Contratto

### 2.1 Parti del contratto

Occorre specificare i **soggetti** che concludono l'accordo:
- Persone fisiche: nome, cognome, data di nascita, residenza, C.F. e P.IVA.
- Persone giuridiche, enti e associazioni: sede legale, C.F., P.IVA e legale rappresentante.

### 2.2 Oggetto del contratto

Art. 1346 c.c.: l'oggetto del contratto deve essere **possibile, lecito, determinato o determinabile**.

> **Q: "determinato o determinabile" — cioè?**
>
> - **Determinato**: l'oggetto è specificato in modo preciso e completo già al momento della conclusione del contratto. Es.: "sviluppare un sistema di login con autenticazione a due fattori per piattaforma web, con specifiche tecniche allegate".
> - **Determinabile**: l'oggetto non è specificato completamente, ma il contratto indica i **criteri** con cui sarà determinato in futuro. Es.: "sviluppare il sistema X secondo le specifiche tecniche che saranno concordate entro 30 giorni dalla firma". La determinabilità è sufficiente purché sia possibile individuare l'oggetto senza necessità di un nuovo accordo tra le parti.
>
> Un oggetto vago ("sviluppare software gestionale") rischia di essere indeterminato e indeterminabile → clausola nulla per violazione dell'art. 1346.

Nell'ambito del software occorre specificare chiaramente:
1. quale software dovrà essere sviluppato (obiettivi, caratteristiche — eventualmente in un allegato tecnico);
2. in che modo verrà rilasciato (es. installato presso il cliente, SaaS via web);
3. a che titolo se ne prevede la realizzazione e consegna (es. cessione dei diritti di utilizzazione economica).

Se deve essere adattato un software già esistente, occorre specificare a quale titolo è utilizzato: l'ingegnere deve avere il diritto di modificarlo.

### 2.3 Natura del contratto — Le tre norme

> ⚠️ **Attenzione al titolo**: "Natura del contratto" ha due significati distinti che il PDF sovrappone.
>
> **Livello 1 — natura in senso teorico-generale** (già trattato nella sezione 1): classificazione giuridica del contratto — cos'è, qual è la sua causa, come si inserisce nella tassonomia del codice civile. Risposta già data: è un contratto d'opera intellettuale (artt. 2222 e 2230 c.c.).
>
> **Livello 2 — natura in senso soggettivo** (quello di questa sezione 2.3): i requisiti del *professionista* che rendono quel contratto valido e azionabile. Gli artt. 2229–2231 non definiscono cos'è il contratto, ma stabiliscono chi può stipularlo con effetti giuridici pieni. I due livelli sono connessi: affermare che questo è un contratto d'opera intellettuale implica già che il prestatore abbia il profilo soggettivo richiesto dall'art. 2229. Senza quel requisito, la classificazione regge ma il contratto produce effetti mutilati (art. 2231).

> **Q: Non capisco cosa comportino le tre norme incluse nella sezione "natura".**
>
> Le tre norme (artt. 2229, 2230, 2231 c.c.) servono a chiarire **chi può fare questo lavoro** e **con quali conseguenze** se non ne ha il titolo.
>
> **Art. 2229 c.c.** — stabilisce il principio generale: alcune professioni intellettuali richiedono l'iscrizione a un albo o elenco previsto dalla legge. La gestione di questi albi è affidata alle associazioni professionali, sotto vigilanza dello Stato.
>
> **Art. 2230 c.c.** — disciplina il contratto d'opera intellettuale: viene regolato prima dalle norme sulle professioni intellettuali (artt. 2229–2238), poi — in quanto compatibili — dalle norme del contratto d'opera. Le "disposizioni delle leggi speciali" restano salve (es. la legge sull'albo degli ingegneri).
>
> **Art. 2231 c.c.** — la norma più rilevante praticamente: se l'esercizio di una professione richiede l'iscrizione a un albo **e il professionista non è iscritto**, la prestazione eseguita **non gli dà azione per il pagamento**. In altre parole: l'ingegnere non iscritto che sviluppa il software non può chiedere il compenso in tribunale. Inoltre, se viene cancellato dall'albo mentre il contratto è in corso, il contratto si risolve automaticamente (salvo rimborso spese e compenso proporzionale all'utilità del lavoro compiuto).
>
> Perché importa? Perché queste norme fissano un **requisito soggettivo**: il contratto di sviluppo software con un ingegnere presuppone che questi sia iscritto all'albo. Se non lo è, rischia di lavorare gratis.

### 2.4 Albo degli ingegneri — Perché è rilevante nel diritto informatico

> **Q: Non capisco proprio cosa c'entri con gli argomenti che stiamo affrontando.**
>
> L'albo degli ingegneri è rilevante qui perché il contratto che stiamo analizzando è stipulato tra un **committente** (un'azienda o un privato che vuole il software) e un **ingegnere informatico** (il professionista che lo sviluppa). La prof lo analizza dalla prospettiva dell'ingegnere che un giorno firmerà questo tipo di contratto.
>
> Il D.P.R. 5 giugno 2001, n. 328 stabilisce che:
> - Sezione A (laurea specialistica) → ingegnere, piena autonomia professionale
> - Sezione B (laurea triennale) → ingegnere junior, con competenze più limitate
> - Ogni sezione è divisa in settori; il **settore dell'informazione** (quello di questo corso) include pianificazione, progettazione, sviluppo, collaudo e gestione di sistemi elettronici e di elaborazione delle informazioni.
>
> Nella pratica: se un ingegnere firma un contratto di sviluppo software e non è iscritto all'albo nel settore giusto, applica l'art. 2231 → non può chiedere il compenso. L'albo è quindi la **soglia di accesso** alla professione che rende valido il contratto d'opera intellettuale.

### 2.5 Responsabile dell'esecuzione

Utile (ma non obbligatorio) designare un referente/persona di contatto per ciascuna delle parti per ogni attività o questione inerente all'esecuzione del contratto.

---

## 3. Esecuzione dell'Opera

Il fulcro contrattuale: se il prestatore d'opera non procede secondo le condizioni stabilite e a regola d'arte, il committente può fissare un congruo termine entro il quale il prestatore **deve** conformarsi. Trascorso inutilmente il termine, il committente può **recedere dal contratto** (art. 2224 c.c.), salvo il diritto al risarcimento dei danni.

### 3.1 Fasi esecutive del software

Potrebbero essere indicate le fasi esecutive, ad esempio:
- Definizione Strategica → Pianificazione → Controllo di qualità → Analisi dei requisiti → Progettazione → Realizzazione e collaudo in fabbrica → Certificazione → Installazione → Collaudo del sistema installato → Esercizio → Diagnosi e manutenzione → Evoluzione → Messa fuori servizio

**N.B.** Le fasi esecutive possono essere indicate in documenti separati, allegati al contratto. Gli allegati devono essere sottoscritti da entrambe le parti e costituire parte integrante del contratto.

I **criteri di verifica** delle varie fasi sono molto importanti: in base ad essi si determinerà l'eventuale inadempimento dell'ingegnere rispetto agli obblighi assunti. Rendono chiaro cosa ci si aspetta in ogni momento dello sviluppo, evitando punti grigi.

### 3.2 Obblighi del committente

> **Q: "In che senso? Perché il committente dovrebbe consegnare qualcosa al commissionato?"**
>
> Perché il committente spesso possiede materiali senza i quali l'ingegnere non può lavorare. Esempi concreti:
> - Il committente ha un database esistente da integrare → deve fornire le credenziali e la struttura dei dati.
> - Il software deve interagire con un sistema legacy → il committente deve fornire documentazione tecnica o accesso al sistema.
> - Il software deve gestire l'immagine aziendale → il committente deve fornire loghi, colori, brand guidelines.
> - Il software deve rispettare normative settoriali specifiche → il committente deve fornire le specifiche di conformità.
>
> Il contratto deve indicare *cosa* fornire e *entro quando*: se il committente non fornisce i materiali nei tempi stabiliti, l'ingegnere ha un alibi contrattuale per il ritardo.

> **Q: "Cosa c'entrano terzi? Fai un esempio."** (clausola di indennizzo)
>
> La clausola di indennizzo protegge l'ingegnere da rivendicazioni di **terzi** relative ai materiali che il committente gli ha fornito. Esempio:
>
> Il committente fornisce all'ingegnere del codice sorgente che sostiene essere suo. L'ingegnere lo integra nel software sviluppato. Dopo la consegna, una terza azienda sostiene che quel codice era suo e brevettato → minaccia una causa sia al committente che all'ingegnere. La clausola di indennizzo fa sì che sia il **committente** a rispondere di questa pretesa, non l'ingegnere: questi non poteva sapere che il codice era di terzi.

---

## 4. Garanzie e Responsabilità

### 4.1 Difformità e vizi dell'opera (art. 2226 c.c.)

> **Q: "Classifichiamo chiaramente cosa sono le difformità e cosa sono i vizi."**
>
> - **Difformità**: il risultato ottenuto *non corrisponde* a quanto pattuito nelle specifiche. Il difetto sta nel confronto con il contratto, non nell'opera in sé — il software può funzionare correttamente e restare utilizzabile, ma non rispetta i parametri concordati. Es.: il contratto prevedeva che il sistema gestisse 10.000 utenti concorrenti, ma ne gestisce solo 1.000. Il sistema è stabile e non ha bug, ma non rispetta le specifiche — si può usare con 1.000 utenti, non è inutilizzabile.
> - **Vizi**: difetti *intrinseci* dell'opera che la rendono instabile o inadatta indipendentemente da quanto dicevano le specifiche. Il difetto sarebbe un problema anche se le specifiche non avessero mai menzionato quel comportamento. Es.: il software ha un bug ricorrente che causa crash non prevedibili; produce risultati errati; ha un memory leak. Il vizio può essere *palese* (visibile a un esame ordinario) o *occulto* (non rilevabile se non con un esame approfondito o dopo un certo utilizzo).
>
> **La distinzione chiave**: difformità = scarto rispetto al contratto (l'opera funziona, ma non è quella pattuita); vizio = difetto interno all'opera (l'opera è rotta). L'inutilizzabilità può essere conseguenza di un vizio grave, ma non è la definizione di vizio — e non caratterizza mai la difformità.

> **Q: "Non capisco grammaticalmente la frase dell'art. 2226, non capisco proprio cosa dica."**
>
> La frase è densa — scomponiamola:
>
> «L'accettazione espressa o tacita dell'opera libera il prestatore d'opera dalla responsabilità per difformità o per vizi della medesima, *se all'atto dell'accettazione questi erano noti al committente o facilmente riconoscibili*, purché in questo caso non siano stati dolosamente occultati.»
>
> Traduzione pratica:
> 1. Se il committente **accetta** il software (esplicitamente firmando, o tacitamente pagando e usando), l'ingegnere è liberato dalla responsabilità per difformità e vizi **che il committente già conosceva o avrebbe potuto riconoscere facilmente** al momento dell'accettazione.
> 2. **Eccezione**: se l'ingegnere ha *dolosamente occultato* i difetti (li nasconde intenzionalmente), la liberazione non vale — risponde ugualmente.
> 3. Per i **vizi occulti** (non riconoscibili all'atto dell'accettazione): il committente deve denunciarli entro 8 giorni dalla scoperta, a pena di decadenza.
>
> In sintesi: accettare il software senza contestare i difetti visibili equivale a rinunciare alla garanzia per quei difetti.

> **Q: "Cosa significa che l'azione si prescrive dopo un anno dalla consegna?"**
>
> **Decadenza** (8 giorni dalla scoperta) e **prescrizione** (1 anno dalla consegna) sono due termini diversi che agiscono in sequenza:
>
> - **Decadenza**: entro 8 giorni dalla *scoperta* del vizio occulto, il committente deve *denunciarlo* all'ingegnere. Se non lo fa, perde il diritto di far valere quel vizio — definitivamente, senza possibilità di recupero.
> - **Prescrizione**: anche se ha denunciato il vizio in tempo, il committente ha poi al massimo **1 anno dalla consegna** per esercitare l'azione in giudizio (chiedere al giudice la riduzione del prezzo, l'eliminazione del vizio, ecc.). Dopo un anno dalla consegna, l'azione è prescritta anche se aveva denunciato il vizio in tempo.
>
> Esempio: software consegnato il 1 gennaio. Vizio occulto scoperto il 15 novembre → va denunciato entro il 23 novembre. Anche dopo la denuncia, l'azione in giudizio si prescrive il 1 gennaio dell'anno successivo.

Il committente è tutelato dall'**art. 1668 c.c.** (richiamato dall'art. 2226): può chiedere che i vizi siano eliminati a spese dell'appaltatore, oppure che il prezzo sia proporzionalmente diminuito, salvo risarcimento del danno in caso di colpa. Se le difformità o vizi rendono l'opera del tutto inadatta alla sua destinazione, il committente può chiedere la **risoluzione del contratto**.

### 4.2 Diligenza e responsabilità del professionista

> ⚠️ Questa sezione non era presente negli appunti grezzi. È integrata dalla lezione.

**Art. 1176 c.c. — Diligenza nell'adempimento**: il debitore deve usare la diligenza del buon padre di famiglia. Per le **obbligazioni professionali**, la diligenza si valuta con riguardo alla natura dell'attività esercitata (standard più elevato rispetto al privato comune).

**Art. 2236 c.c. — Responsabilità limitata per problemi di speciale difficoltà**: se la prestazione implica la soluzione di problemi tecnici di speciale difficoltà, il prestatore d'opera non risponde dei danni se non in caso di **dolo o colpa grave**. Per gli inadempimenti ordinari (non di speciale difficoltà) risponde invece per colpa lieve. Questo è uno dei "privilegi" del professionista intellettuale.

### 4.3 Clausola di garanzia e garanzia di conformità

> **Q: "Cosa si considera software di terzi o prodotti da terzi?"**
>
> Software di terzi o prodotti da terzi = componenti che l'ingegnere non ha sviluppato lui, ma ha integrato nel sistema da librerie esterne, framework open source, API di altri provider, plugin, componenti commerciali. Esempi: una libreria di crittografia open source integrata nel software, un'API di pagamento di Stripe, un motore di database come PostgreSQL.
>
> L'ingegnere tipicamente non garantisce per questi componenti perché non ne controlla il codice, lo sviluppo né i bug: quella responsabilità appartiene ai rispettivi autori o fornitori. La clausola serve a rendere esplicita questa esclusione.

**Garanzia di conformità**: l'ingegnere garantisce che il software funzionerà in modo conforme agli allegati tecnici per un determinato periodo di tempo (es. 60 giorni dalla consegna). Esclusioni tipiche: uso del software secondo modalità diverse da quanto indicato nel contratto; malfunzionamento dell'hardware.

### 4.4 Responsabilità per danni

Occorre indicare entro quali limiti si risponde di eventuali danni causati al committente o a terzi:
- limitazione ai **danni diretti effettivamente causati**, fino a un massimo contrattualmente stabilito (es. TOT euro);
- **esclusione** di mancato guadagno, interruzione dell'attività, danno all'immagine.

---

## 5. Manutenzione e Formazione

### 5.1 Manutenzione software

Occorre specificare:
- se si forniscono servizi di **correzione** o soluzione alternativa per problemi che impediscano al software di funzionare conformemente alle specifiche, indicando i casi in cui tali servizi non saranno erogati;
- se si forniranno **aggiornamenti** del software;
- se si forniranno servizi di **assistenza** relativa agli aggiornamenti e agli interventi correttivi (in loco, da remoto, via telefono, ecc.).

### 5.2 Formazione

Specificare se verranno erogati servizi di formazione del personale preposto all'uso del software, individuando le modalità (luogo, durata, periodicità, strumenti di formazione).

---

## 6. Variazioni al Software

### 6.1 Variazioni richieste (dal committente, volontarie)

Occorre specificare se e in che misura il committente può apportare variazioni alle specifiche tecniche del software, indicando:
- la modalità della richiesta (es. PEC, raccomandata a/r, fax, verbale sottoscritto, e-mail);
- i tempi entro i quali le variazioni non necessarie possono essere richieste.

### 6.2 Variazioni necessarie (per eventi imprevedibili)

> **Q: "Non capisco se l'art. 2228 dice sostanzialmente questa cosa o altro."**
>
> Sono due concetti distinti che la lezione tratta insieme:
>
> **Art. 2228 c.c. — Impossibilità sopravvenuta**: disciplina il caso in cui l'esecuzione dell'opera diventa *impossibile* per causa non imputabile a nessuna delle parti (es. forza maggiore, cambiamento normativo improvviso). In questo caso il contratto non può più essere eseguito, e il prestatore ha diritto a un compenso commisurato all'utilità del lavoro già compiuto. Non è un diritto al compenso pieno, ma proporzionale.
>
> **Le variazioni necessarie** (trattate nel PDF insieme all'art. 2228) sono invece il caso in cui l'esecuzione *non diventa impossibile* in assoluto, ma eventi sopravvenuti imprevedibili rendono necessario modificare le specifiche o i tempi — es. cambia una normativa tecnica di riferimento, il committente cambia il sistema hardware su cui gira il software. Qui il contratto può continuare, ma va adeguato.
>
> La differenza: **art. 2228** = impossibilità totale → risoluzione + compenso proporzionale. **Variazioni necessarie** = difficoltà sopravvenuta → rinegoziazione, e solo se le variazioni sono troppo onerose si arriva al recesso con indennità.

---

## 7. Diritti di Proprietà Intellettuale

### 7.1 Cessione vs licenza

Il titolo in base al quale il committente ottiene il software:

- **Cessione**: l'ingegnere trasferisce al committente tutti (o alcuni) diritti di utilizzazione economica. Trasferendo tutti i diritti, l'ingegnere non disporrà più del software e non potrà ulteriormente svilupparlo o commercializzarlo.
- **Licenza d'uso o concessione**: al committente è data la possibilità di utilizzare il software a determinate condizioni.

> **Q: "In caso di licenza — e quindi non di vendita diretta del software?"**
>
> Esatto. La licenza non è una "vendita" — l'ingegnere rimane titolare del software. Il committente ottiene solo il diritto di *usarlo* secondo le condizioni stabilite. È esattamente lo stesso principio delle licenze di software commerciale (es. Microsoft Office: non lo possiedi, lo usi). La cessione invece equivale alla "vendita": l'ingegnere cede la titolarità e non può più usarlo liberamente.

### 7.2 Titolarità dei diritti di proprietà intellettuale

Occorre concordare quale parte diverrà titolare dei diritti di utilizzazione economica del software e specificare:
- se e quale uso potrà fare la parte **non titolare** (es. l'ingegnere potrebbe voler riutilizzare determinate componenti per lavori futuri);
- quali materiali, software, informazioni le parti già possedevano **prima** dell'inizio del contratto.

> **Q: "Non ha capito cosa discute il secondo punto."** (materiali pre-esistenti)
>
> Il secondo punto riguarda i **componenti pre-esistenti** che ciascuna parte porta dentro il progetto. Es.:
> - L'ingegnere usa una sua libreria di utility che aveva sviluppato in precedenti progetti → quella libreria era sua *prima* del contratto: resta sua anche dopo. Il contratto deve chiarirlo, per evitare che il committente pretenda di aver acquisito anche quella libreria con la cessione.
> - Il committente ha un database preesistente che viene integrato → quel database resta del committente.
>
> Senza questa clausola, chi ha diritto su cosa una volta concluso il contratto diventa controverso.

### 7.3 In caso di licenza: elementi da specificare

- periodo di validità della licenza;
- esclusiva o non esclusiva;
- sub-licenza ammessa o meno;
- numero di installazioni ammesse;
- finalità di utilizzo;
- luogo ammesso per l'utilizzo;
- tipo di utilizzo (in locale o in rete);
- divieto di tradurre, scomporre, disassemblare il codice.

---

## 8. Consegna e Verifica del Software

### 8.1 Consegna

Occorre indicare:
- la data di consegna del software ultimato ed eventuali date intermedie per consegna di componenti;
- se è predisposto un piano di avanzamento lavori (in allegato o come specificazione nel piano di esecuzione);
- se il software sarà consegnato in **codice oggetto** (eseguibile compilato, non modificabile) o **codice sorgente** (codice leggibile, modificabile).

### 8.2 Verifica del software

> **Q: "Spiega meglio il processo di verifica: dove si inserisce temporalmente? Viene testato da chi commissiona? Come è possibile se quando il software viene consegnato si dichiara concluso il contratto?"**
>
> La verifica **non coincide** con la conclusione del contratto — è una fase *intermedia* o *finale* che precede l'accettazione definitiva. Lo schema tipico è:
>
> 1. L'ingegnere **consegna** il software (o una parte di esso).
> 2. Il committente lo **verifica** secondo i criteri stabiliti nel contratto (test funzionali, benchmark, conformità alle specifiche dell'allegato tecnico). Questa fase ha una durata stabilita contrattualmente.
> 3. Se la verifica ha **esito positivo**: il committente accetta quella parte di software. A seconda di quanto stabilito, la verifica positiva può anche implicare il trasferimento dei diritti di utilizzazione economica da quel momento in poi.
> 4. Se la verifica ha **esito negativo**: il committente segnala le difformità → l'ingegnere le corregge → nuova verifica.
>
> La verifica può avvenire in più round (per fasi intermedie) o una sola volta alla consegna finale. È fondamentale perché l'accettazione tacita (usare il software senza contestare) può liberare l'ingegnere dalla responsabilità per i difetti visibili (art. 2226 c.c.).

---

## 9. Compenso e Pagamento

**Determinazione del compenso**: le parti lo stabiliscono nel contratto o fissano i criteri (es. tot euro a ora/giornata). Se non concordano, il giudice lo determina in relazione al risultato ottenuto e al lavoro normalmente necessario per ottenerlo.

**Spese e acconti**:

> **Q: "Saldo finale — in che senso?"**
>
> Il modello tipico è: il committente versa una serie di acconti durante lo sviluppo (es. 30% alla firma, 30% alla metà progetto, 30% alla consegna) e poi un **saldo finale** — cioè la quota residua del compenso totale — al momento della consegna e accettazione del software. Es.: compenso totale 10.000€; tre acconti da 3.000€ = 9.000€ versati; saldo finale = 1.000€ alla consegna.

**Servizi aggiuntivi**:

> **Q: "Non possono essere parte del contratto?"**
>
> Possono esserlo, ma solo se inclusi esplicitamente nell'oggetto. La clausola "servizi aggiuntivi" serve per i servizi che **non** sono nell'oggetto principale (es. il contratto prevede solo lo sviluppo, non la manutenzione). Se il committente vuole anche la manutenzione, o paga un extra concordato a parte, o si stipula un contratto separato. La clausola evita che il committente pretenda manutenzione gratuita "inclusa nel contratto" quando non era stata prevista.

**Modalità di pagamento**: indicare la modalità (bonifico, assegno) e specificare gli effetti del mancato o ritardato pagamento:
- se l'ingegnere ha diritto di recedere dal contratto;
- se può chiedere la restituzione di quanto già consegnato e non pagato;
- se può sospendere l'esecuzione del software.

---

## 10. Durata, Recesso e Risoluzione

**Durata**: indicare il periodo di validità del contratto e quali pattuizioni hanno effetto anche dopo la scadenza (es. riservatezza).

**Recesso**: in caso di prestazione d'opera, il committente può recedere rimborsando all'ingegnere le spese sostenute, il compenso per l'opera svolta e un **indennizzo per il mancato guadagno**. Occorre indicare le modalità di comunicazione (es. in forma scritta).

### Risoluzione del contratto

#### I tre modi di risoluzione (codice civile)

| Modo | Articolo | Causa | Effetto |
|------|----------|-------|---------|
| **Per inadempimento** | Art. 1453 | Una parte non esegue la prestazione dovuta | La parte lesa può scegliere tra esigere l'adempimento o chiedere la risoluzione, in entrambi i casi con risarcimento del danno. Una volta chiesta la risoluzione non si può tornare a chiedere l'adempimento. |
| **Per impossibilità sopravvenuta** | Art. 1463 | La prestazione diventa impossibile per causa non imputabile a nessuna delle parti (es. forza maggiore, evento imprevedibile) | Il contratto si scioglie; la parte liberata non può chiedere la controprestazione e deve restituire quanto già ricevuto. Nessun risarcimento perché nessuno è in colpa. |
| **Per eccessiva onerosità sopravvenuta** | Art. 1467 | Events straordinari e imprevedibili rendono la prestazione di una parte eccessivamente onerosa rispetto all'altra | La parte gravata può chiedere la risoluzione; la controparte può evitarla offrendo di ricondurre il contratto a equità. |

#### Strumenti contrattuali che operano all'interno della risoluzione per inadempimento

Artt. 1456 e 1457 non sono modi autonomi di risoluzione: sono **clausole inseribili nel contratto** che rendono automatica la risoluzione per inadempimento, eliminando la necessità di ricorrere al giudice.

| Articolo | Nome | Come funziona | Applicazione nel contratto di sviluppo software |
|----------|------|---------------|------------------------------------------------|
| **Art. 1456** | Clausola risolutiva espressa | Le parti stabiliscono nel contratto che l'inadempimento di una specifica obbligazione risolve il contratto di diritto. La risoluzione non è automatica: opera quando la parte interessata *dichiara* all'altra di volersi avvalere della clausola. | Es.: "Il mancato pagamento dell'acconto entro X giorni risolve il contratto di diritto." Tutela principalmente l'ingegnere contro il committente che non paga. |
| **Art. 1457** | Termine essenziale | Le parti dichiarano nel contratto che un certo termine è "essenziale": se scade senza adempimento, il contratto si risolve di diritto. La parte che vorrebbe comunque l'esecuzione deve comunicarlo entro **3 giorni** dalla scadenza, altrimenti perde il diritto. | Es.: "La consegna entro il 31 marzo è termine essenziale." Se l'ingegnere non consegna, il committente non deve fare nulla — il contratto è già risolto, salvo che comunichi entro 3 giorni di voler comunque il software. |

#### Effetti della risoluzione (art. 1458)

Art. 1458 non è un modo di risoluzione ma la norma che descrive cosa succede *dopo* che la risoluzione si è verificata per qualunque causa.

**1. Effetto retroattivo tra le parti**

La risoluzione cancella il contratto come se non fosse mai esistito: chi ha pagato riavuto i soldi, chi ha consegnato riavuto l'oggetto. La retroattività opera però solo tra le parti contraenti.

**2. Eccezione: contratti a esecuzione continuata o periodica**

Per le prestazioni già eseguite e consumate la restituzione non ha senso — non si "restituisce" un servizio già fruito.

- **Esecuzione continuata**: la prestazione si svolge ininterrottamente nel tempo. Es.: contratto di hosting — il server è attivo ogni secondo.
- **Esecuzione periodica**: la prestazione si ripete a scadenze discrete. Es.: contratto di manutenzione mensile del software.

Per questi contratti la risoluzione opera solo dal momento in cui viene dichiarata, non a ritroso: il compenso già incassato per i periodi precedenti resta all'ingegnere, il committente tiene il beneficio già ricevuto.

Una **licenza a tempo indeterminato** rientra nell'esecuzione continuata: l'obbligazione del licenziante non è "consegnare il software" (atto istantaneo) ma mantenere il diritto d'uso in capo al licenziatario per tutta la durata del contratto — prestazione che si protrae ininterrottamente. Se la licenza viene risolta, il licenziatario non deve "restituire" l'uso già fruito e il licenziante tiene i canoni già incassati.

Nel contratto di sviluppo a fasi: se le prime due fasi sono state consegnate, verificate, accettate e pagate, una risoluzione sulla fase 3 non travolge le prime due.

**3. La risoluzione non pregiudica i diritti dei terzi**

La retroattività opera solo tra le parti — non può essere opposta a chi ha acquisito diritti da quel contratto in buona fede.

Esempio: l'ingegnere sviluppa software per Committente A, che ne acquisisce la licenza d'uso. A sublicenzia il software ad Azienda B. Sorge una controversia tra ingegnere e A → contratto risolto per inadempimento di A. La risoluzione cancella i diritti di A, ma non travolge la sublicenza di B: B aveva acquisito quel diritto in buona fede durante la vigenza del contratto, senza essere responsabile della controversia.

Si crea così il paradosso apparente per cui B ha un diritto che A non ha più. Non è un paradosso: B lo aveva acquisito *mentre A lo aveva legittimamente*, e quella finestra temporale è sufficiente a consolidare il diritto di B indipendentemente da cosa succede dopo.

A potrebbe teoricamente riacquistare i diritti da B, ma si tratterebbe di un'operazione nuova e autonoma — trattando con B come con qualsiasi terzo, al prezzo che B decide. L'ingegnere non può impedirlo: i diritti di B sono consolidati e B è libero di disporne, incluso rivenderli ad A.

L'unica tutela dell'ingegnere è contrattuale: inserire nel contratto originario con A una clausola che limiti o vieti la sublicenza, oppure che preveda che in caso di risoluzione i diritti concessi a terzi tornino automaticamente all'ingegnere. Senza quella clausola il codice civile non offre strumenti per bloccare questo scenario.

Il limite della tutela dei terzi: opera solo se il terzo ha acquisito i diritti **in buona fede** — senza sapere dell'inadempimento o della controversia in corso. Chi acquisisce diritti sapendo che il contratto originario è già in discussione non è protetto.

**Modifiche del contratto**: indicare come dovranno essere stabilite e formalizzate (es. solo per iscritto, raccomandata A/R, PEC).

**Cessione del contratto**: possibilità o meno di affidare ad altri il lavoro commissionato (analogo al subappalto negli appalti). Se il committente si è rivolto a un determinato ingegnere per fiducia nelle sue competenze, può preferire che il contratto non sia cedibile.

---

## 11. Legge Applicabile, Privacy e Riservatezza

### 11.1 Legge applicabile e foro competente

> **Q: "Si può scegliere a piacere?"**
>
> Per contratti tra soggetti italiani: no, non c'è vera scelta — la legge applicabile è quella italiana. La clausola è rilevante principalmente per contratti **internazionali**, dove le parti (una italiana e una straniera) devono scegliere quale ordinamento governa il contratto (es. legge italiana o legge inglese). Nei contratti tra consumatori e professionisti operano regole speciali che limitano la scelta.

> **Q: "Foro — il cosa?"**
>
> Il **foro competente** (o foro convenzionale) è il **tribunale territorialmente competente** a decidere in caso di controversia sul contratto. In Italia ci sono decine di tribunali (Milano, Bologna, Roma, ecc.): il foro competente stabilisce a quale ci si deve rivolgere. Se non è specificato, si applicano i criteri legali di competenza territoriale (es. residenza del convenuto). Scegliere il foro di Bologna anziché Palermo può fare una grande differenza pratica in termini di costi e tempi.

### 11.2 Trattamento dei dati personali

> **⚠️ Imprecisione negli appunti grezzi**:
>
> Lorenzo scrive: «i dati personali in questo caso sono i dati dell'ingegnere».
>
> **Correzione**: i dati personali oggetto della clausola non sono quelli dell'ingegnere, ma quelli di **terzi** a cui l'ingegnere potrebbe avere accesso durante lo sviluppo del software. Es.: l'ingegnere sviluppa un software gestionale per un'azienda che ha un archivio di 10.000 clienti con nome, email, dati di acquisto. Per sviluppare il software, l'ingegnere ha accesso a quell'archivio → sta trattando dati personali di terzi (i clienti dell'azienda). In questo caso, il GDPR impone che l'azienda (titolare del trattamento) nomini formalmente l'ingegnere come **responsabile del trattamento** (art. 28 GDPR), disciplinando contrattualmente come tratterà quei dati.

> **Q: "Non sta all'azienda dire cosa lui può e non può fare con questi dati, oltre alle leggi generali?"**
>
> Esatto, e non solo. Il GDPR (art. 28) impone che il contratto tra titolare (azienda) e responsabile (ingegnere) specifichi obbligatoriamente: l'oggetto e la durata del trattamento, la natura e la finalità, il tipo di dati personali e le categorie di interessati, e gli obblighi e i diritti del titolare. Quindi sì: è l'azienda a fissare le regole, ma il contratto deve documentarle in modo preciso. Non basta la conformità generica alle leggi — serve un atto contrattuale specifico.

### 11.3 Clausola di riservatezza

Può essere prevista una clausola che vieta all'ingegnere di comunicare a terzi informazioni riservate apprese durante il contratto. Questo obbligo può essere esteso **oltre la durata del contratto**.

**Attenzione alla formulazione**: se l'ingegnere non può neppure fare menzione del fatto che ha sviluppato un software per un determinato committente, questo può costituire una limitazione per il suo curriculum.

---

## Nota d'esame — "Attenzione ripasso!!!" (dall'ultima slide del PDF)

> ⚠️ Questa sezione non era presente negli appunti grezzi. È integrata dalla lezione — importante per l'esame.

La professoressa segnala esplicitamente che all'esame potrebbe chiedere:

1. **In che cosa consiste il contratto di sviluppo software?** → Attenzione: ciò che abbiamo esaminato è un contratto d'opera intellettuale (sviluppatore = professionista). Se il programma fosse sviluppato da un'**impresa** si tratterebbe di contratto d'appalto di servizi — disciplina diversa.

2. **Quali clausole ritenete più importanti a vostra tutela (come ingegnere) e perché?** → Risposta possibile: oggetto dettagliato (delimita i confini del lavoro), criteri di verifica (determina l'inadempimento), limitazione responsabilità per danni (cap al risarcimento), esclusione garanzia su software di terzi, clausola di pagamento (recesso per mancato pagamento).

3. **Cosa succederebbe se il contratto consistesse semplicemente in un preventivo accettato con timbro e firma senza clausole dettagliate?** → Il contratto è valido (accordo + corrispettivo + oggetto), ma mancano le tutele: nessun limite alla responsabilità, nessuna definizione delle fasi, nessuna garanzia di conformità, nessun termine essenziale, nessuna disciplina della proprietà intellettuale → controversie affidate interamente al giudice e al codice civile suppletivo, con esiti imprevedibili.

**Parti da ripassare secondo la prof**: contratto d'opera, oggetto, esecuzione dell'opera (fasi esecutive), obblighi del committente, garanzie e responsabilità, responsabilità per danni, variazioni richieste e necessarie, diritti di proprietà intellettuale, recesso delle parti, risoluzione del contratto.

---

## Domande di Autoverifica

> ⚠️ Le domande di autoverifica non sono state ancora compilate negli appunti grezzi (Lorenzo le risponderà durante lo studio di questi appunti). Le domande sono tratte dalla lezione D6.

1. Quale è la differenza tra un contratto di sviluppo software qualificato come contratto d'opera intellettuale e uno qualificato come contratto d'appalto di servizi? Che conseguenze ha questa distinzione?

2. Cosa prevede l'art. 2231 c.c. nel caso in cui l'ingegnere che ha sviluppato il software non sia iscritto all'albo professionale? E nel caso di cancellazione successiva dall'albo?

3. Quali sono le differenze tra "variazioni richieste" e "variazioni necessarie" nel contratto di sviluppo software? Quale articolo del codice civile governa le variazioni necessarie e qual è il suo contenuto?

4. In che cosa consiste la differenza tra cessione dei diritti di utilizzazione economica e licenza d'uso? Quali elementi specifici devono essere indicati in caso di licenza?

5. Descrivi i meccanismi di risoluzione del contratto previsti dagli artt. 1456, 1457 e 1458 c.c. e spiega come ciascuno di essi può essere rilevante in un contratto di sviluppo software.

---

## Riepilogo

- Il contratto di sviluppo software esaminato è un **contratto d'opera intellettuale** (artt. 2222, 2230 c.c.): lo sviluppatore è un professionista che lavora in autonomia, senza subordinazione; se l'autore fosse un'impresa si applicherebbe invece il contratto d'appalto di servizi.
- La **definizione dettagliata dell'oggetto**, delle fasi esecutive e dei criteri di verifica è il presidio principale contro le controversie: determina cosa è incluso nel compenso e stabilisce i parametri per valutare l'inadempimento.
- I **diritti di proprietà intellettuale** sul software devono essere disciplinati esplicitamente: in assenza di accordo, la titolarità segue le regole del diritto d'autore; cessione e licenza hanno effetti radicalmente diversi per entrambe le parti.
