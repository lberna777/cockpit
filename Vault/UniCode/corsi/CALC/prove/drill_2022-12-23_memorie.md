# Drill 2022-12-23 — memorie (consegne a, b) · 20/11/2026

Svolto da Lorenzo a freddo. Bozza compilata con quanto ricavato fin qui; `__` = ancora da fare.

```
Dispositivi di memoria:

EPROM_1GB     00000000h:3FFFFFFFh, 4 banchi da 256 MB
EPROM_512     40000000h:5FFFFFFFh, 4 banchi da 128 MB
RAM_512       A0000000h:BFFFFFFFh, 4 banchi da 128 MB
RAM_1GB       C0000000h:FFFFFFFFh, 4 banchi da 256 MB

Porte:        60000000h  (da progettare: pezzi P4–P6)

Segnali di decodifica:

CS_EPROM_1GB_i = BA31*·BA30*·BEi          i = 0..3
CS_EPROM_512_i = BA31*·BA30·BA29*·BEi     (BA29 resta: a 60000000h ci sono le porte)
CS_RAM_512_i   = BA31·BA30*·BEi           (BA29 tolto: 80000000h–9FFFFFFFh è libero)
CS_RAM_1GB_i   = BA31·BA30·BEi
```

## Ricavato

- Mappa: da solo, giusta (1536 MB = 1 GB + 512 MB; blocco da 1 GB per primo in basso, in cima in alto).
- Firme: 3/4 da solo; EPROM 512 senza `BA29*` (fermato a due bit), corretta.
- Semplificazione: RAM 512 da solo; EPROM 512 corretta dopo aver visto dove vanno le porte.

## Confronto con la soluzione

| Riga | Lorenzo | Soluzione | Esito |
|---|---|---|---|
| EPROM_1GB | 00000000–3FFFFFFF, 4×256 MB, `BA31*·BA30*·BEi` | uguale | ✅ |
| EPROM_512 | 40000000–5FFFFFFF, 4×128 MB, `BA31*·BA30·BA29*·BEi` | uguale | ✅ (dopo correzione di `BA29*`) |
| RAM_512 | A0000000–BFFFFFFF, `BA31·BA30*·BEi` | `RAM_512_L`, uguale | ✅ |
| RAM_1GB | C0000000–FFFFFFFF, `BA31·BA30·BEi` | divisa in `RAM_512_H` (E0000000–FFFFFFFF, `BA31·BA30·BA29`) e `RAM_512_M` (C0000000–DFFFFFFF, `BA31·BA30·BA29*`), banchi da 128 MB | ✅ equivalente: la soluzione usa un solo tipo di chip per tutta la RAM |
| Taglie banchi RAM | 256 e 128 (ultime due righe scambiate) | 128 e 256 | ❌ svista d'ordine: taglia del banco = taglia del blocco / 4 |
| Porte | 60000000h | 60000000h | ✅ |

