# Template — host "router" (più interfacce di rete, es. eth1/eth2/eth3)

Fa da tramite tra segmenti (`FORWARD`) ed eventualmente offre lui stesso un servizio locale
(`INPUT`/`OUTPUT`, come un endpoint qualunque).

Riferimento: `procedura_operativa_iptables.md` §1-5, `guida_esame_iptables.md` §3-4

## Chiarimenti prima di iniziare (dubbi comuni, non solo di questo esercizio)

- **`-i`/`-o` vs `-s`/`-d`**: `-i`/`-o` prendono **il nome dell'interfaccia locale** (`eth1`,
  `eth2`, `eth3`...), mai un indirizzo IP — dicono "da/verso quale porta fisica/virtuale **di
  questo router**". `-s`/`-d` prendono un **indirizzo IP** (o una rete, es. `172.20.0.0/20`) e
  guardano dentro il pacchetto chi l'ha mandato/a chi è diretto. Sono due criteri indipendenti:
  puoi usarli insieme (`-i eth1 -o eth2 -s 172.20.0.0/20 -d 1.1.1.14`) per essere più precisi, ma
  non sono intercambiabili. Ricorda: i nomi delle interfacce sono **locali a ogni macchina** — non
  esiste relazione tra "l'eth1 del Client" e "l'eth1 del Router", sono cose diverse che condividono
  solo il nome.
- **`<tcp|udp>` nei template**: è solo una notazione per dire "scegli uno dei due secondo il
  servizio" — non va mai copiato alla lettera. Sostituiscilo con `tcp` o `udp` guardando cosa
  chiede la consegna per quella porta.
- **`--dport` vs `--sport`, e se il numero di porta cambia**: `--dport` = porta di
  **destinazione** (dove il pacchetto è diretto); `--sport` = porta di **sorgente** (da dove
  parte). Nella richiesta usi `--dport <porta_servizio>`; nella risposta usi `--sport
  <stessa_porta>`. **Il numero di porta non cambia mai tra richiesta e risposta** — cambia solo
  quale dei due flag lo tiene, perché è cambiata la direzione. Eccezione NTP: porta 123 su
  entrambi i lati, stessa riga ha sia `--dport 123` sia `--sport 123`.
- **FORWARD vs INPUT/OUTPUT — l'errore più facile su un router**: il router ha `FORWARD`
  popolato, ma **non tutto** ciò che lo riguarda è FORWARD. Per OGNI flusso chiediti: il traffico
  *attraversa* il router (due estremi sono host diversi da lui, lui è solo il tramite) → `FORWARD`,
  sempre con **due** interfacce (`-i` e `-o` insieme); oppure il traffico *nasce o muore sul router
  stesso* (es. il router offre lui un servizio, tipo DNS/LDAP) → `INPUT`/`OUTPUT`, sempre con **una
  sola** interfaccia per riga (`-i` da sola o `-o` da sola, mai entrambe). Scrivere in `FORWARD` un
  flusso che in realtà termina sul router è un errore concreto già capitato: quella regola non
  scatta mai (il traffico locale non passa per `FORWARD`), e il vero traffico finisce scartato
  dalla policy `DROP` di `INPUT`/`OUTPUT` perché lì non hai messo nulla.
  **Esempio concreto realmente sbagliato** (13 giu 2024, punto 4): "i client accedono al DNS del
  router, porta 53". Il DNS gira **sul router stesso** → il router è la **destinazione finale**, non
  un tramite: va in `INPUT` (richiesta, `-i eth1 --dport 53`) + `OUTPUT` (risposta, `-o eth1 --sport
  53 ESTABLISHED`), **una** interfaccia per riga. Metterlo in `FORWARD` (`-i eth1 -o eth3 --dport
  53`) è l'errore: quel traffico non attraversa il router verso un **terzo host**, quindi non passa
  **mai** per la catena `FORWARD`, la regola non fa match, e il vero pacchetto DNS viene scartato
  dalla policy `DROP` di `INPUT`. Confrontalo col punto 3 dello stesso esercizio (client→internet:443):
  *quello* attraversa davvero il router verso un host terzo (Internet) → `FORWARD` è corretto. Il
  test è sempre lo stesso: "questo flusso **finisce sul router**, o lo **attraversa** verso qualcun
  altro?" — non "quante interfacce tocca".

