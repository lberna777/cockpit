---
description: "Crea la lezione strutturata per un modulo dai PDF Virtuale. Uso: /lezione <ID>  (es. /lezione 3A, /lezione D1, /lezione S4)"
argument-hint: "ID modulo — SysAdmin: 0A-4C | Security: S1-S15 | Diritto: D1-D13"
---

Il modulo richiesto è: $ARGUMENTS

**Rileva il tipo di modulo dal prefisso dell'ID:**
- ID inizia con `D` → modulo **Diritto** (teoria, nessuna VM)
- ID inizia con `S` → modulo **Security** (lab Kali Linux)
- ID inizia con cifra → modulo **SysAdmin** (lab Vagrant/Debian)
- ID vuoto o non riconosciuto → mostra i formati validi e fermati

---

**1. Carica il contesto necessario**

Leggi questi file in parallelo:
- `stato/corrente.md` — verifica che il modulo esista e il suo stato attuale
- `stato/percorso.md` — recupera: nome completo, corso, materiale Virtuale richiesto, concetti chiave, esercizio attivo, connessioni
- `stato/errori_frequenti.md` — identifica pattern di errore ricorrenti di Lorenzo rilevanti per questo modulo (es. se sta facendo un modulo bash e ha pattern di errori di sintassi, enfatizzare quei punti)

Se il modulo non esiste nel percorso, comunicalo e fermati.

---

**2. Verifica i PDF**

Cerca i PDF in base al tipo di modulo:
- SysAdmin: `SLIDE TEORIA/SYSADM/` e `SLIDE LAB/SYSADM/`
- Security: `SLIDE TEORIA/SICINF/` e `SLIDE LAB/SICINF/` (se esistono)
- Diritto: `SLIDE TEORIA/DIRITTO INFORMATICO/`

Usa **solo i PDF assegnati al modulo in `percorso.md`** — non riclassificare i materiali di tua iniziativa, non attingere a PDF di altri moduli. Se uno o più PDF richiesti mancano: **fermati**, elenca i nomi esatti da caricare e chiedi a Lorenzo. Non creare contenuto senza il PDF corrispondente.

---

**3. Leggi i PDF**

Leggi integralmente tutti i PDF rilevanti. Per PDF molto lunghi (>50 pagine), leggi per sezioni e identifica le parti pertinenti al modulo.

> **REGOLA CRITICA**: il contenuto della lezione deve venire SOLO dai PDF letti in questo passo. I "concetti chiave" in percorso.md sono un indice per sapere quali PDF cercare — NON sono una fonte da cui generare contenuto. Se non hai letto il PDF, non puoi creare la lezione. Contenuto generato senza leggere il PDF è superficiale e inaccettabile. Non inventare comandi/strumenti che non sono nei PDF.

---

**FORMATO della lezione (Security e SysAdmin)** — vincolante, da feedback di Lorenzo:

