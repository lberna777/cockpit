# Esercizio 01 — Conta Estensioni (Top 5)

**Modulo**: 0B — Pipe, Redirect e Filtri  
**Data**: 2026-05-11  
**Difficoltà**: intermedio

---

## Obiettivo

Dato un direttorio (con sottodirettori), contare quante volte appare ciascuna estensione di file e mostrare le 5 più frequenti.

**Definizione di estensione**: la stringa che segue l'**ultimo** carattere punto nel nome del file.  
Esempio: `my.example.c` → estensione `c` (non `example`).

**Comandi da usare**: `ls -R`, `rev`, `cut`, `grep`, `sort`, `uniq`, `head`

---

## Pipeline Finale

```bash
ls -R 2>/dev/null | grep -v ':$' | grep -v '^$' | grep '\.' | rev | cut -d'.' -f1 | rev | sort | uniq -c | sort -rn | head -5
```

---

## Spiegazione Passo per Passo

### 1. `ls -R 2>/dev/null`

`ls -R` lista ricorsivamente tutti i file nelle sottodirectory.  
Quando l'output è piped (non va a terminale), `ls` mette un file per riga invece di formattarli in colonne.  
`2>/dev/null` redirige lo **stderr** (file descriptor 2) verso `/dev/null` (il cestino del sistema), eliminando i messaggi "Permission denied" che appaiono sulle directory non accessibili. Senza questo redirect, gli errori si mischiano all'output e falsano i conteggi.

Output esempio:
```
.:
data.txt
my.example.c
src

./src:
hw.c
hw.h
```

### 2. `grep -v ':$'`

Rimuove le **intestazioni delle directory** — le righe che `ls -R` stampa per indicare in quale cartella si trova (es. `./src:`).  
Queste righe si riconoscono perché finiscono con `:`.

- `$` è un'**ancora di fine riga**: il pattern `:$` significa "due punti nell'ultima posizione".
- `-v` inverte la selezione: passa solo le righe che **non** corrispondono al pattern.

Senza questo filtro anche `./src:` verrebbe trattata come un "file" con estensione `src:`.

### 3. `grep -v '^$'`

Rimuove le **righe vuote** che `ls -R` inserisce come separatore tra una directory e la successiva.

- `^` è un'**ancora di inizio riga**.
- `^$` = inizio riga immediatamente seguito da fine riga = riga vuota.

### 4. `grep '\.'`

Mantiene solo le righe che contengono un punto — cioè i file che hanno un'estensione.  
Elimina automaticamente i nomi di directory (es. `src`) che non hanno estensione.

Il `\.` usa il backslash per rendere il punto **letterale**: in regex, `.` senza backslash significa "qualsiasi carattere". Con `\.` cerchiamo proprio il carattere punto.

### 5. `rev`

Rovescia ogni riga carattere per carattere.

```
my.example.c  →  c.elpmaxe.ym
data.txt      →  txt.atad
hw.c          →  c.wh
```

L'obiettivo è portare l'estensione (la parte dopo l'**ultimo** punto) in **prima posizione**, così il passo successivo può usare `cut` che lavora dal primo campo.

### 6. `cut -d'.' -f1`

Taglia la riga usando il punto come delimitatore (`-d'.'`) e prende il **primo campo** (`-f1`), cioè tutto quello che precede il primo punto.

Dopo il `rev` del passo precedente, il primo campo è proprio l'estensione rovesciata:
```
c.elpmaxe.ym  →  c
txt.atad      →  txt
c.wh          →  c
```

### 7. `rev` (secondo)

Rovescia di nuovo per rimettere le stringhe nel verso corretto. In questo caso le estensioni sono già brevi e simmetriche (`c`, `txt`, `h`) ma il doppio `rev` è necessario per correttezza generale (es. un'estensione come `html` diventerebbe `lmth` senza di esso).

A questo punto l'output è una lista di estensioni, una per riga:
```
txt
c
c
h
```

### 8. `sort`

Ordina le righe alfabeticamente. Serve perché il passo successivo (`uniq -c`) conta solo righe **consecutive** uguali. Senza `sort`, due occorrenze di `c` separate da `txt` verrebbero contate come `1 c`, `1 c` invece di `2 c`.

```
c
c
h
txt
```

### 9. `uniq -c`

Conta le occorrenze consecutive uguali e le prefissa con il conteggio:
```
      2 c
      1 h
      1 txt
```

### 10. `sort -rn`

Secondo `sort`, questa volta per **ordinare i risultati per frequenza**:
- `-n`: ordine **numerico** (senza, `10` verrebbe prima di `2` perché `1` < `2` in ordine lessicografico)
- `-r`: ordine **inverso** (decrescente) — la più frequente per prima

```
      2 c
      1 txt
      1 h
```

### 11. `head -5`

Mostra solo le prime 5 righe — le 5 estensioni più comuni.

---

## Setup per il Test

```bash
mkdir -p ~/test_ext/src
touch ~/test_ext/data.txt ~/test_ext/my.example.c
touch ~/test_ext/src/hw.c ~/test_ext/src/hw.h
cd ~/test_ext
```

Output atteso:
```
      2 c
      1 txt
      1 h
```

---

## Variante: dalla root del sistema

```bash
cd /
ls -R 2>/dev/null | grep -v ':$' | grep -v '^$' | grep '\.' | rev | cut -d'.' -f1 | rev | sort | uniq -c | sort -rn | head -5
```

Il risultato varia in base ai pacchetti installati sulla VM. Il `2>/dev/null` è necessario perché da `/` ci sono directory non accessibili all'utente normale.
