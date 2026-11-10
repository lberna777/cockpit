---
tags: [FI2, confronto]
---

# Confronto — FI2 LAB08 EDLift: il mio codice e la soluzione del docente

**Mio**: `src/edlift/model/` di questa cartella (60/60 test verdi il 2026-11-10, svolto **con guida**
in chat; verificati con `javac` + JUnit 5) · **Docente**: `materiali/lab/Lab08-EDLift-Soluzione.zip`
**Regola**: dove le due versioni differiscono, **si segue quella del docente**. La colonna *migliore*
dice comunque quale delle due regge meglio e perché.

## In sintesi

| # | Punto | Differenza | Migliore | Da seguire |
|---|---|---|---|---|
| 1 | `REJECTED` del salutista | io la restituisco senza `setMsg`/`setFloor`, lui li imposta sempre | docente | docente |
| 2 | Le due condizioni di rifiuto del salutista | io un solo `if` con `\|\|`, lui due rami separati | docente | docente |
| 3 | Piano «prima» del salutista | io due rami quasi uguali, lui l'operatore `? :` e un solo blocco | docente | docente |
| 4 | `getMode` | io `BASIC`, `HEALTHY`, `MULTI`, lui `Basic`, `Healthy`, `Multi` | pari | docente |
| 5 | `goToFloor` del multipiano | stessa logica, rami in ordine inverso; io `insert(floor) == true`, lui `!queue.insert(floor)` | docente | docente |
| 6 | `@Override` su `hasPendingFloors`/`nextPendingFloor` | mancano a tutti e due | nessuno | metterlo |
| 7 | Import inutile `com.sun.net.httpserver.Request` | io c'è (aggiunto da Eclipse), lui no | docente | docente |
| 8 | `Queue`: capacità | io `bookings.length` (il campo `maxBookings` resta inutilizzato), lui `maxBookings` | pari | docente |
| 9 | `Queue.hasItems` | io `if/else` con `true`/`false`, lui `return booked > 0;` | docente | docente |
| 10 | `Queue.toString` | io assente, lui `Arrays.toString(Arrays.copyOf(bookings, booked))` | docente | docente |

---

## 1. `REJECTED` del salutista: la costante dell'enum ha uno stato condiviso

```java
// mio
if (getCurrentState() != LiftState.REST ||
        Math.abs(getCurrentFloor() - floor) <= 1) {
    return RequestResult.REJECTED;          // msg e floor restano quelli dell'ultima chiamata a setMsg/setFloor
}

// docente
result = RequestResult.REJECTED;
result.setMsg("rejected as unhealthy");    // messaggio di questo rifiuto
result.setFloor(Integer.MIN_VALUE);        // nessun piano
```

`RequestResult.REJECTED` è **un solo oggetto** in tutto il programma: `setMsg` e `setFloor` lo
modificano per tutti. Verificato il 10/11: dopo un rifiuto del multipiano per coda piena, il
salutista che rifiuta 5 → 6 restituisce il messaggio `REJECTED: Queue's full` (e `r == r2` è
`true`). I test non lo vedono perché ogni test crea un ascensore nuovo ma **non** azzera l'enum.
Regola: chi restituisce una costante con dati la reimposta **sempre** prima del `return`.

## 2. Due motivi di rifiuto, due rami

Io ho fuso «è in movimento» e «piano troppo vicino» in una condizione. Funziona, ma i due rifiuti
hanno motivi diversi e il docente dà a ciascuno il suo messaggio. Con il `||` non si può.

## 3. Il piano «prima»

```java
// mio: due rami che differiscono solo per + e −
if (getCurrentFloor() > floor) { setRequestedFloor(floor + 1); ... }
else                           { setRequestedFloor(floor - 1); ... }

// docente: si calcola il piano, poi un solo blocco
actualDestinationFloor = floor < getCurrentFloor() ? floor + 1 : floor - 1;
setRequestedFloor(actualDestinationFloor);
```

Stesso risultato; il docente scrive una volta sola `setRequestedFloor`, `setMsg`, `setFloor`.

## 4. `getMode`

I test fanno `toUpperCase()`, quindi passano tutte e due. La factory `Lift.of` invece usa
`"MULTIFLOOR"`: sono stringhe diverse con usi diversi (scheda del lab, «Casi limite»).

## 5. `goToFloor` del multipiano

```java
// mio
if (getCurrentState() == LiftState.REST) {
    setRequestedFloor(floor);              // fermo: si parte subito, la coda non serve
    return RequestResult.ACCEPTED;
} else {
    if (queue.insert(floor) == true) { return RequestResult.ACCEPTED; }
    else { /* REJECTED con msg e MIN_VALUE */ }
}

// docente
if (getCurrentState() != LiftState.REST) {
    if (!queue.insert(floor)) { /* REJECTED con msg e MIN_VALUE */ }
    return RequestResult.ACCEPTED;
} else {
    setRequestedFloor(floor);
    return RequestResult.ACCEPTED;
}
```

La logica coincide. `== true` su un `boolean` è ridondante: `if (queue.insert(floor))`.
Il punto che mi ha bloccato: la **prima** chiamata ad ascensore fermo **non** va in coda, va
dritta in `requestedFloor` (test `QuintaPrenotazioneRifiutata`: 3 diretto + 7, 6, 9, 4 in coda da 4).

## 6. `@Override` sui metodi «gancio»

`hasPendingFloors` e `nextPendingFloor` ridefiniscono i metodi di `Lift` che rispondono sempre
«no». Nessuno dei due mette `@Override`: compila lo stesso, ma senza l'annotazione un errore di
firma (es. `nextPendingFloor()` senza parametro) crea un metodo nuovo che il Controller non chiama
mai, e nessuno se ne accorge.

## 7. Import inutile

`import com.sun.net.httpserver.Request;` l'ha aggiunto Eclipse con un completamento. Non serve e
lega la classe a un modulo del JDK che non c'entra: *Source → Organize Imports* (Ctrl+Shift+O) lo
toglie.

## 8–10. `Queue`

Logica identica (inserimento con `booked` come indice, estrazione con ricopiatura fino a
`booked − 1`, `MIN_VALUE` se vuota). Il docente aggiunge `toString` e due `System.err.println`
di debug dentro `insert` ed `extract`, da non copiare nel codice d'esame.
