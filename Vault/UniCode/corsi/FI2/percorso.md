# FI2 — Fondamenti di Informatica T-2 · percorso

> Mappa dei moduli e stato di dettaglio. Si carica **su necessità**, non a ogni sessione
> (`CLAUDE.md` §4). I concetti elencati qui sono un **indice per trovare il PDF, non una fonte
> da cui generare** (`lezione.md`, regola critica sulle fonti).
>
> Redatto il 2026-09-14 dall'inventario reale di `materiali/`, edizione **2023/24** del corso.
> Identificatore di modulo = numero della slide del docente. Uso: `/lezione FI2 13`.

**Stati**: ⬜ non aperto · 🔶 in corso · ✅ chiuso (esercizio della tipologia risolto **a freddo**,
codice che compila e passa i test — `CLAUDE.md` §7.2)

## Teoria — 45 moduli

| ID  | Titolo                                                  | Fonte in `materiali/slide/`                                              | Stato |
| --- | ------------------------------------------------------- | ------------------------------------------------------------------------ | ----- |
| 00  | Overview del corso                                      | `00-x1-Overview corso.pdf`                                               | ⬜     |
| S00 | Installazione JDK                                       | `Strumenti-00-InstallazioneJDK.pdf`                                      | ⬜     |
| S01 | Eclipse                                                 | `Strumenti-01-Eclipse intro.pdf`                                         | ⬜     |
| S02 | JUnit                                                   | `Strumenti-02-JUnit.pdf`                                                 | ⬜     |
| S04 | Installazione JavaFX                                    | `Strumenti-04-Installazione JavaFX.pdf`                                  | ⬜     |
| S05 | Produrre il JAR eseguibile                              | `Come produrre il JAR eseguibile.pdf`                                    | ⬜     |
| 01  | Dai linguaggi alle infrastrutture software              | `01-x1-Intro.pdf`                                                        | 🔶    |
| 02  | Linguaggio e piattaforma                                | `02-x1-Linguaggi e piattaforme.pdf`                                      | ⬜     |
| 02x | Esercitazione: tipi base                                | `02x-x1-Esercitazione Tipi base.pdf`                                     | ⬜     |
| 02z | Addendum: `main` in Java 21                             | `02z-Addendum-Main in Java21.pdf`                                        | ⬜     |
| 03  | Deployment                                              | `03-x1-Deployment.pdf`                                                   | ⬜     |
| 03x | Esercitazione: JAR                                      | `03x-x1-Esercitazione Jar.pdf`                                           | ⬜     |
| 04a | Componenti software in C                                | `04a-x1-Componenti sw in C.pdf`                                          | ⬜     |
| 04b | Classi e oggetti                                        | `04b-x1-Classi e oggetti.pdf`                                            | ⬜     |
| 05  | Riferimenti                                             | `05-x1-Riferimenti.pdf`                                                  | ⬜     |
| 06  | Stringhe e codice fiscale                               | `06-x1-Stringhe e codice fiscale.pdf`                                    | ⬜     |
| 07  | Array                                                   | `07-x1-Array.pdf`                                                        | ⬜     |
| 07x | Array in Java venendo dal C                             | `07x-x1-Esercitazione Array Java venendo dal C.pdf`                      | ⬜     |
| 08  | Package e namespace                                     | `08-x1-Package e namespace.pdf`                                          | ⬜     |
| 09  | Enumerativi                                             | `09-x1-Enumerativi.pdf`                                                  | ⬜     |
| 10  | Date e gestione del tempo                               | `10-x1-Date.pdf`                                                         | ⬜     |
| 11  | Formati e internazionalizzazione                        | `11-x1-Formati e internazionalizzazione.pdf`                             | ⬜     |
| 12  | Sistemi a oggetti                                       | `12-x1-Sistemi a oggetti.pdf`                                            | ⬜     |
| 12x | Esercitazione: display a 7 segmenti + orologio          | `12x-x1-Esercitazione Display a 7 segmenti+Orologio con display.pdf`     | ⬜     |
| 12z | Esercitazione: elezioni                                 | `12z-x1-Esercizitazione Elezioni.pdf`                                    | ⬜     |
| 13  | Ereditarietà                                            | `13-x1-Ereditarieta.pdf`                                                 | ⬜     |
| 14  | Polimorfismo                                            | `14-x1-Polimorfismo.pdf`                                                 | ⬜     |
| 15  | `equals` e `hashCode`                                   | `15-x1-Equals+hashCode.pdf`                                              | ⬜     |
| 16  | Wrapper per tipi primitivi                              | `16-x1-Wrapper per tipi primitivi.pdf`                                   | ⬜     |
| 17  | Record e data classes                                   | `17-x1-Record+Data classes.pdf`                                          | ⬜     |
| 20  | Classi astratte                                         | `20-x1-Classi astratte.pdf`                                              | ⬜     |
| 21  | Interfacce                                              | `21-x1-Interfacce.pdf`                                                   | ⬜     |
| 22  | Genericità e polimorfismo orizzontale                   | `22-x1-Genericità e polimorfismo orizzontale.pdf`                        | ⬜     |
| 23  | Interfacce standard                                     | `23-x1-Interfacce standard.pdf`                                          | ⬜     |
| 23x | Enumerativi + interfacce                                | `23x-x1-Enumerativi+interfacce.pdf`                                      | ⬜     |
| 24  | Null safety e `Optional`                                | `24-x1-Null safety.pdf`                                                  | ⬜     |
| 24x | Classi generiche                                        | `24x-x1-Classi generiche.pdf`                                            | ⬜     |
| 25  | Collection Framework                                    | `25-x1-Collection Framework.pdf`                                         | ⬜     |
| 25x | Collection nei compiti d'esame                          | `25x-x1-Collection nei compiti desame.pdf`                               | ⬜     |
| 25e | Eccezioni                                               | `25-x1-Eccezioni.pdf`                                                    | ⬜     |
| 26  | I/O in Java: generalità                                 | `26-x1-Gestione IO in Java-generalità.pdf`                               | ⬜     |
| 27  | I/O binario                                             | `27-x1-Gestione IO in Java-IObinario.pdf`                                | ⬜     |
| 28  | I/O testo                                               | `28-x1-Gestione IO in Java-IOtesto.pdf`                                  | ⬜     |
| 29  | I/O: complementi                                        | `29-x1-Gestione IO in Java-complementi.pdf`                              | ⬜     |
| 30  | Lambda expression — parte 1                             | `30-x1-Lambda expression-parte1.pdf`                                     | ⬜     |
| 31  | Grafica in JavaFX                                       | `31-x1-Grafica in JavaFX.pdf`                                            | ⬜     |
| 31x | Esercitazione CounterFX · JAR e JavaFX                  | `31x-x1-Esercitazione CounterFX.pdf`, `31x-x1-Runnable Jar e JavaFX.pdf` | ⬜     |
| 32  | Lambda expression — parte 2                             | `32-x1-Lambda expression-parte2.pdf`                                     | ⬜     |
| 33  | Varianza e wildcard                                     | `33-x1-Varianza e wildcard.pdf`                                          | ⬜     |
| 33x | Principio di sostituzione di Liskov                     | `33x-x1-Principio di sostituzione di Liskov.pdf`                         | ⬜     |
| 34  | Strutture dati ad albero                                | `34-x1-Alberi.pdf`                                                       | ⬜     |
| 34x | Esercitazione ValExp — espressioni, operandi, operatori | `34x-x1-Esercitazione ValExp.pdf`                                        | ⬜     |
| 35  | Functional programming e Stream                         | `35-x1-Functional programming e Stream.pdf`                              | ⬜     |
| 36  | Numeri reali                                            | `36-x1-Numeri reali.pdf`                                                 | ⬜     |
| 37  | Moduli Java                                             | `37-x1-Moduli new.pdf`                                                   | ⬜     |
| 40  | EXTRA — mini-introduzione ad Android                    | `40-Android.pdf`                                                         | ⬜     |

