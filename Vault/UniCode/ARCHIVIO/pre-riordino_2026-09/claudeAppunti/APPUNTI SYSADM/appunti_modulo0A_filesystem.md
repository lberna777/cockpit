# Virtual Machine con Vagrant

Ho inizializzato una cartella di lavoro per amministrazione di sistemi, successivamente inizializzato la virtual machine (OS: Linux-Debian) e avviata con:

```bash
vagrant up --provider=virtualbox
```

Successivamente sono entrato nella VM tramite SSH:

```bash
vagrant ssh
```

---

## Valutazione della situazione iniziale

Ho valutato la situazione attuale con i comandi `pwd`, `whoami`, `id`.

Questi mi hanno detto rispettivamente:
- **`pwd`** — la directory dove mi trovo (`/home/nomeutente`)
- **`whoami`** — il mio nome utente (`vagrant`)
- **`id`** — ID utente, Group ID primario e i gruppi a cui partecipa il mio utente (`uid=1000`, `gid=1000`, `groups=1000`)

---

## Struttura del filesystem — `ls /`

### Binari ed eseguibili — i programmi veri e propri

| Directory | Descrizione |
|---|---|
| `bin` | Comandi essenziali utilizzabili da tutti gli utenti |
| `sbin` | Comandi di sistema riservati all'utente root |
| `usr` | Contiene la maggior parte dei programmi installati |
| `lib` | Librerie condivise da cui dipendono i binari |

### Configurazione — il cervello del sistema

| Directory | Descrizione |
|---|---|
| `etc` | Contiene tutti i file di configurazione del sistema; utile a capire il funzionamento di un servizio |

### Dati utente

| Directory | Descrizione |
|---|---|
| `home` | Comprende una sotto-directory per ogni utente normale (non root) |
| `root` | Home esclusiva di root |

### Filesystem virtuali — privi di file reali, sono interfacce al kernel

| Directory | Descrizione |
|---|---|
| `proc` | Informazioni sui processi in esecuzione |
| `sys` | Interfaccia all'hardware e ai driver del kernel |
| `dev` | Rappresentazione dei dispositivi fisici |

### Dati variabili e temporanei

| Directory | Descrizione |
|---|---|
| `var` | Contiene tutto ciò che varia nel tempo: log, database, code di stampa… |
| `tmp` | File temporanei, svuotati ad ogni riavvio |
| `run` | Dati di runtime dei servizi |

### Nota Vagrant

| Directory | Descrizione |
|---|---|
| `vagrant` | Mount della cartella di installazione della VM (nel mio caso `/sysAdmin-lab`) |

---

## Analisi delle cartelle principali

### `ls /etc`

Mi dà accesso ai file di configurazione di sistema. Noto che molti finiscono in `.d` o `.conf`:
- **`.conf`** — file di configurazione singoli
- **`.d`** — directory che contengono frammenti di configurazione, che il sistema legge e unisce. Serve a far sì che più pacchetti possano scrivere le loro regole senza sovrascriversi

Posso leggere informazioni sul sistema tramite:
- `cat /etc/debian_version` — per vedere la versione dell'OS
- `cat /etc/hostname` — per vedere il nome della macchina

### `ls /var/log`

Mi dà accesso ai registri, che tengono nota di tutto quello che accade nel sistema:
- **`syslog`** — il log generale del sistema
- **`auth.log`** — registra ogni autenticazione nel sistema, al login o all'uso di `sudo`
- **`btmp`** — registra i tentativi di login falliti

---

## Permessi — `ls -la ~`

Uso il comando `ls` con le opzioni `-l` e `-a`, raggruppate in `-la`, con argomento `~` (che indica `/home/vagrant`, la mia cartella utente).

Ogni elemento è identificato da una stringa di 10 caratteri:

```
d  rwx  rwx  rwx
│   │    │    │
│   │    │    └── permessi degli utenti esterni al gruppo del creatore
│   │    └─────── permessi del gruppo
│   └──────────── permessi del proprietario
└──────────────── tipo: (d) directory | (-) file | (l) link
```

I permessi sono: **r** (lettura), **w** (scrittura), **x** (esecuzione del file come programma, oppure accesso/ingresso se è una directory).

### Permessi di default alla creazione

Linux assegna permessi automaticamente quando si crea un nuovo oggetto:
- **Directory** → `rwxr-xr-x`
- **File** → `rw-r--r--`

Un file non è eseguibile finché non lo si dichiara esplicitamente tale.

---

## `chmod` — modifica dei permessi

```bash
chmod NNN nomefile
```

Ogni cifra rappresenta un blocco di permessi (proprietario, gruppo, esterni) ed è la somma dei valori dei permessi attivi:

| Permesso | Valore |
|---|---|
| lettura (r) | 4 |
| scrittura (w) | 2 |
| esecuzione/accesso (x) | 1 |

Se voglio tutti i permessi → `4+2+1 = 7`

### Differenza chiave tra `r` e `x` su una directory

Con `r` posso **vedere** quali nomi di file sono dentro alla cartella — lo faccio tramite `ls`.  
Con `x` posso **attraversare** la cartella, entrandoci con `cd` e accedere ai file al suo interno.

Vanno spesso di pari passo. L'unico caso utile di `x` senza `r` è per permettere a qualcuno di accedere a un file specifico dentro una directory se ne conosce già il nome esatto, senza poter vedere cos'altro c'è dentro.

<!-- AUTO-LINKS:START -->
## 🔗 Collegati


**Hub:** [[master_map_studio]] · [[glossario_sysadm]] · [[concept_maps]] · [[troubleshooting_vm]] · [[metodo_studio_esami_pratici]]
<!-- AUTO-LINKS:END -->
