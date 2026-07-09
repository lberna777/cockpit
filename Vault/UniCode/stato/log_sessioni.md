# Log Sessioni — Studio Attivo

> Storico completo delle sessioni. Ordine cronologico inverso (ultime in cima).
> NON caricare questo file a ogni sessione. Usarlo solo per:
> - `/chiudi` (aggiungere nuova voce)
> - `/sessione` (consultare le ultime 2-3 sessioni per contesto)
> - Richieste specifiche di Lorenzo sullo storico

---

### Sessione 47 — 2026-07-08 (completata)
**Focus**: Security — S10 Network Intrusion Detection. Nuovo binario di lavoro "esercizi prima, teoria dopo" per le tipologie d'esame ancora a 0%, in parallelo al percorso sequenziale (S5 non toccato in questa sessione).

**Coperto in sessione**:
- Chiarite le modalità d'esame: prova doppia (quiz teorico 40% + pratica 60%, 3 esercizi su 5 tipologie).
- Estratto testo e screenshot dai 5 file `SIMULAZIONI ESAMI/SICINF/*.html` (export Virtuale) per individuare, per ciascuna delle 5 tipologie d'esame, un esercizio reale con soluzione recuperabile.
- Creati 5 **modelli risolti** in `SIMULAZIONI ESAMI/SICINF/modelli_risolti/`: Binary exploitation (25/06/2021, screenshot reali), Integrity check/privesc (09/01/2023, screenshot reale), Network Intrusion Detection (11/01/2024, soluzione testuale reale), Web vulnerabilities (13/06/2024 XSS, screenshot reale), Iptables/NFTables (13/09/2023 — soluzione ufficiale non recuperabile, risolto da Claude sullo stesso esercizio reale, segnalato esplicitamente come non ufficiale).
- Per NIDS: creati anche `template_report_NIDS.md` (struttura report.txt con indicazione di dove/come recuperare ogni dato) e `procedura_operativa_NIDS.md` (sequenza fissa di comandi Wireshark/Suricata).
- **Prima volta con Suricata**: installato su Kali/Parrot (`apt install suricata`, v7.0.10 già presente).
- **Eseguito da zero l'esercizio reale 13/02/2025** (S10): scaricato `traffic-2025-02-13.pcap` da Virtuale, analisi in Wireshark (Protocol Hierarchy → Conversations → Follow Stream) guidata passo-passo. Individuati 4 tipi di traffico: SMTP legittimo (172.21.1.166/172.23.3.76 ↔ 172.22.2.81:25), HTTP health-check legittimo (172.21.1.166→172.23.3.76:80, richieste distanziate di secondi), ICMP (ping 172.21.1.166↔172.23.3.76), e attacco HTTP flood/buffer-overflow-probe (172.22.2.81→172.23.3.76:80, richieste a millisecondi, query string `/?AAAA...BBBB`).
- Momento di correzione utile: Lorenzo ha giustamente contestato l'euristica iniziale di Claude ("ripetizione identica = traffico sicuro") — corretto in "conta la frequenza/volume relativo, non la ripetizione in sé", che ha poi portato a distinguere correttamente health-check (secondi) da flood (millisecondi).
- Scritta e verificata una regola Suricata (`alert http 172.22.2.0/24 any -> 172.23.3.0/24 80 (msg:"..."; content:"BBBB"; http_uri; sid:1000001; rev:1;)`) — 31 alert generati su `eve.json`.
- Consegna completa in `esercizi/SICINF/pratica_NIDS_2025-02-13/`: `report.txt` (rivisto da Claude per coerenza reti /24, sezione ICMP completata da Lorenzo), `exam.rules`, `suricata.yaml`, `eve.json`.
- Scoperta pratica: Claude ha accesso screenshot diretto al desktop host (Hyprland, `grim`) — usato più volte per leggere Wireshark/terminale direttamente invece di copia-incolla manuale.

**Non coperto / da riprendere**:
- Nessuna lezione/appunti teorici formali per S10 — resta da fare, deliberatamente rimandato.
- Template + procedura operativa mancanti per le altre 4 tipologie (Web, Binary, Iptables, Integrity) — i modelli risolti ci sono già, mancano solo i due livelli "forma" e "algoritmo".
- S11 (Integrity check/privesc) ancora completamente a 0%, stesso approccio da applicare.
- S5 Es3-9 non toccati in questa sessione (nessun avanzamento sul percorso sequenziale).