> ⚠️ **Collisione di numerazione nella fonte**: il docente ha usato il numero 25 sia per
> «Collection Framework» sia per «Eccezioni». Qui le Eccezioni prendono l'identificatore `25e`.
> Mancano dalla numerazione i numeri 18 e 19: da verificare se corrispondono a materiale non
> pubblicato o a un semplice salto.

## Laboratorio — 13 esercitazioni (`materiali/lab/`)

| ID | Titolo | Materiale |
|---|---|---|
| LAB00 | Introduzione | `LAB-00-Intro.pdf` |
| LAB01 | Linea di comando, mini esempi | `LAB-01-LineaDiComando-MiniEsempi.pdf` |
| LAB02 | Frazione — prima parte | slide + startkit + soluzione |
| LAB03 | Frazione — seconda parte | slide + startkit + soluzione |
| LAB04 | Insiemi di frazioni (a/b/c) | slide + 3 startkit + 3 soluzioni |
| LAB05 | TicketSosta | slide + startkit + soluzione |
| LAB06 | MasterMind | slide + startkit + soluzione |
| LAB07 | MyCalendar | slide + recap + commento + startkit + soluzione + FXView |
| LAB08 | EDLift | slide + startkit + soluzione |
| LAB09 | MyMedia | slide + startkit + soluzione |
| LAB10 | Bussy | slide + startkit + soluzione |
| LAB11 | Agenda — dati e persistenza | slide + startkit + soluzione |
| LAB12 | Flights — UI | intro + testo + startkit + soluzione |
| LAB13 | Oroscopi | slide + startkit + soluzione |

