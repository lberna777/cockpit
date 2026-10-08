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
