Ho osservato i file di configurazione utente:        **/etc/skel        &        /etc/default/useradd        &        /etc/login.defs**

**/etc/skel        -->**        Contiene lo scheletro della home che viene copiato alla creazione della home di ogni nuovo utente **aggiunto con useradd**

**/etc/default/useradd        -->**        Contiene i valori di default che **useradd** assegna **se non gli vengono date specifiche ulteriori**

**/etc/login.defs        -->        è la configurazione più bassa,** include le **policy globali** per la gestione degli account (come impostazioni sulla scadenza della password o come scegliere gli UID da assegnare agli                                                       utenti)

**DIRECTORY COLLABORATIVA CON SGID**

Ho creato due nuovi utenti **Maria** e **Piero**         (ho notato che hanno preso i UID 1004 e 1005, anche se gli utenti che occupavano 1001, 1002, 1003 sono già stati eliminati)

```
sudo useradd -m -s /bin/bash maria
sudo useradd -m -s /bin/bash piero
```

e ho controllato che fossero entrambi correttamente solo nel loro gruppo omonimo

successivamente creo un gruppo **programmatori** e modifico gli utenti con **usermod** per aggiungere **oltre al gruppo di base il nuovo gruppo** programmatori

```
sudo groupadd programmatori
sudo usermod -aG programmatori maria
sudo usermod -aG programmatori piero
```

creo la cartella che diventerà condivisa (capisco che sto creandola, ma sotto quale utente? vagrant? e cosa fa la seconda riga di codice?)

```
sudo mkdir /home/programmatori
sudo chgrp programmatori /home/programmatori
```

cambio le impostazioni della directory e il bashrc (che cos'è?) di entrambi gli utenti facendo si che sia il proprietario che i membri del gruppo possano fare tutto, gli altri nulla (perche 02770? di solito erano numeri a tre cifre, rispettivamente creatore, gruppo, altri) (che cosa fa umask, che cos'è?, cosa fa sudo tee -a?, sezione molto confusa non capisco cosa dovrei trarne)

```
sudo chmod 02770 /home/programmatori
```

```
# Aggiungere umask 0002 al .bashrc di entrambi gli utenti
[](#cb8-2)echo "umask 0002" | sudo tee -a /home/maria/.bashrc
[](#cb8-3)echo "umask 0002" | sudo tee -a /home/piero/.bashrc
```

Ora attraverso i due utenti programmatori posso accedere a questa cartella esclusiva condivisa tra di loro e tutti i membri di "programmatori". possono leggere e scrivere al loro interno (credo) grazie a chmod 02770 (altrimenti bisogna cambiare con chmod i singoli file ogni volta che si creano) mentre chi è fuori dal gruppo non può entrarvi.

```
# Come maria
[](#cb14-2)su - maria
[](#cb14-3)cd /home/programmatori
[](#cb14-4)touch file_di_maria.txt
[](#cb14-5)echo "contenuto di maria" > file_di_maria.txt
[](#cb14-6)ls -la
[](#cb14-7)# -rw-rw-r-- 1 maria programmatori ...  file_di_maria.txt
[](#cb14-8)#                    ^^^^^^^^^^^^^
[](#cb14-9)#                    gruppo programmatori, non maria — grazie a SGID
[](#cb14-10)exit
[](#cb14-11)
[](#cb14-12)# Come piero
[](#cb14-13)su - piero
[](#cb14-14)cd /home/programmatori
[](#cb14-15)cat file_di_maria.txt        # → "contenuto di maria" ✓
[](#cb14-16)echo "aggiunta di piero" >> file_di_maria.txt   # → funziona ✓
[](#cb14-17)exit
[](#cb14-18)
[](#cb14-19)# Come vagrant (fuori dal gruppo)
[](#cb14-20)cd /home/programmatori        # → Permission denied ✓
```

&nbsp;

&nbsp;

&nbsp;

<!-- AUTO-LINKS:START -->
## 🔗 Collegati

- [[appunti_modulo2B_lab_utenti_permessi_file]]
- [[lezione_modulo2B_lab_utenti_permessi_file]]

**Hub:** [[master_map_studio]] · [[glossario_sysadm]] · [[concept_maps]] · [[troubleshooting_vm]] · [[metodo_studio_esami_pratici]]
<!-- AUTO-LINKS:END -->
