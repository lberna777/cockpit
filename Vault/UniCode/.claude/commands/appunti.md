---
description: "Elabora un modulo — teoria e sua pratica insieme — in appunti definitivi con diagrammi, e aggiorna lo stato. Uso: /appunti <CODICE> <ID>"
argument-hint: "<CODICE> <ID modulo> — es. FI2 02, SO 2B"
---

Il parametro passato è: "$ARGUMENTS"

---

**0. Risolvi corso e modulo, e trova il modulo accoppiato**

`$ARGUMENTS` va letto come **due token**: `<CODICE> <ID modulo>`.

- Primo token → codice corso, validato contro `piano/codici.txt`.
- Secondo token → identificativo del modulo.
- Se manca un token o il codice non è valido: mostra i codici da `codici.txt` e fermati.

**Modulo accoppiato** `[2026-09-21, su richiesta di Lorenzo]`. Un modulo con una parte pratica
produce **un solo file di appunti**, che copre teoria e pratica insieme. Non due file.

Risolvi la coppia da `corsi/<COD>/percorso.md`, sezione *Mappa teoria → pratica*: la colonna
*Segue* dice quale modulo di teoria una voce pratica accompagna (es. `02x` segue `02`).

- ID di teoria (`02`) → cerca chi lo *segue* fra esercitazioni, laboratori ed esercizi.
- ID pratico (`02x`) → risali al modulo di teoria che segue.
- Più voci pratiche sullo stesso modulo di teoria → includile **tutte**, nell'ordine della mappa.
- Nessuna voce pratica accoppiata → si procede sul solo modulo, come prima.

Dichiara a Lorenzo la coppia risolta prima di proseguire. Se la pratica non è ancora stata
svolta, **fermati e dillo**: gli appunti di un modulo accoppiato si scrivono *dopo* la pratica,
altrimenti la parte che conta — cosa è emerso eseguendo — non esiste ancora.

---

**1. Raccogli le fonti di ciò che Lorenzo ha prodotto**

Non c'è una sola fonte: ce ne sono tre, e servono tutte
`[2026-09-21, su richiesta di Lorenzo: «le mie domande e quello che hai notato tu»]`.

1. **Appunti grezzi** — `corsi/<COD>/grezzi/grezzi_<COD>_<ID>*.md` per ogni ID della coppia.
   Considera varianti di nome (maiuscole, underscore, spazi).
2. **La guida-lab annotata** — `corsi/<COD>/lezioni/guida_lab_<ID>_*.md`. Se Lorenzo ha scritto
   in linea nel file (risposte ai drill, output ottenuti, dubbi), quelle annotazioni valgono
   come appunti grezzi della parte pratica.
3. **La traccia della sessione** — ciò che **Claude** ha osservato mentre la pratica si svolgeva:
   `stato/giornata.md` e `log/giornate_dettaglio/<data>.md` per le date in cui il modulo è stato
   lavorato, più le occorrenze del modulo in `profilo/errori.md`. Qui stanno gli errori commessi
   a voce o durante i drill, le imprecisioni della fonte scoperte eseguendo, e i punti recuperati
   con guida — cose che negli appunti grezzi non ci sono perché Lorenzo, mentre sbagliava, non
   sapeva di sbagliare.

**Condizione per procedere**: serve almeno una delle tre. Se mancano tutte, comunicalo e fermati:
non c'è niente da elaborare. Se mancano i grezzi ma la traccia della sessione c'è, **si procede**
— e il file lo dichiara in testa, perché è un'informazione sul metodo, non un difetto.

---

**2. Carica il resto del contesto — in parallelo**

- **Lezione di riferimento**: `corsi/<COD>/lezioni/lezione_<ID>_*.md` (del modulo di teoria)
- **Le fonti del docente** usate da lezione e guida-lab, per estrarre le immagini al passo 4
- **Percorso del corso**: `corsi/<COD>/percorso.md` — stato dei moduli e prerequisiti
- **Errori ricorrenti**: `profilo/errori.md` — dove Lorenzo tende a sbagliare

---

**3. Analisi del file grezzo**

Identifica e annota (non scrivere ancora il file di output):

- **Domande aperte**: esplicite ("perché X?") o tra parentesi o quadre.
- **Lacune**: concetti presenti nella lezione ma assenti negli appunti grezzi. Ricorda:
  **l'assenza può essere intenzionale** — Lorenzo salta deliberatamente ciò che ha già
  consolidato. Non marcarla come lacuna finché non è verificata.
- **Errori di esecuzione**, per i corsi pratici: bug negli script o nei comandi (sintassi,
  logica invertita, keyword mancanti). Per i corsi formali: passaggi non giustificati, ipotesi
  usate senza verificarle, errori di segno o di unità. Confronta con i pattern in
  `profilo/errori.md` — se l'errore è già noto, **segnalalo esplicitamente come ricorrente**.
