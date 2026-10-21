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
