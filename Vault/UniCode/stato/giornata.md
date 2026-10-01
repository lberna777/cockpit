# Giornata 2026-10-01

<!-- Claude appende qui, una riga per fatto: HH:MM · CODICE · fatto.
     Marcatori: CHIUSO <cod> <mod> · RIPASSO <cod> <mod> ok|debole -->

13:06 · FI2 · LAB04a avviato da sessione cloud: startkit (solo FrazLibTest, package frazlib) reso progetto Eclipse importabile (compliance 21, launch con -ea); FrazLib da scrivere, Frazione da spostare nel package frazione (modulo 08).
14:28 · FI2 · guida-lab LAB04a generata (scheda di una pagina; ristrutturazione in package util/frazione/frazlib dal LAB03, poi FrazLib.sum/mul). Percorso verificato: codice LAB03 nei package + FrazLib del docente → FrazLibTest verde con -ea.
14:32 · FI2 · progetto LAB04a messo anche in esame_FI2/da_importare/ (l'import dello zip falliva sul laptop); da ora il lavoro del cloud va su master a ogni risposta.
15:01 · FI2 · LAB04a setup completato da Lorenzo: duplicato LAB03, package util/frazione creati e classi spostate (refactoring Move, «potential matches» accettati), FrazioneTest silenzioso con -ea verificato con assert false (configurazione del progetto duplicato). Prossimo: FrazLibTest in frazlib, poi FrazLib.
15:09 · FI2 · domanda di Lorenzo durante LAB04a: «cosa significa ADT?» — risposta da 04a sl. 29 e 04b sl. 35–38 (classe senza membri statici), collegata a LAB04 sl. 23 (ADT + libreria statica).
15:23 · FI2 · LAB04a: Lorenzo confuso sulla teoria — non coglie la differenza fra f[1].sumArray(...) (metodo d'istanza) e FrazLib.sum(...) statico, né cosa significhi static e quali «due mondi» convivano in Frazione (LAB04b). Spiegato col criterio «il metodo usa this?».
