# Compiti — Amministrazione di Sistemi T

> Testi degli esercizi assegnati, estratti da Virtuale il 2026-06-18.

## pipeline di filtri

Contare quanti file esistono con una certa estensione, definita come la stringa posta dopo l'ultimo carattere "punto" presente nel nome del file, per tutte le estensioni trovate nei file presenti nel direttorio corrente e nei sottodirettori. Limitare l'output alle sole 5 estensioni più numerose.
Esempio: 
esistono i file 
./data.txt
./my.example.c./src/hw.c./src/hw.h
la pipeline restituisce
2 c1 h1 txt
Comandi da utilizzare:


ls -R
rev
cut
grep
sort
uniq
head

Check: lanciato nella directory "/" della VM vagrant, deve restituire
    275 mod     89 0     86 pem     62 gz     62 d

---

## Conta Occorrenze

Scrivere uno script bash che dato il file allegato conti le occorrenze:


della lettera 'a'
della parola 'sherlock' case insensitive
per ogni parola distinta conti le sue occorrenze e mostri a terminale le cinque parole con frequenza maggioreIl testo è stato tratto dal sito del prof. Peter Norvig e rilasciato con licenza open

 The_Adventures_Of_Sherlock_Holmes.txt   18 gennaio 2026, 16:00

---

## Estensione degli esercizi risolti

Estendere gli script illustrati di conversione e manipolazione del tempo per gestire, in tutte le versioni proposte, la rimozione delle notifiche relative a eventi che vengono rimossi dal calendario.

---

## "Estensioni" parametrico

Modificare l'esercizio delle estensioni realizzando uno script estparam.sh che accetti sulla riga di comando


un nome di directory da esplorare
un elenco di lunghezza arbitraria di stringhe

Lo script deve contare quanti file esistono nel sottoalbero definito dalla directory passata come primo parametro, che abbiano estensione uguale a una delle stringhe specificate coi parametri successivi. La soluzione deve essere efficiente, non deve invocare comandi pesanti sul filesystem in modo ridondante.

Esempio: 
./estparam /etc conf inc56 conf28 inc

---

## Funzioni, case, test

Realizzare una funzione waitfile che accetti


un primo parametro obbligatorio = nome di comando
un secondo parametro obbligatorio = nome di file
un terzo parametro facoltativo 

La funzione deve 


controllare che il valore di $1 sia uno di ls, rm, touch
eseguire il comando $1 con parametro $2 (basta lanciare $1 $2) in modi diversi a seconda di $3 come spiegato di seguito


Usando case, discriminare tre possibilità:


$3 è "force" --> esecuzione immediata
$3 è un numero "N" di una cifra decimale --> se $2 non esiste, aspetta che eventualmente compaia, riprovando al massimo N volte con un'attesa di 1 secondo tra un tentativo e il successivo (usare sleep 1)
$3 è assente o altro valore --> come caso precedente, considerando un valore di default N=10

La funzione deve ritornare exit code significativi e messaggi d'errore dove opportuno.

---

## Esecuzione parallela generalizzata

Estendere l'esempio dell'esecuzione di due job in parallelo.Realizzare uno script parallenne.sh che lanci in parallelo tutti i comandi forniti come parametricontrolli ogni 5 secondi quali sono ancora in esecuzione, verificando che il PID corrisponda al nome del comandoscriva a ogni controllo sul file "log" lo stato dei processi termini quando tutti i processi in background sono terminatigarantisca la terminazione di tutti i processi in background se viene terminato dall'esterno il processo parallenne

---

## Segnali girati

Cosa dovrebbe fare secondo voi questo script?Perchè non funziona, e come va corretto?#!/bin/bashreport () {	echo $(date) osservate $TOT nuove righe	TOT=0}echo $BASHPID > /tmp/logwatch.pidTOT=0trap report USR1tail -n +0 -f "$1" | while read R ; do	TOT=$(( $TOT + 1 ))done

---

## Conta occorrenze avanzato

Scrivere uno script bash che dato il file allegato all'esercizio Conta occorrenze (The_Adventures_Of_Sherlock_Holmes.txt):Lanciare due processi in parallelo che contino le occorrenze della parola 'sherlock' case insensitive, il primo processo deve leggere la prima metà del file il secondo processo la seconda metà, alla fine restituisca il risultato totale sul terminale. Per definire metà del file si contino le righe totali e si arrotondi per difetto la prima metà in caso le righe siano dispariEseguire lo stesso esercizio proposto sopra ma quando uno dei due processi termina prima dell'altro questo deve segnalare prontamente la cosa al processo che stà ancora lavorando il quale deve gestire l'interruzione interrompendo il conteggio e restituendo il risultato parziale in un file temporaneo scelto in precedenza; dopo di che deve proseguire il conteggio; lo script deve restituire la somma dei due risultati parziali stampata a terminale

