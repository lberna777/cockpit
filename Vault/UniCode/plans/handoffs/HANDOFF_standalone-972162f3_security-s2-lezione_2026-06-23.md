# Security S2 — Lezione autenticazione prodotta, Lorenzo la legge su iPad

**Date:** 2026-06-23
**Status:** IN CORSO
**Corso:** Lab Sicurezza Informatica T
**Modulo:** S2 — Autenticazione
**Chain:** `standalone-972162f3` seq `3`
**Parent:** `HANDOFF_standalone-972162f3_security-s1-guida-lab_2026-06-22.md` (seq 2)
**Prior chain:** `security-s1-setup 18/06` > `security-s1-guida-lab 22/06` > questo

---

## Obiettivo della Sessione

Sessione del 23/06, avviata alle 14:44 con finestra 14:44–18:30. Il parent (22/06) aveva pianificato
S2 come passo immediatamente successivo a S1 (lab completato nel pomeriggio 22/06, sessione 37).
Questa sessione ha prodotto `/lezione S2` leggendo integralmente entrambi i PDF, poi ha pushato
tutto su GitHub perché Lorenzo usa l'iPad per leggere le lezioni. Al momento del handoff Lorenzo
sta leggendo `lezione_moduloS2_autenticazione.md` sull'iPad — nessuna VM aperta.

---

## Cosa Cambia Rispetto al Parent

**Parent (22/06) → questa sessione (23/06):**

- S1 LAB: completato in **sessione 37** del pomeriggio 22/06 (corrente.md: `✅ Sessione 37`)
- S1 appunti: completati (file esiste: `claudeAppunti/APPUNTI SECURITY/appunti_moduloS1_offensive_security_enumerazione.md`)
- S2 lezione: **creata questa sessione** da lettura integrale dei 2 PDF
- PDF batch: convertiti 12 PDF mancanti (Diritto D1-D9, S1 appunti, S2 lezione, guida-lab S1)
- `stato/corrente.md`: S2 → `🔄 lezione ✅`
- Push su GitHub: `fb0abe9` — materiale disponibile su iPad

**Il parent temeva "due guida-lab S1"** (enumerazione.md + enumerazione_nmap.md): verificare se
il vecchio `guida_lab_moduloS1_enumerazione.md` esiste ancora → se sì, si può eliminare (la nuova
`guida_lab_moduloS1_enumerazione_nmap.md` è quella usata in sessione 37 ed è completa).

---

## Concetti Assimilati (S2 — Autenticazione)

Derivati dalla lettura dei PDF e dalla struttura della lezione prodotta:

