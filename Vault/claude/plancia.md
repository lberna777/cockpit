# Plancia di Lorenzo — protocollo di tracciamento

> Regola fissata da Lorenzo il 2026-10-08: **ogni obiettivo o cosa da fare che Lorenzo fissa —
> studio, lavoro, musica o qualunque altro ambito — va registrato nella Plancia**, senza che
> debba chiederlo ogni volta.

- **Artefatto**: https://claude.ai/artifact/B3QifQTD67G5LZmudWk1u4 (fissato nella barra laterale).
- **Come si scrive**: con `ArtifactData` sul database della pagina, non ripubblicando la pagina.
  Prima `list` delle collezioni, poi scrittura con `if_version` sui documenti esistenti.

## Quando scrivere

Nel momento in cui emerge, senza chiedere conferma (stesso principio di `UniCode/CLAUDE.md` §5):

- Lorenzo fissa un obiettivo, una scadenza, un impegno o un «devo fare X» → nuova `attivita`;
- un'attività avanza, si blocca, attende altri, viene rimandata o chiusa → aggiornare `stato`
  (e `note`, `aggiornata`);
- nasce un ambito nuovo (un cliente, un esame che si apre, un progetto musicale) → nuovo
  documento in `progetti`.

Dal 2026-10-08 (seconda richiesta di Lorenzo) la Plancia **si evolve con tutta l'attività su
Claude, non solo UniCode**. Inoltre, sempre senza chiedere:

- si pubblica o si aggiorna un artefatto, un sito, una pagina → documento in `materiali`;
- si crea una repository o vi si invia lavoro in una sessione → `repo` (nuovo documento o
  `ultimo_push` aggiornato);
- una sessione produce qualcosa di sostanziale (studio, lavoro, musica, sistema) → una voce in
  `diario`. Una voce per risultato, non per ogni modifica.

Le repository si rilevano con `list_repos`, gli artefatti con `Artifact action: "list"`: utili
per un riallineamento quando la Plancia è rimasta indietro.

A fine risposta, una riga a Lorenzo su cosa è stato registrato o modificato nella Plancia.
Non inventare scadenze: se Lorenzo non ne dà una, `scadenza: null`.

## Schema

`progetti/<id>`: `nome`, `area`, `nota`, `ordine`.
Aree supportate dalla pagina: `lavoro`, `studio`, `musica`, `personale`.
Ordine: lavoro 1–9, studio 10–19, musica 20–29, personale 30–39.

`attivita/<id>`: `titolo`, `progetto` (id), `scadenza` (`AAAA-MM-GG` o `null`),
`stato` (`da fare` · `in corso` · `in attesa` · `rimandato` · `fatto`),
`priorita` (`alta` · `normale`), `note`, `creata`, `aggiornata` (ISO 8601).
Id leggibili con prefisso del progetto: `fi2-lab`, `calc-checkpoint`, `ari-email`…

`repo/<nome in minuscolo, . → ->`: `nome`, `url`, `visibilita` (`pubblica` · `privata`),
`ultimo_push` (`AAAA-MM-GG`), `area`, `descrizione`, `gruppo`. Il colore dell'attività
(verde ≤14 gg, ambra ≤60) lo calcola la pagina da `ultimo_push`.

`materiali/<art-ID artefatto | sito-…>`: `titolo`, `url`, `tipo` (`artefatto` · `sito` · `pagina`),
`data` (`AAAA-MM-GG`), `area`, `gruppo` (es. `CarGuy`, `Aristocani`), `descrizione`.

`diario/<AAAA-MM-GG-slug>`: `data`, `ora` (`HH:MM` o vuota), `area`, `testo` (una riga),
`url` facoltativo.

## Come la pagina le mostra

Schede: **Attività** (`attivita`), **Codice** (`repo`: dove vive il codice), **Pagine**
(`materiali`: ciò che si apre con un link), **Diario** (`diario`). Le schede Codice e Pagine si
collegano tramite lo stesso `gruppo` (es. `CarGuy`): tenerlo identico nei due documenti.
Le attività stanno in quattro colonne per orizzonte: Adesso (in ritardo + 7 giorni), Entro un
mese, Più avanti, Senza data. Un progetto che porta il nome della sua area (`Musica`,
`Personale`) non compare nel binario: fa da contenitore generico.

## Confine con UniCode

Lo stato fine dei moduli resta in `UniCode/stato/` (tracker, briefing). Nella Plancia vanno
gli obiettivi d'esame a grana grossa: appelli, checkpoint, prossimo blocco di lavoro.