---

## niceexec esteso

Partendo dallo script che esegue un comando solo se il carico è inferiore a una soglia, e in caso contrario si ri-schedula con at, realizzarne una versione che accetta un ulteriore parametro numerico che rappresenta il numero massimo di tentativi da provare.OPZIONALE - Usare getopt (non visto a lezione ma documentato sulle slide) per far sì che il comando abbia la sintassi:niceexec.sh -n MAX_TENTATIVI -s SOGLIA_CARICO  COMANDO_DA_ESEGUIRE  PARAMETRI

---

## logrotate

Realizzare uno script dal comportamento dipendente dal contesto di invocazione.Se logrotate.sh  si rileva lanciato da terminale (man tty), configura rsyslog per dirigere i messaggi etichettati local1 con priorità non inferiore a warning sul file /var/log/my.logconfigura la cron table di root per esegure se stesso ogni giorno lavorativo alle 23:00In caso contrario, effettua la "rotazione" del file /var/log/my.log rinomina eventuali file /var/log/my.log.N.bz2 in /var/log/my.log.N+1.bz2 (per ogni N esistente)rinomina /var/log/my.log in /var/log/my.log.1 e lo comprime con bzip2ricarica rsyslogd (più in generale il processo che vi sta scrivendo man fuser)

---

## Avvio e monitoraggio automatico

Realizzare due unit per systemdP.S Per fare i test a casa una volta creata la Unit Systemd bisogna effettuare un soft reload caricando dal filesystem le varie Unit e rigenerando l'albero delle dipendenze. `# systemctl daemon-reload `mylog.servicedeve funzionare in modalità oneshotall'avvio lancia uno script che aggiunge a rsyslog il canale  local1.=info  /var/log/sd.logall'arresto lo rimuovemymon.servicedeve funzionare in modalità simple, lancia uno script che senza sosta, ogni 10 secondi, logga un messaggio etichettato local1.info contenente (su di un'unica riga) la quantità di RAM libera e la tripla username/pid/comando del processo che sta consumando più CPUIl servizio mymon esige che sia stato avviato mylog. La terminazione di mylog impone la terminazione di mymon.

---

## Archiviatore

Realizzare uno script che individui nel sottoalbero del filesystem passato come parametro tutti i file che rispettano almeno una di queste caratteristiche (ogni punto elenco rappresenta una caratteristica da verificare integralmente):sono stati modificati o acceduti nell'ultima settimanahanno un qualsiasi bit speciale settato e non sono di proprietà dell'utente rootsono di tipo text (secondo il comando file), di dimensione inferiore a 100k, e contengono la stringa DOCe li archivi in un file di nome backup_DATA,tar.gz(DATA sia una stringa che rappresenta l'istante di creazione nel formato AAAAMMGG_HHMM)

---

## Creare un role Ansible

Creare un role ansible che configuri il proxy relativamente al laboratorio3 per il software apt in modo da poterlo usare nelle macchine virtuali create con Vagrant.Leggere la documentazione riportata anche nel prontuario al fine di ottenere un gerarchia standard di cartella Ansible

---

## Gestire un servizio, anche senza vagrant

Modificare lo script copy.sh visto in laboratorio perché esegua un ciclo senza fine che ogni 4 ore esegue il backup.Realizzare una unit systemd che lo avvi come demone.Studiare la man page di ansible-playbook, e svolgere tutti i passi seguenti realizzando un inventory che permetta di gestire la VM senza passare dal Vagrantfile, ma connettendosi direttamente come utente johndInstallare il nuovo script e la unit attraverso ansible.Cosa succede se il processo viene terminato con kill ?Modificare la unit perché venga riavviato automaticamente, ripetendo il provisioning via ansible (sempre indipendentemente da Vagrant), e testare il risultato.

---

## Creare un Task Ansible per il Router visto in lab

Utilizzando l'esercitazone base vista durante il laboratorio di networking:Creare un task che invece di utilizzare il modulo ansible.posix.sysctl utilizzi il modulo Ansible lineinfile per rimuovere il carattere sharp(#) nella riga corrispondete ed abiliti il forward tramite la macchina router tra client e server senza riavviare la macchina virtuale

---

## DHCP - Router due Client tramite Ansible

Modificare il file /etc/dnsmasq.conf visto in laboratorio sul Router al fine
 di realizzare un DHCP che possa erogare indirizzi IP a due client su
subnet diverse, impostando opportunamente le regole di routing. I due
Client una volta configurati dovranno poter comunicare attraverso il
Router usato come gateway, tale Router dovrà avere quindi due interfacce
 di rete distinte una per la subnet 10.1.1.0/24 e una per la subnet
10.2.2.0/24. Gli indirizzi del Router su entrambe le subnet dovranno
essere definiti in modo statico attraverso la modifica del del file /etc/network/interfaces. Inoltre si dovrà provvedere anche ad impostare i vari hostname rinominadoli Client1 e Client2, consiglio sfruttate Vagrant.N.B Abilitare il forwarding sul router tramite l'apposito modulo ansible.posix.sysctl oppure andando a modificare il file /etc/sysctl.conf come precedentemente visto.

---

## DHCP++

Estendere la configurazione DHCP proposta per il client, analogamente, per configurare il server.Modificare la configurazione per assegnare via DHCP in modo sistematico gli indirizzi 10.1.1.1 e 10.2.2.2 rispettivamente a client e a server, riconoscendo i loro MAC addressStudiando la documentazione fornita, configurare il server DNS di router perché risolva i nomi client, server e router sui rispettivi indirizzi (che indirizzo avrà router? se ne possono indicare due? in tal caso client e server come lo risolvono?)

---

## Logging e analisi

Si parta dalla configurazione "multihop"Si installi sui client e sul server il demone rsyslogLo si configurari affinchèsui client mandi tutti i messaggi etichettati local2.warn al serversul server scriva i messaggi etichettati local2.warn sul file /var/log/local2.log Inoltre, sul server si installi uno script /usr/bin/stats.sh che conti quante righe di log sono state inviate da ogni client e scriva il risultato in append sul file /var/log/local2.statsProgettare lo script e la sua esecuzione in due modi diversi: VARIANTE 1: lo script venga eseguito ogni 5 minuti automaticamente; quando viene avviato, svolge il suo compito e terminaVARIANTE 2: lo script venga avviato automaticamente al boot, non termini mai (in caso di terminazione deve essere riavviato) e scriva le statistiche solo quando riceve il segnale USR1 attraverso il comando systemcl reload stats

---

## Esercizio "pivot" risolto - ma da provare prima a fare autonomamente

Supponiamo di avere un agent con un numero imprecisato di processi sorvegliati da direttive proc1) come mi procuro via SNMP il numero di istanze di un processo di cui conosco il nome?2) come verifico rapidamente, ai fini di un test in uno script (es. if o while) se il numero di istanze attive è entro i limiti prestabiliti? pivot.sh   18 gennaio 2026, 16:00

