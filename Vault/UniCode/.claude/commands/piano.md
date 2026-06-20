---
description: "Genera il piano di studio per oggi basandosi sullo stato, le scadenze e la fase corrente."
---

Leggi in parallelo:
- `stato/corrente.md`
- `ESAMI SCELTI.md`
- `stato/tracker_ripasso.md`

La data di oggi è disponibile nel contesto. Calcola i giorni mancanti a ciascun esame:
- Diritto: 16/06/2026
- SysAdmin: 22/06/2026
- Security: 17/07/2026

Determina la fase corrente del piano settimanale. Identifica la **prossima singola cosa da fare** secondo questa priorità:
1. Ripasso scaduto (da tracker_ripasso.md) — se presente, va per primo (15-20 min)
2. Materia più a rischio rispetto alla scadenza (moduli rimasti / giorni rimasti)
3. Modulo aperto nella fase corrente

Produci esclusivamente:

---

**Prossima cosa da fare — [DATA]**

**[Materia] · ~Xh**
[Modulo ID] — [azione concreta: cosa fare, quale esercizio, quale file]

*(Solo se presente: un segnale di rischio in una riga — es. "Security: 5 moduli rimasti, 28 gg")*

---

Regole:
- Una sola azione, non un elenco di blocchi
- Se c'è ripasso scaduto, quello è la prossima cosa (indicalo esplicitamente prima dell'azione principale)
- Se per Security manca il PDF: azione = "Richiedere PDF da Virtuale per [modulo]"
- Se un modulo ha lezione pronta ma pratica non fatta, l'azione è la pratica
- Non aggiungere testo libero
