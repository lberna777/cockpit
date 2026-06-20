**DEMONI (daemon)**

I daemons sono processi di sistema che **si avviano e arrestano automaticamente**, non sono collegati a **nessun terminale** e girano **a nome di un utente specifico** (esistono UID dedicati ai demoni) e **senza una shell interattiva** (cioè?)

Gli **amministratori di sistema** lavorano interagendo con essi e devono poterne **configurare avvio e arresto automatici, verificarne lo stato, tenere un log delle sue esecuzioni, operarli manualmente**

**TIPOLOGIE DI PROCESSI**

Oltre ai processi istanziati dagli **utenti interattivi (noi)** su un sistema Linux esistono **tre fonti principali di processi:**

- **procedure di avvio del sistema**
- **pianificatori periodici e sporadici**
- **demoni di gestione degli eventi**

(Domande: le prime sono le procedute che sono automatizzate ad ogni avvio del sistema? un po' tipo i programmi all'avvio su windows? i pianificatori periodici e sporadici sono azioni, script (?) che salvo come ripetibili in automatico dopo determinato tempo? o che pianifico per un certo istante di tempo?)

* * *

**IL SISTEMA INIT**

Init è il processo con **PID = 1**, è avviato dal kernel ed è responsabile (direttamente o indirettamente, cioe?) di tutti gli altri processi

(non capisco questa parte della lezione, sysVinit, Upstart e Systemd sono tutti tipi di init diversi nel tempo? e ora si usa Systemd?)

**SYSTEMD - concetti fondamentali**

Si occupa della gestione del sistema tramite **unit,** ovvero dei file di configurazione con nome nella forma        **nome.tipo**

**tipi possibili:**

| Tipo | Funzione |
| --- | --- |
| `.service` | controllo e monitoraggio di un demone |
| `.socket` | attivazione via canale IPC (porta di rete, socket UNIX) |
| `.target` | gruppo di unit — **sostituisce il concetto di runlevel** |
| `.timer` | attività legate al tempo (sostituisce cron) |
| `.device` | punti di accesso a dispositivi hardware |
| `.mount` / `.automount` | punti di montaggio filesystem |
| `.slice` | gestione risorse via cgroup |

come posso accedervi?

```
/lib/systemd/system/        ← libreria di riferimento (pacchetti software)
/usr/lib/systemd/system/    ← stessa cosa su alcune distro
/etc/systemd/system/        ← personalizzazioni locali (priorità massima)
```

&nbsp;

* * *

**GESTIONE DEI SERVIZI TRAMITE systemctl**

**Operazioni eseguibili a runtime (cioè?)**

```
systemctl start   nomeservizio    # avvia
systemctl stop    nomeservizio    # ferma
systemctl restart nomeservizio    # stop + start
systemctl reload  nomeservizio    # ricarica configurazione senza restart
systemctl status  nomeservizio    # mostra stato, PID, log recenti
```

**Operazioni di configurazione persistenti (entrano in funzione al prossimo boot)**

```
systemctl enable  nomeservizio    # avvio automatico al boot
systemctl disable nomeservizio    # disabilita avvio automatico (ma manuale rimane possibile)
systemctl mask    nomeservizio    # neutralizza completamente (impedisce anche start manuale)
systemctl unmask  nomeservizio    # ripristina
```

**Ispezione della configurazione (non capisco in che contesto servono?)**

```
systemctl list-units                      # tutte le unit attive
systemctl list-units -t service           # solo i servizi attivi
systemctl list-unit-files -t service      # tutti i servizi installati (anche inattivi)
systemctl list-unit-files -t service --state=enabled  # solo quelli abilitati al boot
systemctl --state=failed                  # unit in stato failed
```

**TARGET - selezione del livello a cui si vuole runnare il processo (credo?)**

|     |     |     |
| --- | --- | --- |
| 0   | `poweroff.target` | Spegnimento |
| 1   | `rescue.target` | Single user mode |
| 3   | `multi-user.target` | Multi-utente, senza GUI |
| 5   | `graphical.target` | Multi-utente con GUI |
| 6   | `reboot.target` | Riavvio |

ho capito che va usato in combo con systemctl ma non capisco a cosa serva, ne cosa modifica nel tangibile, ne se dovrei eseguire questi cambiamenti prima di avviarlo o se necessitino di un reboot

