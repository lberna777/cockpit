
Cosa succede quando un'applicazione web si fida dell'input che riceve?

Un **Applicazione web** è un sistema che riceve input dall'esterno e li usa per **costruire query, comandi, pagine HTML, chiamate API...**, L'**attaccante** sfrutta il fatto che l'applicazione **non distingua** tra **dato ed istruzione**

La prospettiva del **difensore** è speculare. ogni punto dove l'input esterno influenza un interprete (database, shell, browser...) è una superficie d'attacco possibile e va trattato con **zero fiducia**

La difesa di basa sul principio di **validate input, escape output** - valida quello che entra e codifica tutto quello che esce

**A1 - BROKEN ACCESS CONTROL**

(inserisci una tabella di confronto tra IDOR, File desclosure e LFI/RFI)

da quello che ho capito gli IDOR sono semplici cambi di parti di URL per selezionare un oggeto diverso da quello che si sta visualizzando, bypassando i permessi di lettura e accesso se l'applicazione accetta senza verificare. non ho capito invece perchè il file disclosure sarebbe un IDOR ma sui file? e non ho capito molto bene il meccanismo con cui mi muovo tra i files. invece di LFI e RFI non ho capito proprio come funzionano, quale principio e vulnerabilità c'è dietro e nel pratico come avviene

**A2 - Cryptographic Failures**

Failures che riguardano la conservazione e quindi il furto di dati sensibili che circolano o vengono conservati senza una sufficiente protezione crittografica, come password in chiaro nei log, uso di algoritmi deboli, o mancata protezione di un DB

**A3 - Injections**

ho capito il concetto di usare un prompt SQL per accedere a dei dati che sono erroneamente non protetti, ma nell'esempio non capisco, nome e cognome che "hackeri" non sono quello che ci dovrebbe di base dare il DB? come è strutturata la query di "hacking" e come funziona la stampa di tutte le occorrenze? capisco a = a ma non capisco come fa questa cosa sempre vera a far stampare tutto

**Union Based** --> possibilità di concatenare i risultati di due select (nel pratico cosa significa?) ma richiede che le due select abbiano lo stesso numero di colonne

(spiega come coi null progressivi posso comprendere il numero di righe)

(nella "visione attaccante" di questa sezione, dici che tramite un injection SQL Union Based ho accesso a tutto il db e non solo alla tabella originale, cosa significa praticamente?)

**Command Injection** --> al posto di un prompt SQL studiato per tirare fuori qualcosa di specifico, una command injection si svolge dove posso inserire campi che poi interagiscono con un comando (inserisci esempio dell'ip con distinzione ; e &&)

**XSS (cross site scripting)** --> non c'ho capito una mazza, in che senso prospettiva dal server al browser, cos'è il motore javascript del browser e perchè viene colpito? che aspetto ha l'attacco nel concreto? cosa differenzia i tre tipi di scripting? rispiega in termini più capibili e chiariamente

**A4 - Insecure Design**

Vulnerabilità che non derivano da un bug implementativo dell'applicazione ma nella progettazione intriseca del sistema (aggiungi esempi)

**A5 - Security Misconfiguration:**

E' la categoria più amèia, raccoglie tutti gli errore di configurazione a tutti i livelli dello stack (quindi tutti i ngenerale? quali sono i "livelli dello stack"?) è la condizione alla base di qualunque attacco(?), ecco alcuni casi

**Credenziali di default**
(Spiega, ho capito ma non ho voglia di riscriverlo)

**Cifrari TLS deboli**
versioni di protocollo o cifrari obsoleti che espongono la comunicazione anceh se il sistema non ha bug applicativi

HTTP SECURITY HEADERS
non ho capito un cazzo, cosa sono, come funzionano, cosa fanno, nulla, spiega semplicemente e chiaramente

**SOP E CORS**
concetto lineare, l'unico dubbio che avevo è cosa succedeva se due siti dovevano effettivamente comunicare ma erano protetti da SOP, ma me lo ha irisolto introducendo CORS, qua insersici comunque una spiegazione e confronto tra i due

**XXE - XML External Entities**
non ho capito un cazzo, cosa sono, come funzionano, cosa fanno, nulla, spiega semplicemente e chiaramente

**A6 - Vulnerable and Outdated Components**
Autoesplicativo si parla di librerie, framework, OS con vulnerabilità note non patchate

**A7 - IDentification and Authentication Failures**
Lo stato di autenticazione è mantenuto da un meccanismo chiamato **session management** attraverso un cookie che il browser include in ogni richiesa HTML successiva al login.

Può essere aggirato da un attaccante che ottiene un token sessione prima del login della vittima, che convicerà a loggare usando quel token attraverso un link. da quel momento l'attaccante potrà fingersi la vittima loggandosi con quel token
(correggi se sbaglio)

spiega il concetto di Cross-site rquest forgery con l'esempio attacker.com e mybank.com

**A9 security logging and monitoring failures**
Quando si fallisce nel provvedere a un sistema di login sufficentemente sicuro, che non traccia gli accessi falliti, non fornisce dettagli sugli accessi, facilitando la via del brute forcing all'attaccante

**A10 Server-side request forgery**
non ho capito un cazzo, cosa sono, come funzionano, cosa fanno, nulla, spiega semplicemente e chiaramente

