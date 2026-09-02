---
description: "Analisi gap: moduli a rischio, ripasso scaduto, errori ricorrenti, e un piano d'azione prioritizzato."
---

**Carica il contesto — in parallelo**

Il briefing è già in contesto. Leggi in più:
- `piano/piano_laurea.md` — sessione corrente, catene di dipendenza, regole di carico
- `corsi/<COD>/percorso.md` di ogni corso aperto
- `corsi/<COD>/fonti.md` di ogni corso aperto — le fonti mancanti sono lacune a tutti gli
  effetti, spesso le più bloccanti

---

**Analisi e output**

Produci esclusivamente questo report:

---

## Analisi Lacune — [DATA]

### 1. Copertura per esame della sessione corrente

Per ogni esame:
```
<COD> — appello: [data da piano_laurea.md] (fra N settimane)
Moduli chiusi: X/Y (Z%)
Moduli in corso: [lista con stato interno]
Moduli non iniziati: [lista]
Programma rimanente: [in blocchi di moduli, non in ore]
Ritmo necessario: [moduli a settimana per arrivare all'appello]
Ritmo osservato: [moduli a settimana nelle ultime 4 settimane, da log/giornate.md]
Bilancio: [sostenibile / in ritardo di N moduli]
```

> Il bilancio si calcola su **blocchi settimanali di programma coperto, mai su ore giornaliere**
> (`profilo/studente.md`): la disponibilità di Lorenzo è troppo variabile perché una stima
> oraria dica qualcosa. Il ritmo osservato viene dai fatti registrati, non da una stima.

### 2. Fonti mancanti

Da `fonti.md` di ogni corso aperto: cosa manca, e quali moduli blocca. Una fonte mancante su un
modulo in testa a una catena è il rischio più grave che ci sia.

### 3. Moduli a rischio critico

In ordine di urgenza — moduli dove:
- l'appello è vicino e il modulo non è iniziato
- il modulo è aperto da più di due settimane senza progresso
- il ritmo osservato è sotto quello necessario
- il modulo è in testa a una catena di `piano_laurea.md`: un ritardo qui si propaga

Per ciascuno: **l'azione concreta** che lo sblocca.

### 4. Ripasso scaduto

Dal tracker:
```
| Corso | Modulo | Chiuso | Ultimo ripasso | Scaduto da |
```
Suggerimento: "Dedica 15-20 minuti a inizio giornata a `/ripassa <COD> <ID>`".

### 5. Pattern di errore attivi

Da `profilo/errori.md`, quelli che compaiono in **2+ moduli**, e tutti i **trasversali**:
```
| Pattern | Moduli o corsi coinvolti | Rischio all'esame |
```

### 6. Decisione di carico

Se mancano **sei settimane o meno** al primo appello della sessione, il checkpoint di
`piano_laurea.md` è dovuto: dichiara se la sessione regge a quattro esami o va portata a tre.
Se va ridotta, indica **quale esame si taglia** applicando le regole: si taglia dal fondo, mai
un esame in testa a una catena, e il tagliato ha già una destinazione.

### 7. Piano d'azione

Le cinque azioni a maggior impatto, in ordine:
1. [azione] — [blocco di programma] — [perché è prioritaria]

---

Non aggiungere testo libero oltre a questi elementi.
