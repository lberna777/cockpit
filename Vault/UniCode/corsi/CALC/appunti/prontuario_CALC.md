# Prontuario d'esame — CALC

> Cresce a ogni lezione (`/lezione CALC <ID>`, sezione «Passo di procedura»). Si porta alla prova
> del checkpoint (~3 nov) e si rifinisce sul ciclo delle prove. Notazione: quella del docente.

## 0. Leggere il testo: regole di conto *(lezione 02p, 2026-10-08)*

Si applicano **prima** della procedura: traducono le frasi del testo in bit. Entra solo ciò che è
stato esercitato in sessione. Procedure complete con esempi: [[cheatsheet_conversioni_CALC]].

| Regola | Come si applica | Esempio |
|---|---|---|
| **Chi pilota i bus** | `BA` e `RD/WR`: sempre la CPU. `BD`: la CPU in scrittura, il **dispositivo** in lettura | — |
| **Scala delle unità** | ogni gradino è ×1024 = +10 all'esponente: **K = 2^10, M = 2^20, G = 2^30** | 1 GB = 2^30 |
| **Taglia → bit interni K** | spezza in *numero × unità*, scrivi entrambi come potenze di due, **somma gli esponenti** | 32 KB = 2^5·2^10 = 2^15 → 15 · 512 KB → 19 · 64 MB = 2^6·2^20 → 26 · 2 GB → 31 |
| **Bit interni = piedini** | un chip da 2^K byte ha i piedini `A[K-1..0]` | 128 KB → `A0`…`A16` (dispensa 02 p. 11) |
| **Bit che scelgono il blocco** | 32 − K (DLX): sono i bit alti, fissi su tutto il blocco | 2 GB → 32 − 31 = 1 → il solo `BA31` |
| **Binario → decimale** | pesi `… 8 4 2 1`: somma dove c'è `1`; rifai la somma per verifica | `1100` = 8+4 = 12 |
| **Allineamento** | base multipla della taglia 2^K ⇔ **ultimi K bit a 0** | blocco da 8 byte: parte solo da `0000` o `1000` |

**Inciampi da non ripetere** (sessione 2026-10-08):
- dimenticare l'unità: «32 KB → 5 piedini» (preso solo 32 = 2^5). Contromisura: scrivere sempre
  le **due** potenze, numero e unità;
- valore di M sbagliato (2^4 invece di 2^20). Contromisura: K, M, G = 10, 20, 30;
- leggere `1100` come 8: ricontare i pesi da destra.

**Inciampi del 2026-10-09** (esercizio 10, conti in hex):
- di nuovo l'unità persa: «16K = 2^4». Contromisura: riscrivere **16 × 2^10** prima di convertire;
- 2^14 scritto con l'1 in fondo: l'1 sta **a sinistra**, poi 14 zeri, poi gruppi da 4 da destra;
- `10000h − 4000h` → «12000»: in una colonna va **una cifra** (12 = **C**) e l'1 che presta
  diventa 0 → `C000h`;
- quanti chip: numero davanti alla K in binario, un chip per ogni 1 (cheatsheet §10g).

**Inciampi del 2026-10-20** (prova `2025-01-08`, mappa a 32 bit):

| Regola | Come | Esempio fatto |
|---|---|---|
| **Fine di un blocco** | primo fuori = inizio + taglia; **fine = primo fuori − 1** (si conta da 0) | `40000000h + 20000000h = 60000000h` → fine `5FFFFFFFh` |
| **Blocco in alto** (RAM) | fine = `FFFFFFFFh`; **inizio** = `FFFFFFFFh − taglia + 1` | 2 GB: `FFFFFFFFh − 80000000h + 1 = 80000000h` |
| **k · 2^n in hex** | k in binario, poi n zeri, poi gruppi da 4 da destra | 3·2^29 = `11` + 29 zeri = `60000000h` |
| **8 cifre sempre** | un indirizzo DLX ha 8 cifre hex: se ne conti 7, ne manca una | `4000000h` → `04000000h` |
| **Ordine dei CS** | prima **tutte le firme** in una tabella (una riga per dispositivo), poi i CS confrontando le righe | idea di Lorenzo, 20/10 |
| **Dove mettere una porta** | prendi un indirizzo **tondo** nel buco libero, scrivi i suoi bit alti, confrontali con le firme: ti fermi al bit che la separa da tutti | buco `64000000h`–`7FFFFFFFh` → `70000000h` = `0111` → `BA31*·BA30·BA29·BA28` |
| **Zona di un CS** | bit del CS + tutti 0 → inizio; bit del CS + tutti 1 → fine. Con 4 bit copre 1 cifra hex, 3 bit 2 cifre, 2 bit 4, 1 bit 8 | `010` → `40000000h`–`5FFFFFFFh` (non `4FFFFFFFh`) |
| **Repliche** | ogni bit che non arriva né al CS né ai piedini del chip raddoppia le copie; lecito solo se la zona del CS contiene solo il chip e spazio libero | EPROM 64 MB, CS su `0110`: 4 copie a `60`/`64`/`68`/`6C000000h` · porta (0 piedini): tutta `7xxxxxxxh` |
| **Formula repliche** | c = bit BA nel CS, blocco 2^k: repliche ⇔ c < 32 − k; zona 2^(32−c); copie 2^(32−c−k) | 64 MB: c = 4, k = 26 → zona 2^28, copie 2^2 = 4 |
| **Mutua esclusione** | per ogni coppia (n·(n−1)/2) un bit affermato in uno e negato nell'altro | 512 MB – 64 MB su BA29 · 64 MB – porta su BA28 |

