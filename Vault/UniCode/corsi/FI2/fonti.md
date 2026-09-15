# FI2 — Fondamenti di Informatica T-2 · fonti

> **Obbligatorio prima di aprire il corso** (`CLAUDE.md` §7.1). Claude genera contenuto
> didattico **solo** dalle fonti dichiarate qui, lette per intero. Se la fonte di un modulo non
> è disponibile, ci si ferma e la si chiede: mai colmare con conoscenza generica.
>
> Aperta il 2026-09-14, compilata lo stesso giorno dopo l'acquisizione del materiale.

**Esame**: Fondamenti di Informatica T-2 · **12 CFU** · sessione pianificata **S1** (19 dic 2026 – 14 feb 2027)
**Insegnamento**: 434698 · **Docenti**: Enrico Denti, Ambra Molesini, Roberta Calegari
**Tipo di verifica**: prova pratica al calcolatore (+ orale eventuale) → **esercizi + progetto**

## Modalità d'esame (scheda ufficiale 2024/25)

Prova pratica al calcolatore su un problema di tipo ingegneristico: il codice prodotto deve
**compilare e superare almeno 2/3 dei test** forniti. Prova orale su richiesta dello studente o
a discrezione del docente. Strumenti: JDK, Eclipse, JUnit, JavaFX.

> **Unità di verifica** (`CLAUDE.md` §7.2): un modulo è chiuso quando Lorenzo ha risolto un
> esercizio della tipologia **a freddo, senza soluzione sotto mano**, con codice che compila e
> passa i test. Aver letto una soluzione non chiude nulla.

## Gerarchia delle fonti

| Rango | Fonte | Stato | Dove |
|---|---|---|---|
| 1 — primaria | slide del docente, versione `x1` — 57 file | ✅ acquisita 2026-09-14 | `materiali/slide/` |
| 2 — laboratorio | 13 esercitazioni con slide, startkit e soluzione — 58 file | ✅ acquisita | `materiali/lab/` |
| 3 — esercizi autonomi | 11 esercizi con testo, startkit e soluzione — 22 file | ✅ acquisita | `materiali/esercizi/` |
| 4 — prove passate | **30 appelli completi** (testo + start kit + soluzione del docente), 2020-01 → 2025-02, più la simulazione 05/06/2024 | ✅ acquisita 2026-09-14 | `prove/` |
| 5 — libro di testo | elenco tenuto dal docente sul portale | ⬜ non reperito | — |
| esterna | **documentazione ufficiale Apache Maven** (`maven.apache.org`: *What is Maven*, *Introduction to the Build Lifecycle*, *Introduction to the POM*, *Introduction to the Dependency Mechanism*) | ✅ consultata 2026-09-15 | web |

**Fonte esterna — Maven.** Il corso nomina i build tools in una sola slide (01, sl. 17) senza
trattarli. Su richiesta esplicita di Lorenzo (2026-09-15) la documentazione ufficiale di Maven è
ammessa **solo** per spiegare cosa sia un build tool, e ogni passo che ne deriva va marcato
`[fonte: maven.apache.org]`, separato dal materiale del docente. Non è materia d'esame.

**Materiale di supporto in `materiali/slide/` non numerato** (fuori dalla tabella dei moduli in
`percorso.md`): `DiagrammiUML.pdf`, *Nozioni base di UML2* (Molesini, edizione **2019/20**), con
diagramma delle classi, di sequenza e delle attività; `CACM 2018(4)-Google.pdf`, l'articolo
citato in 01 sl. 16.

Non scaricate di proposito: le 49 versioni `x6` delle slide (stesso contenuto, sei per pagina) e
le risorse di tipo video/URL, non scaricabili.

## Annata del materiale

- Materiale scaricato: **edizione 2023/24** — è l'edizione a cui Lorenzo risulta iscritto su Virtuale.
- Scheda d'insegnamento consultata: **2024/25**.
- Differenze rilevate finora: nessuna sui contenuti; la scheda 2024/25 e le slide 2023/24
  concordano su paradigmi, Java a oggetti, lambda, eccezioni, I/O, strutture dati e JavaFX.
- ⚠️ Da verificare all'avvicinarsi dell'appello: se il corso 2026/27 ha cambiato programma o
  modalità, le differenze **non vanno contate come lacune** (`verifica.md` §2), ma dichiarate qui.

## Archivio delle prove — fonte aggiuntiva

`enricodenti.disi.unibo.it/Fond/VecchiEsami/Esami.shtml` — archivio pubblico del docente:
**90 appelli dal 2010 al 2025**, ciascuno con testo, start kit e soluzione ufficiale.

Scaricati il 2026-09-14 i **29 appelli dal 2020 in poi** (87 file), più la simulazione già
presente su Virtuale. Taglio deliberato: le slide in uso sono l'edizione 2023/24 e gli appelli
anteriori al 2020 misurano un programma precedente all'assetto attuale di lambda, `Optional` e
Stream. Il decennio 2010-2019 resta disponibile sul sito se dovesse servire.

⚠️ Tre appelli sono **linkati ma non scaricabili**: `2020-06-16`, `2024-06-12`, `2024-09-11`
rispondono 404 su tutti e tre i file. Verificato con richiesta diretta il 2026-09-14: è un
problema della pagina del docente, non dell'acquisizione. Da chiedere a lui se servono.

## Cosa manca

- **Libro di testo**: la scheda rimanda a un elenco sul portale del docente, non recuperato.
- Numerazione delle slide: mancano i numeri 18 e 19; da chiarire se corrispondono a materiale
  non pubblicato (vedi `percorso.md`).

## Note
- Testa di catena doppia: regge `IDS` (S2) e `WEB` (S3). È l'esame che non può slittare.
- Unico da 12 CFU della sessione: da solo vale il 40% dei CFU di S1.
