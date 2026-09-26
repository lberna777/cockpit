---
tags: [FI2, appunti]
---

# Prontuario FI2 — da tenere aperto all'esame

> **Cos'è.** Materiale di consultazione per la prova pratica, dove si possono portare tutti i file
> che si vuole. Non spiega: *risponde*. Per il perché, ogni sezione rimanda agli appunti del modulo.
> Cresce con i laboratori: una sezione per esercitazione, e l'indice qui sotto si allarga.
>
> **Come si usa in prova.**
> 1. Hai un **errore rosso in Eclipse** o un'eccezione nella console → `Ctrl+F` sul testo del
>    messaggio: ogni sezione si apre con la tabella *errore → causa → rimedio*, con il testo esatto
>    sia di Eclipse sia di `javac`.
> 2. Devi **fare una cosa** (convertire, arrotondare, leggere un numero da stringa) → *Indice per
>    bisogno*.
> 3. ⚠️ segna le righe dove Lorenzo ha già sbagliato almeno una volta: lì rallenta.
>
> **Fonti.** `[sl. N]` = pagina del PDF di slide della sezione. `[prove]` = uso ricorrente nelle
> soluzioni ufficiali dei 30 appelli 2020–2025 in `corsi/FI2/prove/`. `[oltre la fonte]` = non è
> nelle slide, **verificato in jshell / Eclipse compiler (ecj 3.38) su JDK 21 il 2026-09-26**.

---

## Indice per bisogno

