All'interno di linux, ogni cosa è un numero, compresi gli utenti. I vari  **vagrant, root**... sono tutte conversioni raccolte in /etc/passwd

Per informarci sui numeri che ci riguardano usiamo **id**

**uid=1000(vagrant) gid=1000(vagrant) groups=1000(vagrant)**

che ci restituisce il nostro numero personale, del gruppo a cui apparteniamo (non ricordo cosa cambia tra gid e goups)

Per vedere tutti gli utenti disponibili sul pc eseguiamo **cat /etc/passwd**

Otteniamo stringhe di questo tipo:

vagrant:x:1000:1000:,,,:/home/vagrant:/bin/bash  
   | | | | | | |  
  nome | UID GID GECOS home shell  
        |  
      password (sempre "x" — la vera hash è in /etc/shadow)

(inserisci lo schema fatto bene al posto di questo)

I vari UID seguono una convenzione che vede 0 dedicato esclusivamente all'utente root, i numeri da 1 a 999 per i deamon e utenti creati dal computer internamente per far funzionare cose, i numeri da 1000 in poi sono invece dedicati a utenti fisici reali

**STORAGE DELLA PASSWORD**

**Le password non sono in `/etc/passwd` (leggibile da tutti) ma in `/etc/shadow`, accessibile solo da root. Contiene gli hash delle password e le politiche di scadenza.**

accedo tramite

```
sudo cat /etc/shadow | grep vagrant
```

