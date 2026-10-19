# Come lavorare — gruppi di chat, repo e cloud

Deciso con Lorenzo il 2026-10-19. Obiettivo: lavorare il più possibile in sessioni cloud.
La mappa delle repo sta nel `CLAUDE.md` di cockpit («Famiglia delle repository»): qui c'è
solo come usarla.

## Gruppi di chat nell'app Claude

Il nome di ogni gruppo dice cosa si fa e quale repo **padre** selezionare (nomi doppi, decisi il 2026-10-19).

| Gruppo | Repo da selezionare | Primo messaggio | Cosa ci va |
| --- | --- | --- | --- |
| **Studio · cockpit** | `cockpit` | `/sessione`, `/lab FI2 LAB06`, `/pianifica`… | Solo studio; una chat per sessione, chiusa con `/chiudi` |
| **Sistema · cockpit** | `cockpit` | `/manager` oppure «infrastruttura: …» | Plancia e scadenze, mappa delle repo, hook, computer, reset |
| **Progetti · Developing** | `Developing` | `/principale`, `/aristocani`, `/polisportiva`, `/noone` | Clienti: strategia, demo, sviluppo |
| **Portfolio · Developing** | `Developing` | `/portfolio` | Brand, sito (`lberna777.github.io`) e profilo GitHub, aggiunti con `add_repo` |
| **Plugin · plugin-creator** | `plugin-creator` | il nome del plugin | Una chat per plugin |
| **CarGuy · carguy** | `carguy` | — | Solo l'app |
| senza gruppo | nessuna, o `bibiciclo` | — | Domande veloci |

Regola: **una chat, un lavoro**. Cambio di argomento → chat nuova.

**Titolo ed etichetta automatici**: al primo messaggio di ogni sessione cloud l'hook
`.claude/hooks/titolo_chat.py` (identico nelle cinque repo padri, originale in cockpit) ricava il
gruppo dalla repo e dal comando d'apertura, e Claude imposta il titolo «<Gruppo> — <argomento>» e
l'etichetta (`studio`, `sistema`, `progetti`, `portfolio`, `plugin`, `carguy`, `bibiciclo`). In
cockpit apre una chat **Studio** un comando di studio (`/sessione`, `/lab`, `/lezione`, `/appunti`,
`/ripassa`, `/simula`, `/flusso`, `/stato`, `/lacune`, `/piano`, `/pianifica`, `/chiudi`,
`/verifica`), qualunque altro inizio una chat **Sistema**; in Developing `/portfolio` apre
**Portfolio**, il resto **Progetti**. A Lorenzo resta solo spostare la chat nel gruppo dell'app.
Le sessioni concluse o superate si archiviano: lo stato vero sta nelle repo e nella Plancia.

**Chat piena**: al 50% del contesto un hook fa partire `/handoff`. Claude scrive l'handoff, apre
la sessione che la sostituisce (stesso titolo con « (segue)», stesse etichette, stesso ramo) e ti
dà il link; la sessione nuova archivia la vecchia. Va solo spostata nel gruppo giusto.

## Con che comando aprire una chat

### Studio · cockpit — repo `cockpit`

| Primo messaggio | Quando |
| --- | --- |
| `/sessione FI2` | Apri la giornata di studio su un corso: briefing e punto in cui eri |
| `/lab FI2 LAB06` | Guida-lab pratica di un modulo (FI2 si fa così) |
| `/lezione CALC 03` | Lezione di teoria di un modulo, dalle fonti del corso |
| `/appunti CALC 03` | Appunti grezzi scritti: Claude li rifinisce e aggiorna lo stato |
| `/ripassa CALC 02` | Ripasso con domande nuove su un modulo chiuso |
| `/simula CALC` | Simulazione d'esame |
| `/flusso Classe.metodo` | Il flusso di una funzione disegnato passo per passo |
| `/stato` · `/lacune` · `/piano` | Riepilogo · moduli a rischio · piano di oggi |
| `/pianifica settimana` | Date di studio nella Plancia (mese, settimana, domani) |
| `/chiudi` | Fine sessione: registra la giornata e fissa lo studio di domani |

### Sistema · cockpit — repo `cockpit`

| Primo messaggio | Quando |
| --- | --- |
| `/manager` | Scadenze, «cosa faccio questa settimana?», Plancia, giornata a ore |
| `infrastruttura: …` | Hook, script, mappa delle repo, memoria, impostazioni di Claude |
| `computer: …` | Debian, Mac mini, Windows, backup, spazio su disco |

### Progetti · Developing — repo `Developing`

| Primo messaggio | Quando |
| --- | --- |
| `/principale` | Strategia, nuovi clienti, prezzi, riscontro dopo un incontro |
| `/aristocani` · `/polisportiva` · `/noone` | Demo e sviluppo per quel cliente |

### Portfolio · Developing — repo `Developing`

| Primo messaggio | Quando |
| --- | --- |
| `/portfolio` | Brand, sito portfolio, README del profilo GitHub |

### Plugin · plugin-creator — repo `plugin-creator`

| Primo messaggio | Quando |
| --- | --- |
| `C-60: …` · `RSU-10: …` · `Mikro Bridge: …` · `VOCAL FORGE: …` | Lavoro su quel plugin, una chat per plugin |
| `plugin nuovo: …` | Si parte dalla scheda del plugin da compilare (`PLUGIN_SPEC.md`) |

### CarGuy · carguy — repo `carguy`

| Primo messaggio | Quando |
| --- | --- |
| `carguy: …` | Lavoro sull'app; a fine blocco Claude usa da solo `chiudi-blocco` |
| `prove visive: …` | Screenshot e prove su simulatore o web app |
| `finisci il lavoro` | Solo sul Mac, in locale |

### Ovunque

| Comando | Cosa fa |
| --- | --- |
| `/handoff` | Passaggio di consegne a mano; al 50% del contesto parte da solo |
| domanda veloce, senza repo | Chat senza gruppo, da archiviare quando hai finito |

## Cosa si fa in cloud e cosa no

| Lavoro | Cloud | Serve una macchina |
| --- | --- | --- |
| Studio: lezioni, appunti, guide-lab, ripasso | sì, salvataggio automatico su master | — |
| FI2 con Eclipse | sì: scrive, compila con `javac`, consegna uno zip | portatile Debian per importarlo |
| LAS (laboratori su macchina virtuale) | sì, la guida | portatile Debian per la macchina virtuale |
| Developing: demo web, documenti, sito | sì | — |
| Plugin: codice, specifiche, test | in gran parte | Mac mini: build AU, prove in Logic e FL Studio |
| Carguy: server, web app, DriveCore | sì | Mac mini: Xcode, iPhone e Watch |

Quando un lavoro passa al Mac o al portatile, Claude lo dice e lascia un handoff nella repo.

## Il giro tipo

1. Sessione cloud nel gruppo giusto, con la repo padre selezionata.
2. Se serve una figlia, Claude la aggiunge con `add_repo`.
3. A fine lavoro: in cockpit il salvataggio è automatico; altrove Claude fa commit e push su main.
4. Prima di lavorare in locale: `git pull` nella repo. Sul laptop, in cockpit, se il pull si
   ferma per modifiche locali (il consolidamento serale), prima `git add -A && git commit`,
   poi `git pull --no-rebase`.
