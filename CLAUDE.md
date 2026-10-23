# CLAUDE.md — ~/cockpit (base di lancio)

Questa è la **cartella base** da cui lanciare Claude Code. Da qui ti muovi liberamente
nei progetti via i symlink. I CLAUDE.md dei singoli progetti si attivano on-demand quando
entri nei loro sottoalberi.

---

## Famiglia delle repository — mappa unica

Decisa da Lorenzo il 2026-10-19. **Questa è l'unica copia della mappa**: gli altri `CLAUDE.md`
dicono solo chi è il loro padre e rimandano qui. Le repo servono a lavoro agentico: una repo
padre per argomento, su cui si opera; le figlie sono prodotti o storia del padre e hanno una
repo propria solo per non appesantirlo (o perché GitHub lo impone, come per il sito).

| Padre (si opera qui) | Gruppo di chat su claude.ai | Figlie |
| --- | --- | --- |
| **cockpit** — studio e sistema | **Studio · cockpit** (cartella `Vault/UniCode`) · **Sistema · cockpit** (tutto il resto) | Studio: `Unibo_Diritto_Informatico`, `Unibo_Lab_Sicurezza_Informatica` (esami chiusi), `Unibo_Fondamenti_Di_Informatica_T2`, `Laboratorio_Amministrazione_di_Sistemi` (materiale vecchio: i corsi vivono in `Vault/UniCode/corsi/`), `UniCode` (template pubblico in inglese), `UniCode-personal` (versione italiana di giugno), `diritto-quiz-app` (prodotto dello studio). Sistema: `claudereset`, `Boot_Debian`, `AgenticOS` |
| **Developing** — lavoro per clienti | **Progetti · Developing** (clienti) · **Portfolio · Developing** (brand, sito, profilo) | `lberna777.github.io` (sito portfolio, GitHub Pages), `lberna777` (README del profilo GitHub) |
| **plugin-creator** — plugin audio JUCE (area lavoro) | **Plugin · plugin-creator** | `StereoCompressor`, `NEMO-StereoCompressor`, `FreakFM`, `acidmoog-synth`. I plugin nuovi (C-60, RSU-10, Mikro Bridge, Vocal-Chain-Creator) nascono dentro il padre |
| **carguy** — autonoma | **CarGuy · carguy** | — |
| **bibiciclo** — autonoma | senza gruppo | — |
| **Fun** — progetti per divertimento, una repo autonoma per progetto (dal 2026-10-22) | **Fun · <repo>** | `barca-halloween` (gioco a penitenza per la festa di Halloween alla Barca: proiettore + telefoni, hub sul portatile) |
| **home** — autonoma, **solo locale**, una per computer (la cartella home di ogni macchina, nessun remote) | **Debian · home**, **Mac · home**, **Windows · home** (chat locali del Code tab, non cloud) | — |

- **home** è la repo solo locale di ogni computer: Debian dal 2026-10-21, Mac mini e portatile
  Windows dal 2026-10-22, ciascuna con la sua chat di macchina (`/debian`, `/mac`, `/windows`).
  Traccia per lista bianca dotfile, configurazione di Claude Code e auto-memoria della home
  (`CLAUDE.md` e `.gitignore` nella cartella home). Non ha remote, quindi le chat cloud non la
  aprono: la vedono attraverso questa mappa e nella Plancia come `repo/home` (Debian),
  `repo/home-mac` e `repo/home-windows`. Le repo sotto la home con un remote proprio (cockpit,
  `~/Sviluppo/...`) restano indipendenti.
- **carguy** e **bibiciclo** sono progetti veri nati dai tentativi del sistema che ha preceduto
  Developing: restano autonomi, e Developing li usa come prova di competenza nel portfolio.
- **Fun** non ha una repo padre: ogni progetto per divertimento ha la sua repo autonoma, con lo
  stesso `.claude/` delle altre (hook, `/handoff`, subagenti) e nel `CLAUDE.md` il blocco «Famiglia»
  che rimanda qui. Un progetto nuovo si aggiunge alla tupla `FUN` di `titolo_chat.py`.
