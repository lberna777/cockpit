# Appunti — Modulo 3D: Networking di Base
**Corso**: Lab Amministrazione di Sistemi T  
**Stato**: 🔄 Teoria + ip a/ip r eseguiti; esercizi 2–6 (ping, ss, DNS, hosts, tcpdump) da completare  
**Riferimento**: `claudeLezioni/LEZIONI SYSADM/lezione_modulo3D_networking_base.md`

---

## 1. Modello concettuale — Internet e reti IP

Internet è una rete di reti: ogni sottorete IP è un'isola connessa alle altre da **router** (o **gateway**).

```
[Network IP A] --- Router --- [Network IP B] --- Router --- [Network IP C]
```

> **Router vs gateway** — sono quasi sinonimi in questo contesto. *Router* è il nome del dispositivo fisico che invia (routes) i pacchetti tra reti. *Gateway* è il nome logico del "punto di uscita" di una rete verso le altre: quando la VM deve mandare un pacchetto fuori dalla sua subnet, lo consegna al gateway. Il modem wifi di casa è entrambe le cose: è un router che connette la LAN domestica alla rete dell'ISP, ed è il gateway della LAN domestica. In VirtualBox NAT, il gateway è `10.0.2.2`.

Ogni host ha due tipi di indirizzo:
- **IP** — identifica l'host a livello logico, univoco su Internet
- **MAC** — identifica l'interfaccia fisica, valido solo all'interno della LAN locale

