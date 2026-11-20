# Giornata 2026-11-20

<!-- Claude appende qui, una riga per fatto: HH:MM · CODICE · fatto.
     Marcatori: CHIUSO <cod> <mod> · RIPASSO <cod> <mod> ok|debole -->

12:00 · PIANO · /pianifica giorno: §4d (resto) + drill P2–P3 2022-12-23, handler dal testo 2023-02-09, FI2 LAB09 avvio; /chiudi 17:30
12:02 · CALC · §4d domanda 4 (salto se zero): BEQZ R21,ALTRO giusto da solo (il 16/11 non lo ricordava)
12:03 · CALC · §4d domanda 5 (store di un byte con base+offset): SB R21,0x0008(R20) giusto da solo, verso della store e offset corretti
12:06 · CALC · §4d domanda 6 (costante a 32 bit): LHI R22,0xF000 + ORI R22,R22,0x0004 giusto da solo. Vocabolario §4d: 6/6 domande fatte (3 il 18/11 con errori, 3 oggi giuste)
12:07 · CALC · inizio drill P1–P3 a freddo sulla 2022-12-23 (EPROM e RAM da 1536 MB, in basso e in alto)
12:15 · CALC · 2022-12-23 P1: EPROM 1 GB + 512 MB (00000000–3FFFFFFF, 40000000–5FFFFFFF) giusta da solo
12:20 · CALC · 2022-12-23 P1: RAM in alto (C0000000–FFFFFFFF, A0000000–BFFFFFFF) giusta da solo; aveva chiesto se la RAM fosse 1536 MB (il testo dice «stessa quantità»). P1 a freddo e senza errori: è la seconda prova di fila
12:22 · CALC · P2: Lorenzo non ricorda come si ricava la firma («cosa devo confrontare»): rispiegato con il confronto in binario fra primo e ultimo indirizzo del blocco (bit uguali = firma) e con il conteggio 2^n
12:30 · CALC · 2022-12-23 P2 firme complete: 3/4 giuste; EPROM 512 senza BA29* (fermato a 2 bit su 0100/0101, «si ferma al primo indizio»); C scritto 1101 (svista, ininfluente). Regola data: stessa taglia → stesso numero di bit di firma
12:39 · CALC · 2022-12-23 P2 firma minima: proposto di togliere BA29 a EPROM 512 e RAM 512; giusto per la RAM (come la soluzione), sbagliato per la EPROM (le porte stanno a 60000000h). Regola data: prima si piazzano le porte (P4), poi si semplifica nelle zone vuote davvero
12:41 · CALC · P3: Lorenzo non ha capito la consegna «quattro lati di un banco»: rispiegato da zero (4 chip da 8 bit per un bus a 32, CS/indirizzi/dati/OE-WE) con il banco 0 della RAM 512 della 2022-12-23 fatto per esempio; a lui il banco 3
12:43 · CALC · P3 ridimensionato: la soluzione 2022-12-23 riporta per le memorie solo range, banchi (n × taglia) e CS·BEi, nessun piedino/BD/OE-WE; collegamenti disegnati solo per le porte. Da correggere nel prontuario P3 (minimo d'esame vs completamento)
