# Percorso Modulare — Dettaglio Materiali e Concetti

> Questo file contiene la descrizione completa di ogni modulo: materiali Virtuale, concetti chiave, esercizi, connessioni.
> NON contiene stati (⬜🔄✅) — quelli sono in `stato/corrente.md`.
> Caricare questo file solo quando serve il dettaglio di un modulo specifico (es. per `/lezione` o `/appunti`).

---

## Panoramica Corsi

| Corso | VM Richiesta |
|---|---|
| Lab Amministrazione di Sistemi T | Vagrant + Debian 12 |
| Lab Sicurezza Informatica T | Kali Linux / Parrot OS |
| Diritto dell'Informatica T | — |

**Connessione critica**: SysAdmin è prerequisito implicito di Security. I due lab vengono studiati in parallelo e si rinforzano a vicenda. Diritto è indipendente.

---

## Setup VM

### VM SysAdmin — Vagrant + Debian 12
```bash
cd ~/sysAdmin-lab
vagrant up --provider=virtualbox
vagrant ssh
```
Per spegnerla: `vagrant halt`

### VM Security — `LabSicurezzaInformatica` (VirtualBox)
- Debian 64-bit, 8 GB RAM, 4 CPU (verificato 18/06). Avvio: `VBoxManage startvm "LabSicurezzaInformatica"`
- VirtualBox con scheda host-only `vboxnet0`
- Credenziali standard: `kali`/`kali` o `parrot`/`parrot`
- ⚠️ **Zero snapshot al 18/06** — creare baseline pulita prima del primo esercizio:
  `VBoxManage snapshot "LabSicurezzaInformatica" take "baseline-pulita"`
- **Snapshot obbligatorio** prima di ogni esercizio di compromissione

---

## Metodologia di Studio Attivo

**Lab (SysAdmin + Security)**: leggi materiale → esegui sulla VM → verifica → completa esercizio lab
**Diritto**: leggi PDF → leggi lezione → rispondi autoverifica → scrivi appunti grezzi

Non segnare un modulo come completato se Lorenzo ha solo letto senza eseguire/rispondere.

---

## Corrispondenza Nomi Virtuale → File su Disco (SysAdmin)

| Titolo Virtuale | File su disco |
|---|---|
| "Introduzione alla materia [19 feb]" | `SLIDE TEORIA/SYSADM/01_01__quick-intro-2025-2026.pdf` |
| "Predisposizione ambiente virtuale [17 feb]" / "Accesso via SSH [24 feb]" | `SLIDE TEORIA/SYSADM/vagrant_ssh.pdf` |
| "Shell, processi, espansione [5 marzo]" | `SLIDE TEORIA/SYSADM/shell_processi_teoriaespansione.pdf` |
| "Shell scripting [10 marzo]" | `SLIDE TEORIA/SYSADM/shell_scripting.pdf` |
| "Gestione di utenti e file [19 marzo]" | `SLIDE TEORIA/SYSADM/21_22__utenti_file.pdf` |
| "Gestione dei servizi [12 marzo]" | `SLIDE TEORIA/SYSADM/gestione_servizi.pdf` |
| "Gestione dei pacchetti software [26 feb]" | `SLIDE TEORIA/SYSADM/software.pdf` |
| "Networking di base [16 aprile]" | `SLIDE TEORIA/SYSADM/net-config.pdf` |
| "Servizi rete infrastrutturali" | `SLIDE TEORIA/SYSADM/servizi_base_rete.pdf` |
| PDF lab SysAdmin | `SLIDE LAB/SYSADM/__ LAB __ <titolo> _ Virtuale.pdf` |

---

## BLOCCO 0: Fondamenta Linux

