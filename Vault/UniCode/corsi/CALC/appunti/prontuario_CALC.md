# Prontuario d'esame — CALC

> Cresce a ogni lezione (`/lezione CALC <ID>`, sezione «Passo di procedura»). Si porta alla prova
> del checkpoint (~3 nov) e si rifinisce sul ciclo delle prove. Notazione: quella del docente.

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
