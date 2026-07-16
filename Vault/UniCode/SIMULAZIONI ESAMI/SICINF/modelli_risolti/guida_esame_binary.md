# Guida Esame — Binary Exploitation (buffer overflow x86_32)

> File da aprire il giorno dell'esame appena riconosci un esercizio di questa tipologia: un
> **eseguibile ELF a 32 bit** (`es`, `bof`, `esame`, `secret`, `secret_func1`, …) fornito compilato,
> spesso in `.zip`/`.gz`, con consegna del tipo "sfrutta il buffer overflow per **stampare la flag**"
> oppure "per **eseguire lo shellcode / ottenere una shell**". Autosufficiente per ogni combinazione
> di protezioni. Per la sequenza di comandi + le zone grigie vedi `procedura_operativa_binary.md`;
> per i 7 casi reali già risolti, `modello_binary_exploitation.md`; per il deliverable,
> `template_report_binary.md`.
>
> **Principio guida**: ogni **offset** e ogni **indirizzo** li trovi TU con `gdb`/`nm` **sul binario
> che hai davanti** — mai copiarli dal testo, dagli appunti o da un altro esercizio. Il testo ti dice
> *quale* indirizzo cercare e *come*, non *quale numero* digitare.

---

## 0. I due gate che NON hai il permesso di saltare

- ⚠️ **Gate A — ASLR disattivata.** `cat /proc/sys/kernel/randomize_va_space` deve dare `0`. Se no:
  `echo 0 | sudo tee /proc/sys/kernel/randomize_va_space`. **Non sopravvive a un riavvio** e **gdb
  la disattiva da solo per il processo che debugga**: se l'exploit funziona in gdb ma fallisce fuori
  con SIGSEGV immediato e nessuna flag, la prima cosa da ricontrollare è che l'ASLR sia ancora off
  (rifai il comando). È il trabocchetto reale di S4 es2.
- ⚠️ **Gate B — non fermarti alla prima funzione "segreta".** Il binario ne contiene di solito
  **molte** con nomi plausibili (`secret_function_maybe_flag`, `betteryetthisone`, `super_hidden`…):
  quasi tutte sono **decoy** che stampano messaggi falsi o rickroll. **Una sola** stampa `SEC{...}`.
  Il nome non è affidabile — provale **tutte** finché non compare la flag. In 5 casi reali su 7 c'erano
  da 2 a 6 decoy.

---

## 1. Triage — che tipo di esercizio è (in 3 comandi)

Appena hai il binario eseguibile (`chmod +x ./<bin>`), lancia questi tre comandi. Decidono tutto:

```bash
file ./<bin>                          # architettura: deve essere "ELF 32-bit ... Intel 80386"
readelf -lW ./<bin> | grep GNU_STACK  # RWE = stack ESEGUIBILE (shellcode ok) ; RW = NX attivo
nm ./<bin> | grep -iE ' [tT] '        # funzioni definite: c'è una funzione "segreta"?
```

**Canary (protezione non presente nel pool, ma da saper riconoscere).** I 7 binari del pool sono
compilati **senza** stack protector (`nm ./<bin> | grep stack_chk` → vuoto), quindi l'overflow classico
funziona. Se invece durante la bisezione vedi `*** stack smashing detected ***: terminated` (invece di
`0x42424242 in ?? ()`), c'è un **canary**: il valore-sentinella tra buffer e ret address viene
controllato prima del `ret` e il programma aborta. In quel caso l'overflow lineare non basta — servirebbe
leakare/riscrivere il canary (fuori dallo scopo di questo pool); segnala che l'hai riconosciuto. Firma
rapida: `readelf -s ./<bin> | grep -i stack_chk` non vuoto, o `checksec` che riporta "Canary found".

**Vettore d'ingresso (argv o stdin?).** Aggiungi al triage `nm ./<bin> | grep -iE 'gets|fgets|read'`:
se il binario legge il payload da **stdin** (`gets`/`fgets`/`read`) invece che da `argv[1]`, il trasporto
e le regole bad-char cambiano — **salta alla §4-bis**. Se legge da `argv` (i 7 casi del pool: `./bin $(…)`),
prosegui normalmente. Firma pratica: lanciato **senza argomenti**, un binario stdin-based **si blocca in
attesa di input**; uno argv-based no.

