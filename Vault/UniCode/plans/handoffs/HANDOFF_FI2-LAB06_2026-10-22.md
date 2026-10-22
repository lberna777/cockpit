# Handoff — FI2 LAB06 MasterMind (chiuso) · 2026-10-22

- **Chat**: gruppo Studio · cockpit — «Studio · cockpit — FI2 LAB06 scheda», sessione
  `session_013mHJ4gAf7nyPeoQU4294Ub`, chiusa al 50% del contesto
- **Repo e ramo**: `lberna777/cockpit`, `claude/wizardly-lovelace-82vhzz` (tutto anche su master)

## Obiettivo
Svolgere il LAB06 di FI2 (MasterMind) fino ai test verdi, costruendo in chat la procedura d'esame
che Lorenzo aveva chiesto il 5/10.

## Fatto
- **LAB06 chiuso il 22/10**: 34/34 test verdi (verificati anche nel cloud con `javac` + JUnit 5),
  guidato. Codice in `Vault/UniCode/corsi/FI2/esame_FI2/svolti/LAB06_MasterMind/` (copia di
  `da_importare/LAB06_MasterMind-191026`, dove Lorenzo lavora direttamente dentro la repo).
- `svolti/LAB06_MasterMind/confronto_LAB06.md`: 12 punti mio/docente + *Cosa porto via*.
- Scheda `corsi/FI2/lezioni/guida_lab_LAB06_mastermind.md` (19/10).
- **Procedura d'esame** nel prontuario `corsi/FI2/appunti/prontuario_FI2.md` §2; nuova §3.14 (LAB06);
  §1 con 12 righe di errori incontrati (messaggi verificati con ecj 3.38 e JUnit). `/chiudi` del
  21/10 fatto; quello del 22/10 **non ancora**.
- `profilo/errori.md`: righe del 21/10 (pattern 1 e 6 + 5 righe FI2) dall'agente di revisione.
- **Sistema**: `Vault/UniCode/scripts/giornata_laptop.sh` (timer serale del laptop: pull → consolida
  → commit e push) e `invia_lavoro_laptop.sh` (timer ogni 5 min: invia `corsi/*/esame_*`), installati
  da Lorenzo come unità systemd utente `unicode-giornata` (override) e `unicode-invia`. Pull ora con
  merge; in conflitto `merge --abort`.
- Stato aggiornato: `stato/corrente.md` (LAB06 ✅, punto di ripresa LAB07), `stato/giornata.md`
  (marcatore `CHIUSO FI2 LAB06`), Plancia (`fi2-lab` fatto, diario).

## Decisioni prese da Lorenzo
- Lavora **dentro la repo** (`da_importare/…`), non nel workspace di Eclipse: Claude legge il codice
  da GitHub via l'invio automatico.
- Procedura: **tutti i campi prima del costruttore**; poi i metodi che **cambiano** lo stato, poi
  quelli che lo leggono. All'esame struttura dall'UML e promesse dalla SEMANTICA: il tempo va su
  confini, casi limite e formati.
- Vuole trovare i bug **da solo** quando lo dice: Claude dà il metodo (stampe vs tabella a mano), non
  la correzione.
- Oculista e tricologa senza data: li chiama in un giorno a casa.

## Ancora aperto / poco chiaro
- `/chiudi` del 22/10 da fare (giudizio della giornata, revisione errori, prontuario: `this`
  parametro/campo, `Random`/`values()[n]`, `Arrays.fill`/`equals`, *for each*, due cicli con estremi,
  `#` = `protected` e classe anonima; pianificazione del 23/10).
- **Causa del blocco dell'invio automatico** (chat Infrastruttura, non studio): sul laptop
  l'automatismo di fine sessione di Claude Code scrive `Vault/UniCode/log/2026-10.md` senza fare
  commit; il pull poi rifiuta («Le tue modifiche locali… sarebbero sovrascritte»). Inoltre il
  21/10 `scripts/cloud_autosave.sh` ha committato su master marcatori di conflitto in
  `stato/giornata.md` e `log/2026-10.md` (ripuliti a mano).
- CALC: la lezione 02 non si è chiusa né il 21 né (finora) il 22/10; calendario CALC indietro.
- Lorenzo fatica sui «processi interni alle funzioni» (situazione, cicli con due spazi di indici):
  gli serve il caso a mano prima del codice.

## Prossimo passo esatto
Oggi (22/10, dalle 15:52): **CALC lezione 02 dal passo 8 dell'artefatto
https://claude.ai/artifact/5iHgc8vnP9dtjop3fQ8j3w** (piedini, bus dati, interfacciamento, Decisione
3) — in una chat CALC, non in questa. Poi `/chiudi` del 22/10. Per FI2 la prossima voce è
`/lab FI2 LAB07` (MyCalendar), con la procedura del prontuario §2 partendo dall'UML.

## Da leggere per primi
1. `Vault/UniCode/stato/corrente.md` (righe in testa + sezione FI2 «Prossimo passo esatto»)
2. `Vault/UniCode/stato/giornata.md` (righe del 22/10)
3. `Vault/UniCode/corsi/FI2/esame_FI2/svolti/LAB06_MasterMind/confronto_LAB06.md`
4. `Vault/UniCode/corsi/FI2/appunti/prontuario_FI2.md` §2 (procedura) e §3.14

## Concetti assimilati
- Contratto da test e UML; campi come «cosa deve ricordarsi l'oggetto»; ciò che si calcola non è un
  campo. `toString` restituisce, non stampa. `StringJoiner` (separatore solo fra) contro
  `StringBuilder` (a capo anche in fondo). Enum: `ordinal()` e `values()[n]`.
- Algoritmo di MasterMind: neri per posizione, occorrenze per colore, minimi, bianchi = totale − neri;
  la risposta dice quanti, non dove.
- Debug: stampe contro tabella a mano, la prima riga che diverge indica il punto.

## Ancora poco chiaro
- `this`: quando serve (solo se parametro e campo hanno lo stesso nome) — spiegato, da consolidare.
- Estremi dei cicli e degli intervalli (`dim − 1`, `nextInt(n)` esclusivo, prima libera / ultima
  piena): sbagliati più volte, pattern trasversale 6.
- Quale «spazio» scorre un ciclo (posizioni o colori) — pattern 1.
