---
tags: [FI2, grezzi]
---

# Grezzi — FI2 01: Dai linguaggi alle infrastrutture software

**Data**: 2026-09-15
**Fonte**: `lezione_01_linguaggi_infrastrutture.md` ← `materiali/slide/01-x1-Intro.pdf`

---

## Autoverifica a freddo — risposte di Lorenzo (testo originale)

**1. Perché «programmare» richiama una visione obsoleta? Cosa distingue in-the-small da in-the-large?**
il compito di chi sviluppa un applicativo, un softwere, risulta sempre piu simile all'organizzazione industriale rispetto alla programmazione di per se. si deve partire da un progetto, con una visione di insieme, funzionalità che devono convivere funzionando, in ambienti diversi e in tutti i casi possibili. bisogna mantere organizzazione mantenendo traccia delle versioni.

**2. Un test JUnit non passa: quali esiti, cosa li distingue, dove cerchi l'errore?**
quando non passa un test JUnit, si classifica come failure, se al test arriva un risultato, per quanto sbagliato, e un error, se l'esecuzione si blocca per colpa di un fatal error, in questo caso il problema è spesso sintattico, legato alla scrittura formale del codice, mentre nel caso di una failure, l'errore è tipicamente logico, legato alle funzioni da noi scritte con qualche errore logico.

**3. Bus 33: avrebbe aiutato un collaudo più accurato?**
si, in questo caso un collaudo più "estremo" avrebbe potuto notare la dimenticanza nella considerazione delle line di bus circolari. il progetto va preparanto anteriormente allo sviluppo e per qunto se ne sarebbero potuti accorgere gia in questa fase, il collaudo esiste apposta per far emergere problemi legati all'uso pratico dell'applicativo.

**4. Solo JRE installato: cosa puoi fare con un JAR, cosa no con un `.java`? I due livelli del JRE?**
non mi è chiaro il layering di pezzi che compongono java, ma ne parliamo quando dopo scriviamo gli appunti.

**5. Perché un JAR è «eseguibile quanto un EXE»? Link statico vs dinamico.**
come per un EXE, che è preparato a funzionare su un sistema creato in un modo specifico, e quindi necessita di quell'ambiente o uno analogo. un JAR ha bisogno della sottostruttura di java installata per poter runnare. nel primo caso le librerie e i pezzi di codice necessari a funzionare sono hardcodati dentro all'eseguibile, nel caso di java, questi vengono scaricati e chiamati solo quando effettimanete utili

---

## Esito della correzione — 2026-09-15

| # | Esito | Punto |
|---|---|---|
| 1 | parziale | idea generale giusta; manca la risposta sulla coppia *in-the-small / in-the-large* |
| 2 | parziale | classificazione giusta; **error ≠ errore sintattico** (confusione compilazione / esecuzione) |
| 3 | **errata** | è il caso che il docente usa per separare collaudo e progetto: la risposta li fonde |
| 4 | non data | layering JVM / JRE / JDK non chiaro — **da affrontare negli appunti** |
| 5 | buona | imprecisione: i componenti non vengono «scaricati», vengono *caricati e collegati* a run-time |

**Modulo 01: resta 🔶.** Da rifare a freddo dopo gli appunti: domande **2, 3, 4**.

## Domande aperte per `/appunti`

- Il layering di Java: cosa sono JVM, JRE e JDK, e come si incastrano (domanda 4).
- Se un errore di sintassi non produce un *error* di JUnit, cosa lo produce? E cosa succede ai test se il codice non compila?
- Quale collaudo avrebbe potuto trovare il problema del 33, se non quello scritto sul progetto?

## Domande di Lorenzo per gli appunti — 2026-09-15 (testo originale)

> Formato richiesto: risposte integrate nel testo degli appunti, non in forma domanda-risposta.

per primo non mi è chiara la distinzione tra black box testing e white box, ovvero la differenza tra comportamenteo esterno indipendente dalla realizzazione, e la correttezza dell implementazione delle varie funzioni tenendo in conto com'è fatto dentro un componente. poi vorrei sviscerato l'argomento build tools, in qualche corso ho usato meaven, ma se devo essere sincero non ho mai capito di cosa si tratta. poi ti volevo far notare come fai riferimenti a UML, diagrammi di struttura, e rappresentazioni estetiche, che pero non sono riportate negli appunti, e reputo sarebbero utili come immagini inserite negli appunti per capire di cosa stiamo parlano. Sucessivamente, trattiamo le idee prese dal mondo funzionale, che dici elencate a slide 53, voglio approfondire le terminologie e la forma delle strutture base di java per conoscerle bene prima di usarle. Aggiungiamo una classificazione, magari con grafico, dei layer che compongono java, parli di JVM JRE JDK ma non capisco come si relazionano tra di loro e il loro utilizzo effettivo. che ruolo ha ognuna?. infine, parli dei "kit" ma non capisco cosa sono, se sono gli starterkit degli esami o altro, come funzionano e specialmente che strumentiintroducono per produrre documentazione, supportare il collaudo e progettare la distribuzione

**Dove trovano risposta in `appunti_01_linguaggi_infrastrutture.md`**: black-box/white-box §3.2 ·
build tools e Maven §4 · UML con immagini §6 · idee funzionali §7 · JVM/JRE/JDK con schema §8.1 ·
«kit» e start kit §8.2 · (domande aperte della correzione: error/compilazione §3.3, bus 33 §5).
