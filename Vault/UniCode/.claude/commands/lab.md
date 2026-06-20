---
description: "Genera la guida-lab operativa per un modulo dai PDF Virtuale (passo 3 del flusso). Uso: /lab <ID>  (es. /lab 3D, /lab S1)"
argument-hint: "ID modulo — SysAdmin: 0A-4C | Security: S1-S15"
---

Il modulo richiesto è: $ARGUMENTS

**Rileva il tipo di modulo dal prefisso dell'ID:**
- ID inizia con `S` → modulo **Security** (lab Kali Linux / Parrot OS)
- ID inizia con cifra → modulo **SysAdmin** (lab Vagrant/Debian)
- ID inizia con `D` → Diritto non ha lab; comunicalo e fermati
- ID vuoto o non riconosciuto → mostra i formati validi e fermati

---

**1. Carica il contesto necessario**

Leggi questi file in parallelo:
- `stato/corrente.md` — verifica che il modulo esista e il suo stato attuale
- `stato/percorso.md` — recupera: nome completo, corso, materiale Virtuale richiesto (PDF TEORIA + PDF LAB), esercizio attivo
- `stato/errori_frequenti.md` — identifica pattern di errore ricorrenti di Lorenzo rilevanti per questo modulo

Se il modulo non esiste nel percorso, comunicalo e fermati.

---

**2. Identifica e verifica i PDF**

Da `percorso.md`, recupera i nomi esatti dei PDF richiesti per questo modulo:
- SysAdmin: cerca in `SLIDE TEORIA/SYSADM/` e `SLIDE LAB/SYSADM/`
- Security: cerca in `SLIDE TEORIA/SICINF/` e `SLIDE LAB/SICINF/`

Verifica che ogni PDF esista su disco. Se uno o più PDF mancano:
**fermati**, elenca i nomi esatti da caricare e chiedi a Lorenzo. Non generare contenuto senza aver letto i PDF.

---

**3. Leggi i PDF**

Leggi integralmente tutti i PDF del modulo — sia teoria che lab.

> **REGOLA CRITICA**: il contenuto della guida-lab deve venire SOLO dai PDF letti in questo passo. I "concetti chiave" in `percorso.md` sono un indice per trovare i PDF, non una fonte da cui generare contenuto. Non inventare esercizi, comandi o output che non siano nei PDF.

---

**4. Genera la guida-lab**

Path: `claudeLezioni/<SOTTOCARTELLA>/guida_lab_modulo$ARGUMENTS_<nome_breve>.md`

Sottocartelle:
- SysAdmin → `LEZIONI SYSADM/`
- Security → `LEZIONI SECURITY/`

`<nome_breve>` = identificatore conciso del contenuto (es. `networking_base`, `enumerazione_nmap`).

---

### Template SysAdmin

```
# Guida Lab — Modulo $ARGUMENTS: <Nome Completo>
**Corso**: Lab Amministrazione di Sistemi T
**Materiale**: <titoli PDF usati>
**VM**: Vagrant + Debian 12 (`cd ~/Progetti/sysAdmin-lab && vagrant up && vagrant ssh`)
**Prerequisiti**: <moduli precedenti rilevanti — verificare ✅ in corrente.md>

---

## Setup

Passi da eseguire prima di iniziare:
1. ...

---

## Esercizi

> Lorenzo digita tutti i comandi. La guida li fornisce, non li esegue.

Per ogni esercizio del LAB PDF, struttura fissa:

### Esercizio N — <Titolo dal PDF>

**Obiettivo**: cosa deve funzionare al termine di questo esercizio.

**Concetto minimo**: cos'è e perché esiste — solo la teoria necessaria per capire cosa stai facendo.
*(Se Lorenzo ha errori ricorrenti su questo concetto: ⚠️ con il pattern specifico da errori_frequenti.md)*

**Comandi**:
```bash
# comando esatto da digitare
```

**Anatomia del comando**: per ogni comando — *cosa stai scrivendo* (cosa fa), *perché lo stai scrivendo* (a cosa serve qui: quale informazione cerchi o quale pezzo dell'esercizio risolve, nella catena «che informazione ho → cosa cerco → quale comando la trova»), *con che parametri* (la funzione di ogni flag/opzione usata) e *come potresti scriverlo* (varianti equivalenti o adattamenti a un caso simile). Serve a saperlo riscrivere a memoria all'esame, non a copiarlo. Spiega solo comandi presenti nei PDF, ma spiega i parametri in modo accurato e completo.

**Output atteso**:
```
# output tipico da confrontare
```

**Cosa verificare**: come sai che ha funzionato.

---

[Progressione: facile → difficile, nell'ordine del PDF]

## Connessioni

- Con il modulo precedente: [connessione SPECIFICA — cita modulo e concetto preciso]
- Con Security: [quale superficie d'attacco introduce — essere precisi]
```

