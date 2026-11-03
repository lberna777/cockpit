---
tags: [FI2, confronto]
---

# Confronto — FI2 LAB07 MyCalendar: il mio codice e la soluzione del docente

**Mio**: `src/model/` e `src/control/` di questa cartella (14/14 test verdi il 2026-11-03, svolto
**con guida** in chat; verificati anche in cloud con `javac` + JUnit) · **Docente**:
`materiali/lab/Lab07-MyCalendar-Soluzione.zip`
**Regola**: dove le due versioni differiscono, **si segue quella del docente**. La colonna *migliore*
dice comunque quale delle due regge meglio e perché.

## In sintesi

| # | Punto | Differenza | Migliore | Da seguire |
|---|---|---|---|---|
| 1 | Costruttori di `Appointment` | io assegno i campi, lui chiama i setter (`setDuration` compreso) | docente | docente |
| 2 | `equals` | io `isEqual` sulle date, lui `equals` | pari | docente |
| 3 | `toString` | io formatter scritto due volte, `Locale.ITALY` e durata; lui un formatter locale, senza durata | docente | docente |
| 4 | `main` in `Appointment` | io c'è (prova del `toString`), lui no | docente | docente |
| 5 | Array più grande in `add` | io una `AppointmentCollection` intera per prenderne l'array, lui un `Appointment[]` | docente | docente |
| 6 | Inserimento in `add` | io due righe, lui `innerContainer[size++] = …` | pari | docente |
| 7 | `get` e `remove` con indice fuori range | io nessun controllo, lui `null` / nessuna azione | docente | docente |
| 8 | Ultima cella dopo `remove` | io la metto a `null`, lui la lascia | io | docente |
| 9 | Capacità della collezione in `MyCalendar` | io quella di default (10), lui 100 | pari | docente |
| 10 | `getAppointmentsIn` | io `allAppointments.get(i)` tre volte, lui una variabile `app` e capacità `size()` | docente | docente |
| 11 | Mezzanotte di un giorno | io `date.atStartOfDay()`, lui `LocalDateTime.of(date, LocalTime.of(0, 0))` | pari | docente |
| 12 | Lunedì della settimana | io `getValue() - 1`, lui `getValue() - DayOfWeek.MONDAY.getValue()` | docente | docente |
| 13 | `getAllAppointments` | io restituisco la collezione vera, lui una **copia** (slide 29) | docente | docente |

---

## 1. Costruttori di `Appointment`

```java
// mio
public Appointment(String description, LocalDateTime from, Duration duration) {
    super();
    this.description = description;
    this.from = from;
    this.to = from.plus(duration);       // la stessa riga di setDuration, ricopiata
}

// docente
public Appointment(String description, LocalDateTime from, Duration duration){
    setDescription(description);
    setFrom(from);
    setDuration(duration);               // riusa il setter: il calcolo di to sta in un posto solo
}
```

Il risultato è identico. Ma con i setter la regola «`to` = `from` + durata» è scritta **una volta
sola**: se un domani `setDuration` controllasse che la durata non sia negativa, il costruttore lo
erediterebbe gratis. È la seconda domanda della scheda («quale metodo fa già questo?»), che nel mio
codice è rimasta senza risposta. Nota anche l'ordine: `setFrom` **prima** di `setDuration`,
altrimenti `from` è `null` e `from.plus(...)` lancia `NullPointerException`.

## 2. `equals`

```java
// mio
return (app.description.equals(this.description) && app.from.isEqual(this.from) && app.to.isEqual(this.to));

// docente
return from.equals(app.getFrom()) && to.equals(app.getTo())
        && description.equals(app.getDescription());
```

Stessi tre campi, stessa logica. Su `LocalDateTime` (senza fuso orario) `isEqual` e `equals` danno lo
stesso risultato. La versione del docente usa i getter dell'altro oggetto e non ha le parentesi
esterne, che non servono. La prima versione mia confrontava `description` con `==`, e passava i test
solo perché le stringhe letterali `"Natale"` vengono riusate da Java: **mai `==` sulle stringhe**.

## 3. `toString`

