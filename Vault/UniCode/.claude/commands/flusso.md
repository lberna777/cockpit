---
description: "Disegna il flusso di una funzione in chat: passi a sinistra, esempio numerico a destra. Uso: /flusso <Classe.metodo | file> [esempio]"
argument-hint: "<Classe.metodo o file> [caso d'esempio] — es. Parcometro.calcolaCosto, oppure Parcometro.calcolaCosto H1f 7:30-15:00"
---

Il parametro passato è: "$ARGUMENTS"

Scopo: dare a Lorenzo **un colpo d'occhio** su cosa deve fare una funzione, passo per passo, con i
numeri di un caso vero. È un aiuto di *comprensione*, non la soluzione: non scrive il corpo.

**1. Trova la funzione**
- Primo token: `Classe.metodo` o percorso di file. Cercalo con `rg` nei progetti importati
  (`corsi/*/esame_*/da_importare/`, `corsi/*/esame_*/svolti/`) e nell'eventuale workspace Eclipse
  indicato in `stato/corrente.md`. Se ce ne sono più d'uno, scegli il più recente e dillo.
- Se il metodo esiste già, **leggi la versione di Lorenzo**: il disegno segue ciò che *deve* fare, e
  segna in giallo i passi dove il suo codice diverge (es. confronta la variabile sbagliata).
- Se non esiste, ricava i passi in quest'ordine, mai da conoscenza generica:
  1. startkit e test in `corsi/<COD>/materiali/` (firma, ingressi, valori attesi → i numeri dell'esempio);
  2. slide del LAB o del modulo, dove il docente descrive l'algoritmo a parole;
  3. la soluzione del docente **solo per controllare** che i passi portino a una strada che funziona,
     mai come fonte dei passi.
  Se 1 e 2 non bastano, non inventare i passi: dì cosa manca, disegna solo ingressi, uscita e caso di
  prova con i passi interni come «?», e chiedi la fonte (`CLAUDE.md` §7.1).

**2. Scegli l'esempio**
- Se è indicato un caso, usa quello. Altrimenti prendi **un test dello startkit** che attraversi tutti i passi
  e calcola i valori: a mano, o eseguendoli con `javac`/`java` in scratchpad se c'è dubbio.
- I numeri del disegno devono tornare con il valore atteso del test. Se non tornano, **non disegnare**:
  c'è un errore nel ragionamento, trovalo prima.

**3. Disegna** — un solo widget, `mcp__visualize__show_widget` (carica prima `read_me` modulo `diagram`)
- SVG `viewBox="0 0 680 H"`, due colonne: **sinistra «cosa fa il codice»** (passi numerati, riquadro con titolo
  + una riga di formula o chiamata), **destra «esempio»** (stesso passo, numeri del caso). Frecce verticali.
- Un riquadro per passo (4–6 massimo; se di più, raggruppa). Input in alto in grigio, ritorno in fondo in viola,
  passi normali in teal, passo-trappola o punto dove Lorenzo ha sbagliato in giallo.
- Sotto, 1–2 righe di nota: tipo restituito, casi limite rimandati (es. mezzanotte), trappole note
  (⚠️ da `profilo/errori.md`: divisione intera, verso, fisico/logico).
- Se `show_widget` non è disponibile: PNG con graphviz (`rankdir=LR`) in scratchpad e linkato.

**4. Rispondi breve**
- Il disegno è già a schermo: non ripeterlo a parole. Aggiungi solo cosa manca nel codice di Lorenzo
  (in forma di domanda, a gradini: concetto → pseudocodice → frammento da slide) e il prossimo gesto
  («completa il passo N, lancia il test, dimmi quanti passano»).
- **Mai il corpo della funzione** né un algoritmo che Lorenzo deve trovare (`lab.md`, template FI2).
  Vale anche per `/flusso` lanciato su metodi in modalità *compito*: lì non si usa.
