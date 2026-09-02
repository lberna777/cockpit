# Briefing — 2026-09-02

> Generato da `scripts/briefing.py`. **Non modificare a mano**: viene sovrascritto.
> È l'unico contesto caricato d'ufficio. Tutto il resto si carica su necessità.

## Come studia Lorenzo

> Strato **permanente**. Cambia nell'ordine dei mesi. Si emenda, non si riscrive.
> Accoglie solo ciò che vale su più corsi: un fatto valido per un esame solo va in
> `corsi/<CODICE>/percorso.md`.
>
> Quando una riga viene superata, non si cancella: si marca `[superato AAAA-MM]` e si
> aggiunge quella nuova. Come Lorenzo è cambiato come studente è a sua volta informazione.

## Come apprende

- Approccio attivo: esegue, annota in presa diretta con domande aperte, poi consolida.
  La lettura passiva non produce niente di utilizzabile all'esame.
- Vuole il *perché* prima del *come*. Una regola senza la ragione che la genera non regge
  fino alla prova.
- Le domande che si pone durante l'esecuzione sono il materiale migliore che produce:
  vanno raccolte e risposte inline, non lasciate cadere.

## Condizioni operative

- Disponibilità giornaliera **molto variabile**. Pianificare per blocchi settimanali di
  programma coperto, mai per monte ore giornaliero.
- Da agosto 2026: nessuna frequenza, dodici esami arretrati, preparazione autonoma.
- Un solo esame per volta in fase attiva. Gli altri restano in ripasso, non in parallelo.

## Cosa ha funzionato

- Il ciclo orientato alle prove: prova fredda cronometrata → confronto con la soluzione
  ufficiale → estrazione dei pattern mancanti → drill mirato. È il metodo che ha portato
  il 30 in Diritto e il 26 in Sicurezza nella sessione estiva 2026.
- Gli appunti grezzi con domande aperte, poi elaborati.
- L'omissione deliberata: salta negli appunti ciò che ha già consolidato. **L'assenza di
  un argomento non è una lacuna** finché non è verificata.

## Cosa non ha funzionato

- `[2026-06]` Ha lasciato Laboratorio di Amministrazione di Sistemi a metà sessione, dopo

_(troncato — apri il file per il resto)_

## Errori ricorrenti da intercettare

> Strato **permanente**, append-oriented. Aggiornato da `/appunti`, `/ripassa`, `/simula`
> nella stessa esecuzione in cui l'errore emerge.
>
> La sezione **trasversale** è quella che conta: sono modi di ragionare, non errori di
> materia, e si ripresenteranno identici su corsi che Lorenzo non ha ancora aperto.
> Il briefing d'avvio carica questa sezione per prima.

## Trasversale — vale su ogni corso

### 1. Semplificare distinzioni che vanno tenute separate
Tendenza accertata a collassare due concetti vicini in uno. Emerso ripetutamente in
Diritto, ma è un pattern cognitivo, non una lacuna giuridica.

**Dove si ripresenterà**: stabilità asintotica vs. semplice (`CA`); banda vs. banda
passante (`TLC`); processo vs. thread, concorrenza vs. parallelismo (`SO`); tensione di
soglia vs. tensione di saturazione (`ELN`); latenza vs. RTT (`RETI`).

**Contromisura**: davanti a due termini vicini, chiedersi *cosa distingue esattamente il
primo dal secondo, e quale caso limite li separa*. Se non emerge un caso limite, la
distinzione non è stata capita.

### 2. Fermarsi al primo indizio
Considera risolto un esercizio al primo risultato plausibile, senza verificare che spieghi
**tutti** i dati del problema. Emerso su analisi di traffico in Sicurezza.

**Contromisura**: far quadrare i numeri prima di concludere. Un esercizio è chiuso quando

_(troncato — apri il file per il resto)_

## Esame attivo

**Sessione**: 52 | **Aggiornato**: 2026-07-15

> **Istruzione per Claude**: questo file va letto ALL'INIZIO di ogni sessione. È l'unico file obbligatorio per avere contesto.
> Per dettagli sui moduli (materiali, concetti, esercizi): `stato/percorso.md`
> Per lo storico delle sessioni passate: `stato/log_sessioni.md`
> Per il piano fasi e stime ore: `ESAMI SCELTI.md`

---

## Stato Moduli

### SysAdmin — Lab Amministrazione di Sistemi T

> ⚠️ **0A–2B (sistema embrionale)**: lab eseguiti ✅ ma materiali da rifare. Le "lezioni" erano walkthrough — rinominate in `guida_lab_*`. Nessuna lezione teorica esiste per questi moduli. Guida-lab da rifare con le nuove direttive quando c'è tempo. Conoscenza teorica: non verificata. Esame solo pratico → priorità bassa rispetto a 3E–4C.

| Modulo | Nome | Stato | Note |
|--------|------|-------|------|
| 0A | Filesystem e Comandi Base | ⚠️ | Lab eseguito (s.3); guida_lab MANCANTE; no lezione |
| 0B | Pipe, Redirect e Filtri | ⚠️ | Lab eseguito (s.4); guida_lab da rifare; no lezione |
| 1A | Variabili, Condizioni, Loop | ⚠️ | Lab eseguito (s.5); guida_lab da rifare; no lezione |
| 1B | Funzioni, Case, Test | ⚠️ | Lab eseguito (s.6); guida_lab da rifare; no lezione |
| 2A | Gestione Utenti e Permessi | ⚠️ | Lab eseguito (s.7-8); guida_lab da rifare; no lezione |
| 2B | LAB Utenti, Permessi e File | ⚠️ | Lab eseguito; guida_lab da rifare; no lezione |
| 2C | Gestione File: find, tar, rsync | ✅ | |
| 3A | Gestione Servizi con Systemd | ✅ | Sessione 10 |
| 3B | Gestione Pacchetti Software | ✅ | Sessione 13 |
| 3C | Gestione Processi | ✅ | Sessione 16 |
| 3D | Networking di Base | ⬜ | Restart dall'Es.1 — guida_lab in creazione |
| 3E | Vagrant Multi-Machine | ⬜ | |
| 3F | Automazione con Ansible | ⬜ | |
| 4A | Servizi base rete (DHCP, router via Ansible) | ⬜ | ⚠️ non mappato prima |
| 4B | **SNMP / Monitoraggio centralizzato** + LAB | ⬜ | ⚠️ **mancante: né mappato né scaricato né studiato** — è d'esame (netmon/SNMP) |
| 4C | **LDAP / Configurazione centralizzata** + LAB | ⬜ | ⚠️ **mancante: né mappato né scaricato né studiato** — è d'esame (auth LDAP) |

**Esercizi Scripting** (traccia parallela in `esercizi/SYSADM/`):

_(troncato — apri il file per il resto)_

## Ripassi dovuti

_Tracker presente ma vuoto: nessun modulo chiuso finora._

## Ultime giornate

_Nessuno storico giornaliero._
