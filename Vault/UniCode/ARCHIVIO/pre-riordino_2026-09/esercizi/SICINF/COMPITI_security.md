# Compiti — Lab Sicurezza Informatica T

> Testi degli esercizi assegnati, estratti da Virtuale il 2026-06-18.

## Web pentest Altoro Mutual

Lanciare la web app vulnerabile Altoro Mutual dallo script del pentestlab visto a lezione:
# non dovrebbe servire # git clone https://github.com/eystsen/pentestlab.git# non dovrebbe servire # cd pentestlab./pentestlab.sh start altoro
Puntare il browser a http://altoro
Questa macchina ha tante vulnerabilità. Trovarne ALMENO 3 e riportarle in un unico file report.txt con all'interno i dettagli, includendo.

Descrizione di come e perchè si è arrivati a scoprire la vulnerabilità
Payload utilizzato per sfruttarla
Conseguenze della vulnerabilità, cosa siete riusciti a fare di malevolo?
Quale secondo voi è il bug nel codice.

- Hint.Una sqli è molto semplice da trovare, ci sono poi varie XSS.

---

## Altre esercitazioni facoltative di web security

Come spiegato a lezione lo script pentestlab contiene diverse macchine vulnerabili, alcune molto interessanti come webgoat e juicyshop (ricordate che potete vedere tutte le macchine con ./pentestlab.sh --list, avviare la macchina con ./pentestlab.sh start NOME, e accederla seguendo le istruzioni visualizzate all'avvio).Siete caldamente invitati a provare qualche challenge anche con queste macchine e a riportarle in un file report.txt con dovizia di dettagli. Il corso non ha trattato TUTTI i tipi di vulnerabilità web e tutte le possibili tecniche per cui concentratevi soprattutto sugli argomenti trattati a lezione.

---

## Ulteriori Esercitazioni Web Security

Scaricare l'archivio generic_web.zip
E poi eseguire le seguenti istruzioni per estrarre e utilizzare le immagini docker

Estrarre l'archivio zip, la password dell'archivio è "cyberchallenge2021"
Per importare l'immagine eseguire ( con sudo o in alternativa con shell da root )sudo docker load < nome_immagine.tardove nome_immagine.tar è il file risultato dall'estrazione dello zip, se non è stato cambiato è generic_web.tar
Per eseguire il containersudo docker run -i -t nome_immagine bashdove nome_immagine dovrebbe essere sempre se non è stato cambiato generic_web
A questo punto eseguito l'ultimo comando si dovrebbe essere dentro al container conuna shell di root, per cui è sufficente far partire il web server conservice apache2 starte il db mysql conservice mysql startper aver l'applicativo web funzionante.
A questo punto potete verificare l'ip locale assegnato al container con:ip a
Da browser della VM in modalità NON ATTRAVERSO IL PROXY D'ATENEO  (consigliamo quindi di utilizzareil browser di Burp con il proxy d'ateneo disabilitato ) navigate all'indirizzo ip trovato conhttp://IP_DOCKER e troverete il portale della challenges.

---

## Riscrivere una variabile

Esercizio simile a quello svolto in aula.Il programma vulnerabile è write_varconsegnare un file report.pdf che contenga:Payload e screenshot che dimostra la capacità di sovrascrivere la variabile Payload e screenshot dell'exploit finale lanciatoSpiegazione dettagliata di come si è proceduto ad analizzare ed exploitare la vulnerabilità

---

## Funzione nascosta

Esercizio simile a quello svolto in aula.Il programma vulnerabile è secret_functionconsegnare un file report.pdf che contenga:Payload e screenshot che dimostra la capacità di sovrascrivere l'indirizzo di ritornoPayload e screenshot dell'exploit finale lanciatoSpiegazione dettagliata di come si è proceduto ad analizzare ed exploitare la vulnerabilità

---

## Buffer Overflow con shellcode

Esercizio simile a quello svolto in aula.Il programma vulnerabile è shellcodeEseguire l'esercizio in due modi:usando lo stesso shellcode utilizzato durante l'esercitazione in laboratoriousando lo shellcode fornito quiconsegnare un file report.pdf che contenga:Payload e screenshot che dimostra la capacità di sovrascrivere l'indirizzo di ritornoPayload e screenshot dell'exploit finale lanciatoSpiegazione dettagliata di come si è proceduto ad analizzare ed exploitare la vulnerabilità

