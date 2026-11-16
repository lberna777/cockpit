# Giornata 2026-11-16

<!-- Claude appende qui, una riga per fatto: HH:MM · CODICE · fatto.
     Marcatori: CHIUSO <cod> <mod> · RIPASSO <cod> <mod> ok|debole -->

11:40 · PIANO · pianificati settimana 16–22/11 e giorno 16/11: 8 attività riprogrammate e 5 blocchi nella Plancia
11:51 · CALC · checkpoint 2024-01-19: aiuto su EPROM 520 MB non potenza di 2 (va spezzata in blocchi), livello domanda
11:52 · CALC · checkpoint 2024-01-19: aiuto su 520 MB scritti come 2^31 (è la RAM da 2 GB), livello domanda
11:53 · CALC · checkpoint 2024-01-19: aiuto su 2^9 + 2^3 trattata come prodotto (esponenti sommati), livello domanda
12:02 · CALC · checkpoint 2024-01-19: aiuto su 2^23 in esadecimale a 8 cifre (800000h giusto, mancava il riempimento), livello domanda
12:03 · CALC · checkpoint 2024-01-19: aiuto su dimensione del blocco confusa con indirizzo di inizio (00800000h), livello domanda
12:13 · CALC · checkpoint 2024-01-19: aiuto su fine RAM (dove si applica il −1), livello domanda
12:14 · CALC · checkpoint 2024-01-19: aiuto su fine RAM = FFFFFFFFh coincide con inizio+dimensione−1, livello idea
12:22 · CALC · checkpoint 2024-01-19: aiuto su porta OUT mappata a 80000000h, dentro la RAM (stesso errore del 5/11), livello domanda
12:23 · CALC · checkpoint 2024-01-19: rettifica alla riga precedente, la OUT a 80000000h era un refuso (l'aveva a 50000000h); aiuto su IN0/IN1 a indirizzi lontani, che non si leggono a 16 bit con un solo accesso, livello domanda
12:24 · CALC · checkpoint 2024-01-19: la domanda sulle letture a 16 bit da IN0/IN1 era fuori perimetro (porte = moduli 04–05 non aperti); riportato sulla parte memorie, porte lasciate come mappate
12:27 · CALC · checkpoint 2024-01-19: chiesto ripasso della procedura per la tabella dei CS, livello domanda
12:29 · CALC · checkpoint 2024-01-19: firma EPROM 512 MB trovata da solo (BA31..BA29 a 0); domanda su banchi e BE, livello domanda
12:30 · CALC · checkpoint 2024-01-19: aiuto sul banco scelto dai BE e non dai BA (il DLX non porta fuori BA1..BA0), livello idea
12:30 · CALC · checkpoint 2024-01-19: dato il nome BE0..BE3 (Byte Enable), non lo ricordava, livello idea
12:33 · CALC · checkpoint 2024-01-19: firma EPROM 8 MB presa a 8 bit (BA31..BA24), manca BA23 fisso; aiuto livello domanda
12:37 · CALC · checkpoint 2024-01-19: confermata la notazione (asterisco = bit a 0, negato), livello idea
12:39 · CALC · checkpoint 2024-01-19: firma RAM cercata sulle cifre esadecimali invece che sui bit (8..F), livello domanda
12:44 · CALC · checkpoint 2024-01-19: piedini EPROM 128 MB dati come BA2..BA8 (contati 7 invece di 27), aiuto livello domanda
12:45 · CALC · checkpoint 2024-01-19: banco da 2 MB preso come 2^20 (dimenticato il 2 di 2 MB), aiuto livello domanda
12:46 · CALC · checkpoint 2024-01-19: piedini RAM giusti da solo; domanda neutra su collegamenti dei chip ancora mancanti (senza nominare RD/WR), livello domanda
12:47 · CALC · checkpoint 2024-01-19: non coglie la domanda sui collegamenti; riformulata su lettura/scrittura dei chip (parte del 02, già nella prova del 5/11), livello idea
12:48 · CALC · checkpoint 2024-01-19: RD/WR dei chip non ricordati (come il 5/11); data l'idea MEMRD/MEMWR, livello idea
12:49 · CALC · checkpoint 2024-01-19: non capisce la richiesta sui collegamenti RD/WR; riformulata con lo schema del chip (OE/WE), livello idea
12:50 · CALC · checkpoint 2024-01-19: OE/WE giusti dopo lo schema; domanda sul collegamento dei dati dei banchi al bus BD, livello domanda
12:53 · CALC · checkpoint 2024-01-19: BD dei banchi giusti per 0 e 1, sbagliati 2 e 3 (16..24, 25..31), aiuto livello domanda
