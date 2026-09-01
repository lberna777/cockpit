# Appunti — Modulo S5: Firewall — Teoria + Configurazione del Packet Filter Linux
**Corso**: Lab Sicurezza Informatica T
**Lezione di riferimento**: `lezione_moduloS5_firewall_iptables.md`
**Stato**: lezione letta e appunti consolidati — **lab su VM non ancora eseguito** (nessun esercizio pratico riportato nei grezzi)

---

## Il concetto di firewall

Il firewall è un'architettura, non un comando singolo: il punto di passaggio obbligato tra un "dentro" e un "fuori", con una politica di **default deny** — passa solo ciò che è esplicitamente autorizzato.

> **Domanda**: spiega il termine "topologia di rete".
> **Risposta**: è semplicemente *come sono collegati fisicamente/logicamente i dispositivi di una rete tra loro* — chi parla con chi, attraverso quali cavi/segmenti/router. Il motivo per cui conta per il firewall: una regola scritta bene su un firewall non serve a nulla se la **topologia** lascia un'altra strada per raggiungere la rete interna senza passare da lì (un modem dimenticato, una VPN non filtrata, un dispositivo con doppia interfaccia di rete che fa da ponte). Per questo l'efficacia del firewall dipende da *dove* è collocato nella rete, non solo da *cosa* gli scrivi dentro — è il motivo per cui esistono le topologie viste più sotto (screened subnet, DMZ): non bastano le regole, serve che la topologia costringa fisicamente il traffico a passare dal punto controllato.

### Precisazione: cos'è un packet filter rispetto al firewall

> I tuoi appunti dicono: *"un package filter (che immagino sia una proprietà filtro del firewall)..."*
> **Correzione**: il Packet Filter (PF) non è una "proprietà" del firewall — è **uno dei tre tipi fondamentali** in cui un firewall può essere implementato, alla pari di **Application-Level Gateway (ALG)** e **Circuit-Level Gateway (CLG)** (li vedi meglio più sotto, sezione Topologie). Il PF è il tipo più semplice: esamina solo gli header dei pacchetti (indirizzi, porte, flag) — è quello che poi configuri concretamente con `iptables`/`nft` in questo modulo. "Firewall" è il concetto architetturale generale; "packet filter" è una delle possibili implementazioni concrete di quel concetto.

## POV attaccante / POV difensore

Un packet filter "puro" ha limiti strutturali sfruttabili: non vede dentro il payload (non distingue una richiesta HTTP legittima da una con SQL injection nel parametro), è cieco a protocolli che negoziano dinamicamente le connessioni (es. FTP, dove il comando che apre il canale dati viaggia nel payload, non nell'header), ed è vulnerabile a manipolazioni di basso livello come la frammentazione (i frammenti dopo il primo non contengono l'header di trasporto, quindi non attivano le regole che lo controllano — evasione classica) o lo spoofing dell'indirizzo sorgente.

La contromisura è o un componente più intelligente (un ALG che capisce il protocollo) o un irrigidimento della policy (scartare i pacchetti frammentati, verificare la coerenza tra subnet e interfaccia). Per l'esame pratico: il primo passo davanti a un esercizio iptables/nftables non è "che regola scrivo" ma "che tipo di traffico devo lasciare passare, e quale strumento (PF, stateful, ALG) serve per farlo con precisione".

## `iptables` — sintassi e modello concettuale

Forma fissa del comando:

```
iptables [-t <tabella>] -CMD [catena] [match] [-j <target>]
```

Se ometti `-t` si assume `filter`. I comandi (`-L`, `-A`, `-I [n]`, `-D [n]`, `-R n`, `-F`, `-P`) sono verbi sulla catena nel suo complesso.