```bash
#!/bin/bash

# --- 1. Ripulisci lo stato precedente (rilanciabile senza accumulare regole) ---
iptables -F INPUT
iptables -F OUTPUT
iptables -F FORWARD
iptables -t nat -F        # ⚠️ OBBLIGATORIO se questo esercizio usa NAT (vedi §3): i tre -F sopra
                         # svuotano solo la tabella `filter`, NON la tabella `nat`. Se ometti
                         # questa riga, ogni ri-lancio dello script ACCUMULA regole SNAT/DNAT
                         # duplicate (bug silenzioso: la prima traduzione vince, ma la tabella si
                         # riempie di doppioni). Se l'esercizio non ha NAT, la riga è innocua: lasciala.

# --- 2. Loopback sempre permesso ---
iptables -A INPUT -i lo -j ACCEPT
iptables -A OUTPUT -o lo -j ACCEPT

# --- 3. NAT — SOLO se la consegna lo richiede esplicitamente ---
# Segnale nella consegna: un servizio con IP privato va raggiunto "indirettamente"
# dall'esterno (serve DNAT), oppure una rete privata deve "uscire" con un IP
# pubblico che non è il suo (serve SNAT/MASQUERADE). ⚠️ Questo vale ANCHE quando
# il "fuori" non è Internet ma un altro segmento della topologia che non ha
# instradamento di ritorno verso la rete privata (visto nel pool: 13 giu 2024,
# punto 1 — client privato che contatta un server su una rete "pubblica" diversa
# dalla propria, nessuna parola "indiretto" nel testo, ma serve SNAT lo stesso).
# Se la consegna chiede solo "consentire/negare questo traffico" tra reti che SI
# raggiungono già a vicenda, NON serve NAT: salta questa sezione. Dettaglio
# completo dei segnali: procedura_operativa_iptables.md §2.
#
# iptables -t nat -A PREROUTING -i <if_esterna> -d <ip_pubblico> -p tcp --dport <porta_pubblica> \
#     -j DNAT --to-destination <ip_privato>:<porta_reale>
# iptables -t nat -A POSTROUTING -s <rete_privata> -o <if_esterna> -j SNAT --to-source <ip_confine>
#
# ⚠️ Se hai fatto DNAT, le regole FORWARD sotto devono guardare l'indirizzo
# GIÀ TRADOTTO (quello privato), perché prerouting agisce prima di forward.

# --- 4. Regole FORWARD — un blocco per ogni flusso che ATTRAVERSA il router ---
# Per OGNI flusso della consegna che riguarda due host diversi da questo router,
# chiediti: da quale INTERFACCIA DEL ROUTER entra, da quale esce? (mai le
# interfacce dell'altro host: i nomi eth* sono locali a ciascuna macchina).
# Se invece il flusso nasce/muore SUL ROUTER STESSO, non va qui — vedi punto 5.
#
# iptables -A FORWARD -i <if_in> -o <if_out> -p <tcp|udp> --dport <porta> -j ACCEPT
# iptables -A FORWARD -i <if_out> -o <if_in> -p <tcp|udp> --sport <porta> -m state --state ESTABLISHED -j ACCEPT
#
# ⚠️ Se la consegna dice "da/verso qualsiasi host" per un estremo, non aggiungere
# -s/-d per quel lato. Aggiungi -s <rete> / -d <rete> quando conosci il segmento
# esatto, per non essere più permissivo del necessario.

# <<< scrivi qui i tuoi blocchi FORWARD, una coppia per flusso >>>

# --- 5. Regole INPUT/OUTPUT locali — quando il router stesso è sorgente o destinazione ---
# (es. il router fa da server DNS/LDAP per qualcun altro, o inizia lui una richiesta):
# qui NON è FORWARD, perché il router è la destinazione (o la sorgente), non un
# tramite — una sola interfaccia coinvolta per riga, non due.
#
# iptables -A INPUT  -i <if> -p <tcp|udp> --dport <porta> -j ACCEPT
# iptables -A OUTPUT -o <if> -p <tcp|udp> --sport <porta> -m state --state ESTABLISHED -j ACCEPT

# <<< scrivi qui eventuali righe locali >>>

# --- 6. Policy di default, sempre per ultime ---
iptables -P INPUT DROP
iptables -P OUTPUT DROP
iptables -P FORWARD DROP
```
