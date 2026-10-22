---
tags: [FI2, confronto]
---

# Confronto — FI2 LAB06 MasterMind: il mio codice e la soluzione del docente

**Mio**: `src/mastermind/model/` di questa cartella (34/34 test verdi il 2026-10-22, svolto con
guida e con la procedura d'esame) · **Docente**: `materiali/lab/Lab06-MasterMind-Soluzione.zip`
**Regola**: dove le due versioni differiscono, **si segue quella del docente**. La colonna *migliore*
dice comunque quale delle due regge meglio e perché.

## In sintesi

| # | Punto | Differenza | Migliore | Da seguire |
|---|---|---|---|---|
| 1 | Riempire l'array di `VUOTO` | io un ciclo, lui `Arrays.fill` | docente | docente |
| 2 | `equals` | io ciclo con `!=`, lui `this == that` + `Arrays.equals` | docente | docente |
| 3 | Cicli su tutti gli elementi | io `for (int i…)`, lui il *for each* | docente | docente |
| 4 | `dim()` | io `pioli.length`, lui un campo `dim` | pari | docente |
| 5 | `tentativo(i)` / `risposta(i)` | io nessun controllo, lui controlla `index >= numTentativi` | docente | docente |
| 6 | `registraMossa`, ramo `PERSO` | io `tentativiRimasti() == 0`, lui `numTentativi < maxTentativi` | pari | docente |
| 7 | Tab in `situazione` | io `if/else` con 2 o 3 tab, lui 2 tab fisse + 1 condizionale | pari | docente |
| 8 | `toString` di `Gioco` | io senza righe vuote, lui con una riga vuota e un a capo finale | io (slide 23) | docente |
| 9 | Ciclo dei minimi | io `j < occS.length`, lui *for each* su `PioloDiGioco.values()` | docente | docente |
| 10 | Riempire la `Risposta` | io un ciclo con tre rami che consuma `neri`/`bianchi`, lui due cicli con estremi | docente | docente |
| 11 | `occorrenze` | io `occ[ordinal()]++`, lui azzera a mano e usa una variabile d'appoggio | io | docente |
| 12 | `sorteggiaCombinazione` | io il parametro, lui il campo `this.segreta.dim()` nel ciclo | io | docente |

---

## 1. Riempire l'array di `VUOTO`

```java
// mio
for (int i = 0; i < this.dim; i++) {
    this.pioli[i] = PioloDiGioco.VUOTO;
}

// docente
Arrays.fill(combinazione, PioloDiGioco.VUOTO);   // import java.util.Arrays
```

`Arrays.fill(array, valore)` mette lo stesso valore in **tutte** le celle: una riga, e nessun
confine da sbagliare. Il ciclo fa la stessa cosa, ma è proprio il punto dove ho scritto `dim - 1`.

## 2. `equals`

```java
// mio
public boolean equals(Combinazione c2) {
    if (c2 == null) return false;
    if (this.dim() == c2.dim()) {
        for (int i = 0; i < this.dim(); i++) {
            if (this.pioli[i] != c2.pioli[i]) return false;
        }
        return true;
    }
    return false;
}

// docente
public boolean equals(Combinazione that) {
    if (this == that) return true;                 // stesso oggetto: inutile confrontare
    if (that == null) return false;
    return (this.dim == that.dim) && Arrays.equals(this.combinazione, that.combinazione);
}
```

Stessa logica. `Arrays.equals(a, b)` fa lui il ciclo cella per cella (e controlla anche la
lunghezza). `this == that` in testa è una scorciatoia: un oggetto è sempre uguale a sé stesso.
Il controllo su `null` c'è in tutte e due le versioni: l'avevo aggiunto io al passo 5.

## 3. Cicli su tutti gli elementi: il *for each*

```java
// mio
for (int i = 0; i < this.dim(); i++) {
    sj.add(this.pioli[i].toString());
}

// docente
for (PioloDiGioco c : combinazione) {   // «per ogni piolo c dell'array»
    sb.add(c.toString());
}
```

Quando serve **ogni** elemento e non l'indice, il *for each* non ha confini da scrivere.
Il docente lo usa in `toString`, `vittoria` e nel ciclo dei minimi (punto 9).
Serve il `for` con indice solo quando l'indice conta: neri (stessa posizione in due array),
riempimento della `Risposta`, `situazione` (numero di riga).

## 4. `dim()`

Io restituisco `pioli.length`, il docente un campo `dim` impostato nel costruttore. Con un array
che non cambia mai lunghezza sono equivalenti. (Il campo `dim` ce l'ho anch'io, ma non lo uso in
`dim()`: uno dei due è di troppo.)

## 5. `tentativo(i)` e `risposta(i)`

```java
// docente
public Combinazione tentativo(int index) {
    if (index >= numTentativi) {
        System.err.println("Tentativo " + index + " inesistente: l'ultimo è il " + numTentativi);
        return null;   // «pessimo! genera e propaga mine vaganti! Ma per ora...»
    }
    return tentativi[index];
}
```

Il docente controlla l'indice e lo scrive lui stesso: è una soluzione provvisoria, «in futuro si
lancerà eccezione di tipo IllegalArgumentException» (modulo 25e). Io restituisco la cella così
com'è: `null` se la mossa non c'è ancora, eccezione se l'indice è fuori dall'array. Il suo
`ultimoTentativo()` poi passa da `tentativo(numTentativi - 1)` invece di leggere l'array.

## 6. `registraMossa`

```java
// mio
if (risposta.vittoria()) {
    this.status = Status.VITTORIA;
} else if (this.tentativiRimasti() == 0) {
    this.status = Status.PERSO;
} else this.status = Status.IN_CORSO;
return this.status;

// docente
if (risposta.vittoria()) status = Status.VITTORIA;
else if (numTentativi < maxTentativi) status = Status.IN_CORSO;
else status = Status.PERSO;
return status;
```

Stesso ordine dei controlli (prima la vittoria), rami scritti al contrario: equivalenti.

## 7. Tab in `situazione`

```java
// mio
if (this.tentativi[i].toString().length() < 20) {
    sb.append("\t\t\t");
} else sb.append("\t\t");

// docente
"\t\t" + (tentativi[i].toString().length() < 20 ? "\t" : "")
```

Il docente scrive la regola della slide 22 come la slide la dice: **due tab sempre, più una se
corta**. `condizione ? a : b` è l'*operatore ternario*: vale `a` se la condizione è vera, `b`
altrimenti, ed è un'espressione, quindi sta dentro una concatenazione.

## 8. `toString` di `Gioco`

```java
// docente
return "Situazione:" + System.lineSeparator() + situazione() + System.lineSeparator() +
       "Gioco: " + this.stato() + System.lineSeparator();
```

Il docente aggiunge una riga vuota prima di `Gioco:` e un a capo finale; la slide 23 non li
mostra, e i test controllano solo `contains`, quindi passano entrambe. All'esame vince il
testo del compito: se dà un esempio, si copia quello.

## 9. Ciclo dei minimi — il bug che ho trovato con le stampe

```java
// mio (prima)                            // mio (dopo)
for (int j = 0; j < tentativo.dim(); j++) for (int j = 0; j < occS.length; j++)

// docente
for (PioloDiGioco p : PioloDiGioco.values()) {
    totali += Math.min(occorrenzeSegreta[p.ordinal()], occorrenzeTentativo[p.ordinal()]);
}
```

Il ciclo vive nello **spazio dei colori**, non delle posizioni. Il docente lo rende impossibile da
sbagliare: scorre i colori e usa il loro `ordinal()` come indice. Nessun numero da scegliere.

## 10. Riempire la `Risposta`

```java
// mio
for (int y = 0; y < tentativo.dim(); y++) {
    if (neri != 0) { risposta.setPiolo(y, PioloRisposta.NERO); neri--; }
    else if (neri == 0 && bianchi != 0) { risposta.setPiolo(y, PioloRisposta.BIANCO); bianchi--; }
    else if (neri == 0 && bianchi == 0) { risposta.setPiolo(y, PioloRisposta.VUOTO); }
}

// docente
for (int i = 0; i < neri; i++)      r.setPiolo(i, PioloRisposta.NERO);
for (int i = neri; i < totali; i++) r.setPiolo(i, PioloRisposta.BIANCO);
```

Due cicli, uno per colore, con gli estremi della tabella di Claude: neri in `[0, neri)`, bianchi
in `[neri, totali)`. Nemmeno `bianchi` serve: il secondo ciclo finisce a `totali`. Il `VUOTO` non
si scrive, c'è già dal costruttore. La mia versione funziona, ma consuma `neri` e `bianchi`
(dopo il ciclo valgono 0: è per questo che la stampa li mostrava a zero) e i rami ripetono
condizioni già vere (`neri == 0` nel secondo `else if`).

## 11. `occorrenze`

```java
// mio
int[] occ = new int[PioloDiGioco.values().length];
for (int i = 0; i < tentativo.dim(); i++) {
    PioloDiGioco n = tentativo.getPiolo(i);
    occ[n.ordinal()]++;
}

// docente
int[] arrayOccorrenze = new int[PioloDiGioco.values().length];
for (int i = 0; i < PioloDiGioco.values().length; i++) arrayOccorrenze[i] = 0;   // non serve: già 0
for (int i = 0; i < tentativo.dim(); i++) {
    PioloDiGioco pioloAttuale = tentativo.getPiolo(i);
    int frequenzaAttuale = arrayOccorrenze[pioloAttuale.ordinal()];
    arrayOccorrenze[pioloAttuale.ordinal()] = frequenzaAttuale + 1;
}
```

Stessa idea (la cella è l'`ordinal()` del colore). Il docente azzera a mano un array di `int` che
Java crea già a 0, e scrive il `++` in tre passi. Il suo commento: usare array indicizzati con
`ordinal()` «è un modo rozzo per fare tabelle. In futuro infatti useremo, assai più propriamente,
delle mappe!» (`Map`, modulo 25).

## 12. `sorteggiaCombinazione`

```java
// mio
for (int i = 0; i < segreta.dim(); i++) { ... segreta.setPiolo(i, ...); }

// docente
for (int i = 0; i < this.segreta.dim(); i++) { ... segreta.setPiolo(i, ...); }
```

Il docente fa il ciclo sulla lunghezza del **campo** e scrive nel **parametro**: funziona perché
il costruttore gli passa proprio il campo. La mia versione usa solo il parametro, cioè la
combinazione «ricevuta come argomento» della slide 25. Per il resto identica: stesso
`nextInt(values().length - 1) + 1`.

---

## Cosa porto via

- **Prima l'algoritmo a mano, poi il codice.** Neri, minimi e totale − neri li avevo calcolati il
  giorno prima sulle slide 31 e 33: il metodo è venuto quasi in traduzione.
- **Stampe contro tabella a mano.** Il bug dei minimi l'ho trovato io: la prima riga della tabella
  che non tornava (`totali` 3 invece di 4) indicava il ciclo giusto.
- **Due spazi diversi, due limiti diversi**: posizioni (`dim()`) e colori (`values().length`).
  Il *for each* sui colori elimina la scelta del limite.
- **Il *for each* e `Arrays`** (`fill`, `equals`) tolgono di mezzo i confini, cioè l'errore n. 6.
- **Due cicli con estremi** al posto di un ciclo con contatori che si consumano, quando si
  riempiono fasce consecutive (prima i neri, poi i bianchi).
- **Struttura dall'UML, promesse dalla semantica, tempo sui confini**: la procedura d'esame
  (prontuario §2) funziona anche sull'algoritmo.
