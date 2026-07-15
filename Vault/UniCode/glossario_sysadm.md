# Glossario — Lab Amministrazione di Sistemi T

Aggiornato a ogni sessione. Ordine alfabetico.

---

## A

**ASLR (Address Space Layout Randomization)** — contromisura OS che randomizza a ogni avvio gli indirizzi base di stack, heap e librerie di un processo. Impedisce all'attaccante di conoscere l'indirizzo di funzioni di libreria (es. `system()`) o dello stack. Nota critica: **non randomizza `.text`** in configurazioni di base (solo con PIE). Disabilitato con `echo 0 > /proc/sys/kernel/randomize_va_space`.

**AIDE (Advanced Intrusion Detection Environment)** — strumento di *host-based intrusion detection* per il controllo di integrità del filesystem. Funziona a due tempi: `aideinit` crea un database di riferimento (snapshot di permessi/proprietario/dimensione/hash per i path configurati), `aide --check -c /etc/aide/aide.conf` confronta lo stato attuale con quel riferimento e riporta ogni differenza. **Va inizializzato PRIMA** che avvenga una modifica sospetta — un database creato dopo include già l'alterazione e il confronto risulta "pulito" anche se qualcosa è cambiato. Configurazione in `/etc/aide/aide.conf` (parametri database, gruppi di attributi come `Full`) più un'inclusione (`@@x_include /etc/aide/aide.conf.d ...`) di centinaia di regole per-pacchetto in `aide.conf.d/` — **non copre `/usr/bin` di default**, va aggiunta esplicitamente una regola (`/usr/bin f Full`) se si vuole rilevare modifiche lì. `f` nella regola restringe il controllo ai soli file regolari, non riguarda la ricorsività (che è il comportamento di default su un path).

**apt** — Advanced Package Tool. Tool di gestione dei pacchetti di alto livello su Debian/Ubuntu. Si appoggia a `dpkg` per le operazioni sui singoli file `.deb` e aggiunge la risoluzione automatica delle dipendenze, il reperimento dai repository e la gestione degli aggiornamenti. Comandi principali: `apt update`, `apt install`, `apt remove`, `apt purge`, `apt upgrade`, `apt autoremove`.

**apt-cache** — tool di interrogazione del database locale di apt. `apt-cache showpkg <nome>` mostra versioni disponibili, repo di provenienza e dipendenze inverse (chi dipende dal pacchetto). Non modifica il sistema.

**at** — comando per pianificare l'esecuzione di un comando una volta sola in un momento futuro. La coda dei job è visibile con `atq`, la cancellazione con `atrm <job_id>`. Alternativa moderna: `systemd-run --on-calendar=`.

**atime** — access time. Timestamp dell'ultimo accesso al contenuto di un file. Uno dei tre timestamp di ogni file (vedi anche mtime, ctime).

## B

