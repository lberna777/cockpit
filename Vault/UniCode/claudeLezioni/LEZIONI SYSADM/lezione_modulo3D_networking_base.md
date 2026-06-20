# Lezione — Modulo 3D: Networking di Base
**Corso**: Lab Amministrazione di Sistemi T  
**Materiale**: `net-config.pdf` (Linux Networking, Prandini), `servizi_base_rete.pdf` (Servizi rete infrastrutturali, Prandini)  
**Prerequisiti**: 0A (filesystem), 3A (systemd — i servizi di rete sono demoni), 3E (Vagrant multi-machine — richiede comprensione delle reti VM)

---

## Obiettivo
Al termine di questa lezione Lorenzo deve saper leggere l'output di `ip a`, verificare la connettività con `ping`, controllare le porte in ascolto con `ss`, e capire come la VM Debian è connessa alla rete in ambiente VirtualBox/Vagrant.

---

## 1. Come funziona Internet — modello concettuale

Internet è una **rete di reti**: ogni sottorete IP (network IP) è un'isola. Le isole sono collegate da **router** (o gateway), apparati specializzati che inoltrano i pacchetti da una rete all'altra.

```
[Network IP A] --- Router --- [Network IP B] --- Router --- [Network IP C]
```

Ogni host ha un **indirizzo IP** (globale, univoco su Internet) e un **indirizzo MAC** (locale, valido solo all'interno della LAN).

### Perché due indirizzi distinti?
- L'IP identifica la destinazione a livello logico (chi sei nel mondo)
- Il MAC identifica l'interfaccia fisica sulla LAN locale (dove sei adesso)

Il protocollo **ARP (Address Resolution Protocol)** traduce un IP in MAC quando si deve recapitare un pacchetto sulla LAN locale:
1. L'host che vuole comunicare invia in broadcast: *"chi ha l'IP 192.168.1.76?"*
2. Il destinatario risponde in unicast: *"sono io, il mio MAC è bb:2c:eb:18:f6:c8"*
3. La risposta viene cachata da tutti gli host che l'hanno vista

---

## 2. Indirizzi IP, netmask, CIDR

Un indirizzo IPv4 è composto da 32 bit, divisi in due parti:
- **net-id**: identifica la rete
- **host-id**: identifica l'host all'interno della rete

La **netmask** specifica dove cade il confine tra le due parti:
```
Indirizzo:  144.156.166.151
Netmask:    255.255.255.192   (/26 in notazione CIDR)
            11111111.11111111.11111111.11000000
                                        ↑ i 6 bit finali sono host-id
```

La notazione **CIDR** `/N` indica quanti bit sono dedicati al net-id:
- `/24` → 256 indirizzi, netmask `255.255.255.0`
- `/26` → 64 indirizzi, netmask `255.255.255.192`

Due indirizzi speciali in ogni subnet:
- **Network address** (host-id tutti a 0): identifica la rete, non assegnabile a host
- **Broadcast** (host-id tutti a 1): usato per raggiungere tutti gli host della subnet

### IP privati (RFC 1918)
Questi range sono riservati alle reti interne e **non vengono instradati su Internet**:
- `10.0.0.0/8`
- `172.16.0.0/16` – `172.31.0.0/16`
- `192.168.0.0/24` – `192.168.255.0/24`

---

## 3. Porte e servizi — come un host espone applicazioni

L'indirizzo IP identifica un host, ma su un host girano più applicazioni contemporaneamente. Il livello di trasporto aggiunge le **porte** per distinguerle.

Una connessione è identificata dalla **quintupla**:
```
(protocollo, IP_sorgente, porta_sorgente, IP_destinazione, porta_destinazione)
```

**Porte standard** (well-known, 0–1023):
| Porta | Servizio | Protocollo |
|-------|----------|------------|
| 22    | SSH      | TCP        |
| 80    | HTTP     | TCP        |
| 443   | HTTPS    | TCP        |
| 53    | DNS      | UDP/TCP    |
| 25    | SMTP     | TCP        |

Un **servizio in ascolto** è un processo che ha aperto una porta e aspetta connessioni. Su Linux: `ss -tlnp` mostra tutti i processi in ascolto.

### TCP — come si apre una connessione (three-way handshake)
TCP è un protocollo **orientato alla connessione**: prima di scambiarsi dati, i due host si sincronizzano:

```
Client          Server (porta 80)
  │──── SYN ────────►│   "voglio aprire una connessione"
  │◄─── SYN+ACK ─────│   "ok, confermo — e tu conferma me"
  │──── ACK ─────────►│   "confermato"
  │                   │
  │ [scambio dati]    │
```

- **SYN** (synchronize): pacchetto che inizia la connessione
- **ACK** (acknowledge): conferma che il pacchetto precedente è arrivato
- Dopo il three-way handshake la connessione è **ESTABLISHED**

> Questo è il meccanismo che Nmap `-sS` (SYN scan) sfrutta: manda solo il SYN e non completa l'handshake, quindi nei log del server appare una connessione a metà — più difficile da tracciare.

---

## 4. NAT — Network Address Translation

Problema: gli IP pubblici sono scarsi, ma ogni rete domestica/aziendale ha decine di host.  
Soluzione: un solo IP pubblico per tutta la rete, il router **traduce** gli indirizzi.

```
[Host 10.0.0.5:11111] → Router (IP pubblico 82.1.2.3) → [Server 137.204.1.15:80]
                         ↑ modifica l'IP sorgente in 82.1.2.3
```

Il router memorizza una tabella di traduzione per sapere a quale host interno girare le risposte.

**SNAT** (Source NAT): sostituisce l'IP sorgente → usato per dare accesso a Internet a host privati  
**DNAT** (Destination NAT): sostituisce l'IP destinazione → usato per rendere raggiungibile dall'esterno un server interno su una porta specifica

---

## 5. VirtualBox — tipi di interfaccia di rete

VirtualBox permette di connettere ogni VM in modi diversi. È cruciale capirli per i lab.

| Modalità | La VM può raggiungere | La VM è raggiungibile da | Uso tipico |
|----------|-----------------------|--------------------------|------------|
| **NAT** | Internet (tramite SNAT) | Solo con port forwarding | Default — navigazione |
| **Bridged** | LAN fisica + Internet | Tutti nella stessa LAN | VM come host reale |
| **Host-only** | Solo l'host | Solo l'host | Lab isolato host↔VM |
| **Internal** | Solo altre VM nella stessa internal network | Solo altre VM dello stesso gruppo | Lab VM↔VM isolato |

### NAT in VirtualBox
- VirtualBox fa da router SNAT: la VM ha IP `10.0.2.15`, il gateway è `10.0.2.2`
- Per raggiungere la VM dall'host serve port forwarding (DNAT):
  ```ruby
  # Vagrantfile
  config.vm.network "forwarded_port", guest: 22, host: 2222
  ```

### Host-only in VirtualBox
- Crea una rete virtuale tra host e VM sulla subnet `192.168.56.0/24`
- L'host ottiene `192.168.56.1`, la VM ottiene un IP nel range
- In Vagrant:
  ```ruby
  config.vm.network "private_network", ip: "192.168.56.10"
  ```

### Internal network
- Rete totalmente virtuale tra VM, l'host non partecipa
- In Vagrant:
  ```ruby
  config.vm.network "private_network", virtualbox__intnet: "LAN1"
  ```

---

## 6. Configurazione di rete su Linux

### Visualizzare la configurazione attuale

```bash
ip a                    # mostra tutte le interfacce e i loro indirizzi
ip a show eth0          # solo l'interfaccia eth0
ip r                    # mostra la tabella di routing
```

**Leggere l'output di `ip a`:**
```
2: enp0s3: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 ...
    link/ether 08:00:27:16:e5:88 brd ff:ff:ff:ff:ff:ff    ← MAC address
    inet 10.0.2.15/24 brd 10.0.2.255 ...                  ← IPv4 con netmask /24
    inet6 fd17:625c:f037:2:db52:... /64 ...                ← IPv6 globale
    inet6 fe80::5e81:84f8:56ea:a4fa/64 ...                 ← IPv6 link-local (sempre presente)
```

**Interfaccia `lo` (loopback):**
- Interfaccia virtuale interna al kernel, non esce mai sulla rete fisica
- IP fisso `127.0.0.1` (IPv4) e `::1` (IPv6)
- Usata dai processi per comunicare con altri processi sullo stesso host (es. database locale)
- È sempre in stato UP anche senza scheda di rete fisica

**Leggere la tabella di routing:**
```bash
ip r
# default via 10.0.2.2 dev enp0s3        ← default gateway: tutto ciò che non conosco va qui
# 10.0.2.0/24 dev enp0s3 proto kernel    ← subnet locale, consegna diretta
# 192.168.56.0/24 dev enp0s8 proto kernel ← seconda subnet locale (host-only)
```

### Modificare la configurazione (runtime — non persiste al reboot)

```bash
# Aggiungere un indirizzo IP a un'interfaccia
sudo ip a add 192.168.56.10/24 dev eth1

# Rimuovere un indirizzo IP
sudo ip a del 192.168.56.10/24 dev eth1

# Aggiungere una route
sudo ip r add 10.10.0.0/24 via 192.168.56.1

# Rimuovere una route
sudo ip r del 10.10.0.0/24
```

### Configurazione persistente su Debian (`/etc/network/interfaces`)

```bash
# Interfaccia con IP statico
auto eth1
iface eth1 inet static
    address 192.168.56.10
    netmask 255.255.255.0
    gateway 192.168.56.1

# Interfaccia con DHCP
auto eth0
iface eth0 inet dhcp
```

Applicare le modifiche senza reboot:
```bash
sudo systemctl restart networking
# oppure per singola interfaccia:
sudo ifup eth1
sudo ifdown eth1
```

---

## 7. Strumenti di monitoraggio

### `ping` — verifica connettività di base

```bash
ping 8.8.8.8            # testa connettività verso Google DNS
ping -c 4 192.168.56.1  # solo 4 pacchetti
ping hostname           # risolve il nome prima di pingare
```

Cosa dice l'output:
```
PING 8.8.8.8: 64 bytes from 8.8.8.8: icmp_seq=1 ttl=117 time=12.3 ms
```
- `ttl`: quanti router può attraversare il pacchetto prima di essere scartato
- `time`: latenza round-trip in millisecondi

### `ss` — stato delle connessioni e porte in ascolto

```bash
ss -tlnp   # TCP, Listen, Numeric (no risoluzione nomi), con Processo
ss -tunap  # TCP+UDP, tutte le connessioni (incluso ESTABLISHED), Numeric, con Processo
```

| Flag | Significato |
|------|-------------|
| `-t` | Solo TCP |
| `-u` | Solo UDP |
| `-l` | Solo porte in LISTEN (in ascolto) |
| `-a` | Tutti gli stati (LISTEN + ESTABLISHED + ...) |
| `-n` | Non risolvere IP/porte in nomi simbolici |
| `-p` | Mostra il processo che usa la socket |

Output tipico:
```
State   Recv-Q  Send-Q  Local Address:Port  Peer Address:Port  Process
LISTEN  0       128     0.0.0.0:22          0.0.0.0:*          users:(("sshd",pid=789))
```
- `0.0.0.0:22` = SSH in ascolto su tutte le interfacce, porta 22
- `127.0.0.1:3306` = MySQL in ascolto solo sull'interfaccia locale (non raggiungibile dall'esterno)

