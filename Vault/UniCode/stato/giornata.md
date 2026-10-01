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
