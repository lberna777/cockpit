# Template — host "endpoint" (Client o Server: non fa mai da tramite per un terzo host)

Usa questo per qualunque host della topologia il cui traffico **nasce o muore sempre su di lui**
(mai `FORWARD` verso un terzo host). Vale sia per un `ipt-client.sh` che per un `ipt-server.sh`:
cambia solo chi inizia/chi riceve, lo scheletro è identico.

⚠️ **Non identificarlo con "ha una sola interfaccia"**: nel pool esiste un caso reale (un
webserver con **due** interfacce, una verso il Router/Internet e una dedicata verso un DB server —
vedi `modello_iptables_nftables.md`, caso 30 ottobre 2025) che resta comunque un "endpoint" in
questo senso: la sua catena `FORWARD` è vuota perché ogni interfaccia porta solo traffico che
comincia o finisce **su di lui** (client verso il DB, server verso Internet) — nessun terzo host
dall'altra parte a cui inoltrare qualcosa. Il numero di interfacce è un indizio, non la prova: la
domanda giusta è sempre "questo flusso deve *raggiungere un host diverso da questo, passando di
qui*?", non "quante porte fisiche ha la macchina".

Mini-schema del caso reale (30 ott 2025) — **due** interfacce, **zero** regole FORWARD:

```
   Internet ──(Router)── [eth1] WEBSERVER [eth2] ──(link dedicato)── DB server
                                    │                     │
                          traffico che NASCE/MUORE   traffico che NASCE/MUORE
                          sul webserver:             sul webserver:
                          lui è server HTTPS,        lui è client Postgres
                          lui è client DNS           verso il DB (5432)
                          → INPUT/OUTPUT             → INPUT/OUTPUT
```

Nessuna delle due interfacce porta un flusso "di passaggio verso un terzo host": `eth1` porta solo
ciò che riguarda il webserver in prima persona (server HTTPS verso Internet, client DNS), `eth2`
idem (client Postgres verso il DB). Quindi `FORWARD` resta **vuota** anche con due schede. (Se
invece dietro `eth2` ci fosse una rete che il webserver deve far comunicare con Internet
*attraverso di sé*, allora sì: quel flusso sarebbe FORWARD e il webserver farebbe da router per
quel flusso. Non è questo il caso: il DB parla solo col webserver.)

Riferimento: `procedura_operativa_iptables.md` §3-4, `guida_esame_iptables.md` §4.1-4.2

## Chiarimenti prima di iniziare (dubbi comuni, non solo di questo esercizio)

- **`-i`/`-o` vs `-s`/`-d`**: `-i`/`-o` prendono **il nome dell'interfaccia locale** (`eth1`,
  `eth2`...), mai un indirizzo IP — dicono "da/verso quale porta fisica/virtuale di questa
  macchina". `-s`/`-d` prendono un **indirizzo IP** (o una rete, es. `172.20.0.0/20`) e guardano
  dentro il pacchetto chi l'ha mandato/a chi è diretto. Sono due criteri indipendenti: puoi usarli
  insieme (`-i eth1 -s 172.20.0.0/20`) per essere più precisi, ma non sono intercambiabili. Ricorda
  che i nomi delle interfacce sono **locali a ogni macchina**: l'`eth1` di questo host non ha nulla a
  che vedere con l'`eth1` di un altro host del disegno — condividono il nome per caso. Nello script
  di questo host usi **solo** i nomi delle sue interfacce, mai quelli letti accanto ad altri host.
- **`<tcp|udp>` nei template**: è solo una notazione per dire "scegli uno dei due secondo il
  servizio" — non va mai copiato alla lettera. Sostituiscilo con `tcp` o `udp` guardando cosa
  chiede la consegna per quella porta.
- **`--dport` vs `--sport`, e se il numero di porta cambia**: `--dport` = porta di
  **destinazione** (dove il pacchetto è diretto); `--sport` = porta di **sorgente** (da dove
  parte). Nella richiesta usi `--dport <porta_servizio>` (stai andando verso il servizio); nella
  risposta usi `--sport <stessa_porta>` (è il servizio a parlare, ora da lì). **Il numero di porta
  non cambia mai tra richiesta e risposta** — cambia solo quale dei due flag lo tiene, perché è
  cambiata la direzione del pacchetto. Eccezione da ricordare: NTP usa 123 su entrambi i lati,
  quindi lì una stessa riga ha sia `--dport 123` sia `--sport 123`.
- **Quando NON è mai FORWARD**: un host di questo tipo non ha nulla da mettere in `FORWARD` — se
  ti ritrovi a scrivere una riga `FORWARD` qui, è quasi certamente un errore concettuale (stai
  probabilmente confondendo questo host con il router, oppure hai un flusso che in realtà deve
  raggiungere un terzo host attraverso di lui — allora *è* un router per quel flusso, e ti serve
  anche una porzione di `template_ipt-router.md`). Chiediti sempre, per OGNI flusso: questo
  traffico *nasce o muore su questa macchina* (sì → `INPUT`/`OUTPUT`, sempre e solo **una**
  interfaccia per riga, `-i` da sola o `-o` da sola, mai entrambe insieme) o deve *proseguire
  verso un host diverso da questo* (allora è FORWARD, anche se il diagramma lo chiama "server")?

```bash
#!/bin/bash

# --- 1. Ripulisci lo stato precedente (rilanciabile senza accumulare regole) ---
iptables -F INPUT
iptables -F OUTPUT
iptables -F FORWARD

# --- 2. Loopback sempre permesso ---
iptables -A INPUT -i lo -j ACCEPT
iptables -A OUTPUT -o lo -j ACCEPT

# --- 3. Regole di servizio ---
# Per OGNI riga della consegna che coinvolge questo host, chiediti prima:
# questo host è chi INIZIA la connessione (client per quel flusso) o chi
# la RICEVE (server per quel flusso)? Scrivi la coppia corrispondente.
#
# Se questo host INIZIA (es. il Client che accede a un servizio altrove):
#   iptables -A OUTPUT -p <tcp|udp> --dport <porta_servizio> -j ACCEPT
#   iptables -A INPUT  -p <tcp|udp> --sport <porta_servizio> -m state --state ESTABLISHED -j ACCEPT
#
# Se questo host RICEVE (es. il Server che offre un servizio):
#   iptables -A INPUT  -p <tcp|udp> --dport <porta_servizio> -j ACCEPT
#   iptables -A OUTPUT -p <tcp|udp> --sport <porta_servizio> -m state --state ESTABLISHED -j ACCEPT
#
# ⚠️ Se la consegna dice "da/verso qualsiasi host" per l'altro estremo, NON
# aggiungere -s/-d: l'assenza del match è come dire "chiunque va bene".
# ⚠️ Eccezione NTP: porta 123 su entrambi i lati, stessa riga ha sia --dport
# sia --sport 123 (non è lo schema dport-richiesta/sport-risposta standard).

# <<< scrivi qui le tue righe -A, una coppia per servizio >>>

# --- 4. Policy di default, sempre per ultime ---
# Realizzano da sole "qualsiasi altro pacchetto va scartato": non serve un
# DROP esplicito in fondo, basta non aver accettato nulla di indesiderato sopra.
iptables -P INPUT DROP
iptables -P OUTPUT DROP
iptables -P FORWARD DROP
```