| Devo… | Vai a |
|---|---|
| capire un errore «Type mismatch» / «lossy conversion» | [02x · A](#a--errore--causa--rimedio) |
| sapere se un assegnamento fra numeri compila | [02x · C](#c--conversioni-fra-numerici-compila-o-no) |
| fare una divisione che non tronchi | [02x · D](#d--aritmetica-le-trappole-che-compilano) |
| confrontare due `double` | [02x · D](#d--aritmetica-le-trappole-che-compilano) |
| arrotondare (a intero, a 2 decimali, per eccesso) | [02x · E](#e--arrotondare) |
| trasformare una stringa in numero e gestire l'errore | [02x · F](#f--stringa--numero) |
| trasformare un numero in stringa / formattarlo | [02x · F](#f--stringa--numero) |
| fare conti su caratteri (`'7'` → 7, lettera successiva) | [02x · G](#g--caratteri) |
| scrivere un `main` e leggere gli argomenti | [02x · H](#h--main-e-argomenti) |
| sapere quanto è grande / fin dove arriva un tipo | [02x · B](#b--i-tipi-primitivi) |

---

# 02x — Tipi base & dintorni

Fonti: `materiali/slide/02x-x1-Esercitazione Tipi base.pdf` (42 pagine),
`02z-Addendum-Main in Java21.pdf`. Spiegazioni: `lezioni/guida_lab_02x_tipi_base.md` §1–§6.

## A — Errore → causa → rimedio

Il testo di Eclipse è quello che vedi all'esame; quello di `javac` è quello di jshell e del
terminale. **Stessa causa, parole diverse.**

| Eclipse | `javac` / jshell | Causa | Rimedio |
|---|---|---|---|
| `Type mismatch: cannot convert from double to float` | `incompatible types: possible lossy conversion from double to float` | letterale senza `F` (`3.54` è `double`), o espressione con un `double` dentro (`ff * 2.0`) | `3.54F`, oppure cast `(float) espr` — ⚠️ vedi C |
| `Type mismatch: cannot convert from long to int` | `… possible lossy conversion from long to int` | **`Math.round(double)` restituisce `long`**; oppure letterale con `L` | `(int) Math.round(x)` — forma usata nelle soluzioni `[prove]` |
| `Type mismatch: cannot convert from double to long` / `to int` | `… lossy conversion from double to long` | **`Math.ceil`, `floor`, `rint`, `sqrt`, `pow` restituiscono `double`** | `(long) Math.ceil(x)`, `(int) Math.floor(x)` `[prove]` |
| `Type mismatch: cannot convert from int to short` / `to byte` | `… lossy conversion from int to short` | aritmetica su `byte`/`short` **produce `int`** (`c + 1`); oppure si assegna una *variabile* `int` | `(short)(c + 1)` — le parentesi attorno all'intera espressione |
| `Type mismatch: cannot convert from int to char` | `… lossy conversion from int to char` | `ch + 1` è un `int` | `(char)(ch + 1)`, oppure `ch++` (compila: ha il cast incorporato) |
| `Type mismatch: cannot convert from int to boolean` | `int cannot be converted to boolean` | in Java 0/1 **non** sono booleani (in C sì) | `x != 0` |
| `Type mismatch: cannot convert from int to String` | `int cannot be converted to String` | un numero non diventa stringa da solo | `String.valueOf(n)` o `"" + n` — vedi F |
| `Type mismatch: cannot convert from String to int` | `String cannot be converted to int` | idem, nel verso opposto | `Integer.parseInt(s)` — vedi F |
| `The literal 3000000000 of type int is out of range` | `integer number too large` | un letterale senza `L` è `int`, e non arriva a 3·10⁹ | `3000000000L` |

**Eccezioni a run-time** (compila tutto, esplode eseguendo — in console, in rosso):

| Eccezione | Quando | Rimedio |
|---|---|---|
| `ArithmeticException: / by zero` | divisione o `%` fra **interi** per zero. Fra reali **non** succede: dà `Infinity`/`NaN` [sl. 21–22] | controllare il divisore prima |
| `NumberFormatException: For input string: "…"` | `parseInt`/`parseDouble` su stringa non valida — **le virgolette nel messaggio mostrano la stringa esatta**: guardale per vedere spazi e virgole | vedi F |

**Errori silenziosi** — compila, gira, e il risultato è sbagliato. Nessun messaggio: si vedono
solo dai test rossi.

| Sintomo nel test | Causa probabile | Vai a |
|---|---|---|
| risultato intero dove ti aspettavi decimali (`3` invece di `3.5`, `0` invece di `0.33`) | divisione intera | D |
| numero enorme negativo, o segno invertito | overflow | D |
| `expected 3.14 but was 3.1400000000000001` | confronto fra `double` senza tolleranza | D |
| `expected "3.14" but was "3,14"` | `String.format` con il locale italiano | F |
| `(int) 3.9` dà `3` | il cast **tronca**, non arrotonda | E |

## B — I tipi primitivi

| Tipo | Byte | Range | Letterale | Note |
|---|---|---|---|---|
| `byte` | 1 | −128 … 127 | — | [sl. 11] |
| `short` | 2 | −32 768 … 32 767 | — | [sl. 11] |
| `char` | 2 | 0 … 65 535 (**senza segno**) | `'A'` apici singoli | Unicode, UTF-16 [sl. 23] |
| `int` | 4 | ≈ ±2,1·10⁹ (`Integer.MAX_VALUE` = 2 147 483 647) | `42` | **default dei letterali interi** [sl. 11] |
| `long` | 8 | ≈ ±9,2·10¹⁸ | `42L` | «le costanti long terminano con la lettera L» [sl. 11] |
| `float` | 4 | fino a ≈ 3,4·10³⁸ | `3.54F` | 6–7 cifre significative [sl. 14] |
| `double` | 8 | fino a ≈ 1,8·10³⁰⁸ | `3.54`, `1e3` | 14–15 cifre significative. **Default dei letterali con punto** [sl. 14] |
| `boolean` | — | `true` / `false` | — | **non** convertibile da/verso numeri |

Costanti utili: `Integer.MAX_VALUE`, `Integer.MIN_VALUE`, `Long.MAX_VALUE`, `Double.MAX_VALUE`.
⚠️ `Double.MIN_VALUE` = 4.9E−324 è il più piccolo **positivo**, non il più negativo: per un
minimo iniziale usa `-Double.MAX_VALUE`. `[oltre la fonte]`

Il letterale ha un tipo, e lo decide la **sintassi**, non il valore: `42` → `int`, `42L` → `long`,
`3.54` → `double`, `3.54F` → `float`, `'A'` → `char`, `"A"` → `String`.

## C — Conversioni fra numerici: compila o no?

![Conversioni allarganti: ogni freccia (e ogni cammino di frecce) è accettata senza cast](img/FI2_02x_conversioni.png)

*Si legge nel verso delle frecce: se da X a Y c'è un cammino, `Y var = <X>` compila senza cast.
Contro il verso serve il cast. La freccia tratteggiata è l'unico punto dove «compila» e «non perde
niente» smettono di coincidere (riga 5 sotto). Intercetta l'errore del verso invertito — ⚠️
trasversale n. 5.*

**Il procedimento in 2 passi** — sempre in quest'ordine:
1. **Tipo del lato destro**: letterale → tabella B; espressione → il tipo **più largo** fra gli
   operandi, e **mai meno di `int`** (`byte + byte` è `int`).
2. **Cammino nel diagramma** dal tipo di destra a quello di sinistra? Sì → compila. No → cast.

> «In Java, C#, Scala sono ammessi solo gli assegnamenti che non causano perdita di
> informazione.» `double x = 3.54F;` lecita, `float f = 3.54;` illecita. [sl. 15]

**Eccezioni al procedimento**, tutte verificate:

| # | Caso | Esito | Perché |
|---|---|---|---|
| 1 | `short s = 300;` `char c = 65;` `byte b = 10;` | ✓ compila | **costante** nota al compilatore **e** ci sta nel tipo |
| 2 | `byte b = 300;` `short s = 40000;` | ✗ | costante, ma **non** ci sta |
| 3 | `int q = 10; byte b = q;` | ✗ | `q` è una variabile: il compilatore non ne segue il valore |
| 4 | `byte b = 127; b++;` · `int a = 5; a += 2.7;` | ✓ compila → `b` = −128, `a` = 7 | `++`, `+=`, `-=`… **hanno il cast incorporato**: troncano e avvolgono senza avvisare |
| 5 | `float h = 123456789L;` | ✓ compila → stampa `1.2345679E8` | `long → float` è ammessa (conta il *range*), ma `float` tiene solo 7 cifre |

**Il cast** — `(tipo) espressione`: è la dichiarazione di **Design Intent**, cioè la perdita è
una scelta tua e ne rispondi tu. ⚠️ Usa questo termine all'orale (trasversale n. 4).

| Scritto | Valore | Nota |
|---|---|---|
| `(int) 3.9` | `3` | **tronca**, non arrotonda |
| `(int) -3.9` | `-3` | tronca **verso zero**, non verso il basso |
| `(double) 7 / 2` | `3.5` | il cast lega **solo** al `7`, poi la divisione è fra reali |
| `(double) (7 / 2)` | `3.0` | la divisione intera avviene **prima**, il cast arriva tardi |
| `(short)(c + 1)` | — | senza parentesi esterne il cast lega solo a `c` e l'errore resta |

## D — Aritmetica: le trappole che compilano

**Divisione intera.** Se **entrambi** gli operandi sono interi, la divisione è intera e tronca.

| Espressione | Valore | Rimedio nelle soluzioni `[prove]` |
|---|---|---|
| `7 / 2` | `3` | `7 / 2.0` → `3.5` |
| `1 / 3 * 3` | `0` | — |
| `minuti / 60` | intero | `minuti / 60.0` |
| `a / b` con due `int` | intero | `a * 1.0 / b` oppure `(double) a / b` |

**Overflow** — Java protegge dalle *conversioni* che perdono dati, **non** dall'overflow
aritmetico: il valore avvolge in silenzio [sl. 12–13].

| Espressione | Valore |
|---|---|
| `Integer.MAX_VALUE + 1` | `-2147483648` |
| `byte b = 125; b++; ++b; ++b;` | `-128` (da 127 passa a −128) |
| `Math.abs(Integer.MIN_VALUE)` | `-2147483648` — **negativo** `[oltre la fonte]` |

**Reali e IEEE-754** — «Lo standard IEEE-754 incorpora le nozioni di infinito e Not-A-Number
(NaN)» [sl. 21]; «I tipi interi non seguono lo standard IEEE-754» [sl. 22].

| Espressione | Valore |
|---|---|
| `5.0 / 0` | `Infinity` |
| `-5.0 / 0` | `-Infinity` |
| `0.0 / 0.0` · `5.0 % 0` · `Math.sqrt(-1)` | `NaN` |
| `0.0 / -5` | `-0.0` — «Java mantiene il segno nel risultato, MA ciò non ne altera la semantica» [sl. 20]: `-0.0 == 0.0` è `true` |
| `5 / 0` · `5 % 0` | **`ArithmeticException: / by zero`** |
| `Double.NaN == Double.NaN` | `false` — per testare usa `Double.isNaN(x)` |

**Confrontare due `double`: mai con `==`.**

| Espressione | Valore |
|---|---|
| `0.1 + 0.2` | `0.30000000000000004` |
| `0.1 + 0.2 == 0.3` | `false` |

- nel codice: `Math.abs(a - b) < 0.01` — forma usata nelle soluzioni `[prove]`, es.
  `if (Math.abs(importo - sommaItems) > 0.01) throw …`;
- nei test JUnit: `assertEquals(atteso, ottenuto, 0.01)` — **il terzo argomento è la
  tolleranza**; senza di esso il confronto fra `double` è fragile. `[prove]`

## E — Arrotondare

| Funzione | Restituisce | 2.5 | −2.5 | 2.7 | Per assegnarla a `int` |
|---|---|---|---|---|---|
| `(int) x` | `int` | 2 | −2 | 2 | — (tronca verso zero) |
| `Math.round(x)` | **`long`** (da `double`) | 3 | **−2** | 3 | `(int) Math.round(x)` |
| `Math.rint(x)` | **`double`** | **2.0** | −2.0 | 3.0 | `(int) Math.rint(x)` |
| `Math.floor(x)` | `double` | 2.0 | **−3.0** | 2.0 | `(int) Math.floor(x)` |
| `Math.ceil(x)` | `double` | 3.0 | −2.0 | 3.0 | `(int) Math.ceil(x)` |

- `rint` e `round` [sl. 19]: «rint arrotonda un valore reale all'intero più vicino (risultato
  reale); round arrotonda un valore reale all'intero più vicino (risultato intero)». Sui valori
  **esattamente a metà** divergono: `rint` va al **pari** (0.5→0, 1.5→2, 2.5→2, 3.5→4), `round`
  va verso **+∞** (2.5→3, −2.5→−2). `[oltre la fonte]`
- **A 2 decimali**: `Math.rint(x * 100) / 100` → `3.14159` dà `3.14`. `[prove]`
- **Per eccesso a intero** (es. tariffe a ore iniziate): `(long) Math.ceil(minuti * 1.0 / 60)` —
  il `* 1.0` evita la divisione intera, che altrimenti troncherebbe **prima** del `ceil`. `[prove]`
- Altre di `Math` [sl. 10, 19]: `sqrt`, `pow(x, y)` (→ `double`: `pow(2,10)` = `1024.0`),
  `abs`, `max`, `min`, `hypot(x, y)` = √(x²+y²) «senza errori di overflow/underflow intermedi»,
  `log1p(p)` = ln(1+p), `Math.PI`.

## F — Stringa ↔ numero

**Stringa → numero** [sl. 34]: `Integer.parseInt`, `Long.parseLong`, `Double.parseDouble`.
«MA questi metodi pretendono stringhe "giuste"! altrimenti… BOOM!» [sl. 34]

| Input | `parseInt` | `parseDouble` |
|---|---|---|
| `"42"` · `"+7"` | 42 · 7 | 42.0 · 7.0 |
| `" 42"` (spazio) | ✗ **NumberFormatException** | ✓ tollera gli spazi (`" 3.5 "` → 3.5) |
| `"3.5"` | ✗ | 3.5 |
| `"3,5"` (virgola) | ✗ | ✗ — il separatore è il **punto** |
| `""` | ✗ | ✗ |
| `"99999999999"` | ✗ (fuori range) | 9.9999999999E10 |
| `"1e3"` | ✗ | 1000.0 |

⚠️ `parseInt` **non** tollera spazi: nei file letti riga per riga si fa sempre `.trim()` prima.

**Lo schema d'esame** — ricorre in **19 prove su 30**: leggere un campo, convertirlo, e
tradurre il fallimento nell'eccezione del dominio. `[prove]`

```java
int ore;
try {
    ore = Integer.parseInt(items[1].trim());
} catch (NumberFormatException e) {
    throw new BadFileFormatException("ore non valide: " + items[1]);
}
```

In Java «per evitare tale errore si può solo controllare la stringa prima di convertirla» [sl. 35]
— o intercettare l'eccezione, come sopra (eccezioni: moduli successivi).

**Numero → stringa**

| Scritto | Risultato | Nota |
|---|---|---|
| `String.valueOf(3.0)` · `"" + 3.0` | `"3.0"` | equivalenti; `String.valueOf('A')` → `"A"` [sl. 23] |
| `String.format("%.2f", 3.14159)` | ⚠️ **`"3,14"`** | usa il locale del sistema, qui italiano → virgola |
| `String.format(Locale.US, "%.2f", 3.14159)` | `"3.14"` | se il test si aspetta il punto `[oltre la fonte]` |
| `String.format("%5d\|%-5d\|%05d", 42, 42, 42)` | `"   42\|42   \|00042"` | larghezza, allineato a sinistra, zeri davanti |

**Concatenazione con `+`**: «l'operatore + concatena stringhe e nel farlo converte anche in stringa
ciò che stringa non è» [sl. 7]. Si valuta **da sinistra**, e finché non compare una stringa è
somma:

| Espressione | Valore |
|---|---|
| `"a" + 1 + 2` | `"a12"` |
| `1 + 2 + "a"` | `"3a"` |
| `"x" + 'a' + 'b'` | `"xab"` |
| `'a' + 'b' + "x"` | **`"195x"`** — due `char` sommati sono un `int` (97 + 98) |

## G — Caratteri

`char` è un numero da 16 bit con segno di carattere: si somma, si confronta, si converte.

| Espressione | Valore | Uso |
|---|---|---|
| `(int) 'A'` · `int m = 'A';` | `65` | codice del carattere |
| `char c = 65;` | `'A'` | costante che ci sta → nessun cast (C, riga 1) |
| `'7' - '0'` | `7` | cifra-carattere → valore |
| `'a' + 1` | `98` (`int`!) | — |
| `(char)('a' + 1)` | `'b'` | lettera successiva |
| `ch++` | `'b'` | compila senza cast (C, riga 4) |
| `c >= 'a' && c <= 'z'` | — | test di intervallo |

**`Character`, classe-libreria** — «non si può chiedere a un valore primitivo di "fare
qualcosa"… bisogna chiamare una qualche funzione di una qualche libreria» [sl. 27]:

| Chiamata | Valore | Nota |
|---|---|---|
| `Character.toUpperCase('a')` / `toLowerCase` | `'A'` | [sl. 28] |
| `Character.isWhitespace('\t')` | `true` | spazio, tab, a capo… [sl. 28] |
| `Character.isDigit(c)` · `isLetter(c)` | — | `[oltre la fonte]` |
| `Character.digit('8', 10)` | `8` | [sl. 29] |
| `Character.digit('B', 16)` · `digit('B', 10)` | `11` · **`-1`** | −1 = «segnale di errore»: va **controllato** [sl. 29] |

`Integer` [sl. 30]: `signum(-42)` → `-1`; `rotateLeft(6, 1)` → `12`; `rotateRight(6, 2)` →
`-2147483647` (i bit usciti a destra rientrano a sinistra: è una *rotazione*, non uno shift).

**Unicode, UTF, e i tre numeri di un carattere** [sl. 23–26]. «In Java, i caratteri sono Unicode
(16 bit, UTF-16)»; i byte UTF si ottengono «partendo da una stringa, NON da un carattere», con
`getBytes(…)`. ⚠️ `char` e byte non stanno sullo stesso piano (occorrenza del 16/09).

| Per U+1F608 (faccina, fuori dal piano base) | Valore | Risponde a |
|---|---|---|
| `s.length()` | `2` | quanti `char` (unità UTF-16: coppia surrogata) |
| `s.getBytes("UTF-8").length` | `4` | quanto occupa in UTF-8 |
| `s.codePointCount(0, s.length())` | `1` | quanti caratteri *veri* |
| `"À".getBytes("UTF-8").length` | `2` | — |

**BOM di UTF-16.** `"A".getBytes("UTF-16")` → `[-2, -1, 0, 65]` = `FE FF 00 41`. I due byte in
testa sono il BOM U+FEFF. Messi nell'ordine `FE FF`, indicano **big-endian**: è la sl. 25 a essere
corretta («Everything in Java is stored in big-endian order»), mentre la didascalia della sl. 24
(«FE, FF è il marcatore little endian») è **imprecisa**. Verificato in jshell il 2026-09-26.
UTF-8 → `[65]`, UTF-32 → `[0, 0, 0, 65]`.

## H — `main` e argomenti

```java
public class Prog {
    public static void main(String[] args) {
        if (args.length == 0) System.out.println("Nessun argomento");
        for (int i = 0; i < args.length; i++)
            System.out.println("argomento " + i + ": " + args[i]);
    }
}
```

- `static` «perché deve esistere dall'inizio alla fine del programma»; `public` «perché deve
  essere visibile dall'esterno» [sl. 2].
- `args[0]` è il **primo argomento**, non il nome del programma (in C sì) [sl. 3]. `args.length`
  è una proprietà, **senza parentesi** (a differenza di `s.length()` delle stringhe).
- `java Prog alfa "beta gamma"` → **2** argomenti: le virgolette tengono insieme [sl. 9].
- Gli argomenti sono **sempre `String`**: `double a = Double.parseDouble(args[0]);` [sl. 37].
- Java 21 (preview) accetta anche `void main()` senza classe né argomenti, con
  `javac --enable-preview --source 21`. Ordine di ricerca: statico con argomenti → statico senza
  → d'istanza con argomenti → d'istanza senza [02z, sl. 7]. All'esame usa la forma classica.

## I — Per l'orale: Java e gli altri

| | Java | C# | Scala / Kotlin |
|---|---|---|---|
| tipi base | **primitivi**, non oggetti | classi trattate come primitivi (`int` = `Int32`) | **veri tipi-oggetto** |
| chiedere un servizio | funzione statica di libreria: `Character.toUpperCase(c)` | anche metodo: `ch.ToString()`, `'B'.ToString()` | metodo: `x.toFloat` (Scala senza parentesi), `x.toFloat()` (Kotlin) |
| stringa → numero | `Integer.parseInt` | `Convert.ToInt32` | `toInt`; senza eccezione `toDoubleOption` / `toDoubleOrNull` |
| `main` | in una classe, `public static` | in una classe | Scala in un `object`; Kotlin a livello di file |

[sl. 2, 27, 31–35]. ⚠️ `Integer`, `Character` di Java «NON VANNO CONFUSE COI TIPI-OGGETTO DI Scala
e Kotlin» [sl. 27]: sono librerie **accanto** al primitivo, non al suo posto.

> **Trappola collegata, per quando arriveranno le collezioni** `[oltre la fonte]`: gli oggetti
> `Integer` si confrontano con `.equals`, non con `==`. `Integer.valueOf(127) ==
> Integer.valueOf(127)` è `true`, ma con `128` è **`false`**. Nelle `Map<String, Integer>` delle
> prove capita.
