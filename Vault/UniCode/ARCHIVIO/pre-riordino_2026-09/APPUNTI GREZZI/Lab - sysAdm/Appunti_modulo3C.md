GESTIONE DEI PROCESSI

lanciare processi in background

monitorarne lo stato

ucciderli

sincronizzarli

* * *

Comando nella shell --> processo        ogni processo ha:

- PID (Process ID) - Univoco globale assegnato dal kernel
- Job ID - Id locale alla shell corrente, solo per la sessione

Il processo sa che utente lo ha lanciato e agisce in suo nome, agendo con i suoi permessi.Solo un processo lanciato da Root può declassarsi a un altro utente ma senza poter poi tornare indietro

quando lancio un comando nella shell, la shell chiama fork() \[copia il processo\] e exec() \[sostituisce il codice con il programma da eseguire (SPIEGATI MEGLIO??)\]

Ogni processo figlio eredita i file descriptor del padre (cosa sono i file descriptor?)

* * *

PROCESSI in FOREGROUND e BACKGROUND

Per lanciare un processo in background:        aggiungo &

```bash
sleep 1000 &
```

Usando & la shell sponde con il JOB ID tra \[ \] e il PID del processo

N.B.        esiste \$! e si usa per catturare e salvare in variabile il PID dell'ultimo processo lanciato in background (vale anche per processi lanciati non in background?

Un processo in background:

- non riceve più input dal terminale
- continua a scrivere su STDOUT e STDERR quindi l'output appare a schermo (e può essere reindirizzato)

(non ho capito la modifica da foreground a background nel pratico come si fa, non so come usare quel codice accennato)

* * *

SEGNALI

i segnali sono eventi asincroni (cioè?) che vengono mandati dal kernel a un determinato processo. servono a controllare i processi dall'esterno

Un processo quando riceve un segnale può:

- terminare (cosa significa con o senza core dump?)
- ignorarlo
- sospendersi (come si cambia lo stato nel pratico?)
- riprendersi dallo stop (cosa significa cont?)

Ogni processo può designare un HANDLER personalizzato in grado di gestire il segnale come vuole lui. tranne per SIGKILL e SIGSTOP, unici segnali hce non possono essere bloccati, ignorati o intercettati

(non capisco come usare nel pratico le tabelle segnali importanti e invio segnali con kill. la prima non mi spiega come invio i segnali nel pratico, la seconda sembra che si faccia tutto con kill, ma non penso dal nome, i segnali normali saranno diversi e kill solo per uccidere o sospendere il processo?)

posso usare il codice del segnale in negativo in relazione a un PID di un process group (PGID) per agire su un appunto un gruppo di processi

la nota critica sulla non ereditarietà dei processi figli è linkata solo con i pseudo segnali bash o ale per tutti i segnali? dovrò creare un handler per ogni processo figli inclusi? non posso dargli lo stesso handler?)

* * *

COMANDI DI MONITORAGGIO

ps         ---->        crea snapshot dei processi in esecuzione

ES:        

```bash
ps                  # processi della shell corrente
ps $PID             # processo specifico (vuoto se non esiste)
ps aux              # tutti i processi del sistema
ps hp $PID          # output senza header, utile negli script
```

(spiega meglio le colonne di ps)

(chi restituisce questi codici di stato?)

jobs        --->        lista dei job della shell corrente        (cosa cambia tra processo e job?)

fg        ---->           riporta un job in foreground        (è il contrario di lanciarlo con &?)

watch        ---->        esegue un comando periodicamente e mostra l'output aggiornato

```bash
watch "ps aux | grep sleep | grep -v grep"
```

(chiarisci meglio come lo hai costruito)

senza ulteriori specifiche aggiorna ogni 2 secondi, utile per osservare un processo che cambia nel tempo (come cambio tempo di aggiornamento?)

* * *

WAIT

wait blocca l'esecuzione dello script fino al completamento dei job in background

```bash
sleep 30 &
sleep 40 &
wait         # attende entrambi
echo "Tutti terminati"
```

posso aspettare un solo job specifico:

```bash
wait $PID    # aspetta solo quel PID
```

(ricordami cosa faceva trap perchè non ho capito come funziona il suo legame con wait)

* * *

MODIFICATORI PER PROCESSI IN BACKGROUND

immunità alla chiusura della shell

quando chiudo la shell il kernel invia SIGHUP (hangup) a tutti i job in background (e foreground immagino?) terminandoli. nohup lo evita:

