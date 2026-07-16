# Modello Risolto — Web Vulnerabilities

> Fonte: `SIMULAZIONI ESAMI/SICINF/web_vulnerabilities.html` (Virtuale) — **5 esercizi d'esame reali**
> (13 giugno 2024 → 12 gennaio 2026), in ordine cronologico in questo file.
>
> **Nota tecnica sull'estrazione (aggiornamento 16/07/2026)**: come nel pool Iptables, le soluzioni
> ufficiali del docente non sono testo visibile scorrendo la pagina — sono allegate come **data URI
> in base64** dietro i link "SOLUZIONE" (`href="data:application/zip;base64,..."`,
> `data:application/g-zip;base64,...`, `data:text/plain;base64,...`). Vanno decodificate
> esplicitamente. Con questo metodo, **4 dei 5 esercizi del pool hanno soluzione ufficiale del
> docente recuperabile e trascritta fedelmente qui** (13 giu 2024, 10 lug 2025, 30 ott 2025, 12 gen
> 2026). L'unico senza soluzione ufficiale embedded è il **27 giugno 2025** (vuln-file-browser): nel
> suo thread HTML non c'è alcun link/allegato SOLUZIONE (verificato: gli unici 6 data-URI del file
> appartengono agli altri esercizi). Per quel caso la soluzione qui sotto è **ricostruita** ed
> etichettata esplicitamente come tale (ancorata al lab S3 e al tipo di vulnerabilità dichiarato),
> non spacciata per ufficiale.
>
> **Correzione rispetto alla versione precedente di questo file**: la nota finale della prima
> stesura affermava che le soluzioni di SQLi/path-traversal "non sono recuperabili dall'export HTML".
> Era **sbagliato**: erano recuperabili con la decodifica base64 (stesso meccanismo del pool
> iptables). Sono state recuperate e sono qui sotto.

---

## Come leggere questo file

Per ciascuno dei 5 casi: **data**, **consegna** trascritta dall'HTML, **famiglia di vulnerabilità**,
la **soluzione ufficiale** (testo `web.txt` del docente + descrizione degli screenshot reali) e una
sezione **"Perché funziona"** (meccanismo, non solo comandi). Alla fine di ogni caso, un blocco
**"⚠️ Bivio / zona grigia"** segnala dove uno studente sotto stress rischia di imboccare la strada
sbagliata (es. scambiare due famiglie che si somigliano). I 5 casi coprono **4 famiglie distinte**:
XSS riflesso (2 casi, con difese diverse), Command Injection, SQL Injection UNION-based, e Path
Traversal/LFI.

### Indice dei casi
1. **13 giugno 2024** — XSS riflesso (filtro debole su `<script>`, bypass con `<img onerror>`) — *soluzione ufficiale*
2. **27 giugno 2025** — Path Traversal / LFI (vuln-file-browser, esfiltrare `/tmp/flag.txt`) — *ricostruito, no soluzione ufficiale embedded*
3. **10 luglio 2025** — XSS riflesso via decoder base64 (vuln-decoder; limiti input + filtro `script`) — *soluzione ufficiale*
4. **30 ottobre 2025** — Command Injection (vuln-finder; injection nel pattern di `find`) — *soluzione ufficiale*
5. **12 gennaio 2026** — SQL Injection UNION-based (union.sh; estrazione tabella `flags` via `sqlite_schema`) — *soluzione ufficiale*

---

## Caso 1 — 13 giugno 2024 (XSS riflesso, filtro `script` bypassabile)

### Consegna originale

> Predisposizione: importare/lanciare il container docker fornito, collegarsi via browser
> all'indirizzo IP del container.
>
> **Challenge**: vulnerabilità Cross-Site Scripting (Client Side, vista a lezione). Obiettivo:
> sfruttare la XSS ed eseguire un `alert` o `prompt` JavaScript. **Non è possibile usare tool di
> scansione automatica, non è consentito alcun bruteforce.**

**Modalità di consegna**:
1. Un file `payload.(png|jpg)` che mostra l'esecuzione del payload e il relativo alert.
2. Un file `web.txt` che descrive: i passi che hanno portato a scoprire la vulnerabilità, e — dal
   punto di vista del sysadmin — come mitigarla/risolverla.

> Il livello di dettaglio della descrizione è criterio di valutazione.

### Soluzione modello

### `payload.png` (screenshot reale — trascrizione)

URL nella barra degli indirizzi:
```
http://172.17.0.2/xss/xss_exam.php?name=<img src="x" onerror="alert()">
```
Risultato: un dialog JavaScript nativo del browser compare sopra la pagina "ULISSE Research Team",
con intestazione `172.17.0.2` — prova che il codice JavaScript iniettato è stato eseguito dal
browser nel contesto della pagina.

### `web.txt`