- **Regola AAA**: Autenticazione (prova di identità) ≠ Identificazione (dichiarazione) ≠ Autorizzazione (permessi su oggetto) ≠ Auditing (tracciamento). Errore comune: usare elementi identificativi (username, email) come segreti — sembrano oscuri ma non lo sono.
- **4 fattori**: conosce (password/PIN) · possiede (token fisico/Yubikey) · è (biometrico) · fa/dove (posizione GPS). 2FA vera richiede fattori di *categorie distinte*.
- **Autenticazione passiva**: P invia il segreto a V → problemi: intercettazione in chiaro, replay attack, furto del file V. È il modello password classico.
- **Autenticazione attiva**: P prova di conoscere il segreto senza svelarlo, ogni volta con un dato diverso → furto da V e dal canale sono inutili. Resta il rischio MITM attivo.
- **`/etc/shadow`**: formato `$6$<salt>$<fingerprint>` — SHA-512 + salt per utente. Il salt impedisce rainbow tables e rivela utenti con password uguali. Il pepper vive in un HSM, non nel DB: protezione aggiuntiva contro furto di `/etc/shadow`.
- **S-KEY OTP**: V inizializzato con h^k(N); P invia h^(k-1)(N); V verifica applicando hash una volta. Hash = facile da calcolare, impossibile da invertire → chi intercetta non può ricavare il token successivo.
- **Challenge-response (SSH)**: V cifra un nonce con PUB_P e manda a P → P decifra con PRIV_P e rimanda il nonce. P non svela mai la chiave privata. `~/.ssh/authorized_keys` = dove V memorizza PUB_P. Questo è il meccanismo concreto usato ogni giorno in SysAdmin.
- **`/etc/pam.d/`**: un file per ogni programma (`sshd`, `sudo`, `login`). Ogni riga = `module-type control-flag module-path [args]`. Stack di moduli eseguiti in ordine.
- **PAM control-flag**: `required` (continua ma stack fallirà) ≠ `requisite` (termina immediatamente su fallimento) ≠ `sufficient` (termina con successo se nessun required precedente ha fallito) ≠ `optional`. L'**ordine** dei moduli nello stack non è decorativo — cambia la logica completamente.
- **PAM moduli chiave**: `pam_unix.so` (legge `/etc/shadow`) · `pam_tally.so` (blocca dopo N tentativi falliti — difesa brute force online) · `pam_cracklib.so` (robustezza password al cambio) · `pam_deny.so` + `pam_warn.so` in `/etc/pam.d/other` = default-deny per programmi senza config PAM.
- **2FA ≠ 2SA**: codice OTP via SMS è 2SA (due *passi*), non 2FA (due *fattori distinti*) — SMS intercettabile via MITM. Il dispositivo per il secondo fattore deve essere dedicato (telefono violabile da remoto ≠ "qualcosa che si possiede"). Sbloccare un'app con PIN per OTP = "conoscenza aggiuntiva", non fattore distinto.
- **TOTP**: One-Time Password valida anche solo per una finestra temporale (5s–pochi minuti). App come Google Authenticator sono TOTP.
- **FIDO UAF**: autenticazione senza password — chiave privata sul dispositivo, mai trasmessa; verifica locale (biometria/PIN) sblocca la firma della sfida FIDO. Le informazioni di sicurezza non lasciano il dispositivo.
- **FIDO U2F / YubiKey**: hardware per 2FA via USB/NFC. Origin-check integrato: la YubiKey verifica il dominio prima di firmare → protegge dal phishing (un sito fake non riceve una firma valida per il sito reale). Vulnerabilità WebUSB 2018 (Vervier/Orrù): WebUSB in Chrome permetteva di aggirare l'origin-check via CCID — la sicurezza dell'HW dipende dall'isolamento del contesto software.
- **Scelta password — entropia reale**: `Tr0ub4dor&3` sembra complessa ma ha ~28 bit; `correct horse battery staple` ha ~44 bit. Le stime valgono solo se le scelte sono **veramente casuali** — LLM non sono buoni generatori di entropia (seguono distribuzioni statisticamente prevedibili). Password manager = soluzione pratica.

---

## Ancora Poco Chiaro

- **`try_first_pass` vs `use_first_pass`** (argomenti PAM): `use_first_pass` usa la password del modulo precedente e fallisce se non funziona; `try_first_pass` la tenta ma ri-chiede se fallisce. Concettualmente chiari, ma come si combinano in stack reali va consolidato con esempi (S9 PAM approfondisce).
- **Come FIDO UAF gestisce revoca/riemissione**: cosa succede se il dispositivo viene perso? Il PDF non approfondisce.
- **Salt lunghezza e algoritmi bcrypt**: il PDF menziona SHA-512 (`$6$`) ma non bcrypt — bcrypt è il consiglio moderno. La differenza (key-stretching) non è nel PDF, da approfondire in S14 Crittografia.

---

## Connessioni con Altro

- **SysAdmin 2A → `/etc/shadow`**: i permessi che hai configurato su `/etc/shadow` (`-rw-r----- root shadow`) sono la prima difesa contro il furto offline che `hashcat` sfrutta.
- **SysAdmin 4C LDAP → PAM**: l'integrazione LDAP si fa aggiungendo `pam_ldap.so` allo stack in `/etc/pam.d/` — è esattamente il meccanismo di S2 applicato alla directory centralizzata.
- **S1 Nmap → S2 autenticazione**: Nmap ha trovato porta 22 (SSH) → S2 spiega il meccanismo di autenticazione SSH. Brute force su SSH è bloccato da `pam_tally` / `fail2ban`.
- **S3 Web Security**: SQL injection tipicamente bypassa la query di verifica password applicativa — il layer di autenticazione applicativo è distinto da PAM.
- **S4 Binary Exploits**: buffer overflow può sovrascrivere variabili flag di autenticazione in memoria — autenticazione come perimetro da aggirare.
- **S9 Demoni + Autorizzazione**: PAM = autenticazione; DAC/MAC/RBAC di S9 = autorizzazione. I due livelli AAA sono separati e configurabili indipendentemente.