```bash
nohup sleep 1000 &          # sopravvive alla chiusura della shell
```

lo STDOUT viene rediretto su NOHUP.OUT (come faccio a non farlo?)

rimuovere un job dalla job table della shell

```bash
sleep 1000 & disown         # lancia e rimuove subito dalla job table
disown %1                   # rimuove il job 1 già in background
disown -h %1                # implementa anche l'immunità a SIGHUP
```

(non ho capito proprio a cosa serve, lo confornti a nohup ma non mi sembra faccia una cosa simile)

priorità di scheduling

con nice posso impostare la priorità di un comando, da -20(max) a +19(min) solo root può usare valori negativi. il valore default è 10

```bash
nice -n 10 comando          # lancia con niceness +10 (priorità più bassa)
nice nohup long_calc &      # combinazione comune
```

(spiega questa combinazione comune)

* * *

ARRAY BASH PER TRACCIARE I PROGRESSI

```bash
COMANDO1="sleep 10"
COMANDO2="sleep 20"

$COMANDO1 & PID[$!]="$COMANDO1"
$COMANDO2 & PID[$!]="$COMANDO2"

echo ${!PID[@]}    # stampa gli indici (= i PID)
echo ${PID[@]}     # stampa i valori (= i comandi)
echo ${PID[1234]}  # valore associato al PID 1234
```

non ho capito l'esempio e neanche quindi a cosa sia utile che gli array possano avere indici non consecutivi, che cos'è poi l'indice di un array?

* * *

MKTEMP

essenziale per creare file temporanei su cui far scrivere output a processi separati che non possono condividere lo stesso file senza sincronizzazione

```bash
FA=$(mktemp)    # crea /tmp/tmp.XXXXXX e restituisce il path
FB=$(mktemp)
# ... usare $FA e $FB come destinazioni separate ...
rm -f "$FA" "$FB"   # pulizia obbligatoria
```

`mktemp` risolve il problema della race condition (due processi che creano contemporaneamente un file con lo stesso nome).

* * *

## Comandi di Riferimento

| Comando | Sintassi | Descrizione |
| --- | --- | --- |
| `&` | `comando &` | Lancia in background |
| `$!` | `echo $!` | PID dell'ultimo processo in background |
| `jobs` | `jobs [-l]` | Lista job della shell corrente (altri -?) |
| `fg` | `fg %job_id` | Riporta in foreground |
| `bg` | `bg %job_id` | Manda/riavvia in background (manda o riavvia?) |
| `kill` | `kill [-segnale] PID` | Invia segnale a processo |
| `ps` | `ps [aux] [PID]` | Mostra processi (cosa fa aux?) |
| `wait` | `wait [PID]` | Aspetta terminazione job |
| `watch` | `watch "comando"` | Esegue comando periodicamente (sintassi completa?) |
| `nohup` | `nohup cmd &` | Lancia immune a SIGHUP |
| `disown` | `disown [%job]` | Rimuove job dalla job table |
| `nice` | `nice [-n N] cmd` | Lancia con priorità modificata |
| `trap` | `trap "codice" SEGNALE` | Definisce handler per segnale (come è strutturato? fai un esempio a parte) |
| `mktemp` | `FA=$(mktemp)` | Crea file temporaneo sicuro |

&nbsp;                                                                                                                                                                                                       

* * *

ES 1

❯ sleep 1000 &  
\[1\] 12516

~  
✦ ❯ A=\$!

~  
✦ ❯ echo \$A  
12516

✦ ❯ ps \$A  
    PID TTY STAT TIME COMMAND  
  12516 pts/2 SN 0:00 sleep 1000

~        cosa ottengo da questa lettura? il pid ok ma cosa sono tty stat time e command?

✦ ❯ jobs  
\[1\] + running sleep 1000

~  
✦ ❯ jobs -l  
\[1\] + 12516 running sleep 1000

~        quindi -l serve solo per vedere il PID, che altre specifiche posso dargli?

✦ ❯ kill -STOP \$A  
\[1\] + 12516 suspended (signal) sleep 1000

~

✦ ❯ ps \$A  
    PID TTY STAT TIME COMMAND  
  12516 pts/2 TN 0:00 sleep 1000

~        noto che ora da SN sta a TN, per cosa stanno?

✦ ❯ kill \$A

~  
✦ ❯ ps \$A  
    PID TTY STAT TIME COMMAND  
  12516 pts/2 TN 0:00 sleep 1000

