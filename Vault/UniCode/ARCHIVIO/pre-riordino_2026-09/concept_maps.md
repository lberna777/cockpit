# Mappe Concettuali — Lab Amm. di Sistemi T

> **Come usare**:
> - **Obsidian**: apri questo file → i diagrammi vengono renderizzati inline
> - **VS Code**: estensione "Markdown Preview Mermaid Support" (gratuita)
> - **Screenshot → iPad**: apri in Obsidian, screenshot del diagramma per studio offline
>
> Colori: 🟢 concetti SysAdmin | 🔴 connessioni con Lab Sicurezza Informatica T

---

## Panoramica — Dipendenze tra Blocchi

```mermaid
graph TD
  B0["BLOCK 0\nFilesystem · Pipe · Filtri"]
  B1["BLOCK 1\nBash Scripting"]
  B2["BLOCK 2\nUtenti · Permessi · File"]
  B3["BLOCK 3\nServizi · Pacchetti · Processi"]
  SEC["⚔ Lab Sicurezza T\nKali / Parrot OS"]

  B0 -->|prerequisito| B1
  B0 -->|prerequisito| B2
  B1 -->|automazione| B2
  B2 -->|prerequisito| B3
  B0 -.->|stesso filesystem| SEC
  B1 -.->|scripting offensivo| SEC
  B2 -.->|modello privilegi| SEC
  B3 -.->|superficie d'attacco| SEC

  style B0 fill:#3fb950,color:#000,stroke:#2f9e44
  style B1 fill:#3fb950,color:#000,stroke:#2f9e44
  style B2 fill:#3fb950,color:#000,stroke:#2f9e44
  style B3 fill:#3fb950,color:#000,stroke:#2f9e44
  style SEC fill:#f85149,color:#fff,stroke:#a40e26
```

---

## Block 0 — Fondamenta Linux

### 0A: Filesystem e Navigazione

```mermaid
graph LR
  A["/  root del filesystem"] --> B["/etc  configurazione"]
  A --> C["/home  utenti"]
  A --> D["/var  log e dati variabili"]
  A --> E["/proc  processi in memoria"]
  A --> F["/tmp  temporanei"]

  B --> G["file .conf\nfile .d/ frammentati"]
  D --> H["/var/log/auth.log\n/var/log/syslog\n/var/log/btmp"]

  C --> I["chmod · permessi\nrwx = 4+2+1"]
  I --> J["owner / group / others\n3 blocchi separati"]
  J --> K["644 file normale\n755 script/dir\n700 privato"]

  H -.->|forensics / analisi| SEC["⚔ Security\nlog analysis"]
  K -.->|misconfigurazioni| PRIV["⚔ Security\nprivilege escalation"]

  style SEC fill:#f85149,color:#fff,stroke:#a40e26
  style PRIV fill:#f85149,color:#fff,stroke:#a40e26
```

### 0B: Pipe, Redirect e Filtri

```mermaid
graph LR
  A["flussi\nstdin · stdout · stderr"] --> B["redirect\n> >> < 2> 2>&1"]
  A --> C["pipe  |"]
  C --> D["grep\n-c -n -v -i"]
  C --> E["sort | uniq -c\nwc -l\ncut -d: -f1"]

  D -.->|filtrare output tool| SEC["⚔ Security\nanalisi output Nmap\nanalisi log Suricata"]
  E -.->|pipeline su grandi dataset| SEC

  style SEC fill:#f85149,color:#fff,stroke:#a40e26
```

---

## Block 1 — Bash Scripting

```mermaid
graph TD
  S["Script Bash\n#!/bin/bash"] --> V["Variabili\nVAR=val · $VAR · ${#VAR}"]
  S --> A["Argomenti\n$1 $2 $# $@"]
  S --> C["Condizioni\nif [ ] · operatori\n-eq -gt -f -d -z"]
  S --> L["Loop\nfor · while\n$() · $(())"]

  V --> F["Funzioni\nnome() { }\nlocal · return · $?"]
  C --> CS["case $VAR in\np) ;; esac"]
  C --> OP["[[ ]] doppie\n&& · || dentro"]

  F -.->|script enum automatizzata| SEC["⚔ Security\nscanning loop su IP\nreazione per porta"]
  CS -.->|branch per tipo risposta| SEC
  OP -.->|filtrare output nmap/netstat| SEC

  style SEC fill:#f85149,color:#fff,stroke:#a40e26
```

---

## Block 2 — Utenti, Permessi e File

### 2A/2B: Modello Utenti e Permessi