---

## [facoltativo] Return to libc

Esercizio simile a quello svolto in aula.Il programma vulnerabile è returnlibconsegnare un file report.pdf che contenga:Payload e screenshot che dimostra la capacità di sovrascrivere l'indirizzo di ritornoPayload e screenshot dell'exploit finale lanciatoSpiegazione dettagliata di come si è proceduto ad analizzare ed exploitare la vulnerabilità

---

## ** LAB ** Pentesting target [6 maggio]

Create una VM in VirtualBox (x86_64) con questo discoSistemate manualmente l'interfaccia 2 in modo che sia sulla rete host-only insieme alla vostra Parrot.La VM ha una varietà di vulnerabilità dei tipi visti a lezione: enumerate, entrate, scalate i privilegi. Ci sono diverse strade per ottenere lo stesso risultato: diventare root. Caricate un report che documenti tutte quelle che riuscite a trovare, descrivendo le modalità di utilizzo, anche includendo screenshot se opportuno.

---

## Estensione esercizi suricata / 1

Lo studente deve costruire ( e validare ) una regola suricata che identifichi il traffico in uscita per il portale netflix.comNota bene:La regola va generata con un certo criterio. Che significa? Significa che una richiesta a netflix.com comporta più richieste a più domini!Analizzare quindi con wireshark, o altro tool tutti domini coinvolti… Ricordate la lezione su Web Sec!Modalità di Consegna:- Consegnare il file netflix.rules con la/le regola/e suricata.- Consegnare uno screenshot che mostra i log di suricata che mostrano l'alert sui diversi domini.

---

## Estensione esercizi suricata / 2

Il file di tipo pcap assegnato è il tracciato di un traffico mqtt tra un subscriber e un publisher sul broker mosquitto.( Per informazioni su mqtt e mosquitto riprendere le slide su TLS)Vostro compito è quello di creare una regola suricata che scateni un alert ogni volta che nel contenuto del pacchetto MQTT ci sia il contenuto “flag”Se predisposta correttamente, nei log di suricata dovreste essere in grado di vedere il contenuto dei pacchettiNel contenuto dei pacchetti è possibile trovare “pezzi” di una flag nel formato SEC{qualcosa}, che potete ricostruire e sottomettere (insieme alla regola!) sul portale virtuale.ATTENZIONE: Per poter vedere il contenuto dei pacchetti nei log di suricata è necessario abilitare la funzionalità “payload-printable”. Cercare nel file di configurazione di suricata la suddetta feature e abilitarla se disabilitata.Modalità di consegna:- Consegnare il file report.txt che contiene:-- La regola usata per identificare il traffico con suricata.-- lo script/comando usato per parsare il log di suricata e ricostruire la flag-- La flag

---

## Privilege escalation alternative

