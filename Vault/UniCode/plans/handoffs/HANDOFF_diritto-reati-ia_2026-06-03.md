# Diritto — D11 Autoverifica + Lezione D12 (AI Act)

**Date:** 2026-06-03
**Status:** IN CORSO
**Corso:** Diritto dell'Informatica T
**Capitolo/Modulo:** D11 Reati Informatici (✅ chiuso) + D12 AI Act (🔄 lezione pronta)
**Chain:** `diritto-reati-ia` seq `1`
**Parent:** `none — prima sessione`
**Prior chain:** nessuno — prima sessione

---

## Obiettivo della Sessione

Completare D11 con l'autoverifica delle 5 domande rimasta pendente, portarlo a ✅, e avviare D12 (AI Act) con la lezione strutturata dal PDF. Sessione aperta da `/sessione` in modalità generale, poi focus Diritto. Esame tra 13 giorni — ritmo 1 modulo ogni 6 giorni, margine minimo.

---

## Concetti Assimilati

**D11 — Reati Informatici:**
- Art. 615-ter è reato di **mera condotta**: si perfeziona con l'accesso abusivo, senza richiedere danno né furto di dati
- **Abusività oggettiva**: conta *come* si è entrati, non *perché* — le finalità dell'autore e l'uso successivo dei dati sono irrilevanti per la configurazione del reato base
- **Pentest autorizzato**: il consenso del titolare elimina l'elemento dell'abusività per definizione — stessa condotta, qualificazione giuridica opposta
- **Giurisprudenza oscillante** sull'utente autorizzato: Cass. 8/7/2008 (commette 615-ter se usa il sistema per finalità diverse dal mandato aziendale) vs Cass. 8/10/2008 (non commette 615-ter se l'accesso era regolare e il problema è solo l'uso successivo delle informazioni)
- **Criterio discriminante pratico**: "L'accesso era già di per sé abusivo (raccoglievo dati che non competono alla mia funzione, superavo misure di sicurezza)?" → Sì → 615-ter. "L'accesso era regolare e il problema è ciò che ho fatto dopo?" → No 615-ter (ma altri reati)
- Il caso del cancelliere della Cassazione (Cass. 8/10/2008): consultava dati legittimamente accessibili → no 615-ter; i reati derivano dall'uso delle info ai detenuti (favoreggiamento etc.), non dall'accesso
- **615-quater vs 615-quinquies**: distinzione nello **scopo dello strumento** — quater = strumenti per *entrare* (grimaldelli); quinquies = strumenti per *danneggiare* (malware). Entrambi puniscono le stesse condotte (detenere, produrre, diffondere, ecc.)
- **615-quinquies ≠ danno effettivo**: il danno effettivo è nella famiglia 635 (bis/ter/quater/quinquies); il 615-quinquies punisce la detenzione/diffusione degli strumenti
- **Famiglia 635** — due assi: cosa viene danneggiato (dati/programmi = 635-bis/ter; sistemi = 635-quater/quinquies) × chi subisce il danno (privato vs Stato/pubblica utilità)
- **Frode informatica (640-ter)**: vittima è il **sistema informatico** (manipolato), non una persona indotta in errore come nella truffa (640) — non c'è consenso viziato, non c'è persona ingannata
- **Concorso 615-ter + 640-ter**: Cass. 30/09/2008 conferma che possono concorrere — tutelano beni giuridici diversi (domicilio informatico vs patrimonio). Esempio tipico: accesso abusivo a sistema bancario + manipolazione dati per trasferire fondi
- **Nocumento ≠ danno**: per l'art. 621 (documenti segreti) il nocumento è condizione oggettiva di punibilità — se non si produce nocumento il reato non sussiste neanche in forma tentata

