# CALC — raccolta per il modello 3D interattivo (CPU DLX ↔ bus ↔ memoria)

> Idea di Lorenzo del 2026-11-06, durante `/lab CALC 03` guidato: un artefatto con una
> rappresentazione 3D dell'aspetto fisico dei meccanismi (collegamenti, operazioni possibili),
> interattivo. Qui si raccoglie il contenuto **verificato sulle fonti** man mano che emerge;
> l'artefatto si progetta dopo. Ogni voce con la sua fonte.

## 1. Oggetti fisici da rappresentare

| Oggetto | Cosa è | Fonte |
|---|---|---|
| Registri R0–R31 | 32 registri da 32 bit; `R0 = 0` sempre | 03 sl. 14–15 |
| Bus indirizzi | porta l'indirizzo calcolato dalla CPU (BA31…BA2 + BE3…BE0) | 02 p. 61, 02 (decodifica) |
| Bus dati | 32 bit nel DLX = 4 byte → 4 banchi | 02 p. 61 (caso a 16 bit), lezione 02 |
| Banchi di memoria | uno per byte del bus: banco 0 = bit 7–0, banco 1 = 15–8, banco 2 = 23–16, banco 3 = 31–24 | 02 p. 61 |
| Byte Enable BE0–BE3 | uno per banco: dicono quali banchi partecipano al ciclo | 02 p. 61 |
| Riga («piano») | stesso indirizzo di riga su tutti i banchi; BA0 (e BA1 a 32 bit) non escono: li sostituiscono i BE | 02 p. 61 (analogia edificio/montacarichi, pp. ~55–60) |
| MUX interno alla CPU | sposta il byte/halfword dalla posizione sul bus alla parte bassa del registro | 02 p. 61 |
| Sommatore indirizzi | base (registro tra parentesi) + offset 16 bit esteso con segno | 03 sl. 26 |
| Decoder / CS | dall'indirizzo alto sceglie il chip (mapping, allineamento dei dispositivi) | 02, lezione 02 |

## 2. Operazioni da animare

1. **`LHI Rd,imm16`** — l'immediato va nella metà **alta** di Rd, metà bassa a 0. Nessun accesso
   alla memoria. [03 sl. 33]
2. **`ADDI Rd,Rs,imm16`** — imm esteso con segno, sommato a Rs, **la somma va in Rd**.
3. **Store (`SB`/`SH`/`SW`) `Rs,off(Rb)`** — sommatore: `Rb + off` → bus indirizzi (la somma non
   va in nessun registro, `Rb` invariato); BE accesi secondo dimensione e indirizzo; i 8/16/32
   bit **bassi** di Rs vanno sui banchi selezionati.
4. **Load (`LB`/`LBU`/`LH`/`LHU`/`LW`) `Rd,off(Rb)`** — stesso calcolo d'indirizzo; i byte letti
   passano dal MUX nella parte bassa di Rd; parte alta riempita con 0 (`…U`) o con copie del bit
   di segno. Es.: `0x8081` → `LHU` `0x00008081`, `LH` `0xFFFF8081`. [03 sl. 16–17, 30]
5. **Accesso non allineato** — halfword a indirizzo dispari / word non multiplo di 4: il dato
   attraversa due righe → servirebbero due indirizzi di riga nello stesso ciclo → non possibile.
   Es. della dispensa: `SH R2,0x7FF1(R1)`. [03 sl. 46; 02 p. 61, «Non possibile»]
6. **Ciclo che scorre un array** (sl. 47–49): base che avanza di 4 (`ADDI R3,R3,4`), indice,
   `SNEI` + `BNEZ`.

## 3. Regole da far «vedere» (dove Lorenzo si è confuso)

- Un registro contiene solo 32 bit: **valore o indirizzo lo decide l'istruzione che lo usa**
  (tra parentesi = indirizzo; prima della virgola = dato, sorgente in store, destinazione in load).
- In una load il registro prima della virgola viene **sovrascritto**.
- Offset/immediato di 16 bit → metà **bassa** (esteso con segno); solo `LHI` → metà alta.
- Una cifra esadecimale = 4 bit (`1111` = `F`); pari/dispari dall'ultima cifra; multiplo di 4 se
  finisce in `0 4 8 C`.
- Allineamento: indirizzo multiplo della dimensione del dato (byte qualsiasi, halfword pari,
  word multiplo di 4).

## 4. Binario ed esadecimale — dove si parla l'uno, dove l'altro (richiesta di Lorenzo, 6/11)

Il modello deve mostrare **dove si ragiona in binario, dove in esadecimale e dove i due si
incontrano** (Lorenzo li ha mescolati due volte il 6/11: `0x1111` per `0xFFFF`, `0x100` per `0x4`).

| Zona | Si legge in | Perché |
|---|---|---|
| Fili del bus, piedini, BE, bit di segno, singoli bit di un registro | **binario** | ogni filo porta un bit |
| Codice assembler, immediati, offset, indirizzi, contenuto dei registri come numero | **esadecimale** | notazione compatta del docente (`0x…`, `…h`) |
| Punto d'incontro: ogni cifra esadecimale ↔ un gruppo di **4 fili** | conversione | `F` = `1111`, `4` = `0100`; 8 cifre = 32 bit |

Da animare: un registro di 32 bit mostrato come 8 cifre esadecimali, ognuna che si «apre» nei suoi
4 bit; estensione con segno che copia il bit 15 nei 16 bit alti (e il risultato che si richiude in
`FFFF`); somma `E0000000 + 4` sulla cifra più a destra.

## 5. Da raccogliere ancora

- Tabella completa dei BE per ogni combinazione dimensione × 2 bit bassi dell'indirizzo (bus a 32 bit).
- Segnali di controllo del ciclo (RD, WR, tempi) — moduli 02/05.
- Interruzioni (04) e handshake (05), se il modello li deve coprire.
- Pipeline DLX (07–08): fuori scopo per ora.
