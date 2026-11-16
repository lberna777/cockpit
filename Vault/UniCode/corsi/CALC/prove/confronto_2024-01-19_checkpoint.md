# Confronto — checkpoint CALC, prova 2024-01-19, parte memorie (16/11/2026)

Svolta 11:45–12:54 (~70 min) con la chat dei dubbi; 27 interventi annotati in
`stato/giornata.md` del 16/11 (circa 20 a livello «domanda», 7 a livello «idea»).
Fonte del confronto: `2024-01-19-Soluzione.pdf`, pagine 1–2.

| Punto | Lorenzo (risultato finale) | Docente | Esito |
|---|---|---|---|
| EPROM 520 MB | 512 MB + 8 MB (dopo aiuto: non è potenza di 2) | idem | ✅ con aiuto |
| EPROM_512 | 00000000h–1FFFFFFFh | idem | ✅ |
| EPROM_8 | 20000000h–207FFFFFh (dopo aiuto su dimensione vs inizio) | idem | ✅ con aiuto |
| RAM | 80000000h–FFFFFFFFh | idem | ✅ |
| CS EPROM_512 | BA31*·BA30*·BA29*·BEi | idem | ✅ da solo |
| CS EPROM_8 | firma completa BA31..BA23 (dopo aiuto su BA23) | **BA31*·BA30*·BA29·BEi** (decodifica semplificata) | ⚠️ giusta ma non minima |
| CS RAM | BA31·BEi (dopo aiuto: firma sui bit, non sulle cifre) | idem | ✅ con aiuto |
| Banchi | 4×128 MB, 4×2 MB, 4×512 MB | idem | ✅ da solo |
| Banco scelto da | BE0..BE3 (nome dato dal tutor) | idem | ❌ non ricordato |
| Piedini | BA2..BA28, BA2..BA22, BA2..BA30 (due errori di conto corretti) | idem | ✅ con aiuto |
| OE/WE | MEMRD→OE, MEMWR→WE, EPROM senza WE (dopo schema) | idem | ❌ non ricordato (come il 5/11) |
| Bus dati | BD0–7, 8–15, 16–23, 24–31 (un errore di conto corretto) | idem | ✅ con aiuto |
| Porte | IN0 30000000h, IN1 40000000h, OUT 50000000h | IN0 40000000h, IN1 40000001h, FREEZE 40000002h | fuori perimetro (04–05) |

## Le due differenze che contano

1. **Decodifica semplificata.** Il docente usa la firma più corta che distingue un blocco dagli
   altri *presenti nella mappa*: per EPROM_8 bastano BA31*·BA30*·BA29, perché tra 20000000h e
   3FFFFFFFh non c'è nient'altro. Lorenzo ha scritto la firma completa (giusta ma più lunga). Con
   le sue porte a 30000000h la firma corta non bastava: la scelta degli indirizzi delle porte
   decide quanto si può semplificare.
2. **Porte in input sullo stesso indirizzo di parola.** Il docente mette IN0 e IN1 a byte
   adiacenti (40000000h/40000001h, BE0/BE1), così una sola lettura a 16 bit le prende entrambe:
   è il requisito del testo. Da riprendere con i moduli 04–05.

## Esito

Mappa e struttura finali corrette, nessun errore di sostanza nel risultato. **Non è a freddo**:
BE e collegamenti OE/WE non ricordati (gli stessi del 5/11), più errori di conto sulle potenze di
2 corretti solo dopo una domanda. Il modulo 02 resta aperto; checkpoint sulla sola parte memorie.
