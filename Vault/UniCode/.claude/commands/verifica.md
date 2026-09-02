---
description: "Verifica qualità di una lezione o di appunti generati: confronta con la fonte e segnala i gap. Uso: /verifica <CODICE> <ID>"
argument-hint: "<CODICE> <ID modulo> — es. FI2 3A"
---

Il parametro passato è: "$ARGUMENTS"

---

**0. Risolvi corso e modulo**

Due token: `<CODICE> <ID modulo>`, il codice validato contro `piano/codici.txt`.

---

**1. Identifica i file da verificare**

- Lezione: `corsi/<COD>/lezioni/lezione_<ID>_*.md`
- Guida-lab: `corsi/<COD>/lezioni/guida_lab_<ID>_*.md`
- Appunti definitivi: `corsi/<COD>/appunti/appunti_<ID>_*.md`

Se non esiste nessuno dei tre, comunicalo e fermati.

---

**2. Identifica la fonte**

Da `corsi/<COD>/percorso.md` recupera il materiale assegnato al modulo e leggilo da
`corsi/<COD>/materiali/`.

Se la fonte non è disponibile, **dillo esplicitamente nel report**: la verifica si riduce alla
coerenza interna (salta il passo 3) e non può dire nulla sulla copertura. Una verifica senza
fonte che non lo dichiara è peggio di nessuna verifica.

Controlla anche `corsi/<COD>/fonti.md`: se il materiale è di un'annata diversa da quella in cui
il corso era in piano, la copertura va valutata rispetto al programma giusto, e le differenze
vanno segnalate come tali — non come lacune dell'output.

---

**3. Confronto con la fonte**

Per la lezione:
- [ ] Ogni concetto chiave della fonte è presente
- [ ] **Nessun concetto è stato aggiunto** che non sia nella fonte — critico per i corsi
      discorsivi, dove l'esame verte sulle spiegazioni del docente
- [ ] La terminologia corrisponde alla fonte; per i corsi discorsivi, **parola per parola**
- [ ] Corsi pratici: la lezione resta prosa ancorata ai comandi e non è scivolata in walkthrough
      (quello è compito della guida-lab)

Per la guida-lab:
- [ ] Ogni esercizio della fonte è coperto, nell'ordine
- [ ] Ogni comando o passaggio ha l'anatomia completa: cosa fa, perché lì, i parametri o le
      ipotesi, le varianti
- [ ] Nessun comando, output o esercizio inventato

Per gli appunti definitivi:
- [ ] Ogni domanda dei grezzi ha ricevuto risposta
- [ ] Le risposte inline sono accurate rispetto alla fonte
- [ ] Le sezioni integrate sono complete

---

**4. Coerenza interna**

- [ ] Lezione, guida-lab e appunti usano la stessa terminologia
- [ ] I concetti chiave corrispondono a quelli dichiarati in `corsi/<COD>/percorso.md`
- [ ] Le connessioni citate sono accurate: i moduli esistono e i concetti referenziati sono
      corretti
- [ ] Le catene fra corsi citate corrispondono a `piano/piano_laurea.md`

---

**5. Report**

```
## Verifica — <COD> <ID>

Fonte usata: [titolo, oppure "NON DISPONIBILE — verifica limitata alla coerenza interna"]

### Copertura
Concetti nella fonte: X
Concetti coperti: Y
Copertura: Z%
Mancanti: [lista]
Aggiunti fuori fonte: [lista — vuota è il risultato atteso]

### Fedeltà alla formulazione (corsi discorsivi)
Terminologia fedele: [sì/no, con i punti divergenti]
Riferimenti citati correttamente: [sì/no]

### Coerenza interna
Lezione ↔ guida-lab ↔ appunti: [coerente / discrepanze]
Connessioni: [accurate / da correggere]

### Azioni correttive
[Lista numerata, se presenti]
```

---

**6. Prima di correggere, chiedi**

Se ci sono correzioni da fare, **chiedi a Lorenzo se vuole che le applichi**. Non modificare i
file di tua iniziativa: la verifica accerta, non riscrive.

---

**7. Registra l'evento**

Appendi a `stato/giornata.md`:

```
HH:MM · <COD> · verifica <ID>: copertura Z%, <n> azioni correttive.
```
