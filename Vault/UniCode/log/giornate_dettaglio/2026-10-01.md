# Giornata 2026-10-01

<!-- Claude appende qui, una riga per fatto: HH:MM · CODICE · fatto.
     Marcatori: CHIUSO <cod> <mod> · RIPASSO <cod> <mod> ok|debole -->

13:06 · FI2 · LAB04a avviato da sessione cloud: startkit (solo FrazLibTest, package frazlib) reso progetto Eclipse importabile (compliance 21, launch con -ea); FrazLib da scrivere, Frazione da spostare nel package frazione (modulo 08).
14:28 · FI2 · guida-lab LAB04a generata (scheda di una pagina; ristrutturazione in package util/frazione/frazlib dal LAB03, poi FrazLib.sum/mul). Percorso verificato: codice LAB03 nei package + FrazLib del docente → FrazLibTest verde con -ea.
14:32 · FI2 · progetto LAB04a messo anche in esame_FI2/da_importare/ (l'import dello zip falliva sul laptop); da ora il lavoro del cloud va su master a ogni risposta.
15:01 · FI2 · LAB04a setup completato da Lorenzo: duplicato LAB03, package util/frazione creati e classi spostate (refactoring Move, «potential matches» accettati), FrazioneTest silenzioso con -ea verificato con assert false (configurazione del progetto duplicato). Prossimo: FrazLibTest in frazlib, poi FrazLib.
15:09 · FI2 · domanda di Lorenzo durante LAB04a: «cosa significa ADT?» — risposta da 04a sl. 29 e 04b sl. 35–38 (classe senza membri statici), collegata a LAB04 sl. 23 (ADT + libreria statica).
15:23 · FI2 · LAB04a: Lorenzo confuso sulla teoria — non coglie la differenza fra f[1].sumArray(...) (metodo d'istanza) e FrazLib.sum(...) statico, né cosa significhi static e quali «due mondi» convivano in Frazione (LAB04b). Spiegato col criterio «il metodo usa this?».
15:34 · FI2 · passaggio al locale. LAB04a: setup fatto (package util/frazione/frazlib, FrazioneTest verde con -ea), FrazLib ancora da scrivere. Aperte per Lorenzo: le 3 domande di verifica su this / f[1].sumArray(f) / MyMath.mcd static, poi le 3 domande d'impostazione di FrazLib (riuso di sum/mul, valore iniziale e array vuoto, for vs for each).
15:47 · FI2 · LAB04a in locale: Lorenzo dichiara chiara la distinzione metodo d'istanza / static, le 3 domande di verifica sono saltate. FrazLib.sum/mul create vuote; si passa a ragionare sugli array di oggetti (07 sl. 17–19), che non usa da tempo.
16:16 · FI2 · LAB04a: FrazLib.sum scritta corretta (parte da new Frazione(0), for each, riusa Frazione.sum). mul copiata da sum senza adattarla: parte da 0 e chiama sum. Lanciare FrazLibTest per vedere la failure.
16:25 · FI2 · LAB04a test verdi (FrazLibTest + FrazioneTest con -ea), guidato: mul corretta dopo due domande (neutro 1, .mul). Lorenzo: static/istanza e array chiari. Progetto in svolti/LAB04a_FrazioniBase/ con confronto_LAB04a.md (logica identica al docente). CHIUSO FI2 LAB04a
16:25 · FI2 · prontuario: §3.10 package/libreria static/array di oggetti, §1.1 «cannot be resolved» da import mancante e «static context», §1.2 NullPointerException su cella null, §2 duplicare un LAB, Move in package, import da cartella
16:31 · FI2 · revisione errori: 3 nuovi, 0 ricorrenze
16:36 · FI2 · guida-lab LAB04b generata (scheda + progetto importabile da_importare/LAB04b_FrazioniDoubleFace-011026 con la Frazione del LAB04a). LAB04b in corso.
16:47 · FI2 · LAB04b: importato lo zip grezzo invece del progetto preparato (reindirizzato). Credeva risolto 0/6 aggiungendo .minTerm() a FrazLib 04a: metodo sbagliato e minTerm lascia 0/36 (pattern 2, test non lanciato). Chiesto: dimensione logica vs length, ruolo di MyMain → spiegati sl. 28/30/32.
17:19 · FI2 · LAB04b: sum/mul/convertToString con ciclo i<fs.length-1 (salta l'ultima cella fisica, non si ferma ai null) e fs[fs.length] → AIOOBE; confusa fine fisica con fine logica. Chiesto cosa fa sum(setA,setB): spiegata la differenza fra le due sum statiche (overloading).
17:21 · FI2 · LAB04b: sum/mul/convertToString corretti sulla fine fisica (i<fs.length), manca ancora il controllo null (fine logica); convertToString stampa l'ultima cella fisica a parte → NPE/AIOOBE. Data la condizione della sl. 28 (gradino ③).
17:28 · FI2 · LAB04b: sum/mul con condizione sl. 28 verificati (array pieno, a metà, tutto null, length 0). convertToString: corpo con virgola-prima corretto, ma condizione ancora i<fs.length-1 (pattern: corregge il punto indicato e non quello adiacente).
17:30 · FI2 · LAB04b: convertToString corretta (pieno, a metà, tutto null, length 0). Passi 1–2 della scheda chiusi; prossimo size.
17:43 · FI2 · LAB04b test verdi (FrazioneTest -ea, exit 0; MyMain stampa i due array), guidato. size scritta da solo (for a corpo vuoto); sum/mul a coppie guidate su creazione array e return null; 0/6 risolto con sumWithMcm nella somma a coppie. 11 prove extra superate. Da fare: copia in svolti + confronto.
17:45 · FI2 · LAB04b CHIUSO (guidato): progetto in svolti/LAB04b_FrazioniDoubleFace/ con confronto_LAB04b.md (sum(Frazione[]) del docente va in NPE su array a metà, il suo no). CHIUSO FI2 LAB04b
17:54 · FI2 · giudizio LAB04b: static/istanza afferrato; tutto «chiaro ma non chiarissimo». Fatica nel ragionamento sugli array (null, dove finisce l'array logico) e nel trovare la forma «giusta» oltre che funzionante. Nessun problema Eclipse.
17:56 · FI2 · prontuario: §3.11 array a metà (fine fisica/logica, size, somma a coppie, convertToString, tre sum), §1.1 «not applicable for the arguments» e «is undefined», §1.2 NPE "fs[i]" e AIOOBE, §1.3 length-1 e 0/36; messaggi verificati con ecj
17:56 · FI2 · revisione errori: 4 nuovi, 2 ricorrenze
