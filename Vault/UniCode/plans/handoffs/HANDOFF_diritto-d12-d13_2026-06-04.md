# D12 Autoverifica completata · D13 Lezione + Appunti Grezzi pronti

**Date:** 2026-06-04
**Status:** IN CORSO
**Corso:** Diritto dell'Informatica T
**Moduli:** D12 (AI Act) → autoverifica ✅ · D13 (DSA/DMA/Data Act) → lezione ✅ + appunti grezzi ✅
**Chain:** `diritto-d12-d13` seq `1`
**Parent:** none — prima sessione in questa chain
**Prior chain:** `HANDOFF_diritto-reati-ia_2026-06-03.md` (D11 sessione precedente — catena diversa)

---

## Obiettivo della Sessione

Chiudere D12 con l'autoverifica 5 domande (rimaste in sospeso come condizione per ✅), poi avviare D13 con lezione da PDF e appunti grezzi. Contesto urgente: esame Diritto il 16/06, 12 giorni rimasti, 2 moduli ancora da completare.

---

## Concetti Assimilati

- **D12 — AI Act**: struttura a 4 livelli di rischio (inaccettabile → alto → limitato → minimo) compresa nelle linee generali; criterio comune alle pratiche vietate = "ledono diritti fondamentali non negoziabili"; distinzione vietati/alto rischio = divieto assoluto vs ammesso con obblighi
- **D12 — Logica ex ante**: pratiche vietate = il rischio strutturale è così grave che nessun beneficio economico può giustificarle
- **D12 — GPAI vs sistema AI**: GPAI = modello base (GPT-4); sistema AI = applicazione che incorpora il modello; obblighi diversi per ciascuno
- **D12 — Vigilanza GPAI**: AI Office (Commissione europea) ha competenza esclusiva sui fornitori GPAI; autorità nazionali per sistemi ad alto rischio
- **DSA — Principio cardine**: «ciò che è illegale offline è illegale online»
- **DSA — 6 livelli di intermediari**: mere conduit → caching → hosting → piattaforme → VLOP → VLOSE (progressione di obblighi)
- **DSA — Safe harbour**: esenzione responsabilità mantenuta dalla Direttiva e-commerce; condizioni diverse per mere conduit/caching/hosting; principio buon samaritano (indagini volontarie non fanno perdere l'esenzione); nessun obbligo generale di sorveglianza
- **DSA — Dark pattern vietati**: confirm shaming, pulsanti nascosti, urgenza fittizia, preimpostazioni a favore del fornitore
- **DSA vs DMA — distinzione VLOP/gatekeeper**: VLOP = ≥ 45 mln utenti UE (criterio unico, DSA); gatekeeper = 3 criteri cumulativi (fatturato ≥ 7.5 mld € O capitalizzazione ≥ 75 mld €, ruolo gateway ≥ 45 mln utenti + 10K commerciali, posizione consolidata — DMA); stessa piattaforma può essere entrambi ma per ragioni diverse
- **DMA — Logica ex ante**: interviene prima del danno, senza dover dimostrare posizione dominante (diverso dall'antitrust tradizionale che è ex post)
- **DMA — Gatekeeper "do's"**: portabilità dati, interoperabilità (messaggistica), accesso dati performance, notifica acquisizioni, trasparenza ranking, accesso API app store
- **DMA — Gatekeeper "don'ts"**: self-preferencing, anti-steering, bundling forzato, tracciamento senza consenso, blocco pagamenti terzi, lock-in
- **DMA — Casi pratici**: Apple indagata per anti-steering App Store + browser choice screen; Google Shopping 2017 come precedente che ha ispirato DMA
- **Data Act — Principio**: i dati generati dall'uso di un prodotto connesso sono accessibili all'utente (non solo al produttore)
- **Data Act — Prodotto connesso**: oggetto che raccoglie e trasmette dati (auto, smartwatch, macchinario industriale)
- **Data Act — Diritti utente**: accesso gratuito, in tempo reale, machine-readable; condivisione con terzi a condizioni FRAND
- **Data Act — Titolare dati ≠ utente**: il titolare (es. produttore) ha il diritto/obbligo di mettere a disposizione i dati; l'utente ha il diritto di accedervi — distinzione chiave (Lorenzo l'aveva confusa)
- **Data Act — Cloud switching**: eliminare vendor lock-in; switching fees: ridotte da set. 2025, gratuite dal 12 set. 2027
- **Quadro d'insieme**: DSA = "cosa può stare online"; DMA = "come si compete nei mercati digitali"; Data Act = "chi controlla i dati generati dai dispositivi" — affiancati, non sovrapposti

---

## Ancora Poco Chiaro

- **D12 — Pratiche vietate**: Lorenzo ha nominato solo 2/8 (riconoscimento facciale in tempo reale + social scoring). Mancano: tecniche subliminali/manipolative, sfruttamento vulnerabilità (età/disabilità), previsione rischio reato da profilazione, scraping immagini facciali, inferenza emozioni lavoro/scuola, categorizzazione biometrica per categorie protette. Va ripassato come elenco prima dell'esame.
- **D12 — Obblighi GPAI**: quasi assenti nella risposta (solo governance ricordata). Da fissare: documentazione tecnica, diritto d'autore nei dati + sintesi pubblica dei contenuti formativi; per frontier models: sicurezza + valutazione avversariale + segnalazione incidenti.
- **D12 — Fasce sanzionatorie**: numeri non ricordati (35M€/7%, 15M€/3%, 7.5M€/1%). Va memorizzato l'ordine decrescente e il collegamento pratica vietata → fascia 1.
- **D13 — Domande aperte negli appunti grezzi** (molte, elencate sotto in "Esercizi")
- **DSA — Mere conduit / caching**: definizioni operative non consolidate ("so solo gli esempi")
- **DMA — Interoperabilità pratica**: "cosa significa che WhatsApp deve essere interoperabile?" — domanda aperta non ancora risolta
- **DMA — Anti-steering pratica**: "cosa implica nel pratico?" — domanda aperta
- **Data Act — B2B condivisione**: "non riesco a immaginare un commercio di dati B2B" — concetto astratto, serve esempio

---

## Connessioni con Altro

- **DSA dark pattern ↔ D12 AI Act pratica 1** (tecniche manipolative): DSA vieta dark pattern nell'interfaccia indipendentemente dall'IA; AI Act vieta tecniche subliminali/manipolative realizzate tramite sistemi AI — due regimi distinti che si sovrappongono parzialmente
- **DMA tracciamento senza consenso ↔ D8 GDPR**: il divieto DMA di combinare dati da più CPS senza consenso rispecchia il principio di consenso del GDPR; in caso di conflitto prevale GDPR
- **Data Act ↔ D8 GDPR**: Data Act copre dati non personali o misti; GDPR prevale sempre per i dati personali (art. 1 §5 Data Act)
- **DMA gatekeeper + AI Act GPAI**: Alphabet/Meta/Apple sono sia gatekeeper (DMA) che potenziali fornitori GPAI (AI Act) — due regimi normativi che si sovrappongono sulla stessa entità
- **DSA VLOP ↔ D4 hosting provider**: il DSA evolve dalla Direttiva e-commerce (2000/31/CE) che Lorenzo ha studiato in D4 — il safe harbour è lo stesso principio, aggiornato

---

## Esercizi / Domande Aperte D13

Le seguenti domande erano inline negli appunti grezzi di Lorenzo (`APPUNTI GREZZI/Diritto/Appunti_ModuloD13.md`) e devono ricevere risposta in `/appunti D13`:

| Punto | Domanda | Sezione |
|-------|---------|---------|
| VLOP/VLOSE/DSC | "spiegami le classificazioni che usi: VLOP, VLOSE, DSC, AGCOM" | DSA ambito |
| Intermediari vs piattaforme | "differenze tra intermediari di prima e piattaforme online?" | DSA obblighi |
| Buon samaritano | "spiegami meglio il principio del buon samaritano, come funziona, in che modo si rischierebbe di perdere l'esenzione e perché non succede" | DSA safe harbour |
| Hosting | "tipo azure, AWS etc?" (obblighi aggiuntivi hosting) | DSA hosting |
| Sistemi raccomandazione | "ma tipo correlati di youtube o raccomandazioni di adv?" | DSA piattaforme |
| Audit indipendenti | "cosa sono?" | DSA VLOP |
| Misure adeguate minori | "(tipo?)" — cosa significa "misure adeguate" senza verifica età | DSA minori |
| Interoperabilità | "ma in cosa è interoperabile WhatsApp?" | DMA do's |
| Portabilità | "tipo passaggio apple android dei dati" — capisce l'idea ma vuole conferma | DMA do's |
| Notifica acquisizioni | "ma che commissione?" — vuole sapere che è la Commissione europea | DMA do's |
| Accesso API app store | "in parole povere?" | DMA do's |
| Anti-steering pratico | "cosa implica nel pratico?" | DMA don'ts |
| Tracciamento senza consenso | "in parole povere?" | DMA don'ts |
| Piattaforme pagamento | "tipo?" — esempio concreto | DMA don'ts |
| Lock-in | "esempio?" | DMA don'ts |
| Designazione | "quindi queste sono le condizioni per essere designati gatekeeper?" — confusione: la sezione "Designazione e procedura" descrive la procedura, non le condizioni (quelle sono i 3 criteri cumulativi) | DMA procedura |
| Data Act obiettivo | "definizione strana, in che senso mercato dei dati, in che senso prodotti connessi, a chi si rivolge?" | Data Act intro |
| Titolari dati | "non mi è chiaro, avrei detto che l'utente è titolare dei suoi dati" | Data Act definizioni |
| Machine-readable | "ad esempio la memoria di un LLM sempre leggibile e modificabile?" | Data Act accesso |
| Condivisione terzi | "voglio un esempio pratico di questa situazione" | Data Act terzi |
| B2B condivisione | "non riesco a immaginarmi un commercio di dati B2B" | Data Act B2B |
| Responsabilità clausole | "non ho capito verso chi" | Data Act PMI |
| Soggetti pubblici | "chi?" (la Commissione) | Data Act pubblici |
| Cloud switching | "fornisci esempi tangibili per questi obblighi" | Data Act cloud |
| Dati non personali | "come mai non personali? e per i dati personali? e poi lo proteggono dalle autorità? non sono i 'buoni'?" | Data Act cap. VII |

---

## Errori e Misconcezioni

- **D12 — Terminologia livelli di rischio**: Lorenzo ha usato "intermedio" invece di "rischio limitato" — termine che il PDF non usa; da correggere attivamente in sede di ripasso
- **D12 — Confusione pratiche 5 e 8**: pratica 5 = scraping non mirato di immagini facciali per creare database; pratica 8 = uso in tempo reale dell'identificazione biometrica in spazi pubblici. Sono due vietati distinti, Lorenzo le aveva mescolate nella stessa descrizione
- **D12 — "Privati" come esclusione AI Act**: Lorenzo ha detto "non si applica ai privati" — impreciso. La formulazione esatta è "persone fisiche che utilizzano IA nel corso di un'attività non professionale puramente personale"; un privato che usa IA per lavoro in proprio è incluso
- **D12 — Oggetto AI Act ridotto a "sicurezza e fiducia"**: mancavano le altre due gambe (protezione salute/sicurezza/diritti fondamentali + promuovere innovazione)
- **D13 — Titolare dati confuso con utente**: Lorenzo avrebbe spontaneamente detto "l'utente è titolare dei suoi dati". Nel Data Act: titolare = chi ha il diritto/obbligo di mettere a disposizione (es. produttore); utente = chi accede. L'utente ha il diritto di accesso, non la titolarità nel senso tecnico del Data Act.

---

## Materiali Usati

### File creati questa sessione
- `claudeLezioni/LEZIONI DIRITTO/lezione_moduloD13_pacchetto_digitale.md` — lezione completa DSA + DMA + Data Act
- `APPUNTI GREZZI/Diritto/Appunti_ModuloD13.md` — appunti grezzi di Lorenzo (già scritti, con ~25 domande aperte inline)

### Modificati
- `stato/corrente.md` — D12 → ✅, D13 → 🔄
- `stato/tracker_ripasso.md` — aggiunto D12 completato 2026-06-04, prossimo ripasso 2026-06-07

### PDF letti
- `SLIDE TEORIA/DIRITTO INFORMATICO/13_DirInfo_2026_DSA_DMA_DataAct.pdf` (37 pagine)
- `Schemi utili per ripasso-20260521 (1)/13_PacchettoDigitaleEuropeo.pdf` (schema ripasso)
- `claudeAppunti/APPUNTI DIRITTO/appunti_moduloD12_ai_act.md` (per il feedback autoverifica)

---

## Preferenze e Feedback di Sessione

- Lorenzo preferisce l'autoverifica domanda per domanda, non in blocco — risponde poi aspetta feedback, poi prossima
- Feedback apprezzato con struttura: "cosa hai detto bene / da precisare" — tono diretto senza eccessiva indulgenza
- Quando finisce un modulo, dice esplicitamente "passiamo al prossimo" — non chiedere conferma

---

## Dove Stiamo Andando

1. **`/appunti D13`** — elaborare `APPUNTI GREZZI/Diritto/Appunti_ModuloD13.md` in appunti definitivi, rispondendo a tutte le ~25 domande aperte inline (vedi tabella sopra)
2. **Autoverifica D13** — 5 domande dopo `/appunti D13`, come fatto per D12
3. **Ripassone Diritto** — Lorenzo ha detto "una volta finiti i PDF, partiamo con il ripassone"; focus su: D9 (gerarchia firme, opponibilità PEC), D10 (gerarchia 70/2003 vs Codice consumo), D11 (615-quinquies vs 635-xx, mera condotta), D12 (pratiche vietate 8, obblighi GPAI, fasce sanzionatorie), D13 (tbd dopo appunti)
4. **SysAdmin 3D** + **Security S1 LAB** — rimandati dopo completamento Diritto; urgenza più bassa

---

## Rischi e Blocchi

- **Rischio principale**: 12 giorni a Diritto, D13 non ancora ✅. Serve `/appunti D13` nella prossima sessione come prima azione.
- **Lacune D12 pre-esame**: pratiche vietate (8 complete), obblighi GPAI, fasce sanzionatorie — da coprire nel ripassone, non rimandare oltre
- **Ripasso D8/D9/D10 scaduto**: D8 (scad. 29/05), D9 (scad. 31/05), D10 (scad. 01/06) già oltre la scadenza nel tracker; D11 scade 06/06 (dopodomani)

---

## Quick Start Prossima Sessione

```
# Ripristina contesto
Leggi: plans/handoffs/HANDOFF_diritto-d12-d13_2026-06-04.md
Poi: stato/corrente.md (già aggiornato)

# File da aprire
APPUNTI GREZZI/Diritto/Appunti_ModuloD13.md  ← appunti grezzi già scritti, ~25 domande aperte
claudeLezioni/LEZIONI DIRITTO/lezione_moduloD13_pacchetto_digitale.md  ← lezione di riferimento

# Prima azione
/appunti D13
(Non servono PDF — lezione già letta e appunti grezzi già scritti)

# Verifica comprensione prima di andare avanti
Dopo /appunti D13: rispondere a questa domanda senza guardare:
"Qual è la differenza tra VLOP (DSA) e gatekeeper (DMA)?
 Una stessa piattaforma può essere entrambi? Fai un esempio."
Se ok → autoverifica D13 → ripassone
```

---

## Session Closed
**Closed at:** 2026-06-04 ~15:15
**Commit:** 42611fa (auto-commit sessione)
**Session status:** Handed off to next session