### Modulo 0A — Filesystem e Comandi Base Linux
**Corso**: SysAdmin
**Materiale Virtuale**:
- Teoria: "Introduzione alla materia e informazioni pratiche [19 feb]"
- Lab: "Predisposizione ambiente virtuale per le esercitazioni [17 feb]", "Accesso via SSH e creazione VM Vagrant [24 feb]", "Primi esercizi di accesso alla VM e gestione filesystem [24 feb]"
**Concetti chiave**: struttura filesystem Linux (`/`, `/home`, `/etc`, `/var`), navigazione (`ls`, `cd`, `pwd`), visualizzazione file (`cat`, `less`, `head`, `tail`), permessi in lettura (`r`, `w`, `x`), differenza tra utente normale e root
**Esercizio attivo**: Navigare il filesystem della VM Debian, creare una struttura di directory, leggere file di configurazione in `/etc`
**Connessione Security**: Kali Linux ha lo stesso filesystem — questi comandi sono usati in ogni lab di Security

### Modulo 0B — Pipe, Redirect e Filtri
**Corso**: SysAdmin
**Materiale Virtuale**:
- Teoria: "Shell, processi, espansione [5 marzo]"
- Lab: "Primi esercizi sulla riga di comando [24 feb]"
**Concetti chiave**: pipe (`|`), redirect (`>`, `>>`, `<`, `2>`, `2>&1`), filtri (`grep`, `sort`, `uniq`, `wc`, `cut`, `head`, `tail`)
**Esercizio attivo**: Esercizi "Conta Occorrenze" base dalla VM — pipeline su file di testo, analisi `/etc/passwd`, monitoraggio log
**Connessione Security**: `grep` e pipe usati massivamente per analisi di log, output di tool come Nmap

---

## BLOCCO 1: Bash Scripting

### Modulo 1A — Variabili, Condizioni, Loop
**Corso**: SysAdmin
**Materiale Virtuale**:
- Teoria: "Shell, processi, espansione [5 marzo]"
- Lab: "Shell scripting [10 marzo]"
**Concetti chiave**: variabili (`VAR=valore`, `$VAR`), condizionali (`if/then/else/fi`), loop (`for`, `while`), argomenti script (`$1`, `$2`, `$#`)
**Esercizio attivo**: Scrivere script che accetta argomenti, conta righe in file, itera su una lista
**Connessione Security**: Ogni tool di automazione offensiva/difensiva è uno script

### Modulo 1B — Funzioni, Case, Test
**Corso**: SysAdmin
**Materiale Virtuale**:
- Teoria: "Shell, processi, espansione [5 marzo]"
- Lab: "Shell scripting [10 marzo]"
**Concetti chiave**: funzioni (`function nome() {}`), costrutto `case`, test condizionali avanzati (`-f`, `-d`, `-z`, `-eq`), `exit codes`
**Esercizio attivo**: "Estensione degli esercizi risolti" + "Estensioni parametrico" da Virtuale
**Connessione Security**: Pattern usato in script di enumeration automatizzata

---

## BLOCCO 2: Utenti, Permessi e File

### Modulo 2A — Gestione Utenti e Permessi
**Corso**: SysAdmin
**Materiale Virtuale**:
- Teoria: "Gestione di utenti e file [19 marzo]"
- Lab: "Esempi di gestione utenti permessi e file [31 marzo]"
**Concetti chiave**: `useradd`, `usermod`, `passwd`, `groups`, permessi `rwx` in dettaglio, `chmod` (ottale e simbolico), `chown`, `chgrp`, `sudo` e `/etc/sudoers`, `su`
**Esercizio attivo**: Creare utenti sulla VM, assegnare permessi su file e directory, testare accessi con utenti diversi
**Connessione Security**: Privilege escalation sfrutta misconfigurazioni di permessi e sudo

### Modulo 2B — LAB Utenti, Permessi e File
**Corso**: SysAdmin
**Materiale Virtuale**:
- Lab: "Esempi di gestione utenti permessi e file [31 marzo]" (esercizi 1-2: /etc/skel, directory collaborativa con SGID)
**Esercizio attivo**: Esercizi 1 e 2 del lab — osservare `/etc/skel` + `/etc/default/useradd` + `/etc/login.defs`, poi creare utenti `maria`/`piero` con directory collaborativa SGID

