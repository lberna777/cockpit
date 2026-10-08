# CLAUDE.md — ~/cockpit (base di lancio)

Questa è la **cartella base** da cui lanciare Claude Code. Da qui ti muovi liberamente
nei progetti via i symlink. I CLAUDE.md dei singoli progetti si attivano on-demand quando
entri nei loro sottoalberi.

---

## Memoria persistente

La memoria vive in `~/cockpit/Vault` ed è **iniettata automaticamente** a ogni avvio dal
SessionStart hook (`scripts/memory_inject.sh`) — non devi fare nulla per "caricarla", è già
in contesto. L'hook inietta un artefatto compatto: l'indice del vault + gli ultimi recap.

- **Ricerca nel vault**: usa `rg` (ripgrep) dentro `~/cockpit/Vault`. È il motore di ricerca
  della memoria (deciso dal bake-off G3: `Vault/claude/graphify_bakeoff.md`).
- **Indice**: `Vault/index.md` (rigenerabile con `python3 scripts/build_index.py`).
- **Recap giornalieri**: `Vault/recap/YYYY-MM-DD.md` (generati da `scripts/recap_generator.py`,
  consolidati da `scripts/consolidate_recaps.py`).
- **Note curate per Claude**: `Vault/claude/`.
- **Studio universitario**: `Vault/UniCode` (la cartella reale; `~/UniCode` è il symlink).

### Confine con l'auto-memory di Claude (`~/.claude/.../memory/`)
- **Auto-memory** (`MEMORY.md` + frontmatter): chi è l'utente, preferenze, stato progetti —
  fatti curati che Claude scrive su di sé. Per la continuità di Claude.
- **Vault** (`~/cockpit/Vault`): corpus di conoscenza — studio, recap di attività, reference.
  Per il lavoro.
- Regola: preferenze/profilo/stato → auto-memory; corpus/attività/studio → vault. Non duplicare.

---

## Mappa del territorio

Riordinata il 2026-09-01, rivista il 2026-09-14.

> **Lo studio si apre da `~/UniCode` oppure da qui** (deciso da Lorenzo il 2026-10-01: cockpit
> è la cartella sempre aggiornata e la sola che il cloud clona). Da cockpit valgono gli stessi
> automatismi di UniCode, registrati in `.claude/settings.json`:
> - **avvio**: `scripts/unicode_session_start.sh` inietta il briefing di UniCode (nel cloud,
>   prima, `scripts/cloud_bootstrap.sh`: symlink `~/cockpit` e `~/UniCode`, merge dei rami
>   `claude/*` di studio più recenti non ancora in master, consolidamento arretrato);
> - **fine sessione**: `scripts/unicode_session_end.sh` scrive la traccia in `log/AAAA-MM.md`
>   solo se la sessione ha toccato lo studio — le sessioni di codice non contano come giornate;
> - **cloud**: `scripts/cloud_autosave.sh` committa e invia il Vault dopo ogni modifica (`PostToolUse`) e a fine risposta (`Stop`),
>   sul ramo di sessione **e su master** (solo fast-forward; se master è andato avanti lo
>   unisce prima, in conflitto si ferma e avvisa): ciò che Claude crea nel cloud arriva sul laptop
>   e in Obsidian con un `git pull` (richiesta di Lorenzo del 2026-10-01). Rischio da ricordare:
>   un consolidamento serale del laptop non ancora inviato diverge su `log/giornate.md`,
>   `stato/tracker.md`, `log/giornate_dettaglio/` — sul laptop, `git pull` prima di studiare;
> - **progetti Eclipse dal cloud**: in `Vault/UniCode/corsi/FI2/esame_FI2/da_importare/`, da
>   importare con *Existing Projects → Select root directory* + *Copy projects into workspace*;
> - **comandi**: `/lab`, `/chiudi`, `/lezione`… stanno in `.claude/commands` come rimandi agli
>   originali di `Vault/UniCode/.claude/commands`; dopo aver aggiunto o rinominato un comando
>   di UniCode, `python3 scripts/unicode_commands.py`;
> - **fuso**: `TZ=Europe/Rome` in `settings.json`, perché il container cloud è in UTC.
>
> Nei comandi e negli appunti il percorso resta `~/UniCode` (nel cloud è un symlink creato
> all'avvio). Il timer serale di consolidamento esiste solo sul laptop; nel cloud lo sostituisce
> il recupero all'avvio.

- `~/UniCode` — **studio universitario**, cartella di lavoro unica: dodici esami arretrati verso
  la laurea nella sessione estiva 2028. Ha il suo CLAUDE.md e l'architettura di continuità
  installata il 2026-09-02 (memoria a strati, briefing iniettato dal SessionStart hook,
  consolidamento serale via timer systemd). I comandi prendono `<CODICE> <ID modulo>`, es.
  `/lab FI2 LAB02` (per FI2 si lavora sui LAB, non su `/lezione`: vedi `UniCode/CLAUDE.md` §2); i codici stanno in `piano/codici.txt`, il piano per sessioni in
  `piano/piano_laurea.md`. `ARCHIVIO/` contiene il materiale degli esami chiusi.
- `~/Sviluppo` — tutto il codice, diviso per tipo di lavoro:
  - `app/` — accountability-app, agenticdash (dashboard + memoria, Tauri), diritto-quiz-app, bibiciclo
  - `audio/` — StereoCompressor, FreakFM, acidmoog-synth, NEMO, JUCE-shared
  - `giochi/` — Monopoly
  - `tools/` — AgenticOS, claude-code-quest, unicode-ui, UniCode-template, platform-master, cupp
  - `appunti/` — note e piani di sviluppo, non progetti

## Plancia di Lorenzo — tracciamento degli obiettivi

Ogni obiettivo o cosa da fare che Lorenzo fissa — studio, lavoro, musica o qualunque altro
ambito — va registrato **subito e senza chiedere** nella Plancia
(https://claude.ai/artifact/B3QifQTD67G5LZmudWk1u4), con `ArtifactData`; così anche i cambi di
stato. Protocollo e schema: `Vault/claude/plancia.md` (regola di Lorenzo del 2026-10-08).

## Convenzioni globali
- **Lingua**: italiano.
- **Handoff**: a ~75% di contesto usa `/handoff` o `/handoffplan` (vedi `~/Sviluppo/CLAUDE.md`).
- **Skill custom**: `lorenzo-skills` (audio-dsp-debug, game-scope-guard, studia, unicode-output-gate,
  unicode-session-close, unicode-link-note).
- **Recap del giorno**: annota le attività in `Vault/attivita_oggi.md` durante la giornata;
  il recap le raccoglie e poi archivia il file.

## graphify

graphify è installato ma **fuori dal layer memoria** per decisione del bake-off G3
(`Vault/claude/graphify_bakeoff.md`): la ricerca nella memoria si fa con `rg`, non con graphify.

Usalo **solo** dentro un progetto di *codice* che abbia il suo `graphify-out/graph.json`
(es. `graphify query "<domanda>"`, `graphify update .` dopo modifiche). Se `graphify-out/`
non esiste nella cartella corrente, ignora graphify e usa `rg`.

Visualizzazione del vault: la fa **Obsidian** (graph view nativa dei `[[wikilink]]`).
I collegamenti tra le note di studio sono generati da `scripts/link_modules.py`
(deterministico, rigenerabile; `--strip` per rimuoverli).
