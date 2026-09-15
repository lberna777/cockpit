**FIND**

**find** ci permette di esplorare il filesystem **in tempo reale** alla riceca di un file che rispetta **determinati criteri**

```
find <dove> <criteri> <azione>
```

| Criterio | Esempio | Significato |
| --- | --- | --- |
| `-name` | `-name '*.log'` | Nome del file (wildcard tra apici) |
| `-type` | `-type f` / `-type d` | Tipo: `f`\=file, `d`\=directory, `l`\=link |
| `-size` | `-size +100k` | Dimensione: `+` maggiore di, `-`minore di |
| `-mtime` | `-mtime -2` | Modificato negli ultimi 2 giorni (`-`\=entro, `+`\=più di) |
| `-user` | `-user alice` | Proprietario specifico |
| `-nouser` | `-nouser` | Nessun utente corrispondente (file “orfani”) |
| `-perm` | `-perm -2000` | Permessi (es. SGID attivo) |

(aggiungi anche una tabella relativa alle &lt;azioni&gt; per completismo)

la più importante &lt;azione&gt; relativa all'uso di find è **\-exec** che ci permette di eseguire un comando per ogni file che viene trovato dalla ricerca

```
find /usr/src -name '*.c' -size +100k -exec cat {} \;
                                         	^^  ^^
                                         	 |    fine del comando
                                        	  nome del file corrente
```

**LOCATE**

locate è una scorciatoia rispetto a find, ma ha dei trade-off. esplora un database pre compilato attraverso il quale non è obbligato a muoversi manualmente dentro ogni directory del filesystem

|        | `find` | `locate` |  
| --- | --- | --- |  
| Velocità | Lenta (esplora il filesystem) | Istantanea (cerca nel db) |  
| Aggiornamento | Sempre attuale | Obsoleto tra un updatedb e l’altro |  
| Criteri | Tutti (size, mtime, permessi…) | Solo nome del file |  
| Uso tipico | Ricerche precise e condizionali | Trovare rapidamente dove si trova un file |

(per qualche motivo che non capisco il comando locate non funziona nella mia VM dice comando non riconosciuto)

**FILE**

Il comando file ci permette di capire il tipo di contenuto all'interno di un file. in linux le estensioni leggibili (.txt .jpeg ...) sono un costrutto umano, non contano niente a livello di macchina per distinguere un file (vero?), tramite il comando file abbiamo risposte concrete

(non capisco gli esempi che mi hai fatto, cosa nel concreto estraggo da quegli output. non capisco neanche i tre livelli che sfrutta per risonderci)

**TRASFERIMENTO DATI A BASSO LIVELLO - dd**

**dd** è uno strumento bruto che copia un determinato quantitativo di dati da un file a un altro, anche tra file speciali (.qualcosa) normalmente nascosti, e senza eseguire alcun filtraggio

```
dd if=<sorgente> of=<destinazione> bs=<dimensione_blocco> count=<n_blocchi>
```

| Parametro | Significato |
| --- | --- |
| `if=` | Input file (sorgente) |
| `of=` | Output file (destinazione) |
| `bs=` | Block size — dimensione di ogni blocco |
| `count=` | Numero di blocchi da trasferire |
| `skip=` | Blocchi da saltare all’inizio della sorgente |
| `seek=` | Blocchi da saltare all’inizio della destinazione |

