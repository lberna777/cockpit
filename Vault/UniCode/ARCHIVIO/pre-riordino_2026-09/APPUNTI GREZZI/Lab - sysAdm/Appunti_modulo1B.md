**FUNZIONI**

blocco di comandi a cui affido un nome specifico per poterlo riutilizzare

```bash
cat > funzione_base.sh << 'EOF'
[](#cb2-2)#!/bin/bash
[](#cb2-3)
[](#cb2-4)saluta() {
    [](#cb2-5)    echo "Ciao, sono la funzione saluta"
    [](#cb2-6)    echo "La data è: $(date)"
[](#cb2-7)}
[](#cb2-8)
[](#cb2-9)echo "Prima della chiamata"
[](#cb2-10)saluta
[](#cb2-11)echo "Dopo la chiamata"
[](#cb2-12)saluta
[](#cb2-13)EOF
[](#cb2-14)chmod +x funzione_base.sh
[](#cb2-15)./funzione_base.sh
```

Così creo la funziona saluta, che viene richiamata scrivendo semplicemente "saluta", senza le virgolette. la creazione tramite nomeFunzione() { *contenuto* } è congrua con la creazione di funzioni in C

**ARGOMENTI DELLA FUNZIONE**

Gli argomenti della funzione sono propri di questa, non appartengono allo script dove viene creata e usata. si assegnano al lancio, **nomeFunzione argomento.**        Per terminare con esito una funzione uso **return N** a differenza della terminazione con esito di uno script tramite **exit N**

```
cat > funzione_argomenti.sh << 'EOF'
[](#cb5-2)#!/bin/bash
[](#cb5-3)
[](#cb5-4)descrivi_file() {
    [](#cb5-5)    FILE=$1
    [](#cb5-6)    if [ -z "$FILE" ]; then
        [](#cb5-7)        echo "Errore: nessun file specificato"
        [](#cb5-8)        return 1
    [](#cb5-9)    fi
    [](#cb5-10)    if [ -f "$FILE" ]; then
        [](#cb5-11)        echo "$FILE: è un file regolare"
    [](#cb5-12)    elif [ -d "$FILE" ]; then
        [](#cb5-13)        echo "$FILE: è una directory"
    [](#cb5-14)    else
        [](#cb5-15)        echo "$FILE: non esiste"
    [](#cb5-16)    fi
[](#cb5-17)}
[](#cb5-18)
[](#cb5-19)descrivi_file /etc/hostname
[](#cb5-20)descrivi_file /etc
[](#cb5-21)descrivi_file /file_inesistente
[](#cb5-22)descrivi_file
[](#cb5-23)EOF
[](#cb5-24)chmod +x funzione_argomenti.sh
[](#cb5-25)./funzione_argomenti.sh
```

**VARIABILI DELLA FUNZIONE**

le variabili in bash sono sempre globali se non specificato diversamente tramite **local**. è buona pratica nelle funzioni usare sempre variabili **local**

```
cat > variabili_locali.sh << 'EOF'
[](#cb7-2)#!/bin/bash
[](#cb7-3)
[](#cb7-4)funzione_test() {
    [](#cb7-5)    GLOBALE="sono globale"
    [](#cb7-6)    local LOCALE="sono locale"
    [](#cb7-7)    echo "Dentro la funzione: GLOBALE=$GLOBALE, LOCALE=$LOCALE"
[](#cb7-8)}
[](#cb7-9)
[](#cb7-10)funzione_test
[](#cb7-11)echo "Fuori dalla funzione: GLOBALE=$GLOBALE"
[](#cb7-12)echo "Fuori dalla funzione: LOCALE=$LOCALE"
[](#cb7-13)EOF
[](#cb7-14)chmod +x variabili_locali.sh
[](#cb7-15)./variabili_locali.sh
```

**RESTITUIRE QUALCOSA DIVERSO DA UN INTERO TRAMITE UNA FUNZIONe**

Di base possiamo mandare segnali indietro dalla funzione solo tramite numeri interi tramite **return**. possiamo utilizzare echo però per passare un valore stringa

```
cat > funzione_ritorno.sh << 'EOF'
[](#cb9-2)#!/bin/bash
[](#cb9-3)
[](#cb9-4)ottieni_estensione() {
    [](#cb9-5)    local FILE=$1
    [](#cb9-6)    echo "${FILE##*.}"
[](#cb9-7)}
[](#cb9-8)
[](#cb9-9)ESTENSIONE=$(ottieni_estensione "documento.pdf")
[](#cb9-10)echo "Estensione: $ESTENSIONE"
[](#cb9-11)
[](#cb9-12)ESTENSIONE=$(ottieni_estensione "script.sh")
[](#cb9-13)echo "Estensione: $ESTENSIONE"
[](#cb9-14)EOF
[](#cb9-15)chmod +x funzione_ritorno.sh
[](#cb9-16)./funzione_ritorno.sh
```

