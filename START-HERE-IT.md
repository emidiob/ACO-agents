# ACO v0.4.2 — inizia qui, senza conoscere Git

**Cos’è:** una libreria di istruzioni e strumenti per ChatGPT/Codex. **Non è un plugin e non è un’app da aprire ogni mattina.** Tu descrivi il lavoro; ACO sceglie i ruoli e usa gli strumenti effettivamente disponibili.

**Tre cose diverse:** aggiornare GitHub mette online la libreria; installare in Codex aggiorna le copie sul tuo computer; collegare Drive abilita l’accesso alla tua knowledge privata. Nessuna delle tre implica automaticamente le altre.

## Licenza in due righe

ACO v0.4.2 è **source-available ma proprietario**. Puoi usarlo personalmente o internamente, modificarlo in privato e usarlo per produrre lavoro commerciale per i tuoi clienti. **Non puoi ridistribuire ACO, pubblicare fork, rivenderlo, sublicenziarlo o incorporarne parti sostanziali in prodotti distribuiti a terzi senza autorizzazione scritta.** Vedi `LICENSE`.

## 1. Hai già il repository ACO? Aggiornalo così

1. Scarica ed estrai lo ZIP v0.4.2 in una cartella nuova, **fuori** dalla cartella del repository già esistente. Non copiare a mano solo i file visibili: ci sono anche file nascosti importanti.
2. Apri in Codex il tuo repository `emidiob/ACO-agents`. Allega il nuovo ZIP oppure indicagli la cartella estratta reale.
3. Incolla il testo qui sotto. Non devi comprendere i comandi Git; Codex li esegue e ti mostra l’esito.

```text
Aggiorna questo repository con il pacchetto ACO v0.4.2 che ti ho fornito.
Leggi docs/CODEX-MIGRATION-PROMPT.txt DEL NUOVO PACCHETTO.
Usa la migrazione controllata: anteprima, backup, applicazione, test e controllo del diff.
Preserva .git, cronologia, file privati, file estranei e lavoro locale.
Non usare git clean, reset --hard, cancellazioni generiche o force push.
Se i controlli passano, autorizzo il commit e il push sicuro su origin/main.
Riporta versione, commit, test e risultato effettivo del push.
Non modificare Google Drive e non installare plugin o servizi esterni.
```

**Come controlli:** dopo il push, ricarica il README su GitHub. Deve mostrare **0.4.2, 16 skill, 349 ruoli**. La segreteria, Production e Publishing devono comparire nell’indice. Il repository pubblico non deve contenere i tuoi clienti, numeri di telefono, contesti compilati o file di Drive.

Se Codex segnala file modificati o conflitti, non dirgli di cancellarli: chiedi il confronto e conserva il lavoro. Il backup non autorizza a distruggere dati privati.

## 2. Vuoi usarlo qui in ChatGPT?

**Non serve installare nulla sul Mac.** Servono un modo autorizzato di leggere il repository e, solo se desideri memoria, un collegamento separato a Drive.

Crea o usa un progetto privato ChatGPT e incolla nelle sue istruzioni il contenuto di `docs/CHATGPT-PROJECT-INSTRUCTIONS.txt`. Puoi anche iniziare una chat normale con:

```text
Usa ACO dal repository GitHub emidiob/ACO-agents.
Leggi CHATGPT.md e le sole skill necessarie per questa richiesta.
Chiedimi subito le informazioni decisive che mancano, poi lavora con aggiornamenti brevi.
Per ora non usare dati privati e non inviare messaggi.
```

Poi chiedi il lavoro normalmente, ad esempio: **“ACO, prepara la produzione di un film di 30 secondi. Prima chiarisci cosa ti manca.”**

Se ChatGPT non riesce a leggere il repository, deve dirlo. Allegare i file Markdown necessari è una possibilità; non significa che una libreria non letta sia stata caricata. La disponibilità dei collegamenti dipende dal tuo ambiente/account.

## 3. Vuoi usarlo in Codex o nell’estensione VS Code?

Usa la cartella completa aggiornata. Puoi aprire `Install ACO.command` sul Mac, oppure chiedere a Codex:

```text
Leggi il README di ACO v0.4.2 e controlla l’ambiente con doctor.
Installa le skill con l’installer incluso.
Non installare tutti i profili nativi se non servono; mostra la selezione.
Non cambiare i miei permessi, i plugin o i file privati.
Verifica l’installazione e dimmi l’esito reale.
```

Se vuoi TUTTI i profili nativi facoltativi, autorizzalo esplicitamente. L’installer usa `--offices all`; per i soli uffici utili, ad esempio `production-office publishing-office finance-office administration-office product-office`. Tutte le 16 skill restano disponibili con le loro istruzioni; i profili nativi sono un’aggiunta, non obbligatori.

**Prerequisito per gli script locali:** Python 3.11 o successivo. Se manca, Codex deve spiegare come installarlo tramite una fonte approvata, non disattivare protezioni. Se macOS blocca un file scaricato, esamina lo script e usa l’approvazione prevista dal sistema; non disattivare la sicurezza globalmente.

