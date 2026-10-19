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

Ogni sessione porta l'etichetta del suo gruppo (`studio`, `sistema`, `progetti`, `portfolio`,
`plugin`, `carguy`) e un titolo che comincia con il nome del gruppo («Studio · cockpit — …»). Claude la mette con
`set_session_tags` e `set_session_title` quando la sessione non ce l'ha. Le sessioni concluse
o superate si archiviano: lo stato vero sta nelle repo e nella Plancia, non nelle chat.

**Chat piena**: al 50% del contesto un hook fa partire `/handoff`. Claude scrive l'handoff, apre
la sessione che la sostituisce (stesso titolo con « (segue)», stesse etichette, stesso ramo) e ti
dà il link; la sessione nuova archivia la vecchia. Va solo spostata nel gruppo giusto.

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
