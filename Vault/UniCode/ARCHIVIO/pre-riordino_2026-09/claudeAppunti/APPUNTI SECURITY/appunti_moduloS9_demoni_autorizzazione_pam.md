# Appunti — Modulo S9: Demoni di Sistema + Autorizzazione + PAM
**Corso**: Lab Sicurezza Informatica T
**Lezione di riferimento**: `lezione_moduloS9_demoni_autorizzazione_pam.md`
**PDF sorgente**: `Demoni_di_sistema_17_aprile.pdf` · `Autorizzazione_17_aprile.pdf` · `approfondimento_PAM_...pdf`
**Stato**: ⚠️ Modulo **mai** portato a lezione/appunti prima d'ora (esistevano solo i PDF ufficiali). Nessun appunto grezzo di Lorenzo — questi appunti simulano la sua rilettura critica in preparazione al **quiz teorico** dell'esame (17/07). Nessun lab pratico dedicato (S9 alimenta la tipologia Integrity/privesc di S11, quella la si esercita altrove).

---

## 1. Il cuore concettuale: autenticazione vs autorizzazione

Un soggetto **autenticato** deve essere **autorizzato** a operare sulle risorse. Sono due cose diverse, in sequenza: prima si prova chi sei, poi si decide cosa puoi fare.

> **Domanda** (la trappola numero uno del modulo): qual è *esattamente* la differenza tra autenticazione e autorizzazione? Continuo a scambiarle.
> **Risposta**: tienile ancorate a due domande diverse.
> - **Autenticazione** = *"sei davvero chi dici di essere?"* → verifica dell'**identità** (password, chiave SSH, biometria). È il tema di S2.
> - **Autorizzazione** = *"dato che ora so chi sei, cosa ti è permesso fare?"* → decisione sui **diritti** (leggere questo file, eseguire questo programma).
>
> L'ordine è fisso: **prima** autenticazione (produce un'identità certa), **poi** autorizzazione (usa quell'identità per decidere). Sono **indipendenti**: puoi essere autenticato benissimo e non autorizzato a nulla (account `locked`), oppure — col bit SUID — eseguire codice con un'autorità *diversa* dall'identità con cui ti sei autenticato. Il trucco mnemonico infallibile: **autentic-azione = identità; autoriz-zazione = permessi**. E il posto dove questa distinzione diventa *concreta* è PAM: il tipo di riga **`auth` = autenticazione**, il tipo **`account` = autorizzazione** (§7). Se ricordi questo, il resto del modulo si tiene insieme.

## 2. Politiche vs meccanismi, e le loro proprietà

Il controllo d'accesso si costruisce in 3 passi: modellare il sistema → definire la politica (le regole) → attuare la politica (i meccanismi HW/SW). Regola d'oro ripetuta in tutto il corso: **separare politiche e meccanismi**.

> **Domanda**: perché insistono così tanto su "separa politiche e meccanismi"? Mi sembra una frase fatta.
> **Risposta**: non è retorica, è la ragione per cui esiste PAM. La **politica** è *cosa* voglio (es. "root può entrare solo da console"); il **meccanismo** è *come* lo realizzo (es. il modulo `pam_securetty.so`). Separarli serve a: (1) confrontare politiche diverse senza impantanarsi nei dettagli tecnici; (2) trovare il set minimo di requisiti; (3) costruire meccanismi come mattoni riusabili per politiche diverse. PAM è *letteralmente* questo: il programma (`sshd`) non sa *come* si autentica, delega al framework, e tu cambi la politica editando un file di testo senza ricompilare nulla. Stesso principio in S5: "che traffico voglio far passare" (politica) ≠ "quale regola iptables scrivo" (meccanismo).

Proprietà di una buona **politica**: privilegio minimo, consistenza (schema di risoluzione non ambiguo quando più regole si applicano), completezza/correttezza (risposta entro un tempo dato + una regola di default).

> **Domanda**: cosa vuol dire "consistenza — nessuna soluzione unica"?
> **Risposta**: quando due regole diverse potrebbero applicarsi alla stessa richiesta, serve un criterio deterministico per decidere quale vince — ma **non ce n'è uno solo "giusto"**: sistemi diversi scelgono criteri diversi. Le opzioni citate: "la regola più/meno specifica vince", "default allow vs default deny", "vince la prima/ultima regola incontrata in ordine spaziale/temporale", "gerarchia degli autori". L'importante è che il criterio **esista e sia univoco**, non che sia uno in particolare. Esempi concreti dal corso: **iptables** (S5) → vince la *prima* regola che fa match; **Windows NTFS** (§10) → il *deny esplicito* vince sempre. Due criteri di consistenza diversi, entrambi validi.

Proprietà di un buon **meccanismo**: resistenza alle manomissioni, **mediazione completa** (ogni accesso passa dal controllo, nessuna scorciatoia), piccolo e autonomo, economico.

> **Domanda**: "mediazione completa" mi ricorda qualcosa di S5.
> **Risposta**: esatto, è lo stesso principio della **topologia firewall**. In S5 dicevamo: una regola perfetta non serve se la topologia lascia un'altra strada per entrare (modem dimenticato, VPN non filtrata). "Mediazione completa" è la formulazione generale: il meccanismo di controllo deve intercettare *tutti* gli accessi, senza percorsi che lo aggirano. Vale per il firewall come per i permessi filesystem.

## 3. I tre modelli: DAC, MAC, RBAC

- **DAC** (Discretionary): ogni oggetto ha un **proprietario**, che decide i permessi *a sua discrezione*. → Unix e Windows classici.
- **MAC** (Mandatory): la proprietà **non** dà il diritto di cambiare i permessi; c'è una **policy centralizzata** decisa da un security manager, imposta e non modificabile dai soggetti. → SELinux, modelli militari (BLP, Biba).
- **RBAC** (Role-Based): i permessi vanno ai **ruoli**, non agli utenti; il ruolo cambia dinamicamente (tempo, contesto).

> **Domanda**: "discretionary" e "mandatory" li confondo — quale lascia decidere all'utente?
> **Risposta**: parti dal significato inglese. **Discretionary = "a discrezione"** → è l'utente/proprietario che decide → **DAC lascia decidere all'utente**. **Mandatory = "obbligatorio, imposto"** → decide un'autorità centrale, l'utente non può cambiare nulla → **MAC toglie la decisione all'utente**. Test rapido: "posso fare `chmod` sul mio file e darlo a chi voglio?" → sì = DAC; "no, lo decide il security manager con etichette che non posso toccare" = MAC. RBAC è ortogonale: sposta il livello da *utente* a *ruolo* (l'admin assegna ruoli, non permessi singoli).

