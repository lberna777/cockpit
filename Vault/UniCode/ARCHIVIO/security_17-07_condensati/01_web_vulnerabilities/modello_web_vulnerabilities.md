# Modello Risolto — Web Vulnerabilities

> Fonte: `SIMULAZIONI ESAMI/SICINF/web_vulnerabilities.html` (Virtuale), esercizio del
> **13 giugno 2024** (Cross-Site Scripting riflesso). Consegna e screenshot sono quelli reali della
> soluzione ufficiale.

---

## Consegna originale

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

---

## Soluzione modello

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

---

## Perché funziona (meccanismo, non solo comandi)

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

> **Nota**: gli altri esercizi in questo file coprono altre vulnerabilità server-side (path
> traversal/LFI in "vuln-file-browser", "vuln-decoder", "vuln-finder", SQL injection in "union.sh") —
> stessa struttura di consegna (screenshot dell'exploit + `web.txt` con passi e mitigazione), ma la
> soluzione specifica non è recuperabile dall'export HTML (allegati esterni non incorporati). Se vuoi
> un modello anche per SQL injection o path traversal, te lo risolvo su richiesta usando lo stesso
> procedimento.