**Prossima sessione — da dove partire**:
→ Security: scegliere se consolidare S10 con un secondo esercizio pratico, passare a S11 con lo stesso approccio "esercizi prima, teoria dopo", oppure tornare al percorso sequenziale S5 Es3. Se si prosegue sulla pratica esame, riusare `modelli_risolti/` + creare template/procedura per la tipologia scelta.

---

### Sessione 46 — 2026-07-07 (completata)
**Focus**: Security — S5 Firewall/iptables/nftables (lezione + appunti + guida-lab + esecuzione lab Es1-2). Tentativo di drill esame S4 abbandonato a favore del ritorno al percorso sequenziale.

**Coperto in sessione**:
- Discussione iniziale su strategia: aggredire gli esercizi tipo esame (drill `Binary_exploitation.html` su S4) vs proseguire sequenzialmente. Scaricato `secret.gz` (esercizio 12/02/2026, il più recente) in `esercizi/SICINF/sim_binary_2026-02-12/`, ma non eseguito — Lorenzo ha deciso di tornare al percorso sequenziale (S5 prima, drill/simulazioni riservati alla finestra 14-16/07).
- `/lezione S5` → `lezione_moduloS5_firewall_iptables.md`: architettura firewall (default deny, topologie/DMZ/BH/ALG/CLG), iptables (sintassi, tabelle, catene custom, trabocchetto RETURN custom-vs-builtin), nftables (stessa logica, zero default), NAT (DNAT/SNAT/MASQUERADE/REDIRECT), conntrack/stateful, 5 hook di netfilter.
- `/appunti S5` → `appunti_moduloS5_firewall_iptables.md`: 5 domande risolte (sintassi posizionale iptables, struttura comando nft scomposta in 3 passi, hook di netfilter, sezione Topologie riscritta con glossario BH/PF/DMZ/ALG/CLG), 1 precisazione concettuale (PF non è "proprietà" del firewall ma uno dei 3 tipi fondamentali) → aggiunta a `errori_frequenti.md`.
- `/lab S5` → `guida_lab_moduloS5_firewall_iptables.md`: 9 esercizi dal LAB PDF (endpoint, instradamento, gestione regole/handle, stateful, multi-macchina, logging, NAT, catene custom, contatori). Estratto e salvato il diagramma di rete embedded nell'HTML (`diagramma_moduloS5_architettura.png`): Client-R1-R2-{S1,S2}, 4 subnet.
- **Troubleshooting ambiente esteso** (dettagli completi in `troubleshooting_vm.md`): Guest Additions/clipboard rotto di nuovo dopo un upgrade kernel (fix: `virtualbox-guest-utils-hwe`/`virtualbox-guest-x11-hwe` + reboot); conflitto `DOCKER_HOST` che punta a un socket Podman inesistente nonostante Docker vero sia installato e attivo (workaround: `unset DOCKER_HOST` a ogni nuovo terminale, causa radice non identificata); `nftlab.sh` falliva con `interface_name requires Docker Engine v28.1 or later` — il pacchetto distro Parrot (`docker.io` 26.1.5) è troppo vecchio per una proprietà Compose recente, e le istruzioni ufficiali del corso non specificano una versione minima dell'Engine. Risolto rimuovendo `interface_name` **dallo script stesso** (non dal `compose.yaml` generato, che viene rigenerato a ogni lancio via heredoc) — i container ora usano nomi di interfaccia di default (`eth0` invece di `eth1`), da verificare con `ip a` invece di fidarsi del diagramma.
- **Esecuzione lab su VM**: Es1 (packet filter su endpoint, container Client, INPUT/OUTPUT default-drop + eccezione ICMP) ✅ — verificato con ping prima/dopo (0% loss → 100% loss → 0% loss dopo la regola mirata). Es2 (packet filter in instradamento, container R1, FORWARD ristretto a Client↔S1 e Client↔S2) ✅ — stesso pattern di verifica, più un gotcha di case-sensitivity nftables (`forward` minuscolo ≠ `FORWARD` maiuscolo) risolto con `nft list ruleset`.
- Lorenzo ha corretto da solo un'incomprensione sulla topologia (pensava S1↔S2 comunicassero direttamente; in realtà è Client a raggiungere entrambi, via R1→R2) — buon segnale di comprensione concettuale nonostante la sessione fosse pesante di troubleshooting.

