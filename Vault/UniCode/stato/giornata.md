# Giornata 2026-11-10

<!-- Claude appende qui, una riga per fatto: HH:MM · CODICE · fatto.
     Marcatori: CHIUSO <cod> <mod> · RIPASSO <cod> <mod> ok|debole -->

12:12 · FI2 · LAB08 parte 2 avviata (lightwork): Queue sul laptop ancora in edlift.model con insert vuoto; MultiFloorLift stub
12:40 · FI2 · LAB08 Queue: costruttore senza new (bookings null) e new int[] scritto male — non chiaro come si inizializza un array nel costruttore, spiegato; insert giusta da lui (booked come indice, piena con booked == length)
14:51 · FI2 · LAB08 Queue: extract giusta (ciclo booked-1, booked--); «Queue cannot be resolved to a type» = riga package ancora edlift.model; 0/8 per peek su bookings[booked] (primo posto libero vs testa: pattern 1) e coda vuota senza MIN_VALUE
15:38 · FI2 · LAB08 Queue in edlift.model.util: QueueTest 8/8 verdi (lanciati da Lorenzo); peek/extract con hasItems e MIN_VALUE. 40/60, ora MultiFloorLift
16:17 · FI2 · LAB08 MultiFloorLift: non chiaro campo vs variabile locale (chiama «variabile locale» il campo bookings di Queue) e perché un campo oggetto va creato nel costruttore (pensava fosse perché private); confusione aggravata da Claude, che ha usato lo stesso nome bookings nelle due classi
19:17 · FI2 · LAB08 MultiFloorLift: pensava di chiamare hasPendingFloors dentro goToFloor (è la domanda che fa il Controller: si ridefinisce); non trovava il metodo di Queue per «ci sono elementi?» (hasItems, scritto da lui); pseudocodice giusto ma setRequestedFloor dimenticato nel ramo REST (11 failure «expected 3 but was 5»); Claude aveva detto per errore «lo stato non lo guardi», corretto sul test QuintaPrenotazioneRifiutata
19:45 · FI2 · LAB08 nextPendingFloor con peek invece di extract: non capito con la tabella dei metodi, capito con la fila dal salumiere e la traccia del test. getMode MULTI
20:40 · FI2 · LAB08 EDLift 60/60 verdi (Multi 20, Healthy 17, Basic 15, Queue 8; ricontrollati da Claude con javac + JUnit), guidato. CHIUSO FI2 LAB08
20:44 · FI2 · confronto_LAB08.md (10 punti) in svolti/LAB08_EDLift; trovato e verificato: REJECTED del salutista senza setMsg/setFloor restituisce il messaggio della coda piena (costante di enum condivisa)
20:44 · FI2 · prontuario: §3.16 (gerarchia astratta, metodi gancio, coda FIFO), 3 righe in §1.3, 5 voci nell'indice
20:46 · FI2 · revisione errori: 4 nuovi, 6 ricorrenze (pattern 1, 6, 7 trasversali; nessun candidato nuovo)
20:50 · PIANO · pianificato domani (11/11): 3 attività nella Plancia (checkpoint CALC slittato dal 10/11, handler CALC 03, avvio FI2 LAB09) e 7 blocchi in agenda
21:00 · PIANO · mer–ven Lorenzo lavora 8–14: 11/11 studio dalle 15 (checkpoint CALC, handler 03), LAB09 avvio spostato al 12/11, /lab CALC 03 resta il 13/11
