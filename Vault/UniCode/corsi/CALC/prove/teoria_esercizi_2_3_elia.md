# CALC — esercizi 2 e 3 (sbarramento teorico), prove 2020–2022

> Fonte: sito Notion di S. Elia (studente, 2023), vedi `fonti.md` rango 2c. Risposte di uno studente, non del docente: da verificare sulla dispensa. Scaricato il 2026-11-20.

```
(page) Soluzioni domande teoria 
  (header) CALCOLATORI ELETTRONICI
  (header) 2020-07-14
    (sub_header) Esercizio 2
      (callout) Determinare il numero di stalli che	 si verificano con la seguente	 sequenza di istruzioni con processore DLX pipelined studiato a lezione in	due casi:
        (numbered_list) Senza forwarding unit
        (numbered_list) Con forwarding unit
        (text) ADD  R1, R4,R5    
LHI   R5, 8000h    
SB    R4, 100h(R5) 
SB    R4, 200h(R1)
      (text) Gli stalli si trovano tra la seconda e la terza istruzione e tra la prima e la quarta, nel primo caso una delle due istruzioni si trova in MEM l’altra in EX, nel secondo la prima si trova in WB e l’altra in ID.
      (numbered_list) Senza forwarding unit 
        (code) 1 - IF   ID    EX    MEM     WB
2 -      IF    ID    EX      MEM     WB
3 -            IF    stallo  stallo  stallo  EX    MEM   WB
4 -                  stallo  stallo  stallo  IF    ID    EX    MEM     WB
        (text) (Nota bene: lo stallo tra la prima e la quarta istruzione viene “risolto” già stallando la terza istruzione)
      (numbered_list) Con forwarding unit
        (text) Non ci sono problemi di stallo (la forwarding è in grado di risolvere tutte le alee di dato ad eccezione di quella causata dalla LOAD)
    (sub_header) Esercizio 3
      (callout) In cosa consiste il delayed branch? Perché potrebbe non essere la scelta ottimale nella progettazione di una CPU?
      (text) La delayed branch è un metodo di risoluzione delle alee di controllo che consiste nell’anticipare l’istruzione di salto condizionato perchè sono necessari tre cicli di clock per definire se il salto è effettivamente taken o no. 
Se, quindi, ci sono istruzioni dalle quali non dipende la branch vengono posticipate per limitare al massimo gli stalli. 
      (text) Gli aspetti negativi di questa pratica sono essenzialmente 2:
      (bulleted_list) Non è è compatibile con soluzioni hardware, che potrebbero essere più efficienti.
      (bulleted_list)  Soprattutto se la pipeline è lunga, potrebbe non essere possibile individuare un numero sufficiente di istruzioni da posticipare, è dunque necessario utilizzare un numero di NOP elevato.
  (header) 2020-09-01
    (sub_header) Esercizio 2
      (callout) 1. Quali problemi risolve la tecnica del cycle-split?
2. In cosa consiste e quali problemi comporta?
3. E’ necessario utilizzarla necessariamente o esistono alternative (e	quali)?
      (text) La tecnica del cycle split risolve le alee di dato che si vengono a formare quando l’istruzione in ID utilizza un registro modificato dall’istruzione in WB. La tecnica consiste nel dividere in due in ciclo di clock ed eseguire nella prima metà l’operazione di write-back e nella seconda l’estrazione del registro appena modificato dal register file. La controindicazione principale è che questo prevede un allungamento dei cicli di clock e quindi aumentare il tempo di esecuzione di tutta la pipeline. Una valida alternativa potrebbe essere l’utilizzo di un MUX all’uscita del register file comandato dalla forwarding unit.
    (sub_header) Esercizio 3
      (callout) Quali sono i vantaggi derivanti dalla particolare codifica delle istruzioni	nel DLX?
      (text) La struttura generale dell’istruzioni del DLX è molto vantaggiosa perchè contiene le stesse cose codificate sempre nello stesso posto: i primi 6 bit sono sempre op-code, i successivi 5 sono individuano un registro (se necessario) ecc… Questo consente alla pipeline di scomporre a priori e tradurre l’istruzione in maniera molto rapida.
  (header) 2021-01-13
    (sub_header) Esercizio 2
      (callout) Con	 riferimento al forwarding: spiegare qual è la specifica	 funzione del multiplexer	collocato	prima della barriera	ID/EX.
      (text) Il multiplexer permette di utilizzare dei dati non ancora scritti nel register file prima delle istruzioni di execute. Una possibile alternativa sarebbe lo split-cycle. 
Senza il multiplexer la pipeline sarebbe costretta a stallare perchè sarebbe impossibile prelevare i valori corretti.
    (sub_header) Esercizio 3
      (callout) Indicare chiaramente quali sono le	 controindicazioni nell’utilizzo della tecnica del delayed branch.
      (text) La delayed branch è una pratica software che non è compatibile con delle modifiche hardware. Per quanto sia utile ha diverse controindicazioni: la pratica consiste nell’anticipare l’istruzione di salto condizionato per permettere al DLX di eseguire altre istruzioni nel frattempo, tuttavia, spesso con pipeline lunghe, il compilatore potrebbe non trovare un numero sufficiente di istruzioni utili e di conseguenza utilizzare dei NOP a priori. Rispetto a questa eventualità è quindi preferibile usare una strategia più efficiente (come ad esempio la dynamic prediction). 
  (header) 2021-01-28
    (sub_header) Esercizio 2
      (callout) Il codice seguente è corretto? Motivare	chiaramente	la risposta.
ADDI	R7,R0,4321h  
SUBI	R8,R0,0001h  
LHU	R9,R7(1022h) 
AND	R10,R9,R8   
      (text) Il codice non è corretto per il seguente motivo: nella prima istruzione viene assegnato a R7 il valore esadecimale 0000 4321h, ma, nella terza istruzione, viene compiuta una half-word load da R7 con offset 1022h questo implica che l’indirizzo effettivo di lettura è 0000 5343h, ovvero un’indirizzo dispari mentre le HW possono essere lette/scritte solo da indirizzi pari. 
    (sub_header) Esercizio 3
      (callout) In  una  CPU pipelined: come sono eliminate le istruzioni erroneamente inserite nella pipeline di elaborazione nel caso la predizione di un salto risulti errata?
      (text) Le istruzioni vengono semplicemente trasformate in NOP in modo da essere rese innocue per il corretto funzionamento della CPU pipeline.
  (header) 2021-02-10
    (sub_header) Esercizio 2
      (callout) 
      (text) Il delayed load è una procedura completata via SW durante la fase di compilazione che serve per “distanziare” le istruzioni di Load dalle istruzioni che utilizzano i registri appena caricati, tra le motivazioni per il suo utilizzo vi è sicuramente il fatto che essa viene applicata prima dell’avvio del programma e quindi non comporta ritardi né effettivi svantaggi. 
      (text) Tuttavia se il processore lavora con pipeline lunghe la procedura di delayed load potrebbe non trovare un numero di istruzioni sufficienti per riempire i gap che si formano, e di conseguenza tali spazi vengono colmati con istruzioni NOP , rallentando in parte l’esecuzione del codice. 
      (callout) 
        (text) Indicare, chiaramente e sinteticamente, quali sono le motivazioni per utilizzare il delayed load.
Esistono controindicazioni nell’utilizzo di tale strategia?
    (sub_header) Esercizio 3
      (callout) Quali  sono  i  vantaggi nell’utilizzo del protocollo di handshake rispetto a non utilizzarlo. Rispondere in modo sintetico motivando chiaramente la risposta.
      (text) Il protocollo di handshake permette di scambiare dati con una periferica esterna in maniera molto più sicura: senza questo la CPU e la periferica di input/output non avrebbero modo di comunicare tra loro, rischiando di scrivere o leggere più volte la stessa cosa, di non scrivere o non leggere dei dati, oppure di scrivere o leggere dati che stanno cambiando in quell’istante, dando origine a errori. Il protocollo di handshake serve quindi a mettere in comunicazione le due piattaforme per indicare se un azione è già stata compiuta oppure no.
  (header) 2021-06-16
    (sub_header) Esercizio 2
      (callout) Sostituire	alla label DEST, il valore esadecimale corrispondente:
4000 1000h DEST:   ADD R1,R0,R7  
... ...                           
... ...                           
 4000 2000h          JAL DEST         
      (text) La differenza in valore assoluto tra i due valori è 1004h. Deve essere considerata al negativo con un immediato di 26 bit:
      (text) 1004h = 00 0000 0000 0001 0000 0000 0100
      (text) metto in negativo con il complemento a 2:
      (text) 11 1111 1111 1110 1111 1111 1100 = 3FFEFFCh
      (text) In conclusione il valore di DESTè 3FFEFFCh.
    (sub_header) Esercizio 3
      (callout) È possibile eseguire una	JAL	all’interno di codice chiamato	da un'altra JAL?
        (numbered_list) Si o no?
        (numbered_list) In caso di	risposta affermativa, come? In caso contrario, perché?
      (text) è possibile ma bisogna prestare la massima attenzione: Entrambe le JAL salvano l’indirizzo di ritorni in R31, se vengono innestate questo viene sovrascritto e viene persa la possibilità di tornare al codice iniziale. Quindi R31 deve essere salvato prima o in un altro registro (che ovviamente non deve essere utilizzato nella JAL innestata) oppure direttamente in una cella di memoria, e al termine del secondo JAL deve essere ripristinato.
  (header) 2021-07-08
    (sub_header) Esercizio 2
      (callout) 
        (text) Sostituire	alla	label HERE, il valore esadecimale corrispondente:
        (text) 20001400h  HERE: LW R1, R18(0100h)
 20001404h        ADD R18, R1, R6
 20001408h        SUB R12, R1, R3
 2000140Ch        BNEQ R12, HERE
      (text) Guardando gli indirizzi è possibile notare che la prima e l’ultima riga differiscono di 0000 000Ch. Tenendo in considerazione che la Branch è PC+4 relativa la differenza in valore assoluto è 0010h . Il valore però deve essere negativo, eseguo il cambio di segno:
      (text) 0010h = 0000 0000 0001 0000 → 1111 1111 1111 0000 = FFF0h
      (text) In conclusione HERE = FFF0h.
    (sub_header) Esercizio 3
      (callout) Nel	DLX,	sarebbe possibile non generare BE0, BE1, BE2, BE3 e utilizzare in modo	equivalente unicamente	i segnali BA0 e BA1?
        (numbered_list) Si o no?
        (numbered_list) In caso di risposta affermativa, come? In caso contrario, perché?
      (text) Se facessimo solo letture o scritture di byte sarebbe possibile, ma il DLX ha 32 bit di BD e deve essere possibile leggere e scrivere 16 o 32 bit contemporaneamente. I BE possono essere attivi contemporanemente, mentre ciò non sarebbe possibile con i BA0 e BA1.
  (header) 2021-12-23
    (sub_header) Esercizio 2
      (callout) È possibile eseguire un’istruzione jump and link all’interno di un interrupt handler? Si o no?		
Motivare	chiaramente e	sinteticamente la risposta al punto precedente
      (text) Sì è possibile. La JAL però sovrascrive automaticamente il registro R31 che potrebbe essere già utilizzato dal main. Quindi è necessario salvare il registro e ripristinarlo alla fine dell’handler (come per tutti gli altri registri utilizzati nell’handler).
    (sub_header) Esercizio 3
      (callout) Nel DLX, sono presenti vincoli nell’accesso in memoria	a word? Si o No?
        (text) Motivare chiaramente e sinteticamente la risposta al punto precedente
      (text) Sì, le word devono essere allineate in memoria (il loro indirizzo deve terminare con 00), altrimenti sarebbero necessari due cicli di bus. Analogamente le HW non possono essere lette/salvate in indirizzi dispari.
  (header) 2022-01-17
    (sub_header) Esercizio 2
      (sub_sub_header) A
        (callout) Nella rete che	realizza il DLX, è possibile utilizzare un PC a 30 bit? Si o No?
        (text) Sì, le istruzioni hanno tutte dimensioni di 4byte, quindi il Fetch deve obbligatoriamente avvenire su gruppi di 32 bit allineati, di conseguenza ogni indirizzo del PC termina con 00 e quindi solo i primi 30 sono significativi.  
      (sub_sub_header) B
        (callout) Come è possibile eliminare la ALU nello stadio di	fetch del DLX pipelined?	
Fornire dettagli in merito alla risposta fornita nel punto precedente
        (text) 
    (sub_header) Esercizio 3
      (callout) A cosa serve il	segnale di READY in un processore come il DLX?
Spiegare come agisce tale segnale?
      (text) Spesso la CPU non agisce da sola, deve collaborare con altre parti del calcolatore, ad esempio la memoria: in particolare durante i cicli di bus prima che avvenga effettivamente uno scambio di dati è necessario che entrambi i dispositivi siano pronti. 
      (text) La memoria genera dunque un segnale READY che suggerisce al DLX quando è possibile effettivamente iniziare il DATA_IN o DATA_OUT.  
  (header) 2022-02-17
    (sub_header) Esercizio 2
      (callout) A cosa servono i registri A e B nel DLX sequenziale?
Motivare chiaramente la	risposta data al punto precedente.
      (text) Nella maggior parte delle istruzioni DLX vengono usati almeno due registri, nelle istruzioni di Load e Store, ad esempio, ma anche nelle istruzioni che implicano l’utilizzo di una ALU. I registri che vengono utilizzati vengono codificati sempre nello stesso posto all’interno del codice dell’istruzione (subito dopo i 6 bit di cod. operativo), il processore quindi, subito dopo aver fatto il Fetch, associa ad A e a B il contenuto dei registri identificati dai 5+5bit codificati nel codice in modo da averli immediatamente disponibili per essere utilizzati. I casi sono tre: 
      (bulleted_list) L’istruzione è un’istruzione di Jump →  entrambi i registri non vengono utilizzati
      (bulleted_list) L’istruzione prevede l’utilizzo di uno solo dei due registri  (es LHI)→ uno dei due non viene utilizzato 
      (bulleted_list) L’istruzione prevede l’utilizzo di entrambi i registri  (SB, LB, ADD, ADDI ,…)→ entrambi vengono utilizzati
      (text) I registri vengono poi ovviamente impiegati per lo scopo identificato dai 6bit di codice operativo.
      (text) L’operazione di “assegnare al buio”, cioè di copiare i registri ancora prima di sapere se effettivamente siano utilizzati, è praticamente gratuita sia in termini di costi che di energie, permette quindi di risparmiare tempo importante a un costo pressocché nullo. 
    (sub_header) Esercizio 3
      (callout) Esiste una differenza tra indirizzo logico e indirizzo fisico nel DLX?
Motivare chiaramente la risposta fornita al punto precedente.
      (text) Sì, il processore DLX lavora con un bus a 32 bit dunque è necessario poter leggere 4byte a ogni ciclo di bus. Per permettere ciò la memoria è partizionata in 4 blocchi, ognuno individuato dai 30 bit più significativi del Bus Address e da 4 BE con i quali si va a selezionare uno o più byte della memoria. 
      (text) Con ‘memoria logica’ si intende quindi l’insieme di byte numerati e “adiacenti” tra loro, mentre con ‘memoria fisica’ viene inteso il concetto di memoria per com’è nella realtà: i byte sono raggruppati a gruppi di 4 e sono raggiungibili contemporaneamente da un bus a 32 bit. 
  (header) 2022-06-15
    (sub_header) Esercizio 2
      (callout) A cosa serve il	registro MAR nel DLX?
        (text) Quali istruzioni modificano tale registro?
      (text) MAR sta per Memory Address Register e contiene gli indirizzo a cui vengono eseguiti i vari cicli di bus. Il registro viene quindi modificato ogni qual volta ci sia una lettura o una scrittura dalla memoria: durante il Fetch dell’istruzione (a volte è però possibile utilizzare direttamente il PC senza usare il MAR come intermediario), ma soprattutto quando vengono utilizzate istruzioni di Load e di Store.
    (sub_header) Esercizio 3
      (callout) Esistono istruzioni che modificano il contenuto del registro	PC nel DLX?
In caso affermativo, quali? In caso negativo, perché?
      (text) Il registro PC (Program Counter) viene costantemente modificato, ogni volta che viene letta un’istruzione infatti viene aumentato di 4. Tuttavia esistono istruzioni che permettono di modificarne il contenuto in maniera diversa dal solito: le istruzioni della famiglia Jump, Jump-And-Link e le varie istruzioni di Branch, permettono infatti di forzare la scrittura del PC per ottenere dei veri e proprio salti all’interno della memoria. ```
