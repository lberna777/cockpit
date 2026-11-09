---
tags: [CALC, guida-lab]
---

# Scheda — CALC checkpoint del 10/11: prova del 19/01/2024, parte memorie (chiusura a freddo del 02)
**Materiale**: `prove/2024-01-19-Testo.pdf` (poi `2024-01-19-Soluzione.pdf`) · **Modalità**: compito, a freddo, cronometrata
**Teoria che entra qui**: [[lezione_02_mapping_decodifica]] · foglio in 4 riquadri del [[prontuario_CALC]] §0b

> È la prova del checkpoint di sessione (`piano/piano_laurea.md`, regola 1) e insieme la chiusura
> a freddo del 02, dopo la 2023-01-17 del 5/11 non chiusa. Solo la parte memorie: 03–05 non sono
> ancora chiusi, quindi handshake, reti delle porte e handler (consegna c) restano fuori.

## Cosa consegni
(porte, handshake e handler dopo le lezioni 03–05: qui solo **memorie**; le porte solo come
«zona occupata», con indirizzi tondi nel buco)
1. tabella dei dispositivi: nome, range, «4 banchi da …»;
2. CS di ogni banco (`CS_…_i = … · BEi`), semplificati senza toccare le porte;
3. per ogni blocco: `A[..] ← BA[..]`, banco i su `BD[8i+7..8i]`, **RD/WR**.

## Setup
- un foglio vero, una penna, cronometro avviato: **60 minuti**;
- chiusi: lezione, prontuario, soluzione, le prove del 21/12 e del 17/01. Aperto solo il testo.

## Il foglio
① dati · ② linea degli indirizzi (16 tacche) · ③ tabella della risposta colonna per colonna ·
④ controlli.

## Condizioni
- nessun aiuto in chat durante; se ti blocchi, Claude ti dice solo **in quale riquadro e colonna
  sei e cosa ti chiede** quella colonna, mai il valore, e annota il punto;
- a fine tempo: scrivi in chat la tua tabella (o una foto), poi si apre la soluzione;
- confronto: Claude segna errori di sostanza (chiude il 02 se non ce ne sono, `CLAUDE.md` §7.2);
- poi la **decisione sugli esami di S1** (attività `calc-checkpoint` nella Plancia): sotto la
  sufficienza, CALC passa al secondo appello di S1.

⚠️ Dai tuoi errori: unità M (+20) e G (+30) all'esponente; indirizzi sempre a **8 cifre**;
fine = inizio + taglia − 1, e il +1 esadecimale col riporto sulle F; la scomposizione in potenze
di 2 va ricontrollata sommandola; **conta le porte dal testo**, una per una (il 5/11 erano 3 su 4);
**nessuna porta dentro una memoria**: controlla ogni porta contro i range di ① e ② prima di
scrivere i CS (il 5/11 OUT a `80000000h`, dentro la RAM); porte separate con BA27 se le tacche non
bastano, mai con BA1–BA0 (non arrivano sul bus); ogni indirizzo che il testo nomina va
classificato: porta o cella di memoria?; la firma si chiude solo quando il CS non copre nessun
altro dispositivo, porte comprese; RD/WR non va dimenticato.
