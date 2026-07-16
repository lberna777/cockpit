# Template — web.txt (Web Vulnerabilities)

> Struttura riutilizzabile per il deliverable testuale `web.txt` richiesto negli esercizi di tipo
> Web Vulnerabilities. Vale per **qualunque famiglia** (XSS, SQLi, Command Injection, Path Traversal).
> Vedi `modello_web_vulnerabilities.md` per 5 soluzioni ufficiali complete, `guida_esame_web.md` per
> il triage per famiglia, `procedura_operativa_web.md` per l'algoritmo e le zone grigie.
>
> **Regola d'oro (dalla consegna stessa)**: *"il livello di dettaglio e precisione della descrizione
> sarà utilizzato come valutazione della prova"*. Non descrivere solo il payload finale: racconta il
> **ragionamento** — come hai classificato la vulnerabilità, quali difese hai incontrato, come le hai
> aggirate. Ogni bivio superato documentato = punti.

---

## Struttura generale (copia e riempi)

```
VULNERABILITÀ: <famiglia + tecnica specifica>
  es. "Cross-Site Scripting (XSS) Riflesso"
      "SQL Injection (UNION-based, backend SQLite)"
      "OS Command Injection"
      "Path Traversal / Local File Inclusion"

--- (se la consegna lo chiede: CONTENUTO / POSIZIONE FLAG) ---
FLAG: <stringa/e esfiltrate>
POSIZIONE: <path del file o tabella/colonna del DB, se richiesto>

PASSI ESEGUITI:
1. [CLASSIFICAZIONE] Descrivi l'app e l'input controllabile individuato
   (parametro GET/POST/campo). Riporta le SONDE provate e la reazione:
   quale input ha generato quale errore/effetto, e perché concludi per
   questa famiglia. (È il "processo logico" che diversi esercizi valutano
   esplicitamente.)
2. [CONFERMA] Come hai verificato che è davvero sfruttabile (non un falso
   positivo): es. il tag interpretato / il n. di righe cambiato / l'output
   di un comando tuo / il contenuto di un file.
3. [OSTACOLI E BYPASS] Ogni difesa incontrata e come l'hai aggirata
   (filtro su una stringa, maxlength client-side, involucro base64,
   conteggio colonne, filtro su ../). Uno per uno.
4. [EXPLOIT FINALE] Il payload/URL/richiesta esatta che ha avuto successo,
   scritto per intero (riproducibile).
5. [SUCCESSO] Cosa dimostra la prova (l'alert, le flag, il contenuto del
   file) e come compare negli screenshot allegati.

MITIGAZIONE (punto di vista sysadmin/sviluppatore):
- <fix specifico per QUESTA vulnerabilità> (il più importante, per primo)
- <difesa in profondità / hardening generale>
- <principio generale: validare/sanitizzare ogni input esterno>
```

---

## Riempimenti pronti per famiglia (blocco VULNERABILITÀ + MITIGAZIONE)

### XSS riflesso
```
VULNERABILITÀ: Cross-Site Scripting (XSS) Riflesso

MITIGAZIONE:
- Output encoding: convertire < > " ' & nelle rispettive HTML entity prima di
  inserire QUALSIASI input utente nel markup della risposta (fix specifico).
- Whitelist server-side dei caratteri ammessi per il campo (es. solo
  alfanumerici per un "nome"), rifiutando i metacaratteri HTML.
- Content-Security-Policy restrittiva: vietare script inline e limitare le
  fonti di script (difesa in profondità).
- [se c'era un filtro debole:] il filtro su "script" era inefficace perché
  case-sensitive e non ricorsivo, e comunque aggirabile con vettori
  script-less (<img onerror>): la sanitizzazione va fatta per encoding
  dell'output, non per blacklist di parole.
```

### SQL Injection
```
VULNERABILITÀ: SQL Injection (UNION-based, backend SQLite)

MITIGAZIONE:
- Prepared statement / bind variables (PREPARE): separano codice SQL e dati,
  eliminando l'iniezione alla radice (fix vero).
- Whitelist dei valori ammessi del parametro (es. id numerico validato).
- Input validation che vieti i metacaratteri SQL (', --, ;) come minimo.
- Principio: mai concatenare input utente in una stringa di query.
```

