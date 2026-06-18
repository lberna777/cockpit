# Avvio Security S1 — Setup sessione + skill /studia

**Date:** 2026-06-18
**Status:** IN CORSO
**Corso:** Lab Sicurezza Informatica T + Lab Amministrazione di Sistemi T
**Modulo:** S1 LAB Enumerazione (Security) + 3D Es. 2-6 (SysAdmin)
**Chain:** `standalone-972162f3` seq `1`
**Parent:** `none — prima sessione`
**Prior chain:** nessuno — prima sessione

---

## Obiettivo della Sessione

Avviare il primo giorno della fase 1 (18/06–30/06): Security da 0% con S1 LAB come punto di partenza.
Risolvere il planning e il setup della sessione; creare la skill `/studia` per il flusso di annotazione inline.
Il LAB vero (comandi su VM) non è ancora stato eseguito — la sessione è stata pianificazione + tooling.

---

## Concetti Assimilati

- **Kill chain** (Lockheed Martin): 7 fasi — Reconnaissance → Weaponization → Delivery → Exploitation → Installation → C2 → Actions on Objectives. S1 copre il primo anello.
- **MITRE ATT&CK**: framework per descrivere concretamente le tecniche (Reconnaissance = TA0043).
- **VA vs PT**: VA trova vulnerabilità note e si ferma; PT avanza fino in fondo con exploit (più realistico, più rischioso). VA ha falsi positivi; PT ha impatto reale.
- **Offensive security**: usare le stesse tecniche degli attaccanti. MAI su risorse non proprie senza permesso esplicito.
- **OSINT**: qualsiasi fonte pubblicamente disponibile per raccogliere info su un target. Sostanzialmente legale con aree grigie.
- **Google Dork**: operatori per affinare ricerche (allintext, allinurl, filetype, inurl, intitle, site, *). Utile nella fase di enumerazione OSINT.
- **DNS enumeration**: record types (A, CNAME, MX, NS, SOA, TXT, PTR, SRV). Strumenti: nslookup, dig, dnsrecon, dnsmap. I record DNS rivelano IP, server applicativi, sottoreti nascoste.
- **Subdomain enumeration**: strategia passiva (Shodan, Censys, SecurityTrails, crt.sh) vs attiva (DNS bruteforcing). crt.sh enumera sottodomini tramite Certificate Transparency.
- **Enumerazione host**: nmap -sn per host discovery (ping scan, ARP in host-only → richiede sudo).
- **Enumerazione servizi**: nmap -sT (TCP connect), -sV (version detection), -p- (tutte le porte). Greenbone/OpenVAS = VA automatico (fork open-source di Nessus dal 2005).
- **-p- è critico**: senza di esso nmap scansiona solo ~1000 porte → si perde servizi su porte non-standard (es. SSH su 1337).
- **Service fingerprinting**: -sV rivela il servizio reale (porta 1337 classificata "waste" da -sT, ma è SSH per -sV).
- **Misconfiguration**: SMTP banner che rivela info interne; DB esposti fuori da localhost con credenziali deboli. netcat per banner grabbing (nc <ip> 25).
- **psql per PostgreSQL**: -U admin -h <ip> -W -l elenca DB; poi \dt + SELECT * FROM accounts per esfiltrazione.
- **hydra per brute force**: -l root -x 4:4:1 ssh://<ip>:<porta> genera tutti i PIN a 4 cifre. 10.000 combinazioni → minuti.
- **Hash cracking**: CUPP genera wordlist personalizzata da dati personali; unshadow combina passwd+shadow; john cracca.
- **Snapshots**: obbligatori prima di ogni esercizio di compromissione; permettono reset. VBoxManage snapshot "VM" take "nome".

---

## Ancora Poco Chiaro