---

## Esercizi

| Esercizio | Stato | Note |
|---|---|---|
| S1 LAB completo (5 esercizi) | ✅ | Sessione 37 (22/06 pomeriggio) |
| `/appunti S1` | ✅ | File: `claudeAppunti/APPUNTI SECURITY/appunti_moduloS1_*` |
| S2 lezione — lettura su iPad | 🔄 | In corso al momento del handoff |
| S2 autoverifica (6 domande in fondo alla lezione) | ⬜ | Da fare dopo lettura |
| S2 VM/lab | N/A | S2 è modulo teorico puro — nessun lab |

---

## Errori e Misconcezioni

- Nessun errore tecnico questa sessione (output produzione, nessun lab).
- **Distinzione critica per l'esame**: 2FA ≠ 2SA. Il quiz teorico (40%) testa esattamente questa distinzione. Se arriva la domanda "SMS come secondo passo è 2FA?" → **Falso** (è 2SA).
- **AAA**: identificazione ≠ autenticazione — usare lo username come segreto è già un errore di design.

---

## Materiali Usati

### PDF letti questa sessione
- `SLIDE TEORIA/SICINF/Autenticazione_27_febbraio.pdf` — 35 slide integrali (2 batch: pp. 1-18, pp. 19-35)
- `SLIDE TEORIA/SICINF/approfondimento_PAM_-_il_framework_di_autenticazione_e_autorizzazione_.pdf` — 12 pagine integrali

### File prodotti questa sessione
- **NUOVO**: `claudeLezioni/LEZIONI SECURITY/lezione_moduloS2_autenticazione.md` (8 sezioni, ~350 righe)
- **NUOVO PDF**: `claudeLezioni_PDF/LEZIONI SECURITY/lezione_moduloS2_autenticazione.pdf`
- **NUOVO PDF**: `claudeLezioni_PDF/LEZIONI SECURITY/guida_lab_moduloS1_enumerazione_nmap.pdf`
- **NUOVI PDF** (batch): `claudeAppunti_PDF/APPUNTI DIRITTO/` D1-D9 (9 file mai convertiti)
- **NUOVO PDF**: `claudeAppunti_PDF/APPUNTI SECURITY/appunti_moduloS1_*.pdf`
- **MODIFICATO**: `stato/corrente.md` — S2: ⬜ → `🔄 lezione ✅`
- **AUTO-LINKS**: `link_modules.py --apply` → 86 note, 536 archi (S2 aggiunta al cluster Security)

### Script eseguiti
- `link_modules.py --apply` — S2 classificata come Security/S2, blocco AUTO-LINKS scritto
- `pandoc` × 12 — batch PDF (warning su emoji/caratteri speciali, tutti OK)

### Push
- Commit `fb0abe9` su `github.com/lberna777/cockpit` master
- Obiettivo: material disponibile su iPad per lettura di S2

---

## Preferenze e Feedback di Sessione

- **Push immediato per iPad**: Lorenzo studia la lezione sull'iPad dopo la produzione — il workflow è push → leggi su iPad. Tenerlo a mente: al termine di ogni `/lezione` fare push senza aspettare.
- **Nessuna VM oggi**: S2 è teorico puro. La VM si apre per i moduli con lab (S3, S4, S5...).
- **Sessione corta di produzione** (14:44 → ~15:00): lezione S2 prodotta, push, poi Lorenzo ha preso l'iPad. Nessun lavoro SysAdmin questa sessione — 3D Es. 2-6 resta pendente.

---

## Stato Moduli al 23/06

