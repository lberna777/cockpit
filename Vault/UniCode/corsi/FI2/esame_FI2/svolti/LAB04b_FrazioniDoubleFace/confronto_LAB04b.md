---
tags: [FI2, confronto]
---

# Confronto — FI2 LAB04b: il mio codice e la soluzione del docente

**Mio**: `src/` di questa cartella (test verdi il 2026-10-01, **guidato**: `size` scritta da sola;
`convertToString`, `sum` e `mul` a coppie dopo suggerimenti in chat, condizione del ciclo data dalla
sl. 28) · **Docente**: `materiali/lab/Lab04b-FrazioniDoubleFace-Soluzione.zip`
**Regola**: dove le due versioni differiscono, **si segue quella del docente**; all'esame vince il testo.

## In sintesi

| # | Punto | Differenza | Migliore | Da seguire |
|---|---|---|---|---|
| 1 | `sum`/`mul(Frazione[])` | io mi fermo al primo `null`, lui usa il *for each* | **mio** (verificato: il suo va in `NullPointerException` sugli array del test) | la condizione della sl. 28 |
| 2 | `convertToString` | io virgola *prima* (tranne il primo), lui la versione «bruttina» della slide | **mio** | il formato che chiede il testo |
| 3 | `size` | io `for` a corpo vuoto, lui contatore + `break` | pari; il suo si legge meglio | docente |
| 4 | somma a coppie | io `if (==) {…} else return null`, lui `if (!=) return null;` in testa | pari; il suo è più piatto | docente |
| 5 | caso `0/6` | io chiamo `sumWithMcm`, lui `sum`, che **è** già via `mcm` | docente | una sola `sum` d'istanza, via `mcm` |
| 6 | ciclo della somma a coppie | io `i < fA.length && fA[i] != null`, lui `k < result.length` | pari | docente: più corto |

---

## 1. `sum(Frazione[])` e le celle vuote

```java
// mio
for (int i = 0; i < fs.length && fs[i] != null; i++)
    sumTemp = sumTemp.sumWithMcm(fs[i]);
```
```java
// docente
for (Frazione f : fs)
    tmp = tmp.sum(f);
```
Su `collezioneA` del test (`length` 10, 4 frazioni) la versione del docente lancia
`NullPointerException ... because "<parameter1>" is null`: l'ho eseguita. Nessun test la chiama,
quindi il docente non se ne accorge: è il pattern 2 visto dall'altra parte, **un metodo senza
test può essere sbagliato anche nella soluzione ufficiale**. Il *for each* va bene solo sugli
array pieni, come quelli del LAB04a.

## 2. `convertToString`

```java
// mio
for (int i = 0; i < fs.length && fs[i] != null; i++) {
    if (i != 0) res += ", ";   // separatore prima, tranne il primo
    res += fs[i].toString();
}
```
Il docente stampa `[8/15, 11/12, -5/14, 0/6, ]` (la sl. 28 lo dice «bruttino»). La mia prima
versione stampava a parte l'ultima cella **fisica** (`fs[fs.length-1]`): `null` sugli array a metà,
indice `-1` su quelli vuoti. L'ultimo elemento *logico* non si conosce finché non si incontra il
`null`; il primo sì (`i == 0`).

## 3–4–6. `size` e la somma a coppie

```java
// docente
public static int size(Frazione[] tutte) {
    int size = 0;
    for (int i = 0; i < tutte.length; i++) {
        if (tutte[i] == null) break;
        size++;
    }
    return size;
}
public static Frazione[] sum(Frazione[] setA, Frazione[] setB) {
    if (size(setA) != size(setB)) return null;      // condizione rovesciata, uscita subito
    Frazione[] result = new Frazione[size(setB)];
    for (int k = 0; k < result.length; k++)          // qui length = dimensione logica
        result[k] = setA[k].sum(setB[k]);
    return result;
}
```
Stesso comportamento delle mie. Con l'uscita in testa il resto del metodo non sta dentro un `if`, e
il compilatore non chiede un `else`. Entrambi calcoliamo `size` più di una volta: è il costo che la
sl. 29 segnala.

## 5. Il caso `0/6`

Il test vuole `1/6 + (-1/6) = 0/6`. La `sum` d'istanza del docente usa `mcm` (6); la mia, dal LAB03,
fa il prodotto in croce (36), e `minTerm` lascia lo zero com'è → `0/36`. L'ho aggirato chiamando
`sumWithMcm` nella somma a coppie. Da seguire: **una sola** `sum` d'istanza, via `mcm`, come il
docente (era già il punto 1 di `confronto_LAB03.md`). Così `setA[k].sum(setB[k])` della sl. 30
funziona così com'è.

---

## Cosa porto via

- **Fine fisica e fine logica**: `length` dice quante celle esistono, il primo `null` quante sono
  usate. Ogni ciclo su un array riempito a metà le controlla **entrambe**, in quest'ordine:
  `i < a.length && a[i] != null`.
- `i < length - 1` non salta i `null`: salta l'ultima cella.
- **Tre `sum` in `Frazione`** distinte dagli argomenti (overloading): d'istanza → una `Frazione`;
  statica su un array → il totale; statica su due array → un array cella per cella.
- Un array nuovo si crea dove la sua lunghezza è nota e prima del ciclo che lo riempie:
  `new Frazione[n]`, celle tutte `null`.
- Un metodo che restituisce un valore deve farlo su **ogni** strada; per ora l'«allarme» è `null`.