- **Imprecisioni di formulazione**, per i corsi discorsivi: definizioni parafrasate dove la
  fonte è precisa, riferimenti citati in modo errato, concetti confusi.
- **Punti di forza**: concetti che Lorenzo ha spiegato bene o intuizioni originali —
  segnalarli positivamente rafforza l'apprendimento.

---

**4. Crea il file di appunti definitivi**

Path: `corsi/<COD>/appunti/appunti_<ID>_<nome_breve>.md`, e per un modulo accoppiato
`corsi/<COD>/appunti/appunti_<ID teoria>+<ID pratica>_<nome_breve>.md`
(es. `appunti_02+02x_linguaggi_piattaforme.md`).

`<nome_breve>` deve corrispondere a quello usato nella lezione del modulo di teoria.

**Struttura, valida per ogni corso:**
- Segui l'ordine della lezione come ossatura.
- **La pratica si intreccia, non si appende** `[2026-09-21]`. Ciò che è emerso eseguendo va
  inserito nel punto della teoria che quel fatto illumina, non in una sezione «Parte pratica» in
  fondo. È lo stesso principio delle risposte integrate: un drill sul verso delle conversioni sta
  dentro il paragrafo sulle conversioni, con il caso concreto che l'ha chiarito. L'unica cosa che
  sta in fondo è l'esercizio completo, se il modulo ne ha uno.
- Per ogni domanda aperta: **integra la risposta nel testo**, nel punto in cui si tratta il
  concetto — la spiegazione si espande fino a contenerla. **Mai** in forma domanda-risposta, né
  come blocco citazione staccato, né raccolte in fondo (preferenza di Lorenzo dal 2026-09-15).
- Dove la fonte mostra un diagramma o un'immagine a cui il testo si riferisce (UML, schemi a
  strati, schermate): estrai la pagina dal PDF in PNG
  (`pdftoppm -f <p> -l <p> -png -r 110 '<pdf>' corsi/<COD>/appunti/img/<ID>_<nome>`) e inseriscila
  con `![didascalia](img/<file>.png)`, citando la slide.

**Diagrammi propri** `[2026-09-21, su richiesta di Lorenzo]`. Dove un concetto è **relazionale** —
una gerarchia, un verso, un flusso, una macchina a stati, un reticolo di conversioni — disegnalo,
invece di descriverlo in prosa. Il criterio per decidere se un disegno serve è uno: *l'informazione
sta in come le cose sono collegate?* Se sì, la prosa la nasconde e un grafo la mostra.

- **Formato obbligatorio: PNG generato con graphviz.** Scrivi il sorgente in
  `corsi/<COD>/appunti/img/<ID>_<nome>.dot`, poi
  `dot -Tpng -Gdpi=110 -o corsi/<COD>/appunti/img/<ID>_<nome>.png corsi/<COD>/appunti/img/<ID>_<nome>.dot`.
  Il `.dot` resta accanto al PNG: il disegno è così **deterministico e rigenerabile**, come i
  collegamenti di `link_modules.py`.
- **Mai Mermaid**, né altri blocchi che si renderizzano solo in Obsidian. Gli appunti passano da
  `/pdf-batch` (pandoc + xelatex): un blocco Mermaid finisce nel PDF come codice sorgente. Il PNG
  funziona in entrambi, e `--resource-path` è già configurato per `img/`.
- **Grafi orizzontali** (`rankdir=LR`). Verificato il 2026-09-21: una catena di sei nodi in
  verticale produce un PNG alto 7″ e xelatex avvisa `Float too large for page`; la stessa in
  orizzontale entra senza attributi. Se un grafo resta troppo alto, non forzare `{width=…}` —
  peggiora, perché la percentuale è sulla larghezza del testo e l'altezza cresce in proporzione:
  usa `{height=15cm}` o ridisegnalo orizzontale. Controllo: la conversione non deve stampare
  `Float too large`.
- Il diagramma va **commentato nel testo**: cosa guardare, e quale errore intercetta. Un disegno
  senza didascalia che dica dove cade l'occhio è decorazione.
- Testo dei nodi in italiano e leggibile a 110 dpi; niente colore come unico veicolo di
  informazione (gli appunti si stampano in bianco e nero).
- Per ogni sezione omessa dagli appunti grezzi che risulta davvero mancante: includila con
  `> ⚠️ Questa sezione non era presente negli appunti grezzi.`
- Per ogni punto di forza: `> ✅ Ottima osservazione: ...`

**Per i corsi pratici e formali** — aggiungi:
- Per ogni errore individuato: mostra la versione errata, l'analisi di *perché* è sbagliata, e
  la versione corretta. L'analisi conta più della correzione.