E leggi la **consegna**: cosa chiede l'obiettivo?

| Segnale nella consegna | Cosa implica |
|---|---|
| "farsi **stampare la flag**" / "recuperare la Flag" | c'è (quasi sempre) una **funzione segreta** che stampa `SEC{...}` → ret2secret-function. |
| "eseguire lo **shellcode** fornito" / "ottenere una **shell**" | nessuna funzione utile → **shellcode injection** (se stack RWE) o ret2libc (se NX). |
| "stampa la flag **se si conosce la password**" (ex6/ex7) | ret2secret-function + **bonus recupero password** (`strings`/gdb). |
| binario `.gz` singolo (`secret.gz`) | `gunzip` poi `chmod +x`. |
| `.zip` (`bof.zip`) | `unzip`, entra nella cartella estratta, `chmod +x`. |

Il triage indirizza; la **tecnica esatta** la decide l'albero della Sezione 2.

---

## 2. Albero di decisione per protezioni (il cuore della guida)

```
                         ┌─────────────────────────────────────────────┐
                         │  Esiste una funzione che stampa la flag?     │
                         │  (nm / info functions → nome tipo secret,    │
                         │   reveal, super_*, *flag*, *hidden*, trythat)│
                         └───────────────┬──────────────────┬──────────┘
                                    SÌ   │                  │  NO (obiettivo = shell)
                                         ▼                  ▼
                          ┌──────────────────────┐   ┌─────────────────────────────┐
                          │ RET2SECRET-FUNCTION   │   │ GNU_STACK = RWE (eseguibile)?│
                          │ (NX irrilevante:      │   └──────┬──────────────┬───────┘
                          │  salti a codice       │      SÌ  │              │  NO (NX on)
                          │  già presente)        │          ▼              ▼
                          │  → §2.A               │  ┌──────────────┐  ┌──────────────┐
                          └──────────────────────┘   │ SHELLCODE    │  │ RET2LIBC     │
                                                      │ INJECTION    │  │ (system+exit │
                                                      │ → §2.B       │  │  +/bin/sh)   │
                                                      └──────────────┘  │ → §2.C       │
                                                                        └──────────────┘
```

**Nota trasversale — SUID.** Se `ls -l ./<bin>` mostra la `s` (`-rwsr-xr-x`) il binario è SUID-root:
qualunque shell ottieni (§2.B o §2.C) sarà **root** (`id` → `uid=0`). Attenzione: **gdb e il SUID non
vanno d'accordo** — sotto debugger il SUID è disattivato (`id` dà uid normale), va verificato **fuori**
da gdb, e per binari SUID il core dump richiede `sudo sysctl -w fs.suid_dumpable=1` (vedi §2.B).

### §2.A — RET2SECRET-FUNCTION (5 casi su 7 nel pool: il ramo più probabile)

Salti l'indirizzo di ritorno su una funzione già presente che stampa la flag. **NX e stack non
eseguibile NON contano** (non inietti codice).

1. **Trova le funzioni candidate.**
   - **non-PIE** (`nm` mostra indirizzi `0x0804…`): usa direttamente `nm ./<bin>` — gli indirizzi
     sono **fissi**.
   - **PIE** (`nm` mostra `0x0000…`): apri gdb, fai **un `run` qualunque** (anche `run ciao`) e solo
     **dopo** `info functions` — prima del `run` vedi solo l'offset di link. A runtime (ASLR off)
     diventano `0x5655…`, stabili.
   ```bash
   nm ./<bin> | grep -iE ' [tT] ' | grep -viE '__|_start|_init|_fini|frame_dummy|register|gmon'
   # oppure in gdb (binari PIE):  (gdb) run ciao   →   (gdb) info functions
   ```
2. **Trova l'offset per bisezione** (vedi §3): payload `A`*N + `BBBB` finché `EIP = 0x42424242`.
3. **Prova ogni candidata**, sostituendo `BBBB` con l'indirizzo in **little-endian**:
   ```bash
   ./<bin> $(python -c 'print("A"*OFFSET + "\xLL\xLL\xLL\xLL")')   # indirizzo a byte invertiti
   ```
   finché compare `SEC{...}`. Le altre stampano messaggi decoy o crashano.
