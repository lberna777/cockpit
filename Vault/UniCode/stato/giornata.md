# Giornata 2026-11-05

<!-- Claude appende qui, una riga per fatto: HH:MM · CODICE · fatto.
     Marcatori: CHIUSO <cod> <mod> · RIPASSO <cod> <mod> ok|debole -->

10:45 · PIANO · pianificati mese settimana giorno: 15 attività nella Plancia
10:45 · CALC · checkpoint confermato al 10/11 (scelta a di Lorenzo): prova 2024-01-19 solo memorie + decisione su quanti esami in S1
10:47 · CALC · avviato /lab CALC 02 a freddo sulla prova 2023-01-17 (60 min)
10:59 · CALC · lab 02 a freddo: prima di proseguire chiesta e data la procedura in 10 passi (metodo del prontuario §0b/§1, senza valori); cronometro dalle 10:47
11:27 · CALC · lab 02 a freddo: bloccato all'ingresso del riquadro ③ («so cosa fare, non come e in che ordine»); dato ordine delle colonne e cosa chiede ciascuna, senza valori
11:52 · CALC · lab 02 a freddo sulla 2023-01-17 finito (~65 min): mappa, scomposizione, firme e CS delle memorie giusti da solo; CS EPROM 256 MB a 4 bit coerente con le sue porte
11:52 · CALC · errori di sostanza: OUTPUT_PORT messa a 80000000h dentro la RAM (CS identico a BA31, mutua esclusione violata, controllo ④ saltato); contate 3 porte in input invece di 4
11:52 · CALC · non fatti: banchi, piedini, RD/WR, righe ·BEi — Lorenzo: «non penso di essere in grado di svolgere questa parte in autonomia». Il 02 NON si chiude; ritenta al checkpoint del 10/11 (2024-01-19, parte memorie)
12:08 · CALC · guidato dopo la prova: banchi e piedini. Dopo l'esempio sull'EPROM 1 GB (A[27..0] ← BA[29..2]) ha ricavato da solo la regola «+2 per BA1–0» e le righe EPROM 256 MB (A[25..0] ← BA[27..2]) e RAM (A[28..0] ← BA[30..2]), giuste; capito anche come dividere una tacca (bit successivo) per la porta in più
12:13 · CALC · bus dati (banco i su BD[8i+7..8i], uguale per ogni blocco: chiesto e capito da lui) e RD/WR (EPROM solo MEMRD, RAM entrambi) fatti dopo spiegazione dal basso; tabella delle memorie della 2023-01-17 completa
12:14 · CALC · giudizio di Lorenzo sulla tabella delle memorie: sicurezza 3–4/5 (era 3/5 il 23/10, 1/5 il 22/10); «sulla prima metà sono ferrato». Pattern trasversale 2 (si ferma al primo indizio): controllo ④ saltato, porte contate 3 invece di 4
12:21 · FI2 · LAB07 ritocco 13: getAllAppointments restituisce una copia, scritta da Lorenzo (primo tentativo: alias «copia = allAppointments», corretto con new); 14/14 verdi
12:28 · FI2 · LAB07 ritocchi finiti: costruttore con durata ora chiama setDuration (scritto da Lorenzo, ordine giusto: from prima), via main e import Objects; 14/14 verdi. Domanda sua: perché i setter nel costruttore — capito: l'oggetto esiste già, il calcolo sta in un posto solo
14:48 · CALC · lezione 03 creata da 2 fonti (dispensa 03, soluzione 2023-01-17 consegna d); passo «Codice» e regola porte (g) aggiunti al prontuario §1
15:07 · CALC · lezione 03: non capito il quadro («DLX non era il processore? cosa stiamo guardando? devo imparare dal codice?»): manca il legame hardware ↔ programma; ripartito dal basso con l'analogia cucina/cuoco/ricetta
15:28 · CALC · lezione 03 §1: capiti registri (celle interne a 32 bit, dato o indirizzo), istruzione = nomi dei registri + immediato 16 bit, destinazione a sinistra (detto «o il contrario»: pattern 5). Frustrato quando ho fatto domande sul §2 non ancora letto: errore mio di ritmo, da qui niente domande in anticipo
15:37 · CALC · lezione 03 §2: indirizzamento indiretto capito con i numeri (R8 + 4 → 804h); confusione «LW copia un registro in un altro» corretta (R8 dà l'indirizzo, il dato viene dalla memoria); tabella load/store «indirizzo · azione · dato» aggiunta alla lezione
15:38 · CALC · lezione 03 §2: chiesto se LHI «fa quello che fa LB» — distinzione 1 trasversale (due «load» fuse); separate con il caso limite memoria spenta
15:45 · CALC · lezione 03 §2–3: fusi registro-indirizzo (R1) e registro-dato (R7) — pensava che LB «mettesse gli indirizzi bassi» in R1 e che l'estensione del segno riguardasse l'indirizzo; separati con la tabella riga per riga (pattern trasversale 1)
