# Drill 2022-12-23 — memorie (consegne a, b) · 20/11/2026

Svolto da Lorenzo a freddo. Bozza compilata con quanto ricavato fin qui; `__` = ancora da fare.

```
Dispositivi di memoria:

EPROM_1GB     00000000h:3FFFFFFFh, 4 banchi da __ MB
EPROM_512     40000000h:5FFFFFFFh, 4 banchi da __ MB
RAM_512       A0000000h:BFFFFFFFh, 4 banchi da __ MB
RAM_1GB       C0000000h:FFFFFFFFh, 4 banchi da __ MB

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

Alla fine, riga per riga.