La lezione è **prosa discorsiva ancorata ai comandi/file concreti** dell'argomento, NON un walkthrough.
- **Prosa scorrevole**, non tabelle/elenchi a raffica. Si legge la sera prima.
- **Organizzata attorno ai comandi/file concreti** dell'argomento, usati come ganci per spiegare la teoria.
- Per ogni comando/file, **due livelli**: *cosa c'è dietro in piccolo* (il meccanismo) + *la visione d'insieme in grande* (dove si inserisce, perché esiste, superficie d'attacco/difesa).
- **NON è un walkthrough**: niente sequenza "passo 1 → passo 2 → output atteso", niente anatomia parametro-per-parametro. Quella è la **guida-lab** (`/lab`). La lezione spiega *perché*; la guida-lab dice *come, passo passo*.

> Confine col walkthrough: se stai scrivendo "esegui questo, poi quello, output X" → è materia di `/lab`, non della lezione.

---

**4. Crea il file lezione**

Path: `/home/lorenzo/UniCode/claudeLezioni/<SOTTOCARTELLA>/lezione_modulo$ARGUMENTS_<nome_breve>.md`

Sottocartelle:
- SysAdmin → `LEZIONI SYSADM/`
- Security → `LEZIONI SECURITY/`
- Diritto → `LEZIONI DIRITTO/`

`<nome_breve>` = identificatore conciso del contenuto (es. `systemd_servizi`, `diritto_autore`).

---

### Template SysAdmin (ID numerico)

```
# Lezione — Modulo $ARGUMENTS: <Nome Completo>
**Corso**: Lab Amministrazione di Sistemi T
**Materiale**: <titoli PDF usati>
**Prerequisiti**: <moduli precedenti rilevanti — verificare che siano ✅ in corrente.md>

---

## Obiettivo
Una frase: cosa Lorenzo deve saper fare al termine.

## [Sezioni ancorate ai comandi/file chiave] — in prosa

Una sezione per ogni comando o file concreto centrale del modulo (es. `systemctl`, `/etc/fstab`).
Per ciascuno, in prosa discorsiva:
- **cosa fa** (il gesto pratico)
- **cosa c'è dietro** (il meccanismo, in piccolo)
- **la visione** (dove si inserisce, perché esiste, e quale superficie verso Security introduce)
*(Se Lorenzo ha errori ricorrenti su questo da errori_frequenti.md: ⚠️ con il pattern specifico.)*

> NON mettere qui la sequenza di esecuzione passo-passo né l'anatomia parametro-per-parametro: quella è la guida-lab (`/lab`).

## Connessioni
- Con il modulo precedente: [connessione SPECIFICA, non generica]
- Con Security: [quale superficie d'attacco introduce — essere precisi]

## Riepilogo
3 concetti chiave in forma di domanda-risposta (non lista passiva)
```

---

### Template Security (prefisso S)

```
# Lezione — Modulo $ARGUMENTS: <Nome Completo>
**Corso**: Lab Sicurezza Informatica T
**Materiale**: <titoli PDF usati>
**Prerequisiti**: <moduli SysAdmin e Security rilevanti — verificare che siano ✅>
**Nota esame**: conta per il **quiz teorico (40%)** (oltre alla pratica 60%); c'è penalità per risposta sbagliata — segnalalo dove serve.

---

## Come leggere questa lezione
1-2 frasi: l'argomento ridotto ai pochi posti concreti (file/comandi) che faranno da gancio.

## La visione d'insieme / threat model
In prosa: il quadro grande, con **prospettiva attaccante** (perché l'attacco funziona, cosa cerca) e **difensore** (come si rileva, come si mitiga). Scenario reale se presente nel PDF.

## [Sezioni ancorate ai comandi/file chiave] — in prosa

Una sezione per ogni comando o file concreto centrale (es. `nmap`, `/etc/shadow`, `/etc/pam.d/`).
Per ciascuno, in prosa discorsiva:
- **cosa fa** (il gesto)
- **cosa c'è dietro** (il meccanismo, in piccolo)
- **la visione** (dove si inserisce, perché esiste, superficie d'attacco/difesa, gancio col tema d'esame)
*(⚠️ errori ricorrenti da errori_frequenti.md dove rilevante.)*

> NON la sequenza eseguibile né l'anatomia parametro-per-parametro: quella è la guida-lab (`/lab`).

## Connessioni
- Con SysAdmin: [quale configurazione errata viene sfruttata — SPECIFICO]
- Con moduli Security precedenti/successivi: [catena logica]

## Domande di autoverifica (stile quiz teorico)
3-5 domande vero/falso o a scelta multipla, come all'esame. Avvisa: se non sei sicuro, all'esame non rispondere (penalità).
```

---

### Template Diritto (prefisso D)

> **Regola vincolante**: l'esame verte sugli argomenti e spiegazioni del PDF della professoressa. Le definizioni devono rispecchiare il linguaggio del PDF — non riformulare, non parafrasare, non integrare con fonti esterne. Segnalare con `[fonte: PDF]` ogni affermazione tratta dalle slide. Registro accademico-giuridico. Usare paragrafi discorsivi dove il PDF lo fa.

```
# Lezione — Modulo $ARGUMENTS: <Nome Completo>
**Corso**: Diritto dell'Informatica T
**Materiale**: <titolo PDF usato>
**Normative di riferimento**: <leggi e decreti citati nel PDF, con estremi completi>

---

## Obiettivo
Una frase: quale istituto giuridico Lorenzo deve saper spiegare, nelle parole della professoressa.

## Quadro Normativo
Norme di riferimento con estremi completi. Solo quelle presenti nel materiale.

## Concetti Chiave
Per ogni concetto:
- Definizione ripresa fedelmente dal PDF [fonte: PDF]
- Ratio legis se spiegata dalla professoressa
- Esempi usati nelle slide
- Se Lorenzo ha pattern di errore su questo tipo di concetto (da errori_frequenti.md): aggiungere nota esplicita "⚠️ Attenzione: in passato hai confuso X con Y"

## Riferimenti Normativi
| Articolo / Norma | Contenuto (come descritto nel PDF) | Rilevanza per il corso |
|------------------|------------------------------------|------------------------|

## Casi e Scenari
Situazioni concrete dalla professoressa. Se non presenti nel PDF, omettere.

## Domande di Autoverifica
Cinque domande aperte del tipo che la professoressa potrebbe fare all'esame.
Almeno una domanda deve testare le distinzioni che Lorenzo tende a fondere (pattern da errori_frequenti.md).
1. ...
2. ...
3. ...
4. ...
5. ...

## Riepilogo
Tre concetti normativi centrali, formulati come nel PDF.
```

---

**5. Verifica qualità (checklist interna)**

Prima di comunicare il risultato, verifica:
- [ ] Ogni concetto nel PDF è stato coperto nella lezione
- [ ] Security/SysAdmin: **prosa discorsiva ancorata ai comandi/file**, ogni comando spiegato a due livelli (meccanismo + visione) — NON un walkthrough, niente sequenza passo-passo né anatomia parametri (quella è `/lab`)
- [ ] Security: threat model chiaro (attaccante E difensore); domande di autoverifica in stile quiz
- [ ] Diritto: ogni definizione usa la terminologia esatta del PDF, `[fonte: PDF]` dove serve
- [ ] Le connessioni sono specifiche (citano moduli e concetti precisi)
- [ ] Pattern di errore di Lorenzo integrati come avvertimenti ⚠️
- [ ] Nessun comando/strumento inventato fuori dai PDF

Se una checklist non è soddisfatta, correggi prima di procedere. Poi invoca `lorenzo-skills:unicode-output-gate` per la verifica finale.

---

**6. Collega la nota al grafo**

Invoca la skill `lorenzo-skills:unicode-link-note` per scrivere il blocco AUTO-LINKS (fratelli + hub) della nuova lezione.

---

**7. Aggiorna lo stato**

In `stato/corrente.md`: segna il modulo come 🔄 se era ⬜.

---

**8. Comunica il risultato**

- Path del file creato
- Per Security/SysAdmin: indica di leggere la lezione; l'esecuzione sulla VM è la **guida-lab** (`/lab <ID>`), passo separato del flusso
- Per Diritto: indica di leggere la lezione e rispondere alle domande di autoverifica prima di scrivere gli appunti grezzi
- Se sono stati integrati avvertimenti da errori_frequenti.md, menzionarlo brevemente