~        a me sembra ancora attivo....

✦ ❯ kill -TERM \$A

~  
✦ ❯ ps \$A  
    PID TTY STAT TIME COMMAND  
  12516 pts/2 TN 0:00 sleep 1000

~        ho provato anche così ma uguale

✦ ❯ jobs  
\[1\] + suspended (signal) sleep 1000

~        resta questo

* * *

ES 2

vagrant@bookworm:~\$ sleep 1000 &  
\[1\] 1249  
vagrant@bookworm:~\$ sleep 1000 & disown  
\[2\] 1250  
vagrant@bookworm:~\$ nohup spleep 1000 &  
\[2\] 1255  
vagrant@bookworm:~\$ nohup: ignoring input and appending output to 'nohup.out'  
nohup: failed to run command 'spleep': No such file or directory  
^C  
\[2\]+ Exit 127 nohup spleep 1000  
vagrant@bookworm:~\$ jobs  
\[1\]+ Running sleep 1000 &  
vagrant@bookworm:~\$ nohup sleep 1000 &  
\[2\] 1258  
vagrant@bookworm:~\$ nohup: ignoring input and appending output to 'nohup.out'  
jobs  
\[1\]- Running sleep 1000 &  
\[2\]+ Running nohup sleep 1000 &  
vagrant@bookworm:~\$ exit  
logout

// ho fatto un errore di battitutra ma non credo di aver causato problemi

vagrant@bookworm:~\$ ps  
    PID TTY TIME CMD  
   1270 pts/1 00:00:00 bash  
   1274 pts/1 00:00:00 ps  
vagrant@bookworm:~\$ ps aux | grep sleep | grep -v grep  
vagrant 1249 0.0 0.1 2904 876 ? S 12:24 0:00 sleep 1000  
vagrant 1250 0.0 0.1 2904 888 ? S 12:24 0:00 sleep 1000  
vagrant 1258 0.0 0.1 2904 876 ? S 12:25 0:00 sleep 1000

//perchè con ps e basta non vedo un processo? e perchè ci sono 3 processi? dovrei averne 2 no?

* * *

ES 3

vagrant@bookworm:~\$ sleep 30 &  
\[1\] 1305  
vagrant@bookworm:~\$ sleep 40 &  
\[2\] 1308  
vagrant@bookworm:~\$ wait  
echo "tutti terminati"  
\[1\]- Done sleep 30  
\[2\]+ Done sleep 40  
vagrant@bookworm:~\$ echo "tutti terminati"  
tutti terminati  
vagrant@bookworm:~\$

//        questo è il primo terminale e funziona come dovrebbe no? aspetta entrambi e poi stampa

vagrant@bookworm:~\$ watch "ps auxw | grep sleep | grep -v grep"  
Error opening terminal: xterm-kitty.

//        questo è il secondo terminale e penso che questo errore non fosse previsto

* * *

ES 4

vagrant@bookworm:~\$ COMANDO1="sleep 10"  
vagrant@bookworm:~\$ COMANDO2="sleep 20"  
vagrant@bookworm:~\$ \$COMANDO1  
vagrant@bookworm:~\$ \$COMANDO1 & PID\[\$!\]="\$COMANDO1"  
\[1\] 1390        
vagrant@bookworm:~\$ \$COMANDO2 & PID\[\$!\]="\$COMANDO2"  
\[2\] 1393  
\[1\] Done \$COMANDO1  
vagrant@bookworm:~\$ echo \${!PID\[@\]}  
1390 1393  
vagrant@bookworm:~\$ echo \${!PID\[@\]}  
1390 1393  
vagrant@bookworm:~\$ echo \${PID\[@\]}  
sleep 10 sleep 20  
vagrant@bookworm:~\$ echo \${PID\[1390\]}  
sleep 10  
\[2\]+ Done \$COMANDO2  
vagrant@bookworm:~\$

// ho capito come fare tutto ma non cosa sto facendo, commenta il testo spiegando come si abbina cio che scrivo in ogni riga a quello che faccio/succede

<!-- AUTO-LINKS:START -->
## 🔗 Collegati

- [[appunti_modulo3C_gestione_processi]]
- [[lezione_modulo3C_gestione_processi]]

**Hub:** [[master_map_studio]] · [[glossario_sysadm]] · [[concept_maps]] · [[troubleshooting_vm]] · [[metodo_studio_esami_pratici]]
<!-- AUTO-LINKS:END -->