- unità persa ancora: «512 MB → 9·3 = 27», «64 MB → 2^6». Gli esponenti di numero e unità si
  **sommano** (2^9 · 2^20 = 2^29), e M vale 2^20, non 10^6;
- **2 GB = 2048 MB**, non 2000: è già una potenza di due (2^31), non si scompone;
- `FFFFFFFFh − taglia + 1` dà l'**inizio**, non la fine, del blocco in alto;
- prestito: la prima cifra ≠ 0 scende di 1, gli zeri a destra diventano F; riporto: si porta
  **1** a sinistra, non 16.

**Inciampi del 2026-10-23** (prova `2023-12-21`, memorie, guidata):

| Regola | Come | Esempio fatto |
|---|---|---|
| **+1 in esadecimale** | come in decimale, ma trabocca la **F**: F + 1 = 0 con riporto, che scorre su tutte le F | `7FFFFFFFh + 1 = 80000000h` |
| **Valore dei bit di firma** | prendi l'**inizio** del blocco, converti in binario le sole cifre che contengono la firma (1ª cifra = BA31..BA28, 2ª = BA27..BA24, 3ª = BA23..BA20), leggi i bit sotto i nomi; controprova sulla fine | 8 MB a `40000000h`: `0100 0000 0` → `/BA31·BA30·/BA29·…·/BA23` |
| **Prima le porte, poi semplifichi** | scegli un indirizzo tondo nel buco per ogni porta; il CS da semplificare tiene i bit in cui **lui** e **la porta** differiscono | 8 MB `4…` vs INPUT_0 `5…` (BA28) e INPUT_1 `6…` (BA29) → `/BA31·BA30·/BA29·/BA28` |
| **Perché un CS semplificato «invade»** | il CS è una AND sui suoi fili: non sa quanto è grande il chip, si accende su ogni indirizzo che ha quei bit → repliche | `/BA31·BA30` si accende anche su `50000000h` |
| **CS di un banco** | niente da calcolare: CS del blocco **· BEi** | `CS_EPROM1GB_0 = BA31*·BA30*·BE0` |
| **Piedini** | k piedini (banco 2^k), fili **da BA2**: `A[k−1..0] ← BA[k+1..2]` (ultimo BA = piedini + 1); controprova: piedini + CS + BA1–0 = tutti i fili | 2 MB: `A[20..0] ← BA[22..2]` (non `BA[21..2]`: 20 fili per 21 piedini) |
| **RD/WR** | va scritto nelle connessioni: EPROM solo `MEMRD`, RAM `MEMRD` e `MEMWR` | soluzione 2023-12-21 pp. 5–7 |
| **Due porte mutuamente esclusive** | la soluzione le mette **allo stesso indirizzo** (`CS_INPUT·ACTIVE_0` / `·ACTIVE_0*`): moduli 04–05 | soluzione 2023-12-21 p. 2 |

**Dai range ai CS** *(esercizio 10, pomeriggio del 2026-10-09: procedura fatta in sessione)*

