# Stato Corrente — Studio Attivo
**Sessione**: 52 | **Aggiornato**: 2026-07-15

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
| S5 | Firewall + packet filter + LAB | ⭐ **Iptables/NFTables** | ✓ | 🔄 lezione ✅, appunti ✅, guida-lab ✅ (9 esercizi); Es1 (endpoint INPUT/OUTPUT) ✅ ed Es2 (FORWARD su R1) ✅ eseguiti su VM (sessione 46) — Es3-9 ancora da fare. **Sessione 52 (15/07)**: aperto il binario "pool esami" anche per questa tipologia (come già fatto per NIDS/privesc) — pool Iptables/NFTables **7/7 casi catalogati con soluzione ufficiale** (agente background, `modello_iptables_nftables.md`), creati `procedura_operativa_iptables.md` + `guida_esame_iptables.md` + due template riusabili (`template_ipt-router.md`, `template_ipt-endpoint.md`). **Esercizio pool 13/06/2024 (Router+Server+NAT) risolto e verificato contro soluzione ufficiale** — `ipt-router.sh`/`ipt-server.sh` scritti da Lorenzo con guida passo-passo (chain FORWARD vs INPUT/OUTPUT, ragionamento su interfacce, SNAT per attraversamento privato→pubblico), non lanciati su una VM multi-host reale (la consegna richiede solo i file di script corretti). Materiali in ulteriore rifinitura da un agente Opus lanciato a fine sessione. |
| S6 | Sicurezza fisica e cloud | — | ✓ | ⬜ |
| S7 | LAB Backdoor injection | (privesc) | ✓ | ⬜ |
| S8 | LAB Individuare e filtrare attacchi | (NIDS/privesc) | ✓ | ⬜ |
| S9 | Demoni + Autorizzazione + PAM | (privesc) | ✓ | ⬜ |
| S10 | Rilevare attacchi + LAB NIDS Suricata | ⭐ **Network Intrusion Detection** | ✓ | ✅ Sessione 48 (10-13/07) — **3 esercizi reali completati hands-on sulla VM**: 13/02/2025 (HTTP flood, sessione 47), 11/01/2024 (port scan+SSH+Telnet flag+DDoS, confrontato con soluzione ufficiale), 10/07/2025 (buffer-overflow SMTP a padding incrementale). Guida operativa `guida_esame_NIDS.md` rivista ed estesa più volte con le lezioni pratiche di ogni esercizio. Nessuna lezione/appunti teorici formali ancora (scelta deliberata, "esercizi prima teoria dopo") — ARP (2 varianti nel pool) non ancora praticato hands-on |
| S11 | HIDS + LAB Misconfiguration + LAB Pentesting target | ⭐ **Integrity/privesc** | ✓ | 🔄 Sessioni 49-52 (13-15/07) — **3 esercizi reali completati hands-on sulla VM**: 9 gennaio 2023 (`change1`, SUID su `cp`, sessione 49), 11 gennaio 2024 (`change4`, capability `cap_dac_override` su `tee`, sessione 51), e una variante `change5` (11/01/2024, fatta autonomamente da Lorenzo senza assistenza diretta di Claude, confermata come valida in sessione 52 — deliverable in `esercizi/SICINF/privesc_2026-07-14_change5/`, screenshot presente, `integrity.txt` non scritto separatamente ma esercizio contato come completato). `guida_esame_privesc.md`: **audit di autosufficienza confermato completo** in sessione 52 (verificati nel file tutti e 5 i gap corretti: sintassi `/usr/bin f Full`, §4.6 pipe-vs-redirect, bug formato passwd 6→7 campi, prerequisito AIDE non preinstallato, nota rockyou.txt gzippata — valutazione agente: sì con alta confidenza). Nessuna lezione/appunti teorici formali ancora (scelta deliberata, "esercizi prima teoria dopo") — restano da praticare altre varianti del pool (`change2,3,6,7,8,9`, caso 12 gennaio 2026 già documentato in `modello_integrity_privesc.md` ma non hands-on) e i due lab dedicati (misconfiguration, HIDS/AIDE) letti ma non eseguiti |
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
Security  ███░░░░░░░  ~33%  (5/15 moduli ✅ + S5/S11 🔄 — S1 22/06, S2 23/06, S3 26/06, S4 02/07, S10 13/07 — 5/5 tipologie ⭐ d'esame toccate: S3,S4,S10 ✅, S5 parziale (Es1-2 VM + pool 7/7 catalogato, 1 esercizio pool risolto 15/07), S11 3/9 varianti pool 13-15/07)
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
>
> **Aggiornamento 13/07 (sessione 50)**: consegna dell'agente ricevuta e verificata — pool S11 ora **9/9 esercizi catalogati** in `modello_integrity_privesc.md` (610 righe; 6/7 nuovi con soluzione ufficiale completa, 1 — 15/06/2023 — ricostruito per analisi statica, segnalato come non ufficiale). Creati anche `procedura_operativa_privesc.md` (checklist operativa) e `guida_esame_privesc.md` (triage + un ramo per vettore: SUID, capabilities, ACL, sudoers, cracking password, persistenza cron/at/systemd, decoy). Nessun nuovo lavoro hands-on sulla VM in questa chiusura — solo la materiale di riferimento è pronto per la prossima sessione pratica.
>
> **Aggiornamento 14/07 (sessione 51)**: **secondo esercizio reale della famiglia completato** — `change4` (11 gennaio 2024), vettore capability `cap_dac_override` su `/usr/bin/tee` (diverso da `change1`: qui niente SUID, 4 file nel diff AIDE di cui 3 vicoli ciechi verificati singolarmente — `grep` capability svuotata/falso positivo, `vim.tiny` privilegio tolto non dato, `/etc/sudoers` solo ctime/rumore — e 1 vettore reale). Creato utente `hack` con password `hack` e UID/GID 0 scrivendo `/etc/passwd` via `tee` (bypassa i permessi Unix grazie alla capability), root verificato con `id`. Deliverable (`integrity.txt` + `privesc.png`) in `esercizi/SICINF/privesc_2026-07-14_change4/`.
> **Scoperta di processo importante**: i deliverable degli esercizi con revert a snapshot pulito (come questa famiglia) venivano **persi ad ogni ripristino** — successo così con `change1` di sessione 49 (mai trovato nel repo). Fix adottato da questa sessione in poi: screenshot catturati **da Claude sull'host** con `grim` nel momento della prova, `integrity.txt` scritto in tempo reale nel repo via via che Lorenzo incolla l'output — mai più lasciato solo dentro la VM. Dettagli in `troubleshooting_vm.md` (sezioni AIDE + Snapshot VirtualBox) e memoria auto-persistente `feedback_deliverable_vm_revert`.
> Risolto anche un problema di gestione snapshot (GUI VirtualBox poco chiara per il ripristino — fix: `VBoxManage` da riga di comando) e un errore di sintassi in `aide.conf` (`/usr/bin -f Full` con trattino errato, va senza trattino).
> **Lanciato un agente Opus in background** per un audit di autosufficienza di `guida_esame_privesc.md`: la domanda posta è "uno studente saprebbe risolvere QUALSIASI esercizio di questa famiglia usando solo questo file (+ i suoi rimandi), senza altro aiuto?" — l'agente doveva rivedere/correggere il file finché la risposta fosse sì con alta confidenza, includendo almeno due punti già noti da sistemare (sintassi esatta della regola AIDE; il perché serva una pipe verso un binario privilegiato — es. `tee` — invece di un redirect diretto sul file protetto). **Esito verificato in sessione 52**: confermato completo, tutti e 5 i gap presenti e corretti nel file.
>
> **Aggiornamento 15/07 (sessione 52)**: verificato e chiuso il punto in sospeso di sessione 51 (audit privesc confermato) e contata come fatta la variante `change5` di S11 (eseguita autonomamente da Lorenzo). Con **2 giorni all'esame**, aperto lo stesso schema "pool + template" già usato per NIDS/privesc anche sulla **terza tipologia rimasta, Iptables/NFTables (S5)**: pool completo catalogato (7/7 casi con soluzione ufficiale), creati `guida_esame_iptables.md` + `procedura_operativa_iptables.md` + due template riusabili (`template_ipt-router.md`, `template_ipt-endpoint.md`, quest'ultimo copre sia Client che Server). Risolto hands-on (a mano, non su VM multi-host — la consegna richiede solo gli script corretti) l'esercizio **13/06/2024** (Router+Server+NAT): scoperto e corretto un errore concettuale reale a metà esercizio (regola scritta in FORWARD per traffico che in realtà terminava sul router, dovrebbe essere INPUT/OUTPUT) e un requisito di NAT/SNAT inizialmente non individuato (segnale "rete privata verso segmento senza instradamento di ritorno", non solo la parola "indiretto" — ora documentato in `procedura_operativa_iptables.md` §2). Sessione lunga e faticosa (Lorenzo ha segnalato stanchezza a fine sessione): partita da zero assoluto sui concetti di topologia/interfacce/chain, con correzioni di comprensione progressive. **Lanciato un secondo agente Opus in background** a fine sessione per consolidare tutti i chiarimenti emersi nei file `guida_esame_iptables.md`/`procedura_operativa_iptables.md`/i due template, in modo che siano autosufficienti "a mente spenta" il giorno dell'esame. **Esito arrivato a sessione chiusa**: completato, 4 dei 5 file aggiornati (non `modello_iptables_nftables.md`, nessun errore trovato). Aggiunte principali: sezione "da dove viene ogni pezzo di una regola" (consegna/disegno/metodo-fisso) in `procedura_operativa_iptables.md` §0.5; traccia SNAT+conntrack pacchetto-per-pacchetto; generalizzazione del filtro post-NAT a SNAT oltre DNAT; discriminante "quando privato→privato NON serve SNAT" (default gateway comune); DHCP aggiunto come secondo servizio a porte fisse oltre NTP; esempio concreto dell'errore FORWARD/INPUT nel template router; `nat -F` reso passaggio obbligatorio esplicito; mini-schema del caso webserver 2-interfacce/0-FORWARD nel template endpoint. Nessuna azione richiesta: i materiali sono pronti per l'uso. Con 2 giorni residui, priorità suggerita per la prossima sessione: ripasso leggero (non nuovo materiale pesante) + verifica dei materiali di riferimento delle 5 tipologie, dato il poco tempo e la stanchezza accumulata a fine sessione 52.

