# Esercizio 02 — Conta Occorrenze (testo libero)

**Modulo**: 0B — Pipe, Redirect e Filtri  
**Data**: 2026-05-12  
**Difficoltà**: intermedio  
**File di testo**: `The_Adventures_Of_Sherlock_Holmes.txt` (Peter Norvig, licenza open)

---

## Obiettivo

Dato un file di testo passato come argomento, uno script bash deve:

1. Contare le occorrenze della lettera `a` (minuscola)
2. Contare le occorrenze della parola `sherlock` (case insensitive)
3. Per ogni parola distinta, contare le occorrenze e mostrare le 5 più frequenti

---

## Script Finale

```bash
#!/bin/bash

echo "=== LETTERE A ==="
grep -o 'a' "$1" | wc -l

echo "=== SHERLOCK CASE INSENSITIVE ==="
grep -oi 'sherlock' "$1" | wc -l

echo "=== PAROLE PIU' USATE ==="
tr '[:upper:]' '[:lower:]' < "$1" | tr -cs '[:alpha:]' '\n' | sort | uniq -c | sort -rn | head -5
```

**Output su Holmes**:
```
=== LETTERE A ===
34377
=== SHERLOCK CASE INSENSITIVE ===
99
=== PAROLE PIU' USATE ===
   5634 the
   3038 i
   3018 and
   2744 to
   2659 of
```

---

## Spiegazione Passo per Passo

### Obiettivo 1 — Occorrenze della lettera `a`

```bash
grep -o 'a' "$1" | wc -l
```

**`-o`** è il flag chiave: invece di restituire le righe che contengono il pattern, stampa **solo la parte corrispondente**, una per riga. Ogni `a` trovata diventa una riga separata. `wc -l` conta quelle righe → conta le occorrenze.

**Perché non `-i`?** L'esercizio chiede la lettera `a` minuscola, non `A`. Con `-i` si conterebbero anche le `A` maiuscole, falsando il risultato. La distinzione è intenzionale.

**Alternativa equivalente**:
```bash
tr -cd 'a' < "$1" | wc -c
```
`tr -cd 'a'` elimina tutto ciò che non è `a`; `wc -c` conta i byte rimasti.

---

**Riepilogo dei flag di `grep` esplorati in sessione** (con lo stesso file):

| Comando | Risultato | Perché |
|---------|-----------|--------|
| `grep 'a' file \| wc -l` | 2322 | Conta le **righe** con almeno una `a` |
| `grep -c 'a' file \| wc -l` | 1 | `-c` stampa già un numero; `wc -l` conta le righe di quell'output (1 riga) |
| `grep -n 'a' file \| wc -l` | 2322 | `-n` aggiunge il numero di riga, ma le righe restituite sono le stesse |
| `grep -v 'a' file \| wc -l` | 2816 | Righe **senza** `a`; 2322+2816 = totale righe del file |
| `grep -i 'a' file \| wc -l` | 2373 | Righe con `a` o `A`; 51 righe hanno `A` ma non `a` |
| `grep -o 'a' file \| wc -l` | 34377 | Occorrenze effettive della lettera `a` |

La differenza fondamentale: senza `-o` conti **righe con match**; con `-o` conti **occorrenze**.

---

### Obiettivo 2 — Occorrenze di `sherlock` (case insensitive)

```bash
grep -oi 'sherlock' "$1" | wc -l
```

- `-o`: una occorrenza per riga (come sopra)
- `-i`: ignora maiuscole/minuscole — cattura `Sherlock`, `SHERLOCK`, `sherlock` ecc.

I due flag si combinano: `-oi` = una corrispondenza per riga + case insensitive.

**Attenzione**: senza `-o`, `grep -i 'sherlock' | wc -l` conterebbe le **righe** contenenti sherlock — se apparisse due volte sulla stessa riga, verrebbe contato una volta sola.

---

### Obiettivo 3 — Top 5 parole per frequenza

```bash
tr '[:upper:]' '[:lower:]' < "$1" | tr -cs '[:alpha:]' '\n' | sort | uniq -c | sort -rn | head -5
```

**Approccio**: invece di cercare ogni parola nel file (loop con migliaia di `grep` — lento), si trasforma il file in una parola per riga e si riusa la pipeline `sort | uniq -c | sort -rn | head` già nota da 0B.

#### Passo 1 — `tr '[:upper:]' '[:lower:]' < "$1"`

Converte tutto il testo in minuscolo prima della tokenizzazione. Così `The`, `the`, `THE` diventano tutti `the` e vengono contati insieme.

L'ordine conta: va fatto **prima** di spezzare in parole. Se lo mettessi dopo, i token sarebbero già separati e non ci sarebbero più maiuscole miste da unificare.

Effetto sul conteggio:
- `the`: 5267 → 5634 (+367 occorrenze di `The`/`THE`)
- `and`: 2818 → 3018

#### Passo 2 — `tr -cs '[:alpha:]' '\n'`

Spezza il testo continuo in una parola per riga eliminando punteggiatura, spazi, simboli.

- `[:alpha:]`: classe POSIX per tutte le lettere (a-z, A-Z) — usata perché le lettere sono ciò che vogliamo **tenere**
- `-c`: complemento — invece di specificare cosa sostituire, specifichi cosa tenere; tutto il resto viene sostituito
- `-s`: squeeze — sequenze consecutive di `\n` (da più simboli adiacenti) collassate in uno solo, evitando righe vuote

Senza `-c` bisognerebbe elencare esplicitamente ogni carattere da eliminare (`,`, `.`, `'`, `*`, spazio, tab…) — impossibile da gestire.

Senza `-s` ogni segno di punteggiatura tra due parole genererebbe righe vuote che `uniq -c` conterebbe come token vuoti.

#### Passi 3–5 — `sort | uniq -c | sort -rn | head -5`

Identici all'esercizio 01:
- `sort`: ordina alfabeticamente (prerequisito per `uniq`)
- `uniq -c`: conta occorrenze consecutive uguali
- `sort -rn`: ordina per frequenza decrescente
- `head -5`: prime 5

---

## Setup e Uso

```bash
# Trasferire il file dalla VM host tramite cartella condivisa Vagrant
cp /vagrant/The_Adventures_Of_Sherlock_Holmes.txt ~/holmes.txt

# Creare lo script
cat > ~/conta_occorrenze.sh << 'EOF'
#!/bin/bash

echo "=== LETTERE A ==="
grep -o 'a' "$1" | wc -l

echo "=== SHERLOCK CASE INSENSITIVE ==="
grep -oi 'sherlock' "$1" | wc -l

echo "=== PAROLE PIU' USATE ==="
tr '[:upper:]' '[:lower:]' < "$1" | tr -cs '[:alpha:]' '\n' | sort | uniq -c | sort -rn | head -5
EOF

chmod +x ~/conta_occorrenze.sh
~/conta_occorrenze.sh ~/holmes.txt
```

---

## Nota: trasferire file host → VM con Vagrant

Con Vagrant + VirtualBox la cartella condivisa è automatica:
- **Host**: tutto ciò che sta in `~/sysAdmin-lab/` è visibile dentro la VM come `/vagrant/`
- **Dentro la VM**: `cp /vagrant/nomefile.txt ~/` per copiarlo nella home

Non serve `scp` né configurazione aggiuntiva.