### Modulo 2C — Gestione File: find, tar, rsync, Backup
**Corso**: SysAdmin
**Materiale Virtuale**:
- Teoria: "Gestione di utenti e file [19 marzo]" (sezione comandi file, archiviazione, backup)
- Lab: "Esempi di gestione utenti permessi e file [31 marzo]" (esercizi 3-6: dd, fuser/lsof, script find)
**Concetti chiave**: `find` avanzato (`-mtime`, `-type`, `-exec`), `locate`, `tar` (creazione/estrazione), compressione (`gzip`/`bzip2`/`xz`), `rsync`, `dd`, `fuser`, `lsof`, strategie di backup (full/incremental)
**Esercizio attivo**: Esercizi 3-6 del lab — prenotazione spazio con dd, file aperti, script copia flat, script copia con struttura

---

## BLOCCO 3: Servizi, Processi e Rete

### Modulo 3A — Gestione Servizi con Systemd
**Corso**: SysAdmin
**Materiale Virtuale**:
- Teoria: "Gestione dei servizi [12 marzo]"
- Lab: "Gestione dei servizi e monitoraggio [31 marzo]"
**Concetti chiave**: `systemd`, `systemctl` (start/stop/enable/disable/status), unit file, log con `journalctl`, monitoraggio processi (`ps`, `top`, `htop`), `at`, `cron`, timer systemd, `rsyslog`
**Esercizio attivo**: Lab — at, watchdog, nice execution, manipolazione crontab, configurazione rsyslog, logconfig, esame unit reali
**Connessione Security**: I servizi esposti su una macchina sono la sua superficie d'attacco

### Modulo 3B — Gestione dei Pacchetti Software
**Corso**: SysAdmin
**Materiale Virtuale**:
- Teoria: "Gestione dei pacchetti software [26 feb]"
**Concetti chiave**: `apt`, `dpkg`, repository, aggiornamenti di sistema, installazione/rimozione pacchetti
**Esercizio attivo**: Installare, aggiornare, rimuovere pacchetti sulla VM Debian

### Modulo 3C — Gestione dei Processi
**Corso**: SysAdmin
**Materiale Virtuale**:
- Teoria: "Shell, processi, espansione [5 marzo]" (sezione processi)
- Lab: "Gestione di processi [17 marzo]"
**Concetti chiave**: `ps`, `top`, `kill`, `jobs`, `fg`, `bg`, processi in foreground/background, segnali
**Esercizio attivo**: Lab Virtuale — avviare processi, monitorarli, inviargli segnali

### Modulo 3D — Networking di Base
**Corso**: SysAdmin
**Materiale Virtuale**:
- Teoria+Lab: `SLIDE TEORIA/SYSADM/net-config.pdf` + `servizi_base_rete.pdf`
**Concetti chiave**: interfacce di rete, `ip addr`, `ping`, `ss`/`netstat`, routing di base, DNS, `/etc/hosts`, `/etc/resolv.conf`
**Esercizio attivo**: Lab — configurare e verificare la rete sulla VM Debian (6 esercizi: ip a/r, ping, ss, DNS, hosts, tcpdump)

### Modulo 3E — Vagrant Multi-Machine e Configurazione Rete VM
**Corso**: SysAdmin
**Materiale Virtuale**:
- Lab: "Configurazione di un ambiente multi machine tramite Vagrant [21 apr]", "Configurazione della rete delle VM [21 apr]", "Struttura Vagrantfile e playbook [21 apr]"
**Concetti chiave**: Vagrantfile multi-machine, reti host-only/bridged/NAT, provisioning con Ansible, struttura playbook
**Esercizio attivo**: Creare ambiente multi-VM con Vagrantfile, configurare rete tra VM, provisionare con Ansible

### Modulo 3F — Automazione con Ansible
**Corso**: SysAdmin
**Materiale Virtuale**: "LAB Automazione con Ansible [14 aprile]"
**File locale**: `SLIDE LAB/SYSADM/__ LAB __ Automazione con Ansible [14 aprile] _ Virtuale.pdf` ✓
**Concetti chiave**: inventory, playbook YAML, moduli Ansible, idempotenza, SSH-based execution
**Esercizio attivo**: Lab — configurare nodo Vagrant da host tramite playbook

