# Guida Lab — Modulo S1: Principi Offensive Security + LAB Enumerazione
**Corso**: Lab Sicurezza Informatica T
**Materiale**: `Principi_delloffensive_security_20_febbraio.pdf` · `LAB_Enumerazione_25feb.html`
**VM**: `LabSicurezzaInformatica` (Parrot OS/Kali) + 3 VM target in VirtualBox
**Prerequisiti**: S0 (ambiente VM funzionante) · SysAdmin 3A (servizi) e 3D (networking base) — utili per capire cosa trovi

---

## Threat Model

- **Prospettiva attaccante**: nella fase di Reconnaissance & Enumeration si costruisce la mappa del bersaglio *prima* di toccare qualsiasi servizio. Ogni porta aperta, ogni banner, ogni username che riesci a leggere senza autenticarti è un dato che riduce l'incertezza e orienta le fasi successive (exploitation). La misconfiguration di un servizio (DB esposto su rete pubblica, SMTP che risponde a VRFY) ti regala informazioni che il difensore non voleva darti.
- **Prospettiva difensore**: ogni servizio esposto è superficie d'attacco. Limitare i banner, non esporre DB su porte non filtrate dal firewall, disabilitare VRFY su SMTP, usare un `robots.txt` sono contromisure concrete. Ma non esiste difesa completa dall'enumerazione: i sottodomini, i blocchi IP registrati all'IANA, i certificati TLS su `crt.sh` sono pubblici per definizione. Il difensore *deve* sapere cosa espone prima dell'attaccante.

---

## Setup

> ⚠️ **Snapshot obbligatorio** prima di avviare ogni target.

[fonte: PDF — LAB § 1]

1. Avvia la VM Parrot/Kali dal VirtualBox (se non già in esecuzione).

2. Crea le 3 VM target a partire dai dischi preconfigurati in `/opt/owa`:

   ```bash
   # Ripeti per ognuno dei tre dischi: Appliance-disk001.vdi / 002 / 003
   ```

   Per ciascuna VM in VirtualBox:
   - Tipo: Linux → Debian 64-bit
   - RAM: 1024 MB · CPU: 1 core
   - Disco: seleziona il file `.vdi` come disco esistente
   - Scheda di rete: **Host-only (vboxnet0)**
   - **Prima di avviare**: scatta uno snapshot
   - Avvia — osserva il boot nel terminale e prendi nota del nome della VM

owa-target1, owa-target2, owa-target3

3. Verifica che la rete host-only abbia il DHCP abilitato: apri VirtualBox → `Ctrl+H` (Network Manager) → Host-only Networks → spunta DHCP server.

4. Se non ancora fatto, crea lo snapshot baseline della VM Parrot/Kali:

   ```bash
   VBoxManage snapshot "LabSicurezzaInformatica" take "baseline-pulita"
   ```

---

## Esercizio 1 — Host Discovery

**Obiettivo**: trovare quali host tra i tre target hanno acquisito un IP sulla rete host-only e rispondo ai probe di rete.

**Concetto**: il primo passo di qualsiasi enumerazione è capire *chi c'è* sulla rete. Il ping tradizionale funziona su un host alla volta ed è spesso bloccato da firewall. Nmap con `-sn` sostituisce il ping con una serie di probe (ARP su rete locale, ICMP echo, TCP SYN su porte 80/443) che funzionano anche quando l'ICMP è filtrato. [fonte: PDF — slides "Enumerazione – host", "Enumerazione – servizi"]

> ⚠️ **Pattern ricorrente**: `sudo nmap -sn` — senza `sudo`, sulla rete host-only Nmap non può usare ARP e il risultato è più lento e meno affidabile. Aggiungi sempre `sudo` per questa scansione.

**Comando**:
```bash
sudo nmap -sn 192.168.56.0/24
```