### `traceroute` — percorso dei pacchetti

```bash
traceroute 8.8.8.8
```
Mostra ogni router (hop) attraversato dal pacchetto fino alla destinazione, con latenza per ogni salto.

### `tcpdump` — cattura pacchetti

```bash
sudo tcpdump -i eth0              # cattura tutto il traffico su eth0
sudo tcpdump -i eth0 port 80      # solo traffico HTTP
sudo tcpdump -i eth0 host 10.0.2.2
```

---

## 8. Risoluzione dei nomi (DNS)

Quando scrivi `ping google.com`, il sistema deve tradurre `google.com` in un IP. La sequenza è:

1. **NSS (Name Service Switch)**: controlla `/etc/nsswitch.conf` per sapere dove cercare
   ```
   hosts: files dns     ← prima /etc/hosts, poi DNS
   ```

2. **`/etc/hosts`** — file locale, consultato per primo
   ```
   127.0.0.1   localhost
   192.168.56.10   server-web
   8.8.8.8     gdns.google.com
   ```

3. **DNS** — interroga i server configurati in `/etc/resolv.conf`
   ```
   nameserver 8.8.8.8      ← server DNS da interrogare
   nameserver 8.8.4.4      ← server di fallback
   domain unibo.it         ← dominio di default per nomi parziali
   ```

