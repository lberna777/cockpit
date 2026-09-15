# Template — integrity.txt (Integrity check & privilege escalation)

> Struttura riutilizzabile per il resoconto testuale richiesto negli esercizi di tipo
> Integrity check & privilege escalation (S11, famiglia `changeN`/pacchetti `.deb`). Ogni
> sezione ha, tra `[ ]`, **da dove** ricavare l'informazione e **con quale comando/azione**.
> Vedi `modello_integrity_privesc.md` per le soluzioni ufficiali di tutte le varianti del pool,
> `guida_esame_privesc.md` per il triage per vettore (SUID/capability/ACL/sudoers/...), e
> `esercizi/SICINF/privesc_2026-07-14_change4/integrity.txt` per un esempio reale compilato
> da zero (capability `cap_dac_override` su `tee`).

```
INTEGRITY.TXT — Esercizio <data esercizio> (<nome file/pacchetto: changeN, change_AAAA_MM_GG, o .deb>)
Integrity check & privilege escalation — Fase 1

===========================================================
STRATEGIA — procedura generale per trovare le modifiche
(riga fissa, riusabile per ogni variante della famiglia — cambia solo se hai
usato strumenti diversi da AIDE)
===========================================================

1. Config AIDE (PRIMA di tutto — Gate A):
   In /etc/aide/aide.conf, commentare la riga
     @@x_include /etc/aide/aide.conf.d ^[a-zA-Z0-9_-]+$
   (il preset di default NON copre /usr/bin), e aggiungere in fondo al file:
     /usr/bin f Full
     /etc f Full
   Sintassi: "f" da solo, NESSUN trattino prima ("/usr/bin -f Full" non è valido).
   Farlo PRIMA di creare la baseline: se la baseline si crea con le modifiche già
   presenti, il confronto successivo non le rileva.

2. Baseline sul sistema pulito:
     sudo aideinit
     sudo cp /var/lib/aide/aide.db.new /var/lib/aide/aide.db

3. Eseguire il file/pacchetto fornito:
     chmod +x <nomefile>      [solo se changeN eseguibile; per .deb: sudo dpkg -i <pacchetto>.deb]
     sudo ./<nomefile>

4. Confrontare:
     sudo aide -C -c /etc/aide/aide.conf

5. Leggere la riga di sintesi di ogni entry cambiata (formato "f X.... .c....X .+ : /path"):
   [vedi guida_esame_privesc.md §... per la lettura posizionale completa: p=permessi,
   A=ACL, X=xattr/capability, c=ctime, m=mtime — "c" da solo è RUMORE]

6. Per OGNI file segnalato (Gate B — non fermarsi al primo), verificare con il comando
   giusto se è un vettore reale o un vicolo cieco:
   [X/xattr -> getcap <file> (output vuoto "path =" = falso positivo, capability
   svuotata) | A -> getfacl <file> | p su binario senza altro -> ls -l (SUID nuovo?)
   | un privilegio TOLTO non è mai un vettore]

===========================================================
RISULTATO — diff AIDE (<N> entry modificate su <TOT> totali)
===========================================================

[incolla qui le righe di sintesi grezze di `sudo aide -C`, una per file segnalato]

===========================================================
ANALISI FILE PER FILE
===========================================================

1. <path/file>
   Diff: [cosa dice AIDE - attributo cambiato, valore prima -> dopo]
   Verifica: [comando eseguito -> output]
   -> [RUMORE puro / FALSO POSITIVO (con perché) / privilegio tolto, vicolo cieco /
       VETTORE REALE (con perché dà davvero un potere nuovo)]

2. <path/file>
   ...

N. <path/file>
   ...

===========================================================
CONCLUSIONE FASE 1
===========================================================

Su <N> file segnalati da AIDE: <M> sono rumore/falsi positivi/vicoli ciechi (elenco
sintetico del perché ciascuno è stato scartato), <K> è/sono il vettore reale:
<path> ha ottenuto <SUID / capability X / ACL / voce sudoers>, che permette di
<cosa concede in pratica — scrivere un file specifico, eseguire come root, ecc.>.

===========================================================
FASE 2 — EXPLOIT (come <utente base>, senza sudo)
===========================================================

Consegna: [trascrivi cosa chiede l'esercizio — nome utente da creare, password
richiesta o a scelta, oppure "diventare root senza usare il potere sudo di <utente>"]

[SOLO se il vettore è una capability tipo cap_dac_override/cap_fowner su un binario:]
Perché non un redirect diretto:
  echo "..." >> /etc/passwd    # Permission denied
fallisce perché è la SHELL ad aprire il file per il redirect, e la shell ha solo i
permessi normali di <utente>. La capability è attaccata al binario, non a chi lo
lancia: si attiva solo quando è il binario stesso ad aprire il file di destinazione
(pattern: pipe verso il binario privilegiato, mai redirect diretto sul file protetto).

Comandi eseguiti:

  [ogni comando + il suo output, con un commento breve su COSA fa e PERCHÉ è quel
  comando in quel punto — non solo la sequenza cruda. Tipicamente:
  1) generare l'hash della password (openssl passwd [-1] [-salt <salt>] <password>)
  2) copiare il file protetto in una posizione scrivibile
  3) editare la copia aggiungendo la riga utente:hash:0:0:gecos:/root:/bin/bash
  4) usare il vettore per sovrascrivere il file protetto con la copia modificata
  5) verifica (grep dell'utente nel file, o cat)
  6) su <utente creato> -> id (prova finale uid=0)]

Screenshot: privesc.png (comandi di verifica richiesti dalla consegna + prova uid=0).

===========================================================
PERCHÉ FUNZIONA (meccanismo)
===========================================================

[spiega IL MECCANISMO, non solo i comandi: perché il controllo Unix normale viene
bypassato (SUID = eredita i privilegi del proprietario del file eseguibile,
capability = bypassa uno specifico controllo del kernel indipendentemente da chi
esegue, ACL/sudoers = permesso esplicito extra oltre ai permessi standard), e
perché il formato scelto per la riga in /etc/passwd è valido (hash inline nel 2°
campo = formato storico, il sistema non consulta /etc/shadow se il campo non è "x")]
```