---

## SNMP in ambiente multi-machine

Utilizzare Ansible per creare a configurare un ambiente multi-machine con Vagrant. La topologia della rete prevede l'utilizzo di due macchine virtuali usate come Agent SNMP ed una macchina da dove poter controllare i due nodi (denominata da adesso in poi Controller), quindi in tutto è necessario creare nel Vagrantfile 3 macchine virtuali. Impostare correttamente gli hostname delle machine virtuali tramite o Vagrantfile oppure tramite DNSMASQ, rispettivamente agent1, agent2 e controller.La configurazione di rete deve avvenire tramite DHCP erogato da DNSMASQ sul nodo da cui è possibile interrogare i due Agent SNMP, ovvero il Controller.Dopo aver installato tutti i pacchetti del caso e configurato i due demoni SNMPD tutto tramite Ansible, è necessario aggiungere ad entrambi i demoni, nel giusto file di configurazione, la possibilità di lanciare due comandi custom quando viene richiesto il corrispondente OID, impostando correttamente i permessi e i meccanismi con cui effettuare l'inalzamento dei privilegi. Il primo comando in questione (script createdump.sh) deve poter generare un PCAP, utilizzando TCPDUMP, che termini automaticamente dopo aver catturato 10.000 pacchetti, sull'interfaccia di rete interna tra la macchina virtuale con l'Agent e il Controller. Utilizzando Rsyslog (configurato tramite Ansible) gli agent segnalano al Controller la disponibilità del PCAP e quindi la possibilità di poterlo recuperare da remoto. Il secondo comando custom (script deletedump.sh) invece deve poter cancellare i file PCAP che il Controller ha già recuperato, i cui nomi vengono inviati via syslog dal Controller agli Agent. Periodicamente, ogni 3 minuti alternativamente su un agent e sull'altro (es: minuto 3 agent1, minuto 6 agent2, minuto 9 agent1, ...), il Controller invocherà uno script (managedump.sh) per eseguire il protocollo di generazione, recupero e cancellazione dei PCAP. Lo script deve immediatamente uscire senza fare nulla se ce n'è già un'istanza lanciata in precedenza e non ancora terminata, mentre in caso contrario deve avviare la generazione del PCAP usando la richieste del corrispondente oggetto SNMPmettersi in attesa che sul log compaia la conferma di generazione avvenuta, che include il nome del file da scaricarescaricare col metodo più sicuro che conoscete il file dall'agent in una directory localeinviare conferma all'agent loggando il nome del file scaricatoinvocare via SNMP lo script di cancellazione del PCAPConsegnare il Vagrantfile, i playbook necessari chiamandoli playbook_controller.yml, playbook_agent1.yml, playbook_agent2.ymlgli script bashi file di configurazione dei servizi di sistema

