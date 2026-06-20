# Master Map — Studio Attivo Universitario
**Aggiornato**: 2026-05-20 | **Sessione**: 24

> **Istruzione per l'AI**: Leggere questo file all'inizio di ogni sessione per riprendere il filo. Non assumere mai che i moduli "verificati" negli appunti GitHub siano stati interiorizzati, a meno che non compaiano come ✅ nel log di sessione qui sotto.

---

## Panoramica Corsi

| Corso | Stato Reale | Priorità | VM Richiesta |
|---|---|---|---|
| Lab Amministrazione di Sistemi T | 🔴 Da zero | Alta | Vagrant + Debian 12 |
| Lab Sicurezza Informatica T | 🟡 Concetti vaghissimi | Alta | Kali Linux / Parrot OS |
| Diritto dell'Informatica T | 🟡 Visto parzialmente (Gemini, non validato) | Media | — |

**Connessione critica**: SysAdmin è prerequisito implicito di Security. I due lab vengono studiati in parallelo e si rinforzano a vicenda. Diritto è indipendente e può essere parallelizzato.

---

## Setup VM (Prerequisito — da completare prima dei lab)

### VM SysAdmin — Vagrant + Debian 12
```bash
# Installare VirtualBox e Vagrant se non presenti
# Poi, da una directory di progetto:
mkdir sysadmin-lab && cd sysadmin-lab
vagrant init debian/bookworm64
vagrant up
vagrant ssh
```
**Stato setup**: 🔄 In corso (Sessione 2)

### VM Security — Kali Linux
- VirtualBox: aggiungere scheda di rete host-only `vboxnet0`
- Scaricare ISO Kali Linux da kali.org oppure usare Parrot OS
- Credenziali standard: `kali`/`kali` oppure `parrot`/`parrot`
- **Importante**: usare Snapshot prima di ogni esercizio di compromissione

**Stato setup**: ⬜ Non ancora eseguito

---

## Metodologia di Studio Attivo

Per i lab (SysAdmin e Security), ogni modulo segue questo schema:

1. **Leggi** il materiale Virtuale indicato (slide/PDF del corso)
2. **Esegui** i comandi sulla VM mentre leggi — mai solo lettura passiva
3. **Verifica** di saper spiegare il concetto chiave a parole tue
4. **Completa** l'esercizio del lab Virtuale corrispondente

Per Diritto: lettura + sintesi scritta dei punti normativi chiave.

---

## Percorso Modulare

I moduli sono ordinati per dipendenze logiche, non necessariamente per data delle lezioni. Il materiale Virtuale corrispondente è indicato per ogni modulo.

### Corrispondenza nomi Virtuale → file su disco (SysAdmin)

I titoli di Virtuale e i nomi file effettivi divergono. Tabella di riferimento per non cercare PDF inesistenti:

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
| PDF lab SysAdmin | `SLIDE LAB/SYSADM/__ LAB __ <titolo> _ Virtuale.pdf` (nomi invariati) |

### ── BLOCCO 0: Fondamenta Linux ──
*Prerequisito per tutto il resto. Da completare prima di qualsiasi lab.*

#### Modulo 0A — Filesystem e Comandi Base Linux
**Corso**: SysAdmin  
**Materiale Virtuale**:  
- Teoria: "Introduzione alla materia e informazioni pratiche [19 feb]"  
- Lab: "Predisposizione ambiente virtuale per le esercitazioni [17 feb]", "Accesso via SSH e creazione VM Vagrant [24 feb]", "Primi esercizi di accesso alla VM e gestione filesystem [24 feb]"  
**Concetti chiave**: struttura filesystem Linux (`/`, `/home`, `/etc`, `/var`), navigazione (`ls`, `cd`, `pwd`), visualizzazione file (`cat`, `less`, `head`, `tail`), permessi in lettura (`r`, `w`, `x`), differenza tra utente normale e root  
**Esercizio attivo**: Navigare il filesystem della VM Debian, creare una struttura di directory, leggere file di configurazione in `/etc`  
**Connessione Security**: Kali Linux ha lo stesso filesystem — questi comandi sono usati in ogni lab di Security  
**Stato**: ✅ Completato (Sessione 3 — 2026-04-16)

#### Modulo 0B — Pipe, Redirect e Filtri
**Corso**: SysAdmin  
**Materiale Virtuale**:  
- Teoria: "Shell, processi, espansione [5 marzo]"  
- Lab: "Primi esercizi sulla riga di comando [24 feb]"  
**Concetti chiave**: pipe (`|`), redirect (`>`, `>>`, `<`, `2>`, `2>&1`), filtri (`grep`, `sort`, `uniq`, `wc`, `cut`, `head`, `tail`)  
**Esercizio attivo**: Esercizi "Conta Occorrenze" base dalla VM — pipeline su file di testo, analisi `/etc/passwd`, monitoraggio log  
**Connessione Security**: `grep` e pipe usati massivamente per analisi di log, output di tool come Nmap  
**Stato**: ✅ Completato (Sessione 4 — 2026-04-16)

---

### ── TRACCIA ESERCIZI SCRIPTING ──
*Traccia parallela ai moduli — esercizi progressivi orientati all'esame. Due tipi:*
- ***lab_NN*** — esercizi risolti dal prof (PDF "Esercizi di scripting risolti"), da leggere → capire → eseguire → documentare
- ***es_NN*** — esercizi da costruire da zero (nostri + assegnamenti Virtuale)

*File in `esercizi/`. Approccio per lab_: leggi il codice, predici il comportamento, poi esegui. Non copiare passivamente.*

#### Catena A — ls ricorsivo
| ID | Titolo | Tipo | Concetti nuovi | Stato |
|----|--------|------|----------------|-------|
| lab_01 | ls ricorsivo (funzioni, subshell, cicli) | lab PDF p.4-5 | funzioni, subshell `( )`, `test -d`, `cd ..`, ricorsione | ⬜ |
| lab_02 | ls ricorsivo alternative (while, read, filtri) | lab PDF p.6-7 | `ls -l \| while read`, `awk`, `[[ =~ ]]`, `cd -`, symlink parsing | ⬜ |
| lab_03 | ls ricorsivo estensioni (elif, $@) | lab PDF p.8 | `$@`, loop su argomenti multipli | ⬜ |
| es_03 | estparam.sh | assegnamento | estende lab_03: conta file per estensione in albero parametrico | ⬜ |

#### Catena B — conversione e manipolazione del tempo
| ID | Titolo | Tipo | Concetti nuovi | Stato |
|----|--------|------|----------------|-------|
| lab_04 | conversione tempo (calendario → promemoria) | lab PDF p.9 | `date +%s`, `date -d`, `mktemp`, `while sleep`, `egrep` | ⬜ |
| lab_05 | pianificazione eventi (plan.sh + remind.sh) | lab PDF p.10 | `grep -q`, `grep -x`, `grep -qx`, parametri obbligatori | ⬜ |
| lab_06 | esecuzione con cron | lab PDF p.11 | `grep -Fvx` per dedup crontab, `crontab file` | ⬜ |
| lab_07 | esecuzione con at | lab PDF p.12 | `at -t`, `flock`, lock su file condiviso | ⬜ |
| es_04 | estensione risolti (rimozione eventi) | assegnamento | estende lab_05–07: gestire cancellazione eventi dal calendario | ⬜ |

#### Catena C — processi e segnali
| ID | Titolo | Tipo | Concetti nuovi | Stato |
|----|--------|------|----------------|-------|
| es_05 | waitfile (case, sleep, exit code) | assegnamento | `case` su $3, `sleep 1`, retry con contatore, exit code semantici | ⬜ |
| es_06 | parallenne.sh (processi paralleli) | assegnamento | `$!`, PID tracking, `/proc/PID/comm`, `trap`, log su file | ⬜ |
| es_07 | segnali girati (debug script rotto) | assegnamento | `trap`, subshell e variabili, `tail -f \| while read`, BASHPID vs $$ | ⬜ |
| es_08 | conta occorrenze avanzato (parallelo+segnali) | assegnamento — estende es_02 | `wc -l`, `head`/`tail` per dimezzare file, `wait`, `trap USR1`, file temporanei | ⬜ |

---

### ── BLOCCO 1: Bash Scripting ──
*Costruire automazione su Linux. Fondamenta per tutti i tool di security scripted.*

