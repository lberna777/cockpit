---
tags: [CALC, guida-lab]
---

# Scheda — CALC 02: prova del 17/01/2023, parte memorie (chiusura a freddo)
**Materiale**: `prove/2023-01-17-Testo.pdf` (poi `2023-01-17-Soluzione.pdf`) · **Modalità**: compito, a freddo
**Teoria che entra qui**: [[lezione_02_mapping_decodifica]] · foglio in 4 riquadri del [[prontuario_CALC]] §0b

> Il 23/10 la `2023-12-21` è stata svolta **guidata**: non chiude il 02 (`CLAUDE.md` §7.2).
> Questa prova è nuova, non è il checkpoint (`2024-01-19`) né una riserva (`2025-01-29`, `2025-02-12`).

## Il testo (solo la parte che serve)
> Progettare un sistema, basato su un processore DLX nel quale sono presenti **quattro porte in
> input** (INPUT_PORT_0 … INPUT_PORT_3) e **una porta in output** (OUTPUT_PORT). Tutte le porte
> sono a 8 bit […]. Il sistema dispone anche di una memoria **EPROM pari a 1280 MB, mappata nella
> parte bassa** dello spazio di indirizzamento, e **2 GB di RAM mappata nella parte alta**. […]
> b) Progettare il sistema indicando le espressioni di decodifica e il range di indirizzi di tutte
> le periferiche, le memorie e i segnali e le connessioni di tutti i dispositivi con i bus di sistema.

**Cosa consegni** (porte, reti e handler dopo le lezioni 03–05: qui solo **memorie**; le porte
solo come «zona occupata», con indirizzi tondi nel buco):
1. tabella dei dispositivi: nome, range, «4 banchi da …»;
2. CS di ogni banco (`CS_…_i = … · BEi`), semplificati senza toccare le porte;
3. per ogni blocco: `A[..] ← BA[..]`, banco i su `BD[8i+7..8i]`, **RD/WR**.

## Setup
- un foglio vero, una penna, cronometro avviato: **60 minuti**;
- chiusi: lezione, artefatto dell'8/01, prontuario, soluzione, la prova del 21/12. Aperto solo il testo.

## Il foglio
① dati · ② linea degli indirizzi (16 tacche) · ③ tabella della risposta colonna per colonna ·
④ controlli.

## Condizioni
- nessun aiuto in chat durante; se ti blocchi, Claude ti dice solo **in quale riquadro e colonna
  sei e cosa ti chiede** quella colonna, mai il valore, e annota il punto (il lab resta valido
  per la chiusura solo se l'aiuto è stato di questo tipo);
- a fine tempo: scrivi in chat la tua tabella (o una foto), poi si apre la soluzione;
- confronto: Claude segna errori di sostanza (chiude il 02 se non ce ne sono, `CLAUDE.md` §7.2).

⚠️ Dai tuoi errori: unità M (+20) e G (+30) all'esponente; indirizzi sempre a **8 cifre**;
fine = inizio + taglia − 1, e il +1 esadecimale col riporto sulle F; somma della scomposizione da
ricontrollare; la firma si chiude solo quando il CS non copre nessun altro dispositivo, porte
comprese; piedini: conta i fili dei due lati; RD/WR non va dimenticato.
