# Giornata 2026-11-09

<!-- Claude appende qui, una riga per fatto: HH:MM · CODICE · fatto.
     Marcatori: CHIUSO <cod> <mod> · RIPASSO <cod> <mod> ok|debole -->

11:59 · PIANO · pianificati settimana e giorno: 3 attività nuove + 3 riallineate nella Plancia (weekend 7–8/11 senza studio, LAB08 slitta a gio 12)
12:09 · CALC · conti esa: somme ok, sottrazione E0000200h−4 → 1FB (prestito tolto due volte nella stessa colonna), corretto
12:11 · CALC · non sa convertire decimale→esa: spiegate le divisioni successive per 16 (esempio 300 = 12Ch), prova su 1000
12:15 · CALC · 1000 → 000003E8h da solo con le divisioni per 16 (guidato passo passo); ora potenze di 2 in esa
12:21 · CALC · 2^20 = 100000h ok; 2^21 → 100001h (sommato 1 invece di moltiplicare per 2: il resto dell'esponente usato come addendo), corretto
12:26 · CALC · 2^30 = 40000000h da solo (regola esponente = 4k + r); riscaldamento esa chiuso
12:34 · CALC · ripasso 2023-01-17 a voce: RAM 80000000h–FFFFFFFFh, EPROM 1280 MB = 500h MB = 50000000h → 0–4FFFFFFFh, da solo; capito perché OUT a 80000000h stava nella RAM
12:37 · CALC · porte della 2023-01-17 rifatte: 5 porte (4 IN + OUT) a 50/58/60/68/70000000h, dopo correzione (prima 70000001h/02h: BA1–BA0 non arrivano sul bus); errori del 5/11 ripassati
12:40 · CALC · esempio 4 (03): LW letta come «scrive R3 in memoria» — verso load/store invertito, di nuovo (pattern 5, già il 5/11); R2 come parte dell'indirizzo ok
12:42 · CALC · errore mio di ritmo (di nuovo, come il 5/11): domande sul ciclo prima che Lorenzo finisse la lettura riga per riga; ripreso al suo passo
12:45 · CALC · esempio 4 (03) letto riga per riga da solo dopo la LW: ruoli R1 accumulatore/valore, R3 valore, R7 indirizzo, R2 contatore (anche indice: non visto da solo); confusi accumulatore e contatore, «indirizzi alti» per i bit alti di LHI; capito lo scopo con l'analogia del for in Java
12:50 · FI2 · guida-lab LAB08 generata (scheda, 60 test, startkit in da_importare/LAB08_EDLift-091126)
12:50 · CALC · scheda del checkpoint 10/11 generata (lezioni/guida_lab_02_prova_2024-01-19.md, parte memorie, a freddo 60 min)
14:22 · FI2 · LAB08 avviato seguendo il PDF; domanda di Lorenzo (sl. 3): «accetta in movimento» e «più chiamate» sono la stessa cosa? — separati con due casi limite (stato vs struttura dati); pattern 1 intercettato da lui stesso
14:39 · FI2 · LAB08 sl. 10: chiesto cosa vuol dire classe/metodo astratto — spiegato da 20 sl. 2–8 su Lift (concreto = comune, astratto = varia per tipo)
15:28 · FI2 · LAB08 BasicLift.goToFloor prima versione: logica di sl. 16 giusta (REST → setRequestedFloor), ma cambiava lo stato UP/DOWN (compito del controller), rifiutava lo stesso piano, mancava checkArrivalFloor
15:35 · FI2 · LAB08 BasicLift: BasicLiftTest 15/15 verdi (lanciati da Claude nel cloud sul codice incollato); ritocchi: togliere BasicLift.super., aggiungere @Override
16:07 · FI2 · LAB08 HealthyLift: bloccato sul «piano prima» (pensava ai negativi, il punto è la direzione) e ha scambiato MODIFIED per uno stato dell'ascensore (RequestResult vs LiftState: pattern 1)