#### Modulo 1A — Variabili, Condizioni, Loop
**Corso**: SysAdmin  
**Materiale Virtuale**:  
- Teoria: "Shell, processi, espansione [5 marzo]"  
- Lab: "Shell scripting [10 marzo]"  
**Concetti chiave**: variabili (`VAR=valore`, `$VAR`), condizionali (`if/then/else/fi`), loop (`for`, `while`), argomenti script (`$1`, `$2`, `$#`)  
**Esercizio attivo**: Scrivere script che accetta argomenti, conta righe in file, itera su una lista  
**Connessione Security**: Ogni tool di automazione offensiva/difensiva è uno script — capire la struttura è essenziale  
**Stato**: ✅ Completato (Sessione 5 — 2026-04-17)

#### Modulo 1B — Funzioni, Case, Test
**Corso**: SysAdmin  
**Materiale Virtuale**:  
- Teoria: "Shell, processi, espansione [5 marzo]"  
- Lab: "Shell scripting [10 marzo]"  
**Concetti chiave**: funzioni (`function nome() {}`), costrutto `case`, test condizionali avanzati (`-f`, `-d`, `-z`, `-eq`), `exit codes`  
**Esercizio attivo**: "Estensione degli esercizi risolti" + "Estensioni parametrico" da Virtuale  
**Connessione Security**: Pattern usato in script di enumeration automatizzata  
**Stato**: ✅ Completato (Sessione 6 — 2026-04-21)

---

### ── BLOCCO 2: Utenti, Permessi e File ──
*Capire chi può fare cosa su Linux. Base concettuale per privilege escalation in Security.*

#### Modulo 2A — Gestione Utenti e Permessi
**Corso**: SysAdmin  
**Materiale Virtuale**:  
- Teoria: "Gestione di utenti e file [19 marzo]"  
- Lab: "Esempi di gestione utenti permessi e file [31 marzo]"  
**Concetti chiave**: `useradd`, `usermod`, `passwd`, `groups`, permessi `rwx` in dettaglio, `chmod` (ottale e simbolico), `chown`, `chgrp`, `sudo` e `/etc/sudoers`, `su`  
**Esercizio attivo**: Creare utenti sulla VM, assegnare permessi su file e directory, testare accessi con utenti diversi  
**Connessione Security**: Privilege escalation sfrutta misconfigurazioni di permessi e sudo — capire la norma è prerequisito per capire la violazione  
**Stato**: ✅ Completato (Sessione 7/8 — 2026-04-21/23)

#### Modulo 2C — Gestione File: find, tar, rsync, Backup
**Corso**: SysAdmin  
**Materiale Virtuale**:  
- Teoria: "Gestione di utenti e file [19 marzo]" (sezione comandi file, archiviazione, backup)  
- Lab: "Esempi di gestione utenti permessi e file [31 marzo]" (esercizi 3-6: dd, fuser/lsof, script find)  
**Concetti chiave**: `find` avanzato (`-mtime`, `-type`, `-exec`), `locate`, `tar` (creazione/estrazione), compressione (`gzip`/`bzip2`/`xz`), `rsync`, `dd`, `fuser`, `lsof`, strategie di backup (full/incremental)  
**Esercizio attivo**: Esercizi 3-6 del lab — prenotazione spazio con dd, file aperti, script copia flat, script copia con struttura  
**Stato**: ✅ Completato

#### Modulo 2B — LAB Utenti, Permessi e File
**Corso**: SysAdmin  
**Materiale Virtuale**:  
- Lab: "Esempi di gestione utenti permessi e file [31 marzo]" (esercizi 1-2: /etc/skel, directory collaborativa con SGID)  
**Esercizio attivo**: Esercizi 1 e 2 del lab — osservare `/etc/skel` + `/etc/default/useradd` + `/etc/login.defs`, poi creare utenti `maria`/`piero` con directory collaborativa SGID  
**Stato**: ✅ Completato

---

### ── BLOCCO 3: Servizi e Storage ──
*Capire come un server "gira" — cosa sono i demoni, come si gestiscono, dove risiedono i dati.*

#### Modulo 3A — Gestione Servizi con Systemd
**Corso**: SysAdmin  
**Materiale Virtuale**:  
- Teoria: "Gestione dei servizi [12 marzo]"  
- Lab: "Gestione dei servizi e monitoraggio [31 marzo]"  
**Concetti chiave**: `systemd`, `systemctl` (start/stop/enable/disable/status), unit file, log con `journalctl`, monitoraggio processi (`ps`, `top`, `htop`), `at`, `cron`, timer systemd, `rsyslog`  
**Esercizio attivo**: Lab — at, watchdog, nice execution, manipolazione crontab, configurazione rsyslog, logconfig, esame unit reali  
**Connessione Security**: I servizi esposti su una macchina sono la sua superficie d'attacco — enumeration di Security cerca esattamente questi  
**Stato**: ✅ Completato (Sessione 10 — 2026-04-24)

#### Modulo 3B — Gestione dei Pacchetti Software
**Corso**: SysAdmin  
**Materiale Virtuale**:  
- Teoria: "Gestione dei pacchetti software [26 feb]"  
**Concetti chiave**: `apt`, `dpkg`, repository, aggiornamenti di sistema, installazione/rimozione pacchetti  
**Esercizio attivo**: Installare, aggiornare, rimuovere pacchetti sulla VM Debian  
**Stato**: ✅ Completato (Sessione 13 — 2026-04-28) — `claudeAppunti/APPUNTI SYSADM/appunti_modulo3B_gestione_pacchetti.md`

#### Modulo 3C — Gestione dei Processi
**Corso**: SysAdmin  
**Materiale Virtuale**:  
- Teoria: "Shell, processi, espansione [5 marzo]" (sezione processi)  
- Lab: "Gestione di processi [17 marzo]"  
**Concetti chiave**: `ps`, `top`, `kill`, `jobs`, `fg`, `bg`, processi in foreground/background, segnali  
**Esercizio attivo**: Lab Virtuale — avviare processi, monitorarli, inviargli segnali  
**Stato**: ✅ Completato (Sessione 16 — 2026-04-29) — `claudeAppunti/APPUNTI SYSADM/appunti_modulo3C_gestione_processi.md`

---

### ── BLOCCO 3D: Networking e Vagrant Multi-Machine ──
*Networking di base e orchestrazione di ambienti multi-VM — prerequisito per i lab di security in rete.*

#### Modulo 3D — Networking di Base
**Corso**: SysAdmin  
**Materiale Virtuale**:  
- Teoria+Lab: `SLIDE TEORIA/SYSADM/net-config.pdf` (titolo Virtuale: "Networking di base [16 aprile]") + `servizi_base_rete.pdf` ("Servizi rete infrastrutturali")  
**Concetti chiave**: interfacce di rete, `ip addr`, `ping`, `ss`/`netstat`, routing di base, DNS, `/etc/hosts`, `/etc/resolv.conf`  
**Esercizio attivo**: Lab Virtuale — configurare e verificare la rete sulla VM Debian  
**Stato**: 🔄 Es. 1 (ip a, ip r) eseguito; Es. 2–6 (ping, ss, DNS, hosts, tcpdump) da eseguire — `claudeAppunti/APPUNTI SYSADM/appunti_modulo3D_networking_base.md`

#### Modulo 3E — Vagrant Multi-Machine e Configurazione Rete VM
**Corso**: SysAdmin  
**Materiale Virtuale**:  
- Lab: "Configurazione di un ambiente multi machine tramite Vagrant [21 apr]", "Configurazione della rete delle VM [21 apr]", "Struttura Vagrantfile e playbook [21 apr]"  
**Concetti chiave**: Vagrantfile multi-machine, reti host-only/bridged/NAT, provisioning con Ansible, struttura playbook  
**Esercizio attivo**: Creare ambiente multi-VM con Vagrantfile, configurare rete tra VM, provisionare con Ansible  
**Stato**: ⬜ Da fare

#### Modulo 3F — Automazione con Ansible
**Corso**: SysAdmin  
**Materiale Virtuale**: "LAB Automazione con Ansible [14 aprile]"  
**Concetti chiave**: inventory, playbook YAML, moduli Ansible, idempotenza, SSH-based execution  
**Esercizio attivo**: Lab Virtuale — configurare nodo Vagrant da host tramite playbook  
**Stato**: ⬜ Da fare

