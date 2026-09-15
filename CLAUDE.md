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

> **Lo studio universitario ha una sola cartella di lavoro: `~/UniCode`.**
> È da lì che si lancia Claude Code per studiare, ed è l'unico percorso da usare nei comandi,
> nei riferimenti e negli appunti. I file vivono dentro `Vault/UniCode` perché è lì che il repo
> li versiona: quel percorso è una questione di git, non una seconda cartella in cui entrare.
> Da qui — la base di lancio — lo studio **non si apre**: i comandi `/lezione`, `/lab`,
> `/appunti` e gli altri non sono più esposti in `cockpit/.claude/commands`, perché lanciati da
> qui perdono i due hook di UniCode (briefing d'avvio e registrazione di fine sessione), che
> sono registrati in `UniCode/.claude/settings.json` e partono solo quando la cartella di lavoro
> è quella.

- `~/UniCode` — **studio universitario**, cartella di lavoro unica: dodici esami arretrati verso
  la laurea nella sessione estiva 2028. Ha il suo CLAUDE.md e l'architettura di continuità
  installata il 2026-09-02 (memoria a strati, briefing iniettato dal SessionStart hook,
  consolidamento serale via timer systemd). I comandi prendono `<CODICE> <ID modulo>`, es.
  `/lezione FI2 01`; i codici stanno in `piano/codici.txt`, il piano per sessioni in
  `piano/piano_laurea.md`. `ARCHIVIO/` contiene il materiale degli esami chiusi.
- `~/Sviluppo` — tutto il codice, diviso per tipo di lavoro:
  - `app/` — accountability-app, agenticdash (dashboard + memoria, Tauri), diritto-quiz-app, bibiciclo
  - `audio/` — StereoCompressor, FreakFM, acidmoog-synth, NEMO, JUCE-shared
  - `giochi/` — Monopoly
  - `tools/` — AgenticOS, claude-code-quest, unicode-ui, UniCode-template, platform-master, cupp
  - `appunti/` — note e piani di sviluppo, non progetti

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
