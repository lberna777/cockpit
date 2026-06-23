# Security S2 — Appunti definitivi completati, prossimo: SysAdmin 3D Es. 2-6

**Date:** 2026-06-23
**Status:** IN CORSO
**Corso:** Lab Sicurezza Informatica T + Lab Amministrazione di Sistemi T
**Modulo:** S2 ✅ completato — SysAdmin 3D prossimo
**Chain:** `standalone-972162f3` seq `4`
**Parent:** `HANDOFF_standalone-972162f3_security-s2-lezione_2026-06-23.md` (seq 3)
**Prior chain:** `security-s1-setup 18/06` > `security-s1-guida-lab 22/06` > `security-s2-lezione 23/06` > questo

---

## Obiettivo della Sessione

Sessione del 23/06 pomeriggio (ore 17 circa). Partenza dal parent (seq 3): Lorenzo aveva letto la lezione S2 su iPad durante il giorno. Questa sessione ha elaborato gli appunti grezzi S2 (`/appunti S2`), portando S2 a ✅. La prossima azione immediata è SysAdmin 3D Es. 2-6 (VM Vagrant, ~45 min), pendente dalla sessione 37.

---

## Cosa Cambia Rispetto al Parent

**Parent (seq 3) → questa sessione (seq 4):**
- Lezione S2 letta su iPad ✅ (previsto nel parent)
- `/appunti S2` eseguito → `appunti_moduloS2_autenticazione.md` creato
- Autoverifica S2: 4/6 ✅ al primo tentativo; Q4 (required vs requisite) e Q5 (S-KEY) "non capito" → chiariti negli appunti
- S2 → `✅ Sessione 38` in `corrente.md`; Security: 13% (2/15)
- `errori_frequenti.md`: nuovo pattern "autenticazione/autorizzazione in Security" + pattern "FIDO come standard per l'autorizzazione → errore"
- `link_modules.py --apply`: 87 note, 541 archi — S2 appunti collegati a lezione S2

**Doppione guida-lab S1** (rischio segnalato nel parent): verificato → esiste solo `guida_lab_moduloS1_enumerazione_nmap.md`. Nessun doppione.

---

## Concetti Assimilati (S2 — Autenticazione)

Tutte le domande aperte degli appunti grezzi sono state risolte inline. Concetti consolidati questa sessione:

- **AAA formulata correttamente**: identificazione (nome dichiari) ≠ autenticazione (prova) ≠ autorizzazione (permessi su oggetto). Il collegamento PAM/sudo per Linux è corretto nel contesto SysAdmin.
- **4 fattori**: conosce/possiede/è/fa — e il GPS come segnale contestuale, non fattore di accesso primario. Correttamente capito.
- **HSM (domanda aperta risolta)**: dispositivo hardware dedicato a operazioni crittografiche con auto-distruzione su manomissione. Forme: rack 1U enterprise (Thales Luna, AWS CloudHSM), smart card, USB. Il pepper vive nell'HSM, il disco può essere rubato senza rivelare il segreto.
- **Entropia password (domanda aperta risolta)**: formula `lunghezza × log₂(pool_size)`. Entropia teorica ≠ reale: `Tr0ub4dor&3` ~28 bit (pattern prevedibile), `correct horse battery staple` ~44 bit (4 parole casuali da 2048). LLM non producono buona entropia (distribuzioni statisticamente prevedibili).
- **Autenticazione attiva (confusione chiarita)**: Lorenzo pensava fosse una sorta di 2FA — non lo è. Non cambia il numero di fattori, cambia *cosa viene inviato sul canale*. Passiva = mandi il segreto. Attiva = mandi una prova che lo conosci, diversa ogni volta. Analogia: giudice che chiede "terzo carattere + numero sul dado".
- **S-KEY ratchet (domanda Q5 risolta)**: chi intercetta `h^(k-1)(N)` ha già un token consumato. Per la prossima serve `h^(k-2)(N)`, calcolabile solo invertendo l'hash — impossibile. L'hash va solo in avanti.
- **Challenge-response SSH**: V cifra nonce con PUB_P → P decifra con PRIV_P → rimanda nonce. PRIV_P non lascia mai il dispositivo. `~/.ssh/authorized_keys` = dove V memorizza PUB_P — collegamento con SysAdmin già noto.
- **PAM module-type** (domanda aperta risolta): `auth` (verifica identità) / `account` (controlli non-password) / `session` (setup sessione) / `password` (cambio credenziali).
- **PAM control-flag** (domanda Q4 risolta): `required` = fallimento mascherato, stack continua; `requisite` = fallimento immediato, stack termina; `sufficient` = successo immediato se nessun required precedente ha fallito; `optional` = ignorato. Ordine dei moduli non è decorativo — same config, ordine invertito = logica completamente diversa.
- **2FA vs 2SA**: SMS/email come secondo passo = 2SA (canale intercettabile via MITM). "Sbloccare app con PIN per ottenere OTP" = conoscenza aggiuntiva, non secondo fattore distinto.
- **FIDO UAF**: biometria/PIN sblocca chiave privata locale → firma sfida server. Segreti non lasciano il dispositivo.
- **FIDO U2F + origin-check**: YubiKey verifica il dominio prima di firmare → anti-phishing integrato. Vulnerabilità 2018: WebUSB aggirava origin-check via CCID — sicurezza HW dipende dall'isolamento software circostante.