```
VULNERABILITÀ: Cross-Site Scripting (XSS) Riflesso

PASSI ESEGUITI:
1. Navigata l'applicazione e individuato il parametro GET "name" nella
   pagina xss_exam.php: il suo valore viene restituito (riflesso) nel
   corpo della risposta HTML (es. "Hello <valore>").
2. Verificato che i caratteri speciali < > " non vengono codificati
   (HTML-encoded) nell'output: provando name=<b>test</b> il tag <b>
   viene interpretato dal browser invece di essere mostrato come
   testo — conferma l'assenza di sanitizzazione/escaping in output.
3. Costruito un payload che sfrutta un tag <img> con attributo
   onerror, che si attiva automaticamente perché src="x" non è
   un'immagine valida (non serve alcuna interazione dell'utente):
   <img src="x" onerror="alert()">
4. Iniettato il payload nel parametro GET tramite URL:
   http://172.17.0.2/xss/xss_exam.php?name=<img src="x" onerror="alert()">
5. Il browser esegue il JavaScript iniettato, mostrando l'alert:
   prova dell'esecuzione arbitraria di codice lato client nel
   contesto (origin) dell'applicazione vulnerabile.

MITIGAZIONE (punto di vista sysadmin/sviluppatore):
- Effettuare l'escaping HTML di ogni input utente riflesso in output
  (convertire < > " ' & nelle rispettive HTML entity) prima di
  inserirlo nel markup della risposta — è il fix specifico per questo
  bug.
- Impostare una Content-Security-Policy (CSP) restrittiva che vieti
  script inline e limiti le fonti di script consentite: riduce
  l'impatto anche se in futuro un altro punto di input sfugge alla
  sanitizzazione.
- Validare/whitelistare il formato atteso del parametro lato server
  (es. solo caratteri alfanumerici per un campo "nome"), rifiutando
  input contenenti metacaratteri HTML come < e >.
```

### Perché funziona (meccanismo, non solo comandi)

La causa è la mancanza di **output encoding**: il server prende il valore del parametro `name` e lo
inserisce **letteralmente** nell'HTML della risposta, senza convertire i caratteri speciali HTML
nelle entity corrispondenti. Il browser quindi non vede più una stringa di testo "nome utente", ma un
vero tag `<img>` da interpretare. L'attributo `onerror` è un *event handler* HTML: si attiva quando il
browser fallisce nel caricare la risorsa indicata da `src` — qui `src="x"` è deliberatamente non
valida, per garantire che l'errore (e quindi l'esecuzione del JS) scatti sempre, senza bisogno di
alcuna azione dell'utente (a differenza di un `onclick`, che richiederebbe un click).

Questo è **XSS riflesso** (reflected): il payload non viene salvato sul server (a differenza dello
XSS *stored*), ma viaggia nell'URL stesso e viene "riflesso" indietro nella risposta immediata — per
questo la prova di sfruttamento è un URL, non un'azione persistente sul sito.

### `web.txt` — testo ufficiale VERBATIM del docente (recuperato dal data-URI, 16/07/2026)

Il blocco `web.txt` più sopra era una **riformulazione pulita** (struttura VULNERABILITÀ/PASSI/
MITIGAZIONE) fatta nella prima stesura. Per fedeltà, ecco il testo **verbatim** dell'allegato
ufficiale (è prosa discorsiva, non a punti — utile perché mostra il *ragionamento* del docente, non
solo il risultato):

```
La challenge si presenta con una pagina dove viene mostrato un link ad una "XSS CHALLENGE".
Navigando sul link, si osserva come sulla pagina venga mostrato il testo "Hello SEC_EXAM".
Guardando l'URL, si nota come ci sia un parametro name che abbia come valore SEC_EXAM.
Provando a cambiare il parametro name, ci si accorge che questo viene cambiato anche nella pagina.
Si potrebbe quindi avere una XSS Reflected. Si prova un payload classico: <script>alert("ciao")</script>
Il sito restituisce "error". Forse è presente qualche meccanismo contro gli XSS o il payload è stato filtrato.
Proviamo ad utilizzare qualche variazione di script, come ScRiPT. A quanto pare nessuna variazione di
script permette di fare XSS. Si scopre però che <a> funziona, quindi si prova ad utilizzare altri tag.
Si scopre che il tag <img> non è filtrato. Quindi si procede ad utilizzare una classica XSS con img, ovvero:
<img src="x" onerror="alert()">
La vulnerabilità è dovuta ad una NON sanitizzazione dei dati in input, in particolare del parametro name
nel file xss_exam.php. Essendo che questo parametro viene poi mostrato nella pagina, si dovrebbe prima
sanificare, o attraverso escaping dei caratteri che possano portare a dell'HTML valido, o, in maniera
ancora più efficace, con una whitelist di caratteri ammessi per il nome (da cui escludere, per esempio <, >, /, ...).
In generale, ogni dato in input dall'esterno dovrebbe essere controllato e sanificato.
Il filtro impiegato dal file php è troppo permissivo, infatti basta utilizzare un tag diverso da script
per forzare una XSS.
```