| Passo | Come | Esempio (esercizio 10) |
|---|---|---|
| **1. Estremi in binario** | primo e ultimo indirizzo, **a gruppi di 4** (16 bit = 4 cifre hex), sotto `A15 … A0` | `2000h` = `0010 0000 0000 0000` · `27FFh` = `0010 0111 1111 1111` |
| **2. Firma** | le colonne **uguali** sopra e sotto; vale per tutto il blocco perché è allineato | RAM_2: `A15..A11` = `0 0 1 0 0` |
| **3. Verifica** | i bit che cambiano = esponente della taglia = **piedini** del chip | 11 bit, 2K = 2^11 ✓ |
| **4. CS** | dalla firma, solo i bit che separano il chip da **ciascun altro chip presente** (EPROM compresa); un bit di cella non entra mai | `CS_RAM_1 = A15*·A13*`: `A15*` contro la EPROM, `A13*` contro RAM_2/3 |
| **5. Repliche** | un bit di firma omesso fa rispondere il chip anche altrove: lecito solo se lì non c'è nessun altro chip | `CS_EPROM = A15` → attiva su `8000h–FFFFh`, chip solo su `C000h–FFFFh` |

Inciampi: `2000h` scritto con 14 bit e `7` → `1001` (è 9) — scrivere sempre 4 bit per cifra con i
pesi 8-4-2-1; `CS_RAM_1` ridotto ad `A13*` confrontando solo le RAM (domanda di Claude mal posta, notata da
Lorenzo) — controllare il CS contro **tutti** gli altri chip.

## 0b. Il foglio d'esame in quattro riquadri *(2026-10-22)*

1. **Dati** dal testo + fissi del DLX (32 bit, 4 banchi, BA1–0 → BE, EPROM solo RD).
2. **Linea degli indirizzi** a mano: 16 tacche = prima cifra hex; blocchi, buco, porte.
3. **Tabella della risposta**, una riga per blocco, colonne da sinistra a destra:
   `blocco | taglia 2^n | inizio–fine | firma | CS blocco | banco 2^k | A[k−1..0] ← BA[k+1..2] | WR?`;
   poi 4 righe `CS_…_i = CS · BEi` e banco i su `BD[8i+7..8i]`.
4. **Controlli**: somme, 8 cifre, bit che cambiano = esponente, CS a coppie, repliche in zone libere.

Esempio riempito: artefatto «Prova DLX 8 gennaio 2025», sezione «Su carta»
(https://claude.ai/artifact/5iHgc8vnP9dtjop3fQ8j3w).

## 1. Procedura d'esame

La sequenza di decisioni dal testo all'elaborato, consegne a), b), c). Un passo per riga, al suo
posto; ogni passo cita la lezione che lo ha introdotto.

1. **Memorie** *(lezione 02)*. (a) Scomponi ogni taglia in potenze di due. (b) EPROM dal blocco
   più grande in su a partire da `0`, RAM in alto fino a `FFFFFFFFh`; controlla l'allineamento
   (base multipla della taglia). (c) Tabella «nome · range · 4 banchi da taglia/4». (d) Per ogni
   blocco il *chip-select* minimo che lo distingue da **tutti i dispositivi presenti**, porte
   comprese, più `·BEi` per banco. (e) Banco da 2^k byte: `A[k-1..0]` ← `BA[k+1..2]`; banco *i* su
   `BD[8i+7..8i]`. (f) Verifica la mutua esclusione dei CS a coppie.

## 2. Notazione del docente

Forme da riprodurre identiche nell'elaborato (espressioni di decodifica, segnali, range, codice).

| Cosa | Forma del docente | Fonte |
|---|---|---|
| prodotto, negazione | `BA31*·BA30·BE0` (`·` e `*` postfisso) | soluzione 2025-01-08 p. 3 |
| tabella memorie | `RAM  80000000h:FFFFFFFFh, 4 banchi da 512 MB` | soluzione 2025-01-08 p. 2 |
| nome dei CS per banco | `CS_EPROM_1GB_0` … `_3`, `CS_RAM_0` … `_3` | soluzione 2025-01-08 p. 3 |
| comando con verso | `… ·MEMWR` / `… ·MEMRD` in coda | dispensa 02 p. 47 |
| collegamenti banco | `BA[30..2]` → `A[28..0]`; RAM: `RD WR CS`; EPROM: `RD CS` | soluzione 2025-01-08 pp. 9–12 |

## 3. Criticità ricorrenti

Quelle che le soluzioni ufficiali segnalano, con la prova da cui provengono.

- Due driver 3-state sullo stesso filo: mai OE attivi insieme → CS mutuamente esclusivi (dispensa 02 p. 6).
