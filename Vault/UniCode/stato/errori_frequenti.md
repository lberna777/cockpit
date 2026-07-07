# Errori Frequenti — Pattern Ricorrenti

> Aggiornato automaticamente da `/appunti` quando vengono corretti bug o imprecisioni.
> Letto da `/ripassa` e `/simula` per generare domande mirate sui punti deboli.
> Letto da `/lezione` per enfatizzare concetti dove Lorenzo tende a sbagliare.

---

## SysAdmin — Bash / Linux

### Sintassi Bash
| Errore | Modulo | Correzione |
|--------|--------|------------|
| `[ !-d ]` senza spazio | 1B | `[ ! -d ]` — spazio obbligatorio tra `!` e operatore |
| Logica invertita in condizioni | 1A, 1B | Testare sempre con caso limite prima di fidarsi |
| `done` mancante nei loop | 1A | Ogni `for`/`while` deve avere il suo `done` |
| Shebang incompleto | 1A | Sempre `#!/bin/bash` come prima riga |

### Concetti Linux
| Errore | Modulo | Correzione |
|--------|--------|------------|
| Confusione contare righe vs occorrenze con grep | 0B, es_02 | `grep -c` = righe, `grep -o \| wc -l` = occorrenze |

---

## Diritto — Imprecisioni Giuridiche

### Terminologia
| Errore | Modulo | Correzione |
|--------|--------|------------|
| Regolamenti UE: detti "non direttamente applicabili" | D1 | Regolamenti UE sono direttamente applicabili per definizione |
| Direttive UE: dette "ideali" | D1 | Direttive sono vincolanti quanto al risultato, non "ideali" |
| Diritti morali = 70 anni | D3 | Diritti morali sono imprescrittibili; 70 anni = diritti patrimoniali |
| Forma espressiva = funzione del software | D3 | La tutela copre la forma espressiva, non la funzione |
| Dato sensibile = capacità identificativa | D8 | Dato sensibile = natura dell'informazione (salute, orientamento, ecc.), non capacità identificativa |
| CC BY = pubblico dominio | D5 | CC BY ≠ pubblico dominio; CC0 = rinuncia totale inclusa attribuzione |
| FEQ definita genericamente | D9 | FEQ = dispositivo qualificato + certificato qualificato (due elementi precisi) |
| "danno" usato al posto di "nocumento" | D11 | Nocumento ≠ danno generico: è pregiudizio giuridicamente rilevante (condizione oggettiva di punibilità art. 621) |
| Titolo sezione parafrasato invece del nome del reato | D11 | Il reato si chiama "Intercettazione, impedimento o interruzione illecita" — non "Rivelazione di Intercettazioni" |
| 615-quinquies confuso con il danno effettivo | D11 | 615-quinquies = detenzione/diffusione strumenti per danneggiare. Il danno effettivo è famiglia 635-bis/ter/quater/quinquies |
| Citare il danno come elemento del 615-ter | D11 | Art. 615-ter è reato di mera condotta: si perfeziona con l'accesso, il danno non è richiesto né motivo del reato |
| Vittima della frode informatica identificata come persona | D11 | In art. 640-ter la vittima è il sistema informatico (manipolato), non una persona indotta in errore come in art. 640 |
| Reg. UE "non ancora in vigore" quando è solo "non pienamente applicabile" | D12 | "In vigore" = esiste e vincola; "pienamente applicabile" = tutte le norme operative. Reg. 2024/1689: in vigore 1/8/2024, pienamente applicabile 2/8/2026 |
| Lett. e) oggetto AI Act "uguale alla lett. a)" | D12 | Lett. a) = regole per sistemi IA in generale; lett. e) = regole specifiche per modelli GPAI — categorie e regimi distinti |
| Titolare dati (Data Act) confuso con utente | D13 | Nel Data Act: «titolare dei dati» = chi ha il diritto/obbligo di mettere a disposizione (es. produttore); utente = beneficiario del diritto di accesso. ≠ GDPR dove «titolare del trattamento» ha significato diverso |