- Output atteso preciso delle 3 VM target (IP dipendono dalla propria installazione VirtualBox — gli IP del corso .32/.33/.34 sono esempi, non garantiti).
- Greenbone/OpenVAS: come è installato nella VM Kali specifica — da verificare durante il LAB.
- Fase "DA FARE" del lab: gli approfondimenti (smtp-user-enum, enum4linux-ng per SMB) non sono stati esplorati — tocca a Lorenzo decidere se affrontarli o saltare.

---

## Connessioni con Altro

- **SysAdmin 3A/3B (systemd, pacchetti)**: i servizi configurati in SysAdmin (SSH, Apache, MariaDB) sono esattamente quelli che Nmap trova in S1. L'enumerazione offensiva corrisponde all'esposizione difensiva di 3A.
- **SysAdmin 3D (networking di base)**: ping, ss -tlnp, /etc/hosts — concetti speculari all'enumerazione host di S1. Chi konfigura è difensore; chi scansiona è attaccante.
- **Security S5 (firewall iptables)**: il motivo per cui alcuni servizi non sono raggiungibili da fuori è esattamente il firewall — S1 mostra cosa si vede senza firewall.
- **Security S10 (NIDS Suricata)**: le scansioni nmap di S1 generano traffico che Suricata rileverebbe — ogni LAB offensivo ha il suo corrispettivo difensivo.
- **Security S11 (integrity/privilege escalation)**: la guida-lab S1 include un drill finale su Integrity/privesc come collegamento diretto.

---

## Esercizi

| Esercizio | Stato | Approccio usato | Note/Errori |
|---|---|---|---|
| S1 LAB Fase 1 — Predisporre i target | ⬜ | — | 3 VM da /opt/owa (Appliance-disk001/002/003.vdi), host-only vboxnet0, snapshot prima di avviare |
| S1 LAB Fase 2 — nmap host+servizi | ⬜ | — | nmap -sn, poi -sT -p-, poi -sV per porte aperte |
| S1 LAB Fase 3 — Verifica output | ⬜ | — | Confrontare con output atteso nella guida-lab |
| S1 LAB Fase 4 — Misconfiguration | ⬜ | — | netcat SMTP, psql PostgreSQL |
| S1 LAB Fase 5 — SSH + hydra | ⬜ | — | 4 servizi SSH; pin a 4 cifre su porta 1337 |
| S1 LAB Fase 6 — Hash cracking | ⬜ | — | CUPP + john su passwd.bak/shadow.bak |
| SysAdmin 3D Es. 2-3 | ⬜ | — | ping tra macchine + ss -tlnp; ~1h |

---

## Errori e Misconcezioni

- **Snapshot segnalato come ✓ nel file guida**: la guida-lab `guida_lab_moduloS1_enumerazione.md` indicava snapshot `baseline-pulita` già fatto (✓), ma `percorso.md` confermava zero snapshot al 18/06. Corretto → ora mostra il comando VBoxManage da eseguire prima di tutto.
- **Date esami nel template `/piano` erano errate**: il template aveva Diritto 16/06 e SysAdmin 22/06. In realtà Diritto è già superato (30L) e SysAdmin spostato al 15/07. Usare sempre corrente.md come fonte di verità, non il template statico della skill.

---

## Materiali Usati

### File lezione/guida-lab
- `claudeLezioni/LEZIONI SECURITY/guida_lab_moduloS1_enumerazione.md` — guida-lab completa, 6 fasi, già presente da sessione precedente; corretto solo il blocco snapshot
- `claudeLezioni/LEZIONI SECURITY/lezione_moduloS1_offensive_security_enumerazione.md` — lezione già segnata ✅ in corrente.md

### PDF sorgente letti integralmente questa sessione
- `SLIDE TEORIA/SICINF/Principi_delloffensive_security_20_febbraio.pdf` (53 pp) — kill chain, VA/PT, OSINT, Google Dork, DNS enum, subdomain enum, Greenbone
- `SLIDE TEORIA/SICINF/__ LAB __ Enumerazione [25 febbraio] _ Virtuale.pdf` — 6 sezioni del LAB con comandi e output attesi