Caricare in un singolo file TXT le soluzioniPredisposizione: utilizzate la VM Kali, ma prima di accenderla scattate uno snapshot, in modo da poterlo ripristinare al termine o in caso qualche modifica la renda inutilizzabile. Fatto questo, avviatela e rendete direttamente accessibile l'account root (diventate root, lanciate passwd)1) Impostare il SUID bit sul comando find e dimostrare come questo possa ora essere usato per una privilege escalation2) impostare il SUID bit sul comando sed e dimostrare come questo possa ora essere usato per una privilege escalation3) Leggere le man page acl (5), setfacl (1), getfacl (1)Portare qualche esempio di come le POSIX ACL possano essere utilizzate per privilege escalation (suggerimento: vagamente simile all'esempio di sudo) e di come individuare sul sistema file su cui siano impostate in modo potenzialmente pericoloso.4) Leggere le man page capabilities (7), setcap (8), getcap (8)Portare qualche esempio di come le capabilities possano essere utilizzate per privilege escalation (suggerimento: simile all'esempio di SUID) e di come individuare sul sistema file su cui siano impostate in modo potenzialmente pericoloso.

---

## DoS

Ci sono varie modalità di Denial of Service. Hping3 offre la possibilità di lanciarne diverse.Provare almeno due tecniche di DoS diverse da quelle fatte a lezione sia su  Alice che su Bob.Consegnare un file report.pdf dove vengono riportati gli screenshot per ogni attacco eseguitoScreenshot dell'attacco lanciato dalla macchina .105Screenshot dei due container Alice e Bob DURANTE l'attacco ( .05, .06 )

---

## DHCP poisoning

Replicare l'attacco DHCP poisoning visto a lezione, semplicemente con un range diverso di ip.Consegnare un file report.pdf dove vengono riportati gli screenshot per ogni attacco eseguitoScreenshot dell'attacco lanciato dalla macchina .105Screenshot dei due container Alice e Bob DURANTE l'attacco ( .05, .06 )Screenshot del tracciato wireshark

---

## Cracking e bruteforcing

Caricare in un singolo file TXT le soluzioni.1) Dati i seguenti account recuperare le rispettive passwordseser1:x:1003:1003:,,,:/home/eser1:/bin/basheser1:$6$ib4iK6iItGvL1NIE$BVsxQzq.mmepXdCTP4zFJlDcDxLaclYLTfgL3aIo8ZogWlM.BNNpmdJfPuWh69d/n2XnPpYAattoC9r2zP7kL/:19052:0:99999:7:::tulipano:x:1005:1005:,,,:/home/tulipano:/bin/bashtulipano:$6$jBOf0K5/ymFabsrr$E66i753AHnc7A8YB1rIJA0nL2Qe12XD/hrqyuYaPgbNO/NYX1JE4s5Y5bmhnrFJyX.S3DG7tQuWicv7pJjUou/:19052:0:99999:7:::tim:x:1002:1002:Sir Tim Berners-Lee,,,,Inventor of the www:/home/tim:/bin/bashtim:$6$4mnKuGkT$.mMjEJNNRu5HKhKz3byLHT8GHHTA6xfsiavBWCB8QL8qyJW2BEICTZ6IzRFhRYUNv9PXc/obOtv475WHe.wPm.:19792:0:99999:7:::Hint: e possibile craccarli attraverso delle wordlist.Per l'utente eser1 è possibile creare una lista "ad-hoc" piccola e in breve tempoPer l'utente tulipano è opportuno scegliere una wordlist esistente accuratamente, il nome utente è un orientamentoSimilmente, per l'utente tim, ma sfruttando cupp e un po' di OSINT2) Dato il seguente hash "85064efb60a9601805dcea56ec5402f7", scoprire:- Algoritmo di hash- Valore originario3) Dato l'archivio zip "es.zip" protetto da password, craccarlo e:- Trovare la password dell'archivio- Accedere ai contenuti dell'archivioHints.- Usare la suite di john completa, post installazione come da slide ( si consigliano almeno 2 GB di RAM alla VM )- Se non si è riusciti a vederlo in aula fare riferimento ai link a fine slide e cercare come craccare uno zip file con john ( hint zip2john )

---

## Password recovery

ERRATA CORRIGE: installare la libreria sudo apt install zlib1g-dev e ricompilare john come illustrato nelle slideL'archivo zip contiene il file secret.txt con dentro la flag dell'esercitazione.ATTENZIONE l'archivio è stato aggiornato il 16 maggioL'archivio è crittato con una password tale da rendere difficile un brute-force dalla vm del lab.È stata generata però a partire dal sito ulisse.unibo.itRestituire password e flag soluzione_crack_password.txt   18 gennaio 2026, 16:01

---

## Hash e GPG

Salvare in un file di nome esgpg.txt l'output del comando uname -a della vm del corsoSalvare in un file di nome esgpg.sha l'hash del file esgpg.txt calcolato con l'algoritmo sha512 (man sha512sum)Cercare sul sito web https://keys.openpgp.org/ la chiave pubblica di Marco Prandini <marco.prandini@unibo.it> e importarla in gpgGenerare una coppia di chiavi RSA con GPG associate al vostro indirizzo @studio.unibo.itCaricare l'identificativo della chiave qui come consegna dell'esercizioCaricare la chiave pubblica sul server https://keys.openpgp.org/Cifrare per i suddetti destinatari il file esgpg.shaFirmarloSpedirlo via mail ai suddetti destinatariL'oggetto della mail deve essere "Esercitazione SEC GPG 2026 " - Mail con oggetti diversi saranno scartate e non prese in considerazione.

---

