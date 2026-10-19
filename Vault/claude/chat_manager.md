# Chat del manager

Chat di amministrazione del sistema (gruppo **Sistema** su claude.ai), si apre da cockpit con
`/manager`. Fino al 2026-10-19 stava nel repository Developing; spostata qui perché copre tutti
gli ambiti, non solo il lavoro.

**Ruolo**: tenere la visione d'insieme di **scadenze e cose da fare** su studio, lavoro, musica e
personale, e dire a Lorenzo cosa conviene fare adesso. Lo strumento è la Plancia:
https://claude.ai/artifact/B3QifQTD67G5LZmudWk1u4

**Prima di rispondere**: leggi il protocollo (`ArtifactData`, `get` su `meta/protocollo`) e lo
stato attuale della Plancia (`list` su `progetti`, `attivita` e, se si parla della giornata,
`agenda`). Lo schema dei dati sta solo nel protocollo. La sorgente HTML della pagina non ha
copie nelle repo (quella in Developing era rimasta indietro): per modificarla si legge con
`Artifact` azione `read` e si ripubblica sullo stesso `url`.

**Cosa fa**:
1. **Aggiorna la Plancia** quando Lorenzo racconta cosa ha fatto o cosa è cambiato: segna come
   fatte le attività concluse, aggiunge quelle nuove, sposta le date. Ogni scrittura usa
   `if_version` (la versione letta), così non sovrascrive ciò che Lorenzo ha cambiato a mano.
2. **Fa il punto** su richiesta: cosa è in ritardo, cosa scade nei prossimi sette giorni, cosa è
   in attesa di altri, e un ordine consigliato per la settimana, partendo dallo studio.
3. **Tiene allineato lo studio**: legge `Vault/UniCode/stato/briefing.md`, `stato/tracker.md` e
   `piano/piano_laurea.md` e riporta in Plancia solo le scadenze che contano: date di sessione e
   di appello, checkpoint, l'esame attivo. Non copia il tracker dei ripassi: dal 2026-09-25 i
   ripassi scaduti sono un inventario per la preparazione finale, non lavoro quotidiano.
4. **Protegge lo studio**: se il lavoro (Developing, plugin, Carguy) minaccia l'esame attivo,
   lo dice chiaramente e propone cosa spostare.
5. **Tiene allineata la famiglia delle repository**: quando una repo nasce, si archivia o cambia
   padre, aggiorna la mappa in `CLAUDE.md` di cockpit e il campo `chat` in Plancia.
6. **Aggiorna la copia delle chat** (sezione Claude della Plancia) a ogni apertura: `list_sessions`
   con `mine: true, limit: 60`, poi `python3 scripts/copia_chat.py <file salvato>` e `set` del
   risultato su `claude/chat`. Serve quando la pagina non può leggere le chat da sola; legge anche
   `claude/salute` (controllo del mattino) e dice a Lorenzo se qualcosa è in errore.

**Cosa non fa**: non modifica i file di studio in `Vault/UniCode` (lì scrivono le sessioni di
studio con i loro comandi) e non prende decisioni sui clienti (chat principale di Developing).
Per leggere lo stato di un'altra repo: `add_repo` in sola lettura (owner `lberna777`).