---

## Ancora Poco Chiaro

- **`try_first_pass` vs `use_first_pass`** (argomenti PAM): `use_first_pass` usa password del modulo precedente e fallisce se non funziona; `try_first_pass` la tenta ma ri-chiede se fallisce. Concettualmente chiari, ma stack reali con esempi vanno consolidati in S9 (PAM approfondito).
- **FIDO UAF revoca**: cosa succede se il dispositivo viene perso? La sessione non l'ha approfondito — non è nel PDF.
- **bcrypt vs SHA-512**: il PDF usa SHA-512 (`$6$`), bcrypt è il consiglio moderno (key-stretching iterativo). Differenza dettagliata in S14 Crittografia.

---

## Errori e Misconcezioni

- **FIDO "autorizzazione a doppia chiave"** (appunti grezzi): FIDO riguarda l'*autenticazione*, non l'autorizzazione. "Doppia chiave" è impreciso — è crittografia asimmetrica per autenticazione forte. → Aggiunto a `errori_frequenti.md`: pattern "autenticazione/autorizzazione" per Security (la distinzione AAA è corretta in teoria ma scivola nella descrizione di sistemi concreti).
- **Q4 e Q5 autoverifica**: "non ho capito l'argomento" per required/requisite e S-KEY. Chiariti inline negli appunti. Non erano errori tecnici ma lacune di spiegazione — la lezione non entrava nel dettaglio.
- **Distinzione critica per l'esame (valida da parent)**: 2FA ≠ 2SA. SMS = 2SA. Quiz teorico (40%) testa esattamente questo.

---

## Esercizi

| Esercizio | Stato | Note |
|---|---|---|
| S2 lezione — lettura su iPad | ✅ | Fatta durante il giorno, prima di questa sessione |
| S2 autoverifica (6 domande) | ✅ | 4/6 al primo tentativo; Q4+Q5 chiarite negli appunti |
| `/appunti S2` | ✅ | `appunti_moduloS2_autenticazione.md` completato |
| SysAdmin 3D Es. 2-6 | ⬜ | **Prossima azione immediata** (VM Vagrant, ~45 min) |

---

## File Prodotti / Modificati (non ancora committati)

| File | Tipo | Modifica |
|---|---|---|
| `claudeAppunti/APPUNTI SECURITY/appunti_moduloS2_autenticazione.md` | NUOVO | Appunti definitivi S2 + 3 domande aperte risolte |
| `claudeLezioni/LEZIONI SECURITY/lezione_moduloS2_autenticazione.md` | MODIFICATO | AUTO-LINKS aggiornati da link_modules.py |
| `stato/corrente.md` | MODIFICATO | S2 → ✅ sessione 38; Security 13%; prossimi passi → S3 |
| `stato/errori_frequenti.md` | MODIFICATO | Tabella Security: pattern FIDO + pattern autenticazione/autorizzazione |
| `stato/log_sessioni.md` | MODIFICATO | Sessione 38 aggiunta (in corso) |

