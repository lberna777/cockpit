# CALC — Calcolatori Elettronici T · fonti

> **Obbligatorio prima di aprire il corso** (`CLAUDE.md` §7.1). Contenuto didattico solo da
> queste fonti, lette per intero. Fonte mancante → ci si ferma e la si chiede.
>
> Aperta e compilata il 2026-09-14.

**Esame**: Calcolatori Elettronici T · **6 CFU** · sessione pianificata **S1**
**Insegnamento**: 434701 · **Docenti**: Stefano Mattoccia, Ugo Leone Cavalcanti
**Tipo di verifica**: scritto con domande, esercizi **e progetto di un sistema basato su CPU**

**Template lezione**: progetto su prova `[2026-10-06, deciso da Lorenzo]` — vedi `/lezione`.
Prontuario con la procedura d'esame: `appunti/prontuario_CALC.md`.

## Modalità d'esame (scheda ufficiale 2025/26)

Esame scritto: domande di carattere generale sulle tematiche del corso, esercizi e il progetto
di un sistema basato su CPU. Per superarlo servono **entrambe** le componenti.

> `[2026-11-20, scoperto da Lorenzo]` **Prima del progetto c'è uno sbarramento teorico**: le
> «domande di carattere generale» esistono e vanno superate per accedere alla parte pratica.
> **Sono gli esercizi 2 e 3 di ogni prova**: i testi pubblicati li riportano solo come «Rif.
> lucidi/lezioni» (es. `prove/2022-01-17-Soluzione.pdf`), per questo l'indice del 6/10 li aveva
> mancati. Soglia e regola esatta dello sbarramento: **da rilevare** (Lorenzo li sta chiedendo).
> Conseguenza: i moduli 01, 07, 08 non sono più facoltativi.

## Gerarchia delle fonti

| Rango | Fonte | Stato | Dove |
|---|---|---|---|
| 1 — primaria | dispense del docente — 8 moduli + seminario RISC-V | ✅ acquisita 2026-09-14 | `materiali/slide/` |
| 2 — prove passate | cartella `Prove_esame` del docente (12,7 MB) | ✅ acquisita, scompattata e indicizzata 2026-10-06 | `prove/INDICE.md` |
| 2b — dispensa di uno studente | U. Paganelli, *Calcolatori Elettronici*, a.a. 2024/25, 89 pp.: capp. 1.1–1.4 → moduli 01–03, 1.5 → 04, 1.6 → 05 (con due progetti d'esempio, §1.4.5 e §1.6.4), 2.1 → 07, 2.2 → 08 | ✅ acquisita 2026-11-20 (amico di Lorenzo); non è del docente: in caso di contrasto vince il rango 1 | `materiali/dispense_studenti/` |
| 2c — sito di uno studente (S. Elia, 2023) | Notion «Calcolatori elettronici – share point»: **soluzioni degli esercizi 2 e 3 (teoria)** di 11 prove 2020–2022, tabella istruzioni DLX — https://excited-sock-621.notion.site/Calcolatori-elettronici-share-point-eef7a9b6dd8b447a9bc6e1a121fcf84e | ✅ trovato 2026-11-20; le risposte stanno in blocchi da aprire a mano nel browser | online |
| — dispensa integrale condivisa dal docente | | ⏳ Lorenzo se la sta facendo inviare (20/11) | — |
| 3 — libro di testo | Patterson–Hennessy, *Struttura e progetto dei calcolatori* (Zanichelli); Hennessy–Patterson, *Computer Architecture*, capp. 1–5 | ⬜ non reperito | — |

## Annata del materiale

- Materiale scaricato: **edizione 2024/25**, quella a cui Lorenzo è iscritto.
- Scheda d'insegnamento consultata: **2025/26**. Programma coerente con le dispense:
  evoluzione, gerarchia, RISC/DLX vs CISC, memorie e decodifiche, controllo sequenziale e
  pipelined, I/O e interruzioni.
- Differenze rilevate: nessuna sui contenuti.

## Cosa manca

- ⚠️ **Modulo 06**: la numerazione delle dispense salta da `05 - Handshake` a `07 - DLX_sequenziale`.
  Da verificare se esiste un modulo 06 d'esame non pubblicato. Finché non è chiarito, quel punto
  del programma è una fonte mancante ai sensi della regola §7.1.
- **Libro di testo**: dichiarato in scheda, non reperito.
- ~~L'archivio delle prove va scompattato e indicizzato~~ — fatto il 2026-10-06.

## Note
- Testa di catena verso `SO` (S2).