---

### Template Security

```
# Guida Lab — Modulo $ARGUMENTS: <Nome Completo>
**Corso**: Lab Sicurezza Informatica T
**Materiale**: <titoli PDF usati>
**VM**: `LabSicurezzaInformatica` in VirtualBox
**Prerequisiti**: <moduli SysAdmin e Security rilevanti — verificare ✅>

---

## Setup

> ⚠️ **Snapshot obbligatorio** prima di iniziare ogni esercizio di compromissione.

Passi da eseguire prima di iniziare:
1. ...

---

## Threat Model

- **Prospettiva attaccante**: cosa si cerca, perché questa tecnica funziona
- **Prospettiva difensore**: come si rileva, come si mitiga

---

## Esercizi

> Lorenzo digita tutti i comandi. La guida li fornisce, non li esegue.

Per ogni esercizio del LAB PDF, struttura fissa:

### Esercizio N — <Titolo dal PDF>

**Obiettivo**: cosa deve funzionare al termine.

**Concetto**: teoria minima necessaria per capire l'esercizio (attaccante + difensore).

**Comandi**:
```bash
# comando esatto
```

**Anatomia del comando**: per ogni comando — *cosa stai scrivendo* (cosa fa), *perché lo stai scrivendo* (a cosa serve qui: quale informazione cerchi o quale pezzo dell'esercizio risolve, nella catena «che informazione ho → cosa cerco → quale comando la trova»), *con che parametri* (la funzione di ogni flag/opzione usata) e *come potresti scriverlo* (varianti equivalenti o adattamenti a un caso simile). Serve a saperlo riscrivere a memoria all'esame, non a copiarlo. Spiega solo comandi presenti nei PDF, ma spiega i parametri in modo accurato e completo.

**Output atteso**:
```
# output tipico
```

**Cosa verificare**: come sai che ha funzionato.

---

[Progressione: dall'esercizio più semplice al più complesso, nell'ordine del PDF]

## Famiglia d'esame

*(Solo se il modulo è ⭐ — altrimenti ometti questa sezione)*

Tipologia: <nome tipologia d'esame>
Prova passata correlata: `SIMULAZIONI ESAMI/SICINF/<file>` — eseguila al termine del lab.
```

---

**5. Verifica qualità (checklist interna)**

Prima di comunicare il risultato, verifica che la guida rispetti il checklist "Guida-lab" in `UniCode/CLAUDE.md`:
- [ ] Ancorata ai PDF reali: nessun contenuto inventato, [fonte: PDF] dove serve
- [ ] Setup esplicito: VM corretta, snapshot (Security) o vagrant up (SysAdmin)
- [ ] Ogni passo: comando esatto + output atteso + cosa verificare
- [ ] Ogni comando ha l'**anatomia**: cosa fa, perché lì (a cosa serve nel flusso), funzione dei parametri, varianti (saperlo riscrivere, non copiare)
- [ ] Security: threat model (attaccante E difensore)
- [ ] Progressione facile → difficile, ordine del PDF
- [ ] Errori frequenti di Lorenzo integrati come ⚠️ dove rilevanti
- [ ] Se ⭐: collegamento a tipologia d'esame + rimando a prova passata
- [ ] Lorenzo digita i comandi: la guida non li esegue al suo posto

Se un punto non è soddisfatto, correggi prima di procedere.

Poi invoca la skill `lorenzo-skills:unicode-output-gate` per la verifica finale.

---

**6. Collega la nota al grafo**

Invoca la skill `lorenzo-skills:unicode-link-note` per scrivere il blocco AUTO-LINKS (fratelli + hub) della guida-lab.

---

**7. Aggiorna lo stato**

In `stato/corrente.md`: segna il modulo come 🔄 se era ⬜.

---

**8. Comunica il risultato**

- Path del file creato
- Indica di aprire la VM e seguire gli esercizi nell'ordine della guida
- Se sono stati integrati avvertimenti da errori_frequenti.md, menzionarlo brevemente