### Pattern Ricorrenti Diritto
- **Tendenza a semplificare le distinzioni**: Lorenzo fonde concetti che il PDF tiene separati (es. variazioni richieste vs necessarie in D6, doppia base art. 6 + art. 9 in D8)
- **Definizioni parafrasate invece di fedeli al PDF**: il PDF della professoressa usa formulazioni precise che vanno riprodotte, non riformulate
- ~~Articoli citati senza numero preciso~~ → **NON rilevante**: la prof. ha confermato che numeri di articoli/leggi/date NON vanno memorizzati per l'esame (slide InfoGenerali, p. 8)

---

## Security — Comandi e Sintassi

### nmap
| Errore | Modulo | Correzione |
|--------|--------|------------|
| Porte separate da spazi: `-p 22 80 3306` | S1 | `-p 22,80,3306` — spazi fanno trattare i numeri extra come host aggiuntivi |
| `-sT` per version detection | S1 | `-sV` — `-sT` dice solo "aperta/chiusa", non il servizio; `-sV` legge il banner |
| Nmap senza `-p-` su porte non-standard | S1 | Sempre `-p-` quando si cerca tutto — porta 1337 non appare nel default ~1000 porte |
| `nmap -sn` senza `sudo` su host-only | S1 | `sudo nmap -sn` — senza sudo non può usare ARP, più lento e meno affidabile |

### psql
| Errore | Modulo | Correzione |
|--------|--------|------------|
| `\dt SELECT * FROM accounts;` tutto sulla stessa riga | S1 | `\dt` è meta-comando, `SELECT` è SQL — vanno su righe separate |
| Buffer sporco (prompt `->` che non esegue) | S1 | Digitare `\r` per resettare il buffer, poi ridigitare il comando |

### Trasferimento file
| Errore | Modulo | Correzione |
|--------|--------|------------|
| `scp` lanciato da dentro una sessione SSH | S1 | Aprire un nuovo terminale locale, lanciare scp da Parrot verso il target |
| `scp` su server con subsystem SFTP disabilitato | S1 | Usare `ssh -p <porta> user@ip "cat /path/file" > file` — non richiede il subsystem |

### Terminologia Security
| Errore | Modulo | Correzione |
|--------|--------|------------|
| FIDO descritto come "autorizzazione a doppia chiave" | S2 | FIDO riguarda l'**autenticazione** (chi sei), non l'autorizzazione (cosa puoi fare). "Doppia chiave" è impreciso: FIDO usa crittografia asimmetrica per autenticazione forte. |
| AXFR zone transfer: "espone solo il sottodominio richiesto" | S1 | AXFR restituisce l'**intera zona DNS** in una sola query — tutti i record A, MX, NS, CNAME, PTR, SOA. Non è un lookup puntuale. |
| Packet Filter descritto come "proprietà/filtro del firewall" | S5 | Il PF è uno dei **tre tipi fondamentali** di firewall (con ALG e CLG), non una proprietà interna di un firewall generico — è un'implementazione concreta del concetto architetturale "firewall", non un suo attributo. |

### Pattern Ricorrenti Security
- **Narrativa vs comandi**: tendenza a perdere il filo (cosa sto facendo e perché). Costruire sempre la catena: *che informazione ho → cosa cerco → quale comando la trova*.
- **Assumere che gli IP degli esempi siano i propri**: gli IP nei PDF del corso (.32/.33/.34) sono esempi — verificare sempre con `ip a` + `nmap -sn`.
- **Autenticazione vs autorizzazione**: la distinzione AAA viene formulata correttamente in teoria, ma scivola in pratica quando si descrivono sistemi concreti (FIDO, S2). Verificare ogni volta che si parla di un protocollo: *sta stabilendo chi sei (auth) o cosa puoi fare (authz)?*

---

## Come Aggiornare

Quando `/appunti` identifica un bug o un'imprecisione:
1. Verificare se il pattern esiste già in questo file
2. Se sì: incrementare il contatore o aggiungere il nuovo modulo alla riga esistente
3. Se no: aggiungere una nuova riga nella sezione appropriata
4. Se emerge un pattern ricorrente (stesso tipo di errore in 3+ moduli): aggiungerlo alla sezione "Pattern Ricorrenti"
