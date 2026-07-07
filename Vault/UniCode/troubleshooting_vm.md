# Troubleshooting VM — Soluzioni ai problemi ricorrenti

Aggiornato a ogni sessione. Prima di chiedere aiuto, cerca qui.

---

## Avvio VM

**Problema**: `vagrant up` fallisce con errore VirtualBox  
**Soluzione**: Verifica che VirtualBox sia aperto. Se la VM è già in stato "saved", prova `vagrant resume` invece di `vagrant up`.

**Problema**: La VM si avvia ma `vagrant ssh` non si connette  
**Soluzione**:
```bash
vagrant halt
vagrant up
vagrant ssh
```

---

## Pacchetti non trovati

**Problema**: `sudo apt install <pacchetto>` → `Unable to locate package`  
**Causa**: La lista dei pacchetti disponibili è vecchia o vuota.  
**Soluzione**:
```bash
sudo apt update
sudo apt install <pacchetto>
```
`apt update` va eseguito sempre prima di installare pacchetti, specialmente dopo un lungo periodo di inattività della VM.

---

## Comandi non trovati

**Problema**: `locate: command not found`  
**Soluzione**: `sudo apt install plocate && sudo updatedb`

**Problema**: `fuser: command not found`  
**Soluzione**: `sudo apt install psmisc`

**Problema**: `lsof: command not found`  
**Soluzione**: `sudo apt install lsof`

---

## Permessi e sudo

**Problema**: `Permission denied` su file in `/home/altroUtente/`  
**Causa**: I file degli altri utenti non sono leggibili da vagrant.  
**Soluzione**: Usare `sudo` per operazioni che richiedono accesso a file di altri utenti:
```bash
sudo tar cvpf archivio.tar /home/*
sudo cat /home/alice/.bashrc
```

**Problema**: `sudo echo "..." >> /path/file` → `Permission denied`  
**Causa**: Il redirect `>>` viene gestito dalla shell di vagrant, non da sudo.  
**Soluzione**: Usare `tee`:
```bash
echo "contenuto" | sudo tee -a /path/file
```

**Problema**: Utente aggiunto a un gruppo con `usermod -aG` ma il gruppo non risulta attivo  
**Causa**: La modifica ai gruppi è attiva solo alla prossima sessione di login.  
**Soluzione**: Fare logout e re-login, oppure:
```bash
newgrp nomegruppo
```

---

## Filesystem e directory

**Problema**: `tar: /newdisk: Cannot open: No such file or directory`  
**Causa**: La directory di destinazione non esiste.  
**Soluzione**: Crearla prima:
```bash
sudo mkdir /newdisk
tar -C /newdisk -xvpf archivio.tar
```

**Problema**: `rmdir: failed to remove 'dir': Directory not empty`  
**Soluzione**: Usare `rm -r nomedir` per cancellare ricorsivamente (attenzione: irreversibile).

---

## Terminale e editor

**Problema**: `crontab -e` → `Error opening terminal: xterm-kitty`  
**Causa**: Il terminale Kitty usa `TERM=xterm-kitty`, non riconosciuto dalla VM.  
**Soluzione rapida**:
```bash
TERM=xterm-256color crontab -e
```
**Soluzione permanente** (aggiungere al `.bashrc` sulla VM):
```bash
echo 'export TERM=xterm-256color' >> ~/.bashrc
source ~/.bashrc
```

---

## Processi in background

**Problema**: Processi rimasti in stato `Stopped` nel job control (visibili con `jobs`)  
**Causa frequente**: Comando avviato con `&` ma poi interrotto, oppure tentativo di usare un comando interattivo come `systemctl` senza argomenti in background.  
**Soluzione**: Killare i job fermi per indice:
```bash
kill %1 %2   # sostituire con i numeri mostrati da jobs
```

---

## Cartella condivisa /vagrant

