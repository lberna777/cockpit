# Security S1 — Guida-lab prodotta, prossimo: eseguire lab + /appunti S1

**Date:** 2026-06-22
**Status:** IN CORSO
**Corso:** Lab Sicurezza Informatica T
**Modulo:** S1 — Principi Offensive Security + LAB Enumerazione
**Chain:** `standalone-972162f3` seq `2`
**Parent:** `HANDOFF_standalone-972162f3_security-s1-setup_2026-06-18.md`
**Prior chain:** `security-s1-setup 18/06` > questo

---

## Obiettivo della Sessione

Sessione del 22/06, 13:46. Lorenzo aveva già letto + evidenziato la lezione S1 e prodotto
gli appunti grezzi S1. L'obiettivo era produrre la guida-lab operativa di S1 con `/lab S1`
e pianificare il pomeriggio (pausa pranzo → lab su VM dalle ~14:30 alle 18:30).

---

## Concetti Assimilati

*(Già consolidati nel parent; questa sessione era tooling, non studio nuovo. Aggiunte minori:)*

- **Differenza lezione vs guida-lab**: la lezione spiega il *perché* in prosa discorsiva; la guida-lab è un walkthrough passo-passo con comandi esatti + anatomia + output atteso. Per Security servono entrambe.
- **Flusso appunti S1 chiarito**: appunti grezzi della lezione → `/appunti S1` ORA (teoria matura, indipendente dal lab); durante il lab → annotare inline nella guida-lab con blockquote `>` + emoji ❓/✅/⚠️; dopo il lab → update appunti se necessario.
- **Guida-lab S1 — 5 esercizi in progressione** [fonte: LAB_Enumerazione_25feb.html]:
  1. Host discovery (`sudo nmap -sn 192.168.56.0/24`) → trova IP dei 3 target
  2. Port scan completo (`nmap -sT -p-`) poi version detection (`nmap -sV -p <porte>`)
  3. Banner grabbing SMTP (`nc <ip> 25`) + DB PostgreSQL esposto (`psql -U admin -h <ip> -W`)
  4. Accesso SSH con credenziali estratte + brute force PIN (`hydra -l root -x 4:4:1 ssh://<ip>:1337`)
  5. Hash cracking (`scp` backup da VM → `cupp` wordlist custom → `john` cracking)

---

## Cosa Cambia Rispetto al Parent (18/06)

Il parent 18/06 documentava una sessione di *setup e planning*: nessun lab eseguito, guida-lab
già esistente ma incompleta (solo fix snapshot), skill `/studia` appena creata e non testata.

Questa sessione (22/06) ha **sostituito** la guida-lab con una nuova produzione completa:
- vecchia: `guida_lab_moduloS1_enumerazione.md` (prodotta prima del 18/06, solo corretta)
- nuova: `guida_lab_moduloS1_enumerazione_nmap.md` (creata 22/06 — leggendo i PDF integralmente)
  → 5 esercizi strutturati con anatomia di ogni comando, threat model, ⚠️ errori integrati

