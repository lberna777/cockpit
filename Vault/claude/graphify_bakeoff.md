# GATE G3 — graphify vs rg (esito)

**Data:** 2026-06-17
**Esito:** `rg` vince. graphify **esce** dal layer memoria/ricerca.

## Metodo
5 domande reali sul vault, confronto `rg` (baseline) vs `graphify path/explain`.

## Risultati rg
| # | Domanda | rg trova il rilevante? |
|---|---------|------------------------|
| 1 | Moduli Diritto su privacy/GDPR | Sì — glossario, stato/corrente, handoff D12/D13 |
| 2 | Dove ho parlato di systemd | Sì — master_map, concept_maps, percorso |
| 3 | AI Act | Sì — handoff dedicati, master_map |
| 4 | Reati informatici | Sì — handoff reati-ia, percorso |
| 5 | Firme elettroniche | Sì — speedreview_D09 (file dedicato), glossario |

## Decisione (pre-autorizzata da spec §9/§12)
- **Ricerca memoria = `rg`** sul vault. Veloce, trasparente, zero costo, zero dipendenze.
- **graphify NON entra** nel layer memoria: l'estrazione su markdown è un run di agente LLM
  pesante sull'intero UniCode e richiede modifica di `~/.claude` (install della skill).
  Costo/permessi non giustificati dato che `rg` già risponde bene su 119 note.
- **G2 (build headless)**: non eseguito — moot, graphify fuori dal layer core.
- **Grafo come feature OPZIONALE futura**: se in futuro si vuole la visualizzazione
  interattiva (`graph.html`) come oggetto visivo (non come motore di ricerca), si potrà
  installare graphify allora, con consenso esplicito per la modifica di `~/.claude` e
  accettando il costo dell'estrazione. La schermata Memoria dell'app funziona senza.

## Nota
Il vault resta compatibile con graphify (è una cartella di markdown): la decisione è
reversibile in qualsiasi momento senza rifare nulla.