**Problema**: `chmod +x /vagrant/script.sh` non funziona — il file resta non eseguibile  
**Causa**: `/vagrant` è montata con filesystem `vboxsf` che non supporta i permessi Unix.  
**Soluzione**: Copiare il file nella home prima di dargli i permessi, oppure eseguire direttamente con `bash`:
```bash
cp /vagrant/script.sh ~/
chmod +x ~/script.sh
# oppure, senza copiare:
bash /vagrant/script.sh argomento1 argomento2
```

---

## Errori comuni negli script bash

**Problema**: Script non eseguibile → `bash: ./script.sh: Permission denied`  
**Soluzione**:
```bash
chmod +x script.sh
./script.sh
```

**Problema**: `[: unexpected operator` o errori nei test  
**Causa frequente**: Spazio mancante dopo `[` o prima di `]`, o tra `!` e l'operatore.  
**Sbagliato**: `[!-d dir]` — **Corretto**: `[ ! -d dir ]`

**Problema**: `PID=!$` non cattura il PID del processo in background  
**Causa**: `!$` è history expansion (ultimo argomento del comando precedente), non il PID. La variabile corretta è `$!`.  
**Sbagliato**: `PID=!$` — **Corretto**: `PID=$!`

**Problema**: Incollare il corpo di uno script direttamente nella shell → variabili `$1`, `$THIS` vuote, comportamento inatteso  
**Causa**: Le variabili degli argomenti (`$1`, `$2`) sono vuote se il codice viene eseguito interattivamente invece che come script con argomenti.  
**Soluzione**: Salvare il codice in un file, renderlo eseguibile, e lanciarlo con gli argomenti corretti:
```bash
chmod +x script.sh
./script.sh argomento1 argomento2
```

**Problema**: `kill $PID` non termina un processo in stato `T` (Stopped)  
**Causa**: Un processo sospeso non può processare segnali finché non viene ripreso — SIGTERM viene recapitato ma resta in coda.  
**Soluzione**: Usare SIGKILL (termina anche i processi stopped) oppure riprendere prima il processo:
```bash
kill -KILL $PID           # opzione 1: forza terminazione immediata
kill -CONT $PID && kill $PID  # opzione 2: riprendi, poi termina ordinatamente
```

**Problema**: Script con `EOF` come ultima riga → `command not found: EOF`  
**Causa**: `EOF` è rimasto nel file come artefatto di un copy-paste da heredoc. Bash lo interpreta come comando.  
**Soluzione**: Aprire il file con `nano` e cancellare l'ultima riga contenente solo `EOF`.

**Problema**: Variabile passata a funzione senza `$` → il valore non viene scritto nel file atteso  
**Esempio**: `conta "$2" "FB" &` invece di `conta "$2" "$FB" &` — passa la stringa letterale `"FB"` invece del path del file temporaneo.  
**Soluzione**: Verificare che ogni variabile sia preceduta da `$`. Usare `bash -x script.sh` per vedere i valori espansi riga per riga.

**Problema**: Variabile vuota in una condizione causa errore  
**Causa**: La variabile non è tra virgolette.  
**Sbagliato**: `if [ -z $VAR ]` — **Corretto**: `if [ -z "$VAR" ]`

---

## VM Security (Parrot) — aggiornamento di sistema