e ottengo righe di questo tipo (serve una spiegazione dettagliata della composizione

```
vagrant:$6$abc123...:19800:0:99999:7:::
   |        |          |   |   |   |
  nome    hash pw    gg ult  min max warn
```

&nbsp;

**GESTIONE DEGLI UTENTI**

posso creare un utente da zero tramite:

```
sudo useradd -m -s /bin/bash alice
```

dove uso -m per indicare di creare la directory /home/alice e -s per assegnare bash come shell di login, evitando di usare sh o altro

I profili sono proteggibili tramite password tramite:

```
sudo passwd alice
```

Se invece mi interessa modificare un utente esistente e i suoi privilegi:

```
sudo usermod -aG sudo bob
```

(aggiungi una lista di cose fattibili tramite usermod, non credo proprio che -aG sia l'unico flag)

Posso muovermi tra un utente e l'altro con:

```
su - alice
```

(l'uso del trattino è necessario per spostarci completamente nell'ambiente completo di alice, con le proprie variabili di ambiente e directory, senza si cambia "nome" senza cambiare ambiente dall'utente precedente)

Infine posso cancellare un utente (comprendendo o meno la sua directory home) tramite: 

```
sudo userdel -r alice
```

dove -r indica proprio la pulizia della cartella home o meno

**PROPRIETA' DI UN FILE**

Alla creazione di esso, un file viene legato all'utente che lo ha creato e al suo gruppo, di seguito vediamo come impostare un creatore diverso dall'originale a un file e come fare la stessa operazione relativamente al gruppo di appartenenza del creatore

```
# Creare un file come vagrant
[](#cb18-6)echo "file di vagrant" > file_vagrant.txt
[](#cb18-7)ls -la file_vagrant.txt
[](#cb18-8)# output: -rw-r--r-- 1 vagrant vagrant ...
[](#cb18-9)
[](#cb18-10)# Cambiare il proprietario ad alice
[](#cb18-11)sudo chown alice file_vagrant.txt
[](#cb18-12)ls -la file_vagrant.txt
[](#cb18-13)# output: -rw-r--r-- 1 alice vagrant ...
[](#cb18-14)
[](#cb18-15)# Cambiare sia proprietario che gruppo in un solo comando
[](#cb18-16)sudo chown alice:alice file_vagrant.txt
[](#cb18-17)ls -la file_vagrant.txt
[](#cb18-18)# output: -rw-r--r-- 1 alice alice ...
[](#cb18-19)
[](#cb18-20)# Cambiare solo il gruppo
[](#cb18-21)sudo chgrp vagrant file_vagrant.txt
[](#cb18-22)ls -la file_vagrant.txt
[](#cb18-23)# output: -rw-r--r-- 1 alice vagrant ...
```

**L'IMPORTANZA DEL COMANDO SUDO**

**`sudo` (superuser do) permette a un utente autorizzato di eseguire un singolo comando come root, senza diventare root permanentemente. La configurazione che stabilisce chi può usare `sudo` e per quali comandi sta in `/etc/sudoers`.**

attraverso **sudo -l**  ho accesso a tutti i comandi che posso eseguire come **sudo** (non ho capito cosa ottengo materialmente da questo comando ti allego il mio output e aggiungi un analisis dettagliata negli appunti finali)

vagrant@bookworm:~/Lab2A\$ sudo -l  
Matching Defaults entries for vagrant on bookworm:  
    env_reset, mail_badpass,  
    secure_path=/usr/local/sbin\\:/usr/local/bin\\:/usr/sbin\\:/usr/bin\\:/sbin\\:/bin,  
    use_pty

User vagrant may run the following commands on bookworm:  
    (ALL) NOPASSWD: ALL

(come mai posso usare sudo dal profilo vagrant anche se quando chiedo groups vagrant mi dice vagrant : vagrant e non vagrant : vagrant sudo?)

(ho modo di vedere una lista solo degli user fisici del pc?)

**ESERCIZIO FINALE**

vagrant@bookworm:~/Lab2A\$ sudo groupadd progetto  
vagrant@bookworm:~/Lab2A\$ sudo useradd -m -s /bin/bash alice  
vagrant@bookworm:~/Lab2A\$ sudo useradd -m -s /bin/bash bob  
vagrant@bookworm:~/Lab2A\$ sudo usermod -aG progetto alice  
vagrant@bookworm:~/Lab2A\$ sudo usermod -aG progetto bob  
vagrant@bookworm:~/Lab2A\$ groups alice  
alice : alice progetto  
vagrant@bookworm:~/Lab2A\$ groups bob  
bob : bob progetto  
vagrant@bookworm:~/Lab2A\$ sudo mkdir /srv/progetto  
vagrant@bookworm:~/Lab2A\$ sudo chown root:progetto /srv/progetto

(perchè cambio possessore (o creatore?) della directory?)

  
vagrant@bookworm:~/Lab2A\$ sudo chmod 770 /srv/progetto  
vagrant@bookworm:~/Lab2A\$ ls -la /srv/

(srv è una cartella preesistente? cosa sono gli altri ifle oltre progetto?)  
total 12  
drwxr-xr-x 3 root root 4096 Apr 21 15:00 .  
drwxr-xr-x 19 root root 4096 Apr 15 16:03 ..  
drwxrwx--- 2 root progetto 4096 Apr 21 15:00 progetto  
vagrant@bookworm:~/Lab2A\$ su - alice  
Password:  
su: Authentication failure  
vagrant@bookworm:~/Lab2A\$ sudo passwd alice  
New password:  
Retype new password:  
passwd: password updated successfully  
vagrant@bookworm:~/Lab2A\$ sudo passwd bob  
New password:  
Retype new password:  
passwd: password updated successfully  
vagrant@bookworm:~/Lab2A\$ su - alice  
Password:  
alice@bookworm:~\$ cd /srv/progetto/  
alice@bookworm:/srv/progetto\$ echo "file di alice" > alice.txt  
alice@bookworm:/srv/progetto\$ ls -la

(ugualmente qua, cosa sono gli altri due file oltre a alice.txt? in questo caso sono sicuro la cartella non esistesse prima perchè l'ho creata io)  
total 12  
drwxrwx--- 2 root progetto 4096 Apr 21 15:03 .  
drwxr-xr-x 3 root root 4096 Apr 21 15:00 ..  
\-rw-r--r-- 1 alice alice 14 Apr 21 15:03 alice.txt  
alice@bookworm:/srv/progetto\$ exit  
logout  
vagrant@bookworm:~/Lab2A\$ su - bob  
Password:  
bob@bookworm:~\$ cd /srv/progetto/  
bob@bookworm:/srv/progetto\$ cat alice.txt  
file di alice  
bob@bookworm:/srv/progetto\$ exit  
logout  
vagrant@bookworm:~/Lab2A\$ sudo useradd -m -s /bin/bash sconosciuto  
vagrant@bookworm:~/Lab2A\$ sudo passwd sconosciuto  
New password:  
Retype new password:  
passwd: password updated successfully  
vagrant@bookworm:~/Lab2A\$ su - sconosciuto  
Password:  
sconosciuto@bookworm:~\$ cd /srv/progetto/  
\-bash: cd: /srv/progetto/: Permission denied  
sconosciuto@bookworm:~\$ exit  
logout

<!-- AUTO-LINKS:START -->
## 🔗 Collegati

- [[appunti_modulo2A_utenti_permessi]]
- [[lezione_modulo2A_utenti_permessi]]

**Hub:** [[master_map_studio]] · [[glossario_sysadm]] · [[concept_maps]] · [[troubleshooting_vm]] · [[metodo_studio_esami_pratici]]
<!-- AUTO-LINKS:END -->