`${FILE##*.}` è una **parameter expansion**: rimuove tutto fino all’ultimo `.` compreso, lasciando solo l’estensione. È introdotto qui come esempio utile — una panoramica completa delle parameter expansion è materiale avanzato.

DOMANDA: perchè passiamo documento.pdf alla funzione tra virgolette? prima gli argomenti passati alla funzione non erano racchiusi in virgolette, non gli dovremmo passare \$FILE?

**IL COSTRUTTO CASE**

\> #!/bin/bash  
\> GIORNO=\$1  
\>  
\> case \$GIORNO in  
\> lunedi|martedi|mercoledi|giovedi|venerdi)  
\> echo "\$GIORNO è un giorno lavorativo"  
\> ;;  
\> sabato|domenica)  
\> echo "\$GIORNO è un giorno festivo"  
\> ;;  
\> \*)  
\> echo "Giorno non riconosciuto: \$GIORNO"  
\> ;;  
\> esac  
\> EOF  
vagrant@bookworm:~/Lab1B\$ chmod +x case_bash.sh  
vagrant@bookworm:~/Lab1B\$ ./case_bash.sh lunedi  
lunedi è un giorno lavorativo  
vagrant@bookworm:~/Lab1B\$ ./case_bash.sh domenica  
domenica è un giorno festivo  
vagrant@bookworm:~/Lab1B\$ ./case_bash.sh stocazzo  
Giorno non riconosciuto: stocazzo

il costrutto **CASE** si sfrutta similmento allo switch in C si creano delle condizioni possibili che condizionano una risposta piuttosto che un altra, tramite return o la stampa a video con echo. Il caso \* indica tutto quello che non è racchiuso nei casi precedentemente selezionati. si istanza con **case \$VARIABILE in**

la struttura dei casi è **CASE1 | CASE2 | CASE3 | ...)**

dopo la conseguenza dell' entrata in un caso o gruppo di casi, ci sono **le doppie virgolette ;;** che indicano la chiusura del blocco

è essenziale **l'esac** prima della fine del file, **chiude il costrutto case, esattamente come fi chiude il costrutto if**

**ESEMPIO 2**

vagrant@bookworm:~/Lab1B\$ cat > case_file.sh << 'EOF'  
\> #!/bin/bash  
\> FILE=\$1  
\>  
\> if \[ -z \$FILE \]; then  
\> echo "\$FILE non è un file, uso: \$0 &lt;file&gt;"  
\> exit 1  
\> fi  
\>  
\> case \$FILE in  
\> \*.sh)  
\> echo "\$FILE: script bash"  
\> ;;  
\> \*.conf|\*.cfg)  
\> echo "\$FILE: file di configurazione"  
\> ;;  
\> \*.log)  
\> echo "\$FILE: file di log"  
\> ;;  
\> \*.txt|\*.md)  
\> echo "\$FILE: file di testo"  
\> ;;  
\> \*)  
\> echo "\$FILE: tipo non riconosciuto"  
\> ;;  
\> esac  
\> EOF  
vagrant@bookworm:~/Lab1B\$ chmod +x case_file.sh  
vagrant@bookworm:~/Lab1B\$ ./case_file.sh script.sh  
script.sh: script bash  
vagrant@bookworm:~/Lab1B\$ ./case_file.sh syslog.log  
syslog.log: file di log  
vagrant@bookworm:~/Lab1B\$ ./case_file.sh README.md  
README.md: file di testo  
vagrant@bookworm:~/Lab1B\$ ./case_file.sh stocazzo.txt  
stocazzo.txt: file di testo  
vagrant@bookworm:~/Lab1B\$ ./case_file.sh stoca  
stoca: tipo non riconosciuto

vagrant@bookworm:~/Lab1B\$ ./case_file.sh  
 non è un file, uso: ./case_file.sh &lt;file&gt;

Mi è chiaro il ragionamento e il funzionamento, tranne del primo if. non capisco, controlla se la variabile esiste ma non capisco ne perchè ne a cosa serva visto che dice che usa il file stesso dello script ma non fa nulla

**PARENTESI QUADRE DOPPIE PER COMODITA**

cat > test_combinati.sh << 'EOF'  
#!/bin/bash  
FILE=\$1