**Problema**: `apt upgrade`/`full-upgrade` sembra bloccarsi a lungo, poi termina con
`dpkg: error processing package parrot-core (--configure): end of file on stdin at conffile prompt`
e lascia 6 pacchetti a metà (`parrot-core`, `parrot-interface`, `parrot-updater`, ecc.).  
**Causa**: l'upgrade ha incontrato una domanda su un file di configurazione
(`Configuration file '/etc/apt/sources.list.d/parrot.list' ... (Y/I/N/O/D/Z)`), ma stava girando
**senza un terminale interattivo** (es. lanciato dall'updater grafico) → non potendo rispondere,
dpkg si interrompe.  
**Soluzione**: rieseguire la configurazione **in un terminale vero**:
```bash
sudo dpkg --configure -a     # ricompare il prompt: D=diff, poi N (tieni la tua) o Y (versione nuova)
sudo apt --fix-broken install
sudo apt-get check           # nessun errore = pulito
sudo dpkg --audit            # vuoto = nessun pacchetto a metà
```
In dubbio sul conffile: `N` (default) tiene la configurazione attuale, scelta sicura e reversibile.

**Problema**: durante l'upgrade, muro di errori `vbox_fb.c: ... 'fb_debug_enter' ... Error 1`
(compilazione VirtualBox Guest Additions / `vboxvideo`).  
**Causa**: le Guest Additions installate non compilano contro i kernel recenti (funzioni rimosse da
`struct fb_ops`). **Non blocca l'esame**: boot, rete, terminale e tool funzionano. Si perdono solo
ridimensionamento finestra, clipboard e cartelle condivise.  
**Soluzione**: ignorabile. Se servono quelle funzioni, reinstallare le Guest Additions dalla ISO
aggiornata oppure avviare un kernel precedente dal menu GRUB.

**Soluzione che ha funzionato (2026-07-07)**: invece dell'ISO, reinstallare i pacchetti Debian/Parrot
(ricompilano via DKMS contro il kernel corrente) — usare le varianti **`-hwe`** (Hardware Enablement,
pensate per kernel più recenti di quelli stabili), non quelle base:
```bash
sudo apt install --reinstall virtualbox-guest-utils-hwe virtualbox-guest-x11-hwe
sudo reboot
```
Nota: il pacchetto `virtualbox-guest-dkms` non esiste su Parrot come pacchetto a sé — la parte DKMS
è già inclusa in `-utils`/`-x11`. Dopo il riavvio, il clipboard torna a funzionare.
⚠️ Un `apt upgrade` successivo che aggiorna il kernel può far ripresentare lo stesso problema
(i moduli DKMS restano legati alla versione di kernel per cui sono stati compilati) — se il
clipboard smette di funzionare di nuovo dopo un upgrade, ripetere questi due comandi.

---

## VM Security — Modulo S5 (nftlab.sh / Docker / Podman)

**Problema**: `./nftlab.sh` sembra bloccarsi senza output dopo aver stampato poco o nulla.
**Causa**: nessuna — se Docker sta scaricando/caricando le immagini dei container la prima volta,
può volerci più di un minuto senza stampare progresso visibile. Non interrompere con Ctrl+C troppo presto.
**Soluzione**: aspettare; verificare in un secondo terminale con `docker images`/`podman images` se
sono in corso operazioni.

**Problema**: `Cannot connect to the Docker daemon at unix:///run/user/1000/podman/podman.sock`
**Causa**: la variabile d'ambiente `DOCKER_HOST` è impostata (non nei file di shell standard —
`.bashrc`/`.zshrc`/`.profile` risultavano puliti; probabile hook di un tema/plugin zsh che la
reimposta ad ogni nuova shell) e punta a un socket Podman che non esiste, anche quando Docker vero
(`docker.io`/`dockerd`) è installato e attivo (`systemctl status docker` → `active (running)`).
**Soluzione**: `unset DOCKER_HOST` prima di ogni comando `docker`/alias container in un terminale
nuovo — va ripetuto a ogni nuovo terminale aperto, non è persistente. Causa radice non identificata
con certezza (da approfondire con calma se serve fastidio ricorrente, non urgente).

