---
tags: [FI2, guida-lab]
---

# Scheda — FI2 LAB04c: ADT `FractionCollection`
**Materiale**: `LAB-04-Insiemi di frazioni.pdf` (sl. 41–60), `Lab04c-FractionCollection-Startkit.zip` (`FractionCollectionTests`, `CollectionMain`, `FrazioneTest`, `MainFrazione`) · **Modalità**: guidata · **Tempo del docente**: 1 h [sl. 60]
**Teoria che entra qui**: `04b` 🔶 — incapsulamento, campi `private`, costruttori multipli (sl. 41, 51) · `07` 🔶 — copia di array, raddoppio (sl. 49–50) · `06` 🔶 — `StringBuilder` (sl. 52–53).

## Setup
**Sessione normale (laptop)** — i file sono già sul disco:
- *Existing Projects* → *Select root directory* → `~/cockpit/Vault/UniCode/corsi/FI2/esame_FI2/da_importare/LAB04c_FractionCollection-021026` → **Copy projects into workspace** → **Finish**. Niente `git pull`.

**Sessione cloud** — Eclipse non c'è, i file nascono sul ramo cloud:
- sul laptop, prima `git pull` in `~/cockpit` (se un consolidamento serale non inviato ha divergito, vedi `CLAUDE.md` di cockpit), poi stessa importazione di sopra;
- oppure zip importabile: *File → Import → Existing Projects into Workspace → Select archive file*.

**In entrambi i casi**
- compliance 21, due configurazioni con `-ea` (`FractionCollectionTests`, `CollectionMain`);
- `Frazione` e `MyMath` sono **i tuoi** del LAB04b; `fractioncollection/` contiene solo test e main dello startkit;
- X rosse attese: la classe `FractionCollection` non esiste. **Creala tu** nel package `fractioncollection` (sl. 58).

## Ordine di lavoro
| # | In `FractionCollection` | Cosa rappresenta | Test | Costrutto → slide |
|---|---|---|---|---|
| 1 | campi `private Frazione[] innerContainer; private int size;` | array = supporto fisico; `size` = dimensione logica **e** prima cella libera | — | sl. 50–51 |
| 2 | 3 costruttori: `(int)`, `()`, `(Frazione[])` | vuota con capacità data / di default / copia di un array | `...Int`, `...`, `...FrazioneArray` | `this(...)` per non duplicare |
| 3 | `size()`, `get(int)` | accesso mediato | sparsi | sl. 51 |
| 4 | `put(Frazione)` | aggiunge in coda; se pieno, raddoppia | `testPut`, `testPutWithResize` | sl. 49–50: «fattorizzare il codice» |
| 5 | `remove(int)` | toglie e ricompatta | `testRemove` | — |
| 6 | `toString()` | `"[1/3, 2/5, 3/2]"` | `CollectionMain` a video | `StringBuilder` — sl. 52–53 |
| 7 | `sum`, `sub`, `mul`, `div` | nuova collezione, elemento per elemento | `testSum`; `mul` nel main | sl. 47, 49 |

## Casi limite da pensare
- Costruttore 3: copi l'array o tieni lo stesso riferimento? Che cosa succede se poi il chiamante lo modifica (sl. 54: riusa `array` per `collezioneB`)? Quale delle due scelte rispetta l'incapsulamento?
- Che cosa vale `size` dopo il costruttore 3 con `new Frazione[10]` di cui 4 piene? Lo startkit ti dà `fa` di 2 su 2, ma `CollectionMain` della sl. 54 no. (⚠️ LAB04b: fine fisica ≠ fine logica, e stavolta il `null` non ti aiuta più: c'è `size`.)
- `put` a collezione piena: il nuovo array è grande il doppio — e se la capacità iniziale fosse 0? Dove va la frazione che ha causato il resize? Quale parte del codice di `put` è comune ai due rami? (sl. 50)
- `remove(i)`: quali celle devi spostare, in che verso, e che cosa succede alla cella che resta in fondo? `size` come cambia?
- `get(k)`, `remove(k)` con `k` negativo o `≥ size`: la sl. 51 lo chiede e non risponde. I test non lo coprono: decidi tu e dichiara perché.
- `sum` fra collezioni di `size` diverse: la sl. 49 dice «di pari dimensione». Che cosa fai se non lo sono?
- `testSum` e `testMul`: `mul` e `testMul` sono «do it yourself». ⚠️ Pattern 2: scrivi tu il caso di prova per `mul`, `sub`, `div` — i test dati toccano solo `sum`.

## Test rosso?
Non compila: firma/nome/package · `AssertionError` alla riga N = failure: guarda quale `assert` · `NullPointerException` o `ArrayIndexOutOfBoundsException` = error: stack trace, riga del tuo codice → prontuario §1, oppure scrivilo in chat. Silenzio = verde **solo con `-ea`**.

## Dopo i test verdi
- copia il progetto in `corsi/FI2/esame_FI2/svolti/LAB04c_FractionCollection/`;
- confronto con la soluzione del docente → `confronto_LAB04c.md`;
- poi LAB05 (TicketSosta, caso d'esame).

---
**PDF del laboratorio**: [LAB-04-Insiemi di frazioni.pdf](<../materiali/lab/LAB-04-Insiemi di frazioni.pdf>) — per LAB04c le sl. 41–60.