---

### ── Security — Lab Sicurezza Informatica T ──
*Appunti grezzi in: `APPUNTI GREZZI/Lab - Security/`*  
*VM richiesta: Kali Linux / Parrot OS — usare Snapshot prima di ogni esercizio di compromissione.*  
*PDF non ancora scaricati — richiedere il PDF corrispondente a Lorenzo prima di ogni modulo (sono disponibili su Virtuale).*

---
#### ─ Offensive Security ─

#### Modulo S1 — Principi Offensive Security + LAB Enumerazione
**Corso**: Security  
**Materiale Virtuale**:  
- Teoria: "Principi dell'offensive security [20 feb]"  
- LAB: "** LAB ** Enumerazione [25 feb]" — Slide: "Strumenti e metodi per l'enumerazione di host, servizi, e utenti"  
**Concetti chiave**: vulnerability assessment e penetration testing, fasi di un attacco (reconnaissance → exploitation → post-exploitation), `nmap` (scansione porte, versioni, OS), banner grabbing, enumerazione utenti  
**Esercizio attivo**: LAB su "Tre target combinati" — enumerare host, servizi e utenti  
**Connessione SysAdmin**: I servizi configurati in 3A sono esattamente ciò che Nmap trova qui  
**Stato**: 🔄 In corso — lezione pronta (`claudeLezioni/LEZIONI SECURITY/lezione_moduloS1_offensive_security_enumerazione.md`); lab VM non ancora eseguito

#### Modulo S2 — Autenticazione
**Corso**: Security  
**Materiale Virtuale**: "Autenticazione [27 feb]"  
**Concetti chiave**: metodi di autenticazione, robustezza delle credenziali contro l'enumerazione, meccanismi di brute force protection  
**Stato**: ⬜ Da fare

#### Modulo S3 — Web Security + LAB
**Corso**: Security  
**Materiale Virtuale**:  
- Teoria: "Web security [6 mar]" — OWASP Top Ten 2025  
- LAB: "**LAB** web security [11 mar]" — Web pentest Altoro Mutual, `pentestlab.sh`  
**Concetti chiave**: SQL injection, XSS (stored/reflected), CSRF, directory traversal, OWASP Top Ten 2025  
**Esercizio attivo**: `./pentestlab.sh start APP` — attaccare app vulnerabili già presenti su Parrot  
**Stato**: ⬜ Da fare

#### Modulo S4 — Binary Exploits + LAB Bruteforcing
**Corso**: Security  
**Materiale Virtuale**:  
- Teoria: "Binary exploits [13 mar]" — stack overflow, ret2libc/ret2syscall, ROP, contromisure  
- LAB: "** LAB ** bruteforcing e buffer overflows [18 mar]" — `tar xzf pwn_lab.tgz`; esercizi: riscrivere variabile, funzione nascosta, buffer overflow con shellcode, [facoltativo] return to libc  
**Concetti chiave**: stack overflow, shellcode, return-oriented programming, contromisure (canary, NX, ASLR)  
**Nota**: esercizi su binari x86_32 — non compatibili con Apple Silicon senza emulatore  
**Stato**: ⬜ Da fare

---
#### ─ Controllo dell'Accesso e Hardening ─

#### Modulo S5 — Firewall: Teoria + Configurazione + LAB
**Corso**: Security  
**Materiale Virtuale**:  
- Teoria: "Firewall [20 mar]" — tipologie firewall, architettura packet filter Linux  
- Teoria: "Configurazione del packet filter di Linux [1 apr]"  
- LAB: "** LAB ** Firewall [1 apr]"  
**Concetti chiave**: `iptables`/`nftables`, catene INPUT/OUTPUT/FORWARD, politiche di default, regole allow/deny, stateful firewall  
**Esercizio attivo**: Configurare firewall su VM, testare regole  
**Stato**: ⬜ Da fare

#### Modulo S6 — Sicurezza Fisica e Cloud
**Corso**: Security  
**Materiale Virtuale**: "Sicurezza fisica e collocazione in cloud [10 apr]"  
**Concetti chiave**: attacchi fisici ai computer, sicurezza processo di avvio, sicurezza software installato, supply chain attacks ai tempi degli LLM, collocazione in cloud (vantaggi e rischi), esfiltrazione/iniezione attraverso fenomeni fisici (air gap jumping, iniezione comandi agli home assistant)  
**Stato**: ⬜ Da fare

#### Modulo S7 — LAB Backdoor Injection
**Corso**: Security  
**Materiale Virtuale**: "** LAB ** Backdoor injection [15 apr]"  
**Concetti chiave**: persistenza post-exploitation, backdoor su sistema compromesso  
**Nota**: Usare Snapshot VM prima dell'esercizio  
**Stato**: ⬜ Da fare

#### Modulo S8 — LAB Individuare e Filtrare Attacchi
**Corso**: Security  
**Materiale Virtuale**: "** LAB ** Individuare e filtrare attacchi [15 apr]"  
**Esercizio attivo**: Esercitazione di riepilogo — dall'enumerazione alla mitigazione di attacchi pwn e web  
**Stato**: ⬜ Da fare

#### Modulo S9 — Demoni di Sistema + Autorizzazione
**Corso**: Security  
**Materiale Virtuale**:  
- Teoria: "Demoni di sistema [17 apr]"  
- Teoria: "Autorizzazione [17 apr]" — metodi di autenticazione attivi e a più fattori, modelli di controllo dell'accesso, DAC in Linux e Windows, cenni su MAC e RBAC  
- [approfondimento] "PAM - il framework di autenticazione e autorizzazione di Linux"  
**Concetti chiave**: DAC, MAC, RBAC, implementazioni Linux (permessi, ACL, SELinux), autenticazione multifattore  
**Stato**: ⬜ Da fare

---
#### ─ Rilevazione delle Intrusioni ─

#### Modulo S10 — Rilevare gli Attacchi + LAB NIDS Suricata
**Corso**: Security  
**Materiale Virtuale**:  
- Teoria: "Rilevare gli attacchi [8 apr]" — IDS, IPS, NIDS, HIDS, EDR, SIEM, Suricata  
- LAB: "** LAB ** network intrusion detection [8 apr]" + Slide esempi utilizzo Suricata + Documentazione Suricata v7  
**Concetti chiave**: IDS vs IPS, signature-based vs anomaly-based detection, regole Suricata, EVE JSON log format  
**Esercizio attivo**: Installare Suricata, configurare regole, generare traffico da Kali e osservare alert  
**Stato**: ⬜ Da fare

#### Modulo S11 — Host-Based IDS + LAB Misconfiguration
**Corso**: Security  
**Materiale Virtuale**:  
- Teoria: "Host-Based Intrusion Detection [17 apr]"  
- LAB: "** LAB ** Esempi di misconfiguration [22 apr]"  
- LAB: "** LAB ** Misconfiguration attacks e HIDS [22 apr]"  
**Concetti chiave**: HIDS, rilevamento misconfigurazioni, privilege escalation alternativa  
**Stato**: ⬜ Da fare

---
#### ─ Network Security ─

#### Modulo S12 — Sicurezza delle Comunicazioni
**Corso**: Security  
**Materiale Virtuale**: "Sicurezza delle comunicazioni [23 apr]"  
**Concetti chiave**: richiami di reti, minacce ai diversi livelli dello stack protocollare  
**Stato**: ⬜ Da fare

---

### ── BLOCCO 9: Diritto dell'Informatica T ──
*Indipendente dagli altri corsi. Può essere parallelizzato in qualsiasi momento.*  
*Metodologia: lettura PDF → lezione strutturata → sintesi scritta. Nessuna VM richiesta.*  
*Normative di riferimento in `SLIDE TEORIA/DIRITTO INFORMATICO/NORMATIVE/` — citate inline nelle lezioni, non studiate come moduli autonomi.*

**Livello reale accertato (2026-04-23)**: materiale visto parzialmente tramite appunti Gemini (PDF 01–03, 07 probabilmente). Nessun modulo validato in sessione — tutti partono da ⬜.

