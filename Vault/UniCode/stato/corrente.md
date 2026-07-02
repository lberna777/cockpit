# Stato Corrente — Studio Attivo
**Sessione**: 45 | **Aggiornato**: 2026-07-02

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
| S5 | Firewall + packet filter + LAB | ⭐ **Iptables/NFTables** | ✓ | ⬜ |
| S6 | Sicurezza fisica e cloud | — | ✓ | ⬜ |
| S7 | LAB Backdoor injection | (privesc) | ✓ | ⬜ |
| S8 | LAB Individuare e filtrare attacchi | (NIDS/privesc) | ✓ | ⬜ |
| S9 | Demoni + Autorizzazione + PAM | (privesc) | ✓ | ⬜ |
| S10 | Rilevare attacchi + LAB NIDS Suricata | ⭐ **Network Intrusion Detection** | ✓ | ⬜ |
| S11 | HIDS + LAB Misconfiguration + LAB Pentesting target | ⭐ **Integrity/privesc** | ✓ | ⬜ |
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
Security  ████░░░░░░  ~27%  (4/15 moduli ✅ — S1 22/06, S2 23/06, S3 26/06, S4 02/07)
Diritto   ██████████  100%  ✅ ESAME SUPERATO — 30 e lode (16/06)
```

> ⚠️ **Esame Security — prova DOPPIA** (stessa seduta, entrambe devono essere sufficienti):
> - **Quiz teorico (40%)** — 30-40 domande vero/falso o scelta multipla, 45 min, **nessun materiale**, penalità per risposta sbagliata. Copre tutto il programma, inclusi i comandi visti in lab.
> - **Prova pratica (60%)** — 2 ore, esercizi lab offensivi e difensivi, materiale consentito.
> **Esame SysAdmin**: prova pratica su PC del lab. VM a tua cura.

---

## Prossimi Passi

> ✅ **Diritto chiuso** (16/06, **30 e lode**). 🚨 **Aggiornamento 01/07**: obiettivo di questa sessione ridotto a **un solo esame — Security (17/07)**. **Sistemi rimandato a settembre (08/09/2026)**: a 16 giorni dall'esame con Security solo al ~20%, portare avanti entrambi in parallelo non era più sostenibile (vedi `ESAMI SCELTI.md`, Rischi #4). **SysAdmin è sospeso** fino a dopo il 17/07 — nessuna azione su 3D–4C o scripting fino a esame Security superato. Ritmo Security: ~5.5h/gg costanti, senza carico parallelo. I LAB su VM vanno eseguiti giorno per giorno, non accumulati.

**Security** (focus esclusivo) → S1 ✅, S2 ✅, S3 ✅, **S4 ✅ chiuso (sessione 45, 02/07)** — LAB completo tutti e 4 gli esercizi. **Es1 `write_var` ✅**, **es2 `secret_function` ✅** (offset 16, ASLR/reboot gotcha in `troubleshooting_vm.md`), **es2b `secret_function_remote` ✅** (fix `gets()` non dichiarata dalle glibc moderne, esposizione in rete con `ncat` installato ad-hoc, shell remota senza root). **Es3 `returnlib` (shellcode + SUID) ✅ — root shell ottenuta**: offset 112 (bisezione con stadio intermedio "EBP corrotto" a 110-111, `SIGSEGV in main()`, poi `SIGILL` a 112 = ret riuscito ma atterraggio storto, poi `BBBB` → `0x42424242 in ?? ()` = offset confermato). Due gotcha: **bad character** (`0x20` spazio nell'indirizzo scelto tronca il payload via `$(...)` non quotato) e **stack sotto gdb ≠ stack standalone anche con ASLR off** (soluzione: core dump della vera esecuzione con `fs.suid_dumpable=1` + `sudo coredumpctl gdb <PID>`). **Es4 `returnlib` (ret2libc) ✅ — NX bypassato**: stesso offset 112, stack NON eseguibile, riusato `system()`+`exit`+stringa `SHELL=` della libc invece di shellcode iniettato; niente SUID qui (non serviva root). Nuovo gotcha: **bad character su un indirizzo di funzione** (non su un indirizzo di stack a scelta libera) — `system` aveva byte basso `0x20` (spazio), stesso sintomo di es3 ma stavolta il fix non è "sposta il bersaglio" (un solo entry point valido) bensì **quotare la sostituzione di shell** (`run "$(perl -e '...')"`). Anche: `x/500s $esp` inaffidabile su grandi distanze (troppi terminatori consumano il conteggio) → preferire `find $esp, +lunghezza, "pattern"`, attenti a non sforare `0xffffffff` nell'aritmetica degli indirizzi. Tutto annotato in `guida_lab_moduloS4_binary_exploits.md` (sezioni "✍️ Esecuzione — risultati reali" es1-es4). DRILL finale ancora da fare: `SIMULAZIONI ESAMI/SICINF/Binary_exploitation.html`. **Prossimo modulo: S5** (Firewall/iptables) — nuovo, serve `/lezione S5` prima della VM. Poi S6 → S7 → S8 → S9 → S10 → S11 → S12 → S13 → S14 → S15.
**SysAdmin** (sospeso fino al 17/07) → **3D**: lezione ✅, guida_lab ✅ (pronta, lab su VM non ancora eseguito). Ripresa post-Security: avvia VM (`cd ~/Progetti/sysAdmin-lab && vagrant up --provider=virtualbox && vagrant ssh`), segui `guida_lab_modulo3D_networking_base.md` Es. 1–6, annota inline, poi `/appunti 3D`. Poi: 3E → 3F → 4B → 4C. Guida_lab 0A–2B da rifare a bassa priorità. Piano dettagliato per la sessione settembre da definire dopo il 17/07.

---

## Scadenze Esami

| Esame | Data | Ora |
|-------|------|-----|
| ~~Diritto dell'Informatica T~~ | ✅ 16/06/2026 — **30 e lode** | — |
| Lab Amministrazione di Sistemi T | ~~15/07/2026~~ → **08/09/2026** (rimandato) | — |
| Lab Sicurezza Informatica T | **17/07/2026** | 14:00 |

Piano fasi e stime ore dettagliate: `ESAMI SCELTI.md`
