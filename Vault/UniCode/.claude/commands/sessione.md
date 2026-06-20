---
description: "Avvia o cambia il focus della sessione di studio. Uso: /sessione [materia]  (es. /sessione, /sessione diritto, /sessione sysadmin, /sessione security)"
argument-hint: "materia opzionale — sysadmin | diritto | security | (vuoto = panoramica generale)"
---

Il parametro passato è: "$ARGUMENTS"

**Rileva il focus richiesto:**
- `$ARGUMENTS` vuoto → modalità **generale** (tutte le materie)
- contiene "dir" → focus **Diritto**
- contiene "sys" → focus **SysAdmin**
- contiene "sec" → focus **Security**
- altro → avvisa parametro non riconosciuto, mostra opzioni valide, fermati

**Rileva se la sessione è già in corso:**
Controlla se `stato/corrente.md` è già stato letto in questa conversazione. Se sì, usa i dati già in contesto e segnala a Lorenzo che stai cambiando focus senza ricaricare.

---

**1. Leggi lo stato** *(solo se non già letto)*
Leggi `stato/corrente.md` integralmente.

---

**2. Mostra lo stato dei moduli**

*Focus generale* — tabella raggruppata per corso (SysAdmin, Security, Diritto) con stato ✅/🔄/⬜.

*Focus specifico* — mostra solo i moduli di quella materia, con più dettaglio: se un modulo è 🔄, elenca lo stato interno degli esercizi.

---

**3. Identifica il punto di ripresa**

Dalla sezione "Prossimi Passi" di corrente.md.

*Focus generale*: una riga per materia.
*Focus specifico*: solo la materia richiesta, in evidenza.

---

**4. Proponi il piano per questa sessione**

Sulla base del focus e del punto di ripresa:
- Modulo da affrontare (ID, nome)
- Obiettivo concreto

*Per SysAdmin/Security*:
- Sequenza esercizi/comandi
- Se modulo nuovo: ricorda `/lezione <ID>` prima della VM

*Per Diritto*:
- Concetti da consolidare
- Se modulo nuovo: ricorda `/lezione <ID>` + autoverifica
- Se modulo in corso: da quale concetto riprendere

---

**5. Verifica PDF** *(solo per il modulo da affrontare oggi)*

Controlla che il PDF necessario sia presente nella cartella corretta. Se manca, fermati e comunicane il titolo.

---

**6. Prossima cosa da fare**

Leggi `ESAMI SCELTI.md` e `stato/tracker_ripasso.md`. Calcola i giorni mancanti a ciascun esame.

Identifica la **prossima singola cosa da fare** secondo questa priorità:
1. Ripasso scaduto (da tracker_ripasso.md) — se presente, va per primo (15-20 min)
2. In focus specifico: prossimo passo di quella materia
3. In focus generale: materia più a rischio (moduli rimasti / giorni rimasti)

Mostra:

```
**Prossima cosa — [DATA]**

[Materia] · ~Xh
[Modulo ID] — [azione concreta]

(Solo se presente: un segnale di rischio in una riga)
```

**Segnali di rischio** (solo se presenti, in una riga):
- Scadenza vicina con troppi moduli aperti
- Ripasso scaduto

---

**7. Esclusione moduli già fatti oggi**

Se la sessione è già in corso e Lorenzo sta cambiando focus, non riproporre moduli/esercizi già completati in questa conversazione.
