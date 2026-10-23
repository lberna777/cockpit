---
tags: [CALC, guida-lab]
---

# Scheda — CALC 02: prova del 21/12/2023, parte memorie
**Materiale**: `prove/2023-12-21-Testo.pdf` (poi `2023-12-21-Soluzione.pdf`) · **Modalità**: compito, a freddo
**Teoria che entra qui**: [[lezione_02_mapping_decodifica]] · foglio in 4 riquadri del [[prontuario_CALC]] §0b

## Il testo (solo la parte che serve)
> Progettare un sistema, basato su un processore DLX dotato di **1032 MB di EPROM mappata agli
> indirizzi bassi** e **2 GB di RAM mappata agli indirizzi alti**. Nel sistema sono presenti anche
> due porte in input, INPUT_0 e INPUT_1 […] da abilitare in modo mutuamente esclusivo. […]
> a) dispositivi utilizzati, indirizzi e segnali di chip-select;
> b) espressioni di decodifica e range di indirizzi di tutte […] le memorie, e connessioni con i bus.

**Cosa consegni** (le porte si fanno dopo le lezioni 04–05: qui solo **memorie**; le porte, se
vuoi, solo come «zona occupata» con un indirizzo tondo nel buco):
1. tabella dei dispositivi: nome, range, «4 banchi da …»;
2. CS di ogni banco (`CS_…_i = … · BEi`);
3. per ogni blocco: `A[..] ← BA[..]`, banco i su `BD[8i+7..8i]`, RD/WR.

## Setup
- un foglio vero, una penna, cronometro avviato: **60 minuti**;
- chiusi: lezione, artefatto, prontuario, soluzione. Aperto solo il testo.

## Il foglio
① dati · ② linea degli indirizzi (16 tacche) · ③ tabella della risposta colonna per colonna ·
④ controlli. È lo stesso ordine della prova dell'8/01/2025.

## Condizioni
- nessun aiuto in chat durante; se ti blocchi, Claude ti dice solo **in quale riquadro e colonna
  sei e cosa ti chiede** quella colonna, mai il valore, e annota il punto (il lab resta valido
  per la chiusura solo se l'aiuto è stato di questo tipo);
- a fine tempo: scrivi in chat la tua tabella (o una foto), poi si apre la soluzione;
- confronto: Claude segna errori di sostanza (chiude il 02 se non ce ne sono, `CLAUDE.md` §7.2).

⚠️ Dai tuoi errori: unità M (+20) e G (+30) all'esponente, **1 GB = 1024 MB**; indirizzi sempre a
**8 cifre**; fine = inizio + taglia − 1; somma della scomposizione da ricontrollare.
