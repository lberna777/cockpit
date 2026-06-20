Modulo 3B        28/03/26

Le fasi che attraversa un programma sono l'installazione, l'aggiornamento e la disinstallazione. ovviamente ciascuna fase ha delle dipendenze che lo legano a prerequisiti hardware o di sistema, o a altri componente software da installare.

lo standard più basico per l'installazione è quella manuale, che vede l'installazione direttamente dai binari del programma, inseriti manualmente nei posti corretti a nostro rischio e pericolo (bisogna saper constatare i prerequisiti). 

Si può invece installare tramite sorgente (tipicamente un archivio compresso) che una volta reperito si estrae e permette di configurare i sorgenti a nostro piacimento per poi proseguire con l'installazione (sempre guidata nel caso dei sorgenti?)

### Autenticità del software scaricato

Prima di estrarre un archivio, verificarne l’autenticità:

```
[](#cb3-1)gpg --verify FILE.asc FILE.tar.gz    # (mostra key id)
[](#cb3-2)gpg --keyserver pgpkeys.mit.edu --recv-key <KEY_ID>
[](#cb3-3)gpg --verify FILE.asc FILE.tar.gz    # ripetere
[](#cb3-4)
[](#cb3-5)# Alternativa con fingerprint:
[](#cb3-6)sha256 -c FILE.sha256
```

l'installazione tramite sorgente risulta utile nel momento in cui eseguiamo queste verifiche che però nella pratica spesso non si sfruttano. ma risulta anche più difficile da manutenere e richiede molti componenti ausiliari che potrebbero ritorcerci contro come vettori di attacco da un malintenzionato. (cosa si intende per distribuzione e pacchetti? non sono i pacchetti compressi di cui parlavamo prima come sorgenti? come funzionano? esempi pratici?)

* * *

PACCHETTO

un pacchetto è un file singolo che contiene in forma compatta un software precompilato, con procedure di pre e post installazione delineate e check per la compatibilità dei prerequisiti

Criteri per la scelta di una distribuzione

| Criterio | Descrizione |
| --- | --- |
| **Architetture supportate** | Quasi tutte supportano amd64; per architetture esotiche verificare |
| **Stabilità vs aggiornamento** | Distro “stabili” includono solo sw collaudato; altre preferiscono novità anche a costo di minor robustezza |
| **Versioned vs rolling** | Versioned: aggiornamenti correttivi solo durante il ciclo; rolling: sempre all’ultima versione |
| **LTS** | Per server: supporto 5/7 anni con solo security backport |
| **Ampiezza pacchetti** | Da 1500 (minimali) a 26000+ (Debian) |

**Debian** (la nostra VM): versioned, orientata alla stabilità, ~26000 pacchetti.

## 3\. Due Famiglie: Debian e Red Hat

Quasi tutte le distro Linux derivano da una di queste due.

Entrambe usano una struttura a tre livelli: 1. **Tool di basso livello** per gestire singoli pacchetti (`dpkg` / `rpm`) 2. **Tool intermedi** per gestione coordinata di pacchetti e dipendenze (`apt` / `yum`/`dnf`) 3. **Tool per il reperimento automatico** da repository

DIPENDENZE (si intendono dipendenze tra software che  magari ne richiedono un altro preinstallato?)

queste dipendenze possono essere logiche: uno strumento non serve (inutile) se non ho (uso)  l'altro. o fisiche: uno serve all'altro per poter funzionare

lo strumento chiamato package manager conosce l'intero grafo che relaziona i programmi attraverso queste dipendenze e risolve automaticamente le dipendenze al momento dell'installazione e della rimozione

PACCHETTI BASE E PACCHETTI -dev

i pacchetti -dev sono opzionali e inutili per sistemi non usati per lo sviluppo. contengono le parti necessarie a compilare programmi che usano il software che stiamo installando e non solo ad eseguirlo come i pacchetti base

* * *

REPOSITORY

le repository sono sostanzialmente raccolte indicizzate di pacchetti. il package manager legge per ogni repo l'indice e i metadati, rendendogli possibile conoscere le dipendenze tra pacchetti

(non ho capito la parte subito sotto, configurazione repo in debian apt, ho installato pacchetti su debian ma non mi sembra di aver fatto cosi)

COMANDI DPKG E APT SU DEBIAN

### Tabella comandi principali

| Operazione | Comando dpkg | Comando apt |
| --- | --- | --- |
| Update indice repo | —   | `apt update` |
| Cercare pacchetto | —   | `apt search <keyword>` |
| Installare da repo | —   | `apt install <nome>` |
| Installare da file .deb | `dpkg -i file.deb` | —   |
| Aggiornare tutto | —   | `apt upgrade` |
| Aggiornare un pacchetto | —   | `apt upgrade <nome>` |
| Rimuovere (mantieni config) | `dpkg -r <nome>` | `apt remove <nome>` |
| Rimuovere (+ config) | `dpkg -P <nome>` | `apt purge <nome>` |
| Rimuovere dipendenze orfane | —   | `apt autoremove` |
| Info pacchetto | `dpkg -s <nome>` | `apt show <nome>` |
| Lista file installati | `dpkg -L <nome>` | —   |
| A quale pkg appartiene un file | `dpkg -S /path/file` | —   |
| Lista pacchetti installati | `dpkg -l` | `apt list --installed` |
| Lista aggiornabili | —   | `apt list --upgradable` |
| Provenienza pacchetto |     |     |