## 4. Matrice degli accessi: ACL vs capability list

Il modello astratto è una matrice soggetti × oggetti. Troppo grande → si partiziona:
- **per oggetto** = **ACL** (Access Control List): ogni oggetto ha la lista dei soggetti con permessi ≠ default. → POSIX, Windows.
- **per soggetto** = **capability list**: ogni soggetto ha la lista degli oggetti su cui ha permessi ≠ default.

> **Domanda**: ma "capability list" non è la stessa cosa delle capabilities di Linux (`cap_dac_override` ecc.)? Sembrano lo stesso nome.
> **Risposta**: **NO, e il PDF lo segnala apposta perché è una trappola.** Sono due concetti scollegati che condividono la parola.
> - **Capability list** (questa sezione) = un *modo di organizzare la matrice degli accessi* partizionandola per soggetto. Concetto teorico dei modelli di controllo d'accesso.
> - **Linux capabilities** (§8) = i *41 poteri granulari* in cui è spezzettato root (`CAP_DAC_OVERRIDE`, `CAP_NET_RAW`...). Meccanismo concreto del kernel Linux.
> Se al quiz vedi "capability list = Linux capabilities?" → **FALSO**. Ricordati che il PDF apre la slide sulle Linux capabilities proprio scrivendo "*da non confondere con le capability list dei modelli MAC*".

Il filesystem Unix tradizionale usa una ACL "rigida" nell'inode con **sempre e solo 3 soggetti**: proprietario (U), gruppo proprietario (G), tutti gli altri (O).

## 5. Permessi Unix: i 12 bit, la composizione, i bit speciali

12 bit = 9 standard (rwx per U/G/O) + 3 speciali (SUID, SGID, sticky). Semantica leggermente diversa tra file e directory, ricordando che *una directory è un file il cui contenuto è un elenco di coppie (nome, inode)*.

> **Domanda**: perché il permesso **W su una directory** mi lascia cancellare un file di cui non posso toccare il contenuto? È controintuitivo.
> **Risposta**: perché "cancellare un file" **non** è un'operazione sul file — è un'operazione **sulla directory**. Cancellare significa togliere la coppia `(nome, inode)` dall'elenco che *è* la directory: è una **scrittura sulla directory**, non sul file. Quindi conta il permesso W *sulla directory*, non i permessi *sul file*. Stesso motivo per cui puoi rinominare/spostare un file altrui se hai W sulla directory che lo contiene. (È esattamente il perché esiste lo **sticky bit** sulle temp: `/tmp` è world-writable, quindi chiunque potrebbe cancellare i file di chiunque — lo sticky bit lo impedisce, vedi sotto.)

