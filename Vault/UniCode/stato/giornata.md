# Giornata 2026-11-10

<!-- Claude appende qui, una riga per fatto: HH:MM · CODICE · fatto.
     Marcatori: CHIUSO <cod> <mod> · RIPASSO <cod> <mod> ok|debole -->

12:12 · FI2 · LAB08 parte 2 avviata (lightwork): Queue sul laptop ancora in edlift.model con insert vuoto; MultiFloorLift stub
12:40 · FI2 · LAB08 Queue: costruttore senza new (bookings null) e new int[] scritto male — non chiaro come si inizializza un array nel costruttore, spiegato; insert giusta da lui (booked come indice, piena con booked == length)
14:51 · FI2 · LAB08 Queue: extract giusta (ciclo booked-1, booked--); «Queue cannot be resolved to a type» = riga package ancora edlift.model; 0/8 per peek su bookings[booked] (primo posto libero vs testa: pattern 1) e coda vuota senza MIN_VALUE
