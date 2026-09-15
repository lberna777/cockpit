
**Autenticazione / Autorizzazione / Auditing**

Autenticazione è l'attribuzione certa dell'identità di un soggetto che usa il sistema. include un'**identificazione** preliminare, che non è sufficiente a dichiararsi autenticati.
l'identificazione è il **nome che dichiari** mentre l'autenticazione è la **prova che quel nome sia davvero tuo**

Autorizzazione è la verifica dei **diritti** di un soggetto di **compiere un azione su un determinato oggetto** nel sistema. o se ne a il permesso o non lo si ha. i propri permessi sono definiti **dopo l'autenticazione**. su Linux, **PAM** gestisce l'autenticazione, **sudo** e i **permessi su file** gestiscono l'autorizzazione.

Auditing è il tracciamento delle **decisioni di autenticazione e autorizzazione**. ma è base di un compromesso. più dettagliato è il log, più ne risentono prestazioni e privacy

**I fattori dell'autenticazione - come può essere il segreto?**
L'autenticazione si basa su ciò che l'utente **conosce, possiede, è, o fa**. il **prover (P)** deve dimostrare al **Verifier (V)** di conoscere un segreto dei tipi elencati prima:

Sono quindi fattori di autenticazione: **password, PIN, risposte segrete**, sicure fino a quando la password fuoriesce dal canale o DB del verifier, **hard-token, Yubikey, chiavette**, non si possono clonare via rete ma non sono infallibili. **Dati biometrici: iride, impronta...**, sicure finchè non compromesse, ma anche incambiabili in quanto uniche, e infine **GPS, localizzazione**, ma come fattore contestuale, per dire, la posizione non è sufficiente a fare il login, ma al contrario se la posizione non è conosciuta ci obbliga a passare uno step di sicurezza in più.ù

**/etc/shadow: dove vive il segreto lato server**

/etc/shadow è il file che contiene la **fingerprint della password**, una versione **criptata** della password stessa ottenuto dalla **concatenazione password || salt**. il **salt** è una **variazione random** generata quando scelgo la password, e serve a rompere la simmetria, così che **due utenti** con la stessa password **non abbiano la stessa fingerprint**.

il **salt non basta però a difendersi da attacchi offline**, se un attaccante viene in possesso di /etc/shadow può attaccarlo con **metodi brute force** senza limite di tentativi, e per questo la contromisura base più efficace è avere una **password difficile da brute forcare**

Esiste anche **Pepper**, una variante di salt che vive in un **HSM (Hardware Security Module)** a cui l'attaccante non accede anche se copia /etc/shadow. così facendo si impossibilita l'attaccante a **calcolare** la password

(mi spieghi cos'è un HSM nel pratico? che forma ha? cos'è?)

**Password: L'entropia conta più della complessità percepita**

(ho capito il concetto leggendo dal pdf, replicalo qua, ma spiega il concetto di entropia, in base a cosa si ottiene, cosa la determina?)

**Autentiazione passiva vs attiva**

L'autenticazione **passiva**, dove P e V concordano un segreto e lo memorizzano, è il modello della password classica. presenta **problemi strutturali**, se il segreto viaggia in chiaro può essere **intercettato** e anche se è offuscato, se è sempre lo stesso, basta **catturarlo e riprodurlo**. inoltre, V possiede una copia del segreto, e in caso di **compromissione di V** tutti i segreti sono a rischio.

(Spiega meglio, più semplicemente e chiaramente, il concetto di autenticazione attiva, con qualche esempio, la descrizione che hai fatto mi ha confuso, pensavo fosse una sorta di 2fa ma non lo è. stessa cosa per SKEY ONE TIME PASSWORD)

**/etc/pam.d/: il framework che collega tutto a Linux**

PAM (**Pluggable Authentication Modules**) è il (che cos'è?) a cui ogni programma in Linux delega l'autenticazione dell'utente, facendogli caricare **moduli configurabili per programma**. la configurazione per ogni programma vive in /etc/pam.d/, un file per ogni programma

(tabella accurata che spiega più chiaramente tutti i parametri della riga di pam.d, specialmente il control-flag di cui non ho capito proprio a che cosa serva.)

(dopo la tabella aiutami a capi il concetto della modularità di questo sistema, parli dell'importanza dell 'ordine dei moduli, cosa sono? come funzionano? schematizza i più comuni, spiega a parole meglio e rendi tutto chiaro)

**2FA vs 2SA vs MFA**

**2FA (Two-Factor Authentication)**: richiede 2 fattori di autenticazioni, e devono essere distinti, ovvero provenire da due categorie diverse (ciò che l'utente **conosce, possiede, è, o fa**, mix & match di 2 a piacere). 

**2SA (Two-Step Authentication)**: richiede 2 passi ma non necessariamente due fattori distinti. Lo sono le autenticazioni tramite **OTP** via sms, o mail, che sono mezzi non considerati attendibili per **l'autenticazione di secondo fattore** perchè chi controlla il canale può **intercettare il codice**

**MFA (Multi-Factor Authentication)**: generalizza 2FA a **più di due fattori**

**FIDO: standard di crittografia a chiave pubblica per il grande pubblico**

FIDO (**Fast IDentity Online**) è un consorzio di big tech che ha sviluppato uno standard per rendere l'autorizzazione a doppia chiave usabile su larga scala

**FIDO UAF (Universal Authentication Framework)** è lo standard per autenticazione senza password, quando l'utente di autentica localmente sul dispositivo con **biometria o pin**, il dispositivo usa questa verifica per **sbloccare una chiave privata** che firma la sfida emessa dal server FIDO UAF. in questo modo **le informazioni di sicurezza non lasicano mai il dispositivo**

**FIDO U2F (Universal Second Factor)** è l'evoluzione che raffrorza e semplifica la 2FA usando dispositivi hardware (chiavette, NFC, o bluetooth)

**DOMANDE DI AUTOVERIFICA**
1:C 2:F 3:B 4:non ho capito l'argomento 5:non ho capito l'argomento 6:falso






