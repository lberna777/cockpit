---
tags: [FI2, confronto]
---

# Confronto — FI2 LAB04c: il mio codice e la soluzione del docente

**Mio**: `src/` di questa cartella (test verdi il 2026-10-02, **guidato**: campi, costanti e costruttori
scritti da solo; `size`/`get`, `put`, `remove`, `sum`/`mul`, `toString` corretti dopo controlli in chat)
· **Docente**: `Lab04c-FractionCollection-Soluzione.zip`
**Regola**: dove le due versioni differiscono, **si segue quella del docente**; all'esame vince il testo.
**Verifica**: `FractionCollectionTests` con `-ea` esce senza errori (eseguito con `javac`/`java`, non solo
letto); casi extra eseguiti a parte: collezione vuota, un elemento, `size` diverse, array pieno.

## In sintesi

| # | Punto | Differenza | Migliore | Da seguire |
|---|---|---|---|---|
| 1 | `(Frazione[])` | io copio le prime `size` celle (`Frazione.size`), lui scarta i `null` ovunque | pari (diverso se l'array ha buchi) | docente: regge anche i buchi |
| 2 | `()` | io ripeto `new Frazione[DEFAULT_PHYSICAL_SIZE]`, lui `this(DEFAULT_PHYSICAL_SIZE)` | **docente** | `this(...)` |
| 3 | `size()` | uguale (`return size`) dopo la correzione | pari | — |
| 4 | `get` fuori range | io lancio `IndexOutOfBoundsException`, lui restituisce `null` | **mio** (non nasconde l'errore) | scelta mia, dichiarata |
| 5 | `put` | stessa struttura: se pieno, array nuovo, copia, assegna; poi inserisce | pari | — |
| 6 | `put` con lunghezza 0 | io creo un array da `DEFAULT_PHYSICAL_SIZE`; lui `0 * 2` = 0 → eccezione | **mio** | il mio `if` |
| 7 | `remove` fuori range | io lancio, lui esce in silenzio | **mio** (stessa scelta di `get`) | scelta mia |
| 8 | `remove`: cella finale | io azzero l'ultima cella, lui no (resta il doppione) | **mio** | azzerare |
| 9 | `sum`/`mul` | io `sumWithMcm` e eccezione se `size` diverse; lui `sum` e `return null` | **mio** (un `null` esplode più tardi) | scelta mia |
| 10 | `toString` | stessa idea; io `[ ` e ` ]` con spazi, lui `[` e `]` | docente | formato `[a, b, c]` |

---

## 1. `put` quando la capacità iniziale è 0

```java
// docente
Frazione[] newContainer = new Frazione[size * DEFAULT_GROWTH_FACTOR];   // size = 0 → 0 celle
```
```java
// mio
if (innerContainer.length == 0)
    innerContainer = new Frazione[DEFAULT_PHYSICAL_SIZE];
```
Con `new FractionCollection(0)` o con `new FractionCollection(new Frazione[0])` il docente lancia
`ArrayIndexOutOfBoundsException: Index 0 out of bounds for length 0` alla prima `put`. Nessun test lo
prova: è il caso che la scheda segnalava e che il docente non copre.

## 2. `remove`: l'ultima cella

Il docente sposta le celle e fa `size--`, ma lascia in fondo il vecchio ultimo elemento (ora doppione).
Fuori dalla dimensione logica non si vede, perché `get` controlla `size`, ma l'oggetto resta
referenziato. Io azzero `innerContainer[size - 1]`: lo stato resta coerente.

## 3. Fuori range: eccezione o `null`

Il docente restituisce `null` da `get` e da `sum`, ed esce in silenzio da `remove`. Un `null` torna al
chiamante come se fosse un valore; l'errore compare dopo, altrove (`NullPointerException`). Io lancio
`IndexOutOfBoundsException` (`get`, `remove`) e `IllegalArgumentException` (`sum`, `mul`). Il testo non
chiede una delle due: va bene qualunque scelta, purché dichiarata in un commento.

## 4. `toString`

Gli spazi dentro le parentesi (`[ 1/3 ]`, e `[  ]` per la collezione vuota) non seguono il formato della
scheda e del docente: `[1/3, 2/5, 3/2]`, `[]`. Lasciati nel codice svolto com'erano al momento del
verde; nel prontuario è scritta la forma del docente.

## Cosa resta da rifare a freddo

Come per i LAB precedenti, svolto con guida: da rifare senza suggerimenti nella preparazione all'esame,
con attenzione a `put` (il nuovo array va **assegnato** a `innerContainer`, e si **moltiplica** per il
fattore) e a `remove` (estremi del ciclo: `i < size - 1`).
