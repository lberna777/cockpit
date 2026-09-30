---
tags: [FI2, confronto]
---

# Confronto — FI2 LAB02: il mio codice e la soluzione del docente

**Mio**: `src/` di questa cartella (test verdi il 2026-09-30) · **Docente**:
`materiali/lab/Lab02-Frazione-PrimaParte-Soluzione.zip`
**Regola**: dove le due versioni differiscono, **si segue quella del docente**. La colonna
*migliore* dice comunque quale delle due regge meglio e perché, così la scelta si capisce e non si
copia soltanto.

## In sintesi

| # | Punto | Differenza | Migliore | Da seguire |
|---|---|---|---|---|
| 1 | Segno nel costruttore | due rami `if` / una variabile `boolean` + operatore `? :` | docente | docente |
| 2 | Campi o getter dentro la classe | io `this.num`, lui `getNum()` | pari | docente |
| 3 | `equals` | io `if … return true; else return false`, lui `return <condizione>` | docente | docente |
| 4 | `minTerm` con numeratore 0 | io `0/1`, lui copia la frazione (`0/den`) | pari | docente |
| 5 | `Math.abs` sul denominatore in `minTerm` | io lo applico, lui no | docente | docente |
| 6 | `toString` con denominatore 1 | io `4/1`, lui `4` | docente sulla logica | docente, ma all'esame vince il testo |
| 7 | `mcm` | stessa formula | — | — |
| 8 | Residui | `import java.util.Objects`, `super()`, stampa di debug nel `Main` | — | toglierli |

---

## 1. Segno nel costruttore

```java
// mio
int i = num * den;
if (i >= 0) {
    this.num = Math.abs(num);
    this.den = Math.abs(den);
} else if (i < 0) {
    this.num = -Math.abs(num);
    this.den = Math.abs(den);
}
```
```java
// docente
boolean negativo = num * den < 0;
this.num = negativo ? -Math.abs(num) : Math.abs(num);
this.den = Math.abs(den);
```

**Differenza.** L'idea è la stessa: il segno si decide dal prodotto, e il denominatore esce
sempre positivo. Cambia la forma. Io ripeto `this.den = Math.abs(den)` in due rami. Lui lo scrive
una volta sola, perché non dipende dal segno, e decide il numeratore con l'operatore condizionale
`cond ? a : b` [fonte: 06 sl. 96; usato anche in LAB01 sl. 18 e 04b sl. 72].

**Migliore: docente.** Ogni campo viene assegnato **una volta, fuori da qualsiasi ramo**, quindi
non esiste un input che lo lasci non assegnato. È esattamente il buco che avevo io con
`if (i > 0) … else if (i < 0)`: `new Frazione(0, -5)` dava `0/0`. Con la sua forma quel bug non
si può scrivere. Il nome `negativo` inoltre dice cosa significa la condizione, `i` no.

**Da ricordare.** Se un campo riceve lo stesso valore in tutti i rami, va assegnato fuori dai
rami. Nei rami resta solo ciò che cambia davvero.

## 2. Campi o getter dentro la classe

Io uso i campi direttamente (`this.num * f.den`). Lui chiama i getter anche dall'interno
(`getNum()`, `f.getNum()`).

**Migliore: pari.** Dentro la propria classe l'accesso ai campi `private` è lecito, anche sui
campi di un altro oggetto della stessa classe (`f.den`). Qui le due forme si comportano in modo
identico. La slide del LAB non motiva la scelta del docente.
**Da seguire: docente** — usare i getter.

## 3. `equals`

```java
// mio
if ((this.num * f.den) == (this.den * f.num)) {
    return true;
} else return false;
```
```java
// docente
return f.getNum() * getDen() == f.getDen() * getNum();
```

**Migliore: docente.** Il confronto `==` è già un'espressione `boolean`: vale `true` o `false`
da solo. Scrivere `if (condizione) return true; else return false;` equivale a
`return condizione;`, con quattro righe al posto di una. La formula è la stessa della slide 8
(`n * q = m * p`).

**Nota per più avanti, vale per tutte e due le versioni.** `equals(Frazione f)` è un metodo
**nuovo** che accetta una `Frazione`. Non ridefinisce l'`equals` che ogni classe già possiede.
Per ora basta così; la forma completa arriva con i LAB sulle gerarchie (`LAB09`: `equals` con
`instanceof`; `LAB10`: `equals` e `hashCode`).