```java
// mio
return "Appointment: " + description
     + "\nDA: " + from.format(DateTimeFormatter.ofLocalizedDateTime(FormatStyle.SHORT).withLocale(Locale.ITALY))
     + "\nA:"   + to.format(DateTimeFormatter.ofLocalizedDateTime(FormatStyle.SHORT).withLocale(Locale.ITALY))
     + "\nDURATA: " + getDuration();

// docente
DateTimeFormatter dateFormatter = DateTimeFormatter.ofLocalizedDateTime(FormatStyle.SHORT, FormatStyle.SHORT);
return ("Impegno: " + description + " con inizio "
        + dateFormatter.format(from) + " e fine " + dateFormatter.format(to));
```

Il formatter si crea **una volta** in una variabile e si usa due volte: è ciò che chiede la slide 23
(«formatta le date usando un DateTimeFormatter»). La durata nel `toString` non è richiesta, e
`getDuration()` stampato così esce come `PT3H30M`. `ofLocalizedDateTime(SHORT, SHORT)` dà stile
separato per data e ora; con un solo argomento vale per entrambe.

## 4. `main` in `Appointment`

Il mio `main` serviva a vedere il `toString`, perché nessun test lo controlla. Ma non è nell'UML della
slide 24: **all'esame va cancellato**, non commentato. Restano da togliere anche l'import inutile
`java.util.Objects` (residuo di `hashCode`) e i `super();` generati da Eclipse.

## 5. Array più grande in `add`

```java
// mio
AppointmentCollection app = new AppointmentCollection(this.innerContainer.length * this.DEFAULT_GROWTH_FACTOR);
for (int i = 0; i < size; i++) {
    app.innerContainer[i] = this.innerContainer[i];
}
this.innerContainer = app.innerContainer;

// docente
Appointment[] newContainer = new Appointment[size * DEFAULT_GROWTH_FACTOR];
for (int i = 0; i < innerContainer.length; ++i) {
    newContainer[i] = innerContainer[i];
}
innerContainer = newContainer;
```

Mi serviva solo un array, e ho costruito una collezione intera per prenderle il suo: funziona (la
classe può leggere i campi `private` di un altro oggetto della stessa classe), ma è un giro in più.
`this.DEFAULT_GROWTH_FACTOR`: una costante `static` si scrive senza `this.`. Il ciclo e
l'assegnazione finale sono gli stessi; dentro l'`if` l'array è pieno, quindi `size` e `length`
coincidono e i due estremi si equivalgono.

⚠️ Tutte e due le versioni si rompono con una collezione di capacità **0**: `0 × 2 = 0`, l'array
nuovo è ancora vuoto e `innerContainer[size]` lancia `ArrayIndexOutOfBoundsException`. Nei test non
capita; nel LAB04c il mio `put` gestiva il caso con un `if (length == 0)`.

## 6. Inserimento in `add`

```java
// mio
this.innerContainer[size] = appointment;
size++;

// docente
innerContainer[size++] = appointment;   // usa size come indice, POI lo incrementa
```

Equivalenti. `size++` restituisce il valore **prima** dell'incremento, per questo l'indice usato è
quello vecchio. Le due righe separate sono più facili da leggere: vanno bene anche all'esame.

## 7. `get` e `remove` con indice fuori range

```java
// docente
public Appointment get(int index) {
    if (index < 0 || index >= size)
        return null;                  // fuori dagli elementi validi: niente
    return innerContainer[index];
}

public void remove(int index) {
    if (index < 0 || index >= size)
        return;                       // niente da togliere
    ...
}
```

Nel mio codice, su una collezione con 3 elementi e capacità 10, `get(5)` restituisce un `null` per
caso (le celle oltre `size` sono vuote), mentre `get(15)` e `get(-1)` lanciano
`ArrayIndexOutOfBoundsException`. `remove(-1)` farebbe lo stesso. Il
controllo `index < 0 || index >= size` è il confine giusto: gli indici validi vanno da `0` a
`size - 1`.

## 8. Ultima cella dopo `remove`

```java
// mio
for (int i = index; i < this.size-1; i++) {
    this.innerContainer[i] = this.innerContainer[i+1];
}
this.innerContainer[size-1] = null;   // svuoto il doppione rimasto in fondo
size--;

// docente
for (int i = index; i < size - 1; ++i) {
    innerContainer[i] = innerContainer[i+1];
}
size--;
```

