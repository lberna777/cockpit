# Metodo di Studio — Esami Pratici (Sicurezza + Amministrazione di Sistemi)

> Definito il 2026-06-18 dopo l'analisi dei due corsi su Virtuale.
> Vale per **Lab Sicurezza Informatica T** (17/07) e **Lab Amministrazione di Sistemi T** (rimandato a 08/09).
> Per Diritto (chiuso, 30L) vale il metodo separato (lettura → autoverifica → appunti → quiz MC).

---

## Principi comuni (entrambi gli esami)

1. **Esame pratico sui PC del lab.** Si scrivono script / si configura il sistema, in presenza.
   Non sono scritti su carta. → la conoscenza utile si forma **eseguendo**, non leggendo.
2. **La VM è il deliverable #1.** L'ambiente di esame è a tua cura, senza tempo extra in sede.
   La VM (Parrot/Kali per Security, Ubuntu/Vagrant per Sistemi) deve funzionare end-to-end
   PRIMA di studiare i contenuti. Snapshot prima di ogni esercizio distruttivo/di compromissione.
3. **Unità di "fatto" = eseguito sulla VM.** Un modulo non è ✅ se non hai eseguito tu il LAB.
   Leggere il PDF senza aprire la VM vale ~0 ai fini dell'esame.
4. **Le prove passate sono la bussola.** Per esami così, il modo più efficiente è *exam-driven*:
   si studia VERSO le prove, non si "copre il programma" in modo uniforme.
5. **Studio attivo con dubbi inline** (come per Diritto): annota comandi + output + domande negli
   appunti grezzi durante l'esecuzione; poi `/lezione` o `/appunti` consolidano.

---

## Anatomia di una sessione di studio pratica (flusso vincolante)

Diverso da Diritto (leggi → autoverifica → appunti). Per i lab:

1. **APRI** — `corrente.md` è già in contesto; si sceglie il modulo/famiglia del giorno.
2. **SETUP** — avvia la VM; snapshot (solo Security).
3. **GUIDA + ESEGUI** — Claude prepara una **guida al lab costruita dai materiali Virtuale**
   del modulo (LAB PDF + teoria): walkthrough con comandi da digitare, **l'anatomia di ogni
   comando** (cosa fa, perché lì, funzione dei parametri, come riscriverlo a memoria), output atteso dopo ogni
   passo, cosa verificare. **Lorenzo digita sempre i comandi di persona** (Claude NON pilota la
   VM). Lorenzo annota comandi/output/dubbi nei grezzi.
4. **CONSOLIDA** — Claude trasforma l'esecuzione in lezione (prospettiva attaccante + difensore).
5. **DRILL** — se famiglia ⭐: prova d'esame passata, dal vivo, cronometrata.
6. **CHIUDI** — aggiorna `corrente.md` / `errori_frequenti.md`; snapshot finale.

> Il passo 3 è la versione "per fare" delle lezioni di Diritto: stessa idea (guida dai materiali),
> forma operativa (walkthrough eseguibile invece di testo da leggere).

**Vincolo (regola CLAUDE.md):** la guida del passo 3 si genera SOLO dai PDF reali del modulo,
mai inventata né derivata da `percorso.md`/master map → **i materiali vanno scaricati prima**.

**Comandi:** il flusso NON è un comando. Dentro il flusso nasceranno comandi specifici, creati
gradualmente; è compito di Claude pensarli e proporli. Lorenzo scrive sempre i comandi shell di persona.
- *Primo candidato proposto*: un comando che, dato un modulo, legge i suoi PDF Virtuale e produce
  la guida-lab del passo 3 (una "/lezione" in forma di walkthrough operativo).
- **Gate di qualità**: ogni guida-lab passa per la skill `unicode-output-gate` e il checklist
  "Guida-lab" in `UniCode/CLAUDE.md` prima di essere considerata completa — come per le lezioni di Diritto.

---

## Security — metodo "lab-first guidato dal blueprint"

**Blueprint d'esame**: prova pratica = **3 esercizi tra 5 tipologie**. Tutto ruota attorno a queste:

1. ⭐ **Iptables/NFTables** (Firewall)
2. ⭐ **Web vulnerabilities** (OWASP)
3. ⭐ **Network Intrusion Detection** (Suricata)
4. ⭐ **Integrity check & privilege escalation** (Misconfiguration/HIDS, Pentesting target)
5. ⭐ **Binary exploitation** (buffer overflow)

### Loop per ogni famiglia ⭐
1. **PDF in scorrimento** — solo per il threat model (cosa attacco/difendo, perché). No studio profondo.
2. **Esegui il LAB sulla VM** (snapshot prima) — annota comandi, output, dubbi negli appunti grezzi.
3. **`/lezione`** consolida con doppia prospettiva attaccante + difensore (regola del CLAUDE.md).
4. **Esegui dal vivo una prova d'esame passata di quella tipologia, cronometrata** ← il vero test.
5. **Lacune → drill mirato**, poi rifai la prova.

### Ordine consigliato (dal più self-contained al più tosto)
`Iptables → Web vuln → NIDS Suricata → Integrity/privesc → Binary exploitation`
Binary exploitation (buffer overflow x86_32) per ultimo: è il più duro, ma va affrontato entro
**fine giugno** per avere tempo di consolidarlo (rischio #3 del piano).

### Materiale "contesto" (NON drill)
Autenticazione, Sicurezza fisica/cloud, Demoni, Offensive net sec (sniff/spoof/DoS),
Crittografia (cifrari, gpg, chiavi): **passata teorica leggera**, niente LAB drill — salvo che una
prova passata lo richieda esplicitamente.

---

## Amministrazione di Sistemi — metodo "exam-driven, fase di chiusura"

Sei già avanti su scripting e gestione sistema. Due priorità:

### 1. Chiudere il residuo (in ordine)
- **3D** Networking di base (es. 2-6) → 3E Vagrant multi-machine → 3F Ansible
- **4A** Servizi base rete (DHCP, router via Ansible)
- ⚠️ **4B SNMP / Monitoraggio centralizzato** e **4C LDAP / Configurazione centralizzata**:
  questi due partono **da zero** (mai mappati, mai scaricati, mai studiati) e sono **d'esame**
  (esercizi netmon/SNMP e autenticazione LDAP nelle prove). Priorità alta, non rimandabili.

### 2. Ciclo prove passate (il cuore della preparazione)
1. Una prova a **freddo, cronometrata**.
2. Confronto con la soluzione ufficiale.
3. Estrai i pattern mancanti — inclusi i **tuoi errori noti**: spazi nei test `[ ]`,
   logica invertita (da `errori_frequenti.md`).
4. Drill mirato, poi prova successiva.
- Sfrutta la prova **9 luglio 2025 con video-spiegazione** come worked example iniziale.

---

## Codici modulo vs ordine di studio (deciso 18/06)
- I **codici `S<N>` / `<C>` (0A…4C)** sono identità stabili in **ordine di corso** (servono alla
  convenzione dei nomi file e al grafo). NON si riordinano: si estendono (Security → S13–S15;
  SysAdmin → 4A–4C).
- L'**ordine di studio** è separato e guidato dalle 5 famiglie d'esame (Security) / dal residuo +
  prove passate (SysAdmin). Vive qui, non nei codici.

## Stato VM (verificato 18/06 via VBoxManage)
- **Security**: VM `LabSicurezzaInformatica` (Debian 64-bit, 8 GB, 4 CPU) — **esiste**, spenta,
  **zero snapshot**. ⚠️ Creare snapshot "baseline pulita" appena verificato boot + tool + rete
  host-only. Resta da confermare che funzioni end-to-end (boot + nmap/suricata/gcc + rete).
- **SysAdmin**: 2 VM Vagrant `sysAdmin-lab_default_*` (512 MB, una probabile doppione) +
  `platform-master_default` (1 GB). Gestite da Vagrant.

## Decisioni ancora aperte
- **Security**: confermare end-to-end la VM (boot + tool) e creare lo snapshot baseline.
  (L'ordine di studio SysAdmin è irrilevante — moduli indipendenti.)

## Collegamenti
- Piano fasi e date: [[ESAMI SCELTI]]
- Stato moduli: [[stato/corrente]]
- Errori ricorrenti da intercettare: [[stato/errori_frequenti]]