> **Domanda**: questi comandi (`-L`, `-A`, ecc.) vanno al posto di `-CMD` nel comando, oppure dopo `-CMD` in `[catena]`?
> **Risposta**: vanno esattamente al posto di `-CMD` — sono il comando stesso, non un argomento che lo segue. Lo schema `[-t <tabella>] -CMD [catena] [match] [-j <target>]` si legge da sinistra a destra come slot successivi da riempire: primo slot (opzionale) la tabella, secondo slot il comando/verbo, terzo slot (dove richiesto) la catena su cui quel comando opera, poi i match, infine il target. Esempi concreti per chiarire la posizione di ciascuno:
> ```bash
> iptables -L INPUT              # -CMD=-L, [catena]=INPUT — elenca le regole della catena INPUT
> iptables -A FORWARD -p tcp --dport 80 -j ACCEPT   # -CMD=-A, [catena]=FORWARD, poi i match (-p, --dport), poi -j ACCEPT
> iptables -P INPUT DROP         # -CMD=-P, [catena]=INPUT, poi l'argomento della policy (DROP) — qui non c'è [match]/[-j], perché -P non filtra pacchetti: imposta solo il comportamento di default
> iptables -F                    # -CMD=-F, nessuna catena = svuota TUTTE le catene della tabella
> ```
> Quindi la regola pratica: `[catena]` è sempre il primo argomento *dopo* il verbo (quando il verbo la richiede), mai qualcosa che "segue" il verbo in un secondo comando separato — è tutta una singola invocazione di `iptables`.

I match sono i criteri "se": `-s`/`-d`, `-p`, `--sport`/`--dport`, `--tcp-flags mask comp`. Alcuni match richiedono un'estensione esplicita (`-m mac --mac-source`, `-m iprange --src-range`).

## `nft`/nftables — lo stesso modello, sintassi diversa, zero default

`nftables` ha rimpiazzato `iptables` (e `arptables`, `ip6tables`, `ebtables`) come sistema di default nel kernel Linux dal 2014; `iptables` resta rilevante per sistemi legacy o perché altri strumenti lo invocano indirettamente.

**`nft` non ha nulla di predefinito**: dove `iptables` ti dà già tabelle e le cinque catene builtin pronte, in `nft` crei esplicitamente tabella, poi catena specificando tipo, hook e priority.

> **Domanda**: puoi chiarire ed esemplificare meglio la struttura del comando `nft`? La trovo confusa scritta solo in prosa.
> **Risposta**: scomponiamola in tre comandi separati, uno per livello, sullo stesso esempio concreto (un firewall che accetta SSH e il traffico di ritorno, droppa il resto in ingresso):
> ```bash
> # 1. crea la tabella (contenitore di primo livello, per una "famiglia" di protocollo — qui ip = IPv4)
> nft add table ip firewall
>
> # 2. crea la catena DENTRO quella tabella, dichiarando dove/quando/con che default agisce
> nft add chain ip firewall input { type filter hook input priority 0 \; policy drop \; }
> #                     ^tabella  ^nome catena  ^tipo   ^hook a cui si aggancia  ^ordine tra catene sullo stesso hook  ^comportamento se nessuna regola fa match
>
> # 3. aggiungi le regole DENTRO quella catena
> nft add rule ip firewall input tcp dport 22 accept
> nft add rule ip firewall input ct state established,related accept
> ```
> Il punto concettuale: `table` è solo un contenitore (non fa nulla da sola); `chain` è dove dici *quando* intervenire (hook) e *cosa fare se nessuna regola scatta* (policy); `rule` è dove metti la logica vera e propria "se match allora azione". In `iptables` questi tre livelli esistono lo stesso, ma li dai per scontati (la tabella `filter` e le catene `INPUT`/`FORWARD`/ecc. esistono già) — in `nft` li devi dichiarare tutti e tre esplicitamente, uno dentro l'altro, prima di poter scrivere la prima regola.

## NAT — DNAT, SNAT, MASQUERADE, REDIRECT