## Confezionamento finale della consegna

Nella cartella dei deliverable, verifica di avere entrambi i file richiesti:
```
ls -la
```
`integrity.txt` (Fase 1 completa) e `privesc.png` (Fase 2, screenshot dei comandi
richiesti + prova `id`/`whoami` con uid=0). Se la consegna chiede esplicitamente altri
artefatti (es. output grezzo di `aide -C` allegato a parte), aggiungili.

---

## Checklist rapida prima di consegnare

- [ ] Hai verificato **ogni** file segnalato da AIDE con il comando giusto (`getcap`/`getfacl`/`ls -l`), non solo il primo o quello che "sembrava" il vettore — i falsi positivi e i vicoli ciechi vanno scartati con la prova, non per intuito.
- [ ] Un cambiamento che **toglie** un privilegio non è mai il vettore — se lo scarti, dillo esplicitamente col perché.
- [ ] "c" (ctime) da solo, senza altri attributi cambiati, è rumore — non trattarlo come vettore.
- [ ] Se il vettore è una **capability** su un binario, hai spiegato perché serve una pipe verso quel binario e non un redirect diretto della shell (`>>`/`>` fallirebbero con Permission denied).
- [ ] L'hash della password è generato con `openssl passwd` **con la password esatta richiesta dalla consegna** (ricontrollata, non trascritta a orecchio).
- [ ] La riga aggiunta a `/etc/passwd` ha 7 campi (`utente:hash:uid:gid:gecos:home:shell`) e UID/GID `0`.
- [ ] Lo screenshot mostra la **prova finale** (`id` o `whoami` con `uid=0`), non solo i comandi intermedi.
- [ ] La sezione "Perché funziona" spiega il meccanismo di bypass, non ripete solo la sequenza di comandi già scritta sopra.
- [ ] Nessun terminale grezzo incollato con prompt/decorazioni ANSI illeggibili — comando + output riscritti puliti (vedi esempio reale in `privesc_2026-07-14_change4/integrity.txt`).