**Git**: tutto non committato — commit + push da fare a fine sessione SysAdmin.

---

## Stato Moduli al 23/06 ore 17

```
Diritto   ██████████  SUPERATO — 30 e lode (16/06)
SysAdmin  ██████░░░░  ~63%  — 3D 🔄 (Es. 1 ✅, Es. 2-6 ⬜) · 3E/3F/4A/4B/4C ⬜
Security  ██░░░░░░░░  ~13%  — S1 ✅ · S2 ✅ · S3–S15 ⬜
```

**Scadenze**: SysAdmin **15/07** (22 gg) · Security **17/07** (24 gg)
**Ritmo**: ~4h Security + ~1.5h SysAdmin al giorno costanti

---

## Dove Stiamo Andando

1. **Adesso (17:00–18:30)**: SysAdmin 3D Es. 2-6 su VM Vagrant
   - `cd ~/sysAdmin-lab && vagrant up && vagrant ssh`
   - Esercizi: `ping`, `ss -tlnp`, `/etc/hosts`, `dig`, `tcpdump`
   - Poi `/appunti 3D`
2. **24/06**: `/lezione S3` Web Security (PDF: `Web_security_6_mar.pdf`, è in SLIDE TEORIA/SICINF/)
3. **24–25/06**: `/lab S3` (pentestlab.sh, VM Parrot, ⭐ tipo esame Web vulnerabilities)
4. **Entro 30/06**: S4 Binary Exploits iniziato (~12h totali — il più complesso, va sedimentato)
5. **Parallelo SysAdmin**: 3E Vagrant Multi-Machine → 3F Ansible → 4B SNMP → 4C LDAP

---

## Rischi e Blocchi

- **S4 Binary Exploits**: dal 23/06 al 30/06 restano 7 giorni. S3 (~10h) + S4 inizio. Nessun slack — iniziare S3 domani al più tardi.
- **SysAdmin 4B/4C (SNMP + LDAP)**: non mappati, non scaricati, d'esame — rischio reale con 22 gg al 15/07.
- **Git**: commit pendente con appunti S2, stato corrente, errori frequenti, log sessioni — fare dopo questa sessione SysAdmin.

---

## Materiali Usati Questa Sessione

### File appunti grezzi
- `APPUNTI GREZZI/Lab - Security/Appunti_grezzi_lezioneS2.md` — appunti di Lorenzo, con 3 domande aperte inline e autoverifica (4/6 + 2 "non capito")

### Lezione di riferimento (già prodotta nel parent)
- `claudeLezioni/LEZIONI SECURITY/lezione_moduloS2_autenticazione.md` — 8 sezioni, ~350 righe

### File di stato letti
- `stato/corrente.md`, `stato/errori_frequenti.md`, `stato/log_sessioni.md`

### Script eseguiti
- `link_modules.py --apply` — 87 note, 541 archi; S2 appunti → lezione collegati

---

## Quick Start Prossima Sessione

```
# Ripristina contesto
Leggi: cockpit/Vault/UniCode/plans/handoffs/HANDOFF_standalone-972162f3_security-s2-appunti_2026-06-23.md

# Prima azione: apri VM SysAdmin e fai Es. 2-6
cd ~/sysAdmin-lab && vagrant up --provider=virtualbox && vagrant ssh
# Poi esegui in ordine: ping, ss -tlnp, /etc/hosts, dig, tcpdump
# (guida: claudeLezioni/LEZIONI SYSADM/guida_lab_modulo3D_networking_base.md se esiste)

# Dopo Es. 2-6: appunti definitivi
/appunti 3D

# Poi: Security S3
/lezione S3
# PDF atteso: SLIDE TEORIA/SICINF/Web_security_6_mar.pdf
# S3 ha LAB con pentestlab.sh su VM Parrot → dopo la lezione: /lab S3

# Verifica: git commit + push a fine sessione
# (file da committare: appunti S2, corrente.md, errori_frequenti.md, log_sessioni.md)
```

## Session Closed
**Closed at:** 2026-06-23 ~17:15
**Commit:** 320d0f8
**Session status:** Handed off to next session
