# Procedura Operativa — Web Vulnerabilities

> Algoritmo esteso passo-passo per qualunque esercizio di questa famiglia (una web app in container
> docker da testare con browser/curl, obiettivo tipico: `alert()` o esfiltrare una flag). Non contiene
> teoria di base su HTTP/HTML — solo l'algoritmo operativo e i bivi. Per il triage rapido e i rami per
> famiglia vedi `guida_esame_web.md`; per i 5 casi reali già risolti,
> `modello_web_vulnerabilities.md`; per il template del `web.txt`, `template_report_web.md`.

> ⚠️ **Regola d'oro: i deliverable sono screenshot + `web.txt`, e il *livello di dettaglio della
> descrizione È il voto.** Non basta "far partire l'exploit": va documentato il **ragionamento**
> (come hai classificato la vuln, quali ostacoli hai incontrato, come li hai aggirati). Scrivi il
> `web.txt` *mentre* procedi, non alla fine a memoria.

---

## 0. Prima di toccare l'app (setup + lettura)

- [ ] **Avvia il container** come indicato nella predisposizione (`zcat X.tar.gz | sudo docker load`
      poi `sudo docker run --rm -p PORTA:PORTA nome`; oppure `gpg -d union.sh.gpg > union.sh`,
      `chmod +x`, `./union.sh`). Nota la **porta** (5000, 8000...) e l'**indirizzo** (`127.0.0.1` o
      l'IP del container da `ip a`).
- [ ] **Gate scanner/bruteforce**: NON usare sqlmap/nikto/dirb/gobuster/hydra. Vietato su tutto il
      tipo d'esame. Solo browser, DevTools (inspector), curl, e Burp/proxy per comporre richieste a mano.
- [ ] **LEGGI tutta la pagina prima di iniettare.** Cerca indizi che l'app regala: la command line
      eseguita, un link alla doc dello schema, un suggerimento sul formato dell'input, un testo di
      istruzioni. Segna i **parametri controllabili** (URL `?x=`, campi POST, ricerca, dropdown).
- [ ] **Rileggi la consegna** per capire: (a) qual è l'**obiettivo** (alert? leggere un file? flag
      nel DB?), (b) la consegna **nomina o esclude** una famiglia? (c) cosa esattamente va
      consegnato (uno `payload.png` o più `exploitN.png`? cosa deve contenere il `web.txt`?).

---

## 1. Classificazione — sonda l'input, guarda l'interprete

Individua l'input più promettente e mandagli, **uno alla volta**, le sonde. Ogni sonda rompe un
interprete diverso; la reazione rivela la famiglia. **Parti dallo scenario più rapido da escludere.**

| # | Sonda | Reazione che conferma | Famiglia |
|---|---|---|---|
| 1 | `<b>x</b>` / `<img src=x onerror=alert(1)>` | grassetto interpretato / alert parte | XSS (output riflesso in HTML) |
| 2 | `'` | errore SQL / cambia n. righe | SQL Injection |
| 3 | `;` `\|` `` ` `` `#` | errore shell / output di comando / command line mostrata cambia | Command Injection |
| 4 | `../` / `/etc/passwd` | contenuto file / errore con un path | Path Traversal / LFI |