---

## BLOCCO 4: Funzionamento in Rete (avanzato)

> ⚠️ Sezione **aggiunta il 18/06** dopo l'analisi del corso reale (Virtuale id=70291).
> Questi tre moduli mancavano dalla mappa precedente. **Sono d'esame** (esercizi netmon/SNMP,
> autenticazione LDAP nelle prove passate). 4B e 4C partono da zero: PDF da scaricare.

### Modulo 4A — Servizi Base di Rete (DHCP, router via Ansible)
**Corso**: SysAdmin
**Materiale Virtuale**: "Servizi base rete [23 aprile]" + LAB DHCP/router (esercizi Ansible)
**File locale**: `SLIDE TEORIA/SYSADM/servizi_base_rete.pdf` ✓ (LAB da scaricare)
**Concetti chiave**: DHCP server/client, configurazione router Linux, NAT, provisioning servizi rete con Ansible
**Esercizio attivo**: "DHCP - Router due Client tramite Ansible", "DHCP++"

### Modulo 4B — SNMP / Monitoraggio Centralizzato ⚠️ DA ZERO
**Corso**: SysAdmin
**Materiale Virtuale**: "Monitoraggio centralizzato [30 aprile]" + "** LAB ** Esercizi introduttivi SNMP [5 maggio]"
**File locale**: ❌ **da scaricare** (teoria + LAB)
**Concetti chiave**: protocollo SNMP, OID/MIB (UCD-SNMP-MIB, NET-SNMP-EXTEND-MIB), Network Management Systems, agent/manager
**Esercizio attivo**: esercizi SNMP in ambiente multi-machine, "log di sistema, SNMP e scripting", "netmon"

### Modulo 4C — LDAP / Configurazione Centralizzata ⚠️ DA ZERO
**Corso**: SysAdmin
**Materiale Virtuale**: "Configurazione centralizzata [7 maggio]" + "** LAB ** Integrazione di LDAP per l'autenticazione su Linux [12 maggio]"
**File locale**: ❌ **da scaricare** (teoria + LAB)
**Concetti chiave**: protocollo LDAP, modello dei dati, entry LDIF, objectClass/attributeType, autenticazione Linux via LDAP, UID/GID, anonymous bind
**Esercizio attivo**: "Search and replace" su LDIF, integrazione autenticazione LDAP su VM

---

## Traccia Esercizi Scripting

*Traccia parallela ai moduli — esercizi progressivi orientati all'esame.*
- **lab_NN** — esercizi risolti dal prof (PDF "Esercizi di scripting risolti"): leggere → capire → eseguire → documentare
- **es_NN** — esercizi da costruire da zero

File in `esercizi/SYSADM/`. Approccio lab_: leggi il codice, predici il comportamento, poi esegui. Non copiare passivamente.

### Catena A — ls ricorsivo
| ID | Titolo | Tipo | Concetti nuovi |
|----|--------|------|----------------|
| lab_01 | ls ricorsivo (funzioni, subshell, cicli) | lab PDF p.4-5 | funzioni, subshell `( )`, `test -d`, ricorsione |
| lab_02 | ls ricorsivo alternative (while, read, filtri) | lab PDF p.6-7 | `ls -l \| while read`, `awk`, `[[ =~ ]]`, symlink parsing |
| lab_03 | ls ricorsivo estensioni (elif, $@) | lab PDF p.8 | `$@`, loop su argomenti multipli |
| es_03 | estparam.sh | assegnamento | estende lab_03: conta file per estensione in albero parametrico |