**Non coperto / da riprendere**:
- Es3-9 di S5 (handle, stateful SSH selettivo, multi-macchina, logging, NAT, catene custom, contatori).
- Drill S4 (`Binary_exploitation.html`) — rimandato alla finestra 14-16/07.

**Decisione di Lorenzo per le prossime sessioni**: eseguire sulla VM solo gli esercizi guida-lab effettivamente utili e collegati alle modalità d'esame, non tutti per principio — vedi nota in `stato/corrente.md`.

**Prossima sessione — da dove partire**:
→ Security **S5**: VM Parrot, `cd ~/lab_S5 && unset DOCKER_HOST && ./nftlab.sh` (ambiente già patchato, dovrebbe partire liscio). Riprendere da **Esercizio 3** della guida-lab, applicando il filtro di rilevanza d'esame nella scelta di quali esercizi completare fino in fondo.

---

### Sessione 45 — 2026-07-02 (completata)
**Focus**: Security — S4 Binary Exploits (chiusura: es4 ret2libc + drill mancante rimandato)

**Coperto in sessione**:
- **Es4 `returnlib` (ret2libc) ✅ completato — S4 chiuso, tutti e 4 gli esercizi fatti.** Ricompilato senza `-z execstack` (`es_nostack`), niente SUID (non serviva root, solo dimostrare il bypass di NX).
- Prima volta con breakpoint gdb nel modulo (`b *main`): fermarsi con libc già caricata per leggere `p system` (`0xf7db1220`) e `p exit` (`0xf7d9daf0`) prima che il programma crashasse per `argv[1]` nullo.
- `x/500s $esp` insufficiente per raggiungere `envp` (troppi terminatori intermedi consumano il conteggio di 500 stringhe) → risolto con `find $esp, +0x3000, "SHELL="` (trovato `SHELL=/bin/bash` a `0xffffcdfe`, valore a +6 byte). Prima versione di `find` con `$esp+20000` falliva per overflow dell'aritmetica a 32 bit (`Invalid search space, end precedes start`).
- **Nuovo bad character**: `system` aveva byte basso `0x20` (spazio) → `$(...)` non quotato troncava il payload esattamente come `"A"x112` senza marcatore in es3 (stesso crash `SIGILL, 0x56556201 in main ()`). A differenza di es3 (indirizzo di stack, libertà di scegliere un bersaglio vicino), qui il fix è **quotare la sostituzione**: `run "$(perl -e '...')"`.
- Payload finale: `"\x90"x112 + system + exit + /bin/bash` → `[Detaching after vfork from child process ...]` (conferma `system()` eseguito) → shell ottenuta, `id` → `uid=1000` (nessun SUID, atteso).
- Tutto annotato in `guida_lab_moduloS4_binary_exploits.md` (sezione "✍️ Esecuzione — risultati reali (es 4)").
- Teoria/appunti S4 già completi da sessioni precedenti — nessun nuovo grezzo da elaborare con `/appunti`.

**Non coperto / da riprendere**:
- DRILL finale S4: `SIMULAZIONI ESAMI/SICINF/Binary_exploitation.html` (rimandato, non bloccante per iniziare S5).

**Prossima sessione — da dove partire**:
→ Security **S5** (Firewall e packet filter — ⭐ Iptables/NFTables), modulo nuovo: `/lezione S5` dai PDF Virtuale prima di toccare la VM. Il DRILL di S4 può essere fatto prima o incastrato più avanti nel ripasso.

**Aggiornamento 2026-07-07**: `/lezione S5` fatta → `lezione_moduloS5_firewall_iptables.md`. Appunti modulo S5 elaborati → `appunti_moduloS5_firewall_iptables.md` (5 domande risolte, 1 precisazione concettuale su PF vs tipi di firewall, sezione Topologie riscritta con glossario BH/PF/DMZ/ALG/CLG). LAB su VM non ancora eseguito — S5 resta 🔄.

