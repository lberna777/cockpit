---
tags: [FI2, confronto]
---

# Confronto — FI2 LAB04a: il mio codice e la soluzione del docente

**Mio**: `src/` di questa cartella (test verdi il 2026-10-01, **guidato**: `sum` scritta da solo,
`mul` corretta dopo due domande in chat) · **Docente**:
`materiali/lab/Lab04a-FrazioniBase-Soluzione.zip`
**Regola**: dove le due versioni differiscono, **si segue quella del docente**.

## In sintesi

| # | Punto | Differenza | Migliore | Da seguire |
|---|---|---|---|---|
| 1 | `FrazLib.sum` | stessa struttura: elemento neutro, *for each*, riuso di `Frazione.sum` | — | — |
| 2 | `FrazLib.mul` | uguale, **dopo** la correzione (prima era una copia di `sum`) | — | — |
| 3 | elemento neutro | io `new Frazione(0)` / `new Frazione(1)`, lui `(0, 1)` / `(1, 1)` col commento | pari | — |
| 4 | package e `import` | stessa ristrutturazione `util` / `frazione` / `frazlib` | — | — |

`Frazione` e `MyMath` sono quelle del mio LAB03, già confrontate in `confronto_LAB03.md`.

---

## 1–2. `sum` e `mul`

```java
// mio, versione finale
public static Frazione mul(Frazione[] fs) {
    Frazione mulTemp = new Frazione(1);
    for (Frazione f : fs) {
        mulTemp = mulTemp.mul(f);
    }
    return mulTemp;
}
```
```java
// docente
Frazione tmp = new Frazione(1, 1); // Elemento neutro
for (Frazione f : fs)
    tmp = tmp.mul(f);
return tmp;
```
**Identici nella logica.** Nessuna aritmetica nuova in `FrazLib`: ripete l'operazione a due che
`Frazione` sa già fare, lungo l'array. È il punto «riusare i metodi della classe» di LAB03, questa
volta preso al primo colpo su `sum`.

**L'errore di `mul`** (prima versione): copiata da `sum` senza adattarla, con **due** righe sbagliate:
partiva da `0` e chiamava `.sum(f)`. Il test l'ha preso subito (prima `assert` su `mul`). Con la sola
chiamata corretta, il prodotto sarebbe stato `0` per qualunque array: l'elemento neutro dipende
dall'operazione (`0` per la somma, `1` per il prodotto).

## 3. Casi che i test non coprono

- **Array vuoto**: `sum` → `0/1`, `mul` → `1/1`. Corretto in entrambe le versioni, ed è proprio
  l'effetto dell'elemento neutro.
- **Una sola frazione**: il risultato è `neutro op f`, che passa da `minTerm()` dentro `Frazione.sum`
  / `mul`. Quindi `sum({3/6})` restituisce `1/2`, ridotta. Il `179/420` del secondo caso è ridotto per
  lo stesso motivo: lo riduce `Frazione`, non `FrazLib`.
- **Cella `null`**: `NullPointerException` (error, non failure). Nessuna delle due versioni lo
  gestisce, e il testo non lo chiede.

---

## Cosa porto via

- **Copiare un metodo gemello è il punto in cui nascono gli errori**: dopo il copia-incolla, rileggere
  ogni riga chiedendosi «ha senso per *questa* operazione?».
- **Elemento neutro**: il valore da cui parte un accumulatore è quello che non cambia il risultato
  dell'operazione. `0` per `+`, `1` per `×`.
- `Frazione[]` esiste automaticamente per ogni classe: non va dichiarato da nessuna parte.