**Anatomia del comando**:
- *Cosa stai scrivendo*: scansione di host discovery sull'intera subnet `/24`.
- *Perché lo stai scrivendo*: non conosci ancora gli IP delle 3 VM target; questa scansione ti dà la lista degli host attivi senza aprire connessioni TCP/UDP verso i servizi.
- *Parametri*:
  - `nmap`: lo scanner di rete più diffuso, capace di enumerare host, porte, versioni e OS [fonte: PDF — slide "Enumerazione – servizi"].
  - `-sn` (*ping scan*, ex `-sP`): esegue solo host discovery, senza scansione delle porte. Su LAN usa ARP; da remoto usa ICMP + TCP probe.
  - `192.168.56.0/24`: la subnet della rete host-only VirtualBox. Regola: è la rete tipica di vboxnet0 — **verifica la tua subnet con `ip a` prima di usare questo comando**.
- *Varianti*: `nmap -sn 192.168.56.1-254` (range esplicito); `nmap -sn 192.168.56.32,33,34` se già sai gli IP.

**Output atteso**:
```
Nmap scan report for 192.168.56.32
Host is up (0.007s latency).
Nmap scan report for 192.168.56.33
Host is up (0.001s latency).
Nmap scan report for 192.168.56.34
Host is up (0.001s latency).
```

**Cosa verificare**: tre host attivi. Se ne vedi di meno, una VM target non ha acquisito IP — ricontrolla che il DHCP di vboxnet0 sia abilitato.

> ⚠️ **Gli IP nell'output sono i tuoi, non quelli del PDF** — `.32/.33/.34` sono esempi del prof. Usa sempre gli IP che trovi tu con questo comando nelle scansioni successive.

---

## Esercizio 2 — Enumerazione Porte e Versioni Servizi

**Obiettivo**: mappare tutte le porte TCP aperte sui tre target e identificare quale servizio (e versione) gira su ciascuna.

**Concetto**: sapere che un host è attivo non basta. Ogni porta aperta è un potenziale punto d'ingresso. Nmap invia pacchetti TCP SYN (o completano il three-way handshake con `-sT`) e in base alla risposta classifica la porta come aperta/chiusa/filtrata. Per sapere *cosa* gira su una porta usa `-sV`: Nmap manda probe specifici e legge il banner che il servizio restituisce. Questo è il cuore dell'enumerazione. [fonte: PDF — slides "Enumerazione – servizi", "Servizi e porte"]

### 2a — Scansione TCP su tutte le porte

> ⚠️ **Pattern ricorrente**: la scansione Nmap di default copre solo ~1000 porte "popolari". La porta 1337 di t-2 (SSH non-standard) **non appare** senza `-p-`. Usa sempre `-p-` per non perdere servizi nascosti su porte non-standard.

```bash
nmap -sT 192.168.56.32-34 -p-
```