if \[ -f "\$FILE" \] && \[ -r "\$FILE" \]; then  
    echo "\$FILE esiste ed è leggibile"  
fi

if \[ -z "\$FILE" \] || \[ ! -e "\$FILE" \]; then  
    echo "Argomento mancante o file inesistente"  
fi  
EOF  
chmod +x test_combinati.sh  
./test_combinati.sh /etc/hostname  
./test_combinati.sh /file_inesistente  
./test_combinati.sh

  
Operatore Significato (nota: replica la tabella)  
\[ cond1 \] && \[ cond2 \] AND — vero se entrambe le condizioni sono vere  
\[ cond1 \] \\|\\| \[ cond2 \] OR — vero se almeno una condizione è vera  
\[ ! cond \] NOT — inverte la condizione

per sopperire alla macchinosità delle condizioni sommate or/and il bash consente l'uso delle doppie quadre, un costrutto più robusto

```
cat > double_bracket.sh << 'EOF'
[](#cb16-2)#!/bin/bash
[](#cb16-3)NOME=$1
[](#cb16-4)
[](#cb16-5)if [[ -n "$NOME" && "$NOME" != root ]]; then
    [](#cb16-6)    echo "Utente valido e non root: $NOME"
[](#cb16-7)fi
[](#cb16-8)
[](#cb16-9)if [[ "$NOME" == *"admin"* ]]; then
    [](#cb16-10)    echo "$NOME contiene la parola admin"
[](#cb16-11)fi
[](#cb16-12)EOF
[](#cb16-13)chmod +x double_bracket.sh
[](#cb16-14)./double_bracket.sh vagrant
[](#cb16-15)./double_bracket.sh sysadmin
```

Differenze principali tra `[ ]` e `[[ ]]`:

| Aspetto | `[ ]` | `[[ ]]` |
| --- | --- | --- |
| AND/OR | `[ c1 ] && [ c2 ]` | `[[ c1 && c2 ]]` — si può scrivere dentro |
| Pattern matching | non supportato | `[[ "$VAR" == *.sh ]]`funziona |
| Variabili non quotate | possono dare errori | gestite correttamente |
| Portabilità | POSIX — funziona ovunque | solo Bash — non funziona in sh puro |

OR \[ c1 \] && \[ c2 \] \[\[ c1 && c2 \]\] — si può scrivere dentro  
Pattern matching non supportato \[\[ "\$VAR" == \*.sh \]\] funziona  
Variabili non quotate possono dare errori gestite correttamente  
Portabilità POSIX — funziona ovunque solo Bash — non funziona in sh puro

**RESTITUZIONE DEL VALORE DI USCITA DI UNA FUNZIONE CON \$?**

Ogni funzione in bash restituisce un codice di uscita, per convenzione 0 se indica un successo, qualsiasi altro numero per indicare errori. attraverso **\$?.** E' essenziale usarlo la riga immediatamente successiva alla funziona che si vuole analizzare poichè viene sovrascritto da ogni nuovo codice di uscita di qualunque funziona successiva a quella interessata.

**SCRIPT FINALE** 

vagrant@bookworm:~/Lab1B\$ cat > diagnostica.sh << 'EOF'  
\> #!/bin/bash  
\>  
\> # ---- funzioni ----  
\>  
\> controlla_servizio() {  
\> local SERVIZIO=\$1  
\> if systemctl is-active --quiet "\$SERVIZIO"; then  
\> echo " \[OK\] \$SERVIZIO è attivo"  
\> return 0  
\> else  
\> echo " \[KO\] \$SERVIZIO non è attivo"  
\> return 1  
\> fi  
\> }  
\>  
\> controlla_file() {  
\> local FILE=\$1  
\> local TIPO  
\>  
\> case \$FILE in  
\> \*.conf) TIPO="configurazione" ;;  
\> \*.log) TIPO="log" ;;  
\> \*.sh) TIPO="script" ;;  
\> \*) TIPO="generico" ;;  
\> esac  
\> if \[\[ -f "\$FILE" && -r "\$FILE" \]\]; then  
\> echo " \[OK\] \$FILE (\$TIPO) - leggibile"  
\> elif \[ -f "\$FILE" \]; then  
\> echo " \[!\] \$FILE (\$TIPO) - esiste ma non è leggibile"  
\> else  
\> echo " \[KO\] \$FILE - non trovato"  
\> fi  
\> }  
\>  
\> # ---- main ----  
\>  
\> echo "=== Diagnostica sistema ==="  
\> echo ""  
\>  
\> echo ">> Servizi:"  
\> controlla_servizio ssh  
\> controlla_servizio cron  
\>  
\> echo ""  
\> echo ">> File critici:"  
\> controlla_file /etc/hostname  
\> controlla_file /etc/ssh/sshd_config  
\> controlla_file /var/log/auth.log  
\> controlla_file /file_inesistente.conf  
\> EOF  
vagrant@bookworm:~/Lab1B\$ chmod +x diagnostica.sh  
vagrant@bookworm:~/Lab1B\$ ./diagnostica.sh  
\=== Diagnostica sistema ===