**Chiarimento flusso appunti** (non definito nel parent):
- Appunti grezzi *lezione* (già scritti) → `/appunti S1` ORA, prima del lab
- Durante il lab → annotazione inline nella guida-lab (blockquote `>` + ❓✅⚠️)
- Dopo il lab → aggiornamento appunti se emergono osservazioni significative
- **Alternativa rifiutata**: fare `/appunti S1` dopo il lab (rischio: la teoria si mescola con
  l'esperienza VM e si produce un file ibrido meno chiaro da ripassare)

**Directory nuova in APPUNTI GREZZI/**: git status mostra `?? "APPUNTI GREZZI/Lab - Security/"` —
Lorenzo ha già creato una cartella per gli appunti grezzi del lab (presumibilmente durante la lettura
della lezione o durante questa sessione). Verificare il contenuto all'inizio della prossima sessione.

---

## Ancora Poco Chiaro

- **DA FARE del LAB**: sezioni marcate "DA FARE" nel PDF non sono state coperte nella guida-lab
  (smtp-user-enum, enum4linux-ng per SMB su 139/445, Greenbone VA). Lorenzo deciderà se affrontarle
  o tralasciarle — non sono requisiti stretti per l'esame.
- **Greenbone**: il PDF lo menziona come esercitazione da completare (VA su 3 target). Dipende dal
  fatto che sia installato nella VM. Da verificare live.
- **IP reali vs esempi**: gli IP .32/.33/.34 del PDF sono esempi del prof. I veri IP li trovi con
  `sudo nmap -sn` — dipendono dalla tua installazione VirtualBox.

---

## Connessioni con Altro

*(Invariate rispetto al parent — si rimanda al parent per il dettaglio)*

- SysAdmin 3A: i servizi systemd configurati = quello che Nmap vede dall'esterno
- SysAdmin 3D: `ip a` / `ss -tlnp` dal dentro = equivalente interno di Nmap dall'esterno
- S3 Web Security: porte 80 (t-1, t-3) e 8001/Werkzeug (t-3) sono i target del prossimo LAB web
- S10 NIDS Suricata: le scansioni Nmap di S1 generano esattamente il traffico che Suricata rileva

---

## Esercizi

| Esercizio | Stato | Approccio usato | Note |
|---|---|---|---|
| S1 LAB Es. 1 — Host discovery | ⬜ | — | `sudo nmap -sn` sulla subnet vboxnet0 |
| S1 LAB Es. 2a — Port scan -p- | ⬜ | — | `nmap -sT -p-` su range IP trovati |
| S1 LAB Es. 2b — Version detection | ⬜ | — | `nmap -sV -p <porte>` per ogni target |
| S1 LAB Es. 3a — Banner grabbing SMTP | ⬜ | — | `nc <ip_t2> 25` → banner rivela Postgres |
| S1 LAB Es. 3b — DB PostgreSQL esposto | ⬜ | — | `psql -U admin -h <ip> -W accounts_db` → `\dt` → `SELECT * FROM accounts;` |
| S1 LAB Es. 4 — SSH + hydra PIN | ⬜ | — | 4 servizi SSH; `hydra -l root -x 4:4:1 ssh://<ip>:1337` |
| S1 LAB Es. 5 — Hash cracking | ⬜ | — | `scp` → `cupp -i` → `unshadow` → `john --wordlist` |
| `/appunti S1` | ⬜ | — | Appunti grezzi lezione già pronti; da lanciare PRIMA del lab |

---

## Errori e Misconcezioni

- **Due guida-lab S1**: il parent (18/06) aveva già una guida-lab `guida_lab_moduloS1_enumerazione.md`
  (verificata + corretta in quella sessione). Questa sessione ha creato una NUOVA guida-lab:
  `guida_lab_moduloS1_enumerazione_nmap.md`. Verificare all'inizio della prossima sessione se la
  vecchia esiste ancora e se le due sono duplicate o complementari — se la nuova è completa, eliminare
  la vecchia per non avere ambiguità.
- **Errori frequenti S1 già registrati in errori_frequenti.md** (tutti integrati come ⚠️ nella guida):
  - `-p 22 80` → spazio = tratta extras come host; usare virgola `-p 22,80`
  - `-sT` vs `-sV`: `-sT` = aperta/chiusa; `-sV` = legge il banner con versione
  - Nmap senza `-p-` → si perde porte non-standard (es. SSH su 1337)
  - `sudo nmap -sn` → senza sudo non usa ARP su host-only
  - `\dt SELECT *` su stessa riga in psql → `\dt` è meta-comando, `SELECT` è SQL: righe separate
  - Buffer sporco psql (prompt `->`) → `\r` per reset
  - `scp` da dentro SSH → aprire nuovo terminale locale
  - `scp` con SFTP subsystem disabilitato → `ssh -p 1337 user@ip "cat /file" > file`

---

## Materiali Usati

### PDF letti questa sessione
- `SLIDE TEORIA/SICINF/Principi_delloffensive_security_20_febbraio.pdf` — 53 slide integrali
  (lette in 3 batch: 1-20 via tool, 21-40 e 41-53 via screenshot forniti da Lorenzo)
- `SLIDE LAB/SICINF/LAB_Enumerazione_25feb.html` — estratto testo (1.6 MB, immagini strip), 6 sezioni

### File prodotti questa sessione
- **NUOVO** (untracked): `claudeLezioni/LEZIONI SECURITY/guida_lab_moduloS1_enumerazione_nmap.md`
  — 5 esercizi + threat model + anatomia completa + ⚠️ errori frequenti integrati
- **MODIFICATO**: `lezione_moduloS1_offensive_security_enumerazione.md` (+1 blocco AUTO-LINKS da link_modules.py)
- **MODIFICATO**: `stato/corrente.md` — aggiornata nota S1: "lezione ✅ · appunti grezzi ✅ · guida-lab ✅ (22/06)"

### Script eseguiti
- `link_modules.py --apply` → S1: 2 note collegate (lezione ↔ guida-lab)

---

## Preferenze e Feedback di Sessione

- **Non ha aperto la VM oggi**: la sessione era interamente di produzione output (guida-lab), non lab live. La VM si apre nel pomeriggio dopo la pausa pranzo (14:30).
- **Appunti grezzi lezione → convertire subito**: Lorenzo ha confermato che ha senso fare `/appunti S1` PRIMA del lab (teoria già matura, indipendente dall'esecuzione).
- **Annotazione inline durante il lab**: conferma del metodo scelto nella sessione 18/06 — blockquote `>` con ❓✅⚠️ nella guida-lab, `/studia` per checkpoint.

---

## Stato Moduli al 22/06

```
Diritto   ██████████  SUPERATO — 30 e lode (16/06)
SysAdmin  ██████░░░░  ~63%  — 3D 🔄 (Es. 1 ✅, Es. 2-6 ⬜) · 3E/3F/4A/4B/4C ⬜
Security  ░░░░░░░░░░   ~0%  — S1 🔄: lezione ✅ · grezzi ✅ · guida-lab ✅ · lab ⬜
```

**Scadenze**: SysAdmin **15/07** (23 gg) · Security **17/07** (25 gg)
**Ritmo richiesto**: ~5h/gg senza giorni vuoti.

---

## Dove Stiamo Andando

1. **Pomeriggio 22/06** (14:30–18:30 ~4h):
   - `/appunti S1` (teoria grezzi → raffinati, ~30 min)
   - Apri VM + 3 target → segui `guida_lab_moduloS1_enumerazione_nmap.md` esercizio per esercizio (~3h)
   - Annota inline con blockquote; usa `/studia S1` per checkpoint
2. **Fine 22/06 o 23/06**: `/chiudi` per registrare S1 LAB completato se finisci
3. **23/06**: S2 Autenticazione (teoria leggera, ~5h) → S3 Web Security
4. **Fine giugno**: S4 Binary Exploits (il più complesso: ~12h)
5. **SysAdmin parallelo**: 3D Es. 2-6 → 3E Vagrant Multi-Machine → 3F Ansible (ritmo 1.5h/gg)

---

## Rischi e Blocchi

- **Due guida-lab S1** (vedi sopra): chiarire prima di iniziare il lab quale usare.
- **VM targets non ancora create**: le 3 VM da `/opt/owa` non sono mai state create — Fase 1
  della guida richiede ~20 min di setup VirtualBox prima di poter iniziare le scansioni Nmap.
- **S4 Binary Exploits** (~12h): va affrontato entro fine giugno. Dal ritmo attuale si ha ancora
  margine ma non si può perdere giorni.
- **SysAdmin 4B SNMP + 4C LDAP**: non mappati, non scaricati, non studiati — sono d'esame (23 gg).

---

## Quick Start Prossima Sessione

```
# Ripristina contesto
Leggi: cockpit/.claude/handoffs/HANDOFF_standalone-972162f3_security-s1-guida-lab_2026-06-22.md

# Prima azione (PRIMA di aprire la VM)
/appunti S1
# → converte gli appunti grezzi lezione S1 in appunti definitivi (~30 min)

# Poi: verifica guida-lab
ls ~/UniCode/claudeLezioni/LEZIONI\ SECURITY/guida_lab_moduloS1*.md
# Se esistono DUE file (enumerazione.md + enumerazione_nmap.md) → eliminare il vecchio
# Il file da seguire è: guida_lab_moduloS1_enumerazione_nmap.md

# Poi: avvia VM e target
VBoxManage startvm "LabSicurezzaInformatica"
# → segui Setup nella guida-lab: 3 VM da /opt/owa, host-only vboxnet0, snapshot prima di avviare
# → verifica DHCP su vboxnet0: VirtualBox → Ctrl+H → spunta DHCP

# Skill da usare durante il lab
/studia S1
# → ogni volta che hai output inatteso, dubbio su un comando, o vuoi conferma

# Verifica comprensione prima della Fase 2
Sai dire la differenza tra nmap -sT e nmap -sV?
(Risposta: -sT = TCP connect, dice solo aperta/chiusa; -sV = legge il banner, identifica versione)
```

---

## Session Closed
**Closed at:** 2026-06-22 ~14:00
**Commit:** c06cba5
**Session status:** Handed off to next session