> **La distinzione chi/dove** — La confusione è comprensibile perché sembrano ridondanti. La differenza è il *livello* a cui operano.  
> - L'IP dice "questa macchina si chiama 82.1.2.3" — e questo è valido ovunque nel mondo, su qualunque rete.  
> - Il MAC dice "questa scheda di rete ha il seriale 08:00:27:8d:c0:4d" — ma funziona solo sul tratto di cavo (o wifi) a cui la scheda è fisicamente collegata.  
> Analogia: l'IP è il tuo numero di telefono (unico nel mondo), il MAC è il numero di posto in un'aula specifica (utile solo in quell'aula).

### Come funziona l'invio di un pacchetto — il ruolo di ARP

Quando vuoi mandare dati a `192.168.1.76` sulla stessa LAN:
1. Sai l'IP di destinazione, ma Ethernet richiede un MAC per consegnare il frame sulla rete locale
2. Il tuo host manda in **broadcast** (a tutti): *"chi ha l'IP 192.168.1.76?"*
3. L'host con quell'IP risponde in unicast con il suo MAC
4. Tutti gli host che hanno sentito la risposta la salvano nella loro **ARP cache** per evitare di richiedere ogni volta

> **A cosa serve ARP nel pratico** — I pacchetti IP devono attraversare reti fisiche (Ethernet, WiFi) che usano indirizzi MAC, non IP. ARP è il traduttore tra i due livelli. Succede ogni volta che mandi dati, ma è invisibile: il kernel gestisce tutto automaticamente. Per vederlo: `arp -n` sulla VM mostra la cache ARP corrente.  
> Il concetto di "pacchetto" è semplicemente l'unità di dati che viaggia su IP: un blocco di byte con un'intestazione (IP sorgente, IP destinazione, protocollo) e un payload (i dati veri, che siano una richiesta HTTP, un chunk di file, una risposta DNS...). Tutto il traffico di rete è fatto di pacchetti.

---

## 2. Indirizzi IP, netmask, CIDR

Un indirizzo IPv4 è 32 bit divisi in:
- **net-id** — identifica la rete (i bit a sinistra della netmask)
- **host-id** — identifica l'host all'interno di quella rete (i bit a destra)

> **host-id vs MAC** — Il MAC identifica il dispositivo fisico sulla LAN locale. L'host-id è parte dell'indirizzo IP e serve ai *router* per instradare i pacchetti tra reti diverse. Quando un router riceve un pacchetto diretto a `10.0.2.15/24`, guarda il net-id (`10.0.2.0`) per sapere su quale interfaccia/rete deve spedirlo, poi ARP risolve il MAC finale. MAC e host-id operano a livelli diversi dello stack.

La **netmask** separa i due campi. Esempio con l'output reale della VM:

```
inet 10.0.2.15/24
     ─────────── → indirizzo IP completo
              /24 → CIDR: i primi 24 bit sono net-id, gli ultimi 8 sono host-id

net-id:   10.0.2      (24 bit → i tre ottetti di sinistra)
host-id:  15          (8 bit → l'ottetto di destra)
netmask:  255.255.255.0   (24 uni seguiti da 8 zeri)

Network address: 10.0.2.0    (host-id tutti a 0 → identifica la rete, non assegnabile)
Broadcast:       10.0.2.255  (host-id tutti a 1 → raggiunge tutti gli host della subnet)
```

> **Cos'è una subnet** — È semplicemente l'insieme di tutti gli indirizzi che condividono lo stesso net-id. La VM è nella subnet `10.0.2.0/24`, che comprende gli indirizzi da `10.0.2.1` a `10.0.2.254` (255 escluso = broadcast, 0 escluso = network address). Il router gestisce il confine tra una subnet e l'altra — la tua intuizione è corretta.

### IP privati — perché "non instradati su Internet"

Range riservati alle reti interne (RFC 1918):
- `10.0.0.0/8`
- `172.16.0.0/12`
- `192.168.0.0/16`

> **Cosa significa "non instradato"** — Tutti i router della dorsale Internet sono configurati per scartare i pacchetti con questi indirizzi come sorgente o destinazione. È una convenzione globale: qualunque organizzazione può usare `192.168.x.x` internamente senza coordinarsi con nessuno, proprio perché quei pacchetti non usciranno mai da quella rete. Sono come i numeri di interno di un centralino: validi dentro l'ufficio, ma non raggiungibili dall'esterno senza passare dal centralino (= il NAT).

---

## 3. Porte e servizi

L'IP identifica l'host, ma su un host girano più applicazioni contemporaneamente. Le **porte** le distinguono.

Una connessione è identificata dalla **quintupla**:
```
(protocollo, IP_sorgente, porta_sorgente, IP_destinazione, porta_destinazione)
```

Porte standard (well-known, 0–1023):

| Porta | Servizio | Protocollo |
|-------|----------|------------|
| 22    | SSH      | TCP        |
| 80    | HTTP     | TCP        |
| 443   | HTTPS    | TCP        |
| 53    | DNS      | UDP/TCP    |
| 25    | SMTP     | TCP        |

> **Cosa viaggia nei pacchetti** — I pacchetti IP trasportano nel payload qualunque tipo di dato: richieste HTTP, frammenti di file, query DNS, messaggi SSH... Il protocollo (TCP/UDP) nel livello di trasporto garantisce o non garantisce l'ordine e la consegna. Il "pacchetto" è solo il contenitore.

### TCP — three-way handshake

TCP è **orientato alla connessione**: i due host si sincronizzano prima di scambiarsi dati.

> **"Orientato alla connessione" significa** — TCP tiene traccia dello stato della comunicazione: apertura, trasferimento, chiusura. Prima di inviare dati, i due host stabiliscono un accordo (il three-way handshake) e si sincronizzano sui numeri di sequenza. UDP non fa nulla di tutto questo: manda pacchetti e basta, senza sapere se arrivano.

```
Client                    Server (porta 80)
  │──── SYN ────────────►│   "voglio connettermi, parto dalla sequenza X"
  │◄─── SYN+ACK ─────────│   "ok, ricevuto il tuo X (ACK) — la mia sequenza è Y (SYN)"
  │──── ACK ─────────────►│   "ricevuto il tuo Y"
  │                       │
  │   [qui inizia lo scambio dati]
```

> **Quando arriva il pacchetto? Confusione sul SYN+ACK** — Non arriva nessun dato durante il three-way handshake. Il handshake serve solo a sincronizzare i numeri di sequenza (meccanismo che TCP usa per riordinare i pacchetti e rilevare quelli persi). La sequenza è:  
> 1. SYN: client manda un pacchetto vuoto di controllo con il flag SYN settato  
> 2. SYN+ACK: server risponde con due flag: ACK (ho ricevuto il tuo SYN) + SYN (propongo il mio numero di sequenza)  
> 3. ACK: client conferma il SYN del server  
> Solo dopo questo scambio inizia il trasferimento dati reale. Il "pacchetto" che svolge questo lavoro è un pacchetto TCP di controllo, senza payload utile.

---

## 4. NAT — Network Address Translation

**Il problema**: IPv4 ha ~4 miliardi di indirizzi. Sono già esauriti — assegnati ad aziende, università, ISP negli anni '90 prima che Internet esplodesse.

**La soluzione**: un solo IP pubblico per l'intera rete domestica/aziendale; il router *traduce* gli indirizzi.

```
[Host 10.0.0.5:11111] → Router (IP pubblico 82.1.2.3) → [Server 137.204.1.15:80]
                         ↑ sostituisce l'IP sorgente con 82.1.2.3 + memorizza la traduzione
```

> **Il ruolo del NAT rispetto agli altri indirizzi** — Riassumendo i tre livelli:  
> - **MAC**: consegna un frame Ethernet *all'interno di un singolo tratto di LAN fisica* (da switch a switch, massimo)  
> - **IP privato**: identifica l'host *all'interno della rete privata* (valido solo lì)  
> - **IP pubblico (NAT)**: identifica il *router* che rappresenta l'intera rete privata verso Internet  
> Il MAC non c'entra con il NAT: il MAC non attraversa mai un router, viene sostituito ad ogni hop. Il NAT opera a livello IP, non MAC.

- **SNAT** (Source NAT): sostituisce l'IP sorgente → usato quando un host privato vuole raggiungere Internet
- **DNAT** (Destination NAT): sostituisce l'IP destinazione → usato per rendere raggiungibile dall'esterno un server interno su una porta specifica (es. port forwarding)

---

## 5. VirtualBox — tipi di interfaccia di rete

| Modalità | La VM raggiunge | La VM è raggiungibile da | Uso tipico |
|----------|-----------------|--------------------------|------------|
| **NAT** | Internet (via SNAT) | Solo con port forwarding esplicito | Default Vagrant — navigazione |
| **Bridged** | LAN fisica + Internet | Tutti nella LAN (come un host fisico) | VM visibile in rete reale |
| **Host-only** | Solo l'host | Solo l'host | Lab isolato host↔VM |
| **Internal** | Solo altre VM dello stesso gruppo | Solo VM dello stesso gruppo | Lab VM↔VM senza host |

> **NAT in VirtualBox nel pratico** — VirtualBox crea un mini-router software interno. La VM ha sempre IP `10.0.2.15`, il gateway è sempre `10.0.2.2` (il router virtuale di VirtualBox). Quando la VM fa una richiesta verso internet, VirtualBox fa SNAT: sostituisce `10.0.2.15` con l'IP reale del tuo Mac/PC, manda la richiesta, e quando arriva la risposta la gira alla VM. Per raggiungere la VM dall'host si usa il port forwarding (DNAT): `vagrant ssh` funziona perché Vagrant ha configurato il forwarding da `localhost:2222` a `VM:22`.

> **Host-only nel pratico** — VirtualBox crea un'interfaccia di rete virtuale sull'host (tipo un secondo adattatore ethernet, ma virtuale). Host e VM condividono una subnet `192.168.56.0/24`. L'host prende `.1`, la VM prende l'IP configurato. Non c'è accesso a internet da questa interfaccia — è un canale diretto host↔VM. Usato per comunicare con la VM in modo stabile (IP fisso) indipendentemente dal NAT.

> **Internal network nel pratico** — Come host-only ma l'host non partecipa. Solo le VM con lo stesso nome di rete interna si vedono. Usato per simulare reti isolate tra VM (es. un server web e un database che non devono essere raggiungibili dall'esterno).

