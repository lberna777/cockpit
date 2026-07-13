# Stato Corrente — Studio Attivo
**Sessione**: 49 | **Aggiornato**: 2026-07-13

> **Istruzione per Claude**: questo file va letto ALL'INIZIO di ogni sessione. È l'unico file obbligatorio per avere contesto.
> Per dettagli sui moduli (materiali, concetti, esercizi): `stato/percorso.md`
> Per lo storico delle sessioni passate: `stato/log_sessioni.md`
> Per il piano fasi e stime ore: `ESAMI SCELTI.md`

---

## Stato Moduli

### SysAdmin — Lab Amministrazione di Sistemi T

> ⚠️ **0A–2B (sistema embrionale)**: lab eseguiti ✅ ma materiali da rifare. Le "lezioni" erano walkthrough — rinominate in `guida_lab_*`. Nessuna lezione teorica esiste per questi moduli. Guida-lab da rifare con le nuove direttive quando c'è tempo. Conoscenza teorica: non verificata. Esame solo pratico → priorità bassa rispetto a 3E–4C.

| Modulo | Nome | Stato | Note |
|--------|------|-------|------|
| 0A | Filesystem e Comandi Base | ⚠️ | Lab eseguito (s.3); guida_lab MANCANTE; no lezione |
| 0B | Pipe, Redirect e Filtri | ⚠️ | Lab eseguito (s.4); guida_lab da rifare; no lezione |
| 1A | Variabili, Condizioni, Loop | ⚠️ | Lab eseguito (s.5); guida_lab da rifare; no lezione |
| 1B | Funzioni, Case, Test | ⚠️ | Lab eseguito (s.6); guida_lab da rifare; no lezione |
| 2A | Gestione Utenti e Permessi | ⚠️ | Lab eseguito (s.7-8); guida_lab da rifare; no lezione |
| 2B | LAB Utenti, Permessi e File | ⚠️ | Lab eseguito; guida_lab da rifare; no lezione |
| 2C | Gestione File: find, tar, rsync | ✅ | |
| 3A | Gestione Servizi con Systemd | ✅ | Sessione 10 |
| 3B | Gestione Pacchetti Software | ✅ | Sessione 13 |
| 3C | Gestione Processi | ✅ | Sessione 16 |
| 3D | Networking di Base | ⬜ | Restart dall'Es.1 — guida_lab in creazione |
| 3E | Vagrant Multi-Machine | ⬜ | |
| 3F | Automazione con Ansible | ⬜ | |
| 4A | Servizi base rete (DHCP, router via Ansible) | ⬜ | ⚠️ non mappato prima |
| 4B | **SNMP / Monitoraggio centralizzato** + LAB | ⬜ | ⚠️ **mancante: né mappato né scaricato né studiato** — è d'esame (netmon/SNMP) |
| 4C | **LDAP / Configurazione centralizzata** + LAB | ⬜ | ⚠️ **mancante: né mappato né scaricato né studiato** — è d'esame (auth LDAP) |

**Esercizi Scripting** (traccia parallela in `esercizi/SYSADM/`):
- Catena A — ls ricorsivo: lab_01 ⬜, lab_02 ⬜, lab_03 ⬜, es_03 ⬜
- Catena B — conversione tempo: lab_04 ⬜, lab_05 ⬜, lab_06 ⬜, lab_07 ⬜, es_04 ⬜
- Catena C — processi e segnali: es_05 ⬜, es_06 ⬜, es_07 ⬜, es_08 ⬜

