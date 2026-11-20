# CALC — la prova divisa in pezzi

> Deciso con Lorenzo il 16/11/2026, dopo il checkpoint sulla 2024-01-19: si resta sul primo
> appello (22/12) e si cambia metodo. La prova si scompone in pezzi, ogni pezzo si allena da
> solo su più prove (solo quel pezzo, 15–20 minuti), poi si ricompone sulle prove intere.
> Base: `prove/INDICE.md` (una sola tipologia in undici anni, consegne a/b/c).

## I pezzi, nell'ordine in cui compaiono nella prova

| # | Pezzo | Consegna | Modulo | Cosa si allena | Stato al 16/11 |
|---|---|---|---|---|---|
| P1 | **Mappa** | a | 02 | tagli non potenze di 2 → blocchi; inizio e fine (inizio + dimensione − 1) | ✅ quasi a freddo (conti sulle potenze di 2 da controllare) |
| P2 | **Decodifica** | a, b | 02 | firma sui bit; **firma minima** rispetto alla mappa; · BE0..BE3 | 🔶 firma ok, semplificazione e BE da fissare |
| P3 | **Collegamenti delle memorie** | b | 02 | banchi, piedini BA2.., BD per banco, MEMRD→OE, MEMWR→WE | 🔶 schema fisso da sapere a memoria |
| P4 | **Indirizzi delle porte** | a | 02 + 05 | porte in zone libere; byte adiacenti della stessa parola per letture a 16/32 bit | ⬜ |
| P5 | **Porta con handshake** | b | 05 | schema della porta in input e in output: CS, RD/WR, STB/IBF, ACK/OBF, INT | ⬜ |
| P6 | **Interrupt** | b | 04 | INT_DLX da combinazione degli INT delle porte; abilitazioni | ⬜ |
| P7 | **Reti di contorno** | b | 00 | FF di sincronizzazione, CS condizionati, contatori, mutua esclusione | ⬜ |
| P8 | **Handler** | c | 03 + 04 | scheletro fisso: base con LHI, letture LBU/LB, scritture, uscita (RFE) | 🔶 lezione 03 fatta |
| P9 | **Varianti** | b, c | 03 + 05 | dati signed (estensione del segno), half-word/word da più porte, LED | ⬜ |

## Come si allena un pezzo

> `[2026-11-20, decisione di Lorenzo]` **Nei drill Claude non fa domande sue.** Dà il testo della
> consegna parola per parola; Lorenzo risponde nella forma della soluzione ufficiale; il confronto
> riga per riga con la soluzione viene alla fine. Le domande inventate allontanano dall'esame.

1. Una scheda di mezza pagina per pezzo, **lo schema fisso** (cosa si scrive sempre uguale) +
   le varianti viste nelle prove. Va nel prontuario (`appunti/prontuario_CALC.md`).
2. Drill: lo stesso pezzo su 3–4 prove diverse con soluzione, dalle più recenti, solo quel pezzo,
   cronometrato. Confronto subito dopo ognuna.
3. Il pezzo è **allenato** quando esce a freddo e senza errori su due prove di fila.
4. Le prove di riserva (`2025-01-29`, `2025-02-12`) non si usano per i drill.

## Calendario verso il 22/12

| Settimana | Pezzi | Note |
|---|---|---|
| 16–22/11 | P1, P2, P3 (drill), P8 base (handler di 03) | in parallelo FI2 LAB09 |
| 23–29/11 | P5, P6 (lezioni 04 e 05), P4 | |
| 30/11–6/12 | P7, P9; **secondo checkpoint ~6/12 su una prova intera** | FI2 checkpoint il 2/12 |
| 7–13/12 | ricomposizione: prove intere dalle più recenti | |
| 14–20/12 | prove di riserva a freddo; 07, 08, 01: **servono** (sbarramento teorico, 20/11) — calendario da rifare | |
