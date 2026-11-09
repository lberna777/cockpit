---
tags: [FI2, guida-lab]
---

# Scheda — FI2 LAB08: EDLift
**Materiale**: `LAB-08-EDLift.pdf` (sl. 1–51: 1ª parte sl. 1–37, 2ª parte sl. 38–50), `Lab08-EDLift-Startkit.zip` (view JavaFX e `Controller` pronti, 4 classi di test, **60 test**) · **Modalità**: guidata — la procedura la guida Lorenzo, Claude interviene solo se si ferma
**Teoria che entra qui** (moduli ancora ⬜, si aprono qui quando servono): `13` *Ereditarietà* — `extends` sl. 17–18, `protected` sl. 23–24, costruttori e `super(...)` sl. 33–38, ridefinizione e `@Override` sl. 59–62 · `14` *Polimorfismo* — il controller chiama `goToFloor` su un `Lift` e parte quello del sottotipo: sl. 36–39 · `20` *Classi astratte* — `abstract` sl. 3–5, classe derivata concreta sl. 7–8.

## Setup
- *Existing Projects* → *Select root directory* → `~/cockpit/Vault/UniCode/corsi/FI2/esame_FI2/da_importare/LAB08_EDLift-091126` → **Copy projects into workspace**; poi **rinomina il progetto** (il `.project` dice `Lab08-EDLift-Startkit`).
- Date pronte, **da non toccare**: `Lift` (astratta), `LiftState`, `RequestResult`, `Installation`, `controller`, `ui`. Da creare: `BasicLift`, `HealthyLift`, `MultiFloorLift` in `edlift.model`, `Queue` nel package **nuovo** `edlift.model.util` (lo vuole `QueueTest`).
- X rosse attese: `Lift.of` nomina **tutte e tre** le sottoclassi, quindi `Lift` e i test non compilano finché ne manca anche una. Primo passo: crea le tre classi «vuote» (costruttore + i due metodi astratti) e tutto compila. In `ui` restano rosse se JavaFX non è configurato: i test non ne hanno bisogno.
- Procedura: **prontuario §2**. Oggi la guidi tu, dal passo 1.

## Ordine di lavoro
| # | Classe | Cosa rappresenta | Test | Costrutto nuovo → slide |
|---|---|---|---|---|
| 1 | `BasicLift` | accetta una chiamata **solo se fermo** | `BasicLiftTest` (15) | `extends` + `super(...)` → 13 sl. 33–38; metodi astratti da concretizzare → 20 sl. 7–8; LAB sl. 15–16 |
| 2 | `HealthyLift` | ti lascia **un piano prima**, rifiuta se troppo vicino | `HealthyLiftTest` (17) | `MODIFIED` con `setMsg`/`setFloor` → LAB sl. 19, 27 |
| 3 | `util.Queue` | coda **FIFO** di interi su array, capacità fissa | `QueueTest` (8) | array + contatore (come LAB04c, LAB07); estrazione con ricopiatura → LAB sl. 42–45 |
| 4 | `MultiFloorLift` | accetta prenotazioni **anche in movimento**, le serve in ordine | `MultiFloorLiftTest` (20) | ha una `Queue` (composizione); ridefinisce `hasPendingFloors`/`nextPendingFloor` → LAB sl. 40–41 |

Parte 1 = righe 1–2 (in aula: 50 min, sl. 37); parte 2 = righe 3–4. Firme: le dettano `Lift` e i test, non inventarle.

## Casi limite da pensare
- Piano fuori dall'edificio (test `KO`: 11 e 1 su un edificio 2–10 → eccezione): `Lift` ha già un metodo `protected` che lo fa. Quale? Chi lo chiama, e **prima** di cosa?
- Basic: «fermo» corrisponde a quale valore di `LiftState`? Perché `ChiamataAccettata3` accetta una seconda chiamata?
- `getMode`: i test fanno `toUpperCase()`. La factory usa `"MULTIFLOOR"`, il test di `getMode` vuole `"MULTI"`: sono due cose diverse.
- Healthy: «distanza non superiore a 1» va presa con il segno o senza? Prova sui casi del test: da 5 → 6 rifiuta, da 5 → 3 accetta. E da 5 → 4?
- Healthy: il «piano prima» quando sali e quando scendi. Verifica: 5 → 7 dà **6**, 5 → 2 dà **3**.
- Healthy, `DueChiamate`: il test legge `RequestResult.MODIFIED.getFloor()`. Che cosa significa chiedere il piano **alla costante** dell'enum, e chi ce l'ha scritto? (sl. 27)
- Healthy in movimento: `REJECTED`, e `requestedFloor` non cambia (resta 5).
- Queue: dopo `extract` della testa, dove finiscono gli altri elementi? (sl. 44) ⚠️ Limiti del ciclo: `size` contro `length`, pattern 6, gli stessi errori del LAB04c e del LAB07.
- Queue vuota: cosa restituiscono `peek` ed `extract`? (sl. 45 e `testQueueOK`)
- Multi: la **prima** chiamata, a ascensore fermo, va in coda o no? Conta le chiamate in `QuintaPrenotazioneRifiutata`: quanto deve essere grande la coda?
- Multi rifiutato: messaggio e piano `Integer.MIN_VALUE` (sl. 40). `nextPendingFloor(state)`: lo stato conta? (commento in `testNextPendingFloorREST`)
- ⚠️ Pattern 2: hai finito quando passano **tutti i 60** test (tasto destro su `test` → *Run As → JUnit Test*), non il primo verde.

## Test rosso?
Non compila (package `util`, firma, manca una delle tre sottoclassi) · failure (leggi `expected / but was`) · error (eccezione dove non te l'aspetti: hai chiamato il controllo del piano **dopo** aver cambiato lo stato?) → prontuario §1, oppure scrivilo in chat.

## Dopo i test verdi
- copia `src` e `test` in `corsi/FI2/esame_FI2/svolti/LAB08_EDLift/`;
- apri `Lab08-EDLift-Soluzione.zip` e confronta: calcolo del «piano prima», `MODIFIED`/`REJECTED` con messaggio, `extract` della coda, capacità;
- Claude scrive `svolti/LAB08_EDLift/confronto_LAB08.md`; `/chiudi` aggiorna il prontuario (§ `model`: gerarchia astratta, `super(...)`, `@Override`, coda su array).