Stesso ciclo, stessi estremi: è quello su cui ho sbagliato quattro volte prima di arrivarci. Il docente
non azzera l'ultima cella: oltre `size` nessuno legge, quindi funziona. Il mio `null` in più è la
pulizia corretta (l'oggetto non resta trattenuto dall'array), ed è innocuo. Da seguire resta il
docente, ma il `null` si può tenere.

## 9. Capacità in `MyCalendar`

```java
// mio
this.allAppointments = new AppointmentCollection();      // 10, poi cresce

// docente
allAppointments = new AppointmentCollection(100);
```

Con la collezione che si ingrandisce da sola, la capacità iniziale è solo una questione di efficienza.
Pari.

## 10. `getAppointmentsIn`

```java
// mio
AppointmentCollection coll = new AppointmentCollection();
for (int i = 0; i < allAppointments.size(); i++) {
    if (isOverlapped(allAppointments.get(i).getFrom(), allAppointments.get(i).getTo(), start, finish)) {
        coll.add(allAppointments.get(i));
    }
}

// docente
AppointmentCollection appList = new AppointmentCollection(allAppointments.size());
for (int i = 0; i < allAppointments.size(); i++) {
    Appointment app = allAppointments.get(i);           // preso una volta, usato tre
    if (isOverlapped(app.getFrom(), app.getTo(), start, end)) {
        appList.add(app);
    }
}
```

Una variabile locale per l'elemento corrente: si legge meglio e non si ripete `get(i)`. Capacità
`size()`: il risultato non può avere più elementi di tutti gli appuntamenti, quindi non cresce mai
(ma con 0 appuntamenti la capacità è 0: vedi il ⚠️ del punto 5, qui non scatta perché non si aggiunge
niente).

`isOverlapped` è identico al mio, con le due condizioni scritte in ordine inverso: `start < refEnd
&& end > refStart`.

## 11. Mezzanotte di un giorno

```java
// mio
date.atStartOfDay()

// docente
LocalDateTime.of(date, LocalTime.of(0, 0))
```

Stesso valore. `atStartOfDay()` è più corto e dice cosa fa; il docente costruisce il `LocalDateTime`
da una data e un orario. Conviene conoscere tutte e due le forme.

## 12. Lunedì della settimana

```java
// mio
int giorniDaTogliere = date.getDayOfWeek().getValue() - 1;

// docente
long distanceFromPastMonday = date.getDayOfWeek().getValue() - DayOfWeek.MONDAY.getValue();
```

Stesso numero, perché `DayOfWeek.MONDAY.getValue()` vale 1. Il docente scrive **perché** sottrae
quel valore invece di un `1` da spiegare: il codice si commenta da solo.

## 13. `getAllAppointments`

```java
// mio
return allAppointments;               // la collezione vera

// docente
AppointmentCollection appCollection = new AppointmentCollection(allAppointments.size());
for (int i = 0; i < allAppointments.size(); i++) {
    appCollection.add(allAppointments.get(i));
}
return appCollection;                 // una copia
```

La slide 29 lo chiede: «restituisce una copia della collezione». Con la mia versione chi riceve la
collezione può fare `remove(0)` e cancellare un appuntamento dal calendario senza passare da
`MyCalendar.remove`. Con la copia, il calendario resta l'unico a modificare i propri dati. È il
senso del controller («tutto passa attraverso di lui», slide 29). Nota: la copia è della
**collezione**, gli `Appointment` dentro sono gli stessi oggetti.

---

## Cosa porto via

- **Riusare i propri metodi**: costruttori che chiamano i setter (1), un formatter in una variabile
  (3), un elemento in una variabile locale (10). Ogni regola scritta una volta sola.
- **Gli indici validi vanno da `0` a `size - 1`**: è il confine dei controlli in `get` e `remove` (7) e
  degli estremi dei cicli di spostamento (8). `length` serve solo per sapere se l'array è pieno.
- **Leggere tutte le slide della classe, non solo l'UML**: la copia in `getAllAppointments` (13) è
  scritta nella slide 29 e nessun test la controlla.
- **Prima di consegnare**: niente `main` né import inutili nel model (4), niente `this.` davanti alle
  costanti `static` (5).
