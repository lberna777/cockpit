---
tags: [FI2, confronto]
---

# Confronto — FI2 LAB05 (parte 1): il mio codice e la soluzione del docente

**Mio**: `src/ticketsosta/` di questa cartella (test verdi il 2026-10-05) · **Docente**:
`materiali/lab/Lab05-TicketSosta-Soluzione.zip`
**Regola**: dove le due versioni differiscono, **si segue quella del docente**. La colonna *migliore*
dice comunque quale delle due regge meglio e perché.

## In sintesi

| # | Punto | Differenza | Migliore | Da seguire |
|---|---|---|---|---|
| 1 | Minimo dopo la franchigia | io confronto `minutiSosta`, lui la durata dopo la franchigia | docente | docente |
| 2 | Franchigia | io la sottraggo dai minuti, lui sposta l'inizio con `plusMinutes` | io | docente |
| 3 | Struttura | io un metodo a 4 passi, lui franchigia/minimo in `emettiTicket` e durata calcolata due volte | io | docente |
| 4 | Formula del costo | `costoOrario * (min / 60.0)` contro `min * costoOrario / 60.0` | pari | docente |
| 5 | Mezzanotte (fine `00:00`, fine prima dell'inizio) | io non la gestisco, lui con un `if` | docente | docente |
| 6 | Getter di `Ticket` | io `getInizio`/`getFine`, lui `getInizioSosta`/`getFineSosta` | docente | docente |
| 7 | `toString` di `Ticket` | io `SOSTA AUTORIZZATA---`, `Dalle`/`Alle`; lui `Sosta autorizzata`, `dalle`/`alle` | docente | docente |
| 8 | `toString` di `Parcometro` | io `tariffa: `, lui `tariffa ` | pari | docente |

---

## 1. Minimo dopo la franchigia

```java
// mio (prima della correzione)
if (minutiSosta < tariffa.getDurataMinima()) { minutiDaPagare = tariffa.getDurataMinima(); }

// docente
if (durataSosta.toMinutes() < tariffa.getDurataMinima())          // durataSosta parte da inizioEffettivo
    costo = tariffa.getDurataMinima() * tariffa.getTariffaOraria() / 60.0;
```

La regola (slide 8) è *«sottrarre franchigia dalla durata, poi se la durata è inferiore al minimo
considerare il minimo»*: il confronto va fatto su quello che resta **dopo** la franchigia.
Caso che separa le due versioni: `H1f` (franchigia 60, minimo 60), 10:00→11:30. Docente: restano 30
minuti, sotto il minimo, si pagano 60 → **0,50 €**. Mio: `90 < 60` è falso, si pagano 30 → **0,25 €**.
I sei test dello startkit non lo coprono: il test verde non provava la regola (`profilo/errori.md`,
pattern 2). Segnalato in chat due volte prima di essere corretto; corretto da Lorenzo il 2026-10-05.

## 2. Franchigia: sottrarre minuti o spostare l'inizio

```java
// mio
long minutiDaPagare = minutiSosta - tariffa.getMinutiFranchigia();
// docente
LocalTime inizioEffettivo = inizio.plusMinutes(tariffa.getMinutiFranchigia());
```

Il mio lavora su numeri interi e non esce mai dalla giornata. Quello del docente con un `LocalTime`
in fondo alla giornata si rompe: `23:30` + 60 minuti dà `00:30`, e il calcolo che segue vede un'ora
*prima* dell'inizio. Il docente lo può permettere perché nella parte 1 la sosta resta in una giornata
(slide 5, ipotesi 1) e la franchigia è breve. All'esame vince il testo del compito.

## 3. Struttura

Il docente scrive nel commento che «andrebbe fattorizzato il codice»: la durata (con il ramo
mezzanotte) è calcolata sia in `emettiTicket` sia in `calcolaCosto`. Il mio `calcolaCosto` ha una
sola catena (durata → franchigia → minimo → ore e costo) ed è più facile da leggere.
Nel `Ticket` entrano comunque gli orari ufficiali (`inizio`, `fine`), non quelli effettivi: uguale.

## 4. Formula

Stesso risultato sui test: `0,50 × 390 / 60.0` e `0,50 × (390 / 60.0)` danno 3,25. Nel mio la
divisione per `60.0` è già un `double`; la trappola era `390 / 60` fra interi (= 6).

## 5. Mezzanotte

```java
// docente
if (a.isBefore(da) || LocalTime.of(0, 0).equals(a))
    durata = Duration.between(da, LocalTime.of(23, 59)).plusMinutes(1);   // fino a fine giornata
```

Nessun test della parte 1 lo usa. Io: `H1`, 22:00→00:00 dà 0,50 € (durata negativa, scatta il minimo)
dove il docente dà 1,00 €. Il caso «fine prima dell'inizio» è la sosta a cavallo della mezzanotte, che
la slide 5 esclude dalla parte 1 e la parte 2 risolve con `LocalDateTime`. Il caso «fine alle 00:00»
è nella slide 12. **Lasciato fuori dalla parte 1 per scelta di Lorenzo** (2026-10-05).

## 6–8. Forma

- Getter: i nomi sono quelli della slide 11 e dell'UML; nessun test della parte 1 li chiama, ma un
  compito che li chiamasse con quel nome non compilerebbe.
- `toString` di `Ticket`: il formato è libero ma conviene copiare quello della slide 11.
- `toString` di `Parcometro`: i due punti in più non cambiano nulla.

## Cosa porto via

1. **Franchigia e minimo si applicano in quest'ordine, sulla durata dopo la franchigia** (punto 1):
   regola della slide 8, da derivare con un caso a mano, non a memoria.
2. **Un test verde dice che i casi dati tornano, non che la regola sia giusta**: scrivere un caso mio
   che attraversi la regola (qui 90 minuti con franchigia 60) prima di dichiarare finito.
3. **Lavorare in minuti interi e convertire in ore alla fine** evita sia la divisione intera sia lo
   sconfinamento oltre mezzanotte (punti 2 e 4).
4. **`LocalTime` non ha la data**: `+ minuti` può scavalcare la giornata senza avvisare. È il motivo
   per cui la parte 2 passa a `LocalDateTime`.
5. **Frammenti riusabili** (per il prontuario): `NumberFormat.getCurrencyInstance(Locale.ITALY)`,
   `DateTimeFormatter.ofLocalizedTime(FormatStyle.SHORT).withLocale(Locale.ITALY)`,
   `Duration.between(a, b).toMinutes()` contro `toMinutesPart()`.

---

# Parte 2 — `TicketEvoluto`, `ParcometroEvoluto`

**Mio**: `src/ticketsostaevoluto/` (8 test verdi in Eclipse il 2026-10-05) · **Docente**: `Lab05-TicketSosta-Soluzione.zip`, stesso package.
Svolta con guida: il blocco del **minimo** nel ramo «stesso giorno» di `calcolaCostoSuPiuGiorni` è stato
scritto da Claude (verificato eseguendo gli 8 casi); il resto (ciclo sui giorni, franchigia, `toString`) da Lorenzo
dopo correzioni.

## In sintesi

| # | Punto | Differenza | Migliore | Da seguire |
|---|---|---|---|---|
| 9 | Da giorno della settimana a indice | io `getDayOfWeek().getValue() - 1`, lui `getDayOfWeek().ordinal()` | docente (una chiamata, nessun `- 1` da ricordare) | docente |
| 10 | **Dove sta il minimo** | io solo nel ramo «stesso giorno»; lui in `emettiTicket`, sull'intera sosta, con la tariffa del primo giorno | **docente** | docente |
| 11 | Struttura del calcolo | io `if` per un giorno + 3 pezzi (primo, `while` sui giorni in mezzo, ultimo); lui un solo `while` su tutti i giorni con `if` per primo/ultimo | docente (nessun caso a parte, la tariffa si legge una volta) | docente |
| 12 | Franchigia | io `da.plusMinutes(...)` ripetuto in due righe lunghe; lui nel `while`, solo sul primo giorno | pari sul risultato, docente sulla leggibilità | docente |
| 13 | Costruttore | io tengo il riferimento all'array; lui `Arrays.copyOf(tariffa, 7)` | docente (copia difensiva, come per `FractionCollection`) | docente |
| 14 | `toString` | io `String` + ciclo con indice; lui `StringBuilder` + `for` ciascuno | docente | docente |
| 15 | Mezzanotte con le date | stesso trucco (`MIDNIGHT` / `00:00` come fine giorno) | pari | — |
| 16 | Getter di `TicketEvoluto` | io `getInizio`/`getFine`, lui `getInizioSosta`/`getFineSosta` | docente | docente |

## 10. Dove sta il minimo

```java
// docente — in emettiTicket, sull'intera sosta
long durataSosta = Duration.between(inizioEffettivo, fine).toMinutes();
if (durataSosta < tariffaPrimoGiorno.getDurataMinima())
    costo = tariffaPrimoGiorno.getDurataMinima() * tariffaPrimoGiorno.getTariffaOraria() / 60.0;
else
    costo = calcolaCostoSuPiuGiorni(inizio, fine);
```

Il mio controllo del minimo sta nel solo ramo «stesso giorno». Caso che li separa (provato eseguendo):
martedì 23:50 → mercoledì 00:30 (40 minuti di sosta, franchigia 60, minimo 60): **docente 0,50 €, io 12,33 €**.
Nella parte 1 la regola era *«sottrarre franchigia dalla durata, poi controllare il minimo»* (slide 8): il
minimo riguarda l'**intera sosta**, non il singolo giorno. I test dello startkit non hanno un caso a cavallo
di mezzanotte che lo faccia emergere.

## 12. Franchigia a cavallo di mezzanotte — debolezza comune

Martedì 23:30 → mercoledì 10:00 (franchigia 60 sul martedì): **docente e io 26,75 €**, ma il costo corretto è
14,25 € (i 60 minuti gratuiti arrivano fino alle 00:30 del mercoledì). In entrambi, `plusMinutes` su un `LocalTime`
(o `.toLocalTime()` dopo un `plusMinutes`) fa **ripartire** da 00:30 dello stesso giorno. Non è nei test, e il
docente ha la stessa debolezza: la menziono, non la correggo.

## Cosa porto via (parte 2)

1. **Il minimo riguarda la sosta intera**: va deciso prima di spezzare in giorni (punto 10).
2. **Gli oggetti di `java.time` sono immutabili**: `da.plusDays(1);` da solo non fa niente, il risultato va assegnato
   (il ciclo che non terminava, 2026-10-05).
3. **La variabile del ciclo dice qual è il giorno che stai pagando, non quello da cui sei partito**: tariffa dal
   `giorno` che avanza, non da `da`; e `giorno` deve partire dal giorno **dopo** la partenza, senza `+ 1` anche nella condizione.
4. **Eclipse può modificare una classe che non stai scrivendo**: un *quick fix* ha cambiato `Ticket` della parte 1 da
   `LocalTime` a `LocalDateTime` e il progetto ha smesso di compilare. Dopo ogni quick fix, leggi quale file ha cambiato.
5. **Per trovare il bug, stampare**: la `println` del giorno nel ciclo avrebbe mostrato subito la tariffa sbagliata.