- **Due repo per il portfolio, non un doppione**: `lberna777.github.io` è il sito (GitHub Pages
  pubblica solo da una repo con quel nome), `lberna777` è il README mostrato sulla pagina del
  profilo GitHub (anche lui vuole una repo con il nome dell'utente). Si aggiornano insieme.
- **Figlie archiviate** (sola lettura su GitHub dal 2026-10-19): `UniCode`, `UniCode-personal`,
  `Unibo_Diritto_Informatico`, `Unibo_Lab_Sicurezza_Informatica`,
  `Unibo_Fondamenti_Di_Informatica_T2`, `Laboratorio_Amministrazione_di_Sistemi`, `AgenticOS`.
  Si consultano, non ci si lavora: le modifiche vanno nel padre. `mixer` e `claude-code-quest`
  sono state cancellate.
- **Topic GitHub** (`padre`, `autonoma`, `famiglia-cockpit|developing|plugin`): li mette
  `scripts/topics_famiglie.sh` dal laptop con `gh`; se la mappa cambia, si aggiorna anche lui.
- **Regola per i `CLAUDE.md`**: ogni repo ha in testa un blocco «Famiglia» di poche righe (padre,
  figlie, rimando qui). Le regole valgono nel `CLAUDE.md` del padre e non si ricopiano nelle
  figlie; profilo e preferenze di Lorenzo stanno nelle preferenze personali di claude.ai.
  Quando nasce, si archivia o cambia padre una repo, si aggiorna questa tabella e il campo
  `chat` della repo nella Plancia.

### Chat di amministrazione del sistema (gruppo Sistema · cockpit)

| Chat | Cosa fa | Dove legge |
| --- | --- | --- |
| **Manager** | Scadenze e cose da fare di tutti gli ambiti, punto della settimana, Plancia | `Vault/claude/chat_manager.md` · comando `/manager` |
| Infrastruttura | Hook, script, memoria (`Vault`), automatismi di studio, questa mappa | questo file |
| Reset | Esportazione e filtro della memoria di Claude | repo `claudereset` |
| Computer | Debian, Mac mini, portatile Windows, `Boot_Debian` | progetto `computer` della Plancia |

---

## Memoria persistente

La memoria vive in `~/cockpit/Vault` ed è **iniettata automaticamente** a ogni avvio dal
SessionStart hook (`scripts/memory_inject.sh`) — non devi fare nulla per "caricarla", è già
in contesto. L'hook inietta pochi KB: dove cercare, le note curate di `Vault/claude/` e gli
ultimi tre recap (rifatta piccola il 2026-10-22, decisione di Lorenzo; prima erano ~28 KB).

- **Ricerca nel vault**: usa `rg` (ripgrep) dentro `~/cockpit/Vault`. È il motore di ricerca
  della memoria (deciso dal bake-off G3: `Vault/claude/graphify_bakeoff.md`).
- **Indice**: `Vault/index.md`, non iniettato: si apre se serve. Lo rigenera `scripts/build_index.py`
  dal timer serale del laptop.
- **Recap giornalieri**: `Vault/recap/YYYY-MM-DD.md`, solo fatti contati (eventi di studio per corso,
  moduli chiusi, commit che dicono qualcosa per repo), niente sintesi generate. Li scrive
  `scripts/recap_generator.py` dal timer serale del laptop (`giornata_laptop.sh`), che li committa;
  nel cloud non si generano, perché lì mancano le altre repo.
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
>   sul laptop la committa subito (senza push, lo fanno i timer), perché un log sporco bloccava
>   il `git pull` dei timer (2026-10-22). Il log del mese si unisce con `merge=union`
>   (`.gitattributes`): due lati che accodano righe non vanno in conflitto;
> - **cloud**: `scripts/cloud_autosave.sh` committa e invia il Vault dopo ogni modifica (`PostToolUse`) e a fine risposta (`Stop`),
>   sul ramo di sessione **e su master** (solo fast-forward; se master è andato avanti lo
>   unisce prima, in conflitto si ferma e avvisa; un'esecuzione alla volta, e con un merge in
>   conflitto aperto o marcatori `<<<<<<<` nei file non committa niente e avvisa, dal
>   2026-10-22): ciò che Claude crea nel cloud arriva sul laptop
>   e in Obsidian con un `git pull` (richiesta di Lorenzo del 2026-10-01). Rischio da ricordare:
>   un consolidamento serale del laptop non ancora inviato diverge su `log/giornate.md`,
>   `stato/tracker.md`, `log/giornate_dettaglio/` — sul laptop, `git pull` prima di studiare;
> - **progetti Eclipse dal cloud**: in `Vault/UniCode/corsi/FI2/esame_FI2/da_importare/`, da
>   importare con *Existing Projects → Select root directory* + *Copy projects into workspace*;
> - **comandi**: `/lab`, `/chiudi`, `/lezione`… stanno in `.claude/commands` come rimandi agli
>   originali di `Vault/UniCode/.claude/commands`; dopo aver aggiunto o rinominato un comando
>   di UniCode, `python3 scripts/unicode_commands.py`;
> - **fuso**: `TZ=Europe/Rome` in `settings.json`, perché il container cloud è in UTC;
> - **pre-commit** `.githooks/pre-commit`: rifiuta i commit che aggiungono marcatori di conflitto.
>   Attivo con `git config core.hooksPath .githooks` (nel cloud lo fa il bootstrap, sul laptop
>   una volta a mano); `scripts/salute_hook.py` controlla master e l'attivazione.
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

Impegni, progetti, repository, materiali, diario e giornata a ore di Lorenzo si registrano
**subito e senza chiedere** nella Plancia (https://claude.ai/artifact/B3QifQTD67G5LZmudWk1u4) con
`ArtifactData`. Tutte le regole (schema, priorità, pianificazione dello studio, blocchi `toccato`)
stanno nel protocollo **privato** del suo database, documento `meta/protocollo`: leggerlo prima
di scrivere, non ricopiarlo qui.

## Convenzioni globali
- **Lingua**: italiano.
- **Handoff**: al 50% del contesto l'hook `.claude/hooks/context_handoff.py` fa partire `/handoff`
  (`.claude/commands/handoff.md`): scrive l'handoff, crea la sessione che sostituisce questa e le
  affida l'archiviazione della vecchia. Hook e comando sono identici in tutte le repo padri.
- **Skill custom**: `lorenzo-skills` (audio-dsp-debug, game-scope-guard, studia, unicode-output-gate,
  unicode-session-close, unicode-link-note).
- **Cosa è successo nella giornata**: lo studio va in `Vault/UniCode/stato/giornata.md`, tutto il
  resto nel diario della Plancia. `Vault/attivita_oggi.md` non esiste più (dal 2026-10-22).

## Modelli: chi pensa e chi esegue (advisor pattern)

Deciso da Lorenzo il 2026-10-20. Copia identica nei `CLAUDE.md` di cockpit, Developing,
plugin-creator, carguy, bibiciclo e barca-halloween; l'originale è in cockpit: se lo cambi,
ricopialo nelle altre. I due subagenti stanno in `.claude/agents/`, identici in tutte e sei le repo.

| Livello | Chi | Che cosa fa |
| --- | --- | --- |
| **Advisor** | La sessione stessa, su **Opus** (`"model": "opus"` in `.claude/settings.json`) | Organizza, pianifica, decide, parla con Lorenzo, scrive gli incarichi, **giudica ogni consegna**, fa commit e push |
| **Sviluppatore** | Subagente `sviluppatore`, su **Sonnet** | Codice su un piano già deciso: implementa, scrive e fa girare i test, corregge finché passano |
| **Esecutore** | Subagente `esecutore`, su **Haiku** | Lavori ripetitivi e veloci: estrazioni, inventari, conversioni, modifiche meccaniche su molti file, controlli in serie |

- **Si delega** ciò che è definito e verificabile: chi lo riceve non deve scegliere niente.
  **Resta all'advisor** ciò che chiede giudizio: architettura e piani, testi che contano, scelte
  di stile, privacy e dati personali, ogni decisione e ogni domanda per Lorenzo.
- **Studio** (cockpit, `Vault/UniCode`): lezioni, lab, spiegazioni, verifiche e giudizi su come va
  Lorenzo restano all'advisor. All'esecutore vanno conversioni in PDF, indici, collegamenti tra le
  note, controlli su molti file.
- **Incarico** (`Agent` con `subagent_type: "sviluppatore"` o `"esecutore"`): obiettivo in una
  frase, file di partenza, uscita attesa (percorsi e formato), criterio di completamento (per il
  codice: quali test devono passare), cosa non fare. Incarichi indipendenti in parallelo.
- **Controllo**: l'advisor rilegge ogni consegna prima del commit (per intero il codice e i testi,
  a campione i lavori in serie). I subagenti non fanno commit né push. Se una consegna non passa,
  la corregge l'advisor o la rimanda con un incarico più preciso.
- **Non si delega** un lavoro che l'advisor finisce prima di quanto serva a scrivere l'incarico.

## graphify

graphify è installato ma **fuori dal layer memoria** per decisione del bake-off G3
(`Vault/claude/graphify_bakeoff.md`): la ricerca nella memoria si fa con `rg`, non con graphify.

Usalo **solo** dentro un progetto di *codice* che abbia il suo `graphify-out/graph.json`
(es. `graphify query "<domanda>"`, `graphify update .` dopo modifiche). Se `graphify-out/`
non esiste nella cartella corrente, ignora graphify e usa `rg`.

Visualizzazione del vault: la fa **Obsidian** (graph view nativa dei `[[wikilink]]`).
I collegamenti tra le note di studio sono generati da `scripts/link_modules.py`
(deterministico, rigenerabile; `--strip` per rimuoverli).
