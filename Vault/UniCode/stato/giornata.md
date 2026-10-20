# Giornata 2026-10-20

<!-- Claude appende qui, una riga per fatto: HH:MM · CODICE · fatto.
     Marcatori: CHIUSO <cod> <mod> · RIPASSO <cod> <mod> ok|debole -->

11:51 · CALC · sessione aperta su 02 (lezione, Decisione 1: scomposizione 1032 MB della prova 2023-12-21).
12:05 · CALC · 02: scomposizione di 1600 MB scritta 2^10+2^9+2^8 (=1792), terzo termine sbagliato e somma non verificata (pattern «far quadrare i numeri»).
12:07 · CALC · 02: non capito perché 2^30 in binario è 1 seguito da 30 zeri (scambiato per «2»): ripreso dalla base 10 (10^3 = 1000).
12:16 · CALC · 02: 2^30 = 40000000h ricavato da solo (padding 100→0100 ok); non capita la domanda «ultimo indirizzo del blocco» (fatica nota: muoversi nella memoria).
12:25 · CALC · 02: attribuito 3FFFFFFFh come fine del blocco da 512 MB (è la fine di quello da 1 GB): blocchi confusi, di nuovo «muoversi nella memoria».
12:31 · CALC · 02: 512 MB → esponente 9·3 = 27 (moltiplicato invece di sommare i 20 di M): 2^27 = 8000000h al posto di 2^29. Ricorre l'inciampo delle unità K/M.
12:40 · CALC · 02: blocco 512 MB chiuso da solo (20000000h, 60000000h, 5FFFFFFFh). 64 MB scritto 2^6 (persa di nuovo la M, +20) → fine A0000000h−1, blocco da 1 GB.
12:43 · CALC · 02: mappa EPROM della prova 2025-01-08 completata da Lorenzo (3 blocchi, inizio/taglia/fine), coincide con la soluzione ufficiale. Inciampi: unità M (2 volte), cifre perse (7 invece di 8).
13:02 · CALC · 02: RAM 2 GB presa come 2000 MB (decimale) e scomposta; metodo dall'alto (FFFFFFFF − taglia + 1) trovato da solo, ma chiamato «fine» invece di «inizio».