### Skill creata
- `~/.claude/local-marketplace/plugins/lorenzo-skills/skills/studia/SKILL.md` — skill per checkpoint sessione interattiva inline

---

## Preferenze e Feedback di Sessione

- **Annotazione inline > appunti separati**: Lorenzo non trova sensato scrivere appunti in un file separato. Preferisce annotare direttamente nel file lezione/guida-lab mentre studia (legge + esegue + commenta nello stesso file).
- **`/studia` come flusso principale**: la skill `/studia <ID>` è il nuovo punto di contatto durante la sessione: scatta checkpoint, risponde a dubbi, guida al passo successivo. Convenzione: `> ` (blockquote) con ❓ ✅ ⚠️.
- **Piano ridimensionato a 2.5h**: oggi Lorenzo ha solo 2.5h. Blocco 1: S1 LAB Fase 1-3 (~1.5h); Blocco 2: SysAdmin 3D Es. 2-3 (~1h).
- **La sessione di oggi era setup, non studio**: il LAB effettivo non è ancora iniziato. La prossima sessione apre la VM e segue la guida-lab.

---

## Stato Moduli al 18/06

```
Diritto   ██████████  SUPERATO — 30 e lode (16/06)
SysAdmin  ██████░░░░  ~63%  — 3D in corso (Es. 2-6 ⬜), 3E/3F/4A/4B/4C tutti ⬜
Security  ░░░░░░░░░░    0%  — S1 LAB prossimo passo
```

**Scadenze**: SysAdmin 15/07 (27 gg) · Security 17/07 (29 gg)
**Ritmo richiesto**: ~5h/gg senza giorni vuoti per chiudere entrambi in tempo.
**Rischio principale**: S4 Binary Exploits (~12h, il più complesso) va affrontato entro fine giugno.

---

## Dove Stiamo Andando

1. **Oggi**: S1 LAB Fase 1-3 (~1.5h) + SysAdmin 3D Es. 2-3 (~1h)
2. **Domani**: S1 LAB Fase 4-6 (misconfiguration + hydra + hash cracking) → `/appunti S1` (o annotazione inline se preferisce)
3. **Poi**: S2 Autenticazione → S3 Web Security → S4 Binary Exploits (entro 30/06)
4. **SysAdmin parallelo**: 3D completare → 3E Vagrant Multi-Machine → 3F Ansible
5. **11-14/07**: rifinitura SysAdmin + simulazione prima dell'esame del 15/07

---

## Rischi e Blocchi

- **VM non configurata**: zero snapshot, nessuna verifica che la VM sia funzionante. Prima mossa obbligatoria: avviare + snapshot baseline.
- **4B SNMP e 4C LDAP SysAdmin**: non mappati, non scaricati, non studiati — sono d'esame. Vanno recuperati non appena 3D/3E/3F sono chiusi.
- **S4 Binary Exploits**: richiederebbe emulatore x86_32 se su Apple Silicon (Lorenzo è su Linux x86_64 — OK).
- **Ritmo non comprimibile**: una settimana persa rende la coppia di esami non recuperabile.

---

## Skill /studia — Dettagli di implementazione

La skill è stata creata in questa sessione e **non ancora testata su una vera sessione di annotazione**. Primo utilizzo reale = prossima sessione con il LAB S1.

**Convenzione annotazione (da comunicare se Lorenzo non la usa):**
```
> output incollato dal terminale                     ← risultato di un comando
> ❓ cosa significa questo errore?                   ← dubbio esplicito
> ✅ funziona, ho ottenuto X                         ← conferma esecuzione
> ⚠️ errore: Permission denied                       ← qualcosa non ha funzionato
```

**Comportamento atteso della skill:**
- Legge integralmente il file annotato (lezione o guida-lab)
- Trova l'ultima annotazione di Lorenzo (= "frontiera")
- Verifica output copiati vs output attesi nel file
- Risponde a ❓ in modo diretto e pratico
- Diagnostica ⚠️ con fix concreto
- Chiude sempre con **Prossimo →** [azione concreta]
- Non rigenera il file — solo risposta in chat

