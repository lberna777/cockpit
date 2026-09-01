# Lezione — Modulo S9: Demoni di Sistema + Autorizzazione + PAM
**Corso**: Lab Sicurezza Informatica T
**PDF sorgente**: `Demoni_di_sistema_17_aprile.pdf` · `Autorizzazione_17_aprile.pdf` · `approfondimento_PAM_-_il_framework_di_autenticazione_e_autorizzazione_.pdf` (Prandini, DISI)
**Natura del modulo**: teorico-concettuale, ma con forti ancoraggi a comandi/file di configurazione. Nessuna tipologia d'esame pratica dedicata, ma **feed diretto della tipologia Integrity/privesc (S11)** e materiale caldo per il **quiz teorico** (copre tutti e 15 i moduli).

---

## 0. Il filo conduttore: perché questi tre argomenti stanno insieme

Il modulo risponde a un'unica domanda operativa: **quando un utente ha già i piedi dentro il sistema (accesso legittimo con privilegi limitati), che cosa decide se e come può fare qualcosa in più?**

Tre livelli di risposta, ciascuno un PDF:

1. **Autorizzazione** (il modello): *chi può fare cosa su quale risorsa*. Definisce le regole astratte (DAC/MAC/RBAC) e la loro implementazione concreta su Unix (i 12 bit di permesso, SUID/SGID, capabilities, ACL) e Windows (NTFS, gruppi, composizione allow/deny).
2. **Demoni di sistema** (gli attori privilegiati): i processi che girano con privilegi di amministrazione e i loro file di configurazione. Sono il **bersaglio** della privilege escalation: se i file che un demone privilegiato legge hanno permessi sbagliati, un utente non privilegiato inietta codice e aspetta che il sistema lo esegua con privilegi elevati.
3. **PAM** (il framework): l'infrastruttura software attraverso cui i programmi (molti dei quali sono demoni: `sshd`, `login`, `cron`) implementano concretamente **autenticazione e autorizzazione di accesso**, in modo modulare e configurabile per-programma.

Il collegamento preciso: l'**autorizzazione** è il *modello* (le regole), i **demoni** sono i *processi* che agiscono con l'autorità concessa da quelle regole, **PAM** è il *framework* con cui i demoni verificano l'identità (autenticazione) e i diritti d'accesso (account management) prima di concedere una sessione. Un errore in uno qualsiasi dei tre livelli è un vettore di privilege escalation.

---

## PARTE A — AUTORIZZAZIONE: modelli e implementazioni

### A.1 Il processo di controllo dell'accesso e la distinzione fondamentale

Un soggetto **autenticato** deve essere **autorizzato** a svolgere operazioni sulle risorse. Questa frase, nella sua banalità apparente, contiene la distinzione più importante del modulo (e quella che il profilo di Lorenzo tende a confondere):

- **Autenticazione** = *provare chi sei*. Rispondere alla domanda "sei davvero l'utente X?" (password, chiave, biometria). È il tema di S2.
- **Autorizzazione** = *decidere cosa ti è permesso fare*, dato che ora sappiamo chi sei. Rispondere a "l'utente X può leggere questo file / eseguire questo programma / aprire questa socket?".

L'autenticazione viene **prima** e produce un'identità certa; l'autorizzazione viene **dopo** e usa quell'identità per prendere decisioni. Sono due meccanismi indipendenti: si può essere autenticati perfettamente e non autorizzati a nulla (account `locked` che può solo far girare processi), oppure — nel caso dei bit SUID che vedremo — si può eseguire codice con un'autorità che non corrisponde all'identità con cui ci si è autenticati.

