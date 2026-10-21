# Giornata 2026-10-21

<!-- Claude appende qui, una riga per fatto: HH:MM · CODICE · fatto.
     Marcatori: CHIUSO <cod> <mod> · RIPASSO <cod> <mod> ok|debole -->

14:25 · FI2 · LAB06 ripreso: Lorenzo chiede il testo del problema prima della procedura (infarinatura sul dominio da sl. 2–6, 13).
14:38 · FI2 · procedura d'esame avviata in chat su Combinazione (passo 1: testo e test → contratto).
15:09 · FI2 · LAB06 passo 3: «array di dimensione dim-1» per il costruttore → taglia e ultimo indice fusi (pattern 6, confini). Prima: c presentata come «un array» invece che oggetto che contiene un array, equals «confronta i pioli» invece delle combinazioni (pattern 1).
15:33 · FI2 · LAB06 costruttore v1: parametro PioloDiGioco[] invece di int dim (probabile generazione di Eclipse), array mai creato, ciclo su campo this.dim mai assegnato (=0), celle a null invece di VUOTO, campi senza private. dim() giusto.
15:41 · FI2 · LAB06 Combinazione: costruttore, dim(), getPiolo → testInizialmenteVuota verde. Failure di getPiolo (String rgb invece di PioloDiGioco) diagnosticata da Lorenzo da solo.
15:44 · FI2 · LAB06 Combinazione: setPiolo scritto da solo, testOK1/testOK2 verdi; testEquals rosso (equals non ancora scritto: vale quello di Object).
15:49 · FI2 · LAB06 Combinazione: equals(Combinazione) scritto da solo (dim prima, poi ciclo con !=, return false al primo diverso); CombinazioneTest 6/6 verdi.
16:00 · FI2 · LAB06 Combinazione completa: null-check in equals aggiunto dopo il caso proprio (passo 5), toString con StringJoiner (prima stampava invece di restituire: corretto). Verificato qui: VUOTO×4, ROSSO,GIALLO,VERDE,BLU, equals(null)=false.
16:11 · FI2 · LAB06 Risposta scritta da solo con la procedura (tipi PioloRisposta, vittoria() a uscita anticipata come equals): RispostaTest 6/6 verdi.
16:30 · FI2 · LAB06 Gioco: Lorenzo perso sul contatore (non vedeva che serve un campo); chiede di fissare TUTTI i campi prima del costruttore → nota per la procedura: passo 2 = elenco campi dal contratto, presentato come tabella metodo → dato che serve.
16:32 · FI2 · procedura, regola di Lorenzo: ordine di lavoro = campi → costruttore → metodi che CAMBIANO lo stato (registraMossa) → metodi che lo leggono. Da scrivere nel prontuario §2 a /chiudi.
16:54 · FI2 · LAB06 Gioco: registraMossa corretta (status assegnato al campo); ultimoTentativo/ultimaRisposta su [numTentativi] invece di [numTentativi-1] → di nuovo pattern 6 (prima cella libera vs ultima piena), caso 0 mosse non gestito.
17:08 · FI2 · LAB06 situazione v1: StringBuilder giusto e formato della riga giusto, ma niente ciclo (una sola riga) e indice tentativiEffettuati = prima cella libera (null → NPE): stesso confine di ultimoTentativo; regola delle 3 tab assente.
17:23 · FI2 · LAB06 Gioco.toString: spazio prima dell'a capo e manca il prefisso «Gioco: »; in situazione numero riga ancora tentativiEffettuati()+1 invece di i+1 (verificato qui con javac: 2/3 dopo le prime due correzioni, 3/3 con la terza attesa).
17:26 · FI2 · LAB06 Gioco completo: GiocoTest 3/3 verdi. Restano MasterMind e MasterMindTest1–3. Classi fatte: Combinazione, Risposta, Gioco (15 test verdi su 34).
17:55 · FI2 · LAB06 MasterMind passo 2 a mano: sl. 31 (1N, tot 3, 2B) e 33 (1N, tot 4, 3B) giusti; algoritmo detto da Lorenzo in 4 passi (neri, occorrenze, minimi, totale−neri). Inizialmente «totale di bianchi − neri» → corretto in «totale piolini − neri» (pattern 1). Codice di MasterMind rimandato a domani (decisione di Lorenzo).
18:05 · FI2 · giudizio di Lorenzo: giornata positiva; funzioni complesse (situazione) lo hanno confuso sulla logica; utile capire prima la struttura della classe; all'esame la SEMANTICA c'è già, «in mezzo ci sono io che devo capirlo».
18:05 · FI2 · revisione errori: 5 nuovi (sezione FI2: firme dai campi, stato non salvato/stampa, formato a memoria, risposta a metà, processi interni), 2 ricorrenze (trasv. 1 e 6, una riga ciascuna). Nessun candidato trasversale nuovo.
18:05 · FI2 · prontuario: §2 procedura d'esame (UML+SEMANTICA, campi prima, ordine dei metodi, failure/error); §1 4 errori di compilazione, 2 eccezioni, 6 errori silenziosi (messaggi verificati con ecj 3.38 e JUnit 5); nuova §3.14 LAB06 + 9 righe nell'indice.
18:05 · PIANO · 22/10: FI2 MasterMind fino ai 34 verdi + confronto (mattina), CALC lezione 02 chiusura (pomeriggio); /lab CALC 02 → 23/10, lezione CALC 03 → 24/10. Oculista e tricologa senza data (Lorenzo li chiama in un giorno a casa).
