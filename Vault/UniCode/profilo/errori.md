# Errori ricorrenti

> Strato **permanente**, append-oriented. Aggiornato da `/appunti`, `/ripassa`, `/simula`
> nella stessa esecuzione in cui l'errore emerge.
>
> La sezione **trasversale** è quella che conta: sono modi di ragionare, non errori di
> materia, e si ripresenteranno identici su corsi che Lorenzo non ha ancora aperto.
> Il briefing d'avvio carica questa sezione per prima.

## Trasversale — vale su ogni corso

### 1. Semplificare distinzioni che vanno tenute separate
Tendenza accertata a collassare due concetti vicini in uno. Emerso ripetutamente in
Diritto, ma è un pattern cognitivo, non una lacuna giuridica.

**Dove si ripresenterà**: stabilità asintotica vs. semplice (`CA`); banda vs. banda
passante (`TLC`); processo vs. thread, concorrenza vs. parallelismo (`SO`); tensione di
soglia vs. tensione di saturazione (`ELN`); latenza vs. RTT (`RETI`).

**Contromisura**: davanti a due termini vicini, chiedersi *cosa distingue esattamente il
primo dal secondo, e quale caso limite li separa*. Se non emerge un caso limite, la
distinzione non è stata capita.

### 2. Fermarsi al primo indizio
Considera risolto un esercizio al primo risultato plausibile, senza verificare che spieghi
**tutti** i dati del problema. Emerso su analisi di traffico in Sicurezza.

**Contromisura**: far quadrare i numeri prima di concludere. Un esercizio è chiuso quando
ogni dato dell'enunciato è stato usato o esplicitamente scartato con motivazione.

### 3. Autenticazione vs. autorizzazione
Distinzione teoricamente posseduta che scivola in pratica.
**Contromisura**: per ogni meccanismo chiedersi — *stabilisce chi sei, o cosa puoi fare?*

### 4. Parafrasi al posto della formulazione esatta
Dove la fonte usa una formulazione precisa, riformularla la degrada.
**Contromisura**: `[fonte: <fonte>]` sulle affermazioni riprese alla lettera.

---

## Per corso

### `LAS` — Amministrazione di Sistemi (bash/Linux)
- Spazi obbligatori nelle condizioni: `[ ! -d "$x" ]`, non `[ !-d "$x" ]`.
- Loop incompleti: manca `done`.
- Shebang assente o incompleto.
- Confusione fra contare *righe* (`grep -c`) e contare *occorrenze* (`grep -o | wc -l`).
- **Contromisura**: testare con casi limite prima di fidarsi della logica.

### Archivio — corsi chiusi
> Conservati perché i pattern sopravvivono al corso che li ha generati.

<details>
<summary>Diritto dell'Informatica — superato 16/06/2026</summary>

| Concetto | Errore | Correzione |
|---|---|---|
| Regolamenti UE | detti "non direttamente applicabili" | sono **direttamente applicabili** per definizione |
| Direttive UE | dette "ideali" | vincolanti quanto al risultato |
| Diritto d'autore | 70 anni = diritti morali | 70 anni = diritti **patrimoniali**; i morali sono imprescrittibili |
| Creative Commons | CC BY = pubblico dominio | CC BY ≠ pubblico dominio; **CC0** = rinuncia totale |
| Dati sensibili | capacità di identificare la persona | **natura dell'informazione** |
| Reati informatici | parafrasati anziché nominati | 615-ter = mera condotta, il danno non è richiesto |
| AI Act | lett. e) uguale a lett. a) | a) regole generali IA; e) regole specifiche modelli GPAI |

</details>

<details>
<summary>Laboratorio di Sicurezza Informatica — superato 17/07/2026</summary>

- `nmap`: porte con virgole `-p 22,80,3306`; `-sV` per version detection; `-p-` per porte
  non standard; `sudo` per ARP affidabile.
- `psql`: meta-comandi e SQL su righe separate; `\r` resetta il buffer.
- `scp` dal terminale locale, non da una sessione SSH attiva.
- Suricata: verificare sempre il traffico legittimo prima di scrivere regole; variabili
  custom senza `#` iniziale; nel JSON il campo è `signature_id`, non `sid`; `cat -A` per
  verificare i file scritti a mano.

</details>