4. **Bad character** (§4): se l'indirizzo della funzione giusta contiene `0x00`/`0x20`/`0x0a`/`0x09`,
   via `strcpy`/`argv` il payload si tronca. Nel pool non è mai capitato sulla funzione **giusta**,
   ma verifica; se capitasse, vedi §4 e `procedura_operativa_binary.md`.

**Casi reali di riferimento**: ex2 (offset 16), ex4 (offset 16, non-PIE, `secret_function_a..f`),
ex5 (offset 16, 6 decoy, bad char 0x00 su un decoy), ex6 (offset 212, non-PIE, +password),
ex7 (offset 44, non-PIE, +password).

### §2.B — SHELLCODE INJECTION (2 casi su 7: quando l'obiettivo è una shell e lo stack è RWE)

Inietti NOP sled + shellcode nel buffer e fai puntare il ritorno nella slitta.

1. **Serve lo stack eseguibile** — verificato al triage (`GNU_STACK = RWE`). Il testo di solito
   **fornisce lo shellcode** (46 byte tipici che aprono `/bin/sh`): copialo esatto.
2. **Trova l'offset** (§3): `A`*N + `BBBB` → `EIP = 0x42424242`. Chiamalo **OFF**.
3. **Guarda dove sono finiti i tuoi byte**: dopo il crash, `x/200xw $esp` (o `x/700xw $esp`) — cerca
   la fascia di `0x41414141`. Scegli un indirizzo **al centro** di quella fascia = bersaglio del
   NOP sled.
