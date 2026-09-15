

Offensive security: simulazione di attacchi reali, con permesso e obbiettivi definiti, penetrando effettivamente o trovando solo le falle nel sistema

VA (Vulnerability Assessment): assessment che mira ad elencare tutte le vulnerabilità note del sistema

PT (Penetration Testing): assessment autorizzato che sfrutta, verificando le catene di attacco, le falle ritrovate dal VA, e produce un report che ne dimostra l'impatto reale 

Kill Chain: la catena di attacco seguita nel penetration testing; (inserisci la struttura)

RedTeam: pratica di simulazione consistente in un operazione prolungata di settimane o mesi, dove si simula a tutti gli effetti un atto ostile sofisticato, includendo tecniche di social engineering etc etc

Rischio: tutto il concetto della cibersecurity si basa sul concetto di rischio come prodotto tra probabilità e impatto dell'avvenimento. attraverso questo si organizza la dimensione dello sforzo volto a risolvere una falla che introduce quel preciso coefficente di rischio.

Window of Exposure: tempo che passa tra la scoperta della falla e la patch che la risolve, si mira a farla corta

NIST Cybersecuirty framework: ciclo di operazioni che compie la difera per difendersi (argomenta e insersci il processo)

Politiche & Meccanismi: Regole e Regolatori 

Forme di attacco: un attacco può avvenire attraverso diverse superfici. c'è il livello fisico (si accede fisicamente alla macchina), quello cyber (vi si accede via rete, applicazioni, sistemi) oppure umano (phishing, social engineering). 


FASI DELL'ATTACCO

Reconnaissance: l'attaccante impara a conoscere l'obbettivo senza interagire direttamente coi sui sistemi, ha una parte passiva (senza prove) e attiva (con prove)
Il Penetration Test inizia sempre passivamente.

Google Dorking: Google diventa il nostro primo alleato, e attraverso query costruite con operatori avanzati riusciamo a trovare tutto quello che google indicizza attraverso un crawler
(inserisci tabella operatori utili ed esempi)

robots.txt: convenzione tra web developer e creatore di crawler legittimi che viene usato per descrivere quali file escludere dalla indicizzazione. un hacker se ne sbatte

OSINT su IP e domini (per cosa sa OSINT? avrei detto retro engineering): andando a ritroso su da chi e a chi viene assegnato il proprio indirizzo IP si può andare a cercare gli ip e quindi le reti di tutti i blocchi allocati a quell'ambito, organizzazione, tipologia

DNS (spiega cos'è un record dns, a che serve, perche esiste e dove esiste): attraverso l'analisi dei report DNS si rivela molto di più dei semplici IP. (mostra conseguenze, cosa si puo trovare etc)

Subdomain enumeration e CT abuse: (banale, rispiegalo semplicemtne e aggiungi qualche semplificazione riguardo al CT e al come trovare i subdomain)

NMAP (Spiega il comando in forma classica base, con aggiunta di sudo, con aggiunta di -sn, a cosa serve -p- e come interagisce aggiungendo -sV e -sT. assicurati di inserire un esempio di linea di codice intera per ogni esempio che spieghi con annessa risposta di sistema)

Domande di autoverifica: 1:C 2:B 3:B(?) 4:Falso 5:B 6:Fc