> **LAN** = Local Area Network — la rete locale (casa, ufficio, VM dello stesso gruppo). **Port forwarding** = DNAT: reindirizza il traffico che arriva su una porta dell'host verso una porta della VM.

---

## 6. Configurazione di rete su Linux

### `ip a` — lettura dell'output reale dalla VM

```
vagrant@bookworm:~$ ip a
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 ...
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    inet 127.0.0.1/8 scope host lo
    inet6 ::1/128 scope host noprefixroute

2: eth0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 ...
    link/ether 08:00:27:8d:c0:4d brd ff:ff:ff:ff:ff:ff    ← MAC address
    altname enp0s3
    inet 10.0.2.15/24 brd 10.0.2.255 scope global dynamic eth0    ← IPv4
    inet6 fd17:625c:f037:2:a00:27ff:fe8d:c04d/64 scope global dynamic mngtmpaddr  ← IPv6 globale
    inet6 fe80::a00:27ff:fe8d:c04d/64 scope link                                  ← IPv6 link-local
```

> **Interfaccia `lo` (loopback)** — Non è una scheda di rete reale. È un'interfaccia virtuale del kernel usata dai processi per comunicarsi internamente (es. un'app che parla con un database locale usa `127.0.0.1`). È sempre UP anche senza hardware di rete. `00:00:00:00:00:00` come MAC è fittizio.