- `DNAT --to-destination` (in `PREROUTING`/`OUTPUT`): cambia la destinazione — port forwarding verso un server interno.
- `SNAT --to-source` (in `POSTROUTING`/`INPUT`): cambia la sorgente — una rete privata che esce con un solo IP pubblico.
- `REDIRECT`: caso particolare di DNAT, dirotta alla macchina locale (proxy trasparente).
- `MASQUERADE`: caso particolare di SNAT, solo in `POSTROUTING`, assegna automaticamente l'indirizzo dell'interfaccia di uscita — comodo quando quell'indirizzo può cambiare (es. IP dinamico).

Esempio: `iptables -t nat -A PREROUTING -i ppp0 -d <ip_pubblico> -p tcp --dport 2222 -j DNAT --to-destination 192.168.0.1:22`.

## conntrack e stateful filtering

Un PF puro è **stateless**. `conntrack` riconosce che una sequenza di pacchetti appartiene alla stessa connessione (tupla protocollo/IP sorgente/IP destinazione/porte), indipendentemente dal fatto che il protocollo sia connection-oriented o meno. Stati: `NEW`, `ESTABLISHED`, `RELATED`, `INVALID`.

## I cinque hook di netfilter

> **Domanda**: cos'è un hook di netfilter?
> **Risposta**: è un **punto di aggancio nello stack di rete del kernel** — un posto preciso nel codice che gestisce i pacchetti dove il kernel si ferma un istante e chiede "qualcuno ha registrato una funzione da eseguire qui?" prima di proseguire. Netfilter definisce cinque di questi punti nel percorso che un pacchetto IP attraversa; iptables/nft non fanno altro che registrare le tue regole *a uno di questi punti specifici*. È per questo che la catena in cui scrivi una regola non è un dettaglio organizzativo ma decide *quando esattamente* nel ciclo di vita del pacchetto la regola viene valutata.

`PREROUTING` scatta appena il pacchetto entra, prima di ogni decisione di instradamento. Poi si biforca: `INPUT` se il pacchetto è per il sistema locale, `FORWARD` se va inoltrato altrove. Il traffico generato localmente entra da `OUTPUT`. Tutto ciò che sta per lasciare il sistema converge su `POSTROUTING`.

## Topologie e collocazioni — perché non basta un firewall solo

> **Domanda**: questa sezione era di difficile comprensione — troppe sigle (BH, PF, DMZ, ALG, CLG, "screened subnet/single-homed") introdotte senza spiegarle prima.
> **Risposta**: hai ragione, riprendiamola con un piccolo glossario prima, poi lo schema di ogni topologia.
>
> **Glossario**:
> - **PF** = Packet Filter (visto sopra: filtra solo header, tipicamente integrato nei router)
> - **ALG** (Application-Level Gateway) = un proxy che capisce il protocollo applicativo (HTTP, FTP...) e può quindi permettere/negare comandi specifici, non solo header
> - **CLG** (Circuit-Level Gateway) = un intermediario che spezza la connessione a livello di trasporto (diventa lui stesso l'endpoint del traffico) ma inoltra i payload senza esaminarli — meno intelligente di un ALG, ma anche più leggero
> - **BH** (Bastion Host) = un sistema **dedicato** a far girare il software firewall — tipicamente implementa un ALG o un CLG (un PF di solito sta già integrato nel router, non ha bisogno di un host dedicato)
> - **DMZ** (Demilitarized Zone, zona demilitarizzata) = una sottorete "cuscinetto" tra Internet e la rete privata, dove si mettono i server che devono essere raggiungibili dall'esterno, isolati dal resto della rete interna
>
> **Le topologie, in ordine di complessità crescente**:
> 1. **Screened single-homed BH**: un solo PF (tipicamente sul router) lascia passare traffico solo verso il BH; il BH implementa l'ALG/CLG. Il BH però condivide fisicamente la stessa rete degli host interni: se comprometti *sia* il PF *sia* il BH, sei dentro alla rete interna — due sistemi da compromettere, ma non fisicamente separati.
> 2. **Screened dual-homed BH**: uguale, ma il BH ha **due schede di rete** e separa *fisicamente* due segmenti — nasce la DMZ, dove vivono i server pubblici. Compromettere il solo PF esterno non basta più per arrivare alla rete interna, perché il BH è l'unico ponte fisico tra i due segmenti.
> 3. **Screened subnet**: due PF router (uno "outside" verso Internet, uno "inside" verso la rete privata), con la DMZ in mezzo. Nasconde del tutto l'esistenza della subnet privata da chi sta fuori (ostacola l'enumerazione), e lascia che il traffico "banale" tra Internet e DMZ non debba necessariamente passare dal BH.
>
> Il compromesso di fondo: più layer di separazione aggiungi (dalla 1 alla 3), più sistemi in sequenza un attaccante deve compromettere per arrivare alla rete privata, ma più cresce la complessità di gestione. All'estremo opposto ci sono i **Personal Firewall**, installati sulla singola macchina invece che al perimetro: massima precisione (sanno *quale processo* genera un pacchetto, cosa impossibile a un PF di rete puro), ma persa la centralizzazione — spesso configurati "learning by doing", con un volume di alert che finisce ignorato.

