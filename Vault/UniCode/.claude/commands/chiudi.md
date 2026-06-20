---
description: "Chiude la sessione di studio. Aggiorna log, stati, tracker ripasso e punto di ripresa."
---

Esegui i seguenti passi in ordine.

---

**1. Leggi lo stato corrente** *(solo se non già letto in questa conversazione)*
Leggi `stato/corrente.md` per recuperare: numero di sessione, data, stato dei moduli.

---

**2. Raccogli le informazioni dalla sessione**

Chiedi a Lorenzo in un'unica domanda compatta — adattando le domande alla materia trattata:

*Per sessioni SysAdmin o Security (lab con VM):*
- Quali moduli/argomenti sono stati affrontati
- Quali esercizi sulla VM sono stati completati, quali interrotti, quali saltati
- Domande rimaste aperte o blocchi non risolti
- Problemi tecnici nuovi sulla VM

*Per sessioni Diritto (teoria):*
- Quali moduli/argomenti sono stati affrontati
- Se le domande di autoverifica sono state completate
- Concetti rimasti poco chiari o da approfondire

*Se la sessione ha toccato più materie*: chiedi per ciascuna.

Attendi la risposta prima di procedere.

---

**3. Aggiorna stato/corrente.md**

- **Intestazione**: incrementa il numero di sessione di 1, aggiorna la data "Aggiornato"
- **Stato moduli**: aggiorna ⬜/🔄/✅ per ogni modulo toccato
  - SysAdmin/Security → ✅ solo se Lorenzo ha eseguito gli esercizi sulla VM in prima persona
  - Diritto → ✅ solo se ha letto la lezione, risposto alle domande di autoverifica e scritto appunti grezzi
- **Avanzamento**: ricalcola le barre di progresso e le percentuali
- **Prossimi Passi**: aggiorna con il punto esatto da cui iniziare per ogni materia attiva

---

**4. Aggiorna stato/log_sessioni.md**

Aggiungi una nuova voce **in cima** alla sezione (ordine cronologico inverso):

```
### Sessione N — YYYY-MM-DD (completata)
**Focus**: <materia/e — modulo/i>
**Coperto in sessione**:
- ...
**Non coperto / da riprendere**:
- ...
**Prossima sessione — da dove partire**:
→ ...
```

---

**5. Aggiorna stato/tracker_ripasso.md**

Per ogni modulo portato a ✅ in questa sessione:
- Aggiungi una riga nella tabella del corso corrispondente
- "Completato" = data odierna
- "Ultimo ripasso" = mai
- "Prossimo ripasso" = data odierna + 3 giorni
- "Priorità" = 🟢

Per ogni modulo ripassato in questa sessione:
- Aggiorna "Ultimo ripasso" = data odierna
- Calcola "Prossimo ripasso" con intervallo crescente: 3gg → 7gg → 14gg → 30gg
- Aggiorna "Priorità"

---

**6. Aggiorna il glossario** *(se necessario)*

Se sono emersi termini tecnici o giuridici nuovi:
- SysAdmin/Security → `glossario_sysadm.md`
- Diritto → `glossario_diritto.md`

Aggiungi con definizione concisa in ordine alfabetico.

---

**7. Aggiorna il troubleshooting** *(solo per sessioni lab con VM)*

Se sono stati risolti problemi tecnici nuovi, aggiungili a `troubleshooting_vm.md` con: sintomo, causa, soluzione.

---

**8. Conferma finale**

Mostra a Lorenzo:
- Numero della sessione chiusa e materie/moduli aggiornati
- Punto esatto da cui partirà la prossima sessione per ogni materia attiva
- Se ci sono moduli con ripasso scaduto (da tracker_ripasso.md), segnalarli: "⚠️ Ripasso scaduto per: [moduli]"