> **Domanda**: e la differenza tra R e X su una directory?
> **Risposta**: due cose diverse che spesso si confondono.
> - **X su directory** = poter **attraversare** la directory (fare il *lookup* dell'inode di un file dentro di essa). Serve per *arrivare* a un file per path.
> - **R su directory** = poter **elencare** i nomi dei file contenuti (`ls`).
> Conseguenza esaminabile: per accedere a `/a/b/c/file` serve **X su `/a`, `/b`, `/c`** (per attraversarle), **ma non R**. Puoi accedere a un file di cui conosci il nome anche in una directory che non puoi elencare, purché tu abbia X. Viceversa, R senza X ti fa vedere i nomi ma non entrare.

**Composizione (algoritmo deterministico)**: A opera su un file → `A == U?` sì: usa permessi di U e **stop**; no → `A ∈ G?` sì: usa G; no → usa O.

> **Domanda**: se sono il proprietario **e** appartengo al gruppo, ottengo la somma dei due (il più permissivo)?
> **Risposta**: **NO.** La valutazione si ferma alla **prima categoria che fa match**, non prende il più permissivo. Se `A == U`, usa i permessi di **U e basta**, *anche se G fosse più favorevole* — G viene **ignorato**. Il PDF lo chiama "controintuitivo ma deterministico". Esempio: file con U=`r--`, G=`rw-`, tu sei proprietario E nel gruppo → ottieni `r--` (solo lettura), **non** `rw-`. ⚠️ Attenzione: questo è **l'opposto di Windows** (§10), dove invece i permessi dei vari gruppi si **sommano** bit-a-bit. Non fare confusione tra i due sistemi: Unix "prima categoria vince", Windows "somma di tutti i gruppi".

**Bit speciali sui file**:
- **SUID (bit 11)**: eseguibile lanciato → gira con l'identità dell'**utente proprietario del file**, non di chi lo lancia.
- **SGID (bit 10)**: come SUID ma sull'identità di **gruppo**.
- **sticky (bit 9) su file**: **obsoleto** (cache).

> **Domanda**: a cosa serve concretamente SUID? Sembra solo un buco di sicurezza.
> **Risposta**: serve a dare a un utente normale un'interfaccia *controllata* verso un'operazione privilegiata. Esempio-principe: **`passwd`**. Cambiare la tua password richiede di scrivere in `/etc/shadow`, che è di root. Ma tu devi poterlo fare senza essere root. Soluzione: `/usr/bin/passwd` è **SUID-root** → quando lo lanci gira come root *ma solo per fare quella cosa specifica e vincolata*. Guardalo: `ls -l /usr/bin/passwd` mostra la `s` al posto della `x` del proprietario. Altri: `crontab`, `su`, `sudo`. Il rischio (e il motivo per cui in S11 li cerchiamo per primi): se il binario SUID ha un **bug**, o è stato assegnato SUID **per errore** a un programma che non lo dovrebbe avere, chiunque lo lanci ottiene privilegi elevati fuori controllo → privilege escalation.

**Bit speciali sulle directory** (semantica diversa):
- bit 11: non usato.
- **SGID su directory**: i file creati **ereditano il gruppo** della directory → aree collaborative.
- **sticky su directory (Temp bit)**: i file sono **cancellabili solo dal proprietario** → protegge `/tmp`.

> **Domanda**: quindi lo sticky bit fa due cose diverse?
> **Risposta**: sì, ed è un'altra trappola da quiz. **Su file** = obsoleto (suggeriva cache del programma), **oggi irrilevante**. **Su directory** = i file dentro sono cancellabili solo dal loro proprietario (non da chiunque abbia W sulla directory). Sui sistemi moderni conta **solo** il significato "su directory" (lo vedi come `t` in `ls -ld /tmp` → `drwxrwxrwt`). Se al quiz leggi "lo sticky bit ha lo stesso significato su file e directory" → **FALSO**.

**umask**: permessi alla creazione = "tutti quelli sensati" (666 file / 777 dir) **meno** la umask (una maschera che *toglie* permessi). Una umask sensata su Linux è `006` (toglie r+w agli "other").

## 6. Attributi, POSIX ACL, superuser, capabilities

**Attributi** (`chattr` modifica, `lsattr` visualizza) rilevanti per la sicurezza:
- **append-only (`a`)**: si aggiunge solo in coda → impedisce di **azzerare i logfile** (difesa anti-cancellazione tracce).
- **immutable (`i`)**: niente cancellazione/link/rinomina/scrittura → blinda i file di sistema.
- **secure deletion (`s`)**: sovrascrive con zeri i blocchi cancellati (protezione limitata).

**POSIX ACL** (`setfacl` imposta, `getfacl` mostra): rimuovono la rigidità dei 3 soggetti, permettono liste arbitrarie di utenti/gruppi + una **mask** che limita simultaneamente. `ls -l` mostra `+` se una ACL estesa è presente.

**Superuser**: `root` (Unix) / `administrator` (Windows) scavalca i controlli. Difesa: usare account non privilegiato per il 99% del tempo, `sudo` puntuale.

**Linux capabilities**: 41 poteri granulari (kernel 5.9) in cui è spezzettato root — implementano il minimo privilegio (dai a un processo *solo* il potere che gli serve, non root pieno). `getcap`/`setcap` per gestirle.

> **Domanda**: cos'è di preciso `CAP_DAC_OVERRIDE` e perché lo cita sempre?
> **Risposta**: è la capability che permette di **ignorare i permessi del filesystem** ("DAC" = il modello discrezionale, "override" = scavalcalo). Un processo che ce l'ha può leggere/scrivere *qualsiasi* file indipendentemente dai suoi rwx. È il ponte diretto con **S11**: nell'esercizio `change4` (11/01/2024) c'era `cap_dac_override` assegnata a **`tee`** → con `tee` potevi scrivere `/etc/passwd` (aggiungendoti un utente con UID 0) *senza* essere root e *senza* che `tee` fosse SUID. La lezione S9 è la teoria; quell'esercizio è la pratica. Enumerazione tipica in privesc: `getcap -r / 2>/dev/null` per trovare binari con capability pericolose, esattamente come `find / -perm +6000` per i SUID.

## 7. PAM — il framework (dove la teoria diventa file di config)

**PAM = Pluggable Authentication Modules**. Framework a moduli caricabili con cui i programmi delegano autenticazione e autorizzazione, configurabili per-programma senza ricompilare.

> **Domanda**: perché non basta che ogni programma controlli la password da solo? Che problema risolve PAM?
> **Risposta**: senza PAM, ogni programma (`login`, `sshd`, `su`, `sudo`, `passwd`, `cron`...) dovrebbe implementare *da sé* la logica delle credenziali. Risultato: codice duplicato in decine di programmi, incoerente, e — soprattutto — se vuoi cambiare il *modo* di autenticare (aggiungere autenticazione a due fattori, o LDAP, o Kerberos) devi **ricompilare tutti**. PAM astrae questa logica: il programma dice solo "PAM, autentica questo utente" e **l'amministratore decide come**, editando un file di testo in `/etc/pam.d/`. Cambi la politica per tutti i programmi senza toccarne il codice. È il "separa politiche e meccanismi" del §2 reso infrastruttura.
> Dettaglio pratico: un programma è "PAM-aware" se linka `libpam` — lo verifichi con **`ldd /usr/bin/su`** (se compare `libpam.so` lo usa). I moduli `.so` stanno in `/lib/security`.

**Config**: o file unico `/etc/pam.conf` (righe con `program` in testa), o — **più comune** — un file per programma in **`/etc/pam.d/`** (nome file = nome programma, es. `/etc/pam.d/sshd`). Formato riga:
```
module-type   control-flag   module-path   [arguments]
```

### 7a. I quattro module-type (seconda distinzione critica)

- **`auth`** = **autenticazione** (verifica identità: password da `passwd`/`shadow`).
- **`account`** = **autorizzazione** di account (l'utente autenticato può accedere *ora, da qui*? Restrizioni per gruppo/orario/path; scadenza password). **NON riguarda l'autenticazione.**
- **`session`** = setup al login / cleanup al logout (montare home, limiti, log).
- **`password`** = aggiornamento dei token di autenticazione (cambio password).

> **Domanda**: `auth` e `account` mi sembrano la stessa cosa — entrambi decidono se entro o no, no?
> **Risposta**: è **la** confusione da evitare, ed è la distinzione autenticazione/autorizzazione del §1 messa in pratica. Non sono la stessa cosa:
> - **`auth`** verifica *chi sei* → password corretta? → **autenticazione**.
> - **`account`** verifica, *dato che sei già identificato*, se hai il **diritto** di accedere in queste condizioni → **autorizzazione**.
> Esempio che li separa nettamente: inserisci la password giusta → **`auth` passa** (sei tu). Ma sono le 3 di notte e `pam_time` limita il tuo accesso all'orario d'ufficio → **`account` fallisce**. Sei autenticato ma non autorizzato *ora*. Oppure: `/etc/nologin` esiste → `pam_nologin` (che agisce su auth *e* account) blocca tutti tranne root. Regola mnemonica: **`auth` = "chi sei"; `account` = "hai il permesso di entrare adesso"**.
> E non confondere neanche **`password`** con **`auth`**: `auth` *verifica* la password all'ingresso, `password` gestisce il *cambio* della password (momenti diversi, moduli diversi come `cracklib`/`pwcheck`).

### 7b. I control-flag (terza distinzione critica: required vs requisite)

| flag | successo del modulo | fallimento del modulo |
|---|---|---|
| **requisite** | stack continua | **ferma subito** → stack fallisce |
| **required** | stack continua | stack **continua** ma fallirà comunque |
| **sufficient** | **ferma subito con successo** (se nessun required prima è fallito) | stack continua |
| **optional** | stack continua | stack continua (conta solo se è l'unico determinante) |

> **Domanda**: `required` e `requisite` sembrano identici — entrambi "obbligatori". Che differenza c'è?
> **Risposta**: sì, entrambi **devono** passare perché lo stack riesca. La differenza è **cosa succede quando falliscono**:
> - **`requisite` fallisce → SI FERMA SUBITO** e ritorna il fallimento immediatamente. Non esegue i moduli successivi.
> - **`required` fallisce → CONTINUA** a eseguire i moduli successivi, ma lo stack è **già condannato** a fallire alla fine.
> Perché due comportamenti? Con **`required`** l'utente arriva in fondo allo stack e riceve *sempre* lo stesso messaggio di fallimento generico, così un attaccante **non capisce quale** controllo è fallito (username sbagliato? password? orario?) — meno informazione trapela. E permette a moduli successivi (es. logging con `pam_warn`) di girare comunque. Con **`requisite`** invece si taglia corto subito, utile quando non serve proseguire. Mnemonica: **requi-SITE = uSCITa immediata** al fallimento; **required = "richiesto" ma "resta" fino in fondo**.

> **Domanda**: e `sufficient`? Se uno `sufficient` passa, finisce tutto lì?
> **Risposta**: quasi. Se un `sufficient` **riesce** *e nessun `required` precedente era fallito*, lo stack **termina subito con successo**, saltando i moduli rimanenti. MA: un `required` fallito *prima* di lui **sovrascrive** il suo successo — la condanna del required resta. Esempio dal PDF: `auth required pam_unix` + `auth sufficient pam_krb5` → lo stack riesce **se e solo se `pam_unix` riesce**, perché il suo `required` fallito batterebbe il `sufficient` di krb5. Invertendo l'ordine (`sufficient pam_krb5` prima di `required pam_unix`), invece, basta che **uno dei due** riesca → **l'ordine cambia la logica**. Insidia extra: un `sufficient` che riesce **salta** i moduli dopo di lui anche se erano utili (es. `pam_env` che imposta variabili ma non autentica) → effetto collaterale indesiderato.

### 7c. module-path, argomenti, moduli comuni

module-path = percorso della `.so`. Argomenti standard: `debug`, `no_warn`, **`use_first_pass`** (usa la password del modulo precedente, fallisce se non va), **`try_first_pass`** (la *prova*, se fallisce la richiede).

> **Domanda**: `use_first_pass` vs `try_first_pass`?
> **Risposta**: entrambi riusano la password già inserita in un modulo precedente per non chiederla due volte. `use_` è **rigido**: se quella password non funziona, **fallisce e basta**. `try_` è **morbido**: se non funziona, **ripiega chiedendola** all'utente. Mnemonica: *try* = "ci provo, altrimenti te la chiedo".

Moduli comuni (filename `pam_<name>.so`), col loro **tipo** che dice in quale fase agiscono: `unix` (tutti e 4, autenticazione classica su passwd/shadow), `securetty` (auth, root solo da tty in `/etc/securetty`), `nologin` (auth/account, blocca tutti tranne root se esiste `/etc/nologin`), `time` (auth, orari da `time.conf`), `access` (account, coppie utente/macchina da `access.conf`), `limits` (session, limiti risorse), `cracklib`/`pwcheck` (password, robustezza), `tally` (auth/account, nega dopo N tentativi → **anti-bruteforce**), `deny` (tutti, **fallisce sempre**), `warn` (tutti, logga su syslog).

### 7d. Default-deny in PAM

`/etc/pam.d/other` (fallback per i programmi senza file dedicato) con `pam_warn` + `pam_deny` per ogni module-type = **default-deny**: ogni programma privo di configurazione specifica viene **loggato e negato**. Stesso principio del `policy drop` di S5.

## 8. Demoni di sistema — i processi privilegiati come bersaglio

Il PDF "Demoni di sistema" è scritto dal **POV dell'attaccante già dentro**: accesso legittimo → privilegi limitati → privilege escalation via **vulnerabilità locali**. Il vettore centrale è la **bomba logica**: un processo gira con privilegi di admin; se i **file che usa hanno permessi errati**, un utente non privilegiato ci inietta codice e **aspetta che il sistema lo esegua** (a un orario, all'avvio/arresto di un sottosistema, a un evento).

> **Domanda**: qual è la differenza tra un "demone" e un normale processo? Li uso come sinonimi.
> **Risposta**: distinzione da tenere. Un **processo** è qualsiasi programma in esecuzione (anche `ls` mentre gira). Un **demone** (daemon) è un tipo *specifico* di processo: gira **in background**, **senza terminale interattivo**, tipicamente **avviato al boot** e attivo per tutta la vita del sistema, in attesa di eventi o richieste. Convenzionalmente il nome finisce in **`d`**: `crond`, `atd`, `sshd`, `systemd`. Perché contano qui: i demoni sono i processi che girano **con privilegi elevati e in modo persistente**, quindi sono esattamente ciò che un attaccante vuole dirottare — se convinci un demone di root a eseguire il tuo codice (o gli dai in pasto un file di config che controlli), ottieni i suoi privilegi. Un processo utente normale che gira coi tuoi permessi non ti dà nessuna scalata; un *demone* privilegiato sì.

**cron** (`crond`): esegue task pianificati leggendo i **crontab** ogni minuto. Per utente in `/var/spool/cron/crontabs/<utente>` (gestiti con `crontab -l/-e/<file>`); system-wide in `/etc/crontab` (che richiama `/etc/cron.{hourly,daily,weekly,monthly}/`; questi hanno **un campo in più**: l'utente per cui eseguire). Sintassi: `MIN ORA G.MESE MESE G.SETT comando`.

> **Domanda**: i 5 campi del crontab sono in AND o in OR?
> **Risposta**: normalmente in **AND** — il task parte quando l'ora corrente corrisponde a *tutti* i selettori. **ECCEZIONE** (classica da quiz): se specifichi (≠ `*`) **sia** il giorno del mese **sia** il giorno della settimana, quei due campi passano in **OR**. Esempio del PDF: `30 4 1,15 * 6 /bin/backup` → gira il **giorno 1 + il 15 + ogni sabato** alle 4:30 (non "solo i giorni 1/15 che cadono di sabato"). Solo i due campi-giorno hanno questa eccezione; gli altri restano in AND. Perché cron è un vettore privesc: se puoi scrivere uno script eseguito da un cron di root, root eseguirà il tuo codice.

**at** (`atd`): esecuzione **una tantum** a un momento prefissato. Comandi: `at TIME`, `atq` (lista), `atrm` (rimuovi), `batch` (esegue quando il carico è basso). Senza file, legge da stdin: `echo "comando" | at 08:00`.

> **Domanda**: differenza tra cron e at?
> **Risposta**: **cron = ricorrente** (ogni giorno alle 8, ogni lunedì...); **at = una volta sola** a un istante futuro (domani alle 8, poi basta). `batch` è una variante di `at` che aspetta un momento di **basso carico** invece di un orario fisso.

**Event manager / IPC**: **D-Bus** (IPC tra componenti desktop; config in `/etc/dbus-1/`) e **udev** (crea i device special file quando connetti un dispositivo; regole evento→azione in `/etc/udev/rules.d`, oggi parte di systemd). Entrambi eseguono azioni → potenziali vettori se le regole sono scrivibili.

**init** = **primo processo del kernel (PID 1)**, gestisce i **runlevel** (stati definiti dal set di servizi attivi), orchestra boot/shutdown. Tre varianti storiche: **SystemV** (storico), **Upstart** (Canonical 2006-14), **systemd** (2010-oggi).

**sysvinit**: `/sbin/init` configurato da **`/etc/inittab`** (default runlevel `id:2:initdefault:`; keyword `single` al boot → single user mode/runlevel 1 → shell di root per chi ha accesso al boot loader). Righe `wait` → esecuzione sequenziale degli script `S*` (start) e `K*` (stop) in `/etc/rcN.d/` (symlink a `/etc/init.d/`); righe `respawn` → riavvia il processo se muore.

**systemd** — le **unit** (`nome.tipo`) sostituiscono runlevel e script init. Tipi: **Service** (demoni), **Socket** (IPC/attivazione on-demand), **Target** (rimpiazza i runlevel), Device, Mount/Automount/Swap, Snapshot, **Timer** (rimpiazza cron/at), Path (inotify), Slice (cgroup), Scope. Definizioni in ordine di priorità: `/lib/systemd/system/` (riferimento) < `/usr/lib/systemd/system/` (pacchetti) < **`/etc/systemd/system/` (personalizzazioni, prioritarie)**.

> **Domanda**: differenza tra `systemctl start` e `systemctl enable`? E `stop`/`disable`/`mask`?
> **Risposta**: due assi diversi che non vanno mescolati.
> - **`start`/`stop`** = azione **adesso**, **volatile**: avvia/ferma il servizio nella sessione corrente, ma **non cambia** la configurazione (dopo un reboot torna com'era). `restart` = stop+start; `stop` manda SIGTERM poi SIGKILL dopo un timeout.
> - **`enable`/`disable`** = comportamento **al boot**, **persistente**: decidono se il servizio parte automaticamente all'avvio. **Non** hanno effetto immediato (non avviano/fermano nulla ora).
> - **`mask`** = il grado più forte di `disable`: **neutralizza tutta la definizione** della unit, impedendo persino lo `start` manuale (la "spegne" del tutto); `unmask` la riabilita.
> Combinazioni esaminabili: `start` **non** abilita al boot; `enable` **non** avvia subito; `disable` lascia comunque possibile lo `start` a mano, `mask` no. Nota di sicurezza: chi può scrivere in `/etc/systemd/system/` può **ridefinire (override)** una unit di sistema per la sua priorità → esegue codice coi privilegi del servizio (vettore privesc/persistenza).

## 9. Windows DAC — punti da ricordare (differenze da Unix)

- **Domini** + Active Directory (directory database comune). Utenti **locali** vs **di dominio**.
- **Gruppi**: tipo (*Distribution*, solo liste / *Security*, usabili nelle regole) × scope (*Machine Local*, *Domain Local*, *Global*, *Universal*).
- **NTFS**: ACL su partizioni **NTFS non FAT** e su condivisioni. **Ownership**: l'owner ha Full Control; Administrator può *sempre* prenderla.
- **DACL** (autorizza/nega) vs **SACL** (**auditing**: traccia gli esiti dei tentativi).
- **Autorizzazioni speciali** (molte, logica a 3 valori allow/deny/not-set) aggregate in **standard** (R, W, RX, L, M, F).

> **Domanda**: la composizione dei permessi in Windows è come in Unix?
> **Risposta**: **NO, è diversa — attenzione a non trasferire la regola di Unix.**
> - **Unix**: vince la **prima categoria** applicabile (U, poi G, poi O); le altre sono ignorate.
> - **Windows**: l'utente può stare in molti gruppi, e i permessi si **sommano bit-a-bit** su tutti i gruppi. Poi:
>   - **`not set`** (né allow né deny) = **deny "debole"/scavalcabile**: lascia che un `allow` di un *altro* gruppo abbia effetto.
>   - **`deny` esplicito** = **deny "forte"/non scavalcabile**: batte **sempre** qualunque `allow` di qualunque gruppo.
> Ecco perché servono *due* modi di negare: `not set` tiene la porta socchiusa (un altro gruppo può aprirla con allow), `deny` esplicito la sbarra. Esempio: gruppo A ti dà `not set` su Write, gruppo B ti dà `allow` Write → ottieni **Write** (il not-set è scavalcabile). Ma se A ti dà `deny` esplicito Write e B `allow` Write → **niente Write** (il deny vince). Al quiz, se confondono Unix e Windows: "in Windows vince la prima categoria come in Unix" → **FALSO**.

- **Share vs locale**: si applicano **in serie**, effettivo = **il più restrittivo** tra permesso di share e NTFS locale.
- **Copy/Move**: copiato → eredita i permessi della destinazione; spostato nella *stessa* partizione → conserva i suoi; spostato tra partizioni **diverse** = copy+delete → eredita la destinazione.
- **GPO** (Group Policy): privilegi/restrizioni non legati a risorse fisiche (bloccare USB, config desktop), collegabili a OU/Site/Domain, con sezioni user e computer.

## 10. MAC: Bell-LaPadula vs Biba (la coppia speculare)

MAC = regole da autorità centrale; a soggetti/risorse si assegna una **classe di accesso** = livello di sicurezza (insieme *ordinato*: TopSecret ► Segreto ► Riservato ► Non classificato) + categoria/compartment (insieme *non ordinato*). Risorse etichettate = *classification/sensitivity*; soggetti = *clearance*. **Dominanza**: L1 domina L2 ⇔ S1 ≥ S2 **e** C1 ⊇ C2.

> **Domanda**: BLP e Biba li confondo sempre — chi fa cosa?
> **Risposta**: sono **speculari**, ed è proprio la specularità a fregarti. Ancora ognuno alla proprietà che protegge.
> - **Bell-LaPadula = RISERVATEZZA** (i segreti non devono uscire/scendere): **NO-READ-UP** (non leggi sopra la tua clearance, non vedi segreti troppo alti) + **NO-WRITE-DOWN** (non scrivi sotto, non fai colare un segreto verso chi ha clearance minore). Mnemonica: *"read down, write up"* è ciò che **puoi** fare in BLP.
> - **Biba = INTEGRITÀ** (la spazzatura non deve salire/contaminare): **NO-READ-DOWN** (non leggi sotto, non ti contamini con dati meno affidabili) + **NO-WRITE-UP** (non scrivi sopra, non corrompi risorse più affidabili). Mnemonica: *"read up, write down"*, l'opposto di BLP.
> Il modo infallibile: **BLP protegge i segreti** (confidenzialità → li tieni in alto, non scendono), **Biba protegge la qualità** (integrità → la sporcizia sta in basso, non sale). Se ricordi *quale proprietà* protegge ciascuno, le 4 regole si ricostruiscono da sole. Applicandoli insieme (due classi per entità) proteggi riservatezza E integrità contemporaneamente.

## 11. RBAC

Permessi ai **ruoli**, non agli utenti; ruolo dinamico. Modello **"policy neutral"**: esprime minimo privilegio, separazione delle responsabilità, astrazione. Vantaggio gestionale: se ben modellato, i permessi cambiano poco; l'admin **assegna ruoli**, non permessi singoli. Standard ANSI/INCITS 359-2004.

---

## Connessioni

> ⚠️ Sezione non presente in appunti grezzi (non esistono grezzi per S9).

- **S2 (Autenticazione)**: S9 completa S2. S2 = *come* si autentica (hash, `/etc/shadow`); PAM `auth`+`pam_unix` = il *framework* che invoca quei meccanismi. La distinzione autenticazione/autorizzazione (§1) è il raccordo S2↔S9.
- **S5 (Firewall)**: **mediazione completa** (§2) = la topologia firewall che costringe tutto il traffico dal punto di controllo. **Default-deny** (§2, §7d) = `policy drop` delle catene nft. Consistenza "prima regola vince" = ordine delle regole iptables.
- **S11 (Integrity/privesc)** — legame più forte: SUID/SGID (§5), `cap_dac_override` (§6), bombe logiche via cron/at/systemd (§8) sono la **teoria** degli esercizi già fatti da Lorenzo: `change1` (SUID su `cp`), `change4` (`cap_dac_override` su `tee`), `change5`. `find / -type f -perm +6000` e `getcap -r /` = primo passo di enumerazione privesc.
- **S7 (Backdoor injection) / S8 (Filtrare attacchi)**: cron/at/udev + stack PAM = meccanismi di **persistenza** di una backdoor; append-only sui log (§6) = contromisura anti-cancellazione tracce.
- **S1 (Enumerazione)**: `find` (SUID/world-writable/nouser) e `ldd` (uso di PAM) = enumerazione **locale**, gemella post-accesso dell'enumerazione di rete di S1.
- **S10 (NIDS)**: controllo d'accesso = prevenzione; HIDS/AIDE + auditing (SACL, `pam_warn`) = rilevazione locale di ciò che passa comunque.

## Domande di autoverifica — Risposte

> ⚠️ Sezione non presente in appunti grezzi. Risposte alle 20 domande della lezione.

1. **Falso** — invertite: l'**autenticazione** decide *chi* è il soggetto, l'**autorizzazione** decide *cosa* può fare.
2. **Vero** — è la definizione esatta di DAC (proprietario decide) vs MAC (policy centralizzata imposta).
3. **Falso** — trappola: le *capability list* (partizione della matrice per soggetto) NON sono le *Linux capabilities* (`CAP_DAC_OVERRIDE` ecc.). Nomi uguali, concetti scollegati.
4. **(b)** — `r--`: in Unix vince la **prima categoria** applicabile (A == U), G è ignorato anche se più favorevole. Non si somma (quello è Windows).
5. **Vero** — cancellare = scrivere nella directory (togliere la coppia nome/inode), non toccare il contenuto del file. Conta W sulla directory.
6. **Falso** — serve **X** (non R) su ogni directory intermedia per attraversarla; R serve solo a elencare il contenuto.
7. **(b)** — l'utente **proprietario del file**. (Non è "sempre root": è root solo se il file è di root.)
8. **Falso** — su file è obsoleto (cache); su directory impone che i file siano cancellabili solo dal proprietario (protezione `/tmp`).
9. **Falso** — in quel caso specifico (entrambi i giorni ≠ `*`) i due campi-giorno vanno in **OR**, non in AND (eccezione alla regola generale dell'AND).
10. **(c)** — `mask` neutralizza l'intera unit impedendo anche lo start manuale (`disable` lo lascia possibile).
11. **Falso** — `start` è volatile e agisce solo ora; l'avvio al boot lo dà `enable` (persistente).
12. **Falso** — invertiti: **`auth`** verifica l'identità (password), **`account`** verifica il diritto di accedere date le condizioni (orario, gruppo, nologin).
13. **(b)** — `requisite` ferma subito lo stack al fallimento; `required` continua a eseguire i moduli successivi ma lo stack fallirà comunque.
14. **Vero** — un `sufficient` che riesce (senza `required` precedenti falliti) termina subito con successo, saltando i moduli rimanenti.
15. **Vero** — BLP (riservatezza): no-read-up + no-write-down; Biba (integrità): no-read-down + no-write-up. Speculari.
16. **(b)** — allow: `not set` è un deny "debole"/scavalcabile, quindi l'`allow` di un altro gruppo prevale.
17. **Vero** — in Windows il `deny` esplicito è "forte" e batte sempre qualunque `allow` da altri gruppi.
18. **(b)** — `find / -type f -perm +6000` cerca SUID(4000)+SGID(2000). (`-perm +2` = world-writable; `-nouser` = file orfani; `getcap` = capability, ricerca complementare ma non SUID.)
19. **Vero** — `/etc/pam.d/other` con `pam_deny` per ogni module-type nega ogni programma senza config PAM specifica = default-deny.
20. **Vero** — copy → eredita i permessi della destinazione; move tra partizioni diverse = copy+delete → anch'esso eredita la destinazione (move nella *stessa* partizione invece li conserva).

## Riepilogo — le tre distinzioni che valgono metà del quiz su questo modulo

> ⚠️ Sezione non presente in appunti grezzi.

1. **Autenticazione (`auth`, "chi sei") ≠ Autorizzazione (`account`, "cosa puoi fare / puoi entrare ora")**. È il cuore del modulo, presente sia a livello concettuale (§1) sia in PAM (§7a).
2. **required ≠ requisite** (in caso di fallimento: required *continua*, requisite *si ferma subito*); e **sufficient** che riesce chiude lo stack con successo saltando il resto (§7b).
3. **Bell-LaPadula (riservatezza) ≠ Biba (integrità)**, regole speculari (§10); e **composizione permessi Unix (prima categoria vince) ≠ Windows (somma dei gruppi, deny esplicito batte tutto)** (§5, §9).

Più le coppie operative: **cron (ricorrente) vs at (una volta)**; **start/stop (volatile, ora) vs enable/disable/mask (persistente, al boot)**; **SUID (identità utente proprietario) vs SGID (gruppo)**; **capability list del modello (per soggetto) vs Linux capabilities (poteri di root)**.

Filo unico: i **demoni** privilegiati (§8) eseguono con l'autorità definita dal modello di **autorizzazione** (§3-6, 9-11), e verificano identità e diritti tramite **PAM** (§7) — un errore di permessi in uno qualsiasi dei tre livelli è un vettore di privilege escalation (ponte diretto con S11).

<!-- AUTO-LINKS:START -->
<!-- AUTO-LINKS:END -->
