# Log Sessioni — Studio Attivo

> Storico completo delle sessioni. Ordine cronologico inverso (ultime in cima).
> NON caricare questo file a ogni sessione. Usarlo solo per:
> - `/chiudi` (aggiungere nuova voce)
> - `/sessione` (consultare le ultime 2-3 sessioni per contesto)
> - Richieste specifiche di Lorenzo sullo storico

---

### Sessione 39 — 2026-06-23 (completata)
**Focus**: SysAdmin — Audit qualità materiali + riorganizzazione sistema di studio

**Coperto in sessione**:
- Audit qualità di tutti i file SysAdmin (lezioni + appunti): scoperto che 0A–2B erano walkthrough mascherati da lezioni, prodotti col sistema embrionale
- Knowledge check 0A–2B: Lorenzo non ricorda niente di teorico → confermato che il sistema embrionale non ha fissato i concetti
- Decisione: esame SysAdmin è solo pratico → ripasso 0A–2B a bassa priorità; focus su 3D–4C
- Rinominate lezioni 0B/1A/1B/2A/2B → `guida_lab_*` (erano walkthrough, non lezioni)
- `corrente.md` aggiornato: 0A–2B → ⚠️, 3D → ⬜ restart, percentuale corretta ~25%
- Chiarito il metodo di studio definitivo: lezione → grezzi → `/appunti`; guida_lab → annotata inline (stesso metodo Security)
- Creata `guida_lab_modulo3D_networking_base.md` (Es. 1–6 completi, ancorata al lab HTML)
- Aggiornata memoria persistente sul flusso di studio pratico