**Path skill**: `~/.claude/local-marketplace/plugins/lorenzo-skills/skills/studia/SKILL.md`

---

## Dettaglio Flusso /piano e Ridimensionamento

**Piano originale** (da `/piano` inizio sessione):
- Blocco 1: S1 LAB Fasi 1-3 (~1.5h)
- Blocco 2: SysAdmin 3D Es. 2-3 (~1h)
- Blocco 3: Security studio teoria S1 → teoria pages 21-53 (~1h)
- Totale proposto: ~3.5h

**Piano ridimensionato** (su richiesta: "ho 2 ore e mezza o poco più"):
- Blocco 1: S1 LAB Fasi 1-3 (~1.5h) — invariato
- Blocco 2: SysAdmin 3D Es. 2-3 (~1h) — invariato
- Blocco 3 eliminato (la teoria S1 era già stata letta nella sessione precedente alla compaction)

**Nota sul `/piano`**: il template skill aveva date esami hardcoded (Diritto 16/06 come futuro, SysAdmin 22/06). La skill è stata ricalibrata leggendo corrente.md ma il template base va corretto in una futura sessione di manutenzione.

---

## Sessione Precedente (pre-compaction) — Riepilogo

Prima della compaction di contesto questa sessione aveva già:
1. Letto integralmente il LAB PDF (6 sezioni, comandi + output attesi)
2. Letto teoria PDF pagine 1-20 (kill chain, VA/PT, OSINT, Google Dork base)
3. Tentato di leggere pagine 21-53 → fallito per limite 20-pagine/chiamata
4. La sessione post-compaction (questa) ha letto 21-40 e 41-53 in parallelo
5. La guida-lab esistente è stata verificata e corretta (solo fix snapshot)

**Google Dork — operatori specifici visti nel PDF** (utili per domande d'esame):
- `allintext:testo` — tutte le parole nel corpo pagina
- `allinurl:parola` — nel solo URL
- `filetype:pdf` — tipo file specifico
- `inurl:admin` — parola in URL
- `intitle:index.of` — nella title tag (listing directory)
- `intext:password` — nel testo
- `link:url` — pagine che puntano all'URL
- `site:unibo.it` — solo quel dominio
- `*` — wildcard

**Esempio Google Dork dal PDF** (esercitazione tipica d'esame):
```
site:ulisse.unibo.it filetype:PDF intext:password
site:ulisse.unibo.it intitle:index.of id_rsa -id_rsa.pub
```

---

## Quick Start Prossima Sessione

```
# Ripristina contesto
Leggi: .claude/handoffs/HANDOFF_standalone-972162f3_security-s1-setup_2026-06-18.md

# Materiali da aprire
~/UniCode/claudeLezioni/LEZIONI SECURITY/guida_lab_moduloS1_enumerazione.md   ← segui questa
~/UniCode/claudeLezioni/LEZIONI SECURITY/lezione_moduloS1_offensive_security_enumerazione.md  ← annotala inline

# Prima azione (OBBLIGATORIA prima di tutto il resto)
VBoxManage startvm "LabSicurezzaInformatica"
VBoxManage snapshot "LabSicurezzaInformatica" take "baseline-pulita"

# Poi: Fase 1 guida-lab — creare 3 VM target
Aprire VirtualBox → Nuova → Tipo Linux/Debian 64-bit → 1 core, 1024 MB → disco .vdi da /opt/owa
Ripetere per Appliance-disk001.vdi, 002.vdi, 003.vdi
Snapshot ciascuna PRIMA di avviarla

# Skill da usare durante il LAB
/studia S1   ← ogni volta che hai un dubbio o vuoi verificare un output

# Verifica comprensione prima di andare avanti dalla Fase 2
Sai spiegare perché nmap -sT senza -p- si perde la porta 1337?
(Risposta: -sT senza -p- scansiona solo le ~1000 porte più popolari; 1337 non è tra quelle)
```
