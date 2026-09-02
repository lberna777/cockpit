# Riallineamento dei dodici comandi — inventario di lettura

> Redatto il 2026-09-02, prima di riscrivere qualsiasi comando. Ogni file in
> `.claude/commands/` è stato letto per intero. Questo documento separa la **logica da
> preservare** (il valore accumulato in mesi d'uso) dai **riferimenti da riscrivere**
> (percorsi e materie cablate, superati dal riordino e dall'architettura di continuità).

## Sostituzioni meccaniche, valide per tutti i file

| Vecchio | Nuovo |
|---|---|
| `stato/errori_frequenti.md` | `profilo/errori.md` |
| `stato/log_sessioni.md` | `log/AAAA-MM.md` |
| `stato/tracker_ripasso.md` | `stato/tracker.md` |
| `ESAMI SCELTI.md` | `piano/piano_laurea.md` |
| `claudeLezioni/LEZIONI <MATERIA>/` | `corsi/<CODICE>/lezioni/` |
| `claudeAppunti/APPUNTI <MATERIA>/` | `corsi/<CODICE>/appunti/` |
| `APPUNTI GREZZI/<materia>/` | `corsi/<CODICE>/grezzi/` |
| `SLIDE TEORIA/<SIGLA>/`, `SLIDE LAB/<SIGLA>/` | `corsi/<CODICE>/materiali/` |
| `SIMULAZIONI ESAMI/<SIGLA>/` | `corsi/<CODICE>/prove/` |
| `/home/lorenzo/UniCode/...` (path assoluti) | percorsi relativi alla radice risolta |
| tre materie cablate (`dir`/`sys`/`sec`) | dodici codici da `piano/codici.txt` |
| date d'esame cablate (16/06, 22/06, 17/07 2026) | sessioni da `piano/piano_laurea.md` |

Il prefisso dell'ID non basta più a dedurre il corso: con dodici codici serve leggere
`piano/codici.txt`. La forma diventa `<CODICE>` + `<ID modulo>` (es. `FI2 3A`), oppure
il codice si desume dal corso attivo in `stato/corrente.md`.

---

## Logica da preservare, file per file

### `lezione.md` — il file più denso, 222 righe
- **Formato vincolante per gli esami pratici** (dichiarato "da feedback di Lorenzo"): prosa
  discorsiva ancorata ai comandi/file concreti, **non** un walkthrough. Ogni comando
  spiegato a **due livelli** — il meccanismo in piccolo, la visione in grande (dove si
  inserisce, perché esiste, quale superficie apre).
- **Confine esplicito con `/lab`**: «se stai scrivendo "esegui questo, poi quello, output X"
  → è materia di `/lab`». Da tenere parola per parola.
- **REGOLA CRITICA sulle fonti**: il contenuto viene solo dai PDF letti; i concetti chiave in
  `percorso.md` sono un **indice per trovare i PDF, non una fonte da cui generare**. Nessun
  comando inventato fuori dai PDF. Se un PDF manca: fermarsi ed elencare i titoli esatti.
- **Regola Diritto**: terminologia del PDF riprodotta, non parafrasata; `[fonte: PDF]` sulle
  affermazioni riprese; nessuna integrazione da fonti esterne; registro accademico-giuridico.
  Generalizzabile a qualunque corso con un docente di riferimento.
- **Tre template completi** (pratico-lab / teorico / giuridico) con sezioni fisse.
- Nota esame Security: quiz teorico 40% **con penalità per risposta errata** → l'avvertenza
  "se non sei sicuro non rispondere" nelle autoverifiche. Si generalizza ai corsi con quiz.
- Checklist interna di qualità, poi `lorenzo-skills:unicode-output-gate`.
- Chiusura con `lorenzo-skills:unicode-link-note` per il blocco AUTO-LINKS.

### `lab.md` — 217 righe
- **"Anatomia del comando"**, su quattro assi: *cosa stai scrivendo* · *perché lo stai
  scrivendo* (nella catena «che informazione ho → cosa cerco → quale comando la trova») ·
  *con che parametri* · *come potresti riscriverlo*. Fine dichiarato: **saperlo riscrivere a
  memoria all'esame, non copiarlo.** È il cuore del comando.
- **«Lorenzo digita tutti i comandi. La guida li fornisce, non li esegue.»** Ripetuto due volte.
- Struttura fissa per esercizio: Obiettivo · Concetto minimo · Comandi · Anatomia · Output
  atteso · Cosa verificare. Progressione facile → difficile nell'ordine del PDF.
- Security: **snapshot obbligatorio** prima di ogni esercizio di compromissione; threat model
  a due prospettive (attaccante e difensore).
- Sezione **"Famiglia d'esame"** per i moduli ⭐: tipologia + rimando alla prova passata
  correlata, da eseguire al termine del lab.
- **Unico comando già aggiornato al riordino**: cita `ARCHIVIO/sysAdmin-lab-vagrant` con il
  percorso nuovo. È qui che sopravvive il comando VM di `LAS`.

### `appunti.md` — 123 righe
- Tripartizione dell'analisi del grezzo: **domande aperte** · **lacune** · **punti di forza**.
- **«L'assenza può essere intenzionale (sezione consolidata), non marcarla come lacuna.»**
  Corrisponde all'omissione deliberata in `profilo/studente.md`.
- Risposte alle domande **inline come blockquote**, subito dopo il concetto di riferimento —
  non raccolte in fondo.
- Marcatori: `> ⚠️` per sezione mancante o errore, `> ✅ Ottima osservazione` per i punti di
  forza («segnalarli positivamente rafforza l'apprendimento»).
- Per un bug che ripete un pattern noto: rimando esplicito al modulo dove era già emerso.
- Criterio di avanzamento a ✅ **con evidenza pratica**, non dichiarata.
- Checklist interna, poi `unicode-output-gate`, poi `unicode-link-note`.

### `ripassa.md` — 82 righe
- **5 domande nuove, diverse dall'autoverifica della lezione.** Vincoli di composizione:
  almeno una su un **errore ricorrente**, almeno una di **collegamento fra moduli**;
  difficoltà 2 base / 2 intermedio / 1 avanzato.
- Differenziazione: 2 domande di previsione dell'output di un comando per i corsi pratici;
  2 che richiedono la citazione della norma per quelli giuridici. Da generalizzare per tipo
  di verifica, non per nome di materia.
- **Interrogazione una domanda alla volta**, attendendo la risposta. Tre esiti distinti:
  corretta / parziale / errata, ciascuno con un trattamento diverso.
- Nuove debolezze emerse → aggiornano `profilo/errori.md`.

### `simula.md` — 91 righe
- **Soglia di fattibilità**: almeno 3 moduli ✅, altrimenti rimanda a `/ripassa`.
- Se esiste una prova passata reale, si usa quella invece di generare domande.
- Punteggio **0-3 per risposta** (incompleta / parziale / corretta / eccellente).
- **Sotto il 60% → piano di ripasso mirato**, non solo un voto.

### `chiudi.md` — 100 righe
- Raccolta delle informazioni in **una sola domanda compatta**, differenziata per tipo di
  esame (lab con VM vs. teoria).
- Criterio ✅ rigoroso: per i lab **solo se gli esercizi sono stati eseguiti in prima
  persona**; per la teoria solo con autoverifica risposta e grezzi scritti.
- Aggiornamento di glossario e `troubleshooting_vm.md` quando emergono termini o problemi nuovi.
- **Cambia natura**: non è più obbligatorio (CLAUDE.md §5.4). Aggiunge il giudizio, non il fatto.

### `verifica.md` — 75 righe
- Confronto della copertura **contro il PDF sorgente**, con conteggio dei concetti.
- Controllo simmetrico: nessun concetto mancante **e nessuno aggiunto** che non sia nel PDF.
- Per i corsi giuridici: verifica della terminologia **parola per parola**.
- Coerenza incrociata lezione ↔ appunti ↔ percorso del corso.
- **Chiede prima di applicare** le correzioni. Da mantenere.

### `piano.md` · `sessione.md` · `stato.md` · `lacune.md` — i quattro di orientamento
- **Priorità unica e condivisa**: il ripasso scaduto viene **sempre per primo** (15-20 min),
  poi la materia più a rischio (moduli rimasti / giorni rimasti), poi il modulo aperto.
- **«Una sola azione, non un elenco di blocchi»** e **«non aggiungere testo libero»**:
  vincoli di forma che tengono l'output leggibile. Da preservare alla lettera.
- `lacune.md`: bilancio **ore stimate rimanenti vs. ore disponibili**, con surplus/deficit.
  Va ripensato: il piano si verifica su **blocchi settimanali di programma coperto, mai su
  ore giornaliere** (`profilo/studente.md`). Il calcolo resta, l'unità cambia.
- `lacune.md`: pattern d'errore attivi = quelli che compaiono in **2+ moduli**.
- `sessione.md`: non ricaricare lo stato se già in contesto; non riproporre ciò che è già
  stato fatto nella conversazione in corso.
- `stato.md`: barre di avanzamento calcolate, non inventate.

### `pdf-batch.md` — 49 righe
- `pandoc --pdf-engine=xelatex -V geometry:margin=2.5cm -V fontsize=11pt -V lang=it`.
- Su fallimento di un file: segnalare e **continuare** con gli altri.
- Commit e push in coda alla conversione.

---

## Da aggiungere: i marcatori

`/chiudi` e `/appunti` devono appendere a `stato/giornata.md` le righe di evento nella forma:

```
HH:MM · <CODICE> · <fatto in una riga>. CHIUSO <cod> <mod>
HH:MM · <CODICE> · <fatto in una riga>. RIPASSO <cod> <mod> ok|debole
```

È da questi marcatori che `scripts/giornata.py` fa avanzare `stato/tracker.md` alle 23.

**Conseguenza sul disegno**: il tracker ha ora **un solo scrittore**, `giornata.py`. Il passo 6
di `ripassa.md` e il passo 5 di `chiudi.md`, che oggi lo modificano a mano, vanno sostituiti
con la scrittura del marcatore. Due scrittori sullo stesso file riporterebbero il problema che
l'architettura è stata costruita per eliminare.

---

## Esito — 2026-09-02

Tutti e dodici riscritti. Da 1.220 a 1.475 righe.

**Decisioni prese da Lorenzo in questa sessione:**
1. Il tracker ha un solo scrittore per i ripassi. `/chiudi` scrive subito la riga completa dei
   moduli **chiusi** (idempotente al ricontrollo delle 23) e per i **ripassati** aggiorna solo
   *Ultimo ripasso*, lasciando gradino e scadenza al consolidamento — che avanza di un gradino
   a partire dal valore che trova, e raddoppierebbe l'intervallo se qualcuno l'avesse già mosso.
   `/ripassa` e `/simula` scrivono solo il marcatore.
2. Argomento esplicito: `<CODICE> <ID modulo>`, codice validato contro `piano/codici.txt`.
   Niente deduzione del corso dal prefisso dell'ID.
3. PDF in una cartella separata: `corsi/<COD>/pdf/{lezioni,appunti}/`.

**Generalizzazioni fatte.** I tre registri di `lezione.md` e i due template di `lab.md` non sono
più per materia (SysAdmin / Security / Diritto) ma per **tipo di verifica**: laboratorio
pratico, esercizi formali, corso discorsivo con docente di riferimento. Il tipo si legge da
`corsi/<COD>/percorso.md`, non si indovina. `lab.md` ha in più un template per gli esercizi
formali che prima non esisteva: l'anatomia del comando diventa anatomia del passaggio — cosa
fai, perché lì, quale ipotesi usi, cosa cambierebbe se cadesse.

**Aggiunte rispetto alla versione precedente:**
- `lab.md` §Deliverable: dove l'ambiente viene ripristinato, i file e gli screenshot vanno
  catturati sull'host **durante** l'esercizio. Deriva da una perdita reale in un lab con revert.
- `appunti.md` §5: un errore che ricorre in 3+ moduli, o che si ripresenta su un corso diverso,
  va **promosso a trasversale** in `profilo/errori.md`. È la sezione che il briefing carica per
  prima.
- `lezione.md` §2 e `verifica.md` §2: se `fonti.md` segnala materiale di un'annata diversa da
  quella in cui il corso era in piano, va dichiarato nell'output e le differenze non vanno
  contate come lacune.
- `lacune.md` §6: il checkpoint delle sei settimane produce una decisione esplicita di carico.

**Falsi positivi noti del doctor.** Continua a segnalare `corrente.md` in `appunti`, `chiudi`,
`lab`, `lezione`, `stato`: sono **scritture** dello stato attivo, legittime, più la lettura
integrale in `/stato` — il briefing tronca `corrente.md`, quindi per il riepilogo completo va
riletto. Le quattro letture davvero ridondanti sono state rimosse.