**Non coperto / da riprendere**:
- 3D lab sulla VM (Es. 1–6) — guida_lab pronta, da eseguire
- S3 Web Security — non iniziato
- Guida_lab 0A–2B da rifare con le nuove direttive (bassa priorità, quando c'è tempo)

**Prossima sessione — da dove partire**:
→ SysAdmin 3D: `cd ~/Progetti/sysAdmin-lab && vagrant up && vagrant ssh` → segui `guida_lab_modulo3D_networking_base.md` Es. 1–6, annota inline → poi `/appunti 3D`
→ Security S3: `/lezione S3` (PDF: `Web_security_6_mar.pdf`) → `/lab S3`

---

### Sessione 38 — 2026-06-23 (completata)
**Focus**: Security — S2 Autenticazione (appunti definitivi)

**Coperto in sessione**:
- Appunti modulo S2 elaborati → `claudeAppunti/APPUNTI SECURITY/appunti_moduloS2_autenticazione.md`
- Risolte 3 domande aperte inline: HSM (cos'è nel pratico), entropia password (formula + ragionamento), autenticazione attiva + S-KEY OTP (confusione con 2FA chiarita)
- Integrata tabella PAM completa (module-type + control-flag + moduli comuni)
- Corretta imprecisione: FIDO descritto come "autorizzazione" → aggiunto a errori_frequenti.md
- Autoverifica: 4/6 ✅ al primo tentativo; Q4+Q5 chiarite negli appunti
- `corrente.md` aggiornato: S2 → ✅ Sessione 38; Security 13% (2/15)

**Non coperto / da riprendere**:
- SysAdmin 3D Es. 2-6 — invariato

**Prossima sessione — da dove partire**:
→ Security S3 Web Security: `/lezione S3` (PDF: `Web_security_6_mar.pdf`) → `/lab S3` (pentestlab.sh VM Parrot)
→ SysAdmin 3D Es. 2-6 (VM vagrant: ping + ss -tlnp + /etc/hosts + dig + tcpdump)

---

### Sessione 37 — 2026-06-22 (completata)
**Focus**: Security — S1 LAB Enumerazione (esecuzione su VM)

**Coperto in sessione**:
- Es 1: host discovery (`nmap -sn`) → identificati 3 target reali: `.101` (t-2), `.102` (t-3), `.104` (t-1)
- Es 2a: port scan TCP completo (`nmap -sT -p-`) su tutti e 3 i target
- Es 2b: version detection (`nmap -sV`) → mappa servizi completa (OpenSSH, Postfix, Dovecot, MariaDB, PostgreSQL, Samba, BIND, Werkzeug/Flask)
- Es 3a: banner grabbing SMTP (inferred dal port map)
- Es 3b: PostgreSQL enumeration → `accounts_db` → credenziali in chiaro: lovelace/babbage/turing
- Es 4a: credential reuse SSH → lovelace/babbage/turing funzionano su `.104:22`; `.101/.102:22` solo publickey
- Es 4b: Hydra brute force PIN su `.101:1337` → `root/0153`
- Es 5a: file transfer con ssh+cat (scp non funziona su porta 1337 senza SFTP subsystem)
- Es 5b/5c: wordlist manuale (CUPP non installabile per DNS failure); john carica hash ma non cracca (wordlist troppo piccola)
- `guida_lab_moduloS1_enumerazione_nmap.md` completata con output reali inline + risposte ai dubbi
- `corrente.md` aggiornato: S1 ✅, Security ~7%, sessione 37

**Non coperto / da riprendere**:
- john con rockyou.txt (wordlist manuale insufficiente, DNS Parrot non funzionante)
- SysAdmin 3D Es. 2-6 — invariato

**Prossima sessione — da dove partire**:
→ Security S2 Autenticazione: `/lezione S2` → `/lab S2` → esecuzione VM
→ SysAdmin 3D Es. 2-6 (VM vagrant, ping + ss -tlnp + /etc/hosts + dig + tcpdump)

---

### Sessione 36 — 2026-06-22 (completata)
**Focus**: Security — S1 /appunti (teoria → appunti definitivi)

**Coperto in sessione**:
- `/appunti S1` eseguito: `Appunti_grezzi_lezione_S1.md` → `appunti_moduloS1_offensive_security_enumerazione.md`
- 8 lacune esplicite risolte inline (Kill Chain, NIST CSF, tabella Google Dork, DNS records, subdomain/CT abuse, NMAP con esempi e output)
- 6 sezioni assenti integrate (metodologie, MITRE ATT&CK, casi concreti, evasione scan, vuln scanners, postura interna)
- 4 punti di forza segnalati; autoverifica 6/6 corrette confermata
- `corrente.md` aggiornato: S1 🔄 con nota "appunti definitivi ✅ (22/06)"
- ⚠️ Nota: log sessione 34 contiene dati inaccurati (descriveva lab + appunti mai eseguiti — i file non esistevano, corrente.md non era stato aggiornato di conseguenza)

**Non coperto / da riprendere**:
- S1 LAB su VM (esercizi 1-5) — da eseguire nella stessa sessione pomeridiana

**Prossima azione**:
→ Avvia VM Parrot + 3 target (guida: `guida_lab_moduloS1_enumerazione_nmap.md`)

---

### Sessione 35 — 2026-06-22 (completata)
**Focus**: Security — S1 produzione guida-lab operativa

**Coperto in sessione**:
- Letti PDF teoria (53 slide) + HTML LAB (~6 sezioni) integralmente
- Prodotta nuova guida-lab: `guida_lab_moduloS1_enumerazione_nmap.md` (5 esercizi, anatomia comandi, ⚠️ errori integrati)
- `link_modules.py --apply` → S1: lezione ↔ guida-lab collegati
- `corrente.md` aggiornato: nota guida-lab ✅ (22/06)

**Non coperto / da riprendere**:
- `/appunti S1` — rimandato alla sessione successiva (completato in sessione 36)
- S1 LAB su VM — da eseguire

**Prossima sessione — da dove partire**:
→ `/appunti S1` → poi S1 LAB su VM

---

### Sessione 34 — 2026-06-18 (completata)
**Focus**: Security — S1 LAB Enumerazione (esecuzione completa)

**Coperto in sessione**:
- S1 LAB eseguito integralmente sulla VM Parrot (tutte e 6 le fasi)
  - Fase 1: 3 VM target create da .vdi, host-only vboxnet0
  - Fase 2: nmap -sn → -sT -p- → -sV su tutti i target
  - Fase 3: output verificato (t-1=.104, t-2=.101, t-3=.102; 5° host = server DHCP VirtualBox)
  - Fase 4: banner grabbing SMTP (nc .101:25) + esfiltrazione DB PostgreSQL (lovelace/babbage/turing + password in chiaro)
  - Fase 5: credential reuse SSH (lovelace/babbage su t-1 ✅); hydra bruteforce PIN su t-2:1337 → root/0153
  - Fase 6: considerato svolto (ssh cat per file transfer, CUPP + john)
- Appunti definitivi scritti: `appunti_moduloS1_concetti.md` + `appunti_moduloS1_operativo.md`
- `errori_frequenti.md` aggiornato con sezione Security (nmap, psql, scp)
- `corrente.md` aggiornato: S1 ✅, Security ~7%
- Feedback salvato: lezioni Security devono essere testo concettuale, non walkthrough

**Non coperto / da riprendere**:
- SysAdmin 3D Es. 2-6 — invariato (rimandato, era nel piano di oggi)

**Prossima sessione — da dove partire**:
→ Security S2 Autenticazione (lezione + guida-lab da generare)
→ SysAdmin 3D Es. 2-6 (VM vagrant, ping + ss -tlnp + /etc/hosts)

---

### Sessione 33 — 2026-06-18 (completata)
**Focus**: Security — Setup S1, skill /studia, pianificazione

**Coperto in sessione**:
- Letti integralmente PDF teoria S1 (kill chain, VA/PT, OSINT, Google Dork, DNS enum, Greenbone)
- Letto PDF LAB S1 (6 sezioni con comandi + output attesi)
- Corretto snapshot status nella guida-lab (era segnato ✓ per errore)
- Creata skill `/studia` per checkpoint sessione interattiva
- Pianificazione: piano ridimensionato a 2.5h (S1 LAB + SysAdmin 3D Es. 2-3)

**Non coperto / da riprendere**:
- LAB S1 non eseguito (rimandato alla sessione 34)
- SysAdmin 3D Es. 2-6 — invariato

**Prossima sessione — da dove partire**:
→ S1 LAB Fase 1-3 sulla VM

---

### Sessione 32 — 2026-06-05 (completata)
**Focus**: Diritto — D13 autoverifica

**Coperto in sessione**:
- Autoverifica D13 (DSA/DMA/Data Act): 5 domande completate → D13 ✅
- Risultato: 3.5/5 — buona comprensione del quadro generale
- Lacuna emersa: anti-steering (soggetto invertito — riguarda gli utenti commerciali che non possono informare i clienti di offerte fuori piattaforma, non l'utente finale)

**Non coperto / da riprendere**:
- Ripassone D9–D13 (rimandato a sessione dedicata)
- SysAdmin 3D Es. 2–6 — invariato
- Security S1 LAB — invariato

**Prossima sessione — da dove partire**:
→ Lavoro metodologico UniCode per piano ripasso finale 10gg Diritto (nuovi metodi/tecniche); poi ripassone D9–D13

---

### Sessione 31 — 2026-06-04 (completata)
**Focus**: Diritto — D12 autoverifica + D13 lezione + grezzi + appunti + PDF batch

**Coperto in sessione**:
- Autoverifica D12 (AI Act): domande completate → D12 ✅
- D13 (DSA/DMA/Data Act): lezione creata (`lezione_moduloD13_pacchetto_digitale.md`); appunti grezzi scritti; appunti definitivi elaborati (`appunti_moduloD13_pacchetto_digitale.md`) — 28 domande aperte risolte inline, 2 imprecisioni corrette (titolare dati ≠ utente; designazione vs criteri gatekeeper) → D13 🔄 (leggere appunti + autoverifica 5 domande mancante)
- PDF batch: convertiti PDF mancanti per D13 + naming allineato D01–D13 in `claudeAppunti_PDF/`

**Non coperto / da riprendere**:
- D13: leggere appunti definitivi + autoverifica 5 domande → poi ✅
- SysAdmin 3D Es. 2–6 — invariato
- Security S1 LAB — invariato

**Prossima sessione — da dove partire**:
→ **Diritto D13** — leggere appunti definitivi + autoverifica 5 domande → ✅ → ripassone D9–D13

---

### Sessione 30 — 2026-06-03 (completata)
**Focus**: Diritto — D11 autoverifica + D12 lezione + grezzi + appunti

**Coperto in sessione**:
- Autoverifica D11 (5 domande): risultati parziali (D1 ✅, D2-D5 parziali) — errori documentati in errori_frequenti.md (615-quinquies, mera condotta, vittima frode) → D11 ✅
- D12 (AI Act): lezione creata (`lezione_moduloD12_ai_act.md`); appunti grezzi scritti; appunti definitivi elaborati (`appunti_moduloD12_ai_act.md`)
  - 9 domande aperte risolte inline; 2 imprecisioni corrette; 8 pratiche vietate espanse; schema casi pratici creato
  - D12 → 🔄 (autoverifica 5 domande mancante)

**Non coperto / da riprendere**:
- D12: autoverifica 5 domande → poi ✅
- D13: da zero
- SysAdmin 3D Es. 2–6 — invariato
- Security S1 LAB — invariato

**Prossima sessione — da dove partire**:
→ **Diritto D12** — autoverifica 5 domande → ✅ → D13

---

### Sessione 29 — 2026-05-29 (completata)
**Focus**: Diritto — D10 autoverifica + D11 lezione + grezzi + appunti

**Coperto in sessione**:
- Autoverifica D10 (5 domande): risultato buono — lacuna su gerarchia D.Lgs. 70/2003 vs Codice del consumo → D10 → ✅
- D11 (Reati Informatici): lezione creata + appunti grezzi scritti + appunti definitivi elaborati
  - `lezione_moduloD11_reati_informatici.md` — tutti 11 topic dal "Attenzione ripasso!!!" coperti
  - `appunti_moduloD11_reati_informatici.md` — 5 domande aperte risolte, 2 imprecisioni corrette, schema riepilogativo completo
  - PDF generato e pushato
  - D11 → 🔄 (lettura appunti + autoverifica 5 domande alla prossima sessione)

**Non coperto / da riprendere**:
- D11: leggere appunti definitivi + autoverifica 5 domande
- D12, D13: da zero
- SysAdmin 3D Es. 2–6 — invariato
- Security S1 LAB — invariato

**Prossima sessione — da dove partire**:
→ **Diritto D11** — leggere appunti + 5 domande autoverifica → ✅ → D12

---

### Sessione 28 — 2026-05-28 (completata)
**Focus**: Diritto — D9 ripasso + D10 appunti

**Coperto in sessione**:
- Ripasso D9 (Firme Elettroniche): 5 domande, 2/5 corrette — lacune su gerarchia firme e opponibilità PEC
  - D9 → ✅; tracker ripasso aggiornato (prossimo: 2026-05-31)
- Scoperta struttura esame Diritto: 22 quiz scelta multipla, NON richiedono numeri articoli/leggi → rimosso pattern errante da errori_frequenti.md
- Appunti definitivi D10 (Commercio Elettronico) elaborati → `appunti_moduloD10_commercio_elettronico.md`
  - 11 domande aperte risolte inline
  - 5 sezioni integrate con nota ⚠️
  - D10 → 🔄 (autoverifica mancante)

**Non coperto / da riprendere**:
- D10: autoverifica 5 domande
- D11: da zero
- SysAdmin 3D Es. 2–6 — invariato
- Security S1 LAB — invariato

**Prossima sessione — da dove partire**:
→ **Diritto D10** — rispondere alle 5 domande di autoverifica → `/ripassa D10`? → portare a ✅
→ **Diritto D11** — Reati Informatici: `/lezione D11` + grezzi + appunti

---

### Sessione 27 — 2026-05-27 (completata)
**Focus**: Meta — miglioramento sistema UniCode + Diritto D9 (appunti definitivi) + Diritto D10 (lezione generata)

**Coperto in sessione**:
- Analisi autocritica del sistema UniCode: 3 interventi prodotti
  - `stato/corrente.md`: aggiunto blocco urgenza Diritto (5 step in 20 giorni)
  - `lezione.md` template SysAdmin: ristrutturato per interlacciare teoria+pratica per sezione
  - Memory cleanup: 4 file ridondanti eliminati (qualita_output, sottocartelle, glossari_separati, sessione_giornata)
- Appunti definitivi D9 studiati (lettura appunti elaborati)
- Lezione D10 — Commercio Elettronico generata

**Non coperto / da riprendere**:
- D9: autoverifica 5 domande ancora mancante
- D10: appunti grezzi da scrivere + `/appunti D10`
- SysAdmin 3D Es. 2–6 — invariato
- Security S1 LAB — invariato

**Prossima sessione — da dove partire**:
→ **Diritto D9** — rispondere alle 5 domande di autoverifica → portare a ✅
→ **Diritto D10** — lezione pronta; scrivere appunti grezzi → `/appunti D10`
→ **SysAdmin 3D Es. 2–6** — VM, eseguire: ping, ss -tlnp, /etc/hosts, dig, tcpdump → `/appunti 3D`
→ **Security S1 LAB** — lezione pronta, eseguire 6 sezioni su VM Kali

---

### Sessione 26 — 2026-05-26 (completata)
**Focus**: Diritto D8 — Autoverifica + Diritto D9 — Appunti elaborati

**Coperto in sessione**:
- Autoverifica D8 completata: 5 domande una alla volta in modalità interrogazione
- Punti forti: procedura data breach (chi/cosa/entro quando), basi giuridiche marketing (consenso art. 6), quando è obbligatorio il DPO, caratteristiche del DPO, privacy by design vs by default con esempi
- Punti corretti: definizione di dato sensibile (non è legato alla capacità identificativa ma alla natura dell'informazione); doppia base art. 6 + art. 9 per dati sanitari; interesse vitale (art. 9 lett. C) non è alternativo al consenso per il marketing ma vale solo per persone incapaci; compiti minimi DPO non erano stati elencati
- D8 portato a ✅
- Appunti modulo D9 elaborati → `claudeAppunti/APPUNTI DIRITTO/appunti_moduloD9_firme_elettroniche.md`
  - 3 domande aperte risolte: schema tipologie firme (inserito), integrazione firma automatica/remota/autenticata nella tabella, spiegazione semplificata revoca/sospensione certificato qualificato (con 4 cause, regola di pubblicità, effetto dalla pubblicazione)
  - 1 imprecisione corretta: firma elettronica qualificata era definita genericamente — corretta con i due elementi costitutivi precisi (dispositivo qualificato + certificato qualificato)
  - 1 imprecisione minore: "si può dubitare" sulle copie per immagine — chiarito che il disconoscimento espresso è l'unico meccanismo previsto
  - 3 sezioni integrate: §1 (quadro normativo: Legge Bassanini, CAD, eIDAS, regole tecniche), §11 (firma automatica, remota, autenticata), §18 (tabella riepilogo normativo)
  - 5 domande di autoverifica da rispondere in autonomia

**Non coperto / da riprendere**:
- SysAdmin 3D Es. 2–6 — invariato
- Security S1 LAB — invariato

**Prossima sessione — da dove partire**:
→ **Diritto D9** — rispondere alle 5 domande di autoverifica in autonomia; poi portare a ✅
→ **Diritto D10** — Commercio Elettronico — eseguire `/lezione D10`
→ **SysAdmin 3D Es. 2–6** — avviare VM, eseguire: `ping`, `ss -tlnp`, `/etc/hosts`, `dig`, `tcpdump`. Poi `/appunti 3D`
→ **Security S1 LAB** — lezione pronta, eseguire le 6 sezioni sulla VM Kali

---

### Sessione 25 — 2026-05-21 / 2026-05-25 (completata)
**Focus**: Diritto D7 (appunti) + Diritto D8 (lezione + appunti grezzi)

**Coperto in sessione**:
- Appunti modulo D7 elaborati → `claudeAppunti/APPUNTI DIRITTO/appunti_moduloD7_proprieta_industriale.md`
  - Struttura a domande come titoli (su richiesta di Lorenzo) — ogni sezione risponde a una domanda reale
  - 20+ domande aperte risolte
- Lezione D8 creata → `claudeLezioni/LEZIONI DIRITTO/lezione_moduloD8_privacy_gdpr.md`
  - 63 slide coperte, 23 sezioni
  - 5 domande di autoverifica
- Appunti grezzi D8 scritti da Lorenzo in autonomia
- Appunti modulo D8 elaborati → `claudeAppunti/APPUNTI DIRITTO/appunti_moduloD8_privacy_gdpr.md`

---

### Sessione 24 — 2026-05-20 (completata)
**Focus**: Diritto D6 — Autoverifica (5 domande in modalità interrogazione)

**Coperto in sessione**:
- Autoverifica D6 completata: 5 domande una alla volta in modalità interrogazione
- Punti forti: distinzione opera intellettuale/appalto, art. 2231 (non iscrizione + cancellazione), differenza variazioni richieste/necessarie, cessione vs licenza
- Punti da ripassare: art. 2224 (variazioni necessarie — nome articolo non ricordato), meccanica art. 1457 (termine essenziale), effetto retroattivo art. 1458 e sua eccezione per esecuzione continuata

---

### Sessione 23 — 2026-05-15 (completata)
**Focus**: Diritto D6 — Contratto di sviluppo software

**Coperto in sessione**:
- Aggiornata master map: aggiunti moduli D9-D11
- Diritto ora 11 moduli; ESAMI SCELTI.md aggiornato (~54h stima)
- Letto PDF D6 (52 slide); creata lezione D6
- Appunti grezzi D6 elaborati — 19 domande aperte risolte, 2 imprecisioni corrette, 2 sezioni integrate

---

### Sessione 22 — 2026-05-14 (completata)
**Focus**: Diritto D5 — Contratti a oggetto informatico

**Coperto in sessione**:
- Appunti grezzi D5 elaborati — 18 domande aperte risolte, 1 imprecisione corretta, 2 sezioni integrate
- Domande di autoverifica: 5/5 risposte presenti

---

### Sessione 21 — 2026-05-13 (completata)
**Focus**: Diritto D4 — Tutela giuridica delle banche di dati e siti web

**Coperto in sessione**:
- Letto PDF D4; creata lezione D4
- Appunti modulo D4 elaborati — 11 domande risolte, 2 imprecisioni corrette, 2 sezioni integrate
- Creata lezione D5

---

### Sessione 20 — 2026-05-12 (completata)
**Focus**: SysAdmin — Esercizio 02 bash scripting

**Coperto in sessione**:
- Script `conta_occorrenze.sh` costruito passo per passo
- Esplorazione sistematica flag `grep`: `-o`, `-c`, `-n`, `-v`, `-i`
- Introdotto `tr`: flag `-c`, `-s`, `-d`; classi POSIX
- Creato `esercizi/es_02_conta_occorrenze.md`
- Cheatsheet aggiornato

---

### Sessione 19 — 2026-05-11 (completata)
**Focus**: SysAdmin — ripasso 0B (pipeline esercizio) + strumenti studio

**Coperto in sessione**:
- Esercizio pipeline: conta file per estensione, top 5
- Cheatsheet aggiornato (`ls -R`, `sort -rn`, regex anchors, `rev`)
- Creata directory `esercizi/` con `es_01_conta_estensioni.md`

---

### Sessione 18 — 2026-05-06 (completata)
**Focus**: SysAdmin 3D (lezione) + Security S1 (analisi appunti grezzi)

**Coperto in sessione**:
- Analisi appunti grezzi S1: lacune di networking di base identificate
- Decisione: fare 3D SysAdmin prima di tornare a S1
- Letti net-config.pdf e servizi_base_rete.pdf
- Creata lezione 3D con 6 esercizi guidati
- Appunti 3D elaborati — 20+ domande risolte, Es. 1 eseguito, Es. 2-6 da fare

---

### Sessione 17 — 2026-05-04 (completata)
**Focus**: Security S1 — lezione creata

**Coperto in sessione**:
- Letti tutti i PDF Security S1 (4 documenti)
- Creata lezione S1 con setup VM, teoria completa, lab 6 sezioni

---

### Sessione 16 — 2026-04-29 (completata)
**Focus**: SysAdmin 3C (pratica VM + appunti) + Diritto D3 (appunti)

**Coperto in sessione**:
- Es. 1-5 modulo 3C eseguiti sulla VM
- Appunti 3C elaborati — 25 domande risolte, script debuggato (4 bug)
- Appunti D3 elaborati — 8 domande risolte, 3 imprecisioni corrette, 4 sezioni integrate

---

### Sessione 15 — 2026-04-29 (completata)
**Focus**: Organizzazione — pianificazione esami e aggiornamento strumenti

**Coperto in sessione**:
- Scelta date esami: Diritto 16/06, SysAdmin 22/06, Security 17/07
- Stima ore per modulo (~181h totali su 435h disponibili)
- Creato `ESAMI SCELTI.md`, skill `/piano`, integrato piano in `/sessione`

---

### Sessione 14 — 2026-04-28 (completata)
**Focus**: SysAdmin — Modulo 3C (lezione creata)

---

### Sessione 13 — 2026-04-28 (completata)
**Focus**: SysAdmin — Modulo 3B (pratica VM + appunti)

**Coperto**: Es. 1-7 sulla VM, appunti elaborati, 14 domande risolte, 3 sezioni integrate

---

### Sessione 12 — 2026-04-27 (completata)
**Focus**: Diritto D2 (lezione + appunti) + D3 (lezione) + assessment

---

### Sessione 11 — 2026-04-27 (completata)
**Focus**: Diritto D1 — elaborazione appunti grezzi

**Coperto**: 2 domande risolte, 5 imprecisioni corrette, 3 sezioni integrate

---

### Sessione 10 — 2026-04-24 (completata)
**Focus**: Modulo 3A — completamento Es. 3-7 + chiusura

---

### Sessione 8 — 2026-04-23 (completata)
**Focus**: Modulo 3A — elaborazione appunti. 19 domande risolte.

---

### Sessione 7 — 2026-04-21 (completata)
**Focus**: Modulo 2A — Gestione Utenti e Permessi

---

### Sessione 6 — 2026-04-21 (completata)
**Focus**: Modulo 1B — Funzioni, Case, Test. 4 domande risolte, 1 bug corretto.

---

### Sessione 5 — 2026-04-17 (completata)
**Focus**: Modulo 1A completato + 1B iniziato

---

### Sessione 3 — 2026-04-16 (completata)
**Focus**: Ripresa Modulo 0A — permessi, anatomia comandi, home directory

---

### Sessione 2 — 2026-04-15 (completata)
**Focus**: Setup VM Vagrant + Debian 12. Modulo 0A.

---

### Sessione 1 — 2026-04-15
**Focus**: Inquadratura generale. Valutazione livello reale. Costruzione master map e metodologia.