4. **Componi il payload** = `[NOP] + [shellcode] + [indirizzo]`, con `len(NOP) + len(shellcode) = OFF`
   (così l'indirizzo cade esattamente sul ret address) e l'indirizzo che punta **dentro** i NOP:
   ```bash
   ./<bin> $(python -c 'print("\x90"*(OFF-46) + "<46-byte shellcode>" + "\xLL\xLL\xLL\xLL")')
   ```
   Esempio reale ex1: `OFF=622`, `\x90`*576 + shellcode(46) + `\xb0\xd2\xff\xff` (0xffffd2b0).
5. **⚠️ Lo stack sotto gdb ≠ lo stack standalone** (anche con ASLR off): l'`argv[0]` è diverso
   (`/percorso/assoluto` in gdb vs `./bin` da shell) → il buffer si sposta anche di **centinaia di
   byte**. Un indirizzo trovato in gdb può fallire fuori. Rimedi: (a) NOP sled **largo** per assorbire
   lo scarto; (b) se serve precisione, prendi il dump dal **core dump della vera esecuzione standalone**:
   ```bash
   sudo sysctl -w fs.suid_dumpable=1        # solo se il binario è SUID (altrimenti il core non si salva)
   ./<bin> <payload che crasha>              # genera il crash da shell
   coredumpctl list                          # trova il PID
   sudo coredumpctl gdb <PID>                # apri il core (di root se SUID → sudo)
   (gdb) x/200xw $esp                        # QUI vedi la vera fascia di NOP standalone
   ```
6. **Se SUID-root** → la shell è root: verifica **fuori** da gdb con `id` → `uid=0`.

**Casi reali**: ex1 (offset 622), ex3 (buffer ~1518, solo appunti-guida allegati).

### §2.C — RET2LIBC (NON nel pool d'esame, ma nel programma: NX on + nessuna funzione utile)

Quando lo stack **non** è eseguibile (NX) e non c'è una funzione segreta, non puoi iniettare shellcode:
**riusi `system("/bin/sh")` già presente nella libc**.

1. **Trova gli indirizzi** (breakpoint per avere la libc caricata):
   ```bash
   gdb ./<bin>
   (gdb) b *main
   (gdb) run
   (gdb) p system            # indirizzo di system
   (gdb) p exit               # indirizzo di exit (ritorno "pulito" di system)
   (gdb) find $esp, +0x3000, "SHELL="   # cerca la stringa /bin/sh nell'ambiente (vedi §4)
   ```
2. **Payload** = `[padding OFF] + [system] + [exit] + [indirizzo di "/bin/sh"]`:
   ```bash
   run "$(perl -e 'print "\x90"x OFF ,"<system>","<exit>","<addr /bin/sh>"')"
   ```
   `system` esegue la shell; `exit` fa da suo indirizzo di ritorno (chiusura pulita); l'ultimo è il
   **parametro** di `system` (la stringa `/bin/sh`, tipicamente il valore di `SHELL=` in `envp`,
   scavalcando i 6 caratteri `SHELL=` → indirizzo+6).
3. **⚠️ Gotcha ret2libc** (§4): (a) se l'indirizzo di `system` contiene `0x00` lo `strcpy` tronca →
   usa il byte immediatamente successivo, ancora dentro `system`; (b) se contiene `0x20` (spazio) il
   `$()` **non quotato** tronca il payload per word-splitting → **quota** la sostituzione:
   `run "$(perl -e '…')"`; (c) `x/500s $esp` è inaffidabile su lunghe distanze → usa `find` (attento
   all'overflow di `0xffffffff`).

**Riferimento**: S4 es4 (`guida_lab_moduloS4_binary_exploits.md`, "Esercizio 4 — ret2libc").

---

## 3. Trovare l'offset — la bisezione, con gli stadi intermedi da riconoscere

L'offset (byte dall'inizio del buffer al ret address salvato) **cambia ogni volta**. Metodo:

```bash
gdb ./<bin>
(gdb) run $(perl -e 'print "A"x200')   # parti alto: crash? è overflow
(gdb) run $(perl -e 'print "A"x100')   # dimezza: no crash? sei sotto
(gdb) run $(perl -e 'print "A"x150')   # bisezione, avvicinati...
(gdb) run $(perl -e 'print "A"x OFF ,"BBBB"')   # conferma: EIP == 0x42424242
```

**Gli stadi intermedi (fondamentale — non tutti i crash sono uguali):**
- **`SIGSEGV … in <nomefunzione> ()`** (indirizzo riconosciuto, es. `in main`): hai corrotto solo
  l'**EBP salvato** (che sta *prima* del ret address), non ancora il ret. Sei **vicino ma corto**.
- **`SIGILL … in <nomefunzione> ()`**: il `ret` è **avvenuto** ma sei atterrato a metà di un'istruzione
  valida (byte decodificati come opcode illegale). Offset **quasi** giusto.
- **`SIGSEGV 0x42424242 in ?? ()`**: `EIP` è esattamente `BBBB`. **Controllo pieno del ret address** →
  offset esatto. I `?? ()` (indirizzo non riconosciuto) sono la firma del successo.

Regola mnemonica: **`in <funzione>` = EIP non dirottato** (crash da dato corrotto altrove);
**`in ?? ()` = EIP sotto il tuo controllo totale**.

---

## 4. Bad character e quoting — il gruppo di gotcha che fa perdere più tempo

Un indirizzo va **iniettato intatto**. Quattro byte lo troncano se passa via `strcpy`/`argv`/shell:

| Byte | Nome | Perché tronca | Rimedio |
|---|---|---|---|
| `0x00` | NUL | terminatore di stringa C: `strcpy` si ferma lì | se è un **indirizzo di funzione** con scelta multipla (decoy), scartalo; se è l'unico bersaglio, usa il byte adiacente ancora dentro la funzione/zona |
| `0x20` | spazio | la shell fa **word-splitting** su `$()` **non quotato** | **quota**: `run "$(perl -e '…')"` — le doppie apici esterne bloccano lo split, le singole interne restano contesto perl separato |
| `0x0a` | newline | separatore di riga per la shell | come `0x20`: quota, o sposta il bersaglio se hai scelta |
| `0x09` | tab | separatore IFS | come sopra |

**La distinzione chiave (dalla pratica reale S4):**
- Se il byte proibito cade in un **indirizzo dello stack scelto da te** (bersaglio del NOP sled, dove
  hai margine) → **sposta il bersaglio** di qualche decina di byte nella stessa fascia.
- Se cade nell'indirizzo di una **funzione fissa** (`system`, o l'unica funzione segreta) dove non c'è
  scelta → il problema è il **trasporto**, non l'indirizzo: se è `0x20`/`0x0a`/`0x09` **quota il `$()`**;
  se è `0x00` non c'è quoting che tenga (è `strcpy` a fermarsi) → serve il byte adiacente o un vettore
  d'ingresso che non usi `strcpy` (nel pool non è mai stato necessario sulla funzione giusta).

