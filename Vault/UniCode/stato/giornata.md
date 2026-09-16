# Giornata 2026-09-16

<!-- Claude appende qui, una riga per fatto: HH:MM · CODICE · fatto.
     Marcatori: CHIUSO <cod> <mod> · RIPASSO <cod> <mod> ok|debole -->

11:40 · FI2 · giudizio su 01 (sessione del 15/09): direzione del corso chiara; il versioning già usato con GitHub è agganciato all'esperienza e Lorenzo vuole approfondirlo; la scalabilità come criterio per dimensionare il problema è il concetto che ha retto meglio
11:40 · FI2 · non chiaro: la struttura formale di Java (com'è composto il linguaggio); giudicato da Lorenzo poco utile ai fini dell'esame, quindi non prioritario
11:40 · FI2 · decisione di metodo: le domande di verifica le pone Claude a voce dopo che Lorenzo ha letto gli appunti, invece dell'autoverifica scritta rifatta da solo
11:40 · FI2 · modulo 01 resta aperto: verifica rimandata alla prossima sessione (domande 2, 3, 4 + le due nuove su black-box/white-box e mvn package)
11:46 · FI2 · revisione errori: 2 nuovi (commit/push fusi → pattern trasversale 1; risposta data a metà della domanda), 1 ricorrenza; candidati trasversali segnalati non promossi
12:46 · FI2 · Lorenzo ha letto gli appunti definitivi di 01; parte la verifica a voce a libro chiuso (2, 3, 4 + black-box/white-box + mvn package)
12:50 · FI2 · verifica 01 d.2: failure/error classificati bene, niente più causa sintattica; ma error descritto come «interruzione del servizio» e parte «dove cerchi l'errore» non data (ricorre: risposta a metà domanda)
12:52 · FI2 · verifica 01 d.2 esito PARZIALE: Test Runner prosegue ✓, failure → logica/risultato ✓; error → «nella struttura» ✗ (è un'eccezione a run-time, l'asserzione non viene raggiunta: ricorda la confusione sintassi/esecuzione del 15/09)
12:53 · FI2 · verifica 01 d.3: risposta corretta nel verso (no, il software rispettava il progetto) — rovesciata rispetto al 15/09; manca ancora dove sta l'errore e quale sia il rimedio
12:54 · FI2 · verifica 01 d.3 esito BUONA: errore nel progetto (linee circolari non previste), rimedio progetto → codice → collaudo; da precisare solo l'etichetta del docente «dominio del problema mal analizzato»
13:01 · FI2 · verifica 01 d.4 esito BUONA: JAR si esegue, .java non si compila (mancano strumenti di sviluppo), due livelli JVM + JRE vero e proprio; da nominare JDK/javac e «unico strato dipendente dalla piattaforma» invece di «scaricato ad hoc»
13:05 · FI2 · verifica 01 d.black/white: black-box descritto come test singolo «fortunato», white-box come «guardare come lavora invece del risultato» ✗ — la differenza è da dove nasce il caso (specifica vs codice), non se si controlla il risultato; nessun caso white-box concreto dato (ricorre: risposta a metà)
13:06 · FI2 · verifica 01 d.black/white ripresa: caso white-box (4,4) sul confine del > dato correttamente dal codice ✓; esito complessivo PARZIALE → buona dopo la guida
13:07 · FI2 · verifica 01 d.mvn package saltata su richiesta di Lorenzo: Maven rimandato a quando servirà (il corso gli dedica una sola slide, sl. 17; all'esame si consegna un progetto Eclipse)
13:08 · FI2 · CHIUSO FI2 01 — verifica a voce a libro chiuso; punti deboli per il primo ripasso: error = eccezione a run-time, black/white = origine del caso (specifica vs codice)
13:14 · FI2 · lezione 02 creata da 1 fonti (02-x1-Linguaggi e piattaforme.pdf, 74 slide): lezione_02_linguaggi_piattaforme.md
15:46 · FI2 · decisione di piano: mappa teoria → pratica compilata in percorso.md dalle fonti (11 esercitazioni x/z, 14 LAB, 9 esercizi ES-*); prossima pratica di 02 = 02x, primo LAB obbligato = LAB02 (richiede 04b)
15:49 · FI2 · decisione di metodo: /lab ha un template dedicato «progetto a oggetti con startkit e test» (contratto + casi limite + suggerimenti a gradini, frammenti di codice solo da slide fino a LAB04, modalità compito per LAB12/13 e prove); CLAUDE.md §8 aggiornato
15:53 · — · pdf batch: 2 convertiti, 0 falliti.
