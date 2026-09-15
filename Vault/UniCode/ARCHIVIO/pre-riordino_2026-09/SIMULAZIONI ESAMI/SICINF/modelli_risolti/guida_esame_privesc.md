# Guida Esame — Integrity Check & Privilege Escalation

> File cockpit da aprire il giorno dell'esame appena riconosci un esercizio di questo tipo (un
> binario `changeN` o un pacchetto `.deb`/`.deb.gz`/`.deb.gpg` che "apporta modifiche a file dentro
> `/usr/bin` e `/etc`", con Fase 1 = identificare le modifiche e Fase 2 = diventare root **senza il
> potere sudo di `kali`**). Autosufficiente per la maggior parte dei casi. Per l'algoritmo esteso
> passo-passo vedi `procedura_operativa_privesc.md`; per 9 casi reali già risolti,
> `modello_integrity_privesc.md`.
>
> **Principio guida**: se sei bloccato su come costruire un comando, la risposta è quasi sempre
> nella **Sezione 4**. Se sei bloccato su *quale* modifica sfruttare, è nella **Sezione 3**.

---

## 0. I due gate che NON hai il permesso di saltare

- ⚠️ **Gate A — ordine.** Hai creato la baseline AIDE (`aideinit` + copia manuale di `aide.db.new`
  in `aide.db`) **prima** di eseguire `changeN`/installare il `.deb`? Se hai fatto il contrario, la
  baseline è già "sporca": ricrea la VM pulita. E hai davvero aggiunto `/usr/bin f Full` al config
  **prima** di `aideinit`? Senza, i binari non vengono confrontati.
