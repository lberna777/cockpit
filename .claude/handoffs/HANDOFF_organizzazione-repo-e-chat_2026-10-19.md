# Handoff — Organizzazione repo e chat

- **Data**: 2026-10-19
- **Chat**: Sistema · cockpit — Organizzazione repo e chat
- **Sessione**: `session_01CtFEaM5WXvQbw6jimbMwn8` (chiusa al 51% del contesto, `/handoff` lanciato a mano)
- **Repo**: cockpit, `master` (la sessione era partita su UniCode, ramo `claude/affectionate-carson-w31lbc`)

## Obiettivo

Riordinare il rapporto tra le repository GitHub di Lorenzo e i gruppi di chat dell'app Claude,
eliminare doppioni nei `CLAUDE.md` e preparare un modo di lavorare il più possibile in cloud.

## Fatto

- **Mappa unica delle repo** nel `CLAUDE.md` di cockpit, sezione «Famiglia delle repository»: tre
  padri (cockpit per studio e sistema, Developing per il lavoro, plugin-creator per i plugin),
  carguy e bibiciclo autonome. Ogni altra repo ha in testa un blocco «Famiglia» con il padre.
- **Archiviate su GitHub** (da Lorenzo): UniCode, UniCode-personal, Unibo_Diritto_Informatico,
  Unibo_Lab_Sicurezza_Informatica, Unibo_Fondamenti_Di_Informatica_T2,
  Laboratorio_Amministrazione_di_Sistemi, AgenticOS. **Cancellate**: mixer, claude-code-quest.
- **Topic GitHub** (`padre`, `autonoma`, `famiglia-*`) messi con `scripts/topics_famiglie.sh`.
- **Chat Manager** spostata da Developing a cockpit: `Vault/claude/chat_manager.md`, comando
  `/manager`. Tolti da Developing `manager/` (plancia.html vecchia) e il ruolo manager.
- **Nuovo ruolo `/portfolio`** in Developing (`chat/portfolio.md`).
- **Gruppi di chat** con nomi doppi: Studio · cockpit, Sistema · cockpit, Progetti · Developing,
  Portfolio · Developing, Plugin · plugin-creator, CarGuy · carguy. Guida e schema dei comandi
  d'apertura: `Vault/claude/come_lavorare.md`.
- **Sessioni**: 36 archiviate, le 11 attive rinominate «Gruppo · repo — argomento» ed etichettate.
- **Hook nelle cinque repo padri** (originale in cockpit, copie identiche):
  `.claude/hooks/context_handoff.py` (Stop, al 50% fa eseguire `/handoff`, procedura in
  `.claude/commands/handoff.md`) e `.claude/hooks/titolo_chat.py` (UserPromptSubmit, titolo ed
  etichetta automatici al primo messaggio). Registrati in `.claude/settings.json`.
- **Portatile Debian allineato** con `scripts/allinea_repo.sh` (16 repo aggiornate, cartelle
  superate cancellate, conflitto di cockpit del 19/10 risolto in cloud tenendo i due lati).
- **Plancia**: campo `repo.chat`, plugin passati ad area lavoro, repo archiviate segnate, voci di
  diario; il protocollo rimanda alla mappa di cockpit invece di copiarla.

## Decisioni di Lorenzo

- Una repo padre per argomento; le figlie sono prodotti o storia e restano repo a parte.
- Manager nel gruppo Sistema; plugin = area lavoro; nomi dei gruppi doppi «attività · repo».
- Developing diviso in due gruppi: Progetti (clienti) e Portfolio (brand, sito, profilo).
- Handoff automatico al 50%; la sessione nuova archivia la vecchia.

## Ancora aperto

- **Hook mai visti girare in una sessione vera**: provati solo su casi finti e sulla trascrizione
  di questa chat. Alla prima chat nuova verificare che il titolo si imposti da solo e, alla prima
  chat che supera il 50%, che il passaggio crei la sessione e archivi la vecchia.
- Carguy: il ramo `fix/mappe-feed-e-classifica-iphone` aspetta la decisione di Lorenzo (unire a
  main?); sul Mac mini controllare `git status` in carguy (a fine settembre risultavano 17 commit
  non inviati) e lanciare `scripts/allinea_repo.sh` anche lì.
- Ramo `locale-2026-10-19` su cockpit: Lorenzo l'ha cancellato? Da verificare con `git ls-remote`.
- I gruppi dell'app non sono raggiungibili dagli strumenti: Lorenzo sposta le chat a mano.

## Prossimo passo esatto

Verificare su GitHub che il ramo `locale-2026-10-19` di cockpit non esista più, poi chiedere a
Lorenzo se aprire una chat di prova in **Studio · cockpit** con `/stato` per vedere l'hook del
titolo in azione.

## Da leggere per primi

1. `CLAUDE.md` di cockpit, sezione «Famiglia delle repository»
2. `Vault/claude/come_lavorare.md`
3. `.claude/commands/handoff.md`