**Problema**: `validating compose.yaml: ... Additional property interface_name is not allowed`,
poi (dopo aver aggiornato Docker Compose alla v5.3.0 via `~/.docker/cli-plugins/`) l'errore cambia in
`interface_name requires Docker Engine v28.1 or later`.
**Causa**: la proprietà Compose `interface_name` (fissa il nome dell'interfaccia dentro il container,
usata da `nftlab.sh` per garantire `eth1`/`eth2`/`eth3` coerenti col diagramma) richiede un **Docker
Engine** v28.1+, non solo un client/Compose recente. Il pacchetto distro Parrot (`docker.io`,
versione `26.1.5+dfsg1-9+b13`) è troppo vecchio — le istruzioni ufficiali del corso
(`Istruzioni per la configurazione delle VM`) dicono di installare `docker-compose` via apt, senza
specificare una versione dell'Engine, quindi il gap tra script e pacchetto distro è plausibilmente
un limite delle istruzioni stesse, non un errore di setup.
**Soluzione adottata**: rimuovere `interface_name` (rendendo i nomi delle interfacce quelli di
default assegnati da Docker, es. `eth0` invece di `eth1`) **direttamente dallo script**, non dal
`compose.yaml` generato — `nftlab.sh` rigenera `compose.yaml` da zero a ogni lancio con un heredoc
(`cat > compose.yaml <<ENDOFCOMPOSEYAML` — vedi riga con `grep -n "compose.yaml" nftlab.sh`), quindi
modificare il file generato non serve, si perde al lancio successivo:
```bash
sed -i.bak '/interface_name:/d' nftlab.sh
```
Verificare poi con `ip a` dentro ogni container quale nome (`eth0`, `eth1`, ...) corrisponde a quale
rete, invece di fidarsi del diagramma originale.

