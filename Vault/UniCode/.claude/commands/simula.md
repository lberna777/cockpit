---
description: "Simulazione d'esame. Genera domande cross-modulo per una materia o usa simulazioni passate. Uso: /simula [materia]"
argument-hint: "materia — sysadmin | diritto | security"
---

La materia richiesta è: $ARGUMENTS

**Rileva la materia:**
- contiene "dir" → **Diritto**
- contiene "sys" → **SysAdmin**
- contiene "sec" → **Security**
- vuoto o non riconosciuto → mostra opzioni valide, fermati

---

**1. Carica il contesto**

Leggi in parallelo:
- `stato/corrente.md` — per sapere quali moduli sono ✅
- `stato/errori_frequenti.md` — per domande mirate
- `stato/tracker_ripasso.md` — per identificare moduli meno freschi

Solo per SysAdmin: cerca anche `SIMULAZIONI ESAMI/SYSADM/` per esami passati.

---

**2. Verifica fattibilità**

Servono almeno 3 moduli ✅ nella materia per una simulazione significativa. Se non ci sono abbastanza moduli, comunicalo e suggerisci `/ripassa` sui singoli moduli.

---

**3. Genera la simulazione**

### Modalità Diritto

Genera **8 domande aperte** che coprono trasversalmente tutti i moduli completati:
- 3 domande di definizione/classificazione (es. "Definisci X e classificane le tipologie")
- 2 domande di confronto (es. "Distingui X da Y, indicando la base normativa di ciascuno")
- 2 domande applicative (es. "In questo scenario, quale disciplina si applica?")
- 1 domanda avanzata di sintesi (es. "Come interagiscono X, Y e Z nel contesto di...?")

Ogni domanda deve richiedere la citazione della norma specifica. Almeno 2 domande devono testare errori ricorrenti da errori_frequenti.md.

### Modalità SysAdmin

Se esiste un PDF di simulazione esame in `SIMULAZIONI ESAMI/SYSADM/`:
- Leggilo e presentalo a Lorenzo come esercizio
- Fornisci le istruzioni per la VM

Se non esiste (o Lorenzo preferisce domande nuove):
- Genera **6 task pratici** che coprono moduli diversi:
  - 2 task di scripting bash (variabili, loop, funzioni, pipe)
  - 2 task di amministrazione (utenti, permessi, servizi, pacchetti)
  - 1 task di networking
  - 1 task combinato (es. "scrivi uno script che monitora X e invia log a Y")
- Ogni task ha criteri di valutazione espliciti

### Modalità Security

Genera **5 scenari** progressivi:
- Scenario 1: enumerazione di un target (cosa cerchi? con quali tool?)
- Scenario 2: analisi di una vulnerabilità trovata (come la sfrutti? come la mitighi?)
- Scenario 3-5: basati sui moduli completati

---

**4. Esecuzione**

Presenta gli esercizi/domande uno alla volta. Per ogni risposta:
- Valuta la completezza (0-3 punti: incompleta/parziale/corretta/eccellente)
- Segnala elementi mancanti con riferimento al materiale
- Per SysAdmin: se il task richiede VM, chiedi a Lorenzo di eseguirlo e riportare l'output

---

**5. Valutazione finale**

```
## Risultato simulazione — [Materia]
Data: [data odierna]
Moduli coperti: [lista]

Punteggio: X/Y punti (Z%)

**Aree solide**: [concetti dimostrati con sicurezza]
**Aree critiche**: [concetti deboli — con modulo e sezione appunti di riferimento]
**Consiglio**: [cosa ripassare prima dell'esame, in ordine di priorità]
```

Se il punteggio è < 60%: suggerire un piano di ripasso mirato con i moduli da rivedere.
