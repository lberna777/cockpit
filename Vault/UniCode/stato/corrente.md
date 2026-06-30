# Stato Corrente — Studio Attivo
**Sessione**: 43 | **Aggiornato**: 2026-06-30

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
| S4 | Binary exploits + LAB buffer overflow | ⭐ **Binary exploitation** | ✓ | 🔄 lez+app+guida ✅; LAB: es1 `write_var` ✅, es2 `secret_function` in corso |
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
Security  ███░░░░░░░  ~20%  (3/15 moduli ✅ — S1 22/06, S2 23/06, S3 26/06)
Diritto   ██████████  100%  ✅ ESAME SUPERATO — 30 e lode (16/06)
```

> ⚠️ **Esame Security — prova DOPPIA** (stessa seduta, entrambe devono essere sufficienti):
> - **Quiz teorico (40%)** — 30-40 domande vero/falso o scelta multipla, 45 min, **nessun materiale**, penalità per risposta sbagliata. Copre tutto il programma, inclusi i comandi visti in lab.
> - **Prova pratica (60%)** — 2 ore, esercizi lab offensivi e difensivi, materiale consentito.
> **Esame SysAdmin**: prova pratica su PC del lab. VM a tua cura.

---

## Prossimi Passi

> ✅ **Diritto chiuso** (16/06, **30 e lode**). 🚨 **Focus 18/06 → 17/07**: chiudere **Security da 0%** + **SysAdmin residuo** per la coppia **Sistemi 15/07** + **Security 17/07**. Ritmo ~5h/gg costanti (~4h Security + ~1.5h SysAdmin). Security è il collo di bottiglia: i LAB su VM vanno eseguiti giorno per giorno, non accumulati.

**Security** (carico dominante) → S1 ✅, S2 ✅, S3 ✅, S4 🔄 LAB in corso sulla VM. **Es1 `write_var` ✅** fatto (padding 104, payload `"A"x104,"EDCB"`, flag presa). **Riprendere dall'es2 `secret_function`**: ho già trovato offset 16 + indirizzo `secret` = `0x565561ad` con `info functions secret`; manca **lanciare il payload** dentro gdb: `run $(perl -e 'print "A"x16,"\xad\x61\x55\x56"')` → deve uscire la flag; poi riprovare **fuori** da gdb con `./es`. Quindi es2-variante remote → es3 shellcode/root shell → es4 ret2libc. Annotare inline nella guida. DRILL finale: `SIMULAZIONI ESAMI/SICINF/Binary_exploitation.html`. Poi S5.
**SysAdmin** (in parallelo) → **3D**: lezione ✅, guida_lab ✅ (appena creata). Prossimo passo: avvia VM (`cd ~/Progetti/sysAdmin-lab && vagrant up --provider=virtualbox && vagrant ssh`), segui `guida_lab_modulo3D_networking_base.md` Es. 1–6, annota inline, poi `/appunti 3D` per la parte teorica dai grezzi. Poi: 3E → 3F → 4B → 4C. Guida_lab 0A–2B da rifare a bassa priorità.

---

## Scadenze Esami

| Esame | Data | Ora |
|-------|------|-----|
| ~~Diritto dell'Informatica T~~ | ✅ 16/06/2026 — **30 e lode** | — |
| Lab Amministrazione di Sistemi T | **15/07/2026** | 14:00 |
| Lab Sicurezza Informatica T | **17/07/2026** | 14:00 |

Piano fasi e stime ore dettagliate: `ESAMI SCELTI.md`
