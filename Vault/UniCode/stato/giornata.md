# Giornata 2026-10-09

<!-- Claude appende qui, una riga per fatto: HH:MM · CODICE · fatto.
     Marcatori: CHIUSO <cod> <mod> · RIPASSO <cod> <mod> ok|debole -->


12:11 · CALC · 02p §6: Lorenzo chiede perché 12K = 8K+2K+2K e non 8K+4K. Il testo (00 p. 68) non impone taglie, quindi aveva ragione; corretta la lezione, che diceva «dal più grande».
12:34 · CALC · 02p §6: Lorenzo non sa fare somme in hex; spiegata la regola del riporto a 16 su 2000h+0800h e 0800h+0800h. Candidata al cheatsheet conversioni.
12:44 · CALC · 02p §6: 16K → «2^4», persa di nuovo la K (giusto 2^14). Ricorrenza dell'inciampo dell'8/10 (32 KB, 64 MB): unità persa nella conversione a potenza di due.
13:05 · CALC · 02p §6: 2^14 scritto con l'1 in fondo («0000 0000 0000 001»); non sapeva perché 2^n = 1 seguito da n zeri (spiegato col parallelo 10^n). Chiesto anche il ruolo della «h» e perché 16K non si scompone (regola: un solo 1 in binario → un chip).
13:12 · CALC · 02p §6: 10000h − 4000h → «12000»: 16−4 = 12 scritto come due cifre invece di C; dimenticato che l'1 che presta diventa 0. Indirizzi dell'esercizio 10 ricavati tutti (RAM_1..3, EPROM C000h–FFFFh); segnali CS non ancora fatti.
13:15 · CALC · prontuario: §0 inciampi del 9/10 (K persa, 2^14 rovesciato, cifra C, quanti chip); cheatsheet §10e–g (lettere e prestito a 16, 2^n, numero di chip)
13:20 · PIANO · /chiudi mattutino in autonomia: 02p §6–7 resta oggi (pomeriggio); lezione 02 → 10/10; /lab CALC 02 → 12/10; FI2 LAB06 resta all'11/10
13:01 · CALC · revisione errori: 2 nuovi, 1 ricorrenza (unità persa); 1 candidato trasversale debole (2^14 rovesciato ↔ pattern 5)
15:14 · CALC · 02p §6: non capiva lo schema A15..A0 (cosa sono i fili e i loro valori); rispiegato da 1FFFh cifra per cifra. Poi da solo la regola «firma = bit uguali agli estremi», giustificata con l'allineamento.
15:14 · CALC · 02p §6: conversioni a 16 bit: 2000h scritto con 14 bit, 7 → 1001 (è 9). Corrette scrivendo a gruppi di 4 con i pesi 8-4-2-1; RAM_3 ed EPROM convertite giuste da solo.
15:14 · CALC · 02p §6: pausa risolta da Lorenzo: RAM_2/RAM_3 si distinguono solo su A11, ad A13 basta per RAM_1; da solo «un CS ha senso solo per confronto con gli altri chip» → CS_EPROM = A15. Spiegate repliche della decodifica semplificata (A14 ignorato).
15:20 · CALC · 02p §6 finita: Lorenzo sceglie di non fare la variante e la §7, dopo la §6 (CS ricavati e pausa risolta); variante 8K+4K e §7 non svolti; «Prova tu» fatto subito dopo (vedi sotto).
15:41 · CALC · 02p «Prova tu» 6/6 svolti da Lorenzo: regola dei multipli di 4 trovata da solo; K tenuta su 2K, 32 KB, 512 KB (manca «KB» scritto su 512); 3FFFFFFFh dopo guida sui 30 bit a 1; ricordato «piedini = esponente» solo dopo richiamo. CHIUSO CALC 02p
15:52 · CALC · giudizio di Lorenzo: sicuro su conversioni, firma e CS; fatica a «muoversi nella memoria» (dove finisce un blocco, cosa c'è a un indirizzo, ragionare per intervalli), evidente in Prova tu 4–5.
15:53 · CALC · prontuario: §0 «Dai range ai CS» (estremi in binario, firma, verifica piedini, CS per confronto, repliche) e inciampi del pomeriggio
15:53 · PIANO · domani 10/10: lezione CALC 02 Decisioni 1–3 partendo dai 1032 MB (confermato da Lorenzo); 11/10 FI2 LAB06 e 12/10 /lab CALC 02 invariati
15:54 · CALC · revisione errori (pomeriggio): 2 nuovi, 2 ricorrenze; candidati trasversali: confini di un intervallo (forte, con FI2 array/scarti di uno), meccanismo senza regola (debole)
16:09 · — · profilo/errori.md: promossi a trasversali, per decisione di Lorenzo, «6. Confini di un intervallo» (FI2 array + CALC memoria) e «7. Il meccanismo c'è, la regola o il nome no» (JRE + piedini); l'1 di 2^14 rovesciato NON è un'istanza del pattern 5.
