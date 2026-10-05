# Giornata 2026-10-05

<!-- Claude appende qui, una riga per fatto: HH:MM · CODICE · fatto.
     Marcatori: CHIUSO <cod> <mod> · RIPASSO <cod> <mod> ok|debole -->

11:31 · FI2 · guida-lab LAB05 generata (scheda); progetto importabile in esame_FI2/da_importare/LAB05_TicketSosta-051026.
12:21 · FI2 · LAB05: Ticket completa, TicketTest verde (guidato: ordine costruttore, NumberFormat, toStringDuration da lui; toString dalla slide 11, copiato su sua richiesta).
12:50 · FI2 · LAB05 parte 1: Parcometro completo (calcolaCosto in 4 passi scritto da lui, emettiTicket e toString suoi); 6 test verdi in Eclipse. Franchigia/minimo: confronto sulla durata totale invece che dopo la franchigia, corretto dopo tre segnalazioni (caso 90 min). Mezzanotte e getter `getInizioSosta`/`getFineSosta` rimandati.
13:30 · FI2 · confronto_LAB05.md scritto (8 punti); progetto copiato in svolti/LAB05_TicketSosta/.
14:30 · FI2 · /flusso creato (disegno a widget del flusso di una funzione, con esempio numerico), su richiesta di Lorenzo.
15:10 · FI2 · Lorenzo dichiara: classi, chiamate e tipi assimilati, ma i «processi logici» dentro le funzioni (l'algoritmo richiesto dal docente) non li comprende bene; quando Claude li spiega gli sembra «un posto che non conosco». LAB05 resta 🔶 (parte 2 non fatta); verifica a voce saltata.
15:15 · FI2 · prontuario: §3.13 (java.time, formattatori, franchigia+minimo, costruttore vs parametri), 2 righe in §1.1, 1 in §1.3, 5 nell'indice.
15:05 · FI2 · revisione errori: 3 nuovi (sezione FI2), 2 ricorrenze (pattern 1 e 2); 2 candidati trasversali non promossi.
16:00 · FI2 · LAB05 parte 2: `TicketEvoluto` scritto da lui (formato data leggibile da solo); `ParcometroEvoluto`: ciclo sui giorni, tariffa per giorno (`getValue() - 1` derivato da lui), franchigia sul primo pezzo, `toString`. Inciampi: `da.plusDays(1);` senza assegnare (immutabilità, ciclo infinito), tariffa letta da `da` invece che dal giorno che avanza, `+ 1` rimasto nella condizione, `tariffa.toString()` su un array; un quick fix di Eclipse ha cambiato `Ticket` della parte 1. Blocco del minimo nel ramo «stesso giorno» scritto da Claude (guidato).
17:10 · FI2 · LAB05 8/8 + 6/6 + 1 + 1 test verdi in Eclipse; progetto copiato in svolti/LAB05_TicketSosta/; confronto_LAB05.md parte 2 (punti 9–16, minimo sull'intera sosta, franchigia a cavallo di mezzanotte debolezza comune). CHIUSO FI2 LAB05
17:15 · FI2 · prontuario: §3.13 «Parte 2» (giorno della settimana → indice, immutabilità di `plusDays`, ciclo sui giorni, franchigia+minimo su un giorno, `toString` su array, quick fix Eclipse), 4 righe nell'indice.
17:16 · FI2 · revisione errori (parte 2): 5 righe aggiunte (pattern 1, 2; sezione FI2), nessun candidato trasversale nuovo.
17:26 · FI2 · Lorenzo fissa gli obiettivi della prossima sessione: testare il proprio codice, debuggare con stampe ad hoc, costruire insieme una procedura/workflow d'esame.
