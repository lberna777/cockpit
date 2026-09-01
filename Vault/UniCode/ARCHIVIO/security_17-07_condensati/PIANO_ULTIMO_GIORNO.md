# PIANO ULTIMO GIORNO — 16/07/2026

> Esame: **Laboratorio di Sicurezza Informatica T — 17/07/2026, ore 14:00.**
> Questo è l'unico documento decisionale per domani. Leggilo per primo, poi esegui.
> Prova doppia, stessa seduta, **entrambe devono essere sufficienti**: quiz teorico 40% (45 min,
> niente materiale, penalità sulle sbagliate) + prova pratica 60% (2h, materiale consentito → la
> chiavetta con questa cartella).

---

## 1. Fotografia onesta dello stato

### Prova pratica (60%) — le 5 tipologie

| # | Tipologia | Stato reale | Giudizio |
|---|-----------|-------------|----------|
| S3 | Web vulnerabilities | Lab completo su VM (sessione 41). Ma nel pool solo **XSS riflesso** è risolto per intero; SQLi, path traversal/LFI sono solo accennati, senza modello svolto. Nessun `guida_esame`/`procedura`. | **DA RIFINIRE** |
| S4 | Binary exploitation | Il più solido: **4 esercizi hands-on annotati** (write_var, secret_function, remoto, returnlib shellcode+SUID, ret2libc) + modello pool. DRILL 12/02/2026 (il più recente) non ancora fatto. | **PRONTA** |
| S5 | Iptables/NFTables | Kit completo appena costruito e auditato (guida_esame + procedura + modello 7/7 + 2 template). Ma: Es1-2 su VM + **1 solo** esercizio pool risolto a mano (13/06/2024). Kit **mai stress-testato** su un secondo caso in autonomia. | **DA RIFINIRE (il più fragile)** |
| S10 | Network Intrusion Detection | 3 esercizi reali hands-on, kit maturo rivisto più volte. Nessuna teoria formale (scelta deliberata). ARP scoperto hands-on. | **PRONTA** |
| S11 | Integrity/privesc | Kit auditato "autosufficiente ad alta confidenza", **3/9 varianti** pool hands-on. Cracking password (rockyou) e alcune varianti non ancora praticate. | **PRONTA (rifinibile)** |

La prova pratica è la parte messa **bene**. Con la chiavetta e questi kit, sei attrezzato per tutte e 5.

### Quiz teorico (40%) — QUI È IL PROBLEMA VERO

Il quiz copre **tutto il programma** (15 moduli S1-S15), inclusi i comandi visti in lab. Stato copertura teorica formale (lezione + appunti):

- **Coperti**: S1, S2, S3, S4, S5 (5 moduli) — ma il ripasso è **scaduto** (vedi §2).
- **Solo pratica, zero teoria formale**: S10, S11.
- **MAI COPERTI, zero materiale**: **S6, S7, S8, S9, S12, S13, S14, S15 → 8 moduli su 15 (~53% del programma).**

Cosa significa in numeri: se le 30-40 domande sono distribuite sul programma, **grossomodo metà del quiz** cade su moduli mai studiati formalmente (crypto/TLS S12-S15, sicurezza fisica/cloud S6, backdoor S7, filtraggio attacchi S8, PAM/demoni S9). Con la **penalità sulle risposte sbagliate**, tirare a indovinare alla cieca ha valore atteso negativo.

**Questo è il rischio dominante e finora il più trascurato.** La prova pratica può andare benissimo e l'esame fallire comunque sul 40% teorico. Domani il baricentro dello studio va spostato qui.

---

## 2. Il vincolo di tempo (leggi: cosa è impossibile)

**Assunzione** (esplicita, non un dato certo): domani è una giornata di studio piena, stimo **~8-10h effettive**. Regola su questa cifra ma non contarci al minuto.