**Anatomia del comando**:
- *Cosa stai scrivendo*: scansione TCP connect su tutte le 65535 porte dei tre target.
- *Perché lo stai scrivendo*: vuoi la lista completa delle porte aperte — questa è la mappa grezza della superficie d'attacco.
- *Parametri*:
  - `-sT` (*TCP connect scan*): completa il three-way handshake (SYN → SYN-ACK → ACK). Non richiede privilegi root ma è più rumoroso di `-sS` (SYN scan). Rileva solo se la porta è aperta o chiusa, **non la versione del servizio**.
  - `192.168.56.32-34`: range di IP (sostituisci con i tuoi trovati all'esercizio 1).
  - `-p-`: scansiona tutte le porte da 1 a 65535. Senza questo flag Nmap usa le ~1000 porte più comuni.
- *Varianti*: `sudo nmap -sS 192.168.56.32-34 -p-` (SYN scan, più veloce e stealth, richiede root).

**Output atteso** [fonte: PDF — LAB § 3]:
```
Nmap scan report for 192.168.56.32
PORT     STATE SERVICE
22/tcp   open  ssh
80/tcp   open  http
3306/tcp open  mysql
5432/tcp open  postgresql

Nmap scan report for 192.168.56.33
PORT     STATE SERVICE
22/tcp   open  ssh
25/tcp   open  smtp
110/tcp  open  pop3
143/tcp  open  imap
993/tcp  open  imaps
995/tcp  open  pop3s
1337/tcp open  waste        ← classificato erroneamente, -sV lo correggerà

Nmap scan report for 192.168.56.34
PORT     STATE SERVICE
22/tcp   open  ssh
53/tcp   open  domain
80/tcp   open  http
139/tcp  open  netbios-ssn
445/tcp  open  microsoft-ds
8000/tcp open  http-alt
8001/tcp open  vcom-tunnel
```

**Cosa verificare**: vedi porte su tutti e tre i target. Nota che il servizio sulla 1337 è classificato "waste" — `-sT` non legge il banner, quindi mente.

### 2b — Version Detection sulle porte aperte

> ⚠️ **Pattern ricorrente**: `-sT` e `-sV` fanno cose diverse. `-sT` dice aperta/chiusa; `-sV` legge il banner e identifica il servizio reale. Non confonderli.

```bash
nmap -sV 192.168.56.32 -p 22,80,3306,5432
nmap -sV 192.168.56.33 -p 22,25,110,143,993,995,1337
nmap -sV 192.168.56.34 -p 22,53,80,139,445,8000,8001
```

**Anatomia del comando**:
- *Cosa stai scrivendo*: version detection mirata sulle porte già trovate.
- *Perché lo stai scrivendo*: sapere che la 3306 è "mysql" non basta — ti serve la versione per cercare vulnerabilità specifiche su CVE/exploit-db. E la 1337 va riclassificata. [fonte: PDF — "Pubblicare le vulnerabilità", CVE/exploit-db]
- *Parametri*:
  - `-sV` (*service/version detection*): invia probe specifici e legge i banner. Restituisce nome del servizio, versione, extra info (OS, protocollo).
  - `-p 22,80,3306,5432`: lista porte separate da **virgola** (non spazio).
- *Varianti*: `nmap -sV --version-intensity 9 ...` (più aggressivo, più lento).

> ⚠️ **Pattern ricorrente**: `-p 22 80 3306` — le porte separate da spazi fanno trattare `80` e `3306` come host aggiuntivi, non porte. Usa **sempre la virgola**: `-p 22,80,3306`.

**Output atteso** (t-2, nota la porta 1337) [fonte: PDF — LAB § 3]:
```
PORT     STATE SERVICE  VERSION
22/tcp   open  ssh      OpenSSH 9.2p1 Debian 2+deb12u4
25/tcp   open  smtp     Postfix smtpd
110/tcp  open  pop3     Dovecot pop3d
143/tcp  open  imap     Dovecot imapd
993/tcp  open  ssl/imap Dovecot imapd
995/tcp  open  ssl/pop3 Dovecot pop3d
1337/tcp open  ssh      OpenSSH 9.2p1 Debian   ← era "waste", è SSH su porta non-standard
```

**Cosa verificare**: la 1337 su t-2 è SSH. Su t-1 hai DB esposti (MariaDB, PostgreSQL). Su t-3 hai Samba (139/445) e un servizio ignoto su 8000.

---

## Esercizio 3 — Misconfiguration: Banner Grabbing e DB Esposti

**Obiettivo**: sfruttare le misconfigurazioni per estrarre informazioni sensibili senza ancora autenticarsi con credenziali valide.

**Concetto**: una misconfiguration è una configurazione errata che espone informazioni o accesso non intenzionali. SMTP con VRFY abilitato rivela username; un database esposto su rete pubblica senza autenticazione forte svela dati. Questo è il tipo di informazione che trasforma la reconnaissance in exploitation. [fonte: PDF — LAB § 4, "Misconfiguration servizi"]

### 3a — Banner Grabbing SMTP con netcat

```bash
nc <IP_t2> 25
```

**Anatomia del comando**:
- *Cosa stai scrivendo*: connessione TCP grezza alla porta 25 (SMTP) di t-2.
- *Perché lo stai scrivendo*: il server SMTP risponde con un banner che può rivelare informazioni di sistema. Netcat non implementa il protocollo SMTP — manda e riceve byte grezzi — così vedi esattamente cosa il server annuncia prima di qualsiasi autenticazione.
- *Parametri*:
  - `nc` (netcat): tool per connessioni TCP/UDP generiche. Riceve/manda dati grezzi senza interpretare il protocollo. Utilissimo per banner grabbing su qualsiasi servizio testuale (SMTP, POP3, HTTP, FTP).
  - `<IP_t2> 25`: indirizzo e porta di destinazione.
- *Varianti*: `nc -v <IP> 25` (verbose, mostra la connessione); `telnet <IP> 25` (alternativa classica).

**Output atteso** [fonte: PDF — LAB § 4]:
```
220 Talk to Postgres admin to get more info
```

**Cosa verificare**: il banner SMTP ti sta suggerendo di parlare con l'admin di Postgres — un indizio esplicito che c'è un DB da interrogare. Chiudi la connessione con `Ctrl+C`.

### 3b — Enumerazione PostgreSQL esposto

Il database PostgreSQL su t-1 è accessibile dall'esterno senza filtro di rete. Prima tenti un accesso con credenziali banali. [fonte: PDF — LAB § 4]

```bash
psql -U admin -h <IP_t1> -W -l
```

**Anatomia del comando**:
- *Cosa stai scrivendo*: connessione al server PostgreSQL di t-1 come utente `admin`, listando i database disponibili.
- *Perché lo stai scrivendo*: il banner SMTP ti ha suggerito Postgres. Tenti con username `admin` e password triviale per vedere cosa è accessibile — questa è la stessa logica di un attaccante che prova credenziali di default.
- *Parametri*:
  - `psql`: client a riga di comando per PostgreSQL.
  - `-U admin`: username con cui autenticarsi.
  - `-h <IP_t1>`: host remoto (non localhost).
  - `-W`: forza la richiesta di password (non tentare autenticazione automatica).
  - `-l`: lista i database disponibili invece di aprire una sessione interattiva.
- Password da tentare: `admin` (credenziale di default banale).

**Output atteso**:
```
List of databases
   Name       |  Owner   ...
--------------+----------
 accounts_db  |  admin   ...
 postgres     |  postgres ...
```

**Cosa verificare**: esiste un database `accounts_db` — nome molto suggestivo.

```bash
psql -U admin -h <IP_t1> -W accounts_db
```

Una volta dentro la sessione interattiva:

```
\dt
```

> ⚠️ **Pattern ricorrente**: `\dt` è un meta-comando psql, `SELECT` è SQL. Vanno su **righe separate**. Se digiti `\dt SELECT * FROM accounts;` tutto sulla stessa riga, psql eseguirà solo `\dt` e ignorerà il resto — o si comporterà in modo imprevedibile.

```sql
SELECT * FROM accounts;
```

> ⚠️ **Pattern ricorrente**: se il prompt mostra `->` invece di `=#`, c'è un buffer sporco (un comando SQL lasciato a metà). Digita `\r` per resetterlo, poi riscrivi il comando.

**Output atteso**: una tabella con username e password (hash o in chiaro) degli utenti del sistema. Prendi nota di questi dati — serviranno per l'esercizio 4 e 6.

**Cosa verificare**: ottieni le credenziali. Esci da psql con `\q`.

---

## Esercizio 4 — Accesso con Credenziali ed Esplorazione dall'Interno

**Obiettivo**: usare le credenziali estratte dal DB per accedere via SSH ai target; eseguire brute force del PIN di root.

**Concetto**: dalla postura esterna (reconnaissance/enumeration) si passa alla postura interna. Dall'interno, NIDS e FW tipicamente non proteggono più il traffico — puoi raggiungere servizi che dall'esterno sarebbero bloccati. La fase di esplorazione interna alimenta le fasi successive (privilege escalation, lateral movement). [fonte: PDF — slide "La postura interna"]

### 4a — Accesso SSH con le credenziali trovate

Hai 4 servizi SSH disponibili: t-1:22, t-2:22, t-2:1337, t-3:22. Prova le credenziali trovate su tutti e quattro. [fonte: PDF — LAB § 5]

```bash
ssh <username>@<IP_t1>
ssh <username>@<IP_t2>
ssh -p 1337 <username>@<IP_t2>
ssh <username>@<IP_t3>
```

**Anatomia del comando**:
- *Cosa stai scrivendo*: connessione SSH autenticata con le credenziali trovate nel DB.
- *Perché lo stai scrivendo*: SSH è il canale di accesso remoto standard su Linux. Se le stesse credenziali del DB funzionano come account di sistema, hai accesso shell completo.
- *Parametri*:
  - `ssh <user>@<host>`: connessione SSH standard sulla porta 22.
  - `-p 1337`: specifica porta non-standard (per il secondo SSH di t-2).
- *Cosa aspettarsi*: alcuni servizi SSH non accettano autenticazione via password — accettano solo chiavi. Nota quali target entrano e quali rifiutano.

Una volta loggato su un target, cerca il file suggerito: [fonte: PDF — LAB § 5]

```bash
cat /home/turing/note.txt
```

**Output atteso**:
```
Reminder: to get full control of t-2, use your 4-digit pin
```

### 4b — Brute Force del PIN di root con Hydra

Il suggerimento indica un PIN di 4 cifre per root su t-2. Il target è il servizio SSH sulla porta **1337** (più vecchio, potrebbe avere policy diverse). [fonte: PDF — LAB § 5]

```bash
hydra -l root -x 4:4:1 ssh://<IP_t2>:1337
```

**Anatomia del comando**:
- *Cosa stai scrivendo*: brute force automatizzato di tutti i PIN numerici a 4 cifre (0000-9999) come password di `root` sul servizio SSH di t-2 porta 1337.
- *Perché lo stai scrivendo*: hai un indizio esplicito (4-digit pin) e un target preciso (t-2, root, porta 1337). Hydra automatizza i tentativi di login su decine di protocolli. L'insieme dei PIN a 4 cifre è piccolo (10.000 combinazioni) e attaccabile in tempi ragionevoli.
- *Parametri*:
  - `hydra`: tool per login brute force multi-protocollo.
  - `-l root`: username fisso (lowercase L, non maiuscolo I). Usa `root` come singolo target.
  - `-x 4:4:1`: genera password di lunghezza minima 4, massima 4, usando il charset `1` (solo cifre 0-9). Equivale a generare tutti i PIN da 0000 a 9999.
  - `ssh://<IP_t2>:1337`: protocollo SSH sull'host e porta specificati.
- *Varianti*: `hydra -l root -P /path/wordlist.txt ssh://<IP>:22` (wordlist invece di generazione); esplora `hydra -h` e `hydra -x -h` per la sintassi completa di generazione.

**Cosa verificare**: Hydra trova il PIN corretto e lo stampa. Prendi nota del PIN — serve per l'esercizio 6.

> **Nota**: questa operazione può richiedere qualche minuto (fino a 10.000 tentativi). Lasciala girare.

---

## Esercizio 5 — Hash Cracking con Wordlist Custom (CUPP + John)

**Obiettivo**: una volta ottenuto accesso root a t-2, estrarre gli hash delle password da `/root` e craccarli usando una wordlist generata con CUPP.

**Concetto**: gli hash delle password in `/etc/shadow` (o in file di backup) possono essere attaccati offline — nessun lockout, nessun IDS lo rileva. Una wordlist custom generata con CUPP (Common User Passwords Profiler) è più efficace di una wordlist generica perché incorpora dati personali del target (trovati in fase OSINT/enumeration). John the Ripper confronta ogni candidato con l'hash e segnala il match. [fonte: PDF — LAB § 6]

### 5a — Recupera i file di backup da t-2

Una volta autenticato come root su t-2:

```bash
ls /root/
```

**Output atteso**:
```
passwd.bak  shadow.bak
```

Copia i file sulla tua macchina Parrot per lavorarci localmente.

> ⚠️ **Pattern ricorrente**: `scp` va lanciato **da Parrot** (terminale locale), **non da dentro la sessione SSH**. Apri un nuovo terminale sulla VM Parrot e lancia:

```bash
scp -P 1337 root@<IP_t2>:/root/passwd.bak .
scp -P 1337 root@<IP_t2>:/root/shadow.bak .
```

> ⚠️ Se `scp` fallisce con errore SFTP subsystem, usa:
> ```bash
> ssh -p 1337 root@<IP_t2> "cat /root/shadow.bak" > shadow.bak
> ssh -p 1337 root@<IP_t2> "cat /root/passwd.bak" > passwd.bak
> ```

**Anatomia di scp**:
- *Cosa stai scrivendo*: copia sicura di un file remoto in locale.
- *Parametri*:
  - `-P 1337`: porta SSH non-standard (maiuscola P per scp, minuscola p per ssh).
  - `root@<IP>:/root/passwd.bak`: percorso remoto nel formato `user@host:/path`.
  - `.`: destinazione locale (directory corrente).

### 5b — Genera wordlist custom con CUPP

`passwd.bak` contiene informazioni sugli utenti (nome, home directory, shell) che puoi usare come input per CUPP.

```bash
cupp -i
```

**Anatomia del comando**:
- *Cosa stai scrivendo*: CUPP in modalità interattiva — ti chiede dati personali del target (nome, cognome, data di nascita, nickname, animali domestici, ecc.) e genera una wordlist con le combinazioni probabili.
- *Perché lo stai scrivendo*: una wordlist generica (es. rockyou.txt) ha milioni di entry ma copre male le password personalizzate. CUPP incorpora i dati che hai raccolto in fase di enumeration e genera combinazioni specifiche per quel target — molto più efficace.

Inserisci i dati trovati da `passwd.bak` quando CUPP lo chiede. CUPP genera un file `.txt` con la wordlist.

### 5c — Cracking degli hash con John the Ripper

Prima combina passwd.bak e shadow.bak nel formato che John si aspetta:

```bash
unshadow passwd.bak shadow.bak > combined.txt
```

Poi lancia il cracking con la wordlist custom:

```bash
john --wordlist=<nomefile_cupp>.txt combined.txt
```

**Anatomia del comando**:
- *Cosa stai scrivendo*: John the Ripper in modalità wordlist — hash su combined.txt, candidati da wordlist CUPP.
- *Parametri*:
  - `john`: tool per password cracking offline (supporta centinaia di formati hash).
  - `--wordlist=<file>`: specifica la wordlist da usare (invece di brute force puro).
  - `combined.txt`: file in formato `passwd:shadow` prodotto da `unshadow`.
- *Varianti*: `john --show combined.txt` per vedere le password già craccate; `john --format=sha512crypt combined.txt` se John non rileva il formato automaticamente.

**Cosa verificare**: John stampa le password trovate accanto ai rispettivi username.

---

## Connessioni

- **Con SysAdmin 3A (servizi systemd)**: i servizi che hai trovato con Nmap (sshd, Apache, Postfix, MariaDB, PostgreSQL) sono esattamente le unità systemd che `systemctl status` mostra su quella macchina. Enumerare le porte aperte dall'esterno = vedere la superficie d'attacco di ciò che 3A ti ha insegnato a configurare.
- **Con SysAdmin 3D (networking)**: `ip a` e `ss -tlnp` mostrano gli stessi servizi che Nmap scopre dall'esterno — ma dall'interno. Conoscere entrambe le viste (interna vs esterna) è fondamentale: l'attaccante vede l'esterno, il difensore monitora l'interno.
- **Con S3 (Web Security)**: la porta 80 su t-1 e t-3, e 8001 su t-3 (Werkzeug/Flask), saranno target del LAB web security. Quello che hai trovato qui con `-sV` è l'ingresso.
- **Con S10 (NIDS Suricata)**: la scansione Nmap che hai eseguito genera traffico rilevabile da un IDS. In S10 configurerai Suricata per rilevare esattamente questo tipo di probe.

<!-- AUTO-LINKS:START -->
## 🔗 Collegati

- [[lezione_moduloS1_offensive_security_enumerazione]]

**Hub:** [[master_map_studio]] · [[concept_maps]] · [[metodo_studio_esami_pratici]]
<!-- AUTO-LINKS:END -->