**Dettaglio nuovo che emerge dal testo ufficiale (non nel riassunto sopra)**: qui **c'è un filtro**
che blocca `<script>` (restituisce "error"), a differenza dell'esempio "puro" del riassunto. Il
bypass è a due mosse: prima si scopre che il filtro colpisce solo `script` (non gli altri tag: `<a>`
passa), poi si sceglie un tag alternativo che porta esecuzione JS senza `script` → `<img onerror>`.
Questo lo rende **gemello del Caso 3** (10 luglio 2025), dove lo stesso filtro `script` viene aggirato
allo stesso modo — vedi il bivio là.

### ⚠️ Bivio / zona grigia — Caso 1

- **`<script>alert()` che ritorna "error" NON significa "sito non vulnerabile a XSS".** Significa
  "esiste un filtro, ma forse copre solo `<script>`". Non abbandonare la pista XSS al primo blocco:
  prova subito un vettore **script-less** (`<img src=x onerror=...>`, `<svg onload=...>`,
  `<body onload=...>`). Il 90% dei filtri d'esame blocca la stringa letterale `script` e nient'altro.
- **`onerror` vs `onclick`**: usa un handler che scatta **da solo** (`onerror` con `src` invalido,
  `onload`), non uno che richiede interazione (`onclick`) — la consegna vieta il "bruteforce" e vuole
  la prova dell'esecuzione automatica.

---

## Caso 2 — 27 giugno 2025 (Path Traversal / LFI — vuln-file-browser)

> ⚠️ **ATTENZIONE — questo è l'UNICO caso del pool SENZA soluzione ufficiale embedded.** Nel thread
> HTML del 27 giugno 2025 non esiste alcun link/allegato "SOLUZIONE" (verificato: i 6 data-URI del
> file appartengono tutti agli altri 4 esercizi). La soluzione qui sotto è una **RICOSTRUZIONE**
> ancorata a: (a) la famiglia di vulnerabilità dichiarata nella consegna ("Server Side, non sono
> coinvolti database"), (b) il nome dell'immagine (`vuln-file-browser`/`vuln-doc-browser` = un
> browser di documenti = lettura di file per percorso), (c) l'Esercizio 4 del lab S3
> (`guida_lab_moduloS3_web_security.md`), che copre esattamente LFI/path traversal su DVWA. **Non è il
> testo del docente.** Marcata come tale ovunque.

### Consegna originale (verbatim dall'HTML)

> **PREDISPOSIZIONE**: Scaricare l'immagine docker compressa `vuln-file-browser.tar.gz`; importarla
> con `zcat vuln-file-browser.tar.gz | sudo docker load`; lanciare
> `sudo docker run --rm -p 127.0.0.1:5000:5000 vuln-doc-browser`; collegarsi a `http://127.0.0.1:5000`.
>
> **CHALLENGE**: La challenge è basata su una vulnerabilità **Server Side** vista a lezione (**non
> sono coinvolti database**). Obiettivo dello studente è sfruttare la vulnerabilità ed **esfiltrare
> la flag contenuta in `/tmp/flag.txt`**. Non è possibile utilizzare tool di scansione automatica e
> non è consentito alcun tipo di "bruteforce".
>
> **CONSEGNA**: un file `payload.(png|jpg)` che mostra l'esecuzione del payload e relativo output; un
> file `web.txt` che descrive il contenuto di `flag.txt`, i passi per scoprire la vulnerabilità, e la
> mitigazione dal punto di vista del sysadmin.

### Famiglia: Path Traversal / Local File Inclusion (LFI)

**Perché è path traversal e non altro** (il ragionamento che porta a questa famiglia — questa parte
è il metodo, valido a prescindere dalla ricostruzione):

- "**vulnerabilità Server Side, non sono coinvolti database**" → esclude XSS (client-side) e SQLi
  (database). Restano le famiglie server-side che non toccano un DB: **path traversal/LFI** e
  **command injection**.
- "**esfiltrare `/tmp/flag.txt`**" (un percorso di file preciso e assoluto) + un'app che si chiama
  **file/document browser** → il target è la **lettura di un file arbitrario per percorso**. È la
  firma della **Path Traversal / LFI**: l'app apre file il cui nome/percorso arriva dall'utente, e
  con `../` (o un percorso assoluto) si esce dalla cartella prevista fino a `/tmp/flag.txt`.
- Se invece l'app mostrasse un "comando eseguito" (come nel Caso 4), sarebbe command injection. Qui
  il nome "file-browser" spinge su path traversal. **Nota onesta**: senza soluzione ufficiale non è
  escluso al 100% che fosse command injection; il metodo di exploit per entrambe è comunque nel Caso
  4 (CI) e qui sotto (traversal), quindi sei coperto in ogni caso.

### Soluzione RICOSTRUITA (non ufficiale) — `web.txt`