Cosa è **matematicamente impossibile** in un giorno, accettalo subito:
- Costruire lezioni solide da zero per 8 moduli mai visti. Non si fa. Al massimo **infarinatura**: leggere per riconoscere vero/falso, non per padroneggiare.
- Praticare hands-on tutte le varianti pool mancanti di S5/S11 + il DRILL S4 + il ripasso di tutto. Devi scegliere.
- Colmare il gap teorico degli 8 moduli fino a "sicurezza". Puntiamo a **ridurre il danno**, non ad azzerarlo.

Il ripasso pratico è **scaduto** su tutto ciò che è forte (fonte `tracker_ripasso.md`):
- **S3 🔴** (mai ripassato dal 26/06), **S4 🔴** (mai dal 02/07), **S1 🔴 / S2 🔴** (teoria, scaduti da fine giugno), **S10** scade proprio il 16/07.
- Rischio concreto: **perdere punti facili** su roba che sai, solo perché non l'hai rivista.

---

## 3. Allocazione del tempo per domani (in ordine di priorità)

Priorità dichiarata: **il collo di bottiglia è il quiz teorico, non la pratica.** Non sovra-investire su S4/S10/S11 che sono già forti. La sequenza sotto è pensata per massimizzare i punti recuperabili.

### 🟥 BLOCCO 1 — Infarinatura teorica 8 moduli scoperti (~3h) — PRIORITÀ MASSIMA
Obiettivo: passare da "0%" a "riconosco vero/falso" sugli 8 moduli mai visti. **Non** appunti, **non** lezioni: scrematura mirata.
- Fonti: PDF in `SLIDE TEORIA/SICINF/` (leggi solo titoli, definizioni in grassetto, schemi riassuntivi) + `glossario_sysadm.md` (nel pacchetto, blocco `00_trasversale`).
- ~20 min a modulo. Ordine consigliato per resa:
  1. **S9 (PAM/demoni/autorizzazione), S7 (backdoor), S8 (filtrare attacchi)** — vicini al lab, alta probabilità di domande su comandi/concetti già sfiorati in S10/S11.
  2. **S12, S13, S14, S15 (comunicazioni, TLS/OpenSSL, crittografia, gpg)** — concetti definitori (simmetrico vs asimmetrico, hash, rainbow table, handshake TLS, firma): rendono molto nel formato vero/falso.
  3. **S6 (sicurezza fisica e cloud)** — per ultimo, spesso domande a buon senso.
- Per ognuno annota 3-5 fatti-chiave su un foglio (per rinfrescarli prima delle 14:00). Non serve capire tutto: serve sapere quando un'affermazione è falsa.

### 🟧 BLOCCO 2 — Ripasso attivo del già-forte (~2h) — non perdere punti facili
Ripasso = **rispondere a domande senza guardare**, non rileggere.
- **S3, S4, S10**: rivedi `guida_esame_*`/`modello_*` (S10 e i modelli S3/S4 nel pacchetto), poi chiuditi il file e ripeti a voce il procedimento. S4 e S10 bastano 20-30 min l'uno.
- **S1, S2**: teoria scaduta e rilevante al quiz (enumerazione/nmap, autenticazione) — 20 min di scrematura appunti a testa.

### 🟨 BLOCCO 3 — Consolidare S5, il kit più fragile (~1.5-2h)
- Rileggi `guida_esame_iptables.md` + `procedura_operativa_iptables.md` + i due `template_ipt-*`.
- **Valore marginale più alto della giornata sul lato pratica**: risolvi **a mano** un secondo caso pool diverso dal 13/06/2024 — consigliato **8 feb 2024 (solo Router)** perché più semplice e stress-testa il kit senza costarti troppo. Se il tempo stringe, salta l'esercizio e limitati alla rilettura: il kit c'è.

### 🟩 BLOCCO 4 — Rifinitura S11 (~45 min, solo se in orario)
- Rileggi `guida_esame_privesc.md`. Se hai energia, prova **l'unico vettore non ancora praticato ad alto rendimento**: cracking di una password in `/etc/shadow` con `john`/`rockyou` (la nota rockyou.txt gzippata è già nel kit). Un solo giro, non di più.