### SQL Injection — variante BLIND (cieca)
```
VULNERABILITÀ: SQL Injection Blind (boolean-based, backend SQLite)
  [oppure: "... time-based" se l'unico segnale era il tempo di risposta]

PASSI ESEGUITI:
1. [CLASSIFICAZIONE] Il parametro <id> tocca una query SQL (l'apice ' cambia
   l'esito). MA l'app NON stampa i dati recuperati: risponde solo con un esito
   binario ("utente trovato"/"nessun utente" — o pagina diversa / redirect).
   Verificato che ' UNION select 'AAAA',... -- NON fa comparire 'AAAA':
   l'iniezione è quindi CIECA (blind), UNION-based non applicabile.
2. [ORACOLO BOOLEANO] Confermato che l'app funge da oracolo sì/no:
   ?id=Alice' AND 1=1--  -> "utente trovato"  (condizione VERA)
   ?id=Alice' AND 1=2--  -> "nessun utente"   (condizione FALSA)
   Le due risposte diverse dimostrano il canale booleano.
3. [ESTRAZIONE char-per-char] Determinata la lunghezza del dato con length()
   (ricerca binaria), poi estratto ogni carattere con
   substr(<subquery>, i, 1) confrontando il codice ASCII con unicode()
   (SQLite) tramite bisezione sull'intervallo 32-126 (~7 richieste/carattere).
   Algoritmo: per ogni posizione i, dimezzo l'intervallo dei codici in base
   alla risposta a  unicode(substr(SEGRETO,i,1)) > mid.
   [se time-based: il segnale VERO/FALSO è "risposta lenta/veloce"; su SQLite
    il ritardo è forzato con una heavy query randomblob(...) perché manca SLEEP.]
4. [EXPLOIT FINALE] Esempio di richiesta di estrazione (posizione 1):
   ?id=Alice' AND unicode(substr((SELECT val FROM flags LIMIT 1),1,1))>79--
   Ripetuta bisezione per ogni posizione fino a ricomporre la stringa.
5. [SUCCESSO] Flag ricostruita carattere per carattere dalle sole risposte
   binarie: <stringa>. La prova NON è un output stampato ma la SEQUENZA
   richiesta/risposta (vedi screenshot: i due esiti diversi di AND 1=1 / AND 1=2
   + alcuni passi di estrazione con il relativo esito).

MITIGAZIONE (punto di vista sysadmin/sviluppatore):
- Prepared statement / bind variables (PREPARE): elimina l'iniezione alla radice
  — vale identico al caso UNION, la tecnica di estrazione non cambia il fix.
- Whitelist dei valori ammessi del parametro; niente concatenazione di input in SQL.
- Nota: rendere l'output "cieco" NON è una difesa — il dato è comunque estraibile
  un bit alla volta; la vulnerabilità va chiusa a monte (query parametrizzate).
```

> **Come si documenta una blind (nota sul deliverable)**: non hai lo screenshot
> di "flag stampata a schermo" tipico del ramo UNION. La prova è la **catena di
> richieste/risposte binarie**. Cattura almeno: (a) `AND 1=1` vs `AND 1=2` con le
> due risposte **diverse** (prova che l'oracolo esiste), (b) 2-3 richieste di
> estrazione con il loro esito vero/falso, (c) la stringa finale ricostruita.
> Nel `web.txt` **scrivi l'algoritmo** (bisezione) e il perché: è il "livello di
> dettaglio del ragionamento" che vale il voto. Screenshot suggeriti:
> `query1.png` (oracolo 1=1/1=2), `query2..N.png` (passi di estrazione).

### Command Injection
```
VULNERABILITÀ: OS Command Injection

MITIGAZIONE:
- Non costruire una riga di comando con testo fornito dall'utente: usare le
  API/librerie native del linguaggio che implementano la funzionalità senza
  passare per una shell (fix vero).
- Se la shell è inevitabile: esecuzione senza shell (execve con argomenti
  separati, non system()); whitelist di pattern ammessi; escaping dei
  metacaratteri shell (; | & ` $ # ...) così che siano dati e non sintassi.
- Principio del minimo privilegio per il processo web.
```

### Path Traversal / LFI
```
VULNERABILITÀ: Path Traversal / Local File Inclusion

MITIGAZIONE:
- Canonicalizzare il percorso (realpath) e verificare che resti DENTRO la
  cartella base consentita prima di aprire il file (fix vero).
- Whitelist dei file ammessi, o accettare solo un id mappato server-side al
  file reale (mai il percorso grezzo dall'utente).
- Neutralizzare ../ e i percorsi assoluti; minimo privilegio del processo
  web (non deve poter leggere /tmp, /etc, ...).
```

---

## Esempio compilato (Caso 1 del pool — XSS riflesso, 13 giugno 2024)

```
VULNERABILITÀ: Cross-Site Scripting (XSS) Riflesso

PASSI ESEGUITI:
1. [CLASSIFICAZIONE] La pagina "XSS CHALLENGE" mostra "Hello SEC_EXAM"; nell'URL
   c'è il parametro name=SEC_EXAM. Cambiando name, il testo mostrato cambia:
   l'input è RIFLESSO nella pagina -> ipotesi XSS Riflesso.
2. [CONFERMA + OSTACOLO] Provato <script>alert("ciao")</script>: il sito
   risponde "error" -> esiste un filtro. Provate varianti (ScRiPT): nessuna
   variazione di "script" passa. Si scopre però che <a> NON è filtrato ->
   il filtro colpisce solo la parola "script", non tutti i tag.
3. [BYPASS] Scelto un vettore script-less: il tag <img> non è filtrato e
   permette esecuzione JS tramite l'handler onerror (src invalido -> l'errore
   scatta da solo, senza interazione utente).
4. [EXPLOIT FINALE]
   http://<IP>/xss/xss_exam.php?name=<img src="x" onerror="alert()">
5. [SUCCESSO] Il browser esegue il JS iniettato: compare l'alert nativo
   (screenshot payload.png) -> esecuzione arbitraria di codice lato client
   nel contesto dell'applicazione.

MITIGAZIONE:
- Output encoding di ogni input riflesso (< > " ' & -> HTML entity): fix
  specifico di questo bug.
- Whitelist dei caratteri ammessi per il parametro "name" (escludere < > /).
- CSP restrittiva contro script inline (difesa in profondità).
- Nota: il filtro su "script" è insufficiente perché aggirabile con <img>;
  la difesa corretta è l'encoding dell'output, non la blacklist di parole.
```
