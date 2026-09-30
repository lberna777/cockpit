# Giornata 2026-09-30

<!-- Claude appende qui, una riga per fatto: HH:MM · CODICE · fatto.
     Marcatori: CHIUSO <cod> <mod> · RIPASSO <cod> <mod> ok|debole -->

12:52 · FI2 · metodo cambiato: niente più /lezione per FI2, si lavora sui LAB con i test (teoria solo quando serve); prontuario riorganizzato per parte del compito; creato corsi/FI2/esame_FI2/ (kit d'esame)
13:05 · FI2 · guida-lab LAB02 generata (scheda di una pagina, template startkit).
15:46 · FI2 · LAB02: FrazioneTest verde (-ea), ma new Frazione(0, d) dà 0/0 — il costruttore copre solo prodotto >0 e <0, il caso =0 lascia i campi a 0; i test non lo coprono (pattern 2: test verde ≠ classe corretta).
15:53 · FI2 · LAB02: costruttore corretto (i >= 0), Frazione completa — FrazioneTest verde e casi con lo zero verificati (0/-5 → 0/5, minTerm 0/5 → 0/1). Restano mcm e rename del progetto.
15:59 · FI2 · LAB02: mcm scritto come a*b - mcd (sottrazione invece di divisione: «togliere un fattore» letto come togliere un addendo); FrazioneTest resta verde perché nessun test usa mcm.
16:00 · FI2 · LAB02 svolto in modalità guidata: tutti i test verdi, mcm corretto, progetto rinominato (LAB02_Frazione-300926); copiato in esame_FI2/svolti/LAB02_Frazione/. Resta il confronto con la soluzione del docente.
16:03 · FI2 · LAB02: confronto con la soluzione del docente scritto (svolti/LAB02_Frazione/confronto_LAB02.md); da ora il confronto è un passo fisso dopo i test verdi (lab.md, CLAUDE.md §8, README kit).
16:09 · FI2 · Lorenzo, dal confronto LAB02: «scrivo ancora come in C», il docente è più efficiente. Precisato: le differenze sono ridondanze (boolean restituito con if, campo ripetuto nei rami, abs su un invariante), non idiomi Java; criterio «questo lo so già?», chiarezza prima della brevità. Da cercare nei prossimi confronti.
16:11 · FI2 · /chiudi: Lorenzo giudica tutto abbastanza chiaro, nessun intoppo nuovo con Eclipse. Decisione di Lorenzo: un LAB con i test verdi è chiuso anche se svolto con guida — si annota «guidato» come inventario per la preparazione all'esame. CHIUSO FI2 LAB02
16:11 · FI2 · 04b e 06 → 🔶: entrati in LAB02 per le parti usate (costruttori primario/ausiliario, this(...), toString con @Override); si completano con i LAB che li riusano.
16:11 · FI2 · tracker: rimossa la riga spuria «02 | e» (marcatore «CHIUSO FI2 02 e 02x» del 26/09 letto come modulo «e»); restano FI2 02 e FI2 02x.
16:15 · FI2 · revisione errori: 4 nuovi (FI2: rami senza caso 0, stampa in equals, mcd→1 per lo zero, ridondanze), 2 ricorrenze del pattern trasversale 2 (console vuota presa per corretta; mcm non verificato sugli esempi).
16:15 · FI2 · prontuario: §1 (X rosse «cannot be resolved to a type», «must return a result», AssertionError, / by zero in mcd, silenziosi: -ea mancante, campi a 0, test verdi ma mcm sbagliato), §2 procedura startkit completa (import/Finish, rename e conflitto con la cartella, -ea, collaudo metodo per metodo), §3.8 classe-valore immutabile nella forma del docente + mcm; indice aggiornato. Messaggi verificati con javac ed ecj 3.46.
16:29 · FI2 · guida-lab LAB03 generata (scheda di una pagina; si parte dallo startkit con la Frazione del docente).
17:26 · FI2 · LAB03: scritti sum, sumWithMcm, sub, mul, div, reciprocal; mancano compareTo e getDouble. sumWithMcm e sub con den/mcm invece di mcm/den (verso invertito, pattern 5); sub fa anche f − this invece di this − f. Il test di sub passerebbe per caso (1/4 − 1/8: 1 − 0 = 1 → 1/8).
17:42 · FI2 · LAB03: UnsupportedClassVersionError (class file 69 = Java 25, JRE 65 = Java 21). Causa: lo startkit non ha jdt.core.prefs, quindi prende la compliance di default del workspace (25) ma gira sul JRE 21; LAB02 aveva la compliance 21 a livello di progetto. Rimedio: compliance 21 nelle preferenze del workspace. Da mettere nel prontuario §1.
17:48 · FI2 · LAB03: Lorenzo stanco, chiede le correzioni spiegate — date in chat per sumWithMcm (den/mcm → mcm/den), sub (stesso errore + ordine this − f) e getDouble (divisione intera, cast prima della divisione). Voce da annotare come «guidato».
17:57 · FI2 · LAB03 svolto in modalità guidata: FrazioneTest verde, casi extra verdi (compareTo 1/-1, 1/2 − 1/3); copiato in esame_FI2/svolti/LAB03_Frazione/, confronto_LAB03.md scritto (div → riuso di mul, compareTo in croce fra int). CHIUSO FI2 LAB03