---

## Connessioni

> ⚠️ Questa sezione non era presente negli appunti grezzi.

- **Con S1 (Enumerazione)**: le regole firewall scritte qui sono esattamente ciò che un `nmap` esterno vede come porte "filtered" invece di "closed"/"open".
- **Con S4 (Binary exploits)**: `secret_function_remote` (es2b) esponeva un servizio in rete senza controllo di provenienza — è il tipo di superficie che una regola d'ingresso ristretta per sorgente avrebbe limitato.
- **Con S10 (Network Intrusion Detection, non ancora fatto)**: il firewall è prevenzione (blocca/lascia passare secondo policy); un NIDS come Suricata è rilevazione per ciò che il firewall lascia passare perché conforme alla policy ma comunque anomalo.

## Domande di autoverifica — Risposte

> ⚠️ Questa sezione non era presente negli appunti grezzi — Lorenzo non ha ancora risposto alle domande della lezione. Da fare prima di considerare il modulo solido, in aggiunta (non sostituzione) dell'esecuzione del lab su VM.

1. **Falso** — un PF stateless non vede il payload, quindi non può leggere il comando che nel Control Channel FTP annuncia la porta del Data Channel: serve un ALG o un meccanismo di tracking dedicato al protocollo.
2. **Vero** — `nft` non ha nulla di predefinito, va creato tutto esplicitamente (visto sopra).
3. **Risposta corretta: (a)** `ct state established,related accept`.
4. **Falso** — è buona pratica riservare `DROP`/`ACCEPT` alla tabella `filter`; `nat`/`mangle` servono a modificare, non a giudicare il destino finale.
5. **Falso** — `RETURN` in una catena custom torna alla catena chiamante (riprende dalla regola successiva al salto); `RETURN` in una catena builtin equivale invece alla default policy di quella catena. Sono due effetti diversi con lo stesso comando, a seconda del tipo di catena in cui gira.

## Riepilogo

> ⚠️ Questa sezione non era presente negli appunti grezzi.

- Un firewall è un'architettura con una policy (default deny) e una topologia (DMZ, segmentazione) — le regole più corrette non salvano una topologia che lascia altre strade aperte.
- `iptables` e `nft` condividono lo stesso modello concettuale (tabelle per tipo di decisione, catene agganciate agli hook di netfilter, regole in ordine) — `nft` lo rende esplicito dove `iptables` lo dava per scontato.
- conntrack rende il filtraggio stateful: una regola sola per NEW/ESTABLISHED invece di una coppia simmetrica per ogni servizio.

<!-- AUTO-LINKS:START -->
## 🔗 Collegati

- [[guida_lab_moduloS5_firewall_iptables]]
- [[lezione_moduloS5_firewall_iptables]]

**Hub:** [[master_map_studio]] · [[concept_maps]] · [[metodo_studio_esami_pratici]]
<!-- AUTO-LINKS:END -->