```
VULNERABILITÀ: Path Traversal / Local File Inclusion (lettura di file arbitrari)

PASSI ESEGUITI:
1. L'applicazione è un "file/document browser": mostra o apre file del server
   indicandone il nome/percorso in un parametro (es. ?file=doc1.txt, ?page=...,
   ?path=...). Individuato il parametro che controlla QUALE file viene letto.
2. Verificato che il valore finisce in una funzione di lettura file lato server
   senza sanitizzazione del percorso: inserendo un nome di file inesistente si
   ottiene un errore "file not found"/percorso nella risposta (conferma che il
   valore è usato come path reale sul filesystem).
3. Provata la risalita di directory con sequenze ../ per uscire dalla cartella
   dei documenti fino alla radice, puntando al file bersaglio assoluto:
   ?file=../../../../../tmp/flag.txt
   (il numero di ../ va aumentato incrementalmente finché non si raggiunge /;
   in eccesso è innocuo perché / non ha padre). In alternativa, se l'app accetta
   percorsi assoluti, direttamente ?file=/tmp/flag.txt
4. La risposta mostra il contenuto di /tmp/flag.txt = la flag.

CONTENUTO flag.txt: <la stringa restituita, es. SEC{...}> (varia a ogni container)

MITIGAZIONE (punto di vista sysadmin/sviluppatore):
- Non passare mai input utente direttamente a funzioni di apertura file. Risolvere
  il percorso (realpath/canonicalize) e verificare che resti DENTRO la cartella
  consentita (base dir) prima di leggere.
- Whitelist dei file/percorsi ammessi (es. un elenco fisso di documenti), oppure
  accettare solo un identificativo (id numerico) mappato server-side al file.
- Rimuovere/neutralizzare le sequenze ../ e i percorsi assoluti; principio del
  minimo privilegio (il processo web non deve poter leggere /tmp, /etc, ecc.).
```

`payload.png`: screenshot dell'URL con il payload `../../../../../tmp/flag.txt` nella barra e il
contenuto della flag mostrato nella pagina.

### Perché funziona

L'applicazione costruisce un percorso di file concatenando una directory base con l'input utente
(es. `open("/var/www/docs/" + file)`) e lo passa a una funzione di lettura **senza canonicalizzare
né validare**. Le sequenze `../` sono interpretate dal filesystem come "sali di un livello": partendo
da `/var/www/docs/` con abbastanza `../` si arriva a `/`, e da lì si scende su `/tmp/flag.txt`. È lo
stesso meccanismo dell'Esercizio 4 del lab S3 (`?page=../../../../../etc/passwd` su DVWA), dove
servivano **5** livelli di `../` perché la webroot era profonda 5 — da cui la regola "prova
incrementalmente il numero di `../`".

### ⚠️ Bivio / zona grigia — Caso 2

- **Path traversal vs Command Injection**: entrambe sono server-side e "senza database". Le distingui
  da **cosa fa l'app**: se *legge/mostra un file* per nome → traversal (payload `../`); se *esegue un
  comando* e ne mostra l'output (spesso mostra la command line, come nel Caso 4) → command injection
  (payload con `;`, `|`, `#`). Il segnale forte del Caso 2 è il nome "file browser" e il fatto che il
  bersaglio è **leggere** un file.
- **`../` di troppo non è un errore**: `/` non ha padre, quindi `../../../../../../` da qualunque
  profondità arriva comunque a `/`. Se un numero non basta, **aumentalo**, non abbandonare la pista.
- **Se `../` è filtrato**: prova percorso assoluto (`/tmp/flag.txt`), doppia codifica (`%2e%2e%2f`),
  o `....//` (che dopo la rimozione di un `../` interno ridiventa `../`). Sono i bypass classici.

---

## Caso 3 — 10 luglio 2025 (XSS riflesso via decoder base64 — vuln-decoder)

### Consegna originale (verbatim dall'HTML)

> **PREDISPOSIZIONE**: `vuln-decoder.tar.gz`; `zcat vuln-decoder.tar.gz | sudo docker load`;
> `sudo docker run --rm -p 5000:5000 vuln-decoder`; browser su `http://127.0.0.1:5000`.
>
> **CHALLENGE**: Obiettivo dello studente è **identificare il tipo di vulnerabilità e sfruttarla**.
> Non è consentito né in alcun modo utile utilizzare tool di scansione automatica o "bruteforce".
>
> **CONSEGNA**: più screenshot numerati `exploitN.png` che mostrano i passaggi fondamentali
> dell'exploit e il suo successo; un file `web.txt` con i passi e la mitigazione.

Particolarità: la consegna **non dice quale vulnerabilità è** — parte del compito è classificarla.
L'app è un "Base64 Decoder": prende una stringa, la decodifica da base64, e **mostra il risultato**
nella pagina.

### Famiglia: XSS riflesso (attraverso un passaggio di decodifica base64) + bypass di due difese

### `web.txt` — testo ufficiale VERBATIM (recuperato dal data-URI zip)