## 4. `minTerm` con numeratore 0

```java
// mio
if (this.num == 0) {
    return new Frazione(0);          // → 0/1
}
```
```java
// docente
if (getNum()==0) return new Frazione(getNum(), getDen());   // → 0/den, copia
```

**Migliore: pari.** Tutte e due evitano la chiamata `mcd(0, …)`, che finirebbe in una divisione
per zero (slide 9). `0/1` e `0/5` valgono lo stesso numero, e i test non coprono questo caso.
Entrambe restituiscono un oggetto **nuovo**, come la slide chiede.
**Da seguire: docente.** Restituisce una copia di sé stessa: «ridurre» qualcosa che non si può
ridurre la lascia com'è.

## 5. `Math.abs` sul denominatore in `minTerm`

```java
// mio
MyMath.mcd(Math.abs(this.num), Math.abs(this.den));
// docente
MyMath.mcd(Math.abs(getNum()), getDen());
```

**Migliore: docente.** Il costruttore garantisce già che il denominatore sia sempre positivo:
ogni `Frazione` esistente ce l'ha così. Rifare `Math.abs` sul denominatore significa non fidarsi
di questa garanzia. Non è un errore, ma segnala che non si è tenuto a mente cosa il costruttore
assicura. Il `Math.abs` sul numeratore invece serve, perché `mcd` vuole naturali (slide 9).

## 6. `toString` con denominatore 1

```java
// mio
return this.num + "/" + this.den;                       // 4/1
```
```java
// docente
String str = "";
int num = getNum();
int den = getDen();
str += getDen() == 1 ? num : num + "/" + den;           // 4
return str;
```

**Differenza.** Per `new Frazione(4, 1)` io stampo `4/1`, lui `4`. La slide 10 chiede la forma
`Num/Den`: la mia segue la slide alla lettera, la sua aggiunge un caso.

**Migliore.** Sulla **logica**, la sua: un intero si legge meglio senza `/1`. Sulla **forma del
codice**, la stringa vuota più `+=` è un giro in più. Avrebbe potuto restituire direttamente
l'espressione con `? :`, come fa nel costruttore.
**Da seguire: docente.** All'esame però la forma della stringa la stabiliscono il testo e i test
del compito: se chiedono `Num/Den`, si stampa `Num/Den`.

## 7. `mcm`

```java
// mio                                           // docente
return ((a*b) / (MyMath.mcd(a,b)));              return (a * b) / mcd(a, b);
```

Stessa formula. Il prefisso `MyMath.` e le parentesi in più non cambiano nulla: dentro `MyMath`,
`mcd` si chiama anche senza nome della classe.
**Il percorso per arrivarci**: prima ho scritto `a*b - mcd(a,b)`, che dà `mcm(4,6) = 22`. L'mcd è
un *fattore* del prodotto, e un fattore si toglie dividendo.

**Limite comune a tutte e due**: `a * b` può uscire dal range di `int` prima della divisione
(prontuario §3.3, overflow). Con i numeri del LAB non succede.

## 8. Residui da togliere

- `import java.util.Objects;` non è usato.
- `super();` nel costruttore l'ha generato Eclipse: senza, Java lo inserisce da sé. Il docente
  non lo scrive.
- In `MainFrazione.java` è rimasta la mia riga di debug
  `System.out.print(frazione5.getNum() + "/" + frazione5.getDen());`.

## Cosa porto via

1. **Assegnare ogni campo fuori dai rami**, dove possibile. Nei rami va solo ciò che cambia
   (punto 1).
2. **Un `boolean` si restituisce, non si trasforma con un `if`** (punto 3).
3. **Fidarsi di ciò che il costruttore garantisce** (punto 5).
4. **Test verdi non significano classe corretta**: lo zero e `mcm` sbagliato passavano i test.
5. **La regola sotto le prime tre: niente di ridondante, non «meno caratteri».** Riga per riga,
   chiedersi *«questo lo so già?»*: il valore è già un `boolean`, il campo è uguale in tutti i
   rami, il costruttore lo garantisce già. Nessuna delle tre è una scorciatoia di Java: sparirebbero
   anche in C. La chiarezza vince sulla brevità: `negativo` è più lungo di `i` ed è migliore, e il
   `toString` del docente è più lungo del necessario (punto 6). `[2026-09-30, osservazione di
   Lorenzo, precisata]`