(non ho capito l'esempio che fai nella lezione, ho creato questo file.out e ho capito come ne determino le dimensioni, ma non capisco cosa sto copiando e da dove per metterlo dentro questo file.out)

**FILE APERTI - fuser & lsof**

```
# v1 — apre e chiude il file a ogni iterazione
[](#cb10-2)while sleep 1; do
  [](#cb10-3)  dd if=/dev/zero bs=1k count=$(( $(echo $RANDOM | rev | cut -c1) + 1 )) >> output
[](#cb10-4)done
[](#cb10-5)
[](#cb10-6)# v2 — il file viene aperto una sola volta, il redirect è fuori dal loop
[](#cb10-7)while sleep 1; do
  [](#cb10-8)  dd if=/dev/zero bs=1k count=$(( $(echo $RANDOM | rev | cut -c1) + 1 ))
[](#cb10-9)done >> output
```

&nbsp;(non ho capito cosa faccio con questi due script, non c'è più la parte "of=" ma suppongo perchè c'è il redirect ora che in queste occasioni cambia da dentro a fuori il loop. non capisco comunque le condizioni del count in entrambi. di conseguenza non capisco cosa cambia tra un caso e l'altro)

attraverso **fuser** **&lt;file&gt;,** posso stampare il PID (process id?) che hanno aperto un file 

(fuser non risulta un comando runnabile nella mia VM...)

attraverso **lsof** posso mostrare tutti i file aperti o filtrati per file/processo

(lsof funziona ma non ne capisco l'uso ne la sintassi, cosa gli do in pasto? e come lo processa? cosa significa l'output?)

**TAR (archiviazione)**

tar archivia in un unico archivio più file, conservandone tutti i metadati (permessi, proprietà, timestamp) non esegue compressione delle informazioni

### Comandi principali

| Opzione | Azione |
| --- | --- |
| `-c` | **C**rea un nuovo archivio |
| `-x` | E**x**trae file da un archivio |
| `-t` | Elenco (**t**able of contents) senza estrarre |
| `-r` | Aggiunge file a un archivio esistente |

Questi comandi possono aggiungere precisazioni a tar, ma non sono strettamente necessarie. L'unico comando obbligatorio è **\-f** per **specificare il nome dell'archivio dove indirizzo i file**

**ESEMPI PRATICI DI UTILIZZO**

```
# Creare un archivio delle home di tutti gli utenti
[](#cb12-2)tar cvpf users.tar /home/*		# a cosa serve cvpf? cosa significa?
[](#cb12-3)# Nota: tar rimuove automaticamente lo slash iniziale dai path
[](#cb12-4)# → i path nell'archivio sono relativi (es. home/alice/...) # cosa significa che i path sono relativi?
[](#cb12-5)
[](#cb12-6)# Elencare il contenuto senza estrarre
[](#cb12-7)tar tf users.tar
[](#cb12-8)
[](#cb12-9)# Estrarre in una directory specifica	(questo comando non viene runnato poichè non riesce a trovare /newdisk, e nemmeno la crea. ancora non capisco questi codici, prima cvpf, ora -xvpf, questa volta vedo che ha il trattino davanti quindi sarà una "regola"?
[](#cb12-10)tar -C /newdisk -xvpf users.tar
[](#cb12-11)# → ricrea la struttura home/alice/... dentro /newdisk
[](#cb12-12)
[](#cb12-13)# Pipeline: copiare una gerarchia di file preservando tutto
[](#cb12-14)tar cvpf - /home/* | tar -C /newdisk -xvpf -
[](#cb12-15)#           ^                              ^
[](#cb12-16)#           - = stdout                    - = stdin
```

come per "estrarre in una direcotry specifica" l'ultima pipeline non viene lanciata e produce i seguenti errori

vagrant@bookworm:~\$ tar cvpf - /home/\* | tar -C /newdisk -xvpf -  
tar: Removing leading \`/' from member names  
/home/alice/  
/home/alice/.bashrc  
tar: Removing leading \`/' from hard link targets  
/home/alice/.bash_logout  
/home/alice/.profile  
tar: /home/alice/.bash_history: Cannot open: Permission denied  
/home/bob/  
/home/bob/.bashrc  
/home/bob/.bash_logout  
/home/bob/.profiletar: /newdisk: Cannot open: No such file or directory  
tar: Error is not recoverable: exiting now

tar: /home/bob/.bash_history: Cannot open: Permission denied  
/home/maria/  
/home/maria/.bashrc  
/home/maria/.bash_logout  
/home/maria/.profile

inoltre non mi è chiara la struttra della pipe, ma perchè varia ancora il modo di utilizzo di tar, inoltre si includono riferimenti a stdin e stdout che non capisco e non riesco a collegare

**COMPRESSIONE**

Abbiamo detto come **tar** di per se non si occupi di comprimere i file, ma solo di archiviarli insieme. si può sfruttare in combo con un altro strumento per comprimere

**principali metodi di compressione**

| Estensione | Comando | Opzione tar |
| --- | --- | --- |
| `.gz` | `gzip` / `gunzip` | `-z` |
| `.bz2` | `bzip2` / `bunzip2` | `-j` |
| `.xz` | `xz` / `unxz` | `-J` |

```
# Creare archivio compresso
[](#cb13-2)tar czf archivio.tar.gz /home/*     # gzip
[](#cb13-3)tar cjf archivio.tar.bz2 /home/*   # bzip2			non capisco come viene composta la sintassi del # comando tar per la compressione, cosa sono czf, cjf e cJf?
[](#cb13-4)tar cJf archivio.tar.xz /home/*    # xz
[](#cb13-5)
[](#cb13-6)# Estrarre archivio compresso (tar rileva il formato automaticamente)
[](#cb13-7)tar xf archivio.tar.gz		# xf è il modificatore da inserire con tar per estrarre?
[](#cb13-8)tar xf archivio.tar.bz2
[](#cb13-9)tar xf archivio.tar.xz
[](#cb13-10)
[](#cb13-11)# Compressione come filtro (pipeline)
[](#cb13-12)tar cf - * | xz -c > archivio.tar.xz	# anche qua non capisco assolutamente cosa stia facendo visto che # l'output è vuoto, non dice nulla
```

anche la sezione alias utili del modulo non risulta utile perchè si lega a cose non affrontate come le interazioni con grep o il comando gzip

**RSYNC sincronizzazione di file online e offline**

è lo strumento principale per sincronizzare le directory 

### Esercizio 5 — copia “flat”

**Obiettivo**: copiare in una directory (secondo parametro) tutti i file contenuti in una directory (primo parametro) modificati da meno di N giorni (terzo parametro), senza preservare la struttura delle sottodirectory.

```
[](#cb19-1)#!/bin/bash
[](#cb19-2)# Uso: ./copia_flat.sh <sorgente> <destinazione> <giorni>
[](#cb19-3)
[](#cb19-4)SRC="$1"
[](#cb19-5)DST="$2"
[](#cb19-6)GIORNI="$3"
[](#cb19-7)
[](#cb19-8)# Verifica parametri
[](#cb19-9)if [ -z "$SRC" ] || [ -z "$DST" ] || [ -z "$GIORNI" ]; then
    [](#cb19-10)    echo "Uso: $0 <sorgente> <destinazione> <giorni>"
    [](#cb19-11)    exit 1
[](#cb19-12)fi
[](#cb19-13)
[](#cb19-14)mkdir -p "$DST"	# cosa specifico con -p?
[](#cb19-15)
[](#cb19-16)find "$SRC" -maxdepth 1 -type f -mtime -"$GIORNI" -exec cp {} "$DST" \;	#analizza nel dettaglio la  #
# composizione della sintassi di quesa riga
```

### Esercizio 6 — copia con conservazione della struttura

**Obiettivo**: copiare in una directory (primo parametro) tutti i file del sistema modificati da meno di N giorni (secondo parametro) **e** tutti i file sotto `/home` appartenenti a UID senza utente valido, mantenendo la struttura originale delle directory.

```
[](#cb20-1)#!/bin/bash
[](#cb20-2)# Uso: ./copia_struttura.sh <destinazione> <giorni>
[](#cb20-3)
[](#cb20-4)DST="$1"
[](#cb20-5)GIORNI="$2"
[](#cb20-6)
[](#cb20-7)if [ -z "$DST" ] || [ -z "$GIORNI" ]; then
    [](#cb20-8)    echo "Uso: $0 <destinazione> <giorni>"
    [](#cb20-9)    exit 1
[](#cb20-10)fi
[](#cb20-11)
[](#cb20-12)mkdir -p "$DST"
[](#cb20-13)
[](#cb20-14)# File recenti ovunque nel sistema
[](#cb20-15)find / -type f -mtime -"$GIORNI" -exec cp --parents {} "$DST" \;
[](#cb20-16)
[](#cb20-17)# File orfani sotto /home
[](#cb20-18)find /home -type f -nouser -exec cp --parents {} "$DST" \;
```

i dubbi che ho su questo script sono strettamente legati a quello del precedente, all'uso di specifiche nel mkdir sconosciute o alla sintassi di find qui utilizzata

<!-- AUTO-LINKS:START -->
## 🔗 Collegati

- [[appunti_modulo2C_file_tar_rsync_backup]]
- [[lezione_modulo2C_file_tar_rsync_backup]]

**Hub:** [[master_map_studio]] · [[glossario_sysadm]] · [[concept_maps]] · [[troubleshooting_vm]] · [[metodo_studio_esami_pratici]]
<!-- AUTO-LINKS:END -->
