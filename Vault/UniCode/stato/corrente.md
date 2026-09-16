# Stato Corrente — Studio Attivo

**Esame attivo**: `FI2` — Fondamenti di Informatica T-2 (12 CFU) | **Aggiornato**: 2026-09-16

> Un solo esame in fase attiva (`piano/piano_laurea.md`, regola 4). Gli altri tre di S1 —
> `CALC`, `MATAP`, `ELT` — hanno cartella, fonti e percorso pronti, e restano in attesa.
> Lo stato di `LAS` è archiviato in `corsi/LAS/stato.md`.

## Perché FI2

Testa di catena doppia: regge `IDS` in S2 e `WEB` in S3. Vale 12 CFU sui 30 della sessione, e
la sua verifica è pratica — codice che compila e passa i test — quindi è quella che richiede
più tempo di esecuzione e meno di lettura. È l'esame che non può slittare.

## Stato dei moduli

- 57 moduli di teoria, 13 esercitazioni di laboratorio, 11 esercizi autonomi.
- ✅ **01** «Dai linguaggi alle infrastrutture software» — chiuso il 2026-09-16 (criterio *teoria*,
  verifica a voce a libro chiuso: d.2 parziale, d.3 buona, d.4 buona, black-box/white-box parziale
  recuperata con guida; `mvn package` saltata). Primo ripasso dovuto il 2026-09-19.
- Tutti gli altri: non aperti.
- Materiale completo in `corsi/FI2/materiali/`; mappa in `corsi/FI2/percorso.md`.
- Edizione del materiale: 2023/24, quella d'iscrizione.

## Prossimo passo esatto

`/lezione FI2 02` — «Linguaggio e piattaforma», fonte `materiali/slide/02-x1-Linguaggi e
piattaforme.pdf`. A seguire `04b`, che apre la parte a oggetti. Il modulo `00` è la sola overview
del corso: si legge, non si studia.

Al primo ripasso di 01 (2026-09-19) verificare **per primi** i due punti rimasti deboli, che hanno
la stessa radice — *da dove nasce* la cosa:
- **error** JUnit: eccezione imprevista **durante l'esecuzione**, l'asserzione non viene raggiunta
  (non «la struttura», che è a posto perché il codice ha compilato);
- **black-box / white-box**: il caso si ricava dalla **specifica** o dal **codice**; entrambi
  controllano il risultato.

## Punti aperti su questo corso

1. Numeri 18 e 19 assenti dalla numerazione delle slide: da chiarire.
1b. La «struttura formale» di Java (da cosa è composto il linguaggio) resta poco chiara a Lorenzo,
    che la giudica poco rilevante per l'esame: non è prioritaria, ma i moduli 02, 04b e 12 la
    costruiscono in modo operativo, quindi va ripresa lì e non in astratto.
1c. Il versioning è il punto in cui l'esperienza pregressa (GitHub) ha agganciato la teoria:
    Lorenzo vuole approfondirlo. Il corso non ci torna sopra (solo 01 sl. 5–12).
1d. Maven (`mvn package`, perché può non produrre il JAR): rimandato da Lorenzo il 2026-09-16 al
    momento in cui servirà. Il corso gli dedica una sola slide (01 sl. 17) e all'esame si consegna
    un progetto Eclipse: non è una lacuna d'esame.
2. Libro di testo dichiarato in scheda ma non reperito.

## Archivio delle prove — acquisito

**30 sessioni complete** con testo, start kit e soluzione ufficiale (2020-01 → 2025-02), in
`prove/`. Il curricolo si costruisce sulle tipologie ricorrenti che emergono da questi testi
(`CLAUDE.md` §7.3). `15/01/2025` e `12/02/2025` restano di riserva per la verifica finale.