### Catena B — conversione e manipolazione del tempo
| ID | Titolo | Tipo | Concetti nuovi |
|----|--------|------|----------------|
| lab_04 | conversione tempo (calendario → promemoria) | lab PDF p.9 | `date +%s`, `date -d`, `mktemp`, `while sleep`, `egrep` |
| lab_05 | pianificazione eventi (plan.sh + remind.sh) | lab PDF p.10 | `grep -q`, `grep -x`, parametri obbligatori |
| lab_06 | esecuzione con cron | lab PDF p.11 | `grep -Fvx` per dedup crontab, `crontab file` |
| lab_07 | esecuzione con at | lab PDF p.12 | `at -t`, `flock`, lock su file condiviso |
| es_04 | estensione risolti (rimozione eventi) | assegnamento | estende lab_05–07 |

### Catena C — processi e segnali
| ID | Titolo | Tipo | Concetti nuovi |
|----|--------|------|----------------|
| es_05 | waitfile (case, sleep, exit code) | assegnamento | `case` su $3, retry con contatore, exit code semantici |
| es_06 | parallenne.sh (processi paralleli) | assegnamento | `$!`, PID tracking, `/proc/PID/comm`, `trap`, log su file |
| es_07 | segnali girati (debug script rotto) | assegnamento | `trap`, subshell e variabili, `tail -f \| while read`, BASHPID vs $$ |
| es_08 | conta occorrenze avanzato (parallelo+segnali) | assegnamento | `wc -l`, `head`/`tail` per dimezzare file, `wait`, `trap USR1` |

---

## Security — Lab Sicurezza Informatica T

*VM richiesta: Kali Linux / Parrot OS — Snapshot prima di ogni esercizio.*
*Esame pratico sui PC del lab: **3 esercizi tra 5 tipologie** (⭐). VM a cura dello studente.*

**Stato materiali — ✅ SCARICATO il 18/06** da Virtuale (id=70290):
- **Teoria** → `SLIDE TEORIA/SICINF/` (31 file PDF): tutti i moduli S1–S15.
- **Lab** → `SLIDE LAB/SICINF/` (16): walkthrough come **HTML autocontenuto** (immagini incorporate)
  + i LAB-PDF; incluse le soluzioni (Altoro, buffer overflow, pentesting target).
- **Prove d'esame** → `SIMULAZIONI ESAMI/SICINF/` (5 HTML): le 5 tipologie con testi+soluzioni+screenshot.
- **Esercizi** → `esercizi/SICINF/`: binari binary-exploitation (`write_var`, `secret_function`,
  `shellcode`, `returnlib`), pcap Suricata, sfide crypto + `COMPITI_security.md` (testi compiti).
- ⚠️ **Non scaricati** (esterni/grossi, contesto non-esame): repo web app vulnerabili (S3),
  `tls_files.tgz`/`netsec_a,b` (S13). I binari dei compiti coprono già il grosso di S4.

**Le 5 tipologie d'esame**: Integrity/privesc (S11) · NIDS (S10) · Iptables (S5) · Binary expl (S4) · Web vuln (S3).

### ─ Offensive Security ─

### Modulo S1 — Principi Offensive Security + LAB Enumerazione
**Materiale Virtuale**:
- Teoria: "Principi dell'offensive security [20 feb]"
- LAB: "** LAB ** Enumerazione [25 feb]"
**Concetti chiave**: vulnerability assessment e penetration testing, fasi di un attacco (reconnaissance → exploitation → post-exploitation), `nmap` (scansione porte, versioni, OS), banner grabbing, enumerazione utenti
**Esercizio attivo**: LAB su "Tre target combinati"
**Connessione SysAdmin**: I servizi configurati in 3A sono ciò che Nmap trova

### Modulo S2 — Autenticazione
**Materiale Virtuale**: "Autenticazione [27 feb]"
**Concetti chiave**: metodi di autenticazione, robustezza credenziali, brute force protection

### Modulo S3 — Web Security + LAB
**Materiale Virtuale**:
- Teoria: "Web security [6 mar]" — OWASP Top Ten 2025
- LAB: "**LAB** web security [11 mar]" — `pentestlab.sh`
**Concetti chiave**: SQL injection, XSS (stored/reflected), CSRF, directory traversal, OWASP Top Ten 2025
**Esercizio attivo**: `./pentestlab.sh start APP` — attaccare app vulnerabili su Parrot

