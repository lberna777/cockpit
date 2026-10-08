# CALC — Calcolatori Elettronici T · percorso

> Mappa dei moduli e stato di dettaglio. Si carica su necessità (`CLAUDE.md` §4). I concetti
> elencati qui sono un indice per trovare il PDF, non una fonte da cui generare.
>
> Redatto il 2026-09-14 dall'inventario reale, edizione **2024/25** (Mattoccia, Leone Cavalcanti).
> Identificatore di modulo = numero della dispensa. Uso: `/lezione CALC 07`.

**Stato di chiusura**: esercizio della tipologia risolto a freddo **e** parte di progetto
verificata — l'esame è scritto con domande, esercizi *e* progetto di un sistema basato su CPU.

## Moduli

| ID | Titolo | Fonte in `materiali/slide/` | Stato |
|---|---|---|---|
| 00 | Complementi ed esercizi di Reti Logiche | `00_Complementi_Esercizi_Reti_Logiche.pdf` | ⬜ |
| 01 | Introduzione: evoluzione tecnologica, organizzazione gerarchica | `01_Introduzione.pdf` | ⬜ |
| 02p | Fondamenta per il mapping: macchina, chip, numeri (prerequisito di `02`) | `01` pp. 9, 30–36 · `02` pp. 2–13, 34–38 · `00` es. 10 | 🔶 lezione 2026-10-08 (`lezioni/lezione_02p_fondamenta.md`) |
| 02 | Mapping e decodifica delle memorie | `02_Mapping_e_decodifica.pdf` | 🔶 lezione 2026-10-06 (`lezioni/lezione_02_mapping_decodifica.md`); si chiude con `/lab CALC 02` su `2023-12-21` |
| 03 | Linguaggio macchina | `03_Linguaggio_macchina.pdf` | ⬜ |
| 04 | Interruzioni | `04_Interruzioni.pdf` | ⬜ |
| 05 | Handshake e gestione dell'I/O | `05_Handshake.pdf` | ⬜ |
| 06 | **assente dalla fonte** — vedi nota | — | ⚠️ |
| 07 | DLX sequenziale | `07_DLX_sequenziale.pdf` | ⬜ |
| 08 | DLX pipelined | `08_DLX_pipelined.pdf` | ⬜ |
| SEM | Seminario RISC-V (prof. Tagliavini) | `Seminario RISC-V.pdf` | ⬜ |

> ⚠️ **Modulo 06 assente.** Nell'area del corso la numerazione salta da `05 - Handshake` a
> `07 - DLX_sequenziale`. Non si assume che sia una lacuna del programma: può essere materiale
> non pubblicato, accorpato o rinumerato. **Va verificato prima di considerare completo il
> percorso** — se il modulo esiste ed è d'esame, è una fonte mancante ai sensi di `CLAUDE.md`
> §7.1 e va chiesta.

## Prove (`prove/`)

`[2026-10-06]` Archivio scompattato e indicizzato: **62 testi, 46 con soluzione** (2015–2025),
tutti con un unico esercizio di progetto di un sistema DLX. Indice e piano d'uso in
`prove/INDICE.md`.

## Calendario verso l'appello anticipato del 2 dicembre 2026 `[2026-10-06]`

| Settimane | Contenuto |
|---|---|
| 1–3 (6–26 ott) | `02`, `03`, `04`, `05`; `00` su necessità |
| 4 (27 ott – 2 nov) | `07`, `08`, `01` |
| **~3 nov** | **checkpoint**: `2024-01-19` a freddo, cronometrata — sotto la sufficienza, appelli ordinari di S1 |
| 5–8 (3 nov – 1 dic) | ciclo sulle prove; riserva `2025-01-29`, `2025-02-12` |

## Da rilevare all'apertura del corso

- ~~Contenuto e struttura dell'archivio delle prove~~ — rilevato il 2026-10-06, `prove/INDICE.md`.
- Se le «domande di carattere generale» della scheda esistono ancora: nei testi pubblicati non compaiono.
- Se le dispense coprono l'intero programma della scheda (architetture avanzate, unità di
  controllo sequenziali e pipelined) o se parte del programma poggia sul libro di testo.