#### Modulo D1 — Concetti Giuridici di Base
**Corso**: Diritto dell'Informatica T  
**PDF**: `01_DirInfo_2026_ConcettiBase_DEF.pdf`  
**Concetti chiave**: fonti del diritto, gerarchia normativa, soggetti giuridici, persona fisica/giuridica, obbligazione, responsabilità civile e penale, concetti di base per leggere una norma  
**Stato**: ✅ Completato (Sessione 11 — 2026-04-27) — `claudeAppunti/APPUNTI DIRITTO/appunti_moduloD1_concetti_giuridici_base.md`

#### Modulo D2 — Ricerca e Analisi delle Fonti del Diritto
**Corso**: Diritto dell'Informatica T  
**PDF**: `02_DirInfo_2026_RicercaFonti_DEF.pdf`  
**Concetti chiave**: come trovare e leggere una norma, banche dati giuridiche, struttura di leggi e decreti, interpretazione normativa  
**Stato**: ✅ Completato (Sessione 12 — 2026-04-27) — `claudeAppunti/APPUNTI DIRITTO/appunti_moduloD2_ricerca_fonti_diritto.md`

#### Modulo D3 — Diritto d'Autore e Tutela Giuridica del Software
**Corso**: Diritto dell'Informatica T  
**PDF**: `03_DirInfo_2026_IPR_DEF.pdf`  
**Concetti chiave**: diritto d'autore (L. 633/1941), opere dell'ingegno, tutela del software come opera dell'ingegno, diritti morali e patrimoniali, licenze, open source vs proprietario  
**Stato**: ✅ Completato (Sessione 16 — 2026-04-29) — `claudeAppunti/APPUNTI DIRITTO/appunti_moduloD3_diritto_autore.md`

#### Modulo D4 — Tutela Giuridica delle Banche Dati e Siti Web
**Corso**: Diritto dell'Informatica T  
**PDF**: `04_DirInfo_2025_BancheDatiSitiWeb_DEF.pdf`  
**Concetti chiave**: tutela delle banche dati (D.Lgs. 196/1999), diritto sui generis, siti web come opere, responsabilità dell'hosting provider  
**Stato**: ✅ Completato (Sessione 21 — 2026-05-13) — `claudeAppunti/APPUNTI DIRITTO/appunti_moduloD4_banche_dati_siti_web.md`

#### Modulo D5 — Contratti a Oggetto Informatico
**Corso**: Diritto dell'Informatica T  
**PDF**: `05_DirInfo_2026_ContrInformatici_DEF.pdf`  
**Concetti chiave**: tipologie di contratto informatico, licenza d'uso, contratto di sviluppo software, SLA, outsourcing, contratto cloud  
**Stato**: ✅ Completato (Sessione 22 — 2026-05-14) — `claudeAppunti/APPUNTI DIRITTO/appunti_moduloD5_contratti_informatici.md`

#### Modulo D6 — Analisi di un Contratto di Sviluppo Software
**Corso**: Diritto dell'Informatica T  
**PDF**: `06_DirInfo_2026_SchemaContratt_DEF.pdf`  
**Concetti chiave**: lettura guidata di un contratto reale, clausole fondamentali, garanzie, penali, proprietà intellettuale nel contratto, foro competente  
**Stato**: ✅ Completato (Sessione 24 — 2026-05-20) — `claudeAppunti/APPUNTI DIRITTO/appunti_moduloD6_contratto_sviluppo_software.md`

#### Modulo D7 — La Proprietà Industriale
**Corso**: Diritto dell'Informatica T  
**PDF**: `07_DirInfo_2026_ProprietàIndustriale.pdf`  
**Normativa di riferimento**: `decreto-legislativo-10-02-2005-n-30.pdf` (Codice della Proprietà Industriale)  
**Concetti chiave**: brevetti, marchi, segreti industriali, tutela dell'invenzione software, differenza brevetto vs diritto d'autore  
**Stato**: ✅ Completato (Sessione 25 — 2026-05-21) — `claudeAppunti/APPUNTI DIRITTO/appunti_moduloD7_proprieta_industriale.md`

#### Modulo D8 — Privacy e Protezione dei Dati Personali
**Corso**: Diritto dell'Informatica T  
**PDF**: `08_DirInfo_2026_Privacy_DEF.pdf`  
**Normative di riferimento**: GDPR (Reg. UE 2016/679), Codice Privacy (D.Lgs. 196/2003 s.m.i.)  
**Concetti chiave**: principi del trattamento (art. 5 GDPR), basi giuridiche (art. 6), diritti degli interessati (artt. 15-22), titolare/responsabile, DPO, DPIA, notifica violazioni, adattamento italiano  
**Stato**: ⬜ Da fare

#### Modulo D9 — Firme Elettroniche
**Corso**: Diritto dell'Informatica T  
**PDF**: `09_DirInfo_2026_FirmeElettr_DEF.pdf`  
**Concetti chiave**: firma elettronica semplice/avanzata/qualificata, firma digitale, eIDAS (Reg. UE 910/2014), valore probatorio, certificati qualificati, TSP  
**Stato**: ⬜ Da fare

#### Modulo D10 — Commercio Elettronico
**Corso**: Diritto dell'Informatica T  
**PDF**: `10_DirInfo_2026_CommercioElettronico_DEF.pdf`  
**Concetti chiave**: D.Lgs. 70/2003 (recepimento Dir. 2000/31/CE), contratti online, obblighi informativi del prestatore, responsabilità degli intermediari, country of origin principle  
**Stato**: ⬜ Da fare

#### Modulo D11 — Reati Informatici
**Corso**: Diritto dell'Informatica T  
**PDF**: `11_DirInfo_2026_ReatiInformatici_DEF.pdf`  
**Concetti chiave**: accesso abusivo a sistema informatico (art. 615-ter c.p.), danneggiamento informatico, frode informatica, intercettazione illecita, Convenzione di Budapest, responsabilità penale  
**Stato**: ⬜ Da fare

---

## Log di Sessione

### Sessione 25 — 2026-05-21 (in corso)
**Focus**: Diritto D7 — Appunti definitivi Proprietà Industriale

**Coperto in sessione**:
- Appunti modulo D7 elaborati → `claudeAppunti/APPUNTI DIRITTO/appunti_moduloD7_proprieta_industriale.md`
  - Struttura a domande come titoli (su richiesta di Lorenzo) — ogni sezione risponde a una domanda reale
  - 20+ domande aperte risolte: indicazioni geografiche/DOP, esaurimento diritti e sue eccezioni, rappresentabilità nel registro, schema comparativo 6 casi di novità marchio, legame caso f) con e), eccezione preutente, esempio marchio che acquista capacità distintiva per uso, volgarizzazione (Domopak vs Cellofan), "in quanto tale" software approfondito con esempi, stato della tecnica e common knowledge, esperto del ramo e attività inventiva, finzione di invenzione durante il rapporto, effetti brevetto di procedimento e casi di presunzione, schema tempistiche mantenimento brevetto, tabella 3 casi invenzione dipendenti schematizzata, correttezza professionale nelle limitazioni al marchio con esempi (nome proprio, indicazioni descrittive, accessori/ricambi), unitarietà dei segni in cosa è unica rispetto alle regole già viste, trasferimento parziale del marchio spiegato
  - Domanda di autoverifica 1 completa (non era negli appunti grezzi)
  - Domande 2-5 corrette e integrate con precisazioni
  - Sezioni integrate dalla lezione: §2.14 nomi a dominio, §3.3 divulgazioni non opponibili, §3.4 priorità, §3.8 rivendicazioni, riepilogo comparativo marchio/brevetto

**Prossima sessione — da dove partire**:
→ **Diritto D8** — Privacy e GDPR (`08_DirInfo_2026_Privacy_DEF.pdf` presente)
→ **SysAdmin 3D Es. 2–6** — invariato
→ **Security S1 LAB** — invariato

---

### Sessione 24 — 2026-05-20 (completata)
**Focus**: Diritto D6 — Autoverifica (5 domande in modalità interrogazione)

**Coperto in sessione**:
- Autoverifica D6 completata: 5 domande una alla volta in modalità interrogazione
- Punti forti: distinzione opera intellettuale/appalto, art. 2231 (non iscrizione + cancellazione), differenza variazioni richieste/necessarie, cessione vs licenza
- Punti da ripassare: art. 2224 (variazioni necessarie — nome articolo non ricordato), meccanica art. 1457 (termine essenziale), effetto retroattivo art. 1458 e sua eccezione per esecuzione continuata

