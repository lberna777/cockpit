---
tags: [CALC, lezione]
---

# Lezione — CALC 02: Mapping e decodifica delle memorie
**Corso**: Calcolatori Elettronici T
**Materiale**: dispensa *02 Mapping e decodifica* (Mattoccia, ed. 2024/25; pagine citate come
numero di pagina del PDF) · prova `2025-01-08`, testo e traccia di soluzione ufficiale
**Prerequisiti**: reti logiche combinatorie (decoder, AND di letterali) — modulo `00`, da aprire
solo se qui qualcosa non torna
**Consegna servita**: **a)** la tabella di dispositivi, indirizzi e *chip-select*; **b)** la parte
memorie: espressioni di decodifica, *range*, collegamenti di `BA` e `BD` ai banchi

> Annata: dispensa 2024/25, scheda 2025/26; nessuna differenza di programma rilevata (`fonti.md`).

---

## Obiettivo
Dato il testo della prova («N MB di EPROM agli indirizzi bassi, M GB di RAM agli indirizzi
alti»), saper scrivere senza esitazioni la prima metà della soluzione: dove sta ogni memoria,
in quanti banchi si divide, con quale espressione si seleziona ciascun banco, e quali bit di
indirizzo arrivano ai suoi piedini.

## Decisione 1 — Dove mappare ogni dispositivo: la finestra allineata

Un dispositivo è visibile al software solo se è **mappato**, cioè se gli si associa «una finestra
di indirizzi» dello spazio di indirizzamento, e la CPU comunica con esso «unicamente attraverso
dei cicli di bus» [fonte: p. 7]. La finestra ha due vincoli: la sua dimensione è una potenza di
due e gli indirizzi sono contigui [fonte: p. 34]; un dispositivo da `n = 2^K` byte ha al suo
interno un decoder di II livello a K variabili [fonte: pp. 35–36].

Il vincolo che governa la decisione è l'**allineamento**: D è allineato se l'indirizzo più basso
A è multiplo di n, «(indirizzo più basso di D) MOD n = 0», e allora «i k bit meno significativi
di A sono uguali a zero» [fonte: p. 38]. Il perché è tutto qui: se i K bit bassi del blocco sono
liberi, l'indirizzo si spezza in modo pulito in `α ## i`, dove `α` dice *quale* dispositivo e
`i` dice *quale byte dentro* [fonte: p. 39]. Il progettista decodifica solo `α` (I livello,
fuori dal chip); `i` lo decodifica il chip (II livello, dentro) [fonte: p. 39; schema a p. 4].

Conseguenza operativa per la prova. Le taglie del testo spesso **non sono potenze di due**:
1600 MB di EPROM nella prova dell'8/01/2025, 1032 MB in quella del 21/12/2023. La soluzione
ufficiale scompone la taglia in potenze di due e le dispone **dalla più grande alla più piccola**
a partire da 0: 1 GB a `00000000h`, 512 MB a `40000000h`, 64 MB a `60000000h` [fonte: soluzione
2025-01-08, p. 2]. L'ordine non è estetico: ciascun blocco cade così su un multiplo della propria
taglia, e resta allineato. Al contrario, con 64 MB a `0` il blocco da 512 MB partirebbe da
`04000000h`, che non è multiplo di 512 MB.

## Decisione 2 — Quanti banchi: il DLX vede la memoria a 32 bit

Il parallelismo di ciascuna memoria «è sempre 8 bit» [fonte: p. 56]. Per trasferire più byte
nello stesso ciclo di bus si affiancano più memorie, e gli **elementi contigui vanno su memorie
diverse** [fonte: pp. 55–56]. Con un bus dati a 32 bit le memorie vanno a gruppi di quattro: la
cella di indirizzo logico `x` si trova nel banco `x mod 4`, all'indirizzo fisico `x/4` [fonte:
pp. 65, 69]. Il processore **non emette `BA1` e `BA0`**: al loro posto emette `BE3`–`BE0`, che
selezionano i banchi [fonte: pp. 66, 68].

Due conseguenze, che la soluzione d'esame applica ogni volta.
- Ogni blocco logico è fatto di **4 banchi da un quarto** della taglia: la RAM da 2 GB è
  «4 banchi da 512 MB», l'EPROM da 1 GB «4 banchi da 256 MB» [fonte: soluzione 2025-01-08, p. 2].