Scorciatoie di classificazione dalla consegna/contesto (spesso decidono senza sonda):
- "Client Side" / "eseguire alert o prompt" → **XSS**.
- "siti che interrogano database" / "flag nel database" → **SQLi**.
- "Server Side, non sono coinvolti database" → **Path Traversal** (se l'app *legge file*) o
  **Command Injection** (se l'app *esegue e mostra un comando*).
- "identificare il tipo di vulnerabilità" → non te la dice: usa le sonde.
- Nome immagine docker: `vuln-decoder`→XSS, `vuln-finder`→CI, `vuln-file-browser`→traversal, `union.sh`→SQLi.

**Scrivi subito nel `web.txt` il "processo logico" di classificazione**: quali sonde hai provato,
quali errori/reazioni hai visto, e perché concludi per una certa famiglia. È esattamente ciò che il
Caso 4 chiede ("il processo logico col quale si è dedotta la vulnerabilità") e che il web.txt
ufficiale del Caso 3 mostra come modello.

---

## 2. Sfruttamento per famiglia (i quattro algoritmi)

Dettaglio passo-passo nei rami §2–§5 di `guida_esame_web.md`. Sintesi operativa:

- **XSS** → conferma riflessione (`<b>`) → `<script>alert()` → se filtrato, `<img src=x onerror=alert(1)>`
  → bypassa ostacoli client (`maxlength` via inspector/POST) e involucri (base64) → screenshot alert.
- **SQLi UNION** → `' OR '1'='1` (conferma) → conta colonne (`UNION select NULL,...` / `ORDER BY n`) →
  trova colonne visibili → enumera tabelle (`sqlite_schema`) → `UNION select * from <tab>` → screenshot flag.
- **SQLi BLIND** (se l'output NON è riflesso: solo "trovato/non trovato", pagina diversa, o solo il
  tempo) → conferma oracolo `' AND 1=1--` vs `' AND 1=2--` (risposte diverse) → lunghezza con
  `length()` (bisezione) → estrai char-per-char con `substr()`+`unicode()`/`ascii()` (bisezione sul
  codice ASCII, ~7 richieste/char) → se manca pure la risposta binaria, **time-based** (`sleep()` su
  MySQL; su **SQLite niente SLEEP** → heavy query `randomblob`). Dettaglio in §3-bis di
  `guida_esame_web.md`. **Preferisci sempre il boolean** al time-based (a mano il time-based è
  impraticabile).
- **Command Injection** → guarda dove finisce l'input nella command line → `#` per tagliare la coda →
  `;`/`&&`/`|` per concatenare → due tempi (scopri il path, poi `cat`) → screenshot output.
- **Path Traversal** → trova il parametro-file → `../../../../../tmp/flag.txt` (aumenta i `../`) o path
  assoluto → se `../` filtrato: `%2e%2e%2f`, `....//`, path assoluto → screenshot contenuto file.

---

## 3. Conferma di aver trovato IL vettore giusto (non un falso positivo)

- **XSS**: la prova è **codice che esegue**, non testo che appare. `<b>x</b>` che diventa grassetto
  conferma la *riflessione senza encoding* (necessaria) ma NON è ancora esecuzione JS: devi vedere
  un **alert/prompt nativo del browser**. Un `<script>` che compare *come testo* nella pagina =
  encodato = NON sfruttabile da lì.
- **SQLi**: `' OR '1'='1` che restituisce **più righe** del normale è la conferma. Un semplice
  errore 500 su `'` indica che l'input tocca SQL ma **non** che UNION funzionerà: devi arrivare fino
  a estrarre dati reali (le flag) — il conteggio colonne è il vero gate.
- **Command Injection**: la prova è l'**output di un comando tuo** (es. `id`, `cat`), non solo un
  errore. Vedere la command line cambiare con il tuo `;` è il segnale; l'output del comando iniettato
  è la conferma.
- **Path Traversal**: la prova è il **contenuto di un file di sistema/target** (la flag, `root:x:0:0`
  di `/etc/passwd`). Un errore "file not found" con un path conferma solo che l'input è un path reale.

**Falsi positivi / vicoli ciechi tipici:**
- Un tag che compare **come testo** (HTML-encoded) → l'app *è* difesa lì, cerca un altro punto di input.
- `'` che dà errore ma nessuna UNION possibile → forse è filtrato/parametrizzato solo in parte, o il
  conteggio colonne è sbagliato (ricontrollalo, è la causa n.1 di "sembra non vulnerabile").
- Il `maxlength` che tronca il payload fa sembrare l'XSS "non funzionante" → è un ostacolo client, non
  l'assenza della vuln (vedi §4 zona grigia).

---

## 4. §4 — Zone grigie e bivi (lo spirito del §0.5 di iptables: dove si sbaglia strada)

Questi sono i punti dove, sotto stress d'esame, si perde il filo o si confonde una famiglia con
un'altra. Nati risolvendo davvero i 5 casi del pool.

### 4.1 "`<script>` non funziona" ⇒ NON "niente XSS"
Il bivio più costoso. Nei Casi 1 e 3 il primo payload `<script>alert()` viene **filtrato** e l'app
risponde "error". Lo studente inesperto conclude "non è XSS" e cambia pista. **Sbagliato**: il filtro
copre quasi sempre solo la stringa letterale `script`. La mossa corretta è provare **subito** un
vettore script-less (`<img src=x onerror=...>`, `<svg onload=...>`). Regola: *un blocco su `<script>`
è la conferma che c'è un filtro, quindi che c'è qualcosa da bypassare, non che la vuln non esista.*

### 4.2 Difesa client-side vs filtro server-side: sono due ostacoli distinti
Nel Caso 3 ci sono **due** ostacoli indipendenti: (a) `maxlength=20` sul campo, (b) filtro server su
`script`. Confonderli fa girare a vuoto ("il mio payload non funziona" — ma è troncato, non filtrato;
oppure "è troppo lungo" — ma il problema era il filtro). **Procedura**: prima manda un payload
qualunque *lungo* per verificare che il `maxlength` è bypassato (inspector o POST diretto), **poi**
lavora sul contenuto per il filtro. Un ostacolo alla volta.

### 4.3 Path Traversal ⇄ Command Injection: entrambe "server-side, no DB"
I Casi 2 e 4 hanno **la stessa frase di consegna** ("Server Side, non sono coinvolti database"). Il
bivio: quale delle due? **Discriminante**: cosa fa l'app con l'input. *Apre/mostra un file* per nome
→ **path traversal** (payload `../`). *Esegue un comando e ne mostra l'output* (spesso mostra la
"Command run:") → **command injection** (payload `;`/`#`). Il nome dell'immagine aiuta
(`file-browser` vs `finder`). Se resti in dubbio, **provale entrambe**: una delle due sonde
(`../../../../tmp/flag.txt` vs `flag.txt ; cat ... #`) reagirà.

### 4.4 Command Injection: perché serve `#`, e i due tempi
Nel Caso 4 il template del server appende `*.pem 2>/dev/null` **dopo** il tuo input. Se inietti solo
`; cat flag`, quella coda si attacca al tuo comando e lo rompe. Serve `#` (commento shell) per
**tagliare la coda**. E l'attacco è in **due tempi**: il percorso della flag è randomizzato →
mossa 1 `flag.txt #` (scopri il path), mossa 2 `flag.txt ; cat <path> #` (leggi). Saltare la mossa 1
= tirare a indovinare il path = perdere tempo.

### 4.5 SQLi UNION: il conteggio colonne è il collo di bottiglia
Nel Caso 5, se sbagli il numero di colonne, `UNION` dà errore e l'app **sembra non vulnerabile**.
Non abbandonare: ricontrolla il conteggio (`UNION select NULL,NULL,... --` aumentando i NULL, oppure
`ORDER BY n`). Secondo sotto-bivio: **quali** colonne sono visibili a schermo — non tutte. Metti dati
di test al posto dei NULL per scoprire le posizioni visibili prima di piazzarci i dati veri.

### 4.6 SQLi: la tabella di metadati dipende dal DBMS
`sqlite_schema` funziona **solo** su SQLite. Su MySQL è `information_schema.tables`; PostgreSQL idem;
Oracle `all_tables`. Usare la tabella di metadati del DBMS sbagliato = query che fallisce = falso
"non enumerabile". Riconosci il DBMS dagli indizi ("formato sqlite" nel Caso 5), dai messaggi
d'errore, dalla sintassi che funziona. Questo è un bivio silenzioso: non dà un errore "ovvio", solo
"nessun risultato".

### 4.7 Commento SQL `--` e lo spazio
`--` in molti motori deve essere seguito da uno spazio (o fine riga) per essere trattato come
commento. Nell'URL può servire `-- -` o `--%20`. Se l'iniezione "quasi funziona" ma dà errore di
sintassi sulla coda, il colpevole è spesso il commento non terminato correttamente.

### 4.8 SQLi cieca (blind): UNION non serve se l'output non è riflesso
Bivio silenzioso e costoso. Se `'` tocca SQL ma la pagina **non stampa mai i dati** (solo "utente
trovato/non trovato", una pagina che c'è o non c'è, un redirect), insistere con `UNION select ...` è
inutile: la seconda query gira ma il suo output **non viene mostrato**. Il test che scioglie il dubbio:
`' UNION select 'AAAA',... -- ` → se **`AAAA` non compare** ma la pagina reagisce lo stesso, sei in
**blind**. Da lì l'app è un **oracolo booleano**: `' AND 1=1--` (vero) vs `' AND 1=2--` (falso) danno
risposte diverse, e la flag si estrae **carattere per carattere** con `substr()` + bisezione sul codice
ASCII (`unicode()` su SQLite, `ascii()`/`ord()` su MySQL). Solo se manca **anche** la risposta binaria
si passa al **time-based** — e su **SQLite non esiste `SLEEP()`**: serve una *heavy query*
(`randomblob(...)` dentro `hex()`+`like()`) per bruciare tempo. A mano il time-based è lentissimo:
prima cerca meglio un segnale booleano, quasi sempre c'è. Algoritmo completo ed esempio lavorato in
§3-bis di `guida_esame_web.md`. **Deliverable diverso dal ramo UNION**: non uno screenshot di "flag
stampata", ma la **sequenza richiesta/risposta** che prova il canale booleano (i due esiti diversi di
`AND 1=1` vs `AND 1=2`, qualche passo di estrazione, la stringa ricostruita).

### 4.9 Codifica nell'URL e negli involucri
- Nell'URL, spazi → `%20` (o `+`), `&`/`#` vanno encodati se fanno parte del payload.
- Se l'app decodifica base64 prima di usare l'input (Caso 3), **codifica** il payload in base64; e
  ricorda che nella POST i caratteri base64 `+ / =` vanno a loro volta URL-encoded (`+`→`%2B`,
  `=`→`%3D`) — nel web.txt ufficiale il `+` finale è comparso come `%2B`.

---

## 5. Deliverable — cosa consegnare

- [ ] **Screenshot** numerati (`payload.png` singolo, o `exploit1.png..N` / `query1.png..N`): coprire
      **classificazione → ostacolo → bypass → successo**, non solo il risultato. Se la VM fa revert,
      salvali sull'host mano a mano.
- [ ] **`web.txt`** con struttura **VULNERABILITÀ / PASSI ESEGUITI / MITIGAZIONE** (+ contenuto/posizione
      flag se richiesto). Usa `template_report_web.md`. Includi il **ragionamento** di
      classificazione e il **perché** dei bypass — è il criterio di voto.
- [ ] **Rileggi la consegna specifica**: alcune chiedono esplicitamente "posizione e contenuto della
      flag" (Caso 4), o "l'errore di progetto del sito" (Caso 5). Rispondi a ogni punto richiesto.
