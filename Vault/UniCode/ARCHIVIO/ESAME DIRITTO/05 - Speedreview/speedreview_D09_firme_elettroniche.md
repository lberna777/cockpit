# Speed Review — D9: Firme Elettroniche e Documenti Informatici

> La prof ha segnato esplicitamente i temi prioritari (slide 66-67). Il quiz colpisce su: gerarchia firme, certificato qualificato, valore nel tempo, macroistruzioni, PEC.

---

## 1. Documenti e prova (codice civile)

| Tipo | Articolo | Valore probatorio |
|------|----------|-------------------|
| **Atto pubblico** | 2699 | Redatto da pubblico ufficiale; **pubblica fede**, contestabile solo con querela di falso |
| **Scrittura privata** | 2702 | Piena prova della provenienza se **non disconosciuta** o autenticata |
| **Riproduzioni meccaniche** | 2712 | Piena prova se la conformità **non è disconosciuta** (include doc. informatici) |

- Quadro normativo: c.c., **L. 59/1997 (Bassanini)** prima a riconoscere validità doc. informatici, **CAD** (D.Lgs. 82/2005), **eIDAS** (Reg. 910/2014), regole tecniche, Linee Guida AGID.

---

## 2. Firma digitale — meccanismo

- **Crittografia asimmetrica** (chiave **pubblica** + **privata**). Il mittente firma con la **privata**, il destinatario verifica con la **pubblica**.
- Applicata all'**impronta** (hash) del documento, non all'intero file.
- **Certificatore** (terza parte fidata): verifica l'identità, la associa alla chiave pubblica, emette il **certificato**, pubblica revoche/sospensioni nelle liste.

---

## 3. Gerarchia delle firme elettroniche (eIDAS) — IL CUORE

| Tipo | Definizione | Valore giuridico |
|------|-------------|------------------|
| **Firma elettronica (semplice)** | Dati elettronici acclusi/connessi usati per firmare | Non negati effetti né ammissibilità come prova |
| **Firma elettronica avanzata** | Connessa **unicamente** al firmatario, sotto suo **esclusivo controllo**, identifica ogni modifica | **Scrittura privata** (art. 2702) |
| **Firma elettronica qualificata** | Avanzata + **dispositivo qualificato** + **certificato qualificato** | **Equivalente a firma autografa** |
| **Firma digitale** | Tipo specifico di qualificata (italiana), basata su chiavi crittografiche (CAD art. 1) | **Equivalente a firma autografa** |

- **Modalità operative** di qualificata/digitale: **automatica** (senza presidio continuo), **remota** (su HSM), **autenticata** (da notaio/pubblico ufficiale).

### Valore del documento informatico (CAD art. 20)
- Soddisfa la **forma scritta** + efficacia di **scrittura privata** se ha firma **digitale, qualificata o avanzata**, oppure è formato con identificazione informatica + sicurezza/integrità/immodificabilità.
- In **tutti gli altri casi**: idoneità e valore probatorio **liberamente valutabili in giudizio**.

### ⚠️ Macroistruzioni (art. 4 c.3 reg. tecn.)
Il documento con firma qualificata/digitale **NON** soddisfa l'immodificabilità se contiene **macroistruzioni, codici eseguibili** (macro, script PDF, JavaScript) che possono modificarlo.

---

## 4. Certificato qualificato e validità nel tempo

- **Certificato qualificato**: rilasciato da **prestatore di servizi fiduciari qualificato** (conforme allegato I eIDAS); contiene nome firmatario, validità, limiti d'uso.
- **Revoca** (definitiva) / **sospensione** (temporanea): hanno **effetto dalla pubblicazione** nella lista.
- Firma su certificato **revocato/scaduto/sospeso** = **mancata sottoscrizione**.
- **MA**: la firma qualificata/digitale resta **valida** se associata a un **riferimento temporale opponibile ai terzi** che la colloca **prima** della scadenza/revoca (art. 62 reg. tecn.).
- **Marca temporale** / **riferimento temporale**: provano che il documento esisteva in un certo momento. La **PEC** costituisce validazione temporale.

### PEC (DPR 68/2005)
- Trasmissione via PEC = **notificazione a mezzo posta**. Data e ora **opponibili ai terzi**.

### Sigillo elettronico (eIDAS art. 3)
- Equivalente della firma ma per le **persone giuridiche** (non fisiche). Garantisce **origine e integrità**.

---

## ⚠️ Trappole MC

- **Firma qualificata** = avanzata + **dispositivo qualificato** + **certificato qualificato** (entrambi). NON "requisiti più stringenti" generici; NON "dispositivo certificato".
- Valore: avanzata → **scrittura privata**; qualificata/digitale → **firma autografa**. Il quiz scambia i livelli.
- **Firma digitale** = sottotipo di **qualificata** (non un livello superiore separato).
- Documento con **macro/codice eseguibile** → NON immodificabile (anche con firma qualificata).
- Firma su certificato revocato = **mancata sottoscrizione**, salvo **riferimento temporale opponibile** che la colloca prima.
- Revoca/sospensione: effetto dalla **pubblicazione**.
- **PEC** = notificazione a mezzo posta; data/ora opponibili ai terzi.
- **Sigillo** = persone giuridiche; **firma** = persone fisiche.
- Atto pubblico (pubblica fede) ≠ scrittura privata (prova se non disconosciuta).

---

## Da aggiungere dopo le simulazioni:

<br><br><br>
