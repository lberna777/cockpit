
lancio di un eseguibile --> O.S. crea un **processo**, ma di cosa si tratta?

Un **processo** è una copia del programma con uno **spazio di memoria tutto suo** assegnato sulla **RAM**. il blocco che gli viene assegnato non è un blocco indistinto. ma è **diviso in segmenti** ciascuno con un suo ruolo. Su Linux:

**`.text`** — il **codice** del programma, cioè le istruzioni in linguaggio macchina. È in sola lettura (non si dovrebbe modificare il proprio stesso codice).

**`.data`** — le **variabili globali già inizializzate** (es. `char *bash = "/bin/bash";`).

**`.bss`** — le **variabili globali non inizializzate**.

**heap** — la memoria che il programma chiede _dinamicamente_ mentre gira (la `malloc` del C). Cresce **verso indirizzi più alti**.

**stack** — la memoria delle **funzioni**: le variabili locali e le informazioni per tornare indietro dopo una chiamata. Cresce **verso indirizzi più bassi** (su questo torniamo, è cruciale).

sulla VM si può visualizzare con:

	pmap <PID>

Ogni riga corrisponde a un segmento con il suo range di indirizzi

**IL CONCETTO DI STACK**

lo "Stack" è una pila di dati da cui posso fare solo **due operazioni**:

- **PUSH**: metto un nuovo elemento **in cima**
- **POP**: tolgo l'elemento che sta **in cima**

La pila si compone quindi seguendo il protocollo LIFO (**last in first out**) e viene usata dal **processore** per **gestire le chiamate a funzione**.
Quando una funzione viene chiamata, si **PUSHA** nello stack un blocco di informazioni; quando quella funzione finisce, quel blocco viene **POPPATO** dallo stack.

Due fatti che a prima vista sembrano contraddittori, ma che sono **il cuore di tutta la vulnerabilità**:

1. **Lo stack cresce verso il basso.** Cioè ogni nuovo PUSH usa un indirizzo _più piccolo_ del precedente. I dati "più vecchi" stanno in alto (indirizzi grandi), i "più nuovi" in basso (indirizzi piccoli).
2. **Un buffer, invece, si riempie verso l'alto.** Se dentro lo stack c'è un array `char buf[10]`, e lo riempi di caratteri, `buf[0]` sta in basso e `buf[9]` sta più in alto — cioè verso gli indirizzi _crescenti_, nella direzione dei dati più vecchi.

 **riempiendo un buffer oltre la sua dimensione, l'eccesso non va "fuori" a caso, ma sale verso i dati impilati prima — esattamente dove sta l'informazione che dice alla funzione dove tornare.** È questa la collisione che si sfrutta.

**I REGISTRI DEL PROCESSORE (architettura IA32)**

I **registri** sono piccole celle di memoria velocissime _dentro_ il processore (non nella RAM): il processore ci tiene i valori su cui sta lavorando in quell'istante. Il corso usa l'architettura **IA32** (Intel a 32 bit, cioè registri da 4 byte) perché è "non realistica ma comprensibile" (le idee valgono identiche sul 64 bit). I registri da conoscere:

- **`EAX`, `EBX`, `ECX`, `EDX`** — registri "general purpose", per calcoli vari. Per convenzione, `EAX` è anche dove una funzione lascia il proprio **valore di ritorno**.
- **`ESI`, `EDI`** — "source" e "destination", usati per copiare dati in memoria.
- **`EIP`** (_Instruction Pointer_) — **il registro più importante per noi**: contiene l'indirizzo della **prossima istruzione da eseguire**. Chi controlla `EIP` controlla il programma. _Tutto l'attacco serve a mettere in `EIP` un indirizzo scelto da noi._
- **`ESP`** (_Stack Pointer_) — punta alla **cima dello stack** (l'ultima cella occupata). `PUSH` lo decrementa di 4 e scrive; `POP` legge e lo incrementa di 4.
- **`EBP`** (_Base Pointer_) — punta alla **base dello stack frame della funzione corrente**: è il punto di riferimento fisso rispetto a cui la funzione trova le proprie variabili locali e i propri parametri (es. `[EBP-4]` è una variabile locale, `[EBP+8]` è un parametro).

**LO STACK FRAME E LA CONVENZIONE DI CHIAMATA**

Quando una funzione **chiama un'altra funzione**, sullo stack si costruisce uno **stack frame** (o **record di attivazione**) ovvero un blocco ordinato di dati, costruito seguendo quella che si chiama **convenzione di chiamata**. In C, di default, su processori 32bit, è **__cdecl**, e funziona così:

1. Il **chiamante** mette sullo stack i **parametri** della funzione, in ordine inverso (con dei `PUSH`).
2. 1. Il chiamante esegue l'istruzione **`CALL`**, che fa due cose: impila l'**indirizzo di ritorno** (l'indirizzo dell'istruzione a cui tornare quando la funzione finirà) e salta dentro la funzione.
3. 1. Il **chiamato**, appena entra, salva il vecchio `EBP` sullo stack (`PUSH EBP`) e imposta `EBP` sul valore attuale di `ESP`: così crea il proprio sistema di riferimento. Poi riserva spazio per le **variabili locali** (`SUB ESP, ...`).
4. 1. Quando finisce, ripristina `EBP` e `ESP`, e infine esegue **`RET`**: questa istruzione fa il **POP dell'indirizzo di ritorno dallo stack dentro `EIP`** — e quindi l'esecuzione riprende da dove il chiamante l'aveva lasciata.

**`RET` prende l'indirizzo di ritorno _dallo stack_ e lo carica in `EIP`.** L'indirizzo di ritorno è un _dato sullo stack_, vicino alle variabili locali e ai buffer. Se riusciamo a **sovrascrivere quel dato**, allora al `RET` il processore salterà **dove diciamo noi**, non dove il programma voleva tornare. Abbiamo dirottato l'esecuzione.

Ecco quindi la disposizione tipica di uno stack frame, dall'indirizzo alto (in cima) verso il basso:

```
  indirizzi ALTI
  ┌──────────────────────┐
  │ Parametri funzione    │
  ├──────────────────────┤
  │ Indirizzo di ritorno  │  ← se sovrascrivo QUESTO, controllo dove va il RET
  ├──────────────────────┤
  │ EBP salvato           │
  ├──────────────────────┤
  │ buffer / var. locali  │  ← l'input "scorretto" finisce qui e sborda VERSO L'ALTO
  └──────────────────────┘
  indirizzi BASSI  (← qui punta ESP)
```

**Little-endian vs. Big-endian**

Un ultimo tassello che servirà subito. Quando un numero da 4 byte (es. un indirizzo `0x0804D432`) viene memorizzato in RAM, l'ordine dei byte dipende dall'architettura:

- **big-endian** (processori Motorola): si parte dal byte **più significativo** → `08 04 D4 32`.
- **little-endian** (processori **Intel**, quindi il nostro caso): si parte dal byte **meno significativo** → `32 D4 04 08`.

Conseguenza pratica: quando nella stringa d'attacco devi inserire l'indirizzo `0x0804D432`, lo scrivi **byte invertiti**: `\x32\xD4\x04\x08`. Non è un vezzo, è come la CPU Intel rilegge quei 4 byte. Se li metti nell'ordine "naturale", salti all'indirizzo sbagliato.

Con questo, le fondamenta sono complete. Da qui in poi ogni concetto si appoggia su Parte 0.

## La visione d'insieme / threat model

Gli attacchi di questo modulo si chiamano **attacchi applicativi o binary exploit**, sfruttano vulnerabilità **del software** in esecuzione, non falle di rete, non falle nei protocolli. e mirano a **far eseguire a un processo operazioni per cui non era stato pensato**, con tre obbiettivi possibili:

- **fermarlo** → _Denial of Service_ (DoS): il processo va in crash;
- **dirottarne il flusso di esecuzione** → eseguire codice scelto dall'attaccante;
- **ottenere i privilegi di altri utenti** → se il programma vulnerabile gira come root (o ha il bit SUID), prenderne i privilegi.
- 
**Perché esistono ancora queste falle?** Perché la maggior parte del software di base è scritto in **C/C++**, linguaggi "vicini all'hardware" che **non controllano automaticamente** la lunghezza dei dati: il controllo è lasciato al programmatore, che spesso lo dimentica

**Prospettiva dell'attaccante:** cercare un input "non controllato e non validato" con cui scrivere su indirizzi di memoria arbitrari, e da lì arrivare a controllare `EIP`.

**Prospettiva del difensore:** il modulo non è solo offensivo. Buona metà del materiale sono le **contromisure** (canary, NX, ASLR, PIE/RelRO, CFI): capire _come_ ogni difesa rende più difficile l'attacco — e _come_ gli attaccanti la aggirano — è esattamente ciò che il quiz teorico chiede.

## Lo stack overflow: il meccanismo centrale

Tutto nasce da qui. Le **precondizioni** sono due, semplici:

1. esiste un **buffer locale a una funzione** (quindi sta sullo stack), di dimensione fissa;
2. quel buffer si può **riempire con input esterni** (tastiera, file, rete).

Il **gesto dell'attacco**: l'attaccante immette un input più lungo del buffer. In assenza di controlli, i byte in eccesso "sbordano" (è l'_overflow_) e — risalendo verso gli indirizzi alti

Questi byte vanno a sovrascrivere prima **l'EPB salvato** e poi **l'indirizzo di ritorno**. 

Quando avviene il **RET** (**POP dell'indirizzo di ritorno dallo stack dentro `EIP`**) il flusso non torna al chiamante legittimo ma all'indirizzo messo dall'attaccante

I due "rubinetti aperti" tipici, da riconoscere a colpo d'occhio nel codice:

- **`gets(buffer)`** — legge una riga da standard input **senza alcun limite** di lunghezza. È intrinsecamente insicura.
- **`strcpy(dest, src)`** — copia `src` in `dest` finché non trova il terminatore, **senza controllare** che `dest` sia grande abbastanza.

**In piccolo (il meccanismo):** considera `void function(){ char buffer[10]; gets(buffer); }`. Se immetti `"AAAAAAAAAABBBBCCCC"`, le 10 `A` riempiono `buffer[10]`, le 4 `B` coprono l'`EBP` salvato, e le 4 `C` finiscono **esattamente sopra l'indirizzo di ritorno**. Quei 4 byte sono ciò che il `RET` caricherà in `EIP`.

**In grande (la visione):** la stringa d'attacco ha quindi una struttura precisa a tre zone: **`[padding] + [riempimento dell'EBP] + [nuovo indirizzo di ritorno]`**. Il padding serve solo a "consumare" lo spazio fino all'indirizzo di ritorno; ciò che conta è l'ultima zona. Trovare _quanti_ byte di padding servono ("l'offset") è il lavoro pratico della guida-lab; capire _perché_ quella struttura funziona è ciò che ti serve sapere all'esame.

Cosa succede dopo dipende dall'indirizzo che ci metti:

- se punta a una **zona non accessibile** → crash con **segmentation fault** (è il DoS);
- se punta a **codice scelto** → controllo del flusso. Da qui partono le due grandi strade: **iniettare** codice nuovo (_shellcode_), oppure **riusare** codice già presente (_ret2libc_, _ROP_).

## I quattro gradini del lab (cosa illustra ciascun binario)

Il lab è costruito come una scala di quattro esercizi a difficoltà crescente. Non li svolgiamo qui (è materia di `/lab S4`): ti spiego **cosa dimostra ciascuno**, perché è la sequenza logica che lega tutta la teoria.

**1. `write_var` — sovrascrivere una variabile.** Il programma ha una variabile locale `control` e un `buf`; per stampare la flag, `control` deve valere `0x42434445`. Sovrascrivendo il buffer si arriva a **riscrivere il valore di `control`** (il gradino più semplice: scrivo su un dato vicino, senza ancora toccare il flusso). Qui impari due cose che torneranno sempre: che il valore va scritto rispettando il **little-endian** (la `control` giusta si ottiene mettendo `"EDCB"`, cioè `45 44 43 42` al contrario), e che la posizione esatta si trova **per tentativi** (anche con un mini-fuzzing: `for i in {100..150}; do ./es $(perl -e "print 'A'x$i"); done`).

**2. `secret_function` — saltare a una funzione esistente "nascosta".** C'è una funzione `secret()` che stampa la flag (o apre una shell) ma **non viene mai chiamata** dal programma. L'attacco sovrascrive l'indirizzo di ritorno con l'**indirizzo di `secret`**, trovato con `gdb` (`info functions`). È il primo, vero dirottamento di `EIP` verso codice già presente in `.text`. La variante `secret_function_remote` mostra lo stesso attacco quando il programma è **esposto in rete** (con `nc -l -p 8000 -e ./es`): l'input arriva via socket invece che da `argv` — è il ponte verso uno scenario realistico.

**`shellcode` — iniettare codice proprio.** Qui non c'è nessuna funzione comoda da richiamare: il codice da eseguire **lo porti tu**, dentro la stringa, sotto forma di _shellcode_ (vedi sotto). L'indirizzo di ritorno deve puntare **all'inizio del codice iniettato sullo stack**. È l'attacco "classico" completo, e nel lab lo si abbina al bit SUID-root per ottenere una **shell di root**.

**4. `returnlib` — riusare la libreria C (ret2libc).** Quando lo stack è reso non-eseguibile, non puoi più eseguire lo shellcode che inietti. La soluzione è non iniettare codice ma **saltare a una funzione che è già caricata**, in particolare `system("/bin/sh")` della libc. È la risposta diretta alla contromisura NX (vedi sotto).

> **La visione:** questi quattro binari _sono_ la mappa concettuale del modulo. Gradino 1: scrivo su un dato. Gradino 2: salto a codice che già esiste. Gradino 3: porto codice nuovo. Gradino 4: quando il gradino 3 è bloccato dalle difese, torno a riusare codice esistente — ma in modo più sofisticato. Tutta la seconda metà della lezione (contromisure e loro bypass) è la spiegazione di _perché_ si passa dal gradino 3 al gradino 4.

Gli strumenti non sono accessori: ognuno illumina un pezzo di teoria.

- **`gdb` (il debugger).** È _lo_ strumento del reverse engineering: un programma per ispezionare un altro programma. I gesti che userai: `disas main` / `disas vuln` (disassembla una funzione → vedi le istruzioni macchina e dove sta il buffer), `run VALORE` (esegue con un input), `info functions` (elenca le funzioni e i loro indirizzi → così trovi `secret`), `p system` (stampa l'indirizzo di una funzione di libreria, serve per ret2libc), `x/200xw $esp` (esamina la memoria a partire dalla cima dello stack → _vedi_ le tue `A` = `0x41414141` e le `B` = `0x42424242` mentre sovrascrivono l'indirizzo di ritorno). Quel `0x41414141` in un crash è la firma inconfondibile di un overflow riuscito: sono le tue `A` finite dentro `EIP`.
- **`perl` / `python` per comporre l'input.** Servono a generare byte arbitrari, anche non stampabili: `perl -e 'print "A"x112,"\xNN..."'`. È così che si scrive un indirizzo nella stringa (ricordando il little-endian).
- **I flag di `gcc`, che _sono_ le contromisure rese tangibili.** Nel lab i binari si compilano disattivando di proposito le difese, e ogni flag corrisponde a una protezione di cui parleremo:
    - `-fno-stack-protector` → **disattiva i canary**;
    - `-z execstack` → **rende lo stack eseguibile** (disattiva NX), necessario per il gradino 3;
    - `-m32` → compila a 32 bit (architettura IA32 del corso; richiede `gcc-multilib`);
    - e separatamente `echo 0 > /proc/sys/kernel/randomize_va_space` → **disattiva l'ASLR**.

> **La visione, da tenere a mente per l'esame:** il fatto che servano _tutti questi flag_ per far funzionare l'attacco classico ti dice già la conclusione del modulo: **oggi un buffer overflow "alla vecchia maniera" è raro**, perché di default canary + NX + ASLR sono accesi. Gli attacchi moderni (ret2libc, ROP) nascono proprio per aggirare quelle difese.

## Le contromisure (e come si aggirano)

### Canary ("canarino")

**Cosa fa.** Prima di un buffer, sullo stack viene messo un **valore di riferimento casuale** (il "canarino", come quelli dei minatori che rilevavano le fughe di gas). Al ritorno dalla funzione, il programma **verifica che il canarino sia integro**: se un overflow l'ha sovrascritto, la verifica fallisce e il processo viene **terminato** (di default; l'evento può anche essere catturato via segnali dell'OS). L'attaccante non può "scavalcare" il canarino: per arrivare all'indirizzo di ritorno deve passarci sopra, e così lo altera.

**Non** è una protezione dell'OS o dell'hardware. Si attiva con `-fstack-protector` (solo buffer di stringhe) o `-fstack-protector-all` (tutti); `--param ssp-buffer-size=` fissa una soglia oltre cui proteggere, per limitare l'**overhead**.

È aggirabile a **forza bruta** in programmi che fanno _fork_ di figli: il figlio eredita **lo stesso canarino** del padre; provo a indovinarlo un pezzo alla volta — se sbaglio il figlio crasha, ne genero un altro (canarino identico) e riprovo. Generalizzazione difensiva: **CFI** (vedi sotto).

### NX / W^X (stack non eseguibile)

**Cosa fa.** Marca le pagine di memoria dello stack come **non eseguibili**: anche se l'attaccante inietta shellcode sullo stack, la CPU **rifiuta di eseguirlo**. È la difesa diretta contro il gradino 3 (shellcode).

**Chi la fornisce.** È una **feature hardware** (Intel la chiama **XD bit**, _eXecute Disable_), che però **dev'essere supportata dall'OS**. Attenzione a un punto che il PDF sottolinea: **non esiste sui processori Intel/AMD a 32 bit puri** — è arrivata solo coi processori a 64 bit

**Punto debole (quiz!).** NX/W^X sono **quasi inutili da soli**, perché diversi attacchi fanno un uso _legittimo_ dello stack: non eseguono codice _dallo_ stack, ma lo usano per **riusare codice già marcato eseguibile** altrove. È esattamente ciò che fanno ret2libc, ret2syscall e ROP.

### ASLR (Address Space Layout Randomization)

**Cosa fa.** **Rende casuale l'indirizzo di partenza dei segmenti** del processo a ogni esecuzione, così l'attaccante non sa più _dove_ puntare. Senza un indirizzo prevedibile, non può scrivere un indirizzo di ritorno valido né sapere dove sia lo shellcode.

**Chi la fornisce.** L'**OS** (Linux: patch grsecurity/PaX, inclusa nel kernel solo in alcune distro). Randomizza gli **indirizzi virtuali**, non la disposizione fisica in RAM.

**Punto debole (quiz! — è il dettaglio che il PDF ripete).** L'ASLR è **incompleto**: randomizza librerie, base dello stack e base dello heap, **ma NON il segmento `.text`**. Quindi il codice del programma resta a indirizzi **prevedibili** — ed è lì che gli attacchi moderni vanno a pescare i pezzi di codice da riusare. (e come sanno però dove puntare il codice che hanno trovato?) È inoltre attaccabile a forza bruta (difficile sul 64 bit, dove lo spazio è enorme) o aggirabile usando i puntatori del codice legittimo. **Estensione difensiva: PIE.**

### PIE e RelRO (rafforzamenti dell'ASLR)

- **PIE** (_Position Independent Executable_): rende randomizzato **anche `.text`**, chiudendo il buco dell'ASLR. Per funzionare richiede una **doppia indirezione** dei puntatori a funzione tramite le tabelle **PLT** e **GOT** — che però sono a loro volta **sovrascrivibili** per dirottare le chiamate.
- **RelRO** (_Relocation Read-Only_): hardening che rende quelle tabelle (in particolare la GOT) **in sola lettura** dopo il caricamento, per chiudere quel nuovo buco.

### CFI (Control Flow Integrity)

**Cosa fa.** È la **generalizzazione** di tutte le difese precedenti: una _famiglia_ di tecniche (almeno 14 implementazioni note) che mira a **garantire che `EIP` non possa mai essere controllato da un attaccante**. Un esempio rilevante è il **supporto hardware per puntatori cifrati**: il processo sceglie all'avvio una chiave e la CPU **cifra/decifra trasparentemente** tutti gli indirizzi di ingresso/ritorno dalle funzioni; un programma vulnerabile può essere mandato in crash (DoS) ma **non dirottato**. Esempio reale citato: i **PAC** (_Pointer Authentication Codes_) sui processori Apple ≥ A12.

## Gli attacchi "anti-difesa": riusare il codice esistente

Quando NX impedisce di eseguire shellcode sullo stack, l'idea cambia: **non iniettare codice, ma riusare codice già caricato** (in libc o in `.text`, che ricordiamo l'ASLR _non_ randomizza). Lo stack overflow serve ancora, ma ora per iniettare **solo dati** — indirizzi e parametri — non istruzioni.

- **ret2libc.** Si dirotta `EIP` su una **funzione di libreria già caricata**, tipicamente **`system("/bin/sh")`**. Servono tre cose, che si trovano col debugger: l'**indirizzo di `system`** (`p system` in gdb), un modo di mettere sullo stack la **stringa `/bin/sh`** (spesso è già nell'ambiente, nella variabile `SHELL`), e comporre lo stack così che, al `RET`, `system` trovi al posto giusto il suo parametro. Si possono concatenare più ritorni (es. far seguire `exit` per una chiusura pulita che non insospettisca). _Due dettagli pratici dal lab:_ va aggiunto `SHELL=` (6 caratteri) per puntare al valore giusto della variabile, e se l'indirizzo di `system` finisce con un byte `00` lo si "ritocca" col byte successivo (`04`/`08`), perché lo `00` troncherebbe la stringa. Nota importante: ret2libc **funziona anche con lo stack non eseguibile** — è la sua ragion d'essere.
- **ret2syscall.** Variante: invece di saltare a una funzione di libreria, si **innesca direttamente una system call** (caricare il numero in `EAX`, i parametri nei registri, e invocare `INT 0x80`). Poiché queste operazioni sono comuni, in `.text` (non randomizzato!) esistono di sicuro frammenti di codice come `POP EAX; RET` o `INT 0x80` da riusare.
- **ROP (Return-Oriented Programming).** La generalizzazione massima. Si setaccia `.text` cercando **gadget**: brevi sequenze di istruzioni che **terminano con un `RET`** (es. `pop edi; ret`). Sullo stack si impila una **catena di indirizzi di gadget** intervallati dai dati: ogni gadget esegue il suo pezzettino, consuma i suoi dati e col `RET` "salta al gadget successivo" della catena. In pratica si **assembla un intero programma** mettendo in fila pezzi di codice già presenti — senza iniettare nulla e senza eseguire dallo stack, quindi **immune a NX**. Si può perfino sfruttare il **disallineamento**: leggendo i byte di `.text` con un offset diverso, si ottengono istruzioni del tutto nuove rispetto a quelle "intese" dal compilatore.

Esistono anche **Format Strings** (sfruttare una stringa di formato passata a `printf` per leggere/scrivere memoria) e **Heap Overflow** (sfruttare i metadati che la libc usa per l'allocazione dinamica), citati come ulteriori famiglie ma non centrali nel lab.