**Non coperto / da riprendere**:
- SysAdmin 3D Es. 2–6 — invariato
- Security S1 LAB — invariato

**Prossima sessione — da dove partire**:
→ **Diritto D7** — Proprietà Industriale (`07_DirInfo_2026_ProprietàIndustriale.pdf`) — eseguire `/lezione D7`
→ **SysAdmin 3D Es. 2–6** — avviare VM, eseguire: `ping`, `ss -tlnp`, `/etc/hosts`, `dig`, `tcpdump`. Poi `/appunti 3D`
→ **Security S1 LAB** — lezione pronta, eseguire le 6 sezioni sulla VM Kali

---

### Sessione 23 — 2026-05-15 (completata)
**Focus**: Diritto D6 — Contratto di sviluppo software

**Coperto in sessione**:
- Aggiornata master map: aggiunti moduli D9 (Firme Elettroniche), D10 (Commercio Elettronico), D11 (Reati Informatici) — PDF caricati da Lorenzo
- Diritto ora 11 moduli (non 8); ESAMI SCELTI.md aggiornato (~54h stima)
- Letto PDF D6 (52 slide); creata lezione D6 → `claudeLezioni/LEZIONI DIRITTO/lezione_moduloD6_contratto_sviluppo_software.md`
- Appunti grezzi D6 elaborati → `claudeAppunti/APPUNTI DIRITTO/appunti_moduloD6_contratto_sviluppo_software.md`
  - 19 domande aperte risolte (differenza opera/opera intellettuale, determinabilità oggetto, ruolo artt. 2229/2230/2231, albo ingegneri, obblighi committente, terzi nell'indennizzo, difformità vs vizi, art. 2226 spiegato, decadenza/prescrizione, software terzi, art. 2228 vs variazioni necessarie, secondo punto titolarità DPI, licenza vs cessione, processo di verifica, saldo finale, servizi aggiuntivi, tabella risoluzione, legge applicabile/foro, dati personali/GDPR)
  - 2 imprecisioni corrette: dati personali (non sono quelli dell'ingegnere ma di terzi negli archivi del committente); variazioni richieste/necessarie (non fuse — sono concetti distinti)
  - 2 sezioni integrate: artt. 1176/2236 (diligenza professionale, responsabilità per problemi di speciale difficoltà); nota "Attenzione ripasso" con domande d'esame segnalate dalla prof
  - Domande di autoverifica: 5 domande presenti — da rispondere in autonomia durante lo studio

**Non coperto / da riprendere**:
- Autoverifica D6 — da completare leggendo gli appunti
- SysAdmin 3D Es. 2–6 — invariato
- Security S1 LAB — invariato

**Prossima sessione — da dove partire**:
→ **Diritto D7** — Proprietà Industriale (`07_DirInfo_2026_ProprietàIndustriale.pdf`) — eseguire `/lezione D7`
→ **SysAdmin 3D Es. 2–6** — avviare VM, eseguire: `ping`, `ss -tlnp`, `/etc/hosts`, `dig`, `tcpdump`. Poi `/appunti 3D`
→ **Security S1 LAB** — lezione pronta, eseguire le 6 sezioni sulla VM Kali

---

### Sessione 22 — 2026-05-14 (completata)
**Focus**: Diritto D5 — Contratti a oggetto informatico

**Coperto in sessione**:
- Appunti grezzi D5 scritti da Lorenzo dalla lezione → elaborati in `claudeAppunti/APPUNTI DIRITTO/appunti_moduloD5_contratti_informatici.md`
  - 18 domande aperte risolte (conclusione del contratto, inizio dell'esecuzione, moduli/formulari, legislatore/Codice consumo, clausole escluse da vessatorietà, illegalità clausole vessatorie, locazione e licenza, clausole esclusione garanzia, shrink-wrap e doppia firma, negozio giuridico, copyleft con esempio, CCPlus/CC0/brevetti/garanzia/diritti terzi, qualificazione contratto sviluppo, d'opera intellettuale spiegazione completa, manutenzione e clausole licenza, escrow codice sorgente, nullità parziale con esempi)
  - 1 imprecisione corretta: risposta autoverifica 5 — CC BY ≠ pubblico dominio; CC0 = pubblico dominio con rinuncia totale inclusa attribuzione
  - 2 sezioni integrate: requisiti del contratto (§2, causa/motivi); contratto d'opera intellettuale completo (§18)
  - Domande di autoverifica: 5/5 risposte presenti negli appunti grezzi (alcune incomplete, tutte integrate)

**Non coperto / da riprendere**:
- SysAdmin 3D Es. 2–6 — invariato
- Security S1 LAB — invariato

**Prossima sessione — da dove partire**:
→ **Diritto D6** — Analisi di un contratto di sviluppo software (`06_DirInfo_2026_SchemaContratt_DEF.pdf`) — eseguire `/lezione D6`
→ **SysAdmin 3D Es. 2–6** — avviare VM, eseguire: `ping`, `ss -tlnp`, `/etc/hosts`, `dig`, `tcpdump`. Poi `/appunti 3D`
→ **Security S1 LAB** — lezione pronta, eseguire le 6 sezioni sulla VM Kali

---

### Sessione 21 — 2026-05-13 (completata)
**Focus**: Diritto D4 — Tutela giuridica delle banche di dati e siti web

**Coperto in sessione**:
- Letto PDF `04_DirInfo_2025_BancheDatiSitiWeb_DEF.pdf` (29 slide)
- Creata lezione D4 → `claudeLezioni/LEZIONI DIRITTO/lezione_moduloD4_banche_dati_siti_web.md`
- Appunti modulo D4 elaborati → `claudeAppunti/APPUNTI DIRITTO/appunti_moduloD4_banche_dati_siti_web.md`
  - 11 domande aperte risolte (diritto sui generis solo per BD, distinzione LDA/DA, diritto connesso, "stabilito nell'UE", esempi parti non sostanziali sistematiche, impregiudicati diritti sul contenuto, recap regola dipendente, utente legittimo ≠ autore, esempi contratti, casi e scenari a cosa servono)
  - 2 imprecisioni corrette (definizione BD: mancava "o metodicamente"; BD non selettiva: frase incompleta)
  - 2 sezioni integrate: diritti esclusivi dell'autore, sito web come opera (con tabella giurisprudenza)
  - Domande di autoverifica: completate ✅ (5/5 risposte con correzioni integrate)
- Creata lezione D5 → `claudeLezioni/LEZIONI DIRITTO/lezione_moduloD5_contratti_informatici.md`

---

### Sessione 20 — 2026-05-12 (completata)
**Focus**: SysAdmin — Esercizio 02 bash scripting (testo libero)

**Coperto in sessione**:
- Esercizio 02: script `conta_occorrenze.sh` che accetta un file come `$1` e stampa:
  1. Occorrenze della lettera `a` → `grep -o 'a' "$1" | wc -l` → **34377**
  2. Occorrenze di `sherlock` case insensitive → `grep -oi 'sherlock' "$1" | wc -l` → **99**
  3. Top 5 parole per frequenza → `tr '[:upper:]' '[:lower:]' < "$1" | tr -cs '[:alpha:]' '\n' | sort | uniq -c | sort -rn | head -5`
- Esplorazione sistematica dei flag di `grep`: differenza tra contare righe (senza `-o`) e contare occorrenze (con `-o`); comportamento di `-c`, `-n`, `-v`, `-i`, `-o` testati sul file reale
- Introdotto `tr`: flag `-c`, `-s`, `-d`; classi POSIX `[:alpha:]`, `[:upper:]`, `[:lower:]`; pattern "una parola per riga" con `tr -cs '[:alpha:]' '\n'`
- Ragionamento su lowercase prima della tokenizzazione (ordine dei passi nella pipeline)
- Creato `esercizi/es_02_conta_occorrenze.md` con script, tabella flag grep, spiegazione passo per passo e tutti i ragionamenti intermedi
- Cheatsheet aggiornato: `grep` con descrizioni precise dei flag; voce `tr` aggiunta con flag e classi POSIX
- Trasferimento file host → VM tramite cartella condivisa Vagrant (`/vagrant/`)

**Non coperto / da riprendere**:
- SysAdmin 3D Es. 2–6 (ping, ss, DNS, hosts, tcpdump) — invariato
- Diritto D4 — invariato
- Security S1 LAB — invariato

**Prossima sessione — da dove partire**:
→ **SysAdmin 3D Es. 2–6** — avviare VM, eseguire: `ping`, `ss -tlnp`, `/etc/hosts`, `dig`, `tcpdump`. Poi `/appunti 3D`
→ **Diritto D4** — `04_DirInfo_2025_BancheDatiSitiWeb_DEF.pdf` già presente, eseguire `/lezione D4`
→ **Security S1 LAB** — lezione pronta, eseguire le 6 sezioni sulla VM Kali

---

### Sessione 19 — 2026-05-11 (completata)
**Focus**: SysAdmin — ripasso 0B (pipeline esercizio) + strumenti studio

**Coperto in sessione**:
- Esercizio pipeline: conta file per estensione, top 5 — costruito passo per passo sulla VM
  - Pipeline completa: `ls -R 2>/dev/null | grep -v ':$' | grep -v '^$' | grep '\.' | rev | cut -d'.' -f1 | rev | sort | uniq -c | sort -rn | head -5`
  - Spiegati: `ls -R` in modalità pipe (un file per riga), filtro intestazioni con `:$`, filtro righe vuote con `^$`, punto letterale `\.` vs punto regex `.`, trucco `rev|cut|rev` per ultimo campo, doppio uso di `sort` (raggruppare per `uniq` + ordinare per frequenza), flag `-n`/`-r`/`-rn` di `sort`
- Cheatsheet `cheatsheet_sysadm.html` aggiornato:
  - `ls`: aggiunto flag `-R` con nota sul comportamento piped
  - `sort`: aggiunti flag `-n`, `-r`, `-rn` + nota sul rapporto con `uniq`
  - `grep`: aggiunta sottotabella regex anchors (`^`, `$`, `^$`, `.`, `\.`)
  - `rev`: voce nuova con trucco `rev|cut|rev`
  - `cut`: aggiornata descrizione
- Creata directory `esercizi/` con `es_01_conta_estensioni.md` — documentazione completa passo per passo

**Non coperto / da riprendere**:
- SysAdmin 3D Es. 2–6 (ping, ss, DNS, hosts, tcpdump) — nessun lavoro sulla VM oggi
- Diritto e Security: invariati

**Prossima sessione — da dove partire**:
→ **SysAdmin 3D Es. 2–6** — avviare VM, eseguire: `ping`, `ss -tlnp`, `/etc/hosts`, `dig`, `tcpdump`. Poi `/appunti 3D`
→ **Diritto D4** — `04_DirInfo_2025_BancheDatiSitiWeb_DEF.pdf` già presente, eseguire `/lezione D4`
→ **Security S1 LAB** — dopo 3D, tornare agli appunti grezzi S1 (`/appunti S1`)

---

### Sessione 18 — 2026-05-06 (in corso)
**Focus**: SysAdmin 3D (lezione) + Security S1 (analisi appunti grezzi)

**Coperto in sessione**:
- Analisi appunti grezzi S1: Lorenzo ha eseguito `ip a` su Parrot ma non ha trovato le ISO dei target; domande aperte su lo, porte, TCP, Nmap — tutte riconducibili a lacune di networking di base
- Decisione: fare 3D SysAdmin (networking) prima di tornare agli appunti S1
- Letti `net-config.pdf` e `servizi_base_rete.pdf`
- Creata `claudeLezioni/LEZIONI SYSADM/lezione_modulo3D_networking_base.md`
  - Contenuto: modello Internet/IP, CIDR/netmask, ARP, porte e servizi, three-way handshake TCP, NAT/SNAT/DNAT, tipi di interfaccia VirtualBox (NAT/Host-only/Internal/Bridged), `ip a`/`ip r`, `ping`/`ss`/`traceroute`/`tcpdump`, DNS e NSS
  - 6 esercizi guidati sulla VM (lo interfaccia, ping, ss, DNS, /etc/hosts, tcpdump)
  - Connessione esplicita con Security S1 (Nmap, superficie d'attacco, three-way handshake)
- Nota: PDF lab "Networking di base [16 aprile]" non presente — esercizi costruiti dalla teoria

**Coperto in sessione (aggiornamento)**:
- Appunti 3D elaborati → `claudeAppunti/APPUNTI SYSADM/appunti_modulo3D_networking_base.md`
  - 20+ domande aperte risolte: router vs gateway, ARP e pacchetti, host-id vs MAC, netmask/CIDR con output reale VM, subnet, IP privati, NAT vs MAC, three-way handshake, ip a/ip r riga per riga, IPv6 link-local vs global
  - Es. 1 (ip a, ip r) eseguito ✅; Es. 2–6 (ping, ss, DNS, hosts, tcpdump) ancora da eseguire ⬜

**Prossima sessione — da dove partire**:
→ **SysAdmin 3D Es. 2–6** — leggere le risposte nelle domande aperte degli appunti, poi eseguire sulla VM: `ping`, `ss -tlnp`, DNS (`/etc/hosts`, `dig`), alias hosts, tcpdump. Poi `/appunti 3D` per integrare.
→ **Security S1 appunti** — dopo aver completato 3D, tornare agli appunti grezzi S1 (`/appunti S1`)
→ **Diritto D4** — `04_DirInfo_2025_BancheDatiSitiWeb_DEF.pdf` già presente, eseguire `/lezione D4`

---

### Sessione 17 — 2026-05-04 (completata)
**Focus**: Security S1 — lezione creata

**Coperto in sessione**:
- Letti tutti i PDF Security S1: `05_05__va_pt.pdf` (53 pp.), `__ LAB __ Enumerazione [25 febbraio]_.pdf` (10 pp.), `Istruzioni per la configurazione delle VM_.pdf` (7 pp.), `02_03__lab-intro-2026.pdf` (pp. 1-40)
- Creata `claudeLezioni/LEZIONI SECURITY/lezione_moduloS1_offensive_security_enumerazione.md`
- Contenuto: setup VM (VirtualBox, snapshot, rete, credenziali), teoria (VA/PT, kill chain, MITRE ATT&CK, OSINT, DNS enumeration, subdomain enum, IP blocks, host/service enumeration, evasion, Nessus/OpenVAS), lab completo (6 sezioni, dalla predisposizione dei target all'hash cracking)

**Prossima sessione — da dove partire**:
→ **Security S1 LAB** — eseguire la VM e svolgere le 6 sezioni del lab Enumerazione

---

### Sessione 16 — 2026-04-29 (completata)
**Focus**: SysAdmin 3C (pratica VM + appunti) + Diritto D3 (appunti)

**Coperto in sessione**:
- Es. 1–5 eseguiti sulla VM Debian — modulo 3C completato
- Appunti 3C elaborati → `claudeAppunti/APPUNTI SYSADM/appunti_modulo3C_gestione_processi.md`
- 25 domande risolte su processi (fork/exec, segnali, nohup, disown, ecc.)
- Es. 5: script `conta_file.sh` scritto, debuggato (4 bug corretti) ed eseguito con successo
- Fix permanente TERM: `export TERM=xterm-256color` aggiunto a `~/.bashrc` della VM
- Appunti D3 elaborati → `claudeAppunti/APPUNTI DIRITTO/appunti_moduloD3_diritto_autore.md`
  - 8 domande aperte risolte (esteriorizzazione, esaurimento comunitario, diritti connessi, piattaforme online, ecc.)
  - 3 imprecisioni giuridiche corrette (morali imprescrittibili ≠ 70 anni; forma espressiva ≠ funzione; dipendente: mansioni OR istruzioni)
  - 4 sezioni integrate: eccezioni/limitazioni generali, diritti connessi, sanzioni penali in dettaglio, PA durata 20 anni
  - Domande di autoverifica: tutte e 5 risposte (domanda 3 non era negli appunti grezzi — risposta costruita)

**Prossima sessione — da dove partire**:
→ **SysAdmin 3D** — Networking di Base (nuovo modulo — richiedere PDF lab "Networking di base [16 aprile]" da Virtuale, poi `/lezione 3D`)
→ **Diritto D4** — Tutela Banche Dati e Siti Web (`04_DirInfo_2025_BancheDatiSitiWeb_DEF.pdf` già presente)
→ **Security S1** — richiedere PDF da Virtuale prima di iniziare

---

### Sessione 15 — 2026-04-29 (completata)
**Focus**: Organizzazione — pianificazione esami e aggiornamento strumenti

**Coperto in sessione**:
- Analisi date appelli disponibili per tutti e tre i corsi (da file ESAMI.md)
- Scelta date esami: Diritto 16/06, SysAdmin 22/06, Security 17/07
- Stima ore per modulo per ciascuna materia (~181h totali su 435h disponibili)
- Creato `ESAMI SCELTI.md` con date, piano settimanale per fasi e analisi rischi
- Creata skill `/piano` (`.claude/commands/piano.md`)
- Integrato piano del giorno come passo 6 in `/sessione`
- Aggiornato `CLAUDE.md` con blocco scadenze esami e piano orario per fase

**Non coperto / da riprendere**:
- Nessun modulo studiato — sessione puramente organizzativa

**Prossima sessione — da dove partire**:
→ `/sessione` per il piano del giorno aggiornato
→ **SysAdmin 3C** — pratica VM (lezione già pronta in `claudeLezioni/LEZIONI SYSADM/lezione_modulo3C_gestione_processi.md`)
→ **Diritto D3** — appunti grezzi (lezione già pronta in `claudeLezioni/LEZIONI DIRITTO/lezione_moduloD3_diritto_autore.md`)
→ **Security S1** — richiedere PDF da Virtuale prima di iniziare

---

### Sessione 14 — 2026-04-28 (completata)
**Focus**: SysAdmin — Modulo 3C (lezione creata)

**Coperto in sessione**:
- Lezione 3C creata da PDF teoria (slide 23–32) e lab → `claudeLezioni/LEZIONI SYSADM/lezione_modulo3C_gestione_processi.md`
- Concetti coperti: PID/Job ID, fork/exec, background (&, $!), segnali e signal disposition, kill, trap, ps, jobs, fg, bg, watch, wait, nohup, disown, nice, array bash con PID, mktemp

**Prossima sessione — da dove partire**:
→ **Modulo 3C — Pratica VM**: avviare la VM, eseguire Es. 1–5 dalla lezione nell'ordine indicato. Poi scrivere appunti grezzi → `/appunti 3C`

---

### Sessione 13 — 2026-04-28 (completata)
**Focus**: SysAdmin — Modulo 3B (pratica VM + appunti)

**Coperto in sessione**:
- Lezione 3B già creata in sessione precedente
- Es. 1–7 eseguiti sulla VM Debian (tutti completati)
- Appunti elaborati → `claudeAppunti/APPUNTI SYSADM/appunti_modulo3B_gestione_pacchetti.md`
- 14 domande aperte risolte (redirect `2>/dev/null`, `wc -l`, `dpkg -L`, `apt search`, librerie dinamiche vs statiche, `sources.list`, `apt-cache showpkg`, `dpkg -S`)
- 3 sezioni integrate dalla lezione: software injection, problematiche aggiornamento, Snap/Flatpak/Container
- Chiariti a fine sessione: catena di fiducia ISO → keyring → verifica pacchetti; doppia whitelist `sources.list` + `trusted.gpg.d`

**Non coperto / da riprendere**:
- Nessun blocco aperto

**Prossima sessione — da dove partire**:
→ **Modulo 3C** — Lezione già creata. Avviare VM e seguire gli esercizi guidati.

---

### Sessione 12 — 2026-04-27 (completata)
**Focus**: Diritto — D2 (lezione + appunti) + D3 (lezione) + assessment generale

**Coperto in sessione**:
- Lezione D2 creata da PDF; appunti grezzi elaborati → `claudeAppunti/APPUNTI DIRITTO/appunti_moduloD2_ricerca_fonti_diritto.md`
- Domande di autoverifica D2 completate in autonomia da Lorenzo → D2 ✅
- Lezione D3 creata da PDF (95 slide) → `claudeLezioni/LEZIONI DIRITTO/lezione_moduloD3_diritto_autore.md`
- Glossario diritto creato come file separato `glossario_diritto.md`; glossario SysAdmin rinominato `glossario_sysadm.md`
- Assessment generale: situazione esami giugno-luglio, piano di studio (blocco lab + contorno Diritto)

**Non coperto / da riprendere**:
- D3: Lorenzo non ha ancora letto la lezione né scritto gli appunti grezzi

**Prossima sessione — da dove partire**:
→ **Diritto (contorno)**: leggere `lezione_moduloD3_diritto_autore.md`, scrivere appunti grezzi, poi `/appunti D3`
→ **SysAdmin (blocco principale)**: riprendere da 3B (pacchetti apt) → 3C (processi) → 3D (networking)

---

### Sessione 11 — 2026-04-27 (completata)
**Focus**: Diritto — Modulo D1 (elaborazione appunti grezzi)

**Completato**:
- Appunti modulo D1 elaborati → `claudeAppunti/APPUNTI DIRITTO/appunti_moduloD1_concetti_giuridici_base.md`
- 2 domande aperte risolte (fonti obbligazioni, sentenza vs norma)
- 5 imprecisioni giuridiche corrette (Regolamenti UE applicabilità diretta, Direttive vincolanti non "ideali", Regolamenti come fonte pubblica non privata, analogia come divieto non insufficienza, parti del contratto ≠ creditore/debitore)
- 3 sezioni integrate dalla lezione: riserva di legge, criteri applicazione legge nello spazio, ambiti del diritto
- Domande di autoverifica: tutte e 5 risposte presenti negli appunti grezzi

**Prossima sessione — da dove partire**:
→ **Modulo D2** — Ricerca e Analisi delle Fonti del Diritto (`02_DirInfo_2026_RicercaFonti_DEF.pdf`). Eseguire `/lezione D2` prima di iniziare.

---

### Sessione 1 — 2026-04-15
**Focus**: Inquadratura generale. Valutazione livello reale sui 3 corsi. Costruzione master map e metodologia.
**Completato**:
- Analisi checklist e study plan preesistenti
- Valutazione livello reale (SysAdmin: near-zero; Security: vaghissimo; Diritto: quasi completo)
- Creazione master_map_studio.md
- Salvataggio memoria persistente per sessioni future

---

### Sessione 10 — 2026-04-24 (completata)
**Focus**: Modulo 3A — completamento Es. 3–7 + chiusura modulo

**Coperto in sessione**:
- Es. 3 ✅ — niceexec.sh completato e testato sulla VM
- Es. 4 ✅ — manipolazione crontab da script (pattern mktemp + grep -vF + crontab FILE)
- Es. 5 ✅ — configurazione rsyslog con facility personalizzata in `/etc/rsyslog.d/` *(codice commentato, non eseguito sulla VM)*
- Es. 6 ✅ — script logconfig: configura rsyslog + aggiunge job cron per `uptime | logger` *(codice commentato, non eseguito sulla VM)*
- Es. 7 ✅ — esame unit systemd reali (networking, dnsmasq, cron, rsyslog) *(codice commentato, non eseguito sulla VM)*
- Appunti `appunti_modulo3A_systemd_servizi.md` aggiornati con codice commentato per tutti e 7 gli esercizi

**Prossima sessione — da dove partire**:
→ **Modulo 3B** — Gestione dei Pacchetti Software (`apt`, `dpkg`, repository). Eseguire `/lezione 3B` prima di avviare la VM.

---

### Sessione 8 — 2026-04-23
**Focus**: Modulo 3A — Gestione Servizi con Systemd (elaborazione appunti)

**Completato**:
- Appunti modulo `3A` elaborati → `appunti_modulo3A_systemd_servizi.md`
- Risolte 19 domande aperte (demoni, init, target, unit file, dipendenze, at, cron, asterischi, rsyslog, journald)
- Integrata sezione diagnostica istantanea (ps, uptime, free, top) assente dagli appunti grezzi
- Integrati Es. 2–7 del lab con note ⬜ Da eseguire

**Prossima sessione — da dove partire**:
→ **Modulo 3A lab pratico** — Eseguire Es. 2–7 sulla VM (watchdog, niceexec, manipolazione crontab, rsyslog, logconfig, esame unit reali). Poi procedere con **Modulo 3B** — Gestione Pacchetti.

---

### Sessione 7 — 2026-04-21 (in corso)
**Focus**: Modulo 2A — Gestione Utenti e Permessi

**⚠️ PUNTO DI PAUSA — da riprendere qui**:
`chmod` (notazione ottale e simbolica) non è stato eseguito nella sessione pratica. Da riprendere all'inizio della prossima sessione prima di procedere con il Modulo 2B.
Esercizi da fare:
```bash
chmod 000 file_test.txt && cat file_test.txt   # deve dare Permission denied
chmod 644 file_test.txt && cat file_test.txt   # deve funzionare
chmod u+x script.sh / chmod g-w file.txt       # notazione simbolica
```

**Coperto in sessione**:
- UID/GID, `/etc/passwd`, `/etc/shadow` — struttura e lettura
- `useradd`, `passwd`, `usermod -aG`, `su -`, `userdel -r`
- `chown`, `chgrp` — cambio proprietario e gruppo
- `sudo -l` — interpretazione output (`NOPASSWD: ALL` via `/etc/sudoers.d/vagrant`)
- Esercizio integrato completo: groupadd, directory condivisa `/srv/progetto` con permessi 770, test con alice/bob/sconosciuto

**Non coperto (da fare all'inizio sessione 8)**:
- `chmod` notazione ottale (644, 755, 700, 000) e simbolica (`u+x`, `g-w`, `o-r`)

**Prossima sessione — da dove partire**:
→ Riprendere da `chmod` (5 minuti), poi **Modulo 2B** — LAB Utenti, Permessi e File

---

### Sessione 6 — 2026-04-21 (completata)
**Focus**: Modulo 1B — Funzioni, Case, Test avanzati, Exit code

**Coperto in sessione**:
- Elaborazione appunti grezzi del Modulo 1B in appunti strutturati
- Risolte 4 domande aperte emerse dalla sessione pratica autonoma:
  - Perché le stringhe letterali passate a funzioni si quotano
  - Come funziona la guard clause `if [ -z "$FILE" ]` in `case_file.sh`
  - Come funziona `controlla_servizio` — uso diretto dell'exit code di `systemctl` come condizione dell'`if`
  - Bug `[ !-d ]` → corretto in `[ ! -d ]` (spazio obbligatorio tra `!` e operatore)
- Versione corretta di `classifica_dir.sh` con guard clause doppia e contatori

**Prossima sessione — da dove partire**:
→ **Modulo 2A** — Gestione Utenti e Permessi (`useradd`, `chmod`, `chown`, `sudo`)

### Sessione 5 — 2026-04-17 (completata)
**Focus**: Modulo 1A completato + Modulo 1B iniziato (Parte 1 — funzioni)

**Focus**: Modulo 1A — Variabili, Condizioni, Loop Bash

**Coperto in sessione**:
- Creazione script con heredoc (`cat > file << 'EOF'`), shebang, `chmod +x`, esecuzione con `./`
- Command substitution `$()` — `$(date)`, `$(whoami)` e pattern derivati
- Variabili: assegnazione (`VAR=valore`, senza spazi), lettura (`$VAR`, `${VAR}`), lunghezza (`${#VAR}`)
- Variabili speciali: `$0`, `$1`, `$2`, `$#`, `$@` — testate con script `argomenti.sh`
- Variabili d'ambiente: `$HOME`, `$USER`, `$SHELL`, `$PATH`
- Condizioni `if/then/elif/else/fi` — operatori numerici (`-gt`, `-lt`, `-eq`), stringhe (`-z`, `-n`), file (`-f`, `-d`, `-e`, `-r`, `-w`, `-x`)
- Negazione con `!` — pattern guard clause (`if [ ! -d ]; then exit 1; fi`)
- Loop `for` su lista, su glob `/etc/*.conf`, numerico con `$(seq 1 5)`, loop `while` con contatore
- Script completo `analizza_dir.sh` — analisi directory con contatori file/dir
- Esercizio autonomo `cerca_file.sh` — scritto e corretto, bug spiegati (logica invertita, glob non espanso, `done` mancante, shebang incompleto)

**Dubbi risolti in sessione**:
- Variabile del `for` non si dichiara prima; persiste dopo `done`
- `FILE` non è parola riservata — il nome è arbitrario
- Tavola comandi utili con `$()`: `seq`, `ls`, `cat`, `date +%Y-%m-%d`, `hostname`, `wc -l`

**Prossima sessione — da dove partire**:
→ **Modulo 1B** — Funzioni, `case`, test condizionali avanzati (`-f`, `-d`, `-z`, `-eq`), exit codes

---

### Sessione 3 — 2026-04-16 (completata)
**Focus**: Ripresa Modulo 0A — permessi, anatomia comandi, home directory.

**Coperto in sessione**:
- Anatomia di un comando Linux: `comando [opzioni] [argomento]` — spiegato con `ls -la ~`
- Stringa permessi `drwxr-xr-x` smontata carattere per carattere (4 blocchi: tipo | owner | gruppo | altri)
- Concetto di owner, gruppo, altri — spiegato con esempio multi-utente
- Home directory `/home/vagrant` — identificata, file nascosti (`.`) spiegati
- File `.bashrc`, `.bash_history`, `.profile`, `.ssh` — ruoli spiegati
- Creati `cartella_test/` e `file_test.txt` nella home
- Permessi di default Linux: directory→`drwxr-xr-x`, file→`-rw-r--r--`
- Comando `touch` spiegato

**⚠️ PUNTO DI PAUSA — da riprendere qui**:
Esercizio `chmod` interrotto a metà. Sequenza da completare:
```bash
echo "contenuto segreto" > file_test.txt
cat file_test.txt
chmod 000 file_test.txt
cat file_test.txt          # → deve dare "Permission denied"
```
Poi spiegare `chmod` in notazione ottale (000, 644, 755, 700) e fare esercizi su `cartella_test`.

**Prossima sessione — da dove partire**:
→ **Modulo 1A** — Variabili, condizioni, loop Bash. Lezione già scritta da generare a inizio sessione.

### Sessione 2 — 2026-04-15 (completata)
**Focus**: Setup VM Vagrant + Debian 12. Modulo 0A — Filesystem e Comandi Base Linux.
**VirtualBox e Vagrant**: ✅ Già installati sul PC.
**VM Debian**: ✅ Operativa. Directory: `~/sysAdmin-lab`. Comando di accesso: `cd ~/sysAdmin-lab && vagrant up && vagrant ssh`

**Coperto in sessione**:
- Struttura filesystem Linux (`/`, `/etc`, `/home`, `/var`, `/proc`, ecc.) — concetti spiegati e navigati
- Comandi `pwd`, `whoami`, `id`, `ls`, `cat` — eseguiti e compresi
- Sistema UID/GID — spiegato
- File `/etc/debian_version` e `/etc/hostname` — letti
- Contenuto `/var/log` — esplorato (auth.log, btmp, syslog)
- Output `ls -la` — spiegato il formato (permessi, proprietario, gruppo)

**⚠️ PUNTO DI PAUSA — da riprendere qui**:
Comando eseguito: `ls -la ~`
Concetto da chiarire: **la stringa di permessi** (`drwxr-xr-x`) — la spiegazione è stata data ma Lorenzo non l'ha ancora interiorizzata. Riprendere con una spiegazione più graduale, usando esempi concreti su file reali nella home.

**Prossima sessione — da dove partire**:
1. Riepilogo rapido della stringa permessi con esempi pratici
2. Esercizio: creare file e directory nella home, leggerne i permessi
3. Poi concludere Modulo 0A e passare a Modulo 0B

---

## Stato Generale Avanzamento

```
SysAdmin  ████████░░  77%   (10/13 moduli ✅)
Security  ░░░░░░░░░░   0%   (0/12 moduli ✅)
Diritto   ███████░░░  64%   (7/11 moduli ✅)
```

*SysAdmin (13): 0A 0B 1A 1B 2A 2B 2C 3A 3B 3C ✅ | 3D 🔄 | 3E 3F ⬜*
*Security (12): S1 🔄 | S2–S12 ⬜*
*Diritto (11):  D1 ✅ D2 ✅ D3 ✅ D4 ✅ D5 ✅ D6 ✅ D7 ✅ | D8–D11 ⬜*
