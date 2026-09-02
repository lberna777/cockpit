---
description: "Avvia la sessione di studio o cambia il corso in focus. Uso: /sessione [CODICE]"
argument-hint: "<CODICE> opzionale — vuoto = corso attivo dal briefing"
---

Il parametro passato è: "$ARGUMENTS"

---

**0. Risolvi il focus**

- Vuoto → il **corso attivo**, dal briefing già in contesto.
- Un codice valido in `piano/codici.txt` → quel corso.
- Un codice non riconosciuto → mostra i codici dal file e fermati.

Se il codice richiesto è diverso dal corso attivo, avvisa Lorenzo: **un solo esame per volta in
fase attiva** (`profilo/studente.md`). Cambiare focus è legittimo per un ripasso o per aprire
un corso nuovo, ma non per studiarne due in parallelo. Chiedi quale delle due cose sta facendo.

---

**1. Non rileggere ciò che è già in contesto**

Il briefing d'avvio contiene già profilo, errori ricorrenti, esame attivo, ripassi dovuti e le
ultime giornate. Leggi in più **solo** ciò che serve al focus richiesto:
- `corsi/<COD>/percorso.md` — se il focus è un corso non attivo
- `corsi/<COD>/fonti.md` — se si sta aprendo il corso adesso
- `piano/piano_laurea.md` — per la collocazione nella sessione d'esame

---

**2. Mostra lo stato dei moduli**

Solo i moduli del corso in focus, con lo stato. Per quelli in corso, il dettaglio dello stato
interno degli esercizi.

---

**3. Punto di ripresa**

Dal briefing se il focus è il corso attivo, altrimenti da `corsi/<COD>/percorso.md`.
Il punto esatto, non una generica indicazione di continuare.

---

**4. Piano per questa sessione**

- Modulo da affrontare (ID, nome)
- Obiettivo concreto

*Corsi con laboratorio*: la sequenza di esercizi; se il modulo è nuovo, ricorda `/lezione <COD>
<ID>` prima dell'ambiente, e `/lab <COD> <ID>` per l'esecuzione.
*Corsi con esercizi formali*: quali esercizi e in che ordine; se il modulo è nuovo, `/lezione`
prima.
*Corsi discorsivi*: i concetti da consolidare; se il modulo è nuovo, `/lezione` più
autoverifica; se è in corso, da quale concetto riprendere.

---

**5. Verifica la fonte** *(solo per il modulo di oggi)*

Controlla che il materiale del modulo esista in `corsi/<COD>/materiali/`. Se manca, **fermati e
dichiara il titolo esatto** da procurare: senza fonte non si genera niente.

---

**6. Prossima cosa da fare**

Priorità:
1. **Ripasso scaduto** dal tracker — se c'è, va per primo, 15-20 minuti
2. Il prossimo passo del corso in focus

```
**Prossima cosa — [DATA]**

[Corso] · [blocco di programma]
[ID modulo] — [azione concreta]

(Solo se presente: un segnale di rischio in una riga)
```

Segnali di rischio: appello vicino con troppi moduli aperti; ripasso scaduto; **checkpoint
delle sei settimane** in arrivo, che impone di decidere se la sessione resta a quattro esami o
scende a tre.

---

**7. Registra l'apertura**

Appendi a `stato/giornata.md`:

```
HH:MM · <COD> · sessione aperta su <ID modulo>.
```

---

**8. Non riproporre ciò che è già stato fatto**

Se la sessione è già in corso e Lorenzo sta cambiando focus, escludi i moduli e gli esercizi già
completati in questa conversazione.
