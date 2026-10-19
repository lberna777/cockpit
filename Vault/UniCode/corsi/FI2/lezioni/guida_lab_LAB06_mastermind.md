# Scheda — FI2 LAB06: MasterMind
**Materiale**: `LAB-06-MasterMind.pdf` (sl. 1–43), `Lab06-MasterMind-Startkit.zip` (3 enum pronti, `controller` e `ui` pronti, 8 classi di test, 19 test) · **Modalità**: guidata
**Teoria che entra qui**: `09` ⬜ *Enumerativi* — `ordinal()`, `values()` (09 sl. 13–15) · `12` ⬜ *Sistemi a oggetti* — package per funzionalità model/controller/ui (LAB06 sl. 9–12) · `06` 🔶 `StringJoiner` (06 sl. 48–50) · `07` ⬜ `java.util.Random`, `nextInt` (07 sl. 60–61). Non in mappa ma richiesti dai test: `equals` fra oggetti (come in LAB02) e una **classe anonima** che ridefinisce un metodo (anticipo di `13`, 5 righe in chat quando ci arrivi).

## Setup
- *Existing Projects* → *Select root directory* → `~/cockpit/Vault/UniCode/corsi/FI2/esame_FI2/da_importare/LAB06_MasterMind-191026` → **Copy projects into workspace**; poi **rinomina il progetto**.
- Due source folder: `src` e `test` (singolare, non `tests` come LAB05) [sl. 41]. X rosse attese: mancano `Combinazione`, `Risposta`, `Gioco`, `MasterMind` (package `mastermind.model`) [sl. 42].
- ⚠️ Il `.classpath` chiede due librerie utente JavaFX (`JavaFX 17.0.1`, `JavaFX19`): se non le hai, `controller` e `ui` restano rossi **anche a modello finito**. I test del modello girano lo stesso (Eclipse chiede «errors exist… proceed?» → *Proceed*). Per lanciare il gioco: `Strumenti-04-Installazione JavaFX.pdf`, poi run su `MasterMindApp` [sl. 41].
- Prima di scrivere codice: la **procedura d'esame** fissata il 5/10 (testo e test → caso a mano → passi → codice a pezzi → casi tuoi → stampe se rosso). La costruiamo in chat su `Combinazione` e la proviamo su `MasterMind`.

## Ordine di lavoro
| # | Classe | Cosa rappresenta | Test che la coprono | Costrutto nuovo → slide |
|---|---|---|---|---|
| 1 | `Combinazione` | array di `PioloDiGioco`, nato tutto `VUOTO`; `dim`, `getPiolo`, `setPiolo`, `equals`, `toString` | `CombinazioneTest` (6) | `StringJoiner(",")` → 06 sl. 49; sl. 17 |
| 2 | `Risposta` | gemella su `PioloRisposta` + `vittoria()` | `RispostaTest` (6) | sl. 18 |
| 3 | `Gioco` | piano di gioco: due array paralleli tentativi/risposte, contatore, `Status` | `GiocoTest` (3) | `\t`, `System.lineSeparator()` → sl. 20–23 |
| 4 | `MasterMind` | il codice segreto e `calcolaRisposta` | `MasterMindTest1`–`3` (4 di cui 1 ripetuto ×5) | `ordinal()` come indice → sl. 34; `Random` → 07 sl. 61 |

Firme: dai test (`dim()` su Combinazione/Risposta, ma **`dimensione()`** su `Gioco`) e dal `Controller`, che chiama anche `situazione()`. Algoritmo dei piolini: sl. 6 e 28–33.

## Casi limite da pensare
- `ultimoTentativo()` **prima** di ogni mossa: cosa restituisce? (`MasterMindTest1.testSorteggioIniziale`)
- Ordine dei piolini nella `Risposta`: dove vanno i neri, dove i bianchi, cosa resta nelle celle in avanzo? Leggi l'atteso `NERO,NERO,BIANCO,VUOTO` (`MasterMindTest2`). `equals` confronta **posizione per posizione**.
- Tabulazioni: due, o tre se la combinazione è lunga **< 20** [sl. 22]. Quanto è lunga `"ROSSO,GIALLO,VERDE,BLU"`? E `"BLU,BLU,BLU,BLU"`? (⚠️ pattern 6: conta a mano).
- `registraMossa` all'ultimo tentativo: se la risposta è vincente, `VITTORIA` o `PERSO`? In che ordine controlli? (`MasterMindTest3`, `Gioco(5,4)`)
- Sorteggio: l'enum ha 7 valori, `VUOTO` è l'indice 0 e non va sorteggiato [sl. 26]. Che estremi dai a `nextInt` perché esca 1…6 e mai 0 né 7? (⚠️ pattern 6: la slide scrive «1..7», derivalo da `values().length`)
- Colori ripetuti: sl. 31–33 hanno tre casi, calcolali a mano **prima** di scrivere `occorrenze` (atteso: neri e bianchi per ciascuno).
- `sorteggiaCombinazione` deve poter essere **ridefinito** dai test: che visibilità serve? (la slide 25 la dice prima «protetta» poi «privata»: vince il test).
- ⚠️ Pattern 2: finito quando passano **tutti** i 19 test; più un caso tuo, calcolato a mano.

## Test rosso?
Non compila (firma/nome/package) · failure (guarda l'atteso: virgole senza spazi, `\t` contati, `VUOTO` in coda) · error (`NullPointerException`: array non riempito di `VUOTO`) → prontuario §1, oppure scrivilo in chat.

## Dopo i test verdi
- copia `src` e `test` in `corsi/FI2/esame_FI2/svolti/LAB06_MasterMind/`;
- apri `Lab06-MasterMind-Soluzione.zip` e confronta: rappresentazione, ordine dei controlli in `registraMossa`, `occorrenze`, estremi del sorteggio;
- Claude scrive `svolti/LAB06_MasterMind/confronto_LAB06.md`; `/chiudi` aggiorna il prontuario (§ `model`: enum come indice, `StringJoiner`, classe anonima nei test).