---

### Sessione 44 — 2026-07-01 (completata)
**Focus**: Security — S4 Binary Exploits (esecuzione lab, es2 → es3)

**Coperto in sessione**:
- Sessione ripresa dopo spegnimento accidentale del PC; deciso in `/sessione` precedente: **Sistemi rimandato a settembre (08/09)**, focus esclusivo su Security fino al 17/07.
- **Es2 `secret_function` ✅ completato**: lanciato il payload (`"A"x16,"\xad\x61\x55\x56"`) in gdb → flag presa, poi confermato fuori da gdb dopo aver scoperto e risolto il gotcha ASLR/reboot (annotato in `troubleshooting_vm.md`).
- **Es2b `secret_function_remote` ✅ completato**: `es.c` usa `gets()` non più dichiarata dalle glibc moderne → fix `extern char *gets(char *s);`; stesso offset 16; esposizione in rete con `ncat` (il `nc` di Parrot è variante OpenBSD senza `-e`, installato `ncat` ad-hoc); shell remota ottenuta con il trucco del `cat` per tenere aperto lo stdin — privilegi utente normale (nessun SUID qui).
- **Es3 `returnlib` (shellcode injection + SUID) ✅ completato — root shell ottenuta**: setup SUID, bisezione offset (112, con stadio intermedio "EBP corrotto" prima del controllo pieno di EIP), NOP sled + shellcode, due gotcha nuovi risolti — **bad character** (byte `0x20` in un indirizzo troncava il payload via shell non quotata) e **differenza stack gdb vs standalone** (argv[0] diverso sposta il buffer di centinaia di byte, risolto analizzando un core dump della vera esecuzione standalone con `fs.suid_dumpable=1` + `sudo coredumpctl gdb`).
- Tutto annotato inline in `guida_lab_moduloS4_binary_exploits.md` (blocchi "✍️ Esecuzione — risultati reali" per es2, es2b parte 1+2, es3 + una sezione "Metodo generale" per orientarsi quando un indirizzo non torna).
- Aggiornati `troubleshooting_vm.md` (5 nuovi problema/causa/soluzione) e `glossario_sysadm.md` (voce "bad character").

**Non coperto / da riprendere**:
- Es4 (`returnlib`, variante ret2libc — aggirare NX riusando `system("/bin/sh")` della libc).
- DRILL finale `SIMULAZIONI ESAMI/SICINF/Binary_exploitation.html` (dopo es4).

**Prossima sessione — da dove partire**:
→ Security S4: VM Parrot, cartella `~/lab_S4/lab_exercises/returnlib` (stesso binario di es3, stack ancora eseguibile per compatibilità — verificare flag di compilazione in `guida_lab_moduloS4_binary_exploits.md` sezione Esercizio 4). Obiettivo dichiarato per la prossima sessione: **chiudere es4**. Poi drill finale S4, quindi S5 (Iptables/NFTables).

---

### Sessione 43 — 2026-06-30 (completata)
**Focus**: Security — S4 Binary Exploits (appunti + guida-lab + esecuzione lab)

**Coperto in sessione**:
- `/appunti S4` → `appunti_moduloS4_binary_exploits.md`: risolta domanda aperta ASLR (indirizzi `.text` non randomizzato), colmata lacuna shellcode+NOP sled, chiarimento "cima/basso" stack. Nessun bug → errori_frequenti invariato.
- `/lab S4` → `guida_lab_moduloS4_binary_exploits.md` dal LAB PDF (55pp): setup, threat model, 4 gradini con anatomia comandi.
- **Esecuzione lab sulla VM Parrot**:
  - **Es1 `write_var` ✅ COMPLETATO**: bisezione manuale → control pieno a 108 → padding **104**; payload `"A"x104,"EDCB"` → flag `SEC{thisistherightflagidiot!}`. Capito little-endian dal vivo (fill byte-per-byte + test `EDBC` vs `EDCB`). Risultati annotati inline nella guida-lab (blocco ✍️ Esecuzione es1).
  - **Es2 `secret_function` 🔄 a metà**: capita la struct (buffer[16]+puntatore `process`); con 20 A → crash `0x41414141` in gdb (controllo il flusso); trovato indirizzo `secret` = **`0x565561ad`** con `info functions secret`. **Manca il lancio del payload** `"A"x16,"\xad\x61\x55\x56"`.

