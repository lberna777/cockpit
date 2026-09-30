---
tags: [FI2, confronto]
---

# Confronto — FI2 LAB03: il mio codice e la soluzione del docente

**Mio**: `src/` di questa cartella (test verdi il 2026-09-30, **guidato**: correzioni di
`sumWithMcm`, `sub` e `getDouble` date in chat) · **Docente**:
`materiali/lab/Lab03-Frazione-SecondaParte-Soluzione.zip`
**Regola**: dove le due versioni differiscono, **si segue quella del docente**. *Migliore* dice
comunque quale regge meglio e perché.

## In sintesi

| # | Punto | Differenza | Migliore | Da seguire |
|---|---|---|---|---|
| 1 | `sum` | io prodotto in croce (sl. 6, «metodo alternativo»), lui via `mcm` come `sumWithMcm` | pari | docente, ma all'esame vince il testo |
| 2 | `sub` | stessa formula, nomi e ordine diversi | docente | docente |
| 3 | `div` | io ricalcolo con `reciprocal()` chiamato due volte, lui riusa `mul` | docente | docente |
| 4 | `compareTo` | io passo dai `double`, lui moltiplica in croce fra `int` | docente | docente |
| 5 | `getDouble` | io casto un operando, lui entrambi | pari | — |
| 6 | `mul`, `reciprocal` | stessa logica | — | — |

---

## 1. `sum`

```java
// mio — il «metodo alternativo» di sl. 6
int n = (this.num * f.den + f.num * this.den);
int d = (this.den * f.den);
return new Frazione(n, d).minTerm();
```
```java
// docente — identico a sumWithMcm
int mcm = MyMath.mcm(f.getDen(), this.getDen());
int n = ((mcm / this.getDen()) * this.getNum()) + ((mcm / f.getDen()) * f.getNum());
return (new Frazione(n, mcm)).minTerm();
```
**Migliore: pari.** Tutte e due corrette. La mia è quella che la slide chiama `sum`, e dà senso ad
avere due metodi. La sua rende `sum` e `sumWithMcm` gemelli. Il vantaggio della sua: numeri
intermedi più piccoli (`mcm` ≤ prodotto dei denominatori), quindi overflow più lontano.
**Da ricordare.** Se il testo del compito prescrive un metodo, si usa quello.

## 2. `sub`

```java
// mio
int n1 = ((mcm/f.den)*f.num);      // parte di f
int n2 = ((mcm/this.den)*this.num); // parte di this
return new Frazione(n2-n1, mcm).minTerm();
```
```java
// docente
int n = ((mcm / den) * num) - ((mcm / f.getDen()) * f.getNum());
```
**Migliore: docente.** Scrive la sottrazione nell'ordine in cui si legge: `this − f`, con `this` a
sinistra. Nel mio `n1` è `f` e il risultato è `n2 − n1`: proprio l'ordine su cui avevo sbagliato
(prima versione: `n1 − n2`, cioè `f − this`). Nomi come `n1`/`n2` nascondono **da dove** viene il
numero. Il verso sbagliato della divisione (`den/mcm`) è lo stesso errore in `sumWithMcm`: vedi
*Cosa porto via*.

## 3. `div`

```java
// mio
int num = this.num * f.reciprocal().num;
int den = this.den * f.reciprocal().den;
return new Frazione(num, den).minTerm();
```
```java
// docente
return mul(new Frazione(f.getDen(), f.getNum())).minTerm();
```
**Migliore: docente.** Dividere è moltiplicare per il reciproco, e lui lo scrive letteralmente
**riusando `mul`**: una riga, nessun conto ripetuto. Io rifaccio a mano il prodotto che `mul` sa
già fare, e costruisco il reciproco due volte. Onestà: il suo `.minTerm()` finale è ridondante,
perché `mul` restituisce già una frazione ridotta.
**Da ricordare.** Prima di scrivere un conto, chiediti se un metodo della classe lo fa già.

## 4. `compareTo`

```java
// mio
if (this.getDouble() - f.getDouble() > 0) return 1;
else if (this.getDouble() - f.getDouble() < 0) return -1;
else return 0;
```
```java
// docente
thisValue = this.getNum() * f.getDen();
otherValue = f.getNum() * this.getDen();
if (thisValue == otherValue) return 0;
else return thisValue > otherValue ? 1 : -1;
```
**Migliore: docente.** Resta negli interi, quindi il risultato è esatto, e usa **la stessa
formula di `equals`**: `compareTo == 0` e `equals` coincidono per costruzione. Il mio dipende dalla
virgola mobile per concordare con `equals`. Con numeratori e denominatori `int` la differenza in
pratica non si vede (verificato: `1/3` contro `2/6` dà `0`), ma la garanzia è sua, non mia. In più
calcolo `getDouble()` quattro volte e sottraggo prima di confrontare, quando basterebbe confrontare
i due valori direttamente.
Perché il prodotto in croce funziona: `a/b > c/d ⇔ a·d > c·b` **solo se `b` e `d` sono positivi**.
Lo garantisce il costruttore, che mette il segno sul numeratore. Senza quell'invariante il verso
si invertirebbe.

## 5. `getDouble`

`(double) num / den` contro `(double) getNum() / (double) getDen()`: equivalenti. Basta un operando
`double` perché l'altro sia promosso e la divisione diventi reale. Il cast va messo **prima**
della divisione: era il mio errore (`double val = num / den` → `0.0`).

---

## Cosa porto via

- **Il fattore di conversione è `mcm / den`**, mai `den / mcm`: «quante volte il denominatore sta
  nel multiplo». Errore di verso (`profilo/errori.md`, pattern 5), mascherato da `int / int` che
  tronca a 0 senza protestare.
- **Un test verde può essere verde per caso**: il mio primo `sub` passava perché due errori si
  compensavano, `compareTo` passava con `getDouble` rotto perché `3/12` e `1/4` davano entrambe
  `0.0` (pattern 2). Un caso in più, scelto da me, li avrebbe trovati.
- **Riusare i metodi della classe** (`div` → `mul`) e **nomi che dicono la provenienza**
  (`nThis`, `nF`) invece di `n1`, `n2`.