**Meccanismo**: l'autorizzazione si costruisce in tre passaggi, ed è cruciale (principio ripetuto per tutto il corso) **separare politiche e meccanismi**:
1. **modellare** il sistema controllato (solo i fattori critici per il controllo d'accesso);
2. **definire la politica** (le regole con cui l'accesso è regolamentato);
3. **attuare la politica** tramite meccanismi HW/SW.

**Visione**: separare *cosa* si vuole ottenere (politica) da *come* lo si realizza (meccanismo) permette di confrontare politiche diverse senza annegare nei dettagli implementativi, di identificare il set minimo di requisiti, e di progettare meccanismi riusabili come mattoni per politiche diverse. È lo stesso principio di separazione che in S5 distingue "che traffico voglio far passare" (policy) da "quale regola iptables scrivo" (meccanismo).

### A.2 Caratteristiche di una buona politica e di un buon meccanismo

Una **politica** ben progettata rispetta:
- **Privilegio minimo**: ogni accesso concede l'insieme di autorizzazioni più ristretto possibile. È il principio-cardine che ritorna ovunque (account `locked`, capabilities al posto di root pieno, sudo puntuale).
- **Consistenza**: deve esistere uno schema di risoluzione **non ambiguo** quando più autorizzazioni diverse potrebbero applicarsi alla stessa richiesta. Non c'è una soluzione unica: si sceglie tra "regola più/meno specifica vince", "default allow vs default deny", "vince la prima/ultima regola in ordine spaziale o temporale", gerarchia degli autori delle regole. (Nota il parallelo con S5: iptables valuta le regole *in ordine*, prima regola che fa match vince; Windows NTFS invece usa deny-esplicito-prevale, come vedremo.)
- **Completezza e correttezza**: ogni richiesta riceve risposta entro un tempo predeterminato, e deve esistere una **regola predefinita** da applicare quando non si trova un'autorizzazione esplicita (il default-deny/default-allow).

Un buon **meccanismo** deve essere:
- **Resistente alle manomissioni** (non lo si deve poter sabotare senza che nessuno se ne accorga);
- **Mediazione completa**: *ogni* accesso alle risorse passa dal controllo del meccanismo — nessuna scorciatoia (esattamente il parallelo con la topologia firewall di S5: se esiste una strada che aggira il punto di controllo, la policy non serve a nulla);
- **Piccolo e autonomo** (facile da testare e riparare);
- **Ragionevolmente economico** (il costo non deve superare il danno degli accessi non autorizzati).

### A.3 Parametri di decisione

La decisione di autorizzazione può basarsi su: **identità** del soggetto; **ruolo** (decisione presa in base al ruolo attuale, indipendentemente dall'identità → base concettuale di RBAC); **modalità di accesso** (che tipo di operazione — read/write/execute); **vincoli spaziali e temporali** (da dove e quando arriva la richiesta → in PAM lo fanno `pam_time` e `pam_access`); **storia delle attività** (limiti sulla quantità/tipo di uso).

### A.4 I tre modelli fondamentali: DAC, MAC, RBAC

Questa è una classificazione da sapere a memoria per il quiz.

- **DAC — Discretionary Access Control**: ogni oggetto ha un **proprietario**, e **il proprietario decide i permessi** a sua discrezione. È il modello di Unix e Windows "classico". "Discrezionale" = la decisione è lasciata alla discrezione del proprietario, non imposta dall'alto.
- **MAC — Mandatory Access Control**: la proprietà di un oggetto **non** consente di modificarne i permessi. Esiste una **policy centralizzata** decisa da un *security manager*; i soggetti non possono cambiarne alcun dettaglio. "Mandatory" = obbligatorio, imposto dall'autorità centrale. Esempi: SELinux, AppArmor, i modelli militari Bell-LaPadula/Biba.
- **RBAC — Role-Based Access Control**: i permessi sono assegnati **ai ruoli**, non agli utenti; l'utente eredita i permessi del ruolo che ricopre, e il ruolo può cambiare dinamicamente (nel tempo, secondo il contesto).

**Perché esistono modelli diversi**: DAC è flessibile e comprensibile anche ai non tecnici (ognuno gestisce le proprie risorse) ma è fragile — un utente può concedere per errore accesso a tutti. MAC è rigido ma garantisce proprietà di sicurezza globali (riservatezza/integrità) che DAC non può garantire. RBAC è un compromesso gestionale: in un'organizzazione grande, gestire i permessi per ruolo invece che per singolo utente riduce drasticamente il lavoro amministrativo.

### A.5 Meccanismi: la matrice degli accessi, ACL e capability list

Concettualmente, il controllo d'accesso è una **matrice** soggetti × oggetti, dove ogni cella dice cosa quel soggetto può fare su quell'oggetto. Il problema pratico: migliaia di soggetti, milioni di oggetti — la matrice completa è enorme e per lo più fatta di valori di default. Si partiziona in due modi opposti:

- **Capability list**: si partiziona **per soggetto**. A ogni soggetto è associata la lista degli oggetti su cui ha permessi ≠ default. "Cosa può fare questo utente?" è immediato; "chi può toccare questo oggetto?" è costoso.
- **Access Control List (ACL)**: si partiziona **per oggetto**. A ogni oggetto è associata la lista dei soggetti con permessi ≠ default. "Chi può toccare questo file?" è immediato. È il modello di POSIX e Windows.

> ⚠️ **Trappola terminologica** (importante per il quiz): le *capability list* di questa slide (partizione della matrice per soggetto) **NON** sono le *Linux capabilities* di A.9 (i 41 poteri granulari di root). Stesso nome, due concetti diversi. Il PDF lo segnala esplicitamente.

Il **filesystem Unix tradizionale** usa una ACL "rigida" memorizzata nell'inode, che elenca **sempre e solo tre soggetti**: l'utente proprietario (U), il gruppo proprietario (G), e il gruppo implicito di "tutti gli altri" (O, chi non è U e non appartiene a G). POSIX ACL (A.8) rimuove questa rigidità.

### A.6 DAC su Unix: utenti, gruppi, e i 12 bit di permesso

**Utenti e gruppi**: si creano con `adduser`/`addgroup`. Ogni utente **deve** appartenere ad almeno un gruppo; il sistema di norma ne crea uno omonimo contenente solo lui. Un utente può appartenere a più gruppi. Un account può essere **`locked`**: non usabile per login interattivo, ma i processi possono ancora girare con quell'identità (è il minimo privilegio applicato agli account di servizio). Il comando `passwd` cambia le password (le proprie; root le cambia a chiunque) e con `-l`/`-u` blocca/sblocca un account (solo root).

**I 12 bit di permesso** nell'inode: 9 bit "standard" (rwx per U, G, O) + 3 bit "speciali" (SUID, SGID, sticky). Ogni file (regolare, directory, link, socket, block/char special) è descritto da un inode che contiene esattamente un utente proprietario, esattamente un gruppo proprietario, e questi 12 bit.

**Significato dei bit standard**, leggermente diverso tra file e directory (ricordando che *una directory è un file il cui contenuto è un database di coppie (nome, inode)*):
- **R (read)**: leggere il contenuto di un file / elencare i file di una directory.
- **W (write)**: scrivere dentro un file / aggiungere, cancellare, rinominare file in una directory.
  - ⚠️ **Nota controintuitiva ma esaminabile**: il permesso W su una **directory** consente di **cancellare** un file di cui non si ha alcun diritto sul contenuto — perché cancellare significa rimuovere la coppia (nome, inode) dal database-directory, operazione di scrittura *sulla directory*, non sul file.
- **X (execute)**: eseguire un file come programma / fare il **lookup** dell'inode di una directory (cioè "attraversarla").
  - ⚠️ **Nota esaminabile**: accedere a un file per path richiede il permesso **X su ogni directory** del percorso (serve il lookup di ogni inode intermedio), mentre **R non è necessario** sulle directory intermedie. R su una directory serve solo a *elencarne* il contenuto, non ad attraversarla.

**Composizione dei permessi** (algoritmo deterministico, esaminabile): quando l'utente A opera su un file, il SO controlla nell'ordine:
1. `A == U?` → sì: applica i permessi di **U** (e **si ferma qui**);
2. altrimenti `A appartiene a G?` → sì: applica i permessi di **G**;
3. altrimenti: applica i permessi di **O**.
- ⚠️ **Conseguenza controintuitiva**: la valutazione si ferma alla prima categoria che fa match. Se A è il proprietario (`A == U`), si applicano i permessi di U **anche se quelli di G sarebbero più favorevoli** — quelli di G vengono ignorati. Non è "il più permissivo vince": è "la prima categoria applicabile vince".

### A.7 Permessi predefiniti, umask, e bit speciali

**Ownership alla creazione**: l'utente creatore diventa proprietario; il *gruppo attivo* del creatore diventa gruppo proprietario (default = gruppo predefinito da `/etc/passwd`; si cambia a mano con `newgrp`, o automaticamente nelle directory con SGID).

**umask**: i permessi alla creazione sono "tutti quelli sensati" **meno** la umask.
- "Tutti quelli sensati" = `666` (rw-rw-rw-) per i file (l'eseguibilità è un'eccezione, non si concede di default) e `777` per le directory (entrarci è la norma).
- La umask è una **maschera che toglie** i permessi da non concedere. Poiché in Linux il gruppo di default contiene solo l'utente stesso, una umask sensata è `006` (toglie a "other" lettura e scrittura, lascia il gruppo — utile per collaborare mantenendo i file privati verso l'esterno).
- Si interroga/imposta con `umask`; per renderla persistente si usano i file di configurazione della shell.

**Bit speciali sui file** (i 3 bit più significativi della dozzina):
- **BIT 11 — SUID (Set User ID)**: se settato su un eseguibile, al lancio il processo esegue con l'**identità dell'utente proprietario del file**, non di chi lo lancia. È il meccanismo con cui un utente standard esegue codice privilegiato in modo controllato.
- **BIT 10 — SGID (Set Group ID)**: come SUID ma sull'identità di **gruppo** (il processo prende il gruppo proprietario del file).
- **BIT 9 — STICKY (sui file)**: **obsoleto**, suggeriva al SO di tenere in cache una copia del programma.

**Bit speciali sulle directory** (semantica diversa):
- **BIT 11 su directory**: non usato.
- **BIT 10 — SGID su directory**: se un utente appartiene al gruppo proprietario e il bit SGID è settato, l'utente assume quel gruppo come attivo e **i file creati nella directory ereditano quel gruppo**. Con `umask 006`, nelle aree collaborative i file diventano automaticamente leggibili/scrivibili da tutto il gruppo, mentre nelle aree personali restano privati (gruppo principale = solo l'utente).
- **BIT 9 — Sticky su directory (Temp bit)**: nelle directory world-writable (es. `/tmp`), impone che un file sia **cancellabile solo dal suo proprietario**. Risolve il problema "chiunque può scrivere → chiunque può cancellare i file altrui".

⚠️ **Da non confondere**: lo sticky bit ha significato *diverso* su file (obsoleto, cache) e su directory (protezione delle temp). Sui sistemi moderni conta solo il secondo.

### A.8 Attributi estesi e POSIX ACL

**Attributi** (fuori dai 12 bit, gestiti da `chattr` per modificare e `lsattr` per visualizzare): primariamente per fs tuning, ma alcuni sono rilevanti per la sicurezza:
- **append only (`a`)**: si può solo aggiungere in coda → **impedisce il "taglio" dei logfile** (un attaccante non può azzerare i log per cancellare le sue tracce). Contromisura difensiva citata anche in ambito NIDS/HIDS.
- **immutable (`i`)**: vieta cancellazione, creazione di link, rinomina e scrittura → utile per blindare i file di sistema critici.
- **secure deletion (`s`)**: sovrascrive con zeri i blocchi dei file cancellati (protezione limitata, valida solo contro strumenti "in linea").

**POSIX ACL**: estendono la ACL rigida a tre soggetti dell'inode, permettendo di specificare una **lista arbitraria** di utenti e gruppi con i loro permessi, oltre agli owner. Introducono la **mask** che limita simultaneamente tutti i permessi (l'effettivo è l'AND tra permesso concesso e mask). Strumenti: `setfacl` per impostare, `getfacl` per visualizzare; `ls -l` mostra un `+` dopo i permessi quando esiste una ACL estesa. Esempio dal PDF:
```
user::rw-
user:lisa:rw-       #effective:r--   (limitato dalla mask)
group::r--
group:toolies:rw-   #effective:r--
mask::r--
other::r--
```

### A.9 Il super-utente e le Linux capabilities

Esiste tipicamente un utente con privilegi illimitati che **scavalca** i meccanismi di controllo d'accesso: `root` (Unix), `administrator` (Windows). L'account va difeso da ingressi abusivi *e* va minimizzata la probabilità di errori: usare un account non privilegiato per il 99% del tempo, disabilitare l'accesso diretto da GUI/console, ottenere i privilegi solo puntualmente (`sudo` in Linux; "esegui come amministratore" in Windows).

**Linux capabilities** (da NON confondere con le capability list di A.5): i poteri di root non sono monolitici. Esistono **41 capability distinte** (al kernel 5.9), ciascuna un'autorizzazione normalmente negata agli utenti standard, che coprono controllo di risorse, processi, accesso alla rete. La più citata per la sicurezza è **`CAP_DAC_OVERRIDE`**: la capacità di **ignorare i permessi sul filesystem**. Si possono assegnare capability specifiche a processi lanciati da utenti standard → azioni privilegiate senza dare accesso a root pieno = **principio di minimo privilegio** implementato in concreto. Strumenti: `man capabilities`, `getcap`, `setcap`.

> 🔴 **Ponte diretto con S11 (privesc)**: negli esercizi di privilege escalation che Lorenzo ha già fatto, `cap_dac_override` su `tee` (esercizio 11/01/2024, `change4`) è **esattamente questa capability**: un binario con `cap_dac_override` può scrivere `/etc/passwd` o `/etc/shadow` ignorando i permessi → aggiunta di un utente root. La lezione S9 è la *teoria* di ciò che in S11 si sfrutta in pratica.

### A.10 DAC su Microsoft: domini, gruppi, NTFS, GPO, composizione allow/deny

Il PDF dedica ampio spazio al modello Windows. Punti da conoscere:

**Domini**: nell'uso comune i sistemi Microsoft sono raggruppati in un **dominio** — insieme di computer che condividono un *directory database* comune (Active Directory), dove sono memorizzati computer, risorse condivise, utenti, gruppi.

**Utenti**: **Local user accounts** (ristretti alla macchina) vs **Domain user accounts** (profilo in AD, possono accedere a risorse non locali nei limiti dei privilegi, nel proprio dominio e nei domini *trusted*).

**Gruppi** — due dimensioni ortogonali:
- **Tipo**: *Distribution Group* (solo liste per applicazioni, il SO non li usa, non appesantiscono il logon ticket) vs *Security Group* (come i DG ma possono essere soggetti nelle regole di accesso alle risorse).
- **Scope**: *Machine Local*, *Domain Local (DLG)*, *Global (GG)*, *Universal (UG)*. Ogni scope definisce quali oggetti può contenere, di cosa può essere membro, e su quali risorse gli si possono assegnare permessi. La strategia consigliata (mnemonica **A-G-DL-P** implicita): mettere utenti simili in un **GG**, rendere i GG membri di **DLG**, assegnare i permessi ai **DLG** (con gli UG come livello extra di nesting per organizzazioni grandi).

**NTFS e ACL**: le autorizzazioni sono ACL (lista di soggetti + permessi per ogni risorsa), disponibili su partizioni **NTFS (non FAT)** e sulle condivisioni di rete. Per modificare una ACL serve l'ownership o il permesso `Full Control`/`Change Permissions`. **Ownership**: l'owner ha Full Control; Administrator può *sempre* prendere l'ownership; chi crea un file ne detiene l'ownership.

**SACL e auditing**: oltre alla ACL "normale" (DACL, che autorizza/nega), ogni risorsa ha una **SACL** (System ACL) usata per l'**auditing** — registra gli esiti (successo e/o fallimento) dei tentativi di accesso. La ACL *decide*, la SACL *traccia*.

**Autorizzazioni standard vs speciali**: sistema a tre strati per conciliare precisione e facilità d'uso. A basso livello ci sono molte **autorizzazioni speciali** con logica a **tre valori (allow, deny, not set)**; queste sono aggregate in poche **autorizzazioni standard** (R, W, RX, L, M, F); le standard si possono vedere a due valori (allow/not set) o esplicitando i tre.

**Composizione dei permessi in Windows** (esaminabile — logica *diversa* da Unix):
- Windows segue **default deny**: ciò che non è esplicitamente consentito è proibito.
- Un utente può appartenere a molti gruppi; il permesso complessivo è la **somma bit-a-bit** dei permessi ottenuti da tutti i gruppi di appartenenza (a differenza di Unix, dove *una sola* categoria vince).
- **not set** (né allow né deny) == **deny "debole"/scavalcabile**: consente che un allow ottenuto da un altro gruppo abbia effetto.
- **deny esplicito** == **deny "forte"/non scavalcabile**: prevale *sempre* su qualunque allow ottenuto da altri gruppi.
- Questo spiega perché servono *due* modi di negare: "not set" lascia aperta la porta ad altri gruppi, "deny esplicito" la chiude definitivamente.

**Condivisioni**: le ACL di *share* si compongono come quelle NTFS, ma si applicano **in serie** — l'autorizzazione effettiva su una risorsa condivisa è **la più restrittiva** tra permesso di share e permesso NTFS locale. **Copy/Move**: un file *copiato* eredita i permessi della directory di destinazione; *spostato* nella stessa partizione conserva i suoi permessi; ma un MOVE tra **partizioni diverse** = COPY (+delete), quindi eredita i permessi della destinazione.

**Group Policy (GPO)**: framework per assegnare privilegi/restrizioni non legati a risorse fisiche ovvie (es. bloccare le porte USB, configurare il desktop). Le regole stanno in un *Group Policy Object* collegabile a una OU, un Site o un Domain; ogni GPO ha una sezione *user settings* e una *computer settings*.

### A.11 Cenni a MAC: Bell-LaPadula e Biba

Nel MAC le regole sono dettate da un'autorità centrale; a ogni soggetto/risorsa è assegnata una **classe di accesso**: un **livello di sicurezza** in un insieme *ordinato* (es. TopSecret ► Segreto ► Riservato ► Non classificato) + una **categoria/compartment** in un insieme *non ordinato* (es. {armi, piani di battaglia, ...}).
- Le risorse sono etichettate con un livello (*classification/sensitivity*); i soggetti con un livello (*clearance*, la loro affidabilità).
- Relazione di **dominanza**: L1 = ⟨S1,C1⟩ domina L2 = ⟨S2,C2⟩ ⇔ S1 ≥ S2 **e** C1 ⊇ C2.

I due modelli usano la dominanza per proprietà opposte:
- **Bell-LaPadula (riservatezza)**: **NO-READ-UP** (non leggere sopra la tua clearance) + **NO-WRITE-DOWN** (non scrivere sotto, per non far trapelare segreti verso il basso). Mnemonica: "no read up, no write down" → protegge la *confidenzialità*.
- **Biba (integrità)**: **NO-READ-DOWN** (non leggere sotto, per non contaminarti con dati meno affidabili) + **NO-WRITE-UP** (non scrivere sopra, per non corrompere risorse più affidabili). Mnemonica: speculare a BLP → protegge l'*integrità*.

⚠️ **Trappola esaminabile**: BLP e Biba hanno regole *speculari*. Confonderle è l'errore classico. Ancora: BLP protegge la **riservatezza** (segreti che non devono scendere), Biba l'**integrità** (spazzatura che non deve salire). Applicandoli insieme (due classi per soggetto/risorsa) si proteggono entrambe.

### A.12 Cenni a RBAC

Le autorizzazioni sono concesse ai **ruoli**, non agli utenti; il ruolo può cambiare dinamicamente. È **"policy neutral"**: esprime tutti i principi fondamentali (minimo privilegio, separazione delle responsabilità, astrazione). Vantaggio: le autorizzazioni cambiano poco se ben modellate; il lavoro dell'amministratore diventa essenzialmente **assegnare il ruolo giusto** ai soggetti. Esiste uno standard (ANSI/INCITS 359-2004) con livelli di funzionalità incrementali.

---

## PARTE B — DEMONI DI SISTEMA: i processi privilegiati come bersaglio

### B.0 Il threat model del PDF: "bombe logiche"

Il PDF "Demoni di sistema" è dichiaratamente scritto dal **punto di vista dell'attaccante già dentro**: l'accesso come utente legittimo dà privilegi limitati, e la privilege escalation sfrutta **vulnerabilità locali**. Il vettore centrale è la **bomba logica**: molti processi girano con privilegi di amministrazione; se i **file** che questi processi usano hanno **permessi errati**, un utente non privilegiato può iniettarci il proprio codice e **attendere che il sistema lo esegua** con privilegi elevati — in un momento predeterminato, all'avvio/arresto di un sottosistema, o al verificarsi di un evento.

Da qui la mappa di questa parte: **quali sono i sistemi che eseguono codice per conto del sistema, e dove sono i loro file di configurazione** (che diventano il bersaglio da controllare).

### B.1 Esecuzione periodica — cron

**`crond`** è un demone che ogni minuto esamina una serie di file di configurazione (**crontab**) e determina quali compiti eseguire. I crontab sono di due insiemi:
- **Per utente**: `/var/spool/cron/crontabs/<utente>`, gestiti con `crontab -l` (visualizza), `crontab -e` (edita), `crontab <file>` (sostituisce).
- **System-wide**: `/etc/crontab`, che di solito richiama tutto ciò che trova in `/etc/cron.hourly/`, `/etc/cron.daily/`, `/etc/cron.weekly/`, `/etc/cron.monthly/`. Questi file di sistema hanno **un campo in più** rispetto a quelli personali: **il nome dell'utente** per conto del quale eseguire il task.

**Sintassi di una direttiva crontab**:
```
MINUTO  ORA  G.MESE  MESE  G.SETTIMANA   <comando>
```
- L'azione parte quando l'ora corrente corrisponde a **tutti** i selettori della riga (campi in **AND logico**).
- **ECCEZIONE esaminabile**: se sono specificati (≠ `*`) **entrambi** i giorni (settimana E mese), i due campi sono in **OR logico**. Es. `30 4 1,15 * 6 /bin/backup` → il backup gira il giorno 1 **+** il 15 **+** ogni sabato, alle 4:30.

> 🔴 **Ponte con S11/S7**: cron è un vettore di persistenza/privesc da manuale. Se un utente non privilegiato può scrivere uno script eseguito da un cron di root (perché lo script è world-writable, o la directory `/etc/cron.*` ha permessi laschi), inietta codice che root eseguirà. È il pattern "bomba logica" più diretto.

### B.2 Esecuzione posticipata — at

**`atd`** gestisce code di compiti da svolgere in momenti prefissati. Interfaccia a 4 comandi:
- `at [-V] [-q queue] [-f file] [-mldbv] TIME` — pianifica un comando al tempo TIME;
- `atq` — elenca i comandi in coda;
- `atrm job [job...]` — rimuove comandi dalla coda;
- `batch [-V] [-q queue] [-f file] [-mv] [TIME]` — esecuzione **condizionata al carico** del sistema.

Se non si specifica un file comandi, `at`/`batch` leggono da **standard input**. La specifica dell'ora è flessibile (`/usr/share/doc/at/timespec` per la definizione completa). Esempi:
```
echo 'wall "sveglia"' | at 08:00
echo "$HOME/bin/pulisci" | at now + 2 weeks
echo "$HOME/bin/auguri" | at midnight 31.12.2021
```

### B.3 Event manager / sistemi IPC — dbus e udev

- **D-Bus**: architettura di **Inter-Process Communication**, nata per uniformare la comunicazione tra elementi delle interfacce desktop. Configurazione in `/etc/dbus-1/`; in `/etc/dbus-1/event.d` stanno gli script di avvio dei sottosistemi gestiti.
- **udev**: ha rimpiazzato *devfs* come event manager per la **creazione istantanea dei device special file** quando si connette un nuovo dispositivo; oggi è parte di systemd. Le regole *evento → azione* stanno in `/etc/udev/rules.d` (es. `70-persistent-net.rules`, che alla comparsa nel subsystem `net` di una scheda con un certo MAC le assegna un nome fisso). Una regola udev associa un evento (connessione di un dispositivo) a un'azione (esecuzione di un comando) → altro potenziale vettore se scrivibile.

### B.4 Inizializzazione e demoni: init e i runlevel

**`init`** è il **primo processo avviato dal kernel** (PID 1). Gestisce i **runlevel** (stati di funzionamento definiti dal sottoinsieme di servizi attivi), orchestra la sequenza per raggiungere un runlevel, intercetta eventi (ctrl-alt-canc, terminazioni anomale), e spegne il sistema in modo ordinato. Tre varianti storiche da conoscere per l'attuale mix di distribuzioni:
- **SystemV-style** (storico);
- **Upstart** (Canonical, 2006–2014);
- **systemd** (ispirazione RedHat, 2010–oggi).

### B.5 sysvinit

`/sbin/init` originale di SystemV Unix, configurato da **`/etc/inittab`**:
- Specifica il **default runlevel** (`id:2:initdefault:`).
- Se al kernel si passa la keyword `single` dal boot loader, il settaggio è scavalcato e il sistema parte in **single user mode** (runlevel 1) — nota di sicurezza: chi ha accesso fisico al boot loader può ottenere una shell di root.
- init avvia i **virtual terminal** e i gestori delle console seriali (`getty`) — arcaico ma tornato attuale con l'IoT.

**Processi avviati da sysvinit** — due righe-tipo di `/etc/inittab`:
- `l0:0:wait:/etc/init.d/rc 0` — pilota l'avvio SystemV-style: `wait` = esecuzione **sequenziale**; per il runlevel N, `rc` esegue ogni script che inizia per **`S`** in `/etc/rcN.d/` con parametro `start`, e ogni script che inizia per **`K`** con `stop`. Gli script veri stanno in `/etc/init.d/`, *symlinked* dalle 7 directory `/etc/rcN.d/` (per non duplicarli).
- `x:5:respawn:/usr/X11/bin/gdm` — avvia il programma indicato e con **`respawn`** init lo **riavvia** se termina.

### B.6 systemd — unit, tipi, e posizioni

systemd sostituisce runlevel e script init con le **unit**, la cui denominazione segue `nome.tipo`. **Tipi di unit** da conoscere:
- **Service**: controllo e monitoraggio dei **demoni** (il tipo più comune).
- **Socket**: attivazione di canali IPC (file/net/Unix socket) — permette l'avvio *on-demand* di un servizio alla prima connessione.
- **Target**: gruppo di unit che **rimpiazza il concetto di runlevel**.
- **Device**: punti di accesso ai dispositivi, creati dal kernel.
- **Mount/Automount/Swap**: filesystem-related.
- **Snapshot**: stato salvato del sistema.
- **Timer**: attività legate al tempo (→ rimpiazza cron/at).
- **Path**: monitoraggio del contenuto di una directory via `inotify`.
- **Slice**: gestione risorse via **cgroup**.
- **Scope**: raggruppamento di processi.

**Dove stanno le definizioni** (ordine di priorità crescente):
- `/lib/systemd/system/` — "libreria" di riferimento;
- `/usr/lib/systemd/system/` — file dei manutentori dei pacchetti (quasi sempre link ai riferimenti);
- `/etc/systemd/system/` — **personalizzazioni locali, prioritarie** su tutte le precedenti.

⚠️ **Nota di sicurezza esaminabile**: poiché `/etc/systemd/system/` ha priorità, chi può scriverci può *ridefinire* una unit di sistema (override) e far eseguire codice arbitrario con i privilegi del servizio — è un vettore di privesc/persistenza se i permessi sono errati.

### B.7 systemd — gestione dei servizi

**A run-time (volatile)**:
```
systemctl {start|stop|status|restart|reload} <servicename>
```
- `status` dà output molto descrittivo: stato corrente + passi fatti, process tree, righe di log rilevanti. Con `-H [hostname]` si connette a un host remoto via SSH.
- Nelle unit i comandi effettivi sono definiti da `ExecStart`, `ExecReload`, `ExecStop`; `restart` = `stop` seguito da `start`; systemd traccia i PID dei processi avviati; `stop` di default manda **SIGTERM** e poi **SIGKILL** dopo un timeout (varianti in `man 5 systemd.kill`).
- Questi comandi sono **volatili**: hanno effetto immediato ma non cambiano la configurazione.

**A boot/shutdown (persistente)**:
```
systemctl {enable|disable|mask|unmask} <servicename>
```
- `enable`/`disable` decidono l'avvio automatico al boot; `disable` lascia comunque possibile lo `start` manuale.
- `mask` **neutralizza l'intera definizione** della unit, impedendo anche il controllo manuale (la "spegne" del tutto).
- Questi comandi **non** hanno effetto immediato, ma l'effetto sulla configurazione è **persistente**.

⚠️ **Coppia esaminabile da tenere distinta**: `start/stop` = azione *ora*, volatile; `enable/disable` = comportamento *al boot*, persistente. Fare `start` non abilita al boot; fare `enable` non avvia subito.

---

## PARTE C — PAM: il framework di autenticazione e autorizzazione

### C.1 Cos'è PAM e perché esiste

**PAM = Pluggable Authentication Modules**. Il problema che risolve: senza PAM, ogni programma che deve autenticare un utente (`login`, `sshd`, `su`, `sudo`, `passwd`, `cron`) dovrebbe implementare da sé la logica di controllo delle credenziali — con codice duplicato, incoerente e difficile da aggiornare (cambiare il meccanismo di autenticazione richiederebbe di ricompilare ogni programma).

PAM astrae questa logica in un **framework a moduli caricabili**: il programma delega a PAM le funzioni di sicurezza, e l'amministratore decide *tramite configurazione* (senza toccare il programma) come queste funzioni sono implementate. È l'applicazione del principio "separa politiche e meccanismi" (A.1) all'autenticazione.

Oltre alla pura autenticazione, PAM fornisce: **gestione dei diritti di account** (tempo, posizione...), **gestione delle password**, **housekeeping delle sessioni** utente, lo **stacking** di moduli che fanno controlli diversi, e la **configurazione individuale per ogni programma**.

**Come si rende un programma PAM-aware** (livello meccanismo): si include il prototipo `<security/pam_appl.h>` nel sorgente e si linka l'eseguibile alle **librerie PAM** (`libpam`, `libpam_misc`), che forniscono i meccanismi di chiamata alle funzioni di sicurezza astratte. Si verifica se un programma usa PAM con **`ldd`** (che elenca le librerie dinamiche linkate). Ogni modulo PAM è installato in **`/lib/security`**.

### C.2 Configurazione: dove e in che formato

Due modalità:
- **File unico `/etc/pam.conf`**: ogni riga ha il formato `program module-type control-flag module-path arguments` (il campo `program` in più, perché il file è condiviso).
- **Un file per programma in `/etc/pam.d/`** (la modalità **più comune**): ogni file ha **lo stesso nome del programma** (es. `/etc/pam.d/sshd`, `/etc/pam.d/login`) e righe nel formato `module-type control-flag module-path arguments` (senza il campo `program`, implicito nel nome del file).

Esempio (formato `/etc/pam.d/`):
```
auth     sufficient  /lib/security/pam_ldap.so
account  sufficient  /lib/security/pam_ldap.so
password sufficient  /lib/security/pam_ldap.so
session  optional    /lib/security/pam_ldap.so
auth     requisite   pam_unix2.so
auth     required    pam_securetty.so
auth     required    pam_nologin.so
```

### C.3 I quattro module-type (la distinzione da NON confondere)

Il `module-type` definisce **quale servizio** si sta configurando. La maggior parte dei programmi ha almeno una riga per ciascun servizio. Sono **quattro fasi indipendenti** del ciclo di gestione di un accesso — e vanno tenute distinte con precisione:

| module-type | Cosa gestisce | Risponde alla domanda | Esempio concreto |
|---|---|---|---|
| **auth** | **Autenticazione**: verifica dell'identità | "sei chi dici di essere?" | lookup password da `passwd`/`shadow` |
| **account** | **Autorizzazione di account** (non legata all'autenticazione): l'account autenticato può accedere *ora, da qui*? | "hai il diritto di entrare in queste condizioni?" | restrizioni per gruppo, ora del giorno, path d'accesso; avvisi di scadenza password |
| **session** | Gestione della **sessione**: setup al login e cleanup al logout | "cosa va preparato/ripulito attorno alla sessione?" | montare home, impostare limiti, log |
| **password** | Aggiornamento dei **token di autenticazione** (le password) | "come si cambia la password?" | controlli di robustezza al cambio password |

⚠️ **Distinzione-cardine del modulo** (quasi certa al quiz): **`auth` è autenticazione** (*provi chi sei*), **`account` è autorizzazione** (*hai il diritto di accedere in queste condizioni, ora che sappiamo chi sei*). È **esattamente** la distinzione autenticazione/autorizzazione di A.1, resa operativa in due tipi di riga diversi nello stesso file PAM. Un utente può passare `auth` (password giusta) e fallire `account` (fuori dall'orario consentito, o `/etc/nologin` presente). Non confondere neppure `password` (cambio credenziali) con `auth` (verifica credenziali): sono momenti diversi.

### C.4 I control-flag: come PAM reagisce a successo/fallimento

Un file PAM è uno **stack** di moduli valutati in ordine; il `control-flag` decide come il risultato di ogni modulo influenza l'esito dell'intero stack.

| Control-flag | Se il modulo ha **successo** | Se il modulo **fallisce** |
|---|---|---|
| **requisite** | lo stack continua (esito dipende dagli altri) | lo stack **termina subito** e **fallisce** |
| **required** | lo stack continua (esito dipende dagli altri) | lo stack **continua**, ma **fallirà** comunque |
| **sufficient** | lo stack **termina subito con successo** (se nessun `required` precedente è fallito) | lo stack continua (esito dipende dagli altri) |
| **optional** | lo stack continua | lo stack continua; conta solo se è l'unico modulo determinante |

⚠️ **La distinzione più insidiosa: `required` vs `requisite`**. Entrambi *devono* passare perché lo stack abbia successo. La differenza è **quando** si ferma in caso di fallimento:
- **`requisite`** fallisce → **si ferma immediatamente** e ritorna. L'utente non prosegue oltre. Utile per non rivelare *dove* è fallito e per non eseguire i moduli successivi.
- **`required`** fallisce → lo stack è **già condannato** a fallire, ma **continua a eseguire** i moduli successivi (poi ritornerà fallimento). Utile perché non rivela all'attaccante *quale* controllo è fallito (il fallimento arriva alla fine, uguale in tutti i casi) e permette a moduli successivi (es. logging) di girare comunque.

E la coppia con **`sufficient`**: se un `sufficient` ha successo *e nessun `required` precedente è fallito*, lo stack **termina subito con successo**, saltando i moduli rimanenti. Ma un `required` fallito *prima* **sovrascrive** un `sufficient` successivo: la sua condanna resta.

### C.5 module-path e argomenti

Il **module-path** è il percorso assoluto della shared library (`.so`) che implementa le funzioni. Dopo il path si passano argomenti — molti specifici del modulo, alcuni standard supportati da quasi tutti:
- **`debug`**: genera info di debug (su stdout o via `syslogd`);
- **`no_warn`**: disabilita il logging dei fallimenti di autenticazione;
- **`use_first_pass`**: usa la password inserita per il modulo *precedente*, e **fallisce** se non funziona (non richiede di nuovo la password);
- **`try_first_pass`**: *tenta* di usare la password del modulo precedente; se fallisce, **chiede** all'utente di inserirla per questo modulo.

⚠️ `use_first_pass` vs `try_first_pass`: entrambi riusano la password precedente per non chiederla due volte; `use_` è rigido (fallisce e basta), `try_` è morbido (ripiega chiedendola).

### C.6 Moduli PAM comuni (il filename è `pam_<name>.so`)

Tabella dei più comuni, con i module-type che supportano — utile per il quiz perché lega ogni modulo al suo tipo e al suo file di configurazione:

| Modulo | auth | account | session | password | Funzione / file di config |
|---|:-:|:-:|:-:|:-:|---|
| **unix** | x | x | x | x | Autenticazione Unix tradizionale su `/etc/passwd` e `/etc/shadow` |
| **time** | x | | | | Restrizioni temporali d'accesso (`/etc/security/time.conf`) |
| **nologin** | x | x | | | Se esiste `/etc/nologin`, solo root può entrare; agli altri mostra il file |
| **env** | x | | | | Imposta variabili d'ambiente della sessione (`/etc/security/pam_env.conf`) |
| **deny** | x | x | x | x | Ritorna **sempre fallimento**; utile a fine stack per bloccare accessi da misconfigurazione |
| **limits** | | | x | | Limiti su memoria, CPU, ecc. (`/etc/security/limits.conf`) |
| **access** | | x | | | Coppie username/macchina ammesse o negate (`/etc/security/access.conf`) |
| **pwcheck** | | | | x | Controlli extra al cambio password (`/etc/login.defs`) |
| **cracklib** | | | | x | Rifiuta password troppo semplici o già usate |
| **tally** | x | x | | | Conta i tentativi d'accesso; **nega dopo N fallimenti** (anti-bruteforce) |
| **warn** | x | x | x | x | Registra informazioni su syslog |

Nota la coerenza: i moduli `password` (`pwcheck`, `cracklib`) agiscono sul *cambio* password; i moduli `account` (`access`) sull'*autorizzazione* d'accesso; i moduli `auth` (`unix`, `securetty`, `nologin`) sulla *verifica* dell'identità. Il **tipo** del modulo dice in *quale fase* interviene.

### C.7 Esempi di stack ragionati

**Esempio 1** — tre `required` in auth:
```
auth  required  /lib/security/pam_unix.so
auth  required  /lib/security/pam_securetty.so
auth  required  /lib/security/pam_nologin.so
```
L'autenticazione riesce solo se **tutti e tre** approvano. `pam_unix` fa user+password su `/etc/passwd`; `pam_securetty` fa **fallire un login di root** a meno che sia su un terminale elencato in `/etc/securetty`; `pam_nologin` fa **fallire tutti i login tranne root** se esiste `/etc/nologin`. **L'ordine e la combinazione contano**: con `/etc/nologin` presente, solo root può entrare — **ma solo da console sicura** (per via di `securetty`). Se il flag della prima riga fosse `sufficient` invece di `required`, root potrebbe entrare **da ovunque** e `/etc/nologin` non avrebbe effetto (il `sufficient` riuscito salterebbe i controlli successivi).

**Esempio 2** — interazione required/sufficient e importanza dell'ordine:
```
auth required   pam_unix.so try_first_pass
auth sufficient pam_krb5.so try_first_pass
auth required   pam_env.so
```
Questo stack riesce **se e solo se `pam_unix` riesce**: se fallisce, il suo status `required` sovrascrive il `sufficient` di `pam_krb5`; se riesce, il suo successo non è sovrascrivibile da un fallimento di `pam_krb5`. Se si **invertisse** l'ordine dei due moduli di autenticazione:
```
auth sufficient pam_krb5.so try_first_pass
auth required   pam_unix.so try_first_pass
auth required   pam_env.so
```
poiché il `sufficient pam_krb5` viene **prima**, il suo successo **bypassa** il `required pam_unix` successivo → lo stack riesce se **almeno uno** dei due riesce. In entrambi i casi, però, il successo di `pam_krb5` (sufficient) **salta `pam_env`** (che imposta variabili d'ambiente ma non ritorna mai fallimento) — effetto **indesiderabile**, perché le variabili non vengono impostate. Lezione: nello stacking, un `sufficient` che riesce può saltare moduli successivi *necessari ma non di autenticazione*.

### C.8 Configurazione default-deny: `/etc/pam.d/other`

Un default sicuro blocca qualunque programma che **non abbia una propria configurazione PAM specifica**. Si crea `/etc/pam.d/other` (il fallback per ogni servizio senza file dedicato) così:
```
auth     required  pam_warn.so
auth     required  pam_deny.so
account  required  pam_warn.so
account  required  pam_deny.so
password required  pam_warn.so
password required  pam_deny.so
session  required  pam_warn.so
session  required  pam_deny.so
```
Per ogni module-type: `pam_warn` **logga** il tentativo, `pam_deny` lo **nega sempre**. È l'applicazione a PAM del principio **default deny** visto in A.2 e in S5: ciò che non è esplicitamente autorizzato (con un file PAM dedicato) è rifiutato.

---

## PARTE D — THREAT MODEL INTEGRATO: attaccante e difensore

Questo modulo è, per struttura, il *ponte teorico* verso la tipologia d'esame **Integrity/privesc (S11)**. Ecco i vettori concreti che emergono dall'unione dei tre PDF.

### D.1 Vettori di privilege escalation (POV attaccante)

1. **Binari SUID/SGID vulnerabili o mal assegnati** (A.7): un binario SUID-root con un bug (o assegnato per errore) fa eseguire codice con identità root. È il vettore centrale di S11. *Come li trova l'attaccante*: `find / -type f -perm +6000` (cerca i bit SUID+SGID). Altre ricerche: `find / -perm +2` (world-writable) e `find / -nouser` (file di account cancellati).
2. **Capability pericolose** (A.9): un binario con `cap_dac_override` ignora i permessi del filesystem → può scrivere `/etc/passwd`/`/etc/shadow`. Corrisponde all'esercizio S11 `change4` (`tee` + `cap_dac_override`).
3. **Bombe logiche via demoni** (B.0–B.6): file scrivibili eseguiti da processi privilegiati —
   - script world-writable lanciati da un **cron** di root (B.1);
   - job **`at`** iniettati (B.2);
   - regole **udev**/**dbus** scrivibili (B.3);
   - script di init `/etc/init.d/`, `/etc/rc*.d/` (B.5) o **unit systemd** ridefinibili in `/etc/systemd/system/` per la priorità (B.6).
4. **PAM come backdoor/persistenza** (C.*): un attaccante che ha già root può **modificare uno stack PAM** per creare una backdoor difficile da notare — ad esempio inserendo un modulo `sufficient` che accetta una password universale, o rimuovendo `pam_deny`/`pam_securetty`. Poiché PAM è caricato da tutti i servizi di login (`sshd`, `login`, `su`), una riga aggiunta a `/etc/pam.d/` è un punto di persistenza potente e discreto. È il rovescio del "separa politiche e meccanismi": la stessa modularità che rende PAM flessibile lo rende un bersaglio di manomissione.

### D.2 Irrobustimento (POV difensore)

- **Minimo privilegio ovunque**: account `locked` per i servizi (A.6); `sudo` puntuale invece di root permanente (A.9); **capability** specifiche invece di root pieno (A.9); ruoli RBAC ben modellati (A.12).
- **Sorveglianza dei binari privilegiati** (A.7): auditare periodicamente i SUID/SGID con `find / -type f -perm +6000`, tenerli **pochi e vincolati**; nessun binario SUID che non serva.
- **Blindare i file critici**: attributo **immutable (`chattr +i`)** sui file di sistema, **append-only (`chattr +a`)** sui log per impedirne il taglio (A.8).
- **Permessi corretti su tutto ciò che un demone privilegiato legge/esegue**: crontab, script init, unit systemd, regole udev — nessuno di essi deve essere world-writable.
- **Default-deny in PAM** (`/etc/pam.d/other` con `pam_deny`, C.8); anti-bruteforce con `pam_tally` (C.6); limitare root a console sicure con `pam_securetty` e ai momenti giusti con `pam_time`.
- **Auditing**: SACL su Windows (A.10); log via `pam_warn`; integrity checking (HIDS/AIDE di S11) per accorgersi di modifiche non autorizzate a `/etc/passwd`, agli stack PAM, ai crontab.

---

## Connessioni SPECIFICHE con altri moduli

- **S2 (Autenticazione)**: S9 chiude il cerchio aperto da S2. S2 spiega *come* si autentica un utente (password, hash, `/etc/shadow`); PAM (C.3, `auth` + `pam_unix`) è **il framework concreto** con cui quei meccanismi di S2 vengono invocati dai programmi. La distinzione autenticazione/autorizzazione (A.1) è il punto di raccordo tra S2 (autenticazione) e S9 (autorizzazione).
- **S5 (Firewall/iptables)**: stesso schema concettuale di controllo d'accesso. La **mediazione completa** (A.2) è il principio per cui la topologia firewall di S5 deve costringere *tutto* il traffico a passare dal punto di controllo. Il **default deny** di A.2/C.8 è letteralmente la `policy drop` delle catene nft di S5. La composizione ordinata delle regole iptables (prima che fa match vince) è una delle "regole di consistenza" di A.2.
- **S11 (Integrity/privesc)** — connessione più forte: A.7 (SUID/SGID), A.9 (`cap_dac_override`) e B.0–B.6 (bombe logiche via cron/at/systemd) sono **la teoria** degli esercizi pratici già svolti da Lorenzo — `change1` (SUID su `cp`), `change4` (`cap_dac_override` su `tee`), `change5`. `find / -perm +6000` (A.7) è il primo comando di enumerazione in un esercizio privesc.
- **S7 (Backdoor injection)** e **S8 (Filtrare attacchi)**: cron/at/udev/PAM (B.1–B.3, D.1.4) sono i **meccanismi di persistenza** che una backdoor sfrutta per farsi rieseguire; l'append-only sui log (A.8) è la contromisura a chi vuole cancellare le tracce.
- **S1 (Enumerazione)**: `find` per SUID/world-writable/nouser (A.7) e `ldd` per verificare l'uso di PAM (C.1) sono strumenti di enumerazione locale, il gemello "post-accesso" dell'enumerazione di rete di S1.
- **S10 (NIDS)**: come in S5, il controllo d'accesso è *prevenzione*; il NIDS/HIDS è *rilevazione* di ciò che passa comunque. L'auditing (SACL, `pam_warn`, AIDE) è l'anello di rilevazione locale.

---

## Autoverifica — quiz in stile esame (vero/falso e scelta multipla)

*(Rispondi senza guardare; le risposte sono negli appunti `appunti_moduloS9_...`.)*

1. **V/F** — L'autenticazione decide *cosa* un soggetto può fare; l'autorizzazione decide *chi* è il soggetto.
2. **V/F** — In DAC il proprietario di un oggetto decide i permessi; in MAC no, perché la policy è centralizzata e imposta.
3. **V/F** — Le "capability list" (partizione della matrice per soggetto) sono la stessa cosa delle "Linux capabilities" come `CAP_DAC_OVERRIDE`.
4. **Scelta multipla** — Un utente A è proprietario del file `f` (categoria U: `r--`) e appartiene anche al gruppo proprietario (categoria G: `rw-`). Che permessi ottiene A su `f`?
   (a) `rw-` perché si sommano  (b) `r--` perché vince U e G è ignorato  (c) `rw-` perché vince il più permissivo  (d) nessun accesso.
5. **V/F** — Il permesso W su una directory permette di cancellare un file anche se non si ha alcun permesso sul contenuto di quel file.
6. **V/F** — Per attraversare le directory di un path e accedere a un file serve il permesso R su ciascuna directory intermedia.
7. **Scelta multipla** — Il bit **SUID** su un eseguibile fa sì che al lancio il processo giri con l'identità di:
   (a) chi lancia il programma  (b) l'utente proprietario del file  (c) root sempre  (d) il gruppo proprietario del file.
8. **V/F** — Lo sticky bit ha lo stesso significato su file e su directory.
9. **V/F** — In un crontab, se sono specificati (≠ `*`) sia il giorno del mese sia il giorno della settimana, i due campi sono in **AND** logico.
10. **Scelta multipla** — In systemd, quale comando **neutralizza** completamente una unit impedendo anche lo start manuale?
    (a) `disable`  (b) `stop`  (c) `mask`  (d) `unmask`.
11. **V/F** — `systemctl start` di un servizio lo abilita anche all'avvio automatico al boot.
12. **V/F** — In PAM, un modulo di tipo **`account`** verifica l'identità dell'utente (password), mentre **`auth`** verifica se l'account ha il diritto di accedere ora.
13. **Scelta multipla** — Differenza tra `required` e `requisite` quando il modulo **fallisce**:
    (a) nessuna  (b) `requisite` ferma subito lo stack, `required` continua ma lo stack fallirà comunque  (c) `required` ferma subito, `requisite` continua  (d) entrambi fanno riuscire lo stack.
14. **V/F** — Un modulo `sufficient` che ha successo (senza `required` precedenti falliti) fa terminare subito lo stack con successo, saltando i moduli rimanenti.
15. **V/F** — Bell-LaPadula (riservatezza) impone NO-READ-UP e NO-WRITE-DOWN; Biba (integrità) impone NO-READ-DOWN e NO-WRITE-UP.
16. **Scelta multipla** — In Windows, un utente ha `not set` su un permesso da un gruppo e `allow` dello stesso permesso da un altro gruppo. Il risultato è:
    (a) deny, perché not set == deny  (b) allow, perché not set è un deny "debole" scavalcabile  (c) errore  (d) dipende dall'ordine.
17. **V/F** — In Windows un `deny` esplicito prevale sempre su qualunque `allow` ottenuto da altri gruppi.
18. **Scelta multipla** — Quale comando cerca i file SUID/SGID sul sistema?
    (a) `find / -perm +2`  (b) `find / -type f -perm +6000`  (c) `find / -nouser`  (d) `getcap -r /`.
19. **V/F** — `/etc/pam.d/other` con `pam_deny` per ogni module-type implementa una politica di default-deny per i programmi privi di configurazione PAM specifica.
20. **V/F** — Un file *copiato* in una cartella NTFS eredita i permessi della cartella di destinazione; uno *spostato* tra partizioni diverse conserva i suoi permessi originali.

---

<!-- AUTO-LINKS:START -->
<!-- AUTO-LINKS:END -->
