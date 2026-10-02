# Giornata 2026-10-02

<!-- Claude appende qui, una riga per fatto: HH:MM · CODICE · fatto.
     Marcatori: CHIUSO <cod> <mod> · RIPASSO <cod> <mod> ok|debole -->

11:48 · FI2 · guida-lab LAB04c generata (scheda + progetto importabile LAB04c_FractionCollection-021026); LAB04c in corso.
12:10 · FI2 · LAB04c: errore mio (Claude) nel progetto — messa in `LAB04c_…-021026` la `Frazione` di partenza del 04b (senza `static`) invece della sua; corretta sovrascrivendo da `svolti/`. Lorenzo aveva anche importato lo zip della Soluzione e poi dello Startkit invece del progetto preparato (due progetti 04c nel workspace).
12:25 · FI2 · LAB04c: capito da solo il senso dell'ADT (array nascosto, non più trattato nudo); chiesto perché 3 costruttori (diagramma sl. 59: `(Frazione[])`, `(int)`, `()`); capito `size` ≠ `length` («length non va bene»).
12:40 · FI2 · LAB04c: campi iniziali `collection` e `physicalSize` (non nel modello), costruttore `(int)` solo memorizzava il numero senza creare l'array, `size` assente; dichiarato «sono veramente confuso». Dopo il modello a scaffale (array = posti, `size` = occupati) e la lettura riga per riga del diagramma: `innerContainer`, `size`, due costanti, costruttori `(int)` e `()` giusti.
13:10 · FI2 · LAB04c: costruttore `(Frazione[])` scritto con `Frazione.size`, copia solo le celle occupate, lunghezza = `size` (scelta B); verificato da Claude con array da 2, 4, 0 frazioni: corretto, copia reale. Inciampo: `Frazione.Size` (maiuscola). NON chiuso: mancano `size()`, `get`, `put`, `remove`, `toString`, `sum`, `mul`.
13:30 · FI2 · prontuario: §3.12 (campi, costanti, 3 costruttori di FractionCollection, verificati), 3 voci d'indice, riga errore `Size`/`size`
13:31 · FI2 · revisione errori: 1 nuovo (pattern FI2: costruttore che memorizza il parametro senza costruire la rappresentazione), 1 ricorrenza (trasversale 1, fisica vs logica)
