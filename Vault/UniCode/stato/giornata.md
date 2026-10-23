# Giornata 2026-10-23

<!-- Claude appende qui, una riga per fatto: HH:MM · CODICE · fatto.
     Marcatori: CHIUSO <cod> <mod> · RIPASSO <cod> <mod> ok|debole -->

14:23 · CALC · guida-lab 02 generata (scheda compito: prova 2023-12-21, memorie, a freddo, 60 min). Lab avviato.
14:33 · CALC · lab 02 iniziato da Lorenzo con la scheda e l'artefatto della prova 8/01/2025 aperto (non a freddo: segnalato).
14:35 · CALC · decisione di Lorenzo: lab 02 sulla 2023-12-21 come esercizio guidato (artefatto 8/01 aperto); la chiusura del 02 si sposta a una prova a freddo (proposta: 2024-01-19, quella del checkpoint).
15:20 · CALC · lab 02: scomposizione 1032 = 2^30 + 2^23 e blocco 1 GB (00000000h–3FFFFFFFh) da solo; 2^23 = 800000h (ricordate le 8 cifre). Handoff al 50% del contesto: plans/handoffs/HANDOFF_CALC-lab02_2026-10-23.md.
15:26 · CALC · lab 02: dubbio di Lorenzo «il secondo blocco è da 16 MB»; ricontrollato sul testo: 1032 − 1024 = 8 MB (2^23, non 2^24).
15:31 · CALC · lab 02: blocco EPROM 8 MB 40000000h–407FFFFFh calcolato da solo ✓.
15:44 · CALC · lab 02: RAM 2 GB = 2^31 = 80000000h da solo; bloccato sul +1 in esadecimale (7FFFFFFFh + 1, riporto F+1=10).
15:47 · CALC · lab 02: RAM 80000000h–FFFFFFFFh da solo (+1 esadecimale fatto dopo la regola del riporto) ✓.
15:52 · CALC · lab 02: mappa completa da solo, buco 40800000h–7FFFFFFFh ✓. Si passa alle firme.
15:57 · CALC · lab 02: Lorenzo non ricorda come si ricava la firma di un blocco; ripresa con analogia decimale + esempio inventato da 256 MB (10000000h–1FFFFFFFh).
16:07 · CALC · lab 02: firma EPROM 1 GB (BA31=0, BA30=0) e bit di firma dell'8 MB (BA31..BA23) da solo dopo l'esempio ✓.
16:10 · CALC · lab 02: Lorenzo dichiara di non saper ricavare il VALORE dei bit di firma (sa trovare fin dove arriva): ripresa con conversione esadecimale→binario cifra per cifra e bit etichettati BA31..BA20.
