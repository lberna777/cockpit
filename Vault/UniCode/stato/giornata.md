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
16:34 · CALC · lab 02: firma EPROM 8 MB da solo dopo l'esempio passo per passo (BA30=1, gli altri 8 a 0), controllata su inizio e fine ✓.
16:39 · CALC · lab 02: firma RAM (BA31=1, CS_RAM = BA31) da solo ✓. Tutte le firme complete; si passa alla semplificazione.
16:43 · CALC · lab 02: semplificazione: 1 GB /BA31·/BA30 ✓; 8 MB a /BA31·BA30 ✗ (copre tutto il buco, non lascia posto alle porte); RAM scritta BA30 invece di BA31 (svista?).
16:44 · CALC · lab 02: decisione di Lorenzo: semplificare il CS dell'8 MB; porte da inserire come zona occupata nel buco. Spiegato il metodo «rimetti un bit → metà zona libera» su esempio inventato.
17:17 · CALC · lab 02: Lorenzo non ha capito il metodo «rimetti un bit»; si riparte dal suo ragionamento: prima si scelgono gli indirizzi delle porte nel buco, poi si semplifica il CS dell'8 MB.
17:19 · CALC · lab 02: porte scelte da Lorenzo nel buco: INPUT_0 a 50000000h, INPUT_1 a 60000000h ✓.
17:32 · CALC · lab 02: Lorenzo collega da solo CS semplificato → repliche nel buco → ritagliare gli indirizzi delle porte ✓ (concetto di semplificazione sbloccato).
17:34 · CALC · lab 02: confronto 4/5/6 in binario da solo: differenze su BA28 (INPUT_0) e BA29 (INPUT_1) ✓.
17:42 · CALC · lab 02: tutti i CS semplificati da solo, porte comprese (INPUT_1 semplificata a /BA31·BA30·BA29); zone disgiunte ✓. Si passa ai banchi.
17:45 · CALC · lab 02: banchi da solo (256 MB, 2 MB, 512 MB) ✓. Lorenzo ha chiesto un voto se l'esame fosse domani: risposto «non passeresti», circa un terzo dell'esercizio, guidato.
17:46 · CALC · lab 02: Lorenzo dichiara di non aver capito la regola CS banco = CS · BEi e BD[8i+7..8i]; ripresa con analogia dei 4 cassetti + esempio LB/LW.
17:49 · CALC · lab 02: CS per banco (CS blocco · BEi) capito dopo l'esempio del banco 0 ✓. Si passa ai piedini.
17:55 · CALC · lab 02: piedini banco 1 GB: 28 da solo, non sa quali BA arrivano (regola A[k-1..0] ← BA[k+1..2] non ricordata).
17:59 · CALC · lab 02: piedini EPROM 1 GB A[27..0] ← BA[29..2] da solo dopo l'esempio ✓.
18:00 · CALC · lab 02: piedini 8 MB scritti A[20..0] ← BA[21..2] ✗ (fili contati 20 per 21 piedini; atteso BA[22..2]): errore di ±1 sul limite alto.
18:01 · CALC · lab 02: piedini 8 MB corretti a BA[22..2] (Lorenzo: refuso) ✓.
18:03 · CALC · lab 02: piedini RAM A[28..0] ← BA[30..2] da solo ✓. Tabella memorie completa; si apre la soluzione per il confronto.
18:03 · CALC · lab 02 (prova 2023-12-21, memorie) svolto GUIDATO, non chiude il 02: confronto con la soluzione ufficiale senza errori di sostanza su range, banchi, CS, piedini, bus. Differenza: CS 8 MB con un bit in più (/BA28) perché INPUT_0 messa a 50000000h; la soluzione mette le due porte su un unico CS_INPUT a 60000000h (mutua esclusione via ACTIVE_0, moduli 04–05). Mancava RD/WR (EPROM MEMRD; RAM MEMRD+MEMWR).
18:07 · CALC · giudizio di Lorenzo: sicurezza 3/5 sulla tabella delle memorie (era 1/5 il 22/10); scelta degli spazi 5/5; piedini sa farli nell'esercizio ma non gli è chiaro cosa siano nel pratico e come funzionino, da rifare per assodarli. Modulo 02 resta aperto (lab guidato).
18:09 · CALC · prontuario §0: inciampi del 23/10 (+1 hex, valore dei bit di firma, prima le porte poi semplifichi, CS banco, piedini, RD/WR, porte allo stesso indirizzo).
18:10 · CALC · revisione errori: 3 nuovi, 5 ricorrenze (pattern 2, pattern 6 ×2, aritmetica hex, piedini); candidato trasversale: consegna incompleta (RD/WR), da decidere con Lorenzo.
