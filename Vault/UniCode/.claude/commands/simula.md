---
description: "Simulazione d'esame: usa una prova passata se esiste, altrimenti genera domande cross-modulo. Uso: /simula <CODICE>"
argument-hint: "<CODICE> corso — es. FI2, SO, CA"
---

Il parametro passato è: "$ARGUMENTS"

---

**0. Risolvi il corso**

`$ARGUMENTS` è il **codice del corso**, validato contro `piano/codici.txt`. Se è vuoto o non
riconosciuto, mostra i codici dal file e fermati. Se è vuoto ma il briefing indica un
esame attivo, proponi quello e chiedi conferma.

---

**1. Carica il contesto — in parallelo**

- `corsi/<COD>/percorso.md` — quali moduli sono chiusi
- `corsi/<COD>/fonti.md` — quali prove passate sono state reperite e quali mancano
- `profilo/errori.md` — per le domande mirate
- `stato/tracker.md` — per individuare i moduli meno freschi, da coprire per primi
- Il contenuto di `corsi/<COD>/prove/`

---

**2. Verifica fattibilità**

Servono almeno **3 moduli chiusi** perché una simulazione sia significativa. Se non ci sono,
comunicalo e suggerisci `/ripassa` sui singoli moduli.

---

**3. Scegli la modalità**

**Se in `corsi/<COD>/prove/` esiste una prova passata non ancora svolta**, usa quella: è
sempre preferibile a domande generate. Presentala come all'esame, con il tempo previsto, e
tieni la soluzione ufficiale per il confronto successivo. Non anticiparla.

**Altrimenti genera la prova**, nella forma che il corso usa davvero — la dice
`corsi/<COD>/percorso.md`, non va indovinata:

*Prova scritta discorsiva* — 8 domande aperte trasversali ai moduli chiusi: 3 di
definizione o classificazione, 2 di confronto fra concetti vicini, 2 applicative su uno
scenario, 1 di sintesi. Ogni domanda richiede il riferimento esatto.

*Prova con esercizi formali* — 6 esercizi che coprono moduli diversi, con la distribuzione di
difficoltà della prova reale e i criteri di valutazione espliciti per ciascuno.

*Prova pratica di laboratorio* — 6 task su moduli diversi, ciascuno con criteri di valutazione
espliciti e l'elenco dei deliverable richiesti. Lorenzo esegue sull'ambiente e riporta l'output.

*Quiz a risposta chiusa* — il numero di domande della prova reale, con il **punteggio negativo
per risposta errata** se il corso lo prevede: dichiaralo prima di iniziare.

In tutti i casi: almeno **2 domande devono testare errori ricorrenti** da `profilo/errori.md`,
e la copertura deve privilegiare i moduli con il ripasso più vecchio.

---

**4. Esecuzione**

Presenta gli item **uno alla volta**. Per ciascuna risposta:
- Valuta su **0-3 punti**: incompleta / parziale / corretta / eccellente
- Segnala gli elementi mancanti con il riferimento al materiale
- Per i task pratici: chiedi a Lorenzo di eseguirli e riportare l'output, non eseguirli tu

---

**5. Valutazione finale**

```
## Risultato simulazione — <COD>
Data: [oggi]
Moduli coperti: [lista]

Punteggio: X/Y punti (Z%)

**Aree solide**: [concetti dimostrati con sicurezza]
**Aree critiche**: [concetti deboli, con modulo e sezione di riferimento]
**Consiglio**: [cosa ripassare prima dell'esame, in ordine di priorità]
```

**Sotto il 60%**: non fermarti al punteggio, proponi un piano di ripasso mirato con i moduli da
rivedere nell'ordine in cui vanno ripresi.

---

**6. Registra l'evento**

Appendi a `stato/giornata.md`:

```
HH:MM · <COD> · simulazione: X/Y punti (Z%), moduli <lista>.
```

Per ogni modulo che la simulazione ha mostrato debole, aggiungi anche il marcatore di ripasso,
così il tracker lo riporta indietro di un gradino:

```
RIPASSO <COD> <ID> debole
```

E per quelli risultati solidi, se erano in scadenza:

```
RIPASSO <COD> <ID> ok
```

> Il tracker non va modificato a mano: lo aggiorna `scripts/giornata.py` alle 23 da questi
> marcatori.

Se sono emerse debolezze nuove, aggiornale in `profilo/errori.md`.