**D12 — AI Act (lezione letta, non ancora appunti grezzi):**
- Reg. UE 2024/1689 — primo quadro giuridico mondiale sull'IA; vigore 1/8/2024, piena applicabilità 2/8/2026
- Tappe: divieti + alfabetizzazione dal 2/2/2025; GPAI dal 2/8/2025; piena applicazione 2/8/2026
- **4 livelli di rischio**: inaccettabile (8 pratiche vietate) → alto rischio (obblighi rigorosi) → limitato (trasparenza) → minimo/nullo (nessuna norma)
- **Definizioni chiave**: sistema di IA (automatizzato, autonomia variabile, adattabilità post-diffusione, deduce output da input); fornitore (sviluppa + immette sul mercato); deployer (usa); rischio (probabilità × gravità danno)
- **8 pratiche vietate**: (1) tecniche subliminali/manipolative, (2) sfruttamento vulnerabilità, (3) social scoring, (4) previsione rischio reato da profilazione, (5) scraping immagini facciali non mirato, (6) inferenza emozioni al lavoro/scuola, (7) categorizzazione biometrica per inferire categorie protette, (8) identificazione biometrica remota real-time in spazi pubblici (salvo 3 eccezioni tassative)
- **Sistemi ad alto rischio**: infrastrutture critiche, istruzione, occupazione (CV screening), credito, biometria retroattiva, attività di contrasto, migrazione, giustizia
- **GPAI**: modelli general-purpose (ChatGPT, Gemini, Claude, LLaMA) — obblighi distinti da quelli dei sistemi ad alto rischio; vigilanza esclusiva Commissione tramite AI Office
- **Sanzioni**: fascia 1 (divieti) 35M€/7%; fascia 2 (alto rischio) 15M€/3%; fascia 3 (false dichiarazioni) 7,5M€/1% — struttura analoga al GDPR, si cumulano
- **Digital Omnibus (accordo 7/5/2026)**: prorogati sistemi alto rischio standalone a 2/12/2027 e embedded a 2/8/2028; invariati divieti, alfabetizzazione, GPAI
- **ALTAI**: Assessment List for Trustworthy AI (luglio 2020) — 7 requisiti: sorveglianza umana, robustezza tecnica, governance dati, trasparenza, non discriminazione, benessere sociale, accountability
- **Casi pratici PDF**: Clearview AI (pratica vietata n.5 + n.8); Amazon CV screening (alto rischio, bias ereditato dai dati); 3 esempi pratiche vietate (manipolazione e-commerce, social scoring e-commerce, riconoscimento emozioni in azienda)

---

## Ancora Poco Chiaro

- Il **test fluido per la giurisprudenza oscillante** su 615-ter (Lorenzo capisce i casi singoli ma applicare il criterio a un caso nuovo richiede ancora attenzione — da rafforzare in ripasso)
- Distinzione **fornitore vs deployer** in casi ambigui dove la stessa azienda svolge entrambi i ruoli — da chiarire con la lettura degli appunti grezzi D12
- Quando esattamente la pratica vietata n.8 (identificazione biometrica remota) si applica alle **3 eccezioni tassative** e quando no — dettaglio che emerge solo dalla lettura attenta

---

## Connessioni con Altro

- D11 e D8 (Privacy/GDPR): il 615-ter tutela il **domicilio informatico**, il GDPR tutela i **dati personali** — un'intrusione può violare entrambi in concorso
- D12 AI Act e D8 GDPR: le sanzioni AI Act si **cumulano** con quelle GDPR (caso Clearview AI: sanzionata sia per GDPR che per pratiche AI vietate); struttura a fasce analoga
- D12 AI Act e D11 Reati Informatici: la pratica vietata n.4 (previsione rischio reato da profilazione) è il confine tra strumento IA lecito e illecito penale — connessione diretta con il divieto di presunte "pre-crime" detection
- D12 e D7 (Proprietà Industriale): i GPAI hanno obblighi sul **diritto d'autore** nei dati di addestramento — rimanda ai concetti di tutela del diritto d'autore in D3

---

## Esercizi (Autoverifica D11)

| Domanda | Stato | Risposta Lorenzo | Note |
|---------|-------|-----------------|------|
| D1 — pentest autorizzato vs non autorizzato | ✓ | Corretta | Ha centrato abusività e consenso del titolare |
| D2 — 615-quater vs 615-quinquies | ~ | Parziale | Errore: distinzione posta come possesso vs uso effettivo invece che scopo dello strumento; mancavano esempi concreti |
| D3 — dipendente con credenziali legittime + giurisprudenza univoca? | ~ | Parziale | Ragionamento sbagliato (citava danno, non finalità); seconda parte (univocità) completamente assente |
| D4 — ospedale pubblico inutilizzabile: quali articoli? | ~ | Parziale | Ha confuso 615-quinquies con danno effettivo; 615-ter corretto; non ha distinto 635-ter (dati) da 635-quinquies (sistemi) |
| D5 — frode informatica vs truffa + concorso 615-ter | ~ | Parziale | Mancava la distinzione vittima persona vs sistema; "concorso a seconda della situazione" troppo vago |

