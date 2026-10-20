# Giornata 2026-10-20

<!-- Claude appende qui, una riga per fatto: HH:MM · CODICE · fatto.
     Marcatori: CHIUSO <cod> <mod> · RIPASSO <cod> <mod> ok|debole -->

11:51 · CALC · sessione aperta su 02 (lezione, Decisione 1: scomposizione 1032 MB della prova 2023-12-21).
12:05 · CALC · 02: scomposizione di 1600 MB scritta 2^10+2^9+2^8 (=1792), terzo termine sbagliato e somma non verificata (pattern «far quadrare i numeri»).
12:07 · CALC · 02: non capito perché 2^30 in binario è 1 seguito da 30 zeri (scambiato per «2»): ripreso dalla base 10 (10^3 = 1000).
12:16 · CALC · 02: 2^30 = 40000000h ricavato da solo (padding 100→0100 ok); non capita la domanda «ultimo indirizzo del blocco» (fatica nota: muoversi nella memoria).
12:31 · CALC · 02: 512 MB → esponente 9·3 = 27 (moltiplicato invece di sommare i 20 di M): 2^27 = 8000000h al posto di 2^29. Ricorre l'inciampo delle unità K/M.
12:40 · CALC · 02: blocco 512 MB chiuso da solo (20000000h, 60000000h, 5FFFFFFFh). 64 MB scritto 2^6 (persa di nuovo la M, +20) → fine A0000000h−1, blocco da 1 GB.
12:43 · CALC · 02: mappa EPROM della prova 2025-01-08 completata da Lorenzo (3 blocchi, inizio/taglia/fine), coincide con la soluzione ufficiale. Inciampi: unità M (2 volte), cifre perse (7 invece di 8).
13:02 · CALC · 02: RAM 2 GB presa come 2000 MB (decimale) e scomposta; metodo dall'alto (FFFFFFFF − taglia + 1) trovato da solo, ma chiamato «fine» invece di «inizio».
13:14 · CALC · 02: chip-select non capiti con la tabella abbreviata (solo prime cifre hex): chiesto tutto esplicito a 32 bit.
13:17 · CALC · pausa di un'ora; /chiudi intermedio (stato, log, prontuario). Ripresa: firma EPROM 1 GB a 32 bit, poi EPROM 512 MB passo 1.
13:18 · CALC · prontuario §0: inciampi del 20/10 (fine blocco, blocco in alto, k·2^n, 8 cifre, unità M, 2 GB = 2048 MB).
13:18 · CALC · revisione errori: 1 nuovo (indirizzi a 7 cifre), 6 ricorrenze (trasv. 2, trasv. 6 ×2, unità, 2^n in binario, aritmetica hex).
15:06 · CALC · ripresa dopo la pausa: firma EPROM 1 GB a 32 bit riletta, «mi torna». Avanti con EPROM 512 MB passo 1.
15:09 · CALC · 02: firma EPROM 512 MB trovata da solo (BA31..BA29 = 010, 29 bit variabili = 2^29 verificato).
15:15 · CALC · 02: proposto da Lorenzo l'ordine «prima tutte le firme, poi tutti i CS» (adottato). Firma EPROM 64 MB = 011000 (BA31..26) trovata da solo.
15:18 · CALC · 02: firma RAM = BA31 = 1 trovata da solo. Tabella delle firme completa.
15:37 · CALC · 02: mapping della porta capito dopo 3 spiegazioni fallite (dimezzamento, caselle): sbloccato dalla sua regola «prendi un indirizzo comodo nel buco e confronta la sua firma con le altre».
15:43 · CALC · 02: CS_EPROM_512MB = BA31*·BA30·BA29* da solo, coincide con la soluzione ufficiale.