```
La pagina presenta una casella di input, e suggerisce che il compito svolto dal sito sia quello di
decodificare stringhe fornite in formato base64.

In presenza di input controllabili dal client, questi possono interagire col server in vari modi, tra cui:
- componendo una query SQL
- componendo una riga di comando
- componendo un percorso di file o cartella
- venendo integrati nella pagina di risposta

Tentando diversi tipi di input si può capire in quale caso ci si trova, sulla base del fatto che alcuni
caratteri speciali inseriti provochino o no errori che facciano capire come la stringa stessa viene usata.

In questo caso, qualsiasi stringa "leggibile", con caratteri speciali per SQL o shell o path, inserita
provoca la visualizzazione dell'errore "stringa base64 non valida", per cui si traggono tre conclusioni:
- l'input deve effettivamente essere fornito in base64
- è estremamente improbabile che venga usato per una query (ritorna solo quanto inserito, non altri dati)
- pare che non venga trattato con una riga di comando tipo "echo $input | base64 -d" (i caratteri
  speciali della shell non influenzano l'esecuzione)

L'ipotesi più probabile, dato che il risultato della decodifica viene riportato al browser, è che si
possa tentare un attacco di Reflected XSS.

[XSS = iniezione di codice (JavaScript) eseguito nel browser degli altri utenti: furto di cookie,
sessioni, dati sensibili.]

Si può quindi tentare di codificare in base64 il tipico <script>alert("vuln")</script>

Primo ostacolo: l'input field è limitato a 20 caratteri
Soluzione:
a) usare l'inspector per modificare la proprietà del campo input rimuovendo il limite
b) usare Burp per creare la richiesta POST, intercettando una richiesta e sostituendo l'input con la
   versione codificata in base64 della stringa da iniettare

Secondo ostacolo: la parola "script" viene filtrata lato server, sostituendola con la stringa vuota
Soluzione:
a) scrivere "script" in modi diversi -- la sostituzione è case sensitive (Script passa) e non è
   reiterata (scrscriptipt diventa script)
b) usare eventi, iniettando <img src="" onerror='alert("vuln")'>

Quest'ultima stringa, codificata in base64, è:
PGltZyBzcmM9IiIgb25lcnJvcj0nYWxlcnQoInZ1bG4iKSc+

La richiesta finale composta con Burp (estratto):
POST / HTTP/1.1
Host: 127.0.0.1:5000
Content-Type: application/x-www-form-urlencoded
...
b64=PGltZyBzcmM9IiIgb25lcnJvcj0nYWxlcnQoInZ1bG4iKSc%2B

Per mitigare: sanitizzare l'input, a monte della decodifica (escaping dei caratteri speciali della
shell, se si teme uso in command line) e a valle della decodifica base64 (convertendo i caratteri
speciali HTML in modo che il browser li visualizzi testualmente e non li interpreti come tag).
```

Screenshot (`exploit1..6.png`): il flusso mostra la pagina "Base64 Decoder", i tentativi di
classificazione, e infine (`exploit6.png`) l'**alert JavaScript nativo "127.0.0.1:5000 says — vuln"**
= prova dell'esecuzione. Il payload finale iniettato è `<img src="" onerror='alert("vuln")'>` fornito
in base64.

### Perché funziona

Il decoder prende l'input, lo decodifica da base64, e **inserisce il testo decodificato nell'HTML
della risposta senza output-encoding** → XSS riflesso classico, ma con due strati in più:

1. **Lo strato base64**: il payload va **codificato** perché il server lo decodifica prima di
   rifletterlo. Se scrivessi il tag in chiaro, verrebbe visto come "base64 non valido". È solo un
   involucro: dentro c'è lo stesso `<img onerror>` del Caso 1.
2. **Il limite di 20 caratteri sul campo input** è una difesa **solo lato client** (attributo
   `maxlength`): si aggira modificando il DOM con l'inspector, oppure — meglio — inviando la richiesta
   POST direttamente (Burp/curl), che non passa affatto dal campo HTML.
3. **Il filtro `script` lato server** è debole: sostituisce la stringa `script` con vuoto, ma è
   **case-sensitive** (`ScRiPT` sopravvive) e **non ricorsivo** (`scrscriptipt` → dopo aver tolto il
   `script` interno diventa `script`). In ogni caso lo si evita del tutto usando un vettore
   script-less (`<img onerror>`) — stessa mossa del Caso 1.

### ⚠️ Bivio / zona grigia — Caso 3

- **La procedura di classificazione all'inizio del web.txt è oro d'esame**: davanti a un input
  "misterioso", prova input che romperebbero **ciascun** interprete e guarda l'errore — `'` (SQL),
  `; | \`` (shell), `../` (path), `<b>` (HTML). L'errore ti dice a quale interprete arriva l'input.
  Qui l'errore "base64 non valido" per qualunque cosa non-base64 rivela che c'è un layer di decodifica
  prima, e che l'output viene riflesso → XSS.
- **Non farti fuorviare dal `maxlength=20`**: NON è una vera difesa, è client-side. Se il payload non
  ci sta nel campo, la strada NON è "trova un payload più corto" (rischio di perdere tempo), è
  "bypassa il campo" (inspector o POST diretto).
- **`maxlength` bypass vs filtro server**: sono due ostacoli **distinti e indipendenti**. Uno studente
  sotto stress può confonderli e pensare che il payload "non funzioni" per il filtro quando in realtà
  è stato troncato dal maxlength (o viceversa). Affrontali uno alla volta: prima manda un payload
  qualsiasi lungo per verificare che il maxlength è bypassato, poi lavora sul filtro `script`.