- ⚠️ **Gate B — non fermarti al primo file.** Il pacchetto introduce **più modifiche insieme** e di
  norma **una sola è sfruttabile**. Hai analizzato *ogni* riga del diff (con `getcap`/`getfacl`/
  `ls -l`) e scritto per ciascuna se è il vettore o un vicolo cieco? In 7 dei 9 esercizi reali la
  maggior parte delle modifiche era rumore deliberato. Saltare l'analisi porta a inseguire un
  depistaggio (una `cap_mknod`, un'ACL su `mknod`, un SUID su `yes`) e perdere tempo.

---

## 1. Triage — che tipo di esercizio è

Tutti gli esercizi della famiglia hanno la **stessa struttura** (baseline AIDE → esegui →
confronta → sfrutta), ma cambiano formato di consegna e obiettivo di Fase 2. Guarda la consegna:

| Segnale nella consegna | Cosa implica |
|---|---|
| File `changeN` (binario ELF) | Modifiche applicate direttamente; formato più vecchio (2023–2025). `chmod +x` + `sudo ./changeN`. |
| Pacchetto `.deb.gz` | `gunzip` poi `sudo dpkg -i`. Formato dal luglio 2025. |
| Pacchetto `.deb.gpg` | `gpg -d file > e.deb` (password tipica `esame`) poi `sudo dpkg -i`. Formato dal 2025-10. |
| "creare utente `X` con privilegi di root e **senza password**" | riga passwd `X::0:0::/root:/bin/bash` (campo pw vuoto). |
| "…con password `Y`" | serve un hash: `openssl passwd -1 -salt s Y` inline nel 2° campo passwd, oppure in shadow. |
| "diventare root e lanciare `id`" (senza nome/pw) | libertà totale sul metodo; scegli il vettore più diretto. |
| "senza ricorrere al potere sudo dell'utente `kali`" (quasi sempre) | l'exploit non può essere `sudo <x>` come `kali`; deve passare per il vettore introdotto dal pacchetto. |
| "più eventualmente altre modifiche da dedurre" | il diff AIDE potrebbe non mostrare tutto: usa anche `getcap -r /`, `find / -perm /7000`, `getfacl -sR /`. |

Il triage non decide il vettore: quello emerge **solo** dall'analisi del diff (Sezione 3). Non
assumere che l'esercizio X usi lo stesso vettore di un esercizio simile — il pool ricicla i
binari (`vim.tiny`, `tee`, `chmod`, `cp`) ma cambia quale sia quello *vero*.

---

## 2. Percorso standard (checklist)

Versione condensata di `procedura_operativa_privesc.md` — apri quel file per il dettaglio.

- [x] **0. AIDE installato?** `which aide` — se non c'è (`/etc/aide` non esiste), **`sudo apt install
  aide`** prima di tutto. Su Parrot/Kali di questa VM AIDE **non è preinstallato di default**
  (troubleshooting_vm.md, §S11): senza, sei bloccato al passo 1.
- [x] **1. Config AIDE**: commenta `@@x_include …`; aggiungi `/usr/bin f Full` e `/etc f Full`
  (o regola custom `p+n+u+g+s+m+c+xattrs+md5+sha512`). ⚠️ **Sintassi esatta: `/usr/bin f Full`,
  campi separati da SPAZI, NIENTE trattino.** `/usr/bin -f Full` (col `-f`) è un errore comune e
  fa fallire/ignorare la regola. *(Gate A: prima della baseline.)*
- [x] **2. Baseline**: `sudo aideinit` **poi** `sudo cp /var/lib/aide/aide.db.new /var/lib/aide/aide.db`.
- [x] **3. Esegui il file** fornito (binario o `.deb`).
- [x] **4. Confronta**: `sudo aide -C -c /etc/aide/aide.conf`.
- [x] **5. Leggi il diff**: legenda della riga di sintesi in `procedura_operativa_privesc.md` §5
  (ricorda: `X`=xattr/capability, `A`=ACL, `>`=contenuto cresciuto, `c`/ctime da solo = rumore).
- [x] *(Gate B qui.)* **6. Analizza OGNI file segnalato** (§3): vettore o vicolo cieco?
- [ ] **7. Sfrutta** il vettore (§3/§4), verifica con `id` → `uid=0(root)`.
- [ ] **8. `integrity.txt`** (strategia + output AIDE incollato + analisi file-per-file) e
  **`privesc.png`** (comandi + prova `id`).

---

## 3. Rami speciali — un ramo per vettore

Per ciascuno: **come si riconosce nel diff/ispezione**, **come si sfrutta**, **gotcha**. I nomi
tra parentesi rimandano ai casi reali in `modello_integrity_privesc.md`.

### 3.1 SUID bit (9 gen 2023; ricreato in 8 feb 2024)

- **Riconoscere**: nel diff `p` (permessi) su un binario; `ls -l` mostra la **`s`** al posto della
  `x` nel campo utente (`-rwsr-xr-x`). Scoperta a tappeto: `find / -perm /7000 2>/dev/null`.
- **Sfruttare**: il binario gira coi privilegi del **proprietario** (root), chiunque lo lanci. Se è
  `cp`/`tee`/un editor → scrivi `/etc/passwd`/`/etc/shadow` come root:
```
cp /etc/passwd ~/p ; cat ~/p > ~/passwd            # cat > per una copia scrivibile
echo "toor::0:0::/root:/bin/bash" >> ~/passwd
cp ~/passwd /etc/passwd
su toor
```
- **Sfruttare (2) — il SUID è un interprete/shell, non solo "scrive file"**: se il bit SUID cade su
  un binario che sa **eseguire comandi o aprire una shell** (`find`, `python3`, `perl`, `bash`,
  `vim`, `awk`, `less`, `nmap`…), non serve passare da `/etc/passwd`: prendi una **shell root
  diretta**. Ricette GTFOBins (funzione *Shell*, generalizza §3.6 dal sudoers al SUID):
```
find . -exec /bin/sh -p \; -quit          # -p: la shell NON rilascia l'euid ereditato dal SUID
bash -p                                    # se il SUID è direttamente bash: -p preserva l'euid
python3 -c 'import os; os.setuid(0); os.system("/bin/sh")'   # setuid(0) allinea ruid/euid a 0
perl -e 'use POSIX qw(setuid); setuid(0); exec "/bin/sh";'
vim -c ':py3 import os; os.setuid(0); os.execl("/bin/sh","sh","-pc","reset; exec sh")'
```
  ⚠️ **Il `-p` / `setuid(0)` NON è un dettaglio.** Un SUID lancia il binario con **euid=0** ma
  **ruid=<tuo utente>**; bash e molti interpreti, all'avvio, **rilasciano** l'euid quando
  `euid≠ruid` (misura di sicurezza) e ti riportano ai tuoi privilegi. `-p` (bash/sh) impedisce quel
  rilascio; `setuid(0)` (python/perl) forza `ruid=euid=suid=0`. È lo **stesso principio
  real-vs-effective** del gotcha `cat > file` qui sotto e di §4.6. **Differenza col caso sudoers
  (§3.6)**: lì `vi`/`find` girano con **ruid=euid=0** (è `sudo`, non SUID), quindi `:!/bin/bash`
  senza `-p` basta — con un SUID *puro* invece il `-p`/`setuid` è necessario.
- **Gotcha**: se copi `passwd`/`shadow` con un `cp` SUID, la **copia resta di root** e non è
  editabile — serve il passo intermedio `cat file > file_scrivibile` (la redirezione gira coi tuoi
  privilegi reali, non con quelli del SUID). **Prima di liquidare un SUID come vicolo cieco,
  cercalo in GTFOBins** (funzione *Shell*/*Command*/*File read*/*File write*): `find`, `python`,
  `perl`, `bash`, `vim`, `awk`, `less`, `nano`, `env`, `nmap`… hanno una via di fuga verso root e
  sono **quasi certamente il vettore vero**, non rumore (criterio generale in §4.5). Solo i binari
  **senza** alcuna funzione sfruttabile (`yes`, `whoami`, `sort`) sono davvero vicoli ciechi.

### 3.2 Capabilities (11 gen 2024, 8 feb 2024, feb 2025, 10 lug 2025, 30 ott 2025, 12 gen 2026)

Il ramo più frequente e più insidioso: le capability spacchettano "i poteri di root" in permessi
granulari assegnati a un binario **senza SUID**. Nel diff appaiono come `X`/`+` (xattr
`security.capability`). **Verifica sempre con `getcap <file>`** — il diff dice "c'è una capability",
solo `getcap` dice *quale*, e da quella dipende tutto:

- **`cap_dac_override`** (su `vim.tiny`, `vim.basic`, `tee`) → **il vettore d'oro**: ignora i
  controlli di permesso in lettura/scrittura, quindi l'editor/`tee` scrive **qualunque file**.
  Sfruttare: apri `/etc/passwd`, aggiungi `toor::0:0::/root:/bin/bash` o togli la `x` di root o
  metti a 0 l'UID di un utente-ponte; con vim salva forzando `:w!` (avvisa che non è scrivibile —
  è normale, la cap bypassa il DAC). Con `tee` usa **sempre la pipe** (`echo … | tee -a /etc/passwd`),
  mai `echo … >> /etc/passwd` → vedi §4.6 (il redirect lo apre la shell, non tee: fallisce sempre).
- **`cap_fowner`** (su `chmod`) → può cambiare permessi/bit di file di **altri proprietari**.
  Sfruttare: **fabbrica un secondo vettore** — `chmod u+s /usr/bin/cp` (→ SUID cp, §3.1) oppure
  `chmod 0777 /etc/passwd` e poi edita.
- **`cap_setuid`** (su un **interprete** — `python3`, `perl` — o su una shell) → permette al
  processo di chiamare `setuid(0)`/`setgid(0)` e **assumere direttamente l'identità di root**, senza
  toccare `/etc/passwd`. È il vettore più **diretto** di tutti quando cade su un binario capace di
  eseguire codice arbitrario. Verifica: `getcap /usr/bin/python3` → `cap_setuid=ep` (serve la `e` =
  *effective*; se fosse solo `p`=permitted il processo dovrebbe alzarla da sé). Sfruttare — one-liner
  che fa `setuid(0)` e apre una shell root:
```
python3 -c 'import os; os.setuid(0); os.system("/bin/bash")'
perl -e 'use POSIX qw(setuid); setuid(0); exec "/bin/bash";'
```
  poi `id` → `uid=0`. Distinguere dal rumore: `cap_setuid` su un binario che **non** esegue codice
  arbitrario (es. su `ping`) non è banalmente sfruttabile — serve un interprete/eseguibile
  controllabile. Su python/perl/una shell è quasi sempre il vettore vero.
- **`cap_dac_read_search`** (l'equivalente in **lettura** di `cap_dac_override`, che è
  lettura+scrittura) → bypassa i controlli di permesso in **lettura** e la ricerca nelle directory:
  consente di **leggere qualunque file**, incluso `/etc/shadow`, senza essere root. **Non** dà
  scrittura, quindi da solo non riscrive `passwd`/`sudoers` — ma abilita il **cracking offline**
  (§3.5). Verifica: `getcap /usr/bin/cat` (o su un interprete) → `cap_dac_read_search=ep`. Sfruttare:
  usa il binario per leggere shadow e poi cracca:
```
cat /etc/shadow                      # ora leggibile grazie alla cap (con getcap su cat)
# oppure, se la cap è su un interprete:
python3 -c 'print(open("/etc/shadow").read())'
unshadow /etc/passwd /etc/shadow > /tmp/f
john -format=crypt -wordlist=/usr/share/wordlists/rockyou.txt /tmp/f     # → §3.5
```
  Distinguere: è utile **solo** in catena con un utente da crackare (il vettore è "lettura shadow →
  john", §3.5). Di per sé **non** ti fa root: è un anello, non il traguardo. (Simmetria da capire e
  saper spiegare: `cap_dac_override` = scrittura → riscrivi `passwd`; `cap_dac_read_search` = lettura
  → leggi `shadow` e cracchi.)
- **`cap_sys_admin`** (la capability "quasi onnipotente" — la man page la chiama *"the new root"*:
  include `mount(2)` e decine di operazioni privilegiate) → per una VM/container Debian il caso più
  pulito e verificabile è l'abuso di **mount**. Con `cap_sys_admin` puoi fare un **bind-mount** di un
  file che controlli **sopra** un file di sistema: da quel momento il kernel serve il *tuo*
  contenuto, **senza nemmeno modificare l'inode originale** (AIDE sul file reale non vedrebbe la
  sostituzione). Verifica: `getcap /usr/bin/mount` (o un interprete che chiami `mount(2)`) →
  `cap_sys_admin=ep`. Sfruttare — sovrascrivi *virtualmente* `/etc/passwd` con una versione con un
  root senza password:
```
cp /etc/passwd /tmp/passwd
echo "toor::0:0::/root:/bin/bash" >> /tmp/passwd
mount --bind /tmp/passwd /etc/passwd     # richiede cap_sys_admin
su toor                                   # il login legge il passwd bind-montato → root
```
  Distinguere: a differenza di `cap_setuid`, **non** è un one-liner-shell automatico — è sfruttabile
  solo se il binario che la porta compie davvero un'operazione privilegiata (`mount` stesso, o un
  interprete che invoca `mount(2)`); serve un'azione concreta (qui il bind-mount). In un container
  abilita spesso anche altri percorsi (accesso a `/proc`, namespace), ma per questo esame il mount è
  il più diretto.
- **`cap_mknod`** (su `sort`, `whoami`), **`cap_audit_read`** (su `date`) → reali ma **inutili**
  in pratica (creare device / leggere audit log non ti danno root): **vicoli ciechi**.
- **Falso positivo** (`getcap` restituisce **vuoto** pur essendo il file nel diff): il binario
  `changeN` ha impostato e poi **ripristinato** la capability (`mycapfake` = set + `cap_clear`),
  lasciando solo il `ctime` cambiato. **Vicolo cieco.**
- **Gotcha**: `getcap` è in `/usr/sbin` (se non nel PATH: `/usr/sbin/getcap`). Un editor con
  capability può essere **eseguibile solo da un certo gruppo** (permessi tipo `----rwx--- root:wbr`)
  → devi prima diventare quell'utente (vedi §3.6).

### 3.3 ACL POSIX (11 gen 2024, 13 giu 2024, feb 2025, 10 lug 2025, 30 ott 2025, 12 gen 2026)

- **Riconoscere**: nel diff `A` (ACL); `ls -l` mostra un **`+`** finale nei permessi
  (`-rw-r--r--+`). **Verifica con `getfacl <file>`** — cerca righe `user:<nome>:rwx`/`rw-`.
- **Sfruttare**: dipende da *su cosa* è l'ACL:
  - ACL di **scrittura su `/etc/sudoers`** → l'utente si aggiunge una riga sudo onnipotente
    (`echo 'X ALL=(ALL:ALL) ALL' | tee -a /etc/sudoers`) e poi `sudo -i`.
  - ACL di **scrittura su `/etc/passwd`** → aggiunge/edita una riga root.
  - ACL di **lettura su `/etc/shadow`** (`user:first:r--`) → può leggere gli hash → `unshadow` +
    `john` (§3.5).
- **Gotcha**: un'ACL che dà pieno controllo di un **binario senza privilegi speciali** (es.
  `user:spy:rw` su `tee`, o su `mknod`) è un **vicolo cieco** — poter modificare il file del binario
  non ti dà i suoi privilegi di runtime. Spesso però l'ACL indica *quale utente* è il ponte (es.
  `spy`): usalo come indizio, non come exploit. `newaclfake` nei binari `changeN` imposta e
  **ripristina** l'ACL → nel diff resta solo il ctime: falso positivo.

### 3.4 Utente senza password in /etc/passwd (13 giu 2024, 10 lug 2025, 30 ott 2025)

- **Riconoscere**: `/etc/passwd` cresciuto (`>` nel diff); leggendolo (è pubblico) trovi una riga
  col **secondo campo vuoto**: `intruso::1202:1000::/tmp:/bin/bash`, `first::1001:…`,
  `searcher::11110:…`.
- **Sfruttare**: `su <utente>` non chiede password → hai subito quel foothold. Da lì combini con
  l'altro vettore (l'utente-ponte serve a *raggiungere* la capability/ACL/sudoers introdotta). Se
  l'utente senza password ha già **UID 0** → sei direttamente root.
- **Gotcha**: quasi mai l'utente passwordless è già root; è il primo anello di una catena. La mossa
  finale tipica è metterne l'UID a 0 con un editor privilegiato (§3.2) e poi rifare `su`.

### 3.5 Utente CON password → crack (offline john / online hydra) (feb 2025, 10 lug 2025, 30 ott 2025)

Quando il vettore richiede un utente protetto da password (`next`, `wbr`, `spy`), la password va
**ottenuta**. Due strade, mutuamente esclusive a seconda dell'accesso a shadow:

- **Puoi leggere `/etc/shadow`** (ACL di lettura, o un comando che te lo fa `cat` come root):
  crack **offline**, veloce e silenzioso:
```
unshadow /etc/passwd /etc/shadow > /tmp/f
john -format=crypt -wordlist=/usr/share/wordlists/rockyou.txt /tmp/f
john --show /tmp/f          # rileggi la password trovata
```
- **NON puoi leggere shadow**: brute-force **online** via SSH:
```
hydra -l <utente> -P /usr/share/wordlists/rockyou.txt ssh://localhost
```
- **Gotcha wordlist**: se `/usr/share/wordlists/rockyou.txt` non esiste, di norma è ancora compressa:
  `sudo gunzip /usr/share/wordlists/rockyou.txt.gz` (una volta sola). Senza, john/hydra falliscono
  con "No such file".
- **Gotcha**: se il servizio SSH è disabilitato, hydra su ssh non funziona → devi trovare un modo
  di leggere shadow come root (es. abuso sudoers, §3.7) e passare a john. Viceversa, se shadow non è
  leggibile e SSH è attivo, hydra è l'unica via (caso feb 2025). Non esiste un unico comando
  "giusto": dipende da quale delle due condizioni vale.

### 3.6 sudoers permissivo (feb 2025, 30 ott 2025; base nei lab)

- **Riconoscere**: `/etc/sudoers` nel diff, o un file **aggiunto** in `/etc/sudoers.d/` (entry
  `ADDED`). Leggilo; conferma con `sudo -l` una volta che sei l'utente giusto.
- **Sfruttare**, per tipo di regola:
  - `NOPASSWD: /usr/bin/tee` → `echo "toor::0:0::/root:/bin/bash" | sudo /usr/bin/tee -a /etc/passwd`.
  - `NOPASSWD: /usr/bin/vi <path>/*` → dentro `vi` esegui `:!/bin/bash` (shell come root), oppure
    apri un file fuori path con **path traversal** (`…/../../../etc/shadow`).
  - **Wildcard** `… -exec cat *` → il `*` finale ti lascia mettere **qualunque argomento**: `sudo
    /usr/bin/find /etc/passwd -exec cat /etc/shadow \;` esegue `cat /etc/shadow` **come root** →
    esfiltrazione. (Caso 30 ott 2025: è così che si legge shadow per poi crackare `wbr`.)
- **Gotcha**: `sudo -l` ti dice *esattamente* cosa puoi fare come root — è la prima cosa da lanciare
  appena diventi un nuovo utente. Le wildcard e i binari "GTFOBins" (`vi`, `find`, `tee`, editor)
  sono il punto: un binario innocuo diventa arbitrario per come è scritta la regola.

### 3.7 Persistenza / processi nascosti — cron, at, systemd timer (dai lab; NON ancora vettore d'esame)

- **Riconoscere**: non emerge dal diff AIDE su `/usr/bin`+`/etc` standard. Ispezione attiva:
```
systemctl list-timers
atq
crontab -l ; sudo crontab -l ; ls -l /etc/cron.*  /var/spool/cron/
```
- **Sfruttare**: se trovi uno **script eseguito da root** periodicamente e **scrivibile** da te,
  modificalo e attendi che giri per tuo conto (aggiunge un utente, setta un SUID, ecc.).
- **Stato nel pool**: nei 9 esercizi reali questo **non** è mai stato il vettore vincente (in
  13 giu 2024 `/etc/crontab` compare nel diff ma solo come cambio di permessi *ininfluente*, un
  depistaggio). È un ramo dei **lab** (`LAB_Misconfiguration_attacks_e_HIDS`, sez. 8) da conoscere
  per completezza e perché la consegna può dire "più modifiche da dedurre" — ma **non** è dove
  cercare per primo. Segnalato qui come tale, non inventato.

### 3.8 SSH private key / SGID / altri decoy (12 gen 2026)

- **Chiave privata SSH** lasciata leggibile (es. `/etc/backup/id_guest`, `file` → "OpenSSH private
  key") → `ssh -i key utente@localhost` per diventare quell'utente (vettore reale in 12 gen 2026).
- **SGID su directory** per un gruppo di cui non fai parte (es. `/etc/timidity` gruppo root) →
  **vicolo cieco**: il bit ha effetto solo sui file creati dai membri di quel gruppo.

---

## 4. Riferimento comandi — come si costruiscono, non solo cosa copiare

### 4.1 AIDE, pezzo per pezzo

- **`aide.conf`**: le direttive `database_out` (snapshot creato ora), `database_in` (riferimento
  con cui si confronta il filesystem), `database_new` (per confrontare due db tra loro). La regola
  `/percorso  f  Full` dice "sui file sotto questo percorso applica il preset Full" (permessi,
  owner, size, tempi, hash, **xattrs**). ⚠️ **Tre token separati da spazi: `<percorso> f Full`. La
  `f` è un selettore, NON un'opzione: si scrive `f`, mai `-f`** (`/usr/bin -f Full` col trattino non
  seleziona i file → i binari non vengono confrontati). `@@x_include …` (ultima riga) include tutta la conf.d:
  commentalo per velocità e copertura prevedibile.
- **`sudo aideinit`**: crea `database_out`; copia in `database_in` **solo se non esiste**. → copia
  a mano sempre: `sudo cp /var/lib/aide/aide.db.new /var/lib/aide/aide.db`.
- **`sudo aide -C -c /etc/aide/aide.conf`**: modalità Check (filesystem vs `database_in`). Il `-c`
  è obbligatorio anche qui.
- Perché l'ordine è vincolante: AIDE confronta *stato salvato* vs *stato attuale*. Se salvi lo stato
  **dopo** la modifica, la modifica è già "normale" e non viene rilevata.

### 4.2 Leggere una capability / ACL / SUID

```
getcap <file>            # quale capability (vuoto = nessuna effettiva → falso positivo)
getfacl <file>           # ACL: righe user:<nome>:<perm> oltre a owner/group/other
ls -l <file>             # SUID = 's' nel campo utente (-rws...); '+' finale = ACL presente
/usr/sbin/getcap -r / 2>/dev/null      # scoperta a tappeto capability
find / -perm /7000 2>/dev/null         # scoperta a tappeto SUID(4000)/SGID(2000)/sticky(1000)
getfacl -sR / 2>/dev/null              # scoperta a tappeto ACL non standard
```

### 4.3 Formato di /etc/passwd e /etc/shadow (perché gli exploit funzionano)

`/etc/passwd`: **7 campi** separati da `:` → `utente:password:UID:GID:GECOS:home:shell`.
- 2° campo `x` = "password in shadow"; **vuoto** = **nessuna password**; un **hash** inline = quello
  è la password (formato storico ancora accettato).
- **UID 0 = root** a prescindere dal nome. Quindi bastano: campo pw vuoto (o hash noto) + UID/GID 0.
- Riga tipo: `toor::0:0::/root:/bin/bash` (root senza password) oppure
  `hack:$1$hack$xR6zsfvpez/t8teGRRSNr.:0:0:root:/root:/bin/bash` (root con password `hack`).
- ⚠️ **Conta sempre i campi: devono essere 7, quindi 6 `:`.** Un errore facile è omettere la home
  e scrivere `hack:$1$hack$…:0:0:root:/bin/bash` (**6 campi** — è proprio come appare la riga nella
  trascrizione ufficiale di 11 gen 2024 in `modello_integrity_privesc.md`, che è un refuso). Con 6
  campi i valori slittano: `root` finisce nel campo home e `/bin/bash` nel campo shell sbagliato →
  home inesistente e comportamento imprevedibile di `su`. Se il campo GECOS non ti serve, lascialo
  **vuoto** ma tienilo (`hack:$1$hack$…:0:0::/root:/bin/bash`), non eliminarlo.

`/etc/shadow`: `utente:hash:lastchange:…`. Campo hash vuoto = nessuna password. Generare un hash:
```
openssl passwd -1 -salt <salt> <password>     # MD5-crypt ($1$)
openssl passwd -6 -salt <salt> <password>      # SHA-512 ($6$)
openssl passwd <password>                       # salt casuale, algoritmo di default
```

### 4.4 Diventare root — la mossa finale, per vettore

```
su toor                 # dopo aver creato l'utente in passwd
su root                 # dopo aver svuotato/rimosso la password di root in passwd
su <utente>             # dopo aver messo il suo UID a 0
sudo -i  /  sudo su     # dopo esserti concesso una riga sudoers
id                      # PROVA: deve dare uid=0(root) — è lo screenshot da consegnare
```

### 4.5 Distinguere vettore reale da decoy — il ragionamento in una frase

Una modifica è **sfruttabile** solo se combina (a) un **meccanismo che bypassa un controllo** (SUID,
cap_dac_override, cap_dac_read_search, cap_setuid, cap_sys_admin, cap_fowner, ACL di scrittura su
file critico, regola sudoers) con (b) un **bersaglio che controlla l'autenticazione o i privilegi**
(`/etc/passwd`, `/etc/shadow`, `/etc/sudoers`, l'UID). Se manca (a) — capability inutile, ACL su
binario innocuo, falso positivo — o se il bersaglio non porta a root, è un **vicolo cieco**, per
quanto AIDE lo segnali. AIDE trova tutto indiscriminatamente; scegliere è lavoro umano.

**Corollario GTFOBins (vale sia per il SUID §3.1 sia per le capability §3.2, e i due si richiamano a
vicenda).** Quando il "meccanismo (a)" è un **bit SUID** o una **capability** (`cap_setuid`,
`cap_dac_override`, `cap_dac_read_search`) su un **binario che è un interprete/tool con una via di
fuga** (`find`, `python`, `perl`, `bash`, `vim`, `awk`, `less`, `tee`, `cp`…), il "bersaglio (b)"
**non deve** per forza essere `/etc/passwd`: il bersaglio può essere la **shell stessa** (setuid/-p)
o un file arbitrario letto/scritto dal binario. **Perciò, prima di scartare un binario SUID o con
capability come rumore, verifica se è un nome noto in GTFOBins** con una funzione
*Shell*/*Command*/*File read*/*File write* — se sì, è **quasi certamente il vettore reale**. Regola
pratica: `yes`/`whoami`/`sort` = nessuna funzione utile = rumore; `find`/`python`/`bash`/`vim`/`tee`/
`cp` = funzione sfruttabile = vettore. Nei rami §3.1/§3.2 c'è la ricetta; qui il criterio per
decidere se applicarla — senza dover ricordare GTFOBins a memoria.

### 4.6 Perché `| tee`/pipe e MAI `>>` diretto (il punto meccanico da capire, e da saper spiegare a voce)

Con un binario privilegiato (SUID, o con `cap_dac_override`) devi passargli il contenuto **in pipe**
e dargli il file protetto **come argomento** — mai usare la redirezione della shell:
```
echo "toor::0:0::/root:/bin/bash" | sudo /usr/bin/tee -a /etc/passwd   # ✅ è tee che apre /etc/passwd
cat /tmp/passwd | tee /etc/passwd                                      # ✅ (tee con SUID/cap)
echo "toor::0:0::/root:/bin/bash" >> /etc/passwd                       # ❌ Permission denied, SEMPRE
```
**Perché il `>>` fallisce anche se il binario ha la capability/SUID**: `>>` e `>` sono **redirezioni
della shell**. È la **shell** (che gira coi permessi dell'utente `kali`, non privilegiati) ad aprire
il file di destinazione *prima* di lanciare il comando — quindi `/etc/passwd` viene aperto senza
alcun privilegio e l'apertura fallisce con *Permission denied* prima ancora che tee/l'editor parta.
La capability/il SUID vivono sul **binario**, e si attivano **solo quando è il binario stesso ad
aprire il file**. Perciò: il contenuto arriva a `tee` via **pipe** (o stdin) e il file protetto è un
**argomento** di `tee`, così è `tee` — privilegiato — a fare la `open()`.
- Corollario per l'editor (`vim.tiny` con `cap_dac_override`): apri il file *da dentro l'editor*
  (`vim.tiny /etc/passwd`) e salva con `:w!` — è `vim.tiny` ad aprirlo, quindi la cap si applica.
  Non usare `vim.tiny < x > /etc/passwd`.
- Corollario per il SUID `cp` (§3.1): stesso principio, per questo la ricetta è
  `cp fileScrivibile /etc/passwd` (è `cp` ad aprire la destinazione), mai `cat x > /etc/passwd`.

---

## 5. Vettori catalogati (indice rapido) e casi reali

| Vettore | § | Comparso in (casi reali) |
|---|---|---|
| SUID bit (scrive file protetti) | 3.1 | 9 gen 2023; 8 feb 2024 (creato via cap_fowner) |
| SUID su binario-shell (GTFOBins: `find`/`python`/`bash`/`vim`) | 3.1 | variante non ancora nel pool (shell root diretta con `-p`/`setuid`) |
| Capability `cap_dac_override` | 3.2 | 11 gen 2024 (tee), 15 giu 2023 (vim.tiny), 30 ott 2025 (vim.tiny), 12 gen 2026 (vim.tiny) |
| Capability `cap_fowner` | 3.2 | 8 feb 2024 (chmod), 10 lug 2025 (chmod) |
| Capability `cap_setuid` / `cap_dac_read_search` / `cap_sys_admin` | 3.2 | variante non ancora nel pool (setuid→shell diretta; dac_read_search→lettura shadow+john; sys_admin→bind-mount di passwd) |
| Capability inutili (`cap_mknod`, `cap_audit_read`) | 3.2 | 10 lug 2025, 30 ott 2025, feb 2025 (decoy) |
| ACL POSIX (scrittura sudoers/passwd, lettura shadow) | 3.3 | 13 giu 2024 (sudoers), 10 lug/30 ott 2025 (shadow) |
| Utente senza password | 3.4 | 13 giu 2024, 10 lug 2025, 30 ott 2025 |
| Crack password (john offline / hydra online) | 3.5 | 10 lug 2025 (john), 30 ott 2025 (john), feb 2025 (hydra) |
| sudoers permissivo / wildcard | 3.6 | feb 2025 (NOPASSWD tee), 30 ott 2025 (wildcard find) |
| Persistenza cron/at/systemd | 3.7 | solo lab (mai vettore vincente nel pool) |
| Chiave SSH / SGID decoy | 3.8 | 12 gen 2026 |

- `modello_integrity_privesc.md` — 9 casi reali completi (9 gen 2023 → 12 gen 2026), con consegna,
  soluzione trascritta e "perché funziona". Il caso **15 giugno 2023** è l'unico senza soluzione
  ufficiale allegata: è ricostruito per analisi statica del binario e segnalato come tale.
- `procedura_operativa_privesc.md` — algoritmo esteso passo per passo + gotcha AIDE.
- Lab di riferimento: `SLIDE LAB/SICINF/LAB_Esempi_di_misconfiguration_22apr.html` (4 vettori) e
  `LAB_Misconfiguration_attacks_e_HIDS_22apr.html` (AIDE + 4 vettori + persistenza).