---

## Errori e Misconcezioni

1. **615-quinquies = uso effettivo di malware** — SBAGLIATO. Il 615-quinquies punisce detenzione/diffusione di strumenti per danneggiare, esattamente come il 615-quater punisce la detenzione di strumenti per accedere. La differenza è lo **scopo dello strumento**, non il tipo di condotta (detenere vs usare)
2. **Il danno è elemento del 615-ter** — SBAGLIATO. Il 615-ter è reato di mera condotta; il danno è irrilevante per la configurazione del reato. Questo errore porta a confondere la causa del reato con la sua aggravante o con reati concorrenti
3. **Vittima della frode informatica = persona indotta in errore** — SBAGLIATO. Nella frode informatica (640-ter) la vittima dell'azione è il **sistema informatico** manipolato; non c'è nessuna persona che "cade" nella truffa. La distinzione è la chiave dell'intero art. 640-ter
4. **Giurisprudenza 615-ter univoca** — SBAGLIATO. La Cassazione ha sentenze esplicitamente contraddittorie su utenti autorizzati che agiscono fuori mandato — questa oscillazione è trattata dal PDF come dato di fatto, non come un'eccezione
5. **Qualificazione reato nel danno a ente pubblico**: ha identificato 615-quinquies invece di 635-ter (dati) + 635-quinquies (sistemi) — confusione sistematica tra la serie 615 (accesso/strumenti) e la serie 635 (danneggiamento effettivo)

---

## Materiali Usati

### PDF sorgente
- `SLIDE TEORIA/DIRITTO INFORMATICO/11_DirInfo_2026_ReatiInformatici_DEF.pdf` — D11, usato per autoverifica
- `SLIDE TEORIA/DIRITTO INFORMATICO/12_DirInfo_2026_AI_Act_DEF.pdf` — D12, 46 pagine lette integralmente (pp. 1-20, 21-40, 41-46)

### File prodotti questa sessione
- `claudeLezioni/LEZIONI DIRITTO/lezione_moduloD12_ai_act.md` — lezione D12 completa (12 sezioni, 5 casi pratici, 5 domande autoverifica)
- `stato/corrente.md` — D11 → ✅, D12 → 🔄, Diritto 85% (11/13), sessione 30, aggiornato 2026-06-03
- `stato/tracker_ripasso.md` — aggiunto D11: completato 2026-06-03, prossimo ripasso 2026-06-06
- `stato/errori_frequenti.md` — aggiunte 3 righe D11: 615-quinquies vs danno effettivo, mera condotta, vittima frode informatica

### Appunti esistenti D11
- `claudeAppunti/APPUNTI DIRITTO/appunti_moduloD11_reati_informatici.md` — già completi, usati come riferimento per autoverifica

---

## Preferenze e Feedback di Sessione

- Lorenzo risponde alle domande di autoverifica una alla volta (non le ha bufferizzate tutte insieme) — il ritmo domanda/risposta/feedback funziona bene
- Ha posto una domanda di chiarimento autonoma mid-verifica ("quindi per il caso coi detenuti il problema è stato passarle ai detenuti?") — segnale di ragionamento attivo, non passivo
- Quando le domande contengono una seconda parte esplicita ("la risposta è univoca?"), tende a rispondere solo alla prima parte — da segnalare attivamente nelle prossime autoverifica
- Non chiede "posso passare al prossimo modulo?" — decide autonomamente; seguire il suo ritmo senza checkpoint non richiesti

---

## Dove Stiamo Andando

1. **D12** — leggere `claudeLezioni/LEZIONI DIRITTO/lezione_moduloD12_ai_act.md` → scrivere appunti grezzi → `/appunti D12` → autoverifica 5 domande → D12 ✅
2. **D13** — `/lezione D13` (PDF: `13_DirInfo_2026_DSA_DMA_DataAct.pdf`) → grezzi → `/appunti D13` → D13 ✅
3. **Ripasso Diritto** — D8/D9/D10 ripasso scaduto (D8 da 29/05, D9 da 31/05, D10 da 1/06); D1-D7 mai ripassati. Prima dell'esame (16/06) inserire almeno `/simula diritto` cross-modulo
4. **SysAdmin 3D** — VM Vagrant, eseguire Es. 2-6 (ping, ss -tlnp, /etc/hosts, dig, tcpdump) → `/appunti 3D`
5. **Security S1** — VM Kali, eseguire 6 sezioni LAB Enumerazione → `/appunti S1`