### Modulo S4 — Binary Exploits + LAB Bruteforcing
**Materiale Virtuale**:
- Teoria: "Binary exploits [13 mar]"
- LAB: "** LAB ** bruteforcing e buffer overflows [18 mar]" — `tar xzf pwn_lab.tgz`
**Concetti chiave**: stack overflow, shellcode, return-oriented programming, contromisure (canary, NX, ASLR)
**Nota**: esercizi su binari x86_32 — non compatibili con Apple Silicon senza emulatore

### ─ Controllo dell'Accesso e Hardening ─

### Modulo S5 — Firewall: Teoria + Configurazione + LAB
**Materiale Virtuale**:
- Teoria: "Firewall [20 mar]", "Configurazione del packet filter di Linux [1 apr]"
- LAB: "** LAB ** Firewall [1 apr]"
**Concetti chiave**: `iptables`/`nftables`, catene INPUT/OUTPUT/FORWARD, politiche di default, stateful firewall
**Esercizio attivo**: Configurare firewall su VM, testare regole

### Modulo S6 — Sicurezza Fisica e Cloud
**Materiale Virtuale**: "Sicurezza fisica e collocazione in cloud [10 apr]"
**Concetti chiave**: attacchi fisici, sicurezza processo di avvio, supply chain attacks, collocazione in cloud, air gap jumping

### Modulo S7 — LAB Backdoor Injection
**Materiale Virtuale**: "** LAB ** Backdoor injection [15 apr]"
**Concetti chiave**: persistenza post-exploitation, backdoor su sistema compromesso
**Nota**: Snapshot VM prima dell'esercizio

### Modulo S8 — LAB Individuare e Filtrare Attacchi
**Materiale Virtuale**: "** LAB ** Individuare e filtrare attacchi [15 apr]"
**Esercizio attivo**: Esercitazione di riepilogo — dall'enumerazione alla mitigazione

### ─ Autorizzazione e Rilevazione ─

### Modulo S9 — Demoni di Sistema + Autorizzazione
**Materiale Virtuale**:
- "Demoni di sistema [17 apr]"
- "Autorizzazione [17 apr]"
- [approfondimento] "PAM - il framework di autenticazione e autorizzazione di Linux"
**Concetti chiave**: DAC, MAC, RBAC, implementazioni Linux (permessi, ACL, SELinux), autenticazione multifattore

### Modulo S10 — Rilevare gli Attacchi + LAB NIDS Suricata
**Materiale Virtuale**:
- Teoria: "Rilevare gli attacchi [8 apr]"
- LAB: "** LAB ** network intrusion detection [8 apr]" + Documentazione Suricata v7
**Concetti chiave**: IDS vs IPS, signature-based vs anomaly-based, regole Suricata, EVE JSON
**Esercizio attivo**: Installare Suricata, configurare regole, generare traffico da Kali

### Modulo S11 — Host-Based IDS + LAB Misconfiguration + LAB Pentesting Target
**⭐ Tipo esame**: Integrity check & privilege escalation
**Materiale Virtuale**:
- "Host-Based Intrusion Detection [17 apr]"
- LAB: "** LAB ** Esempi di misconfiguration [22 apr]"
- LAB: "** LAB ** Misconfiguration attacks e HIDS [22 apr]"
- LAB: "** LAB ** Pentesting target [6 maggio]" — VM x86_64, host-only con Parrot; enumerare → entrare → privesc → root (capstone offensivo, soluzione disponibile)
**Concetti chiave**: HIDS, rilevamento misconfigurazioni, privilege escalation alternativa, integrity check
**Esercizio attivo**: pentesting target completo + esercizi misconfiguration; allineato alla tipologia d'esame "integrity/privesc"

### ─ Network Security ─

### Modulo S12 — Sicurezza delle Comunicazioni
**Materiale Virtuale**: "Sicurezza delle comunicazioni [23 apr]"
**Concetti chiave**: richiami di reti, minacce ai diversi livelli dello stack protocollare