**Non coperto / da riprendere**:
- Es2 dal lancio del payload; poi es2-remote, es3 (shellcode/root shell), es4 (ret2libc).
- DRILL `SIMULAZIONI ESAMI/SICINF/Binary_exploitation.html` a lab finito.

**Prossima sessione — da dove partire**:
→ Security S4: VM Parrot, `cd ~/lab_S4/lab_exercises/secret_function`, `gdb ./es`, `run $(perl -e 'print "A"x16,"\xad\x61\x55\x56"')` → flag; poi fuori da gdb con `./es`. Avanti coi gradini 2b→4.

---

### Sessione 42 — 2026-06-29 (completata)
**Focus**: Security — S4 Binary Exploits (lezione)

**Coperto in sessione**:
- Lettura integrale PDF teoria "Binary exploits" (64pp) + PDF lab "LAB bruteforcing e buffer overflows" (55pp)
- Creazione `lezione_moduloS4_binary_exploits.md`: stack frame IA32, __cdecl, buffer overflow, GDB, little endian, shellcode + NOP sled, ret2libc, ROP, contromisure (canarini/NX/ASLR/PIE/CFI)
- Threat model attaccante+difensore, 5 domande autoverifica stile quiz 40%
- Stato S4 aggiornato a 🔄

**Non coperto / da riprendere**:
- Appunti grezzi S4: Lorenzo studia la lezione e li scrive in autonomia
- VM non toccata — `/lab S4` da fare dopo gli appunti grezzi

**Prossima sessione — da dove partire**:
→ (vedi sessione 43 sopra)
→ SysAdmin 3D: `cd ~/Progetti/sysAdmin-lab && vagrant up && vagrant ssh` → segui guida_lab_modulo3D

---

### Sessione 41 — 2026-06-26 (completata)
**Focus**: Security — S2 ripasso + S3 lab VM (DVWA)

**Coperto in sessione**:
- Ripasso S2 Autenticazione: 1/5 corrette, 2/5 parziali, 2/5 errate — debolezze su PAM control-flag e autenticazione vs autorizzazione
- Lab S3 Web Security su VM Parrot: tutti 9 esercizi completati
  - Es.1 Service Enumeration (nmap) ✅
  - Es.2 Directory Discovery (gobuster) ✅
  - Es.3 Brute Force Login (Burp + Hydra) ✅ — fix sintassi Hydra 9.5 (condition string last)
  - Es.4 LFI Path Traversal ✅ — fix: 5 livelli `../` non 4
  - Es.5 Command Injection ✅
  - Es.6 SQL Injection semplice ✅
  - Es.7 SQL Injection Union Based ✅
  - Es.8 XSS Reflected ✅
  - Es.9 XSS Stored ✅
- Guida lab aggiornata con output reali, fix e spiegazioni inline

**Non coperto / da riprendere**:
- SysAdmin 3D: lab sulla VM ancora da eseguire

**Prossima sessione — da dove partire**:
→ Security S4 Binary Exploits: `/lezione S4` (PDF: cercare in `SLIDE LAB/SICINF/`) → `/lab S4`
→ SysAdmin 3D: `cd ~/Progetti/sysAdmin-lab && vagrant up && vagrant ssh` → segui guida_lab_modulo3D

---

### Sessione 40 — 2026-06-24 (completata)
**Focus**: Security S3 — Web Security OWASP Top Ten (teoria)

**Coperto in sessione**:
- Letti integralmente Web_security_6_marzo.pdf (45 pp.) e LAB_web_security_11_marzo.pdf (42 pp.)
- Scritta lezione S3 completa (A1-A10, threat model, SQLi Union Based, XSS 3 tipi, CSRF, XXE, SSRF)
- Appunti modulo S3 elaborati → `appunti_moduloS3_web_security.md`
- Risolte 16 domande aperte dagli appunti grezzi

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