---

## Rischi e Blocchi

- 🚨 **Diritto urgente**: 13 giorni all'esame (16/06), ancora D12 (🔄 lezione pronta ma no grezzi) + D13 (⬜ tutto da fare). Ritmo necessario: ~1 modulo ogni 6 giorni — margine minimo senza margine per imprevisti
- 🔴 **Ripasso Diritto scaduto**: D8 (-5 gg), D9 (-3 gg), D10 (-2 gg) — tutti mai ripassati. D1-D7 mai ripassati. L'esame è a scelta multipla (22 quiz): il ripasso cross-modulo è critico
- 🔴 **Security a 0%**: S1 LAB non eseguito, S2-S12 tutti ⬜ — l'esame è il 17/07 ma il backlog è enorme (~111h stimate)
- 📋 **Dipendenza**: per `/appunti D12` serve che Lorenzo abbia prima scritto gli appunti grezzi — non saltare questo step

---

## Dettaglio Autoverifica D11 — Feedback Completo

Riportato per completezza, utile per `/ripassa D11` futuro.

**D1 (pentest)** → ✅ corretta. Punto aggiunto: il pentest autorizzato non è "un'eccezione" — manca strutturalmente l'elemento dell'abusività. Non è "ammesso nonostante sia uguale" — è giuridicamente diverso.

**D2 (quater vs quinquies)** → errore principale: Lorenzo ha detto che quater = possesso, quinquies = uso effettivo. Corretto: ENTRAMBI puniscono possesso/produzione/diffusione. La differenza è nello **scopo**: quater → entrare; quinquies → fare danno. Mancavano anche esempi concreti richiesti dalla domanda.

**D3 (dipendente credenziali legittime)** → due errori: (a) ragionamento basato su "dati a cui non avrebbe accesso" e "causa danno" — il criterio reale è "finalità diverse da quelle consentite" (Cass. 8/7/2008); (b) seconda parte "giurisprudenza univoca?" non risposta — risposta corretta: NO, oscillante. Cass. 8/7/2008 vs Cass. 8/10/2008.

**D4 (ospedale pubblico)** → errore sistematico 615 vs 635: Lorenzo ha citato 615-quinquies per il danno effettivo. Risposta corretta: 615-ter (accesso) + 635-ter (dati/programmi ente pubblico danneggiati) + 635-quinquies (sistemi di pubblica utilità resi inservibili) — aggravante 635-quinquies per sistema inservibile 3 giorni.

**D5 (frode informatica vs truffa)** → errore: ha definito la differenza come "avviene tramite strumento informatico" invece di "vittima è il sistema (non la persona); no induzione in errore". Sul concorso ha risposto "a seconda della situazione" — corretto è: sì, possono concorrere sempre (Cass. 30/09/2008), beni giuridici distinti.

---

## Stato Completo File Modificati Questa Sessione

| File | Modifica |
|------|----------|
| `stato/corrente.md` | Sessione 29→30; aggiornato 2026-05-29→2026-06-03; D11 🔄→✅; D12 ⬜→🔄; Diritto 77%→85% (10→11/13); urgenza Diritto ricalcolata (4 step→2 moduli in 13 gg) |
| `stato/tracker_ripasso.md` | Aggiunta riga D11: completato 2026-06-03, mai ripassato, prossimo 2026-06-06, 🟢 |
| `stato/errori_frequenti.md` | Aggiunte 3 righe D11: (1) 615-quinquies confuso con danno effettivo; (2) citare danno come elemento 615-ter; (3) vittima frode informatica come persona |
| `claudeLezioni/LEZIONI DIRITTO/lezione_moduloD12_ai_act.md` | File nuovo — lezione D12 AI Act completa da PDF 46pp |

---

## Contenuto Chiave Lezione D12 (per riferimento rapido)

La lezione D12 copre nell'ordine:

1. Quadro normativo: Reg. UE 2024/1689 — 4 tappe di applicazione (2/2/2025, 2/8/2025, 2/8/2026, proroghe Digital Omnibus)
2. Ratio legis: IA antropocentrica affidabile — protezione diritti fondamentali + promozione innovazione
3. Oggetto: 7 cose che la legge stabilisce (lett. a-g)
4. Esclusioni: militare/difesa/sicurezza nazionale; ricerca scientifica; uso personale non professionale
5. Definizioni: sistema di IA (3 tratti costitutivi), rischio, fornitore, deployer, incidente grave
6. Alfabetizzazione: obbligo fornitore + deployer dal 2/2/2025
7. **4 livelli di rischio** (piramide): inaccettabile → alto → limitato → minimo/nullo
8. **8 pratiche vietate** — testo integrale di ciascuna dal PDF
9. **Sistemi ad alto rischio**: 9 categorie elencate + 7 obblighi pre-mercato
10. Rischio limitato: obblighi di trasparenza (chatbot, IA generativa, deepfake)
11. Rischio minimo: nessuna norma (videogiochi, filtri antispam)
12. **GPAI**: definizione, obblighi fornitori (dal 2/8/2025), modelli a rischio sistemico, Codice GPAI, AI Office
13. **Sanzioni**: 3 fasce (35M€/7%, 15M€/3%, 7,5M€/1%) + sanzioni non pecuniarie + PMI
14. **Digital Omnibus 2026**: cosa cambia (scadenze alto rischio, watermarking, nuovo divieto deepfake intimi) e cosa resta (divieti, alfabetizzazione, GPAI)
15. Orientamenti etici (2019) + ALTAI (2020): 3 componenti IA affidabile, 4 principi etici, 7 requisiti
16. **5 casi pratici**: Clearview AI, Amazon CV screening, manipolazione e-commerce, social scoring, riconoscimento emozioni in azienda

**Domande di autoverifica D12** (le 5 nella lezione):
1. Cos'è l'AI Act e qual è il suo oggetto? In quali casi non si applica?
2. 4 livelli di rischio con esempio concreto e regime per ciascuno
3. Almeno 4 delle 8 pratiche vietate + criterio comune che le accomuna; distinguerle dai sistemi ad alto rischio
4. GPAI: definizione + obblighi fornitori vs alto rischio
5. Sistema sanzionatorio: 3 fasce, rapporto con GDPR, cosa ha cambiato il Digital Omnibus

**Pattern di errore preventivo per D12** (da errori_frequenti.md rilevanti):
- Tendenza a semplificare distinzioni → in D12 non fondere: fornitore vs deployer; pratiche vietate vs alto rischio vs limitato; GPAI vs sistema di IA
- Definizioni parafrasate invece di fedeli al PDF → le definizioni di "sistema di IA", "fornitore", "deployer" vanno riprodotte fedelmente

---

## Quick Start Prossima Sessione

```
# Ripristina contesto
Leggi: plans/handoffs/HANDOFF_diritto-reati-ia_2026-06-03.md

# Stato al riavvio
- D11 ✅ chiuso (autoverifica completata, errori documentati in errori_frequenti.md)
- D12 🔄 lezione pronta, grezzi e appunti da fare
- Prossima azione: leggere lezione D12 + scrivere appunti grezzi

# Materiali da aprire
claudeLezioni/LEZIONI DIRITTO/lezione_moduloD12_ai_act.md  (lezione D12 completa)
SLIDE TEORIA/DIRITTO INFORMATICO/12_DirInfo_2026_AI_Act_DEF.pdf  (se vuoi rivedere il PDF)

# Prima azione
Apri la lezione D12 e leggila. Scrivi appunti grezzi in APPUNTI GREZZI/Diritto/
(o direttamente in chat). Poi: /appunti D12

# Verifica prerequisito D12
Sai rispondere: "Qual è la differenza tra fornitore e deployer nell'AI Act? 
Cosa succede se la stessa azienda sviluppa e usa il proprio sistema?"
→ Se no: rileggere §2 della lezione D12 prima di procedere agli appunti grezzi

# Segnale di rischio da monitorare
Esame Diritto tra 13 giorni (16/06). D12 + D13 devono essere ✅ entro ~12/06.
Dopo D13: almeno una sessione /simula diritto cross-modulo prima dell'esame.
```

---

## Session Closed
**Closed at:** 2026-06-03
**Commit:** 183190c
**Session status:** Handed off to next session