### Strumenti di debug DNS

```bash
getent hosts www.unibo.it          # usa NSS (rispetta /etc/hosts + DNS)
host www.unibo.it                  # query DNS diretta
dig www.unibo.it                   # query DNS con dettagli tecnici
dig mx unibo.it                    # record MX (mail exchanger)
dig ns unibo.it                    # name server autorevoli
host www.unibo.it 8.8.8.8         # interroga un server DNS specifico
```

---

## Comandi di Riferimento

| Comando | Descrizione |
|---------|-------------|
| `ip a` | Mostra interfacce di rete e indirizzi IP |
| `ip r` | Mostra la tabella di routing |
| `ip a add ADDR/MASK dev IF` | Aggiunge indirizzo IP all'interfaccia |
| `ip r add NET/MASK via GW` | Aggiunge una route |
| `ping HOST` | Verifica connettività ICMP |
| `ping -c N HOST` | Ping con N pacchetti |
| `ss -tlnp` | Porte TCP in ascolto con processo |
| `ss -tunap` | Tutte le connessioni TCP+UDP |
| `traceroute HOST` | Percorso dei pacchetti |
| `tcpdump -i IF` | Cattura traffico sull'interfaccia |
| `getent hosts NOME` | Risolve nome tramite NSS |
| `host NOME` | Query DNS diretta |
| `dig NOME` | Query DNS con dettagli |
| `cat /etc/hosts` | File di risoluzione locale |
| `cat /etc/resolv.conf` | Server DNS configurati |
| `cat /etc/nsswitch.conf` | Ordine di risoluzione nomi |