- Se l'errore corrisponde a un pattern noto:
  `> ⚠️ Errore ricorrente: stesso pattern di <modulo precedente>. Vedi profilo/errori.md`

**Per i corsi discorsivi** — aggiungi:
- Per ogni imprecisione: la formulazione di Lorenzo, la correzione, e il riferimento esatto
  alla fonte.
- In chiusura: "Domande di autoverifica — Risposte", se Lorenzo le ha incluse nel grezzo.

---

**5. Aggiorna `profilo/errori.md`**

Se sono emersi errori o imprecisioni:
- Pattern già presente → aggiungi il modulo alla riga esistente.
- Pattern nuovo, legato alla materia → nuova voce nella sezione del corso (creala se il corso
  non ne ha ancora una).
- **Se lo stesso modo di sbagliare compare in 3+ moduli, o si ripresenta su un corso diverso**
  → promuovilo alla sezione **Trasversale**, con la contromisura e la previsione di dove
  tornerà. È quella sezione che il briefing carica per prima.

---

**6. Registra l'evento e aggiorna lo stato**

Appendi a `stato/giornata.md` una riga per fatto. Se il modulo è stato completato, il marcatore
è obbligatorio:

```
HH:MM · <COD> · appunti <ID> elaborati: <n> domande risolte, <n> errori corretti, <n> diagrammi. CHIUSO <COD> <ID>
```

Il marcatore `CHIUSO` va scritto **solo con evidenza pratica**: per i corsi con laboratorio,
solo se Lorenzo ha eseguito gli esercizi in prima persona; per i corsi discorsivi, solo se ha
risposto alle domande di autoverifica. Verificalo dalle fonti del passo 1, non darlo per scontato.
Se l'evidenza manca, niente marcatore: scrivi la riga di evento e basta.

**Modulo accoppiato**: un marcatore **per ciascun ID** della coppia, su righe separate
(`CHIUSO FI2 02` e `CHIUSO FI2 02x`), perché il tracker segue i moduli uno per uno e i loro
ripassi scadranno insieme. Il criterio è quello di `CLAUDE.md` §7.2 applicato alla coppia: è la
pratica risolta **a freddo** che chiude entrambi. Se la pratica è stata svolta seguendo la
soluzione, non si chiude niente — né la pratica né la teoria.

> È da questi marcatori che `scripts/giornata.py` fa avanzare `stato/tracker.md` alle 23.
> Il tracker **non va modificato a mano da questo comando**.

Se `<COD>` è il corso attivo, aggiorna `stato/corrente.md`: stato del modulo e punto di ripresa.

---

**7. Verifica qualità (checklist interna)**

- [ ] Ogni domanda dagli appunti grezzi ha una risposta integrata nel testo, non in forma domanda-risposta
- [ ] **Modulo accoppiato**: un solo file per teoria + pratica, e la pratica è intrecciata nei
      paragrafi di teoria, non appesa in fondo
- [ ] **Le tre fonti del passo 1 sono state usate tutte** quelle disponibili: grezzi, guida-lab
      annotata, traccia della sessione. Gli errori visti da Claude durante l'esecuzione compaiono
      negli appunti, non solo in `profilo/errori.md`
- [ ] I diagrammi citati sono inseriti come immagini estratte dalla fonte
- [ ] **Ogni concetto relazionale ha il suo diagramma**, in PNG da graphviz con il `.dot` accanto;
      nessun blocco Mermaid; ogni diagramma ha la didascalia che dice dove guardare
- [ ] Il PDF regge: `pandoc … --pdf-engine=xelatex` non stampa `Missing character` e le immagini
      `img/…` sono risolte
- [ ] Nessuna sezione della lezione è stata saltata senza nota
- [ ] Gli errori hanno l'analisi del perché, non solo la correzione
- [ ] `profilo/errori.md` aggiornato dove serviva, con promozione a trasversale se ricorre
- [ ] La riga di evento è in `stato/giornata.md`, e il marcatore `CHIUSO` c'è **solo** con
      evidenza pratica

Poi invoca `lorenzo-skills:unicode-output-gate` per la verifica finale.

---

**8. Collega la nota al grafo**

Invoca `lorenzo-skills:unicode-link-note`: la nota riceve in testa il frontmatter
`tags: [<COD>, appunti]`, e se è la prima nota del corso si aggiunge il suo gruppo colore in Obsidian.

---

**9. Comunica il risultato**

- Path del file creato
- Conteggio: domande risolte, errori corretti, sezioni integrate, punti di forza segnalati
- Se il modulo è stato chiuso o è rimasto aperto, con la motivazione
- Se sono emersi errori ricorrenti, menzionali