## Esercizi autonomi (`materiali/esercizi/`)

Persona · JUnit · uso di NaN · Matrici (testo, startkit, soluzione) · PhonePlan (testo,
startkit, soluzione, commento) · Battaglia Navale (slide, UML, startkit, soluzione) ·
ZannoTassametro (testo, startkit, soluzione) · BinaryBasicPersistence · Media-IOBinario
(soluzione) · MyCalendar-IOBinario (soluzione) · FormeGeometricheConInterfacce.

## Prove (`prove/`) — 30 sessioni complete

Ogni riga: testo, start kit e **soluzione ufficiale del docente**. Fonte: archivio pubblico di
Denti, `VecchiEsami`, scaricato il 2026-09-14 (dal 2020 in poi).

| Appello | File | Usata il | Note |
|---|---|---|---|
| 05/06/2024 | `2024-06-05-SimulazioneEsame*` | — | simulazione, da Virtuale |
| 09/01/2020 | `2020-01-09-Testo.pdf` · `-StartKit.zip` · `-Soluzione.zip` | — |  |
| 06/02/2020 | `2020-02-06-Testo.pdf` · `-StartKit.zip` · `-Soluzione.zip` | — |  |
| 07/07/2020 | `2020-07-07-Testo.pdf` · `-StartKit.zip` · `-Soluzione.zip` | — |  |
| 23/07/2020 | `2020-07-23-Testo.pdf` · `-StartKit.zip` · `-Soluzione.zip` | — |  |
| 09/09/2020 | `2020-09-09-Testo.pdf` · `-StartKit.zip` · `-Soluzione.zip` | — |  |
| 13/01/2021 | `2021-01-13-Testo.pdf` · `-StartKit.zip` · `-Soluzione.zip` | — |  |
| 04/02/2021 | `2021-02-04-Testo.pdf` · `-StartKit.zip` · `-Soluzione.zip` | — |  |
| 15/06/2021 | `2021-06-15-Testo.pdf` · `-StartKit.zip` · `-Soluzione.zip` | — |  |
| 06/07/2021 | `2021-07-06-Testo.pdf` · `-StartKit.zip` · `-Soluzione.zip` | — |  |
| 22/07/2021 | `2021-07-22-Testo.pdf` · `-StartKit.zip` · `-Soluzione.zip` | — |  |
| 14/09/2021 | `2021-09-14-Testo.pdf` · `-StartKit.zip` · `-Soluzione.zip` | — |  |
| 14/01/2022 | `2022-01-14-Testo.pdf` · `-StartKit.zip` · `-Soluzione.zip` | — |  |
| 31/01/2022 | `2022-01-31-Testo.pdf` · `-StartKit.zip` · `-Soluzione.zip` | — |  |
| 14/06/2022 | `2022-06-14-Testo.pdf` · `-StartKit.zip` · `-Soluzione.zip` | — |  |
| 05/07/2022 | `2022-07-05-Testo.pdf` · `-StartKit.zip` · `-Soluzione.zip` | — |  |
| 22/07/2022 | `2022-07-22-Testo.pdf` · `-StartKit.zip` · `-Soluzione.zip` | — |  |
| 14/09/2022 | `2022-09-14-Testo.pdf` · `-StartKit.zip` · `-Soluzione.zip` | — |  |
| 13/01/2023 | `2023-01-13-Testo.pdf` · `-StartKit.zip` · `-Soluzione.zip` | — |  |
| 08/02/2023 | `2023-02-08-Testo.pdf` · `-StartKit.zip` · `-Soluzione.zip` | — |  |
| 12/06/2023 | `2023-06-12-Testo.pdf` · `-StartKit.zip` · `-Soluzione.zip` | — |  |
| 05/07/2023 | `2023-07-05-Testo.pdf` · `-StartKit.zip` · `-Soluzione.zip` | — |  |
| 26/07/2023 | `2023-07-26-Testo.pdf` · `-StartKit.zip` · `-Soluzione.zip` | — |  |
| 13/09/2023 | `2023-09-13-Testo.pdf` · `-StartKit.zip` · `-Soluzione.zip` | — |  |
| 17/01/2024 | `2024-01-17-Testo.pdf` · `-StartKit.zip` · `-Soluzione.zip` | — |  |
| 14/02/2024 | `2024-02-14-Testo.pdf` · `-StartKit.zip` · `-Soluzione.zip` | — |  |
| 03/07/2024 | `2024-07-03-Testo.pdf` · `-StartKit.zip` · `-Soluzione.zip` | — |  |
| 25/07/2024 | `2024-07-25-Testo.pdf` · `-StartKit.zip` · `-Soluzione.zip` | — |  |
| 15/01/2025 | `2025-01-15-Testo.pdf` · `-StartKit.zip` · `-Soluzione.zip` | — | **riserva — verifica finale** |
| 12/02/2025 | `2025-02-12-Testo.pdf` · `-StartKit.zip` · `-Soluzione.zip` | — | **riserva — verifica finale** |

**Come si spende questo archivio.** Ventinove prove con soluzione cambiano il metodo: non si
tratta più di conservare l'unica traccia disponibile, ma di **ricavare dai testi le tipologie
ricorrenti** — quali strutture dati compaiono, quali pattern di I/O, quanto JavaFX, come è
formulata la parte a oggetti — e costruire il curricolo su quelle, che è la regola di
`CLAUDE.md` §7.3. Gli ultimi due appelli, **15/01/2025 e 12/02/2025**, restano di riserva:
sono i più vicini per forma a quello che troverai a gennaio 2027 e vanno spesi come prova
fredda cronometrata di verifica finale, non nello studio corrente.

Le tre sessioni `16/06/2020`, `12/06/2024` e `11/09/2024` sono linkate dal sito ma i file
rispondono 404: vedi `fonti.md`.
