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

## VM Security — nmap su rete host-only

**Problema**: `nmap -sn <rete>/24` mostra un host in più rispetto alle VM avviate (es. 5 invece di 4)
**Causa**: Il server DHCP di VirtualBox gira sull'host fisico e risponde ai ping sulla rete host-only. Prende il primo IP del range DHCP (spesso `.100`). Ha latenza ~10× più bassa delle VM vere.
**Soluzione**: Ignorarlo — non ha porte aperte interessanti. Identificabile dalla latenza anomala.

**Problema**: `nmap -sn` lento (~10 secondi per /24) invece dei ~3 secondi attesi
**Causa**: Lanciato senza `sudo` — usa TCP/ICMP invece di ARP, meno efficiente su LAN.
**Soluzione**: `sudo nmap -sn <rete>/24`

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
