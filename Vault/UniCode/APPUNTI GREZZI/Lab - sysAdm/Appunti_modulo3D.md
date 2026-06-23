
Internet è una composizione di reti connesse tra di loro, ognuna di queste reti si chiama **network IP**. vari network ip sono connessi tra di loro tramite **router** (tipo il modem del wifi?) o **gateway** (cosa sono?) che servono a far comunicare reti tra di loro.

ogni **host** (dispositivo collegato in rete) ha un **indirizzo IP** e un **indirizzo MAC**

1. L'indirizzo IP identifica l'host globalmente ed è univoco su tutto l'internet
2. l'indrizzo MAC identifica il dispositivo fisico nella rete locale (LAN)
non capisco bene però la distinzione tra il chi e il dove che fai tra i due indirizzi, a me sembrano solo un modo di identificarsi globalmente e localmente.

A cosa serve nel pratico il protocollo ARP? capisco che a un interrogazione che chiede l'identificazione mediante IP faccia rispondere all'interessato il suo MAC, ma non capisco come funziona e che scopo abbia.
forse non mi è chiaro come funziona l'invio e ricezione di pacchetti, quando avviene, per cosa?

**COMPOSIZIONE INDIRIZZO IP**

il formato attuale è l'IPv4 e comprende 32 bit, divisi in due parti:
- **net id**: identifica la rete (a cui l'host è connesso?)
- **host-id** identifica l'host all'interno della rete (non lo fa già il MAC?)
non capisco come funziona questa netmask e come sia rappresentata nel concreto. fammi un esempio con del codice vero uscito da un terminale. stessa cosa per il CIDR che è collegato e i due indirizzi speciali di ogni subnet. cos'è una subnet? una rete gestita da un router? e sti indirizzi cosa sono?

cosa significa che un indirizzo è riservato alle reti interne e non instradato su internet? poi visto che parli di di indirizzi ip immagino sia una cosa che vale a livello internet, quindi mondiale e che questi indirizzi siano riservati per qualche motivo

**PORTE E SERVIZI - Gestione delle applicazioni da parte dell'host**
l'host è identificato globalmente dal suo indirizzo ip. ma su un host girano molteplici applicazioni contemporaneamente che hanno bisogno di mandare e inviare pacchetti in rete.

l'host connette le applicazioni alla rete tramite le **porte**

ogni connessione tramite porta è identificato da questa **quintupla**

- protocollo
	- protocollo della rete, regole, come funziona la comunicazione
- IP_sorgente
	- da quale IP appartiene la porta da cui parte la comunicazione
- porta_sorgente
	- da quale porta di quell'ip parte
- IP_destinazione
	- a quale IP appartiene la porta a cui arriva la comunicazione
- porta_destinazione
	- a quale porta di quell'ip arriva

ma nel pratico cosa viene comunicato? solo pacchetti? dati diversi che si mettono sempre in questi pacchetti? altre cose al posto dei pacchetti? il termine pacchetti mi confonde.

**TCP - come si apre una connessione?**

il TCP è un **protocollo** orientato alla connessione (cioè?)

Viene usato per sincronizzare due host e successivamente fargli scambiare dati

riporta il disegno fatto per spiegarlo, ma identifica meglio chi sta parlando in ogni momento oltre a cosa dicono

**three-way perchè?**
prima i due host si sincronizzano (**SYN**) quando il pacchetto inizia la connessione, poi dall'altro lato si conferma l'arrivo del pacchetto (**ACK**) e infine si stabilisce la connessione **ESTABLISHMENT**

non capiso quando effettivamente si invia il pacchetto, io direi alla fine quando la connessione viene stabilita, ma dici che in fase **ACK** si conferma già l'arrivo del pacchetto. inoltre dalle tue parole sembra che sia il pacchetto a svolgere questo lavoro, è così?

**NAT - Network Address Translation**

non ho capito il problema che poni. perchè gli ip pubblici sono scarsi? in che senso? 

capisco che gli host in una sottorete abbiano e comunichino con un indirizzo locale, ma mi sembrava di aver capito che questo era il ruolo dell'indizzo MAC

qual'è il ruolo dell'indirizzo NAT? come si relaziona agli altri tipi di indirizzo che abbiamo visto?

**VBox - tipi di interfaccia di rete**

carina e utile la tabella, ma troppo scarna, come funzionano nel pratico le varie interfacce di rete, che pro e contro hanno?

usi termini che non sono scontati come SNAT, port forwarding, LAN, internal network, gruppi, che non capisco cosa intendono.

**Configurazione di rete su Linux**

ip a - vedo le varie interfacce di rete e i loro indirizzi, quindi come si connette la VM a internet e con quale nome? che tipo di indirizzo mostra?

`vagrant@bookworm:~$ ip a`
`1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN group default qlen 1000`
    `link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00`
    `inet 127.0.0.1/8 scope host lo`
       `valid_lft forever preferred_lft forever`
    `inet6 ::1/128 scope host noprefixroute` 
       `valid_lft forever preferred_lft forever`
`2: eth0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc fq_codel state UP group default qlen 1000`
    `link/ether 08:00:27:8d:c0:4d brd ff:ff:ff:ff:ff:ff`
    `altname enp0s3`
    `inet 10.0.2.15/24 brd 10.0.2.255 scope global dynamic eth0`
       `valid_lft 86313sec preferred_lft 86313sec`
    `inet6 fd17:625c:f037:2:a00:27ff:fe8d:c04d/64 scope global dynamic mngtmpaddr` 
       `valid_lft 86313sec preferred_lft 14313sec`
    `inet6 fe80::a00:27ff:fe8d:c04d/64 scope link` 
       `valid_lft forever preferred_lft forever`
`vagrant@bookworm:~$ ip a`
`1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN group default qlen 1000`
    `link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00`
    `inet 127.0.0.1/8 scope host lo`
       `valid_lft forever preferred_lft forever`
    `inet6 ::1/128 scope host noprefixroute` 
       `valid_lft forever preferred_lft forever`
`2: eth0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc fq_codel state UP group default qlen 1000`
    `link/ether 08:00:27:8d:c0:4d brd ff:ff:ff:ff:ff:ff`
    `altname enp0s3`
    `inet 10.0.2.15/24 brd 10.0.2.255 scope global dynamic eth0`
       `valid_lft 83200sec preferred_lft 83200sec`
    `inet6 fd17:625c:f037:2:a00:27ff:fe8d:c04d/64 scope global dynamic mngtmpaddr` 
       `valid_lft 86373sec preferred_lft 14373sec`
    `inet6 fe80::a00:27ff:fe8d:c04d/64 scope link` 
       `valid_lft forever preferred_lft forever`

con `show` posso specificare una sola interfaccia da visualizzare

`vagrant@bookworm:~$ ip a show eth0`
`2: eth0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc fq_codel state UP group default qlen 1000`
    `link/ether 08:00:27:8d:c0:4d brd ff:ff:ff:ff:ff:ff`
    `altname enp0s3`
    `inet 10.0.2.15/24 brd 10.0.2.255 scope global dynamic eth0`
       `valid_lft 83104sec preferred_lft 83104sec`
    `inet6 fd17:625c:f037:2:a00:27ff:fe8d:c04d/64 scope global dynamic mngtmpaddr` 
       `valid_lft 86277sec preferred_lft 14277sec`
    `inet6 fe80::a00:27ff:fe8d:c04d/64 scope link` 
       `valid_lft forever preferred_lft forever`

leggo il nome della interfaccia **eth0**, il suo indirizzo IP fisso (credo) **10.0.2.15**, non capisco come recupero la sua versione IPv6 però. 

con `ip r` posso vedere la tabella di routing

`vagrant@bookworm:~$ ip r`
`default via 10.0.2.2 dev eth0` 
`10.0.2.0/24 dev eth0 proto kernel scope link src 10.0.2.15` 

`default via 10.0.2.2 dev eth0` 
**default gateway**: ogni cosa che non conosco (in che senso?) va qui

non riesco a riconoscere le altre informazioni però

gli esercizi successivi credo richiedano delle chiarificazioni e avere ben chiaro di cosa stiamo parlando prima di affrontarli

---

> **⚠️ NOTA 2026-06-23**: appunti grezzi parziali (teoria + Es.1 ip a/ip r). Es. 2-6 da eseguire. La guida-lab completa Es.1–6 è in `guida_lab_modulo3D_networking_base.md`. Dopo aver eseguito tutti gli esercizi, aggiungere qui gli output e le osservazioni, poi `/appunti 3D`.

## Es. 2–6 (da completare dopo il lab)

<!-- Dopo aver eseguito ping, ss, /etc/hosts, dig, tracepath, tcpdump: aggiungi qui i tuoi output e le domande che emergono -->

<!-- AUTO-LINKS:START -->
## 🔗 Collegati

- [[appunti_modulo3D_networking_base]]
- [[lezione_modulo3D_networking_base]]

**Hub:** [[master_map_studio]] · [[glossario_sysadm]] · [[concept_maps]] · [[troubleshooting_vm]] · [[metodo_studio_esami_pratici]]
<!-- AUTO-LINKS:END -->
