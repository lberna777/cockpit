# Giornata 2026-10-22

<!-- Claude appende qui, una riga per fatto: HH:MM · CODICE · fatto.
     Marcatori: CHIUSO <cod> <mod> · RIPASSO <cod> <mod> ok|debole -->

12:14 · FI2 · LAB06 ripreso su MasterMind (inizio alle 12:14, blocco delle 10:15 slittato).
12:38 · FI2 · LAB06 sorteggio: «0..5 + 1» giusto a parole, ma values().length creduto 6 (è 7) e nextInt(5) per «0..5» (nextInt esclude n) → pattern 6 ancora sugli estremi.
12:44 · FI2 · LAB06 sorteggiaCombinazione v2: values()[i] invece di values()[n] (indice del ciclo al posto del numero sorteggiato: escono sempre VUOTO,ROSSO,GIALLO,VERDE); this.segreta (campo) invece del parametro; Random creato a ogni giro.
13:02 · FI2 · LAB06 MasterMind: costruttore, combinazioneSegreta, sorteggiaCombinazione (testSorteggioIniziale verde ×5), occorrenze scritti da Lorenzo; calcolaRisposta impostata a passi, da scrivere dopo pranzo (ripresa: passo 1, conteggio dei neri).
15:01 · FI2 · LAB06 ripreso dopo pranzo su calcolaRisposta (passo 1: neri).
15:26 · FI2 · LAB06 calcolaRisposta v1 scritta da Lorenzo: neri giusti; ciclo dei minimi fino a tentativo.dim() (4) invece dei 7 colori; riempimento con condizioni su neri/bianchi che non cambiano (tutto NERO se neri>0). Lorenzo chiede di trovare il perché da solo → guida col passo 8 (stampe vs tabella a mano).
15:41 · FI2 · LAB06 calcolaRisposta: bug dei minimi trovato da Lorenzo con stampe vs tabella a mano (passo 8): ciclo sui colori limitato da tentativo.dim() → «sto scorrendo i vettori dei colori, non di una risposta». Posizioni e colori fusi (pattern 1); riempimento della risposta già corretto da solo.
15:51 · FI2 · LAB06 MasterMind chiuso: 34/34 verdi (verificati anche qui con javac), guidato; calcolaRisposta pensata da Lorenzo, bug dei minimi trovato da lui con le stampe. Copia in svolti/LAB06_MasterMind/, confronto_LAB06.md scritto (12 punti). CHIUSO FI2 LAB06
15:51 · SISTEMA · invio automatico dal laptop fermo da ieri sera: pull bloccato da log/2026-10.md modificato in locale (traccia di fine sessione del laptop). Sbloccato a mano; script resi tolleranti ai rami divisi; riga di log del laptop riportata qui. Causa da sistemare nella chat Infrastruttura.
15:53 · FI2 · handoff scritto: plans/handoffs/HANDOFF_FI2-LAB06_2026-10-22.md (sessione chiusa al 50% del contesto).
15:58 · PIANO · Lorenzo passa alla chat CALC per la lezione 02 (dal passo 8); /chiudi unico a fine giornata per FI2 e CALC.
16:01 · CALC · sessione aperta su 02 (passo 8 dell'artefatto: piedini, bus dati, interfacciamento; poi Decisione 3).
16:02 · SISTEMA · automatismi corretti (chat Infrastruttura): autosave cloud non committa più merge in conflitto né marcatori, pre-commit contro i marcatori, traccia di fine sessione del laptop committata, log del mese con merge=union.
16:17 · CALC · 02: piedini — «persissimo», non inquadra a quale parte della soluzione serve; ripreso dallo scopo pratico (schema di interfacciamento p. 9).
16:27 · CALC · 02: chiesto da Lorenzo uno schema fisico del sistema; aggiunto all'artefatto «Prova DLX 8 gennaio 2025» (chip, bus, decodifica, porte → dato del testo e riga della soluzione).
17:15 · CALC · 02: lo schema a blocchi non basta («voglio vedere i singoli piedini e fili»); aggiunte all'artefatto la tabella dati/incognite e la vista «filo per filo» (piedini DLX → AND/CS e A[..] dei 4 chip, indirizzo di prova interattivo).
17:19 · CALC · 02: piedini capiti con la vista filo per filo: EPROM 64 MB A[23..0] ← BA[25..2]; «ogni byte avanti cambio banco» detto da lui.
17:21 · CALC · 02: piedini EPROM 512 MB A[26..0] ← BA[28..2] da solo con i tre passi (esponente, piedini, fili).
17:23 · CALC · lezione 02 finita (Decisione 3 nella sostanza già fatta; RESET_P = comando → ·MEMWR, p. 47). Modulo 02 non ancora chiuso: /lab CALC 02 a freddo il 23/10, come in Plancia.
17:28 · CALC · artefatto: aggiunte «Mappa della memoria» (linea degli indirizzi cliccabile → blocchi divisi in banchi e righe, bit sui piedini) e «Su carta» (foglio in 4 riquadri: dati, linea, tabella della risposta, controlli); prontuario §0b.
17:37 · FI2 · giudizio di Lorenzo su LAB06: codice scritto quasi tutto da solo e bug trovato con le stampe, ma sintassi di classi e metodi non ancora a mente; si aspetta di seguire meglio il filo su un esercizio nuovo, con un po' di aiuto.
17:37 · CALC · giudizio di Lorenzo: sicurezza 1/5 a fare da solo la tabella della risposta; la fatica è «dove mi sto muovendo, cosa cerco, cosa so» e la comprensione fisica di ciò che controlla (→ artefatto: dati/incognite, foglio su carta, mappa, filo per filo).
17:37 · PIANO · 23/10 solo CALC: /lab CALC 02 a freddo sulla 2023-12-21 la mattina; altro solo se avanza tempo (decisione di Lorenzo).
17:38 · PIANO · 23/10 nella Plancia: lab CALC 02 a freddo 09:45–11:30, confronto 11:45–13:00, /chiudi 14:00; pianificazione.md: corretto il commento di «giorno:» sovrascritto da un sed del 20/10.
17:39 · FI2 · revisione errori: 1 nuovo (riempimento della Risposta su condizioni che non cambiano), 3 ricorrenze (trasv. 1 ×2 posizioni/colori, trasv. 6 values().length e nextInt, parametro/campo fusi). CALC: 0.
