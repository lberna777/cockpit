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
- **Studio universitario**: `Vault/UniCode` (symlink a `~/UniCode`).

### Confine con l'auto-memory di Claude (`~/.claude/.../memory/`)
- **Auto-memory** (`MEMORY.md` + frontmatter): chi è l'utente, preferenze, stato progetti —
  fatti curati che Claude scrive su di sé. Per la continuità di Claude.
- **Vault** (`~/cockpit/Vault`): corpus di conoscenza — studio, recap di attività, reference.
  Per il lavoro.
- Regola: preferenze/profilo/stato → auto-memory; corpus/attività/studio → vault. Non duplicare.

---

## Mappa del territorio

Symlink di navigazione da qui:
- `Idee/` → `~/Idee` — progetti personali: app, plugin, giochi, esperimenti musicali/creativi.
  - `agenticdash/` — questa app (dashboard + memoria, Tauri). Vedi il suo CLAUDE.md.
  - `diritto-quiz-app/`, `unicode-ui/`, `NEMO/`, ecc.
- `UniCode/` → `~/UniCode` — studio universitario (Diritto, SysAdmin, Security). Ha il suo
  CLAUDE.md con workflow `/lezione`, `/appunti`, `/chiudi`, ecc.

---

## Convenzioni globali
- **Lingua**: italiano.
- **Handoff**: a ~75% di contesto usa `/handoff` o `/handoffplan` (vedi `~/Idee/CLAUDE.md`).
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