Riconoscere **in anticipo** quale dei due casi stai affrontando evita di cercare un "indirizzo vicino"
quando invece il fix è quotare (e viceversa).

---

## 4-bis. Variante di trasporto — il binario legge da **stdin** (`gets`/`fgets`/`read`), non da `argv`

> ⚠️ **Estensione critica della §4.** Tutti i 7 casi del pool ricevono il payload come **argomento**
> (`./bin $(python -c '…')`), quindi via `argv[1]` + `strcpy`. Ma la vulnerabilità classica del corso è
> `gets(buf)`/`fgets`/`read`, che leggono da **standard input**: se all'esame capita un binario così, il
> `$(…)` come argomento **non arriva mai al buffer** e cambiano sia il *trasporto* sia le *regole bad-char*.
> Questa sezione è la variante gemella della §4: **se il binario legge da stdin, applica questa; se legge
> da argv, applica la §4**. Gli esempi qui sotto sono **didattici** (dichiarati come tali): nel pool storico
> non compaiono, ma il vettore è esattamente quello del lab S4.

### 4-bis.1 Come riconosci che legge da stdin (non da argv)

Due segnali, uno statico e uno comportamentale:

- **Analisi statica** — nel disassemblato/nei simboli compare una lettura da stdin, **non** un accesso a
  `argv`:
  ```bash
  nm ./<bin> | grep -iE 'gets|fgets|read|scanf'      # gets/fgets/read/gets_s presenti?
  objdump -d ./<bin> | grep -iE 'call.*(gets|fgets|read|__isoc99_scanf)@plt'
  strings ./<bin> | grep -iE 'gets|Enter|password:|input'   # spesso c'è un prompt "Enter …"
  ```
  Se in `main`/`vuln` vedi `call gets@plt` o `call fgets@plt` (con `stdin` come 3° argomento) o
  `call read@plt` (con `0` = fd stdin come 1° argomento) **e non** vedi la catena
  `mov eax,[eax+0x4] ; …[eax]` che carica `argv[1]` (cfr. modello ex3/ex4) → **legge da stdin**.
- **Comportamento** — lancia il binario **senza argomenti**: se **si blocca in attesa** (cursore fermo,
  nessun crash, riprende solo quando digiti `Invio`) sta leggendo stdin. Un binario argv-based invece
  termina subito (o stampa un `Usage:`), non aspetta niente.
  ```bash
  ./<bin>            # si ferma qui in attesa? → stdin.  Ctrl-D o Ctrl-C per uscire
  ```

### 4-bis.2 Come consegni il payload a un binario stdin-based

Il payload va **su stdin**, non in `argv`. Tre vettori equivalenti, con pro/contro:

