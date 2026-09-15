# Template — report.txt (Network Intrusion Detection)

> Struttura riutilizzabile per il resoconto testuale richiesto negli esercizi di tipo
> Network Intrusion Detection (S10). Ogni sezione ha, tra `[ ]`, **da dove** ricavare
> l'informazione e **con quale comando/azione**. Vedi `modello_network_intrusion_detection.md`
> per un esempio completo già risolto, e `esercizi/SICINF/pratica_NIDS_2025-02-13/report.txt`
> per un esempio reale compilato da zero.

```
ANALISI DEL TRACCIATO <nome_file.pcap>
[nome file: quello scaricato da Virtuale]
(catturato su router che connette N host/subnet diverse)
[N e le subnet: Wireshark -> ordina per colonna Source (click sull'intestazione
nella lista pacchetti) -> conta quanti IP sorgente distinti compaiono e le loro subnet]

METODO:
[una riga fissa, riusabile sempre uguale — cambia solo se hai usato strumenti diversi]
Analisi in Wireshark: ordinamento per indirizzo sorgente (colonna Source),
poi Statistics -> Protocol Hierarchy per la vista d'insieme dei protocolli
presenti, poi Statistics -> Conversations (tab TCP/UDP) per isolare i
singoli flussi, e Follow -> TCP/UDP Stream per ispezionare il contenuto
applicativo di ciascun gruppo di conversazioni.

TRAFFICO INDIVIDUATO:

1. <NOME TIPO DI TRAFFICO>
   [nome: Statistics -> Protocol Hierarchy ti dice quali protocolli applicativi
   sono presenti (SMTP, HTTP, DNS, Telnet, ...) e la % di ciascuno]
   - Host coinvolti: <IP o rete sorgente> <-> <IP o rete destinazione>, porta <N>
     [ricava IP/porte da: Statistics -> Conversations, tab del protocollo
     giusto (TCP/UDP). Se la consegna chiede reti /24 (non singoli host),
     scrivi la rete, non il singolo IP]
   - Descrizione: [perché è innocuo — apri Follow Stream su un esempio e
     controlla: 1) la richiesta è sintatticamente valida? 2) contenuto/path
     sospetti? 3) risposta anomala? 4) frequenza/volume compatibile con uso
     normale? Scrivi la conclusione con la prova, non solo l'aggettivo]

2. <NOME TIPO DI TRAFFICO>
   - Host coinvolti: ...
   - Descrizione: ...

3. ICMP
   [quasi sempre presente e quasi sempre ignorato per errore — controllalo:
   filtro Wireshark "icmp", guarda colonna Info per il tipo (Echo request/
   reply, Destination unreachable, ...) e sorgente/destinazione]
   - Host coinvolti: ...
   - Descrizione: ...

N. ATTACCO INDIVIDUATO: <nome/tipo>
   [il tipo si deduce da CONTENUTO (stringa/pattern anomalo nel payload) o
   da COMPORTAMENTO (volume/frequenza anomali) o entrambi]
   - Sorgente: <IP/rete>  ->  Vittima: <IP/rete>, porta <N>
   - Come l'ho riconosciuto:
     a) Contenuto: [Follow Stream sul gruppo sospetto -> cerca stringhe,
        path, parametri fuori dal comune rispetto al traffico legittimo
        analogo (stesso protocollo, confronta i due Follow Stream fianco
        a fianco)]
     b) Frequenza/volume: [Wireshark -> attiva "Time delta from previous
        displayed packet" in View -> Time Display Format -> Seconds Since
        Previously Displayed Packet, poi guarda la colonna Time sui
        pacchetti del gruppo sospetto e del gruppo legittimo, confrontali]
   - Perché è incompatibile con uso legittimo: [confronto esplicito col
     punto 2 — stesso protocollo, comportamento diverso: quale differenza
     numerica/qualitativa lo dimostra]

REGOLA SURICATA SCRITTA (exam.rules):
[scrivi qui la regola: azione + protocollo + sorgente + porta -> dest + porta
(msg:"..."; content:"..."; <buffer keyword tipo http_uri se serve>; sid:<numero
univoco >=1000000>; rev:1;) — vedi modello_network_intrusion_detection.md per
la sintassi completa]

DISCUSSIONE DEI LIMITI DI SURICATA RISPETTO A QUESTO ATTACCO:
[SOLO se la consegna lo chiede esplicitamente, O se l'attacco vive sotto il
livello IP (es. ARP spoofing/poisoning — Suricata non ha sintassi per
condizionare un alert su un pacchetto ARP o un MAC address). In quel caso
la regola è un'approssimazione dichiarata (es. pattern $GOOD_NET/$BAD_NET),
non un rilevamento diretto — spiega qui perché. Vedi il secondo caso in
modello_network_intrusion_detection.md per un esempio completo]

VERIFICA — LA REGOLA FUNZIONA:
Comando eseguito:
  mkdir -p <dir_output>
  suricata -r <pcap> -S exam.rules -l <dir_output>
  [verifica che non stampi errori di parsing della regola all'avvio]

Numero di alert generati: <N>
  [comando: grep -c '"signature_id":<sid>' <dir_output>/eve.json — NON "sid",
  nel JSON il campo si chiama signature_id (annidato in "alert":{...}); se il
  conteggio sembra 0 verifica prima con grep -c '"event_type":"alert"' che
  ci siano alert di qualunque tipo, per escludere che sia solo il grep sbagliato]

Esempio di alert (da eve.json):
  [comando: grep '"signature_id":<sid>' <dir_output>/eve.json | head -1
  poi trascrivi SOLO i campi rilevanti (src_ip, dest_ip, http.url o
  content applicativo, signature_id, timestamp) — non incollare il JSON
  grezzo né il terminale con prompt/decorazioni: riscrivi pulito]

NOTA SU suricata.yaml:
[di default NON serve modificarlo se la regola specifica reti/IP espliciti
invece di $HOME_NET. Se invece la regola usa $HOME_NET, o se serve abilitare
qualche opzione (es. payload-printable per leggere il payload in eve.json),
scrivi qui cosa hai cambiato e perché]
Consegnato invariato / modificato in <punto X> perché <motivazione>.
```