- **Codifica base64 corretta**: ricordati che nella POST i caratteri `+` `/` `=` vanno URL-encoded
  (`=` → `%3D`, `+` → `%2B`). Nell'esempio ufficiale il trailing `>` codificato finisce come `%2B`
  (era un `+` in base64).

---

## Caso 4 — 30 ottobre 2025 (Command Injection — vuln-finder)

### Consegna originale (verbatim dall'HTML)

> **PREDISPOSIZIONE**: `vuln-finder.tar.gz`; `zcat vuln-finder.tar.gz | sudo docker load`;
> `sudo docker run --rm -p 5000:5000 vuln-finder`; browser su `http://127.0.0.1:5000`.
>
> **CHALLENGE**: Obiettivo dello studente è **sfruttare la vulnerabilità per trovare il file
> `flag.txt` ed estrarne il contenuto**. Non è consentito né utile usare scansione automatica o
> "bruteforce".
>
> **CONSEGNA**: screenshot numerati `exploit1.png, exploit2.png, ...`; un file `web.txt` che descrive
> il **processo logico** con cui si è dedotta la vulnerabilità, il **principio** della vulnerabilità e
> come si sono **aggirate le difese**, la mitigazione, e **posizione e contenuto** di `flag.txt`.

### Famiglia: OS Command Injection (iniezione in una riga di comando `find`)

### `web.txt` — testo ufficiale VERBATIM (recuperato dal data-URI g-zip)

```
Aprendo la pagina vediamo che è presente una barra di ricerca, l'elemento vulnerabile.

Viene anche mostrato il comando eseguito lato server, che inizialmente è
find / \( -path /proc -o -path /sys -o -path /run -o -path /dev \) -prune -o -name \*.pem 2>/dev/null

Inserendo un pattern nella barra di ricerca, ad esempio ANF, si nota in che punto esso viene inserito:
find / \( ... \) -prune -o -name ANF\*.pem 2>/dev/null
e il risultato è di cercare tutti i file il cui nome inizia con il pattern e termina con .pem
(screenshot 1)

Il sistema è chiaramente vulnerabile a una COMMAND INJECTION.

Per prima cosa, sfruttando il comando find già predisposto (che cerca ricorsivamente dalla root), si
cerca il file di nome flag.txt. Per farlo si deve neutralizzare la parte che appende .pem al pattern:
è sufficiente inserire come pattern il nome desiderato seguito da un carattere shell di commento:
flag.txt #
(screenshot 2)

Trovato il file:
/usr/local/share/325SQTNCIGVRGDRX/DMEW5LUIQQJ3IH5P/flag.txt
(nota: cambia a ogni esecuzione del container)
si procede a iniettare il comando per esfiltrarne il contenuto, usando come pattern:
flag.txt ; cat /usr/local/share/325SQTNCIGVRGDRX/DMEW5LUIQQJ3IH5P/flag.txt #

Questo causa l'esecuzione di
find / \( ... \) -prune -o -name flag.txt ; cat /usr/local/share/.../flag.txt #\*.pem 2>/dev/null

che esegue correttamente il find, poi il cat, poi commenta la parte inutile del comando predefinito.

La flag è: SEC{YouFoundTheDeepFlagOnOctoberThirtieth}

Per evitare command injection:
- non costruire mai una riga di comando con testo fornito dall'utente; preferire librerie che
  implementino la funzionalità senza passare per un interprete sintattico
- se serve l'esecuzione shell, controllare attentamente l'input (whitelist di pattern ammessi) e
  neutralizzare (escaping) i caratteri pericolosi in modo che siano dati puri, non sintassi shell
```

Screenshot chiave (`exploit3.png`): l'app "**Find PEM files by prefix**" mostra il campo "Prefix
(PATTERN)" con `flag.txt ; cat /usr/local/share/.../flag.txt` e — sotto — "**Command run:**" con la
riga `find` completa, e in "**Results**" appare il percorso del file **e** la riga
`SEC{YouFoundTheDeepFlagOnOctoberThirtieth}`.

### Perché funziona

L'app costruisce **letteralmente** una riga di shell interpolando il pattern dell'utente:
`find / (...) -prune -o -name <PATTERN>*.pem 2>/dev/null`. Poiché il `<PATTERN>` finisce **non
quotato** in una rida passata a una shell, l'utente può iniettare **metacaratteri shell**:

- **`#`** = commento shell: tutto ciò che segue viene ignorato. Serve a **buttare via la coda**
  `*.pem 2>/dev/null` che altrimenti si attaccherebbe al payload e lo romperebbe. Prima mossa:
  `flag.txt #` trasforma il find in una ricerca del nome esatto `flag.txt`, rivelandone il percorso.
