# Speed Review — D13: Pacchetto Digitale Europeo (DSA, DMA, Data Act)

> Tre regolamenti, tre domande distinte. Il quiz colpisce su: VLOP vs gatekeeper, anti-steering (soggetto!), sanzioni a percentuali diverse, safe harbour, Data Act (titolare ≠ utente).

---

## 1. Quadro d'insieme

| Regolamento | Domanda | Chi regola | Sanzione max |
|-------------|---------|------------|--------------|
| **DSA** | Cosa può stare online? | Intermediari online | **6%** fatturato |
| **DMA** | Come si compete? | Gatekeeper (grandi piattaforme) | **10%** (20% recidiva) |
| **Data Act** | Chi controlla i dati IoT? | Produttori IoT + cloud | Sanzioni nazionali |

> Tutti e tre: applicazione **extraterritoriale**, coordinamento con GDPR (in conflitto **prevale il GDPR**), Commissione UE con poteri di vigilanza.

---

## 2. DSA (Digital Services Act)

- Principio: **«ciò che è illegale offline è illegale online»**.
- **Vigilanza**: **DSC nazionale** (in Italia **AGCOM**) su tutti gli intermediari; **Commissione UE** esclusiva su **VLOP/VLOSE**.

### I 6 livelli (obblighi crescenti)
Mere conduit → Caching → Hosting → Piattaforme online → **VLOP** (≥45 mln utenti UE) → **VLOSE** (≥45 mln, motori di ricerca).

### Safe harbour (esenzione responsabilità)
- **Mere conduit** (art. 4), **Caching** (art. 5), **Hosting** (art. 6, rimuove appena a conoscenza).
- **Buon samaritano** (art. 7): le indagini volontarie **in buona fede** NON fanno perdere l'esenzione.
- **No obbligo generale di sorveglianza** (art. 8).
- **Divieto dark pattern** (art. 25); pubblicità profilata **vietata ai minori** e su categorie speciali; **sistemi di raccomandazione** (art. 27): almeno un'opzione **non basata su profilazione**.
- **VLOP/VLOSE**: valutazione rischi sistemici, **audit indipendenti**, accesso dati ai ricercatori, repository annunci.

---

## 3. DMA (Digital Markets Act)

- Logica **ex ante** (preventiva), diversa dall'antitrust tradizionale (ex post).
- **Gatekeeper** (art. 3, **3 criteri cumulativi**): (1) impatto significativo (≥7,5 mld € fatturato UE o ≥75 mld cap.), (2) ruolo di gateway (≥45 mln utenti + ≥10.000 utenti commerciali), (3) posizione consolidata.

### ⚠️ VLOP (DSA) vs Gatekeeper (DMA)
| | VLOP (DSA) | Gatekeeper (DMA) |
|--|-----------|------------------|
| Criterio | **uno solo**: ≥45 mln utenti | **tre cumulativi** |
| Fatturato | irrilevante | ≥7,5 mld € o cap. ≥75 mld |
> Piattaforma con 50 mln utenti ma piccolo fatturato → VLOP, NON gatekeeper.

### Obblighi (do's) e divieti (don'ts)
- **Do's**: interoperabilità (messaggistica), **portabilità dati**, accesso alle stesse API, trasparenza ranking.
- **Don'ts**:
  - **Self-preferencing** (favorire i propri servizi, es. Google Shopping).
  - **Anti-steering**: vietato impedire agli **utenti commerciali** (sviluppatori) di informare i **propri clienti** di offerte migliori fuori dalla piattaforma (caso Spotify/Apple).
  - **Bundling forzato**, **tracciamento senza consenso**, esclusiva pagamenti, **lock-in** (impedire disinstallazione).
- Sanzione: **10%** fatturato (20% recidiva).

---

## 4. Data Act

- I dati generati dall'uso di un **prodotto connesso** (IoT) sono accessibili all'**utente**, non solo al produttore.
- **Titolare dei dati** (data holder) = chi detiene/mette a disposizione i dati (il **produttore**). **Utente** = chi possiede/usa il prodotto (**beneficiario** dei diritti, NON "titolare").
- **Diritto di accesso**: gratuito, sicuro, in tempo reale, formato **machine-readable** (JSON/CSV/XML).
- **Condivisione con terzi** designati dall'utente, a condizioni **FRAND**.
- **Switching cloud**: eliminare il **vendor lock-in**; switching fees **gratuite dal 12 set 2027**.
- **Trasferimento dati non personali**: il cloud deve resistere a ordini di autorità di paesi terzi (per i personali → GDPR).
- **Rapporto con GDPR**: in conflitto **prevale il GDPR** (art. 1 §5).

---

## ⚠️ Trappole MC

- **VLOP** (DSA, un criterio: 45 mln utenti) ≠ **Gatekeeper** (DMA, 3 criteri cumulativi + fatturato). Errore classico.
- **Anti-steering**: il soggetto protetto è l'**utente commerciale/sviluppatore** (es. Spotify), che vuole informare i **propri clienti** — NON l'utente finale generico. Il quiz inverte il soggetto.
- Sanzioni: **DSA 6%**, **DMA 10%/20%**, Data Act = nazionali. Il quiz scambia le percentuali.
- **Buon samaritano**: le indagini volontarie in buona fede NON fanno perdere il safe harbour.
- **No obbligo generale di sorveglianza** (vale per tutti gli intermediari).
- Data Act: **titolare dei dati = produttore** (data holder), NON l'utente. L'utente è beneficiario dell'accesso.
- In conflitto con GDPR, **prevale il GDPR** (per tutti e tre).
- Self-preferencing ≠ anti-steering: il primo è favorire i propri servizi, il secondo è bloccare l'indirizzamento fuori piattaforma.
- DMA = ex ante; antitrust tradizionale = ex post.

---

## Da aggiungere dopo le simulazioni:

<br><br><br>