---

## Esercizi Guidati

> **Prima di iniziare**: avvia la VM con `cd ~/sysAdmin-lab && vagrant up && vagrant ssh`

### Esercizio 1 — Esplorare le interfacce di rete

```bash
# Visualizza tutte le interfacce
ip a

# Rispondi:
# - Quante interfacce ci sono?
# - Qual è l'interfaccia NAT (IP nella subnet 10.x)?
# - Qual è l'interfaccia host-only (IP nella subnet 192.168.x)?
# - Cosa rappresenta l'interfaccia "lo"?

# Visualizza la tabella di routing
ip r

# Rispondi:
# - Qual è il default gateway?
# - Quante subnet conosce direttamente la VM?
```

### Esercizio 2 — Verifica connettività

```bash
# Ping verso il gateway NAT di VirtualBox
ping -c 3 10.0.2.2

# Ping verso Internet
ping -c 3 8.8.8.8

# Ping verso l'host (interfaccia host-only)
ping -c 3 192.168.56.1

# Se un ping fallisce, perché? (firewall? route mancante? host spento?)
```

### Esercizio 3 — Porte in ascolto sulla VM

```bash
# Mostra tutte le porte TCP in ascolto
ss -tlnp

# Domande:
# - SSH (porta 22) è in ascolto? Su quale indirizzo?
# - Ci sono altri servizi in ascolto?

# Mostra tutte le connessioni attive (inclusa la tua sessione SSH)
ss -tnap

# Identifica la connessione SSH corrente:
# - qual è il tuo IP (client)?
# - qual è la porta sorgente? e quella destinazione?
```

