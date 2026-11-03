# Giornata 2026-11-03

<!-- Claude appende qui, una riga per fatto: HH:MM · CODICE · fatto.
     Marcatori: CHIUSO <cod> <mod> · RIPASSO <cod> <mod> ok|debole -->

12:50 · FI2 · LAB07 Appointment: costruttori e getDuration ok; Lorenzo non ha chiaro cosa debba fare un setter di proprietà calcolata (setDuration scrive sul parametro invece che su to).
12:51 · FI2 · LAB07 Appointment: setDuration corretto da Lorenzo dopo la spiegazione (setter di proprietà calcolata = scrive il campo da cui la proprietà dipende).
12:57 · FI2 · LAB07 AppointmentTest 5/6 verdi (manca equals: testEqualsAppointment in failure). Pausa pranzo.
14:15 · FI2 · LAB07 AppointmentTest 6/6 verdi, ma equals confronta description con == (passa solo per stringhe letterali internate): pattern 2, verde ≠ corretto. Da correggere con equals.
14:19 · FI2 · LAB07 equals corretto da Lorenzo (description.equals, return diretto), hashCode rimosso.
15:19 · FI2 · LAB07 Appointment finito (6/6 verdi, toString provato con main). Si passa ad AppointmentCollection.
15:27 · FI2 · LAB07 AppointmentCollection: Lorenzo ha perso il filo sui due costruttori (perché due, cosa fa this(...)); rispiegato da capo con esempio.
16:00 · FI2 · LAB07 remove: tre tentativi con limiti sbagliati, size e length usati come intercambiabili (pattern 1, distinzione collassata: posti occupati vs posti esistenti). Dato il codice corretto con traccia.
16:04 · FI2 · LAB07 AppointmentCollection 3/3 verdi (remove corretto su [size-1]). Lorenzo dichiara: non chiaro lavorare con gli array, soprattutto contenitori annidati ed espansione/restrizione (registrato in profilo/errori.md, pattern 6). Si passa a MyCalendar.
16:49 · FI2 · LAB07 MyCalendar: costruttore, add, getAllAppointments, remove (indexOf + -1 → false) scritti. Restano getDay/Month/WeekAppointments, getAppointmentsIn, isOverlapped.
17:12 · FI2 · LAB07 isOverlapped e getAppointmentsIn corretti (dopo ||→&&: confondeva «sovrapposto» con «contenuto», sbloccato con la tabella dei sei casi).
17:31 · FI2 · CHIUSO FI2 LAB07 — 14/14 verdi, guidato. Restano ritocchi (private, copia in getAllAppointments), copia in svolti/ e confronto.