### Modulo S13 — Offensive Net Sec + Protezione delle Comunicazioni + TLS
**Materiale Virtuale**:
- LAB: "LAB: Offensive network security" (sniffing, spoofing, DoS) + "Comandi per l'esercitazione offensive net sec"
- "Protezione delle comunicazioni [15-20 maggio]"
- LAB: "** LAB** OpenSSL [20 maggio]" + "Altri esercizi configurazione servizi con TLS [20 maggio]" (`tls_files.tgz`)
**Concetti chiave**: sniffing/spoofing/DoS, ARP/DHCP poisoning, TLS/SSL, HTTPS su nginx, TLS su mosquitto, Heartbleed
**Esercizio attivo**: setup rete di test (`setup_infra.sh`), DoS, DHCP poisoning, attivazione HTTPS/TLS

### ─ Crittografia ─

### Modulo S14 — Crittografia: Fondamenti e Cifrari Moderni
**Materiale Virtuale**:
- "Introduzione alla crittografia [8 maggio]" (cifrari classici, sicurezza perfetta)
- "Cifrari moderni [8-13 maggio]" (simmetrici a blocchi/flusso, hash, RSA, firma digitale)
- "[approfondimento] Rainbow Tables"
**Concetti chiave**: trasposizione/sostituzione, one-time pad, AES, funzioni hash, crittografia asimmetrica, RSA, firma digitale, rainbow tables
**Esercizio attivo**: "Cracking e bruteforcing", "Password recovery"

### Modulo S15 — LAB gpg + Gestione delle Chiavi
**Materiale Virtuale**:
- "** LAB ** gpg [13 maggio]" (cifratura/firma, decifrazione/verifica)
- "Proprietà e gestione delle chiavi [15 maggio]"
**Concetti chiave**: gpg cifratura+firma, web of trust, generazione/robustezza/memorizzazione/distribuzione chiavi
**Esercizio attivo**: "Hash e GPG", verifica file firmato con chiave pubblica Prandini

---

## Diritto dell'Informatica T

*Indipendente dagli altri corsi. Metodologia: lettura PDF → lezione strutturata → sintesi scritta.*
*Normative di riferimento in `SLIDE TEORIA/DIRITTO INFORMATICO/NORMATIVE/` — citate inline, non moduli autonomi.*
*Schemi ripasso in `SLIDE TEORIA/DIRITTO INFORMATICO/Schemi utili per ripasso-20260521 (1)/` — utili per autoverifica finale.*
*Totale moduli: 13 (D1–D13).*

### Modulo D1 — Concetti Giuridici di Base
**PDF**: `01_DirInfo_2026_ConcettiBase_DEF.pdf`
**Concetti chiave**: fonti del diritto, gerarchia normativa, soggetti giuridici, persona fisica/giuridica, obbligazione, responsabilità civile e penale
**Appunti**: `claudeAppunti/APPUNTI DIRITTO/appunti_moduloD1_concetti_giuridici_base.md`

### Modulo D2 — Ricerca e Analisi delle Fonti del Diritto
**PDF**: `02_DirInfo_2026_RicercaFonti_DEF.pdf`
**Concetti chiave**: come trovare e leggere una norma, banche dati giuridiche, struttura di leggi e decreti, interpretazione normativa
**Appunti**: `claudeAppunti/APPUNTI DIRITTO/appunti_moduloD2_ricerca_fonti_diritto.md`

### Modulo D3 — Diritto d'Autore e Tutela Giuridica del Software
**PDF**: `03_DirInfo_2026_IPR_DEF.pdf`
**Concetti chiave**: diritto d'autore (L. 633/1941), opere dell'ingegno, tutela del software, diritti morali e patrimoniali, licenze, open source vs proprietario
**Appunti**: `claudeAppunti/APPUNTI DIRITTO/appunti_moduloD3_diritto_autore.md`