Riavvia/apri una nuova sessione Codex se la nuova versione non appare. Usa una cartella di lavoro diversa per il sito, video o progetto di un cliente. Non mettere il lavoro del cliente dentro la libreria pubblica ACO.

**Controllo:** `install-status` verifica i file locali; chiedere “usa ACO” verifica anche se il tuo host legge davvero la skill. Il solo messaggio “copia completata” non prova l’integrazione in Codex.

## 4. Dove va la memoria?

Su Drive, o in una cartella privata locale fuori da Git. Se hai già una knowledge ACO, **non crearne una seconda**.

```text
Usa questa cartella privata come knowledge ACO: [inserisci il link solo qui].
Controlla se è già inizializzata. Riutilizza ciò che esiste e crea solo ciò che manca.
Se richiede una migrazione, confronta i documenti e conserva gli originali.
Non condividere nulla e non cercare in cartelle non autorizzate.
```

Con strumenti di scrittura autorizzati, ACO prepara registro/cartelle e verifica il risultato. In sola lettura può lavorare sui dati, ma deve lasciare gli aggiornamenti **in attesa**, non dichiararli salvati. Lo ZIP pubblico non contiene la tua knowledge e non configura automaticamente account o autorizzazioni.

## 5. Più aziende, clienti e attività

Parla in modo naturale, indicando il contesto quando cambia:

> Per l’azienda A, attività publishing, cliente X: prepara un catalogo con versione cartacea ed EPUB.

> Per l’azienda B, prepara il cash flow. Non usare i dati dell’azienda A.

> Torniamo alla mia pratica artistica: organizza la prossima mostra.

ACO deve mantenere separati i contesti e chiedere se il cliente è ambiguo. Un libro con stampa e versione audio può avere un progetto unico con deliverable distinti. Dossier HR e dati finanziari riservati richiedono permessi reali separati, non soltanto una cartella diversa.

## 6. Email, WhatsApp e telefonate

**“Scrivi”** significa prepara una bozza. **“Invia”** richiede destinatario corretto, contenuto autorizzato e un vero strumento di invio.

> Prepara un WhatsApp per questo contatto. Non inviarlo.

> Invia questa versione al contatto verificato tramite il mio MCP WhatsApp, se disponibile.

> Prepara una telefonata al fornitore per chiedere disponibilità. Non impegnarmi a comprare nulla.

Se l’integrazione manca, ACO ti dà subito il testo da copiare. Per una telefonata ti prepara apertura, domande e copione per la segreteria telefonica. Se un tool legge le chiamate ma non può farle, non può telefonare. WhatsApp messaggi e WhatsApp chiamate non sono la stessa capacità. L’esito **accettato/in coda** non significa consegnato, letto o risposto.

Non inserire password, token o codici di accesso nei prompt o nel repository. Un collegamento MCP va autorizzato nel tuo ambiente secondo il provider, non tramite segreti incollati nella chat.

## 7. Produzione ed editoria: esempi pronti

> ACO, organizza ingest, montaggio, conform, color, suono e consegna di questo film. Ho bisogno prima delle domande essenziali e poi di un piano operativo.

> ACO, ritocca queste immagini prodotto preservando forma, logo ed etichette. Se non hai il software, scrivi il brief operativo per il ritoccatore.

> ACO, costruisci questo workflow ComfyUI usando la mia versione e i nodi realmente installati. Non installare nulla senza autorizzazione.

> ACO, porta questo manoscritto da editing a impaginazione, proof, stampa/EPUB e distribuzione. Tieni diritti e approvazioni sotto controllo.

> ACO, struttura una newsletter o un podcast per questa media company, con flusso editoriale, ricavi e controllo delle fonti.

Le figure sono metodi di lavoro, non software o persone assunte. Un colorist senza filmato/software non ha colorato il film. Un agente per ComfyUI senza un’esecuzione verificata produce un workflow o un piano non collaudato. Un progetto editoriale preparato non è già pubblicato.

## 8. Se vuoi meno testo

Scrivi **“modalità ACTION, solo risultato e problemi essenziali”**. Per spiegazioni chiedi **EXPLAIN**. ACO deve comunque chiedere subito i punti decisivi che mancano e non nascondere errori, costi o esiti incerti.

## 9. Quando hai finito

> Registra cosa abbiamo fatto, quali decisioni ho approvato, i file prodotti e cosa manca. Dimmi se è salvato su Drive oppure soltanto localmente.

Nessuna attività continua a chat chiusa senza un vero sistema pianificato autorizzato. Non è sufficiente scriverlo nel prompt.

**Regola da ricordare:** GitHub = istruzioni pubbliche; Drive = dati privati; Codex/ChatGPT = ambiente che lavora. Pubblicare su GitHub non installa nulla e non invia nessun messaggio.
