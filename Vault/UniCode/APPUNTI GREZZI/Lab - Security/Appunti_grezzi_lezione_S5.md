

Il concetto di Firewall: il fireewall è un'architettura, non un comando singolo. si tratta del punto di passaggio tra un "dentro" e un "fuori", con una politica di **default deny**, ovvero passa solamente ciò che è autorizzato.

Per risultare efficace il firewall necessita di una sola condizoopne. ovvero essere l'unica via d'accesso dal "fuori" al "dentro", serve che la **topologia di rete** (spiega questo termine) costringa il traffico a passare di li.

POV ATTACCANTE

Per un attaccante, un package filter (che immagino sia una proprietà filtro del firewall) "puro" (quello che esamina solo header — indirizzi, porte, flag TCP) ha limiti strutturali sfruttabili: non vede dentro il payload, quindi non distingue una richiesta HTTP legittima da una con un'iniezione SQL nel parametro; è cieco a protocolli che negoziano dinamicamente le connessioni

un PF senza logica applicativa è vulnerabile a manipolazioni di basso livello come la frammentazione (i frammenti successivi al primo non contengono l'header di trasporto, quindi non attivano le regole che lo controllano — evasione classica) o lo spoofing dell'indirizzo sorgente.

POV DIFENSORE

A contromisura a ciascuno di questi limiti è o un componente più intelligente (un Application-Level Gateway che capisce il protocollo) o un irrigidimento della policy (scartare tutti i pacchetti frammentati, verificare la coerenza tra subnet e interfaccia per bloccare lo spoofing). Tienilo a mente per l'esame pratico: il primo passo davanti a un esercizio iptables/nftables non è "che regola scrivo" ma "che tipo di traffico devo lasciare passare, e quale strumento (PF, stateful, ALG) serve per farlo con precisione".

## `iptables` — sintassi e modello concettuale

Il comando ha una forma fissa:

	iptables [-t <tabella>] -CMD [catena] [match] [-j <target>]

se ometti `-t` si assume `filter`, la tabella "di default" per chi pensa solo a bloccare/lasciar passare traffico.

I comandi (`-CMD`) sono verbi sulla catena nel suo complesso:

- `-L` elenca
- `-A` aggiunge in fondo
- `-I [n]` inserisce (in testa se ometti `n`)
- `-D [n]` cancella
- `-R n` sostituisce
- `-F` svuota
- `-P` imposta la default policy.

(ma questi vanno al posto di -CMD nel comando? oppure dopo -CMD in [catena])

I match sono i criteri "se". Layer 3-4:

- `-s`/`-d` (indirizzo sorgente/destinazione)
- `-p` (protocollo: tcp/udp/icmp/...)
- `--sport`/`--dport` (porte, solo se il protocollo le supporta)
- `--tcp-flags mask comp` (dove `mask` è l'elenco dei flag "che contano" e `comp` quelli tra questi che devono essere settati — utile per rilevare scan anomali tipo un pacchetto con FIN da solo, senza un SYN precedente).

Alcuni match richiedono di caricare esplicitamente un'estensione (`-m mac --mac-source`, `-m iprange --src-range`) — è lo stesso principio delle `iptables-extensions`, moduli aggiuntivi rispetto al comportamento di base.

## `nft`/nftables — lo stesso modello, sintassi diversa, zero default

`nftables` ha rimpiazzato `iptables` (e con esso `arptables`, `ip6tables`, `ebtables` — un solo strumento per tutti i livelli) come sistema di default nel kernel Linux dal 2014 in poi; `iptables` resta rilevante per sistemi legacy o perché altri strumenti lo invocano indirettamente.

**`nft` non ha nulla di predefinito**. Dove `iptables` ti dà già `filter`/`nat`/`mangle` e le cinque catene builtin pronte all'uso, in `nft` devi creare esplicitamente la tabella (`nft add table ip foo`), poi la catena specificando _tipo_ (`type filter|route|nat`), _hook_ (a quale punto dello stack si aggancia: `prerouting`, `input`, `forward`, `output`, `postrouting`) e _priority_ (per ordinare tra catene agganciate allo stesso hook). Questo obbliga a essere espliciti su qualcosa che in `iptables` è implicito nel nome della catena — è più verboso ma toglie ambiguità.

(puoi chiarificare ed esemplificare meglio la struttura del comando, cosi verbosamente la trovo confusa)

## NAT — DNAT, SNAT, MASQUERADE, REDIRECT

La tabella `nat` ha senso solo in due punti del percorso: in `PREROUTING`/`OUTPUT` puoi cambiare la destinazione (`DNAT --to-destination ipaddr[-ipaddr][:port[-port]]` — "questo pacchetto in realtà va a quest'altro indirizzo/porta", tipico di un port forwarding verso un server interno);

in `POSTROUTING`/`INPUT` puoi cambiare la sorgente (`SNAT --to-source ...`, "questo pacchetto in uscita deve sembrare provenire da questo indirizzo", tipico di una rete privata che esce verso Internet con un solo IP pubblico).

`REDIRECT` è un caso particolare di DNAT che dirotta specificamente alla macchina locale (utile per un proxy trasparente);

`MASQUERADE` è un caso particolare di SNAT, valido solo in `POSTROUTING`, che assegna automaticamente al pacchetto l'indirizzo dell'interfaccia di uscita — comodo quando quell'indirizzo può cambiare

Un esempio da tenere a mente è la coppia SNAT+DNAT per instradare SSH verso una macchina interna su una porta non standard: `iptables -t nat -A PREROUTING -i ppp0 -d <ip_pubblico> -p tcp --dport 2222 -j DNAT --to-destination 192.168.0.1:22` fa arrivare a `192.168.0.1:22` chi si connette a `<ip_pubblico>:2222` da fuori.

## conntrack e stateful filtering — perché lo stato conta

Un packet filter "puro" è **stateless**: valuta ogni pacchetto isolatamente, senza memoria di cosa è successo prima. `conntrack` è il componente di netfilter che rompe questa cecità: riconosce che una sequenza di pacchetti appartiene alla stessa connessione (identificata dalla tupla protocollo/IP sorgente/IP destinazione/porte), a prescindere dal fatto che il protocollo sottostante sia connection-oriented (TCP) o connection-less (UDP, ICMP) — è un'astrazione di netfilter, non del protocollo.

Gli stati che assegna sono:

- `NEW` (primo pacchetto valido di una connessione)
- `ESTABLISHED` (risposta o pacchetto successivo di una connessione riconosciuta)
- `RELATED` (un flusso diverso ma correlato a una connessione già tracciata — es. l'ICMP di errore generato da un timeout su una connessione UDP)
- `INVALID` (non valido come primo pacchetto e non appartenente a nulla di noto).

## I cinque hook di netfilter — dove, non solo cosa

(cos'è un hook di netfilter?)

non sono nomi arbitrari: corrispondono uno a uno ai cinque punti in cui netfilter intercetta un pacchetto nello stack di rete del kernel.

`PREROUTING` scatta appena il pacchetto entra, _prima_ di qualunque decisione di instradamento — non sai ancora se è per te o da inoltrare. Dopo la decisione di routing, il percorso si biforca:

se il pacchetto è per il sistema locale passa da `INPUT`; se va inoltrato altrove passa da `FORWARD`.

Il traffico generato localmente (da un processo di questa macchina) entra nel percorso da `OUTPUT`.

tutto ciò che sta per lasciare il sistema — sia esso inoltrato o generato localmente — converge su `POSTROUTING`, l'ultima tappa prima di essere immesso in rete

## Topologie e collocazioni — perché non basta un firewall solo

questa sezione è iimpossibile da cpaire, perchè come al solito non introduci i concetti prima di spiegarli, cosa sono tutte le sigle che usi? BH PF DMZ bastion host, application level, circuit level gateway TCPIP Screened submet o single homed...)