**Security** (focus esclusivo) → S1 ✅, S2 ✅, S3 ✅, **S4 ✅ chiuso (sessione 45, 02/07)** — LAB completo tutti e 4 gli esercizi. **Es1 `write_var` ✅**, **es2 `secret_function` ✅** (offset 16, ASLR/reboot gotcha in `troubleshooting_vm.md`), **es2b `secret_function_remote` ✅** (fix `gets()` non dichiarata dalle glibc moderne, esposizione in rete con `ncat` installato ad-hoc, shell remota senza root). **Es3 `returnlib` (shellcode + SUID) ✅ — root shell ottenuta**: offset 112 (bisezione con stadio intermedio "EBP corrotto" a 110-111, `SIGSEGV in main()`, poi `SIGILL` a 112 = ret riuscito ma atterraggio storto, poi `BBBB` → `0x42424242 in ?? ()` = offset confermato). Due gotcha: **bad character** (`0x20` spazio nell'indirizzo scelto tronca il payload via `$(...)` non quotato) e **stack sotto gdb ≠ stack standalone anche con ASLR off** (soluzione: core dump della vera esecuzione con `fs.suid_dumpable=1` + `sudo coredumpctl gdb <PID>`). **Es4 `returnlib` (ret2libc) ✅ — NX bypassato**: stesso offset 112, stack NON eseguibile, riusato `system()`+`exit`+stringa `SHELL=` della libc invece di shellcode iniettato; niente SUID qui (non serviva root). Nuovo gotcha: **bad character su un indirizzo di funzione** (non su un indirizzo di stack a scelta libera) — `system` aveva byte basso `0x20` (spazio), stesso sintomo di es3 ma stavolta il fix non è "sposta il bersaglio" (un solo entry point valido) bensì **quotare la sostituzione di shell** (`run "$(perl -e '...')"`). Anche: `x/500s $esp` inaffidabile su grandi distanze (troppi terminatori consumano il conteggio) → preferire `find $esp, +lunghezza, "pattern"`, attenti a non sforare `0xffffffff` nell'aritmetica degli indirizzi. Tutto annotato in `guida_lab_moduloS4_binary_exploits.md` (sezioni "✍️ Esecuzione — risultati reali" es1-es4). DRILL finale ancora da fare (rimandato, non bloccante): `SIMULAZIONI ESAMI/SICINF/Binary_exploitation.html` — file scaricato in `esercizi/SICINF/sim_binary_2026-02-12/secret.gz`, esercizio 12/02/2026 (il più recente).
**S5 (Firewall/iptables/nftables) 🔄 — sessione 46, 07/07**: lezione ✅, appunti ✅, guida-lab ✅ (9 esercizi). Ambiente VM sbloccato dopo troubleshooting corposo (Guest Additions clipboard, conflitto Docker/Podman via `DOCKER_HOST`, `interface_name` che richiede Docker Engine v28.1+ non presente nel pacchetto distro — fix: rimossa la proprietà da `nftlab.sh`, dettagli in `troubleshooting_vm.md`). **Es1 (packet filter endpoint, Client, INPUT/OUTPUT default-drop) ✅** e **Es2 (packet filter in instradamento, R1, FORWARD ristretto a Client↔S1/S2) ✅** eseguiti e verificati con ping prima/dopo. **Prossimo: Es3** (gestione regole con handle: add/insert/delete/replace) — poi Es4 (stateful SSH selettivo), Es5 (multi-macchina), Es6 (logging), Es7 (NAT — ⭐ rilevante), Es8 (catene custom), Es9 (contatori). Applicare il filtro "solo se utile per l'esame" (vedi nota sopra) nella scelta di quali di questi completare. Poi S6 → S7 → S8 → S9 → S10 → S11 → S12 → S13 → S14 → S15.

**S10 (Network Intrusion Detection) ✅ chiuso — sessione 48, 10-13/07**: 3 esercizi reali completati hands-on sulla VM. **13/02/2025** (sessione 47): HTTP flood/buffer-overflow-probe, 31 alert, consegna in `esercizi/SICINF/pratica_NIDS_2025-02-13/`. **11/01/2024** (`dump.pcap`): 4 tipi di interazione verso `10.10.10.10` — port scan TCP-connect da `10.10.3.1` (porte 22/80 trovate aperte via SYN,ACK), SSH legittima (2 sessioni con dati reali sulla stessa porta 22 dello scan — lezione: stessa porta/coppia host può nascondere cose diverse, verificare sempre con `tcp.flags`+`tcp.len`, non assumere), Telnet con flag `FLAG{this_port_is_dangerous}` da due sorgenti diverse (10.10.5.21, 10.10.31.2), DDoS con 151 sorgenti distinte su porta 80; regola scritta, 2 alert verificati, flag estratta (jq assente sulla VM → fallback Python), report scritto e **confrontato con la soluzione ufficiale** (ottimo allineamento, in più punti più rigoroso del testo ufficiale). **10/07/2025** (`trace-2025-07-10.pcapng`): topologia a 3 host/3 subnet confermata via scheda Ethernet Conversations (MAC riscritti a ogni salto router); buffer-overflow via SMTP con padding incrementale 0/1 e marcatore fisso `ABCD` (`10.10.101.129→10.10.103.172:25`); HTTP/DNS/ICMP/ARP tutti verificati e classificati come legittimi (DNS = query PTR/A ripetute per l'host mittente, spiegate dai tentativi SMTP ripetuti, non un fenomeno a parte); regola scritta ed eseguita con successo. **Momento critico**: attacco di panico a metà del secondo esercizio per troppi comandi tecnici concatenati senza spiegazione — gestito con pausa, poi ripreso con ritmo più lento (spiegare il perché prima di ogni comando) fino a chiusura. `guida_esame_NIDS.md` rivista e ampliata più volte con le lezioni pratiche di tutti e 3 gli esercizi (mappatura Conversations↔Protocol Hierarchy, criteri ICMP/DNS, verifica flag TCP grezzi, fallback jq). Non ancora praticato hands-on: ARP (2 varianti nel pool, 12/01/2026 e 30/10/2025) — Lorenzo ha scelto di consolidare prima il territorio TCP/applicativo. Nessuna lezione/appunti teorici formali (scelta deliberata).
**S11 (Integrity check/privilege escalation) 🔄 — sessione 49-51, 13-14/07**: due esercizi reali completati hands-on. **9 gennaio 2023** (`change1`, sessione 49): Fase 1 configurato AIDE (scoperto che `/usr/bin` non è coperto dalla config di default — serve regola esplicita `/usr/bin f Full`, aggiunta **prima** di `aideinit`), identificata la modifica: `/usr/bin/cp` ha acquisito il bit **SUID**. Fase 2: sfruttato il SUID di `cp` per riscrivere `/etc/passwd`/`/etc/shadow` senza `sudo` (via `cat file > file_editable` per la copia scrivibile), utente `toor` UID/GID `0` senza password, `su toor` → `id` conferma root. Soluzione confrontata con quella ufficiale su Virtuale. **AIDE non era preinstallato** (`sudo apt install aide`), annotato in `troubleshooting_vm.md`.
**11 gennaio 2024** (`change4`, sessione 51): stesso schema Fase1/Fase2, vettore diverso — **capability `cap_dac_override` su `/usr/bin/tee`** invece di SUID. Diff AIDE con 4 file, triage completo con `getcap`/`ls -l`: `/etc/sudoers` solo ctime (rumore), `/usr/bin/grep` capability impostata e ripristinata dallo stesso `change4` (falso positivo), `/usr/bin/vim.tiny` bit di scrittura tolto — non dato (vicolo cieco), `/usr/bin/tee` `cap_dac_override=ep` (vettore reale). Exploit: `openssl passwd -1 -salt hack hack` per l'hash, riga `hack:$1$hack$xR6zsfvpez/t8teGRRSNr.:0:0:hack:/root:/bin/bash` scritta su `/etc/passwd` via `cat copia | tee /etc/passwd` (la capability si attiva solo se è `tee` stesso ad aprire il file, non con un redirect diretto della shell), `su hack` → `id` conferma root. Confrontato con soluzione ufficiale in `modello_integrity_privesc.md`, combacia.
Deliverable di entrambi gli esercizi in `esercizi/SICINF/privesc_2026-07-14_change4/` (quelli di `change1` sono andati persi al revert VM). **Cambiato il workflow da questa sessione**: screenshot/report catturati sul host in tempo reale durante l'esercizio, non più esportati dalla VM a posteriori (dettagli in `troubleshooting_vm.md`).
`guida_esame_privesc.md` sottoposta ad audit di autosufficienza da un agente Opus in background (sessione 51): trovati e corretti 5 gap (avviso sintassi `/usr/bin f Full` senza trattino, nuova §4.6 sul meccanismo pipe-vs-redirect, bug formato passwd a 6→7 campi in §4.3, prerequisito "AIDE non preinstallato" mancante in §2, nota su `rockyou.txt` compressa in §3.5). Valutazione finale dell'agente: **sì con alta confidenza** per tutti i vettori già catalogati nel pool; limite intrinseco dichiarato — un vettore mai visto prima non è pre-scrivibile, mitigato dal criterio generale in §4.5 + comandi di scoperta a tappeto §4.2/§9.
Restano da esplorare le altre varianti del pool (`change2,3,5,6,7,8,9`) e i due lab dedicati non ancora praticati hands-on (misconfiguration: sudoers/suid/acl/capabilities; HIDS: AIDE + privesc, letti ma non eseguiti).

**SysAdmin** (sospeso fino al 17/07) → **3D**: lezione ✅, guida_lab ✅ (pronta, lab su VM non ancora eseguito). Ripresa post-Security: avvia VM (`cd ~/cockpit/Vault/UniCode/ARCHIVIO/sysAdmin-lab-vagrant && vagrant up --provider=virtualbox && vagrant ssh`), segui `guida_lab_modulo3D_networking_base.md` Es. 1–6, annota inline, poi `/appunti 3D`. Poi: 3E → 3F → 4B → 4C. Guida_lab 0A–2B da rifare a bassa priorità. Piano dettagliato per la sessione settembre da definire dopo il 17/07.

---

## Scadenze Esami

| Esame | Data | Ora |
|-------|------|-----|
| ~~Diritto dell'Informatica T~~ | ✅ 16/06/2026 — **30 e lode** | — |
| Lab Amministrazione di Sistemi T | ~~15/07/2026~~ → **08/09/2026** (rimandato) | — |
| Lab Sicurezza Informatica T | **17/07/2026** | 14:00 |

Piano fasi e stime ore dettagliate: `ESAMI SCELTI.md`