- **`;`** = separatore di comandi: esegue un secondo comando indipendente. Seconda mossa:
  `flag.txt ; cat <percorso> #` esegue il find (innocuo), poi `cat` del file trovato (esfiltrazione),
  poi `#` commenta la coda `*.pem 2>/dev/null`.

È un attacco **in due tempi** perché il percorso della flag è randomizzato per container: prima lo
**scopri** (`flag.txt #`), poi lo **leggi** (`; cat <percorso> #`).

### ⚠️ Bivio / zona grigia — Caso 4

- **Il segnale che è Command Injection e non altro**: l'app **mostra la command line eseguita**
  ("Command run: ..."). Quando vedi il tuo input comparire dentro un comando shell mostrato a schermo,
  la famiglia è quasi certamente command injection, e il gioco è **spezzare la sintassi** di quel
  comando specifico (guarda dove finisce il tuo input e cosa gli sta attaccato dopo).
- **Perché serve `#` e non basta `;`**: senza il commento finale, la coda del comando originale
  (`*.pem 2>/dev/null` o simili) si concatena al tuo `cat` e può causare errore o comportamento
  inatteso. `#` "taglia" tutto ciò che il template mette dopo il tuo payload. Alternative a `#`:
  concludere con un altro separatore che assorba la coda, o commentarla; su shell POSIX `#` è il più
  pulito.
- **Due tempi, non uno**: non tentare di leggere la flag prima di conoscerne il percorso. Il percorso
  è random per container: la mossa 1 (`flag.txt #`) serve a **scoprirlo**, la mossa 2 a leggerlo.
  Saltare la mossa 1 = tirare a indovinare = perdere tempo.
- **Command Injection vs SQL Injection**: entrambe "spezzano" un linguaggio interpolato. Le distingui
  dai caratteri che provocano l'errore/effetto: `;` `|` `` ` `` `#` `&&` → shell; `'` `"` `--` `UNION`
  → SQL. E dal contesto: un "finder/search di file" → shell; una "directory/lista di record" → SQL.

---

## Caso 5 — 12 gennaio 2026 (SQL Injection UNION-based — union.sh)

### Consegna originale (verbatim dall'HTML)

> **PREDISPOSIZIONE**: scaricare `union.sh.gpg`, decifrare con `gpg -d union.sh.gpg > union.sh` (la
> password è `esame`), `chmod +x union.sh`, lanciare `./union.sh`; browser su `http://127.0.0.1:8000`.
>
> **CHALLENGE**: La challenge è basata su una vulnerabilità, vista a lezione, presente su siti che
> **interrogano database**. Obiettivo: sfruttare la vulnerabilità ed **esfiltrare le flag contenute
> nel database**. Non è possibile usare scansione automatica né "bruteforce".
>
> **CONSEGNA**: screenshot `query1.png, query2.png, ...` che mostrano le query iniettate e le
> risposte; un file `web.txt` con le **flag**, la **logica** delle query, e la descrizione
> dell'**errore di progetto** e della mitigazione.

### Famiglia: SQL Injection, tecnica UNION-based, backend SQLite

### `web.txt` — testo ufficiale VERBATIM (recuperato dal data-URI g-zip)

```
1. Accedendo al sito e seguendo le istruzioni: visitando ?id=Alice il sito mostra "People Directory"
   con un menu drop-down di tre utenti. L'ipotesi più probabile è che il parametro id interroghi un DB.

Prima verifica: iniezione classica
  http://127.0.0.1:8000/?id=Alice'+OR+'1'='1
Risultano 7 utenti, con commenti utili una volta ricomposti:
  "Niente di interessante In questa tabella Forse bisogna Guardare altrove In questo database
   In formato sqlite Doc: http://127.0.0.1:8000/schemata.html"

La tecnica che consente di estrarre tabelle diverse da quella cablata è la SQLi UNION-BASED.

Per prima cosa determino il numero di colonne della query originale. Dopo qualche tentativo:
  http://127.0.0.1:8000/?id=Alice' UNION select NULL,NULL,NULL,NULL --
non dà errori. (=> 4 colonne)

Dalla documentazione al link indicato, la tabella coi metadati dello schema è sqlite_schema.
Le colonne interessanti sono tre, quindi lascio un NULL:
  http://127.0.0.1:8000/?id=Alice' UNION select type,name,tbl_name,NULL from sqlite_schema --
Rilevo tre tabelle: flags, people, sqlite_sequence.
Ipotizzo che people sia la tabella standard e sqlite_sequence sia metadati. Esploro flags,
ipotizzando abbia tante colonne quante people (SQLITE non offre un modo semplice di scoprire i nomi
delle colonne di ogni tabella):
  http://127.0.0.1:8000/?id=Alice' UNION select * from flags --

SUCCESSO (query5.png). Tre flag:  SEC_F1rstPrize   SEC_S3c0nd_PL4CE   SEC_3rd_qualified

VULNERABILITÀ E MITIGAZIONE
La vulnerabilità è dovuta a NON sanitizzazione del parametro id nell'URL. Ogni input esterno va
controllato:
- come minimo vietando caratteri che possano confondere interpreti (incluso SQL)
- meglio: evitare l'uso di interpreti, usando PREPARE (prepared statement / bind variables)
- se possibile, elencando esplicitamente i soli valori ammessi del parametro
```