> **L'IP è fisso o dinamico?** — La parola `dynamic` nell'output di `ip a` dice che l'IP è stato assegnato via DHCP (Dynamic Host Configuration Protocol), non configurato staticamente. Il `valid_lft 86313sec` è la durata del lease DHCP — dopo quel tempo va rinnovato. In pratica VirtualBox assegna sempre `10.0.2.15` alla prima VM NAT, ma tecnicamente potrebbe cambiare.

> **Come leggere gli IPv6** — Ci sono due indirizzi IPv6 per eth0:  
> 1. `fd17:625c:f037:2:.../64` con `scope global` — IPv6 globale (instradabile, equivale all'IP pubblico IPv6)  
> 2. `fe80::a00:27ff:fe8d:c04d/64` con `scope link` — IPv6 link-local: prefisso `fe80::/10`, valido solo sulla LAN locale, presente su ogni interfaccia IPv6 sempre  
> Per ora è sufficiente sapere che `fe80:...` è locale, `fd17:...` (o `2001:...` per IP veri) è globale.

### `ip r` — lettura della tabella di routing

```
vagrant@bookworm:~$ ip r
default via 10.0.2.2 dev eth0
10.0.2.0/24 dev eth0 proto kernel scope link src 10.0.2.15
```

> **Come leggere ogni riga**:  
> - `default via 10.0.2.2 dev eth0` → regola default: qualunque pacchetto diretto a un IP che non conosco, mandalo a `10.0.2.2` (il gateway NAT di VirtualBox) tramite l'interfaccia eth0  
> - `10.0.2.0/24 dev eth0 proto kernel scope link src 10.0.2.15` → regola per la subnet locale: i pacchetti diretti a qualunque IP in `10.0.2.0/24` vengono consegnati direttamente su eth0 (senza passare da un gateway), usando `10.0.2.15` come IP sorgente. `proto kernel` = aggiunta automaticamente dal kernel quando l'IP è stato assegnato all'interfaccia.

Con `ip a show eth0` puoi filtrare l'output a una sola interfaccia — già eseguito ✅.

---

## 7. Strumenti di monitoraggio

> ⚠️ Questa sezione non era presente negli appunti grezzi — gli esercizi 2–6 non sono stati eseguiti. Contenuto dalla lezione di riferimento.

### `ping` — verifica connettività

```bash
ping -c 3 10.0.2.2       # gateway NAT (deve rispondere)
ping -c 3 8.8.8.8        # DNS Google (verifica uscita internet)
ping -c 3 192.168.56.1   # host fisico (se hai interfaccia host-only)
```

Output: `time=12.3 ms` è la latenza round-trip; `ttl=117` è il numero di router attraversabili prima che il pacchetto venga scartato.

### `ss` — porte in ascolto e connessioni attive

```bash
ss -tlnp    # TCP, Listen, Numeric, con Processo → mostra servizi esposti
ss -tnap    # tutte le connessioni TCP attive (inclusa la sessione SSH)
```

| Flag | Significato |
|------|-------------|
| `-t` | Solo TCP |
| `-u` | Solo UDP |
| `-l` | Solo LISTEN |
| `-a` | Tutti gli stati |
| `-n` | No risoluzione nomi |
| `-p` | Mostra il processo |

Lettura output:
```
State   Recv-Q  Send-Q  Local Address:Port  Peer Address:Port
LISTEN  0       128     0.0.0.0:22          0.0.0.0:*          sshd
```
- `0.0.0.0:22` = SSH in ascolto su *tutte* le interfacce, porta 22 → raggiungibile dall'esterno
- `127.0.0.1:3306` (esempio) = MySQL in ascolto solo su loopback → non raggiungibile dall'esterno

### `traceroute` — percorso dei pacchetti

```bash
traceroute 8.8.8.8    # mostra ogni router (hop) con latenza
```

### `tcpdump` — cattura pacchetti in tempo reale

```bash
sudo tcpdump -i eth0 icmp           # cattura solo ICMP (ping)
sudo tcpdump -i eth0 port 80        # solo HTTP
sudo tcpdump -i eth0 host 10.0.2.2  # solo traffico verso/da gateway
```

---

## 8. Risoluzione dei nomi (DNS)

> ⚠️ Questa sezione non era presente negli appunti grezzi — esercizi 4–5 non eseguiti.

La sequenza quando scrivi `ping google.com`:

1. Il kernel consulta `/etc/nsswitch.conf` → `hosts: files dns` → prima `/etc/hosts`, poi DNS
2. `/etc/hosts` — file locale, editabile, ha priorità:
   ```
   127.0.0.1   localhost
   ```
3. `/etc/resolv.conf` — server DNS da interrogare:
   ```
   nameserver 10.0.2.3    # DNS di VirtualBox (in modalità NAT)
   ```

Strumenti:
```bash
getent hosts www.unibo.it      # usa NSS (rispetta /etc/hosts)
host www.unibo.it              # DNS diretto
dig www.unibo.it               # DNS con dettagli tecnici
cat /etc/hosts
cat /etc/resolv.conf
```

---

## Stato esercizi

| Esercizio | Contenuto | Stato |
|-----------|-----------|-------|
| Es. 1 | `ip a`, `ip r` — lettura interfacce e routing | ✅ Eseguito |
| Es. 2 | `ping` verso gateway, internet, host | ⬜ Da eseguire |
| Es. 3 | `ss -tlnp`, `ss -tnap` — porte in ascolto | ⬜ Da eseguire |
| Es. 4 | DNS: `/etc/hosts`, `/etc/resolv.conf`, `getent`, `dig` | ⬜ Da eseguire |
| Es. 5 | Aggiungere alias in `/etc/hosts` | ⬜ Da eseguire |
| Es. 6 | `tcpdump` + ping (opzionale) | ⬜ Da eseguire |

**Prossimo step**: riprendere dalla VM con Es. 2–6 nell'ordine. Le domande aperte qui sopra sono già risolte — leggi le risposte prima di eseguire, poi esegui e scrivi eventuali nuovi dubbi.

---

## Connessione con Security S1

- `ss -tlnp` e Nmap vedono le stesse porte, da prospettive opposte (difensore vs attaccante)
- Il three-way handshake spiega la differenza tra `-sT` (handshake completo) e `-sS` (SYN scan, non completa)
- `0.0.0.0:22` = superficie d'attacco esposta; `127.0.0.1:3306` = non raggiungibile dall'esterno
- L'interfaccia `lo` risponde ai ping locali ma non è visibile da altre macchine

<!-- AUTO-LINKS:START -->
## 🔗 Collegati

- [[Appunti_modulo3D]]
- [[guida_lab_modulo3D_networking_base]]
- [[lezione_modulo3D_networking_base]]

**Hub:** [[master_map_studio]] · [[glossario_sysadm]] · [[concept_maps]] · [[troubleshooting_vm]] · [[metodo_studio_esami_pratici]]
<!-- AUTO-LINKS:END -->
