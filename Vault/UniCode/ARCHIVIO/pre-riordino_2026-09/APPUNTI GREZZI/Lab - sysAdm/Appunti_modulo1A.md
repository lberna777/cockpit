**CREAZIONE DI UNO SCRIPT BASH**

**cat > "nomeFile.sh" &lt;< 'EOF'                --&gt;**                Uso cat con > per indirizzare il testo nel file "nomeFile.sh" creandolo se non esiste della directory attuale, con << 'EOF' dico di aspettare una riga con scritto                                                                                                  letteralmente EOF.

**SCRITTURA DI UNO SCRIPT BASH**

**\>         !/bin/bash                                                        SHEBANG:** Dico quale linguaggio usare per compilare il file, in questo caso bash

**\>        echo "ciao mondo, oggi è il** \$**(date)"**             Comando vero e proprio che stampa a schermo qualcosa (uso il \$() per inserire comandi dentro stringe di testo

**\>        EOF**

&nbsp;

Come visto nelle scorse lezioni, i file appena creati non sono eseguibili, uso **chmod 766 "nomeFile.sh"** oppure **chmod +x "nomeFile.sh"** e attribuisco al creatore i diritti di esecuzione. lo lancio con **./nomeFile.sh**

**VARIABILI IN UNO SCRIPT BASH**

E' possibile inserire variabili in uno script bash, scrivendole come testo con regole precise, per far si di usarle nello script senza stampare la vera linea di testo scritta.

\>        VARNOME="NOME"                                                                                Creo la variabile con questo schema preciso

\>        VARETA = 21

\>        echo "ciao \$NOME, hai \$ETA anni. Il tuo nome ha \${#NOME}                Uso le variabili create per stamparle, attraverso \$ con altri operatori posso estrapolare altre informazioni, come il conto dei caratteri

**VARIABILI SPECIALI**

| \$0 | Nome del file dove la si usa |
| --- | --- |
| **\$1, \$2, \$3, ...** | **Gli N elementi inseriti all'esecuzione del file -> ./nomeFile.sh elemento1 elemento2, elemento3** |
| **\$#** | **Numero di elementi inseriti all'esecuzione del file** |
| **\$@** | **Stampa tutti gli elementi inseriti all'esecuzione del file** |

Alcune variabili sono incluse nel sistema di base, \$HOME, \$USER, \$SHELL, \$PATH (che indica le directory da dove il computer pesca quando scrivi **ls**)

**ELSE / IF**

**Inserisci l'esempio di esercizio con else/if che hai fatto a me, assicurati di includere tutte le tabelle che hai messo per gli operatori tra numeri e stringhe e files, raccomanda l'importanza della formattazione, lo spazio tra le parentesi quadre e il contenuto dell if etc etc...**

**CONTROLLO FILE**

****Inserisci l'esempio di esercizio con il controllo dei file che hai fatto a me, assicurati di includere la specifica sui codici di uscita raccomanda l'importanza della formattazione dicendo a cosa stare attenti****

****LOOP****

vagrant@bookworm:~/Lab1A\$ cat > loop_for.sh << 'EOF'  
\> #!/bin/bash  
\> for FRUTTO in mela pera banana arancia; do                                                for VARIABILE in lista_elementi; do  
\> echo "Frutto: \$FRUTTO"                                                                                #comandi  
\> done                                                                                                                #done chiude il ciclo  
\> EOF

DUBBIO:         Ma qua creo le variabili direttamente nel for? non mi sembra di aver dichiarato nessuna variabile frutta prima. le stesse variabili che creo qua posso usarle dopo il done e prime dell'EOF?

&nbsp;

vagrant@bookworm:~/Lab1A\$ cat > loop_file.sh << 'EOF'  
\> #!/bin/bash  
\> for FILE in /etc/\*.conf; do  
\> echo "Trovato file di configurazione: \$FILE"  
\> done  
\> EOF

DUBBIO:        Perchè ho potuto scrivere for FILE? FILE è un nome gia conosciuto dalla macchina, sto istituendo che ogni elemento di quella cartella che termina in .conf venga considerato una variabile FILE?

&nbsp;

vagrant@bookworm:~/Lab1A\$ cat > loop_numerico.sh << 'EOF'  
\> #!/bin/bash  
\> for I in \$(seq 1 5); do  
\> echo "Iterazione numero: \$I"  
\> done  
\> EOF

DUBBIO: mi elenchi un po' di comandi utili e come utilizzarli come nel caso di \$(seq 1 5)?

**LOOP WHILE**

vagrant@bookworm:~/Lab1A\$ cat > loop_while.sh << 'EOF'  
\> #!/bin/bash  
\> CONTATORE=1  
\> while \[ \$CONTATORE -le 5 \]; do        -le significa minore uguale  
\> echo "Contatore: \$CONTATORE"  
\> CONTATORE=\$((CONTATORE+1))        \$(()) è la sintassi per l'aritmetica in bash, tutto ciò che accade nelle doppie parentesi è inteso come matematica  
\> done  
\> EOF

**PARTE 5 SCRIPT COMPLETO:** 

**nota:** Ho scritto tutto lo script e capito che prima di tutto analizza il primo argomento che gli viene passato, ne verifica l'essere una directory e in caso contrario restituisce errore, se no conferma dicendo che lancia lo script su quella directory, successivamente con un for analizzo tutti gli elementi (/\*) della directory passata, contando in due contatori separati file e directory, questi due dati insieme al totale degli elementi trovato viene stampato alla fine. purtroppo nello scrivere devo aver fatto un errore di battitura 

&nbsp;

vagrant@bookworm:~/Lab1A\$ cat > analizza_dir.sh << 'EOF'  
\> !/bin/bash  
\> DIRECTORY=\$1  
\>  
\> if \[ -z "\$DIRECTORY" \]; then  
\> echo "Uso: \$0 &lt;directory&gt;"  
\> exit 1  
\> fi  
\> if \[ -d "\$DIRECTORY" \]; then  
\> echo "ERRORE: \$DIRECTORY non è una directory"  
\> exit 1  
\> fi  
\>  
\> echo "=== Analisi di: \$DIRECTORY ==="  
\>  
\> CONTATORE_FILE=0  
\> CONTATORE_DIR=0  
\>  
\> for ELEMENTO in "\$DIRECTORY"/\*; do  
\> if \[ -f "\$ELEMENTO" \]; then  
\> CONTATORE_FILE=\$((CONTATORE_FILE + 1))  
\> elif \[ -d "\$ELEMENTO" \]; then  
\> CONTATORE_DIR=\$((CONTATORE_DIR + 1))  
\> fi  
\> done  
\>  
\> echo "File trovati: \$CONTATORE_FILE"  
\> echo "Directory trovate: \$CONTATORE_DIR"  
\> echo "Totale elementi: \$((CONTATORE_FILE + CONTATORE_DIR))"  
\> EOF

&nbsp;

**ESERCIZIO IN AUTONOMIA:**

questo è lo script che mi hai chiesto di fare come esercizio, correggilo eventualmente, considera che ho aggiunto convinto che servisse una verifica anche sui diritti di scrittura

vagrant@bookworm:~/Lab1A\$ cat > cerca_file.sh << 'EOF'  
\> !/bin/bash  
\>  
\> NOMEFILE=\$1  
\> NOMEDIR=\$2  
\>  
\> if \[ -e "\$NOMEFILE" \]; then  
\>  
\> else  
\> echo "ERRORE: \$1 non è un file o un path"  
\> fi  
\> if \[ -d "\$NOMEDIR" \]; then  
\>  
\> else  
\> echo "ERRORE: \$2 non è una directory"   
\> fi  
\>  
\> for ELEMENTO in "\$2"\$1; do  
\>  
\> if \[ -r "\$ELEMENTO" \]; then  
\> echo "il file \$ELEMENTO è leggibile"  
\> else  
\> echo "il file \$ELEMENTO non è leggibile"  
\> fi  
\> if \[ -w "\$ELEMENTO" \]; then  
\> echo "il file \$ELEMENTO è scrivibile"  
\> else  
\> echo "il file \$ELEMENTO non è scrivibile"  
\> fi  
\> EOF

&nbsp;

<!-- AUTO-LINKS:START -->
## 🔗 Collegati

- [[appunti_modulo1A_bash_scripting]]
- [[guida_lab_modulo1A_bash_scripting]]

**Hub:** [[master_map_studio]] · [[glossario_sysadm]] · [[concept_maps]] · [[troubleshooting_vm]] · [[metodo_studio_esami_pratici]]
<!-- AUTO-LINKS:END -->