\>> Servizi:  
 \[OK\] ssh è attivo  
 \[OK\] cron è attivo

\>> File critici:  
 \[OK\] /etc/hostname (generico) - leggibile  
 \[OK\] /etc/ssh/sshd_config (generico) - leggibile  
 \[!\] /var/log/auth.log (log) - esiste ma non è leggibile  
 \[KO\] /file_inesistente.conf - non trovato

Ho capito molto di questo script finale, il costrutto case usato nella identificazione del file, questa volta in maniera più semplice tramite una variabile locale. così come l'uso delle doppi quadre per poter concatenare delle condizioni nell'if. non mi è chiara però la funzione controlla_servizio ne nei dati che prende in input ne come li controlla.

**SCRIPT IN AUTONOMIA**

Ho scritto questo:

vagrant@bookworm:~/Lab1B\$ cat > classifica_dir.sh << 'EOF'  
\> #!/bin/bash  
\>  
\> DIR=\$1  
\>  
\> if \[ !-d "\$DIR" \]; then  
\> echo " \[KO\] \$DIR non è una directory"  
\> exit 1  
\> fi  
\>  
\> # ---- funzioni ----  
\>  
\> classifica_file() {  
\> local FILE=\$1  
\> local TIPO  
\>  
\> case \$FILE in  
\> \*.conf) TIPO="configurazione" ;;  
\> \*.log) TIPO="log" ;;  
\> \*.sh) TIPO="script" ;;  
\> \*) TIPO="generico" ;;  
\> esac  
\>  
\> echo " \$FILE è un file, di tipo \$TIPO"  
\> }  
\>  
\> # ---- main ----  
\> for FILE in \$DIR/\*; do  
\> if \[ -f "\$FILE" \]; then  
\> classifica_file \$FILE  
\> fi  
\> done  
\> EOF  
vagrant@bookworm:~/Lab1B\$ chmod +x ./classifica_dir.sh  
vagrant@bookworm:~/Lab1B\$ ./classifica_dir.sh /bin/bash  
./classifica_dir.sh: line 5: \[: !-d: unary operator expected  
vagrant@bookworm:~/Lab1B\$

sono conscio che non funzioni, ma l'errore è strettamente legato alla negazione della clausola con !-d, la versione corretta sarà una combinazione diversa di questi caratteri. per quanto riguarda le richieste, sistemato questo dovrebbe adempiere a tutto, tranne il conto separato di quanti file e quanti directory trovo nel path, perchè l'ho letto alla fine e avrei dovuto dichiarare precedentemente le variabili

&nbsp;

## Riepilogo sintattico

| Sintassi | Funzione |
| --- | --- |
| `nome() { ... }` | Dichiara una funzione |
| `nome arg1 arg2` | Chiama una funzione con argomenti |
| `local VAR=valore` | Variabile locale alla funzione |
| `return N` | Termina la funzione con exit code N |
| `$(funzione arg)` | Cattura l’output di una funzione come stringa |
| `case $VAR in p) ;; esac` | Confronto su pattern multipli |
| `p1\\|p2)` | OR tra pattern in case |
| `*)` | Pattern catch-all in case |
| `[ c1 ] && [ c2 ]` | AND tra condizioni |
| `[ c1 ] \\|\\| [ c2 ]` | OR tra condizioni |
| `[[ c1 && c2 ]]` | AND dentro doppie parentesi |
| `[[ "$VAR" == *pattern* ]]` | Pattern matching in doppie parentesi |
| `$?` | Exit code dell’ultimo comando eseguito |

&nbsp;

&nbsp;

<!-- AUTO-LINKS:START -->
## 🔗 Collegati

- [[appunti_modulo1B_funzioni_case_test]]
- [[guida_lab_modulo1B_funzioni_case_test]]

**Hub:** [[master_map_studio]] · [[glossario_sysadm]] · [[concept_maps]] · [[troubleshooting_vm]] · [[metodo_studio_esami_pratici]]
<!-- AUTO-LINKS:END -->