### ⬜ BLOCCO 5 — Logistica + stop (~45 min, la sera)
Vedi checklist §4. **Poi smetti e dormi.** Sei arrivato stanco da sessione 52: un cervello riposato al quiz vale più di un'ora extra stanotte.

> **Se la giornata è più corta del previsto**: taglia nell'ordine BLOCCO 4 → esercizio pratico del BLOCCO 3 → S1/S2 del BLOCCO 2. **Non tagliare mai il BLOCCO 1**: è dove si gioca la sufficienza del 40%.

---

## 4. Checklist mattina 17/07 (prima delle 14:00)

**Chiavetta / materiale pratico (per il 60%)**
- [ ] Copiata `~/esame_security_17-07/` **intera** su chiavetta USB.
- [ ] **Verificata su un PC diverso**: infila la chiavetta e apri almeno un `.md` (es. `03_iptables_nftables/guida_esame_iptables.md`) per confermare che si legga davvero. Una chiavetta che non monta all'esame = 60% perso.
- [ ] I `.md` si leggono anche senza tool: sono testo puro. Se hai dubbi sull'aula, considera una seconda copia (secondo USB o file leggibili).

**VM (per il 60%)**
- [ ] **Snapshot pulito** pronto e verificato che **parta** (VirtualBox). Ricorda i residui da sessioni precedenti (utente `toor`, SUID su `cp`, banner `nftlab.sh`): parti da uno snapshot senza queste tracce.
- [ ] Comando di revert a portata: `VBoxManage snapshot <vm> restore <nome>` (la GUI è ambigua — vedi `00_trasversale/troubleshooting_vm.md`, sezioni AIDE + Snapshot).
- [ ] Clipboard Guest Additions funzionante (fix noto in `troubleshooting_vm.md`).
- [ ] **AIDE non è preinstallato** sulla VM privesc: se serve, `sudo apt install aide` (annotato nel troubleshooting).
- [ ] Cattura i deliverable **sull'host in tempo reale** durante l'esercizio (screenshot + `integrity.txt`/`web.txt`/`bof.txt` via via), **mai** lasciarli solo dentro la VM: un revert li cancella (lezione di sessione 51).

**Quiz teorico (per il 40%)**
- [ ] Niente materiale: la teoria dev'essere **in testa**. Rileggi il foglio dei fatti-chiave del BLOCCO 1 poco prima.
- [ ] **Conferma la regola esatta della penalità** (quanto toglie una sbagliata, se l'omessa vale 0). Strategia: rispondi dove hai confidenza ragionevole; sui moduli-infarinatura, **lascia in bianco** se sei nel buio totale e la penalità sulle sbagliate è pesante — meglio 0 che negativo.

**Generale**
- [ ] Controlla aula e orario, arriva presto.
- [ ] Documento d'identità / credenziali richieste.

---

## 5. Rischi residui (accettati per mancanza di tempo — messi in chiaro, non sorvolati)

1. **8 moduli teorici resteranno a livello infarinatura.** Sul quiz, su questi ti affidi a riconoscimento + eliminazione, con la penalità gestita col bianco strategico. Impossibile di più in un giorno: è un rischio accettato, non un errore da correggere.
2. **Kit S5 non stress-testato a sufficienza.** Se all'esame esce una topologia pool mai vista, ti appoggi a `procedura_operativa_iptables.md` §0.5 (da dove viene ogni pezzo di una regola) e ai template. Il secondo esercizio del BLOCCO 3 serve proprio a ridurre questo rischio.
3. **S3 pool sottile.** Se esce SQL injection o path traversal invece di XSS, non hai un modello risolto: ti appoggi a `guida_lab_moduloS3_web_security.md` (hai già fatto il lab) e al ragionamento sul meccanismo. Rischio medio.
4. **Stanchezza.** Sei arrivato provato. Il piano è volutamente sostenibile e chiude presto la sera: rispettalo.

**In una riga**: la pratica è pronta, il quiz teorico è il fronte scoperto — domani il tempo va speso lì più che a lucidare ciò che già brilla.