n.B. remove rispetto a purge non rimuove i file di configurazione, essenziali da rimuovere se vogliamo reinstallare lo stesso pacchetto da zero

7/8)  (come funziona questa autenticazione dei pacchetti? anche se non credo sia essenziale per l'esame. non ho mai autenticato un pacchetto e non capisco come si garantisce che la chiave non sia recapitata da malintenzionati)

9 - installare aggiornare e disinstallare un software presenta dei rischi...

10- non mi sembra importante per il mio esame

* * *

ESERCIZII

ho acceso la vm

ES 1

```
# Aggiorna l'indice dei repository
[](#cb13-2)sudo apt update
```

non ha risultato programmi da aggiornare

```
# Quanti pacchetti sono aggiornabili?
[](#cb13-5)apt list --upgradable 2>/dev/null | wc -l
```

nessuno, giustamente, ma non ho capito che cosa fa 2>/dev/null | wc -l

```
# Quanti pacchetti sono installati?
[](#cb13-8)dpkg -l | wc -l
```

325, e | wc -l conta le righe vero?

ES 2

```
# Installa tree (visualizza filesystem ad albero)
[](#cb14-2)sudo apt install tree
```

installazione a buon fine

```
# Dove sono stati installati i suoi file?
[](#cb14-5)dpkg -L tree
```

mi da le directory, ma come funziona dpkg? cosa fa -L?

```
# Cosa fa esattamente?
[](#cb14-8)apt show tree
```

descrizione completa del pacchetto ok

```
# Prova:
[](#cb14-11)tree /etc/systemd/system/
```

funziona!

ES 3

```
# Cerca pacchetti correlati a htop
[](#cb15-2)apt search htop
```

mi fa vedere dei pacchetti ma non capisco se sono installati ne in che modo sono "correlati", ma poi perchè vedo dei correlati a un programma con search che voldire cerca

```
# Vedi i metadati (dipendenze, dimensione, descrizione)
[](#cb15-5)apt show htop
```

non lo avevamo già visto sto comando?

```
# Installa
[](#cb15-8)sudo apt install htop
```

ha funzionato ma mi ha chiesto un autorizzazione Y/n che per tree non mi ha chiesto  

```
# Verifica da quale repository viene
[](#cb15-11)apt-cache showpkg htop
```

bello ma non capisco come sono strutturate le info che mi vengono date da questo comando

ES 4

```
# A quale pacchetto appartiene /bin/ls?
[](#cb16-2)dpkg -S /bin/ls
```

mi ha risposto coreutils: /bin/ls ma non capisco che significa

```
# Quali file ha installato quel pacchetto?
[](#cb16-8)dpkg -L openssh-client
```

elencone di un sacco di file, ci sta

ES 5

```
# Quali librerie usa sshd?
[](#cb17-2)ldd /usr/sbin/sshd
[](#cb17-3)
[](#cb17-4)# Conta quante librerie dinamiche usa
[](#cb17-5)ldd /usr/sbin/sshd | wc -l
[](#cb17-6)
[](#cb17-7)# Confronta con un binario più semplice
[](#cb17-8)ldd /bin/ls
```

pacchetti ampli avranno più dipendenze da librerie mentre i binari meno, ma cosa cambia tra libreria dinamica e non?

ES 6

```
# Rimuovi tree mantenendo config (se esistesse)
[](#cb18-2)sudo apt remove tree
[](#cb18-3)
[](#cb18-4)# Verifica che sia andato via
[](#cb18-5)which tree    # deve dare errore
[](#cb18-6)
[](#cb18-7)# Rimuovi le dipendenze orfane
[](#cb18-8)sudo apt autoremove
```

direi tutto chiaro

ES 7

```
cat /etc/apt/sources.list
[](#cb19-2)ls /etc/apt/sources.list.d/
[](#cb19-3)ls /etc/apt/trusted.gpg.d/
```

ho letto ma non capisco la sources.list cosa mi restituisce, gli altri due comandi sotto stampano solo che sono directory

&nbsp;

<!-- AUTO-LINKS:START -->
## 🔗 Collegati

- [[appunti_modulo3B_gestione_pacchetti]]
- [[lezione_modulo3B_gestione_pacchetti]]

**Hub:** [[master_map_studio]] · [[glossario_sysadm]] · [[concept_maps]] · [[troubleshooting_vm]] · [[metodo_studio_esami_pratici]]
<!-- AUTO-LINKS:END -->
