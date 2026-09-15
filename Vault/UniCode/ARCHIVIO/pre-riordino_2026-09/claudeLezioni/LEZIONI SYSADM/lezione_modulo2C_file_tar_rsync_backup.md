# Gestione File — find, tar, rsync, Backup

**Modulo**: 2C | **Corso**: Lab Amministrazione di Sistemi T  
**Prerequisiti**: Modulo 2B completato  
**VM**: `cd ~/sysAdmin-lab && vagrant up --provider=virtualbox && vagrant ssh`  
**Fonte**: "Gestione di utenti e file [19 marzo]" (sezione file) + LAB esercizi 3–6

---

## Ricerca nel filesystem — `find`

`find` esplora il filesystem **in tempo reale** cercando file che soddisfano una combinazione di criteri. È potente ma ha un costo: percorre fisicamente le directory.

### Sintassi base

```bash
find <dove> <criteri> <azione>
```

### Criteri principali

| Criterio | Esempio | Significato |
|---|---|---|
| `-name` | `-name '*.log'` | Nome del file (wildcard tra apici) |
| `-type` | `-type f` / `-type d` | Tipo: `f`=file, `d`=directory, `l`=link |
| `-size` | `-size +100k` | Dimensione: `+` maggiore di, `-` minore di |
| `-mtime` | `-mtime -2` | Modificato negli ultimi 2 giorni (`-`=entro, `+`=più di) |
| `-user` | `-user alice` | Proprietario specifico |
| `-nouser` | `-nouser` | Nessun utente corrispondente (file "orfani") |
| `-perm` | `-perm -2000` | Permessi (es. SGID attivo) |

```bash
# Tutti i file .c sotto /usr/src più grandi di 100KB
find /usr/src -name '*.c' -size +100k -print

# File modificati nelle ultime 48 ore
find /var/log -mtime -2 -type f

# File orfani (utente eliminato) modificati meno di 2 giorni fa
find / -type f -nouser -mtime -2
```

### Eseguire comandi sui file trovati — `-exec`

`-exec` è una delle opzioni più potenti: per ogni file trovato esegue un comando.

```bash
find /usr/src -name '*.c' -size +100k -exec cat {} \;
#                                            ^^  ^^
#                                            |    fine del comando
#                                            nome del file corrente
```

