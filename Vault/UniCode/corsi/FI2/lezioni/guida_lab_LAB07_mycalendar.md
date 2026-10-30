---
tags: [FI2, guida-lab]
---

# Scheda — FI2 LAB07: MyCalendar
**Materiale**: `LAB-07-MyCalendar.pdf` (sl. 1–51), `-Recap.pdf`, `-Commento.pdf` (**solo dopo i test verdi**: contiene codice della soluzione), `Lab07-MyCalendar-Startkit.zip` (view a console pronta, 3 classi di test, 14 test) · **Modalità**: guidata
**Teoria che entra qui**: `10` *Date* — `Duration` (10 sl. 22–26), `LocalDateTime` come in LAB05 · `12` *Sistemi a oggetti* — MVC (LAB07 sl. 6–11), associazione e composizione in UML (sl. 13–19) · `S02` JUnit.

## Setup
- *Existing Projects* → *Select root directory* → `~/cockpit/Vault/UniCode/corsi/FI2/esame_FI2/da_importare/LAB07_MyCalendar-301026` → **Copy projects into workspace**; poi **rinomina il progetto** (il `.project` dice `Lab07-MyCalendar-Startkit`).
- Due source folder `src` e `test`. Package **da creare tu**: `model` (Appointment, AppointmentCollection) e `control` (MyCalendar) [sl. 39–41]. X rosse attese: in `consoleview` e in tutti e tre i test, finché mancano le classi.
- `AppointmentTest` importa `org.junit.Test` (JUnit 4), gli altri due JUnit 5: se Eclipse non lo trova, *Quick Fix → Add JUnit 4 library*, o cambia l'import in `org.junit.jupiter.api.Test`.
- Procedura d'esame: **prontuario §2**, otto passi. Oggi la usiamo su `Appointment`.

## Ordine di lavoro
| # | Classe | Cosa rappresenta | Test | Costrutto nuovo → slide |
|---|---|---|---|---|
| 1 | `model.Appointment` | un appuntamento **modificabile**: descrizione, inizio, fine; due costruttori, get/set, `equals`, `toString` | `AppointmentTest` (6) | `Duration` → 10 sl. 22–25; UML sl. 24 |
| 2 | `model.AppointmentCollection` | FractionCollection (LAB04c) con `Appointment` al posto di `Frazione`; `put` diventa `add`, in più `indexOf` | `AppointmentCollectionTest` (3) | UML sl. 26; `equals` per cercare → sl. 25 |
| 3 | `control.MyCalendar` | il controller: tiene la collezione, aggiunge, rimuove, filtra per giorno/mese/settimana | `MyCalendarTest` (5) | intervalli `[inizio, fine)` → sl. 31–38; UML sl. 33 |

Si parte da quella con meno legami [sl. 21]. Firme: UML delle sl. 24, 26, 33, confermate dai test (`new AppointmentCollection(10)`, `myCal.remove(app)` → `boolean`).

## Casi limite da pensare
- UML sl. 24: tre campi, ma quattro coppie get/set. Quale proprietà **non** è un campo, e perché tenerla come campo sarebbe un errore? (sl. 22–23: «proprietà calcolata»)
- `setDuration`: cosa resta fermo e cosa si ricalcola? Verifica sul caso del test: 12:45 + 10 min, poi durata 20 min → `to` atteso? (`testSetGetDuration`)
- Secondo costruttore: in che **ordine** devi impostare i valori perché `setDuration` funzioni?
- `equals`: quando due appuntamenti sono uguali? Solo dalla firma UML e dai due test, **non inventare** [sl. 23]. Nota la firma: `equals(app: Appointment)`, non `Object`.
- `remove` di MyCalendar riceve un appuntamento, quello della collezione un **indice**: come passi dall'uno all'altro?
- Giorno: dove finisce il 10 marzo? Mese: un `LocalDate` del **10** marzo deve dare tutto marzo (`testGetListAppointmentMonth`).
- Sovrapposizione [sl. 38]: disegna i quattro casi su una riga del tempo **prima** di scrivere la condizione. Un appuntamento che finisce alle 00:00 del giorno dopo, è nel giorno?
- ⚠️ Pattern 2: finito quando passano **tutti** i 14 (tasto destro su `test` → *Run As → JUnit Test*); più un caso tuo: appuntamento da lunedì a mercoledì, cercato il martedì [sl. 30].

## Test rosso?
Non compila (package `model`/`control`, firma) · failure (leggi `expected / but was`) · error (`NullPointerException`: `from` ancora `null` quando calcoli la durata?) → prontuario §1, oppure scrivilo in chat.

## Dopo i test verdi
- copia `src` e `test` in `corsi/FI2/esame_FI2/svolti/LAB07_MyCalendar/`;
- apri `Lab07-MyCalendar-Soluzione.zip` e il **Commento**: confronta durata calcolata, `equals`, `isOverlapped`, calcolo del lunedì;
- Claude scrive `svolti/LAB07_MyCalendar/confronto_LAB07.md`; `/chiudi` aggiorna il prontuario (§ `model`: oggetto modificabile, proprietà calcolata; § `controller`: intervalli e sovrapposizione).
- Opzionale [sl. 44]: `getWeekAppointments` è già nei test (`testGetListAppointmentWeek`).