```
Diritto   ██████████  SUPERATO — 30 e lode (16/06)
SysAdmin  ██████░░░░  ~63%  — 3D 🔄 (Es. 1 ✅, Es. 2-6 ⬜) · 3E/3F/4A/4B/4C ⬜
Security  █░░░░░░░░░   ~7%  — S1 ✅ · S2 🔄 (lezione ✅) · S3-S15 ⬜
```

**Scadenze**: SysAdmin **15/07** (22 gg) · Security **17/07** (24 gg)
**Piano settimana corrente** (18/06–30/06): Security S2 → S3 → S4 (entro 30/06). SysAdmin: 3D → 3E → 3F (1.5h/gg).

---

## Dove Stiamo Andando

1. **Oggi (23/06)**: Lorenzo legge `lezione_moduloS2_autenticazione.md` su iPad → risponde alle 6 domande di autoverifica in fondo alla lezione (senza guardare le risposte)
2. **Fine 23/06 o 24/06**: S2 non ha lab — dopo la lettura si passa direttamente a S3.
   - `/lezione S3` (Web Security + OWASP 2025, ha lab con `pentestlab.sh`)
3. **Parallelamente** (ritmo basso): SysAdmin 3D Es. 2-6 → VM Vagrant, `ping`, `ss -tlnp`, `/etc/hosts`, `dig`, `tcpdump` → poi `/appunti 3D` → 3E Vagrant Multi-Machine
4. **Entro 30/06**: S4 Binary Exploits (buffer overflow, ~12h — il più complesso, va sedimentato)
5. **4B SNMP + 4C LDAP** (SysAdmin): non ancora mappati — da affrontare entro prima settimana di luglio

---

## Rischi e Blocchi

- **S4 Binary Exploits** (~12h, x86_32): va iniziato entro questa settimana. Dal 23/06 al 30/06 restano 7 giorni: S3 (~10h) + S4 inizio. Non c'è slack.
- **SysAdmin 4B/4C (SNMP + LDAP)**: non mappati, non scaricati, d'esame — ogni giorno perso è un rischio reale con 22 gg al 15/07.
- **SysAdmin 3D Es. 2-6**: piccolo blocco pendente da sessione 37. Non complesso, ma richiede VM Vagrant accesa. 30–45 min.
- **Vecchia guida-lab S1**: `guida_lab_moduloS1_enumerazione.md` potrebbe esistere ancora accanto alla nuova `guida_lab_moduloS1_enumerazione_nmap.md` → verificare e rimuovere il doppione.

---

## Quick Start Prossima Sessione

```
# Ripristina contesto
Leggi: cockpit/Vault/UniCode/plans/handoffs/HANDOFF_standalone-972162f3_security-s2-lezione_2026-06-23.md

# Verifica stato
/stato        # oppure /sessione per la visione completa

# Prima azione: chiudi S2 (se hai letto la lezione e risposto all'autoverifica)
/sessione security
# → S2 teorico completato, identifica prossimo modulo

# Poi: avvia S3
/lezione S3
# PDF atteso: "SLIDE TEORIA/SICINF/Web_security_6_mar.pdf"
# S3 ha un LAB: "pentestlab.sh start APP" su VM Parrot
# → dopo la lezione: /lab S3

# SysAdmin (in parallelo, 30-45 min):
# Apri VM Vagrant: cd ~/sysAdmin-lab && vagrant up && vagrant ssh
# Esercizi 3D Es. 2-6: ping, ss -tlnp, /etc/hosts, dig, tcpdump
# Poi: /appunti 3D

# Verifica doppio guida-lab S1
ls ~/UniCode/claudeLezioni/LEZIONI\ SECURITY/guida_lab_moduloS1*.md
# Se esistono DUE file → tieni guida_lab_moduloS1_enumerazione_nmap.md, elimina l'altro

# Domanda di autoverifica S2 (rispondi senza guardare la lezione):
# "Un codice OTP ricevuto via SMS in aggiunta alla password è 2FA vera o 2SA?"
# (Risposta: 2SA — SMS è vulnerabile a MITM, non è un fattore "possesso" affidabile)
```