Descrizione screenshot reali:
- `query1.png`: URL `?id=' OR '1'='1` → "Details (7 entries)", i record ID 1..3 hanno negli **Address**
  frammenti di messaggio ("Niente di interessante", "In questa tabella", "Forse bisogna"...) che
  ricomposti indicano di guardare in un altro database SQLite e linkano `schemata.html`.
- `query3.png`: `?id=Alice' UNION select NULL,NULL,NULL,NULL --` → "**2 entries**" (Alice + una riga
  `ID None — None` di NULL): la query UNION è **sintatticamente valida** → **4 colonne** confermate.
- `query4.png`: `?id=Alice' UNION select type,name,tbl_name,NULL from sqlite_schema --` → compaiono
  righe `ID table — flags`, `ID table — people`, `ID table — sqlite_sequence`: enumerate le tabelle.
- `query5.png`: `?id=Alice' UNION select * from flags --` → tre righe **Gold / Silver / Bronze** con
  negli Address le flag **`SEC_F1rstPrize`**, **`SEC_S3c0nd_PL4CE`**, **`SEC_3rd_qualified`**.

### Perché funziona

Il server costruisce la query concatenando l'input: `SELECT ... FROM people WHERE id = '<id>'`.
Chiudendo l'apice (`Alice'`) l'attaccante esce dal literal e aggiunge SQL proprio; `--` commenta il
resto della query originale (l'apice di chiusura che altrimenti resterebbe spaiato).

- **`' OR '1'='1`**: rende la `WHERE` sempre vera → il sito restituisce **tutte** le righe. Serve da
  **prova** che l'iniezione funziona (7 righe invece di 1) e, qui, rivela messaggi-indizio.
- **UNION-based**: `UNION SELECT` **accoda** i risultati di una **seconda** query arbitraria a quella
  originale. Vincolo: la seconda query deve avere **lo stesso numero di colonne** e tipi compatibili —
  per questo prima si trova il numero di colonne (4) con `UNION select NULL,NULL,NULL,NULL --`
  (i NULL sono compatibili con qualunque tipo).
- **`sqlite_schema`** (alias `sqlite_master`): la tabella di sistema di SQLite che elenca tutte le
  tabelle/indici del DB. È il modo per **scoprire** che esiste una tabella `flags` non prevista
  dall'app. Poi `UNION select * from flags` la svuota.

### ⚠️ Bivio / zona grigia — Caso 5

- **Trovare il numero di colonne è il collo di bottiglia**: se sbagli il conteggio, `UNION` dà errore
  e sembra "non vulnerabile". Due metodi: (a) `UNION select NULL,NULL,... --` aumentando i NULL finché
  **sparisce l'errore**; (b) `ORDER BY 1--`, `ORDER BY 2--`, ... finché dà errore (l'ultimo numero
  valido = numero di colonne). Con SQLite il metodo NULL è il più affidabile.
- **Quali colonne "escono" a schermo**: non tutte le colonne della query vengono mostrate. Metti dati
  di test (o `sqlite_version()`, stringhe) al posto dei NULL per capire **quale** posizione è
  visibile, e piazza lì i dati che vuoi leggere. Qui l'app mostra 3 dei 4 campi (id/name→heading,
  address, phone), per questo si tiene un NULL.
- **`sqlite_schema` è specifico di SQLite**. La consegna/gli indizi dicono "in formato sqlite": se il
  backend fosse MySQL useresti `information_schema.tables`/`.columns`; PostgreSQL idem; Oracle
  `all_tables`. Riconoscere il DBMS (dagli indizi, dai messaggi d'errore, dalla sintassi che
  funziona) decide **quale** tabella di metadati interrogare. Questo è il bivio che fa perdere tempo:
  usare la tabella di metadati del DBMS sbagliato.
- **SQLi vs Command Injection** (di nuovo): qui l'effetto di `'` è un errore/ cambiamento SQL e il
  contesto è "sito che interroga un database / directory di persone" → SQL, non shell.
- **`--` in SQLite richiede attenzione allo spazio**: `--` deve essere seguito da fine-riga o, in
  molti motori, da uno spazio per essere trattato come commento. Nell'URL a volte serve `-- -` o
  `--%20`. Se l'iniezione "quasi funziona" ma dà errore di sintassi sulla coda, sospetta il commento.

---

## Nota finale sul pool

Pool completo: **5 esercizi, 4 famiglie** (XSS riflesso ×2, Command Injection, SQLi UNION, Path
Traversal/LFI). **4/5 con soluzione ufficiale del docente trascritta verbatim** dai data-URI base64;
**1/5 (27 giugno 2025, path traversal) ricostruito** ed etichettato come tale — nel suo thread HTML
non c'è alcuna soluzione ufficiale allegata. Se un giorno comparisse quella soluzione su Virtuale,
va sostituita al blocco ricostruito del Caso 2.