### Esercizio 4 — Risoluzione dei nomi

```bash
# Consulta /etc/hosts
cat /etc/hosts

# Consulta /etc/resolv.conf
cat /etc/resolv.conf

# Risolvi un nome tramite NSS
getent hosts localhost
getent hosts www.unibo.it

# Risolvi con DNS diretto
host www.unibo.it
dig www.unibo.it
```

### Esercizio 5 — Aggiungere un alias locale

```bash
# Aggiungi una voce in /etc/hosts
echo "192.168.56.1 host-mac" | sudo tee -a /etc/hosts

# Verifica che funzioni
ping -c 2 host-mac
getent hosts host-mac
```

### Esercizio 6 — Cattura traffico con tcpdump (opzionale)

```bash
# In un terminale: avvia la cattura su enp0s3
sudo tcpdump -i enp0s3 icmp

# In un altro terminale (o dopo Ctrl+C e riprendi):
ping -c 3 8.8.8.8

# Osserva i pacchetti ICMP catturati
# Quante righe per ogni ping? (request + reply = 2)
```

---

## Connessioni

**Con SysAdmin 3A (systemd)**: i servizi di rete (SSH, DNS, DHCP) sono demoni gestiti da systemd. `ss -tlnp` mostra gli stessi processi che vedi con `systemctl list-units --type=service`.

**Con SysAdmin 3E (Vagrant multi-machine)**: le modalità NAT, host-only e internal definite in questa lezione sono esattamente le direttive `config.vm.network` del Vagrantfile. Senza questa lezione il Vagrantfile multi-machine è incomprensibile.

**Con Security S1 (Nmap e enumerazione)**:
- Nmap scansiona le porte che `ss -tlnp` mostra — stessa informazione, prospettive opposte
- Il three-way handshake spiegato al §3 è il meccanismo che differenzia `-sT` da `-sS`
- L'interfaccia `lo` risponde a ping locali ma non è visibile dall'esterno
- La distinzione tra `0.0.0.0:22` (raggiungibile da fuori) e `127.0.0.1:3306` (solo locale) è il concetto chiave di "superficie d'attacco esposta"

---

## Riepilogo

- **`ip a` / `ip r`**: comandi fondamentali per leggere la configurazione di rete corrente
- **`ss -tlnp`**: mostra quali servizi sono esposti su quali porte — base per capire la superficie d'attacco
- **VirtualBox networking**: NAT (uscita internet), host-only (comunicazione host↔VM), internal (VM↔VM) — configurabile in Vagrant con `config.vm.network`
- **DNS**: la risoluzione nomi segue NSS → `/etc/hosts` → server DNS in `/etc/resolv.conf`
- **three-way handshake TCP**: SYN → SYN+ACK → ACK — la base del funzionamento di ogni servizio TCP e delle tecniche di scansione Nmap

<!-- AUTO-LINKS:START -->
## 🔗 Collegati

- [[Appunti_modulo3D]]
- [[appunti_modulo3D_networking_base]]

**Hub:** [[master_map_studio]] · [[glossario_sysadm]] · [[concept_maps]] · [[troubleshooting_vm]] · [[metodo_studio_esami_pratici]]
<!-- AUTO-LINKS:END -->