| Vettore | Comando | Pro / Contro |
|---|---|---|
| **Pipe** | `python3 -c 'import sys; sys.stdout.buffer.write(b"A"*OFF + b"\xLL\xLL\xHH\xHH")' \| ./<bin>` | Il più diretto. `sys.stdout.buffer.write` scrive **byte grezzi** senza newline finale né ricodifiche → pulito per byte binari. **Contro:** con la pipe il processo eredita stdin dalla pipe, non dal terminale: se il binario dopo l'overflow apre una **shell** (shellcode/ret2libc) la shell trova subito EOF e muore → per le shell usa here-string o file, non la pipe. |
| **Here-string** | `./<bin> <<< "$(python3 -c '…')"` | Comodo da riga di comando. **Contro:** il `<<<` di bash/zsh **aggiunge un `\n` finale** — di solito innocuo (il newline sta *dopo* l'indirizzo di ritorno), ma se ti serve controllo esatto sull'ultimo byte, evitalo. Vale lo stesso avviso pipe/EOF per le shell. |
| **File + redirect** | `python3 -c '…' > payload.bin` poi `./<bin> < payload.bin` | Il più **robusto e riproducibile** (stesso file in shell e in gdb: `(gdb) run < payload.bin`). **Consigliato in fase di bisezione** e per gli screenshot. Nessuna sorpresa di newline se costruisci il file con `sys.stdout.buffer.write`. |

⚠️ **`echo`/`printf` vs `python3`.** `echo "$payload"` aggiunge un `\n` finale (a meno di `echo -n`) e
può reinterpretare le sequenze; `printf` non aggiunge newline ma richiede `\xNN` esatti nel formato.
Per byte binari **preferisci sempre** `python3 -c 'import sys; sys.stdout.buffer.write(b"…")'` (oppure
`perl -e 'print …'`, che non aggiunge newline): eviti newline fantasma e ricodifiche UTF-8 dei byte alti.

### 4-bis.3 Come cambiano i bad character (il ribaltamento rispetto alla §4)

Questo è il punto in cui è **facilissimo confondersi sotto stress**: con stdin le regole si **ribaltano**
rispetto al caso argv/strcpy della §4.

| Byte | argv + `strcpy` (§4, il pool) | stdin + `gets` |
|---|---|---|
| `0x00` NUL | **BAD**: `strcpy` termina la copia sul NUL → il payload si tronca. Se è nell'indirizzo giusto sei bloccato. | **USABILE**: `gets` **non** si ferma sul NUL (non è `strcpy`); copia byte per byte fino a newline/EOF. `0x00` diventa un byte normale del payload. |
| `0x0a` newline | Bad **solo** se passa via `$()` **non quotato** (word-splitting shell) → si risolve **quotando** `"$(…)"`. | **BAD principale**: `gets` **termina l'input** esattamente sulla `\n`. Un `0x0a` nell'indirizzo o nello shellcode tronca lì → tutto ciò che segue non entra. Non c'è quoting che aiuti: è la semantica di `gets`, non della shell. |
| `0x20` spazio | Bad se `$()` non quotato (word-splitting) → **quota**. | **USABILE**: stdin è un flusso di byte grezzi, non un elenco di argomenti → nessun word-splitting. Lo spazio entra intatto. |
| `0x09` tab | come `0x20` (IFS) → quota. | **USABILE**: come lo spazio, nessuno split su stdin. |

**In una frase, per non sbagliare:** *via **argv/strcpy** il nemico n.1 è `0x00`; via **stdin/gets** il
nemico n.1 diventa `0x0a` (newline), mentre `0x00` è diventato tuo amico.* Spazi e tab, che via argv
richiedevano il quoting, su stdin non danno alcun problema.

**Dipende da QUALE funzione legge** (non tutte le letture da stdin sono uguali):

| Funzione | Termina su | `0x00` | `0x0a` | Limite di lunghezza |
|---|---|---|---|---|
| `gets(buf)` | newline o EOF | usabile | **bad** (termina) | nessuno (è proprio l'overflow) |
| `fgets(buf, N, stdin)` | newline, EOF **o** `N-1` byte | usabile | **bad** (termina) | **sì, N-1 byte**: se l'offset+4 supera `N-1` l'overflow classico **non raggiunge** il ret address → riconoscilo dal disassemblato (`N` è il 2° argomento di `fgets`) e verifica che `OFF+4 ≤ N-1`. |
| `read(0, buf, N)` | `N` byte o EOF | usabile | **usabile** (non è speciale) | sì, N byte — ma nessun byte è proibito: il vettore **più permissivo** (né `0x00` né `0x0a` bloccano). |

### 4-bis.4 La bisezione dell'offset resta identica — cambia solo **come invii** ogni tentativo

Il metodo della §3 (parti alto con `A`*N, dimezza, conferma con `A`*OFF + `BBBB` fino a
`0x42424242 in ?? ()`, riconosci gli stadi `in <func>`/`SIGILL`/`?? ()`) è **concettualmente invariato**:
cambia **solo il modo di consegnare** ogni prova, da argomento a stdin. In gdb:

```bash
# invece di:   (gdb) run $(perl -e 'print "A"x OFF ,"BBBB"')        ← argv (§3)
python3 -c 'import sys; sys.stdout.buffer.write(b"A"*OFF + b"BBBB")' > t.bin
gdb ./<bin>
(gdb) run < t.bin        # ← stesso payload, consegnato su stdin
# atteso identico:  Program received signal SIGSEGV, 0x42424242 in ?? ()
```

Tutto il resto (interpretazione degli stadi del crash, EBP corrotto vs ret controllato) è invariato.
⚠️ Un solo accorgimento: se usi `gets`, **non mettere `0x0a` nel padding di prova** (le `A` = `0x41` vanno
benissimo, ma se un giorno usi byte casuali evita la newline) — un `0x0a` accidentale nel payload di test
troncherebbe la prova e ti farebbe leggere un offset falso.

**Rimando incrociato:** una volta trovato l'offset e scelto l'indirizzo/shellcode, il ramo è lo stesso
della §2 (ret2secret-function / shellcode injection / ret2libc): l'unica differenza end-to-end è il
**vettore d'ingresso** di questa §4-bis e le **bad-char ribaltate** della §4-bis.3.

---

## 5. Recupero della password (bonus ex6/ex7)

Quando la consegna dice "stampa la flag **senza conoscere la password**" e chiede la password come bonus:

- **Metodo A — in chiaro:** `strings ./<bin>` — se la password è una stringa letterale compare
  direttamente (es. `ThisShouldBeHardToGuess…`). Riconoscila accanto a `SEC{%s}`, `Usage:`, ecc.
- **Metodo B — de-offuscata a runtime:** se `strings` non la mostra (è calcolata), mettiti un
  breakpoint **subito prima** della `strcmp`/confronto e leggi la memoria puntata dal registro
  argomento:
  ```bash
  (gdb) disas check                    # individua l'indirizzo del push/lea prima di call strcmp@plt
  (gdb) b *0xINDIRIZZO_PRIMA_DI_STRCMP
  (gdb) run ciao
  (gdb) x/s $eax                        # (o l'altro operando) → la password de-offuscata
  ```
- **Limite (da scrivere nel pwn.txt):** funziona solo se il programma **de-offusca** la password per
  confrontarla in chiaro. Non funziona per sistemi reali che **hashano l'input** e confrontano col
  digest (non c'è mai la password in chiaro in memoria). La **flag**, invece, spesso è ricostruita via
  XOR solo dentro la funzione target → non esce da `strings`, esce solo **eseguendola** (cioè con
  l'exploit stesso).

---

## 6. Verifica finale e deliverable

- **ret2secret-function**: la flag `SEC{...}` è stampata (il `Segmentation fault` che segue è atteso e
  **non** è un errore — la flag esce prima del crash del ret finale).
- **shellcode injection / ret2libc**: si apre una shell (`$`, o `executing new program: /bin/sh|dash`);
  se SUID, `id` → `uid=0(root)` **fuori** da gdb.
- Deliverable tipici (vedi `template_report_binary.md`): un file di testo (`bof.txt` o `pwn.txt`) con
  flag + payload finale + descrizione dettagliata dei passaggi (il **dettaglio è criterio di voto**),
  e **2+ screenshot**: uno che dimostra il controllo del ret address (`AAAA..AA+BBBB` → `0x42424242`),
  uno con l'exploit funzionante (flag stampata / shell ottenuta). Nomi ricorrenti: `overflow.png`,
  `payload.png`, `exploit.png`, `overflowNN.png`.

---

## 7. Checklist mentale d'esame (la catena)

1. `file` + `readelf -lW … GNU_STACK` + `nm` + leggi la consegna → **quale ramo** (§2.A/B/C).
2. ASLR off (Gate A). Binario PIE o non-PIE? (cambia come leggi gli indirizzi).
3. **Offset per bisezione** (`A`*N + `BBBB` → `0x42424242 in ?? ()`) — mai copiarlo.
4. **ret2secret**: prova **tutte** le funzioni candidate (Gate B), riconosci `SEC{...}`.
   **shellcode**: NOP sled + shellcode + indirizzo nella slitta (occhio a gdb≠standalone).
   **ret2libc**: system + exit + /bin/sh (occhio a bad char e quoting).
5. **Bad character** sull'indirizzo iniettato? (§4) sposta il bersaglio *oppure* quota il `$()`.
6. Verifica (flag stampata / shell / `id`=root se SUID), poi scrivi il report dettagliato + screenshot.

---

## 8. Materiale di riserva — binari a **64 bit** (x86_64) — *raramente necessario*

> ⚠️ **Dichiarazione:** tutto il pool storico e il lab S4 sono **x86_32** (`file` → *Intel 80386*). Un
> binario a 64 bit all'esame è **improbabile**. Questa sezione è una rete di sicurezza minima, non il caso
> standard: se `file ./<bin>` dice `ELF 64-bit … x86-64`, ecco cosa cambia rispetto a tutto quanto sopra.

**Cosa NON cambia:** il concetto di overflow, la bisezione per trovare l'offset, l'idea di dirottare il
ret address, l'ASLR-off, i due gate. **Cosa cambia** (3 punti):

1. **Indirizzi a 8 byte, non 4.** Il ret address ora è un valore a 64 bit → nel payload l'indirizzo è
   **8 byte** little-endian, non 4. Il marcatore di conferma diventa `"BBBBBBBB"` (8 `B`) e il crash da
   cercare è `RIP = 0x4242424242424242`. **Occhio alla bisezione/conteggio offset:** l'offset in sé si
   trova come prima (byte fino al ret salvato), ma quando componi l'indirizzo ricorda che ne servono
   **8** — un errore frequente è scriverne 4 e sballare tutto l'allineamento.
   - **Nota bad-char pratica:** gli indirizzi tipici del codice/stack a 64 bit hanno i **byte alti a `0x00`**
     (es. `0x0000555555555189`): via `argv`/`strcpy` quegli zeri **troncano** → un altro motivo per cui
     l'exploit via **stdin** (§4-bis, dove `0x00` è usabile) è spesso l'unica strada su 64 bit.
2. **Argomenti nei registri, non sullo stack.** La convenzione **System V AMD64** passa i primi argomenti
   in `rdi, rsi, rdx, rcx, r8, r9` (nel 32 bit erano tutti sullo stack). Conseguenza: se vuoi chiamare
   `system("/bin/sh")` **non basta** mettere la stringa sullo stack come nel ret2libc a 32 bit — devi
   caricare l'indirizzo di `"/bin/sh"` in **`rdi`** *prima* di saltare a `system`. Per la sola
   **ret2secret-function** (salti a una funzione **senza argomenti** che stampa la flag) questa complicazione
   **non si presenta**: sovrascrivi il ret con l'indirizzo della funzione e basta, come a 32 bit.
3. **Servono gadget ROP** per impostare i registri. Per mettere un valore in `rdi` si riusa una sequenza
   già presente nel binario del tipo `pop rdi ; ret`: la metti nel payload seguita dal valore da caricare,
   poi l'indirizzo di `system`. Come si cercano i gadget:
   ```bash
   ROPgadget --binary ./<bin> | grep 'pop rdi'      # tool dedicato (se installato)
   objdump -d ./<bin> | grep -B1 'ret'              # fallback grezzo: cerca "pop rdi" seguito da "ret"
   ```
   Payload ret2libc a 64 bit (schema minimo): `[padding OFF] + [addr di "pop rdi; ret"] + [addr "/bin/sh"]
   + [addr system]`. (A 64 bit c'è anche il vincolo di **allineamento dello stack a 16 byte** prima di
   `call system`: se `system` crasha subito, inserisci un gadget `ret` in più come padding di allineamento.)

**In pratica all'esame:** se ti capita un 64 bit ed è un **ret2secret-function**, procedi quasi come a 32
bit (solo indirizzo a 8 byte). Se è **shell via ret2libc**, serve la catena ROP del punto 3 — segnala nel
report che l'hai riconosciuta anche se non fai in tempo a completarla: dimostra il metodo.

<!-- AUTO-LINKS:START -->
## 🔗 Collegati

- [[modello_binary_exploitation]]
- [[guida_lab_moduloS4_binary_exploits]]
- [[appunti_moduloS4_binary_exploits]]

**Hub:** [[master_map_studio]] · [[metodo_studio_esami_pratici]]
<!-- AUTO-LINKS:END -->