---

## log di sistema, SNMP e scripting

Configurare l'agent di Server per poter monitorare il numero di righe nel file /var/log/auth.log che contengono la stringa FAILED--> consegnare il file snmpd.confRealizzare su Client uno script che recuperi via SNMP questa informazione da un host il cui indirizzo viene passato come parametro.--> consegnarlo come file failcount.shRealizzare su Client uno script che deve essere invocato con la sintassifailkill.sh -f FILE -s SOGLIAlo script interroga usando failcount.sh tutti gli host elencati in FILE. Per ogni host che riporta un valore superiore a SOGLIA, lo script si collega via ssh  all'host e lo spegne.

---

## Search and replace

Realizzare uno script con questo comportamento:

Individua tutti gli utenti presenti nella directory.
Per ognuno, modifica l'attributo gecos in modo che contenga la
concatenazione dei valori degli attributi cn, sn, mail.

Se per un utente uno o più dei suddetti attributi fosse privo di valore,
lo script dovrà notificarlo a terminale e acquisirne interattivamente il
valore da tastiera.

---

## netmon

0) avviare un sistema con 2 Client sulla subnet 172.20.20.0/24 e 2 server sulla subnet 172.30.30.0/24; gli indirizzi sono erogati via DHCP dal Router che le interconnette, e che ha indirizzi con byte finale 254 su ognuna, nel range di byte finale 100-200Nel seguito, predisporre via ansible l'installazione di ogni programma nei rispettivi hostl'installazione, configurazione e attivazione dei servizi ausiliari menzionati nei programmi e necessari per ottenere il comportamento desiderato (job cron e at, systemd units, rsyslog, ecc.)in particolaresi creino predisponendo l'opportuno LDIF e gli opportuni comandi, da eseguire al provisioning, tre utenti kirk, id=10001, password=instinctspock, id=10002, password=logicmccoy, id=10003, password=empathycreando anche gruppi omonimi con gli stessi idsi generi manualmente sul controller una coppia di chiavi ed25519si creino le directory necessarie per gli utenti su C* e S* e si installino le chiavi (usando la stessa chiave per tutti gli utenti) in modo opportuno per consentire l'accesso ssh senza password da client a serverNOTA: tutti i programmi sono da installare in /usr/local/bin1) file netmon.sh Monitorare con tcpdump il traffico ssh tra la VM Client e la VM Server, sulla VM Router, loggando attraverso syslog attraverso la facility local1.notice sul file /var/log/newconn l'inizio e la fine di ogni  connessione diretta da Client a Server2) file connection-monitor.shal verificarsi di questi eventi, avviare/fermare il monitoraggio con traffic-monitor.sh della specifica connessione per poter poi controllare il relativo trafficoNOTA: Curare tramite signal handling la pulizia automatica di processi  in caso di terminazione volontaria o involontaria del procedimento di monitoraggio3) file traffic-monitor.shdurante la "vita" di ogni connessione, tracciata con una specifica istanza di tcpdump, al superamento di una certa soglia espressa in numero di pacchetti per minuto, usare log-user.sh per individuare l'utente responsabile loggare lo username nel file /var/log/excess; attraverso la facility local2.noticeincrementare un contatore nell'attributo description dell'utente ESTENSIONI: inviare i messaggi di superamento di soglia anche al syslog del client che sta generando il traffico eccessivose una connessione non genera traffico per oltre 5 minuti, loggare il messaggio _IDLE_<user>_ e settare description a idle4) file log-user.sh Si connette via SNMP alla sorgente del traffico eccessivo  ed individua l'utente responsabile (indicare in snmpd.conf come sono configurati gli agent per consentire tale controllo)ESTENSIONI:*) individuare variabili e funzioni che vengono utilizzate da diversi script e collocarle in un file di risorse condivise da installare ovunque con nome /etc/netmon.rc5) file notify.sh collocato sui ClientViene lanciato automaticamente dalla configurazione di syslog in modo da ricevere su standard input i messaggi etichettati local2.notice; per ognuno, individua i terminali aperti dall'utente menzionato, e vi scrive il messaggio "ATTENZIONE TRAFFICO ECCESSIVO"6) file reaper.sh collocato sui ServerViene lanciato automaticamente ogni 5 minuti nei periodi fuori dall'orario lavorativo (inteso come 8:00-19:00 da lunedì a venerdì); per ogni utente diverso da root che ha in esecuzione un processo sshd, verifica se l'attributo description vale idle, e in tal caso termina tutti i processi sshd dell'utente

---