### Modulo D4 — Tutela Giuridica delle Banche Dati e Siti Web
**PDF**: `04_DirInfo_2025_BancheDatiSitiWeb_DEF.pdf`
**Concetti chiave**: tutela banche dati, diritto sui generis, siti web come opere, responsabilità hosting provider
**Appunti**: `claudeAppunti/APPUNTI DIRITTO/appunti_moduloD4_banche_dati_siti_web.md`

### Modulo D5 — Contratti a Oggetto Informatico
**PDF**: `05_DirInfo_2026_ContrInformatici_DEF.pdf`
**Concetti chiave**: tipologie contratto informatico, licenza d'uso, sviluppo software, SLA, outsourcing, contratto cloud
**Appunti**: `claudeAppunti/APPUNTI DIRITTO/appunti_moduloD5_contratti_informatici.md`

### Modulo D6 — Analisi di un Contratto di Sviluppo Software
**PDF**: `06_DirInfo_2026_SchemaContratt_DEF.pdf`
**Concetti chiave**: lettura guidata contratto reale, clausole fondamentali, garanzie, penali, proprietà intellettuale, foro competente
**Appunti**: `claudeAppunti/APPUNTI DIRITTO/appunti_moduloD6_contratto_sviluppo_software.md`

### Modulo D7 — La Proprietà Industriale
**PDF**: `07_DirInfo_2026_ProprietàIndustriale.pdf`
**Normativa**: `decreto-legislativo-10-02-2005-n-30.pdf` (Codice della Proprietà Industriale)
**Concetti chiave**: brevetti, marchi, segreti industriali, tutela invenzione software, differenza brevetto vs diritto d'autore

### Modulo D8 — Privacy e Protezione dei Dati Personali
**PDF**: `08_DirInfo_2026_Privacy_DEF.pdf`
**Normative**: GDPR (Reg. UE 2016/679), Codice Privacy (D.Lgs. 196/2003 s.m.i.)
**Concetti chiave**: principi trattamento (art. 5), basi giuridiche (art. 6), diritti interessati (artt. 15-22), titolare/responsabile, DPO, DPIA, notifica violazioni
**Appunti**: `claudeAppunti/APPUNTI DIRITTO/appunti_moduloD8_privacy_gdpr.md`

### Modulo D9 — Firme Elettroniche
**PDF**: `09_DirInfo_2026_FirmeElettr_DEF.pdf`
**Concetti chiave**: firma elettronica semplice/avanzata/qualificata, firma digitale, eIDAS (Reg. UE 910/2014), valore probatorio, certificati qualificati, TSP
**Appunti**: `claudeAppunti/APPUNTI DIRITTO/appunti_moduloD9_firme_elettroniche.md`

### Modulo D10 — Commercio Elettronico
**PDF**: `10_DirInfo_2026_CommercioElettronico_DEF.pdf`
**Concetti chiave**: D.Lgs. 70/2003, contratti online, obblighi informativi, responsabilità intermediari, country of origin principle

### Modulo D11 — Reati Informatici
**PDF**: `11_DirInfo_2026_ReatiInformatici_DEF.pdf`
**Concetti chiave**: accesso abusivo (art. 615-ter c.p.), danneggiamento informatico, frode informatica, Convenzione di Budapest

### Modulo D12 — AI Act
**PDF**: `12_DirInfo_2026_AI_Act_DEF.pdf`
**Schema ripasso**: `Schemi utili per ripasso-20260521 (1)/12_AIAct.pdf`
**Concetti chiave**: Reg. UE 2024/1689, classificazione sistemi AI per rischio, obblighi provider/deployer, GPAI

### Modulo D13 — Pacchetto Digitale Europeo (DSA, DMA, Data Act)
**PDF**: `13_DirInfo_2026_DSA_DMA_DataAct.pdf`
**Schema ripasso**: `Schemi utili per ripasso-20260521 (1)/13_PacchettoDigitaleEuropeo.pdf`
**Concetti chiave**: DSA (Reg. UE 2022/2065) — VLOP/VLOSE; DMA (Reg. UE 2022/1925) — gatekeeper; Data Act (Reg. UE 2023/2854) — portabilità, cloud switching