**Problema**: `nft add rule filter FORWARD ...` → `Error: Could not process rule: No such file or directory`
**Causa**: nftables è case-sensitive — la catena era stata creata come `forward` (minuscolo, dallo
scheletro dell'esercizio "packet filter su endpoint"), mentre il comando la referenziava come
`FORWARD` (maiuscolo, convenzione iptables-style usata nel testo dell'esercizio "packet filter in
instradamento"). Sono due nomi diversi per nft.
**Soluzione**: `nft list ruleset` per vedere il nome esatto (case) di tabelle/catene effettivamente
create, prima di scrivere `add rule` — non fidarsi della convenzione di maiuscole/minuscole del testo
dell'esercizio.

---

## VM Security — Trasferimento file da target compromesso

**Problema**: `scp -P <porta> root@<ip>:/path/file .` → `subsystem request failed on channel 0` + `scp: Connection closed`
**Causa**: Il server SSH sulla porta non-standard ha il subsystem SFTP disabilitato (configurazione restrittiva intenzionale nel lab).
**Soluzione**: Usare `ssh` con `cat` e redirect — non richiede il subsystem SFTP:
```bash
ssh -p <porta> root@<ip> "cat /root/passwd.bak" > passwd.bak
ssh -p <porta> root@<ip> "cat /root/shadow.bak" > shadow.bak
```

**Problema**: `scp` lanciato da dentro una sessione SSH → copia il target su se stesso
**Causa**: Si è dimenticato di aprire un nuovo terminale locale; il comando gira sulla macchina remota.
**Soluzione**: Aprire un nuovo terminale sulla propria macchina Parrot e lanciare scp da lì.

---

## VM Security — IP target cambia dopo riavvio

**Problema**: dopo il riavvio di una VM target, `nmap -sn` mostra un IP diverso da prima (es. era `.100`, ora è `.102`). Il vecchio IP potrebbe ancora comparire nella scansione.
**Causa**: il DHCP di vboxnet0 assegna un nuovo lease ad ogni boot se quello precedente è scaduto. Il vecchio IP resta visibile brevemente come **ARP ghost** nella cache del gateway `.1`, poi sparisce.
**Soluzione**: rilanciare `nmap -sn` dopo qualche minuto per confermare gli IP aggiornati. Verificare in VirtualBox quante VM sono "Running" per escludere duplicati. Il conteggio definitivo dei target: numero di MAC con vendor Oracle/VirtualBox, escluso il proprio IP (nessun MAC) e il gateway `.1`.

---

## VM Security — CUPP non installabile per DNS failure

**Problema**: `sudo apt install cupp` → `Temporary failure resolving 'deb.parrot.sh'`
**Causa**: la VM Parrot non riesce a risolvere i nomi DNS — può succedere se la scheda NAT ha problemi o il resolver è mal configurato.
**Soluzione rapida**: creare la wordlist manualmente con `nano shannon.txt` inserendo varianti del target (nome, cognome, anno di nascita, username). Alternativa: usare `crunch` se disponibile (`which crunch`). Per ripristinare DNS: `ping 8.8.8.8` (testa connettività), poi `cat /etc/resolv.conf` (verifica nameserver configurato).

---

## VM Security — nmap su rete host-only

**Problema**: `nmap -sn <rete>/24` mostra un host in più rispetto alle VM avviate (es. 5 invece di 4)
**Causa**: Il server DHCP di VirtualBox gira sull'host fisico e risponde ai ping sulla rete host-only. Prende il primo IP del range DHCP (spesso `.100`). Ha latenza ~10× più bassa delle VM vere.
**Soluzione**: Ignorarlo — non ha porte aperte interessanti. Identificabile dalla latenza anomala.

**Problema**: `nmap -sn` lento (~10 secondi per /24) invece dei ~3 secondi attesi
**Causa**: Lanciato senza `sudo` — usa TCP/ICMP invece di ARP, meno efficiente su LAN.
**Soluzione**: `sudo nmap -sn <rete>/24`

---

## VM Security — Hydra http-get-form (Hydra 9.5)

**Problema**: `hydra ... http-get-form "path:params:condition:H=Cookie: value"` → `[ERROR] optional parameters must have the format X=value: <condition_string>`
**Causa**: In Hydra 9.5 il parser di http-get-form richiede che la **condition string sia l'ultimo campo**, dopo tutti gli optional (`H=`, `C=`, ecc.). Il PDF del prof usa la sintassi Hydra 8.x (condition prima dell'header) che non funziona più.
**Soluzione**: spostare la condition string in ultima posizione e usare `\:` per il due punti nell'header Cookie:
```bash
hydra IP \
  -L users.txt -P passwords.txt \
  http-get-form \
  "/path:user=^USER^&pass=^PASS^:H=Cookie\: PHPSESSID=<id>; security=low:Username and/or password incorrect."
```
Formato corretto: `"path:params:H=header\: value:condition_string"`

**Problema**: wordlist `xato-net-10-million-passwords-100.txt` non trovata su Parrot
**Soluzione**: usare `/usr/share/wordlists/fasttrack.txt` (222 password comuni, contiene "password")

---

## VM Security — Lab binary exploit (S4): compilare ed eseguire

**Problema**: `./es.c` → `bash: ./es.c: Permission denied`, poi (dopo `chmod +x es.c`) `./es.c: line 5: char: command not found` / `syntax error near unexpected token '('`
**Causa**: si sta tentando di eseguire il **sorgente** `es.c` (testo C), non il programma. La shell prova a interpretarlo come script bash.
**Soluzione**: si **compila** `es.c` e si **esegue** `es` (senza `.c`):
```bash
gcc -o es -fno-stack-protector -m32 -z execstack es.c
./es ciao
```
Regola: in ogni cartella esercizio, prima `gcc -o es … es.c`, poi si lavora su `es`.

**Problema**: `./es` → `Permission denied` (sul binario, non sul sorgente)
**Causa**: di solito **non è stato (ri)compilato** — l'`es` presente è quello fornito nell'archivio `pwn_lab.tar.gz`, senza bit di esecuzione (e con flag di compilazione ignoti). Nelle cartelle ci sono `es.c` (sorgente), `es_1` (binario precompilato dei docenti) ed eventualmente un `es` dell'archivio.
**Soluzione**: ricompilare il proprio `es` (lo crea eseguibile e coi flag noti): `gcc -o es … es.c`. In alternativa `chmod +x es`, ma meglio ricompilare per controllare i flag (canary/execstack contano nei gradini 3–4).

**Nota PIE / indirizzi**: i binari del lab sono **PIE**; con ASLR off (`echo 0 > /proc/sys/kernel/randomize_va_space`) gli indirizzi sono fissi per-run ma **diversi da quelli del PDF**. Ogni indirizzo (`secret`, `system`, ritorno) va trovato sul proprio binario con gdb (`info functions`, `p system`, `x/200xw $esp`), mai copiato dalle slide.

**Problema**: l'exploit funziona **dentro** gdb (`run $(perl -e ...)`) ma fuori, con lo stesso comando su `./es` da shell, va subito in segfault senza stampare la flag.
**Causa**: `gdb` disattiva l'ASLR per il processo debuggato **per default**, indipendentemente dal settaggio di sistema. Se nel frattempo la VM è stata riavviata (reboot, spegnimento accidentale, sospensione/ripristino), `randomize_va_space` torna al default (`2`) perché la scrittura in `/proc/sys/...` **non sopravvive al reboot** — l'indirizzo hardcoded trovato con gdb non è più valido fuori da gdb.
**Soluzione**: verificare `cat /proc/sys/kernel/randomize_va_space` prima di ogni sessione post-riavvio; se ≠ `0`, ridisattivare con `sudo su && echo 0 > /proc/sys/kernel/randomize_va_space && exit`, poi ripetere il comando standalone.

**Problema**: un indirizzo di ritorno/atterraggio composto a mano (little-endian) fa fallire l'exploit in modo "strano" — il crash torna `in <funzione>` invece di `?? ()`, come se l'indirizzo non fosse mai arrivato intatto.
**Causa**: uno dei 4 byte dell'indirizzo è un **"bad character"**: `0x20` (spazio), `0x09` (tab), `0x0a` (newline) o `0x00` (terminatore). Se il payload passa per `$(perl -e '...')` **senza virgolette**, bash fa *word splitting* su spazio/tab/newline e tronca l'argomento esattamente lì; `0x00` invece termina qualunque stringa C, indipendentemente da come viaggia.
**Soluzione**: prima di scegliere un indirizzo di atterraggio, controllare i suoi 4 byte little-endian e scartare quelli con `0x20`/`0x09`/`0x0a`/`0x00` — nella stessa fascia di memoria (es. dentro un NOP sled) ce ne sono quasi sempre altri validi vicini.

**Problema**: un indirizzo di atterraggio sullo stack (non di codice) funziona dentro gdb ma dà `Segmentation fault` fuori, anche con ASLR disattivata.
**Causa**: a differenza degli indirizzi di **codice** (`.text`, fissi con ASLR off), gli indirizzi **sullo stack** dipendono anche da `argv`/ambiente all'avvio. gdb lancia l'eseguibile con il **percorso assoluto** come `argv[0]`; da shell si usa spesso `./es` (più corto) — la differenza di lunghezza (più eventuali differenze nell'ambiente ereditato) sposta la posizione reale del buffer sullo stack, anche di centinaia di byte.
**Soluzione**: non fidarsi del dump (`x/200xw $esp`) preso sotto gdb per un exploit che punta allo stack. Far generare un core dump dalla vera esecuzione standalone e analizzare quello: se il binario è **SUID**, il dump non si salva di default (`fs.suid_dumpable=0`) → `sudo sysctl -w fs.suid_dumpable=1`, rigenerare il crash, poi `coredumpctl list` + `sudo coredumpctl gdb <PID>` (il core appartiene a root, serve sudo). Nel dump si riconosce anche `argv[0]` come stringa ASCII sullo stack (utile per orientarsi).

**Problema**: `find $esp, $esp+20000, "pattern"` → `Invalid search space, end precedes start.`
**Causa**: aritmetica indirizzi su target **32 bit**. `$esp` vicino alla cima dello stack (es. `0xffffcadc`) ha poco margine prima del limite `0xffffffff`; sommare un valore troppo grande sfora quel limite e "avvolge" (wrap-around) l'indirizzo risultante, che dopo il troncamento a 32 bit diventa numericamente più piccolo di `$esp` — gdb rifiuta l'intervallo perché sembra invertito.
**Soluzione**: usare un incremento che stia dentro il margine reale rimasto sotto `0xffffffff` (es. `find $esp, +0x3000, "SHELL="`); se non trova nulla, allargare di poco (`+0x3500`), mai a salti larghi come `+20000` vicino alla cima dello stack.

**Problema**: `x/500s $esp` (o conteggi simili) si esaurisce prima di raggiungere la zona `argv`/`envp` in cima allo stack, mostrando solo byte grezzi/garbage.
**Causa**: appena dopo `main`, `$esp` è ancora dentro il frame locale, pieno di byte `\x00` che gdb legge come tante mini-stringhe vuote — il conteggio si esaurisce senza coprire la distanza (spesso migliaia di byte) fino a `argv`/`envp`.
**Soluzione**: preferire `find $esp, +lunghezza, "pattern"` (es. `"SHELL="`) invece di scorrere a occhio con `x/Ns`; è mirato e non soffre del problema del conteggio.

**Problema**: dopo un `continue` (`c`) il programma va in `SIGSEGV ... in ?? () from /lib32/libc.so.6` e i comandi successivi (`find`, `p`, ecc.) rispondono `No registers.` / `The program is not being run.`
**Causa**: comportamento atteso, non un bug — si era fermati su un breakpoint (es. `b *main`) dopo un `run` **senza payload/argomenti**; proseguendo, il programma raggiunge la `strcpy`/`gets` che si aspetta un argomento, trova `NULL` e crasha nella libc. Una volta morto il processo, i registri non esistono più finché non si fa un nuovo `run`.
**Soluzione**: usare il breakpoint solo per leggere la memoria (indirizzi di libreria, stack) subito dopo `run`, senza proseguire con `c` se non si è passato un payload valido; per il tentativo vero, rilanciare con `run <payload>` (eventualmente `delete <N>` prima per togliere il breakpoint che non serve più).

**Problema**: un indirizzo di una **funzione di libreria** (es. `system`) contiene un bad character (`0x20`/`0x09`/`0x0a`), ma a differenza di un indirizzo di stack non si può "spostare di qualche byte" per evitarlo — la funzione ha un solo punto d'ingresso valido.
**Causa**: stesso meccanismo del bad character su indirizzi di stack (`$(...)` non quotato → word splitting della shell), ma qui il rimedio "scegli un indirizzo vicino" non è applicabile.
**Soluzione**: quotare l'intera sostituzione di comando: `run "$(perl -e '...')"` invece di `run $(perl -e '...')`. Le doppie apici esterne impediscono lo split sui caratteri IFS (spazio/tab/newline) preservandoli come byte letterali del payload; le eventuali apici singole interne (lo script perl) restano un contesto di parsing separato e non ne risentono.

---

## Checklist pre-snapshot "baseline-pulita" (VM Security)

Prima di congelare la baseline, verificare che i tool delle 5 famiglie d'esame ci siano già:
```bash
which nmap suricata nikto sqlmap iptables nft tcpdump   # enum/web/NIDS/firewall
which gcc gdb objdump                                    # binary exploitation
dpkg -l | grep -E 'libc6-i386|gcc-multilib'             # supporto 32-bit (binari x86_32 del corso)
```
Tool mancanti tipici su Parrot di default: **`suricata`** (NIDS, famiglia d'esame!) e **`gcc-multilib`**.
Installarli PRIMA dello snapshot così restano nella baseline:
```bash
sudo apt install -y suricata gcc-multilib
```
Snapshot: `VBoxManage snapshot "LabSicurezzaInformatica" take "baseline-pulita"`.