- `{}` viene sostituito di volta in volta con il nome del file trovato
- `\;` segnala la fine del comando da eseguire (il backslash fa l'escape del `;`)

```bash
# Mostrare i permessi di tutti gli script nella home
find /home -name '*.sh' -exec ls -la {} \;

# Cercare file con SGID attivo (utile per audit di sicurezza)
find / -perm -2000 -type f -exec ls -la {} \;
```

### `locate` — ricerca rapida su database

`locate` non esplora il filesystem: cerca in un **database pre-costruito**. Molto più veloce, ma con un trade-off.

```bash
locate passwd        # istantaneo
sudo updatedb        # aggiorna il database (solitamente schedulato automaticamente)
```

| | `find` | `locate` |
|---|---|---|
| Velocità | Lenta (esplora il filesystem) | Istantanea (cerca nel db) |
| Aggiornamento | Sempre attuale | Obsoleto tra un updatedb e l'altro |
| Criteri | Tutti (size, mtime, permessi…) | Solo nome del file |
| Uso tipico | Ricerche precise e condizionali | Trovare rapidamente dove si trova un file |

---

## Identificazione del contenuto — `file`

In Linux le estensioni dei nomi non hanno significato per il sistema — sono solo etichette leggibili. Il comando `file` identifica il vero tipo del contenuto:

```bash
file /bin/bash
# /bin/bash: ELF 64-bit LSB pie executable, x86-64...

file /etc/passwd
# /etc/passwd: ASCII text

file foto.jpg.txt   # anche se il nome dice .txt
# foto.jpg.txt: JPEG image data, JFIF standard
```

`file` usa tre metodi in sequenza: controlla se il file è vuoto o speciale, poi usa i **magic number** (sequenze di byte caratteristiche di ogni formato), poi analisi euristica per testo e linguaggi.

---

## Trasferimento dati a basso livello — `dd`

`dd` legge e scrive byte da qualsiasi file, inclusi i file speciali di device. Non c'è filtraggio — trasferisce esattamente quello che trova.

```bash
dd if=<sorgente> of=<destinazione> bs=<dimensione_blocco> count=<n_blocchi>
```

| Parametro | Significato |
|---|---|
| `if=` | Input file (sorgente) |
| `of=` | Output file (destinazione) |
| `bs=` | Block size — dimensione di ogni blocco |
| `count=` | Numero di blocchi da trasferire |
| `skip=` | Blocchi da saltare all'inizio della sorgente |
| `seek=` | Blocchi da saltare all'inizio della destinazione |

### Lab esercizio 3 — prenotazione spazio su disco

```bash
dd if=/dev/zero of=file.out bs=4k count=16k
```

- `if=/dev/zero` — sorgente infinita di byte zero (file speciale sempre disponibile su Linux)
- `bs=4k` — blocchi da 4 kilobyte
- `count=16k` — 16.384 blocchi

Dimensione risultante: `4096 × 16384 = 67.108.864 byte = 64 MB`

```bash
ls -lh file.out
# -rw-r--r-- 1 vagrant vagrant 64M ... file.out
```

Questa tecnica serve a **riservare spazio su disco** in anticipo — ad esempio per creare un file di swap, un'immagine disco, o garantire che uno spazio sia disponibile prima di un'operazione critica.

---

## File aperti — `fuser` e `lsof`

### Lab esercizio 4 — differenza tra due versioni di script

```bash
# v1 — apre e chiude il file a ogni iterazione
while sleep 1; do
  dd if=/dev/zero bs=1k count=$(( $(echo $RANDOM | rev | cut -c1) + 1 )) >> output
done

# v2 — il file viene aperto una sola volta, il redirect è fuori dal loop
while sleep 1; do
  dd if=/dev/zero bs=1k count=$(( $(echo $RANDOM | rev | cut -c1) + 1 ))
done >> output
```

La differenza è **dove si trova il redirect `>>`**:

- **v1**: il `>>` è dentro il loop — ogni iterazione apre il file, scrive, chiude il file
- **v2**: il `>>` è fuori dal loop — il file viene aperto una volta sola all'avvio dello script, rimane aperto per tutta la durata

**Conseguenza pratica**: se rinomini o cancelli il file `output` mentre v2 è in esecuzione, lo script continua a scrivere sul vecchio inode (il file "esiste ancora" perché è aperto), e non si accorge che il nome è stato cambiato. Con v1, al ciclo successivo riapre il file per nome — quindi crea un nuovo `output` se quello vecchio è sparito.

### Strumenti per ispezionare file aperti

```bash
# fuser: mostra i PID che hanno aperto un file
fuser output

# lsof: mostra tutti i file aperti (o filtrati per file/processo)
lsof output
lsof -p <PID>
```

Questi comandi sono fondamentali per diagnosticare: "perché non riesco a smontare questo filesystem?" (qualcuno ha un file aperto), "chi sta scrivendo in questo log?", "perché lo spazio non si libera anche dopo aver cancellato il file?" (un processo lo tiene aperto).

---

## Archiviazione — `tar`

`tar` (Tape ARchiver) raccoglie più file in un unico archivio conservando tutti i metadati: permessi, ownership, timestamp. Non comprime di per sé.

### Comandi principali

| Opzione | Azione |
|---|---|
| `-c` | **C**rea un nuovo archivio |
| `-x` | E**x**trae file da un archivio |
| `-t` | Elenco (**t**able of contents) senza estrarre |
| `-r` | Aggiunge file a un archivio esistente |

Sempre necessario: `-f <file>` per specificare il nome dell'archivio (senza, tar prova a leggere/scrivere su un nastro fisico).

### Opzioni comuni

| Opzione | Significato |
|---|---|
| `-v` | **V**erboso — stampa i file processati |
| `-p` | Preserva permessi e ownership |
| `-C <dir>` | Esegue l'operazione come se ci si trovasse in `<dir>` |
| `-T <file>` | Legge la lista dei file da archiviare da un file di testo |

### Esempi pratici

```bash
# Creare un archivio delle home di tutti gli utenti
tar cvpf users.tar /home/*
# Nota: tar rimuove automaticamente lo slash iniziale dai path
# → i path nell'archivio sono relativi (es. home/alice/...)

# Elencare il contenuto senza estrarre
tar tf users.tar

# Estrarre in una directory specifica
tar -C /newdisk -xvpf users.tar
# → ricrea la struttura home/alice/... dentro /newdisk

# Pipeline: copiare una gerarchia di file preservando tutto
tar cvpf - /home/* | tar -C /newdisk -xvpf -
#           ^                              ^
#           - = stdout                    - = stdin
```

---

## Compressione

`tar` non comprime — si combina con un filtro di compressione separato.

### I tre formati più comuni su Linux

| Estensione | Comando | Opzione tar |
|---|---|---|
| `.gz` | `gzip` / `gunzip` | `-z` |
| `.bz2` | `bzip2` / `bunzip2` | `-j` |
| `.xz` | `xz` / `unxz` | `-J` |

`xz` offre la compressione migliore ma è più lento. `gzip` è il più veloce. `bzip2` è nel mezzo.

```bash
# Creare archivio compresso
tar czf archivio.tar.gz /home/*     # gzip
tar cjf archivio.tar.bz2 /home/*   # bzip2
tar cJf archivio.tar.xz /home/*    # xz

# Estrarre archivio compresso (tar rileva il formato automaticamente)
tar xf archivio.tar.gz
tar xf archivio.tar.bz2
tar xf archivio.tar.xz

# Compressione come filtro (pipeline)
tar cf - * | xz -c > archivio.tar.xz
```

### Alias utili

```bash
zcat file.gz          # equivale a: gzip -dc file.gz
zgrep pattern file.gz # equivale a: gzip -dc file.gz | grep pattern
```

---

## Copia massiva — `rsync`

`rsync` è lo strumento standard per sincronizzare directory, localmente o via rete. Il suo vantaggio principale su `cp`: trasferisce solo le **differenze**, non ricopiando file già presenti a destinazione.

### Sintassi

```bash
rsync [opzioni] SORGENTE DESTINAZIONE
```

### Modalità di trasferimento

```bash
# Copia locale
rsync -av /home/alice/ /backup/alice/

# Copia via SSH (non richiede demone rsync sul server)
rsync -av /home/alice/ user@host:/backup/alice/
rsync -av user@host:/backup/alice/ /home/alice/

# Copia via protocollo nativo rsync (richiede demone rsyncd)
rsync user@host::srcdir /destinazione
```

### Opzioni principali

| Opzione | Significato |
|---|---|
| `-a` | Archive: equivale a `-rlptgoD` — ricorsivo, preserva link, permessi, timestamps, owner, group, file speciali |
| `-v` | Verbose |
| `-r` | Ricorsivo |
| `-u` | Salta file più nuovi a destinazione |
| `-c` | Confronta per checksum invece che per timestamp+size |
| `-b` | Backup dei file sovrascritti |
| `--exclude` | Esclude path dalla copia |
| `--dry-run` | Simula senza copiare nulla (ottimo per verificare prima) |

```bash
# Sincronizzazione tipica preservando tutto
rsync -av --exclude '.cache' /home/alice/ /backup/alice/

# Verifica cosa verrebbe copiato senza farlo davvero
rsync -av --dry-run /home/ /backup/home/
```

---

## Backup — strategie

Il backup è la copia dei dati su un supporto offline. Va pianificato considerando cosa copiare, quando, dove conservare le copie e per quanto.

### Full backup

Copia completa di ogni file. Semplice da ripristinare, ma lento e ingombrante — difficile da eseguire frequentemente.

### Incremental backup

Copia solo i file cambiati dall'ultimo backup. Adatto all'esecuzione frequente. Per il ripristino completo servono sia il full che tutti gli incrementali successivi. Può essere a più livelli:

```
Full
├── Incrementale/0 (rispetto al full)
│   ├── Incrementale/1a (rispetto all'incrementale/0)
│   └── Incrementale/1b (rispetto all'incrementale/0)
└── Incrementale/0b (rispetto al full)
```

### Cautele

| Rischio | Misura |
|---|---|
| File aperti/database in scrittura | Pianificare il backup in orari di basso traffico o usare snapshot |
| Riservatezza dei dati | Il backup contiene tutto — va protetto fisicamente o cifrato |
| Affidabilità del supporto | Testare periodicamente che i dati siano leggibili |
| Reperimento | Organizzare le copie in modo da trovare rapidamente quello che serve |

---

## Lab esercizi 5 e 6 — script con `find`

### Esercizio 5 — copia "flat"

**Obiettivo**: copiare in una directory (secondo parametro) tutti i file contenuti in una directory (primo parametro) modificati da meno di N giorni (terzo parametro), senza preservare la struttura delle sottodirectory.

```bash
#!/bin/bash
# Uso: ./copia_flat.sh <sorgente> <destinazione> <giorni>

SRC="$1"
DST="$2"
GIORNI="$3"

# Verifica parametri
if [ -z "$SRC" ] || [ -z "$DST" ] || [ -z "$GIORNI" ]; then
    echo "Uso: $0 <sorgente> <destinazione> <giorni>"
    exit 1
fi

mkdir -p "$DST"

find "$SRC" -maxdepth 1 -type f -mtime -"$GIORNI" -exec cp {} "$DST" \;
```

`-maxdepth 1` limita la ricerca alla directory specificata senza scendere nelle sottodirectory (copia "flat" = senza struttura).

### Esercizio 6 — copia con conservazione della struttura

**Obiettivo**: copiare in una directory (primo parametro) tutti i file del sistema modificati da meno di N giorni (secondo parametro) **e** tutti i file sotto `/home` appartenenti a UID senza utente valido, mantenendo la struttura originale delle directory.

```bash
#!/bin/bash
# Uso: ./copia_struttura.sh <destinazione> <giorni>

DST="$1"
GIORNI="$2"

if [ -z "$DST" ] || [ -z "$GIORNI" ]; then
    echo "Uso: $0 <destinazione> <giorni>"
    exit 1
fi

mkdir -p "$DST"

# File recenti ovunque nel sistema
find / -type f -mtime -"$GIORNI" -exec cp --parents {} "$DST" \;

# File orfani sotto /home
find /home -type f -nouser -exec cp --parents {} "$DST" \;
```

`cp --parents` preserva il path completo — se copi `/var/log/syslog` in `/backup`, il risultato è `/backup/var/log/syslog`, non `/backup/syslog`.

---

## Riepilogo comandi

| Comando | Funzione |
|---|---|
| `find /path -name '*.log'` | Cerca file per nome |
| `find /path -mtime -2 -type f` | File modificati nelle ultime 48h |
| `find /path -nouser` | File orfani (utente eliminato) |
| `find /path -exec comando {} \;` | Esegue un comando su ogni file trovato |
| `locate nome` | Ricerca rapida su database |
| `sudo updatedb` | Aggiorna il database di locate |
| `file nome` | Identifica il tipo di contenuto di un file |
| `dd if=src of=dst bs=4k count=16k` | Copia a basso livello / prenotazione spazio |
| `fuser file` | Mostra i processi che hanno il file aperto |
| `lsof file` | Dettagli sui file aperti |
| `tar czf archivio.tar.gz /path` | Crea archivio compresso con gzip |
| `tar xf archivio.tar.gz` | Estrae un archivio |
| `tar tf archivio.tar.gz` | Elenca il contenuto senza estrarre |
| `rsync -av src/ dst/` | Sincronizza directory preservando tutto |
| `rsync -av --dry-run src/ dst/` | Simula rsync senza copiare |

<!-- AUTO-LINKS:START -->
## 🔗 Collegati

- [[Appunti_modulo2C]]
- [[appunti_modulo2C_file_tar_rsync_backup]]

**Hub:** [[master_map_studio]] · [[glossario_sysadm]] · [[concept_maps]] · [[troubleshooting_vm]] · [[metodo_studio_esami_pratici]]
<!-- AUTO-LINKS:END -->
