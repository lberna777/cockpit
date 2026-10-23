# Handoff — CALC lab 02 (prova 2023-12-21), 23/10/2026

- **Chat**: Studio · cockpit — sessione CALC lezione 02 · sessione `session_01LPmufQWXoXrp38YK2XX2bj`
- **Repo / ramo**: `lberna777/cockpit` · `claude/sleepy-tesla-wlmyle` (allineato con master)

## Obiettivo
Chiudere il modulo CALC 02 «Mapping e decodifica»: lezione sulla prova 8/01/2025 (fatta 20–22/10),
poi lab sulla parte memorie della prova 21/12/2023.

## Fatto
- Lezione 02 finita il 22/10: mappa, firme, CS, repliche, mutua esclusione, banchi/BE, piedini
  `A[k−1..0] ← BA[k+1..2]`, bus dati. Stato in `stato/corrente.md` (sezione CALC).
- Artefatto «Prova DLX 8 gennaio 2025» https://claude.ai/artifact/5iHgc8vnP9dtjop3fQ8j3w
  (sorgente `corsi/CALC/appunti/prova_2025-01-08_svolta.html`): dati/incognite, foglio su carta in
  4 riquadri, mappa della memoria cliccabile, vista «filo per filo», schema del sistema, 10 passi ↔
  soluzione ufficiale.
- Prontuario CALC §0 (inciampi 20/10, regole CS/repliche/formula) e §0b (foglio in 4 riquadri);
  cheatsheet §1a; lezione 02 corretta (estratto con i CS per banco).
- Scheda del lab: `corsi/CALC/lezioni/guida_lab_02_prova_2023-12-21.md` (avviato alle 14:23 del 23/10).
- FI2 LAB06 chiuso il 22/10 (altra sessione), nel tracker.

## Decisioni di Lorenzo
- 23/10: il lab sulla 2023-12-21 lo fa **con l'artefatto dell'8/01 aperto** → è un esercizio
  **guidato**, non chiude il 02. La chiusura a freddo si sposta a un'altra prova (proposta: 2024-01-19,
  quella del checkpoint ~10 nov). Si può aiutarlo di più che con la sola domanda del riquadro.
- 23/10: giornata solo CALC; altro solo se avanza tempo.
- Sicurezza dichiarata 1/5 sulla tabella della risposta; fatica su «dove mi muovo, cosa cerco, cosa so»
  e sulla comprensione fisica → lavorare con il foglio in 4 riquadri e l'artefatto.

## Dove eravamo nel lab (riquadro ③, colonna range)
- Scomposizione fatta da lui: 1032 MB = 1024 + 8 MB = 2^30 + 2^23 ✓.
- EPROM 1 GB: `00000000h–3FFFFFFFh`, primo libero `40000000h` ✓ (da lui).
- 2^23 in hex: `800000h` → ricordato di scriverlo a 8 cifre, `00800000h`.
- **Domanda aperta a Lorenzo**: il blocco da 8 MB inizia a `40000000h`: dove finisce? (atteso:
  primo fuori `40800000h`, fine `407FFFFFh`; non dirglielo, farlo calcolare).

## Concetti assimilati
Scomposizione con le unità (M = +20), 2^n in hex a 8 cifre, firma → CS, banchi = blocco/4, piedini
da BA2 (vista filo per filo), ogni byte avanti cambia banco.

## Ancora poco chiaro
Muoversi nella memoria senza appoggio visivo; legame banchi–BE–CS a metà; porte e RESET_P (moduli 04–05).

## Prossimo passo esatto
Far calcolare a Lorenzo la fine del blocco EPROM 8 MB (`40000000h + 00800000h − 1`), poi RAM 2 GB in alto
(`80000000h–FFFFFFFFh`), poi firme e CS (attenzione: 8 MB ha firma lunga 9 bit `BA31..BA23`; CS
semplificato contro RAM e porte nel buco `40800000h–7FFFFFFFh`), banchi (256 MB, 2 MB, 512 MB),
piedini (`A[27..0]←BA[29..2]`, `A[20..0]←BA[22..2]`, `A[28..0]←BA[30..2]`), controlli. Poi confronto con
`prove/2023-12-21-Soluzione.pdf`, voce in `stato/giornata.md` (guidato, non CHIUSO), `/chiudi` (blocco 14:00 in Plancia).

## Da leggere per primi
1. `Vault/UniCode/corsi/CALC/lezioni/guida_lab_02_prova_2023-12-21.md`
2. `Vault/UniCode/stato/corrente.md`, sezione CALC
3. `Vault/UniCode/stato/giornata.md` (righe del 23/10)
4. `Vault/UniCode/corsi/CALC/appunti/prontuario_CALC.md` §0b