**bad character** — byte che, in un payload di buffer overflow, viene alterato o interpretato in modo speciale da chi lo trasporta (shell, funzione di parsing, protocollo) invece di arrivare intatto al programma bersaglio. Esempi classici: `0x00` (terminatore di stringa C, tronca sempre), `0x20`/`0x09`/`0x0a` (spazio/tab/newline: se il payload passa per una sostituzione di comando non quotata come `$(perl -e '...')`, la shell fa *word splitting* su questi byte e spezza l'argomento). Prima di scegliere un indirizzo o un byte di payload, va sempre controllato che non contenga bad character per il canale usato. **Due rimedi diversi a seconda del bersaglio**: se l'indirizzo è su uno spazio con libertà di scelta (es. un punto qualsiasi dentro un NOP sled), si sposta il bersaglio su un byte vicino senza il carattere proibito; se l'indirizzo è un punto d'ingresso fisso senza alternative (es. l'indirizzo di una funzione di libreria come `system`), non si può spostare — si quota la sostituzione di comando (`run "$(perl -e '...')"`), che preserva i byte IFS come letterali senza subire lo split.

**banner grabbing** — tecnica di enumeration che consiste nel connettersi raw a un servizio testuale (SMTP, FTP, HTTP, ecc.) con `nc` o `telnet` e leggere il banner che il server invia automaticamente prima di qualsiasi autenticazione. Rivela nome software, versione, hostname. Spesso è l'unica azione necessaria per raccogliere info senza autenticarsi.

**buffer overflow** — vulnerabilità che si verifica quando un programma scrive dati oltre i limiti di un buffer allocato in memoria, sovrascrivendo dati adiacenti. In IA32 su stack: la scrittura oltre i limiti può raggiungere l'EBP salvato del chiamante e poi il **return address**, consentendo all'attaccante di redirigere il flusso di esecuzione. Causa tipica: uso di `gets()` o `strcpy()` senza bounds check.

**brute force** — attacco che prova sistematicamente tutte le combinazioni possibili di una password finché non trova quella corretta. Efficace su spazi piccoli (es. PIN 4 cifre = 10.000 combinazioni). Tool: Hydra (online, su servizi di rete), John the Ripper (offline, su hash locali).

## C

**canary (stack canary)** — valore casuale a 4 byte inserito dal compilatore GCC tra le variabili locali e l'EBP salvato in ogni stack frame. Prima di eseguire `RET`, il codice verifica che il valore sia intatto; se un buffer overflow lo ha sovrascritto, il processo viene terminato. Si abilita con `-fstack-protector` / `-fstack-protector-all`, si disabilita con `-fno-stack-protector`. Bypass: brute force su processi che forkano (il canarino è identico nel figlio).

**capability (Linux capability)** — meccanismo che spacchetta "tutti i poteri di root" in permessi granulari (~40) assegnabili a un binario senza renderlo SUID-root pieno. Attaccata come xattr (`security.capability`) direttamente sul file, sul filesystem — non su un utente/sessione — quindi si attiva per chiunque esegua quel binario e sopravvive ai reboot. Nel diff AIDE appare come `X` (xattr cambiato) + `+` (aggiunto): il diff dice solo "c'è una capability", non quale — va decodificata con `getcap <file>` (vuoto = nessuna capability effettiva, spesso un falso positivo se è stata impostata e subito ripristinata dallo stesso processo). Rilevanti per privesc: `cap_dac_override` (ignora ogni controllo di permesso lettura/scrittura — un editor o `tee` con questa capability scrive qualunque file, bypassando i permessi Unix), `cap_fowner` (ignora il controllo "solo il proprietario cambia i permessi" — puoi settare SUID su un binario altrui). Altre (`cap_mknod`, `cap_audit_read`) sono reali ma di norma inutili per l'escalation. Vedi `guida_esame_privesc.md` §3.2.

**CFI (Control Flow Integrity)** — famiglia di tecniche di difesa che impedisce all'attaccante di controllare EIP/RIP. Variante hardware moderna: **puntatori cifrati** — la CPU cifra/decifra trasparentemente tutti gli indirizzi di ingresso/uscita da funzioni usando una chiave scelta all'avvio del processo. Esempio reale: Pointer Authentication Codes (PAC) sui processori Apple ≥ A12. Un programma vulnerabile può essere fatto crashare ma non dirottato.

**core dump** — copia dello stato di memoria di un processo scritta su disco al momento della terminazione anomala (es. SIGSEGV, SIGQUIT). Usata per debugging post-mortem con `gdb ./programma core`. Non tutti i segnali producono core dump; dipende dalla signal disposition e dal limite `ulimit -c`.

**cron** — demone che legge i file crontab ogni minuto e lancia i task pianificati. Permette esecuzioni periodiche (ogni ora, ogni giorno, ogni lunedì). Configurazione per utente con `crontab -e`. Alternativa moderna: timer systemd.

**crontab** — file di configurazione che contiene le regole per cron. Sintassi: `MINUTO ORA G.MESE MESE G.SETTIMANA comando`. `/etc/crontab` è il crontab di sistema (ha un campo aggiuntivo per l'utente).

**ctime** — change time. Timestamp dell'ultima modifica ai *metadati* del file (permessi, owner, ecc.) — non al contenuto. Diverso da mtime.

## D

**daemon (demone)** — processo di sistema che gira in background senza terminale associato, a nome di un utente specifico, senza shell interattiva. Avviato e arrestato automaticamente. Esempi: `sshd`, `crond`, `rsyslog`.

**dipendenze (pacchetti)** — relazioni tra pacchetti software. Logiche: un pacchetto non ha senso senza un altro (es. PHP senza web server). Fisiche: un binario usa una libreria dinamica e non può girare senza di essa. Il package manager conosce l'intero grafo e lo risolve automaticamente a ogni installazione/rimozione.

**dpkg** — tool di basso livello per la gestione dei pacchetti `.deb` su Debian. Opera sul singolo file senza risolvere dipendenze. Comandi utili: `-i` (installa da file), `-r` (rimuovi), `-P` (purge), `-l` (lista installati), `-L <nome>` (file del pacchetto), `-S /path` (a quale pacchetto appartiene un file), `-s <nome>` (stato/info).

## D

**disown** — bash builtin che rimuove un job dalla job table della shell. Effetto: quando la shell chiude non sa più che il processo esiste e non gli invia SIGHUP. `disown -h %1` aggiunge solo l'immunità a SIGHUP senza rimuovere dalla job table. Differenza con `nohup`: `disown` agisce su processi già avviati; `nohup` si specifica all'avvio.

## E

**effective user ID (euid)** — identità che un processo usa effettivamente per operare. Normalmente uguale al real user ID, ma può differire se il programma ha il bit SUID impostato (es. `passwd` gira con euid=root anche se lanciato da un utente normale).

**eval** — bash builtin che esegue una stringa come se fosse un comando digitato da shell. Usato quando il comando da eseguire è costruito dinamicamente (es. in niceexec.sh: `eval "$@"` esegue tutti gli argomenti passati allo script come un unico comando). Da usare con cautela: valuta il contenuto della stringa senza sanitizzazione.

**exit code** — numero intero restituito da ogni comando al termine. `0` = successo, qualsiasi altro valore = errore. Leggibile con `$?`. Usato negli `if` degli script per sapere se un comando è andato a buon fine.

## F

**file descriptor (fd)** — numero intero con cui il kernel rappresenta una risorsa aperta (file, pipe, socket). I tre standard sono sempre presenti in ogni processo: 0=stdin, 1=stdout, 2=stderr. Ogni processo figlio eredita i fd aperti dal padre — motivo per cui i redirect impostati prima del `&` funzionano anche per il processo in background.

**fork / exec** — coppia di syscall usata per creare un nuovo processo. `fork()` duplica il processo corrente (stesso codice, stesso spazio di memoria). `exec()` sostituisce il codice del processo figlio con quello del programma da eseguire. Insieme producono un processo figlio con un'identità nuova che eredita fd e variabili d'ambiente dal padre.

**facility (syslog)** — categoria che identifica la sorgente di un messaggio di log. Esempi: `auth` (autenticazione), `kern` (kernel), `cron` (scheduler), `daemon` (demoni generici), `local0`–`local7` (applicazioni personalizzate). Forma una coppia con la priority: `facility.priority`.

## G

**GID** — Group ID. Numero che identifica univocamente un gruppo nel sistema. Come l'UID ma per i gruppi. Memorizzato in `/etc/group`.

**gruppo primario** — il gruppo assegnato di default a ogni file creato dall'utente. Uno solo per utente, definito in `/etc/passwd`. Distinto dai gruppi supplementari.

**gruppo supplementare** — gruppi aggiuntivi a cui un utente appartiene oltre al primario. Aggiunti con `usermod -aG`. Visibili con `groups nomeutente`.

## H

**host-only network (VirtualBox)** — tipo di rete virtuale isolata tra l'host fisico e le VM. Non c'è accesso a internet né alla LAN fisica. Le VM si vedono tra loro e con l'host tramite l'interfaccia `vboxnet0`. Tipicamente `192.168.56.x`. Contrapposta alla scheda NAT (`enp0s3`, `10.0.2.x`) che dà solo internet uscente. Usata nei lab Security per ambiente isolato attacco/difesa.

**Hydra** — tool di brute force multi-protocollo (SSH, HTTP, FTP, SMTP, ecc.). Prova combinazioni username/password in parallelo su servizi di rete. Flag: `-l user` (username fisso), `-P wordlist.txt` (wordlist), `-x 4:4:1` (genera PIN a 4 cifre numeriche al volo), `ssh://ip:porta` (target).

## I

**init** — processo con PID=1, il primo avviato dal kernel. È responsabile (direttamente o indirettamente) di tutti gli altri processi del sistema. Implementazioni storiche: SysVinit → Upstart → Systemd (attuale standard).

**idempotenza** — proprietà di un'operazione che produce lo stesso risultato indipendentemente da quante volte viene eseguita. Concetto chiave in Ansible: un playbook eseguito 10 volte produce lo stesso stato di uno eseguito 1 volta.

**inode** — struttura dati del filesystem che contiene i metadati di un file (permessi, owner, timestamp, puntatori ai blocchi dati). Il nome del file è separato dall'inode — un file può avere più nomi (hard link) che puntano allo stesso inode.

## J

**John the Ripper** — tool di password cracking offline. Prova candidati da wordlist o genera combinazioni contro hash locali (da `/etc/shadow` o file `.bak`). Nessun lockout: lavora su file, non su servizi di rete. `unshadow passwd shadow > combined.txt` prepara l'input; `john --wordlist=file.txt combined.txt` lancia il cracking; `john --show combined.txt` mostra le password trovate.

**job (job control)** — astrazione della shell per gestire i processi che ha lanciato direttamente. Identificato da un Job ID locale (prefisso `%`). Distinto dal PID: un job può comprendere più processi in pipeline. Quando la shell chiude, i job vengono notificati con SIGHUP; i processi senza job (disowned o nohup) no.

**journald (systemd-journald)** — sistema di log integrato in systemd. Raccoglie i messaggi di tutti i servizi in formato binario, accessibile solo tramite `journalctl`. Attivo dal boot, non dipende da altri servizi. Può coesistere con rsyslog inoltrandogli i messaggi via `ForwardToSyslog=yes`.

## K

**keyring (apt)** — file `.gpg` contenente le chiavi pubbliche GPG dei maintainer di un repository. Usato da apt per verificare la firma di ogni pacchetto scaricato. Su Debian va in `/etc/apt/trusted.gpg.d/`. Installato automaticamente dall'ISO di sistema; aggiunto manualmente per repo di terze parti con `gpg --dearmor`.

## L

**ldd** — comando che mostra le librerie dinamiche (`.so`) richieste da un eseguibile. Es: `ldd /usr/sbin/sshd` elenca tutte le `.so` caricate a runtime con il loro path. Utile per capire le dipendenze fisiche di un binario e diagnosticare errori "library not found".

**libreria dinamica (`.so`)** — codice condiviso caricato in memoria a runtime da uno o più programmi. Il binario non la include al suo interno (linking dinamico) — dipende dalla sua presenza sul filesystem. Vantaggio: aggiornabile senza ricompilare i programmi che la usano. Svantaggio: il programma non gira se la libreria è assente o incompatibile.

**load average** — misura del carico del sistema calcolata su 1, 5 e 15 minuti. Rappresenta il numero medio di processi in attesa di CPU. Va interpretato in rapporto al numero di CPU: load=2 su 4 CPU = sistema al 50% di carico. Visibile con `uptime` e `top`.

## M

**misconfiguration** — configurazione errata di un servizio che espone informazioni o accesso non intenzionali. Esempi: SMTP con VRFY abilitato rivela username; DB esposto sulla rete senza filtro firewall; password in chiaro nel DB invece di hash; banner che rivela versione software vulnerabile. È la causa più comune di violazioni evitabili.

**logger** — comando che invia messaggi a rsyslog dalla riga di comando. Usato per testare la configurazione e negli script cron. Sintassi: `logger -p facility.priority "messaggio"`. Es: `logger -p local4.info "test"`.

**magic number** — sequenza di byte all'inizio di un file che identifica il formato. Es: i file JPEG iniziano sempre con `FF D8 FF`, gli eseguibili Linux con `7F 45 4C 46`. Usati dal comando `file` per identificare il tipo di contenuto indipendentemente dall'estensione.

**mktemp** — crea un file temporaneo con nome univoco in `/tmp` e stampa il suo path. Usato negli script per salvare dati intermedi (es. job ID di at, crontab temporaneo). Il file va rimosso manualmente con `rm` al termine dello script.

**mtime** — modification time. Timestamp dell'ultima modifica al *contenuto* del file. Il più usato dei tre timestamp (vedi anche atime, ctime).

## N

**NOP sled (slitta di NOP)** — sequenza di istruzioni `NOP` (`\x90`) iniettata prima dello shellcode in un attacco buffer overflow. La CPU esegue le NOP senza effetti avanzando di un byte alla volta finché non raggiunge lo shellcode. Permette all'attaccante di puntare il return address a qualsiasi punto della slitta invece che all'esatto inizio dello shellcode, aumentando la probabilità di successo.

**NX stack (No-eXecute)** — contromisura hardware/OS che marca le pagine di stack come non eseguibili. Tentare di eseguire codice iniettato sullo stack causa un'eccezione di protezione della memoria. Implementato con il bit XD (eXecution Disable) di Intel, disponibile solo su architetture a 64 bit (non sui 32 bit nativi). Bypass: ret2libc, ROP. In gcc, si forza lo stack eseguibile con `-z execstack`.

**nmap** — scanner di rete per host discovery e port scanning. Flag principali: `-sn` (ping scan, solo host discovery, usa ARP su LAN con sudo), `-sT` (TCP connect scan, non richiede root), `-sS` (SYN scan, più veloce e stealth, richiede root), `-sV` (version detection: legge i banner), `-p-` (tutte le 65535 porte), `-p 22,80,443` (porte specifiche). Senza `-p-` scansiona solo ~1000 porte popolari.

**nohup** — comando che rende un processo immune al segnale SIGHUP (hangup inviato alla chiusura della shell). Redirige anche stdout su `nohup.out` se non diversamente specificato. Si usa all'avvio: `nohup cmd &`. Differenza con `disown`: `nohup` si specifica prima che il processo parta; `disown` agisce su processi già in background.

**nice / renice** — comandi per gestire la priorità di scheduling di un processo. `nice -n VALORE comando` avvia un comando con la priorità specificata. `renice VALORE -p PID` cambia la priorità di un processo già in esecuzione. Valori da -20 (massima priorità) a +19 (minima). Solo root può usare valori negativi.

## P

**`$!`** — variabile speciale bash che contiene il PID dell'ultimo processo mandato in background con `&`. Da non confondere con `!$` (history expansion = ultimo argomento del comando precedente).

**PID** — Process ID. Numero che identifica univocamente un processo in esecuzione. Assegnato dal kernel all'avvio del processo, liberato alla sua terminazione. Visibile con `ps`, `top`, `pgrep`.

**payload (exploit)** — stringa di byte costruita dall'attaccante per sfruttare una vulnerabilità. In un buffer overflow: il payload contiene il padding fino all'offset del return address, l'indirizzo di destinazione (little endian), e opzionalmente shellcode o indirizzi di funzioni. Non va confuso con il payload di rete (dati trasportati da un pacchetto).

**PIE (Position Independent Executable)** — modalità di compilazione che estende ASLR anche al segmento `.text` del binario. Senza PIE, `.text` ha indirizzi fissi — i gadget ROP sono prevedibili. Con PIE, anche il codice del programma viene randomizzato. Usa le tabelle PLT e GOT per l'indirizzamento; il GOT è potenzialmente sovrascrivibile (hardening aggiuntivo: RelRO).

**pacchetto (`.deb`)** — file singolo che contiene software precompilato + metadati (dipendenze, architettura, versione) + script di pre/post-installazione. Formato Debian: `nome-versione_arch.deb`. Gestito da `dpkg` a basso livello, da `apt` ad alto livello.

**pipe** (`|`) — meccanismo che collega lo stdout di un comando allo stdin del successivo. Es: `ls | grep .txt` — l'output di `ls` diventa l'input di `grep`.

**repository (repo)** — raccolta indicizzata di pacchetti software, distribuita online o su filesystem locale. Il package manager legge l'indice del repo per conoscere versioni disponibili e dipendenze. Su Debian, i repo abilitati sono elencati in `/etc/apt/sources.list` e `/etc/apt/sources.list.d/`.

## R

**RET2LIBC (return-to-libc)** — tecnica di exploit che bypassa la protezione NX stack: invece di iniettare shellcode, si sovrascrive il return address con l'indirizzo di una funzione di libreria già caricata in memoria (tipicamente `system()`). Lo stack viene riempito con `[addr_system][addr_exit][addr_"/bin/sh"]` — quando il processo esegue `RET`, salta a `system("/bin/sh")`. Non richiede stack eseguibile. Bypass di ASLR richiede trovare gli indirizzi a runtime con GDB.

**ROP (Return-Oriented Programming)** — tecnica di exploit avanzata che bypassa sia NX che ASLR di base. Costruisce il codice da eseguire concatenando **gadget** — brevi sequenze di istruzioni già presenti nel segmento `.text` del binario che terminano con `RET`. Ogni gadget esegue un'operazione atomica (es. `POP EAX; RET`), poi `RET` salta al gadget successivo via stack. Il segmento `.text` non è soggetto ad ASLR senza PIE, quindi gli indirizzi dei gadget sono prevedibili.

**race condition** — situazione in cui due o più processi accedono a una risorsa condivisa contemporaneamente producendo risultati imprevedibili. Esempio classico: due processi creano un file con lo stesso nome in `/tmp` allo stesso momento — uno sovrascrive l'altro. Soluzione: `mktemp` garantisce nomi univoci atomicamente.

**priority (syslog)** — livello di gravità di un messaggio di log. In ordine decrescente: `emerg`, `alert`, `crit`, `err`, `warning`, `notice`, `info`, `debug`. Nelle regole rsyslog, specificare una priority fa match con quella e tutte le superiori (prefisso `=` per exact match).

**real user ID (ruid)** — identità reale dell'utente che ha lanciato un processo. Non cambia durante l'esecuzione. Distinto dall'effective user ID (euid).

**rsyslog** — demone di logging standard su Debian, successore di syslog. Riceve messaggi dai processi (e da journald se configurato), li classifica per facility/priority e li smista verso file, programmi o server remoti. Configurazione in `/etc/rsyslog.conf` e `/etc/rsyslog.d/*.conf`.

**redirect** — meccanismo per redirigere stdin/stdout/stderr verso file invece che verso il terminale. `>` sovrascrive, `>>` aggiunge, `<` legge da file, `2>` redirige stderr.

## S

**shellcode** — sequenza di byte che rappresenta istruzioni assembly eseguibili direttamente dal processore, progettata per essere iniettata in un processo vulnerabile tramite buffer overflow. Vincolo fondamentale: non può contenere byte nulli (`\x00`) perché `strcpy`/`gets` lo usano come terminatore di stringa (operazione di **zeros cut-off**). Esempio tipico: invoca `execve("/bin/sh")` via `int 0x80` per aprire una shell con i privilegi del processo vittima.

**stack frame** — porzione dello stack allocata a ogni chiamata di funzione in IA32. Contiene (dall'alto verso il basso in memoria): parametri della funzione chiamante → return address → EBP salvato → variabili locali e buffer. La dimensione è determinata dall'istruzione `SUB ESP, N` nel function prologue. Il buffer overflow sfrutta il fatto che i buffer crescono verso indirizzi alti, verso il return address.

**segnale** — evento asincrono inviato dal kernel a un processo per notificargli una condizione. Asincrono = può arrivare in qualsiasi momento, indipendentemente da cosa stia facendo il processo. Un processo può terminare, ignorare, sospendersi o riprendersi in risposta a un segnale. `SIGKILL` e `SIGSTOP` sono gli unici non intercettabili né ignorabili.

**signal disposition** — la risposta che un processo ha configurato per ciascun segnale: azione default (termina/sospende/ignora), handler personalizzato (`trap` in bash, `signal()` in C), oppure ignorato. Non viene ereditata dai processi figli lanciati con `exec()`.

**software injection** — attacco in cui un repo di terze parti distribuisce un pacchetto con lo stesso nome di un pacchetto di sistema, dichiarandolo a versione più recente. Il package manager lo installa al posto di quello ufficiale. Difese: verificare la provenienza con `apt-cache showpkg`; usare version pinning (`/etc/apt/preferences.d/`); non aggiungere repo non fidati.

**sources.list** — file di configurazione principale di apt in `/etc/apt/sources.list`. Ogni riga attiva elenca un repository: `deb <url> <versione> <componenti>`. Frammenti aggiuntivi in `/etc/apt/sources.list.d/*.list`. `apt update` sincronizza gli indici di tutti i repo elencati.

**runlevel** — stato operativo del sistema in SysVinit: definisce quale sottoinsieme di servizi deve essere attivo (0=spegnimento, 1=single user, 3=multiutente, 5=grafico, 6=reboot). Sostituito dai **target** in systemd.

**SGID** — Set Group ID. Bit speciale (valore ottale `2` nella prima cifra). Su file eseguibili: il processo gira con il GID del proprietario del file. Su directory: i file creati al suo interno ereditano il gruppo della directory invece del gruppo primario del creatore.

**systemctl** — comando principale per interagire con systemd. Gestisce avvio/arresto/stato dei servizi (runtime) e la configurazione persistente (enable/disable/mask). Senza `--user` opera come root sul service manager di sistema.

**systemd** — sistema init moderno (PID=1 su Debian 8+). Gestisce avvio parallelo dei servizi, logging (journald), timer, mount e molto altro. Sostituisce SysVinit, Upstart, cron e syslog.

**shell** — interprete dei comandi. Legge i comandi digitati (o in uno script), li espande e li esegue. `bash` è la shell standard su Debian/Ubuntu.

**sticky bit** — bit speciale (valore ottale `1` nella prima cifra). Su directory world-writable: i file possono essere cancellati solo dal loro proprietario (non da chiunque abbia accesso in scrittura alla directory). Usato su `/tmp`.

**SUID** — Set User ID. Bit speciale (valore ottale `4` nella prima cifra). Su file eseguibili: il processo gira con l'UID del proprietario del file invece di quello di chi lo lancia. Es: `passwd` gira come root perché ha SUID impostato.

**stdout / stdin / stderr** — i tre canali standard di I/O di ogni processo. stdin (0) = input, stdout (1) = output normale, stderr (2) = output errori. Di default collegati al terminale; redirigibili con `>`, `<`, `2>`.

## T

**trap** — bash builtin per definire un handler da eseguire quando la shell riceve un segnale. Sintassi: `trap "codice" SEGNALE`. Pseudo-segnali bash: `EXIT` (all'uscita), `ERR` (quando un comando fallisce), `DEBUG` (prima di ogni comando). Gli handler non vengono ereditati dai processi figli lanciati con `exec()`.

**target (systemd)** — gruppo di unit che definisce lo stato operativo del sistema. Sostituisce il concetto di runlevel. Esempi: `multi-user.target` (server senza GUI), `graphical.target` (desktop con GUI), `rescue.target` (single user per riparazione).

**unit (systemd)** — file di configurazione che descrive a systemd come gestire una risorsa. Nome nella forma `nome.tipo` (es. `ssh.service`, `cron.timer`). Tipi principali: `.service`, `.timer`, `.target`, `.socket`, `.mount`.

## U

**UID** — User ID. Numero che identifica univocamente un utente nel sistema. `0` = root, 1-999 = utenti di sistema, 1000+ = utenti fisici. Memorizzato in `/etc/passwd`.

**umask** — maschera sottratta ai permessi massimi alla creazione di un file. Massimo per file: `666`, per directory: `777`. Con umask `0022`: file → `644`, directory → `755`. Con umask `0002`: file → `664`, directory → `775`.

## V

**version pinning** — tecnica per bloccare un pacchetto a una versione specifica, impedendo ad `apt upgrade` di aggiornarlo. Configurato in `/etc/apt/preferences.d/`. Utile per evitare che aggiornamenti automatici rompano configurazioni stabili o per bloccare pacchetti da repo di terze parti.

**vagrant** — strumento per creare e gestire VM in modo riproducibile tramite un file di configurazione (`Vagrantfile`). Usato nel corso per creare la VM Debian 12 di laboratorio.

## W

**wait** — bash builtin che sospende l'esecuzione dello script fino alla terminazione dei job in background. `wait` senza argomenti aspetta tutti i job attivi; `wait $PID` aspetta solo quel processo. Se durante l'attesa arriva un segnale con handler `trap`, `wait` esce immediatamente con exit code >128 e l'handler viene eseguito.

**watchdog** — pattern di programmazione che limita il tempo di esecuzione di un processo. Si avvia un processo in background, si pianifica un kill con `at` dopo N minuti, e si cancella il job `at` se il processo termina naturalmente prima del timeout.

---

## Security — Termini Chiave

**ALG** (Application-Level Gateway) — tipo di firewall che comprende il protocollo applicativo (HTTP, FTP...) e può quindi filtrare/permettere comandi specifici, non solo header. Anche detto proxy server. Più pesante di un packet filter, ma capisce cosa sta passando.

**banner grabbing** — tecnica di enumerazione passiva che consiste nell'aprire una connessione TCP a un servizio e leggere la stringa che invia all'apertura (il "banner"). Rivela versione del software, sistema operativo, e talvolta informazioni di configurazione. Eseguito con `nc <ip> <porta>` o da nmap con `-sV`. Misconfiguration classica: banner SMTP personalizzato con informazioni sull'infrastruttura interna.

**Bastion Host (BH)** — sistema dedicato a far girare il software firewall (tipicamente un ALG o CLG). Nella topologia "screened dual-homed" separa fisicamente due segmenti di rete, creando la DMZ.

**bruteforce** — attacco che prova sistematicamente tutte le combinazioni di un keyspace finito per trovare una credenziale. Efficace quando il keyspace è piccolo (es. PIN a 4 cifre = 10.000 combinazioni). Strumento standard: `hydra`. Mitigazioni: fail2ban (blocca IP dopo N tentativi), account lockout, password lunghe (keyspace esponenzialmente più grande).

**CLG** (Circuit-Level Gateway) — tipo di firewall che spezza la connessione a livello di trasporto, diventando esso stesso l'endpoint del traffico, ma inoltra i payload senza esaminarli (meno intelligente di un ALG, più leggero).

**conntrack** — componente di netfilter che riconosce quando una sequenza di pacchetti appartiene alla stessa connessione (tupla protocollo/IP sorgente/IP destinazione/porte), a prescindere dal protocollo sottostante. Rende possibile il filtraggio *stateful* (`ct state established,related accept` in nftables, `-m state --state ESTABLISHED` in iptables) invece di dover scrivere regole simmetriche per andata e ritorno di ogni servizio.

**credential reuse** — riuso della stessa password su sistemi diversi. Vulnerabilità frequente nel mondo reale: credenziali esfiltrate da un DB (es. password applicativa) funzionano anche per autenticazione SSH o altri servizi, perché l'utente ha usato la stessa password ovunque.

**CUPP** (Common User Passwords Profiler) — tool che genera wordlist personalizzate basandosi su dati personali del target (nome, cognome, data di nascita, animali domestici, ecc.). Efficace perché le persone costruiscono password derivate dalla propria vita. Uso: `python3 cupp.py -i` (modalità interattiva).

**DMZ** (Demilitarized Zone) — sottorete "cuscinetto" tra Internet e la rete privata, dove si collocano i server che devono essere raggiungibili dall'esterno, isolati dal resto della rete interna. Nasce nella topologia firewall "screened dual-homed BH" o "screened subnet".

**DNAT / SNAT / MASQUERADE / REDIRECT** — target NAT di iptables/nftables. `DNAT` cambia la destinazione di un pacchetto (port forwarding verso un server interno); `SNAT` cambia la sorgente (una rete privata che esce con un solo IP pubblico); `REDIRECT` è un caso particolare di DNAT che dirotta alla macchina locale (proxy trasparente); `MASQUERADE` è un caso particolare di SNAT, solo in POSTROUTING, che assegna automaticamente l'indirizzo dell'interfaccia di uscita (utile con IP dinamico).

**eve.json** — file di log di Suricata (formato JSON, una riga per evento) dove finiscono gli alert generati dalle regole. Ogni riga con `"event_type":"alert"` contiene i campi rilevanti per il resoconto d'esame: `src_ip`/`dest_ip`, `signature_id`, `signature` (il `msg` della regola), e se il traffico è HTTP anche `http.url`/`http_user_agent`. Si genera passando `-l <dir>` a Suricata; si consulta con `grep "<sid>" eve.json` o `jq`.

**hook di netfilter** — punto di aggancio nello stack di rete del kernel dove netfilter permette di registrare regole. Cinque hook: `PREROUTING` (pacchetto appena entrato, prima del routing), `INPUT` (destinato al sistema locale), `FORWARD` (da inoltrare altrove), `OUTPUT` (generato localmente), `POSTROUTING` (in uscita dal sistema). Le catene builtin di iptables corrispondono uno a uno a questi hook; in nftables vanno dichiarati esplicitamente (`type filter hook input priority 0`).

**HTTP flood** — attacco DoS volumetrico che invia moltissime richieste HTTP sintatticamente valide verso un server, a frequenza molto più alta di un uso umano/legittimo (nel tracciato analizzato in S10, richieste identiche a distanza di millisecondi contro un'analoga richiesta legittima distanziata di secondi). A differenza di un flood TCP/SYN generico, le richieste possono essere perfettamente valide: la firma dell'attacco è nel **volume/frequenza**, non necessariamente nel contenuto — anche se spesso il contenuto rivela anche l'intento (es. query string usata per fuzzing/ricerca di offset di buffer overflow).

**hydra** — tool per bruteforce su protocolli di rete (SSH, FTP, HTTP, SMTP, ecc.). Sintassi: `hydra -l <user> -P <wordlist> <proto>://<host>:<porta>`. Per generazione automatica: `-x min:max:charset` (es. `-x 4:4:1` = PIN numerici a 4 cifre).

**kill chain** (Lockheed Martin) — modello che descrive le 7 fasi di un attacco informatico: Reconnaissance → Weaponization → Delivery → Exploitation → Installation → C2 → Actions on Objectives. S1 copre la fase di Reconnaissance (enumerazione).

**misconfiguration** — errore di configurazione che espone un sistema ad attacchi non necessari. Esempi: DB in ascolto su tutte le interfacce invece di localhost; password di default non cambiate; banner che rivelano informazioni; password in chiaro nel DB; shell abilitata per utenti di servizio.

**netcat (nc)** — tool universale per connessioni TCP/UDP raw. `nc <ip> <porta>` apre una connessione e mostra/invia dati senza parlare nessun protocollo. Usato per banner grabbing, test di connettività, trasferimento file. `nc -l <porta>` apre un listener.

**nmap** — network mapper, strumento principale per enumerazione di rete. Flag chiave: `-sn` (ping scan, solo host discovery), `-sT` (TCP connect scan, porte aperte), `-sV` (version detection, banner grabbing), `-p-` (tutte le 65535 porte), `-O` (OS detection). Senza `-p-` scansiona solo ~1000 porte comuni.

**penetration test (PT)** — verifica pratica che una vulnerabilità sia effettivamente sfruttabile, spingendo l'attacco fino alla compromissione dimostrata. Più mirato e profondo del VA. Richiede autorizzazione esplicita. Output: catena di compromissione dimostrata.

**Protocol Hierarchy** (Wireshark, `Statistics → Protocol Hierarchy`) — vista ad albero che mostra tutti i protocolli presenti in un tracciato con percentuale/conteggio pacchetti, annidati per livello (Ethernet → IPv4 → TCP → HTTP...). Va **espansa completamente** (tasto destro → Expand All) per vedere i protocolli applicativi. Utile come primo passo di analisi: se la somma dei protocolli applicativi etichettati non copre il totale di TCP/UDP, la differenza è spesso dove si nasconde traffico anomalo (non riconosciuto dai dissector standard).

**regola Suricata (anatomia)** — `alert <proto> <src> <src_port> -> <dst> <dst_port> (msg:"..."; content:"..."; <sticky buffer>; sid:<N>; rev:1;)`. `alert` è l'azione (genera un evento, non blocca); `content` cerca una stringa nel payload; una **sticky buffer** come `http_uri` (nessun valore, va subito dopo il `content` a cui si riferisce) restringe la ricerca a un campo specifico invece che a tutto il pacchetto; `sid` è un ID univoco (convenzione: ≥1000000 per regole locali, per non confliggere con ruleset ufficiali); `rev` è la versione della regola. Si esegue su un pcap con `suricata -r <file>.pcap -S <regole.rules> -l <dir_output>` (modalità offline/replay).

**shadow** (`/etc/shadow`) — file che contiene gli hash delle password degli utenti Linux. Leggibile solo da root. Formato di ogni riga: `$<algoritmo>$<salt>$<hash>`. `$6$` = SHA-512 (sicuro), `$1$` = MD5 (obsoleto). Il salt impedisce rainbow table precompilate.

**TTL** (Time To Live) — contatore nell'header IP che ogni router attraversato decrementa di 1; se arriva a 0 il pacchetto viene scartato. Serve a evitare che un pacchetto giri all'infinito in un loop di routing. Utile in diagnosi: confrontando il TTL osservato con quello di partenza (default 64 su Linux) si conta quanti router ha attraversato un pacchetto (es. `ttl=62` osservato da un mittente con default 64 = 2 hop).

**unshadow** — tool che combina `/etc/passwd` e `/etc/shadow` nel formato richiesto da John the Ripper per il cracking. Uso: `unshadow passwd.bak shadow.bak > combined.txt`.

**VA** (Vulnerability Assessment) — identificazione sistematica delle vulnerabilità di un sistema. Ampio, meno profondo del PT. Output: lista di rischi con severità. Non verifica se le vulnerabilità sono effettivamente sfruttabili.
