# Giornata 2026-11-06

<!-- Claude appende qui, una riga per fatto: HH:MM · CODICE · fatto.
     Marcatori: CHIUSO <cod> <mod> · RIPASSO <cod> <mod> ok|debole -->

12:05 · PIANO · /chiudi del 5/11 rimasto senza conferma su domani (Lorenzo uscito, fatto tardi la sera); il 6/11 si pianifica in una chat nuova di Studio
12:15 · PIANO · pianificati giorno: 2 attività nella Plancia (CALC 03 guidato, FI2 LAB08 avvio), 5 blocchi orari
14:28 · CALC · 03 sl. 46: R2 = 0x81 (dato da scrivere) classificato come indirizzo — confusione valore/indirizzo del 5/11 confermata
14:35 · CALC · 03 sl. 46: SH pensata come scrittura di tutto il registro (32 bit) invece che dei 16 bassi
14:52 · CALC · 03 sl. 46: SH a 0x7FF1 non allineata riconosciuta da solo, dopo aver chiarito banchi/righe/BE (bus a 32 bit = 4 banchi) e pari/dispari in esadecimale
15:02 · CALC · 03 sl. 46: LHU/LH su 0x0081 giuste; su 0x8081 LH scritta 0x11118081 (bit a 1 scritti come cifre esadecimali 1 invece di F) — binario e esadecimale mescolati
15:09 · CALC · 03: chiarito che i ???? sono 16 bit alti = 4 cifre esa da 4 bit ciascuna (1111 = F); regola nuova «domanda in pausa» nel profilo
15:19 · CALC · 03 sl. 47: ruoli in SW giusti da solo (R2 valore, R3 base); dubbio se l'offset 0800 diventa 00000800 o 08000000 (confusione con LHI)
15:24 · CALC · 03: chiaro sommatore indirizzi vs ADDI (la somma va sul bus, non in un registro); idea di Lorenzo: modello 3D interattivo CPU-bus-memoria, raccolta in corsi/CALC/appunti/modello_3d_raccolta.md
15:43 · CALC · 03 sl. 47 giro 2: R3+4 scritto E0000100 (somma esadecimale sbagliata: 4 messo nella cifra delle centinaia); SNEI letto su R3 invece di R2 — registri scambiati
15:45 · CALC · 03: origine di E0000100 = 4 scritto in binario (100) e letto come esadecimale; seconda volta oggi che mescola cifre binarie ed esadecimali (dopo 0x1111 per FFFF)
