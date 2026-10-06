# CALC — indice delle prove d'esame

> Redatto il 2026-10-06 dall'archivio `Prove_esame-20260914.zip` del docente, scompattato qui
> (lo zip è stato rimosso: i 108 PDF ne sono il contenuto integrale, e resta nella storia git).
> Nomi uniformati a FI2: `AAAA-MM-GG-Testo.pdf`, `AAAA-MM-GG-Soluzione.pdf`.

## Consistenza

- **62 testi** (gennaio 2015 – settembre 2025), **46 con soluzione ufficiale**.
- Senza soluzione: 2019-06-08, 2019-09-05, 2020-06-16, 2020-07-14, 2020-09-01, 2021-07-08,
  2021-09-02, 2022-06-15, 2023-06-15, 2023-07-12, 2023-09-07, 2024-02-07, 2024-06-19,
  2025-06-19, 2025-07-03, 2025-09-04 — in pratica gli appelli estivi e autunnali.
- Appelli di dicembre presenti: 2017-12-22, 2018-12-21, 2019-12-19, 2021-12-23, 2022-12-23,
  2023-12-21. **Nessuno nell'archivio cade prima del 19 dicembre.**

## Tipologia — una sola, invariata in undici anni

Ogni testo pubblicato contiene **un unico esercizio di progetto** di un sistema basato sul DLX,
con le stesse tre consegne:

- **a)** descrizione sintetica: dispositivi, indirizzi, segnali di *chip-select*;
- **b)** progetto: espressioni di decodifica, *range* di indirizzi di memorie e periferiche,
  collegamenti ai bus, criticità;
- **c)** codice dell'*interrupt handler* (formula ricorrente: «R20–R25 non vanno ripristinati»).

Varia solo il caso. Gli ingredienti ricorrenti, contati sui 62 testi:

| Ingrediente | Testi |
|---|---|
| EPROM agli indirizzi bassi + RAM agli alti, tagli non potenze di 2 (es. 1032 MB, 1600 MB) | 62 |
| porte di I/O a 8 bit con protocollo di *handshake* | 49 |
| rete logica richiesta esplicitamente («soluzioni puramente software non valide») | 13 |
| dati *signed* / estensione del segno | 16 |
| trasferimenti a *word* o *half-word* composti da più porte a 8 bit | 10 |
| LED | 10 |
| contatori / temporizzazione | 8 |
| porte da abilitare in modo **mutuamente esclusivo**, cicli di trasferimenti alternati | 7 |

> Le «domande di carattere generale» della scheda non compaiono nei testi pubblicati: o sono
> somministrate a parte, o non sono più in uso. **Da verificare** (moduli 01, 07, 08 dipendono
> da questa risposta per il peso che meritano).

## Moduli che reggono l'esercizio

`02` mapping e decodifica → consegna b · `05` handshake e `04` interruzioni → a, b, c ·
`03` linguaggio macchina → c · `00` reti logiche → le reti richieste dal caso.

## Uso nel ciclo di preparazione

- **Addestramento**: le prove con soluzione, dalle più recenti all'indietro (la formulazione si
  è stabilizzata dal 2019-12).
- **Checkpoint (~2026-11-03)**: `2024-01-19`, a freddo e cronometrata.
- **Riserva per la verifica finale**: `2025-01-29` e `2025-02-12` — non si aprono prima.