### Security — Lab Sicurezza Informatica T
> **Codici S1–S12 invariati** (ordine di corso, come in `percorso.md`); **aggiunti S13–S15**
> per le sezioni che mancavano (Net Security/TLS, Crittografia). Dettaglio materiali +
> file locali/da scaricare: `percorso.md`. Ordine di *studio* (per famiglie d'esame):
> `metodo_studio_esami_pratici.md`.
> **Esame = prova pratica sui PC del lab: 3 esercizi tra 5 tipologie** (⭐). VM a tua cura.

| Cod | Modulo | ⭐ Tipo esame | Locale | Stato |
|---|---|---|---|---|
| S1 | Principi offensive + LAB Enumerazione | base (feed tutte) | ✓ | ✅ Sessione 37 |
| S2 | Autenticazione | — | ✓ | ✅ Sessione 38 |
| S3 | Web security + LAB (OWASP 2025) | ⭐ **Web vulnerabilities** | ✓ | ✅ Sessione 41 |
| S4 | Binary exploits + LAB buffer overflow | ⭐ **Binary exploitation** | ✓ | ✅ Sessione 45 — LAB completo: es1 `write_var` ✅, es2 `secret_function` ✅, es2b `secret_function_remote` ✅ (shell remota, no root), es3 `returnlib` shellcode+SUID ✅ (root shell), es4 `returnlib` ret2libc ✅ (NX bypassato via `system()`, no root — non serviva) |
| S5 | Firewall + packet filter + LAB | ⭐ **Iptables/NFTables** | ✓ | 🔄 lezione ✅, appunti ✅, guida-lab ✅ (9 esercizi); **Es1 (endpoint INPUT/OUTPUT) ✅ ed Es2 (FORWARD su R1) ✅ eseguiti su VM** — Es3-9 da fare (handle, stateful multi-macchina, logging, NAT, catene custom, contatori) |
| S6 | Sicurezza fisica e cloud | — | ✓ | ⬜ |
| S7 | LAB Backdoor injection | (privesc) | ✓ | ⬜ |
| S8 | LAB Individuare e filtrare attacchi | (NIDS/privesc) | ✓ | ⬜ |
| S9 | Demoni + Autorizzazione + PAM | (privesc) | ✓ | ⬜ |
| S10 | Rilevare attacchi + LAB NIDS Suricata | ⭐ **Network Intrusion Detection** | ✓ | ✅ Sessione 48 (10-13/07) — **3 esercizi reali completati hands-on sulla VM**: 13/02/2025 (HTTP flood, sessione 47), 11/01/2024 (port scan+SSH+Telnet flag+DDoS, confrontato con soluzione ufficiale), 10/07/2025 (buffer-overflow SMTP a padding incrementale). Guida operativa `guida_esame_NIDS.md` rivista ed estesa più volte con le lezioni pratiche di ogni esercizio. Nessuna lezione/appunti teorici formali ancora (scelta deliberata, "esercizi prima teoria dopo") — ARP (2 varianti nel pool) non ancora praticato hands-on |
| S11 | HIDS + LAB Misconfiguration + LAB Pentesting target | ⭐ **Integrity/privesc** | ✓ | 🔄 Sessione 49 (13/07) — **1 esercizio reale completato hands-on sulla VM**: 9 gennaio 2023 (`change1`, SUID su `cp`, verificato contro soluzione ufficiale su Virtuale). Nessuna lezione/appunti teorici formali ancora (scelta deliberata, "esercizi prima teoria dopo") — restano da praticare altre varianti del pool (`change2...change9`, caso 12 gennaio 2026 già documentato in `modello_integrity_privesc.md` ma non hands-on) e i due lab dedicati (misconfiguration, HIDS/AIDE) letti ma non eseguiti |
| S12 | Sicurezza delle comunicazioni | — | ✓ | ⬜ |
| S13 | Offensive net sec + Protezione comunicazioni + OpenSSL/TLS | — | ✓ | ⬜ |
| S14 | Crittografia: intro + cifrari moderni + rainbow tables | — | ✓ | ⬜ |
| S15 | LAB gpg + gestione chiavi | — | ✓ | ⬜ |

**Le 5 tipologie d'esame** (testi+soluzioni su Virtuale → scaricare in `SIMULAZIONI ESAMI/SICINF/`):
Integrity check & privilege escalation (S11) · Network Intrusion Detection (S10) ·
Iptables/NFTables (S5) · Binary exploitation (S4) · Web vulnerabilities (S3).

### Diritto — Diritto dell'Informatica T
| Modulo | Nome | Stato | Note |
|--------|------|-------|------|
| D1 | Concetti Giuridici di Base | ✅ | Sessione 11 |
| D2 | Ricerca e Analisi Fonti | ✅ | Sessione 12 |
| D3 | Diritto d'Autore e Software | ✅ | Sessione 16 |
| D4 | Banche Dati e Siti Web | ✅ | Sessione 21 |
| D5 | Contratti Informatici | ✅ | Sessione 22 |
| D6 | Contratto Sviluppo Software | ✅ | Sessione 24 |
| D7 | Proprietà Industriale | ✅ | Sessione 25 |
| D8 | Privacy e GDPR | ✅ | Sessione 26 |
| D9 | Firme Elettroniche | ✅ | Sessione 28 — ripasso 2/5 corrette, lacuna su gerarchia firme e opponibilità PEC |
| D10 | Commercio Elettronico | ✅ | Sessione 29 — lacuna: gerarchia 70/2003 vs Codice consumo |
| D11 | Reati Informatici | ✅ | Sessione 30 — lacune: 615-quinquies vs 635-xx, mera condotta, vittima frode |
| D12 | AI Act | ✅ | Sessione 31 — lacune: pratiche vietate (solo 2/8 elencate), obblighi GPAI, fasce sanzionatorie |
| D13 | DSA/DMA/Data Act | ✅ | Sessione 32 — lacuna: anti-steering (soggetto invertito: commerciale, non utente finale) |

---

## Avanzamento

```
SysAdmin  ████░░░░░░  ~25%  (4/16 moduli ✅ solidi: 2C, 3A, 3B, 3C — 0A–2B lab fatti ma materiali da rifare, 3D–4C da fare)
Security  ███░░░░░░░  ~33%  (5/15 moduli ✅ + S11 🔄 — S1 22/06, S2 23/06, S3 26/06, S4 02/07, S10 13/07 — 5/5 tipologie ⭐ d'esame toccate: S3,S4,S10 ✅, S5 parziale, S11 avviato 13/07)
Diritto   ██████████  100%  ✅ ESAME SUPERATO — 30 e lode (16/06)
```

> ⚠️ **Esame Security — prova DOPPIA** (stessa seduta, entrambe devono essere sufficienti):
> - **Quiz teorico (40%)** — 30-40 domande vero/falso o scelta multipla, 45 min, **nessun materiale**, penalità per risposta sbagliata. Copre tutto il programma, inclusi i comandi visti in lab.
> - **Prova pratica (60%)** — 2 ore, esercizi lab offensivi e difensivi, materiale consentito.
> **Esame SysAdmin**: prova pratica su PC del lab. VM a tua cura.

---

## Prossimi Passi

> ✅ **Diritto chiuso** (16/06, **30 e lode**). 🚨 **Aggiornamento 01/07**: obiettivo di questa sessione ridotto a **un solo esame — Security (17/07)**. **Sistemi rimandato a settembre (08/09/2026)**: a 16 giorni dall'esame con Security solo al ~20%, portare avanti entrambi in parallelo non era più sostenibile (vedi `ESAMI SCELTI.md`, Rischi #4). **SysAdmin è sospeso** fino a dopo il 17/07 — nessuna azione su 3D–4C o scripting fino a esame Security superato. Ritmo Security: ~5.5h/gg costanti, senza carico parallelo. I LAB su VM vanno eseguiti giorno per giorno, non accumulati.
>
> **Aggiornamento 07/07 (sessione 46)**: da qui in avanti, negli esercizi guida-lab **eseguire sulla VM solo quelli effettivamente utili e collegati alle modalità d'esame** (non tutti i 9/N esercizi di un modulo per principio) — con 10 giorni rimasti, priorità a ciò che allena direttamente il formato della prova pratica (specialmente per i moduli ⭐ delle 5 tipologie) piuttosto che copertura esaustiva di ogni variante dimostrativa del PDF.
>
> **Aggiornamento 08/07 (sessione 47)**: aperto un **secondo binario di lavoro in parallelo al percorso sequenziale** (S5→S6→...) — pratica diretta sulle 5 tipologie d'esame tramite `SIMULAZIONI ESAMI/SICINF/modelli_risolti/` (esempi reali risolti + template + procedura operativa per tipologia, si costruiscono progressivamente). Approccio deciso da Lorenzo: "esercizi prima, teoria dopo" per le tipologie ancora a 0% (S10, S11), vista la vicinanza dell'esame — vedi `[[feedback_esercizi_prima_teoria_dopo]]` in memoria. Non sostituisce il percorso sequenziale, lo affianca.
>
> **Aggiornamento 13/07 (sessione 48)**: **S10 chiuso ✅** — 2 esercizi reali aggiuntivi completati (11/01/2024, 10/07/2025), portando il totale a 3 esercizi NIDS hands-on. `guida_esame_NIDS.md` rivista a fondo con le lezioni pratiche emerse (mappatura Protocol Hierarchy↔Conversations, criteri di giudizio ICMP/DNS, verifica con flag TCP grezzi). Con 4 giorni all'esame, **priorità decisa**: S11 (Integrity check/privesc, ⭐ tipologia ancora a 0%) o completare S5 (⭐ già parziale) — da confermare a inizio prossima sessione in base al tempo disponibile. ARP (2 varianti nel pool S10) resta scoperto hands-on, priorità bassa.
>
> **Aggiornamento 13/07 (sessione 49)**: **S11 avviato 🔄** — primo esercizio reale completato hands-on (9 gennaio 2023, SUID su `cp`), verificato contro la soluzione ufficiale su Virtuale. Con 3 giorni all'esame, lanciato un agente in background per catalogare le altre varianti del pool (`change2...change9` + caso 12/01/2026 già in `modello_integrity_privesc.md`) e produrre una guida operativa analoga a `guida_esame_NIDS.md`. **VM da ripristinare da snapshot pulito** prima del prossimo esercizio (utente `toor` e SUID su `cp` sono residui di sessione 49).

**Security** (focus esclusivo) → S1 ✅, S2 ✅, S3 ✅, **S4 ✅ chiuso (sessione 45, 02/07)** — LAB completo tutti e 4 gli esercizi. **Es1 `write_var` ✅**, **es2 `secret_function` ✅** (offset 16, ASLR/reboot gotcha in `troubleshooting_vm.md`), **es2b `secret_function_remote` ✅** (fix `gets()` non dichiarata dalle glibc moderne, esposizione in rete con `ncat` installato ad-hoc, shell remota senza root). **Es3 `returnlib` (shellcode + SUID) ✅ — root shell ottenuta**: offset 112 (bisezione con stadio intermedio "EBP corrotto" a 110-111, `SIGSEGV in main()`, poi `SIGILL` a 112 = ret riuscito ma atterraggio storto, poi `BBBB` → `0x42424242 in ?? ()` = offset confermato). Due gotcha: **bad character** (`0x20` spazio nell'indirizzo scelto tronca il payload via `$(...)` non quotato) e **stack sotto gdb ≠ stack standalone anche con ASLR off** (soluzione: core dump della vera esecuzione con `fs.suid_dumpable=1` + `sudo coredumpctl gdb <PID>`). **Es4 `returnlib` (ret2libc) ✅ — NX bypassato**: stesso offset 112, stack NON eseguibile, riusato `system()`+`exit`+stringa `SHELL=` della libc invece di shellcode iniettato; niente SUID qui (non serviva root). Nuovo gotcha: **bad character su un indirizzo di funzione** (non su un indirizzo di stack a scelta libera) — `system` aveva byte basso `0x20` (spazio), stesso sintomo di es3 ma stavolta il fix non è "sposta il bersaglio" (un solo entry point valido) bensì **quotare la sostituzione di shell** (`run "$(perl -e '...')"`). Anche: `x/500s $esp` inaffidabile su grandi distanze (troppi terminatori consumano il conteggio) → preferire `find $esp, +lunghezza, "pattern"`, attenti a non sforare `0xffffffff` nell'aritmetica degli indirizzi. Tutto annotato in `guida_lab_moduloS4_binary_exploits.md` (sezioni "✍️ Esecuzione — risultati reali" es1-es4). DRILL finale ancora da fare (rimandato, non bloccante): `SIMULAZIONI ESAMI/SICINF/Binary_exploitation.html` — file scaricato in `esercizi/SICINF/sim_binary_2026-02-12/secret.gz`, esercizio 12/02/2026 (il più recente).
**S5 (Firewall/iptables/nftables) 🔄 — sessione 46, 07/07**: lezione ✅, appunti ✅, guida-lab ✅ (9 esercizi). Ambiente VM sbloccato dopo troubleshooting corposo (Guest Additions clipboard, conflitto Docker/Podman via `DOCKER_HOST`, `interface_name` che richiede Docker Engine v28.1+ non presente nel pacchetto distro — fix: rimossa la proprietà da `nftlab.sh`, dettagli in `troubleshooting_vm.md`). **Es1 (packet filter endpoint, Client, INPUT/OUTPUT default-drop) ✅** e **Es2 (packet filter in instradamento, R1, FORWARD ristretto a Client↔S1/S2) ✅** eseguiti e verificati con ping prima/dopo. **Prossimo: Es3** (gestione regole con handle: add/insert/delete/replace) — poi Es4 (stateful SSH selettivo), Es5 (multi-macchina), Es6 (logging), Es7 (NAT — ⭐ rilevante), Es8 (catene custom), Es9 (contatori). Applicare il filtro "solo se utile per l'esame" (vedi nota sopra) nella scelta di quali di questi completare. Poi S6 → S7 → S8 → S9 → S10 → S11 → S12 → S13 → S14 → S15.

**S10 (Network Intrusion Detection) ✅ chiuso — sessione 48, 10-13/07**: 3 esercizi reali completati hands-on sulla VM. **13/02/2025** (sessione 47): HTTP flood/buffer-overflow-probe, 31 alert, consegna in `esercizi/SICINF/pratica_NIDS_2025-02-13/`. **11/01/2024** (`dump.pcap`): 4 tipi di interazione verso `10.10.10.10` — port scan TCP-connect da `10.10.3.1` (porte 22/80 trovate aperte via SYN,ACK), SSH legittima (2 sessioni con dati reali sulla stessa porta 22 dello scan — lezione: stessa porta/coppia host può nascondere cose diverse, verificare sempre con `tcp.flags`+`tcp.len`, non assumere), Telnet con flag `FLAG{this_port_is_dangerous}` da due sorgenti diverse (10.10.5.21, 10.10.31.2), DDoS con 151 sorgenti distinte su porta 80; regola scritta, 2 alert verificati, flag estratta (jq assente sulla VM → fallback Python), report scritto e **confrontato con la soluzione ufficiale** (ottimo allineamento, in più punti più rigoroso del testo ufficiale). **10/07/2025** (`trace-2025-07-10.pcapng`): topologia a 3 host/3 subnet confermata via scheda Ethernet Conversations (MAC riscritti a ogni salto router); buffer-overflow via SMTP con padding incrementale 0/1 e marcatore fisso `ABCD` (`10.10.101.129→10.10.103.172:25`); HTTP/DNS/ICMP/ARP tutti verificati e classificati come legittimi (DNS = query PTR/A ripetute per l'host mittente, spiegate dai tentativi SMTP ripetuti, non un fenomeno a parte); regola scritta ed eseguita con successo. **Momento critico**: attacco di panico a metà del secondo esercizio per troppi comandi tecnici concatenati senza spiegazione — gestito con pausa, poi ripreso con ritmo più lento (spiegare il perché prima di ogni comando) fino a chiusura. `guida_esame_NIDS.md` rivista e ampliata più volte con le lezioni pratiche di tutti e 3 gli esercizi (mappatura Conversations↔Protocol Hierarchy, criteri ICMP/DNS, verifica flag TCP grezzi, fallback jq). Non ancora praticato hands-on: ARP (2 varianti nel pool, 12/01/2026 e 30/10/2025) — Lorenzo ha scelto di consolidare prima il territorio TCP/applicativo. Nessuna lezione/appunti teorici formali (scelta deliberata).
**S11 (Integrity check/privilege escalation) 🔄 — sessione 49, 13/07**: primo esercizio reale completato hands-on: **9 gennaio 2023** (`change1`). Fase 1: configurato AIDE (scoperto che `/usr/bin` non è coperto dalla config di default — serve regola esplicita `/usr/bin f Full`, aggiunta **prima** di `aideinit` perché l'ordine baseline→modifica→confronto è l'unico che ha senso), identificata la modifica: `/usr/bin/cp` ha acquisito il bit **SUID**. Fase 2: sfruttato il SUID di `cp` per leggere/scrivere `/etc/passwd` e `/etc/shadow` senza `sudo` — copia via `cp` (resta root-owned, non scrivibile), resa editabile con `cat file > file_editable` (la redirezione gira con privilegi normali, a differenza di `cp`), riga utente `toor` con UID/GID `0` e campo password vuoto in shadow, riscrittura dei file di sistema di nuovo via `cp` SUID. Verificato: `su toor` senza richiesta di password, `id` conferma `uid=0(root)`. Soluzione confrontata con quella ufficiale su Virtuale (stessa strategia). Deliverable prodotti: `integrity.txt`, `privesc.png`. **AIDE non era preinstallato** su questa VM (`sudo apt install aide`), annotato in `troubleshooting_vm.md` e aggiunto alla checklist pre-snapshot. Restano da esplorare le altre varianti del pool (agente in background per il catalogo completo) e i due lab dedicati non ancora praticati hands-on (misconfiguration: sudoers/suid/acl/capabilities; HIDS: AIDE + privesc, letti ma non eseguiti sulla VM).

**SysAdmin** (sospeso fino al 17/07) → **3D**: lezione ✅, guida_lab ✅ (pronta, lab su VM non ancora eseguito). Ripresa post-Security: avvia VM (`cd ~/Progetti/sysAdmin-lab && vagrant up --provider=virtualbox && vagrant ssh`), segui `guida_lab_modulo3D_networking_base.md` Es. 1–6, annota inline, poi `/appunti 3D`. Poi: 3E → 3F → 4B → 4C. Guida_lab 0A–2B da rifare a bassa priorità. Piano dettagliato per la sessione settembre da definire dopo il 17/07.

---

## Scadenze Esami

| Esame | Data | Ora |
|-------|------|-----|
| ~~Diritto dell'Informatica T~~ | ✅ 16/06/2026 — **30 e lode** | — |
| Lab Amministrazione di Sistemi T | ~~15/07/2026~~ → **08/09/2026** (rimandato) | — |
| Lab Sicurezza Informatica T | **17/07/2026** | 14:00 |

Piano fasi e stime ore dettagliate: `ESAMI SCELTI.md`