- Ai piedini di indirizzo dei banchi arriva il bus **a partire da `BA2`**: `BA2` va su `A0`,
  `BA3` su `A1`, e così via [fonte: p. 66]. Un banco da 512 MB = 2^29 byte ha `A[28..0]`,
  collegati a `BA[30..2]`; uno da 16 MB ha `A[23..0]` su `BA[25..2]` [fonte: soluzione
  2025-01-08, pp. 10–12].

⚠️ **Distinzione da tenere separata** (pattern trasversale 1): *indirizzo logico*, quello che vede
il programmatore, e *indirizzo fisico*, quello sui piedini del singolo banco. Il caso che li
separa: i byte `40000000h` e `40000001h` sono contigui per il programma, ma stanno su due chip
diversi, entrambi all'indirizzo interno `00000h` [fonte: p. 69].

## Decisione 3 — L'espressione di *chip-select*: completa o semplificata

La decodifica di `α` è **completa** se usa tutti i bit sopra i K interni, **semplificata** se ne usa
«solo un sottoinsieme (minimo)» [fonte: p. 39]. Con la semplificata il dispositivo compare in più
zone dello spazio logico [fonte: pp. 40–41]. Questo è lecito perché quelle zone non vengono mai
indirizzate dai programmi, e in cambio si ottiene un'«espressione CS più semplice» [fonte: p. 40].
**All'esame si usa la semplificata**: «decodifica completa e semplificata (quella da usare
all'esame)» [fonte: p. 42].

La regola per scegliere i bit: usarne **il minimo che distingue il dispositivo da tutti gli altri
presenti nel sistema**, non da tutti gli indirizzi possibili. L'esempio a 8 bit della dispensa lo
mostra bene: 64 KB di EPROM agli indirizzi bassi in uno spazio da 1 MB si selezionano con
`CS_EPROM = BA19*`, un solo letterale [fonte: p. 47].

La **notazione del docente**, da riprodurre identica: prodotto con `·`, negazione con `*`
postfisso, banco nel suffisso numerico, `BEi` in coda.

```
CS_RAM_0          = BA31·BE0
CS_EPROM_1GB_0    = BA31*·BA30*·BE0
CS_EPROM_512MB_0  = BA31*·BA30·BA29*·BE0
CS_EPROM_64MB_0   = BA31*·BA30·BA29·BA28*·BE0
```
[fonte: soluzione 2025-01-08, p. 3; le altre tre righe di ogni gruppo cambiano solo `BEi`]

Se l'elemento da selezionare è un comando e non una memoria, si aggiunge `MEMRD` o `MEMWR`
[fonte: p. 47]. Torna nel modulo `05`, sulle porte.

⚠️ **Fermarsi al primo indizio** (pattern trasversale 2): un'espressione semplificata «che
sembra giusta» non basta. La verifica consiste nel prendere ogni coppia di *chip-select* e
controllare che non possano essere veri insieme. Il motivo è elettrico: due driver 3-state sullo
stesso filo con OE attivi entrambi danno un valore non significativo. La dispensa lo pone come
domanda: «che cosa è necessario garantire?» [fonte: p. 6, con la tabella di verità del
3-state a p. 5].

## Nella prova — 8 gennaio 2025

**Testo**: «processore DLX dotato di 1600 MB di EPROM mappata agli indirizzi bassi e 2 GB di RAM
mappata agli indirizzi alti», più due porte in input lette insieme a 16 bit [fonte: testo
2025-01-08].

**Ragionamento, nell'ordine delle decisioni**:
1. 2 GB di RAM «agli indirizzi alti»: è la metà superiore dello spazio da 4 GB, cioè
   `80000000h:FFFFFFFFh`. Un solo bit la distingue da tutto il resto: `BA31`.
2. 1600 MB = 1024 + 512 + 64. Disposti dal più grande a partire da 0, danno `00000000h:3FFFFFFFh`,
   `40000000h:5FFFFFFFh` e `60000000h:63FFFFFFh`.
3. Bit per distinguere ciascun blocco: il blocco da 1 GB ha tutti i bit sopra il 30 fissi, cioè
   `BA31*·BA30*`; il blocco da 512 MB ne ha tre, `BA31*·BA30·BA29*`.
