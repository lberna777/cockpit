

![](https://virtuale.unibo.it/theme/image.php/boost_union/assign/1773824434/monologo?filtericon=1)

# Estensione degli esercizi risolti

Aggregazione dei criteri

**Aperto:** martedì, 10 marzo 2026, 00:00

**Data limite:** venerdì, 3 aprile 2026, 19:00

Estendere gli script illustrati di conversione e manipolazione del tempo per gestire, in tutte le versioni proposte, la rimozione delle notifiche relative a eventi che vengono rimossi dal calendario.

![](https://virtuale.unibo.it/theme/image.php/boost_union/assign/1773824434/monologo?filtericon=1)

# "Estensioni" parametrico

Aggregazione dei criteri

**Aperto:** lunedì, 9 marzo 2026, 00:00

**Data limite:** venerdì, 3 aprile 2026, 19:00

Modificare l'esercizio delle estensioni realizzando uno script estparam.sh che accetti sulla riga di comando

- un nome di directory da esplorare
- un elenco di lunghezza arbitraria di stringhe

Lo script deve contare quanti file esistono nel sottoalbero definito dalla directory passata come primo parametro, che abbiano estensione uguale a una delle stringhe specificate coi parametri successivi. La soluzione deve essere efficiente, non deve invocare comandi pesanti sul filesystem in modo ridondante.

Esempio: 

**./estparam /etc conf inc  
****56 conf  
28 inc**


## **FUNZIONI, CASE, TEST**


Realizzare una funzione **waitfile** che accetti

- un primo parametro obbligatorio = nome di comando
- un secondo parametro obbligatorio = nome di file
- un terzo parametro facoltativo 

La funzione deve 

- controllare che il valore di $1 sia uno di **ls**, **rm**, **touch**
- eseguire il comando $1 con parametro $2 (basta lanciare $1 $2) in modi diversi a seconda di $3 come spiegato di seguito

Usando case, discriminare tre possibilità:

- $3 è "force" --> esecuzione immediata
- $3 è un numero "N" di una cifra decimale --> se $2 non esiste, aspetta che eventualmente compaia, riprovando al massimo N volte con un'attesa di 1 secondo tra un tentativo e il successivo (usare sleep 1)
- $3 è assente o altro valore --> come caso precedente, considerando un valore di default N=10

La funzione deve ritornare exit code significativi e messaggi d'errore dove opportuno.




============ processi =================

Estendere l'esempio dell'esecuzione di due job in parallelo.

Realizzare uno script **parallenne.sh** che 

- lanci in parallelo tutti i comandi forniti come parametri
- controlli ogni 5 secondi quali sono ancora in esecuzione, verificando che il PID corrisponda al nome del comando
- scriva a ogni controllo sul file "log" lo stato dei processi 
- termini quando tutti i processi in background sono terminati
- garantisca la terminazione di tutti i processi in background se viene terminato dall'esterno il processo parallenne

![](https://virtuale.unibo.it/theme/image.php/boost_union/assign/1773824434/monologo?filtericon=1)

# Segnali girati

Aggregazione dei criteri

**Aperto:** mercoledì, 15 marzo 2023, 00:00

**Data limite:** lunedì, 3 aprile 2023, 19:00

Cosa dovrebbe fare secondo voi questo script?

Perchè non funziona, e come va corretto?

#!/bin/bash  
report () {  
	echo $(date) osservate $TOT nuove righe  
	TOT=0  
}  
echo $BASHPID > /tmp/logwatch.pid  
TOT=0  
trap report USR1  
tail -n +0 -f "$1" | while read R ; do  
	TOT=$(( $TOT + 1 ))  
done


  
Conta occorrenze avanzato

Scrivere uno script bash che dato il file allegato all'esercizio [Conta occorrenze](https://virtuale.unibo.it/mod/assign/view.php?id=2239085 "Conta Occorrenze") ([The_Adventures_Of_Sherlock_Holmes.txt](https://virtuale.unibo.it/pluginfile.php/2919797/mod_assign/introattachment/0/The_Adventures_Of_Sherlock_Holmes.txt?forcedownload=1)):  

- Lanciare due processi in parallelo che contino le occorrenze della parola 'sherlock' case insensitive, il primo processo deve leggere la prima metà del file il secondo processo la seconda metà, alla fine restituisca il risultato totale sul terminale. Per definire metà del file si contino le righe totali e si arrotondi per difetto la prima metà in caso le righe siano dispari
- Eseguire lo stesso esercizio proposto sopra ma quando uno dei due processi termina prima dell'altro questo deve segnalare prontamente la cosa al processo che stà ancora lavorando il quale deve gestire l'interruzione interrompendo il conteggio e restituendo il risultato parziale in un file temporaneo scelto in precedenza; dopo di che deve proseguire il conteggio; lo script deve restituire la somma dei due risultati parziali stampata a terminale