```mermaid
graph TD
  U["Modello utenti\nUID · GID\n/etc/passwd · /etc/shadow"] --> G["Gruppi\ngroupadd · usermod -aG"]
  U --> PRIV["Privilegi elevati\nsudo · /etc/sudoers\n/etc/sudoers.d/"]

  G --> DIR["Directory condivisa\nchown root:gruppo\nchmod 770"]
  DIR --> SGID["SGID bit  2xxx\nfile ereditano gruppo dir"]
  SGID --> UMASK["umask 0002\nfile creati: 664\nscrivibili dal gruppo"]

  U --> PERM["chmod rwx\n644 755 700 777\nu+x g-w o-r a+r"]
  PERM --> SPECIAL["Bit speciali\nSUID 4xxx → gira come owner\nSGID 2xxx → gira come gruppo\nSticky 1xxx → solo owner cancella"]

  PRIV -.->|sudo -l = prima mossa attaccante| SEC_PRIV["⚔ Security\nPrivilege Escalation\nsudo NOPASSWD: ALL"]
  SPECIAL -.->|SUID su binari = vettore| SEC_SUID["⚔ Security\nSUID exploitation\nfind / -perm -4000"]
  U -.->|/etc/shadow leggibile = critico| SEC_HASH["⚔ Security\nhash offline\njohn · hashcat"]

  style SEC_PRIV fill:#f85149,color:#fff,stroke:#a40e26
  style SEC_SUID fill:#f85149,color:#fff,stroke:#a40e26
  style SEC_HASH fill:#f85149,color:#fff,stroke:#a40e26
```

### 2C: Gestione File

```mermaid
graph LR
  A["find\nwhere criteria action"] --> B["-name -type -size\n-mtime -user -perm"]
  B --> C["-exec {} \\;\n-delete -ls"]

  D["tar\nc · x · t · v · p · f"] --> E["czf gzip\ncjf bzip2\ncJf xz"]
  E --> F["tar -C /dst -xvpf archive\npipeline: tar cf - | tar -C /dst -xvpf -"]

  G["rsync -av /src/ /dst/"] --> H["solo le differenze\n-a = ricorsivo + permessi"]

  I["dd if=/dev/zero of=file\nbs=4k count=N"] --> J["riserva spazio su disco\nbyte zero senza dati"]

  K["fuser file\nlsof file\nlsof -p PID"] --> L["chi ha il file aperto?\nperché non posso smontare?"]
```

---

## Block 3 — Servizi e Storage

### 3A: Systemd e Pianificazione

```mermaid
graph TD
  INIT["PID=1 — init\nevoluzione: SysVinit → Upstart → Systemd"] --> UNIT["Unit systemd\n.service .socket .timer\n.target .mount .slice"]
  UNIT --> SCTL["systemctl\nstart stop restart reload\nstatus enable disable mask"]
  UNIT --> TGT["Target\nmulti-user.target\ngraphical.target\nrescue.target"]
  UNIT --> LOG["journalctl\n-u servizio\n-f follow\n--since"]

  SCTL --> ENUM["list-units -t service\nlist-unit-files --state=enabled\n--state=failed"]
  
  SCHED["Pianificazione"] --> AT["at\nesecuzione una-tantum\natq · atrm"]
  SCHED --> CRON["cron / crontab\n*/10 8-18 * * 1-5 cmd\ncrontab -e · -l"]

  ENUM -.->|inventario servizi attivi| SEC_SURF["⚔ Security\nattack surface\nNmap enumera questi"]
  CRON -.->|cron usato per persistenza| SEC_PERS["⚔ Security\npersistenza post-exploit\nbackdoor schedulata"]

  style SEC_SURF fill:#f85149,color:#fff,stroke:#a40e26
  style SEC_PERS fill:#f85149,color:#fff,stroke:#a40e26
```

### 3B: Gestione Pacchetti

```mermaid
graph LR
  A["Software lifecycle\ninstall → update → remove"] --> B["Pacchetto .deb\nbinario precompilato\n+ metadati + dipendenze"]
  B --> C["dpkg basso livello\n-i -r -P -l -L -S -s"]
  B --> D["apt alto livello\nupdate install remove\npurge autoremove search"]
  
  D --> R["Repository\n/etc/apt/sources.list\n/etc/apt/trusted.gpg.d/"]
  R --> SIG["Firma GPG\nISO → keyring → apt verify\nfiliera di fiducia"]

  C --> LDD["ldd /path/binario\nlibrerie dinamiche .so"]

  SIG -.->|aggiungere repo non fidati = rischio| SEC_SC["⚔ Security\nSupply chain attacks\npacchetti compromessi"]
  LDD -.->|dipendenze = vettori di attacco| SEC_SC

  style SEC_SC fill:#f85149,color:#fff,stroke:#a40e26
```

---

## Come aggiungere Wikilinks in Obsidian

Per attivare il **Graph View** in Obsidian, aggiungi nei tuoi appunti i link tra note:

```markdown
# Negli appunti di un modulo — esempio
Vedi [[glossario_sysadm#chmod]] per la sintassi ottale.
Connessione con [[concept_maps#block-2]] per il quadro d'insieme.
```

Ogni `[[collegamento]]` diventa un nodo nel grafo di Obsidian — senza spostare né riscrivere il contenuto esistente.