4. Il blocco da 64 MB è quello istruttivo. La decodifica completa fisserebbe i bit 31–26:
   `BA31*·BA30·BA29·BA28*·BA27*·BA26*`. La soluzione si ferma a `BA28*`, perché basta a separarlo
   dalla porta mappata a `70000000h`, l'unico altro dispositivo in quella zona. L'EPROM da 64 MB
   compare quindi quattro volte in `60000000h:6FFFFFFFh`: è la decodifica semplificata di p. 40,
   applicata alla lettera.
5. Ogni blocco si divide in quattro banchi selezionati con `BE0`–`BE3`.

**Soluzione ufficiale** (estratto) [fonte: soluzione 2025-01-08, pp. 2–3]:
```
RAM            80000000h:FFFFFFFFh, 4 banchi da 512 MB
EPROM_64_MB    60000000h:63FFFFFFh, 4 banchi da 16 MB
EPROM_512_MB   40000000h:5FFFFFFFh, 4 banchi da 128 MB
EPROM_1GB      00000000h:3FFFFFFFh, 4 banchi da 256 MB
CS_INPUT       = BA31*·BA30·BA29·BA28·BE0·BE1
RESET_P        = BA31*·BA30·BA29·BA28·BE2·MEMWR
```
`CS_INPUT` e `RESET_P` mostrano in anticipo i moduli `04`–`05`. La porta occupa la zona libera
tra 64 MB e 2 GB. Le due porte da 8 bit lette insieme sono una *half-word*, e la selezionano i
due banchi bassi, `BE0·BE1`. Il comando di reset è un byte all'indirizzo `70000002h`, cioè il
banco 2: per questo compare `BE2`.

**Collegamenti** [fonte: soluzione, pp. 10–12]: le RAM ricevono `RD`, `WR` e `CS`, le EPROM solo
`RD` e `CS`. Tutti i banchi condividono `BA[..2]`. Il banco *i* sta su `BD[8i+7..8i]`.

## Passo di procedura

Riportato in `appunti/prontuario_CALC.md` §1:

> **1. Memorie.** (a) Scomponi ogni taglia in potenze di due. (b) Disponi le EPROM dal blocco più
> grande in su a partire da `0`, e la RAM in alto a partire da `FFFFFFFFh` verso il basso;
> controlla l'allineamento (indirizzo base multiplo della taglia). (c) Scrivi la tabella
> «nome · range · 4 banchi da taglia/4». (d) Per ogni blocco, il *chip-select* minimo che lo
> distingue da **tutti i dispositivi presenti**, porte comprese, più `·BEi` per banco. (e) Per
> ogni banco da 2^k byte: `A[k-1..0]` ← `BA[k+1..2]`; banco *i* su `BD[8i+7..8i]`. (f) Verifica
> la mutua esclusione dei CS a coppie.

## Riepilogo

**Perché la soluzione mette l'EPROM da 1 GB a `0` e quella da 64 MB per ultima, e non il
contrario?**
Perché ogni blocco deve cadere su un multiplo della propria taglia (allineamento, p. 38).
Andando dal più grande al più piccolo la condizione è soddisfatta da sola; nell'ordine inverso
il blocco da 512 MB finirebbe a `04000000h`, non allineato.

**Perché `CS_EPROM_64MB` non contiene `BA27*·BA26*`, e cosa succede di conseguenza?**
Perché la decodifica d'esame è quella semplificata (p. 42): bastano i bit che separano il blocco
dagli altri dispositivi presenti, e `BA28*` lo separa dalla porta a `70000000h`. Di conseguenza
il blocco compare quattro volte in `60000000h:6FFFFFFFh`. Questo non crea problemi, perché quella
zona non è usata da nessun altro (p. 40).

**Un banco della RAM da 2 GB: quali bit di `BA` riceve, e perché non `BA0`/`BA1`?**
Riceve `BA[30..2]` sui suoi `A[28..0]`, perché il banco è da 512 MB = 2^29. Il DLX non emette
`BA1` e `BA0`: al loro posto emette `BE3`–`BE0`, che scelgono il banco (pp. 66, 68).

---
*Prossimo passo*: `/lab CALC 02`, in cui svolgi a freddo la parte memorie della prova
`2023-12-21` (1032 MB di EPROM, 2 GB di RAM). Il riscaldamento facoltativo è l'esercizio di p. 42.