**CONTESTUALIZZIAMO SYSTEMCTL**

Di base il comando opera sul service manager disistema e quindi **richiede i privilegi di root**, ma **ogni utente** ha un proprio **service manager**, attivabile così:

```
systemctl --user start   mioservizio
systemctl --user enable  mioservizio    # avvio automatico al login (non al boot)
```

come si relaziona al service manager principale? cosa vedo di diverso? che differenze ho?

* * *

**STRUTTURA DI UN FILE UNIT**

(domanda: a cosa servono? in che contesto si usano? chi li legge? l'unico altro pezzo di lezione che parlava di unit era "ispezione della configurazione" ma non ho capito niente come a questo punto avrai letto dalle domande)

```
[Unit]
Description=Il mio servizio di esempio
Requires=network.target
After=network.target

[Service]
Type=exec
ExecStart=/usr/bin/mioprogramma --opzione
ExecStop=/usr/bin/mioprogramma --stop
Restart=on-failure

[Install]
WantedBy=multi-user.target
```

**SEZIONE 1 - \[UNIT\]**

|     |     |
| --- | --- |
| `Requires=B` | B deve essere attiva; se B fallisce, questa si ferma |
| `Wants=B` | come Requires ma tollerante: se B fallisce, questa continua |
| `After=B` | avvia *dopo* B (Wants/Requires non implicano l’ordine temporale!) |
| `Conflicts=B` | mutuamente esclusivi con B |
| `OnFailure=C` | avvia C se questa fallisce |
| `WantedBy=` (in \[Install\]) | crea automaticamente un Wants nella unit indicata all’`enable` |

(non c'ho capito un cazzo, cosa significano ste B, ste C, ma non sto capedo l'utilità e l'ulitizzo generale del file direi)

```
ExecStart=/usr/bin/mio-configuratore
[](#cb8-2)ExecStop=/usr/bin/mio-de-configuratore
```

```
Restart=on-failure    # riavvia se termina con exit code non zero o segnale non clean
[](#cb9-2)Restart=always        # riavvia sempre, tranne se fermato da systemctl stop
```

* * *

**ESECUZIONI PIANIFICATE**

**una tantum - at**

**at** ci permette di pianificare un comando da eseguire **una sola volta** in un **momento futu\*\*\*\*ro**

```
sudo apt install at           # installa se non presente

# Pianificare
echo "/bin/comando" | at now + 30 minutes
echo "/bin/comando" | at 14:30
echo "/bin/comando" | at midnight 31.12.2025

# Gestire la coda
atq                           # lista job in coda
atrm <job_id>                 # rimuove un job
```

per poter cancellare un comando pianificato, è necessario conoscere l\*\*'ID\*\* del **job**

```
ATJOB=$(mktemp)
echo "/bin/comando" | at now + 30 minutes 2>&1 | grep '^job ' | cut -f2 -d' ' > $ATJOB
# Per cancellare:
atrm $(cat $ATJOB)
```

domanda: non mi è chiaro il meccanismo per la cancellazione, come si applica nel pratico?

**esecuzione periodica - cron**

**cron** legge i file **crontab** ogni minuto e lancia i **task pianificati**

```
crontab -l        # mostra il crontab dell'utente corrente
crontab -e        # edita il crontab
crontab FILE      # sostituisce il crontab con FILE
```

**Sintassi crontab**:

```
MINUTO  ORA  G.MESE  MESE  G.SETTIMANA  <comando>
```

Esempi:

```
30 4 1,15 * 6     /bin/backup    # alle 4:30 del giorno 1, 15 e ogni sabato
*/10 8-18 * * 1-5 /home/las/lavora.sh  # ogni 10 min, 8-18h, lun-ven
0 0 1 1 *         /usr/sbin/auguri    # 1 gennaio a mezzanotte
```

&nbsp;come funziona l'uso degli asterischi qua? nello specifico non capisco la sintassi della seconda riga di questo codice

**Crontab di sistema** (`/etc/crontab`) ha un campo aggiuntivo per specificare l’utente:

```
30 4 * * * root /usr/sbin/backup
```

come funziona e a cosa serve materialmente il crontab di sistema? e cosa intendi per manipolazione programmatica del crontab? tutto quel codice non l'ho capito

**sostituzione moderna di cron e at - TIMER SYSTEMD**

Si può integrare l'esecuzione una tantum in futuro o la ripetizione di esecuzioni nel tempo direttamente nei file UNIT che legge systemd. Questo avviene mediante due file, uno con il servizio da eseguire e uno con il timer che lo attiva.

```
[Unit]
Description=Il mio script periodico

[Service]
Type=oneshot
ExecStart=/path/to/script.sh
```

`/etc/systemd/system/myscript.timer`:

```
[Unit]
Description=Timer per myscript

[Timer]
OnCalendar=*-*-* 04:30:00    # ogni giorno alle 4:30
Persistent=true               # esegue anche se la macchina era spenta

[Install]
WantedBy=timers.target
```

&nbsp;il file si esegue allo scadere DEL timer, in questo caso replicando un **cron** con esecuzione periodica, che devo startare (solo manualmente?) all'avvio con:

```
sudo systemctl enable --now myscript.timer   # attiva il timer subito e al boot
systemctl list-timers                         # mostra tutti i timer attivi
```

per quanto riguarda le ripetizioni **una-tantum (come con at):**

```
systemd-run --on-active=30m /path/to/script.sh           # tra 30 minuti
systemd-run --on-calendar="2025-12-24 11:00:00" /path/to/script.sh
systemd-run --user --on-active=1m /bin/cmd               # come utente normale
```

sfrutto il contatore che controlla da quanto è acceso il sistema?

**Sintassi OnCalendar**:

```
DayOfWeek YYYY-MM-DD HH:MM:SS
```

- `*` = qualsiasi valore
- `A..B` = range
- `A,B,C` = lista
- `/P` = incrementi di P unità (es. `*/2` = ogni 2)

chiarisci meglio cosa si può effettivamente inserire per riempire questi placeholder?

**MONITORAGGIO - log di sistema**

I log sono un meccanismo indispensabile per la diagnostica di sistema. si aggiornano periodicamente (spesso anche dopo ogni azione sul dispositivo) e tengono traccia di tutto. vanno checkati spesso per integrità dei dati e sarebbe ideale replicarli su macchine esterne alla rete che si amministra.

su debian questa meccanica è gestita da **rsyslog**, il successore di **syslog** che segue però gli stessi concetti

- I processi inviano messaggi al logger (**rsyslog)**
- il loger serializza, fa timestamping (registra date e o) e classifica i messaggi
- il logger smista verso destinazioni configurate (i corretti file di log singoli)
- Ogni messaggio ha una coppia `<facility>.<priority>`: - **Facility**: argomento del messaggio (`auth`, `cron`, `daemon`, `kern`, `mail`, `user`, `local0`–`local7`, …) - **Priority** (decrescente): `emerg`, `alert`, `crit`, `err`, `warning`, `notice`, `info`, `debug`

approfondisci la struttura della sintassi di rsyslog e gli esempi che hai fatto? non sono chiari e non considerano le basi dell'argomento. come funziona nel tangibile, le regole cosa riguardano?

approfondisci l'utilità di systemd-journald, non capisco a cosa serva, non ra systemd il sistema di log? o systemd smista i messaggi e tramite journald li scrive nei log? o interagisce coi log qualdir si voglia?

* * *

**Es. 1 - Installare at e pianificare un comando**

**//        installo at**

```
sudo apt install at
```

//        pianifico un comando tra 30 minuti

```
echo "/bin/echo ciao" | at now + 30 minutes
```

come funziona echo "/bin/echo ciao"? la sintassi corretta per inviare un comando tramite at

ho notato che l'orario della mia VM è sballato e diverse ore prima di quello che deve essere

//        verifico la coda dei comandi da eseguire

```
atq
```

//        posso cancellare il job (inserendo N = numero del job)

```
atrm N
```

come ricavo il numero del job?

&nbsp;

&nbsp;

<!-- AUTO-LINKS:START -->
## 🔗 Collegati

- [[appunti_modulo3A_systemd_servizi]]
- [[lezione_modulo3A_systemd_servizi]]

**Hub:** [[master_map_studio]] · [[glossario_sysadm]] · [[concept_maps]] · [[troubleshooting_vm]] · [[metodo_studio_esami_pratici]]
<!-- AUTO-LINKS:END -->
