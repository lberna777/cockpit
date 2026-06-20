---
description: "Mostra il riepilogo rapido dello stato di tutti i moduli e il prossimo step per ciascun corso."
---

Leggi `stato/corrente.md` e produci esclusivamente:

---

**1. Tabelle di stato per corso**

Una tabella per corso nell'ordine: SysAdmin → Security → Diritto.

```
### SysAdmin — Lab Amministrazione di Sistemi T
| Modulo | Nome | Stato |
|--------|------|-------|

### Security — Lab Sicurezza Informatica T
| Modulo | Nome | Stato |

### Diritto — Diritto dell'Informatica T
| Modulo | Nome | Stato |
```

Per i moduli 🔄: stato interno tra parentesi.

---

**2. Avanzamento per corso**

```
SysAdmin  ████████░░ 77%  (10/13 moduli ✅)
Security  ░░░░░░░░░░  0%  (0/12 moduli ✅)
Diritto   ██████░░░░ 62%  (8/13 moduli ✅)
```

Calcola percentuali dal file.

---

**3. Prossimo step per corso**

```
SysAdmin  → [ID] — [azione concreta]
Security  → [ID] — [azione concreta]
Diritto   → [ID] — [azione concreta]
```

---

**4. Alert ripasso** *(solo se presenti)*

Leggi `stato/tracker_ripasso.md`. Se ci sono moduli con ripasso scaduto:
```
⚠️ Ripasso scaduto: [lista moduli con data scadenza]
```

---

Non aggiungere spiegazioni, commenti o testo libero oltre a questi elementi.