## Confezionamento finale della consegna

Nella cartella dove hai già `report.txt` e `exam.rules`, copia gli altri due file richiesti:
```
cp /etc/suricata/suricata.yaml .
cp <dir_output_suricata>/eve.json .
ls -la
```
Verifica che ci siano tutti e 4: `report.txt`, `exam.rules`, `suricata.yaml`, `eve.json`.

---

## Checklist rapida prima di consegnare

- [ ] Ogni tipo di traffico (anche quello innocuo) ha una riga che spiega **perché** è innocuo o malevolo — mai solo "è normale" senza motivazione.
- [ ] Hai controllato **anche** l'ICMP, non solo TCP — è facile da dimenticare perché di solito non contiene l'attacco, ma la consegna chiede tutti i tipi di traffico.
- [ ] L'attacco è descritto sia nel **contenuto** (cosa c'è nel payload, citato testualmente) sia nel **comportamento** (volume/frequenza, con numeri) — i due argomenti si rinforzano a vicenda.
- [ ] La regola Suricata è stata **testata** (non solo scritta) — il numero di alert generati è riportato, non solo ipotizzato.
- [ ] Le reti nella regola e nel report sono coerenti: se la consegna chiede "rete /24", scrivi `X.X.X.0/24`, non il singolo IP dell'host che hai osservato.
- [ ] Nessun terminale grezzo incollato (prompt, decorazioni, ANSI) — solo comando + risultato rilevante, riscritti puliti.
- [ ] `suricata.yaml` ha una nota esplicita sul perché è invariato o cosa è stato modificato — mai consegnarlo senza commento.
